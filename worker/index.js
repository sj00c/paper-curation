// Cloudflare Worker entry — serves static assets and exposes POST /api/embed
// as a query embedding proxy for the Deep Research RAG UI.
//
// Secrets (set via `npx wrangler secret put <NAME>`):
//   GOOGLE_API_KEY  — Google AI Studio key. Required for /api/embed (Gemini
//                      gemini-embedding-001). Keeps the key server-side so the
//                      browser never sees it.
//
// Limits:
//   - /api/embed: 2000-char query cap, single embedContent call per request.

// Deep Research 쿼리 임베딩 프록시 — index 와 동일한 gemini-embedding-001 을
// RETRIEVAL_QUERY task 로 호출한다. 768D 출력은 비정규화 상태로 오므로
// (output_dimensionality != 3072 이면 항상) 서버에서 L2 정규화한 뒤 돌려준다.
const EMBED_MODEL = "gemini-embedding-001";
const EMBED_DIM = 768;
const MAX_QUERY_CHARS = 2000;

function jsonResponse(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
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

  const apiUrl =
    `https://generativelanguage.googleapis.com/v1beta/models/${EMBED_MODEL}:embedContent`;
  const payload = {
    model: `models/${EMBED_MODEL}`,
    content: { parts: [{ text }] },
    taskType: "RETRIEVAL_QUERY",
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
  return jsonResponse({ embedding, model: EMBED_MODEL, dim: EMBED_DIM }, 200);
}

async function allowEmbedRequest(request, env) {
  if (!env.EMBED_RATE_LIMITER) {
    return jsonResponse({ error: "Rate limiter is not configured" }, 503);
  }
  const origin = request.headers.get("Origin");
  if (origin && origin !== new URL(request.url).origin) {
    return jsonResponse({ error: "Cross-origin requests are not allowed" }, 403);
  }
  const key = request.headers.get("CF-Connecting-IP") || "unknown";
  const result = await env.EMBED_RATE_LIMITER.limit({ key });
  return result.success
    ? null
    : jsonResponse({ error: "Embedding rate limit exceeded" }, 429);
}

function secureResponse(resp) {
  const headers = new Headers(resp.headers);
  headers.set("X-Content-Type-Options", "nosniff");
  headers.set("X-Frame-Options", "DENY");
  headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  headers.set("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  headers.set(
    "Content-Security-Policy",
    "frame-ancestors 'none'; base-uri 'self'; object-src 'none'");
  return new Response(resp.body, {
    status: resp.status,
    statusText: resp.statusText,
    headers,
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/embed") {
      if (request.method !== "POST") {
        return secureResponse(new Response("Method Not Allowed", {
          status: 405,
          headers: { "Allow": "POST" },
        }));
      }
      const denied = await allowEmbedRequest(request, env);
      return secureResponse(denied || await handleEmbed(request, env));
    }
    // Everything else falls through to the static-assets binding.
    return secureResponse(await env.ASSETS.fetch(request));
  },
};
