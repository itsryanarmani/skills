#!/usr/bin/env python3
"""Best-of-N voice takes (the loop used with prosody.py in ad-video-styles/SKILL.md). For each script line: generate N takes with the same voice and emotion tags, trim edge silence, squeeze any
inside pause to 0.15 s, measure pitch range and pauses (prosody.py), keep the most expressive take that passes the limits.
Writes vo/t<i>.wav (the file the build uses) and prints a table. Needs OPENROUTER_API_KEY and ffmpeg. Usage: python3 pick-voice.py [N]  (reads script.json: [{"say": "[tag] line with tags", "text": "line without tags"}, ...])
"""
import hashlib, json, os, subprocess, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent   # where prosody.py lives
WORK = Path.cwd()                          # where script.json is read and vo/ is written
src = (HERE / "prosody.py").read_text().replace("\nmain()\n", "\n")   # import the measuring code without running the CLI
ns = {}; exec(compile(src, "prosody", "exec"), ns)
measure = ns["measure"]
LINES = json.loads((WORK / "script.json").read_text())
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3
key = os.environ.get("OPENROUTER_API_KEY") or sys.exit("set OPENROUTER_API_KEY")
VOICE, MODEL = os.environ.get("VOICE", "laura"), os.environ.get("MODEL", "elevenlabs/eleven-v3")   # set VOICE and MODEL to try another
(WORK / "vo").mkdir(exist_ok=True)
CLEAN = ("silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03,"
         "silenceremove=stop_periods=-1:stop_duration=0.18:stop_threshold=-40dB:stop_silence=0.07,"
         "areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03,areverse")

def tts(text, out):
    req = urllib.request.Request("https://openrouter.ai/api/v1/audio/speech", data=json.dumps({"model": MODEL, "voice": VOICE, "input": text, "response_format": "mp3"}).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
    out.write_bytes(urllib.request.urlopen(req, timeout=180).read())

report, spent = [], 0.0
for i, ln in enumerate(LINES, 1):
    cands = []
    tag = hashlib.sha1(f"{MODEL}|{VOICE}|{ln['say']}".encode()).hexdigest()[:8]   # a changed line, voice or model must not reuse old audio
    for k in range(1, N + 1):
        mp3 = WORK / "vo" / f"take{i}_{k}_{tag}.mp3"
        if not mp3.exists(): tts(ln["say"], mp3); spent += 0.005
        wav = WORK / "vo" / f"take{i}_{k}_{tag}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3), "-af", CLEAN, str(wav)], check=True)
        m = measure(str(wav))
        if m and m["lead"] > 0.35:   # a long unvoiced lead-in (a breath), not a hard s or f: cut it, keep 0.15 s of air
            cut = WORK / "vo" / f"take{i}_{k}_{tag}_trim.wav"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(m['first_voiced'] - 0.15, 0):.2f}", "-i", str(wav), str(cut)], check=True)
            cut.replace(wav); m = measure(str(wav))
        if m: cands.append((m, wav, k))
    ok = [c for c in cands if c[0]["range"] >= 6.0 and c[0]["longest"] <= 0.5 and c[0]["lead"] <= 0.35]
    pool = ok or cands
    best = max(pool, key=lambda c: c[0]["range"])
    (WORK / "vo" / f"t{i}.wav").write_bytes(best[1].read_bytes())
    report.append((i, ln["text"], best[2], best[0], bool(ok), [round(c[0]["range"], 1) for c in cands]))
for i, text, k, m, passed, ranges in report:
    print(f"line {i} take {k}: range {m['range']:.1f} st, longest pause {m['longest']:.2f}s, {m['speech']:.2f}s  {'PASS' if passed else 'FAIL (no take passed)'}  all ranges {ranges}  {text}")
print(f"extra speech spend about USD {spent:.3f}")
sys.exit(0 if all(r[4] for r in report) else 1)
