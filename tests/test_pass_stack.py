#!/usr/bin/env python3
"""PASS-API-V1 — a stack of cues: several voices on one frame.
Run: python3 tests/test_pass_stack.py

Root: his word 2026-08-14 08:39 — the missing layer is a passage of several voices, with cues
overlapping freely. The composer emits exactly that; until this suite the host took one instrument
per transaction, so a composed passage naming three could not be played at all.

WHAT IS BUILT AND WHAT IS MEASURED HERE.

  The stack. A score names several cues, each with its own instrument, window, works, driver graph
  and declared resources. The host prepares every instrument the score names, draws every live cue
  in ONE frame on THE ONE canvas and THE ONE context, and holds a cue outside its window at its own
  door. Draw order is the score's `stack`, ascending, so the cue nearest the eye is laid down last.

  The order rule is the charter's own, from its log entry of 12.08 opening shelf 7: «A layer's place
  in the stack is written by the score (`stack`) ... where the score names none, the order of its
  lines still puts the first layer topmost.» The lab engine states which way that points —
  lab/crossing-engine.js:552-559, «Higher stands nearer the eye, as everywhere» — so the host walks
  the list ascending and the first line, absent a `stack`, takes the highest number.

  NO OPACITY IS INVOLVED, ANYWHERE. The charter forbids it outright: «a score carries no opacity
  field, the engine hands out no opacity handle», and «a plan physically cannot fade layers». The
  host therefore imposes no weight of its own on any cue. It composites on the alpha the
  INSTRUMENT'S OWN shader writes, so an instrument declaring coverage lets the frame beneath show
  where it carries nothing. All three instruments standing today write `vec4(col, 1.0)`, so each
  covers the frame whole and the stack reads as plain occlusion. That is measured below rather than
  described, and it is the finding this suite carries back.

  The levels law (§4.4, the charter's shelf 17). On one structural level, one owner; every other cue
  on that level names the owner it accompanies there. The composed passage of the worked pair is
  exactly that shape — the band family owns SURFACE for the whole pass and the other two play over
  it — so the row proves both halves: the three cues pass, and one stripped declaration reds.

  The tier budget (§4.4, amended 2026-08-14 10:31). Letters, accompaniments, miracles, duration and
  held time, WITH THE CAMERA COUNTED AS ONE ACCOMPANIMENT wherever the score names a camera track.

  Resources across a stack (§7). With several instruments live at once the grants add up, so the
  declaration compared against a variant's budget is the SUM at the pass's worst instant, and the
  census counts what was actually created against that sum.

THE ACCEPTANCE TARGET IS A PICTURE, and it is the real composed passage of the worked pair:
lab/data/sceneplans/plan-example-17847744487144891__17897050660015868__ab.json. The woven instrument
carries the band family from 0 to 6.5 s and owns SURFACE; the meshing instrument travels from an
angular reading to a ring reading from 1.17 to 5.59 and owns CELL; `matter` carries the arrival from
4.03 to 6.5 and owns TEXTURE; the camera pans as the stage's own voice. Every number in the score
below is read off that plan or off the manifests of the three instruments. None is invented.

  The two photographs are stand-ins. The worked pair's own files are not in this tree, so the walk's
  own two pictures stand in their place. What the rows measure is the stack — which cue draws when,
  in what order, on one canvas — and that is a property of the score, not of which two pictures the
  two texture slots hold.

RESTORING A FILE. Every red-on-bug proof below reverts a rule IN THE BUILT ARTIFACT the browser
loads, from this suite's own copy of it, and never through git. The source tree is never written to,
which also keeps this suite safe to run beside the others under tests/run_all.py.
"""
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
import build as _engine  # noqa: E402  — engine/build.py, already on sys.path via engine_build
from headless import serve, Browser, chrome_available  # noqa: E402

PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame every instrument suite measures on

# ---- the composed passage's own numbers, read off the plan -------------------------------------
PLAN = ("lab/data/sceneplans/"
        "plan-example-17847744487144891__17897050660015868__ab.json")
DUR_MS, DUR = 6500, 6.5
W_PIVOT, W_TRAVEL, W_ARRIVAL = [0.0, 6.5], [1.17, 5.59], [4.03, 6.5]
SEED = 1.983657397                  # the plan's own seed
BAND_HELD = 0.3333                  # the pivot: the band family, held for the whole pass
RATIO_HELD = 0.3333
CENTRE_X, CENTRE_Y = 0.5481, 0.425  # the meshing pair's own centre; the FIELD's centre pans by camera
SIZE_FROM, SIZE_TO = 0.7, 1.8019    # angular to ring; the travel stays above 0.7 by measurement
# The woven instrument's own floor. The measured band family is 480 px of a 1440-px work — three
# bands across the frame — and the woven instrument clamps its strip count to a floor of 6, so the
# score sits ON that floor rather than on the family's own number. Written down because it is a
# measured limit of the port and not a choice: nV = clamp(strips * nMul * clamp(cssWidth/1000,
# 0.5, 1), 6, 64), and at 390 points wide the middle term clamps to 0.5.
PIVOT_STRIPS = 12

# The instants the pass is photographed and read at: both doors and five across the middle.
INSTANTS = [0.0, 1.17, 2.5, 4.03, 5.0, 5.59, 6.5]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score
def _res(variant):
    """What one cue declares, per §7 and per the plan: the two source-texture slots the host already
    holds and the one programme the host builds from the manifest. Nothing of its own."""
    return {"bytesEstimate": 0, "framebuffers": 0, "passes": 1, "pingPong": 0,
            "programs": 1, "textureSlots": 2, "textures": 0, "variant": variant}


RESOURCES = {v: _res(v) for v in ("lean", "standard", "rich")}


def _static(v):
    return {"op": "static", "value": v}


def cue_pivot():
    """THE BAND FAMILY, carried by the woven instrument for the whole pass. It OWNS SURFACE — it is
    the ground the passage stands on — and accompanies the travelling voice on CELL."""
    return {
        "id": "pivot", "instrument": {"api": 1, "id": "weave"},
        "voice": "accompaniment", "roles": ["surface", "breath"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"SURFACE": "owns", "CELL": "accompanies:travel"},
        "window": list(W_PIVOT), "works": ["a", "b"], "stack": 0,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {
            "pivot-mix": {"source": "cueProgress"},
            "pivot-clock": {"source": "time"},
            "pivot-strips": _static(PIVOT_STRIPS),
            "pivot-axis": _static(2),
            "pivot-speed": _static(1),
            "pivot-seed": _static(SEED),
            "pivot-nMul": _static(1),
            "pivot-press": _static(1),
        },
        # `bal` is the instrument's one OPEN handle: a score naming no track for it leaves the
        # balance derived from the dial through the response curve, which is the module's own road.
        "tracks": {"mix": {"node": "pivot-mix"}, "clock": {"node": "pivot-clock"},
                   "strips": {"node": "pivot-strips"}, "axis": {"node": "pivot-axis"},
                   "speed": {"node": "pivot-speed"}, "seed": {"node": "pivot-seed"},
                   "nMul": {"node": "pivot-nMul"}, "press": {"node": "pivot-press"}},
        "resources": dict(RESOURCES),
    }


def cue_travel():
    """SPOKES INTO RINGS, carried by the meshing instrument. It OWNS CELL and accompanies the band
    family on SURFACE. The pair's size carries the radial reading from angular to ring; the band
    period stands still at the pivot; the field's own centre travels by the CAMERA, because the
    meshing handle places where two wheels meet and the measured centre stands a wheel-radius from
    it (lab/PASSAGE-COMPOSER.md, the two corrections of 09:30)."""
    return {
        "id": "travel", "instrument": {"api": 1, "id": "gears"},
        "voice": "miracle", "roles": ["mystery", "world"],
        "levels": ["SURFACE", "CELL"],
        "levelOwnership": {"CELL": "owns", "SURFACE": "accompanies:pivot"},
        "window": list(W_TRAVEL), "works": ["a", "b"], "stack": 1,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {
            "travel-mix": {"source": "cueProgress"},
            "travel-clock": {"source": "time"},
            "travel-size": {"op": "segment", "in": {"source": "cueProgress"}, "points": [
                {"at": 0, "value": SIZE_FROM},
                {"at": 1, "value": SIZE_TO, "shape": "smooth"}]},
            "travel-centreX": _static(CENTRE_X),
            "travel-centreY": _static(CENTRE_Y),
            "travel-bandPeriod": _static(BAND_HELD),
            "travel-ratio": _static(RATIO_HELD),
            "travel-tooth": _static(0.4), "travel-order": _static(0.4),
            "travel-turn": _static(0.55), "travel-flank": _static(0.35),
            "travel-seed": _static(SEED), "travel-shade": _static(1), "travel-travel": _static(1),
        },
        "tracks": {"mix": {"node": "travel-mix"}, "clock": {"node": "travel-clock"},
                   "size": {"node": "travel-size"},
                   "centreX": {"node": "travel-centreX"}, "centreY": {"node": "travel-centreY"},
                   "bandPeriod": {"node": "travel-bandPeriod"}, "ratio": {"node": "travel-ratio"},
                   "tooth": {"node": "travel-tooth"}, "order": {"node": "travel-order"},
                   "turn": {"node": "travel-turn"}, "flank": {"node": "travel-flank"},
                   "seed": {"node": "travel-seed"}, "shade": {"node": "travel-shade"},
                   "travel": {"node": "travel-travel"}},
        "resources": dict(RESOURCES),
    }


def cue_arrival():
    """THE CONDENSING FIGURE, carried by `matter`. It OWNS TEXTURE and accompanies the band family
    on SURFACE. It is the pass's one letter and it holds the last door."""
    return {
        "id": "arrival", "instrument": {"api": 1, "id": "matter"},
        "voice": "letter", "roles": ["assembly"],
        "levels": ["SURFACE", "TEXTURE"],
        "levelOwnership": {"TEXTURE": "owns", "SURFACE": "accompanies:pivot"},
        "window": list(W_ARRIVAL), "works": ["a", "b"], "stack": 2,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": {
            "arrival-mix": {"source": "cueProgress"},
            "arrival-clock": {"source": "time"},
            "arrival-loosen": _static(0.6), "arrival-drift": _static(0.45),
            "arrival-gather": _static(0.3), "arrival-grain": _static(0.45),
            "arrival-seed": _static(SEED), "arrival-shade": _static(1),
            "arrival-travel": _static(1),
        },
        "tracks": {"mix": {"node": "arrival-mix"}, "clock": {"node": "arrival-clock"},
                   "loosen": {"node": "arrival-loosen"}, "drift": {"node": "arrival-drift"},
                   "gather": {"node": "arrival-gather"}, "grain": {"node": "arrival-grain"},
                   "seed": {"node": "arrival-seed"}, "shade": {"node": "arrival-shade"},
                   "travel": {"node": "arrival-travel"}},
        "resources": dict(RESOURCES),
    }


# THE CAMERA IS THE STAGE'S OWN VOICE and it pans so the meeting point travels from work A's radial
# centre to work B's. The plan's four track points carry `a`, `centre-from`, `centre-to` and `b`;
# the two middle ones are placed at the travelling cue's own window edges, since the travel is what
# moves the centre. Every pan and dolly number below is the plan's.
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


def passage(cues=None, camera=True, duration=DUR_MS):
    """The composed passage as a §4.4 score."""
    s = {
        "schema": 2, "duration": duration, "direction": "a-to-b", "failLand": "arrive",
        "seed": SEED, "pair": {"a": "a", "b": "b"}, "intent": INTENT,
        "interruption": {"resolve": "nearest-door", "withinMs": 500},
        "quality": {v: {"renderScale": None} for v in ("lean", "standard", "rich")},
        "provenance": {"source": "sceneplan-v1/17847744487144891__17897050660015868__ab",
                       "measuredAt": "2026-08-14", "by": "lab/build-elements-v1.py"},
        "cues": cues if cues is not None else [cue_pivot(), cue_travel(), cue_arrival()],
    }
    if camera:
        s["camera"] = json.loads(json.dumps(CAMERA))
    return s


def one_cue():
    """A ONE-CUE SCORE, the shape every score on file carries today. Row 2 measures this picture
    against the picture the same score drew before the stack was built."""
    c = cue_pivot()
    c["voice"] = "letter"
    # A LONE CUE OWNS EVERY LEVEL IT STANDS ON. The pivot cue of the composed passage accompanies
    # the travelling voice on CELL, and lifted out on its own there is no such voice to accompany —
    # which the host refuses by name, as the first run of this suite proved by refusing it.
    c["levelOwnership"] = {"SURFACE": "owns", "CELL": "owns"}
    return {
        "schema": 2, "duration": 3000, "direction": "a-to-b", "failLand": "arrive",
        "seed": SEED, "pair": {"a": "a", "b": "b"},
        "intent": "the band family alone, one cue, the shape every score on file carries today",
        "interruption": {"resolve": "nearest-door", "withinMs": 500},
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0, "pitch": 0,
                              "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [c],
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

# WHERE THE LEVELS LAW IS ENFORCED SINCE 2026-08-14 — the composition gate over the authored plans,
# in the tlvphotos tree, which is READ ONLY here. Absent, row 4 is a pinned SKIP naming this path,
# which is the same shape the lab-module rows in test_pass_weave.py use.
GATE = Path(os.environ.get("TLVPHOTOS_SCENEPLAN_ROOT",
                           "/Users/sashaabramovich/tlvphotos-sceneplan/lab")) / "sceneplan-build-check.py"

TMP = Path(tempfile.mkdtemp(prefix="synth_passstack_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# Since 2026-08-14 the instruments ship in their own built file, fetched by the host by address,
# version and digest. A row about the HOST reads LAYER; a row about the shaders reads PACK.
PACK = (TMP / "pass-pack.js").read_text(encoding="utf-8")

# THE SAME FILE AS IT STOOD BEFORE THE STACK WAS BUILT, put through the very same two steps the
# build puts the source through — the namespace resolution and the comment strip — so what row 2
# compares is two builds of one file and never a build against a source.
#
# THE PACK'S OWN ADDRESS IS STAMPED THE WAY THE BUILD STAMPS IT. Until 2026-08-14 the host carried
# its instruments inline and asked for no second file, so the namespace and the comment strip were
# the whole of a build. Since the instruments left for pass-pack.js the host carries two tokens the
# build fills — the pack's version and the digest of the served pack — and a host whose tokens stand
# unfilled refuses every pack it is offered. Left unstamped, this row's older bench drew no
# instrument at all and the comparison read as a whole picture of difference. Both benches serve the
# SAME built pack, so both are stamped with that pack's own numbers and what the row compares is
# again two builds of the host over one picture.
HEAD_BUILT = None
HEAD_PACK = None
HEAD_WHY = ""


def _head_file(path):
    return subprocess.run(["git", "show", "HEAD:" + path],
                          cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8")


def _bake(src):
    return _engine.strip_js_comments(_engine.apply_namespace(src, _engine._NAMESPACE))


try:
    _head = subprocess.run(["git", "show", "HEAD:engine/assets/pass-layer.js"],
                           cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8")
    _served = (TMP / "pass-pack.js").read_bytes()
    _version = re.search(r'var\s+PACK_VERSION\s*=\s*"([^"]+)"', PACK).group(1)
    _head = (_engine.apply_namespace(_head, _engine._NAMESPACE)
             .replace("@@PACK_VERSION@@", _version)
             .replace("@@PACK_DIGEST@@", hashlib.sha256(_served).hexdigest()))
    HEAD_BUILT = _engine.strip_js_comments(_head)
except Exception as e:  # noqa: BLE001 — the reason is reported on the row itself
    HEAD_BUILT = None
    HEAD_PACK = None
    HEAD_WHY = str(e)

# ---------------------------------------------------------------- string rows
# The built artifact, read for the rules that are visible in it. These cost no browser.

check("PASS-STACK the host imposes no opacity of its own on any cue",
      "blendFunc" in LAYER
      and "ONE_MINUS_SRC_ALPHA" in LAYER
      and not re.search(r"\bblendColor\b|\bCONSTANT_ALPHA\b", LAYER)
      and not re.search(r"\bopacity\b", LAYER)
      and not re.search(r"\bopacity\b", PACK),
      "the charter forbids it: «a score carries no opacity field, the engine hands out no opacity "
      "handle» and «a plan physically cannot fade layers». The host composites on the alpha the "
      "instrument's own shader writes and names no weight of its own — so no blendColor, no "
      "constant alpha, and no opacity in the host OR in the pack")

# SUPERSEDED 2026-08-14 by the coverage law. This row used to assert the debt — all three shaders
# writing alpha 1.0, so a stack read as plain occlusion. Coverage landed, so the row now asserts what
# replaced it: the ground fills the frame and the two voices above it publish their own masks.
check("PASS-STACK the ground fills the frame and the voices above it write coverage",
      PACK.count("gl_FragColor = vec4(col, 1.0)") == 1
      and PACK.count("gl_FragColor = vec4(col, 1.0 - cov)") == 2,
      "the woven instrument has no absence to publish — its two ribbon sets partition the frame and "
      "both branches of every mix are picture — so it writes alpha 1.0 and carries the ground. "
      "`matter` and the meshing instrument each publish the mask they already build, 1.0 - cov, the "
      "share of the arriving work, so the frame beneath them reaches the eye where their own matter "
      "is absent")

check("PASS-STACK the draw walks the stack ascending, so the first line is topmost by default",
      "(c.stack === undefined || c.stack === null) ? (n - i)" in LAYER
      and "(p.stack - q.stack) || (q.line - p.line)" in LAYER,
      "the charter's own rule: «where the score names none, the order of its lines still puts the "
      "first layer topmost», and higher stands nearer the eye, so the first line takes n - i and "
      "the walk is ascending")

check("PASS-STACK the camera counts as one accompaniment in the tier budget",
      "if (camera) accompaniments++;" in LAYER,
      "§4.4 amended 2026-08-14 10:31, and the charter's shelf 17: «EVERYTHING counts; no «never "
      "counted» class exists»")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-STACK row 1  · three cues play, each drawing inside its window and nothing outside it",
    "PASS-STACK row 1  · a cue outside its window draws nothing and holds at its own door",
    "PASS-STACK row 2  · a one-cue score is byte-identical to what it drew before the stack",
    "PASS-STACK row 3  · draw order follows `stack`, and the line order where no `stack` is named",
    "PASS-STACK row 4  · the levels law is enforced where the plan is authored",
    "PASS-STACK row 5  · the tier budget holds, with the camera counted as an accompaniment",
    "PASS-STACK row 6  · the summed declaration meets the variant budget, and the census matches",
    "PASS-STACK row 7  · one canvas and one context across a three-cue pass",
    "PASS-STACK row 8  · two cues claiming the camera over meeting windows red, with both named",
    "PASS-STACK row 9  · a seeded three-cue run repeats to the pixel",
    "PASS-STACK row 10 · no empty frame at any sampled instant of a three-cue pass",
    "PASS-STACK row 11 · the census returns to baseline after ten three-cue runs",
    "PASS-STACK row 12 · the console stays clean",
    "PASS-STACK both doors: every live cue draws one picture, so the doors stay exact",
    "PASS-STACK the composed passage of the worked pair plays, and is kept as evidence",
]

RED_ROWS = [
    "PASS-STACK red-on-bug · the camera dropped from the count: accompaniments fall by one",
    "PASS-STACK red-on-bug · the window gate removed: every cue draws at every instant",
    "PASS-STACK red-on-bug · the default stack order reversed: the last line becomes topmost",
    "PASS-STACK red-on-bug · the resource sum reduced to one cue: the census overruns it",
]

missing = [str(p) for p in PHOTOS if not p.exists()]


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def diff(p, q):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, c))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def spread(p):
    """How much picture a frame carries. A frame nothing drew into stands at the canvas's own clear
    colour and has no spread at all, which is what row 10 reads."""
    from PIL import Image, ImageStat
    st = ImageStat.Stat(Image.open(p).convert("L"))
    return st.stddev[0], st.mean[0]


def bench_dir(layer_text, pack_text=None):
    """A served root holding one BUILT pass-layer.js, the two photographs and the fixture.

    THE PACK SERVED MUST BE THE ONE THE HOST WAS STAMPED AGAINST. The host fetches its pack by
    address, weighs its bytes and refuses anything whose digest disagrees, so a bench that serves
    this tree's pack to a host built elsewhere draws nothing at all — which is a blank frame rather
    than a comparison. Row 2 therefore hands its own matching pack, and every other caller takes
    this tree's."""
    d = Path(tempfile.mkdtemp(prefix="synth_stackbench_"))
    (d / "pass-layer.js").write_text(layer_text, encoding="utf-8")
    if pack_text is None:
        shutil.copy2(TMP / "pass-pack.js", d / "pass-pack.js")
    else:
        (d / "pass-pack.js").write_text(pack_text, encoding="utf-8")
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


def live_at(seconds):
    """Which cues the score itself says are playing at this second — computed here, in python, so
    the row compares the host's answer against the score rather than against the host."""
    out = []
    for cid, w in (("pivot", W_PIVOT), ("travel", W_TRAVEL), ("arrival", W_ARRIVAL)):
        if w[0] <= seconds <= w[1]:
            out.append(cid)
    return out


if not chrome_available():
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS + RED_ROWS:
        skip(r, "the walk's own photographs are absent here: " + missing[0])
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_stackshots_"))
    BENCH = bench_dir(LAYER)
    SCORE = json.dumps(passage())
    ONE = json.dumps(one_cue())

    def sample(br, score_json, seconds, dur, name=None):
        """One instant of the pass, held and photographed. The host runs its real frame loop with
        its clock and its progress pinned there, so the same instant reads the same twice."""
        js(br, "return window.__at(%s, %r, %r);" % (score_json, seconds, dur))
        br.sleep(0.55)
        st = js(br, "return window.__stack();")
        shot = png(br, SHOTS / ("%s.png" % name)) if name else None
        br.evaluate("window.__cancel('bench'); 0")
        br.sleep(0.45)
        return st, shot

    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS + RED_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            else:
                # ---- row 1 + row 10 + row 13: the pass, instant by instant -------------------
                walked, shots = [], {}
                for sec in INSTANTS:
                    nm = "passage-%.2f" % sec
                    st, shot = sample(br, SCORE, sec, DUR, nm)
                    walked.append((sec, st))
                    shots[sec] = shot

                wrong = []
                for sec, st in walked:
                    want = live_at(sec)
                    got = [r["id"] for r in st["stack"] if r["live"]]
                    if sorted(got) != sorted(want) or st["drew"] != len(want) \
                            or st["passes"] != len(want):
                        wrong.append((sec, want, got, st["drew"], st["passes"]))
                check(BROWSER_ROWS[0], not wrong,
                      "seven instants of the pass; at each, the cues the host drew against the "
                      "cues the score says are playing, and one pass a frame per live cue. "
                      + ("all seven agree: "
                         + ", ".join("%.2fs→%d" % (s, len(live_at(s))) for s in INSTANTS)
                         if not wrong else "disagreements: %s" % wrong))

                held = []
                for sec, st in walked:
                    off = [(r["id"], r["handles"]) for r in st["stack"]
                           if not r["live"] and r["handles"] is not None]
                    held.append((sec, {i: h.get("mix") for i, h in off}))
                doors_ok = all(
                    all((m == 0.0 if sec < dict(pivot=W_PIVOT, travel=W_TRAVEL,
                                                arrival=W_ARRIVAL)[i][0] else m == 1.0)
                        for i, m in hs.items())
                    for sec, hs in held)
                check(BROWSER_ROWS[1], doors_ok,
                      "a cue outside its window holds at its own door — the entry door before it "
                      "opens and the exit door after it closes: %s" % held)

                empties = [(sec, spread(shots[sec])) for sec in INSTANTS
                           if spread(shots[sec])[0] < 1.0]
                check(BROWSER_ROWS[10], not empties,
                      "the spread of each of the seven frames; a frame nothing drew into stands at "
                      "the canvas's own clear colour and has none. measured: "
                      + ", ".join("%.2fs=%.2f" % (s, spread(shots[s])[0]) for s in INSTANTS)
                      + ("" if not empties else "  EMPTY: %s" % empties))

                # THE TWO DOORS. Every cue's doors name one handle, `mix`, with 0 at the entry and
                # 1 at the exit, so at either door every live cue draws THE SAME picture — the
                # departing work whole at 0, the arriving work whole at the end. That is why a
                # stack lands its doors exactly however the middle composites.
                sample(br, ONE, 0.0, 3.0, "door-a-onecue")
                dmean, dmax = diff(shots[0.0], str(SHOTS / "door-a-onecue.png"))
                check(BROWSER_ROWS[13], dmean <= 1.0,
                      "door A of the three-cue pass against door A of a one-cue pass of the same "
                      "instrument: mean %.4f, worst channel %d of 255. At a door every live cue "
                      "draws one picture, so the stack and the single cue land the same door."
                      % (dmean, dmax))

                # ---- row 3: the order --------------------------------------------------------
                named = js(br, "return window.__order(%s);"
                           % json.dumps([cue_pivot(), cue_travel(), cue_arrival()]))
                bare = [dict(c) for c in (cue_pivot(), cue_travel(), cue_arrival())]
                for c in bare:
                    c.pop("stack", None)
                unnamed = js(br, "return window.__order(%s);" % json.dumps(bare))
                order_named = [r["id"] for r in named]
                order_bare = [r["id"] for r in unnamed]
                check(BROWSER_ROWS[3],
                      order_named == ["pivot", "travel", "arrival"]
                      and order_bare == ["arrival", "travel", "pivot"]
                      and [r["stack"] for r in unnamed] == [1, 2, 3],
                      "draw order is ascending and the last drawn stands nearest the eye. With the "
                      "score's own numbers 0/1/2 the walk is %s, so the arrival is nearest. With "
                      "no number named the first line takes the highest — %s — so the walk is %s "
                      "and the FIRST line is topmost, which is the charter's own sentence."
                      % (order_named, [r["stack"] for r in unnamed], order_bare))

                # ---- row 4: the levels law, and where it now lives ---------------------------
                # MOVED OUT OF THE HOST ON 2026-08-14, AND THE LAW KEEPS ITS FULL FORCE. The
                # declaration it reads is the cue's own `levelOwnership` record, and §4.4's cue
                # allow-list is closed and does not carry that field — a score is refused whole on
                # any unknown field, so a run-time checker here stood on a field no legal score may
                # carry. The levels law is a law about how a passage is COMPOSED and is decidable
                # from the authored plan alone, so it is enforced where the plan is authored.
                #
                # This row reads that gate's own source, the way the browser rows above read the
                # lab modules: the per-level reading that gathers each level's holders, requires
                # every declared level to be owned or accompanied, and refuses two owners of one
                # level. A row that merely asserted the host no longer checks would prove the check
                # was deleted and say nothing about whether the law survived the move.
                three_ok = js(br, "return window.__whyNo(%s);" % SCORE)
                if not GATE.exists():
                    skip(BROWSER_ROWS[4], "the composition gate is not on this machine: %s" % GATE)
                else:
                    gate = GATE.read_text(encoding="utf-8")
                    check(BROWSER_ROWS[4],
                          three_ok is None
                          and 'c.get("levelOwnership")' in gate
                          and '"owns"' in gate
                          and 'for lv in sorted(' in gate,
                          "the host takes the composed passage without a word about levels (%r), "
                          "because the law is checked over the authored plan at build time. Its "
                          "home is %s, which reads each level's holders and refuses two owners of "
                          "one level." % (three_ok, GATE))

                # ---- row 5: the tier budget --------------------------------------------------
                b = js(br, "return window.__budget(%s);" % SCORE)
                # the row 18 shape: two accompaniment cues, a camera, and a middle tier
                two_acc = [cue_pivot(), cue_travel(), cue_arrival()]
                two_acc[1]["voice"] = "accompaniment"      # a second accompaniment beside the pivot
                over = json.dumps(passage(two_acc))
                over_b = js(br, "return window.__budget(%s);" % over)
                over_no = js(br, "return window.__whyNo(%s);" % over)
                nocam = json.dumps(passage(two_acc, camera=False))
                nocam_b = js(br, "return window.__budget(%s);" % nocam)
                nocam_no = js(br, "return window.__whyNo(%s);" % nocam)
                check(BROWSER_ROWS[5],
                      b["tier"] == "middle" and b["letters"] == 1 and b["accompaniments"] == 2
                      and b["miracles"] == 1 and b["camera"] is True and b["held"] == 0.0
                      and three_ok is None
                      and over_b["accompaniments"] == 3 and isinstance(over_no, str)
                      and nocam_b["accompaniments"] == 2 and nocam_no is None,
                      "the composed passage reads middle at %.1f s: %d letter, %d accompaniments "
                      "(the camera among them), %d miracle, held %.3f of a %.3f ceiling — and it "
                      "passes. Make the travelling cue a second accompaniment and the count goes "
                      "2→3 against a middle's ceiling of 2, refused with «%s». Take the camera "
                      "track away from that same score and the count falls 3→2 and it passes — "
                      "which is the whole of what the camera term does."
                      % (b["seconds"], b["letters"], b["accompaniments"], b["miracles"],
                         b["held"], b["heldMax"], over_no))

                # ---- row 6: the summed declaration and the census ----------------------------
                g_std = js(br, "return window.__grant(%s, 'standard');" % SCORE)
                g_lean = js(br, "return window.__grant(%s, 'lean');" % SCORE)
                budgets = js(br, "return window.__budgets();")
                st_end, _ = sample(br, SCORE, 5.0, DUR)
                res = st_end["resources"]
                check(BROWSER_ROWS[6],
                      g_std["variant"] == "standard"
                      and g_std["sum"]["programs"] == 3 and g_std["sum"]["passes"] == 3
                      and g_std["sum"]["textureSlots"] == 6
                      and g_lean["variant"] is None and isinstance(g_lean["why"], str)
                      and res["declared"]["programs"] == 3
                      and res["granted"]["programs"] == 3
                      and res["over"] is False,
                      "the three cues meet at 4.03…5.59 s, so the sum at the pass's worst instant "
                      "is %d programmes, %d passes and %d texture slots. `standard` grants %d/%d/%d "
                      "and takes it; `lean` grants %d/%d/%d and declines with «%s», which is §7's "
                      "own floor. The census then counts %d programmes actually created against "
                      "the %d declared, and does not overrun."
                      % (g_std["sum"]["programs"], g_std["sum"]["passes"],
                         g_std["sum"]["textureSlots"],
                         budgets["standard"]["programs"], budgets["standard"]["passes"],
                         budgets["standard"]["textureSlots"],
                         budgets["lean"]["programs"], budgets["lean"]["passes"],
                         budgets["lean"]["textureSlots"], g_lean["why"],
                         res["granted"]["programs"], res["declared"]["programs"]))

                # ---- row 7: one canvas, one context ------------------------------------------
                st_mid, _ = sample(br, SCORE, 4.5, DUR)
                in_dom = int(br.evaluate("String(window.__canvasCount())"))
                check(BROWSER_ROWS[7],
                      st_mid["canvases"] == 1 and st_mid["contexts"] == 1 and in_dom == 1
                      and st_mid["textures"] == 2 and st_mid["drew"] == 3,
                      "three cues drawing in one frame: %d canvas, %d context, %d canvas element in "
                      "the document, %d source textures, %d cues laid down. The three cues declare "
                      "six texture slots between them and the host binds the SAME two stage "
                      "textures for every one of them, which is why the declared sum is six and "
                      "the census still reads two."
                      % (st_mid["canvases"], st_mid["contexts"], in_dom, st_mid["textures"],
                         st_mid["drew"]))

                # ---- row 8: two cues claiming the camera -------------------------------------
                cam_cues = [cue_pivot(), cue_travel(), cue_arrival()]
                cam_cues[1]["cameraAuthority"] = "own"
                cam_cues[2]["cameraAuthority"] = "own"
                cam_no = js(br, "return window.__whyNo(%s);" % json.dumps(passage(cam_cues)))
                check(BROWSER_ROWS[8],
                      isinstance(cam_no, str) and "travel" in cam_no and "arrival" in cam_no
                      and "camera" in cam_no,
                      "the two cues meet across 4.03…5.59 s and both declare `own`: %r" % cam_no)

                # ---- row 9: a seeded three-cue run repeats to the pixel ----------------------
                _, r1 = sample(br, SCORE, 4.5, DUR, "repeat-1")
                _, r2 = sample(br, SCORE, 4.5, DUR, "repeat-2")
                rmean, rmax = diff(r1, r2)
                check(BROWSER_ROWS[9], rmean == 0.0 and rmax == 0,
                      "one seeded three-cue score, the same instant of the pass photographed "
                      "twice: mean %.6f, worst channel %d of 255" % (rmean, rmax))

                # ---- row 11: the census returns to baseline ---------------------------------
                base_c = js(br, "return window.__stack();")
                for _ in range(10):
                    sample(br, SCORE, 3.0, DUR)
                after_c = js(br, "return window.__stack();")
                check(BROWSER_ROWS[11],
                      after_c["textures"] == base_c["textures"]
                      and after_c["programs"] == base_c["programs"]
                      and after_c["framebuffers"] == base_c["framebuffers"]
                      and after_c["canvases"] == base_c["canvases"]
                      and after_c["contexts"] == base_c["contexts"],
                      "ten three-cue runs: textures %d→%d, programmes %d→%d, framebuffers %d→%d, "
                      "canvases %d→%d, contexts %d→%d"
                      % (base_c["textures"], after_c["textures"],
                         base_c["programs"], after_c["programs"],
                         base_c["framebuffers"], after_c["framebuffers"],
                         base_c["canvases"], after_c["canvases"],
                         base_c["contexts"], after_c["contexts"]))

                # ---- row 12: the console --------------------------------------------------
                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[12], not errs, "console errors across the whole run: %s" % errs)

                # ---- row 14: the evidence ---------------------------------------------------
                check(BROWSER_ROWS[14], all(shots[s] for s in INSTANTS),
                      "the composed passage of the worked pair, photographed at both doors and at "
                      "five instants across the middle, kept at %s: %s"
                      % (SHOTS, ", ".join("%.2fs" % s for s in INSTANTS)))

    shutil.rmtree(BENCH, ignore_errors=True)

    # ---- row 2: the one-cue picture, before the stack and after ---------------------------
    if HEAD_BUILT is None:
        skip(BROWSER_ROWS[2], "the file as it stood before the stack could not be read: " + HEAD_WHY)
    else:
        OLD = bench_dir(HEAD_BUILT, HEAD_PACK)
        NEW = bench_dir(LAYER)
        pair = {}
        for tag, root in (("before", OLD), ("after", NEW)):
            with serve(root) as b2:
                with Browser(width=VW, height=VH) as br2:
                    br2.navigate(b2 + "/index.html")
                    if not ready(br2):
                        pair[tag] = None
                        continue
                    frames = []
                    for sec in (0.0, 1.5, 3.0):
                        js(br2, "return window.__at(%s, %r, 3.0);" % (ONE, sec))
                        br2.sleep(0.55)
                        frames.append(png(br2, SHOTS / ("onecue-%s-%.1f.png" % (tag, sec))))
                        br2.evaluate("window.__cancel('bench'); 0")
                        br2.sleep(0.45)
                    pair[tag] = frames
        if not pair.get("before") or not pair.get("after"):
            skip(BROWSER_ROWS[2], "one of the two benches never came up")
        else:
            offs = [diff(p, q) for p, q in zip(pair["before"], pair["after"])]
            check(BROWSER_ROWS[2], all(m == 0.0 and x == 0 for m, x in offs),
                  "one cue, three instants of the same score, drawn by the file as it stood at HEAD "
                  "and by the file the stack was built into: "
                  + ", ".join("%.1fs mean %.6f worst %d" % (s, m, x)
                              for s, (m, x) in zip((0.0, 1.5, 3.0), offs)))
        shutil.rmtree(OLD, ignore_errors=True)
        shutil.rmtree(NEW, ignore_errors=True)

    # ---- the red-on-bug proofs -------------------------------------------------------------
    # Each reverts ONE rule in the built artifact the browser loads, from this suite's own copy of
    # it, runs the check the rule answers, and puts the copy back. The source tree is never written
    # to and git is never asked to restore anything.
    def red_on_bug(row, find, replace, probe, expect):
        """`probe` is a javascript expression run against the crippled build; the row passes when
        its answer MOVES to `expect`, which is what «reds when the rule is removed» means."""
        if find not in LAYER:
            check(row, False, "the rule's own text was not found in the built file: %r" % find[:60])
            return
        hurt = LAYER.replace(find, replace, 1)
        d = bench_dir(hurt)
        try:
            with serve(d) as b3:
                with Browser(width=VW, height=VH) as br3:
                    br3.navigate(b3 + "/index.html")
                    if not ready(br3):
                        check(row, False, "the crippled bench never came up")
                        return
                    got = js(br3, probe)
                    check(row, got == expect,
                          "with the rule in place the answer is not this; with it removed the "
                          "answer moves to %r, and this run read %r" % (expect, got))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    twoacc = [cue_pivot(), cue_travel(), cue_arrival()]
    twoacc[1]["voice"] = "accompaniment"
    OVERBUDGET = json.dumps(passage(twoacc))
    BARE = json.dumps([{k: v for k, v in c.items() if k != "stack"}
                       for c in (cue_pivot(), cue_travel(), cue_arrival())])

    red_on_bug(RED_ROWS[0],
               "if (camera) accompaniments++;", "",
               "return window.__budget(%s).accompaniments;" % OVERBUDGET, 2)
    ALLCUES = json.dumps([cue_pivot(), cue_travel(), cue_arrival()])
    red_on_bug(RED_ROWS[1],
               "return seconds >= Number(w[0]) && seconds <= Number(w[1]);", "return true;",
               "return window.__live(%s, 0.5);" % ALLCUES,
               ["pivot", "travel", "arrival"])
    red_on_bug(RED_ROWS[2],
               "? (n - i)", "? i",
               "return window.__order(%s).map(function(r){return r.id;});" % BARE,
               ["pivot", "travel", "arrival"])
    red_on_bug(RED_ROWS[3],
               "if (!cueLiveAt(voices[i].cue, edges[k])) continue;", "if (i > 0) continue;",
               "return window.__grant(%s, 'standard').sum.programs;" % json.dumps(passage()), 1)

    print("\nthe captures this run judged are kept at %s" % SHOTS)

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
