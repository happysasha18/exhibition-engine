#!/usr/bin/env python3
"""PASS-API-V1 — the meshing instrument on the host's frame.
Run: python3 tests/test_pass_gears.py

Root: his word 2026-08-14 08:39 — continue the effect farm, integrate only green conforming
instruments. `gears` is the one picked because the measured pair on the demonstration path travels
from angular structure to ring structure, and meshing repeat counts are what carries that travel.

THE MEASURED JOB, IN THE PAIR'S OWN NUMBERS (lab/data/cut-lines.json, measure version cut-lines-v2).
  work A 17847744487144891 — radial 0.4797, sub-type angular, centre [0.6, 0.35]
  work B 17897050660015868 — radial 0.9031, sub-type ring,    centre [0.4961, 0.5]
  both   — vertical banding at period 480 px, which is the pair's held invariant
The instrument therefore has to carry a radial field from an angular reading to a ring one while a
band period stands still, and every one of those is a handle a score drives.

WHAT IS COMPARED, AND AGAINST WHAT.

  The doors. At the dial's two ends one whole work stands. Each is measured against ITS OWN FILE —
  the picture cover-fitted into the frame and pulled in by the headroom the tangential sweep needs
  (the module's own ZOOM of 1.13) — inside the project's seam threshold of 6 of 255.

  The three poses. The host's frame is compared against the LAB MODULE's own frame, on one pose
  taken from the module through its own reading(). Two roads of one frame, never two guesses at one.

  The travel. The instrument's OWN FIELD is measured, not the photographs seen through it: the two
  works are swapped for a flat white one and a flat black one, so what the frame shows is the mask
  itself. The project's own measures then read it — lab/cut-lines.py's `_polar_eta_squared` for the
  radial reading and `measure_banding` for the band period, the same code that produced the pair's
  numbers above.

  The lab tree is READ ONLY and is found at $TLVPHOTOS_LAB_ROOT, defaulting to the immersive
  worktree's lab. Absent, every browser row here is a pinned SKIP that names the missing path.
"""
import base64
import importlib.util
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
PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
          Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]
CUTLINES = LAB / "cut-lines.py"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844          # the phone frame the woven rows measure on
SEAM = 6.0                 # the project's seam threshold, 6 of 255 (TRANSITION-STAGE-V0 §1)
SAME = 1.5                 # two roads of one frame: the carrier check's own bar
FAR = 40.0                 # further than this from a file and it is a different work
ZOOM = 1 + 2 * 0.05 + 0.03  # the module's own crop, gears.js:208-209

# THE PAIR'S OWN NUMBERS, carried here as the constants the rows are stated against.
A_CENTRE = (0.6, 0.35)
B_CENTRE = (0.4961, 0.5)
WORK_BAND_PX = 480.0        # of a 1440-point work
WORK_DIM = 1440.0
# The same physical period once the work is cover-fitted into the frame and pulled in by ZOOM: the
# visible part of the work is its height over ZOOM, so a period of 480 of 1440 stands at this much
# of the frame's own height.
HELD_BAND = (WORK_BAND_PX / WORK_DIM) * ZOOM
# Where the pair's size stands at each end of the travel, read off the sweep this suite's own
# measurement below re-runs: the reading crosses from angular to ring between 0.6 and 0.7.
SIZE_ANGULAR, SIZE_MID, SIZE_RING = 0.35, 0.6, 2.0

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the score
# THE MEASURED JOB, WRITTEN DOWN AS A SCORE. Every one of the six things the pair's measurement asks
# to travel is a track here: the pair's size carries the radial reading from angular to ring, the
# centre walks from work A's measured centre to work B's, the band period stands still at the pair's
# held invariant, and the ratio holds one rung so the repeat counts on the two sides move together.
def score_of(size_from=SIZE_ANGULAR, size_to=SIZE_RING):
    return {
        "schema": 2, "duration": 3000, "direction": "a-to-b", "failLand": "arrive",
        "seed": 4.91016,
        "pair": {"a": "a", "b": "b"},
        "intent": "the meshing line rolls across the frame while the pair's own reading travels "
                  "from angular to ring and the band period stands still",
        "interruption": {"resolve": "nearest-door", "withinMs": 500},
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "fov": None, "logScale": 0, "owner": "stage",
                              "pan": {"x": 0, "y": 0}, "pitch": 0, "roll": 0, "yaw": 0}]},
        "cues": [{
            "id": "gears-main", "cameraAuthority": "stage", "stack": 0, "voice": "letter",
            "instrument": {"api": 1, "id": "gears"},
            "window": [0, 3.0], "works": ["a", "b"],
            "levels": ["SURFACE", "CELL"],
            "roles": ["disassembly", "mystery", "assembly"],
            "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                      "out": {"handle": "mix", "value": 1, "measured": True}},
            "nodes": {
                "mixDrive": {"source": "progress"},
                "clockDrive": {"source": "time"},
                # the pair's size, carrying the radial reading across the pass
                "sizeTravel": {"op": "segment", "in": {"source": "progress"}, "points": [
                    {"at": 0, "value": size_from},
                    {"at": 1, "value": size_to, "shape": "smooth"}]},
                # the centre, from work A's own measured centre to work B's
                "centreXTravel": {"op": "segment", "in": {"source": "progress"}, "points": [
                    {"at": 0, "value": A_CENTRE[0]},
                    {"at": 1, "value": B_CENTRE[0], "shape": "smooth"}]},
                "centreYTravel": {"op": "segment", "in": {"source": "progress"}, "points": [
                    {"at": 0, "value": A_CENTRE[1]},
                    {"at": 1, "value": B_CENTRE[1], "shape": "smooth"}]},
                # the pair's held invariant: one number, standing still for the whole pass
                "bandHeld": {"op": "static", "value": HELD_BAND},
                "ratioStatic": {"op": "static", "value": 0},
                "toothStatic": {"op": "static", "value": 0.4},
                "orderStatic": {"op": "static", "value": 0.4},
                "turnStatic": {"op": "static", "value": 0.55},
                "flankStatic": {"op": "static", "value": 0.35},
                "seedStatic": {"op": "static", "value": 4.91016},
                "shadeStatic": {"op": "static", "value": 1},
                "travelStatic": {"op": "static", "value": 1},
            },
            "tracks": {
                "mix": {"node": "mixDrive"}, "clock": {"node": "clockDrive"},
                "size": {"node": "sizeTravel"},
                "centreX": {"node": "centreXTravel"}, "centreY": {"node": "centreYTravel"},
                "bandPeriod": {"node": "bandHeld"}, "ratio": {"node": "ratioStatic"},
                "tooth": {"node": "toothStatic"}, "order": {"node": "orderStatic"},
                "turn": {"node": "turnStatic"}, "flank": {"node": "flankStatic"},
                "seed": {"node": "seedStatic"}, "shade": {"node": "shadeStatic"},
                "travel": {"node": "travelStatic"},
            },
            "resources": {v: {"bytesEstimate": 0, "framebuffers": 0, "passes": 1, "pingPong": 0,
                              "programs": 1, "textureSlots": 2, "textures": 0, "variant": v}
                          for v in ("lean", "standard", "rich")},
        }],
    }


# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_passgears_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER = (TMP / "pass-layer.js").read_text(encoding="utf-8")

# The instrument's own region of the built file, so the fence rows read it and nothing else.
REGION = LAYER.split("function gearsInstrument()")[1].split("register(gearsInstrument())")[0]

# ---------------------------------------------------------------- string rows

check("PASS-GEARS the host binds this instrument's uniforms by declared name",
      "getUniformLocation(p, u.name)" in LAYER
      and all(('name: "%s"' % u) in REGION for u in
              ["uCA", "uCB", "uR1", "uR2", "uN1", "uN2", "uAmp", "uPh", "uFlank", "uSpread",
               "uOff", "uGuard"])
      and "U.uCA" not in LAYER and "U.uPh" not in LAYER,
      "the meshing set shares only six names with the woven one; twelve more are its own, and none "
      "of them is written into the host")

check("PASS-GEARS the shader carries no version header of its own and receives exactly one",
      REGION.count("#version") == 0
      and 'if (/^\\s*#version\\b/.test(src)) return src;' in LAYER,
      "gears ships WebGL 1 syntax, so the host stamps one header; the guard is what stops a second")

check("PASS-GEARS the meshing instrument creates no context, no canvas, no loop and no listener",
      all(s not in REGION for s in
          ["createElement", "getContext", "requestAnimationFrame", "addEventListener",
           "performance.now", "Date.now", "new Image", "ResizeObserver"]),
      "§1.2's fence, read against the instrument's own region of the file")

check("PASS-GEARS every handle the instrument publishes is a handle a score can drive",
      all(('%s: { min' % h) in REGION for h in
          ["mix", "clock", "dial", "size", "centreX", "centreY", "bandPeriod", "ratio",
           "tooth", "order", "turn", "flank", "seed", "shade", "travel"]),
      "§4.4b: the module ran its wheels on its own accumulating clock and held its judges, its die, "
      "its flank, its pair size and its tooth pitch as constants — all fifteen are handles here")

check("PASS-GEARS the manifest declares the drawing buffer unpreserved",
      "preserveDrawingBuffer: false" in REGION,
      "the module asks for it at gears.js:276; the redraw it stood in for is carried instead")

check("PASS-GEARS the instrument draws on every frame it is handed, reduced or not",
      "if (!live) return;" in REGION and "reduced: st.reduced" in REGION
      and "st.reduced ? 0 : st.t" in REGION,
      "the module drew once under reduced motion and let the preserved buffer hold the picture; "
      "here reduced motion stops the wheels' drive inside values and stops no drawing")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "PASS-GEARS §8     · the manifest registers, and carries every field the contract names",
    "PASS-GEARS row 7  · door 0 stands the departing work, measured against its own file",
    "PASS-GEARS row 7  · door 0 carries no trace of the arriving work",
    "PASS-GEARS row 7  · door 1 stands the arriving work, measured against its own file",
    "PASS-GEARS row 7  · door 1 carries no trace of the departing work",
    "PASS-GEARS the host's frame and the lab module's frame agree: door-0",
    "PASS-GEARS the host's frame and the lab module's frame agree: the meshing middle",
    "PASS-GEARS the host's frame and the lab module's frame agree: door-1",
    "PASS-GEARS row 10 · a seeded run repeats to the pixel",
    "PASS-GEARS row 12 · no instant of the pass draws an empty frame",
    "PASS-GEARS row 14 · textures, programmes and framebuffers return to their baseline after ten runs",
    "PASS-GEARS row 15 · the console stays clean",
    "PASS-GEARS row 22 · the census shows granted against declared, and neither overruns",
    "PASS-GEARS §7     · one canvas, one context, two source textures, one pass a frame",
    "PASS-GEARS §7     · a manifest asking for a preserved drawing buffer is refused, with its reason",
    "PASS-GEARS row 9  · one camera authority through a real pass, and the pose rests on the arrival",
    "PASS-GEARS the real transaction road: curtain up, one pass drawn, exactly one dock at the end",
    "PASS-GEARS §7     · a reduced-motion pass draws every frame and holds the wheels still",
    "PASS-GEARS the score drives all six measured handles, and the band period stands still",
    "PASS-GEARS the radial reading travels from angular to ring, measured on the mask",
    "PASS-GEARS the meshing repeat counts carry the travel",
    "PASS-GEARS every rung of the ratio gives two counts in exactly that ratio",
    "PASS-GEARS the band period the handle names is the period the picture shows",
    "PASS-GEARS the pair's centre reaches the picture and moves it",
    "PASS-GEARS both doors stand whole at every size the travel passes through",
]

missing = [str(p) for p in (PHOTOS + [LAB / "effects" / "gears.js", CUTLINES]) if not p.exists()]


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
    """The work as the instrument seats it: cover-fit, then the centre crop the tangential sweep is
    paid for with (the module's own ZOOM)."""
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
    d = Path(tempfile.mkdtemp(prefix="synth_gearsbench_"))
    shutil.copy2(TMP / "pass-layer.js", d / "pass-layer.js")
    shutil.copy2(LAB / "effects" / "gears.js", d / "gears.js")
    (d / "photos").mkdir()
    for p in PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_gears.html", d / "index.html")
    return d


def ready(br, tries=80):
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
    import numpy as np
    from PIL import Image

    # The project's own measures, imported from the lab tree they were written in. Nothing is
    # re-implemented here: these are the very functions that produced cut-lines.json.
    _spec = importlib.util.spec_from_file_location("cutlines", CUTLINES)
    CL = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(CL)

    def gray_of(path):
        im = Image.open(path).convert("RGB")
        a = np.asarray(im, dtype=np.float64) / 255.0
        return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]

    def crossing_period(gray):
        """The band period read straight off the picture: how often the profile the teeth repeat
        along crosses its own mean. The project's FFT measure reports nothing longer than a third of
        its profile (cut-lines.py's min_k of 3), and the pair's own period stands just past that on
        a single frame, so this reads the same structure without that floor."""
        prof = gray.mean(axis=1)
        prof = prof - prof.mean()
        sign = np.sign(prof)
        sign[sign == 0] = 1
        crossings = int(np.count_nonzero(np.diff(sign) != 0))
        return (2.0 * len(prof) / crossings if crossings else None), crossings

    def centroid(gray):
        tot = float(gray.sum())
        if tot <= 1e-9:
            return None
        ys, xs = np.mgrid[0:gray.shape[0], 0:gray.shape[1]]
        return (float((gray * xs).sum() / tot) / gray.shape[1],
                float((gray * ys).sum() / tot) / gray.shape[0])

    # EVIDENCE. The captures this suite judges are kept rather than swept away, so a reader can look
    # at the three frames the travel rows state numbers about.
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_gearsshots_"))
    BENCH = bench_dir()
    SCORE_JSON = json.dumps(score_of())
    with serve(BENCH) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/index.html")
            if not ready(br):
                for r in BROWSER_ROWS:
                    skip(r, "the bench never came up: "
                         + br.evaluate("JSON.stringify(window.__errs||[])"))
            else:
                # ---- §8: the manifest itself -------------------------------------------------
                man = js(br, "return window.__exPass.bench.manifest('gears');")
                reg = js(br, "return window.__host.report().registered;")
                need = ["id", "api", "arity", "roles", "params", "handles", "neutrals", "doors",
                        "framings", "drivers", "camera", "gl", "passes", "resources",
                        "capabilities", "decline", "provenance", "readiness"]
                lacks = [k for k in need if k not in (man or {})]
                doors_ok = (man and man["doors"]["in"]["value"] == 0
                            and man["doors"]["out"]["value"] == 1
                            and man["doors"]["in"]["handle"] == "mix")
                framing_ok = (man and abs(man["framings"]["0"]["coverCrop"] - ZOOM) < 1e-9
                              and abs(man["framings"]["1"]["coverCrop"] - ZOOM) < 1e-9)
                check(BROWSER_ROWS[0],
                      "gears" in reg and not lacks and doors_ok and framing_ok
                      and man["camera"]["authority"] == "stage"
                      and man["provenance"]["labPath"] == "lab/effects/gears.js"
                      and man["resources"]["standard"]["programs"] == 1
                      and man["resources"]["standard"]["bytesEstimate"] == 0,
                      f"registered={reg} lacking={lacks} camera={man and man['camera']} "
                      f"provenance={man and man['provenance']} readiness={man and man['readiness']} "
                      f"coverCrop={man and man['framings']['0']['coverCrop']}")

                # ---- the three poses: the host's frame beside the lab module's ----------------
                br.evaluate("window.__clock(7.0); 0")
                br.sleep(0.9)
                pairs = []
                for name, v in (("door-0", 0.0), ("mid", 0.5), ("door-1", 1.0)):
                    br.evaluate("window.__mix(%r); 0" % v)
                    br.sleep(0.9)
                    js(br, "return window.__hostDraw();")
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
                towers = work_in_the_frame(BENCH / "photos" / "towers.jpg", w, h, ZOOM)
                glass = work_in_the_frame(BENCH / "photos" / "glassgrid.jpg", w, h, ZOOM)

                for i, (door, own, other, ownn, othern) in enumerate((
                        ("door-0", towers, glass, "towers.jpg", "glassgrid.jpg"),
                        ("door-1", glass, towers, "glassgrid.jpg", "towers.jpg"))):
                    a, amx = apart(shots[door], own)
                    check(BROWSER_ROWS[1 + i * 2], a <= SEAM,
                          f"{door} against {ownn}: mean {a:.4f} of 255 (threshold {SEAM}), "
                          f"worst channel {amx}")
                    o, _ = apart(shots[door], other)
                    check(BROWSER_ROWS[2 + i * 2], o >= FAR,
                          f"{door} against {othern}: mean {o:.4f} of 255 (must exceed {FAR})")

                for i, (name, ph, pm) in enumerate(pairs):
                    m, mx = diff(ph, pm)
                    check(BROWSER_ROWS[5 + i], m <= SAME,
                          f"{name}: mean {m:.4f} of 255 (threshold {SAME}), worst channel {mx}")

                # ---- the real transaction road, and the seeded repeat -------------------------
                br.evaluate("window.__show('host'); 0")
                took = js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                first = png(br, SHOTS / "seeded-1.png")
                rep1 = js(br, "return window.__report();")
                br.evaluate("window.__cancel('between runs'); 0")
                br.sleep(0.4)
                js(br, "return window.__offer(%s, {clock: 1.5, progress: 0.5});" % SCORE_JSON)
                br.sleep(0.9)
                second = png(br, SHOTS / "seeded-2.png")
                m, mx = diff(first, second)
                check(BROWSER_ROWS[8], took["took"] and m == 0.0 and mx == 0,
                      f"took={took['took']} two runs of one seeded score: mean {m} worst channel {mx}")

                # ---- no empty frame at any sampled instant ------------------------------------
                # An empty frame is one that carries no picture: a flat field, or one so dark that
                # nothing of either work is in it. Both are read off the capture.
                empt = []
                for at in (0.0, 0.15, 0.3, 0.5, 0.7, 0.85, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.45)
                    p = png(br, SHOTS / ("instant-%.2f.png" % at))
                    g = gray_of(p)
                    empt.append({"at": at, "mean": round(float(g.mean()), 4),
                                 "std": round(float(g.std()), 4)})
                    br.evaluate("window.__cancel('instant'); 0")
                    br.sleep(0.6)
                worst_std = min(e["std"] for e in empt)
                worst_mean = min(e["mean"] for e in empt)
                check(BROWSER_ROWS[9], worst_std > 0.02 and worst_mean > 0.02,
                      "the flattest instant carries a spread of %.4f and the darkest a mean of %.4f "
                      "(both must clear 0.02): %s"
                      % (worst_std, worst_mean, ", ".join("%.2f→%.3f/%.3f" % (e["at"], e["mean"],
                                                                              e["std"]) for e in empt)))

                # ---- ten runs, and the baseline ----------------------------------------------
                base_c = rep1["census"]
                for _ in range(10):
                    js(br, "return window.__offer(%s, {clock: 2.0, progress: 0.3});" % SCORE_JSON)
                    br.sleep(0.12)
                    br.evaluate("window.__cancel('leak row'); 0")
                br.sleep(0.5)
                after = js(br, "return window.__report();")["census"]
                same = (after["textures"] == base_c["textures"] == 2
                        and after["framebuffers"] == base_c["framebuffers"] == 0
                        and after["canvases"] == base_c["canvases"] == 1
                        and after["contexts"] == base_c["contexts"] == 1
                        and after["programsCached"] == base_c["programsCached"])
                check(BROWSER_ROWS[10], same,
                      f"before={base_c['textures']}/{base_c['programsCached']}/"
                      f"{base_c['framebuffers']} after ten runs={after['textures']}/"
                      f"{after['programsCached']}/{after['framebuffers']} "
                      f"(textures/programmes cached/framebuffers)")

                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                check(BROWSER_ROWS[11], not errs, "; ".join(errs)[:300])

                # ---- the census against the declaration --------------------------------------
                res = js(br, "return window.__report();")["resources"]
                check(BROWSER_ROWS[12],
                      res["declared"] and res["over"] is False
                      and res["granted"]["textures"] == res["declared"]["textures"]
                      and res["granted"]["framebuffers"] == res["declared"]["framebuffers"]
                      and res["granted"]["bytes"] == res["declared"]["bytesEstimate"],
                      f"declared={res['declared']} granted={res['granted']}")

                # ---- the hardware, counted where each thing is made ---------------------------
                js(br, "return window.__offer(%s, {clock: 1.0, progress: 0.4});" % SCORE_JSON)
                br.sleep(0.7)
                cen = js(br, "return window.__report();")["census"]
                check(BROWSER_ROWS[13],
                      cen["canvases"] == 1 and cen["contexts"] == 1 and cen["textures"] == 2
                      and cen["passesLastFrame"] == 1 and cen["framebuffers"] == 0
                      and cen["preserveDrawingBuffer"] is False
                      and int(br.evaluate("String(document.querySelectorAll('canvas').length)")) == 2,
                      f"census={cen}")

                # ---- a manifest asking for a preserved drawing buffer -------------------------
                r = js(br, """
                  var m = JSON.parse(JSON.stringify(window.__exPass.bench.manifest('gears')));
                  m.gl.preserveDrawingBuffer = true;
                  var ok = window.__exPass.bench.register({name:'gears-preserve', manifest:m,
                      values:function(){return {cA:[0,0],cB:[1,0],R1:1,R2:1,n1:3,n2:3,amp:0,ph:0,
                                                flank:0.35,spread:0,off:0,guard:0};},
                      fit:function(){return [1,1,0,0];},
                      prepare:function(){return {take:false};}, start:function(){}, frame:function(){}});
                  var evs = window.__host.report().events.filter(function(e){return e.name==='manifest-refused';});
                  return {ok: ok, why: evs.length ? evs[evs.length-1].why : null,
                          registered: window.__host.report().registered};
                """)
                check(BROWSER_ROWS[14],
                      r["ok"] is False and r["why"] and "preserved" in r["why"]
                      and "gears-preserve" not in r["registered"],
                      f"registered={r['ok']} why={r['why']}")

                # ---- the whole pass, the camera, and one dock ---------------------------------
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
                for _ in range(80):
                    if js(br, "return window.__report().state;") == "idle":
                        break
                    br.sleep(0.1)
                end = js(br, "return {state: window.__report().state, docks: window.__hooks.docks.slice(), "
                             "curtains: window.__hooks.curtains.slice(), "
                             "events: window.__report().events.map(function(e){return e.name;}).slice(-6)};")
                check(BROWSER_ROWS[16],
                      took["took"] and mid["state"] == "running" and mid["curtains"][:1] == [True]
                      and end["state"] == "idle" and len(end["docks"]) == 1
                      and end["curtains"][-1] is False and "docked" in end["events"],
                      f"mid={mid} end={end}")

                # THE CAMERA, read off the run that just landed. This instrument claims no camera:
                # its construction decides which wheel owns each point of the frame and slides the
                # two works along their own rims inside it, and both are what it does to its own
                # surface. The stage's own flight therefore runs the whole window, and this score
                # authors no move, so the pass never leaves the neutral pose.
                cam = js(br, "var r = window.__report(); "
                             "return {camera: r.camera, rest: r.rest, handoffs: r.handoffs, "
                             "tol: r.camTolerances};")
                check(BROWSER_ROWS[15],
                      cam["camera"] and cam["camera"]["owner"] == "stage"
                      and cam["handoffs"] == []
                      and cam["rest"] and cam["rest"]["rested"] is True
                      and cam["rest"]["off"] <= cam["tol"]["rest"],
                      f"owner={cam['camera'] and cam['camera']['owner']} rest={cam['rest']} "
                      f"handoffs={cam['handoffs']} tolerances={cam['tol']}")

                # ---- a reduced-motion pass ----------------------------------------------------
                # The redraw the preserved buffer stood in for. Two instants of one reduced run at
                # the same dial and two different clocks: the picture is drawn both times, and the
                # wheels stand still, so the two frames are the same picture.
                red = []
                for sec in (1.5, 9.0):
                    js(br, "return window.__offer(%s, {clock: %r, progress: 0.5, reduced: true});"
                       % (SCORE_JSON, sec))
                    br.sleep(0.6)
                    red.append(png(br, SHOTS / ("reduced-%.1f.png" % sec)))
                    br.evaluate("window.__cancel('reduced'); 0")
                    br.sleep(0.6)
                rg = gray_of(red[0])
                rm, rmx = diff(red[0], red[1])
                check(BROWSER_ROWS[17],
                      float(rg.std()) > 0.02 and rm == 0.0 and rmx == 0,
                      f"a reduced frame carries a spread of {float(rg.std()):.4f} (so it was drawn) "
                      f"and the clock moving from 1.5 s to 9 s moves it by mean {rm} worst channel "
                      f"{rmx} (so the wheels stand still)")

                # ---- the score drives all six measured handles --------------------------------
                walked = []
                for at in (0.0, 0.25, 0.5, 0.75, 1.0):
                    js(br, "return window.__offer(%s, {clock: 1.5, progress: %r});"
                       % (SCORE_JSON, at))
                    br.sleep(0.4)
                    walked.append({"at": at, "h": js(br, "return window.__report().handles;")})
                    br.evaluate("window.__cancel('walk'); 0")
                    br.sleep(0.6)
                sizes = [w_["h"]["size"] for w_ in walked]
                cxs = [w_["h"]["centreX"] for w_ in walked]
                cys = [w_["h"]["centreY"] for w_ in walked]
                bands = [w_["h"]["bandPeriod"] for w_ in walked]
                held = all(abs(b - HELD_BAND) <= 1e-9 for b in bands)
                rising = all(sizes[i] < sizes[i + 1] for i in range(len(sizes) - 1))
                check(BROWSER_ROWS[18],
                      rising and held
                      and abs(sizes[0] - SIZE_ANGULAR) <= 1e-9 and abs(sizes[-1] - SIZE_RING) <= 1e-9
                      and abs(cxs[0] - A_CENTRE[0]) <= 1e-9 and abs(cxs[-1] - B_CENTRE[0]) <= 1e-9
                      and abs(cys[0] - A_CENTRE[1]) <= 1e-9 and abs(cys[-1] - B_CENTRE[1]) <= 1e-9,
                      "size %s · centre x %s · centre y %s · band period held at %.6f across all "
                      "five instants (%s)"
                      % ([round(s, 4) for s in sizes], [round(c, 4) for c in cxs],
                         [round(c, 4) for c in cys], HELD_BAND,
                         "yes" if held else [round(b, 6) for b in bands]))

                # ---- THE TRAVEL, MEASURED ON THE MASK -----------------------------------------
                # The two works are swapped for a flat white one and a flat black one, so the frame
                # shows the instrument's own field and nothing of any photograph, and the shadow and
                # the counter-motion are put down (the module's own two judge handles, which exist
                # for exactly this). The project's own radial measure then reads the mask about work
                # A's own measured centre — the same centre, the same code, that gave the pair its
                # numbers.
                js(br, "window.__source('flat'); return 1;")
                br.evaluate("window.__show('host'); 0")
                br.sleep(0.3)

                def mask(name, over):
                    v = js(br, "return window.__poseDraw(%s);" % json.dumps(over))
                    br.sleep(0.15)
                    p = png(br, SHOTS / (name + ".png"))
                    return p, v

                steps = []
                for label, size in (("angular", SIZE_ANGULAR), ("middle", SIZE_MID),
                                    ("ring", SIZE_RING)):
                    p, v = mask("travel-" + label,
                                {"dial": 0.5, "size": size, "ratio": 0, "bandPeriod": HELD_BAND,
                                 "shade": 0, "travel": 0, "centreX": 0.5, "centreY": 0.5})
                    g = gray_of(p)
                    er, et, _ = CL._polar_eta_squared(g, *A_CENTRE)
                    per, cr = crossing_period(g)
                    steps.append({"label": label, "size": size, "n1": v["n1"], "n2": v["n2"],
                                  "eta_r": er, "eta_theta": et,
                                  "sub": "ring" if er >= et else "angular",
                                  "period_px": per, "crossings": cr})
                lo, hi = steps[0], steps[-1]
                check(BROWSER_ROWS[19],
                      lo["sub"] == "angular" and hi["sub"] == "ring"
                      and lo["eta_theta"] > 0.55 and hi["eta_r"] > 0.30
                      and hi["eta_r"] > hi["eta_theta"] and lo["eta_theta"] > lo["eta_r"],
                      "measured about work A's own centre %s, band period held at %.4f: "
                      % (list(A_CENTRE), HELD_BAND)
                      + " · ".join("%s (size %.2f) eta_r %.4f eta_theta %.4f → %s"
                                   % (s["label"], s["size"], s["eta_r"], s["eta_theta"], s["sub"])
                                   for s in steps))

                check(BROWSER_ROWS[20],
                      lo["n1"] < steps[1]["n1"] < hi["n1"] and lo["n1"] >= 3,
                      "the teeth round each wheel across the same travel: "
                      + " · ".join("%s %d:%d" % (s["label"], s["n1"], s["n2"]) for s in steps)
                      + " — the counts are what the reading rides")

                # ---- the ratio's rungs ---------------------------------------------------------
                rungs = []
                for i, want in enumerate([[1, 1], [3, 4], [2, 3], [1, 2], [2, 5], [1, 3], [1, 4]]):
                    v = js(br, "return window.__poseDraw(%s);"
                           % json.dumps({"dial": 0.5, "size": 2.0, "ratio": i / 6.0,
                                         "bandPeriod": HELD_BAND, "shade": 0, "travel": 0}))
                    n1, n2 = v["n1"], v["n2"]
                    exact = n1 * want[1] == n2 * want[0]
                    rungs.append((want, n1, n2, exact))
                check(BROWSER_ROWS[21], all(r[3] for r in rungs),
                      "; ".join("%d:%d asked → %d:%d %s" % (r[0][0], r[0][1], r[1], r[2],
                                                            "exact" if r[3] else "OFF THE RUNG")
                                for r in rungs))

                # ---- the band period the handle names ------------------------------------------
                # Read with the project's own FFT measure at the two periods a frame this size can
                # carry — its own floor of three periods puts anything longer out of its reach, and
                # the pair's held invariant stands just past that floor, which the row states.
                bandrows = []
                for asked in (1 / 6.0, 0.25):
                    p, v = mask("band-%.4f" % asked,
                                {"dial": 0.5, "size": 2.0, "ratio": 0, "bandPeriod": asked,
                                 "shade": 0, "travel": 0})
                    g = gray_of(p)
                    b = CL.measure_banding(g)
                    bandrows.append({"asked": asked, "want": asked * VH,
                                     "got": b["period_px_working"], "axis": b["axis"],
                                     "score": b["score"], "pitch": v["pitch"]})
                check(BROWSER_ROWS[22],
                      all(abs(r["got"] - r["want"]) <= 1.0 for r in bandrows),
                      "; ".join("asked %.4f of the frame's height = %.1f points, the measure reads "
                                "%.1f (%s, score %.3f)"
                                % (r["asked"], r["want"], r["got"], r["axis"], r["score"])
                                for r in bandrows)
                      + " — the pair's own %.4f is %.1f points, under the measure's floor of three "
                        "periods, so it is stated rather than read here"
                        % (HELD_BAND, HELD_BAND * VH))

                # ---- the centre reaches the picture --------------------------------------------
                seen = []
                for cx, cy in ((0.35, 0.35), (0.65, 0.65)):
                    p, v = mask("centre-%.2f-%.2f" % (cx, cy),
                                {"dial": 0.5, "size": SIZE_RING, "ratio": 0,
                                 "bandPeriod": HELD_BAND, "shade": 0, "travel": 0,
                                 "centreX": cx, "centreY": cy})
                    seen.append({"asked": (cx, cy), "path": p, "cA": v["cA"],
                                 "centroid": centroid(gray_of(p))})
                moved, mmx = diff(seen[0]["path"], seen[1]["path"])
                dx = seen[1]["centroid"][0] - seen[0]["centroid"][0]
                dy = seen[1]["centroid"][1] - seen[0]["centroid"][1]
                check(BROWSER_ROWS[23],
                      moved > SEAM and abs(dx) > 0.01,
                      "carrying the pair's centre from %s to %s moves the frame by mean %.4f of 255 "
                      "(worst channel %d, the seam threshold is %.1f) and carries the mask's own "
                      "centroid by %.4f across and %.4f down"
                      % (list(seen[0]["asked"]), list(seen[1]["asked"]), moved, mmx, SEAM, dx, dy))

                # ---- both doors, at every size the travel passes through ----------------------
                # THE DOOR LAW ACROSS THE WHOLE HANDLE, not only at the module's own size. The
                # module holds its doors by standing the meeting line beyond the frame's edge by a
                # margin derived at one wheel size; the port lets the size travel, so it solves the
                # module's own door condition instead. Read on the mask, a door is a flat field: at
                # dial 0 the whole frame is the departing work, at dial 1 the whole frame is the
                # arriving one, and any tooth of the far work standing anywhere shows up as spread.
                # The tooth height and the tooth order are swept to their far ends as well as the
                # module's own, because those two are what the margin has to clear: a taller tooth
                # and a wider spread both reach further past the meeting line, and the module's
                # margin was fitted with neither of them at its end.
                doorrows = []
                for label, size in (("angular", SIZE_ANGULAR), ("middle", SIZE_MID),
                                    ("ring", SIZE_RING)):
                    for ratio in (0.0, 1.0):
                        for tooth, order in ((0.4, 0.4), (1.0, 1.0)):
                            for dial, want, work in ((0.0, 1.0, "the departing work"),
                                                     (1.0, 0.0, "the arriving work")):
                                p, v = mask("door-%s-r%.0f-t%.1f-%.0f"
                                            % (label, ratio, tooth, dial),
                                            {"dial": dial, "size": size, "ratio": ratio,
                                             "bandPeriod": HELD_BAND, "shade": 0, "travel": 0,
                                             "tooth": tooth, "order": order,
                                             "centreX": 0.5, "centreY": 0.5})
                                g = gray_of(p)
                                doorrows.append({"size": size, "dial": dial, "work": work,
                                                 "ratio": ratio, "tooth": tooth,
                                                 "mean": float(g.mean()), "std": float(g.std()),
                                                 "off": abs(float(g.mean()) - want),
                                                 "reach": v["reach"]})
                worst = max(doorrows, key=lambda r: max(r["off"], r["std"]))
                check(BROWSER_ROWS[24],
                      all(r["off"] <= 0.005 and r["std"] <= 0.01 for r in doorrows),
                      "%d doors across three sizes, two ratio rungs and two tooth heights; the "
                      "furthest any stood from a whole work was %.5f with a spread of %.5f "
                      "(size %.2f, ratio %.0f, tooth %.1f, dial %.0f, %s, reach %.3f). Bars: "
                      "0.005 and 0.010."
                      % (len(doorrows), worst["off"], worst["std"], worst["size"], worst["ratio"],
                         worst["tooth"], worst["dial"], worst["work"], worst["reach"]))

    shutil.rmtree(BENCH, ignore_errors=True)
    print("\nthe captures this run judged are kept at %s" % SHOTS)

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
