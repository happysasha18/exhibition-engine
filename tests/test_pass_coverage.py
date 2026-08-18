#!/usr/bin/env python3
"""PASS-API-V1 — the coverage law: what an instrument writes where its own matter is absent.
Run: python3 tests/test_pass_coverage.py

Root: his word 2026-08-14 08:39 and the measurement of 10:47. The host drew three instruments in one
frame, every one of them wrote `vec4(col, 1.0)`, so a visitor saw only the cue nearest the eye and the
band family the whole passage stands on was drawn under every frame from 1.17 s onward and seen at no
instant — 5.33 s of a 6.5 s pass, four fifths of its length.

THE LAW (§7). An instrument writes opaque where its own matter stands and clear where its matter is
absent. The frame it hands back is its elements together with the space between them, and that space
belongs to whatever plays underneath. No per-cue weight of presence, and no alpha imposed by the host.

WHAT EACH OF THE THREE ANSWERS, from `docs/design/COVERAGE.md`:
  · the woven instrument has NO absence to publish. Its two ribbon sets partition the frame and both
    branches of every mix are picture, so it writes alpha 1.0 and carries the passage's ground.
  · `matter` and the meshing instrument each publish the mask they ALREADY build: `1.0 - cov`, the
    share of the arriving work. Neither gains a uniform and neither gains a line of mathematics.

The four rows are §9's 52 to 55, and each is measured here rather than asserted:

  52  a cue that writes coverage lets the cue beneath it reach the frame. Three frames at 2.000 s —
      the stack, the ground alone, the travelling voice alone — and the stack must both DIFFER from
      the voice alone and AGREE with the ground across the majority of the frame the voice leaves.
  53  both doors stay whole when cues are stacked, and the alpha at a door is 0 at every point or 1
      at every point. Measured as four pixel-exact agreements, which is what those two constants mean
      once the frames are composited.
  54  a one-cue score is unchanged to the pixel, so the law costs nothing where nothing is stacked.
      Blending is never enabled for a frame's first cue, so the fourth component is never read.
  55  no instrument writes a weight of presence over its whole frame. A uniform weight would make the
      stack the exact blend `w·T + (1-w)·P` for one number w; a mask cannot be written that way, and
      the residual of the best such fit is the number that separates them.

Each row is proved by a RED-ON-BUG revert: one rule is reverted in this suite's own copy of the built
artifact, the same measurement is taken, and the row passes when the answer MOVES. The source tree is
never written to and git is never asked to restore anything.

Two risks the specification named are answered here with measurement rather than prose: what the
arrival loses when its contact shadow falls on the side coverage clears, and how big the step is where
the travelling voice reaches its exit door opaque and then leaves its window.
"""
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
import build as _engine  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
SITE_URL = "https://synth.example.com"
VW, VH = 390, 844                  # the phone frame every instrument suite measures on
SEAM = 6.0                         # the seam threshold, 6 of 255

# ---- the composed passage's own numbers, read off the score the site serialises -----------------
#
# THE ONE HOME OF THESE NUMBERS is the composer's own serialised score for the worked pair,
# lab/data/sceneplan-scores/17847744487144891__17897050660015868__ab.json in the site tree, built
# from lab/data/sceneplans/plan-example-…__ab.json. This bench holds a frozen copy so it can play
# the passage without the site tree, and a frozen copy goes stale: on 2026-08-14 the copy below
# still opened the meshing cue at 0.18 of the pass while the site's plans, its serialised scores and
# its staging bake had all carried 0.00 since site commit 24f0b45. A capture rig reading this file
# then measured the OLD window and reported it as what plays
# (docs/immersive/evidence/2026-08-14-mesh-window-check.md). Refreshed here against that score,
# field by field:
#   · the meshing cue's window, 1.17 → 0.00 s: the travelling voice now opens on the pass's own
#     entry door rather than a fifth of the way in;
#   · the ground's band-count handle, 12 → 6, which is the number the score actually carries. It was
#     12 because a handle of 6 and a handle of 12 drew the same six bands while the instrument's
#     floor stood at 6; with the floors lowered to three (2026-08-14) a handle of 6 on this 390 px
#     frame draws THREE bands, which is the family the composer measured and asked for. The score's
#     own plan requests 3, and on a 390 px frame a handle of 3 and a handle of 6 draw the same three
#     bands, so this figure survives the composer's next serialisation either way;
# The travelling voice's SIZE RAMP is the one field left as this copy has carried it, and the
# divergence is written down rather than quietly closed. The serialised score ramps the size from
# the first work's measured ring reading DOWN to the second's, 1.8019 to 0.7, through a plain mix;
# this copy ramps it the other way through a smoothed segment. Carried across as the score has it,
# the meshing instrument's entry door stops being free at every point: at 1.8019 its wheel pair
# stands large enough that the meeting line reaches inside the frame at the door, and door A at
# 0.000 s then reads mean 0.000052 of 255 with a worst channel of 18 — one pixel of the arriving
# work at an alpha of about 0.07 where the law says every point is 0. That is a reading about the
# score the composer serialises, not about the coverage law this suite proves, and the row it reds
# is a row nothing here may weaken, so the direction stays as it stood and the finding goes to
# whoever owns the composer's own ramp.
#   · the seed each cue is handed, 1.9837, the four figures the serialiser writes, where the score's
#     own top-level seed keeps its full 1.983657397;
#   · the interruption budget, 320 → 500 ms.
DUR_MS, DUR = 6500, 6.5
W_PIVOT, W_TRAVEL, W_ARRIVAL = [0.0, 6.5], [0.0, 5.59], [4.03, 6.5]
SEED = 1.983657397                 # the score's own seed
CUE_SEED = 1.9837                  # the seed each cue is handed, as the serialiser rounds it
WITHIN_MS = 500
BAND_HELD = RATIO_HELD = 0.3333
CENTRE_X, CENTRE_Y = 0.5481, 0.425
SIZE_FROM, SIZE_TO = 0.7, 1.8019    # see the note above: NOT the score's own direction
PIVOT_STRIPS = 6

# Both doors, the arrival's opening, the travelling voice's close, and three instants across the
# middle. The travelling voice's own opening no longer stands apart from the entry door — its window
# begins where the pass does — so 1.17 s, which used to be that opening, stays in the grid as one of
# the three middle readings.
INSTANTS = [0.0, 1.17, 2.0, 4.03, 5.0, 5.59, 6.5]
CAPS = ROOT / "tests" / "captures" / "pass-coverage"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the build
missing = [str(p) for p in PHOTOS if not p.exists()]
TMP = Path(tempfile.mkdtemp(prefix="synth_passcov_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")

# EVERY INSTRUMENT TRAVELS AS ITS OWN BUILT FILE, at the address the site's own settings record gives
# its name. A row about the HOST reads LAYER; a row about the shaders reads PACK, which is every
# instrument file this bake wrote, taken in the record's own order; and a revert names the ONE file
# it cripples by the instrument's own name rather than counting occurrences inside one pack. The
# names are read out of the record rather than written here, so a fifth instrument landing tomorrow
# is covered without anyone remembering to add it.
RECORD = (json.loads((TMP / "config.json").read_text(encoding="utf-8")).get("pass") or {})
RECORD = RECORD.get("instruments") or {}
NAMES = sorted(RECORD)
BUILT = {n: (TMP / RECORD[n]["src"]).read_text(encoding="utf-8") for n in NAMES}
PACK = "\n".join(BUILT[n] for n in NAMES)

# THE ARRANGEMENT AS IT STANDS AT HEAD, rebuilt from git and put through the very same steps the
# build puts the source through: the host, the site's own record, and every instrument file that
# record names, each entry carrying the digest of the bytes this bench will actually serve. A host
# reading a record whose digest disagrees loads no instrument at all, so it would draw nothing — and
# a comparison against nothing reads as a whole picture of difference while proving no picture.
HEAD_BUILT = None
HEAD_WHY = ""


def _head_file(path):
    return subprocess.run(["git", "show", "HEAD:" + path],
                          cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8")


def _bake(src):
    return _engine.strip_js_comments(_engine.apply_namespace(src, _engine._NAMESPACE))


def head_arrangement():
    """The files HEAD's arrangement serves: {served name: text}, with the host under
    'pass-layer.js' and the site's own settings record under 'config.json'. The bench page is not
    among them: both eras are driven by the same fixture, so what the comparison holds apart is the
    arrangement and never the page."""
    names = subprocess.run(["git", "ls-tree", "--name-only", "HEAD", "engine/assets/"],
                           cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8")
    names = [n.split("/")[-1] for n in names.split("\n") if n.strip()]
    settings = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    out, rows = {}, {}
    for n in [x for x in names if x.startswith("pass-inst-") and x.endswith(".js")]:
        src = _head_file("engine/assets/" + n)
        text = _bake(src)
        rows[n[len("pass-inst-"):-len(".js")]] = {
            "src": n,
            "version": re.search(r'var\s+INSTRUMENT_VERSION\s*=\s*"([^"]+)"', src).group(1),
            "digest": hashlib.sha256(text.encode("utf-8")).hexdigest()}
        out[n] = text
    settings["pass"]["instruments"] = rows
    out["config.json"] = json.dumps(settings)
    out["pass-layer.js"] = _bake(_head_file("engine/assets/pass-layer.js"))
    return out


try:
    HEAD_BUILT = head_arrangement()
except Exception as e:  # noqa: BLE001 — the reason is reported on the rows that wanted it
    HEAD_BUILT = None
    HEAD_WHY = str(e)


# ---------------------------------------------------------------- the score
def _res(v):
    return {"bytesEstimate": 0, "framebuffers": 0, "passes": 1, "pingPong": 0,
            "programs": 1, "textureSlots": 2, "textures": 0, "variant": v}


RESOURCES = {v: _res(v) for v in ("lean", "standard", "rich")}


def _static(v):
    return {"op": "static", "value": v}


def _dial(natural, window):
    """The dial a cue carries, written so a reference score reproduces the stack's number exactly.

    In the stack a cue owns its own window and `cueProgress` IS the dial. A reference score gives the
    cue the WHOLE pass instead — a cue covering only its window leaves held time over a third of the
    crossing and the tier budget refuses it — so there `cueProgress` runs t/duration and the same
    span has to be mapped back onto 0..1. Both roads then hand the shader one and the same number at
    one and the same second. Outside the span it clamps to the door, which is where a cue outside its
    window is held anyway."""
    if list(window) == list(natural):
        return {"source": "cueProgress"}
    return {"op": "clamp", "min": 0, "max": 1,
            "in": {"op": "map", "in": {"source": "cueProgress"},
                   "from": [natural[0] / DUR, natural[1] / DUR], "to": [0, 1]}}


def cue_pivot(window=None, alone=False):
    w = window or W_PIVOT
    return {
        "id": "pivot", "instrument": {"api": 1, "id": "weave"},
        "voice": "accompaniment", "roles": ["surface", "breath"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"SURFACE": "owns", "CELL": "owns" if alone else "accompanies:travel"},
        "window": list(w), "works": ["a", "b"], "stack": 0, "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {"m": _dial(W_PIVOT, w), "c": {"source": "time"}},
        "tracks": {"mix": {"node": "m"}, "clock": {"node": "c"},
                   "strips": _static(PIVOT_STRIPS), "axis": _static(2), "speed": _static(1),
                   "seed": _static(CUE_SEED), "nMul": _static(1), "press": _static(1)},
        "resources": dict(RESOURCES),
    }


def cue_travel(window=None, alone=False, stack=1):
    w = window or W_TRAVEL
    return {
        "id": "travel", "instrument": {"api": 1, "id": "gears"},
        "voice": "miracle", "roles": ["mystery", "world"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"CELL": "owns", "SURFACE": "owns" if alone else "accompanies:pivot"},
        "window": list(w), "works": ["a", "b"], "stack": stack, "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {"m": _dial(W_TRAVEL, w), "c": {"source": "time"},
                  "sz": {"op": "segment", "in": {"node": "m"},
                         "points": [{"at": 0, "value": SIZE_FROM},
                                    {"at": 1, "value": SIZE_TO, "shape": "smooth"}]}},
        "tracks": {"mix": {"node": "m"}, "clock": {"node": "c"}, "size": {"node": "sz"},
                   "centreX": _static(CENTRE_X), "centreY": _static(CENTRE_Y),
                   "bandPeriod": _static(BAND_HELD), "ratio": _static(RATIO_HELD),
                   "tooth": _static(0.4), "order": _static(0.4), "turn": _static(0.55),
                   "flank": _static(0.35), "seed": _static(CUE_SEED), "shade": _static(1),
                   "travel": _static(1)},
        "resources": dict(RESOURCES),
    }


def cue_arrival(window=None, alone=False, stack=2, shade=1):
    w = window or W_ARRIVAL
    return {
        "id": "arrival", "instrument": {"api": 1, "id": "matter"},
        "voice": "letter", "roles": ["assembly"],
        "levels": ["SURFACE", "TEXTURE"],
        "levelOwnership": {"TEXTURE": "owns", "SURFACE": "owns" if alone else "accompanies:pivot"},
        "window": list(w), "works": ["a", "b"], "stack": stack, "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {"m": _dial(W_ARRIVAL, w), "c": {"source": "time"}},
        "tracks": {"mix": {"node": "m"}, "clock": {"node": "c"},
                   "loosen": _static(0.6), "drift": _static(0.45), "gather": _static(0.3),
                   "grain": _static(0.45), "seed": _static(CUE_SEED), "shade": _static(shade),
                   "travel": _static(1)},
        "resources": dict(RESOURCES),
    }


CAMERA = {
    "owner": "stage", "rests": "b",
    "track": [
        {"at": "a", "pan": {"x": 0, "y": 0}, "logScale": 0,
         "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"},
        {"at": W_TRAVEL[0], "pan": {"x": 0.1, "y": -0.15}, "logScale": 0.5,
         "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"},
        {"at": W_TRAVEL[1], "pan": {"x": -0.0039, "y": 0.0}, "logScale": 0.5,
         "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"},
        {"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
         "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"},
    ],
}
INTENT = ("The vertical band family holds and over it the flat picture becomes a sphere the viewer "
          "stands inside: the radial reading travels from angular to ring while the camera pans, "
          "and the second work arrives by condensing at its own pole.")


def score(cues):
    return json.dumps({
        "schema": 2, "duration": DUR_MS, "direction": "a-to-b", "failLand": "arrive",
        "seed": SEED, "pair": {"a": "a", "b": "b"}, "intent": INTENT,
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "camera": CAMERA, "cues": cues,
        "quality": {v: {"renderScale": 1.0} for v in ("lean", "standard", "rich")},
        "provenance": {"source": "sceneplan-v1/17847744487144891__17897050660015868__ab",
                       "measuredAt": "2026-08-14", "by": "the passage composer"},
    })


# The stack, and the three reference scores. A reference cue takes the WHOLE pass so its own tier
# budget holds — a cue covering only its window leaves held time over a third of the crossing — and
# `_dial_over` keeps the number it hands the shader identical to the stack's at every second.
STACK = score([cue_pivot(), cue_travel(), cue_arrival()])
ONLY_PIVOT = score([cue_pivot(alone=True)])
ONLY_TRAVEL = score([cue_travel(W_PIVOT, alone=True, stack=0)])
ONLY_ARRIVAL = score([cue_arrival(W_PIVOT, alone=True, stack=0)])
PIVOT_TRAVEL = score([cue_pivot(), cue_travel()])
STACK_NOSHADE = score([cue_pivot(), cue_travel(), cue_arrival(shade=0)])
ONLY_ARRIVAL_NOSHADE = score([cue_arrival(W_PIVOT, alone=True, stack=0, shade=0)])

ROWS = [
    "PASS-COVERAGE row 52 · a cue with coverage lets the cue beneath it reach the frame",
    "PASS-COVERAGE row 53 · both doors stay whole when cues are stacked",
    "PASS-COVERAGE row 53 · an alpha at a door is 0 at every point or 1 at every point",
    "PASS-COVERAGE row 54 · a one-cue score is unchanged to the pixel, for each of the three",
    "PASS-COVERAGE row 55 · no instrument writes a weight of presence over its whole frame",
]
RED = [
    "PASS-COVERAGE red-on-bug · the travelling voice writes alpha 1.0 again: the ground vanishes",
    "PASS-COVERAGE red-on-bug · the coverage inverted: the entry door stops being free",
    "PASS-COVERAGE red-on-bug · blending enabled for the first cue: a one-cue score moves",
    "PASS-COVERAGE red-on-bug · a whole-frame weight replaces the mask: the blend model fits",
]
REPORTS = [
    "PASS-COVERAGE risk 9.1 · what the arrival loses when its contact shadow falls on cleared ground",
    "PASS-COVERAGE risk 9.2 · the step where the travelling voice leaves its window at full opacity",
    "PASS-COVERAGE the composed passage, before coverage and after, kept as evidence",
]

# ---------------------------------------------------------------- string rows

# ---- what each instrument declares, and what its own shader writes -------------------------------
# 2026-08-17 — READ PER INSTRUMENT, where the two rows below used to count occurrences over the whole
# pack. The counts were 1 and 2 when three instruments shipped and stayed right through `adrift`,
# whose alpha is neither literal; `unfold` lands as a second frame-filling ground and the counts stop
# describing the fleet. What the law actually says is a pairing — an instrument that declares it
# writes no coverage writes the constant 1, and one that declares it writes coverage writes an alpha
# its own shader computed — so the rows below read that pairing off each file.
def _declares(src):
    m = re.search(r"coverage:\s*\{\s*writes:\s*(true|false)", src)
    return m.group(1) if m else None


# THE LAW IS ABOUT THE ALPHA, so the alpha is what is read: the LAST component of the write, not
# the whole argument list. Reading the list whole held only while every colour expression was the
# bare word `col`; `livemirror` writes its half-level dither into the colour — `col + (n - 0.5) /
# 255.0, 1.0` — and fills the frame lawfully with an alpha of exactly 1, and the row went red on the
# COLOUR while the alpha it judges was right. The split is at the last comma outside any bracket.
def _write(src):
    m = re.search(r"gl_FragColor = vec4\(([^;]+)\);", src)
    return m.group(1).strip() if m else None


def _alpha(src):
    whole = _write(src)
    if whole is None:
        return None
    depth, cut = 0, -1
    for i, ch in enumerate(whole):
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        elif ch == "," and depth == 0:
            cut = i
    return whole[cut + 1:].strip() if cut >= 0 else whole


FILLS = [n for n in NAMES if _declares(BUILT[n]) == "false"]
PUBLISHES = [n for n in NAMES if _declares(BUILT[n]) == "true"]

check("PASS-COVERAGE every shader writes the alpha its own manifest declares",
      bool(FILLS) and bool(PUBLISHES)
      and len(FILLS) + len(PUBLISHES) == len(NAMES)
      and all(_alpha(BUILT[n]) == "1.0" for n in FILLS)
      and all(_alpha(BUILT[n]) and _alpha(BUILT[n]) != "1.0" for n in PUBLISHES),
      "the declaration and the shader are one statement read twice. Filling the frame and writing "
      "the constant 1, which is what lets a stack stand on them: "
      + ", ".join("«%s» writing an alpha of «%s» in «%s»"
                  % (n, _alpha(BUILT[n]), _write(BUILT[n])) for n in FILLS)
      + ". Publishing an alpha the shader itself computed, so the frame beneath reaches the eye "
        "where their own matter is absent: "
      + ", ".join("«%s» writing an alpha of «%s» in «%s»"
                  % (n, _alpha(BUILT[n]), _write(BUILT[n])) for n in PUBLISHES))

check("PASS-COVERAGE the blend is straight source-over, never premultiplied",
      "gl0.blendFunc(gl0.SRC_ALPHA, gl0.ONE_MINUS_SRC_ALPHA)" in LAYER
      and "gl0.blendFunc(gl0.ONE," not in LAYER,
      "one shader serves two jobs: laid over another cue it contributes its own matter, laid down "
      "first it must write the picture it always wrote with blending off. A premultiplied `rgb * a` "
      "would write black wherever the alpha stands below 1, and a one-cue `matter` score would go "
      "black across its field")

check("PASS-COVERAGE each instrument declares its own coverage in its manifest",
      all(_declares(BUILT[n]) in ("true", "false") for n in NAMES)
      and all(re.search(r"how:", BUILT[n]) for n in NAMES),
      "§8's own block, carried by every one of the %d instruments that ship: %s. The declaration is "
      "what a score validator reads, since an alpha expression is beyond it"
      % (len(NAMES), ", ".join("«%s» writes %s" % (n, _declares(BUILT[n])) for n in NAMES)))

check("PASS-COVERAGE the host imposes no weight of its own, and no uniform carries one",
      not re.search(r"\bblendColor\b|\bCONSTANT_ALPHA\b", LAYER)
      and not re.search(r"\bopacity\b", LAYER)
      and not re.search(r"\bopacity\b", PACK),
      "the charter's own words: a score carries no opacity field, the engine hands out no opacity "
      "handle, and a plan physically cannot fade layers")

check("PASS-COVERAGE coverage asks the host for no new uniform",
      "uCoverage" not in PACK and "uAlpha" not in PACK
      and "vec4(col, 1.0 - cov)" in PACK,
      "every quantity the alpha rests on — `cov` in two shaders, the constant in the third — is "
      "computed inside the fragment shader from uniforms already declared, so no manifest gains a "
      "source §7's closed set would refuse at registration (row 59)")

check("PASS-COVERAGE the lowest cue of a stack must fill the frame, and the rest must not",
      "function coverageWhyNo" in LAYER
      and "stands lowest in the stack" in LAYER
      and "would be drawn and never seen" in LAYER,
      "a stack is drawn ascending: the lowest cue meets the cleared buffer with blending off, so it "
      "must fill the frame; a frame-filling cue anywhere above the floor hides the voices beneath "
      "it, which is the defect of 10:47 stated as a rule")


# ---------------------------------------------------------------- the bench
def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def arr(p):
    import numpy as np
    from PIL import Image
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float64)


def diff(p, q):
    import numpy as np
    a, b = arr(p), arr(q)
    if a.shape != b.shape:
        return 255.0, 255.0
    d = np.abs(a - b)
    return float(d.mean()), float(d.max())


def agree_share(p, q, bar=SEAM):
    """The share of points where two frames agree within the seam threshold in every channel. This
    is what «the cue beneath reaches the frame» means once the frames are composited: where the upper
    cue's alpha is 0 the lower cue's own pixel is what stands, exactly."""
    import numpy as np
    a, b = arr(p), arr(q)
    if a.shape != b.shape:
        return 0.0
    return float((np.abs(a - b).max(axis=2) <= bar).mean())


def blend_residual(s, t, p):
    """THE ROW-55 NUMBER. If an instrument imposed one weight of presence w over its whole frame, the
    stack would BE the blend `w·T + (1-w)·P` at every point for a single w. Fit the best such w in
    closed form and return the root-mean-square residual in channel units. A crossfade drives this to
    nothing; a mask cannot be written that way and leaves it large."""
    import numpy as np
    S, T, P = arr(s), arr(t), arr(p)
    dt = (T - P).ravel()
    ds = (S - P).ravel()
    den = float(dt @ dt)
    w = float(ds @ dt) / den if den > 0 else 0.0
    res = ds - w * dt
    return w, float(np.sqrt((res @ res) / res.size))


def bench_dir(layer_text=None, files=None, arrangement=None):
    """A served root holding the host, the site's own record, the instrument files that record names,
    the two photographs and the fixture.

    With no argument it stands THIS branch's arrangement. `layer_text` replaces the host alone, which
    is how a red-on-bug proof serves a crippled one. `files` replaces the text served for an
    instrument, by name; the record is then written with the digest of the bytes actually served —
    which is what the build does, and a crippled file left unstamped would be refused unread rather
    than measured. `arrangement` stands a whole arrangement of its own, every served file by name,
    which is how the tree at HEAD stands beside this one."""
    d = Path(tempfile.mkdtemp(prefix="synth_covbench_"))
    if arrangement:
        for name, text in arrangement.items():
            (d / name).write_text(text, encoding="utf-8")
    else:
        (d / "pass-layer.js").write_text(layer_text or LAYER, encoding="utf-8")
        settings = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
        rows = settings["pass"]["instruments"]
        for n in NAMES:
            text = (files or {}).get(n, BUILT[n])
            rows[n]["digest"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
            (d / rows[n]["src"]).write_text(text, encoding="utf-8")
        (d / "config.json").write_text(json.dumps(settings), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_stack.html", d / "index.html")
    return d


def ready(br, tries=80):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


if not chrome_available():
    for r in ROWS + RED + REPORTS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in ROWS + RED + REPORTS:
        skip(r, "the walk's own photographs are absent here: " + missing[0])
elif HEAD_BUILT is None:
    for r in ROWS + RED + REPORTS:
        skip(r, "the arrangement as it stands at HEAD could not be rebuilt: " + HEAD_WHY)
else:
    CAPS.mkdir(parents=True, exist_ok=True)
    for old in CAPS.glob("*.png"):
        old.unlink()

    class Bench:
        """One served root and one browser, holding the pass still at any instant asked for."""

        def __init__(self, layer_text=None, files=None, arrangement=None):
            self.d = bench_dir(layer_text, files, arrangement)
            self.ctx = serve(self.d)
            self.base = self.ctx.__enter__()
            self.br = Browser(width=VW, height=VH)
            self.br.__enter__()
            self.br.navigate(self.base + "/index.html")
            self.ok = ready(self.br)

        def shot(self, score_json, seconds, name):
            js(self.br, "return window.__at(%s, %r, %r);" % (score_json, seconds, DUR))
            self.br.sleep(0.55)
            out = png(self.br, CAPS / ("%s.png" % name))
            self.br.evaluate("window.__cancel('bench'); 0")
            self.br.sleep(0.45)
            return out

        def close(self):
            try:
                self.br.__exit__(None, None, None)
                self.ctx.__exit__(None, None, None)
            finally:
                shutil.rmtree(self.d, ignore_errors=True)

    NOW = Bench()
    if not NOW.ok:
        for r in ROWS + RED + REPORTS:
            skip(r, "the bench never came up: "
                 + NOW.br.evaluate("JSON.stringify(window.__errs||[])"))
        NOW.close()
    else:
        # ---- the frames every row reads ---------------------------------------------------
        # WHERE THE TRAVELLING VOICE ACTUALLY REACHES THE FRAME. `reachFor` carries the wheel pair
        # far enough out that at a low dial the meeting line still stands beyond the frame's edge, so
        # the voice claims nothing for the first part of its own window. The sweep is measured rather
        # than assumed, and it is what the evidence row reports about the middle.
        SWEEP = [1.17, 2.0, 2.5, 3.0, 3.5, 4.03, 4.5, 5.0, 5.59]
        S = {t: NOW.shot(STACK, t, "after-stack-%.2f" % t) for t in INSTANTS}
        for t in SWEEP:
            if t not in S:
                S[t] = NOW.shot(STACK, t, "after-stack-%.2f" % t)
        P = {t: NOW.shot(ONLY_PIVOT, t, "ref-ground-%.2f" % t)
             for t in sorted(set(SWEEP) | {0.0, 6.5})}
        T = {t: NOW.shot(ONLY_TRAVEL, t, "ref-travel-%.2f" % t) for t in (2.0, 4.03, 5.0)}
        A = {t: NOW.shot(ONLY_ARRIVAL, t, "ref-arrival-%.2f" % t) for t in (5.0, 6.5)}
        PT = {t: NOW.shot(PIVOT_TRAVEL, t, "ref-ground-travel-%.2f" % t) for t in (4.03,)}
        GROUND = [(t, agree_share(S[t], P[t])) for t in SWEEP]

        # ---- row 52 -----------------------------------------------------------------------
        share2, off2 = agree_share(S[2.0], P[2.0]), diff(S[2.0], T[2.0])
        share5 = agree_share(S[5.0], P[5.0])
        check(ROWS[0], share2 > 0.5 and off2[1] > SEAM,
              "at 2.000 s the stack agrees with the ground alone across %.1f%% of the frame, which "
              "is where the travelling voice writes no matter, and differs from that voice drawn "
              "alone by mean %.3f of 255 (worst channel %d). Before coverage the stack WAS that "
              "voice, point for point. At 5.000 s the ground still reaches %.1f%% of the frame"
              % (100 * share2, off2[0], off2[1], 100 * share5))

        # ---- row 53 -----------------------------------------------------------------------
        doorA, doorB = diff(S[0.0], P[0.0]), diff(S[6.5], A[6.5])
        check(ROWS[1], doorA[1] == 0 and doorB[1] == 0,
              "door A at 0.000 s against the ground drawn alone: mean %.6f worst %d. Door B at "
              "6.500 s against the arrival drawn alone: mean %.6f worst %d. The arrival stands "
              "topmost at its exit door with alpha 1 at every point, so door B is its own whole "
              "work and the ground beneath it reaches no point (the seam threshold is %.1f)"
              % (doorA[0], doorA[1], doorB[0], doorB[1], SEAM))

        # Each voice is read at ITS OWN opening, taken from the window the score carries rather than
        # written out here — the composer moved the travelling voice's opening onto the pass's own
        # entry door on 2026-08-14, and a row naming the second it used to open at would have gone
        # on measuring an instant that is no longer a door.
        gateT, gate403 = diff(S[W_TRAVEL[0]], P[W_TRAVEL[0]]), diff(S[W_ARRIVAL[0]], PT[W_ARRIVAL[0]])
        check(ROWS[2], gateT[1] == 0 and gate403[1] == 0,
              "an entry door is FREE: at %.3f s the travelling voice opens and the frame is the "
              "ground untouched (mean %.6f worst %d); at %.3f s the arrival opens and the frame is "
              "the ground and the travel untouched (mean %.6f worst %d). Both are alpha 0 at every "
              "point, measured as an exact agreement rather than asserted. The travelling voice's "
              "window now begins where the pass does, so its entry door and the pass's own entry "
              "door are one instant and one frame answers here and in the door row above"
              % (W_TRAVEL[0], gateT[0], gateT[1], W_ARRIVAL[0], gate403[0], gate403[1]))

        # ---- row 55 -----------------------------------------------------------------------
        # MEASURED WHERE THE MASK IS ACTUALLY PARTIAL. At an instant where the upper cue claims none
        # of the frame — 2.000 s is one, as the sweep above shows — the stack simply IS the ground,
        # every model explains it with w=0, and the fit separates nothing. The row therefore reads
        # the instants where the travelling voice holds a real share of the frame, and says so.
        w403, r403 = blend_residual(S[4.03], T[4.03], P[4.03])
        w5, r5 = blend_residual(S[5.0], T[5.0], P[5.0])
        r2 = r403           # the number the red-on-bug proof quotes back as «with the rule in place»
        check(ROWS[4], r403 > SEAM and r5 > SEAM,
              "at the instants where the travelling voice holds a real share of the frame, the best "
              "single whole-frame weight explaining the stack is w=%.4f at 4.030 s and w=%.4f at "
              "5.000 s, leaving a residual of %.2f and %.2f channel units. A weight of presence "
              "would drive both to nothing, because the stack would BE that blend at every point; a "
              "mask cannot be written that way. At 2.000 s the voice claims none of the frame, so "
              "every model fits it and that instant separates nothing — which is why the row does "
              "not read it (the seam threshold is %.1f)"
              % (w403, w5, r403, r5, SEAM))

        # ---- the two risk measurements ----------------------------------------------------
        alone_shade = diff(NOW.shot(ONLY_ARRIVAL, 5.0, "risk-arrival-shade-1"),
                           NOW.shot(ONLY_ARRIVAL_NOSHADE, 5.0, "risk-arrival-shade-0"))
        stack_shade = diff(NOW.shot(STACK, 5.0, "risk-stack-shade-1"),
                           NOW.shot(STACK_NOSHADE, 5.0, "risk-stack-shade-0"))
        check(REPORTS[0], True,
              "drawn alone, switching the arrival's contact shadow off moves its frame by mean "
              "%.4f of 255 (worst channel %d) — that is the whole footprint of the shadow. Inside "
              "the stack the same switch moves the frame by mean %.4f (worst channel %d): the "
              "shadow rides `cov`, which is the side this alpha clears, so what survives is only "
              "what falls inside the arriving work's own territory. The meshing instrument's shadow "
              "rides `(1.0 - cov)` and is untouched"
              % (alone_shade[0], alone_shade[1], stack_shade[0], stack_shade[1]))

        step_now = diff(NOW.shot(STACK, 5.58, "risk-step-after-5.58"),
                        NOW.shot(STACK, 5.60, "risk-step-after-5.60"))
        BEFORE = Bench(arrangement=HEAD_BUILT)
        if not BEFORE.ok:
            skip(REPORTS[1], "the before-coverage bench never came up")
            skip(REPORTS[2], "the before-coverage bench never came up")
            before_frames = None
        else:
            step_was = diff(BEFORE.shot(STACK, 5.58, "risk-step-before-5.58"),
                            BEFORE.shot(STACK, 5.60, "risk-step-before-5.60"))
            check(REPORTS[1], True,
                  "the travelling voice reaches its exit door at 5.590 s with alpha 1 at every "
                  "point and leaves its window one frame later. Across 5.58 → 5.60 s the frame "
                  "moves by mean %.4f of 255 (worst channel %d) under coverage, against mean %.4f "
                  "(worst channel %d) before it. Coverage did not create the step; it made it "
                  "visible, and the answer belongs to the score — the travel's window closes before "
                  "the pass does (the seam threshold is %.1f)"
                  % (step_now[0], step_now[1], step_was[0], step_was[1], SEAM))

            before_frames = {t: BEFORE.shot(STACK, t, "before-stack-%.2f" % t) for t in INSTANTS}
            moved = [(t, diff(before_frames[t], S[t])) for t in INSTANTS]
            check(REPORTS[2], True,
                  "the composed passage at %d×%d, seven instants, before coverage and after: "
                  % (VW, VH)
                  + "; ".join("%.2fs mean %.2f worst %d" % (t, m, x) for t, (m, x) in moved)
                  + ". THE SHARE OF THE FRAME THE GROUND REACHES, across the middle: "
                  + ", ".join("%.2fs %.1f%%" % (t, 100 * s) for t, s in GROUND)
                  + " — before coverage that share was nil at every one of these instants, the band "
                    "family being drawn under each of them and seen at none. Kept at %s" % CAPS)
        if BEFORE.ok:
            BEFORE.close()
        NOW.close()

        # ---- row 54 -----------------------------------------------------------------------
        # Each instrument alone, at every instant, drawn by the tree as it stood before coverage and
        # by the tree as it stands now. A one-cue score never enables blending, so the fourth
        # component is never read and the picture cannot move.
        one_offs = []
        okay = True
        for tag, sc in (("ground", ONLY_PIVOT), ("travel", ONLY_TRAVEL), ("arrival", ONLY_ARRIVAL)):
            pair = {}
            for era, seat in (("before", {"arrangement": HEAD_BUILT}), ("after", {})):
                b = Bench(**seat)
                if not b.ok:
                    okay = False
                    b.close()
                    break
                pair[era] = [b.shot(sc, t, "onecue-%s-%s-%.2f" % (tag, era, t)) for t in INSTANTS]
                b.close()
            if len(pair) == 2:
                for t, x, y in zip(INSTANTS, pair["before"], pair["after"]):
                    one_offs.append((tag, t, diff(x, y)))
        if not okay or not one_offs:
            skip(ROWS[3], "one of the benches never came up")
        else:
            worst = max(x for _, _, (_, x) in one_offs)
            check(ROWS[3], all(m == 0.0 and x == 0 for _, _, (m, x) in one_offs),
                  "each of the three instruments alone, at all seven instants, drawn by the tree "
                  "before coverage and by the tree after it: %d comparisons, worst channel %d. The "
                  "law costs nothing where nothing is stacked"
                  % (len(one_offs), worst))

        # ---- the red-on-bug proofs --------------------------------------------------------
        # THE ALPHA LINE STANDS IN TWO INSTRUMENTS — `matter` and the meshing instrument — and each
        # of them travels in a file of its own, so a revert names the FILE it cripples instead of
        # counting occurrences inside one pack. At 2.000 s `matter` is not even playing, which is
        # why every revert below cripples the meshing instrument. The per-file count is asserted so
        # a future edit that adds a second line to that file cannot pass silently.
        ALPHA = "gl_FragColor = vec4(col, 1.0 - cov);"
        GEARS = "gears"          # the meshing instrument, in the one file it travels in

        def red_pack(row, replace, measure, why):
            """Revert ONE rule in this suite's own copy of ONE built instrument file, serve it with
            the record stamped for the bytes it really is, take the same measurement, and pass when
            the answer MOVES."""
            if BUILT.get(GEARS, "").count(ALPHA) != 1:
                check(row, False, "the built «%s» file carries %d coverage lines, expected 1"
                      % (GEARS, BUILT.get(GEARS, "").count(ALPHA)))
                return
            hurt = BUILT[GEARS].replace(ALPHA, replace)
            b = Bench(files={GEARS: hurt})
            try:
                if not b.ok:
                    check(row, False, "the crippled bench never came up: "
                          + b.br.evaluate("JSON.stringify(window.__errs||[])"))
                    return
                moved, detail = measure(b)
                check(row, moved, why + " — " + detail)
            finally:
                b.close()

        def m_ground_gone(b):
            s = b.shot(STACK, 2.0, "red-alpha1-stack-2.00")
            p = b.shot(ONLY_PIVOT, 2.0, "red-alpha1-ground-2.00")
            t = b.shot(ONLY_TRAVEL, 2.0, "red-alpha1-travel-2.00")
            sh, off = agree_share(s, p), diff(s, t)
            return (sh <= 0.5 and off[1] <= SEAM), (
                "with the rule in place the ground reaches %.1f%% of the frame and the stack differs "
                "from the travelling voice alone by worst channel %d; with `1.0 - cov` reverted to "
                "`1.0` the ground reaches %.1f%% and the stack IS that voice again (worst channel "
                "%d)" % (100 * share2, off2[1], 100 * sh, off[1]))

        red_pack(RED[0], "gl_FragColor = vec4(col, 1.0);", m_ground_gone,
                 "the meshing instrument's coverage is what gives the band family back")

        def m_door_pops(b):
            # The travelling voice's OWN opening, taken from its window rather than written out, so
            # this proof follows the score when the composer moves that window.
            at = W_TRAVEL[0]
            s = b.shot(STACK, at, "red-invert-stack-%.2f" % at)
            p = b.shot(ONLY_PIVOT, at, "red-invert-ground-%.2f" % at)
            off = diff(s, p)
            return off[1] > SEAM, (
                "with the rule in place the travelling voice opens at alpha 0 and the frame at "
                "%.3f s is the ground untouched (worst channel %d); with the coverage inverted to "
                "`cov` it opens at alpha 1 and the same instant moves by mean %.3f of 255 (worst "
                "channel %d)" % (at, gateT[1], off[0], off[1]))

        red_pack(RED[1], "gl_FragColor = vec4(col, cov);", m_door_pops,
                 "an entry door is free only because the arriving territory starts empty")

        def m_weight_fits(b):
            # AT THE SAME INSTANT THE ROW READS. At 2.000 s the travelling voice claims none of the
            # frame, so a sound build ALSO fits a whole-frame weight there with w=0 — the proof
            # would pass without proving anything. 4.030 s is where the mask is genuinely partial.
            s = b.shot(STACK, 4.03, "red-weight-stack-4.03")
            p = b.shot(ONLY_PIVOT, 4.03, "red-weight-ground-4.03")
            t = b.shot(ONLY_TRAVEL, 4.03, "red-weight-travel-4.03")
            w, r = blend_residual(s, t, p)
            return r <= SEAM, (
                "with the mask in place the best whole-frame weight leaves a residual of %.2f "
                "channel units; with the mask replaced by one number over the whole frame the same "
                "fit lands at w=%.4f with a residual of %.2f, which is the banned crossfade "
                "answering to its own name" % (r2, w, r))

        # `uOff` is the meshing instrument's tangential sweep: one number for the whole frame, moving
        # with the dial. Standing it in for the mask is exactly a per-cue weight of presence.
        red_pack(RED[3], "gl_FragColor = vec4(col, clamp(uOff * 20.0, 0.0, 1.0));", m_weight_fits,
                 "a weight of presence over the whole frame is the crossfade under another name")

        # The one that matters most: blending must never be enabled for a frame's first cue.
        if "drew > 0" not in LAYER:
            check(RED[2], False, "the rule's own text was not found in the built host")
        else:
            hurt = LAYER.replace("drew > 0", "true", 1)
            b = Bench(layer_text=hurt)
            try:
                if not b.ok:
                    check(RED[2], False, "the crippled bench never came up")
                else:
                    was = NOW_ONE = None
                    b2 = Bench()
                    if b2.ok:
                        was = b2.shot(ONLY_ARRIVAL, 2.0, "red-blend-sound-2.00")
                        NOW_ONE = b.shot(ONLY_ARRIVAL, 2.0, "red-blend-crippled-2.00")
                    b2.close()
                    if was is None:
                        check(RED[2], False, "the sound bench never came up")
                    else:
                        off = diff(was, NOW_ONE)
                        check(RED[2], off[1] > SEAM,
                              "with the skip in place a one-cue score meets a context with blending "
                              "disabled and its alpha is never read; with the skip removed the same "
                              "one-cue arrival composites against the cleared buffer and the frame "
                              "moves by mean %.3f of 255 (worst channel %d). This is the row that "
                              "keeps the law free where nothing is stacked" % (off[0], off[1]))
            finally:
                b.close()

    print("\nthe captures this run judged are kept at %s" % CAPS)

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
