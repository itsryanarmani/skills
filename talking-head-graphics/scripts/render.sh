#!/usr/bin/env bash
# render.sh PROJECT_DIR OUT.mp4
# Renders, grades, normalises loudness, then measures. Exit 0 only if the file passes. Low disk uses one worker.
set -euo pipefail
[ $# -eq 2 ] || { echo "usage: render.sh PROJECT_DIR OUT.mp4" >&2; exit 2; }
P="$1"; OUT="$2"; T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
# the renderer works beside its output ($T), so measure that disk and the disk of the final file
free_of() { df -Pk "$1" | awk 'NR==2 {print int($4 / 1048576)}'; }
free_t="$(free_of "$T")"; free_o="$(free_of "$(dirname "$OUT")")"
for v in "$free_t" "$free_o"; do case "$v" in ''|*[!0-9]*) echo "render: cannot read free disk space" >&2; exit 1 ;; esac; done
workers=auto; { [ "$free_t" -lt 5 ] || [ "$free_o" -lt 1 ]; } && workers=1   # the default mode stores every frame on disk
(cd "$P" && npx -y hyperframes@0.9.91 render -o "$T/raw.mp4" -q looks --workers "$workers" >"$T/render.log" 2>&1) || { tail -5 "$T/render.log" >&2; exit 1; }
GRADE="eq=contrast=1.06:saturation=0.86:gamma=0.98,colorbalance=rs=0.02:bs=-0.03:rm=0.03:bm=-0.04:rh=0.03:bh=-0.05,noise=alls=4:allf=t,vignette=angle=PI/7"
ffmpeg -v error -y -i "$T/raw.mp4" -vf "$GRADE" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$OUT"
# measure in its own step so a failed measurement cannot read as a pass
meas="$(ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1)" || { echo "render: loudness measurement failed" >&2; exit 1; }
lufs="$(printf '%s\n' "$meas" | awk '/ I:/ {i=$2} END {print i}')"; peak="$(printf '%s\n' "$meas" | awk '/Peak:/ {p=$2} END {print p}')"
dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")"; base="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$P/assets/base.mp4")"
python3 - "$lufs" "$peak" "$dur" "$base" <<'PY'
import json, sys
try:
    l, p, d, b = map(float, sys.argv[1:5])
except ValueError:
    sys.exit("render: a measurement is missing")
v = {"lufs": l, "peak_db": p, "duration": d, "base_duration": b, "pass": abs(l + 16) <= 1 and p <= -1.0 and abs(d - b) <= 0.15}
print(json.dumps(v)); sys.exit(0 if v["pass"] else 1)
PY
