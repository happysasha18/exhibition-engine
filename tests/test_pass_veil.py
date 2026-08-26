#!/usr/bin/env python3
"""PASS-API-V1 — the veil instrument on the host's frame.
Run: python3 tests/test_pass_veil.py

Root: charter shelf 14, the elements — «fog/veil layers, hiding and revealing; depth read as
thickness». There is no lab module for a veil, so there is no second road to compare against: this
instrument was authored against the charter rather than ported.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors, twice. Once as ARITHMETIC, under plain Node against the built artifact, over a sweep of
  every handle that could move a door — the veil's thickness, the stack's spread, the bodies, the
  wind's angle and the buffer — because a door claimed exact by construction is a claim about the
  whole span of those numbers and not about the handful a photograph happens to produce. Once as
  PIXELS, in a browser, against each work's own file cover-fitted into the frame at a crop of one.

  The one thing that decides whether this is a crossfade in weather's clothing: that the two works
  are never weighed against each other. A row reads the shader for the only mix it may carry — the
  one-buffer-point crossover — and a row measures that a work standing at a door has EXACTLY nothing
  in front of it while the other has all four sheets.

  The red-on-bug rows. Each serves a COPY of the built instrument file with one rule changed and
  reads what the instrument then says about its own door. The source tree is never written to.

  Node absent, or Chrome absent, or the two photographs absent, is a pinned SKIP that names what is
  missing — never a silent pass.
"""
import base64
import hashlib
import json
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

NAME = "veil"
SITE_URL = "https://synth.example.com"
NODE = shutil.which("node")
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
VW, VH = 390, 844          # the phone frame every instrument suite measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
SHOTS = ROOT / "tests" / "captures" / "pass-veil"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passveil_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
BUILT = (TMP / ("pass-inst-%s.js" % NAME)).read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in BUILT]
check("PASS-VEIL the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there"
      if not held else "the instrument's file holds " + ", ".join(held))

HANDLES = ["mix", "clock", "thickness", "bodies", "depth", "airAngle", "seed", "mask"]
check("PASS-VEIL every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in BUILT for h in HANDLES),
      "§4.4b: eight handles. The one place a second reaches this instrument — the wind's own run — "
      "reads the `clock` handle, which is what makes a seeded repeat mean anything. `shade` and "
      "`travel` are absent and the file says why: nothing here moves light and nothing is carried")

READS = {"thickness": "texture.scoreFromCutLines",
         "bodies": "structure.grid.periodPx",
         "depth": "structure.polar.tunnel",
         "airAngle": "structure.grid.angleDeg",
         "seed": "the score's own die"}
missing_reads = [h for h, m in READS.items() if m not in BUILT]
check("PASS-VEIL every handle that shapes the picture names the measurement of a work it reads",
      not missing_reads,
      "; ".join("%s reads %s" % (h, m) for h, m in READS.items()) if not missing_reads
      else "these name no measurement: " + ", ".join(missing_reads))

check("PASS-VEIL a sheet is nowhere absent, which is what makes both doors exact",
      "const float FLOOR = 0.22;" in BUILT and "var FLOOR = 0.22;" in BUILT
      and "float body = FLOOR + (1.0 - FLOOR) * nv.x;" in BUILT,
      "at a door the standing work has no sheet in front of it and the other has all four, each at "
      "least its own floor — so the standing work has less veil in front of it at every point of "
      "every buffer. A sheet with a hole in it would let the far work through at the door, which is "
      "why the floor is the door's own mechanism rather than a taste in the weather")

check("PASS-VEIL the works' travel is derived from the stack rather than typed against it",
      "return 1.5 * gap + SLAB_SHARE * gap + DEPTH_MARGIN;" in BUILT
      and "return [0.5 - 1.5 * gap, 0.5 - 0.5 * gap, 0.5 + 0.5 * gap, 0.5 + 1.5 * gap];" in BUILT,
      "the deepest sheet stands at 1.5 gaps from the middle and occupies a slab of its own, so a "
      "reach of 1.5 gaps plus a slab plus a margin puts a work in front of every sheet at one door "
      "and behind every sheet at the other — at every spread a score can name")

check("PASS-VEIL the two works are never weighed against each other",
      BUILT.count("mix(colB, colA, cov)") == 1
      and "float cov = clamp(0.5 + (tB - tA) / band, 0.0, 1.0);" in BUILT,
      "the ban this instrument came nearest to is the alpha crossfade as the arrival. There is "
      "exactly one mix between the two works in the whole shader and its weight is the coverage — "
      "which is 0 or 1 everywhere but inside a one-point crossover read off the two thicknesses' "
      "own analytic gradient. What travels with the dial is a DEPTH, and this file publishes no "
      "opacity to travel instead")

check("PASS-VEIL the veil writes no colour of its own anywhere",
      "DEEPEST * clamp(tA, 0.0, 1.0)" in BUILT and "DEEPEST * clamp(tB, 0.0, 1.0)" in BUILT
      and "const float DEEPEST = 5.0;" in BUILT,
      "the whole of the thickness is spent on the level of the picture's own chain each work is "
      "read at, so a work deep in the veil is its own masses rather than a wash — there is no "
      "colour in this shader to whiten a frame with, which is what separates it from the stock fog")

check("PASS-VEIL the chain of smaller copies is asked for, because it is the mechanism",
      "gl: { preserveDrawingBuffer: false, readsChain: true }" in BUILT,
      "§8's `readsChain`. Without the chain a coarser reading silently returns the sharpest copy "
      "and the frame comes out flat — the depth would be declared and invisible")

check("PASS-VEIL the level and the cut are both declared, in the instrument's own file",
      'levels: ["SURFACE", "TEXTURE"]' in BUILT and 'cuts: ["scale"]' in BUILT,
      "the site's settings build prefers a manifest's own `cuts` to any table it keeps and names an "
      "instrument that declares none as UNPLACED. This one parts each work by how coarsely it is "
      "read, which is the kind the recorded `texture` measure carries")

check("PASS-VEIL the coverage is declared, with the mechanism that pays for it",
      "coverage: { writes: false," in BUILT
      and "gl_FragColor = vec4(col, 1.0);" in BUILT,
      "every point of the frame carries one of the two photographs, so the alpha is the constant 1 "
      "and this instrument is lawful as the lowest cue of a stack and as a whole one-cue score")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', BUILT))
spelled = set(re.findall(r'uniform \w+ (u\w+);', BUILT))
check("PASS-VEIL the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 9,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ---------------------------------------------------------------- the rows Node runs

NODE_ROWS = [
    "PASS-VEIL §8     · the host's own registration takes this manifest, with nothing stubbed",
    "PASS-VEIL the two doors are exact over every thickness, spread, bodies and wind, on four buffers",
    "PASS-VEIL at a door the standing work has nothing in front of it and the other has all four sheets",
    "PASS-VEIL the two works trade depths on one straight line and cross exactly once",
    "PASS-VEIL the die moves where the banks stand and moves neither door",
    "PASS-VEIL the same pose answers the same numbers twice",
]
RED_ROWS = [
    "PASS-VEIL red-on-bug · the floor taken out from under a sheet: the door leaks and says so",
    "PASS-VEIL red-on-bug · the reading removed as well: the leaking door is answered with no refusal",
    "PASS-VEIL red-on-bug · the works' travel shortened: the standing work is read through veil",
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
// which is the very function the browser road calls.
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
                       coverage: man.coverage, gl: man.gl } : null;

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
var BUFFERS = [[390, 844], [780, 1688], [1170, 2532], [100, 100]];
var THICK = [0, 0.25, 0.5, 0.75, 1];
var SPREAD = [0, 0.25, 0.5, 0.75, 1];
var BODIES = [0, 0.5, 1];
var WIND = [0, 45, 90, 180];
var leaks = [], walked = 0, thinnest = 1e9, mostInFront = 0;
BUFFERS.forEach(function (b) {
  THICK.forEach(function (t) {
    SPREAD.forEach(function (s) {
      BODIES.forEach(function (bo) {
        WIND.forEach(function (w) {
          [0, 1].forEach(function (m) {
            var v = values({ mix: m, thickness: t, depth: s, bodies: bo, airAngle: w,
                             bufWidth: b[0], bufHeight: b[1] });
            walked++;
            if (v.doorWhyNo && leaks.length < 5) leaks.push([b, t, s, bo, w, m, v.doorWhyNo]);
            if (v.veil) {
              if (v.veil.clear < thinnest) thinnest = v.veil.clear;
              if (v.veil.inFront > mostInFront) mostInFront = v.veil.inFront;
            }
          });
        });
      });
    });
  });
});
out.doors = { walked: walked, leaks: leaks, thinnest: thinnest, mostInFront: mostInFront,
              ok: leaks.length === 0 };

// ---- WHAT STANDS IN FRONT OF EACH WORK AT A DOOR ----------------------------------------------
var atIn = values({ mix: 0 }), atOut = values({ mix: 1 });
out.sheets = { entry: [atIn.veil.inFront, atIn.veil.behind, atIn.veil.clear],
               exit: [atOut.veil.inFront, atOut.veil.behind, atOut.veil.clear],
               ok: atIn.veil.inFront === 0 && atOut.veil.inFront === 0
                   && atIn.veil.behind === 4 && atOut.veil.behind === 4
                   && atIn.veil.clear > 0 && atOut.veil.clear > 0 };

// ---- THE TWO WORKS TRADE DEPTHS ----------------------------------------------------------------
// One straight line each, in opposite directions, crossing exactly once: the departing work only
// ever goes deeper and the arriving one only ever comes forward, so nothing here retraces a path.
var walk = [], back = 0, forward = 0, crossings = 0, prev = null;
for (var k = 0; k <= 40; k++) {
  var v = values({ mix: k / 40 });
  if (prev) {
    if (v.zA < prev.zA - 1e-12) back++;
    if (v.zB > prev.zB + 1e-12) forward++;
    if ((prev.zA - prev.zB > 0) !== (v.zA - v.zB > 0)) crossings++;
  }
  prev = v;
  walk.push([k / 40, v.zA, v.zB]);
}
out.trade = { walk: [walk[0], walk[20], walk[40]], back: back, forward: forward,
              crossings: crossings,
              ok: back === 0 && forward === 0 && crossings === 1 };

// ---- THE DIE -----------------------------------------------------------------------------------
var d0 = values({ mix: 0.5, seed: 0 }), d3 = values({ mix: 0.5, seed: 3 });
var dDoor = [values({ mix: 0, seed: 3 }), values({ mix: 1, seed: 3 })];
out.die = { phases: [d0.phase, d3.phase],
            ok: d0.phase !== d3.phase && !dDoor[0].doorWhyNo && !dDoor[1].doorWhyNo };

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
                          capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout)[-700:]
    try:
        return json.loads(proc.stdout), None
    except Exception as e:
        return None, "%s: %s" % (e, proc.stdout[:400])


def plant(name, pairs):
    """A copy of the BUILT instrument file with one rule changed. Returns the path, or None when the
    line the proof stands on is no longer there to change — a plant that finds nothing asserts that
    loudly instead of passing.

    KEPT OUT OF THE BAKE'S OWN DIRECTORY, and that is not tidiness. The runner hands the host every
    `pass-inst-*.js` the bake wrote; a planted copy left beside them would be a SECOND file declaring
    the same instrument name, and the last one registered would decide what the rows measured."""
    out = BUILT
    for a, b in pairs:
        if out.count(a) < 1:
            return None
        out = out.replace(a, b)
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
        check(NODE_ROWS[0],
              G["registered"] and man.get("id") == NAME and man.get("arity") == 2
              and man.get("coverage", {}).get("writes") is False
              and man.get("levels") == ["SURFACE", "TEXTURE"] and man.get("cuts") == ["scale"]
              and man.get("gl", {}).get("readsChain") is True,
              "the host's own `register` took it, so its `manifestWhyNo` found every uniform "
              "supplied and its own frame values answered a neutral pose: arity %s, levels %s, "
              "cuts %s, chain %s"
              % (man.get("arity"), man.get("levels"), man.get("cuts"),
                 man.get("gl", {}).get("readsChain"))
              if G["registered"] else "the host refused it; refusals: %s" % G["refused"])

        d = G["doors"]
        check(NODE_ROWS[1], d["ok"],
              "%d poses walked — four buffers, five thicknesses, five spreads, three body counts, "
              "four wind angles, both doors — and not one leaks. Across all of them the standing "
              "work never had more than %s of a sheet in front of it and the far work's thinnest "
              "thickness never fell under %.4f"
              % (d["walked"], d["mostInFront"], d["thinnest"])
              if d["ok"] else "%d of %d poses leak; first: %s"
              % (len(d["leaks"]), d["walked"], json.dumps(d["leaks"][:2])))

        s = G["sheets"]
        check(NODE_ROWS[2], s["ok"],
              "at the entry door the departing work has %s sheets in front of it and the arriving "
              "one %s, whose thinnest thickness is %.4f; at the exit door the same the other way "
              "round. That difference is what a door stands on, and it has no width in it — no "
              "buffer can open or close it"
              % (s["entry"][0], s["entry"][1], s["entry"][2]))

        t = G["trade"]
        check(NODE_ROWS[3], t["ok"],
              "over forty-one steps of the dial the departing work goes deeper %d times against the "
              "run of the line and the arriving one comes forward %d times against it, and the two "
              "cross exactly %d time; the ends stand at %s and the middle at %s — so nothing here "
              "retraces a path"
              % (t["back"], t["forward"], t["crossings"],
                 json.dumps(t["walk"][0]), json.dumps(t["walk"][1])))

        di = G["die"]
        check(NODE_ROWS[4], di["ok"],
              "a die of three stands the sheets' own hash at a phase of %.4f against %.4f, so two "
              "passes over one edge meet two different weathers — and both doors stay whole under "
              "it, because a door reads only that a sheet is nowhere absent"
              % (di["phases"][1], di["phases"][0]))

        check(NODE_ROWS[5], G["repeat"]["ok"],
              "the same pose asked twice answers %d bytes of identical numbers, so a seeded score "
              "repeats to the pixel" % G["repeat"]["bytes"])

        # ---- red on bug ---------------------------------------------------------------------
        p1 = plant("nofloor", [("var FLOOR = 0.22;", "var FLOOR = 0.0;"),
                               ("const float FLOOR = 0.22;", "const float FLOOR = 0.0;")])
        if p1 is None:
            skip(RED_ROWS[0], "the plant found nothing to change")
        else:
            R1, w1 = run_node(p1, "nofloor")
            leaked = R1 and not R1["doors"]["ok"] and len(R1["doors"]["leaks"]) > 0
            check(RED_ROWS[0], bool(leaked),
                  "with the floor taken out a sheet is thin to nothing somewhere on the frame, so "
                  "the far work stands as clear there as the near one and the door is two "
                  "photographs; the instrument refuses it: «%s»"
                  % (R1["doors"]["leaks"][0][6][:200] if leaked else str(w1)))

            p2 = plant("nofloor-silent",
                       [("var FLOOR = 0.22;", "var FLOOR = 0.0;"),
                        ("const float FLOOR = 0.22;", "const float FLOOR = 0.0;"),
                        ("v.doorWhyNo = doorWhyNoOf(read);", "v.doorWhyNo = null;")])
            if p2 is None:
                skip(RED_ROWS[1], "the plant found nothing to change")
            else:
                R2, w2 = run_node(p2, "nofloor-silent")
                check(RED_ROWS[1], bool(R2) and R2["doors"]["ok"],
                      "with the reading taken out as well the very same leak is answered with no "
                      "refusal at all over all %d poses — so the reading is what stands between a "
                      "visitor and a door that is two photographs, rather than a number nobody acts "
                      "on" % (R2["doors"]["walked"] if R2 else 0))

        p3 = plant("shortreach", [("return 1.5 * gap + SLAB_SHARE * gap + DEPTH_MARGIN;",
                                   "return 1.0 * gap;")])
        if p3 is None:
            skip(RED_ROWS[2], "the plant found nothing to change")
        else:
            R3, w3 = run_node(p3, "shortreach")
            leaked3 = R3 and not R3["doors"]["ok"] and len(R3["doors"]["leaks"]) > 0
            check(RED_ROWS[2], bool(leaked3),
                  "with the works' travel shortened inside the stack the standing work stops in "
                  "front of only some of the sheets, so at its own door it is read off a coarser "
                  "copy than its file — the instrument refuses it with the number in it: «%s»"
                  % (R3["doors"]["leaks"][0][6][:200] if leaked3 else str(w3)))

# ---------------------------------------------------------------- the rows a browser runs

BROWSER_ROWS = [
    "PASS-VEIL the shader builds on a real context and the host draws with it",
    "PASS-VEIL row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-VEIL row 7  · door 0 carries no trace of the arriving work",
    "PASS-VEIL row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-VEIL row 7  · door 1 carries no trace of the departing work",
    "PASS-VEIL the veil reaches the picture: the middle is no door",
    "PASS-VEIL row 10 · a seeded run repeats to the pixel",
    "PASS-VEIL row 15 · the console stays clean",
    "PASS-VEIL the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-VEIL row 16 · the captures are kept as evidence",
    "PASS-VEIL red-on-bug · the sheets' own noise painted onto the picture: a pattern laid over a "
    "work that carries its own",
    "PASS-VEIL red-on-bug · the door hold widened past the door: the pass stalls on a still frame "
    "mid-crossing",
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
    """The work as this instrument seats it at a door: the plain cover fit, and nothing beyond it."""
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
    d = Path(tempfile.mkdtemp(prefix="synth_veilbench_"))
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    for inst in sorted(TMP.glob("pass-inst-*.js")):
        shutil.copy2(inst, d / inst.name)
    shutil.copy2(TMP / "config.json", d / "config.json")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_elements.html", d / "index.html")
    return d


def bench_dir_plant(path):
    """Like `bench_dir()`, but the instrument's own file is served from `path` — a copy planted by
    `plant()` with one rule changed — and the record's digest is recomputed to match, exactly as a
    real build stamps the file it serves. Without this a planted file is refused unread rather than
    measured, which is the same refusal `plant()`'s own docstring names for the Node road."""
    d = Path(tempfile.mkdtemp(prefix="synth_veilbenchplant_"))
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    settings = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
    text = Path(path).read_text(encoding="utf-8")
    settings["pass"]["instruments"][NAME]["digest"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    for inst in sorted(TMP.glob("pass-inst-*.js")):
        if inst.name == "pass-inst-%s.js" % NAME:
            (d / inst.name).write_text(text, encoding="utf-8")
        else:
            shutil.copy2(inst, d / inst.name)
    (d / "config.json").write_text(json.dumps(settings), encoding="utf-8")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_elements.html", d / "index.html")
    return d


def highpass_energy(path, radius=2):
    """The mean size of what a Gaussian blur of `radius` takes out of the frame — its own
    high-frequency content. A pattern laid over a photograph (a periodic texture, a grain, a weave)
    raises this; a photograph's own material, read at whatever level of the chain, does not."""
    from PIL import Image, ImageFilter
    import numpy as np
    im = Image.open(path).convert("L")
    blurred = im.filter(ImageFilter.GaussianBlur(radius))
    a = np.asarray(im).astype(np.float64)
    b = np.asarray(blurred).astype(np.float64)
    return float(np.abs(a - b).mean())


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


def on_bench_plant(path, fn):
    """Same road as `on_bench`, standing a PLANTED copy of this instrument instead of the built one —
    the pixel-side twin of `run_node(instrument_file=...)`."""
    d = bench_dir_plant(path)
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
        for i, m in enumerate([0.25, 0.4, 0.5, 0.6, 0.75]):
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
              "context, translated to GLSL ES 3.00 by its own `toES3`, bound both sources with the "
              "walking filter this manifest asks for, and drew a pose — which is the one thing no "
              "arithmetic row can prove")

        wA = work_in_the_frame(PHOTOS[0], VW, VH)
        wB = work_in_the_frame(PHOTOS[1], VW, VH)
        m0, x0 = apart(B["door0"], wA)
        m0b, _ = apart(B["door0"], wB)
        m1, x1 = apart(B["door1"], wB)
        m1a, _ = apart(B["door1"], wA)
        check(BROWSER_ROWS[1], m0 <= SEAM,
              "door 0 stands %.3f of 255 from the departing work's own cover fit at a crop of one "
              "(worst channel %.1f), against the %s the project's seam allows — the standing work "
              "is read at the sharpest copy of its own chain because nothing stands in front of it"
              % (m0, x0, SEAM))
        check(BROWSER_ROWS[2], m0b >= FAR,
              "and %.1f of 255 from the arriving work, which is a different photograph" % m0b)
        check(BROWSER_ROWS[3], m1 <= SEAM,
              "door 1 stands %.3f of 255 from the arriving work's own cover fit (worst channel %.1f)"
              % (m1, x1))
        check(BROWSER_ROWS[4], m1a >= FAR,
              "and %.1f of 255 from the departing work" % m1a)

        # WHERE A VEIL DOES ITS WORK, AND WHY THIS ROW MEASURES THE MIDDLE RATHER THAN THE WHOLE
        # WALK. The handover here is a change of DEPTH, so it is fastest where the two works pass
        # each other and slowest at either end: by three quarters of the dial the arriving work has
        # come forward past most of the stack and the frame is that work read through what is left,
        # which stands a few of 255 from its own file. That is the construction working rather than
        # a door held early, and the walk is printed whole so the shape is on the record instead of
        # being hidden by a row that only looks at its own two favourite places.
        mid_far = [(m, apart(p, wA)[0], apart(p, wB)[0]) for m, p in B["mids"]]
        middle = [r for r in mid_far if abs(r[0] - 0.5) < 1e-9][0]
        check(BROWSER_ROWS[5], min(middle[1], middle[2]) >= SEAM,
              "; ".join("mix %.2f stands %.1f from work a and %.1f from work b" % r
                        for r in mid_far)
              + " — where the two works pass each other the frame stands %.1f from one and %.1f "
                "from the other, both over the project's seam, so the middle of the crossing is a "
                "picture of its own and not a door held twice"
              % (middle[1], middle[2]))

        rm, rx = diff(B["rep0"], B["rep1"])
        check(BROWSER_ROWS[6], rx == 0,
              "the same pose drawn twice: %.4f of 255, worst channel %.0f" % (rm, rx))
        check(BROWSER_ROWS[7], not B["errs"],
              "no error, no rejection and no console.error over the whole run"
              if not B["errs"] else "; ".join(B["errs"][:4]))

        def road(br):
            score = {
                "schema": 2,
                "intent": "four sheets of veil hang between the eye and the two works, and the "
                          "arriving photograph comes forward through them",
                "pair": {"a": "a", "b": "b"}, "seed": 0, "duration": 3000,
                "direction": "a-to-b",
                "interruption": {"withinMs": 500, "resolve": "nearest-door"},
                "failLand": "arrive",
                "camera": {"owner": "stage", "rests": "b",
                           "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                                      "pitch": 0, "yaw": 0, "roll": 0, "fov": None,
                                      "owner": "stage"}]},
                "cues": [{
                    "id": "veil-main",
                    "instrument": {"id": NAME, "api": 1},
                    "voice": "letter",
                    "roles": ["disassembly", "mystery", "assembly"],
                    "levels": ["SURFACE", "TEXTURE"],
                    "window": [0, 3.0], "works": ["a", "b"], "stack": 0,
                    "cameraAuthority": "stage",
                    "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                              "out": {"handle": "mix", "value": 1, "measured": True}},
                    "nodes": {"mixDrive": {"source": "progress"},
                              "clockDrive": {"source": "time"},
                              "thickStatic": {"op": "static", "value": 0.5},
                              "bodiesStatic": {"op": "static", "value": 0.4},
                              "depthStatic": {"op": "static", "value": 0.5},
                              "angleStatic": {"op": "static", "value": 90},
                              "seedStatic": {"op": "static", "value": 0},
                              "maskStatic": {"op": "static", "value": 0}},
                    "tracks": {"mix": {"node": "mixDrive"}, "clock": {"node": "clockDrive"},
                               "thickness": {"node": "thickStatic"},
                               "bodies": {"node": "bodiesStatic"},
                               "depth": {"node": "depthStatic"},
                               "airAngle": {"node": "angleStatic"},
                               "seed": {"node": "seedStatic"},
                               "mask": {"node": "maskStatic"}},
                    "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0,
                                  "pingPong": 0, "programs": 1, "passes": 1, "bytesEstimate": 0,
                                  "variant": "standard"},
                }],
                "quality": {v: {"renderScale": None,
                                "cues": {"veil-main": {
                                    "textures": 0, "textureSlots": 2, "framebuffers": 0,
                                    "pingPong": 0, "programs": 1, "passes": 1,
                                    "bytesEstimate": 0, "variant": v}}}
                            for v in ("lean", "standard", "rich")},
                "provenance": {"source": "charter shelf 14, the elements",
                               "measuredAt": None, "by": "tests/test_pass_veil.py"},
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
        check(BROWSER_ROWS[9], len(kept) >= 9,
              "%d captures kept at %s" % (len(kept), SHOTS))

        # ---- red on bug: charter shelf 18's pattern laid over a work that carries its own --------
        # `tA` and `tB` are the two thicknesses the shader already reads off the sheets' own noise —
        # the walk that decides which work stands where and how coarsely it is read (§96-97 above).
        # The plant below folds that same field into the OUTPUT colour as a visible modulation,
        # which is the one thing the file's own comment says never happens. The pose stands the
        # sheets at their widest so the noise the plant paints is there to find.
        p5 = plant("paint",
                   [('vec3 col = mix(colB, colA, cov);',
                     'vec3 col = mix(colB, colA, cov) * (1.0 + 0.8 * (tA + tB - 1.0));')])
        if p5 is None:
            skip(BROWSER_ROWS[10], "the plant found nothing to change")
        else:
            pose = {"mix": 0.5, "thickness": 1.0, "bodies": 1.0, "depth": 0.6}

            def shoot_paint(br, tag):
                js(br, "window.__draw(%s); return 1;" % json.dumps(pose))
                return png(br, SHOTS / ("redbug-paint-%s.png" % tag))
            real_shot = on_bench(lambda br: shoot_paint(br, "real"))
            mut_shot = on_bench_plant(p5, lambda br: shoot_paint(br, "paint"))
            if real_shot is None or mut_shot is None:
                skip(BROWSER_ROWS[10], "one of the two benches never reported ready")
            else:
                hp_real = highpass_energy(real_shot)
                hp_mut = highpass_energy(mut_shot)
                caught = hp_mut > hp_real * 2.0
                check(BROWSER_ROWS[10], caught,
                      "a Gaussian blur of the frame at mix 0.5 with the sheets at their widest takes "
                      "out %.3f of 255 on average — the photographs' own material, at whatever level "
                      "of the chain each is read at; with the sheets' own thickness field folded "
                      "into the colour the same measure rises to %.3f, more than twice as much — the "
                      "sheets are drawn after all, which is the mark on the picture the file's own "
                      "comment says never lands" % (hp_real, hp_mut))

        # ---- red on bug: charter shelf 18's full-frame freeze ------------------------------------
        # `FEEL_D0` is the dead band `feelOf` holds flat at either door (§4.4's 5%, matching
        # `test_pass_adrift.py`'s own reading of this same construction on a neighbouring
        # instrument). The plant below widens it past the middle of the dial, so most of the pass
        # stands on the flat part of the curve and only a sliver in the middle still moves — a
        # frame that stops changing while the dial keeps advancing, which is the growth-only pacing
        # and full-frame freeze §18 bans.
        p6 = plant("widedoor", [("var FEEL_D0 = 0.05;", "var FEEL_D0 = 0.45;")])
        if p6 is None:
            skip(BROWSER_ROWS[11], "the plant found nothing to change")
        else:
            SWEEP = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

            def sweep_shots(br, tag):
                shots = []
                for i, m in enumerate(SWEEP):
                    js(br, "window.__draw({mix: %r}); return 1;" % m)
                    shots.append(png(br, SHOTS / ("redbug-sweep-%s-%d.png" % (tag, i))))
                return shots
            real_shots = on_bench(lambda br: sweep_shots(br, "real"))
            mut_shots = on_bench_plant(p6, lambda br: sweep_shots(br, "wide"))
            if real_shots is None or mut_shots is None:
                skip(BROWSER_ROWS[11], "one of the two benches never reported ready")
            else:
                real_diffs = [diff(real_shots[i], real_shots[i + 1])[0]
                              for i in range(len(real_shots) - 1)]
                mut_diffs = [diff(mut_shots[i], mut_shots[i + 1])[0]
                             for i in range(len(mut_shots) - 1)]
                frozen_real = sum(1 for d in real_diffs if d < 0.5)
                frozen_mut = sum(1 for d in mut_diffs if d < 0.5)
                caught = frozen_real == 0 and frozen_mut > 0
                check(BROWSER_ROWS[11], caught,
                      "nine steps of the dial from 0.1 to 0.9, each pair of neighbours diffed: with "
                      "the door's own 5%% dead band every one of the eight pairs moves (least %.2f "
                      "of 255); with the dead band widened to 45%% %d of the eight pairs stand at "
                      "the same frame to the byte (%s) — the pass stalls on a still frame while the "
                      "dial keeps advancing through most of its own middle"
                      % (min(real_diffs), frozen_mut,
                         ", ".join("%.1f-%.1f" % (SWEEP[i], SWEEP[i + 1])
                                   for i, d in enumerate(mut_diffs) if d < 0.5)))

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
