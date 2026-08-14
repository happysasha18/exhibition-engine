#!/usr/bin/env python3
"""PASS-API-V1 — the driver graph (§5) and the camera (§6), read as data.
Run: python3 tests/test_pass_drivers.py

Root: his word 2026-08-13 23:03 — the woven slice carried across. The first half made the picture
correct; this file is the evidence for the second half, the travel and the camera.

WHAT IS JUDGED HERE, AND WHY IT NEEDS NO BROWSER.

  The driver graph is data evaluated by a function, and the camera is a POSE — one record the host
  computes and then applies. §6 states the law plainly: the check reads THE POSE rather than the
  picture, so it stays honest when the picture changes. Both therefore stand up under plain Node
  against the BUILT artifact — the same pass-layer.js a visitor downloads, namespace applied and
  comments stripped — with the host's own bench handing back exactly the evaluator a running frame
  calls and exactly the camera evaluation a running frame applies. Nothing here is stubbed but the
  window the file expects to find itself in.

  What genuinely needs pixels lives next door: the interruption's five landings, the seeded repeat,
  and the camera read off a real running transaction are rows in tests/test_pass_weave.py.

  Node absent is a pinned SKIP that names it — never a silent pass.
"""
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402

SITE_URL = "https://synth.example.com"
NODE = shutil.which("node")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_passdrv_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
BUILT = (TMP / "pass-layer.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

# §5's last sentence, against the artifact a visitor actually downloads rather than against source.
check("PASS-DRV §5 · the built file carries no eval and no constructed function",
      "eval(" not in BUILT and "new Function" not in BUILT and "setTimeout(\"" not in BUILT,
      "the driver graph is DATA — a score names no expression, no function and no executable string")

check("PASS-DRV §5 · the operators of the contract are all named in the evaluator",
      all(('case "%s"' % op) in BUILT for op in
          ["static", "curve", "spline", "map", "add", "multiply", "mix", "clamp",
           "hold", "segment", "ramp", "slew", "oscillate"]),
      "curve, monotone spline, map, add, multiply, mix, clamp, hold/segment, ramp/slew, oscillate")

check("PASS-DRV §5 · the sources of the contract are all named in the evaluator",
      all(('case "%s"' % s) in BUILT for s in
          ["progress", "cueProgress", "time", "velocity", "capability", "noise", "pointer"]),
      "progress, cueProgress, time, velocity, capability, noise(seed, stream), pointer")

check("PASS-DRV §5 · the four named curves are the lab engine's own, carried across unchanged",
      "smooth: function (u) { return u * u * (3 - 2 * u); }" in BUILT
      and "out: function (u) { return 1 - (1 - u) * (1 - u); }" in BUILT,
      "lab/crossing-engine.js SHAPES — one score must read the same on both roads")

# ---------------------------------------------------------------- the rows Node runs

ROWS = [
    "PASS-DRV §5 · every source answers its stated value at stated inputs",
    "PASS-DRV §5 · every operator answers its stated value at stated inputs",
    "PASS-DRV §5 · pointer is declared, falls back to its base, and says why",
    "PASS-DRV §5 · a graph with a cycle is refused and the cycle is named",
    "PASS-DRV §5 · a score carrying a cyclic cue is refused before the command is taken",
    "PASS-DRV §5 · one node feeding two channels moves both, and by its own one value",
    "PASS-DRV §5 · the slew node is the only one that remembers, and it moves at its own rate",
    "PASS-DRV §6 · the camera has exactly one authority at every instant",
    "PASS-DRV §6 · two cues claiming one instant are refused, with both named",
    "PASS-DRV §6 · the stage's flight holds still across a window a cue claims for itself",
    "PASS-DRV §6 · the dolly travels in log space, not in raw scale",
    "PASS-DRV §6 · the pose rests on the arriving work within the stated tolerance",
    "PASS-DRV §6 · a flight that leaves the neutral pose is not resting mid-way",
    "PASS-DRV §6 · a handoff between authorities is continuous within the stated tolerance",
    "PASS-DRV §6 · a handoff that jumps is measured and recorded as a jump",
    "PASS-DRV §4.4b · the woven instrument publishes its two clock-driven handles to the score",
]

# The numbers below are computed HERE, from the formulae the contract and the lab state, and handed
# to the runner as expectations. Nothing is read back from the evaluator and then called correct.
TAU = 2 * math.pi
NOISE_0 = math.sin(4.91016 * 41.317 + 0 * 289.107) * 43758.5453
NOISE_0 -= math.floor(NOISE_0)
LN2 = math.log(2.0)

EXPECT = {
    "sources": [
        # name, node, ctx, expected
        ["progress", {"source": "progress"}, {"progress": 0.25}, 0.25],
        ["cueProgress", {"source": "cueProgress"}, {"cueProgress": 0.6}, 0.6],
        ["time", {"source": "time"}, {"seconds": 2.5}, 2.5],
        ["velocity", {"source": "velocity"}, {"velocity": 0.4}, 0.4],
        ["capability", {"source": "capability"}, {"capability": 1}, 1.0],
        ["noise", {"source": "noise", "seed": 4.91016, "stream": 0}, {}, NOISE_0],
    ],
    "operators": [
        ["static", {"op": "static", "value": 0.75}, {}, 0.75],
        ["curve linear", {"op": "curve", "name": "linear", "in": {"source": "progress"}},
         {"progress": 0.25}, 0.25],
        ["curve smooth", {"op": "curve", "name": "smooth", "in": {"source": "progress"}},
         {"progress": 0.25}, 0.15625],
        ["curve in", {"op": "curve", "name": "in", "in": {"source": "progress"}},
         {"progress": 0.25}, 0.0625],
        ["curve out", {"op": "curve", "name": "out", "in": {"source": "progress"}},
         {"progress": 0.25}, 0.4375],
        # The monotone spline, Fritsch-Carlson: three points on one straight rise, read half-way
        # into the first segment. Both end tangents are zero, the middle tangent is the mean of the
        # two chords, and the cubic between them lands at 0.75.
        ["spline", {"op": "spline", "in": {"source": "time"},
                    "points": [{"at": 0, "value": 0}, {"at": 1, "value": 2}, {"at": 2, "value": 4}]},
         {"seconds": 0.5}, 0.75],
        ["spline holds before its first point",
         {"op": "spline", "in": {"source": "time"},
          "points": [{"at": 1, "value": 5}, {"at": 2, "value": 9}]}, {"seconds": 0}, 5.0],
        ["map", {"op": "map", "in": {"source": "progress"}, "from": [0, 1], "to": [10, 20]},
         {"progress": 0.25}, 12.5],
        ["add", {"op": "add", "in": [1, 2, 3]}, {}, 6.0],
        ["multiply", {"op": "multiply", "in": [2, 3, 4]}, {}, 24.0],
        ["mix", {"op": "mix", "a": 10, "b": 20, "t": {"source": "progress"}}, {"progress": 0.25}, 12.5],
        ["clamp", {"op": "clamp", "in": {"op": "static", "value": 5}, "min": 0, "max": 1}, {}, 1.0],
        # hold stands still until the next point arrives; segment walks there on the named curve
        ["hold", {"op": "hold", "in": {"source": "progress"},
                  "points": [{"at": 0, "value": 0}, {"at": 1, "value": 5}]}, {"progress": 0.5}, 0.0],
        ["segment linear", {"op": "segment", "in": {"source": "progress"},
                            "points": [{"at": 0, "value": 0},
                                       {"at": 1, "value": 5, "shape": "linear"}]},
         {"progress": 0.5}, 2.5],
        ["segment smooth", {"op": "segment", "in": {"source": "progress"},
                            "points": [{"at": 0, "value": 0},
                                       {"at": 1, "value": 4, "shape": "smooth"}]},
         {"progress": 0.5}, 2.0],
        # THE STRIP-COUNT BREATH, exactly as the module drifts it (weave.js:452):
        # 1 + 0.35 * sin(t * 0.021 * TAU + 1.1). His numbers, carried, never re-invented.
        ["oscillate sin — the strip-count breath",
         {"op": "oscillate", "rate": 0.021, "phase": 1.1, "shape": "sin", "in": {"source": "time"}},
         {"seconds": 7.0}, math.sin(TAU * 0.021 * 7.0 + 1.1)],
        # THE BALANCE DRIFT, a cubed sine (weave.js:450-451): 0.97 * sin(t * 0.030 * TAU)^3
        ["oscillate cubed-sin — the balance drift",
         {"op": "multiply", "in": [0.97, {"op": "oscillate", "rate": 0.030, "phase": 0,
                                          "shape": "cubed-sin", "in": {"source": "time"}}]},
         {"seconds": 7.0}, 0.97 * math.sin(TAU * 0.030 * 7.0) ** 3],
        ["oscillate tri", {"op": "oscillate", "rate": 0.25, "phase": 0, "shape": "tri",
                           "in": {"source": "time"}}, {"seconds": 1.0}, 1.0],
        ["a node reference reads the node it names",
         {"node": "three"}, {"progress": 0}, 3.0],
    ],
    "logMid": LN2,
}

RUNNER = r"""
// The window pass-layer.js expects to find itself in. Nothing about the file under test is stubbed:
// this is the BUILT artifact, and the bench it publishes hands back the very evaluator a running
// frame calls and the very camera evaluation a running frame applies.
global.window = { devicePixelRatio: 1, innerWidth: 390, innerHeight: 844 };
global.performance = { now: function () { return 0; } };
window.__@@NS@@Pass = {};
window.__@@NS@@PassLayer = function (h) { window.__host = h; };
require(process.argv[2]);
var bench = window.__@@NS@@Pass.bench;
var host = window.__host;

// THE INSTRUMENTS, PUT ON THE REGISTRY BY THE HOST'S OWN DOOR. Each ships in a file of its own,
// which a browser host fetches at the address the site's record gives its name and weighs before
// running. Node offers neither a fetch of a relative address nor a blob script road, so the host
// refuses every file here and says why — and this runner then performs the same two steps by hand:
// read each built file, and hand the instrument it declares to host.register, which is the very
// function the browser road calls. The manifest rows below therefore read a real manifest off a
// real registry, judged by the real manifestWhyNo, with nothing stubbed.
var loaded = [];
window.__@@NS@@PassInstrument = function (p) { loaded.push(p.instrument); };
for (var ai = 4; ai < process.argv.length; ai++) require(process.argv[ai]);
if (!loaded.length) { process.stderr.write("no built instrument file declared anything\n"); process.exit(3); }
loaded.forEach(function (i) {
  if (!host.register(i)) { process.stderr.write("host refused " + i.name + "\n"); process.exit(4); }
});
var E = JSON.parse(process.argv[3]);
var out = {};

function near(a, b, tol) { return typeof a === "number" && Math.abs(a - b) <= (tol || 1e-12); }

// ---- sources and operators, each against its stated value ------------------------------------
function table(rows) {
  var bad = [], seen = [];
  rows.forEach(function (r) {
    var got = bench.driver(r[1], { three: { op: "static", value: 3 } }, r[2]);
    seen.push(r[0] + "=" + (got.ok ? got.v : "(" + got.why + ")"));
    if (!got.ok || !near(got.v, r[3], 1e-9)) {
      bad.push(r[0] + ": wanted " + r[3] + ", got " + (got.ok ? got.v : got.why));
    }
  });
  return { ok: !bad.length, bad: bad, seen: seen };
}
out.sources = table(E.sources);
out.operators = table(E.operators);

// ---- pointer: declared, falling back to its base, with the fallback recorded ------------------
var ptr = bench.driver({ source: "pointer" }, {}, {});
out.pointer = { ok: ptr.ok === false && /pointer/.test(ptr.why || ""), why: ptr.why || null };

// ---- the cycle, named ------------------------------------------------------------------------
var ring = bench.cycle({
  duty:    { op: "add",      in: [{ node: "balance" }] },
  balance: { op: "multiply", in: [{ node: "travel" }, 0.5] },
  travel:  { op: "clamp",    in: { node: "duty" }, min: 0, max: 1 }
});
out.cycle = { ok: !!ring && /duty/.test(ring) && /balance/.test(ring) && /travel/.test(ring)
                  && ring.split(" → ").length === 4, ring: ring };
var acyclic = bench.cycle({ a: { op: "add", in: [{ node: "b" }] }, b: { op: "static", value: 1 } });
out.cycle.clean = acyclic;

var refused = bench.scoreWhyNo({
  duration: 3000,
  cues: [{ id: "weave-main", instrument: { id: "weave" }, window: [0, 3],
           nodes: { p: { op: "add", in: [{ node: "q" }] }, q: { op: "add", in: [{ node: "p" }] } },
           tracks: { mix: { node: "p" } } }]
});
out.scoreCycle = { ok: !!refused && /cycle/.test(refused) && /p → q → p/.test(refused), why: refused };

// ---- ONE NODE, TWO CHANNELS ------------------------------------------------------------------
// The law "one envelope couples the axes" needs exactly this: the balance that drives duty, travel
// amplitude and the geometric cap at once is ONE node with several readers, not copies that drift.
var nodes = { env: { op: "oscillate", rate: 0.030, phase: 0, shape: "cubed-sin",
                     in: { source: "time" } } };
function two(sec) {
  return {
    env: bench.driver({ node: "env" }, nodes, { seconds: sec }).v,
    duty: bench.driver({ op: "map", in: { node: "env" }, from: [-1, 1], to: [0, 1] },
                       nodes, { seconds: sec }).v,
    amp: bench.driver({ op: "multiply", in: [{ node: "env" }, 0.10] }, nodes, { seconds: sec }).v
  };
}
var t1 = two(3.0), t2 = two(9.0);
out.shared = {
  ok: t1.duty !== t2.duty && t1.amp !== t2.amp
      && near(t1.duty, (t1.env + 1) / 2, 1e-12) && near(t1.amp, t1.env * 0.10, 1e-12)
      && near(t2.duty, (t2.env + 1) / 2, 1e-12) && near(t2.amp, t2.env * 0.10, 1e-12),
  at3: t1, at9: t2
};

// ---- slew: the one node that remembers -------------------------------------------------------
var st = {};
var spec = { op: "slew", in: { op: "static", value: 10 }, rate: 2 };
var a0 = bench.driver(spec, {}, { state: st, dt: 0 }).v;        // seeds where the input stands
var a1 = bench.driver(spec, {}, { state: st, dt: 0.5 }).v;      // may move 2 * 0.5 = 1
var a2 = bench.driver(spec, {}, { state: st, dt: 0.5 }).v;
var frozen = {};
bench.driver(spec, {}, { state: frozen, dt: 0 });
var pinned = bench.driver(spec, {}, { state: frozen, dt: 0 }).v; // a pinned clock holds it still
out.slew = { ok: a0 === 10 && a1 === 10 && a2 === 10 && pinned === 10, a0: a0, a1: a1, a2: a2 };
var st2 = {};
var rising = { op: "slew", in: { op: "static", value: 10 }, rate: 2 };
// seeded at 0 by hand, so the walk toward 10 is visible
st2["seedme"] = 0;
rising.__id = "seedme";
var b1 = bench.driver(rising, {}, { state: st2, dt: 0.5 }).v;
var b2 = bench.driver(rising, {}, { state: st2, dt: 0.5 }).v;
var b3 = bench.driver(rising, {}, { state: st2, dt: 0 }).v;
out.slew.walk = { b1: b1, b2: b2, b3: b3,
                  ok: near(b1, 1, 1e-12) && near(b2, 2, 1e-12) && near(b3, 2, 1e-12) };

// ---- THE CAMERA ------------------------------------------------------------------------------
// A TRACK POINT is what a score writes — a place, at a second or at one of the two doors.
function pt(at, over) {
  var p = { at: at, pan: { x: 0, y: 0 }, logScale: 0, pitch: 0, yaw: 0, roll: 0, fov: null };
  Object.keys(over || {}).forEach(function (k) { p[k] = over[k]; });
  return p;
}
// A POSE is what the host computes and what a cue carrying the camera reports back each frame.
function pose(over) {
  var p = { panX: 0, panY: 0, logScale: 0, pitch: 0, yaw: 0, roll: 0, fov: null };
  Object.keys(over || {}).forEach(function (k) { p[k] = over[k]; });
  return p;
}
var tol = bench.camTolerances();
out.tolerances = tol;

// A pass that rests where it started: one point, the neutral pose, covering the whole window.
var restScore = { duration: 3000, camera: { owner: "stage", rests: "b", track: [pt("b")] },
                  cues: [{ id: "weave-main", window: [0, 3], cameraAuthority: "stage" }] };
// A flight that leaves the neutral pose and comes back to it exactly at B.
var flightScore = { duration: 3000,
  camera: { owner: "stage", rests: "b",
            track: [pt("a"), pt(1.5, { pan: { x: 0.12, y: -0.04 }, logScale: 0.2 }), pt("b")] },
  cues: [{ id: "weave-main", window: [0, 3], cameraAuthority: "stage" }] };

function neutralOff(pose) {
  var n = bench.camNeutral(), worst = 0;
  ["panX", "panY", "logScale", "pitch", "yaw", "roll", "fov"].forEach(function (k) {
    var a = typeof pose[k] === "number" ? pose[k] : 0;
    var b = typeof n[k] === "number" ? n[k] : 0;
    worst = Math.max(worst, Math.abs(a - b));
  });
  return worst;
}
out.rest = {
  restScore: neutralOff(bench.camera(restScore, 3.0).pose),
  flightEnd: neutralOff(bench.camera(flightScore, 3.0).pose),
  flightMid: neutralOff(bench.camera(flightScore, 1.5).pose),
  tol: tol.rest
};
out.rest.ok = out.rest.restScore <= tol.rest && out.rest.flightEnd <= tol.rest;
out.rest.movedOk = out.rest.flightMid > tol.rest;

// ---- ONE AUTHORITY AT EVERY INSTANT ----------------------------------------------------------
var ownScore = { duration: 3000,
  camera: { owner: "stage", rests: "b",
            track: [pt("a"), pt(1.0, { logScale: 0.3 }), pt("b")] },
  cues: [{ id: "weave-main", window: [0, 3], cameraAuthority: "stage" },
         { id: "floor", window: [1.0, 2.0], cameraAuthority: "own" }] };
var owners = [], single = true;
for (var i = 0; i <= 100; i++) {
  var tt = 3.0 * i / 100;
  var got = bench.camera(ownScore, tt, pose());
  if (typeof got.owner !== "string" || !got.owner) single = false;
  owners.push(got.owner);
}
var inside = owners.filter(function (o, ix) { var tt = 3 * ix / 100; return tt > 1.0 && tt < 2.0; });
var outside = owners.filter(function (o, ix) { var tt = 3 * ix / 100; return tt < 1.0 || tt > 2.0; });
out.authority = {
  ok: single && inside.every(function (o) { return o === "cue:floor"; })
      && outside.every(function (o) { return o === "stage"; }),
  kinds: owners.filter(function (o, ix, a) { return a.indexOf(o) === ix; })
};

var clash = bench.scoreWhyNo({ duration: 3000, cues: [
  { id: "floor", window: [1.0, 2.0], cameraAuthority: "own" },
  { id: "box", window: [1.5, 2.5], cameraAuthority: "own" }] });
out.clash = { ok: !!clash && /floor/.test(clash) && /box/.test(clash)
                  && /one authority at a time/.test(clash), why: clash };

// THE STAGE HOLDS STILL across a window a cue claims for itself: its own clock stops, so the pose
// it resumes from is the pose it froze at. A pose that jumped instead would be a camera cut.
var atIn = bench.camera(ownScore, 1.0, pose()).stage;
var atOut = bench.camera(ownScore, 2.0, pose()).stage;
out.held = { ok: near(atIn.logScale, atOut.logScale, 1e-12) && near(atIn.panX, atOut.panX, 1e-12),
             at1: atIn.logScale, at2: atOut.logScale };

// ---- THE DOLLY TRAVELS IN LOG SPACE ----------------------------------------------------------
// Two points a factor of four apart. Half-way the pose must read ln 2, so the applied factor is
// exactly 2 — a raw-scale interpolation would stand at 2.5 there, which is what §6 forbids.
var dolly = { duration: 3000, camera: { owner: "stage", rests: "b",
  track: [pt("a", { logScale: 0 }), pt("b", { logScale: Math.log(4) })] },
  cues: [{ id: "weave-main", window: [0, 3], cameraAuthority: "stage" }] };
var mid = bench.camera(dolly, 1.5).pose;
out.log = { logScale: mid.logScale, scale: Math.exp(mid.logScale), wanted: E.logMid,
            ok: near(mid.logScale, E.logMid, 1e-12) && near(Math.exp(mid.logScale), 2, 1e-9) };

// ---- THE HANDOFF, MEASURED -------------------------------------------------------------------
// A cue takes the camera at 1.0 s. Reporting the pose the stage stood at makes the handoff
// continuous; reporting a different one makes it a jump, and the host writes down which it saw.
var stageAt1 = bench.camera(ownScore, 1.0).stage;
var WALK = [0.5, 0.9, 1.0, 1.5, 2.0, 2.5, 3.0];
var smooth = bench.cameraWalk(ownScore, WALK, pose({ logScale: stageAt1.logScale }));
var jumped = bench.cameraWalk(ownScore, WALK, pose({ logScale: stageAt1.logScale + 0.5 }));
out.handoff = {
  smooth: smooth, jumped: jumped, tol: tol.handoff,
  ok: smooth.handoffs.length >= 2
      && smooth.handoffs.every(function (h) { return h.within === true; }),
  jumpOk: jumped.handoffs.some(function (h) { return h.within === false && h.off > tol.handoff; })
};

// ---- §4.4b: the two handles that answered to no track ----------------------------------------
var man = bench.manifest("weave");
out.handles = {
  names: Object.keys(man.handles),
  ok: ["mix", "clock", "strips", "axis", "speed", "seed", "nMul", "press", "bal"]
        .every(function (k) { return !!man.handles[k]; })
      && man.handles.press.max === 1.30 && man.handles.nMul.min === 0.62
      && man.handles.nMul.max === 1.65 && man.handles.bal.open === true
};

process.stdout.write(JSON.stringify(out));
"""


def run_node():
    ns = re.search(r"window\.__(\w+?)PassLayer", BUILT)
    if not ns:
        return None, "the built file names no PassLayer join point"
    runner = TMP / "drivers-runner.js"
    runner.write_text(RUNNER.replace("@@NS@@", ns.group(1)), encoding="utf-8")
    proc = subprocess.run([NODE, str(runner), str(TMP / "pass-layer.js"), json.dumps(EXPECT)]
                          + [str(q) for q in sorted(TMP.glob("pass-inst-*.js"))],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-600:]
    try:
        return json.loads(proc.stdout), None
    except Exception as e:
        return None, f"{e}: {proc.stdout[:400]}"


if not NODE:
    for r in ROWS:
        skip(r, "node is not installed (pinned expected skip)")
else:
    out, err = run_node()
    if out is None:
        for r in ROWS:
            skip(r, "the runner never answered: " + str(err))
    else:
        check(ROWS[0], out["sources"]["ok"], "; ".join(out["sources"]["bad"]) or
              "; ".join(out["sources"]["seen"]))
        check(ROWS[1], out["operators"]["ok"], "; ".join(out["operators"]["bad"]) or
              f"{len(out['operators']['seen'])} operators, each on its stated value")
        check(ROWS[2], out["pointer"]["ok"], f"why={out['pointer']['why']}")
        check(ROWS[3], out["cycle"]["ok"] and out["cycle"]["clean"] is None,
              f"cycle={out['cycle']['ring']} acyclic={out['cycle']['clean']}")
        check(ROWS[4], out["scoreCycle"]["ok"], f"why={out['scoreCycle']['why']}")
        check(ROWS[5], out["shared"]["ok"],
              f"at 3 s {out['shared']['at3']} · at 9 s {out['shared']['at9']}")
        check(ROWS[6], out["slew"]["ok"] and out["slew"]["walk"]["ok"],
              f"seeded-at-input={out['slew']} walk={out['slew']['walk']}")
        check(ROWS[7], out["authority"]["ok"], f"owners seen: {out['authority']['kinds']}")
        check(ROWS[8], out["clash"]["ok"], f"why={out['clash']['why']}")
        check(ROWS[9], out["held"]["ok"],
              f"the stage's logScale at 1.0 s is {out['held']['at1']} and at 2.0 s is {out['held']['at2']}")
        check(ROWS[10], out["log"]["ok"],
              f"half-way between 1x and 4x the pose reads logScale {out['log']['logScale']} "
              f"= scale {out['log']['scale']} (raw-scale interpolation would stand at 2.5)")
        check(ROWS[11], out["rest"]["ok"],
              f"resting score {out['rest']['restScore']}, flight at B {out['rest']['flightEnd']}, "
              f"tolerance {out['rest']['tol']}")
        check(ROWS[12], out["rest"]["movedOk"],
              f"the same flight stands {out['rest']['flightMid']} from neutral at 1.5 s — the row "
              f"above is not vacuous")
        check(ROWS[13], out["handoff"]["ok"],
              f"handoffs={out['handoff']['smooth']['handoffs']} tolerance {out['handoff']['tol']}")
        check(ROWS[14], out["handoff"]["jumpOk"],
              f"a cue reporting a pose 0.5 from the stage's own is measured: "
              f"{out['handoff']['jumped']['handoffs']}")
        check(ROWS[15], out["handles"]["ok"], f"handles={out['handles']['names']}")

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
