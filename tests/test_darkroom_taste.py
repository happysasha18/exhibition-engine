#!/usr/bin/env python3
"""DR-7 — the edge of taste is felt as resistance.

WHAT IS UNDER TEST. `resist(travel, busyness)` and `darkroomEase(current, target, dt, tau)`
(engine/assets/darkroom.js), the REAL, currently shipped functions, extracted by balanced-brace
text extraction — the same idiom tests/test_pass_levels.py's own `extract_function` carries
(:63-97) — and run in a generated Node driver script (`subprocess.run(["node", driver])`, never
Node's `vm` module, matching tests/test_pass_levels.py's own driver at :140-150). This is the same
idiom tests/test_darkroom_bench.py already uses for `darkroomBenchOffers` in this same file.

SCOPE. This unit was shrunk by a standing rule that arrived mid-execution (docs/DARKROOM-EXECUTION.md,
"DR-7, the cliff — shrunk"): dropped are the equal-felt-change ratio row (FEEL_CEIL/2.5, borrowed
from a different measurement space) and Requirement 34 criterion 5's four-count formal curve proof
(continuous in speed / stands at both ends / monotone in the hand / passes through the measurement's
own points), copied from tests/test_pass_feel.py — both curve-shape measurements-for-measurement's-
sake, not defects this unit's own shape can fail on. No exact ease time constant (0.09s or 0.5s) is
asserted either; the ease is proven only on the shape Requirement 40 criterion 11 asks for — nothing
ever snaps.

Five rows (TEST_MATRIX-style, stated once each):
  1. monotone in busyness — for a fixed travel, resist does not increase as busyness rises.
  2. no clamp — over a sweep of the busyness range [0, 1] and an interior travel range (0, 1), the
     handle's own normalized bounds (darkroom.js's own `readingOf` already clamps every reading to
     this same [0, 1] scale, so a handle's declared min/max are 0 and 1 here), resist never returns
     0 (the min) and never returns 1 (the max) — a return at either boundary would be a clamp, and
     Requirement 41 criterion 7 bans clamps and warnings both.
  3. never flat — at one fixed busyness, distinct travels never return the same value.
  4. driving one handle from its declared min (0) to its declared max (1) in equal hand steps,
     against a busyness that rises monotonically with the handle (busyness := the handle's own
     fraction travelled, 0 at min and 1 at max), the handle's final value stands short of 1 and
     every step still moved it.
  5. the exponential ease never arrives in one step: after one frame, a handle eased toward a
     target stands strictly between its old value and that target — proof of shape only, no tau.

PLANTED DEFECTS, each a text mutation applied to a throwaway in-memory copy of the extracted
source — the file on disk is never touched (tests/test_pass_matter.py:358-364's own rule: "the
source file on disk is never touched, so nothing has to be restored and no working tree can be left
changed by a red-on-bug proof"):
  - replace `resist`'s body with a hard stop that returns zero travel past busyness 0.5: row 2 reds
    (the returned travel leaves the range at the bottom, 0, for every busyness above the threshold),
    and row 3 reds with it (every travel past that same threshold returns the identical zero value,
    so the curve goes flat there);
  - replace `darkroomEase`'s return with the bare target (a direct assignment, so the handle jumps
    straight there): row 5 reds, because the eased value now equals the target instead of standing
    strictly short of it.

Run: python3 tests/test_darkroom_taste.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DARKROOM = ROOT / "engine" / "assets" / "darkroom.js"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def extract_function(text, name, after_idx=0):
    """Balanced-brace extraction of `function NAME(...) { ... }` — the REAL, current body, the
    same idiom tests/test_pass_levels.py's own `extract_function` carries (:63-97)."""
    marker = "function %s(" % name
    idx = text.index(marker, after_idx)
    brace = text.index("{", idx)
    depth, i = 0, brace
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[idx:i + 1]
        i += 1
    raise ValueError("unbalanced braces for function %s" % name)


def plant(src, frm, to):
    if src.find(frm) < 0:
        raise ValueError("plant target not found: %r" % frm)
    return src.replace(frm, to)


DARKROOM_SOURCE = DARKROOM.read_text(encoding="utf-8")
RESIST_SRC = extract_function(DARKROOM_SOURCE, "resist")
EASE_SRC = extract_function(DARKROOM_SOURCE, "darkroomEase")

TMP = Path(tempfile.mkdtemp(prefix="darkroom_taste_"))
DRIVER_PATH = TMP / "darkroom-taste-driver.js"

MIN, MAX = 0.0, 1.0   # the handle's own declared bounds — darkroom.js's own `readingOf` already
                       # normalizes every reading to this same [0, 1] scale (darkroom.js:41-46).
BUSY_SWEEP = [i / 10.0 for i in range(11)]          # 0.0 .. 1.0
TRAVEL_INTERIOR = [j / 20.0 for j in range(1, 20)]  # 0.05 .. 0.95, strictly inside (MIN, MAX)
TRAVEL_FIXED = [0.1, 0.4, 0.9]


def run_js(funcs_src, script_src):
    driver = "\"use strict\";\n" + funcs_src + "\n" + script_src + "\n"
    DRIVER_PATH.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(DRIVER_PATH)], capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-2000:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


def resist_sweep(resist_src):
    """Rows 1-3 in one Node call: fixed-travel busyness sweep (row 1), the full interior sweep
    (row 2), and the per-busyness travel groups (row 3)."""
    script = (
        "var row1 = " + json.dumps(TRAVEL_FIXED) + ".map(function (t) {\n"
        "  return { travel: t, values: " + json.dumps(BUSY_SWEEP) + ".map(function (b) { return resist(t, b); }) };\n"
        "});\n"
        "var row2 = [];\n"
        + json.dumps(TRAVEL_INTERIOR) + ".forEach(function (t) {\n"
        "  " + json.dumps(BUSY_SWEEP) + ".forEach(function (b) { row2.push(resist(t, b)); });\n"
        "});\n"
        "var row3 = " + json.dumps(BUSY_SWEEP) + ".map(function (b) {\n"
        "  return { busyness: b, values: " + json.dumps(TRAVEL_INTERIOR) + ".map(function (t) { return resist(t, b); }) };\n"
        "});\n"
        "console.log(JSON.stringify({ row1: row1, row2: row2, row3: row3 }));\n"
    )
    return run_js(resist_src, script)


def drive_sim(resist_src, steps=20):
    """Row 4: drive one handle from MIN to MAX in `steps` equal hand steps, busyness read live off
    the handle's own current fraction travelled (0 at MIN, 1 at MAX, rising monotonically with the
    handle by construction)."""
    script = (
        "var MIN = " + json.dumps(MIN) + ", MAX = " + json.dumps(MAX) + ", N = " + json.dumps(steps) + ";\n"
        "var STEP = (MAX - MIN) / N;\n"
        "var pos = MIN, everyStepMoved = true;\n"
        "for (var i = 0; i < N; i++) {\n"
        "  var b = (pos - MIN) / (MAX - MIN);\n"
        "  var actual = resist(STEP, b);\n"
        "  if (!(actual > 0)) everyStepMoved = false;\n"
        "  pos += actual;\n"
        "}\n"
        "console.log(JSON.stringify({ finalPos: pos, everyStepMoved: everyStepMoved }));\n"
    )
    return run_js(resist_src, script)


def ease_once(ease_src, current, target, dt=1.0 / 60.0, tau=0.09):
    script = (
        "var out = darkroomEase(" + json.dumps(current) + ", " + json.dumps(target) + ", "
        + json.dumps(dt) + ", " + json.dumps(tau) + ");\n"
        "console.log(JSON.stringify({ out: out }));\n"
    )
    return run_js(ease_src, script)


def main():
    if not node_available():
        print("SKIP: node not available")
        return 0

    # ------------------------------------------------------------------- rows 1-3: the real curve
    got = resist_sweep(RESIST_SRC)
    if "error" in got:
        check("taste/resist-runs", False, got["error"])
        print("RESIST FAILED TO RUN: %s" % got["error"])
        print_results()
        return 1

    row1_ok = all(
        all(entry["values"][i] >= entry["values"][i + 1] for i in range(len(entry["values"]) - 1))
        for entry in got["row1"]
    )
    check("taste/monotone-in-busyness", row1_ok,
          "fixed travels %r, busyness 0..1: non-increasing=%s" % (TRAVEL_FIXED, row1_ok))
    print("row 1 (monotone in busyness): holds for travels %r = %s" % (TRAVEL_FIXED, row1_ok))

    row2_ok = all(MIN < v < MAX for v in got["row2"])
    check("taste/no-clamp", row2_ok,
          "%d combinations swept, min/max returned=%s"
          % (len(got["row2"]), not row2_ok))
    print("row 2 (no clamp, never 0 or 1 over %d combinations): %s" % (len(got["row2"]), row2_ok))

    row3_ok = all(
        all(entry["values"][i] < entry["values"][i + 1] for i in range(len(entry["values"]) - 1))
        for entry in got["row3"]
    )
    check("taste/never-flat", row3_ok,
          "strictly increasing in travel at every one of %d busyness readings=%s"
          % (len(got["row3"]), row3_ok))
    print("row 3 (never flat, strictly increasing in travel) at every busyness reading: %s" % row3_ok)

    # --------------------------------------------------------------------- row 4: min-to-max drive
    sim = drive_sim(RESIST_SRC)
    if "error" in sim:
        check("taste/drive-runs", False, sim["error"])
    else:
        row4_ok = sim["everyStepMoved"] and sim["finalPos"] < MAX
        check("taste/short-of-far-end", row4_ok,
              "finalPos=%.6f (MAX=%.1f), everyStepMoved=%s"
              % (sim["finalPos"], MAX, sim["everyStepMoved"]))
        print("row 4 (min->max, busyness rising with the handle): finalPos=%.4f, every step moved=%s"
              % (sim["finalPos"], sim["everyStepMoved"]))

    # ---------------------------------------------------------------------- row 5: the ease
    up = ease_once(EASE_SRC, 0.2, 0.9)
    down = ease_once(EASE_SRC, 0.9, 0.2)
    if "error" in up or "error" in down:
        check("taste/ease-runs", False, "%r / %r" % (up, down))
    else:
        row5_ok = (0.2 < up["out"] < 0.9) and (0.2 < down["out"] < 0.9)
        check("taste/ease-never-one-step", row5_ok,
              "0.2->0.9 lands at %.6f, 0.9->0.2 lands at %.6f, both strictly between=%s"
              % (up["out"], down["out"], row5_ok))
        print("row 5 (ease never arrives in one step): 0.2->0.9 lands at %.6f, 0.9->0.2 lands at %.6f"
              % (up["out"], down["out"]))

    # ------------------------------------------------------------ planted defects, throwaway only
    #
    # Each mutation is applied to a throwaway in-memory copy of RESIST_SRC/EASE_SRC; the file on
    # disk is never touched (tests/test_pass_matter.py:358-364).
    print("\n-- planted defects: each must red the row it targets, clear once removed --")

    defect1_src = plant(RESIST_SRC,
                         "return travel / (1 + b);",
                         "if (b > 0.5) { return 0; }\n  return travel / (1 + b);")
    d1 = resist_sweep(defect1_src)
    d1_row2_red = "error" not in d1 and not all(MIN < v < MAX for v in d1["row2"])
    d1_row3_red = "error" not in d1 and not all(
        all(entry["values"][i] < entry["values"][i + 1] for i in range(len(entry["values"]) - 1))
        for entry in d1["row3"]
    )
    check("defect/hard-stop reds row 2 (no-clamp)", d1_row2_red,
          "some value in [0,1] returned under the hard stop=%s" % d1_row2_red)
    check("defect/hard-stop reds row 3 (never-flat)", d1_row3_red,
          "a busyness group went flat under the hard stop=%s" % d1_row3_red)
    print("defect 1 (resist hard stop at busyness>0.5): row 2 reds=%s, row 3 reds=%s"
          % (d1_row2_red, d1_row3_red))

    defect2_src = plant(EASE_SRC,
                         "return current + (target - current) * k;",
                         "return target;")
    d2_up = ease_once(defect2_src, 0.2, 0.9)
    d2_row5_red = "error" not in d2_up and not (0.2 < d2_up["out"] < 0.9)
    check("defect/direct-assignment reds row 5 (ease)", d2_row5_red,
          "0.2->0.9 landed at %r under the direct assignment" % (d2_up.get("out"),))
    print("defect 2 (ease direct assignment): row 5 reds=%s (landed at %r)"
          % (d2_row5_red, d2_up.get("out")))

    # Confirmation: with both defects removed (i.e. against the real, unmutated source), the same
    # rows stand green again — the exact same calls already made above, at the top of this run.
    clean_row2_ok = row2_ok
    clean_row3_ok = row3_ok
    clean_row5_ok = row5_ok if "error" not in up and "error" not in down else False
    clears = clean_row2_ok and clean_row3_ok and clean_row5_ok
    check("defect/all clear once removed", clears,
          "row2=%s row3=%s row5=%s" % (clean_row2_ok, clean_row3_ok, clean_row5_ok))
    print("both defects removed: rows 2, 3 and 5 green again=%s" % clears)

    print()
    print_results()
    failed = [r for r in results if r[1] == "FAIL"]
    return 1 if failed else 0


def print_results():
    failed = [r for r in results if r[1] == "FAIL"]
    for name, status, detail in results:
        print("%-6s %-45s %s" % (status, name, detail))
    print("\n%d checks, %d passed, %d failed" % (len(results), len(results) - len(failed),
                                                  len(failed)))


if __name__ == "__main__":
    sys.exit(main())
