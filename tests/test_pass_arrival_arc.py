#!/usr/bin/env python3
"""PASS-ARRIVAL-ARC (P1.1/A4) — no collapsed arrival, as a visual invariant.

Run: python3 tests/test_pass_arrival_arc.py

Root: this наряд's own file:line evidence. `pass-composer.js` reads
`baseArrivalOpen = r4(arrivalRoomEnd - locusFit * (arrivalRoomEnd - beforeAtR))`, so the arrival's
own published span is `(1 - arrivalRoomEnd) + locusFit * (arrivalRoomEnd - beforeAtR)` of the pass.
Where no travelling voice plays `arrivalRoomEnd` is the pass's own end and that reads `locusFit`
alone: at `locusFit === 0` the window is exactly `[1.0, 1.0]`. Where one does play, the room's far
end is the travelling move's own close (`travelWindowBound[1]`, shelf 18's repair of 2026-09-01), so
the span cannot fall under what is left of the pass after that close — and a pair whose ground holds
strongly and whose axis reaches far hands its level back at the pass's own end, leaving nothing to
open in. Either way the arrival cue's own `window` — `[arrivalOpenAtR, 1.0]` in the fraction the
composer reasons in, converted to seconds once the pass's own duration is chosen (`fillPlan`) — can
run to a zero or near-zero length: a flash rather than a crossing, in violation of the charter's own
seam ("A hang → one continuous passage → exact B hang", no cut, no collapse).

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
that measured gap, its open end only, its close end untouched. The collapse is a property of the
pair, so this file never manufactures one — but a sweep that comes back empty is this row GOING
SILENT, not a green, and it is read below as a red (see the note over the sweep's own no-hit branch).

WHY THE SWEEP'S REACH MOVED (2026-09-02). It read four seeds — `0, 2, 4, 6`, a stride — and stopped
at a cap of 6000 ordered pair/seed combinations. Shelf 18's repair of 2026-09-01 widened every
three-voice arrival window by exactly `(1 - travelClose) * (1 - locusFit)` of the pass (the close of
the room moved from the pass's own end down onto the travelling move's own close, and the span is
what is left above it), which lifted the pair this row used to catch — `17843153263050281 ->
17992521517652668` — clear of the hunt. The first crossing this fixture still composes under a frame
gap sits on an ODD seed, so the stride read straight past it and the row skipped three rows without
one number changing in this file. The sweep now reads every seed the instruments' own manifests
declare (`seed: {min: 0, max: 8}` in `pass-inst-parquet.js`, `pass-inst-weave.js`, and their
siblings) rather than a stride across that span, and it finds a real collapse inside the first
hundred combinations.
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
// Capped rather than exhaustive (121 works squared, times every seed, is minutes of composing a row
// has no business spending): the search reads ATTEMPT_CAP ordered pair/seed combinations, which is
// itself a fact this row reports honestly rather than papering over with a smaller, hand-picked
// collection.
//
// IT READS THE WHOLE CAP AND KEEPS THE WORST COLLAPSE, rather than stopping at the first one.
// Stopping at the first hit made the row's own proof a matter of scan order: on 2026-09-02 the first
// crossing in reach was 0.0992s wide against a 0.1s frame gap, so the widening it proved moved the
// arrival's open by under a millisecond — a real check, but the thinnest one in the collection. The
// narrowest window the sweep can reach is where the fix has the most work to do and where a widening
// that quietly stopped happening shows up furthest from the threshold. The count of hits travels
// back with it, so a search thinning out toward silence is visible in the row's own detail line
// BEFORE it reaches zero and this row goes red.
const ATTEMPT_CAP = 6000;
// EVERY SEED THE INSTRUMENTS' OWN MANIFESTS DECLARE, not a stride across them. Each instrument
// publishes its die handle as `seed: {min: 0, max: 8}` (`pass-inst-parquet.js`, `pass-inst-weave.js`,
// `pass-inst-gates.js`, and the rest), so the integers a pass actually draws on are these, read off
// the engine rather than picked here. A stride over the even ones alone is what let this row's hunt
// walk past a real collapse and skip in silence — see the header.
const SEEDS = [0, 1, 2, 3, 4, 5, 6, 7];
const scoutComposer = joined.make(fix.consts);
let found = null, attempts = 0, hits = 0;
outer:
for (let i = 0; i < ids.length; i++) {
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
        hits++;
        if (!found || (got.window[1] - got.window[0]) < (found.before[1] - found.before[0])) {
          found = {from: from, to: to, direction: req.direction, seed: s, before: got.window};
        }
      }
    }
  }
}

// THE READ COUNT AND THE HIT COUNT TRAVEL BACK whether or not the hunt hit, so a row that goes
// silent can say how far it actually looked before it did — a bare "found nothing" hides whether the
// sweep exhausted its cap or fell over after two pairs — and a row that still hits can say whether
// it is hitting on many crossings or hanging on by one.
const out = {found: found, attempts: attempts, hits: hits};
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
        # A SWEEP THAT COMES BACK EMPTY IS THIS ROW GOING SILENT, AND IT SAYS SO OUT LOUD.
        # This used to skip, on the reasoning that the collapse is a property of the fixture rather
        # than of this file. That reasoning holds for the DEFECT and not for the ROW: this row's one
        # job is to prove the widening acts on a real crossing, and a search that returns nothing
        # proves nothing while still printing a suite the gate reads as [OK]. On 2026-09-02 that is
        # exactly what happened — shelf 18's repair lifted the one pair this hunt used to catch, the
        # three rows turned into three abstentions, and the gate went on reading them as fine.
        # So: empty is red. The repair is never to loosen the hunt's own threshold (that is the
        # device's own p95, and it is what the fix acts on) but to answer WHICH of the two happened —
        # the sweep's reach fell short of a collapse that is still there (widen the reach, as the
        # header records doing), or the composer's construction genuinely put the collapse out of
        # reach, in which case this row is replaced by a proof from the derivation itself rather
        # than left as a search that quietly gives up.
        check(ROW_FOUND, False,
              f"the sweep read {got.get('attempts')} ordered pair/seed combinations of the "
              f"{WORKS.name} collection and none collapsed under {COLLAPSE_UNDER_MS}ms with no "
              f"frame-pace reading — this row has nothing left to prove the widening against, "
              f"which is a red on the row and not a fact about the fixture; see the branch's own "
              f"note in this file for the two things it can mean and what each one asks for")
        skip(ROW_WIDENED, "no collapsing pair found — see the row above")
        skip(ROW_COLD, "no collapsing pair found — see the row above")
        return

    before = found["before"]
    check(ROW_FOUND, True,
          f"{found['from']} -> {found['to']} ({found['direction']}, seed {found['seed']}): "
          f"the arrival's own window read {before}, {before[1] - before[0]:.4f}s wide, with no "
          f"frame-pace reading supplied — the narrowest of {got.get('hits')} such crossings among "
          f"the {got.get('attempts')} ordered pair/seed combinations this sweep read")

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
