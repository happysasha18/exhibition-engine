#!/usr/bin/env python3
"""The one-frame walk (EX-GLIDE / INV-39) — one test per contract row, on the engine's synthetic
fixture. The decided motion model (supersedes the old free-inertia settle): every input — an arrow
key, a wheel notch, a touch swipe — makes EXACTLY ONE ideal transition to the adjacent frame. It
always starts and lands smoothly, CENTERED on the target; it never rests between frames and never
floats/drifts afterwards (the felt defect: "stops somewhere, then slowly floats ~1.5s"). Phase 1
ignores force — one fixed sine-in-out curve for every input. Desktop (wheel+keys) is owned by a JS
animator (real CDP wheel events, preventDefault kills native free-scroll). Touch docks under native
momentum via CSS scroll-snap (mandatory + stop:always) — no JS writes the position, so the iOS
jerk-fix holds by construction.
Asserts the REAL baked bundle in a REAL headless Chrome. Chrome absent → pinned expected SKIPs.
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
    "EX-GLIDE one input → one frame (a wheel notch advances exactly one, lands centered; force ignored)",
    "EX-GLIDE always lands centered, no post-drift (settled on a frame top, unchanged 1s+ later)",
    "EX-GLIDE the transition cannot overshoot (monotonic to the target, never past it — sine in-out)",
    "EX-GLIDE a mid-transition input chains one frame (re-targets to the next, lands centered)",
    "EX-GLIDE rides the clock (collapsed tempo lands near-instant; default is still in flight then)",
    "EX-GLIDE keys page by frame (space/↓ forward, ↑ back; chained presses ride the goal)",
    "EX-GLIDE instant roads stay instant (hash + place restore land exact, no drift; the door ignores a wheel)",
    "EX-GLIDE touch docks one work at a time (CSS scroll-snap floor; no JS writes the position — jerk-fix holds)",
]


def room(br, base, tempo):
    """a stored walk straight into the room at the given tempo"""
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
        # 0 · one input → one frame, both directions, always centered (tempo 0.2 → a quick dock)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            vh = br.evaluate("innerHeight")
            br.wheel(delta_y=400)                      # one notch down
            br.sleep(0.45)
            d1 = br.evaluate("scrollY")
            down_ok = abs(d1 - vh) <= 2
            br.wheel(delta_y=-400)                     # one notch up
            br.sleep(0.45)
            u1 = br.evaluate("scrollY")
            up_ok = u1 <= 2
            check(BROWSER_ROWS[0], down_ok and up_ok,
                  f"down→{d1} (want {vh}) up→{u1} (want 0)")

        # 1 · lands centered, then STAYS — no float, no creep, no rest between frames
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            vh = br.evaluate("innerHeight")
            br.wheel(delta_y=400)
            br.sleep(0.5)
            at1 = br.evaluate("scrollY")               # landed
            br.sleep(1.3)
            at2 = br.evaluate("scrollY")               # far past any old "float" window
            check(BROWSER_ROWS[1],
                  abs(at1 - vh) <= 2 and at1 == at2,
                  f"landed={at1} then={at2} (want {vh}, stable)")

        # 2 · the transition provably cannot overshoot (sample the peak through the flight)
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")                     # default clock → a visible, samplable flight
            vh = br.evaluate("innerHeight")
            br.evaluate("window.__mx=0;"
                        "window.__smp=setInterval(()=>{window.__mx=Math.max(window.__mx,scrollY);},8);")
            br.wheel(delta_y=400)
            br.sleep(0.75)                             # past the ~520ms transition
            peak = br.evaluate("clearInterval(window.__smp); window.__mx")
            final = br.evaluate("scrollY")
            check(BROWSER_ROWS[2],
                  peak <= vh + 2 and abs(final - vh) <= 2,
                  f"peak={peak} final={final} target={vh} (peak must not pass target)")

        # 3 · a second input mid-transition chains to the NEXT frame (never re-rounds back)
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")                     # a long clock so the first is still in flight
            vh = br.evaluate("innerHeight")
            br.wheel(delta_y=400)                      # heading to frame 1
            br.sleep(0.16)                             # in flight
            mid = br.evaluate("scrollY")
            in_flight = 2 < mid < vh - 20
            br.wheel(delta_y=400)                      # chain → frame 2
            br.sleep(0.9)
            landed = br.evaluate("scrollY")
            check(BROWSER_ROWS[3],
                  in_flight and abs(landed - 2 * vh) <= 2,
                  f"mid={mid} (in flight {in_flight}) landed={landed} (want {2*vh})")

        # 4 · the transition rides the one clock (INV-33): collapsed lands, default still moving
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.05")                     # the collapsed clock (reduced-motion feel)
            vh = br.evaluate("innerHeight")
            br.wheel(delta_y=400)
            br.sleep(0.1)
            collapsed = br.evaluate("scrollY")
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")                     # the default clock (~520ms)
            vh = br.evaluate("innerHeight")
            br.wheel(delta_y=400)
            br.sleep(0.1)                              # same moment the collapsed clock had landed
            deflt = br.evaluate("scrollY")
        check(BROWSER_ROWS[4],
              abs(collapsed - vh) <= 2 and 2 < deflt < vh - 20,
              f"collapsed@0.1s={collapsed} (want {vh}) default@0.1s={deflt} (still in flight)")

        # 5 · keys page by frame (space/arrows step to the next work)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            vh = br.evaluate("innerHeight")
            br.key("ArrowDown")
            br.sleep(0.55)
            one = br.evaluate("scrollY")
            br.key("ArrowDown")                        # two presses chain — the second rides
            br.key("ArrowDown")                        # the first's goal, never re-rounds back
            br.sleep(0.8)
            three = br.evaluate("scrollY")
            br.key("ArrowUp")
            br.sleep(0.55)
            back = br.evaluate("scrollY")
            br.key(" ", "Space")
            br.sleep(0.55)
            spaced = br.evaluate("scrollY")
            keys_ok = (abs(one - vh) <= 2 and abs(three - 3 * vh) <= 2
                       and abs(back - 2 * vh) <= 2 and abs(spaced - 3 * vh) <= 2)
            check(BROWSER_ROWS[5], keys_ok,
                  f"↓→{one} (want {vh}) ↓↓→{three} (want {3*vh}) "
                  f"↑→{back} (want {2*vh}) space→{spaced} (want {3*vh})")

        # 6 · instant roads stay instant: hash arrival exact + no drift; place restore too;
        #     and the cold door ignores a wheel (the animator only owns the walk)
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
            br.sleep(1.2)                              # far past any transition window
            at2 = br.evaluate("scrollY")
            hash_ok = abs(at1 - top) <= 2 and at1 == at2
            # place restore: walk to frame 3, reload — exact and stable
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
        # the cold door ignores a wheel (no step at the door / no ex-walk owner)
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.reload()
            br.sleep(1.0)
            at_door = br.evaluate("document.body.classList.contains('ex-door')")
            br.evaluate("window.__wrote=0;const o=window.scrollTo;"
                        "window.scrollTo=function(){window.__wrote++;return o.apply(this,arguments);};")
            br.wheel(delta_y=400)
            br.sleep(0.4)
            door_quiet = br.evaluate("window.__wrote") == 0
        check(BROWSER_ROWS[6], hash_ok and place_ok and at_door and door_quiet,
              f"hash at={at1}/{at2} top={top} · place {r1}/{r2} want={2*vh} · "
              f"door={at_door} door_wheel_writes={0 if door_quiet else '>0'}")

        # 7 · touch: the CSS scroll-snap floor is present AND no JS ever writes the position
        with Browser(width=1280, height=900) as br:
            br.touch(True)                             # a phone's media (hover:none / coarse)
            room(br, base, "0.2")
            snap = br.evaluate(
                "getComputedStyle(document.documentElement).scrollSnapType")
            frame_css = br.evaluate(
                "(()=>{const f=document.querySelector('.exh-frame');const s=getComputedStyle(f);"
                "return s.scrollSnapAlign+'|'+s.scrollSnapStop;})()")
            # no JS writer on touch: patch scrollTo AFTER load, then a wheel must move nothing via JS
            br.evaluate("window.__wrote=0;const o=window.scrollTo;"
                        "window.scrollTo=function(){window.__wrote++;return o.apply(this,arguments);};")
            br.wheel(delta_y=400)
            br.sleep(0.6)
            wrote = br.evaluate("window.__wrote")
            align, stop = (frame_css.split("|") + [""])[:2]
            check(BROWSER_ROWS[7],
                  snap == "y mandatory" and align == "start" and stop == "always" and wrote == 0,
                  f"snap-type={snap!r} align={align!r} stop={stop!r} js-scroll-writes={wrote}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
