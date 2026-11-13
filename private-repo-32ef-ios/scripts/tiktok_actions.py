#!/usr/bin/env python3
"""TikTok actions for a 428x926 iPhone through WDA (port 8100). Human-like taps and typing.

usage: tiktok_actions.py launch|shot [path]|like|double-tap-like|save|share|comment TEXT|search TEXT|next
Do not run while a farm run is active: a second WDA session kills the farm's session.
Positions come from references/live-learnings.md. Comment, share, search tested. Like and save: see live-learnings.md.
"""
import base64, json, random, subprocess, sys, time, urllib.request

UDID = "00008101-001144A82130001E"
BUNDLE = "com.zhiliaoapp.musically"
WDA = "http://127.0.0.1:8100"
FARM = "http://127.0.0.1:3000"
POS = {"search": (402, 69), "like": (397, 518), "comment": (397, 585),
       "save": (397, 654), "share": (397, 722),
       "composer": (150, 896), "send": (402, 583)}  # composer: sheet just opened. send: keyboard open.


def wda(method, path, body=None):
    # curl, not urllib: WDA truncates responses to urllib's HTTP/1.1 "Connection: close".
    cmd = ["curl", "-s", "-m", "60", "-X", method, WDA + path]
    if body is not None:
        cmd += ["-H", "content-type: application/json", "-d", json.dumps(body)]
    return json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)


def session():
    # The WDA proxy drops some responses (RemoteDisconnected, IncompleteRead). Retry.
    for _ in range(6):
        try:
            return wda("POST", "/session", {"capabilities": {}})["sessionId"]
        except (subprocess.CalledProcessError, ValueError, KeyError):
            time.sleep(4)
    sys.exit("cannot open a WDA session")


def touch(sid, steps):
    wda("POST", f"/session/{sid}/actions", {"actions": [{"type": "pointer", "id": "f",
        "parameters": {"pointerType": "touch"}, "actions": steps}]})


def tap(sid, x, y):
    x += random.gauss(0, 2); y += random.gauss(0, 2)
    touch(sid, [{"type": "pointerMove", "duration": 0, "x": round(x), "y": round(y)}, {"type": "pointerDown", "button": 0},
                {"type": "pause", "duration": random.randint(45, 120)}, {"type": "pointerUp", "button": 0}])
    time.sleep(random.uniform(1.2, 2.4))


def double_tap(sid, x=214, y=463):
    """Like by double tap on the video. The heart burst shows inside the screenshot crop."""
    step = [{"type": "pointerMove", "duration": 0, "x": x, "y": y}, {"type": "pointerDown", "button": 0},
            {"type": "pause", "duration": random.randint(40, 80)}, {"type": "pointerUp", "button": 0},
            {"type": "pause", "duration": random.randint(70, 130)}]
    touch(sid, step + step[1:] + [step[0]][:0])
    time.sleep(0.4)


def type_text(sid, text):
    for ch in text:
        wda("POST", f"/session/{sid}/wda/keys", {"value": [ch]})
        time.sleep(max(0.04, random.lognormvariate(-2.3, 0.5)))  # about 100 ms median, rare long gaps


def shot(path="/tmp/tt.png"):
    # The farm API pads the cropped image. Raw WDA /screenshot often returns a truncated body.
    for _ in range(4):
        try:
            data = urllib.request.urlopen(FARM + f"/api/devices/{UDID}/remote/screenshot", timeout=30).read()
            if data[:4] == b"\x89PNG":
                open(path, "wb").write(data)
                return print(path)
        except OSError:
            pass
        time.sleep(3)
    sys.exit("no screenshot")


def launch():
    subprocess.run(["xcrun", "devicectl", "device", "process", "launch", "--device", UDID,
                    "--terminate-existing", BUNDLE], check=True, capture_output=True)
    time.sleep(7)


def main(argv):
    cmd, arg = argv[0], " ".join(argv[1:])
    if cmd == "launch": return launch()
    if cmd == "shot": return shot(arg or "/tmp/tt.png")
    sid = session()
    if cmd in ("like", "save", "share"): tap(sid, *POS[cmd])
    elif cmd == "double-tap-like": double_tap(sid)
    elif cmd == "search":
        tap(sid, *POS["search"]); tap(sid, 150, 69); type_text(sid, arg); type_text(sid, "\n")
    elif cmd == "comment":
        tap(sid, *POS["comment"]); tap(sid, *POS["composer"]); type_text(sid, arg); tap(sid, *POS["send"])
    elif cmd == "next":
        touch(sid, [{"type": "pointerMove", "duration": 0, "x": 130, "y": 700}, {"type": "pointerDown", "button": 0},
                    {"type": "pointerMove", "duration": 380, "x": 136, "y": 200}, {"type": "pointerUp", "button": 0}])
    else: sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:] or ["help"])
