#!/usr/bin/env python3
"""EX-ROUTE — the walk's own dramaturgy: what a step of the route is FOR, and how it is read.
Run: python3 tests/test_pass_route.py

Root: charter shelf 15 (`SPEC.md` Requirement 27, in the tlvphotos tree) — the route's five names are
entrance, quiet link, middle, culmination and return, and they are the IMAGE of the shelf's three
harmonic functions: a tonic the eye settles in, a subdominant that moves away and prepares, and a
dominant whose tension demands resolution. Unit brief:
docs/immersive/briefs/2026-08-17-U27-composed-full-route.md, stage 2, and his 18:43 formulation of
the full route — 10 works, extendable twice by 5, every edge composed.

WHAT THIS MEASURES.

  The route is the walk itself. `SPREAD`, `UNFOLD` and `MAXU` are settings this shell already had —
  10, 5 and 2 — so the 10+5+5 route is the product's own shape and nothing was invented to carry it.

  The function of a step is READ, not typed. The hang is already ordered by kinship: `arcOrder`
  draws the near neighbours in and then widens its steps on purpose, so the distance the route
  crosses at each step is a number the walk has already measured. Every function below comes off
  that curve — the widest step is the crest and the route's one dominant culmination, the step that
  leads into it prepares it, a step standing above both its neighbours is a motion away, and
  everything else is a home the eye settles in.

  WHAT DECIDES, SINCE THE HARMONIC LAYER LANDED (2026-08-25). The step's FUNCTION decides, and the
  name follows from it: `passRoleOfFunction` is the one place any of the five is written, and every
  row here that names a step is reading the image of a function. The two facts about the VISIT no
  longer OUTRANK the curve as a second ordering laid over it — they are read as functions too. An
  edge this visit has already walked is the walk restating something it has already resolved, so it
  is a tonic, and the name that tonic goes by there is the return (the same edge §4.8's return
  reference crosses on). The visit's first crossing is where the key is first stated at this
  person's ear, so it is a tonic as well, and the name it goes by is the entrance. Both keep the
  precedence they have always had; what changed is that there is one ordering and not two that can
  disagree. The layer's own rows — the key, the modulation through a pivot, the cadences and the
  reprise — live in tests/test_pass_harmony.py; this file goes on judging what a step ASKS UNDER
  and what the composer reads back.

  The name reaches the composer. It is put on the passage request at one place, and the composer's
  own reading of the request echoes it, so what the walk authored is what the passage was bounded by.

WHAT EVERY ROW HERE IS ANCHORED TO. Three things, and no fourth.

  1. THE WALK'S OWN SETTINGS AND THE COMPOSER'S OWN FENCE. The route's length is read from the
     bundle's own `spread_size` / `unfold_step` / `max_unfolds` lines, and the five names from
     the composer's own `routeRoles`. Neither is typed twice here.

  2. THE RULE, RE-DERIVED AND COMPARED. The naming rows recompute shelf 15's grammar in Python from
     the gaps the walk publishes and compare it against the names the walk published beside them.
     A change to the curve moves both sides together, so these never re-base on a change of content;
     they redden only when the walk stops reading the grammar it says it reads.

  3. NOTHING — a measured reading, printed so a person can read the number. How one dealt hang
     divides among the five names is one of these: it is the outcome of the grammar over that hang,
     never a quota to compose toward, and the walk deals a different hang every visit.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug row below serves a COPY of the built bundle with
one rule put back the way it stood. The source tree is never written to; the copy lives in the
temporary bake this suite serves and is restored byte for byte afterwards.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"
CLIENT = ROOT / "engine" / "assets" / "exhibition.js"
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_route_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")
BUNDLE = (TMP / "exhibition.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- the route is the walk's own shape
# The three numbers are read out of the bundle's own knob lines rather than restated: a route of ten
# extendable twice by five is what this shell already builds, and the unit's own 10+5+5 is that.
KNOB = {name: re.search(r"const %s = clampInt\(EX\.(\w+), (\d+), " % name, BUNDLE)
        for name in ("SPREAD", "UNFOLD", "MAXU")}
check("EX-ROUTE the route is the walk's own 10+5+5 — the hang's spread, its unfold step and how "
      "many unfolds it allows, each read off the shell's own settings",
      all(KNOB.values())
      and KNOB["SPREAD"].group(2) == "10" and KNOB["SPREAD"].group(1) == "spread_size"
      and KNOB["UNFOLD"].group(2) == "5" and KNOB["UNFOLD"].group(1) == "unfold_step"
      and KNOB["MAXU"].group(2) == "2" and KNOB["MAXU"].group(1) == "max_unfolds"
      and "const CAP = SPREAD + MAXU * UNFOLD;" in BUNDLE,
      "spread=%s unfold=%s unfolds=%s, so the route runs to %s works and %s steps"
      % (KNOB["SPREAD"].group(2) if KNOB["SPREAD"] else "?",
         KNOB["UNFOLD"].group(2) if KNOB["UNFOLD"] else "?",
         KNOB["MAXU"].group(2) if KNOB["MAXU"] else "?",
         10 + 2 * 5, 10 + 2 * 5 - 1))

# ---------------------------------------------------------------- one home for the five names
COMPOSER_ROLES = re.search(r'var ROUTE_ROLES = \[([^\]]+)\]', COMPOSER.read_text(encoding="utf-8"))
FENCED = set(re.findall(r'"([^"]+)"', COMPOSER_ROLES.group(1))) if COMPOSER_ROLES else set()
ROUTE_BLOCK = SRC[SRC.index("let passRouteAt = null;"):SRC.index("// THE PASSAGE REQUEST")]
SAID = set(re.findall(r'"(entrance|quiet link|middle|culmination|return)"', ROUTE_BLOCK))
check("EX-ROUTE the five functions the walk can state are exactly the five the composer fences on",
      bool(FENCED) and SAID == FENCED,
      "the walk states %s; the composer accepts %s" % (sorted(SAID), sorted(FENCED)))

# ---------------------------------------------------------------- one place writes the role
# What this row fences is the DERIVATION and the WRITE, each of which stands once. Reading the role
# back off a request it is already on is the opposite of a second derivation — it is what keeps one
# home for the fact — so a reader is counted and named here rather than refused.
ROLE_WRITES = re.findall(r"routeRole\s*=(?!=)", SRC)
ROLE_READS = SRC.count("routeRole") - len(ROLE_WRITES)
check("EX-ROUTE the role is derived in one place and put on the request in one place",
      SRC.count("function passRouteRole(") == 1
      and SRC.count("req.routeRole = role") == 1
      and len(ROLE_WRITES) == 1,
      "passRouteRole is declared %d time(s) and the request is written %d time(s); the %d further "
      "mention(s) of the name read the role back off a request that already carries it"
      % (SRC.count("function passRouteRole("), len(ROLE_WRITES), ROLE_READS))

# ==================================================================================================
# THE WALK'S ONE IMPOSSIBLE EVENT IS HELD FOR THE STEP IT NAMES THE CULMINATION
# ==================================================================================================
#
# THE DEFECT, MEASURED. With the composer repaired (729bd13 — a role whose tier shelf 17 floors with
# a miracle is PLANNED for), a step named a culmination still reached one on 7 of 40 simulated
# routes, and 20 of the 40 were refused with the composer's own new sentence: «the walk had already
# spent its one impossible event on an earlier crossing». The two laws collided. A walk spends ONE
# impossible event and the first fold anywhere on it is that event (naряд S-18); a culmination FLOORS
# at exactly one; and `ROLE_BUDGETS.middle.miracle` is true, so any of the several middles a route
# puts before its crest could spend the walk's only one on the way there.
#
# WHAT IS AUTHORED IS THE DIRECTOR'S OWN INTENT, and it is soft: while the route still holds an
# uncrossed crest, a middle before it is sent a walk log saying the event is not its to spend, so a
# fold it casts plays as an ordinary letter — which is exactly what a fold after the crest already
# does. The crest itself, and every step after it, are sent the walk's own true log. Where the crest's
# own pair is refused by the composer's gate, the hold ends with that crossing rather than with the
# tier it managed, so the steps after it are free.
#
# HOW THIS IS MEASURED, AND WHY BOTH ARMS RUN IN ONE PROCESS. 40 routes of ten works are walked
# through the composer's own `passageFor` — real WorkRecords out of `tests/fixture_pass_works.json`,
# nine crossings each, at the nine names the walk's own grammar reads off a ten-work hang (the
# grammar itself is what the browser rows above judge; these rows judge what the walk does with the
# one slot once the names are read). `walkMemory`, `walkGenres` and `walkMiracles` are threaded
# forward exactly as `01a-pass.js` builds them at the dock. The two arms differ in ONE thing: the
# BEFORE arm sends the walk's own spent list as this file sent it before today, and the AFTER arm
# sends it through the shipped policy — `passMiraclesToSend` and `passCrestAhead` lifted out of
# `engine/client/01a-pass.js` as text and run, never retyped here, so a policy deleted or renamed
# reddens these rows rather than quietly leaving them measuring a copy.
MIRACLE_ROWS = [
    "EX-ROUTE the walk holds its one impossible event for the step it names the culmination — the "
    "crest reaches one far more often, and hardly any walk spends it before getting there",
    "EX-ROUTE no route that reached its crest lawfully loses it, and every crest that still falls "
    "short says which gate refused it",
    "EX-ROUTE the hold ends at the crest and never outlives it, and the walk spends no more "
    "impossible events than it did",
    "EX-ROUTE the hold is authored in one place, the request is built through it, and the step's "
    "own record says when it stood",
]

FIXTURE_WORKS = Path(__file__).resolve().parent / "fixture_pass_works.json"
NODE = shutil.which("node")
# The nine names a ten-work hang reads, in the order shelf 15's own grammar puts them: the visit's
# opening, the homes the eye settles in, the motions away, the crest, and the way back.
ROUTE_ROLES = ["entrance", "quiet link", "middle", "middle", "culmination",
               "middle", "quiet link", "middle", "return"]


def lift(name):
    """The shipped policy's own text, taken out of `01a-pass.js` whole. The functions stand at one
    indent inside the module closure, so the body runs to the first line that closes at that indent;
    a name this cannot find is a red below and never a silently skipped reading."""
    m = re.search(r"\n  function %s\(.*?\n  \}\n" % re.escape(name), SRC, re.S)
    return m.group(0) if m else None


MIRACLE_HELD_LINE = re.search(r'\n  const PASS_MIRACLE_HELD = "[^"]*";\n', SRC)
POLICY_PARTS = {name: lift(name) for name in ("passCrestAhead", "passMiraclesToSend")}

MIRACLE_DRIVER = r"""
"use strict";
const vm = require("vm");
const job = %(job)s;

let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(%(source)s, sandbox, {filename: "pass-composer.js"});
const composer = joined.make(%(consts)s);
const works = %(works)s;

// THE DIRECTOR'S OWN POLICY, run as the text it ships as. Nothing here re-states it.
const policy = new Function(job.policy + "\nreturn {held: PASS_MIRACLE_HELD, "
  + "crestAhead: passCrestAhead, toSend: passMiraclesToSend};")();

// A DIE PER CROSSING, ON THE EDGE'S OWN NAME, inside the composer's own published seed span — the
// same shape `passSeedFor` strikes, without the visit seed a simulation has no visit to read.
const SPAN = composer.seedSpan;
function seedOf(text) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 16777619); }
  return SPAN[0] + ((h >>> 0) / 4294967296) * (SPAN[1] - SPAN[0]);
}

// ONE WALK. `played` is the walk's own route record as `passEdgeRemember` files it — one row per
// crossing that landed, carrying the edge's key, the road it ran on, the instruments its stack
// carried and the fold, if any, its score voiced the miracle on. The three lists the request carries
// are read back off it exactly as `passWalkMemory` / `passWalkGenres` / `passWalkMiracles` read it.
function walk(ids, holding) {
  const shape = {ids: ids, crest: job.roles.indexOf("culmination")};
  const played = [], steps = [];
  for (let i = 0; i < job.roles.length; i++) {
    const from = String(ids[i]), to = String(ids[i + 1]);
    const forward = from <= to;
    const edgeKey = forward ? from + "__" + to : to + "__" + from;
    const memory = [], genres = [], spent = [];
    for (let j = played.length - 1; j >= 0; j--) {
      if (played[j].genre) { memory.push(played[j].genre); genres.push(played[j].genre); }
      played[j].stack.forEach((id) => { if (id) memory.push(id); });
      if (played[j].miracle) spent.push(played[j].miracle);
    }
    const sent = holding
      ? policy.toSend(spent, policy.crestAhead(shape, played), job.roles[i])
      : spent;
    const got = composer.passageFor({
      workRecordA: works[forward ? from : to], workRecordB: works[forward ? to : from],
      direction: forward ? "a-to-b" : "b-to-a", seed: seedOf(edgeKey),
      routeRole: job.roles[i], walkMemory: memory, walkGenres: genres, walkMiracles: sent});
    const cues = (got && got.plan && got.plan.cues) || [];
    const miracleCue = cues.filter((c) => c.voice === "miracle")[0] || null;
    const miracle = (miracleCue && miracleCue.instrument && miracleCue.instrument.id) || null;
    steps.push({role: job.roles[i], realisedTier: got ? (got.realisedTier || null) : null,
                why: got ? (got.downgradeReason || null) : null, miracle: miracle,
                held: sent.indexOf(policy.held) >= 0,
                declined: got ? (got.declined || null) : "the entry answered nothing"});
    played.push({edgeKey: edgeKey, genre: (got && got.plan && got.plan.genre) || null,
                 stack: cues.map((c) => c.instrument && c.instrument.id),
                 miracle: miracle});
  }
  return steps;
}

const out = [];
for (const ids of job.routes) out.push({before: walk(ids, false), after: walk(ids, true)});
console.log(JSON.stringify(out));
"""


def miracle_run():
    fix = json.loads(FIXTURE_WORKS.read_text(encoding="utf-8"))
    ids = sorted(fix["works"])
    # 40 ROUTES, DEALT OFF THE FIXTURE ITSELF rather than chosen: each starts three works further on
    # and steps by seven, which is coprime with the fixture's own count, so every route is ten
    # distinct works and the forty between them cross the whole collection rather than one corner.
    routes = [[ids[(r * 3 + i * 7) % len(ids)] for i in range(len(ROUTE_ROLES) + 1)]
              for r in range(40)]
    driver = TMP / "route-miracle.js"
    driver.write_text(MIRACLE_DRIVER % {
        # The namespace token the build fills in, emptied here exactly as the composer's own suite
        # empties it (`tests/test_pass_bundle.py`) — the file ships as a template.
        "source": json.dumps(COMPOSER.read_text(encoding="utf-8").replace("@@NS@@", "")),
        "consts": json.dumps(fix["consts"]),
        "works": json.dumps(fix["works"]),
        "job": json.dumps({"routes": routes, "roles": ROUTE_ROLES,
                           "policy": MIRACLE_HELD_LINE.group(0) + POLICY_PARTS["passCrestAhead"]
                                     + POLICY_PARTS["passMiraclesToSend"]}),
    }, encoding="utf-8")
    proc = subprocess.run([NODE, str(driver)], capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1200:]}
    lines = (proc.stdout or "").strip().splitlines()
    return json.loads(lines[-1]) if lines else {"error": "the route driver said nothing"}


CREST_AT = ROUTE_ROLES.index("culmination")
SPENT_SAYS = "already spent its one impossible event"


def tally(arm):
    """Every route whose crest fell short, counted by the gate that refused it — the composer's own
    sentence, cut at its first clause so four reasons do not read as forty."""
    out = {}
    for steps in arm:
        step = steps[CREST_AT]
        if step["realisedTier"] == "culmination":
            continue
        why = step["why"] or step["declined"] or "nothing said"
        key = ("the walk had already spent its one impossible event" if SPENT_SAYS in why
               else "no arrival voice at all" if "no arrival voice" in why
               else "every bundle that would have made one was refused" if "every bundle" in why
               else "no instrument in the ranking opens a world" if "opens a world" in why
               else why[:70])
        out[key] = out.get(key, 0) + 1
    return out


if not NODE or not FIXTURE_WORKS.exists() or not MIRACLE_HELD_LINE \
        or not all(POLICY_PARTS.values()):
    _missing = [n for n, t in POLICY_PARTS.items() if not t] + \
               ([] if MIRACLE_HELD_LINE else ["PASS_MIRACLE_HELD"])
    if _missing:
        # NOT A SKIP. The policy is the subject of these rows; a tree that does not carry it is a
        # tree where the walk spends its one impossible event before it reaches its crest.
        for _n in MIRACLE_ROWS[:3]:
            check(_n, False, "engine/client/01a-pass.js carries no %s, so the walk holds nothing "
                             "back for the step it names its culmination" % ", ".join(_missing))
    else:
        for _n in MIRACLE_ROWS[:3]:
            skip(_n, "node is not on this machine" if not NODE
                 else "tests/fixture_pass_works.json is not on this machine")
else:
    _run = miracle_run()
    if not isinstance(_run, list):
        for _n in MIRACLE_ROWS[:3]:
            check(_n, False, "the route driver itself failed: " + json.dumps(_run)[:800])
    else:
        _before = [r["before"] for r in _run]
        _after = [r["after"] for r in _run]
        _reached_b = {i for i, s in enumerate(_before) if s[CREST_AT]["realisedTier"] == "culmination"}
        _reached_a = {i for i, s in enumerate(_after) if s[CREST_AT]["realisedTier"] == "culmination"}
        _tally_b, _tally_a = tally(_before), tally(_after)
        _spent_b = sum(v for k, v in _tally_b.items() if "already spent" in k)
        _spent_a = sum(v for k, v in _tally_a.items() if "already spent" in k)
        _early_b = sum(1 for s in _before if any(x["miracle"] for x in s[:CREST_AT]))
        _early_a = sum(1 for s in _after if any(x["miracle"] for x in s[:CREST_AT]))
        # THE RESIDUE, NAMED RATHER THAN ROUNDED OFF. A step the hold was in force on that spent the
        # event anyway spent it by a road `spendsTheMiracle` does not read: `mayFold` opens the
        # ARRIVING WORK'S OWN WORLD off the role's budget alone, and a world voices the miracle on
        # the travelling move exactly as a fold does. The walk has no lever on that road — it is the
        # composer's, beside `spendsTheMiracle` — so it is measured here and left where it lives.
        _leaked = [(i, j) for i, s in enumerate(_after) for j, x in enumerate(s)
                   if x["held"] and x["miracle"]]
        # ---- ROW 1: the crest reaches its tier far more often, and hardly anything is spent before
        check(MIRACLE_ROWS[0],
              len(_reached_a) > len(_reached_b) and _early_a < _early_b and _spent_a < _spent_b,
              "%d of %d routes reached a culmination at the step named one before, %d after; %d "
              "walks spent the event before reaching their crest before, %d after. Crests refused "
              "before: %s. After: %s. The %d step(s) that spent it under the hold spent it on the "
              "arriving work's own world (%s), which is the composer's own road and not the walk's."
              % (len(_reached_b), len(_run), len(_reached_a), _early_b, _early_a,
                 json.dumps(_tally_b, sort_keys=True), json.dumps(_tally_a, sort_keys=True),
                 len(_leaked), _leaked))
        # ---- ROW 2: nothing lawful is taken from a route that already had its crest --------------
        # A CREST REACHED ON A WALK THAT SPENT TWO IMPOSSIBLE EVENTS was never lawfully reached:
        # shelf 6 gives a walk one. Those are read out of the before arm rather than counted as
        # losses — the composer's `mayFold` road hands a second event to a walk that has already
        # spent one, and a crest bought with it is a crest bought against the charter.
        _twice_b = {i for i, s in enumerate(_before) if sum(1 for x in s if x["miracle"]) > 1}
        _lost = sorted((_reached_b - _twice_b) - _reached_a)
        _traded = sorted((_reached_b & _twice_b) - _reached_a)
        _silent = [i for i, s in enumerate(_after)
                   if s[CREST_AT]["realisedTier"] != "culmination"
                   and not (s[CREST_AT]["why"] or s[CREST_AT]["declined"])]
        check(MIRACLE_ROWS[1],
              not _lost and not _silent,
              "%d route(s) lost a crest reached on a walk that spent one event%s; %d route(s) lost "
              "a crest that had been bought with a SECOND event on the same walk (routes %s); %d "
              "crest(s) fell short with nothing said"
              % (len(_lost), "" if not _lost else " (routes " + str(_lost) + ")",
                 len(_traded), _traded, len(_silent)))
        # ---- ROW 3: the hold ends at the crest, and the one-event law is not loosened ------------
        # WHY THIS IS THE GUARANTEE A WALK GETS. The hold never survives the crest, so a walk that
        # ends with no impossible event at all is one whose own pairs offered none from the crest
        # onward — never one the walk's intent went on forbidding. That is what the first clause
        # measures, and it is why no floor under the event count is asserted: a floor would be a
        # number chosen here rather than read.
        _late_hold = [(i, j) for i, s in enumerate(_after)
                      for j in range(CREST_AT, len(ROUTE_ROLES)) if s[j]["held"]]
        _twice_a = {i for i, s in enumerate(_after) if sum(1 for x in s if x["miracle"]) > 1}
        _wow_b = sum(1 for s in _before if any(x["miracle"] for x in s))
        _wow_a = sum(1 for s in _after if any(x["miracle"] for x in s))
        _late_b = sum(1 for s in _before for j in range(CREST_AT + 1, len(ROUTE_ROLES))
                      if s[j]["miracle"])
        _late_a = sum(1 for s in _after for j in range(CREST_AT + 1, len(ROUTE_ROLES))
                      if s[j]["miracle"])
        check(MIRACLE_ROWS[2],
              not _late_hold and len(_twice_a) <= len(_twice_b),
              "%d step(s) at or after the crest were held; %d route(s) spent two events on one walk "
              "before, %d after; %d of %d walks played an impossible event at all before, %d after; "
              "the middles AFTER the crest played %d before and %d after"
              % (len(_late_hold), len(_twice_b), len(_twice_a), _wow_b, len(_run), _wow_a,
                 _late_b, _late_a))

# ---- ROW 4: one home for the policy, one write of the list, one field on the record --------------
check(MIRACLE_ROWS[3],
      SRC.count("function passMiraclesToSend(") == 1
      and SRC.count("passMiraclesToSend(") == 2
      and SRC.count("req.walkMiracles = ") == 1
      and "req.walkMiracles = passMiraclesToSend(" in SRC
      and SRC.count("function passCrestAhead(") == 1
      and SRC.count("passage.miracleHeldForCrest = passMiracleHeldSaid(request.walkMiracles)") == 1,
      "passMiraclesToSend is declared %d time(s) and called %d time(s); the walk's miracle list is "
      "written onto the request %d time(s); the step's own record is written %d time(s)"
      % (SRC.count("function passMiraclesToSend("), SRC.count("passMiraclesToSend(") - 1,
         SRC.count("req.walkMiracles = "),
         SRC.count("passage.miracleHeldForCrest = passMiracleHeldSaid(request.walkMiracles)")))

# ---------------------------------------------------------------- the browser rows
BROWSER_ROWS = [
    "EX-ROUTE every step of the hung route carries a function, read off the walk's own kinship gaps "
    "by shelf 15's grammar",
    "EX-ROUTE the route's realised dynamics: one crest, and the home the eye settles in carries the "
    "largest share",
    "EX-ROUTE the walk's authored role reaches the composer, and the composer's own reading of the "
    "request echoes it",
    "EX-ROUTE a route's steps do not all read alike — the functions of one hang are several",
    "EX-ROUTE the visit's FIRST crossing is an entrance, and the crossing after it is not",
    "EX-ROUTE an edge this visit has already walked asks as a RETURN, and the return reference of "
    "§4.8 crosses on that same step",
    "EX-ROUTE a step between two works that do not stand next to each other states no function, and "
    "the composer's own default stands",
    "EX-ROUTE «ещё 5» lengthens the route and the functions are re-read on the longer curve",
    "EX-ROUTE red-on-bug · the crest rule reverted: the route carries no culmination at all",
    "EX-ROUTE red-on-bug · the local-widening rule reverted: every motion away collapses",
    "EX-ROUTE red-on-bug · the return rule reverted: a walked-back edge stops asking as a return",
    "EX-ROUTE red-on-bug · the entrance rule reverted: the visit's first crossing is not an entrance",
]


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


# EX-PASS-RECORDS (2026-08-19): `pass.works` left config.json — the site now carries `pass.records`
# (a route + a cap) and the id → record map is answered over that route instead, the way a Cloudflare
# Worker answers it in production (engine/assets/worker.js's `passRecordsRoute`). This suite serves
# the same contract locally through the harness's `answer` hook (tests/headless_harness.py's `serve`,
# threaded through by tests/headless.py) — RECORDS_STORE is filled by `put_records` below and read by
# `records_answer`, a MUTABLE dict shared by both so a hook bound into `serve(...)` before any id is
# known still sees records `put_records` writes afterward.
RECORDS_ROUTE = "/api/pass/records"
RECORDS_CAP = 20   # spread_size 10 + max_unfolds 2 × unfold_step 5 — the built-in defaults (build.py)
RECORDS_STORE = {}


def records_answer(raw_path):
    """The harness's `answer` hook for this suite: answers `GET /api/pass/records?ids=...` the way
    the Worker does — over-cap or empty is refused with 400, an id `RECORDS_STORE` does not carry is
    simply left out of the answer."""
    if not raw_path.startswith(RECORDS_ROUTE):
        return None
    ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
    if not ids or len(ids) > RECORDS_CAP:
        return (400, "text/plain", "bad request")
    out = {i: RECORDS_STORE[i] for i in ids if i in RECORDS_STORE}
    return (200, "application/json", json.dumps({"records": out}))


def put_records(base_dir, ids):
    """The settings record as the site writes it for the composed road. The fixture's two records
    are re-keyed onto the works this bake hangs — what the composer reads is measurement, and the id
    is only its name."""
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    fix = json.loads(FIXTURE.read_text(encoding="utf-8"))
    src = [fix["works"][fix["pair"]["a"]], fix["works"][fix["pair"]["b"]]]
    works = {}
    for i, wid in enumerate(ids):
        rec = json.loads(json.dumps(src[i % 2]))
        rec["id"] = wid
        works[wid] = rec
    RECORDS_STORE.update(works)
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fix["consts"],
                       records={"route": RECORDS_ROUTE, "cap": RECORDS_CAP})
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return works


# The picture layer of this suite. A record is written only for a passage that actually DREW, and
# what says one drew is the host's own report; a stub host stands in for the renderer so the route's
# returns are measured on every machine and not only on one with a working WebGL2 context.
STUB = """
  if (!window.__exPassLayer) return {no: true};
  window.__exPassLayer({
    offer: function () { return true; },
    report: function () { return {active: false, instrument: 'stub',
                                  census: {buffer: '800x600', dpr: 1},
                                  stack: [{id: 'pivot', instrument: 'stub', handles: {}}]}; },
    cancel: function () {}, resize: function () {}
  });
  return {no: false};
"""

DECLARE = """
  var A = document.querySelector('.exh-frame[data-id="%s"]');
  var B = document.querySelector('.exh-frame[data-id="%s"]');
  if (!A || !B) return {absent: true};
  var req = window.__exPass.request(A, B);
  var cmd = window.__exPass.adapter.declare({fromEl: A, toEl: B, dir: %s, span: 100,
                                             kind: 'step', cause: 'route', velocity: 0});
  window.__cmd = cmd;
  var rows = window.__exPass.report().composer.passages;
  var row = rows.length ? rows[rows.length - 1] : null;
  var no = window.__exPass.report().refusals.filter(function (x) { return x.what === 'declare'; });
  return {absent: false, got: !!cmd, hasScore: !!(cmd && cmd.score),
          asked: req ? (req.routeRole === undefined ? null : req.routeRole) : null,
          crossed: req ? (req.sessionMemory || null) : null,
          read: row && row.request ? row.request.routeRole : null,
          key: row ? row.key : null, declined: row ? row.declined : null,
          noWhy: no.length ? no[no.length - 1].why : null};
"""

LAND = """
  var cmd = window.__cmd;
  if (!cmd) return {no: true};
  window.__exPass.adapter.dock(cmd);
  var r = window.__exPass.report();
  return {no: false, edges: r.memory.edges.length, opened: r.route.opened};
"""


def declare(br, a, b, direction=1):
    """One step declared programmatically. Two declares inside one animation frame are refused by
    law (§1.1), and a headless browser can hold a frame open far longer than a person's hand does,
    so a refusal for that one reason is waited out rather than read as an answer."""
    got = {}
    for _ in range(10):
        got = js(br, DECLARE % (a, b, direction))
        if got.get("absent") or got.get("got") or "one frame" not in (got.get("noWhy") or ""):
            return got
        br.sleep(0.3)
    return got


def enter(br, base, pass_arg="diagnostics:on,familySeed:4242", clear=True):
    br.navigate(base + "/")
    if clear:
        br.clear_storage()
    br.navigate(base + "/" + ("?pass=" + pass_arg if pass_arg else ""))
    br.sleep(0.8)
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        try:
            br.click(".exd-window", settle=1.4)
        except RuntimeError:
            br.sleep(1.0)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    # The engine's own file arrives at the walk's LANDING (§4.4d), with no crossing needed. The
    # PICTURE layer's door opens elsewhere — at the first real step — so one real step is taken
    # here, and it is the visit's own first crossing. That crossing is what the entrance row reads,
    # off the passage record the walk keeps, rather than a declare made afterwards: a declare made
    # afterwards would be the SECOND crossing and would read the curve instead of the opening.
    # AND THE RECORDS THE STEP WILL NEED (2026-08-19). Since they arrive with the selection rather
    # than inside the settings block, «the composer has landed» no longer means «a crossing can be
    # composed»: the wave is a request of its own and can still be in flight. A step taken before it
    # lands plays the walk's own glide and composes nothing, which for this suite would silently move
    # the visit's opening onto the NEXT step.
    #
    # THE TWO FACTS ARE WAITED ON TOGETHER, NOT ONE NESTED INSIDE THE OTHER (2026-08-19, same-day
    # fix). The composer's own script and the first record wave are two independent async arrivals
    # with no order between them — nothing in the client ever makes one wait on the other. The first
    # shape of this wait nested the records check inside the composer-state check, so a composer
    # slow to arrive (this suite's own Chrome under load, a cold fetch) let the OUTER loop exhaust
    # its budget and fall through in silence: ArrowDown then fired with `passComposer` still null,
    # `passComposeFor` refused before ever building a request, and the visit's real first crossing
    # composed nothing — the entrance role this file's rows read off `composer.passages[0]` was
    # never written, and every row downstream that assumed it was read a later crossing as if it
    # were the first. Reading both facts on every tick, until both hold, closes that gap: a slow
    # composer is waited out rather than raced past. The budget (150 ticks, 30s) is generous against
    # this suite's own launch of a fresh Chrome for every row: a script fetch racing page-load work
    # under a loaded machine is exactly the case this wait exists for.
    for _ in range(150):
        got = js(br, "var r = window.__exPass.report();"
                     "return {st: r.composer.state, held: r.records.held};")
        if got.get("st") == "read" and (got.get("held") or 0) > 1:
            break
        br.sleep(0.2)
    br.key("ArrowDown")
    for _ in range(30):
        if br.evaluate("String(!!window.__exPassLayer)") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.6)
    js(br, STUB)


def grammar(gaps):
    """Shelf 15's grammar, re-derived here from the gaps the walk publishes. The row compares this
    against the roles the walk published beside them, so both sides move together when the hang
    moves and the row goes on measuring the same claim."""
    # The search for the widest step begins AFTER the route's first, which shelf 15 gives to the
    # entrance; a one-step route keeps its only step.
    crest = max(range(1 if len(gaps) > 1 else 0, len(gaps)), key=lambda i: (gaps[i], -i))
    out = []
    for i, g in enumerate(gaps):
        if i == crest:
            out.append("culmination")
        elif i == crest - 1:
            out.append("middle")
        else:
            before = gaps[i - 1] if i > 0 else float("-inf")
            after = gaps[i + 1] if i + 1 < len(gaps) else float("-inf")
            out.append("middle" if (g > before and g > after) else "quiet link")
    return out


# The plants: one rule of the derivation put back the way it stood, in a COPY of the bundle the
# browser is served. Each names the line it reverts and what that line was for.
# EACH PLANT NOW REVERTS THE RULE WHERE THE HARMONIC LAYER PUT IT (2026-08-25). The four lines these
# anchored on before the layer landed wrote the five names straight off the curve; two of them WERE
# the second ordering the layer removed and cannot come back. Each plant below reverts the same rule
# at its new home, and each leaves the same floor behind it always did.
PLANTS = {
    # the crest's own name, taken away where the function is mapped to a name: every dominant then
    # reads as a middle and the route carries no culmination at all.
    "crest": ('if (fn === "dominant") return standingAs === "crest" ? "culmination" : "middle";',
              'if (fn === "dominant") return "middle";'),
    # the local-widening rule, taken away where the function is read: every step that is neither the
    # crest nor its own preparation collapses to a tonic, so every motion away is lost.
    "widening": ('if (!(g > before && g > after)) return "tonic";',
                 'return "tonic";'),
    # a walked-back edge is still heard as a tonic, but reverted to the name a tonic goes by on the
    # route itself, so it stops asking as a return.
    "return": ('return { at: at, fn: "tonic", role: passRoleOfFunction("tonic", "restated") };',
               'return { at: at, fn: "tonic", role: passRoleOfFunction("tonic", "route") };'),
    # and the same for the visit's opening, so it stops asking as an entrance.
    "entrance": ('return { at: at, fn: "tonic", role: passRoleOfFunction("tonic", "founding") };',
                 'return { at: at, fn: "tonic", role: passRoleOfFunction("tonic", "route") };'),
}
SERVED = TMP / "exhibition.js"
ORIGINAL = SERVED.read_text(encoding="utf-8")


def plant(name):
    was, now = PLANTS[name]
    if ORIGINAL.count(was) != 1:
        return False
    SERVED.write_text(ORIGINAL.replace(was, now), encoding="utf-8")
    return True


def unplant():
    SERVED.write_text(ORIGINAL, encoding="utf-8")


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP, answer=records_answer) as base:
        with Browser(width=1280, height=900) as br:
            # EVERY WORK OF THE CATALOGUE IS GIVEN A RECORD, not only the ten this entry hung: the
            # walk deals its works afresh on every entry, so a record set built from one hang would
            # leave the next hang's works unrecorded and every request would answer nothing.
            everyone = [w["id"] for w in json.loads(
                (TMP / "exhibition_data.json").read_text(encoding="utf-8"))["works"]]
            put_records(TMP, everyone)
            enter(br, base)

            shape = js(br, "return window.__exPass.report().route;")
            ids = shape.get("ids") or []

            # 0 · the curve names every step
            want = grammar(shape["gaps"]) if shape.get("gaps") else []
            check(BROWSER_ROWS[0],
                  bool(want) and want == shape["roles"] and len(shape["roles"]) == len(ids) - 1,
                  "%d works, %d steps; gaps %s; the walk reads %s and shelf 15's grammar over those "
                  "same gaps reads %s; the crest stands at step %s"
                  % (shape["works"], shape["steps"], shape["gaps"], shape["roles"], want,
                     (shape["crest"] or 0) + 1))

            # 1 · the realised dynamics
            share = shape.get("share") or {}
            n = max(1, shape.get("steps") or 1)
            check(BROWSER_ROWS[1],
                  share.get("culmination") == 1
                  and share.get("quiet link", 0) >= share.get("middle", 0),
                  "over %d steps: %d quiet, %d middle, %d culmination — how the grammar divided one "
                  "dealt hang, printed so a person can read it and gated on nothing"
                  % (n, share.get("quiet link", 0), share.get("middle", 0),
                     share.get("culmination", 0)))

            # 2 · the role reaches the composer. The visit's first crossing is the real step
            # `enter` took, and it is an entrance by the rule above; the step measured here is the
            # SECOND, where the curve is what answers.
            first = js(br, "var rows = window.__exPass.report().composer.passages;"
                           "var row = rows.length ? rows[0] : null;"
                           "return {absent: !row,"
                           " asked: row && row.request ? row.request.routeRole : null,"
                           " crossed: row && row.request ? (row.request.sessionMemory || null)"
                           "          : null};")
            second = declare(br, ids[1], ids[2]) if len(ids) > 2 else {"absent": True}
            check(BROWSER_ROWS[2],
                  not second.get("absent") and second.get("asked") == shape["roles"][1]
                  and second.get("read") == second.get("asked"),
                  "the walk asked for «%s» on step 2 and the composer read «%s»; the curve names "
                  "«%s» there" % (second.get("asked"), second.get("read"),
                                  shape["roles"][1] if len(shape["roles"]) > 1 else "?"))

            # 3 · the steps of one route do not all read alike
            kinds = sorted(set(shape["roles"]))
            check(BROWSER_ROWS[3], len(kinds) >= 2,
                  "the route's %d steps carry %d different functions: %s"
                  % (shape["steps"], len(kinds), kinds))

            # 4 · the entrance is the first crossing and only the first
            check(BROWSER_ROWS[4],
                  first.get("asked") == "entrance" and second.get("asked") != "entrance",
                  "the visit's first crossing asked «%s» and the one after it «%s»"
                  % (first.get("asked"), second.get("asked")))

            # 5 · a walked-back edge is a return, and the reference crosses on it
            js(br, LAND)
            back = declare(br, ids[2], ids[1], direction=-1) if len(ids) > 2 else {"absent": True}
            js(br, LAND)
            check(BROWSER_ROWS[5],
                  back.get("asked") == "return" and bool(back.get("crossed"))
                  and sorted((back.get("crossed") or {}).keys()) == ["family", "passIndex", "seed"],
                  "walking the same edge back asked «%s» and carried %s"
                  % (back.get("asked"), back.get("crossed")))

            # 6 · a step off the route's own thread states no function
            off = declare(br, ids[0], ids[len(ids) - 1]) if len(ids) > 3 else {"absent": True}
            check(BROWSER_ROWS[6],
                  off.get("asked") is None and off.get("read") == "middle",
                  "a step between two works standing %d apart in the hang asked «%s», and the "
                  "composer read «%s»" % (len(ids) - 1, off.get("asked"), off.get("read")))

            # 7 · the unfold lengthens the route
            grew = js(br, "var b = document.getElementById('ex-unfold');"
                          "if (b) b.click();"
                          "return {clicked: !!b};")
            br.sleep(1.0)
            longer = js(br, "return window.__exPass.report().route;")
            check(BROWSER_ROWS[7],
                  grew["clicked"] and longer["steps"] > shape["steps"]
                  and longer["roles"] == grammar(longer["gaps"]),
                  "«ещё 5» took the route from %d steps to %d, and the grammar over the longer "
                  "curve reads the walk's own roles back: %s"
                  % (shape["steps"], longer["steps"], longer["share"]))

            # ---- the four red-on-bug rows, each on a COPY of the served bundle ----
            for row, name, want_of in (
                    (8, "crest", "culmination"),
                    (9, "widening", "middle")):
                if not plant(name):
                    check(BROWSER_ROWS[row], False,
                          "the line this plant reverts stands %d time(s) in the served bundle"
                          % ORIGINAL.count(PLANTS[name][0]))
                    continue
                enter(br, base)
                planted = js(br, "return window.__exPass.report().route;")
                unplant()
                enter(br, base)
                stands = js(br, "return window.__exPass.report().route;")
                # THE FLOOR EACH PLANT LEAVES BEHIND. Reverting the crest rule leaves no culmination
                # at all. Reverting the local-widening rule leaves exactly the one middle the crest's
                # own preparation is, since that line is a separate rule and this plant does not
                # touch it — so the row measures the collapse rather than an emptying.
                floor = 0 if name == "crest" else (1 if (planted["crest"] or 0) > 0 else 0)
                check(BROWSER_ROWS[row],
                      (planted["share"].get(want_of, 0) == floor
                       and stands["share"].get(want_of, 0) > floor),
                      "with the rule reverted the route carries %d step(s) of «%s» (%s), which is "
                      "the %d the other rules still name; with it standing it carries %d (%s)"
                      % (planted["share"].get(want_of, 0), want_of, planted["share"], floor,
                         stands["share"].get(want_of, 0), stands["share"]))

            # the return rule
            if plant("return"):
                enter(br, base)
                ids2 = js(br, "return window.__exPass.report().route.ids;")
                declare(br, ids2[1], ids2[2])
                js(br, LAND)
                planted_back = declare(br, ids2[2], ids2[1], direction=-1)
                unplant()
                check(BROWSER_ROWS[10],
                      planted_back.get("asked") != "return" and back.get("asked") == "return",
                      "with the rule reverted a walked-back edge asks «%s»; with it standing it "
                      "asks «%s»" % (planted_back.get("asked"), back.get("asked")))
            else:
                check(BROWSER_ROWS[10], False, "the return line was not found in the served bundle")

            # the entrance rule
            if plant("entrance"):
                enter(br, base)
                planted_first = js(br, "var rows = window.__exPass.report().composer.passages;"
                                       "var row = rows.length ? rows[0] : null;"
                                       "return {asked: row && row.request"
                                       "        ? row.request.routeRole : null};")
                unplant()
                check(BROWSER_ROWS[11],
                      planted_first.get("asked") != "entrance"
                      and first.get("asked") == "entrance",
                      "with the rule reverted the visit's first crossing asks «%s»; with it "
                      "standing it asks «%s»" % (planted_first.get("asked"), first.get("asked")))
            else:
                check(BROWSER_ROWS[11], False, "the entrance line was not found in the served bundle")

shutil.rmtree(TMP, ignore_errors=True)

print()
for name, verdict, detail in results:
    print("[%s] %s%s" % (verdict, name, ("  — " + detail) if detail else ""))
n_pass = sum(1 for r in results if r[1] == "PASS")
n_fail = sum(1 for r in results if r[1] == "FAIL")
n_skip = sum(1 for r in results if r[1] == "SKIP")
print("\n%d rows: %d pass, %d fail, %d skip" % (len(results), n_pass, n_fail, n_skip))
sys.exit(1 if n_fail else 0)
