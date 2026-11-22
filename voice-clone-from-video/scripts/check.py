#!/usr/bin/env python3
"""Rough check that a cloned voice matches its sample. It is not a likeness judge: listen too.

  check.py SAMPLE.wav GENERATED.mp3 "the exact text that was spoken"

Passes when the median pitch is within 15% of the sample and the transcript of the
generated audio matches the text in order (90% sequence match). Needs ffmpeg, numpy,
whisper-cli and a ggml model. With no model it FAILS CLOSED (exit 2): an unchecked
transcript is not a pass.
"""
import difflib, json, os, re, subprocess, sys, tempfile
import numpy as np

SR = 16000


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def pitch(x):
    """Median, 10th and 90th percentile of voiced pitch in Hz (autocorrelation, 40 ms frames)."""
    fr, hop, f0 = int(0.04 * SR), int(0.01 * SR), []
    lo, hi = int(SR / 300), int(SR / 70)
    for i in range(0, len(x) - fr, hop):
        w = x[i:i + fr] - x[i:i + fr].mean()
        if np.sqrt((w ** 2).mean()) < 0.02:
            continue
        ac = np.correlate(w, w, "full")[fr - 1:]
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] / ac[0] > 0.4:
            f0.append(SR / k)
    return [float(np.percentile(f0, p)) for p in (50, 10, 90)] if f0 else [0.0, 0.0, 0.0]


def words(text):
    return re.findall(r"[\w']+", text.lower())   # Unicode words, so no script is dropped


def transcript(path):
    model = os.environ.get("WHISPER_CPP_MODEL", os.path.expanduser("~/.cache/hyperframes/whisper/models/ggml-small.en.bin"))
    if not os.path.exists(model):
        return None
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, "g.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav], check=True)
        return subprocess.run(["whisper-cli", "-m", model, "-f", wav, "-nt", "-np"], capture_output=True, text=True).stdout


sample, gen, text = sys.argv[1:4]
ps, pg = pitch(load(sample)), pitch(load(gen))
t = transcript(gen)
res = {"sample_pitch_hz": [round(v) for v in ps], "generated_pitch_hz": [round(v) for v in pg],
       "pitch_ratio": round(pg[0] / ps[0], 2) if ps[0] else None}
res["pitch_ok"] = bool(ps[0] and abs(pg[0] / ps[0] - 1) <= 0.15)
if t is None:
    res.update(transcript="no whisper-cli model, so the words are unchecked", words_ok=None, pass_=False)
    print(json.dumps({("pass" if k == "pass_" else k): v for k, v in res.items()}, indent=2))
    sys.exit(2)
want, got = words(text), words(t)
res["transcript"] = " ".join(got)
ratio = difflib.SequenceMatcher(None, want, got).ratio()  # order and counts matter
res["word_match"] = round(ratio, 2)
res["words_ok"] = bool(want) and ratio >= 0.9   # test the unrounded value
res["pass"] = res["pitch_ok"] and res["words_ok"]
print(json.dumps(res, indent=2))
sys.exit(0 if res["pass"] else 1)
