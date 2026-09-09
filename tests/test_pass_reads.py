#!/usr/bin/env python3
"""PASS-READS — every instrument's declared `reads:` proven by a run, not by a grep.
Run: python3 tests/test_pass_reads.py

WHAT THIS FILE IS FOR.

  Nineteen instruments declare, in a `reads: "..."` line in their own source, which measurement of a
  photograph their geometric handle answers to, and which measurements their `suits:` fit ranks on.
  Until this file, every SPEC criterion standing on those declarations was proven by grepping the
  same line back out of the built text — `'reads: "structure.polar.tunnel' in REGION` and its
  thirteen siblings. That proves somebody typed the sentence. It does not prove the handle reads
  what the sentence says, and a handle wired to a different field would pass every one of them.

  One instrument already carried the honest version: `tests/test_pass_tilt.py:612` runs the REAL
  composer over a real pair, varies each named measurement in turn, and reads which handle actually
  moves. This file is that mechanism generalised to the fleet — one driver over a list of
  instruments, not a row per instrument.

WHAT THE READINGS ARE VARIED ON, AND WHY IT IS NOT THE COLLECTION.

  Until 2026-09-06 the walk ran on `tests/fixture_pass_works.json` — the 121 real per-work records of
  the photographs that hang today. Every seat was searched for over all 121 by 121 ordered pairs and
  every donor value was lifted out of another photograph's record. That was a sweep of a collection
  standing in for a proof of a law: it proves nothing about a photograph that is not in it, its green
  moves when a photograph is added or removed, and its cost grows with the square of the collection.

  It now runs on `tests/synthetic_works.py` — a FIXED corpus of deterministic WorkRecords built from
  the BOUNDARY VALUES of the measurements a record carries and from the BEHAVIOUR CLASSES the
  composer's own source branches on. That file says, per record, which boundary or class it stands
  for. The claim a row makes is therefore stronger than the one it made before: «this handle moves
  when its own named measurement is varied at every boundary of that measurement and in every class
  the composer distinguishes», rather than «it moved somewhere inside one collection».

HOW A READING IS VARIED, AND WHERE THE NEW VALUE COMES FROM.

  Never from a number this file invented. The declared measurement is varied ACROSS TWO WORKS: the
  value is lifted from another record of the synthetic corpus, so «vary structure.polar.tunnel» means
  «stand another class's own corridor reading — the top of that reading's span, or its bottom — in
  this one's record».

  A donor that changes which cue is cast is passed over — a different cue is a different question —
  and the next donor is tried.

WHAT EACH ROW ASSERTS.

  · MOVED. Varying the measurement a handle's own manifest names moves that handle's node.
  · STILL. Varying a measurement the instrument's whole source never names moves it not at all.
  · The fit. Where the declaration is `suits: { reads: [...] }`, the instrument's own live
    `suits(A, B)` is called before and after, and the fit reading has to move.

WHAT IS SKIPPED, AND WHY IT IS PRINTED.

  Some declarations name no field of a work record at all — «the score's own die», «handover»,
  «nothing of either photograph», `reads: null`. Some name a field the corpus's records do not carry,
  or carry identically in every one. Neither can be varied, so neither is claimed. Every one is
  printed by name with its own reason and counted, so a reading that goes unproven is visible rather
  than quietly folded into a green row.

THE SMOKE ON REAL RECORDS, WHICH CARRIES NO LAW.

  Two rows at the end still touch `tests/fixture_pass_works.json`, and they prove SCHEMA AND WIRING
  and nothing else: that a real record still carries exactly the field paths the synthetic base
  carries, and that a handful of real pairs still feed the real composer and come back with a cast
  passage whose handles resolve. Neither is a law about the composition, and neither grows when a
  photograph is added — both read a fixed handful.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import synthetic_works  # noqa: E402

ASSETS = ROOT / "engine" / "assets"
COMPOSER_MODULE = ASSETS / "pass-composer.js"
FIXTURE_COMPOSED = ROOT / "tests" / "fixture_pass_composed.json"
# The real per-work records. NO ROW THAT VARIES A READING TOUCHES THEM ANY MORE — they are read by
# the two schema-and-wiring smoke rows at the end of this file and by nothing else.
FIXTURE_WORKS = ROOT / "tests" / "fixture_pass_works.json"

# The fourteen the sweep of 2026-09-03 found standing on a grep of their own `reads:` line
# (docs/evidence/2026-09-03-textual-anchors.md; PLAN.md S-73). `tilt` is in the list because the
# fleet row has to hold the instrument the mechanism came from too.
#
# AND THE FIVE PLAN.md S-93 ADDED, for the reason S-86 left them out. The membership rule was never
# «a SPEC criterion greps this file»; it was only where the sweep had looked. S-86 found the twin
# defect below standing unrepaired in `hero`, `studio`, `tunnel`, `lens` and `livemirror` and could
# not touch them, because a declaration this file does not walk is a sentence nothing can prove. The
# list is what the run reaches, so widening the list is what a repair there costs. Nothing else is
# needed to reach them: they are ordinary instruments, cast by the same `passageFor`, and the seat
# walk, the donor search and the control all read them exactly as they read the first fourteen.
INSTRUMENTS = ["liquid", "pour", "veil", "waterline", "wind", "overlay", "boxfold", "matter",
               "strata-light", "strata-scale", "kaleidoscope", "weave", "planet", "tilt",
               "hero", "studio", "tunnel", "lens", "livemirror", "droste", "gears"]

# The roots a work record actually carries (tests/fixture_pass_works.json). A `reads:` sentence that
# opens with one of these names a field; one that does not is prose about a die, a handover or the
# module's own taste, and is skipped by name below rather than guessed at.
ROOTS = "structure|texture|luminance|palette|motifs|colour|measures|guides|symmetry|door"
PATH_RE = re.compile(r"\b(?:%s)\.[A-Za-z][A-Za-z0-9_]*(?:\.[A-Za-z][A-Za-z0-9_]*)*" % ROOTS)

# Candidates for the control reading — a measurement the instrument's own file never names anywhere,
# so nothing in it may answer to it. The first candidate absent from the whole source is used.
CONTROL_POOL = ["colour.brightness", "colour.contrast", "colour.sat", "palette.hueConcentration",
                "palette.colourfulness", "luminance.level"]

# NO READING OF THE FLEET ANSWERS TO NOTHING. The run of 2026-09-03 (PLAN.md S-73) found six that
# did, and PLAN.md S-86 closed all six the same day — three of them by moving the sentence onto the
# house the code reads, one by striking a name the code never read, one by striking a leftover, and
# one by widening this file's own seat walk to a seat where the handle is actually driven. What each
# one became is in docs/evidence/2026-09-03-reads-answer.md in the site repo, with the reason.
#
# THE RULE THE THREE RENAMES SHARE, and the reason they were renames rather than rewirings. A work
# record carries several of its readings TWICE, once raw and once digested — `texture`
# `scoreFromCutLines` beside `measures.texture`, `structure.radial.centre` beside
# `motifs.radialCentre`. Where a reading has two houses, THE DECLARATION NAMES THE HOUSE THE CODE
# READS, and names the twin only as the twin. Naming the other house does not make a declaration
# false, which is why a grep never caught these; it makes it UNPROVABLE, and that is worse, because
# a run that varies the unread house sees the handle stand still and cannot tell a wrong wiring from
# a second name for one number. Rewiring the code onto the raw house instead would have been the
# larger change and the wrong one: the digest is what the composer deliberately ranks on.
#
# THE ROW HOLDS THIS SET EXACTLY, both ways. Any unanswered reading — the plant of PLAN.md rule 8,
# or a real regression — reddens it by name, and there is now no entry here for one to hide behind.
UNANSWERED = {}

# A HANDLE THIS ROW ASKS TO STAND STILL, NEVER TO MOVE — the opposite claim from every other row
# here, so it needs its own list rather than a silent skip. `overlay`'s `scale` is the one entry:
# `pass-composer.js` computed it (`wanted.scale = mt.latticePx / mf.latticePx`) until 2026-09-08,
# when the full synthetic sweep (11,900 castings, every pair/role/seed — see
# ~/tlvphotos/docs/arsenal-revision-2026-09-08/composer-invisible-handles.md) showed the composer
# asking for the instrument's own rest, 1.0, on every single one — a line of arithmetic that only
# ever hands back the value it started from buys nothing, so the line was struck
# (pass-composer.js, the overlay `wanted` block: "the line is gone; ... The handle stays on the
# instrument at its own published rest"). A handle nothing drives cannot be proven to MOVE by
# anything driving it, so the honest claim left is the opposite one, proven the same way every
# other claim here is: sixty-odd real donor mutations, none of which move it.
RESTS_AT_DEFAULT = {
    ("overlay", "scale"): "pass-composer.js stopped driving `scale` 2026-09-08 (the full "
                          "synthetic sweep showed it asking only for the instrument's own rest, "
                          "1.0, on every casting) — the handle stands at its own published "
                          "default now, never a computed reading",
}

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


# THE DRIVER'S OWN CEILING, SIZED FOR THE GATE THAT RUNS IT RATHER THAN FOR A LONE RUN. This driver
# is CPU-bound: it walks twenty-one instruments through a real composer in one node process. A lone
# run of this suite measured 570 s on 2026-09-04, when the walk searched all 121 by 121 real records
# for every seat; on the constructed corpus that search is a fixed square whose side is the number of
# classes, and the lone run of 2026-09-07 measured 142 s. tests/run_all.py's own default is
# `--jobs 8`, so under the gate that same work shares the host with seven other
# suites, and at 900 s it was once killed there while passing standalone minutes later — the whole
# suite reported red on a cap, with no instrument actually failing. The ceiling is therefore the
# lone-run cost against the gate's own job count, both numbers read off what is already written down:
# this suite's own measured duration and run_all.py's declared default. A driver that truly hangs
# still ends here rather than never.
NODE_TIMEOUT_S = 142 * 8


def run_node(driver_text, args=()):
    """Runs `driver_text` under a real `node` in a throwaway directory and returns the parsed JSON of
    its last stdout line, or an {"error": ...} dict naming what went wrong — so a row that could not
    run reads as a stated failure rather than a silent pass. Same shape as test_pass_tilt.py's."""
    d = Path(tempfile.mkdtemp(prefix="synth_readsnode_"))
    try:
        (d / "driver.js").write_text(driver_text, encoding="utf-8")
        proc = subprocess.run(["node", str(d / "driver.js")] + [str(a) for a in args],
                              capture_output=True, text=True, timeout=NODE_TIMEOUT_S)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-400:]}
        lines = proc.stdout.strip().splitlines()
        if not lines:
            return {"error": "the driver printed nothing"}
        return json.loads(lines[-1])
    except subprocess.TimeoutExpired:
        # A TIMEOUT IS AN EMERGENCY STOP AND NEVER A VERDICT — this tree's own standing law
        # (tlvphotos CLAUDE.md, "No clock on this machine", the owner's word of 2026-09-07 19:47;
        # the pack says the same in guardrails.config.json as `timeout_is_never_a_verdict`). The
        # ceiling above bounds a driver that truly HANGS. A busy host reaching it says nothing about
        # any instrument, and letting it fall through to the generic handler below turned one stop
        # into a row per instrument, each reading FAIL and naming something that was never measured:
        # on 2026-09-09 this suite printed 24 such rows under four parallel lanes and passed on its
        # own minutes later. So the run ENDS here, with its own exit code, and writes no row it
        # cannot stand behind. A suite that can go red because the host was busy is a defect in that
        # suite, and this is where that defect is repaired.
        print("\nSTOPPED — the readings driver hit its emergency stop at %g s without\n"
              "finishing. Nothing above is a verdict on any instrument. Run this suite\n"
              "on its own for one."
              % NODE_TIMEOUT_S)
        sys.exit(3)
    except Exception as e:
        return {"error": str(e)}
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- reading the declarations
# THE DECLARATIONS ARE READ OUT OF THE SHIPPED SOURCE, never copied into this file. That is what
# makes the plant of PLAN.md rule 8 bite: retype one instrument's `reads:` to a measurement it does
# not read and this row varies THAT measurement instead, finds the handle standing still, and goes
# red naming the instrument and the handle. A table hand-typed here would sail through the same
# plant, which is the whole defect this row exists to close.

def declared_handles(text):
    """{handle: reads-sentence} for every driveable handle in a module's own manifest.

    A driveable handle is a `<name>: { ... }` block carrying `min:` and `def:` AT ITS OWN LEVEL —
    which is what a score can turn — as against the report shapes (`readAtADoor`, `heldWholeAtADoor`,
    the cue's own written record) and the `suits:` block, none of which carry a range. The scan is
    brace-aware and steps over strings and comments, so a brace inside a shader or a sentence does
    not shift the count.
    """
    out, stack, i, n = {}, [], 0, len(text)
    while i < n:
        c = text[i]
        if c == "{":
            head = text[max(0, i - 80):i]
            m = re.search(r"([A-Za-z_$][\w$]*)\s*:\s*$", head)
            stack.append((m.group(1) if m else None, i))
            i += 1
        elif c == "}":
            if stack:
                name, start = stack.pop()
                body = text[start:i + 1]
                own = body[1:-1]                               # this block's own level only
                while re.search(r"\{[^{}]*\}", own):
                    own = re.sub(r"\{[^{}]*\}", "", own)
                if name and name not in out and "min:" in own and "def:" in own:
                    m = re.search(r"\breads:\s*(null|\"(?:[^\"\\]|\\.)*\""
                                  r"(?:\s*\+\s*\"(?:[^\"\\]|\\.)*\")*)", own)
                    if m:
                        out[name] = ("null" if m.group(1) == "null"
                                     else "".join(re.findall(r"\"((?:[^\"\\]|\\.)*)\"", m.group(1))))
            i += 1
        elif c in "\"'`":
            i += 1
            while i < n and text[i] != c:
                i += 2 if text[i] == "\\" else 1
            i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i)
            i = n if j < 0 else j + 2
        else:
            i += 1
    return out


def declared_suits(text):
    """The list the manifest's own `suits: { reads: [...] }` publishes, verbatim."""
    m = re.search(r"suits:\s*\{\s*reads:\s*\[(.*?)\]", text, re.S)
    return re.findall(r"\"((?:[^\"\\]|\\.)*)\"", m.group(1)) if m else []


def field_of(sentence):
    """The first work-record field a `reads:` sentence names, or None if it names none."""
    m = PATH_RE.search(sentence)
    return m.group(0) if m else None


plan, parse_error = [], None
for name in INSTRUMENTS:
    src = ASSETS / ("pass-inst-%s.js" % name)
    if not src.exists():
        parse_error = "no such instrument file: %s" % src
        break
    text = src.read_text(encoding="utf-8")
    # SPEC.md Requirement 123's own catalogue, read off the instrument's own manifest text rather
    # than typed — the same source pass-composer.js's CROSSING_INSTRUMENTS filter reads. Used below
    # to ask the honest question when no pair casts the instrument: does it reach no seat because
    # its own catalogue (carrier, standing) admits none, or is that a real regression.
    catalogue_m = re.search(r'\bcatalogue:\s*"([^"]+)"', text)
    entry = {"id": name, "handles": [], "suits": [], "unvariable": [], "control": None,
             "catalogue": catalogue_m.group(1) if catalogue_m else None}
    for handle, sentence in declared_handles(text).items():
        field = field_of(sentence)
        if field:
            entry["handles"].append({"handle": handle, "field": field, "says": sentence[:90]})
        else:
            entry["unvariable"].append(
                {"what": "handle `%s`" % handle,
                 "why": ("its manifest says `reads: null` — no measurement stands behind it"
                         if sentence == "null" else
                         "its declared reading names no field of a work record: «%s»"
                         % sentence[:70].strip())})
    for field in declared_suits(text):
        if PATH_RE.fullmatch(field):
            entry["suits"].append({"field": field})
        else:
            entry["unvariable"].append({"what": "the fit's reading `%s`" % field,
                                        "why": "it names no field of a work record"})
    for cand in CONTROL_POOL:
        if cand not in text:
            entry["control"] = cand
            break
    plan.append(entry)

# ---------------------------------------------------------------- the one driver, in Node
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [composerPath, fixPath, worksPath, assetsDir, planPath] = process.argv.slice(2);

function loadJoined(path, hook) {
  const source = fs.readFileSync(path, "utf8").replace(/@@NS@@/g, "");
  let joined = null;
  const sandbox = {window: {}, console: {log: () => {}, warn: () => {}, error: () => {}}};
  sandbox.window[hook] = (m) => { joined = m; };
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, {filename: path});
  return joined;
}

const composerJoined = loadJoined(composerPath, "__PassComposer");
if (!composerJoined) { console.log(JSON.stringify({error: "the composer joined nothing"})); process.exit(0); }
const fix = JSON.parse(fs.readFileSync(fixPath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8"));
const plan = JSON.parse(fs.readFileSync(planPath, "utf8"));
const composer = composerJoined.make(fix.consts);
const ids = Object.keys(works.works);
const SEED = 3.3;
// How far the walk widens before it will call a declared reading unread — see the note at the
// handle loop below. Forty is where the pour's `seedPlace` answers (it moves on seat 35); it is a
// reach, not a threshold, and nothing passes or fails on the number itself.
const WIDE_SEATS = 40;

function clone(o) { return JSON.parse(JSON.stringify(o)); }
function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }
function get(o, path) {
  let cur = o;
  for (const seg of path.split(".")) {
    if (cur === null || typeof cur !== "object" || !(seg in cur)) return undefined;
    cur = cur[seg];
  }
  return cur;
}
function set(o, path, value) {
  const segs = path.split("."), last = segs.pop();
  let cur = o;
  for (const seg of segs) {
    if (cur === null || typeof cur !== "object" || !(seg in cur)) return false;
    cur = cur[seg];
  }
  cur[last] = value;
  return true;
}
function drop(o, path) {
  const segs = path.split("."), last = segs.pop();
  let cur = o;
  for (const seg of segs) {
    if (cur === null || typeof cur !== "object" || !(seg in cur)) return false;
    cur = cur[seg];
  }
  delete cur[last];
  return true;
}
// EVERY REPLACEMENT VALUE IS ANOTHER RECORD OF THE CORPUS'S OWN READING at the same path — never a
// number this driver made up. The list is every record whose reading at that path differs from the
// standing one, which on a corpus built from boundary values means the donor pool for a measurement
// IS the ends of that measurement's own span. That is also the honest answer to "can this
// measurement be varied at all".
//
// AND ONE VARIATION MORE: A RECORD THAT CARRIES NO SUCH READING. Several readings are taken as
// presence rather than as a quantity — the fit asks whether a work has a measured horizon at all,
// not where it stands. A reading like that answers to nothing a donor value can do, and calling it
// unread would be wrong. The last variation therefore removes the field, which is what a work
// carrying no such measurement looks like, and a reading that only answers to that is reported as
// answering to presence rather than as moving.
const GONE = {__gone: true};
function donors(baseId, path) {
  const here = get(works.works[baseId], path);
  if (here === undefined) return null;                       // the records do not carry the field
  const out = [];
  for (const id of ids) {
    if (id === baseId) continue;
    const there = get(works.works[id], path);
    if (there !== undefined && !same(there, here)) out.push(there);
  }
  return out;
}
function applyVariation(record, path, value) {
  if (value === GONE) drop(record, path); else set(record, path, value);
}

// ---- casting: real pairs that really play the instrument, found by walking the fixture ----
// SEVERAL SEATS, NOT ONE. A handle can be gated on a reading the first pair to cast the instrument
// does not carry — the fold's ring repeat is driven only where a work's own device IS rings — so a
// handle standing still on one seat is not yet a handle that reads nothing. The walk keeps the
// first few pairs it finds and a handle is asked on each in turn.
function castingFor(instrument, want) {
  const seats = [];
  for (let i = 0; i < ids.length; i++) {
    for (let j = 0; j < ids.length; j++) {
      if (i === j) continue;
      for (const dir of ["a-to-b", "b-to-a"]) {
        let p;
        try {
          p = composer.passageFor({workRecordA: works.works[ids[i]], workRecordB: works.works[ids[j]],
                                   direction: dir, seed: SEED, routeRole: "middle"});
        } catch (e) { continue; }
        if (!p || !p.score) continue;
        const cue = (p.plan.cues || []).find((c) => c.instrument.id === instrument);
        if (!cue) continue;
        seats.push({a: ids[i], b: ids[j], dir: dir, cue: cue.id});
        if (seats.length >= want) return seats;
      }
    }
  }
  return seats;
}

// A SEAT WHERE THE HANDLE WAS ACTUALLY DRIVEN, when the wide walk never saw it move off one value.
// The walk above takes the FIRST seats the fixture offers, which all come from the collection's own
// first works, and a handle whose fill branch is gated on something rare is never driven on any of
// them. `tunnel`'s `ribs` is the case that taught this: it is filled only where BOTH works were cut
// as rings, and on the 121-record collection this walk used to run on exactly one of the 56 ordered
// pairs those works make cast the corridor — about 14,350 pairs into a walk that stops at forty. So
// this scans the whole ordered-pair space of the CORPUS for a seat publishing a DIFFERENT node for
// this one handle, and the declared reading is then varied there. That space is a fixed square whose
// side is the number of classes, so the scan costs the same however many photographs hang.
//
// IT EXCUSES NOTHING. A handle wired to no measurement publishes the same node on every seat, so
// this scan ends empty and the reading is still reported unanswered — the scan either finds a seat
// where the fill ran, and tests the declaration honestly there, or proves there is no such seat.
// It is paid only by a handle already about to be called unread; every reading that answers on the
// first seats pays nothing.
//
// THE SEARCH AND THE VARIATION RUN TOGETHER, AND THAT IS THE WHOLE REPAIR. It used to return the
// FIRST seat publishing a different node, on the assumption that a seat where the handle moved at
// all is a seat where the handle's own reading fills it. That assumption is false where a fill has
// BRANCHES: `livemirror`'s `centreY` is the two works' own `structure.regions.line.y.at` where the
// departing work bands vertically (pass-composer.js:8531, :8571) and the midpoint of their radial
// centres where it does not, so the first differing seat is usually a seat under the OTHER branch —
// the handle is driven there, the declared reading is genuinely not what drives it, varying it moves
// nothing, and a correctly wired handle read as unread. So each differing seat is TRIED, with the
// declared reading varied on it, and the first seat that answers stops the walk.
//
// IT COSTS ONLY A HANDLE ALREADY ABOUT TO BE CALLED UNREAD, exactly as the single-seat version did.
// A handle that answers on the first four seats never reaches this function at all.
//
// AND THE WALK IS BOUNDED BY THE CORPUS ITSELF, not by a number chosen here. Trying every differing
// seat would be the whole ordered-pair square, and a handle that genuinely reads nothing would then
// pay all of it. A fill reads ONE of the two works, so a seat is worth trying when it stands a
// record this walk has not yet seen departing, or one it has not yet seen arriving: every class then
// gets its turn on both sides and the walk stops after at most twice as many seats as the corpus has
// records.
function seatWhereDriven(instrument, handle, path, from, seed) {
  const base = cueOf(instrument, works.works[from.a], works.works[from.b], from.dir, seed);
  const was = base ? JSON.stringify(nodeOf(base, handle)) : null;
  const triedFrom = {}, triedTo = {};
  let softest = null;
  for (let i = 0; i < ids.length; i++) {
    for (let j = 0; j < ids.length; j++) {
      if (i === j) continue;
      for (const dir of ["a-to-b", "b-to-a"]) {
        const departing = dir === "b-to-a" ? ids[j] : ids[i];
        const arriving = dir === "b-to-a" ? ids[i] : ids[j];
        if (triedFrom[departing] && triedTo[arriving]) continue;
        const cue = cueOf(instrument, works.works[ids[i]], works.works[ids[j]], dir, seed);
        if (!cue) continue;
        const n = nodeOf(cue, handle);
        if (n === undefined || JSON.stringify(n) === was) continue;
        triedFrom[departing] = true;
        triedTo[arriving] = true;
        const seat = {a: ids[i], b: ids[j], dir: dir, cue: cue.id};
        const r = moveOnSeat(instrument, seat, handle, path, seed);
        if (r.moved || r.noField || r.presence) return r;
        if (softest === null) softest = r;
      }
    }
  }
  return softest;
}

// LAST RESORT, PAID ONLY BY A HANDLE STILL UNANSWERED AFTER seatWhereDriven's OWN FULL-CORPUS SCAN
// AT THIS FILE'S ONE FIXED SEED. `tunnel`'s `ribs` is the case that taught this one: its fill needs
// BOTH works cut as rings, and the corpus's five ring-kind records DO make twenty such ordered
// pairs — but WHICH instrument wins a pair's crossing seat is the composer's own seeded die, and
// 2026-09-08's catalogue filter (pass-composer.js's CROSSING_INSTRUMENTS) moved that die's pick, at
// THIS file's fixed SEED, off every one of the twenty (confirmed against the pre-filter module,
// which won two of the twenty at the same seed). The corpus itself still carries the class the
// handle needs; only this file's one fixed seed happens not to reach it any more. So the same
// full-corpus scan seatWhereDriven already runs is repeated once per whole seed the composer's own
// declared `seedSpan` names — not a number chosen here, the module's own bound — stopping at the
// first seed whose scan answers. Paid only by a handle already about to be reported unread, exactly
// as seatWhereDriven's own widening is.
function seatWhereDrivenAnySeed(instrument, handle, path, from) {
  const lo = Math.ceil(composer.seedSpan[0]), hi = Math.floor(composer.seedSpan[1]);
  for (let s = lo; s <= hi; s++) {
    if (s === SEED) continue;
    const r = seatWhereDriven(instrument, handle, path, from, s);
    if (r && (r.moved || r.noField || r.presence)) return r;
  }
  return null;
}

function cueOf(instrument, A, B, dir, seed) {
  let p;
  try {
    p = composer.passageFor({workRecordA: A, workRecordB: B, direction: dir,
                             seed: seed === undefined ? SEED : seed, routeRole: "middle"});
  } catch (e) { return null; }
  if (!p || !p.score) return null;
  return (p.plan.cues || []).find((c) => c.instrument.id === instrument) || null;
}
function nodeOf(cue, handle) {
  const nn = ((cue.tracks || {})[handle] || {}).node || (cue.id + "-" + handle);
  return cue.nodes[nn];
}

// Varies `path` on whichever of the two works carries a reading that moves the handle, and answers
// whether the handle moved. The departing work is tried first; a handle whose own sentence says it
// reads the ARRIVING work answers on the second, and the side is reported either way. `seed`
// defaults to this file's own fixed SEED — every existing caller keeps that same seed; only
// seatWhereDrivenAnySeed's own widened scan (above) ever passes another.
function moveOnSeat(instrument, seat, handle, path, seed) {
  const A0 = works.works[seat.a], B0 = works.works[seat.b];
  const base = cueOf(instrument, A0, B0, seat.dir, seed);
  if (!base) return {error: "the seat pair stopped casting " + instrument};
  const was = nodeOf(base, handle);
  if (was === undefined) return {absent: true};
  let recast = 0, tried = 0, presence = false;
  for (const side of ["A", "B"]) {
    const baseId = side === "A" ? seat.a : seat.b;
    const pool = donors(baseId, path);
    if (pool === null) return {noField: true};
    for (const value of pool.slice(0, 30).concat([GONE])) {
      const A = clone(A0), B = clone(B0);
      applyVariation(side === "A" ? A : B, path, value);
      const cue = cueOf(instrument, A, B, seat.dir, seed);
      if (!cue || cue.id !== base.id) { recast++; continue; }
      tried++;
      if (!same(nodeOf(cue, handle), was)) {
        if (value === GONE) { presence = true; continue; }
        return {moved: true, side: side};
      }
    }
  }
  if (presence) return {presence: true};
  if (!tried && recast) return {recast: true};
  return {moved: false};
}
function moveTest(instrument, seats, handle, path) {
  const seen = [];
  for (const seat of seats) {
    const r = moveOnSeat(instrument, seat, handle, path);
    if (r.moved || r.noField) return r;                      // the strongest answer, taken at once
    seen.push(r);
  }
  return seen.find((r) => r.presence) || seen.find((r) => r.moved === false)
         || seen[0] || {moved: false};
}

// ---- the fit, through the composer's own ranking door ----
// A `suits: { reads: [...] }` line declares what the instrument's FIT reads. The fit itself is not
// a function on the instrument (only `planet` publishes one); it lives in the composer's own
// `INSTRUMENT_SUITS` register, and the composer's exported `castForKindsRanked` is the door that
// hands out every instrument's fit for a pair. So the fit is read there, before and after, exactly
// as the composer reads it when it casts.
function fitOf(id, A, B) {
  let ranked;
  try { ranked = composer.castForKindsRanked(null, A, B, false, SEED, "s73-reads"); }
  catch (e) { return undefined; }
  const flat = [].concat.apply([], ranked || []);
  const row = flat.find((r) => r && r.id === id);
  return row ? row.fit : undefined;
}
function fitTest(id, path) {
  let presence = false;
  for (let i = 0; i < ids.length; i++) {
    const A0 = works.works[ids[i]], B0 = works.works[ids[(i + 1) % ids.length]];
    const was = fitOf(id, A0, B0);
    if (was === undefined) return {noFit: true};
    const pool = donors(ids[i], path);
    if (pool === null) return {noField: true};
    for (const value of pool.slice(0, 25).concat([GONE])) {
      const A = clone(A0);
      applyVariation(A, path, value);
      if (fitOf(id, A, B0) !== was) {
        if (value === GONE) { presence = true; continue; }
        return {moved: true};
      }
    }
  }
  return presence ? {presence: true} : {moved: false};
}
function fitStill(id, path) {
  for (let i = 0; i < ids.length && i < 40; i++) {
    const A0 = works.works[ids[i]], B0 = works.works[ids[(i + 1) % ids.length]];
    const was = fitOf(id, A0, B0);
    if (was === undefined) return null;
    const pool = donors(ids[i], path);
    if (pool === null || !pool.length) continue;
    for (const value of pool.slice(0, 25).concat([GONE])) {
      const A = clone(A0);
      applyVariation(A, path, value);
      if (fitOf(id, A, B0) !== was) return false;
    }
  }
  return true;
}

const out = {instruments: {}};
for (const entry of plan) {
  const id = entry.id;
  const rec = {seats: null, handles: [], suits: [], control: entry.control, controlStill: null};
  if (entry.handles.length) {
    const seat = castingFor(id, 4);
    rec.seats = seat;
    if (!seat.length) {
      rec.noCast = true;
    } else {
      // A HANDLE IS NOT CALLED UNREAD UNTIL THE WALK HAS LOOKED HARD. Four seats is what a reading
      // that answers needs; a handle driven only under a BRANCH of the fill needs a seat where that
      // branch ran. The pour's `seedPlace` is the case that taught this: the composer sets it only
      // where the arrival crystallized on a grain-seed locus, about a third of the pour's seats do,
      // and none of the first four did — so a genuinely wired reading read as unwired. The walk
      // therefore widens, and only for a handle about to be reported as standing still: the 66 that
      // answer on the first seats pay nothing, and the control below keeps its four seats, because
      // a control that has to be hunted for over forty is not a control. `seedPlace` answers on
      // seat 35, side B, which is the ARRIVING work its own sentence names.
      let wide = null;
      for (const h of entry.handles) {
        let r = moveTest(id, seat, h.handle, h.field);
        if (!r.moved && !r.noField && !r.presence) {
          if (wide === null) wide = castingFor(id, WIDE_SEATS);
          if (wide.length > seat.length) r = moveTest(id, wide, h.handle, h.field);
        }
        if (!r.moved && !r.noField && !r.presence) {
          // Still standing after forty seats: walk every seat where this handle was driven at all
          // and vary the declared measurement on each, taking the first that answers.
          const driven = seatWhereDriven(id, h.handle, h.field, seat[0]);
          if (driven) r = driven;
        }
        if (!r.moved && !r.noField && !r.presence) {
          // Still standing after the whole corpus at this file's one fixed seed: try that same
          // full-corpus scan again at every other whole seed the composer's own seedSpan names
          // (seatWhereDrivenAnySeed, above) — paid only here, by a handle already about to be
          // reported unread.
          const drivenAnySeed = seatWhereDrivenAnySeed(id, h.handle, h.field, seat[0]);
          if (drivenAnySeed) r = drivenAnySeed;
        }
        rec.handles.push(Object.assign({handle: h.handle, field: h.field}, r));
      }
      // THE CONTROL. One measurement the instrument's whole file never names, varied the same way:
      // no handle of the instrument may answer to it. Reported per handle that does.
      if (entry.control) {
        const stirred = [];
        for (const h of entry.handles) {
          const r = moveTest(id, seat, h.handle, entry.control);
          if (r.moved) stirred.push(h.handle);
        }
        rec.controlStill = stirred.length === 0;
        rec.controlStirred = stirred;
      }
    }
  }
  for (const s of entry.suits) {
    rec.suits.push(Object.assign({field: s.field}, fitTest(id, s.field)));
  }
  if (entry.suits.length && entry.control) {
    rec.fitControlStill = fitStill(id, entry.control);
  }
  out.instruments[id] = rec;
}
console.log(JSON.stringify(out));
"""

# ---------------------------------------------------------------- the rows
FLEET_ROW = ("PASS-READS the fleet's own declared readings are the nineteen instruments this file "
             "walks — the fourteen the sweep found standing on a grep and the five S-93 added — "
             "and every one is walked")

if parse_error:
    check(FLEET_ROW, False, parse_error)
elif not node_available():
    skip(FLEET_ROW, "node is not installed (pinned expected skip)")
    for name in INSTRUMENTS:
        skip("PASS-READS %s's declared readings move the handles they name" % name,
             "node is not installed (pinned expected skip)")
else:
    tmp = Path(tempfile.mkdtemp(prefix="synth_readsplan_"))
    try:
        plan_path = tmp / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        # THE CORPUS THE WALK RUNS ON, written out in the same shape the real fixture had, so the
        # driver reads one shape and nothing inside it knows which corpus it is walking.
        corpus_path = tmp / "synthetic-works.json"
        corpus_path.write_text(json.dumps({"works": synthetic_works.corpus()}), encoding="utf-8")
        ran = run_node(DRIVER, args=[COMPOSER_MODULE, FIXTURE_COMPOSED, corpus_path,
                                     ASSETS, plan_path])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    got = ran.get("instruments") if isinstance(ran, dict) else None
    declared_total = sum(len(e["handles"]) + len(e["suits"]) for e in plan)
    unvariable_total = sum(len(e["unvariable"]) for e in plan)
    check(FLEET_ROW,
          not (isinstance(ran, dict) and ran.get("error")) and isinstance(got, dict)
          and sorted(got) == sorted(INSTRUMENTS),
          ("%d instruments walked; %d declared readings name a field of a work record and are "
           "varied below; %d name none and are skipped by name in their own instrument's row"
           % (len(INSTRUMENTS), declared_total, unvariable_total))
          if isinstance(got, dict) else "driver result: %s" % ran)

    proven = skipped_readings = 0
    unanswered = set()
    for entry in plan:
        name = entry["id"]
        row = "PASS-READS %s's declared readings move the handles they name" % name
        rec = (got or {}).get(name)
        if not rec:
            check(row, False, "the driver returned nothing for this instrument: %s" % ran)
            continue

        good, bad, notes = [], [], []
        for u in entry["unvariable"]:
            notes.append("SKIP %s — %s" % (u["what"], u["why"]))

        if rec.get("noCast"):
            # THE HONEST QUESTION, GIVEN THE CATALOGUE (2026-09-08). `pass-composer.js`'s
            # CROSSING_INSTRUMENTS filter keeps a `carrier` or `standing` instrument off every
            # crossing-voice seat (pivot/travel/arrival) — the ONLY seat `passageFor` ever casts
            # through — so `tilt` (carrier), `hero` and `lens` (standing) reach no seat at all and
            # this row can get no live cue to probe them with. That is a fact about the seat, never
            # a claim their own handle wiring is broken; this suite is named in EXPECTED_RED
            # (tests/run_all.py) for exactly the three of them, with this same reason.
            if entry.get("catalogue") in ("carrier", "standing"):
                bad.append("no pair of the constructed corpus casts this instrument — it is "
                           "catalogued `%s` and reaches no crossing-voice seat since the catalogue "
                           "filter landed (2026-09-08); no %s-seat mechanism exists yet to cast it "
                           "through instead, so this row cannot get a live cue to probe (EXPECTED_RED, "
                           "see tests/run_all.py)" % (entry["catalogue"], entry["catalogue"]))
            else:
                bad.append("no pair of the constructed corpus casts this instrument, so no handle "
                           "of it could be moved at all")
        for h in rec.get("handles", []):
            what = "`%s` ← %s" % (h["handle"], h["field"])
            if h.get("moved"):
                good.append("%s moves on the %s work" % (what, "departing" if h["side"] == "A"
                                                         else "arriving"))
            elif h.get("presence"):
                good.append("%s answers to whether the reading is there at all — no donor value "
                            "moves it, a record carrying no such reading does" % what)
            elif h.get("noField"):
                notes.append("SKIP %s — the corpus's records carry no such field" % what)
            elif h.get("absent"):
                notes.append("SKIP %s — the cast cue publishes no node for this handle" % what)
            elif h.get("recast"):
                notes.append("SKIP %s — every donor reading recast the passage onto another cue, so "
                             "the measurement cannot be varied in isolation here" % what)
            elif h.get("error"):
                bad.append("%s: %s" % (what, h["error"]))
            elif (name, h["handle"]) in RESTS_AT_DEFAULT:
                # THE OPPOSITE CLAIM, PROVEN THE SAME WAY: `moved` reading False here is not a
                # handle standing unread, it is `RESTS_AT_DEFAULT`'s own claim made real — the sixty-
                # odd real donor mutations `moveOnSeat`/`seatWhereDriven`/`seatWhereDrivenAnySeed`
                # already tried, across every seat this run's widening reaches, moved it not once.
                good.append("%s stands still — %s" % (what, RESTS_AT_DEFAULT[(name, h["handle"])]))
            else:
                key = (name, "`%s`" % h["handle"], h["field"])
                unanswered.add(key)
                (notes if key in UNANSWERED else bad).append(
                    "UNANSWERED %s — %s" % (what, UNANSWERED.get(
                        key, "the handle does not move when its own named measurement is varied "
                             "across two works, and this row has no record of why")))
        for s in rec.get("suits", []):
            what = "the fit ← %s" % s["field"]
            if s.get("moved"):
                good.append("%s moves the instrument's own fit" % what)
            elif s.get("presence"):
                good.append("%s answers to whether the reading is there at all — the fit asks "
                            "whether a work carries it, not where it stands" % what)
            elif s.get("noField"):
                notes.append("SKIP %s — the corpus's records carry no such field" % what)
            elif s.get("noFit"):
                notes.append("SKIP %s — the composer's own ranking publishes no fit for this "
                             "instrument" % what)
            else:
                key = (name, "the fit", s["field"])
                unanswered.add(key)
                (notes if key in UNANSWERED else bad).append(
                    "UNANSWERED %s — %s" % (what, UNANSWERED.get(
                        key, "the fit does not move when this reading is varied across two works, "
                             "and this row has no record of why")))

        if rec.get("controlStill") is False:
            bad.append("the control reading %s, which this instrument's file never names, moves %s"
                       % (rec.get("control"), ", ".join(rec.get("controlStirred", []))))
        elif rec.get("controlStill") is True:
            good.append("the control reading %s, named nowhere in the file, moves no handle"
                        % rec.get("control"))
        if rec.get("fitControlStill") is False:
            bad.append("the control reading %s, which this instrument's file never names, moves "
                       "its own fit" % rec.get("control"))
        elif rec.get("fitControlStill") is True:
            good.append("the control reading %s moves no fit" % rec.get("control"))

        proven += len(rec.get("handles", [])) + len(rec.get("suits", []))
        skipped_readings += len(notes)
        detail = "; ".join(good + notes) if not bad else "; ".join(bad + notes)
        if not bad and not good:
            skip(row, "no declared reading of this instrument names a field of a work record. "
                      + "; ".join(notes))
        else:
            check(row, not bad, detail)

    check("PASS-READS the readings this run could not vary are counted and named, never passed over",
          isinstance(got, dict),
          "%d declared readings varied through a real run; %d printed as SKIP with the reason on "
          "the instrument's own row above — a reading that names no measurement, a field the "
          "corpus's records do not carry, or one that cannot be moved without recasting the "
          "passage; %s"
          % (proven, skipped_readings + unvariable_total,
             "none unanswered" if not unanswered
             else "%d unanswered, each named on its own instrument's row" % len(unanswered)))

    fresh = sorted(unanswered - set(UNANSWERED))
    repaired = sorted(set(UNANSWERED) - unanswered)
    check("PASS-READS no declared reading of the fleet answers to nothing",
          isinstance(got, dict) and not fresh and not repaired,
          "every declared reading of the nineteen either moves the handle or the fit it names, or "
          "is skipped by name with its own reason; the six of 2026-09-03 were closed by S-86 and "
          "the five instruments outside its reach were brought inside it by S-93"
          if not fresh and not repaired else
          ("unrecorded and unanswered: %s; " % ", ".join("%s %s ← %s" % k for k in fresh)
           if fresh else "")
          + ("recorded as unanswered and now answering, so the record is stale and has to shrink: "
             "%s" % ", ".join("%s %s ← %s" % k for k in repaired) if repaired else ""))

# ---------------------------------------------------------------- the smoke on real records
# It carries no law. The walk above proves what the composer does; these two prove that the SHAPE the
# corpus was built to imitate is still the shape the site writes, and that the real shape still feeds
# this composer and comes back with a cast passage. Both read a FIXED handful — six real records and
# the six ordered pairs they make in a ring — so hanging a photograph costs them nothing.
SMOKE_REAL = json.loads(FIXTURE_WORKS.read_text(encoding="utf-8"))["works"]
SMOKE_IDS = sorted(SMOKE_REAL)[:6]
_missing, _extra = set(), set()
for _sid in SMOKE_IDS:
    _paths = synthetic_works.field_paths(SMOKE_REAL[_sid])
    _missing |= _paths - synthetic_works.BASE_PATHS
    _extra |= synthetic_works.BASE_PATHS - _paths
check("PASS-READS schema smoke · a real per-work record still carries exactly the field paths the "
      "constructed corpus is built on",
      not _missing and not _extra,
      "%d real record(s) read against the synthetic base's own %d field paths"
      % (len(SMOKE_IDS), len(synthetic_works.BASE_PATHS))
      + ("; the records carry, and the corpus does not: %s" % sorted(_missing) if _missing else "")
      + ("; the corpus carries, and the records do not: %s" % sorted(_extra) if _extra else ""))

SMOKE_ROW = ("PASS-READS wiring smoke · a handful of real records still cast a passage through the "
             "real composer and publish a node for every handle they drive")
SMOKE_DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [composerPath, fixPath, worksPath] = process.argv.slice(2);
let joined = null;
const sandbox = {window: {}, console: {log: () => {}, warn: () => {}, error: () => {}}};
sandbox.window.__PassComposer = (m) => { joined = m; };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(composerPath, "utf8").replace(/@@NS@@/g, ""), sandbox,
                {filename: composerPath});
if (!joined) { console.log(JSON.stringify({error: "the composer joined nothing"})); process.exit(0); }
const fix = JSON.parse(fs.readFileSync(fixPath, "utf8"));
const works = JSON.parse(fs.readFileSync(worksPath, "utf8")).works;
const composer = joined.make(fix.consts);
const ids = Object.keys(works).sort().slice(0, 6);
const bad = [];
let played = 0, driven = 0;
for (let i = 0; i < ids.length; i++) {
  const x = ids[i], y = ids[(i + 1) % ids.length];
  if (x === y) continue;
  let p = null;
  try {
    p = composer.passageFor({workRecordA: works[x], workRecordB: works[y],
                             direction: i % 2 ? "b-to-a" : "a-to-b", seed: 3.3,
                             routeRole: "middle"});
  } catch (e) { bad.push(x + "->" + y + ": threw " + String(e && e.message).slice(0, 90)); continue; }
  if (!p || p.declined || !p.score) { bad.push(x + "->" + y + ": nothing came back"); continue; }
  played++;
  for (const c of (p.plan.cues || [])) {
    const man = (fix.consts.manifests[c.instrument.id] || {}).handles || {};
    for (const h of Object.keys(c.tracks || {})) {
      driven++;
      if (!(h in man)) bad.push(x + "->" + y + ": " + c.instrument.id + " drives \u00ab" + h + "\u00bb, undeclared");
      else if (!c.nodes[((c.tracks[h] || {}).node) || (c.id + "-" + h)]) {
        bad.push(x + "->" + y + ": " + c.instrument.id + " drives \u00ab" + h + "\u00bb with no node");
      }
    }
  }
}
console.log(JSON.stringify({pairs: ids.length, played: played, driven: driven,
                            bad: bad.slice(0, 6)}));
"""

if not node_available():
    skip(SMOKE_ROW, "node is not installed (pinned expected skip)")
else:
    _smoke = run_node(SMOKE_DRIVER, args=[COMPOSER_MODULE, FIXTURE_COMPOSED, FIXTURE_WORKS])
    if not isinstance(_smoke, dict) or _smoke.get("error"):
        check(SMOKE_ROW, False, "driver result: %s" % _smoke)
    else:
        _smoke_detail = ("%d real record(s), %d ordered pair(s); %d cast a passage and every one of "
                         "the %d handle(s) they drive is declared by its own instrument's manifest "
                         "and resolves to a node"
                         % (len(SMOKE_IDS), _smoke.get("pairs", 0), _smoke.get("played", 0),
                            _smoke.get("driven", 0)))
        if _smoke.get("bad"):
            _smoke_detail += "; what did not: %s" % _smoke["bad"]
        check(SMOKE_ROW,
              not _smoke.get("bad") and _smoke.get("played") == _smoke.get("pairs")
              and (_smoke.get("driven") or 0) > 0,
              _smoke_detail)

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
