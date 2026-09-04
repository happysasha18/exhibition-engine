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

ADDED FOR `engage(instrumentId, state, manifests)` (engine/assets/darkroom.js), shelf 17's
one-owner-per-level law (pass-composer.js:3994's `ownTheLevels`) felt as a hand's own action: when
the newly engaged instrument declares a structural level an already-engaged instrument's own handle
also declares, that handle is walked back toward its own manifest's `def` through `darkroomEase` —
never a second ease — instead of snapping there. Run against the REAL fleet, the same concatenated
`pass-inst-*.js` idiom as tests/test_darkroom_bench.py, so the level declarations read are the real
shipped ones. Two real instruments anchor the rows: `gates` (its `teeth` handle declares CELL, def
9, and its `shade` handle declares `level: null`, def 1) and `livemirror` (declares CELL only, over
several of its own handles) collide on CELL; `beat` (declares SURFACE only) does not.

Four rows:
  6. engage("livemirror") after engage("gates") — with gates.teeth moved off its def to 22 first —
     walks gates.teeth back toward its own manifest's def (9) through several sampled ease steps,
     never landing on it in one step.
  7. that walk-back is monotone toward 9 and lands within a small distance of it after enough steps
     — it neither overshoots nor stalls short forever.
  8. engage("beat") — a different level (SURFACE, no CELL of its own) — after the same gates.teeth
     setup leaves gates.teeth exactly where it stood; no exchange triggers across different levels.
  9. gates.shade (level: null, moved off its def to 0.3) is left exactly where it stood when
     engage("livemirror") walks gates.teeth (CELL) back — a level: null handle claims no level and
     is never part of an exchange, whichever side of it a real level sits on.

PLANTED DEFECTS for `engage`, each a text mutation applied to a throwaway in-memory copy of the
extracted source (tests/test_pass_matter.py:358-364's rule — the file on disk is never touched):
  - replace the eased assignment with a direct assignment to `def`: row 6 reds, because the sampled
    sequence jumps straight to def with no intermediate values.
  - drop the level-match test out of the walk-back guard, keeping only the null check, so every
    engage() walks back the previously engaged handle regardless of level: row 8 reds, because the
    SURFACE-only `beat` now disturbs gates.teeth anyway.
  - make `isRealLevel` always true, so `level: null` is treated as a real (shared) level of its own:
    row 9 reds, because gates.shade and livemirror's own null-level handles now count as the same
    level and trigger an exchange.

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
ENGAGE_SRC = extract_function(DARKROOM_SOURCE, "engage")

# ENGAGE'S OWN FLEET. `engage` reads structural levels off each handle's own manifest field, so the
# manifests it is run against here are the REAL, shipped ones — every engine/assets/pass-inst-*.js,
# concatenated exactly as the browser host would evaluate them one at a time, each still its own
# IIFE, `@@NS@@` stripped the same way tests/test_pass_levels.py:60 strips it for pass-composer.js.
# This is the same idiom tests/test_darkroom_bench.py already uses for `darkroomBenchOffers`.
INST_DIR = ROOT / "engine" / "assets"
INST_PATHS = sorted(INST_DIR.glob("pass-inst-*.js"))
FLEET_SRC = "\n".join(
    p.read_text(encoding="utf-8").replace("@@NS@@", "") for p in INST_PATHS
)

TMP = Path(tempfile.mkdtemp(prefix="darkroom_taste_"))
DRIVER_PATH = TMP / "darkroom-taste-driver.js"
ENGAGE_DRIVER_PATH = TMP / "darkroom-engage-driver.js"

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


def run_engage(script_src, engage_src=None):
    """Builds the REAL fleet from the REAL pass-inst-*.js files (same idiom as
    tests/test_darkroom_bench.py's own `run`), then runs `script_src` with `engage`, `darkroomEase`
    and `FLEET` (instrument id -> manifest) in scope. `engage_src` defaults to the real, current
    `engage` — pass a mutated throwaway copy for a planted-defect run."""
    engage_src = ENGAGE_SRC if engage_src is None else engage_src
    driver = (
        "\"use strict\";\n"
        "var FLEET = {};\n"
        "var window = { __PassInstrument: function (p) {\n"
        "  if (p && p.instrument && p.instrument.name) { FLEET[p.instrument.name] = p.instrument.manifest; }\n"
        "} };\n"
        + FLEET_SRC + "\n"
        + EASE_SRC + "\n"
        + engage_src + "\n"
        + script_src + "\n"
    )
    ENGAGE_DRIVER_PATH.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(ENGAGE_DRIVER_PATH)], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-2000:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


# The two real, shipped instruments the engage rows collide on CELL, plus one that shares no level
# with either: `gates`'s `teeth` handle (CELL, def 9) and `shade` handle (level: null, def 1) sit in
# state; `livemirror` declares CELL over several of its own handles; `beat` declares SURFACE only.
ENGAGE_WALK_SCRIPT = (
    "var state = {};\n"
    "state = engage('gates', state, FLEET);\n"
    "state.gates.teeth = 22;\n"
    "var seq = [state.gates.teeth];\n"
    "for (var i = 0; i < 60; i++) {\n"
    "  state = engage('livemirror', state, FLEET);\n"
    "  seq.push(state.gates.teeth);\n"
    "}\n"
    "console.log(JSON.stringify({ seq: seq, def: FLEET.gates.handles.teeth.def }));\n"
)

ENGAGE_DIFFERENT_LEVEL_SCRIPT = (
    "var state = {};\n"
    "state = engage('gates', state, FLEET);\n"
    "state.gates.teeth = 22;\n"
    "var before = state.gates.teeth;\n"
    "state = engage('beat', state, FLEET);\n"
    "console.log(JSON.stringify({ before: before, after: state.gates.teeth }));\n"
)

ENGAGE_NULL_LEVEL_SCRIPT = (
    "var state = {};\n"
    "state = engage('gates', state, FLEET);\n"
    "state.gates.teeth = 22;\n"
    "state.gates.shade = 0.3;\n"
    "var beforeTeeth = state.gates.teeth, beforeShade = state.gates.shade;\n"
    "state = engage('livemirror', state, FLEET);\n"
    "console.log(JSON.stringify({ beforeTeeth: beforeTeeth, afterTeeth: state.gates.teeth,\n"
    "                             beforeShade: beforeShade, afterShade: state.gates.shade }));\n"
)


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

    # ------------------------------------------------------------------ rows 6-9: engage's exchange
    walk = run_engage(ENGAGE_WALK_SCRIPT)
    row6_ok = row7_ok = False
    if "error" in walk:
        check("taste/engage-runs", False, walk["error"])
        print("ENGAGE FAILED TO RUN: %s" % walk["error"])
    else:
        seq, engage_def = walk["seq"], walk["def"]
        # row 6: never in one step — the first step off 22 stands strictly between 22 and def (9),
        # never landing on def itself.
        row6_ok = engage_def < seq[1] < seq[0]
        check("taste/engage-walk-back-never-one-step", row6_ok,
              "gates.teeth 22 -> first step %.6f (def=%.1f), strictly between=%s"
              % (seq[1], engage_def, row6_ok))
        print("row 6 (engage walk-back never one step): 22 -> %.6f -> ... (def=%.1f): %s"
              % (seq[1], engage_def, row6_ok))

        # row 7: strictly closer to def on every sampled step (cheaper and exact — an exponential
        # ease approaches its target asymptotically, so it is never exactly reached, but every step
        # must move strictly nearer to it and never overshoot or stall short).
        strictly_closer = all(seq[i] > seq[i + 1] > engage_def for i in range(len(seq) - 1))
        row7_ok = strictly_closer
        check("taste/engage-walk-back-reaches-def", row7_ok,
              "strictly closer to def=%.1f on every one of %d steps=%s" % (engage_def, len(seq) - 1, strictly_closer))
        print("row 7 (engage walk-back strictly approaches def): every step closer=%s, final=%.6f"
              % (strictly_closer, seq[-1]))

    diff = run_engage(ENGAGE_DIFFERENT_LEVEL_SCRIPT)
    row8_ok = False
    if "error" in diff:
        check("taste/engage-different-level-runs", False, diff["error"])
        print("ENGAGE (different level) FAILED TO RUN: %s" % diff["error"])
    else:
        row8_ok = diff["after"] == diff["before"]
        check("taste/engage-different-level-untouched", row8_ok,
              "gates.teeth before=%r after engage(beat)=%r" % (diff["before"], diff["after"]))
        print("row 8 (different level leaves the handle untouched): before=%r after=%r"
              % (diff["before"], diff["after"]))

    nul = run_engage(ENGAGE_NULL_LEVEL_SCRIPT)
    row9_ok = False
    if "error" in nul:
        check("taste/engage-null-level-runs", False, nul["error"])
        print("ENGAGE (null level) FAILED TO RUN: %s" % nul["error"])
    else:
        shade_untouched = nul["afterShade"] == nul["beforeShade"]
        teeth_moved = nul["afterTeeth"] != nul["beforeTeeth"]
        row9_ok = shade_untouched and teeth_moved
        check("taste/engage-null-level-never-exchanged", row9_ok,
              "shade %r -> %r (untouched=%s), teeth %r -> %r (moved=%s)"
              % (nul["beforeShade"], nul["afterShade"], shade_untouched,
                 nul["beforeTeeth"], nul["afterTeeth"], teeth_moved))
        print("row 9 (level: null never exchanged): shade untouched=%s, sibling CELL handle moved=%s"
              % (shade_untouched, teeth_moved))

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

    # Defect 3: the exchange sets the handle to its neutral in one assignment instead of through the
    # ease — row 6 reds, the sampled sequence jumps straight to def with no intermediate values.
    defect3_src = plant(ENGAGE_SRC,
                         "next[iid][h] = darkroomEase(next[iid][h], def, ENGAGE_DT, ENGAGE_TAU);",
                         "next[iid][h] = def;")
    d3 = run_engage(ENGAGE_WALK_SCRIPT, defect3_src)
    d3_row6_red = "error" not in d3 and not (d3["def"] < d3["seq"][1] < d3["seq"][0])
    check("defect/direct-assignment reds row 6 (engage walk-back)", d3_row6_red,
          "gates.teeth 22 -> first step %r under the direct assignment" % (d3.get("seq", [None, None])[1],))
    print("defect 3 (engage direct assignment to def): row 6 reds=%s" % d3_row6_red)

    # Defect 4: drop the level-match test out of the walk-back guard, keeping only the null check,
    # so every engage() walks back the previously engaged handle regardless of level — row 8 reds,
    # the SURFACE-only `beat` now disturbs gates.teeth anyway.
    defect4_src = plant(ENGAGE_SRC,
                         "if (!isRealLevel(lv) || incomingLevels.indexOf(lv) < 0) return;",
                         "if (!isRealLevel(lv)) return;")
    d4 = run_engage(ENGAGE_DIFFERENT_LEVEL_SCRIPT, defect4_src)
    d4_row8_red = "error" not in d4 and d4["after"] != d4["before"]
    check("defect/level-comparison-dropped reds row 8 (different level)", d4_row8_red,
          "gates.teeth before=%r after engage(beat)=%r under the dropped comparison"
          % (d4.get("before"), d4.get("after")))
    print("defect 4 (engage level comparison dropped): row 8 reds=%s" % d4_row8_red)

    # Defect 5: `isRealLevel` always answers true, so `level: null` is treated as a real (shared)
    # level of its own — row 9 reds, gates.shade and livemirror's own null-level handles now count
    # as the same level and trigger an exchange.
    defect5_src = plant(ENGAGE_SRC,
                         "function isRealLevel(lv) { return !!lv; }",
                         "function isRealLevel(lv) { return true; }")
    d5 = run_engage(ENGAGE_NULL_LEVEL_SCRIPT, defect5_src)
    d5_row9_red = "error" not in d5 and d5["afterShade"] != d5["beforeShade"]
    check("defect/null-as-real-level reds row 9 (level: null exchanged)", d5_row9_red,
          "gates.shade before=%r after=%r under null-as-real-level"
          % (d5.get("beforeShade"), d5.get("afterShade")))
    print("defect 5 (engage treats level: null as real): row 9 reds=%s" % d5_row9_red)

    # Confirmation: with all defects removed (i.e. against the real, unmutated source), the same
    # rows stand green again — the exact same calls already made above, at the top of this run.
    clean_row2_ok = row2_ok
    clean_row3_ok = row3_ok
    clean_row5_ok = row5_ok if "error" not in up and "error" not in down else False
    clean_row6_ok, clean_row7_ok = row6_ok, row7_ok
    clean_row8_ok, clean_row9_ok = row8_ok, row9_ok
    clears = (clean_row2_ok and clean_row3_ok and clean_row5_ok
              and clean_row6_ok and clean_row7_ok and clean_row8_ok and clean_row9_ok)
    check("defect/all clear once removed", clears,
          "row2=%s row3=%s row5=%s row6=%s row7=%s row8=%s row9=%s"
          % (clean_row2_ok, clean_row3_ok, clean_row5_ok,
             clean_row6_ok, clean_row7_ok, clean_row8_ok, clean_row9_ok))
    print("all defects removed: rows 2, 3, 5, 6, 7, 8 and 9 green again=%s" % clears)

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
