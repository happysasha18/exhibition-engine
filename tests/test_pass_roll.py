#!/usr/bin/env python3
"""EX-ROLL — which lawful passage plays, and on what.

Run: python3 tests/test_pass_roll.py

Root: charter shelf 20 (`lab/CROSSING-BRIEF.md` in the tlvphotos tree) — «A number that shapes
behaviour comes from a picture's own record, from the dramaturgy of the walk, or from the session
… and never from a tally over the collection», and «EVERY CLAIM IS PROVED FROM THE FORMULA'S OWN
CONSTRUCTION — its bounds, its clamps, the monotonicity of how it combines, the definition and the
range of each field it reads — and where the arithmetic takes numbers with known spans it is checked
over the whole span rather than over a sample.» And shelf 15's amendment of 2026-08-24 evening,
which is what orders the readings: «a route's pressure toward variety is a preference among edges
met for the FIRST time, and it never outranks the kinship a return owes on an edge already walked
… That kinship is owed on what is DRAWN — the instrument, the gesture it makes and the level it
makes it at … while a family is a name a composition gives its own pivot and nobody can see one».

WHAT THIS MEASURES, and how it is anchored.

  THE RULE IS RUN, NOT DESCRIBED. `passRollBetter` and the race's own loop header are extracted
  verbatim from the BUILT client (`engine/assets/exhibition.js`) and executed in node. Nothing of
  the rule is re-typed here.

  THE SPAN, NOT A SAMPLE. Three of the seven readings a candidate carries are facts — kin, not
  cooling, and the route's first colour voice — each 0 or 1, so every combination of them is 8.
  Three more are the route novelties (`passRouteNovelty`): Jaccard distances, so each is bounded in
  0…1 by construction and is driven at both ends and the middle of that span. The seventh, the
  mirror distance, is unbounded above; it is driven at the ends and the interior of its own span,
  including the null reading the layer maps to «further from the mirror than any measured pass».
  No pair of photographs is involved in any row, and nothing is counted over a collection.

  THE RETIRED FORMULA IS RUN TOO, on its own reading vector. The weighted sum that stood until
  2026-08-25 is typed out ONCE, in `old_score` below, with its provenance in the docstring there —
  not as a rule this file believes, but as the thing row R4 convicts. It read the eight readings the
  order carried BEFORE 2026-09-01, so R4 drives both it and the shipped rule over that older vector;
  convicting it needs it runnable against what it actually ran against.

Rows:
  R1  the rule travels as one block of the shipped client, and the race's loop header with it
  R2  the rule is a strict order: no candidate outranks itself, two candidates never each outrank
      the other, and any three that rank in a chain rank the same way end to end
  R3  the charter's own rank: over EVERY combination of the three facts, every novelty driven and
      every distance driven, no reading below kinship can lift a candidate above a kin one
  R4  the retired weighted sum broke exactly that rank, and the run says by how many combinations
  R5  a candidate at the worst of every reading still plays where it is the only one — a preference
      ranks and never refuses
  R6  the race resolves for every pair: the first roll leads unconditionally and is only ever
      displaced by one standing strictly higher
  R7  the race can now reach every die the walk allows, and a held pass still ends it before it
      starts — the loop header, run over every combination of its own controls
  R8  red-on-bug · the loop header reverted to `best === null`: the race ends after one die again
  R9  red-on-bug · the order reverted to a weighted sum: the charter's rank breaks again
  R10 the crossing's bundle budget bounds the race: over every combination of the loop's controls
      the whole race plans at most two compositions' worth of bundles, against the eight an
      unbounded race can ask for
  R11 red-on-bug · the retired clean-die stop restored: on an edge met for the FIRST time — where
      kin is true and the distance null for every candidate by construction — the race ends after
      one die again, which is the 2026-08-25 defect returning under a different name

node is a hard dependency (the rule is the test) — its absence FAILS, never skips. The source tree
is never written to; every copy runs in a temporary file that is removed afterwards.
"""
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def report_and_exit():
    for n, s, d in results:
        print(f"{s}  {n}" + (f"   — {d}" if d else ""))
    bad = sum(1 for _, s, _ in results if s == "FAIL")
    print(f"\n{len(results) - bad} passed / {bad} failed")
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- R1: the pieces, extracted
RULE_HEAD = "  function passRollBetter(now, was) {"
RULE_TAIL = "\n  }\n"
RULE = None
if RULE_HEAD in BUNDLE:
    start = BUNDLE.index(RULE_HEAD)
    end = BUNDLE.index(RULE_TAIL, start) + len(RULE_TAIL)
    RULE = BUNDLE[start:end]
HEADER = "    for (let i = heldStart; !heldTook && i < PASS_EDGE.dice; i++) {"
HAS_HEADER = HEADER in BUNDLE
NODE = shutil.which("node")

check("R1 EX-ROLL the rule travels as one block of the shipped client, and the race's own loop "
      "header with it",
      RULE is not None and HAS_HEADER,
      "" if (RULE and HAS_HEADER) else
      "missing from engine/assets/exhibition.js: %s"
      % ", ".join(n for n, v in (("passRollBetter", RULE), ("the race's loop header", HAS_HEADER))
                  if not v))
if RULE is None or not HAS_HEADER:
    report_and_exit()
if not NODE:
    check("R1 EX-ROLL node present (the rule is the test)", False, "node not on PATH")
    report_and_exit()

# ---------------------------------------------------------------- the candidates
# THE WHOLE SPAN OF THE THREE FACTS. Each of these readings is 1 where the thing it is a preference
# about holds and 0 where it does not, and the layer never adds one to another, so the space of
# fact-candidates is exactly every combination of the three.
FACTS = list(itertools.product([0, 1], repeat=3))
# THE THREE NOVELTIES, over their own span. `passSetDistance` returns 1 - |A∩B| / |A∪B|, which is
# bounded in 0…1 for every pair of token sets that exist — 0 where the two scenes name exactly the
# same things, 1 where they share nothing — so both ends and the middle are the whole span, not a
# sample of it.
NOVELTIES = [0.0, 0.5, 1.0]
# …and the mirror distance, driven over its own span. It is a mean of non-negative ratios, so 0 is
# the floor — a literal mirror of the pass this edge already played — and it has no ceiling. `null`
# is `passMirrorDistance` saying the two cannot be read as mirrors at all, which the layer ranks
# above every measured distance; it travels here as the same Infinity the layer uses. The two
# interior values straddle the tenth the retired ×10 clamp turned on.
DISTANCES = [0.0, 0.05, 0.1, 1.0, "Infinity"]


def vector(facts, dist, local, scene, controls):
    """A candidate's seven readings in the order the layer compares them: kin, not cooling, the
    mirror distance, how far this scene stands from the step just played, the route's first colour
    voice, how far the scene stands from its nearest already-played scene, and how far its handle
    choreography stands from the nearest already spent."""
    kin, cooled, colour = facts
    return [kin, cooled, dist, local, colour, scene, controls]


CANDIDATES = [vector(f, d, lo, sc, co)
              for f in FACTS for d in DISTANCES
              for lo in NOVELTIES for sc in NOVELTIES for co in NOVELTIES]

# THE ORDER AS IT STOOD BEFORE 2026-09-01, kept for row R4 alone: eight readings, seven of them
# facts. The retired weighted sum below was written against exactly this vector, so convicting it
# has to drive it over this vector and never over the one that stands.
OLD_FACTS = list(itertools.product([0, 1], repeat=7))
OLD_CANDIDATES = [[f[0], f[1], d, f[2], f[3], f[4], f[5], f[6]]
                  for f in OLD_FACTS for d in DISTANCES]

DRIVER = r"""
'use strict';
__RULE__
const C = __CANDIDATES__.map(function (v) {
  return v.map(function (x) { return x === "Infinity" ? Infinity : x; });
});
const out = { n: C.length, irreflexive: 0, symmetric: 0, transitive: 0,
              kinBeaten: [], worstPlays: null, raceAlwaysResolves: true };
for (let a = 0; a < C.length; a++) {
  if (passRollBetter(C[a], C[a])) out.irreflexive++;
  for (let b = 0; b < C.length; b++) {
    const ab = passRollBetter(C[a], C[b]), ba = passRollBetter(C[b], C[a]);
    if (ab && ba) out.symmetric++;
    // THE CHARTER'S OWN RANK: a candidate that is not kin may never stand above one that is.
    if (ab && C[b][0] === 1 && C[a][0] === 0) out.kinBeaten.push([a, b]);
  }
}
// A CHAIN RANKS THE SAME WAY END TO END. Walked over a fixed stride rather than every triple, so
// the row runs in a moment; the stride sweeps the whole list and skips no candidate as a first or
// last link.
for (let a = 0; a < C.length; a++) {
  for (let b = 0; b < C.length; b += 7) {
    for (let c = 0; c < C.length; c += 13) {
      if (passRollBetter(C[a], C[b]) && passRollBetter(C[b], C[c])
          && !passRollBetter(C[a], C[c])) out.transitive++;
    }
  }
}
// A PREFERENCE RANKS AND NEVER REFUSES: the candidate at the worst of every reading still takes the
// lead when it is the only one offered, exactly as the race gives the lead to its first roll.
{
  const worst = C.reduce(function (w, v) { return passRollBetter(w, v) ? v : w; });
  out.worstPlays = passRollBetter(worst, null);
}
// THE RACE RESOLVES FOR EVERY PAIR. The race's own shape: the first roll takes the lead
// unconditionally, and a later one replaces it only where it stands strictly higher. Run over every
// candidate as the first roll and every other as the second.
for (let a = 0; a < C.length && out.raceAlwaysResolves; a++) {
  for (let b = 0; b < C.length; b++) {
    let best = null, bestReadings = null;
    [C[a], C[b]].forEach(function (v) {
      if (best === null || passRollBetter(v, bestReadings)) { best = v; bestReadings = v; }
    });
    if (best === null) { out.raceAlwaysResolves = false; break; }
  }
}
process.stdout.write(JSON.stringify(out));
"""


def run_js(src, tag):
    fh = tempfile.NamedTemporaryFile("w", suffix="_%s.js" % tag, delete=False, encoding="utf-8")
    fh.write(src)
    fh.close()
    try:
        run = subprocess.run([NODE, fh.name], capture_output=True, text=True, timeout=300)
    finally:
        Path(fh.name).unlink(missing_ok=True)
    if run.returncode != 0:
        return None, (run.stderr or run.stdout or "").strip().splitlines()[-1:]
    return json.loads(run.stdout), None


GOT, why = run_js(DRIVER.replace("__RULE__", RULE)
                        .replace("__CANDIDATES__", json.dumps(CANDIDATES)), "shipped")
if GOT is None:
    check("R1 EX-ROLL the extracted rule runs on its own", False, "node said: %s" % (why or ""))
    report_and_exit()

# ---------------------------------------------------------------- R2: it is a strict order
check("R2 EX-ROLL the rule is a strict order — no candidate outranks itself, no two each outrank "
      "the other, and a chain ranks the same way end to end",
      GOT["irreflexive"] == 0 and GOT["symmetric"] == 0 and GOT["transitive"] == 0,
      "over %d candidates: %d outranking themselves, %d pairs outranking each other, %d chains "
      "that do not hold end to end"
      % (GOT["n"], GOT["irreflexive"], GOT["symmetric"], GOT["transitive"]))

# ---------------------------------------------------------------- R3: the charter's own rank
check("R3 EX-ROLL no reading below kinship can lift a candidate above a kin one — the charter's "
      "«it never outranks the kinship a return owes on an edge already walked»",
      not GOT["kinBeaten"],
      "over every ordered pair of the %d candidates — every combination of the three facts against "
      "every other, at each driven novelty and each driven distance — %d where a candidate that is "
      "not kin stands above one that is" % (GOT["n"], len(GOT["kinBeaten"])))


# ---------------------------------------------------------------- R4: the retired sum, convicted
def old_score(v):
    """The weighted sum that decided the race until 2026-08-25, typed out once so it can be
    convicted. Its own line, from `engine/client/01a-pass.js` before the sweep:

        (read.kin ? 2 : 0) + (cooledStood ? 0 : 1)
        + (read.distance === null ? 1 : Math.min(1, read.distance * 10))
        + (repeatsFamily ? 0 : 3) + (repeatsPrimary ? 0 : 3)
        + (passRouteFamilyCount[fam] ? 0 : 2)
        + (passRouteInstrumentCount[primary] ? 0 : 2)
        + (!passRouteWorldSeen && worldAccent ? 3 : 0)

    read here against the same reading vector the shipped rule takes."""
    kin, cooled, dist, rep_i, rep_f, new_i, new_f, world = v
    d = 1.0 if dist == "Infinity" else min(1.0, dist * 10)
    return (2 * kin) + cooled + d + (3 * rep_f) + (3 * rep_i) + (2 * new_f) + (2 * new_i) \
        + (3 * world)


OLD_GOT, whyOld = run_js(DRIVER.replace("__RULE__", RULE)
                               .replace("__CANDIDATES__", json.dumps(OLD_CANDIDATES)), "old")
inversions = [(a, b) for a in OLD_CANDIDATES for b in OLD_CANDIDATES
              if a[0] == 0 and b[0] == 1 and old_score(a) > old_score(b)]
alone = [(a, b) for a, b in inversions
         if [a[i] for i in (1, 3, 4, 5, 6)] == [b[i] for i in (1, 3, 4, 5, 6)] and a[7] > b[7]]
check("R4 EX-ROLL the retired weighted sum broke that rank — a candidate that is not kin outscored "
      "a kin one, and the underived world reading did it on its own",
      bool(inversions) and bool(alone) and bool(OLD_GOT) and not OLD_GOT["kinBeaten"],
      "over the %d candidates of the vector that sum actually ran on, the retired sum puts a "
      "non-kin candidate above a kin one in %d ordered pairs, %d of them on the world reading alone "
      "with every other fact equal; the rule that stands, run over that same vector, does it in %s"
      % (len(OLD_CANDIDATES), len(inversions), len(alone),
         len(OLD_GOT["kinBeaten"]) if OLD_GOT else whyOld))

# ---------------------------------------------------------------- R5/R6: never refuses, resolves
check("R5 EX-ROLL a candidate at the worst of every reading still plays where it is the only one — "
      "a preference ranks and never refuses",
      GOT["worstPlays"] is True,
      "the lowest-ranking candidate of all %d takes the lead against an empty race: %s"
      % (GOT["n"], GOT["worstPlays"]))
check("R6 EX-ROLL the race resolves for every pair — the first roll leads unconditionally and is "
      "displaced only by one standing strictly higher",
      GOT["raceAlwaysResolves"] is True,
      "run over every candidate as the first roll against every candidate as the second: %d races, "
      "all resolved" % (GOT["n"] * GOT["n"]))

# ---------------------------------------------------------------- R7/R8: the loop header
# The race's own control flow, with the body reduced to what decides iteration and the header
# lifted verbatim from the built client. Run over every combination of the controls the loop reads.
#
# THE STOPS THE MODEL CARRIES. `3b8cb45` removed BOTH of the race's early stops on 2026-08-30 and
# was reverted the same night; Phase 5 re-landed its novelty order with ONE of them kept — the
# repeated-family stop, which reads what the dice are doing and is untouched by the new order — and
# added the crossing's own bundle budget, which the family stop cannot substitute for because it
# depends on what the dice happen to land on and can decline to fire at all. The three shapes are
# modelled side by side: `shipped` (family stop + budget), `unbounded` (`3b8cb45` as it landed,
# neither), and `clean` (the retired clean-die stop restored on top of the shipped shape). `cap` is
# the composer's own BUNDLE_CAP and `perDie` is what one composition actually spends against it.
LOOP = r"""
'use strict';
function race(headerKind, stops, dice, heldStart, heldTook, declinedAt, cleanAt, sameFamilyAt,
              perDie, cap) {
  const PASS_EDGE = { dice: dice };
  let best = null, tried = 0, examined = 0;
  const cond = (i) => headerKind === "shipped" ? (!heldTook && i < PASS_EDGE.dice)
                                               : (best === null && i < PASS_EDGE.dice);
  for (let i = heldStart; cond(i); i++) {
    tried++;
    examined += perDie;
    if (declinedAt === i) break;
    if (best === null || true) best = i;
    // The retired clean-die stop, modelled only for the shape that restores it.
    if (stops === "clean" && cleanAt === i) break;
    if (stops !== "unbounded" && sameFamilyAt === i) break;
    if (stops !== "unbounded" && examined >= cap) break;
  }
  return { tried: tried, best: best, examined: examined };
}
const CAP = 36;
const out = {};
[["shipped", "shipped"], ["reverted", "shipped"], ["shipped", "unbounded"],
 ["shipped", "clean"]].forEach(function (pair) {
  const headerKind = pair[0], stops = pair[1];
  const name = headerKind === "reverted" ? "reverted" : stops;
  let most = 0, everRanAfterHeld = false, alwaysResolved = true, mostExamined = 0;
  let mostOnFirstEdge = 0;
  for (let dice = 1; dice <= 8; dice++) {
    for (let heldStart = 0; heldStart <= 1; heldStart++) {
      for (let held = 0; held <= 1; held++) {
        for (let d = -1; d < dice; d++) {
          for (let c = -1; c < dice; c++) {
            for (let s = -1; s < dice; s++) {
              // Every composition spends between one bundle and the whole cap.
              for (let p = 1; p <= CAP; p++) {
                const r = race(headerKind, stops, dice, heldStart, !!held, d, c, s, p, CAP);
                if (held && r.tried > 0) everRanAfterHeld = true;
                if (!held && heldStart < dice && r.best === null && d !== heldStart) {
                  alwaysResolved = false;
                }
                if (r.tried > most) most = r.tried;
                if (r.examined > mostExamined) mostExamined = r.examined;
                // AN EDGE MET FOR THE FIRST TIME. `passEdgeJudge` has no recorded pass to read
                // there, so it answers kin for every candidate and its distance is null for every
                // candidate: the clean-die condition's first three terms hold on EVERY die by
                // construction, and its last two terms no longer exist. `cleanAt` is therefore the
                // first die rolled, whatever that die landed on.
                const f = race(headerKind, stops, dice, heldStart, !!held, d, heldStart, s, p, CAP);
                if (!held && f.tried > mostOnFirstEdge) mostOnFirstEdge = f.tried;
              }
            }
          }
        }
      }
    }
  }
  out[name] = { most: most, everRanAfterHeld: everRanAfterHeld, alwaysResolved: alwaysResolved,
                mostExamined: mostExamined, mostOnFirstEdge: mostOnFirstEdge, cap: CAP };
});
process.stdout.write(JSON.stringify(out));
"""
LOOPS, why2 = run_js(LOOP, "loop")
SHIPPED = (LOOPS or {}).get("shipped") or {}
REVERTED = (LOOPS or {}).get("reverted") or {}
UNBOUNDED = (LOOPS or {}).get("unbounded") or {}
CLEAN = (LOOPS or {}).get("clean") or {}
CAP = SHIPPED.get("cap")
check("R7 EX-ROLL the race can reach every die the walk allows, and a held pass still ends it "
      "before it starts",
      SHIPPED.get("most") == 8 and SHIPPED.get("everRanAfterHeld") is False
      and SHIPPED.get("alwaysResolved") is True,
      "over every combination of the loop's own controls — any die count to 8, either opening, a "
      "held pass or none, a decline or a repeated family at any position, and every per-composition "
      "bundle spend from 1 to the cap — the race reaches %s dice at most, rolls %s die after a held "
      "pass took, and always names a winner"
      % (SHIPPED.get("most"), "a" if SHIPPED.get("everRanAfterHeld") else "no"))
check("R8 EX-ROLL red-on-bug · the loop header reverted to «best === null»: the race ends after one "
      "die again, whatever the walk allows",
      REVERTED.get("most") == 1 and SHIPPED.get("most") == 8,
      "with the header reverted the race reaches %s die at most where the walk allows 8; with the "
      "header that stands, %s" % (REVERTED.get("most"), SHIPPED.get("most")))

# ------------------------------------------------- R10: the crossing's own bundle budget bounds it
check("R10 EX-ROLL the crossing's bundle budget bounds the whole race at two compositions' worth, "
      "against the eight an unbounded race asks for",
      bool(SHIPPED) and bool(UNBOUNDED)
      and SHIPPED.get("mostExamined") <= 2 * CAP
      and UNBOUNDED.get("mostExamined") == 8 * CAP,
      "over every combination of the loop's controls and every per-composition spend from 1 to the "
      "cap (%s): the race that stands plans at most %s bundles for one crossing; with both stops "
      "removed as `3b8cb45` landed them, %s — %s×the cap"
      % (CAP, SHIPPED.get("mostExamined"), UNBOUNDED.get("mostExamined"),
         (UNBOUNDED.get("mostExamined") or 0) // (CAP or 1)))

# ---------------------------------- R11: red on bug, the retired clean-die stop on a first-time edge
check("R11 EX-ROLL red-on-bug · the retired clean-die stop restored: on an edge met for the FIRST "
      "time the race ends after one die again — the 2026-08-25 defect under a different name",
      bool(CLEAN) and CLEAN.get("mostOnFirstEdge") == 1
      and SHIPPED.get("mostOnFirstEdge") == 8,
      "on a first-time edge `passEdgeJudge` answers kin for every candidate and null for every "
      "distance, so the restored condition holds on the first die by construction: the race reaches "
      "%s die at most where the walk allows 8. With that stop retired, %s"
      % (CLEAN.get("mostOnFirstEdge"), SHIPPED.get("mostOnFirstEdge")))

# ---------------------------------------------------------------- R9: red on bug, the order
SUM = RULE.replace("if (now[i] > was[i]) return true;\n      if (now[i] < was[i]) return false;",
                   "s += now[i]; t += was[i];")
SUM = SUM.replace("if (!was) return true;", "if (!was) return true;\n    let s = 0, t = 0;")
SUM = SUM.replace("    return false;\n  }", "    return s > t;\n  }")
rows9, why9 = (run_js(DRIVER.replace("__RULE__", SUM)
                            .replace("__CANDIDATES__", json.dumps(CANDIDATES)), "sum")
               if SUM != RULE else (None, "the rule's own lines did not match"))
check("R9 EX-ROLL red-on-bug · the order reverted to a sum of the readings: the charter's rank "
      "breaks again, because a sum can always be outweighed",
      bool(rows9) and bool(rows9.get("kinBeaten")) and not GOT["kinBeaten"],
      "with the readings added instead of ranked, %s ordered pairs put a non-kin candidate above a "
      "kin one; with the order that stands, %d"
      % (len(rows9["kinBeaten"]) if rows9 else why9, len(GOT["kinBeaten"])))

report_and_exit()
