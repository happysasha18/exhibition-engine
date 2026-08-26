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

THE ACCEPTANCE TARGET IS A PICTURE, and it is the real composed passage of the worked pair, as the
site serialises it: lab/data/sceneplan-scores/17847744487144891__17897050660015868__ab.json, built
from lab/data/sceneplans/plan-example-17847744487144891__17897050660015868__ab.json. The woven
instrument carries the band family from 0 to 6.5 s and owns SURFACE; the meshing instrument travels
from an angular reading to a ring reading from 0.00 to 5.59 and owns CELL; `matter` carries the
arrival from 4.03 to 6.5 and owns TEXTURE; the camera pans as the stage's own voice. Every number in
the score below is read off that serialised score or off the manifests of the three instruments.
None is invented.

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
SEAM = 6.0                 # the same visual-change seam the door and hang suites use

# ---- the composed passage's own numbers, read off the score the site serialises -----------------
#
# THE ONE HOME OF THESE NUMBERS is the composer's own serialised score for the worked pair, SCORE_SRC
# below, built from the authored plan beside it. This bench holds a frozen copy so it can play the
# passage without the site tree, and a frozen copy goes stale: the copy here still opened the
# meshing cue a fifth of the way into a pass the site has opened at its own door since site commit
# 24f0b45, and still asked the ground for twice the bands the composer measured. Refreshed against
# that score on 2026-08-14, the way the coverage bench was at engine commit 12b9099 — a field at a
# time, every instant that is a window's own edge derived from the window rather than written out:
#   · THE MESHING CUE'S WINDOW, [1.17, 5.59] → [0.00, 5.59]. The travelling voice opens on the
#     pass's own entry door. The camera's two middle track points are placed at that cue's window
#     edges below, so the camera follows the same move — which is what the serialised camera track
#     carries, its middle points standing at 0.00 and 5.59.
#   · THE GROUND'S BAND-COUNT HANDLE, 12 → 3, the number the score carries. The woven instrument
#     draws nV = clamp(strips * nMul * clamp(cssWidth/1000, 0.5, 1), 3, 64) bands
#     (engine/assets/pass-inst-weave.js:220), and on this 390-point frame the middle term clamps to
#     0.5, so a handle of 3 lands on the floor and draws THREE bands — the family the composer
#     measured, 480 px of a 1440-px work — where 12 drew six. The floor itself fell from 6 to 3 on
#     2026-08-14, which is why the old handle had to sit at twice the family's own number.
#   · THE TRAVELLING VOICE'S SIZE RAMP, a smoothed segment climbing 0.7 → 1.8019, becomes the
#     score's own plain mix falling 1.9919 → 0.7: the first work's measured ring reading down to the
#     second's. The upper figure is the composer's own since the plans were re-serialised on
#     2026-08-14 (site commit 7464c50); it read 1.8019 before that. The coverage bench keeps the old
#     direction on purpose, because the score's own reds a row there that nothing may weaken: at
#     that size the meshing pair's meeting line reaches inside the frame at the entry door, and that
#     bench proves an entry door free at EVERY point. No row here asks that of the meshing voice —
#     the door row below measures the whole three-cue stack against a one-cue pass of the same
#     instrument and prints what it read — so this copy carries the score's own ramp.
#   · THE SEED EACH CUE IS HANDED, 1.9837, the four figures the serialiser writes, where the score's
#     own top-level seed keeps its full 1.983657397.
# One divergence is left standing and written down rather than quietly closed: the banding AXIS. The
# score asks for 0 and this copy carries 2, as the coverage bench also does against the same score.
# It is not one of the fields this refresh was asked for, and it belongs to whoever owns the
# composer's own axis reading.
SCORE_SRC = ("lab/data/sceneplan-scores/"
             "17847744487144891__17897050660015868__ab.json")
PLAN = ("lab/data/sceneplans/"
        "plan-example-17847744487144891__17897050660015868__ab.json")
DUR_MS, DUR = 6500, 6.5
W_PIVOT, W_TRAVEL, W_ARRIVAL = [0.0, 6.5], [0.0, 5.59], [4.03, 6.5]
SEED = 1.983657397                  # the score's own seed
CUE_SEED = 1.9837                   # the seed each cue is handed, as the serialiser rounds it
BAND_HELD = 0.3333                  # the pivot: the band family, held for the whole pass
RATIO_HELD = 0.3333
CENTRE_X, CENTRE_Y = 0.5481, 0.425  # the meshing pair's own centre; the FIELD's centre pans by camera
SIZE_FROM, SIZE_TO = 1.9919, 0.7    # angular to ring, the score's own direction and figures
PIVOT_STRIPS = 3

# WHERE THE THREE VOICES MEET, from the windows themselves: the last of the three openings to the
# first of the three closings. Every row that needs all three cues live reads its instant from here
# instead of naming a second, so the rows follow the score when the composer moves a window.
MEET = [max(W_PIVOT[0], W_TRAVEL[0], W_ARRIVAL[0]), min(W_PIVOT[1], W_TRAVEL[1], W_ARRIVAL[1])]
MEET_MID = round((MEET[0] + MEET[1]) / 2.0, 2)

# The instants the pass is photographed and read at: every door and window edge the score itself
# carries, and three readings across the middle. The travelling voice's opening no longer stands
# apart from the entry door — its window begins where the pass does — so 1.17 s, which used to be
# that opening, stays in the grid as one of the middle readings.
INSTANTS = sorted({W_PIVOT[0], W_TRAVEL[0], W_ARRIVAL[0], W_TRAVEL[1], W_PIVOT[1],
                   1.17, 2.5, 5.0})

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
            "pivot-seed": _static(CUE_SEED),
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
            # The score's own shape for this track: a plain mix over the cue's progress, from the
            # first work's measured ring reading to the second's.
            "travel-size": {"op": "mix", "a": SIZE_FROM, "b": SIZE_TO,
                            "t": {"source": "cueProgress"}},
            "travel-centreX": _static(CENTRE_X),
            "travel-centreY": _static(CENTRE_Y),
            "travel-bandPeriod": _static(BAND_HELD),
            "travel-ratio": _static(RATIO_HELD),
            "travel-tooth": _static(0.4), "travel-order": _static(0.4),
            "travel-turn": _static(0.55), "travel-flank": _static(0.35),
            "travel-seed": _static(CUE_SEED), "travel-shade": _static(1),
            "travel-travel": _static(1),
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
            "arrival-seed": _static(CUE_SEED), "arrival-shade": _static(1),
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
# Since 2026-08-14 every instrument ships in a built file of its own, fetched by the host at the
# address the site's own settings record gives its name. A row about the HOST reads LAYER; a row
# about the shaders reads PACK, which is every instrument file this bake wrote.
PACK = "\n".join(p.read_text(encoding="utf-8") for p in sorted(TMP.glob("pass-inst-*.js")))

# THE ARRANGEMENT BEFORE THE LATEST CARRIER CHANGE, rebuilt from git and put through the very same
# steps the
# build puts the source through, so what row 2 compares is two builds and never a build against a
# source. Every part of that arrangement is reconstructed — the host, the picture it draws with, and
# the bench page that drives it — because a host of one arrangement driven by the other's page draws
# nothing at all, and a comparison against nothing reads as a whole picture of difference while
# proving no picture.
#
# The two arrangements the engine has carried are read apart by what HEAD's assets dir holds. One
# pack file: the host is stamped at bake with that pack's version and the digest of its served
# bytes, and it fetches that one file. One file per instrument: the host is stamped with nothing and
# reads every address out of the site's own record, so the record is written here with the digests
# of the bytes this bench actually serves.
HEAD_WHY = ""

# A test committed with the carrier cannot use literal HEAD as its "before": once the commit lands,
# HEAD already contains the new carrier and the comparison becomes new-vs-new.  Follow the latest
# commit that touched the host and use its first parent.  This keeps the proof meaningful after
# cherry-picks and merge commits, while an uncommitted follow-up still compares against the last
# committed carrier boundary.
CARRIER_COMMIT = subprocess.run(
    ["git", "rev-list", "-1", "HEAD", "--", "engine/assets/pass-layer.js"],
    cwd=str(ROOT), capture_output=True, check=True, text=True).stdout.strip()
CARRIER_BEFORE = CARRIER_COMMIT + "^"


def head_text(path):
    return subprocess.run(["git", "show", CARRIER_BEFORE + ":" + path], cwd=str(ROOT),
                          capture_output=True, check=True).stdout.decode("utf-8")


def head_built():
    """The files HEAD's arrangement serves: {served name: text}, with the host under 'pass-layer.js'
    and the site's record under 'config.json' when that arrangement reads one."""
    names = subprocess.run(["git", "ls-tree", "--name-only", CARRIER_BEFORE, "engine/assets/"],
                           cwd=str(ROOT), capture_output=True, check=True).stdout.decode("utf-8")
    names = [n.split("/")[-1] for n in names.split("\n") if n.strip()]
    built = lambda src: _engine.strip_js_comments(_engine.apply_namespace(src, _engine._NAMESPACE))
    layer = _engine.apply_namespace(head_text("engine/assets/pass-layer.js"), _engine._NAMESPACE)
    out = {}
    if "pass-pack.js" in names:
        pack = built(head_text("engine/assets/pass-pack.js"))
        version = re.search(r'var\s+PACK_VERSION\s*=\s*"([^"]+)"',
                            head_text("engine/assets/pass-pack.js")).group(1)
        layer = (layer.replace("@@PACK_VERSION@@", version)
                      .replace("@@PACK_DIGEST@@", hashlib.sha256(pack.encode("utf-8")).hexdigest()))
        out["pass-pack.js"] = pack
    else:
        record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
        rows = {}
        for n in [n for n in names if n.startswith("pass-inst-") and n.endswith(".js")]:
            src = head_text("engine/assets/" + n)
            text = built(src)
            rows[n[len("pass-inst-"):-len(".js")]] = {
                "src": n, "version": re.search(r'var\s+INSTRUMENT_VERSION\s*=\s*"([^"]+)"',
                                               src).group(1),
                "digest": hashlib.sha256(text.encode("utf-8")).hexdigest()}
            out[n] = text
        record["pass"]["instruments"] = rows
        out["config.json"] = json.dumps(record)
    out["pass-layer.js"] = _engine.strip_js_comments(layer)
    out["index.html"] = head_text("tests/fixture_pass_stack.html")
    return out


try:
    HEAD_BUILT = head_built()
except Exception as e:  # noqa: BLE001 — the reason is reported on the row itself
    HEAD_BUILT = None
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
# writing alpha 1.0, so a stack read as plain occlusion. Coverage landed, so the row asserts what
# replaced it: the instruments that carry a ground fill the frame, and every voice standing over one
# publishes its own mask.
#
# 2026-08-17 — READ PER INSTRUMENT, where the row used to count occurrences over the whole pack. The
# counts were 1 and 2 when three instruments shipped and stayed right through `adrift`, whose alpha
# is neither literal; `unfold` lands as a second frame-filling ground and the counts stop describing
# the fleet. What the law says is a pairing — an instrument that declares it writes no coverage writes
# the constant 1, and one that declares it writes coverage writes an alpha its own shader computed —
# so the row reads that pairing off each file.
BUILT = {p.name[len("pass-inst-"):-len(".js")]: p.read_text(encoding="utf-8")
         for p in sorted(TMP.glob("pass-inst-*.js"))}
NAMES = sorted(BUILT)


def _declares(src):
    m = re.search(r"coverage:\s*\{\s*writes:\s*(true|false)", src)
    return m.group(1) if m else None


# THE LAW IS ABOUT THE ALPHA, so the alpha is what is read: the LAST component of the write, not
# the whole argument list. Reading the list whole held only while every colour expression was the
# bare word `col`; `livemirror` writes its half-level dither into the colour and fills the frame
# lawfully with an alpha of exactly 1, and the row went red on the COLOUR while the alpha it judges
# was right. The split is at the last comma outside any bracket.
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

check("PASS-STACK the ground fills the frame and the voices above it write coverage",
      bool(FILLS) and bool(PUBLISHES)
      and len(FILLS) + len(PUBLISHES) == len(NAMES)
      and all(_alpha(BUILT[n]) == "1.0" for n in FILLS)
      and all(_alpha(BUILT[n]) and _alpha(BUILT[n]) != "1.0" for n in PUBLISHES),
      "the declaration and the shader are one statement read twice. Filling the frame and writing "
      "alpha 1.0, which is what a stack stands on: "
      + ", ".join("«%s»" % n for n in FILLS)
      + ". Publishing an alpha the shader itself computed, so the frame beneath reaches the eye "
        "where their own matter is absent: "
      + ", ".join("«%s» writing an alpha of «%s» in «%s»"
                  % (n, _alpha(BUILT[n]), _write(BUILT[n])) for n in PUBLISHES))

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
    "PASS-STACK row 2  · the full-source carrier deliberately supersedes HEAD's cropped canvas",
    "PASS-STACK row 3  · draw order follows `stack`, and the line order where no `stack` is named",
    "PASS-STACK row 4  · the levels law is enforced where the plan is authored",
    "PASS-STACK row 5  · the tier budget is reckoned and recorded and refuses nothing, with the "
    "camera counted as an accompaniment",
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


def bench_dir(layer_text=None, arrangement=None):
    """A served root holding one BUILT pass-layer.js, the picture it draws with, the two photographs
    and the fixture.

    With no argument it stands THIS branch's arrangement: the built host, the site's own record and
    the instrument files that record names, each fetched by the host as a visitor's browser fetches
    them. `layer_text` replaces the host alone, which is how a red-on-bug proof serves a crippled
    one. `arrangement` stands a whole arrangement of its own — every served file by name — which is
    how row 2 stands HEAD's beside this one."""
    d = Path(tempfile.mkdtemp(prefix="synth_stackbench_"))
    if arrangement:
        for name, text in arrangement.items():
            (d / name).write_text(text, encoding="utf-8")
    else:
        (d / "pass-layer.js").write_text(layer_text or LAYER, encoding="utf-8")
        # Each instrument travels as its own file, and the host reads every address out of the
        # site's own settings record, so the bench root serves that record and the files it names.
        shutil.copy2(TMP / "config.json", d / "config.json")
        for _inst in sorted(TMP.glob("pass-inst-*.js")):
            shutil.copy2(_inst, d / _inst.name)
        shutil.copy2(ROOT / "tests" / "fixture_pass_stack.html", d / "index.html")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
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
                sample(br, ONE, W_PIVOT[0], 3.0, "door-a-onecue")
                dmean, dmax = diff(shots[W_PIVOT[0]], str(SHOTS / "door-a-onecue.png"))
                check(BROWSER_ROWS[13], dmean <= 1.0,
                      "door A of the three-cue pass at %.2f s against door A of a one-cue pass of "
                      "the same instrument: mean %.4f, worst channel %d of 255. At a door every "
                      "live cue draws one picture, so the stack and the single cue land the same "
                      "door. Since the travelling voice's window now opens on the pass's own entry "
                      "door it is live here too, and it lands the same door because its shader "
                      "publishes the arriving work's absence as its own alpha: at the entry door "
                      "that work is absent everywhere, so it covers nothing."
                      % (W_PIVOT[0], dmean, dmax))

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
                # allow-list does not carry that field, so a run-time checker here stood on a field
                # no legal score may carry. The levels law is a law about how a passage is COMPOSED
                # and is decidable from the authored plan alone, so it is enforced where the plan is
                # authored.
                #
                # THE SECOND HALF OF THAT ARGUMENT WAS COUNTERFACTUAL UNTIL 2026-08-25, and this
                # note is what it cost to state plainly. It used to read that a score is «refused
                # whole on any unknown field», so `levelOwnership` could never arrive here. No such
                # checker existed on the road a visitor's crossing travels: `passScoreCheck` read
                # the envelope's own keys and never descended into `cues`, and the composer's
                # `serialise` holds a deny-list of the four plan-only names that judges output the
                # composer has just built — it can only catch the composer contradicting itself. So
                # the field the law was said to be unable to reach was reaching the host in cue
                # records across this suite and others, and playing, because nothing looked. The cue
                # allow-list is checked from 2026-08-25 (`PASS_CUE_FIELDS`), and it STRIPS rather
                # than refusing whole — §4.4 amended the same day. The move of the law is right for
                # its own reason, which is the sentence above this one: the law is about how a
                # passage is composed and needs nothing from a live frame. It never needed an
                # allow-list that was not there to hold it up.
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
                # THE TIER BUDGET IS RECKONED AND RECORDED AND IT REFUSES NOTHING (2026-08-18,
                # his word of 09:51). It refused a whole crossing until that morning, and a second
                # reckoning at the host could only disagree with the composer's first — a
                # well-formed score with every instrument ready, refused for a count. So the row
                # holds both halves of what now stands: the reckoning still counts exactly as it
                # did, and the score still plays. The camera term is proved the same way it always
                # was, by taking the camera track away and watching the count fall.
                check(BROWSER_ROWS[5],
                      b["tier"] == "middle" and b["letters"] == 1 and b["accompaniments"] == 2
                      and b["miracles"] == 1 and b["camera"] is True and b["held"] == 0.0
                      and b["why"] is None and three_ok is None
                      and over_b["accompaniments"] == 3 and isinstance(over_b["why"], str)
                      and over_no is None
                      and nocam_b["accompaniments"] == 2 and nocam_b["why"] is None
                      and nocam_no is None,
                      "the composed passage reads middle at %.1f s: %d letter, %d accompaniments "
                      "(the camera among them), %d miracle, held %.3f of a %.3f ceiling — and it "
                      "plays. Make the travelling cue a second accompaniment and the count goes "
                      "2→3 against a middle's ceiling of 2: the reckoning records «%s» and the "
                      "score is NOT refused for it — the crossing plays and the count stands on the "
                      "diagnostic surface where a person can read it. Take the camera track away "
                      "from that same score and the count falls 3→2 and the reckoning has nothing "
                      "to record — which is the whole of what the camera term does."
                      % (b["seconds"], b["letters"], b["accompaniments"], b["miracles"],
                         b["held"], b["heldMax"], over_b["why"]))

                # ---- row 6: the summed declaration and the census ----------------------------
                g_std = js(br, "return window.__grant(%s, 'standard');" % SCORE)
                g_lean = js(br, "return window.__grant(%s, 'lean');" % SCORE)
                budgets = js(br, "return window.__budgets();")
                st_end, _ = sample(br, SCORE, MEET_MID, DUR)
                res = st_end["resources"]
                check(BROWSER_ROWS[6],
                      g_std["variant"] == "standard"
                      and g_std["sum"]["programs"] == 3 and g_std["sum"]["passes"] == 3
                      and g_std["sum"]["textureSlots"] == 6
                      and g_lean["variant"] is None and isinstance(g_lean["why"], str)
                      and res["declared"]["programs"] == 3
                      and res["granted"]["programs"] == 3
                      and res["over"] is False,
                      "the three cues meet at %.2f…%.2f s — the windows' own overlap, read here at "
                      "%.2f s — so the sum at the pass's worst instant is %d programmes, %d passes "
                      "and %d texture slots. `standard` grants %d/%d/%d "
                      "and takes it; `lean` grants %d/%d/%d and declines with «%s», which is §7's "
                      "own floor. The census then counts %d programmes actually created against "
                      "the %d declared, and does not overrun."
                      % (MEET[0], MEET[1], MEET_MID,
                         g_std["sum"]["programs"], g_std["sum"]["passes"],
                         g_std["sum"]["textureSlots"],
                         budgets["standard"]["programs"], budgets["standard"]["passes"],
                         budgets["standard"]["textureSlots"],
                         budgets["lean"]["programs"], budgets["lean"]["passes"],
                         budgets["lean"]["textureSlots"], g_lean["why"],
                         res["granted"]["programs"], res["declared"]["programs"]))

                # ---- row 7: one canvas, one context ------------------------------------------
                st_mid, _ = sample(br, SCORE, MEET_MID, DUR)
                in_dom = int(br.evaluate("String(window.__canvasCount())"))
                check(BROWSER_ROWS[7],
                      st_mid["canvases"] == 1 and st_mid["contexts"] == 1 and in_dom == 1
                      and st_mid["textures"] == 2 and st_mid["drew"] == 3,
                      "three cues drawing in one frame: %d canvas, %d context, %d canvas element in "
                      "the document, %d source textures, %d cues laid down. The three cues declare "
                      "six texture slots between them and the host binds the SAME two stage "
                      "textures for every legacy voice; an explicit scene-reading manifest lazily "
                      "activates the one auxiliary carrier texture."
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
                      "the two cues meet across %.2f…%.2f s — their windows' own overlap — and both "
                      "declare `own`: %r"
                      % (max(W_TRAVEL[0], W_ARRIVAL[0]), min(W_TRAVEL[1], W_ARRIVAL[1]), cam_no))

                # ---- row 9: a seeded three-cue run repeats to the pixel ----------------------
                _, r1 = sample(br, SCORE, MEET_MID, DUR, "repeat-1")
                _, r2 = sample(br, SCORE, MEET_MID, DUR, "repeat-2")
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
        skip(BROWSER_ROWS[2], "the arrangement as it stands at HEAD could not be rebuilt: " + HEAD_WHY)
    else:
        OLD = bench_dir(arrangement=HEAD_BUILT)
        NEW = bench_dir()
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
            check(BROWSER_ROWS[2], all(m > SEAM for m, _ in offs),
                  "the carrier now moves the whole canvas box hang→scene→hang, so it MUST differ "
                  "from HEAD's fullscreen centre crop; PASS-HANG separately gates both endpoints "
                  "against the live DOM. Differences: "
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
