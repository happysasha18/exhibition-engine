#!/usr/bin/env python3
"""PASS-API-V1 — the woven instrument on the host's frame.
Run: python3 tests/test_pass_weave.py

Root: his word 2026-08-13 23:03 — carry the woven instrument across first, with a real pair score
feeding a real instrument. docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and
§9's conformance rows 7, 10, 14, 15 and 22 are what this file makes real; the lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the strips' travel needs
  (the module's own ZOOM) — inside the project's seam threshold of 6 of 255. A door that carried a
  ten-thousandth of the other photograph would fail this, which is the point of it.

  The three poses. The host's frame is compared against the LAB MODULE's own frame, on one pose
  taken from the module through its own pose() — the same three poses lab/carrier-check.py already
  uses (the two doors and the woven middle, at second 7). Two roads of one frame, never two guesses
  at one.

  Three bands. The count the lowered floors exist for, on the worked pair's own two works and on
  both frames it has to hold on: a handle of 3 on 1440 px and a handle of 6 on the 390 px phone,
  each drawing three bands. This one is asked of the SHIPPED instrument alone — the lab module
  cannot be brought to it, for the reason written at BAND_ROWS below — and the drawn frame is read
  by the collection's own banding measure (lab/cut-lines.py, imported) to say where the band family
  actually lands: 1440 / 3 is the pair's own period of 480 px, and 390 / 3 is 130 px.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.

WHERE THE SCORE COMES FROM, AND WHY IT IS NO LONGER A FILE.

  Every row below that offers this instrument a score used to read one off disk:
  lab/data/scores/17847744487144891__17897050660015868.json — a stored score keyed by an ordered
  PAIR of work ids. His word of 2026-08-17 19:21 retired that whole shape, and site commit e25bbc8
  («Nothing on disk carries a row per pair of works any more; what two photographs share is worked
  out when they meet») deleted the directory and the builder that wrote it. From then until
  2026-09-07 this suite went on asking for the file, found it absent, and abstained on all
  thirty-nine of its browser rows — reporting green over rows that never ran, because a SKIP is an
  abstention and not a pass.

  The score is now COMPOSED, by the shipped `engine/assets/pass-composer.js`, for a pair of
  constructed WorkRecords out of `tests/synthetic_works.py` — the same fixed corpus of boundary
  values and behaviour classes `tests/test_pass_composed.py` and `tests/test_pass_reads.py` stand
  on. Nothing in it names a photograph and nothing in it grows when the collection does. The pair is
  not chosen by hand either: the walk takes the FIRST case of `synthetic_works.pairs()` whose
  composed passage names the woven instrument and names nothing else, so the rows that count what
  the host made — one programme, two textures, one pass a frame — are counting this instrument
  alone. What reaches the host is the composer's own serialised `json`, byte for byte the string a
  visitor's browser is handed.
"""
import base64
import hashlib
import json
import math
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
import synthetic_works  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

LAB = Path(os.environ.get("TLVPHOTOS_LAB_ROOT", "/Users/sashaabramovich/tlvphotos/lab"))
# The two photographs lab/carrier-check.py itself compares on; they live in the main worktree, which
# the immersive one does not copy. Either root is read only here.
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
# THE WORKED PAIR'S OWN TWO WORKS, which the three-band rows below are read on. The band family the
# composed passage stands on was measured on THESE two: vertical, period 480 px in a 1440 px frame,
# held at 0.8807 and 0.8437 (lab/data/cut-lines.json). A drawn frame read on any other pair answers
# a different question, so the acceptance names its own two files.
PAIR_WORKS = [Path("/Users/sashaabramovich/tlvphotos/gallery/assets/"
                   "constructed/17847744487144891.jpg"),
              Path("/Users/sashaabramovich/tlvphotos/gallery/assets/"
                   "coda/17897050660015868.jpg")]
# The collection's own banding measure, IMPORTED and not copied — the very function that read the
# two numbers above off the two photographs. A copy could drift from the number the pair was judged
# by, which is the same rule lab/weave-bands-measure.py states for itself.
CUT_LINES = LAB / "cut-lines.py"

# THE COMPOSER THAT SHIPS, AND THE CONSTANTS IT IS MADE WITH. Read out of the engine's own assets
# rather than out of a bake, so the score every row below is offered is composed by exactly the file
# a visitor's browser fetches.
COMPOSER_MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE_COMPOSED = ROOT / "tests" / "fixture_pass_composed.json"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


# THE COMPOSE DRIVER'S OWN CEILING. The walk below runs the shipped composer over the corpus's own
# ordered pair cases in ONE node process and stops at the first pair that names the woven instrument
# alone; a lone run of it measured 1.0 s on 2026-09-07. tests/run_all.py's own default is `--jobs 8`,
# so under the gate that work shares the host with seven other suites, and the ceiling is that
# measured cost against the runner's own declared job count — both numbers already written down. A
# driver that truly hangs still ends here rather than never.
COMPOSE_TIMEOUT_S = 1.0 * 8

# THE ONE WALK THAT COMPOSES WHAT THIS SUITE PLAYS. It answers two questions in one node process,
# because both are questions about what the shipped composer emits for constructed works:
#
#   · THE SCORE. The first ordered pair case of `synthetic_works.pairs()` whose composed passage
#     carries exactly one cue and that cue is the woven instrument. The score handed back is the
#     composer's own `json` — the serialised string a visitor's browser is handed — so nothing this
#     file does can reshape it on the way.
#   · THE BANDING AXIS AS THE COMPOSER ENCODES IT. For every pair whose passage names the woven
#     instrument, the value the composer put on that cue's `axis` node, beside the banding axis each
#     of the two constructed works actually carries. The row below reads the encoding off those
#     answers rather than off a sentence anybody typed.
COMPOSE_DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [composerPath, fixPath, worksPath] = process.argv.slice(2);
let joined = null;
const sandbox = {window: {}, console: {log: () => {}, warn: () => {}, error: () => {}}};
sandbox.window.__PassComposer = (m) => { joined = m; };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(composerPath, "utf8").replace(/@@NS@@/g, ""), sandbox,
                {filename: composerPath});
if (!joined) { console.log(JSON.stringify({error: "the composer joined nothing"})); process.exit(0); }
const fix = JSON.parse(fs.readFileSync(fixPath, "utf8"));
const data = JSON.parse(fs.readFileSync(worksPath, "utf8"));
const works = data.works, pairs = data.pairs;
const composer = joined.make(fix.consts);
// The seed the whole corpus is walked at in tests/test_pass_reads.py, carried here for the same
// reason: one die for one walk, so a repeat of this suite composes the same passage.
const SEED = 3.3;
let alone = null;
const axis = [];
for (const c of pairs) {
  const a = c[0], b = c[1], dir = c[2];
  let p;
  try {
    p = composer.passageFor({workRecordA: works[a], workRecordB: works[b], direction: dir,
                             seed: SEED, routeRole: "middle"});
  } catch (e) { continue; }
  if (!p || !p.score) continue;
  const cues = p.score.cues || [];
  const woven = cues.filter((c2) => c2.instrument && c2.instrument.id === "weave");
  if (!woven.length) continue;
  const node = woven[0].nodes[((woven[0].tracks || {}).axis || {}).node];
  if (node && typeof node.value === "number") {
    axis.push({a: a, b: b, dir: dir, value: node.value,
               bandingA: works[a].structure.banding.axis,
               bandingB: works[b].structure.banding.axis});
  }
  if (!alone && cues.length === 1) {
    alone = {a: a, b: b, dir: dir, json: p.json, cue: woven[0].id};
  }
}
console.log(JSON.stringify({alone: alone, axis: axis}));
"""


def compose():
    """Runs the walk above under a real `node` and returns its answer, or {"error": ...} naming what
    went wrong — so a row that could not be composed reads as a stated failure rather than a silent
    pass. Same shape as tests/test_pass_reads.py's own driver runner."""
    d = Path(tempfile.mkdtemp(prefix="synth_weavecompose_"))
    try:
        (d / "driver.js").write_text(COMPOSE_DRIVER, encoding="utf-8")
        (d / "works.json").write_text(
            json.dumps({"works": synthetic_works.corpus(), "pairs": synthetic_works.pairs()}),
            encoding="utf-8")
        proc = subprocess.run(["node", str(d / "driver.js"), str(COMPOSER_MODULE),
                               str(FIXTURE_COMPOSED), str(d / "works.json")],
                              capture_output=True, text=True, timeout=COMPOSE_TIMEOUT_S)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-400:]}
        lines = proc.stdout.strip().splitlines()
        if not lines:
            return {"error": "the compose driver printed nothing"}
        return json.loads(lines[-1])
    except subprocess.TimeoutExpired:
        # A TIMEOUT IS AN EMERGENCY STOP AND NEVER A VERDICT — this tree's own standing law
        # (tlvphotos CLAUDE.md, "No clock on this machine", the owner's word of 2026-09-07 19:47;
        # the pack says the same in guardrails.config.json as `timeout_is_never_a_verdict`). The
        # ceiling above bounds a driver that truly HANGS. A busy host reaching it says nothing about
        # any instrument, and letting it fall through to the generic handler below turned one stop
        # into a row per instrument, each reading FAIL and naming something that was never measured:
        # on 2026-09-09 this suite printed 24 such rows under four parallel lanes and passed on its
        # own minutes later. So the run ENDS here, with its own exit code, and writes no row it
        # cannot stand behind. A suite that can go red because the host was busy is a defect in that
        # suite, and this is where that defect is repaired.
        print("\nSTOPPED — the compose driver hit its emergency stop at %g s without\n"
              "finishing. Nothing above is a verdict on any instrument. Run this suite\n"
              "on its own for one."
              % COMPOSE_TIMEOUT_S)
        sys.exit(3)
    except Exception as e:
        return {"error": str(e)}
    finally:
        shutil.rmtree(d, ignore_errors=True)


COMPOSED = compose() if node_available() else {"error": "node is not installed"}
COMPOSED_WHY = (COMPOSED.get("error")
                or (None if COMPOSED.get("alone") else
                    "no ordered pair case of the constructed corpus composes a passage naming the "
                    "woven instrument alone"))


def score_of():
    """The score the shipped composer emits for a constructed pair, parsed out of its own serialised
    `json`. One fresh copy per call, because every caller below edits the one it is handed."""
    return json.loads(COMPOSED["alone"]["json"])


def scored(pair_a="a", pair_b="b"):
    """That composed score, with the two work slots named for whatever the caller is arming.

    NOTHING ELSE IS ADDED, and that is the change of 2026-09-07. The generator this suite used to
    read wrote only `mix` and `clock` into `tracks`, because lab/module-contract.json published only
    those two, so this file had to wire the other seven handles up by hand before a row could claim
    the instrument was driven rather than resting on its defaults. The shipped composer publishes all
    twelve — the strips, the axis, the speed, the die, the press, the strip-count multiplier and the
    ribbon's three wave handles — each with the measurement it was placed from written on the node's
    own `note`. A hand-written track laid over that would be this file overruling the composer and
    then proving its own arithmetic back to itself.

    `bal` is deliberately NOT tracked, by the composer and by this file alike: the balance is the
    open handle the dial owns through a crossing. A row that needs a door at a stated balance names
    `tracks.bal` itself, which is what `balanced` below does and the only way a score reaches it."""
    s = score_of()
    s["pair"] = {"a": pair_a, "b": pair_b}
    return s


def balanced(bal, pair_a="a", pair_b="b", strips=None):
    """The same score with the OPEN handle driven — the one case in which a door of this instrument
    can stand at a balance other than the one the response curve puts it at. `bal` is open by
    declaration (`open: true` in the manifest), so a score that names a track for it wins over the
    dial, and at a door the fabric then leaves a share of every band to the other work. That is the
    door this lane's reading is about, and this is the only way a score reaches it.

    WHY A ROW ABOUT A REFUSED DOOR ALSO NAMES `strips`. The instrument holds a leaking door at the
    fabric's own whole band wherever one stands within DOOR_HOLD = 2 bands of the balance handed in
    (pass-inst-weave.js:718), and the share a balance leaves open is a share of EVERY band — so the
    distance in bands is that share times the count drawn. On this 390-point frame the composed
    score's own measured family draws the instrument's floor of three bands, at which a balance of a
    half stands 0.69 of a band from whole: every balance is inside the hold, no door can be refused,
    and a row about a refusal has nothing to read. Naming the instrument's own declared default of
    28 puts the count at fourteen bands on the same frame, where a half stands 3.24 bands out and
    the refusal the row is about is reachable. It is the handle's own published default, not a
    number chosen here, and only the rows about a REFUSAL name it."""
    s = scored(pair_a, pair_b)
    cue = s["cues"][0]
    cue["nodes"]["balStatic"] = {"op": "static", "value": bal,
                                 "note": "the open handle driven flat, so the door stands where "
                                         "this number puts it rather than where the dial does"}
    cue["tracks"]["bal"] = {"node": "balStatic"}
    if strips is not None:
        cue["nodes"]["stripsAlt"] = {"op": "static", "value": strips}
        cue["tracks"]["strips"] = {"node": "stripsAlt"}
    return s


def coupled(pair_a="a", pair_b="b"):
    """ONE NODE FEEDING TWO CHANNELS — the fifth law of the grammar, on the real instrument. One
    breath drives the strip count AND the press, so the two cannot disagree; the row reads both
    handles off the diagnostic surface and solves them back to the single value they came from.

    THE BREATH IS AUTHORED HERE AND NOWHERE ELSE, because the law is about the graph and not about
    this instrument's own taste. The composed score drives `nMul` and `press` from the crossing's own
    progress, each off a node of its own, which is the right thing for a passage and the wrong shape
    for this row: two nodes cannot prove that one node reaches two channels. So this score replaces
    both tracks with the single oscillator below and the two expressions that read it.

    Its two numbers are the module's own, carried digit for digit out of lab/effects/weave.js: the
    strip-count breath 1 + 0.35·sin(t·0.021·TAU + 1.1) (weave.js:452) and the press resting at 1
    under a parked pointer (weave.js:466 with :236)."""
    s = scored(pair_a, pair_b)
    cue = s["cues"][0]
    cue["nodes"]["breath"] = {"op": "oscillate", "rate": 0.021, "phase": 1.1, "shape": "sin",
                              "in": {"source": "time"},
                              "note": "lab/effects/weave.js:452 — the strip-count drift's own rate "
                                      "and its own head start, unchanged"}
    cue["nodes"]["nMulDrive"] = {"op": "add", "in": [{"op": "static", "value": 1},
                                                     {"op": "multiply",
                                                      "in": [{"op": "static", "value": 0.35},
                                                             {"node": "breath"}]}]}
    cue["nodes"]["pressDrive"] = {"op": "add", "in": [
        {"op": "static", "value": 1},
        {"op": "multiply", "in": [{"op": "static", "value": 0.30},
                                  {"op": "clamp", "in": {"node": "breath"}, "min": 0, "max": 1}]}]}
    cue["tracks"]["nMul"] = {"node": "nMulDrive"}
    cue["tracks"]["press"] = {"node": "pressDrive"}
    return s


def with_statics(strips=None, nMul=None, press=None, pair_a="a", pair_b="b"):
    """The same score with one voice moved. Used to prove a handle reaches the PICTURE and not only
    the diagnostic record — reading a driver's value back off the surface says the graph evaluated,
    and says nothing about whether the instrument obeyed it.

    `strips` is raised to 28, the module's own declared default, for these runs alone: the composed
    score names the band family it measured on the constructed pair, which is a handful of strips,
    and on a 390-point frame the count lands at clamp(strips * nMul * 0.5, 3, 64), whose floor
    swallows the whole of the breath's range at so few. At 28 the same range moves the count from
    about ten strips to about twenty, which is the difference the row is trying to see."""
    s = scored(pair_a, pair_b)
    cue = s["cues"][0]
    if strips is not None:
        cue["nodes"]["stripsAlt"] = {"op": "static", "value": strips}
        cue["tracks"]["strips"] = {"node": "stripsAlt"}
    if nMul is not None:
        cue["nodes"]["nMulAlt"] = {"op": "static", "value": nMul}
        cue["tracks"]["nMul"] = {"node": "nMulAlt"}
    if press is not None:
        cue["nodes"]["pressAlt"] = {"op": "static", "value": press}
        cue["tracks"]["press"] = {"node": "pressAlt"}
    return s


def breath_at(seconds):
    """The very formula the node above carries, computed here so the row states its number instead of
    reading one back and calling it correct."""
    return math.sin(2 * math.pi * 0.021 * seconds + 1.1)


# ---------------------------------------------------------------- bake once
# The site's own `pass` record. This is the WHOLE delivery road: a site writes the block into its own
# site.json, engine/build.py passes it through into config.json as DATA and judges nothing in it, and
# the client reads the names it knows at declare time. No engine rebuild, no new asset, no new road.
#
# `deliveryProbe` is a name the bake has never heard of and the client has no register row for, put
# here on purpose: it is what makes the row below a proof about the CONTENT rather than about two
# settings that happen to survive. A block is data, so a member of a shape neither side knows must
# reach the served file unread and unaltered — that is what lets a score road change without an
# engine rebuild, and it is the half of the retired row above that did not retire with it. The
# client passes over a name its register does not carry rather than refusing the block, which is
# the same law read from the other end.
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {
    "visualLayer": "pass", "diagnostics": "on",
    "deliveryProbe": {"schema": 1, "rows": [1, 2.5, "три"], "nested": {"depth": {"here": None}}},
}

TMP = Path(tempfile.mkdtemp(prefix="synth_passweave_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# Since 2026-08-14 the instruments ship in their OWN built file, which the host fetches by address,
# version and digest. A row about the HOST reads LAYER; a row about the woven instrument's own
# mathematics reads its region of PACK. Splitting the two is what lets the boundary row in
# test_pass_pack.py demand that no instrument name appear in the host at all.
PACK = "\n".join(p.read_text(encoding="utf-8") for p in sorted(TMP.glob("pass-inst-*.js")))
WEAVE = (TMP / "pass-inst-weave.js").read_text(encoding="utf-8")
# The one script in this tree that raises a bench of its own for this instrument; it has to serve
# the same two files a visitor is served, and a row below holds it to that.
CAPTURE = (ROOT / "scripts" / "capture-weave.py").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

check("PASS-WEAVE the host binds uniforms by declared name, never by position or a written list",
      "u.name" in LAYER and "getUniformLocation(p, u.name)" in LAYER
      and "gl.uniform1f(U.uNv" not in LAYER,
      "the lab carrier names one instrument's six uniforms literally; the host must read the manifest")

check("PASS-WEAVE a shader that already carries its own version header receives no second one",
      'if (/^\\s*#version\\b/.test(src)) return src;' in LAYER,
      "two lab modules ship GLSL ES 3.00 already — a second header is a build-time red")

check("PASS-WEAVE the host's own context leaves the drawing buffer unpreserved",
      "preserveDrawingBuffer: false" in LAYER,
      "one canvas, one context, nothing kept between frames (§7)")

check("PASS-WEAVE the woven instrument creates no context, no canvas, no loop and no listener",
      all(s not in WEAVE
          for s in ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
                    "performance.now", "Date.now", "new Image"]),
      "§1.2's fence, read against the instrument's own region of the file")

check("PASS-WEAVE every handle the instrument publishes is a handle a score can drive",
      all(('%s: { min' % h) in WEAVE for h in
          ["mix", "clock", "strips", "axis", "speed", "seed", "nMul", "press", "bal"]),
      "§4.4b: a handle that keeps its own clock or its own roll makes the determinism row red — "
      "`nMul`, `press` and `bal` were the three that answered to no track until 2026-08-14")

check("PASS-WEAVE the instrument reads its balance, its strip-count breath and its press from handles",
      "nMul: h.nMul, press: h.press" in WEAVE
      and "typeof h.bal === \"number\" ? h.bal :" in WEAVE
      and WEAVE.count("nMul: 1, press: 1") == 1,
      "the two constants standing where the module's own eased clock used to run are gone — the one "
      "remaining pair is the manifest's neutral pose, which is a pose and not a channel")

# ---- the response curves, measured 2026-08-17 ----------------------------------------------------
# The charter's law: equal movement of the hand, equal felt change. This instrument carried one
# measured curve — `feelOf` — and spent it on the crossing's own progress, so equal steps of its
# other handles were not equal felt change and the composer that drives them said so in its own
# report. These rows read the curves off the built file and hold their shape and their measured
# bands. What the measurement found is worth stating: this fabric's handles were already close to
# the law, so the curves are published rather than applied and the number is now on the record.
_CURVE_HANDLES = ["nMul", "press", "speed", "wave"]
_knots = {}
for _h in _CURVE_HANDLES:
    _m = re.search(r"\n      %s: \[([^\]]+)\]" % _h, WEAVE)
    _knots[_h] = [float(x) for x in _m.group(1).replace("\n", " ").split(",")] if _m else []
_bad = [h for h, k in _knots.items()
        if len(k) != 21 or k[0] != 0 or k[-1] != 1
        or any(k[i + 1] < k[i] for i in range(len(k) - 1))]
check("PASS-WEAVE every response curve runs 0 to 1 over twenty-one marks and never turns back",
      not _bad,
      "a curve is the inverse of the picture's own running travel, so it is non-decreasing by "
      "construction and its two ends are the handle's two ends. Twenty-one marks is the count this "
      "instrument's own measured response curve carries, so the two are read the same way. Handles "
      "carrying one: " + ", ".join(sorted(_knots))
      if not _bad else "these are not a curve: " + ", ".join(_bad))

check("PASS-WEAVE no curve is applied here, and the file says why",
      "applied: false," in WEAVE and WEAVE.count("curve: { knots: CURVES.") >= 1
      and "applied: true" not in WEAVE,
      "a curve belongs on a handle whose value is a POSITION on a scale, and not one of these four "
      "is: nMul multiplies a measured band count, speed is a rate, press is a pressure in the "
      "module's own units and wave is a depth in cells read from the work. A composer places each "
      "of them from a measurement, so a curve applied here would corrupt the number that was asked "
      "for. The measured bands run 1.034 to 1.538, where the unfold's own stagger measured 12.728")

# ---- the wave came off the ribbon edge and became the work's own reading, 2026-08-17 ------------
check("PASS-WEAVE the ribbon's wave is a parameter of the work and rests at the straight edge",
      "uniform vec4 uWave;" in WEAVE
      and "float alive = wAmp * smoothstep(0.0, 0.10, uDuty)" in WEAVE
      and "wave: { min: 0, max: WAVE_MAX, def: 0" in WEAVE,
      "the depth of the wave is the whole switch and it rests at 0, so the shader's own arithmetic "
      "hands back the pre-wave cell coordinate and the pre-wave footprint for a work carrying none")

check("PASS-WEAVE not one number of the wave is a literal of the instrument any more",
      all(s not in WEAVE for s in
          ["uv.y * 1.7 - uT * 0.090", "uv.y * 3.1 + uT * 0.062", "uv.x * 1.6 + uT * 0.081",
           "uv.x * 2.9 - uT * 0.055", "0.34 * sin(aV1)", "0.34 * 1.7 * cos(aV1)"]),
      "the eleven literals 32a013a put on the edge — two depths, four spatial frequencies, four "
      "drift rates and two phase offsets — read nothing off the photograph and drew one wave on "
      "every work alike; his 19:13 word calls that the regression")

check("PASS-WEAVE every wave handle names the measurement it is read from",
      all(s in WEAVE for s in
          ["texture.type at \u00ab\u0440\u044f\u0431\u044c\u00bb as the gate",
           "1 - texture.localStraightness",
           "texture.spectralPeriodPx over the work's own frame side"]),
      "the class law of his 19:21 word: every geometric and temporal parameter names the "
      "measurement it derives from, and the composer's own handle register reads these names")

# ---- the two handles whose published shape misdescribed them, repaired 2026-08-14 ---------------
# Both rows read the manifest against the very lines it describes, so a number that moves in one
# place and stands still in the other is red rather than quietly wrong.

# THE HANDLE GAINED A LEVEL with the sweep that made every handle in the fleet declare the
# structural level it drives (charter shelf 17). The ribbon's grain is a CELL reading, and the
# pattern follows it there: every number this row was written to hold — the three named states, the
# two band directions, the one that turns and the period it turns on — is unchanged and still read
# off the very lines the manifest describes.
AXIS_ENUM = re.search(
    r'axis: \{ min: 0, max: 2, def: 2, kind: "enum", step: 1, names: AXES,\s*'
    r'banding: \["vertical", "horizontal"\], turns: 2, turnPeriodS: 27, level: "CELL" \}', WEAVE)
check("PASS-WEAVE the ribbon axis publishes three named states, their band directions, and the one that turns",
      bool(AXIS_ENUM)
      and 'var AXES = ["up and down", "side to side", "both"];' in WEAVE
      and 'if (a === "up and down") return 0;' in WEAVE
      and 'if (a === "side to side") return 1;' in WEAVE
      and "var p = (time / 27) % 1;" in WEAVE,
      "the handle carried min 0, max 2 — the shape of a continuous range — over three named states, "
      "of which only «both» answers the clock; the published names, the band direction each stands "
      "for and the 27 s turn all read off the lines above")

# The other half of the same fact belongs to whoever WRITES the number onto the handle. Until
# 2026-09-07 this row read it out of lab/build-sceneplan-v1.py, the second composer that authored
# plans at site-build time; site commit f5ca9e6 («The second composer and every crossing it stored
# are gone; a crossing is composed at the moment two works meet») deleted that file, and the row has
# been abstaining ever since on a path nobody was going to restore.
#
# THE ENCODING DID NOT GO WITH IT. It moved into the composer that ships — pass-composer.js:6584
# reads `e.axis === "vertical" ? 0 : 1` and :1435 publishes the sentence a composer author reads,
# «axis: 0 vertical, 1 horizontal» — and that is where this row now stands. It is stronger than the
# grep it replaces: the numbers are the ones the RUNNING composer actually put on the woven cue's
# axis node for constructed pairs, one whose two works both band vertically and one whose two both
# band horizontally, so a wiring that typed the sentence and encoded the other way reds here.
AXIS_ROW = ("PASS-WEAVE the axis handle's 0 and 1 are the banding measure's own vertical and "
            "horizontal, as the shipped composer writes them")
COMPOSER_SRC = COMPOSER_MODULE.read_text(encoding="utf-8")
if COMPOSED_WHY:
    skip(AXIS_ROW, "the shipped composer could not be run here: " + COMPOSED_WHY)
else:
    _upright = [c for c in COMPOSED["axis"]
                if c["bandingA"] == "vertical" and c["bandingB"] == "vertical"]
    _across = [c for c in COMPOSED["axis"]
               if c["bandingA"] == "horizontal" and c["bandingB"] == "horizontal"]
    check(AXIS_ROW,
          bool(_upright) and bool(_across)
          and all(c["value"] == 0 for c in _upright)
          and all(c["value"] == 1 for c in _across)
          and 'e.axis === "vertical" ? 0 : 1' in COMPOSER_SRC
          and '"axis: 0 vertical, 1 horizontal"' in COMPOSER_SRC,
          "the composer encodes a measured vertical family as 0 and a horizontal one as 1, which is "
          "the same pair the shader draws at uRot 0 and uRot 1. Composed over the constructed "
          "corpus: %d pair(s) whose two works both band vertically, and the composer wrote %s onto "
          "the woven cue's axis node; %d whose two both band horizontally, and it wrote %s"
          % (len(_upright), sorted({c["value"] for c in _upright}) or "nothing",
             len(_across), sorted({c["value"] for c in _across}) or "nothing"))

_pub = re.search(r"strips: \{ min: (\d+), max: (\d+), def: (\d+),", WEAVE)
# The band count the handle itself rests at, read off the built instrument rather than retyped. The
# door-refusal rows below hand it to `balanced` for the reason written there.
DOOR_STRIPS = int(_pub.group(3)) if _pub else None
_app = re.search(r"applied: \{ floor: (\d+), ceiling: (\d+), timesHandle: \"nMul\",\s*"
                 r"frameWidth: \{ full: (\d+), least: ([\d.]+) \},\s*"
                 r"drawnFloor: (\d+), basketTakes: ([\d.]+) \}", WEAVE)
_clamp = re.search(r"clamp\(st\.strips \* st\.nMul \* clamp\(st\.cssWidth / 1000, ([\d.]+), 1\), "
                   r"(\d+), (\d+)\)", WEAVE)
_shader = re.search(r"float nV = max\(([\d.]+), uNv \* \(1\.0 - ([\d.]+) \* basket\)\);", WEAVE)
check("PASS-WEAVE the band count publishes the floor the instrument applies, and every number in it names its own line",
      all([_pub, _app, _clamp, _shader])
      and (_pub.group(1), _pub.group(2)) == (_clamp.group(2), _clamp.group(3))
      and (_app.group(1), _app.group(2)) == (_clamp.group(2), _clamp.group(3))
      and _app.group(3) == "1000" and _app.group(4) == _clamp.group(1)
      and _app.group(5) == _shader.group(1).split(".")[0]
      and _app.group(6) == _shader.group(2),
      "the four gates between the handle and the shader — the declared param range, the published "
      "handle range, the frame number clamp and the shader floor — stood at 8, 8, 6 and 5, one "
      "behind another and none of them published, so a composer asking for a measured band family "
      "of three read none of the floors it would meet and got six bands whatever it asked. They "
      f"now read {_pub and _pub.group(1)}, {_app and _app.group(1)}, {_clamp and _clamp.group(2)} "
      f"and {_shader and _shader.group(1)}: the number the manifest publishes and the number the "
      "frame draws are one number, at three bands as at six")

# THE MEASUREMENT THE BALANCE IS READ AGAINST AT A DOOR, published in the manifest. His 19:13 word,
# lifted to the class at 19:21: every geometric parameter names the measurement of the work it reads.
# The balance's own reading is the share of every band the fabric leaves to the other work, on the
# drawing buffer — and the handle says so where a composer can read it.
check("PASS-WEAVE the balance handle publishes the measurement its door is read against",
      'heldWholeAtADoor: { bands: DOOR_HOLD, readOn: "the drawing buffer",' in WEAVE
      and 'reads: "balRequest"' in WEAVE
      and "var BAL_WHOLE = 0.88;" in WEAVE
      and "var DOOR_HOLD = 2;" in WEAVE
      and "var DOOR_SHOW = 0.5 / 255;" in WEAVE,
      "the handle carries `applied.heldWholeAtADoor` — what is read, on which grid, how far the "
      "hold reaches and where the request stays on the record — beside its own range, and the "
      "balance the duty's own smoothstep closes at is named once")

check("PASS-WEAVE the capture bench serves the record and the files it names, before the host",
      'shutil.copy2(tmp / "config.json"' in CAPTURE
      and 'tmp.glob("pass-inst-*.js")' in CAPTURE
      and CAPTURE.index('tmp.glob("pass-inst-*.js")') < CAPTURE.index('tmp / "pass-layer.js"'),
      "the instruments left the host on 2026-08-14 and left the single pack for a file each; a "
      "bench root carrying the host alone answers its fetch for the site's own record with a 404, "
      "and a root carrying the record without the files it names answers every instrument with one")

# THE ROW THAT STOOD HERE RETIRED 2026-08-17 (U27 stage 0), with the road it asserted. It read
# `function passScoreFor` out of engine/client/01a-pass.js and stood for one sentence: the site's
# pass record carries scores keyed by the pair, the bake passes the block through as data, and so a
# new score for a pair is a content change rather than an engine rebuild. His word of 19:21 retired
# the first clause — the collection grows to thousands of works and nothing on the product path may
# carry a table keyed by the pair — and `passScoreFor` was deleted with the two other score roads.
#
# The second clause did not retire, and it is the half this suite owns: the bake judges NOTHING in
# the block, whatever the block contains, so a road into the walk is still a content change. It
# moves into the row below, which already read the block back out of the served file and now reads
# a member the bake has never heard of back out of it too. That is the property under the sentence,
# stated once, in the one row that measures it.
#
# What proves the rest: the walk deriving its passage from the two works' own records is
# tests/test_pass_composed.py, whose first four rows read the served bundle for the composer's door
# and for the absence of all three roads that left.
# The judge resolved the two lanes' answers to this row on 2026-08-17 21:30. The closing lane
# repointed it to grep the composed road's own function names; the seam lane retired it and moved
# the half that still holds into the row below, where it is measured against a member the bake has
# never heard of. The measured road is the stronger instrument and it is kept; a grep for two
# function names adds nothing the first four rows of tests/test_pass_composed.py do not already
# read out of the served bundle.

# The delivery road's own row: what a site wrote into site.json is what the served settings file
# carries, byte for byte, with the bake judging none of it.
#
# THE BAKE ADDS TWO MEMBERS OF ITS OWN, and this row names them rather than letting them pass unread.
# The instrument record, keyed by instrument name, carrying the address each file is served at, the
# version it declares and the digest its served bytes weigh to: the bake weighed the bytes it wrote,
# so that record is the one thing in the block the site cannot author for the files the bake ships.
# And, since 2026-08-15, the capability record — the limits the client applies, read out of the
# served client itself, so a site composing scores measures them against the number the client will
# actually accept instead of against a copy of it.
# Everything else the site wrote reaches the file untouched, which is what the second half reads.
served = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
_block = served.get("pass") or {}
_added = sorted(set(_block) - set(build_site.SITE_CONFIG["pass"]))
_kept = {k: v for k, v in _block.items() if k in build_site.SITE_CONFIG["pass"]}
check("PASS-WEAVE the site's pass record reaches the served settings file untouched, whatever it "
      "carries, with the bake's own instrument and capability records beside it",
      _kept == build_site.SITE_CONFIG["pass"] and _added == ["capabilities", "instruments"]
      and all(sorted(e) == ["digest", "src", "version"] for e in _block["instruments"].values())
      # the member neither side knows, read back whole: a nested record, a float, an integer and a
      # non-ASCII string all standing where site.json put them
      and _kept.get("deliveryProbe") == build_site.SITE_CONFIG["pass"]["deliveryProbe"],
      f"config.json carries {_kept} exactly as site.json wrote it — including «deliveryProbe», a "
      f"member the bake has never heard of and the client has no register row for, which is what "
      f"makes a new score road a content change — and the bake added "
      f"{_added} — {sorted(_block.get('instruments') or {})}, each with its address, version and digest")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-WEAVE row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-WEAVE row 7  · door 0 carries no trace of the arriving work",
    "PASS-WEAVE row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-WEAVE row 7  · door 1 carries no trace of the departing work",
    "PASS-WEAVE the host's frame and the lab module's frame agree: door-0",
    "PASS-WEAVE the host's frame and the lab module's frame agree: the woven middle",
    "PASS-WEAVE the host's frame and the lab module's frame agree: door-1",
    "PASS-WEAVE row 10 · a seeded run repeats to the pixel",
    "PASS-WEAVE row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-WEAVE row 15 · the console stays clean",
    "PASS-WEAVE row 22 · the census shows granted against declared, and neither overruns",
    "PASS-WEAVE §7 · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-WEAVE §7 · a manifest naming a uniform the host cannot supply is refused, with its reason",
    "PASS-WEAVE §7 · one canvas, one context, two source textures, one pass a frame",
    "PASS-WEAVE the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-WEAVE §2.5 · an interruption at each of five instants lands inside the score's own budget",
    "PASS-WEAVE §2.5 · every handle stands on its door when the cadence ends",
    "PASS-WEAVE §2.5 · the cadence walks to the door the visit is LANDING on, from every instant",
    "PASS-WEAVE row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-WEAVE §5     · one node drives two handles of the real instrument, and moves both",
    "PASS-WEAVE §4.4b  · the strip-count breath and the press reach the PICTURE, not just the record",
    "PASS-WEAVE the door is read on the DRAWING BUFFER, and the band the door is held at is published",
    "PASS-WEAVE a door no whole band can close is refused on the real road, and the visitor still lands",
    "PASS-WEAVE what the instrument applied reaches the host's own stack row, field for field",
]

# THE WAVE'S OWN TWO ENDS, READ ON THE FRAME. The straight ribbon is the default and the wave plays
# only where the work carries one, so the acceptance has to show both ends and show that they are
# not the same frame. Every row here runs on ONE ribbon set — the ribbon axis driven to «up and
# down», where `uRot` holds at 0, the basket is nothing and `showV` is 1 at every point — so the
# frame is the column set alone and the reading is about the wave and about nothing else.
WAVE_ROWS = [
    "PASS-WEAVE straight  · a work with no measured wave draws the pre-wave frame",
    "PASS-WEAVE waved     · a work that carries a wave draws the very wave 32a013a recorded",
    "PASS-WEAVE the wave is no ornament: the straight fabric and the waved one stand apart",
]

RED_ROWS = [
    "PASS-WEAVE red-on-bug · the door reading removed: a door woven of both photographs is drawn",
    "PASS-WEAVE red-on-bug · the reporting call reverted: the host's stack row carries no reading",
    "PASS-WEAVE red-on-bug · the wave forced back to a literal: a work carrying none is drawn waved",
]

# THE THREE-BAND ACCEPTANCE. The floors were lowered so that the band family the composed passage
# stands on could be REACHED at all; before it, a handle of 3, 4, 5, 6 or 8 all drew six bands. The
# rows above hold the instrument against the lab module on the poses the carrier check already used,
# and not one of them asks for three bands, so the pose the whole change exists for went unmeasured.
# These two rows are that pose: the shipped instrument driven to it, and the drawn frame read by the
# collection's own banding measure on the worked pair's own two works — on a 1440 px frame, where
# three bands is the pair's own period of 480 px, and on the 390 px phone frame, where a handle of 6
# is what puts three bands on the glass and the peak tracks the count row for row.
#
# THE TWO ROWS THAT STOOD HERE AND HELD THE HOST'S THREE-BAND FRAME AGAINST THE LAB MODULE'S ARE
# GONE, 2026-09-07, AND THEY CANNOT BE REPAIRED. Both were pure parity — one drawn frame against the
# other at a request of three bands — and the lab module cannot be brought to that pose at all: its
# own `strips` handle floors the request at eight (lab/effects/weave.js:703, `clamp(+value, 8, 64)`)
# and its own band count floors at six (:324, `clamp(..., 6, 64)`), which are two of the very four
# floors the shipped instrument lowered to three so that a measured family of three could be reached
# — the row above this one reads all four and holds them at 3, 3, 3 and 3. So the second road never
# draws three bands, and asking whether the two roads agree there asks whether one implementation
# matches another at a pose the other refuses to take. Run standalone on 2026-09-07 they read
# exactly that: at a request of three on 1440 px both roads drew EIGHT, and at a request of six on
# 390 px the host drew four against the module's six with the two frames 53.65 of 255 apart.
#
# WHAT SURVIVES OF THEIR INTENT is the two rows below, which no longer ask a second implementation
# anything. They drive the SHIPPED instrument to the pose, read the count off its own numbers, and
# read the drawn frame with the collection's own banding measure — so what is judged is where the
# band family the passage stands on actually lands on the glass, which is the thing the lowered
# floors were lowered for. The three poses at the head of this suite and the wave's two ends still
# hold the two roads against each other, because those are poses the module can take.
BAND_ROWS = [
    "PASS-WEAVE three bands · 1440 wide: a request of three draws three, and the drawn frame's band family lands on the frame's own third",
    "PASS-WEAVE three bands · 390 wide: a request of three draws three, and the drawn frame's band family lands on the frame's own third",
]

# §2.5's landing slack. The host's own force-end is a timer at the score's `withinMs`; a browser
# fires a timer a little late and the frame that draws the door is scheduled after it, so the
# measured landing is allowed this much past the budget. It is a scheduling number, not a pacing
# one — the pacing number is `withinMs` and it belongs to the score.
#
# 100ms was sized for a lone Chrome. tests/run_all.py's own default (`--jobs 8`) is eight suites'
# worth of Chrome sharing this host's CPU, and that is the scheduling delay this slack exists to
# absorb — not a rare edge case but the runner's ordinary mode. Reproduced here 2026-09-03 by
# running this suite alongside seven others: a lone run lands at 508-581ms; the same run under that
# contention landed once at 601ms (101ms over the old 100ms slack) and a full-gate run on this
# machine the same day recorded landings to 635ms (135ms over). 200ms covers both with headroom
# without touching `withinMs`, the number the score itself paces by.
LAND_SLACK_MS = 200

WALK_ROWS = [
    "PASS-WEAVE the walk reads the pair's own score and freezes it onto the command",
    "PASS-WEAVE the score's cue names the instrument, and that instrument takes the command",
    "PASS-WEAVE the pass over a scored pair lands in exactly one dock, curtain down",
    "PASS-WEAVE a pair with no score of its own is carried by the last resort, and still lands",
]

# THE EIGHT PASS-TABLE ROWS RETIRED WITH THE ROAD THEY GUARDED (U27 stage 0, 2026-08-17). They drove
# the inline fill road — `pass.scoreTemplates` filled from `pass.scoreTables`, one row of measured
# numbers per ordered pair — which the no-pair-table law of his 19:21 word retired: a table of pairs
# is quadratic in the collection and nothing on the product path may scale with it. What replaces
# them is tests/test_pass_composed.py, where the score for a pair is DERIVED from the two works'
# own records at the instant the walk casts the pair, and the family roll they proved is now the
# die the walk rolls per crossing (§4.4f is unchanged and passBreath still holds it).

# THE READ-ONLY SOURCE MATERIAL THE PARITY ROWS STAND ON, and it no longer includes a score. The
# stored per-pair score left this list on 2026-09-07, when the score became something the shipped
# composer works out for two constructed records (see the head of this file). What is still read from
# outside the engine is the material a SECOND ROAD needs: the two photographs the doors are measured
# against, and the lab module the host's own frame is compared with.
missing = [str(p) for p in (PHOTOS + [LAB / "effects" / "weave.js"]) if not p.exists()]

# What a row is told when the score could not be composed. Node absent is the same class of
# abstention as Chrome absent — a tool this machine does not carry — and is pinned. Anything else is
# the composer failing to compose, which is a failure of the thing under test and reds.
NO_NODE = ("node is not installed, so the shipped composer cannot compose a score "
           "(pinned expected skip)")
NO_SCORE = "the shipped composer composed no score for this suite: %s" % COMPOSED_WHY


# ---------------------------------------------------------------- the lab copy, straightened
# THE WAVE THIS LANE TOOK OFF THE RIBBON EDGE, AND WHY THE LAB MODULE IS SERVED STRAIGHTENED HERE.
#
# The wave entered lab/effects/weave.js at 32a013a on 2026-08-13 and the engine's copy was born with
# it (aeb8c7c, 08-14), so the two files hold ONE regression rather than two. Eleven literals — two
# depths, four spatial frequencies, four drift rates and two phase offsets — drew a wandering ribbon
# edge on every work alike, reading nothing off the photograph, while the band count on the same
# instrument was measured from the work. His 2026-08-17 19:13 word calls that a regression and
# carries the resolution in its own sentence: a wavy cut plays only where the work itself carries
# the wave. The instrument's answer is a wave that is a PARAMETER of the work and rests at nothing.
#
# The lab file in the tlvphotos tree is read-only from here, and the identical edit is the judge's
# to land. Until it lands, the rows that hold the two roads of one frame against each other would be
# comparing a straight engine against a waved module and would red for the wrong reason. So this
# file states the edit as code, applies it to the BYTES IT SERVES, and never touches the file: the
# straightened module is what the default bench serves, and the file as it stands is what the waved
# row serves. Both directions assert their own input, so a lab file in neither state reds loudly
# rather than quietly serving something nobody described.
LAB_WEAVE = LAB / "effects" / "weave.js"

# The nine lines the wave lives on, and the three the wave changed underneath it. Every one of them
# is quoted from lab/effects/weave.js as 32a013a left it.
WAVE_LINES = [
    "    '  float aV1 = TAU * (uv.y * 1.7 - uT * 0.090);',\n",
    "    '  float aV2 = TAU * (uv.y * 3.1 + uT * 0.062 + 1.3);',\n",
    "    '  float edgeV = alive * (0.34 * sin(aV1) + 0.17 * sin(aV2));',\n",
    "    '  float dEdgeV = alive * TAU * (0.34 * 1.7 * cos(aV1) + 0.17 * 3.1 * cos(aV2));',\n",
    "    '  float aH1 = TAU * (uv.x * 1.6 + uT * 0.081);',\n",
    "    '  float aH2 = TAU * (uv.x * 2.9 - uT * 0.055 + 0.7);',\n",
    "    '  float edgeH = alive * (0.34 * sin(aH1) + 0.17 * sin(aH2));',\n",
    "    '  float dEdgeH = alive * TAU * (0.34 * 1.6 * cos(aH1) + 0.17 * 2.9 * cos(aH2));',\n",
]
# `alive` ITSELF STAYS (repointed 2026-09-08, cause found not guessed): it left WAVE_LINES because
# the lab grew a CURVE feature after 32a013a that shares `alive` as its own door gate (lab/effects/
# weave.js, the block right below the wave lines — `curveV`/`dCurveV`/`curveH`/`dCurveH` all read
# `alive`). `alive`'s declaration used to be a wave line and straighten() deleted it outright; the
# four WAVE_PAIRS below still named the pre-curve text of cV/cH/wV/wH, so `.replace()` silently
# no-op'd on all four (the lab's own lines now read `+ edgeV + curveV`, `+ (abs(dEdgeV) +
# abs(dCurveV))`, never the old two-term form) and a straightened pack kept `curveV` etc. referring
# to the `alive` declaration straighten() had just removed — the browser's own compiler read that
# as `alive`/`edgeV`/`edgeH`/`dEdgeV`/`dEdgeH` undeclared, which is the row's real, reproducing
# defect. Curve is a later, separate feature straighten()'s own docstring already promises not to
# touch, so the repair keeps `alive` declared and drops only the wave edge's own eight lines, and
# the four pairs below are read off the lab file as it stands today rather than as it stood at
# 32a013a.
WAVE_PAIRS = [
    ("    '  float cV = warpV(uv.x, 2.0, phV) * nV + edgeV + curveV;',",
     "    '  float cV = warpV(uv.x, 2.0, phV) * nV + curveV;',"),
    ("    '  float cH = warpV(uv.y, 3.0, phH) * nH + edgeH + curveH;',",
     "    '  float cH = warpV(uv.y, 3.0, phH) * nH + curveH;',"),
    ("    '  float wV = 0.5 * (nV * warpD(uv.x, 2.0, phV) / uRes.x + (abs(dEdgeV) + abs(dCurveV)) "
     "/ uRes.y);',",
     "    '  float wV = 0.5 * (nV * warpD(uv.x, 2.0, phV) / uRes.x + abs(dCurveV) / uRes.y);',"),
    ("    '  float wH = 0.5 * (nH * warpD(uv.y, 3.0, phH) / uRes.y + (abs(dEdgeH) + abs(dCurveH)) "
     "/ uRes.x);',",
     "    '  float wH = 0.5 * (nH * warpD(uv.y, 3.0, phH) / uRes.y + abs(dCurveH) / uRes.x);',"),
]


def lab_is_waved(text):
    return all(one in text for one in WAVE_LINES) and all(a in text for a, _ in WAVE_PAIRS)


def lab_is_straight(text):
    return (not any(one in text for one in WAVE_LINES)
            and all(b in text for _, b in WAVE_PAIRS))


def straighten(text):
    """The lab-side edit, applied to bytes. The nine wave lines go; the two cell coordinates and the
    two footprints return to the form they carried before 32a013a. Nothing else that commit brought
    is touched — the over-and-under alternation, the contact shadow on both sides and the per-ribbon
    content offset answered the flat-blinds complaint on their own merits and stay."""
    if lab_is_straight(text):
        return text
    for one in WAVE_LINES:
        text = text.replace(one, "", 1)
    for a, b in WAVE_PAIRS:
        text = text.replace(a, b, 1)
    return text


# THE WAVE THE MODULE ITSELF DREW, said in the instrument's own three handles. Two thirds of the
# depth in the fundamental and one third in the overtone makes 0.34 and 0.17; a period of one over
# 1.7 of the frame side makes the fundamental's 1.7 cycles and the overtone's 1.7 x 1.8235 = 3.1;
# a drift of 0.090 cycles a second makes the overtone's 0.090 x 0.6889 = 0.062 the other way. So a
# work measured to carry exactly the wave 32a013a hardcoded asks for these three numbers and the
# instrument draws that wave — which is what makes the parameter a faithful carrier of it and not a
# new effect wearing its name.
MODULE_WAVE = {"wave": 0.51, "wavePeriod": 1.0 / 1.7, "waveDrift": 0.090}


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return path


def diff(p, q):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, c))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def work_in_the_frame(src, w, h, zoom):
    """The work as the instrument seats it: cover-fit, then the centre crop the strips' travel is
    paid for with (the module's own ZOOM). The very same construction lab/carrier-check.py uses, so
    the two checks judge a door the same way."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= zoom
    sh /= zoom
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir(pack_text=None, lab_text=None):
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied and
    comments stripped), the lab module unchanged, the two photographs, and the page that stands the
    two roads of one frame side by side.

    A row proving a rule reds hands over a CHANGED instrument file and writes the site's own record
    with the digest of the bytes actually served, which is what the build does. The source file on
    disk is never touched, so nothing has to be restored and no working tree can be left changed by
    a red-on-bug proof. The road is the one the adrift and unfold suites already prove by."""
    d = Path(tempfile.mkdtemp(prefix="synth_weavebench_"))
    pack = WEAVE if pack_text is None else pack_text
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    # Each instrument travels as its own file and the host learns every address from the site's own
    # settings record, so the bench root serves that record and the files it names — the same files
    # a visitor is served, unaltered.
    for _inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, d / _inst.name)
    (d / "pass-inst-weave.js").write_text(pack, encoding="utf-8")
    record = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    record["pass"]["instruments"]["weave"]["digest"] = hashlib.sha256(
        pack.encode("utf-8")).hexdigest()
    (d / "config.json").write_text(json.dumps(record), encoding="utf-8")
    # The lab module, in the state this bench means to compare against. The default is the
    # STRAIGHTENED one, because the engine instrument's own default is the straight ribbon; a bench
    # that means to compare the waved fabric hands the file as it stands.
    lab = LAB_WEAVE.read_text(encoding="utf-8") if lab_text is None else lab_text
    (d / "weave.js").write_text(straighten(lab) if lab_text is None else lab, encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS + [w for w in PAIR_WORKS if w.exists()]:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_weave.html", d / "index.html")
    return d


def ready(br, tries=60):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def landed_read(brx, bal):
    """One whole pass at `bal`, landed through the interruption cadence, read as the host's own
    stack row for the woven voice. The landing is what makes the row readable in one piece: the
    cadence walks every handle to its nearest door and the host writes those door handles onto the
    stack row, and the last frame drawn is ON that door — so the reading the instrument published
    came from exactly the handles standing beside it."""
    jsx = lambda body: json.loads(              # noqa: E731 — one expression, read twice below
        brx.evaluate("JSON.stringify((function(){%s})())" % body))
    brx.evaluate("window.__cancel('applied row'); 0")
    for _ in range(60):
        if jsx("return window.__report().state;") == "idle":
            break
        brx.sleep(0.05)
    jsx("return window.__offer(%s, {clock: 0, progress: 0});" % json.dumps(balanced(bal)))
    brx.sleep(0.8)
    brx.evaluate("window.__cancel('applied row landing'); 0")
    for _ in range(80):
        if jsx("return window.__report().state;") == "idle":
            break
        brx.sleep(0.05)
    r = jsx("var r = window.__report();"
            "return {state: r.state, buffer: r.census.buffer, stack: r.stack};")
    rows_ = [s for s in (r["stack"] or []) if s["instrument"] == "weave"]
    r["row"] = rows_[0] if rows_ else None
    return r


def on_bench(fn, pack_text=None, lab_text=None, query=""):
    """One reading, taken on a bench of its own: a served root, a fresh browser, and the instrument
    file this call names. Held apart so a red-on-bug proof and the run it is compared against differ
    in exactly one thing — the bytes the host was handed."""
    d = bench_dir(pack_text, lab_text)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html" + query)
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


if not chrome_available():
    for r in BROWSER_ROWS + BAND_ROWS + WAVE_ROWS + RED_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif not node_available():
    for r in BROWSER_ROWS + BAND_ROWS + WAVE_ROWS + RED_ROWS:
        skip(r, NO_NODE)
elif COMPOSED_WHY:
    for r in BROWSER_ROWS + BAND_ROWS + WAVE_ROWS + RED_ROWS:
        check(r, False, NO_SCORE)
elif missing:
    for r in BROWSER_ROWS + BAND_ROWS + WAVE_ROWS + RED_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_weaveshots_"))
    BENCH = bench_dir()
    SCORE_JSON = json.dumps(scored())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    check(r, False, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            else:
                zoom = float(br.evaluate("String(window.LAB.branchSource.weave.ZOOM)"))
                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.9)

                # ---- the three poses: the host's frame beside the lab module's ------------------
                pairs = []
                for name, v in (("door-0", 0.0), ("mid", 0.5), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.9)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.2)
                    ph = png(br, SHOTS / (name + "-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.2)
                    pm = png(br, SHOTS / (name + "-module.png"))
                    pairs.append((name, ph, pm))

                shots = {n: h for n, h, _ in pairs}
                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, zoom)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, zoom)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst channel {amx}")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[i * 2 + 1], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                for i, (name, ph, pm) in enumerate(pairs):
                    m, mx = diff(ph, pm)
                    check(BROWSER_ROWS[4 + i], m <= SAME,
                          f"{name}: mean {m:.4f} of 255 (threshold {SAME}), worst channel {mx}")

                # ---- the real transaction road, and the seeded repeat ---------------------------
                # One command of the shape the bundle freezes, carrying the pair's own score. The
                # host arms both works off the walk markup, builds the programme from the manifest,
                # raises the curtain and runs its own frame loop; the run is pinned to one instant so
                # the same instant can be photographed twice.
                br.evaluate("window.__show('host'); 0")
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                br.sleep(0.3)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                second = png(br, SHOTS / "seeded-2.png")
                m, mx = diff(first, second)
                check(BROWSER_ROWS[7], took["took"] and m == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {m} worst channel {mx}")

                # ---- ten runs, and the baseline ------------------------------------------------
                base_c = rep1["census"]
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: 2.0, progress: 0.3});" % SCORE_JSON)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after = js(br, "return window.__report();")["census"]
                same = (after["textures"] == base_c["textures"] == 2
                        and after["programs"] == base_c["programs"] == 1
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"] == 1
                        and after["contexts"] == base_c["contexts"] == 1)
                check(BROWSER_ROWS[8], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[9], not errs, "; ".join(errs)[:200])

                # ---- the census against the declaration ----------------------------------------
                # THE THREE COUNTS ARE HELD EQUAL AND THE BYTES ARE HELD UNDER, and the difference
                # is not a softening. §7's law is one-sided in the host's own words at
                # pass-layer.js:2604 — «the host counts what was actually created FOR THEM and shows
                # both, so a declaration that understates its counts or its bytes reads as the lie it
                # is» — and its verdict, `over`, is exactly `granted > declared` on all four
                # (pass-layer.js:2614). The counts stand equal because this instrument makes what it
                # declares: no texture of its own, no framebuffer, one programme. The BYTES are a
                # different quantity on the two sides: the composer's estimate is the whole footprint
                # of the cue at its variant, the two source texture slots the HOST owns included,
                # while a grant counts only what the host created for the instrument — which for a
                # cue declaring no textures of its own is nothing. Holding those two equal would
                # demand that an estimate be exact rather than sufficient, which no law here says.
                res = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[10],
                      res["declared"] and res["over"] is False
                      and res["granted"]["programs"] == res["declared"]["programs"]
                      and res["granted"]["textures"] == res["declared"]["textures"]
                      and res["granted"]["framebuffers"] == res["declared"]["framebuffers"]
                      and res["granted"]["bytes"] <= res["declared"]["bytesEstimate"],
                      f"declared={res['declared']} granted={res['granted']}")

                # ---- the two manifest refusals -------------------------------------------------
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('weave')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'weave-preserve', manifest:m,
                      values:function(){return {duty:0,amp:0,nV:8,rot:0,wave:[0,1.7,0,0],depth:0};}, fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[11],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "weave-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # THE STAND-IN ANSWERS THE FRAME KEYS THE INSTRUMENT ANSWERS. The host judges a
                # uniform's source against the keys this `values` returns, so a stand-in listing
                # fewer keys than the real instrument refuses the manifest for the WRONG uniform and
                # the row stops proving what it names. `depth` joined the frame values on
                # 2026-08-18 and is added to both stand-ins here for that reason; the assertions
                # themselves are untouched and still require the reason to name `uPointer`.
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('weave')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'weave-pointer', manifest:m,
                      values:function(){return {duty:0,amp:0,nV:8,rot:0,wave:[0,1.7,0,0],depth:0};}, fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[12],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "weave-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made -----------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                c = js(br, "return window.__report();")
                cen = c["census"]
                check(BROWSER_ROWS[13],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}")

                # ---- curtain up, one pass drawn, exactly one dock -------------------------------
                # The pin comes off, so the pass runs to its own end door and the instrument settles
                # of its own accord — the whole road, from the offer to the single dock.
                # The standing transaction is ended and LET LAND before the hooks are cleared: since
                # 2026-08-14 a cancel plays the interruption cadence, so its own dock arrives a few
                # hundred milliseconds later. Clearing first would have left that dock counted
                # against the pass this row is actually about.
                br.evaluate("window.__cancel('before the whole pass'); 0")
                for _ in range(60):
                    if js(br, "return window.__report().state;") == "idle":
                        break
                    br.sleep(0.05)
                br.evaluate("window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
                took = js(br, "return window.__offer(%s, {});" % SCORE_JSON)
                br.sleep(0.5)
                mid = js(br, "return {state: window.__report().state, "
                             "curtains: window.__hooks.curtains.slice()};")
                for _ in range(60):
                    if js(br, "return window.__report().state;") == "idle":
                        break
                    br.sleep(0.1)
                end = js(br, "return {state: window.__report().state, docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                check(BROWSER_ROWS[14],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                # ---- row 9: the camera through the whole pass ----------------------------------
                # Read off the RUN THAT JUST LANDED. This score's flight is a rest at the neutral
                # pose, so the pass never leaves it — which is exactly what "rests on B" asks of a
                # score that authors no dolly. The row reads the POSE, never the picture.
                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[18],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} "
                      f"rest={cam['rest']} handoffs={cam['handoffs']} tolerances={cam['tol']}")

                # ---- §2.5: the interruption cadence, at five instants ---------------------------
                # The pass is pinned at each instant in turn, then interrupted. The host reads the
                # score's own budget, walks every handle to its nearest door on that handle's own
                # envelope, force-ends at the deadline and lands through the one dock. Everything
                # below is read off the host's own record of what it actually did.
                WITHIN = score_of()["interruption"]["withinMs"]
                lands = []
                for at in (0.1, 0.3, 0.5, 0.7, 0.9):
                    br.evaluate("window.__hooks.docks.length = 0; "
                                "window.__hooks.curtains.length = 0; 0")
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.3)
                    js(br, "window.__cancel('row-19 at %r'); return null;" % at)
                    for _ in range(60):
                        if js(br, "return window.__report().state;") == "idle":
                            break
                        br.sleep(0.05)
                    r = js(br, "var rep = window.__report(); "
                               "return {cadence: rep.cadence, state: rep.state, "
                               "docks: window.__hooks.docks.length, "
                               "curtains: window.__hooks.curtains.slice()};")
                    lands.append({"at": at, "r": r})

                inside = [L for L in lands
                          if L["r"]["cadence"] and L["r"]["cadence"]["ended"]
                          and L["r"]["cadence"]["landedInMs"] <= WITHIN + LAND_SLACK_MS
                          and L["r"]["state"] == "idle" and L["r"]["docks"] == 1
                          and L["r"]["curtains"][-1] is False]
                check(BROWSER_ROWS[15], len(inside) == 5,
                      "budget %d ms + %d ms of scheduling slack; landings "
                      % (WITHIN, LAND_SLACK_MS)
                      + ", ".join("%s→%s ms (door %s, %d dock)"
                                  % (L["at"],
                                     L["r"]["cadence"] and L["r"]["cadence"]["landedInMs"],
                                     L["r"]["cadence"] and L["r"]["cadence"]["door"],
                                     L["r"]["docks"]) for L in lands))

                # EVERY HANDLE AT A DOOR. The host writes down, per handle, what the door wanted and
                # where the handle actually stood when the cadence ended.
                measured = []
                for L in lands:
                    for h, v in ((L["r"]["cadence"] or {}).get("atDoor") or {}).items():
                        if v.get("off") is None:
                            continue
                        measured.append((v["off"], "%s at %s" % (h, L["at"])))
                # Eleven of the twelve handles carry a number at a door; `bal` is the open one this
                # score leaves to the dial, so it has no door value of its own to be measured
                # against. The number of readings is not asserted: it moved from eight handles to
                # eleven on 2026-08-17 when the ribbon's wave became three handles the work drives,
                # and a snapshot of it reds on ordinary work while proving nothing. What is asserted
                # is the DISTANCE — every reading finishes on its door — plus a floor of one reading
                # per landing, so the row can never pass on nothing.
                worst = max(measured) if measured else (255.0, "nothing was measured at all")
                check(BROWSER_ROWS[16], len(measured) >= 5 and worst[0] <= 1e-9,
                      f"{len(measured)} handle readings across five landings; the furthest any "
                      f"handle finished from its door was {worst[0]} ({worst[1]}) — the doors are "
                      f"exact, so the bar is 1e-09")

                # THE DOOR MOVED ON 2026-08-25, and this row moved with it. It read
                # ["in", "in", "in", "out", "out"] — the NEAREST door, whichever of the dial's two
                # ends the handle happened to stand closer to. That gave one question two answers:
                # interrupted early the cadence walked back to the DEPARTING work while `finish`
                # docked the visit on the ARRIVING one, so the canvas rested on A while the DOM
                # revealed B (his own complaint of that morning; tests/test_pass_seam.py measured it
                # at 241 of 255 over 99.87 per cent of the frame). Four readings in the engine
                # already named the arrival — §6's rest law, the dock's own key, the walk's own
                # notion of where a further step counts from, and the score's `failLand` — and the
                # nearest door was the one that moved. A cadence now resolves to the door the visit
                # is landing on from every instant, so every landing reads «out».
                doors = [(L["at"], (L["r"]["cadence"] or {}).get("door")) for L in lands]
                check(BROWSER_ROWS[17],
                      [d for _, d in doors] == ["out"] * 5,
                      f"the door walked to per instant: {doors} — the visit docks on the arriving "
                      f"work from every one of them, so the picture lands there too")

                # ---- §5: one node, two handles, on the real instrument -------------------------
                # The one breath drives the strip count and the press together. Read at two clocks:
                # both move, and both stand exactly where that single value puts them.
                COUPLED = json.dumps(coupled())
                seen = []
                for sec in (1.5, 13.0):
                    js(br, "return window.__offer(%s, {clock: %r, progress: 0.5});" % (COUPLED, sec))
                    br.sleep(0.4)
                    seen.append(js(br, "return window.__report().handles;"))
                    br.evaluate("window.__cancel('coupled'); 0")
                    br.sleep(0.7)
                want = []
                for sec in (1.5, 13.0):
                    b = breath_at(sec)
                    want.append({"nMul": 1 + 0.35 * b, "press": 1 + 0.30 * max(0.0, min(1.0, b))})
                moved = (abs(seen[0]["nMul"] - seen[1]["nMul"]) > 1e-6
                         and abs(seen[0]["press"] - seen[1]["press"]) > 1e-6)
                exact = all(abs(seen[i]["nMul"] - want[i]["nMul"]) <= 1e-9
                            and abs(seen[i]["press"] - want[i]["press"]) <= 1e-9 for i in (0, 1))
                check(BROWSER_ROWS[19], moved and exact,
                      f"at 1.5 s {seen[0]['nMul']:.9f}/{seen[0]['press']:.9f}, at 13 s "
                      f"{seen[1]['nMul']:.9f}/{seen[1]['press']:.9f} — wanted "
                      f"{want[0]['nMul']:.9f}/{want[0]['press']:.9f} and "
                      f"{want[1]['nMul']:.9f}/{want[1]['press']:.9f} from the one breath node")

                # ---- §4.4b: the two voices reach the picture ------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it. It
                # says nothing about whether the instrument obeyed it — a port that kept its
                # constants would still report the driver's number. So these three runs differ by
                # exactly one voice each and are photographed: a picture that did not move is a
                # handle the instrument is not actually reading.
                br.evaluate("window.__show('host'); 0")
                shot = {}
                for name, s_ in (("base", with_statics(strips=28, nMul=1.0, press=1.0)),
                                 ("breath", with_statics(strips=28, nMul=1.4, press=1.0)),
                                 ("press", with_statics(strips=28, nMul=1.0, press=1.30))):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % json.dumps(s_))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("voice-" + name + ".png"))
                    br.evaluate("window.__cancel('voice row'); 0")
                    br.sleep(0.7)
                dBreath, mxBreath = diff(shot["base"], shot["breath"])
                dPress, mxPress = diff(shot["base"], shot["press"])
                # The bar is the project's own seam threshold, 6 of 255: a difference smaller than
                # that is what the door rows call "the same picture", so a voice must move the frame
                # by more than the seam to count as having reached it.
                check(BROWSER_ROWS[20], dBreath > SEAM and dPress > SEAM,
                      f"the strip-count breath at 1.0 against 1.4 moves the frame by {dBreath:.4f} "
                      f"of 255 (worst channel {mxBreath}); the press at 1 against 1.30 moves it by "
                      f"{dPress:.4f} (worst channel {mxPress}); the seam threshold is {SEAM}")

                # ---- THE GRID THE DOOR IS READ ON --------------------------------------------
                # The door rows above read the doors the DIAL puts the fabric at, where the response
                # curve's own dead band closes the duty exactly. `bal` is an OPEN handle, so a score
                # that names a track for it lands a door wherever that track says — and there the
                # fabric leaves a share of every band to the other work. Whether that share can be
                # SEEN is a question about the grid: the shader's own anti-aliasing spreads it over
                # the buffer points nearest each band's edge, so the same balance is a whole door on
                # one buffer and a leak on the next. This row states one such balance and asks three
                # things of the instrument: that the CSS frame calls it whole, that the buffer that
                # frame is drawn on does not, and that the hold moves to the fabric's own whole band
                # with the score's request kept on the record beside it.
                def door_pose(bal, mix=0, buf=None):
                    p = {"mix": mix, "bal": bal, "nMul": 1, "press": 1, "strips": 28, "axis": 0,
                         "speed": 1, "seed": 0, "cssWidth": VW, "cssHeight": VH,
                         "t": 0, "reduced": False}
                    if buf:
                        p["bufWidth"], p["bufHeight"] = int(buf[0]), int(buf[1])
                    return p

                def values_of(p):
                    return js(br, "return window.__exPass.bench.values('weave', %s);"
                              % json.dumps(p))

                def per_door_ms(p, n=2000):
                    return js(br, "var p = %s, b = window.__exPass.bench;"
                                  "for (var i = 0; i < 400; i++) b.values('weave', p);"
                                  "var t0 = performance.now();"
                                  "for (var j = 0; j < %d; j++) b.values('weave', p);"
                                  "return {ms: (performance.now() - t0) / %d};"
                                  % (json.dumps(p), n, n))["ms"]

                BUF_W, BUF_H = VW * 2, VH * 2   # the buffer a device ratio of 2 draws this frame on
                EDGE_BAL = 0.87642              # whole on the CSS frame, a leak on that buffer
                on_css = values_of(door_pose(EDGE_BAL))
                on_buf = values_of(door_pose(EDGE_BAL, buf=(BUF_W, BUF_H)))
                on_applied = values_of(door_pose(on_buf["bal"], buf=(BUF_W, BUF_H)))
                away = values_of(door_pose(0.5, mix=0.5, buf=(BUF_W, BUF_H)))
                refused = values_of(door_pose(0.5, buf=(BUF_W, BUF_H)))
                exitdoor = values_of(door_pose(-0.80, mix=1, buf=(BUF_W, BUF_H)))
                whole_ms = per_door_ms(door_pose(0.88, buf=(BUF_W, BUF_H)))
                held_ms = per_door_ms(door_pose(EDGE_BAL, buf=(BUF_W, BUF_H)))
                check(BROWSER_ROWS[21],
                      on_css["doorWhyNo"] is None and on_css["doorHeld"] is None
                      and on_css["balBands"] == 0 and on_css["bal"] == EDGE_BAL
                      and on_css["doorGrid"] == {"w": VW, "h": VH, "drawn": False}
                      and on_buf["doorWhyNo"] is None
                      and ("%d x %d buffer" % (BUF_W, BUF_H)) in (on_buf["doorHeld"] or "")
                      and on_buf["balRequest"] == EDGE_BAL and on_buf["bal"] == 0.88
                      and on_buf["duty"] == 1.0 and on_buf["amp"] == 0
                      and on_buf["doorGrid"] == {"w": BUF_W, "h": BUF_H, "drawn": True}
                      and on_applied["doorHeld"] is None and on_applied["doorWhyNo"] is None
                      and away["doorHeld"] is None and away["doorWhyNo"] is None
                      and away["doorGrid"] is None
                      and refused["doorWhyNo"] is not None
                      and "no whole band stands within 2 bands" in refused["doorWhyNo"]
                      and "the exit door leaks" in (exitdoor["doorHeld"] or ""),
                      "on the %d x %d CSS frame a balance of %s says «%s»; on the %d x %d buffer "
                      "that frame is drawn on it says «%s» and holds the fabric at its own whole "
                      "band (%s, duty %s, travel %s), keeping the request at %s. The applied "
                      "balance read again on that buffer: «%s». Away from a door it reads nothing "
                      "at all (grid %s); at a balance of 0.5 no whole band is within reach: «%s». "
                      "One door instant costs %.4f ms whole and %.4f ms held, on this machine."
                      % (VW, VH, EDGE_BAL, on_css["doorHeld"] or "nothing", BUF_W, BUF_H,
                         on_buf["doorHeld"] or "nothing", on_buf["bal"], on_buf["duty"],
                         on_buf["amp"], on_buf["balRequest"],
                         on_applied["doorHeld"] or "nothing", away["doorGrid"],
                         refused["doorWhyNo"], whole_ms, held_ms))

                # ---- THE DOOR REFUSED ON THE REAL TRANSACTION ROAD ---------------------------
                # The row above reads the instrument's own record. This one puts real commands on
                # the real road: one score drives the open handle to a balance the fabric's own
                # whole band closes, and it draws; the next drives it to the middle, where the door
                # is a fabric of both photographs and no band closes it, and the host has to land
                # the visitor on the instrument's own reason rather than draw it.
                def road(gen):
                    return js(br, "var r = window.__report(); return {state: r.state, "
                                  "drew: r.drew, buffer: r.census.buffer, "
                                  "refused: r.events.filter(function(e){ return e.gen === %d "
                                  "&& e.why && String(e.why).indexOf('door leaks') >= 0; })"
                                  ".map(function(e){ return e.name + ': ' + e.why; })};" % gen)

                br.evaluate("window.__cancel('door road row'); 0")
                br.sleep(0.6)
                held_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(balanced(0.87, strips=DOOR_STRIPS)))["gen"]
                br.sleep(1.0)
                played = road(held_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                br.sleep(0.6)
                leak_gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                              % json.dumps(balanced(0.5, strips=DOOR_STRIPS)))["gen"]
                br.sleep(1.1)
                leaked = road(leak_gen)
                br.evaluate("window.__cancel('door road row'); 0")
                br.sleep(0.6)
                check(BROWSER_ROWS[22],
                      played["state"] == "running" and played["drew"] == 1
                      and not played["refused"]
                      and len(leaked["refused"]) == 1 and leaked["state"] == "idle"
                      and "the entry door leaks" in leaked["refused"][0]
                      and ("%s buffer" % played["buffer"].replace("x", " x ")) in leaked["refused"][0]
                      and "no whole band stands within 2 bands" in leaked["refused"][0],
                      "on the %s buffer the host drew, a balance of 0.87 at the entry door is held "
                      "and drawn (%d cue, state %s, refused %s); a balance of 0.5 is refused with "
                      "«%s», on which the host lands the transaction (state %s, %d cue drawn) and "
                      "the walk's own glide carries the visitor"
                      % (played["buffer"], played["drew"], played["state"],
                         played["refused"] or "nothing",
                         (leaked["refused"] or ["nothing refused"])[0], leaked["state"],
                         leaked["drew"]))

                # ---- WHAT THE INSTRUMENT APPLIED, ON THE HOST'S OWN RECORD -------------------
                # The two rows above read the instrument's own numbers through the bench and the
                # host's refusal through the event log. This one reads the channel that carries the
                # instrument's reading BACK to the host: the frame state's `reportApplied`, called
                # at every door instant, whose record the host stores untouched on the voice's stack
                # row (his architecture decision of 2026-08-17 18:00 — the run-time reading on the
                # actual buffer is the truth of a passage).
                #
                # THE RUN IS TAKEN TO ITS LANDING, because that is the instant both halves of the
                # row are readable at once: the cadence walks every handle to its nearest door and
                # the host writes those door handles onto the stack row, and the last frame drawn is
                # ON that door, so the reading the instrument published came from exactly the
                # handles standing beside it. The instrument's numbers are then recomputed from
                # those same handles, on the same buffer, through the bench's own `values` — the
                # pure function the drawing frame calls — and the published reading must be that
                # recomputation, field for field.
                landed = landed_read(br, 0.87)
                bw, bh = (int(x) for x in landed["buffer"].split("x"))
                a = (landed["row"] or {}).get("applied")
                h = (landed["row"] or {}).get("handles")
                own = None
                if a and h:
                    own = values_of({"bal": h["bal"], "mix": h["mix"], "nMul": h["nMul"],
                                     "press": h["press"], "strips": h["strips"], "axis": h["axis"],
                                     "speed": h["speed"], "seed": h["seed"],
                                     "cssWidth": VW, "cssHeight": VH, "t": h["clock"],
                                     "reduced": False, "bufWidth": bw, "bufHeight": bh})
                check(BROWSER_ROWS[23],
                      bool(a) and bool(own)
                      and a["door"] in ("in", "out") and a["buffer"] == [bw, bh]
                      and a["reads"] == "bal"
                      and a["request"] == own["balRequest"] and a["applied"] == own["bal"]
                      and a["moved"] == own["balBands"] and a["held"] == own["doorHeld"]
                      and a["whyNo"] == own["doorWhyNo"] and a["unit"] == "bands",
                      "the reading the instrument published at its %s door on the %s buffer: %s. "
                      "Recomputed from the very handles the host resolved for that frame (%s), the "
                      "instrument's own `values` answers balRequest %s, bal %s, balBands %s, "
                      "doorHeld %s, doorWhyNo %s — the published record is that recomputation, "
                      "field for field."
                      % ((a or {}).get("door"), landed["buffer"],
                         json.dumps(a, ensure_ascii=False),
                         json.dumps(h, ensure_ascii=False)[:200],
                         (own or {}).get("balRequest"), (own or {}).get("bal"),
                         (own or {}).get("balBands"), (own or {}).get("doorHeld"),
                         (own or {}).get("doorWhyNo")))

        # ---- the three-band acceptance ------------------------------------------------------
        # THE POSE THE FLOORS WERE LOWERED FOR. Each frame gets its own browser, because the count
        # the instrument draws is scaled by the frame's own width and a phone and a wide frame are
        # two different questions: on 1440 px a handle of 3 draws three bands and 1440 / 3 is the
        # pair's own period of 480 px; on 390 px the width term rests on its floor of 0.5, so a
        # handle of 6 is what puts three bands on the glass and the period is 130 px.
        #
        # THE POSE IS PINNED THE WAY lab/weave-bands-rig.html PINS IT — the ribbon axis standing up
        # and down (the axis the pair's own band family was measured on, so the turn never enters),
        # the dial at the middle where the weave is widest, and the clock held at the second where
        # the strip-count breath, 1 + 0.35·sin(t·0.021·TAU + 1.1), crosses 1 exactly. Held there, the
        # breath eases onto 1 and the drawn count is the handle times the width term, with nothing
        # drifting under the shot. The dwell is the ease's own time constant of 0.5 s many times
        # over, so the count is settled to a thousandth before anything is read.
        #
        # THE BAND COUNT IS ASKED OF THE SHIPPED INSTRUMENT DIRECTLY, and that is the change of
        # 2026-09-07. The count used to be requested through the lab module's own `strips` handle and
        # the pose the module settled on was then handed to the host. That road cannot reach this
        # pose: the module clamps the request at eight (lab/effects/weave.js:703) and floors its own
        # count at six (:324) — the two floors this instrument lowered to three for exactly this
        # family — so a request of three arrived at the host as eight. The named handle is now
        # written onto the module's own settled pose through `__drawWith`, which is the bench's own
        # door for holding every other number of a pose still and walking one, and the count is read
        # off the instrument's own numbers for that pose.
        FLAT_CLOCK = (math.pi - 1.1) / (2 * math.pi * 0.021)
        BAND_TOL = 0.06          # lab/weave-bands-measure.py's own bar for «the peak IS the strips»
        pair_missing = [str(w) for w in PAIR_WORKS if not w.exists()] + \
                       ([] if CUT_LINES.exists() else [str(CUT_LINES)])
        if pair_missing:
            for r_ in BAND_ROWS:
                skip(r_, "the worked pair's own material is read-only source and is absent here: "
                         + pair_missing[0])
        else:
            import importlib.util
            _spec = importlib.util.spec_from_file_location("cut_lines", str(CUT_LINES))
            cut_lines = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(cut_lines)

            def band_of(path):
                """The drawn frame read by the collection's own measure, on the road the two
                photographs' own numbers travelled: prep_arrays resamples the long side to 512 and
                takes Rec.709 luma, measure_banding reads the column and row profiles, and the
                period comes back rescaled into the frame's own pixels."""
                gray, _rgb, to_orig, ow, oh = cut_lines.prep_arrays(str(path))
                b = cut_lines.measure_banding(gray)
                return {"axis": b["axis"],
                        "period": b["period_px_working"] * to_orig,
                        "score": b["score"],
                        "vertical_period": b["vertical"]["period_px"] * to_orig,
                        "vertical_score": b["vertical"]["score"],
                        "size": (ow, oh)}

            works = "?a=photos/%s&b=photos/%s" % (PAIR_WORKS[0].name, PAIR_WORKS[1].name)
            for i, (fw, fh, handle) in enumerate(((1440, 900, 3), (VW, VH, 6))):
                row_ = BAND_ROWS[i]
                with Browser(width=fw, height=fh) as bb:
                    bb.navigate(base + "/index.html" + works)
                    if not ready(bb):
                        check(row_, False, "the bench never came up: "
                              + bb.evaluate("JSON.stringify(window.__errs||[])"))
                        continue
                    bb.evaluate("window.__param('axis', 'up and down'); 0")
                    bb.evaluate("window.__mix(0.5); 0")
                    bb.evaluate("window.__clock(%.9f); 0" % FLAT_CLOCK)
                    bb.sleep(5.0)
                    pose = js(bb, "return window.__drawWith({strips: %d});" % handle)
                    vals = js(bb, "return window.__values(%s);" % json.dumps(pose))
                    bb.sleep(0.2)
                    bb.evaluate("window.__show('host'); 0")
                    bb.sleep(0.3)
                    ph = png(bb, SHOTS / ("bands3-%d-host.png" % fw))

                nv_host = vals["host"]["nV"]
                drawn = fw / nv_host if nv_host else 0.0
                b = band_of(ph)
                # The peak is read on the VERTICAL family, which is the family the pair was measured
                # on and the family the axis handle asks for — the strongest reading of any axis is
                # reported beside it rather than asserted, because at a wide frame in a woven pose
                # the row set can be the louder one and that is a property of the picture, not of
                # the count.
                check(row_,
                      abs(nv_host - 3.0) < 0.005
                      and abs(b["vertical_period"] - drawn) <= BAND_TOL * drawn,
                      "a handle of %d on a %d×%d frame draws %.2f bands by the instrument's own "
                      "numbers. The drawn period is %.1f px and the collection's own banding "
                      "measure reads the vertical family of the drawn frame at %.1f px, strength "
                      "%.4f (bar: within %d%% of the drawn period). Strongest family of either "
                      "axis: %s at %.1f px, strength %.4f. WHERE the peak lands is what this row "
                      "judges; HOW STRONG the family reads is reported beside it and moves with the "
                      "second the pose is held at — the module's own sweep at the pair's seed read "
                      "0.4149 on the wide frame and 0.3735 on the phone at another second, and the "
                      "floor was lowered to buy reachability, never a strength"
                      % (handle, fw, fh, nv_host, drawn, b["vertical_period"],
                         b["vertical_score"], int(BAND_TOL * 100), b["axis"], b["period"],
                         b["score"]))

    # ============================================================================================
    # THE WAVE'S TWO ENDS, EACH AGAINST THE LAB MODULE IN THE MATCHING STATE.
    #
    # The straight end is the one this lane exists for. A work with no measured wave hands the
    # instrument nothing on all three wave handles, and the frame it then draws must be the frame
    # this fabric drew BEFORE 32a013a — not a near neighbour of it. The reference is the lab module
    # with the identical edit applied to the bytes served: the nine wave lines gone and the two cell
    # coordinates and two footprints back to the form cfbb62a left them, with everything else that
    # commit brought — the over-and-under alternation, the contact shadow on both sides, the
    # per-ribbon content offset — standing exactly as it is.
    #
    # The waved end says the parameter is a faithful carrier of the wave and not a new effect
    # wearing its name. A work measured to carry exactly the ripple 32a013a hardcoded asks for a
    # depth of 0.51 cells, a period of one over 1.7 of the frame side and a drift of 0.090 cycles a
    # second; the instrument then draws that wave, and the module as it stands is what it is held
    # against. Both rows run on the column set alone, where the wave is the only thing that differs.
    def settled(br, tries=80):
        """The module eases its own balance, its strip-count breath and its press toward whatever
        the page just asked for, and it keeps easing after a frame is drawn. The host is handed the
        pose the module reports at ONE instant, so a pose still on the move makes the two roads two
        different frames — the breath alone moves this fabric by forty-eight of 255 across its own
        range. So the page waits until the module's own numbers stop moving, and says how long it
        waited rather than trusting a sleep."""
        last, held = None, 0
        for i in range(tries):
            now = js(br, "var p = window.__pose(); "
                         "return [p.bal, p.nMul, p.press, p.t];")
            if last is not None and all(abs(a - b) < 1e-6 for a, b in zip(now, last)):
                held += 1
                if held >= 3:
                    return i
            else:
                held = 0
            last = now
            br.sleep(0.1)
        return -1

    def wave_pair(tag):
        def one(br):
            br.evaluate("window.__param('axis', 'up and down'); 0")
            br.evaluate("window.__clock(%r); 0" % CLOCK)
            br.evaluate("window.__mix(0.5); 0")
            br.sleep(0.4)
            waited = settled(br)
            br.evaluate("window.__hostDraw(); 0")
            br.sleep(0.15)
            br.evaluate("window.__show('host'); 0")
            br.sleep(0.3)
            ph = str(png(br, SHOTS / (tag + "-host.png")))
            br.evaluate("window.__show('module'); 0")
            br.sleep(0.3)
            pm = str(png(br, SHOTS / (tag + "-module.png")))
            return {"host": ph, "module": pm, "waited": waited,
                    "pose": js(br, "return window.__pose();"),
                    "errs": json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))}
        return one

    LAB_SRC = LAB_WEAVE.read_text(encoding="utf-8")
    WAVE_QUERY = ("?wave=%.6f&wavePeriod=%.10f&waveDrift=%.6f"
                  % (MODULE_WAVE["wave"], MODULE_WAVE["wavePeriod"], MODULE_WAVE["waveDrift"]))

    straight = on_bench(wave_pair("wave-off"))
    waved = on_bench(wave_pair("wave-on"), lab_text=LAB_SRC, query=WAVE_QUERY)

    if straight and waved:
        sm, sx = diff(straight["host"], straight["module"])
        check(WAVE_ROWS[0],
              sm <= SAME and not straight["errs"] and straight["waited"] >= 0
              and (lab_is_waved(LAB_SRC) or lab_is_straight(LAB_SRC)),
              "the three wave handles left unnamed, which is what a work carrying no measured "
              "ripple hands the instrument: mean %.4f of 255 against the straightened lab module "
              "(threshold %.1f), worst channel %d. The lab file as it stands is %s, and the edit "
              "this row applies to the bytes it serves is the one the report hands the judge for "
              "the tlvphotos tree" %
              (sm, SAME, sx, "waved" if lab_is_waved(LAB_SRC) else
               ("already straightened" if lab_is_straight(LAB_SRC) else
                "in NEITHER of the two states this file describes")))

        wm, wx = diff(waved["host"], waved["module"])
        check(WAVE_ROWS[1], wm <= SAME and not waved["errs"] and waved["waited"] >= 0,
              "a depth of %.2f cells, a period of %.4f of the frame side and a drift of %.3f "
              "cycles a second: mean %.4f of 255 against the lab module as it stands (threshold "
              "%.1f), worst channel %d — the parameter draws the recorded wave itself"
              % (MODULE_WAVE["wave"], MODULE_WAVE["wavePeriod"], MODULE_WAVE["waveDrift"],
                 wm, SAME, wx))

        am, ax = diff(straight["host"], waved["host"])
        check(WAVE_ROWS[2], am > SEAM,
              "the same pose drawn twice, once with the wave handles unnamed and once at the "
              "work's own ripple: mean %.4f of 255 (must exceed the project's seam of %.1f), "
              "worst channel %d — a wave that made no difference to the frame would prove nothing"
              % (am, SEAM, ax))
    else:
        for r in WAVE_ROWS:
            check(r, False, "the wave bench never came up")

    # ============================================================================================
    # THE RED-ON-BUG PROOF. The lane's own rule reverted in the artifact the browser actually loads:
    # the door test in `doorReadOf` is taken out, so no instant is ever a door and the reading is
    # never taken — this instrument exactly as it stood before it read its doors at runtime,
    # declaring both doors whole in its manifest and never checking the frame it drew. The pack
    # served is changed and the host is re-stamped with the digest of the bytes it is handed, which
    # is what the build does; the file on disk is never touched, so no working tree can be left
    # changed by a proof.
    #
    # TWO NUMBERS MOVE, and the second is the one that matters. What the HOST is told: with the
    # reading standing a door at a driven balance of 0.5 is refused and the transaction lands, and
    # with it removed the same command draws. And what the VISITOR sees: at that balance the fabric
    # is half one photograph and half the other, so the drawn door stands far outside the project's
    # own 6-of-255 seam from the departing work's own file — which is what a door that is not read
    # actually costs.
    def red_one(br):
        gen = js(br, "return window.__offer(%s, {clock: 0, progress: 0});"
                 % json.dumps(balanced(0.5, strips=DOOR_STRIPS)))["gen"]
        br.sleep(1.1)
        r = js(br, "var r = window.__report(); return {state: r.state, drew: r.drew, "
                   "buffer: r.census.buffer, refused: r.events.filter(function(e){ "
                   "return e.gen === %d && e.why "
                   "&& String(e.why).indexOf('door leaks') >= 0; }).length};" % gen)
        br.evaluate("window.__show('host'); 0")
        br.sleep(0.3)
        shot = png(br, SHOTS / ("red-door-%s.png" % ("bug" if r["refused"] == 0 else "held")))
        w_ = int(br.evaluate("String(document.querySelector('canvas').width)"))
        h_ = int(br.evaluate("String(document.querySelector('canvas').height)"))
        zoom_ = float(br.evaluate("String(window.LAB.branchSource.weave.ZOOM)"))
        r["fromOwnFile"] = apart(shot, work_in_the_frame(BENCH / "photos" / PHOTOS[0].name,
                                                        w_, h_, zoom_))[0]
        br.evaluate("window.__cancel('red one'); 0")
        return r

    base_read = on_bench(red_one)
    bug = WEAVE.replace("var want = st.mix === 0 ? 1 : (st.mix === 1 ? 0 : -1);",
                        "var want = -1;", 1)
    bug_read = on_bench(red_one, pack_text=bug)
    # A READING MAY BE ABSENT — `on_bench` returns None outright when its own bench never came up
    # (`ready(br)` timed out) — and the row's job is to say so in its own voice rather than format a
    # number it does not have. `_f4` reads one field of a reading that may itself be None, in which
    # case the field is absent too; both are printed as "no reading" rather than crashing the whole
    # suite the way `bug_read and bug_read['fromOwnFile']` did, which is None exactly when the field
    # is None AND when `bug_read` itself is — the same word standing for two different absences.
    def _f4(read, field):
        v = (read or {}).get(field)
        return "%.4f" % v if isinstance(v, (int, float)) else "no reading"
    check(RED_ROWS[0],
          bug != WEAVE and base_read and bug_read
          and base_read["refused"] == 1 and base_read["state"] == "idle"
          and bug_read["refused"] == 0 and bug_read["state"] == "running"
          and bug_read["drew"] == 1 and bug_read["fromOwnFile"] > SEAM,
          f"with a balance of 0.5 driven onto the entry door on the "
          f"{(base_read or {}).get('buffer', 'no reading')} buffer, the reading tells the host so "
          f"({(base_read or {}).get('refused', 'no reading')} refusal, state "
          f"{(base_read or {}).get('state', 'no reading')}) and the walk's own glide carries the "
          f"visitor. With the door test taken out — no instant is a door, the instrument as it "
          f"stood before it read its doors at runtime — the same command draws that door instead "
          f"({(bug_read or {}).get('refused', 'no reading')} refusals, state "
          f"{(bug_read or {}).get('state', 'no reading')}, "
          f"{(bug_read or {}).get('drew', 'no reading')} cue drawn), and the frame the visitor gets "
          f"stands {_f4(bug_read, 'fromOwnFile')} of 255 from the departing work's own file against "
          f"the project's seam of {SEAM}: a door woven of both photographs"
          + ("" if base_read and bug_read else " — the bench never came up for "
             + (", ".join(n for n, r in (("the standing", base_read), ("the bug", bug_read))
                          if r is None)) + " read"))

    # THE SECOND RED-ON-BUG PROOF: the reporting call reverted. `reportApplied` is the channel the
    # instrument's own reading travels back to the host on; with it taken out of the served file the
    # instrument still reads its door, still holds it and still refuses when it must — nothing the
    # visitor sees moves — and the host's own stack row goes empty, which is exactly the state the
    # composed road printed as a gap before this lane. One thing differs between the two runs: the
    # bytes the host was handed. The file on disk is never touched.
    def applied_one(brx):
        r = landed_read(brx, 0.87)
        return {"applied": (r["row"] or {}).get("applied"),
                "handles": bool((r["row"] or {}).get("handles")),
                "buffer": r["buffer"], "state": r["state"]}

    base_say = on_bench(applied_one)
    mute = WEAVE.replace("if (st.reportApplied) {", "if (false) {", 1)
    mute_say = on_bench(applied_one, pack_text=mute)
    # SAME ABSENCE THE FIRST PROOF ABOVE GUARDS FOR: `on_bench` returns None outright when its own
    # bench never comes up, and the message below is built whether or not the row passed — so it
    # reads each reading through `.get()` on a dict-or-empty-dict rather than subscripting a
    # possible None, and says "no reading" for a field it does not have instead of crashing on it.
    check(RED_ROWS[1],
          mute != WEAVE and base_say and mute_say
          and isinstance(base_say["applied"], dict)
          and base_say["applied"].get("reads") == "bal"
          and mute_say["applied"] is None
          and mute_say["handles"] is True and base_say["handles"] is True,
          f"with the call in place the host's stack row for the woven voice carries "
          f"{json.dumps((base_say or {}).get('applied'), ensure_ascii=False)} on the "
          f"{(base_say or {}).get('buffer', 'no reading')} buffer; with the call reverted in a "
          f"copy of the served file the same landing on the "
          f"{(mute_say or {}).get('buffer', 'no reading')} buffer carries "
          f"{json.dumps((mute_say or {}).get('applied'))}, while the handles the HOST resolved "
          f"stand on both rows ({(base_say or {}).get('handles', 'no reading')} and "
          f"{(mute_say or {}).get('handles', 'no reading')}) — the reading is the instrument's own "
          f"to publish, and nothing else on the row moves when it stops"
          + ("" if base_say and mute_say else " — the bench never came up for "
             + (", ".join(n for n, r in (("the standing", base_say), ("the mute", mute_say))
                          if r is None)) + " read"))

    # THE THIRD RED-ON-BUG PROOF: the wave forced back to a literal. The depth handle is the whole
    # switch, so the regression is restored in one line — the served instrument stops reading the
    # handle and answers the module's own 0.51 cells whatever the work said. Nothing else moves; the
    # source file on disk is never touched. With it, the frame a work carrying NO measured ripple
    # gets is a waved fabric, which is exactly the state his 19:13 word called a regression, and the
    # straight row above goes red by the number it already measures.
    lit = WEAVE.replace('var amp = typeof st.wave === "number" ? clamp(st.wave, 0, WAVE_MAX) : 0;',
                        "var amp = WAVE_MAX;", 1)
    lit_read = on_bench(wave_pair("wave-red"), pack_text=lit)
    if straight and lit_read:
        base_m, _ = diff(straight["host"], straight["module"])
        lit_m, lit_x = diff(lit_read["host"], lit_read["module"])
        check(RED_ROWS[2],
              lit != WEAVE and base_m <= SAME and lit_m > SEAM,
              "with the handle read, a work carrying no measured ripple draws the pre-wave frame "
              "(mean %.4f of 255 from the straightened module, threshold %.1f). With the depth "
              "forced back to the literal 32a013a hardcoded, the same work draws a waved fabric "
              "and stands %.4f of 255 from that same module (worst channel %d) — the regression, "
              "restored in one line and caught by the row that guards it"
              % (base_m, SAME, lit_m, lit_x))
    else:
        check(RED_ROWS[2], False, "the wave bench never came up")

    shutil.rmtree(BENCH, ignore_errors=True)
    shutil.rmtree(SHOTS, ignore_errors=True)

# ---------------------------------------------------------------- the walk's own road
# The score arriving at a real visitor, on the baked site: declare freezes it onto the command, and
# the instrument the cue names is the one that takes the command.
if not chrome_available():
    for r in WALK_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif not node_available():
    for r in WALK_ROWS:
        skip(r, NO_NODE)
elif COMPOSED_WHY:
    for r in WALK_ROWS:
        check(r, False, NO_SCORE)
elif missing:
    for r in WALK_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    def enter(br, base):
        # A returning visitor is put back where they were, so the door is not always standing; the
        # second entry of this row is exactly such a return.
        if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
            br.click(".exd-window", settle=1.4)
        for _ in range(25):
            if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                           "&& !document.documentElement.classList.contains('ex-face'))") == "true":
                break
            br.sleep(0.2)
        br.sleep(0.4)
        br.key("ArrowDown")           # the one step that makes the client fetch pass-layer.js
        for _ in range(30):
            if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
                return frame_gone(br)
            br.sleep(0.2)
        return False

    def frame_gone(br, tries=25):
        """Let the animation frame the walk's own step was declared in END before this file
        declares anything of its own.

        PASS-API §1.1 gives `declare` a same-frame lock: two declares inside one animation frame
        make the second a refusal («second declare in one frame»), and the lock is released on the
        `requestAnimationFrame` the first declare schedules. The step above IS a declare, and the
        poll it is followed by can return on its very first read — the host registers the instant
        pass-layer.js executes, which on a return visit is served from the browser's own cache — so
        the rows below could put their programmatic declare into that same frame and be refused for
        racing the walk rather than for anything they measure. Waiting for a frame to pass is the
        exact fact the lock is keyed on, so nothing here is a guessed delay."""
        br.evaluate("window.__frameGone = false;"
                    "requestAnimationFrame(function () { window.__frameGone = true; }); 0")
        for _ in range(tries):
            if br.evaluate("String(!!window.__frameGone)") == "true":
                return True
            br.sleep(0.1)
        return False

    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base)
            # The pair the visitor is ACTUALLY walking over, read from the walk itself: the order is
            # the visitor's own and no test may pin it.
            WORKS = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                           ".map(function(e){return e.dataset.id;}).slice(0,2);")
            PAIR_KEY = "__".join(WORKS)

            # THE SCORE ARRIVES ON THE DECLARE (PASS-API §1.1). Until U27 stage 0 it arrived in the
            # settings record under `pass.scores`, keyed by ordered pair — a road the no-pair-table
            # law retired with the delivery pack, because a score per pair in the settings file is
            # quadratic in the collection. What a walk derives for a real pair now comes out of the
            # composer, and tests/test_pass_composed.py proves that road; what these rows need is one
            # weave score whose numbers they read back off the picture, so the score is handed to the
            # declare, which is the road §1.1 has always named for a programmatic caller. The score
            # itself is composed — by that same composer, over two constructed records — and only its
            # two work slots are named for the pair the visitor is standing in front of.
            THE_SCORE = scored(WORKS[0], WORKS[1])
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base) and armed
            shown = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                           ".map(function(e){return e.dataset.id;});")

            walkable = armed and WORKS[0] in shown and WORKS[1] in shown
            if walkable:
                br.evaluate("window.__weaveScore = " + json.dumps(THE_SCORE) + "; 0")
            for r_ in ([] if walkable else WALK_ROWS):
                skip(r_, f"the walk never registered a host, or re-hung without the pair: "
                         f"armed={armed} pair={WORKS} shown={shown[:4]}")

            if walkable:
                r = js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var B = document.querySelector('.exh-frame[data-id="%s"]');
                  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                             kind:'step', cause:'weave-road', velocity:0,
                                                             score: window.__weaveScore});
                  window.__wcmd = cmd;
                  return {got: !!cmd, hasScore: !!(cmd && cmd.score),
                          schema: cmd && cmd.score ? cmd.score.schema : null,
                          cue: cmd && cmd.score && cmd.score.cues ? cmd.score.cues[0].instrument.id : null,
                          duration: cmd && cmd.score ? cmd.score.duration : null};
                """ % (WORKS[0], WORKS[1]))
                # The duration is the composed score's own, read off the score this row handed over
                # rather than retyped: what is being proved is that the declare freezes the score
                # onto the command whole, and a number copied into this file would only prove that
                # two copies agree.
                check(WALK_ROWS[0],
                      r["got"] and r["hasScore"] and r["schema"] == 2 and r["cue"] == "weave"
                      and r["duration"] == THE_SCORE["duration"],
                      f"command={r}; the composed score's own duration is "
                      f"{THE_SCORE['duration']} ms")
                br.sleep(0.15)

                r = js(br, """
                  var marks = {docks:0, curtains:[]};
                  var took = window.__exPass.layer().offer(window.__wcmd, {
                    dock: function(){ marks.docks++; },
                    glide: function(){ marks.glide = true; },
                    curtain: function(on){ marks.curtains.push(!!on); },
                    mark: function(){}});
                  window.__wmarks = marks;
                  return {took: took};
                """)
                br.sleep(0.6)
                after = js(br, """
                  var rep = window.__exPass.host.report();
                  return {took: true, instrument: rep.instrument, state: rep.state,
                          canvases: document.querySelectorAll('canvas').length,
                          marks: window.__wmarks,
                          events: rep.events.map(function(e){return e.name;}).slice(-8)};
                """)
                check(WALK_ROWS[1],
                      r["took"] is True and after["canvases"] >= 1
                      and after["marks"]["curtains"][:1] == [True],
                      f"took={r['took']} after={after}")
                for _ in range(60):
                    if js(br, "return window.__exPass.host.report().state;") == "idle":
                        break
                    br.sleep(0.1)
                landed = js(br, """
                  var rep = window.__exPass.host.report();
                  return {docks: window.__wmarks.docks, curtains: window.__wmarks.curtains,
                          events: rep.events.map(function(e){return e.name;}).slice(-8),
                          state: rep.state};
                """)
                check(WALK_ROWS[2],
                      landed["docks"] == 1 and landed["state"] == "idle"
                      and landed["curtains"][-1] is False and "docked" in landed["events"],
                      f"landed={landed}")

                # THE SAME TWO WORKS WALKED THE OTHER WAY, and this declare hands over no score.
                # Nothing is frozen onto the command and no cue names an instrument, so the funnel's
                # own first give-up exit is reached — and behind that exit stands the LAST RESORT
                # (2026-08-24), which casts on the two pictures the DOM already holds. The visitor is
                # carried by a real crossing rather than handed back to the walk's glide: the offer
                # is taken, the curtain rises and falls, and the passage lands in exactly one dock.
                # Until the last resort existed this row read the other outcome, the plain glide,
                # which is the road the host now takes only where even that cast fails.
                # A→B and B→A are two distinct passages of one edge, which is the direction the
                # charter's model asks for and what the composed road derives per direction.
                r = js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var B = document.querySelector('.exh-frame[data-id="%s"]');
                  var cmd = window.__exPass.adapter.declare({fromEl:B, toEl:A, dir:-1, span:100,
                                                             kind:'step', cause:'no-score', velocity:0});
                  window.__noscore = {glide:false, curtains:[], docks:0, marks:[]};
                  var seen = window.__noscore;
                  var took = window.__exPass.layer().offer(cmd, {dock:function(){ seen.docks++; },
                    glide:function(){ seen.glide = true; },
                    curtain:function(on){ seen.curtains.push(!!on); },
                    mark:function(n){ seen.marks.push(n); }});
                  return {score: cmd ? cmd.score : 'no command', took: took === true};
                """ % (WORKS[0], WORKS[1]))
                for _ in range(80):
                    if js(br, "return window.__exPass.host.report().state;") == "idle":
                        break
                    br.sleep(0.1)
                after = js(br, "var rep = window.__exPass.host.report();"
                               "return {seen: window.__noscore, state: rep.state,"
                               " events: rep.events.map(function(e){return e.name;}).slice(-8)};")
                seen = after["seen"]
                check(WALK_ROWS[3],
                      r["score"] is None and r["took"] is True
                      and seen["docks"] == 1 and seen["glide"] is False
                      and seen["curtains"] == [True, False]
                      and after["state"] == "idle" and "docked" in after["events"],
                      f"the declare froze no score onto the command (score={r['score']}) and the "
                      f"host took it anyway (took={r['took']}): curtains={seen['curtains']} "
                      f"docks={seen['docks']} glide={seen['glide']} marks={seen['marks']}, "
                      f"state={after['state']}, events={after['events']} — the last resort cast on "
                      f"the two pictures the DOM already holds, so the visitor is carried by a real "
                      f"crossing and the walk's own glide is not spent")

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
