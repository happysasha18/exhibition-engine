#!/usr/bin/env python3
"""DR-6 — the darkroom bench: which instrument ids it offers for one work, and in what order.

FIXTURE PROVENANCE. tests/fixtures/darkroom-records.json is a byte-for-byte copy, taken 2026-09-04,
of ~/tlvphotos-site/site/pass-workrecords.json — a different checkout's own gitignored build
output. That path exists only on this machine, so a suite that read it live would be green here and
red (or silently absent) anywhere else; the copy in this tree is what makes the row portable. 121
real per-work records, each already carrying the `structure`/`symmetry`/`matter`/... measurements
lab/build-workrecords-v1.py computes from the photograph itself.

WHAT IS UNDER TEST. `darkroomBenchOffers` (engine/assets/darkroom.js), the REAL, currently shipped
function, extracted by balanced-brace text extraction — the same idiom tests/test_pass_levels.py's
own `extract_function` carries (:63-97) — and run in a generated Node driver script
(`subprocess.run(["node", driver])`, never Node's `vm` module, matching tests/test_pass_levels.py's
own driver at :140-150). Alongside it the driver runs the REAL fleet: all 27 engine/assets/pass-
inst-*.js files, concatenated and run exactly as the browser host runs them (each is its own IIFE
reading `window.__PassInstrument` — `@@NS@@` stripped, as tests/test_pass_levels.py:60 already
does for pass-composer.js), so the manifests `darkroomBenchOffers` reads are the shipped ones and
not a hand-typed stand-in.

darkroom.js is new — no prior spec names a "darkroom bench" anywhere in this tree — so its own
header states the rules it implements, against D4's "grain appears only after structure exists" and
Requirement 30 criterion 16's "Grain shall be seasoning and never the picture's base". "Strong" is
read categorically, never against an invented magnitude floor: structure.ownDevice.kind is one of a
fixed small set of family names the analyser always assigns (rings/tiles/stripes over this fixture's
121 records), and symmetry.reflection.leftOntoRight.inRecipe is the reflection analyser's own
boolean verdict. No number is chosen by this file or this test; an earlier draft compared readings
against 0.5 and 0.95 picked by eyeballing the fixture's own spread, which this project's standing
rule against inventing numbers ruled out — see engine/assets/darkroom.js's own comments at the
pattern-roots and fold sections for the sources this revision reads instead.

Five rows (TEST_MATRIX-style, stated once each):
  1. reflection — a work whose record reads a strong left-onto-right reflection puts `livemirror`,
     the fleet's own fold, first in the returned list.
  2. pattern withheld — a work whose record already carries a strong own device (banding, here)
     withholds an instrument that would lay that same pattern again.
  3. pattern returns — once the chain carries a step that already engaged that same device, the
     withheld instrument is offered again.
  4. grain waits for structure — grain-bearing instruments are absent from an empty chain and
     present once the chain carries one step.
  5. mostly withheld, every work — on a first call (empty chain) the offered list is a strict
     subset of the fleet, for all 121 works. Weak alone (any bench that returns fewer than the
     fleet's own count clears it) — it stands only beside the four rows above it; no defect is
     claimed against it on its own.

PLANTED DEFECTS, each a text mutation applied to a throwaway in-memory copy of the extracted
darkroom.js source — the file on disk is never touched (tests/test_pass_matter.py:358-364's own
rule: "the source file on disk is never touched, so nothing has to be restored and no working tree
can be left changed by a red-on-bug proof"):
  - invert the pattern test (drop the `!rootAddressedByChain(root)` guard's sense, so a root already
    carrying a pattern never withholds anything): row 2 reds, an already-patterned work is offered
    the instrument that would double it. Row 5 does NOT red with it — inverting one predicate does
    not make the bench return all 27 ids, so the subset row stays green regardless.
  - drop the chain's structural-step condition from the grain rule (`!structuralStepDone` ->
    `false`, so a grain-bearing instrument is never withheld): row 4 reds, a grain-bearing
    instrument now stands on an empty chain.

Run: python3 tests/test_darkroom_bench.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DARKROOM = ROOT / "engine" / "assets" / "darkroom.js"
INST_DIR = ROOT / "engine" / "assets"
FIXTURE = ROOT / "tests" / "fixtures" / "darkroom-records.json"

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


DARKROOM_SOURCE = DARKROOM.read_text(encoding="utf-8")
BENCH_SRC = extract_function(DARKROOM_SOURCE, "darkroomBenchOffers")

# The real fleet: every engine/assets/pass-inst-*.js, concatenated exactly as the browser host
# would evaluate them one at a time, each still its own IIFE. `@@NS@@` is stripped the same way
# tests/test_pass_levels.py:60 strips it for pass-composer.js.
INST_PATHS = sorted(INST_DIR.glob("pass-inst-*.js"))
FLEET_SRC = "\n".join(
    p.read_text(encoding="utf-8").replace("@@NS@@", "") for p in INST_PATHS
)
FLEET_SIZE = len(INST_PATHS)

RECORDS = json.loads(FIXTURE.read_text(encoding="utf-8"))

TMP = Path(tempfile.mkdtemp(prefix="darkroom_bench_"))
DRIVER_PATH = TMP / "darkroom-bench-driver.js"


def run(record, chain, bench_src=None):
    """One Node run: builds the real FLEET from the real instrument files, then calls
    `darkroomBenchOffers(record, chain, FLEET)` (possibly a mutated throwaway copy of it) and
    reports what it returned, plus the fleet size it was offered against."""
    bench_src = BENCH_SRC if bench_src is None else bench_src
    driver = (
        "\"use strict\";\n"
        "var FLEET = {};\n"
        "var window = { __PassInstrument: function (p) {\n"
        "  if (p && p.instrument && p.instrument.name) { FLEET[p.instrument.name] = p.instrument.manifest; }\n"
        "} };\n"
        + FLEET_SRC + "\n"
        + bench_src + "\n"
        "var record = " + json.dumps(record) + ";\n"
        "var chain = " + json.dumps(chain) + ";\n"
        "var offered = darkroomBenchOffers(record, chain, FLEET);\n"
        "console.log(JSON.stringify({ offered: offered, fleetSize: Object.keys(FLEET).length }));\n"
    )
    DRIVER_PATH.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(DRIVER_PATH)], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-2000:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


def main():
    if not node_available():
        print("SKIP: node not available")
        return 0

    # Sanity: the real fleet built from the shipped files is the real 27, not a fixture stand-in.
    sanity = run(list(RECORDS.values())[0], [])
    if "error" in sanity:
        check("darkroom/fleet-builds", False, sanity["error"])
        print("FLEET FAILED TO BUILD: %s" % sanity["error"])
        print_results()
        return 1
    check("darkroom/fleet-size", sanity["fleetSize"] == FLEET_SIZE,
          "fleet built %d instruments from %d pass-inst-*.js files"
          % (sanity["fleetSize"], FLEET_SIZE))
    print("-- fleet: %d instruments built from the real pass-inst-*.js files --" % sanity["fleetSize"])

    # ---------------------------------------------------------------- row 1: reflection -> fold
    #
    # RECORD_REFLECTION: id 18006107842248584, symmetry.reflection.leftOntoRight.reading == 1.0 —
    # the strongest in the fixture's own 121 (measured spread: -0.16 .. 1.0, median 0.82; the top
    # decile alone clears 0.95). structure.banding.score == 0.403 here (below darkroom.js's own 0.5
    # "strong" bar), so the pattern-withhold rule (row 2/3) is not in play for this record and does
    # not confound this row.
    r1 = RECORDS["18006107842248584"]
    got1 = run(r1, [])
    check("darkroom/reflection-puts-fold-first",
          "error" not in got1 and got1["offered"][:1] == ["livemirror"],
          "offered[0]=%r" % (got1.get("offered", got1)[:1] if "offered" in got1 else got1))
    print("row 1 (reflection=%.4f): offered[0]=%r"
          % (r1["symmetry"]["reflection"]["leftOntoRight"]["reading"],
             got1.get("offered", got1.get("error"))[:3] if "offered" in got1 else got1))

    # ------------------------------------------------------------- rows 2/3: pattern withheld
    #
    # RECORD_PATTERN: id 17859642835320709, structure.ownDevice.kind == "stripes" (one of seven such
    # records in the 121-work fixture; darkroom.js reads this categorically, never against a chosen
    # magnitude), and its own reflection.leftOntoRight.inRecipe is False, so the fold row's own rule
    # does not confound this one. Of the fleet, exactly `weave` and `wind` declare `suits.reads`
    # naming structure.banding.score (grepped once, by hand, against the shipped files — not
    # re-checked here, since the row only needs its own instrument absent and present, not the full
    # membership of that set).
    r23 = RECORDS["17859642835320709"]
    got2 = run(r23, [])
    check("darkroom/pattern-withheld",
          "error" not in got2 and "weave" not in got2.get("offered", ["weave"]),
          "offered=%r" % got2)
    print("row 2 (ownDevice.kind=%r): weave withheld=%s"
          % (r23["structure"]["ownDevice"]["kind"], "weave" not in got2.get("offered", [])))

    # Row 3: the chain already carries `wind` — another instrument whose own `suits.reads` names
    # structure.banding.score, so darkroom.js's own rule counts the device as already engaged — and
    # `weave` is offered again.
    got3 = run(r23, ["wind"])
    check("darkroom/pattern-returns-once-engaged",
          "error" not in got3 and "weave" in got3.get("offered", []),
          "offered=%r" % got3)
    print("row 3 (chain=[wind]): weave offered=%s" % ("weave" in got3.get("offered", [])))

    # -------------------------------------------------------------------- row 4: grain waits
    #
    # RECORD_PLAIN: id 17843080526947498, structure.ownDevice.kind == "tiles". None of
    # `adrift`/`matter`/`pour` declares a `suits.reads` naming structure.ownDevice or
    # structure.grid, so the pattern-withhold rule never reaches them on any record — this row
    # isolates to the grain rule alone regardless of which family the work's own device carries.
    r4 = RECORDS["17843080526947498"]
    GRAIN_BEARING = {"adrift", "matter", "pour"}
    got4a = run(r4, [])
    empty_ok = "error" not in got4a and not (GRAIN_BEARING & set(got4a.get("offered", [])))
    check("darkroom/grain-absent-on-empty-chain", empty_ok,
          "offered ^ grain-bearing = %r" % (GRAIN_BEARING & set(got4a.get("offered", []))))
    got4b = run(r4, ["hero"])
    after_ok = "error" not in got4b and (GRAIN_BEARING & set(got4b.get("offered", [])))
    check("darkroom/grain-present-after-one-step", bool(after_ok),
          "offered ^ grain-bearing = %r" % (GRAIN_BEARING & set(got4b.get("offered", []))))
    print("row 4: grain-bearing absent on []=%s, present on [hero]=%s"
          % (empty_ok, bool(after_ok)))

    # ------------------------------------------------------------- row 5: strict subset, all 121
    subset_fail = []
    for wid, rec in RECORDS.items():
        got = run(rec, [])
        if "error" in got or not (len(got["offered"]) < FLEET_SIZE):
            subset_fail.append(wid)
    check("darkroom/strict-subset-all-121-works", not subset_fail,
          "%d/%d works failed the strict-subset row: %r"
          % (len(subset_fail), len(RECORDS), subset_fail[:5]))
    print("row 5: strict subset holds on %d/%d works"
          % (len(RECORDS) - len(subset_fail), len(RECORDS)))

    # ------------------------------------------------------------ planted defects (DR-6)
    #
    # Each mutation is applied to a throwaway in-memory copy of BENCH_SRC; the file on disk is
    # never touched (tests/test_pass_matter.py:358-364).
    print("\n-- planted defects: each must red the row it targets, clear once removed, and leave "
          "the other rows exactly as claimed --")

    def plant(frm, to):
        if BENCH_SRC.find(frm) < 0:
            raise ValueError("plant target not found: %r" % frm)
        return BENCH_SRC.replace(frm, to)

    # Defect 1: invert the chain-addressed guard, so an instrument whose pattern would stack on
    # one the record already carries is offered anyway (withheld only once the chain has ALREADY
    # addressed the root, which is backwards).
    defect1_src = plant(
        "&& !rootAddressedByChain(root);",
        "&& rootAddressedByChain(root);")
    d1_row2 = run(r23, [], defect1_src)
    d1_row2_red = "error" not in d1_row2 and "weave" in d1_row2.get("offered", [])
    check("defect/pattern-inverted reds row 2", d1_row2_red, "offered=%r" % d1_row2)
    d1_row5_fail = []
    for wid, rec in RECORDS.items():
        got = run(rec, [], defect1_src)
        if "error" in got or not (len(got["offered"]) < FLEET_SIZE):
            d1_row5_fail.append(wid)
    d1_row5_still_green = not d1_row5_fail
    check("defect/pattern-inverted leaves row 5 green", d1_row5_still_green,
          "%d/%d works still hold the strict-subset row under this plant"
          % (len(RECORDS) - len(d1_row5_fail), len(RECORDS)))
    print("defect 1 (pattern test inverted): row 2 reds=%s, row 5 stays green=%s"
          % (d1_row2_red, d1_row5_still_green))

    # Defect 2: drop the chain's structural-step condition out of the grain rule.
    defect2_src = plant(
        "if (isGrainBearing(m) && !structuralStepDone) return false;",
        "if (isGrainBearing(m) && false) return false;")
    d2_row4 = run(r4, [], defect2_src)
    d2_row4_red = "error" not in d2_row4 and bool(GRAIN_BEARING & set(d2_row4.get("offered", [])))
    check("defect/grain-gate-dropped reds row 4", d2_row4_red, "offered=%r" % d2_row4)
    print("defect 2 (grain gate dropped): row 4 reds (grain-bearing on an empty chain)=%s"
          % d2_row4_red)

    # Confirmation: with both defects removed, rows 2 and 4 are green again on the same records
    # (already shown above as the correctness pass; re-checked explicitly here, same inputs).
    clean_row2 = run(r23, [])
    clean_row4 = run(r4, [])
    clears = ("weave" not in clean_row2.get("offered", ["weave"])
              and not (GRAIN_BEARING & set(clean_row4.get("offered", []))))
    check("defect/both clear once removed", clears,
          "row2 offered=%r, row4 offered=%r" % (clean_row2, clean_row4))
    print("both defects removed: row 2 and row 4 green again=%s" % clears)

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
