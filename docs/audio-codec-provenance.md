# Audio codec provenance

The Audio codec wrapper uses the reviewed, vendored `lamejs` runtime bundle only.

- Source registry document: <https://registry.npmjs.org/lamejs/1.2.1>
- Tarball: <https://registry.npmjs.org/lamejs/-/lamejs-1.2.1.tgz>
- Package: `lamejs@1.2.1`
- Declared SPDX license: `LGPL-3.0`
- Registry integrity: `sha512-s7bxvjvYthw6oPLCm5pFxvA84wUROODB8jEO2+CE1adhKgrIvVOlmMgY8zyugxGrvRaDHNJanOiS21/emty6dQ==`
- `vendor/lamejs/lame.all.js` SHA-256: `026bd88846040f357a937cd85821a48492a362eff0812cda734f23fca55fea3b`
- `vendor/lamejs/LICENSE` SHA-256: `cd144ca132e3842b01f5ed2d6f3a32141e24a1cc15e115aa5f19a2294ce0a379`

The tarball was retrieved to a system temporary directory from the registry URL above. Its SHA-512 matched the registry integrity metadata before extraction; its extracted `package.json` identified `lamejs`, version `1.2.1`, and license `LGPL-3.0` before the two files above were copied.

## fd3 codec contract

`bin/audio-encode-lamejs.mjs` is an already-running child process. It first reads the canonical, length-prefixed fd3 bootstrap used by `pipeline.lib.child_context`; the bootstrap provides the 32-byte HMAC key and nonce and is never accepted from argv, environment, or a file. It subsequently receives canonical UTF-8 JSON objects, one per newline, on fd3. Each request has exactly `schema: 1`, `type`, `operation_id`, `nonce`, `sequence`, and lowercase hexadecimal `mac`. The MAC is HMAC-SHA-256 over canonical JSON of the frame without `mac`; sequence starts at one and increases by one.

`start` additionally fixes mono 24-kHz s16le, 128-kbps CBR, a 1..32 chunk count, and an absolute output path named `audio.mp3`. Its parent is the owned 0700 operation directory. `chunk` accepts only the next ordinal and its exact fixed sibling path `pcm-<ordinal>.s16le`; it verifies 0600 ownership, one link, regular no-follow opening, declared byte length, and SHA-256. `finish` has no extra fields. `cancel` has a restricted `reason_code`.

Responses are canonical authenticated JSONL with the same operation ID, nonce, and request sequence: `started`, `chunk_accepted`, `completed`, `cancelled`, or `error`. On any malformed or unauthorized request the wrapper fails closed and removes its partial output. It never accepts source prose, recipients, arbitrary paths, or aggregate PCM. It reads PCM in bounded blocks, admits chunks only in order (therefore never retaining more than the permitted four-slot window), inserts one 6,000-sample (250 ms) silence block between accepted chunks, and rejects timelines over 3,600 seconds or MP3 output over 64 MiB. The wrapper itself allocates only bounded PCM/MP3 blocks and has an 8 MiB codec working-memory contract.
