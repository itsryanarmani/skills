#!/usr/bin/env python3
"""Measure an edited video and print a short verdict. No model runs here.

  verify.py OUT.mp4 REPORT.json EDITED_WORDS.json

Checks: loudness of the real output, joins that sit above the room floor,
cut edges that touch voice, and repeated words in the edited transcript
(stutters that a pause used to hide).
"""
import json, re, subprocess, sys

out, report_path, words_path = sys.argv[1:4]
r = json.load(open(report_path))
words = [w for s in json.load(open(words_path))["segments"] for w in s.get("words", [])]


def lufs(p):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-i", p, "-af", "loudnorm=print_format=json",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(e[e.rindex("{"):e.rindex("}") + 1])
    return float(j["input_i"]), float(j["input_tp"])


norm = lambda w: re.sub(r"[^a-z0-9']", "", w["word"].lower())
repeats = []
for a, b in zip(words, words[1:]):
    x, y = norm(a), norm(b)
    if x and (x == y or (len(x) <= 2 and y.startswith(x) and y != x)):
        repeats.append({"at_s": round(a["start"], 1), "text": f"{x} {y}"})

sd = lambda s: float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", s, "-show_entries",
                                     "stream=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
i, tp = lufs(out)
checks = {
    "av_lengths_match": abs(sd("v:0") - sd("a:0")) <= 0.1,
    "length_matches_plan": abs(r["edited_s"] - r["planned_s"]) <= 0.15,
    "loudness_within_1lu": abs(i - r["target_lufs"]) <= 1.0,
    "true_peak_ok": tp <= -1.0,
    "joins_in_silence": r["worst_join_above_floor_db"] <= 14,
    "no_warnings": not r["warnings"],
}
v = {"original_s": r["original_s"], "edited_s": r["edited_s"], "planned_s": r["planned_s"],
     "removed_s": r["removed_s"],
     "cuts": r["cuts"], "loudness_lufs": i, "true_peak_db": tp,
     "worst_join_above_floor_db": r["worst_join_above_floor_db"],
     "repeated_words_to_review": repeats,
     "sound_without_word_to_review": r["sound_without_word_to_review"], "warnings": r["warnings"],
     "checks": checks, "pass": all(checks.values())}
print(json.dumps(v, indent=2))
sys.exit(0 if v["pass"] else 1)
