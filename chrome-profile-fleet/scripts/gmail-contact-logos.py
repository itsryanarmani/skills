#!/usr/bin/env python3
"""Give each sending address a logo in your own Gmail, using Google Contacts photos.

Gmail shows a contact's photo in place of the letter avatar. This script builds
one contact per address and sets the photo from the site's own favicon. When a
domain has no usable favicon, it draws a simple symbolic mark instead.

Only YOU see these photos. A recipient's Gmail ignores your contacts. For
recipients you need BIMI with a paid Common Mark Certificate, or a Google
Account that owns the address and has a profile photo.

Needs:
  - GOOGLE_ACCESS_TOKEN  an OAuth access token with the "contacts" scope
  - rsvg-convert         renders SVG (brew install librsvg)
  - Pillow               python3 -m pip install pillow

Usage:
  python3 gmail-contact-logos.py --domains example.com example.org
  python3 gmail-contact-logos.py --domains-file domains.txt --locals hello lily
  python3 gmail-contact-logos.py --domains example.com --dry-run
  python3 gmail-contact-logos.py --domains example.com --logo-dir ./logos

--logo-dir holds optional overrides named <domain>.svg or <domain>.png.
--names takes a JSON file of {"address": "Display Name"}. Without it the display
name is the title-cased domain label for hello@, else the title-cased local part.
Every write is skipped with --dry-run. Rendered PNGs go to --out (default ./logos-out).
"""
import argparse, base64, colorsys, hashlib, io, json, os, re, shutil, subprocess, sys, time
import urllib.error, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (compatible; contact-logo-bot)"}
PEOPLE = "https://people.googleapis.com/v1"
SIZE = 512

# Symbols on a 64x64 canvas, drawn in white on a coloured rounded square.
# The first keyword found in the domain picks the symbol.
GLYPHS = [
    (("daycare", "map", "pin"),
     '<path d="M32 52S16 38 16 26a16 16 0 0 1 32 0c0 12-16 26-16 26z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/><circle cx="32" cy="26" r="5.5" fill="#fff"/>'),
    (("marina", "yacht", "sail", "boat"),
     '<path d="M32 14v30M32 16l14 22H32M32 22L20 38h12M18 46h28l-4 6H22z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'),
    (("cool", "liquid", "water", "drop"),
     '<path d="M32 13c9 11 14 18 14 25a14 14 0 0 1-28 0c0-7 5-14 14-25z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/><path d="M25 40a7 7 0 0 0 7 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>'),
    (("quantum", "atom", "physics"),
     '<g fill="none" stroke="#fff" stroke-width="3"><ellipse cx="32" cy="32" rx="19" ry="8"/><ellipse cx="32" cy="32" rx="19" ry="8" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="19" ry="8" transform="rotate(120 32 32)"/></g><circle cx="32" cy="32" r="4" fill="#fff"/>'),
    (("surrogac", "fertil", "baby", "family", "care", "child"),
     '<path d="M32 50C16 39 14 28 14 24a9 9 0 0 1 18-3 9 9 0 0 1 18 3c0 4-2 15-18 26z" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/>'),
    (("visa", "passport", "golden", "immigr", "travel"),
     '<path d="M32 12l5.6 12 13 1.6-9.6 9 2.6 12.9L32 40.6 20.4 47.5 23 34.6l-9.6-9L26.4 24z" fill="none" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>'),
]
DEFAULT_GLYPH = '<circle cx="32" cy="32" r="13" fill="none" stroke="#fff" stroke-width="3.4"/><circle cx="32" cy="32" r="4.2" fill="#fff"/>'


def die(msg):
    sys.exit(f"error: {msg}")


def http(url, data=None, headers=None, method=None, timeout=20):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.headers, r.read()


def api(method, path, token, body=None):
    for attempt in range(6):
        try:
            _, _, raw = http(f"{PEOPLE}{path}", data=json.dumps(body).encode() if body is not None else None,
                             headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method=method)
            return json.loads(raw or b"{}")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 503):
                time.sleep(5 * (attempt + 1))
                continue
            die(f"{method} {path} -> {e.code} {e.read()[:200].decode('utf-8', 'replace')}")
    die(f"{method} {path} kept failing")


def discover_icon(domain):
    """Return (kind, bytes) for the best icon the site offers, or None."""
    try:
        _, hdr, html = http(f"https://{domain}/", headers=UA)
    except Exception:
        return None
    html = html.decode("utf-8", "replace")
    cands = []
    for tag in re.findall(r"<link[^>]+>", html, re.I):
        if not re.search(r'rel="[^"]*icon[^"]*"', tag, re.I):
            continue
        m = re.search(r'href="([^"]+)"', tag)
        if not m:
            continue
        href = urllib.parse.urljoin(f"https://{domain}/", m.group(1))
        sz = re.search(r'sizes="(\d+)x', tag)
        size = int(sz.group(1)) if sz else 0
        is_svg = ".svg" in href.split("?")[0] or "svg" in tag.lower()
        # SVG first, then the largest raster, apple-touch icons ahead of small favicons.
        score = (3 if is_svg else 0) + (1 if "apple" in tag.lower() else 0) + size / 1000
        cands.append((score, href))
    cands.sort(reverse=True)
    cands.append((0, f"https://{domain}/favicon.ico"))
    for _, href in cands:
        try:
            _, h, body = http(href, headers=UA)
        except Exception:
            continue
        ctype = h.get("Content-Type", "")
        if body[:200].lstrip().startswith(b"<svg") or b"<svg" in body[:400] or "svg" in ctype:
            return "svg", body
        if "image" in ctype or body[:4] in (b"\x89PNG", b"\x00\x00\x01\x00") or body[:3] == b"\xff\xd8\xff":
            return "raster", body
    return None


def monogram(domain):
    """A symbolic mark for a domain with no usable favicon."""
    label = domain.split(".")[0]
    hue = int(hashlib.sha256(domain.encode()).hexdigest()[:6], 16) % 360 / 360
    r, g, b = colorsys.hls_to_rgb(hue, 0.36, 0.55)
    fill = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
    glyph = next((svg for keys, svg in GLYPHS if any(k in label for k in keys)), DEFAULT_GLYPH)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="{label}">'
            f'<rect width="64" height="64" rx="18" fill="{fill}"/>{glyph}</svg>').encode()


def oklch_to_hex(m):
    """rsvg-convert cannot read oklch(); convert each one to an sRGB hex colour."""
    import math
    L, C, H = float(m.group(1)), float(m.group(2)), float(m.group(3))
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    def gamma(x):
        x = max(0.0, min(1.0, x))
        return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return "#%02x%02x%02x" % tuple(round(gamma(x) * 255) for x in rgb)


def to_png(kind, data):
    from PIL import Image
    if kind == "svg":
        if not shutil.which("rsvg-convert"):
            die("rsvg-convert is not installed (brew install librsvg)")
        data = re.sub(rb"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)[^)]*\)",
                      lambda m: oklch_to_hex(type("M", (), {"group": lambda self, i: m.group(i).decode().rstrip("%")})()).encode(), data)
        png = subprocess.run(["rsvg-convert", "-w", str(SIZE), "-h", str(SIZE)], input=data,
                             capture_output=True, check=True).stdout
        im = Image.open(io.BytesIO(png)).convert("RGBA")
    else:
        im = Image.open(io.BytesIO(data)).convert("RGBA")
        im = im.resize((SIZE, SIZE), Image.LANCZOS)
    # Flatten transparency onto a background that keeps the mark visible.
    px = [p for p in im.get_flattened_data() if p[3] > 200] if hasattr(im, "get_flattened_data") else [p for p in im.getdata() if p[3] > 200]
    lum = sum(0.3 * r + 0.59 * g + 0.11 * b for r, g, b, _ in px) / (255 * len(px)) if px else 0
    bg = (31, 41, 55, 255) if lum > 0.8 else (255, 255, 255, 255)
    flat = Image.new("RGBA", im.size, bg)
    flat.alpha_composite(im)
    out = io.BytesIO()
    flat.convert("RGB").save(out, "PNG")
    return out.getvalue()


def logo_for(domain, logo_dir):
    if logo_dir:
        for ext, kind in (("svg", "svg"), ("png", "raster")):
            p = os.path.join(logo_dir, f"{domain}.{ext}")
            if os.path.exists(p):
                return "override", to_png(kind, open(p, "rb").read())
    found = discover_icon(domain)
    if found:
        try:
            return "favicon", to_png(*found)
        except Exception:
            pass
    return "monogram", to_png("svg", monogram(domain))


def load_existing(token):
    by_email, token_next = {}, None
    while True:
        q = "?personFields=names,emailAddresses&pageSize=1000" + (f"&pageToken={token_next}" if token_next else "")
        d = api("GET", f"/people/me/connections{q}", token)
        for p in d.get("connections", []):
            for e in p.get("emailAddresses", []):
                by_email[e["value"].lower()] = p["resourceName"]
        token_next = d.get("nextPageToken")
        if not token_next:
            return by_email


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domains", nargs="*", default=[])
    ap.add_argument("--domains-file")
    ap.add_argument("--locals", nargs="*", default=["hello", "lily", "pooria"])
    ap.add_argument("--names")
    ap.add_argument("--logo-dir")
    ap.add_argument("--out", default="logos-out")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    domains = list(a.domains)
    if a.domains_file:
        domains += [l.strip() for l in open(a.domains_file) if l.strip() and not l.startswith("#")]
    if not domains:
        die("pass --domains or --domains-file")
    token = os.environ.get("GOOGLE_ACCESS_TOKEN")
    if not token and not a.dry_run:
        die("GOOGLE_ACCESS_TOKEN is not set")
    names = json.load(open(a.names)) if a.names else {}
    os.makedirs(a.out, exist_ok=True)
    existing = load_existing(token) if token else {}
    report = []
    for d in domains:
        source, png = logo_for(d, a.logo_dir)
        open(os.path.join(a.out, f"{d}.png"), "wb").write(png)
        for lp in a.locals:
            addr = f"{lp}@{d}"
            label = d.split(".")[0].title()
            name = names.get(addr) or (label if lp == "hello" else lp.title())
            if a.dry_run:
                report.append((addr, source, "dry-run"))
                continue
            rn = existing.get(addr)
            if not rn:
                made = api("POST", "/people:createContact", token,
                           {"names": [{"givenName": name}], "emailAddresses": [{"value": addr}]})
                rn = made["resourceName"]
                existing[addr] = rn
                time.sleep(0.7)
            api("PATCH", f"/{rn}:updateContactPhoto", token,
                {"photoBytes": base64.b64encode(png).decode(), "personFields": "photos"})
            report.append((addr, source, "photo set"))
            time.sleep(0.7)
    for row in report:
        print("\t".join(row))
    json.dump([dict(zip(("address", "source", "result"), r)) for r in report],
              open(os.path.join(a.out, "report.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
