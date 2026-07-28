import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import { spawn } from 'node:child_process';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const encoder = path.join(root, 'bin/audio-encode-lamejs.mjs');
const canonical = (value) => Buffer.from(JSON.stringify(Object.fromEntries(Object.entries(value).sort(([a], [b]) => a.localeCompare(b)))));
const digest = (value) => crypto.createHash('sha256').update(value).digest('hex');

function run(frames, setup = () => {}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'audio-codec-'));
  fs.chmodSync(directory, 0o700);
  setup(directory);
  const child = spawn(process.execPath, [encoder], { stdio: ['ignore', 'ignore', 'ignore', 'pipe'] });
  const channel = child.stdio[3];
  const key = crypto.randomBytes(32);
  const nonce = crypto.randomBytes(32).toString('base64url');
  const bootstrap = canonical({ key: key.toString('base64url'), nonce, parent_pid: process.pid, type: 'bootstrap' });
  channel.write(Buffer.concat([Buffer.from([0, 0, bootstrap.length >> 8, bootstrap.length & 255]), bootstrap]));
  let sequence = 0;
  for (const input of frames(directory)) {
    const unsigned = { ...input, schema: 1, nonce, sequence: ++sequence };
    const mac = crypto.createHmac('sha256', key).update(canonical(unsigned)).digest('hex');
    channel.write(Buffer.concat([canonical({ ...unsigned, mac: input.badMac ? mac.replace(/^./, '0') : mac }), Buffer.from('\n')]));
  }
  channel.end();
  return new Promise((resolve, reject) => {
    let output = '';
    channel.setEncoding('utf8');
    channel.on('data', (part) => { output += part; });
    child.on('error', reject);
    child.on('close', (status) => {
      const mp3Path = path.join(directory, 'audio.mp3');
      const mp3 = fs.existsSync(mp3Path) ? fs.readFileSync(mp3Path) : Buffer.alloc(0);
      fs.rmSync(directory, { recursive: true, force: true });
      resolve({ status, mp3, replies: output.trim() ? output.trim().split('\n').map(JSON.parse) : [] });
    });
  });
}
function writePcm(directory, ordinal, pcm) {
  const target = path.join(directory, `pcm-${ordinal}.s16le`);
  fs.writeFileSync(target, pcm, { mode: 0o600 }); fs.chmodSync(target, 0o600);
  return target;
}
function sine(samples, phase = 0) {
  const pcm = Buffer.alloc(samples * 2);
  for (let i = 0; i < samples; i += 1) pcm.writeInt16LE(Math.round(Math.sin((i + phase) / 12) * 12000), i * 2);
  return pcm;
}
function normalFrames(directory, chunks) {
  const output = path.join(directory, 'audio.mp3');
  return [
    { type: 'start', operation_id: 'audio-test', output_path: output, sample_rate: 24000, channels: 1, sample_format: 's16le', bitrate_kbps: 128, chunk_count: chunks.length },
    ...chunks.map((pcm, index) => ({ type: 'chunk', operation_id: 'audio-test', ordinal: index + 1, path: writePcm(directory, index + 1, pcm), length: pcm.length, sha256: digest(pcm) })),
    { type: 'finish', operation_id: 'audio-test' },
  ];
}

test('encodes deterministic playable CBR MP3 for one and four ordered chunks with exact gap input', async () => {
  const one = await run((directory) => normalFrames(directory, [sine(2400)]));
  assert.equal(one.status, 0); assert.deepEqual(one.replies.map((reply) => reply.type), ['started', 'chunk_accepted', 'completed']);
  assert.ok(one.mp3.length > 0); assert.equal(one.mp3.subarray(0, 3).toString('hex'), 'fff3c4');
  const four = await run((directory) => normalFrames(directory, [sine(2400), sine(2400, 1), sine(2400, 2), sine(2400, 3)]), (directory) => { fs.mkdirSync(path.join(directory, 'unused')); });
  assert.equal(four.status, 0); assert.deepEqual(four.replies.map((reply) => reply.type), ['started', 'chunk_accepted', 'chunk_accepted', 'chunk_accepted', 'chunk_accepted', 'completed']);
  assert.ok(four.mp3.length > one.mp3.length);
  const repeat = await run((directory) => normalFrames(directory, [sine(2400)]));
  assert.equal(repeat.status, 0);
  assert.equal(digest(one.mp3), digest(repeat.mp3));
});

// D1: the inter-chunk gap is a cross-boundary contract. `pipeline/lib/audio_operation.py`
// derives SILENCE_SAMPLES = round(GAP_SECONDS * PCM_SAMPLE_RATE) = 6000 and a Python test
// pins the declaration below; this asserts the codec BEHAVIOURALLY emits that gap, so a
// silent drift back to 200 ms (4800 samples) cannot pass the Node suite.
const SAMPLES_PER_FRAME = 576; // MPEG-2 Layer III at 24 kHz
function encodedSamples(mp3) {
  const bitrates = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160, 0];
  let index = 0;
  let frames = 0;
  while (index < mp3.length - 4) {
    if (mp3[index] === 0xff && (mp3[index + 1] & 0xe0) === 0xe0 && ((mp3[index + 1] >> 1) & 0x03) === 1) {
      const bitrateIndex = (mp3[index + 2] >> 4) & 0x0f;
      const padding = (mp3[index + 2] >> 1) & 0x01;
      if (bitrateIndex !== 0 && bitrateIndex !== 15) {
        frames += 1;
        index += Math.floor((SAMPLES_PER_FRAME / 8) * bitrates[bitrateIndex] * 1000 / 24000) + padding;
        continue;
      }
    }
    index += 1;
  }
  return frames * SAMPLES_PER_FRAME;
}

test('inserts exactly one 6000-sample (250 ms) gap between accepted chunks', async () => {
  const declared = fs.readFileSync(encoder, 'utf8').match(/\bSILENCE_SAMPLES\s*=\s*([0-9][0-9_]*)\s*;/g) ?? [];
  assert.equal(declared.length, 1, `codec must declare SILENCE_SAMPLES exactly once, found ${declared}`);
  assert.equal(Number(declared[0].split('=')[1].replace(/[^0-9]/g, '')), 6000);

  const joined = await run((directory) => normalFrames(directory, [sine(1200), sine(1200, 1)]));
  const contiguous = await run((directory) => normalFrames(directory, [sine(2400)]));
  assert.equal(joined.status, 0);
  assert.equal(contiguous.status, 0);

  // The two runs carry identical PCM payloads; the only difference is one gap.
  const measuredGap = encodedSamples(joined.mp3) - encodedSamples(contiguous.mp3);
  assert.ok(
    Math.abs(measuredGap - 6000) <= SAMPLES_PER_FRAME,
    `expected a ~6000-sample gap, measured ${measuredGap} (a 200 ms/4800-sample regression is ${Math.abs(4800 - 6000)} off)`,
  );
});

test('rejects bad MAC, digest, ordinal, format, arbitrary path, and +1 PCM bound', async (t) => {
  const cases = [
    ['bad MAC', (directory) => [{ ...normalFrames(directory, [sine(2)])[0], badMac: true }]],
    ['bad digest', (directory) => { const frames = normalFrames(directory, [sine(2)]); frames[1].sha256 = '0'.repeat(64); return frames; }],
    ['ordinal gap/four-slot discipline', (directory) => { const frames = normalFrames(directory, [sine(2), sine(2), sine(2), sine(2), sine(2)]); frames[1].ordinal = 5; frames[1].path = path.join(directory, 'pcm-5.s16le'); return frames; }],
    ['format', (directory) => { const frames = normalFrames(directory, [sine(2)]); frames[0].sample_rate = 24001; return frames; }],
    ['arbitrary path', (directory) => { const frames = normalFrames(directory, [sine(2)]); frames[1].path = path.join(directory, 'other.pcm'); return frames; }],
    ['PCM +1 bound', (directory) => { const frames = normalFrames(directory, [sine(2)]); frames[1].length = 6 * 1024 * 1024 + 1; return frames; }],
  ];
  for (const [name, frames] of cases) await t.test(name, async () => { const result = await run(frames); assert.notEqual(result.status, 0); assert.equal(result.replies.at(-1)?.type, 'error'); });
});

test('rejects symlink and hardlink PCM sources and cancel removes partial output', async () => {
  for (const linked of ['symlink', 'hardlink']) {
    const result = await run((directory) => {
      const pcm = sine(2); const source = writePcm(directory, 1, pcm); const replacement = path.join(directory, 'replacement.pcm');
      fs.renameSync(source, replacement);
      if (linked === 'symlink') fs.symlinkSync(replacement, source); else fs.linkSync(replacement, source);
      return [
        { type: 'start', operation_id: 'audio-test', output_path: path.join(directory, 'audio.mp3'), sample_rate: 24000, channels: 1, sample_format: 's16le', bitrate_kbps: 128, chunk_count: 1 },
        { type: 'chunk', operation_id: 'audio-test', ordinal: 1, path: source, length: pcm.length, sha256: digest(pcm) },
        { type: 'finish', operation_id: 'audio-test' },
      ];
    });
    assert.notEqual(result.status, 0, linked); assert.equal(result.replies.at(-1)?.type, 'error');
  }
  const cancelled = await run((directory) => {
    const frames = normalFrames(directory, [sine(2400)]); frames.splice(2, 1, { type: 'cancel', operation_id: 'audio-test', reason_code: 'user_cancelled' }); return frames;
  });
  assert.equal(cancelled.status, 0); assert.equal(cancelled.replies.at(-1)?.type, 'cancelled'); assert.equal(cancelled.mp3.length, 0);
});

test('MP3 output carries no source prose or ID3 tag', async () => {
  const sourceProse = 'DO-NOT-EMBED-SOURCE-PROSE';
  const result = await run((directory) => normalFrames(directory, [sine(2400)]));
  assert.equal(result.status, 0);
  assert.equal(result.replies.at(-1)?.type, 'completed');
  assert.ok(result.replies.at(-1).bytes > 0);
  assert.equal(result.mp3.subarray(0, 3).equals(Buffer.from('ID3')), false);
  assert.equal(result.mp3.includes(Buffer.from(sourceProse)), false);
});

// D3/A3: the framing headroom is a MEASURED property of the vendored encoder, not a trusted
// constant. The codec reserves FRAMING_RESERVE_SECONDS out of the 3600 s hard ceiling and admits
// chunks against the remaining budget BEFORE encoding them. These tests read the codec's own
// declarations so a silent edit to either constant is caught, and re-measure the delay rather
// than asserting a golden number.
function codecConstants(names) {
  const source = fs.readFileSync(encoder, 'utf8');
  const declarations = names.map((name) => {
    const found = source.match(new RegExp(`^const ${name} = .+;$`, 'gm')) ?? [];
    assert.equal(found.length, 1, `codec must declare ${name} exactly once, found ${found.length}`);
    return found[0];
  });
  return vm.runInNewContext(`${declarations.join('\n')}\n({ ${names.join(', ')} })`);
}
function vendoredLame() {
  const source = fs.readFileSync(path.join(root, 'vendor/lamejs/lame.all.js'), 'utf8');
  const lamejs = vm.runInThisContext(`${source}\nlamejs`, { filename: 'vendor/lamejs/lame.all.js' });
  assert.equal(typeof lamejs?.Mp3Encoder, 'function', 'vendored lamejs is unavailable');
  return lamejs;
}
function encodeDirect(lamejs, pcm) {
  const samples = new Int16Array(pcm.length / 2);
  for (let index = 0; index < samples.length; index += 1) samples[index] = pcm.readInt16LE(index * 2);
  const instance = new lamejs.Mp3Encoder(1, 24000, 128);
  const parts = [];
  const block = 32768; // the codec's 64 KiB PCM read block, in samples
  for (let offset = 0; offset < samples.length; offset += block) {
    const slice = samples.subarray(offset, Math.min(offset + block, samples.length));
    parts.push(Buffer.from(instance.encodeBuffer(slice, slice)));
  }
  parts.push(Buffer.from(instance.flush()));
  return Buffer.concat(parts);
}
function addedFraming(mp3, inputSamples) {
  const covered = encodedSamples(mp3);
  const frames = covered / SAMPLES_PER_FRAME;
  assert.ok(Number.isInteger(frames) && frames > 0, `parsed no MPEG-2 Layer III frames for ${inputSamples} samples`);
  assert.ok(covered >= inputSamples, `${frames} frames cannot cover ${inputSamples} samples`);
  return { frames, added: covered - inputSamples };
}

test('golden vector MEASURES the lamejs framing delay over a full residue sweep and it fits the reserve', async (t) => {
  const { FRAMING_RESERVE_SECONDS } = codecConstants(['FRAMING_RESERVE_SECONDS']);
  const lamejs = vendoredLame();
  const base = SAMPLES_PER_FRAME * 4;
  let worst = { added: -1 };
  for (let residue = 0; residue < SAMPLES_PER_FRAME; residue += 1) {
    const inputSamples = base + residue;
    const { frames, added } = addedFraming(encodeDirect(lamejs, sine(inputSamples)), inputSamples);
    if (added > worst.added) worst = { inputSamples, residue, frames, added };
  }
  const seconds = worst.added / 24000;
  t.diagnostic(`measured worst-case added framing over ${SAMPLES_PER_FRAME} residues: ${worst.added} samples = ${seconds.toFixed(6)} s (${worst.inputSamples} samples in, residue ${worst.residue}, ${worst.frames} frames); reserve ${FRAMING_RESERVE_SECONDS} s leaves ${(FRAMING_RESERVE_SECONDS - seconds).toFixed(6)} s headroom`);
  assert.ok(worst.added >= 0 && worst.added < SAMPLES_PER_FRAME * 4, `added framing ${worst.added} is implausible for ${SAMPLES_PER_FRAME}-sample frames`);
  assert.ok(seconds <= FRAMING_RESERVE_SECONDS, `measured framing delay ${seconds.toFixed(6)} s exceeds the declared reserve of ${FRAMING_RESERVE_SECONDS} s`);

  // Re-measure end to end through the real codec child. Byte identity ties the in-process sweep
  // above to exactly what the codec emits, so the sweep cannot drift away from production.
  const probes = [SAMPLES_PER_FRAME * 8, SAMPLES_PER_FRAME * 8 + 1, worst.inputSamples];
  assert.ok(probes.some((n) => n % SAMPLES_PER_FRAME === 0), 'probes must include a frame-aligned length');
  assert.ok(probes.some((n) => n % SAMPLES_PER_FRAME !== 0), 'probes must include a non-frame-aligned length');
  for (const inputSamples of probes) {
    const pcm = sine(inputSamples);
    const result = await run((directory) => normalFrames(directory, [pcm]));
    assert.equal(result.status, 0, `codec rejected ${inputSamples} samples`);
    assert.equal(digest(result.mp3), digest(encodeDirect(lamejs, pcm)), `codec output diverged from the in-process encode at ${inputSamples} samples`);
    const { added } = addedFraming(result.mp3, inputSamples);
    assert.ok(added / 24000 <= FRAMING_RESERVE_SECONDS, `codec added ${added} samples of framing at ${inputSamples} samples`);
  }
});

test('admission rejects an over-budget chunk before any of its PCM is opened, read or encoded', async () => {
  const source = fs.readFileSync(encoder, 'utf8');
  const body = source.slice(source.indexOf('function chunk(frame) {'), source.indexOf('function finish(frame) {'));
  const gate = body.indexOf('ADMISSION_SAMPLES');
  assert.ok(gate >= 0, 'chunk() must gate on ADMISSION_SAMPLES');
  assert.ok(gate < body.indexOf('ownedInput('), 'admission must run before the PCM file is opened');
  assert.ok(gate < body.indexOf('encodeSamples('), 'admission must run before any sample is encoded');

  const { MAX_SAMPLES, ADMISSION_SAMPLES } = codecConstants(['MAX_SAMPLES', 'FRAMING_RESERVE_SECONDS', 'ADMISSION_SAMPLES']);
  const chunkSamples = (6 * 1024 * 1024) / 2; // MAX_PCM: the largest chunk the protocol accepts
  const accepted = 27;
  const before = accepted * chunkSamples + (accepted - 1) * 6000;
  // The offending chunk is sized so the projected total lands strictly inside the window between
  // the admission budget and the hard ceiling. Only the pre-dispatch gate can reject it: the
  // MAX_SAMPLES timeline checks would have admitted it and the operation would have completed.
  const offendingSamples = ADMISSION_SAMPLES - before - 6000 + Math.floor((MAX_SAMPLES - ADMISSION_SAMPLES) / 2);
  const projected = before + 6000 + offendingSamples;
  assert.ok(accepted + 1 <= 32, 'fixture must respect the 32-chunk protocol bound');
  assert.ok(before <= ADMISSION_SAMPLES, `fixture must keep the first ${accepted} chunks admissible`);
  assert.ok(offendingSamples > 0 && offendingSamples * 2 <= 6 * 1024 * 1024, 'offending chunk must be a legal PCM size');
  assert.ok(projected > ADMISSION_SAMPLES, `projected ${projected} must overrun the admission budget ${ADMISSION_SAMPLES}`);
  assert.ok(projected <= MAX_SAMPLES, `projected ${projected} must stay under the hard ceiling ${MAX_SAMPLES}, so only admission can reject it`);

  const bulk = sine(chunkSamples);
  const bulkSha = digest(bulk);
  const offending = sine(offendingSamples);
  const result = await run((directory) => [
    { type: 'start', operation_id: 'audio-test', output_path: path.join(directory, 'audio.mp3'), sample_rate: 24000, channels: 1, sample_format: 's16le', bitrate_kbps: 128, chunk_count: accepted + 1 },
    ...Array.from({ length: accepted }, (unused, index) => ({ type: 'chunk', operation_id: 'audio-test', ordinal: index + 1, path: writePcm(directory, index + 1, bulk), length: bulk.length, sha256: bulkSha })),
    { type: 'chunk', operation_id: 'audio-test', ordinal: accepted + 1, path: writePcm(directory, accepted + 1, offending), length: offending.length, sha256: digest(offending) },
    { type: 'finish', operation_id: 'audio-test' },
  ]);
  const types = result.replies.map((reply) => reply.type);
  assert.notEqual(result.status, 0);
  // The offending chunk is the one that fails: every earlier chunk was accepted, none later ran.
  assert.equal(types.filter((type) => type === 'chunk_accepted').length, accepted, `expected exactly ${accepted} accepted chunks, got ${types.join(',')}`);
  assert.equal(types.at(-1), 'error');
  assert.equal(types.includes('completed'), false);
  assert.equal(result.replies.at(-1).sequence, accepted + 2, 'the error must be bound to the offending chunk frame (start is sequence 1)');
  assert.equal(result.mp3.length, 0, 'a rejected operation must leave no audio.mp3 behind');
});

test('the pre-dispatch admission budget stays strictly below the hard sample ceiling', () => {
  const { MAX_SAMPLES, FRAMING_RESERVE_SECONDS, ADMISSION_SAMPLES } = codecConstants(['MAX_SAMPLES', 'FRAMING_RESERVE_SECONDS', 'ADMISSION_SAMPLES']);
  assert.equal(MAX_SAMPLES, 24000 * 3600, 'the hard codec ceiling must stay at 3600 s');
  assert.ok(FRAMING_RESERVE_SECONDS > 0, 'the framing reserve must be positive');
  assert.ok(ADMISSION_SAMPLES < MAX_SAMPLES, `admission (${ADMISSION_SAMPLES}) must stay strictly below the hard ceiling (${MAX_SAMPLES}); collapsing them deletes the framing reserve`);
  assert.equal(MAX_SAMPLES - ADMISSION_SAMPLES, Math.round(FRAMING_RESERVE_SECONDS * 24000), 'the gap between admission and the ceiling must be exactly the framing reserve');
  const source = fs.readFileSync(encoder, 'utf8');
  assert.equal((source.match(/> MAX_SAMPLES\) fail\('PCM timeline limit exceeded'\)/g) ?? []).length, 2, 'both defensive MAX_SAMPLES timeline checks must be retained alongside admission');
});
