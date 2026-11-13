#!/usr/bin/env python3
"""Check a finished vertical video ad before anyone watches it. Exit 0 only if every check passes.

Usage: python3 video-ad-check.py VIDEO --manifest build.json --transcript words.json [options]

The build writes the manifest (see ad-video-styles/SKILL.md, section 6):
  {"duration": 15.9, "size": [1080, 1920], "allow": ["2 weeks"], "muted": false,
   "shots":    [{"start": 0, "end": 2.4}, ...],
   "voice":    [{"start": 0.6, "end": 2.4, "text": "I watched Dave go down"}, ...],
   "captions": [{"start": 0.6, "end": 1.5, "text": "I watched Dave"}, ...],
   "labels":   [{"text": "Dave", "start": 0.7, "end": 2.0}], "arrows": []}
The transcript is a list of {"text","start","end"} words from an independent speech-to-text run on the CLEAN voice track
(for example: npx hyperframes transcribe voice.wav --json). It is required: without it nothing proves that the captions
match what is really spoken. A video with no voice sets "muted": true and needs no transcript.
Needs ffmpeg and ffprobe. Standard library only.
"""
import argparse, json, re, subprocess, sys

results = []
def rec(name, ok, msg):
    results.append((name, ok, msg)); print(("PASS " if ok else "FAIL ") + f"{name}: {msg}")

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def norm(s): return re.findall(r"[a-z0-9']+", s.lower())

def rms_db(video, start, dur):
    r = run(["ffmpeg", "-hide_banner", "-ss", f"{start:.3f}", "-t", f"{dur:.3f}", "-i", video, "-vn", "-af", "astats=metadata=0:reset=0", "-f", "null", "-"])
    m = re.findall(r"RMS level dB:\s*(-?[\d.]+|-inf)", r.stderr)
    if not m: return -99.0
    return -99.0 if m[-1] == "-inf" else float(m[-1])

def rms_track(video):
    """RMS level (dB) of the audio every 0.05 s, in one pass. Returns [(time, db)]."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", video, "-vn", "-af", "aresample=16000,asetnsamples=n=800:p=0,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-", "-f", "null", "-"], capture_output=True, text=True)
    out, t = [], 0.0
    for line in r.stdout.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m: t = float(m.group(1)); continue
        m = re.search(r"RMS_level=(-?[\d.]+|-inf)", line)
        if m: out.append((t, -99.0 if m.group(1) == "-inf" else float(m.group(1))))
    return out

def gray_frame(video, t):
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-vf", "scale=64:114,format=gray", "-f", "rawvideo", "-"], capture_output=True)
    return r.stdout

def union_length(spans, lo, hi):
    """Length of the union of spans, clipped to [lo, hi]."""
    total, cur = 0.0, lo
    for s, e in sorted((max(s, lo), min(e, hi)) for s, e in spans if min(e, hi) > max(s, lo)):
        if e > cur: total += e - max(s, cur); cur = e
    return total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--manifest", required=True); ap.add_argument("--transcript")
    ap.add_argument("--max-shot", type=float, default=3.0); ap.add_argument("--max-labels", type=int, default=2); ap.add_argument("--max-arrows", type=int, default=1)
    ap.add_argument("--sync-tol", type=float, default=0.25); ap.add_argument("--transcript-tol", type=float, default=0.35)
    ap.add_argument("--hook-motion", type=float, default=15.0)
    a = ap.parse_args()

    try:
        m = json.load(open(a.manifest))
        shots, voice, caps = m["shots"], m["voice"], m["captions"]
        labels, arrows, allow = m.get("labels", []), m.get("arrows", []), [x.lower() for x in m.get("allow", [])]
        want_size, want_dur, muted = m["size"], m["duration"], bool(m.get("muted", False))
    except Exception as e:  # a missing or broken manifest is a failure, not a skip
        rec("manifest", False, f"cannot read {a.manifest}: {e}"); sys.exit(1)

    pr = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", a.video])
    try: info = json.loads(pr.stdout)
    except Exception: rec("file", False, "ffprobe could not read the video"); sys.exit(1)
    vs = [s for s in info["streams"] if s["codec_type"] == "video"]; au = [s for s in info["streams"] if s["codec_type"] == "audio"]
    dur = float(info["format"]["duration"])
    rec("size", bool(vs) and [vs[0]["width"], vs[0]["height"]] == want_size, f"{vs[0]['width']}x{vs[0]['height']}, the manifest says {want_size[0]}x{want_size[1]}" if vs else "no video stream")
    rec("duration", abs(dur - want_dur) <= 0.3, f"{dur:.2f}s, the manifest says {want_dur:.2f}s (allowed difference 0.3s)")
    rec("audio-present", bool(au) or muted, "audio stream found" if au else ("no audio stream, and the manifest says muted" if muted else "no audio stream"))

    lens = [s["end"] - s["start"] for s in shots]
    bad = [f"{l:.1f}s" for l in lens if l > a.max_shot or l < 0.8]
    avg = sum(lens) / len(lens)
    rec("cut-pace", not bad and avg <= 2.5, f"{len(lens)} shots, average {avg:.2f}s, longest {max(lens):.1f}s (each 0.8 to {a.max_shot:g}s, average 2.5s or less)" + (f"; out of range: {', '.join(bad)}" if bad else ""))

    frames = [gray_frame(a.video, t * 0.25) for t in range(0, 9)]
    diffs = [sum(abs(x - y) for x, y in zip(f1, f2)) / max(len(f1), 1) for f1, f2 in zip(frames, frames[1:]) if f1 and f2]
    mot = sum(diffs) / len(diffs) if diffs else 0.0
    rec("hook-motion", mot >= a.hook_motion, f"mean frame change in the first 2 s is {mot:.1f} (needs at least {a.hook_motion:g}; measured 21 on a sped-up fall, 13 on the slow cut, under 6 on calm talking shots)")
    rec("hook-cut", shots[0]["end"] - shots[0]["start"] <= 2.5, f"first shot runs {shots[0]['end'] - shots[0]['start']:.1f}s (needs 2.5s or less)")

    # voice: present, loud enough, and starting where the manifest says, measured in the RENDERED audio
    if not voice:
        rec("voice-present", muted, "the manifest has no voice lines and is marked muted" if muted else "the manifest has no voice lines and is not marked muted")
    elif not au:
        rec("voice-present", False, "the manifest lists voice lines but the video has no audio")
    else:
        gaps = []; t = 0.0
        for v in sorted(voice, key=lambda x: x["start"]):
            if v["start"] - t >= 0.4: gaps.append((t, v["start"] - t))
            t = max(t, v["end"])
        if dur - t >= 0.4: gaps.append((t, dur - t))
        floor = max([rms_db(a.video, s, d) for s, d in gaps] or [-60.0])
        levels = [rms_db(a.video, v["start"], v["end"] - v["start"]) for v in voice]
        weak = [f"{v['text'][:24]!r} ({lv:.0f} dB)" for v, lv in zip(voice, levels) if lv < floor + 6 or lv < -45]
        rec("voice-present", not weak, f"voice is at least 6 dB above the gap level ({floor:.0f} dB) and above -45 dB in all {len(voice)} windows" if not weak else "voice is missing or too quiet in: " + ", ".join(weak))
        track = rms_track(a.video)
        thr = max(sorted(levels)[len(levels) // 2] - 12, -50.0)   # relative to the voice itself, so speech with no gaps still works
        late, prev_end = [], -1.0
        for v in sorted(voice, key=lambda x: x["start"]):
            lo = max(v["start"] - 0.5, prev_end + 0.02)   # do not mistake the tail of the line before for this onset
            hit = next((t for t, db in track if lo <= t <= v["start"] + 1.0 and db >= thr), None)
            prev_end = v["end"]
            if hit is None or abs(hit - v["start"]) > a.sync_tol + 0.05: late.append(f"{v['text'][:24]!r}: heard at {('%.2f' % hit) if hit is not None else 'never'}s, manifest says {v['start']:.2f}s")
        rec("voice-onset", not late, f"the voice starts within {a.sync_tol + 0.05:.2f}s of the manifest in all {len(voice)} lines (found in the rendered audio)" if not late else "; ".join(late))
        vd = run(["ffmpeg", "-hide_banner", "-i", a.video, "-vn", "-af", "volumedetect", "-f", "null", "-"]).stderr
        mx = re.search(r"max_volume:\s*(-?[\d.]+)", vd); mn = re.search(r"mean_volume:\s*(-?[\d.]+)", vd)
        mxv, mnv = float(mx.group(1)) if mx else 0.0, float(mn.group(1)) if mn else -99.0
        rec("audio-level", mxv <= -1.0 and mnv >= -35.0, f"peak {mxv:.1f} dB (needs -1 or lower), mean {mnv:.1f} dB (needs -35 or higher)")

    # captions: short, spelled exactly like the line, on time, and on screen for the whole line
    over = next((c["text"] for c in caps if len(norm(c["text"])) > 6), None)
    rec("caption-length", over is None, "every caption has 6 words or fewer" if over is None else "caption over 6 words: " + over)
    sync_bad, cover_bad = [], []
    for v in voice:
        lw = norm(v["text"]); lset = set(lw)
        mine = sorted((c for c in caps if norm(c["text"]) and set(norm(c["text"])) <= lset and c["end"] > v["start"] - 1.5 and c["start"] < v["end"] + 1.5), key=lambda c: c["start"])
        if not mine: cover_bad.append(f"{v['text'][:28]!r} has no caption"); continue
        spelled = [w for c in mine for w in norm(c["text"])]
        if spelled != lw: cover_bad.append(f"{v['text'][:28]!r}: captions spell {' '.join(spelled)!r}, the line is {' '.join(lw)!r}")
        d0, d1 = mine[0]["start"] - v["start"], mine[-1]["end"] - v["end"]
        if abs(d0) > a.sync_tol or d1 < -0.15: sync_bad.append(f"{v['text'][:28]!r}: caption starts {d0:+.2f}s from the voice, ends {d1:+.2f}s from it")
        cov = union_length([(c["start"], c["end"]) for c in mine], v["start"], v["end"]) / max(v["end"] - v["start"], 0.01)
        if cov < 0.85: cover_bad.append(f"{v['text'][:28]!r} is captioned for only {cov * 100:.0f}% of the line")
    rec("sync-manifest", not sync_bad, f"captions start within {a.sync_tol}s of each voice line and end no more than 0.15s before it" if not sync_bad else "; ".join(sync_bad))
    rec("mute-coverage", not cover_bad, f"all {len(voice)} spoken lines are captioned word for word, for at least 85% of their length (the story reads with sound off)" if not cover_bad else "; ".join(cover_bad))

    # independent transcript: required whenever there is a voice
    if not voice and muted:
        rec("sync-transcript", True, "muted video, no voice to check")
    elif not a.transcript:
        rec("sync-transcript", False, "no --transcript given: nothing proves the captions match the spoken words. Transcribe the clean voice track and pass it")
    else:
        try: words = json.load(open(a.transcript))
        except Exception as e: rec("sync-transcript", False, f"cannot read transcript: {e}"); words = None
        if words is not None:
            words = [dict(w) for w in words if norm(w["text"])]
            if len(words) > 1 and words[0]["end"] - words[0]["start"] < 0.25 and words[1]["start"] - words[0]["end"] > 0.3:
                words[0]["start"] = words[1]["start"] - 0.3   # speech-to-text often reports a first word at 0.0 after leading silence
            seq = [norm(w["text"])[0] for w in words]; pos, off, bad = 0, [], []
            script = [x for v in sorted(voice, key=lambda v: v["start"]) for x in norm(v["text"])]
            if seq != script:
                bad.append(f"the voice says {' '.join(seq)[:90]!r} but the script says {' '.join(script)[:90]!r}")
            vocab = {x for v in voice for x in norm(v["text"])}
            for c in caps:
                cw = norm(c["text"])
                if not cw or not (set(cw) & vocab): continue   # end cards and other captions that share no word with the voice
                if seq[pos: pos + len(cw)] != cw:
                    hit = next((i for i in range(pos, len(seq)) if seq[i: i + len(cw)] == cw), None)
                    if hit is None: bad.append(f"{c['text']!r} is not what the voice says there"); continue
                    if hit > pos: bad.append(f"captions skip the spoken words {' '.join(seq[pos:hit])!r} before {c['text']!r}")
                    pos = hit
                off.append((c["text"], c["start"] - words[pos]["start"])); pos += len(cw)
            if pos < len(seq): bad.append(f"the voice says {' '.join(seq[pos:])!r} at the end with no caption")
            bad += [f"{t!r} is {d:+.2f}s from the spoken words" for t, d in off if abs(d) > a.transcript_tol]
            rec("sync-transcript", not bad, f"{len(off)} captions match the spoken words, word for word, within {a.transcript_tol}s" if not bad else "; ".join(bad))

    # overlays and claims
    rec("overlay-density", len(labels) <= a.max_labels and len(arrows) <= a.max_arrows, f"{len(labels)} labels (max {a.max_labels}), {len(arrows)} arrows (max {a.max_arrows})")
    short = [l["text"] for l in labels if l["end"] - l["start"] < 1.0]
    rec("label-hold", not short, "every label stays on screen at least 1.0 s" if not short else "label on screen under 1.0 s: " + ", ".join(short))
    bad = []
    for c in caps:
        rest = c["text"].lower()
        for x in allow: rest = rest.replace(x, " ")      # remove each confirmed claim, then look at what is left
        if re.search(r"[\d%$]|guarantee|risk-free", rest): bad.append(c["text"])
    rec("claims", not bad, "no unconfirmed numbers or guarantees in captions" if not bad else "unconfirmed claim in caption: " + "; ".join(bad))

    failed = [r for r in results if not r[1]]
    print(f"\n{len(results)} checks, {len(failed)} failed")
    sys.exit(1 if failed else 0)

main()
