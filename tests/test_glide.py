#!/usr/bin/env python3
"""The one-frame walk (EX-GLIDE / INV-39) — one test per contract row, on the engine's synthetic
fixture. The decided motion model (supersedes the old free-inertia settle): every input — an arrow
key, a wheel notch, a touch swipe — makes EXACTLY ONE ideal transition to the adjacent frame. It
always starts and lands smoothly, CENTERED on the target; it never rests between frames and never
floats/drifts afterwards. Phase 1 ignores force — one fixed sine-in-out curve for every input.
Desktop (wheel+keys) AND touch are owned by the SAME JS animator.

CENTERED is asserted as MEASURED GEOMETRY, never k×innerHeight arithmetic: on a real phone the
browser chrome makes the live innerHeight smaller than the frames' 100vh, so an arithmetic stop
lands off centre and drifts FURTHER off with every step (his bug 2026-07-09 evening — «картинка
следующая каждый раз съезжает»). The old suite asserted the same arithmetic the code used, so it
was green over the broken phone walk. Every row below reads the landed section's own rect against
the live viewport; rows 8–9 pin the mismatched-viewport case explicitly.
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
    "EX-GLIDE always lands centered, no post-drift (settled centered, unchanged 1s+ later)",
    "EX-GLIDE the transition cannot overshoot (monotonic to the target, never past it — sine in-out)",
    "EX-GLIDE a mid-transition input chains one frame (re-targets to the next, lands centered)",
    "EX-GLIDE rides the clock (collapsed tempo lands near-instant; default is still in flight then)",
    "EX-GLIDE keys page by frame (space/↓ forward, ↑ back; chained presses ride the goal)",
    "EX-GLIDE instant roads land centered (hash + place restore, no drift; the door ignores a wheel)",
    "EX-GLIDE touch docks one work per swipe (a momentum swipe no longer flies through — one JS-driven frame each)",
    "EX-GLIDE frames taller than the live viewport still land CENTERED every step (the phone-chrome "
    "mismatch — measured geometry, no accumulating drift)",
    "EX-GLIDE a viewport-metric change re-centers the resting frame (phone chrome collapses → quiet re-dock)",
    "EX-GLIDE a light trackpad swipe (one ramping burst) advances exactly ONE frame — never several",
    "EX-GLIDE a deliberate second swipe over the first's decaying tail still steps (never eaten)",
]

# facts this suite CANNOT close — they live in real-device physics a headless desktop never has;
# each is closed only by a named walk on a real phone (the honest boundary, not pretended coverage)
REAL_DEVICE_FACTS = [
    "iOS touch momentum + scroll-snap interplay (the swipe fly-through was invisible headless)",
    "browser-chrome viewport dance on real scroll (rows 8-9 EMULATE the metric, not the dance)",
    "background-tab timer throttling (the 2.5s failsafe black screen)",
    "trackpad hardware event cadence (row 10 replays a recorded shape, not a finger)",
]

# the walk's sections in order (frames + the closing screen) — the stops the animator owes
SECTIONS = "[...document.querySelectorAll('#ex-stage .exh-frame, #ex-stage .exh-fin')]"


def cur(br):
    """index of the section holding the viewport's centre line — the frame the eye is on"""
    return br.evaluate(
        "(()=>{const s=%s;return s.findIndex(x=>{const r=x.getBoundingClientRect();"
        "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});})()" % SECTIONS)


def off(br):
    """the landed section's centre offset from the LIVE viewport centre, px — 0 = truly centered"""
    return br.evaluate(
        "(()=>{const s=%s;const f=s.find(x=>{const r=x.getBoundingClientRect();"
        "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});if(!f)return 99999;"
        "const r=f.getBoundingClientRect();"
        "return Math.round((r.top+r.height/2)-innerHeight/2);})()" % SECTIONS)


def stop(br, k):
    """section k's own centered stop, measured off its rect — the position a landing owes"""
    return br.evaluate(
        "(()=>{const s=%s;const r=s[%d].getBoundingClientRect();"
        "return Math.round(scrollY+r.top+(r.height-innerHeight)/2);})()" % (SECTIONS, k))


MISMATCH = ("const st=document.createElement('style');st.id='mm';"
            "st.textContent='#ex-stage .exh-frame,#ex-stage .exh-fin{height:calc(100vh + 72px)}';"
            "document.head.appendChild(st)")


def burst(br, deltas, gap=0.016):
    """a trackpad gesture as the wheel-event burst it really is — ramp-in, peak, decaying tail.
    Dispatched on the PAGE's own clock (setTimeout), never test-runner sleeps: a real trackpad
    ticks at device cadence, and a loaded runner stretching a python sleep past the 150ms idle
    window would split one gesture into two — a harness artifact, not a product fact."""
    br.evaluate(
        "(()=>{const ds=%s,gap=%d;ds.forEach((d,i)=>setTimeout(()=>{"
        "dispatchEvent(new WheelEvent('wheel',{deltaY:d,cancelable:true,bubbles:true}));"
        "},i*gap));})()" % (json.dumps(deltas), int(gap * 1000)))
    br.sleep(len(deltas) * gap + 0.25)


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
            br.wheel(delta_y=400)                      # one notch down
            br.sleep(0.45)
            d_i, d_off = cur(br), off(br)
            br.wheel(delta_y=-400)                     # one notch up
            br.sleep(0.45)
            u_i, u_off = cur(br), off(br)
            check(BROWSER_ROWS[0],
                  d_i == 1 and abs(d_off) <= 2 and u_i == 0 and abs(u_off) <= 2,
                  f"down→frame {d_i} off {d_off} (want 1, ≤2) up→frame {u_i} off {u_off} (want 0, ≤2)")

        # 1 · lands centered, then STAYS — no float, no creep, no rest between frames
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            br.wheel(delta_y=400)
            br.sleep(0.5)
            o1 = off(br)
            at1 = br.evaluate("scrollY")               # landed
            br.sleep(1.3)
            at2 = br.evaluate("scrollY")               # far past any old "float" window
            check(BROWSER_ROWS[1],
                  cur(br) == 1 and abs(o1) <= 2 and at1 == at2,
                  f"landed frame {cur(br)} off {o1} scrollY {at1}→{at2} (want centered, stable)")

        # 2 · the transition provably cannot overshoot (sample the peak through the flight)
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")                     # default clock → a visible, samplable flight
            goal = stop(br, 1)
            br.evaluate("window.__mx=0;"
                        "window.__smp=setInterval(()=>{window.__mx=Math.max(window.__mx,scrollY);},8);")
            br.wheel(delta_y=400)
            br.sleep(0.75)                             # past the ~520ms transition
            peak = br.evaluate("clearInterval(window.__smp); window.__mx")
            final = br.evaluate("scrollY")
            check(BROWSER_ROWS[2],
                  peak <= goal + 2 and abs(final - goal) <= 2,
                  f"peak={peak} final={final} target={goal} (peak must not pass target)")

        # 3 · a second input mid-transition chains to the NEXT frame (never re-rounds back)
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")                     # a long clock so the first is still in flight
            g1, g2 = stop(br, 1), stop(br, 2)
            br.wheel(delta_y=400)                      # heading to frame 1
            br.sleep(0.16)                             # in flight
            mid = br.evaluate("scrollY")
            in_flight = 2 < mid < g1 - 20
            br.wheel(delta_y=400)                      # chain → frame 2
            br.sleep(0.9)
            landed = br.evaluate("scrollY")
            check(BROWSER_ROWS[3],
                  in_flight and abs(landed - g2) <= 2,
                  f"mid={mid} (in flight {in_flight}) landed={landed} (want {g2})")

        # 4 · the transition rides the one clock (INV-33): collapsed lands, default still moving
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.05")                     # the collapsed clock (reduced-motion feel)
            g1 = stop(br, 1)
            br.wheel(delta_y=400)
            br.sleep(0.1)
            collapsed = br.evaluate("scrollY")
        with Browser(width=1280, height=900) as br:
            room(br, base, "1.35")                     # the default clock (~520ms)
            h1 = stop(br, 1)
            br.wheel(delta_y=400)
            br.sleep(0.1)                              # same moment the collapsed clock had landed
            deflt = br.evaluate("scrollY")
        check(BROWSER_ROWS[4],
              abs(collapsed - g1) <= 2 and 2 < deflt < h1 - 20,
              f"collapsed@0.1s={collapsed} (want {g1}) default@0.1s={deflt} (still in flight)")

        # 5 · keys page by frame (his 2026-07-07 word: space/arrows step to the next work)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            br.key("ArrowDown")
            br.sleep(0.55)
            one, o_one = cur(br), off(br)
            br.key("ArrowDown")                        # two presses chain — the second rides
            br.key("ArrowDown")                        # the first's goal, never re-rounds back
            br.sleep(0.8)
            three, o_three = cur(br), off(br)
            br.key("ArrowUp")
            br.sleep(0.55)
            back, o_back = cur(br), off(br)
            br.key(" ", "Space")
            br.sleep(0.55)
            spaced, o_sp = cur(br), off(br)
            keys_ok = ((one, three, back, spaced) == (1, 3, 2, 3)
                       and max(abs(o_one), abs(o_three), abs(o_back), abs(o_sp)) <= 2)
            check(BROWSER_ROWS[5], keys_ok,
                  f"↓→{one}/{o_one} ↓↓→{three}/{o_three} ↑→{back}/{o_back} space→{spaced}/{o_sp} "
                  f"(want frames 1,3,2,3 all centered ≤2)")

        # 6 · instant roads land centered: hash arrival + place restore, exact and stable;
        #     and the cold door ignores a wheel (the animator only owns the walk)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            shown = br.evaluate(
                "JSON.stringify([...document.querySelectorAll('.exh-frame')].map(f=>f.dataset.id))")
            target = json.loads(shown)[4]
            br.navigate(base + "/#w-" + target)
            br.sleep(0.5)
            on_target = br.evaluate(
                "(()=>{const s=%s;const f=s.find(x=>{const r=x.getBoundingClientRect();"
                "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});"
                "return f&&f.dataset.id==='%s';})()" % (SECTIONS, target))
            h_off = off(br)
            at1 = br.evaluate("scrollY")
            br.sleep(1.2)                              # far past any transition window
            at2 = br.evaluate("scrollY")
            hash_ok = on_target and abs(h_off) <= 2 and at1 == at2
            # place restore: walk to frame 3, reload — centered on it, and stable
            br.evaluate(
                "document.querySelectorAll('.exh-frame')[2].scrollIntoView({behavior:'instant'})")
            br.sleep(0.8)
            br.reload()
            br.sleep(1.4)
            p_i, p_off = cur(br), off(br)
            r1 = br.evaluate("scrollY")
            br.sleep(1.0)
            r2 = br.evaluate("scrollY")
            place_ok = p_i == 2 and abs(p_off) <= 2 and r1 == r2
        # the cold door ignores a wheel (G3: no step at the door / no ex-walk owner)
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
              f"hash on_target={on_target} off={h_off} scrollY {at1}/{at2} · "
              f"place frame {p_i} off {p_off} scrollY {r1}/{r2} · "
              f"door={at_door} door_wheel_writes={0 if door_quiet else '>0'}")

        # 7 · touch: ONE swipe → exactly ONE framed transition, both directions, and a tap-sized
        #     nudge moves nothing (his phone bug — a momentum swipe used to fly through several works)
        with Browser(width=1280, height=900) as br:
            br.touch(True)                             # a phone's media (hover:none / coarse)
            room(br, base, "0.2")
            br.swipe(-300)                             # a firm swipe up → forward exactly one frame
            f1, of1 = cur(br), off(br)
            br.swipe(-300)                             # a second swipe → exactly one more, never several
            f2, of2 = cur(br), off(br)
            br.swipe(300)                              # swipe down → back one frame
            back, ob = cur(br), off(br)
            pos = br.evaluate("scrollY")
            br.swipe(-10)                              # a tap-sized nudge (below the swipe floor) does nothing
            nudge = br.evaluate("scrollY")
            one_each = ((f1, f2, back) == (1, 2, 1)
                        and max(abs(of1), abs(of2), abs(ob)) <= 2 and nudge == pos)
            check(BROWSER_ROWS[7], one_each,
                  f"swipe→{f1}/{of1} swipe→{f2}/{of2} back→{back}/{ob} "
                  f"(want frames 1,2,1 centered ≤2) nudge {pos}→{nudge} (no move)")

        # 8 · THE PHONE GEOMETRY (his 2026-07-09 bug): the frames' CSS height is BIGGER than the
        #     live viewport (100vh vs a chrome-shrunk innerHeight) — every landing must still put
        #     the section's centre on the viewport's centre, with NO accumulating per-step drift.
        ok8, det8 = True, []
        for extra in (72, 36):                         # two chrome geometries (letter: ≥2 sizes)
            with Browser(width=1280, height=900) as br:
                br.touch(True)
                room(br, base, "0.2")
                br.evaluate(MISMATCH.replace("72px", f"{extra}px"))  # frames = innerHeight+extra
                br.sleep(0.2)
                frames, offs = [], []
                for _ in range(5):                     # ≥5 advances — drift is cumulative
                    br.swipe(-300)
                    frames.append(cur(br))
                    offs.append(off(br))
                ok8 = ok8 and frames == [1, 2, 3, 4, 5] and all(abs(o) <= 3 for o in offs)
                det8.append(f"+{extra}px: frames {frames} offsets {offs}")
        check(BROWSER_ROWS[8], ok8, " · ".join(det8) + " (want 1..5, each ≤3px)")

        # 9 · the viewport metric CHANGES while the walk rests (phone chrome collapses / a window
        #     resize) — the walk quietly re-docks the resting frame to the new centre, no jump cut.
        with Browser(width=1280, height=900) as br:
            br.touch(True)
            room(br, base, "0.2")
            br.swipe(-300)                             # rest centered on frame 1
            before = off(br)
            br.evaluate(MISMATCH + ";dispatchEvent(new Event('resize'))")
            br.sleep(0.8)                              # the debounced re-dock + its short glide
            after = off(br)
            check(BROWSER_ROWS[9],
                  abs(before) <= 2 and cur(br) == 1 and abs(after) <= 3,
                  f"before={before} after metric change off={after} (want re-centered ≤3, frame 1)")

        # 10 · a LIGHT trackpad swipe is one RAMPING burst of small deltas (the instance bug 2026-07-09:
        #      one light trackpad swipe flew through half the gallery): the gesture's own ramp-in must
        #      never re-arm the step — one burst, one frame, landed centered.
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            burst(br, [2, 4, 9, 18, 34, 52, 38, 22, 12, 6, 3, 2])
            br.sleep(0.8)
            i1, o1 = cur(br), off(br)
            check(BROWSER_ROWS[10], i1 == 1 and abs(o1) <= 2,
                  f"landed frame {i1} off {o1} (want exactly frame 1, centered ≤2)")

        # 11 · the dropped-swipe protection SURVIVES the ramp fix: a REAL second swipe — a sharp
        #      rise over the first's STILL-FLOWING decaying tail (one continuous event stream,
        #      human-paced ~700ms in), must still step. One stream, never split by dead gaps —
        #      a gap longer than the idle window would end the gesture and test nothing.
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            burst(br, [3, 8, 20, 44, 60, 41]                       # swipe 1: ramp + peak
                      + [30, 26, 22, 18, 15, 12, 10, 8, 7, 6,      # its momentum tail flows on
                         5, 5, 4, 4, 3, 3]
                      + [26, 48, 70, 45],                          # swipe 2: a sharp rise, ~700ms in
                  gap=0.03)
            br.sleep(0.9)
            i2, o2 = cur(br), off(br)
            check(BROWSER_ROWS[11], i2 == 2 and abs(o2) <= 2,
                  f"landed frame {i2} off {o2} (want frame 2 — swipe 2 must not be eaten)")

        print("\n-- real-device boundary (closed only by a named walk on a real phone, never headless):")
        for f in REAL_DEVICE_FACTS:
            print("   [REAL-DEVICE] " + f)

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
