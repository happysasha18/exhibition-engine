#!/usr/bin/env python3
"""PASS-API-V1 — the woven instrument on the host's frame.
Run: python3 tests/test_pass_weave.py

Root: his word 2026-08-13 23:03 — carry the woven instrument across first, with a real pair score
feeding a real instrument. docs/design/PASS-API-V1.md §7 (GPU and resources), §8 (the manifest) and
§9's conformance rows 7, 10, 14, 15 and 22 are what this file makes real; the lifecycle rows stay in
tests/test_pass_api.py and are untouched.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the strips' travel needs
  (the module's own ZOOM) — inside the project's seam threshold of 6 of 255. A door that carried a
  ten-thousandth of the other photograph would fail this, which is the point of it.

  The three poses. The host's frame is compared against the LAB MODULE's own frame, on one pose
  taken from the module through its own pose() — the same three poses lab/carrier-check.py already
  uses (the two doors and the woven middle, at second 7). Two roads of one frame, never two guesses
  at one.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path —
  never a silent pass.
"""
import base64
import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

LAB = Path(os.environ.get("TLVPHOTOS_LAB_ROOT", "/Users/sashaabramovich/tlvphotos-immersive/lab"))
# The two photographs lab/carrier-check.py itself compares on; they live in the main worktree, which
# the immersive one does not copy. Either root is read only here.
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
SCORE = LAB / "data" / "scores" / "17847744487144891__17897050660015868.json"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on
CLOCK = 7.0                # the second the comparison holds at, as the carrier's own check does
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def score_of():
    return json.loads(SCORE.read_text(encoding="utf-8"))["score"]


def scored(pair_a="a", pair_b="b"):
    """The lab's own score for this pair, with every handle the generator left untracked wired up.

    build-scores-v1.py names only `mix` and `clock` in tracks because module-contract.json publishes
    only those two; the port publishes NINE (§4.4b), so the strips, the axis, the speed, the die and
    the three voices that used to run on the module's own eased clock all reach the instrument
    instead of falling back to a default.

    THE FOUR STATICS are nodes the generator already put in the file, and it now writes their tracks
    too, so re-stating them here changes nothing — it only keeps this file honest against a score
    written before it did. Nothing there is invented.
    THE TWO VOICES are the module's own numbers, carried digit for digit out of lab/effects/weave.js:
    the strip-count breath 1 + 0.35·sin(t·0.021·TAU + 1.1) (weave.js:452) and the press resting at 1
    under a parked pointer (weave.js:466 with :236). They stand here as driver nodes rather than as
    constants inside the instrument, which is what makes the seeded repeat below mean anything.

    `bal` is deliberately NOT tracked: the balance drift is the module's IDLE life, and this score's
    intent is the crossing, where the dial owns the balance. A score that wants the drift names
    `tracks.bal` and the node is written out in this build's return."""
    s = score_of()
    s["pair"] = {"a": pair_a, "b": pair_b}
    cue = s["cues"][0]
    cue["nodes"]["axisStatic"] = {"op": "static", "value": 0,
                                  "note": "walk-v1.json steps[0].axis is 'up and down' = index 0, "
                                          "the same fact rotStatic 0 records"}
    cue["nodes"]["breath"] = {"op": "oscillate", "rate": 0.021, "phase": 1.1, "shape": "sin",
                              "in": {"source": "time"},
                              "note": "lab/effects/weave.js:452 — the strip-count drift's own rate "
                                      "and its own head start, unchanged"}
    cue["nodes"]["nMulDrive"] = {"op": "add", "in": [{"op": "static", "value": 1},
                                                     {"op": "multiply",
                                                      "in": [{"op": "static", "value": 0.35},
                                                             {"node": "breath"}]}]}
    cue["nodes"]["pressStatic"] = {"op": "static", "value": 1,
                                   "note": "weave.js:466 — the press rests at 1 under a parked "
                                           "pointer, and a scored run parks it"}
    cue["tracks"]["strips"] = {"node": "stripsStatic"}
    cue["tracks"]["speed"] = {"node": "speedStatic"}
    cue["tracks"]["seed"] = {"node": "seedStatic"}
    cue["tracks"]["axis"] = {"node": "axisStatic"}
    cue["tracks"]["nMul"] = {"node": "nMulDrive"}
    cue["tracks"]["press"] = {"node": "pressStatic"}
    return s


def coupled(pair_a="a", pair_b="b"):
    """ONE NODE FEEDING TWO CHANNELS — the fifth law of the grammar, on the real instrument. The one
    breath above drives the strip count AND the press, so the two cannot disagree; the row reads both
    handles off the diagnostic surface and solves them back to the single value they came from."""
    s = scored(pair_a, pair_b)
    cue = s["cues"][0]
    cue["nodes"]["pressDrive"] = {"op": "add", "in": [
        {"op": "static", "value": 1},
        {"op": "multiply", "in": [{"op": "static", "value": 0.30},
                                  {"op": "clamp", "in": {"node": "breath"}, "min": 0, "max": 1}]}]}
    cue["tracks"]["press"] = {"node": "pressDrive"}
    return s


def with_statics(strips=None, nMul=None, press=None, pair_a="a", pair_b="b"):
    """The same score with one voice moved. Used to prove a handle reaches the PICTURE and not only
    the diagnostic record — reading a driver's value back off the surface says the graph evaluated,
    and says nothing about whether the instrument obeyed it.

    `strips` is raised to 28, the module's own declared default, for these runs alone: this pair's
    score names 8, and on a 390-point frame the count lands at clamp(8 * nMul * 0.5, 6, 64), whose
    floor of 6 swallows most of the breath's range. At 28 the same range moves the count from about
    ten strips to about twenty, which is the difference the row is trying to see."""
    s = scored(pair_a, pair_b)
    cue = s["cues"][0]
    if strips is not None:
        cue["nodes"]["stripsAlt"] = {"op": "static", "value": strips}
        cue["tracks"]["strips"] = {"node": "stripsAlt"}
    if nMul is not None:
        cue["nodes"]["nMulAlt"] = {"op": "static", "value": nMul}
        cue["tracks"]["nMul"] = {"node": "nMulAlt"}
    if press is not None:
        cue["nodes"]["pressAlt"] = {"op": "static", "value": press}
        cue["tracks"]["press"] = {"node": "pressAlt"}
    return s


def breath_at(seconds):
    """The very formula the node above carries, computed here so the row states its number instead of
    reading one back and calling it correct."""
    return math.sin(2 * math.pi * 0.021 * seconds + 1.1)


# ---------------------------------------------------------------- bake once
# The site's own `pass` record carries the pair's score. This is the WHOLE delivery road: a site
# writes it into its own site.json, engine/build.py passes the block through into config.json as
# DATA and judges nothing in it, and the client reads it at declare time. No engine rebuild, no new
# asset, no new road — a new score for a pair is a content change.
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passweave_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")
# Since 2026-08-14 the instruments ship in their OWN built file, which the host fetches by address,
# version and digest. A row about the HOST reads LAYER; a row about the woven instrument's own
# mathematics reads its region of PACK. Splitting the two is what lets the boundary row in
# test_pass_pack.py demand that no instrument name appear in the host at all.
PACK = (TMP / "pass-pack.js").read_text(encoding="utf-8")
WEAVE = PACK.split("function weaveInstrument()")[1].split("function matterInstrument()")[0]

# ---------------------------------------------------------------- string rows

check("PASS-WEAVE the host binds uniforms by declared name, never by position or a written list",
      "u.name" in LAYER and "getUniformLocation(p, u.name)" in LAYER
      and "gl.uniform1f(U.uNv" not in LAYER,
      "the lab carrier names one instrument's six uniforms literally; the host must read the manifest")

check("PASS-WEAVE a shader that already carries its own version header receives no second one",
      'if (/^\\s*#version\\b/.test(src)) return src;' in LAYER,
      "two lab modules ship GLSL ES 3.00 already — a second header is a build-time red")

check("PASS-WEAVE the host's own context leaves the drawing buffer unpreserved",
      "preserveDrawingBuffer: false" in LAYER,
      "one canvas, one context, nothing kept between frames (§7)")

check("PASS-WEAVE the woven instrument creates no context, no canvas, no loop and no listener",
      all(s not in WEAVE
          for s in ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
                    "performance.now", "Date.now", "new Image"]),
      "§1.2's fence, read against the instrument's own region of the file")

check("PASS-WEAVE every handle the instrument publishes is a handle a score can drive",
      all(('%s: { min' % h) in WEAVE for h in
          ["mix", "clock", "strips", "axis", "speed", "seed", "nMul", "press", "bal"]),
      "§4.4b: a handle that keeps its own clock or its own roll makes the determinism row red — "
      "`nMul`, `press` and `bal` were the three that answered to no track until 2026-08-14")

check("PASS-WEAVE the instrument reads its balance, its strip-count breath and its press from handles",
      "nMul: h.nMul, press: h.press" in WEAVE
      and "typeof h.bal === \"number\" ? h.bal :" in WEAVE
      and WEAVE.count("nMul: 1, press: 1") == 1,
      "the two constants standing where the module's own eased clock used to run are gone — the one "
      "remaining pair is the manifest's neutral pose, which is a pose and not a channel")

check("PASS-WEAVE the score's road into the walk needs no engine rebuild",
      "function passScoreFor" in (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8"),
      "the site's pass record carries scores keyed by the pair; the bake passes the block through as data")

# The delivery road's own row: what a site wrote into site.json is what the served settings file
# carries, byte for byte, with the bake judging none of it.
served = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
check("PASS-WEAVE the site's pass record reaches the served settings file untouched",
      served.get("pass") == build_site.SITE_CONFIG["pass"],
      f"config.json carries {served.get('pass')} exactly as site.json wrote it")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-WEAVE row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-WEAVE row 7  · door 0 carries no trace of the arriving work",
    "PASS-WEAVE row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-WEAVE row 7  · door 1 carries no trace of the departing work",
    "PASS-WEAVE the host's frame and the lab module's frame agree: door-0",
    "PASS-WEAVE the host's frame and the lab module's frame agree: the woven middle",
    "PASS-WEAVE the host's frame and the lab module's frame agree: door-1",
    "PASS-WEAVE row 10 · a seeded run repeats to the pixel",
    "PASS-WEAVE row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-WEAVE row 15 · the console stays clean",
    "PASS-WEAVE row 22 · the census shows granted against declared, and neither overruns",
    "PASS-WEAVE §7 · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-WEAVE §7 · a manifest naming a uniform the host cannot supply is refused, with its reason",
    "PASS-WEAVE §7 · one canvas, one context, two source textures, one pass a frame",
    "PASS-WEAVE the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-WEAVE §2.5 · an interruption at each of five instants lands inside the score's own budget",
    "PASS-WEAVE §2.5 · every handle stands on its door when the cadence ends",
    "PASS-WEAVE §2.5 · the cadence walks to the NEARER door, not always the same one",
    "PASS-WEAVE row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-WEAVE §5     · one node drives two handles of the real instrument, and moves both",
    "PASS-WEAVE §4.4b  · the strip-count breath and the press reach the PICTURE, not just the record",
]

# §2.5's landing slack. The host's own force-end is a timer at the score's `withinMs`; a browser
# fires a timer a little late and the frame that draws the door is scheduled after it, so the
# measured landing is allowed this much past the budget. It is a scheduling number, not a pacing
# one — the pacing number is `withinMs` and it belongs to the score.
LAND_SLACK_MS = 100

WALK_ROWS = [
    "PASS-WEAVE the walk reads the pair's own score and freezes it onto the command",
    "PASS-WEAVE the score's cue names the instrument, and that instrument takes the command",
    "PASS-WEAVE the pass over a scored pair lands in exactly one dock, curtain down",
    "PASS-WEAVE a pair with no score of its own keeps the walk's own glide",
]

# A score per pair covers nothing on a dealt walk: the walk deals its works afresh each visit, and a
# 121-work collection holds about fourteen thousand ordered pairs. These rows drive the road that
# does cover it — one template per instrument, one row of measured numbers per ordered pair, filled
# at the moment a transition is declared. The lab's own template and table are the material.
TABLE_ROWS = [
    "PASS-TABLE the template filled from a pair's row is a score the checker takes",
    "PASS-TABLE the filled score is the very score the per-pair builder wrote for that pair",
    "PASS-TABLE a row naming a slot the template lacks is refused whole, and names it",
    "PASS-TABLE a row whose readiness stands under the table's floor is refused, and says so",
    "PASS-TABLE a pair with a row reaches the walk with a score, and the instrument takes it",
    "PASS-TABLE a pair with no row hands back nothing, and the walk's own glide runs",
]

TEMPLATE = LAB / "data" / "scores" / "template-weave.json"
TABLE = LAB / "data" / "scores" / "table-weave.json"

missing = [str(p) for p in ([SCORE, TEMPLATE, TABLE] + PHOTOS + [LAB / "effects" / "weave.js"])
           if not p.exists()]


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return path


def diff(p, q):
    from PIL import Image, ImageChops, ImageStat
    a = Image.open(p).convert("RGB")
    c = Image.open(q).convert("RGB")
    if a.size != c.size:
        return 255.0, 255.0
    st = ImageStat.Stat(ImageChops.difference(a, c))
    return sum(st.mean) / 3.0, max(m for _, m in st.extrema)


def work_in_the_frame(src, w, h, zoom):
    """The work as the instrument seats it: cover-fit, then the centre crop the strips' travel is
    paid for with (the module's own ZOOM). The very same construction lab/carrier-check.py uses, so
    the two checks judge a door the same way."""
    from PIL import Image
    im = Image.open(src).convert("RGB")
    iw, ih = im.size
    fa, ia = w / float(h), iw / float(ih)
    sw, sh = (ih * fa, float(ih)) if ia > fa else (float(iw), iw / fa)
    sw /= zoom
    sh /= zoom
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
    """The bench's own served root: the BUILT pass-layer.js (the real artifact, namespace applied and
    comments stripped), the lab module unchanged, the two photographs, and the page that stands the
    two roads of one frame side by side."""
    d = Path(tempfile.mkdtemp(prefix="synth_weavebench_"))
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    # The host fetches its pack by address and weighs its bytes, so the bench root serves the built
    # pack beside the built host: the same two files a visitor gets, unaltered.
    shutil.copy2(TMP / "pass-pack.js", d / "pass-pack.js")
    shutil.copy2(LAB / "effects" / "weave.js", d / "weave.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_weave.html", d / "index.html")
    return d


def ready(br, tries=60):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in BROWSER_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_weaveshots_"))
    BENCH = bench_dir()
    SCORE_JSON = json.dumps(scored())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            else:
                zoom = float(br.evaluate("String(window.LAB.branchSource.weave.ZOOM)"))
                br.evaluate("window.__clock(%r); 0" % CLOCK)
                br.sleep(0.9)

                # ---- the three poses: the host's frame beside the lab module's ------------------
                pairs = []
                for name, v in (("door-0", 0.0), ("mid", 0.5), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.9)
                    br.evaluate("window.__hostDraw(); 0")
                    br.sleep(0.1)
                    br.evaluate("window.__show('host'); 0")
                    br.sleep(0.2)
                    ph = png(br, SHOTS / (name + "-host.png"))
                    br.evaluate("window.__show('module'); 0")
                    br.sleep(0.2)
                    pm = png(br, SHOTS / (name + "-module.png"))
                    pairs.append((name, ph, pm))

                shots = {n: h for n, h, _ in pairs}
                w = int(br.evaluate("String(window.__exPass.bench.make() && "
                                    "document.querySelector('canvas').width)"))
                h = int(br.evaluate("String(document.querySelector('canvas').height)"))
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, zoom)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, zoom)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), worst channel {amx}")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[i * 2 + 1], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                for i, (name, ph, pm) in enumerate(pairs):
                    m, mx = diff(ph, pm)
                    check(BROWSER_ROWS[4 + i], m <= SAME,
                          f"{name}: mean {m:.4f} of 255 (threshold {SAME}), worst channel {mx}")

                # ---- the real transaction road, and the seeded repeat ---------------------------
                # One command of the shape the bundle freezes, carrying the pair's own score. The
                # host arms both works off the walk markup, builds the programme from the manifest,
                # raises the curtain and runs its own frame loop; the run is pinned to one instant so
                # the same instant can be photographed twice.
                br.evaluate("window.__show('host'); 0")
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                br.sleep(0.3)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                second = png(br, SHOTS / "seeded-2.png")
                m, mx = diff(first, second)
                check(BROWSER_ROWS[7], took["took"] and m == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {m} worst channel {mx}")

                # ---- ten runs, and the baseline ------------------------------------------------
                base_c = rep1["census"]
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: 2.0, progress: 0.3});" % SCORE_JSON)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.4)
                after = js(br, "return window.__report();")["census"]
                same = (after["textures"] == base_c["textures"] == 2
                        and after["programs"] == base_c["programs"] == 1
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"] == 1
                        and after["contexts"] == base_c["contexts"] == 1)
                check(BROWSER_ROWS[8], same,
                      f"before={base_c['textures']}/{base_c['programs']}/{base_c['framebuffers']} "
                      f"after ten runs={after['textures']}/{after['programs']}/{after['framebuffers']} "
                      f"(textures/programmes/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[9], not errs, "; ".join(errs)[:200])

                # ---- the census against the declaration ----------------------------------------
                res = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[10],
                      res["declared"] and res["over"] is False
                      and res["granted"]["programs"] == res["declared"]["programs"]
                      and res["granted"]["textures"] == res["declared"]["textures"]
                      and res["granted"]["framebuffers"] == res["declared"]["framebuffers"]
                      and res["granted"]["bytes"] == res["declared"]["bytesEstimate"],
                      f"declared={res['declared']} granted={res['granted']}")

                # ---- the two manifest refusals -------------------------------------------------
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('weave')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'weave-preserve', manifest:m,
                      values:function(){return {duty:0,amp:0,nV:8,rot:0};}, fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[11],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "weave-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('weave')));
                  m.passes[0].uniforms.push({name:'uPointer', type:'vec2', source:'pointer'});
                  var ok = window.__exPass.bench.register({name:'weave-pointer', manifest:m,
                      values:function(){return {duty:0,amp:0,nV:8,rot:0};}, fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[12],
                      r["ok"] is False and r["why"] and "uPointer" in r["why"]
                      and "cannot supply" in r["why"] and "weave-pointer" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the hardware, counted where each thing is made -----------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.6)
                c = js(br, "return window.__report();")
                cen = c["census"]
                check(BROWSER_ROWS[13],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}")

                # ---- curtain up, one pass drawn, exactly one dock -------------------------------
                # The pin comes off, so the pass runs to its own end door and the instrument settles
                # of its own accord — the whole road, from the offer to the single dock.
                # The standing transaction is ended and LET LAND before the hooks are cleared: since
                # 2026-08-14 a cancel plays the interruption cadence, so its own dock arrives a few
                # hundred milliseconds later. Clearing first would have left that dock counted
                # against the pass this row is actually about.
                br.evaluate("window.__cancel('before the whole pass'); 0")
                for _ in range(60):
                    if js(br, "return window.__report().state;") == "idle":
                        break
                    br.sleep(0.05)
                br.evaluate("window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
                took = js(br, "return window.__offer(%s, {});" % SCORE_JSON)
                br.sleep(0.5)
                mid = js(br, "return {state: window.__report().state, "
                             "curtains: window.__hooks.curtains.slice()};")
                for _ in range(60):
                    if js(br, "return window.__report().state;") == "idle":
                        break
                    br.sleep(0.1)
                end = js(br, "return {state: window.__report().state, docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                check(BROWSER_ROWS[14],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                # ---- row 9: the camera through the whole pass ----------------------------------
                # Read off the RUN THAT JUST LANDED. This score's flight is a rest at the neutral
                # pose, so the pass never leaves it — which is exactly what "rests on B" asks of a
                # score that authors no dolly. The row reads the POSE, never the picture.
                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[18],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} "
                      f"rest={cam['rest']} handoffs={cam['handoffs']} tolerances={cam['tol']}")

                # ---- §2.5: the interruption cadence, at five instants ---------------------------
                # The pass is pinned at each instant in turn, then interrupted. The host reads the
                # score's own budget, walks every handle to its nearest door on that handle's own
                # envelope, force-ends at the deadline and lands through the one dock. Everything
                # below is read off the host's own record of what it actually did.
                WITHIN = score_of()["interruption"]["withinMs"]
                lands = []
                for at in (0.1, 0.3, 0.5, 0.7, 0.9):
                    br.evaluate("window.__hooks.docks.length = 0; "
                                "window.__hooks.curtains.length = 0; 0")
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.3)
                    js(br, "window.__cancel('row-19 at %r'); return null;" % at)
                    for _ in range(60):
                        if js(br, "return window.__report().state;") == "idle":
                            break
                        br.sleep(0.05)
                    r = js(br, "var rep = window.__report(); "
                               "return {cadence: rep.cadence, state: rep.state, "
                               "docks: window.__hooks.docks.length, "
                               "curtains: window.__hooks.curtains.slice()};")
                    lands.append({"at": at, "r": r})

                inside = [L for L in lands
                          if L["r"]["cadence"] and L["r"]["cadence"]["ended"]
                          and L["r"]["cadence"]["landedInMs"] <= WITHIN + LAND_SLACK_MS
                          and L["r"]["state"] == "idle" and L["r"]["docks"] == 1
                          and L["r"]["curtains"][-1] is False]
                check(BROWSER_ROWS[15], len(inside) == 5,
                      "budget %d ms + %d ms of scheduling slack; landings "
                      % (WITHIN, LAND_SLACK_MS)
                      + ", ".join("%s→%s ms (door %s, %d dock)"
                                  % (L["at"],
                                     L["r"]["cadence"] and L["r"]["cadence"]["landedInMs"],
                                     L["r"]["cadence"] and L["r"]["cadence"]["door"],
                                     L["r"]["docks"]) for L in lands))

                # EVERY HANDLE AT A DOOR. The host writes down, per handle, what the door wanted and
                # where the handle actually stood when the cadence ended.
                measured = []
                for L in lands:
                    for h, v in ((L["r"]["cadence"] or {}).get("atDoor") or {}).items():
                        if v.get("off") is None:
                            continue
                        measured.append((v["off"], "%s at %s" % (h, L["at"])))
                # Eight of the nine handles carry a number at a door; `bal` is the open one this
                # score leaves to the dial, so it has no door value of its own to be measured
                # against. Five landings therefore owe forty readings, and a row that read none
                # would be vacuous — so the count is asserted alongside the distance.
                worst = max(measured) if measured else (255.0, "nothing was measured at all")
                check(BROWSER_ROWS[16], len(measured) == 40 and worst[0] <= 1e-9,
                      f"{len(measured)} handle readings across five landings; the furthest any "
                      f"handle finished from its door was {worst[0]} ({worst[1]}) — the doors are "
                      f"exact, so the bar is 1e-09")

                doors = [(L["at"], (L["r"]["cadence"] or {}).get("door")) for L in lands]
                check(BROWSER_ROWS[17],
                      [d for _, d in doors] == ["in", "in", "in", "out", "out"],
                      f"nearest door per instant: {doors} — the dial's own two ends are 0 and 1, so "
                      f"0.5 and below walks back to «in» and past it walks on to «out»")

                # ---- §5: one node, two handles, on the real instrument -------------------------
                # The one breath drives the strip count and the press together. Read at two clocks:
                # both move, and both stand exactly where that single value puts them.
                COUPLED = json.dumps(coupled())
                seen = []
                for sec in (1.5, 13.0):
                    js(br, "return window.__offer(%s, {clock: %r, progress: 0.5});" % (COUPLED, sec))
                    br.sleep(0.4)
                    seen.append(js(br, "return window.__report().handles;"))
                    br.evaluate("window.__cancel('coupled'); 0")
                    br.sleep(0.7)
                want = []
                for sec in (1.5, 13.0):
                    b = breath_at(sec)
                    want.append({"nMul": 1 + 0.35 * b, "press": 1 + 0.30 * max(0.0, min(1.0, b))})
                moved = (abs(seen[0]["nMul"] - seen[1]["nMul"]) > 1e-6
                         and abs(seen[0]["press"] - seen[1]["press"]) > 1e-6)
                exact = all(abs(seen[i]["nMul"] - want[i]["nMul"]) <= 1e-9
                            and abs(seen[i]["press"] - want[i]["press"]) <= 1e-9 for i in (0, 1))
                check(BROWSER_ROWS[19], moved and exact,
                      f"at 1.5 s {seen[0]['nMul']:.9f}/{seen[0]['press']:.9f}, at 13 s "
                      f"{seen[1]['nMul']:.9f}/{seen[1]['press']:.9f} — wanted "
                      f"{want[0]['nMul']:.9f}/{want[0]['press']:.9f} and "
                      f"{want[1]['nMul']:.9f}/{want[1]['press']:.9f} from the one breath node")

                # ---- §4.4b: the two voices reach the picture ------------------------------------
                # A handle read back off the diagnostic surface proves the GRAPH evaluated it. It
                # says nothing about whether the instrument obeyed it — a port that kept its
                # constants would still report the driver's number. So these three runs differ by
                # exactly one voice each and are photographed: a picture that did not move is a
                # handle the instrument is not actually reading.
                br.evaluate("window.__show('host'); 0")
                shot = {}
                for name, s_ in (("base", with_statics(strips=28, nMul=1.0, press=1.0)),
                                 ("breath", with_statics(strips=28, nMul=1.4, press=1.0)),
                                 ("press", with_statics(strips=28, nMul=1.0, press=1.30))):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % json.dumps(s_))
                    br.sleep(0.7)
                    shot[name] = png(br, SHOTS / ("voice-" + name + ".png"))
                    br.evaluate("window.__cancel('voice row'); 0")
                    br.sleep(0.7)
                dBreath, mxBreath = diff(shot["base"], shot["breath"])
                dPress, mxPress = diff(shot["base"], shot["press"])
                # The bar is the project's own seam threshold, 6 of 255: a difference smaller than
                # that is what the door rows call "the same picture", so a voice must move the frame
                # by more than the seam to count as having reached it.
                check(BROWSER_ROWS[20], dBreath > SEAM and dPress > SEAM,
                      f"the strip-count breath at 1.0 against 1.4 moves the frame by {dBreath:.4f} "
                      f"of 255 (worst channel {mxBreath}); the press at 1 against 1.30 moves it by "
                      f"{dPress:.4f} (worst channel {mxPress}); the seam threshold is {SEAM}")

    shutil.rmtree(BENCH, ignore_errors=True)
    shutil.rmtree(SHOTS, ignore_errors=True)

# ---------------------------------------------------------------- the walk's own road
# The score arriving at a real visitor, on the baked site: the settings file carries it, declare
# freezes it onto the command, and the instrument the cue names is the one that takes the command.
if not chrome_available():
    for r in WALK_ROWS + TABLE_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in WALK_ROWS + TABLE_ROWS:
        skip(r, "the lab tree is read-only source material and is absent here: " + missing[0])
else:
    def enter(br, base):
        # A returning visitor is put back where they were, so the door is not always standing; the
        # second entry of this row is exactly such a return.
        if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
            br.click(".exd-window", settle=1.4)
        for _ in range(25):
            if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                           "&& !document.documentElement.classList.contains('ex-face'))") == "true":
                break
            br.sleep(0.2)
        br.sleep(0.4)
        br.key("ArrowDown")           # the one step that makes the client fetch pass-layer.js
        for _ in range(30):
            if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
                return True
            br.sleep(0.2)
        return False

    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base)
            # The pair the visitor is ACTUALLY walking over, read from the walk itself: the order is
            # the visitor's own and no test may pin it.
            WORKS = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                           ".map(function(e){return e.dataset.id;}).slice(0,2);")
            PAIR_KEY = "__".join(WORKS)

            # THE SCORE ARRIVES WITHOUT A REBUILD. Nothing is baked again: the served settings file
            # is rewritten on disk with a score for the pair this visitor walks over, and the walk is
            # entered afresh. That is the whole delivery road, and this is its proof.
            cfg = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
            cfg["pass"]["scores"] = {PAIR_KEY: scored(WORKS[0], WORKS[1])}
            (TMP / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2,
                                                        sort_keys=True) + "\n", encoding="utf-8")
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base) and armed
            shown = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                           ".map(function(e){return e.dataset.id;});")

            walkable = armed and WORKS[0] in shown and WORKS[1] in shown
            for r_ in ([] if walkable else WALK_ROWS):
                skip(r_, f"the walk never registered a host, or re-hung without the pair: "
                         f"armed={armed} pair={WORKS} shown={shown[:4]}")

            if walkable:
                r = js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var B = document.querySelector('.exh-frame[data-id="%s"]');
                  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                             kind:'step', cause:'weave-road', velocity:0});
                  window.__wcmd = cmd;
                  return {got: !!cmd, hasScore: !!(cmd && cmd.score),
                          schema: cmd && cmd.score ? cmd.score.schema : null,
                          cue: cmd && cmd.score && cmd.score.cues ? cmd.score.cues[0].instrument.id : null,
                          duration: cmd && cmd.score ? cmd.score.duration : null};
                """ % (WORKS[0], WORKS[1]))
                check(WALK_ROWS[0],
                      r["got"] and r["hasScore"] and r["schema"] == 2 and r["cue"] == "weave"
                      and r["duration"] == 3000,
                      f"command={r}")
                br.sleep(0.15)

                r = js(br, """
                  var marks = {docks:0, curtains:[]};
                  var took = window.__exPass.layer().offer(window.__wcmd, {
                    dock: function(){ marks.docks++; },
                    glide: function(){ marks.glide = true; },
                    curtain: function(on){ marks.curtains.push(!!on); },
                    mark: function(){}});
                  window.__wmarks = marks;
                  return {took: took};
                """)
                br.sleep(0.6)
                after = js(br, """
                  var rep = window.__exPass.host.report();
                  return {took: true, instrument: rep.instrument, state: rep.state,
                          canvases: document.querySelectorAll('canvas').length,
                          marks: window.__wmarks,
                          events: rep.events.map(function(e){return e.name;}).slice(-8)};
                """)
                check(WALK_ROWS[1],
                      r["took"] is True and after["canvases"] >= 1
                      and after["marks"]["curtains"][:1] == [True],
                      f"took={r['took']} after={after}")
                for _ in range(60):
                    if js(br, "return window.__exPass.host.report().state;") == "idle":
                        break
                    br.sleep(0.1)
                landed = js(br, """
                  var rep = window.__exPass.host.report();
                  return {docks: window.__wmarks.docks, curtains: window.__wmarks.curtains,
                          events: rep.events.map(function(e){return e.name;}).slice(-8),
                          state: rep.state};
                """)
                check(WALK_ROWS[2],
                      landed["docks"] == 1 and landed["state"] == "idle"
                      and landed["curtains"][-1] is False and "docked" in landed["events"],
                      f"landed={landed}")

                # The SAME two works walked the other way. The key names an ordered pair — A→B is not
                # B→A, which is the direction the charter's model asks for — so this crossing has no
                # score of its own: nothing is frozen onto the command, no cue names an instrument, the
                # host declines the offer outright and the walk's own glide takes it.
                r = js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var B = document.querySelector('.exh-frame[data-id="%s"]');
                  var cmd = window.__exPass.adapter.declare({fromEl:B, toEl:A, dir:-1, span:100,
                                                             kind:'step', cause:'no-score', velocity:0});
                  var seen = {glide:false, curtains:[]};
                  window.__exPass.layer().offer(cmd, {dock:function(){},
                    glide:function(){ seen.glide = true; },
                    curtain:function(on){ seen.curtains.push(!!on); }, mark:function(){}});
                  return {score: cmd ? cmd.score : 'no command', glide: seen.glide,
                          curtains: seen.curtains};
                """ % (WORKS[0], WORKS[1]))
                check(WALK_ROWS[3],
                      r["score"] is None and r["glide"] is True and r["curtains"] == [],
                      f"score={r['score']} glide={r['glide']} curtains={r['curtains']}")

            # ---- the template and the table ------------------------------------------------
            # The settings file is rewritten once more, this time with NO score of any pair's own:
            # only the lab's template, and a table of rows. Everything the visitor gets from here
            # on is filled at declare time from four numbers.
            template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
            table = json.loads(TABLE.read_text(encoding="utf-8"))
            LAB_KEY = json.loads(SCORE.read_text(encoding="utf-8"))["pairKey"]
            lab_row = (table.get("rows") or {}).get(LAB_KEY)

            if lab_row is None:
                for r_ in TABLE_ROWS:
                    skip(r_, f"the lab table carries no row for its own scored pair {LAB_KEY}")
            else:
                # The visitor's own pair borrows the lab pair's numbers — the same measured row,
                # under the key this walk actually steps over. The two planted rows are the bad
                # ones: one names a slot the template has never heard of, one stands under the
                # table's own readiness floor.
                rows = {LAB_KEY: lab_row, PAIR_KEY: dict(lab_row),
                        "stray__row": dict(lab_row, tilt=0.5),
                        "unready__row": dict(lab_row,
                                             readiness=round(table["readinessFloor"] - 0.01, 4))}
                cfg = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
                cfg["pass"].pop("scores", None)
                cfg["pass"]["scoreTemplates"] = {template["instrument"]: template}
                cfg["pass"]["scoreTables"] = {template["instrument"]: dict(table, rows=rows)}
                (TMP / "config.json").write_text(
                    json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
                br.navigate(base + "/")
                br.sleep(0.8)
                armed = enter(br, base)
                shown = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                               ".map(function(e){return e.dataset.id;});")

                r = js(br, """
                  var s = window.__exPass.fill('%s');
                  var chk = window.__exPass.score(s);
                  return {ok: !!s, read: chk.read || null, why: chk.why || null,
                          pair: s ? s.pair : null, seed: s ? s.seed : null,
                          strips: s ? s.cues[0].nodes.stripsStatic.value : null,
                          axis: s ? s.cues[0].nodes.axisStatic.value : null,
                          instrument: s ? s.cues[0].instrument.id : null};
                """ % PAIR_KEY)
                check(TABLE_ROWS[0],
                      r["ok"] and r["read"] == 2 and r["instrument"] == "weave"
                      and r["pair"] == {"a": PAIR_KEY.split("__")[0], "b": PAIR_KEY.split("__")[1]}
                      and r["seed"] == lab_row["seed"] and r["strips"] == lab_row["strips"]
                      and r["axis"] == lab_row["axis"],
                      f"filled={r} row={lab_row}")

                # THE TWO ROADS MEET. The lab pair is the one pair that has both a row and a score
                # the per-pair builder wrote in full. Filled here, in the product, from four
                # numbers, it must be that score — every field, to the last node.
                filled = js(br, "return window.__exPass.fill('%s');" % LAB_KEY)
                built = score_of()
                check(TABLE_ROWS[1], filled == built,
                      "the filled score differs from lab/data/scores/%s.json" % LAB_KEY
                      if filled != built else "identical, %d B of score from a %d-field row"
                      % (len(json.dumps(built, separators=(",", ":"))), len(lab_row)))

                r = js(br, """
                  var s = window.__exPass.fill('stray__row');
                  var said = window.__exPass.report().refusals.filter(function(x){
                    return x.what === 'row' && x.name === 'stray__row'; });
                  return {score: s, why: said.length ? said[said.length - 1].why : null};
                """)
                check(TABLE_ROWS[2],
                      r["score"] is None and "tilt" in (r["why"] or "")
                      and "slot the template lacks" in (r["why"] or ""),
                      f"filled={'a whole score' if r['score'] else 'nothing'} why={r['why']!r}")

                r = js(br, """
                  var s = window.__exPass.fill('unready__row');
                  var said = window.__exPass.report().refusals.filter(function(x){
                    return x.what === 'row' && x.name === 'unready__row'; });
                  return {score: s, why: said.length ? said[said.length - 1].why : null};
                """)
                check(TABLE_ROWS[3],
                      r["score"] is None and "under the floor" in (r["why"] or ""),
                      f"filled={'a whole score' if r['score'] else 'nothing'} why={r['why']!r}")

                walkable = armed and WORKS[0] in shown and WORKS[1] in shown
                for r_ in ([] if walkable else TABLE_ROWS[4:]):
                    skip(r_, f"the walk never registered a host, or re-hung without the pair: "
                             f"armed={armed} pair={WORKS} shown={shown[:4]}")
                if walkable:
                    r = js(br, """
                      var A = document.querySelector('.exh-frame[data-id="%s"]');
                      var B = document.querySelector('.exh-frame[data-id="%s"]');
                      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                                 kind:'step', cause:'table-road',
                                                                 velocity:0});
                      var seen = {curtains: [], docks: 0};
                      var took = cmd ? window.__exPass.layer().offer(cmd, {
                        dock: function(){ seen.docks++; },
                        glide: function(){ seen.glide = true; },
                        curtain: function(on){ seen.curtains.push(!!on); },
                        mark: function(){}}) : false;
                      window.__tseen = seen;
                      return {hasScore: !!(cmd && cmd.score),
                              schema: cmd && cmd.score ? cmd.score.schema : null,
                              seed: cmd && cmd.score ? cmd.score.seed : null,
                              took: took,
                              instrument: window.__exPass.host.report().instrument};
                    """ % (WORKS[0], WORKS[1]))
                    # the curtain rises after the prepare, not inside the offer call, so it is read
                    # once the pass has actually run its course
                    for _ in range(60):
                        if js(br, "return window.__exPass.host.report().state;") == "idle":
                            break
                        br.sleep(0.1)
                    seen = js(br, "return window.__tseen;")
                    check(TABLE_ROWS[4],
                          r["hasScore"] and r["schema"] == 2 and r["seed"] == lab_row["seed"]
                          and r["took"] is True and seen["curtains"] == [True, False]
                          and seen["docks"] == 1 and r["instrument"] == "weave",
                          f"declared={r} seen={seen}")

                    r = js(br, """
                      var A = document.querySelector('.exh-frame[data-id="%s"]');
                      var B = document.querySelector('.exh-frame[data-id="%s"]');
                      var cmd = window.__exPass.adapter.declare({fromEl:B, toEl:A, dir:-1, span:100,
                                                                 kind:'step', cause:'no-row',
                                                                 velocity:0});
                      var seen = {glide:false, curtains:[]};
                      window.__exPass.layer().offer(cmd, {dock:function(){},
                        glide:function(){ seen.glide = true; },
                        curtain:function(on){ seen.curtains.push(!!on); }, mark:function(){}});
                      return {score: cmd ? cmd.score : 'no command', glide: seen.glide,
                              curtains: seen.curtains};
                    """ % (WORKS[0], WORKS[1]))
                    check(TABLE_ROWS[5],
                          r["score"] is None and r["glide"] is True and r["curtains"] == [],
                          f"score={r['score']} glide={r['glide']} curtains={r['curtains']}")

shutil.rmtree(TMP, ignore_errors=True)

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
