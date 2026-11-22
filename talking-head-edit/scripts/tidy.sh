#!/usr/bin/env bash
# One command: transcribe, cut dead air, set loudness, verify. No model tokens.
#
#   tidy.sh IN.mov [OUT.mp4] [edit.py options...]
#
# Writes OUT.mp4 (default IN-edited.mp4), OUT.report.json, OUT.transcript.txt.
# Prints the verdict. Never touches IN. Env: WHISPER_MODEL (small.en), PROMPT
# (names and terms to help whisper spell them), WHISPER_CPP_MODEL (ggml file;
# default ~/.cache/hyperframes/whisper/models). Uses whisper-cli (Metal) when it
# and the model exist, else Python whisper.
set -euo pipefail
exec </dev/null  # ffmpeg and whisper read stdin and would eat a caller's `find | while read` list
here="$(cd "$(dirname "$0")" && pwd)"
in="$1"; shift
out="${1:-}"; if [[ -n "$out" && "$out" != --* ]]; then shift; else out="${in%.*}-edited.mp4"; fi
for f in "$out" "${out%.*}".{report.json,transcript.txt}; do [[ "$in" -ef "$f" ]] && { echo "refusing to overwrite the source" >&2; exit 2; }; done
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT; t0=$(date +%s)
stage() { echo "  $1: $(( $(date +%s) - t0 ))s" >&2; t0=$(date +%s); }
asr() {  # audio.wav -> word json in $work/$2/<name>.json. Metal whisper-cli if it works, else Python whisper.
  local model="${WHISPER_MODEL:-small.en}" preset j
  local cpp="${WHISPER_CPP_MODEL:-$HOME/.cache/hyperframes/whisper/models/ggml-$model.bin}"
  preset="$(basename "$cpp" .bin)"; preset="${preset#ggml-}"; j="$work/$2/$(basename "${1%.wav}").json"
  mkdir -p "$work/$2"
  # -nfa -dtw gives word ends that match Python whisper; -mc 0 stops it dropping a phrase.
  # Any failure of the Metal path, or a missing model, falls through to Python whisper.
  if [[ -f "$cpp" ]] && command -v whisper-cli >/dev/null \
     && whisper-cli -m "$cpp" -f "$1" -l en -ml 1 -sow -nfa -dtw "$preset" -mc 0 ${PROMPT:+--prompt "$PROMPT"} \
          -ojf -of "$work/$2/raw" -np >/dev/null 2>&1 \
     && python3 -I "$here/cpp2words.py" "$work/$2/raw.json" > "$j"; then :
  else
    whisper "$1" --model "$model" --language en --word_timestamps True --initial_prompt "${PROMPT:-}" \
      --output_format json --output_dir "$work/$2" --verbose False >/dev/null 2>&1
  fi
}

ffmpeg -loglevel error -y -i "$in" -map 0:a:0 -ac 1 -ar 16000 "$work/a.wav"; stage extract
asr "$work/a.wav" src; stage transcribe
python3 -I "$here/edit.py" "$in" "$out" --words "$work/src/a.json" \
  --report "${out%.*}.report.json" "$@" >/dev/null; stage edit
ffmpeg -loglevel error -y -i "$out" -vn -ac 1 -ar 16000 "$work/o.wav"
asr "$work/o.wav" out; stage re-transcribe
python3 -I - "$work/src/a.json" > "${out%.*}.transcript.txt" <<'PY'
import json, sys
for s in json.load(open(sys.argv[1]))["segments"]: print(f"[{s['start']:6.1f}] {s['text'].strip()}")
PY
python3 -I "$here/verify.py" "$out" "${out%.*}.report.json" "$work/out/o.json" || rc=$?; stage verify
echo "transcript: ${out%.*}.transcript.txt" >&2
exit "${rc:-0}"
