#!/usr/bin/env python3
"""PASS-ARRIVAL-ARC (P1.1/A4) — no collapsed arrival, as a visual invariant.

Run: python3 tests/test_pass_arrival_arc.py

Root: this наряд's own file:line evidence. `pass-composer.js` reads
`baseArrivalOpen = r4(1 - locusFit * (1 - beforeAtR))` — at `locusFit === 0` this is exactly `1.0`,
and even away from zero it runs to `1.0` whenever `beforeAtR` (the room the travelling move already
used) itself stands close to `1.0`, because `(1 - beforeAtR)` is what `locusFit` has to work with.
Either way the arrival cue's own `window` — `[arrivalOpenAtR, 1.0]` in the fraction the composer
reasons in, converted to seconds once the pass's own duration is chosen (`fillPlan`) — can run to a
zero or near-zero length: a flash rather than a crossing, in violation of the charter's own seam ("A
hang → one continuous passage → exact B hang", no cut, no collapse).

THE FIX IS A VISUAL INVARIANT, NOT A TYPED MINIMUM. `fillPlan` now widens the arrival's own OPEN end
(never the close, which always sits at the pass's own end) so its span is never under the device's
OWN measured frame gap — `pass-layer.js`'s rolling buffer, published as `report().frames.p95` and
threaded onto the composer's request as `framePace` (`01a-pass.js`'s `passRequestFor`). No number is
typed anywhere in the fix: the bound is read off the device, and a device with no reading yet (a
cold visit, `framePace: null`) widens nothing, which is the honest answer.

WHAT THIS FILE MEASURES. It runs the shipped composer directly (Node's `vm`, the same technique
`tests/dump_pass_arrival_walk.py` already uses to run it outside a browser) over the real 121-work
fixture collection, hunting real pairs and seeds whose arrival window collapses to under 20ms with
NO frame-pace reading supplied — the naturally-occurring defect, not a fabricated one — and then
re-composes each one WITH a stated frame pace and checks the arrival's own span widened to at least
that measured gap, its open end only, its close end untouched. If the sweep below finds no naturally
collapsing pair in this fixture, the row says so and skips rather than manufacturing one: the defect
is a property of the pair, not of this file.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
WORKS = HERE / "fixture_pass_works.json"

# A REALISTIC READING, IN THE SHAPE `pass-layer.js` PUBLISHES IT — not a bound this file invents for
# the RUNTIME (the runtime reads the device's own live number), only a stated INPUT this file hands
# the composer to prove the wiring, at a p95 this project's own tests/test_pass_hang.py already
# documents from a real loaded machine ("50 ms when a frame stalls on an idle machine and passes
# 200 ms on a loaded one") — 100ms, comfortably inside that measured range rather than a fresh guess.
FRAME_PACE = {"count": 240, "p95": 100.0, "p50": 33.0}
# THE SWEEP'S OWN HUNTING THRESHOLD IS THE SAME NUMBER THE FIX ITSELF WOULD ACT ON — a span already
# shorter than this device's own p95 IS the collapse the fix exists to widen, so hunting for exactly
# that condition (rather than some separate hand-picked cutoff) is what makes a find here a real,
# unforced proof that the fixture actually exercises the defect.
COLLAPSE_UNDER_MS = FRAME_PACE["p95"]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROW_FOUND = "PASS-ARRIVAL-ARC the sweep finds a real pair/seed whose arrival window collapses with " \
            "no frame-pace reading"
ROW_WIDENED = "PASS-ARRIVAL-ARC that same pair widens its arrival's OPEN end to the device's own " \
              "measured frame gap once one is supplied, the close end untouched"
ROW_COLD = "PASS-ARRIVAL-ARC a cold visit with no frame-pace reading yet widens nothing (never a " \
           "typed number standing in for a measurement)"

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, worksPath, framePaceJson, collapseUnderSec] = process.argv.slice(2);
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(1); }

const fix = JSON.parse(fs.readFileSync(worksPath, "utf8"));
const works = fix.works;
const framePace = JSON.parse(framePaceJson);
const underSec = parseFloat(collapseUnderSec);
const ids = Object.keys(works);

// A CUE'S NUMBERS TRAVEL WRAPPED (`{v: <number>}`, `flt()` in pass-composer.js) so the writer that
// serialises a plan to disk can tell a float from an int; `unwrap` is the same one-line read
// `tests/dump_pass_arrival_walk.py` already uses for the same reason.
function unwrap(v) { return (v && typeof v === "object" && "v" in v) ? v.v : v; }
function arrivalWindow(composer, req) {
  let p = null;
  try { p = composer.passageFor(req); } catch (e) { return {error: String((e && e.message) || e)}; }
  const cues = (p && p.plan && p.plan.cues) || [];
  const c = cues.filter((x) => x.id === "arrival")[0];
  const w = c ? [unwrap(c.window[0]), unwrap(c.window[1])] : null;
  return {window: w, declined: (p && p.declined) || null};
}

// ---- the hunt: a FRESH composer, framePace NEVER supplied, so `lastFramePace` never leaves null --
// Capped rather than exhaustive (121 works squared, times several seeds, is minutes of composing a
// row has no business spending): the search stops at the first hit, or once ATTEMPT_CAP pairs have
// been read with none, which is itself a fact this row reports honestly rather than papering over
// with a smaller, hand-picked collection.
const ATTEMPT_CAP = 6000;
const SEEDS = [0, 2, 4, 6];
const scoutComposer = joined.make(fix.consts);
let found = null, attempts = 0;
outer:
for (let i = 0; i < ids.length && !found; i++) {
  for (let j = 0; j < ids.length; j++) {
    if (i === j) continue;
    const from = ids[i], to = ids[j];
    const forward = String(from) <= String(to);
    for (const s of SEEDS) {
      if (attempts++ >= ATTEMPT_CAP) break outer;
      const req = {
        workRecordA: works[forward ? from : to], workRecordB: works[forward ? to : from],
        direction: forward ? "a-to-b" : "b-to-a", seed: s,
      };
      const got = arrivalWindow(scoutComposer, req);
      if (got.window && (got.window[1] - got.window[0]) < underSec) {
        found = {from: from, to: to, direction: req.direction, seed: s, before: got.window};
        break outer;
      }
    }
  }
}

const out = {found: found};
if (found) {
  const req = {
    workRecordA: works[found.direction === "a-to-b" ? found.from : found.to],
    workRecordB: works[found.direction === "a-to-b" ? found.to : found.from],
    direction: found.direction, seed: found.seed,
  };
  // ---- a FRESH composer for the "with a reading" case, so nothing scouted above leaks into it ----
  const warmComposer = joined.make(fix.consts);
  const withPace = arrivalWindow(warmComposer, Object.assign({}, req, {framePace: framePace}));
  out.after = withPace.window;
  // ---- and a FRESH composer again for the cold-visit case: no reading, same pair -----------------
  const coldComposer = joined.make(fix.consts);
  const cold = arrivalWindow(coldComposer, Object.assign({}, req, {framePace: null}));
  out.cold = cold.window;
}
console.log(JSON.stringify(out));
"""


def main():
    if not MODULE.exists() or not WORKS.exists():
        skip(ROW_FOUND, "the composer or the fixture works are not on this machine")
        skip(ROW_WIDENED, "no sweep to read a widened pair off")
        skip(ROW_COLD, "no sweep to read a cold visit off")
        return

    driver = HERE / "_arrival_arc_driver.js"
    driver.write_text(DRIVER, encoding="utf-8")
    try:
        proc = subprocess.run(
            ["node", str(driver), str(MODULE), str(WORKS), json.dumps(FRAME_PACE),
             str(COLLAPSE_UNDER_MS / 1000.0)],
            capture_output=True, text=True, timeout=180)
    finally:
        driver.unlink(missing_ok=True)

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout)[-800:]
        check(ROW_FOUND, False, f"the driver failed: {detail}")
        skip(ROW_WIDENED, "the sweep itself failed — see the row above")
        skip(ROW_COLD, "the sweep itself failed — see the row above")
        return

    got = json.loads(proc.stdout.strip().splitlines()[-1])
    if got.get("error"):
        check(ROW_FOUND, False, got["error"])
        skip(ROW_WIDENED, "the module never joined — see the row above")
        skip(ROW_COLD, "the module never joined — see the row above")
        return

    found = got.get("found")
    if not found:
        skip(ROW_FOUND,
             f"no pair/seed among the {WORKS.name} collection collapsed under "
             f"{COLLAPSE_UNDER_MS}ms with no frame-pace reading in this run — the sweep found "
             f"nothing to prove the fix against, which is a fact about this fixture rather than "
             f"a red or a green")
        skip(ROW_WIDENED, "no collapsing pair found — see the row above")
        skip(ROW_COLD, "no collapsing pair found — see the row above")
        return

    before = found["before"]
    check(ROW_FOUND, True,
          f"{found['from']} -> {found['to']} ({found['direction']}, seed {found['seed']}): "
          f"the arrival's own window read {before}, {before[1] - before[0]:.4f}s wide, with no "
          f"frame-pace reading supplied")

    after = got.get("after")
    min_span = FRAME_PACE["p95"] / 1000.0
    widened = (isinstance(after, list) and len(after) == 2
               and after[1] == before[1]                       # the close end never moved
               and after[0] <= before[0]                        # the open end only ever widens
               and (after[1] - after[0]) >= min_span - 1e-9)
    check(ROW_WIDENED, widened,
          f"before={before} (span {before[1]-before[0]:.4f}s), after={after} "
          f"(span {(after[1]-after[0]) if isinstance(after, list) else None}), "
          f"the device's own measured gap: {min_span:.4f}s (p95 of {FRAME_PACE})")

    cold = got.get("cold")
    check(ROW_COLD, cold == before,
          f"the same pair recomposed with framePace:null reads {cold} — unwidened, exactly the "
          f"reading with no measurement supplied ({before}), since a measurement ranks and "
          f"parameterises and never gates, and a cold visit has nothing to widen against")


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
