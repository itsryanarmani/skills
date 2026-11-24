#!/usr/bin/env bash
# render.sh PROJECT_DIR OUT.mp4 [--pace 1.05] [--end SECONDS] [--lufs -14]
# Renders, grades, balances the voice, trims, measures. Exit 0 only if the file passes. Low disk uses one worker.
#   --pace  speed-up for energy (0.9 to 1.15, default 1.0): video and audio, pitch kept
#   --end   cut the film here, in base-video seconds, with a 0.25 s audio fade (use it when the speaker looks away at the end)
#   --lufs  loudness target (default -14: louder than the old -16, which the speaker found quiet)
set -euo pipefail
[ $# -ge 2 ] || { echo "usage: render.sh PROJECT_DIR OUT.mp4 [--pace F] [--end S] [--lufs L]" >&2; exit 2; }
P="$1"; OUT="$2"; shift 2; PACE=1.0; END=""; LUFS=-14
while [ $# -gt 0 ]; do
  case "$1" in
    --pace) [ $# -ge 2 ] || { echo "render: --pace needs a value" >&2; exit 2; }; PACE="$2"; shift 2 ;;
    --end) [ $# -ge 2 ] || { echo "render: --end needs a value" >&2; exit 2; }; END="$2"; shift 2 ;;
    --lufs) [ $# -ge 2 ] || { echo "render: --lufs needs a value" >&2; exit 2; }; LUFS="$2"; shift 2 ;;
    *) echo "render: unknown option $1" >&2; exit 2 ;;
  esac
done
python3 - "$PACE" "${END:-0}" "$LUFS" <<'PY' || { echo "render: --pace must be 0.9 to 1.15, --end a positive number, --lufs -23 to -9" >&2; exit 2; }
import sys
p, e, l = map(float, sys.argv[1:4])
sys.exit(0 if 0.9 <= p <= 1.15 and e >= 0 and -23 <= l <= -9 else 1)
PY
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
base="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$P/assets/base.mp4")"
if [ -n "$END" ]; then python3 -c 'import re, sys; e, b = float(sys.argv[1]), float(sys.argv[2]); sys.exit(0 if re.fullmatch(r"[0-9]+(\.[0-9]+)?", sys.argv[1]) and 1 <= e <= b + 0.01 else 1)' "$END" "$base" || { echo "render: --end must be a plain number from 1 up to the base video length ($base s)" >&2; exit 2; }; fi
# the renderer works beside its output ($T), so measure that disk and the disk of the final file
free_of() { df -Pk "$1" | awk 'NR==2 {print int($4 / 1048576)}'; }
free_t="$(free_of "$T")"; free_o="$(free_of "$(dirname "$OUT")")"
for v in "$free_t" "$free_o"; do case "$v" in ''|*[!0-9]*) echo "render: cannot read free disk space" >&2; exit 1 ;; esac; done
workers=auto; { [ "$free_t" -lt 5 ] || [ "$free_o" -lt 1 ]; } && workers=1   # the default mode stores every frame on disk
(cd "$P" && npx -y hyperframes@0.9.91 render -o "$T/raw.mp4" -q looks --workers "$workers" >"$T/render.log" 2>&1) || { tail -5 "$T/render.log" >&2; exit 1; }
# Grade: keep the black point at 0 (logo tiles stay black), lift the mid-shadows where the eyes sit, add warmth to skin.
# The first grade (contrast up, saturation down, vignette) turned the under-eyes dark and the speaker looked tired.
GRADE="curves=all='0/0 0.12/0.17 0.25/0.33 0.5/0.57 1/1',eq=saturation=1.08:gamma=1.05:brightness=0.015,colorbalance=rs=0.02:rm=0.025:rh=0.025:bm=-0.02:bh=-0.025"
inargs=(); afade=""
if [ -n "$END" ]; then inargs=(-t "$END"); afade="afade=t=out:st=$(python3 -c 'import sys; print(max(0, float(sys.argv[1]) - 0.25))' "$END"):d=0.25,"; fi
# Voice: a little presence (3.2 kHz) and light compression for energy, then loudness.
AF="${afade}atempo=$PACE,acompressor=threshold=-18dB:ratio=2.5:attack=5:release=80:makeup=2,equalizer=f=3200:t=q:w=1.2:g=1.5,loudnorm=I=$LUFS:TP=-1.5:LRA=9"
ffmpeg -v error -y ${inargs[@]+"${inargs[@]}"} -i "$T/raw.mp4" -vf "setpts=PTS/$PACE,fps=30,$GRADE" -af "$AF" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$OUT"
# measure in its own step so a failed measurement cannot read as a pass
meas="$(ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1)" || { echo "render: loudness measurement failed" >&2; exit 1; }
lufs="$(printf '%s\n' "$meas" | awk '/ I:/ {i=$2} END {print i}')"; peak="$(printf '%s\n' "$meas" | awk '/Peak:/ {p=$2} END {print p}')"
dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"
sdur() { ffprobe -v error -select_streams "$1" -show_entries stream=duration -of csv=p=0 "$OUT" | head -1; }   # video and audio lengths on their own: the container length hides a short picture
vdur="$(sdur v:0)"; adur="$(sdur a:0)"
python3 - "$lufs" "$peak" "$dur" "$base" "$PACE" "${END:-0}" "$LUFS" "$vdur" "$adur" <<'PY'
import json, sys
try:
    l, p, d, b, pace, end, target, vd, ad = map(float, sys.argv[1:10])
except ValueError:
    sys.exit("render: a measurement is missing")
want = (end if end > 0 else b) / pace
v = {"lufs": l, "target_lufs": target, "peak_db": p, "duration": d, "expected_duration": round(want, 2), "video_duration": vd, "audio_duration": ad, "pass": abs(l - target) <= 1 and p <= -1.0 and abs(d - want) <= 0.2 and abs(vd - want) <= 0.2 and abs(ad - want) <= 0.2}
print(json.dumps(v)); sys.exit(0 if v["pass"] else 1)
PY
