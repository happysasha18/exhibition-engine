#!/usr/bin/env python3
"""PASS-API-V1 — the return to the hang: the two ends of a passage, measured.

Run: python3 tests/test_pass_hang.py

Root: his word 2026-08-14 08:39. A passage takes the frame and gives it back, and until now nothing
guaranteed the two ends lined up. These rows measure both ends against the DOM the walk actually
hangs, rather than asserting that they agree.

WHAT IS COMPARED, AND AGAINST WHAT.

  The departure. The walk stands on the departing work. The renderer takes the frame and draws its
  first frame. Those two pictures are photographed and compared inside the project's seam threshold
  of 6 of 255 — the same bar tests/test_pass_weave.py judges a door by. A first frame that stood at
  the whole frame instead of on the work's own box would miss it by the width of the picture.

  The arrival. The renderer's last frame stands on the arriving work's hang box; the handoff then
  releases the canvas and reveals the DOM. Both are photographed and compared over the canvas's OWN
  rect — the region the renderer actually drew, which is the region a seam could show in.

  The comparison is always made on the canvas's rect rather than on the whole viewport, because
  outside it the renderer never claimed anything and the walk's own chrome is free to differ.

The score below is this file's own: one cue naming the woven instrument, every handle tracked so the
picture is a function of progress alone. It needs no lab tree, so these rows never skip for a
missing read-only source.
"""
import base64
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
VW, VH = 1000, 900
SEAM = 6.0          # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
DUR = 2400          # the pass this file measures, in milliseconds
# The rise and the fall this file's score names, in seconds. They are named rather than left to the
# default share so the descent onto the arriving box is a wide, unhurried window: the reframe rows
# turn the frame INSIDE that descent, which is the only stretch where the destination box is what
# the camera is actually reading. A turn during the plateau would move nothing, and a row that
# turned there could not tell a carried reframe from an uncarried one.
RISE, FALL = 0.4, 0.9
TURN_AT = 0.75      # where in the pass the reframe rows turn the frame — inside the fall
REST_TOL = 1e-6     # §6's rest tolerance, now read against the hang pose
# How much more sharply the pose may turn across a reframe than it turns in the same flight
# undisturbed. The bar is the flight's OWN sharpest turn, measured on a control run, times this.
# A carried reframe adds no corner at all; a cut one adds exactly one.
JUMP_FACTOR = 3.0

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def score(duration=DUR, rise=RISE, fall=FALL, chrome=None):
    """One cue, the woven instrument, every handle on a track. `axis` stands at 0 — the up-and-down
    weave — so the picture never turns on its own clock, and the three voices that used to drift are
    pinned, so one instant of one seed is one picture."""
    cam = {"owner": "stage", "rests": "b", "track": []}
    if rise is not None or fall is not None:
        cam["hang"] = {}
        if rise is not None:
            cam["hang"]["rise"] = rise
        if fall is not None:
            cam["hang"]["fall"] = fall
    s = {
        "schema": 2,
        "intent": "the return to the hang, measured at both of its ends",
        "pair": {"a": "a", "b": "b"},
        "seed": 3,
        "duration": duration,
        "interruption": {"withinMs": 200, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": cam,
        "cues": [{
            "id": "hang-main",
            "instrument": {"id": "weave", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "assembly"],
            "levels": ["SURFACE", "CELL"],
            "window": [0, duration / 1000.0],
            "works": ["a", "b"],
            "cameraAuthority": "stage",
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
        "provenance": {"source": "tests/test_pass_hang.py", "measuredAt": "2026-08-14",
                       "by": "the return-to-the-hang rows"},
    }
    if chrome is not None:
        s["chromeReveal"] = chrome
    return s


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passhang_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
BUNDLE = (TMP / "exhibition.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

check("PASS-HANG the adapter measures the work's own box, never the section around it",
      "function hangGeometry(" in BUNDLE and 'querySelector("img.work")' in BUNDLE,
      "the section is a full-viewport grid cell and says nothing about where the work hangs in it")

check("PASS-HANG the geometry carries the layout's own crop, fit, radius and transform",
      all(s in BUNDLE for s in ["getComputedStyle(im)", "objectFit", "borderTopLeftRadius",
                                "crop: 1", "orientation:"]),
      "a layout that began to crop or to transform must say so here rather than blur the seam")

check("PASS-HANG the host seats the frame from the instrument's OWN fit",
      "function hangPoseOf(" in LAYER and "inst.fit(iw, ih, W, H)" in LAYER,
      "recomputing the seating here would let the two roads drift by the framing headroom")

check("PASS-HANG the flight is anchored at both hangs, with the score's track riding on it",
      "function anchorPose(" in LAYER and "function camCompose(" in LAYER,
      "a score that rests at its neutral must leave both ends exact")

check("PASS-HANG the rest is read against the arriving work's hang pose",
      "rec.hangPoseB || CAM_NEUTRAL" in LAYER and 'on: rec.hangPoseB ? "hang" : "neutral"' in LAYER,
      "§6's 1e-6 stands, now read against the hang pose; the neutral pose is its special case")

check("PASS-HANG the first frame is drawn before the canvas is shown",
      LAYER.index("playFrame(rec, 0, 0, 0, null)") < LAYER.index("stageShow(true)"),
      "showing an unpainted canvas puts one frame of its clear colour between the walk and the pass")

# Read inside `finish`'s OWN region: `handoff` and `stageShow(false)` both appear elsewhere in the
# file (the under-cover placement, and the context-loss road), so a whole-file index would compare
# two lines that have nothing to do with the landing.
FINISH = LAYER.split("function finish(")[1].split("function settle(")[0]
check("PASS-HANG the handoff reveals the DOM before it releases the canvas, and fades nothing",
      'im.style.transition = "none"' in BUNDLE and "function handoff(cmd, place)" in BUNDLE
      and FINISH.index("hooks.handoff(rec.cmd)") < FINISH.index("stageShow(false)")
      < FINISH.index("camApply(null"),
      "no opacity transition, no generic fade, and no frame that draws neither picture — and the "
      "transform is cleared only once the canvas is gone")

check("PASS-HANG the chrome is revealed once, after the landing, with its parts named",
      "function chromeReveal(" in BUNDLE and BUNDLE.count("chromeReveal(cmd);") == 1
      and "passDockKeys[key]" in BUNDLE
      and all(p in BUNDLE for p in ["plaque", "counter", "share", "sound", "series", "focus"]),
      "the six named parts, and one caller — dock, which already keeps the single ledger that says "
      "whether this command has landed, so the reveal is once because the landing is once")

check("PASS-HANG a score may name the chrome's own timing",
      '"chromeReveal"' in BUNDLE and "PASS_CHROME_MS" in BUNDLE,
      "scoreable timing with a working default where the score names nothing")

# ---------------------------------------------------------------- browser rows

ROWS = [
    "PASS-HANG row 8 · the first drawn frame coincides with the DOM's A, measured pixel-wise",
    "PASS-HANG row 1 · the renderer's door B agrees with the DOM's hang B, measured pixel-wise",
    "PASS-HANG row 1 · the pass rests ON the arriving work's hang pose, not on the whole frame",
    "PASS-HANG row 2 · no blank frame is drawn across a whole passage",
    "PASS-HANG row 2 · the canvas is released at the landing and leaks no z-index",
    "PASS-HANG row 3 · the product landing happens exactly once, on every exit including failures",
    "PASS-HANG row 4 · the chrome appears after the arrival, never before",
    "PASS-HANG row 5 · focus and the accessibility tree each change exactly once",
    "PASS-HANG row 6 · audio, history, the story portion and the caption stay coherent",
    "PASS-HANG row 7 · a resize mid-passage reframes without a jump and still lands on the box",
    "PASS-HANG row 7 · an orientation change mid-passage does the same",
    "PASS-HANG row 7 · a moved destination moves the picture at no instant, and still lands exactly",
]

HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};
window.__marks = function (name, gen) {
  return window.__exPass.report().events.filter(function (e) {
    return e.name === name && (gen === undefined || e.gen === gen); }).length;
};
0"""


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return path


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def canvas_box(br):
    """The canvas's rect as it actually stands, transform and all — the region the renderer claims."""
    return js(br, "var c=document.querySelector('canvas');"
                  "if(!c) return null;"
                  "var b=c.getBoundingClientRect();"
                  "return {x:b.left, y:b.top, w:b.width, h:b.height,"
                  " iw:innerWidth, ih:innerHeight, vis:c.style.visibility,"
                  " z:getComputedStyle(c).zIndex};")


def crop_of(path, box, shot_scale, inset=2):
    """Both pictures cropped to the same region, in shot pixels. The inset drops the outermost ring
    of points: at the very edge of the canvas the renderer's own bilinear sample and the browser's
    image scaler read half a point differently, and that ring says nothing about the seating."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    s = shot_scale
    x0 = max(0, int(round(box["x"] * s)) + inset)
    y0 = max(0, int(round(box["y"] * s)) + inset)
    x1 = min(im.width, int(round((box["x"] + box["w"]) * s)) - inset)
    y1 = min(im.height, int(round((box["y"] + box["h"]) * s)) - inset)
    if x1 - x0 < 8 or y1 - y0 < 8:
        return None
    return im.crop((x0, y0, x1, y1))


def apart(a, b):
    from PIL import Image, ImageChops, ImageStat  # noqa: F401
    if a is None or b is None or a.size != b.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, b))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def region_stats(path, box, shot_scale):
    """The mean and the spread of one region — how a blank frame is told from a drawn one."""
    from PIL import ImageStat
    im = crop_of(path, box, shot_scale)
    if im is None:
        return None
    st = ImageStat.Stat(im)
    return {"mean": sum(st.mean) / 3.0, "spread": sum(st.stddev) / 3.0}


def shot_scale(br, path):
    from PIL import Image
    return Image.open(path).width / float(br.evaluate("String(innerWidth)"))


def wait_state(br, want, tries=80):
    for _ in range(tries):
        if js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(0.05)
    return False


def enter(br, base):
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    br.key("ArrowDown")            # the one step that makes the client fetch pass-layer.js
    for _ in range(30):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            br.evaluate(HOOKS)
            return True
        br.sleep(0.2)
    return False


def rest_at(br, a):
    """Put the walk back on the departing work, chrome settled, nothing in flight.

    Ending whatever is in flight FIRST is the whole point of this helper. A pass still running would
    place the walk at its own arriving work the moment it reached the middle of its passage, and the
    next row would then measure a departing work that stands a viewport away from the eye — which is
    a real reading of a walk that was never put back, not a defect in what it reads."""
    js(br, "window.__exPass.adapter.interrupt('rest'); return null;")
    wait_state(br, "idle")
    top = 9999.0
    for _ in range(10):
        # The walk has its own snap-back guard and its own notion of which frame is resting, so a
        # scroll written once can be written back. The place is therefore READ AFTER it has had time
        # to settle, and asked for again until it holds.
        js(br, "var A=document.querySelector('.exh-frame[data-id=\"%s\"]');"
               "A.classList.add('seen');"
               "scrollTo(0, Math.round(scrollY + A.getBoundingClientRect().top"
               " + (A.getBoundingClientRect().height - innerHeight)/2)); return null;" % a)
        br.sleep(0.35)
        top = float(js(br, "return document.querySelector('.exh-frame[data-id=\"%s\"]')"
                           ".getBoundingClientRect().top;" % a))
        if abs(top) < 3:
            return True
    return False


def declare_and_offer(br, a, b, cause):
    return js(br, """
      var A = document.querySelector('.exh-frame[data-id="%s"]');
      var B = document.querySelector('.exh-frame[data-id="%s"]');
      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                 kind:'step', cause:'%s', velocity:0});
      window.__cmd = cmd;
      var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
      return {got: !!cmd, took: took, gen: cmd ? cmd.gen : null,
              hasScore: !!(cmd && cmd.score)};
    """ % (a, b, cause))


def put_score(base_dir, key, s):
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    cfg["pass"]["scores"] = {key: s}
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if not chrome_available():
    for r in ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_hangshots_"))
    with serve(TMP) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base)
            WORKS = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                           ".map(function(e){return e.dataset.id;}).slice(0,2);")
            ok_pair = armed and len(WORKS) == 2 and all(WORKS)

            if not ok_pair:
                for r in ROWS:
                    skip(r, f"the walk never registered a host, or hung no pair: "
                            f"armed={armed} works={WORKS}")
            else:
                A, B = WORKS[0], WORKS[1]
                PAIR = A + "__" + B
                put_score(TMP, PAIR, score())
                br.navigate(base + "/")
                br.sleep(0.8)
                enter(br, base)
                br.evaluate(HOOKS)

                # ---- row 8 · the departure ------------------------------------------------
                # The walk stands on A with its chrome up. The renderer takes the frame, held at its
                # own first instant, and the two pictures are compared over the region the renderer
                # actually drew. Nothing here is stubbed: this is the real declare, the real offer
                # and the real first frame.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                            " clockPin:0, progressPin:0, fixedScale:true}); 0")
                before = png(br, SHOTS / "depart-dom.png")
                scale = shot_scale(br, before)
                where = js(br, "return {scrollY: Math.round(scrollY),"
                               " aTop: Math.round(document.querySelector('.exh-frame[data-id=\"%s\"]')"
                               ".getBoundingClientRect().top)};" % A)
                r = declare_and_offer(br, A, B, "hang-depart")
                running = wait_state(br, "running")
                br.sleep(0.6)
                box = canvas_box(br)
                read = js(br, "var h=window.__exPass.host.report().hang;"
                              "return {a: h && h.a, scrollY: Math.round(scrollY)};")
                after = png(br, SHOTS / "depart-canvas.png")
                if not (r["took"] and running and box and box["vis"] == "visible"):
                    check(ROWS[0], False,
                          f"the pass never took the frame: took={r['took']} running={running} box={box}")
                else:
                    ca, cb = crop_of(before, box, scale), crop_of(after, box, scale)
                    m, mx = apart(ca, cb)
                    check(ROWS[0], m <= SEAM,
                          f"the first drawn frame against the DOM's A over the renderer's own rect: "
                          f"mean {m:.4f} of 255 (threshold {SEAM}), worst channel {mx}; "
                          f"crops {ca and ca.size} vs {cb and cb.size} from box={box}; "
                          f"the walk stood at {where} before the offer and at {read} after it")
                js(br, "window.__exPass.adapter.interrupt('row8-done'); return null;")
                wait_state(br, "idle")
                br.sleep(0.3)

                # ---- row 1 · the arrival --------------------------------------------------
                # Held at its own last instant, the renderer stands on B's hang box. The handoff then
                # places the walk, reveals the DOM and releases the canvas; the same region is read
                # again. A seam would show here and nowhere else.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:4000,"
                            " clockPin:%f, progressPin:1, fixedScale:true}); 0" % (DUR / 1000.0))
                r = declare_and_offer(br, A, B, "hang-arrive")
                running = wait_state(br, "running")
                br.sleep(0.8)
                box = canvas_box(br)
                canvas_shot = png(br, SHOTS / "arrive-canvas.png")
                rep = js(br, "return window.__exPass.host.report();")
                # the handoff itself: the DOM revealed, the canvas released, inside one task
                js(br, "window.__exPass.adapter.handoff(window.__cmd);"
                       "window.__exPass.bench.show(false); return null;")
                br.sleep(0.4)
                dom_shot = png(br, SHOTS / "arrive-dom.png")
                if not (r["took"] and running and box):
                    check(ROWS[1], False, f"the pass never took the frame: took={r['took']} running={running}")
                else:
                    m, mx = apart(crop_of(canvas_shot, box, scale), crop_of(dom_shot, box, scale))
                    check(ROWS[1], m <= SEAM,
                          f"the renderer's door B against the DOM's hang B over the renderer's own "
                          f"rect: mean {m:.4f} of 255 (threshold {SEAM}), worst channel {mx}")
                hang = rep.get("hang") or {}
                poseB, camera = hang.get("poseB"), (rep.get("camera") or {}).get("pose")
                near = (poseB and camera
                        and max(abs((camera.get(k) or 0) - (poseB.get(k) or 0))
                                for k in ("panX", "panY", "logScale")) <= REST_TOL)
                check(ROWS[2],
                      bool(poseB) and bool(hang.get("b")) and near,
                      f"the box the pass arrived on: {hang.get('b')}; the pose it asks for: {poseB}; "
                      f"the pose actually applied: {camera}")
                js(br, "window.__exPass.adapter.interrupt('row1-done'); return null;")
                wait_state(br, "idle")
                br.sleep(0.3)

                # ---- row 2 · no blank frame, and no canvas left behind ---------------------
                # A whole passage at its own pace, sampled as fast as the harness can photograph. A
                # blank frame is the canvas's own clear colour standing where a picture should be:
                # nearly uniform, and nearly black. Every sample must carry a picture.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                            " clockPin:null, progressPin:null, fixedScale:true}); 0")
                r = declare_and_offer(br, A, B, "hang-frames")
                samples, blanks = [], []
                for _ in range(14):
                    st = js(br, "return {state: window.__exPass.host.report().state,"
                                " box: (function(){var c=document.querySelector('canvas');"
                                " if(!c||c.style.visibility!=='visible') return null;"
                                " var b=c.getBoundingClientRect();"
                                " return {x:b.left,y:b.top,w:b.width,h:b.height};})()};")
                    if st["box"]:
                        p = png(br, SHOTS / ("frame-%02d.png" % len(samples)))
                        s = region_stats(p, st["box"], scale)
                        if s:
                            samples.append(s)
                            # the clear colour is #08080a: nearly black and perfectly flat
                            if s["mean"] < 12.0 and s["spread"] < 3.0:
                                blanks.append(s)
                    if st["state"] == "idle":
                        break
                wait_state(br, "idle")
                br.sleep(0.4)
                check(ROWS[3], len(samples) >= 3 and not blanks,
                      f"{len(samples)} frames sampled across the pass, {len(blanks)} of them blank"
                      + (f" — {blanks[:1]}" if blanks else ""))
                left = canvas_box(br)
                curtained = br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                check(ROWS[4],
                      bool(left) and left["vis"] == "hidden" and curtained == "false",
                      f"after the landing the canvas is {left and left['vis']} at z-index "
                      f"{left and left['z']}, and the curtain class is {curtained}")

                # ---- row 3 · one landing per command, on every exit ------------------------
                # Four exits, four commands: the pass that runs its course, one cut short by a
                # product surface, one whose renderer fails, and one whose renderer never calls back
                # at all. Each must land exactly one dock and reveal the chrome exactly once.
                exits = {}
                for name, drive in (
                        ("settle", None),
                        ("interrupt", "window.__exPass.adapter.interrupt('row3-cut');"),
                        ("fail", "window.__exPass.host.fail(window.__cmd.gen, 'row3-fail');"),
                        ("watchdog", None)):
                    rest_at(br, A)
                    if name == "watchdog":
                        br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                    " settleSlackMs:20, clockPin:0, progressPin:0}); 0")
                    else:
                        br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                    " settleSlackMs:2000, clockPin:null, progressPin:null}); 0")
                    got = declare_and_offer(br, A, B, "hang-exit-" + name)
                    if drive:
                        br.sleep(0.5)
                        br.evaluate(drive + " 0")
                    wait_state(br, "idle")
                    br.sleep(0.6)
                    exits[name] = js(br, "var g=window.__cmd.gen;"
                                         "return {gen:g, docks:window.__marks('dock',g),"
                                         " chrome:window.__marks('chrome',g),"
                                         " handoffs:window.__marks('handoff',g),"
                                         " took:%s};" % ("true" if got["took"] else "false"))
                bad = {k: v for k, v in exits.items() if not (v["docks"] == 1 and v["chrome"] == 1)}
                check(ROWS[5], not bad, f"per exit: {exits}")

                # ---- row 4 · the chrome comes after the arrival ----------------------------
                # Read WHILE the pass is running, then again after it lands. The order is read off
                # the lifecycle marks rather than from the clock, so a fast machine cannot make it
                # look right by accident.
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:4000,"
                            " clockPin:0, progressPin:0}); 0")
                declare_and_offer(br, A, B, "hang-chrome")
                wait_state(br, "running")
                br.sleep(0.5)
                during = js(br, "var g=window.__cmd.gen;"
                                "return {chrome: window.__marks('chrome',g),"
                                " dock: window.__marks('dock',g),"
                                " state: window.__exPass.host.report().state};")
                br.evaluate("window.__exPass.host.configure({progressPin:null, clockPin:null}); 0")
                js(br, "window.__exPass.adapter.interrupt('row4-land'); return null;")
                wait_state(br, "idle")
                br.sleep(0.6)
                order = js(br, """
                  var g = window.__cmd.gen;
                  var evs = window.__exPass.report().events.filter(function(e){return e.gen===g;});
                  var at = function (n) {
                    for (var i=0;i<evs.length;i++) if (evs[i].name===n) return i;
                    return -1; };
                  return {handoff: at('handoff'), dock: at('dock'), chrome: at('chrome'),
                          parts: evs.filter(function(e){return e.name.indexOf('chrome-')===0;})
                                    .map(function(e){return e.name;}),
                          names: evs.map(function(e){return e.name;})};
                """)
                check(ROWS[6],
                      during["chrome"] == 0 and during["state"] == "running"
                      and order["handoff"] >= 0 and order["dock"] > order["handoff"]
                      and order["chrome"] > order["dock"] and len(order["parts"]) == 6,
                      f"while running the chrome had fired {during['chrome']} times; after landing "
                      f"the order is handoff@{order['handoff']} → dock@{order['dock']} → "
                      f"chrome@{order['chrome']}, parts={order['parts']}")

                # ---- row 5 · focus and the accessibility tree, once each -------------------
                rest_at(br, A)
                br.evaluate("""
                  window.__watch = {focus: 0, aria: 0};
                  document.addEventListener('focusin', function () { window.__watch.focus++; }, true);
                  window.__mo = new MutationObserver(function (recs) {
                    recs.forEach(function (m) {
                      if (m.attributeName === 'aria-hidden') window.__watch.aria++; }); });
                  window.__mo.observe(document.getElementById('ex-stage'), {attributes: true});
                  document.body.focus(); 0""")
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                            " clockPin:null, progressPin:null}); 0")
                declare_and_offer(br, A, B, "hang-focus")
                wait_state(br, "idle")
                br.sleep(0.8)
                w = js(br, "window.__mo.disconnect();"
                           "return {focus: window.__watch.focus, aria: window.__watch.aria,"
                           " on: document.activeElement ? document.activeElement.dataset.id : null,"
                           " inert: !!document.getElementById('ex-stage').inert};")
                check(ROWS[7],
                      w["focus"] == 1 and w["aria"] == 2 and w["on"] == B and w["inert"] is False,
                      f"focus moved {w['focus']} time(s) and rests on {w['on']} (the arriving work "
                      f"is {B}); the stage's aria-hidden changed {w['aria']} times — once on, once "
                      f"off; inert now {w['inert']}")

                # ---- row 6 · what a passage owns none of ----------------------------------
                rest_at(br, A)
                start = js(br, """
                  var snd = document.getElementById('ex-sound');
                  var au = document.querySelector('audio');
                  return {history: history.length, hash: location.hash,
                          sound: snd ? snd.className : null,
                          playing: au ? !au.paused : null,
                          told: (document.querySelector('.exh-capzone .told')||{}).textContent || ''};
                """)
                declare_and_offer(br, A, B, "hang-coherent")
                wait_state(br, "idle")
                br.sleep(0.9)
                end = js(br, """
                  var snd = document.getElementById('ex-sound');
                  var au = document.querySelector('audio');
                  var cap = document.querySelector('.exh-capzone');
                  return {history: history.length, hash: location.hash,
                          sound: snd ? snd.className : null,
                          playing: au ? !au.paused : null,
                          share: (document.querySelector('.ex-share')||{dataset:{}}).dataset.share,
                          place: (function () {
                            // the remembered place carries the bundle's own namespace, so the key is
                            // found rather than spelled out here
                            for (var i = 0; i < sessionStorage.length; i++) {
                              var k = sessionStorage.key(i);
                              if (k.indexOf('place') < 0) continue;
                              try { return JSON.parse(sessionStorage.getItem(k)).id; } catch (e) {}
                            }
                            return null; })(),
                          title: cap ? (cap.querySelector('.title')||{}).textContent : null,
                          shown: cap ? cap.classList.contains('show') : false};
                """)
                check(ROWS[8],
                      end["history"] == start["history"] and end["hash"] == start["hash"]
                      and end["sound"] == start["sound"] and end["playing"] == start["playing"]
                      and end["share"] == B and end["place"] == B and end["shown"] is True
                      and bool(end["title"]),
                      f"history {start['history']}→{end['history']}, hash {start['hash']!r}→"
                      f"{end['hash']!r}, sound {start['sound']!r}→{end['sound']!r}, playing "
                      f"{start['playing']}→{end['playing']}; the caption stands on {end['share']} "
                      f"({end['title']!r}) and the remembered place is {end['place']}")

                # ---- row 7 · the viewport and orientation matrix ---------------------------
                # A real turn of the frame, mid-passage, on the walk's own resize road. The applied
                # pose is sampled every step; the largest step across the change is the jump, and
                # the landing must still stand on the box the new layout hangs.
                def one_flight(turn=None):
                    """One whole pass, with the applied pose sampled throughout. `turn` gives the
                    frame's new size, applied a quarter of the way in on the walk's own resize road.
                    Returns the largest step the pose took between two samples, and how it landed."""
                    rest_at(br, A)
                    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                " settleSlackMs:4000, clockPin:null, progressPin:null,"
                                " fixedScale:true}); 0")
                    # Only poses belonging to the transaction in flight are sampled. The diagnostic
                    # surface keeps the LAST run's camera readable after it has gone, so a sampler
                    # that took whatever it found would count the step from the previous landing to
                    # this pass's first frame as a jump — a jump between two transactions, which is
                    # no jump at all.
                    # SAMPLED EVERY ANIMATION FRAME, from inside the page. A sampler driven from
                    # outside returns every thirty or forty milliseconds, and a pose that stepped
                    # once within a single frame would be spread across that whole gap and read as
                    # ordinary travel. One sample a frame is what makes a step visible as a step.
                    br.evaluate("""
                      window.__poses = [];
                      (function tick() {
                        window.__raf = requestAnimationFrame(tick);
                        var r = window.__exPass.host.report();
                        if (r.active && r.state === 'running' && r.camera && r.camera.pose) {
                          window.__poses.push({gen: r.gen, pose: r.camera.pose,
                                               t: performance.now()});
                        }
                      })(); 0""")
                    got = declare_and_offer(br, A, B, "hang-reframe")
                    wait_state(br, "running")
                    br.sleep(DUR * TURN_AT / 1000.0)
                    if turn:
                        br._cmd("Emulation.setDeviceMetricsOverride", width=turn[0], height=turn[1],
                                deviceScaleFactor=1, mobile=False)
                        br.sleep(0.35)
                    landed = wait_state(br, "idle", tries=160)
                    br.sleep(0.5)
                    out = js(br, """
                      cancelAnimationFrame(window.__raf);
                      var r = window.__exPass.host.report();
                      var gen = window.__cmd.gen;
                      var p = window.__poses.filter(function (s) { return s.gen === gen; });
                      // HOW SHARPLY THE POSE TURNS, frame against frame — the change in its change.
                      // The rise and the fall are real motion, and fast motion, so the plain step
                      // between two frames is large by nature and says nothing about continuity: a
                      // reframe's own step hides inside it. A STEP, though, is a corner, and a
                      // corner shows in the second difference while smooth travel does not, however
                      // fast that travel is. This is what tells a reframe carried across from a
                      // reframe cut.
                      var worst = 0;
                      for (var i = 2; i < p.length; i++) {
                        ['panX','panY','logScale'].forEach(function (k) {
                          var a = p[i-2].pose[k]||0, b = p[i-1].pose[k]||0, c = p[i].pose[k]||0;
                          var d = Math.abs(c - 2*b + a);
                          if (d > worst) worst = d; }); }
                      return {worst: worst, n: p.length, rest: r.rest,
                              hang: r.hang, events: r.events.filter(function (e) {
                                return e.name === 'reframe-hang'; }).length};
                    """)
                    if turn:
                        br._cmd("Emulation.setDeviceMetricsOverride", width=VW, height=VH,
                                deviceScaleFactor=1, mobile=False)
                        br.sleep(0.4)
                    out["took"] = bool(got["took"])
                    out["landed"] = landed
                    return out

                # THE CONTROL. The rise and the fall are real motion — the pose travels the whole way
                # from the departing box to the whole frame inside a fifth of the pass — so the step
                # between two samples is large by nature, and a bare number would say nothing about
                # continuity. The same flight, undisturbed, is what the reframed ones are read
                # against: a reframe that put a step into the flight would show as a step BEYOND the
                # one the flight already takes.
                control = one_flight(None)
                CTRL = control["worst"]

                def reframe_case(row, w2, h2):
                    out = one_flight((w2, h2))
                    rest = out.get("rest") or {}
                    hangb = (out.get("hang") or {}).get("b") or {}
                    # the destination was recalculated against the NEW frame, and the pass landed on
                    # it: the box the walk hangs in is centred in the frame that now stands
                    centred = abs(hangb.get("x", -999) + hangb.get("w", 0) / 2.0 - w2 / 2.0) <= 2
                    # the rise and the fall the score named are the ones the flight actually flew
                    edge = (out.get("hang") or {}).get("edge") or {}
                    scored_edges = (abs(edge.get("rise", -1) - RISE) < 1e-9
                                    and abs(edge.get("fall", -1) - FALL) < 1e-9)
                    check(row,
                          scored_edges and
                          out["took"] and out["landed"] and out["n"] >= 5 and out["events"] >= 1
                          and out["worst"] <= CTRL * JUMP_FACTOR and rest.get("rested") is True
                          and rest.get("on") == "hang" and centred,
                          f"{out['n']} poses sampled, {out['events']} reframe(s) recorded; the "
                          f"sharpest the pose turned was {out['worst']:.6f} against the "
                          f"undisturbed flight's own {CTRL:.6f} (bar {JUMP_FACTOR}×); it rested "
                          f"{rest.get('off')} from the {rest.get('on')} pose (tolerance "
                          f"{rest.get('tol')}) on the box {hangb}, centred in the new frame: "
                          f"{centred}; the score's own rise and fall were flown: {edge}")

                reframe_case(ROWS[9], 760, 900)      # a plain resize: the frame narrows
                reframe_case(ROWS[10], 900, 760)     # an orientation change: the frame turns

                # THE RESEAT, ISOLATED. The two rows above turn a real frame on a real walk, and on
                # a walk that hangs its works small and centred the destination's pose hardly moves
                # when the frame changes — the step a cut reframe would leave is a quarter of what
                # the flight is travelling anyway, and no sampler can pick it out of that. Here the
                # two boxes are stated and far apart, and the real reseat runs between them: the
                # picture must not move at the instant the destination does, and the flight must
                # still land on the box that now stands.
                r = js(br, """
                  var s = %s;
                  var box = function (x, y, w, h) {
                    return {workId:'b', x:x, y:y, w:w, h:h, fit:'fill', crop:1, radius:2,
                            transform:null, dpr:1, orientation:'landscape'}; };
                  var got = window.__exPass.bench.hangReseat(
                    s, %d,
                    box(468, 418, 64, 64),        // where the departing work hangs
                    box(468, 418, 64, 64),        // where the arriving work hung
                    box(60, 700, 420, 300),       // and where it hangs after the frame changed
                    %f);
                  var worst = 0;
                  ['panX','panY','logScale'].forEach(function (k) {
                    var d = Math.abs((got.after[k]||0) - (got.before[k]||0));
                    if (d > worst) worst = d; });
                  var landed = 0;
                  ['panX','panY','logScale'].forEach(function (k) {
                    var d = Math.abs((got.end[k]||0) - (got.wants[k]||0));
                    if (d > landed) landed = d; });
                  return {moved: worst, landed: landed, carry: got.carry,
                          before: got.before, after: got.after, end: got.end, wants: got.wants};
                """ % (json.dumps(score()), DUR, DUR * TURN_AT / 1000.0))
                check(ROWS[11],
                      r["moved"] <= REST_TOL and r["landed"] <= REST_TOL,
                      f"at the instant the destination moved, the picture moved {r['moved']:.9f} "
                      f"(tolerance {REST_TOL}); by the end it stood {r['landed']:.9f} from the box "
                      f"that now hangs. The carry the reseat took up: {r['carry']}")

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
