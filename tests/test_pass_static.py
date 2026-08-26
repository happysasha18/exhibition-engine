#!/usr/bin/env python3
"""EX-PASS — charter shelf 21's own test, applied to every named constant on the composition road.

Run: python3 tests/test_pass_static.py

Shelf 21's test: could this value have existed before the two pictures in front of it were known? If
yes, it is banned, however it was arrived at. That is not quite the whole law, because some numbers
lawfully could — how many bytes a float takes to write, how long a frame is, how many textures a
context holds. Those are facts about the machine, the format or the arithmetic, and no picture could
answer them. What the shelf forbids is a number that shapes what a CROSSING does and answers to
nothing.

THE MECHANISM THIS ROW EXISTS FOR. A number with no sentence beside it reads as measured. That is
the mechanism behind every defect found on this road: a seam score of zero read as a measurement, a
fit of one read as a reading, a strength of nothing read as a strength, a dropped manifest field read
as an instrument declaring nothing. So the class repair is not a list of repaired numbers — it is
that EVERY named constant on this road carries its own verdict where it stands, in one of three
words:

  DERIVED      it answers a question a picture, the walk or the session can answer, and it does —
               or the sentence says what it would read and where the derivation stands.
  CAPABILITY   it is a fact about the machine, the format, the browser or the arithmetic rather than
               about pictures. The sentence says which, so nobody has to re-litigate it.
  UNJUSTIFIED  nobody measured it and nothing derives it. The sentence says plainly that it was
               chosen, by whom, and that it stands on nothing — which is what `DOLLY_CAP`'s own
               comment already does and what the rest do not.

Row one reds on every named constant whose comment carries none of the three. It is written against
SOURCE TEXT, and that is said out loud: there is no behaviour to ask, because a number with no
sentence beside it computes exactly what the same number with a sentence computes. That is precisely
why nothing caught any of them.

WHAT COUNTS AS A NAMED CONSTANT ON THIS ROAD, and the definition is the row's whole scope: a
module-scope declaration whose name is in capitals and whose value carries a digit, plus every
numeric member of a module-scope object literal whose own name is in capitals. Nothing inside a
function, because a value that shapes a crossing and lives inside a function is a number that has not
been given a name yet — and giving it one IS the repair for it, after which this row sees it.

WHAT THIS ROW DELIBERATELY DOES NOT REACH, said so nobody reads its green as wider than it is:
a bare literal inline in an expression. The sweep in docs/design/STATIC-SWEEP.md names the ones that
shape a crossing today and hands each a name; once named, they fall inside this row by themselves.

OUT OF SCOPE BY THE OWNER'S OWN BOUNDARY: a per-frame percentile over a visitor's own frame times, a
share over one picture's own pixels, a count of instruments or of test rows. None of those is a
number that shapes what a crossing does.

Row two is the one derivation this file can check by behaviour rather than by text: the composer's
transaction ceiling and the top of charter shelf 17's longest band are one number, and it should have
one home. It reds if the two ever drift.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROAD = [ROOT / "engine" / "assets" / "pass-composer.js",
        ROOT / "engine" / "assets" / "pass-layer.js",
        ROOT / "engine" / "client" / "01a-pass.js"]
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"

VERDICTS = ("DERIVED", "CAPABILITY", "UNJUSTIFIED")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- row 1: every constant answers
NUM = r"-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?"
CAPS = re.compile(r"^[A-Z][A-Z0-9_]*$")
DECL = re.compile(r"^(\s{0,4})(?:var|const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*(.+?)\s*;\s*$")
OPEN = re.compile(r"^(\s{0,4})(?:var|const|let)\s+([A-Za-z_$][\w$]*)\s*=\s*\{\s*$")
MEMBER = re.compile(r'^\s*["\']?([\w.$-]+)["\']?\s*:\s*(' + NUM + r")\s*,?\s*$")
CLOSE = re.compile(r"^\s*\}\s*;?\s*$")
# A version stamp names a format rather than shaping a crossing, and a value with no digit in it is
# not a number at all.
EXEMPT_NAME = re.compile(r"_VERSION$|^SCHEMA_")


def verdict_above(lines, at):
    """The comment block standing immediately above this line, and the verdict it names."""
    i, block = at - 2, []
    while i >= 0 and re.match(r"^\s*//", lines[i]):
        block.append(lines[i])
        i -= 1
    text = "\n".join(reversed(block))
    named = [v for v in VERDICTS if re.search(r"\b" + v + r"\b", text)]
    return text, named


def constants_of(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    out, stack = [], []
    for n, line in enumerate(lines, 1):
        o = OPEN.match(line)
        if o:
            stack.append(o.group(2))
            continue
        if stack:
            m = MEMBER.match(line)
            if m:
                if CAPS.match(stack[-1]):
                    out.append((n, stack[-1] + "." + m.group(1), m.group(2)))
                continue
            if CLOSE.match(line):
                stack.pop()
            continue
        d = DECL.match(line)
        if not d:
            continue
        name, value = d.group(2), d.group(3)
        if not CAPS.match(name) or EXEMPT_NAME.search(name):
            continue
        if not re.search(r"\d", value):
            continue
        if value.startswith(("function", "(function", "new ", "require")):
            continue
        out.append((n, name, value))
    return lines, out


unmarked, marked = [], 0
for path in ROAD:
    lines, consts = constants_of(path)
    for n, name, value in consts:
        text, named = verdict_above(lines, n)
        if named:
            marked += 1
        else:
            unmarked.append((path.name, n, name, "no sentence at all" if not text.strip()
                             else "a sentence that names no verdict"))

check("STATIC · every named constant on the composition road carries its own verdict",
      not unmarked,
      "" if not unmarked else
      ("charter shelf 21 asks of every value whether it could have existed before the two pictures "
       "in front of it were known. A number with no verdict beside it reads as measured, which is "
       "the mechanism behind every defect found on this road. Each of these needs one of "
       + ", ".join(VERDICTS) + " in the sentence above it — see docs/design/STATIC-SWEEP.md for the "
       "verdict this sweep gives each:\n"
       + "\n".join("        " + f + ":" + str(n) + "  " + name.ljust(30) + "  — " + why
                   for f, n, name, why in unmarked)))

# ---------------------------------------------------------------- row 2: one number, one home
#
# The composer shortens a derived length that runs past its transaction ceiling, and that ceiling is
# the same number as the top of charter shelf 17's longest band — a culmination runs nine to fourteen
# seconds and the transaction ends at fourteen. Two copies of one number drift; one home does not.
# This is the one entry in the sweep that can be judged by behaviour rather than by text, so it is.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath] = process.argv.slice(2);
const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const composer = joined.make(fix.consts);
const bands = composer.tierBands || {};
let top = null;
Object.keys(bands).forEach(function (t) {
  const hi = bands[t][1];
  if (top === null || hi > top) top = hi;
});
// The ceiling itself is not exported, so it is read out of the module's own source beside the value
// it is being held against — the one place this row has to read text, and it says so.
//
// IT NOW STANDS IN TWO POSSIBLE FORMS AND BOTH ARE READ. It was a typed number, which is what this
// row was written to argue against; it is now derived from the tier table itself. Both are captured
// here and the verdict is chosen on the Python side, so the row keeps a verdict whichever form the
// module is in rather than standing aside the moment the repair it asked for lands.
const lit = source.match(/var\s+TRANSACTION_MS\s*=\s*([0-9]+)\s*;/);
const der = source.match(/var\s+TRANSACTION_MS\s*=\s*\(function\s*\(\)\s*\{([\s\S]*?)\}\(\)\);/);
console.log(JSON.stringify({longestBandTop: top,
                            transactionMs: lit ? Number(lit[1]) : null,
                            derivation: der ? der[1] : null,
                            bands: bands}));
"""

TMP = Path(tempfile.mkdtemp(prefix="pass_static_"))
DRIVER_PATH = TMP / "static-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


NAME2 = "STATIC · the transaction ceiling and shelf 17's longest band are one number"
if not node_available():
    skip(NAME2, "node is not on this machine")
else:
    proc = subprocess.run(["node", str(DRIVER_PATH), str(MODULE), str(FIXTURE)],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        check(NAME2, False, (proc.stderr or "").strip()[-400:])
    else:
        got = json.loads(proc.stdout.strip().splitlines()[-1])
        top, tx, derivation = (got["longestBandTop"], got["transactionMs"],
                               got.get("derivation"))
        if tx is not None:
            # STILL A TYPED NUMBER. The original claim, unchanged: two copies of one fact, held
            # against each other, and a red here is the drift between them.
            check(NAME2, top == tx,
                  "" if top == tx else
                  ("the composer shortens a length past " + str(tx) + " ms and shelf 17's longest "
                   "band ends at " + str(top) + " ms. They are the same fact and they have drifted, "
                   "which is what two copies of one number do"))
        elif derivation is not None:
            # THE COPY IS GONE, WHICH IS WHAT THIS ROW ASKED FOR — and the row does not stand aside
            # for having been answered. What it argued was that the ceiling and shelf 17's longest
            # band must be ONE number; a derivation off the tier table makes that true by
            # construction rather than by agreement, and the verdict moves to guarding the
            # construction: the ceiling must be read from TIERS, and no number may be typed back
            # into it. A literal reappearing here re-opens exactly the drift the derivation closed,
            # so it reds.
            #
            # Only 0 and 1 are allowed in the derivation — a loop's own start and the index of a
            # band's upper end. Any other number is a magnitude, and a magnitude typed here is the
            # third copy coming back.
            typed = sorted({n for n in re.findall(r"\b\d+(?:\.\d+)?\b", derivation)
                            if n not in ("0", "1")})
            reads_table = "TIERS" in derivation and "band[1]" in derivation
            ok = reads_table and not typed and isinstance(top, (int, float)) and top > 0
            bad = []
            if not reads_table:
                bad.append("the derivation does not read TIERS' own band ends")
            if typed:
                bad.append("a magnitude is typed back into it: " + ", ".join(typed))
            if not (isinstance(top, (int, float)) and top > 0):
                bad.append("the tier table publishes no longest band to derive from")
            check(NAME2, ok,
                  ("the ceiling is derived from shelf 17's own tier table rather than typed, so it "
                   "and the longest band (" + str(top) + " ms) are one number by construction and "
                   "cannot drift apart") if ok else "; ".join(bad))
        else:
            check(NAME2, False,
                  "`TRANSACTION_MS` stands in neither form this row can read — neither a plain "
                  "literal nor a derivation off TIERS. The ceiling and shelf 17's longest band are "
                  "one fact, and this row cannot say whether they still agree")

# ---------------------------------------------------------------- row 3: no instrument ranks unread
#
# THE SAME TYPED NUMBER, COME BACK A THIRD TIME. `suitsPair` answers an instrument that publishes no
# reading of a pair with a typed 0.5, so that instrument ranks against measured rivals on a number
# nobody read — permanently, on every pair, in either direction. The file has already named this
# defect twice, for the water instrument and for the mirror floor, and repaired it both times by
# giving that one instrument a row. Repairing the instance leaves the rule, and the rule is that
# anything landing without a row inherits the typed number.
#
# This row is written against source text and says so: what it asks is whether a published
# instrument has a row at all, which is a fact about the two files rather than about any behaviour a
# pair could show.
SUITS = re.compile(r'^\s*"?([a-z][\w-]*)"?\s*:\s*function\s*\(a, b\)', re.M)
NAME3 = "STATIC · every published instrument publishes its own reading of a pair"
comp = MODULE.read_text(encoding="utf-8")
at = comp.find("var INSTRUMENT_SUITS")
end = comp.find("function suitsPair", at)
if at < 0 or end < 0:
    skip(NAME3, "`INSTRUMENT_SUITS` or `suitsPair` was not found; re-pin this row")
else:
    rows = set(SUITS.findall(comp[at:end]))
    published = sorted(p.name[len("pass-inst-"):-3]
                       for p in (ROOT / "engine" / "assets").glob("pass-inst-*.js"))
    missing = sorted(set(published) - rows)
    check(NAME3, not missing,
          "" if not missing else
          ("these instruments are cast for real pairs and publish no reading of one, so `suitsPair` "
           "answers for each of them with a number typed into the composer and each ranks against "
           "measured rivals on nothing: «" + "», «".join(missing) + "». The file has already "
           "named and repaired this for two other instruments one at a time; the class repair is "
           "in docs/design/STATIC-SWEEP.md"))

# ------------------------------------------------- rows 4 and 5: what the manifests declare
#
# The manifests are the other half of the road: a module's published cap is a number that shapes what
# a crossing does, and the composer places every reading onto one. These two rows ask the two
# questions about them that are answerable without opening a shader.
#
# Both are written against the manifests as the fleet actually registers them — each instrument file
# is loaded and its manifest read, not grepped — so a file that changes its own declaration re-bases
# them by itself.
FLEET = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const dir = process.argv[2];
const live = {}, failed = [];
for (const f of fs.readdirSync(dir).filter((n) => /^pass-inst-.*\.js$/.test(n))) {
  const sb = {window: {__PassInstrument: (r) => { live[r.instrument.name] = r.instrument.manifest; }},
              console, document: undefined};
  vm.createContext(sb);
  try { vm.runInContext(fs.readFileSync(path.join(dir, f), "utf8").replace(/@@NS@@/g, ""), sb,
                        {filename: f}); }
  catch (e) { failed.push(f); }
}
const names = Object.keys(live).sort();
const shapes = {}, clocks = {};
names.forEach(function (n) {
  const m = live[n];
  const key = JSON.stringify(m.resources || {});
  (shapes[key] = shapes[key] || []).push(n);
  const c = (m.handles || {}).clock;
  if (c) clocks[n] = c.max;
});
console.log(JSON.stringify({names: names, failed: failed, shapes: shapes, clocks: clocks}));
"""
FLEET_PATH = TMP / "fleet-driver.js"
FLEET_PATH.write_text(FLEET, encoding="utf-8")

NAME4 = "STATIC · the fleet's declared cost is a declaration, not one constant repeated"
NAME5 = "STATIC · no handle publishes a span its own transaction cannot reach"
if not node_available():
    skip(NAME4, "node is not on this machine")
    skip(NAME5, "node is not on this machine")
else:
    proc = subprocess.run(["node", str(FLEET_PATH), str(ROOT / "engine" / "assets")],
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        check(NAME4, False, (proc.stderr or "").strip()[-400:])
        skip(NAME5, "the fleet did not load")
    else:
        fleet = json.loads(proc.stdout.strip().splitlines()[-1])
        shapes = fleet["shapes"]
        # ONE distinct `resources` block across the whole fleet means no instrument declares a cost
        # different from any other's, and no quality variant declares one different from its
        # siblings — so the quality ladder cannot be walked on what a crossing would cost, and
        # PASS-API-V1's row 22 (a declaration understating its bytes reds) has nothing to judge.
        one = len(shapes) == 1
        sole = list(shapes.values())[0] if one else []
        zero_bytes = one and '"bytesEstimate":0' in list(shapes.keys())[0].replace(" ", "")
        check(NAME4, not (one and len(sole) > 1),
              "" if not (one and len(sole) > 1) else
              ("every instrument the arsenal publishes declares one byte-identical `resources` block, "
               "and it is identical across the lean, standard and rich variants"
               + (" with `bytesEstimate` at nothing" if zero_bytes else "")
               + ". So no crossing declares a cost different from any other, the quality ladder "
                 "cannot be walked on what a crossing would cost, and PASS-API-V1's row 22 — a "
                 "resource declaration understating its bytes reds — has nothing to judge. Seven "
                 "numbers carried across the fleet unchanged read as twenty-seven independent "
                 "measurements agreeing"))

        # §2.5 bounds a transaction, and `kaleidoscope.js` names that bound in its own comment as
        # what its clock's span is. A clock published past it declares reach the transaction ends
        # before: unreachable by construction, on every pair, in either direction.
        clocks = fleet["clocks"]
        spans = sorted(set(clocks.values()))
        floor = spans[0] if spans else None
        odd = sorted(n for n in clocks if clocks[n] != floor)
        check(NAME5, not odd,
              "" if not odd else
              ("every clock handle in the fleet publishes a span ending at " + str(floor)
               + " seconds, which the fold's own manifest names as §2.5's transaction bound, except: "
               + ", ".join("«" + n + "» at " + str(clocks[n]) for n in odd)
               + ". A transaction is over at its own bound, so the span above it cannot be reached "
                 "by any score on any pair — a published cap that says something false about the "
                 "module"))

# ---------------------------------------------------------------- report
print("EX-PASS · shelf 21 over every named constant on the composition road")
for p in ROAD:
    print("  road: " + str(p))
print("")
worst = 0
for name, verdict, detail in results:
    print("  " + verdict.ljust(5) + " " + name)
    if detail:
        for ln in detail.split("\n"):
            print("        " + ln if not ln.startswith("        ") else ln)
    if verdict == "FAIL":
        worst = 1
print("")
print("  " + str(marked) + " named constants already carry a verdict, "
      + str(len(unmarked)) + " do not")
print("  " + str(sum(1 for r in results if r[1] == "PASS")) + " pass, "
      + str(sum(1 for r in results if r[1] == "FAIL")) + " fail, "
      + str(sum(1 for r in results if r[1] == "SKIP")) + " skip")
sys.exit(worst)
