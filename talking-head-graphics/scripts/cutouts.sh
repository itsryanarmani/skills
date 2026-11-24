#!/usr/bin/env bash
# cutouts.sh IN.mp4 PROJECT_DIR
# Makes one short transparent cutout of the speaker per text-behind window. build.py writes PROJECT_DIR/windows.txt
# ("id start end", seconds in IN.mp4). Cutting only these windows takes about 10 s per second of window on a laptop CPU.
set -euo pipefail
[ $# -eq 2 ] || { echo "usage: cutouts.sh IN.mp4 PROJECT_DIR" >&2; exit 2; }
IN="$1"; P="$2"; W="$P/windows.txt"
[ -f "$IN" ] && [ -f "$W" ] || { echo "cutouts: need $IN and $W (run build.py first)" >&2; exit 2; }
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT   # the trap also covers a failed run
n=0
while read -r id a b || [ -n "$id" ]; do
  [ -n "$id" ] || continue
  d="$(python3 -c 'import sys; print(round(float(sys.argv[2]) - float(sys.argv[1]), 2))' "$a" "$b")"
  # stdin is the window list: a tool that reads it eats the next ids, so both tools get /dev/null
  ffmpeg -nostdin -v error -y -ss "$a" -t "$d" -i "$IN" -c:v libx264 -crf 12 -an "$T/$id.mp4" </dev/null
  npx -y hyperframes@0.9.91 remove-background "$T/$id.mp4" -o "$P/assets/person-$id.webm" --quality best >/dev/null </dev/null
  [ -s "$P/assets/person-$id.webm" ] || { echo "cutouts: no output for $id" >&2; exit 1; }
  n=$((n + 1))
done < "$W"
echo "cutouts done: $n window(s)"
