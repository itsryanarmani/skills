#!/usr/bin/env bash
# e2e.sh [verdict.json]  Proves the pipeline scripts with stub tools (no network, no model). Exit 0 only if every check passes.
# Each failure mode found in review has a check, and each check was shown to fail when its fix is removed (see SKILL.md).
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
REAL_FF="$(command -v ffmpeg)"; export REAL_FF
mkdir "$T/bin"; res="$T/res"; : > "$res"; ok() { printf '%s\t%s\n' "$1" "$([ "$2" = 0 ] && echo true || echo false)" >> "$res"; }
cat > "$T/bin/npx" <<'S'
#!/usr/bin/env bash
case "$3" in
  init) [ -e "$4" ] && [ -n "$(ls -A "$4")" ] && { echo "refuses non-empty" >&2; exit 1; }; mkdir -p "$4"; echo "<html></html>" > "$4/index.html" ;;
  remove-background) [ -n "${STUB_FAIL:-}" ] && exit 7; cp "$4" "$6" ;;
  render) if [ -n "${STUB_SHORT:-}" ]; then "$REAL_FF" -v error -y -i assets/base.mp4 -t 40 -c copy "$5" </dev/null; else cp assets/base.mp4 "$5"; fi ;;
esac
S
cat > "$T/bin/ffmpeg" <<'S'
#!/usr/bin/env bash
[ -n "${STUB_EAT_STDIN:-}" ] && head -c 4 >/dev/null
if [ -n "${STUB_MEASURE_FAIL:-}" ] && printf '%s ' "$@" | grep -q ebur128; then printf '  I:         -16.0 LUFS\n  Peak:      -2.0 dBFS\n'; exit 9; fi
exec "$REAL_FF" "$@"
S
printf '#!/usr/bin/env bash\nexit 0\n' > "$T/bin/whisper-cli"
cat > "$T/bin/earshot" <<'S'
#!/usr/bin/env bash
mkdir -p "$5"; for n in whoosh whoosh_big pop coin rise tick win; do echo x > "$5/$n.wav"; done
S
chmod +x "$T/bin/"*; export PATH="$T/bin:$PATH"
mk() { "$REAL_FF" -v error -y -f lavfi -i "testsrc=s=320x180:r=30:d=$2" -f lavfi -i "sine=f=300:d=$2" -shortest -c:v libx264 -g 30 -c:a aac "$1" </dev/null; }
mk "$T/in2.mp4" 2; mk "$T/in60.mp4" 60; mk "$T/in100.mp4" 100

# 1 fresh project: init runs before assets are made; base video and sound effects exist
bash "$here/prep.sh" "$T/in2.mp4" "$T/p" >/dev/null 2>&1; rc=$?
[ $rc = 0 ] && [ -s "$T/p/assets/base.mp4" ] && [ -s "$T/p/assets/sfx/whoosh.wav" ] && [ -f "$T/p/index.html" ]; ok prep_fresh_project $?
# 2 a folder that is not a project is refused (exit 2) and left alone
mkdir "$T/other"; echo keep > "$T/other/f"; bash "$here/prep.sh" "$T/in2.mp4" "$T/other" >/dev/null 2>&1; rc=$?
[ $rc = 2 ] && [ "$(cat "$T/other/f")" = keep ]; ok prep_refuses_foreign_folder $?
# 3 no readable base video: build fails, it does not fall back to an example length
mkdir -p "$T/e"; python3 "$here/build.py" "$T/e" >/dev/null 2>&1; rc=$?
[ $rc != 0 ] && [ ! -f "$T/e/index.html" ]; ok build_requires_base_video $?
# 4 a 2 s base: some clips exist, none runs past 2 s, no window is listed
python3 "$here/build.py" "$T/p" >/dev/null 2>&1; rc=$?
python3 - "$T/p/index.html" 2.0 > "$T/o" <<'PY'
import re, sys
h = open(sys.argv[1]).read(); D = float(sys.argv[2]); c = [(float(a), float(b)) for a, b in re.findall(r'data-start="([\d.]+)" data-duration="([\d.]+)"', h)]
print(sum(1 for a, b in c if a + b > D + 0.011), len(c))
PY
[ $rc = 0 ] && [ "$(cut -d' ' -f1 "$T/o")" = 0 ] && [ "$(cut -d' ' -f2 "$T/o")" -ge 2 ] && [ ! -s "$T/p/windows.txt" ]; ok build_clamps_to_base_length $?
# 5 a 100 s base: the full structure is there (many clips, images from assets/gen, morphs with immediateRender off)
mkdir -p "$T/q/assets"; cp "$T/in100.mp4" "$T/q/assets/base.mp4"
python3 "$here/build.py" "$T/q" >/dev/null 2>&1; rc=$?; h="$T/q/index.html"
n=$(grep -o 'class="clip' "$h" | wc -l | tr -d ' ')
[ $rc = 0 ] && [ "$n" -ge 40 ] && grep -q 'assets/gen/' "$h" && ! grep -q 'assets/gen2/' "$h" && grep -q 'immediateRender:false' "$h"; ok build_full_structure $?
# 6 a text-behind window starts only after the morph back to full frame
python3 - "$T/q/windows.txt" "$here/build.py" > "$T/o" <<'PY'
import re, sys
w = [l.split() for l in open(sys.argv[1])]; src = open(sys.argv[2]).read()
seq = [(float(a), b) for a, b in re.findall(r'\((\d+\.\d+), "(full|R)"\)', src.split("SEQ = ")[1].split("\n")[0])]
bad = sum(1 for i, a, b in w if [t for t, st in seq if st == "full" and t <= float(a) + 0.01] and float(a) < max(t for t, st in seq if st == "full" and t <= float(a) + 0.01) + 0.69)
print(bad, len(w))
PY
[ "$(cut -d' ' -f1 "$T/o")" = 0 ] && [ "$(cut -d' ' -f2 "$T/o")" -ge 2 ]; ok cutout_waits_for_morph $?
# 7 bad windows are refused: in the panel, across a morph, an id with a space
bad=0
for call in 'behind("dp", 30, 31, "")' 'behind("cm", 25, 27, "")' 'behind("two words", 3, 4, "")'; do
  python3 - "$here/build.py" "$T/x.py" "$call" <<'PY'
import sys
s = open(sys.argv[1]).read(); open(sys.argv[2], "w").write(s.replace("states(SEQ)", sys.argv[3] + "\nstates(SEQ)", 1))
PY
  python3 "$T/x.py" "$T/q" >/dev/null 2>&1 && bad=1
done
[ $bad = 0 ]; ok build_refuses_bad_windows $?
# 8 cutouts: the expected file for every window id, each a real video, even when a tool reads stdin
python3 "$here/build.py" "$T/q" >/dev/null 2>&1
STUB_EAT_STDIN=1 bash "$here/cutouts.sh" "$T/in60.mp4" "$T/q" > "$T/o" 2>&1; rc=$?; good=0; want=0
while read -r id a b; do want=$((want + 1)); f="$T/q/assets/person-$id.webm"; [ -s "$f" ] && [ "$("$REAL_FF" -i "$f" 2>&1 | grep -c 'Video:')" -ge 1 ] && good=$((good + 1)); done < "$T/q/windows.txt"
[ $rc = 0 ] && [ "$want" -ge 2 ] && [ "$good" = "$want" ] && grep -q 'cutouts done' "$T/o"; ok cutouts_expected_file_per_window $?
# 9 a failing cutout fails the script and does not say done
rm -f "$T/q/assets"/person-*.webm; STUB_FAIL=1 bash "$here/cutouts.sh" "$T/in60.mp4" "$T/q" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && ! grep -q 'cutouts done' "$T/o"; ok control_failed_cutout_fails_script $?
# 10 a last line with no newline is still processed
mkdir -p "$T/r/assets"; printf 'b9 1.00 2.00' > "$T/r/windows.txt"; bash "$here/cutouts.sh" "$T/in60.mp4" "$T/r" >/dev/null 2>&1; rc=$?
[ $rc = 0 ] && [ -s "$T/r/assets/person-b9.webm" ]; ok last_line_without_newline $?
# 11 render: writes the file and a verdict with the base length
bash "$here/render.sh" "$T/q" "$T/out.mp4" > "$T/o" 2>&1; rc=$?
python3 - "$T/o" > "$T/o2" <<'PY'
import json, sys
l = [x for x in open(sys.argv[1]) if x.startswith("{")]; v = json.loads(l[-1]) if l else {}
print("ok" if v and v.get("pass") is True and abs(v["duration"] - v["base_duration"]) < 0.2 and v["base_duration"] > 99 else "bad")
PY
[ $rc = 0 ] && [ -s "$T/out.mp4" ] && [ "$(cat "$T/o2")" = ok ] && grep -q '"pass": true' "$T/o"; ok render_passes_and_reports $?
# 12 a failed loudness measurement is a failure, never a pass
rm -f "$T/out2.mp4"; STUB_MEASURE_FAIL=1 bash "$here/render.sh" "$T/q" "$T/out2.mp4" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && ! grep -q '"pass": true' "$T/o"; ok control_failed_measurement_fails $?

# 13 a render of the wrong length is rejected: the measurement works, the verdict says fail
rm -f "$T/out3.mp4"; STUB_SHORT=1 bash "$here/render.sh" "$T/q" "$T/out3.mp4" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && grep -q '"pass": false' "$T/o"; ok control_wrong_length_render_fails $?

python3 - "$res" "${1:-}" <<'PY'
import json, sys
c = {a: b == "true" for a, b in (l.rstrip("\n").split("\t") for l in open(sys.argv[1]))}
v = {"checks": c, "pass": all(c.values()) and len(c) == 13}
s = json.dumps(v, indent=2); print(s)
if sys.argv[2]: open(sys.argv[2], "w").write(s + "\n")
sys.exit(0 if v["pass"] else 1)
PY
