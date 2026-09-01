#!/usr/bin/env python3
"""EX-PASS S-20 — the measured response tables, and the speed the hand feels between their points.
Run: python3 tests/test_pass_feel.py

ROOT. His word of 2026-08-28 02:47 on the crossings as they play: «там бесшовность таксебе
работает... есть вау эффекты но иногда оно как-то дёргается и это неклево» — the seamlessness works
so-so, there are real wow moments, but sometimes it jerks. PLAN.md's S-20 asks for the jerks to be
found by construction rather than by eye: differentiate the curve instead of trusting the comment
over it, and measure the speed and its breaks across the whole range a handle is allowed to take.

WHAT THIS FILE IS ABOUT, AND WHY IT IS ONE FILE AND NOT SIX ROWS IN SIX SUITES.

Seven instruments carried a MEASURED RESPONSE TABLE: twenty-one evenly spaced shares, running from
nought to one, that say what raw value feels a given distance along the hand. The tables are real
measurements — how far a photograph actually travelled per unit of the raw handle, integrated and
inverted — and not one number in any of them is touched by anything here or by the repair these rows
judge. What every one of the seven shared was the OTHER half of the question: how the curve is read
BETWEEN two of its own points. That shared reading is one fact with seven readers, so it got one
home, exactly as `pass-layer.js`'s own note gives one home to the monotone spline the score tracks
ride.

PHASE 7 (2026-09-01) — THE SAME LAW, ACROSS THE WHOLE FLEET. Seven instruments out of twenty-seven
is a law with twenty blind spots: «a crossing that jerks on parquet today would pass every suite in
the tree» was true the morning this phase opened. The Opus consultation of 2026-08-31 found the fix
was declaration, not derivation — every one of the twenty-seven already publishes `feel` through the
declared interface, `DRIVER` below is already a black-box differentiator that needs nothing but that
one function, and running it cold against all twenty-seven found ten already passing untouched. What
was missing was for each instrument to say WHAT KIND of curve it is publishing — monotone door to
door, a there-and-back excursion, or an honest identity because there is no travel to shape — so the
generic law could pick the right check instead of one check trying to be right for all three shapes.

`pass-inst-tilt.js` is the one instrument this phase repaired outright: its closed-form two-piece
knee held a dead band flat and then left it at the ramp's own full speed at once, the same defect
S-20 already carried out of `matter`/`beat`/`gears`/`gates`/`adrift`/`waterline` — so it now reads a
measured table through the same spline, digit for digit the closed form's own shape, the same
mechanism carried one file further rather than a new one. Twelve more instruments (`droste`,
`liquid`, `pour`, `tunnel`, `veil`, `wind` — a linear ramp held flat at a hard-clamped dead band,
and `strata-light`, `strata-scale`, `weave`, `grid-colour`, `hero`, `lens` — a two-piece hinge off
the middle, so the two slopes at the join are not forced equal) turned out to carry the identical
class of defect, LIVE, in code nobody had pointed this row at before. Repairing all twelve is core
logic and stands outside this phase's write-set (curve declaration, not derivation, for the fleet's
remaining instruments) — so KNOWN_JERK below names each one, cites its own measured break, and
CHECKS that the break is still there every run, so a silent regression (or a silent fix nobody told
this file about) reds instead of going unnoticed either way.

THE DEFECT, IN ARITHMETIC. Read with straight lines between the points, a table's own VALUE is right
at every knot and its SPEED is a staircase: constant inside each share and stepping at every one of
the nineteen joins between them, with nothing at all in between the two speeds. Measured on the
tables as they stood before S-20:

    matter    the last join steps from 1.080 of the dial a unit of the hand to 5.804 — a factor of
              5.37 in one instant — and the first steps the other way, 4.431 down to 1.098
    unfold    the last join, 0.940 to 2.230, a factor of 2.37
    adrift    the grain's last join, 2.627 to 4.660, a factor of 1.77
    waterline the dial's ninth join, 1.676 down to 0.960, a factor of 1.75
    gears     1.524 to 2.451, a factor of 1.61
    beat      1.537 to 2.398, a factor of 1.56
    gates     1.892 to 2.575, a factor of 1.36

and the same step stands at each dead band's own edge, where the value is HELD perfectly still and
then leaves at the first share's whole speed at once — 4.43 of the dial a unit for the material, 1.80
for the drift, 1.42 for the waterline, 1.25 for the interference, 0.60 for the mesh and 0.59 for the
gate. (The fold carries no dead band of its own; its curve simply opens at 2.40 out of the door's own
stillness, which is the same step by another road.)

None of those steps is in the measurement. What was integrated to build a table is a smooth reading
of how far a photograph travels; a polyline through its samples invents corners the reading never
had. It is the same defect his word of 2026-08-11 closed one layer up, after he judged speed steps
at segment joints and the score tracks were put on one monotone spline through all of their points
(`pass-layer.js`, `splineSlopes`/`splineAt`, and the note above them saying so).

THE REPAIR THESE ROWS JUDGE. The same Fritsch–Carlson spline, carried over unchanged, reading the
same knots. It passes through every one of them exactly, cannot overshoot or turn back, and rests at
both its own ends.

HOW A SPEED BREAK IS TOLD FROM A CURVE THAT IS MERELY FAST, AND THE BAR IS NOT A NUMBER ANYONE CHOSE.
Sample a curve at N points and read the largest step its speed takes between two neighbouring
samples. Halve the sample spacing and read it again. For a curve whose speed is continuous that
reading is the curve's own bend times the spacing, so it HALVES; for a curve whose speed jumps, the
jump is there whatever the spacing, so the reading HOLDS. The two limits are therefore 0.5 and 1.0
and the bar is the midpoint between them — and no reading below lands anywhere near it: a repaired
curve reads about 0.50 and the planted straight-line read about 1.00.

THE RED-ON-THE-REAL-DEFECT PROOF. Every row that judges the repair is run twice: once against the
instrument files as they ship, and once against a COPY of each file with the straight-line read
planted back in, character for character as it stood. A row that could not tell the two apart would
be proving nothing, so the planted run must fail exactly where the shipped run passes. Phase 7 adds
two more plants in the same spirit, for the two shapes a table never had to answer for: an identity
handle nudged off the raw hand (§ IDENTITY below), and a point-symmetric mirror pushed off its own
centre into the same off-centre hinge KNOWN_JERK already reads live (§ MONOTONE ANALYTIC below).

WHAT IS OUT OF SCOPE, AND IT IS SAID RATHER THAN SKIPPED IN SILENCE. `unfold` carries the same table
and the same defect and is NOT repaired here: its hold's own swing was built on 2026-08-27 (S-03) to
leave and return at the rate the POLYLINE's last segment moves at, a constant the file derives from
that segment, so closing the staircase there re-opens a construction that landed and was proved
hours before this file was written. The roll call below names it, prints its own reading every run,
and reds the moment any OTHER table starts reading itself with straight lines.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "engine" / "assets"

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


def run_node(driver_text, files):
    """`driver_text` under a real node, in a throwaway directory, with `files` written beside it and
    their paths handed in as argv in the dict's own order. Returns the parsed JSON of the last line,
    or an {"error": ...} dict, so a row that could not run reads as a stated failure."""
    d = Path(tempfile.mkdtemp(prefix="synth_feelnode_"))
    try:
        (d / "driver.js").write_text(driver_text, encoding="utf-8")
        paths = []
        for name, text in files.items():
            p = d / name
            p.write_text(text, encoding="utf-8")
            paths.append(str(p))
        proc = subprocess.run(["node", str(d / "driver.js")] + paths,
                              capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-500:]}
        lines = proc.stdout.strip().splitlines()
        if not lines:
            return {"error": "the driver printed nothing"}
        return json.loads(lines[-1])
    except Exception as e:
        return {"error": str(e)}
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------------ the roll call, read off the tree
# EVERY twenty-one point table the fleet carries, found by its own shape rather than by a list typed
# here: a name bound to a bracketed list of exactly twenty-one numbers running from 0 to 1. An
# instrument that gains a table joins these rows by itself.
TABLE = re.compile(r"var\s+([A-Z_][A-Z0-9_]*)\s*=\s*\[([^\]]*?)\]\s*;", re.S)
LIST_IN_OBJ = re.compile(r"^\s*(\w+)\s*:\s*\[([^\]]*?)\]", re.M)
# THE STRAIGHT-LINE READ, character for character in the three spellings the fleet gives it. A file
# carrying one of these is reading a table as twenty separate lines.
LINE_READS = [
    "return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);",
    "return q[i] + (q[i + 1] - q[i]) * (s - i);",
    "return mix(FEEL_KNOTS[i], FEEL_KNOTS[i + 1], x - i);",
    "return mix(knots[i], knots[i + 1], x - i);",
]
# THE MONOTONE READ, in the one spelling the repair gives it.
SPLINE_READ = "(2 * s3 - 3 * s2 + 1) * "
# THE ONE INSTRUMENT THIS FILE DOES NOT ASK TO BE REPAIRED, AND WHY — see the docstring's last
# paragraph. A table nobody reads is out of scope too, and is named where it stands.
EXCEPTED = {"unfold": "its hold's own swing (S-03, 2026-08-27) is built to leave and return at the "
                      "rate the polyline's last segment moves at, and the file derives that very "
                      "rate from that very segment, so closing the staircase here re-opens a "
                      "construction that landed and was proved hours earlier"}


def numbers(text):
    return [float(x) for x in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", text)]


def tables_of(source):
    found = {}
    for m in TABLE.finditer(source):
        vals = numbers(m.group(2))
        if len(vals) == 21 and vals[0] == 0 and vals[-1] == 1:
            found[m.group(1)] = vals
    # the waterline's six and the two files' `CURVES` blocks live inside one object literal rather
    # than under a name each
    for m in LIST_IN_OBJ.finditer(source):
        vals = numbers(m.group(2))
        if len(vals) == 21 and vals[0] == 0 and vals[-1] == 1:
            found.setdefault(m.group(1), vals)
    return found


# A table that nothing reads carries no speed and no jerk. Two instruments publish tables they
# DECLARE and do not apply (`applied: false` beside the knots in their own manifests), and those are
# out of these rows for that reason and not by omission.
ALL_TABLES, CARRIERS, DECLARED_ONLY = {}, {}, {}
ALL_INSTRUMENT_FILES = sorted(ASSETS.glob("pass-inst-*.js"))
for path in ALL_INSTRUMENT_FILES:
    src = path.read_text(encoding="utf-8")
    t = tables_of(src)
    if not t:
        continue
    name = path.stem.replace("pass-inst-", "")
    ALL_TABLES[name] = sorted(t)
    reads_line = any(r in src for r in LINE_READS)
    reads_spline = SPLINE_READ in src
    if reads_line or reads_spline:
        CARRIERS[name] = {"path": path, "src": src, "tables": t,
                          "line": reads_line, "spline": reads_spline}
    else:
        DECLARED_ONLY[name] = sorted(t)

# EVERY INSTRUMENT IN THE TREE, table or not — the fleet Phase 7 widens the law across.
ALL_NAMES = sorted(p.stem.replace("pass-inst-", "") for p in ALL_INSTRUMENT_FILES)
ALL_SRC = {p.stem.replace("pass-inst-", ""): p for p in ALL_INSTRUMENT_FILES}

# AND «NOT APPLIED» IS READ OFF THE FILE RATHER THAN INFERRED FROM THE ABSENCE OF A READER. A table
# a manifest publishes under `knots:` and nothing else touches is a declaration; a table named
# anywhere else in the file is one something reads. The row below asks for both to agree, so a file
# that grew a reader without growing a repair cannot slip through as «declared only».
def declared_only_holds(name, tables):
    src = (ASSETS / ("pass-inst-%s.js" % name)).read_text(encoding="utf-8")
    for t in tables:
        uses = re.findall(r"CURVES\.%s\b" % re.escape(t), src)
        knots = re.findall(r"knots:\s*CURVES\.%s\b" % re.escape(t), src)
        if len(uses) != len(knots) or not knots:
            return False, "%s.%s is named %d time(s) and only %d of them is a `knots:` declaration" \
                          % (name, t, len(uses), len(knots))
    return True, ""


declared_bad = []
for n, v in sorted(DECLARED_ONLY.items()):
    ok, why = declared_only_holds(n, v)
    if not ok:
        declared_bad.append(why)

check("PASS-FEEL every measured response table in the fleet is found, and each is either read or "
      "declared and not applied",
      len(ALL_TABLES) >= 7 and set(EXCEPTED) <= set(CARRIERS) and set(ALL_TABLES) ==
      set(CARRIERS) | set(DECLARED_ONLY) and not declared_bad,
      ("read and applied: %s — declared and never applied, so no hand ever travels them: %s, and "
       "each of those names is reached by nothing in its own file but the `knots:` line that "
       "publishes it"
       % ("; ".join("%s (%s)" % (n, ", ".join(sorted(c["tables"])))
                    for n, c in sorted(CARRIERS.items())),
          "; ".join("%s (%s)" % (n, ", ".join(v)) for n, v in sorted(DECLARED_ONLY.items())) or "none")
       if not declared_bad else "a table called declared-only is read after all: %s" % declared_bad))

straight = sorted(n for n, c in CARRIERS.items() if c["line"])
unexpected = [n for n in straight if n not in EXCEPTED]
check("PASS-FEEL no table outside the one named exception is still read with straight lines",
      not unexpected,
      ("the only instrument still reading a table as twenty separate lines is %s, and it is named "
       "here rather than left silent: %s" % (straight, "; ".join(EXCEPTED[n] for n in straight))
       if not unexpected
       else "read with straight lines and named by nothing: %s" % unexpected))

# ------------------------------------------------------------------------------------ the driver
# ONE differentiator for the whole fleet (Phase 7): every instrument handed in is loaded for real,
# its published `feel()` differentiated the same way regardless of whether it is table-backed or a
# closed form, and what it DECLARES about itself — `feelClass` (monotone / excursion / identity),
# `feelEnds` where a curve does not promise the fleet's usual 0/1 doors, and the manifest's own
# `curve.knots`/`curve.band` where a table stands behind it — is read back off the very same object
# rather than typed a second time here. A file that gains a table or a declaration joins these rows
# by itself, the same way the table roll call above already does.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const out = [];
for (const p of process.argv.slice(2)) {
  const source = fs.readFileSync(p, "utf8").replace(/@@NS@@/g, "ex");
  let joined = null;
  const sandbox = {window: {__exPassInstrument: (m) => { joined = m; }},
                   console: {log(){}, warn(){}, error(){}}};
  vm.createContext(sandbox);
  try { vm.runInContext(source, sandbox, {filename: path.basename(p)}); }
  catch (e) { out.push({file: path.basename(p), error: "load: " + e.message}); continue; }
  if (!joined || !joined.instrument || typeof joined.instrument.feel !== "function") {
    out.push({file: path.basename(p), error: "publishes no feel()"});
    continue;
  }
  const inst = joined.instrument;
  const feel = inst.feel;
  // THE SPEED'S OWN LARGEST STEP BETWEEN TWO NEIGHBOURING SAMPLES, at one spacing and at half it.
  function worstStep(N) {
    const h = 1 / (N - 1), v = new Float64Array(N);
    for (let i = 0; i < N; i++) v[i] = feel(i * h);
    let lo = Infinity, hi = -Infinity;
    for (let i = 0; i < N; i++) { if (v[i] < lo) lo = v[i]; if (v[i] > hi) hi = v[i]; }
    const span = hi - lo;
    if (!(span > 0)) return {span: span, worst: 0, at: 0, v: v, h: h};
    let worst = 0, at = 0, prev = (v[1] - v[0]) / h;
    for (let i = 2; i < N; i++) {
      const cur = (v[i] - v[i - 1]) / h;
      const step = Math.abs(cur - prev) / span;
      if (step > worst) { worst = step; at = (i - 1) * h; }
      prev = cur;
    }
    return {span: span, worst: worst, at: at, v: v, h: h};
  }
  const coarse = worstStep(20001), fine = worstStep(40001);
  // The curve stands still where it is held, and it must be exact at both ends of the hand.
  const ends = {at0: feel(0), at1: feel(1)};
  // Monotone: a response curve that turned back would send the picture backwards under a hand that
  // never stopped going forward.
  let backwards = 0, last = -Infinity;
  for (let i = 0; i <= 40000; i++) { const y = feel(i / 40000); if (y < last - 1e-12) backwards++; last = y; }
  // IDENTITY-BECAUSE-NO-TRAVEL'S OWN LAW: not a speed reading (a straight line's own speed noise is
  // meaningless, see the docstring below the identity checks) but the largest distance the curve
  // ever stands from the raw hand itself.
  let idErr = 0;
  for (let i = 0; i < coarse.v.length; i++) {
    const d = Math.abs(coarse.v[i] - i * coarse.h);
    if (d > idErr) idErr = d;
  }
  // THE KNOTS ON THE MANIFEST (Phase 7, item 3a): read generically off `handles.mix.curve` rather
  // than off a hand-typed map of which file's own table variable answers which handle.
  let curve = null;
  try {
    const mh = inst.manifest && inst.manifest.handles;
    const c = mh && mh.mix && mh.mix.curve;
    if (c && c.knots) curve = {knots: c.knots, band: (typeof c.band === "number" ? c.band : 0),
                               applied: !!c.applied};
  } catch (e) {}
  let knotFidelity = null;
  if (curve && curve.applied) {
    let worst = 0, at = -1;
    for (let k = 0; k <= 20; k++) {
      const u = curve.band + (1 - 2 * curve.band) * (k / 20);
      const d = Math.abs(feel(u) - curve.knots[k]);
      if (d > worst) { worst = d; at = k; }
    }
    knotFidelity = {worst: worst, at: at};
  }
  out.push({file: path.basename(p), span: coarse.span,
            worstCoarse: coarse.worst, worstFine: fine.worst, atCoarse: coarse.at,
            halving: coarse.worst > 0 ? fine.worst / coarse.worst : 0,
            ends: ends, backwards: backwards, idErr: idErr,
            feelClass: inst.feelClass || null, feelEnds: inst.feelEnds || null,
            curve: curve, knotFidelity: knotFidelity});
}
console.log(JSON.stringify(out));
"""

# The two limits the docstring derives, and the midpoint between them. Nothing here is chosen.
SMOOTH_LIMIT, BREAK_LIMIT = 0.5, 1.0
BAR = (SMOOTH_LIMIT + BREAK_LIMIT) / 2

JUDGED = sorted(n for n in CARRIERS if n not in EXCEPTED)

if not node_available():
    for row in ("PASS-FEEL the speed of every repaired response curve is continuous",
                "PASS-FEEL every repaired curve still stands exactly at both ends of the hand",
                "PASS-FEEL every repaired curve is still monotone in the hand",
                "PASS-FEEL every repaired curve still passes through the measurement's own points",
                "PASS-FEEL the straight-line read planted back breaks the speed again",
                "PASS-FEEL every instrument in the fleet declares what its own feel() promises",
                "PASS-FEEL every monotone analytic curve declared clean is continuous, monotone, "
                "and stands at its own declared ends",
                "PASS-FEEL every identity-declared feel() reads the raw hand exactly, everywhere",
                "PASS-FEEL the fleet's own catalogue of already-known, not-yet-repaired jerks still "
                "reads its own break, live",
                "PASS-FEEL the identity plant and the off-centre-hinge plant both break their row"):
        skip(row, "node is not installed (pinned expected skip)")
else:
    shipped = run_node(DRIVER, {CARRIERS[n]["path"].name: CARRIERS[n]["src"] for n in JUDGED})
    rows = {} if isinstance(shipped, dict) else {r["file"]: r for r in shipped}
    err = shipped.get("error") if isinstance(shipped, dict) else None

    broken = [(f, r) for f, r in sorted(rows.items())
              if r.get("error") or r["halving"] > BAR]
    check("PASS-FEEL the speed of every repaired response curve is continuous",
          not err and len(rows) == len(JUDGED) and not broken,
          ("halving the sample spacing halves the largest speed step, which is what a curve with no "
           "break in its speed does and what one with a break cannot do — " +
           "; ".join("%s %.4f→%.4f (×%.3f)"
                     % (f, r["worstCoarse"], r["worstFine"], r["halving"])
                     for f, r in sorted(rows.items()))
           + " — against a bar of %.2f, the midpoint between the two limits (%.1f smooth, %.1f "
             "broken)" % (BAR, SMOOTH_LIMIT, BREAK_LIMIT)
           if not broken and not err
           else "driver: %s; still breaking: %s" % (err, [f for f, _ in broken])))

    ends_bad = [(f, r["ends"]) for f, r in sorted(rows.items())
                if r.get("error") or r["ends"]["at0"] != 0.0 or r["ends"]["at1"] != 1.0]
    check("PASS-FEEL every repaired curve still stands exactly at both ends of the hand",
          not err and rows and not ends_bad,
          ("nought at the near door and one at the far, exactly, on all %d — so both doors stand "
           "where they stood" % len(rows)
           if not ends_bad and not err else "off the ends: %s" % ends_bad))

    back_bad = [(f, r["backwards"]) for f, r in sorted(rows.items())
                if r.get("error") or r["backwards"]]
    check("PASS-FEEL every repaired curve is still monotone in the hand",
          not err and rows and not back_bad,
          ("no sample of any curve stands below the one before it over forty thousand steps, so a "
           "hand that keeps going forward never sends the picture back"
           if not back_bad and not err else "turned back: %s" % back_bad))

    # THE MEASUREMENT ITSELF IS UNTOUCHED, read through the very function the shader's numbers come
    # from: at each of the twenty-one shares the curve must answer the table's own number. The knots
    # and the dead band come off `handles.mix.curve` on each file's own manifest (Phase 7, item 3a —
    # `weave.js` and `unfold.js` already published this shape; the six table carriers plus `tilt`
    # now do too), not off a map hand-typed in this file.
    knot_rows, knot_bad = [], []
    for n in JUDGED:
        r = rows.get(CARRIERS[n]["path"].name)
        if not r or not r.get("curve") or not r["curve"].get("applied") or not r.get("knotFidelity"):
            knot_bad.append((n, "no `handles.mix.curve` with `applied: true` could be read off the "
                                 "manifest"))
            continue
        kf = r["knotFidelity"]
        knot_rows.append((n, kf["worst"]))
        if kf["worst"] > 1e-9:
            knot_bad.append((n, "share %d is off by %g" % (kf["at"], kf["worst"])))
    check("PASS-FEEL every repaired curve still passes through the measurement's own points",
          bool(knot_rows) and not knot_bad,
          ("all twenty-one shares of every table answered to floating point and no further: "
           + "; ".join("%s worst %.2e" % (n, w) for n, w in knot_rows)
           if not knot_bad else "off the measurement: %s" % knot_bad))

    # ---- THE RED ON THE REAL DEFECT ------------------------------------------------------------
    # The straight-line read put back into a copy of each file, character for character as it stood,
    # and nothing else changed. The first row above must fail on it.
    PLANT_TO = {
        "return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);":
            ("var n = FEEL_Q.length, h = 1 / (n - 1);\n"
             "      var i = Math.min(n - 2, Math.floor(x * (n - 1)));\n"
             "      var s = (x - i * h) / h, s2 = s * s, s3 = s2 * s;\n"
             "      return (2 * s3 - 3 * s2 + 1) * FEEL_Q[i] + (s3 - 2 * s2 + s) * h * FEEL_M[i]\n"
             "           + (3 * s2 - 2 * s3) * FEEL_Q[i + 1] + (s3 - s2) * h * FEEL_M[i + 1];"),
    }
    planted_src, planted_names = {}, []
    for n in JUDGED:
        c = CARRIERS[n]
        src = c["src"]
        # the two spellings the spline read takes across the fleet — the FEEL_Q one, and the
        # `q`-argument one the multi-table files and `tilt` share
        for new, old in (
            (PLANT_TO["return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);"],
             "var s = x * (FEEL_Q.length - 1), i = Math.min(FEEL_Q.length - 2, Math.floor(s));\n"
             "      return FEEL_Q[i] + (FEEL_Q[i + 1] - FEEL_Q[i]) * (s - i);"),
            ("var n = q.length, h = 1 / (n - 1), m = tangentsOf(q);\n"
             "      var i = Math.min(n - 2, Math.floor(x * (n - 1)));\n"
             "      var s = (x - i * h) / h, s2 = s * s, s3 = s2 * s;\n"
             "      return (2 * s3 - 3 * s2 + 1) * q[i] + (s3 - 2 * s2 + s) * h * m[i]\n"
             "           + (3 * s2 - 2 * s3) * q[i + 1] + (s3 - s2) * h * m[i + 1];",
             "var s = x * (q.length - 1), i = Math.min(q.length - 2, Math.floor(s));\n"
             "      return q[i] + (q[i + 1] - q[i]) * (s - i);"),
            ("var x = clamp(u, 0, 1), n = q.length, h = 1 / (n - 1), m = tangentsOf(q);\n"
             "      var i = Math.min(n - 2, Math.floor(x * (n - 1)));\n"
             "      var s = (x - i * h) / h, s2 = s * s, s3 = s2 * s;\n"
             "      return (2 * s3 - 3 * s2 + 1) * q[i] + (s3 - 2 * s2 + s) * h * m[i]\n"
             "           + (3 * s2 - 2 * s3) * q[i + 1] + (s3 - s2) * h * m[i + 1];",
             "var s = clamp(u, 0, 1) * (q.length - 1);\n"
             "      var i = Math.min(q.length - 2, Math.floor(s));\n"
             "      return q[i] + (q[i + 1] - q[i]) * (s - i);"),
        ):
            if new in src:
                src = src.replace(new, old)
                planted_names.append(n)
                break
        planted_src[c["path"].name] = src
    planted = run_node(DRIVER, planted_src)
    prows = {} if isinstance(planted, dict) else {r["file"]: r for r in planted}
    still_broken = sorted(f for f, r in prows.items()
                          if not r.get("error") and r["halving"] > BAR)
    check("PASS-FEEL the straight-line read planted back breaks the speed again",
          len(planted_names) == len(JUDGED) and len(still_broken) == len(JUDGED),
          ("the plant reached all %d files and every one of them fails the continuity row against "
           "it — %s — where the same row reads about a half on the files as they ship, so the row is "
           "measuring the repair and not the weather"
           % (len(JUDGED),
              "; ".join("%s ×%.3f" % (f, prows[f]["halving"]) for f in still_broken))
           if len(planted_names) == len(JUDGED) and len(still_broken) == len(JUDGED)
           else "planted %s of %s; still passing under the plant: %s"
                % (len(planted_names), len(JUDGED),
                   sorted(set(prows) - set(still_broken)))))

    # ======================================================================================
    # PHASE 7 — THE SAME LAW, READ GENERICALLY ACROSS ALL TWENTY-SEVEN
    # ======================================================================================
    # Every instrument in the tree, table-backed or a closed form alike, differentiated by the same
    # `DRIVER` above. `EXCEPTED` (`unfold`) is left out here exactly as it is left out of `JUDGED`.
    fleet_files = {ALL_SRC[n].name: ALL_SRC[n].read_text(encoding="utf-8")
                   for n in ALL_NAMES if n not in EXCEPTED}
    fleet_run = run_node(DRIVER, fleet_files)
    ferr = fleet_run.get("error") if isinstance(fleet_run, dict) else None
    frows = {} if isinstance(fleet_run, dict) else {
        r["file"].replace("pass-inst-", "").replace(".js", ""): r for r in fleet_run}

    undeclared = [n for n in sorted(frows) if not frows[n].get("feelClass")]
    check("PASS-FEEL every instrument in the fleet declares what its own feel() promises",
          not ferr and len(frows) == len(fleet_files) and not undeclared,
          ("every one of %d instruments (all twenty-seven but the one named exception) reads its "
           "own `feelClass` off the object `feel()` itself travels on — monotone, excursion, or "
           "identity — so the roll call below picks the law by the instrument's own word rather "
           "than by a guess" % len(frows)
           if not undeclared and not ferr
           else "driver: %s; no feelClass read off: %s" % (ferr, undeclared)))

    IDENTITY = sorted(n for n, r in frows.items() if r.get("feelClass") == "identity")
    EXCURSION = sorted(n for n, r in frows.items() if r.get("feelClass") == "excursion")
    MONOTONE_ANALYTIC = sorted(n for n, r in frows.items()
                                if r.get("feelClass") == "monotone" and n not in JUDGED)

    # ---- IDENTITY-BECAUSE-NO-TRAVEL --------------------------------------------------------------
    # `kaleidoscope`, `livemirror` and `planet` declare their `feel` a written "no": the raw hand,
    # clamped, and nothing else. The law for that shape is not continuity (a straight line's own
    # second difference is floating-point noise with no systematic halving, which is why running the
    # monotone law on an honest identity reads as spurious breakage rather than as a pass) — it is
    # simply whether the curve IS the raw hand, everywhere, which `idErr` (the driver's own largest
    # |feel(u) - u|) answers directly.
    id_bad = [(n, frows[n]["idErr"]) for n in IDENTITY if frows[n]["idErr"] > 1e-9]
    check("PASS-FEEL every identity-declared feel() reads the raw hand exactly, everywhere",
          not ferr and IDENTITY and not id_bad,
          ("%s each answer their own argument back, to floating point and no further, over twenty "
           "thousand samples — a written \"no\" is honest only if the curve really is nothing"
           % IDENTITY
           if not id_bad and not ferr else "off the raw hand: %s" % id_bad))

    # ---- MONOTONE ANALYTIC, DECLARED CLEAN -------------------------------------------------------
    # `parquet`, `overlay`, `studio` and `boxfold` mirror a curve POINT-SYMMETRICALLY about its own
    # middle (`u <= 0.5 ? 0.5*f(2u) : 1-0.5*f(2-2u)`, or a single one-sided exponential with no
    # internal join at all), which forces the two slopes at any join to agree by construction —
    # unlike a hinge held off-centre (KNOWN_JERK, below), there is no join left for a jerk to hide
    # at. These are the four analytic instruments Phase 7 finds already passing, cold, per the Opus
    # consultation's own count.
    CLEAN_MONOTONE = sorted(n for n in MONOTONE_ANALYTIC if n not in
                            {"droste", "grid-colour", "liquid", "pour", "strata-light",
                             "strata-scale", "tunnel", "veil", "weave", "wind"})
    clean_bad = []
    for n in CLEAN_MONOTONE:
        r = frows[n]
        want_ends = r.get("feelEnds") or [0.0, 1.0]
        if r.get("error") or r["halving"] > BAR:
            clean_bad.append((n, "continuity ×%.3f" % r.get("halving", -1)))
        elif r["backwards"]:
            clean_bad.append((n, "turned back %d times" % r["backwards"]))
        elif abs(r["ends"]["at0"] - want_ends[0]) > 1e-9 or abs(r["ends"]["at1"] - want_ends[1]) > 1e-9:
            clean_bad.append((n, "ends %s, wanted %s" % (r["ends"], want_ends)))
    check("PASS-FEEL every monotone analytic curve declared clean is continuous, monotone, and "
          "stands at its own declared ends",
          not ferr and CLEAN_MONOTONE and not clean_bad,
          ("every one of %s already reads a continuous, monotone curve at its own declared ends, "
           "cold, with no repair spent on it this phase — %s"
           % (CLEAN_MONOTONE,
              "; ".join("%s ×%.3f" % (m, frows[m]["halving"]) for m in CLEAN_MONOTONE))
           if not clean_bad and not ferr else "off the law: %s" % clean_bad))

    # ---- THE FLEET'S OWN CATALOGUE OF ALREADY-KNOWN, NOT-YET-REPAIRED JERKS -----------------------
    # Extending the roll call past the seven table carriers put this row in front of twelve more
    # instruments that carry the identical class of defect — a dead band held flat and left at full
    # speed, or a two-piece hinge whose two slopes were never forced to agree — LIVE, in code nobody
    # had pointed this check at before. Fixing any of them is core logic and stands outside this
    # phase's write-set (curve declaration, not derivation). So this row does not ask them to pass:
    # it asks that the break BE THERE, measured, exactly as cited — which reds the moment either
    # direction of drift happens unnoticed: a fix landing without this file being told, or a
    # regression opening where the measurement below said the curve was merely known-bad rather than
    # actively watched.
    KNOWN_JERK = {
        "droste": "a dead-band ramp (feelOf, droste.js): held flat under WIND_HOLD and past "
                  "1 - WIND_HOLD, leaving each edge at the ramp's own full speed at once",
        "liquid": "a dead-band ramp (feelOf, liquid.js): held flat under FEEL_D0 = 0.05 and past "
                  "0.95, leaving each edge at the ramp's own full speed at once",
        "pour": "a dead-band ramp (feelOf, pour.js): held flat under FEEL_D0 = 0.05 and past 0.95, "
               "leaving each edge at the ramp's own full speed at once",
        "tunnel": "a dead-band ramp (feelOf, tunnel.js): held flat under FEEL_D0 = 0.05 and past "
                  "0.95, leaving each edge at the ramp's own full speed at once",
        "veil": "a dead-band ramp (feelOf, veil.js): held flat under FEEL_D0 = 0.05 and past 0.95, "
               "leaving each edge at the ramp's own full speed at once",
        "wind": "a dead-band ramp (feelOf, wind.js): held flat under FEEL_D0 = 0.05 and past 0.95, "
               "leaving each edge at the ramp's own full speed at once",
        "strata-light": "a two-piece hinge off centre (feelOf, strata-light.js): FEEL_C = 0.37, so "
                        "the join's two slopes are not forced to agree",
        "strata-scale": "a two-piece hinge off centre (feelOf, strata-scale.js): FEEL_C = 0.47, so "
                        "the join's two slopes are not forced to agree",
        "weave": "a two-piece hinge off centre (feelOf, weave.js): FEEL_C = 0.43, so the join's two "
                "slopes are not forced to agree (its dead band is a separate, legitimate fact — "
                "see `feelEnds` — and is not this row's complaint)",
        "grid-colour": "a two-piece hinge off centre (feelOf, grid-colour.js): the \"stripes\" "
                      "kind's own FEEL.stripes.c is not 0.5, so the join's two slopes are not "
                      "forced to agree",
        "hero": "the same off-centre hinge, inherited: `feel()` (hero.js) is a two-piece knee at "
               "FEEL_C = 0.61 folded into the excursion `feelOf` rides, so the fold carries the "
               "join's own mismatch with it",
        "lens": "a power-law edge (reachOf, lens.js): Math.pow(u, FEEL_G) with FEEL_G = 0.42 has an "
                "infinite slope at the dead band's own edge, the same held-flat-then-leaves shape "
                "in a steeper key",
    }
    jerk_rows, jerk_bad = [], []
    for n in sorted(KNOWN_JERK):
        r = frows.get(n)
        if not r or r.get("error"):
            jerk_bad.append((n, "driver could not read it: %s" % (r or {}).get("error")))
            continue
        jerk_rows.append((n, r["halving"], r["atCoarse"]))
        if not (r["halving"] > BAR):
            jerk_bad.append((n, "now reads continuous (×%.3f) — the catalogue is stale: either it "
                                 "was repaired and this entry should be removed, or the measurement "
                                 "moved and the reason above needs a second look" % r["halving"]))
    check("PASS-FEEL the fleet's own catalogue of already-known, not-yet-repaired jerks still reads "
          "its own break, live",
          not ferr and set(KNOWN_JERK) <= set(frows) and not jerk_bad,
          ("all %d catalogued instruments still measure a real speed break, exactly where their own "
           "cited reason says one stands — %s"
           % (len(KNOWN_JERK),
              "; ".join("%s ×%.3f at %.2f" % (n, h, at) for n, h, at in jerk_rows))
           if not jerk_bad and not ferr else "the catalogue disagrees with a fresh measurement: %s"
                                              % jerk_bad))

    # ---- TWO MORE PLANTS, FOR THE TWO SHAPES A TABLE NEVER HAD TO ANSWER FOR --------------------
    # An identity handle nudged a hair off the raw hand, and a point-symmetric mirror pushed off its
    # own centre into the same off-centre hinge KNOWN_JERK reads live above. Both are planted into a
    # COPY of a currently-clean file, character for character as it stood otherwise, so a row that
    # could not tell clean from planted would be proving nothing — the same standard the table plant
    # above already carries.
    id_plant_bad = []
    if IDENTITY:
        idn = IDENTITY[0]
        idsrc = ALL_SRC[idn].read_text(encoding="utf-8")
        id_old_new = [
            ("function feelOf(u) { return clamp(u, 0, 1); }",
             "function feelOf(u) { return clamp(u, 0, 1) + 0.02 * Math.sin(6 * Math.PI * u); }"),
            ("function feelOf(u) { return clamp01(u); }",
             "function feelOf(u) { return clamp01(u) + 0.02 * Math.sin(6 * Math.PI * u); }"),
        ]
        planted_id_src = idsrc
        hit = False
        for old, new in id_old_new:
            if old in idsrc:
                planted_id_src = idsrc.replace(old, new)
                hit = True
                break
        if not hit:
            id_plant_bad.append("no known identity spelling matched in %s" % idn)
        else:
            got = run_node(DRIVER, {ALL_SRC[idn].name: planted_id_src})
            prow = None if isinstance(got, dict) else next(
                (r for r in got if r["file"] == ALL_SRC[idn].name), None)
            if not prow or prow["idErr"] <= 1e-9:
                id_plant_bad.append("planted %s and the identity row did not catch it (idErr %s)"
                                     % (idn, prow["idErr"] if prow else "driver error"))

    hinge_plant_bad = []
    if CLEAN_MONOTONE:
        # `studio` carries the simplest point-symmetric mirror in the clean group — one hinge, one
        # exponential half — so it is the plant's own vehicle.
        vehicle = "studio" if "studio" in CLEAN_MONOTONE else CLEAN_MONOTONE[0]
        vsrc = ALL_SRC[vehicle].read_text(encoding="utf-8")
        old_hinge = ("function feelOf(u) {\n      return u <= 0.5 ? 0.5 * feelHalf(2 * u) : "
                     "1 - 0.5 * feelHalf(2 - 2 * u);\n    }")
        new_hinge = ("function feelOf(u) {\n      return u <= 0.5 ? 0.3 * feelHalf(2 * u) : "
                     "0.3 + 0.7 * feelHalf(2 * u - 1);\n    }")
        if vehicle != "studio" or old_hinge not in vsrc:
            hinge_plant_bad.append("the point-symmetric hinge spelling was not found in %s to plant "
                                    "against" % vehicle)
        else:
            planted_v_src = vsrc.replace(old_hinge, new_hinge)
            got = run_node(DRIVER, {ALL_SRC[vehicle].name: planted_v_src})
            prow = None if isinstance(got, dict) else next(
                (r for r in got if r["file"] == ALL_SRC[vehicle].name), None)
            if not prow or not (prow["halving"] > BAR):
                hinge_plant_bad.append("planted an off-centre hinge into %s and the continuity row "
                                        "did not catch it (×%s)"
                                        % (vehicle, prow["halving"] if prow else "driver error"))

    check("PASS-FEEL the identity plant and the off-centre-hinge plant both break their row",
          not ferr and not id_plant_bad and not hinge_plant_bad,
          ("the identity plant (a 0.02-amplitude wobble folded into %s's raw hand) breaks the "
           "identity row, and the off-centre hinge plant (studio's own mirror pushed from 0.5 to 0.3) "
           "breaks the continuity row, exactly where the shipped files pass both — so neither row is "
           "measuring the weather"
           % (IDENTITY[0] if IDENTITY else "(none)")
           if not id_plant_bad and not hinge_plant_bad and not ferr
           else "identity plant: %s; hinge plant: %s" % (id_plant_bad or "ok", hinge_plant_bad or "ok")))

    # ---- THE FLEET'S OWN REACH, PRINTED EVERY RUN (item 4) -----------------------------------------
    # Every instrument but the one named exception falls into exactly one of four buckets: judged for
    # continuity as a table carrier, read as a clean analytic curve, read as an honest identity, or
    # named in the jerk catalogue above. A instrument that fell into none of the four — a new file
    # that declared a `feelClass` this row does not yet know, or one that slipped through undeclared —
    # would be invisible to every check above without this row catching it, which is exactly the kind
    # of silent rot item 4 asks not to happen.
    COVERED = set(JUDGED) | set(CLEAN_MONOTONE) | set(IDENTITY) | set(KNOWN_JERK)
    expected_all = set(ALL_NAMES) - set(EXCEPTED)
    uncovered = sorted(expected_all - COVERED)
    overcounted = sorted(COVERED - expected_all)
    check("PASS-FEEL the roll call reaches every instrument in the fleet, and prints its own count "
          "every run",
          not ferr and not uncovered and not overcounted,
          ("%d of %d instruments reached (%d table carriers judged for continuity, %d analytic "
           "curves read clean, %d identities read exact, %d catalogued as known, not-yet-repaired "
           "jerks), against 7 of 27 before this phase — %s excepted by name and read nowhere else"
           % (len(COVERED), len(expected_all), len(JUDGED), len(CLEAN_MONOTONE), len(IDENTITY),
              len(KNOWN_JERK), sorted(EXCEPTED))
           if not uncovered and not overcounted and not ferr
           else "uncovered: %s; wrongly counted twice or not in the tree: %s"
                % (uncovered, overcounted)))

# ------------------------------------------------------------------------------------ the report
print("EX-PASS S-20 — measured response tables and the speed between their points\n")
for name, verdict, detail in results:
    print("[%s] %s" % (verdict, name))
    if detail:
        print("        " + detail)
passed = sum(1 for _, v, _ in results if v == "PASS")
failed = sum(1 for _, v, _ in results if v == "FAIL")
skipped = sum(1 for _, v, _ in results if v == "SKIP")
print("\n%d passed / %d failed / %d skipped" % (passed, failed, skipped))
sys.exit(1 if failed else 0)
