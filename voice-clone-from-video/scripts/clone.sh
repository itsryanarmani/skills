#!/usr/bin/env bash
# Clone your own voice from a video with WaveSpeed minimax/voice-clone, use it once, save a record.
#
#   clone.sh VIDEO VOICE_ID [--start 0.4] [--secs 20] [--dry-run]
#
# Needs WAVESPEED_API_KEY in the environment (never pass it on the command line).
# Costs $1.60 once. --dry-run does everything except the paid call and prints the price.
# Writes $VOICE_DIR/VOICE_ID/{sample.wav,preview.*,voice.json}; VOICE_DIR defaults to ~/.voice-clones.
set -euo pipefail
exec </dev/null
video="$1"; id="$2"; shift 2
start=0.4; secs=20; dry=0
while (($#)); do case "$1" in
  --start) start="$2"; shift 2;; --secs) secs="$2"; shift 2;; --dry-run) dry=1; shift;;
  *) echo "unknown option $1" >&2; exit 2;; esac; done

# The ID rules come from WaveSpeed: 8+ characters, starts with a letter, letters and digits, unique.
[[ "$id" =~ ^[A-Za-z][A-Za-z0-9]{7,}$ && "$id" =~ [0-9] && "$id" =~ [A-Za-z] ]] \
  || { echo "VOICE_ID needs 8+ characters, start with a letter, and mix letters and digits" >&2; exit 2; }
[[ -n "${WAVESPEED_API_KEY:-}" ]] || { echo "set WAVESPEED_API_KEY first" >&2; exit 2; }
(( $(echo "$secs < 5 || $secs > 20" | bc) )) && echo "note: WaveSpeed recommends 5 to 20 s of speech" >&2

dir="${VOICE_DIR:-$HOME/.voice-clones}/$id"; mkdir -p "$dir"; chmod 700 "$dir"
ffmpeg -loglevel error -y -ss "$start" -t "$secs" -i "$video" -vn -ac 1 -ar 32000 -c:a pcm_s16le "$dir/sample.wav"
echo "sample: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$dir/sample.wav") s, $(ffmpeg -hide_banner -i "$dir/sample.wav" -af volumedetect -f null - 2>&1 | grep mean_volume | sed 's/.*mean_volume: //')"
echo "price: $(wavespeed price minimax/voice-clone 2>&1 | tr -d '\n' | head -c 120)"
((dry)) && { echo "dry run: no upload, no clone, no charge"; exit 0; }

url=$(wavespeed upload "$dir/sample.wav" 2>&1 | grep -o 'https://[^ ]*' | tail -1)
[[ -n "$url" ]] || { echo "upload failed" >&2; exit 1; }
wavespeed run minimax/voice-clone -i audio="$url" -i custom_voice_id="$id" -i model=speech-02-hd \
  -i need_volume_normalization=true -i text="Hi, this is a short test of my cloned voice." \
  --download "$dir/preview.{ext}" --json >"$dir/clone-response.json"
# An ID that no speech call has used is deleted after 7 days. One real call makes it reusable.
wavespeed run minimax/speech-02-hd -i voice_id="$id" -i text="Checking in." --json >/dev/null
python3 -I - "$dir/voice.json" "$id" <<'PY'
import datetime, json, sys
today = datetime.date.today().isoformat()
json.dump({"voice_id": sys.argv[2], "provider": "wavespeed minimax/voice-clone", "created": today,
           "last_used": today, "deleted_if_never_used_after_days": 7, "cost_usd": 1.6,
           "speak_with": ["minimax/speech-02-hd", "minimax/speech-02-turbo", "minimax/speech-2.6-hd"],
           "consent": "own voice, recorded by the owner"}, open(sys.argv[1], "w"), indent=2)
PY
chmod 600 "$dir/voice.json"; echo "cloned $id. Record: $dir/voice.json. Optional insurance: keepalive.sh $id"
