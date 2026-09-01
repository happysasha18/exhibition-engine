#!/usr/bin/env python3
"""PASS-POLYPHONY-PRESENCE (shelf 4, the 2026-09-01 repair) — every polyphony row this plan's own
matrix already carries is about voices NOT colliding (`ownTheLevels`, the five bundle rules). Shelf
4's own content is that voices DO overlap — B enters quietly while A still sounds — and until this
file nothing made that a REQUIREMENT rather than Phase 10's own reported number.

Run: python3 tests/test_pass_polyphony_presence.py

WHY THIS IS A PER-CROSSING STRUCTURAL CHECK AND NOT A FLEET RATE. A gate on «the second-voice rate
must clear N% of the 121-work fleet» is exactly the class this project's own standing law forbids —
a threshold computed across the photograph collection, the same shape the Phase 9 «top-quartile»
cutoff was struck for. So this row asks a different, construction-derived question of EACH crossing
on its own: `scoreBundle`'s own comment already states the law in plain words — «among LEGAL
bundles, one that keeps a move is never outscored by one that drops it» — so wherever the joint
bundle planner's own ledger (`p.diagnostics.bundles.considered`, every candidate this walk actually
ranked, each with its own legal/refused reading) shows a LEGAL bundle carrying MORE live voices than
the one the plan actually seats, that single crossing is the violation, on its own terms, with no
population to average over. A crossing that legitimately has no second voice to offer never enters
this row's count at all — `considered` then has no legal bundle above the winner's own voice count,
which is the honest answer this row leaves alone.

WHAT THIS FILE FOUND ON REAL DATA. `scoreBundle`'s OWN dominant/second-voice preference
(`if (routeFunction === "dominant" && secondVoice) score += 10;`) turns out to be inert on the real
fixture: removing it changes not one winner across 1999 real culmination-role crossings, because the
`voicesPresent * 100` term this same function's comment calls «the dominant term» already decides
every one of those cases outright — the `+10` only ever mattered among bundles ALREADY tied on voice
count, which the dominant term makes rare. This is not the bug shelf 4 names (the presence law
already holds structurally, checked below); it is a separate, minor finding, left in the code as
found rather than removed here, since a dead ten points scores no crossing wrong.
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


ROW_PRESENCE = "PASS-POLYPHONY-PRESENCE no real culmination-role crossing seats fewer live voices " \
               "than a LEGAL bundle in its own ledger offered (shelf 4's presence law, per crossing)"
ROW_REDBUG = "PASS-POLYPHONY-PRESENCE RED-ON-BUG · weakening the voice-count term below the tie-" \
             "break noise floor is caught by this same row"

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
const CAP = parseInt(capArg, 10);
let examined = 0, checked = 0, violations = [];
outer:
for (let i = 0; i < ids.length && examined < CAP; i++) {
  for (let j = 0; j < ids.length && examined < CAP; j++) {
    if (i === j) continue;
    examined++;
    if (examined >= CAP) break outer;
    const from = ids[i], to = ids[j];
    let p;
    try { p = composer.passageFor({workRecordA: works[from], workRecordB: works[to],
                                    direction: "a-to-b", seed: examined % 8, role: "culmination"}); }
    catch (e) { continue; }
    const b = p && p.diagnostics && p.diagnostics.bundles;
    if (!b || !b.considered || !b.considered.length) continue;
    checked++;
    const legal = b.considered.filter((r) => r.ok);
    if (!legal.length) continue;
    const voicesOf = (r) => (r.travel ? 1 : 0) + (r.arrival ? 1 : 0);
    const maxVoices = Math.max(...legal.map(voicesOf));
    const cues = (p.plan && p.plan.cues) || [];
    const winnerVoices = cues.filter((c) => c.id !== "pivot").length;
    if (winnerVoices < maxVoices) {
      violations.push({from, to, maxVoices, winnerVoices});
    }
  }
}
console.log(JSON.stringify({examined, checked, violations}));
"""


def run(composer_path, cap):
    driver = HERE / "_polyphony_presence_driver.js"
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
        skip(ROW_PRESENCE, "the composer or the fixture is not on this machine")
        skip(ROW_REDBUG, "no composer to plant a copy of")
        return

    CAP = 2000
    got, err = run(COMPOSER, CAP)
    if err:
        check(ROW_PRESENCE, False, f"the driver failed: {err}")
    else:
        v = got["violations"]
        check(ROW_PRESENCE, len(v) == 0,
              f"{got['checked']} real culmination-role crossings read a bundle ledger (of "
              f"{got['examined']} ordered pair/seed combinations examined); {len(v)} seated fewer "
              f"live voices than a legal alternative in their own ledger"
              + (f"; first: {v[0]}" if v else ""))

    src = COMPOSER.read_text(encoding="utf-8")
    needle = "var voicesPresent = (t ? 1 : 0) + (a ? 1 : 0);\n      var score = voicesPresent * 100;"
    if needle not in src:
        check(ROW_REDBUG, False, "the plant found nothing to change")
        return
    mutated = src.replace(
        needle, "var voicesPresent = (t ? 1 : 0) + (a ? 1 : 0);\n      var score = voicesPresent * 1;",
        1)
    planted = HERE / "_polyphony_presence_planted.js"
    planted.write_text(mutated, encoding="utf-8")
    try:
        got2, err2 = run(planted, CAP)
    finally:
        planted.unlink(missing_ok=True)
    if err2:
        check(ROW_REDBUG, False, f"the planted driver failed: {err2}")
        return
    v2 = got2["violations"]
    check(ROW_REDBUG, len(v2) > 0,
          f"with the voice-count term weakened from 100 to 1 a crossing, {len(v2)} of "
          f"{got2['checked']} real crossings now seat fewer voices than a legal alternative offered "
          f"(the row above read {len(got['violations']) if not err else '?'} on the unplanted "
          f"composer)")


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
