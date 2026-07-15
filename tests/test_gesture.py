#!/usr/bin/env python3
"""Gesture physics — INV-84 (one gesture → one frame; force scales SPEED not count), INV-85 (the
desktop trackpad pinch drives the zoom, parity with touch; the plain-wheel / ctrl-wheel split), and
INV-86 (the walk and the open zoom survive a device rotation). One test per TEST_MATRIX row, on the
engine's synthetic fixture, in a REAL headless Chrome — a ctrl+wheel is Blink's trackpad-pinch, a
setDeviceMetricsOverride with a screenOrientation is the portrait↔landscape turn.

RED-FIRST: at authoring time the behaviour is NOT built — the wheel handler REFUSES a ctrl+wheel
(`if (e.ctrlKey) { preventDefault(); return; }`) instead of handing it to the zoom, `glideToFrame`
ignores its `velocity` hook so a sharp and a calm gesture glide for the identical time, and the
resize re-dock bails while a glide runs (`if (gliding) return`). The rows below therefore fail on
the current bundle for the RIGHT reason (the behaviour is absent), and go green when it lands.

The glide-SPEED FEEL itself (how a sharp flick should feel against a calm one) stays Alexander's own
eye on a real trackpad — the timing row here is a coarse machine proxy (the sharp glide provably
settles sooner), never the arbiter of feel. Touch momentum + real trackpad cadence + the exit-FLIP's
re-measured source rect live past a desktop headless browser and are named as real-device walks.

Asserts the REAL baked bundle. Chrome absent → pinned expected SKIPs. Run: python tests/test_gesture.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_gesture_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps(json.dumps({"v": VER, "pick": PICK, "shown": 10}))

# INV-84
GLIDE_ROWS = [
    "EX-GLIDE/INV-84 a FIRM desktop wheel burst advances EXACTLY one frame (never two — the "
    "retired two-frame flick allowance)",
    "EX-GLIDE/INV-84 force scales the single glide's SPEED — a sharp burst settles SOONER than a "
    "calm one at the same tempo, each still exactly one frame",
    "EX-GLIDE/INV-84 a firm TOUCH swipe advances exactly one frame (the desktop↔touch parity)",
    "EX-GLIDE/INV-84 one arrow press advances exactly one frame (already guarded, held here)",
]
# INV-85
ZOOM_ROWS = [
    "EX-ZOOM/INV-85 a ctrl+wheel (trackpad pinch-OUT) over a picture OPENS #ex-zoom and scales it "
    "up (1×→>1×, under the 4× clamp)",
    "EX-ZOOM/INV-85 a ctrl+wheel pinch-IN past the ~0.82× dismiss threshold DISMISSES the open zoom",
    "EX-ZOOM/INV-85 a PLAIN wheel (no ctrl) NEVER opens the zoom — it navigates one frame (the split)",
    "EX-ZOOM/INV-85 target resolution — a ctrl+wheel with the pointer OVER a picture opens THAT "
    "picture (its own src)",
]
# INV-86
TURN_ROWS = [
    "EX-GLIDE/INV-86 the docked frame stays centered across a portrait↔landscape rotation (stops "
    "recomputed against the new viewport)",
    "EX-GLIDE/INV-86 a rotation arriving MID-GLIDE docks at the TARGET frame, centered in the new "
    "viewport (never lands on a stale stop)",
    "EX-ZOOM/INV-86 the open zoom survives a rotation and exits cleanly to a centered frame (the "
    "source re-measured under the turn)",
]

# facts that live in real-device physics a desktop headless browser can never see — each closed only
# by a named walk on a real phone / real trackpad, never pretended green here
REAL_DEVICE_FACTS = [
    "the glide-SPEED FEEL of a sharp flick vs a calm swipe on a real trackpad (the machine row here "
    "only proves the sharp glide settles sooner, never how it FEELS — Alexander's meter)",
    "iOS touch momentum carrying the force→speed feel through native scroll-snap (headless has no "
    "momentum to read)",
    "Safari's gesturestart/gesturechange trackpad-pinch path (Blink dispatches no gesture* events; "
    "only the ctrl+wheel equivalent is reachable headless — the Safari path is an eye-check on a real Mac)",
    "the exit-FLIP flying to the freshly RE-MEASURED source rect after a rotation under the open "
    "zoom (a transient animation to a sub-pixel place — the machine row only proves a clean exit)",
]

SECTIONS = "[...document.querySelectorAll('#ex-stage .exh-frame, #ex-stage .exh-fin')]"


def cur(br):
    return br.evaluate(
        "(()=>{const s=%s;return s.findIndex(x=>{const r=x.getBoundingClientRect();"
        "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});})()" % SECTIONS)


def off(br):
    return br.evaluate(
        "(()=>{const s=%s;const f=s.find(x=>{const r=x.getBoundingClientRect();"
        "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});if(!f)return 99999;"
        "const r=f.getBoundingClientRect();"
        "return Math.round((r.top+r.height/2)-innerHeight/2);})()" % SECTIONS)


def stop(br, k):
    return br.evaluate(
        "(()=>{const s=%s;const r=s[%d].getBoundingClientRect();"
        "return Math.round(scrollY+r.top+(r.height-innerHeight)/2);})()" % (SECTIONS, k))


def room(br, base, tempo):
    """a stored walk straight into the room at the given tempo — READY by condition (copied from
    test_glide: four suites share the machine, a hot run stretches Chrome's start)."""
    br.navigate(base + "/")
    br.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.evaluate("sessionStorage.clear()")
    br.reload()
    for _ in range(40):
        br.sleep(0.15)
        if br.evaluate("document.documentElement.classList.contains('ex-walk')"
                       "&&document.querySelectorAll('.exh-frame').length>0"
                       "&&scrollY===0"):
            break
    br.sleep(0.3)


def burst(br, deltas, gap=0.008):
    """a plain trackpad gesture as its real wheel-event burst, on the PAGE's own clock."""
    br.evaluate(
        "(()=>{const ds=%s,gap=%d;ds.forEach((d,i)=>setTimeout(()=>{"
        "dispatchEvent(new WheelEvent('wheel',{deltaY:d,cancelable:true,bubbles:true}));"
        "},i*gap));})()" % (json.dumps(deltas), int(gap * 1000)))
    br.sleep(len(deltas) * gap + 0.5)


def cwheel(br, deltas, cx, cy, gap=0.012):
    """a ctrl+wheel burst at (cx,cy) — Blink's trackpad-pinch equivalent (INV-85). Dispatched on the
    element under the point so both e.ctrlKey and the pointer target/coords are present, whichever the
    handler reads. deltaY<0 = pinch OUT (zoom in), deltaY>0 = pinch IN (zoom out)."""
    br.evaluate(
        "(()=>{const ds=%s,cx=%d,cy=%d,gap=%d;const el=document.elementFromPoint(cx,cy)"
        "||document.documentElement;ds.forEach((d,i)=>setTimeout(()=>{el.dispatchEvent("
        "new WheelEvent('wheel',{deltaY:d,ctrlKey:true,clientX:cx,clientY:cy,"
        "cancelable:true,bubbles:true}));},i*gap));})()"
        % (json.dumps(deltas), int(cx), int(cy), int(gap * 1000)))
    br.sleep(len(deltas) * gap + 0.35)


def rotate(br, w, h, angle, otype):
    """a portrait↔landscape turn: swap the real viewport metrics (so innerWidth/Height truly change)
    AND raise the orientationchange event INV-86 wants caught as its own beat (not merely a resize)."""
    br._cmd("Emulation.setDeviceMetricsOverride", width=w, height=h,
            deviceScaleFactor=1, mobile=True,
            screenOrientation={"type": otype, "angle": angle})
    br.width, br.height = w, h
    br.evaluate("window.dispatchEvent(new Event('orientationchange'))")
    br.sleep(0.5)


def img_center(br, selector):
    """viewport-centre (x,y) of the first matching in-view picture, or None."""
    box = br.evaluate(
        "(()=>{const e=document.querySelector(%s);if(!e)return null;"
        "const r=e.getBoundingClientRect();if(r.width<1)return null;"
        "return {x:Math.round(r.left+r.width/2),y:Math.round(r.top+r.height/2)};})()"
        % json.dumps(selector))
    return (box["x"], box["y"]) if box else None


ZOPEN = ("(()=>{const z=document.getElementById('ex-zoom');"
         "return !!z&&!z.hidden;})()")
ZSCALE = ("(()=>{const i=document.querySelector('#ex-zoom .exz-img');if(!i)return null;"
          "const m=/scale\\(([0-9.]+)\\)/.exec(i.style.transform||'');"
          "return m?parseFloat(m[1]):1;})()")
ZSRC = ("(()=>{const i=document.querySelector('#ex-zoom .exz-img');"
        "return i?(i.getAttribute('src')||''):'';})()")
NORM = "(u)=>{try{return new URL(u,location.href).href}catch(e){return u}}"

# an in-page settle-timer: dispatch a burst, resolve the ms from first event to the frame landing
SETTLE = """
(ds,goal)=>new Promise(res=>{
  const t0 = performance.now();
  ds.forEach((d,i)=>setTimeout(()=>dispatchEvent(
    new WheelEvent('wheel',{deltaY:d,cancelable:true,bubbles:true})), i*8));
  const iv = setInterval(()=>{
    if (scrollY>2 && Math.abs(scrollY-goal)<=2){ clearInterval(iv); res(Math.round(performance.now()-t0)); }
    else if (performance.now()-t0 > 1800){ clearInterval(iv); res(-1); }
  }, 8);
})
"""

CALM = [2, 4, 9, 18, 34, 52, 38, 22, 12, 6, 3, 2]                 # a gentle swipe (low peak)
SHARP = [120, 320, 500, 540, 420, 240, 120, 60]                  # a hard flick (high peak, fast)


def measure_settle(base, deltas):
    with Browser(width=1280, height=900) as b:
        room(b, base, "1.35")                                    # the default clock (~520ms baseline)
        if b.evaluate("%s.length" % SECTIONS) < 2:               # the walk never booted (no frames)
            return -1, -1, 99999                                 # → a clean FAIL, never a traceback
        goal = stop(b, 1)
        ms = b.evaluate("(%s)(%s,%d)" % (SETTLE, json.dumps(deltas), goal), awaitp=True)
        landed = cur(b)
        return ms, landed, abs(off(b))


if not chrome_available():
    for r in GLIDE_ROWS + ZOOM_ROWS + TURN_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # ---- INV-84 ----------------------------------------------------------------
        # 0 · a FIRM desktop wheel burst = exactly ONE frame (the two-frame flick is retired)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            burst(br, SHARP)
            i1, o1 = cur(br), off(br)
            check(GLIDE_ROWS[0], i1 == 1 and abs(o1) <= 2,
                  f"landed frame {i1} off {o1} (want EXACTLY frame 1, never 2)")

        # 1 · force scales SPEED: the sharp burst settles sooner than the calm one, each ONE frame
        calm_ms, calm_land, calm_off = measure_settle(base, CALM)
        sharp_ms, sharp_land, sharp_off = measure_settle(base, SHARP)
        check(GLIDE_ROWS[1],
              calm_land == 1 and sharp_land == 1 and calm_off <= 2 and sharp_off <= 2
              and calm_ms > 0 and sharp_ms > 0 and (calm_ms - sharp_ms) >= 120,
              f"calm settle={calm_ms}ms (frame {calm_land}) sharp settle={sharp_ms}ms "
              f"(frame {sharp_land}) — want sharp ≥120ms sooner, each frame 1")

        # 2 · a firm TOUCH swipe = one frame (parity)
        with Browser(width=1280, height=900) as br:
            br.touch(True)
            room(br, base, "0.2")
            br.swipe(-380)                                       # a hard, fast swipe up
            t1, to1 = cur(br), off(br)
            check(GLIDE_ROWS[2], t1 == 1 and abs(to1) <= 2,
                  f"swipe→frame {t1} off {to1} (want exactly frame 1)")

        # 3 · one arrow press = one frame
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            br.key("ArrowDown")
            br.sleep(0.5)
            k1, ko1 = cur(br), off(br)
            check(GLIDE_ROWS[3], k1 == 1 and abs(ko1) <= 2,
                  f"arrow→frame {k1} off {ko1} (want exactly frame 1)")

        # ---- INV-85 (desktop trackpad pinch = ctrl+wheel; the split) ----------------
        # 4 · ctrl+wheel pinch-OUT over a walk work opens #ex-zoom and scales it up
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            c = img_center(br, ".exh-frame img.work")
            if not c:
                check(ZOOM_ROWS[0], False, "no in-view work image to pinch")
            else:
                cwheel(br, [-60, -80, -100, -80, -60], c[0], c[1])   # pinch OUT (zoom in)
                br.sleep(0.3)
                opened = br.evaluate(ZOPEN)
                sc = br.evaluate(ZSCALE)
                check(ZOOM_ROWS[0], opened and isinstance(sc, (int, float)) and sc > 1.0,
                      f"opened={opened} scale={sc} (want open, scale>1×)")

        # 5 · ctrl+wheel pinch-IN past the dismiss threshold closes it
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            c = img_center(br, ".exh-frame img.work")
            if not c:
                check(ZOOM_ROWS[1], False, "no in-view work image to pinch")
            else:
                cwheel(br, [-60, -100, -120, -100, -60], c[0], c[1])  # open first
                br.sleep(0.3)
                was_open = br.evaluate(ZOPEN)
                cwheel(br, [80, 140, 200, 260, 320], c[0], c[1])      # pinch IN hard, past dismiss
                br.sleep(0.5)
                gone = not br.evaluate(ZOPEN)
                check(ZOOM_ROWS[1], was_open and gone,
                      f"opened_first={was_open} dismissed={gone} (want open, then gone)")

        # 6 · a PLAIN wheel never opens the zoom — it navigates one frame (the split fence)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            c = img_center(br, ".exh-frame img.work")
            cx, cy = c if c else (640, 450)
            burst(br, [400], gap=0.008)                          # a single plain wheel notch
            br.sleep(0.4)
            zoomed = br.evaluate(ZOPEN)
            stepped = cur(br)
            check(ZOOM_ROWS[2], (not zoomed) and stepped == 1,
                  f"zoom_open={zoomed} (want False) walk_frame={stepped} (want 1 — it navigated)")

        # 7 · target resolution — the picture UNDER the pointer opens (its own src)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            sel = ".exh-frame img.work"
            c = img_center(br, sel)
            want_src = br.evaluate("(()=>{const e=document.querySelector(%s);"
                                   "return e?(e.getAttribute('src')||''):'';})()" % json.dumps(sel))
            if not c:
                check(ZOOM_ROWS[3], False, "no in-view work image to target")
            else:
                cwheel(br, [-60, -100, -80], c[0], c[1])
                br.sleep(0.3)
                opened = br.evaluate(ZOPEN)
                got = br.evaluate(ZSRC) or ""
                same = bool(got) and br.evaluate("(%s)(%s)===(%s)(%s)"
                                                 % (NORM, json.dumps(got), NORM, json.dumps(want_src)))
                check(ZOOM_ROWS[3], opened and same,
                      f"opened={opened} src_match={same} (want the pointed picture's own src)")

        # ---- INV-86 (the walk & the open zoom survive a rotation) -------------------
        # 8 · the docked frame stays centered across a portrait↔landscape turn
        with Browser(width=390, height=844) as br:                # phone, portrait
            br.touch(True)
            room(br, base, "0.2")
            br.swipe(-300)                                        # rest on frame 1
            f_before, o_before = cur(br), off(br)
            rotate(br, 844, 390, 90, "landscapePrimary")          # → landscape
            f_after, o_after = cur(br), off(br)
            check(TURN_ROWS[0],
                  f_before == 1 and abs(o_before) <= 3 and f_after == 1 and abs(o_after) <= 3,
                  f"before frame {f_before} off {o_before} → after frame {f_after} off {o_after} "
                  f"(want frame 1 centered ≤3 both sides of the turn)")

        # 9 · a rotation arriving MID-GLIDE docks at the TARGET frame, centered in the new viewport
        with Browser(width=390, height=844) as br:
            br.touch(True)
            room(br, base, "2.0")                                 # a long clock → a samplable flight
            target_k = 1
            br.key("ArrowDown")                                   # launch a glide toward frame 1
            br.sleep(0.14)                                        # in flight
            in_flight = br.evaluate("scrollY") > 2 and cur(br) != 1
            rotate(br, 844, 390, 90, "landscapePrimary")          # rotate mid-glide
            br.sleep(0.9)                                         # let any settle finish
            f_land, o_land = cur(br), off(br)
            check(TURN_ROWS[1],
                  f_land == target_k and abs(o_land) <= 3,
                  f"in_flight_at_rotate={in_flight} landed frame {f_land} off {o_land} "
                  f"(want frame 1 centered ≤3 in the NEW viewport — not a stale stop)")

        # 10 · the open zoom survives a rotation and exits cleanly to a centered frame
        with Browser(width=390, height=844) as br:
            br.touch(True)
            room(br, base, "0.2")
            br.swipe(-300)                                        # rest on frame 1
            c = img_center(br, ".exh-frame img.work")
            if not c:
                check(TURN_ROWS[2], False, "no in-view work image to open")
            else:
                # open the zoom the touch way (the desktop path is INV-85 above) via a two-finger pinch
                br.evaluate(
                    "(()=>{const e=document.querySelector('.exh-frame img.work');if(!e)return;"
                    "const mk=(id,x,y)=>new Touch({identifier:id,target:e,clientX:x,clientY:y});"
                    "const r=e.getBoundingClientRect(),cx=r.left+r.width/2,cy=r.top+r.height/2;"
                    "e.dispatchEvent(new TouchEvent('touchstart',{touches:[mk(1,cx-20,cy),mk(2,cx+20,cy)],"
                    "targetTouches:[mk(1,cx-20,cy),mk(2,cx+20,cy)],changedTouches:[mk(1,cx-20,cy),mk(2,cx+20,cy)],"
                    "bubbles:true,cancelable:true}));"
                    "e.dispatchEvent(new TouchEvent('touchmove',{touches:[mk(1,cx-70,cy),mk(2,cx+70,cy)],"
                    "targetTouches:[mk(1,cx-70,cy),mk(2,cx+70,cy)],changedTouches:[mk(1,cx-70,cy),mk(2,cx+70,cy)],"
                    "bubbles:true,cancelable:true}));})()")
                br.sleep(0.3)
                open_before = br.evaluate(ZOPEN)
                rotate(br, 844, 390, 90, "landscapePrimary")      # rotate with the zoom standing
                open_after = br.evaluate(ZOPEN)
                # exit — the × / history; then the underlying frame must sit centered in the new viewport
                br.evaluate("var b=document.querySelector('#ex-zoom .exz-close'); if(b) b.click();")
                br.sleep(0.5)
                closed = not br.evaluate(ZOPEN)
                f_end, o_end = cur(br), off(br)
                check(TURN_ROWS[2],
                      open_before and open_after and closed and abs(o_end) <= 3,
                      f"open_before={open_before} open_after_turn={open_after} closed={closed} "
                      f"exit frame {f_end} off {o_end} (want survive the turn, exit centered ≤3)")

        print("\n-- real-device boundary (closed only by a named walk on a real phone / trackpad / Safari):")
        for f in REAL_DEVICE_FACTS:
            print("   [REAL-DEVICE] " + f)

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
