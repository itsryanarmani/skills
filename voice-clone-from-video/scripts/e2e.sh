#!/usr/bin/env bash
# End-to-end check for the voice-clone scripts. Costs a few cents, never the $1.60 clone call.
#
#   set -a; . /path/to/wavespeed.env; set +a; bash e2e.sh [verdict.json]
#
# It proves four things with the real service and the real balance:
#   1. clone.sh --dry-run extracts a sample and prints the price, and the balance does not move.
#   2. A speech call with a system voice works and check.py passes on its own output.
#   3. CONTROL: check.py fails on a different voice for the PITCH reason, and on wrong text for the WORDS reason.
#   4. The whole run cost under $0.05.
# Needs say (macOS) or espeak, ffmpeg, whisper-cli with a ggml model, numpy, wavespeed.
set -euo pipefail
exec </dev/null
here="$(cd "$(dirname "$0")" && pwd)"
[[ -n "${WAVESPEED_API_KEY:-}" ]] || { echo "set WAVESPEED_API_KEY first" >&2; exit 2; }
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT
verdict="${1:-$PWD/voice-verdict.json}"; [[ "$verdict" = /* ]] || verdict="$PWD/$verdict"
bal() { wavespeed balance 2>&1 | grep -o 'Balance: \$[0-9.]*' | grep -o '[0-9.]*$'; }
cd "$work"

text="Hello, this is a short test of the voice check."
if command -v say >/dev/null; then say -o s.aiff "$text"; else espeak -w s.wav "$text" && ffmpeg -loglevel error -y -i s.wav s.aiff; fi
ffmpeg -loglevel error -y -i s.aiff -ar 48000 -ac 2 s.wav
ffmpeg -loglevel error -y -f lavfi -i "color=c=0x335577:s=640x360:r=30:d=8" -i s.wav -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest in.mp4

before=$(bal)
VOICE_DIR="$work/v" bash "$here/clone.sh" in.mp4 TestVoice0001 --start 0 --secs 5 --dry-run > dry.txt 2>&1 || true
after_dry=$(bal)

wavespeed run minimax/speech-02-hd -i voice_id=Casual_Guy -i text="$text" --download "$work/gen.{ext}" --json >/dev/null 2>&1 || true
gen="$(ls "$work"/gen.* 2>/dev/null | head -1)"
python3 -I "$here/check.py" "$gen" "$gen" "$text" > ok.json 2>&1 && ok=true || ok=false           # a clip against itself
python3 -I "$here/check.py" s.wav "$gen" "$text" > diffvoice.json 2>&1 && diffv=true || diffv=false  # other voice
python3 -I "$here/check.py" "$gen" "$gen" "completely different words here" > wrongtext.json 2>&1 && wrongt=true || wrongt=false
end=$(bal)

python3 -I - "$before" "$after_dry" "$end" "$ok" "$diffv" "$wrongt" "$verdict" <<'PY'
import json, sys
before, after_dry, end = map(float, sys.argv[1:4]); ok, diffv, wrongt = (a == "true" for a in sys.argv[4:7])
dry = open("dry.txt").read()
def why(path, must_fail, must_pass):   # the intended check fails and the other holds; a crash is no pass
    try: r = json.load(open(path))
    except Exception: return False
    return r.get(must_fail) is False and r.get(must_pass) is True
checks = {
  "dry_run_prints_sample_and_price": "sample:" in dry and "price:" in dry and "1.6" in dry and "dry run" in dry,
  "dry_run_costs_nothing": abs(before - after_dry) < 1e-9,
  "speech_call_made_audio_file": __import__("glob").glob("gen.*") != [] and __import__("os").path.getsize(__import__("glob").glob("gen.*")[0]) > 5000,
  "check_passes_on_matching_clip": ok,
  "CONTROL: a different voice fails on PITCH, words still match": why("diffvoice.json", "pitch_ok", "words_ok"),
  "CONTROL: wrong text fails on WORDS, pitch still matches": why("wrongtext.json", "words_ok", "pitch_ok"),
  "whole_run_under_5_cents": before - end < 0.05,
}
v = {"balance_before": before, "balance_end": end, "spent": round(before - end, 4), "checks": checks, "pass": all(checks.values())}
json.dump(v, open(sys.argv[7], "w"), indent=2); print(json.dumps(v, indent=2))
sys.exit(0 if v["pass"] else 1)
PY
