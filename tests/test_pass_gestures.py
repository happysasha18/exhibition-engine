#!/usr/bin/env python3
"""EX-DARKROOM-GESTURES — the darkroom's own gesture recognisers (Requirement 40, unit U6).

pass-hand-gestures.js is a second host-side layer, the same classic-script-plus-namespaced-receiver
shape pass-hand.js ships in (unit U1) — fetched separately, joining `window.__exPassHandGestures`
with one plain object of `{attach, detach, report}`. This unit wires no consumer for it yet (that is
a later lane's own concern), so every row below drives the file directly: a minimal fixture page
loads it, calls `attach(el, instrument, record)` itself, dispatches real Pointer/Touch/Wheel events
on the attached element — Touch objects on `.exh-frame img.work` for the two-finger rows, modeled on
tests/test_gesture.py:466-471; PointerEvents with pointerType:'touch' for the one-contact rows,
modeled on tests/test_a11y.py:968-981 — and reads the result off `report()`.

Root: `~/tlvphotos/SPEC.md` Requirement 40, "Case: The gestures" and "Case: The tuning chart and the
mouse dialect". The crease's own magnet (criterion 5) reads a record shape that already ships:
`structure.regions.line.{x,y}.{at,explains}` and `symmetry.reflection.leftOntoRight.axisX` /
`.topOntoBottom.axisY`, both written by `~/tlvphotos-site/lab/build-workrecords-v1.py` (region line at
:92-112, the reflection axes at :242-245) and served at `/api/pass/records` in production — this
suite hands the same shape straight to `attach()` rather than standing up that wire, since nothing in
this unit fetches it from anywhere.

No clock anywhere in this file either: every gesture below is driven by discrete dispatched samples
(a fixed sequence of points/touches/notches), never by a real elapsed delay, so a rerun reproduces
the same rows exactly.

Run: python tests/test_pass_gestures.py
"""
import json
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


# ---------------------------------------------------------------- bake once, the real build.py road
TMP = Path(tempfile.mkdtemp(prefix="synth_pass_gestures_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

BAKE_ROW = ("EX-DARKROOM-GESTURES the bake serves pass-hand-gestures.js — build.py's own copy tuple "
            "(engine/build.py:995) carries it beside pass-hand.js and pass-composer.js")
_served = TMP / "pass-hand-gestures.js"
check(BAKE_ROW, _served.exists() and _served.read_text(encoding="utf-8").strip() != "",
      f"exists={_served.exists()}")

# A minimal fixture page — this unit wires no consumer of the recogniser into the real walk, so the
# rows below drive it directly: three elements, one per instrument, and the join receiver installed
# BEFORE the classic script runs (the same handoff 01a-pass.js performs for pass-hand.js, done here
# by the test in its stead).
FIXTURE = """<!doctype html><html><head><meta charset="utf-8"><title>gestures</title></head><body>
<script>window.__exPassHandGestures = function (api) { window.__gestures = api; };</script>
<div class="exh-frame" style="position:fixed;left:20px;top:20px;width:300px;height:300px;">
  <img class="work" id="lm" style="width:100%;height:100%;display:block;">
</div>
<div id="kal" style="position:fixed;left:400px;top:20px;width:200px;height:200px;"></div>
<div class="exh-frame" style="position:fixed;left:20px;top:360px;width:300px;height:300px;">
  <img class="work" id="dr" style="width:100%;height:100%;display:block;">
</div>
<script src="pass-hand-gestures.js"></script>
</body></html>"""
(TMP / "gesture-fixture.html").write_text(FIXTURE, encoding="utf-8")

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps(json.dumps({"v": VER, "pick": PICK, "shown": 10}))

ROWS = [
    "R40c5 the crease's own magnet: a crease ending nearer one candidate line than any other lands "
    "exactly on it — the region line when it is nearest, and a tie between two lines broken by the "
    "higher explains",
    "R40c5 a crease drawn on a work whose record carries no line stays exactly where the finger left "
    "it — the planted defect's own target (S-44 «сгиб без магнита»)",
    "R40c4 twirl on kaleidoscope: angular speed moves twist and the circle's radius moves reach, each "
    "monotone in its own input and within the instrument's own declared span",
    "R40c4 pinch on droste: a two-finger spread steps size through its five whole states alone, never "
    "an interpolation",
    "R40c8 the mouse dialect: Shift+wheel is the pinch, a Shift-held drag is the second finger, a "
    "plain drag is the crease — and the walk's own plain wheel still steps one frame, firing no "
    "gesture, while ctrl+wheel still reaches the zoom",
    "R40c6 touch is the first-class driver: a hover carries no operation and no row of this suite "
    "moves focus by script",
    "R40c11 every handle change passes through an envelope — a target far from where a handle stands "
    "is reached over more than one recorded step, and no handle jumps straight to it",
]


# ---------------------------------------------------------------- JS-side helpers
def attach(br, sel, instrument, record):
    return br.evaluate(
        "(function(sel,inst,rec){var el=document.querySelector(sel);"
        "window.__gestures.attach(el,inst,rec);return true;})(%s,%s,%s)"
        % (json.dumps(sel), json.dumps(instrument), json.dumps(record)))


def report(br):
    return json.loads(br.evaluate("JSON.stringify(window.__gestures.report())"))


def changes_for(rep, handle):
    return [c for c in rep["changes"] if c["handle"] == handle]


def pointer_el(br, sel, kind, x, y, opts=None):
    """A PointerEvent dispatched at `sel`'s own target — the pointerdown road (bound on the
    element itself), modeled on tests/test_a11y.py's PointerEvent rows (:968-981)."""
    o = opts or {}
    return br.evaluate(
        "(function(sel,kind,x,y,o){var el=document.querySelector(sel);"
        "el.dispatchEvent(new PointerEvent(kind,{pointerId:1,pointerType:o.pointerType||'touch',"
        "clientX:x,clientY:y,isPrimary:true,bubbles:true,cancelable:true,"
        "shiftKey:!!o.shiftKey,ctrlKey:!!o.ctrlKey}));return true;})(%s,%s,%s,%s,%s)"
        % (json.dumps(sel), json.dumps(kind), x, y, json.dumps(o)))


def pointer_win(br, kind, x, y, opts=None):
    """The pointermove/pointerup road — bound on window, tracking a gesture past the element's
    own bounds exactly as a real drag can."""
    o = opts or {}
    return br.evaluate(
        "(function(kind,x,y,o){window.dispatchEvent(new PointerEvent(kind,{pointerId:1,"
        "pointerType:o.pointerType||'touch',clientX:x,clientY:y,isPrimary:true,bubbles:true,"
        "cancelable:true,shiftKey:!!o.shiftKey,ctrlKey:!!o.ctrlKey}));return true;})(%s,%s,%s,%s)"
        % (json.dumps(kind), x, y, json.dumps(o)))


def drag(br, sel, points, pointer_type="touch", shift=False):
    """One full one-contact gesture: down at points[0], move through the rest, up at the last —
    the single-pointer shape tests/test_a11y.py's long-press rows already use."""
    opts = {"pointerType": pointer_type, "shiftKey": shift}
    pointer_el(br, sel, "pointerdown", points[0][0], points[0][1], opts)
    for (x, y) in points[1:]:
        pointer_win(br, "pointermove", x, y, opts)
    pointer_win(br, "pointerup", points[-1][0], points[-1][1], opts)


def touch_event(br, sel, kind, touches):
    """A real TouchEvent built from Touch objects on the attached element, modeled exactly on
    tests/test_gesture.py:466-471 (the two-finger pinch's own road)."""
    return br.evaluate(
        "(function(sel,kind,raw){var el=document.querySelector(sel);"
        "var list=raw.map(function(t){return new Touch({identifier:t[0],target:el,"
        "clientX:t[1],clientY:t[2]});});"
        "el.dispatchEvent(new TouchEvent(kind,{touches:list,targetTouches:list,changedTouches:list,"
        "bubbles:true,cancelable:true}));return true;})(%s,%s,%s)"
        % (json.dumps(sel), json.dumps(kind), json.dumps(touches)))


def wheel_event(br, sel, delta_y, shift=False, ctrl=False):
    return br.evaluate(
        "(function(sel,dy,sh,ct){var el=document.querySelector(sel);"
        "el.dispatchEvent(new WheelEvent('wheel',{deltaY:dy,shiftKey:sh,ctrlKey:ct,"
        "bubbles:true,cancelable:true}));return true;})(%s,%s,%s,%s)"
        % (json.dumps(sel), delta_y, json.dumps(shift), json.dumps(ctrl)))


def active_is_body(br):
    return br.evaluate("document.activeElement === document.body")


CLOSE = 1e-6


def near(a, b, eps=1e-3):
    return abs(a - b) <= eps


if not chrome_available():
    for r in [BAKE_ROW] + ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/gesture-fixture.html")

            # ---------------------------------------------------- row 1 — the magnet
            REC_A = {"structure": {"regions": {"line": {"x": {"at": 0.7, "explains": 0.6}}}},
                      "symmetry": {"reflection": {"leftOntoRight": {"axisX": 0.3},
                                                   "topOntoBottom": {"axisY": 0.5}}}}
            attach(br, "#lm", "livemirror", REC_A)
            drag(br, "#lm", [(20 + 0.10 * 300, 20 + 0.10 * 300),
                              (20 + 0.72 * 300, 20 + 0.90 * 300)])
            rep_a = report(br)
            wonA = near(rep_a["handles"]["centreX"], 0.7)

            REC_B = {"structure": {"regions": {"line": {
                "x": {"at": 0.6, "explains": 0.3}, "y": {"at": 0.6, "explains": 0.8}}}}}
            attach(br, "#lm", "livemirror", REC_B)
            drag(br, "#lm", [(20 + 0.10 * 300, 20 + 0.10 * 300),
                              (20 + 0.50 * 300, 20 + 0.50 * 300)])
            rep_b = report(br)
            wonB = near(rep_b["handles"]["centreY"], 0.6) and near(rep_b["handles"]["centreX"], 0.5)
            check(ROWS[0], wonA and wonB,
                  f"nearest-over-reflection centreX={rep_a['handles'].get('centreX')} (want 0.7); "
                  f"tie-by-explains centreX={rep_b['handles'].get('centreX')} (want ~0.5) "
                  f"centreY={rep_b['handles'].get('centreY')} (want 0.6)")

            # ---------------------------------------------------- row 2 — no line, no magnet
            REC_C = {"structure": {}}
            attach(br, "#lm", "livemirror", REC_C)
            drag(br, "#lm", [(20 + 0.05 * 300, 20 + 0.05 * 300),
                              (20 + 0.35 * 300, 20 + 0.65 * 300)])
            rep_c = report(br)
            check(ROWS[1],
                  near(rep_c["handles"]["centreX"], 0.35) and near(rep_c["handles"]["centreY"], 0.65),
                  f"handles={rep_c['handles']} (want centreX≈0.35 centreY≈0.65 — the finger's own "
                  f"place, no line in the record to snap to)")

            # ---------------------------------------------------- row 3 — twirl
            def twirl_run(delta_angle, radius, steps=8):
                attach(br, "#kal", "kaleidoscope", None)
                import math
                cx, cy = 400 + 100, 20 + 100  # #kal's own fixed centre (left+half, top+half)
                pts = [(cx + radius * math.cos(delta_angle * i),
                        cy + radius * math.sin(delta_angle * i)) for i in range(steps + 1)]
                drag(br, "#kal", pts, pointer_type="mouse")
                return report(br)["handles"]

            slow_twist = twirl_run(0.05, 60)["twist"]
            fast_twist = twirl_run(0.9, 60)["twist"]
            small_reach = twirl_run(0.3, 15)["reach"]
            big_reach = twirl_run(0.3, 90)["reach"]
            check(ROWS[2],
                  fast_twist > slow_twist and big_reach > small_reach,
                  f"twist: slow={slow_twist} fast={fast_twist} (want fast>slow); "
                  f"reach: small_radius={small_reach} big_radius={big_reach} (want big>small)")

            # ---------------------------------------------------- row 4 — pinch, stepped states
            attach(br, "#dr", "droste", None)
            cx, cy = 20 + 150, 360 + 150  # #dr's own fixed centre
            d = 40.0
            touch_event(br, "#dr", "touchstart",
                        [[1, cx - d / 2, cy], [2, cx + d / 2, cy]])
            sizes = []
            for _ in range(4):
                d *= 1.3  # clears PINCH_STEP_RATIO (1.25) every time — one step per move
                touch_event(br, "#dr", "touchmove",
                            [[1, cx - d / 2, cy], [2, cx + d / 2, cy]])
                sizes.append(report(br)["handles"]["size"])
            touch_event(br, "#dr", "touchend", [])
            rep_d = report(br)
            size_changes = changes_for(rep_d, "size")
            all_integer = all(float(c["to"]).is_integer() for c in size_changes)
            check(ROWS[3],
                  sizes == [5, 6, 6, 6] and all_integer and len(size_changes) == 2,
                  f"sizes after each spread-growth move={sizes} (want [5,6,6,6] — two real steps off "
                  f"a default of 4, clamped at the enum's own max of 6); "
                  f"all size changes integer={all_integer}, changes={size_changes}")

            # ---------------------------------------------------- row 5 — the mouse dialect
            attach(br, "#dr", "droste", None)
            size0 = report(br)["handles"]["size"]
            wheel_event(br, "#dr", -120, shift=True)   # deltaY<0 — one pinch-out notch
            size1 = report(br)["handles"]["size"]
            wheel_event(br, "#dr", 120, shift=True)    # deltaY>0 — one pinch-in notch
            wheel_event(br, "#dr", 120, shift=True)
            size2 = report(br)["handles"]["size"]
            wheel_ok = size1 == size0 + 1 and size2 == size1 - 2

            attach(br, "#dr", "droste", None)
            size3 = report(br)["handles"]["size"]
            pointer_el(br, "#dr", "pointerdown", cx, cy, {"pointerType": "mouse", "shiftKey": True})
            pointer_win(br, "pointermove", cx + 45, cy, {"pointerType": "mouse", "shiftKey": True})
            size4 = report(br)["handles"]["size"]
            pointer_win(br, "pointermove", cx + 90, cy, {"pointerType": "mouse", "shiftKey": True})
            size5 = report(br)["handles"]["size"]
            pointer_win(br, "pointerup", cx + 90, cy, {"pointerType": "mouse", "shiftKey": True})
            drag_ok = size4 == size3 + 1 and size5 == size3 + 2

            # the plain-drag-is-crease check reads only that a MOUSE drives the same fold recogniser
            # a touch drives (row 1/2's own subject, the magnet, is proven there and not repeated
            # here) — a work with no candidate line, so this stays clear of the magnet's own branch.
            attach(br, "#lm", "livemirror", REC_C)
            drag(br, "#lm", [(20 + 0.10 * 300, 20 + 0.10 * 300),
                              (20 + 0.72 * 300, 20 + 0.40 * 300)], pointer_type="mouse", shift=False)
            rep_plain = report(br)["handles"]
            plain_drag_ok = near(rep_plain["centreX"], 0.72) and near(rep_plain["centreY"], 0.40)

            check(ROWS[4], wheel_ok and drag_ok and plain_drag_ok,
                  f"shift+wheel sizes {size0}->{size1}->(x2)->{size2} (want +1 then -2); "
                  f"shift-drag sizes {size3}->{size4}->{size5} (want +1 then +2 total); "
                  f"plain mouse drag handles={rep_plain} (want ~0.72/~0.40 — the mouse drives the "
                  f"same one-contact recogniser touch does)")

        # the real walk — the walk's own plain-wheel step and ctrl-wheel zoom, both unaffected
        with Browser(width=1280, height=900) as br2:
            br2.navigate(base + "/")
            br2.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
            br2.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br2.reload()
            for _ in range(40):
                br2.sleep(0.15)
                if br2.evaluate("document.documentElement.classList.contains('ex-walk')"
                                "&&document.querySelectorAll('.exh-frame').length>0"
                                "&&scrollY===0"):
                    break
            br2.sleep(0.3)
            SECTIONS = "[...document.querySelectorAll('#ex-stage .exh-frame, #ex-stage .exh-fin')]"
            def cur(b):
                return b.evaluate(
                    "(()=>{const s=%s;return s.findIndex(x=>{const r=x.getBoundingClientRect();"
                    "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});})()" % SECTIONS)
            idx0 = cur(br2)
            br2.wheel(delta_y=400)
            br2.sleep(0.5)
            idx1 = cur(br2)
            plain_wheel_steps = idx1 == idx0 + 1

            ZOPEN = "(()=>{const z=document.getElementById('ex-zoom');return !!(z&&!z.hidden);})()"
            br2.evaluate(
                "(()=>{var e=new WheelEvent('wheel',{deltaY:-100,ctrlKey:true,bubbles:true,"
                "cancelable:true});var img=document.querySelector('.exh-frame img.work');"
                "if(img)img.dispatchEvent(e); else window.dispatchEvent(e);})()")
            br2.sleep(0.3)
            ctrl_wheel_zooms = bool(br2.evaluate(ZOPEN))
            check(ROWS[4] + " (real walk)", plain_wheel_steps and ctrl_wheel_zooms,
                  f"plain wheel {idx0}->{idx1} (want +1); ctrl+wheel opened zoom={ctrl_wheel_zooms}")

        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/gesture-fixture.html")

            # ---------------------------------------------------- row 6 — hover + no scripted focus
            attach(br, "#lm", "livemirror", REC_C)
            before_hover = report(br)
            pointer_win(br, "pointermove", 20 + 40, 20 + 40, {"pointerType": "mouse"})  # no prior down
            after_hover = report(br)
            active_ok = active_is_body(br)
            check(ROWS[5],
                  after_hover["changes"] == before_hover["changes"]
                  and after_hover["handles"] == before_hover["handles"] and active_ok,
                  f"hover produced changes={after_hover['changes'] != before_hover['changes']} "
                  f"(want none); document.activeElement is body={active_ok}")

            # ---------------------------------------------------- row 7 — envelopes
            # A work with NO candidate line — the magnet (row 1/2's own subject) never enters this
            # row, so a plant on it cannot touch this one. Two live moves in opposite directions each
            # spend the envelope's own bounded step (ENV_STEP_FRACTION of the handle's span) without
            # fully reaching where the finger is, so the raw release point still sits well past where
            # centreX stands the instant the finger lifts — release alone needs more than one call.
            attach(br, "#lm", "livemirror", REC_C)
            pointer_el(br, "#lm", "pointerdown", 20 + 0.90 * 300, 20 + 0.50 * 300, {"pointerType": "mouse"})
            pointer_win(br, "pointermove", 20 + 0.05 * 300, 20 + 0.50 * 300, {"pointerType": "mouse"})
            before_release = report(br)
            n_before = len(changes_for(before_release, "centreX"))
            mid_centre_x = before_release["handles"]["centreX"]
            pointer_win(br, "pointerup", 20 + 0.05 * 300, 20 + 0.50 * 300, {"pointerType": "mouse"})
            after_release = report(br)
            release_changes = changes_for(after_release, "centreX")[n_before:]
            multi_step = len(release_changes) > 1
            all_envelope = all(c["via"] == "envelope" for c in release_changes)
            landed_exact = near(after_release["handles"]["centreX"], 0.05, eps=1e-9)
            # "no handle jumps to a value" — read directly off the bound every logged step obeys,
            # never off an assumed direction: each one moves by at most the envelope's own designed
            # share of the handle's span (ENV_STEP_FRACTION · its declared [lo,hi]), never the whole
            # remaining distance in one call.
            no_instant_jump = bool(release_changes) and all(
                abs(c["to"] - c["from"]) <= 0.35 + 1e-9 for c in release_changes)
            check(ROWS[6],
                  multi_step and all_envelope and landed_exact and no_instant_jump,
                  f"before release centreX={mid_centre_x} (finger already at 0.05); release-time "
                  f"steps={release_changes} (want >1, each via 'envelope', the first short of 0.05, "
                  f"the last landing exactly on the finger's own place)")

# ---------------------------------------------------------------- report
import shutil  # noqa: E402

shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
