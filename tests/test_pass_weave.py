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
    """The lab's own score for this pair, with the four handles the generator left untracked wired to
    the static nodes it already wrote. build-scores-v1.py names only `mix` and `clock` in tracks
    because module-contract.json publishes only those two; the port publishes all six (§4.4b), so the
    strips, the axis, the speed and the die reach the instrument instead of falling back to the
    module's own defaults. Nothing is invented: every value is a node the generator already put in
    the file."""
    s = score_of()
    s["pair"] = {"a": pair_a, "b": pair_b}
    cue = s["cues"][0]
    cue["nodes"]["axisStatic"] = {"op": "static", "value": 0,
                                  "note": "walk-v1.json steps[0].axis is 'up and down' = index 0, "
                                          "the same fact rotStatic 0 records"}
    cue["tracks"]["strips"] = {"node": "stripsStatic"}
    cue["tracks"]["speed"] = {"node": "speedStatic"}
    cue["tracks"]["seed"] = {"node": "seedStatic"}
    cue["tracks"]["axis"] = {"node": "axisStatic"}
    return s


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
      all(s not in LAYER.split("function weaveInstrument()")[1].split("register(weaveInstrument())")[0]
          for s in ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
                    "performance.now", "Date.now", "new Image"]),
      "§1.2's fence, read against the instrument's own region of the file")

check("PASS-WEAVE every handle the instrument publishes is a handle a score can drive",
      all(('%s: { min' % h) in LAYER for h in ["mix", "clock", "strips", "axis", "speed", "seed"]),
      "§4.4b: a handle that keeps its own clock or its own roll makes the determinism row red")

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
]

WALK_ROWS = [
    "PASS-WEAVE the walk reads the pair's own score and freezes it onto the command",
    "PASS-WEAVE the score's cue names the instrument, and that instrument takes the command",
    "PASS-WEAVE the pass over a scored pair lands in exactly one dock, curtain down",
    "PASS-WEAVE a pair with no score of its own keeps the walk's own glide",
]

missing = [str(p) for p in ([SCORE] + PHOTOS + [LAB / "effects" / "weave.js"]) if not p.exists()]


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
                br.evaluate("window.__cancel('before the whole pass'); "
                            "window.__hooks.docks.length = 0; window.__hooks.curtains.length = 0; 0")
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

    shutil.rmtree(BENCH, ignore_errors=True)
    shutil.rmtree(SHOTS, ignore_errors=True)

# ---------------------------------------------------------------- the walk's own road
# The score arriving at a real visitor, on the baked site: the settings file carries it, declare
# freezes it onto the command, and the instrument the cue names is the one that takes the command.
if not chrome_available():
    for r in WALK_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif missing:
    for r in WALK_ROWS:
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
