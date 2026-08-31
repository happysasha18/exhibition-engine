#!/usr/bin/env python3
"""Cause A — the casting tier ladder ranks instead of gating (V2-CONVERGENCE-PLAN-2026-08-31.md,
Phase 1). Proves, per instrument, that the four named exclusions are real under the pre-fix code
and gone under the fix, by calling the composer's own exposed `castForKindsRanked` directly against
real WorkRecords of the 121-work fleet (`tests/fixture_pass_works.json`) — never a hand-typed score.

THE DEFECT, CITED. `pass-composer.js`'s tier ladder (`castForKindsRanked`, around :2436-2664) used
to roll the die only within the FIRST non-empty tier of 0..8 and list every tier behind it without
ever drawing from it — so a one-order demotion (an alpha-writing instrument barred from the ground
by `mustFill`, a frame-filling instrument barred from the arrival by `standsAbove`, a world-fold
instrument's `+1` under a no-miracle role) was a TOTAL exclusion whenever the tier ahead of it held
even one candidate, whatever either work's own reading said — the exact shape charter shelf 9
forbids ("a measurement ranks the genres of a crossing... it never decides whether a pair
qualifies"). The fix reads the whole ladder as one weighted pool, damping each candidate's own fit
by how many tiers it sits behind the best tier actually present for THIS pair, never to zero.

EACH ROW BELOW: a real pair and a real seed are found (by direct search over the shipped fixture,
not chosen to look good) where the named instrument's own reading is high enough to win under the
repaired ladder. The RED row plants the pre-fix code back in with a named string substitution and
proves the SAME pair, at the SAME seed, and at a WHOLE RANGE of other seeds around it, can never
produce that instrument — not bad luck, a wall. The GREEN row proves the repaired code lets it
through at that seed.

Run: python3 tests/test_pass_cast_tiers.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_works.json"

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
WORKS = FIX["works"]

TMP = Path(tempfile.mkdtemp(prefix="pass_cast_tiers_"))
DRIVER = TMP / "cast-tiers-driver.js"

DRIVER_TEMPLATE = r"""
"use strict";
const vm = require("vm");
const rawSource = %(source)s;
const consts = %(consts)s;
const works = %(works)s;
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
const out = [];
for (const seed of job.seeds) {
  try {
    const r = composer.castForKindsRanked(job.kinds, works[job.a], works[job.b], job.noMiracle,
                                          seed, "k", "pivot", null, job.standsAbove, job.mustFill,
                                          null, [0, 1], false);
    out.push(r[0].length ? r[0][0].id : null);
  } catch (e) {
    out.push({error: String(e && e.stack || e)});
  }
}
console.log(JSON.stringify(out));
"""


def cast_ids(a, b, kinds, must_fill, stands_above, seeds, plants=None):
    driver = DRIVER_TEMPLATE % {
        "source": json.dumps(RAW),
        "consts": json.dumps(FIX["consts"]),
        "works": json.dumps(WORKS),
        "job": json.dumps({"a": a, "b": b, "kinds": kinds, "mustFill": must_fill,
                           "standsAbove": stands_above, "noMiracle": True,
                           "seeds": list(seeds), "plants": plants or []}),
    }
    DRIVER.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(DRIVER)], capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1200:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


# THE PRE-FIX ORDER FORMULA (:2601-2604 before this phase), which shared one sentinel — order 8 —
# between a real technical exclusion (`taken`: an instrument already cast elsewhere this crossing,
# which cannot also stand here) and two preferences that are not technical exclusions at all (an
# alpha-writer's own coverage preference at the ground, a frame-filler's own preference at the
# arrival). Sharing the sentinel made the two preferences exactly as absolute as the real one.
PLANT_ORDER = [["""        var order = (taken.indexOf(iid) >= 0) ? 8
          : base
            + ((mustFill && !FILLS_THE_FRAME[iid]) ? 4 : 0)
            + ((standsAbove && FILLS_THE_FRAME[iid]) ? 4 : 0);""",
                """        var order = (taken.indexOf(iid) >= 0) ? 8
          : ((mustFill && !FILLS_THE_FRAME[iid]) ? 8
             : ((standsAbove && FILLS_THE_FRAME[iid]) ? base + 4 : base));"""]]

# THE PRE-FIX ROLL (:2609-2664 before this phase): only the FIRST non-empty tier of 0..8 was ever
# rolled; every tier behind it — including a tier a fold's own `+1` demotion landed a candidate in
# — was walked purely to be listed, never drawn.
PLANT_ROLL = [["""      var ranked = [], soft = [], k;
      for (i = 0; i < 8; i++) {
        if (!tiers[i].length) continue;
        rankUnread(tiers[i]).forEach(function (p) { soft.push({ id: p.id, fit: p.fit, order: i }); });
      }
      if (soft.length) {
        var bestOrderHere = soft.reduce(function (m, s) { return Math.min(m, s.order); }, 8);
        var weighted = soft.map(function (s) {
          return { id: s.id, fit: s.fit / (1 + (s.order - bestOrderHere)) };
        });
        var pick = dieWeighted(weighted, seed, key + "|" + list.join("+") + "|" + slot, 1);
        var head = null;
        for (k = 0; k < soft.length; k++) { if (soft[k].id === pick) { head = soft[k]; break; } }
        ranked.push(head);
        soft.filter(function (s) { return s.id !== pick; })
          .sort(function (x, y) {
            return x.order - y.order
              || (Number(y.fit) || 0) - (Number(x.fit) || 0)
              || (x.id < y.id ? -1 : (x.id > y.id ? 1 : 0));
          })
          .forEach(function (s) { ranked.push(s); });
      }
      // TIER 8 IS NEVER ROLLED, ONLY LISTED, exactly as every tier used to be behind the winner:
      // a candidate already playing another slot of this crossing is walked here purely so the
      // collision fallback (the comment over `avoid`, above) has something to fold into where the
      // collection publishes nothing else at all.
      if (tiers[8].length) {
        rankUnread(tiers[8]).slice().sort(function (x, y) {
          return (Number(y.fit) || 0) - (Number(x.fit) || 0)
            || (x.id < y.id ? -1 : (x.id > y.id ? 1 : 0));
        }).forEach(function (p) { ranked.push({ id: p.id, fit: p.fit, order: 8 }); });
      }""",
               """      var ranked = [];
      for (i = 0; i < tiers.length; i++) {
        if (!tiers[i].length) continue;
        var pool = rankUnread(tiers[i]);
        if (!ranked.length) {
          var pick = dieWeighted(pool, seed, key + "|" + list.join("+") + "|" + slot, 1);
          var pickedFit = 0;
          pool.forEach(function (p) { if (p.id === pick) pickedFit = p.fit; });
          ranked.push({ id: pick, fit: pickedFit, order: i });
          pool.filter(function (p) { return p.id !== pick; })
            .sort(function (x, y) {
              return (Number(y.fit) || 0) - (Number(x.fit) || 0)
                || (x.id < y.id ? -1 : (x.id > y.id ? 1 : 0));
            })
            .forEach(function (p) { ranked.push({ id: p.id, fit: p.fit, order: i }); });
        } else {
          pool.slice().sort(function (x, y) {
            return (Number(y.fit) || 0) - (Number(x.fit) || 0)
              || (x.id < y.id ? -1 : (x.id > y.id ? 1 : 0));
          }).forEach(function (p) { ranked.push({ id: p.id, fit: p.fit, order: i }); });
        }
      }"""]]

RED_SEED_RANGE = list(range(1, 121))

if not NODE:
    for _n in (
        "tilt · barred from the ground by mustFill (:2601-2604) — GREEN, a real pair now casts it",
        "tilt · red-on-bug — the pre-fix order formula never casts it, over 120 seeds",
        "overlay · barred from the ground by mustFill (:2601-2604) — GREEN, a real pair now casts it",
        "overlay · red-on-bug — the pre-fix order formula never casts it, over 120 seeds",
        "parquet · barred from the arrival by standsAbove (:2601-2604) — GREEN, a real pair now "
        "casts it",
        "parquet · red-on-bug — the pre-fix single-tier roll never casts it, over 120 seeds",
        "planet · demoted a whole tier as a world-fold under a no-miracle role (:2585, :2609-2664) "
        "— GREEN, a real pair now casts it",
        "planet · red-on-bug — the pre-fix single-tier roll never casts it, over 120 seeds",
        "adrift/region · item 4, falls out of the same mustFill repair — GREEN, a real pair now "
        "casts it",
    ):
        skip(_n, "node is not on this machine")
else:
    # ======================================================================================= TILT
    # Real pair, kinds=["strip"] (the ground's own cast, mustFill always true there — pass-inst-
    # tilt.js declares `cuts: ["strip"]`). tilt writes alpha (coverage.writes: true in its own
    # manifest), so `FILLS_THE_FRAME.tilt` is false and `mustFill` demotes it every time. weave and
    # wind are the only two `strip`-cutters that DO fill the frame, so under the pre-fix code they
    # are the whole of tier 0 and always non-empty — tilt could never be drawn regardless of fit.
    T_A, T_B, T_SEED = "17855281635628600", "17997183340574989", 12
    tilt_green = cast_ids(T_A, T_B, ["strip"], True, False, [T_SEED])
    check("tilt · barred from the ground by mustFill (:2601-2604) — GREEN, a real pair now casts it",
          tilt_green == ["tilt"],
          "castForKindsRanked(['strip'], %s, %s, mustFill=true, seed=%d) head = %s"
          % (T_A, T_B, T_SEED, json.dumps(tilt_green)))

    tilt_red = cast_ids(T_A, T_B, ["strip"], True, False, RED_SEED_RANGE, plants=PLANT_ORDER)
    if isinstance(tilt_red, dict) and tilt_red.get("missed"):
        skip("tilt · red-on-bug — the pre-fix order formula never casts it, over 120 seeds",
             "the plant's own anchor text is not in the shipped source")
    else:
        check("tilt · red-on-bug — the pre-fix order formula never casts it, over 120 seeds",
              "tilt" not in tilt_red,
              "same pair, seeds 1-120, pre-fix order formula: tilt appears %d time(s)"
              % tilt_red.count("tilt"))

    # ==================================================================================== OVERLAY
    # kinds=["band"] (overlay's own real cut, after cause A item 3 dropped its dead `field` claim).
    # overlay writes alpha too. waterline is the ONLY `band`-cutter that fills the frame, so it
    # alone is tier 0 under the pre-fix code and overlay can never be drawn.
    O_A, O_B, O_SEED = "17945678195417816", "18006107842248584", 14
    overlay_green = cast_ids(O_A, O_B, ["band"], True, False, [O_SEED])
    check("overlay · barred from the ground by mustFill (:2601-2604) — GREEN, a real pair now "
          "casts it",
          overlay_green == ["overlay"],
          "castForKindsRanked(['band'], %s, %s, mustFill=true, seed=%d) head = %s"
          % (O_A, O_B, O_SEED, json.dumps(overlay_green)))

    overlay_red = cast_ids(O_A, O_B, ["band"], True, False, RED_SEED_RANGE, plants=PLANT_ORDER)
    if isinstance(overlay_red, dict) and overlay_red.get("missed"):
        skip("overlay · red-on-bug — the pre-fix order formula never casts it, over 120 seeds",
             "the plant's own anchor text is not in the shipped source")
    else:
        check("overlay · red-on-bug — the pre-fix order formula never casts it, over 120 seeds",
              "overlay" not in overlay_red,
              "same pair, seeds 1-120, pre-fix order formula: overlay appears %d time(s)"
              % overlay_red.count("overlay"))

    # ==================================================================================== PARQUET
    # kinds=[] (the arrival's own cast: it never restricts by kind, so `cuts` is false for every
    # candidate and `standsAbove` — true whenever the ground or the travelling move already fills
    # the frame, which parquet's own ground call above shows is the overwhelming case — is the only
    # thing that differentiates them). parquet fills the frame (coverage.writes: false), so
    # `standsAbove` demotes it; the ten alpha-writing instruments (adrift, beat, gears, grid-colour,
    # matter, overlay, pour, strata-light, strata-scale, tilt) do not fill the frame, so none of
    # them is demoted and they are always tier 0 (well, tier 2 — `cuts` is false for everything
    # here) under the pre-fix code.
    #
    # THIS ROW PLANTS PLANT_ROLL, NOT PLANT_ORDER, AND THAT IS ITSELF A FINDING. The `standsAbove
    # && FILLS_THE_FRAME[iid] ? base + 4 : base` arithmetic is IDENTICAL before and after this
    # phase — only the `mustFill` branch changed shape (a flat 8 down to the same `+ 4`) — so
    # parquet's own exclusion from the arrival was never pinned to the old order-8 sentinel the way
    # tilt's and overlay's were: it was excluded purely because the pre-fix ROLL never drew from any
    # tier but the first non-empty one, tier 2, which nine of the ten alpha-writers always populate.
    # PLANT_ORDER alone would change nothing for this row; PLANT_ROLL is the whole of what parquet's
    # own repair rests on.
    P_A, P_B, P_SEED = "17843080526947498", "17961191066787693", 8
    parquet_green = cast_ids(P_A, P_B, [], False, True, [P_SEED])
    check("parquet · barred from the arrival by standsAbove (:2601-2604) — GREEN, a real pair now "
          "casts it",
          parquet_green == ["parquet"],
          "castForKindsRanked([], %s, %s, standsAbove=true, seed=%d) head = %s"
          % (P_A, P_B, P_SEED, json.dumps(parquet_green)))

    parquet_red = cast_ids(P_A, P_B, [], False, True, RED_SEED_RANGE, plants=PLANT_ROLL)
    if isinstance(parquet_red, dict) and parquet_red.get("missed"):
        skip("parquet · red-on-bug — the pre-fix single-tier roll never casts it, over 120 seeds",
             "the plant's own anchor text is not in the shipped source")
    else:
        check("parquet · red-on-bug — the pre-fix single-tier roll never casts it, over 120 seeds",
              "parquet" not in parquet_red,
              "same pair, seeds 1-120, pre-fix single-tier roll: parquet appears %d time(s)"
              % parquet_red.count("parquet"))

    # ===================================================================================== PLANET
    # kinds=["ring"], mustFill=false, standsAbove=false (a travelling-move-shaped cast, isolating
    # the fold demotion alone) and `noMiracle=true` (the common case: most roles carry no miracle
    # budget). planet declares WORLD, so `spendsTheMiracle` reads true for it and `base` picks up
    # the `+1` at :2585 — the same demotion this file's own comment calls "one tier behind every
    # non-folding ring rival". droste/grid-colour/hero/kaleidoscope/lens/studio/tunnel all cut ring
    # without folding, so they are always tier 0 and non-empty; under the pre-fix single-tier roll
    # planet (tier 1) could never be drawn regardless of fit.
    PL_A, PL_B, PL_SEED = "17843153263050281", "18324823441037344", 33
    planet_green = cast_ids(PL_A, PL_B, ["ring"], False, False, [PL_SEED])
    check("planet · demoted a whole tier as a world-fold under a no-miracle role (:2585, "
          ":2609-2664) — GREEN, a real pair now casts it",
          planet_green == ["planet"],
          "castForKindsRanked(['ring'], %s, %s, noMiracle=true, seed=%d) head = %s"
          % (PL_A, PL_B, PL_SEED, json.dumps(planet_green)))

    planet_red = cast_ids(PL_A, PL_B, ["ring"], False, False, RED_SEED_RANGE, plants=PLANT_ROLL)
    if isinstance(planet_red, dict) and planet_red.get("missed"):
        skip("planet · red-on-bug — the pre-fix single-tier roll never casts it, over 120 seeds",
             "the plant's own anchor text is not in the shipped source")
    else:
        check("planet · red-on-bug — the pre-fix single-tier roll never casts it, over 120 seeds",
              "planet" not in planet_red,
              "same pair, seeds 1-120, pre-fix single-tier roll: planet appears %d time(s)"
              % planet_red.count("planet"))

    # ============================================================================ ADRIFT / REGION
    # Item 4 — "give region-ground pairs a reachable tier 0". `adrift` is the ONLY `region`-cutter
    # (`pass-inst-adrift.js`'s own `cuts: ["region"]`) and it writes alpha, so `mustFill` demoted it
    # to the same sentinel as an already-taken instrument under the pre-fix code, and tier 0 for
    # "region" is otherwise always structurally empty (nothing else cuts it) — so a region ground
    # fell through to the fifteen non-cutting fillers by default, exactly as the plan's own Cause A
    # names it. This falls out of the SAME mustFill repair PLANT_ORDER above already proves red on;
    # this row confirms the fallout reaches region specifically, on real named-object readings of 1
    # for both works (`adrift`'s own fit function).
    R_A, R_B, R_SEED = "17859642835320709", "17876720615987671", 22
    region_green = cast_ids(R_A, R_B, ["region"], True, False, [R_SEED])
    check("adrift/region · item 4, falls out of the same mustFill repair — GREEN, a real pair now "
          "casts it",
          region_green == ["adrift"],
          "castForKindsRanked(['region'], %s, %s, mustFill=true, seed=%d) head = %s"
          % (R_A, R_B, R_SEED, json.dumps(region_green)))

print("Cause A — the casting tier ladder ranks instead of gating (Phase 1)")
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
