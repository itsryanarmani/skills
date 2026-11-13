#!/usr/bin/env python3
"""Measure how expressive and how tight a spoken take is, with numbers, and fail a flat or gappy take. Needs ffmpeg and numpy.

Usage: python3 prosody.py [--min-range 6] [--max-pause 0.5] [--max-lead 0.35] take1.mp3 take2.wav ...
Exit 0 only if every take passes both limits. Per take it prints:
  range  = pitch range in semitones, 10th to 90th percentile of the voiced frames. A flat read measured 2.7 to 3.7;
           lively takes measured 12 to 17 on the same lines.
  std    = standard deviation of the pitch in semitones
  swing  = mean pitch change per 10 ms in cents
  loud   = loudness range in dB (10th to 90th percentile of the voiced frames)
  pauses = silences over 0.25 s inside the speech, and the longest one in seconds
  speech = seconds from the first to the last sound
  lead   = seconds of sound that is not voiced before the first voiced frame (a breath or an exhale before the first word)
Pitch comes from autocorrelation (70 to 400 Hz), so treat it as a measure to compare takes, not as a lab instrument.
"""
import argparse, subprocess, sys
import numpy as np

SR = 16000

def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)

def pitch_track(x, hop=160, win=640, fmin=70, fmax=400):
    f0, rms = [], []
    lo, hi = SR // fmax, SR // fmin
    for i in range(0, len(x) - win, hop):
        fr = x[i:i + win]; fr = fr - fr.mean()
        e = float(np.sqrt(np.mean(fr * fr)) + 1e-9); rms.append(e)
        if e < 0.01: f0.append(0.0); continue
        ac = np.correlate(fr, fr, mode="full")[win - 1:]
        ac = ac / (ac[0] + 1e-9)
        k = lo + int(np.argmax(ac[lo:hi]))
        f0.append(SR / k if ac[k] > 0.35 else 0.0)
    return np.array(f0), np.array(rms)

def measure(path):
    x = load(path); f0, rms = pitch_track(x)
    db = 20 * np.log10(rms + 1e-9)
    voiced = f0 > 0
    if voiced.sum() < 10: return None
    st = 12 * np.log2(f0[voiced] / np.median(f0[voiced]))
    rng = float(np.percentile(st, 90) - np.percentile(st, 10))
    v = np.where(voiced)[0]; cents = np.abs(np.diff(1200 * np.log2(f0[v] / f0[v].min()))); cents = cents[(np.diff(v) == 1)]
    loud = float(np.percentile(db[voiced], 90) - np.percentile(db[voiced], 10))
    active = db > -45; idx = np.where(active)[0]
    first, last = idx[0], idx[-1]
    runs, cur = [], 0
    for a in active[first:last + 1]:
        if not a: cur += 1
        elif cur: runs.append(cur * 0.01); cur = 0
    long = [r for r in runs if r > 0.25]
    return dict(range=rng, std=float(st.std()), swing=float(cents.mean()) if len(cents) else 0.0, loud=loud, npause=len(long), longest=max(long) if long else 0.0, speech=(last - first) * 0.01, lead=max(0.0, (int(v[0]) - int(first)) * 0.01), first_voiced=int(v[0]) * 0.01)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("takes", nargs="+"); ap.add_argument("--min-range", type=float, default=6.0); ap.add_argument("--max-pause", type=float, default=0.5); ap.add_argument("--max-lead", type=float, default=0.35)
    a = ap.parse_args(); bad = 0
    for p in a.takes:
        m = measure(p); name = p.split("/")[-1]
        if m is None: print(f"FAIL voiced: {name} has too few voiced frames to measure"); bad += 1; continue
        print(f"{name:28s} range {m['range']:4.1f} st  std {m['std']:3.1f}  swing {m['swing']:4.0f} c  loud {m['loud']:4.1f} dB  pauses {m['npause']} (longest {m['longest']:.2f}s)  speech {m['speech']:.2f}s  lead {m['lead']:.2f}s")
        if m["range"] < a.min_range: print(f"FAIL pitch-range: {name} spans {m['range']:.1f} semitones, needs {a.min_range:g} or more (a flat read)"); bad += 1
        if m["longest"] > a.max_pause: print(f"FAIL pause: {name} has a {m['longest']:.2f}s silence inside the speech, the limit is {a.max_pause:g}s"); bad += 1
        if m["lead"] > a.max_lead: print(f"FAIL lead: {name} has {m['lead']:.2f}s of unvoiced sound before the first word, the limit is {a.max_lead:g}s (trim the breath)"); bad += 1
    sys.exit(1 if bad else 0)

main()
