#!/usr/bin/env bash
# End-to-end check for tidy.sh. Builds a synthetic talking video whose audio
# starts 0.3 s after the video (like real camera files), runs the real flow,
# then measures the output. A control run with the offset fix switched off
# must FAIL, or the test cannot see the bug it guards. Writes a JSON verdict.
# Needs macOS `say` (or espeak), ffmpeg, whisper, python3 + numpy.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT; verdict="${1:-$work/verdict.json}"
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
# variable frame rate: one frame in four dropped (timestamps kept), the video starts 0.2 s after the
# audio, and its tail runs 0.5 s past the audio. The picture is a sawtooth in time (255 levels a
# second), so any frame can be checked against the time it should show.
ffmpeg -loglevel error -y -f lavfi -i "nullsrc=s=640x360:r=30:d=$(echo "$dur + 0.8" | bc),format=gray,geq=lum='255*mod(T\,1)'" \
  -vf "select='not(eq(mod(n,4),1))'" -fps_mode passthrough -c:v libx264 -pix_fmt yuv420p -an v.mp4
ffmpeg -loglevel error -y -itsoffset 0.5 -i v.mp4 -itsoffset 0.3 -i quiet.wav -map 0:v -map 1:a -c:v copy -c:a aac vfr.mp4
# audio much longer than the video: the plan must end where the video ends
ffmpeg -loglevel error -y -f lavfi -i "color=c=0x335577:s=640x360:r=30:d=$(echo "$dur * 0.66" | bc)" -i quiet.wav \
  -c:v libx264 -pix_fmt yuv420p -c:a aac short.mp4
python3 -I "$here/edit.py" short.mp4 short-out.mp4 --report short.json >/dev/null 2>&1 || true
vstart=$(ffprobe -v error -select_streams v:0 -show_entries stream=start_time -of csv=p=0 vfr.mp4)
fstart=$(ffprobe -v error -show_entries format=start_time -of csv=p=0 vfr.mp4)

words() {  # text of a video's speech as one word per line
  ffmpeg -loglevel error -y -i "$1" -vn -ac 1 -ar 16000 w.wav
  whisper w.wav --model base.en --language en --output_format txt --output_dir wt --verbose False >/dev/null 2>&1
  tr 'A-Z' 'a-z' < wt/w.txt | tr -c "a-z0-9'\n" ' ' | tr -s ' \n' '\n' | sed '/^$/d'
}
words in.mp4 > before.txt
bash "$here/tidy.sh" in.mp4 good.mp4 > good.json 2>/dev/null || true
bash "$here/tidy.sh" in.mp4 bad.mp4 --no-offset-fix > bad.json 2>/dev/null || true
bash "$here/tidy.sh" vfr.mp4 vfrgood.mp4 > vfr.json 2>/dev/null || true
words good.mp4 > good.txt; words bad.mp4 > bad.txt

python3 -I - "$off" "$verdict" "$vstart" "$fstart" <<'PY'
import json, subprocess, sys
off, out = float(sys.argv[1]), sys.argv[2]
v0 = float(sys.argv[3]) - float(sys.argv[4])      # video start on the clock ffmpeg cuts on
g, b = json.load(open("good.json")), json.load(open("bad.json"))
try: vf = json.load(open("vfr.json"))
except Exception: vf = {"pass": False}
rd = lambda p: open(p).read().split()
same = lambda p: rd("before.txt") == rd(p)
def avgap(p):
    def d(s):
        try: return float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", s, "-show_entries", "stream=duration",
                                          "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
        except ValueError: return None
    v, a = d("v:0"), d("a:0")
    return 99 if v is None or a is None else abs(v - a)   # a missing output is a failure, not a match
def aligned(shift=0.0):   # worst error, in picture levels, of the frames the output shows (1 frame = 8.5)
    r = json.load(open("vfrgood.report.json")); acc, errs = 0.0, []
    for s, e in r["keep"]:
        for f in (0.25, 0.5, 0.75):
            tf = s + r["audio_start_s"] + f * (e - s)
            if tf >= v0 + 0.1:                       # earlier than that is padding before the video begins
                px = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{acc + f * (e - s):.3f}", "-i", "vfrgood.mp4",
                                     "-frames:v", "1", "-vf", "crop=2:2:300:170,format=gray", "-f", "rawvideo", "-"],
                                    capture_output=True).stdout
                want = 255 * ((tf - v0 + shift) % 1.0)
                errs.append(999 if not px else min(abs(want - px[0]), 255 - abs(want - px[0])))
        acc += e - s
    return max(errs) if errs else 999
checks = {
  "input_audio_starts_late (test is meaningful)": off >= 0.25,
  "verdict_passes": g["pass"],
  "variable_frame_rate_clip_passes (audio and video lengths match)": vf["pass"],
  "frames_match_their_time (late video start, dropped frames): worst error <= 12 levels": aligned() <= 12,
  "CONTROL: an expectation shifted by 0.27 s is rejected": aligned(0.27) > 12,
  "audio longer than the video: output lengths still match": avgap("short-out.mp4") <= 0.07,
  "shorter_by_2s_or_more": g["original_s"] - g["edited_s"] >= 2.0,
  "loudness_within_1lu": abs(g["loudness_lufs"] - (-16)) <= 1.0,
  "joins_in_silence": g["worst_join_above_floor_db"] <= 14,
  "no_word_lost_or_added": same("good.txt"),
  "CONTROL: fix switched off is caught (verdict fails or words differ)":
      (not b["pass"]) or (not same("bad.txt")),
}
v = {"audio_start_s": off, "good": g, "control_pass_flag": b["pass"], "checks": checks, "pass": all(checks.values())}
json.dump(v, open(out, "w"), indent=2)
print(json.dumps({"checks": checks, "pass": v["pass"]}, indent=2))
sys.exit(0 if v["pass"] else 1)
PY
