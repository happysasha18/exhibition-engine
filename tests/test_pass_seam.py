#!/usr/bin/env python3
"""EX-SEAM — the seam check: every handoff a passage has, photographed on both sides.
Run: python3 tests/test_pass_seam.py

Root: the crossing charter's build ladder, step 1, clause (b) — "the SEAM CHECK joins the suite:
headless frames captured just before and just after every handoff must near-match pixel-wise, a
visible jump is a red — continuity becomes a red/green test instead of a hope".

Of that step's three enforcement clauses only the first held: no opacity handle reaches a plan. This
file is the second. It is a red/green over EVERY handoff a passage has, not only its last one:

  1. the curtain going up            the walk's own DOM hands the frame to the renderer
  2. a cue entering through its door a voice joins the stack at its window's own open
  3. a cue leaving through its door   a voice stands down at its window's own close
  4. the level handover              one voice leaves a structural level as another takes it
  5. the frame given back            the renderer hands the frame to the still picture at the end
  6. the cadence landing on a door   an interruption resolves and hands the frame back

WHAT MAKES THIS MEASURABLE AT ALL, AND IT IS THE WHOLE DESIGN. A handoff is a change of AUTHORITY,
not a change of picture. Four of the six happen inside one running passage, and the host's frame loop
can be PINNED — `clockPin` and `progressPin` stop it reading the wall clock, which is what lets one
instant be photographed twice. So each of those handoffs is photographed at the pinned instant just
under its own edge and just over it, at a clock separation of one millisecond of the passage's own
2.4-second span. Across that separation the passage's own motion is nil; what changes is which voice
holds the frame. The measurement is therefore of the authority change ALONE, and no model of the
passage's motion enters it. The remaining two cross from the DOM to the canvas and back, and those
are already one instant seen through two renderers.

THE TOLERANCE, ARGUED FROM THE MECHANISM RATHER THAN CHOSEN.

  What can a lawful handoff legitimately change? Only the resampling. The two sides of a handoff are
  the same picture — that is what continuity means — carried by two authorities that may lay it on
  the grid a fraction of a pixel apart: a WebGL cover fit and the browser's own image scaler at the
  two ends, and one voice's own sampling against another's in the middle. Every resampling filter in
  use — box, bilinear, bicubic's positive lobe, the GPU's own — writes each output pixel as a
  weighted average of the input pixels around it. A weighted average of a set of numbers lies
  BETWEEN the smallest and the largest of them.

  So the bound writes itself, and it carries no number: after a lawful handoff, every pixel must lie
  inside the range its own immediate neighbourhood spanned before it. Formally, for pixel p and
  channel c, `after(p,c)` must fall within [min, max] of `before` over p's own 3x3 neighbourhood —
  and, because either side may be the resampled one, it is enough that ONE of the two directions
  explains it. What is reported is the EXCESS: how far outside that range the pixel fell, in the
  picture's own 0-255 units. A sub-pixel shift, a slight scale, a change of filter and a different
  gamma ramp all land at zero excess. A picture flipping to another picture does not, because a work
  that is not there cannot be a weighted average of the work that was.

  THE FLOOR IS MEASURED ON THIS BENCH, NOT WRITTEN DOWN. Row 0 photographs one pinned instant twice
  through one renderer with nothing whatever changed between the two shots, and reads the excess.
  Whatever that reads is what two identical pictures cost on this machine, and it is the bar every
  other row is held to. Nothing here is set to make today's code pass: if a handoff exceeds the
  bench's own floor, that is the finding.

  AND THE CHECK IS HELD AGAINST VACUITY. The last row hands the very same predicate two instants a
  passage apart. If it cannot tell those apart, it can tell nothing apart, and every green above it
  is worthless.

WHAT REGION IS COMPARED. The region the renderer actually claims at that instant — the canvas's own
rect, read live off the DOM. Outside it the passage claims nothing and the walk's own chrome is free
to differ; the chrome is separately choreographed and is not part of the crossing's continuity. In
the middle of a passage that rect IS the whole viewport, so a middle handoff is judged over every
pixel on the screen.
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
# THE PASSAGE THIS FILE MEASURES, in milliseconds, and it is long ON PURPOSE. The host ends a
# transaction that has not settled at its own duration plus the settle slack, and the slack is capped
# at 2000 ms — so a passage of ordinary length gives a bench about two seconds of wall clock to work
# in. The door rows walk the pin across three window edges of ONE passage and photograph both sides
# of each, which costs more wall clock than that, and a passage cut short under them would have them
# reading a walk that had already landed rather than a handoff. The pin is what makes the length
# free: the picture is a function of the pinned second and not of the wall clock, so lengthening the
# passage buys the bench time and changes nothing it measures. 12 s sits inside the host's own
# DURATION_MAX of 14 s and leaves the watchdog 14 s out.
DUR = 12000
RISE, FALL = 2.0, 4.5      # the score's own rise and fall, in seconds
# THE CLOCK SEPARATION THE TWO SHOTS OF A HANDOFF STRADDLE IT BY, in seconds of the passage's own
# clock. It is not a frame interval and it is not a wait: the frame loop is PINNED, so this is simply
# how far either side of the edge the pinned instant is set, and it should be as small as the
# arithmetic allows.
#
# WHY IT HAS TO BE THIS SMALL RATHER THAN MERELY SMALL. Both shots of a pair stand at one pinned
# PROGRESS, so every handle driven by the passage's progress is identical across them. A handle
# driven by a cue's OWN progress is not: `cueProgress` is derived from the second, so it moves by the
# straddle divided by the cue's own window. At a millisecond that came to some tens of millionths of
# a cue's window — enough for a voice a hair past its own door to draw at a few parts in a hundred
# thousand of its strength, which the picture still quantises to one or two of 255 and which the
# floor of zero then reads as a step. It is not a step: it is the crossing legitimately having begun.
# A microsecond puts that motion below the picture's own quantisation, so what the pair carries is
# the change of authority and nothing else, which is what the rows below claim to measure.
STRADDLE = 0.000001
# The windows of the two upper voices. `first` opens at OPEN, hands the TEXTURE level to `second` at
# HANDOVER, and `second` closes at CLOSE — so one score carries a door opening, a door closing and a
# level handover, each at a second of its own.
OPEN, HANDOVER, CLOSE = 3.0, 6.0, 9.0
# Where the interruption row cuts in. Early enough that the cadence's nearest door is the departing
# one, so the row measures a cadence that walks somewhere rather than one already standing still.
CUT_AT = 1.5

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score

def ground_cue(dur):
    """The lowest voice: it fills the frame, so the coverage law puts it at the bottom of the stack
    and nothing may stand under it. Every handle is on a track, so the picture is a function of the
    pinned progress alone."""
    return {
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
    }


def overlay_cue(cid, w0, w1, dry=None):
    """A voice standing OVER the ground, entering and leaving AT ITS OWN NEUTRAL.

    `overlay` declares `presence` — "the share of the frame the exposure stands on" — and at zero its
    region covers nothing at all, so the voice is present in the stack and contributes no pixel. That
    is the DRY of the charter's step-0 module contract, and it is what lets a voice join a running
    picture without replacing it. The handle is driven by a spline over the cue's OWN progress: zero
    at the window's open, whole across its middle, zero again at its close — so both of this cue's
    doors are a frame in which it draws nothing, and crossing either of them is an authority change
    and nothing else."""
    return {
        "id": cid, "instrument": {"id": "overlay", "api": 1}, "voice": "letter",
        "roles": ["assembly"], "levels": ["TEXTURE"], "stack": 1,
        "window": [w0, w1], "works": ["a", "b"], "cameraAuthority": "stage",
        "doors": {"in": {"handle": "presence", "value": 0, "measured": True},
                  "out": {"handle": "presence", "value": 0, "measured": True}},
        "nodes": {"sec": {"source": "time"}, "zero": {"op": "static", "value": 0},
                  "one": {"op": "static", "value": 1},
                  "dial": {"source": "cueProgress"},
                  "arc": {"op": "spline", "in": {"source": "cueProgress"},
                          "points": [{"at": 0, "value": 0}, {"at": 0.5, "value": 1},
                                     {"at": 1, "value": 0}]}},
        "tracks": {"mix": {"node": "dial"}, "clock": {"node": "sec"},
                   "presence": {"node": dry or "arc"}, "exposure": {"node": "one"},
                   "turn": {"node": "zero"}, "arrival": {"node": "zero"},
                   "mixTurn": {"node": "zero"}, "regionTurn": {"node": "zero"},
                   "mask": {"node": "zero"}},
    }


def beat_cue(cid, w0, w1, dry=None):
    """The second voice of the level handover, entering and leaving at the reserved dry.

    `beat` is the kind of voice the fleet is mostly made of: a letter that always drew something,
    whose entry door was `mix` at 0 — the departing work whole — so that standing over a ground it
    had no state in which it was merely present. The entry-door contract gives it `presence`, the
    one name the whole fleet declares: at zero it draws nothing anywhere and what stands beneath it
    shows whole. Both of this cue's doors are named on it, and it is driven by a spline over the
    cue's own progress — zero at the window's open, whole across its middle, zero again at its
    close."""
    return {
        "id": cid, "instrument": {"id": "beat", "api": 1}, "voice": "letter",
        "roles": ["assembly"], "levels": ["TEXTURE"], "stack": 1,
        "window": [w0, w1], "works": ["a", "b"], "cameraAuthority": "stage",
        "doors": {"in": {"handle": "presence", "value": 0, "measured": True},
                  "out": {"handle": "presence", "value": 0, "measured": True}},
        "nodes": {"sec": {"source": "time"}, "zero": {"op": "static", "value": 0},
                  "dial": {"source": "cueProgress"},
                  "arc": {"op": "spline", "in": {"source": "cueProgress"},
                          "points": [{"at": 0, "value": 0}, {"at": 0.5, "value": 1},
                                     {"at": 1, "value": 0}]}},
        "tracks": {"mix": {"node": "dial"}, "clock": {"node": "sec"}, "seed": {"node": "zero"},
                   "mask": {"node": "zero"}, "presence": {"node": dry or "arc"}},
    }


def score(within=200, dry=None):
    dur = DUR / 1000.0
    return {
        "schema": 2,
        "intent": "the seam check: every handoff a passage has, photographed on both sides",
        "pair": {"a": "a", "b": "b"}, "seed": 3, "duration": DUR,
        "interruption": {"withinMs": within, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b", "track": [],
                   "hang": {"rise": RISE, "fall": FALL}},
        "cues": [ground_cue(dur),
                 overlay_cue("first", OPEN, HANDOVER, dry),
                 beat_cue("second", HANDOVER, CLOSE, dry)],
        "provenance": {"source": "tests/test_pass_seam.py", "measuredAt": "2026-08-25",
                       "by": "the seam rows"},
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passseam_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

# THE STRUCTURAL READING BEHIND THE DOOR ROWS, taken off the manifests rather than off a picture.
# A voice may stand OVER another only if its instrument declares `coverage.writes: true` — it does
# not fill the frame. Of those, a voice can join a running picture WITHOUT replacing it only if it
# also declares a handle whose zero means it contributes nothing; the charter's step-0 module
# contract calls that the effect's DRY, and its own diagnosis of the shipped modules was that "every
# module is built permanently 100% wet, which is why layers could only crossfade". This row names
# which instruments of the fleet carry such a handle and which do not, so the door rows below read
# against a fact rather than against a guess.
ZERO_STATE_HANDLES = ("presence",)


def dry_reading():
    """Per instrument that may stand above another voice: whether it declares a state in which it
    draws nothing at all."""
    import re
    wet, dry = [], []
    for p in sorted((ROOT / "engine" / "assets").glob("pass-inst-*.js")):
        src = p.read_text(encoding="utf-8")
        name = p.name[len("pass-inst-"):-3]
        m = re.search(r"coverage: *\{\s*writes: *(true|false)", src)
        if not m or m.group(1) != "true":
            continue          # it fills the frame, so it stands lowest and covers whatever it likes
        i, j = src.find("handles:"), src.find("coverage:")
        block = src[i:j] if 0 <= i < j else src
        (dry if any(("%s: {" % h) in block for h in ZERO_STATE_HANDLES) else wet).append(name)
    return dry, wet


check("EX-SEAM no plan can fade a layer: the engine exposes no opacity handle",
      ".style.opacity" not in LAYER and "function doorBridge(" not in LAYER,
      "the ladder's first enforcement clause, which already held and is held here beside the second")

check("EX-SEAM the frame loop can be pinned, which is what makes one instant photographable twice",
      "pinClock" in LAYER and "pinProgress" in LAYER
      and "seconds = pinClock !== null ? pinClock" in LAYER,
      "the seam rows below stand entirely on this: a handoff straddled at a pinned instant is an "
      "authority change with no motion in it")

_DRY, _WET = dry_reading()
check("EX-SEAM every voice that may stand over another declares a state in which it draws nothing",
      bool(_DRY) and not _WET,
      "a voice can join a running picture without replacing it only where its instrument names a "
      "handle whose zero means it contributes nothing — the charter's step-0 DRY. Carrying one: "
      + (", ".join(_DRY) or "none") + ". Carrying none, so their entry door is the departing work "
      "whole and opening their window puts one picture where another stood: "
      + (", ".join(_WET) or "none"))

# ---------------------------------------------------------------- the predicate

def arr(path):
    from PIL import Image
    import numpy as np
    return np.asarray(Image.open(path).convert("RGB")).astype(np.int16)


def _band(x):
    """The range each pixel's own 3x3 neighbourhood spans, per channel."""
    import numpy as np
    h, w, _ = x.shape
    pad = np.pad(x, ((1, 1), (1, 1), (0, 0)), mode="edge")
    views = [pad[dy:dy + h, dx:dx + w] for dy in (0, 1, 2) for dx in (0, 1, 2)]
    return np.minimum.reduce(views), np.maximum.reduce(views)


def _excess(a, b):
    """How far each pixel of `b` falls outside the range `a`'s own neighbourhood spanned — zero
    wherever `b` could be a resampling of `a`, because every resampling filter writes an output
    pixel as a weighted average of the input pixels around it and an average lies between them."""
    import numpy as np
    lo, hi = _band(a)
    return np.maximum(np.maximum(b - hi, lo - b), 0)


def resample_excess(pa, pb):
    """The reading a seam is judged on. Either side may be the resampled one, so a pixel is lawful
    if EITHER direction explains it, and what is reported is the smaller of the two excesses."""
    import numpy as np
    a, b = arr(pa), arr(pb)
    if a.shape != b.shape:
        return {"worst": 255, "share": 1.0, "mean": 255.0, "why": f"{a.shape} vs {b.shape}"}
    e = np.minimum(_excess(a, b), _excess(b, a))
    return {"worst": int(e.max()), "share": round(float((e.max(axis=2) > 0).mean()), 6),
            "mean": round(float(e.mean()), 6), "why": None}


# ---------------------------------------------------------------- browser plumbing

HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};
0"""


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def canvas_box(br):
    return js(br, "var c=document.querySelector('canvas');"
                  "if(!c) return null;"
                  "var b=c.getBoundingClientRect();"
                  "return {x:b.left, y:b.top, w:b.width, h:b.height,"
                  " iw:innerWidth, ih:innerHeight, vis:c.style.visibility};")


def shot_scale(br, path):
    from PIL import Image
    return Image.open(path).size[0] / float(br.evaluate("String(innerWidth)"))


def crop_of(path, box, scale, inset=2):
    """Both shots cropped to the same region in shot pixels. The inset drops the outermost ring of
    the rect: at the very edge the renderer's own bilinear sample and the browser's image scaler
    read half a point differently, and that ring says nothing about the seam."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    x0 = int(round(box["x"] * scale)) + inset
    y0 = int(round(box["y"] * scale)) + inset
    x1 = int(round((box["x"] + box["w"]) * scale)) - inset
    y1 = int(round((box["y"] + box["h"]) * scale)) - inset
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(im.size[0], x1), min(im.size[1], y1)
    if x1 - x0 < 4 or y1 - y0 < 4:
        return None
    return im.crop((x0, y0, x1, y1))


def cropped_excess(pa, pb, box, scale, shots, tag):
    """The predicate, applied over the region the renderer claims."""
    ca, cb = crop_of(pa, box, scale), crop_of(pb, box, scale)
    if ca is None or cb is None:
        return {"worst": 255, "share": 1.0, "mean": 255.0, "why": "the claimed rect is too small"}
    a_p, b_p = shots / (tag + "-a.png"), shots / (tag + "-b.png")
    ca.save(a_p)
    cb.save(b_p)
    out = resample_excess(a_p, b_p)
    out["size"] = ca.size
    return out


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
            return True
        br.sleep(0.2)
    return False


def rest_revealed(br, a, tries=40, nap=0.1):
    """Wait until the resting work's own reveal has finished — the picture stands at full strength,
    not part way up its fade. A row comparing the renderer's pixels against a half-faded photograph
    would be reading the fade rather than the seam."""
    for _ in range(tries):
        op = js(br, "var I=document.querySelector('.exh-frame[data-id=\"%s\"] img.work');"
                    "return I ? Number(getComputedStyle(I).opacity) : 1;" % a)
        if op >= 0.999:
            return True
        br.sleep(nap)
    return False


def rest_at(br, a):
    """The walk put back on the departing work, its picture centred in the frame, nothing in flight
    and the reveal finished. Without the scroll the work hangs off the top of the viewport and the
    rect the renderer claims lies outside the shot entirely."""
    js(br, "window.__exPass.adapter.interrupt('seam-rest'); return null;")
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
            return rest_revealed(br, a)
    return False


def pin(br, seconds, progress):
    br.evaluate("window.__exPass.host.configure({clockPin:%r, progressPin:%r}); 0"
                % (seconds, progress))


def offer(br, a, b, cause, sc):
    return js(br, """
      window.__seamScore = %s;
      var A = document.querySelector('.exh-frame[data-id="%s"]');
      var B = document.querySelector('.exh-frame[data-id="%s"]');
      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                 kind:'step', cause:'%s', velocity:0,
                                                 score: window.__seamScore});
      window.__cmd = cmd;
      var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
      return {got: !!cmd, took: took, gen: cmd ? cmd.gen : null};
    """ % (json.dumps(sc), a, b, cause))


def live_at(br):
    return js(br, "var r = window.__exPass.host.report();"
                  "return {live: r.live, drew: r.drew, state: r.state,"
                  " stack: (r.stack||[]).map(function(s){return s.id + '/' + s.instrument"
                  "         + (s.live ? '/live' : '/held');}),"
                  " shed: r.events.filter(function(e){"
                  "   return e.name === 'voice-shed' || e.name === 'score-shed'"
                  "       || e.name === 'no-instrument' || e.name === 'plan-lightened';})"
                  "   .map(function(e){return e.name + ': ' + e.why;}),"
                  " last: r.events.slice(-6).map(function(e){return e.name + ': ' + e.why;})};")


# ---------------------------------------------------------------- rows

ROWS = [
    "EX-SEAM row 0 · the bench's own floor: one pinned instant photographed twice reads no excess",
    "EX-SEAM row 0b · the floor for a voice joining at no presence at all, which costs a draw call",
    "EX-SEAM handoff 1 · the curtain goes up: the renderer's first frame is the walk's own picture",
    "EX-SEAM handoff 2 · a cue enters through its own door and the picture does not step",
    "EX-SEAM handoff 3 · a cue leaves through its own door and the picture does not step",
    "EX-SEAM handoff 4 · one voice hands a structural level to another with no step in the picture",
    "EX-SEAM handoff 5 · the frame given back to the still picture at the end",
    "EX-SEAM handoff 6 · the interruption cadence lands on a door and hands the frame back",
    "EX-SEAM the check is not vacuous: two instants of one passage are no resampling of one another",
]


if not chrome_available():
    for r in ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_seamshots_"))
    FLOOR = {"worst": None}
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
                    SC = score()

                    # ---- row 0 · the floor this bench itself sets ------------------------
                    # One pinned instant, photographed twice, with NOTHING changed between the two
                    # shots — not the clock, not the progress, not the authority. Whatever this
                    # reads is what two identical pictures cost here, and it is the bar every row
                    # below is held to.
                    rest_at(br, A)
                    br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                                " settleSlackMs:2000, fixedScale:true}); 0")
                    pin(br, HANDOVER + STRADDLE, (HANDOVER + STRADDLE) / (DUR / 1000.0))
                    r0 = offer(br, A, B, "seam-floor", SC)
                    running = wait_state(br, "running")
                    br.sleep(1.0)
                    box0 = canvas_box(br)
                    scale = shot_scale(br, png(br, SHOTS / "scale.png"))
                    p1 = png(br, SHOTS / "floor-1.png")
                    br.sleep(0.25)
                    p2 = png(br, SHOTS / "floor-2.png")
                    if not (r0["took"] and running and box0):
                        check(ROWS[0], False, f"the passage never took the frame: {r0} "
                                              f"running={running} box={box0}")
                    else:
                        f = cropped_excess(p1, p2, box0, scale, SHOTS, "floor")
                        FLOOR["worst"] = f["worst"]
                        check(ROWS[0], f["worst"] is not None,
                              f"one instant photographed twice over the renderer's own rect "
                              f"{f.get('size')}: worst excess {f['worst']} of 255, "
                              f"{f['share'] * 100:.4f}% of pixels outside their own neighbourhood "
                              f"range. This is the bar every seam below is held to")
                    js(br, "window.__exPass.adapter.interrupt('floor-done'); return null;")
                    wait_state(br, "idle")

                    bar = FLOOR["worst"] if FLOOR["worst"] is not None else 0

                    dur = DUR / 1000.0
                    def straddle(tag, at, prog=None, sc=None):
                        """One window edge, photographed on both sides of itself.

                        EACH EDGE GETS ITS OWN OFFER. A passage the host ends part way — a voice
                        whose own door proof refuses it, say — would leave every later reading
                        photographing a walk that had already landed, and a row cannot tell that
                        from a seam. A fresh passage per edge means each reading either stands on a
                        live passage or says plainly that it did not.

                        ONE PROGRESS, TWO SECONDS. Every handle of the passage is a function of
                        progress, and the clock is what decides which voice holds the frame — so
                        both shots stand at one progress and differ only in the second. Nothing of
                        the passage's own motion is in the reading; the change of authority is."""
                        rest_at(br, A)
                        p_at = at / dur if prog is None else prog
                        pin(br, at - STRADDLE, p_at)
                        got = offer(br, A, B, "seam-" + tag, sc or SC)
                        live = wait_state(br, "running")
                        br.sleep(0.9)
                        boxa = canvas_box(br)
                        livea = live_at(br)
                        pa = png(br, SHOTS / (tag + "-before.png"))
                        pin(br, at + STRADDLE, p_at)
                        br.sleep(0.7)
                        liveb = live_at(br)
                        pb = png(br, SHOTS / (tag + "-after.png"))
                        e = (cropped_excess(pa, pb, boxa, scale, SHOTS, tag) if boxa
                             else {"worst": 255, "share": 1.0, "size": None,
                                   "why": "the renderer claimed no rect"})
                        js(br, "window.__exPass.adapter.interrupt('%s-done'); return null;" % tag)
                        wait_state(br, "idle")
                        return {"took": got["took"], "live": live, "a": livea, "b": liveb, "e": e}

                    def straddle_pinned(tag, at):
                        """The same straddle over the same edge, with the joining voice's dry pinned
                        to nothing at all — so the voice joins the stack and cannot change a pixel."""
                        return straddle(tag, at, sc=score(dry="zero"))

                    # ---- row 0b · the floor for a voice that joins and contributes nothing ---
                    # Row 0 measures what two renderings of ONE frame cost, and it is nothing. A door
                    # row compares two frames that differ by one more DRAW CALL — a voice has joined
                    # the stack — and a lawful one contributes no pixel. Those two renderings reach
                    # the same picture by different numbers of arithmetic steps, and an eight-bit
                    # channel cannot carry a difference below its own last step. So the cost of that
                    # extra call is measured here rather than assumed: the same straddle over the
                    # same window edge, with the joining voice's dry pinned to nothing at all, so it
                    # cannot change the picture by construction. Whatever this reads is the
                    # arithmetic; anything above it in a door row is the crossing.
                    join = straddle_pinned("joinfloor", OPEN)
                    joinBar = max(bar, join["e"]["worst"])
                    check(ROWS[1],
                          join["a"]["state"] == "running" and join["b"]["state"] == "running"
                          and join["a"]["live"] != join["b"]["live"],
                          f"a voice joining at no presence at all, over the rect the renderer claims "
                          f"{join['e'].get('size')}: worst excess {join['e']['worst']} of 255 on "
                          f"{join['e']['share'] * 100:.4f}% of pixels, with the live voices going "
                          f"{join['a']['live']} → {join['b']['live']}. That is the cost of the extra "
                          f"draw call, and it is the bar the two door rows below are held to")

                    # ---- handoff 1 · the curtain goes up ---------------------------------
                    rest_at(br, A)
                    pin(br, 0, 0)
                    before = png(br, SHOTS / "curtain-dom.png")
                    r1 = offer(br, A, B, "seam-curtain", SC)
                    running = wait_state(br, "running")
                    br.sleep(0.7)
                    box1 = canvas_box(br)
                    after = png(br, SHOTS / "curtain-canvas.png")
                    if not (r1["took"] and running and box1 and box1["vis"] == "visible"):
                        check(ROWS[2], False, f"the passage never took the frame: {r1} box={box1}")
                    else:
                        e = cropped_excess(before, after, box1, scale, SHOTS, "curtain")
                        check(ROWS[2], e["worst"] <= bar,
                              f"the walk's own picture against the renderer's first frame over the "
                              f"rect the renderer claims {box1} → crop {e.get('size')}: worst "
                              f"excess {e['worst']} of 255 against the bench's floor of {bar}; "
                              f"{e['share'] * 100:.4f}% of pixels fell outside their own "
                              f"neighbourhood range{'' if e['why'] is None else ' — ' + e['why']}")
                    js(br, "window.__exPass.adapter.interrupt('curtain-done'); return null;")
                    wait_state(br, "idle")

                    # ---- handoffs 2, 3 and 4 · inside one running passage ----------------
                    # One offer carries all three: the frame loop is pinned, so the passage is held
                    # still and the pin is walked to either side of each edge in turn. Nothing but
                    # the pin moves between the two shots of a pair.
                    edges = [(ROWS[3], "open", OPEN), (ROWS[5], "handover", HANDOVER),
                             (ROWS[4], "close", CLOSE)]

                    for row, tag, at in edges:
                        # EACH EDGE'S OWN FLOOR, MEASURED AT THAT EDGE. What an authority change
                        # costs the arithmetic depends on how many voices change hands there: one
                        # door is one more draw call, a level handover is one call gone and another
                        # arrived. So the floor is taken at the very edge the row is about, with the
                        # voices' dry pinned to nothing at all — they change hands and cannot change
                        # a pixel — and the row's own reading is held to that. Anything above it is
                        # the crossing stepping rather than the renderer rounding.
                        f = straddle_pinned(tag + "-floor", at)
                        edgeBar = max(bar, f["e"]["worst"])
                        g = straddle(tag, at)
                        livea, liveb, e = g["a"], g["b"], g["e"]
                        # THREE THINGS MUST HOLD BEFORE A PIXEL READING MEANS ANYTHING HERE: the
                        # passage was on the frame for both shots, and the authority really did
                        # change between them. A row green for having measured a landed walk would
                        # be worse than a red.
                        standing = livea["state"] == "running" and liveb["state"] == "running"
                        moved = livea["live"] != liveb["live"]
                        why = []
                        if not standing:
                            why.append("THE PASSAGE WAS NOT ON THE FRAME FOR BOTH SHOTS")
                        if not moved:
                            why.append("NO VOICE CHANGED HANDS HERE")
                        check(row, standing and moved and e["worst"] <= edgeBar,
                              f"across {at:.3f} s the live voices went {livea['live']} → "
                              f"{liveb['live']} (stack {livea['stack']}, host {livea['state']} → "
                              f"{liveb['state']}); over the rect the renderer claims "
                              f"{e.get('size')} the worst excess is {e['worst']} of 255 against the "
                              f"floor of {edgeBar} for this edge's own change of hands (measured "
                              f"there with every voice's dry pinned to nothing, where "
                              f"{f['a']['live']} → {f['b']['live']}), with "
                              f"{e['share'] * 100:.4f}% of pixels "
                              f"outside their own neighbourhood range. The host's own last words: "
                              f"{liveb['last']}"
                              + ("" if not why else " — " + "; ".join(why)))

                    # ---- the vacuity guard, on the very same predicate -------------------
                    # Two instants of ONE passage, a passage apart, straddled the same way every
                    # row above straddles an edge — so what separates this reading from those is
                    # the size of the step and nothing else about the method.
                    v = straddle("far", CLOSE, prog=0.25)
                    v2 = straddle("far2", CLOSE, prog=0.95)
                    pv1, pv2 = SHOTS / "far-before.png", SHOTS / "far2-before.png"
                    boxv = {"x": 0, "y": 0, "w": VW, "h": VH}
                    ev = cropped_excess(pv1, pv2, boxv, scale, SHOTS, "vac")
                    check(ROWS[8], ev["worst"] > bar,
                          f"the same predicate on one passage at two of its own instants "
                          f"(progress 0.2500 and 0.9500, host {v['a']['state']}/"
                          f"{v2['a']['state']}) over "
                          f"{ev.get('size')}: worst excess {ev['worst']} of 255 against the bench's "
                          f"floor of {bar}, {ev['share'] * 100:.4f}% of pixels outside their own "
                          f"neighbourhood range. A check that could not see this could see nothing")

                    js(br, "window.__exPass.adapter.interrupt('doors-done'); return null;")
                    wait_state(br, "idle")

                    # ---- handoff 5 · the frame given back --------------------------------
                    rest_at(br, A)
                    pin(br, DUR / 1000.0, 1)
                    r5 = offer(br, A, B, "seam-arrive", SC)
                    running = wait_state(br, "running")
                    br.sleep(1.0)
                    box5 = canvas_box(br)
                    canvas_shot = png(br, SHOTS / "arrive-canvas.png")
                    js(br, "window.__exPass.adapter.handoff(window.__cmd);"
                           "window.__exPass.bench.show(false); return null;")
                    br.sleep(0.5)
                    dom_shot = png(br, SHOTS / "arrive-dom.png")
                    if not (r5["took"] and running and box5):
                        check(ROWS[6], False, f"the passage never took the frame: {r5}")
                    else:
                        e = cropped_excess(canvas_shot, dom_shot, box5, scale, SHOTS, "arrive")
                        check(ROWS[6], e["worst"] <= bar,
                              f"the renderer's last frame against the DOM it handed to, over the "
                              f"rect the renderer claims {e.get('size')}: worst excess {e['worst']} "
                              f"of 255 against the bench's floor of {bar}, "
                              f"{e['share'] * 100:.4f}% of pixels outside their own neighbourhood "
                              f"range")
                    js(br, "window.__exPass.adapter.interrupt('arrive-done'); return null;")
                    wait_state(br, "idle")

                    # ---- handoff 6 · the cadence lands on a door -------------------------
                    # THE CADENCE WALKS IN REAL TIME while the pinned clock holds the passage's own
                    # second still, so the frame the cadence lands on cannot be pinned into place.
                    # It is caught instead: the canvas is photographed repeatedly while the cadence
                    # runs and the LAST shot taken while the canvas still stood is the one compared.
                    # What that costs is bounded by the envelope itself — the cadence walks on
                    # `smooth`, whose slope at its own end is zero, so the picture's motion over the
                    # last poll interval is second order in it and vanishes beside the step a jump
                    # would make.
                    rest_at(br, A)
                    br.evaluate("window.__exPass.host.configure({clockPin:null, progressPin:null,"
                                " prepareBudgetMs:400, settleSlackMs:2000}); 0")
                    solo = score(within=2000)
                    solo["cues"] = [ground_cue(DUR / 1000.0)]
                    r6 = offer(br, A, B, "seam-cadence", solo)
                    running = wait_state(br, "running")
                    br.sleep(CUT_AT)
                    js(br, "window.__exPass.host.cancel('seam-cadence'); return null;")
                    last_canvas, last_box = None, None
                    for i in range(40):
                        bx = canvas_box(br)
                        if not bx or bx["vis"] != "visible":
                            break
                        last_box = bx
                        last_canvas = png(br, SHOTS / "cadence-canvas.png")
                        br.sleep(0.05)
                    wait_state(br, "idle")
                    br.sleep(0.5)
                    cadence_dom = png(br, SHOTS / "cadence-dom.png")
                    rep6 = js(br, "var r = window.__exPass.host.report();"
                                  "return {cadence: r.cadence, state: r.state};")
                    if not (r6["took"] and running and last_canvas and last_box):
                        check(ROWS[7], False, f"no cadence frame was caught: {r6} "
                                              f"running={running} box={last_box} "
                                              f"first-look={canvas_box(br)} "
                                              f"report={rep6}")
                    else:
                        e = cropped_excess(last_canvas, cadence_dom, last_box, scale, SHOTS,
                                           "cadence")
                        cad = rep6.get("cadence") or {}
                        check(ROWS[7], e["worst"] <= bar,
                              f"the cadence landed on door «{cad.get('door')}» in "
                              f"{cad.get('landedInMs')} ms; its last frame against the DOM it "
                              f"handed to, over the rect the renderer claimed {e.get('size')}: "
                              f"worst excess {e['worst']} of 255 against the bench's floor of "
                              f"{bar}, {e['share'] * 100:.4f}% of pixels outside their own "
                              f"neighbourhood range")
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
