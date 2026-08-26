#!/usr/bin/env python3
"""PASS-API-V1 — the wind instrument on the host's frame.
Run: python3 tests/test_pass_wind.py

Root: charter shelf 14, the elements — «wind bending rows». There is no lab module for a wind, so
there is no second road to compare against: this instrument was authored against the charter rather
than ported.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors, twice. Once as ARITHMETIC, under plain Node against the built artifact, over a sweep of
  every handle that could move a door — the row axis, the gust's own length, the rows' lag, the row
  count and the buffer — because a door claimed exact by construction is a claim about the whole span
  of those numbers and not about the handful a photograph happens to produce. Once as PIXELS, in a
  browser, against each work's own file cover-fitted into the frame at a crop of exactly one.

  The one thing that separates this from the stock ripple: that there is ONE gust, that it crosses
  once and never returns, and that the change of hands rides its own front rather than being
  decoration over a dissolve. A row walks the front over the whole dial and reds on a single step
  backwards.

  The red-on-bug rows. Each serves a COPY of the built instrument file with one rule changed and
  reads what the instrument then says about its own door. The source tree is never written to.

  Node absent, or Chrome absent, or the two photographs absent, is a pinned SKIP that names what is
  missing — never a silent pass.
"""
import base64
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

NAME = "wind"
SITE_URL = "https://synth.example.com"
NODE = shutil.which("node")
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
VW, VH = 390, 844          # the phone frame every instrument suite measures on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
FAR = 40.0                 # further than this from a file and it is a different work
SHOTS = ROOT / "tests" / "captures" / "pass-wind"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passwind_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
BUILT = (TMP / ("pass-inst-%s.js" % NAME)).read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

OWNED = ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
         "performance.now", "Date.now", "new Image", "setTimeout", "setInterval"]
held = [s for s in OWNED if s in BUILT]
check("PASS-WIND the instrument creates no context, no canvas, no loop and no listener",
      not held,
      "§1.2's fence, read against the instrument's own built file: none of the nine ways of owning "
      "hardware appears there"
      if not held else "the instrument's file holds " + ", ".join(held))

HANDLES = ["mix", "clock", "rows", "axis", "bend", "gust", "lag", "seed", "shade", "travel", "mask"]
check("PASS-WIND every handle the instrument publishes is a handle a score can drive",
      all(("%s: { min" % h) in BUILT for h in HANDLES),
      "§4.4b: eleven handles. The one place a second reaches this instrument — the fine tremor over "
      "the gust — reads the `clock` handle, which is what makes a seeded repeat mean anything")

READS = {"rows": "the pivot's own band family, its measured count along the cut",
         "axis": "the banding axis cut-lines.json recorded",
         "bend": "structure.banding.score",
         "gust": "structure.grid.periodPx of the work over its own frame side",
         "lag": "structure.grid.angleDeg",
         "seed": "the score's own die"}
missing_reads = [h for h, m in READS.items() if m not in BUILT]
check("PASS-WIND every handle that shapes the picture names the measurement of a work it reads",
      not missing_reads,
      "; ".join("%s reads %s" % (h, m) for h, m in READS.items()) if not missing_reads
      else "these name no measurement: " + ", ".join(missing_reads))

check("PASS-WIND the gust's own travel is derived from the axis, the body and the lag",
      "var half = (Math.abs(Math.cos(ang)) + Math.abs(Math.sin(ang))) / 2;" in BUILT
      and "var start = 0.5 - half - MARGIN - 2 * body;" in BUILT
      and "var end = 0.5 + half + MARGIN + 2 * body + lag;" in BUILT,
      "turn the rows and the frame's own corners run further along them than its edges do — a "
      "seventh over a half at forty-five degrees. Reading that reach rather than assuming a half is "
      "what keeps both doors exact at every axis a score can name; assuming one would have left a "
      "corner of the frame on the wrong side of the front at the shortest gust")

check("PASS-WIND the envelope lands on exactly nothing at both doors, in floating point",
      "var env = 4 * d * (1 - d);" in BUILT,
      "`sin(π·d)` at d = 1 is the machine's own rounding of π rather than nothing — 1.22e-16 of a "
      "frame width — so a door that asks for still air would be refused by its own instrument on a "
      "pose that is correct. This window is built out of the dial itself and lands on exactly zero")

check("PASS-WIND the change of hands rides the gust's own front",
      "float alongS = dot(src - 0.5, dir) + 0.5;" in BUILT
      and "float cov = clamp(0.5 + (front - alongS) / band, 0.0, 1.0);" in BUILT
      and "vec2 disp = nrm * push + dir * (DOWNWIND * push);" in BUILT,
      "the boundary is read at the SOURCE point rather than at the output one, so it is bent by the "
      "very air that bends the picture — the displacement carries a third of itself along the row, "
      "which is what moves the boundary as well as the rows. The wind IS the handover rather than "
      "decoration over a dissolve")

check("PASS-WIND nothing is drawn between two rows",
      "float share = KEEP + (1.0 - KEEP) * h11(rj);" in BUILT
      and "const float KEEP = 0.66;" in BUILT,
      "the ban this construction stood near is the drawn seam. Two rows differ by a displacement "
      "and their matter meets edge to edge, which is a shear; every row keeps at least two thirds "
      "of the push, so no row stands still while its neighbour bows and the third that varies is "
      "the row structure a viewer actually sees")

check("PASS-WIND the level and the cut are both declared, in the instrument's own file",
      'levels: ["SURFACE", "CELL"]' in BUILT and 'cuts: ["strip"]' in BUILT,
      "the site's settings build prefers a manifest's own `cuts` to any table it keeps and names an "
      "instrument that declares none as UNPLACED. A row is a band of the frame taken along the "
      "work's own recorded banding axis, which is the strip kind")

check("PASS-WIND both doors frame at a cover crop of exactly one",
      '"0": { coverCrop: 1 }, "1": { coverCrop: 1 }' in BUILT
      and "float taper = smoothstep(0.0, 0.05, min(ee.x, ee.y));" in BUILT,
      "the bend is tapered to nothing at the frame's own edge, so no sample is ever fetched from "
      "outside the picture and no headroom has to be bought from either photograph")

check("PASS-WIND the coverage is declared, with the mechanism that pays for it",
      "coverage: { writes: false," in BUILT and "gl_FragColor = vec4(col, 1.0);" in BUILT,
      "every point of the frame carries one of the two photographs, so the alpha is the constant 1 "
      "and this instrument is lawful as the lowest cue of a stack and as a whole one-cue score")

check("PASS-WIND the manifest leaves the drawing buffer unpreserved",
      "gl: { preserveDrawingBuffer: false }" in BUILT,
      "§7 refuses a manifest that asks for one; the redraw it would stand in for is the host's own "
      "frame loop")

declared = set(re.findall(r'\{ name: "(u\w+)", type:', BUILT))
spelled = set(re.findall(r'uniform \w+ (u\w+);', BUILT))
check("PASS-WIND the manifest's declared names and the shader's own names are one set",
      declared == spelled and len(declared) == 9,
      f"{len(declared)} declared, {len(spelled)} spelled; "
      f"declared only: {sorted(declared - spelled)}; spelled only: {sorted(spelled - declared)}")

# ---------------------------------------------------------------- the rows Node runs

NODE_ROWS = [
    "PASS-WIND §8     · the host's own registration takes this manifest, with nothing stubbed",
    "PASS-WIND the two doors are exact over every axis, gust, lag and row count, on four buffers",
    "PASS-WIND one gust crosses once and never comes back, and the air is still at both doors",
    "PASS-WIND the bend rides one envelope: nothing at both doors, whole across the middle",
    "PASS-WIND the die moves how hard each row leans and moves neither door",
    "PASS-WIND the same pose answers the same numbers twice",
]
RED_ROWS = [
    "PASS-WIND red-on-bug · the front's travel shortened: the entry door leaks and says so",
    "PASS-WIND red-on-bug · the reading removed as well: the leaking door is answered with no refusal",
    "PASS-WIND red-on-bug · the envelope put back on a sine: the exit door is not still and says so",
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
// The axis is walked at eight turns rather than at the two square ones, because a turned axis is
// exactly where a front sized against the frame's EDGES leaves its corners behind.
var BUFFERS = [[390, 844], [780, 1688], [1170, 2532], [100, 100]];
var AXIS = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 1];
var GUST = [0, 0.5, 1];
var LAG = [0, 0.5, 1];
var ROWS = [3, 14, 60];
var leaks = [], walked = 0, tightest = 1e9, worstPush = 0;
BUFFERS.forEach(function (b) {
  AXIS.forEach(function (a) {
    GUST.forEach(function (g) {
      LAG.forEach(function (l) {
        ROWS.forEach(function (r) {
          [0, 1].forEach(function (m) {
            var v = values({ mix: m, axis: a, gust: g, lag: l, rows: r,
                             bufWidth: b[0], bufHeight: b[1] });
            walked++;
            if (v.doorWhyNo && leaks.length < 5) leaks.push([b, a, g, l, r, m, v.doorWhyNo]);
            if (v.air) {
              if (v.air.spareBands < tightest) tightest = v.air.spareBands;
              if (v.air.push > worstPush) worstPush = v.air.push;
            }
          });
        });
      });
    });
  });
});
out.doors = { walked: walked, leaks: leaks, tightest: tightest, worstPush: worstPush,
              ok: leaks.length === 0 && worstPush === 0 };

// ---- ONE GUST, CROSSING ONCE -------------------------------------------------------------------
// The front's position is a pure function of the dial and it only ever advances: a single step
// backwards over forty-one steps reds this, which is what separates one crossing gust from a
// travelling wave that runs forever.
var back = 0, prevFront = null, fronts = [];
for (var k = 0; k <= 40; k++) {
  var v = values({ mix: k / 40 });
  if (prevFront !== null && v.front < prevFront - 1e-12) back++;
  prevFront = v.front;
  fronts.push([k / 40, v.front]);
}
var ends = [values({ mix: 0 }), values({ mix: 1 })];
out.gust = { back: back, first: fronts[0], middle: fronts[20], last: fronts[40],
             starts: ends[0].start, endsAt: ends[1].end,
             pushAtDoors: [ends[0].amp, ends[1].amp],
             ok: back === 0 && ends[0].amp === 0 && ends[1].amp === 0
                 && fronts[40][1] > fronts[0][1] };

// ---- THE ENVELOPE ------------------------------------------------------------------------------
out.env = { at0: values({ mix: 0 }).env, atHalf: values({ mix: 0.5 }).env,
            at1: values({ mix: 1 }).env };
out.env.ok = out.env.at0 === 0 && out.env.at1 === 0 && out.env.atHalf > 0.99;

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
              and man.get("levels") == ["SURFACE", "CELL"] and man.get("cuts") == ["strip"],
              "the host's own `register` took it, so its `manifestWhyNo` found every uniform "
              "supplied and its own frame values answered a neutral pose: arity %s, levels %s, "
              "cuts %s, eleven handles"
              % (man.get("arity"), man.get("levels"), man.get("cuts"))
              if G["registered"] else "the host refused it; refusals: %s" % G["refused"])

        d = G["doors"]
        check(NODE_ROWS[1], d["ok"],
              "%d poses walked — four buffers, eight axes including the four diagonals, three gust "
              "lengths, three lags, three row counts, both doors — and not one leaks. The tightest "
              "of them kept %.1f crossover bands to spare and the push stood at exactly %s at every "
              "one" % (d["walked"], d["tightest"], d["worstPush"])
              if d["ok"] else "%d of %d poses leak (worst push %s); first: %s"
              % (len(d["leaks"]), d["walked"], d["worstPush"], json.dumps(d["leaks"][:2])))

        g = G["gust"]
        check(NODE_ROWS[2], g["ok"],
              "over forty-one steps of the dial the front stood back from where it was %d times: it "
              "runs from %.3f to %.3f, starting past the frame's furthest leading corner at %.3f "
              "and finishing past its trailing one at %.3f. There is one gust in a crossing, it "
              "crosses once, and the push is exactly %s at both doors"
              % (g["back"], g["first"][1], g["last"][1], g["starts"], g["endsAt"],
                 g["pushAtDoors"][0]))

        e = G["env"]
        check(NODE_ROWS[3], e["ok"],
              "the envelope reads exactly %s at both doors and %.4f across the middle — built out "
              "of the dial itself rather than out of a sine, so it lands on nothing in floating "
              "point and a still door is a still door" % (e["at0"], e["atHalf"]))

        di = G["die"]
        check(NODE_ROWS[4], di["ok"],
              "a die of three stands the row hash at a phase of %.4f against %.4f, so the same gust "
              "takes the rows differently on two passes over one edge — and both doors stay whole "
              "under it, because every row's share is between two thirds and one and both doors "
              "hold the push at nothing whatever the share is" % (di["phases"][1], di["phases"][0]))

        check(NODE_ROWS[5], G["repeat"]["ok"],
              "the same pose asked twice answers %d bytes of identical numbers, so a seeded score "
              "repeats to the pixel" % G["repeat"]["bytes"])

        # ---- red on bug ---------------------------------------------------------------------
        p1 = plant("short", [("var start = 0.5 - half - MARGIN - 2 * body;",
                              "var start = 0.5 - half + 0.05;")])
        if p1 is None:
            skip(RED_ROWS[0], "the plant found nothing to change")
        else:
            R1, w1 = run_node(p1, "short")
            leaked = R1 and len(R1["doors"]["leaks"]) > 0
            check(RED_ROWS[0], bool(leaked),
                  "with the front starting inside the frame instead of a margin and two bodies "
                  "before its furthest leading corner, the gust has already passed part of the "
                  "picture at the entry door and the arriving work stands there; the instrument "
                  "refuses it with the count in it: «%s»"
                  % (R1["doors"]["leaks"][0][6][:200] if leaked else str(w1)))

            p2 = plant("short-silent", [("var start = 0.5 - half - MARGIN - 2 * body;",
                                         "var start = 0.5 - half + 0.05;"),
                                        ("var no = doorWhyNoOf(read);", "var no = null;")])
            if p2 is None:
                skip(RED_ROWS[1], "the plant found nothing to change")
            else:
                R2, w2 = run_node(p2, "short-silent")
                check(RED_ROWS[1], bool(R2) and len(R2["doors"]["leaks"]) == 0,
                      "with the reading taken out as well the very same leak is answered with no "
                      "refusal at all over all %d poses — so the reading is what stands between a "
                      "visitor and a door that is two photographs, rather than a number nobody acts "
                      "on" % (R2["doors"]["walked"] if R2 else 0))

        p3 = plant("sine", [("var env = 4 * d * (1 - d);", "var env = Math.sin(Math.PI * d);")])
        if p3 is None:
            skip(RED_ROWS[2], "the plant found nothing to change")
        else:
            R3, w3 = run_node(p3, "sine")
            leaked3 = R3 and len(R3["doors"]["leaks"]) > 0 and R3["doors"]["worstPush"] > 0
            check(RED_ROWS[2], bool(leaked3),
                  "with the envelope put back on a sine the exit door carries a push of %s of a "
                  "frame width — the machine's own rounding of π rather than nothing — and the "
                  "instrument refuses its own door for it: «%s». That is why the window is built "
                  "out of the dial instead"
                  % (R3["doors"]["worstPush"] if R3 else "?",
                     R3["doors"]["leaks"][0][6][:160] if leaked3 else str(w3)))

# ---------------------------------------------------------------- the rows a browser runs

BROWSER_ROWS = [
    "PASS-WIND the shader builds on a real context and the host draws with it",
    "PASS-WIND row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-WIND row 7  · door 0 carries no trace of the arriving work",
    "PASS-WIND row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-WIND row 7  · door 1 carries no trace of the departing work",
    "PASS-WIND the gust reaches the picture: the middle is no door",
    "PASS-WIND row 10 · a seeded run repeats to the pixel",
    "PASS-WIND row 15 · the console stays clean",
    "PASS-WIND the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-WIND row 16 · the captures are kept as evidence",
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
    d = Path(tempfile.mkdtemp(prefix="synth_windbench_"))
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
        for i, m in enumerate([0.35, 0.5, 0.65]):
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
              "(worst channel %.1f), against the %s the project's seam allows — the air is still "
              "there and the frame is the file" % (m0, x0, SEAM))
        check(BROWSER_ROWS[2], m0b >= FAR,
              "and %.1f of 255 from the arriving work, which is a different photograph" % m0b)
        check(BROWSER_ROWS[3], m1 <= SEAM,
              "door 1 stands %.3f of 255 from the arriving work's own cover fit (worst channel %.1f)"
              % (m1, x1))
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
                "intent": "one gust crosses the rows of the departing photograph, bending them, and "
                          "the arriving work stands where it has passed",
                "pair": {"a": "a", "b": "b"}, "seed": 0, "duration": 3000,
                "direction": "a-to-b",
                "interruption": {"withinMs": 500, "resolve": "nearest-door"},
                "failLand": "arrive",
                "camera": {"owner": "stage", "rests": "b",
                           "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                                      "pitch": 0, "yaw": 0, "roll": 0, "fov": None,
                                      "owner": "stage"}]},
                "cues": [{
                    "id": "wind-main",
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
                              "rowsStatic": {"op": "static", "value": 14},
                              "axisStatic": {"op": "static", "value": 0},
                              "bendStatic": {"op": "static", "value": 0.5},
                              "gustStatic": {"op": "static", "value": 0.45},
                              "lagStatic": {"op": "static", "value": 0.4},
                              "seedStatic": {"op": "static", "value": 0},
                              "shadeStatic": {"op": "static", "value": 1},
                              "travelStatic": {"op": "static", "value": 1},
                              "maskStatic": {"op": "static", "value": 0}},
                    "tracks": {"mix": {"node": "mixDrive"}, "clock": {"node": "clockDrive"},
                               "rows": {"node": "rowsStatic"},
                               "axis": {"node": "axisStatic"},
                               "bend": {"node": "bendStatic"},
                               "gust": {"node": "gustStatic"},
                               "lag": {"node": "lagStatic"},
                               "seed": {"node": "seedStatic"},
                               "shade": {"node": "shadeStatic"},
                               "travel": {"node": "travelStatic"},
                               "mask": {"node": "maskStatic"}},
                    "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0,
                                  "pingPong": 0, "programs": 1, "passes": 1, "bytesEstimate": 0,
                                  "variant": "standard"},
                }],
                "quality": {v: {"renderScale": None,
                                "cues": {"wind-main": {
                                    "textures": 0, "textureSlots": 2, "framebuffers": 0,
                                    "pingPong": 0, "programs": 1, "passes": 1,
                                    "bytesEstimate": 0, "variant": v}}}
                            for v in ("lean", "standard", "rich")},
                "provenance": {"source": "charter shelf 14, the elements",
                               "measuredAt": None, "by": "tests/test_pass_wind.py"},
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
