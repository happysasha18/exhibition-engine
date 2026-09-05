#!/usr/bin/env python3
"""S-47 — the link is the work: the word, the film compiled through the crossing skeleton, and the
two checks run on every film.
Run: python3 tests/test_darkroom_film.py [--plant NAME]

WHAT IS UNDER TEST. The functions engine/assets/darkroom.js ships for the result's life —
`darkroomWord`, `darkroomReadWord`, `darkroomMadeRecord`, `darkroomFilm`, `darkroomFilmChecks`,
`darkroomFilmFrame` and `darkroomStripStates` — driven against the REAL, shipped crossing skeleton
(engine/assets/pass-composer.js, unmodified) over the REAL work records
(tests/fixtures/darkroom-records.json) and the REAL fleet's own manifests, which are the collection's
own constants out of tests/fixture_pass_composed.json. Everything runs in one generated Node driver,
the same idiom tests/test_darkroom_taste.py already carries for this file's neighbours; the composer
is joined in a `vm` sandbox exactly as tests/test_pass_step_sequencer.py joins it.

NO CLOCK IS DRIVEN ANYWHERE HERE. A film's frame is a pure read of the compiled plan at one named
instant, so every row below reads arithmetic and none of them waits, times or benchmarks anything.

THE LAW EACH ROW ANSWERS TO is SPEC.md Requirement 41:
  13  a finished work is a word — the photograph by name, the ordered chain with each step's
      numbers, and the recursion depth;
  15  the receiver is played the making-movie, compiled through the crossing skeleton and never
      replayed step by step;
  16  the seam check and the no-wipe lint run on EVERY compiled movie;
  18  a downloadable card carries the print plus a thin contact strip of its making;
  35  a word naming a photograph the collection no longer holds is neither rewritten nor silently
      resolved to a different photograph;
  36  a step naming an operation the registry no longer carries plays at its declared neutral, with
      the surviving steps still reading in their own order.
Requirement 41 criterion 11 names the tier the room runs at, and row 6 reads it off the plan.

WHAT THE NO-CUT LINT IS, said once. Shelf 18 (SPEC.md Requirement 30 criterion 9) bans «playing
whole operations one after another, each from start to finish». On a compiled plan that ban is three
counts, and darkroom.js's own `darkroomFilmChecks` reads all three: the ground must span the film
whole, no voice may open only after another has closed (the same predicate
tests/test_pass_step_sequencer.py reads off `cues[i].window` for a walk's passage), and the camera's
knots must run forward inside the film's own span, because Requirement 14 criterion 2 makes a camera
cut one instance of the same ban.

WHAT THE SEAM IS, on a plan. tests/test_pass_seam.py photographs a handoff and calls it a change of
AUTHORITY, not of picture. On a compiled plan that authority change is the cue's own door — the
handle it enters on and the handle it leaves on — so a voice with no door on a side hands the frame
over with nothing standing at the handover, and the film's own two ends are the same fact at the
outside: the camera rests on the departing work at the head and the arriving one at the foot.

PLANTED DEFECTS. Five are mutations of a REAL composed plan, applied inside the driver to a film the
skeleton actually composed; three are text mutations of a throwaway in-memory copy of darkroom.js.
The file on disk is never touched (tests/test_pass_matter.py:358-364's own rule), so nothing has to
be restored and no working tree can be left changed by a red-on-bug proof.
  seam-vanishes          every voice's out door dropped                         → row 8 reds
  camera-unanchored      the camera no longer rests on the arriving work        → row 8 reds
  cut-ground-late        the ground opens after the film's own head             → row 9 reds
  cut-end-to-end         a voice laid entirely after another has closed         → row 9 reds
  cut-camera-backwards   two camera knots exchanged, so one runs backwards      → row 9 reds
  word-writes-rest       the quiet-value rule dropped from `darkroomWord`       → row 2 reds
  retired-step-dropped   an unknown step dropped instead of held at neutral     → row 4 reds
  absent-photo-swapped   a missing photograph answered with a different one     → row 5 reds
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
DARKROOM = ROOT / "engine" / "assets" / "darkroom.js"
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = HERE / "fixture_pass_composed.json"
RECORDS = HERE / "fixtures" / "darkroom-records.json"

# HOW MANY PHOTOGRAPHS THE FILM ROWS SWEEP. Every claim below is a claim about ONE film, proved on
# each film separately — the count is how many separate proofs this run carried out, never a share
# of anything (SPEC.md Requirement 12 criterion 7, and Requirement 32's proof by construction). It
# is set by what one Node call composes without the run growing a wait of its own.
SWEEP = 24

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


ROW1 = "S-47 WORD a making written as a word and read back stands at the same handle values"
ROW2 = "S-47 WORD a handle resting at its own manifest's def writes nothing, and reads back at it"
ROW3 = "S-47 WORD the word names the photograph and the depth, and a depth of 1 leaves no mark"
ROW4 = "S-47 WORD a step the registry no longer carries keeps its place and names no handle"
ROW5 = "S-47 WORD a photograph the collection no longer holds is refused, never swapped for another"
ROW6 = "S-47 FILM every film is the crossing skeleton's own plan, at the tier the room runs at"
ROW7 = "S-47 FILM every compiled film carries its two checks — none is handed back without them"
ROW8 = "S-47 SEAM every compiled film's seam is whole: every voice's own doors, both hangs anchored"
ROW9 = "S-47 NO CUT every compiled film carries no cut: ground whole, voices overlapping, camera forward"
ROW10 = "S-47 FILM the film opens on the bare print and closes on the made work, travelling between"
ROW11 = "S-47 CARD the contact strip carries one frame per step of the making, in its own order"
ROW12 = "S-47 RED-ON-BUG a film compiled with a cut in it reds the no-cut row, three ways"
ROW13 = "S-47 RED-ON-BUG a seam that vanishes reds the seam row, two ways"
ROW14 = "S-47 RED-ON-BUG the word's own three rules each red their own row when dropped"

ROWS = [ROW1, ROW2, ROW3, ROW4, ROW5, ROW6, ROW7, ROW8, ROW9, ROW10, ROW11, ROW12, ROW13, ROW14]

# THE MAKING THE FILM ROWS ARE COMPOSED FROM — a chain over the two instruments DR-10 gave the
# room's own three gestures, with each handle standing away from its own manifest's def so the
# making is a real one. No value here is a threshold: each is a point inside the handle's own
# published range, and the driver reads the range off the manifest rather than trusting these.
MAKING_CHAIN = [
    {"instrument": "livemirror", "handles": {"axis": 1, "centreX": 0.42, "centreY": 0.5}},
    {"instrument": "studio", "handles": {"zoom": 1.9, "panX": 0.12}},
    {"instrument": "livemirror", "handles": {"axis": 0, "centreY": 0.31}},
]

TMP = Path(tempfile.mkdtemp(prefix="darkroom_film_"))
DRIVER_PATH = TMP / "darkroom-film-driver.js"

SOURCE_PLANTS = {
    "word-writes-rest": (
        "      if (spec && typeof spec.def === \"number\" && v === darkroomRound4(spec.def)) return;",
        "      if (false) return;",
    ),
    "retired-step-dropped": (
        "    chain.push({ instrument: id, handles: handles, held: !manifest });",
        "    if (!manifest) return;\n    chain.push({ instrument: id, handles: handles, held: false });",
    ),
    "absent-photo-swapped": (
        "  if (!from) return { word: word, refused: \"the collection holds no such photograph\" };",
        "  if (!from) from = (records || {})[Object.keys(records || {})[0]];\n"
        "  if (!from) return { word: word, refused: \"the collection holds no such photograph\" };",
    ),
}

PLAN_PLANTS = ["seam-vanishes", "camera-unanchored", "cut-ground-late", "cut-end-to-end",
               "cut-camera-backwards"]

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [darkroomPath, composerPath, fixturePath, recordsPath, sweepArg, planPlant, sourcePlantJson]
  = process.argv.slice(2);

let darkroomSrc = fs.readFileSync(darkroomPath, "utf8");
const sourcePlant = JSON.parse(sourcePlantJson);
if (sourcePlant) {
  if (darkroomSrc.indexOf(sourcePlant[0]) < 0) {
    console.log(JSON.stringify({error: "source plant anchor not found"}));
    process.exit(0);
  }
  if (darkroomSrc.split(sourcePlant[0]).length !== 2) {
    console.log(JSON.stringify({error: "source plant anchor is not unique"}));
    process.exit(0);
  }
  darkroomSrc = darkroomSrc.replace(sourcePlant[0], sourcePlant[1]);
}
const dk = {console, window: {}};
vm.createContext(dk);
vm.runInContext(darkroomSrc, dk, {filename: "darkroom.js"});

let joined = null;
const cs = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(cs);
vm.runInContext(fs.readFileSync(composerPath, "utf8").replace(/@@NS@@/g, ""), cs,
                {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the composer joined nothing"})); process.exit(0); }
const consts = JSON.parse(fs.readFileSync(fixturePath, "utf8")).consts;
const composer = joined.make(consts);
const manifests = consts.manifests || {};
const records = JSON.parse(fs.readFileSync(recordsPath, "utf8"));
const ids = Object.keys(records);
const SWEEP = parseInt(sweepArg, 10);

const CHAIN = MAKING_CHAIN_JSON;

function u(v) { return (v && typeof v === "object" && "v" in v) ? v.v : v; }
function clone(o) { return JSON.parse(JSON.stringify(o)); }

// ---- the plan plants, each applied to a film the skeleton really composed --------------------
function plantPlan(plan, name) {
  const cues = plan.cues || [];
  const track = (plan.camera || {}).track || [];
  const duration = u(plan.duration) / 1000;
  if (name === "seam-vanishes") {
    cues.forEach((c) => { if (c.doors) delete c.doors.out; });
  } else if (name === "camera-unanchored") {
    if (track.length) track[track.length - 1].at = {v: duration};
  } else if (name === "cut-ground-late") {
    const ground = dk.darkroomFilmGround(plan);
    if (ground) ground.window[0] = {v: duration / 4};
  } else if (name === "cut-end-to-end") {
    // A SECOND VOICE, laid whole after the ground has closed — the step sequencer itself.
    cues.push({id: "planted", instrument: {api: 1, id: "beat"}, voice: "letter", levels: [],
               window: [{v: duration}, {v: duration}], stack: 1,
               doors: {in: {handle: "mix", value: 0}, out: {handle: "mix", value: 1}}});
    cues.push({id: "planted-2", instrument: {api: 1, id: "beat"}, voice: "letter", levels: [],
               window: [{v: duration + 1}, {v: duration + 2}], stack: 2,
               doors: {in: {handle: "mix", value: 0}, out: {handle: "mix", value: 1}}});
  } else if (name === "cut-camera-backwards") {
    if (track.length >= 3) { const swap = track[1]; track[1] = track[2]; track[2] = swap; }
  }
  return plan;
}

// ---- the films -------------------------------------------------------------------------------
const films = [];
for (let i = 0; i < ids.length && films.length < SWEEP; i++) {
  const making = {photo: ids[i], chain: CHAIN, depth: 1};
  const film = dk.darkroomFilm(making, records, {manifests}, composer);
  if (film.refused) { films.push({id: ids[i], refused: film.refused}); continue; }
  if (planPlant !== "none") {
    plantPlan(film.plan, planPlant);
    film.checks = dk.darkroomFilmChecks(film.plan);
  }
  const duration = u(film.plan.duration) / 1000;
  const frame0 = dk.darkroomFilmFrame(film.plan, 0);
  const frameEnd = dk.darkroomFilmFrame(film.plan, duration);
  const walk = [0, 0.25, 0.5, 0.75, 1].map((f) => dk.darkroomFilmFrame(film.plan, duration * f).travel);
  const ground = dk.darkroomFilmGround(film.plan);
  films.push({
    id: ids[i], word: film.word, madeId: film.made && film.made.id,
    hasChecks: !!(film.checks && film.checks.seam && film.checks.cut),
    seam: film.checks.seam, cut: film.checks.cut,
    tier: film.plan.tier, duration: u(film.plan.duration),
    cues: (film.plan.cues || []).length,
    windows: (film.plan.cues || []).map((c) => [c.id, u(c.window[0]), u(c.window[1])]),
    knots: ((film.plan.camera || {}).track || []).length,
    groundIn: ground && ground.doors && ground.doors.in ? u(ground.doors.in.value) : null,
    groundOut: ground && ground.doors && ground.doors.out ? u(ground.doors.out.value) : null,
    travel0: frame0.travel, travelEnd: frameEnd.travel, walk: walk,
  });
}

// ---- the word --------------------------------------------------------------------------------
const making = {photo: ids[0], chain: CHAIN, depth: 1};
const word = dk.darkroomWord(making, manifests);
const back = dk.darkroomReadWord(word, manifests);
// Every handle the making named, read back off the word.
const roundTrip = CHAIN.map((step, i) => {
  const got = (back.chain[i] || {}).handles || {};
  return Object.keys(step.handles).map((h) => [step.instrument, h, step.handles[h], got[h]]);
});
// A handle standing at its own def: livemirror's centreY is set to 0.5 in the chain's first step and
// its manifest's own def is 0.5, so the word must not name it, and it must read back at 0.5.
const restHandle = manifests.livemirror.handles.centreY.def;
const steps = (word.split("/")[1] || "").split(";");
const namesRest = steps[0].indexOf("centreY=") >= 0;
// the making's THIRD step moves centreY off its def, and that step must name it — otherwise the
// rule above would be green on a word that names nothing at all.
const namesMoved = steps[2].indexOf("centreY=") >= 0;
const restBack = ((back.chain[0] || {}).handles || {}).centreY;

const deep = dk.darkroomWord({photo: ids[0], chain: CHAIN, depth: 3}, manifests);
const deepBack = dk.darkroomReadWord(deep, manifests);
const flatBack = dk.darkroomReadWord(word, manifests);

// A step naming an instrument nobody carries — the retired half of Requirement 41 criterion 36.
const retiredWord = ids[0] + "/livemirror,centreX=0.3;shatter,amount=7;studio,zoom=2";
const retired = dk.darkroomReadWord(retiredWord, manifests);

// A photograph the collection no longer holds.
const absent = dk.darkroomFilm({photo: "no-such-photograph", chain: CHAIN, depth: 1},
                               records, {manifests}, composer);

// ---- the strip -------------------------------------------------------------------------------
const strip = dk.darkroomStripStates(making);

console.log(JSON.stringify({
  films: films, word: word, roundTrip: roundTrip,
  namesRest: namesRest, namesMoved: namesMoved, restHandle: restHandle, restBack: restBack,
  steps: steps,
  deep: deep, deepDepth: deepBack.depth, flatDepth: flatBack.depth,
  photoInWord: word.split("/")[0], photoId: ids[0],
  retired: retired.chain.map((c) => [c.instrument, !!c.held, Object.keys(c.handles).length]),
  absentRefused: absent.refused || null, absentPlan: !!absent.plan,
  strip: strip.map((s) => Object.keys(s).sort()),
  stripValues: strip.map((s) => JSON.parse(JSON.stringify(s))),
}));
"""


def run(plan_plant="none", source_plant=None):
    driver = DRIVER.replace("MAKING_CHAIN_JSON", json.dumps(MAKING_CHAIN))
    DRIVER_PATH.write_text(driver, encoding="utf-8")
    proc = subprocess.run(
        ["node", str(DRIVER_PATH), str(DARKROOM), str(COMPOSER), str(FIXTURE), str(RECORDS),
         str(SWEEP), plan_plant, json.dumps(SOURCE_PLANTS.get(source_plant) if source_plant else None)],
        capture_output=True, text=True, timeout=600)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-2000:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


def word_rows(got):
    """Rows 1 to 5, off one clean run. Returns each row's own boolean so a plant run can read it."""
    round_ok = all(
        pair[2] == pair[3] for step in got["roundTrip"] for pair in step
    )
    rest_ok = ((not got["namesRest"]) and got["namesMoved"]
               and got["restBack"] == got["restHandle"])
    depth_ok = (got["photoInWord"] == got["photoId"] and got["deep"].endswith("/x3")
                and got["deepDepth"] == 3 and got["flatDepth"] == 1
                and "/x" not in got["word"])
    retired = got["retired"]
    retired_ok = (len(retired) == 3 and retired[1][0] == "shatter" and retired[1][1] is True
                  and retired[1][2] == 0 and retired[0][1] is False and retired[2][1] is False
                  and retired[2][2] > 0)
    absent_ok = bool(got["absentRefused"]) and not got["absentPlan"]
    return round_ok, rest_ok, depth_ok, retired_ok, absent_ok


def film_rows(got):
    """Rows 6 to 11. Returns each row's own boolean so a plant run can read it."""
    films = [f for f in got["films"] if not f.get("refused")]
    # THE ROOM'S OWN TIER IS A CEILING, NOT AN EXACT NAME. Requirement 41 criterion 11 says the room
    # runs at middle tier; the composer reads that as `TIER_RANK[tier] <= TIER_RANK[roleBudget.tier]`
    # (pass-composer.js:5070) against the `middle` role's own budget, so a film lands at `middle` or
    # under it and never above. `TIERS` (pass-composer.js:355-367) publishes the three in order, and
    # the two at or under the room's ceiling are the two named here.
    skeleton_ok = bool(films) and all(
        f["cues"] >= 1 and f["knots"] >= 2 and f["duration"] > 0
        and f["tier"] in ("quiet", "middle")
        and all(w[1] is not None and w[2] is not None for w in f["windows"])
        for f in films)
    checks_ok = bool(films) and all(f["hasChecks"] for f in films)
    seam_ok = bool(films) and all(f["seam"]["ok"] for f in films)
    cut_ok = bool(films) and all(f["cut"]["ok"] for f in films)
    ends_ok = bool(films) and all(
        abs(f["travel0"] - (f["groundIn"] if f["groundIn"] is not None else 0)) < 1e-9
        and abs(f["travelEnd"] - (f["groundOut"] if f["groundOut"] is not None else 1)) < 1e-9
        and all(f["walk"][i] <= f["walk"][i + 1] + 1e-9 for i in range(len(f["walk"]) - 1))
        for f in films)
    # THE STRIP IS THE MAKING AS IT STOOD AT EACH STEP. The chain folds, then zooms, then folds
    # again, so the first frame carries the fold alone, and the two after it carry the fold and the
    # zoom together, the second fold moving only what the second fold moved.
    strip = got["strip"]
    strip_ok = (len(strip) == len(MAKING_CHAIN)
                and strip == [["livemirror"], ["livemirror", "studio"], ["livemirror", "studio"]]
                and got["stripValues"][0]["livemirror"]["centreX"] == 0.42
                and "studio" not in got["stripValues"][0]
                and got["stripValues"][1]["studio"]["zoom"] == 1.9
                and got["stripValues"][1]["livemirror"]["centreY"] == 0.5
                and got["stripValues"][2]["livemirror"]["centreY"] == 0.31
                and got["stripValues"][2]["studio"]["zoom"] == 1.9)
    return skeleton_ok, checks_ok, seam_ok, cut_ok, ends_ok, strip_ok, films


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plant", default=None)
    args = ap.parse_args()

    if args.plant:
        plan_plant = args.plant if args.plant in PLAN_PLANTS else "none"
        source_plant = args.plant if args.plant in SOURCE_PLANTS else None
        got = run(plan_plant, source_plant)
        print(json.dumps(got.get("error") or {k: got[k] for k in ("films",) if k in got})[:2000])
        return 0

    clean = run()
    if "error" in clean:
        print("the driver failed: %s" % clean["error"])
        return 2

    round_ok, rest_ok, depth_ok, retired_ok, absent_ok = word_rows(clean)
    skeleton_ok, checks_ok, seam_ok, cut_ok, ends_ok, strip_ok, films = film_rows(clean)

    check(ROW1, round_ok,
          "%d handle values written into the word and read back, over the real fleet's manifests"
          % sum(len(s) for s in clean["roundTrip"]))
    check(ROW2, rest_ok,
          "livemirror.centreY rests at its manifest's own def (%s) in the first step and the word's "
          "own token for it is «%s»; the third step moves it and its token is «%s»; the resting one "
          "reads back at %s" % (clean["restHandle"], clean["steps"][0], clean["steps"][2],
                                clean["restBack"]))
    check(ROW3, depth_ok,
          "the word opens with the photograph's own name (%s); a depth of 3 writes /x3 and reads "
          "back as %s, a depth of 1 writes nothing and reads back as %s"
          % (clean["photoInWord"], clean["deepDepth"], clean["flatDepth"]))
    check(ROW4, retired_ok,
          "the chain reads back as %s — the retired step keeps its place, names no handle of its "
          "own, and the two the registry carries are unchanged" % clean["retired"])
    check(ROW5, absent_ok,
          "refused as «%s», and no plan was composed for a photograph the collection does not hold"
          % clean["absentRefused"])
    check(ROW6, skeleton_ok,
          "%d films composed by the shipped passageFor, each carrying cues with windows, a camera "
          "track and a duration; tiers cast: %s, all at or under the room's own ceiling"
          % (len(films), sorted({f["tier"] for f in films})))
    check(ROW7, checks_ok, "%d of %d films handed back both checks" % (
        sum(1 for f in films if f["hasChecks"]), len(films)))
    check(ROW8, seam_ok, "%d films; seam faults: %s" % (
        len(films), sorted({x for f in films for x in f["seam"]["faults"]}) or "none"))
    check(ROW9, cut_ok, "%d films; cut faults: %s" % (
        len(films), sorted({x for f in films for x in f["cut"]["faults"]}) or "none"))
    check(ROW10, ends_ok,
          "each film's frame at 0 stands at its ground's own in door and its frame at the film's own "
          "end at the out door, travelling forward between (first film: %s → %s over %s)"
          % (films[0]["travel0"], films[0]["travelEnd"], films[0]["walk"]) if films else "no film")
    check(ROW11, strip_ok,
          "%d steps of the making, %d frames on the strip, each carrying the chain as it stood: %s"
          % (len(MAKING_CHAIN), len(clean["strip"]), clean["strip"]))

    # ---- the plants ----------------------------------------------------------------------------
    cut_reds = {}
    for name in ("cut-ground-late", "cut-end-to-end", "cut-camera-backwards"):
        got = run(plan_plant=name)
        cut_reds[name] = "error" not in got and not film_rows(got)[3]
    check(ROW12, all(cut_reds.values()), "each plant and whether row 9 went red: %s" % cut_reds)

    seam_reds = {}
    for name in ("seam-vanishes", "camera-unanchored"):
        got = run(plan_plant=name)
        seam_reds[name] = "error" not in got and not film_rows(got)[2]
    check(ROW13, all(seam_reds.values()), "each plant and whether row 8 went red: %s" % seam_reds)

    word_reds = {}
    got = run(source_plant="word-writes-rest")
    word_reds["word-writes-rest → row 2"] = "error" not in got and not word_rows(got)[1]
    got = run(source_plant="retired-step-dropped")
    word_reds["retired-step-dropped → row 4"] = "error" not in got and not word_rows(got)[3]
    got = run(source_plant="absent-photo-swapped")
    word_reds["absent-photo-swapped → row 5"] = "error" not in got and not word_rows(got)[4]
    check(ROW14, all(word_reds.values()), "each plant and whether its own row went red: %s" % word_reds)

    # THE DEFECTS ARE ALL IN MEMORY — the file on disk was never written to, so a clean run after
    # them must read exactly as the clean run before them did.
    again = run()
    check("S-47 the planted defects left the tree untouched",
          "error" not in again and film_rows(again)[:6] == (skeleton_ok, checks_ok, seam_ok,
                                                            cut_ok, ends_ok, strip_ok),
          "every row green again on a fresh clean run")

    print()
    failed = [r for r in results if r[1] == "FAIL"]
    for name, status, detail in results:
        print("%-6s %s\n       %s" % (status, name, detail))
    print("\n%d checks, %d passed, %d failed"
          % (len(results), len(results) - len(failed), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
