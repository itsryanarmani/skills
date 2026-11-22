#!/usr/bin/env bash
# End-to-end check for tidy.sh. Builds a synthetic talking video whose audio
# starts 0.3 s after the video (like real camera files), runs the real flow,
# then measures the output. A control run with the offset fix switched off
# must FAIL, or the test cannot see the bug it guards. Writes a JSON verdict.
# Needs macOS `say` (or espeak), ffmpeg, whisper, python3 + numpy.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="$(mktemp -d)"; verdict="${1:-$work/verdict.json}"
[[ "$verdict" = /* ]] || verdict="$PWD/$verdict"
cd "$work"

text='Hello this is a test clip. [[slnc 2500]] The middle part has a long pause before it. [[slnc 2500]] And this is the end of the clip.'
if command -v say >/dev/null; then say -o speech.aiff "$text"; else
  espeak -w s.wav "${text//\[\[slnc 2500\]\]/...}" && ffmpeg -loglevel error -y -i s.wav speech.aiff; fi
ffmpeg -loglevel error -y -i speech.aiff -af volume=-14dB -ar 48000 -ac 2 quiet.wav
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 quiet.wav)
# audio delayed 0.3 s: the container clock and the audio clock now differ
ffmpeg -loglevel error -y -f lavfi -i "color=c=0x335577:s=1280x720:r=30:d=$(echo "$dur + 0.3" | bc)" \
  -itsoffset 0.3 -i quiet.wav -c:v libx264 -pix_fmt yuv420p -c:a aac in.mp4
off=$(ffprobe -v error -select_streams a:0 -show_entries stream=start_time -of csv=p=0 in.mp4)

words() {  # text of a video's speech as one word per line
  ffmpeg -loglevel error -y -i "$1" -vn -ac 1 -ar 16000 w.wav
  whisper w.wav --model base.en --language en --output_format txt --output_dir wt --verbose False >/dev/null 2>&1
  tr 'A-Z' 'a-z' < wt/w.txt | tr -c "a-z0-9'\n" ' ' | tr -s ' \n' '\n' | sed '/^$/d'
}
words in.mp4 > before.txt
bash "$here/tidy.sh" in.mp4 good.mp4 > good.json 2>/dev/null || true
bash "$here/tidy.sh" in.mp4 bad.mp4 --no-offset-fix > bad.json 2>/dev/null || true
words good.mp4 > good.txt; words bad.mp4 > bad.txt

python3 -I - "$off" "$verdict" <<'PY'
import json, sys
off, out = float(sys.argv[1]), sys.argv[2]
g, b = json.load(open("good.json")), json.load(open("bad.json"))
rd = lambda p: open(p).read().split()
same = lambda p: rd("before.txt") == rd(p)
checks = {
  "input_audio_starts_late (test is meaningful)": off >= 0.25,
  "verdict_passes": g["pass"],
  "shorter_by_2s_or_more": g["original_s"] - g["edited_s"] >= 2.0,
  "loudness_within_1lu": abs(g["loudness_lufs"] - (-16)) <= 1.0,
  "joins_in_silence": g["worst_join_above_floor_db"] <= 10,
  "no_word_lost_or_added": same("good.txt"),
  "CONTROL: fix switched off is caught (verdict fails or words differ)":
      (not b["pass"]) or (not same("bad.txt")),
}
v = {"audio_start_s": off, "good": g, "control_pass_flag": b["pass"], "checks": checks, "pass": all(checks.values())}
json.dump(v, open(out, "w"), indent=2)
print(json.dumps({"checks": checks, "pass": v["pass"]}, indent=2))
sys.exit(0 if v["pass"] else 1)
PY
