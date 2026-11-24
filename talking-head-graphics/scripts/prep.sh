#!/usr/bin/env bash
# prep.sh IN.mp4 PROJECT_DIR
# IN.mp4 is a finished talking-head cut (1080p, from talking-head-edit). Makes a HyperFrames project with a seekable base
# video, word times and sound effects. The speaker cutouts come later (cutouts.sh), after build.py has chosen the windows.
set -euo pipefail
[ $# -eq 2 ] || { echo "usage: prep.sh IN.mp4 PROJECT_DIR" >&2; exit 2; }
IN="$1"; P="$2"
[ -f "$IN" ] || { echo "prep: no such file: $IN" >&2; exit 2; }
for c in ffmpeg whisper-cli earshot npx; do command -v "$c" >/dev/null || { echo "prep: $c not found" >&2; exit 2; }; done
mkdir -p "$(dirname "$P")"; P="$(cd "$(dirname "$P")" && pwd)/$(basename "$P")"
if [ ! -f "$P/index.html" ]; then
  # init must make the folder itself: it refuses a folder that already has files
  if [ -e "$P" ] && [ -n "$(ls -A "$P")" ]; then echo "prep: $P exists and is not a HyperFrames project" >&2; exit 2; fi
  (cd "$(dirname "$P")" && npx -y hyperframes@0.9.91 init "$(basename "$P")" --example blank --non-interactive --skip-transcribe >/dev/null)
fi
mkdir -p "$P/assets/sfx" "$P/assets/logos" "$P/assets/gen"
# keyframe every second so a seek never freezes
ffmpeg -v error -y -i "$IN" -c:v libx264 -preset fast -crf 17 -g 30 -c:a copy "$P/assets/base.mp4"
# word times (whisper.cpp, same flags as talking-head-edit)
ffmpeg -v error -y -i "$IN" -ac 1 -ar 16000 "$P/words.wav"
whisper-cli -m "${WHISPER_CPP_MODEL:-$HOME/.cache/hyperframes/whisper/models/ggml-small.en.bin}" -f "$P/words.wav" -l en -ml 1 -sow -ojf -of "$P/words" -np -nfa -mc 0 >/dev/null 2>&1
# sound effects from earshot (no model, no network)
cat > "$P/sfx.json" <<'J'
{"set":"ui","format":"wav","sounds":[
{"name":"whoosh","want":"a hand swept quickly through the air"},{"name":"whoosh_big","want":"a heavy deep whoosh of something large passing"},
{"name":"pop","want":"a soft rounded tactile tap with a faint note"},{"name":"coin","want":"a small metallic tick, a coin clink"},
{"name":"rise","want":"three quick rising notes, a short soft confirmation"},{"name":"tick","want":"a small dry wooden tick"},
{"name":"win","want":"a quick rising major arpeggio landing on the octave, a small happy flourish"}]}
J
earshot make --spec "$P/sfx.json" -o "$P/assets/sfx" >/dev/null
echo "prep done: $P"
