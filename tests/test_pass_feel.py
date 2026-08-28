#!/usr/bin/env python3
"""EX-PASS S-20 — the measured response tables, and the speed the hand feels between their points.
Run: python3 tests/test_pass_feel.py

ROOT. His word of 2026-08-28 02:47 on the crossings as they play: «там бесшовность таксебе
работает... есть вау эффекты но иногда оно как-то дёргается и это неклево» — the seamlessness works
so-so, there are real wow moments, but sometimes it jerks. PLAN.md's S-20 asks for the jerks to be
found by construction rather than by eye: differentiate the curve instead of trusting the comment
over it, and measure the speed and its breaks across the whole range a handle is allowed to take.

WHAT THIS FILE IS ABOUT, AND WHY IT IS ONE FILE AND NOT SIX ROWS IN SIX SUITES.

Seven instruments carry a MEASURED RESPONSE TABLE: twenty-one evenly spaced shares, running from
nought to one, that say what raw value feels a given distance along the hand. The tables are real
measurements — how far a photograph actually travelled per unit of the raw handle, integrated and
inverted — and not one number in any of them is touched by anything here or by the repair these rows
judge. What every one of the seven shares is the OTHER half of the question: how the curve is read
BETWEEN two of its own points. That shared reading is one fact with seven readers, so it gets one
home, exactly as `pass-layer.js`'s own note gives one home to the monotone spline the score tracks
ride.

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
be proving nothing, so the planted run must fail exactly where the shipped run passes.

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
for path in sorted(ASSETS.glob("pass-inst-*.js")):
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
DRIVER = r"""
"use strict";
// Every instrument handed in, loaded for real, and its published response curve differentiated.
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
  const feel = joined.instrument.feel;
  // THE SPEED'S OWN LARGEST STEP BETWEEN TWO NEIGHBOURING SAMPLES, at one spacing and at half it.
  function worstStep(N) {
    const h = 1 / (N - 1), v = new Float64Array(N);
    for (let i = 0; i < N; i++) v[i] = feel(i * h);
    let lo = Infinity, hi = -Infinity;
    for (let i = 0; i < N; i++) { if (v[i] < lo) lo = v[i]; if (v[i] > hi) hi = v[i]; }
    const span = hi - lo;
    if (!(span > 0)) return {span: span, worst: 0, at: 0};
    let worst = 0, at = 0, prev = (v[1] - v[0]) / h;
    for (let i = 2; i < N; i++) {
      const cur = (v[i] - v[i - 1]) / h;
      const step = Math.abs(cur - prev) / span;
      if (step > worst) { worst = step; at = (i - 1) * h; }
      prev = cur;
    }
    return {span: span, worst: worst, at: at};
  }
  const coarse = worstStep(20001), fine = worstStep(40001);
  // The curve stands still where it is held, and it must be exact at both ends of the hand.
  const ends = {at0: feel(0), at1: feel(1)};
  // Monotone: a response curve that turned back would send the picture backwards under a hand that
  // never stopped going forward.
  let backwards = 0, last = -Infinity;
  for (let i = 0; i <= 40000; i++) { const y = feel(i / 40000); if (y < last - 1e-12) backwards++; last = y; }
  out.push({file: path.basename(p), span: coarse.span,
            worstCoarse: coarse.worst, worstFine: fine.worst, atCoarse: coarse.at,
            halving: coarse.worst > 0 ? fine.worst / coarse.worst : 0,
            ends: ends, backwards: backwards});
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
                "PASS-FEEL the straight-line read planted back breaks the speed again"):
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
    # from: at each of the twenty-one shares the curve must answer the table's own number.
    KNOT_DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const [modulePath, knotsPath] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(knotsPath, "utf8"));
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "ex");
let joined = null;
const sandbox = {window: {__exPassInstrument: (m) => { joined = m; }},
                 console: {log(){}, warn(){}, error(){}}};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: path.basename(modulePath)});
const feel = joined.instrument.feel;
let worst = 0, at = -1;
for (let k = 0; k <= 20; k++) {
  const u = spec.d0 + (1 - 2 * spec.d0) * (k / 20);
  const d = Math.abs(feel(u) - spec.q[k]);
  if (d > worst) { worst = d; at = k; }
}
console.log(JSON.stringify({worst: worst, at: at}));
"""
    DEAD_BAND = re.compile(r"var\s+(?:FEEL_D0|DIAL_D0)\s*=\s*([0-9.]+)\s*;")
    DIAL_TABLE = {"matter": "FEEL_Q", "beat": "FEEL_Q", "gears": "FEEL_Q", "gates": "FEEL_Q",
                  "adrift": "FEEL_MIX", "waterline": "dial"}
    knot_rows, knot_bad = [], []
    for n in JUDGED:
        c = CARRIERS[n]
        name = DIAL_TABLE.get(n)
        band = DEAD_BAND.search(c["src"])
        if not name or name not in c["tables"] or not band:
            knot_bad.append((n, "no dial table or dead band could be read off the file"))
            continue
        spec = {"d0": float(band.group(1)), "q": c["tables"][name]}
        got = run_node(KNOT_DRIVER, {c["path"].name: c["src"], "knots.json": json.dumps(spec)})
        if got.get("error"):
            knot_bad.append((n, got["error"]))
        else:
            knot_rows.append((n, got["worst"]))
            if got["worst"] > 1e-12:
                knot_bad.append((n, "share %d is off by %g" % (got["at"], got["worst"])))
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
        # `q`-argument one the two multi-table files share
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
