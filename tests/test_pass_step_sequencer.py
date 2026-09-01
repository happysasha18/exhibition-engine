#!/usr/bin/env python3
"""PASS-STEP-SEQUENCER (shelf 18, the 2026-09-01 repair) — «playing whole operations one after
another, each from start to finish, is banned — that is the step sequencer he rejected in the first
transit.js build» (`~/tlvphotos/lab/CROSSING-HISTORY.md`, the crossing's own root brief). The
charter's positive law is the same sentence's other half: «several operations are alive at once
while parameters travel». Of the charter's bans (shelf 18), this is the one on record three times
(transit.js, the field deck, batch 1) and, until this file, the one no row in the suite would notice
returning — a plan could sequence its travel and its arrival, closing one before opening the other,
and every existing test stayed green.

Run: python3 tests/test_pass_step_sequencer.py

THE CHECK NEEDS NO EXECUTION OF THE HOST'S OWN CURVE MATH: `buildTemplate` already publishes each
cue's own `window`, in seconds, on the composed plan (`p.plan.cues[i].window`) — the pivot always
`[0, duration]` (the ground never sequences, by construction), the travel and the arrival each their
own sub-span. Two cues overlap, in the charter's own sense, exactly when the later one opens before
the earlier one closes; this file reads that off the plan directly, over real pairs from the 121-work
fixture, the shipped composer, unmodified.

WHAT THIS HUNT FOUND, AND WHY THE ROW BELOW IS WRITTEN AS IT IS. Over every ordered real pair this
file could compose (4 seeds each, capped for run time), of the crossings that cast BOTH a travelling
move and an arrival, 541 of 1661 — a third — open the arrival only after the travelling move has
already closed, some by several seconds inside a passage a few seconds long: `travel` plays start to
finish, falls silent, and only then does `arrival` begin. That is the step sequencer, present on real
data, today, in the shipped composer — not a defect this file invents to prove itself. Silencing this
row (weakening the assertion until it is green) would be exactly the failure item 1 above was built to
stop happening again to shelf 7; this row is written to red on that real condition and stay red until
`arrivalOpenBase`'s own derivation (`pass-composer.js`, the block feeding `cueWindows`) is repaired to
guarantee the overlap the charter asks for — a repair this phase's own write-set does not reach (an
enforcer for a promise, per this phase's own title, not a rewrite of the timing derivation the promise
is a promise about). The row's own detail names every violating pair so the repair has a real list to
work from rather than a percentage.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = HERE / "fixture_pass_composed.json"
WORKS = HERE / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROW_OVERLAP = "PASS-STEP-SEQUENCER no real three-voice crossing opens its arrival only after its " \
              "travelling move has already closed (shelf 18, «playing whole operations one after " \
              "another... is banned»)"
ROW_REDBUG = "PASS-STEP-SEQUENCER RED-ON-BUG · this same row catches a planted arrival delayed " \
             "past the travel's own close"

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath, worksPath, capArg] = process.argv.slice(2);
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(0); }
const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const composer = joined.make(fix.consts);
const ids = Object.keys(works);
function unwrap(v) { return (v && typeof v === "object" && "v" in v) ? v.v : v; }
const CAP = parseInt(capArg, 10);
let examined = 0, threeVoice = 0, gaps = [];
outer:
for (let i = 0; i < ids.length && examined < CAP; i++) {
  for (let j = 0; j < ids.length && examined < CAP; j++) {
    if (i === j) continue;
    for (const seed of [0, 1, 2, 3]) {
      examined++;
      if (examined >= CAP) break outer;
      const from = ids[i], to = ids[j];
      let p;
      try { p = composer.passageFor({workRecordA: works[from], workRecordB: works[to],
                                      direction: "a-to-b", seed}); }
      catch (e) { continue; }
      const cues = (p && p.plan && p.plan.cues) || [];
      const byId = {}; cues.forEach((c) => { byId[c.id] = c; });
      if (!byId.travel || !byId.arrival) continue;
      threeVoice++;
      const tw = byId.travel.window.map(unwrap), aw = byId.arrival.window.map(unwrap);
      if (!(aw[0] < tw[1])) gaps.push({from, to, seed, travel: tw, arrival: aw,
                                        gap: Number((aw[0] - tw[1]).toFixed(4))});
    }
  }
}
console.log(JSON.stringify({examined, threeVoice, gaps}));
"""


def run(composer_path, cap):
    driver = HERE / "_step_sequencer_driver.js"
    driver.write_text(DRIVER, encoding="utf-8")
    try:
        proc = subprocess.run(["node", str(driver), str(composer_path), str(FIXTURE), str(WORKS),
                               str(cap)], capture_output=True, text=True, timeout=300)
    finally:
        driver.unlink(missing_ok=True)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-800:]
    got = json.loads(proc.stdout.strip().splitlines()[-1])
    if got.get("error"):
        return None, got["error"]
    return got, None


def main():
    if not COMPOSER.exists() or not WORKS.exists() or not FIXTURE.exists():
        skip(ROW_OVERLAP, "the composer or the fixture is not on this machine")
        skip(ROW_REDBUG, "no composer to plant a copy of")
        return

    CAP = 5000
    got, err = run(COMPOSER, CAP)
    if err:
        check(ROW_OVERLAP, False, f"the driver failed: {err}")
    else:
        gaps = got["gaps"]
        check(ROW_OVERLAP, len(gaps) == 0,
              f"{got['threeVoice']} real three-voice crossings composed (of {got['examined']} "
              f"ordered pair/seed combinations examined); {len(gaps)} open the arrival only after "
              f"the travelling move already closed — a real, currently-unrepaired step-sequencer "
              f"gap this row now names rather than leaving invisible; first 3: "
              + json.dumps(gaps[:3]))

    # ---- red on bug: a copy of the composer with the arrival's own open forced past the travel's
    # close on every crossing that carries both — proving this row catches the class of defect it
    # names, independent of whether the shipped code above happens to clear it on a given pair.
    src = COMPOSER.read_text(encoding="utf-8")
    needle = "var arrivalWindowBound = [arrivalOpenAtR, 1.0];"
    if needle not in src:
        check(ROW_REDBUG, False, "the plant found nothing to change")
        return
    plant_line = ("var arrivalWindowBound = [arrivalOpenAtR, 1.0]; "
                  "arrivalOpenAtR = Math.min(0.999, Math.max(arrivalOpenAtR, beforeAtR + 0.9)); "
                  "arrivalWindowBound = [arrivalOpenAtR, 1.0];")
    mutated = src.replace(needle, plant_line, 1)
    planted = HERE / "_step_sequencer_planted.js"
    planted.write_text(mutated, encoding="utf-8")
    try:
        got2, err2 = run(planted, 400)
    finally:
        planted.unlink(missing_ok=True)
    if err2:
        check(ROW_REDBUG, False, f"the planted driver failed: {err2}")
        return
    check(ROW_REDBUG, got2["threeVoice"] > 0 and len(got2["gaps"]) > 0,
          f"with the arrival's own open forced 0.9s past the room the travelling move already "
          f"established, {len(got2['gaps'])} of {got2['threeVoice']} three-voice crossings among "
          f"the first {got2['examined']} pair/seed combinations now open their arrival after the "
          f"travelling move has closed")


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
