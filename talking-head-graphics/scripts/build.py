#!/usr/bin/env python3
"""build.py [OUT_DIR] -> index.html. Paper-cut minimal explainer over a talking head.
Rules: ONE visual at a time; the speaker morphs into a rounded panel (right or left quarter, no border) while a visual plays;
one accent colour; real logos on ink tiles; paper cards with soft shadow; text may sit behind the speaker (cutout)."""
import sys, math, random

import os, subprocess
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
        S(t, "whoosh", 0.22)
        cur = st


# ---- one visual at a time: items live in the content area beside the panel ----
def poly(w, h, inset, amp, seed, step=44):
    r = random.Random(seed); pts = []
    def edge(x0, y0, x1, y1):
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / step))
        for i in range(n):
            t = i / n
            pts.append((x0 + (x1 - x0) * t + r.uniform(-amp, amp), y0 + (y1 - y0) * t + r.uniform(-amp, amp)))
    edge(inset, inset, w - inset, inset); edge(w - inset, inset, w - inset, h - inset); edge(w - inset, h - inset, inset, h - inset); edge(inset, h - inset, inset, inset)
    return "polygon(" + ",".join(f"{x:.0f}px {y:.0f}px" for x, y in pts) + ")"


def sheet(id, a, b, color, seed, exit_, dark):
    _n[0] += 1; d = 1 if _n[0] % 2 else -1
    r = random.Random(seed)
    ht = f'<div class="ht" style="{"left:110px;bottom:120px" if seed % 2 else "right:110px;top:120px"};background-image:radial-gradient(circle,rgba({255 if dark else 0},{255 if dark else 0},{255 if dark else 0},.16) 34%,transparent 36%)"></div>'
    tapes = "".join(f'<div class="tape" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)"></div>' for x, y, rot in [(r.randint(80, 220), 22, r.randint(-14, -4)), (r.randint(1560, 1700), 1012, r.randint(-12, 10))])
    html = f'<div class="sheet" id="{id}-sh"><div class="so" style="clip-path:{poly(1920, 1080, 38, 7, seed)}"></div><div class="si" style="background:{color};clip-path:{poly(1920, 1080, 54, 6, seed + 5)}">{ht}</div>{tapes}</div>'
    clip(id + "-sc", a - 0.12, b + (0.7 if exit_ else 0.5), html, z=0)
    J(f'tl.fromTo("#{id}-sh",{{x:{d * 1950},rotation:{d * 3}}},{{x:0,rotation:{[-0.4, 0.5][seed % 2]},duration:.85,ease:"expo.out"}},{a - 0.12:.2f});')
    if exit_:
        J(f'tl.to("#{id}-sh",{{x:{-d * 1950},duration:.6,ease:"power3.in"}},{b:.2f});')
    S(a - 0.1, "whoosh", 0.2)


CFG = {"m1": "blue", "so1": "light", "so2": "light", "c1": ("blue", 1), "t1": "light", "t2": "char", "t3": ("blue", 1), "be1": "light", "be2": "blue", "g0": "char",
       "g1": "light", "g2": "blue", "g3": "light", "g4": "blue", "g5": ("light", 1), "cl": "blue", "us": "light", "np": ("blue", 1), "ve": "light", "di": ("char", 1), "ca": ("blue", 1)}


def _dk(on):
    global TXT, MUT
    TXT, MUT = ("#FFFFFF", "#CFCFCF") if on else (INK, MID)


def item(id, side, a, b, html, rot=0.0):
    side = "R"
    c = CFG[id]; color, exit_ = (c, 0) if isinstance(c, str) else c
    dark = color == "char"
    sheet(id, a, b, SHEETS[color], len(id) * 7 + int(a * 3), exit_, dark)
    html = html if not dark else html
    cx = PANEL[side]["cx"]
    clip(id, a, b, f'<div class="stage" style="left:{cx - 560}px">{html}</div>', z=4)
    d = min(0.75, max(0.2, (b - a) - 0.6))
    J(f'tl.fromTo("#{id} .stage > *",{{opacity:0,y:40,rotation:{rot - 2.5}}},{{opacity:1,y:0,rotation:{rot},duration:{d:.2f},ease:"power3.out",stagger:{0.12 if d > 0.5 else 0},}},{a + 0.05:.2f});')
    J(f'tl.to("#{id} .stage",{{opacity:0,y:-26,duration:.3,ease:"power2.in"}},{b - 0.32:.2f});')
    S(a + 0.1, "tick", 0.3)


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


SEQ = [(6.1, "R"), (22.45, "full"), (26.25, "R"), (49.05, "full"), (52.0, "R"), (69.8, "full"), (78.85, "R"), (98.55, "full")]
# ================= TIMELINE =================
# opening: name tag, text behind speaker
clip("s0", 0.3, 5.7, f'<div class="nt"><b>Name</b><span>Intro · Role</span></div>', z=4)
J('tl.fromTo("#s0 .nt",{opacity:0,y:30},{opacity:1,y:0,duration:.7,ease:"power3.out"},0.6);'); J('tl.to("#s0 .nt",{opacity:0,duration:.3},5.3);')


def behind(id, t0, t1, inner):
    """Text between the video and a cutout of the speaker. The speaker must be full frame for the whole window."""
    import re
    if not re.fullmatch(r"[a-z0-9_-]+", id):
        sys.exit(f"build: window id {id!r} must match [a-z0-9_-]+")
    past = [(t, st) for t, st in SEQ if t <= t0 + 0.01]
    if past and past[-1][1] != "full":
        sys.exit(f"build: window {id} starts at {t0}s while the speaker is in the panel; move it after a return to full frame")
    if past:
        t0 = max(t0, past[-1][0] + 0.7)
    nxt = [t for t, st in SEQ if t > t0 + 0.01]
    if nxt and t1 > nxt[0]:
        sys.exit(f"build: window {id} ({t0}-{t1}s) runs into the panel morph at {nxt[0]}s")
    t1 = min(t1, DUR)
    if t0 >= t1:
        return
    WINDOWS.append((id, t0, t1))
    clip(id + "-bt", t0, t1, inner, z=2)
    els.append(f'<video id="{id}-pv" class="clip person" data-start="{t0:.2f}" data-duration="{(t1 - t0):.2f}" data-media-start="0" data-track-index="{tr()}" src="assets/person-{id}.webm" muted playsinline data-layout-allow-occlusion></video>')
    for e in (f"#{id}-bt", f"#{id}-pv"):
        J(f'tl.to("{e}",{{opacity:0,duration:.25,ease:"power2.in"}},{t1 - 0.25:.2f});')


behind("b1", 3.3, 6.0, f'<div class="bt" style="top:330px"><span id="b1w" style="color:{INK}">COMPANY</span></div>')
J('tl.fromTo("#b1w",{opacity:0,y:60,scale:1.06},{opacity:1,y:0,scale:1,duration:.9,ease:"expo.out"},3.45);'); S(3.45, "whoosh_big", 0.25)

# 1 a logo tile
item("m1", "R", 6.5, 12.2, tile("logo-a", 380), -1.5)
# 2 title, then a mock window
item("so1", "R", 12.5, 16.4, big("Role title<br>here", 120))
item("so2", "R", 16.5, 18.6, card(f'<div class="dots"><i></i><i></i><i></i><b style="margin-left:14px;font-size:30px;color:#6E6E73">Previous Co</b></div><div class="blk" style="width:100%;height:46px"></div><div class="blk" style="width:58%;height:120px;margin-top:18px"></div>', 760, 40), -1.2)
# 3 30K -> 80K: one continuous line, one accent
chart = ('<div class="num" id="c-n" style="font-size:250px">20K</div>'
         f'<svg width="1000" height="300" viewBox="0 0 1000 300" style="margin-top:20px;overflow:visible"><path id="c-p" d="M20 270 C250 262 420 240 560 170 S840 40 980 22" pathLength="1" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"/>'
         f'<circle id="c-d0" cx="20" cy="270" r="12" fill="{INK}"/><text id="c-l0" x="20" y="320" font-family="Inter" font-weight="700" font-size="34" fill="#6E6E73" text-anchor="start">20K</text><circle id="c-d1" cx="980" cy="22" r="16" fill="{ACC}" style="filter:drop-shadow(0 0 14px {ACC})"/></svg>'
         )
item("c1", "R", 18.7, 22.4, chart)
J('tl.fromTo("#c-d0",{opacity:0,scale:.2,transformOrigin:"50% 50%"},{opacity:1,scale:1,duration:.4,ease:"back.out(2)"},18.9);')
J('tl.fromTo("#c-d1",{opacity:0,scale:.2,transformOrigin:"50% 50%"},{opacity:0,scale:.2,duration:.01},18.9);')
J('tl.fromTo("#c-l0",{opacity:0},{opacity:1,duration:.4},18.95);')
J('tl.fromTo("#c-p",{strokeDashoffset:1},{strokeDashoffset:0,duration:1.1,ease:"power2.inOut"},19.4);')
J('(()=>{const o={v:20};tl.to(o,{v:80,duration:1.1,ease:"power2.inOut",onUpdate:()=>{document.getElementById("c-n").textContent=Math.round(o.v)+"K"}},19.4);})();')
J('tl.fromTo("#c-d1",{opacity:0,scale:.2},{opacity:1,scale:1,duration:.4,ease:"back.out(2.4)"},20.4);'); S(19.4, "rise", 0.2); S(20.45, "win", 0.22)

# 4 growth: text behind the speaker
behind("b2", 22.6, 26.2, f'<div class="bt" style="top:340px"><span id="b2w" style="color:{INK}">GROWTH</span></div>')
J('tl.fromTo("#b2w",{opacity:0,y:60,scale:1.06},{opacity:1,y:0,scale:1,duration:.9,ease:"expo.out"},23.25);'); S(23.25, "whoosh_big", 0.25)

# 5 tactics (L): phones -> GEO/AEO -> grey hat, one at a time
item("t1", "L", 26.6, 28.6, pic("phones", 700), -1)
(_dk(1), item("t2", "L", 28.7, 31.4, big("GEO", 220) + big("AEO", 220, ACC)), _dk(0))
item("t3", "L", 31.5, 34.4, pic("hat", 620), 1.5)

# 6 Studio Name (R)
item("be1", "R", 34.55, 38.7, pic("rocket", 620))
item("be2", "R", 38.8, 41.3, card(big("Studio Name", 190), 880, 70), -1)
# 7 what Studio Name gives (R): one icon at a time
(_dk(1), item("g0", "R", 41.45, 43.7, big("Pre-seed", 140) + f'<div class="arrow" style="background:#fff"></div>' + big("Seed", 140, ACC)), _dk(0))
for i, (n, lab, a, b) in enumerate([("coins", "Funding", 43.8, 45.2), ("mentor", "Mentorship", 45.25, 46.25), ("gift", "Perks", 46.3, 47.35), ("hack", "Hackathons", 47.4, 48.45), ("stage", "Events", 48.5, 49.1)]):
    item(f"g{i + 1}", "R", a, b, pic(n, 560))

# 8 token maxer: behind the speaker
behind("b3", 49.2, 52.0, f'<div class="bt" style="top:350px;font-size:210px"><span id="b3a" style="color:{INK}">BIG</span> <span id="b3b" style="color:{ACC}">IDEA</span></div>')
J('tl.fromTo("#b3a",{opacity:0,y:50},{opacity:1,y:0,duration:.7,ease:"expo.out"},50.6);'); J('tl.fromTo("#b3b",{opacity:0,y:50},{opacity:1,y:0,duration:.7,ease:"expo.out"},51.1);'); S(50.6, "whoosh_big", 0.25); S(51.1, "coin", 0.3)

# 9 Claude subscriptions (L)
fan = "".join(f'<div class="tile" style="position:absolute;left:{i * 165}px;top:{(i % 2) * 36}px;width:230px;height:230px;transform:rotate({[-6, 3, -2, 5][i]}deg)"><img src="assets/logos/logo-c.svg" style="width:128px;height:128px"></div>' for i in range(4))
item("cl", "L", 52.2, 55.4, f'<div style="position:relative;width:850px;height:290px">{fan}</div>')
# 10 users (L)
item("us", "L", 55.7, 59.9, big("10,000s", 240) + pic("crowd", 520))
# 11 npm (L)
item("np", "L", 60.1, 69.7, f'<div style="display:flex;gap:60px;align-items:center">{tile("logo-b", 240)}<div><div class="num" id="n-n" style="font-size:260px">0</div></div></div>')
J('(()=>{const o={v:0};tl.to(o,{v:100,duration:1.5,ease:"power2.out",onUpdate:()=>{document.getElementById("n-n").textContent="~"+Math.round(o.v)+"K"}},63.4);})();'); S(63.4, "rise", 0.2)

# 13 venn (R)
venn = (f'<svg width="860" height="640" viewBox="0 0 860 640"><g fill="rgba(232,85,47,.10)" stroke="{INK}" stroke-width="5"><circle id="v1" cx="300" cy="230" r="200"/><circle id="v2" cx="560" cy="230" r="200"/><circle id="v3" cx="430" cy="430" r="200"/></g>'
        f'<g font-family="Inter" font-weight="800" font-size="40" fill="{INK}" text-anchor="middle"><text id="v1t" x="220" y="200">Product</text><text id="v2t" x="640" y="200">Business</text><text id="v3t" x="430" y="520">Growth</text></g></svg>')
item("ve", "R", 79.1, 84.1, venn)
for k, t in (("v1", 79.7), ("v2", 80.4), ("v3", 81.0)):
    J(f'tl.fromTo("#{k}",{{opacity:0,scale:.6,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:.6,ease:"back.out(1.6)"}},{t});'); J(f'tl.fromTo("#{k}t",{{opacity:0}},{{opacity:1,duration:.4}},{t + 0.25});')
# 14 Company (R)
item("di", "R", 84.4, 90.9, card(big("Company", 200), 860, 70), -1)
# 15 calendar (L)
item("ca", "L", 91.3, 98.5, tile("logo-d", 340), -1)

# morph sequence (explicit, so every beat has the right side)
states(SEQ)
open(os.path.join(OUT, "windows.txt"), "w").write("".join(f"{i} {a:.2f} {b:.2f}\n" for i, a, b in WINDOWS))

# ---- audio ----
L = {"whoosh": 0.42, "whoosh_big": 1.2, "pop": 0.26, "coin": 0.39, "rise": 1.2, "tick": 0.07, "win": 1.2}
aud = "".join(f'<audio id="sfx{i}" class="clip" data-start="{t:.2f}" data-duration="{min(L[n], DUR - t):.2f}" data-track-index="{tr()}" src="assets/sfx/{n}.wav" data-volume="{v}"></audio>' for i, (t, n, v) in enumerate(sorted(sfx), 1) if t < DUR - 0.1)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}html,body{width:1920px;height:1080px;overflow:hidden;background:#000}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;font-family:Inter,sans-serif}
#paper{position:absolute;inset:0;z-index:0;background:%PAPER%}
#paper::after{content:"";position:absolute;inset:0;opacity:.5;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' seed='4'/><feColorMatrix values='0 0 0 0 .3  0 0 0 0 .28  0 0 0 0 .24  0 0 0 .09 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
#bw{position:absolute;inset:0;z-index:1;overflow:hidden}#bi{position:absolute;inset:0;transform-origin:960px 540px}#base{position:absolute;left:0;top:0;width:1920px;height:1080px}
.sh{position:absolute;z-index:0;top:90px;height:900px;width:530px;border-radius:40px;opacity:0;box-shadow:0 40px 90px rgba(0,0,0,.28),0 4px 0 rgba(0,0,0,.05)}#shR{left:1330px}#shL{left:60px}
.person{position:absolute;left:0;top:0;width:1920px;height:1080px;z-index:3}
.stage{position:absolute;top:0;width:1120px;height:1080px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;text-align:center}
.big{font-weight:900;letter-spacing:-.045em;line-height:.95}.num{font-weight:900;letter-spacing:-.05em;line-height:.9;color:%INK%}.sub{font-weight:600;letter-spacing:-.01em;line-height:1.15}
.tile{background:%INK%;border-radius:28%;display:flex;align-items:center;justify-content:center;box-shadow:0 30px 60px rgba(0,0,0,.22),0 2px 0 rgba(255,255,255,.08) inset}
.sheet{position:absolute;inset:0;filter:drop-shadow(0 20px 30px rgba(0,0,0,.22))}.so,.si{position:absolute;inset:0}.ht{position:absolute;width:420px;height:300px;background-size:20px 20px;-webkit-mask-image:radial-gradient(ellipse at 50% 50%,#000 10%,transparent 70%)}.tape{position:absolute;width:170px;height:46px;background:rgba(240,228,176,.78);box-shadow:0 2px 6px rgba(0,0,0,.18);clip-path:polygon(0 10%,4% 0,8% 12%,12% 0,16% 10%,100% 10%,96% 100%,92% 88%,88% 100%,84% 90%,0 90%)}.paper{position:relative;border-radius:14px}.pb{position:absolute;inset:0;background:%CARD%;border-radius:10px;box-shadow:0 2px 0 rgba(0,0,0,.05),0 36px 70px rgba(0,0,0,.16);filter:url(#rough)}.pc{position:relative;display:flex;flex-direction:column;align-items:center;gap:22px}
.pic{filter:drop-shadow(0 26px 30px rgba(0,0,0,.2))}.arrow{width:6px;height:70px;background:%INK%;border-radius:3px}
.dots{display:flex;gap:10px;width:100%}.dots i{width:16px;height:16px;border-radius:50%;background:#cfcac0}.blk{background:#e4dfd4;border-radius:10px}
.nt{position:absolute;left:64px;top:900px;display:flex;flex-direction:column;gap:4px;color:#fff;text-shadow:0 2px 6px rgba(0,0,0,.55),0 4px 24px rgba(0,0,0,.45)}.nt b{font-size:64px;font-weight:900;letter-spacing:-.03em}.nt span{font-size:36px;font-weight:700}
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
