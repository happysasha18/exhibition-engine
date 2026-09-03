#!/usr/bin/env python3
"""EX-HARMONY — the ordering grammar of the walk: keys, functions, modulation, cadences.
Run: python3 tests/test_pass_harmony.py

Root: charter shelf 15 (`SPEC.md` Requirement 27, in the tlvphotos tree), «THE HARMONIC LAYER». Its
own words: every station of the walk carries a FUNCTION relative to the current KEY, and a key is a
region of the collection's space — a matter family plus a palette world. Tonic is home, the eye
settles; subdominant is motion away, preparation; dominant is tension that demands resolution, and
the culmination crossing is a dominant. The walk changes key through a PIVOT WORK whose recipe
belongs to both families. Cadences land the walk: authentic is dominant onto home, plagal the soft
one, and the deceptive cadence — home promised, an unexpected kin arrived at — is a rare event. The
grammar is a small state machine over functions, read live off each work's own record at the moment
of casting, never stored per work or per pair; it orders the performance and never reaches inside a
single crossing.

WHAT THIS MEASURES, and how it is anchored.

  THE LAYER IS RUN, NOT DESCRIBED. The whole block — the record readings, the key, the modulation
  walk, the functions, the role map and the cadences — is extracted verbatim from the BUILT client
  (`engine/assets/exhibition.js`) and executed in node against routes this file builds. The walk's
  own surroundings are the only things stubbed: the hung order, the kinship coordinates and the map
  of records the walk holds. Nothing of the grammar is re-typed here, so a change to the rule moves
  what runs and the rows go on judging the same claim.

  THE RULE IS RE-DERIVED AND COMPARED. Every judged row recomputes the shelf's rule in Python from
  what the layer publishes beside its answer — the gaps, the served records, the keys it named —
  and compares. A row reddens when the layer stops reading the grammar it says it reads, never
  because the content moved.

  THE SWEEP IS EXHAUSTIVE, NOT SAMPLED. Rows H3, H4, H8 and H11 run EVERY route of three, four and
  five works whose steps are drawn from a three-value gap alphabet and whose works are drawn from a
  three-record alphabet — every shape of that size, none picked at random and none left out. A
  claim that holds over all of them holds by construction over that space, and the hand-built cases
  below pin the claims a small space cannot reach: the pivot, the deceptive landing, and a key
  change with nothing belonging to both families.

  NO ROW COUNTS PHOTOGRAPHS. What is counted here is routes this file generated, never works or
  pairs of the collection, and no row asserts a proportion of anything.

Rows:
  H1  the harmonic layer travels as one block of the shipped client, and runs on its own
  H2  the five names the walk can state come out of ONE map over the three functions, and are
      exactly the five the composer fences on
  H3  every step of every route carries one of the three functions — the reading ranks, never refuses
  H4  the five names are the IMAGE of the functions, and the image is still shelf 15's own curve
      grammar: the crest is the culmination, its approach and the widenings are middles
  H5  a key is named off the work's own record — matter family and palette world — and a work whose
      record has not arrived names none
  H6  the walk changes key THROUGH a pivot work that belongs to both families, not by cutting at the
      step where the new key first stands
  H7  a key change with nothing belonging to both families still lands, and every step still carries
      a function — no walk is refused for want of a pivot
  H8  the crest stays the crest: it is the one dominant the route builds to, and it is the culmination
  H9  the three cadences land where the shelf says they do
  H10 the deceptive landing is rare by the walk's own reading: three readings must hold at once, and
      dropping any one of them leaves none
  H11 a walk holding no records reads exactly as the curve alone read it — the key adds, never removes
  H12 red-on-bug · the pivot reverted to a cut: the key changes at the first foreign work
  H13 red-on-bug · the role map reverted to a second ordering read off the curve
  H14 a progression replayed in a key two axes away is a reprise, named where the later era opens
  H15 the same progression returning one axis away is not a reprise — the «two axes changed» rule
  H16 every reprise holds all three readings at once and points only backward
  H17 the reprise is a reading and never a name: silencing it moves nothing the walk does
  H18 red-on-bug · the «two axes changed» rule reverted to one axis
  H19 the passage request carries the function beside the name, so a preparation and a tension
      reach the composer telling apart where the five names call both a middle
  H20 red-on-bug · the function line dropped from the request

node is a hard dependency (the layer is the test) — its absence FAILS, never skips. The source tree
is never written to: the two red-on-bug rows run a COPY of the extracted block with one rule put
back, in a temporary file that is removed afterwards.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
COMPOSER = (ROOT / "engine" / "assets" / "pass-composer.js").read_text(encoding="utf-8")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def report_and_exit():
    for n, s, d in results:
        print(f"{s}  {n}" + (f"   — {d}" if d else ""))
    bad = sum(1 for _, s, _ in results if s == "FAIL")
    print(f"\n{len(results) - bad} passed / {bad} failed")
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- H1: the block, extracted
START = "  function passMatterOf(rec) {"
END = "  // Which step of the route this edge is"
REQ_END = "  // THE PASSAGE REQUEST"
BLOCK = None
if START in BUNDLE and END in BUNDLE and BUNDLE.index(START) < BUNDLE.index(END):
    BLOCK = BUNDLE[BUNDLE.index(START):BUNDLE.index(END)]
# …and the step-to-station half that stands after it: which step of the route an edge is, whether
# this visit's thread has opened, and the station a step is for this person at this instant.
STATION = None
if BLOCK is not None and REQ_END in BUNDLE and BUNDLE.index(END) < BUNDLE.index(REQ_END):
    STATION = BUNDLE[BUNDLE.index(END):BUNDLE.index(REQ_END)]
# …and the lines of the passage request that put the two readings on it. These are lifted verbatim
# so the lines that ship are the lines that run here.
REQ_FIRST = "    const station = passRouteStation(from, to, edge);"
REQ_LAST = "    if (station.fn) req.routeFunction = station.fn;"
REQUEST = None
if REQ_FIRST in BUNDLE and REQ_LAST in BUNDLE and BUNDLE.index(REQ_FIRST) < BUNDLE.index(REQ_LAST):
    REQUEST = BUNDLE[BUNDLE.index(REQ_FIRST):BUNDLE.index(REQ_LAST) + len(REQ_LAST)]

NODE = shutil.which("node")

# ---------------------------------------------------------------- the driver
# The layer's own surroundings, and nothing else: the hung order, the kinship coordinates the walk
# measures its gaps in, and the map of records it holds at this instant. Positions are laid on one
# axis, so the distance between two neighbours is exactly the gap the case asks for.
DRIVER = r"""
'use strict';
function makeWalk(ids, positions, recsMap) {
  const order = ids, shown = ids.length;
  const place = {};
  ids.forEach(function (id, i) { place[id] = [positions[i]]; });
  const vec = (id) => place[id];
  const dist = (p, q) => {
    let s = 0;
    for (let i = 0; i < p.length; i++) { const d = p[i] - q[i]; s += d * d; }
    return Math.sqrt(s);
  };
  const passWorkRecords = () => recsMap;
  // The visit's own two facts, stubbed so the station rows read the ROUTE rather than the opening:
  // a thread this visit has already opened, and an edge handed in with no pass on it.
  const PASS_EDGE = { visitWindowSeconds: 1 };
  const passEdgeAll = () => ({ opened: { "a-to-b": { lastAt: 0 } } });
  const passEdgeNow = () => 0;
__BLOCK__
__STATION__
  // The two lines of the passage request that put the walk's two readings on it, lifted verbatim
  // from the built client and run here on a station the walk itself derived.
  function requestFieldsFor(from, to, edge) {
    const req = {};
__REQUEST__
    return req;
  }
  return { shape: passRouteShape, roleOf: passRoleOfFunction, key: passWorkKey,
           standing: passStandingIn, station: passRouteStation, request: requestFieldsFor };
}

// The three records every generated route draws its works from, and the pivot record the hand-built
// cases add. Each is a work record of the shape the settings record ships: a `structure` block whose
// scored entries say what the picture is made of, and a `palette` block whose leading hue and hold
// say which palette world it is in.
const REC = {
  A: { structure: { radial: { score: 0.9 }, grid: { score: 0.1 } },
       palette: { hues: ["blue"], hueConcentration: 0.9 } },
  B: { structure: { radial: { score: 0.1 }, grid: { score: 0.9 } },
       palette: { hues: ["red"], hueConcentration: 0.9 } },
  // C stands ONE axis from A — the matter family moved, the palette world did not. It is what the
  // reprise rows measure the «two axes changed» rule against.
  C: { structure: { radial: { score: 0.1 }, grid: { score: 0.9 } },
       palette: { hues: ["blue"], hueConcentration: 0.9 } },
  P: { structure: { radial: { score: 0.8 }, grid: { score: 0.7 } },
       palette: { hues: ["blue", "red"], hueConcentration: 0.8 } },
  none: null
};

function runCase(letters, gaps) {
  const ids = letters.map((l, i) => "w" + i + l);
  const pos = [0];
  gaps.forEach((g) => pos.push(pos[pos.length - 1] + g));
  const recs = {};
  letters.forEach((l, i) => { if (REC[l]) recs[ids[i]] = Object.assign({ id: ids[i] }, REC[l]); });
  const w = makeWalk(ids, pos, recs);
  const s = w.shape();
  return { letters: letters, gaps: gaps, ids: ids,
           keys: s.keys, keyAt: s.keyAt, standing: s.standing, functions: s.functions,
           roles: s.roles, crest: s.crest, cadences: s.cadences, modulations: s.modulations,
           eras: s.eras, reprises: s.reprises };
}

const out = [];
// the role map, asked directly at every one of its inputs
{
  const w = makeWalk(["x", "y"], [0, 1], {});
  out.push({ what: "roleMap", rows: [
    ["tonic", "restated", w.roleOf("tonic", "restated")],
    ["tonic", "founding", w.roleOf("tonic", "founding")],
    ["tonic", "route", w.roleOf("tonic", "route")],
    ["dominant", "crest", w.roleOf("dominant", "crest")],
    ["dominant", "route", w.roleOf("dominant", "route")],
    ["subdominant", "route", w.roleOf("subdominant", "route")],
    ["subdominant", "crest", w.roleOf("subdominant", "crest")]
  ] });
  // the key each record names, asked of the reading itself
  out.push({ what: "keys", rows: Object.keys(REC).map(function (l) {
    return [l, w.key(REC[l] ? Object.assign({ id: l }, REC[l]) : null),
            w.standing(REC[l] ? Object.assign({ id: l }, REC[l]) : null,
                       { matter: "radial", palette: "blue" })];
  }) });
}
// the exhaustive sweeps — one over two keys standing TWO axes apart, one over two keys standing ONE
const GAPS = [1, 2, 3];
function words(alpha, n) {
  let acc = [[]];
  for (let i = 0; i < n; i++) {
    const next = [];
    acc.forEach((w) => alpha.forEach((a) => next.push(w.concat([a]))));
    acc = next;
  }
  return acc;
}
[["sweep", ["A", "B", "none"]], ["sweep1", ["A", "C", "none"]]].forEach(function (pair) {
  for (let n = 3; n <= 5; n++) {
    const ws = words(pair[1], n), gs = words(GAPS, n - 1);
    ws.forEach((letters) => gs.forEach(function (gaps) {
      out.push({ what: pair[0], got: runCase(letters, gaps) });
    }));
  }
});
// THE REPRISE SWEEP. A route of three to five works cannot hold two eras of two steps each, so the
// sweeps above can only ever name the odd reprise. These two fix the works — eight of them, with a
// pivot work in the middle, so the walk always changes key half way and both eras always have a
// progression to open with — and run EVERY gap shape those seven steps can take. One stands the
// second era two axes from the first; the other stands it one axis away.
[["sweepR", "B"], ["sweepR1", "C"]].forEach(function (pair) {
  const letters = ["A", "A", "A", "P", pair[1], pair[1], pair[1], pair[1]];
  words(GAPS, letters.length - 1).forEach(function (gaps) {
    out.push({ what: pair[0], got: runCase(letters, gaps) });
  });
});
// the hand-built cases
out.push({ what: "pivot", got: runCase(["A", "A", "A", "A", "P", "B", "B", "B"],
                                       [1, 2, 1, 3, 1, 5, 1]) });
// One progression, returning in a key TWO axes away and in a key ONE axis away. The two routes are
// the same shape work for work and gap for gap; only the family the second half stands in differs.
const RGAPS = [1, 2, 1, 1, 1, 2, 1, 1, 5];
out.push({ what: "reprise",
           got: runCase(["A", "A", "A", "A", "P", "B", "B", "B", "B", "B"], RGAPS) });
out.push({ what: "nearReprise",
           got: runCase(["A", "A", "A", "A", "P", "C", "C", "C", "C", "C"], RGAPS) });
// WHAT THE PASSAGE REQUEST CARRIES for the two stations the five names cannot tell apart. The
// culmination has a name of its own, so the pair that matters is a subdominant and a dominant that
// is NOT the crest — a widening that carried the eye out of the key. This route stands one foreign
// work at a widening, alone, so no key change follows it and the widening reads as a dominant while
// the walk is still in its opening key; both it and the crest's own preparation ask under «middle».
{
  const letters = ["A", "A", "B", "A", "A", "A", "A"];
  const gaps = [1, 3, 1, 1, 1, 6];
  const ids = letters.map((l, i) => "w" + i + l);
  const pos = [0];
  gaps.forEach((g) => pos.push(pos[pos.length - 1] + g));
  const recs = {};
  letters.forEach((l, i) => { if (REC[l]) recs[ids[i]] = Object.assign({ id: ids[i] }, REC[l]); });
  const w = makeWalk(ids, pos, recs);
  const s = w.shape();
  const pick = { subdominant: s.functions.indexOf("subdominant"),
                 dominant: s.functions.findIndex((f, i) => f === "dominant" && i !== s.crest) };
  const rows = Object.keys(pick).map(function (want) {
    const i = pick[want];
    return { want: want, at: i, crest: s.crest,
             station: i < 0 ? null : w.station(ids[i], ids[i + 1], null),
             request: i < 0 ? null : w.request(ids[i], ids[i + 1], null) };
  });
  out.push({ what: "request", rows: rows, functions: s.functions, roles: s.roles });
}
out.push({ what: "noBridge", got: runCase(["A", "A", "A", "B", "B", "B"], [1, 2, 1, 3, 1]) });
out.push({ what: "deceptive", got: runCase(["A", "A", "A", "A", "A", "B"], [1, 2, 1, 5, 1]) });
out.push({ what: "blind", got: runCase(["none", "none", "none", "none", "none", "none"],
                                       [1, 2, 1, 5, 1]) });
out.push({ what: "seeing", got: runCase(["A", "A", "A", "A", "A", "A"], [1, 2, 1, 5, 1]) });
process.stdout.write(out.map((r) => JSON.stringify(r)).join("\n"));
"""


def run_block(block, tag, station=None, request=None):
    """One node run of one copy of the three lifted pieces. The copy lives in a temporary file and
    is removed; the source tree is never written to."""
    src = (DRIVER.replace("__BLOCK__", block)
                 .replace("__STATION__", STATION if station is None else station)
                 .replace("__REQUEST__", REQUEST if request is None else request))
    fh = tempfile.NamedTemporaryFile("w", suffix="_%s.js" % tag, delete=False, encoding="utf-8")
    fh.write(src)
    fh.close()
    try:
        run = subprocess.run([NODE, fh.name], capture_output=True, text=True, timeout=180)
    finally:
        Path(fh.name).unlink(missing_ok=True)
    if run.returncode != 0:
        return None, (run.stderr or run.stdout or "").strip().splitlines()[-1:]
    rows = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    return rows, None


check("H1 EX-HARMONY the harmonic layer travels as one block of the shipped client, with the station "
      "it answers a step with and the request lines that carry that answer",
      BLOCK is not None and STATION is not None and REQUEST is not None,
      "" if (BLOCK and STATION and REQUEST) else
      "missing from engine/assets/exhibition.js: %s"
      % ", ".join(n for n, v in (("the layer block", BLOCK), ("the station block", STATION),
                                 ("the request lines", REQUEST)) if v is None))
if BLOCK is None or STATION is None or REQUEST is None:
    report_and_exit()
if not NODE:
    check("H1 EX-HARMONY node present (the layer is the test)", False, "node not on PATH")
    report_and_exit()

ROWS, why = run_block(BLOCK, "shipped")
if ROWS is None:
    check("H1 EX-HARMONY the extracted block runs on its own", False, "node said: %s" % (why or ""))
    report_and_exit()

BY = {}
for r in ROWS:
    BY.setdefault(r["what"], []).append(r)
SWEEP = [r["got"] for r in BY.get("sweep", [])]
SWEEP1 = [r["got"] for r in BY.get("sweep1", [])]
SWEEPR = [r["got"] for r in BY.get("sweepR", [])]
SWEEPR1 = [r["got"] for r in BY.get("sweepR1", [])]
HAND = {k: BY[k][0]["got"] for k in
        ("pivot", "noBridge", "deceptive", "blind", "seeing", "reprise", "nearReprise") if k in BY}

# ---------------------------------------------------------------- H2: one map, five names
FENCED = re.search(r'var ROUTE_ROLES = \[([^\]]+)\]', COMPOSER)
FENCED = set(re.findall(r'"([^"]+)"', FENCED.group(1))) if FENCED else set()
MAP = {(a, b): c for a, b, c in BY["roleMap"][0]["rows"]}
check("H2 EX-HARMONY the five names come out of one map over the three functions, and are exactly "
      "the five the composer fences on",
      bool(FENCED) and set(MAP.values()) == FENCED
      and MAP[("tonic", "restated")] == "return"
      and MAP[("tonic", "founding")] == "entrance"
      and MAP[("tonic", "route")] == "quiet link"
      and MAP[("dominant", "crest")] == "culmination"
      and MAP[("dominant", "route")] == "middle"
      and MAP[("subdominant", "route")] == "middle"
      and MAP[("subdominant", "crest")] == "middle",
      "the map answers %s; the composer accepts %s"
      % (sorted(set(MAP.values())), sorted(FENCED)))

# ---------------------------------------------------------------- H3: every step has a function
FUNCTIONS = {"tonic", "subdominant", "dominant"}
unread = [c for c in SWEEP if not c["functions"]
          or any(f not in FUNCTIONS for f in c["functions"])]
check("H3 EX-HARMONY every step of every route carries one of the three functions — the reading "
      "ranks and never refuses",
      SWEEP and not unread,
      "%d routes swept (every route of 3, 4 and 5 works over the gap and record alphabets), "
      "%d with a step the grammar left unread" % (len(SWEEP), len(unread)))


# ---------------------------------------------------------------- H4: the names are the image
def grammar(gaps):
    """Shelf 15's own curve grammar, re-derived here. The widest step after the opening is the one
    crest; the step leading into it prepares it; a step standing above both its neighbours is a
    widening; everything else is where the eye settles."""
    crest = 1 if len(gaps) > 1 else 0
    for i in range(crest + 1, len(gaps)):
        if gaps[i] > gaps[crest]:
            crest = i
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
    return crest, out


def image(functions, crest):
    """The five names as the image of the three functions, re-derived. A route read here is never
    a step a visitor has already walked and never a visit's opening, so the tonic goes by the one
    name it goes by on the route itself."""
    return [("culmination" if i == crest else "middle") if f == "dominant"
            else "middle" if f == "subdominant" else "quiet link"
            for i, f in enumerate(functions)]


off_image = [c for c in SWEEP if c["roles"] != image(c["functions"], c["crest"])]
off_curve = [c for c in SWEEP if (c["crest"], c["roles"]) != grammar(c["gaps"])]
check("H4 EX-HARMONY the five names are the image of the functions, and that image is still shelf "
      "15's own curve grammar — the crest is the culmination, its approach and the widenings middles",
      SWEEP and not off_image and not off_curve,
      "%d routes swept; %d where a name is not the image of its own function, %d where the image "
      "parts company with the curve grammar" % (len(SWEEP), len(off_image), len(off_curve)))

# ---------------------------------------------------------------- H5: the key is named off the record
KEYNAMES = {l: k for l, k, _ in BY["keys"][0]["rows"]}
STANDINGS = {l: s for l, _, s in BY["keys"][0]["rows"]}
check("H5 EX-HARMONY a key is named off the work's own record — the matter family its structure "
      "block scores highest, and the palette world its palette block leads with — and a work whose "
      "record has not arrived names none",
      KEYNAMES["A"] == {"matter": "radial", "palette": "blue"}
      and KEYNAMES["B"] == {"matter": "grid", "palette": "red"}
      and KEYNAMES["P"] == {"matter": "radial", "palette": "blue"}
      and KEYNAMES["none"] is None and STANDINGS["none"] is None
      and STANDINGS["A"] > STANDINGS["P"] > STANDINGS["B"],
      "A names %s, B names %s, the pivot record names %s and a work with no record names %s; "
      "standing in radial/blue reads A %s, pivot %s, B %s"
      % (KEYNAMES["A"], KEYNAMES["B"], KEYNAMES["P"], KEYNAMES["none"],
         STANDINGS["A"], STANDINGS["P"], STANDINGS["B"]))

# ---------------------------------------------------------------- H6: the change goes through a pivot
# The hand-built route stands four works in radial/blue, then a work whose record holds strongly in
# BOTH families, then three works in grid/red. A cut would change key at the first grid/red work
# (index 5); the shelf asks the change to be declared at the work belonging to both (index 4).
PIV = HAND.get("pivot", {})
PIV_MODS = PIV.get("modulations") or []
first_foreign = next((i for i, k in enumerate(PIV.get("keys") or []) if k == "grid/red"), None)
check("H6 EX-HARMONY the walk changes key THROUGH a pivot work that belongs to both families, not "
      "by cutting at the step where the new key first stands",
      len(PIV_MODS) == 1 and PIV_MODS[0]["at"] == 4 and first_foreign == 5
      and PIV_MODS[0]["from"] == "radial/blue" and PIV_MODS[0]["to"] == "grid/red"
      and (PIV.get("keyAt") or [])[4] == "grid/red"
      and (PIV.get("keyAt") or [])[3] == "radial/blue",
      "the key changes at %s (the new key first stands at %s), %s, belonging %s"
      % (PIV_MODS[0]["at"] if PIV_MODS else "nowhere", first_foreign,
         "%s → %s" % (PIV_MODS[0]["from"], PIV_MODS[0]["to"]) if PIV_MODS else "-",
         PIV_MODS[0]["belonging"] if PIV_MODS else "-"))

# ---------------------------------------------------------------- H7: no walk refused for want of one
NB = HAND.get("noBridge", {})
NB_MODS = NB.get("modulations") or []
check("H7 EX-HARMONY a key change with nothing belonging to both families still lands, and every "
      "step still carries a function — no walk is refused for want of a pivot",
      len(NB_MODS) == 1 and NB_MODS[0]["to"] == "grid/red"
      and all(f in FUNCTIONS for f in (NB.get("functions") or []))
      and len(NB.get("functions") or []) == len(NB.get("gaps") or [None]),
      "the change lands at %s with belonging %s, and the route's functions read %s"
      % (NB_MODS[0]["at"] if NB_MODS else "nowhere",
         NB_MODS[0]["belonging"] if NB_MODS else "-", NB.get("functions")))

# ---------------------------------------------------------------- H8: the crest stays the crest
bad_crest = [c for c in SWEEP
             if c["functions"][c["crest"]] != "dominant"
             or c["roles"][c["crest"]] != "culmination"
             or c["roles"].count("culmination") != 1]
check("H8 EX-HARMONY the crest stays the crest: the step the route builds to is a dominant, it is "
      "the culmination, and a route has one",
      SWEEP and not bad_crest,
      "%d routes swept, %d whose crest is not the one dominant culmination"
      % (len(SWEEP), len(bad_crest)))


# ---------------------------------------------------------------- H9: the cadences
def cadences(case):
    """The shelf's landings, re-derived from what the layer publishes beside its answer: a step
    whose pull falls below the one before it is a landing, and what raised it and where it arrives
    say which landing it is."""
    gaps, fns, st = case["gaps"], case["functions"], case["standing"]
    out = []
    for i, g in enumerate(gaps):
        away = st[i] is not None and (1 - st[i]) > st[i]
        if i == 0 or not g < gaps[i - 1]:
            out.append(None)
        elif fns[i - 1] == "dominant":
            out.append("deceptive" if away else "authentic")
        elif fns[i - 1] == "subdominant":
            out.append(None if away else "plagal")
        else:
            out.append(None)
    return out


off_cad = [c for c in SWEEP if c["cadences"] != cadences(c)]
DEC = HAND.get("deceptive", {})
check("H9 EX-HARMONY the three cadences land where the shelf says they do — a dominant onto home "
      "is authentic, a subdominant onto home is plagal, a dominant onto a work outside the key is "
      "deceptive",
      SWEEP and not off_cad and (DEC.get("cadences") or [])[-1] == "deceptive"
      and (DEC.get("functions") or [])[-2] == "dominant",
      "%d routes swept, %d whose landings part company with the rule; the hand-built route lands %s"
      % (len(SWEEP), len(off_cad), DEC.get("cadences")))

# ---------------------------------------------------------------- H10: the deception is conjunctive
# Three readings have to hold at once on one step, and none of them is a number chosen here. The row
# proves that by construction: every deceptive landing holds all three, and relaxing any one of the
# three — the step before it being a dominant, the pull falling, the arrival standing outside the
# key — leaves the walk with no deceptive landing at all.
holds, breaks = 0, []
for c in SWEEP + list(HAND.values()):
    gaps, fns, st, cad = c["gaps"], c["functions"], c["standing"], c["cadences"]
    for i, name in enumerate(cad):
        if name != "deceptive":
            continue
        raised = i > 0 and fns[i - 1] == "dominant"
        fell = i > 0 and gaps[i] < gaps[i - 1]
        away = st[i] is not None and (1 - st[i]) > st[i]
        if raised and fell and away:
            holds += 1
        else:
            breaks.append((c["letters"], gaps, i, raised, fell, away))
relaxed = [c for c in SWEEP + list(HAND.values())
           for i, name in enumerate(c["cadences"])
           if name == "deceptive" and (c["standing"][i] is None
                                       or not (1 - c["standing"][i]) > c["standing"][i])]
check("H10 EX-HARMONY the deceptive landing is rare by the walk's own reading: three readings hold "
      "at once on it, and no landing is called deceptive with any one of them missing",
      holds > 0 and not breaks and not relaxed,
      "%d deceptive landings, all three readings holding on each; %d called deceptive without them"
      % (holds, len(breaks)))

# ---------------------------------------------------------------- H11: a walk holding no records
blind_sweep = [c for c in SWEEP if all(l == "none" for l in c["letters"])]
seen_sweep = {tuple(c["gaps"]): c for c in SWEEP if all(l == "A" for l in c["letters"])}
drifted = [c for c in blind_sweep
           if c["roles"] != grammar(c["gaps"])[1]
           or any(k != "-" for k in c["keys"])
           or c["modulations"]
           or (tuple(c["gaps"]) in seen_sweep
               and c["functions"] != seen_sweep[tuple(c["gaps"])]["functions"])]
BLIND, SEEING = HAND.get("blind", {}), HAND.get("seeing", {})
check("H11 EX-HARMONY a walk holding no records reads exactly as the curve alone read it — no key, "
      "no key change, and the same functions and names a walk holding records in one key reads",
      blind_sweep and not drifted
      and BLIND.get("roles") == SEEING.get("roles")
      and BLIND.get("functions") == SEEING.get("functions")
      and not BLIND.get("modulations"),
      "%d record-less routes swept, %d that drifted off the curve; the hand-built blind route reads "
      "%s and the same route holding records reads %s"
      % (len(blind_sweep), len(drifted), BLIND.get("functions"), SEEING.get("functions")))

# ---------------------------------------------------------------- H12/H13: red on bug
# Each runs a COPY of the extracted block with one rule put back the way it stood before the layer
# existed. The copy lives in a temporary file; the source tree is never written to.
CUT = BLOCK.replace("if (both >= best) { best = both; at = j; }",
                    "if (j === i) { best = both; at = j; }")
rows, why = run_block(CUT, "cut") if CUT != BLOCK else (None, "the pivot search did not match")
cut_at = None
if rows:
    cut_at = ((next(r for r in rows if r["what"] == "pivot")["got"]["modulations"] or [{}])[0]
              .get("at"))
check("H12 EX-HARMONY red-on-bug · the pivot reverted to a cut: the key then changes at the first "
      "work of the new family instead of at the work belonging to both",
      cut_at == 5 and PIV_MODS and PIV_MODS[0]["at"] == 4,
      "with the pivot search reverted the change lands at %s; the shipped rule lands it at %s"
      % (cut_at, PIV_MODS[0]["at"] if PIV_MODS else "-"))

SECOND = BLOCK.replace(
    'const roles = functions.map((fn, i) => passRoleOfFunction(fn, i === crest ? "crest" : "route"));',
    'const roles = gaps.map((g, i) => {\n'
    '      if (i === crest) return "culmination";\n'
    '      const b = i > 0 ? gaps[i - 1] : -Infinity, a = i + 1 < gaps.length ? gaps[i + 1]\n'
    '                                                                        : -Infinity;\n'
    '      return (g > b && g > a) ? "middle" : "quiet link";\n'
    '    });')
rows2, why2 = run_block(SECOND, "second") if SECOND != BLOCK else (None, "the role map did not match")
split = []
if rows2:
    for r in rows2:
        if r["what"] != "sweep":
            continue
        c = r["got"]
        if c["roles"] != image(c["functions"], c["crest"]):
            split.append(c)
check("H13 EX-HARMONY red-on-bug · the role map reverted to a second ordering read straight off the "
      "curve: the names then part company with the functions they are supposed to be the image of",
      bool(split) and not off_image,
      "with the map reverted %d of %d swept routes carry a name that is not the image of its own "
      "function; with the shipped map, %d" % (len(split), len(SWEEP), len(off_image)))

# ---------------------------------------------------------------- H14: the reprise
# One route, ten works, whose key changes at a pivot half way. The first era opens on a progression
# and the second era opens on the same one, in a key standing two axes from it.
REP = HAND.get("reprise", {})
REP_R = REP.get("reprises") or []
REP_E = REP.get("eras") or []
opening = None
if REP_R and len(REP_E) > 1:
    span = REP_R[0]["span"]
    opening = (REP_E[0]["pattern"][:span] == REP_E[1]["pattern"][:span])
check("H14 EX-HARMONY a progression replayed in a key two axes away is a reprise, named where the "
      "later era opens and pointing back at the era it echoes",
      len(REP_E) == 2 and len(REP_R) == 1 and REP_R[0]["at"] == REP_E[1]["at"]
      and REP_R[0]["of"] == REP_E[0]["at"] and REP_R[0]["span"] >= 2 and opening,
      "the route falls into %d eras — %s — and the reprise reads %s"
      % (len(REP_E), [(e["at"], e["key"], e["pattern"]) for e in REP_E], REP_R))

# ---------------------------------------------------------------- H15: one axis is not enough
# The same route, work for work and gap for gap, with the second half standing in a key that moved
# on ONE axis. The progression returns exactly as before; the shelf's «two axes changed» rule says
# that return is the one the viewer can name, and nothing here calls it a reprise.
NEAR = HAND.get("nearReprise", {})
NEAR_E = NEAR.get("eras") or []
check("H15 EX-HARMONY the same progression returning in a key ONE axis away is not a reprise — the "
      "shelf's «two axes changed» rule — and the two routes differ in nothing but the key",
      not (NEAR.get("reprises") or [])
      and NEAR.get("functions") == REP.get("functions")
      and NEAR.get("roles") == REP.get("roles")
      and [e["pattern"] for e in NEAR_E] == [e["pattern"] for e in REP_E]
      and NEAR.get("keyAt") != REP.get("keyAt"),
      "the one-axis route carries the same functions %s and the same era progressions %s, stands in "
      "%s rather than %s, and names %d reprise(s)"
      % (NEAR.get("functions"), [e["pattern"] for e in NEAR_E],
         NEAR_E[-1]["key"] if NEAR_E else "-", REP_E[-1]["key"] if REP_E else "-",
         len(NEAR.get("reprises") or [])))

# ---------------------------------------------------------------- H16: every reprise, by construction
# Three readings hold on every reprise the sweep names, and none is a number chosen here: the two
# eras stand two axes apart, their openings agree over the whole span, and the span is at least two
# functions — one function repeating is two stations doing the same thing, not a progression
# returning. And no reprise points at itself or at an era later than itself.
bad_reprise, spans = [], 0
for c in SWEEP + SWEEP1 + SWEEPR + SWEEPR1 + list(HAND.values()):
    eras = {e["at"]: e for e in (c.get("eras") or [])}
    for r in (c.get("reprises") or []):
        here, there = eras.get(r["at"]), eras.get(r["of"])
        two_axes = (here and there and r["from"] != r["to"]
                    and r["from"].split("/")[0] != r["to"].split("/")[0]
                    and r["from"].split("/")[1] != r["to"].split("/")[1])
        same_opening = (here and there
                        and here["pattern"][:r["span"]] == there["pattern"][:r["span"]])
        if two_axes and same_opening and r["span"] >= 2 and r["of"] < r["at"]:
            spans += 1
        else:
            bad_reprise.append((c["letters"], c["gaps"], r))
never_one_axis = [c for c in SWEEP1 + SWEEPR1 if c.get("reprises")]
two_era = [c for c in SWEEPR if len(c.get("eras") or []) == 2]
check("H16 EX-HARMONY every reprise holds all three readings at once — two axes apart, the same "
      "opening over its whole span, at least two functions long — and points only backward; and a "
      "route whose keys stand one axis apart never names one",
      spans > 0 and not bad_reprise and not never_one_axis and len(two_era) == len(SWEEPR),
      "%d reprises named over %d two-axis and %d one-axis routes (%d of the two-axis ones fall "
      "into the two eras a reprise needs); %d named without all three readings, %d named where "
      "only one axis moved"
      % (spans, len(SWEEP) + len(SWEEPR), len(SWEEP1) + len(SWEEPR1), len(two_era),
         len(bad_reprise), len(never_one_axis)))

# ---------------------------------------------------------------- H17: it is a reading, not a name
# The shelf's target is wordless déjà vu and its recorded failure is the viewer being able to name
# the return, so the reprise must change nothing a person can be shown. The row proves it by running
# a copy of the block with the reprise never named and comparing everything the walk does: the same
# functions, the same five names, the same landings, the same key changes, the same keys in force.
BLIND_REP = BLOCK.replace("      if (best) {\n", "      if (false) {\n")
rows3, why3 = (run_block(BLIND_REP, "noreprise") if BLIND_REP != BLOCK
               else (None, "the reprise write did not match"))
WATCH = ("functions", "roles", "cadences", "modulations", "keyAt", "keys", "standing", "eras")
moved, silent = [], 0
if rows3:
    mine = {(r["what"], tuple(r["got"]["letters"]), tuple(r["got"]["gaps"])): r["got"]
            for r in ROWS if "got" in r}
    for r in rows3:
        if "got" not in r:
            continue
        c = r["got"]
        was = mine.get((r["what"], tuple(c["letters"]), tuple(c["gaps"])))
        if was is None:
            continue
        silent += len(c.get("reprises") or [])
        if any(c.get(k) != was.get(k) for k in WATCH):
            moved.append((c["letters"], c["gaps"]))
check("H17 EX-HARMONY the reprise is a reading and never a name: with it never named, every route "
      "carries the same functions, the same five names, the same landings and the same key changes",
      bool(rows3) and not moved and silent == 0,
      "%d routes replayed with the reprise silenced, %d where anything the walk does moved"
      % (len(rows3 or []), len(moved)) if rows3 else "node said: %s" % (why3 or ""))

# ---------------------------------------------------------------- H18: red on bug
ONE_AXIS = BLOCK.replace("return a.matter !== b.matter && a.palette !== b.palette;",
                         "return a.matter !== b.matter || a.palette !== b.palette;")
rows4, why4 = (run_block(ONE_AXIS, "oneaxis") if ONE_AXIS != BLOCK
               else (None, "the two-axes rule did not match"))
near_planted = None
if rows4:
    near_planted = next(r for r in rows4
                        if r["what"] == "nearReprise")["got"].get("reprises") or []
check("H18 EX-HARMONY red-on-bug · the «two axes changed» rule reverted to one axis: the walk then "
      "names a reprise on the return the shelf calls the recorded failure",
      bool(near_planted) and not (NEAR.get("reprises") or []),
      "with the rule reverted the one-axis route names %s; with it standing it names %s"
      % (near_planted, NEAR.get("reprises")))

# ---------------------------------------------------------------- H19: the request carries both
# A subdominant and a dominant are the two stations the five names cannot tell apart — one prepares,
# the other demands resolution, and both ask under the name «middle». The request carries the name
# the walk has always sent, unchanged, and the function beside it.
REQ_CASE = BY["request"][0]
REQ = {r["want"]: r for r in REQ_CASE["rows"]}
SUB, DOM = REQ.get("subdominant") or {}, REQ.get("dominant") or {}
check("H19 EX-HARMONY the passage request carries the function beside the name, so a preparation "
      "and a tension that demands resolution reach the composer telling apart where the five names "
      "call both a middle",
      (SUB.get("request") or {}).get("routeRole") == "middle"
      and (DOM.get("request") or {}).get("routeRole") == "middle"
      and (SUB.get("request") or {}).get("routeFunction") == "subdominant"
      and (DOM.get("request") or {}).get("routeFunction") == "dominant"
      and (SUB.get("station") or {}).get("fn") == "subdominant"
      and (DOM.get("station") or {}).get("fn") == "dominant",
      "over a route reading %s, the step at %s asks %s and the step at %s asks %s"
      % (REQ_CASE.get("functions"), SUB.get("at"), SUB.get("request"),
         DOM.get("at"), DOM.get("request")))

# ---------------------------------------------------------------- H20: red on bug
# The function line dropped from a COPY of the shipped request lines. The name is untouched — which
# is the point: it was already the same for both — and the two stations go back to reaching the
# composer as one and the same thing.
NO_FN = REQUEST.replace(REQ_LAST, "")
rows5, why5 = (run_block(BLOCK, "nofunction", request=NO_FN) if NO_FN != REQUEST
               else (None, "the request line did not match"))
planted_req = {}
if rows5:
    planted_req = {r["want"]: r["request"] for r in
                   next(x for x in rows5 if x["what"] == "request")["rows"]}
check("H20 EX-HARMONY red-on-bug · the function line dropped from the request: the preparation and "
      "the tension go back to reaching the composer as one and the same middle",
      bool(planted_req)
      and planted_req.get("subdominant") == planted_req.get("dominant")
      and planted_req.get("subdominant") == {"routeRole": "middle"}
      and (SUB.get("request") or {}) != (DOM.get("request") or {}),
      "with the line dropped both stations ask %s; with it standing they ask %s and %s"
      % (planted_req.get("subdominant"), SUB.get("request"), DOM.get("request")))

report_and_exit()
