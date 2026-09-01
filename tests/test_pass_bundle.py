#!/usr/bin/env python3
"""P1.2 — the joint phrase planner's own five legality rules, its score, and its widened return.

Run: python3 tests/test_pass_bundle.py

His 2026-08-28 sprint brief. `compose`'s old budget loop (pass-composer.js) shrank one fixed stack
in one fixed order — swap the ground once, drop travel, drop arrival, surrender structural colour
first of all, before anything else was ever weighed. This file proves the five rules that now stand
BEFORE any bundle is scored (one WORLD at a time, one level-owner per overlapping window, the tier
budget, the declared resource peak, the surface-handover stub), the score that replaces "colour goes
first" with "colour is not the first voice surrendered when it carries the herald, the bridge or the
arrival", and the widened `passIndex` die that keeps a repeated return from settling into an
alternation of two frames forever.

THE ROAD THIS FILE WALKS. `tests/test_pass_lawful.py` proved `tierFor` by extracting its source text
and running it standalone; these five rules and the score read the REAL, loaded `MANIFESTS` (real
instrument levels and resources), so they are exposed directly off `make(consts)`'s own returned
object instead (pass-composer.js's own export list, right beside `tierFor`'s neighbours) — never a
retyped mirror, the real functions, loaded once per job in a fresh `vm` context exactly as
test_pass_lawful.py's own driver already does.

RED-BEFORE/GREEN-AFTER, THE WAY THIS SUITE ALREADY PROVES A RULE IS LOAD-BEARING (PLANT_R1,
PLANT_SLOT in test_pass_lawful.py): a positive case is shown legal, a violating case is shown
refused with its own reason, and then a PLANT — a minimal, named substring replacement disabling
exactly that rule's own guard — is applied and the violating case is shown to wrongly pass under it,
proving the assertion actually depends on the rule's own code rather than on a name.
"""
import json
import copy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"
FIXTURE_WORKS = ROOT / "tests" / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def node_available():
    return shutil.which("node") is not None


NODE = node_available()

RAW = MODULE.read_text(encoding="utf-8").replace("@@NS@@", "")
FIX = json.loads(FIXTURE.read_text(encoding="utf-8"))

TMP = Path(tempfile.mkdtemp(prefix="pass_bundle_"))
DRIVER = TMP / "bundle-driver.js"

# THE JOBS. Each names the exposed function to call and the arguments to call it with; the driver
# below is one small dispatch table over `make(consts)`'s own returned object, never a second copy
# of any rule's own logic.
DRIVER_TEMPLATE = r"""
"use strict";
const vm = require("vm");
const rawSource = %(source)s;
const consts = %(consts)s;
const job = %(job)s;

let source = rawSource;
const missed = [];
for (const [from, to] of (job.plants || [])) {
  if (source.indexOf(from) < 0) { missed.push(from); continue; }
  source = source.split(from).join(to);
}
if (missed.length) { console.log(JSON.stringify({missed: missed})); process.exit(0); }

let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
try {
  vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
} catch (e) {
  console.log(JSON.stringify({error: String(e && e.stack || e)}));
  process.exit(0);
}
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(0); }
const composer = joined.make(consts);
let out;
try {
  out = composer[job.fn].apply(null, job.args);
} catch (e) {
  out = {error: String(e && e.stack || e)};
}
console.log(JSON.stringify(out === undefined ? null : out));
"""


def run(fn, args, plants=None, consts=None):
    driver = DRIVER_TEMPLATE % {
        "source": json.dumps(RAW),
        "consts": json.dumps(consts if consts is not None else FIX["consts"]),
        "job": json.dumps({"fn": fn, "args": args, "plants": plants or []}),
    }
    DRIVER.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(DRIVER)], capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1200:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


if not NODE:
    for _n in (
        "RULE 1 (one WORLD) · a bundle with one fold and no miracle budget is refused",
        "RULE 1 · two folding voices in one bundle are refused even where the role may spend one",
        "RULE 1 · a bundle with one fold and a role that may spend it is legal",
        "RULE 1 red-on-bug · removing the per-bundle miracle bound lets a role with no budget fold",
        "RULE 1 red-on-bug · removing the two-fold bound lets two miracles stand in one bundle",
        "RULE 2 (level ownership) · a travelling voice left nothing free by the ground is refused",
        "RULE 2 · a travelling voice on a level the ground does not hold is legal",
        "RULE 2 red-on-bug · removing the ownership check lets a voice own nothing and still play",
        "RULE 3 (tier budget) · a bundle whose realised tier outranks its role's own ceiling is "
        "refused",
        "RULE 3 · a bundle within its role's own tier and letter ceiling is legal",
        "RULE 3 red-on-bug · removing the tier/letter/accompaniment check passes everything",
        "RULE 4 (resource peak) · a bundle past the fleet's own richest published budget is refused",
        "RULE 4 · a bundle within the fleet's own richest published budget is legal",
        "RULE 4 red-on-bug · removing the resource ceiling check passes an overrun bundle",
        "RULE 5 (surface handover) · stubbed legal, on purpose, pending P3",
        "SCORE · structural colour carried by the arrival outweighs colour merely on the ground",
        "SCORE red-on-bug · collapsing the herald/bridge/arrival read makes the two indistinguishable",
        "RETURN VARIATION · naming the failure first — a decimal-suffixed key alone still just "
        "re-derives passIndex's own parity through dieAmong's degenerate n=2 reduction",
        "RETURN VARIATION · the widened per-passIndex die no longer collapses to two alternating "
        "states",
        "STRUCTURE · the new P1.2 code names no cache or table keyed across pairs",
        "P4 · shared directional guides gently strengthen an already viable box fold",
        "P4 red-on-bug · removing the guide corroboration leaves its ranking unchanged",
    ):
        skip(_n, "node is not on this machine")
else:
    # ============================================================================ P4 / work guides
    # Guides are part of each work's wire record, not a precomputed pair classification.  Start
    # with a real fixture pair whose departing work already has panels, add the same high-confidence
    # direction to both records, and ask the real composer for its candidates.  This proves that the
    # optional guide can support an existing fold reading, while its absence still leaves the genre
    # available; the plant then removes only the corroborating assignment.
    p4_from = copy.deepcopy(FIX["works"][FIX["pair"]["a"]])
    p4_to = copy.deepcopy(FIX["works"][FIX["pair"]["b"]])
    p4_plain = run("genresFor", [p4_from, p4_to])
    guide = {"edge": {"coherence": 1, "straightness": 1, "angleDeg": 0}}
    p4_from["guides"] = copy.deepcopy(guide)
    p4_to["guides"] = copy.deepcopy(guide)
    p4_guided = run("genresFor", [p4_from, p4_to])

    def box_fit(reading):
        for genre in reading.get("genres", []):
            if genre.get("id") == "box-fold":
                return genre.get("fit"), genre.get("why", "")
        return None, ""

    p4_plain_fit, _p4_plain_why = box_fit(p4_plain)
    p4_guided_fit, p4_guided_why = box_fit(p4_guided)
    check("P4 · shared directional guides gently strengthen an already viable box fold",
          isinstance(p4_plain_fit, (int, float)) and isinstance(p4_guided_fit, (int, float))
          and p4_plain_fit > 0 and p4_guided_fit > p4_plain_fit
          and "measured edge directions agree" in p4_guided_why,
          "plain=%s guided=%s why=%s" % (p4_plain_fit, p4_guided_fit, p4_guided_why))

    p4_broken = run("genresFor", [p4_from, p4_to], plants=[[
        "boxFit = corroboratedFit(boxFit, guidePair);", "boxFit = boxFit;"
    ]])
    p4_broken_fit, _p4_broken_why = box_fit(p4_broken)

    # The fixture's own works now carry real, measured `guides.edge` data of their own — `p4_plain`
    # above already reads a small (non-zero) guide corroboration baked into that real data, so it is
    # no longer the right target for "corroboration fully removed". The right target is a pair with
    # no guide reading AT ALL (support=0, under which corroboratedFit is a no-op by construction —
    # see the docstring on corroboratedFit above `base + base * (1 - base) * 0 == base`), so the
    # planted (no-op) line and a genuinely guideless pair must land on the exact same fit.
    p4_from_noguide = copy.deepcopy(FIX["works"][FIX["pair"]["a"]])
    p4_to_noguide = copy.deepcopy(FIX["works"][FIX["pair"]["b"]])
    p4_from_noguide.pop("guides", None)
    p4_to_noguide.pop("guides", None)
    p4_noguide = run("genresFor", [p4_from_noguide, p4_to_noguide])
    p4_noguide_fit, _p4_noguide_why = box_fit(p4_noguide)

    if p4_broken.get("missed"):
        skip("P4 red-on-bug · removing the guide corroboration leaves its ranking unchanged",
             "the corroborating assignment is not in the shipped source")
    else:
        check("P4 red-on-bug · removing the guide corroboration leaves its ranking unchanged",
              p4_broken_fit == p4_noguide_fit and p4_broken_fit != p4_guided_fit,
              "noguide=%s guided=%s planted=%s (plain, with the fixture's own small real guide "
              "reading baked in, was %s)" %
              (p4_noguide_fit, p4_guided_fit, p4_broken_fit, p4_plain_fit))

    # ================================================================================= RULE 1
    NO_MIRACLE = {"tier": "quiet", "miracle": False, "letters": 1}
    MAY_MIRACLE = {"tier": "middle", "miracle": True, "letters": 2}

    r1a = run("bundleWorldLegal", ["boxfold", None, None, None, NO_MIRACLE])
    check("RULE 1 (one WORLD) · a bundle with one fold and no miracle budget is refused",
          r1a.get("ok") is False,
          "" if r1a.get("ok") is False else
          "bundleWorldLegal('boxfold', null, null, null, {miracle:false}) read " + json.dumps(r1a))

    r1b = run("bundleWorldLegal", ["boxfold", "planet", None, None, MAY_MIRACLE])
    check("RULE 1 · two folding voices in one bundle are refused even where the role may spend one",
          r1b.get("ok") is False,
          "" if r1b.get("ok") is False else
          "bundleWorldLegal('boxfold', 'planet', null, null, {miracle:true}) read " + json.dumps(r1b))

    r1c = run("bundleWorldLegal", ["boxfold", None, None, None, MAY_MIRACLE])
    check("RULE 1 · a bundle with one fold and a role that may spend it is legal",
          r1c.get("ok") is True,
          "" if r1c.get("ok") is True else
          "bundleWorldLegal('boxfold', null, null, null, {miracle:true}) read " + json.dumps(r1c))

    PLANT_R1_ROLE = [["if (n > 0 && !roleBudget.miracle) {", "if (false) {"]]
    r1_broke_role = run("bundleWorldLegal", ["boxfold", None, None, None, NO_MIRACLE],
                        plants=PLANT_R1_ROLE)
    if r1_broke_role.get("missed"):
        skip("RULE 1 red-on-bug · removing the per-bundle miracle bound lets a role with no budget "
             "fold", "the guard this plant names is not in the shipped source")
    else:
        check("RULE 1 red-on-bug · removing the per-bundle miracle bound lets a role with no budget "
              "fold", r1_broke_role.get("ok") is True,
              "" if r1_broke_role.get("ok") is True else
              "the plant left the row above's own refusal standing, so it is not what the role's "
              "own miracle bound holds up")

    PLANT_R1_TWO = [["if (n > 1) {", "if (false) {"]]
    r1_broke_two = run("bundleWorldLegal", ["boxfold", "planet", None, None, MAY_MIRACLE],
                       plants=PLANT_R1_TWO)
    if r1_broke_two.get("missed"):
        skip("RULE 1 red-on-bug · removing the two-fold bound lets two miracles stand in one bundle",
             "the guard this plant names is not in the shipped source")
    else:
        check("RULE 1 red-on-bug · removing the two-fold bound lets two miracles stand in one bundle",
              r1_broke_two.get("ok") is True,
              "" if r1_broke_two.get("ok") is True else
              "the plant left the two-fold refusal standing, so it is not what shelf 6's one-slot "
              "law holds up")

    # ================================================================================= RULE 2
    # `beat` and `droste` both declare exactly one level, SURFACE, and nothing else — the ground's
    # own window is always [0, 1], so a travelling voice on the same one level, live at any point
    # inside that whole span, owns nothing free.
    entries_bad = [{"id": "beat", "window": [0, 1]}, {"id": "droste", "window": [0, 0.5]}]
    r2a = run("bundleLevelsLegal", [entries_bad])
    check("RULE 2 (level ownership) · a travelling voice left nothing free by the ground is refused",
          r2a.get("ok") is False,
          "" if r2a.get("ok") is False else
          "bundleLevelsLegal(beat@[0,1], droste@[0,0.5]) read " + json.dumps(r2a))

    entries_good = [{"id": "beat", "window": [0, 1]}, {"id": "overlay", "window": [0, 0.5]}]
    r2b = run("bundleLevelsLegal", [entries_good])
    check("RULE 2 · a travelling voice on a level the ground does not hold is legal",
          r2b.get("ok") is True,
          "" if r2b.get("ok") is True else
          "bundleLevelsLegal(beat@[0,1], overlay@[0,0.5]) read " + json.dumps(r2b))

    PLANT_R2 = [
        ["if (!hasFree) refused = entries[i].id;", "if (false) refused = entries[i].id;"],
    ]
    r2_broke = run("bundleLevelsLegal", [entries_bad], plants=PLANT_R2)
    if r2_broke.get("missed"):
        skip("RULE 2 red-on-bug · removing the ownership check lets a voice own nothing and still "
             "play", "the guard this plant names is not in the shipped source")
    else:
        check("RULE 2 red-on-bug · removing the ownership check lets a voice own nothing and still "
              "play", r2_broke.get("ok") is True,
              "" if r2_broke.get("ok") is True else
              "the plant left the refusal standing, so it is not what the ownership check holds up")

    # ================================================================================= RULE 3
    QUIET = {"tier": "quiet", "miracle": False, "letters": 1}
    MIDDLE = {"tier": "middle", "miracle": True, "letters": 2}

    r3a = run("bundleTierLegal", [True, True, None, "quiet link", None, QUIET, False, False])
    check("RULE 3 (tier budget) · a bundle whose realised tier outranks its role's own ceiling is "
          "refused", r3a.get("ok") is False,
          "" if r3a.get("ok") is False else
          "bundleTierLegal(travel+arrival, role=quiet link) read " + json.dumps(r3a))

    r3b = run("bundleTierLegal", [True, False, None, "middle", None, MIDDLE, False, False])
    check("RULE 3 · a bundle within its role's own tier and letter ceiling is legal",
          r3b.get("ok") is True,
          "" if r3b.get("ok") is True else
          "bundleTierLegal(travel only, role=middle) read " + json.dumps(r3b))

    PLANT_R3 = [
        ["var ok = letters <= roleBudget.letters && countedAccs <= accCeiling\n"
         "        && TIER_RANK[tier] <= TIER_RANK[roleBudget.tier];",
         "var ok = true;"],
    ]
    r3_broke = run("bundleTierLegal", [True, True, None, "quiet link", None, QUIET, False, False],
                  plants=PLANT_R3)
    if r3_broke.get("missed"):
        skip("RULE 3 red-on-bug · removing the tier/letter/accompaniment check passes everything",
             "the guard this plant names is not in the shipped source")
    else:
        check("RULE 3 red-on-bug · removing the tier/letter/accompaniment check passes everything",
              r3_broke.get("ok") is True,
              "" if r3_broke.get("ok") is True else
              "the plant left the refusal standing, so it is not what the tier budget check holds up")

    # ================================================================================= RULE 4
    # `boxfold`'s own "rich" resources are overridden to a value past every published ceiling — a
    # synthetic input, on purpose: the fleet's real manifests never near this rule today (the note
    # over RESOURCE_CEILING says so), so a real-corpus witness would prove nothing about the rule
    # itself and this rule needs its own witness rather than an accident of what the corpus happens
    # to declare.
    consts_over = json.loads(json.dumps(FIX["consts"]))
    consts_over["manifests"]["boxfold"]["resources"]["rich"]["bytesEstimate"] = 999999999
    r4a = run("bundleResourcesLegal", [["boxfold"]], consts=consts_over)
    check("RULE 4 (resource peak) · a bundle past the fleet's own richest published budget is "
          "refused", r4a.get("ok") is False,
          "" if r4a.get("ok") is False else
          "bundleResourcesLegal(['boxfold']) with bytesEstimate=999999999 read " + json.dumps(r4a))

    r4b = run("bundleResourcesLegal", [["boxfold"]])
    check("RULE 4 · a bundle within the fleet's own richest published budget is legal",
          r4b.get("ok") is True,
          "" if r4b.get("ok") is True else
          "bundleResourcesLegal(['boxfold']) on the shipped fixture read " + json.dumps(r4b))

    PLANT_R4 = [
        ["return { ok: over === null, why: over === null ? null",
         "return { ok: true, why: over === null ? null"],
    ]
    r4_broke = run("bundleResourcesLegal", [["boxfold"]], plants=PLANT_R4, consts=consts_over)
    if r4_broke.get("missed"):
        skip("RULE 4 red-on-bug · removing the resource ceiling check passes an overrun bundle",
             "the guard this plant names is not in the shipped source")
    else:
        check("RULE 4 red-on-bug · removing the resource ceiling check passes an overrun bundle",
              r4_broke.get("ok") is True,
              "" if r4_broke.get("ok") is True else
              "the plant left the refusal standing, so it is not what the resource ceiling check "
              "holds up")

    # ================================================================================= RULE 5
    r5 = run("surfaceHandoverLegal", [])
    check("RULE 5 (surface handover) · stubbed legal, on purpose, pending P3",
          r5.get("ok") is True, "" if r5.get("ok") is True else json.dumps(r5))

    # ================================================================================= SCORE
    # `overlay` declares exactly LIGHT-COLOUR and nothing else; `beat` declares exactly SURFACE and
    # nothing else — the two bundles below cast the identical PAIR of instruments, one as ground and
    # one as arrival, only swapped, so every other term `scoreBundle` reads (the second-voice bonus,
    # the arrival's own +1) is identical between them and the only thing that can move the score is
    # WHICH of the two carries LIGHT-COLOUR: the arrival (shelf 11's amendment — colour carries the
    # herald/bridge/arrival) or the ground (colour merely riding along).
    s_leads = run("scoreBundle", ["beat", None, "overlay", True, "middle", True])
    s_ground = run("scoreBundle", ["overlay", None, "beat", True, "middle", True])
    ok_score = (isinstance(s_leads, int) and isinstance(s_ground, int) and s_leads - s_ground == 5)
    check("SCORE · structural colour carried by the arrival outweighs colour merely on the ground",
          ok_score,
          "" if ok_score else
          "scoreBundle with colour on the arrival (ground=beat, arrival=overlay) read "
          + json.dumps(s_leads) + "; the identical pair swapped (ground=overlay, arrival=beat) "
          + "read " + json.dumps(s_ground) + " — the gap should be exactly 5 (6 vs 1), never a wash")

    PLANT_SCORE = [
        ["score += (singer && singer !== g) ? 6 : 1;", "score += 1;"],
    ]
    s_leads_broke = run("scoreBundle", ["beat", None, "overlay", True, "middle", True],
                       plants=PLANT_SCORE)
    s_ground_broke = run("scoreBundle", ["overlay", None, "beat", True, "middle", True],
                        plants=PLANT_SCORE)
    if isinstance(s_leads_broke, dict) and s_leads_broke.get("missed"):
        skip("SCORE red-on-bug · collapsing the herald/bridge/arrival read makes the two "
             "indistinguishable", "the line this plant names is not in the shipped source")
    else:
        collapsed = (s_leads_broke == s_ground_broke)
        check("SCORE red-on-bug · collapsing the herald/bridge/arrival read makes the two "
              "indistinguishable", collapsed,
              "" if collapsed else
              "even under the plant the two scores still differ (" + json.dumps(s_leads_broke) + " "
              "vs " + json.dumps(s_ground_broke) + "), so the row above is not measuring the "
              "herald/bridge/arrival read this plant removes")

    # ========================================================================= P2 / route function
    # `overlay` owns a level `beat` does not. The same legal two-voice phrase receives P1.2's
    # existing ten-point second-voice preference at a dominant station and none at tonic; no density
    # is forced at tonic just because the broad visual role happens to be called "middle".
    dominant_voice = run("scoreBundle", ["beat", None, "overlay", False, "middle", False,
                                           "dominant"])
    tonic_voice = run("scoreBundle", ["beat", None, "overlay", False, "middle", False,
                                        "tonic"])
    check("P2 ROUTE FUNCTION · a dominant raises a legal distinct second voice over the same tonic phrase",
          dominant_voice == tonic_voice + 10,
          "dominant=" + json.dumps(dominant_voice) + ", tonic=" + json.dumps(tonic_voice))

    dominant_broke = run("scoreBundle", ["beat", None, "overlay", False, "middle", False,
                                          "dominant"],
                         plants=[["if (routeFunction === \"dominant\" && secondVoice) score += 10;",
                                  "if (false) score += 10;"]])
    if isinstance(dominant_broke, dict) and dominant_broke.get("missed"):
        skip("P2 ROUTE FUNCTION red-on-bug · removing the dominant bonus removes the lift",
             "the route-function guard this plant names is not in the shipped source")
    else:
        check("P2 ROUTE FUNCTION red-on-bug · removing the dominant bonus removes the lift",
              dominant_broke == tonic_voice,
              "planted dominant=" + json.dumps(dominant_broke) + ", tonic=" + json.dumps(tonic_voice))

    # The same function must reach the real composer entry and its diagnostic ledger, not only the
    # exposed scorer used above. The fixture is two real WorkRecords; this names no pair table and
    # asks one runtime composition directly.
    pair_key = FIX["pair"]["a"] + "__" + FIX["pair"]["b"] + "__ab"
    composed_dominant = run("scoreFor", [FIX["works"][FIX["pair"]["a"]],
                                           FIX["works"][FIX["pair"]["b"]], "a-to-b",
                                           FIX["seeds"][pair_key], "middle", None, [], None,
                                           "dominant", None, [], []])
    diag = composed_dominant.get("diagnostics", {}) if isinstance(composed_dominant, dict) else {}
    ledger = diag.get("bundles") if isinstance(diag, dict) else None
    check("P2 ROUTE FUNCTION · the runtime score carries its dominant reading and actual bundle ledger",
          diag.get("routeFunction") == "dominant" and isinstance(ledger, dict)
          and isinstance(ledger.get("considered"), list) and ledger.get("winner") is not None,
          "runtime diagnostics=" + json.dumps(diag)[:800])

    # ============================================================================================
    # REAL-DATA PROOF, ONE SEARCH SERVING BOTH P1.2 items 1 and 2 (V2-CONVERGENCE-PLAN-2026-08-31
    # Phase 4). Everything above proves each rule and the score with hand-typed instrument ids and
    # hand-typed cue records — real proof the CODE holds the rule, no proof any REAL pair the planner
    # actually composes ever exercises it. This block runs the real, full `passageFor` entry over the
    # real 121-work fleet (`tests/fixture_pass_works.json`, never a hand-picked pair) and reads its
    # own `diagnostics.bundles.considered`/`.winner` — the joint planner's own ledger, at
    # `pass-composer.js`'s "THE FULL LEDGER, NEVER HIDDEN" comment — for a real candidate each rule
    # actually refused or actually won.
    #
    # THE SEARCH SUPPLIES ROUTEROLE/ROUTEFUNCTION THE WAY A LIVE ROUTE STEP DOES (Phase 6's own
    # finding, carried into this phase's brief): a station always states both together
    # (`engine/client/01a-pass.js:2010-2011`), and `routeRole` alone can flip which bundle wins
    # outright, so a search that only varies `workRecordA`/`workRecordB`/`seed` finds a DIFFERENT
    # result than what is actually live-cast for the same pair/seed. `cameraState` is left at its
    # cold-visit `null`: `pass-composer.js` reads it onto the diagnostic echo alone and touches no
    # legality or scoring decision with it (`grep cameraState engine/assets/pass-composer.js`), so a
    # DOM-derived pose has nothing to add to a search over what the COMPOSER decides.
    REAL_SEARCH_DRIVER = r"""
"use strict";
const vm = require("vm");
const source = %(source)s;
const consts = %(consts)s;
const works = %(works)s;

let joined = null;
const sandbox = { window: { __PassComposer: (m) => { joined = m; } }, console: console };
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: "pass-composer.js" });
const composer = joined.make(consts);

const ids = Object.keys(works);
// Every role/function pairing a live route station can actually send together (shelf 15's own map,
// `FUNCTION_OF_ROLE` in pass-composer.js, plus "middle"'s own crest exception it already reads).
const ROLE_FN = [["entrance", "subdominant"], ["quiet link", "tonic"], ["middle", "subdominant"],
                 ["middle", "dominant"], ["culmination", "dominant"], ["return", "tonic"]];
const SEEDS = [0, 3];

const goals = { colourPromo: null, rule1: null, rule2: null, rule3: null, rule4: null };
let neverFiresHandover = true;

outer:
for (let i = 0; i < ids.length; i++) {
  for (let j = 0; j < ids.length; j++) {
    if (i === j) continue;
    const from = ids[i], to = ids[j];
    for (const [role, fn] of ROLE_FN) {
      for (const seed of SEEDS) {
        const req = { workRecordA: works[from], workRecordB: works[to], direction: "a-to-b",
                      seed: seed, routeRole: role, routeFunction: fn, cameraState: null,
                      walkMemory: [], walkGenres: [], walkMiracles: [], framePace: null };
        let made;
        try { made = composer.passageFor(req); } catch (e) { continue; }
        if (!made || made.declined || !made.plan || !made.diagnostics
            || !made.diagnostics.bundles) continue;
        const bundles = made.diagnostics.bundles;
        const winner = bundles.winner;
        if (!goals.colourPromo && winner && winner.ok && winner.colour === true) {
          const g = winner.ground, t = winner.travel, a = winner.arrival;
          const levelsOf = (iid) => (iid && consts.manifests[iid]
            && consts.manifests[iid].levels) || [];
          const singer = [t, a, g].filter((iid) => iid
            && levelsOf(iid).indexOf("LIGHT-COLOUR") >= 0)[0];
          if (singer && singer !== g) {
            goals.colourPromo = { from: from, to: to, seed: seed, role: role, fn: fn,
                                   winner: winner, singer: singer };
          }
        }
        if (!goals.rule4 && winner && winner.ok && (winner.travel || winner.arrival)) {
          goals.rule4 = { from: from, to: to, seed: seed, role: role, fn: fn, winner: winner };
        }
        for (const row of bundles.considered || []) {
          if (!row.why) continue;
          if (row.why.indexOf("handover") >= 0) neverFiresHandover = false;
          if (!goals.rule1 && (row.why.indexOf("impossible event") >= 0
                               || row.why.indexOf("no miracle") >= 0)) {
            goals.rule1 = { from: from, to: to, seed: seed, role: role, fn: fn, row: row };
          }
          if (!goals.rule2 && row.why.indexOf("would own nothing free") >= 0) {
            goals.rule2 = { from: from, to: to, seed: seed, role: role, fn: fn, row: row };
          }
          if (!goals.rule3 && row.why.indexOf("does not take letters") >= 0) {
            goals.rule3 = { from: from, to: to, seed: seed, role: role, fn: fn, row: row };
          }
        }
      }
      if (goals.colourPromo && goals.rule1 && goals.rule2 && goals.rule3 && goals.rule4) break outer;
    }
  }
}
console.log(JSON.stringify({ goals: goals, neverFiresHandover: neverFiresHandover }));
"""

    def real_search():
        if not FIXTURE_WORKS.exists():
            return {"error": "tests/fixture_pass_works.json is not on this machine"}
        fix_works = json.loads(FIXTURE_WORKS.read_text(encoding="utf-8"))
        driver_text = REAL_SEARCH_DRIVER % {
            "source": json.dumps(RAW),
            "consts": json.dumps(FIX["consts"]),
            "works": json.dumps(fix_works["works"]),
        }
        driver_path = TMP / "bundle-real-search.js"
        driver_path.write_text(driver_text, encoding="utf-8")
        proc = subprocess.run(["node", str(driver_path)], capture_output=True, text=True,
                              timeout=180)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-1200:]}
        lines = (proc.stdout or "").strip().splitlines()
        if not lines:
            return {"error": "the search driver said nothing"}
        return json.loads(lines[-1])

    if not FIXTURE_WORKS.exists():
        for _n in (
            "REAL DATA · item 1 — a real planner-composed pair casts structural colour on travel "
            "or arrival",
            "REAL DATA red-on-bug · reverting the +6/+1 split on that same real bundle collapses "
            "the two",
            "REAL DATA · item 2 RULE 1 — a real composed candidate is refused for spending the "
            "one miracle at a role shelf 17 gives none",
            "REAL DATA · item 2 RULE 2 — a real composed candidate is refused because a voice "
            "owns nothing free",
            "REAL DATA · item 2 RULE 3 — a real composed candidate is refused past its role's own "
            "tier/letter ceiling",
            "REAL DATA · item 2 RULE 4 — a real composed winner's own cast clears the fleet's "
            "richest published resource budget",
            "REAL DATA · item 2 RULE 5 — across every real candidate this search considered, the "
            "still-stubbed surface-handover check never once refuses one",
        ):
            skip(_n, "tests/fixture_pass_works.json is not on this machine")
    else:
        _search = real_search()
        _goals = _search.get("goals") if isinstance(_search, dict) else None
        if not isinstance(_goals, dict):
            for _n in (
                "REAL DATA · item 1 — a real planner-composed pair casts structural colour on "
                "travel or arrival",
                "REAL DATA red-on-bug · reverting the +6/+1 split on that same real bundle "
                "collapses the two",
                "REAL DATA · item 2 RULE 1 — a real composed candidate is refused for spending "
                "the one miracle at a role shelf 17 gives none",
                "REAL DATA · item 2 RULE 2 — a real composed candidate is refused because a "
                "voice owns nothing free",
                "REAL DATA · item 2 RULE 3 — a real composed candidate is refused past its "
                "role's own tier/letter ceiling",
                "REAL DATA · item 2 RULE 4 — a real composed winner's own cast clears the "
                "fleet's richest published resource budget",
                "REAL DATA · item 2 RULE 5 — across every real candidate this search "
                "considered, the still-stubbed surface-handover check never once refuses one",
            ):
                skip(_n, "the real search itself failed: " + json.dumps(_search)[:800])
        else:
            # ---- item 1: the +6/+1 herald/bridge/arrival promotion, on a real found bundle -------
            promo = _goals.get("colourPromo")
            if not promo:
                skip("REAL DATA · item 1 — a real planner-composed pair casts structural colour "
                     "on travel or arrival",
                     "the search found no real pair whose composed winner carries colour off the "
                     "ground")
                skip("REAL DATA red-on-bug · reverting the +6/+1 split on that same real bundle "
                     "collapses the two", "no real pair found above to replant")
            else:
                w = promo["winner"]
                g_id, t_id, a_id = w["ground"], w["travel"], w["arrival"]
                role, fn = promo["role"], promo["fn"]
                real_leads = run("scoreBundle", [g_id, t_id, a_id, True, role, True, fn])
                real_ground = run("scoreBundle", [promo["singer"],
                                                    g_id if promo["singer"] != g_id else t_id,
                                                    a_id, True, role, True, fn])
                real_ok = (isinstance(real_leads, int) and isinstance(real_ground, int)
                          and real_leads - real_ground == 5)
                check("REAL DATA · item 1 — a real planner-composed pair casts structural colour "
                      "on travel or arrival",
                      real_ok,
                      "real pair %s→%s (seed %s, role %s/%s): the planner's own winner casts "
                      "ground=%s travel=%s arrival=%s colour=on, singer=«%s» (not the ground); "
                      "scoreBundle reads %s carrying colour off the ground and %s with the same "
                      "singer swapped onto it — the gap should be exactly 5 (6 vs 1)"
                      % (promo["from"], promo["to"], promo["seed"], role, fn, g_id, t_id, a_id,
                         promo["singer"], real_leads, real_ground))
                real_leads_broke = run("scoreBundle", [g_id, t_id, a_id, True, role, True, fn],
                                       plants=PLANT_SCORE)
                real_ground_broke = run("scoreBundle",
                                        [promo["singer"], g_id if promo["singer"] != g_id else t_id,
                                         a_id, True, role, True, fn], plants=PLANT_SCORE)
                if isinstance(real_leads_broke, dict) and real_leads_broke.get("missed"):
                    skip("REAL DATA red-on-bug · reverting the +6/+1 split on that same real "
                         "bundle collapses the two",
                         "the line this plant names is not in the shipped source")
                else:
                    collapsed_real = (real_leads_broke == real_ground_broke)
                    check("REAL DATA red-on-bug · reverting the +6/+1 split on that same real "
                          "bundle collapses the two", collapsed_real,
                          "" if collapsed_real else
                          "even reverted to +1/+1 the same real bundle's two readings still "
                          "differ (" + json.dumps(real_leads_broke) + " vs "
                          + json.dumps(real_ground_broke) + ")")

            # ---- item 2: one real-pair-driven witness per named legality rule -------------------
            r1 = _goals.get("rule1")
            check("REAL DATA · item 2 RULE 1 — a real composed candidate is refused for spending "
                  "the one miracle at a role shelf 17 gives none",
                  isinstance(r1, dict) and r1.get("row", {}).get("ok") is False,
                  ("real pair %s→%s (seed %s, role %s): the planner's own real candidate ground=%s "
                   "travel=%s arrival=%s was refused, why=%s"
                   % (r1["from"], r1["to"], r1["seed"], r1["role"], r1["row"]["ground"],
                      r1["row"]["travel"], r1["row"]["arrival"], r1["row"]["why"]))
                  if isinstance(r1, dict) else
                  "the search found no real candidate this rule ever refused")

            r2 = _goals.get("rule2")
            check("REAL DATA · item 2 RULE 2 — a real composed candidate is refused because a "
                  "voice owns nothing free",
                  isinstance(r2, dict) and r2.get("row", {}).get("ok") is False,
                  ("real pair %s→%s (seed %s, role %s): the planner's own real candidate ground=%s "
                   "travel=%s arrival=%s was refused, why=%s"
                   % (r2["from"], r2["to"], r2["seed"], r2["role"], r2["row"]["ground"],
                      r2["row"]["travel"], r2["row"]["arrival"], r2["row"]["why"]))
                  if isinstance(r2, dict) else
                  "the search found no real candidate this rule ever refused")

            r3 = _goals.get("rule3")
            check("REAL DATA · item 2 RULE 3 — a real composed candidate is refused past its "
                  "role's own tier/letter ceiling",
                  isinstance(r3, dict) and r3.get("row", {}).get("ok") is False,
                  ("real pair %s→%s (seed %s, role %s): the planner's own real candidate ground=%s "
                   "travel=%s arrival=%s was refused, why=%s"
                   % (r3["from"], r3["to"], r3["seed"], r3["role"], r3["row"]["ground"],
                      r3["row"]["travel"], r3["row"]["arrival"], r3["row"]["why"]))
                  if isinstance(r3, dict) else
                  "the search found no real candidate this rule ever refused")

            # RULE 4 never refuses on this fleet's own real manifests (the rule's own comment says
            # so — every real cast stands well under the fleet's richest published budget), so its
            # real-data witness is a real WINNING cast's own ids run straight through the exposed
            # rule, in place of the literal ['boxfold'] the synthetic RULE 4 rows above hand-type.
            r4 = _goals.get("rule4")
            if not r4:
                skip("REAL DATA · item 2 RULE 4 — a real composed winner's own cast clears the "
                     "fleet's richest published resource budget",
                     "the search found no real legal winner with a travel or arrival voice")
            else:
                w4 = r4["winner"]
                real_ids = [iid for iid in (w4["ground"], w4["travel"], w4["arrival"]) if iid]
                r4_out = run("bundleResourcesLegal", [real_ids])
                check("REAL DATA · item 2 RULE 4 — a real composed winner's own cast clears the "
                      "fleet's richest published resource budget",
                      r4_out.get("ok") is True,
                      "bundleResourcesLegal(%s), the real planner's own winning cast for %s→%s "
                      "(seed %s, role %s), read %s"
                      % (json.dumps(real_ids), r4["from"], r4["to"], r4["seed"], r4["role"],
                         json.dumps(r4_out)))

            # RULE 5 is still the Phase-2-revisited stub (`function surfaceHandoverLegal() { "
            # "return { ok: true, why: null }; }`) — what it DOES, proved on real data, is refuse
            # nothing: across every real candidate this whole search's own ledger considered (every
            # role/function/pair/seed tried above), no `why` ever named a surface-handover refusal.
            check("REAL DATA · item 2 RULE 5 — across every real candidate this search considered, "
                  "the still-stubbed surface-handover check never once refuses one",
                  _goals is not None and bool(_search.get("neverFiresHandover")),
                  "" if _search.get("neverFiresHandover") else
                  "a real candidate's own why-string named a surface-handover refusal, which the "
                  "shipped stub can never produce — re-check that RULE 5 is still the stub this "
                  "row assumes")

    # ========================================================================= RETURN VARIATION
    # The old formula read `dieAmong(seed, key + "|moves", 2)` — one die value regardless of
    # `passIndex` — so only `(passIndex + dieValue) % 2`'s own PARITY moved: EVERY odd return drew
    # the identical flip and every even one the identical no-flip, whatever the actual pass index,
    # because `(1+d)%2 === (3+d)%2 === (5+d)%2` for any fixed `d`.
    #
    # FOLDING `passIndex` INTO THE KEY ALONE DOES NOT FIX THIS, and the row below proves it before
    # proving the real fix: `dieAmong`'s own hash is an XOR-then-multiply-by-an-ODD-constant chain,
    # which makes the raw result's lowest bit a pure XOR of the salt string's own character codes —
    # asking it for a die of 2 on a key ending in the decimal `passIndex` reads next to nothing but
    # that digit's own parity, so `dieAmong(seed, key + "|moves|" + passIndex, 2)` still just
    # re-derives `passIndex % 2` by another road. The actual fix reads a WIDE die first (1009, a
    # prime unrelated to 2) and takes ITS OWN parity, which mixes far more of the hash before the
    # last, degenerate reduction.
    naive_locked = True
    for trial in range(10):
        seed, key = 1000 + trial * 37, "work%d__work%d__ab" % (trial, trial + 1)
        n1 = run("dieAmong", [seed, key + "|moves|1", 2])
        n3 = run("dieAmong", [seed, key + "|moves|3", 2])
        if n1 != n3:
            naive_locked = False
            break
    check("RETURN VARIATION · naming the failure first — a decimal-suffixed key alone still just "
          "re-derives passIndex's own parity through dieAmong's degenerate n=2 reduction",
          naive_locked,
          "" if naive_locked else
          "the naive `dieAmong(seed, key+'|moves|'+passIndex, 2)` no longer collapses on its own — "
          "if `dieAmong`'s own hash changed, the note above and the real fix's own reasoning need "
          "re-checking")

    broke_parity = False
    witness = None
    for trial in range(30):
        seed, key = 1000 + trial * 37, "work%d__work%d__ab" % (trial, trial + 1)
        d1 = run("dieAmong", [seed, key + "|moves|1", 1009])
        d3 = run("dieAmong", [seed, key + "|moves|3", 1009])
        d1, d3 = d1 % 2, d3 % 2
        if d1 != d3:
            broke_parity = True
            witness = (seed, key, d1, d3)
            break
    check("RETURN VARIATION · the widened per-passIndex die no longer collapses to two alternating "
          "states", broke_parity,
          "" if broke_parity else
          "over 30 (seed, key) pairs, dieAmong at passIndex 1 and passIndex 3 (both odd under the "
          "old scheme) always agreed — the old parity collapse is still there")

    # ==================================================================== STRUCTURE / no pair table
    # A code-level check beside R4's comment-level shelf-20 sweep in test_pass_lawful.py: the new
    # P1.2 block introduces no module-level cache or table indexed by a pair, and no loop over the
    # collection of works. Extracted by the same balanced-brace/name markers the block itself
    # carries, so a reviewer moving this code keeps the sweep honest without hand-editing a line
    # range here.
    p12_start = RAW.index("P1.2 — THE JOINT PHRASE PLANNER'S OWN LEGALITY RULES")
    p12_end = RAW.index("function scoreBundle(g, t, a, colourOn, role, singsHere, routeFunction) {",
                        p12_start)
    p12_end = RAW.index("\n    }\n", p12_end) + len("\n    }\n")
    p12_block = RAW[p12_start:p12_end]
    forbidden = ["pairTable", "pairCache", "allPairs", "ALL_PAIRS", "precompute",
                 "for (var wi = 0; wi < WORKS", "for (var wi = 0; wi < works.length"]
    found = [f for f in forbidden if f in p12_block]
    check("STRUCTURE · the new P1.2 code names no cache or table keyed across pairs",
          not found,
          "" if not found else
          "the P1.2 block contains: " + ", ".join(found))

print("P1.2 — the joint phrase planner's own legality rules, score and return widening")
print("module: " + str(MODULE))
print()
passed = failed = skipped = 0
for name, status, detail in results:
    print(f"  {status:4}  {name}")
    if detail:
        for line in str(detail).splitlines():
            print(f"        {line}")
    if status == "PASS":
        passed += 1
    elif status == "FAIL":
        failed += 1
    else:
        skipped += 1
print()
print(f"  {passed} pass, {failed} fail, {skipped} skip")
sys.exit(1 if failed else 0)
