#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const FD = 3;
const MAX_FRAME = 64 * 1024;
const MAX_PCM = 6 * 1024 * 1024;
const MAX_MP3 = 64 * 1024 * 1024;
const MAX_SAMPLES = 24_000 * 3_600;
// MEASURED, not assumed: the vendored lamejs@1.2.1 at 24 kHz emits MPEG-2 Layer III frames of
// 576 samples, and a full residue sweep (mod 576) measures a worst-case added framing of
// 1_727 samples = 0.071958 s, so 0.100 s holds with 0.028042 s of headroom. The golden vector
// in tests/audio-codec.test.mjs re-measures this instead of trusting the number.
const FRAMING_RESERVE_SECONDS = 0.100;
// Budget-derived pre-dispatch admission limit (3599.900 s of PCM). MAX_SAMPLES above stays the
// hard codec ceiling and its timeline checks below stay as defensive fails.
const ADMISSION_SAMPLES = Math.round((3_600 - FRAMING_RESERVE_SECONDS) * 24_000);
const BLOCK = 64 * 1024;
const MAX_WORKING_MEMORY = 8 * 1024 * 1024;
const SILENCE_SAMPLES = 6_000;
const uid = process.getuid?.();

function fail(message) { throw new Error(message); }
function canonical(value) {
  const visit = (item) => {
    if (item === null || typeof item === 'boolean') return item;
    if (typeof item === 'string') {
      if (item.normalize('NFC') !== item) fail('non-NFC string');
      return item;
    }
    if (typeof item === 'number') {
      if (!Number.isSafeInteger(item)) fail('non-integer number');
      return item;
    }
    if (Array.isArray(item)) return item.map(visit);
    if (!item || Object.getPrototypeOf(item) !== Object.prototype) fail('noncanonical value');
    const out = {};
    for (const key of Object.keys(item).sort()) {
      if (key.normalize('NFC') !== key || Object.hasOwn(out, key)) fail('noncanonical key');
      out[key] = visit(item[key]);
    }
    return out;
  };
  return Buffer.from(JSON.stringify(visit(value)));
}
function readExact(size) {
  const result = Buffer.allocUnsafe(size);
  let offset = 0;
  while (offset < size) {
    const count = fs.readSync(FD, result, offset, size - offset, null);
    if (count === 0) fail('fd3 closed');
    offset += count;
  }
  return result;
}
function bootstrap() {
  const size = readExact(4).readUInt32BE();
  if (!size || size > MAX_FRAME) fail('invalid bootstrap length');
  const raw = readExact(size);
  let value;
  try { value = JSON.parse(raw.toString('utf8')); } catch { fail('invalid bootstrap'); }
  if (!Buffer.from(canonical(value)).equals(raw) || Object.keys(value).sort().join(',') !== 'key,nonce,parent_pid,type' || value.type !== 'bootstrap') fail('invalid bootstrap');
  if (!Number.isSafeInteger(value.parent_pid) || value.parent_pid !== process.ppid) fail('bootstrap parent mismatch');
  const key = Buffer.from(value.key, 'base64url');
  const nonce = Buffer.from(value.nonce, 'base64url');
  if (key.length !== 32 || nonce.length !== 32 || key.toString('base64url') !== value.key || nonce.toString('base64url') !== value.nonce) fail('invalid bootstrap credentials');
  return { key, nonce: value.nonce };
}
function ownedDirectory(dir) {
  const info = fs.lstatSync(dir);
  if (!info.isDirectory() || info.isSymbolicLink() || (uid !== undefined && info.uid !== uid) || (info.mode & 0o777) !== 0o700) fail('unsafe operation directory');
}
function ownedInput(file, expectedLength) {
  const info = fs.lstatSync(file);
  if (!info.isFile() || info.isSymbolicLink() || info.nlink !== 1 || (uid !== undefined && info.uid !== uid) || (info.mode & 0o777) !== 0o600 || info.size !== expectedLength) fail('unsafe PCM input');
  const fd = fs.openSync(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  const opened = fs.fstatSync(fd);
  if (!opened.isFile() || opened.nlink !== 1 || opened.dev !== info.dev || opened.ino !== info.ino || opened.size !== expectedLength) { fs.closeSync(fd); fail('PCM changed while opening'); }
  return fd;
}
function loadLame() {
  const source = fs.readFileSync(new URL('../vendor/lamejs/lame.all.js', import.meta.url), 'utf8');
  const lamejs = vm.runInThisContext(`${source}\nlamejs`, { filename: 'vendor/lamejs/lame.all.js' });
  if (typeof lamejs?.Mp3Encoder !== 'function') fail('vendored lamejs is unavailable');
  return lamejs;
}
const { key, nonce } = bootstrap();
const lamejs = loadLame();
let expectedSequence = 1;
let state = null;
let line = Buffer.alloc(0);

function hmac(value) { return crypto.createHmac('sha256', key).update(canonical(value)).digest('hex'); }
function response(type, sequence, extra = {}) {
  const value = { schema: 1, type, operation_id: state?.operationId ?? '', nonce, sequence, ...extra };
  const wire = { ...value, mac: hmac(value) };
  fs.writeSync(FD, Buffer.concat([canonical(wire), Buffer.from('\n')]));
}
function reject(sequence, code) {
  try { response('error', Number.isSafeInteger(sequence) ? sequence : 0, { code }); } catch {}
  cleanup();
  process.exitCode = 1;
  return false;
}
function cleanup() {
  if (state?.outputFd !== undefined) { try { fs.closeSync(state.outputFd); } catch {} state.outputFd = undefined; }
  if (state?.outputPath) { try { fs.unlinkSync(state.outputPath); } catch {} }
}
function verifyFrame(raw) {
  let frame;
  try { frame = JSON.parse(raw.toString('utf8')); } catch { fail('invalid JSON frame'); }
  if (!canonical(frame).equals(raw)) fail('frame is not canonical JSON');
  const keys = Object.keys(frame);
  if (!keys.includes('mac')) fail('missing MAC');
  const { mac, ...unsigned } = frame;
  if (!/^[0-9a-f]{64}$/.test(mac) || !crypto.timingSafeEqual(Buffer.from(mac), Buffer.from(hmac(unsigned)))) fail('invalid MAC');
  if (frame.schema !== 1 || typeof frame.type !== 'string' || typeof frame.operation_id !== 'string' || frame.operation_id.length === 0 || frame.nonce !== nonce || !Number.isSafeInteger(frame.sequence) || frame.sequence !== expectedSequence) fail('invalid frame binding');
  expectedSequence += 1;
  return frame;
}
function start(frame) {
  const allowed = ['bitrate_kbps', 'channels', 'chunk_count', 'mac', 'nonce', 'operation_id', 'output_path', 'sample_format', 'sample_rate', 'schema', 'sequence', 'type'];
  if (frame.type !== 'start' || Object.keys(frame).some((key) => !allowed.includes(key)) || frame.sample_rate !== 24000 || frame.channels !== 1 || frame.sample_format !== 's16le' || frame.bitrate_kbps !== 128 || !Number.isSafeInteger(frame.chunk_count) || frame.chunk_count < 1 || frame.chunk_count > 32 || !path.isAbsolute(frame.output_path)) fail('invalid start');
  const outputPath = path.resolve(frame.output_path);
  const root = path.dirname(outputPath);
  if (path.basename(outputPath) !== 'audio.mp3' || outputPath !== path.join(root, 'audio.mp3')) fail('output path is not fixed');
  ownedDirectory(root);
  if (fs.existsSync(outputPath)) fail('output already exists');
  const outputFd = fs.openSync(outputPath, fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | fs.constants.O_NOFOLLOW, 0o600);
  const info = fs.fstatSync(outputFd);
  if (!info.isFile() || info.nlink !== 1 || (info.mode & 0o777) !== 0o600 || (uid !== undefined && info.uid !== uid)) { fs.closeSync(outputFd); fs.unlinkSync(outputPath); fail('unsafe output'); }
  state = { operationId: frame.operation_id, root, outputPath, outputFd, chunkCount: frame.chunk_count, nextOrdinal: 1, samples: 0, bytes: 0, encoder: new lamejs.Mp3Encoder(1, 24000, 128) };
  response('started', frame.sequence);
}
function writeEncoded(bytes) {
  if (!bytes?.length) return;
  state.bytes += bytes.length;
  if (state.bytes > MAX_MP3) fail('MP3 limit exceeded');
  fs.writeSync(state.outputFd, Buffer.from(bytes));
}
function encodeSamples(samples) { writeEncoded(state.encoder.encodeBuffer(samples, samples)); }
function pcmSamples(bytes) {
  const samples = new Int16Array(bytes.length / 2);
  for (let index = 0; index < samples.length; index += 1) samples[index] = bytes.readInt16LE(index * 2);
  return samples;
}
function chunk(frame) {
  const allowed = ['length', 'mac', 'nonce', 'operation_id', 'ordinal', 'path', 'schema', 'sequence', 'sha256', 'type'];
  if (frame.type !== 'chunk' || Object.keys(frame).some((key) => !allowed.includes(key)) || frame.operation_id !== state.operationId || frame.ordinal !== state.nextOrdinal || !Number.isSafeInteger(frame.length) || frame.length < 0 || frame.length > MAX_PCM || frame.length % 2 || !/^[0-9a-f]{64}$/.test(frame.sha256) || typeof frame.path !== 'string') fail('invalid chunk');
  // Pre-dispatch admission: reject on the DECLARED size, before any PCM is opened, read or encoded.
  if (state.samples + (frame.ordinal > 1 ? SILENCE_SAMPLES : 0) + frame.length / 2 > ADMISSION_SAMPLES) fail('PCM admission budget exceeded');
  const expected = path.join(state.root, `pcm-${frame.ordinal}.s16le`);
  if (path.resolve(frame.path) !== expected) fail('PCM path is not fixed');
  const fd = ownedInput(expected, frame.length);
  const digest = crypto.createHash('sha256');
  if (frame.ordinal > 1) {
    if (state.samples + SILENCE_SAMPLES > MAX_SAMPLES) fail('PCM timeline limit exceeded');
    encodeSamples(new Int16Array(SILENCE_SAMPLES));
    state.samples += SILENCE_SAMPLES;
  }
  try {
  if (BLOCK * 3 + SILENCE_SAMPLES * 2 > MAX_WORKING_MEMORY) fail('codec memory limit exceeded');
    const buffer = Buffer.allocUnsafe(Math.min(BLOCK, Math.max(frame.length, 1)));
    let remaining = frame.length;
    while (remaining) {
      const read = fs.readSync(fd, buffer, 0, Math.min(buffer.length, remaining), null);
      if (!read) fail('truncated PCM');
      const bytes = buffer.subarray(0, read);
      digest.update(bytes);
      encodeSamples(pcmSamples(bytes));
      state.samples += read / 2;
      if (state.samples > MAX_SAMPLES) fail('PCM timeline limit exceeded');
      remaining -= read;
    }
  } finally { fs.closeSync(fd); }
  if (digest.digest('hex') !== frame.sha256) fail('PCM digest mismatch');
  state.nextOrdinal += 1;
  response('chunk_accepted', frame.sequence, { ordinal: frame.ordinal });
}
function finish(frame) {
  const allowed = ['mac', 'nonce', 'operation_id', 'schema', 'sequence', 'type'];
  if (frame.type !== 'finish' || Object.keys(frame).some((key) => !allowed.includes(key)) || frame.operation_id !== state.operationId || state.nextOrdinal !== state.chunkCount + 1) fail('invalid finish');
  writeEncoded(state.encoder.flush());
  if (state.bytes === 0) fail('empty MP3');
  fs.closeSync(state.outputFd); state.outputFd = undefined;
  response('completed', frame.sequence, { bytes: state.bytes });
  state = null;
}
function cancel(frame) {
  const allowed = ['mac', 'nonce', 'operation_id', 'reason_code', 'schema', 'sequence', 'type'];
  if (frame.type !== 'cancel' || Object.keys(frame).some((key) => !allowed.includes(key)) || !/^[a-z0-9_.-]{1,64}$/.test(frame.reason_code) || (state && frame.operation_id !== state.operationId)) fail('invalid cancel');
  response('cancelled', frame.sequence, { reason_code: frame.reason_code });
  cleanup(); state = null;
}
function handle(raw) {
  let sequence;
  try {
    const frame = verifyFrame(raw); sequence = frame.sequence;
    if (frame.type === 'start' && !state) start(frame);
    else if (frame.type === 'chunk' && state) chunk(frame);
    else if (frame.type === 'finish' && state) finish(frame);
    else if (frame.type === 'cancel') cancel(frame);
    else fail('invalid state transition');
  } catch (error) { return reject(sequence, 'INVALID_FRAME'); }
  return true;
}
for (;;) {
  const byte = Buffer.allocUnsafe(1);
  const count = fs.readSync(FD, byte, 0, 1, null);
  if (count === 0) break;
  line = Buffer.concat([line, byte]);
  if (line.length > MAX_FRAME) { reject(undefined, 'FRAME_TOO_LARGE'); break; }
  if (byte[0] === 10) {
    const raw = line.subarray(0, -1); line = Buffer.alloc(0);
    if (!raw.length || !handle(raw)) break;
  }
}
if (state) cleanup();
