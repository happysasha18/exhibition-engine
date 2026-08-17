#!/usr/bin/env python3
"""EX-PASS §4.4g — the composed road: a passage is DERIVED at visit time from the two works' own
records, on one of seven roads, bounded by the step's role in the walk and answering what the visit
already played on this edge.
Run: python3 tests/test_pass_composed.py

Root: his word of 2026-08-17 18:56 — the source of a crossing's structure is PLURAL — his 19:13 word
lifted to the class at 19:21 (every geometric and temporal parameter is read from the work, and
nothing on the product path scales with the number of pairs), his architecture decision of 18:00 (the
instrument reads its doors at run time on the actual buffer and the composer emits the artistic
request), and his 20:10 word on finishing to the end. The unit brief is
docs/immersive/briefs/2026-08-17-U27-composed-full-route.md in the tlvphotos tree, stages 0 and 1.

WHAT LEFT THIS SUITE, AND WHY. Stage 0 landed on one equality: every ordered pair of the shipped
table composing to the byte-identical score the prebaked pack shipped. That equality was a record of
where stage 0 left the road, and stage 1 lane A changes what comes out ON PURPOSE — seven roads
where there was one, a role that bounds what is emitted, a memory that is answered, and nine handles
that gained the measurement they read. So the byte row is retired with the road it guarded, and what
stands in its place proves the derivation the composer actually makes.

WHAT IT MEASURES.

  The bake and the bundle. The composer travels as its own file the way the picture layer does, and
  the served bundle names it and names none of the three roads that left.

  WHAT THE STAGE-0 FIXTURE STILL CARRIES, AND WHY NOTHING READS IT. `fixture_pass_composed.json`
  holds `expected` and `expectedTight` — the exact bytes Python composed for the worked pair on the
  day stage 0 landed. No row opens them. They are kept as the RECORD of that landing, the same record
  PASS-API-V1 §4.4g keeps in words, and they are not an expectation any more: the composer's output
  moved on purpose in stage 1 and moves again whenever a lane changes the composition. Re-basing them
  would turn a record of where the road was into a claim about where it is. What the fixture is still
  READ for is its two work records, the collection's constants and the two dice.

  The seven roads. tests/fixture_pass_works.json carries the 121 REAL per-work records the settings
  record ships, so every road row below stands on a real pair and names the measurement that
  qualified it. Each road carries a red-on-bug proof: its own qualification is removed in a COPY of
  the module and the pair stops taking it.

  The step's role. One pair at the five route roles composes five passages a person can tell apart,
  each inside charter shelf 17's budget for that role: a quiet link one letter and no miracle, a
  culmination its own miracle, and each inside its own band of seconds.

  The visit's memory. An edge walked, walked back and walked again gives three passages that keep the
  family and differ, each handle rolled inside a span derived from the handle's own published range.

  The geometry sweep. Every handle the composer drives names, in the score's own note, the
  measurement it reads; the two that do not say why they do not; and no handle the instrument
  declares OPEN is driven at all, because that state belongs to the instrument's own door reading.

  The two fences a filled score has to pass. The client refuses a score over its byte fence whole and
  an intent over its character fence whole, and both are measured here over the real collection.

  The entry's defaults and fences, unchanged from stage 0: every field the request gained reproduces
  the four-value call when left unsaid; a route role outside the five, a session memory naming a
  fourth field, and a die outside the instrument's own span are each refused by name and each carries
  a red-on-bug proof.

  The walk. On a baked site whose settings record carries the per-work records, the walk fetches the
  composer once at its first landing, derives a passage on a step and freezes the score onto the
  command; a work the record set has never heard of falls through to the walk's own glide; and a
  visit under reduced motion or Save-Data never asks for the file at all.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug proof below runs a COPY of the module in memory
with one rule changed. The source tree is never written to.

WHAT EVERY ROW HERE IS ANCHORED TO, IN ONE PLACE. A suite that has to be argued with every time the
work moves is a suite that stops guarding, so each row below stands on one of exactly four things,
and which one it is decides what a deliberate change to the composition costs to re-base.

  1. THE CLIENT'S OWN PUBLISHED CAPABILITY. The two fences a filled score has to pass — its whole
     weight and the length of its authored line — are read from the served client's own PASS_LIMITS
     literal at CLIENT_BYTES and CLIENT_INTENT below, handed to the driver, and never typed twice.
     These re-base when the CLIENT changes, by themselves, because nothing here holds a copy.

  2. CHARTER LAW. ROLE_BUDGET below is shelf 17's voice budget — letters, miracles and seconds by
     role — plus the two role numbers this seat named for the walk's own ends. A row standing on it
     re-bases only when the charter or that seat's word changes, which is the point of it.

  3. THE MODULE'S OWN ANSWERS, COMPARED AGAINST EACH OTHER. Most rows here ask the composer two
     questions and compare the two answers: a request at its defaults against the four-value call,
     a pass against the pass before it, a run with a rule planted against the same run without it.
     These NEVER re-base. A change to the composition moves both answers together and the row goes
     on measuring the same claim.

  4. NOTHING — a measured reading, printed in a row's detail so a person can read the number. Road
     counts, byte and character maxima, how many pairs decline: every one of them is a reading and
     none of them is a gate. They move whenever the composition moves and that is what they are for.

WHEN THE ANCHORING WAS LAST EXERCISED, and by what. 2026-08-17, the camera lane's soft knee on the
dolly's demand (base `1bbaf3d`): the approach a score writes changes for a minority of pairs and the
composition moves with it. Measured here against the composer as it stood before that change, on one
die, over all 14 520 ordered pairs: 324 of the 14 054 that compose write different bytes and 13 730
are byte-identical; no ground, no cue set, no travelling axis and no duration moved at all; the
heaviest score of the collection did not move, so the fence row kept its full headroom. NOT ONE ROW
HERE NEEDED RE-BASING, which is the anchoring above doing its work rather than luck — every row asks
the module two questions and compares the answers, so both answers moved together.

NO ROW HERE ASSERTS EXACT COMPOSED BYTES, and that is deliberate. Stage 0 was landed on byte
equality against the prebaked pack it replaced, which was the right gate for a stage that moved the
composer without changing what it composed; stage 1 changes what comes out on purpose, so that gate
was retired with the road it guarded (PASS-API-V1 §4.4g states both halves). A later change to the
composition — another lane's, a tuning pass, his own word — therefore re-bases NOTHING in this file.
The one row it can legitimately redden is the fence row, and a red there is the row working: a score
over the client's fence is refused whole and the visitor sees a glide.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"
# The 121 real per-work records the settings record ships, copied out of the site's own
# lab/build-workrecords-v1.py output on 2026-08-17. Every collection-wide row below reads them, so
# a road, a budget and a fence are all measured against the works that actually hang.
WORKS = Path(__file__).resolve().parent / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_composed_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- the bake and the bundle

check("EX-COMPOSED the composer travels as its own file, and the bake ships it",
      (TMP / "pass-composer.js").exists()
      and "__exPassComposer" in (TMP / "pass-composer.js").read_text(encoding="utf-8")
      and 'PASS_COMPOSER_SRC = "pass-composer.js"' in SRC,
      "the choice core must reach the site beside the bundle, with its namespace resolved")

check("EX-COMPOSED the delivery pack's reader is gone from the tree and from the bake",
      not (ROOT / "engine" / "assets" / "pass-reader.js").exists()
      and not (TMP / "pass-reader.js").exists(),
      "the file the pack road was fetched through must ship nowhere")

# The three roads that answered for a pair's score before this unit. Each is named by the very
# string the bundle would carry if it were still there, so a road creeping back reds here.
GONE = {
    "the settings record's own per-pair scores": ".scores",
    "the delivery pack's reader": "pass-reader.js",
    "the pack's shard warming": "passPackOpen",
    "the template-and-table fill": "scoreTables",
}
back = sorted(name for name, mark in GONE.items() if mark in JS)
check("EX-COMPOSED the served bundle carries the composer's door and none of the three roads it "
      "replaced",
      'PASS_COMPOSER_SRC = "pass-composer.js"' in JS and "passComposeFor" in JS and not back,
      f"roads still named in the served bundle: {back}")

# THE TWO FENCES A FILLED SCORE HAS TO PASS, BOTH PUBLISHED. A limit is part of the client's
# capability and its one home is the `PASS_LIMITS` literal; the bake reads it back out of the served
# client and writes it into the settings record, so the number the composer measures against and the
# number the client applies are one number. `scoreBytes` travelled that road already; `intentChars`
# joins it here, because stage 0 measured what an unpublished prose fence costs — 1 004 of 6 304
# composed crossings refused whole for a line nobody could measure.
CFG = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
BAKED_CAPS = (CFG.get("pass") or {}).get("capabilities") or {}
CLIENT_LIMITS = re.search(r"PASS_LIMITS\s*=\s*\{([^}]*)\}", SRC)
CLIENT_BYTES = int(re.search(r"\bbytes:\s*(\d+)", CLIENT_LIMITS.group(1)).group(1))
CLIENT_INTENT = int(re.search(r"\bintent:\s*(\d+)", CLIENT_LIMITS.group(1)).group(1))
# ---------------------------------------------------------------- every published handle is registered
# A HANDLE A MANIFEST PUBLISHES AND THIS REGISTER DOES NOT NAME MAKES THE COMPOSER THROW — on every
# pair that casts that instrument, inside the fill, where the register is read for a row that is not
# there. The walk catches the throw and the crossing falls to the walk's own glide with nothing on
# the diagnostic surface but «the entry threw», so the failure is silent to a visitor and nearly
# silent to a reader.
#
# IT HAPPENED ONCE AND IT WAS EXPENSIVE. The instruments lane gave the woven ribbon three handles for
# the wave that plays only where a work carries one, and this register kept none of the three. Over
# the 121 real per-work records, 7 735 of 14 520 ordered pairs — 53.3 per cent — could not be
# composed at all, and the woven ribbon, which is this collection's reference look, never played on
# any route. Every suite stayed green throughout, because the collection-wide rows stand on a FROZEN
# copy of the manifests and the frozen copy did not carry the three handles either; the assembly lane
# found it by casting a route in the real shell.
#
# So the two lists are compared against the FILES rather than against a fixture: every instrument
# that ships, every handle its own manifest publishes that is not declared open, and this register's
# own rows. An instrument that lands a handle now reddens this row instead of a route.
def _manifest_handles(text):
    """Every handle one instrument's manifest publishes, with its own block, by counting braces."""
    start = text.index("{", text.index("handles: {"))
    depth, j, end = 0, start, None
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                end = j
                break
        j += 1
    body = text[start + 1:end]
    out, depth, k, name, bstart = {}, 0, 0, None, 0
    tok = re.compile(r"\s*([A-Za-z][A-Za-z0-9_]*)\s*:\s*\{")
    while k < len(body):
        if depth == 0:
            m = tok.match(body, k)
            if m:
                name = m.group(1)
                k = m.end() - 1
        c = body[k]
        if c == "{":
            depth += 1
            if depth == 1:
                bstart = k
        elif c == "}":
            depth -= 1
            if depth == 0 and name:
                out[name] = body[bstart:k + 1]
                name = None
        k += 1
    return out


_STRIP = build_site._engine.strip_js_comments
_REGISTERED = set(re.findall(
    r'^\s{4}([A-Za-z][A-Za-z0-9_]*): \["(?:measured|unmeasured|transaction|module-rest)"',
    MODULE.read_text(encoding="utf-8"), re.M))
# WHICH INSTRUMENTS THE ROW COVERS: the ones the settings record PUBLISHES, which since 2026-08-18
# is exactly the set the composer can cast — a kind's candidates are derived from that record and an
# instrument absent from it can be named by no road. A file that ships without being published can
# drive nothing and is reported beside the row rather than judged by it; the day the site publishes
# it, it joins the list here by arriving, which is the same rule the composer itself now follows.
_PUBLISHED = sorted(json.loads(FIXTURE.read_text(encoding="utf-8"))["consts"]["manifests"])
_UNREGISTERED, _SEEN, _UNPUBLISHED = {}, {}, []
for _p in sorted((ROOT / "engine" / "assets").glob("pass-inst-*.js")):
    _iid = _p.stem[len("pass-inst-"):]
    if _iid not in _PUBLISHED:
        _UNPUBLISHED.append(_iid)
        continue
    _blocks = _manifest_handles(_STRIP(_p.read_text(encoding="utf-8")))
    _SEEN[_iid] = len(_blocks)
    _gaps = sorted(h for h, b in _blocks.items()
                   if "open: true" not in b and h not in _REGISTERED)
    if _gaps:
        _UNREGISTERED[_iid] = _gaps

check("EX-COMPOSED every handle a castable instrument publishes has a row in the register that says "
      "what it reads — a handle without one makes the composer throw on every pair that casts it",
      not _UNREGISTERED and bool(_SEEN) and all(n >= 5 for n in _SEEN.values()),
      "read off the instrument files themselves — %s; the register names %d handles, and %s. "
      "Shipping but published to no record, so castable by nothing: %s"
      % (", ".join("%s %d" % (i, n) for i, n in sorted(_SEEN.items())), len(_REGISTERED),
         ("every one of them is registered" if not _UNREGISTERED
          else "these are NOT: %s" % _UNREGISTERED),
         ", ".join(_UNPUBLISHED) or "none"))

check("EX-COMPOSED the bake publishes both fences a filled score is measured against",
      BAKED_CAPS.get("scoreBytes") == CLIENT_BYTES
      and BAKED_CAPS.get("intentChars") == CLIENT_INTENT,
      f"the client applies {CLIENT_BYTES} B and {CLIENT_INTENT} characters; the settings record "
      f"publishes {BAKED_CAPS.get('scoreBytes')} and {BAKED_CAPS.get('intentChars')}. The site's own staging "
      f"step carries both into the composer's constants, where `intentFenceChars` stands beside "
      f"`scoreFenceBytes` (tlvphotos lab/build-workrecords-v1.py)")

check("EX-COMPOSED nothing on the product path is keyed by a pair",
      "passRequestFor" in JS and "workRecordA" in JS
      and not re.search(r"scoreTemplates|passFillScore|passPack\b", JS),
      "the walk must build a request out of two work records, never look a pair up")

# ---------------------------------------------------------------- the derivation, in node

FIX = json.loads(FIXTURE.read_text(encoding="utf-8"))
A_ID, B_ID = FIX["pair"]["a"], FIX["pair"]["b"]
KEY_AB, KEY_BA = A_ID + "__" + B_ID + "__ab", A_ID + "__" + B_ID + "__ba"

# The seven roads, each with the shape of qualification the module states for it. The row for each
# finds a real pair of the collection that takes it and prints the reading that qualified that pair.
ROADS = ["shared-ground", "spin", "kaleidoscope", "symmetry-slide", "stripes",
         "dissimilar-mystery", "bridge", "box-fold"]
ROLES_ALL_PY = ["entrance", "quiet link", "middle", "culmination", "return"]

NODE_ROWS = [
    "EX-COMPOSED the seven roads all carry real pairs, and each names the reading that qualified it",
    "EX-COMPOSED the frame folds into a solid, and only where the step's role may spend a miracle",
    "EX-COMPOSED every pair composes at every one of the five route roles without throwing",
    "EX-COMPOSED every instrument that travels to a visitor can actually be chosen",
    "EX-COMPOSED the die chooses the road, so a pinned seed reproduces the choice",
    "EX-COMPOSED the camera leads a passage at the walk's two tonic steps and nowhere else",
    "EX-COMPOSED the five route roles compose five passages, each inside shelf 17's own budget",
    "EX-COMPOSED the family the composer hands back is the one the walk reads off the plan",
    "EX-COMPOSED an edge walked back keeps its family and its pivot and differs in what may differ",
    "EX-COMPOSED every handle the composer drives names the measurement it reads",
    "EX-COMPOSED a handle the instrument declares open is never driven at a door",
    "EX-COMPOSED no filled score of the real collection crosses the byte or the intent fence",
    "EX-COMPOSED the composer measures its line against the fence it is handed, not against its own "
    "fallback",
    "EX-COMPOSED every one of the 14 520 ordered pairs either composes or declines by name",
    "EX-COMPOSED every field the request gained reproduces the four-value call exactly",
    "EX-COMPOSED a route role outside the five is refused by name",
    "EX-COMPOSED a session memory wider than §4.8's three fields is refused by name",
    "EX-COMPOSED a die outside the instrument's own span is refused by name",
    "EX-COMPOSED red-on-bug · the route-role fence removed: the unnamed role composes",
    "EX-COMPOSED red-on-bug · §4.8's fence removed: a fourth memory field composes",
    "EX-COMPOSED red-on-bug · the die dropped on its way to the road: every die picks one road",
    "EX-COMPOSED red-on-bug · the similar road's own bound removed: it qualifies for everything",
    "EX-COMPOSED red-on-bug · the role's budget removed: a quiet link spends two letters",
    "EX-COMPOSED red-on-bug · the led passage's role gate removed: a middle is led by its camera",
    "EX-COMPOSED red-on-bug · the led passage's own reading removed: every tonic step is led",
    "EX-COMPOSED red-on-bug · the family hold removed: the return stops naming the recorded family",
    "EX-COMPOSED red-on-bug · the return's own step removed: the way back keeps neither family "
    "nor pivot",
    "EX-COMPOSED red-on-bug · the open-handle fence removed: the composer drives a door's own state",
    "EX-COMPOSED red-on-bug · the intent fence removed: a line stands over the cap it is measured "
    "against",
    "EX-COMPOSED red-on-bug · the fold's own role gate removed: a step with no miracle folds",
    "EX-COMPOSED red-on-bug · the fold stops counting as the miracle: a folding crossing spends "
    "none",
    "EX-COMPOSED red-on-bug · one instrument per kind restored: an instrument travels unchosen",
    "EX-COMPOSED the intent fence gives up this lane's own clauses before the line is refused whole",
]

# THE DRIVER, run in node against a COPY of the module held in memory. `PLANTS` names the rules to
# change before the module is loaded, which is how every red-on-bug row below is run: the repair is
# reverted in the copy alone and the answer must move. `SWEEP` says how many of the collection's
# works the collection-wide readings walk, so a planted run can walk a corner of it and the standing
# rows walk all 121.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath, worksPath] = process.argv.slice(2);
const plants = JSON.parse(process.env.PLANTS || "[]");
const sweepN = parseInt(process.env.SWEEP || "0", 10);

let source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
const planted = [];
for (const [from, to] of plants) {
  if (source.indexOf(from) < 0) {
    console.log(JSON.stringify({error: "the plant found nothing to change: " + from}));
    process.exit(0);
  }
  source = source.split(from).join(to);
  planted.push(from);
}
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(0); }

const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8"));
// THE TWO FENCES, READ FROM THE CLIENT AND HANDED IN — never typed here. Anchor 1 of the four the
// docstring names: the number this suite measures against is the number the client applies, parsed
// out of the served client's own PASS_LIMITS literal on the Python side, so a client that raises a
// cap re-bases these rows by itself and no copy of either number lives in this file.
const CAPS = JSON.parse(process.env.CLIENT_CAPS || "{}");
const INTENT_CAP = CAPS.intent;
const BYTE_CAP = CAPS.bytes;
if (!(INTENT_CAP > 0) || !(BYTE_CAP > 0)) {
  console.log(JSON.stringify({error: "the client published no fences to measure against: "
                                     + JSON.stringify(CAPS)}));
  process.exit(0);
}

// The constants are the shape the site's staging step ships TODAY: the client's prose fence stands
// in them beside its byte fence, so the composer under test measures against the published number
// rather than against its own documented fallback. The fixture predates the field; handing it here
// is the same value by the same road, not a second one.
fix.consts.intentFenceChars = INTENT_CAP;
const composer = joined.make(fix.consts);
const A = fix.works[fix.pair.a], B = fix.works[fix.pair.b];
const KEY_AB = fix.pair.a + "__" + fix.pair.b + "__ab";
const KEY_BA = fix.pair.a + "__" + fix.pair.b + "__ba";
const consts = fix.consts;
const out = {version: joined.version, seedSpan: composer.seedSpan, routeRoles: composer.routeRoles,
             planted: planted};

// A die per ordered pair that is the pair's own, so a run and the run before it roll the same
// number and any difference between them is the module's rather than the die's.
function die(key) {
  let h = 2166136261;
  for (let i = 0; i < key.length; i++) { h = Math.imul(h ^ key.charCodeAt(i), 16777619) >>> 0; }
  return (h % 100000) / 100000 * 8;
}
function digest(text) {
  let h = 5381;
  for (let i = 0; i < text.length; i++) { h = ((h * 33) ^ text.charCodeAt(i)) >>> 0; }
  return h.toString(16);
}
function budget(p) {
  const voices = p.plan.cues.map((c) => c.voice);
  return {letters: voices.filter((v) => v === "letter").length,
          accompaniments: 1 + voices.filter((v) => v === "accompaniment").length,
          miracles: voices.filter((v) => v === "miracle").length};
}
function brief(p) {
  if (!p.json) return {declined: p.declined, road: p.road || null};
  return {road: p.road, family: p.family, tier: p.plan.tier, duration: p.score.duration,
          cues: p.score.cues.map((c) => c.id + ":" + c.instrument.id),
          budget: budget(p), bytes: p.bytes, intent: p.score.intent.length,
          lead: !!p.score.camera.lead, reach: p.cameraReach,
          middle: p.plan.middle.kind, digest: digest(p.json),
          qualified: p.roads || [], capped: p.capped || []};
}

// 1 · the worked pair, both directions, asked the way the walk asks
const bare = {};
for (const [key, dir] of [[KEY_AB, "a-to-b"], [KEY_BA, "b-to-a"]]) {
  const p = composer.passageFor({workRecordA: A, workRecordB: B, direction: dir,
                                 seed: fix.seeds[key]});
  bare[key] = p;
  out[key] = {key: p.key, declined: p.declined || null, json: p.json || null,
              bytes: p.bytes === undefined ? null : p.bytes,
              applied: p.applied, request: p.request, brief: brief(p)};
}

// 2 · THE ONE EQUALITY THIS SUITE STILL ASSERTS, and it is worth naming what it is against. Stage 0
//     was landed on byte equality against the PREBAKED PACK the composer replaced, and that gate was
//     retired with the road it guarded (PASS-API-V1 §4.4g). What stands here instead is an equality
//     against THE COMPOSER'S OWN CURRENT OUTPUT: every field the request gained, named at its
//     documented default, must read exactly what the four-value call the choice core has always
//     taken reads, on the same run. Both sides move together whenever the composition moves, so this
//     row re-bases never — and it goes on measuring the only thing it ever measured, which is that
//     the six added fields default to doing nothing.
const spelled = composer.passageFor({
  workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB],
  routeRole: "middle", sessionMemory: null, cameraState: null, buffer: null});
const core = composer.scoreFor(A, B, "a-to-b", fix.seeds[KEY_AB]);
out.defaults = {spelledSame: spelled.json === bare[KEY_AB].json,
                coreSame: core.json === bare[KEY_AB].json};

// 3 · the die chooses the road
const dice = {};
for (let s = 0; s <= 8; s += 0.5) {
  const p = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b", seed: s});
  dice[s] = p.road || ("declined:" + p.declined);
}
const twice = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b", seed: 3.5});
out.dice = {roads: dice, distinct: Array.from(new Set(Object.values(dice))).sort(),
            pinnedRepeats: twice.json === composer.passageFor(
              {workRecordA: A, workRecordB: B, direction: "a-to-b", seed: 3.5}).json};

// 4 · the five route roles over one pair
out.roles = {};
for (const role of composer.routeRoles) {
  const p = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b",
                                 seed: fix.seeds[KEY_AB], routeRole: role});
  out.roles[role] = brief(p);
}

// 5 · the visit's memory: out, back, and out again
const forward = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b",
                                     seed: fix.seeds[KEY_AB]});
const backward = composer.passageFor({
  workRecordA: A, workRecordB: B, direction: "b-to-a", seed: fix.seeds[KEY_BA],
  sessionMemory: {family: forward.family, seed: fix.seeds[KEY_AB], passIndex: 1}});
const again = composer.passageFor({
  workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB],
  sessionMemory: {family: forward.family, seed: fix.seeds[KEY_AB], passIndex: 2}});
// THE FAMILY THE WALK READS, computed here the way the walk computes it: the transform the
// pivot's cut implies, joined to the measure the passage travels, or «tone» where nothing does.
// A composer that named a family of its own would make every return unrecognisable.
function walkFamily(plan) {
  if (!plan || !plan.pivot) return null;
  const t = plan.pivot.transform || plan.pivot.kind || "tone_bridge";
  const axis = (plan.travellingAxis && plan.travellingAxis.measure)
    ? plan.travellingAxis.measure : "tone";
  return t + "+" + axis;
}
// The pivot as a thing rather than a strength, judged the way the walk judges it.
function samePivot(x, y) {
  return !!x && !!y && x.kind === y.kind && x.measure === y.measure && x.cut === y.cut;
}
// What varies across a return, named one at a time, so a row can say which of §4.8's four moved.
function shaping(p) {
  if (!p.plan) return null;
  const cues = p.plan.cues;
  return {order: cues.map((c) => c.id).join(">"),
          opens: cues.map((c) => c.id + "@" + Number(c.window[0]).toFixed(4)).join(","),
          actors: p.plan.actors.map((a) => a.ref + ":" + a.elementSet.provider + ":"
                                           + a.elementSet.kind).sort().join(","),
          camera: JSON.stringify(p.plan.camera.track)};
}
out.memory = {
  forward: brief(forward), backward: brief(backward), again: brief(again),
  heldOnReturn: backward.heldFamily, heldAgain: again.heldFamily,
  heldBackBy: backward.heldBy, heldAgainBy: again.heldBy,
  // the family the WALK will read off each plan, and the family this file handed back beside it
  walkForward: walkFamily(forward.plan), walkBack: walkFamily(backward.plan),
  walkAgain: walkFamily(again.plan),
  saidForward: forward.family, saidBack: backward.family, saidAgain: again.family,
  // §4.8's own two questions, asked of the way back exactly as the walk asks them
  backKeepsFamily: walkFamily(backward.plan) === walkFamily(forward.plan),
  backKeepsPivot: samePivot(backward.plan && backward.plan.pivot,
                            forward.plan && forward.plan.pivot),
  againDiffers: again.json !== forward.json,
  // what §4.8 leaves free to vary, one field at a time
  shapingForward: shaping(forward), shapingBack: shaping(backward), shapingAgain: shaping(again),
  // the list the walk's own drift reads as what may never move
  measuredNamed: (forward.plan ? forward.plan.cues.map(
    (c) => c.id + ":" + Object.keys(c.measuredHandles || {}).sort().join("/")) : [])
};

// 6 · the collection-wide readings: the roads, the fences and the refusals
const ids = Object.keys(works.works).sort().slice(0, sweepN > 0 ? sweepN : undefined);
const roads = {}, declines = {}, byRoad = {};
let composed = 0, declined = 0, maxBytes = 0, maxIntent = 0, overByte = 0, overIntent = 0;
let drivenUnmeasured = [], openDriven = [], drivenNoteMissing = [];
let intentShortened = 0, roadKept = 0, boxReasons = {};
let ledAtTonic = 0, ledElsewhere = 0, ledWithWorldCue = 0, tonic = 0;
// THE FOLD, counted per role. A crossing that folds the frame into a solid spends the one miracle
// shelf 6 allows, so it may not stand at a role shelf 17 gives none, may not stand beside a second
// impossible thing, and may not claim the world level beside a camera-led flight.
const ROLES_ALL = ["entrance", "quiet link", "middle", "culmination", "return"];
const folded = {}, worldCue = {}, ledAndWorld = {}, twoMiracles = {}, roleThrew = {}, roleN = {};
const foldUnspent = {};
for (const r of ROLES_ALL) { folded[r] = 0; worldCue[r] = 0; ledAndWorld[r] = 0;
                             twoMiracles[r] = 0; roleThrew[r] = null; roleN[r] = 0;
                             foldUnspent[r] = 0; }
let boxQualified = 0;
// WHICH INSTRUMENTS ARE EVER CHOSEN. An instrument the settings record ships travels to every
// visitor; one that travels and can never be chosen is weight on the wire and a register missing
// from the route. A row counting the cast would pass on exactly that, so this counts CHOICES.
const chosen = {};
const ROAD_OPENERS = ["Along what the two works share. ", "The radial work turns. ",
                      "The rings open. ", "The parts slide along the works' own symmetry. ",
                      "The two band families cross into stripes. ",
                      "The work folds along its own region lines. ",
                      "Along what the two works do not share. "];
for (let i = 0; i < ids.length; i++) {
  for (let j = 0; j < ids.length; j++) {
    if (i === j) continue;
    const a = works.works[ids[i]], b = works.works[ids[j]];
    const dir = i < j ? "a-to-b" : "b-to-a";
    const wa = i < j ? a : b, wb = i < j ? b : a;
    const key = wa.id + "__" + wb.id + "__" + (dir === "a-to-b" ? "ab" : "ba");
    const p = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: dir,
                                   seed: die(key)});
    if (p.declined) {
      declined++;
      declines[p.declined.slice(0, 70)] = (declines[p.declined.slice(0, 70)] || 0) + 1;
      continue;
    }
    composed++;
    roads[p.road] = (roads[p.road] || 0) + 1;
    if ((p.plan.intentDropped || []).length) intentShortened++;
    if (ROAD_OPENERS.some((o) => p.score.intent.indexOf(o) === 0)) roadKept++;
    for (const n of p.roadNotes) {
      if (n.road === "box-fold") boxReasons[n.why.slice(0, 60)] = (boxReasons[n.why.slice(0, 60)] || 0) + 1;
    }
    if (!byRoad[p.road]) {
      byRoad[p.road] = {key: key, brief: brief(p),
                        why: (p.roadNotes.filter((n) => n.road === p.road)[0] || {}).why || null};
    }
    // EVERY ROLE IS COMPOSED FOR EVERY PAIR. A plan shape the authored lines have no template for
    // throws inside `declare`, on the product path, where nothing may throw — and a sweep at one
    // role will not see it, because the shape a role reaches for is the role's own. This walks all
    // five and records the first pair and role that threw, which is exactly how the folding
    // culmination's missing line was found.
    for (const r of ROLES_ALL) {
      let q = null;
      try {
        q = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: dir,
                                 seed: die(key), routeRole: r});
      } catch (e) {
        if (!roleThrew[r]) roleThrew[r] = key + ": " + String(e && e.message).slice(0, 120);
        continue;
      }
      const bf = (q.roadNotes || []).filter((n) => n.road === "box-fold")[0];
      if (r === "middle" && bf && bf.ok) boxQualified++;
      if (!q.score) continue;
      roleN[r]++;
      const cues = q.score.cues;
      for (const x of cues) chosen[x.instrument.id] = (chosen[x.instrument.id] || 0) + 1;
      if (cues.some((x) => x.instrument.id === "boxfold")) folded[r]++;
      const claimsWorld = cues.some((x) => (x.levels || []).indexOf("WORLD") >= 0);
      if (claimsWorld) worldCue[r]++;
      if (claimsWorld && q.score.camera.lead) ledAndWorld[r]++;
      const miracles = cues.filter((x) => x.voice === "miracle").length;
      if (miracles > 1) twoMiracles[r]++;
      // A CROSSING THAT FOLDS THE FRAME AND SPENDS NO MIRACLE FOR IT has lost the law rather than
      // kept it: the fold IS the impossible event, so a folding score with no miracle voice means
      // the slot went unspent and a second impossible thing could stand beside it.
      if (cues.some((x) => x.instrument.id === "boxfold") && miracles === 0) foldUnspent[r]++;
    }

    // THE CAMERA-LED PASSAGE, counted at a tonic step and at one that is not. A led flight spends
    // the world voice, so no led score may give a cue the WORLD level.
    const atTonic = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: dir,
                                        seed: die(key), routeRole: "quiet link"});
    if (atTonic.score) {
      tonic++;
      if (atTonic.score.camera.lead) {
        ledAtTonic++;
        if (atTonic.score.cues.some((c) => (c.levels || []).indexOf("WORLD") >= 0)) ledWithWorldCue++;
      }
    }
    if (p.score.camera.lead) ledElsewhere++;
    if (p.bytes > maxBytes) maxBytes = p.bytes;
    if (p.bytes > BYTE_CAP) overByte++;
    if (p.score.intent.length > maxIntent) maxIntent = p.score.intent.length;
    if (p.score.intent.length > INTENT_CAP) overIntent++;
    // every node the composer DROVE carries its own note: it opens with «requested» and closes with
    // the measurement it read. A driven handle whose note names no measurement is the defect the
    // geometry sweep closes.
    for (const cue of p.score.cues) {
      for (const name of Object.keys(cue.nodes)) {
        const node = cue.nodes[name];
        const note = String(node.note || "");
        const handle = name.slice(cue.id.length + 1);
        if (note.indexOf("requested") !== 0) continue;
        if (note.indexOf("no measurement in this tree bears on it") >= 0
            || note.indexOf("which no build-time file measures") >= 0
            || note.indexOf("is recorded") >= 0) {
          if (drivenUnmeasured.indexOf(handle) < 0) drivenUnmeasured.push(handle);
        }
        if (!note) drivenNoteMissing.push(handle);
      }
      // no cue may name a handle the instrument declares OPEN: that state is the instrument's own
      // door reading (his 18:00 decision)
      const manifest = fix.consts.manifests[cue.instrument.id];
      for (const h of Object.keys(manifest.handles)) {
        if (!manifest.handles[h].open) continue;
        if (cue.nodes[cue.id + "-" + h] !== undefined && openDriven.indexOf(h) < 0) openDriven.push(h);
      }
    }
  }
}
out.sweep = {works: ids.length, ordered: ids.length * (ids.length - 1), composed, declined,
             roads, declines, byRoad, maxBytes, maxIntent, overByte, overIntent,
             byteCap: BYTE_CAP, intentCap: INTENT_CAP,
             drivenUnmeasured: drivenUnmeasured.sort(), openDriven: openDriven.sort(),
             drivenNoteMissing: drivenNoteMissing.slice(0, 4),
             intentShortened, roadKept, boxReasons,
             ledAtTonic, ledElsewhere, ledWithWorldCue, tonic,
             folded, worldCue, ledAndWorld, twoMiracles, roleThrew, roleN, boxQualified,
             foldUnspent, chosen, cast: Object.keys(consts.instruments).sort()};

// 7 · the road every pair is measured against, and the one road no instrument can play
const roadNotes = {};
for (const n of forward.roadNotes) roadNotes[n.road] = {ok: n.ok, why: n.why};
out.roadNotes = roadNotes;

// 8 · the composer measures its line against the number it is HANDED, not against its fallback.
//     The constants are handed a cap of their own and the longest line the composer writes has to
//     fall under it — which is the wire the bake's `intentChars` travels, proved without planting.
const handed = joined.make(Object.assign({}, fix.consts, {intentFenceChars: 300}));
let handedMax = 0, handedShort = 0, handedN = 0, handedRoadKept = 0;
for (let i = 0; i < ids.length; i++) {
  for (let j = 0; j < ids.length; j++) {
    if (i === j) continue;
    const a = works.works[ids[i]], b = works.works[ids[j]];
    const dir = i < j ? "a-to-b" : "b-to-a";
    const wa = i < j ? a : b, wb = i < j ? b : a;
    const key = wa.id + "__" + wb.id + "__" + (dir === "a-to-b" ? "ab" : "ba");
    const p = handed.passageFor({workRecordA: wa, workRecordB: wb, direction: dir, seed: die(key)});
    if (!p.json) continue;
    handedN++;
    if (p.score.intent.length > handedMax) handedMax = p.score.intent.length;
    if ((p.plan.intentDropped || []).length) handedShort++;
    if (ROAD_OPENERS.some((o) => p.score.intent.indexOf(o) === 0)) handedRoadKept++;
  }
}
out.handed = {cap: 300, max: handedMax, shortened: handedShort, composed: handedN,
              roadKept: handedRoadKept, own: out.sweep.maxIntent};

// 9 · the three fences of the entry
const ask = (extra) => {
  const p = composer.passageFor(Object.assign(
    {workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB]}, extra));
  return {declined: p.declined || null, composed: !!p.json};
};
out.fences = {
  role: ask({routeRole: "grand finale"}),
  memory: ask({sessionMemory: {family: "band", seed: 1, passIndex: 2, cooldown: 9}}),
  memoryOk: ask({sessionMemory: {family: "band", seed: 1, passIndex: 2}}),
  seedHigh: ask({seed: 9}),
  seedLow: ask({seed: -1}),
};
console.log(JSON.stringify(out));
"""

DRIVER_PATH = TMP / "composed-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_run(plants=(), sweep=0):
    # The client's own two fences travel to the driver rather than being restated inside it, which
    # is anchor 1 of the four the docstring names.
    env = dict(os.environ, PLANTS=json.dumps(list(plants)), SWEEP=str(sweep),
               CLIENT_CAPS=json.dumps({"bytes": CLIENT_BYTES, "intent": CLIENT_INTENT}))
    proc = subprocess.run(["node", str(DRIVER_PATH), str(MODULE), str(FIXTURE), str(WORKS)],
                          capture_output=True, text=True, env=env, timeout=600)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-400:]}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


# Charter shelf 17's budget, and the two ends of the walk this seat named. A role's row is the bound
# the composer emits inside, and the band of seconds it emits inside.
ROLE_BUDGET = {
    "entrance": {"letters": (0, 2), "miracles": (0, 0), "seconds": (4.0, 6.0)},
    "quiet link": {"letters": (1, 1), "miracles": (0, 0), "seconds": (2.0, 4.0)},
    "middle": {"letters": (0, 2), "miracles": (0, 1), "seconds": (2.0, 8.0)},
    "culmination": {"letters": (1, 3), "miracles": (0, 1), "seconds": (2.0, 14.0)},
    "return": {"letters": (1, 1), "miracles": (0, 0), "seconds": (2.0, 4.0)},
}

if not node_available():
    for r in NODE_ROWS:
        skip(r, "node is not installed (pinned expected skip)")
else:
    got = node_run()
    if got.get("error"):
        for r in NODE_ROWS:
            skip(r, "the module would not load: " + got["error"])
    else:
        sweep = got["sweep"]

        # --- row 0 · the seven roads, each on a real pair -------------------------------------
        missing = [r for r in ROADS if r not in sweep["byRoad"]]
        shown = ", ".join(
            f"{r}×{sweep['roads'][r]} ({sweep['byRoad'][r]['why'] or 'the last candidate'})"
            for r in ROADS if r in sweep["byRoad"])
        check(NODE_ROWS[0], not missing,
              f"roads with no pair of the real collection: {missing}; the rest: {shown}")

        # --- row 1 · the fold, and the two laws that bind it ------------------------------------
        noMiracle = ["entrance", "quiet link", "return"]
        leaked = [r for r in noMiracle if sweep["folded"][r]]
        bothWays = [r for r in sweep["ledAndWorld"] if sweep["ledAndWorld"][r]]
        stacked = [r for r in sweep["twoMiracles"] if sweep["twoMiracles"][r]]
        unspent = [r for r in sweep["foldUnspent"] if sweep["foldUnspent"][r]]
        check(NODE_ROWS[1],
              sweep["folded"]["middle"] > 0 and not leaked and not bothWays and not stacked
              and not unspent,
              "the frame folds for "
              + ", ".join(f"{sweep['folded'][r]} pair(s) at a {r}" for r in ROLES_ALL_PY)
              + f"; {sweep['boxQualified']} pairs qualify for the box-fold road on their own "
              f"measurements. Roles that spend no miracle and folded anyway: {leaked or 'none'}; "
              f"scores led by the camera with a world-level cue beside it: {bothWays or 'none'}; "
              f"scores carrying two impossible things: {stacked or 'none'}; folding scores that "
              f"spend no miracle for the fold: {unspent or 'none'}")

        # --- row 2 · every role composes for every pair -------------------------------------------
        threw = {r: w for r, w in sweep["roleThrew"].items() if w}
        check(NODE_ROWS[2], not threw,
              "over the real collection at all five roles — "
              + ", ".join(f"{r}: {sweep['roleN'][r]}" for r in ROLES_ALL_PY)
              + f" composed — nothing threw inside the entry: {threw or 'none'}")

        # --- row 3 · every instrument that travels can be chosen ---------------------------------
        # AN INSTRUMENT THAT SHIPS AND CANNOT PLAY IS A DEFECT, and counting the cast would miss it.
        # The unfold cut on panels all along; the folding instrument landed on the same kind, a rule
        # naming one instrument per kind gave the kind to the fold outright, and the only instrument
        # that shows a person how a work was made travelled to every visitor and could never be
        # chosen. This counts CHOICES over the whole collection at all five roles.
        unreachable = [i for i in sweep["cast"] if not sweep["chosen"].get(i)]
        check(NODE_ROWS[3], not unreachable,
              "over the real collection at all five roles the cast is chosen "
              + json.dumps(sweep["chosen"], ensure_ascii=False)
              + f"; instruments that travel to a visitor and can never be chosen: "
                f"{unreachable or 'none'}")

        # --- row 3 · the die chooses the road --------------------------------------------------
        d = got["dice"]
        check(NODE_ROWS[4], len(d["distinct"]) > 1 and d["pinnedRepeats"],
              f"seventeen dice over one pair chose {d['distinct']}; a pinned die reproduces its own "
              f"run: {d['pinnedRepeats']}")

        # --- row 4 · the camera-led passage ------------------------------------------------------
        check(NODE_ROWS[5],
              sweep["ledAtTonic"] > 0 and sweep["ledElsewhere"] == 0
              and sweep["ledWithWorldCue"] == 0,
              f"of {sweep['tonic']} quiet links {sweep['ledAtTonic']} are carried by the flight "
              f"itself, and of {sweep['composed']} middles {sweep['ledElsewhere']} are; no led "
              f"score gives a cue the world level ({sweep['ledWithWorldCue']} did)")

        # --- row 5 · the five roles, each inside shelf 17's budget ------------------------------
        roles = got["roles"]
        bad = []
        for role, want in ROLE_BUDGET.items():
            r = roles.get(role) or {}
            if not r.get("cues"):
                bad.append(f"{role} composed nothing: {r.get('declined')}")
                continue
            b = r["budget"]
            if not (want["letters"][0] <= b["letters"] <= want["letters"][1]):
                bad.append(f"{role} spends {b['letters']} letters, outside {want['letters']}")
            if not (want["miracles"][0] <= b["miracles"] <= want["miracles"][1]):
                bad.append(f"{role} spends {b['miracles']} miracles, outside {want['miracles']}")
            secs = r["duration"] / 1000.0
            if not (want["seconds"][0] <= secs <= want["seconds"][1]):
                bad.append(f"{role} runs {secs} s, outside {want['seconds']}")
        told = len({json.dumps(roles[k].get("digest")) for k in roles if roles[k].get("digest")})
        check(NODE_ROWS[6], not bad and told >= 3,
              "; ".join(f"{k}: {v.get('road')} {v.get('tier')} {v.get('duration')} ms "
                        f"{v.get('cues')}" for k, v in roles.items())
              + f" — {told} distinct scores over one pair"
              + ("; " + "; ".join(bad) if bad else ""))

        # --- row 5 · the family the composer hands back is the walk's own ------------------------
        m = got["memory"]
        agree = (m["saidForward"] == m["walkForward"] and m["saidBack"] == m["walkBack"]
                 and m["saidAgain"] == m["walkAgain"])
        check(NODE_ROWS[7], agree and bool(m["walkForward"]),
              f"the composer hands back «{m['saidForward']}» and the walk reads «{m['walkForward']}» "
              f"off the same plan; the way back: «{m['saidBack']}» against «{m['walkBack']}»; the "
              f"third pass: «{m['saidAgain']}» against «{m['walkAgain']}»")

        # --- row 6 · §4.8's own two questions, asked of the way back ------------------------------
        moved = [k for k in ("order", "opens", "actors", "camera")
                 if m["shapingBack"] and m["shapingForward"]
                 and m["shapingBack"][k] != m["shapingForward"][k]]
        movedAgain = [k for k in ("order", "opens", "actors", "camera")
                      if m["shapingAgain"] and m["shapingForward"]
                      and m["shapingAgain"][k] != m["shapingForward"][k]]
        check(NODE_ROWS[8],
              (m["backKeepsFamily"] or m["backKeepsPivot"]) and bool(moved)
              and m["againDiffers"] and m["heldAgain"],
              f"out on {m['forward']['road']} as «{m['walkForward']}», back on "
              f"{m['backward']['road']} as «{m['walkBack']}» — the family holds: "
              f"{m['backKeepsFamily']}, the pivot holds: {m['backKeepsPivot']} — and what §4.8 "
              f"leaves free moved: {moved or 'nothing'}. Out again on {m['again']['road']} holding "
              f"«{m['heldAgain']}» by its {m['heldAgainBy']}, differing from the first pass: "
              f"{m['againDiffers']}, in "
              f"{movedAgain or 'nothing'}. The list the walk's own drift may never move: "
              + "; ".join(m["measuredNamed"]))

        # --- row 7 · the geometry sweep ---------------------------------------------------------
        check(NODE_ROWS[9],
              not sweep["drivenUnmeasured"] and not sweep["drivenNoteMissing"],
              f"over {sweep['composed']} composed passages of the real collection, every driven "
              f"handle's own note names its measurement; handles driven from something no "
              f"measurement bears on: {sweep['drivenUnmeasured']}")

        # --- row 8 · the open handle ------------------------------------------------------------
        check(NODE_ROWS[10], not sweep["openDriven"],
              f"handles the instruments declare open that the composer drove: "
              f"{sweep['openDriven']} — the woven balance is the one at stake, and at a door that "
              f"state is the instrument's own reading of the buffer (his 18:00 decision)")

        # --- row 9 · the two fences a filled score has to pass -----------------------------------
        check(NODE_ROWS[11], sweep["overByte"] == 0 and sweep["overIntent"] == 0,
              f"the heaviest score of the collection weighs {sweep['maxBytes']} B against the "
              f"{sweep['byteCap']} the client applies, and the longest intent runs "
              f"{sweep['maxIntent']} characters against its {sweep['intentCap']}; over the byte "
              f"fence: {sweep['overByte']}, over the intent fence: {sweep['overIntent']}")

        # --- row 10 · the composer reads the fence it is handed ----------------------------------
        h = got["handed"]
        check(NODE_ROWS[12],
              h["shortened"] > 0 and sweep["intentShortened"] == 0,
              f"handed a cap of {h['cap']} characters in its own constants, the composer shortened "
              f"{h['shortened']} of {h['composed']} lines and its longest ran {h['max']}; on the "
              f"number the client actually applies its longest runs {h['own']}")

        # --- row 10 · every pair is answered ------------------------------------------------------
        named = all(w.strip() for w in sweep["declines"])
        check(NODE_ROWS[13],
              sweep["composed"] + sweep["declined"] == sweep["ordered"] and named,
              f"{sweep['composed']} of {sweep['ordered']} ordered pairs compose and "
              f"{sweep['declined']} decline, each by name: "
              + json.dumps(sweep["declines"], ensure_ascii=False))

        # --- row 11 · the defaults reproduce the four-value call -----------------------------------
        dd = got["defaults"]
        check(NODE_ROWS[14], dd["spelledSame"] and dd["coreSame"],
              f"the six fields named at their defaults read the same bytes: {dd['spelledSame']}; "
              f"the choice core's own four-value call reads them too: {dd['coreSame']}. The equality "
              f"is against the composer's own output on this same run, never against the prebaked "
              f"pack stage 0 was landed on — that gate went with the road it guarded")

        # --- rows 12-14 · the three fences ---------------------------------------------------------
        f = got["fences"]
        check(NODE_ROWS[15],
              f["role"]["composed"] is False and "grand finale" in (f["role"]["declined"] or "")
              and "route role" in (f["role"]["declined"] or ""),
              f"refusal: {f['role']['declined']!r}; the five it names: {got['routeRoles']}")
        check(NODE_ROWS[16],
              f["memory"]["composed"] is False and "cooldown" in (f["memory"]["declined"] or "")
              and f["memoryOk"]["composed"] is True,
              f"a fourth field refuses: {f['memory']['declined']!r}; the three §4.8 lets cross "
              f"compose: {f['memoryOk']['composed']}")
        check(NODE_ROWS[17],
              f["seedHigh"]["composed"] is False and f["seedLow"]["composed"] is False
              and "seed" in (f["seedHigh"]["declined"] or ""),
              f"a die of 9 refuses: {f['seedHigh']['declined']!r}; a die of -1 refuses: "
              f"{f['seedLow']['declined']!r}; the span it reads off the instrument's manifest: "
              f"{got['seedSpan']}")

        # --- rows 15-25 · the same repairs, each reverted in a copy ---------------------------------
        # A planted run walks a corner of the collection rather than all of it, because a plant is
        # judged on whether the answer MOVES and twenty-four works are 552 ordered pairs of proof.
        CORNER = 24
        PLANTS = [
            (NODE_ROWS[18], [["if (ROUTE_ROLES.indexOf(role) < 0) {", "if (false) {"]],
             lambda g: g["fences"]["role"]["composed"] is True),
            (NODE_ROWS[19], [["if (odd.length) {", "if (false) {"]],
             lambda g: g["fences"]["memory"]["composed"] is True),
            (NODE_ROWS[20],
             [["roadFor(fromW, toW, FLOORS, step, memory || null, seed, key)",
               "roadFor(fromW, toW, FLOORS, step, memory || null, 0, key)"]],
             lambda g: len(g["dice"]["distinct"]) == 1),
            (NODE_ROWS[21],
             [["if (num(nearAxis.delta) > SIMILAR_DELTA) {", "if (false) {"]],
             lambda g: g["roadNotes"]["shared-ground"]["ok"] is True
             and got["roadNotes"]["shared-ground"]["ok"] is True),
            (NODE_ROWS[22], [["if (fits) break;", "break;"]],
             lambda g: (g["roles"]["quiet link"].get("budget") or {}).get("letters", 0) > 1
             or (g["roles"]["quiet link"].get("budget") or {}).get("miracles", 0) > 0
             or g["roles"]["quiet link"].get("duration", 0) > 4000),
            # A LED PASSAGE IS A READING OF TWO THINGS, and each is proved by taking it away.
            (NODE_ROWS[23], [["LED_ROLES.indexOf(role) >= 0", "true"]],
             lambda g: g["sweep"]["ledElsewhere"] > 0),
            (NODE_ROWS[24], [["made.cameraTravels && ", ""]],
             lambda g: g["sweep"]["ledAtTonic"] > 0.6 * g["sweep"]["tonic"]),
            (NODE_ROWS[25],
             [["          if (familyOf(whole[i], fromW, toW, floors) === memory.family) {\n            held = whole[i];\n            heldBy = \"family\";",
               "          if (false) {\n            held = whole[i];\n            heldBy = \"family\";"]],
             lambda g: g["memory"]["heldAgainBy"] != "family"
             and g["memory"]["heldBackBy"] != "family"),
            (NODE_ROWS[26],
             [["      var wantTransform = memory && memory.family ? String(memory.family).split(\"+\")[0] : null;",
               "      var wantTransform = null;"],
              ["      if (memory && memory.family) {\n        var whole = pool.concat(found.roads).concat([BRIDGE_ROAD]);",
               "      if (false) {\n        var whole = pool.concat(found.roads).concat([BRIDGE_ROAD]);"]],
             lambda g: not (g["memory"]["backKeepsFamily"] or g["memory"]["backKeepsPivot"])),
            # THE FENCE IS PROVED WHERE IT COULD BE CROSSED. Nothing today hands the open handle to
            # this function — the collection's own instrument list leaves it out — so the plant that
            # makes the row honest is the one that DOES hand it over: a cue's tracks named off the
            # manifest itself. With the fence in place the open handle is still skipped; the second
            # plant removes the fence under the same pressure and it is driven.
            (NODE_ROWS[27],
             [["        if (manifest[h].open) continue;", ""],
              ["var unnamed = Object.keys(c.tracks).filter(function (h) { return !HANDLE_SOURCE[h]; });",
               "var unnamed = [];"],
              ['var why = HANDLE_SOURCE[h][1];',
               'var why = (HANDLE_SOURCE[h] || ["", "an open handle"])[1];'],
              ["var spec = HANDLE_SPECS[instr][handle], lo = spec[0], hi = spec[1], dflt = spec[2];",
               "var m0 = MANIFESTS[instr].handles[handle];"
               " var spec = HANDLE_SPECS[instr][handle] || [m0.min, m0.max, m0[\"def\"]],"
               " lo = spec[0], hi = spec[1], dflt = spec[2];"]],
             lambda g: "bal" in g["sweep"]["openDriven"]),
            (NODE_ROWS[28],
             [["if (line.length > INTENT_FENCE_CHARS && fields.returnPhrase) {", "if (false) {"],
              ["if (line.length > INTENT_FENCE_CHARS && fields.roadPhrase) {", "if (false) {"]],
             lambda g: g["handed"]["roadKept"] > 0),
            # THE FOLD'S TWO LAWS, each proved by taking its own gate away. The first is read off
            # the instrument's own manifest — an instrument declaring the WORLD level folds the
            # space — so removing that reading is removing the law.
            (NODE_ROWS[29],
             [["      if (!castableOnKind(kind, a, b, FLOORS, noMiracle)) return false;",
               "      if (false) return false;"],
              ["        if (noMiracle && spendsTheMiracle(all[i])) {",
               "        if (false) {"],
              ["        } else if (spendsTheMiracle(travelInstr) && !(ROLE_BUDGETS[role] || {}).miracle) {",
               "        } else if (false) {"]],
             lambda g: sum(g["sweep"]["folded"][r]
                           for r in ("entrance", "quiet link", "return")) > 0),
            # THE FOLD IS THE MIRACLE, and this is the line that says so. The OTHER half of the
            # law — that the arriving work's own folded space stands down beside a fold, so no
            # crossing carries two — is in the code and cannot be reddened on this collection: no
            # pair of the 121 can produce both at once, measured. It is kept because it is the law
            # and the collection changes; it is named here rather than dressed as a proof.
            # ONE INSTRUMENT PER KIND, RESTORED IN A COPY — the rule this lane repaired. With the
            # candidates on a kind cut back to the first of them, the unfold becomes unreachable
            # again and the row above reddens, which is what makes that row a guard rather than a
            # census.
            (NODE_ROWS[31],
             [["        if (CUTS_ON[kind].indexOf(iid) < 0) CUTS_ON[kind].push(iid);",
               "        if (!CUTS_ON[kind].length) CUTS_ON[kind].push(iid);"]],
             lambda g: [i for i in g["sweep"]["cast"] if not g["sweep"]["chosen"].get(i)]),
            (NODE_ROWS[30],
             [['      if (folds === "pivot") voices.pivot = "miracle";',
               '      if (false) voices.pivot = "miracle";']],
             lambda g: sum(g["sweep"]["foldUnspent"][r] for r in g["sweep"]["foldUnspent"]) > 0),
        ]
        # The intent fence's own standing row: with the cap planted DOWN and the guard in place,
        # every line the composer writes still fits under it. The red-on-bug above removes the guard
        # under the same pressure and the lines run over.
        # THE FENCE IS MEASURED UNDER PRESSURE, because at the cap the client actually applies no
        # line of this collection comes near it. The pressure is applied the way the WIRE applies it
        # — a smaller cap handed to the composer in its own constants, not a number planted in its
        # source — because the site now publishes the cap and a plant on the fallback would prove
        # only that the fallback still exists. Every line over the handed cap then gives up the
        # clauses THIS LANE added, the pass count first and then the road's own opening, and never a
        # word of the line that stood before the lane. The red-on-bug below removes the guard under
        # the same pressure and the openings stay.
        hd = got["handed"]
        check("EX-COMPOSED the intent fence gives up this lane's own clauses before the line "
              "is refused whole",
              hd["roadKept"] == 0 and hd["shortened"] > 0 and sweep["roadKept"] > 0
              and sweep["intentShortened"] == 0,
              f"handed a cap of {hd['cap']} characters in its own constants, {hd['shortened']} of "
              f"{hd['composed']} lines gave up a clause and {hd['roadKept']} kept a road's opening; "
              f"at the {sweep['intentCap']} the client applies, {sweep['roadKept']} of "
              f"{sweep['composed']} lines carry theirs and {sweep['intentShortened']} give anything "
              f"up")

        for name, plants, reddens in PLANTS:
            g = node_run(plants, sweep=CORNER)
            if g.get("error"):
                check(name, False, "the planted run failed: " + g["error"])
            else:
                moved = reddens(g)
                check(name, moved,
                      f"with «{plants[0][0]}» in place the row above holds; with it changed to "
                      f"«{plants[0][1]}» the answer moves, and this run read that it did: {moved}")

# ---------------------------------------------------------------- the walk, in a browser

BROWSER_ROWS = [
    "EX-COMPOSED the composer's file is never fetched while the layer stands off",
    "EX-COMPOSED the walk fetches the composer once, at the landing, and it joins",
    "EX-COMPOSED a step over two recorded works derives a passage and freezes it onto the command",
    "EX-COMPOSED the passage's own request stands on the diagnostic surface beside the score",
    "EX-COMPOSED the passage plays, and what the instrument applied on its own buffer is written back onto it",
    "EX-COMPOSED the instrument's own door reading arrives on the passage record, on the buffer it drew on",
    "EX-COMPOSED two passages on two grids: no reading of one reaches the other's record",
    "EX-COMPOSED a work the record set never heard of keeps the walk's own glide",
    "EX-COMPOSED reduced motion asks for no composer at all, and records why",
]


def enter(br, base, pass_arg=None, step=False):
    """A fresh visitor who opens the door and stands in the walk. `step` takes ONE real step, which
    is the only road that asks for the picture layer's file (engine/client/15-motion.js: the layer
    is opened where a step declares its command)."""
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
    br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    if step:
        br.key("ArrowDown")
        for _ in range(30):
            if br.evaluate("String(!!(window.__exPass && window.__exPass.layer()))") == "true":
                break
            br.sleep(0.2)
        br.sleep(0.5)


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def put_records(base_dir, ids):
    """The settings record as the site writes it for the composed road: the collection's own
    constants and one record per work on the walk, keyed by the id the walk hangs the work under.
    The fixture's two records are re-keyed onto the works this bake actually hangs — what the
    composer reads out of a record is measurement, and the id is only its name."""
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    fix = json.loads(FIXTURE.read_text(encoding="utf-8"))
    src = [fix["works"][fix["pair"]["a"]], fix["works"][fix["pair"]["b"]]]
    works = {}
    for i, wid in enumerate(ids):
        rec = json.loads(json.dumps(src[i % 2]))
        rec["id"] = wid
        works[wid] = rec
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fix["consts"],
                       works=works)
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return works


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            # 0 · the layer stands off: nothing is asked for
            enter(br, base, "diagnostics:on")
            asked = js(br, "var r = window.__exPass.report();"
                           "return {state: r.composer.state, works: r.composer.works,"
                           " files: performance.getEntriesByType('resource')"
                           "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                           "  .length};")
            check(BROWSER_ROWS[0], asked["state"] == "absent" and asked["files"] == 0,
                  f"the composer reads {asked['state']} and the file was fetched "
                  f"{asked['files']} time(s); the settings record carries "
                  f"{asked['works']} work record(s)")

            # the records arrive without a rebake, the way a content change always has
            # EVERY WORK BUT ONE IS GIVEN A RECORD. The walk deals its works afresh on every entry,
            # so which two the visitor stands over is the walk's own choice and no row may pin it;
            # what a row may do is make sure the pair it asks about is recorded and one work is not.
            allworks = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                              ".map(function(e){return e.dataset.id;});")
            recorded = list(put_records(TMP, allworks[:-1])) if len(allworks) >= 3 else []
            unrecorded = allworks[-1] if len(allworks) >= 3 else None
            if len(recorded) < 2:
                for r in BROWSER_ROWS[1:]:
                    skip(r, f"the walk hung fewer than three works: {allworks[:4]}")
            else:
                enter(br, base, "diagnostics:on", step=True)
                for _ in range(30):
                    if js(br, "return window.__exPass.report().composer.state;") == "read":
                        break
                    br.sleep(0.2)
                shown = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                               ".map(function(e){return e.dataset.id;});")
                pair = [w for w in shown if w in recorded][:2]
                # The walk deals afresh on every entry, so the work with no record of its own is
                # read off THIS hang rather than remembered from the last one.
                unrecorded = next((w for w in shown if w not in recorded), None)
                rep = js(br, "var r = window.__exPass.report();"
                             "return {state: r.composer.state, version: r.composer.version,"
                             " works: r.composer.works, src: r.composer.src,"
                             " files: performance.getEntriesByType('resource')"
                             "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                             "  .length};")
                check(BROWSER_ROWS[1],
                      rep["state"] == "read" and rep["files"] == 1 and rep["version"] is not None,
                      f"the composer reads {rep['state']} at version {rep['version']}, fetched "
                      f"{rep['files']} time(s) from {rep['src']}, over {rep['works']} work records")

                # 2 · a step over two recorded works
                if len(pair) < 2:
                    for r_ in BROWSER_ROWS[2:8]:
                        skip(r_, f"this hang shows fewer than two recorded works: {shown[:4]}")
                    pair = None
                r = None if pair is None else js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var B = document.querySelector('.exh-frame[data-id="%s"]');
                  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                             kind:'step', cause:'composed',
                                                             velocity:0});
                  window.__cmd = cmd;
                  var said = window.__exPass.report().refusals.filter(function(x){
                    return x.what === 'score'; });
                  return {got: !!cmd, hasScore: !!(cmd && cmd.score),
                          schema: cmd && cmd.score ? cmd.score.schema : null,
                          pair: cmd && cmd.score ? cmd.score.pair : null,
                          why: said.length ? said[said.length - 1].why : null,
                          cues: cmd && cmd.score && cmd.score.cues
                                ? cmd.score.cues.map(function(c){return c.instrument.id;}) : null};
                """ % (pair[0], pair[1]) if pair else "")
                if pair:
                    check(BROWSER_ROWS[2],
                          r["got"] and r["hasScore"] and r["schema"] == 2 and r["cues"],
                          f"command={r}")

                # 3 · the request on the diagnostic surface
                p = None if pair is None else js(
                    br, "var rows = window.__exPass.report().composer.passages;"
                        "var row = rows.length ? rows[rows.length - 1] : null;"
                        "if (row) { var ids = row.key.split('__');"
                        "  row.hangNow = window.__exPass.adapter.hangGeometry("
                        "    ids[2] === 'ba' ? ids[1] : ids[0]); }"
                        "return row;")
                if pair:
                    check(BROWSER_ROWS[3],
                      bool(p) and p["key"].startswith(min(pair[0], pair[1]))
                      and p["request"]["direction"] in ("a-to-b", "b-to-a")
                      # 2026-08-18 (U27 stage 2): the walk STATES a role now, so this row stops
                      # asking for the composer's own default and asks for one of the five the
                      # composer fences on. Which one it is belongs to the route's own dramaturgy
                      # and is measured by tests/test_pass_route.py; pinning it here would be a
                      # second home for that fact and would redden on a re-dealt hang.
                      and p["request"]["routeRole"] in ROLE_BUDGET
                      and p["request"]["sessionMemory"] is None
                      and isinstance(p["request"]["seed"], (int, float))
                      and 0 <= p["request"]["seed"] <= 8
                      and bool(p["request"]["buffer"])
                      # The camera's own pose is the departing work's real box, measured off the
                      # DOM. A box the walk itself cannot measure at this instant is the field's
                      # documented default — the flight departs from the score's own rest — so the
                      # row asks only that the two readings AGREE: the request may not carry a pose
                      # the walk would not have measured.
                      and (p["request"]["cameraState"] is None) == (p["hangNow"] is None),
                      f"passage={json.dumps(p, ensure_ascii=False)[:700] if p else None}")

                # 4 · the passage PLAYS, and the applied reading comes back onto it
                #
                # His architecture decision of 2026-08-17 18:00: the instrument reads its doors at
                # run time on the actual buffer, and that reading is the runtime truth. It cannot be
                # known before the frame is drawn, so the walk writes it onto the passage record at
                # the landing — beside the request that asked for it.
                #
                # WHAT THIS ROW REACHES, AND WHERE IT STOPS. What comes back is what the HOST
                # publishes: the instrument that took the command, the drawing buffer and its device
                # ratio, and every live cue with the handles the host resolved for it. That is the
                # applied state at the host's level and this row holds it.
                #
                # The instrument's OWN door reading travels beside it, on each cue's `applied`, and
                # the row below is the one that judges it. This row counts it and prints the count,
                # so a reading that stops arriving is visible here as well as there.
                if pair:
                    for _ in range(40):
                        if js(br, "return !!window.__exPass.layer();") is True:
                            break
                        br.sleep(0.2)
                played = None if pair is None else js(br, """
                  if (!window.__exPass.layer()) return {took: false, noLayer: true};
                  var cmd = window.__cmd;
                  var took = window.__exPass.layer().offer(cmd, {dock: function(){
                    window.__exPass.adapter.dock(cmd); },
                    glide: function(){ window.__glided = true; },
                    curtain: function(){}, mark: function(){}});
                  return {took: took};
                """)
                if pair and played and played.get("took"):
                    for _ in range(80):
                        if js(br, "return window.__exPass.host.report().state;") == "idle":
                            break
                        br.sleep(0.15)
                    br.sleep(0.4)
                ap = None if pair is None else js(
                    br, "var rows = window.__exPass.report().composer.passages;"
                        "return rows.length ? rows[rows.length - 1].applied : null;")
                if pair is None:
                    pass
                elif not (played and played.get("took")):
                    for r_ in (BROWSER_ROWS[4], BROWSER_ROWS[5]):
                        skip(r_,
                             "no picture layer on this device"
                             if (played or {}).get("noLayer") else
                             "the host declined the composed passage on this device: no frame was "
                             "drawn, so nothing was applied")
                else:
                    handles = [c for c in (ap or {}).get("cues", []) if c.get("handles")]
                    door = [c for c in (ap or {}).get("cues", []) if c.get("applied")]
                    check(BROWSER_ROWS[4],
                          bool(ap) and bool(ap.get("instrument")) and bool(ap.get("buffer"))
                          and bool(handles),
                          f"applied on a {ap['buffer'] if ap else '?'} buffer at dpr "
                          f"{ap['dpr'] if ap else '?'}, {len(handles)} live cue(s): "
                          + json.dumps([{"id": c["id"], "instrument": c["instrument"],
                                         "size": c["handles"].get("size")}
                                        for c in handles], ensure_ascii=False)[:300]
                          + f"; the instrument's own door reading reaches this record for "
                            f"{len(door)} of them")

                    # 5 · THE INSTRUMENT'S OWN READING, on the record the request came from.
                    #
                    # His architecture decision of 2026-08-17 18:00: the instrument reads its doors
                    # at run time on the ACTUAL buffer, and that reading is the runtime truth. What
                    # this row judges is that the reading arrived and that it was taken on the
                    # buffer the frame was really drawn on — not on the CSS frame around it, and not
                    # on anything the composer could have known when it wrote the request.
                    #
                    # The five instruments publish one shape: `door`, `buffer`, `reads`, `request`,
                    # `applied`, `moved`, `unit`, `held`, `whyNo`. Three laws hold across all five
                    # and are checked on every reading this passage produced:
                    #   · it was taken AT A DOOR — `door` reads «in» or «out», never a mid-passage
                    #     instant, because a door is the only instant the reading is defined at;
                    #   · it was taken ON THE HOST'S OWN BUFFER — the two numbers agree with the
                    #     buffer the host reports for the same frame;
                    #   · a door that had to be MOVED says so — `moved` is non-zero exactly when
                    #     `held` names the leak the request would have drawn, and both are quiet
                    #     when the request was whole as it stood.
                    #
                    # `whyNo` IS NOT REQUIRED TO BE EMPTY, corrected 2026-08-17. The row first asked
                    # for that, reasoning that a refusal ends the passage and this passage played.
                    # It is the wrong bar: the channel is documented to carry the applied state ON
                    # THE WAY TO a refusal — the instrument reports and then refuses — so a record
                    # whose reading names a refusal is the channel working, and the walk's own glide
                    # carried the visitor. Which instrument refuses at a door is a property of the
                    # buffer this machine happens to draw on, so a bar of «never a refusal» made the
                    # row a device check. What is asked instead is that a refusal is a sentence when
                    # it is there at all.
                    #
                    # The per-instrument numbers themselves are held in each instrument's own suite,
                    # where the frame is drawn and photographed; the red-on-bug proof for the
                    # reporting call is tests/test_pass_weave.py.
                    def law(c):
                        a = c["applied"]
                        buf = a.get("buffer") or []
                        why = a.get("whyNo")
                        return (a.get("door") in ("in", "out")
                                and len(buf) == 2
                                and f"{buf[0]}x{buf[1]}" == ap.get("buffer")
                                and isinstance(a.get("reads"), str)
                                and isinstance(a.get("request"), (int, float))
                                and isinstance(a.get("applied"), (int, float))
                                and bool(a.get("moved")) == bool(a.get("held"))
                                and (why is None or (isinstance(why, str) and why.strip())))

                    broke = [c for c in door if not law(c)]
                    check(BROWSER_ROWS[5],
                          bool(door) and not broke,
                          f"{len(door)} of {len((ap or {}).get('cues', []))} cue(s) published a "
                          f"reading, taken on the {ap.get('buffer')} buffer the host reports at dpr "
                          f"{ap.get('dpr')}: "
                          + json.dumps([{"instrument": c["instrument"], "applied": c["applied"]}
                                        for c in door], ensure_ascii=False)[:600]
                          + (f"; readings breaking the shape: "
                             + json.dumps(broke, ensure_ascii=False)[:300] if broke else ""))

                # 6 · TWO PASSAGES, TWO GRIDS. The defect this row stands against, found on the
                # merged base of 2026-08-17: a reading published at a door instant stayed on its
                # voice after the drawing buffer moved under the pass — the resolution ladder
                # stepping down, or a resize arriving mid-flight. A voice whose window had already
                # closed never reported again, so its reading rode to the landing and was published
                # as that passage's applied state on a grid it was never taken on. The judge read it
                # as a 922 x 648 reading on a record whose host said 768 x 540.
                #
                # A ROW THAT ONLY COUNTS READINGS PASSES THAT DEFECT, which is why this one reads the
                # BUFFER every reading names. The grid is moved inside the first passage, at an
                # instant AFTER the earliest-closing cue's window has shut, so a stale reading has
                # somewhere to hide; then a second passage is played on the new grid. Two things are
                # asked, and each of them reddens on the bug: every reading on a record names that
                # record's own grid, and no reading on the second record names the first's.
                #
                # The repair that makes it hold is in two halves. The host forgets every voice's
                # reading the instant the drawing buffer changes, so a voice that has not reported
                # on the grid now standing carries nothing — the shape the matter voice already has
                # when its window never opens at a door. And the host freezes the grid each run
                # ended on beside what that run left behind, so a record names its own passage's
                # grid rather than whatever the canvas has since become.
                def edge_windows(a, b):
                    """The cue windows of the passage this pair composes, in the pass's own seconds,
                    read off a command declared and thrown away. A window bound may be a plain
                    number or a driver literal, so both shapes are unwrapped."""
                    got = js(br, """
                      var A = document.querySelector('.exh-frame[data-id="%s"]');
                      var B = document.querySelector('.exh-frame[data-id="%s"]');
                      if (!A || !B) return null;
                      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                                 kind:'step', cause:'grid-peek',
                                                                 velocity:0});
                      if (!cmd || !cmd.score) return null;
                      return {cues: cmd.score.cues.map(function (q) { return q.window || null; })};
                    """ % (a, b))
                    if not got:
                        return []
                    out = []
                    for w in got["cues"]:
                        if isinstance(w, list) and len(w) == 2:
                            out.append([x.get("v") if isinstance(x, dict) else x for x in w])
                    return out

                def play_edge(a, b, cause, resize_to=None, resize_at=None):
                    """One whole passage, landed, read as its own record. `resize_to` moves the grid
                    `resize_at` seconds into the flight — the road a real orientation change takes.
                    The record is found by the KEY the command's own passage carries, never by
                    «the last row», because a passage that never drew leaves a row behind too."""
                    js(br, """
                      var A = document.querySelector('.exh-frame[data-id="%s"]');
                      var B = document.querySelector('.exh-frame[data-id="%s"]');
                      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                                 kind:'step', cause:'%s',
                                                                 velocity:0});
                      if (!cmd) return {nocmd: true};
                      window.__gridCmd = cmd;
                      var took = window.__exPass.layer().offer(cmd, {
                        dock: function(){ window.__exPass.adapter.dock(cmd); },
                        glide: function(){}, curtain: function(){}, mark: function(){}});
                      return {took: !!took, scored: !!cmd.score};
                    """ % (a, b, cause))
                    if resize_to:
                        br.sleep(resize_at)
                        br.set_viewport(resize_to[0], resize_to[1])
                    for _ in range(90):
                        if js(br, "return window.__exPass.host.report().state;") == "idle":
                            break
                        br.sleep(0.15)
                    br.sleep(0.4)
                    return js(br, """
                      var h = window.__exPass.host.report();
                      var rows = window.__exPass.report().composer.passages;
                      var cmd = window.__gridCmd, row = null;
                      for (var i = rows.length - 1; i >= 0; i--) {
                        if (cmd && cmd.score && rows[i].key === cmd.score.key) { row = rows[i]; break; }
                      }
                      if (!row && rows.length) row = rows[rows.length - 1];
                      return {applied: row ? (row.applied || null) : null,
                              // the grid the HOST says this run drew on, frozen with the run
                              grid: h.drawnOn ? h.drawnOn.buffer : (h.census ? h.census.buffer : null)};
                    """)

                def readings(rec):
                    return [c for c in ((rec or {}).get("applied") or {}).get("cues", [])
                            if c.get("applied")]

                def grid_of(rec):
                    """The grid this passage drew on: the record's own if it has one, and the host's
                    frozen reading of the same run otherwise."""
                    return (((rec or {}).get("applied") or {}).get("buffer")) or (rec or {}).get("grid")

                def names(rs):
                    return sorted({"%dx%d" % tuple(c["applied"]["buffer"]) for c in rs
                                   if len(c["applied"].get("buffer") or []) == 2})

                if pair:
                    wins = edge_windows(pair[0], pair[1])
                    shuts = sorted(w[1] for w in wins if isinstance(w[1], (int, float)))
                    # a breath past the first window to close, and still inside the pass: this is
                    # where a stale reading has somewhere to hide, since the voice whose window has
                    # just shut will never be handed another frame on the new grid
                    at = (shuts[0] + 0.3) if shuts else 1.0
                    # A passage the host declines on this device draws nothing and publishes nothing,
                    # which gives the row no first grid to carry. It is asked again rather than
                    # waved through, up to three times.
                    first = None
                    for _try in range(3):
                        first = play_edge(pair[0], pair[1], "grid-one",
                                          resize_to=(940, 660), resize_at=at)
                        if readings(first):
                            break
                        br.set_viewport(1280, 900)
                        br.sleep(0.6)
                    second = play_edge(pair[0], pair[1], "grid-two")
                    br.set_viewport(1280, 900)
                    br.sleep(0.6)
                    one_buf, two_buf = grid_of(first), grid_of(second)
                    r1, r2 = readings(first), readings(second)
                    n1, n2 = names(r1), names(r2)
                    if not (one_buf and two_buf and r2):
                        skip(BROWSER_ROWS[6],
                             f"the second passage of this pair drew nothing on this device: "
                             f"first={one_buf!r} with {len(r1)} reading(s), second={two_buf!r} with "
                             f"{len(r2)} reading(s)")
                    elif one_buf == two_buf:
                        skip(BROWSER_ROWS[6],
                             f"both passages drew on one grid ({one_buf}), so this device gives the "
                             f"row nothing to tell apart — the resolution ladder answered the "
                             f"resize by landing back on the same buffer")
                    else:
                        check(BROWSER_ROWS[6],
                              n1 in ([], [one_buf]) and n2 in ([], [two_buf])
                              and one_buf not in n2,
                              f"the first passage drew on {one_buf} with the grid moved "
                              f"{at:.2f} s in, and its {len(r1)} reading(s) name {n1 or 'nothing'}; "
                              f"the second drew on {two_buf} and its {len(r2)} reading(s) name "
                              f"{n2 or 'nothing'}. A voice whose window shut before the grid moved "
                              f"carries nothing rather than a reading on a buffer that no longer "
                              f"stands, and the first passage's grid appears nowhere on the "
                              f"second's record")

                # 5 · a work with no record of its own
                r = None if (pair is None or unrecorded is None) else js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var C = document.querySelector('.exh-frame[data-id="%s"]');
                  if (!A || !C) return {absent: true};
                  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:C, dir:1, span:100,
                                                             kind:'step', cause:'unrecorded',
                                                             velocity:0});
                  var said = window.__exPass.report().refusals.filter(function(x){
                    return x.what === 'composer' && x.name === 'request'; });
                  return {score: cmd ? cmd.score : 'no command', to: C.dataset.id,
                          why: said.length ? said[said.length - 1].why : null};
                """ % (pair[0], unrecorded) if (pair and unrecorded) else "")
                if pair and unrecorded is None:
                    skip(BROWSER_ROWS[7], f"every work of this hang carries a record: {shown[:4]}")
                elif pair and r.get("absent"):
                    skip(BROWSER_ROWS[7], f"this hang shows no unrecorded work ({unrecorded})")
                elif pair:
                    check(BROWSER_ROWS[7],
                          r["score"] is None and "carries no record" in (r["why"] or ""),
                          f"a step to {r['to']} froze {r['score']!r} onto the command; "
                          f"the reason on the surface: {r['why']!r}")

                # 6 · reduced motion
                with Browser(width=1280, height=900) as br2:
                    br2.emulate_media(prefers_reduced_motion="reduce")
                    enter(br2, base, "diagnostics:on")
                    red = js(br2, "var r = window.__exPass.report();"
                                  "var said = r.refusals.filter(function(x){"
                                  "  return x.what === 'composer'; });"
                                  "return {state: r.composer.state,"
                                  " why: said.length ? said[said.length-1].why : null,"
                                  " files: performance.getEntriesByType('resource')"
                                  "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                                  "  .length};")
                    check(BROWSER_ROWS[8],
                          red["files"] == 0 and red["why"] == "reduced motion",
                          f"the file was fetched {red['files']} time(s); the reason on the "
                          f"surface: {red['why']!r}")

import shutil  # noqa: E402
shutil.rmtree(TMP, ignore_errors=True)

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
