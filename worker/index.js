// Cloudflare Worker entry — serves static assets from docs/ via the
// ASSETS binding, intercepts POST /api/audio-email to forward the generated
// MP3 to Resend for email delivery, and exposes POST /api/embed as a query
// embedding proxy for the Deep Research RAG UI (Gemini embeddings).
//
// Secrets (set via `npx wrangler secret put <NAME>`):
//   RESEND_API_KEY  — Resend API key (re_xxx). Required for /api/audio-email.
//   AUDIO_REPLY_TO  — Optional. Reply-To header (e.g. "jehyun.lee@gmail.com")
//                      so visitors' replies land in the operator's inbox even
//                      though the From: stays on resend.dev.
//   AUDIO_FROM      — Optional. Override "From:" address. Defaults to
//                      "Paper Curation <onboarding@resend.dev>" (Resend's
//                      shared sandbox sender — only delivers to the Resend
//                      account email until a custom domain is verified).
//   GOOGLE_API_KEY  — Google AI Studio key. Required for /api/embed (Gemini
//                      gemini-embedding-001). Keeps the key server-side so the
//                      browser never sees it.
//
// Limits:
//   - 25 MB request body (Resend attachment cap), 10 recipients max.
//   - One Resend call per recipient (Resend free tier: 100 mails/day).
//   - /api/embed: 2000-char query cap, single embedContent call per request.

const DEFAULT_FROM = "Paper Curation <onboarding@resend.dev>";
const MAX_ATTACHMENT_BYTES = 25 * 1024 * 1024;
const MAX_RECIPIENTS = 10;

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

// Deep Research 쿼리 임베딩 프록시 — document index metadata must match the
// Python search_index_metadata.py contract, while the query call deliberately
// uses RETRIEVAL_QUERY for Gemini's asymmetric retrieval embedding.
const INDEX_SCHEMA_VERSION = 1;
const EMBED_PROVIDER = "google";
const EMBED_MODEL = "gemini-embedding-001";
const INDEX_TASK_TYPE = "RETRIEVAL_DOCUMENT";
const QUERY_TASK_TYPE = "RETRIEVAL_QUERY";
const EMBED_DIM = 768;
const EMBED_QUANT = "int8-l2norm";
const CHUNK_HASH_BASIS = "sha256(model + '\\n' + text)";
const SIDECAR_FORMAT_VERSION = 1;
const CACHE_FORMAT_VERSION = 1;
const PROVENANCE_STATUS = "local-current";
const EMBED_SIDECAR_FILE = "_search_index_emb.bin";
const REBUILD_GUIDANCE = "Rebuild the local search index with pipeline/build_search_index.py; validation never rebuilds automatically.";
const MAX_QUERY_CHARS = 2000;

function bytesToBase64(bytes) {
  // Workers runtime has btoa but it expects a binary string. Build it in
  // 32 KB chunks so we don't blow the call-stack on multi-MB attachments.
  let s = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    s += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(s);
}

async function handleAudioEmail(request, env) {
  if (!env.RESEND_API_KEY) {
    return new Response("RESEND_API_KEY not configured on Worker", { status: 503 });
  }

  let form;
  try {
    form = await request.formData();
  } catch (e) {
    return new Response("Invalid form data", { status: 400 });
  }

  const recipients = form.getAll("email")
    .map(v => String(v).trim())
    .filter(v => EMAIL_RE.test(v));
  if (!recipients.length) {
    return new Response("No valid recipient", { status: 400 });
  }
  if (recipients.length > MAX_RECIPIENTS) {
    return new Response(`Too many recipients (max ${MAX_RECIPIENTS})`, { status: 400 });
  }

  const file = form.get("mp3");
  if (!file || typeof file === "string") {
    return new Response("Missing mp3 attachment", { status: 400 });
  }
  const buf = await file.arrayBuffer();
  if (buf.byteLength > MAX_ATTACHMENT_BYTES) {
    return new Response("Attachment too large", { status: 413 });
  }
  const b64 = bytesToBase64(new Uint8Array(buf));

  const filename = String(form.get("filename") || file.name || "audio-overview.mp3");
  const title = String(form.get("title") || "Audio Overview");
  const lang = String(form.get("lang") || "ko");
  const isKo = lang === "ko";

  const subject = isKo
    ? `[Paper Curation] Audio Overview: ${title}`
    : `[Paper Curation] Audio Overview: ${title}`;
  const html = isKo
    ? `<p>요청하신 Audio Overview 가 첨부되어 있습니다.</p>
       <p><b>제목</b>: ${escapeHtml(title)}</p>
       <p>이 메일은 Paper Curation 의 자동 발송입니다. 답장은 운영자에게 전달됩니다.</p>`
    : `<p>Your requested Audio Overview is attached.</p>
       <p><b>Title</b>: ${escapeHtml(title)}</p>
       <p>This is an automated message from Paper Curation. Replies route to the operator.</p>`;

  const payloadBase = {
    from: env.AUDIO_FROM || DEFAULT_FROM,
    subject,
    html,
    attachments: [{ filename, content: b64 }],
  };
  if (env.AUDIO_REPLY_TO) payloadBase.reply_to = env.AUDIO_REPLY_TO;

  const results = await Promise.all(recipients.map(async (to) => {
    const payload = { ...payloadBase, to: [to] };
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    const text = await r.text();
    return { to, ok: r.ok, status: r.status, body: text.slice(0, 400) };
  }));

  const anyFail = results.some(r => !r.ok);
  const status = anyFail ? 502 : 200;
  return new Response(JSON.stringify({ results }), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

function jsonResponse(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
function metadataError(key, expected, actual) {
  return `${key} expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}. ${REBUILD_GUIDANCE}`;
}

function hasAnyKey(payload, keys) {
  return keys.some(k => Object.prototype.hasOwnProperty.call(payload || {}, k));
}

function contractShapeError(payload, expected) {
  if (!payload || typeof payload !== "object") return "";
  let canonicalComplete = true;
  for (const key of Object.keys(expected)) {
    if (key === "emb_file") continue;
    if (!Object.prototype.hasOwnProperty.call(payload, key)) canonicalComplete = false;
  }
  const hasCanonicalOnly = hasAnyKey(payload, CANONICAL_ONLY_CONTRACT_KEYS);
  const hasLegacyOnly = hasAnyKey(payload, LEGACY_ONLY_CONTRACT_KEYS);
  const hasShared = hasAnyKey(payload, VERSIONED_SHARED_CONTRACT_KEYS);
  const hasShortenedVersioned = hasAnyKey(payload, SHORTENED_VERSIONED_CONTRACT_KEYS);
  if (hasShortenedVersioned) {
    return `shortened versioned metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`;
  }
  if (hasCanonicalOnly && hasLegacyOnly) {
    return `mixed canonical and legacy metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`;
  }
  if (hasCanonicalOnly && !canonicalComplete) {
    return `partial canonical metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`;
  }
  if (hasShared && !canonicalComplete) {
    return `partial versioned metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`;
  }
  return "";
}

const CANONICAL_CONTRACT_KEYS = [
  "index_schema_version", "embedding_provider", "embedding_model",
  "embedding_task_type", "embedding_dimension", "embedding_quantization",
  "chunk_hash_basis", "sidecar_format_version", "cache_format_version",
  "source_provenance_approval_status",
];
const CANONICAL_ONLY_CONTRACT_KEYS = [
  "index_schema_version", "embedding_provider", "embedding_model",
  "embedding_task_type", "embedding_dimension", "embedding_quantization",
  "source_provenance_approval_status",
];
const LEGACY_CONTRACT_KEY_MAP = {
  model: "embedding_model",
  dim: "embedding_dimension",
  quant: "embedding_quantization",
};
const LEGACY_ONLY_CONTRACT_KEYS = [
  "model", "dim", "quant",
];
const SHORTENED_VERSIONED_CONTRACT_KEYS = [
  "schema_version", "provider", "task_type", "provenance_status",
];
const VERSIONED_SHARED_CONTRACT_KEYS = [
  "chunk_hash_basis", "sidecar_format_version", "cache_format_version",
];


function expectedIndexMetadata() {
  return {
    index_schema_version: INDEX_SCHEMA_VERSION,
    embedding_provider: EMBED_PROVIDER,
    embedding_model: EMBED_MODEL,
    embedding_task_type: INDEX_TASK_TYPE,
    embedding_dimension: EMBED_DIM,
    embedding_quantization: EMBED_QUANT,
    chunk_hash_basis: CHUNK_HASH_BASIS,
    sidecar_format_version: SIDECAR_FORMAT_VERSION,
    cache_format_version: CACHE_FORMAT_VERSION,
    source_provenance_approval_status: PROVENANCE_STATUS,
    emb_file: EMBED_SIDECAR_FILE,
  };
}

function validateKnownSafeLegacyIndex(payload) {
  const errors = [];
  if (!payload || typeof payload !== "object") {
    return { ok: false, errors: [`index metadata missing. ${REBUILD_GUIDANCE}`] };
  }
  const expected = expectedIndexMetadata();
  const shapeError = contractShapeError(payload, expected);
  if (shapeError) return { ok: false, errors: [shapeError] };
  const hasCanonical = hasAnyKey(payload, CANONICAL_ONLY_CONTRACT_KEYS);
  const hasLegacy = hasAnyKey(payload, LEGACY_ONLY_CONTRACT_KEYS);
  const hasShared = hasAnyKey(payload, VERSIONED_SHARED_CONTRACT_KEYS);
  const hasShortenedVersioned = hasAnyKey(payload, SHORTENED_VERSIONED_CONTRACT_KEYS);
  if (hasShortenedVersioned) {
    return { ok: false, errors: [`shortened versioned metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`] };
  }
  if (hasCanonical && hasLegacy) {
    return { ok: false, errors: [`mixed canonical and legacy metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`] };
  }
  if (hasCanonical) {
    return { ok: false, errors: [`partial canonical metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`] };
  }
  if (hasShared) {
    return { ok: false, errors: [`partial versioned metadata is not known-safe legacy. ${REBUILD_GUIDANCE}`] };
  }
  if (payload.model !== EMBED_MODEL) errors.push(metadataError("model", EMBED_MODEL, payload.model));
  if (payload.dim !== EMBED_DIM) errors.push(metadataError("dim", EMBED_DIM, payload.dim));
  if (payload.quant !== EMBED_QUANT) errors.push(metadataError("quant", EMBED_QUANT, payload.quant));
  if (payload.emb_file != null && payload.emb_file !== EMBED_SIDECAR_FILE) {
    errors.push(metadataError("emb_file", EMBED_SIDECAR_FILE, payload.emb_file));
  }
  return { ok: errors.length === 0, errors };
}

function validateIndexMetadata(payload) {
  const expected = expectedIndexMetadata();
  const shapeError = contractShapeError(payload, expected);
  if (shapeError) return { ok: false, errors: [shapeError] };
  const errors = [];
  for (const key of Object.keys(expected)) {
    if (!payload || payload[key] !== expected[key]) {
      errors.push(metadataError(key, expected[key], payload && payload[key]));
    }
  }
  if (!errors.length) return { ok: true, errors: [] };
  const legacy = validateKnownSafeLegacyIndex(payload);
  if (legacy.ok) return legacy;
  return { ok: false, errors };
}

// gemini-embedding-001 은 outputDimensionality != 3072 일 때 비정규화 벡터를
// 돌려준다 (공식 가이드 명시). int8 양자화 전 단계와 동일하게 코사인 검색을
// 쓰려면 반드시 단위 벡터로 맞춰야 하므로 여기서 L2 정규화한다.
function l2normalize(vec) {
  let sumSq = 0;
  for (let i = 0; i < vec.length; i++) sumSq += vec[i] * vec[i];
  const norm = Math.sqrt(sumSq);
  if (!(norm > 0)) return vec.slice();
  const out = new Array(vec.length);
  for (let i = 0; i < vec.length; i++) out[i] = vec[i] / norm;
  return out;
}

async function handleEmbed(request, env) {
  if (!env.GOOGLE_API_KEY) {
    return jsonResponse(
      { error: "GOOGLE_API_KEY not configured on Worker" }, 503);
  }

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse({ error: "Invalid JSON body" }, 400);
  }

  const text = (body && typeof body.text === "string") ? body.text.trim() : "";
  if (!text) {
    return jsonResponse({ error: "Missing or empty 'text'" }, 400);
  }
  if (text.length > MAX_QUERY_CHARS) {
    return jsonResponse(
      { error: `Query too long (max ${MAX_QUERY_CHARS} chars)` }, 413);
  }
  const meta = validateIndexMetadata(body && body.index_metadata);
  if (!meta.ok) {
    return jsonResponse(
      { error: "Incompatible document index metadata", detail: meta.errors.join("; ") },
      409);
  }


  const apiUrl =
    `https://generativelanguage.googleapis.com/v1beta/models/${EMBED_MODEL}:embedContent`;
  const payload = {
    model: `models/${EMBED_MODEL}`,
    content: { parts: [{ text }] },
    taskType: QUERY_TASK_TYPE,
    outputDimensionality: EMBED_DIM,
  };

  let upstream;
  try {
    upstream = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // 키를 URL 쿼리스트링이 아닌 헤더로 — 로그/리퍼러 유출 방지.
        "x-goog-api-key": env.GOOGLE_API_KEY,
      },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    return jsonResponse({ error: "Embedding upstream request failed" }, 502);
  }

  if (!upstream.ok) {
    const detail = (await upstream.text()).slice(0, 400);
    return jsonResponse(
      { error: "Embedding upstream error", status: upstream.status, detail },
      502);
  }

  let data;
  try {
    data = await upstream.json();
  } catch (e) {
    return jsonResponse({ error: "Invalid embedding response" }, 502);
  }

  const values = data && data.embedding && data.embedding.values;
  if (!Array.isArray(values) || values.length !== EMBED_DIM) {
    return jsonResponse({ error: "Unexpected embedding shape" }, 502);
  }

  const embedding = l2normalize(values);
  return jsonResponse({
    embedding,
    embedding_model: EMBED_MODEL,
    embedding_provider: EMBED_PROVIDER,
    embedding_task_type: QUERY_TASK_TYPE,
    embedding_dimension: EMBED_DIM,
  }, 200);
}

// Local pages (localhost / file://) call these APIs cross-origin — without
// CORS headers the browser cannot read the response and reports the send as
// failed even when the mail actually went out.
function corsPreflight() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
    },
  });
}

function withCors(resp) {
  const h = new Headers(resp.headers);
  h.set("Access-Control-Allow-Origin", "*");
  return new Response(resp.body, { status: resp.status, headers: h });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/audio-email") {
      if (request.method === "OPTIONS") return corsPreflight();
      if (request.method !== "POST") {
        return new Response("Method Not Allowed", {
          status: 405,
          headers: { "Allow": "POST" },
        });
      }
      return withCors(await handleAudioEmail(request, env));
    }
    if (url.pathname === "/api/embed") {
      if (request.method === "OPTIONS") return corsPreflight();
      if (request.method !== "POST") {
        return new Response("Method Not Allowed", {
          status: 405,
          headers: { "Allow": "POST" },
        });
      }
      return withCors(await handleEmbed(request, env));
    }
    // Everything else falls through to the static-assets binding.
    return env.ASSETS.fetch(request);
  },
};
