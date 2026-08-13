#!/bin/bash
# Generic local launcher. Optional first argument is a configured topic alias.
set -eu
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
[ -f pipeline/serve_local.py ] || {
  echo "paper-curation checkout not found: $ROOT" >&2
  exit 1
}

TOPIC="${1:-}"
PORT="${PAPER_CURATION_PORT:-8000}"
URL="http://localhost:${PORT}/${TOPIC:+${TOPIC}/}"
alive() { curl -fsS -m 5 -o /dev/null "http://localhost:${PORT}/"; }

if ! alive; then
  if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
    echo "port $PORT is owned by another process; refusing to terminate it" >&2
    exit 1
  fi
  SERVER_ARGS=(pipeline/serve_local.py --port "$PORT")
  if [ -n "$TOPIC" ]; then SERVER_ARGS+=(--topic "$TOPIC"); fi
  python3 "${SERVER_ARGS[@]}" &
  SERVER_PID=$!
  for _ in $(seq 1 20); do
    alive && break
    sleep 0.5
  done
  alive || {
    echo "paper-curation server did not become ready on port $PORT" >&2
    kill "$SERVER_PID" 2>/dev/null || true
    exit 1
  }
fi

open "$URL"
if [ -n "${SERVER_PID:-}" ]; then wait "$SERVER_PID"; fi
