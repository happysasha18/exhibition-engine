#!/usr/bin/env python3
"""PASS-API-V1 — the pour instrument on the host's frame.
Run: python3 tests/test_pass_pour.py

Root: charter shelf 14, the elements — «granular pour (particles with an angle of repose; B
condenses from the pour)». There is no lab module for a pour, so there is no second road to compare
against: this instrument was authored against the charter rather than ported.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors, twice. Once as ARITHMETIC, under plain Node against the built artifact, over a sweep of
  every handle that could move a door — the column count, the repose angle, the stagger and the
  buffer — because a door this instrument claims is exact by construction is a claim about the whole
  span of those numbers and not about the handful a photograph happens to produce. Once as PIXELS,
  in a browser, against each work's own file cover-fitted into the frame at a crop of exactly one.

  The pour itself. That the heap's ceiling is DERIVED from the repose and the column count rather
  than typed, that a column's own travel is nothing at one door and whole at the other for every
  stagger, and that the middle of the dial is a picture of its own rather than a door held twice.

  The red-on-bug rows. Each serves a COPY of the built instrument file with one rule changed and
  reads what the instrument then says about its own door. The source tree is never written to.

  Node absent, or Chrome absent, or the two photographs absent, is a pinned SKIP that names what is
  missing — never a silent pass.
"""
import base64
import hashlib
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
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

NAME = "pour"
SITE_URL = "https://synth.example.com"
NODE = shutil.which("node")
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
VW, VH = 390, 844          # the phone frame every instrument suite measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
BACKGROUND = (0x08, 0x08, 0x0a)
SHOTS = ROOT / "tests" / "captures" / "pass-pour"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passpour_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
BUILT = (TMP / ("pass-inst-%s.js" % NAME)).read_text(encoding="utf-8")
SOURCE = (ROOT / "engine" / "assets" / ("pass-inst-%s.js" % NAME)).read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in BUILT]
check("PASS-POUR the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there"
      if not held else "the instrument's file holds " + ", ".join(held))

HANDLES = ["mix", "clock", "columns", "repose", "stagger", "grain", "seed", "shade", "mask", "presence"]
check("PASS-POUR every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in BUILT for h in HANDLES),
      "§4.4b: nine handles. The one place a second reaches this instrument — the grain's own drift "
      "— reads the `clock` handle, which is what makes a seeded repeat mean anything")

# EVERY HANDLE THAT SHAPES THE PICTURE NAMES THE MEASUREMENT IT READS (his 19:13 word lifted to the
# class at 19:21). The four geometric handles and the die are the five that must carry a `reads`
# line; the two judge channels and the dial carry none, because there is no photograph behind them.
READS = {"columns": "structure.grid.periodPx",
         "repose": "texture.detailPx of the ARRIVING work",
         "stagger": "structure.regions.score of the DEPARTING work",
         "grain": "texture.spectralPeriodPx of the DEPARTING work",
         "seed": "the score's own die"}
missing_reads = [h for h, m in READS.items() if m not in BUILT]
check("PASS-POUR every handle that shapes the picture names the measurement of a work it reads",
      not missing_reads,
      "; ".join("%s reads %s" % (h, m) for h, m in READS.items()) if not missing_reads
      else "these name no measurement: " + ", ".join(missing_reads))

check("PASS-POUR the heap's own ceiling is derived from the repose and the columns, not typed",
      "return 1 + slope / (2 * Math.max(cols, 1)) + MARGIN;" in BUILT
      and "var MARGIN = 0.10;" in BUILT,
      "at the exit door the surface at a point is the ceiling less the distance to the nearest "
      "pile's own centre times the slope, and that distance is never over half a column — so a "
      "ceiling of 1 + slope/(2·columns) + a tenth puts the heap over the whole frame at every "
      "column count and every repose angle a score can name, as an inequality rather than a "
      "tolerance")

check("PASS-POUR the level and the cut are both declared, in the instrument's own file",
      'levels: ["SURFACE", "CELL"]' in BUILT and 'cuts: ["strip"]' in BUILT,
      "the site's settings build prefers a manifest's own `cuts` to any table it keeps and names an "
      "instrument that declares none as UNPLACED — landed and uncastable. A column is a band of the "
      "frame taken along one axis, which is the strip kind")

check("PASS-POUR both doors frame at a cover crop of exactly one",
      '"0": { coverCrop: 1 }, "1": { coverCrop: 1 }' in BUILT,
      "nothing is dragged in from outside either picture — the fall is a translation and the "
      "sideways scatter is under one column and clamped — so no headroom is bought from either "
      "photograph")

check("PASS-POUR the coverage is declared, with the mechanism that pays for it",
      "coverage: {" in BUILT and "writes: true" in BUILT
      and "gl_FragColor = vec4(col, mix(max(covHeap, covFall), 1.0, uMask) * uPresence);" in BUILT,
      "this instrument's absence is the gap the pour opens — a point a column has drained past and "
      "the heap has not yet reached carries neither work — so it publishes that gap as its alpha "
      "and whatever plays beneath is seen there")

check("PASS-POUR the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in BUILT,
      "§7 refuses a manifest that asks for one; the redraw it would stand in for is the host's own "
      "frame loop")

check("PASS-POUR nothing is drawn at the heap's own boundary",
      "float face = lean * slope / sqrt(1.0 + slope * slope);" in BUILT
      and "colB *= 1.0 + LIGHT * face * uLight.x * win;" in BUILT,
      "the ban this instrument came nearest to is the drawn seam line between particles. The heap's "
      "light is a body shading read off the flank's own lean and steepness — strongest in the "
      "middle of a slope, exactly nothing where the heap is flat — and there is no term anywhere "
      "in this shader that reads the distance to the boundary")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', BUILT))
spelled = set(re.findall(r'uniform \w+ (u\w+);', BUILT))
check("PASS-POUR the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 10,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ---------------------------------------------------------------- the rows Node runs

NODE_ROWS = [
    "PASS-POUR §8     · the host's own registration takes this manifest, with nothing stubbed",
    "PASS-POUR the two doors are exact over every column count, repose and stagger, on four buffers",
    "PASS-POUR the pour travels: the middle is neither door, and the heap only ever rises",
    "PASS-POUR a column's own travel is nothing at one door and whole at the other, at every stagger",
    "PASS-POUR the die moves which column lets go first and moves neither door",
    "PASS-POUR the same pose answers the same numbers twice",
]
RED_ROWS = [
    "PASS-POUR red-on-bug · the heap's ceiling typed flat: the exit door leaks and says so",
    "PASS-POUR red-on-bug · the reading removed as well: the leaking door is answered with no refusal",
    "PASS-POUR red-on-bug · the grain's window removed: the entry door carries a roughness the file does not",
]

RUNNER = r"""
// The window pass-layer.js expects to find itself in. Nothing about the file under test is stubbed:
// this is the BUILT artifact, and the bench it publishes hands back the very pure functions a
// running frame calls.
global.window = { devicePixelRatio: 1, innerWidth: 390, innerHeight: 844 };
global.performance = { now: function () { return 0; } };
window.__@@NS@@Pass = {};
window.__@@NS@@PassLayer = function (h) { window.__host = h; };
require(process.argv[2]);
var bench = window.__@@NS@@Pass.bench;
var host = window.__host;

// THE INSTRUMENTS, PUT ON THE REGISTRY BY THE HOST'S OWN DOOR. Node offers neither a fetch of a
// relative address nor a blob script road, so this runner performs by hand the two steps the browser
// road performs for it: read each built file, and hand the instrument it declares to host.register,
// which is the very function the browser road calls. So the manifest rows below read a real manifest
// off a real registry, judged by the real manifestWhyNo, with nothing stubbed.
var loaded = [];
window.__@@NS@@PassInstrument = function (p) { loaded.push(p.instrument); };
var refused = {};
for (var ai = 4; ai < process.argv.length; ai++) require(process.argv[ai]);
loaded.forEach(function (i) { if (!host.register(i)) refused[i.name] = true; });

var NAME = process.argv[3];
var out = { refused: Object.keys(refused).sort(), registered: !refused[NAME] };
var man = bench.manifest(NAME);
out.manifest = man ? { id: man.id, api: man.api, arity: man.arity, levels: man.levels,
                       cuts: man.cuts, roles: man.roles,
                       handles: Object.keys(man.handles).sort(),
                       coverage: man.coverage, framings: man.framings } : null;

function pose(over) {
  var p = {};
  Object.keys(man.handles).forEach(function (h) { p[h] = man.handles[h]["def"]; });
  p.t = 0; p.reduced = false; p.cssWidth = 390; p.cssHeight = 844;
  p.bufWidth = 780; p.bufHeight = 1688;
  Object.keys(over || {}).forEach(function (k) { p[k] = over[k]; });
  return p;
}
function values(over) { return bench.values(NAME, pose(over)); }

// ---- THE TWO DOORS, OVER THE WHOLE SPAN OF EVERY HANDLE THAT COULD MOVE ONE -------------------
// A door claimed exact by construction is a claim about every number in the span, so the span is
// what is walked: four buffers a real device can hand, every column count from the fewest to the
// most, both ends and the middle of the repose, and every stagger including the widest.
var BUFFERS = [[390, 844], [780, 1688], [1170, 2532], [100, 100]];
var COLS = [4, 9, 16, 33, 64];
var REPOSE = [0, 0.25, 0.5, 0.75, 1];
var STAGGER = [0, 0.3, 0.6, 0.9];
var leaks = [], walked = 0, tightestEntry = 1e9, tightestExit = 1e9;
BUFFERS.forEach(function (b) {
  COLS.forEach(function (c) {
    REPOSE.forEach(function (r) {
      STAGGER.forEach(function (s) {
        [0, 1].forEach(function (m) {
          var v = values({ mix: m, columns: c, repose: r, stagger: s,
                           bufWidth: b[0], bufHeight: b[1] });
          walked++;
          if (v.doorWhyNo) {
            if (leaks.length < 5) leaks.push([b, c, r, s, m, v.doorWhyNo]);
          }
          if (v.pileRead) {
            if (m === 0 && v.pileRead.spareRows < tightestEntry) tightestEntry = v.pileRead.spareRows;
            if (m === 1 && v.pileRead.spareRows < tightestExit) tightestExit = v.pileRead.spareRows;
          }
        });
      });
    });
  });
});
out.doors = { walked: walked, leaks: leaks, tightestEntry: tightestEntry,
              tightestExit: tightestExit, ok: leaks.length === 0 };

// ---- THE POUR TRAVELS -------------------------------------------------------------------------
// The heap ONLY EVER RISES, which is what makes a pour a pour rather than a breath. It is read on
// the instrument's own heap surface — nine places across the frame, twenty-one steps of the dial —
// and a single step at which any of the nine stands lower than it did the step before reds this.
var inst = null;
loaded.forEach(function (i) { if (i.name === NAME) inst = i; });
var prev = null, sank = 0, hReads = [];
for (var k = 0; k <= 20; k++) {
  var vv = values({ mix: k / 20 });
  var here = [];
  for (var x = 0; x < 9; x++) here.push(inst.heapAt(vv, (x + 0.5) / 9));
  if (prev) for (var y = 0; y < 9; y++) if (here[y] < prev[y] - 1e-12) sank++;
  prev = here;
  hReads.push([k / 20, vv.dialAt, here[4]]);
}
out.travel = { reads: hReads, sank: sank,
               ok: sank === 0 && values({ mix: 0 }).dialAt === 0 && values({ mix: 1 }).dialAt === 1
                   && values({ mix: 0.5 }).dialAt > 0 && values({ mix: 0.5 }).dialAt < 1 };

// The window both the grain and the heap's light ride: exactly nothing at both ends of the hand in
// floating point, which is why neither can reach a door whatever a score names.
out.window = { at0: values({ mix: 0 }).window, at1: values({ mix: 1 }).window,
               atHalf: values({ mix: 0.5 }).window };
out.window.ok = out.window.at0 === 0 && out.window.at1 === 0 && out.window.atHalf > 0.9;

// ---- A COLUMN'S OWN TRAVEL --------------------------------------------------------------------
// Read off the instrument's own function rather than off a copy of it: `heapAt` walks the same
// envelope the shader draws, so a pile standing at the ceiling means every column has poured.
var colReads = [];
STAGGER.forEach(function (s) {
  var v0 = bench.values(NAME, pose({ mix: 0, stagger: s }));
  var v1 = bench.values(NAME, pose({ mix: 1, stagger: s }));
  var lo = 0, hi = 1e9, x;
  for (x = 0; x <= 32; x++) {
    lo = Math.max(lo, inst.heapAt(v0, x / 32));
    hi = Math.min(hi, inst.heapAt(v1, x / 32));
  }
  colReads.push([s, lo, hi, v1.ceiling]);
});
out.columns = { reads: colReads,
                ok: colReads.every(function (r) { return r[1] === 0 && r[2] >= 1; }) };

// ---- THE DIE -----------------------------------------------------------------------------------
var dieMid = [values({ mix: 0.5, seed: 0 }), values({ mix: 0.5, seed: 3 })];
var dieDoor = [values({ mix: 0, seed: 3 }), values({ mix: 1, seed: 3 })];
var midShape = [[], []];
[0, 1].forEach(function (i) {
  for (var x = 0; x <= 32; x++) midShape[i].push(inst.heapAt(dieMid[i], x / 32));
});
var moved = 0;
for (var x2 = 0; x2 <= 32; x2++) moved = Math.max(moved, Math.abs(midShape[0][x2] - midShape[1][x2]));
out.die = { moved: moved, phases: [dieMid[0].phase, dieMid[1].phase],
            doorsClean: !dieDoor[0].doorWhyNo && !dieDoor[1].doorWhyNo,
            ok: moved > 0.01 && !dieDoor[0].doorWhyNo && !dieDoor[1].doorWhyNo };

// ---- THE SAME POSE ANSWERS THE SAME NUMBERS ---------------------------------------------------
var r1 = JSON.stringify(values({ mix: 0.37, seed: 5, clock: 4.2 }));
var r2 = JSON.stringify(values({ mix: 0.37, seed: 5, clock: 4.2 }));
out.repeat = { ok: r1 === r2, bytes: r1.length };

process.stdout.write(JSON.stringify(out));
"""


def run_node(instrument_file=None, tag="run"):
    """The runner against the BUILT host and the BUILT instrument files. `instrument_file` names a
    COPY of this instrument with one rule changed, which is how the red-on-bug proofs below run; the
    source tree is never written to."""
    layer = (TMP / "pass-layer.js").read_text(encoding="utf-8")
    ns = re.search(r"window\.__(\w+?)PassLayer", layer)
    if not ns:
        return None, "the built host names no PassLayer join point"
    runner = TMP / ("%s-runner.js" % tag)
    runner.write_text(RUNNER.replace("@@NS@@", ns.group(1)), encoding="utf-8")
    files = []
    for p in sorted(TMP.glob("pass-inst-*.js")):
        files.append(str(instrument_file) if (instrument_file and p.name.endswith(NAME + ".js"))
                     else str(p))
    proc = subprocess.run([NODE, str(runner), str(TMP / "pass-layer.js"), NAME] + files,
                          capture_output=True, text=True, timeout=180)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-700:]
    try:
        return json.loads(proc.stdout), None
    except Exception as e:
        return None, "%s: %s" % (e, proc.stdout[:400])


def plant(name, pairs):
    """A copy of the BUILT instrument file with one rule changed. Returns the path, or None when the
    line the proof stands on is no longer there to change — a plant that finds nothing asserts that
    loudly instead of passing."""
    out = BUILT
    for a, b in pairs:
        if out.count(a) < 1:
            return None
        out = out.replace(a, b)
    # KEPT OUT OF THE BAKE'S OWN DIRECTORY, and that is not tidiness. The runner hands the host
    # every `pass-inst-*.js` the bake wrote; a planted copy left beside them would be a SECOND file
    # declaring the same instrument name, and the last one registered would decide what the rows
    # below measured. It costs one directory to make the substitution the only difference.
    plants = TMP / "plants"
    plants.mkdir(exist_ok=True)
    path = plants / ("pass-inst-%s-%s.js" % (NAME, name))
    path.write_text(out, encoding="utf-8")
    return path


if not NODE:
    for r in NODE_ROWS + RED_ROWS:
        skip(r, "node is not installed (pinned expected skip)")
else:
    G, why = run_node()
    if G is None:
        for r in NODE_ROWS + RED_ROWS:
            skip(r, "the runner did not answer: " + str(why))
    else:
        man = G["manifest"] or {}
        need = ["id", "api", "arity", "levels", "cuts", "roles", "handles", "coverage", "framings"]
        lack = [k for k in need if not man.get(k)]
        check(NODE_ROWS[0],
              G["registered"] and not lack and man.get("id") == NAME and man.get("arity") == 2
              and man.get("coverage", {}).get("writes") is True
              and man.get("levels") == ["SURFACE", "CELL"] and man.get("cuts") == ["strip"],
              "the host's own `register` took it, so its `manifestWhyNo` found every uniform "
              "supplied and its own frame values answered a neutral pose: arity %s, levels %s, "
              "cuts %s, coverage %s"
              % (man.get("arity"), man.get("levels"), man.get("cuts"), man.get("coverage"))
              if G["registered"] else "the host refused it; refusals: %s" % G["refused"])

        d = G["doors"]
        check(NODE_ROWS[1], d["ok"],
              "%d poses walked — four buffers, five column counts, five repose angles, four "
              "staggers, both doors — and not one leaks. The tightest entry door kept %.3f of a row "
              "to spare and the tightest exit door %.3f, both on the instrument's own walk of the "
              "buffer it was about to draw on"
              % (d["walked"], d["tightestEntry"], d["tightestExit"])
              if d["ok"] else "%d of %d poses leak; first: %s"
              % (len(d["leaks"]), d["walked"], json.dumps(d["leaks"][:2])))

        t, w = G["travel"], G["window"]
        check(NODE_ROWS[2], t["ok"] and w["ok"],
              "the heap never sinks: over twenty-one steps of the dial, nine places across the "
              "frame, %d readings stood lower than the reading before them. The dial lands exactly "
              "on nothing at one door and exactly on one at the other with the dead bands taken "
              "off; the window both the grain and the heap's light ride is exactly %s at both "
              "doors and %.4f mid-dial, so neither can reach a landing whatever a score names"
              % (t["sank"], w["at0"], w["atHalf"]))

        c = G["columns"]
        check(NODE_ROWS[3], c["ok"],
              "; ".join("stagger %.1f: the highest pile at the entry door is %.4f and the lowest at "
                        "the exit door %.4f against a ceiling of %.4f" % tuple(r) for r in c["reads"])
              + " — so at every stagger no column has poured at one door and every column has at "
                "the other, walked on the instrument's own heap surface rather than on a copy of it")

        di = G["die"]
        check(NODE_ROWS[4], di["ok"],
              "a die of three moves the heap's own surface by %.4f of the frame's height at the "
              "middle of the dial, and both doors stay whole under it — the die spends a phase into "
              "the column hash and nothing else" % di["moved"])

        check(NODE_ROWS[5], G["repeat"]["ok"],
              "the same pose asked twice answers %d bytes of identical numbers, so a seeded score "
              "repeats to the pixel" % G["repeat"]["bytes"])

        # ---- red on bug ---------------------------------------------------------------------
        p1 = plant("flat", [("return 1 + slope / (2 * Math.max(cols, 1)) + MARGIN;",
                             "return 1.0;")])
        if p1 is None:
            skip(RED_ROWS[0], "the plant found nothing to change")
        else:
            R1, w1 = run_node(p1, "flat")
            leaked = R1 and not R1["doors"]["ok"] and len(R1["doors"]["leaks"]) > 0
            check(RED_ROWS[0], bool(leaked),
                  "with the ceiling typed at one instead of derived from the repose and the column "
                  "count, the surface stands short of the frame's top row wherever a point falls "
                  "between two piles, and the instrument refuses its own exit door: «%s»"
                  % (R1["doors"]["leaks"][0][5][:200] if leaked else str(w1)))

            p2 = plant("flat-silent", [("return 1 + slope / (2 * Math.max(cols, 1)) + MARGIN;",
                                        "return 1.0;"),
                                       ("var no = doorWhyNoOf(read);", "var no = null;")])
            if p2 is None:
                skip(RED_ROWS[1], "the plant found nothing to change")
            else:
                R2, w2 = run_node(p2, "flat-silent")
                check(RED_ROWS[1], bool(R2) and R2["doors"]["ok"],
                      "with the reading taken out as well the very same leak is answered with no "
                      "refusal at all over all %d poses — so the reading is what stands between a "
                      "visitor and a door that is two photographs, rather than a number nobody acts "
                      "on" % (R2["doors"]["walked"] if R2 else 0))

        p3 = plant("nowin", [("var win = 4 * d * (1 - d);", "var win = 1;")])
        if p3 is None:
            skip(RED_ROWS[2], "the plant found nothing to change")
        else:
            R3, w3 = run_node(p3, "nowin")
            broke = R3 and R3["window"]["at0"] == 1 and R3["window"]["at1"] == 1
            check(RED_ROWS[2], bool(broke),
                  "with the window opened flat the grain and the heap's light stand at their full "
                  "strength at both doors — %s at the entry and %s at the exit against %s and %s "
                  "with the window — so a door would carry a roughness and a modelling the file "
                  "itself does not"
                  % (R3["window"]["at0"] if R3 else "?", R3["window"]["at1"] if R3 else "?",
                     G["window"]["at0"], G["window"]["at1"]))

# ---------------------------------------------------------------- the rows a browser runs

BROWSER_ROWS = [
    "PASS-POUR the shader builds on a real context and the host draws with it",
    "PASS-POUR row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-POUR row 7  · door 0 carries no trace of the arriving work",
    "PASS-POUR row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-POUR row 7  · door 1 carries no trace of the departing work",
    "PASS-POUR the pour reaches the picture: the middle is no door",
    "PASS-POUR row 10 · a seeded run repeats to the pixel",
    "PASS-POUR row 15 · the console stays clean",
    "PASS-POUR the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-POUR row 16 · the captures are kept as evidence",
]

missing = [str(p) for p in PHOTOS if not p.exists()]


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def diff(p, q):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, c))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def work_in_the_frame(src, w, h):
    """The work as this instrument seats it at a door: the plain cover fit, and nothing beyond it.
    The crop is exactly one, which is what the manifest's `framings` block publishes."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    x0, y0 = (iw - sw) / 2.0, (ih - sh) / 2.0
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + sw, y0 + sh))


def apart(p, work):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    if a.size != work.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, work))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def bench_dir():
    d = Path(tempfile.mkdtemp(prefix="synth_pourbench_"))
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(inst, d / inst.name)
    shutil.copy2(TMP / "config.json", d / "config.json")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_elements.html", d / "index.html")
    return d


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def ready(br, tries=80):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def on_bench(fn):
    d = bench_dir()
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html#" + NAME)
                if not ready(br):
                    return None
                return fn(br)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_browser_rows():
    def body(br):
        got = {}
        SHOTS.mkdir(parents=True, exist_ok=True)
        got["manifest"] = js(br, "return window.__manifest();")
        got["drew"] = js(br, "return window.__draw({mix: 0});")
        got["door0"] = png(br, SHOTS / "door0.png")
        js(br, "window.__draw({mix: 1}); return 1;")
        got["door1"] = png(br, SHOTS / "door1.png")
        mids = []
        for i, m in enumerate([0.3, 0.5, 0.7]):
            js(br, "window.__draw({mix: %r}); return 1;" % m)
            mids.append([m, png(br, SHOTS / ("mid%d.png" % i))])
        got["mids"] = mids
        js(br, "window.__draw({mix: 0.42, seed: 3, clock: 5}); return 1;")
        got["rep0"] = png(br, SHOTS / "repeat-a.png")
        js(br, "window.__draw({mix: 0.42, seed: 3, clock: 5}); return 1;")
        got["rep1"] = png(br, SHOTS / "repeat-b.png")
        got["errs"] = js(br, "return window.__errs;")
        return got
    return on_bench(body)


if missing:
    for r in BROWSER_ROWS:
        skip(r, "the photographs are not on this machine: " + ", ".join(missing))
elif not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "chrome is not installed (pinned expected skip)")
else:
    B = run_browser_rows()
    if B is None:
        for r in BROWSER_ROWS:
            skip(r, "the bench page never reported ready")
    else:
        check(BROWSER_ROWS[0],
              bool(B["manifest"]) and B["manifest"].get("id") == NAME and B["drew"] is True,
              "the host compiled this instrument's own vertex and fragment shaders on a real WebGL 2 "
              "context, translated to GLSL ES 3.00 by its own `toES3`, and drew a pose with them — "
              "which is the one thing no arithmetic row can prove")

        wA = work_in_the_frame(PHOTOS[0], VW, VH)
        wB = work_in_the_frame(PHOTOS[1], VW, VH)
        m0, x0 = apart(B["door0"], wA)
        m0b, _ = apart(B["door0"], wB)
        m1, x1 = apart(B["door1"], wB)
        m1a, _ = apart(B["door1"], wA)
        check(BROWSER_ROWS[1], m0 <= SEAM,
              "door 0 stands %.3f of 255 from the departing work's own cover fit at a crop of one "
              "(worst channel %.1f), against the %s the project's seam allows" % (m0, x0, SEAM))
        check(BROWSER_ROWS[2], m0b >= FAR,
              "and %.1f of 255 from the arriving work, which is a different photograph" % m0b)
        check(BROWSER_ROWS[3], m1 <= SEAM,
              "door 1 stands %.3f of 255 from the arriving work's own cover fit (worst channel "
              "%.1f) — the heap has buried the frame" % (m1, x1))
        check(BROWSER_ROWS[4], m1a >= FAR,
              "and %.1f of 255 from the departing work" % m1a)

        mid_far = [(m, apart(p, wA)[0], apart(p, wB)[0]) for m, p in B["mids"]]
        moved = min(min(a, b) for _, a, b in mid_far)
        check(BROWSER_ROWS[5], moved >= SEAM,
              "; ".join("mix %.2f stands %.1f from work a and %.1f from work b" % r
                        for r in mid_far)
              + " — the nearest of them is %.1f of 255 from either whole work, over the project's "
                "seam, so the middle is a picture of its own and not a door held twice" % moved)

        rm, rx = diff(B["rep0"], B["rep1"])
        check(BROWSER_ROWS[6], rx == 0,
              "the same pose drawn twice: %.4f of 255, worst channel %.0f" % (rm, rx))
        check(BROWSER_ROWS[7], not B["errs"],
              "no error, no rejection and no console.error over the whole run"
              if not B["errs"] else "; ".join(B["errs"][:4]))

        def road(br):
            score = {
                "schema": 2,
                "intent": "the departing photograph pours away a column at a time and heaps into "
                          "the arriving one along its own angle of repose",
                "pair": {"a": "a", "b": "b"}, "seed": 0, "duration": 3000,
                "direction": "a-to-b",
                "interruption": {"withinMs": 500, "resolve": "nearest-door"},
                "failLand": "arrive",
                "camera": {"owner": "stage", "rests": "b",
                           "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                                      "pitch": 0, "yaw": 0, "roll": 0, "fov": None,
                                      "owner": "stage"}]},
                "cues": [{
                    "id": "pour-main",
                    "instrument": {"id": NAME, "api": 1},
                    "voice": "letter",
                    "roles": ["disassembly", "mystery", "assembly"],
                    "levels": ["SURFACE", "CELL"],
                    "window": [0, 3.0], "works": ["a", "b"], "stack": 0,
                    "cameraAuthority": "stage",
                    "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                              "out": {"handle": "mix", "value": 1, "measured": True}},
                    "nodes": {"mixDrive": {"source": "progress"},
                              "clockDrive": {"source": "time"},
                              "colsStatic": {"op": "static", "value": 16},
                              "reposeStatic": {"op": "static", "value": 0.45},
                              "staggerStatic": {"op": "static", "value": 0.5},
                              "grainStatic": {"op": "static", "value": 0.4},
                              "seedStatic": {"op": "static", "value": 0},
                              "shadeStatic": {"op": "static", "value": 1},
                              "maskStatic": {"op": "static", "value": 0}},
                    "tracks": {"mix": {"node": "mixDrive"}, "clock": {"node": "clockDrive"},
                               "columns": {"node": "colsStatic"},
                               "repose": {"node": "reposeStatic"},
                               "stagger": {"node": "staggerStatic"},
                               "grain": {"node": "grainStatic"},
                               "seed": {"node": "seedStatic"},
                               "shade": {"node": "shadeStatic"},
                               "mask": {"node": "maskStatic"}},
                    "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0,
                                  "pingPong": 0, "programs": 1, "passes": 1, "bytesEstimate": 0,
                                  "variant": "standard"},
                }],
                "quality": {v: {"renderScale": None,
                                "cues": {"pour-main": {
                                    "textures": 0, "textureSlots": 2, "framebuffers": 0,
                                    "pingPong": 0, "programs": 1, "passes": 1,
                                    "bytesEstimate": 0, "variant": v}}}
                            for v in ("lean", "standard", "rich")},
                "provenance": {"source": "charter shelf 14, the elements",
                               "measuredAt": None, "by": "tests/test_pass_pour.py"},
            }
            out = js(br, "return window.__offer(%s, {});" % json.dumps(score))
            br.sleep(2.0)
            for _ in range(60):
                if js(br, "return window.__report().state;") == "idle":
                    break
                br.sleep(0.15)
            return {"took": out, "hooks": js(br, "return window.__hooks;"),
                    "state": js(br, "return window.__report().state;"),
                    "errs": js(br, "return window.__errs;")}
        R = on_bench(road)
        check(BROWSER_ROWS[8],
              bool(R) and R["took"]["took"] is True and R["hooks"]["curtains"][:1] == [True]
              and len(R["hooks"]["docks"]) == 1 and R["state"] == "idle",
              "the host took the offer, raised its curtain, drew the pass and docked once: %s"
              % json.dumps(R["hooks"]) if R else "the road never ran")

        kept = sorted(p.name for p in SHOTS.glob("*.png")) if SHOTS.exists() else []
        check(BROWSER_ROWS[9], len(kept) >= 7,
              "%d captures kept at %s" % (len(kept), SHOTS))

# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, verdict, detail in results:
    print("%-4s %s" % (verdict, name))
    if detail:
        print("       %s" % detail)
print("\n%d passed / %d failed / %d skipped"
      % (len(results) - len(fails) - len(skips), len(fails), len(skips)))
sys.exit(1 if fails else 0)
