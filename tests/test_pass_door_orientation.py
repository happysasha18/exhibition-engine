#!/usr/bin/env python3
"""PASS-DOOR-ORIENTATION — every instrument's real door, on a work that is not square.
Run: python3 tests/test_pass_door_orientation.py

ROOT. His report of 2026-09-01, watching the live product: sometimes a crossing is beautiful, and
sometimes «the picture turns ninety degrees or mirrors». Chasing it turned up a defect class rather
than a turn: an instrument whose flat, door-time reading of the photograph applies a factor of the
FRAME'S OWN SHAPE that the host's crop cancellation cannot reach. At the whole frame the factor is
right — it is part of the cover fit — so nothing anywhere looked wrong. At a real DOOR, where the
host drives `fit` toward identity so the whole work spans the work's own box (`seated`, in
pass-layer.js's `drawPose`), the factor stands alone and the work is drawn stretched, squeezed or
cropped along ONE axis by the frame's own ratio. On a portrait photograph in a landscape frame that
is the strongest it can be, which is why it reached him as a turn.

WHY NOTHING CAUGHT IT. Two reasons, and both are about what the suite was made of rather than about
what it asserted.

  · EVERY FIXTURE WORK IS SQUARE. `tests/make_synthetic.py` writes 64x64 pictures, and
    `pass-layer.js`'s own bench road states `src: {aw: 1000, ah: 1000, bw: 1000, bh: 1000}`. A
    seating that is wrong by the frame's ratio on a portrait work is wrong by nothing at all on a
    square one at a square frame, and the fleet's door rows were driven on nothing else.
  · `tests/test_pass_door_invariant.py` STATES THE LAW BUT CANNOT SEE THIS. It reads `fit` as
    arithmetic, and says so itself: an instrument whose SHADER bypasses `uFitA` is invisible to it.
    That is exactly this class.

So this file drives the real thing: the real client, the real `declare`/`offer`, the real hang
geometry measured off the DOM, on a pair whose two works are a PORTRAIT and a LANDSCAPE photograph,
for EVERY instrument the site's own record names — never a list typed here. What it compares is the
renderer's own last frame against the DOM's own picture over the renderer's own rect, at the
project's seam threshold of 6 of 255, which is the same comparison `tests/test_pass_hang.py` makes
for three instruments and the same threshold.

WHAT THIS FILE'S FIRST WRITING GOT WRONG ABOUT GATES AND GEARS (2026-09-02). It read both of them
over the seam and named a cause in its own prose: `gates`'s `seatOf` reading `st.fitA` off the
frame state, which is the instrument's own `fit` before the host's `seated` cancels it. That was
never the cause and neither instrument was ever at fault. What reddened them was THIS FILE'S OWN
SCORE. `score_for` was handed every handle carrying a numeric default, held at that default, and
both instruments declare `dial` — the travelled number each derives from `mix` through its own
measured response curve — with `open: true`, which says exactly that a score naming no track for it
leaves the instrument doing the deriving. Named as a static rest of 0, `dial` OVERRODE `mix` and
pinned both passes at their ENTRY door for the whole run, so the frame photographed at the arriving
door was the DEPARTING work drawn into the arriving work's own box — a portrait file stretched
across a landscape hang, which is the very picture this file was written to catch and which it here
produced itself. With `open: true` handles left untracked and not one byte of either instrument
moved, gates and gears read 0.75 and 0.75 of 255 at the same door, level with the twenty-four this
file already judged. Both stand in the fleet-wide row now, and the pinned score is driven on
purpose in a row of its own so the line that repairs it cannot go quiet.

WHAT WAS LEFT OPEN, AND WHAT CLOSED IT (2026-09-02, a later pass than the one above, itself
corrected once — see below). `overlay` read over the seam at the same door, 20.25-21.5 of 255
across the runs that took it, held apart in a `read` row rather than judged because no pass had yet
gone and looked at why. It is the same defect class droste and planet carried: `pass-inst-
overlay.js`'s own frame coordinate (`p`, the coordinate FRAG's `main` builds each work's sampling
from) was squeezed by the drawing buffer's own resolution ratio (`uRes.x / uRes.y`, read via
`uRes / m`) unconditionally — a factor of the frame's own shape standing outside `uFitA`/`uFitB`,
the one channel the host's crop-cancellation (`seated` in pass-layer.js's `drawPose`) reaches. A
first repair rode that factor on `cw` (this instrument's own composite envelope) instead, which
closed this file's own row but reddened a REAL one, `tests/test_pass_overlay.py`'s row 7: that
suite drives the instrument straight off the bench, with no door simulated at all (`drawPose`'s own
`door` defaults to 0), where `uFitA`/`uFitB` carry the real, un-seated crop throughout — including
at the bench's own dominance extremes, where `cw` reads zero same as at a real door but the crop is
not seated away. Gating `p`'s own factor on `cw` there desynced it from `uFitA`/`uFitB`, which
still expected it, and stretched the very thing meant to be fixed. The repair that actually closes
both suites drops that factor from `p` entirely — FRAG's `main` now reads `p` plain — and folds the
frame's own ratio into `fit` itself, combined with the work's own, the same road droste's and
planet's own `fit` already take: `seated` already cancels exactly what `fit` returns toward
identity at a real door and hands it straight through everywhere else, a bench draw included, so
nothing needed gating on anything this file's own hand computes.

WHAT IS JUDGED, AND WHAT IS ONLY REPORTED. The ARRIVING door is judged. The departing one is read
and printed beside it but not judged, and that is measured rather than cautious: driving the
departing door needs the walk put back on the departing work, its own reveal waited out and the
pinned pass caught before it settles, and on repeated runs a control instrument whose door is exact
(`lens`) read 0.38, 1.59 and 20.43 of 255 in that column on one machine in one hour. A row that
reads three different numbers for one unchanged file measures the rig. The arriving door needs none
of that — the pass is pinned at its own end and the handoff hands the DOM over in the same task —
and it read every instrument within 0.61-0.75 of 255 across every run, so it is the column with a
verdict on it.

THE PICTURE THIS FILE HANGS is a fine checker over a coordinate ramp with a white block standing in
the work's own top-left sixth. The checker makes any shift or scale bite in a mean; the ramp says
which way each axis runs; the block says where the work's own corner went. A smooth picture would
hide the very error this file is for.
"""
import base64
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 1000, 900
DUR = 2400
RISE, FALL = 0.4, 0.9
SEAM = 6.0                      # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SIZES = {"portrait": (450, 900), "landscape": (900, 450), "square": (700, 700)}

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def read(name, detail):
    """A number this file measures and prints WITHOUT a verdict on it — the third thing this file
    does, beside judging and abstaining, and the one its own header already names ("WHAT IS JUDGED,
    AND WHAT IS ONLY REPORTED"). Until 2026-09-02 the only way to print an unjudged reading was to
    fold it into some other row's detail, as the departing door still is, and the one reading that
    wanted a row of its own was given a `check` instead — which made a permanent FAIL out of a line
    whose own text says it carries no verdict. This is not a SKIP: a SKIP says the measurement was
    never taken and is counted against the runner's own abstention ratchet, and this measurement was
    taken and is printed. It never reddens the suite."""
    results.append((name, "READ", detail))


# ---------------------------------------------------------------- the two pre-repair files
# RED-ON-BUG, BY CONSTRUCTION. Each entry turns the shipped file back into the bytes it replaced, by
# the exact substitution the repair made and nothing else. The rows below re-serve the site with the
# reversed file in place and re-drive the identical door: a row that reads green on both sets of
# bytes is measuring nothing.
PRE_REPAIR = {
    # droste: the seating went back to the module's own `flatTexel` (the fit read in the frame's own
    # height) and the flat read went back to multiplying the frame's ratio in on top of it.
    "droste": [
        ("if (ia > fa) return [fa / ia, 1, 0, 0];\n      return [1, ia / fa, 0, 0];",
         "var Sw = Math.max(fa, ia);\n      return [1 / Sw, ia / Sw, 0, 0];"),
        ("vec2 fp = uv - 0.5;", "vec2 fp = (uv - 0.5) * vec2(aspect, 1.0);"),
    ],
    # planet: the flat read went back to the cover fit the script worked out for itself, which the
    # host's own cancellation cannot reach.
    "planet": [
        ("vec2 uvFlatA = clamp(vec2(0.5 + fp.x * uFitA.x, 0.5 - fp.y * uFitA.y), 0.0, 1.0);",
         "vec2 uvFlatA = clamp(vec2(0.5 + P.x * uFlatPP.x, 0.5 - P.y * uFlatPP.y), 0.0, 1.0);"),
        ("vec2 uvFlatB = clamp(vec2(0.5 + fp.x * uFitB.x, 0.5 - fp.y * uFitB.y), 0.0, 1.0);",
         "vec2 uvFlatB = clamp(vec2(0.5 + P.x * uFlatPP.z, 0.5 - P.y * uFlatPP.w), 0.0, 1.0);"),
    ],
}


def marker(w, h, path, tint):
    x = np.linspace(0, 1, w)[None, :].repeat(h, 0)
    y = np.linspace(0, 1, h)[:, None].repeat(w, 1)
    im = np.zeros((h, w, 3), dtype=np.uint8)
    im[..., 0] = (20 + 215 * x).astype(np.uint8)
    im[..., 1] = (20 + 215 * y).astype(np.uint8)
    im[..., 2] = tint
    cx = (np.arange(w)[None, :] // 12) % 2
    cy = (np.arange(h)[:, None] // 12) % 2
    checker = ((cx + cy) % 2).astype(bool)
    im[checker] = (im[checker].astype(np.int16) + 40).clip(0, 255).astype(np.uint8)
    im[: max(1, h // 8), : max(1, w // 6)] = 255
    Image.fromarray(im).save(path)


def bake():
    """The synthetic site, with every work re-hung at one of three real shapes and the marker
    picture in place of the flat 64x64 fixture squares."""
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    out = Path(tempfile.mkdtemp(prefix="synth_doororient_"))
    build_site.OUT = out
    build_site.build(SITE_URL)
    data = json.loads((out / "exhibition_data.json").read_text())
    order = ["portrait", "landscape", "square"]
    shapes = {}
    for i, w in enumerate(data["works"]):
        kind = order[i % 3]
        shapes[w["id"]] = kind
        ww, hh = SIZES[kind]
        w["w"], w["h"] = ww, hh
        marker(ww, hh, out / w["img"].lstrip("/"), 60 + (i * 7) % 180)
    (out / "exhibition_data.json").write_text(json.dumps(data))
    gd = json.loads((out / "gallery" / "gallery_data.json").read_text())
    for it in gd["items"]:
        if it["id"] in shapes:
            it["w"], it["h"] = SIZES[shapes[it["id"]]]
    (out / "gallery" / "gallery_data.json").write_text(json.dumps(gd))
    return out, shapes


HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};0"""

DECLARE = """
  var A = document.querySelector('.exh-frame[data-id="%s"]');
  var B = document.querySelector('.exh-frame[data-id="%s"]');
  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                             kind:'step', cause:'%s', velocity:0,
                                             score: window.__doorScore});
  window.__cmd = cmd;
  var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
  return {took: !!took};
"""


def score_for(inst_id, handles, duration=DUR):
    """One cue, one instrument, `mix` on the pass's own progress and every other handle held at the
    rest its own manifest declares — so the frame at either end is that instrument's own door and
    nothing this file chose."""
    tracks = {"mix": {"node": "prog"}, "clock": {"node": "sec"}}
    nodes = {"prog": {"source": "progress"}, "sec": {"source": "time"}}
    for h, v in handles.items():
        if h in ("mix", "clock"):
            continue
        tracks[h] = {"node": "rest:" + h}
        nodes["rest:" + h] = {"op": "static", "value": v}
    return {
        "schema": 2,
        "intent": "one instrument, both doors, on a mixed-orientation pair",
        "pair": {"a": "a", "b": "b"},
        "seed": 3,
        "duration": duration,
        "interruption": {"withinMs": 200, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b", "track": [],
                   "hang": {"rise": RISE, "fall": FALL}},
        "cues": [{
            "id": "door-main",
            "instrument": {"id": inst_id, "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "assembly"],
            "levels": ["SURFACE", "CELL"],
            "window": [0, duration / 1000.0],
            "works": ["a", "b"],
            "cameraAuthority": "stage",
            "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                      "out": {"handle": "mix", "value": 1, "measured": True}},
            "nodes": nodes,
            "tracks": tracks,
        }],
        "provenance": {"source": "tests/test_pass_door_orientation.py",
                       "measuredAt": "2026-09-01", "by": "the mixed-orientation door rows"},
    }


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return path


def canvas_box(br):
    return js(br, "var c=document.querySelector('canvas');if(!c)return null;"
                  "var b=c.getBoundingClientRect();"
                  "return {x:b.left,y:b.top,w:b.width,h:b.height,vis:c.style.visibility};")


def crop_of(path, box, s, inset=2):
    im = Image.open(path).convert("RGB")
    x0 = max(0, int(round(box["x"] * s)) + inset)
    y0 = max(0, int(round(box["y"] * s)) + inset)
    x1 = min(im.width, int(round((box["x"] + box["w"]) * s)) - inset)
    y1 = min(im.height, int(round((box["y"] + box["h"]) * s)) - inset)
    if x1 - x0 < 8 or y1 - y0 < 8:
        return None
    return im.crop((x0, y0, x1, y1))


def apart(a, b):
    if a is None or b is None or a.size != b.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, b))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def wait_state(br, want, tries=120):
    for _ in range(tries):
        if js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(0.05)
    return False


def rest_at(br, a):
    js(br, "window.__exPass.adapter.interrupt('rest'); return null;")
    wait_state(br, "idle")
    for _ in range(10):
        js(br, "var A=document.querySelector('.exh-frame[data-id=\"%s\"]');"
               "A.classList.add('seen');"
               "scrollTo(0, Math.round(scrollY + A.getBoundingClientRect().top"
               " + (A.getBoundingClientRect().height - innerHeight)/2)); return null;" % a)
        br.sleep(0.35)
        top = float(js(br, "return document.querySelector('.exh-frame[data-id=\"%s\"]')"
                           ".getBoundingClientRect().top;" % a))
        if abs(top) < 3:
            break
    for _ in range(40):
        op = js(br, "var I=document.querySelector('.exh-frame[data-id=\"%s\"] img.work');"
                    "return I ? Number(getComputedStyle(I).opacity) : 1;" % a)
        if op >= 0.999:
            return True
        br.sleep(0.1)
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
    for _ in range(40):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            br.evaluate(HOOKS)
            return True
        br.sleep(0.2)
    return False


def pick_pair(ids, shapes):
    for i in range(len(ids) - 1):
        a, b = ids[i], ids[i + 1]
        if {shapes.get(a), shapes.get(b)} == {"portrait", "landscape"}:
            return a, b
    for i in range(len(ids) - 1):
        a, b = ids[i], ids[i + 1]
        if shapes.get(a) != shapes.get(b):
            return a, b
    return None


def drive(site, shapes, only=None, shots=None, pin_open=False):
    """Every instrument the record names, driven through both real doors on a mixed-orientation
    pair. Answers {name: (depart, arrive)} where each is `(mean, worst)` of 255 or None.

    `pin_open` puts the score back the way this file first wrote it — every handle carrying a
    numeric default held at that default, an `open: true` handle included. It exists for one row,
    and the reason it is a row rather than a deleted mistake stands at A HANDLE THE INSTRUMENT
    DERIVES FOR ITSELF below."""
    out = {}
    with serve(site) as base, Browser(width=VW, height=VH) as br:
        br.set_viewport(VW, VH)
        br.navigate(base + "/")
        if not enter(br):
            return None
        names = js(br, "return window.__exPass.host.report().record.names;")
        if only:
            names = [n for n in names if n in only]
        # WARMED FIRST, AND THAT IS THE RIG'S OWN NEED. The first pass of a session pays for the
        # instrument fetch, the programme build and the walk's own first settle; whatever stands
        # first in the list reads its departing door through all three.
        names = names[:1] + names
        js(br, "window.__exPass.bench.load(%s, function(){window.__warm=1;}); return null;"
               % json.dumps(names))
        for _ in range(200):
            if br.evaluate("String(!!window.__warm)") == "true":
                break
            br.sleep(0.1)
        manifests = js(br, "var out={}; %s.forEach(function(n){"
                           " var m=window.__exPass.bench.manifest(n);"
                           " out[n]= m ? {handles: m.handles||null} : null;}); return out;"
                       % json.dumps(names))
        ids = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame[data-id]'))"
                     ".map(function(f){return f.getAttribute('data-id');});")
        pair = pick_pair(ids, shapes)
        if pair is None:
            return None
        A, B = pair
        out["__pair__"] = (A, shapes[A], B, shapes[B])
        for n in names:
            handles = {}
            for h, spec in ((manifests.get(n) or {}).get("handles") or {}).items():
                if not (isinstance(spec, dict) and isinstance(spec.get("def"), (int, float))):
                    continue
                # A HANDLE THE INSTRUMENT DERIVES FOR ITSELF IS LEFT UNTRACKED, and that is what
                # «every other handle held at the rest its own manifest declares» has to mean once
                # a manifest declares `open: true` on one. That word says the instrument works the
                # number out from another handle unless a score names a track for it — `gates` and
                # `gears` both carry it on `dial`, the travelled number each derives from `mix`
                # through its own measured response curve, and `weave` carries it on `turn` and
                # `bal`. Naming such a handle at its own rest does NOT hold the instrument still at
                # a rest: it overrides the walk. Both gates and gears read `dial` first and fall
                # back to `mix` only where no track named it, so the score this file first wrote —
                # `dial` static at 0 while `mix` walked the pass's own progress — pinned both at
                # their ENTRY door for the whole run, and the frame photographed at the arriving
                # door was the DEPARTING work drawn into the arriving work's own box.
                #
                # MEASURED 2026-09-02, on this file's own pair and door, with no instrument byte
                # moved: 28.31 and 28.31 of 255 with the handle pinned, 0.75 and 0.75 with this one
                # line in place, against a control (`lens`) that read 0.75 either way. The row
                # named RED_SCORE below drives the pinned score on purpose, so a line that stopped
                # mattering would be caught rather than quietly kept.
                if spec.get("open") is True and not pin_open:
                    continue
                handles[h] = spec["def"]
            sc = score_for(n, handles)
            if js(br, "return window.__exPass.bench.scoreWhyNo(%s);" % json.dumps(sc)):
                out[n] = (None, None)
                continue
            br.evaluate("window.__doorScore = " + json.dumps(sc) + "; 0")

            rest_at(br, A)
            br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:2000,"
                        " clockPin:0, progressPin:0, fixedScale:true}); 0")
            before = png(br, shots / (n + "-depart-dom.png"))
            scale = Image.open(before).width / float(br.evaluate("String(innerWidth)"))
            r = js(br, DECLARE % (A, B, n + "-depart"))
            running = wait_state(br, "running")
            br.sleep(0.5)
            box = canvas_box(br)
            after = png(br, shots / (n + "-depart-canvas.png"))
            depart = None
            if r["took"] and running and box and box["vis"] == "visible":
                depart = apart(crop_of(before, box, scale), crop_of(after, box, scale))
            js(br, "window.__exPass.adapter.interrupt('d'); return null;")
            wait_state(br, "idle")
            br.sleep(0.2)

            rest_at(br, A)
            br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400, settleSlackMs:4000,"
                        " clockPin:%f, progressPin:1, fixedScale:true}); 0" % (DUR / 1000.0))
            r2 = js(br, DECLARE % (A, B, n + "-arrive"))
            running2 = wait_state(br, "running")
            br.sleep(0.6)
            box2 = canvas_box(br)
            canvas_shot = png(br, shots / (n + "-arrive-canvas.png"))
            js(br, "window.__exPass.adapter.handoff(window.__cmd);"
                   "window.__exPass.bench.show(false); return null;")
            br.sleep(0.4)
            dom_shot = png(br, shots / (n + "-arrive-dom.png"))
            arrive = None
            if r2["took"] and running2 and box2:
                arrive = apart(crop_of(canvas_shot, box2, scale), crop_of(dom_shot, box2, scale))
            js(br, "window.__exPass.adapter.interrupt('a'); return null;")
            wait_state(br, "idle")
            br.sleep(0.2)
            out[n] = (depart, arrive)
    return out


ROW = "PASS-DOOR-ORIENT · %s's arriving door stands the whole work on a mixed-orientation pair"
RED = ("PASS-DOOR-ORIENT red-on-bug · %s's pre-repair seating reddens the same door on the same "
       "pair")
RED_SCORE = ("PASS-DOOR-ORIENT red-on-bug · the pre-repair score, pinning the handle gates derives "
             "for itself, reddens the same door on the same pair")

if not chrome_available():
    for n in ("every instrument", "droste", "planet"):
        skip(ROW % n, "no headless Chrome on this machine")
else:
    SITE, SHAPES = bake()
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_doororient_shots_"))
    try:
        got = drive(SITE, SHAPES, shots=SHOTS)
        if not got:
            skip(ROW % "every instrument", "the walk never handed the renderer a frame")
        else:
            a, ash, b, bsh = got.pop("__pair__")
            # NOTHING IS HELD APART ANY MORE. `gates` and `gears` stood in a row of their own until
            # 2026-09-02 and stand in this one now: neither ever carried a seating fault, and what
            # reddened them was this file's own score pinning the `dial` each declares `open: true`
            # (A HANDLE THE INSTRUMENT DERIVES FOR ITSELF, in `drive` above). `overlay` stood in a
            # row of its own after that, read but not judged at 20.25-21.5 of 255 — its own frame
            # coordinate squeezed one axis by the canvas's own resolution ratio, a factor riding
            # nothing (§8's `cw`, the one envelope every other axis of this frame hangs on already
            # shuts it at both doors) and so surviving past the host's own crop-cancellation, the
            # same class droste and planet carried. Fixed in pass-inst-overlay.js by putting that
            # factor on `cw` with the rest, it now reads inside the same seam every other instrument
            # passes at and stands in this one row too.
            over = {n: round(v[1][0], 2) for n, v in got.items()
                    if v[1] is not None and v[1][0] > SEAM}
            unread = [n for n, v in got.items() if v[1] is None]
            worst = max(((v[1][0], n) for n, v in got.items() if v[1] is not None),
                        default=(0.0, "-"))
            check(ROW % "every instrument",
                  not over,
                  "%d instruments driven through a real arriving door, %s(%s) -> %s(%s), at a "
                  "%dx%d frame. Over the %.1f-of-255 seam: %s. The worst of the rest read %.2f on "
                  "%s. Unread (the pass never took the frame, which is the rig and not a seating): "
                  "%s. The departing door, read but not judged, stood at %s."
                  % (len(got), a, ash, b, bsh, VW, VH, SEAM, over or "none",
                     worst[0], worst[1], unread or "none",
                     {n: (round(v[0][0], 2) if v[0] else None) for n, v in sorted(got.items())}))

            # ---- red-on-bug: the score this file first wrote ----------------------------------
            # THE REPAIR THIS BRANCH MADE IS THIS FILE'S OWN — no instrument byte moved — so it is
            # proved the way the two file repairs below are proved: by driving the identical door
            # with the pre-repair score put back and reading it red. `gates` is the instrument
            # driven because `dial` is the handle that score pinned and because it is the row the
            # branch was opened on; `gears` reddens by the same line and needs no second browser to
            # say so.
            site3, shapes3 = bake()
            shots3 = Path(tempfile.mkdtemp(prefix="synth_doororient_prescore_"))
            try:
                back = drive(site3, shapes3, only={"gates"}, shots=shots3, pin_open=True)
                row = (back or {}).get("gates")
                now = got.get("gates")
                check(RED_SCORE,
                      bool(row) and row[1] is not None and row[1][0] > SEAM,
                      "gates driven with `dial` held at its own rest of 0 while `mix` walked the "
                      "pass's own progress, arriving door against the DOM's own picture: %s of "
                      "255, against the same %.1f-of-255 threshold the same unmoved file passes "
                      "at %s once the handle it declares `open: true` is left untracked"
                      % (("%.2f" % row[1][0]) if row and row[1]
                         else "the pass never took the frame",
                         SEAM,
                         ("%.2f" % now[1][0]) if now and now[1] else "-"))
            finally:
                shutil.rmtree(shots3, ignore_errors=True)
                shutil.rmtree(site3, ignore_errors=True)

            # ---- red-on-bug: the same door, on the bytes each repair replaced ------------------
            # The substitution is made on the BUILT file the site actually serves, so what is driven
            # is the artifact a visitor is handed with one seating turned back and nothing else
            # touched. A row whose anchor has gone says so and skips, rather than quietly reversing
            # nothing and reading green.
            for name, subs in PRE_REPAIR.items():
                site2, shapes2 = bake()
                served = site2 / ("pass-inst-%s.js" % name)
                text = served.read_text(encoding="utf-8")
                missed = [old for old, _ in subs if text.count(old) != 1]
                if missed:
                    shutil.rmtree(site2, ignore_errors=True)
                    skip(RED % name,
                         "the served file no longer carries exactly one of the lines this row "
                         "reverses, so the row cannot state what it would be reversing: %r"
                         % missed[0][:90])
                    continue
                for old, new in subs:
                    text = text.replace(old, new, 1)
                served.write_text(text, encoding="utf-8")
                # THE RECORD WEIGHS THE BYTES IT SERVES. The site's own settings record carries a
                # sha256 of each instrument file and the host refuses a file that does not weigh to
                # it (`fileWhyNo` in pass-layer.js) — so a row that edits a served file and leaves
                # the record alone measures the refusal and not the picture. Re-stamped here the
                # same way `engine/build.py` stamps it: over the bytes actually written.
                cfg_path = site2 / "config.json"
                cfg = json.loads(cfg_path.read_text())
                cfg["pass"]["instruments"][name]["digest"] = hashlib.sha256(
                    served.read_bytes()).hexdigest()
                cfg_path.write_text(json.dumps(cfg, indent=2, sort_keys=True))
                shots2 = Path(tempfile.mkdtemp(prefix="synth_doororient_pre_"))
                try:
                    back = drive(site2, shapes2, only={name}, shots=shots2)
                    row = (back or {}).get(name)
                    now = got.get(name)
                    check(RED % name,
                          bool(row) and row[1] is not None and row[1][0] > SEAM,
                          "pre-repair %s, arriving door against the DOM's own picture: %s of 255, "
                          "against the same %.1f-of-255 threshold the shipped file passes at %s"
                          % (name,
                             ("%.2f" % row[1][0]) if row and row[1]
                             else "the pass never took the frame",
                             SEAM,
                             ("%.2f" % now[1][0]) if now and now[1] else "-"))
                finally:
                    shutil.rmtree(shots2, ignore_errors=True)
                    shutil.rmtree(site2, ignore_errors=True)
    finally:
        shutil.rmtree(SHOTS, ignore_errors=True)
        shutil.rmtree(SITE, ignore_errors=True)

print(__doc__.strip().splitlines()[0])
print()
bad = 0
for name, verdict, detail in results:
    print("[%s] %s" % (verdict, name))
    if detail:
        print("        " + detail)
    if verdict == "FAIL":
        bad += 1
print()
print("%d passed / %d failed / %d skipped / %d read without a verdict"
      % (sum(1 for r in results if r[1] == "PASS"), bad,
         sum(1 for r in results if r[1] == "SKIP"),
         sum(1 for r in results if r[1] == "READ")))
sys.exit(1 if bad else 0)
