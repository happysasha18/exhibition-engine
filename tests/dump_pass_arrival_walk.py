#!/usr/bin/env python3
"""dump_pass_arrival_walk — what a ten-transition walk actually arrives by, read off the SHIPPED
composer over the records the site publishes.

WHY IT EXISTS. Charter shelf 7 names five arrivals — CARRIED, CRYSTALLIZED, CONDENSED, PROPAGATED,
INTERFERED — and наряд S-06 asks for one thing no arithmetic row answers: «живой прогон на десяти
переходах показывает больше одного режима», a run of ten transitions showing more than one mode.
tests/test_pass_composed.py proves each mode CAN win a pair built to make it win; that is a
different question from what a walk over the real collection does.

WHAT IT RUNS. `engine/assets/pass-composer.js` itself, loaded the way the client loads it, over the
121 per-work records in tests/fixture_pass_works.json — the same records the site's own settings
build publishes. Ten consecutive edges of the record's own published order are walked in one visit,
and the visit's memory is carried from step to step exactly as engine/client/01a-pass.js carries it:
`walkMemory` (the letters docked so far, most recent first), `walkGenres` (the roads), and
`walkMiracles` (the cues the composer itself voiced a miracle on). Every one of those is read OFF
THE COMPOSED SCORE of the step before, never described here.

WHAT EACH STEP REPORTS. The arrival the plan names, the point it seeds at where it names one, the
instrument the arrival was cast to, and — the reading the наряд is actually after — WHETHER THE MODE
REACHED A HANDLE: `pour.arrival`/`pour.seedPlace` for the crystallized order, `livemirror.propagate`
for the mirrored copies, `overlay.arrival`/`grid-colour.arrival` for the interfered one. A mode that
is only named is reported as named and no more.

WHAT IT IS NOT, AND THE READING IT DOES NOT REPLACE. It is not a browser: no pixel is drawn here,
and the наряд's own clause is about a walk a person watches. What this answers is the half that can
be answered without one — that a real walk over real records reaches more than one arrival, and
which of them reach an instrument. A person's own look at ten transitions on the moving page is
still owed, and is named as owed rather than papered over by this file.

AND THE ROUTE ROLES ARE LEFT UNSAID, deliberately. The walk's dramaturgy — which edge is an
entrance, a middle, a culmination, a return — is derived in the client from the hung route's own
kinship vectors and keys (`passRouteShape`), and re-typing that here would be a description of the
client rather than the client. The composer's own «missing means unstated» road stands instead, so
every step below composes at its own default. A role changes the voice budget and can change which
instrument is cast; it does not change which arrival `arrivalOf` ranks highest, which is what this
file reads.

Run: python3 tests/dump_pass_arrival_walk.py
Writes tests/pass_arrival_walk.txt beside its stdout.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE.parent / "engine" / "assets" / "pass-composer.js"
FIXTURE = HERE / "fixture_pass_composed.json"
WORKS = HERE / "fixture_pass_works.json"
OUT_TXT = HERE / "pass_arrival_walk.txt"
STEPS = 10

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

// A die per ordered pair that is the pair's own, so this run and the run before it roll the same
// number — the same construction tests/test_pass_composed.py walks the collection with.
function die(key) {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) { h = Math.imul(h ^ key.charCodeAt(i), 16777619) >>> 0; }
  return (h % 100000) / 100000 * 8;
}

// WHICH HANDLES CARRY AN ARRIVAL'S OWN WORD TO THE PICTURE. Each is read off the composed score
// itself — the node the fill wrote for that handle on that cue — so nothing here asserts that a
// handle exists; it reports whether this crossing drove it.
const CARRIERS = {
  "pour.arrival": "CRYSTALLIZED", "pour.seedPlace": "CRYSTALLIZED",
  "livemirror.propagate": "PROPAGATED",
  "overlay.arrival": "INTERFERED", "grid-colour.arrival": "INTERFERED"
};
function unwrap(v) { return (v && typeof v === "object" && "v" in v) ? v.v : v; }

const ids = Object.keys(works);
const out = {steps: [], modes: {}, reached: 0, named: 0};
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
  let p = null, err = null;
  try { p = composer.passageFor(req); } catch (e) { err = String((e && e.message) || e); }
  const plan = (p && p.plan) || null;
  const arr = (plan && plan.arrival) || {};
  const cues = (plan && plan.cues) || [];
  const arrivalCue = cues.filter((c) => c.id === "arrival")[0] || null;
  // WHAT THIS STEP DROVE, of the handles that carry an arrival's own word.
  // `measuredHandles` is the cue's own record of what the FILL asked for, so a handle standing at
  // the instrument's own rest — which the score still writes a node for — is never counted here.
  // A CARRIER COUNTS ONLY WHERE ITS OWN VALUE SAYS THE MODE IS ON. Two of these handles are
  // written on every crossing the instrument plays — `grid-colour.arrival` stands at 0 for every
  // arrival but the interfered one — so the value is what is read, never the presence of the row.
  const drove = [];
  for (const c of cues) {
    const mh = c.measuredHandles || {};
    const on = (h) => unwrap(mh[h]);
    if (c.instrument.id === "pour" && on("arrival") >= 0.5) {
      drove.push("pour.arrival=1", "pour.seedPlace=" + JSON.stringify(on("seedPlace")));
    }
    if (c.instrument.id === "livemirror" && on("propagate") > 0) {
      drove.push("livemirror.propagate=" + JSON.stringify(on("propagate")));
    }
    if ((c.instrument.id === "overlay" || c.instrument.id === "grid-colour")
        && on("arrival") >= 0.5) {
      drove.push(c.instrument.id + ".arrival=1");
    }
  }
  const mode = arr.mode || null;
  if (mode) { out.modes[mode] = (out.modes[mode] || 0) + 1; out.named++; }
  if (drove.length) out.reached++;
  out.steps.push({
    at: i + 1, from: from, to: to, mode: mode,
    locusKind: arr.locusKind || null, locus: arr.locus || null,
    genre: (plan && plan.genre) || (p && p.genre) || null,
    instrument: arrivalCue ? arrivalCue.instrument.id : null,
    roles: arrivalCue ? arrivalCue.roles : null,
    drove: drove, declined: (p && p.declined) || null, error: err
  });
  // THE VISIT'S OWN MEMORY, CARRIED THE WAY THE CLIENT CARRIES IT — read off the score just
  // composed, most recent first, never described.
  if (plan) {
    const letters = cues.map((c) => c.instrument.id);
    played.unshift.apply(played, letters);
    if (plan.genreName || plan.genre) genres.unshift(plan.genreName || plan.genre);
    for (const c of cues) if (c.voice === "miracle") miracles.unshift(c.instrument.id);
  }
}
console.log(JSON.stringify(out));
"""


def main():
    if not MODULE.exists() or not WORKS.exists():
        print("the composer or the records are not on this machine", file=sys.stderr)
        return 3
    driver = HERE / "_arrival_walk_driver.js"
    driver.write_text(DRIVER, encoding="utf-8")
    try:
        proc = subprocess.run(["node", str(driver), str(MODULE), str(FIXTURE), str(WORKS),
                               str(STEPS)],
                              capture_output=True, text=True, timeout=600)
    finally:
        driver.unlink(missing_ok=True)
    if proc.returncode != 0:
        print((proc.stderr or proc.stdout)[-800:], file=sys.stderr)
        return 1
    got = json.loads(proc.stdout.strip().splitlines()[-1])
    if got.get("error"):
        print(got["error"], file=sys.stderr)
        return 1

    lines = []
    lines.append("A TEN-TRANSITION WALK, AND WHAT IT ARRIVES BY")
    lines.append("=" * 78)
    lines.append("")
    lines.append("Read off engine/assets/pass-composer.js itself, over the 121 per-work records in")
    lines.append("tests/fixture_pass_works.json, ten consecutive edges of the record's own order in")
    lines.append("one visit with the walk's memory carried from step to step. No pixel is drawn")
    lines.append("here: what a person sees on the moving page is a separate look, still owed.")
    lines.append("")
    for s in got["steps"]:
        lines.append("step %2d  %s -> %s" % (s["at"], s["from"], s["to"]))
        seed = ("" if not s["locus"]
                else "  seeded at %s of the frame's width, %s of its height"
                     % (s["locus"][0], s["locus"][1]))
        lines.append("         arrival: %s (%s)%s"
                     % (s["mode"], s["locusKind"], seed))
        lines.append("         cast:    %s%s"
                     % (s["instrument"] or "no instrument of its own",
                        "" if not s["roles"] else " " + json.dumps(s["roles"])))
        lines.append("         reached: %s"
                     % (", ".join(s["drove"]) if s["drove"]
                        else "no handle — the mode is named on the plan and no instrument of this "
                             "crossing carries it"))
        if s["declined"] or s["error"]:
            lines.append("         declined/threw: %s" % (s["declined"] or s["error"]))
        lines.append("")
    lines.append("-" * 78)
    modes = got["modes"]
    lines.append("modes over the walk: "
                 + ", ".join("%s x%d" % (k, modes[k]) for k in sorted(modes)))
    lines.append("distinct modes: %d of the charter's five" % len(modes))
    lines.append("steps whose arrival reached an instrument handle: %d of %d"
                 % (got["reached"], got["named"]))
    lines.append("")
    lines.append("WHAT REACHING A HANDLE MEANS. `pour.arrival`/`pour.seedPlace` order the pour's")
    lines.append("own columns outward from the seed; `livemirror.propagate` spreads the mirrored")
    lines.append("copies' exchanges apart, the further copy first; `overlay.arrival` and")
    lines.append("`grid-colour.arrival` carry the interfered arrival. CARRIED and CONDENSED have no")
    lines.append("handle of their own: the first is the gesture already running and the second is")
    lines.append("the arrival instrument's own cast, which the `cast:` line above names.")
    text = "\n".join(lines) + "\n"
    OUT_TXT.write_text(text, encoding="utf-8")
    print(text)
    print("written to %s" % OUT_TXT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
