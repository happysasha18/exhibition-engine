#!/usr/bin/env python3
"""P1.3 — connecting `record.symmetry` and `record.matter`/`record.substance`, read by no line
of pass-composer.js before this phase, into the genre fit `genresFor` already ranks bundles on.

Run: python3 tests/test_pass_p13.py

Root: his 2026-08-28 P1.3 brief, on top of P1.2's joint bundle planner (test_pass_bundle.py).
Verified before this phase, by grep: each WorkRecord already carries `record.symmetry` (reflection
axes with their own `reading` correlation, rotation order and reading, translation) and
`record.matter`/`record.substance` (material, second material, substance, with
`materialVotes`/`substanceVotes` — 2-of-3 or 3-of-3 agreement — as the record's own explicit
confidence), both computed by lab/build-workrecords-v1.py (tlvphotos-site repo) and read by zero
lines of this composer. This phase connects both as confidence-carrying corroboration of the fit
`genresFor` already ranks bundles by — never as a new gate, per shelf 9 (a measurement ranks, it
never gates). Its arithmetic has no made-up weight: a supporting reading occupies only the
structural fit's own unused headroom, in proportion to that structural fit.

THE ROAD THIS FILE WALKS. Same driver idiom as test_pass_bundle.py: the real, loaded `MANIFESTS`
and `genresFor` itself, exposed off `make(consts)`'s own returned object, run once per job in a
fresh `vm` context — never a retyped mirror of the ranking arithmetic.

WHAT EACH SECTION PROVES:
  (a) SYMMETRY   — a structural check that `genresFor`'s box-fold and kaleidoscope branches call the
                   new `strongestReflection`/`rotationReading` functions, plus a behavioural sweep:
                   two works sharing a strong symmetry axis rank higher than two that do not, exactly
                   by the source's no-constant corroboration law, and a work with too few faces to fold or
                   an arrival not on rings is NEVER pushed above zero by symmetry alone (never oblige
                   a box).
  (b) MATTER     — the same two-part proof for `record.matter`/`record.materialSecond`/
                   `record.substance` on the
                   shared-ground genre, plus a THIRD point on the sweep showing a low-confidence vote
                   (materialVotes=2) nudges less than a high-confidence one (materialVotes=3) on an
                   otherwise identical pair — the vote count IS the confidence, read directly.
  (c) ABSENCE    — a WorkRecord missing `symmetry` or `matter` entirely never crashes `genresFor` and
                   never zeroes a fit structure already gave it; it just ranks without that cause.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"

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

TMP = Path(tempfile.mkdtemp(prefix="pass_p13_"))
DRIVER = TMP / "p13-driver.js"

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


def genre_fit(fromW, toW, genre_id, plants=None):
    out = run("genresFor", [fromW, toW], plants=plants)
    if isinstance(out, dict) and out.get("error"):
        return None, out
    if isinstance(out, dict) and out.get("missed"):
        return None, out
    hit = [g for g in out["genres"] if g["id"] == genre_id]
    if not hit:
        return None, out
    return hit[0]["fit"], out


# ── synthetic WorkRecords, minimal but real-shaped ──────────────────────────────────────────────
def reflection_block(reading):
    axis = {"axisX": 0.5, "inRecipe": reading > 0.7, "reading": reading, "diffScore": 0.8}
    return {"leftOntoRight": dict(axis), "topOntoBottom": dict(axis),
            "mainDiagonal": dict(axis), "antiDiagonal": dict(axis)}


def box_work(refl_reading, faces=3, regions_score=0.5):
    return {
        "id": "synthA",
        "measures": {},
        "structure": {"regions": {"score": regions_score, "count": faces}},
        "sets": [{"kind": "panel", "realCount": faces}],
        "symmetry": {"reflection": reflection_block(refl_reading),
                     "rotation": {"order": 1, "reading": 0}, "translation": {}, "glide": None},
    }


def ring_work(rot_reading, radial_score=0.6, sub_type="ring"):
    return {
        "id": "synthB",
        "measures": {},
        "structure": {"radial": {"score": radial_score, "centre": [0.5, 0.5], "subType": sub_type}},
        "sets": [],
        "symmetry": {"reflection": reflection_block(0), "rotation": {"order": 4, "reading": rot_reading},
                     "translation": {}, "glide": None},
    }


def ground_work(wid, regions_score=0.7, banding_score=0.5, matter=None):
    w = {
        "id": wid,
        "measures": {"regions": regions_score, "banding": banding_score},
        "structure": {"regions": {"score": regions_score, "count": 3},
                      "banding": {"score": banding_score, "axis": "horizontal", "periodPx": 100}},
        "sets": [],
    }
    if matter is not None:
        w["matter"] = matter
    return w


if not NODE:
    for _n in (
        "SYMMETRY structural · genresFor's box-fold/kaleidoscope branches call the new symmetry "
        "readers",
        "SYMMETRY behavioural · a strong shared reflection ranks box-fold measurably higher than a "
        "weak one, through the base fit's own unused headroom",
        "SYMMETRY never-oblige · too few faces to fold keeps box-fold at zero however strong the "
        "shared reflection reads",
        "SYMMETRY behavioural (kaleidoscope) · a strong shared rotational reading ranks the rings "
        "road measurably higher than a weak one",
        "SYMMETRY never-oblige (kaleidoscope) · an arrival not on rings keeps kaleidoscope at zero "
        "however strong the shared rotation reads",
        "MATTER structural · genresFor's shared-ground branch calls the new matterAgreement reader",
        "MATTER behavioural · two works agreeing on material rank shared-ground higher than two that "
        "disagree, through the existing shared-ground fit's own headroom",
        "MATTER confidence · a low-confidence vote (2 of 3) nudges shared-ground less than a "
        "high-confidence one (3 of 3) on an otherwise identical pair",
        "RED-ON-BUG (box-fold) · removing the reflection corroboration collapses strong back to the "
        "unweighted base",
        "RED-ON-BUG (kaleidoscope) · removing the rotation corroboration collapses strong back to the "
        "unweighted base",
        "RED-ON-BUG (shared-ground) · removing the matter corroboration collapses the matched pair back to "
        "the unweighted base",
        "ABSENCE · a WorkRecord missing `symmetry` entirely still produces a legal, non-crashing "
        "genresFor reading",
        "ABSENCE · a WorkRecord missing `matter` entirely still produces a legal, non-crashing "
        "genresFor reading",
        "ABSENCE · missing symmetry/matter never lowers a fit structure already gave — it only "
        "withholds the corroboration",
    ):
        skip(_n, "node is not on this machine")
else:
    # ================================================================================= SYMMETRY
    p13_start = RAW.index("P1.3 — RECORD.SYMMETRY AND RECORD.MATTER")
    genres_for_start = RAW.index("function genresFor(fromW, toW) {", p13_start)
    genres_for_end = RAW.index("\n    function facesOf(", genres_for_start)
    genres_for_block = RAW[genres_for_start:genres_for_end]
    wired = ("strongestReflection(fromW)" in genres_for_block
             and "strongestReflection(toW)" in genres_for_block
             and "rotationReading(fromW)" in genres_for_block
             and "rotationReading(toW)" in genres_for_block)
    check("SYMMETRY structural · genresFor's box-fold/kaleidoscope branches call the new symmetry "
          "readers", wired,
          "" if wired else "expected strongestReflection(fromW/toW) inside box-fold and "
          "rotationReading(fromW/toW) inside kaleidoscope, inside genresFor's own source text")

    # P1.3 must not smuggle in a second, unexplained policy scale. The support takes only the
    # base fit's own unused headroom: base + base * (1 - base) * support. Every term comes from
    # the existing [0, 1] readings; no coefficient lives between them.
    p13_block = RAW[p13_start:genres_for_start]
    no_weight_knob = ("SYMMETRY_FOLD_WEIGHT" not in p13_block
                      and "MATTER_WEIGHT" not in p13_block
                      and "function corroboratedFit(baseFit, support)" in p13_block)
    check("P1.3 arithmetic · symmetry and matter use the base fit's own headroom, with no invented "
          "weight", no_weight_knob,
          "" if no_weight_knob else "P1.3 still contains a named arbitrary weight or lacks "
          "corroboratedFit(baseFit, support)")

    def corroborated(base, support):
        return base + base * (1.0 - base) * support

    weak_a, weak_b = box_work(0.0), box_work(0.0)
    strong_a, strong_b = box_work(0.9), box_work(0.9)
    fit_weak, out_weak = genre_fit(weak_a, weak_b, "box-fold")
    fit_strong, out_strong = genre_fit(strong_a, strong_b, "box-fold")
    base_fit = 0.5  # box_work's own regions_score default, read straight (readingOf is the identity
    # here since 0.5 is already inside [0,1])
    expected_strong = corroborated(base_fit, 0.9)
    ok = (fit_weak is not None and fit_strong is not None
          and abs(fit_weak - base_fit) < 1e-9
          and abs(fit_strong - expected_strong) < 1e-9
          and fit_strong > fit_weak)
    check("SYMMETRY behavioural · a strong shared reflection ranks box-fold measurably higher than a "
          "weak one, through the base fit's own unused headroom", ok,
          "" if ok else ("weak fit=%r (want %r), strong fit=%r (want %r); raw: weak=%s strong=%s"
                          % (fit_weak, base_fit, fit_strong, expected_strong,
                             json.dumps(out_weak), json.dumps(out_strong))))

    no_faces_a, no_faces_b = box_work(0.9, faces=1), box_work(0.9, faces=1)
    fit_no_faces, out_no_faces = genre_fit(no_faces_a, no_faces_b, "box-fold")
    ok = fit_no_faces == 0
    check("SYMMETRY never-oblige · too few faces to fold keeps box-fold at zero however strong the "
          "shared reflection reads", ok,
          "" if ok else "box-fold fit with faces=1 and reflection=0.9 read %r, want exactly 0 — "
          "symmetry alone must never oblige a box" % (fit_no_faces,) + " raw: " + json.dumps(out_no_faces))

    kal_weak_a, kal_weak_b = ring_work(0.0), ring_work(0.0)
    kal_strong_a, kal_strong_b = ring_work(0.85), ring_work(0.85)
    kfit_weak, kout_weak = genre_fit(kal_weak_a, kal_weak_b, "kaleidoscope")
    kfit_strong, kout_strong = genre_fit(kal_strong_a, kal_strong_b, "kaleidoscope")
    kal_base = 0.6  # ring_work's own radial_score default, both works identical so the pair reading
    # is that same value
    expected_kal_strong = corroborated(kal_base, 0.85)
    ok = (kfit_weak is not None and kfit_strong is not None
          and abs(kfit_weak - kal_base) < 1e-9
          and abs(kfit_strong - expected_kal_strong) < 1e-9
          and kfit_strong > kfit_weak)
    check("SYMMETRY behavioural (kaleidoscope) · a strong shared rotational reading ranks the rings "
          "road measurably higher than a weak one", ok,
          "" if ok else ("weak fit=%r (want %r), strong fit=%r (want %r); raw: weak=%s strong=%s"
                          % (kfit_weak, kal_base, kfit_strong, expected_kal_strong,
                             json.dumps(kout_weak), json.dumps(kout_strong))))

    kal_notring_a, kal_notring_b = ring_work(0.85, sub_type="angular"), ring_work(0.85, sub_type="angular")
    kfit_notring, kout_notring = genre_fit(kal_notring_a, kal_notring_b, "kaleidoscope")
    ok = kfit_notring == 0
    check("SYMMETRY never-oblige (kaleidoscope) · an arrival not on rings keeps kaleidoscope at zero "
          "however strong the shared rotation reads", ok,
          "" if ok else "kaleidoscope fit with subType=angular and rotation=0.85 read %r, want "
          "exactly 0" % (kfit_notring,) + " raw: " + json.dumps(kout_notring))

    # =================================================================================== MATTER
    shared_ground_start = RAW.index("function genresFor(fromW, toW) {")
    shared_ground_end = RAW.index("BUILT FROM HOW A RADIAL WORK IS MADE", shared_ground_start)
    sg_block = RAW[shared_ground_start:shared_ground_end]
    wired_matter = "matterAgreement(fromW, toW)" in sg_block
    check("MATTER structural · genresFor's shared-ground branch calls the new matterAgreement reader",
          wired_matter,
          "" if wired_matter else "expected matterAgreement(fromW, toW) inside shared-ground's own "
          "source text, before the radial section begins")

    nomatch_a = ground_work("gA", matter={"material": "wood", "materialSecond": None,
                                           "materialVotes": 3, "substance": ["bark"],
                                           "substanceVotes": {"bark": 3}})
    nomatch_b = ground_work("gB", matter={"material": "metal", "materialSecond": None,
                                           "materialVotes": 3, "substance": ["steel"],
                                           "substanceVotes": {"steel": 3}})
    match_low_a = ground_work("gA", matter={"material": "wood", "materialSecond": None,
                                             "materialVotes": 2, "substance": [],
                                             "substanceVotes": {}})
    match_low_b = ground_work("gB", matter={"material": "wood", "materialSecond": None,
                                             "materialVotes": 2, "substance": [],
                                             "substanceVotes": {}})
    match_high_a = ground_work("gA", matter={"material": "wood", "materialSecond": None,
                                              "materialVotes": 3, "substance": [],
                                              "substanceVotes": {}})
    match_high_b = ground_work("gB", matter={"material": "wood", "materialSecond": None,
                                              "materialVotes": 3, "substance": [],
                                              "substanceVotes": {}})
    # The record's primary and second material are two seats for the same measured fact. A shared
    # material must travel even when it sits primary in one work and secondary in the other — the
    # route ranks agreement, not a label's field position.
    match_second_a = ground_work("gA", matter={"material": "glass", "materialSecond": "metal",
                                                "materialVotes": 3, "substance": [],
                                                "substanceVotes": {}})
    match_second_b = ground_work("gB", matter={"material": "stone", "materialSecond": "glass",
                                                "materialVotes": 3, "substance": [],
                                                "substanceVotes": {}})

    fit_nomatch, out_nomatch = genre_fit(nomatch_a, nomatch_b, "shared-ground")
    fit_low, out_low = genre_fit(match_low_a, match_low_b, "shared-ground")
    fit_high, out_high = genre_fit(match_high_a, match_high_b, "shared-ground")
    fit_second, out_second = genre_fit(match_second_a, match_second_b, "shared-ground")

    gbase = 0.7  # ground_work's own regions_score default, held as the shared ground; banding at 0.5
    # on both is the nearest axis at delta 0, so closeness = 1 and the base fit is exactly gbase
    expected_nomatch = gbase
    expected_low = corroborated(gbase, 2.0 / 3.0)
    expected_high = corroborated(gbase, 1.0)

    ok = (fit_nomatch is not None and fit_low is not None and fit_high is not None and fit_second is not None
          and abs(fit_nomatch - expected_nomatch) < 1e-9
          and abs(fit_low - expected_low) < 1e-9
          and abs(fit_high - expected_high) < 1e-9
          and abs(fit_second - expected_high) < 1e-9)
    check("MATTER behavioural · two works agreeing on material rank shared-ground higher than two "
          "that disagree, through the existing shared-ground fit's own headroom", ok,
          "" if ok else ("nomatch=%r (want %r), low=%r (want %r), high=%r (want %r); raw: "
                          "nomatch=%s low=%s high=%s"
                          % (fit_nomatch, expected_nomatch, fit_low, expected_low, fit_high,
                             expected_high, json.dumps(out_nomatch), json.dumps(out_low),
                             json.dumps(out_high))))

    check("MATTER completeness · a shared material in primary/second seats ranks exactly like a "
          "shared primary material", fit_second is not None and abs(fit_second - expected_high) < 1e-9,
          "" if fit_second is not None and abs(fit_second - expected_high) < 1e-9 else
          "primary/second match read %r (want %r); raw=%s"
          % (fit_second, expected_high, json.dumps(out_second)))

    ok = (fit_low is not None and fit_high is not None and fit_nomatch is not None
          and fit_nomatch < fit_low < fit_high)
    check("MATTER confidence · a low-confidence vote (2 of 3) nudges shared-ground less than a "
          "high-confidence one (3 of 3) on an otherwise identical pair", ok,
          "" if ok else "expected nomatch < low-confidence-match < high-confidence-match, read "
          "%r < %r < %r" % (fit_nomatch, fit_low, fit_high))

    # ============================================================== RED-ON-BUG, THE THREE CORROBORATIONS
    # The same proof test_pass_bundle.py already uses for P1.2's own rules: a minimal, named
    # substring replacement that disables exactly one corroboration, applied to the identical
    # weak/strong pair above — showing the behavioural assertion actually depends on that line of
    # code, never on a name a reviewer could delete without a red test noticing.
    PLANT_BOX = [["boxFit = corroboratedFit(boxFit, reflPair);", "boxFit = boxFit;"]]
    fit_strong_broke, out_strong_broke = genre_fit(strong_a, strong_b, "box-fold", plants=PLANT_BOX)
    if isinstance(out_strong_broke, dict) and out_strong_broke.get("missed"):
        skip("RED-ON-BUG (box-fold) · removing the reflection corroboration collapses strong back to the "
             "unweighted base", "the line this plant names is not in the shipped source")
    else:
        collapsed = fit_strong_broke is not None and abs(fit_strong_broke - base_fit) < 1e-9
        check("RED-ON-BUG (box-fold) · removing the reflection corroboration collapses strong back to the "
              "unweighted base", collapsed,
              "" if collapsed else "under the plant, the 'strong reflection' pair still read %r "
              "instead of the base %r — the behavioural row above is not measuring this line"
              % (fit_strong_broke, base_fit))

    PLANT_KAL = [["kalFit = corroboratedFit(kalFit, rotPair);", "kalFit = kalFit;"]]
    kfit_strong_broke, kout_strong_broke = genre_fit(kal_strong_a, kal_strong_b, "kaleidoscope",
                                                      plants=PLANT_KAL)
    if isinstance(kout_strong_broke, dict) and kout_strong_broke.get("missed"):
        skip("RED-ON-BUG (kaleidoscope) · removing the rotation corroboration collapses strong back to the "
             "unweighted base", "the line this plant names is not in the shipped source")
    else:
        collapsed = kfit_strong_broke is not None and abs(kfit_strong_broke - kal_base) < 1e-9
        check("RED-ON-BUG (kaleidoscope) · removing the rotation corroboration collapses strong back to the "
              "unweighted base", collapsed,
              "" if collapsed else "under the plant, the 'strong rotation' pair still read %r "
              "instead of the base %r — the behavioural row above is not measuring this line"
              % (kfit_strong_broke, kal_base))

    PLANT_GROUND = [["groundFit = corroboratedFit(groundFit, matterShare);",
                      "groundFit = groundFit;"]]
    fit_high_broke, out_high_broke = genre_fit(match_high_a, match_high_b, "shared-ground",
                                                plants=PLANT_GROUND)
    if isinstance(out_high_broke, dict) and out_high_broke.get("missed"):
        skip("RED-ON-BUG (shared-ground) · removing the matter corroboration collapses the matched pair back "
             "to the unweighted base", "the line this plant names is not in the shipped source")
    else:
        collapsed = fit_high_broke is not None and abs(fit_high_broke - gbase) < 1e-9
        check("RED-ON-BUG (shared-ground) · removing the matter corroboration collapses the matched pair back "
              "to the unweighted base", collapsed,
              "" if collapsed else "under the plant, the high-confidence matter match still read %r "
              "instead of the base %r — the behavioural row above is not measuring this line"
              % (fit_high_broke, gbase))

    # ================================================================================== ABSENCE
    no_sym_a = box_work(0.9, faces=3)
    no_sym_b = box_work(0.9, faces=3)
    del no_sym_a["symmetry"]
    del no_sym_b["symmetry"]
    fit_no_sym, out_no_sym = genre_fit(no_sym_a, no_sym_b, "box-fold")
    ok = (isinstance(out_no_sym, dict) and not out_no_sym.get("error") and fit_no_sym is not None)
    check("ABSENCE · a WorkRecord missing `symmetry` entirely still produces a legal, non-crashing "
          "genresFor reading", ok,
          "" if ok else "raw: " + json.dumps(out_no_sym))
    ok2 = ok and abs(fit_no_sym - 0.5) < 1e-9
    check("ABSENCE · missing symmetry/matter never lowers a fit structure already gave — it only "
          "withholds the corroboration", ok2,
          "" if ok2 else "box-fold fit with symmetry entirely absent read %r, want exactly 0.5 "
          "(the base regions reading, no corroboration added or subtracted)" % (fit_no_sym,))

    no_matter_a = ground_work("gA")
    no_matter_b = ground_work("gB")
    assert "matter" not in no_matter_a and "matter" not in no_matter_b
    fit_no_matter, out_no_matter = genre_fit(no_matter_a, no_matter_b, "shared-ground")
    ok = (isinstance(out_no_matter, dict) and not out_no_matter.get("error")
          and fit_no_matter is not None and abs(fit_no_matter - gbase) < 1e-9)
    check("ABSENCE · a WorkRecord missing `matter` entirely still produces a legal, non-crashing "
          "genresFor reading", ok,
          "" if ok else "raw: " + json.dumps(out_no_matter))

print("P1.3 — record.symmetry and record.matter/record.substance connected into genresFor's ranking")
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
