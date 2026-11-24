#!/usr/bin/env python3
"""mutate.py  Removes each fix from a copy of these scripts, runs e2e.sh, and checks the check named for it fails.
Prints CAUGHT or MISSED per mutation. Exit 0 only if all are caught. About 6 minutes (4 runs in parallel)."""
import json, os, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
SRC = os.path.dirname(os.path.abspath(__file__))
M = [("no-morph-guard", "build.py", "t0 = max(t0, past[-1][0] + 0.7)", "pass", "cutout_waits_for_morph"),
     ("no-shift-recheck", "build.py", 'if again[-1][1] != "full":', "if False:", "build_refuses_shifted_window_in_panel"),
     ("probe-fallback", "build.py", "DUR = round(_probe(), 2)", "DUR = 99.3", "build_requires_base_video"),
     ("gen2-path", "build.py", "assets/gen/", "assets/gen2/", "build_full_structure"),
     ("immediate-render", "build.py", "immediateRender:false", "immediateRender:true", "build_full_structure"),
     ("no-window-refusal", "build.py", 'if past and past[-1][1] != "full":|if again[-1][1] != "full":', "if False:|if False:", "build_refuses_bad_windows"),
     ("mask-measure", "render.sh", '|| { echo "render: loudness measurement failed" >&2; exit 1; }', "|| true", "control_failed_measurement_fails"),
     ("verdict-target", "render.sh", "abs(l + 16) <= 1", "abs(l + 80) <= 1", "render_passes_and_reports"),
     ("no-length-check", "render.sh", "abs(d - b) <= 0.15", "True", "control_wrong_length_render_fails"),
     ("lost-last-line", "cutouts.sh", ' || [ -n "$id" ]', "", "last_line_without_newline"),
     ("ffmpeg-stdin", "cutouts.sh", '-nostdin -v error -y -ss "$a" -t "$d" -i "$IN" -c:v libx264 -crf 12 -an "$T/$id.mp4" </dev/null', '-v error -y -ss "$a" -t "$d" -i "$IN" -c:v libx264 -crf 12 -an "$T/$id.mp4"', "cutouts_expected_file_per_window"),
     ("swallow-cutout-failure", "cutouts.sh", "--quality best >/dev/null </dev/null\n", "--quality best >/dev/null </dev/null || true\n", "control_failed_cutout_fails_script")]


def run(m):
    name, f, a, b, expect = m
    d = tempfile.mkdtemp(); shutil.copytree(SRC, d + "/s", ignore=shutil.ignore_patterns("mutate.py"))
    t = open(f"{d}/s/{f}").read()
    for x, y in zip(a.split("|"), b.split("|")):   # "|" lists several replacements (a guard that has a second guard behind it)
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


with ThreadPoolExecutor(4) as ex:
    out = list(ex.map(run, M))
for n, r in out:
    print(n, r)
sys.exit(0 if all(r.startswith("CAUGHT") for _, r in out) else 1)
