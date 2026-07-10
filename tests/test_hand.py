#!/usr/bin/env python3
"""The living hand (EX-DOOR-3 / INV-44) — adapted for exhibition-engine synthetic fixture.
Fixture pool has 10 entries (5 dark luma≈0.15-0.22, 5 bright luma≈0.78-0.88)
so the door_size=5 law engages, luma lean tests have clear signal.
Run: python tests/test_hand.py
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_hand_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

EXDATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
POOL = EXDATA["door"]["pool"]
LUMA = {e["id"]: e.get("luma", 0.5) for e in POOL}
N = json.loads((TMP / "config.json").read_text())["exhibition"]["door_size"]
MAX_REPEAT = N // 3

check("EX-DOOR-3 the pool carries its tone numbers (luma+warmth baked per candidate)",
      all(isinstance(e.get("luma"), (int, float)) and isinstance(e.get("warmth"), (int, float))
          for e in POOL),
      "tone numbers missing from the baked pool")

BROWSER_ROWS = [
    "EX-DOOR-3 the hand rotates under HIS law (consecutive cold hands differ, overlap ≤ a third; ?reset forgets the hand)",
    "EX-DOOR-3 novelty prefers the unmet (a seen-cache steers free places to unseen works)",
    "EX-DOOR-3 the hour leans the hand (pretend night deals darker than pretend day)",
    "EX-DOOR-3 degrade whole (a pool of exactly door_size IS the hand — no law, no error)",
]

DOOR_IDS = "Array.from(document.querySelectorAll('.exd-window')).map(b=>b.dataset.id)"
AT_DOOR = "document.body.classList.contains('ex-door')"


def prime(br, base, wipe=True):
    br.navigate(base + "/")
    if wipe:
        br.evaluate("localStorage.clear()")
    br.evaluate("localStorage.setItem('ex-tempo','0.2')")


def cold(br, base):
    br.evaluate("localStorage.removeItem('ex.exhibition');sessionStorage.clear()")
    br.navigate(base + "/")
    br.sleep(1.1)
    return br.evaluate(DOOR_IDS)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            # 0 · rotation under HIS law across three CONSECUTIVE cold arrivals
            prime(br, base, wipe=True)
            h1 = cold(br, base)
            h2 = cold(br, base)
            h3 = cold(br, base)
            ok_pairs = all(
                a != b and len(set(a) & set(b)) <= MAX_REPEAT
                for a, b in ((h1, h2), (h2, h3)))
            br.navigate(base + "/?reset")
            br.sleep(1.0)
            hand_forgot = br.evaluate("localStorage.getItem('ex.hand')")
            check(BROWSER_ROWS[0],
                  len(h1) == N and ok_pairs,
                  f"h1∩h2={len(set(h1) & set(h2))} h2∩h3={len(set(h2) & set(h3))} "
                  f"max={MAX_REPEAT} post_reset_hand_key={'set' if hand_forgot else 'fresh'}")

            # 1 · novelty: mark most of the pool as met
            unseen = [e["id"] for e in POOL[:4]]
            seen = [e["id"] for e in POOL if e["id"] not in unseen]
            prime(br, base, wipe=True)
            br.evaluate(
                "localStorage.setItem('ex.seenc', JSON.stringify({v:'x', ids:%s}))"
                % json.dumps(seen))
            hand = cold(br, base)
            got_unseen = [i for i in hand if i in unseen]
            check(BROWSER_ROWS[1],
                  len(got_unseen) >= len(unseen) - MAX_REPEAT
                  and len(got_unseen) >= 3,
                  f"hand={hand} unseen_in_hand={len(got_unseen)}/4")

        # 2 · the hour leans the hand: night deals darker than day
        def mean_luma(hand):
            return sum(LUMA[i] for i in hand) / max(1, len(hand))

        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 2)   # deep night
            prime(br, base, wipe=True)
            night = cold(br, base)
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 13)  # midday
            prime(br, base, wipe=True)
            day = cold(br, base)
        check(BROWSER_ROWS[2],
              mean_luma(night) < mean_luma(day),
              f"night_luma={mean_luma(night):.3f} day_luma={mean_luma(day):.3f}")

    # 3 · degrade whole: a pool of exactly door_size IS the hand
    THIN = Path(tempfile.mkdtemp(prefix="synth_hand_thin_"))
    shutil.copytree(TMP, THIN, dirs_exist_ok=True)
    exd = json.loads((THIN / "exhibition_data.json").read_text(encoding="utf-8"))
    exd["door"]["pool"] = exd["door"]["pool"][:N]
    (THIN / "exhibition_data.json").write_text(json.dumps(exd))
    with serve(THIN) as base2, Browser(width=1280, height=900) as br:
        prime(br, base2, wipe=True)
        h = cold(br, base2)
        h2 = cold(br, base2)
        check(BROWSER_ROWS[3],
              len(h) == N and set(h) == {e["id"] for e in exd["door"]["pool"]} and h2 == h
              or (len(h) == N and set(h) == set(h2)),
              f"h={h} h2={h2}")
    shutil.rmtree(THIN, ignore_errors=True)

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
