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
import threading
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
# `pickGenre`'s OWN CALL, READ RATHER THAN TRUSTED (2026-08-26 night-run separation). It is the one
# die in this file that used to cool a road off the mixed `walkMemory` pool by passing `dieWeighted`
# a plain `1`; the fix repoints it at the road's own pool by naming the fourth argument `"road"`
# instead, which is what `coolOfRoad` (beside `coolOf`, pass-composer.js) answers to. Read here as a
# source fact rather than assumed from the numbers below composing right, for the same reason
# `DOLLY_CAP_VALUE` above is read off the source and not retyped.
PICK_GENRE_CALL = re.search(
    r"function pickGenre\(pool, seed, key\) \{\s*"
    r"var at = dieWeighted\(pool\.map\(function \(r\) \{ return \{ id: r\.id, fit: r\.fit \}; \}\), "
    r"seed, key,(.{0,40}?)\);", COMPOSER_SRC, re.S)
PICK_GENRE_READS_ROAD = bool(PICK_GENRE_CALL) and '"road"' in PICK_GENRE_CALL.group(1)

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

# ---------------------------------------------------------------- the frozen cast is the fleet
# THE CAST THE TWO FIXTURES FREEZE MUST NAME EVERY INSTRUMENT THIS TREE SHIPS, and that is asked
# here as a verdict rather than noted in some other row's detail line.
#
# The reason is that this file's collection-wide rows take their REACH from `consts` in the two
# fixtures: the fill is only ever asked to cast what the cast names, the levels law is only ever
# asked about the handles those manifests carry, and the register roll call below reports an
# instrument the fixture omits BESIDE its verdict instead of failing on it. So an instrument missing
# from the frozen cast is an instrument no row in this file judges, and every row stays green while
# it ships unjudged. That is not a hypothetical: beat, gates, grid-colour, pour, strata-light,
# strata-scale, studio, tilt, veil, waterline and wind were all shipping and all unjudged, three of
# them landed the same day, and nothing reddened — because the reach of each row was set by the very
# file that had gone stale.
#
# The right-hand side is INSTRUMENT_ROSTER above, one entry per instrument FILE the tree ships, so
# an instrument that lands reddens this row on the day it lands and no second list of names is kept
# anywhere. `consts.instruments` and `consts.manifests` are both read, so a fixture widened in one
# and not the other does not pass. `tests/build_pass_fixture_consts.py` rebuilds both fixtures from
# the site's own staging step, and running it is what greens this row again.
_CAST_DRIFT = []
for _fx in (FIXTURE, WORKS):
    _fx_consts = json.loads(_fx.read_text(encoding="utf-8")).get("consts") or {}
    for _key in ("instruments", "manifests"):
        _named = sorted(_fx_consts.get(_key) or {})
        _absent = [i for i in INSTRUMENT_ROSTER if i not in _named]
        _phantom = [i for i in _named if i not in INSTRUMENT_ROSTER]
        if _absent or _phantom:
            _CAST_DRIFT.append(
                f"{_fx.name} consts.{_key} names {len(_named)} of the {len(INSTRUMENT_ROSTER)} "
                f"instrument(s) the tree ships"
                + (f"; shipping but uncast, so judged by no row here: {_absent}" if _absent else "")
                + (f"; cast but published by no file: {_phantom}" if _phantom else ""))

check("EX-COMPOSED the frozen cast names every instrument this tree ships — a fixture narrower than "
      "the fleet narrows the reach of every collection-wide row that reads it, silently",
      not _CAST_DRIFT,
      "; ".join(_CAST_DRIFT) if _CAST_DRIFT
      else f"{FIXTURE.name} and {WORKS.name} both name, under consts.instruments and "
           f"consts.manifests alike, the same {len(INSTRUMENT_ROSTER)} instrument(s) the tree "
           f"ships: {', '.join(INSTRUMENT_ROSTER)}")

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
# THE REGISTER'S SIX WORDS, and the row below is read against the list rather than against a copy
# of it. `transaction` stood here until the writer was made to dispatch on the word instead of on
# the handle's name; it covered four different sources at once, and it is now `progress`,
# `host-clock` and `plan` beside the two that already said what they meant.
# `entry-door` joined them on 2026-08-25, when the reserved dry landed across the fleet. It is not
# `progress` — that word promises a monotone rise across a handle's own published span and the
# writer keeps that promise literally — and it is not `plan`, which names a choice a score is free
# to make. The dry's shape is fixed by the entry-door contract and by where the cue stands in its
# own stack, so it is a law being stated, and the writer dispatches on the word rather than on the
# handle's name, which is the whole reason this list has six words in it and not one.
_REGISTER_WORDS = "measured|unmeasured|module-rest|progress|host-clock|plan|entry-door"
_REGISTERED = set(re.findall(
    r'^\s{4}"?([A-Za-z][A-Za-z0-9_.\-]*)"?: \["(?:' + _REGISTER_WORDS + r')"',
    MODULE.read_text(encoding="utf-8"), re.M))
# a scoped row (`"weave.depth"`) answers for that instrument's handle as well as the bare name does
_REGISTERED |= {h.split(".", 1)[1] for h in list(_REGISTERED) if "." in h}
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
    "EX-COMPOSED the camera's floor-and-lift and the voice's own loudness hold for EVERY value "
    "their arguments can take, walked over the whole span each one has",
    "EX-COMPOSED red-on-bug · the carrying axis lifted against another axis's ceiling: a pitch "
    "passage flies half the grain it owes",
    "EX-COMPOSED the passage's length is composed from the pair inside the band its tier names, and "
    "the band holds over the whole span of the reading that places it",
    "EX-COMPOSED red-on-bug · the length taken off the band's own floor again: two different pairs "
    "at one role run the same milliseconds",
    "EX-COMPOSED the miracle is counted by what an instrument declares about itself, so every "
    "world-declaring instrument that is cast is voiced the miracle",
    "EX-COMPOSED red-on-bug · the miracle counted by an effect's name again: three instruments fold "
    "the space and spend nothing for it",
    "EX-COMPOSED a step whose role spends no miracle never opens a world, and the gate that holds "
    "that is a bound rather than the ranking's own nudge",
    "EX-COMPOSED red-on-bug · the nudge and the three follow-up gates removed: a quiet link opens "
    "the world",
    "EX-COMPOSED two instruments that each declare the world never stand in one crossing, by either "
    "of the two roads that put them within reach",
    "EX-COMPOSED red-on-bug · the levels test's world clause removed: a world ground takes a world "
    "arrival beside it",
    "EX-COMPOSED every handle every published instrument publishes declares the structural level it "
    "drives, and no handle claims a seventh level or one its own instrument never declared",
    "EX-COMPOSED one active voice per structural level, the ground included: no cue drives a handle "
    "on a level it does not own, and no level is driven by two cues at once",
    "EX-COMPOSED red-on-bug · the handles of an unowned level left on the track list: a ground and a "
    "voice above it cut the same way",
    "EX-COMPOSED every handle whose register row promises a value is given one: no row saying it "
    "reads a measurement, the passage's travel or a plan's word lands frozen at its own default",
    "EX-COMPOSED red-on-bug · the writer dispatching on the handle's name again: a row promising the "
    "passage's own travel holds still for the whole of it",
    "EX-COMPOSED the cast is not narrowed by the levels law: the two named pairs whose ground and "
    "voice share a level both compose, with the non-owner playing on where it owns",
    "EX-COMPOSED a voice standing over another joins at no presence and stands down the same way, "
    "and the lowest voice of a stack is whole throughout",
    "EX-COMPOSED the step's harmonic function reaches the composer, is held to its own three names, "
    "and is what says whether the crest suspends",
    "EX-COMPOSED what a cue declares it costs is its own instrument's declaration, per quality "
    "variant, and never one block this file types",
    "EX-COMPOSED the day arrives on the request, biases the roll, and leaves a request that states "
    "none reproducible",
    "EX-COMPOSED the letter cooldown's floor is bounded by the walk's own vocabulary and never by "
    "how long the visit has run, so a road just played cannot lose to an arbitrarily worse rival "
    "for no reason but the log's own length, over the whole span of place and pool size either "
    "can take",
    "EX-COMPOSED a road's own cooldown reads a pool of the walk's eight roads and never the mixed "
    "pool a visit's instruments also stand in, so the floor for a road just played stays fixed at "
    "1/9 however many instruments the same walk has cast",
    "EX-COMPOSED a fold spends the crossing's one miracle the first time a walk plays it and never "
    "again, freeing the slot for another fold in the same crossing",
    "EX-COMPOSED red-on-bug · the miracle read off the static mark again: the same fold spends it "
    "twice on one nine-step walk",
    "EX-COMPOSED red-on-bug · one shared cooling pool given back to roads and letters: a road's own "
    "floor divides by the mixed list again",
]
# THE ROWS THIS FILE READS BY NAME rather than by position. Every row above is addressed by its
# index, which is fine while the list only ever grows at the end — and it stopped being fine the
# moment two rows landed there in one night: the first took `NODE_ROWS[-1]` and the second silently
# took it away. A name cannot be taken away by a neighbour.
ROW_ENTRY_DOOR = NODE_ROWS[-9]
ROW_HARMONIC = NODE_ROWS[-8]
ROW_COST = NODE_ROWS[-7]
ROW_DAY = NODE_ROWS[-6]
ROW_COOLDOWN_ARITH = NODE_ROWS[-5]
ROW_ROAD_POOL = NODE_ROWS[-4]
ROW_MIRACLE_RARITY = NODE_ROWS[-3]
ROW_MIRACLE_RARITY_RED = NODE_ROWS[-2]
ROW_ROAD_POOL_RED = NODE_ROWS[-1]

# THE DRIVER, run in node against a COPY of the module held in memory. `PLANTS` names the rules to
# change before the module is loaded, which is how every red-on-bug row below is run: the repair is
# reverted in the copy alone and the answer must move. `SWEEP` says how many of the collection's
# works the collection-wide readings walk, so a planted run can walk a corner of it and the standing
# rows walk all 121.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
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
// AND THE BYTE FENCE BESIDE IT, BY THE SAME ROAD AND FOR A HARDER REASON (2026-09-01). The prose
// fence's absence from the fixture only meant a longer line; the byte fence's absence means
// `fitTheWeight` returns on its own first line — «a score with no fence published is left exactly
// as it was composed» — so the composer under test sheds NOTHING, and the fence row measures a
// composer that was never asked to fit. The fixture carried `scoreFenceBytes` until 2e68cb0 wrote
// it out truncated; 090e8e9 repaired the truncation and restored `pair` and `expectedTight` but not
// this field, and the row went red on 42 unfitted scores with the engine untouched. Handing it in
// from the client closes that for good: this suite can no longer measure a fenceless composer,
// whatever a frozen fixture happens to carry, and the number is the client's own exactly as the
// prose fence above is.
fix.consts.scoreFenceBytes = BYTE_CAP;

// EACH HANDLE'S OWN STRUCTURAL LEVEL, CARRIED IN FROM THE INSTRUMENT'S OWN FILE. A handle declares
// the level it drives in the manifest its own file registers, which is the one home of that fact;
// the frozen fixture predates the declaration and is not re-based for it, exactly as the client's
// two fences are handed in above rather than copied into it. So every published instrument's file is
// loaded here, its manifest read, and the level written onto the fixture's own copy — the same value
// by the same road, and a file that gains or moves a level re-bases this by itself.
//
// A PUBLISHED HANDLE THAT DECLARES NO LEVEL IS RECORDED AND NOT DEFAULTED. Reading a missing
// declaration as "drives nothing" would read exactly like today's behaviour and hide a half-done
// migration, so the names travel out on `out.levels.undeclared` and the row below reds on them.
const levelsUndeclared = [], levelsSeen = {}, levelsByInstrument = {}, live = {};
{
  const assetsDir = path.dirname(modulePath);
  for (const f of fs.readdirSync(assetsDir).filter((n) => /^pass-inst-.*\.js$/.test(n))) {
    const isrc = fs.readFileSync(path.join(assetsDir, f), "utf8").replace(/@@NS@@/g, "");
    const sb = {window: {__PassInstrument: (r) => { live[r.instrument.name] = r.instrument.manifest; }},
                console, document: undefined};
    vm.createContext(sb);
    vm.runInContext(isrc, sb, {filename: f});
  }
  // THE DECLARATION IS READ OFF EVERY INSTRUMENT FILE THE ENGINE SHIPS, not off the subset this
  // fixture froze. A migration that closed the ban for the instruments one fixture happens to carry
  // and left it open for the rest would be the worst of the three states — closed for some,
  // silently open for others — so the roll call below is the whole assets directory, and only the
  // OVERLAY is limited to the manifests this fixture hands the composer.
  for (const iid of Object.keys(live).sort()) {
    const theirs = live[iid].handles || {};
    const mine = (fix.consts.manifests[iid] || {}).handles || null;
    levelsByInstrument[iid] = {};
    for (const h of Object.keys(theirs).sort()) {
      const spec = theirs[h];
      if (!spec || !("level" in spec)) { levelsUndeclared.push(iid + "." + h); continue; }
      if (mine && mine[h]) mine[h].level = spec.level;
      levelsByInstrument[iid][h] = spec.level;
      if (spec.level) levelsSeen[spec.level] = (levelsSeen[spec.level] || 0) + 1;
    }
  }
}

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
// THE ANGLE FOLLOWS THE SAME ORDER OF PREFERENCE AS THE STEP, NOT THE STEP'S PRESENCE — the rule
// pass-composer.js:4401-4416 states and takes (2026-08-24). This function used to ask whether a
// DEVICE was recovered and then take that device's angle whatever it read, and a ring-cut or
// tile-cut work carries a device with a real step and NO direction at all: `ownDevice.angleDeg`
// stands at 0 on 114 of the collection's 121 records. Read that way the roll axis sees two works at
// one angle wherever both were cut that way, and folds an excursion of nothing out of them. The
// work's own measured grid angle is a reading of the same thing and it answers where the device's
// says nothing, so the device speaks first only where it recovered a direction.
function camLattice(w) {
  var st = w.structure || {};
  var stepPx = Number((st.ownDevice || {}).stepPx) || 0;
  var gridPx = Number((st.grid || {}).periodPx) || 0;
  var angle = Number((st.ownDevice || {}).angleDeg) || Number((st.grid || {}).angleDeg) || 0;
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
function camExpected(fromW, toW, carried) {
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
  // own grain sets — `camVoiceFloor` below. The lift is `(floor + (1 − floor)·share) / share`, so
  // the reading still spends the whole span above the floor, the shape of every axis is carried
  // through untouched, and nothing passes its own ceiling. Re-derived here from the raw record, as
  // every other line of this function is.
  //
  // AND THE CEILING THE FLOOR IS TAKEN AGAINST IS THE CARRYING AXIS'S OWN, which is why `carried`
  // is handed in. The grain asks for an ANGLE, 2·grainFrac; the axes are compared as SHARES; and
  // the three do not share one ceiling — roll and yaw reach DOLLY_CAP, pitch reaches half of it.
  // The same angle is therefore a different share on each axis, twice as large on pitch as on the
  // other two. A floor taken against DOLLY_CAP and then spent on pitch buys pitch half the angle
  // the grain asked for; re-deriving it that way here would mean this function agreed with a
  // composer that only ever half-lifted its pitch, and the row below would have nothing to catch
  // it with. Which axis carries is read off the composer's own output rather than re-run here (the
  // tie-break is its own die, see the note above), exactly as expRoll/expYaw/expPitch already are.
  var eCeiling = carried === "pitch" ? 0.5 * DOLLY_CAP : DOLLY_CAP;
  var eRollShare = Math.abs(rollRaw) / DOLLY_CAP;
  var eYawShare = Math.abs(yawRaw) / DOLLY_CAP;
  var ePitchShare = Math.max(Math.abs(pitchFrom), Math.abs(pitchTo)) / (0.5 * DOLLY_CAP);
  var eMaxShare = Math.max(eRollShare, eYawShare, ePitchShare);
  var eFloor = camVoiceFloor(fromW, toW, eCeiling);
  var eLift = (eFloor > 0 && eMaxShare > 0)
    ? (eFloor + (1 - eFloor) * eMaxShare) / eMaxShare : 1;
  rollRaw *= eLift; yawRaw *= eLift;
  pitchFrom *= eLift; pitchTo *= eLift; pitchInTied *= eLift;
  return {reach: reach, panFrom: panFrom, panTo: panTo, logScale: logScale,
          rollRaw: rollRaw, rollFraction: rollFraction, yawRaw: yawRaw, yawFraction: yawFraction,
          pitchFrom: pitchFrom, pitchTo: pitchTo, pitchInTied: pitchInTied,
          voiceFloor: eFloor, voiceLift: eLift, voiceCeiling: eCeiling};
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
// is stated in — through θ·0.5, so one element of grain asks θ ≥ 2·grainFrac. That is an ANGLE, and
// an angle is only a share once it is divided by the ceiling of the axis that will fly it: the same
// θ is twice the share on pitch, whose ceiling is half of DOLLY_CAP, that it is on roll or yaw. So
// the ceiling is an ARGUMENT here and never DOLLY_CAP by default — a floor that assumed the widest
// of the three ceilings would let a half-lifted pitch through unremarked. Nothing here is a number
// of taste: every term is a reading off the two records or a bound already published in the
// composer.
function camGrainFrac(w) {
  var side = Number(w.frameSide) || 0;
  var px = camLattice(w).latticePx;
  return side > 0 && px > 0 ? px / side : 0;
}
function camVoiceFloor(fromW, toW, ceiling) {
  var a = camGrainFrac(fromW), b = camGrainFrac(toW);
  if (!(a > 0) || !(b > 0) || !(ceiling > 0)) return 0;
  var f = 2 * Math.min(a, b) / ceiling;
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
let accSightings = 0;
const accStillDriven = [];
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
  // A CUE THAT DOES NOT OWN THE LEVEL NOW CARRIES NO NODE FOR THESE HANDLES AT ALL. Until the
  // per-handle levels landed, `fillPlan` simply never wrote a value for them and the node writer
  // resolved each to the manifest's own 0; now the handles are taken off such a cue's track list,
  // so there is no node to read a zero off. Both are the same silence and the second is the
  // stronger one, so what the accompanying side records is the SIGHTING and any handle that still
  // has a node — an empty reading list is the law kept, not an empty spot-check.
  if (!owns) accSightings++;
  for (const h of handles) {
    const node = cue.nodes[cue.id + "-" + h];
    if (node) bucket[h].push(toNum(startValue(node)));
    if (!owns && node && accStillDriven.indexOf(cue.instrument.id + "." + h) < 0) {
      accStillDriven.push(cue.instrument.id + "." + h);
    }
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
// WHICH INSTRUMENTS CAN EVER SPEND THE MIRACLE, read off `composer.worldFoldInstruments` — the one
// home naряд S-18 (2026-08-27) gave this fact once `spendsTheMiracle` stopped reading a manifest
// mark that doubled as shelf 17's own camera-ownership law. This names CAPABILITY, exactly as the
// old manifest scan did: whether a given cast of one of these four actually SPENDS the crossing's
// one impossible event now also depends on `walkMiracles`, the walk's own history, which the sweep
// below never sends — so every read of this list, with no walk behind it, still answers "first
// play" for each of the four exactly as the old always-on mark did. The row that proves the history
// itself is its own, separate row (below).
const SPENDS_THE_MIRACLE = composer.worldFoldInstruments.slice().sort();
const folded = {}, worldCue = {}, ledAndWorld = {}, twoMiracles = {}, roleThrew = {}, roleN = {};
const foldUnspent = {}, worldsCast = {}, worldStack = {}, worldNotVoiced = {};
const worldSeen = {};
for (const r of ROLES_ALL) { folded[r] = 0; worldCue[r] = 0; ledAndWorld[r] = 0;
                             twoMiracles[r] = 0; roleThrew[r] = null; roleN[r] = 0;
                             foldUnspent[r] = 0; worldsCast[r] = 0; worldStack[r] = 0;
                             worldNotVoiced[r] = 0; }
let boxQualified = 0;
// Breaches of shelf 17's levels law, counted at the handles: a cue driving a handle whose
// level it does not own, and a level driven by two cues at once. Both must stand at nothing.
let levelBreaches = 0, levelSharedBy = 0;
// Handles whose register row promises a value, held against what the composition wrote.
const REGISTER = composer.handleSource;
const promiseSeen = [], promiseKept = [], promiseKind = {};
const levelBreachCases = [], levelSharedCases = [];
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
        const got1 = track[1], got2 = track[2];
        const close = (a, b) => Math.abs(toNum(a) - b) < 0.0006;
        const nz = (v) => Math.abs(toNum(v)) > 1e-9;
        // WHICH AXIS THE COMPOSER ACTUALLY CARRIED, read off its own output — the palindrome ban's
        // tie-break is the composer's own die and is not reproduced here (see the note above
        // camExpected). At most one of roll/yaw/pitch may be non-zero at either point; that
        // invariant is asserted directly rather than assumed. It is read BEFORE the re-derivation
        // because the re-derivation needs it: the voice floor is a share of the carrying axis's own
        // ceiling, and the three axes do not publish one ceiling between them.
        const carried = (nz(got1.roll) || nz(got2.roll)) ? "roll"
          : (nz(got1.yaw) || nz(got2.yaw)) ? "yaw"
          : (nz(got1.pitch) || nz(got2.pitch)) ? "pitch" : "none";
        const exp = camExpected(fromWork, toWork, carried);
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
        // THE CARRYING AXIS'S OWN LEVEL, against the level the pair's own grain sets. BOTH sides of
        // the comparison stand on the SAME ceiling — the carrying axis's own — and that is the whole
        // content of the check. The share worn is `magnitude / thatAxis'sCeiling`; the level asked
        // for is `2·grainFrac / thatAxis'sCeiling`. Divide the angle by one ceiling and the
        // magnitude by another and the comparison silently passes for any pitch-carried pair that
        // travelled half the angle it owed, which is exactly the shape a floor taken against
        // DOLLY_CAP alone produces.
        if (carried !== "none") {
          const ceiling = carried === "pitch" ? 0.5 * DOLLY_CAP : DOLLY_CAP;
          const worn = Math.max(Math.abs(toNum(got1[carried])), Math.abs(toNum(got2[carried])));
          const share = ceiling > 0 ? worn / ceiling : 0;
          const floorAsked = camVoiceFloor(fromWork, toWork, ceiling);
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
      // WHAT THE REGISTER PROMISED, AGAINST WHAT THE COMPOSITION WROTE. This is the gate that was
      // missing, and its shape is the point. The row it replaces walked a cue's nodes and SKIPPED
      // any whose note did not open with «requested» — so it went blind on exactly the handles the
      // writer had declined to write a note for, which is precisely where the defect lives. This
      // one runs the other way about: it starts from the register's own word and asks whether the
      // composition kept it.
      //
      // A row saying `measured`, `progress` or `plan` promises a value. A node standing at
      // `{op:"static"}` with no provenance on it is the writer's own mark for «nobody drove this»,
      // so the two together are a broken promise. `unmeasured` and `module-rest` promise nothing and
      // resting is the honest answer for both.
      for (const cue of q.plan.cues) {
        const iid = cue.instrument.id;
        for (const h of Object.keys(cue.tracks || {})) {
          const kind = REGISTER[iid + "." + h] || REGISTER[h] || null;
          if (["measured", "progress", "plan"].indexOf(kind) < 0) continue;
          const node = cue.nodes[(cue.tracks[h] || {}).node || (cue.id + "-" + h)];
          const frozen = !node || (node.op === "static" && !node.note);
          const key = iid + "." + h;
          if (promiseSeen.indexOf(key) < 0) promiseSeen.push(key);
          promiseKind[key] = kind;
          if (!frozen && promiseKept.indexOf(key) < 0) promiseKept.push(key);
        }
      }
      // SHELF 17'S LEVELS LAW, READ OFF WHAT EACH CUE ACTUALLY DRIVES. A cue drives a handle when
      // that handle has a track on it, and a handle declares the structural level it drives. So a
      // breach here is a cue driving a handle on a level it does not own — pattern stacked on
      // pattern, the thing a person sees. The ground is read exactly like every other cue: it holds
      // no exemption any more.
      {
        const drivenBy = {};
        for (const cue of q.plan.cues) {
          const man = fix.consts.manifests[cue.instrument.id].handles;
          for (const h of Object.keys(cue.tracks || {})) {
            const lv = (man[h] || {}).level;
            if (!lv) continue;
            if ((cue.levelOwnership || {})[lv] !== "owns") {
              levelBreaches++;
              if (levelBreachCases.length < 4) {
                levelBreachCases.push({role: r, cue: cue.id, instrument: cue.instrument.id,
                                       handle: h, level: lv,
                                       ownership: (cue.levelOwnership || {})[lv] || null});
              }
            }
            if (!drivenBy[lv]) drivenBy[lv] = {};
            drivenBy[lv][cue.id] = [Number(cue.window[0]), Number(cue.window[1])];
          }
        }
        // AND NO LEVEL IS DRIVEN BY TWO CUES THAT ARE LIVE TOGETHER, which is the same law read
        // from the level's side rather than the cue's. The words «at once» carry it: shelf 17 bars
        // two ACTIVE voices from one level, and two cues whose windows never meet are not two
        // active voices — which is the release `castForKinds` already grants at the cast, and which
        // ownership takes back the moment it forgets the windows.
        for (const lv of Object.keys(drivenBy)) {
          const who = Object.keys(drivenBy[lv]).sort();
          for (let x = 0; x < who.length; x++) {
            for (let y = x + 1; y < who.length; y++) {
              const A = drivenBy[lv][who[x]], B = drivenBy[lv][who[y]];
              if (A[0] < B[1] && B[0] < A[1]) {
                levelSharedBy++;
                if (levelSharedCases.length < 4) {
                  levelSharedCases.push({role: r, level: lv, cues: [who[x], who[y]],
                                         windows: [A, B]});
                }
              }
            }
          }
        }
      }
      const cues = q.score.cues;
      for (const x of cues) chosen[x.instrument.id] = (chosen[x.instrument.id] || 0) + 1;
      // WHICH CUES OF THIS CROSSING SPEND THE MIRACLE, by the declaration and never by the name.
      // `folded` and `foldUnspent` read `=== "boxfold"` until now, which is one of the four
      // instruments the collection publishes that declare the world: the other three folded the
      // space a work lives in and were counted as nothing at all.
      const worldCues = cues.filter((x) => SPENDS_THE_MIRACLE.indexOf(x.instrument.id) >= 0);
      for (const x of worldCues) {
        worldSeen[x.instrument.id] = (worldSeen[x.instrument.id] || 0) + 1;
        if (x.voice !== "miracle") worldNotVoiced[r]++;
      }
      if (worldCues.length) { folded[r]++; worldsCast[r]++; }
      // SHELF 6: THE SLOT IS CONSUMED AND NEVER STACKS. Two instruments that each declare the world
      // are two impossible events whatever their windows and whichever of them holds the ground, so
      // this counts the crossings that carry more than one.
      if (worldCues.length > 1) worldStack[r]++;
      const claimsWorld = cues.some((x) => (x.levels || []).indexOf("WORLD") >= 0);
      if (claimsWorld) worldCue[r]++;
      if (claimsWorld && q.score.camera.lead) ledAndWorld[r]++;
      const miracles = cues.filter((x) => x.voice === "miracle").length;
      if (miracles > 1) twoMiracles[r]++;
      // A CROSSING THAT FOLDS THE FRAME AND SPENDS NO MIRACLE FOR IT has lost the law rather than
      // kept it: the fold IS the impossible event, so a folding score with no miracle voice means
      // the slot went unspent and a second impossible thing could stand beside it.
      if (worldCues.length && miracles === 0) foldUnspent[r]++;
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
// ---------------------------------------------------------------- THE ENTRY DOOR
// The charter's build ladder, step 0: a voice must be able to join a running picture without
// replacing it. The fleet's reserved dry is `presence`, and the plan's half of the contract is
// what this block puts to the composer.
//
// WHY THE MANIFESTS ARE PATCHED HERE RATHER THAN READ. The settings record this suite composes
// against is the one the site's staging step last published, and it was published before the dry
// landed: nine of the ten instruments that now declare it ship a manifest here without it, so the
// composer's own `tracksFor` builds no track for a handle the record never named. Patching the
// record is not inventing a reading — the handle's four numbers are the contract's own, quoted
// from `docs/design/ENTRY-DOOR.md`, identical in every instrument's file, and the moment the site
// stages again the record carries exactly this. `overlay` is left alone on purpose: its own
// `presence` is a LIGHT-COLOUR reading of the pair and means something else, and the row below
// asks that the composer tell the two apart.
{
  const DRY = {min: 0, max: 1, def: 1, level: null,
               unit: "whether this voice is in the frame at all"};
  const consts2 = JSON.parse(JSON.stringify(fix.consts));
  let patched = 0;
  for (const iid of Object.keys(consts2.manifests)) {
    if (!consts2.manifests[iid].handles.presence) {
      consts2.manifests[iid].handles.presence = JSON.parse(JSON.stringify(DRY));
      patched += 1;
    }
  }
  const c2 = joined.make(consts2);
  let upperSeen = 0, lowestSeen = 0, overlaySeen = 0;
  const badUpperDoor = [], badUpperArc = [], badLowestDoor = [], badLowestWhole = [], badOverlay = [];
  for (const [x, y] of SPOT) {
    const wa = works.works[x], wb = works.works[y];
    if (!wa || !wb) continue;
    for (const role of ["entrance", "quiet link", "middle", "culmination", "return"]) {
      const key = x + "__" + y + "__ab";
      let p = null;
      try {
        p = c2.passageFor({workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                           seed: die(key + role), routeRole: role});
      } catch (e) { badUpperArc.push([key, role, "threw: " + e.message]); continue; }
      if (!p || !p.score) continue;
      for (const cue of p.score.cues) {
        const iid = cue.instrument.id;
        const track = (cue.tracks || {}).presence;
        const door = (cue.doors || {})["in"] || {};
        const out2 = (cue.doors || {}).out || {};
        if (iid === "overlay") {
          // The scoped row: `overlay`'s presence is a reading of the pair, so its door must still
          // be the crossing dial and its track must not carry the contract's arc.
          if (track) {
            overlaySeen += 1;
            const nd = (cue.nodes || {})[track.node] || {};
            if (door.handle !== "mix" || nd.op === "spline") {
              if (badOverlay.length < 3) badOverlay.push([key, role, door.handle, nd.op]);
            }
          }
          continue;
        }
        if (!track) continue;
        const nd = (cue.nodes || {})[track.node] || {};
        if (Number(cue.stack) > 0) {
          upperSeen += 1;
          if (!(door.handle === "presence" && toNum(door.value) === 0
                && out2.handle === "presence" && toNum(out2.value) === 0)) {
            if (badUpperDoor.length < 3) {
              badUpperDoor.push([key, role, cue.id, iid, door.handle, toNum(door.value),
                                 out2.handle, toNum(out2.value)]);
            }
          }
          const pts = (nd.points || []).map((q) => [toNum(q.at), toNum(q.value)]);
          const overCue = nd.op === "spline" && nd.in && nd.in.source === "cueProgress";
          if (!(overCue && pts.length === 3
                && pts[0][0] === 0 && pts[0][1] === 0
                && pts[1][0] === 0.5 && pts[1][1] === 1
                && pts[2][0] === 1 && pts[2][1] === 0)) {
            if (badUpperArc.length < 3) {
              badUpperArc.push([key, role, cue.id, iid, nd.op,
                                nd.in ? nd.in.source : null, pts]);
            }
          }
        } else {
          lowestSeen += 1;
          // `presenceWhyNo` in the host refuses a score whose LOWEST cue names a door at no
          // presence at all. The composer must never write one.
          if ((door.handle === "presence" && toNum(door.value) === 0)
              || (out2.handle === "presence" && toNum(out2.value) === 0)) {
            if (badLowestDoor.length < 3) {
              badLowestDoor.push([key, role, cue.id, iid, door.handle, toNum(door.value),
                                  out2.handle, toNum(out2.value)]);
            }
          }
          if (!(nd.op === "static" && toNum(nd.value) === 1)) {
            if (badLowestWhole.length < 3) {
              badLowestWhole.push([key, role, cue.id, iid, nd.op, toNum(nd.value)]);
            }
          }
        }
      }
    }
  }
  out.entryDoor = {patched, upperSeen, lowestSeen, overlaySeen,
                   badUpperDoor, badUpperArc, badLowestDoor, badLowestWhole, badOverlay};
}

// ---------------------------------------------------------------- WHAT A CUE COSTS
// §7: the INSTRUMENT declares what it costs, per quality variant, and the host grants against that
// declaration and then counts what was created against it. The composer's job is to carry the
// declaration onto the cue and never to author one — a cost the composer invented is a number the
// host would measure a real instrument against.
//
// The composer typed ONE block for every cue of every score at every quality, so no crossing could
// declare a cost different from any other and the quality ladder could not be walked on cost. This
// block asks the repair the way the entry door's is asked: the settings record is patched with a
// declaration that is DIFFERENT per instrument and per variant, and the row asks that what reaches
// the cue is that instrument's own row and not one number repeated.
//
// The numbers below are arbitrary and deliberately so — they are a fingerprint, not a measurement.
// What is being read is which declaration reaches which cue, and a fingerprint that is distinct per
// instrument and per variant is the only thing that can answer it.
{
  const consts3 = JSON.parse(JSON.stringify(fix.consts));
  const iids = Object.keys(consts3.manifests).sort();
  const VARIANTS = ["lean", "standard", "rich"];
  const want = {};
  iids.forEach((iid, k) => {
    want[iid] = {};
    VARIANTS.forEach((v, j) => {
      want[iid][v] = {bytesEstimate: 1000 * (k + 1) + j, framebuffers: k % 3, passes: 1 + j,
                      pingPong: j, programs: 1 + (k % 2), textureSlots: 2 + j, textures: k % 4};
    });
    consts3.manifests[iid].resources = JSON.parse(JSON.stringify(want[iid]));
  });
  const c3 = joined.make(consts3);
  let checked = 0;
  const wrong = [], flatVariants = [];
  for (const [x, y] of SPOT) {
    const wa = works.works[x], wb = works.works[y];
    if (!wa || !wb) continue;
    for (const role of ROLES_ALL) {
      let p = null;
      try {
        p = c3.passageFor({workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                           seed: die(x + "__" + y + "__ab"), routeRole: role});
      } catch (e) { wrong.push([x, y, role, "threw " + e.message]); continue; }
      if (!p || !p.score) continue;
      for (const cue of p.score.cues) {
        const w = want[cue.instrument.id];
        if (!w) continue;
        for (const v of VARIANTS) {
          checked += 1;
          const got2 = (cue.resources || {})[v] || {};
          for (const f of Object.keys(w[v])) {
            if (got2[f] !== w[v][f] && wrong.length < 4) {
              wrong.push([cue.instrument.id, v, f, got2[f], w[v][f]]);
            }
          }
        }
        const lean = JSON.stringify((cue.resources || {}).lean || null);
        const rich = JSON.stringify((cue.resources || {}).rich || null);
        if (lean === rich && flatVariants.length < 3) flatVariants.push([cue.instrument.id, lean]);
      }
    }
  }
  out.cost = {checked, wrong, flatVariants, declarations: iids.length};
}

// ---------------------------------------------------------------- THE DAY ON THE REQUEST
// Charter shelf 16's third dice step. `weatherNow` called `new Date()` and was the last thing in
// the composer a pinned run could not reproduce: one request at one seed composed two different
// scores an hour apart, and the family a return is matched against moved with the hour. The shelf's
// own last two sentences settle the collision — seeds and determinism are the JUDGING mode,
// ephemerality is the VIEWER mode — so the day is an input the walk states in the mode that has
// one, never a call the composer makes.
//
// TWO THINGS ARE ASKED, and the second matters as much as the first: the step must still WORK.
// Deleting a clock is easy and it would leave shelf 16's third step deleted with it, silently.
//
//   · REPRODUCIBLE. One request stating no day, composed twice, is byte-identical — and stating a
//     day does not break that either: the same day twice is the same score.
//   · STILL A BIAS. Two requests differing in NOTHING but the day compose differently on some pair,
//     so the day still reaches the die it was written for.
//   · FENCED. A day that is no instant is left unread and recorded, and reads as neutral.
{
  const askDay = (x, y, day) => {
    const req = {workRecordA: works.works[x], workRecordB: works.works[y], direction: "a-to-b",
                 seed: die(x + "__" + y + "__ab"), routeRole: "middle"};
    if (day !== undefined) req.day = day;
    return composer.passageFor(req);
  };
  // Two instants a long way apart in the day and in the year, so the hue wheel, the light curve and
  // the tempo curve all stand somewhere else. They are two numbers on a request, not a measurement.
  const DAY_ONE = Date.UTC(2026, 0, 15, 3, 0, 0), DAY_TWO = Date.UTC(2026, 6, 2, 15, 0, 0);
  let pairs = 0, moved = 0, unstable = 0, dayUnstable = 0;
  const firstMove = [];
  // A SLICE OF THE CORNER, EVERY FOURTH PAIR, and the slice is a cost rather than a claim: each
  // pair here composes five whole passages and what is being asked is whether the day reaches a die
  // at all, which one pair answers and the rest only make louder. The slice is taken by position in
  // the corner's own settled order, so it is the same slice on every run.
  for (const [x, y] of SPOT.filter((_, k) => k % 4 === 0)) {
    const none1 = askDay(x, y), none2 = askDay(x, y);
    const one = askDay(x, y, DAY_ONE), oneAgain = askDay(x, y, DAY_ONE);
    const two = askDay(x, y, DAY_TWO);
    if (!none1.score || !one.score || !two.score) continue;
    pairs += 1;
    if (none1.json !== none2.json) unstable += 1;
    if (one.json !== oneAgain.json) dayUnstable += 1;
    if (one.json !== two.json) {
      moved += 1;
      if (firstMove.length < 1) firstMove.push([x + "__" + y, one.plan.pivot.kind, two.plan.pivot.kind]);
    }
  }
  const [sx, sy] = SPOT[0];
  const stray = askDay(sx, sy, "not an instant");
  out.day = {
    pairs, moved, unstable, dayUnstable,
    readsNone: (askDay(sx, sy).request || {}).day,
    readsOne: (askDay(sx, sy, DAY_ONE).request || {}).day,
    strayRead: (stray.request || {}).day,
    strayRecorded: ((stray.request || {}).unread || []).filter((u) => /^day /.test(u)),
    strayMatchesNone: stray.json === askDay(sx, sy).json,
    firstMove
  };
}

// ---------------------------------------------------------------- THE HARMONIC FUNCTION
// The client writes `routeFunction` beside `routeRole` and has done since the harmonic layer
// landed. Two things are asked here.
//
//   · THE FENCE. The field is read, held to the three names, defaulted off the role where the walk
//     states none, recorded on the request, and a stray value is RECORDED rather than charged to
//     the visitor — the road every other field of this request already takes.
//   · THE CREST (charter shelf 15: the crest law is the culmination's suspension). Whether the
//     cue's shared course dwells at its middle is read off the step's FUNCTION and no longer off
//     the two works' tone alone. A dominant suspends; a tonic and a subdominant do not. Tone still
//     says how long the hold is and where it sits.
//
// HOW A HOLD IS READ HERE: the course is a spline over the cue's own progress, and it dwells when
// it carries FOUR points — the two middle ones at one value — against three for a passage through.
// That is the shape `pass-layer.js`'s own `splineSlopes` zeroes both tangents of, which is what
// makes the dwell read as the picture standing still.
{
  const courseOf = (cue) => {
    const names = Object.keys(cue.nodes || {}).filter((k) => /-course(-shared)*$/.test(k));
    return names.length ? cue.nodes[names[0]] : null;
  };
  const holdsIn = (p) => {
    let held = 0, passed = 0;
    for (const cue of (p.score ? p.score.cues : [])) {
      const c = courseOf(cue);
      if (!c || c.op !== "spline") continue;
      if ((c.points || []).length >= 4) held += 1; else passed += 1;
    }
    return {held, passed};
  };
  const ask = (x, y, role, fn) => {
    const wa = works.works[x], wb = works.works[y];
    const req = {workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                 seed: die(x + "__" + y + "__ab"), routeRole: role};
    if (fn !== undefined) req.routeFunction = fn;
    return composer.passageFor(req);
  };
  // 1 · THE FENCE. One pair, one seed, one role, three ways of stating the function.
  const [fx, fy] = SPOT[0];
  const plain = ask(fx, fy, "middle");
  const asDom = ask(fx, fy, "middle", "dominant");
  const stray = ask(fx, fy, "middle", "plagal");
  // 2 · THE CREST, over the same settled corner every other row here walks, at every role.
  let tonicHeld = 0, tonicSeen = 0, domSeen = 0, domHeld = 0, subHeld = 0, subSeen = 0;
  const tonicWitness = [], subWitness = [];
  for (const [x, y] of SPOT) {
    for (const role of ROLES_ALL) {
      const p = ask(x, y, role);
      if (!p.score) continue;
      const fn = p.request.routeFunction;
      const {held, passed} = holdsIn(p);
      if (fn === "tonic") {
        tonicSeen += held + passed;
        tonicHeld += held;
        if (held && tonicWitness.length < 3) tonicWitness.push([x + "__" + y, role]);
      } else if (fn === "dominant") {
        domSeen += held + passed;
        domHeld += held;
      } else {
        subSeen += held + passed;
        subHeld += held;
        if (held && subWitness.length < 3) subWitness.push([x + "__" + y, role]);
      }
    }
  }
  out.harmonic = {
    read: plain.request ? plain.request.routeFunction : null,
    readWhenStated: asDom.request ? asDom.request.routeFunction : null,
    readWhenStray: stray.request ? stray.request.routeFunction : null,
    strayRecorded: ((stray.request || {}).unread || []).filter((u) => /routeFunction/.test(u)),
    plainHolds: holdsIn(plain), statedHolds: holdsIn(asDom),
    tonicSeen, tonicHeld, subSeen, subHeld, domSeen, domHeld,
    tonicWitness, subWitness
  };
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
             spendsTheMiracle: SPENDS_THE_MIRACLE, worldsCast, worldStack, worldNotVoiced,
             worldSeen, levelBreaches, levelSharedBy,
             promiseSeen: promiseSeen.sort(), promiseKept: promiseKept.sort(),
             registerOf: promiseKind,
             levelBreachCases, levelSharedCases,
             adriftSeams, tideCellsSeen, levelASeen, levelBSeen, gateSlots,
             gridColourVoicesOwns, strataLightVoicesOwns,
             gridColourVoicesAccompanies, strataLightVoicesAccompanies,
             accSightings, accStillDriven};
out.camera = {checked: camChecked, mismatches: camMismatches, allZero: camAllZeroCount,
              endsBad: camEndsBad, fitMismatch: camFitMismatch, maxTrackLen: camMaxTrackLen,
              trackPointCap: CAMERA_POINT_CAP, distinctTracks: camDistinctTracks.size,
              dollyCap: DOLLY_CAP,
              voiceChecked: camVoiceChecked, voiceUnder: camVoiceUnder, voiceWorst: camVoiceWorst,
              voiceShares: camVoiceShares.sort((p, q) => p - q)};
out.voices = {checked: voiceChecked, silentDeclared: voiceSilentDeclared, worst: voiceWorst,
              target255: VOICE_TARGET_255};

// 6d · THE ARITHMETIC PUT THROUGH ITS OWN WHOLE SPAN, and no photograph anywhere in it.
//
// His word of 2026-08-24: «I NEVER asked to measure the combinations, they do not help to anything!
// we should be able to cope with any set of pics in real time, the distribution should never be
// measured in prior!» and, on whether a large sample would do instead, «I don't know if 190 pairs is
// enough or not, I don't know which pairs or pics did you select, it all sounds bad to me as we
// don't have any confidence about the coverage. I know we have X effects, each effect can have Y
// parameters, etc etc.»
//
// The sweeps above run the composer over the records that happen to be on disk. That is a SMOKE
// reading — it says the code runs and writes plausible numbers on real input — and it is not
// evidence about any pair not in the fixture, because the fixture is one arbitrary handful of points
// inside a space of every possible pair times every effect times every parameter. This section
// answers the other question. The three functions below are pure arithmetic the composer EXPORTS,
// and their arguments are numbers with known spans, so every claim about them can be put to every
// number the span holds: the grid walks the span end to end and the die walks it again at random
// where a grid would only ever land on round values. A red here is a red for all inputs and not for
// 190 of them.
//
// IT RUNS ON THE STANDING RUN ONLY. A planted run walks a corner of the collection to prove one
// guard, and the arithmetic below is the same arithmetic whatever is planted elsewhere in the
// module — re-walking every span once per plant would buy nothing and cost the suite its whole
// budget. The row that reads it reads the standing run.
const PROOF = plants.length ? {checked: 0, broke: [], standing: false} : (() => {
  let checked = 0;
  const broke = [];
  const fail = (why, at) => { if (broke.length < 8) broke.push({why: why, at: at}); };
  // A DIE OF THIS FILE'S OWN, so the random half of the walk repeats exactly run to run — a property
  // that only reds on a Tuesday is not a property.
  let s = 20260824;
  const rnd2 = () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; };

  // ---- camVoiceFloor and camVoiceLift ----
  // THE SPANS, and each is the argument's own and not a sample of one. `grainFrac` is a lattice step
  // over a frame side: a step below one pixel of the frame is no step, and a step wider than the
  // frame is no lattice, so it runs (0, 1]. `ceiling` is an axis's own published maximum: both of
  // the camera lane's two — DOLLY_CAP and half of it — and every value between 0 and 1 besides, so
  // an axis published at some third ceiling tomorrow is already answered for. `share` is a magnitude
  // over that same ceiling, [0, 1] by every axis's own derivation. The ends and the two ceilings are
  // named explicitly, because a bound that only breaks AT its own edge is exactly what a grid of
  // round numbers steps over.
  const grains = [1e-9, 1e-6, 1e-4, 0.2499, 0.25, 0.2501, 0.4999, 0.5, 0.5001, 0.999999, 1];
  for (let i = 1; i <= 64; i++) grains.push(i / 64);
  const ceilings = [DOLLY_CAP, 0.5 * DOLLY_CAP, 1e-6, 1e-3, 0.999999, 1];
  for (let i = 1; i <= 48; i++) ceilings.push(i / 48);
  const shares = [0, 1e-12, 1e-6, 0.999999, 1];
  for (let i = 0; i <= 64; i++) shares.push(i / 64);
  for (let i = 0; i < 200; i++) { grains.push(rnd2()); ceilings.push(rnd2()); shares.push(rnd2()); }
  shares.sort((p, q) => p - q);
  const EPS = 1e-9;
  for (const g of grains) {
    for (const c of ceilings) {
      const floor = composer.camVoiceFloor(g, c);
      const asked = 2 * g / c;
      checked++;
      // (1) THE FLOOR IS A SHARE AND STAYS ONE. Nothing a grain or a ceiling can be puts it outside
      //     [0, 1], because clamp01 is the last thing that touches it.
      if (!(floor >= 0 && floor <= 1)) fail("floor outside [0,1]", {g: g, c: c, floor: floor});
      // (2) IT IS THE LAW'S OWN NUMBER, not an approximation of it: below the clamp it is exactly
      //     2·grainFrac / thatCeiling, and at or above the clamp it is exactly 1 — the axis flying to
      //     its own published maximum, which is as far as it is allowed to go.
      if (asked <= 1 ? Math.abs(floor - asked) > EPS : floor !== 1) {
        fail("floor is not 2*grain/ceiling under the clamp", {g: g, c: c, floor: floor});
      }
      // (3) A COARSER GRAIN NEVER ASKS FOR LESS, and a wider ceiling never asks for more of itself.
      if (composer.camVoiceFloor(g / 2, c) - floor > EPS) fail("floor fell as grain rose", {g: g, c: c});
      if (c < 1 && floor - composer.camVoiceFloor(g, Math.min(1, c * 2)) < -EPS) {
        fail("floor rose as the ceiling widened", {g: g, c: c});
      }
    }
  }
  // The lift is swept against every floor the sweep above produced, over every share — this is the
  // pair (floor, share) the composer actually forms, and both halves of it walk their whole span.
  const floors = [0, 1e-9, 1e-6, 0.5, 0.999999, 1];
  for (let i = 0; i <= 64; i++) floors.push(i / 64);
  for (let i = 0; i < 200; i++) floors.push(rnd2());
  for (const floor of floors) {
    let last = -1;
    for (const share of shares) {
      const lift = composer.camVoiceLift(floor, share);
      checked++;
      // (4) NO EXCURSION, NO LIFT, and no floor, no lift: the multiplier rests at exactly 1 so a pair
      //     that calls for nothing is left calling for nothing.
      if ((!(floor > 0) || !(share > 0)) && lift !== 1) fail("lift moved with nothing to lift", {floor: floor, share: share, lift: lift});
      if (!(share > 0)) continue;
      const lifted = share * lift;
      // (5) IT NEVER PASSES THE AXIS'S OWN CEILING. `lifted` is the share of the ceiling the pose is
      //     written at, so lifted ≤ 1 IS «the magnitude never exceeds the ceiling», for every ceiling
      //     at once — the ceiling divides out of both sides.
      if (lifted > 1 + EPS) fail("the lifted share passed 1", {floor: floor, share: share, lifted: lifted});
      // (6) IT NEVER FALLS BELOW THE LEVEL THE GRAIN ASKED FOR.
      if (lifted < floor - EPS) fail("the lifted share fell under its floor", {floor: floor, share: share, lifted: lifted});
      // (7) A LIFT LIFTS. It can never quiet an axis the pair called loudly for.
      if (lifted < share - EPS) fail("the lift lowered the reading", {floor: floor, share: share, lifted: lifted});
      // (8) THE READINGS STILL RANK — shelf 9's law, which is the one thing a floor could have cost.
      //     Two pairs on one floor keep their order: a stronger call still flies further.
      if (lifted < last - EPS) fail("the lift stopped ranking", {floor: floor, share: share, lifted: lifted, last: last});
      last = lifted;
    }
  }
  // (9) THE TWO TOGETHER KEEP THE LAW THEY EXIST FOR: the angle actually flown clears one element of
  //     the pair's finer grain — or the whole ceiling, where the grain asks for more than the axis is
  //     allowed to give. Stated in ANGLES, which is where the law lives, so the ceiling cannot cancel
  //     itself out of the claim: this is the check that a pitch axis lifted against roll's ceiling
  //     fails, and the check the fixture sweep could never make.
  for (let i = 0; i < 40000; i++) {
    const g = rnd2(), c = rnd2(), share = rnd2();
    const floor = composer.camVoiceFloor(g, c);
    const flown = share * composer.camVoiceLift(floor, share) * c;
    checked++;
    if (flown > c + EPS) fail("the angle flown passed the ceiling", {g: g, c: c, share: share, flown: flown});
    if (flown < Math.min(2 * g, c) - EPS) fail("the angle flown missed one element of grain", {g: g, c: c, share: share, flown: flown, asked: Math.min(2 * g, c)});
  }

  // ---- voiceLoudness ----
  // THE SPANS AGAIN. `measure` is a work's own colour or contrast reading, a share in [0, 1].
  // `period` and `phase` are what the composer writes beside the amplitude; the periods are clamped
  // into each instrument's own manifest range before they arrive, so the span walked here is wider
  // than any manifest can ask for, and phase is a turn — [0, 1). The threshold is the LAB's, the same
  // 6 of 255 the row above reads, and the four decimal places are the score's own.
  const SEEN = VOICE_TARGET_255 / 255;
  const measures = [0, 1e-9, 1e-6, 1e-4, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.999999, 1];
  for (let i = 1; i <= 24; i++) measures.push(i / 24);
  const periods = [0, -1, 1e-6, 0.05, 0.1, 0.25, 0.5, 1, 1.5, 2, 3, 5, 8, 13, 21, 40, 120];
  const phases = [0, 0.25, 0.5, 0.75, 1 / 3, 0.999999];
  const tryLoud = (m, per, pha) => {
    const v = composer.voiceLoudness(m, per, pha);
    const peak = voicePeakShare(per, pha);
    checked++;
    if (v === null) {
      // (10) A MUTE IS EARNED. The voice is left unwritten only where the work's own reading — the
      //      ceiling a voice may never be louder than — stands below the least four-decimal loudness
      //      that clears the lab's threshold. Nothing else can mute a voice.
      if (m > 0 && peak > 0) {
        const want = Math.ceil(SEEN / peak * 10000) / 10000;
        if (m >= want - EPS) fail("a voice was muted that its own measure could carry", {m: m, per: per, pha: pha, want: want});
      }
      return null;
    }
    // (11) A DECLARED VOICE IS A SEEN VOICE — at the value that reaches the wire, four decimals and
    //      all, not at the value before rounding. This is the lab's own law: «Заявленный и неслышный
    //      голос — пустое утверждение разбора».
    if (!(composer.r4(v) * peak * 255 >= VOICE_TARGET_255 - 1e-6)) {
      fail("a declared voice peaks under the lab's threshold", {m: m, per: per, pha: pha, v: v});
    }
    // (12) AND NEVER LOUDER THAN THE THING IT IS A VOICE OF, nor outside [0, 1].
    if (!(v > 0 && v <= m + EPS && v <= 1)) fail("a voice passed its own measure", {m: m, per: per, pha: pha, v: v});
    return v;
  };
  for (const per of periods) for (const pha of phases) for (const m of measures) tryLoud(m, per, pha);
  // AND THE SAME SPANS AGAIN OFF THE DIE, because a grid of round values is exactly where a formula
  // written from round values would happen to be right. The die lands between the grid's own steps.
  for (let i = 0; i < 5000; i++) tryLoud(rnd2(), rnd2() * 60, rnd2());
  // (13) A LOUDER WORK IS NEVER A QUIETER VOICE, and a voice never goes silent as its measure grows.
  //      Both are the shape of `max(quarter, want)` in the measure and neither depends on any pair.
  for (const per of [0.7, 1.3, 2.6, 5.5, 11.1]) {
    for (const pha of [0, 0.25, 0.5, 0.75]) {
      let prev = null;
      for (let i = 0; i <= 120; i++) {
        const v = tryLoud(i / 120, per, pha);
        if (prev !== null && v === null) fail("a voice went silent as its measure grew", {per: per, pha: pha, m: i / 120});
        if (prev !== null && v !== null && v < prev - EPS) fail("a louder measure sang quieter", {per: per, pha: pha, m: i / 120});
        prev = v;
      }
    }
  }
  return {checked: checked, broke: broke};
})();
out.proof = PROOF;

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

// 8j-2 · THE COOLDOWN'S OWN FLOOR, PROVED OVER THE WHOLE SPAN OF `at` AND `poolSize` RATHER THAN
// walked on any route. His 2026-08-26 word: «разнообразие необходимо, вопрос в ранжировании» — the
// die and the cooling both stay, and what moved is what `coolFactor`'s `poolSize` counts. Before the
// fix it was `walkPlayed.length`, the raw length of the walk's own log — a quantity `walkMemory`'s
// own law declares deliberately unbounded, so the floor for the letter played most recently
// (at = 0) had no floor of its own: it fell toward 0 as a visit ran on, and at n = 100 it already
// stood under 0.01 — meaning a road read at the file's own best fit (1.0) lost to a rival read at a
// hundredth of it (0.01) for no reason but the length of the log, and the same arithmetic inverts
// any fit gap given a long enough visit. `coolFactor` and `walkCooldown` are the module's own
// arithmetic (pass-composer.js :2501-2531), exposed exactly as `camVoiceFloor` is, so this is
// proved over the numbers rather than assumed from the fix reading right.
const sweepBad = [];
for (let poolSize = 0; poolSize <= 64; poolSize++) {
  const never = composer.coolFactor(-1, poolSize);
  if (never !== 1) sweepBad.push(`poolSize ${poolSize} at -1 -> ${never}, wanted 1`);
  let prev = 0;
  for (let at = 0; at < Math.max(poolSize, 1); at++) {
    const v = composer.coolFactor(at, poolSize);
    if (!(v > 0 && v <= 1)) sweepBad.push(`poolSize ${poolSize} at ${at} -> ${v}, outside (0,1]`);
    if (v < prev) sweepBad.push(`poolSize ${poolSize} at ${at} -> ${v}, fell below ${prev}`);
    prev = v;
  }
}
// A THOUSAND PASSAGES THAT KEEP RETURNING TO ONE LETTER, against a walk of exactly one passage
// naming that same letter. Old `n` (raw log length) reads 1000 against 1 and the floors it hands
// out differ by three orders of magnitude for the SAME recency; `walkCooldown` (the fixed,
// distinct-letter `n`) reads both logs as poolSize 1 and hands out the same floor for both, because
// how many times a walk revisited one letter is not what the cooldown was ever supposed to answer.
const longLog = [];
for (let i = 0; i < 1000; i++) longLog.push("kaleidoscope");
const cooldownArith = {
  sweepBad,
  longLogFixedFloor: composer.walkCooldown(longLog, "kaleidoscope"),
  oneLogFixedFloor: composer.walkCooldown(["kaleidoscope"], "kaleidoscope"),
  longLogOldFloorWouldHaveBeen: composer.coolFactor(0, longLog.length),
  neverPlayedStaysWhole: composer.walkCooldown(["spin", "spin", "spin"], "kaleidoscope"),
};
out.cooldownArith = cooldownArith;

// 8j-3 · THE ROAD'S OWN POOL, READ OFF THE COMPOSER'S OWN REQUEST DIAGNOSTICS, NEVER THE MIXED ONE
// ---------------------------------------------------------------------------------------------------
// His adversarial follow-up on this same fix (2026-08-26 night run, a live production walk): a
// road's own cooldown was read off `walkPlayedDistinct`, which dedupes `walkMemory` — and
// `walkMemory` (`passWalkMemory`, 01a-pass.js) mixes a step's road with every instrument its stack
// carried. A dozen or two passages carry roughly eight roads and twenty-seven instruments between
// them, so the pool a road's cooldown divided by ran to ~35 rather than the eight `genresFor` ever
// answers with — his own live numbers, a floor near 1/36 where the design claims 1/9, and a fitness
// gap of 0.88 against 0.14 inverting at a pool six wide. `walkGenres` (`passWalkGenres`, roads only,
// never the stack) is read as a second channel and `pickGenre` now cools off it
// (`coolOfRoad`/`roadPlayedDistinct`, pass-composer.js) rather than off `walkMemory`.
const roadVocab = ["shared-ground", "kaleidoscope", "spin", "symmetry-slide", "stripes", "box-fold",
                   "dissimilar-mystery", "tonal-and-spectral"];
const fakeInstruments = [];
for (let fi = 0; fi < 27; fi++) fakeInstruments.push("fake-instrument-" + fi);
// THE MIXED LOG HIS REPORT MEASURED: the walk's eight roads and, beside them, roughly the
// instrument roster's own width — one list, the same shape `passWalkMemory` hands the composer
// over a real visit.
const mixedLog = roadVocab.concat(fakeInstruments);
const roadEcho = composer.passageFor({
  workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB],
  walkMemory: mixedLog, walkGenres: roadVocab.slice()
});
const echoedMixed = (roadEcho.request && roadEcho.request.walkMemory) || [];
const echoedRoad = (roadEcho.request && roadEcho.request.walkGenres) || [];
// AND WHAT THE TWO COOLINGS ACTUALLY DIVIDED BY, off the composition's own diagnostics rather than
// off the request it was handed: the echo above shows the two lists reached the composer apart, and
// this shows the two coolings READ them apart. It is the reading a plant can move — restoring one
// shared pool for roads and letters puts both numbers on the mixed list at once — where the echo and
// the source grep cannot be moved by any plant at all.
const roadCooling = ((roadEcho.diagnostics || {}).cooling) || {};
out.roadPool = {
  mixedLen: echoedMixed.length,
  mixedDistinct: new Set(echoedMixed).size,
  roadLen: echoedRoad.length,
  roadDistinct: new Set(echoedRoad).size,
  roadPoolRead: roadCooling.roadPool,
  letterPoolRead: roadCooling.letterPool,
  floorAtEight: composer.coolFactor(0, 8),
  floorAtMixed: composer.coolFactor(0, echoedMixed.length || 1),
};

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
  "two records with nothing measured at all": [bareRecord("bare-a"), bareRecord("bare-b")],
  // A RECORD CARRYING ONLY ITS OWN ID, which is the hardest record there is and the one the
  // composer's own two refusals AGREE to compose over: `passageFor` asks each record for an `id`
  // and for nothing else. Everything else here is a field that may be absent, so the composer's own
  // contract already says this record must yield a crossing. `bareRecord` above is not this case —
  // it ships every optional container present and empty, and a container present and empty is a
  // different thing from a field that is not there at all. Charter shelf 21: no branch may
  // terminate in "no crossing", and a throw is worse than a refusal.
  "a record carrying only its own id": [{ id: "id-only" },
                                        fullRecord("ordinary", { measures: { banding: 0.4 },
                                          structure: { banding: { score: 0.4 } } })],
  "two records carrying only their own ids": [{ id: "id-a" }, { id: "id-b" }]
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

// 12b · THE FIVE ARRIVALS ANSWER TOO (charter shelf 7, naряд S-06), each proved by a pair BUILT to
//       win it — `arrivalOf`'s own ranking, exercised through the one door it has, `passageFor`,
//       never through an internal function this suite would otherwise have to reach past. Each
//       built pair raises exactly the one reading its own arrival's fit reads and leaves every
//       other reading at `fullRecord`'s own zero, so the winning name is a genuine ranking rather
//       than a coincidence of the real collection's 121 records.
{
  // MISMATCH THE PAIR'S OWN TWO RHYTHMS, so INTERFERED's own fit — which two untouched
  // `fullRecord`s would otherwise hand a perfect 1, both carrying the same default step and
  // angle — never outranks the arrival a given pair is built to prove. Left off only for
  // INTERFERED's own pair, where the match IS the reading being proved.
  const detune = { ownDevice: { stepPx: 400.0, angleDeg: 90 } };
  const runArrival = (label, bStructure, bTexture) => {
    const wa = fullRecord("arr-a-" + label, {});
    const wb = fullRecord("arr-b-" + label, { structure: bStructure || {} });
    if (bTexture) Object.assign(wb.texture, bTexture);
    let p, err = null;
    try {
      p = composer.passageFor({ workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                                routeRole: "middle", seed: 0 });
    } catch (e) {
      err = String((e && e.message) || e);
    }
    // THE ARRIVAL'S OWN CUE, AND WHAT THE PLAN ACTUALLY WROTE ONTO IT. The mode alone says which of
    // the five was ranked highest; these say whether the decision reached an instrument — which is
    // the whole difference between an arrival that is NAMED and one that is PLAYED.
    const plan = (p && p.plan) || null;
    const arr = (plan && plan.arrival) || {};
    const cue = plan ? (plan.cues || []).filter((c) => c.id === "arrival")[0] : null;
    // WHAT THE FILL ASKED FOR, never what the score wrote. A score carries a node for EVERY handle
    // of a cue — the ones the fill named and the ones left standing at the instrument's own rest —
    // so reading the node would answer «0.5» for a seed nobody placed, which is exactly the silence
    // one row below has to be able to see. `measuredHandles` is the cue's own record of the fill's
    // own requests and carries nothing else.
    const nodeOf = (h) => {
      const asked = (cue && cue.measuredHandles) || {};
      return Object.prototype.hasOwnProperty.call(asked, h) ? toNum(asked[h]) : null;
    };
    return { mode: arr.mode || null, locusKind: arr.locusKind || null, locus: arr.locus || null,
             instrument: cue ? cue.instrument.id : null,
             seedPlace: nodeOf("seedPlace"), arrivalHandle: nodeOf("arrival"),
             propagate: nodeOf("propagate"), roles: cue ? cue.roles : null,
             declined: (p && p.declined) || null, error: err };
  };
  out.arrivalVocabulary = {
    CARRIED: runArrival("carried", Object.assign({}, detune)),
    CONDENSED: runArrival("condensed",
      Object.assign({ radial: { score: 0.9, centre: [0.3, 0.4] } }, detune)),
    CRYSTALLIZED: runArrival("crystallized",
      Object.assign({ regions: { line: { x: { at: 0.2 }, y: { at: 0.6 } } } }, detune),
      { scoreFromCutLines: 0.85 }),
    PROPAGATED: runArrival("propagated",
      Object.assign({ rotational: { n: 4, score: 0.9 } }, detune)),
    INTERFERED: runArrival("interfered", {})
  };
  // 12c · WHERE THE CRYSTALLIZED ARRIVAL PUTS ITS SEED, ON A PAIR BUILT SO THE TWO CANDIDATE
  //       PLACES CANNOT BE CONFUSED. The наряд asks for a seed «в точке наибольшего беспорядка» —
  //       at the point of greatest disorder — and the file placed it for a while at the arriving
  //       work's own strongest DIVIDING line, which is the most ordered place its record names.
  //       So this record puts the two far apart: its detail stratum gathers at 0.14 of the frame's
  //       width and its region line falls at 0.82. One of the two numbers comes back on the plan,
  //       and which one it is settles the question.
  //
  //       AND THE SEED HAS TO REACH THE PICTURE. The second reading is the arrival cue's own
  //       `seedPlace` node — the handle the pour's column releases are ordered outward from — so a
  //       seed that named a place and never reached an instrument would still red this.
  //
  //       THE SILENT CASE IS BUILT TOO. A work with the same grain score and no relief reading at
  //       all has no measured point of disorder; it must seed nowhere and say so, rather than
  //       standing the seed at a middle nobody read.
  out.crystalSeed = {
    apart: runArrival("crystal-apart",
      Object.assign({ regions: { line: { x: { at: 0.82 }, y: { at: 0.6 } }, score: 0.4 } }, detune),
      { scoreFromCutLines: 0.85, reliefCentreDetailX: 0.14 }),
    silent: runArrival("crystal-silent",
      Object.assign({ regions: { line: { x: { at: 0.82 }, y: { at: 0.6 } }, score: 0.4 } }, detune),
      { scoreFromCutLines: 0.85 })
  };
}

// ---- ONE INSTRUMENT, BOTH SIDES OF THE LEVELS LAW --------------------------------------------
// `adrift` publishes handles on two levels: its seam and its grain read the whole SURFACE, and its
// flights, voids and homes belong to what stands inside a cell. So it is the plain case for the
// law's two halves, and both are read here on NAMED ordered pairs rather than on whatever the
// ranking happens to choose across a corner of the collection.
//
//   · `owns` — a pair where adrift's cue owns SURFACE. Its seam handles are driven, off the
//     departing work's own measured seam.
//   · `accompanies` — a pair where another cue owns SURFACE instead. The seam handles are gone
//     from adrift's track list altogether, which is what resting on a lost level means; every one
//     of its CELL CONTENT handles is still driven, which is what playing on where it owns means.
{
  const adriftAt = (a, b, role) => {
    const wa = works.works[a], wb = works.works[b];
    const p = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                                   seed: die(a + "__" + b + "__ab"),
                                   routeRole: role || "middle"});
    const cue = p.score ? p.plan.cues.find((c) => c.instrument.id === "adrift") : null;
    if (!cue) return {cast: false};
    const man = fix.consts.manifests.adrift.handles;
    const driven = Object.keys(cue.tracks || {});
    const on = (level) => driven.filter((h) => (man[h] || {}).level === level).sort();
    const seamNode = cue.nodes[cue.id + "-seamA"];
    return {cast: true, cue: cue.id, owns: (cue.levelOwnership || {})["SURFACE"] || null,
            surfaceDriven: on("SURFACE"), cellContentDriven: on("CELL CONTENT"),
            seamApplied: seamNode ? toNum(startValue(seamNode)) : null,
            seamNote: seamNode ? String(seamNode.note || "") : null,
            recordSeam: Number(((wa.structure || {}).horizon || {}).seam) || 0};
  };
  // THE TWO PAIRS ARE DERIVED, NEVER PINNED. Two ordered pairs stood written out here, chosen
  // because adrift happened to be cast on them in the two shapes the law's two halves need. That
  // went stale once already — the day `liquid` stopped declaring SURFACE, the pair that used to
  // show adrift ACCOMPANYING showed it owning, and the row had to be re-picked by hand — and a
  // pinned witness goes stale again on the next correction to any declaration, silently, because a
  // pair that no longer casts adrift reads `{cast: false}` and says nothing about why.
  //
  // So the two witnesses are searched for instead, over the same settled corner of ordered pairs
  // every other row here walks, in the same settled order: the first pair on which adrift is cast
  // and OWNS the surface, and the first on which it is cast and does NOT. Both are properties of
  // the composition rather than of any pair chosen in advance, so a declaration corrected tomorrow
  // moves which pair is found and not whether one is. Where the corner carries no such pair, the
  // witness says `{cast: false}` and the row reds with that on its face — which is the honest
  // answer: the law's half could not be exercised at all.
  // THE OWNING WITNESS ALSO NEEDS A SEAM WORTH READING, and the condition is put on the RECORD and
  // never on what the composition wrote. The row below asks that adrift's seam carry the departing
  // work's own MEASURED strength rather than presence-or-absence, so a witness whose departing work
  // records a seam of exactly nothing or exactly whole cannot tell the two apart — that is a fact
  // about the record and it is knowable before the composer is asked. Reading it off the record
  // keeps the row honest: were the wire to break tomorrow and write nothing everywhere, the search
  // would still find this pair and the row would still red on what it applied.
  const realSeamOf = (x) => {
    const s = Number((((works.works[x] || {}).structure || {}).horizon || {}).seam) || 0;
    return s > 0 && s < 1;
  };
  const findAdrift = (wantOwns, needRealSeam) => {
    for (const [x, y] of SPOT) {
      if (needRealSeam && !realSeamOf(x)) continue;
      for (const role of ROLES_ALL) {
        const got = adriftAt(x, y, role);
        if (got.cast && (got.owns === "owns") === wantOwns) {
          got.pair = x + "__" + y + "__ab";
          got.role = role;
          return got;
        }
      }
    }
    return {cast: false, searched: SPOT.length, needRealSeam: !!needRealSeam};
  };
  out.adriftBothWays = {owns: findAdrift(true, true), accompanies: findAdrift(false, false)};

  // ---- THE GATE SLOT'S OWN WITNESSES, SOUGHT RATHER THAN HOPED FOR --------------------------
  // The gate-slot row asks three things: every applied slot matches the departing work's own
  // record, slotPlace takes more than one value, and slotAxis is seen at both 0 and 1. The first
  // is a claim about the reading and the sweep answers it wherever it lands. The other two are
  // claims about REACH — that the row saw a slot in each direction and more than one place — and
  // those the sweep cannot answer, because which pairs cast `gates` at all is the ranking's
  // business and moves whenever a record does.
  //
  // It moved on 2026-08-26. Not one gate field in one record changed value; the ranking simply
  // stopped casting `gates` on any horizontally-slotted departing work inside the 192-pair spot,
  // and a row that had been green for weeks went red having found nothing wrong. That is the shape
  // this file has been closing all night: a verdict whose reach is set by what something else
  // happened to hand it.
  //
  // So the witnesses are DERIVED, the way the drifting instrument's two above are. Ordered pairs
  // are walked in the collection's own id order until a `gates` cast is found on a departing work
  // of each axis and at more than one place. The walk is bounded and it reports what it reached, so
  // a corner that genuinely holds no such pair REDS SAYING SO rather than passing on a thinner
  // sample — the clauses are not loosened, they are given something to stand on.
  {
    const seen = [], readings = [];
    let tried = 0;
    const axesFound = () => new Set(seen.map((s) => s.axis));
    const placesFound = () => new Set(seen.map((s) => s.place));
    const halvesFound = () => new Set(seen.map((s) => s.half));
    outerGate:
    for (let i = 0; i < ids.length; i++) {
      for (let j = 0; j < ids.length; j++) {
        if (i === j) continue;
        for (const dir of ["a-to-b", "b-to-a"]) {
          if (tried++ > 4000) break outerGate;
          const a = ids[i], b = ids[j];
          const key = a + "__" + b + "__" + (dir === "a-to-b" ? "ab" : "ba");
          let q;
          try {
            q = composer.passageFor({workRecordA: works.works[a], workRecordB: works.works[b],
                                     direction: dir, seed: die(key)});
          } catch (e) { continue; }
          if (!q.score) continue;
          const cue = q.plan.cues.find((c) => c.instrument.id === "gates");
          if (!cue) continue;
          // A GATES CUE THAT DOES NOT OWN ITS LEVEL DRIVES NO SLOT AT ALL, and that is the levels
          // law working rather than anything missing: `ownedTracks` strips slotPlace/slotHalf/
          // slotAxis from a cue that merely accompanies on CELL, so such a cue carries no slot
          // reading for this row to check. The witness therefore looks for a cue that DRIVES the
          // slot rather than for one that merely plays the instrument — asked of the track list
          // itself, so it stays true however the ownership rule is later written.
          if (!(cue.tracks || {}).slotPlace) continue;
          // The departing work under the same b-to-a flip the composer itself takes.
          const from = dir === "b-to-a" ? works.works[b] : works.works[a];
          const mot = from.motifs || {};
          const axis = mot.gateAxis === "vertical" ? 1
            : (mot.gateAxis === "horizontal" ? 0 : null);
          seen.push({key: key, axis: axis, place: mot.gatePlace, half: mot.gateHalf});
          for (const handle of ["slotPlace", "slotHalf", "slotAxis"]) {
            const node = cue.nodes[cue.id + "-" + handle];
            if (!node) continue;
            const record = handle === "slotPlace" ? mot.gatePlace
              : handle === "slotHalf" ? mot.gateHalf : axis;
            readings.push({key: key, handle: handle, applied: toNum(startValue(node)),
                           record: record});
          }
          // THE SEARCH STOPS WHEN EVERY CLAUSE THE ROW ASKS HAS SOMETHING TO STAND ON, not when
          // most of them do. Stopping at two axes and two places left `slotHalf` on whatever the
          // first two pairs happened to share, which is the same «reach set by what turned up»
          // this witness exists to end — one clause short is still hoping.
          if (axesFound().size >= 2 && placesFound().size >= 2
              && halvesFound().size >= 2) break outerGate;
        }
      }
    }
    out.gateSlotWitness = {tried: tried, pairs: seen, readings: readings,
                           axes: [...axesFound()].sort(), places: [...placesFound()].sort(),
                           halves: [...halvesFound()].sort()};
  }

  // THE GROUND AND THE VOICE ABOVE IT, CUTTING THE SAME WAY. A pair whose plan casts two cues that
  // both DECLARE one level and both publish handles on it — the plain shape of shelf 18's ban,
  // pattern stacked on pattern. What is read is which cues actually DRIVE a handle on each level:
  // one cue per level is the law kept, two is the defect.
  //
  // THE PAIR IS DERIVED, NEVER PINNED, for the same reason `adriftBothWays` above is. One ordered
  // pair at one role stood written out here and it went stale the night the entry door's dry landed
  // across the fleet and moved what this collection casts: the pair stopped casting two cues on one
  // level, so the red-on-bug that plants `ownedTracks` out read `False` — the plant could no longer
  // fire, and a guard that cannot fail is worse than no guard because the row above it still reads
  // green. A pinned witness goes stale silently on the next correction to any declaration; a
  // searched one moves with it.
  //
  // AND THE SEARCH KEY IS WHAT MAKES IT A LAWFUL PLANT: it reads the cues' own DECLARED levels and
  // the manifests' own handle declarations, never the track lists. Those are identical whether
  // `ownedTracks` stands or is planted out, so the planted run and the plain run find the SAME
  // witness and the plant measures the guard rather than measuring which pair each run happened to
  // pick. The track lists are what is then read off that one witness, and they are exactly what the
  // guard changes.
  {
    const levelsOfCue = (cue) => {
      const man = fix.consts.manifests[cue.instrument.id].handles;
      const out2 = {};
      for (const h of Object.keys(man)) {
        if (man[h].open) continue;
        const l = man[h].level;
        if (l && (cue.levels || []).indexOf(l) >= 0) out2[l] = true;
      }
      return Object.keys(out2);
    };
    // TWO CUES ON ONE LEVEL ARE A BREACH ONLY WHERE THEY ARE LIVE TOGETHER, and this reading takes
    // that from the sweep above rather than keeping a second idea of the law. Shelf 17 bars two
    // ACTIVE voices from one level and the word carries it: `ownTheLevels` settles ownership per
    // OVERLAPPING group (`meets`), so two cues whose windows never meet may both own a level and
    // both drive their handles on it, lawfully. Reading the track lists alone called that a breach —
    // it is how this row first reported a perfectly lawful plan, `travel` and `arrival` both on
    // SURFACE across windows that never touch.
    const meet = (A, B) => A[0] < B[1] && B[0] < A[1];
    const windowOf = (cue) => [Number(toNum(cue.window[0])), Number(toNum(cue.window[1]))];
    const readPlan = (p) => {
      const byLevel = {}, windows = {}, cast = [];
      for (const cue of (p.score ? p.plan.cues : [])) {
        cast.push(cue.id + ":" + cue.instrument.id);
        windows[cue.id] = windowOf(cue);
        const man = fix.consts.manifests[cue.instrument.id].handles;
        for (const h of Object.keys(cue.tracks || {})) {
          const l = (man[h] || {}).level;
          if (!l) continue;
          if (!byLevel[l]) byLevel[l] = [];
          if (byLevel[l].indexOf(cue.id) < 0) byLevel[l].push(cue.id);
        }
      }
      const shared = Object.keys(byLevel).filter((l) => {
        const who = byLevel[l];
        for (let i2 = 0; i2 < who.length; i2++) {
          for (let j2 = i2 + 1; j2 < who.length; j2++) {
            if (meet(windows[who[i2]], windows[who[j2]])) return true;
          }
        }
        return false;
      }).sort();
      return {cast: cast, byLevel: byLevel, shared: shared};
    };
    // THE WALK IS THE COLLECTION'S OWN, IN ITS OWN ID ORDER, and not the 192-pair corner. The
    // corner is what every ranking row here stands on and it is the right sample for a reading; it
    // is the wrong one for a SHAPE, because whether any pair reaches this door is the cast's
    // business and a corner that misses it says nothing about the collection. The walk is bounded
    // and it reports how far it went, so "none found" is a statement with a number behind it.
    //
    // THE BOUND IS 600 AND IT IS A COST, NOT A CLAIM. Each step composes a whole passage; the walk
    // stops at the first witness and pays the whole bound only when there is none to find, so the
    // number is chosen to keep this file runnable rather than to bound the question. The question
    // itself was answered by hand at 6 002 compositions on 2026-08-26 and found nothing — that
    // reading is written into the retirement note beside the plant below, where it belongs, and the
    // day this walk finds a pair the note says what to do.
    let found = null, walked = 0;
    outerGV:
    for (let gi = 0; gi < ids.length; gi++) {
      for (let gj = 0; gj < ids.length; gj++) {
        if (gi === gj) continue;
        const x = ids[gi], y = ids[gj];
        for (const role of ROLES_ALL) {
        if (walked++ > 600) break outerGV;
        let p;
        try {
          p = composer.passageFor({workRecordA: works.works[x], workRecordB: works.works[y],
                                   direction: "a-to-b", seed: die(x + "__" + y + "__ab"),
                                   routeRole: role});
        } catch (e) { continue; }
        if (!p.score) continue;
        const cues2 = p.plan.cues;
        if (cues2.length < 2) continue;
        // The witness has to be a pair where two cues declare one level AND are live together,
        // because only there does the guard have anything to hold: two cues on one level across
        // windows that never meet are lawful with `ownedTracks` in place and lawful with it planted
        // out, so such a pair would prove nothing either way.
        const overlap = [];
        for (let i2 = 0; i2 < cues2.length; i2++) {
          for (let j2 = i2 + 1; j2 < cues2.length; j2++) {
            if (!meet(windowOf(cues2[i2]), windowOf(cues2[j2]))) continue;
            const li = levelsOfCue(cues2[i2]);
            for (const l of levelsOfCue(cues2[j2])) {
              if (li.indexOf(l) >= 0 && overlap.indexOf(l) < 0) overlap.push(l);
            }
          }
        }
        if (!overlap.length) continue;
        found = readPlan(p);
        found.pair = x + "__" + y + "__ab";
        found.role = role;
        found.declaredOverlap = overlap.sort();
        break outerGV;
        }
      }
    }
    if (found) found.walked = walked;
    out.groundVoice = found
      || {cast: [], byLevel: {}, shared: [], declaredOverlap: [], walked: walked, none: true};
  }
}

// ---- SHELF 17'S LEVELS LAW, AT THE HANDLES ---------------------------------------------------
// Every handle every published instrument publishes declares the structural level it drives, or
// declares that it drives none. Three things are asked of that here and none of them reads a
// photograph: every published handle has a declaration; every declaration names one of shelf 17's
// six levels or nothing at all; and no handle claims a level its own instrument does not declare in
// its `levels` array, which would put a cue on a level the cast never knew it was standing on.
{
  const six = composer.levels;
  const seventh = [], outside = [];
  for (const iid of Object.keys(levelsByInstrument).sort()) {
    const declared = ((fix.consts.manifests[iid] || live[iid] || {}).levels || []);
    for (const h of Object.keys(levelsByInstrument[iid]).sort()) {
      const lv = levelsByInstrument[iid][h];
      if (lv === null || lv === undefined) continue;
      if (six.indexOf(lv) < 0) seventh.push(iid + "." + h + " -> " + lv);
      else if (declared.indexOf(lv) < 0) outside.push(iid + "." + h + " -> " + lv);
    }
  }
  // WHICH LEVELS ARE ACTUALLY DRIVEN AND BY WHOM, so a level that no handle anywhere claims shows
  // up as the empty declaration it is rather than as a quiet nothing.
  out.levels = {six: six, undeclared: levelsUndeclared.sort(), seventh: seventh,
                outside: outside, driven: Object.keys(levelsSeen).sort(),
                instruments: Object.keys(levelsByInstrument).length};
}

// ---- SHELF 6'S ONE SLOT, ON THE TWO ORDERED PAIRS THAT REACH FOR IT TWICE -------------------
// THE LAW HAS THREE DOORS AND EACH NEEDS ITS OWN PAIR. A sweep of a corner of the collection reads
// what the ranking happens to choose there; these two ordered pairs are named because each one puts
// two world-declaring instruments within reach of one another by a DIFFERENT road, so the guard on
// that road is what decides the answer rather than the ranking.
//
//   · `levels` — the ground is cast to an instrument that declares the world and the arrival's own
//     candidate declares it too with a level of its own left free, so the levels test's first
//     clause (every level taken) does not catch it and only the world clause does.
//   · `swap` — the ground is re-cast mid-loop by §7's coverage law, AFTER the arrival is already
//     cast, so no levels test stands between the two at all and only the swap's own gate does.
{
  const twoWorlds = (p) => (p.score ? p.plan.cues
    .filter((c) => SPENDS_THE_MIRACLE.indexOf(c.instrument.id) >= 0).length : -1);
  const at = (a, b, role) => {
    const wa = works.works[a], wb = works.works[b];
    if (!wa || !wb) return {cues: null, worlds: -1};
    const p = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                                   seed: die(a + "__" + b + "__ab"), routeRole: role});
    return {cues: p.score ? p.plan.cues.map((c) => c.id + ":" + c.instrument.id) : null,
            worlds: twoWorlds(p), declined: p.declined || null};
  };
  out.oneSlot = {
    // THE PAIR CHANGED, 2026-09-02: the old pair's own arrival locks to CRYSTALLIZED -> pour under
    // `ARRIVAL_WANTS_INSTRUMENT`, and pour declares no WORLD level, so the scenario this row proves
    // — a world ground taking a world arrival beside it — was unreachable on that pair no matter
    // which gate the plant struck. This pair puts a world-declaring arrival within reach instead.
    // AND MOVED AGAIN 2026-09-02, for the ground-is-the-pivot repair in `placeTheStack`: that
    // pair's own arrival is no longer a world-declaring instrument under either the standing cast
    // or the planted one, so the plant had nothing to move. Searched again over the whole fleet:
    // this pair casts «boxfold» the ground and «pour» the arrival with the clause in place, and
    // «boxfold» beside «tilt» — two worlds in one crossing — with it struck.
    levels: at("17843080526947498", "18158795992274002", "middle"),
    swap: at("17843153263050281", "17856720509033958", "middle")
  };
}

// ---- SHELF 6'S ONE SLOT, READ OFF THE WALK RATHER THAN THE MANIFEST (naряд S-18) --------------
// His word of 2026-08-26 20:17: a miracle is a wow, a concept, it is subjective, and repeated it
// stops being one. `spendsTheMiracle` no longer answers the same way for the same instrument on
// every walk that ever casts it; it answers by what THIS walk has already played. The row watches a
// synthetic nine-step walk of ONE edge, threading `walkMiracles` forward exactly as
// `01a-pass.js`'s `passWalkMiracles` does: the fold each step actually voiced `"miracle"`, most
// recent first.
//
// WHICH EDGE, AND WHY IT HAD TO CHANGE (2026-09-01). This read `oneSlot.levels`'s own pair at a
// middle, reused because THAT row's law needed a pair putting two world-declaring instruments
// within reach of one cast. Between then and now the cast became a joint bundle planner (P1.2,
// 431a10c), which enumerates whole `{ground, travel, arrival, colour}` bundles instead of filling
// slots one at a time — and over that pair's own bundle set exactly ONE world fold, «planet», is
// ever a candidate at all. So the walk it drew could only ever show the first half of the law: the
// fold spends the slot once and never again. The second half — the freed slot taken by ANOTHER fold
// in the same crossing — had nothing on that pair to be taken by, and the row read silence as a
// breach when what it had actually run out of was a second candidate.
//
// The edge below is named for the property the law needs and the old one no longer has: TWO folds
// stand among the bundles this crossing considers. `foldsWithinReach` reads that off the composer's
// own published bundle ledger (`diagnostics.bundles.considered`, the planner's own record of what
// it weighed) rather than asserting it in prose, so the day this pair carries one fold again the
// row says exactly that instead of quietly going vacuous. What it shows: step 1 voices «planet»,
// step 2 hands the freed slot to «tilt», and steps 3 to 9 — both spent — voice no miracle at all,
// which is the law's own «and never again» made visible on the same edge.
{
  // THE EDGE MOVED AGAIN, 2026-09-02, and for the same KIND of reason it moved on 2026-09-01: what
  // the crossing casts changed under it. `placeTheStack` now refuses a plan whose ground would be
  // anything but the pivot — the one cue whose window runs the whole passage — so the 71 of 1200
  // composed passages that used to hand the floor to a short-windowed cue are re-cast through the
  // bundle planner's own ground swap, and the edge below is one of them. On it the freed slot went
  // to «tilt» before and to nothing after: the law's second half had nothing left to show. Searched
  // again over the whole fleet, both roles a miracle is granted at, for an edge where two folds
  // stand within reach AND the second step actually hands the slot to the other one.
  const a = "17843080526947498", b = "18021749102649971";
  const wa = works.works[a], wb = works.works[b];
  const seed = die(a + "__" + b + "__ab");
  let walkMiracles = [];
  const steps = [];
  const foldsWithinReach = [];
  for (let i = 0; i < 9; i++) {
    const req = {workRecordA: wa, workRecordB: wb, direction: "a-to-b", seed: seed,
                 routeRole: "middle"};
    if (walkMiracles.length) req.walkMiracles = walkMiracles.slice();
    const p = (wa && wb) ? composer.passageFor(req) : {declined: "fixture is missing the work"};
    const cues = p.score ? p.score.cues.map((c) => ({id: c.id, instrument: c.instrument.id,
                                                     voice: c.voice})) : null;
    const miracle = cues ? (cues.find((c) => c.voice === "miracle") || null) : null;
    // EVERY FOLD THIS CROSSING COULD HAVE CAST, off the planner's own ledger of the bundles it
    // weighed — the slot cannot be handed on to a fold that was never a candidate, so this is the
    // precondition the law's second half rests on and it is read rather than assumed.
    ((((p.diagnostics || {}).bundles || {}).considered) || []).forEach((bn) => {
      [bn.ground, bn.travel, bn.arrival].forEach((iid) => {
        if (iid && SPENDS_THE_MIRACLE.indexOf(iid) >= 0 && foldsWithinReach.indexOf(iid) < 0) {
          foldsWithinReach.push(iid);
        }
      });
    });
    steps.push({walkMiracles: walkMiracles.slice(), declined: p.declined || null, cues: cues,
               miracle: miracle ? miracle.instrument : null});
    if (miracle) walkMiracles = [miracle.instrument].concat(walkMiracles);
  }
  // A FOLD VOICED THE MIRACLE MORE THAN ONCE OVER THE NINE STEPS is the law's own subject failing:
  // read here as how many times each instrument that was EVER the miracle was voiced it, so a
  // count over 1 anywhere names the repeat.
  const miracleVoicedCount = {};
  steps.forEach((s) => { if (s.miracle) miracleVoicedCount[s.miracle] = (miracleVoicedCount[s.miracle] || 0) + 1; });
  // THE COUNT THE RUN PRINTS FOR ITSELF, and it is the number the row is judged on: how many times
  // over these nine steps the strongest strong move played AS THE MIRACLE. Rarity is the whole law
  // here, so what the run has to hand back is a count and not a verdict — the row reads it against
  // one and prints it either way, which is what makes the planted run below legible.
  const mostVoiced = Object.keys(miracleVoicedCount)
    .reduce((n, id) => Math.max(n, miracleVoicedCount[id]), 0);
  out.miracleRarity = {
    steps: steps,
    foldsWithinReach: foldsWithinReach.slice().sort(),
    distinctFolds: Object.keys(miracleVoicedCount).sort(),
    voicedCount: miracleVoicedCount,
    mostVoiced: mostVoiced,
    repeats: Object.keys(miracleVoicedCount).filter((id) => miracleVoicedCount[id] > 1)
  };
}

// ---- THE PASSAGE'S OWN LENGTH ----------------------------------------------------------------
// Two claims, and both are claims about NUMBERS rather than about the photographs on disk. The
// first: the band a role names holds for EVERY value the reading that places a length inside it
// can take, walked over that reading's whole span and not over a sample of pairs. The second: the
// reading is a reading of the two works, so two different pairs at one role come out at different
// lengths — which is the defect this closed, where the length was one typed constant per role and
// two pairs ran the same milliseconds to the millisecond.
{
  const bands = composer.roleBands;
  const tierBands = composer.tierBands;
  const everyBand = Object.assign({}, tierBands, bands);
  const broke = [];
  const note = (why, at) => { if (broke.length < 8) broke.push({why: why, at: at}); };

  // THE SHARE'S OWN SPAN IS [0, 1], and it is walked to both ends and past them: `lengthInBand`
  // clamps, so a caller handing it anything at all is answered here too.
  const shares = [];
  for (let i = 0; i <= 2000; i++) shares.push(i / 2000);
  for (const extra of [-1e9, -1, -1e-12, 1e-12, 1 - 1e-12, 1 + 1e-12, 1e9]) shares.push(extra);
  shares.sort((p, q) => p - q);
  for (const role of Object.keys(everyBand)) {
    const band = everyBand[role];
    if (!(band[0] > 0 && band[1] >= band[0])) note("the band is no band", {role: role, band: band});
    if (composer.lengthInBand(band, 0) !== band[0]) note("a share of nothing misses the floor",
                                                        {role: role});
    if (composer.lengthInBand(band, 1) !== band[1]) note("a whole share misses the ceiling",
                                                        {role: role});
    let prev = -Infinity;
    for (const s of shares) {
      const ms = composer.lengthInBand(band, s);
      if (!(ms >= band[0] && ms <= band[1])) note("outside the band", {role: role, s: s, ms: ms});
      if (ms < prev) note("the placement fell as the share rose", {role: role, s: s, ms: ms});
      prev = ms;
    }
  }

  // THE READING'S OWN SPAN. `cameraFlight` writes the dolly as `DOLLY_CAP · asked / (|asked| +
  // DOLLY_CAP)` — the same limit-not-a-wall shape the camera lane put there — and leaves it at
  // exactly 0 where either work carries no measured door step. `asked` is the natural logarithm of
  // one measured step over the other, so it runs the whole real line; this walks it there and
  // reads what the share the length is placed by can be.
  const asks = [0, 1e-12, -1e-12, 1e-6, -1e-6, 1, -1, 12, -12, 1e6, -1e6, 1e15, -1e15];
  for (let i = -400; i <= 400; i++) asks.push(i / 8);
  let shareLo = Infinity, shareHi = -Infinity;
  for (const a of asks) {
    const dolly = composer.r4(DOLLY_CAP * a / (Math.abs(a) + DOLLY_CAP));
    const share = Math.abs(dolly) / DOLLY_CAP;
    if (share < shareLo) shareLo = share;
    if (share > shareHi) shareHi = share;
    if (!(share >= 0 && share <= 1)) note("the share left [0,1]", {asked: a, share: share});
  }

  // THE SAME LENGTH, ASKED OF THE COMPOSER ITSELF, on two ordered pairs that are not the same pair.
  const [p1a, p1b] = SPOT[0], [p2a, p2b] = SPOT[SPOT.length - 1];
  const pairOf = (xi, yi, role) => {
    const wa = works.works[xi], wb = works.works[yi];
    const key = wa.id + "__" + wb.id + "__ab";
    const p = composer.passageFor({workRecordA: wa, workRecordB: wb, direction: "a-to-b",
                                   seed: die(key), routeRole: role});
    return p.score ? {ms: p.score.duration, tier: p.plan.tier} : null;
  };
  const perRole = {};
  for (const role of Object.keys(bands)) {
    const one = pairOf(p1a, p1b, role), two = pairOf(p2a, p2b, role);
    // WHICH BAND EACH RUNS INSIDE. The role's own where the plan reached that role's tier, and the
    // REALISED tier's where it did not — so a plan never declares a tier its length contradicts.
    // Both are named here and the row asks the length to stand inside one of them.
    perRole[role] = {band: bands[role], one: one, two: two,
                     tierOne: one ? tierBands[one.tier] : null,
                     tierTwo: two ? tierBands[two.tier] : null};
  }
  out.length = {bands: bands, tierBands: tierBands, broke: broke, shareLo: shareLo,
                shareHi: shareHi, perRole: perRole,
                walked: shares.length * Object.keys(everyBand).length + asks.length};
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


# Charter shelf 17's voice budget, and it is a budget BY TIER: a quiet tier carries one letter, at
# most one accompaniment and no miracle; a middle at most two letters, at most two accompaniments and
# at most one miracle; a culmination two or three letters, at most three accompaniments and exactly
# one. The camera is counted as one accompaniment before a single cue is counted (PASS-API-V1 §4.4,
# amended 2026-08-14 10:31), which is what `budget()` in the driver above already does.
TIER_BUDGET = {
    "quiet": {"letters": (1, 1), "accompaniments": (0, 1), "miracles": (0, 0)},
    "middle": {"letters": (0, 2), "accompaniments": (0, 2), "miracles": (0, 1)},
    "culmination": {"letters": (2, 3), "accompaniments": (0, 3), "miracles": (1, 1)},
}

# The same shelf's band of seconds per tier, in milliseconds. Shelf 17 names three and no more, so a
# ROLE gets no band of its own: it gets the band of the tier its row declares, which is why
# ROLE_SECONDS below is these three read through the role table's own `tier` and never a fourth pair
# of numbers. A composer that opened any of these would be widening the charter rather than placing a
# length inside it, so the row below reads the tables the composer publishes against these and never
# the other way about.
TIER_SECONDS = {"quiet": (2000, 4000), "middle": (5000, 8000), "culmination": (9000, 14000)}
ROLE_SECONDS = {"entrance": (5000, 8000), "quiet link": (2000, 4000), "middle": (5000, 8000),
                "culmination": (9000, 14000), "return": (2000, 4000)}

# The bound each ROLE emits inside — the letters it may spend, the miracles, and the band of seconds
# — with the entrance's and the return's own two rows this seat's. A role's letter bound holds: shelf
# 15 wants most of a walk quiet and shelf 17's quiet row is one letter, so a quiet link playing one
# structural gesture is the charter's own intent rather than a thin passage.
ROLE_BUDGET = {
    "entrance": {"letters": (0, 2), "miracles": (0, 0), "seconds": (5.0, 8.0)},
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

        # --- row 0b · the five arrivals, each proved by a pair built to win it ------------------
        # Charter shelf 7 names five arrivals — CARRIED, CRYSTALLIZED, CONDENSED, PROPAGATED,
        # INTERFERED — and naряд S-06 lifted the choice among them off a two-way gate onto the
        # same ranking-by-the-pair's-own-records shape row 0 above already proves for the genres.
        # Each of the five checks below builds one pair through the public `passageFor` door,
        # raising exactly the reading its own arrival's fit reads and leaving every other reading
        # at the record's own zero, and asks the composed plan's own `arrival.mode` for the name
        # the ranking actually played.
        av = got["arrivalVocabulary"]
        for _mode in ("CARRIED", "CRYSTALLIZED", "CONDENSED", "PROPAGATED", "INTERFERED"):
            _row = av[_mode]
            check(f"EX-COMPOSED the {_mode} arrival wins the pair built to read highest on it",
                  _row["mode"] == _mode,
                  f"built pair declined: {_row['declined']}; threw: {_row['error']}; the plan's "
                  f"own arrival.mode read «{_row['mode']}»" if _row["mode"] != _mode
                  else f"the plan's own arrival.mode read «{_row['mode']}» exactly as built")

        # --- row 0c · WHERE THE CRYSTALLIZED ARRIVAL SEEDS, AND WHETHER THE SEED REACHES PIXELS ---
        # The наряд's own sentence for this arrival is «зерно в точке наибольшего беспорядка,
        # порядок расходится задержкой по расстоянию» — a seed at the point of greatest disorder,
        # and order spreading from it with a delay proportional to distance. The pair below is built
        # so the two candidate places stand far apart: the arriving work's detail stratum gathers at
        # 0.14 of the frame's width — the least ordered place its record names — and its region
        # line, the strongest DIVIDING line the same record carries and the most ordered place in
        # it, falls at 0.82. The plan can hand back only one of the two.
        cs = got["crystalSeed"]["apart"]
        seeded = (cs["mode"] == "CRYSTALLIZED" and cs["locusKind"] == "grain-seed"
                  and cs["locus"] and abs(float(cs["locus"][0]) - 0.14) < 1e-6)
        check("EX-COMPOSED the crystallized seed stands at the arriving work's own point of "
              "greatest disorder, never at its strongest dividing line",
              seeded,
              "the work's own grain gathers at 0.14 of the frame's width and its region line falls "
              "at 0.82; the plan seeded at %s, which is the grain and not the line"
              % (cs["locus"],)
              if seeded else "the plan seeded at %s under «%s» (mode «%s») — 0.82 is the dividing "
                             "line and 0.14 is the grain" % (cs["locus"], cs["locusKind"],
                                                             cs["mode"]))

        reached = (cs["arrivalHandle"] == 1 and cs["seedPlace"] is not None
                   and abs(float(cs["seedPlace"]) - 0.14) < 1e-6)
        check("EX-COMPOSED the crystallized seed reaches the instrument that spreads order out "
              "from it, rather than staying a word on the plan",
              reached,
              "the arrival casts «%s» and the score writes its arrival at rung %s with the seed at "
              "%s of the frame's width — which is what orders that instrument's own releases "
              "outward from the seed" % (cs["instrument"], cs["arrivalHandle"], cs["seedPlace"])
              if reached else "the arrival cast «%s» and the score wrote arrival=%s seedPlace=%s"
                              % (cs["instrument"], cs["arrivalHandle"], cs["seedPlace"]))

        sil = got["crystalSeed"]["silent"]
        silent = (sil["mode"] == "CRYSTALLIZED" and sil["locusKind"] == "none"
                  and sil["seedPlace"] is None)
        check("EX-COMPOSED a work whose record carries no grain reading seeds nowhere and says so",
              silent,
              "the same pair with the relief reading taken out of the record still ranks "
              "CRYSTALLIZED on its grain score, names no place at all («%s») and drives no seed "
              "onto any instrument — the region line at 0.82 is not borrowed to stand in for a "
              "point nobody measured" % sil["locusKind"]
              if silent else "mode «%s», locus kind «%s», seed %s"
                             % (sil["mode"], sil["locusKind"], sil["seedPlace"]))

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
            # The counts are judged as well against the row of the tier the plan DECLARES — §4.7
            # calls a plan whose declared tier its own voices contradict a red, and this is that
            # read.
            row = TIER_BUDGET.get(r.get("tier"))
            if row is None:
                bad.append(f"{role} declares the tier «{r.get('tier')}», which shelf 17 has no row "
                           f"for")
            else:
                for count in ("letters", "accompaniments", "miracles"):
                    if not (row[count][0] <= b[count] <= row[count][1]):
                        bad.append(f"{role} declares a {r['tier']} and spends {b[count]} "
                                   f"{count}, outside that row's {row[count]}")
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

        # --- rows 5e-5f · shelf 17's levels law, at the handles ----------------------------------
        # THE DECLARATION FIRST. A handle that publishes no level would read exactly like a handle
        # that drives nothing, so a half-done migration would close the ban for some instruments and
        # leave it silently open for the rest. The composer treats a missing declaration as levelless
        # because it must not lose a crossing over one; this row is what makes a missing one loud.
        sw = got["sweep"]
        lv = got["levels"]
        lvbad = []
        if lv["undeclared"]:
            lvbad.append(f"handles that declare no level: {lv['undeclared']}")
        if lv["seventh"]:
            lvbad.append(f"handles claiming a level outside shelf 17's six: {lv['seventh']}")
        if lv["outside"]:
            lvbad.append(f"handles claiming a level their own instrument never declares: "
                         f"{lv['outside']}")
        check(NODE_ROWS[60], not lvbad,
              f"every handle of all {lv['instruments']} published instruments declares its own "
              f"structural level or declares none; the levels actually driven are "
              f"{lv['driven']}, all of them inside shelf 17's {lv['six']}"
              + ("; " + "; ".join(lvbad) if lvbad else ""))

        # AND THE LAW ITSELF, read off what each cue actually drives rather than off what it says.
        # A cue drives a handle when that handle has a track on it. Two readings, and both must
        # stand at nothing: a cue driving a handle on a level it does not own, and a level driven by
        # two cues at once. The ground is read like every other cue — it holds no exemption now.
        lawbad = []
        if sw["levelBreaches"]:
            lawbad.append(f"cues driving a handle on a level they do not own: "
                          f"{sw['levelBreachCases']}")
        if sw["levelSharedBy"]:
            lawbad.append(f"levels driven by two cues at once: {sw['levelSharedCases']}")
        check(NODE_ROWS[60], not lawbad,
              "over the sweep at all five roles, no cue drives a handle on a level it does not own "
              "and no structural level is driven by two cues at once"
              + ("; " + "; ".join(lawbad) if lawbad else ""))

        # --- row 5g · what the register promised, against what the composition wrote -----------
        # THE GATE THAT WAS MISSING, AND ITS SHAPE IS THE POINT. Three tables decided independently
        # what a handle is — the register said what it READS, `tracksFor` gave it a TRACK on the
        # strength of having any row at all, and `fillPlan`'s own branch decided whether a VALUE was
        # computed — and nothing held the three against each other. A handle in the first two and not
        # the third reached the node writer with nothing, and the writer wrote
        # `{op: "static", value: <the manifest's own default>}` with no provenance on it: one number
        # for the whole passage, and no sentence saying so.
        #
        # It survived because the only row over it walked a cue's nodes and skipped any whose note
        # did not open with «requested» — blind on exactly the handles the writer had declined to
        # write a note for. This row runs the other way about: it starts from the register's own
        # word and asks whether the composition kept it.
        # A ROW KEPT ON SOME PAIRS AND NOT OTHERS IS A COMPOSITION DECISION, and the plan says why
        # in its own sentences — a colour voice too quiet to be seen leaves its three handles
        # unwritten, which is the lab's own mute. A row kept NOWHERE is something else: the promise
        # was never written at all, and no pair in the world would have kept it. That is the breach
        # this reads, and it is a claim about the register against the code rather than about which
        # photographs happen to be on disk.
        never = sorted(set(sw["promiseSeen"]) - set(sw["promiseKept"]))
        # A `progress` OR `plan` ROW CAN ALWAYS BE KEPT, because what it reads always exists: the
        # passage has a travel on every pair and the plan has named its arrival before this runs. So
        # a row of either kind that the composition never keeps is a defect outright, and that is
        # what this reds on. A `measured` row can honestly go unkept on a pair whose records carry
        # nothing for it — `tunnel.ribs` reads a ring count and answers only where a work was cut as
        # rings — so those are reported beside the row rather than failing it, because whether this
        # sample happens to contain such a pair is a fact about the photographs on disk.
        promised = [k for k in never
                    if (sw["registerOf"].get(k) or "") in ("progress", "plan")]
        check(NODE_ROWS[60], not promised,
              f"every handle whose row promises a measurement, the passage's own travel or a plan's "
              f"word is kept somewhere — {len(sw['promiseKept'])} of {len(sw['promiseSeen'])} "
              f"such handle(s) driven, and every row promising the passage's own travel or a "
              f"plan's word is kept"
              + (f"; measured rows this sample never exercised: {never}" if never else "")
              + (f"; promises broken: {promised}" if promised else ""))

        # AND THE CAST IS NOT NARROWED BY ANY OF IT. The exclusion the cast still makes is one
        # disjunct shorter than it was — the clause that dropped a candidate for standing beside
        # another voice on an ungated level is gone, and removing a disjunct from an OR can only
        # shrink the set it excludes, for any collection whatever. So no candidate that played
        # before can be turned away now, and what the row reads on real records is the other half of
        # the promise: on the named pair whose ground and voice share a level, BOTH still compose,
        # and the one that lost the level goes on driving every handle it owns elsewhere.
        gv = got["groundVoice"]
        acc2 = got["adriftBothWays"]["accompanies"]
        narrowed = []
        # A WALK THAT FINDS NO SUCH PAIR IS NOT THIS ROW FAILING, and it is worth saying which of the
        # two it is. The row asserts a NEGATIVE — no level is driven by two cues that are live
        # together — and `castForKinds`'s own levels clause now closes that shape one stage EARLIER
        # than `ownedTracks` does: a candidate whose levels are all taken by a cue it meets is never
        # cast at all, so the plan handed to `ownedTracks` no longer carries the overlap. The law is
        # kept more strictly than this half was written to check it, not less.
        #
        # WHAT KEEPS THE ROW FROM READING NOTHING is therefore the other two clauses it already
        # carries, and both are live: the sweep's own reading below walks every crossing at all five
        # roles for a handle driven on an unowned level and for a level driven by two cues at once,
        # and `acc2` is a derived witness of `ownedTracks` actually stripping a level from a cue that
        # only accompanies on it. If BOTH of those ever went quiet this half would be vacuous; while
        # either stands, it is not.
        if gv.get("none") and gv["cast"]:
            narrowed.append(f"the pair found composes {gv['cast']}, which is not two voices")
        elif gv["cast"] and len(gv["cast"]) < 2:
            narrowed.append(f"the pair found composes {gv['cast']}, which is not two voices")
        if gv["shared"]:
            narrowed.append(f"levels driven by two cues on {gv.get('pair')} at a "
                            f"{gv.get('role')}: {gv['shared']}")
        if not acc2.get("cast"):
            narrowed.append("the sharing pair casts no adrift cue at all")
        elif not acc2["cellContentDriven"]:
            narrowed.append("the cue that lost SURFACE drives nothing on the level it owns")
        gvSays = (
            f"no pair of the collection casts two cues that declare one level and are live "
            f"together, over {gv.get('walked', 0)} composition(s) walked in the collection's own id "
            f"order at every role (and 6002 by hand on 2026-08-26) — the cast itself now closes the "
            f"shape, one stage earlier than `ownedTracks` does"
            if gv.get("none") else
            f"the pair this run found — {gv.get('pair')} at a {gv.get('role')}, whose cast declares "
            f"{gv.get('declaredOverlap')} on two cues that are live together — composes "
            f"{gv['cast']} with one cue per level ")
        check(NODE_ROWS[60], not narrowed,
              gvSays + 
              f"({json.dumps(gv['byLevel'], ensure_ascii=False)}); on the sharing pair the cue that "
              f"lost SURFACE still drives {len(acc2.get('cellContentDriven') or [])} handle(s) on "
              f"the level it owns"
              + ("; " + "; ".join(narrowed) if narrowed else ""))

        # --- the entry door · a voice joins a running picture without replacing it ---------------
        # The charter's build ladder, step 0, and the oldest standing debt in the engine: every
        # module was built permanently wet, so a layer could only be crossfaded in. The fleet's
        # reserved dry closed the module half; this is the plan half, and the row asks four things
        # of one composed sweep at all five roles.
        #
        # IT IS NOT A CROSSFADE COMING BACK. The row asks that an upper voice's dry be exactly
        # NOTHING at both of its doors — never a half, never a share — so at no instant is one
        # picture weighed against another. A plan that faded would be caught by this row and by the
        # host's own door proof both.
        ed = got.get("entryDoor") or {}
        edbad = []
        if ed.get("badUpperDoor"):
            edbad.append("upper voices whose two doors do not name the dry at nothing: "
                         f"{ed['badUpperDoor']}")
        if ed.get("badUpperArc"):
            edbad.append("upper voices whose dry is not the contract's arc over their own "
                         f"progress — (0,0), (0.5,1), (1,0): {ed['badUpperArc']}")
        if ed.get("badLowestDoor"):
            edbad.append("lowest voices named at no presence at all, which the host refuses "
                         f"outright (`presenceWhyNo`): {ed['badLowestDoor']}")
        if ed.get("badLowestWhole"):
            edbad.append(f"lowest voices not held whole across their window: {ed['badLowestWhole']}")
        if ed.get("badOverlay"):
            edbad.append("«overlay», whose own `presence` is a reading of the pair and not the "
                         f"reserved dry, was driven as though it were: {ed['badOverlay']}")
        check(ROW_ENTRY_DOOR,
              bool(ed) and not edbad and ed.get("upperSeen", 0) > 0 and ed.get("lowestSeen", 0) > 0,
              f"over the sweep at all five roles: {ed.get('upperSeen', 0)} voice(s) standing over "
              f"another and {ed.get('lowestSeen', 0)} lowest voice(s) were read, on a settings "
              f"record with the contract's own dry added to the {ed.get('patched', 0)} manifest(s) "
              f"published before it landed. Every upper voice names both its doors on `presence` at "
              f"nothing and rides the contract's arc across its own window; no lowest voice is ever "
              f"given a door at no presence, and each stands whole throughout. «overlay» keeps its "
              f"own sense of the name on {ed.get('overlaySeen', 0)} sighting(s)"
              + ("; " + "; ".join(edbad) if edbad else ""))

        # --- the harmonic function, and the crest law it decides -------------------------------
        # WHAT WAS WRONG. The client had been writing `routeFunction` beside `routeRole` since the
        # harmonic layer landed, and the composer contained ZERO occurrences of the identifier — the
        # one distinction that layer exists to make was dropped at the seam with nothing saying so.
        # And charter shelf 15's crest law — the culmination's suspension — was read from the two
        # works' tone apartness alone, so a quiet link between tonally distant works dwelt at its
        # middle while a culmination between two works standing close in tone passed straight
        # through. Tone is not what says whether a suspension is owed.
        #
        # WHY THE NAME COULD NOT CARRY IT: a subdominant and a dominant that does not stand at the
        # route's crest are BOTH called a middle (`passRoleOfFunction`, engine/client/01a-pass.js),
        # and those two are exactly the pair the composer most needs apart — one prepares, the other
        # is a tension demanding resolution.
        hm = got["harmonic"]
        hmbad = []
        if hm["read"] != "subdominant":
            hmbad.append(f"a middle stating no function reads «{hm['read']}» rather than the "
                         "subdominant shelf 15's own map makes it")
        if hm["readWhenStated"] != "dominant":
            hmbad.append(f"a middle stating «dominant» reads «{hm['readWhenStated']}»")
        if hm["readWhenStray"] != "subdominant" or not hm["strayRecorded"]:
            hmbad.append(f"a function outside the three read «{hm['readWhenStray']}» and was "
                         f"recorded as {hm['strayRecorded']}")
        if hm["tonicHeld"]:
            hmbad.append(f"tonic steps whose course dwells at its middle: {hm['tonicWitness']}")
        if hm["subHeld"]:
            hmbad.append(f"subdominant steps whose course dwells: {hm['subWitness']}")
        if not hm["domHeld"]:
            hmbad.append(f"no dominant step suspends at all, over {hm['domSeen']} course(s)")
        if hm["plainHolds"] == hm["statedHolds"] and hm["statedHolds"]["held"] == 0:
            hmbad.append("stating the function changes nothing about the same pair at the same "
                         "role on the same die, so the distinction is still dropped")
        check(ROW_HARMONIC, not hmbad,
              f"one pair at one role on one die: stating nothing reads «{hm['read']}» and its "
              f"course {hm['plainHolds']}, stating «dominant» reads «{hm['readWhenStated']}» and "
              f"its course {hm['statedHolds']}, and «plagal» reads «{hm['readWhenStray']}» with "
              f"{len(hm['strayRecorded'])} note(s) on the request. Over the corner at all five "
              f"roles: {hm['domHeld']} of {hm['domSeen']} dominant courses suspend, and no tonic "
              f"({hm['tonicSeen']} course(s)) or subdominant ({hm['subSeen']}) course does"
              + ("; " + "; ".join(hmbad) if hmbad else ""))

        # --- what a cue declares it costs ------------------------------------------------------
        # §7 gives this to the INSTRUMENT: it declares textures, texture slots, framebuffers,
        # ping-pong pairs, programs, passes and a byte estimate PER QUALITY VARIANT, the host grants
        # against that declaration at `prepare` and counts what was created against it at runtime,
        # and conformance row 22 reds a declaration that understates its bytes. The composer carries
        # the declaration onto the cue; it must never author one, because a cost the composer
        # invented is a number the host would then measure a real instrument against.
        #
        # `resourcesBlock` typed one block for every cue of every score at every quality, so no
        # crossing could declare a cost different from any other, the quality ladder could not be
        # walked on cost, and row 22 had nothing to judge. The row reads a settings record patched
        # with a declaration that differs per instrument AND per variant, and asks that what reaches
        # each cue is that instrument's own row.
        cost = got["cost"]
        costbad = []
        if cost["wrong"]:
            costbad.append(f"cues carrying a declaration that is not their instrument's own: "
                           f"{cost['wrong']}")
        if cost["flatVariants"]:
            costbad.append(f"cues whose lean and rich rungs declare the identical block, so the "
                           f"ladder cannot be walked on cost: {cost['flatVariants']}")
        if not cost["checked"]:
            costbad.append("no cue was read at all")
        check(ROW_COST, not costbad,
              f"over {cost['checked']} cue-and-variant reading(s), against a record in which each of "
              f"the {cost['declarations']} published instruments declares its own cost per variant, "
              f"every cue carries its own instrument's declaration and the three rungs differ"
              + ("; " + "; ".join(costbad) if costbad else ""))

        # --- the day on the request -------------------------------------------------------------
        # Charter shelf 16 asks for both the day's weather bias and a seeded run that repeats, and
        # never said which answers first. Its own last two sentences do: seeds and determinism are
        # the JUDGING mode, ephemerality is the VIEWER mode. So the day is an input the walk states
        # in the mode that has one and never a call the composer makes — a public walk sends the
        # instant it cast the pair, a pinned walk sends none and the run reproduces to the pixel.
        #
        # THE SECOND HALF OF THIS ROW IS THE ONE THAT COULD HAVE BEEN LOST QUIETLY. Deleting the
        # clock makes the reproducibility rows green on its own; it would also delete shelf 16's
        # third step, and nothing would have said so. The row therefore asks that a day still MOVES
        # a composition, not only that its absence leaves one still.
        dy = got["day"]
        daybad = []
        if dy["unstable"]:
            daybad.append(f"{dy['unstable']} pair(s) stating no day composed two different scores "
                          "from one request")
        if dy["dayUnstable"]:
            daybad.append(f"{dy['dayUnstable']} pair(s) stating one day twice composed two "
                          "different scores")
        if not dy["moved"]:
            daybad.append(f"over {dy['pairs']} pair(s), no composition moved between two days six "
                          "months and twelve hours apart — the day reaches no die and shelf 16's "
                          "third step is deleted rather than moved onto the request")
        if dy["readsNone"] is not None or dy["readsOne"] is None:
            daybad.append(f"a request stating no day reads {dy['readsNone']} and one stating a day "
                          f"reads {dy['readsOne']}")
        if dy["strayRead"] is not None or not dy["strayRecorded"] or not dy["strayMatchesNone"]:
            daybad.append(f"a day that names no instant read {dy['strayRead']}, was recorded as "
                          f"{dy['strayRecorded']} and composed the neutral: {dy['strayMatchesNone']}")
        check(ROW_DAY, not daybad,
              f"over {dy['pairs']} pair(s): one request stating no day composes the same score "
              f"twice, and so does one stating a day; {dy['moved']} of them compose differently on "
              f"two days six months and twelve hours apart (first: {dy['firstMove']}); a day that "
              f"names no instant is left unread with {len(dy['strayRecorded'])} note(s) on the "
              f"request and composes exactly what stating none composes"
              + ("; " + "; ".join(daybad) if daybad else ""))

        # --- rows 5b-5d · shelf 6's one slot, counted by the declaration ------------------------
        # THE SUBJECT OF THE LAW IS WHAT AN INSTRUMENT DECLARES, NOT WHAT IT IS CALLED. Naряд S-18
        # (2026-08-27) moved `spendsTheMiracle`'s reading of WHICH instruments fold off the
        # manifest's shared `levels` mark (which also carries shelf 17's own camera-ownership law)
        # onto the instrument's own identity, kept beside the function it feeds — and the driver
        # reads the very same list back off `composer.worldFoldInstruments` rather than keeping a
        # second copy, so neither side names an instrument twice. Whether a given cast of one of the
        # four actually SPENDS the slot now also asks the walk's own history (`walkMiracles`); this
        # sweep sends none, so every read below still answers "first play" for each of the four,
        # exactly as the retired manifest mark always did — the row proving the history itself is
        # its own, separate row (below, the rarity-on-a-walk check).
        # A planted run walks a corner of the collection rather than all of it, because a plant is
        # judged on whether the answer MOVES and twenty-four works are 552 ordered pairs of proof.
        CORNER = 24
        sw = got["sweep"]
        worlds = sw["spendsTheMiracle"]
        unvoiced = {r: n for r, n in sw["worldNotVoiced"].items() if n}
        castWorlds = sorted(sw["worldSeen"])
        check(NODE_ROWS[54],
              not unvoiced and castWorlds == sorted(worlds),
              f"the collection publishes {len(worlds)} instrument(s) that declare the world — "
              + ", ".join(worlds)
              + f" — and the cast reaches every one of them ({', '.join(castWorlds)}); each is "
              f"voiced the crossing's one miracle wherever it stands"
              + (f"; cues that were not: {unvoiced}" if unvoiced else ""))

        # A ROLE THAT SPENDS NO MIRACLE NEVER OPENS A WORLD, and what holds that is a BOUND. The
        # ranking's own nudge — `castForKinds` demoting a world candidate one order under
        # `noMiracle` — decides which candidate is likeliest and never which may stand, so the row
        # asks the question with the nudge taken away: the three follow-up gates, one per cast slot,
        # must carry the law by themselves. `nudged` is that run.
        no_miracle_roles = ("entrance", "quiet link", "return")
        opened = {r: sw["worldsCast"][r] for r in no_miracle_roles if sw["worldsCast"][r]}
        nudged = node_run([["        var base = (cuts ? 0 : 2) + ((noMiracle && folds) ? 1 : 0);",
                            "        var base = (cuts ? 0 : 2);"]], sweep=CORNER)
        nudged_opened = ({} if nudged.get("error") else
                         {r: nudged["sweep"]["worldsCast"][r] for r in no_miracle_roles
                          if nudged["sweep"]["worldsCast"][r]})
        check(NODE_ROWS[56],
              not opened and not nudged.get("error") and not nudged_opened,
              f"no world-declaring instrument is cast at an {', a '.join(no_miracle_roles)} — and "
              f"with the ranking's own nudge removed in a copy, so that a world instrument ranks "
              f"level with every other candidate, still none is"
              + (f"; opened anyway: {opened}" if opened else "")
              + (f"; opened with the nudge gone: {nudged_opened}" if nudged_opened else "")
              + (f"; the planted run failed: {nudged['error']}" if nudged.get("error") else ""))

        # TWO WORLDS NEVER STAND TOGETHER, by either road that puts them within reach — the levels
        # test at a cast, and §7's coverage law re-casting the ground after the arrival is already
        # placed. The sweep answers for the ranking's own choices; the two named ordered pairs
        # answer for the two roads themselves, each chosen because it reaches for the slot twice by
        # that road and by no other.
        one = got["oneSlot"]
        stacked_roles = {r: n for r, n in sw["worldStack"].items() if n}
        doors = {k: v for k, v in one.items() if v["worlds"] != 1 and v["worlds"] != 0}
        check(NODE_ROWS[58],
              not stacked_roles and not doors,
              "no crossing of the sweep carries two instruments that declare the world; the pair "
              "that reaches for it through the levels test composes "
              f"{one['levels']['cues']} and the pair that reaches for it through §7's ground swap "
              f"composes {one['swap']['cues']}"
              + (f"; crossings carrying two: {stacked_roles}" if stacked_roles else "")
              + (f"; the two named pairs: {doors}" if doors else ""))

        # --- row 5e · the miracle is a reading of the walk, not a mark an effect keeps for life ---
        # Naряд S-18 (2026-08-27), his word of 2026-08-26 20:17: a miracle is a wow, a concept, it
        # is subjective, and repeated it stops being one. Nine steps of the SAME edge, the walk's
        # own `walkMiracles` threaded forward exactly as `01a-pass.js` would thread it: step 1 casts
        # a fold and voices it the miracle; every step after names that same fold in its own walk
        # history, so the slot it no longer spends is free, and this collection's own second
        # world-declaring instrument (excluded from standing beside the first by the very levels-law
        # row just above) takes it instead — a second fold, once, and never again either.
        mr = got["miracleRarity"]
        rr_bad = [s for s in mr["steps"] if s["declined"]]
        rr_first = mr["steps"][0]["miracle"] if mr["steps"] else None
        rr_second = mr["steps"][1]["miracle"] if len(mr["steps"]) > 1 else None
        rr_reach = mr.get("foldsWithinReach") or []
        # THE RUN PRINTS THE COUNT ITSELF and the row reads it against one. `mostVoiced` is the
        # largest number of times any one strong move played the miracle over these nine steps —
        # the whole of what rarity means here said as a number, so the row can be read without
        # taking its own prose on trust and the planted run below moves a number rather than a word.
        rr_counts = ", ".join(f"«{k}» {v}×" for k, v in sorted(mr["voicedCount"].items())) or "none"
        check(ROW_MIRACLE_RARITY,
              not rr_bad and len(mr["steps"]) == 9 and len(rr_reach) >= 2
              and rr_first is not None
              and rr_second is not None and rr_second != rr_first
              and mr["mostVoiced"] <= 1 and not mr["repeats"],
              f"nine steps of one edge, walkMiracles threaded forward. THE STRONG MOVE PLAYED THE "
              f"MIRACLE AT MOST {mr['mostVoiced']} TIME(S) OVER THE NINE STEPS ({rr_counts}), "
              f"against the law's own one. The crossing's own bundle "
              f"ledger puts {len(rr_reach)} fold(s) within reach of it ({', '.join(rr_reach) or 'none'}), "
              f"which is what a freed slot can be handed on TO; step 1 voices «{rr_first}» the "
              f"miracle; with «{rr_first}» now in the walk's own history step 2 no longer voices it "
              f"and voices «{rr_second}» instead — a different fold takes the freed slot in the "
              f"same crossing; over all nine steps {len(mr['distinctFolds'])} distinct fold(s) were "
              f"ever the miracle ({', '.join(mr['distinctFolds'])}) and none twice: {mr['repeats'] or 'none'}"
              + (f"; steps that declined: {rr_bad}" if rr_bad else ""))

        # --- row 5e red-on-bug · the static mark restored, and the same walk spends twice --------
        # THE PLANT IS THE DEFECT ITSELF, put back in one line: `spendsTheMiracle` reading the
        # instrument's own standing declaration and nothing about this walk — which is how it read
        # before naряд S-18 moved the count onto the walk's own history. On the same nine steps of
        # the same edge, the same fold is then free to be the miracle again, and the count the run
        # prints for itself climbs past one. What this row proves is that the row above is held up
        # by the reading and not by the edge: an edge whose second step simply never casts a fold
        # would pass the row above with the reading struck out, and this shows it does not.
        _rr_red = node_run(plants=[["return isWorldFold(iid) && walkMiracles.indexOf(iid) < 0;",
                                    "return isWorldFold(iid);"]], sweep=1)
        _rr_red_mr = (_rr_red.get("miracleRarity") or {}) if isinstance(_rr_red, dict) else {}
        _rr_red_counts = ", ".join(f"«{k}» {v}×"
                                   for k, v in sorted((_rr_red_mr.get("voicedCount") or {}).items()))
        check(ROW_MIRACLE_RARITY_RED,
              bool(_rr_red_mr) and _rr_red_mr.get("mostVoiced", 0) > 1,
              f"with the walk's own history struck out of `spendsTheMiracle` and the standing "
              f"declaration read alone, the same nine steps of the same edge give "
              f"{_rr_red_mr.get('mostVoiced')} play(s) of one strong move as the miracle "
              f"({_rr_red_counts or 'none'}) against the shipped run's {mr['mostVoiced']} — so the "
              f"row above is held up by the reading of the walk and by nothing else"
              + (f"; the planted run failed: {_rr_red.get('error')}"
                 if isinstance(_rr_red, dict) and _rr_red.get("error") else ""))

        # --- row 5a · the length is composed from the pair, inside its tier's own band ----------
        # BOTH HALVES ARE PROVED BY CONSTRUCTION, not by sampling pairs. The band's own half is
        # walked over the WHOLE span of the share that places a length inside it, ends included and
        # both sides of both ends; the share's own half is walked over the whole real line the
        # logarithm of one measured door step over the other can be. What is read off real pairs is
        # only the last thing, which is not a bound at all: two different ordered pairs at one role
        # come out at different lengths, which one typed constant per role could not do.
        ln = got["length"]
        wrong = list(ln["broke"])
        if not (ln["shareLo"] >= 0 and ln["shareHi"] <= 1):
            wrong.append(f"the share ran [{ln['shareLo']}, {ln['shareHi']}], outside [0, 1]")
        # NO BAND IS WIDER THAN THE ONE THE CHARTER GIVES IT, AND THERE ARE ONLY THREE BANDS. A
        # length placed inside a band that had been opened first would be the charter widened under
        # cover of placing it, so both tables the composer publishes are read against shelf 17's own
        # three rows here — and a role band that is not one of those three rows exactly is a fourth
        # band nobody named, which this reds on.
        for tier, want_band in TIER_SECONDS.items():
            if ln["tierBands"].get(tier) != list(want_band):
                wrong.append(f"the {tier} tier band is {ln['tierBands'].get(tier)}, and shelf 17's "
                             f"row is {list(want_band)}")
        for role, want_band in ROLE_SECONDS.items():
            got_band = ln["bands"].get(role)
            if got_band != list(want_band):
                wrong.append(f"the {role} band is {got_band}, not {list(want_band)}")
            elif got_band not in [list(b) for b in TIER_SECONDS.values()]:
                wrong.append(f"the {role} band {got_band} is a fourth band, and shelf 17 names "
                             f"three: {json.dumps(TIER_SECONDS)}")
        same = []
        for role, r in ln["perRole"].items():
            for which, tier_key in (("one", "tierOne"), ("two", "tierTwo")):
                if r[which] is None:
                    same.append(f"{role} composed nothing for the {which} pair")
                    continue
                ms, band, tband = r[which]["ms"], r["band"], r[tier_key]
                if not ((band[0] <= ms <= band[1]) or (tband and tband[0] <= ms <= tband[1])):
                    same.append(f"{role} ran {ms} ms declaring a {r[which]['tier']}, outside its "
                                f"role band {band} and outside that tier's {tband}")
            if r["one"] is not None and r["two"] is not None and r["one"]["ms"] == r["two"]["ms"]:
                same.append(f"{role} ran {r['one']['ms']} ms for both pairs")
        check(NODE_ROWS[52], not wrong and not same,
              f"{ln['walked']} values walked: every band "
              f"{json.dumps(ln['bands'], ensure_ascii=False)} over shelf 17's own "
              f"{json.dumps(ln['tierBands'], ensure_ascii=False)} holds for every share, floor at a "
              f"share of nothing and ceiling at a whole one, and the share the length is placed by "
              f"ran [{ln['shareLo']}, {ln['shareHi']}] over the whole real line the two door steps "
              f"can ask for; two ordered pairs come out at "
              + "; ".join(f"{k} {v['one'] and v['one']['ms']}/{v['two'] and v['two']['ms']} ms in "
                          f"{v['band']}" for k, v in ln["perRole"].items())
              + ("; " + "; ".join(wrong + same) if (wrong or same) else ""))

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
        # READ ON TWO NAMED PAIRS, ONE FOR EACH SIDE OF THE LEVELS LAW, and no longer on whichever
        # adrift cues a corner of the collection happens to cast. Since every handle declares the
        # level it drives, adrift's seam is written only where adrift's cue OWNS SURFACE — on a pair
        # whose ground drives SURFACE the ground owns it and adrift rests there, which is the law
        # rather than a wire that stopped working. So the wire is proved where the wire is live, and
        # the resting is proved beside it. The sweep's own readings are still checked wherever they
        # occur; they are no longer what makes the row non-vacuous.
        ab = got["adriftBothWays"]
        seams = sweep["adriftSeams"]
        seamMismatch = [s for s in seams
                         if abs(s["applied"] - (s["recordSeam"] or 0)) > 0.0002]
        seamValues = sorted(set(s["applied"] for s in seams))
        onlyBinary = seamValues and all(v in (0, 1) for v in seamValues)
        owns, acc = ab["owns"], ab["accompanies"]
        seambad = []
        if not owns.get("cast"):
            seambad.append("the owning pair casts no adrift cue at all")
        else:
            if owns["owns"] != "owns":
                seambad.append(f"the owning pair's adrift cue reads «{owns['owns']}» on SURFACE")
            if owns["seamApplied"] is None:
                seambad.append("the owning pair drives no seam at all")
            elif abs(owns["seamApplied"] - owns["recordSeam"]) > 0.0002:
                seambad.append(f"the owning pair applied {owns['seamApplied']} against the record's "
                               f"own {owns['recordSeam']}")
            elif owns["seamApplied"] in (0, 1):
                seambad.append("the owning pair's seam reads back as presence-or-absence")
        if not acc.get("cast"):
            seambad.append("the accompanying pair casts no adrift cue at all")
        else:
            if acc["owns"] == "owns":
                seambad.append("the accompanying pair's adrift cue owns SURFACE after all")
            if acc["surfaceDriven"]:
                seambad.append(f"the accompanying cue still drives {acc['surfaceDriven']} on a "
                               f"level it does not own")
            if not acc["cellContentDriven"]:
                seambad.append("the accompanying cue drives nothing on the level it does own")
        check(NODE_ROWS[35],
              not seambad and not seamMismatch and not onlyBinary,
              f"where adrift owns SURFACE it applies {owns.get('seamApplied')} against the record's "
              f"own {owns.get('recordSeam')}, driving {owns.get('surfaceDriven')} there; where "
              f"another cue owns it adrift drives {acc.get('surfaceDriven')} on SURFACE and goes on "
              f"driving {len(acc.get('cellContentDriven') or [])} handle(s) on the level it does "
              f"own. Over the sweep {len(seamMismatch)} of {len(seams)} readings sit off the "
              f"record's own structure.horizon.seam by more than 0.0002; distinct values seen: "
              f"{seamValues[:12]}" + (" …" if len(seamValues) > 12 else "")
              + ("; " + "; ".join(seambad) if seambad else ""))

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
        # WHAT «DRIVEN OFF THE WORKS» IS READ AS HERE, AND WHY IT IS NOT «DISTINCT ACROSS THE
        # SWEEP» (changed 2026-09-02). Grid-colour's own row above reads distinctness across the
        # sweep because it can: it is sighted owning LIGHT-COLOUR 80 to 200 times. Strata-light is
        # sighted owning it four times in the whole fleet — `ownTheLevels` deprioritises the pivot
        # cue on every level but SURFACE and this instrument plays pivot far more often than not, so
        # the only way it wins the level is standing alone on it. Those four sightings shared one
        # departing work after `placeTheStack`'s ground-is-the-pivot repair re-cast the 71 passages
        # that used to hand the floor to a short-windowed cue, so every A reading among them is one
        # number and a distinctness clause over them measures which works the sweep happened to
        # land on rather than anything the writer does. Widening does not answer it either: walked
        # at 288, 363 and 480 ordered pairs the bucket grows to four sightings and stays at ONE
        # distinct value.
        #
        # THE TWELVE HANDLES ARE SIX READINGS TAKEN TWICE — the A set off the departing work's own
        # colour.sat/brightness/contrast, the B set off the arriving work's — so ONE sighting
        # already carries the same formula applied to two different works, and A standing apart from
        # B is the writer reading a record rather than carrying a constant. That holds on every
        # sighting there will ever be, whatever the sweep catches, which the clause it replaces
        # could not say. Read pairwise below, beside the non-zero clause that already stood.
        def slPairsApart(bucket):
            pairs = [("colourPeriodA", "colourPeriodB"), ("colourAmpA", "colourAmpB"),
                     ("lightPeriodA", "lightPeriodB"), ("lightAmpA", "lightAmpB")]
            for ha, hb in pairs:
                va, vb = bucket.get(ha) or [], bucket.get(hb) or []
                if not va or len(va) != len(vb):
                    return False
                if not all(abs(x - y) > 1e-9 for x, y in zip(va, vb)):
                    return False
            return True
        slVariesOk = (all(bool(slVoices[h]) and any(abs(v) > 1e-9 for v in slVoices[h])
                          for h in SL_VARIES)
                      and slPairsApart(slVoices))
        # Read the same way row 8d's phases are, and for the same reason: a muted voice rests all
        # three of its handles together, so a phase at 0 must have its own amplitude at 0 beside it.
        slPhaseOk = all(phaseHolds(slVoices, h, c, h.replace("Phase", "Amp"))
                        for h, c in SL_PHASE_CONST.items())
        check(NODE_ROWS[38], slVariesOk and slPhaseOk,
              "on cues that OWN LIGHT-COLOUR, every handle read off the departing work standing "
              "apart from its own twin read off the arriving one: "
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
        allSilent = all(not off for off in accOffZero.values())
        # WHAT MAKES THIS ROW NON-VACUOUS MOVED WHEN OWNERSHIP LEARNED THE WINDOWS. It used to
        # require a sighting of an accompanying cue, and accompaniment was common because a single
        # owner held a level for the whole passage. Now two cues that are never live together each
        # own the level in their own stretch, so accompaniment on LIGHT-COLOUR arises only where two
        # colour voices genuinely overlap — which this sample need not contain. So the row stands on
        # the mechanism being live (some cue owns the level and sings there, the row above) plus the
        # law itself: wherever a cue does only accompany, not one of the eighteen handles is on its
        # track list. A sighting is reported when it happens and is no longer what the row rests on.
        ownsSightings = sum(len(vs) for vs in
                            list(sweep["gridColourVoicesOwns"].values())
                            + list(sweep["strataLightVoicesOwns"].values()))
        check(NODE_ROWS[39],
              ownsSightings > 0 and not sweep["accStillDriven"] and allSilent,
              f"{sweep['accSightings']} sighting(s) of a cue accompanying another on LIGHT-COLOUR "
              f"and {ownsSightings} reading(s) on cues that own it; on no accompanying cue does any "
              f"of the eighteen colour and light handles carry a node at all — the handles are off "
              f"its track list, so the client writes the manifest's own rest for each. Handles "
              f"still driven there: {sweep['accStillDriven'] or 'none'}; readings that were present "
              f"and off 0: { {k: v for k, v in accOffZero.items() if v} or 'none' }")

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
        # THE READING IS CHECKED WHEREVER THE SWEEP LANDS; THE REACH IS CHECKED WHERE IT WAS SOUGHT.
        # Those are two different questions and they had one answer between them, which is why this
        # row went red on 2026-08-26 without a single gate field having moved in a single record:
        # the ranking stopped casting `gates` on a horizontally-slotted departing work inside the
        # 192-pair spot, and the row reported that as a defect in the reading. The correctness
        # clause still runs over everything the sweep touched, which is the wider sample and the
        # right place for it. The two spread clauses now run over `gateSlotWitness`, the pairs the
        # driver went looking for — so «I did not see both axes» becomes a statement about the
        # collection rather than about which 192 pairs happened to be walked.
        gs = sweep["gateSlots"]
        wit = got["gateSlotWitness"]
        both = wit["readings"] + gs
        gsMismatch = [r for r in both if r["record"] is not None
                      and abs(r["applied"] - r["record"]) > 0.0002]

        def seenIn(rows, h):
            return sorted(set(r["applied"] for r in rows if r["handle"] == h))
        placeSeen = seenIn(wit["readings"], "slotPlace")
        halfSeen = seenIn(wit["readings"], "slotHalf")
        axisSeen = seenIn(wit["readings"], "slotAxis")
        # A witness search that reached nothing is a red of its own, and a different one: it says
        # the corner walked holds no such pair, not that the slot is misread.
        gsBad = []
        if not both:
            gsBad.append("no gates cue was cast at all, by the sweep or by the witness search")
        if gsMismatch:
            gsBad.append(f"{len(gsMismatch)} applied slot(s) off the departing work's own record")
        if len(placeSeen) <= 1:
            gsBad.append(f"the witness search reached {len(placeSeen)} distinct slotPlace, so this "
                         f"run cannot say the place is the slot's own rather than one number reused")
        if len(halfSeen) <= 1:
            gsBad.append(f"the witness search reached {len(halfSeen)} distinct slotHalf")
        if axisSeen != [0, 1]:
            gsBad.append(f"the witness search reached slotAxis {axisSeen} rather than both 0 and 1, "
                         f"over {wit['tried']} ordered pair(s) walked")
        check(NODE_ROWS[41], not gsBad,
              f"{len(gs)} gate slot reading(s) over the sweep and {len(wit['readings'])} more from "
              f"{len(wit['pairs'])} pair(s) the witness search found in {wit['tried']} walked; "
              f"{len(gsMismatch)} off the departing work's own record by more than 0.0002; "
              f"slotPlace {len(placeSeen)} distinct {placeSeen[:8]}, slotHalf {len(halfSeen)} "
              f"distinct {halfSeen[:8]}, slotAxis seen {axisSeen}"
              + ("; " + "; ".join(gsBad) if gsBad else ""))

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
        # WHAT PROVES IT, AND IT IS THE FORMULA AND NOT A TALLY. `coolOf` multiplies a candidate's fit
        # by (k + 1) / (n + 1), where k is where the letter sits in the walk's own list. Read as
        # arithmetic and not as an outcome, that factor settles both halves of this row for any walk,
        # any collection and any pool:
        #   · it is at most 1 and it is never 0. k runs 0..n−1, so the factor runs 1/(n+1)..n/(n+1) —
        #     strictly inside (0, 1). A letter the walk has not played is not in the list at all and
        #     keeps its whole weight. So a played letter's stretch of the die NARROWS and a rival's
        #     widens, which is the cooling; and no candidate's weight ever reaches zero, so no pool
        #     is ever emptied and no step can lose its crossing to a cooldown. That is shelf 9's law
        #     («a measurement ranks the genres», never gates) holding by construction.
        #   · the most recent letter is the most cooled. k = 0 for the letter just played gives the
        #     smallest factor and k = n−1 the largest, in even steps between — the cooling fades with
        #     distance rather than switching off, again for any n.
        # None of that is a claim about which photographs are on disk, so no count of pairs could
        # strengthen it and none could weaken it.
        #
        # WHAT `n` IS, AND HIS 2026-08-26 WORD ABOUT IT. Until that word, `n` was `walkPlayed.length`
        # — the raw length of the walk's own log, a quantity with no ceiling (a passage played a
        # thousand times over a long visit still pushes a thousand entries). That let the floor for
        # the letter JUST played (k = 0) fall toward 0 as a visit ran on, and past n = 100 it already
        # inverted any fit gap, however wide, for no reason but the log's length — the one factor of
        # `dieWeighted`'s four whose own bound moved with something that has nothing to do with fit
        # (`viewerBiasOf` and `weatherBiasOf` both hold fixed floors, 0.7 and 0.65, on every request).
        # `n` now counts the DISTINCT letters the log holds, never how many times any one of them was
        # logged, so it is bounded by the walk's own vocabulary — the eight roads, or the collection's
        # fixed instrument list — for as long as the visit runs. Row 8j-2 below proves both halves of
        # that repair as arithmetic, over the whole span of place and pool size, not on this route.
        #
        # WHAT THE TWO WALKS BELOW ARE FOR, THEN. They are a SMOKE reading: the reading actually
        # crosses the wire from the walk into the die, the composer takes it, and a real route
        # composed with it still composes every step it composed without it. The two walks are the
        # same 40 routes on the same dice, one blind and one handed its own memory. The row holds the
        # mechanism (the remembered walk leans less on one letter, loses nothing, and covers at least
        # as many letters); the numbers travel in the detail as a reading a person can look at, and
        # they are evidence of nothing beyond these routes on these records.
        rt0, rt1 = got["route"], got["routeRemembered"]
        check(NODE_ROWS[46],
              rt1["topShareMean"] < rt0["topShareMean"] and rt1["lost"] == 0
              and rt1["composed"] == rt0["composed"] and rt1["letters"] >= rt0["letters"],
              f"smoke, on the records that happen to be on disk: the reading reaches the die and a "
              f"remembered walk leans less on its commonest letter than the same walk composed "
              f"blind, loses no step ({rt1['lost']}), composes the same count "
              f"({rt1['composed']} against {rt0['composed']}) and covers "
              f"{rt1['letters']} letters against {rt0['letters']}. The law itself — a cooling factor "
              f"in (0, 1] that narrows a played letter's stretch and can never empty a pool — is the "
              f"shape of (k+1)/(n+1) and holds for any walk; see the note above. Remembered spread "
              + json.dumps(rt1["spread"], ensure_ascii=False))

        # --- row 8j-2 · THE COOLDOWN'S OWN FLOOR, PROVED OVER NUMBERS AND NOT OVER A ROUTE ---------
        # His 2026-08-26 word: «разнообразие необходимо, вопрос в ранжировании». `coolFactor(at,
        # poolSize)` is the module's own ratio and `walkCooldown(list, id)` is its exact production
        # path from a raw walk-memory list down to that ratio (pass-composer.js :2501-2531),
        # exposed for the same reason `camVoiceFloor` is (:8996): a claim about numbers is answered
        # over the numbers.
        ca = got["cooldownArith"]
        check(ROW_COOLDOWN_ARITH,
              not ca["sweepBad"]
              and ca["longLogFixedFloor"] == ca["oneLogFixedFloor"] == 0.5
              and ca["neverPlayedStaysWhole"] == 1
              and ca["longLogFixedFloor"] > ca["longLogOldFloorWouldHaveBeen"] * 100,
              "swept every (at, poolSize) from at=-1 through poolSize=64: coolFactor(-1, ·) is "
              "always exactly 1 and coolFactor(at, ·) for at>=0 always lands in (0, 1] rising with "
              "at" + ("" if not ca["sweepBad"]
                      else "; violations: " + json.dumps(ca["sweepBad"][:5], ensure_ascii=False))
              + f". A log of 1000 entries all naming one letter and a log of exactly 1 entry naming "
              f"it give the SAME floor for that letter now "
              f"({ca['longLogFixedFloor']} both), where the raw log length the old formula read "
              f"would have handed the 1000-entry walk {ca['longLogOldFloorWouldHaveBeen']} — under "
              f"a hundredth of the fixed floor — for no reason but how long the visit had run. A "
              f"letter never played keeps its whole weight ({ca['neverPlayedStaysWhole']}).")

        # --- row 8j-3 · THE ROAD'S OWN POOL, NEVER THE MIXED ONE (his 2026-08-26 night-run
        # adversarial follow-up on this same fix, a live production walk) ---------------------------
        # His report, word for word: the fix made the floor `(at+1)/(pool+1)` bounded where it had
        # been unbounded, but the pool it divides by mixes roads and instruments into one list
        # (`passWalkMemory` pushes a step's genre AND every instrument its stack carried), so the
        # divisor reaches ~35 rather than 8 and the floor for a road just played sits near 1/36. His
        # own live numbers: a fitness of 0.1394 beat 0.901 and 0.1955 beat 0.943, and «после — 0.88
        # не проигрывает 0.14 ни при какой длине визита» is false at a pool of six or wider.
        #
        # THE REPAIR IS A SECOND, ROADS-ONLY CHANNEL rather than a filter over the mixed one: a road
        # and an instrument can share a spelling (`kaleidoscope` names both), so telling them apart
        # after they are flattened into one list is not sound. `01a-pass.js`'s `passWalkGenres` reads
        # `step.genre` alone, never `step.stack`, and rides the wire as `walkGenres` beside
        # `walkMemory`; `pickGenre` cools off it (`coolOfRoad`) and every instrument cast still
        # cools off the mixed `walkMemory` pool exactly as before.
        #
        # PROVED TWO WAYS. First, on the composer's own request diagnostics: a request naming his
        # report's own shape — the walk's eight roads plus twenty-seven instruments, one mixed list —
        # echoes back a `walkGenres` of exactly the eight roads and never absorbs the instruments
        # beside them, so the floor `coolFactor(0, ·)` divides by is fixed at 8 (1/9) rather than the
        # mixed list's own length. Second, on the composer's own source: `pickGenre` — the one die
        # that used to cool a road off the mixed pool — now names `"road"` rather than the bare `1`
        # every instrument cast still passes, read at `PICK_GENRE_READS_ROAD` above rather than
        # assumed from the numbers composing right.
        rp = got["roadPool"]
        road_wiring_note = ("confirmed" if PICK_GENRE_READS_ROAD
                             else "NOT FOUND — pickGenre still reads the mixed pool")
        check(ROW_ROAD_POOL,
              rp["mixedLen"] == 35 and rp["mixedDistinct"] == 35
              and rp["roadLen"] == 8 and rp["roadDistinct"] == 8
              and rp["roadPoolRead"] == 8 and rp["letterPoolRead"] == 35
              and abs(rp["floorAtEight"] - 1 / 9) < 1e-9
              and rp["floorAtMixed"] < rp["floorAtEight"] / 3
              and PICK_GENRE_READS_ROAD,
              f"a request naming eight roads and twenty-seven instruments in one {rp['mixedLen']}"
              f"-entry `walkMemory` echoes back a `walkGenres` of {rp['roadDistinct']} distinct "
              f"entries, never {rp['mixedDistinct']}, and the composition's own diagnostics say the "
              f"two coolings then DIVIDED by {rp['roadPoolRead']} and {rp['letterPoolRead']} "
              f"respectively — the road off the roads, the letter off the mixed list. So the floor "
              f"for a road just played is fixed at "
              f"{rp['floorAtEight']:.4f} (1/9), not the {rp['floorAtMixed']:.4f} (~1/36) the mixed "
              f"pool his report measured would give it, and `pickGenre`'s own source names "
              f"«road» rather than the mixed pool's «1»: {road_wiring_note}.")

        # --- row 8j-3 red-on-bug · the one shared pool given back -------------------------------
        # THE PLANT IS THE DEFECT HIS NIGHT RUN FOUND, put back in one line: the road channel's own
        # pool set to the letters' mixed one, which is what a road cooled off before `walkGenres`
        # rode the wire as a second channel. The row above then has nothing left holding it up — the
        # request echo still shows two lists arriving apart and `pickGenre`'s source still names
        # «road», both untouched by any plant — so what has to move is the number the composition
        # itself publishes about what it divided by, and it does: the road's floor goes back onto
        # the mixed list's own length, near a thirty-sixth where the design says a ninth.
        _rp_red = node_run(plants=[["roadPlayedDistinct = dedupeMostRecent("
                                    "Array.isArray(roadPlayed) ? roadPlayed : []);",
                                    "roadPlayedDistinct = walkPlayedDistinct;"]], sweep=1)
        _rp_red_rp = (_rp_red.get("roadPool") or {}) if isinstance(_rp_red, dict) else {}
        check(ROW_ROAD_POOL_RED,
              bool(_rp_red_rp)
              and _rp_red_rp.get("roadPoolRead") == _rp_red_rp.get("letterPoolRead") == 35
              and _rp_red_rp.get("roadLen") == 8,
              f"with the roads-only pool struck out and the mixed one put back in its place, the "
              f"same request — the same eight roads still arriving apart from the same twenty-seven "
              f"instruments — has its ROAD cooling divide by "
              f"{_rp_red_rp.get('roadPoolRead')} instead of {rp['roadPoolRead']}, which is the "
              f"floor near a thirty-sixth his night run measured, against the ninth the design "
              f"claims. Nothing else about the request moved: `walkGenres` still arrives "
              f"{_rp_red_rp.get('roadLen')} entries long"
              + (f"; the planted run failed: {_rp_red.get('error')}"
                 if isinstance(_rp_red, dict) and _rp_red.get("error") else ""))

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
        #
        # WHERE THE PROOF OF THAT LIVES, AND IT IS NOT THIS ROW. `camVoiceFloor` and `camVoiceLift`
        # are pure arithmetic over a grain, a ceiling and a share, and row 8m below puts every value
        # each of those three can take through them — including that the angle actually flown clears
        # one element of the pair's finer grain, which is the law in the units the law is written in.
        # THIS row is a SMOKE reading beside it: the two functions are wired into the camera lane on
        # the right axis's ceiling and the composed output on real records agrees. It carries no
        # count and no median, because a tally over the fixture would say only that these particular
        # photographs did not break it — his 2026-08-24 word, «we don't have any confidence about the
        # coverage» — while row 8m says no photographs can.
        #
        # THE ONE THING ONLY THIS ROW CAN CATCH is the WIRING: that the floor handed to the lift is
        # taken against the ceiling of the axis that actually carries, and not against the widest of
        # the three. `camVoiceFloor` here is handed `ceiling`, the carrying axis's own, and the share
        # worn is measured against the same ceiling — so a composer that lifted pitch against roll's
        # ceiling would show pitch-carried pairs flying half the angle they owe. Row 8n plants exactly
        # that and this row is what reds.
        check(NODE_ROWS[47],
              cam["voiceChecked"] > 0 and cam["voiceUnder"] == 0,
              f"smoke, on the records that happen to be on disk: every composed pair whose flight "
              f"carries a rotational axis was measured against that axis's OWN ceiling, and none "
              f"flies under the level the pair's own grain asks for ({cam['voiceUnder']} short). The "
              f"law itself is proved over the whole span of grains, ceilings and readings in the row "
              f"below, not here. Shortfalls: "
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
        #
        # WHERE THE PROOF LIVES, AGAIN NOT HERE. `voiceLoudness` takes a measure, a period and a
        # phase, and row 8m below walks all three over their own whole spans: every value it returns
        # clears the lab's threshold at four decimal places, never passes the work's own measure, and
        # a mute happens only where the measure itself cannot carry a seen voice. THIS row is the
        # SMOKE beside it — the function is actually wired into all three instruments that publish
        # these handles, on the period and phase each of them writes. It states no count of voices,
        # because a count over the fixture would report which handles this fixture happened to drive,
        # which says nothing about the eighteen handles on a collection nobody has hung yet.
        vo = got["voices"]
        check(NODE_ROWS[48],
              vo["checked"] > 0 and vo["silentDeclared"] == 0,
              f"smoke, on the records that happen to be on disk: colour and light voices were driven "
              f"and every one of them was read back against the lab's own {vo['target255']} of 255 "
              f"at the period and phase written beside it; none is declared and unseeable "
              f"({vo['silentDeclared']} were). The law itself is proved over the whole span of "
              f"measures, periods and phases in the row below. Quietest: "
              + (json.dumps(vo["worst"], ensure_ascii=False) if vo["worst"] else "none"))

        # --- row 8m · THE ARITHMETIC, PUT THROUGH ITS OWN WHOLE SPAN -------------------------------
        # His word of 2026-08-24, on being shown counts over the fixture: «I don't know if 190 pairs
        # is enough or not, I don't know which pairs or pics did you select, it all sounds bad to me
        # as we don't have any confidence about the coverage. I know we have X effects, each effect
        # can have Y parameters, etc etc.» A count over the records on disk answers a question nobody
        # asked. The question he names — does this hold for any pictures at all — is answerable
        # exactly where the behaviour is arithmetic over numbers with known spans, and the composer's
        # camera floor, its lift and its voice loudness all are. The driver's own §6d walks each
        # argument end to end, hits every bound and every boundary value explicitly, and walks the
        # spans again at random on a pinned die; thirteen numbered claims are checked at every point,
        # including the one the fixture could never reach — that the ANGLE actually flown clears one
        # element of the pair's finer grain, in the units the law is stated in rather than in shares
        # of whichever ceiling happens to be in hand.
        pr = got["proof"]
        check(NODE_ROWS[50],
              pr["checked"] > 0 and not pr["broke"],
              f"{pr['checked']} readings put through the composer's own floor, lift and loudness "
              f"over the whole span of every argument they take — no photograph anywhere in it; "
              f"claims broken: "
              + (json.dumps(pr["broke"], ensure_ascii=False) if pr["broke"] else "none"))

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
            # RETARGETED 2026-09-01. `compose`'s old budget loop (`if (fits) break;`) is gone with
            # the shrink-one-fixed-stack shape P1.2 replaced (the comment over `bundleTierLegal`
            # above names the same move) — the tier budget is now RULE 3, an entry condition asked
            # once of a whole joint bundle rather than a loop's own exit test. The line that plays
            # its old part is the joint bundle loop's own gate on `check3` (`bundleTierLegal`'s
            # verdict): removed, a bundle whose voices overrun its role's own tier still wins the
            # bundle loop and is scored and placed, which is the same overrun the old plant produced.
            (NODE_ROWS[23],
             [["              if (!check3.ok) { row.why = check3.why; considered.push(row); continue; }",
               "              if (false) { row.why = check3.why; considered.push(row); continue; }"]],
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
            # RETARGETED 2026-08-25 (R2). The lead is decided in `scoreFor`, where the score is
            # still being built, rather than in `passageFor` after the score has been weighed — so
            # the gate now reads `scoreFor`'s own defaulted role, `step`. The plant is the same
            # plant against the same rule; only the identifier the rule is written with moved.
            # THE PLANT NOW NAMES TWO LINES, NOT ONE (2026-08-27, P1/P2 repair). `compose` used to
            # decide the arrival on a plain `locusKind !== "none"` test and this plant struck the
            # one line that read it; that line is gone, replaced by a call to `arrivalOf` (the same
            # ranking `fillPlan` already used), and the instrument-casting gate widened from
            # CONDENSED alone to CONDENSED/CRYSTALLIZED/PROPAGATED together, so the same-worded
            # condition now stands at TWO places in the file — here, gating whether `compose` casts
            # an arrival instrument at all, and in `registerOf`, gating the apparition register.
            # Only the first is what a led passage needs struck, so the plant carries the next
            # source line along as context: `source.split(from).join(to)` matches the exact text
            # including that second line, and `registerOf`'s own occurrence is followed by
            # different text (`pool.push({ name: "apparition"`), so it never matches and stands.
            # RETARGETED 2026-09-01. Gutting the whole `if (arrival === "CONDENSED" || ...)` block
            # with `if (false)` now crashes rather than reddens: `ARRIVAL_WANTS_INSTRUMENT` (the
            # CRYSTALLIZED/PROPAGATED handle-narrowing map P2 of the 2026-08-27 review added) is
            # declared INSIDE that same block and the joint bundle planner's own
            # `arrivalCandidatesFor` (added by P1.2, 2026-08-28) reads it unconditionally further
            # down the same function — so disabling the block never leaves the map assigned and the
            # read throws `TypeError: Cannot read properties of undefined`. The shape this row needs
            # — no instrument cast for the arrival — does not need the whole block struck, only its
            # own final assignment: `arrivalInstr` pinned to null undoes exactly the "three of the
            # five cast an instrument" repair the row is proving, leaves `ARRIVAL_WANTS_INSTRUMENT`
            # and everything else in the block intact, and the second plant line below is unchanged.
            (NODE_ROWS[24], [["LED_ROLES.indexOf(step) >= 0", "true"],
                             ["        arrivalInstr = arrivalRanked.length ? arrivalRanked[0].id : "
                              "null;",
                              "        arrivalInstr = null;"],
                             ["      var axis = travellingAxisOn(fromW, toW, pivot.measure, "
                              "road.axis);",
                              "      var axis = null;"]],
             lambda g: g["sweep"]["ledElsewhere"] > 0),
            # RETARGETED 2026-08-25 (R2), for the same reason: the reading is now read in
            # `scoreFor` off `plan.spec` and carried out on the return record, instead of being
            # re-read off that record after the weighing.
            (NODE_ROWS[25], [["cameraTravels && LED_ROLES", "LED_ROLES"]],
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
              ['var srcRow = sourceOf(c.instrument.id, h);',
               'var srcRow = sourceOf(c.instrument.id, h) || ["", "an open handle"];'],
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
            #
            # A FIFTH PLACE JOINED THE FOUR, 2026-09-01: P1.2's joint bundle planner (2026-08-28)
            # added RULE 1 (`bundleWorldLegal`, the `check1` gate in the outer bundle loop) as an
            # independent, final legality check on every candidate bundle — «the bundle spends the
            # crossing's one impossible event at a role shelf 17 gives no miracle» is now asked
            # there too, after the four older guards, so leaving it standing proved it alone at every
            # corner size just as the fourth once did. Added as a fifth sub-plant, same shape as the
            # other four: the gate's own `continue` struck.
            (NODE_ROWS[30],
             [["        var base = (cuts ? 0 : 2) + ((noMiracle && folds) ? 1 : 0);",
               "        var base = (cuts ? 0 : 2);"],
              ["        } else if (spendsTheMiracle(travelInstr) && !(ROLE_BUDGETS[role] || {}).miracle) {",
               "        } else if (false) {"],
              ["        pool = pool.filter(function (r) { return !r.mustFold; });", ""],
              ["        if (noMiracle && spendsTheMiracle(iid)) continue;", ""],
              ["              if (!check1.ok) { row.why = check1.why; considered.push(row); continue; }",
               "              if (false) { row.why = check1.why; considered.push(row); continue; }"]],
             lambda g: sum(g["sweep"]["folded"][r] + g["sweep"]["worldCue"][r]
                           for r in ("entrance", "quiet link", "return")) > 0),
            # ONE INSTRUMENT PER KIND, RESTORED IN A COPY — the rule an earlier lane repaired. With
            # the candidates on a kind cut back to the first of them, and the ranking's second and
            # third orders of preference removed with it, an instrument travels to every visitor and
            # can never be chosen.
            #
            # RETARGETED 2026-09-01, DOWN TO THE TWO PLANTS THE ROW'S OWN SENTENCE ABOVE ACTUALLY
            # NAMES. `tiers.length` (a first-non-empty-tier loop) and the name-fallback assignment
            # `arrivalInstr = castArrival[0]` are both gone from the file, not moved: P1.2's
            # 2026-08-31 rewrite (`castForKindsRanked`'s own comment, "EVERY TIER BELOW 8 NOW SHARES
            # ONE ROLL") replaced the tier walk with a `soft` array built by looping every tier 0..7
            # and weight-rolling across all of them together, and the 2026-08-27 P2 review struck the
            # name-fallback outright (`grep '"matter"'` over this file finds no fallback of that
            # shape left anywhere — the sequential path picks `arrivalRanked[0].id`, not a name). The
            # fourth sub-plant (`fill1`) belongs to a third mechanism entirely — the joint bundle
            # planner's own ground fill-swap candidate, P1.2, 2026-08-28 — that the row's own
            # sentence above never names and the standing row this one guards (NODE_ROWS[3], "every
            # instrument that travels to a visitor can actually be chosen") never mentions either; it
            # is dropped rather than re-targeted at speculation. What is left: cut CUTS_ON back to
            # its first entry per kind (unchanged, still the exact line), and restore "only the first
            # non-empty tier is ever rolled" by breaking the `soft`-building loop after its first hit
            # — the two defects the row's own comment names, verified together to strand several
            # instruments unchosen over the same 24-pair corner every other plant here walks.
            (NODE_ROWS[32],
             [["        if (CUTS_ON[kind].indexOf(iid) < 0) CUTS_ON[kind].push(iid);",
               "        if (!CUTS_ON[kind].length) CUTS_ON[kind].push(iid);"],
              ["        rankUnread(tiers[i]).forEach(function (p) { soft.push({ id: p.id, "
               "fit: p.fit, order: i }); });",
               "        rankUnread(tiers[i]).forEach(function (p) { soft.push({ id: p.id, "
               "fit: p.fit, order: i }); });\n        break;"]],
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
            # own target, not a downstream consequence of it.
            # AND THE DIRECTION IS THE GATE'S OWN SHAPE, not a tally. The plant replaces each reading
            # by `reading OR 0` — it can only ever ZERO a reading and never raise one — so the set of
            # pairs whose shared ground survives under the gate is a SUBSET of the set that survives
            # without it, for any collection whatever. There is no collection on which gating widens
            # that road. What a run can add to that is only whether the plant BIT here — whether at
            # least one pair of the records in hand stands below some threshold — and that is what
            # the strict «fewer» below reads. The old note in this place carried two counts over the
            # fixture as the gate's cost; they were a reading of 190 arbitrary pairs and never the
            # argument, which is above.
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
            # --- row 8n · THE CARRYING AXIS LIFTED AGAINST SOMEBODY ELSE'S CEILING ------------------
            # The defect this plant restores is the one the voice-level block shipped with on
            # 2026-08-24 and stood a day: `camFloor` was taken against `camBound` — roll's and yaw's
            # own ceiling — and then spent on whichever axis won, pitch included. Pitch's ceiling is
            # HALF of `camBound`, so a pitch-carried passage was lifted to half the angle its grain
            # asked for and the block missed its whole purpose on one axis in three.
            # WHY IT NEEDED A PLANT AND NOT ONLY THE CONSTRUCTION PROOF. Row 8m proves the arithmetic
            # for every grain, ceiling and share there is, and the arithmetic was never wrong — the
            # WIRING was: the right function was handed the wrong ceiling. A construction proof of a
            # function cannot catch a caller passing it the wrong argument, so the guard against that
            # is here, where the composer's own line is changed back and the composed output has to
            # move. Nothing about this plant reads a count: the row asks whether pairs whose flight
            # actually lands on pitch now fall under the level their own grain sets, which is the
            # defect itself and not a proportion of anything.
            (NODE_ROWS[51],
             [["camVoiceFloor(Math.min(camGrainA, camGrainB), camCap)",
               "camVoiceFloor(Math.min(camGrainA, camGrainB), camBound)"]],
             lambda g: g["camera"]["voiceUnder"] > 0),
            # THE LENGTH TAKEN OFF ONE NUMBER AGAIN. The pair's own share is dropped on its way into
            # the band and the band's floor stands in its place — which is exactly the shape the
            # defect had, one constant per role — and the two ordered pairs stop differing at every
            # one of the five roles.
            (NODE_ROWS[53],
             [["      var duration = lengthInBand(row.band, lengthShare);",
               "      var duration = lengthInBand(row.band, 0);"]],
             lambda g: all(v["one"] is not None and v["one"] == v["two"]
                           for v in g["length"]["perRole"].values())),
            # THE MIRACLE COUNTED BY AN EFFECT'S NAME AGAIN. `folds` and `foldsOn` both read
            # `=== "boxfold"` until this lane, and the file held the truer definition four screens
            # above them the whole time. Put the name back at both readings and the other three
            # world-declaring instruments go on folding the space a work lives in while being voiced
            # ordinary letters — the slot unspent, and a second impossible thing free to stand beside
            # the first.
            #
            # RETARGETED 2026-09-01. `compose`'s own `folds`/`foldsOn` locals are gone — the joint
            # bundle planner (P1.2, 2026-08-28) reads both off `bundleFoldsAndWorld`'s own returned
            # `folds`/`foldsOn` fields instead, and that function is where the `spendsTheMiracle`
            # reads this plant reverts now actually stand (`bundleFolds`/`foldsOnHere`, four screens
            # above `scoreBundle`). Same two readings, same revert, the identifiers moved with the
            # function.
            (NODE_ROWS[55],
             [["      var bundleFolds = spendsTheMiracle(g) || (!!t && spendsTheMiracle(t))\n"
               "        || (!!a && spendsTheMiracle(a));",
               '      var bundleFolds = g === "boxfold" || (!!t && t === "boxfold")\n'
               '        || (!!a && a === "boxfold");'],
              ['      var foldsOnHere = spendsTheMiracle(g) ? "pivot"\n'
               '        : ((t && spendsTheMiracle(t)) ? "travel" : ((a && spendsTheMiracle(a)) '
               '? "arrival" : null));',
               '      var foldsOnHere = g === "boxfold" ? "pivot"\n'
               '        : ((t && t === "boxfold") ? "travel" : ((a && a === "boxfold") '
               '? "arrival" : null));']],
             lambda g: sum(g["sweep"]["worldNotVoiced"].values()) > 0),
            # THE NUDGE AND THE THREE FOLLOW-UP GATES, ALL REMOVED. `castForKinds`'s one-order demote
            # is a ranking nudge and the three gates — one per cast slot — are the bound. The row
            # above proves the gates carry the law with the nudge gone; this proves they are what
            # carries it, by taking them away under the same conditions and watching a step that may
            # spend no miracle open a world.
            #
            # A FIFTH GATE JOINED THE FOUR, 2026-09-01, THE SAME ONE ROW NODE_ROWS[30] NAMES ABOVE:
            # the joint bundle planner's own RULE 1 (`check1`/`bundleWorldLegal`) refuses the same
            # bundle a fifth time, after the four sequential-cast guards this plant already struck,
            # so it needs striking too.
            (NODE_ROWS[57],
             [["        var base = (cuts ? 0 : 2) + ((noMiracle && folds) ? 1 : 0);",
               "        var base = (cuts ? 0 : 2);"],
              ["      if (!(ROLE_BUDGETS[role] || {}).miracle && !road.mustFold "
               "&& spendsTheMiracle(castPivot[0])) {",
               "      if (false) {"],
              ["        } else if (spendsTheMiracle(travelInstr) "
               "&& !(ROLE_BUDGETS[role] || {}).miracle) {",
               "        } else if (false) {"],
              ["        if (arrivalInstr !== null && spendsTheMiracle(arrivalInstr)\n"
               "            && !(ROLE_BUDGETS[role] || {}).miracle) {",
               "        if (false) {"],
              ["              if (!check1.ok) { row.why = check1.why; considered.push(row); continue; }",
               "              if (false) { row.why = check1.why; considered.push(row); continue; }"]],
             lambda g: sum(g["sweep"]["worldsCast"][r]
                           for r in ("entrance", "quiet link", "return")) > 0),
            # THE FIRST OF THE TWO ROADS TO A SECOND WORLD: the levels test at a cast. Its older
            # clause excludes a candidate only where EVERY level it declares is already claimed, so a
            # world instrument carrying a second level of its own walks straight past it and stands
            # beside a world ground. The named pair is the one that reaches for the slot that way.
            #
            # A FIFTH PLACE JOINED THE FOUR, 2026-09-01, THE SAME ONE THE OTHER TWO WORLD-CLAUSE ROWS
            # NAME ABOVE: the joint bundle planner's own RULE 1 (`check1`/`bundleWorldLegal`) refuses
            # the same bundle downstream of this older per-slot clause, so weakening the clause alone
            # no longer lets the violation reach `oneSlot`'s own reading — RULE 1 catches it first.
            # Struck alongside it, same as the other two rows.
            (NODE_ROWS[59],
             [['          if (everyLevelTaken || (worldTaken && spendsTheMiracle(iid))) {',
               "          if (everyLevelTaken) {"],
              ["              if (!check1.ok) { row.why = check1.why; considered.push(row); continue; }",
               "              if (false) { row.why = check1.why; considered.push(row); continue; }"]],
             lambda g: g["oneSlot"]["levels"]["worlds"] > 1),
            # THE SECOND ROAD TO A SECOND WORLD HAD A ROW HERE AND IT IS RETIRED, WITH ITS REASON.
            # It planted out the ground swap's own gate and read a named pair that then seated a
            # world instrument under another. That plant can no longer fire. Two things closed the
            # road ahead of it: ownership is settled in time now, and `bestFilling` gained
            # `soleAbove`, so §7's swap chooses a ground from those that leave every voice above
            # them something to say — and on this collection no pair reaches the state the plant
            # was written to expose, with the gate in place or planted out. A red-on-bug that cannot
            # go red proves the guard it was pointed at exactly as well as an empty file would, so
            # keeping it would be a row that lies about its own reach. The law it guarded is not
            # unguarded: the standing row above reads every crossing of the sweep for two
            # world-declaring instruments, and the levels test's own world clause keeps its plant,
            # which does still fire. The day a pair reaches this door again, the plant comes back.
            # THE WRITER DISPATCHING ON THE HANDLE'S NAME AGAIN. The branch that reads the
            # register's own word is switched off, so every handle whose row promises the passage's
            # own travel falls through to the static branch and holds at its manifest default for
            # the whole passage — a row promising travel and a node that never moves. `mix` is
            # untouched by the plant because it is matched by name one branch earlier, which is
            # exactly the asymmetry that hid this: the two handles the writer knew by name worked,
            # and every other one of the same kind did not.
            (NODE_ROWS[60],
             [['          if (kind === "progress") {', "          if (false) {"]],
             lambda g: bool({"parquet.spin", "unfold.field"}
                            & (set(g["sweep"]["promiseSeen"]) - set(g["sweep"]["promiseKept"])))),
            # THE HANDLES OF AN UNOWNED LEVEL LEFT ON THE TRACK LIST HAD A ROW HERE, AND IT IS
            # RETIRED 2026-08-26, WITH ITS REASON. It planted `ownedTracks(...)` out of the levels
            # row in one line — `ownTheLevels` still settling who owns what, the plan still
            # recording it, and nothing acting on the record — and read a pair whose ground and
            # arrival both cut into cells and both started cutting again.
            #
            # WHAT CLOSED THE ROAD. `castForKinds`'s own levels clause now refuses a candidate whose
            # levels are all taken by a cue it MEETS, so the plan handed to `ownedTracks` no longer
            # carries two live cues on one level and there is nothing left for the plant to expose.
            # It was reachable while the pinned pair the plant read still cast that shape; the entry
            # door's dry landing across the fleet moved what this collection casts, the pair stopped
            # casting it, and the plant went quiet rather than red. Deriving the witness instead of
            # pinning it — done above, and it is the right repair for a stale witness — did not
            # bring it back: 4 000 compositions walked in the collection's own id order at every
            # role find no pair that reaches the door, and a wider hand walk of 6 002 found none
            # either. The road is closed at the cast and not merely missed by a sample.
            #
            # A RED-ON-BUG THAT CANNOT GO RED PROVES ITS GUARD EXACTLY AS WELL AS AN EMPTY FILE
            # WOULD, and it is worse than no guard because the row above it still reads green. So it
            # goes, rather than standing as a row that lies about its own reach.
            #
            # THE LAW IT GUARDED IS NOT UNGUARDED. Three things still hold it, and all three are in
            # this file: the standing row reads every crossing of the sweep at all five roles for a
            # handle driven on a level its cue does not own and for a level driven by two cues that
            # are live together; the levels clause's OWN plant, one row up, still fires; and
            # `adriftBothWays.accompanies` is a derived witness of `ownedTracks` actually stripping a
            # level from a cue that only accompanies on it, re-found on every run.
            #
            # WHAT WOULD BRING IT BACK: a cast that once more admits two cues declaring one level
            # across windows that meet — a new instrument whose levels leave `castForKinds` no
            # alternative, or a loosening of that clause. The day the walk above finds a pair, the
            # plant belongs here again, pointed at the same line.

            # THE SEED PUT BACK ON THE DIVIDING LINE, which is where it stood until 2026-08-27 and
            # what the audit of that day found. The plant is the placement and nothing else — the
            # fit the arrival is RANKED on is untouched, so CRYSTALLIZED still wins the same pair —
            # and the row it reddens is the one that says the seed reads the work's own grain. With
            # the line back, the same record seeds at 0.82, its strongest dividing line and the most
            # ordered place it names.
            ("EX-COMPOSED red-on-bug · the seed placed back on the work's own dividing line: the "
             "point of greatest disorder is read off the most ordered place in the frame",
             [["      var seedAt = isFinite(mt.reliefCentreDetailXAt)\n"
               "        ? [r4(clamp01(mt.reliefCentreDetailXAt)), 0.5] : null;",
               "      var seedAt = (isFinite(mt.regionLineXAt) && isFinite(mt.regionLineYAt))\n"
               "        ? [r4(mt.regionLineXAt), r4(mt.regionLineYAt)] : null;"]],
             lambda g: (g["crystalSeed"]["apart"]["locus"] or [None])[0] == 0.82),
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
    "EX-COMPOSED a step declared while its wave is on the wire waits for the wave and composes",
    # 2026-08-27: the composer's own file is the other half of what a crossing needs, and it was the
    # half nothing ever waited for. The two rows below hold the wait and prove it is not vacuous.
    "EX-COMPOSED the FIRST crossing of a visit whose composer file is still on the wire waits for "
    "it and plays a composed passage",
    "EX-COMPOSED RED-ON-BUG · with the composer's own hold reverted, that same first crossing "
    "composes nothing and the visitor gets the walk's plain glide",
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
        # A STEP IS NOT FINISHED WHERE THE LAYER'S FILE ARRIVES — IT IS FINISHED WHERE THE CROSSING
        # IT DECLARED HAS LANDED (2026-08-25). The key above declares one command. Where the two
        # works it crosses both carry records — which is the deal's own coin-flip, since the walk
        # deals a fresh hand every entry and only some of the hang is recorded — that command is a
        # COMPOSED passage, and the host runs it for its whole length (five seconds on the score this
        # collection composes) with the renderer's canvas over the walk the whole time. A caller that
        # went on working while it ran aimed its click at a control the canvas was covering and the
        # walk's own scroll was still travelling to the arriving work, so the click landed on
        # nothing: that is exactly the visit the unfold row below read as a walk that never unfolded.
        # THE WAIT IS ON THE WALK COMING TO REST, and it takes two readings because either alone is
        # satisfied too early — the host carries no transaction and none awaiting (state «idle»),
        # AND the scroll has stopped moving. The scroll alone stands equally still in the moment
        # before the command is offered; the host alone goes idle a frame before the landing's own
        # scroll finishes. Two consecutive still readings clear both.
        was = None
        for _ in range(90):
            now = js(br, "return {state: (window.__exPass.host && window.__exPass.host.report)"
                         "                  ? window.__exPass.host.report().state : 'idle',"
                         "        y: Math.round(window.scrollY)};")
            if (now["state"] == "idle" and was is not None
                    and was["state"] == "idle" and was["y"] == now["y"]):
                break
            was = now
            br.sleep(0.2)
        br.sleep(0.4)


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def frame_gone(br, tries=25):
    """Let the animation frame a walk's own step was declared in END before another step is taken.

    PASS-API §1.1 gives `declare` a same-frame lock: two declares inside one animation frame make
    the second a refusal («second declare in one frame»), and the lock is released on the
    `requestAnimationFrame` the first declare schedules. A keystroke IS a declare, and the polls a
    row puts after one can every one of them return on their first read — `js()` costs no frame and
    a loop that breaks at once costs no sleep — so a row's SECOND keystroke can land inside the
    first one's frame and be refused for racing the walk rather than for anything the row measures.
    Read live off the refusal ring 2026-09-01, on the wave-and-wire row below: the row's own step
    never reached the wire at all and its «the step did not hold» read was that refusal wearing the
    law's clothes. Waiting for a frame to pass is the exact fact the lock is keyed on, so nothing
    here is a guessed delay; the same repair `tests/test_pass_weave.py` took for the same class."""
    br.evaluate("window.__frameGone = false;"
                "requestAnimationFrame(function () { window.__frameGone = true; }); 0")
    for _ in range(tries):
        if br.evaluate("String(!!window.__frameGone)") == "true":
            return True
        br.sleep(0.1)
    return False


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
FAIL_WAVE = {"on": False}    # held on by the "wave that never lands" row; every GET answers 500
# HOW THE LAST ROW DELAYS A WAVE, AND WHY IT IS A GATE RATHER THAN A SLEEP. The row below asks what a
# step does while its records are STILL ON THE WIRE, so the wire has to be held open for exactly as
# long as the row needs and not one beat longer or shorter. A sleep of N seconds would make the row a
# race against its own driving (the door's ceremony, the layer's file, two keystrokes), and a race is
# what the wave-fails row above already had to be rewritten out of. So the hook waits on a
# `threading.Event` instead: while it is unset every `/api/pass/records` GET hangs unanswered, and the
# row opens it at the exact instant it has finished asserting what a held step looks like. The
# harness serves on a ThreadingHTTPServer (tests/headless_harness.py), so a held GET blocks its own
# connection and nothing else the page is loading.
WAVE_GATE = {"ev": None}
# HOW THE COMPOSER'S OWN FILE IS HELD ON THE WIRE, and why it is held the same way a wave is. The
# two rows about the first crossing of a cold visit (2026-08-27) ask what a step does while
# `pass-composer.js` is still travelling — the window every real visitor's first gesture lands in,
# since that file is the heaviest of the three the door's pick asks for and therefore the last to
# arrive. `serve(hold=...)` cannot express it: the delay it takes is fixed when the server is built,
# and these rows have to open the wire at the exact instant they have finished reading what a held
# step looks like. So the hook below waits on this `threading.Event` for any request naming that
# file and then falls through to the ordinary file serving, exactly as `WAVE_GATE` does for a wave.
COMPOSER_GATE = {"ev": None}


def records_answer(raw_path):
    # THE COMPOSER'S FILE IS SERVED FROM DISK AS ALWAYS — only later. Returning None hands the
    # request back to the harness's ordinary file road (tests/headless_harness.py's `serve`), so
    # what the browser finally receives is the real built artifact and nothing about the file
    # itself is faked; the only thing this hook owns is WHEN it starts arriving.
    if "pass-composer.js" in raw_path:
        gate = COMPOSER_GATE["ev"]
        if gate is not None:
            gate.wait(90)     # bounded so a row that dies without opening it cannot wedge the server
        return None
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
    gate = WAVE_GATE["ev"]
    if gate is not None:
        gate.wait(90)     # bounded so a row that dies without opening it cannot wedge the server
    if FAIL_WAVE["on"]:
        # HELD ON WHILE THE ROW STANDS, RATHER THAN FIRED ONCE (2026-08-25). A wave the route refuses
        # is RETRIED with backoff — engine/client/01a-pass.js's own `.catch()` takes every id of the
        # failed wave back off `passRecordsAsked` and puts it on the wire again 1.5 s later, up to
        # three tries. A hook that refused only the FIRST GET therefore let the SECOND one land, and
        # the row named after a wave that never lands was really racing that backoff: where the
        # refusal took longer than 1.5 s to reach the diagnostic surface the row polls, the crossing
        # it then declared found its two records after all and froze a whole score. Refusing every
        # wave while the gate is on IS the row's own precondition — the route is down, not down for
        # one request — and the row turns the gate off again when it is finished with it.
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
                #
                # WHICH TWO, AND WHY NOT SIMPLY THE FIRST TWO RECORDED (2026-08-25). The one step
                # `enter(..., step=True)` takes crosses the first two works of a hang the walk deals
                # afresh every entry, and whether the record set happens to cover both of them is
                # that deal's own coin-flip. Where it does, the step's crossing composes and LANDS,
                # and from the landing on the edge it crossed carries §4.8's own record — which is
                # also, by the same coincidence, the very edge «the first two recorded works» names.
                # A row declaring over it then reads a request carrying a return reference where it
                # means to read a first crossing's nothing, and the diagnostic-surface row below
                # reddened on exactly that. So the pair is chosen against the walk's own edge
                # register, read off the diagnostic surface at this instant — the first two recorded
                # works of this hang whose edge this visit has NOT already walked. The rows below ask
                # for nothing weaker than before; the precondition they were always written against
                # is made true here instead of left to the deal.
                walked = set(js(br, "return window.__exPass.report().memory.edges"
                                    ".map(function(e){return e.edgeKey;});"))
                cand = [w for w in shown if w in recorded]
                pair = next(([a, b] for i, a in enumerate(cand) for b in cand[i + 1:]
                             if "__".join(sorted([a, b])) not in walked), [])
                if len(pair) < 2:
                    for r_ in BROWSER_ROWS[2:8]:
                        skip(r_, f"this hang shows no two recorded works on an edge this visit has "
                                 f"not already walked: recorded {cand[:4]}, walked {sorted(walked)}")
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

                # 11 · EX-PASS-RECORDS: a wave that never lands. FAIL_WAVE holds the harness's
                # `answer` hook (records_answer, above) at 500 for every `/api/pass/records` GET this
                # visit makes — real requests the client's own fetch really receives and really has to
                # handle, the same road `passRecordsAskFor`'s own `.catch()` was written for (its
                # comment: "the wave for N id(s) did not land"). A fresh visit's very first wave is
                # the door's own spread, so turning the gate on just before a fresh `enter()`
                # sabotages that request and every retry the client makes of it — which is what the
                # row's own name says and what the client's 1.5 s backoff means it has to say (the
                # note on the hook itself). What the row asks: the refusal is said in plain words,
                # the visitor still lands, and a crossing over the still-unrecorded pair freezes no
                # score onto the command — the walk's own glide, not a thrown error breaking the
                # visit.
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
                FAIL_WAVE["on"] = False   # the route stands again

                # 13 · EX-PASS-RECORDS: a step declared while its own wave is still on the wire
                #
                # THE DEFECT THIS ROW HOLDS. The door picks the hand and asks the route for its ids
                # in the same beat, so the records of the works a first step crosses are ALREADY on
                # the wire when that step is declared. Until 2026-08-25 the step read «no record» —
                # which is true of the map at that instant and false about the visit — and took the
                # walk's plain glide, so a visitor whose wire was slow paid for the latency with the
                # whole passage. The step now waits for its own wave and composes when it lands.
                #
                # HOW THE WAVE IS DELAYED, IN ONE SENTENCE: `WAVE_GATE` above holds every
                # `/api/pass/records` GET unanswered until this row opens it, so the wire is open for
                # exactly the window the row drives and the row is not racing anything.
                #
                # WHY TWO KEYSTROKES. The picture layer's own file is fetched at the FIRST step of a
                # visit (engine/client/15-motion.js: `passOpen()` runs where a step declares), so at
                # that first step no layer is registered and the walk glides by its own standing law —
                # the layer's own 350 ms hold, which this row does not touch. The SECOND step is the
                # first one declared with a layer registered, and it is the step this row is about.
                # Both are taken with the gate shut, so the wave is on the wire for both.
                # EVERY WORK OF THE CATALOGUE IS GIVEN A RECORD, not only the ten `allworks` names:
                # the walk deals a fresh hand on every entry, so a record set built from the hang the
                # rows above read leaves most of the NEXT hang unrecorded and the step this row is
                # about would find no record however long it waited. Read off the bake's own data
                # file, the same way tests/test_pass_route.py does.
                every = put_records(TMP, [w["id"] for w in json.loads(
                    (TMP / "exhibition_data.json").read_text(encoding="utf-8"))["works"]])
                gate = threading.Event()
                WAVE_GATE["ev"] = gate
                with Browser(width=1280, height=900) as br4:
                    try:
                        enter(br4, base, "diagnostics:on")
                        # AMENDED 2026-08-27, and the amendment is what the composer's own hold
                        # cost this row. The warm-up step below used to reach nothing that could
                        # wait: the composer was still on the wire, `passRecordsHold` bails without
                        # one in hand, and the step simply glided. It HOLDS now — first on the
                        # composer's file, then, once that lands, on this row's own shut wave — so
                        # `records.holds` already stands at one by the time the baseline below is
                        # read. Nothing about what this row measures changed; what changed is that
                        # the delta has to be waited FOR rather than read the instant after the
                        # keystroke, and the poll at the foot of the row does exactly that.
                        br4.key("ArrowDown")           # opens the layer's file; holds or glides
                        for _ in range(50):
                            if js(br4, "return !!(window.__exPass && window.__exPass.layer());") is True:
                                break
                            br4.sleep(0.2)
                        for _ in range(50):
                            if js(br4, "return window.__exPass.report().composer.state;") == "read":
                                break
                            br4.sleep(0.2)
                        before = js(br4, "var r = window.__exPass.report();"
                                         "return {coming: r.records.coming, held: r.records.held,"
                                         " state: r.composer.state, holds: r.records.holds,"
                                         " layer: !!window.__exPass.layer(),"
                                         " passages: window.__exPass.passages().length};")
                        # …AND THE WARM-UP STEP'S OWN FRAME IS LET GO OF FIRST (2026-09-01). Both
                        # polls above break on their first read whenever the layer and the composer
                        # are already in hand, and `js()` costs no frame — so the keystroke below
                        # could land inside the warm-up step's own animation frame and be refused by
                        # `declare`'s same-frame lock («second declare in one frame», read live off
                        # the refusal ring). The row then measured a step that was never declared and
                        # called it a step that did not hold. See `frame_gone` for the lock itself.
                        frame_gone(br4)
                        br4.key("ArrowDown")           # THE STEP: declared with its records in flight
                        held = {}
                        for _ in range(20):
                            held = js(br4, "var r = window.__exPass.report();"
                                           "return {holds: r.records.holds,"
                                           " waiting: r.records.waiting,"
                                           " coming: r.records.coming,"
                                           " passages: window.__exPass.passages().length};")
                            # THE ROW'S OWN STEP, never merely «some step held». A truthy count is
                            # satisfied by the warm-up step's hold above, which was declared before
                            # this row's keystroke and says nothing about it; the DELTA is the only
                            # reading that belongs to the step this row took.
                            if held["holds"] > before["holds"]:
                                break
                            br4.sleep(0.2)
                    finally:
                        WAVE_GATE["ev"] = None
                        gate.set()                     # the wave lands from here
                    after = {}
                    for _ in range(80):
                        after = js(br4, "var rows = window.__exPass.passages();"
                                        "var r = window.__exPass.report();"
                                        "return {coming: r.records.coming, held: r.records.held,"
                                        " holds: r.records.holds, waiting: r.records.waiting,"
                                        " passages: rows.length,"
                                        " scored: rows.filter(function(x){return !!x.score;}).length,"
                                        " keys: rows.map(function(x){return x.key;})};")
                        if after["scored"]:
                            break
                        br4.sleep(0.25)
                    if not (before["layer"] and before["state"] == "read"):
                        skip(BROWSER_ROWS[13],
                             f"the second step could not be taken with a layer and a composer both "
                             f"standing: {before}")
                    elif not before["coming"]:
                        skip(BROWSER_ROWS[13],
                             f"the wave was not on the wire when the step was declared: {before}")
                    else:
                        check(BROWSER_ROWS[13],
                              before["held"] == 0 and before["passages"] == 0
                              and held["holds"] > before["holds"] and held["waiting"] >= 1
                              and held["passages"] == 0
                              and after["held"] > 0 and after["scored"] >= 1,
                              f"{before['coming']} id(s) were still on the wire and {before['held']} "
                              f"record(s) held when the step was declared; the step held "
                              f"({before['holds']} → {held['holds']} holds, {held['waiting']} "
                              f"waiting) and composed nothing while it waited "
                              f"({held['passages']} passage(s)); the gate then opened, the walk "
                              f"came to hold {after['held']} record(s) and derived "
                              f"{after['scored']} scored passage(s) of {after['passages']} — "
                              f"{after['keys'][:2]} over {len(every)} recorded works")

                # 14 / 15 · THE FIRST CROSSING OF A COLD VISIT (2026-08-27)
                #
                # THE DEFECT THESE TWO ROWS HOLD, and why it outlived the fixes before it. A crossing needs
                # three files, and the door's pick asks for all three in one beat: the drawing
                # layer, the record wave and the composer. Two of them had a wait — the layer's own
                # bounded one since 2026-08-24, the wave's since 2026-08-25 — and the composer, the
                # heaviest of the three by a wide margin and therefore the LAST to land, had none at
                # all. `passComposeFor` answered null the instant it found no composer, the command
                # froze with no score, and the visitor's FIRST gesture played the walk's plain glide
                # while every gesture after it played a composed passage. Worse, `passRecordsHold`
                # bails at `!passComposer`, so the one wait that could have covered the window was
                # switched off precisely while the window stood open.
                #
                # WHY THE FIRST GESTURE AND NOT A RARE RACE. The window is the composer file's own
                # travel time, and the visitor's first gesture is the only one that can land inside
                # it. That is not a probability this row shifts: with the wait in place the first
                # crossing composes however long the file takes, and that is what row 14 measures.
                #
                # WHAT THE RED ROW REVERTS, AND WHAT IT DOES NOT. Row 15 runs the SAME drive against
                # a copy of the built artifact with one line of `passOffer` removed — the composer
                # hold's own dispatch, which restores that function byte-for-byte to what it was
                # before this fix. The source tree is never written to and git is never touched (the
                # convention tests/test_pass.py's own red row and tests/test_pass_coverage.py's
                # `red_pack` both document). A row that only asserted the green half would pass just
                # as well on a visit whose composer happened to arrive early, which is exactly how
                # this bug has been closed before without being fixed.

                def first_crossing(served_base):
                    """A genuinely fresh visit whose composer file is held on the wire until this
                    drive has read what its first crossing did. Returns the three readings the two
                    rows compare: the walk as the step was declared, the walk while the step was
                    held, and the walk once the file had landed."""
                    gate = threading.Event()
                    COMPOSER_GATE["ev"] = gate
                    seen = {"before": None, "held": None, "after": None, "marks": []}
                    READ = ("var r = window.__exPass.report();"
                            "var rows = window.__exPass.passages();"
                            "return {layer: !!window.__exPass.layer(),"
                            " composer: r.composer.state, holds: r.composer.holds,"
                            " waiting: r.composer.waiting,"
                            " coming: r.records.coming, held: r.records.held,"
                            " passages: rows.length,"
                            " scored: rows.filter(function(x){return !!x.score;}).length,"
                            " keys: rows.map(function(x){return x.key;})};")
                    try:
                        with Browser(width=1280, height=900) as brc:
                            try:
                                enter(brc, served_base, "diagnostics:on")
                                # THE PRECONDITION, MEASURED RATHER THAN ASSUMED: the layer has
                                # registered and the wave has landed, so neither of them can be what
                                # this step waits on — and the composer alone is still «asked».
                                st = {}
                                for _ in range(60):
                                    st = js(brc, READ)
                                    if (st["layer"] and st["composer"] == "asked"
                                            and st["held"] > 0 and not st["coming"]):
                                        break
                                    brc.sleep(0.2)
                                seen["before"] = st
                                if not (st["layer"] and st["composer"] == "asked"
                                        and st["held"] > 0 and not st["coming"]):
                                    return seen
                                brc.key("ArrowDown")     # THE FIRST CROSSING OF THE VISIT
                                held = st
                                for _ in range(15):
                                    held = js(brc, READ)
                                    if held["holds"] or held["scored"]:
                                        break
                                    brc.sleep(0.2)
                                seen["held"] = held
                            finally:
                                COMPOSER_GATE["ev"] = None
                                gate.set()               # the composer's file lands from here
                            after = seen["held"] or seen["before"]
                            for _ in range(80):
                                after = js(brc, READ)
                                if after["scored"]:
                                    break
                                brc.sleep(0.25)
                            seen["after"] = after
                            seen["marks"] = js(
                                brc, "return window.__exPass.report().events"
                                     ".filter(function(e){return e.name === 'composer-hold';})"
                                     ".map(function(e){return e.why;});")
                    finally:
                        COMPOSER_GATE["ev"] = None
                        gate.set()
                    return seen

                import shutil as _shutil     # the bottom-of-file import comes too late for this row
                now = first_crossing(base)

                HURT_JS = JS.replace(
                    "  function passOffer(cmd) {\n"
                    "    if (passComposerHold(cmd)) return true;\n"
                    "    if (passRecordsHold(cmd)) return true;\n",
                    "  function passOffer(cmd) {\n"
                    "    if (passRecordsHold(cmd)) return true;\n",
                    1,
                )
                reverted = HURT_JS != JS
                hurt = None
                if reverted:
                    HURT_DIR = Path(tempfile.mkdtemp(prefix="synth_composed_hurt_"))
                    _shutil.copytree(TMP, HURT_DIR, dirs_exist_ok=True)
                    (HURT_DIR / "exhibition.js").write_text(HURT_JS, encoding="utf-8")
                    with serve(HURT_DIR, answer=records_answer) as base_hurt:
                        hurt = first_crossing(base_hurt)
                    _shutil.rmtree(HURT_DIR, ignore_errors=True)

                if not (now["before"] and now["held"]):
                    skip(BROWSER_ROWS[14],
                         f"the first crossing could not be taken with the layer standing, the wave "
                         f"landed and the composer still on the wire: {now['before']}")
                    skip(BROWSER_ROWS[15], "row 14 never reached its own precondition")
                else:
                    check(BROWSER_ROWS[14],
                          now["before"]["composer"] == "asked"
                          and now["before"]["scored"] == 0
                          and now["held"]["holds"] >= 1 and now["held"]["waiting"] >= 1
                          and now["held"]["scored"] == 0
                          and now["after"]["composer"] == "read"
                          and now["after"]["scored"] >= 1,
                          f"with the composer still on the wire ({now['before']['composer']}), the "
                          f"layer standing and {now['before']['held']} record(s) already held, the "
                          f"first crossing held ({now['held']['holds']} hold(s), "
                          f"{now['held']['waiting']} waiting, marked {now['marks'][:1]}) and "
                          f"composed nothing while it waited ({now['held']['scored']} scored); the "
                          f"file then landed and that same crossing derived "
                          f"{now['after']['scored']} scored passage(s) — {now['after']['keys'][:1]}")

                    if not reverted:
                        skip(BROWSER_ROWS[15],
                             "the composer hold's own dispatch line was not found in the served "
                             "client, so there was nothing to revert")
                    elif not (hurt and hurt["before"] and hurt["held"]):
                        skip(BROWSER_ROWS[15],
                             f"the reverted copy never reached the same precondition: "
                             f"{hurt['before'] if hurt else None}")
                    else:
                        check(BROWSER_ROWS[15],
                              hurt["held"]["holds"] == 0 and hurt["held"]["scored"] == 0
                              and hurt["after"]["scored"] == 0
                              and now["after"]["scored"] >= 1,
                              f"reverted to the pre-fix `passOffer`, the same drive held the step "
                              f"{hurt['held']['holds']} time(s) and its first crossing ended with "
                              f"{hurt['after']['scored']} scored passage(s) even after the composer "
                              f"landed ({hurt['after']['composer']}); with the hold in place the "
                              f"same crossing ended with {now['after']['scored']}")


# ================================================================================================
# REAL-DATA CAMERA HANDOFF (V2-CONVERGENCE-PLAN-2026-08-31 Phase 4, item 3). The inventory this
# phase's brief carries found the composer's own `cameraAuthority` field — P3's declared-surface
# capability, comment above `pass-composer.js:4187-4191` — never once read by this file: a `grep
# cameraAuthority tests/test_pass_composed.py` before this section landed matched nothing. What the
# field states is a HANDOFF — camera control passes from the stage's own track to the one cast cue
# whose instrument declares its own surface pose (`boxfold` is the one shipped carrier today), and
# back — and no test anywhere in this file asked a real composed plan whether that handoff actually
# happened. This searches the real 121-work fleet (never a hand-picked pair) for a real winning
# plan that casts an own-authority instrument, and proves two things a silent regression could break
# without any other row here noticing: the cast own-authority cue is actually marked `"own"`, and
# every other cue sharing that same real plan is left `"stage"` — one authority handed to one voice,
# never asserted, never assumed.
_HANDOFF_ROW = ("EX-COMPOSED real-data camera handoff · a real composed plan hands "
                "cameraAuthority to its one own-authority instrument and leaves every other cue "
                "stage-held")
_HANDOFF_RED_ROW = ("EX-COMPOSED real-data camera handoff red-on-bug · collapsing the declared-"
                     "surface read to always stage silently erases that same real handoff")
_HANDOFF_DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, worksPath] = process.argv.slice(2);
const plants = JSON.parse(process.env.HANDOFF_PLANTS || "[]");
let source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
const missed = [];
for (const [from, to] of plants) {
  if (source.indexOf(from) < 0) { missed.push(from); continue; }
  source = source.split(from).join(to);
}
if (missed.length) { console.log(JSON.stringify({missed: missed})); process.exit(0); }
let joined = null;
const sandbox = { window: { __PassComposer: (m) => { joined = m; } }, console: console };
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: "pass-composer.js" });
const consts = JSON.parse(fs.readFileSync(process.env.HANDOFF_FIXTURE, "utf8")).consts;
const composer = joined.make(consts);
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const ids = Object.keys(works);
// Own-authority instruments declare it on their own manifest (P3's own reading) — never a name
// typed here; a future carrier joins this search automatically.
const ownIds = Object.keys(consts.manifests).filter((iid) =>
  ((consts.manifests[iid].surface || {}).cameraAuthority) === "own");

function cast(from, to, seed, role, fn) {
  const req = { workRecordA: works[from], workRecordB: works[to], direction: "a-to-b",
               seed: seed, routeRole: role, routeFunction: fn, cameraState: null,
               walkMemory: [], walkGenres: [], walkMiracles: [], framePace: null };
  let made;
  try { made = composer.passageFor(req); } catch (e) { return null; }
  if (!made || made.declined || !made.plan) return null;
  return made.plan.cues || [];
}

// REPLAY: the green run's own found (from, to, seed, role, fn), handed back in rather than
// re-searched — the plant below touches only the field's own value, never which pair or bundle
// wins, so re-composing the SAME real request is the direct proof and an exhaustive re-search
// under a plant that (by construction) can never again satisfy the search's own stopping
// condition would otherwise never terminate inside this fleet's own 121*120*6*2 request space.
const replay = process.env.HANDOFF_REPLAY ? JSON.parse(process.env.HANDOFF_REPLAY) : null;
if (replay) {
  const cues = cast(replay.from, replay.to, replay.seed, replay.role, replay.fn);
  console.log(JSON.stringify({
    replayed: cues ? cues.map((c) => ({ id: c.id, instrument: c.instrument.id,
                                        cameraAuthority: c.cameraAuthority })) : null,
    ownIds: ownIds,
  }));
} else {
  const ROLE_FN = [["entrance", "subdominant"], ["quiet link", "tonic"], ["middle", "subdominant"],
                   ["middle", "dominant"], ["culmination", "dominant"], ["return", "tonic"]];
  const SEEDS = [0, 3];
  let found = null;
  outer:
  for (let i = 0; i < ids.length && !found; i++) {
    for (let j = 0; j < ids.length && !found; j++) {
      if (i === j) continue;
      const from = ids[i], to = ids[j];
      for (const [role, fn] of ROLE_FN) {
        for (const seed of SEEDS) {
          const cues = cast(from, to, seed, role, fn);
          if (!cues) continue;
          const ownCue = cues.filter((c) => ownIds.indexOf(c.instrument.id) >= 0
                                            && c.cameraAuthority === "own")[0];
          if (!ownCue) continue;
          found = { from: from, to: to, seed: seed, role: role, fn: fn,
                    cues: cues.map((c) => ({ id: c.id, instrument: c.instrument.id,
                                             cameraAuthority: c.cameraAuthority })) };
          break outer;
        }
      }
    }
  }
  console.log(JSON.stringify({ found: found, ownIds: ownIds }));
}
"""

def _handoff_node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def _handoff_run(plants=None, replay=None):
    handoff_dir = Path(tempfile.mkdtemp(prefix="pass_composed_handoff_"))
    driver_path = handoff_dir / "handoff-driver.js"
    driver_path.write_text(_HANDOFF_DRIVER, encoding="utf-8")
    env = dict(os.environ, HANDOFF_PLANTS=json.dumps(list(plants or [])),
              HANDOFF_FIXTURE=str(FIXTURE))
    if replay is not None:
        env["HANDOFF_REPLAY"] = json.dumps(replay)
    proc = subprocess.run(["node", str(driver_path), str(MODULE), str(WORKS)],
                          capture_output=True, text=True, env=env, timeout=180)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1200:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the handoff driver said nothing"}
    return json.loads(lines[-1])


if not _handoff_node_available():
    skip(_HANDOFF_ROW, "node is not on this machine")
    skip(_HANDOFF_RED_ROW, "node is not on this machine")
elif not (MODULE.exists() and FIXTURE.exists() and WORKS.exists()):
    skip(_HANDOFF_ROW, "the composer or its fixtures are not on this machine")
    skip(_HANDOFF_RED_ROW, "no real pair to replant")
else:
    _handoff_green = _handoff_run()
    _handoff_found = (_handoff_green.get("found")
                      if isinstance(_handoff_green, dict) else None)
    _own_ids = _handoff_green.get("ownIds") if isinstance(_handoff_green, dict) else None
    if isinstance(_handoff_found, dict):
        _others_stage = all(c["cameraAuthority"] == "stage" for c in _handoff_found["cues"]
                            if c["instrument"] not in (_own_ids or []))
        _owner_cue = [c for c in _handoff_found["cues"] if c["cameraAuthority"] == "own"]
    else:
        _others_stage = False
        _owner_cue = []
    check(_HANDOFF_ROW,
          isinstance(_handoff_found, dict) and len(_owner_cue) == 1 and _others_stage,
          ("real pair %s→%s (seed %s, role %s/%s): the planner's own real winning plan casts %s, "
           "cameraAuthority %s"
           % (_handoff_found["from"], _handoff_found["to"], _handoff_found["seed"],
              _handoff_found["role"], _handoff_found["fn"],
              [c["instrument"] for c in _handoff_found["cues"]],
              {c["id"]: c["cameraAuthority"] for c in _handoff_found["cues"]}))
          if isinstance(_handoff_found, dict) else
          ("the real 121-work fleet's own search cast no own-authority instrument (%s) on any "
           "real pair at all" % (_own_ids,)))

    if not isinstance(_handoff_found, dict):
        skip(_HANDOFF_RED_ROW, "no real pair found above to replant")
    else:
        _handoff_plant = [['? "own" : "stage",', '? "stage" : "stage",']]
        _handoff_replay = {"from": _handoff_found["from"], "to": _handoff_found["to"],
                           "seed": _handoff_found["seed"], "role": _handoff_found["role"],
                           "fn": _handoff_found["fn"]}
        _handoff_red = _handoff_run(plants=_handoff_plant, replay=_handoff_replay)
        if _handoff_red.get("missed"):
            skip(_HANDOFF_RED_ROW, "the line this plant names is not in the shipped source")
        else:
            _replayed = (_handoff_red.get("replayed")
                        if isinstance(_handoff_red, dict) else None)
            _replayed_owns = ([c for c in _replayed if c["cameraAuthority"] == "own"]
                              if isinstance(_replayed, list) else None)
            check(_HANDOFF_RED_ROW,
                  isinstance(_replayed, list) and not _replayed_owns,
                  ("re-composing the exact same real request under the plant reads %s — the "
                   "handoff this row's green above proved is now silently gone"
                   % json.dumps(_replayed))
                  if isinstance(_replayed, list) else
                  "re-composing the exact same real request under the plant produced no plan at "
                  "all: " + json.dumps(_handoff_red))

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
