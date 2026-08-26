#!/usr/bin/env python3
"""EX-PASS shelf 5, THE CONJUROR — the content swap sits at the plan's own motion peak.
Run: python3 tests/test_pass_peak.py

The charter's shelf 5 (lab/CROSSING-BRIEF.md) names two corollaries it calls enforceable at plan
level, and this file measures the second of them:

    the CONJUROR (the content swap sits at the plan's motion peak, computable as argmax of summed
    normalized parameter velocity, where the eye is led away)

WHAT THE SHELF ASKS FOR, IN ARITHMETIC. Over the passage's own normalised time, every handle the
plan drives has a rate of change; each is divided by that handle's own published range, so a handle
with a wide span does not drown one with a narrow span; the sum of those is one dimensionless
reading of how fast the whole plan is moving at an instant, and the instant it is largest is the
motion peak. The witness camera's excursion — its two middle track points, the outbound pose and the
inbound one — is what leads the eye away, so the peak stands inside it.

TWO HANDLES ARE OUT OF THE SUM, AND FOR ONE REASON. A measurement cannot read the thing it is
placing. The DOOR — the handle each cue's own `doors` record names, the share of the arriving work
standing in the frame — IS the content swap the shelf places, so counting its own speed would make
the law say the swap sits where the swap moves fastest. The CAMERA's own track is the other: its two
middle points are what the peak positions, so their velocity is a consequence of the answer and not
an input to it. Everything else the plan drives is in.

WHERE THE TWO POINTS LAND. The excursion keeps the length the composition measured for it and the
room left over, the passage less that length, is shared between the two legs in the proportion the
peak shares the passage. Writing `q` for the peak's own share of the passage, `L` for the
excursion's length and `D` for the passage:

    track[1].at = q · (D − L)          track[2].at = q · (D − L) + L

which needs no clamp: both points stand inside the passage, in their order, at exactly `L` apart,
and the peak itself stands inside the excursion at the same share `q` of it — all four by algebra,
for every `q` in nought to one and every `L` no longer than `D`.

WHAT THIS FILE MEASURES, AND HOW IT AVOIDS ASSERTING THE COMPOSER'S OWN ANSWER BACK AT IT.

  1. THE PLACEMENT, RECOMPUTED FROM THE WIRE. For each pair walked below the composer's own plan is
     read — its cues, their windows, their node tables, and the manifests' published ranges — and
     the summed normalised velocity is walked again HERE, in Python, by an implementation that
     shares no line with the module. The two points must stand where the two lines above put them. A
     module that computed the peak wrongly and placed its excursion consistently with its own wrong
     answer still reds here, because the answer this row compares against is not the module's.

  2. THE ARITHMETIC ITSELF, ON NUMBERS RATHER THAN ON PHOTOGRAPHS. The module hands its peak
     arithmetic out beside its entry, the way it already hands out `r4`, the two writers and the
     four voice arithmetics, and for the same stated reason: what it claims is a claim about
     NUMBERS. So the rows below put constructed cue tables through it — every node kind the composer
     writes, each of the four named curves, each published handle range, windows from a sliver to
     the whole passage — and check the claims over that whole span:

       · the four curves' own crests are closed-form and are checked against the numbers hand
         arithmetic gives: `out` crests at the passage's open, `in` at its close, `smooth` at 1.5 at
         its middle, and `linear` never crests at all because its rate never changes;
       · a window narrower than the passage multiplies the rate by exactly the passage's own length
         over the window's, so a handle that crosses its range in half the passage reads twice as
         fast as one that takes the whole of it;
       · the sum is finite and the argmax lands inside the passage for every one of them;
       · a passage carrying one cue that drives nothing but static readings still has a peak — the
         whole passage attains the maximum, and the peak is that plateau's own middle.

  3. WHAT MUST NOT MOVE. The excursion keeps the LENGTH the composer measured for it — the
     travelling cue's own window, or half the passage where the plan travels on no cue — and both of
     its points stay inside the passage in their own order. These two rows pass before the change
     and after it, and they are the fence around what the change is allowed to touch.

NO ROW HERE COUNTS PAIRS. Every row that walks the real records states a LAW over every pair it
walks and prints the worst reading it found, named by the pair it came from. Nothing here is a
share, a median or a tally of how many pairs did anything, because none of those is a fact about the
crossing a visitor sees.

WHAT IS RED BEFORE THE CHANGE. Rows 1 and 2 are red against the composer as it stands: the module
asserts its motion peak rather than computing one — `fillPlan` puts the excursion at the travelling
cue's own window, or at a tone split where the plan travels on no cue — and it hands out no peak
arithmetic at all. Rows 3 and 4 are green before and after.
"""
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
LAYER = ROOT / "engine" / "assets" / "pass-layer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"
WORKS = ROOT / "tests" / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROW_PLACED = ("EX-PEAK the witness camera's excursion stands at the plan's own motion peak, "
              "recomputed off the wire")
ROW_CURVES = ("EX-PEAK the four named curves' crests are the numbers their own derivatives give, "
              "and where they stand")
ROW_WINDOW = ("EX-PEAK a handle that crosses its range in part of the passage reads faster by "
              "exactly that share")
ROW_SPAN = ("EX-PEAK over every published handle range, every node kind and every window shape the "
            "sum is finite and the peak lands inside the passage")
ROW_STILL = ("EX-PEAK a passage whose handles never move still has a peak, and it is the passage's "
             "own middle")
ROW_LENGTH = ("EX-PEAK the excursion keeps the length the composition measured for it")
ROW_INSIDE = ("EX-PEAK both middle points stand inside the passage, in their own order")
ROW_HOST = ("EX-PEAK the four curves this file differentiates are the four the drawing host draws")
ALL_ROWS = [ROW_PLACED, ROW_CURVES, ROW_WINDOW, ROW_SPAN, ROW_STILL, ROW_LENGTH, ROW_INSIDE,
            ROW_HOST]

STEPS = 1000

# ---------------------------------------------------------------------------------------------
# THE FOUR NAMED CURVES AND THEIR DERIVATIVES, written out. The four shapes are the drawing host's
# own (engine/assets/pass-layer.js's `CURVES`) and the row below reads that file to prove these are
# still the same four, so this table cannot drift away from the curve the viewer actually sees.
#
#   linear(x) = x                        linear'(x) = 1
#   smooth(x) = x²(3 − 2x)               smooth'(x) = 6x(1 − x)
#   in(x)     = x²                       in'(x)     = 2x
#   out(x)    = 1 − (1 − x)²             out'(x)    = 2(1 − x)
#
# Every one is bounded on [0, 1]: the largest any of the four derivatives reaches is 2, at an end
# for `in` and `out` and 1.5 at the middle for `smooth`.
# ---------------------------------------------------------------------------------------------
CURVES = {
    "linear": (lambda x: x, lambda x: 1.0),
    "smooth": (lambda x: x * x * (3 - 2 * x), lambda x: 6 * x * (1 - x)),
    "in": (lambda x: x * x, lambda x: 2 * x),
    "out": (lambda x: 1 - (1 - x) * (1 - x), lambda x: 2 * (1 - x)),
}


def spline_slopes(pts):
    """Fritsch–Carlson tangents, the drawing host's own `splineSlopes` carried over."""
    n = len(pts)
    d = []
    for i in range(n - 1):
        h = pts[i + 1]["at"] - pts[i]["at"]
        d.append((pts[i + 1]["value"] - pts[i]["value"]) / h if h > 0 else 0.0)
    m = [0.0 if (i == 0 or i == n - 1) else (d[i - 1] + d[i]) / 2 for i in range(n)]
    for i in range(n - 1):
        if d[i] == 0:
            m[i] = 0.0
            m[i + 1] = 0.0
            continue
        a = m[i] / d[i]
        b = m[i + 1] / d[i]
        if a < 0:
            a = 0.0
            m[i] = 0.0
        if b < 0:
            b = 0.0
            m[i + 1] = 0.0
        s = a * a + b * b
        if s > 9:
            s = 3 / math.sqrt(s)
            m[i] = s * a * d[i]
            m[i + 1] = s * b * d[i]
    return m


def read_at(spec, u, cue, dur, depth=0):
    """One node's value at normalised passage time `u`, and its rate of change there.

    Returns (value, slope). The slope is in the node's own units per unit of PASSAGE time, so two
    handles living in windows of different lengths are comparable before either is normalised by
    its own published range.
    """
    if spec is None:
        return (0.0, 0.0)
    if isinstance(spec, (int, float)) and not isinstance(spec, bool):
        return (float(spec), 0.0)
    if not isinstance(spec, dict):
        return (0.0, 0.0)
    if depth > 64:
        return (0.0, 0.0)
    if "node" in spec:
        ref = (cue.get("nodes") or {}).get(spec["node"])
        return read_at(ref, u, cue, dur, depth + 1) if ref else (0.0, 0.0)
    if "source" in spec:
        src = spec["source"]
        if src == "progress":
            return (u, 1.0)
        if src == "time":
            return (u * dur, dur)
        if src == "cueProgress":
            w = cue.get("window") or [0.0, dur]
            w0, w1 = float(w[0]), float(w[1])
            if not w1 > w0:
                return (0.0, 0.0)
            p = (u * dur - w0) / (w1 - w0)
            if p <= 0:
                return (0.0, 0.0)
            if p >= 1:
                return (1.0, 0.0)
            return (p, dur / (w1 - w0))
        # velocity, capability, noise and pointer are the HOST's own live signals. A plan cannot
        # know them when it is composed, so they carry no shape here and add nothing to the sum.
        return (0.0, 0.0)
    op = spec.get("op")
    if op == "static":
        return (float(spec.get("value") or 0), 0.0)
    if op == "curve":
        fn, dfn = CURVES.get(spec.get("name"), CURVES["linear"])
        v, s = read_at(spec.get("in"), u, cue, dur, depth + 1)
        if v <= 0:
            return (fn(0.0), 0.0)
        if v >= 1:
            return (fn(1.0), 0.0)
        return (fn(v), dfn(v) * s)
    if op == "map":
        v, s = read_at(spec.get("in"), u, cue, dur, depth + 1)
        f = spec.get("from") or [0, 1]
        t = spec.get("to") or [0, 1]
        f0, f1, t0, t1 = float(f[0]), float(f[1]), float(t[0]), float(t[1])
        if f1 - f0 == 0:
            return (0.0, 0.0)
        return (t0 + (t1 - t0) * ((v - f0) / (f1 - f0)), (t1 - t0) / (f1 - f0) * s)
    if op == "mix":
        av, as_ = read_at(spec.get("a"), u, cue, dur, depth + 1)
        bv, bs = read_at(spec.get("b"), u, cue, dur, depth + 1)
        tv, ts = read_at(spec.get("t"), u, cue, dur, depth + 1)
        return (av + (bv - av) * tv, as_ + (bs - as_) * tv + (bv - av) * ts)
    if op == "clamp":
        v, s = read_at(spec.get("in"), u, cue, dur, depth + 1)
        lo = -math.inf if spec.get("min") is None else float(spec["min"])
        hi = math.inf if spec.get("max") is None else float(spec["max"])
        if v <= lo:
            return (lo, 0.0)
        if v >= hi:
            return (hi, 0.0)
        return (v, s)
    if op == "spline":
        pts = spec.get("points")
        if not isinstance(pts, list) or not pts:
            return (0.0, 0.0)
        pts = [{"at": float(p["at"]), "value": float(p["value"])} for p in pts]
        inp = spec.get("in") if spec.get("in") is not None else {"source": "progress"}
        x, s = read_at(inp, u, cue, dur, depth + 1)
        n = len(pts)
        if n == 1 or x <= pts[0]["at"]:
            return (pts[0]["value"], 0.0)
        if x >= pts[n - 1]["at"]:
            return (pts[n - 1]["value"], 0.0)
        m = spline_slopes(pts)
        i = n - 1
        for k in range(1, n - 1):
            if x <= pts[k]["at"]:
                i = k
                break
        a, b = pts[i - 1], pts[i]
        h = b["at"] - a["at"]
        if not h > 0:
            return (b["value"], 0.0)
        va, vb = a["value"], b["value"]
        t = (x - a["at"]) / h
        t2 = t * t
        t3 = t2 * t
        value = ((2 * t3 - 3 * t2 + 1) * va + (t3 - 2 * t2 + t) * h * m[i - 1]
                 + (3 * t2 - 2 * t3) * vb + (t3 - t2) * h * m[i])
        dt = ((6 * t2 - 6 * t) * va + (3 * t2 - 4 * t + 1) * h * m[i - 1]
              + (6 * t - 6 * t2) * vb + (3 * t2 - 2 * t) * h * m[i]) / h
        return (value, dt * s)
    # An operator the composer writes nowhere carries no shape this file can differentiate. It adds
    # nothing to the ranking and refuses nothing, which is what a measurement is allowed to do.
    return (0.0, 0.0)


def terms_of(cues, manifests):
    """Every driven handle of every cue, with the reciprocal of its own published range.

    THREE HANDLES ARE LEFT OUT, AND FOR ONE REASON: a measurement cannot read the thing it is
    placing. The peak places the content swap, so whatever CARRIES that swap is not evidence about
    where it should stand.

      · the cue's own door handle, taken off the cue's `doors` record rather than off a name typed
        here;
      · `mix`, the crossing dial;
      · `presence`, the reserved dry — the share of the frame a cue stands on, which the composer
        holds back from the swap for the same reason.

    THIS MIRROR WAS ONE LINE BEHIND THE COMPOSER. It dropped the door handle alone, which was the
    whole of the rule while a cue's door record named `mix`. Once the entry door landed, an upper
    cue's door record names `presence` instead — so the dial went back into the sum on exactly those
    cues, while the composer went on excluding both. The composer was swept over 950 plans against
    its own exported arithmetic with no placement disagreement, so the composer is self-consistent
    and it is this side that had drifted.

    `overlay` KEEPS ITS OWN OLDER SENSE OF THE NAME. Its `presence` is not the reserved dry — it is
    an ordinary driven handle of that instrument — so it stays in the sum. The exclusion is about
    what a handle DOES on a cue, and one instrument giving the word another meaning is exactly the
    case a name typed once and applied everywhere would get wrong.
    """
    out = []
    for c in cues:
        iid = (c.get("instrument") or {}).get("id")
        handles = ((manifests.get(iid) or {}).get("handles")) or {}
        door = ((c.get("doors") or {}).get("in") or {}).get("handle")
        for h in sorted((c.get("tracks") or {}).keys()):
            if h == door or h == "mix":
                continue
            if h == "presence" and iid != "overlay":
                continue
            spec = handles.get(h)
            if not spec or spec.get("open"):
                continue
            rng = abs(float(spec["max"]) - float(spec["min"]))
            if not rng > 0:
                continue
            node = (c.get("nodes") or {}).get((c["tracks"][h] or {}).get("node"))
            if node is None:
                continue
            out.append((node, c, 1.0 / rng))
    return out


def peak_of(cues, dur, manifests):
    """The summed normalised velocity's own argmax, as a share of the passage and in seconds.

    The sum is walked on the passage's own normalised time at the same thousand steps the module's
    other walk takes, and STRICTLY INSIDE it: the passage's two ends are where the two works stand
    still — the camera's own first and last poses are the neutral rest, shelf 2's "resting exactly
    when B stands" — so the instant the eye is led away is an instant inside the crossing rather
    than one of its two ends.

    The peak is the MIDDLE of the first maximal run of grid points, so a plateau reads as its own
    centre rather than as its first instant, and a sum that never changes has the whole interior for
    its plateau, whose middle is the passage's own middle.
    """
    if not dur > 0:
        return {"at": 0.0, "share": 0.5, "flat": True, "top": 0.0}
    terms = terms_of(cues, manifests)
    sums = []
    for i in range(1, STEPS):
        u = i / STEPS
        s = 0.0
        for node, cue, inv in terms:
            s += abs(read_at(node, u, cue, dur)[1]) * inv
        sums.append(s)
    top = max(sums)
    low = min(sums)
    lo = hi = None
    for i, s in enumerate(sums):
        if s >= top:
            if lo is None:
                lo = i
            hi = i
        elif lo is not None:
            break
    if lo is None:
        lo = hi = 0
    share = (lo + hi + 2) / 2.0 / STEPS
    return {"at": share * dur, "share": share, "flat": top == low, "top": top}


# ---------------------------------------------------------------------------------------------
# THE DRIVER — the module run in node against a copy of itself held in memory, exactly as
# tests/test_pass_composed.py runs it. Nothing is written to the source tree.
# ---------------------------------------------------------------------------------------------
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath, worksPath] = process.argv.slice(2);
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(0); }
const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8"));
const composer = joined.make(fix.consts);

// The module marks a value Python holds as a float by wrapping it ({v: <number>}). This file runs
// outside the module's own closure and keeps no copy of its `num()`; this is the same unwrap, done
// once over everything that travels out.
function plain(v) {
  if (v === null || typeof v !== "object") return v;
  if (Array.isArray(v)) return v.map(plain);
  const keys = Object.keys(v);
  if (keys.length === 1 && keys[0] === "v" && typeof v.v === "number") return v.v;
  const o = {};
  for (const k of keys) o[k] = plain(v[k]);
  return o;
}
function die(key) {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) { h = Math.imul(h ^ key.charCodeAt(i), 16777619) >>> 0; }
  return (h % 100000) / 100000 * 8;
}

const out = {version: joined.version, plans: [], arithmetic: null};

// ---- the real pairs, composed and handed over whole ----
const PAIRS = JSON.parse(process.env.PAIRS || "[]");
const ALL_IDS = Object.keys(works.works).sort();
for (const [ii, jj] of PAIRS) {
  const xi = ALL_IDS[ii], yi = ALL_IDS[jj];
  const wa = works.works[xi], wb = works.works[yi];
  if (!wa || !wb) continue;
  const dir = xi < yi ? "a-to-b" : "b-to-a";
  const key = wa.id + "__" + wb.id + "__" + (dir === "a-to-b" ? "ab" : "ba");
  let p;
  try { p = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: dir, seed: die(key)}); }
  catch (e) { out.plans.push({key: key, threw: String(e && e.message || e)}); continue; }
  if (!p || p.declined || !p.plan) { out.plans.push({key: key, declined: (p || {}).declined || "no plan"}); continue; }
  out.plans.push({key: key,
                  duration: plain(p.plan.duration),
                  camera: plain(p.plan.camera),
                  cues: plain(p.plan.cues).map((c) => ({id: c.id, instrument: c.instrument,
                                                        window: c.window, tracks: c.tracks,
                                                        doors: c.doors, nodes: c.nodes}))});
}

// ---- the arithmetic itself, on constructed numbers ----
// The module hands its peak arithmetic out beside its entry. Where it does not, this block says so
// and every row that reads it reds by name rather than by an exception.
if (typeof composer.motionPeak !== "function") {
  out.arithmetic = {absent: true};
} else {
  const D = 4.0;
  const mans = fix.consts.manifests;
  // The handle every row below rides is `size` of the meshing instrument, and its two published
  // ends are read off the manifest rather than typed, so a node travelling from one end to the
  // other travels exactly one published range and its normalised rate is the curve's own
  // derivative undivided.
  const SZ = mans.gears.handles.size;
  function cueOf(instrument, handle, node, window) {
    const tracks = {}; tracks[handle] = {node: "t-" + handle};
    const nodes = {}; nodes["t-" + handle] = node;
    return {id: "t", instrument: {id: instrument, api: 1}, window: window || [0, D],
            tracks: tracks, nodes: nodes,
            doors: {"in": {handle: "mix", value: 0}, out: {handle: "mix", value: 1}}};
  }
  function rideNode(shape) {
    return {op: "map", in: {op: "curve", name: shape, in: {source: "cueProgress"}},
            from: [0, 1], to: [Number(SZ.min), Number(SZ.max)]};
  }
  const curves = {};
  for (const shape of ["linear", "smooth", "in", "out"]) {
    curves[shape] = composer.motionPeak([cueOf("gears", "size", rideNode(shape))], D);
  }
  // A handle that crosses its own range inside PART of the passage: the same ride over the whole
  // passage, over half of it, and over a quarter.
  const windows = {
    whole: composer.motionPeak([cueOf("gears", "size", rideNode("linear"), [0, D])], D),
    half: composer.motionPeak([cueOf("gears", "size", rideNode("linear"), [0, D / 2])], D),
    quarter: composer.motionPeak([cueOf("gears", "size", rideNode("linear"), [D / 4, D / 2])], D),
  };
  // One cue that drives nothing but a fixed reading.
  const still = composer.motionPeak(
    [cueOf("gears", "size", {op: "static", value: 0.5})], D);
  // AND THE DOOR IS NOT IN THE SUM. The same cue driving nothing but its own door reads exactly as
  // the still one does, whatever shape the door takes.
  const doorOnly = composer.motionPeak(
    [cueOf("gears", "mix", {op: "mix", a: 0, b: 1,
                            t: {op: "curve", name: "in", in: {source: "cueProgress"}}})], D);
  // THE WHOLE SPAN OF THE VALUES THE FORMULA READS: every published instrument, every handle it
  // publishes that is not open, each of the four curves, and four window shapes — a sliver at the
  // open, a sliver at the close, half the passage and the whole of it.
  const sweep = {worstTop: 0, badTop: [], outside: [], nodeKinds: {}};
  const WINDOWS = [[0, D], [0, D / 2], [D / 2, D], [0, D / STEPS_JS], [D - D / STEPS_JS, D]];
  for (const iid of Object.keys(mans).sort()) {
    const hs = mans[iid].handles || {};
    for (const h of Object.keys(hs).sort()) {
      const spec = hs[h];
      if (!spec || spec.open) continue;
      const lo = Number(spec.min), hi = Number(spec.max);
      for (const shape of ["linear", "smooth", "in", "out"]) {
        for (const w of WINDOWS) {
          const kinds = [
            {op: "map", in: {op: "curve", name: shape, in: {source: "cueProgress"}},
             from: [0, 1], to: [lo, hi]},
            {op: "mix", a: lo, b: hi, t: {op: "curve", name: shape, in: {source: "cueProgress"}}},
            {op: "clamp", min: lo, max: hi,
             in: {op: "map", in: {op: "curve", name: shape, in: {source: "cueProgress"}},
                  from: [0, 1], to: [lo - (hi - lo), hi + (hi - lo)]}},
            {op: "spline", in: {source: "cueProgress"},
             points: [{at: 0, value: lo}, {at: 0.5, value: hi}, {at: 1, value: (lo + hi) / 2}]},
            {op: "static", value: lo},
            {source: "time"},
          ];
          for (let ki = 0; ki < kinds.length; ki++) {
            const got = composer.motionPeak([cueOf(iid, h, kinds[ki], w)], D);
            sweep.nodeKinds[ki] = (sweep.nodeKinds[ki] || 0) + 1;
            if (!isFinite(got.top) || got.top < 0) {
              if (sweep.badTop.length < 4) sweep.badTop.push([iid, h, shape, ki, got.top]);
            } else if (got.top > sweep.worstTop) sweep.worstTop = got.top;
            if (!(got.at >= 0 && got.at <= D)) {
              if (sweep.outside.length < 4) sweep.outside.push([iid, h, shape, ki, got.at]);
            }
          }
        }
      }
    }
  }
  out.arithmetic = {curves: curves, windows: windows, still: still, doorOnly: doorOnly,
                    sweep: sweep, D: D};
}
console.log(JSON.stringify(out));
"""


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


# The ordered pairs this file walks. They are named by index so the walk is the same on every run
# and on every machine; nothing about the collection is read off them beyond the plans they compose.
PAIRS = [[i, j] for i in range(0, 6) for j in range(0, 6) if i != j]

if not node_available():
    for r in ALL_ROWS:
        skip(r, "node is not installed (pinned expected skip)")
elif not FIXTURE.exists() or not WORKS.exists():
    for r in ALL_ROWS:
        skip(r, "the composer's own two fixtures are not in the tree")
else:
    TMP = Path(tempfile.mkdtemp(prefix="synth_peak_"))
    DRIVER_PATH = TMP / "peak-driver.js"
    DRIVER_PATH.write_text(DRIVER.replace("STEPS_JS", str(STEPS)), encoding="utf-8")
    env = dict(os.environ, PAIRS=json.dumps(PAIRS))
    proc = subprocess.run(["node", str(DRIVER_PATH), str(MODULE), str(FIXTURE), str(WORKS)],
                          capture_output=True, text=True, env=env, timeout=600)
    if proc.returncode != 0:
        for r in ALL_ROWS:
            check(r, False, "the driver did not run: " + (proc.stderr or "").strip()[-300:])
        data = None
    else:
        data = json.loads(proc.stdout.strip().splitlines()[-1])

    if data is not None:
        MANIFESTS = json.loads(FIXTURE.read_text(encoding="utf-8"))["consts"]["manifests"]

        # ------------------------------------------------------------------ 1 · the placement
        worst = None
        walked = False
        outside = []
        threw = [p for p in data["plans"] if p.get("threw")]
        for p in data["plans"]:
            if p.get("threw") or p.get("declined"):
                continue
            track = ((p.get("camera") or {}).get("track")) or []
            if len(track) != 4:
                continue
            dur = float(p["duration"]) / 1000.0
            got = peak_of(p["cues"], dur, MANIFESTS)
            a1, a2 = float(track[1]["at"]), float(track[2]["at"])
            if got["flat"]:
                # No instant of this plan moves faster than another, so the shelf names no peak and
                # the composition leaves the excursion exactly where its own measurement put it.
                continue
            walked = True
            length = a2 - a1
            want1 = got["share"] * (dur - length)
            # Two steps of the walk over the room the excursion leaves over, plus the four decimal
            # places a score is written at: the module's own sum and this file's are two floating
            # walks over the same curve and may part by a grid point at a plateau's edge.
            tol = 2 * (dur - length) / STEPS + 2e-4
            gap = max(abs(a1 - want1), abs(a2 - (want1 + length)))
            if not (a1 <= got["at"] <= a2):
                outside.append((p["key"], round(a1, 3), round(got["at"], 3), round(a2, 3)))
            if worst is None or gap > worst[0]:
                worst = (gap, p["key"], a1, want1, got["at"], dur, got["top"], tol)
        check(ROW_PLACED,
              bool(walked) and not threw and not outside and worst is not None
              and worst[0] <= worst[7],
              ("no pair composed a plan with a four-point camera track and a peak to name"
               if worst is None else
               (f"the widest a middle point stood from where the peak puts it was {worst[0]:.4f} s "
                f"on {worst[1]} — the outbound pose stands at {worst[2]:.4f} s against the "
                f"{worst[3]:.4f} s the peak asks for, the peak of the summed normalised velocity "
                f"({worst[6]:.3f} per unit of passage time) standing at {worst[4]:.4f} s of a "
                f"{worst[5]:.3f} s passage; the walk's own tolerance is {worst[7]:.4f} s"
                + (f"; pairs whose peak fell outside their own excursion: {outside[:3]}"
                   if outside else "")
                + (f"; plans that threw: {[t['key'] for t in threw][:2]}" if threw else ""))))

        # ------------------------------------------------------------------ 2 · the arithmetic
        arith = data.get("arithmetic") or {}
        if arith.get("absent") or not arith:
            for r in (ROW_CURVES, ROW_WINDOW, ROW_SPAN, ROW_STILL):
                check(r, False,
                      "the module hands out no peak arithmetic beside its entry, so the claim "
                      "cannot be put to it over the span of numbers it takes")
        else:
            D = float(arith["D"])
            c = arith["curves"]

            def near(a, b, eps=1e-6):
                return abs(float(a) - float(b)) <= eps

            # `out` rises fastest at the open (2(1−x) at x = 0), `in` at the close (2x at x = 1),
            # `smooth` at the middle (6x(1−x) = 1.5 at x = ½), and `linear` moves at one for the
            # whole passage and therefore never crests. The walk stands strictly inside the
            # passage, so the two that crest at an end are read one step in from it — 2(1 − 1/N)
            # rather than 2, at the first and last interior step — and the two the walk reads whole
            # are exact.
            edge = 2 * (1 - 1.0 / STEPS)
            curve_ok = (
                near(c["out"]["top"], edge) and near(c["out"]["at"], D / STEPS)
                and not c["out"]["flat"]
                and near(c["in"]["top"], edge) and near(c["in"]["at"], D * (STEPS - 1) / STEPS)
                and not c["in"]["flat"]
                and near(c["smooth"]["top"], 1.5) and near(c["smooth"]["at"], D / 2)
                and not c["smooth"]["flat"]
                and near(c["linear"]["top"], 1.0) and c["linear"]["flat"]
                and near(c["linear"]["at"], D / 2))
            check(ROW_CURVES, curve_ok,
                  f"out crests at {c['out']['top']:.4f} at {c['out']['at']:.4f} s ({edge:.4f} at "
                  f"{D / STEPS:.4f} asked); in at {c['in']['top']:.4f} at {c['in']['at']:.4f} s "
                  f"({edge:.4f} at {D * (STEPS - 1) / STEPS:.4f} asked); smooth at "
                  f"{c['smooth']['top']:.4f} at {c['smooth']['at']:.4f} s (1.5 at {D / 2:.1f} "
                  f"asked); linear at {c['linear']['top']:.4f}, flat={c['linear']['flat']} "
                  f"(1, flat asked)")

            w = arith["windows"]
            window_ok = (near(w["whole"]["top"], 1.0) and near(w["half"]["top"], 2.0)
                         and near(w["quarter"]["top"], 4.0)
                         and w["quarter"]["at"] >= D / 4 - 1e-9
                         and w["quarter"]["at"] <= D / 2 + 1e-9)
            check(ROW_WINDOW, window_ok,
                  f"the same door reads {w['whole']['top']:.4f} over the whole passage, "
                  f"{w['half']['top']:.4f} over half of it and {w['quarter']['top']:.4f} over a "
                  f"quarter (1, 2 and 4 asked), and the quarter's peak stands at "
                  f"{w['quarter']['at']:.4f} s, inside its own window")

            sw = arith["sweep"]
            check(ROW_SPAN, not sw["badTop"] and not sw["outside"],
                  f"the largest sum any published handle range, node kind, curve and window shape "
                  f"produced was {sw['worstTop']:.4f} per unit of passage time, every one of them "
                  f"finite; readings that were not finite: {sw['badTop']}; peaks that landed "
                  f"outside the passage: {sw['outside']}")

            st = arith["still"]
            dr = arith["doorOnly"]
            check(ROW_STILL,
                  near(st["top"], 0.0) and st["flat"] and near(st["at"], D / 2)
                  and near(dr["top"], 0.0) and dr["flat"] and near(dr["at"], D / 2),
                  f"a cue driving one fixed reading sums to {st['top']:.4f} and its peak stands at "
                  f"{st['at']:.4f} s of a {D:.1f} s passage (0 and {D / 2:.1f} asked), flat="
                  f"{st['flat']}; a cue driving nothing but its own door reads {dr['top']:.4f} at "
                  f"{dr['at']:.4f} s, flat={dr['flat']}, because the swap is not in the sum that "
                  f"places it")

        # ------------------------------------------------------------------ 3 · what must not move
        bad_len, bad_inside = [], []
        for p in data["plans"]:
            if p.get("threw") or p.get("declined"):
                continue
            track = ((p.get("camera") or {}).get("track")) or []
            if len(track) != 4:
                continue
            dur = float(p["duration"]) / 1000.0
            a1, a2 = float(track[1]["at"]), float(track[2]["at"])
            travel = [c for c in p["cues"] if c["id"] == "travel"]
            want = ((float(travel[0]["window"][1]) - float(travel[0]["window"][0]))
                    if travel else dur / 2.0)
            if abs((a2 - a1) - want) > 2e-4:
                bad_len.append((p["key"], round(a2 - a1, 4), round(want, 4)))
            if not (0 <= a1 < a2 <= dur + 1e-9):
                bad_inside.append((p["key"], a1, a2, dur))
        check(ROW_LENGTH, not bad_len,
              "the excursion must span the travelling cue's own window, or half the passage where "
              f"the plan travels on no cue; pairs where it did not: {bad_len[:3]}")
        check(ROW_INSIDE, not bad_inside,
              "both middle points must stand inside the passage with the outbound pose before the "
              f"inbound one; pairs where they did not: {bad_inside[:3]}")

    import shutil  # noqa: E402
    shutil.rmtree(TMP, ignore_errors=True)

    # ------------------------------------------------------------------ 4 · the host's own curves
    layer = LAYER.read_text(encoding="utf-8") if LAYER.exists() else ""
    host_curves = {
        "linear": "linear: function (u) { return u; }",
        "smooth": "smooth: function (u) { return u * u * (3 - 2 * u); }",
        "in": '"in": function (u) { return u * u; }',
        "out": "out: function (u) { return 1 - (1 - u) * (1 - u); }",
    }
    drifted = sorted(n for n, text in host_curves.items() if text not in layer)
    check(ROW_HOST, not drifted,
          "the derivatives written out at the head of this file are the derivatives of these four "
          f"shapes and of no others; shapes the drawing host no longer draws this way: {drifted}")

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
