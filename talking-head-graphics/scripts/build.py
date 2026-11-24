#!/usr/bin/env python3
"""build.py [OUT_DIR] -> index.html. Paper-cut minimal explainer over a talking head.
Rules: ONE visual at a time; the speaker morphs into a rounded panel (right or left quarter, no border) while a visual plays;
one accent colour; real logos on ink tiles; paper cards with soft shadow; text may sit behind the speaker (cutout)."""
import sys, math, random

import json, os, re, subprocess
from html.parser import HTMLParser


def ids_in(html):
    """Every id attribute in an HTML string, however it is quoted (id="a", id='a', id=a)."""
    out = []
    class P(HTMLParser):
        def handle_starttag(self, tag, attrs):
            out.extend(v for k, v in attrs if k == "id" and v)
        handle_startendtag = handle_starttag
    P().feed(html)
    return out


RESERVED = {"root", "paper", "shR", "shL", "bw", "bi", "base", "rough", "s0"}   # ids the builder itself writes
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
def _probe():
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(OUT, "assets/base.mp4")], capture_output=True, text=True)
    try:
        d = float(r.stdout.strip())
    except ValueError:
        d = 0.0
    if r.returncode != 0 or not (d > 0 and d < 7200):
        sys.exit(f"build: cannot read the length of {OUT}/assets/base.mp4 (run prep.sh first)")
    return d
DUR = round(_probe(), 2)
WINDOWS = []
INK, PAPER, CARD, MID, ACC = "#151515", "#F2EFE8", "#FBFAF6", "#6E6E73", "#D4623F"
els, js, sfx = [], [], []
TXT, MUT = INK, MID
SHEETS = {"blue": "#B9CAD9", "sage": "#C3CDB4", "clay": "#E2B9A0", "mustard": "#E6CB86", "char": "#2B2B2B", "light": "#F4F0E6"}
_n = [0]
trk = [10]
PANEL = {"R": dict(inset="90px 60px 90px 1330px", tx=635, ty=70, cx=675), "L": dict(inset="90px 1330px 90px 60px", tx=-635, ty=70, cx=1245)}
FULL = "0px 0px 0px 0px"


def tr():
    trk[0] += 1
    return trk[0]


def J(s):
    js.append(s)


def S(t, n, v=0.25):
    sfx.append((max(0.0, t), n, v))


def clip(id, t0, t1, inner, style="", z=4, cls=""):
    t1 = min(t1, DUR)
    if t0 >= t1:
        return
    els.append(f'<div id="{id}" class="clip {cls}" data-start="{t0:.2f}" data-duration="{(t1 - t0):.2f}" data-track-index="{tr()}" style="z-index:{z};{style}">{inner}</div>')


# ---- speaker states: full / R / L (shared-element morph of the video into a rounded panel) ----
def states(seq):
    """seq: [(time, 'full'|'R'|'L')]; each change morphs over 0.65 s."""
    cur = "full"
    for t, st in seq:
        if st == cur:
            continue
        a = PANEL.get(cur); b = PANEL.get(st)
        fi = f"inset({a['inset'] if a else FULL} round {40 if a else 0}px)"
        ti = f"inset({b['inset'] if b else FULL} round {40 if b else 0}px)"
        J(f'tl.fromTo("#bw",{{clipPath:"{fi}"}},{{clipPath:"{ti}",duration:.65,ease:"power3.inOut",immediateRender:false}},{t:.2f});')
        J(f'tl.fromTo("#bi",{{x:{a["tx"] if a else 0},y:{a["ty"] if a else 0},scale:{1.04 if a else 1}}},{{x:{b["tx"] if b else 0},y:{b["ty"] if b else 0},scale:{1.04 if b else 1},duration:.65,ease:"power3.inOut",immediateRender:false}},{t:.2f});')
        for side in ("R", "L"):
            on = 1 if st == side else 0
            if (cur == side) != (st == side):
                J(f'tl.to("#sh{side}",{{opacity:{on},duration:.5,ease:"power2.out"}},{t + 0.1:.2f});')
        cur = st


def poly(w, h, inset, amp, seed, step=44, jit=0.0, v=0):
    r = random.Random(seed); j = random.Random(seed * 31 + v + 1); pts = []
    def edge(x0, y0, x1, y1):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            t = i / n
            pts.append((x0 + (x1 - x0) * t + r.uniform(-amp, amp) + (j.uniform(-jit, jit) if jit else 0), y0 + (y1 - y0) * t + r.uniform(-amp, amp) + (j.uniform(-jit, jit) if jit else 0)))
    edge(inset, inset, w - inset, inset); edge(w - inset, inset, w - inset, h - inset); edge(w - inset, h - inset, inset, h - inset); edge(inset, h - inset, inset, inset)
    return "polygon(" + ",".join(f"{x:.0f}px {y:.0f}px" for x, y in pts) + ")"


def tile(name, size=300):
    return f'<div class="tile" style="width:{size}px;height:{size}px"><img src="assets/logos/{name}.svg" style="width:{int(size * .56)}px;height:{int(size * .56)}px"></div>'


def card(inner, w=900, pad=70):
    return f'<div class="paper" style="width:{w}px;padding:{pad}px"><div class="pb"></div><div class="pc">{inner}</div></div>'


def big(s, size=150, color=INK, extra=""):
    color = TXT if color == INK else color
    return f'<div class="big" style="font-size:{size}px;color:{color};{extra}">{s}</div>'


def sub(s, size=48, color=MID):
    color = TXT if color == INK else (MUT if color == MID else color)
    return f'<div class="sub" style="font-size:{size}px;color:{color}">{s}</div>'


def pic(name, w=520):
    return f'<img class="pic" src="assets/gen/{name}.png" style="width:{w}px">'



# ---- scenes: a background sheet plus the visuals that play on it ----
# One scene change = background sheet + speaker panel together. Then a pause. Then the visuals fade in on the settled sheet.
# Inside a scene only the visuals change, with one effect (fade). Nothing else moves at the same time.
SLIDE, PAUSE, FADE_IN, FADE_OUT, SHEET_OUT, MORPH = 0.85, 0.25, 0.35, 0.25, 0.6, 0.65
SCENES = []
_IDS = set(RESERVED)
SHEET_COLORS = {"blue": "#B9CAD9", "light": "#F4F0E6"}


def scene(sid, color, enter, items, exit_=None):
    """items: [(id, a, b, html)] with the content windows. Checks the pacing rules and writes the clips."""
    assert color in SHEET_COLORS, f"scene {sid}: unknown sheet colour {color!r}"
    assert enter >= 0 and (exit_ is None or exit_ > enter), f"scene {sid}: bad enter/exit times"
    html_ids = [x for it in items for x in ids_in(it[3])]
    for i in [sid, sid + "-sc", sid + "-sh"] + [it[0] for it in items] + html_ids:
        assert i not in _IDS and not re.fullmatch(r"sfx\d+", i), f"duplicate or reserved id {i!r}: every scene, visual and element id must be unique"
        _IDS.add(i)
    for iid, a, b, _ in items:
        assert b <= DUR + 0.01, f"visual {iid} ends at {b}s but the video is {DUR}s long"
    assert exit_ is None or exit_ + MORPH <= DUR + 0.01, f"scene {sid}: the return to full frame ends after the video ({DUR}s)"
    first = items[0][1]
    assert first >= enter + SLIDE + PAUSE - 0.01, f"scene {sid}: first visual at {first}s needs the sheet settled ({enter + SLIDE + PAUSE:.2f}s)"
    if SCENES:
        prev = SCENES[-1]
        assert enter >= prev["items"][-1][2] - 0.01, f"scene {sid}: sheet starts at {enter}s before the last visual of {prev['sid']} ends ({prev['items'][-1][2]}s)"
        assert prev["exit"] is None or enter >= prev["exit"] + MORPH + 0.05 - 0.01, f"scene {sid}: starts {enter - prev['exit']:.2f}s after a return to full frame; the morph takes {MORPH}s, wait {MORPH + 0.05:.2f}s"
    for i, (iid, a, b, html) in enumerate(items):
        assert b - a >= FADE_IN + FADE_OUT + 0.05 - 0.001, f"visual {iid}: {b - a:.2f}s on screen is too short for a fade in and a fade out"
        assert i == 0 or a >= items[i - 1][2] + 0.1 - 0.01, f"visual {iid}: starts before the last one has faded out"
        assert exit_ is None or b <= exit_ - 0.05 + 0.01, f"visual {iid}: still on screen when the sheet leaves"
    SCENES.append({"sid": sid, "color": color, "enter": enter, "items": items, "exit": exit_})


def _emit_scenes():
    n = 0
    for k, sc in enumerate(SCENES):
        n += 1; d = 7 + 11 * n
        end = sc["exit"] + 0.7 if sc["exit"] else (SCENES[k + 1]["enter"] + SLIDE + 0.1 if k + 1 < len(SCENES) else DUR)
        vo = [poly(1920, 1080, 38, 7, d, jit=1.6, v=v) for v in range(3)]; vi = [poly(1920, 1080, 54, 6, d + 5, jit=1.6, v=v) for v in range(3)]
        html = (f'<div class="sheet" id="{sc["sid"]}-sh"><div class="so" style="clip-path:{vo[0]}"></div>'
                f'<div class="si" style="background:{SHEET_COLORS[sc["color"]]};clip-path:{vi[0]}"><div class="tex"></div></div>'
                f'<div class="tape" style="left:{120 + d % 90}px;top:22px;transform:rotate(-8deg)"></div><div class="tape" style="left:{1600 + d % 60}px;top:1012px;transform:rotate(5deg)"></div></div>')
        clip(sc["sid"] + "-sc", sc["enter"], end, html, z=0)
        J(f'(()=>{{const VO={json.dumps(vo)},VI={json.dumps(vi)};for(let k=0;k<{int((end - sc["enter"]) * 12) + 2};k++){{tl.set("#{sc["sid"]}-sh .so",{{clipPath:VO[k%3]}},{sc["enter"]:.3f}+k/12);tl.set("#{sc["sid"]}-sh .si",{{clipPath:VI[k%3]}},{sc["enter"]:.3f}+k/12);}}}})();')   # hand-cut edge boil on a 12 fps grid
        J(f'tl.fromTo("#{sc["sid"]}-sh",{{x:1950,rotation:3}},{{x:0,rotation:-0.3,duration:{SLIDE},ease:"expo.out"}},{sc["enter"]:.2f});')   # always from the right
        S(sc["enter"], "paper", 0.2)
        if sc["exit"]:
            J(f'tl.to("#{sc["sid"]}-sh",{{x:-1950,duration:{SHEET_OUT},ease:"power3.in"}},{sc["exit"]:.2f});')   # always to the left
            S(sc["exit"], "paper", 0.16)
        for iid, a, b, ih in sc["items"]:
            clip(iid, a - 0.05, b, f'<div class="stage">{ih}</div>', z=4)
            J(f'tl.fromTo("#{iid} .stage",{{opacity:0,scale:.97}},{{opacity:1,scale:1,duration:{FADE_IN},ease:"power2.out"}},{a:.2f});')
            J(f'tl.to("#{iid} .stage",{{opacity:0,duration:{FADE_OUT},ease:"power2.in"}},{b - FADE_OUT - 0.05:.2f});')


def compute_seq():
    seq = []
    for sc in SCENES:
        seq.append((sc["enter"], "R"))
        if sc["exit"]:
            seq.append((sc["exit"], "full"))
    return seq


def behind(id, t0, pop, t1, inner):
    """Text between the video and a cutout of the speaker. t0 = cutout start, pop = when the word appears (say it on the spoken word)."""
    import re
    if not re.fullmatch(r"[a-z0-9_-]+", id):
        sys.exit(f"build: window id {id!r} must match [a-z0-9_-]+")
    for i in [id, id + "-bt", id + "-pv"] + ids_in(inner):
        assert i not in _IDS, f"duplicate id {i!r}"
        _IDS.add(i)
    if t1 > DUR + 0.01:
        sys.exit(f"build: window {id} ends at {t1}s but the video is {DUR}s long")
    past = [(t, st) for t, st in SEQ if t <= t0 + 0.01]
    if past and past[-1][1] != "full":
        sys.exit(f"build: window {id} starts at {t0}s while the speaker is in the panel; move it after a return to full frame")
    if past:
        t0 = max(t0, past[-1][0] + 0.7)
        if [(t, st) for t, st in SEQ if t <= t0 + 0.01][-1][1] != "full":
            sys.exit(f"build: window {id} cannot start before the speaker is back at full frame; move it later")
        assert pop >= past[-1][0] + 1.0 - 0.01, f"window {id}: the word appears {pop - past[-1][0]:.2f}s after the morph; wait 1 s so only one thing moves at a time"
    nxt = [t for t, st in SEQ if t > t0 + 0.01]
    if nxt and t1 > nxt[0] - 0.4:
        sys.exit(f"build: window {id} ({t0}-{t1}s) is too close to the next scene change at {nxt[0]}s")
    t1 = min(t1, DUR)
    if t0 >= t1:
        return
    WINDOWS.append((id, t0, t1))
    clip(id + "-bt", t0, t1, inner, z=2)
    els.append(f'<video id="{id}-pv" class="clip person" data-start="{t0:.2f}" data-duration="{(t1 - t0):.2f}" data-media-start="0" data-track-index="{tr()}" src="assets/person-{id}.webm" muted playsinline data-layout-allow-occlusion></video>')
    for e in (f"#{id}-bt", f"#{id}-pv"):
        J(f'tl.to("{e}",{{opacity:0,duration:.25,ease:"power2.in"}},{t1 - 0.25:.2f});')


# ================= TIMELINE (times are seconds in the base video) =================
# opening: just the name, bottom left
clip("s0", 0.3, 5.4, '<div class="nt"><b>Name</b></div>', z=4)
J('tl.fromTo("#s0 .nt",{opacity:0},{opacity:1,duration:.6,ease:"power2.out"},0.6);'); J('tl.to("#s0 .nt",{opacity:0,duration:.4},4.9);')

# 1 logos (blue)
scene("m", "blue", 6.3, [("m1", 7.4, 12.2, '<div style="display:flex;gap:50px;align-items:center">' + tile("logo-a", 330) + tile("logo-e", 330) + '</div>')])
# 2 role, the product, the growth line (light)
chart = (card('<div class="num" id="c-n" style="font-size:210px">20K</div>', 560, 36) +
         f'<svg width="1000" height="300" viewBox="0 0 1000 300" style="margin-top:20px;overflow:visible"><path id="c-p" d="M20 270 C250 262 420 240 560 170 S840 40 980 22" pathLength="1" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
         f'<circle id="c-d0" cx="20" cy="270" r="12" fill="{INK}"/><text x="20" y="320" font-family="Inter" font-weight="700" font-size="34" fill="#6E6E73">20K</text><circle id="c-d1" cx="980" cy="22" r="16" fill="{ACC}" style="filter:drop-shadow(0 0 14px {ACC})"/></svg>')
scene("p", "light", 12.5, [
    ("so1", 13.6, 16.35, card(big("Role title<br>here", 110), 1000, 50)),
    ("so2", 16.6, 18.6, card('<div class="dots"><i></i><i></i><i></i><b style="margin-left:14px;font-size:30px;color:#6E6E73">Previous Co</b></div><div class="blk" style="width:100%;height:46px"></div><div class="blk" style="width:58%;height:120px;margin-top:18px"></div>', 760, 40)),
    ("c1", 18.8, 22.3, chart)], exit_=22.35)
J('tl.fromTo("#c-d1",{opacity:0,scale:.2,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:.4,ease:"back.out(2.4)"},20.4);')
J('tl.fromTo("#c-p",{strokeDashoffset:1},{strokeDashoffset:0,duration:1.1,ease:"power2.inOut"},19.4);')
J('(()=>{const o={v:20};tl.to(o,{v:80,duration:1.1,ease:"power2.inOut",onUpdate:()=>{document.getElementById("c-n").textContent=Math.round(o.v)+"K"}},19.4);})();'); S(19.4, "rise", 0.1)
# 3 tactics (blue)
scene("t", "blue", 26.65, [
    ("t1", 27.8, 28.55, pic("phones", 700)),
    ("t2", 28.7, 31.4, card(big("GEO", 200) + f'<div id="t-aeo">{big("AEO", 200, ACC)}</div>', 640, 50)),
    ("t3", 31.5, 34.3, pic("hat", 620))])
J('tl.fromTo("#t-aeo",{opacity:0},{opacity:1,duration:.35,ease:"power2.out"},29.6);')
# 4 the studio (light)
scene("b", "light", 34.85, [
    ("be1", 36.0, 38.65, pic("rocket", 620)),
    ("be2", 38.85, 41.35, card(big("Studio Name", 190), 880, 70)),
    ("g0", 41.5, 43.75, card(big("Pre-seed", 110) + '<div class="arrow"></div>' + big("Seed", 110, ACC), 560, 44)),
    ("g1", 43.9, 45.2, pic("coins", 560)), ("g2", 45.3, 46.25, pic("mentor", 560)), ("g3", 46.35, 47.35, pic("gift", 560)),
    ("g4", 47.45, 48.45, pic("hack", 560)), ("g5", 48.55, 49.25, pic("stage", 560))], exit_=49.3)
# 5 subscriptions, users, downloads (blue)
fan = "".join(f'<div class="tile" style="position:absolute;left:{i * 165}px;top:{(i % 2) * 36}px;width:230px;height:230px;transform:rotate({[-6, 3, -2, 5][i]}deg)"><img src="assets/logos/logo-c.svg" style="width:128px;height:128px"></div>' for i in range(4))
scene("s", "blue", 52.4, [
    ("cl", 53.5, 55.9, f'<div style="position:relative;width:850px;height:290px">{fan}</div>'),
    ("us", 56.8, 59.9, f'<div id="us-n">{card(big("10,000s", 200), 620, 40)}</div>' + pic("crowd", 520)),
    ("np", 62.2, 69.6, f'<div style="display:flex;gap:60px;align-items:center">{tile("logo-b", 240)}<div class="paper" id="n-n" style="opacity:0;padding:36px 60px"><div class="pb"></div><div class="pc"><div class="num" id="n-t" style="font-size:210px">0</div></div></div></div>')], exit_=69.7)
J('tl.fromTo("#us-n",{opacity:0},{opacity:1,duration:.35},58.1);')
J('tl.fromTo("#n-n",{opacity:0},{opacity:1,duration:.3},63.3);'); J('(()=>{const o={v:0};tl.to(o,{v:100,duration:1.5,ease:"power2.out",onUpdate:()=>{document.getElementById("n-t").textContent="~"+Math.round(o.v)+"K"}},63.4);})();'); S(63.4, "rise", 0.1)
# 6 what I bring, the company (light)
venn = (f'<svg width="860" height="640" viewBox="0 0 860 640"><g fill="rgba(212,98,63,.10)" stroke="{INK}" stroke-width="5"><circle id="v1" cx="300" cy="230" r="200"/><circle id="v2" cx="560" cy="230" r="200"/><circle id="v3" cx="430" cy="430" r="200"/></g>'
        f'<g font-family="Inter" font-weight="800" font-size="40" fill="{INK}" text-anchor="middle"><text id="v1t" x="220" y="200">Product</text><text id="v2t" x="640" y="200">Business</text><text id="v3t" x="430" y="520">Growth</text></g></svg>')
scene("v", "light", 78.55, [("ve", 79.7, 84.15, venn), ("di", 84.7, 90.8, card(big("Company", 200), 860, 70))])
for k, t in (("v1", 79.7), ("v2", 80.4), ("v3", 81.0)):
    J(f'tl.fromTo("#{k}",{{opacity:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.6,ease:"back.out(1.6)"}},{t});'); J(f'tl.fromTo("#{k}t",{{opacity:0}},{{opacity:1,duration:.4}},{t + 0.25});')
# 7 calendar (blue)
scene("k", "blue", 91.3, [("ca", 92.45, 98.3, tile("logo-d", 340))], exit_=98.4)

SEQ = compute_seq()
# big words behind the speaker: the cutout starts after the speaker is back at full frame, the word appears on the spoken word
behind("b2", 24.7, 24.9, 26.2, f'<div class="bt" style="top:340px"><span id="b2w" style="color:{INK}">GROWTH</span></div>')
J('tl.fromTo("#b2w",{opacity:0,y:50,scale:1.05},{opacity:1,y:0,scale:1,duration:.9,ease:"expo.out"},24.9);'); S(24.9, "whoosh_big", 0.12)
behind("b3", 50.4, 50.6, 52.0, f'<div class="bt" style="top:350px;font-size:210px"><span id="b3a" style="color:{INK}">BIG</span> <span id="b3b" style="color:{ACC}">IDEA</span></div>')
J('tl.fromTo("#b3a",{opacity:0,y:50},{opacity:1,y:0,duration:.7,ease:"expo.out"},50.6);'); J('tl.fromTo("#b3b",{opacity:0,y:50},{opacity:1,y:0,duration:.7,ease:"expo.out"},51.1);'); S(51.1, "coin", 0.12)

_emit_scenes()
states(SEQ)
open(os.path.join(OUT, "windows.txt"), "w").write("".join(f"{i} {a:.2f} {b:.2f}\n" for i, a, b in WINDOWS))
import json
open(os.path.join(OUT, "timeline.json"), "w").write(json.dumps({"duration": DUR, "seq": SEQ, "scenes": [{"id": c["sid"], "enter": c["enter"], "exit": c["exit"], "items": [[i[0], i[1], i[2]] for i in c["items"]]} for c in SCENES], "windows": WINDOWS}, indent=1))


# ---- audio ----
L = {"paper": 1.15, "whoosh": 0.42, "whoosh_big": 1.2, "pop": 0.26, "coin": 0.39, "rise": 1.2, "tick": 0.07, "win": 1.2}
aud = "".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.2f}" data-duration="{min(L[n], DUR - t):.2f}" data-track-index="{tr()}" src="assets/sfx/{n}.wav" data-volume="{v}"></audio>' for i, (t, n, v) in enumerate(sorted(sfx), 1) if t < DUR - 0.1)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden;background:#000}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Inter,sans-serif}
#paper{position:absolute;inset:0;z-index:0;background:%PAPER%}
#paper::after{content:"";position:absolute;inset:0;opacity:.5;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='4'/><feColorMatrix values='0 0 0 0 .3  0 0 0 0 .28  0 0 0 0 .24  0 0 0 .09 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
#bw{position:absolute;inset:0;z-index:1;overflow:hidden}#bi{position:absolute;inset:0;transform-origin:960px 540px}#base{position:absolute;left:0;top:0;width:1920px;height:1080px}
.sh{position:absolute;z-index:0;top:90px;height:900px;width:530px;border-radius:40px;opacity:0;box-shadow:0 40px 90px rgba(0,0,0,.28),0 4px 0 rgba(0,0,0,.05)}#shR{left:1330px}#shL{left:60px}
.person{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:3}
.stage{position:absolute;top:0;left:115px;width:1120px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center}
.big{font-weight:900;letter-spacing:-.045em;line-height:.95}.num{font-weight:900;letter-spacing:-.05em;line-height:.9;color:%INK%}.sub{font-weight:600;letter-spacing:-.01em;line-height:1.15}
.tile{background:%INK%;border-radius:28%;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.22),0 2px 0 rgba(255,255,255,.08) inset}
.sheet{position:absolute;inset:0;filter:drop-shadow(0 20px 30px rgba(0,0,0,.22))}.so,.si{position:absolute;inset:0}.tex{position:absolute;inset:0;opacity:.55;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' seed='9'/><feColorMatrix values='0 0 0 0 .25  0 0 0 0 .22  0 0 0 0 .18  0 0 0 .16 0'/></filter><rect width='260' height='260' filter='url(%23n)'/></svg>")}.tape{position:absolute;width:170px;height:46px;background:rgba(240,228,176,.78);box-shadow:0 2px 6px rgba(0,0,0,.18);clip-path:polygon(0 10%,4% 0,8% 12%,12% 0,16% 10%,100% 10%,96% 100%,92% 88%,88% 100%,84% 90%,0 90%)}.paper{position:relative;border-radius:14px}.pb{position:absolute;inset:0;background:%CARD%;border-radius:10px;box-shadow:0 2px 0 rgba(0,0,0,.05),0 36px 70px rgba(0,0,0,.16);filter:url(#rough)}.pc{position:relative;display:flex;flex-direction:column;align-items:center;gap:22px}
.pic{filter:drop-shadow(0 26px 30px rgba(0,0,0,.2))}.arrow{width:6px;height:70px;background:%INK%;border-radius:3px}
.dots{display:flex;gap:10px;width:100%}.dots i{width:16px;height:16px;border-radius:50%;background:#cfcac0}.blk{background:#e4dfd4;border-radius:10px}
.nt{position:absolute;left:64px;top:900px;display:flex;flex-direction:column;gap:4px;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.55),0 4px 24px rgba(0,0,0,.45)}.nt b{font-size:64px;font-weight:900;letter-spacing:-.03em}
.bt{position:absolute;left:0;width:1920px;text-align:center;font-size:330px;font-weight:900;letter-spacing:-.05em;line-height:1}
"""
for k, v in {"%PAPER%": PAPER, "%INK%": INK, "%CARD%": CARD}.items():
    CSS = CSS.replace(k, v)

HTML = f"""<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{CSS}</style></head><body>
<svg width="0" height="0" style="position:absolute"><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="3" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="5"/></filter></svg>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
<div id="paper"></div><div id="shR" class="sh"></div><div id="shL" class="sh"></div>
<div id="bw"><div id="bi"><video id="base" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" src="assets/base.mp4" data-has-audio="true" playsinline></video></div></div>
{chr(10).join(els)}
{aud}
</div>
<script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(js)}
gsap.set("#bw",{{clipPath:"inset(0px 0px 0px 0px round 0px)"}});window.__timelines["main"]=tl;tl.seek(0);</script></body></html>"""
out = sys.argv[1] if len(sys.argv) > 1 else "."
open(f"{out}/index.html", "w").write(HTML)
print("ok", len(els), "elements", len(sfx), "sfx")
