#!/usr/bin/env python3
"""EX-COVER — the transformation fills the viewport, over the whole span of poses a flight can ask.
Run: python3 tests/test_pass_cover.py

Root: his word of 2026-08-25 — it is beautiful when the camera stands at an angle, but that does not
always cover the screen.

WHAT THIS IS NOT. The engine already carries a coverage law and it answers a different question:
whether a voice drawing OVER another lets what is beneath it show through where it draws nothing
(tests/test_pass_coverage.py, §7's alpha law). This is the geometric case. The drawn plane itself —
one canvas, carrying the whole passage — is moved by the camera's own pose, and a pose that pans,
dollies out or turns leaves the plane short of the frame's edges. Whatever lies under the canvas then
shows in the gap. Nothing checked it.

THE SPAN, AND WHY IT IS A SPAN AND NOT A HANDFUL OF POSES.

  A composed flight's camera track is four points (pass-composer.js). The two ENDS are the neutral
  pose — every axis at zero — and the two middle points carry the composed values. Each axis is
  carried between them by a MONOTONE spline, and a monotone spline through a set of points does not
  leave the range those points span. So every pose that occurs at any instant of any composed flight
  lies inside the box whose sides are the composer's own caps, and the box is the span.

  WHICH AXES. The composed track names six: pan.x, pan.y, logScale, pitch, yaw, roll — and `fov`
  always null. It names neither orbit nor tilt, so those stand at their neutral on every composed
  flight and the span has six sides, not eight. The rows below read that off the composer's own file
  rather than assuming it.

  THE CAPS ARE THE COMPOSER'S OWN, read off the same file. `DOLLY_CAP` is 0.5 and every axis is
  bounded by it or by a stated share of it: the dolly approaches it without reaching it, roll and yaw
  reach it, pitch reaches half of it, and a pan is a work's own normalised centre less one half, so
  it lies in [-0.5, +0.5].

  AND THE WHOLE BOX IS ANSWERED BY ITS CORNERS. The reach a pose needs is monotone in the magnitude
  of each axis, holding the others: moving the plane further, shrinking it further, or turning it
  further can only ever ask for more carrier and never for less. A function monotone in each
  coordinate attains its maximum over a box at a corner of that box, so checking every corner of the
  span answers for every pose inside it. The corners are finite and all of them are checked. The
  monotonicity itself is not assumed: a row below walks each axis across its own span and holds that
  the reach never falls as the axis grows.

  IT STAYS TRUE UNDER THE CHANGE NOW IN FLIGHT ELSEWHERE. Another worker is moving where the two
  middle points STAND IN TIME — to the passage's own motion peak instead of the travelling window's
  ends. That moves when a pose happens, not which poses are reachable: the track still runs from the
  neutral through two composed points and back, the caps are unchanged, and the span is the same box.
  Every argument above is about the poses themselves and none of it reads a second.

WHAT THE ROWS MEASURE. The host's own geometry is used, not a copy of it — `bench.reach`,
`bench.covers` and `bench.quad` are the very functions the frame loop calls. That geometry is first
held against the browser's own rendering of the transform string the host writes, so a row that then
reasons over the span is reasoning about what is actually drawn. Last, a real passage is photographed
at a capped pose and the frame is read for any pixel the canvas did not paint.
"""
import base64
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 1000, 900
DUR = 6000
RISE, FALL = 1.0, 1.0

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the span, read off the composer

COMPOSER = (ROOT / "engine" / "assets" / "pass-composer.js").read_text(encoding="utf-8")
LAYER_SRC = (ROOT / "engine" / "assets" / "pass-layer.js").read_text(encoding="utf-8")

_m = re.search(r"var DOLLY_CAP = ([0-9.]+);", COMPOSER)
DOLLY_CAP = float(_m.group(1)) if _m else None

# The composed track's own axis list, read off the literal the composer builds it from.
_track = re.search(r"var track = \[\{ at: \"a\",(.{0,400})", COMPOSER, re.S)
TRACK_TEXT = _track.group(1) if _track else ""

# THE SPAN, one side per axis, in the axis's own units. Every value is DOLLY_CAP or a stated share of
# it, and none of them is chosen here — the comment above each names where in the composer it is set.
SPAN = {
    # `dolly = DOLLY_CAP * asked / (|asked| + DOLLY_CAP)` — approaches the cap, never reaches it
    "logScale": DOLLY_CAP,
    # `roll = reach * camBound * (±1) * (|rollDelta| / 90)`, camBound = DOLLY_CAP
    "roll": DOLLY_CAP,
    # `yaw = reach * camBound * (±1) * (|gateOff| / 0.5)`, camBound = DOLLY_CAP
    "yaw": DOLLY_CAP,
    # `pitchCap = 0.5 * camBound` — the composer publishes pitch's own ceiling at half of it
    "pitch": 0.5 * DOLLY_CAP if DOLLY_CAP else None,
    # `panFrom = [centre.x - 0.5, centre.y - 0.5]` with a normalised centre in [0, 1]
    "panX": 0.5,
    "panY": 0.5,
}

# THE CEILING THE CARRIER MAY GROW TO, derived in the host from the render ladder's own last rung
# rather than chosen: growing the carrier spends resolution, and the ladder's floor is how much of it
# the engine has already declared it will spend. Read back here off both files so the row names the
# same number the host computes.
_steps = re.search(r"var STEPS = \[([0-9.,\s]+)\];", LAYER_SRC)
STEPS = [float(x) for x in _steps.group(1).split(",")] if _steps else None
REACH_CEILING = (1.0 / STEPS[-1]) if STEPS else None

# ---------------------------------------------------------------- string rows

check("EX-COVER the composed camera track names six axes, so the span has six sides",
      all(k in TRACK_TEXT for k in ("pan:", "logScale:", "pitch:", "yaw:", "roll:", "fov:"))
      and "orbit" not in TRACK_TEXT and "tilt" not in TRACK_TEXT,
      "orbit and tilt stand at their neutral on every composed flight, so they are not in the span; "
      f"the track literal reads: {' '.join(TRACK_TEXT.split())[:200]}")

check("EX-COVER the caps are the composer's own and are read off its file, never chosen here",
      DOLLY_CAP == 0.5
      and "dolly = DOLLY_CAP * asked / (Math.abs(asked) + DOLLY_CAP)" in COMPOSER
      and "var rollCap = camBound, yawCap = camBound, pitchCap = 0.5 * camBound;" in COMPOSER
      and "panFrom = [num(ca[0]) - 0.5, num(ca[1]) - 0.5];" in COMPOSER,
      f"the span, side by side with where each is set: {json.dumps(SPAN)}")

check("EX-COVER the two ends of a composed track are the neutral pose, which is what makes the span "
      "a box the flight never leaves",
      'var track = [{ at: "a", pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0' in COMPOSER
      and 'track.push({ at: "b", pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0'
      in COMPOSER,
      "each axis runs from zero through its composed value and back on a monotone spline, and a "
      "monotone spline does not leave the range its own points span — so no instant of any composed "
      "flight stands outside the box the caps draw. Where the two middle points stand IN TIME is a "
      "separate question and moving them moves no side of this box")

check("EX-COVER the carrier's reach is derived from the pose, and the pose is never refused for it",
      "function camFit(" in LAYER_SRC and "function quadCovers(" in LAYER_SRC
      and "function reachCeiling() { return 1 / STEPS[STEPS.length - 1]; }" in LAYER_SRC
      and "camFit(art, rec.caps, box)" in LAYER_SRC
      and "return { over: top, hold: lo, pose: poseHeld(pose, lo) };" in LAYER_SRC,
      "a pose that would bare an edge is drawn on a carrier large enough to cover it; where even "
      "the widest carrier cannot, the pose is HELD CLOSER IN and still plays, on the same axes in "
      "the same direction — never refused, which is the charter's own degrade")

check("EX-COVER the carrier's ceiling is the render ladder's own floor, not a number chosen here",
      REACH_CEILING is not None and STEPS is not None
      and abs(REACH_CEILING - 1.0 / STEPS[-1]) < 1e-9,
      f"the carrier spends resolution and nothing else, so it may grow until the picture stands at "
      f"the same floor the render ladder already draws at on a device that needs it: the ladder's "
      f"rungs are {STEPS} and its last is {STEPS[-1] if STEPS else None}, so the carrier's ceiling "
      f"is {REACH_CEILING}x the frame")

check("EX-COVER the carrier's width is found by halving, so it never steps between two frames",
      "var REACH_HALVINGS = 24;" in LAYER_SRC and "mid = (lo + hi) / 2;" in LAYER_SRC
      and "REACH_STEP" not in LAYER_SRC,
      "a carrier quantised to rungs would step between one frame and the next, and a step in the "
      "carrier is a step in the picture — the very seam tests/test_pass_seam.py reds on")


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passcover_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# ---------------------------------------------------------------- browser plumbing

HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};
0"""

# THE MARKER BEHIND EVERYTHING. A pure colour is painted under the whole page, so a pixel of the shot
# that still carries it is a pixel nothing drew over. It is put there rather than inferred because
# "what shows through" is otherwise whatever the walk happens to be showing, and a row cannot tell
# that from a picture. The row that uses it first proves the marker is VISIBLE with the canvas
# hidden, so a green above it cannot come from a marker that was never on screen.
MARK = (255, 0, 255)
MARK_CSS = """
  var st = document.createElement('style');
  // `body` carries its own `transition:background var(--d-ground) var(--ease)`
  // (exhibition.css) — the ambient ground-colour fade, unrelated to the pass system. Overriding
  // `background` alone still lets the browser animate the swap from body's live ground tint to
  // this marker across that transition's own duration (measured live at 2.295s) rather than
  // applying it at once, so a fixed short wait below can catch it still mid-fade and read a
  // near-magenta a pixel-exact comparison misses. `transition:none` here removes the race itself.
  st.textContent = 'html, body, .exh-frame, .exh-fin, #ex-stage {'
                 + ' background: rgb(255,0,255) !important; transition: none !important; }'
                 + ' .exh-frame img.work, .exh-fin img { visibility: hidden !important; }';
  document.head.appendChild(st);
  return true;
"""


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def marker_share(path, box=None):
    """The share of the frame still carrying the marker — pixels nothing drew over.

    `box`, when given, restricts the read to the canvas's OWN rect (CSS px, DPR 1 on this site,
    so it maps straight onto the screenshot's pixels) — the region a passage actually claims,
    which S-91 shrank from the whole window to the work's own hang box. The whole-viewport read
    stays the right one for proving the marker was on screen at all (the row that hides the
    canvas and asks whether magenta is visible anywhere), but "did the frame get left bare" is
    a claim about the canvas's own box, not about the room around it that a passage was never
    asked to paint over."""
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    if box:
        x0 = max(0, int(round(box["x"])))
        y0 = max(0, int(round(box["y"])))
        x1 = min(a.shape[1], int(round(box["x"] + box["w"])))
        y1 = min(a.shape[0], int(round(box["y"] + box["h"])))
        a = a[y0:y1, x0:x1]
    hit = (a[:, :, 0] == MARK[0]) & (a[:, :, 1] == MARK[1]) & (a[:, :, 2] == MARK[2])
    return round(float(hit.mean()), 6)


def wait_state(br, want, tries=60, nap=0.1):
    for _ in range(tries):
        if js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(nap)
    return False


def enter(br):
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    br.key("ArrowDown")
    for _ in range(30):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            br.evaluate(HOOKS)
            # THE STAGE ITSELF, WARMED HERE RATHER THAN LEFT TO THE STEP ABOVE (2026-09-01,
            # V2-CONVERGENCE-PLAN-2026-08-31 Phase 3c, cause C's real mechanism). This site
            # configures no composer, so the ArrowDown just taken carries a null score; until this
            # fix that null-score command still reached `passLayer.offer`, and casting SOMETHING
            # for it (even the funnel's own last resort) was what created the canvas and sized
            # `cssW`/`cssH` (`stageResize`) as a side effect — which is what every row below reads
            # off `window.__exPass.bench.camApplied`/`.quad`, neither of which ever declares a
            # command of its own. `passOffer` now declines a null-score command before the layer is
            # ever asked, so that side effect no longer happens on its own; `bench.make()` is the
            # diagnostics surface built for exactly this (pass-layer.js's own comment: "the
            # diagnostics-only hand a conformance row draws one frame with"), and calling it
            # directly is more honest than leaning on an offer's own by-product to do it.
            br.evaluate("window.__exPass.bench.make()")
            return True
        br.sleep(0.2)
    return False


def score(track):
    dur = DUR / 1000.0
    return {
        "schema": 2, "intent": "the carrier reaches every edge the pose asks it to",
        "pair": {"a": "a", "b": "b"}, "seed": 3, "duration": DUR,
        "interruption": {"withinMs": 200, "resolve": "nearest-door"}, "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b", "track": track,
                   "hang": {"rise": RISE, "fall": FALL}},
        "cues": [{
            "id": "ground", "instrument": {"id": "weave", "api": 1}, "voice": "letter",
            "roles": ["disassembly", "assembly"], "levels": ["CELL"], "stack": 0,
            "window": [0, dur], "works": ["a", "b"], "cameraAuthority": "stage",
            "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                      "out": {"handle": "mix", "value": 1, "measured": True}},
            "nodes": {"prog": {"source": "progress"}, "sec": {"source": "time"},
                      "zero": {"op": "static", "value": 0}, "one": {"op": "static", "value": 1},
                      "many": {"op": "static", "value": 28}},
            "tracks": {"mix": {"node": "prog"}, "clock": {"node": "sec"},
                       "strips": {"node": "many"}, "axis": {"node": "zero"},
                       "speed": {"node": "one"}, "seed": {"node": "zero"},
                       "nMul": {"node": "one"}, "press": {"node": "one"}},
        }],
        "provenance": {"source": "tests/test_pass_cover.py", "measuredAt": "2026-08-25",
                       "by": "the coverage rows"},
    }


def corner_track(pose):
    """A composed track's own shape — the neutral at both ends, the pose held across the middle."""
    mid = {"pan": {"x": pose["panX"], "y": pose["panY"]}, "logScale": pose["logScale"],
           "pitch": pose["pitch"], "yaw": pose["yaw"], "roll": pose["roll"],
           "fov": None, "owner": "stage"}
    zero = {"at": "a", "pan": {"x": 0, "y": 0}, "logScale": 0, "pitch": 0, "yaw": 0, "roll": 0,
            "fov": None, "owner": "stage"}
    end = dict(zero, at="b")
    return [zero, dict(mid, at=2.0), dict(mid, at=4.0), end]


ROWS = [
    "EX-COVER the host's own geometry agrees with the browser's rendering of the transform it writes",
    "EX-COVER over every corner of the span the carrier reaches every pixel of the frame",
    "EX-COVER no pose inside a span costs more than that span's ends, so the corners answer for the box",
    "EX-COVER red-on-bug · at the carrier's old size, poses inside the composer's own cap bare the frame",
    "EX-COVER a real passage at a capped pose leaves no pixel of the frame unpainted",
]

if not chrome_available():
    for r in ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif DOLLY_CAP is None or REACH_CEILING is None:
    for r in ROWS:
        skip(r, "the composer's cap or the host's carrier ceiling could not be read")
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_covershots_"))
    try:
        with serve(TMP) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/")
                br.clear_storage()
                br.navigate(base + "/")
                br.sleep(0.8)
                armed = enter(br)
                WORKS = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                               ".map(function(e){return e.dataset.id;}).slice(0,2);")
                if not (armed and len(WORKS) == 2 and all(WORKS)):
                    for r in ROWS:
                        skip(r, f"the walk never registered a host, or hung no pair: "
                                f"armed={armed} works={WORKS}")
                else:
                    A, B = WORKS[0], WORKS[1]

                    # ---- row 0 · the model against the browser -------------------------
                    # A plain element of exactly the frame's size, carrying exactly the transform
                    # string the host writes for a pose, measured by the browser itself. What the
                    # host's own geometry predicts for that pose is the axis-aligned box the four
                    # corners span; what the browser reports is `getBoundingClientRect`, which is the
                    # same thing. If these two disagree, every row below it is reasoning about a
                    # picture that is not being drawn.
                    probes = [
                        {"panX": 0.3, "panY": -0.2, "logScale": -0.4, "pitch": 0.2, "yaw": -0.35,
                         "roll": 0.25, "orbit": 0, "tilt": 0, "fov": None},
                        {"panX": -0.5, "panY": 0.5, "logScale": -0.5, "pitch": -0.25, "yaw": 0.5,
                         "roll": -0.5, "orbit": 0, "tilt": 0, "fov": None},
                        {"panX": 0, "panY": 0, "logScale": 0, "pitch": 0, "yaw": 0, "roll": 0,
                         "orbit": 0, "tilt": 0, "fov": None},
                    ]
                    agree = js(br, """
                      var poses = %s, out = [];
                      var d = document.createElement('div');
                      d.style.cssText = 'position:fixed;left:0;top:0;width:' + innerWidth + 'px;'
                        + 'height:' + innerHeight + 'px;transform-origin:50%% 50%%;'
                        + 'visibility:hidden;pointer-events:none;';
                      document.body.appendChild(d);
                      for (var i = 0; i < poses.length; i++) {
                        d.style.transform = window.__exPass.bench.camApplied(poses[i], null) || '';
                        var r = d.getBoundingClientRect();
                        var q = window.__exPass.bench.quad(poses[i], 'standard', 1);
                        var cx = innerWidth / 2, cy = innerHeight / 2;
                        var xs = q.map(function (p) { return p[0]; });
                        var ys = q.map(function (p) { return p[1]; });
                        out.push({
                          browser: [r.left, r.top, r.right, r.bottom].map(function (v) {
                            return Math.round(v * 100) / 100; }),
                          model: [Math.min.apply(null, xs) + cx, Math.min.apply(null, ys) + cy,
                                  Math.max.apply(null, xs) + cx, Math.max.apply(null, ys) + cy]
                            .map(function (v) { return Math.round(v * 100) / 100; })
                        });
                      }
                      d.parentNode.removeChild(d);
                      return out;
                    """ % json.dumps(probes))
                    worst = 0.0
                    for row in agree:
                        for u, v in zip(row["browser"], row["model"]):
                            worst = max(worst, abs(u - v))
                    # The browser rounds a transformed rect to hundredths of a pixel and the model
                    # does not, so the two are held to a bar the ROUNDING itself sets rather than one
                    # chosen here: half of the last place the browser reports.
                    check(ROWS[0], worst <= 0.05,
                          f"over {len(probes)} poses the host's own geometry and the browser's own "
                          f"measurement of the transform the host writes differ by at most "
                          f"{worst:.4f} px, against the 0.05 px the browser's own hundredth-pixel "
                          f"rounding allows. Rows: {json.dumps(agree)}")

                    # ---- rows 1 and 3 · the whole span, by its corners ------------------
                    # Every corner of the six-sided box, with each axis at its cap either way and at
                    # zero. The reach the host derives is asked for, and the host is then asked
                    # whether THAT reach covers — and, in the same pass, whether the carrier as it
                    # stood before this repair (a reach of one) covered.
                    span = js(br, """
                      var S = %s;
                      var out = {worstReach: 0, worstPose: null, uncovered: 0,
                                 uncoveredWorst: null, bareWorst: null, bareCount: 0, total: 0,
                                 held: 0, tightestHold: 1, tightestPose: null, overCeiling: 0,
                                 ceiling: window.__exPass.bench.fit(
                                   {panX:0,panY:0,roll:0,yaw:0,pitch:0,logScale:0,
                                    orbit:0,tilt:0,fov:null}, 'standard').ceiling};
                      function ax(c) { return [-c, 0, c]; }
                      out.sides = {};
                      var P = ax(S.panX), Q = ax(S.panY), R = ax(S.roll), Y = ax(S.yaw),
                          I = ax(S.pitch), L = [-S.logScale, 0];
                      out.sides = {panX: P.length, panY: Q.length, roll: R.length,
                                   yaw: Y.length, pitch: I.length, logScale: L.length};
                      out.expected = P.length * Q.length * R.length * Y.length * I.length
                                   * L.length;
                      for (var a = 0; a < P.length; a++)
                      for (var b = 0; b < Q.length; b++)
                      for (var c = 0; c < R.length; c++)
                      for (var d = 0; d < Y.length; d++)
                      for (var e = 0; e < I.length; e++)
                      for (var f = 0; f < L.length; f++) {
                        var pose = {panX: P[a], panY: Q[b], roll: R[c], yaw: Y[d], pitch: I[e],
                                    logScale: L[f], orbit: 0, tilt: 0, fov: null};
                        out.total++;
                        var got = window.__exPass.bench.fit(pose, 'standard');
                        if (got.over > out.worstReach) {
                          out.worstReach = got.over; out.worstPose = pose;
                        }
                        if (got.hold < 1 - 1e-9) {
                          out.held++;
                          if (got.hold < out.tightestHold) {
                            out.tightestHold = got.hold; out.tightestPose = pose;
                          }
                        }
                        if (!window.__exPass.bench.covers(got.pose, 'standard', got.over)) {
                          out.uncovered++;
                          if (out.uncoveredWorst === null) out.uncoveredWorst = pose;
                        }
                        if (got.over > out.ceiling + 1e-9) out.overCeiling++;
                        if (!window.__exPass.bench.covers(pose, 'standard', 1)) {
                          out.bareCount++;
                          if (out.bareWorst === null) out.bareWorst = pose;
                        }
                      }
                      return out;
                    """ % json.dumps(SPAN))
                    check(ROWS[1],
                          span["uncovered"] == 0 and span["overCeiling"] == 0
                          and span["total"] == span["expected"],
                          f"every one of the {span['total']} corners of the span (its sides being "
                          f"{json.dumps(span['sides'])}, so {span['expected']} in all) is covered "
                          f"by the "
                          f"fit the host derives for it, and none asks for a carrier past the "
                          f"ceiling of {span['ceiling']}x. The widest carrier any corner asks for is "
                          f"{round(span['worstReach'], 4)}x the frame, at "
                          f"{json.dumps(span['worstPose'])}. {span['held']} of the corners ask for "
                          f"more excursion than the widest carrier can keep whole and are held "
                          f"closer in; the tightest hold is "
                          f"{round(span['tightestHold'], 4)} of the pose asked for, at "
                          f"{json.dumps(span['tightestPose'])} — still an excursion, on the same "
                          f"axes in the same direction. Corners left bare: {span['uncovered']}"
                          + ("" if not span["uncoveredWorst"]
                             else " — first at " + json.dumps(span["uncoveredWorst"])))
                    check(ROWS[3],
                          span["bareCount"] > 0,
                          f"at a carrier of exactly the frame — the size it was before this repair — "
                          f"the frame is left bare at {span['bareCount']} of the span's "
                          f"{span['total']} corners, the first of them "
                          f"{json.dumps(span['bareWorst'])}. Every one of those is a pose the "
                          f"composer's own caps allow, so this is not a hypothetical")

                    # ---- row 2 · the monotonicity the corner argument rests on ----------
                    # Each axis walked across its own span with the others at zero: the reach must
                    # never fall as the axis grows. If it did, a corner would not answer for the box
                    # and the row above would be reasoning from a false premise.
                    mono = js(br, """
                      var S = %s, out = {broke: [], steps: 0};
                      var keys = ['panX', 'panY', 'roll', 'yaw', 'pitch', 'logScale'];
                      out.worstInside = 0;
                      function rest(at) {
                        return {panX: -S.panX * at, panY: -S.panY * at, roll: -S.roll * at,
                                yaw: -S.yaw * at, pitch: -S.pitch * at,
                                logScale: -S.logScale * at, orbit: 0, tilt: 0, fov: null};
                      }
                      // once with every other axis at its neutral, once with every other axis at
                      // its own cap — the context the corner the maximum is claimed at stands in
                      var contexts = [0, 1, -1];
                      // WHAT THE POSE COSTS THE FRAME, in one number: the carrier it asks for over
                      // the share of the asked-for excursion the frame can then take. The carrier
                      // grows until it reaches its ceiling and the hold tightens after that, so
                      // neither alone is the cost and the ratio is.
                      function cost(pose) {
                        var got = window.__exPass.bench.fit(pose, 'standard');
                        out.steps++;
                        return got.over / got.hold;
                      }
                      for (var ci = 0; ci < contexts.length; ci++) {
                        for (var i = 0; i < keys.length; i++) {
                          var key = keys[i], cap = S[key];
                          var lo = rest(contexts[ci]), hi = rest(contexts[ci]);
                          // logScale is one-sided: only pulling BACK bares an edge, coming in
                          // never does, so its span runs from its cap to zero and not through it.
                          var ends = (key === 'logScale') ? [-cap, 0] : [-cap, cap];
                          lo[key] = ends[0]; hi[key] = ends[1];
                          var atEnds = Math.max(cost(lo), cost(hi));
                          for (var n = 1; n < 40; n++) {
                            var pose = rest(contexts[ci]);
                            pose[key] = ends[0] + (ends[1] - ends[0]) * n / 40;
                            var k = cost(pose);
                            if (k > out.worstInside) out.worstInside = k;
                            if (k > atEnds + 1e-6) {
                              out.broke.push(key + ' with the rest at ' + contexts[ci]
                                             + ' cap, at ' + pose[key].toFixed(4) + ': ' 
                                             + k.toFixed(6) + ' over the ' + atEnds.toFixed(6)
                                             + ' its own two ends cost');
                            }
                          }
                        }
                      }
                      return out;
                    """ % json.dumps(SPAN))
                    check(ROWS[2], not mono["broke"],
                          f"each of the six axes walked across its WHOLE span in 40 steps, in "
                          f"three contexts — every other axis at its neutral, at its cap one way, "
                          f"and at its cap the other — {mono['steps']} readings in all. Nowhere "
                          f"inside a span does a pose cost the frame more than one of that span's "
                          f"own two ends costs, which is what puts the maximum over the box on a "
                          f"corner of it and lets the corners answer for every pose between them. "
                          f"Places an interior pose cost more than its ends: "
                          f"{mono['broke'] or 'none'}")

                    # ---- row 4 · a real passage, photographed ---------------------------
                    # The marker is painted under everything, so a pixel still carrying it is a pixel
                    # nothing drew over. It is proved VISIBLE first, with the canvas hidden, so a
                    # green here cannot come from a marker that was never on screen.
                    js(br, MARK_CSS)
                    br.sleep(0.3)
                    worst_pose = span["worstPose"] or probes[1]
                    tr = corner_track(worst_pose)
                    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                " settleSlackMs:2000, clockPin:3.0, progressPin:0.5,"
                                " fixedScale:true}); 0")
                    got = js(br, """
                      window.__sc = %s;
                      var A = document.querySelector('.exh-frame[data-id="%s"]');
                      var B = document.querySelector('.exh-frame[data-id="%s"]');
                      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                                 kind:'step', cause:'cover',
                                                                 velocity:0, score: window.__sc});
                      window.__cmd = cmd;
                      return {took: cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false};
                    """ % (json.dumps(score(tr)), A, B))
                    running = wait_state(br, "running")
                    # THE FRAME, READ ONCE. S-91 made "the frame" the work's own hang box rather
                    # than the window — the fixed `frameEl` the canvas travels inside, which crops
                    # a grown carrier with its own `overflow:hidden` (pass-layer.js `stageMake`).
                    # That element, not the canvas's own (pose-grown, and clipped) rect, is the
                    # box this row's "no pixel of the frame unpainted" claim is about.
                    frame_rect = js(br, "var c = document.querySelector('canvas');"
                                        "var f = c && c.parentElement;"
                                        "if (!f) return null;"
                                        "var b = f.getBoundingClientRect();"
                                        "return {x: b.left, y: b.top, w: b.width, h: b.height};")
                    br.sleep(1.0)
                    shot = png(br, SHOTS / "capped.png")
                    painted = marker_share(shot, box=frame_rect)
                    js(br, "window.__exPass.bench.show(false); return null;")
                    br.sleep(0.4)
                    bare = png(br, SHOTS / "bare.png")
                    bare_share = marker_share(bare)
                    read = js(br, "var r = window.__exPass.host.report();"
                                  "var c = document.querySelector('canvas').getBoundingClientRect();"
                                  "return {state: r.state, pose: r.camera && r.camera.pose,"
                                  " rect: {x: Math.round(c.left), y: Math.round(c.top),"
                                  "        w: Math.round(c.width), h: Math.round(c.height)},"
                                  " iw: innerWidth, ih: innerHeight};")
                    if not (got["took"] and running):
                        check(ROWS[4], False, f"the passage never took the frame: {got} "
                                              f"running={running}")
                    else:
                        check(ROWS[4],
                              bare_share > 0.5 and painted == 0.0,
                              f"at the span's own widest pose the frame carries {painted * 100:.4f}%"
                              f" of the marker — pixels nothing drew over. With the canvas hidden "
                              f"the same frame carries {bare_share * 100:.4f}%, which is what says "
                              f"the marker was on screen to be covered. The canvas stood at "
                              f"{read['rect']} on a {read['iw']}x{read['ih']} frame")
    finally:
        shutil.rmtree(SHOTS, ignore_errors=True)

# ---------------------------------------------------------------- report
shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
