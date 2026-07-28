// 생성된 페이지의 메인 <script> 를 최소 DOM 셰임 위에서 "실제로 실행"하고
// 관측 결과를 JSON 으로 뱉는다. 소스 grep 이 아니라 동작으로 계약을 검증하기
// 위한 도구이므로, 식별자 이름이 바뀌어도 #deep-status 텍스트와 버튼 disabled
// 상태라는 관측 가능한 결과는 그대로 확인된다.
//
// usage: node _generated_page_shim.mjs <page.js> '<json-options>'
//   options: { promptReturn: string|null, seedLocalStorage: {k:v}, action: "run"|null,
//              runQuery: string }
import fs from 'node:fs';
import vm from 'node:vm';

const js = fs.readFileSync(process.argv[2], 'utf8');
let opt = {};
try { opt = JSON.parse(process.argv[3] || '{}'); } catch (e) { opt = {}; }
const promptReturn = Object.prototype.hasOwnProperty.call(opt, 'promptReturn')
  ? opt.promptReturn : null;

function mkEl(id) {
  return {
    id, _text: '', disabled: false, title: '', value: '', innerHTML: '',
    style: new Proxy({}, { get: () => '', set: () => true }),
    classList: {
      _s: new Set(),
      add(...c) { c.forEach((x) => this._s.add(x)); },
      remove(...c) { c.forEach((x) => this._s.delete(x)); },
      contains(c) { return this._s.has(c); },
      toggle() {},
    },
    get textContent() { return this._text; },
    set textContent(v) { this._text = String(v); },
    addEventListener() {}, removeEventListener() {}, appendChild() {}, remove() {},
    querySelector: () => null, querySelectorAll: () => [], setAttribute() {},
    getAttribute: () => null, focus() {}, click() {}, scrollIntoView() {},
    insertAdjacentHTML() {}, closest: () => null, getBoundingClientRect: () => ({}),
  };
}

const els = new Map();
const handlers = [];
const calls = { prompt: [], alert: [] };

const doc = {
  getElementById(id) { if (!els.has(id)) els.set(id, mkEl(id)); return els.get(id); },
  querySelector: () => null,
  querySelectorAll: () => [],
  createElement: (t) => mkEl('created:' + t),
  addEventListener(ev, fn) { handlers.push([ev, fn]); },
  removeEventListener() {},
  body: mkEl('body'), head: mkEl('head'), documentElement: mkEl('html'),
  readyState: 'loading', cookie: '',
};

const store = new Map(Object.entries(opt.seedLocalStorage || {}));
const sandbox = {
  console,
  document: doc,
  navigator: { userAgent: 'node', clipboard: { writeText: async () => {} }, language: 'ko' },
  location: { hostname: 'localhost', href: 'http://localhost/qa/', search: '', protocol: 'http:' },
  localStorage: {
    getItem: (k) => (store.has(k) ? store.get(k) : null),
    setItem: (k, v) => store.set(k, String(v)),
    removeItem: (k) => store.delete(k),
  },
  sessionStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  fetch: async () => { throw new Error('network disabled in shim'); },
  prompt: (m) => { calls.prompt.push(String(m)); return promptReturn; },
  alert: (m) => { calls.alert.push(String(m)); },
  confirm: () => false,
  setTimeout, clearTimeout, setInterval, clearInterval,
  requestAnimationFrame: (f) => setTimeout(f, 0),
  URL, URLSearchParams, TextDecoder, TextEncoder, AbortController,
  Blob: class {}, performance,
  matchMedia: () => ({ matches: false, addEventListener() {} }),
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

let loadError = null;
try {
  vm.runInContext(js, sandbox, { filename: 'page.js' });
} catch (e) {
  loadError = String((e && e.message) || e);
}

const fired = [];
for (const [ev, fn] of handlers) {
  if (ev !== 'DOMContentLoaded') continue;
  try { fn({ type: ev }); fired.push('ok'); } catch (e) { fired.push('ERR:' + e.message); }
}

const status = () => (els.has('deep-status') ? els.get('deep-status') : null);
const out = {
  loadError,
  domHandlers: handlers.filter(([e]) => e === 'DOMContentLoaded').length,
  fired,
  statusText: status() ? status().textContent : null,
  statusActive: status() ? status().classList.contains('active') : null,
  rerunDisabled: els.has('deep-rerun') ? els.get('deep-rerun').disabled : null,
  audioDisabled: els.has('deep-audio') ? els.get('deep-audio').disabled : null,
  rerunTitle: els.has('deep-rerun') ? els.get('deep-rerun').title : null,
  hasRunDeepResearch: typeof sandbox.runDeepResearch,
  hasRunDeeperResearch: typeof sandbox.runDeeperResearch,
};

if (opt.action === 'run') {
  out.statusBeforeRun = out.statusText;
  if (typeof sandbox.runDeepResearch === 'function') {
    try { sandbox.runDeepResearch(opt.runQuery || 'qa probe'); } catch (e) { out.runError = e.message; }
  } else {
    out.runError = 'runDeepResearch is not a function';
  }
  out.statusAfterRun = status() ? status().textContent : null;
  out.promptMessages = calls.prompt.map((m) => m.slice(0, 400));
  out.alerts = calls.alert;
}

// 두 번째 실행 경로(runDeeperResearch)도 같은 게이트를 거치는지 — 이쪽은
// 프롬프트 없이 키 상태 메시지를 그대로 reject 로 던진다.
if (opt.action === 'deeper') {
  if (typeof sandbox.runDeeperResearch === 'function') {
    try {
      await sandbox.runDeeperResearch(0, opt.runQuery || 'qa probe');
      out.deeperRejected = false;
    } catch (e) {
      out.deeperRejected = true;
      out.deeperError = String((e && e.message) || e);
    }
  } else {
    out.deeperError = 'runDeeperResearch is not a function';
  }
}

process.stdout.write(JSON.stringify(out, null, 1));
