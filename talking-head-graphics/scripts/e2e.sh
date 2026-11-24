#!/usr/bin/env bash
# e2e.sh [verdict.json]  Proves the pipeline scripts with stub tools (no network, no model). Exit 0 only if every check passes.
# Each failure mode found in review has a check, and mutate.py shows each check fails when its fix is removed.
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
REAL_FF="$(command -v ffmpeg)"; export REAL_FF
mkdir "$T/bin"; res="$T/res"; : > "$res"; ok() { printf '%s\t%s\n' "$1" "$([ "$2" = 0 ] && echo true || echo false)" >> "$res"; }
cat > "$T/bin/npx" <<'S'
#!/usr/bin/env bash
case "$3" in
  init) [ -e "$4" ] && [ -n "$(ls -A "$4")" ] && { echo "refuses non-empty" >&2; exit 1; }; mkdir -p "$4"; echo "<html></html>" > "$4/index.html" ;;
  remove-background) [ -n "${STUB_FAIL:-}" ] && exit 7; cp "$4" "$6" ;;
  render) if [ -n "${STUB_SHORT_VIDEO:-}" ]; then "$REAL_FF" -v error -y -i assets/base.mp4 -map 0:v -t 40 -c copy "$5.v.mp4" </dev/null; "$REAL_FF" -v error -y -i "$5.v.mp4" -i assets/base.mp4 -map 0:v -map 1:a -c copy "$5" </dev/null; elif [ -n "${STUB_SHORT:-}" ]; then "$REAL_FF" -v error -y -i assets/base.mp4 -t 40 -c copy "$5" </dev/null; else cp assets/base.mp4 "$5"; fi ;;
esac
S
cat > "$T/bin/ffmpeg" <<'S'
#!/usr/bin/env bash
[ -n "${STUB_EAT_STDIN:-}" ] && head -c 4 >/dev/null
if [ -n "${STUB_MEASURE_FAIL:-}" ] && printf '%s ' "$@" | grep -q ebur128; then printf '  I:         -14.0 LUFS\n  Peak:      -2.0 dBFS\n'; exit 9; fi
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

bash "$here/prep.sh" "$T/in2.mp4" "$T/p" >/dev/null 2>&1; rc=$?
[ $rc = 0 ] && [ -s "$T/p/assets/base.mp4" ] && [ -s "$T/p/assets/sfx/whoosh.wav" ] && [ -f "$T/p/index.html" ]; ok prep_fresh_project $?
mkdir "$T/other"; echo keep > "$T/other/f"; bash "$here/prep.sh" "$T/in2.mp4" "$T/other" >/dev/null 2>&1; rc=$?
[ $rc = 2 ] && [ "$(cat "$T/other/f")" = keep ]; ok prep_refuses_foreign_folder $?
mkdir -p "$T/e"; python3 "$here/build.py" "$T/e" >/dev/null 2>&1; rc=$?
[ $rc != 0 ] && [ ! -f "$T/e/index.html" ]; ok build_requires_base_video $?
python3 "$here/build.py" "$T/p" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && grep -q 'long' "$T/o" && [ ! -f "$T/p/windows.txt" ]; ok build_refuses_timeline_longer_than_video $?
mkdir -p "$T/q/assets"; cp "$T/in100.mp4" "$T/q/assets/base.mp4"
python3 "$here/build.py" "$T/q" >/dev/null 2>&1; rc=$?; h="$T/q/index.html"
n=$(grep -o 'class="clip' "$h" | wc -l | tr -d ' ')
python3 -c "import json,sys; d=json.load(open(sys.argv[1])); assert len(d['scenes'])>=6 and len(d['windows'])>=2 and d['duration']>99" "$T/q/timeline.json" 2>/dev/null; jj=$?
[ $rc = 0 ] && [ "$n" -ge 30 ] && grep -q 'assets/gen/' "$h" && ! grep -q 'assets/gen2/' "$h" && [ $jj = 0 ]; ok build_full_structure $?
python3 - "$h" "$T/q/timeline.json" > "$T/o" <<'PY'
import json, re, sys
h = open(sys.argv[1]).read(); seq = json.load(open(sys.argv[2]))["seq"]
n = sum(1 for i, (t, st) in enumerate(seq) if st != (seq[i - 1][1] if i else "full"))
print("ok" if n >= 6 and len(re.findall("immediateRender:false", h)) == 2 * n else "bad")
PY
[ "$(cat "$T/o")" = ok ]; ok morphs_do_not_pre_render $?
tl() {
  python3 - "$here/build.py" "$T/t.py" "$1" <<'PY'
import sys
s = open(sys.argv[1]).read(); a = s.index("# ================= TIMELINE"); b = s.index("_emit_scenes()\nstates(SEQ)")
open(sys.argv[2], "w").write(s[:a] + sys.argv[3] + "\n" + s[b:])
PY
  python3 "$T/t.py" "$T/q" >/dev/null 2>&1; echo $?
}
V='scene("a","blue",10,[("x",11.2,13,"")],exit_=13.05)
SEQ = compute_seq()
behind("w",14.2,14.4,15.5,"")'
[ "$(tl "$V")" = 0 ]; ok valid_timeline_builds $?
r() { [ "$(tl "$1")" != 0 ]; }
r 'scene("a","blue",10,[("x",10.5,13,"")],exit_=13.05)
SEQ = compute_seq()'; ok pace_visual_waits_for_sheet $?
r 'scene("a","blue",10,[("x",11.2,14,"")])
scene("b","light",13,[("y",14.5,16,"")])
SEQ = compute_seq()'; ok pace_sheet_waits_for_last_visual $?
r 'scene("a","blue",10,[("x",11.2,13,"")],exit_=13.05)
scene("b","light",13.5,[("y",14.7,16,"")])
SEQ = compute_seq()'; ok pace_wait_after_return_to_full $?
r 'scene("a","blue",10,[("x",11.2,11.8,"")])
SEQ = compute_seq()'; ok pace_visual_has_room_to_fade $?
r 'scene("a","blue",10,[("x",11.2,13,"")])
scene("a","light",14,[("y",15.2,17,"")])
SEQ = compute_seq()'; ok build_refuses_duplicate_ids $?
r 'scene("a","blue",10,[("x",11.2,13,"<b id=\"d\"></b>")])
scene("b","light",14,[("y",15.2,17,"<b id=\"d\"></b>")])
SEQ = compute_seq()'; ok build_refuses_duplicate_element_ids $?
r "scene('a','blue',10,[('x',11.2,13,'<b id=\\'d\\'></b><b id=\\'d\\'></b>')])
SEQ = compute_seq()"; ok build_refuses_single_quoted_duplicate_ids $?
r 'scene("a","blue",10,[("x",11.2,13,"<b id=d></b>")])
scene("b","light",14,[("y",15.2,17,"<b id=d></b>")])
SEQ = compute_seq()'; ok build_refuses_unquoted_duplicate_ids $?
r 'scene("a","blue",10,[("x",11.2,13,"<b id=\"bw\"></b>")])
SEQ = compute_seq()'; ok build_refuses_reserved_ids $?
# controls for the three id tests: the same syntax with a unique id builds, so the refusals above are not syntax errors
[ "$(tl "scene('a','blue',10,[('x',11.2,13,'<b id=\\'d\\'></b>')])
SEQ = compute_seq()")" = 0 ] && [ "$(tl 'scene("a","blue",10,[("x",11.2,13,"<b id=d></b>")])
SEQ = compute_seq()')" = 0 ] && [ "$(tl 'scene("a","blue",10,[("x",11.2,13,"<b id=\"zz\"></b>")])
SEQ = compute_seq()')" = 0 ]; ok control_valid_id_syntaxes_build $?
r 'scene("a","blue",10,[("x",99.2,101,"")])
SEQ = compute_seq()'; ok build_refuses_visual_past_the_video $?
r 'scene("a","blue",10,[("x",11.2,14,"")],exit_=13.5)
SEQ = compute_seq()'; ok pace_visual_gone_before_sheet_leaves $?
r 'scene("a","blue",10,[("x",11.2,12.5,""),("y",12.55,14,"")])
SEQ = compute_seq()'; ok pace_visuals_do_not_overlap $?
r 'scene("a","blue",10,[("x",11.2,13,"")],exit_=13.05)
SEQ = compute_seq()
behind("w",13.8,13.9,15.5,"")'; ok pace_word_waits_after_morph $?
# the cutout never starts inside the morph: asked for 13.1 s, it starts after the morph back (13.05 + 0.65 + margin)
rm -f "$T/q/windows.txt"; st=$(tl 'scene("a","blue",10,[("x",11.2,13,"")],exit_=13.05)
SEQ = compute_seq()
behind("w",13.1,14.2,15.5,"")')
python3 -c "import sys; w=open(sys.argv[1]).read().split(); sys.exit(0 if float(w[1]) >= 13.74 else 1)" "$T/q/windows.txt" 2>/dev/null; jj=$?
[ "$st" = 0 ] && [ $jj = 0 ]; ok pace_cutout_starts_after_morph $?
bad=0
A='scene("a","blue",10,[("x",11.2,13,"")],exit_=13.05)'
for code in "$A
scene(\"b\",\"light\",20,[(\"y\",21.2,23,\"\")])
SEQ = compute_seq()
behind(\"w\",21.5,21.7,22.5,\"\")" "$A
scene(\"b\",\"light\",20,[(\"y\",21.2,23,\"\")])
SEQ = compute_seq()
behind(\"w\",14.2,14.4,19.8,\"\")" "$A
scene(\"b\",\"light\",13.75,[(\"y\",14.9,16.5,\"\")])
SEQ = compute_seq()
behind(\"w\",13.5,14.9,15.5,\"\")" "$A
SEQ = compute_seq()
behind(\"two words\",14.2,14.4,15.5,\"\")"; do
  [ "$(tl "$code")" != 0 ] || bad=1
done
[ $bad = 0 ]; ok build_refuses_bad_windows $?
python3 "$here/build.py" "$T/q" >/dev/null 2>&1
STUB_EAT_STDIN=1 bash "$here/cutouts.sh" "$T/in60.mp4" "$T/q" > "$T/o" 2>&1; rc=$?; good=0; want=0
while read -r id a b; do want=$((want + 1)); f="$T/q/assets/person-$id.webm"; [ -s "$f" ] && [ "$("$REAL_FF" -i "$f" 2>&1 | grep -c 'Video:')" -ge 1 ] && good=$((good + 1)); done < "$T/q/windows.txt"
[ $rc = 0 ] && [ "$want" -ge 2 ] && [ "$good" = "$want" ] && grep -q 'cutouts done' "$T/o"; ok cutouts_expected_file_per_window $?
rm -f "$T/q/assets"/person-*.webm; STUB_FAIL=1 bash "$here/cutouts.sh" "$T/in60.mp4" "$T/q" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && ! grep -q 'cutouts done' "$T/o"; ok control_failed_cutout_fails_script $?
mkdir -p "$T/r/assets"; printf 'b9 1.00 2.00' > "$T/r/windows.txt"; bash "$here/cutouts.sh" "$T/in60.mp4" "$T/r" >/dev/null 2>&1; rc=$?
[ $rc = 0 ] && [ -s "$T/r/assets/person-b9.webm" ]; ok last_line_without_newline $?
bash "$here/render.sh" "$T/q" "$T/out.mp4" > "$T/o" 2>&1; rc=$?
python3 -c "
import json, sys
l = [x for x in open(sys.argv[1]) if x.startswith('{')]; v = json.loads(l[-1]) if l else {}
print('ok' if v and v.get('pass') is True and v['target_lufs'] == -14 and abs(v['duration'] - 100) < 0.5 else 'bad')" "$T/o" > "$T/o2"
[ $rc = 0 ] && [ -s "$T/out.mp4" ] && [ "$(cat "$T/o2")" = ok ]; ok render_passes_and_reports $?
bash "$here/render.sh" "$T/q" "$T/out4.mp4" --pace 1.1 --end 80 > "$T/o" 2>&1; rc=$?; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$T/out4.mp4")
[ $rc = 0 ] && python3 -c "import sys; sys.exit(0 if abs(float(sys.argv[1]) - 72.73) < 0.3 else 1)" "$d"; ok render_pace_and_end_set_the_length $?
rm -f "$T/out2.mp4"; STUB_MEASURE_FAIL=1 bash "$here/render.sh" "$T/q" "$T/out2.mp4" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && ! grep -q '"pass": true' "$T/o"; ok control_failed_measurement_fails $?
rm -f "$T/out7.mp4"; STUB_SHORT_VIDEO=1 bash "$here/render.sh" "$T/q" "$T/out7.mp4" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && grep -q '"pass": false' "$T/o"; ok control_short_video_long_audio_fails $?
rm -f "$T/out3.mp4"; STUB_SHORT=1 bash "$here/render.sh" "$T/q" "$T/out3.mp4" > "$T/o" 2>&1; rc=$?
[ $rc != 0 ] && grep -q '"pass": false' "$T/o"; ok control_wrong_length_render_fails $?
bash "$here/render.sh" "$T/q" "$T/out5.mp4" --pace 3 >/dev/null 2>&1; rc=$?; [ $rc = 2 ] && [ ! -e "$T/out5.mp4" ]; ok control_bad_option_refused $?
bash "$here/render.sh" "$T/q" "$T/out6.mp4" --end 0 >/dev/null 2>&1; rc1=$?; bash "$here/render.sh" "$T/q" "$T/out6.mp4" --end 1e0 >/dev/null 2>&1; rc3=$?; bash "$here/render.sh" "$T/q" "$T/out6.mp4" --end 9999 >/dev/null 2>&1; rc2=$?; [ $rc1 = 2 ] && [ $rc2 = 2 ] && [ $rc3 = 2 ] && [ ! -e "$T/out6.mp4" ]; ok control_bad_end_refused $?

python3 - "$res" "${1:-}" <<'PY'
import json, sys
c = {a: b == "true" for a, b in (l.rstrip("\n").split("\t") for l in open(sys.argv[1]))}
v = {"checks": c, "pass": all(c.values()) and len(c) == 33}
s = json.dumps(v, indent=2); print(s)
if sys.argv[2]: open(sys.argv[2], "w").write(s + "\n")
sys.exit(0 if v["pass"] else 1)
PY
