#!/usr/bin/env python3
"""mutate.py  Removes each fix from a copy of these scripts, runs e2e.sh, and checks the check named for it fails.
Prints CAUGHT or MISSED per mutation. Exit 0 only if all are caught. About 15 minutes (4 runs in parallel).
A "@@" in a pattern lists several replacements made together (a guard that has a second guard behind it)."""
import json, os, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
SRC = os.path.dirname(os.path.abspath(__file__))
OFF = "assert True or "
M = [
 ("no-sheet-settle-rule", "build.py", "assert first >= enter", OFF + "first >= enter", "pace_visual_waits_for_sheet"),
 ("no-sheet-after-visual-rule", "build.py", 'assert enter >= prev["items"][-1][2]', OFF + 'enter >= prev["items"][-1][2]', "pace_sheet_waits_for_last_visual"),
 ("no-return-wait-rule", "build.py", 'assert prev["exit"] is None or enter', OFF + 'prev["exit"] is None or enter', "pace_wait_after_return_to_full"),
 ("no-leave-rule", "build.py", "assert exit_ is None or b <=", OFF + "exit_ is None or b <=", "pace_visual_gone_before_sheet_leaves"),
 ("no-fade-room-rule", "build.py", "assert b - a >= FADE_IN", OFF + "b - a >= FADE_IN", "pace_visual_has_room_to_fade"),
 ("no-duplicate-id-rule", "build.py", "assert i not in _IDS", OFF + "i not in _IDS", "build_refuses_duplicate_ids"),
 ("regex-ids", "build.py", "html_ids = [x for it in items for x in ids_in(it[3])]", "html_ids = [x for it in items for x in re.findall(r'\\bid=\"([^\"]+)\"', it[3])]", "build_refuses_single_quoted_duplicate_ids"),
 ("no-reserved-ids", "build.py", "_IDS = set(RESERVED)", "_IDS = set()", "build_refuses_reserved_ids"),
 ("no-element-id-rule", "build.py", " + html_ids:", ":", "build_refuses_duplicate_element_ids"),
 ("no-duration-rule", "build.py", 'assert b <= DUR + 0.01', OFF + 'b <= DUR + 0.01', "build_refuses_visual_past_the_video"),
 ("no-overlap-rule", "build.py", "assert i == 0 or a >=", OFF + "i == 0 or a >=", "pace_visuals_do_not_overlap"),
 ("no-word-wait-rule", "build.py", "assert pop >= past[-1][0] + 1.0", OFF + "pop >= past[-1][0] + 1.0", "pace_word_waits_after_morph"),
 ("no-morph-shift", "build.py", "t0 = max(t0, past[-1][0] + 0.7)", "pass", "pace_cutout_starts_after_morph"),
 ("no-panel-guard", "build.py", 'if past and past[-1][1] != "full":@@if [(t, st) for t, st in SEQ if t <= t0 + 0.01][-1][1] != "full":', "if False:@@if False:", "build_refuses_bad_windows"),
 ("no-shift-recheck", "build.py", 'if [(t, st) for t, st in SEQ if t <= t0 + 0.01][-1][1] != "full":', "if False:", "build_refuses_bad_windows"),
 ("no-crossing-guard", "build.py", "if nxt and t1 > nxt[0] - 0.4:", "if False:", "build_refuses_bad_windows"),
 ("no-id-guard", "build.py", 'if not re.fullmatch(r"[a-z0-9_-]+", id):', "if False:", "build_refuses_bad_windows"),
 ("probe-fallback", "build.py", "DUR = round(_probe(), 2)", "DUR = 99.3", "build_requires_base_video"),
 ("no-boil", "build.py", "for(let k=0;k<{int(", "for(let k=0;k<0*{int(", "paper_craft_details_are_present"),
 ("boil-step-24", "build.py", "+k/12);tl.set", "+k/24);tl.set", "paper_craft_details_are_present"),
 ("boil-fixed-variant", "build.py", "clipPath:VI[k%3]", "clipPath:VI[0]", "paper_craft_details_are_present"),
 ("no-grain-css", "build.py", ".tex{position:absolute;", ".texx{position:absolute;", "paper_craft_details_are_present"),
 ("no-paper-tags", "build.py", 'card(big("Role title<br>here", 110), 1000, 50)', 'big("Role title<br>here", 110)', "paper_craft_details_are_present"),
 ("stage-uncentred", "build.py", ".stage{position:absolute;top:0;left:115px;", ".stage{position:absolute;top:0;left:0px;", "paper_craft_details_are_present"),
 ("no-paper-sound-file", "prep.sh", ',\n{"name":"paper","want":"a page of a paperback turned"}', "", "paper_sound_is_made_and_used"),
 ("gen2-path", "build.py", "assets/gen/", "assets/gen2/", "build_full_structure"),
 ("immediate-render", "build.py", "immediateRender:false", "immediateRender:true", "morphs_do_not_pre_render"),
 ("mask-measure", "render.sh", '|| { echo "render: loudness measurement failed" >&2; exit 1; }', "|| true", "control_failed_measurement_fails"),
 ("verdict-target", "render.sh", "abs(l - target) <= 1", "abs(l - 80) <= 1", "render_passes_and_reports"),
 ("no-length-check", "render.sh", " and abs(d - want) <= 0.2 and abs(vd - want) <= 0.2 and abs(ad - want) <= 0.2", "", "control_wrong_length_render_fails"),
 ("default-lufs", "render.sh", "LUFS=-14", "LUFS=-16", "render_passes_and_reports"),
 ("pace-ignored", "render.sh", "atempo=$PACE", "atempo=1.0", "render_pace_and_end_set_the_length"),
 ("end-ignored", "render.sh", 'inargs=(-t "$END")', "inargs=()", "render_pace_and_end_set_the_length"),
 ("no-stream-check", "render.sh", " and abs(vd - want) <= 0.2 and abs(ad - want) <= 0.2", "", "control_short_video_long_audio_fails"),
 ("no-end-range", "render.sh", " and 1 <= e <= b + 0.01", "", "control_bad_end_refused"),
 ("no-end-format", "render.sh", 're.fullmatch(r"[0-9]+(\\.[0-9]+)?", sys.argv[1]) and ', "", "control_bad_end_refused"),
 ("no-option-check", "render.sh", "sys.exit(0 if 0.9 <= p <= 1.15 and e >= 0 and -23 <= l <= -9 else 1)", "sys.exit(0)", "control_bad_option_refused"),
 ("lost-last-line", "cutouts.sh", ' || [ -n "$id" ]', "", "last_line_without_newline"),
 ("ffmpeg-stdin", "cutouts.sh", '-nostdin -v error -y -ss "$a" -t "$d" -i "$IN" -c:v libx264 -crf 12 -an "$T/$id.mp4" </dev/null', '-v error -y -ss "$a" -t "$d" -i "$IN" -c:v libx264 -crf 12 -an "$T/$id.mp4"', "cutouts_expected_file_per_window"),
 ("swallow-cutout-failure", "cutouts.sh", "--quality best >/dev/null </dev/null\n", "--quality best >/dev/null </dev/null || true\n", "control_failed_cutout_fails_script"),
]


def run(m):
    name, f, a, b, expect = m
    d = tempfile.mkdtemp(); shutil.copytree(SRC, d + "/s", ignore=shutil.ignore_patterns("mutate.py"))
    t = open(f"{d}/s/{f}").read()
    for x, y in zip(a.split("@@"), b.split("@@")):
        if x not in t:
            return name, "PATTERN-MISSING"
        t = t.replace(x, y)
    open(f"{d}/s/{f}", "w").write(t)
    if name == "swallow-cutout-failure":   # also drop the second guard so only set -e protects
        c = open(f"{d}/s/cutouts.sh").read(); open(f"{d}/s/cutouts.sh", "w").write("\n".join(l for l in c.split("\n") if "no output for" not in l))
    r = subprocess.run(["bash", f"{d}/s/e2e.sh"], capture_output=True, text=True)
    shutil.rmtree(d, ignore_errors=True)
    try:
        failed = [k for k, v in json.loads(r.stdout)["checks"].items() if not v]
    except Exception:
        return name, "NO-JSON"
    return name, ("CAUGHT" if expect in failed else "MISSED") + f" {failed}"


if __name__ == "__main__":
    with ThreadPoolExecutor(4) as ex:
        out = list(ex.map(run, M))
    for n, r in out:
        print(n, r)
    sys.exit(0 if all(r.startswith("CAUGHT") for _, r in out) else 1)
