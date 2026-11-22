#!/usr/bin/env python3
"""Turn `whisper-cli -ml 1 -nfa -dtw MODEL -ojf` output into Python whisper's word JSON.

  cpp2words.py raw.json > a.json      # {"segments": [{"start","end","text","words":[...]}]}

edit.py and verify.py read the Python shape, so one adapter keeps both
transcribers usable. whisper-cli's plain word times are smoothed across
silence, which hides a pause. DTW gives each token's end time, which matches
Python whisper. It gives no start, so a word starts at the later of the
previous end and (end - an estimated length). That keeps a real pause open.
"""
import json, re, sys

words, prev_end = [], 0.0
for e in json.load(open(sys.argv[1]))["transcription"]:
    w = e["text"].strip()
    if not w or re.fullmatch(r"[\[(].*[\])]", w):  # skip [BLANK_AUDIO], (music)
        continue
    dtw = [t["t_dtw"] for t in e.get("tokens", []) if t.get("t_dtw", -1) > 0 and re.search(r"\w", t["text"])]
    end = max(dtw) / 100 if dtw else e["offsets"]["to"] / 1000
    est = 0.1 + 0.07 * len(re.sub(r"\W", "", w))
    start = max(prev_end, end - est)
    words.append({"word": " " + w, "start": round(start, 2), "end": round(max(end, start), 2)})
    prev_end = words[-1]["end"]

segments, cur = [], []
for w in words:
    cur.append(w)
    if re.search(r"[.?!]$", w["word"]):
        segments.append(cur)
        cur = []
if cur:
    segments.append(cur)
print(json.dumps({"segments": [
    {"start": s[0]["start"], "end": s[-1]["end"],
     "text": "".join(w["word"] for w in s), "words": s} for s in segments]}))
