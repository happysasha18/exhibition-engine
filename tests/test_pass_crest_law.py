#!/usr/bin/env python3
"""PASS-CREST-LAW (shelf 15, the 2026-09-01 repair) — no LIVE surface ever freezes, checked over a
COMPOSED PLAN rather than one instrument at a time.

Run: python3 tests/test_pass_crest_law.py

ROOT. Charter shelf 15's crest law reads «no LIVE surface ever freezes» — the same family as his
2026-08-19 11:58 word, «nothing should be static», for which a per-handle check already exists
(`ownTheLevels`/`ownedTracks`, and per-instrument dead-band rows such as `test_pass_veil.py`'s own
red-on-bug over charter shelf 18's «full-frame freeze»). What is missing is the PLAN-LEVEL sibling:
a passage is composed from several cues at once (a ground, sometimes a travelling move, sometimes an
arrival), and nothing in the tree asked whether the WHOLE composed passage — every cue that is
actually live at a given instant, together — ever goes completely still while it plays.

THE ONE THING THIS FILE READS: `mix`, the door every cue publishes (`buildTemplate`'s own doors
contract) and the one handle every playing cue is guaranteed to carry a track for, driven by a
`{op: "mix", ..., t: {op: "curve", ..., in: {source: "cueProgress"}}}` node — a curve read straight
off `cueProgress`, so a cue whose `mix` genuinely stops answering to progress is a cue that has
stopped moving in the one respect every voice shares, whatever else its own content handles do (a
handle that is a fixed measured fact about one photograph — a period, a tilt, an axis — is not itself
a freeze; `test_pass_arrival_reach.py`'s own hunt found MOST structural handles across the fleet are
exactly such facts, driven once and never meant to travel, so gating on THEM read the wrong law).
Where the crest law's own legitimate suspension holds a VOICE's content still at its own culmination
(`courseHolds`, `pass-composer.js`'s own comment: «the crest law IS the culmination's own
suspension»), the ground and the door dial of every other simultaneously-live cue still answer to
progress — the suspension pauses one voice's content, never the whole composed passage — which is
exactly why this row reads the UNION of every live cue's own door, not any one cue alone: shelf 15's
own law is about the whole picture standing still, not about any one voice holding a pose.

THE EVALUATOR IS THE HOST'S OWN, sliced out of `pass-layer.js` between the same two landmarks
`tests/test_pass_planet.py` already uses (`evalNode`, plain arithmetic, no DOM) — so what this file
walks is what a running frame would actually read, not a second reading of the node graph invented
here.

WHAT COUNTS AS LIVE. A cue with `cues.length < 2` on its own plan (no travel, no arrival — the
ground plays entirely alone) is a single-voice pass with nothing to cross against; its own door
correctly reads whole and constant for the entire window (`buildTemplate`'s own «the lowest cue is
never given a zero door»), which is a different, already-understood shape and not this row's
concern. Every plan with two or more live cues is where the crest law actually applies, and every
one of those this file could compose from the real 121-work fixture is walked.

WHAT A FREEZE IS, WITHOUT A TYPED THRESHOLD. At each of a fixed number of evenly spaced instants
across the plan's own real duration, this file reads the `mix` value of every cue whose own window
covers that instant and joins them into one signature. Two ADJACENT instants whose signatures are
BYTE-IDENTICAL are two moments in which nothing this passage plays moved at all — no percentage, no
band, no fraction is chosen; the law is «no LIVE surface ever freezes», so any one such repeat is
already the violation, whatever else happens either side of it.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
LAYER = ROOT / "engine" / "assets" / "pass-layer.js"
FIXTURE = HERE / "fixture_pass_composed.json"
WORKS = HERE / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROW_HELD = "PASS-CREST-LAW the crest law holds over real composed multi-voice plans: no two " \
           "adjacent instants ever read the same door signature (shelf 15, «no LIVE surface " \
           "ever freezes»)"
ROW_REDBUG = "PASS-CREST-LAW RED-ON-BUG · a copy of the composer with the door's own curve node " \
             "replaced by a fixed value is caught by this same row"

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [composerPath, layerPath, fixturePath, worksPath, capArg, samplesArg] = process.argv.slice(2);

const L = fs.readFileSync(layerPath, "utf8").replace(/@@NS@@/g, "ex").split("\n");
const a = L.findIndex((l) => /^  var TAU = Math\.PI \* 2;/.test(l));
const b = L.findIndex((l) => /^  var slewIds = 0;/.test(l));
if (a < 0 || b < 0) { console.log(JSON.stringify({error: "the host's evaluator could not be found"})); process.exit(0); }
const ebox = {console, Math, JSON, Object, Number, Array, String, isFinite};
vm.createContext(ebox);
vm.runInContext(L.slice(a, b + 1).join("\n") + "\n; this.__e = evalNode;", ebox, {filename: "pass-layer-slice.js"});
const evalNode = ebox.__e;

const csrc = fs.readFileSync(composerPath, "utf8").replace(/@@NS@@/g, "");
let jc = null;
const cbox = {window: {__PassComposer: (m) => { jc = m; }}, console};
vm.createContext(cbox);
vm.runInContext(csrc, cbox, {filename: "pass-composer.js"});
if (!jc) { console.log(JSON.stringify({error: "the composer joined nothing"})); process.exit(0); }

const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const composer = jc.make(fix.consts);
const ids = Object.keys(works);
const CAP = parseInt(capArg, 10), N = parseInt(samplesArg, 10);

function mixAt(cue, dur, tSec) {
  const w = cue.window || [0, dur], w0 = Number(w[0]), w1 = Number(w[1]);
  if (tSec < w0 - 1e-9 || tSec > w1 + 1e-9) return null;
  const ctx = {nodes: cue.nodes || {}, progress: dur > 0 ? tSec / dur : 0,
               cueProgress: (w1 > w0) ? Math.max(0, Math.min(1, (tSec - w0) / (w1 - w0))) : 0,
               seconds: tSec, velocity: 0, capability: 1, pointer: null, state: {}, dt: 1};
  const ts = (cue.tracks || {}).mix;
  if (!ts) return null;
  const r = evalNode(ts.node ? {node: ts.node} : ts, ctx, 0);
  return r.ok ? Number(r.v.toFixed(6)) : null;
}

let examined = 0, multiVoice = 0, violations = [];
outer:
for (let i = 0; i < ids.length && examined < CAP; i++) {
  for (let j = 0; j < ids.length && examined < CAP; j++) {
    if (i === j) continue;
    examined++;
    if (examined >= CAP) break outer;
    const from = ids[i], to = ids[j];
    let p;
    try { p = composer.passageFor({workRecordA: works[from], workRecordB: works[to],
                                    direction: "a-to-b", seed: examined % 8}); }
    catch (e) { continue; }
    if (!p || !p.json) continue;
    const score = JSON.parse(p.json);
    const dur = (score.duration && score.duration.seconds) || (score.durationMs || 3000) / 1000 || 3;
    const cues = score.cues || [];
    if (cues.length < 2) continue;
    multiVoice++;
    let prevSig = null, frozenAt = null;
    for (let s = 0; s <= N && frozenAt === null; s++) {
      const t = (s / N) * dur;
      const sig = cues.map((c) => mixAt(c, dur, t)).join("|");
      if (prevSig !== null && sig === prevSig) frozenAt = {step: s, t: t, sig: sig};
      prevSig = sig;
    }
    if (frozenAt) violations.push({from, to, cues: cues.length, dur, frozenAt});
  }
}
console.log(JSON.stringify({examined, multiVoice, violations: violations.slice(0, 5),
                            count: violations.length}));
"""


def run(composer_path, cap, samples):
    driver = HERE / "_crest_law_driver.js"
    driver.write_text(DRIVER, encoding="utf-8")
    try:
        proc = subprocess.run(
            ["node", str(driver), str(composer_path), str(LAYER), str(FIXTURE), str(WORKS),
             str(cap), str(samples)],
            capture_output=True, text=True, timeout=300)
    finally:
        driver.unlink(missing_ok=True)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-800:]
    got = json.loads(proc.stdout.strip().splitlines()[-1])
    if got.get("error"):
        return None, got["error"]
    return got, None


def main():
    if not COMPOSER.exists() or not LAYER.exists() or not WORKS.exists() or not FIXTURE.exists():
        skip(ROW_HELD, "the composer, the host's evaluator, or the fixture is not on this machine")
        skip(ROW_REDBUG, "no composer to plant a copy of")
        return

    CAP, SAMPLES = 3000, 60
    got, err = run(COMPOSER, CAP, SAMPLES)
    if err:
        check(ROW_HELD, False, f"the driver failed: {err}")
    else:
        check(ROW_HELD, got["count"] == 0,
              f"{got['multiVoice']} real multi-voice crossings composed (of {got['examined']} "
              f"ordered pairs examined, seeds 0-7), each walked at {SAMPLES} evenly spaced instants "
              f"across its own real duration: {got['count']} ever repeated a door signature between "
              + ("adjacent instants" if got["count"] else "adjacent instants — none did")
              + (f"; first: {got['violations'][0]}" if got["count"] else ""))

    # ---- red on bug: a copy of the composer with the door's own curve node replaced by a fixed
    # value — the door stops answering to `cueProgress` on every cue at once, which is the plan-level
    # shape of «no LIVE surface ever freezes» broken outright. The source tree is never written to.
    src = COMPOSER.read_text(encoding="utf-8")
    needle = ('nodes[nodeName] = { op: "mix", a: flt(num(mixSpan[0])), b: flt(num(mixSpan[1])),\n'
              '                                t: { op: "curve", name: doorShape, '
              'in: { source: "cueProgress" } },\n'
              '                                note: why };')
    if needle not in src:
        check(ROW_REDBUG, False, "the plant found nothing to change")
        return
    mutated = src.replace(needle, 'nodes[nodeName] = { op: "static", value: flt(1.0), note: why };')
    planted = HERE / "_crest_law_planted.js"
    planted.write_text(mutated, encoding="utf-8")
    try:
        got2, err2 = run(planted, CAP, SAMPLES)
    finally:
        planted.unlink(missing_ok=True)
    if err2:
        check(ROW_REDBUG, False, f"the planted driver failed: {err2}")
        return
    check(ROW_REDBUG, got2["count"] > 0,
          f"with every cue's own door frozen at a fixed value, {got2['count']} of "
          f"{got2['multiVoice']} real multi-voice crossings now repeat a door signature between "
          f"adjacent instants, where the unplanted composer read {got['count'] if not err else '?'}")


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
