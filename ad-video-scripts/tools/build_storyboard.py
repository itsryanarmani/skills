#!/usr/bin/env python3
"""Render a storyboard page from a scripts.json.

Usage: python3 build_storyboard.py scripts.json out.html [--img-base PATH_OR_URL_PREFIX]

Frame types per shot:
  person  an image with the on-screen text on top      (needs "img")
  end     an image, dimmed, with the end card text     (needs "img"; "onscreen" is "title\\nurl")
  card    a drawn card: {"card": {"title", "bullets", "hi": [bullet indexes to highlight]}}
The page shows a beat timeline, each shot with what is said, shown, edited and checked,
and a word-budget check per shot and per video (words at voice_rate_wps against the time).
A shot is flagged when its words need more than its slot plus 0.3 s.
Standard library only. Open the output in a browser. The page loads only the images under --img-base, so use a local folder, not a URL, for private images.
"""
import html, json, math, re, sys

e = html.escape
TOLERANCE_S = 0.3  # a shot may run this long past its slot
COL = {"Hook": "#c2410c", "Cost": "#b91c1c", "Turn": "#1d4ed8", "Proof": "#047857", "Afterthought": "#6d28d9"}
CSS = """
:root{--bg:#f7f5f0;--fg:#1a1a1a;--card:#fff;--bd:#e3dfd5;--mut:#615d55}
@media(prefers-color-scheme:dark){:root{--bg:#121212;--fg:#f1efe9;--card:#1c1c1c;--bd:#2f2f2f;--mut:#aaa69d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif}.w{max-width:1180px;margin:0 auto;padding:0 16px 60px}
h1{font-size:28px;margin:24px 0 4px}h2{margin:40px 0 6px;font-size:22px}.mut{color:var(--mut)}.box{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px 16px;margin:10px 0}
.tl{display:flex;height:26px;border-radius:8px;overflow:hidden;margin:10px 0}.tl div{color:#fff;font:700 11px/26px system-ui;text-align:center}
.shots{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;align-items:start}@media(max-width:900px){.shots{grid-template-columns:repeat(2,1fr)}}
.sh{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:8px;font-size:12px}
.fr{position:relative;aspect-ratio:9/16;border-radius:10px;overflow:hidden;background:#222;margin-bottom:6px}.fr img{width:100%;height:100%;object-fit:cover;display:block}
.fr:after{content:"";position:absolute;left:6%;right:6%;top:14%;bottom:35%;border:1px dashed rgba(255,255,255,.55);pointer-events:none}
.ov{position:absolute;left:8%;right:8%;top:16%;text-align:center;color:#fff;font:900 20px/1.05 system-ui;text-shadow:0 2px 8px #000;text-transform:uppercase}
.end{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:14px;color:#fff;gap:10px}.end b{font-size:17px}.end span{font:9.5px ui-monospace,monospace;overflow-wrap:anywhere}
.card{position:absolute;inset:14% 6% 48% 6%;background:#ece7db;padding:12px;color:#222;border-radius:8px;overflow:hidden}.card h6{margin:0 0 4px;font-size:11px}.row{padding:3px 5px;border-radius:5px;margin:2px 0;background:#fff;font-size:8.5px;line-height:1.25}.row.hi{background:#fde68a;outline:2px solid #f59e0b}
.meta b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);margin-top:6px}.pill{display:inline-block;padding:1px 8px;border-radius:99px;color:#fff;font:700 11px system-ui}
.over{color:#b91c1c;font-weight:700}.ok{color:#047857;font-weight:700}
"""


def frame(s, base):
    kind = s.get("frame", "person")
    if kind == "card":
        c = s["card"]
        rows = "".join(f'<div class="row{" hi" if i in c.get("hi", []) else ""}">{e(b)}</div>' for i, b in enumerate(c.get("bullets", [])))
        return f'<div class="card"><h6>{e(c["title"])}</h6>{rows}</div><div class="ov" style="top:auto;bottom:37%">{e(s["onscreen"])}</div>'
    img = f'{base}{s["img"]}'
    if kind == "end":
        a, _, b = s["onscreen"].partition("\n")
        return f'<img src="{e(img)}" style="filter:brightness(.45)"><div class="end"><b>{e(a)}</b><span>{e(b)}</span></div>'
    return f'<img src="{e(img)}"><div class="ov">{e(s["onscreen"])}</div>'


def bail(msg):
    print("error: " + " ".join(str(msg).split()), file=sys.stderr)
    sys.exit(2)


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def validate(data):
    """Check the file before rendering, so bad input never prints 'every shot fits'. Returns the voice rate."""
    if not isinstance(data, dict) or not isinstance(data.get("videos"), list) or not data["videos"]:
        bail("the file needs a non-empty 'videos' list")
    meta = data.get("meta")
    if meta is None:
        meta = {}
    if not isinstance(meta, dict):
        bail("'meta' must be an object")
    wps = meta.get("voice_rate_wps", 2.4)
    if not finite(wps) or not 0.5 <= wps <= 6:
        bail("meta.voice_rate_wps must be a number from 0.5 to 6 words a second")
    for v in data["videos"]:
        if not isinstance(v, dict) or not all(isinstance(v.get(k), str) for k in ("id", "title", "offer", "goal", "hook_formula")):
            bail("each video needs text fields: id, title, offer, goal, hook_formula")
        shots = v.get("shots")
        if not isinstance(shots, list) or not shots:
            bail(f"video {v.get('id')}: 'shots' must be a non-empty list")
        prev_end = 0.0
        for n, s in enumerate(shots, 1):
            where = f"video {v['id']} shot {n}"
            if not isinstance(s, dict) or not all(isinstance(s.get(k), str) for k in ("beat", "spoken", "onscreen", "edit", "source")):
                bail(f"{where}: needs text fields beat, spoken, onscreen, edit, source")
            t = s.get("t")
            if not (isinstance(t, list) and len(t) == 2 and finite(t[0]) and finite(t[1])) or not 0 <= t[0] < t[1]:
                bail(f"{where}: 't' must be [start, end] with 0 <= start < end")
            if t[0] < prev_end - 1e-6:
                bail(f"{where}: starts at {t[0]} before the previous shot ends at {prev_end}")
            prev_end = t[1]
            kind = s.get("frame", "person")
            if kind not in ("person", "end", "card"):
                bail(f"{where}: unknown frame type {kind!r}")
            if kind in ("person", "end") and not isinstance(s.get("img"), str):
                bail(f"{where}: frame {kind} needs an 'img' text value")
            if kind == "card":
                c = s.get("card")
                if not (isinstance(c, dict) and isinstance(c.get("title"), str)):
                    bail(f"{where}: a card needs a 'card' object with a 'title'")
                b = c.get("bullets", [])
                if not (isinstance(b, list) and all(isinstance(x, str) for x in b)):
                    bail(f"{where}: card 'bullets' must be a list of text lines")
                if len(b) > 5:
                    bail(f"{where}: a card holds at most 5 bullets (it has {len(b)}); split it, because rows past five would be cut")
                h = c.get("hi", [])
                if not (isinstance(h, list) and all(isinstance(i, int) and not isinstance(i, bool) and 0 <= i < len(b) for i in h)):
                    bail(f"{where}: card 'hi' must be a list of row numbers inside 'bullets'")
    return float(wps)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, out = sys.argv[1], sys.argv[2]
    base = sys.argv[sys.argv.index("--img-base") + 1] if "--img-base" in sys.argv else ""
    if base and not base.endswith("/"):
        base += "/"
    try:
        data = json.load(open(src, encoding="utf-8"))
    except (OSError, ValueError) as err:
        bail(f"cannot read {src}: {err}")
    wps = validate(data)
    meta = data.get("meta") or {}
    parts = []
    for v in data["videos"]:
        total = v["shots"][-1]["t"][1]
        words = sum(len(re.findall(r"\b[\w'’-]+\b", s["spoken"])) for s in v["shots"])
        need = words / wps
        late = [s for s in v["shots"] if len(re.findall(r"\b[\w'’-]+\b", s["spoken"])) / wps > s["t"][1] - s["t"][0] + TOLERANCE_S]
        flag = (f'<span class="over">{len(late)} shot(s) too long: cut words or add time</span>' if late else
                f'<span class="over">over by {need - total:.0f} s: cut words</span>' if need > total else '<span class="ok">every shot fits</span>')
        tl = "".join(f'<div style="width:{(s["t"][1] - s["t"][0]) / total * 100:.1f}%;background:{COL.get(s["beat"], "#555")}">{e(s["beat"])}</div>' for s in v["shots"])
        cards = ""
        for s in v["shots"]:
            slot = s["t"][1] - s["t"][0]
            sw = len(re.findall(r"\b[\w'’-]+\b", s["spoken"]))
            tight = ' <span class="over">too long</span>' if sw / wps > slot + TOLERANCE_S else ''
            cards += (f'<div class="sh"><div class="fr">{frame(s, base)}</div><span class="pill" style="background:{COL.get(s["beat"], "#555")}">{e(s["beat"])} · {s["t"][0]}–{s["t"][1]} s</span>'
                      f'<div class="meta"><b>Says ({sw} words, {sw / wps:.1f} s of {slot:.1f} s){tight}</b>“{e(s["spoken"])}”<b>On screen</b>{e(s["onscreen"]).replace(chr(10), " / ")}'
                      f'<b>Edit</b>{e(s["edit"])}<b>Claim check</b>{e(s["source"])}</div></div>')
        vo = " ".join(s["spoken"] for s in v["shots"])
        parts.append(f'<h2>{e(v["id"].upper())} · {e(v["title"])}</h2><div class="box"><b>Offer:</b> {e(v["offer"])}<br><b>Goal:</b> {e(v["goal"])}<br>'
                     f'<b>Hook formula:</b> {e(v["hook_formula"])}<br><b>Length:</b> {total} s · <b>{words} words</b> ≈ {need:.0f} s of voice · {flag}</div>'
                     f'<div class="tl">{tl}</div><div class="shots">{cards}</div><div class="box"><b>Full voice-over:</b> {e(vo)}</div>')
    page = (f'<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Storyboard</title><style>{CSS}</style>'
            f'<div class="w"><h1>Storyboard</h1><p class="mut">{e(str(meta.get("site", "")))} · {e(str(meta.get("format", "")))}</p>{"".join(parts)}</div>')
    open(out, "w", encoding="utf-8").write(page)
    print("wrote", out)


main()
