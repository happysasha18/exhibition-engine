#!/usr/bin/env python3
"""EX-SCORE — what the client accepts of a score, and what it does to what it was handed.

Run: python3 tests/test_pass_score.py

Root: `docs/design/PASS-API-V1.md` §4.4 and §4.4a — the score's allow-list, the thirteen fields a
cue may hold, and the four §4.4/§4.7 call plan-only (`cast`, `levelOwnership`, `measuredHandles`,
`returnOf`). And charter shelf 20 (`SPEC.md` Requirement 32, in the tlvphotos tree): «A number that
shapes behaviour comes from a picture's own record, from the dramaturgy of the walk, or from the
session … and never from a tally over the collection.»

WHAT THIS MEASURES, and how it is anchored.

  THE CHECKER IS RUN, NOT DESCRIBED. `passScoreCheck`, the ceiling it reads a weight against and the
  reading it asks of an authored line are extracted verbatim from the BUILT client
  (`engine/assets/exhibition.js`) and executed in node, together with the register block they stand
  on. Nothing of the rule is re-typed here.

  THE CUE ALLOW-LIST IS READ OFF THE CONTRACT, NOT COPIED. Row S5 parses the thirteen names out of
  §4.4's own cue block in `docs/design/PASS-API-V1.md` and compares them with the list the client
  fences on, so the two cannot drift apart without a row going red.

  ONE SMOKE CHECK, LABELLED AS ONE. Row S6 runs the shipped composer in node over the one pair the
  composed fixture carries and reads which keys its cues come out with. It is a smoke check that the
  code runs and writes plausible output on real records — never coverage, never correctness, and it
  proves nothing about any other pair. What it is FOR is the opposite of a claim: it would go red if
  the fence stripped something the composer writes.

Rows:
  S1  the checker travels as one block of the shipped client, and runs on its own
  S2  the strip copies and never edits what it was handed — envelope and cues alike
  S3  an unknown top-level field is stripped, recorded, and the score still reads
  S4  a cue carrying a plan-only field is stripped and recorded; a cue carrying only what it may is
      carried over untouched, the same object rather than a copy of it
  S5  the thirteen names the client fences a cue on are the thirteen §4.4 itself lists
  S6  smoke check · the shipped composer's own cues carry nothing the fence would strip
  S7  an authored line that reads as a payload is not carried; an honest sentence travels WHOLE,
      however long, and nothing is cut to a length
  S8  the weight is read against a ceiling constructed from the register and the manifests held, and
      a client holding no manifest states no reading rather than guessing one
  S9  red-on-bug · the cue fence removed: the plan-only fields reach the host again
  S10 red-on-bug · the strip mutating again: the record handed in comes back edited
  S11 red-on-bug · the authored line cut to a length again: an honest sentence is truncated

node is a hard dependency (the checker is the test) — its absence FAILS, never skips. The source
tree is never written to; every copy runs in a temporary file that is removed afterwards.
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
CONTRACT = (ROOT / "docs" / "design" / "PASS-API-V1.md").read_text(encoding="utf-8")
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def report_and_exit():
    for n, s, d in results:
        print(f"{s}  {n}" + (f"   — {d}" if d else ""))
    bad = sum(1 for _, s, _ in results if s == "FAIL")
    print(f"\n{len(results) - bad} passed / {bad} failed")
    sys.exit(1 if bad else 0)


# ---------------------------------------------------------------- S1: the pieces, extracted
def slice_between(head, tail):
    if head not in BUNDLE or tail not in BUNDLE:
        return None
    a, b = BUNDLE.index(head), BUNDLE.index(tail)
    return BUNDLE[a:b] if a < b else None


REGISTER = slice_between('  const PASS_KEY = "', "  const passEvents = [];")
CHECKER = slice_between("  const PASS_POINT_CHARS = ",
                        "  // NO SCORE PER PAIR TRAVELS WITH THE PRODUCT.")
NODE = shutil.which("node")

check("S1 EX-SCORE the checker travels as one block of the shipped client, with the register it "
      "stands on",
      REGISTER is not None and CHECKER is not None,
      "" if (REGISTER and CHECKER) else
      "missing from engine/assets/exhibition.js: %s"
      % ", ".join(n for n, v in (("the register block", REGISTER), ("the checker block", CHECKER))
                  if v is None))
if REGISTER is None or CHECKER is None:
    report_and_exit()
if not NODE:
    check("S1 EX-SCORE node present (the checker is the test)", False, "node not on PATH")
    report_and_exit()

# ---------------------------------------------------------------- the driver
# The checker's own surroundings and nothing else: the collection's constants, which is where the
# instrument manifests the ceiling is constructed from live.
DRIVER = r"""
'use strict';
function makeChecker(manifests) {
  const passComposerConsts = () => (manifests === null ? null : { manifests: manifests });
__REGISTER__
__CHECKER__
  return { check: passScoreCheck, ceiling: passScoreCeiling, pointChars: PASS_POINT_CHARS,
           cueFields: PASS_CUE_FIELDS.slice(), limits: PASS_LIMITS };
}

// Two instruments' worth of manifest, the shape `pass.composer.manifests` carries: a handle list per
// instrument. The widest of them is what the ceiling is built on.
const MANIFESTS = { narrow: { handles: { a: {}, b: {} } },
                    wide: { handles: { a: {}, b: {}, c: {}, d: {}, e: {} } } };
const K = makeChecker(MANIFESTS);
const BLIND = makeChecker(null);

function cue(extra) {
  const c = { id: "c1", instrument: { id: "weave", api: 1 }, voice: "letter", roles: ["assembly"],
              levels: ["SURFACE"], window: [0, 1], works: ["a", "b"], stack: 0,
              cameraAuthority: "stage", doors: {}, nodes: {}, tracks: {}, resources: {} };
  Object.keys(extra || {}).forEach((k) => { c[k] = extra[k]; });
  return c;
}
function score(over) {
  const s = { schema: 2, intent: "a plain sentence about the crossing", pair: { a: "a", b: "b" },
              seed: 1, duration: 800, direction: "a-to-b", cues: [cue(null)] };
  Object.keys(over || {}).forEach((k) => { s[k] = over[k]; });
  return s;
}

const out = {};

// S2/S10 · the record handed in is untouched
{
  const handed = score({ mystery: 1, cues: [cue({ levelOwnership: { SURFACE: "c1" } })] });
  const before = JSON.stringify(handed);
  const got = K.check(handed);
  out.copies = { after: JSON.stringify(handed), unchanged: JSON.stringify(handed) === before,
                 ok: got.ok, sameEnvelope: got.score === handed,
                 sameCue: got.score.cues[0] === handed.cues[0] };
}
// S3 · the envelope strip
{
  const got = K.check(score({ mystery: 1, andAnother: 2 }));
  out.envelope = { ok: got.ok, keys: Object.keys(got.score).sort(), noted: got.noted };
}
// S4 · the cue fence, one plan-only name at a time, and the untouched case
out.cues = ["cast", "levelOwnership", "measuredHandles", "returnOf"].map(function (name) {
  const extra = {};
  extra[name] = { anything: true };
  const got = K.check(score({ cues: [cue(extra)] }));
  return { name: name, ok: got.ok, left: Object.keys(got.score.cues[0]).sort(),
           noted: got.noted };
});
{
  const handed = score(null);
  const got = K.check(handed);
  out.cueUntouched = { same: got.score.cues[0] === handed.cues[0], noted: got.noted };
}
// S7 · the authored line
out.prose = {};
["{a:1}", "[1,2]", "<b>x</b>", "a\\b", "`x`", "() => 1", "function (x)"].forEach(function (p, i) {
  const got = K.check(score({ intent: "a sentence and then " + p }));
  out.prose["payload" + i] = { carried: got.score.intent !== undefined, noted: got.noted };
});
{
  const long = new Array(400).join("a long honest sentence about the crossing, ");
  const got = K.check(score({ intent: long }));
  out.prose.longSentence = { carried: got.score.intent === long, chars: long.length };
}
{
  const got = K.check(score({ intent: 42 }));
  out.prose.notText = { carried: got.score.intent !== undefined, noted: got.noted };
}
// S8 · the ceiling
{
  const heavy = score({ intent: new Array(300000).join("x ") });
  out.ceiling = { built: K.ceiling(), blind: BLIND.ceiling(), pointChars: K.pointChars,
                  limits: { instruments: K.limits.instruments, curve: K.limits.curve },
                  heavyNoted: K.check(heavy).noted,
                  blindOnHeavy: BLIND.check(heavy).noted,
                  plainNoted: K.check(score(null)).noted };
}
out.cueFields = K.cueFields.sort();
process.stdout.write(JSON.stringify(out));
"""


def run(register, checker, tag):
    src = (DRIVER.replace("__REGISTER__", register).replace("__CHECKER__", checker))
    fh = tempfile.NamedTemporaryFile("w", suffix="_%s.js" % tag, delete=False, encoding="utf-8")
    fh.write(src)
    fh.close()
    try:
        r = subprocess.run([NODE, fh.name], capture_output=True, text=True, timeout=180)
    finally:
        Path(fh.name).unlink(missing_ok=True)
    if r.returncode != 0:
        return None, (r.stderr or r.stdout or "").strip().splitlines()[-1:]
    return json.loads(r.stdout), None


GOT, why = run(REGISTER, CHECKER, "shipped")
if GOT is None:
    check("S1 EX-SCORE the extracted checker runs on its own", False, "node said: %s" % (why or ""))
    report_and_exit()

# ---------------------------------------------------------------- S2: copies, never edits
C = GOT["copies"]
check("S2 EX-SCORE the strip copies and never edits what it was handed — the record handed in comes "
      "back exactly as it went, envelope and cues alike",
      C["unchanged"] is True and C["ok"] is True and C["sameEnvelope"] is False
      and C["sameCue"] is False,
      "the record handed in is unchanged: %s; what comes back is a new envelope: %s, and the cue "
      "that had a field taken off it is a new cue: %s"
      % (C["unchanged"], not C["sameEnvelope"], not C["sameCue"]))

# ---------------------------------------------------------------- S3: the envelope
E = GOT["envelope"]
check("S3 EX-SCORE an unknown top-level field is stripped, the cut is recorded, and the score still "
      "reads",
      E["ok"] is True and "mystery" not in E["keys"] and "andAnother" not in E["keys"]
      and E["noted"] and any("mystery" in n and "andAnother" in n for n in E["noted"]),
      "what comes back holds %s; the cut is said as %s" % (E["keys"], E["noted"]))

# ---------------------------------------------------------------- S4: the cue fence
bad_cue = [r for r in GOT["cues"]
           if not (r["ok"] and r["name"] not in r["left"]
                   and r["noted"] and any(r["name"] in n for n in r["noted"]))]
U = GOT["cueUntouched"]
check("S4 EX-SCORE a cue carrying a plan-only field is stripped and the cut recorded; a cue carrying "
      "only what it may is carried over untouched, the same object rather than a copy",
      not bad_cue and U["same"] is True and not U["noted"],
      "the four plan-only names are cut and said: %s; a clean cue comes back as the very object "
      "handed in (%s) with nothing noted"
      % ([r["name"] for r in GOT["cues"]], U["same"]))

# ---------------------------------------------------------------- S5: the list is the contract's
# §4.4's cue block, parsed out of the contract itself: the names of the record's OWN fields, which
# are the identifiers standing at the top level of the fenced block between «Each cue:» and the
# paragraph after it. A field is named either with a colon after it or bare; either way it opens at
# the head of the record or just after a comma, and anything deeper belongs to a nested record.
block = CONTRACT[CONTRACT.index("Each cue:"):]
block = block[block.index("```") + 3:]
block = block[:block.index("```")]
CONTRACT_CUE, depth, at_head = [], 0, False
for token in re.findall(r"[{}\[\],]|[A-Za-z][A-Za-z0-9]*", block):
    if token in "{[":
        depth += 1
        at_head = depth == 1
    elif token in "}]":
        depth -= 1
        at_head = False
    elif token == ",":
        at_head = depth == 1
    elif at_head and depth == 1:
        CONTRACT_CUE.append(token)
        at_head = False
CONTRACT_CUE = sorted(set(CONTRACT_CUE))
FENCE = GOT["cueFields"]
check("S5 EX-SCORE the names the client fences a cue on are the ones §4.4 itself lists — read off "
      "the contract rather than copied here",
      bool(CONTRACT_CUE) and sorted(FENCE) == CONTRACT_CUE,
      "the contract lists %s; the client fences on %s" % (CONTRACT_CUE, sorted(FENCE)))

# ---------------------------------------------------------------- S6: the smoke check
SMOKE = r"""
const fs = require("fs");
let src = fs.readFileSync(process.argv[2], "utf8").replace(/@@NS@@/g, "exh");
let captured = null;
global.window = { __exhPassComposer: function (part) { captured = part; } };
eval(src);
const fix = JSON.parse(fs.readFileSync(process.argv[3], "utf8"));
const composer = captured.make(fix.consts);
const a = fix.works[fix.pair.a], b = fix.works[fix.pair.b];
const keys = new Set();
let n = 0;
["entrance", "quiet link", "middle", "culmination", "return", null].forEach(function (role) {
  ["a-to-b", "b-to-a"].forEach(function (dir) {
    for (let s = 0; s < 20; s++) {
      const req = { workRecordA: a, workRecordB: b, direction: dir, seed: s * 0.137 };
      if (role) req.routeRole = role;
      let got = null;
      try { got = composer.passageFor(req); } catch (e) { return; }
      if (!got || got.declined) continue;
      n++;
      ((got.score || {}).cues || []).forEach((c) => Object.keys(c).forEach((k) => keys.add(k)));
    }
  });
});
process.stdout.write(JSON.stringify({ n: n, keys: [...keys].sort() }));
"""
fh = tempfile.NamedTemporaryFile("w", suffix="_smoke.js", delete=False, encoding="utf-8")
fh.write(SMOKE)
fh.close()
try:
    r = subprocess.run([NODE, fh.name, str(COMPOSER), str(FIXTURE)],
                       capture_output=True, text=True, timeout=300)
finally:
    Path(fh.name).unlink(missing_ok=True)
SMOKED = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
check("S6 EX-SCORE smoke check · the shipped composer's own cues carry nothing the fence would "
      "strip (a check that the code runs and writes plausible output on real records — never "
      "coverage, and it says nothing about any pair but the one it ran)",
      SMOKED is not None and SMOKED["n"] > 0 and not set(SMOKED["keys"]) - set(FENCE),
      "over %s passages composed from the fixture's one pair, the cues carry %s; the fence would "
      "strip %s of them"
      % (SMOKED["n"] if SMOKED else "no", SMOKED["keys"] if SMOKED else "-",
         sorted(set(SMOKED["keys"]) - set(FENCE)) if SMOKED else "?"))

# ---------------------------------------------------------------- S7: the authored line
P = GOT["prose"]
payloads = [P[k] for k in sorted(P) if k.startswith("payload")]
check("S7 EX-SCORE an authored line that reads as a payload is not carried and the reading is said; "
      "an honest sentence travels WHOLE however long, and nothing is cut to a length",
      all(p["carried"] is False and p["noted"] for p in payloads)
      and P["longSentence"]["carried"] is True
      and P["notText"]["carried"] is False and P["notText"]["noted"],
      "%d payload shapes, none carried; a sentence of %d characters travels whole (%s); a line that "
      "is no text at all is not carried"
      % (len(payloads), P["longSentence"]["chars"], P["longSentence"]["carried"]))

# ---------------------------------------------------------------- S8: the constructed ceiling
CE = GOT["ceiling"]
want = CE["limits"]["instruments"] * 5 * CE["limits"]["curve"] * CE["pointChars"]
check("S8 EX-SCORE the weight is read against a ceiling constructed from the register and the "
      "manifests the client holds; a client holding none states no reading rather than guessing one",
      CE["built"] == want and CE["blind"] is None and not CE["plainNoted"]
      and CE["heavyNoted"] and any("over the" in n for n in CE["heavyNoted"])
      and not CE["blindOnHeavy"],
      "%d cues x %d handles (the widest manifest held) x %d points x %d characters a written point "
      "takes = %d; a plain score notes nothing, a runaway line is read as %s, and a client with no "
      "manifest reads %s"
      % (CE["limits"]["instruments"], 5, CE["limits"]["curve"], CE["pointChars"], CE["built"],
         CE["heavyNoted"], CE["blindOnHeavy"]))

# ---------------------------------------------------------------- S9/S10/S11: red on bug
NO_CUE = CHECKER.replace("    if (v === 2 && Array.isArray(score.cues)) {",
                         "    if (false) {")
r9, w9 = run(REGISTER, NO_CUE, "nocue") if NO_CUE != CHECKER else (None, "no match")
leaked = None
if r9:
    leaked = [x["name"] for x in r9["cues"] if x["name"] in x["left"]]
check("S9 EX-SCORE red-on-bug · the cue fence removed: the plan-only fields reach the host again",
      bool(leaked) and len(leaked) == 4 and not [r for r in GOT["cues"] if r["name"] in r["left"]],
      "with the fence removed %s reach the host inside a cue; with it standing, none do" % leaked)

MUTATES = CHECKER.replace("      if (allowed.indexOf(k) < 0) stray.push(k); else score[k] = raw[k];",
                          "      if (allowed.indexOf(k) < 0) { stray.push(k); delete raw[k]; }\n"
                          "      else score[k] = raw[k];")
r10, w10 = run(REGISTER, MUTATES, "mutates") if MUTATES != CHECKER else (None, "no match")
check("S10 EX-SCORE red-on-bug · the strip mutating again: the record handed in comes back edited",
      bool(r10) and r10["copies"]["unchanged"] is False and C["unchanged"] is True,
      "with the strip mutating, the record handed in comes back as %s; with the strip that stands "
      "it comes back unchanged"
      % ((r10["copies"]["after"][:70] + "…") if r10 else w10))

BY_LENGTH = CHECKER.replace(
    "      } else if (PASS_PROSE_STRUCTURE.test(score.intent)) {",
    "      } else if (score.intent.length > PASS_LIMITS.intent) {\n"
    "        score.intent = score.intent.slice(0, PASS_LIMITS.intent - 1) + \"\\u2026\";\n"
    "      } else if (PASS_PROSE_STRUCTURE.test(score.intent)) {")
r11, w11 = run(REGISTER, BY_LENGTH, "bylength") if BY_LENGTH != CHECKER else (None, "no match")
check("S11 EX-SCORE red-on-bug · the authored line cut to a length again: an honest sentence is "
      "truncated instead of travelling whole",
      bool(r11) and r11["prose"]["longSentence"]["carried"] is False
      and P["longSentence"]["carried"] is True,
      "with the length cut back, a sentence of %d characters no longer arrives whole; with the "
      "reading that stands, it does" % P["longSentence"]["chars"])

# ---------------------------------------------------------------- S12: the copy's own coupling
# THE COPY HAS A CONSEQUENCE OUTSIDE THE CHECKER, and it is the one thing that almost shipped broken.
# The walk finds a passage record again at the landing by the IDENTITY of the score that played
# (`passEdgeRemember`), which worked only while the checker edited the composer's object in place.
# With a copy, nothing matched: no edge record was written, so §4.8 went silently off — no return, no
# drift, no cooldown — on nothing but a changed object identity. `declare` now tells the row which
# reading of its score went to the host, and the landing looks for either. This row reads the two
# halves of that in the built client, so neither can be removed without a red; what they DO is
# measured on the real walk by `tests/test_pass_route.py`'s return row and `tests/test_pass_memory.py`.
PLAYED_SET = "if (passPassages[i].score === raw) { passPassages[i].played = score; break; }"
PLAYED_READ = "if (r.score === cmd.score || r.played === cmd.score) { row = r; break; }"
check("S12 EX-SCORE the copy keeps the walk's own passage record findable: the row that composed a "
      "score is told which reading of it played, and the landing looks for either",
      BUNDLE.count(PLAYED_SET) == 1 and BUNDLE.count(PLAYED_READ) == 1,
      "declare records the reading that played %d time(s); the landing matches on either %d time(s)"
      % (BUNDLE.count(PLAYED_SET), BUNDLE.count(PLAYED_READ)))

report_and_exit()
