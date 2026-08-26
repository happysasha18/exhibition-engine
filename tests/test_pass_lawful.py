#!/usr/bin/env python3
"""EX-PASS — four laws the passage composer breaks today, each row red until its repair lands.

Run: python3 tests/test_pass_lawful.py

The repairs these rows judge are designed in docs/design/COMPOSER-REPAIRS.md, R1 to R4. Every row
below FAILS against engine/assets/pass-composer.js as it stands and PASSES once the blocks in that
document are applied. A row that passes today would be proving nothing, so a green run before the
blocks land is itself a defect in this file.

WHAT EACH ROW STANDS ON.

  R1 — the accompaniment budget. Charter shelf 17 budgets a crossing by tier: a quiet tier one
  letter and at most one accompanying voice, a middle at most two of each, a culmination two or
  three letters and at most three accompanying voices, with the camera counted as one accompaniment
  before a single cue is counted (PASS-API-V1 §4.4, amended 2026-08-14 10:31). PASS-API-V1 §4.7:
  "The declared tier and the measured one must agree ... Neither value silently wins." The row asks
  one question of every composed passage — do the plan's declared tier and the score's own voice
  counts satisfy the same row of shelf 17 — and it is a UNIVERSAL claim, never a tally: it names one
  witness passage and never how many there were.

  R2 — atomicity. A score is weighed after the last field that will ever be written to it, or not at
  all. `scoreFor` weighs the score and computes `overTheFence`; `passageFor` then writes
  `score.camera.lead` onto it. The row holds the published reading against the score that was
  actually handed back.

  R3 — the clock inside the die. PASS-API-V1 §4.4g: the die is made of the visit's seed, the pass
  index and the edge's key, "so there is one idea of a seed and no clock in either"; conformance row
  10 is that a seeded run repeats to the pixel. The composer calls `new Date()` inside the weight
  that ranks every ground candidate, and reads the LOCAL hour, so one seeded request composes
  differently across an hour boundary and differently again on a machine set to another timezone.

  R4 — charter shelf 20. No statistic over the collection of photographs may justify any behaviour
  of the engine or any claim about it, "in code, in comments, in documents, in tests, and in
  anything reported to him". The row reads the composer's own source and the contract's own text and
  reds on every place a tally over the collection stands as an argument. It is the one row here that
  can only be written against SOURCE TEXT rather than against behaviour, and it names line numbers
  and the enclosing rule alone — it never prints the tally it found, because printing it would break
  the same shelf inside this file.

WHAT THIS FILE NEVER DOES. It never reports a count, a share or a percentage of the collection; the
real per-work records are read as a SMOKE input under shelf 20's one lawful use — a check that the
code runs and writes plausible output on real records — and never as coverage. Where a row can name
a witness it names one, by id.

NO CHROME. Every behavioural row runs the composer under `node` in a `vm` sandbox, exactly as the
driver in tests/test_pass_composed.py does, so this file contends with nothing.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
CONTRACT = ROOT / "docs" / "design" / "PASS-API-V1.md"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"
WORKS = ROOT / "tests" / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the node driver
#
# One driver, four jobs. The composer is loaded into a fresh `vm` context per job so a job that
# stubs the clock cannot leak into one that does not.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const [modulePath, fixturePath, worksPath] = process.argv.slice(2);
const job = JSON.parse(process.env.JOB || "{}");

const rawSource = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
const fixRaw = fs.readFileSync(fixturePath, "utf8");

// EACH INSTRUMENT'S OWN DECLARED LEVELS, read off the instrument's own file rather than off the
// frozen fixture, which predates the declaration. Same road tests/test_pass_composed.py's driver
// takes, and for the same reason: the manifest is the one home of that fact.
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

// A CLOCK THAT CAN BE STOOD STILL AND MOVED. `atMs` fixes the instant; `offsetMin` is what the
// machine's own timezone would add to the LOCAL getters. Both are only ever set by the R3 rows;
// every other job runs on the real clock.
function makeContext(atMs, offsetMin, plants, fenceBytes) {
  let source = rawSource;
  const missed = [];
  for (const [from, to] of (plants || [])) {
    if (source.indexOf(from) < 0) { missed.push(from); continue; }
    source = source.split(from).join(to);
  }
  let joined = null;
  const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
  if (atMs !== null && atMs !== undefined) {
    const Real = Date;
    const shift = (offsetMin || 0) * 60000;
    function Stood(...a) {
      const d = a.length === 0 ? new Real(atMs) : new Real(...a);
      const local = new Real(d.getTime() + shift);
      return new Proxy(d, {get(t, k) {
        if (k === "getHours") return () => local.getUTCHours();
        if (k === "getMinutes") return () => local.getUTCMinutes();
        if (k === "getFullYear") return () => local.getUTCFullYear();
        if (k === "getMonth") return () => local.getUTCMonth();
        if (k === "getDate") return () => local.getUTCDate();
        const v = t[k];
        return typeof v === "function" ? v.bind(t) : v;
      }});
    }
    Stood.prototype = Real.prototype;
    Stood.UTC = Real.UTC;
    Stood.now = () => atMs;
    sandbox.Date = new Proxy(Stood, {construct: (T, a) => Stood(...a)});
  }
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
  if (!joined) return {error: "the module joined nothing"};
  const fix = JSON.parse(fixRaw);
  Object.keys(fix.consts.manifests).forEach(function (iid) {
    if (live[iid] && live[iid].levels) fix.consts.manifests[iid].levels = live[iid].levels;
    if (live[iid] && live[iid].handles) {
      Object.keys(live[iid].handles).forEach(function (h) {
        if (fix.consts.manifests[iid].handles[h] && live[iid].handles[h].level !== undefined) {
          fix.consts.manifests[iid].handles[h].level = live[iid].handles[h].level;
        }
      });
    }
  });
  if (fenceBytes) fix.consts.scoreFenceBytes = fenceBytes;
  return {composer: joined.make(fix.consts), fence: fix.consts.scoreFenceBytes, missed: missed};
}

// ---- the records the rows compose over ----
//
// TWO SOURCES, AND THE FIRST IS BUILT HERE FROM THE FIELDS' OWN DEFINITIONS. `built()` writes a
// record out of the fields the composer reads, each set to a value inside that field's own declared
// range — no photograph is consulted for any of them. The second source is the real per-work records
// the settings record ships, read as a SMOKE input under shelf 20's one lawful use.
function built(id, tune) {
  const r = {
    id: id, frameSide: 1440.0,
    colour: {brightness: 0.5, contrast: 0.4, sat: 0.4},
    luminance: {level: 0.5},
    palette: {colourfulness: 0.5, hueConcentration: 0.6, hues: ["blue"], rung: "rung-one"},
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
// A HANDFUL OF CONSTRUCTED RECORDS, each moving ONE field across its own range. Nothing here is
// read off a photograph, so what the rows below claim about them is a claim about the arithmetic.
const BUILT = [
  built("built-plain", []),
  built("built-dark", [[["luminance", "level"], 0.1], [["colour", "brightness"], 0.15]]),
  built("built-light", [[["luminance", "level"], 0.92], [["colour", "brightness"], 0.9]]),
  built("built-coarse", [[["structure", "grid", "periodPx"], 300.0],
                         [["door", "stepPx"], 300.0], [["door", "pieces"], 3.0]]),
  built("built-fine", [[["structure", "grid", "periodPx"], 20.0],
                       [["door", "stepPx"], 20.0], [["door", "pieces"], 40.0]]),
  built("built-turned", [[["structure", "rotational", "n"], 6],
                         [["structure", "rotational", "score"], 0.8],
                         [["measures", "radial"], 0.8]]),
  built("built-hued", [[["palette", "hues"], ["red", "orange", "yellow"]],
                       [["palette", "rung"], "rung-two"]])
];

const ROLES = ["entrance", "quiet link", "middle", "culmination", "return"];
// Charter shelf 17's three rows, in the shape the composer's own `TIERS` carries them. They are the
// shelf's own numbers, not a fourth copy: the row below reads them from the module where it can.
const SHELF17 = {quiet: {letters: [1, 1], accompaniments: [0, 1], miracles: [0, 0]},
                 middle: {letters: [0, 2], accompaniments: [0, 2], miracles: [0, 1]},
                 culmination: {letters: [2, 3], accompaniments: [0, 3], miracles: [1, 1]}};

// THE COUNTS, READ OFF THE SCORE THE HOST WOULD ACTUALLY PLAY. `voice` per cue, the camera as one
// accompaniment before a single cue is counted, and the LIGHT-COLOUR voice once however many
// handles carry it — which is exactly what §4.4's own budget check reads.
function countsOf(score) {
  let letters = 0, accs = 1, miracles = 0, colour = false;
  (score.cues || []).forEach(function (c) {
    if (c.voice === "letter") letters += 1;
    else if (c.voice === "accompaniment") accs += 1;
    else if (c.voice === "miracle") miracles += 1;
    if ((c.levels || []).indexOf("LIGHT-COLOUR") >= 0) colour = true;
  });
  if (colour) accs += 1;
  return {letters: letters, accompaniments: accs, miracles: miracles};
}
function holdsItsRow(tier, c) {
  const r = SHELF17[tier];
  if (!r) return null;
  return c.letters >= r.letters[0] && c.letters <= r.letters[1]
      && c.accompaniments >= r.accompaniments[0] && c.accompaniments <= r.accompaniments[1]
      && c.miracles >= r.miracles[0] && c.miracles <= r.miracles[1];
}

function* pairsOf(records) {
  for (let i = 0; i < records.length; i++) {
    for (let j = 0; j < records.length; j++) {
      if (i !== j) yield [records[i], records[j]];
    }
  }
}

const worksFile = JSON.parse(fs.readFileSync(worksPath, "utf8"));
const realIds = Object.keys(worksFile.works).sort();
// A SMOKE HANDFUL, taken in the file's own order and never chosen for what it would show.
const REAL = realIds.slice(0, 8).map((k) => worksFile.works[k]);

function out(v) { console.log(JSON.stringify(v)); }

// ---------------------------------------------------------------- job: r1
if (job.job === "r1") {
  const ctx = makeContext(null, 0, job.plants);
  if (ctx.error) { out({error: ctx.error}); process.exit(0); }
  if ((ctx.missed || []).length) { out({missed: ctx.missed}); process.exit(0); }
  const answer = {built: null, real: null, threw: null};
  [["built", BUILT], ["real", REAL]].forEach(function (src) {
    for (const [a, b] of pairsOf(src[1])) {
      for (const role of ROLES) {
        let p;
        try {
          p = ctx.composer.passageFor({workRecordA: a, workRecordB: b, direction: "a-to-b",
                                       seed: 7, routeRole: role});
        } catch (e) {
          if (!answer.threw) answer.threw = {a: a.id, b: b.id, role: role, why: String(e.message)};
          continue;
        }
        if (!p || !p.score) continue;
        const tier = p.plan ? p.plan.tier : null;
        const c = countsOf(p.score);
        if (holdsItsRow(tier, c) === false && !answer[src[0]]) {
          answer[src[0]] = {a: a.id, b: b.id, role: role, declaredTier: tier, counts: c,
                            cues: (p.score.cues || []).map(
                              (x) => [x.id, x.instrument.id, x.voice, (x.levels || []).join("+")])};
        }
      }
    }
  });
  out(answer);
  process.exit(0);
}

// ---------------------------------------------------------------- job: r2
if (job.job === "r2") {
  const ctx = makeContext(null, 0, job.plants);
  if (ctx.error) { out({error: ctx.error}); process.exit(0); }
  if ((ctx.missed || []).length) { out({missed: ctx.missed}); process.exit(0); }
  const w = ctx.composer;
  const answer = {weight: null, text: null, fence: null, ledSeen: false};
  for (const [a, b] of pairsOf(BUILT.concat(REAL))) {
    for (const role of ROLES) {
      let p;
      try {
        p = w.passageFor({workRecordA: a, workRecordB: b, direction: "a-to-b", seed: 5,
                          routeRole: role});
      } catch (e) { continue; }
      if (!p || !p.score) continue;
      if (p.score.camera && p.score.camera.lead === true) answer.ledSeen = true;
      const tight = w.writeJsonTight(p.score).length;
      const text = w.writeJson(p.score, 0);
      if (p.bytes !== tight && !answer.weight) {
        answer.weight = {a: a.id, b: b.id, role: role, published: p.bytes, actual: tight};
      }
      if (p.json !== text && !answer.text) {
        answer.text = {a: a.id, b: b.id, role: role,
                       publishedHasLead: p.json.indexOf('"lead"') >= 0,
                       scoreHasLead: !!(p.score.camera && p.score.camera.lead)};
      }
    }
  }
  out(answer);
  process.exit(0);
}

// ---------------------------------------------------------------- job: r2 fence
//
// THE DAY THE FENCE IS A WALL AGAIN. Today the client reads the weight and lets the passage play,
// so a wrong reading costs a lying diagnostic. This job asks what the same defect costs when the
// number decides: the fence is set one byte under the weight of the score that is actually handed
// back, so a truthful composer sheds prose and says so, and a composer that weighed the score
// before its last field says the score fits when it does not.
if (job.job === "r2fence") {
  const wide = makeContext(null, 0, job.plants, 4000000);
  if (wide.error) { out({error: wide.error}); process.exit(0); }
  if ((wide.missed || []).length) { out({missed: wide.missed}); process.exit(0); }
  let found = null;
  for (const [a, b] of pairsOf(BUILT.concat(REAL))) {
    for (const role of ["quiet link", "return"]) {
      let p;
      try {
        p = wide.composer.passageFor({workRecordA: a, workRecordB: b, direction: "a-to-b",
                                      seed: 5, routeRole: role});
      } catch (e) { continue; }
      if (p && p.score && p.score.camera && p.score.camera.lead === true) {
        found = {a: a, b: b, role: role, tight: wide.composer.writeJsonTight(p.score).length};
        break;
      }
    }
    if (found) break;
  }
  if (!found) { out({none: true}); process.exit(0); }
  const tight = makeContext(null, 0, job.plants, found.tight - 1);
  const q = tight.composer.passageFor({workRecordA: found.a, workRecordB: found.b,
                                       direction: "a-to-b", seed: 5, routeRole: found.role});
  const actual = tight.composer.writeJsonTight(q.score).length;
  out({a: found.a.id, b: found.b.id, role: found.role, fence: found.tight - 1,
       published: q.overTheFence, publishedBytes: q.bytes, actualBytes: actual,
       actual: actual > found.tight - 1, shed: q.weightShed});
  process.exit(0);
}

// ---------------------------------------------------------------- job: r3
if (job.job === "r3") {
  const at = job.atMs, other = job.atMs + job.deltaMs;
  const one = makeContext(at, job.offsetA, job.plants);
  const two = makeContext(job.deltaMs ? other : at, job.offsetB, job.plants);
  if (one.error || two.error) { out({error: one.error || two.error}); process.exit(0); }
  if ((one.missed || []).length) { out({missed: one.missed}); process.exit(0); }
  const answer = {witness: null};
  for (const [a, b] of pairsOf(BUILT.concat(REAL))) {
    const req = {workRecordA: a, workRecordB: b, direction: "a-to-b", seed: 11,
                 routeRole: "middle"};
    let p, q;
    try { p = one.composer.passageFor(req); q = two.composer.passageFor(req); } catch (e) { continue; }
    if (!p || !q || !p.score || !q.score) continue;
    if (p.json !== q.json && !answer.witness) {
      answer.witness = {a: a.id, b: b.id, familyOne: p.family, familyTwo: q.family,
                        sameFamily: p.family === q.family,
                        bytesOne: p.bytes, bytesTwo: q.bytes};
    }
  }
  out(answer);
  process.exit(0);
}

out({error: "no job named"});
"""

TMP = Path(tempfile.mkdtemp(prefix="pass_lawful_"))
DRIVER_PATH = TMP / "lawful-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def run(job):
    env = dict(os.environ, JOB=json.dumps(job))
    proc = subprocess.run(["node", str(DRIVER_PATH), str(MODULE), str(FIXTURE), str(WORKS)],
                          capture_output=True, text=True, env=env, timeout=900)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-500:]}
    line = (proc.stdout or "").strip().splitlines()
    if not line:
        return {"error": "the driver said nothing"}
    return json.loads(line[-1])


NODE = node_available()

# ---------------------------------------------------------------- R1
if not NODE:
    skip("R1 · a plan never declares a tier its own voice counts contradict",
         "node is not on this machine")
    skip("R1 · the accompaniment ceiling is what shapes the crossing", "node is not on this machine")
else:
    r1 = run({"job": "r1"})
    if r1.get("error"):
        check("R1 · a plan never declares a tier its own voice counts contradict", False, r1["error"])
    else:
        witness = r1.get("built") or r1.get("real")
        detail = "" if witness is None else (
            "the plan declares «" + str(witness["declaredTier"]) + "» at role «" + witness["role"]
            + "» and its own voices count letters=" + str(witness["counts"]["letters"])
            + " accompaniments=" + str(witness["counts"]["accompaniments"])
            + " miracles=" + str(witness["counts"]["miracles"])
            + ", which shelf 17's «" + str(witness["declaredTier"]) + "» row does not take"
            + " — witness " + witness["a"] + " → " + witness["b"]
            + "; cues " + "; ".join("/".join(map(str, c)) for c in witness["cues"]))
        check("R1 · a plan never declares a tier its own voice counts contradict",
              witness is None, detail)

    # RED ON BUG. Once R1's block stands, taking the accompaniment ceiling back out of the loop's
    # own condition must put the row above back into the red. The plant names the text the block
    # introduces; before the block lands there is nothing to plant against and the row says so.
    # Both halves of R1-c, because the repair is the two together: the ceiling in the loop's own
    # condition, and the give-up that answers it. Restoring either alone leaves a lawful composer
    # that shapes the crossing by another road, and a plant that cannot tell those apart proves
    # nothing about which road it took.
    PLANT_R1 = [["colourVoice = !(singsHere && accs + 1 > accCeiling);", "colourVoice = true;"],
                ["&& accs + ((colourVoice && singsHere) ? 1 : 0) <= accCeiling", "&& true"]]
    probe = run({"job": "r1", "plants": PLANT_R1})
    if probe.get("missed"):
        skip("R1 · the accompaniment ceiling is what shapes the crossing",
             "R1's block is not applied yet, so there is no ceiling to remove; this row arms itself "
             "the moment the block lands")
    elif probe.get("error"):
        check("R1 · the accompaniment ceiling is what shapes the crossing", False, probe["error"])
    else:
        broke = probe.get("built") or probe.get("real")
        check("R1 · the accompaniment ceiling is what shapes the crossing", broke is not None,
              "" if broke is not None else
              "removing the accompaniment ceiling from the loop's own condition left the row above "
              "green, so that row is not what the ceiling holds up")

# ---------------------------------------------------------------- R2
if not NODE:
    skip("R2 · the published weight is the weight of the score handed back",
         "node is not on this machine")
    skip("R2 · the published text is the text of the score handed back",
         "node is not on this machine")
    skip("R2 · the fence reading answers for the score that exists", "node is not on this machine")
else:
    r2 = run({"job": "r2"})
    if r2.get("error"):
        for n in ("weight", "text", "fence"):
            check("R2 · " + n, False, r2["error"])
    else:
        if not r2.get("ledSeen"):
            skip("R2 · the published weight is the weight of the score handed back",
                 "no composed passage was camera-led over these records, so the row saw nothing "
                 "to judge")
        w = r2.get("weight")
        check("R2 · the published weight is the weight of the score handed back", w is None,
              "" if w is None else
              ("`bytes` says " + str(w["published"]) + " and the score handed back weighs "
               + str(w["actual"]) + " — witness " + w["a"] + " → " + w["b"] + " at «"
               + w["role"] + "»; the score was weighed before `camera.lead` was written to it"))
        t = r2.get("text")
        check("R2 · the published text is the text of the score handed back", t is None,
              "" if t is None else
              ("`json` " + ("carries" if t["publishedHasLead"] else "does not carry")
               + " the camera's own `lead` while the score handed back "
               + ("does" if t["scoreHasLead"] else "does not")
               + " — witness " + t["a"] + " → " + t["b"] + " at «" + t["role"] + "»"))
    fence = run({"job": "r2fence"})
    if fence.get("error"):
        check("R2 · the fence reading answers for the score that exists", False, fence["error"])
    elif fence.get("none"):
        skip("R2 · the fence reading answers for the score that exists",
             "no composed passage was camera-led over these records")
    else:
        check("R2 · the fence reading answers for the score that exists",
              fence["published"] == fence["actual"],
              "" if fence["published"] == fence["actual"] else
              ("with the client's fence standing one byte under the score's true weight, "
               "`overTheFence` says " + str(fence["published"]) + " and the score handed back "
               "weighs " + str(fence["actualBytes"]) + " against a fence of "
               + str(fence["fence"]) + "; `weightShed` names " + str(fence["shed"])
               + " — witness " + fence["a"] + " → " + fence["b"] + " at «" + fence["role"]
               + "». On the day the fence is a wall again this is a lost crossing"))

# ---------------------------------------------------------------- R3
HOUR = 3600000
# One fixed instant, named outright so this file carries no clock of its own either.
AT = 1787654400000  # 2026-08-25 12:00:00 UTC
if not NODE:
    skip("R3 · one seeded request composes one passage whatever the hour",
         "node is not on this machine")
    skip("R3 · one seeded request composes one passage whatever the machine's timezone",
         "node is not on this machine")
else:
    hour = run({"job": "r3", "atMs": AT, "deltaMs": HOUR, "offsetA": 0, "offsetB": 0})
    if hour.get("error"):
        check("R3 · one seeded request composes one passage whatever the hour", False, hour["error"])
    else:
        wit = hour.get("witness")
        check("R3 · one seeded request composes one passage whatever the hour", wit is None,
              "" if wit is None else
              ("one request at one pinned seed composes two different scores an hour apart"
               + " — witness " + wit["a"] + " → " + wit["b"]
               + "; the family a return is matched against reads «" + str(wit["familyOne"])
               + "» and «" + str(wit["familyTwo"]) + "»"
               + ("" if wit["sameFamily"] else ", which are not kin")))

    tz = run({"job": "r3", "atMs": AT, "deltaMs": 0, "offsetA": 0, "offsetB": 9 * 60})
    if tz.get("error"):
        check("R3 · one seeded request composes one passage whatever the machine's timezone",
              False, tz["error"])
    else:
        wit = tz.get("witness")
        check("R3 · one seeded request composes one passage whatever the machine's timezone",
              wit is None,
              "" if wit is None else
              ("one request at one pinned seed and one instant composes two different scores on two "
               "machines whose local hour differs — witness " + wit["a"] + " → " + wit["b"]
               + "; the family reads «" + str(wit["familyOne"]) + "» and «"
               + str(wit["familyTwo"]) + "». The viewer's timezone is an input from none of the "
               "three sources charter shelf 20 allows"))

# ---------------------------------------------------------------- R4
#
# THE ONE ROW THAT CAN ONLY BE WRITTEN AGAINST SOURCE TEXT, and it is said out loud. There is no
# behaviour to ask: a tally standing as an argument in a comment changes nothing the composer
# computes, which is exactly why nothing caught it. The patterns below read the SHAPES a tally over
# the collection takes in English prose. Two of them are deliberately narrow so a lawful sentence
# survives: a share of one work's own frame, a median of ONE work's own luminance, and a count of
# the instruments the arsenal publishes are all lawful and none of them matches.
#
# WHAT IS PRINTED WHEN IT REDS: the line number and the sentence's own opening words with every
# digit struck out. The tally itself is never printed, because printing it here would break shelf 20
# inside this file.
#
# A SENTENCE, NOT A LINE. A tally wrapped across two lines is the same tally, so the sweep joins
# each run of comment lines (and each paragraph of the contract) into one block and reads that.
NUM = "[0-9][0-9   ,.]*"
TALLY = [
    (re.compile(NUM + r"\s?(per ?cent|%)"), "a share of the collection said as a percentage"),
    (re.compile(r"\b(top |bottom )?(quartile|percentile|nine-tenths)\b"),
     "a quantile over the collection"),
    (re.compile(r"\bmedian of " + NUM), "a median over the collection"),
    (re.compile(NUM + r"of (the )?" + NUM), "N of M over the collection"),
    (re.compile(NUM + r"(ordered |unordered )?pairs\b"), "a count of pairs"),
    (re.compile(NUM + r"(real |filled |shipped |composed )*(works|records|cues|compositions|"
                r"scores|passages|photographs)\b"), "a count over the collection"),
    (re.compile(r"\b(works|pairs|passages|cues|records)\s+in\s+(a hundred|two|three|four|five|six|"
                r"ten)\b|\b(one|two|three|four|five|six|seven|eight|nine|about \w+)\s+times\s+in\s+"
                r"(two|three|four|five|six|ten)\b|\b(a|one)\s+(sixth|quarter|third|fifth|"
                r"twentieth|twenty-fifth)\s+of\s+(pairs|passages|cues|the collection|all)\b"),
     "a share of the collection said in words"),
]
# What reads like a tally and is not one: a file path with a line citation, a date, a span written
# low-to-high, a threshold in the unit the eye reads, and a schema, api, row or section number.
INNOCENT = re.compile(r"[A-Za-z0-9_./-]+\.(py|js|md|json):[0-9-]+|[0-9]{4}-[0-9]{2}-[0-9]{2}|"
                      r"\b[0-9]+–[0-9]+\b|\b[0-9]+-[0-9]+\b|\bof 255\b|\bof [0-9]+ ms\b|"
                      r"\bschema [0-9]|\bapi [0-9]|§[0-9.]+|\brows? [0-9]+\b")


def enclosing_rule(lines, at):
    """The nearest name above this line a reader would call the rule: a function, a var, or the
    capitalised sentence the file opens each of its arguments with."""
    for i in range(at, max(-1, at - 60), -1):
        m = re.match(r"\s*(function|var) ([A-Za-z_][A-Za-z0-9_]*)", lines[i])
        if m:
            return m.group(2)
        m = re.match(r"\s*//\s+([A-Z][A-Z ,'`«»-]{12,})", lines[i])
        if m:
            return m.group(1).strip().rstrip(",")
    return "the file's own head"


def blocks_of(path, only_comments):
    """Each run of comment lines (or each paragraph) as one block of joined text, with an index
    that maps any offset inside the block back to the line it came from."""
    lines = path.read_text(encoding="utf-8").split("\n")
    out, run, marks, at = [], [], [], None
    for n, line in enumerate(lines):
        if only_comments:
            piece = line.split("//", 1)[1] if "//" in line else None
        else:
            piece = line if line.strip() else None
        if piece is None:
            if run:
                out.append((at, " ".join(run), list(marks)))
                run, marks, at = [], [], None
            continue
        if at is None:
            at = n
        marks.append((sum(len(r) + 1 for r in run), n))
        run.append(piece.strip())
    if run:
        out.append((at, " ".join(run), list(marks)))
    return lines, out


def line_at(marks, offset):
    """The source line an offset inside a joined block came from."""
    found = marks[0][1]
    for start, n in marks:
        if start <= offset:
            found = n
        else:
            break
    return found


def sweep(path, only_comments):
    lines, blocks = blocks_of(path, only_comments)
    hits = []
    for at, text, marks in blocks:
        # The innocent shapes are blanked rather than removed, so every offset still points at the
        # line it came from.
        text = INNOCENT.sub(lambda m: " " * len(m.group(0)), text)
        for pat, why in TALLY:
            m = pat.search(text)
            if m:
                hits.append((line_at(marks, m.start()) + 1, why, enclosing_rule(lines, at)))
                break
    return hits


comp_hits = sweep(MODULE, True)
doc_hits = sweep(CONTRACT, False)

check("R4 · no tally over the collection argues for a rule in the composer",
      not comp_hits,
      "" if not comp_hits else
      ("charter shelf 20 binds comments as much as code. Each line below stands a count over the "
       "photographs where an argument from the formula's own construction belongs — the tallies "
       "themselves are not reprinted here:\n"
       + "\n".join("        " + MODULE.name + ":" + str(n) + "  in `" + rule + "`  — " + why
                   for n, why, rule in comp_hits)))

check("R4 · no tally over the collection argues for a rule in the contract",
      not doc_hits,
      "" if not doc_hits else
      ("PASS-API-V1.md carries the same class in its own sections:\n"
       + "\n".join("        " + CONTRACT.name + ":" + str(n) + "  — " + why
                   for n, why, rule in doc_hits)))

# ---------------------------------------------------------------- report
print("EX-PASS · four laws the composer breaks today")
print("module: " + str(MODULE))
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
print("  " + str(sum(1 for r in results if r[1] == "PASS")) + " pass, "
      + str(sum(1 for r in results if r[1] == "FAIL")) + " fail, "
      + str(sum(1 for r in results if r[1] == "SKIP")) + " skip")
sys.exit(worst)
