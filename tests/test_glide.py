#!/usr/bin/env python3
"""The amortized scroll (EX-GLIDE / INV-39) — adapted for exhibition-engine synthetic fixture.
Run: python tests/test_glide.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_glide_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps(json.dumps({"v": VER, "pick": PICK, "shown": 10}))

BROWSER_ROWS = [
    "EX-GLIDE the latch is retired (scroll-snap none; no CSS smooth fighting the glide)",
    "EX-GLIDE a pause settles the nearest frame (1.4vh→1vh · 0.4vh→0)",
    "EX-GLIDE the hand always wins (a key mid-glide cancels; the room holds off-grid, stable)",
    "EX-GLIDE rides the clock (collapsed tempo settles fast; default tempo still in flight then)",
    "EX-GLIDE instant roads stay instant (hash arrival + place restore: exact, no drift)",
    "EX-GLIDE touch follows the hand (down 25%→forward; up mirrors; <12% drift settles back; never a pull-back)",
    "EX-GLIDE the settle waits for TRUE stillness (no glide fights a still-moving scroll)",
    "EX-GLIDE keys page by frame (space/↓ glide forward, ↑ back; chained presses ride the goal)",
]


def room(br, base, tempo):
    br.navigate(base + "/")
    br.evaluate(f"localStorage.setItem('tlv.exhibition', {WALK})")
    br.evaluate(f"localStorage.setItem('tlv-tempo','{tempo}')")
    br.evaluate("sessionStorage.clear()")
    br.reload()
    br.sleep(1.2)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            vh = br.evaluate("innerHeight")

            # 0 · the latch is retired
            snap = br.evaluate(
                "getComputedStyle(document.documentElement).scrollSnapType")
            smooth = br.evaluate(
                "getComputedStyle(document.documentElement).scrollBehavior")
            check(BROWSER_ROWS[0], snap == "none" and smooth != "smooth",
                  f"scroll-snap-type={snap!r} scroll-behavior={smooth!r}")

            # 1 · a pause settles the nearest frame
            br.evaluate(f"scrollTo(0, {vh} * 1.4)")
            br.sleep(0.9)
            down_ok = abs(br.evaluate("scrollY") - vh) <= 2
            br.evaluate(f"scrollTo(0, {vh} * 0.4)")
            br.sleep(0.9)
            up_ok = br.evaluate("scrollY") <= 2
            check(BROWSER_ROWS[1], down_ok and up_ok,
                  f"1.4vh→{br.evaluate('scrollY') if not down_ok else vh} "
                  f"0.4vh→{br.evaluate('scrollY')}")

        # 2+3 · the hand wins / collapsed tempo
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")
            vh = br.evaluate("innerHeight")
            br.evaluate(f"scrollTo(0, {vh} * 1.5)")
            br.sleep(0.55)
            in_flight = br.evaluate("scrollY")
            moving = abs(in_flight - vh * 1.5) > 5 and abs(in_flight - vh) > 20
            br.key("Shift")
            br.sleep(0.15)
            held1 = br.evaluate("scrollY")
            br.sleep(0.6)
            held2 = br.evaluate("scrollY")
            off_grid = abs(held2 - round(held2 / vh) * vh) > 20
            check(BROWSER_ROWS[2],
                  moving and abs(held2 - held1) <= 2 and off_grid,
                  f"in_flight={in_flight} held={held1}→{held2} vh={vh} moving={moving}")
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.05")
            vh = br.evaluate("innerHeight")
            br.evaluate(f"scrollTo(0, {vh} * 1.5)")
            br.sleep(0.55)
            fast_settled = abs(br.evaluate("scrollY") - vh) <= 2 \
                or abs(br.evaluate("scrollY") - 2 * vh) <= 2
            check(BROWSER_ROWS[3], fast_settled,
                  f"collapsed@0.55s scrollY={br.evaluate('scrollY')} vh={vh}")

        # 4 · instant roads stay instant
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            shown = br.evaluate(
                "JSON.stringify([...document.querySelectorAll('.exh-frame')].map(f=>f.dataset.id))")
            target = json.loads(shown)[4]
            br.navigate(base + "/#w-" + target)
            br.sleep(0.5)
            top = br.evaluate(
                f"document.querySelector('.exh-frame[data-id=\"{target}\"]').offsetTop")
            at1 = br.evaluate("scrollY")
            br.sleep(1.2)
            at2 = br.evaluate("scrollY")
            hash_ok = abs(at1 - top) <= 2 and at1 == at2
            vh = br.evaluate("innerHeight")
            br.evaluate(
                "document.querySelectorAll('.exh-frame')[2].scrollIntoView({behavior:'instant'})")
            br.sleep(0.8)
            br.reload()
            br.sleep(1.4)
            r1 = br.evaluate("scrollY")
            br.sleep(1.0)
            r2 = br.evaluate("scrollY")
            place_ok = abs(r1 - 2 * vh) <= 2 and r1 == r2
            check(BROWSER_ROWS[4], hash_ok and place_ok,
                  f"hash at={at1}/{at2} top={top} · place {r1}/{r2} want={2*vh}")

        # 5 · touch follows the hand
        with Browser(width=1280, height=900) as br:
            br.touch(True)
            room(br, base, "0.2")
            vh = br.evaluate("innerHeight")
            br.evaluate(f"scrollTo(0, {vh} * 0.6)")
            br.sleep(0.05)
            br.evaluate(f"scrollTo(0, {vh} * 1.25)")
            br.sleep(0.9)
            fwd = br.evaluate("scrollY")
            down_ok = abs(fwd - 2 * vh) <= 2
            br.evaluate(f"scrollTo(0, {vh} * 1.75)")
            br.sleep(0.9)
            up_at = br.evaluate("scrollY")
            up_ok = abs(up_at - vh) <= 2
            br.evaluate(f"scrollTo(0, {vh} * 1.06)")
            br.sleep(0.9)
            drift_ok = abs(br.evaluate("scrollY") - vh) <= 2
            check(BROWSER_ROWS[5], down_ok and up_ok and drift_ok,
                  f"down25%→{fwd} (want {2*vh}) up25%→{up_at} (want {vh}) "
                  f"drift6%→{br.evaluate('scrollY')} (want {vh})")

        # 6 · TRUE stillness
        with Browser(width=1280, height=900) as br:
            br.touch(True)
            room(br, base, "1.35")
            vh = br.evaluate("innerHeight")
            br.evaluate("""
              window.__fight = [];
              (function(){
                let y = 0, i = 0;
                const steps = [120,110,95,80,65,52,40,30,22,15,10,6];
                function put(){
                  if (i >= steps.length) { window.__momentumDone = true; return; }
                  y += steps[i];
                  scrollTo(0, y);
                  const want = y;
                  setTimeout(() => {
                    if (Math.abs(scrollY - want) > 2 && !window.__momentumDone)
                      window.__fight.push([i, Math.round(scrollY), want]);
                  }, 25);
                  i += 1;
                  setTimeout(put, 40 + i * 20);
                }
                put();
              })();
            """)
            br.sleep(1.9)
            fights = json.loads(br.evaluate("JSON.stringify(window.__fight)") or "[]")
            br.sleep(2.6)
            final = br.evaluate("scrollY")
            settled = abs(final - round(final / vh) * vh) <= 2
            check(BROWSER_ROWS[6], not fights and settled,
                  f"mid-motion fights={fights[:3]} final={final} vh={vh} settled={settled}")

        # 7 · keys page by frame
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            vh = br.evaluate("innerHeight")
            br.key("ArrowDown")
            br.sleep(0.6)
            one = br.evaluate("scrollY")
            br.key("ArrowDown")
            br.key("ArrowDown")
            br.sleep(0.8)
            three = br.evaluate("scrollY")
            br.key("ArrowUp")
            br.sleep(0.6)
            back = br.evaluate("scrollY")
            br.key(" ", "Space")
            br.sleep(0.6)
            spaced = br.evaluate("scrollY")
            keys_ok = (abs(one - vh) <= 2 and abs(three - 3 * vh) <= 2
                       and abs(back - 2 * vh) <= 2 and abs(spaced - 3 * vh) <= 2)
            check(BROWSER_ROWS[7], keys_ok,
                  f"↓→{one} (want {vh}) ↓↓→{three} (want {3*vh}) "
                  f"↑→{back} (want {2*vh}) space→{spaced} (want {3*vh})")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
