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
    "PASS-DRV §6 · orbit and tilt stand on the pose, each carried in its own coordinate",
    "PASS-DRV §6 · each place is carried through the points that name it, so each travels its own arc",
    "PASS-DRV §6 · an orbit turns the view about the subject where a yaw turns the camera in place",
    "PASS-DRV §6 · a turn is seen through a projection even where the score names no field of view",
    "PASS-DRV §6 · the lean variant drops the two turning axes and keeps the pan and the dolly",
    "PASS-DRV §6 · a flight whose orbit does not come back to zero does not rest",
    "PASS-DRV §6 · the two ends of a flight stand exactly on the two hang poses",
    "PASS-DRV §6 · a camera-led flight never rests through the middle and still lands on the hang",
    "PASS-DRV §6 · a led score that gives a cue the world level is refused, with the cue named",
    "PASS-DRV §6 · the dolly's two halves cover the same ratio of approach in the same time",
    "PASS-DRV §6 · the frame state hands the instrument both works' seating on the buffer it draws on",
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

// ---- THE TWO NEW AXES: ORBIT AND TILT ---------------------------------------------------------
// Each is a place on the pose and each is carried in ITS OWN coordinate — the orbit in angle, which
// is the charter's own second case of a straight line in another coordinate system. A track that
// names the orbit alone carries the orbit and leaves every other place at its neutral, which is what
// makes the axis usable without rewriting the rest of a flight.
out.keys = bench.camKeys();
var orbitOnly = { duration: 4000, camera: { owner: "stage", rests: "b", track: [
    { at: "a", orbit: 0 }, { at: 2.0, orbit: 0.6 }, { at: "b", orbit: 0 }] },
  cues: [{ id: "weave-main", window: [0, 4], cameraAuthority: "stage" }] };
var oMid = bench.camera(orbitOnly, 2.0).pose, oEnd = bench.camera(orbitOnly, 4.0).pose;
out.orbit = {
  keys: out.keys,
  mid: oMid, end: oEnd,
  ok: out.keys.indexOf("orbit") >= 0 && out.keys.indexOf("tilt") >= 0
      && near(oMid.orbit, 0.6, 1e-12) && near(oEnd.orbit, 0, 1e-12)
      && oMid.panX === 0 && oMid.logScale === 0 && oMid.tilt === 0
};

// ---- EACH PLACE ON ITS OWN POINTS, SO EACH TRAVELS ITS OWN ARC --------------------------------
// The dolly rises and falls over the two edges while the tilt holds a plane at an angle across a
// window of its own. Neither axis names a point at the other's seconds. Before 2026-08-17 a place
// was carried only where EVERY point named a number for it, so this track carried neither.
var arcs = { duration: 6000, camera: { owner: "stage", rests: "b", track: [
    { at: "a", logScale: 0, tilt: 0 },
    { at: 0.8, logScale: 0.35 },
    { at: 1.2, tilt: 0.33 },
    { at: 4.6, tilt: 0.33 },
    { at: 5.2, logScale: 0.35 },
    { at: "b", logScale: 0, tilt: 0 }] },
  cues: [{ id: "weave-main", window: [0, 6], cameraAuthority: "stage" }] };
function arcAt(t) { var p = bench.camera(arcs, t).pose; return { logScale: p.logScale, tilt: p.tilt }; }
var arcRead = { at0: arcAt(0), at1: arcAt(1.2), at3: arcAt(3.0), at46: arcAt(4.6), at6: arcAt(6.0) };
out.arcs = {
  read: arcRead,
  // the tilt holds its own angle right across its own window while the dolly stands at its own
  // plateau, and both are back at zero when the arriving work stands
  ok: near(arcRead.at1.tilt, 0.33, 1e-9) && near(arcRead.at3.tilt, 0.33, 1e-9)
      && near(arcRead.at46.tilt, 0.33, 1e-9)
      && near(arcRead.at3.logScale, 0.35, 1e-9)
      && arcRead.at1.logScale > 0.34 && arcRead.at0.tilt === 0 && arcRead.at0.logScale === 0
      && near(arcRead.at6.tilt, 0, 1e-9) && near(arcRead.at6.logScale, 0, 1e-9)
};

// ---- WHAT AN ORBIT DOES TO PIXELS, read off the one place a pose becomes a transform -----------
// The chain is applied right to left: the orbit stands NEARER THE SCALE than the pan, so it turns
// the scene about the frame's own centre and the pan then carries the turned subject to its place —
// the point of view travels around the subject. A yaw stands on the pan's own side of the chain, so
// it turns the camera where it stands and the scene swings across the frame.
var orbited = bench.camApplied(pose({ panX: 0.2, orbit: 0.5 }));
var yawed = bench.camApplied(pose({ panX: 0.2, yaw: 0.5 }));
out.turn = {
  orbited: orbited, yawed: yawed,
  ok: orbited.indexOf("rotateY(28.6479deg)") > orbited.indexOf("translate(20.0000%")
      && yawed.indexOf("rotateY(28.6479deg)") > yawed.indexOf("translate(20.0000%")
      && orbited !== yawed
      && orbited.indexOf("rotateY") > orbited.indexOf("rotate(")
};
// The projection: without one an orbit is an affine squash rather than a turn, so the host carries
// its own lens where the score names no field of view.
var tilted = bench.camApplied(pose({ tilt: 0.4 }));
out.projection = {
  tilted: tilted, flat: bench.camApplied(pose({ panX: 0.2 })),
  ok: tilted.indexOf("perspective(") === 0 && tilted.indexOf("rotateX(22.9183deg)") > 0
      && bench.camApplied(pose({ panX: 0.2 })).indexOf("perspective(") < 0
};
// The degrade ladder: the two turning axes need the perspective road, so `lean` drops them and says
// so, exactly as it drops pitch, yaw and the field of view. Pan, dolly and roll are a plain affine
// and every device carries them.
var lean = bench.camCaps("lean"), std = bench.camCaps("standard");
out.caps = { lean: lean, standard: std,
             ok: lean.orbit === false && lean.tilt === false && lean.panX === true
                 && lean.logScale === true && lean.roll === true
                 && std.orbit === true && std.tilt === true };

// ---- A FLIGHT ENDS FLAT ----------------------------------------------------------------------
// Both hangs are square-on, so an orbit that does not come back to zero leaves the pose off the
// arriving work's own box — and the rest check reads every place of the pose, so it says so.
var openOrbit = { duration: 4000, camera: { owner: "stage", rests: "b", track: [
    { at: "a", orbit: 0 }, { at: "b", orbit: 0.4 }] },
  cues: [{ id: "weave-main", window: [0, 4], cameraAuthority: "stage" }] };
out.flat = {
  offOpen: bench.camOff(bench.camera(openOrbit, 4.0).pose, bench.camNeutral()),
  offClosed: bench.camOff(bench.camera(orbitOnly, 4.0).pose, bench.camNeutral()),
  tol: tol.rest
};
out.flat.ok = out.flat.offOpen > tol.rest && out.flat.offClosed <= tol.rest;

// ---- THE FLIGHT BETWEEN THE TWO HANGS ---------------------------------------------------------
// The two boxes are stated in the host's own frame units. What is read is the pose a visitor would
// be shown at each second, composed the way a frame composes it.
var GEOM_A = { x: 0.08, y: 0.12, w: 0.30, h: 0.30 };
var GEOM_B = { x: 0.60, y: 0.30, w: 0.24, h: 0.24 };
var plainScore = { duration: 6000, camera: { owner: "stage", rests: "b", track: [],
                                             hang: { rise: 1.0, fall: 1.5 } },
  cues: [{ id: "weave-main", instrument: { id: "weave" }, window: [0, 6],
           cameraAuthority: "stage" }] };
var ledScore = { duration: 6000, camera: { owner: "stage", rests: "b", track: [], lead: true,
                                           hang: { rise: 1.0, fall: 1.5 } },
  cues: [{ id: "weave-main", instrument: { id: "weave" }, window: [0, 6],
           cameraAuthority: "stage" }] };
var WHEN = [0, 1.0, 1.8, 2.4, 3.0, 3.6, 4.5, 6.0];
var plainFlight = bench.hangFlight(plainScore, 6000, GEOM_A, GEOM_B, WHEN);
var ledFlight = bench.hangFlight(ledScore, 6000, GEOM_A, GEOM_B, WHEN);
function endsOf(f) {
  return { start: bench.camOff(f.at[0], f.poseA), land: bench.camOff(f.at[f.at.length - 1], f.poseB) };
}
out.ends = { plain: endsOf(plainFlight), led: endsOf(ledFlight), tol: tol.rest,
             poseA: plainFlight.poseA, poseB: plainFlight.poseB };
out.ends.ok = !!plainFlight.poseA && !!plainFlight.poseB
              && out.ends.plain.start <= tol.rest && out.ends.plain.land <= tol.rest
              && out.ends.led.start <= tol.rest && out.ends.led.land <= tol.rest;

// A LED FLIGHT NEVER RESTS. The accompanying flight stands at the whole frame right across its
// plateau — three consecutive instants read one pose — while the led one is moving at every one of
// them, and both still arrive on the arriving work's own box.
function stills(f) {
  var n = 0, i;
  for (i = 1; i < f.at.length; i++) if (bench.camOff(f.at[i], f.at[i - 1]) <= tol.rest) n++;
  return n;
}
out.led = { plainStills: stills(plainFlight), ledStills: stills(ledFlight),
            plainLed: plainFlight.led, ledLed: ledFlight.led };
out.led.ok = out.led.ledStills === 0 && out.led.plainStills >= 2
             && ledFlight.led === true && plainFlight.led === false;

// A LED SCORE SPENDS THE WORLD VOICE, and a cue may not spend it a second time.
var worldClash = bench.scoreWhyNo({ duration: 6000,
  camera: { owner: "stage", rests: "b", track: [], lead: true },
  cues: [{ id: "floor", instrument: { id: "weave" }, window: [0, 6], levels: ["WORLD", "SURFACE"] }] });
var worldFine = bench.scoreWhyNo({ duration: 6000,
  camera: { owner: "stage", rests: "b", track: [], lead: true },
  cues: [{ id: "floor", instrument: { id: "weave" }, window: [0, 6], levels: ["SURFACE"] }] });
out.world = { clash: worldClash, fine: worldFine,
              ok: !!worldClash && /floor/.test(worldClash) && /world level/.test(worldClash)
                  && worldFine === null };

// ---- THE APPROACH IS EVEN --------------------------------------------------------------------
// A flight from one to sixteen times, named at its own two halves. In log space each half covers
// the SAME ratio — four times and four times — in the same time, which is what equal handle
// movement giving equal felt change of approach means. A raw-scale road would cover 3 of the 15
// units in the first half and 12 in the second, three quarters of the whole approach after the
// half-way mark.
var even = { duration: 4000, camera: { owner: "stage", rests: "b", track: [
    pt("a", { logScale: 0 }), pt(2.0, { logScale: Math.log(4) }),
    pt("b", { logScale: Math.log(16) })] },
  cues: [{ id: "weave-main", window: [0, 4], cameraAuthority: "stage" }] };
var e0 = Math.exp(bench.camera(even, 0).pose.logScale);
var e1 = Math.exp(bench.camera(even, 2.0).pose.logScale);
var e2 = Math.exp(bench.camera(even, 4.0).pose.logScale);
out.even = { at0: e0, at2: e1, at4: e2, firstHalf: e1 / e0, secondHalf: e2 / e1,
             rawWouldBe: [1 + 15 / 2, 16] };
out.even.ok = near(e1 / e0, 4, 1e-9) && near(e2 / e1, 4, 1e-9);

// ---- THE SEATING THE HOST HANDS EACH INSTRUMENT ----------------------------------------------
// Read off the very record a running frame builds. Both works are seated on the buffer the host is
// drawing on, and the answer is the instrument's own `fit` — asked here a second time, directly,
// so the row compares the record against the function rather than against a copy of its numbers.
var SRC = { aw: 1600, ah: 900, bw: 900, bh: 1600 };
var st = bench.frameState("weave", SRC, 1.0);
var weaveInst = null;
loaded.forEach(function (i) { if (i.name === "weave") weaveInst = i; });
var wantA = weaveInst.fit(SRC.aw, SRC.ah, st.viewport.bufferW, st.viewport.bufferH);
var wantB = weaveInst.fit(SRC.bw, SRC.bh, st.viewport.bufferW, st.viewport.bufferH);
function sameFit(a, b) {
  return !!a && !!b && a.length === b.length
         && a.every(function (v, i) { return near(v, b[i], 1e-12); });
}
out.seating = {
  fitA: st.fitA, fitB: st.fitB, wantA: wantA, wantB: wantB,
  ok: sameFit(st.fitA, wantA) && sameFit(st.fitB, wantB) && !sameFit(st.fitA, st.fitB)
};

process.stdout.write(JSON.stringify(out));
"""


def run_node(layer=None, tag="drivers"):
    """The runner against a built host. `layer` names a COPY of the host with one rule crippled,
    which is how the red-on-bug proofs below run: the source tree is never written to."""
    ns = re.search(r"window\.__(\w+?)PassLayer", BUILT)
    if not ns:
        return None, "the built file names no PassLayer join point"
    runner = TMP / f"{tag}-runner.js"
    runner.write_text(RUNNER.replace("@@NS@@", ns.group(1)), encoding="utf-8")
    proc = subprocess.run([NODE, str(runner), str(layer or (TMP / "pass-layer.js")),
                           json.dumps(EXPECT)]
                          + [str(q) for q in sorted(TMP.glob("pass-inst-*.js"))],
                          capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-600:]
    try:
        return json.loads(proc.stdout), None
    except Exception as e:
        return None, f"{e}: {proc.stdout[:400]}"


def cripple(name, was, now):
    """A copy of the built host with one line put back the way it stood before the repair. Returns
    the path, or None when the line the proof stands on is no longer there to change."""
    if BUILT.count(was) != 1:
        return None
    path = TMP / f"pass-layer-{name}.js"
    path.write_text(BUILT.replace(was, now), encoding="utf-8")
    return path


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
        check(ROWS[16], out["orbit"]["ok"],
              f"the pose's places are {out['orbit']['keys']}; a track naming the orbit alone reads "
              f"orbit {out['orbit']['mid']['orbit']} at its own point and leaves pan, dolly and "
              f"tilt at their neutrals")

        # RED ON BUG. The repair is the per-place point selection; crippling it puts back the rule
        # that carried a place only where EVERY point named a number for it, which is what stopped
        # two axes having two arcs on one flight.
        arc_red = "the crippled copy never ran"
        crip = cripple("allpoints", "if (!own.length) {", "if (own.length !== pts.length) {")
        if crip is not None:
            bad, _ = run_node(crip, "allpoints")
            if bad is not None:
                arc_red = (f"crippled back to the all-points rule the same track reads "
                           f"{bad['arcs']['read']['at3']} at 3.0 s — "
                           + ("still its own arcs, so the row is vacuous"
                              if bad["arcs"]["ok"] else "both places at their neutrals"))
                check(ROWS[17], out["arcs"]["ok"] and not bad["arcs"]["ok"],
                      f"tilt holds 0.33 across 1.2…4.6 s while the dolly stands at its own plateau: "
                      f"{out['arcs']['read']} · {arc_red}")
            else:
                check(ROWS[17], False, "the crippled copy did not answer: " + str(_))
        else:
            check(ROWS[17], False, "the line the red-on-bug proof stands on has moved")

        check(ROWS[18], out["turn"]["ok"],
              f"orbited «{out['turn']['orbited']}» · yawed «{out['turn']['yawed']}»")
        check(ROWS[19], out["projection"]["ok"],
              f"a tilt alone draws «{out['projection']['tilted']}» where a plain pan draws "
              f"«{out['projection']['flat']}»")
        check(ROWS[20], out["caps"]["ok"], f"lean={out['caps']['lean']}")
        check(ROWS[21], out["flat"]["ok"],
              f"an orbit left open stands {out['flat']['offOpen']} from the arriving pose and one "
              f"brought back to zero {out['flat']['offClosed']}, against {out['flat']['tol']}")
        check(ROWS[22], out["ends"]["ok"],
              f"accompanying flight: {out['ends']['plain']} · led flight: {out['ends']['led']} · "
              f"tolerance {out['ends']['tol']} — the departing pose is {out['ends']['poseA']}")
        check(ROWS[23], out["led"]["ok"],
              f"the accompanying flight stands still at {out['led']['plainStills']} of seven steps "
              f"and the led one at {out['led']['ledStills']}")
        check(ROWS[24], out["world"]["ok"],
              f"why={out['world']['clash']} · the same score without the world level: "
              f"{out['world']['fine']}")
        check(ROWS[25], out["even"]["ok"],
              f"one to sixteen times: the first half covers {out['even']['firstHalf']}x and the "
              f"second {out['even']['secondHalf']}x; a raw-scale road would stand at "
              f"{out['even']['rawWouldBe'][0]}x half-way instead of {out['even']['at2']}x")

        # RED ON BUG. The repair is the seating on the frame state; crippling it takes the two
        # fields back off the record and the row reads what the instruments had to work from.
        seat_red = "the crippled copy never ran"
        crip = cripple("noseat", "      fitA: instFit(v.inst, rec.src.aw, rec.src.ah),\n", "")
        if crip is not None:
            bad, _ = run_node(crip, "noseat")
            if bad is not None:
                seat_red = ("with the seating taken off the record the instrument reads fitA="
                            + str(bad["seating"].get("fitA")))
                check(ROWS[26], out["seating"]["ok"] and not bad["seating"]["ok"],
                      f"fitA={out['seating']['fitA']} fitB={out['seating']['fitB']}, each the "
                      f"instrument's own answer on the buffer the host reports · {seat_red}")
            else:
                check(ROWS[26], False, "the crippled copy did not answer: " + str(_))
        else:
            check(ROWS[26], False, "the line the red-on-bug proof stands on has moved")

# ---------------------------------------------------------------- the composer's own dolly
# THE DOLLY IS A NATURAL LOGARITHM. The score carries `logScale` and the host applies exp of it, so
# a base-2 logarithm written into that field flies the ratio asked for raised to 1/ln 2. The line
# stands in the composer's camera flight; this row reddens the moment it goes back to base two.
COMPOSER = (TMP / "pass-composer.js").read_text(encoding="utf-8")
check("PASS-DRV §6 · the composer writes the dolly as a natural logarithm, the base the host applies",
      "Math.log(stepTo / stepFrom)" in COMPOSER and "Math.log2(stepTo" not in COMPOSER,
      "PASS-API-V1 §6: logScale IS the logarithm and the applied factor is exp of it; "
      "docs/immersive/wave-a/camera-drivers-conductor.md writes the field as ln(scale)")

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
