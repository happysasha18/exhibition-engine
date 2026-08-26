#!/usr/bin/env python3
"""dump_pass_cooldown_walk — the S-19 naряд's own before/after: what the letter cooldown inside
`dieWeighted` (engine/assets/pass-composer.js) does to a road's weight on a LONG visit, read off the
SHIPPED module twice — once with its ratio taken over the walk's raw log length (`n = the log's own
length`, the formula standing before 2026-08-26) and once over the walk's DISTINCT letters
(`n = walkPlayedDistinct.length`, the formula standing after).

THE SCENARIO IS THE FILE'S OWN. `walkPlayed`'s own comment names the failure this cooldown exists
to correct: "a letter that suits a whole collection well carried step after step of one route." So
the walk built below is exactly that — the pair's own best-fit road, played over and over because it
keeps winning the die — and what is measured is what happens to THAT road's own weight as the visit
carries on, against a rival of some fixed, unrelated fit that the visit has simply never played.

WHAT THIS IS NOT. The arithmetic proof of the fix is `coolFactor`/`walkCooldown`, exported from the
module and swept over their whole domain in tests/test_pass_composed.py's row 8j-2 — that is what
CLOSES the hole, by construction, not anything this script measures. This script is the reading a
person looks at: the same die, on records already on disk, so the numbers below ride the actual
wire rather than a hand-picked pair of fits. It does not replace his own look at the moving page —
it is the arithmetic that stood behind that motion, not the motion itself.

Run: python3 tests/dump_pass_cooldown_walk.py
Writes tests/pass_cooldown_before_after.txt beside its stdout.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE.parent / "engine" / "assets" / "pass-composer.js"
FIXTURE = HERE / "fixture_pass_composed.json"
WORKS = HERE / "fixture_pass_works.json"
OUT_TXT = HERE / "pass_cooldown_before_after.txt"

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath, worksPath] = process.argv.slice(2);
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(1); }

const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const composer = joined.make(fix.consts);

function die(key) {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) { h = Math.imul(h ^ key.charCodeAt(i), 16777619) >>> 0; }
  return (h % 100000) / 100000 * 8;
}

// THE OLD RATIO, reimplemented here rather than read off the shipped module — the module no longer
// computes a cooldown this way, on purpose, so this is the historical formula frozen for the
// comparison, not a second copy of anything still live.
function oldCoolFactor(at, rawLen) {
  return at < 0 ? 1 : (at + 1) / (rawLen + 1);
}

// THREE SYNTHETIC PAIRS — synthetic in the sense the naряд asks for: not a walk anyone actually
// took, but three ordered pairs spread across the 121 real work records this tree ships, so the FIT
// numbers below are the module's own, on real records, and only the WALK MEMORY handed in is
// invented for the demonstration.
const ids = Object.keys(works).sort();
const PAIRS = [[ids[0], ids[1]], [ids[40], ids[41]], [ids[80], ids[81]]];

const report = {pairs: [], floorAsVisitGrows: []};

for (const [aId, bId] of PAIRS) {
  const A = works[aId], B = works[bId];
  const seed = die(aId + "__" + bId + "__ab");
  const p = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b", seed,
                                  routeRole: "middle"});
  if (!p.ranking) { report.pairs.push({pair: [aId, bId], error: p.declined || "no ranking"}); continue; }
  const ranking = p.ranking.slice(); // sorted best fit first, all 8 roads always present
  const target = ranking[0];               // the road THIS PAIR suits best
  const rival = ranking.slice().reverse().find((r) => r.fit > 0) || ranking[ranking.length - 1];

  // THE WALK: the pair's own best-suited road, played on every passage of a visit that keeps
  // returning to it because it keeps winning the die — `walkPlayed`'s own comment names exactly
  // this as the failure the cooldown exists to correct. `rival` never plays at all, which is the
  // ordinary case `coolOf`/`viewerBiasOf` already read as neutral (weight 1) on every request.
  const crossovers = {before: null, after: null};
  const rows = [];
  for (const visits of [1, 5, 20, 50, 100, 300, 1000]) {
    const logLen = visits;
    const before = target.fit * oldCoolFactor(0, logLen);
    const targetLog = new Array(visits).fill(target.genre);
    const after = target.fit * composer.walkCooldown(targetLog, target.genre);
    if (crossovers.before === null && before < rival.fit) crossovers.before = visits;
    if (crossovers.after === null && after < rival.fit) crossovers.after = visits;
    rows.push({visits, targetWeightBefore: Math.round(before * 1e6) / 1e6,
               targetWeightAfter: Math.round(after * 1e6) / 1e6});
  }
  report.pairs.push({pair: [aId, bId], target: target.genre, targetFit: target.fit,
                      rival: rival.genre, rivalFit: rival.fit, rows, crossovers});
}

// THE FLOOR ITSELF, AS THE VISIT GROWS — the SAME road, played on every passage so far (the
// pathological case `walkPlayed`'s own comment names), read at growing visit lengths. `before at=0`
// is `1/(visits+1)`: no floor, it keeps falling. `after at=0` is `coolFactor(0, 1)` — the log names
// one distinct letter whatever `visits` is — and does not move.
for (const visits of [1, 8, 40, 160, 800, 4000]) {
  const targetLog = new Array(visits).fill("target");
  report.floorAsVisitGrows.push({
    visits,
    before: Math.round(oldCoolFactor(0, visits) * 1e8) / 1e8,
    after: composer.walkCooldown(targetLog, "target"),
  });
}

console.log(JSON.stringify(report));
"""


def main():
    driver_path = HERE / "_dump_pass_cooldown_walk_driver.js"
    driver_path.write_text(DRIVER)
    try:
        proc = subprocess.run(["node", str(driver_path), str(MODULE), str(FIXTURE), str(WORKS)],
                               capture_output=True, text=True)
    finally:
        driver_path.unlink(missing_ok=True)
    if proc.returncode != 0 or not proc.stdout.strip():
        sys.stderr.write(proc.stdout + proc.stderr)
        sys.exit(1)
    report = json.loads(proc.stdout.strip().splitlines()[-1])

    lines = []

    def out(s=""):
        lines.append(s)

    out("S-19 - the letter cooldown's floor, before and after 2026-08-26")
    out("=" * 72)
    out("")
    out("weight = fit * cooldown(at, poolSize); cooldown = 1 if at < 0 (never played),")
    out("else (at+1)/(poolSize+1).")
    out("BEFORE: poolSize = the walk's raw log length (grows without end as a visit runs).")
    out("AFTER:  poolSize = the walk's DISTINCT letters (bounded by the vocabulary in play).")
    out("")
    out("-- 1. THE FLOOR ITSELF, AS THE SAME ROAD KEEPS BEING PLAYED " + "-" * 12)
    out("The pair's own favourite road, played on every passage of the visit so far (the exact")
    out("failure walkPlayed's own comment names: 'a letter that suits a whole collection well")
    out("carried step after step of one route'). Column shown: what fraction of its own fit that")
    out("road's weight keeps, played most recently, as the visit lengthens.")
    out("")
    out(f"{'visits so far':>14} | {'before (raw length)':>20} | {'after (distinct=1)':>19}")
    for row in report["floorAsVisitGrows"]:
        out(f"{row['visits']:>14} | {row['before']:>20} | {row['after']:>19}")
    out("")
    out("The 'before' column has no floor: it halves roughly every doubling of the visit and")
    out("keeps falling for as long as the visit runs. The 'after' column is exactly 0.5 at every")
    out("length, because one road played any number of times is still ONE distinct letter.")
    out("")
    out("-- 2. WHEN A NEVER-PLAYED RIVAL OVERTAKES THE FAVOURITE " + "-" * 16)
    out("Same walk (the pair's own best-fit road, played on every passage so far) against a rival")
    out("of fixed, lower fit that the visit has simply never played (cooldown neutral, weight =")
    out("its own fit throughout — the ordinary case for a road no walk has touched). 'crossover'")
    out("is the first visit length at which the rival's fixed weight overtakes the favourite's.")
    out("")
    for pr in report["pairs"]:
        if "error" in pr:
            out(f"pair {pr['pair']}: declined - {pr['error']}")
            continue
        out(f"pair {pr['pair'][0]} -> {pr['pair'][1]}")
        out(f"  favourite = {pr['target']} (fit {pr['targetFit']}), "
            f"never-played rival = {pr['rival']} (fit {pr['rivalFit']})")
        out(f"  {'visits':>7} | {'favourite weight before':>24} | {'favourite weight after':>23}")
        for r in pr["rows"]:
            out(f"  {r['visits']:>7} | {r['targetWeightBefore']:>24} | {r['targetWeightAfter']:>23}")
        cb = pr["crossovers"]["before"]
        ca = pr["crossovers"]["after"]
        out(f"  crossover before: {'visit ' + str(cb) if cb else 'not reached by visit 1000'} "
            f"-- the favourite loses to the never-played rival once the visit runs that long")
        out(f"  crossover after:  {'visit ' + str(ca) if ca else 'never, at any visit length'} "
            f"-- whether it can lose depends only on the two fits, never on how long the visit runs")
        out("")

    text = "\n".join(lines) + "\n"
    OUT_TXT.write_text(text)
    sys.stdout.write(text)
    print(f"[written to {OUT_TXT}]")


if __name__ == "__main__":
    main()
