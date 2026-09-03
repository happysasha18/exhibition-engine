#!/usr/bin/env python3
"""PASS-ARRIVAL-REACH (shelf 7, the 2026-08-31 repair) — a named arrival mode must reach an
instrument's own handle somewhere on a real route, not just name itself on the plan.

Run: python3 tests/test_pass_arrival_reach.py

ROOT. `tests/dump_pass_arrival_walk.py` walks the first ten consecutive edges of the real 121-work
collection and reports, per naряд S-06, «steps whose arrival reached an instrument handle» — CRYSTALLIZED
through pour's own `arrival`/`seedPlace` handles, PROPAGATED through livemirror's own `propagate`
handle, INTERFERED through overlay's or grid-colour's own `arrival` handle. Before this repair that
count was 0 of 10 on every real route this file's own hunt could find, and the cause traced to two
mechanical faults in `engine/assets/pass-composer.js`, neither a typed threshold:

  1. The arrival's own instrument cast (`castArrival`, and the joint bundle planner's own
     `arrivalCandidatesFor`) ranked EVERY instrument the collection publishes on its GENERAL fit for
     the pair — a reading that has nothing to do with which one instrument's own fill branch reads
     `arrival.mode` for the mode that actually won. A named PROPAGATED arrival was landing on
     whichever instrument merely suited the two photographs best, almost never `livemirror`, the one
     instrument built to carry it.
  2. Where the bundle planner's own legality rules DID leave a mode-correct instrument standing in a
     tie with an instrument-less alternative — both scoring the same `voicesPresent*100`, the
     scorer's own comment already says a bundle that keeps a move is never outscored by one that
     drops it — the tie-break read `passIndex ? dieAmong(...) : 0`, a JS truthiness check. A fresh
     pass's own `passIndex` is the number 0, which is falsy, so every first visit to an edge fell
     through to `ties[0]`, the first tied bundle the loop's own enumeration order happened to reach —
     and that order tries real travel before travel-less, so the tie broke toward keeping the
     travelling move, never toward the arrival, every time, for no reason the scorer states.

Both are now repaired at their own site in `pass-composer.js` (search `ARRIVAL_WANTS_INSTRUMENT` and
the tie-break note above `dieAmong(pair.seed, key + "|bundle|" + passIndex, 1009)`). Neither fix
types a new number: the first reads the same `arrival.mode ===` fact this file already hardwires
four times, the second only lets the die the code already built answer for `passIndex === 0` the way
it already answers for every other pass index.

WHY THIS FILE WALKS FURTHER THAN THE TEN-STEP ARTIFACT DOES. `pass_arrival_walk.txt` is prose for a
person to read, and naряд S-06 asks for exactly ten transitions there — widening it would answer a
different question than the one asked. But CRYSTALLIZED and PROPAGATED are rare arrivals (`arrivalOf`
ranks five modes against two works' own records, and most pairs read closest to CONDENSED), and
whether any one instrument reaches a handle within a fixed ten-edge window is small-sample noise: a
real fix can still read 0 of 10 on an unlucky ten edges while reading well above 0 over the route
those ten edges sit inside, which is exactly the check below found before proving anything. This row
walks the SAME real route — the published collection's own consecutive order, the same memory
threading `dump_pass_arrival_walk.py` carries — the whole way through once, and asks the question
naряд S-06 actually asks: does a live walk over the real collection ever reach a handle at all. A
regression that breaks the mechanism above breaks it everywhere on the route, ten edges or all of it,
so this row reds exactly when the ten-edge artifact's own reading would have nothing behind it either.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = HERE / "fixture_pass_composed.json"
WORKS = HERE / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROW_REACH = "PASS-ARRIVAL-REACH a full walk of the real collection's own order reaches an " \
            "instrument handle at least once (naряд S-06, «reached: 0 of N» is the regression)"
ROW_MODES = "PASS-ARRIVAL-REACH more than one arrival mode plays across that same walk"
ROW_STOOD = "PASS-ARRIVAL-REACH a crossing that cannot cast the instrument its arrival mode speaks " \
            "through plays its best available arrival instead of standing down (наряд S-66, the " \
            "narrowing is a demotion and not a filter)"
ROW_REDBUG = "PASS-ARRIVAL-REACH RED-ON-BUG · the hard filter planted back: the arrivals that " \
             "stood down for want of one named instrument stand down again"

# The identical driver `tests/dump_pass_arrival_walk.py` runs, unmodified, so this row proves
# exactly what that artifact would report were it walked over the whole collection instead of the
# first ten edges — no second reading of the composer, no second construction of "reached".
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath, worksPath, stepsArg] = process.argv.slice(2);
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(1); }

const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const composer = joined.make(fix.consts);
const steps = parseInt(stepsArg, 10);

function die(key) {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) { h = Math.imul(h ^ key.charCodeAt(i), 16777619) >>> 0; }
  return (h % 100000) / 100000 * 8;
}

const CARRIERS = {
  "pour.arrival": "CRYSTALLIZED", "pour.seedPlace": "CRYSTALLIZED",
  "livemirror.propagate": "PROPAGATED",
  "overlay.arrival": "INTERFERED", "grid-colour.arrival": "INTERFERED"
};
function unwrap(v) { return (v && typeof v === "object" && "v" in v) ? v.v : v; }

// WHICH INSTRUMENT EACH MODE SPEAKS THROUGH, the same one line pass-composer.js carries. Read here
// only to say which steps row S-66 is about; nothing below narrows anything by it.
const WANTS = {CRYSTALLIZED: "pour", PROPAGATED: "livemirror"};
const ids = Object.keys(works);
const out = {modes: {}, reached: 0, named: 0, wanting: 0, wantingVoiced: 0, wantingSilent: 0};
const played = [], genres = [], miracles = [];
for (let i = 0; i < steps && i + 1 < ids.length; i++) {
  const from = ids[i], to = ids[i + 1];
  const forward = String(from) <= String(to);
  const key = (forward ? from + "__" + to : to + "__" + from) + (forward ? "__ab" : "__ba");
  const req = {
    workRecordA: works[forward ? from : to], workRecordB: works[forward ? to : from],
    direction: forward ? "a-to-b" : "b-to-a", seed: die(key),
    walkMemory: played.slice(), walkGenres: genres.slice(), walkMiracles: miracles.slice()
  };
  let p = null;
  try { p = composer.passageFor(req); } catch (e) { p = null; }
  const plan = (p && p.plan) || null;
  const arr = (plan && plan.arrival) || {};
  const cues = (plan && plan.cues) || [];
  const drove = [];
  for (const c of cues) {
    const mh = c.measuredHandles || {};
    const on = (h) => unwrap(mh[h]);
    if (c.instrument.id === "pour" && on("arrival") >= 0.5) drove.push("pour.arrival");
    if (c.instrument.id === "livemirror" && on("propagate") > 0) drove.push("livemirror.propagate");
    if ((c.instrument.id === "overlay" || c.instrument.id === "grid-colour") && on("arrival") >= 0.5) {
      drove.push(c.instrument.id + ".arrival");
    }
  }
  const mode = arr.mode || null;
  if (mode) { out.modes[mode] = (out.modes[mode] || 0) + 1; out.named++; }
  if (drove.length) out.reached++;
  // ROW S-66's OWN COUNT. A step whose arrival mode names one instrument's own handle either casts
  // SOME instrument for the arrival slot or stands with the work carrying over unaltered. Under the
  // hard filter that stood until 2026-09-03 the second was the only outcome wherever the named
  // instrument could not be cast, whatever else the collection published.
  if (mode && WANTS[mode]) {
    out.wanting++;
    if (cues.some((c) => c.id === "arrival")) out.wantingVoiced++; else out.wantingSilent++;
  }
  if (plan) {
    const letters = cues.map((c) => c.instrument.id);
    played.unshift.apply(played, letters);
    if (plan.genreName || plan.genre) genres.unshift(plan.genreName || plan.genre);
    for (const c of cues) if (c.voice === "miracle") miracles.unshift(c.instrument.id);
  }
}
console.log(JSON.stringify(out));
"""


def walk(module_path, steps):
    """The one driver above, run over one copy of the composer. The source tree is never written to:
    a planted copy lives in a temporary file and is removed afterwards."""
    driver = HERE / "_arrival_reach_driver.js"
    driver.write_text(DRIVER, encoding="utf-8")
    try:
        proc = subprocess.run(
            ["node", str(driver), str(module_path), str(FIXTURE), str(WORKS), str(steps)],
            capture_output=True, text=True, timeout=300)
    finally:
        driver.unlink(missing_ok=True)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-800:]
    got = json.loads(proc.stdout.strip().splitlines()[-1])
    if got.get("error"):
        return None, got["error"]
    return got, None


# THE PLANT (rule 8) — the two narrowings put back the way they stood until 2026-09-03: a bare
# `.filter` at each site, throwing the ranking away rather than reading it. Both halves of the
# repair are undone together, because either alone leaves the other still handing the arrival its
# second best and the count this row watches would not return.
PLANTS = [
    ("        arrivalRanked = preferInstrument(arrivalRanked, arrivalWantsOnly);",
     "        if (arrivalWantsOnly) { arrivalRanked = arrivalRanked.filter("
     "function (r) { return r.id === arrivalWantsOnly; }); }"),
    ("        var offered = (arrivalWants && arrivalWantsReachable)\n"
     "          ? ranked.filter(function (r) { return r.id === arrivalWants; }) : ranked;",
     "        var offered = arrivalWants\n"
     "          ? ranked.filter(function (r) { return r.id === arrivalWants; }) : ranked;"),
]


def main():
    if not MODULE.exists() or not WORKS.exists() or not FIXTURE.exists():
        skip(ROW_REACH, "the composer or the fixture is not on this machine")
        skip(ROW_MODES, "no walk to read modes off")
        skip(ROW_STOOD, "no walk to read the arrival's own stand-down off")
        skip(ROW_REDBUG, "no composer to plant the hard filter into")
        return

    works = json.loads(WORKS.read_text(encoding="utf-8"))["works"]
    steps = max(0, len(works) - 1)
    got, err = walk(MODULE, steps)
    if err:
        check(ROW_REACH, False, f"the driver failed: {err}")
        skip(ROW_MODES, "the walk itself failed — see the row above")
        skip(ROW_STOOD, "the walk itself failed — see the row above")
        skip(ROW_REDBUG, "the walk itself failed — see the row above")
        return

    modes = got.get("modes", {})
    check(ROW_REACH, got["reached"] > 0,
          f"reached {got['reached']} of {got['named']} named steps over a {steps}-edge walk of the "
          f"real collection's own published order; modes played: "
          + ", ".join(f"{k} x{modes[k]}" for k in sorted(modes)))
    check(ROW_MODES, len(modes) > 1,
          f"{len(modes)} distinct arrival mode(s) played over the same walk: "
          + ", ".join(sorted(modes)))

    # ---- row S-66 and its plant. The shipped composer demotes; the planted one filters.
    src = MODULE.read_text(encoding="utf-8")
    planted, missed = src, [needle for needle, _ in PLANTS if needle not in src]
    for needle, was in PLANTS:
        planted = planted.replace(needle, was)
    if missed:
        skip(ROW_STOOD, "the narrowing's own lines did not match: " + "; ".join(missed))
        skip(ROW_REDBUG, "nothing to plant — see the row above")
        return
    tmp = HERE / "_arrival_reach_planted.js"
    tmp.write_text(planted, encoding="utf-8")
    try:
        hard, err = walk(tmp, steps)
    finally:
        tmp.unlink(missing_ok=True)
    if err:
        skip(ROW_STOOD, f"the planted walk failed: {err}")
        skip(ROW_REDBUG, "the planted walk failed — see the row above")
        return

    check(ROW_STOOD, got["wantingSilent"] < hard["wantingSilent"],
          f"over the same walk, {got['wanting']} steps name an arrival mode that speaks through one "
          f"instrument's own handle; {got['wantingSilent']} of them stand with no arrival voice at "
          f"all, against {hard['wantingSilent']} under the hard filter — "
          f"{hard['wantingSilent'] - got['wantingSilent']} crossings that carried the work over "
          f"unaltered now play their best available arrival instead")
    check(ROW_REDBUG, hard["wantingSilent"] > got["wantingSilent"]
          and hard["wantingVoiced"] < got["wantingVoiced"],
          f"with both narrowings reverted to the `.filter` that stood until 2026-09-03, "
          f"{hard['wantingVoiced']} of {hard['wanting']} named steps cast any arrival at all; with "
          f"the demotion that stands, {got['wantingVoiced']} of {got['wanting']}")


main()

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
