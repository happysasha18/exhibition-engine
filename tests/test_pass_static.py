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
const shapes = {}, clocks = {}, cuts = {}, seams = {}, handles = {};
names.forEach(function (n) {
  const m = live[n];
  const key = JSON.stringify(m.resources || {});
  (shapes[key] = shapes[key] || []).push(n);
  const c = (m.handles || {}).clock;
  if (c) clocks[n] = c.max;
  cuts[n] = m.cuts || [];
  seams[n] = m.seams || null;
  handles[n] = Object.keys(m.handles || {});
});
console.log(JSON.stringify({names: names, failed: failed, shapes: shapes, clocks: clocks,
                            cuts: cuts, seams: seams, handles: handles}));
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

        # ------------------------------------------------- rows 6 and 7: every seam is declared
        #
        # An instrument that cuts the frame has a boundary a picture cannot help but have, and three
        # of them — kaleidoscope, planet, tunnel — rounded that boundary by hand, with a typed number
        # no reader outside the file could find. §8's `seams` block is the repair: an instrument
        # DECLARES where it has a seam (a line, a wedge, a ring, a tile, an isoline) and what measure
        # sets that seam's own width, so a reader — and the host, which answers the width — finds it
        # in one place rather than by reading every shader.
        #
        # WHO THIS ROW HOLDS TO THE FIELD, AND WHY IT IS EVERYONE. It used to be the instruments whose
        # own `cuts` block is non-empty, PLUS eight more named here by hand because their headers
        # describe a cut their manifests never publish. That union was exactly the set of files that
        # already complied, so the three that did not — `liquid`, `matter`, `overlay` — published no
        # `cuts` block, stood in no list, and were exempt BY CONSTRUCTION: the row could not have
        # caught them, and it did not. A gate whose population is drawn from the files that pass it
        # is not a gate. So the population is now THE WHOLE FLEET, every instrument the registry
        # loads, and the question each is asked is the one a reader actually needs answered: where
        # does this instrument cut, and how wide is that cut held? An instrument with no boundary of
        # its own answers `seams: []` and says why in its own file — five did so before this row
        # changed (adrift, livemirror, pour, strata-light, strata-scale) and that is the pattern.
        # Silence is no longer one of the answers available.
        #
        # WHAT ELSE IS HELD. A declaration must be a list. Every entry must name a `kind` and a
        # `unit`, and the unit must be one of the exactly two the host distinguishes — a misspelt
        # unit does not fail loudly, it falls into the handover branch of `seamsOf` and silently
        # draws a share of a repeat where a hairline was meant. An entry naming a handle in `of` must
        # name one this instrument actually publishes, so a seam cannot claim to be set by a
        # measurement nobody can drive.
        NAME6 = "STATIC · every instrument in the fleet declares where it cuts the frame"
        UNITS = {"points of the drawing buffer", "a share of one repeat's own span"}

        def seam_verdict(f):
            """The row's own predicate, held apart so the red-on-bug run below is judged by the very
            code the live run is judged by rather than by a second description of it."""
            seams_of, handles_of = f.get("seams", {}), f.get("handles", {})
            gone, bad = [], []
            for name in sorted(f["names"]):
                decl = seams_of.get(name)
                if decl is None:
                    gone.append(name)
                    continue
                if not isinstance(decl, list):
                    bad.append(name + ": `seams` is not a list")
                    continue
                own = set(handles_of.get(name, []))
                for entry in decl:
                    if not isinstance(entry, dict) or "kind" not in entry or "unit" not in entry:
                        bad.append(name + ": a seam entry names no `kind` or no `unit`")
                        continue
                    if entry["unit"] not in UNITS:
                        bad.append(name + ": a seam names the unit «" + str(entry["unit"])
                                   + "», which is neither of the two the host reads")
                    if entry.get("of") is not None and entry["of"] not in own:
                        bad.append(name + ": a seam names `of: " + str(entry["of"])
                                   + "`, which is not one of its own published handles")
                    # A HAIRLINE MAY NAME NO HANDLE, and this is the host's own arithmetic rather
                    # than a preference. `seamsOf` reads the handle named in `of` into `count` and
                    # hands `count` to `seamHandoverOf` alone; `seamHairlineOf` takes no argument at
                    # all, because a hairline spends none of an element's own room and so does not
                    # shrink as that element repeats more often. A hairline naming a handle would
                    # therefore publish a dependence the host discards without a word — a sentence
                    # about the instrument that is false the moment it is read.
                    if (entry.get("of") is not None
                            and entry["unit"] == "points of the drawing buffer"):
                        bad.append(name + ": a hairline seam names `of: " + str(entry["of"])
                                   + "`, and the host's own hairline reading takes no count — only "
                                     "a handover's width is divided by one")
            return gone, bad

        seams_map = fleet.get("seams", {})
        handles_map = fleet.get("handles", {})
        expected = sorted(fleet["names"])
        missing6, malformed = seam_verdict(fleet)
        check(NAME6, not missing6 and not malformed,
              "" if not (missing6 or malformed) else
              ("every one of the " + str(len(expected)) + " instruments the registry loads is asked "
               "where it cuts the frame — a non-empty `manifest.seams` with a kind and a unit the "
               "host reads, or an empty list said outright with the reason in the file, which is "
               "what five of them already publish. No instrument is exempt by name or by what it "
               "leaves undeclared. "
               + ("declares nothing at all: " + ", ".join(missing6) + ". " if missing6 else "")
               + ("malformed: " + "; ".join(malformed) + "." if malformed else ""))
              )

        # ROW 7 IS THE OTHER DIRECTION, and it closes the way round the row above cannot see. An
        # instrument reads its width back off the pose the host hands it (`st.seams`), and a file
        # that reads one while its manifest declares none is spending a width nobody published: the
        # host answers `null` for an instrument with no declaration, the file silently falls back to
        # a private constant, and the declaration §8 exists for is gone again by another door.
        #
        # WHAT THIS ROW DOES NOT ASSERT, said outright rather than left as a silence. The reverse —
        # every DECLARED seam being read back — does not hold today and this row does not pretend it
        # does: most declarations still stand as paper, each instrument drawing its own softening in
        # its own shader. The count stands in this row's own words at every run, so it cannot rot
        # unnoticed, and the names are printed rather than summarised.
        NAME7 = "STATIC · no instrument reads a seam width the host was never asked for"
        readers, declared_names = [], []
        for n in expected:
            path = ROOT / "engine" / "assets" / ("pass-inst-" + n + ".js")
            body = path.read_text(encoding="utf-8") if path.exists() else ""
            if "st.seams" in body or "state.seams" in body:
                readers.append(n)
            if seams_map.get(n):
                declared_names.append(n)
        unpublished = sorted(set(readers) - set(declared_names))
        paper = sorted(set(declared_names) - set(readers))
        check(NAME7, not unpublished,
              ("these instruments read `st.seams` back at render time and their manifests declare "
               "no seam for the host to answer: " + ", ".join(unpublished) + ". "
               if unpublished else "")
              + str(len(readers)) + " of the " + str(len(declared_names))
              + " instruments declaring a seam read the host's own answer back and draw at it — "
              + ", ".join(readers) + ". The remaining " + str(len(paper))
              + " declare a seam and draw their own softening in their own shaders, so the "
                "declaration tells a reader where the boundary is and does not yet set its width: "
              + ", ".join(paper))

        # ---------------------------------------- row 8: the row above, run against a silent file
        #
        # WHY THIS ROW EXISTS. The row it guards was green for weeks while three instruments in this
        # very tree published no `seams` block at all, because its population was built as
        # «instruments declaring a cut» ∪ «eight names typed here», and that union was exactly the
        # set of files that already complied. The row was not wrong about the files it looked at; it
        # never looked at the others. So the repair cannot be judged by the repaired row coming out
        # green — a row that examines nobody comes out green too. It is judged by handing the SAME
        # predicate a fleet with one declaration taken out and watching it red.
        #
        # WHAT IS TAKEN OUT, and it is the exact shape of the defect this row was blind to: the
        # instrument keeps every other field, publishes no `cuts` block it did not publish before,
        # and simply does not mention `seams`. Under the old population it would have been exempt by
        # construction. The whole asset tree is copied and the copy is edited, so the file on disk is
        # never touched and no working tree can be left changed by a proof.
        NAME8 = "STATIC · the row above reds when an instrument declares no seam at all"
        SILENT = "veil"
        import shutil as _shutil
        mute = TMP / "silent-fleet"
        if mute.exists():
            _shutil.rmtree(mute)
        _shutil.copytree(ROOT / "engine" / "assets", mute)
        target = mute / ("pass-inst-" + SILENT + ".js")
        text = target.read_text(encoding="utf-8")
        cut = 'seams: [{ kind: "isoline", of: null, unit: "points of the drawing buffer" }],'
        if cut not in text:
            check(NAME8, False, "the plant found no declaration to take out of «" + SILENT + "»")
        else:
            target.write_text(text.replace(cut, "", 1), encoding="utf-8")
            muted = subprocess.run(["node", str(FLEET_PATH), str(mute)],
                                   capture_output=True, text=True, timeout=300)
            if muted.returncode != 0:
                check(NAME8, False, (muted.stderr or "").strip()[-400:])
            else:
                bug = json.loads(muted.stdout.strip().splitlines()[-1])
                gone, bad = seam_verdict(bug)
                check(NAME8,
                      gone == [SILENT] and not bad and not missing6 and len(bug["names"]) == len(expected),
                      "with «" + SILENT + "»'s own declaration taken out of a copy of the asset tree "
                      "— every other field of its manifest left standing, and no `cuts` block added "
                      "or removed — the same predicate that passes the shipped fleet names it: "
                      + (", ".join(gone) if gone else "nobody") + ". It stands over the same "
                      + str(len(bug["names"])) + " instruments either way, so what changed is the "
                      "declaration and nothing about the population")
        _shutil.rmtree(mute, ignore_errors=True)

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
