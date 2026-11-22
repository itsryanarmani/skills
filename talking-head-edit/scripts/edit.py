#!/usr/bin/env python3
"""Cut dead air and set loudness on a talking-head video. No model runs here.

  edit.py SRC OUT [--words w.json] [--cut START-END ...] [--report r.json]

Pauses come from the audio energy, not from transcript timestamps. Whisper
word ends run early, so cuts placed from them clip the tail of a word.
Needs ffmpeg, ffprobe and numpy.
"""
import argparse, atexit, json, os, shutil, subprocess, sys, tempfile
from fractions import Fraction
import numpy as np

FR = 160  # 10 ms frames at 16 kHz


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def ffprobe(path, show, *sel):
    return run(["ffprobe", "-v", "error", *sel, "-show_entries", show, "-of", "csv=p=0", path],
               capture_output=True, text=True).stdout.strip()


def probe_duration(path):
    return float(ffprobe(path, "format=duration"))


def audio_start(path):
    """Seconds the audio starts after the container clock (often 0.1-0.2 s). ffmpeg
    trims on the container clock; energy frames start at audio sample 0. Without
    this offset every cut lands early, inside the tail of the previous word.
    ffmpeg also shifts the clock by the container start, so subtract it."""
    try:
        return (float(ffprobe(path, "stream=start_time", "-select_streams", "a:0"))
                - float(ffprobe(path, "format=start_time")))
    except ValueError:
        return 0.0


def energy_db(path):
    """Per-10ms level in dB of the first audio stream."""
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-f", "f32le", "-ac", "1",
               "-ar", "16000", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32)
    n = len(x) // FR
    return 20 * np.log10(np.sqrt((x[:n * FR].reshape(n, FR) ** 2).mean(1)) + 1e-9)


def silent_runs(db, floor, min_len, margin=10):
    """(start, end) frame runs quieter than floor+margin dB and at least min_len frames."""
    d = np.diff(np.concatenate(([0], (db < floor + margin).astype(int), [0])))
    return [(int(s), int(e)) for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0])
            if e - s >= min_len]


def snap(db, t, reach=0.08):
    """Move a hand-picked cut edge to the quietest 10 ms within +-reach."""
    i = int(t * 100)
    lo, hi = max(i - int(reach * 100), 0), min(i + int(reach * 100) + 1, len(db))
    return (lo + int(np.argmin(db[lo:hi]))) / 100


def plan(db, total, gap, keep_gap, extra, lead, tail):
    floor = float(np.percentile(db, 10))
    half = keep_gap / 2
    n = len(db)
    remove = []
    # true silences only, found from the audio energy. Never from word times.
    for s, e in silent_runs(db, floor, int(gap * 100), 10):
        if s == 0:
            if e / 100 - lead > 0.05:
                remove.append((0.0, e / 100 - lead))
        elif e >= n - 1:
            if total - (s / 100 + tail) > 0.05:
                remove.append((s / 100 + tail, total))
        else:
            remove.append((s / 100 + half, e / 100 - half))
    remove += [(snap(db, a), snap(db, b)) for a, b in extra]
    merged = []
    for r in sorted(r for r in remove if r[1] - r[0] > 0.02):
        if merged and r[0] <= merged[-1][1] + 0.02:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
        else:
            merged.append(r)
    remove = merged
    keep, t = [], 0.0
    for r0, r1 in remove:
        if r0 > t:
            keep.append((t, r0))
        t = max(t, r1)
    if t < total:
        keep.append((t, total))
    return keep, remove, floor


def make_mapper(keep):
    def newt(o):
        acc = 0.0
        for k0, k1 in keep:
            if o <= k0:
                return acc
            if o < k1:
                return acc + (o - k0)
            acc += k1 - k0
        return acc
    return newt


def measure_lufs(wav, target, tp):
    err = run(["ffmpeg", "-hide_banner", "-i", wav, "-af",
               f"loudnorm=I={target}:TP={tp}:LRA=11:print_format=json",
               "-f", "null", "-"], capture_output=True, text=True).stderr
    return json.loads(err[err.rindex("{"):err.rindex("}") + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--words", help="whisper JSON: only used to flag sounds with no word")
    ap.add_argument("--cut", action="append", default=[], help="extra removal START-END seconds")
    ap.add_argument("--gap", type=float, default=0.5, help="shorten silences longer than this")
    ap.add_argument("--keep-gap", type=float, default=0.3, help="silence left after a cut")
    ap.add_argument("--lead", type=float, default=0.3, help="silence kept before the first word")
    ap.add_argument("--tail", type=float, default=0.5, help="silence kept after the last word")
    ap.add_argument("--fade", type=float, default=0.015, help="audio fade at each join, seconds")
    ap.add_argument("--lufs", type=float, default=-16)
    ap.add_argument("--tp", type=float, default=-1.5)
    ap.add_argument("--crf", default="20")
    ap.add_argument("--preset", default="veryfast")
    ap.add_argument("--no-offset-fix", action="store_true",
                    help="test only: ignore the audio start offset, to prove the test catches it")
    ap.add_argument("--report")
    a = ap.parse_args()

    for p in (a.out, a.report):  # never write over the source, by any path
        if p and os.path.exists(p) and os.path.samefile(p, a.src):
            sys.exit("refusing to overwrite the source")
    work = tempfile.mkdtemp(prefix="the-")
    atexit.register(shutil.rmtree, work, ignore_errors=True)
    a0 = 0.0 if a.no_offset_fix else audio_start(a.src)
    container_total = probe_duration(a.src)
    total = container_total - a0           # audio-clock length; plan() works on this clock
    db = energy_db(a.src)
    extra = [tuple(float(x) for x in c.split("-")) for c in a.cut]
    words = None
    if a.words:
        words = [w for s in json.load(open(a.words))["segments"] for w in s.get("words", [])]
    keep, removed, floor = plan(db, total, a.gap, a.keep_gap, extra, a.lead, a.tail)
    # snap every cut to the video frame grid, so audio and video cut at the same instants
    fps = float(Fraction(ffprobe(a.src, "stream=r_frame_rate", "-select_streams", "v:0")))
    keep = [(round((s + a0) * fps) / fps - a0, round((e + a0) * fps) / fps - a0) for s, e in keep]
    newt = make_mapper(keep)
    n = len(keep)
    new_len = sum(k1 - k0 for k0, k1 in keep)

    # voiced stretches whisper gave no word to: an "um" or a breath. FLAG only.
    # Word times are early or late by up to 0.5 s, so cutting from them clipped a word.
    sounds = []
    for x, y in zip(words or [], (words or [])[1:]):
        if y["start"] - x["end"] > 0.5:
            seg = db[int((x["end"] + 0.2) * 100):int((y["start"] - 0.1) * 100)]
            if (seg > floor + 10).sum() >= 80:
                sounds.append({"at_s": round(x["end"], 1), "voiced_s": round(float((seg > floor + 10).sum()) / 100, 1)})

    # source level at each cut edge: must sit in silence or the cut clips a word
    def edge(t, side):
        i = int(t * 100)
        w = db[max(i - 4, 0):i] if side == "before" else db[i:i + 4]
        return float(w.max()) if len(w) else float("-inf")
    edges = [{"cut": [round(r0, 2), round(r1, 2)],
              "before_db": round(edge(r0, "before"), 1), "after_db": round(edge(r1, "after"), 1)}
             for r0, r1 in removed if 0.01 < r0 and r1 < total - 0.01]
    warns = [f"cut {e['cut']} edge is {max(e['before_db'], e['after_db'])} dB, "
             f"above silence ({round(floor + 14, 1)} dB): may clip a word"
             for e in edges if max(e["before_db"], e["after_db"]) > floor + 14]

    # audio: cut, fade each join, high-pass, then two-pass loudnorm
    f = a.fade
    parts = []
    for i, (s, e) in enumerate(keep):
        fx = ""
        if i > 0:
            fx += f",afade=t=in:st=0:d={f}"
        if i < n - 1:
            fx += f",afade=t=out:st={e - s - f:.3f}:d={f}"
        parts.append(f"[0:a]atrim={s + a0:.3f}:{e + a0:.3f},asetpts=PTS-STARTPTS{fx}[a{i}];")
    cat = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,highpass=f=80[ac]"
    cut_wav, norm_wav = f"{work}/cut.wav", f"{work}/norm.wav"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", a.src, "-vn",
         "-filter_complex", "".join(parts) + cat, "-map", "[ac]", cut_wav])
    m = measure_lufs(cut_wav, a.lufs, a.tp)
    ln = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA=11:measured_I={m['input_i']}:"
          f"measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", cut_wav,
         "-af", ln, "-ar", "48000", norm_wav])

    # video: cut with the same offset-corrected times
    chain = "".join(f"[0:v]trim={s + a0:.3f}:{e + a0:.3f},setpts=PTS-STARTPTS[v{i}];"
                    for i, (s, e) in enumerate(keep))
    chain += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[vc]"
    inputs = ["-i", a.src, "-i", norm_wav]
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + inputs +
        ["-filter_complex", chain, "-map", "[vc]", "-map", "1:a",
         "-c:v", "libx264", "-crf", a.crf, "-preset", a.preset, "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out])

    # measure the OUTPUT at every join: it must be as quiet as the room
    odb = energy_db(a.out)
    ofloor = float(np.percentile(odb, 10))
    joins, acc = [], 0.0
    for k0, k1 in keep[:-1]:
        acc += k1 - k0
        i = int(acc * 100)
        joins.append(float(odb[max(i - 2, 0):i + 3].max()) - ofloor)
    worst = round(max(joins), 1) if joins else 0.0
    if worst > 14:
        warns.append(f"a join in the output is {worst} dB above the room floor: listen to it")

    report = {"original_s": round(container_total, 2), "audio_start_s": round(a0, 3), "edited_s": round(probe_duration(a.out), 2),
              "planned_s": round(new_len, 2), "cuts": len(removed),
              "removed_s": round(total - new_len, 2),
              "loudness_in_lufs": float(m["input_i"]), "target_lufs": a.lufs,
              "worst_join_above_floor_db": worst, "joins_db": [round(j, 1) for j in joins],
              "keep": [[round(s, 3), round(e, 3)] for s, e in keep], "cut_edges": edges,
              "sound_without_word_to_review": sounds, "warnings": warns}
    if a.report:
        json.dump(report, open(a.report, "w"), indent=2)
    print(json.dumps({k: v for k, v in report.items() if k not in ("cut_edges", "keep", "joins_db")}, indent=2))


if __name__ == "__main__":
    sys.exit(main())
