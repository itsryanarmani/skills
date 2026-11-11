#!/usr/bin/env python3
"""Aggregate landing-page teardown JSON files. Standard library only.

  python3 -I aggregate_teardowns.py <json_dir> [--csv out.csv]   full report
  python3 -I aggregate_teardowns.py --table teardown-summary.csv  recheck from CSV

One screen = 1500 px of screenshot height. Income claims are a keyword
heuristic (see income_claim), not a reading of the page.
"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
from statistics import median

COLS = ["slug", "funnel_type", "screens", "first_screen_words", "total_words",
        "cta_count", "person_in_hero", "nav", "urgency", "price_shown"]
MONEY = re.compile(r"[$₹£€]|\bgbp\b|crore|\bcr\b|figure", re.I)
OUTCOME = re.compile(r"revenue|income|sales|earn|figure|pipeline|crore|\bcr\b|/month|per month|in \d+ days", re.I)
FREE = re.compile(r"[\s(]*(?:\$0|0|100% free|free|no cost|complimentary)(?![\w.,])")
CAP = 23040  # screenshot height limit of the capture tool
GAPS =re.compile(r"blank|empty|did not render|cut off|capped|not loaded|half-loaded", re.I)


def income_claim(d):
    """True if a shown number mixes money with an outcome word, or the page's
    own do-not-copy list names income, revenue or earnings."""
    nums = d["proof"].get("numbers_shown", [])
    hit = any(MONEY.search(n) and OUTCOME.search(n) for n in nums)
    return hit or bool(re.search(r"income|revenue|earning", " ".join(d["do_not_steal"]), re.I))


def price_shown(d):
    """The JSON flag counts a bare 'free' on some pages and not on others
    (batch notes differ). Here a free offer is 0, even with a struck-through
    or 'value' price; a free first step with a paid tier is 1."""
    o = d["offer"]
    text = (o.get("price_text") or "").strip().lower()
    free_only = FREE.match(text) and not re.search(r"vip|monthly|subscri", text)
    return int(bool(o["price_shown"]) and not free_only)


def row(d):
    h, t = d["hero"], d["totals"]
    return {"slug": d["slug"], "funnel_type": d["funnel_type"],
            "screens": round(d["image"]["height"] / 1500, 1),
            "first_screen_words": h["first_screen_words"], "total_words": t["approx_words"],
            "cta_count": t["cta_buttons"], "person_in_hero": int(h["person_in_hero"]),
            "nav": int(h["nav_present"]), "urgency": int(d["urgency"]["present"]),
            "price_shown": price_shown(d)}


def share(rows, key):
    return f"{sum(int(r[key]) for r in rows)}/{len(rows)}"


def med(rows, key):
    return median(float(r[key]) for r in rows)


def table_report(rows):
    print(f"pages: {len(rows)}")
    types = Counter(r["funnel_type"] for r in rows)
    print("\nfunnel_type counts:", dict(types.most_common()))
    print("\nper funnel type (n | median screens, first-screen words, total words, CTAs | "
          "person, nav, urgency, price)")
    for ft, n in types.most_common():
        g = [r for r in rows if r["funnel_type"] == ft]
        print(f"{ft:22} n={n:<3} {med(g,'screens'):5.1f} {med(g,'first_screen_words'):6.0f} "
              f"{med(g,'total_words'):6.0f} {med(g,'cta_count'):4.1f} | {share(g,'person_in_hero')} "
              f"{share(g,'nav')} {share(g,'urgency')} {share(g,'price_shown')}")
    print(f"{'ALL':22} n={len(rows):<3} {med(rows,'screens'):5.1f} {med(rows,'first_screen_words'):6.0f} "
          f"{med(rows,'total_words'):6.0f} {med(rows,'cta_count'):4.1f} | {share(rows,'person_in_hero')} "
          f"{share(rows,'nav')} {share(rows,'urgency')} {share(rows,'price_shown')}")


def order_of(d):
    seq = [s["type"] for s in sorted(d["sections"], key=lambda s: s["order"]) if s["type"] != "other"]
    return [t for i, t in enumerate(seq) if i == 0 or t != seq[i - 1]]


def json_report(docs):
    by = defaultdict(list)
    for d in docs:
        by[d["funnel_type"]].append(d)
    print("\nper funnel type (median form fields in first screen | testimonials | anchoring | "
          "guarantee | income claim)")
    for ft, g in sorted(by.items(), key=lambda kv: -len(kv[1])):
        ff = median(d["hero"]["form_fields_in_first_screen"] for d in g)
        k = lambda f: f"{sum(1 for d in g if f(d))}/{len(g)}"
        print(f"{ft:22} n={len(g):<3} {ff:3.0f} | {k(lambda d: d['totals']['testimonials'] > 0)} "
              f"{k(lambda d: d['offer']['anchoring'])} {k(lambda d: d['offer']['guarantee'])} "
              f"{k(income_claim)}")
    allk = lambda f: f"{sum(1 for d in docs if f(d))}/{len(docs)}"
    print("\nALL pages: person in hero", allk(lambda d: d["hero"]["person_in_hero"]),
          "| nav", allk(lambda d: d["hero"]["nav_present"]),
          "| testimonials", allk(lambda d: d["totals"]["testimonials"] > 0),
          "| urgency", allk(lambda d: d["urgency"]["present"]),
          "| price shown", allk(price_shown),
          "| anchoring", allk(lambda d: d["offer"]["anchoring"]),
          "| guarantee", allk(lambda d: d["offer"]["guarantee"]),
          "| income claim (heuristic)", allk(income_claim),
          "| capture gaps (heuristic)", allk(lambda d: GAPS.search(d["limits"])),
          f"| capped at {CAP} px", allk(lambda d: d["image"]["height"] == CAP))
    print("urgency types:", dict(Counter(t for d in docs for t in d["urgency"]["types"]).most_common()))
    pres = Counter(t for d in docs for t in {s["type"] for s in d["sections"]})
    print("pages with section type:", dict(pres.most_common()))
    scr = lambda d: d["image"]["height"] / 1500
    short = [d for d in docs if scr(d) <= 2.2]
    paid = [d for d in docs if price_shown(d)]
    print(f"short pages (<=2.2 screens): {len(short)}, with testimonials "
          f"{sum(1 for d in short if d['totals']['testimonials'] > 0)}, with a nav "
          f"{sum(1 for d in short if d['hero']['nav_present'])}")
    print(f"median screens: price shown {median(scr(d) for d in paid):.1f} (n={len(paid)}), "
          f"no price {median(scr(d) for d in docs if d not in paid):.1f} (n={len(docs) - len(paid)})")
    print("form field in first screen:", allk(lambda d: d["hero"]["form_fields_in_first_screen"] > 0),
          "| video on page", allk(lambda d: d["totals"]["videos"] > 0),
          "| first-screen CTA count median",
          median(d["hero"]["cta_buttons_in_first_screen"] for d in docs),
          "| proof types", dict(Counter(t for d in docs for t in d["proof"]["types"]).most_common()))
    print("\nsection order per funnel type with n>=4 (modal exact order | consensus order, "
          "types in >=50% of pages by median relative position; 'other' dropped)")
    for ft, g in sorted(by.items(), key=lambda kv: -len(kv[1])):
        if len(g) < 4:
            continue
        orders = Counter(tuple(order_of(d)) for d in g)
        top, c = orders.most_common(1)[0]
        pos = defaultdict(list)
        for d in g:
            o = order_of(d)
            for i, t in enumerate(dict.fromkeys(o)):
                pos[t].append(i / max(len(o) - 1, 1))
        cons = sorted((median(p), t, len(p)) for t, p in pos.items() if len(p) * 2 >= len(g))
        print(f"{ft} (n={len(g)}): exact modal order seen in {c} page(s)")
        print("   consensus: " + " > ".join(f"{t}({n})" for _, t, n in cons))
    lev, first = Counter(), defaultdict(list)
    for d in docs:
        seen = set()
        for rank, p in enumerate(d["psychology"]):
            if p["lever"] not in seen:
                seen.add(p["lever"])
                lev[p["lever"]] += 1
                first[p["lever"]].append((rank, d["slug"], p["evidence"]))
    print("\npsychology levers (pages | best example: page where the lever ranks highest, "
          "ties by slug)")
    for name, n in lev.most_common():
        rank, slug, ev = sorted(first[name])[0]
        print(f"{name:24} {n:3}/{len(docs)} | {slug} (rank {rank + 1}): {ev[:80]}")


def main(argv):
    if len(argv) >= 2 and argv[0] == "--table":
        with open(argv[1], newline="") as f:
            table_report(list(csv.DictReader(f)))
        return
    docs = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(argv[0], "*.json")))]
    rows = [row(d) for d in docs]
    table_report(rows)
    json_report(docs)
    if "--csv" in argv:
        with open(argv[argv.index("--csv") + 1], "w", newline="") as f:
            w = csv.DictWriter(f, COLS, lineterminator="\n")
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: r["slug"]))


if __name__ == "__main__":
    main(sys.argv[1:])
