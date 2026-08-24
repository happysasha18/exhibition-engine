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
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import parse_qs, urlparse

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
# THE CLIENT'S OWN CAP ON A CAMERA TRACK'S POINTS (engine/client/01a-pass.js's PASS_LIMITS.camera),
# read the same road as CLIENT_BYTES/CLIENT_INTENT above rather than retyped: the witness camera's
# flight below has to stand under the same published number the client itself enforces.
CLIENT_CAMERA_POINTS = int(re.search(r"\bcamera:\s*(\d+)", CLIENT_LIMITS.group(1)).group(1))
# THE ONE BOUND THE WITNESS CAMERA'S FIVE AXES SHARE (pass-composer.js's own `DOLLY_CAP`), read out
# of the composer's source rather than retyped, so a change to that number re-bases this suite by
# itself instead of leaving a second copy to drift.
COMPOSER_SRC = MODULE.read_text(encoding="utf-8")
DOLLY_CAP_VALUE = float(re.search(r"\bDOLLY_CAP\s*=\s*([\d.]+)\s*;", COMPOSER_SRC).group(1))

# ---------------------------------------------------------------- EX-PASS-RECORDS: no per-work record
# rides the first file a visitor's browser ever parses (2026-08-19). `works` left the settings
# record's `pass` block for the reason engine/build.py's own EX-PASS-RECORDS comment states: his word
# of 13:36, «какой размер по устройству?? почему это должно зависеть от числа работ?» — the block
# config.json carries at the very first parse must never grow with the collection. The claim is read
# STRUCTURALLY, off what each key left sizes against, never by counting the fixture's own works (WORKS
# above holds 121 of them and never enters this check): `capabilities` is exactly the client's OWN two
# published fences (CLIENT_INTENT, CLIENT_BYTES, already read off the bundle above), and `instruments`
# is keyed one entry per instrument FILE this tree actually ships — a roster the engine's own arsenal
# bounds, not the collection.
INSTRUMENT_ROSTER = sorted(
    p.stem[len("pass-inst-"):]
    for p in (ROOT / "engine" / "assets").glob("pass-inst-*.js")
)
PASS_BLOCK = CFG.get("pass") or {}
check("EX-COMPOSED the block a visitor's browser parses first carries no per-work record: «works» "
      "is gone, and every key left sizes off the instrument roster this tree ships or the client's "
      "own published fences — never off how many works the collection holds",
      "works" not in PASS_BLOCK
      and set(PASS_BLOCK.get("capabilities", {}).keys()) == {"intentChars", "scoreBytes"}
      and PASS_BLOCK["capabilities"]["intentChars"] == CLIENT_INTENT
      and PASS_BLOCK["capabilities"]["scoreBytes"] == CLIENT_BYTES
      and sorted(PASS_BLOCK.get("instruments", {}).keys()) == INSTRUMENT_ROSTER,
      f"pass block ships the keys {sorted(PASS_BLOCK.keys())}; capabilities="
      f"{PASS_BLOCK.get('capabilities')} against the client's own {CLIENT_INTENT}/{CLIENT_BYTES}; "
      f"{len(PASS_BLOCK.get('instruments') or {})} instrument record(s) against the "
      f"{len(INSTRUMENT_ROSTER)} the tree ships")

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
# The eight genres of crossing. There is no fallback among them and no last candidate: each answers
# for every pair with a fit, and the best-suited plays (his word of 2026-08-18 10:15).
ROADS = ["shared-ground", "spin", "kaleidoscope", "symmetry-slide", "stripes",
         "dissimilar-mystery", "tonal-and-spectral", "box-fold"]
ROLES_ALL_PY = ["entrance", "quiet link", "middle", "culmination", "return"]

NODE_ROWS = [
    "EX-COMPOSED every genre answers for every pair with a fit and the reading behind it",
    "EX-COMPOSED the frame folds into a solid, and only where the step's role may spend a miracle",
    "EX-COMPOSED every pair composes at every one of the five route roles without throwing",
    "EX-COMPOSED every instrument that travels to a visitor can actually be chosen",
    "EX-COMPOSED no one instrument carries a cast route, and the route's shapes are several",
    "EX-COMPOSED the die chooses the road, so a pinned seed reproduces the choice",
    "EX-COMPOSED the camera leads a passage at the walk's two tonic steps and nowhere else",
    "EX-COMPOSED the five route roles compose five passages, each inside shelf 17's own budget",
    "EX-COMPOSED the family the composer hands back is the one the walk reads off the plan",
    "EX-COMPOSED an edge walked back keeps its family and its pivot and differs in what may differ",
    "EX-COMPOSED every handle the composer drives names the measurement it reads",
    "EX-COMPOSED a handle the instrument declares open is never driven at a door",
    "EX-COMPOSED no filled score ever crosses the byte or the intent fence, because it is fitted",
    "EX-COMPOSED the composer measures its line against the fence it is handed, not against its own "
    "fallback",
    "EX-COMPOSED every hard record yields a playable crossing, at every role and both ways",
    "EX-COMPOSED every field the request gained reproduces the four-value call exactly",
    "EX-COMPOSED a route role outside the five reads as a middle and the stray name is recorded",
    "EX-COMPOSED a session memory wider than §4.8's three fields has the extra left unread",
    "EX-COMPOSED a die outside the instrument's own span is wrapped into it",
    "EX-COMPOSED red-on-bug · the pair fence removed: a request with one work is no longer refused",
    "EX-COMPOSED red-on-bug · §4.8's fence removed: a fourth memory field is read",
    "EX-COMPOSED red-on-bug · the die dropped on its way to the road: every die picks one road",
    "EX-COMPOSED red-on-bug · the genre fits flattened: the ranking stops reading the pair",
    "EX-COMPOSED red-on-bug · the role's budget removed: a quiet link spends two letters",
    "EX-COMPOSED red-on-bug · the led passage's role gate removed: a middle is led by its camera",
    "EX-COMPOSED red-on-bug · the led passage's own reading removed: every tonic step is led",
    "EX-COMPOSED red-on-bug · the family hold removed: the return stops naming the recorded family",
    "EX-COMPOSED red-on-bug · the return's own step removed: the way back keeps neither family "
    "nor pivot",
    "EX-COMPOSED red-on-bug · the open-handle fence removed: the composer drives a door's own state",
    "EX-COMPOSED red-on-bug · the line stops being fitted: it stands over the cap it is measured "
    "against",
    "EX-COMPOSED red-on-bug · all four of the miracle's own gates removed: a step with no miracle "
    "folds the world",
    "EX-COMPOSED red-on-bug · the fold stops counting as the miracle: a folding crossing spends "
    "none",
    "EX-COMPOSED red-on-bug · one instrument per kind restored: an instrument travels unchosen",
    "EX-COMPOSED red-on-bug · the ground gated on the top quartile again: fewer pairs reach their "
    "own shared ground",
    "EX-COMPOSED the line gives up its own clauses and then its tail, and is never lost",
    "EX-COMPOSED adrift's seamA/seamB carry the record's own seam strength, not a whole-or-nothing "
    "reading of it",
    "EX-COMPOSED waterline's tideCells is driven off the record's own grain, not left at its "
    "manifest default",
    "EX-COMPOSED grid-colour's six colour-and-light voice handles are driven off the departing "
    "work's own colour reading on the cue that owns LIGHT-COLOUR, not left resting at 0",
    "EX-COMPOSED strata-light's twelve colour-and-light voice handles are driven off the two "
    "works' own colour readings on the cue that owns LIGHT-COLOUR, not left resting at 0",
    "EX-COMPOSED a cue that only accompanies another on LIGHT-COLOUR leaves all its colour-and-light "
    "voice handles at their manifest rest of 0, shelf 17's levels law holding",
    "EX-COMPOSED strata-light's levelA/levelB are driven off the two works' own luminance.level, "
    "not left resting at their manifest default of 0.5",
    "EX-COMPOSED gates' slotPlace/slotHalf/slotAxis are driven off the departing work's own "
    "measured slot, not left resting at the module's own naive middle",
    "EX-COMPOSED the witness camera's middle carries a non-neutral pose that differs pair to pair, "
    "and the camera block survives the score's own wire-fitting",
    "EX-COMPOSED each camera axis, where it is non-zero, matches the record reading it claims to "
    "read",
    "EX-COMPOSED the camera's two ends stand at the plain neutral pose on every pair, whatever the "
    "middle does",
    "EX-COMPOSED the camera track never exceeds the client's own published camera-point fence",
    "EX-COMPOSED the letters a walk has already played cool in the die, so a route handed its own "
    "memory spreads wider than the same route composed blind — and never loses a crossing for it",
    "EX-COMPOSED the camera axis that carries the passage clears the level the pair's own grain "
    "sets, so the flight reads against the pictures rather than against nothing",
    "EX-COMPOSED a colour or light voice that is driven at all is loud enough to be seen, by the "
    "lab's own measured threshold, and one that cannot be is not declared",
    "EX-COMPOSED a walk memory the entry cannot read as sent is read as far as it can be and "
    "recorded, never a reason to lose the crossing",
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
// engine/client/01a-pass.js's own PASS_LIMITS.camera — the client's own cap on a camera track's
// points — and pass-composer.js's own DOLLY_CAP, the one bound the witness camera's five axes
// share. Both travel in from Python exactly as BYTE_CAP/INTENT_CAP do, read out of the served
// client and the composer's own source rather than retyped here.
const CAMERA_POINT_CAP = CAPS.cameraPoints;
const DOLLY_CAP = CAPS.dollyCap;
if (!(INTENT_CAP > 0) || !(BYTE_CAP > 0)) {
  console.log(JSON.stringify({error: "the client published no fences to measure against: "
                                     + JSON.stringify(CAPS)}));
  process.exit(0);
}
if (!(CAMERA_POINT_CAP > 0) || !(DOLLY_CAP > 0)) {
  console.log(JSON.stringify({error: "the camera's own two bounds did not travel in: "
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
// A NODE'S VALUE MAY BE THE MODULE'S OWN FLT WRAPPER ({v: <number>}) rather than a bare number —
// pass-composer.js prints a non-integer through it so the score keeps four decimal places on the
// wire. This file runs outside that module's own closure and so keeps no copy of its `num()`; this
// is the same unwrap, typed once, for the two raw node values CHANGE A and CHANGE B read below.
function toNum(v) { return (v && typeof v === "object" && "v" in v) ? v.v : v; }

// A TRAVELLING HANDLE'S NODE CARRIES NO TOP-LEVEL `.value` — pass-composer.js's node loop (tonight's
// shaped doors and the middle spline) resolves any handle whose `wanted[h]` is a two-point array to
// an `{op:"mix", a, b, ...}` or `{op:"spline", points:[...], ...}` node, exactly the shape every
// other travelling handle in this file already takes; only a handle left at one fixed reading stays
// `{op:"static", value, ...}`. `slotPlace`/`slotHalf` travel from the departing work's own reading
// to the arriving one (the gate's slot moves with the passage), so reading `node.value` on them
// finds nothing — the departing work's own reading is `node.a` (mix) or `node.points[0].value`
// (spline), the value the door of the journey opens on.
function startValue(node) {
  if (!node) return undefined;
  if (node.op === "mix") return node.a;
  if (node.op === "spline" && Array.isArray(node.points) && node.points.length) {
    return node.points[0].value;
  }
  // 2026-08-19, THE CUE'S OWN COURSE. A travelling handle no longer carries its own shape: it maps
  // the cue's one shared course, which runs from nought to one, onto its own two measured ends —
  // so the value it starts at is the first of those ends, `to[0]`, exactly as `a` is for a `mix`
  // and the first point is for a `spline`. Where the course would carry the handle past what its
  // manifest publishes the map stands inside a `clamp`, and the clamp is transparent to this
  // question: the same reading, one node deeper.
  if (node.op === "clamp") return startValue(node["in"]);
  if (node.op === "map" && Array.isArray(node.to) && node.to.length) return node.to[0];
  return node.value;
}

// THE WITNESS CAMERA'S OWN FLIGHT, RE-DERIVED HERE FROM THE RAW RECORD — independently of
// pass-composer.js's own `measuredParts()`/`camAxisPan`/`camAxisPitch` and the camera block inside
// `fillPlan`, so the row below is a real check of what the composer wrote rather than the composer
// checking its own arithmetic against itself. Every reading mirrors measuredParts() (pass-
// composer.js) field for field: grainCells, latticePx/latticeAngleDeg, gateAxis/gatePlace,
// horizonY, radialScore/radialCx/radialCy, figureShare/figureCx/figureCy, colourfulness.
function camGrainCells(w) {
  var side = Number(w.frameSide) || 0;
  var spectral = Number((w.texture || {}).spectralPeriodPx) || 0;
  return spectral > 0 && side > 0 ? side / spectral : 0;
}
function camLattice(w) {
  var st = w.structure || {};
  var stepPx = Number((st.ownDevice || {}).stepPx) || 0;
  var gridPx = Number((st.grid || {}).periodPx) || 0;
  var angle = stepPx > 0 ? (Number((st.ownDevice || {}).angleDeg) || 0)
                         : (Number((st.grid || {}).angleDeg) || 0);
  return {latticePx: stepPx || gridPx, latticeAngleDeg: angle};
}
function camGate(w) {
  var mot = w.motifs || {};
  var axis = mot.gateAxis === "vertical" ? 1 : (mot.gateAxis === "horizontal" ? 0 : null);
  return {gateAxis: axis, gatePlace: Number(mot.gatePlace) || 0};
}
function camHorizon(w) {
  var y = ((w.structure || {}).horizon || {}).y;
  return (y === null || y === undefined) ? null : Number(y);
}
function camOwnCentre(w) {
  var st = w.structure || {};
  var radialScore = Number((st.radial || {}).score) || 0;
  if (radialScore > 0) {
    var rc = (w.motifs || {}).radialCentre || (st.radial || {}).centre || [0.5, 0.5];
    return [Number(rc[0]) || 0.5, Number(rc[1]) || 0.5];
  }
  var box = (st.dominantObject || {}).bbox || [0, 0, 0, 0];
  var figureShare = Math.max(0, box[2] - box[0]) * Math.max(0, box[3] - box[1]);
  if (figureShare > 0) return [(Number(box[0]) + Number(box[2])) / 2,
                                (Number(box[1]) + Number(box[3])) / 2];
  return null;
}
function camLevel(w) { return Number((w.luminance || {}).level) || 0; }
// ONE ENVELOPE (grammar law 5): the pair's own reach, taken on the two works' own TONE —
// `luminance.level`, the median of a work's own luminance — because a camera is shelf 17's WORLD
// voice and flies through light, so how far apart two works stand in their own light is the
// apartness a flight answers to. The judge seat settled this 2026-08-19 02:20, against the first
// build's colour-spread reading; pass-composer.js's own camera block carries the same note.
function camReach(fromW, toW) {
  var v = Math.abs(camLevel(fromW) - camLevel(toW));
  return v < 0 ? 0 : (v > 1 ? 1 : v);
}
// THE FIVE AXES, EXPECTED. Mirrors pass-composer.js's `fillPlan` camera block: pan and pitch differ
// at the outbound and inbound points (an arc), logScale, roll and yaw hold one pair fact across
// both (a plateau) — the shapes named in the code's own comments there.
function camExpected(fromW, toW) {
  var reach = camReach(fromW, toW);
  var cFrom = camOwnCentre(fromW), cTo = camOwnCentre(toW);
  var panFrom = cFrom ? [(cFrom[0] - 0.5) * reach, (cFrom[1] - 0.5) * reach] : [0, 0];
  var panTo = cTo ? [(cTo[0] - 0.5) * reach, (cTo[1] - 0.5) * reach] : [0, 0];
  var gcFrom = camGrainCells(fromW), gcTo = camGrainCells(toW);
  // THE GATE BECOME THE SIGNAL (2026-08-19, this file's own note beside pass-composer.js's own).
  // Until then this line read `-reach * DOLLY_CAP` whenever both works carried grain, the gate
  // deciding whether the dolly moved and `reach` alone deciding how far — so two pairs whose own
  // grains stood a hair apart and two whose grains stood worlds apart flew the same distance the
  // instant both cleared the gate. `grainAsked` is the gap between the two works' own `grainCells`,
  // taken as a signed ratio; `grainShare` spends it against the shared bound with the same shape
  // this row already gives roll and yaw, `CAP · a / (|a| + CAP)`, a limit and never a wall.
  var logScale = 0;
  if (gcFrom > 0 && gcTo > 0) {
    var grainAsked = Math.log(gcFrom / gcTo);
    var grainShare = Math.abs(grainAsked) / (Math.abs(grainAsked) + DOLLY_CAP);
    logScale = -reach * DOLLY_CAP * grainShare;
  }
  // THE PALINDROME BAN (charter shelf 18, 2026-08-19): roll and yaw no longer hold one plateau
  // value at both middle points. pass-composer.js:5680-5750 now GRADES each by the magnitude of
  // its own reading (roll by |lattice angle gap|/90, yaw by |gate offset|/0.5, the identical shape
  // this row's own logScale grading above already takes) and then picks exactly ONE of roll/yaw/
  // pitch — whichever reads the largest SHARE of its own ceiling — to carry the excursion; the
  // other two are written zero at both points, and the winning axis's own OUTBOUND reading is the
  // full graded magnitude while its INBOUND reading is graded down by a further fraction specific
  // to that axis (pass-composer.js:5786-5799): roll by the two works' own lattice-scale ratio
  // (min/max of latticePx), yaw by the ARRIVING work's own gate place. Which of the three axes wins
  // a tie is the composer's own die, salted by the cue's key — not reproduced here, since that is a
  // routing choice, not an arithmetic claim; this function hands back the raw graded magnitude and
  // both fractions, and the row below reads which axis the composer actually carried off the real
  // output before checking that axis's own two points against the formula.
  var latFrom = camLattice(fromW), latTo = camLattice(toW);
  var rollRaw = 0;
  if (latFrom.latticePx > 0 && latTo.latticePx > 0) {
    var d = (latTo.latticeAngleDeg - latFrom.latticeAngleDeg) % 180;
    if (d > 90) d -= 180;
    if (d < -90) d += 180;
    if (d !== 0) rollRaw = reach * DOLLY_CAP * (d > 0 ? 1 : -1) * (Math.abs(d) / 90);
  }
  var rollFraction = 1;
  if (latFrom.latticePx > 0 && latTo.latticePx > 0) {
    rollFraction = Math.min(latFrom.latticePx, latTo.latticePx)
      / Math.max(latFrom.latticePx, latTo.latticePx);
  }
  var gate = camGate(fromW), yawRaw = 0;
  if (gate.gateAxis !== null && gate.gatePlace > 0) {
    var off = gate.gatePlace - 0.5;
    if (off !== 0) yawRaw = reach * DOLLY_CAP * (off > 0 ? 1 : -1) * (Math.abs(off) / 0.5);
  }
  var gateTo = camGate(toW);
  var yawFraction = Math.min(1, Math.max(0, gateTo.gatePlace));
  var hFrom = camHorizon(fromW), hTo = camHorizon(toW);
  var pitchFrom = hFrom === null ? 0 : (hFrom - 0.5) * reach * DOLLY_CAP;
  var pitchTo = hTo === null ? 0 : (hTo - 0.5) * reach * DOLLY_CAP;
  var levelFrom = camLevel(fromW), levelTo = camLevel(toW), levelSum = levelFrom + levelTo;
  var pitchInTied = pitchFrom * (levelSum > 0 ? levelFrom / levelSum : 0.5);
  // THE VOICE LEVEL (2026-08-24, this file's own note beside pass-composer.js's own). The three
  // magnitudes above are exactly as they always were; what is new is that the axis which WINS the
  // contest between them is then lifted so its share of its own ceiling clears the level the pair's
  // own grain sets — `camVoiceFloor` above. The lift is `(floor + (1 − floor)·share) / share`, so
  // the reading still spends the whole span above the floor, the shape of every axis is carried
  // through untouched, and nothing passes its own ceiling. Re-derived here from the raw record, as
  // every other line of this function is.
  var eRollShare = Math.abs(rollRaw) / DOLLY_CAP;
  var eYawShare = Math.abs(yawRaw) / DOLLY_CAP;
  var ePitchShare = Math.max(Math.abs(pitchFrom), Math.abs(pitchTo)) / (0.5 * DOLLY_CAP);
  var eMaxShare = Math.max(eRollShare, eYawShare, ePitchShare);
  var eFloor = camVoiceFloor(fromW, toW);
  var eLift = (eFloor > 0 && eMaxShare > 0)
    ? (eFloor + (1 - eFloor) * eMaxShare) / eMaxShare : 1;
  rollRaw *= eLift; yawRaw *= eLift;
  pitchFrom *= eLift; pitchTo *= eLift; pitchInTied *= eLift;
  return {reach: reach, panFrom: panFrom, panTo: panTo, logScale: logScale,
          rollRaw: rollRaw, rollFraction: rollFraction, yawRaw: yawRaw, yawFraction: yawFraction,
          pitchFrom: pitchFrom, pitchTo: pitchTo, pitchInTied: pitchInTied,
          voiceFloor: eFloor, voiceLift: eLift};
}
// THE LEVEL THE CARRYING AXIS HAS TO CLEAR (charter shelf 2 with shelf 17's voice budget, and his
// 2026-08-24 word watching the live route: the camera does not visibly read during a crossing).
// Re-derived here from the raw record, independently of the composer, exactly as camExpected() is.
//
// A camera excursion reads when the frame's own edge travels by at least ONE element of the pair's
// finer measured grain — below that the pose has moved by less than the picture's own smallest
// feature and there is nothing on screen to read the motion against. The grain is `ownDevice.stepPx`
// falling back to `grid.periodPx`, the same `latticePx` the composer's own roll axis already reads,
// taken as a share of the work's own frame side; the FINER of the two is what registers the smallest
// motion, so the pair's floor is the smaller of the two. A rotation of θ about the frame's centre
// carries a point at the edge — half a frame out, which is the same 0.5 the composer's own camBound
// is stated in — through θ·0.5, so one element of grain asks θ ≥ 2·grainFrac, and as a share of the
// axis's own ceiling that is 2·grainFrac/DOLLY_CAP. Nothing here is a number of taste: every term is
// a reading off the two records or a bound already published in the composer.
function camGrainFrac(w) {
  var side = Number(w.frameSide) || 0;
  var px = camLattice(w).latticePx;
  return side > 0 && px > 0 ? px / side : 0;
}
function camVoiceFloor(fromW, toW) {
  var a = camGrainFrac(fromW), b = camGrainFrac(toW);
  if (!(a > 0) || !(b > 0)) return 0;
  var f = 2 * Math.min(a, b) / DOLLY_CAP;
  return f > 1 ? 1 : f;
}
// THE VOICE'S OWN PEAK, and the threshold it has to clear — both the LAB's, not this file's.
// lab/step4-assembler.js:343 (grid-colour.js's `voiceAt`) drives every colour and light voice as
// `amp · sin(2π(u/period + phase)) · 4u(1−u)`, and lab/step4-assembler.js:102-105 carries the
// measured threshold beside it: VISIBLE = 5/255 with VOICE_TARGET = 6 of 255, the nearest
// distinguishable step above it. The lab's own record of 12.08 names the reading that set it —
// contrast 0,083, amplitude 0,0208, voice peak 0,0187, «то есть 4,77 из 255 при пороге 5» — and its
// own law: «Заявленный и неслышный голос — пустое утверждение разбора». The lab reached the peak by
// RENDERING the layer off-screen twice; the shape above is closed-form in the two numbers the
// composer itself writes, so the same reading needs no probe here.
var VOICE_TARGET_255 = 6;
function voicePeakShare(period, phase) {
  if (!(period > 0)) return 0;
  var best = 0, i, u, v;
  for (i = 0; i <= 2000; i++) {
    u = i / 2000;
    v = Math.abs(Math.sin(2 * Math.PI * (u / period + (phase || 0)))) * 4 * u * (1 - u);
    if (v > best) best = v;
  }
  return best;
}
function camNeutral(pt) {
  return !!pt && (!pt.pan || (toNum(pt.pan.x) === 0 && toNum(pt.pan.y) === 0))
    && toNum(pt.logScale) === 0 && toNum(pt.pitch) === 0 && toNum(pt.yaw) === 0
    && toNum(pt.roll) === 0;
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

// 6 · THE READINGS TAKEN ON REAL RECORDS, and they are readings of RECORDS rather than a census of
//     a collection. His word of 2026-08-18 09:51 strikes out counting how many pairs of some
//     collection reach anything — «не надо считать пары которые получает пакет» — so what stood
//     here, a double loop over all 14 520 ordered pairs asking how many composed and how many
//     declined, is gone with the question it answered. What is left is a settled handful of real
//     ordered pairs, walked so the per-record laws below stand on records that actually hang: every
//     driven handle names its measurement, no handle an instrument declares open is driven, the fold
//     spends the one miracle, the camera leads only at a tonic step, and every instrument the record
//     ships can be chosen. None of those is a count of a collection; each is a law about one
//     crossing, checked on enough crossings to catch a breach.
// HOW MANY CROSSINGS «ENOUGH» IS, and it is a measurement rather than a habit. The handful stood at
// 48 while the record published five instruments; on a field of sixteen, whose rarest plays about
// two cues in a hundred, 48 ordered pairs miss it about as often as they catch it — this suite read
// ««liquid» can never be chosen» off a spot of 48 while the same module casts it 2 948 times over
// the whole collection. Swept at 96, 144, 192, 240 and 363 pairs every one of the sixteen is cast;
// 192 is taken, which puts the rarest at 37 casts rather than at the edge of its own noise. The
// planted runs below still walk a corner of 24 — a plant that reddens needs one breach, not a
// margin.
const allIds = Object.keys(works.works).sort();
const SPOT = [];
for (let i = 0; i < (sweepN > 0 ? Math.min(sweepN, 192) : 192); i++) {
  const x = allIds[(i * 7) % allIds.length], y = allIds[(i * 13 + 3) % allIds.length];
  if (x !== y) SPOT.push([x, y]);
}
const ids = allIds;
const roads = {}, declines = {}, byRoad = {};
let composed = 0, declined = 0, maxBytes = 0, maxIntent = 0, overByte = 0, overIntent = 0;
let drivenUnmeasured = [], openDriven = [], drivenNoteMissing = [];
let intentShortened = 0, roadKept = 0, boxReasons = {};
let ledAtTonic = 0, ledElsewhere = 0, ledWithWorldCue = 0, tonic = 0;
// THE WITNESS CAMERA'S OWN FLIGHT (charter shelf 2), swept over the same real pairs every other
// row here stands on. `camChecked` counts every composed pair the axis check actually ran on;
// `camMismatches` keeps the first few disagreements between the composer's own written track and
// `camExpected()`'s independent re-derivation, so a red row shows what actually differs rather
// than only that something did; `camAllZeroCount` counts pairs whose whole middle came out at the
// neutral pose — a static camera again — which is the number his brief asks to be told rather than
// silently fixed; `camEndsBad` counts a pair whose "a" or "b" point was touched at all;
// `camFitMismatch` counts a pair whose score (post wire-fitting) carries a different track than its
// plan (pre-fitting); `camMaxTrackLen` is the longest track any composed pair wrote, measured
// against the client's own published camera-point fence.
let camChecked = 0, camMismatches = [], camAllZeroCount = 0, camEndsBad = 0, camFitMismatch = 0,
    camMaxTrackLen = 0;
const camDistinctTracks = new Set();
// THE VOICE LEVEL, swept over the same pairs. `camVoiceUnder` counts every composed pair whose
// carrying axis spends LESS of its own ceiling than the pair's own grain asks for — a flight the
// pictures cannot register — and `camVoiceWorst` keeps the widest few gaps so a red shows how far
// short rather than only that something is. `camVoiceShares` is the whole distribution, printed
// beside the row because his word was about what the flight LOOKS like, not about a count.
let camVoiceUnder = 0, camVoiceChecked = 0, camVoiceWorst = [];
const camVoiceShares = [];
// THE COLOUR AND LIGHT VOICES, swept the same way: every driven amp paired with the period and the
// phase the composer wrote beside it, so this file can compute the voice's own peak the way the
// lab's law does and count the ones that are declared but cannot be seen.
let voiceSilentDeclared = 0, voiceChecked = 0, voiceWorst = [];
// CHANGE A/B PROOF ROWS. `adriftSeams` pairs each `adrift` cue's own driven `seamA`/`seamB` against
// the two works' own recorded `structure.horizon.seam`, so the row below can prove the handle now
// carries the record's own strength rather than the old whole-or-nothing reading. `tideCellsSeen`
// collects every `waterline` cue's own driven `tideCells`, so the row below can prove it moves off
// the manifest's own 0.5 default instead of resting there on every pair.
let adriftSeams = [], tideCellsSeen = [];
// PART 1 OF THE GATE-SLOT LANE: gates' own slotPlace/slotHalf/slotAxis, off the departing work's
// own measured motifs.gatePlace/gateHalf/gateAxis (lab/step1-motifs.py's slot_on(), ported from
// the archived lab/effects/gates.js). Before this change none of the three was ever written by
// `fillPlan`, so `appliedValue` resolved every one to the manifest's own naive middle — slotAxis
// upright, slotPlace and slotHalf at the motif's own fixed band. Collected the same way
// `adriftSeams` proves seamA/seamB above: applied value paired against the record's own field, so
// the row below can prove both that the wire carries the record's own reading and that the reading
// differs across pairs.
let gateSlots = [];
// CHANGE D: strata-light's own levelA/levelB, off each work's own `luminance.level` (the median
// luminance lab/analyze/recipes.py:551-613 colour_stats() ports from `measure(image)`,
// lab/effects/strata-light.js:108-113). Before this change nothing ever wrote `wanted.levelA`/
// `wanted.levelB`, so both rested at the manifest's own 0.5 default on every pair; these collect
// every value the sweep actually sees so the row below can prove they now differ across pairs.
let levelASeen = [], levelBSeen = [];
// CHANGE C: the eighteen colour-and-light voice handles ported from lab/step4-assembler.js:1966-2010
// — grid-colour's six (one set, the module carries both works inside itself) and strata-light's
// twelve (two sets, A the departing work's own reading and B the arriving work's). Before this
// change every one of the eighteen rested at its manifest default of 0 for every pair; these
// collect every value the sweep actually sees so the rows below can prove they now differ across
// pairs instead of standing still.
const GC_VOICE_HANDLES = ["colourPeriod", "colourPhase", "colourAmp",
                          "lightPeriod", "lightPhase", "lightAmp"];
const SL_VOICE_HANDLES = ["colourPeriodA", "colourPhaseA", "colourAmpA",
                          "lightPeriodA", "lightPhaseA", "lightAmpA",
                          "colourPeriodB", "colourPhaseB", "colourAmpB",
                          "lightPeriodB", "lightPhaseB", "lightAmpB"];
// Bucketed by shelf 17's levels law (his correction of 2026-08-18, folded into this lane): a cue
// that OWNS LIGHT-COLOUR is where the eighteen handles must be driven and differ across pairs; a
// cue that only ACCOMPANIES another cue on that level must leave all of them at the manifest's own
// rest of 0, so the "owns" and "accompanies" collections are kept apart rather than merged.
const gridColourVoicesOwns = {}, strataLightVoicesOwns = {};
const gridColourVoicesAccompanies = {}, strataLightVoicesAccompanies = {};
for (const h of GC_VOICE_HANDLES) {
  gridColourVoicesOwns[h] = []; gridColourVoicesAccompanies[h] = [];
}
for (const h of SL_VOICE_HANDLES) {
  strataLightVoicesOwns[h] = []; strataLightVoicesAccompanies[h] = [];
}
// Reads one cue's own eighteen-handle slice, bucketed by shelf 17's own levels law rather than by
// the "requested" note the loop above filters on — an ACCOMPANYING cue's handles are never
// requested at all (`fillPlan` leaves them unset), so reading `node.value` directly here, per cue,
// is what lets the silent case be proven rather than merely absent. `cue.levelOwnership` is the
// composer's own resolution (`ownTheLevels`, threaded onto every cue in `buildTemplate` before
// `fillPlan` ever runs), read here exactly as it stands rather than re-derived.
//
// CALLED AT EVERY ROUTE ROLE, not only the sweep's own default-role request: strata-light plays
// PIVOT far more often than not, and `ownTheLevels` deprioritises the pivot cue on every level but
// SURFACE — a pivot cue loses LIGHT-COLOUR to any other cue of the same passage that also declares
// it, on every road, at every role. Sampled at one role alone (the sweep's own default) this
// instrument was found to win LIGHT-COLOUR zero times in 26 sightings over 192 pairs; sampled at
// all five roles the same 192 pairs give it many more chances to be cast ALONE on its level, which
// is the only way a pivot cue wins it.
function collectVoiceHandles(cue) {
  if (cue.instrument.id !== "grid-colour" && cue.instrument.id !== "strata-light") return;
  const owns = !!(cue.levelOwnership && cue.levelOwnership["LIGHT-COLOUR"] === "owns");
  const handles = cue.instrument.id === "grid-colour" ? GC_VOICE_HANDLES : SL_VOICE_HANDLES;
  const ownsBucket = cue.instrument.id === "grid-colour" ? gridColourVoicesOwns
                                                         : strataLightVoicesOwns;
  const accBucket = cue.instrument.id === "grid-colour" ? gridColourVoicesAccompanies
                                                        : strataLightVoicesAccompanies;
  const bucket = owns ? ownsBucket : accBucket;
  for (const h of handles) {
    const node = cue.nodes[cue.id + "-" + h];
    if (node) bucket[h].push(toNum(startValue(node)));
  }
  // IS A DECLARED VOICE ACTUALLY SEEN. Each amp is read beside the period and the phase written on
  // the same cue, which is everything the lab's own peak needs; a voice driven at nothing is not
  // declared at all and is passed over here, exactly as the lab's own mute leaves the three handles
  // unwritten rather than writing a zero.
  if (!owns) return;
  for (const h of handles) {
    if (h.indexOf("Amp") < 0) continue;
    const stem = h.slice(0, h.indexOf("Amp")), tail = h.slice(h.indexOf("Amp") + 3);
    const ampN = cue.nodes[cue.id + "-" + h];
    const perN = cue.nodes[cue.id + "-" + stem + "Period" + tail];
    const phaN = cue.nodes[cue.id + "-" + stem + "Phase" + tail];
    if (!ampN || !perN) continue;
    const amp = toNum(startValue(ampN));
    if (!(amp > 0)) continue;
    const seen = amp * voicePeakShare(toNum(startValue(perN)),
                                      phaN ? toNum(startValue(phaN)) : 0) * 255;
    voiceChecked++;
    if (seen < VOICE_TARGET_255) {
      voiceSilentDeclared++;
      if (voiceWorst.length < 5) {
        voiceWorst.push({instrument: cue.instrument.id, handle: h,
                         amp: Math.round(amp * 10000) / 10000,
                         seen: Math.round(seen * 100) / 100});
      }
    }
  }
}
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
{
  for (const [xi, yi] of SPOT) {
    const wa = works.works[xi], wb = works.works[yi];
    const dir = xi < yi ? "a-to-b" : "b-to-a";
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
    // THE WITNESS CAMERA'S OWN FLIGHT, CHECKED ON THIS PAIR. `fromWork`/`toWork` take the same
    // b-to-a flip `adriftSeams` above takes, because the composer's own `fromW`/`toW` do.
    {
      const fromWork = dir === "b-to-a" ? wb : wa, toWork = dir === "b-to-a" ? wa : wb;
      const track = (p.plan.camera || {}).track || [];
      if (track.length > camMaxTrackLen) camMaxTrackLen = track.length;
      if (track.length === 4) {
        camChecked++;
        if (!camNeutral(track[0]) || !camNeutral(track[3])) camEndsBad++;
        const exp = camExpected(fromWork, toWork);
        const got1 = track[1], got2 = track[2];
        const close = (a, b) => Math.abs(toNum(a) - b) < 0.0006;
        const nz = (v) => Math.abs(toNum(v)) > 1e-9;
        // WHICH AXIS THE COMPOSER ACTUALLY CARRIED, read off its own output — the palindrome ban's
        // tie-break is the composer's own die and is not reproduced here (see the note above
        // camExpected). At most one of roll/yaw/pitch may be non-zero at either point; that
        // invariant is asserted directly rather than assumed.
        const carried = (nz(got1.roll) || nz(got2.roll)) ? "roll"
          : (nz(got1.yaw) || nz(got2.yaw)) ? "yaw"
          : (nz(got1.pitch) || nz(got2.pitch)) ? "pitch" : "none";
        const singleExcursion = ["roll", "yaw", "pitch"].filter((ax) =>
          nz(got1[ax]) || nz(got2[ax])).length <= 1;
        const expRoll = carried === "roll" ? [exp.rollRaw, exp.rollRaw * exp.rollFraction] : [0, 0];
        const expYaw = carried === "yaw" ? [exp.yawRaw, exp.yawRaw * exp.yawFraction] : [0, 0];
        const pitchTied = exp.pitchFrom === exp.pitchTo && exp.pitchFrom !== 0;
        const expPitch = carried === "pitch"
          ? [exp.pitchFrom, pitchTied ? exp.pitchInTied : exp.pitchTo] : [0, 0];
        const ok = singleExcursion
          && close(got1.pan.x, exp.panFrom[0]) && close(got1.pan.y, exp.panFrom[1])
          && close(got2.pan.x, exp.panTo[0]) && close(got2.pan.y, exp.panTo[1])
          && close(got1.logScale, exp.logScale) && close(got2.logScale, exp.logScale)
          && close(got1.roll, expRoll[0]) && close(got2.roll, expRoll[1])
          && close(got1.yaw, expYaw[0]) && close(got2.yaw, expYaw[1])
          && close(got1.pitch, expPitch[0]) && close(got2.pitch, expPitch[1]);
        if (!ok && camMismatches.length < 5) {
          camMismatches.push({key, expected: exp,
                              got: {p1: {pan: {x: toNum(got1.pan.x), y: toNum(got1.pan.y)},
                                         logScale: toNum(got1.logScale), roll: toNum(got1.roll),
                                         yaw: toNum(got1.yaw), pitch: toNum(got1.pitch)},
                                    p2: {pan: {x: toNum(got2.pan.x), y: toNum(got2.pan.y)},
                                         logScale: toNum(got2.logScale), roll: toNum(got2.roll),
                                         yaw: toNum(got2.yaw), pitch: toNum(got2.pitch)}}});
        }
        if (camNeutral(got1) && camNeutral(got2)) camAllZeroCount++;
        camDistinctTracks.add(JSON.stringify([got1, got2]));
        // THE CARRYING AXIS'S OWN LEVEL, against the level the pair's own grain sets. The share is
        // taken against each axis's own ceiling, which is the composer's own comparison unit for
        // the three (roll and yaw reach DOLLY_CAP, pitch half of it) and the only one in which the
        // three are comparable at all.
        if (carried !== "none") {
          const ceiling = carried === "pitch" ? 0.5 * DOLLY_CAP : DOLLY_CAP;
          const worn = Math.max(Math.abs(toNum(got1[carried])), Math.abs(toNum(got2[carried])));
          const share = ceiling > 0 ? worn / ceiling : 0;
          const floorAsked = camVoiceFloor(fromWork, toWork);
          camVoiceChecked++;
          camVoiceShares.push(Math.round(share * 10000) / 10000);
          // The written value is rounded to four places, which on the tighter of the two ceilings
          // is worth two ten-thousandths of a share; the reading is allowed that much and no more.
          if (share + 5e-4 < floorAsked) {
            camVoiceUnder++;
            if (camVoiceWorst.length < 5) {
              camVoiceWorst.push({key, axis: carried,
                                  share: Math.round(share * 10000) / 10000,
                                  asked: Math.round(floorAsked * 10000) / 10000});
            }
          }
        }
        if (p.score && p.score.camera
            && JSON.stringify(p.score.camera.track) !== JSON.stringify(p.plan.camera.track)) {
          camFitMismatch++;
        }
      }
    }
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
      // CHANGE C, at every role: see `collectVoiceHandles`'s own note on why one role's sample
      // undercounts a pivot instrument's chances to own LIGHT-COLOUR. Read off `q.plan.cues`, not
      // `q.score.cues`, for the same reason the note above `p.plan.cues` gives — the wire-fitting
      // step sheds provenance and `levelOwnership` survives only on the plan's own copy.
      for (const cue of q.plan.cues) collectVoiceHandles(cue);
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
    //
    // THIS READS `p.plan.cues`, THE COMPOSER'S OWN FILLED PLAN, AND NOT `p.score.cues`, THE SERIALISED
    // AND WEIGHT-FITTED WIRE FORM. `fitTheWeight` (pass-composer.js) sheds every node's own note —
    // ALL of them, on the whole score, in one pass — whenever the serialised score stands over the
    // client's byte fence, which is the very fitting the byte-fence row above proves works. That
    // fitting is real and correct and has nothing to do with what this row asks: whether the
    // composer NAMED a measurement for a handle it drove, which is a fact about the plan the composer
    // built, not about how much of its own provenance prose survived being fitted onto the wire. On
    // the twenty-two-instrument field a folding score (waterline+tilt+matter, say) crosses that fence
    // often enough that reading `score.cues` here left every note-bearing row starved regardless of
    // which instrument was cast — `plan` and `score` hold separate deep copies of the same cues
    // (`serialise`'s own `copy()`), so `plan.cues[*].nodes[*].note` carries what the composer wrote
    // whether or not the wire form later lost it.
    for (const cue of p.plan.cues) {
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
        // CHANGE A: the drifting instrument's own seamA/seamB, read against the two works' own
        // recorded structure.horizon.seam — proves the handle carries the record's own strength.
        if (cue.instrument.id === "adrift" && (handle === "seamA" || handle === "seamB")) {
          // `seamA` reads the DEPARTING work, `seamB` the arriving one, and which of wa/wb departs
          // flips with direction (fromW = direction === "b-to-a" ? b : a, pass-composer.js:1898) —
          // the same flip the composer itself takes, so this must take it too or a b-to-a pair
          // would compare seamA against the wrong work's own record.
          const fromWork = dir === "b-to-a" ? wb : wa, toWork = dir === "b-to-a" ? wa : wb;
          const rec = handle === "seamA" ? fromWork : toWork;
          adriftSeams.push({ handle, applied: toNum(startValue(node)),
                             recordSeam: toNum((rec.structure.horizon || {}).seam) });
        }
        // CHANGE B: the waterline instrument's own tideCells — proves it moves off its 0.5 default.
        if (cue.instrument.id === "waterline" && handle === "tideCells") {
          tideCellsSeen.push(toNum(startValue(node)));
        }
        // CHANGE D: strata-light's own levelA/levelB — proves each moves off its 0.5 default.
        if (cue.instrument.id === "strata-light" && handle === "levelA") {
          levelASeen.push(toNum(startValue(node)));
        }
        if (cue.instrument.id === "strata-light" && handle === "levelB") {
          levelBSeen.push(toNum(startValue(node)));
        }
        // GATE-SLOT LANE PART 1: gates' slotPlace/slotHalf/slotAxis all read the DEPARTING work
        // only (pass-inst-gates.js: "the departing work's own slot is what parts"), so the record
        // compared against is `fromWork` under the same b-to-a flip `adriftSeams` above takes.
        if (cue.instrument.id === "gates"
            && (handle === "slotPlace" || handle === "slotHalf" || handle === "slotAxis")) {
          var gFromWork = dir === "b-to-a" ? wb : wa;
          var gMot = gFromWork.motifs || {};
          var gRecord = handle === "slotPlace" ? gMot.gatePlace
            : handle === "slotHalf" ? gMot.gateHalf
            : (gMot.gateAxis === "vertical" ? 1 : (gMot.gateAxis === "horizontal" ? 0 : null));
          gateSlots.push({ handle: handle, applied: toNum(startValue(node)), record: gRecord });
        }
      }
      collectVoiceHandles(cue);
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
out.sweep = {works: allIds.length, ordered: SPOT.length, composed, declined,
             roads, declines, byRoad, maxBytes, maxIntent, overByte, overIntent,
             byteCap: BYTE_CAP, intentCap: INTENT_CAP,
             drivenUnmeasured: drivenUnmeasured.sort(), openDriven: openDriven.sort(),
             drivenNoteMissing: drivenNoteMissing.slice(0, 4),
             intentShortened, roadKept, boxReasons,
             ledAtTonic, ledElsewhere, ledWithWorldCue, tonic,
             folded, worldCue, ledAndWorld, twoMiracles, roleThrew, roleN, boxQualified,
             foldUnspent, chosen, cast: Object.keys(consts.instruments).sort(),
             adriftSeams, tideCellsSeen, levelASeen, levelBSeen, gateSlots,
             gridColourVoicesOwns, strataLightVoicesOwns,
             gridColourVoicesAccompanies, strataLightVoicesAccompanies};
out.camera = {checked: camChecked, mismatches: camMismatches, allZero: camAllZeroCount,
              endsBad: camEndsBad, fitMismatch: camFitMismatch, maxTrackLen: camMaxTrackLen,
              trackPointCap: CAMERA_POINT_CAP, distinctTracks: camDistinctTracks.size,
              dollyCap: DOLLY_CAP,
              voiceChecked: camVoiceChecked, voiceUnder: camVoiceUnder, voiceWorst: camVoiceWorst,
              voiceShares: camVoiceShares.sort((p, q) => p - q)};
out.voices = {checked: voiceChecked, silentDeclared: voiceSilentDeclared, worst: voiceWorst,
              target255: VOICE_TARGET_255};

// 7 · the road every pair is measured against, and the one road no instrument can play
const roadNotes = {};
for (const n of forward.roadNotes) roadNotes[n.road] = {ok: n.ok, why: n.why};
out.roadNotes = roadNotes;

// 8 · THE ROUTE'S OWN SPREAD. A derivation can be broad and what a person SEES narrow: seven roads
//     that all arrive at one instrument fail his 19:13 word about a route's breadth exactly as
//     surely as one road would. So this casts routes the way the walk casts them — 22 works, 21
//     edges, the first step an entrance, the widest gap after it the culmination, the step before
//     that a middle, every local maximum a middle and the rest quiet links — and measures what
//     reaches the eye. The kinship vectors that decide the ORDER live in the walk, so the order and
//     the gaps are sampled here on a pinned seed rather than read.
const ROUTES = [];
let rseed = 20260818;
function rnd() { rseed = (rseed * 1103515245 + 12345) & 0x7fffffff; return rseed / 0x7fffffff; }
{
  const all = Object.keys(works.works).sort();
  for (let r = 0; r < 40; r++) {
    const pick = all.slice();
    for (let i = pick.length - 1; i > 0; i--) {
      const k = Math.floor(rnd() * (i + 1));
      const t = pick[i]; pick[i] = pick[k]; pick[k] = t;
    }
    const hang = pick.slice(0, 22), gaps = [];
    for (let i = 0; i + 1 < hang.length; i++) gaps.push(rnd());
    let crest = gaps.length > 1 ? 1 : 0;
    for (let i = crest + 1; i < gaps.length; i++) if (gaps[i] > gaps[crest]) crest = i;
    const roles = gaps.map((g, i) => {
      if (i === crest) return "culmination";
      if (i === crest - 1) return "middle";
      const before = i > 0 ? gaps[i - 1] : -Infinity;
      const after = i + 1 < gaps.length ? gaps[i + 1] : -Infinity;
      return (g > before && g > after) ? "middle" : "quiet link";
    });
    roles[0] = "entrance";
    ROUTES.push({ hang, roles });
  }
}
// THE SAME ROUTES, WALKED TWICE. Once BLIND — every step asked in isolation, which is every reading
// this section ever took — and once with the route's own memory: at each step the walk hands back the
// letters it has already played, most recent first, exactly as `passRoutePlayed` in the client does.
// Charter shelf 16 puts the letter cooldowns INSIDE the dice, between the base weights and the roll,
// and his 19:13 word about a route's breadth is what they serve. The two readings stand side by side
// so the row below can measure the cooldown's own effect rather than a fence's.
function walkRoutes(withMemory) {
  let shapesSum = 0, shapesMax = 0, shareSum = 0, shareMax = 0, casted = 0, stepsRun = 0, lost = 0;
  const spread = {};
  for (const R of ROUTES) {
    const seen = new Set(), per = {};
    let n = 0;
    const played = [];
    for (let i = 0; i + 1 < R.hang.length; i++) {
      const x = R.hang[i], y = R.hang[i + 1], fwd = x <= y;
      const A = works.works[fwd ? x : y], B = works.works[fwd ? y : x];
      const key = A.id + "__" + B.id + "__" + (fwd ? "ab" : "ba");
      stepsRun++;
      const req = { workRecordA: A, workRecordB: B,
                    direction: fwd ? "a-to-b" : "b-to-a",
                    seed: die(key), routeRole: R.roles[i] };
      if (withMemory) req.walkMemory = played.slice();
      let p = null;
      try {
        p = composer.passageFor(req);
      } catch (e) { continue; }
      if (!p.score) { lost++; continue; }
      casted++; n++; seen.add(p.shape);
      const step = [p.genre];
      for (const cue of p.score.cues) {
        per[cue.instrument.id] = (per[cue.instrument.id] || 0) + 1;
        spread[cue.instrument.id] = (spread[cue.instrument.id] || 0) + 1;
        step.push(cue.instrument.id);
      }
      played.unshift.apply(played, step);
    }
    shapesSum += seen.size;
    if (seen.size > shapesMax) shapesMax = seen.size;
    const worst = Math.max.apply(null, Object.keys(per).map((k) => per[k]).concat([0]))
      / Math.max(n, 1);
    shareSum += worst;
    if (worst > shareMax) shareMax = worst;
  }
  const tot = Object.keys(spread).map((k) => spread[k]).reduce((a, b) => a + b, 0) || 1;
  const share = {};
  for (const k of Object.keys(spread).sort()) share[k] = Math.round(1000 * spread[k] / tot) / 10;
  return { routes: ROUTES.length, steps: stepsRun, composed: casted, lost: lost,
           shapesMean: Math.round(10 * shapesSum / ROUTES.length) / 10, shapesMax,
           topShareMean: Math.round(1000 * shareSum / ROUTES.length) / 10,
           topShareWorst: Math.round(1000 * shareMax) / 10, spread: share,
           letters: Object.keys(spread).length };
}
out.route = walkRoutes(false);
out.routeRemembered = walkRoutes(true);

// 9 · the composer measures its line against the number it is HANDED, not against its fallback.
//     The constants are handed a cap of their own and the longest line the composer writes has to
//     fall under it — which is the wire the bake's `intentChars` travels, proved without planting.
const handed = joined.make(Object.assign({}, fix.consts, {intentFenceChars: 300}));
let handedMax = 0, handedShort = 0, handedN = 0, handedRoadKept = 0;
{
  for (const [xi, yi] of SPOT) {
    const wa = works.works[xi], wb = works.works[yi];
    const dir = xi < yi ? "a-to-b" : "b-to-a";
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

// 10 · WHAT THE ENTRY DOES WITH A REQUEST IT CANNOT READ AS SENT. Three of these were refusals by
//      name until 2026-08-18 and each cost the visitor a whole crossing for a field; they are
//      defaults now, and what could not be read stands on the request under `unread` so a walk
//      sending a stray value can still be found. The two that remain are the two that say there is
//      no PAIR.
const ask = (extra) => {
  const p = composer.passageFor(Object.assign(
    {workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB]}, extra));
  return {declined: p.declined || null, composed: !!p.json,
          unread: (p.request && p.request.unread) || null,
          role: p.request && p.request.routeRole, seed: p.request && p.request.seed,
          memory: p.request && p.request.sessionMemory,
          walk: (p.request && p.request.walkMemory) || null};
};
// A half-pair is asked through its own reader, because the fence that catches it is the ONE fence
// left in the entry and what stands behind that fence is arithmetic over two records. With the
// fence in place the answer is the refusal's own sentence; with it planted away the request reaches
// the pair arithmetic and dies there, and the reader carries that back rather than losing the run.
const refusalFor = (req) => {
  try { return composer.passageFor(req).declined || null; }
  catch (e) { return "threw inside the pair arithmetic: " + ((e && e.message) || String(e)); }
};
out.fences = {
  role: ask({routeRole: "grand finale"}),
  memory: ask({sessionMemory: {family: "band", seed: 1, passIndex: 2, cooldown: 9}}),
  memoryOk: ask({sessionMemory: {family: "band", seed: 1, passIndex: 2}}),
  seedHigh: ask({seed: 9}),
  seedLow: ask({seed: -1}),
  walkNotAList: ask({walkMemory: "unfold"}),
  walkStray: ask({walkMemory: ["unfold", 7, null, "weave"]}),
  walkOk: ask({walkMemory: ["unfold", "weave"]}),
  noA: refusalFor({workRecordA: {}, workRecordB: B, direction: "a-to-b", seed: 1}),
  noB: refusalFor({workRecordA: A, workRecordB: {}, direction: "a-to-b", seed: 1}),
};

// 11 · THE HARD RECORDS, AND THIS IS THE ROW THE LANE STANDS ON. His word of 2026-08-18 09:51: any
//      two photographs in the world get a crossing, always. It is proved on RECORDS rather than on
//      a collection, because a collection is a sample and a record is a case — so the cases here are
//      the ones deliberately built to be the worst a composer could be handed, and each is asked at
//      every route role, in both directions, on three dice. Every one has to come back playable: a
//      score of schema 2 with at least one cue, every cue naming an instrument, its authored line
//      inside the client's own character fence and its whole weight inside the client's own byte
//      fence. A single input yielding nothing reddens this row.
function bareRecord(id) {
  return { id: id, frameSide: 1000.0, door: {}, luminance: {}, measures: {}, motifs: {},
           palette: {}, readiness: [0, 0], sets: [], structure: {}, texture: {} };
}
function fullRecord(id, o) {
  const w = {
    id: id, frameSide: 1000.0,
    door: { angleDeg: 0, device: "rings", elementKind: "ring", level: "CELL", pieces: 8,
            stepPx: 40.0 },
    luminance: {},
    measures: { banding: 0, dominant_object: 0, grid: 0, named_objects: 0, radial: 0, regions: 0,
                texture: 0 },
    motifs: { gateGap: 0, measured: [], radialCentre: [0.5, 0.5], voidShare: 0 },
    // `colourfulness`, renamed from `luminance.ladderPosition` (the judge seat's standing
    // correction of 2026-08-18/19): `o.ladder` keeps its own name, unused by any caller in this
    // file, its default of 0.5 unchanged.
    palette: { hueConcentration: 0.5, hues: [], rung: "one",
               colourfulness: o.ladder === undefined ? 0.5 : o.ladder },
    readiness: [0.5, 100.0, "vertical"],
    sets: o.sets || [],
    structure: {
      banding: { axis: "vertical", periodPx: 100.0, score: 0 },
      dominantObject: { bbox: [0.25, 0.25, 0.75, 0.75], score: 0 },
      grid: { angleDeg: 0, periodPx: 100.0, score: 0 },
      horizon: { y: 0.5 },
      ownDevice: { angleDeg: 0, confidence: 0, count: 4, kind: "rings", pieces: 4, stepPx: 40.0 },
      polar: { planet: 0, radial_streak: 0, tunnel: 0, twirl: 0 },
      radial: { centre: [0.5, 0.5], score: 0, subType: "none" },
      regions: { count: 0, score: 0 },
      rotational: { n: 0, score: 0 }
    },
    texture: { detailPx: 2.0, scoreFromCutLines: 0, spectralPeriodPx: 100.0 }
  };
  for (const k of Object.keys(o.measures || {})) w.measures[k] = o.measures[k];
  for (const k of Object.keys(o.structure || {})) {
    for (const f of Object.keys(o.structure[k])) w.structure[k][f] = o.structure[k][f];
  }
  return w;
}
const HARD = {
  // Two records sharing no measured structure at all: one reads only on bands, the other only on
  // tiles, and every other measure of each stands at nothing.
  "two works sharing no measured structure": [
    fullRecord("bands-only", { measures: { banding: 0.9 },
      structure: { banding: { score: 0.9, axis: "vertical" } },
      sets: [{ count: 4, fig: null, index: 1, kind: "strip", measuredGrain: 250, mergeFactor: 1,
               provider: "structural", realCount: 4 }] }),
    fullRecord("tiles-only", { measures: { grid: 0.9 }, structure: { grid: { score: 0.9 } },
      sets: [{ count: 9, fig: null, index: 2, kind: "tile", measuredGrain: 0, mergeFactor: 1,
               provider: "structural", realCount: 9 }] })
  ],
  // A record with almost every measurement near zero.
  "a record with almost every measurement at nothing": [
    fullRecord("flat", {}),
    fullRecord("ordinary", { measures: { banding: 0.4, radial: 0.3 },
      structure: { banding: { score: 0.4 }, radial: { score: 0.3 } },
      sets: [{ count: 3, fig: null, index: 3, kind: "strip", measuredGrain: 300, mergeFactor: 1,
               provider: "structural", realCount: 3 }] })
  ],
  // Two identical records — one photograph crossing to itself.
  "two identical records": [
    fullRecord("twin", { measures: { banding: 0.6 }, structure: { banding: { score: 0.6 } } }),
    fullRecord("twin", { measures: { banding: 0.6 }, structure: { banding: { score: 0.6 } } })
  ],
  // A record missing every optional field.
  "a record missing its optional fields": [
    bareRecord("bare"),
    fullRecord("ordinary", { measures: { banding: 0.4 }, structure: { banding: { score: 0.4 } } })
  ],
  // Two records with nothing measured about either of them at all.
  "two records with nothing measured at all": [bareRecord("bare-a"), bareRecord("bare-b")]
};
{
  const rows = {};
  let asked = 0, playable = 0;
  const failures = [];
  for (const name of Object.keys(HARD)) {
    const [ha, hb] = HARD[name];
    for (const role of composer.routeRoles) {
      for (const dir of ["a-to-b", "b-to-a"]) {
        for (const seed of [0, 3.1, 7.9]) {
          asked++;
          let q = null;
          try {
            q = composer.passageFor({workRecordA: ha, workRecordB: hb, direction: dir,
                                     routeRole: role, seed: seed});
          } catch (e) {
            failures.push(name + " / " + role + " / " + dir + " / " + seed + ": threw "
                          + String(e && e.message).slice(0, 90));
            continue;
          }
          const s2 = q && q.score;
          if (!s2) {
            failures.push(name + " / " + role + " / " + dir + " / " + seed + ": "
                          + ((q && q.declined) || "nothing came back"));
            continue;
          }
          if (s2.schema !== 2 || !s2.cues.length
              || s2.cues.some((c) => !c.instrument || !c.instrument.id)) {
            failures.push(name + " / " + role + " / " + dir + " / " + seed + ": no playable cue");
            continue;
          }
          if (String(s2.intent || "").length > INTENT_CAP) {
            failures.push(name + " / " + role + ": the line runs to " + s2.intent.length);
            continue;
          }
          if (q.bytes > BYTE_CAP) {
            failures.push(name + " / " + role + ": the score weighs " + q.bytes);
            continue;
          }
          playable++;
          if (!rows[name] && role === "middle" && dir === "a-to-b" && seed === 3.1) {
            rows[name] = {genre: q.road, fit: q.genreFit,
                          cues: s2.cues.map((c) => c.id + ":" + c.instrument.id).join(","),
                          duration: s2.duration, bytes: q.bytes,
                          stood: (q.stood || []).length};
          }
        }
      }
    }
  }
  out.hard = {asked, playable, failures: failures.slice(0, 6), rows,
              cases: Object.keys(HARD).length};
}

// 12 · EVERY GENRE ANSWERS FOR EVERY PAIR, with a fit and the sentence naming what it read. Nothing
//      is qualified and nothing is turned away, so the vocabulary is whole on the hardest record in
//      hand as much as on a real pair.
{
  const seen = {};
  const [ba, bb] = HARD["two records with nothing measured at all"];
  const bareRun = composer.passageFor({workRecordA: ba, workRecordB: bb, seed: 1});
  const realRun = composer.passageFor({workRecordA: A, workRecordB: B, seed: fix.seeds[KEY_AB]});
  const shaped = (r) => (r.roadNotes || []).map((n) => ({genre: n.genre || n.road, fit: n.fit,
                                                         said: !!n.why}));
  out.vocabulary = {
    onBare: shaped(bareRun), onReal: shaped(realRun),
    barePlayed: bareRun.road, realPlayed: realRun.road,
    everyGenreSaidSomething: shaped(bareRun).every((g) => g.said)
                             && shaped(realRun).every((g) => g.said),
    ranking: realRun.ranking || null
  };
}

console.log(JSON.stringify(out));
"""

DRIVER_PATH = TMP / "composed-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_run(plants=(), sweep=0):
    # The client's own two fences travel to the driver rather than being restated inside it, which
    # is anchor 1 of the four the docstring names.
    env = dict(os.environ, PLANTS=json.dumps(list(plants)), SWEEP=str(sweep),
               CLIENT_CAPS=json.dumps({"bytes": CLIENT_BYTES, "intent": CLIENT_INTENT,
                                       "cameraPoints": CLIENT_CAMERA_POINTS,
                                       "dollyCap": DOLLY_CAP_VALUE}))
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

        # --- row 0 · every genre answers, with a fit and a reading -----------------------------
        # WHAT THIS ROW USED TO ASK, AND WHY THE QUESTION CHANGED. It asked whether each of the seven
        # roads QUALIFIED at least one real pair — a question that only makes sense while a road can
        # turn a pair away. Since 2026-08-18 none can: every genre answers for every pair with a fit
        # between nothing and whole, and the die runs over the ranking. So the row asks what the
        # contract actually promises — that the vocabulary is whole for any pair, including a pair
        # of records with nothing measured about either of them, and that every genre says what it
        # read whatever its fit.
        v = got["vocabulary"]
        namesOnBare = sorted(g["genre"] for g in v["onBare"])
        namesOnReal = sorted(g["genre"] for g in v["onReal"])
        check(NODE_ROWS[0],
              namesOnBare == sorted(ROADS) and namesOnReal == sorted(ROADS)
              and v["everyGenreSaidSomething"],
              f"the whole vocabulary answers on two records with nothing measured at all "
              f"({len(namesOnBare)} genres, played «{v['barePlayed']}») and on a real pair "
              f"({len(namesOnReal)} genres, played «{v['realPlayed']}»); every one carries the "
              f"sentence naming what it read: {v['everyGenreSaidSomething']}. The real pair's own "
              f"ranking: " + json.dumps(v["ranking"], ensure_ascii=False))

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
        check(NODE_ROWS[5], len(d["distinct"]) > 1 and d["pinnedRepeats"],
              f"seventeen dice over one pair chose {d['distinct']}; a pinned die reproduces its own "
              f"run: {d['pinnedRepeats']}")

        # --- row 4 · what reaches the eye on a cast route ----------------------------------------
        # THE SHARE, AND WHY IT IS THIS NUMBER. Over 300 cast routes the commonest instrument carries
        # 59.1 percent of a route's steps on average; the project's own convention is a fence just
        # above the measured figure, so it stands at 65. The reading it guards is not a near miss:
        # when the ground was gated on the collection's top quartile the same measurement read 91.9
        # percent — one instrument in nine steps of ten — which is the state the judge saw on the
        # filmed route, matter in 15 of 17 passages. The MEAN is what the row holds because it is
        # stable over routes; the worst single route is printed beside it as a reading, since a short
        # route of mostly quiet links can be carried by one instrument without anything being wrong.
        rt = got["route"]
        check(NODE_ROWS[4],
              rt["topShareMean"] <= 65.0 and rt["shapesMean"] >= 7.0,
              f"over {rt['routes']} cast routes of 21 steps: {rt['shapesMean']} distinct shapes on "
              f"average and {rt['shapesMax']} at most; the commonest instrument carries "
              f"{rt['topShareMean']}% of a route on average (fence 65%) and {rt['topShareWorst']}% "
              f"on the most one-sided single route; the spread across every step is "
              + json.dumps(rt["spread"], ensure_ascii=False))

        # --- row 4 · the camera-led passage ------------------------------------------------------
        check(NODE_ROWS[6],
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
        check(NODE_ROWS[7], not bad and told >= 3,
              "; ".join(f"{k}: {v.get('road')} {v.get('tier')} {v.get('duration')} ms "
                        f"{v.get('cues')}" for k, v in roles.items())
              + f" — {told} distinct scores over one pair"
              + ("; " + "; ".join(bad) if bad else ""))

        # --- row 5 · the family the composer hands back is the walk's own ------------------------
        m = got["memory"]
        agree = (m["saidForward"] == m["walkForward"] and m["saidBack"] == m["walkBack"]
                 and m["saidAgain"] == m["walkAgain"])
        check(NODE_ROWS[8], agree and bool(m["walkForward"]),
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
        check(NODE_ROWS[9],
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
        check(NODE_ROWS[10],
              not sweep["drivenUnmeasured"] and not sweep["drivenNoteMissing"],
              f"over {sweep['composed']} composed passages of the real collection, every driven "
              f"handle's own note names its measurement; handles driven from something no "
              f"measurement bears on: {sweep['drivenUnmeasured']}")

        # --- row 8 · the open handle ------------------------------------------------------------
        check(NODE_ROWS[11], not sweep["openDriven"],
              f"handles the instruments declare open that the composer drove: "
              f"{sweep['openDriven']} — the woven balance is the one at stake, and at a door that "
              f"state is the instrument's own reading of the buffer (his 18:00 decision)")

        # --- row 8b · CHANGE A: adrift's seamA/seamB read the record's own seam strength ---------
        # Before this change the drifting instrument's seamA/seamB were driven off `carriesSeam`,
        # a 0-or-1 reading of whether a work's motif list carries the waterline motif at all. The
        # fix reads `structure.horizon.seam` — lab/step1-motifs.py:347-360's own score — instead, so
        # this row asks two things of the sweep: every applied value equals the record's own seam
        # (proving the wire, not a stand-in), and the values seen are not confined to {0, 1} (proving
        # the strength survived rather than being read back down to presence-or-absence).
        seams = sweep["adriftSeams"]
        seamMismatch = [s for s in seams
                         if abs(s["applied"] - (s["recordSeam"] or 0)) > 0.0002]
        seamValues = sorted(set(s["applied"] for s in seams))
        onlyBinary = seamValues and all(v in (0, 1) for v in seamValues)
        check(NODE_ROWS[35],
              bool(seams) and not seamMismatch and not onlyBinary,
              f"{len(seams)} adrift seamA/seamB readings over the sweep, {len(seamMismatch)} off "
              f"the record's own structure.horizon.seam by more than 0.0002; distinct values seen: "
              f"{seamValues[:12]}" + (" …" if len(seamValues) > 12 else ""))

        # --- row 8c · CHANGE B: waterline's tideCells is driven off the record's own grain -------
        # Before this change nothing ever wrote `wanted.tideCells`, so `appliedValue` resolved it to
        # the manifest's own 0.5 default on every pair — HANDLE_SOURCE's own row for it named a
        # measurement the composer never read. The fix positions the departing work's own grain
        # (said as cells across its frame) against the arriving work's, the same uncalibrated-ratio
        # idiom `grain`/`squeeze` already take on this exact reading. This row asks the sweep for at
        # least one value off the 0.5 default and more than one distinct value, so a fix that always
        # lands on one new constant cannot pass it either.
        tc = sweep["tideCellsSeen"]
        tcOffDefault = [v for v in tc if abs(v - 0.5) > 1e-9]
        check(NODE_ROWS[36],
              bool(tc) and bool(tcOffDefault) and len(set(tc)) > 1,
              f"{len(tc)} waterline tideCells readings over the sweep, {len(tcOffDefault)} off the "
              f"manifest's own 0.5 default; distinct values seen: {sorted(set(tc))[:12]}")

        # --- row 8d · CHANGE C: grid-colour's six voice handles are driven where it OWNS ------------
        #     LIGHT-COLOUR, not left at 0
        # Before this change nothing ever wrote `wanted.colourPeriod` et al. for this instrument, so
        # `appliedValue` resolved every one of the six to the manifest's own 0 default on every pair.
        # The fix reads the departing work's own colour.sat and colour.contrast (PART 2, step 4 of
        # the colour-and-light lane) — but ONLY on the cue the composer's own `ownTheLevels` marks
        # as owning LIGHT-COLOUR (shelf 17's levels law: one active voice per level). This row reads
        # the "owns" bucket only; the sibling row below reads the "accompanies" bucket and proves the
        # opposite half of the same law.
        #
        # PERIOD AND AMPLITUDE READ A MEASUREMENT AND SO MUST DIFFER ACROSS PAIRS: each is the
        # departing work's own colour.sat or colour.contrast carried through BEAT_DIAL/VOICE_SHARE,
        # and Part 1's own sweep found 111 and 107 distinct readings of those two measures over the
        # 121 works, so a period or an amplitude landing on one value across the whole spot-check
        # would itself be the defect.
        #
        # PHASE DOES NOT, AND THAT IS THE LAB'S OWN LAW RATHER THAN A GAP IN THE PORT. A voice's phase
        # is its own fixed place among this instrument's voices (`i / N`, step4-assembler.js:2000),
        # never the work's own measure — the lab's own code sets `s.phase = i / 4` with no per-pair
        # term in it either. So this row proves phase is DRIVEN (present in the collection at all,
        # which an undriven handle could not be) and CORRECT (holds exactly its own structural
        # constant, 0 for colour and 1/2 for light), not that it varies, because the law it ports
        # says it must not.
        # AMENDED 2026-08-24, when the lab's own audibility pass landed in the composer. A voice the
        # work cannot sing loudly enough to be seen is not declared at all, and the lab's own words
        # are the reason: «Заявленный и неслышный голос — пустое утверждение разбора». Its three
        # handles are then left unwritten and rest at the manifest's own 0, phase included — so a
        # phase reading of 0 where the constant is not 0 is a MUTED voice rather than a wrong one.
        # The row reads that distinction instead of forbidding it, and in doing so proves something
        # the old form could not: that a mute is whole. A voice never goes silent by halves — where
        # the phase rests, its own amplitude rests beside it.
        def phaseHolds(bucket, handle, const, ampHandle):
            vs, amps = bucket[handle], bucket[ampHandle]
            if not vs or len(vs) != len(amps):
                return False
            sung = 0
            for v, a in zip(vs, amps):
                if abs(v - const) <= 1e-9:
                    sung += 1
                elif not (abs(v) <= 1e-9 and abs(a) <= 1e-9):
                    return False
            return sung > 0

        gcVoices = sweep["gridColourVoicesOwns"]
        GC_VARIES = ["colourPeriod", "colourAmp", "lightPeriod", "lightAmp"]
        GC_PHASE_CONST = {"colourPhase": 0.0, "lightPhase": 0.5}
        gcDistinct = {h: sorted(set(vs)) for h, vs in gcVoices.items()}
        gcVariesOk = all(bool(gcVoices[h]) and any(abs(v) > 1e-9 for v in gcVoices[h])
                         and len(gcDistinct[h]) > 1 for h in GC_VARIES)
        gcPhaseOk = all(phaseHolds(gcVoices, h, c, h.replace("Phase", "Amp"))
                        for h, c in GC_PHASE_CONST.items())
        check(NODE_ROWS[37], gcVariesOk and gcPhaseOk,
              "on cues that OWN LIGHT-COLOUR: "
              + "; ".join(f"{h}: {len(vs)} readings, {len(gcDistinct[h])} distinct "
                          f"({gcDistinct[h][:6]})" for h, vs in gcVoices.items()))

        # --- row 8e · CHANGE C: strata-light's twelve voice handles are driven where it OWNS --------
        #     LIGHT-COLOUR, not left at 0
        # The same proof as above, over the twelve handles this instrument publishes twice — A off
        # the departing work's own colour.sat/colour.brightness/colour.contrast, B off the arriving
        # work's — ported from lab/step4-assembler.js:1966-2010 into the "strata-light" branch of
        # `fillPlan`, again read only from the "owns" bucket. The four phase handles hold the
        # assembler's own quarter-turn constants exactly: 0, 1/4, 2/4, 3/4 for colourPhaseA,
        # lightPhaseA, colourPhaseB, lightPhaseB in that order.
        slVoices = sweep["strataLightVoicesOwns"]
        SL_VARIES = ["colourPeriodA", "colourAmpA", "lightPeriodA", "lightAmpA",
                    "colourPeriodB", "colourAmpB", "lightPeriodB", "lightAmpB"]
        SL_PHASE_CONST = {"colourPhaseA": 0.0, "lightPhaseA": 0.25,
                          "colourPhaseB": 0.5, "lightPhaseB": 0.75}
        slDistinct = {h: sorted(set(vs)) for h, vs in slVoices.items()}
        slVariesOk = all(bool(slVoices[h]) and any(abs(v) > 1e-9 for v in slVoices[h])
                         and len(slDistinct[h]) > 1 for h in SL_VARIES)
        # Read the same way row 8d's phases are, and for the same reason: a muted voice rests all
        # three of its handles together, so a phase at 0 must have its own amplitude at 0 beside it.
        slPhaseOk = all(phaseHolds(slVoices, h, c, h.replace("Phase", "Amp"))
                        for h, c in SL_PHASE_CONST.items())
        check(NODE_ROWS[38], slVariesOk and slPhaseOk,
              "on cues that OWN LIGHT-COLOUR: "
              + "; ".join(f"{h}: {len(vs)} readings, {len(slDistinct[h])} distinct "
                          f"({slDistinct[h][:6]})" for h, vs in slVoices.items()))

        # --- row 8f · CHANGE C: a cue that only ACCOMPANIES on LIGHT-COLOUR stays silent there ------
        # Shelf 17's levels law names both halves: one active voice per level, so the cue that does
        # NOT own LIGHT-COLOUR must not sing there either. `fillPlan` never writes `wanted.*` for any
        # of the eighteen handles on such a cue, so `appliedValue` resolves every one of them to the
        # manifest's own 0 — this row proves that resolution actually happens across the sweep,
        # reading the "accompanies" bucket the driver keeps apart from the "owns" one above. An empty
        # bucket would mean no accompanying cue was ever cast in this spot-check and the row would
        # have nothing to prove; a non-empty bucket holding anything but 0 would mean the levels law
        # was not honoured.
        accAll = {}
        for prefix, bucket in (("grid-colour.", sweep["gridColourVoicesAccompanies"]),
                               ("strata-light.", sweep["strataLightVoicesAccompanies"])):
            for h, vs in bucket.items():
                accAll[prefix + h] = vs
        accCounts = {k: len(vs) for k, vs in accAll.items()}
        accOffZero = {k: [v for v in vs if abs(v) > 1e-9] for k, vs in accAll.items()}
        anyAccompanying = any(accCounts.values())
        allSilent = all(not off for off in accOffZero.values())
        check(NODE_ROWS[39], anyAccompanying and allSilent,
              f"accompanying-cue readings seen: {accCounts}; any off 0: "
              f"{ {k: v for k, v in accOffZero.items() if v} }")

        # --- row 8g · CHANGE D: strata-light's levelA/levelB are driven off luminance.level -------
        # Before this change nothing ever wrote `wanted.levelA`/`wanted.levelB`, so `appliedValue`
        # resolved both to the manifest's own 0.5 default on every pair. The fix reads each work's
        # own `luminance.level` — the median luminance lab/analyze/recipes.py:551-613 colour_stats()
        # ports from `measure(image)`, lab/effects/strata-light.js:108-113 — A the departing work's,
        # B the arriving work's. Unlike the eighteen voice handles above, level is not gated by
        # LIGHT-COLOUR ownership (it drives the CELL-level cut, not the accompaniment voice), so it
        # is driven on every strata-light cue and the row asks for at least one value off the 0.5
        # default and more than one distinct value over the sweep.
        levelASeen = sweep["levelASeen"]
        levelBSeen = sweep["levelBSeen"]
        levelAOffDefault = [v for v in levelASeen if abs(v - 0.5) > 1e-9]
        levelBOffDefault = [v for v in levelBSeen if abs(v - 0.5) > 1e-9]
        check(NODE_ROWS[40],
              bool(levelASeen) and bool(levelBSeen)
              and bool(levelAOffDefault) and bool(levelBOffDefault)
              and len(set(levelASeen)) > 1 and len(set(levelBSeen)) > 1,
              f"{len(levelASeen)} levelA readings ({len(set(levelASeen))} distinct), "
              f"{len(levelBSeen)} levelB readings ({len(set(levelBSeen))} distinct); "
              f"levelA sample {sorted(set(levelASeen))[:8]}, "
              f"levelB sample {sorted(set(levelBSeen))[:8]}")

        # --- row 8h · GATE-SLOT LANE PART 1: gates' slotPlace/slotHalf/slotAxis read the -----------
        #     departing work's own measured slot
        # Before this change none of the three was ever written by `fillPlan`'s "gates" branch, so
        # `appliedValue` resolved every one to the manifest's own naive middle: slotAxis upright
        # (1), slotPlace and slotHalf at half the motif's own fixed band — the exact reading
        # pass-inst-gates.js:604-638 spent thirty-odd lines explaining was missing from the record.
        # lab/step1-motifs.py's rewrite of 2026-08-19 (slot_on()/gateOf(), ported from the archived
        # lab/effects/gates.js) publishes `motifs.gatePlace`/`gateHalf`/`gateAxis` on every work, and
        # this row asks the sweep for three things at once: every applied value matches the
        # departing work's own record (within the four-decimal rounding both sides already carry),
        # slotPlace and slotHalf each take more than one distinct value (proving the reading is the
        # slot's own place and width rather than one number reused), and slotAxis takes both 0 and 1
        # (proving the sweep actually reaches works of each axis, 69 vertical and 52 horizontal over
        # the full collection per lab/step1-motifs.py's own count).
        gs = sweep["gateSlots"]
        def gsFor(h):
            return [r for r in gs if r["handle"] == h]
        gsMismatch = [r for r in gs if r["record"] is not None
                      and abs(r["applied"] - r["record"]) > 0.0002]
        placeSeen = sorted(set(r["applied"] for r in gsFor("slotPlace")))
        halfSeen = sorted(set(r["applied"] for r in gsFor("slotHalf")))
        axisSeen = sorted(set(r["applied"] for r in gsFor("slotAxis")))
        check(NODE_ROWS[41],
              bool(gs) and not gsMismatch
              and len(placeSeen) > 1 and len(halfSeen) > 1 and axisSeen == [0, 1],
              f"{len(gs)} gate slot readings over the sweep, {len(gsMismatch)} off the departing "
              f"work's own record by more than 0.0002; slotPlace {len(placeSeen)} distinct "
              f"{placeSeen[:8]}, slotHalf {len(halfSeen)} distinct {halfSeen[:8]}, slotAxis seen "
              f"{axisSeen}")

        # --- row 8i · THE WITNESS CAMERA'S OWN FLIGHT (charter shelf 2) -----------------------------
        # Until 2026-08-19 every camera track on every pair that did not carry the gears instrument
        # wrote the same four all-zero points — pan, logScale, pitch, yaw and roll all at nothing —
        # which reads on screen as no camera at all, exactly the defect his 2026-08-12 report named
        # and that stood unfixed because the earlier proof was words rather than pixels. These four
        # rows are the words; the headless render three-pairs-before/three-pairs-after proof this
        # unit's own report carries is the pixels.
        cam = got["camera"]
        # row A · the middle is non-neutral, differs pair to pair, and survives the wire-fitting
        # step. `fitTheWeight` (pass-composer.js) sheds every driven node's own provenance note
        # whenever a filled score stands over the client's byte fence; it never touches `camera`,
        # and this row is what proves that rather than assuming it.
        check(NODE_ROWS[42],
              cam["checked"] > 0 and cam["allZero"] < cam["checked"] and cam["distinctTracks"] > 1
              and cam["fitMismatch"] == 0,
              f"of {cam['checked']} composed pairs checked, {cam['allZero']} land on a fully "
              f"static middle (every axis at nothing on both points) and {cam['checked'] - cam['allZero']} "
              f"do not; {cam['distinctTracks']} distinct middles seen over the sample; a score's "
              f"own camera block differs from its plan's on {cam['fitMismatch']} of them, which "
              f"would mean the wire-fitting step touched it")
        # row B · each axis, where non-zero, matches the record reading it claims to read — checked
        # by re-deriving the same five axes independently in this driver (camExpected(), mirroring
        # pass-composer.js's own fillPlan camera block) rather than trusting the composer's own
        # arithmetic against itself.
        check(NODE_ROWS[43],
              cam["checked"] > 0 and not cam["mismatches"],
              f"{cam['checked']} pairs checked against an independent re-derivation of the same "
              f"five readings; disagreements: "
              + (json.dumps(cam["mismatches"][:2], ensure_ascii=False) if cam["mismatches"]
                 else "none"))
        # row C · the two ends stay honest on every pair — shelf 2's "resting exactly when B
        # stands", never touched by the middle's own derivation.
        check(NODE_ROWS[44],
              cam["checked"] > 0 and cam["endsBad"] == 0,
              f"of {cam['checked']} composed pairs, {cam['endsBad']} carry a non-neutral «a» or "
              f"«b» point")
        # row D · the track never exceeds the client's own published camera-point fence
        # (engine/client/01a-pass.js's PASS_LIMITS.camera, read once at CLIENT_CAMERA_POINTS above).
        check(NODE_ROWS[45],
              cam["checked"] > 0 and cam["maxTrackLen"] <= cam["trackPointCap"],
              f"the longest camera track composed here carries {cam['maxTrackLen']} points against "
              f"the client's own fence of {cam['trackPointCap']}")

        # --- row 8j · THE LETTERS THE WALK HAS ALREADY PLAYED (charter shelf 16's dice pipeline,
        # his 2026-08-17 19:13 word about a route's breadth, and his 2026-08-24 word watching the
        # live route: the effects repeat noticeably across crossings) --------------------------------
        # Shelf 16 orders the dice: base weights (structure fit) → LETTER COOLDOWNS → the day's
        # weather → viewer memory → roll. The cooldown was the one step of that order with nothing
        # behind it: the composer answered every step of a walk as though it were the first, so a
        # letter that suited a collection well carried step after step of one route. The walk has
        # always known what it played — `passRoutePlayed` in the client — and the reading simply
        # never crossed the line.
        #
        # THE ROW IS THE LAW, NOT A FENCE. Two walks of the same 40 routes on the same dice, one
        # blind and one handed its own memory at every step; the remembered walk has to spread
        # WIDER. A fence would drift with the collection; this reads the mechanism itself, and it
        # reds the moment the cooldown stops being applied whatever the collection does. Beside it
        # stands shelf 9's own law and the lab's: a cooldown RANKS and never gates, so not one step
        # of the remembered walk may lose its crossing.
        rt0, rt1 = got["route"], got["routeRemembered"]
        check(NODE_ROWS[46],
              rt1["topShareMean"] < rt0["topShareMean"] and rt1["lost"] == 0
              and rt1["composed"] == rt0["composed"] and rt1["letters"] >= rt0["letters"],
              f"over {rt0['routes']} cast routes of 21 steps: blind, the commonest instrument "
              f"carries {rt0['topShareMean']}% of a route on average over {rt0['letters']} letters; "
              f"handed the route's own memory it carries {rt1['topShareMean']}% over "
              f"{rt1['letters']} letters, with {rt1['lost']} steps losing their crossing to the "
              f"cooldown (a cooldown never empties a pool); remembered spread "
              + json.dumps(rt1["spread"], ensure_ascii=False))

        # --- row 8k · THE LEVEL THE CARRYING AXIS CLEARS (charter shelf 2 with shelf 17) ----------
        # His 2026-08-24 word watching the live route: the camera's movement does not visibly read
        # during a crossing. It is not a bug in the derivation — every axis reads its own record
        # correctly — it is that the amplitude is a PRODUCT of independent readings each already
        # short of its own ceiling, so the excursion collapses toward nothing however strongly the
        # pair calls for it. The composer's own note above `reach` names the same gap from the other
        # side: the tier reaches this flight nowhere.
        #
        # The repair is shelf 17's voice budget made into a LEVEL rather than a count, and shelf 9's
        # law holds inside it: the readings still rank — which axis carries, and how far above the
        # floor it flies — and the floor only guarantees that the voice which was chosen can be seen.
        # Nothing is refused: a floor on an amplitude cannot decline a crossing.
        low = cam["voiceShares"]
        med = low[len(low) // 2] if low else 0
        check(NODE_ROWS[47],
              cam["voiceChecked"] > 0 and cam["voiceUnder"] == 0,
              f"of {cam['voiceChecked']} composed pairs whose flight carries a rotational axis, "
              f"{cam['voiceUnder']} spend less of that axis's own ceiling than the pair's own grain "
              f"asks for; the share worn runs {low[0] if low else 0}…{low[-1] if low else 0} with a "
              f"median of {med}; the widest shortfalls were "
              + (json.dumps(cam["voiceWorst"], ensure_ascii=False) if cam["voiceWorst"] else "none"))

        # --- row 8l · A DECLARED VOICE IS A SEEN VOICE (charter shelf 11 with shelf 17) -----------
        # The eighteen colour-and-light handles were ported from lab/step4-assembler.js in first-pass
        # form: amplitude = a quarter of the departing work's own reading. What was left in the lab
        # was the pass AFTER it — the audibility loop that measures whether the voice moves a real
        # frame at all and raises it until it does, muting the voice a work cannot sing loudly
        # enough. The lab's own law for it: «Заявленный и неслышный голос — пустое утверждение
        # разбора». The lab needed a rendered probe; the peak of `amp·sin(2π(u/period+phase))·4u(1−u)`
        # is closed-form in the two numbers the composer already writes, so the same reading is taken
        # here without one.
        vo = got["voices"]
        check(NODE_ROWS[48],
              vo["checked"] > 0 and vo["silentDeclared"] == 0,
              f"of {vo['checked']} colour and light voices driven over the sweep, "
              f"{vo['silentDeclared']} peak below the lab's own {vo['target255']} of 255 — declared "
              f"and unseeable; the quietest were "
              + (json.dumps(vo["worst"], ensure_ascii=False) if vo["worst"] else "none"))

        # --- row 9 · the two fences a filled score has to pass -----------------------------------
        # THE FENCES ARE NO LONGER WALLS, AND THAT IS WHY THIS ROW MATTERS MORE THAN IT DID. The
        # client refused a score over either fence WHOLE, so a score standing over one was a
        # crossing the visitor never saw; both are shapings now — the composer fits its own line and
        # its own weight before the client ever sees them. The row therefore proves the FITTING
        # works: nothing composed here, on real records or on the hardest records this suite can
        # build, ever stands over either number.
        hard = got["hard"]
        check(NODE_ROWS[12], sweep["overByte"] == 0 and sweep["overIntent"] == 0,
              f"the heaviest score here weighs {sweep['maxBytes']} B against the "
              f"{sweep['byteCap']} the client applies, and the longest line runs "
              f"{sweep['maxIntent']} characters against its {sweep['intentCap']}; over the byte "
              f"fence: {sweep['overByte']}, over the line's fence: {sweep['overIntent']}; and over "
              f"{hard['asked']} crossings of the hard records, none stands over either")

        # --- row 10 · the composer reads the fence it is handed ----------------------------------
        h = got["handed"]
        check(NODE_ROWS[13],
              h["shortened"] > 0 and sweep["intentShortened"] == 0,
              f"handed a cap of {h['cap']} characters in its own constants, the composer shortened "
              f"{h['shortened']} of {h['composed']} lines and its longest ran {h['max']}; on the "
              f"number the client actually applies its longest runs {h['own']}")

        # --- row 10 · THE ROW THIS LANE STANDS ON --------------------------------------------------
        # His word of 2026-08-18 09:51: any two photographs in the world get a crossing, always. It
        # is proved on RECORDS rather than on a collection — a collection is a sample and a record is
        # a case — so the cases are the ones deliberately built to be the worst the composer could be
        # handed, each asked at every route role, in both directions, on three dice. A single input
        # yielding nothing reddens this row.
        #
        # WHAT THIS ROW REPLACES. «every one of the 14 520 ordered pairs either composes or declines
        # by name» — a census of a collection, and the very habit his word strikes out. It also
        # accepted a decline as a lawful answer, which is the whole idea this lane removes.
        shown = "; ".join(f"{k}: {v2['genre']} at {v2['fit']} → {v2['cues']} "
                          f"({v2['duration']} ms, {v2['bytes']} B, {v2['stood']} shaping(s))"
                          for k, v2 in hard["rows"].items())
        check(NODE_ROWS[14],
              hard["playable"] == hard["asked"] and not hard["failures"] and hard["asked"] > 0,
              f"{hard['playable']} of {hard['asked']} crossings over {hard['cases']} deliberately "
              f"hard records are playable; failures: {hard['failures'] or 'none'}. At a middle, "
              f"a-to-b, on one die — {shown}")

        # --- row 11 · the defaults reproduce the four-value call -----------------------------------
        dd = got["defaults"]
        check(NODE_ROWS[15], dd["spelledSame"] and dd["coreSame"],
              f"the six fields named at their defaults read the same bytes: {dd['spelledSame']}; "
              f"the choice core's own four-value call reads them too: {dd['coreSame']}. The equality "
              f"is against the composer's own output on this same run, never against the prebaked "
              f"pack stage 0 was landed on — that gate went with the road it guarded")

        # --- rows 12-14 · what the entry does with a request it cannot read as sent -----------------
        # THESE WERE THREE REFUSALS BY NAME and each cost the visitor a whole crossing for a field
        # the walk got wrong. They are defaults now: the vocabulary still cannot drift, §4.8's fence
        # still lets nothing outside its three fields cross, and the die still lands inside the
        # instrument's own span — the entry simply reaches those ends by reading the request as it
        # can rather than by turning the pair away. What could not be read stands on the request
        # under `unread`, so a walk sending a stray value is still findable.
        f = got["fences"]
        check(NODE_ROWS[16],
              f["role"]["composed"] is True and f["role"]["role"] == "middle"
              and any("grand finale" in u for u in (f["role"]["unread"] or [])),
              f"the crossing plays, the step reads as a «{f['role']['role']}», and the stray name is "
              f"recorded: {f['role']['unread']}; the five the entry names: {got['routeRoles']}")
        check(NODE_ROWS[17],
              f["memory"]["composed"] is True
              and "cooldown" not in json.dumps(f["memory"]["memory"] or {})
              and any("cooldown" in u for u in (f["memory"]["unread"] or []))
              and f["memoryOk"]["composed"] is True,
              f"the crossing plays and the fourth field never crosses the line — the memory the "
              f"composer read is {f['memory']['memory']}, and what it left unread: "
              f"{f['memory']['unread']}")
        check(NODE_ROWS[18],
              f["seedHigh"]["composed"] is True and f["seedLow"]["composed"] is True
              and got["seedSpan"][0] <= f["seedHigh"]["seed"] <= got["seedSpan"][1]
              and got["seedSpan"][0] <= f["seedLow"]["seed"] <= got["seedSpan"][1],
              f"a die of 9 is rolled at {f['seedHigh']['seed']} and a die of -1 at "
              f"{f['seedLow']['seed']}, both inside the span the entry reads off the instrument's "
              f"own manifest: {got['seedSpan']}; and the two refusals that remain both say there is "
              f"no PAIR — {got['fences']['noA']!r}, {got['fences']['noB']!r}")
        # The walk memory joins the entry on the same terms as the rest: read where it can be, left
        # unread and recorded where it cannot, and never a reason to lose the crossing.
        check(NODE_ROWS[49],
              f["walkNotAList"]["composed"] is True and f["walkNotAList"]["walk"] is None
              and any("no list" in u for u in (f["walkNotAList"]["unread"] or []))
              and f["walkStray"]["composed"] is True
              and f["walkStray"]["walk"] == ["unfold", "weave"]
              and any("naming no letter" in u for u in (f["walkStray"]["unread"] or []))
              and f["walkOk"]["composed"] is True
              and f["walkOk"]["walk"] == ["unfold", "weave"]
              and f["walkOk"]["unread"] is None,
              f"a walk memory that is no list reads as nothing played and says so "
              f"({f['walkNotAList']['unread']}); a list carrying two entries that name no letter "
              f"keeps the two that do ({f['walkStray']['walk']}) and records the rest "
              f"({f['walkStray']['unread']}); a plain list of letters crosses whole with nothing "
              f"unread")

        # --- rows 15-25 · the same repairs, each reverted in a copy ---------------------------------
        # A planted run walks a corner of the collection rather than all of it, because a plant is
        # judged on whether the answer MOVES and twenty-four works are 552 ordered pairs of proof.
        CORNER = 24
        PLANTS = [
            # THE ONE FENCE LEFT IN THE ENTRY, and it says there is no PAIR. Removed, a request
            # naming one work no longer meets a refusal: it walks into the pair arithmetic, which
            # reads two records and is handed one, and the answer moves off the refusal's sentence.
            (NODE_ROWS[19], [["if (!a || !a.id) return no(", "if (!a) return no("]],
             lambda g: g["fences"]["noA"] != got["fences"]["noA"]),
            (NODE_ROWS[20], [["          if (odd.length) {", "          if (false) {"]],
             lambda g: "cooldown" in json.dumps(g["fences"]["memory"]["memory"] or {})),
            (NODE_ROWS[21],
             [["genreFor(fromW, toW, step, memory || null, seed, key)",
               "genreFor(fromW, toW, step, memory || null, 0, key)"]],
             lambda g: len(g["dice"]["distinct"]) == 1),
            # THE FITS ARE WHAT RANK THE GENRES. Flattened to one number, the ranking stops reading
            # the pair at all and the die is even over the vocabulary — which is exactly the state
            # the floors produced by another road, and the route's spread says so.
            #
            # MOVED OFF `topShareMean` TO THE FULL `spread` DICT (PART 2 OF THE COLOUR-AND-LIGHT
            # LANE, 2026-08-19). `tonalSpectral()` now reads `luminance.level` — a field that ties
            # far more often across the collection than `palette.colourfulness` did — so the
            # tonal-and-spectral genre reaches fit 1 on more pairs of this route's own 40-route
            # sample, and `topShareMean` (rounded to one decimal place over 40 routes) landed on the
            # same 28.5 whether the fit is flattened or not: a coincidence of the rounding on this
            # one pinned sample, not evidence the plant stopped moving anything. The full per-
            # instrument `spread` the same run already carries moves on nearly every one of its
            # twenty-two keys (matter 9.3 → 10.2, gates 7.6 → 7.1, grid-colour 12.4 → 12.8, and on),
            # so the observation is here instead: the ground truly moved and the row now reads it
            # where it actually shows.
            (NODE_ROWS[22],
             [["        genre.fit = clamp01(fit);", "        genre.fit = 1;"]],
             lambda g: g["route"]["spread"] != got["route"]["spread"]),
            (NODE_ROWS[23], [["if (fits) break;", "break;"]],
             lambda g: (g["roles"]["quiet link"].get("budget") or {}).get("letters", 0) > 1
             or (g["roles"]["quiet link"].get("budget") or {}).get("miracles", 0) > 0
             or g["roles"]["quiet link"].get("duration", 0) > 4000),
            # A LED PASSAGE IS A READING OF TWO THINGS, and each is proved by taking it away.
            # THE ROLE'S HALF NEEDS A PASSAGE THAT COULD BE LED, and since the arrival stopped being
            # dropped on a collision no middle of this collection runs on its ground alone — the one
            # shape a camera can carry — so removing the role gate moved nothing and the row proved
            # nothing. The two plants beneath it make that shape again, and they make it honestly:
            # a crossing with no travelling move and no arriving one, which is exactly what the
            # reading beside the role gate answers. With the role gate in place such a middle is
            # still not led; with it removed it is, and that is the gate.
            (NODE_ROWS[24], [["LED_ROLES.indexOf(role) >= 0", "true"],
                             ["      if (arrival === \"CONDENSED\") {", "      if (false) {"],
                             ["      var axis = travellingAxisOn(fromW, toW, pivot.measure, "
                              "road.axis);",
                              "      var axis = null;"]],
             lambda g: g["sweep"]["ledElsewhere"] > 0),
            (NODE_ROWS[25], [["made.cameraTravels && ", ""]],
             lambda g: g["sweep"]["ledAtTonic"] > 0.6 * g["sweep"]["tonic"]),
            (NODE_ROWS[26],
             [["          if (familyOf(whole[i], fromW, toW, seed) === memory.family) {\n            held = whole[i];\n            heldBy = \"family\";",
               "          if (false) {\n            held = whole[i];\n            heldBy = \"family\";"]],
             lambda g: g["memory"]["heldAgainBy"] != "family"
             and g["memory"]["heldBackBy"] != "family"),
            # MOVED OFF THE OUTCOME (`backKeepsFamily`/`backKeepsPivot`) TO THE MECHANISM
            # (`heldBackBy`/`heldAgainBy`), PART 2 OF THE COLOUR-AND-LIGHT LANE, 2026-08-19.
            # `tonalSpectral()` now reads `luminance.level`, whose fit is symmetric in the two works
            # and ties at 1 far more often than `palette.colourfulness`'s did — so on this pair the
            # tonal-and-spectral ground is now the strongest candidate independently in BOTH
            # directions, and the walk back can land on the SAME ground by nothing but that shared
            # strength even with the retry loop cut out, which left `backKeepsPivot` True on a
            # planted run and the row unable to move. `heldBackBy`/`heldAgainBy` are the retry
            # loop's own flag — set only when it actively matched a recorded family or pivot — so
            # they read whether the MECHANISM fired rather than whether the outcome happens to
            # resemble it, which is the real effect this plant removes.
            (NODE_ROWS[27],
             [["      var wantTransform = memory && memory.family ? String(memory.family).split(\"+\")[0] : null;",
               "      var wantTransform = null;"],
              ["      if (memory && memory.family) {\n        var whole = pool.concat(found.genres);",
               "      if (false) {\n        var whole = pool.concat(found.genres);"]],
             lambda g: g["memory"]["heldBackBy"] is None and g["memory"]["heldAgainBy"] is None),
            # THE OPEN HANDLE'S FENCE IS PROVED WHERE IT COULD BE CROSSED. Nothing today hands the
            # open handle to the fill — the collection's own instrument list leaves it out — so the
            # plant that makes the row honest is the one that DOES hand it over: a cue's tracks named
            # off the manifest itself, with the open reading removed.
            #
            # THE ROW USED TO NAME «bal», THE WOVEN INSTRUMENT'S OWN OPEN HANDLE, BECAUSE ON A
            # SEVENTEEN-INSTRUMENT FIELD THE CORNER THE PLANTS WALK — `CORNER`, 24 pairs, the same 24
            # every run — always cast weave at least once. It no longer does: with twenty-two
            # instruments sharing the corner's own cuts, weave loses the die often enough that this
            # exact corner casts it zero times, so «bal» never gets the chance the plant opens for it.
            # THAT IS A FACT ABOUT WHICH INSTRUMENT THE CORNER HAPPENS TO CAST, and pinning the row to
            # one instrument's own handle is exactly the «lucky pair» this suite's law forbids —
            # weave was never the point; the fence being open to WHATEVER declares an open handle is.
            # `gates` and `gears` both publish `dial` as open and both are cast in this corner every
            # run, so the plant already opens a door the corner can walk through; the row now asks
            # the general question the fence's own law states — is ANY handle an instrument declares
            # open ever driven — rather than the name of the one instrument that happened to answer
            # it on the field this row was written against.
            (NODE_ROWS[28],
             [["        if (manifest[h].open) continue;", ""],
              # The register gained an instrument-scoped key on 2026-08-18, so both reads below go
              # through `sourceOf` now. The plant follows the line rather than the name it used to
              # have: a plant that stops matching stops proving, and this row's claim is unchanged.
              ["        if (!sourceOf(instr, h)) continue;", ""],
              ['var why = sourceOf(c.instrument.id, h)[1];',
               'var why = (sourceOf(c.instrument.id, h) || ["", "an open handle"])[1];'],
              ["var spec = HANDLE_SPECS[instr][handle], lo = spec[0], hi = spec[1], dflt = spec[2];",
               "var m0 = MANIFESTS[instr].handles[handle];"
               " var spec = HANDLE_SPECS[instr][handle] || [m0.min, m0.max, m0[\"def\"]],"
               " lo = spec[0], hi = spec[1], dflt = spec[2];"]],
             lambda g: bool(g["sweep"]["openDriven"])),
            # THE LINE IS FITTED RATHER THAN REFUSED. With every step of the fitting removed, a line
            # handed a small cap runs over it — which under the client's own reading is a crossing
            # refused WHOLE, and the reason 1 004 composed crossings were never seen.
            (NODE_ROWS[29],
             [["if (line.length > INTENT_FENCE_CHARS && fields.returnPhrase) {", "if (false) {"],
              ["if (line.length > INTENT_FENCE_CHARS && fields.roadPhrase) {", "if (false) {"],
              ["      if (line.length > INTENT_FENCE_CHARS) {", "      if (false) {"]],
             lambda g: g["handed"]["max"] > g["handed"]["cap"]),
            # THE FOLD'S TWO LAWS, each proved by taking its own reading away. The first is read off
            # the instrument's own manifest — an instrument declaring the WORLD level folds the
            # space — so removing that reading is removing the law.
            # THE PLANT WAS INCOMPLETE AND THE ROW WENT GREEN ON THREE GUARDS WHILE A FOURTH HELD.
            # Shelf 17's law is kept in FOUR places, not three: the tier `castForKinds` gives a
            # folding instrument, the travelling voice's own check, the genre pool's filter, and
            # `bestFilling`'s `continue`. With three removed the fourth held alone and the answer
            # did not move at all, at any corner size up to the whole collection — measured at the
            # merge on a field of fifteen instruments, where the earlier field of five let the first
            # three carry it. A plant that leaves a guard standing proves the guard it left.
            #
            # AND THE READING IS WIDENED FROM ONE INSTRUMENT TO THE LAW. `folded` counts the folding
            # instrument alone; the law is about spending the crossing's one miracle, and three
            # instruments now publish the WORLD level. So the row reads both — a fold at a
            # no-miracle role, and any WORLD cue at one — and either moving reddens the plant.
            (NODE_ROWS[30],
             [["        var base = (cuts ? 0 : 2) + ((noMiracle && folds) ? 1 : 0);",
               "        var base = (cuts ? 0 : 2);"],
              ["        } else if (spendsTheMiracle(travelInstr) && !(ROLE_BUDGETS[role] || {}).miracle) {",
               "        } else if (false) {"],
              ["        pool = pool.filter(function (r) { return !r.mustFold; });", ""],
              ["        if (noMiracle && spendsTheMiracle(iid)) continue;", ""]],
             lambda g: sum(g["sweep"]["folded"][r] + g["sweep"]["worldCue"][r]
                           for r in ("entrance", "quiet link", "return")) > 0),
            # ONE INSTRUMENT PER KIND, RESTORED IN A COPY — the rule an earlier lane repaired. With
            # the candidates on a kind cut back to the first of them, and the ranking's second and
            # third orders of preference removed with it, an instrument travels to every visitor and
            # can never be chosen.
            (NODE_ROWS[32],
             [["        if (CUTS_ON[kind].indexOf(iid) < 0) CUTS_ON[kind].push(iid);",
               "        if (!CUTS_ON[kind].length) CUTS_ON[kind].push(iid);"],
              ["      for (i = 0; i < tiers.length; i++) {\n        if (tiers[i].length) {",
               "      for (i = 0; i < 1; i++) {\n        if (tiers[i].length) {"],
              # THE ARRIVAL HANDED TO A NAME AGAIN, which is the state this lane removed: the slot
              # went to «matter» whenever «matter» was free, with no fit read and no die rolled, and
              # every other instrument reached the arrival only through a fallback that then dropped
              # the voice on a collision. Restoring it here is what makes the row's own sentence
              # true again — an instrument travels to every visitor and can never be chosen.
              ["        arrivalInstr = castArrival[0];",
               "        arrivalInstr = MANIFESTS.matter ? \"matter\" : castArrival[0];"],
              ["          if (fill1 && fill1 !== pivotInstr) {", "          if (false) {"]],
             lambda g: [i for i in g["sweep"]["cast"] if not g["sweep"]["chosen"].get(i)]),
            # THE GROUND GATED ON THE COLLECTION'S TOP QUARTILE AGAIN — the shape this lane removed.
            # Both works clearing a measure's top quartile happens on about 6 per cent of pairs for
            # every measure by construction, so nearly everything fell through to one ground with one
            # cut and one instrument, and that instrument carried the route.
            # THE READING WAS RE-ANCHORED ONCE ALREADY, AND THE FIELD HAS MOVED PAST IT AGAIN. This
            # row first read the gate's harm off `topShareMean`, then off the route's own distinct-
            # shape count once a field of fifteen instruments put several instruments on one cut —
            # both readings sit one hop downstream of what the mutation itself does, and both are
            # exactly as far as the instrument roster can carry them. On the field of twenty-two the
            # five new instruments (beat, gates, grid-colour, strata-light, tilt) sit across enough
            # cuts that a pair pushed off its shared ground no longer plays a narrower route — measured
            # at the merge, the route's own `shapesMean` ROSE from 17.4 to 18.6 with the gate back,
            # the opposite of what it did on the smaller fields. Chasing the shape count a third time
            # would be reading whichever way the instrument roster happens to lean this month, not
            # the gate.
            # THE ROW READS THE GATE'S OWN MECHANISM INSTEAD, which no instrument roster can turn
            # around: `groundReadings` is exactly what the gate zeroes, and `groundReadings` is what
            # decides whether a pair reaches the «shared-ground» road at all — the road IS the gate's
            # own target, not a downstream consequence of it. Gating out everything short of a
            # measure's own top quartile starves that road directly: measured over the same sweep the
            # standing rows walk, 44 of 190 pairs land on shared-ground with the gate out and 9 of 190
            # with it back in. That is the gate's own cost, read where the gate itself acts.
            (NODE_ROWS[33],
             [["        per[m] = { min: r4(Math.min(sa, sb)), a: r4(sa), b: r4(sb) };",
               "        var th = (consts.thresholds || {})[m];"
               " per[m] = { min: r4((th !== undefined && (sa < th || sb < th)) ? 0 : Math.min(sa, sb)),"
               " a: r4(sa), b: r4(sb) };"]],
             lambda g: g["sweep"]["roads"].get("shared-ground", 0)
             < got["sweep"]["roads"].get("shared-ground", 0)),
            # THE FOLD IS COUNTED WHEREVER THE FOLDING CUE STANDS, so the plant has to take the
            # reading away at all three slots. It named the PIVOT alone, and it went red only while
            # the folding instrument could reach no slot but the ground: since the arrival is cast
            # like every other voice, a folding cue at the arrival kept its miracle through the
            # second line and the plant proved the line it left standing. A plant that leaves a
            # guard standing proves the guard it left.
            (NODE_ROWS[31],
             [['      if (folds === "pivot") voices.pivot = "miracle";',
               '      if (false) voices.pivot = "miracle";'],
              ['        voices.travel = (folds === "travel" || world) ? "miracle" : "letter";',
               '        voices.travel = "letter";'],
              ['      if (hasArrival) voices.arrival = folds === "arrival" ? "miracle" : "letter";',
               '      if (hasArrival) voices.arrival = "letter";']],
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
        check("EX-COMPOSED the line gives up its own clauses and then its tail, and is never lost",
              hd["roadKept"] == 0 and hd["shortened"] > 0 and hd["max"] <= hd["cap"]
              and sweep["roadKept"] > 0 and sweep["intentShortened"] == 0,
              f"handed a cap of {hd['cap']} characters in its own constants, {hd['shortened']} of "
              f"{hd['composed']} lines gave up a clause, {hd['roadKept']} kept a genre's opening and "
              f"the longest ran {hd['max']} — inside the cap, so nothing is ever lost to its own "
              f"length; at the {sweep['intentCap']} the client applies, {sweep['roadKept']} of "
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
    # EX-PASS-RECORDS (2026-08-19): the four rows below hold the wave contract itself — what
    # config.json's pass.records route is asked, in what shape, and when it is asked for nothing.
    "EX-COMPOSED the door's own spread asks the route once, for exactly its own ids, and an unfold "
    "asks once more, for exactly the ids it appends — no id asked twice, no wave of one id alone",
    "EX-COMPOSED the route's own cap refuses a wave that asks past it",
    "EX-COMPOSED a wave that never lands leaves the walk on its own glide, not a throw",
    "EX-COMPOSED a visit standing still asks the route for nothing at all",
]


def enter(br, base, pass_arg=None, step=False):
    """A fresh visitor who opens the door and stands in the walk. `step` takes ONE real step, which
    is the only road that asks for the picture layer's file (engine/client/15-motion.js: the layer
    is opened where a step declares its command)."""
    br.navigate(base + "/")
    br.clear_storage()
    # WHERE THIS VISIT'S OWN WAVES BEGIN (2026-08-19). A record map belongs to one page load: the
    # client holds it in memory and a fresh load starts with nothing, so the first navigate above —
    # the one that exists only to have somewhere to clear storage from — legitimately asks the route
    # for the spread it hangs, and so does the real one below. Both are right, and a row that reads
    # the log from before the pair would see one spread asked twice and call the walk wasteful. The
    # mark is taken here, between them, so a row reads only the load it is actually about.
    RECORDS_MARK[0] = len(RECORDS_LOG)
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


# ---------------------------------------------------------------- EX-PASS-RECORDS: the route itself
#
# `config.json`'s `pass` block no longer carries `works` (2026-08-19): it carries `records: {route,
# cap}` instead, and the full id → record map travels as a static asset no browser fetches — read
# instead by a Cloudflare Worker at `GET /api/pass/records?ids=a,b,c` (engine/assets/worker.js's
# `passRecordsRoute`). This suite serves the SAME contract locally through the harness's `answer`
# hook (tests/headless_harness.py's `serve`), so the walk asks a real route over the wire exactly as
# it does in production, and every wave this suite drives is proof of the wire and not of a config
# key the client no longer reads.
#
# THE STORE IS MUTABLE AND MODULE-LEVEL because `answer` is bound into `serve(...)` once, before any
# work's id is known, while `put_records` is called AFTER the server is already up (some rows only
# learn which ids the walk hung by reading the DOM). Mutating the same dict in place — never
# reassigning it — is what lets a hook captured early see records written late.
RECORDS_ROUTE = "/api/pass/records"
RECORDS_CAP = 20   # spread_size 10 + max_unfolds 2 × unfold_step 5 — the built-in defaults (build.py)
RECORDS_STORE = {}           # id -> record, exactly the shape pass-workrecords.json ships
RECORDS_LOG = []              # one entry per GET this run answered: the `ids` list it was asked for
RECORDS_MARK = [0]            # where the CURRENT page load's own waves begin in that log (see enter)
FAIL_WAVE = {"on": False}    # armed by the "wave that never lands" row; answers the NEXT GET with 500


def records_answer(raw_path):
    """The harness's `answer` hook for this suite: answers `GET /api/pass/records?ids=...` the way
    `engine/assets/worker.js`'s `passRecordsRoute` does — a request over `RECORDS_CAP` ids, or with
    none at all, is refused with 400; an id `RECORDS_STORE` does not carry is simply left out of the
    answer, never a per-id error. Every ids list asked is appended to `RECORDS_LOG` before either
    outcome, so a row can read off this log what the walk actually asked for and when, rather than
    inferring it from the client's own report."""
    if not raw_path.startswith(RECORDS_ROUTE):
        return None
    ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
    RECORDS_LOG.append(ids)
    if FAIL_WAVE["on"]:
        FAIL_WAVE["on"] = False    # fires once — the very next wave this hook sees, and no other
        return (500, "text/plain", "induced failure (EX-COMPOSED wave-fails row, 2026-08-19)")
    if not ids or len(ids) > RECORDS_CAP:
        return (400, "text/plain", "bad request")
    out = {i: RECORDS_STORE[i] for i in ids if i in RECORDS_STORE}
    return (200, "application/json", json.dumps({"records": out}))


def put_records(base_dir, ids):
    """The settings record as the site writes it for the composed road: the collection's own
    constants and `pass.records`, the route + cap a visitor's browser actually reads (2026-08-19 —
    `works` left this block; see the EX-PASS-RECORDS row above). The full id → record map this call
    builds is handed to `RECORDS_STORE` — the harness's `answer` hook — rather than to config.json, so
    the route this suite serves answers exactly as the Worker does. The fixture's two records are
    re-keyed onto the works this bake actually hangs — what the composer reads out of a record is
    measurement, and the id is only its name."""
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


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP, answer=records_answer) as base:
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
                # THE WAVE LOG IS THE WHOLE RUN'S, AND THIS ROW IS ONE VISIT'S (2026-08-19). The
                # harness hook appends every request any visit of this file ever makes, and rows
                # above this one have already walked the site more than once, so the log carries
                # their waves too. The mark is taken before this visit's own entry, and everything
                # the wave row reads is sliced from it — a row that counted the whole log would read
                # a green run as a walk asking three times for one spread.
                enter(br, base, "diagnostics:on", step=True)
                records_at_entry = RECORDS_MARK[0]
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

                # 9 · EX-PASS-RECORDS: the wave contract, read off the harness's own log of what it
                # was asked (RECORDS_LOG) rather than off the client's own report — a defect that
                # asked the route rightly but reported wrongly must still redden here. `shown` above
                # is the door's own spread, already landed by the `enter(..., step=True)` just above;
                # clicking «ещё 5» appends the next UNFOLD ids and should ask the route exactly once
                # more, for exactly those, and no id already asked should be asked again.
                for _ in range(20):
                    if len(RECORDS_LOG) > records_at_entry:
                        break
                    br.sleep(0.2)
                mine = RECORDS_LOG[records_at_entry:]
                wave1 = list(mine[-1]) if mine else []
                before_unfold = set(shown)
                br.click("#ex-unfold", settle=0.8)
                grown = shown
                for _ in range(20):
                    grown = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                                   ".map(function(e){return e.dataset.id;});")
                    mine = RECORDS_LOG[records_at_entry:]
                    if len(mine) > 1 and len(grown) > len(shown):
                        break
                    br.sleep(0.2)
                mine = RECORDS_LOG[records_at_entry:]
                wave2 = list(mine[-1]) if len(mine) > 1 else []
                added = set(grown) - before_unfold
                RECORDS_LOG_MINE = mine
                check(BROWSER_ROWS[9],
                      len(RECORDS_LOG_MINE) == 2
                      and sorted(wave1) == sorted(shown) and len(wave1) > 1
                      and sorted(wave2) == sorted(added) and len(wave2) > 1
                      and not (set(wave1) & set(wave2)),
                      f"the route's own log carries {len(RECORDS_LOG_MINE)} request(s) for this "
                      f"visit {[len(w) for w in RECORDS_LOG_MINE]} = {RECORDS_LOG_MINE}: "
                      f"the first asked "
                      f"{len(wave1)} id(s) against the door's spread of {len(shown)}, the second "
                      f"(after «ещё 5») asked {len(wave2)} id(s) against {len(added)} newly "
                      f"appended, sharing {len(set(wave1) & set(wave2))} id(s) between them")

                # 10 · the route's own cap. A request the client would never build by itself (the
                # client trims a wave to the wire's own cap before it ever asks), aimed straight at
                # the route with urllib rather than through the browser, so this row proves the
                # SERVER'S OWN fence and not merely that the client stays under it.
                over_cap = ["cap-probe-%d" % i for i in range(RECORDS_CAP + 5)]
                try:
                    with urllib.request.urlopen(
                            base + RECORDS_ROUTE + "?ids=" + ",".join(over_cap), timeout=5) as resp:
                        cap_status = resp.status
                except urllib.error.HTTPError as e:
                    cap_status = e.code
                check(BROWSER_ROWS[10],
                      cap_status == 400,
                      f"a request for {len(over_cap)} ids over the route's own cap of {RECORDS_CAP} "
                      f"answered {cap_status}")

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
                elif ap is None:
                    # A ROW READS A RECORD OR IT REDS — IT NEVER RAISES (2026-08-19). The host took
                    # the passage and the composer's own register then carried no passage at all, so
                    # there is nothing to read a door reading off. Until today this state reached the
                    # rows below as a bare `None` and took the whole file down with an attribute
                    # error before a single result was flushed, which turns one red row into no run
                    # at all. It reds here instead, and it carries the diagnostic surface with it so
                    # the reason is in the failure rather than in a second run.
                    said = js(br, "return JSON.stringify(window.__exPass.report().refusals || []);")
                    for r_ in (BROWSER_ROWS[4], BROWSER_ROWS[5]):
                        check(r_, False,
                              "the host took the passage and the composer's own register carried no "
                              "passage, so no applied record exists to read; the refusal ring says "
                              + str(said)[:600])
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
                    # A READING MAY HAVE TWO ENDS, corrected 2026-08-19 at the judge seat. This row
                    # asked for a plain number and went red on every run where an instrument that
                    # plays its module ONCE PER WORK happened to be cast — `beat` publishes its
                    # period as `[periodA, periodB]`, `strata-light` its voices the same way, and
                    # both are the instrument reporting honestly rather than a broken shape. Which
                    # instrument wins a cast is a property of the pair and the die, so the row read
                    # as an intermittent red that moved with the roster: it fired far more often
                    # once the arsenal went from 17 castable instruments to 22 on 2026-08-18. What
                    # the row is for — the door is named, the reading was taken on the buffer the
                    # host reports, a refusal is a sentence — is untouched by accepting both forms.
                    def reading(v):
                        if isinstance(v, (int, float)) and not isinstance(v, bool):
                            return True
                        return (isinstance(v, list) and bool(v)
                                and all(isinstance(x, (int, float)) and not isinstance(x, bool)
                                        for x in v))

                    def law(c):
                        a = c["applied"]
                        buf = a.get("buffer") or []
                        why = a.get("whyNo")
                        return (a.get("door") in ("in", "out")
                                and len(buf) == 2
                                and f"{buf[0]}x{buf[1]}" == ap.get("buffer")
                                and isinstance(a.get("reads"), str)
                                and reading(a.get("request"))
                                and reading(a.get("applied"))
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
                records_before_stillness = len(RECORDS_LOG)
                with Browser(width=1280, height=900) as br2:
                    br2.emulate_media(prefers_reduced_motion="reduce")
                    enter(br2, base, "diagnostics:on")
                    # THE REASON IS READ OFF WHICHEVER CHANNEL STOOD THE VISIT DOWN (2026-08-19).
                    # Until the records moved off the settings block, a still visit still held every
                    # record, so a step reached the composer's own open and the sentence «reduced
                    # motion» was written there. A still visit now asks the route for nothing at all,
                    # so the composer is never reached and the sentence is written by the wave's own
                    # stand-down instead. The row asks the same question it always asked — is the
                    # reason on the surface, and is the file unfetched — and reads the whole ring for
                    # it rather than one channel of it.
                    red = js(br2, "var r = window.__exPass.report();"
                                  "var said = r.refusals.filter(function(x){"
                                  "  return x.why === 'reduced motion'; });"
                                  "return {state: r.composer.state,"
                                  " why: said.length ? said[said.length-1].why : null,"
                                  " files: performance.getEntriesByType('resource')"
                                  "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                                  "  .length};")
                    check(BROWSER_ROWS[8],
                          red["files"] == 0 and red["why"] == "reduced motion",
                          f"the file was fetched {red['files']} time(s); the reason on the "
                          f"surface: {red['why']!r}")

                    # 12 · EX-PASS-RECORDS: stillness carries no wave either. `passRecordsAskFor`
                    # reads the SAME stand-down gate `passOpen` does (engine/client/01a-pass.js,
                    # 2026-08-19 comment on the gate), so this is the same visit row 8 above already
                    # drove — the added claim is over the route's own log rather than the composer's
                    # resource entries.
                    check(BROWSER_ROWS[12],
                          len(RECORDS_LOG) == records_before_stillness,
                          f"the route's own log carried {records_before_stillness} request(s) "
                          f"before this visit and {len(RECORDS_LOG)} after — a visit standing still "
                          f"asks the route for nothing, the same as it asks the composer for nothing")

                # 11 · EX-PASS-RECORDS: a wave that never lands. FAIL_WAVE arms the harness's
                # `answer` hook (records_answer, above) to answer the NEXT `/api/pass/records` GET
                # with 500 — a real request the client's own fetch really receives and really has to
                # handle, the same road `passRecordsAskFor`'s own `.catch()` was written for (its
                # comment: "the wave for N id(s) did not land"). A fresh visit's very first wave is
                # the door's own spread, so arming it just before a fresh `enter()` sabotages exactly
                # that request. What the row asks: the refusal is said in plain words, the visitor
                # still lands, and a crossing over the now-unrecorded pair still freezes no score
                # onto the command — the walk's own glide, not a thrown error breaking the visit.
                FAIL_WAVE["on"] = True
                with Browser(width=1280, height=900) as br3:
                    enter(br3, base, "diagnostics:on")
                    said = []
                    for _ in range(30):
                        said = js(br3, "return window.__exPass.report().refusals.filter("
                                       "function(x){return x.what === 'records' "
                                       "&& x.name === 'wave';});")
                        if said:
                            break
                        br3.sleep(0.2)
                    landed = js(br3, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                                     ".map(function(e){return e.dataset.id;});")
                    fell = None if len(landed) < 2 else js(br3, """
                      var A = document.querySelector('.exh-frame[data-id="%s"]');
                      var B = document.querySelector('.exh-frame[data-id="%s"]');
                      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                                 kind:'step', cause:'wave-fails',
                                                                 velocity:0});
                      return {score: cmd ? cmd.score : 'no command'};
                    """ % (landed[0], landed[1]))
                    why = said[-1]["why"] if said else None
                    if len(landed) < 2:
                        skip(BROWSER_ROWS[11],
                             f"this hang shows fewer than two works: {landed[:4]}")
                    else:
                        check(BROWSER_ROWS[11],
                              bool(said) and "did not land" in (why or "") and fell is not None
                              and fell.get("score") is None,
                              f"the induced failure was noted: {why!r}; a step declared straight "
                              f"after it froze {fell.get('score') if fell else '?'!r} onto the "
                              f"command — the walk's own glide, not a throw that broke the visit")

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
