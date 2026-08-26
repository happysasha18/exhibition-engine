#!/usr/bin/env python3
"""EX-PASS — the palette rung: a field whose definition is a statistic over the collection, read by
the composer to decide a crossing.

Run: python3 tests/test_pass_palette.py

The repair these rows judge is designed in docs/design/PALETTE-RUNG.md. Every row below FAILS against
the tree as it stands and PASSES once the blocks in that document are applied. A green run before the
blocks land would be a defect in this file.

WHAT IS BROKEN.

  `palette.rung` names one of five steps on a tone-and-colour ladder. Four of the five steps are cut
  at the collection's own third quartile on their defining measure — the record builder's own
  `classify_tone` in the tlvphotos lab sorts every work's reading and takes the value standing at the
  top-quarter index. So which rung a photograph stands on is not a fact about that photograph: it is
  a statement about the other photographs it happened to be measured beside.

  `groundCandidates` in engine/assets/pass-composer.js reads that name as a GATE — the share of hues
  two works have between them counts for nothing unless their two rung names are equal. Hanging one
  more picture on the wall can move an existing work's rung, close or open that gate, and change
  which ground two OTHER pictures cross on, neither of them the picture that was hung. Charter
  shelf 20 forbids exactly that: no statistic over the collection may decide any behaviour of the
  engine. This is that, at the source rather than in a comment.

  The same expression breaks a second law on its own account. An equality between two bucket names
  is a gate, and `dieWeighted` never rolls a candidate whose fit is nothing while any rival reads
  anything — so two works standing a hair apart on the ladder, in different buckets, have this ground
  REFUSED rather than ranked. Shelf 9's law and his word of 2026-08-18 09:51: a measurement ranks and
  never admits.

WHAT THE ROWS ASK.

  Row 1 is the law itself, behaviourally: a crossing between two pictures may not move when a field
  that only the rest of the collection decides is moved. It holds two records fixed and walks the
  rung name through the whole five-by-five space of what the two records could be labelled, and asks
  for one score.

  Row 2 is the second half: the reading must rank. A pair that shares its hues outright and stands in
  one place in colour space must be able to cross on the shared palette region. The row names the die
  that reaches it; where none does, that is the gate.

  Row 3 watches the producer, so the two sides cannot drift apart. It is a source row against the
  tlvphotos lab and it skips cleanly where that tree is not on the machine.

NO STATISTIC ANYWHERE. Row 1 walks a space and reports a witness, never a share. Row 2 is an
existence claim and names the die that satisfies it, or says no die did. The work records the rows
compose over are built here out of the fields' own definitions, each set inside its own declared
range, and no photograph is consulted for any of them.

NO CHROME. The composer runs under `node` in a `vm` sandbox, so this file contends with nothing.
"""
import ast
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import tokenize
from pathlib import Path


def _statements_of(source, name):
    """The statements a named function actually runs — no comments, no docstring.

    This row asks what `classify_tone` READS to decide a rung, and prose about the function is
    not the function. Both kinds of prose had to go: the note left behind to say what the rule
    used to be, and the docstring that explains the same history in the same words. Either one
    kept the row failing a repair that had already landed, which is a verdict about a sentence
    wearing the clothes of a verdict about code.

    Returns None where the function is not there, so the row can say it needs re-pinning rather
    than read an empty body and call it clean.
    """
    stripped = _without_comments(source)
    try:
        tree = ast.parse(stripped)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            stmts = node.body
            if (stmts and isinstance(stmts[0], ast.Expr)
                    and isinstance(stmts[0].value, ast.Constant)
                    and isinstance(stmts[0].value.value, str)):
                stmts = stmts[1:]
            parts = [ast.get_source_segment(stripped, s) or "" for s in stmts]
            return "\n".join(parts)
    return None


def _without_comments(source):
    """The source with its comments removed and every line's own length kept.

    A row that reads code must read the code. Blanking a comment in place rather than deleting
    the line keeps every line number and every indent exactly where it stood, so the function
    body this row extracts afterwards is the same body, minus the prose about it. Where the file
    cannot be tokenised the text is handed back whole: a row that cannot read honestly says what
    it found rather than quietly reading less.
    """
    try:
        lines = source.splitlines(keepends=True)
        cuts = {}
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.COMMENT:
                row, col = tok.start
                cuts[row] = min(col, cuts.get(row, col))
        for row, col in cuts.items():
            line = lines[row - 1]
            tail = "\r\n" if line.endswith("\r\n") else ("\n" if line.endswith("\n") else "")
            lines[row - 1] = line[:col].rstrip() + tail
        return "".join(lines)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return source

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"
# The record builder lives in the other tree and is read, never run and never written.
LAB = Path("/Users/sashaabramovich/tlvphotos/lab/step1-tone-texture.py")

# The ladder's five steps, in the record builder's own order. They are a vocabulary, not a
# measurement, and this file only ever uses them as labels to move.
RUNGS = ["чёрно-белое", "тонировка", "дутон", "ограниченный цвет", "полный цвет"]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const [modulePath, fixturePath] = process.argv.slice(2);
const job = JSON.parse(process.env.JOB || "{}");

const source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
const fixRaw = fs.readFileSync(fixturePath, "utf8");

// Each instrument's own declared levels, read off the instrument's own file rather than off the
// frozen fixture, which predates the declaration.
const live = {};
{
  const assetsDir = path.dirname(modulePath);
  for (const f of fs.readdirSync(assetsDir).filter((n) => /^pass-inst-.*\.js$/.test(n))) {
    const isrc = fs.readFileSync(path.join(assetsDir, f), "utf8").replace(/@@NS@@/g, "");
    const sb = {window: {__PassInstrument: (r) => { live[r.instrument.name] = r.instrument.manifest; }},
                console, document: undefined};
    vm.createContext(sb);
    try { vm.runInContext(isrc, sb, {filename: f}); } catch (e) { /* an instrument that needs a DOM */ }
  }
}
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
const fix = JSON.parse(fixRaw);
Object.keys(fix.consts.manifests).forEach(function (iid) {
  if (live[iid] && live[iid].levels) fix.consts.manifests[iid].levels = live[iid].levels;
});
const composer = joined.make(fix.consts);

// A WORK RECORD BUILT FROM THE FIELDS' OWN DEFINITIONS. Every value sits inside the range its own
// field declares and none of them is read off a photograph, so what the rows claim about these two
// records is a claim about the arithmetic that reads them.
function built(id, palette, tune) {
  const r = {
    id: id, frameSide: 1440.0,
    colour: {brightness: 0.5, contrast: 0.4, sat: 0.4},
    luminance: {level: 0.5},
    palette: palette,
    measures: {banding: 0.5, dominant_object: 0.2, grid: 0.3, named_objects: 0.3,
               radial: 0.3, regions: 0.5, texture: 0.4},
    motifs: {gateAxis: "horizontal", gateGap: 0.1, gateHalf: 0.02, gatePlace: 0.5,
             gateScore: 0.1, radialCentre: [0.5, 0.5], voidShare: 0.4, measured: []},
    readiness: [0.5, 200.0, "horizontal"],
    door: {angleDeg: 0, device: "rings", elementKind: "ring", level: "CELL",
           pieces: 8.0, stepPx: 120.0},
    structure: {grid: {periodPx: 90.0, angleDeg: 0.0, score: 0.3},
                ownDevice: {stepPx: 120.0, angleDeg: 0.0, kind: "rings"},
                radial: {score: 0.3, subType: "ring"},
                rotational: {n: 2, score: 0.3},
                horizon: {y: 0.5, seam: 0.3},
                polar: {twirl: 0.2},
                banding: {periodPx: 100.0, score: 0.4},
                dominantObject: {bbox: [0.3, 0.3, 0.4, 0.4]},
                regions: {score: 0.5}},
    texture: {reliefEdge: 0.3, reliefCentreMassX: 0.5, scoreFromCutLines: 0.4,
              spectralPeriodPx: 60.0},
    sets: [{kind: "band", index: 0, count: 4, realCount: 4, measuredGrain: 4.0, mergeFactor: 1.0,
            fig: null, provider: "structural"},
           {kind: "region", index: 1, count: 6, realCount: 6, measuredGrain: 6.0, mergeFactor: 1.0,
            fig: null, provider: "hybrid"},
           {kind: "panel", index: 2, count: 5, realCount: 5, measuredGrain: 5.0, mergeFactor: 1.0,
            fig: 0, provider: "structural"},
           {kind: "ring", index: 3, count: 8, realCount: 8, measuredGrain: 8.0, mergeFactor: 1.0,
            fig: null, provider: "structural"},
           {kind: "strip", index: 4, count: 4, realCount: 4, measuredGrain: 200.0,
            mergeFactor: 1.0, fig: 1, provider: "structural"},
           {kind: "tile", index: 5, count: 16, realCount: 16, measuredGrain: 16.0,
            mergeFactor: 1.0, fig: 3, provider: "structural"},
           {kind: "scale", index: 6, count: 5, realCount: 5, measuredGrain: 5.0, mergeFactor: 1.0,
            fig: null, provider: "fallback"},
           {kind: "wedge", index: 7, count: 6, realCount: 6, measuredGrain: 6.0, mergeFactor: 1.0,
            fig: null, provider: "structural"},
           {kind: "field", index: 8, count: 1, realCount: 1, measuredGrain: 0.0, mergeFactor: 1.0,
            fig: null, provider: "fallback"}]
  };
  (tune || []).forEach(function (t) {
    let at = r, i;
    for (i = 0; i < t[0].length - 1; i++) at = at[t[0][i]];
    at[t[0][t[0].length - 1]] = t[1];
  });
  return r;
}
// THE PALETTE BLOCK, spelled out per row. `colourfulness` is the ladder's OWN CONTINUOUS
// COORDINATE and it already ships: the record builder writes `tone.ladder_position` into it, which
// is half how much colour is present (the chroma at the coloured end of the frame against a fixed
// perceptual anchor) and half how wide it is spread (the normalised entropy of the work's own hue
// histogram). Both halves are read off one picture's own pixels and both are 0 at grey and 1 at a
// frankly polychrome frame, so the coordinate is in [0, 1] by construction. The rows that set it and
// the rows that leave it out both matter: a record that does not carry it must still compose.
function palette(hues, rung, world) {
  const p = {hueConcentration: 0.6, hues: hues, rung: rung};
  if (world !== null && world !== undefined) p.colourfulness = world;
  return p;
}

function out(v) { console.log(JSON.stringify(v)); }

// ---------------------------------------------------------------- job: stability
//
// ONE PAIR, EVERY LABEL THE COLLECTION COULD HANG ON IT. The two records are fixed; only the two
// rung names move, through all twenty-five ways the ladder could name them. Every one of the
// twenty-five must compose the same score, because none of the twenty-five is a fact about either
// photograph.
if (job.job === "stability") {
  const rungs = job.rungs;
  const worldA = job.world === null ? null : job.world[0];
  const worldB = job.world === null ? null : job.world[1];
  let witness = null, base = null;
  // EVERY DIE THE ROW WALKS, because the claim is about the crossing and not about one roll: a
  // labelling that moves the ground moves it for the dice that were landing on that ground, and
  // which dice those are is the die's own business. The row fails on the first die that moves.
  for (let s = 0; s < job.dice && witness === null; s++) {
    let here = null;
    for (let i = 0; i < rungs.length; i++) {
      for (let j = 0; j < rungs.length; j++) {
        const a = built("world-a", palette(["blue", "green"], rungs[i], worldA));
        const b = built("world-b", palette(["blue", "green", "cyan"], rungs[j], worldB));
        const p = composer.passageFor({workRecordA: a, workRecordB: b, direction: "a-to-b",
                                       seed: s, routeRole: "middle"});
        if (!p.score) { out({error: "the constructed pair composed nothing"}); process.exit(0); }
        const one = {json: p.json, ground: p.plan.pivot.kind, family: p.family,
                     rungs: [rungs[i], rungs[j]], die: s};
        if (here === null) { here = one; continue; }
        if (one.json !== here.json) { base = here; witness = one; break; }
      }
      if (witness !== null) break;
    }
  }
  out({base: base === null ? null : {ground: base.ground, family: base.family,
                                     rungs: base.rungs, die: base.die},
       witness: witness === null ? null : {ground: witness.ground, family: witness.family,
                                           rungs: witness.rungs, die: witness.die}});
  process.exit(0);
}

// ---------------------------------------------------------------- job: reach
//
// CAN THIS PAIR CROSS ON THE GROUND IT PLAINLY STANDS ON? Both works name the same two hues and sit
// at the same place in colour space. The dice are walked in order and the first that reaches the
// shared palette region is named. A ground whose fit is nothing is never rolled while any rival
// reads anything, so a search that finds no die has found the gate rather than an unlucky roll.
if (job.job === "reach") {
  const a = built("reach-a", palette(job.huesA, job.rungA, job.world));
  const b = built("reach-b", palette(job.huesB, job.rungB, job.world));
  let at = null;
  for (let s = 0; s < job.dice; s++) {
    const p = composer.passageFor({workRecordA: a, workRecordB: b, direction: "a-to-b",
                                   seed: s, routeRole: "middle"});
    if (p.score && p.plan.pivot.kind === "shared-palette-region") { at = s; break; }
  }
  out({at: at, dice: job.dice});
  process.exit(0);
}

out({error: "no job named"});
"""

TMP = Path(tempfile.mkdtemp(prefix="pass_palette_"))
DRIVER_PATH = TMP / "palette-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def run(job):
    env = dict(os.environ, JOB=json.dumps(job))
    proc = subprocess.run(["node", str(DRIVER_PATH), str(MODULE), str(FIXTURE)],
                          capture_output=True, text=True, env=env, timeout=900)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-500:]}
    line = (proc.stdout or "").strip().splitlines()
    if not line:
        return {"error": "the driver said nothing"}
    return json.loads(line[-1])


NODE = node_available()
NAME1 = "PALETTE · a crossing does not move when only the rung name moves"
NAME2 = "PALETTE · the shared palette region is ranked, never gated on a rung name"
NAME3 = "PALETTE · the rung is named from one picture's own readings"

# ---------------------------------------------------------------- row 1
if not NODE:
    skip(NAME1, "node is not on this machine")
else:
    # Walked twice: once on records that carry the ladder's own coordinate, once on records built
    # before that field exists. Both must be stable, because neither the name nor its absence is a
    # fact the crossing may read.
    worst = None
    for label, world in (("carrying the ladder's own coordinate", [0.42, 0.47]),
                         ("not carrying the ladder's own coordinate", None)):
        r = run({"job": "stability", "rungs": RUNGS, "dice": 24, "world": world})
        if r.get("error"):
            worst = {"error": r["error"], "label": label}
            break
        if r.get("witness") and worst is None:
            worst = {"label": label, "base": r["base"], "witness": r["witness"]}
    if worst and worst.get("error"):
        check(NAME1, False, worst["error"])
    else:
        check(NAME1, worst is None,
              "" if worst is None else
              ("on records " + worst["label"] + ", at die " + str(worst["base"]["die"])
               + ", labelling the two works «"
               + worst["base"]["rungs"][0] + "» and «" + worst["base"]["rungs"][1]
               + "» crosses them on the «" + worst["base"]["ground"]
               + "» ground with family «" + str(worst["base"]["family"])
               + "», and labelling the same two works «"
               + worst["witness"]["rungs"][0] + "» and «"
               + worst["witness"]["rungs"][1] + "» crosses them on «"
               + worst["witness"]["ground"] + "» with family «"
               + str(worst["witness"]["family"]) + "». Neither label is a reading of either "
               "photograph: the ladder's four coloured steps are cut at the collection's own top "
               "quarter, so hanging one more picture can move a label and move this crossing"))

# ---------------------------------------------------------------- row 2
if not NODE:
    skip(NAME2, "node is not on this machine")
else:
    DICE = 160
    same = run({"job": "reach", "huesA": ["blue", "green"], "huesB": ["blue", "green"],
                "rungA": RUNGS[2], "rungB": RUNGS[2], "world": 0.45, "dice": DICE})
    apart = run({"job": "reach", "huesA": ["blue", "green"], "huesB": ["blue", "green"],
                 "rungA": RUNGS[2], "rungB": RUNGS[1], "world": 0.45, "dice": DICE})
    if same.get("error") or apart.get("error"):
        check(NAME2, False, same.get("error") or apart.get("error"))
    elif same.get("at") is None:
        skip(NAME2, "the pair that shares its hues outright never reached the shared palette region "
                    "under either labelling, so the row had nothing to compare")
    else:
        check(NAME2, apart.get("at") is not None,
              "" if apart.get("at") is not None else
              ("two works naming the same two hues and standing at the same place in colour space "
               "cross on the shared palette region at die " + str(same["at"])
               + " when the ladder happens to label them alike, and no die reaches that ground when "
               "the ladder labels them one step apart. A fit of nothing is never rolled while any "
               "rival reads anything, so the equality of two bucket names is a gate, and shelf 9's "
               "law is that a measurement ranks and never admits"))

# ---------------------------------------------------------------- row 3
#
# THE PRODUCER'S OWN SIDE, and it can only be written against source text: what is wrong there is
# not what the function returns for one work but what it READS to decide, and a value already
# baked into a record carries no trace of the set it was decided against. The row therefore asks
# whether `classify_tone` reads the set at all.
if not LAB.exists():
    skip(NAME3, "the record builder's tree is not on this machine, so the producer side is "
                "unwatched here; the row arms itself wherever that tree stands")
else:
    # READ THE CODE, NEVER THE PROSE ABOUT THE CODE. This row looks for three shapes in the
    # function's own text, and a comment naming a shape is not the shape: once the cuts moved onto
    # absolute anchors, the note left behind to say what the rule USED to be still carried the word
    # `sorted()`, and the row went on failing a repair that had landed. A verdict anchored on
    # comment text answers about the comment. Comments are stripped by the tokenizer rather than by
    # a pattern, so a `#` inside a string cannot be mistaken for one.
    body = _statements_of(LAB.read_text(encoding="utf-8"), "classify_tone")
    if body is None:
        check(NAME3, False, "`classify_tone` was not found in " + str(LAB)
                            + "; the producer may have been renamed and this row needs re-pinning")
    else:
        # A threshold decided against the set is one of three shapes, all of them present today: a
        # quantile helper, a sort over the records the function was handed, or an index into such a
        # sort. None of the three can be written without the other photographs.
        reads = []
        if re.search(r"\bq75\b", body):
            reads.append("a quantile helper over the records it was handed")
        if re.search(r"sorted\s*\(", body):
            reads.append("a sort over the records it was handed")
        if re.search(r"\bq_index\b", body):
            reads.append("an index into the collection's own sorted readings")
        check(NAME3, not reads,
              "" if not reads else
              ("`classify_tone` decides its cuts by " + " and ".join(reads) + " ("
               + str(LAB) + "). Four of the ladder's five steps are therefore cut at the "
               "collection's own top quarter, so the step a photograph stands on is a statement "
               "about the other photographs it was measured beside. Every measure the cut is taken "
               "on is already absolute and already per-work — CIELAB chroma, a normalised "
               "entropy, a correlation, a resultant length — and the file already carries "
               "absolute anchors for all four under NAIVE"))

# ---------------------------------------------------------------- report
print("EX-PASS · the palette rung")
print("composer: " + str(MODULE))
print("producer: " + str(LAB) + ("" if LAB.exists() else "   (not on this machine)"))
print("")
worst = 0
for name, verdict, detail in results:
    print("  " + verdict.ljust(5) + " " + name)
    if detail:
        for ln in detail.split("\n"):
            print("        " + ln)
    if verdict == "FAIL":
        worst = 1
print("")
print("  " + str(sum(1 for r in results if r[1] == "PASS")) + " pass, "
      + str(sum(1 for r in results if r[1] == "FAIL")) + " fail, "
      + str(sum(1 for r in results if r[1] == "SKIP")) + " skip")
sys.exit(worst)
