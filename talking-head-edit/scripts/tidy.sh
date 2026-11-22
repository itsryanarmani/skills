#!/usr/bin/env bash
# One command: transcribe, cut dead air, set loudness, verify. No model tokens.
#
#   tidy.sh IN.mov [OUT.mp4] [edit.py options...]
#
# Writes OUT.mp4 (default IN-edited.mp4), OUT.report.json, OUT.transcript.txt.
# Prints the verdict. Never touches IN. Env: WHISPER_MODEL (small.en), PROMPT
# (names and terms to help whisper spell them).
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
in="$1"; shift
out="${1:-}"; if [[ -n "$out" && "$out" != --* ]]; then shift; else out="${in%.*}-edited.mp4"; fi
[[ "$in" == "$out" ]] && { echo "refusing to overwrite the source" >&2; exit 2; }
work="$(mktemp -d)"; t0=$(date +%s)
stage() { echo "  $1: $(( $(date +%s) - t0 ))s" >&2; t0=$(date +%s); }
asr() {  # audio.wav -> word json in $work/$2
  whisper "$1" --model "${WHISPER_MODEL:-small.en}" --language en --word_timestamps True \
    --initial_prompt "${PROMPT:-}" --output_format json --output_dir "$work/$2" --verbose False >/dev/null 2>&1
}

ffmpeg -loglevel error -y -i "$in" -vn -ac 1 -ar 16000 "$work/a.wav"; stage extract
asr "$work/a.wav" src; stage transcribe
python3 -I "$here/edit.py" "$in" "$out" --words "$work/src/a.json" \
  --report "${out%.*}.report.json" "$@" >/dev/null; stage edit
ffmpeg -loglevel error -y -i "$out" -vn -ac 1 -ar 16000 "$work/o.wav"
asr "$work/o.wav" out; stage re-transcribe
python3 -I - "$work/src/a.json" > "${out%.*}.transcript.txt" <<'PY'
import json, sys
for s in json.load(open(sys.argv[1]))["segments"]: print(f"[{s['start']:6.1f}] {s['text'].strip()}")
PY
python3 -I "$here/verify.py" "$out" "${out%.*}.report.json" "$work/out/o.json" || true; stage verify
echo "transcript: ${out%.*}.transcript.txt" >&2
