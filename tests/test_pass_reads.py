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

HOW A READING IS VARIED, AND WHERE THE NEW VALUE COMES FROM.

  Never from a number this file invented. The declared measurement is varied ACROSS TWO WORKS: the
  value is lifted from another work in `tests/fixture_pass_works.json`, whose records are the
  collection's own measurements. So «vary structure.polar.tunnel» means «stand a second, real
  photograph's own corridor reading in the first one's record», and the reading that comes back is
  the composer's answer to real measured data rather than to a figure typed here.

  A donor that changes which cue is cast is passed over — a different cue is a different question —
  and the next donor is tried.

WHAT EACH ROW ASSERTS.

  · MOVED. Varying the measurement a handle's own manifest names moves that handle's node.
  · STILL. Varying a measurement the instrument's whole source never names moves it not at all.
  · The fit. Where the declaration is `suits: { reads: [...] }`, the instrument's own live
    `suits(A, B)` is called before and after, and the fit reading has to move.

WHAT IS SKIPPED, AND WHY IT IS PRINTED.

  Some declarations name no field of a work record at all — «the score's own die», «handover»,
  «nothing of either photograph», `reads: null`. Some name a field the fixture's 121 records do not
  carry, or carry identically in every one. Neither can be varied, so neither is claimed. Every one
  is printed by name with its own reason and counted, so a reading that goes unproven is visible
  rather than quietly folded into a green row.
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
ASSETS = ROOT / "engine" / "assets"
COMPOSER_MODULE = ASSETS / "pass-composer.js"
FIXTURE_COMPOSED = ROOT / "tests" / "fixture_pass_composed.json"
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
               "hero", "studio", "tunnel", "lens", "livemirror"]

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


def run_node(driver_text, args=()):
    """Runs `driver_text` under a real `node` in a throwaway directory and returns the parsed JSON of
    its last stdout line, or an {"error": ...} dict naming what went wrong — so a row that could not
    run reads as a stated failure rather than a silent pass. Same shape as test_pass_tilt.py's."""
    d = Path(tempfile.mkdtemp(prefix="synth_readsnode_"))
    try:
        (d / "driver.js").write_text(driver_text, encoding="utf-8")
        proc = subprocess.run(["node", str(d / "driver.js")] + [str(a) for a in args],
                              capture_output=True, text=True, timeout=900)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-400:]}
        lines = proc.stdout.strip().splitlines()
        if not lines:
            return {"error": "the driver printed nothing"}
        return json.loads(lines[-1])
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
    entry = {"id": name, "handles": [], "suits": [], "unvariable": [], "control": None}
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
// EVERY REPLACEMENT VALUE IS ANOTHER REAL WORK'S OWN READING at the same path — never a number this
// driver made up. The list is every work in the fixture whose record differs from the standing one
// there, which is also the honest answer to "can this measurement be varied at all".
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
// as rings, eight of the 121 records are, and of the 56 ordered pairs those eight make exactly ONE
// casts the corridor — at fixture positions 119 and 70, about 14,350 pairs into a walk that stops
// at forty. So this scans the whole ordered-pair space for a seat publishing a DIFFERENT node for
// this one handle, and the declared reading is then varied there.
//
// IT EXCUSES NOTHING. A handle wired to no measurement publishes the same node on every seat, so
// this scan ends empty and the reading is still reported unanswered — the scan either finds a seat
// where the fill ran, and tests the declaration honestly there, or proves there is no such seat.
// It is paid only by a handle already about to be called unread; every reading that answers on the
// first seats pays nothing.
function seatWhereDriven(instrument, handle, from) {
  const base = cueOf(instrument, works.works[from.a], works.works[from.b], from.dir);
  const was = base ? JSON.stringify(nodeOf(base, handle)) : null;
  for (let i = 0; i < ids.length; i++) {
    for (let j = 0; j < ids.length; j++) {
      if (i === j) continue;
      for (const dir of ["a-to-b", "b-to-a"]) {
        const cue = cueOf(instrument, works.works[ids[i]], works.works[ids[j]], dir);
        if (!cue) continue;
        const n = nodeOf(cue, handle);
        if (n !== undefined && JSON.stringify(n) !== was) {
          return {a: ids[i], b: ids[j], dir: dir, cue: cue.id};
        }
      }
    }
  }
  return null;
}

function cueOf(instrument, A, B, dir) {
  let p;
  try {
    p = composer.passageFor({workRecordA: A, workRecordB: B, direction: dir, seed: SEED,
                             routeRole: "middle"});
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
// reads the ARRIVING work answers on the second, and the side is reported either way.
function moveOnSeat(instrument, seat, handle, path) {
  const A0 = works.works[seat.a], B0 = works.works[seat.b];
  const base = cueOf(instrument, A0, B0, seat.dir);
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
      const cue = cueOf(instrument, A, B, seat.dir);
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
          // Still standing after forty seats: look for one where this handle was driven at all.
          const driven = seatWhereDriven(id, h.handle, seat[0]);
          if (driven) r = moveTest(id, [driven], h.handle, h.field);
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
        ran = run_node(DRIVER, args=[COMPOSER_MODULE, FIXTURE_COMPOSED, FIXTURE_WORKS,
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
            bad.append("no pair in the 121 fixture works casts this instrument, so no handle of it "
                       "could be moved at all")
        for h in rec.get("handles", []):
            what = "`%s` ← %s" % (h["handle"], h["field"])
            if h.get("moved"):
                good.append("%s moves on the %s work" % (what, "departing" if h["side"] == "A"
                                                         else "arriving"))
            elif h.get("presence"):
                good.append("%s answers to whether the reading is there at all — no donor value "
                            "moves it, a record carrying no such reading does" % what)
            elif h.get("noField"):
                notes.append("SKIP %s — the fixture's records carry no such field" % what)
            elif h.get("absent"):
                notes.append("SKIP %s — the cast cue publishes no node for this handle" % what)
            elif h.get("recast"):
                notes.append("SKIP %s — every donor reading recast the passage onto another cue, so "
                             "the measurement cannot be varied in isolation here" % what)
            elif h.get("error"):
                bad.append("%s: %s" % (what, h["error"]))
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
                notes.append("SKIP %s — the fixture's records carry no such field" % what)
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
          "fixture's 121 records do not carry, or one that cannot be moved without recasting the "
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
