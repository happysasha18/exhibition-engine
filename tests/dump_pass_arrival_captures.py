#!/usr/bin/env python3
"""S-06 follow-up — real browser-rendered frames of the two arrival modes that reach pixels today.

tests/pass_arrival_walk.txt is a COMPOSER-LEVEL log: ten edges through the shipped composer, three
of five arrival modes triggered, but 0 of 10 steps reached a rendered instrument handle — the log
proves the composer's decision logic, not what a visitor would see. This script is the still-owed
visual half: it drives the same two instruments the earlier S-06 pass (8fd279c) proved reach pixels
— `pour` under CRYSTALLIZED (`arrival: 1`, `seedPlace`) and `livemirror` under PROPAGATED
(`propagate`) — through the real headless-Chrome harness this suite already uses for
test_pass_pour.py and test_pass_livemirror.py, and saves a frame sequence of each so a human can
look at real pixels and judge whether the arrival reads as intended.

Not a test: no pass/fail rows, no CI membership. It writes PNG sequences to
tests/captures/s06-arrival-walk/{crystallized,propagated}/ and a README describing them.

Run: python3 tests/dump_pass_arrival_captures.py
"""
import base64
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844

# pour's own bench (charter shelf 14, no lab module — same pair test_pass_pour.py uses)
POUR_PHOTOS = [Path("/Users/sashaabramovich/tlvphotos/lab/photos/towers.jpg"),
               Path("/Users/sashaabramovich/tlvphotos/lab/photos/glassgrid.jpg")]

# livemirror's own bench (lab-ported — same pair and lab module test_pass_livemirror.py uses)
LAB = Path("/Users/sashaabramovich/tlvphotos/lab")
MIRROR_PHOTOS = [LAB / "photos" / "glassgrid.jpg", LAB / "photos" / "towers.jpg"]
MODULE = LAB / "effects" / "livemirror.js"

OUT = ROOT / "tests" / "captures" / "s06-arrival-walk"
CRYSTAL_DIR = OUT / "crystallized"
PROPAGATED_DIR = OUT / "propagated"

N_FRAMES = 8
N_MIRROR_FRAMES = 9

# CRYSTALLIZED's own dial: an off-centre seed so the outward spread from it is legible in a frame,
# a stagger under one (some frame carries both a released and an unreleased column at once).
SEED_PLACE = 0.30
STAGGER = 0.85
COLUMNS = 16

# PROPAGATED's own pose: axis 2 is the "both" fold (down the middle AND across it, so three copy
# depths stand in one frame — the picture, the two panels reflected once, and the corner reflected
# twice), drift 0 holds the mirror still so only the exchange itself moves, centred, spread wide so
# the depth-ordered exchange is spread widely enough across the hand to sample.
MIRROR_AXIS = 2
MIRROR_DRIFT = 0
MIRROR_CENTRE = 0.5
MIRROR_PROPAGATE = 0.9

# THE HAND'S OWN EXCHANGE WINDOW. pass-inst-livemirror.js folds the frame in over hand [0, 0.46],
# holds it wholly mirrored, and folds it back out over [0.54, 1] (its own SHUT_IN/SHUT_OUT, HOLD =
# 0.08 of the hand) — the mirrored-COPY exchange this arrival names only happens inside that 8%
# band. A plain 0..1 sweep spends every frame on the fold's own geometry closing and opening and
# never lands inside that band (verified: frames at 0.43 and 0.57 already stand at opposite whole
# works, fully folded, with nothing of the exchange between them) — so this walk samples the band
# itself, with a margin of context on each side to show the fold arriving and leaving fully closed.
MIRROR_HAND_START = 0.30
MIRROR_HAND_END = 0.70


def log(msg):
    print(msg, flush=True)


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def ready(br, tries=120):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.25)
    return False


def pour_bench_dir(tmp):
    d = Path(tempfile.mkdtemp(prefix="s06_pourcap_"))
    shutil.copy2(tmp / "pass-layer.js", d / "pass-layer.js")
    for inst in sorted(tmp.glob("pass-inst-*.js")):
        shutil.copy2(inst, d / inst.name)
    shutil.copy2(tmp / "config.json", d / "config.json")
    (d / "photos").mkdir()
    for p in POUR_PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_elements.html", d / "index.html")
    return d


def mirror_bench_dir(tmp):
    d = Path(tempfile.mkdtemp(prefix="s06_mirrorcap_"))
    shutil.copy2(tmp / "pass-layer.js", d / "pass-layer.js")
    for inst in sorted(tmp.glob("pass-inst-*.js")):
        shutil.copy2(inst, d / inst.name)
    shutil.copy2(tmp / "config.json", d / "config.json")
    (d / "livemirror.js").write_text(MODULE.read_text(encoding="utf-8"), encoding="utf-8")
    (d / "photos").mkdir()
    for p in MIRROR_PHOTOS:
        shutil.copy2(p, d / "photos" / p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_livemirror.html", d / "index.html")
    return d


def capture_crystallized(tmp):
    missing = [str(p) for p in POUR_PHOTOS if not p.exists()]
    if missing:
        log("crystallized: SKIP, photos missing: %s" % missing)
        return None
    shutil.rmtree(CRYSTAL_DIR, ignore_errors=True)
    CRYSTAL_DIR.mkdir(parents=True, exist_ok=True)
    d = pour_bench_dir(tmp)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html#pour")
                if not ready(br):
                    log("crystallized: bench never became ready")
                    return None
                frames = []
                for i in range(N_FRAMES):
                    mix = i / (N_FRAMES - 1)
                    js(br, "window.__draw({mix: %r, arrival: 1, seedPlace: %r, "
                           "stagger: %r, columns: %r}); return 1;"
                       % (mix, SEED_PLACE, STAGGER, COLUMNS))
                    p = png(br, CRYSTAL_DIR / ("frame-%02d.png" % i))
                    frames.append({"index": i, "mix": round(mix, 4), "path": p})
                errs = js(br, "return window.__errs;")
                log("crystallized: %d frames, errs=%s" % (len(frames), errs))
                return frames, errs
    finally:
        shutil.rmtree(d, ignore_errors=True)


def capture_propagated(tmp):
    missing = [str(p) for p in MIRROR_PHOTOS if not p.exists()]
    if not MODULE.exists():
        missing.append(str(MODULE))
    if missing:
        log("propagated: SKIP, missing: %s" % missing)
        return None
    shutil.rmtree(PROPAGATED_DIR, ignore_errors=True)
    PROPAGATED_DIR.mkdir(parents=True, exist_ok=True)
    d = mirror_bench_dir(tmp)
    try:
        with serve(d) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not ready(br):
                    log("propagated: bench never became ready")
                    return None
                br.evaluate(
                    "window.__param('axis', %r); window.__param('drift', %r);"
                    "window.__param('centreX', %r); window.__param('centreY', %r);"
                    "window.__param('propagate', %r); window.__mask(0); 0"
                    % (MIRROR_AXIS, MIRROR_DRIFT, MIRROR_CENTRE, MIRROR_CENTRE, MIRROR_PROPAGATE))
                br.sleep(0.3)
                frames = []
                for i in range(N_MIRROR_FRAMES):
                    hand = (MIRROR_HAND_START
                            + (MIRROR_HAND_END - MIRROR_HAND_START) * i / (N_MIRROR_FRAMES - 1))
                    url = br.evaluate("window.__grab(%r)" % hand)
                    if isinstance(url, str) and url.startswith('"'):
                        url = json.loads(url)
                    p = PROPAGATED_DIR / ("frame-%02d.png" % i)
                    p.write_bytes(base64.b64decode(url.split(",", 1)[1]))
                    frames.append({"index": i, "hand": round(hand, 4), "path": str(p)})
                errs = js(br, "return window.__errs;")
                log("propagated: %d frames, errs=%s" % (len(frames), errs))
                return frames, errs
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    if not chrome_available():
        log("chrome is not installed — cannot capture real frames")
        return 1

    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    tmp = Path(tempfile.mkdtemp(prefix="s06_capbuild_"))
    build_site.OUT = tmp
    build_site.build(SITE_URL)

    try:
        crystal = capture_crystallized(tmp)
        propagated = capture_propagated(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "crystallized": crystal[0] if crystal else None,
        "crystallized_errs": crystal[1] if crystal else None,
        "propagated": propagated[0] if propagated else None,
        "propagated_errs": propagated[1] if propagated else None,
        "seedPlace": SEED_PLACE, "stagger": STAGGER, "columns": COLUMNS,
        "mirrorAxis": MIRROR_AXIS, "mirrorDrift": MIRROR_DRIFT,
        "mirrorCentre": MIRROR_CENTRE, "mirrorPropagate": MIRROR_PROPAGATE,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    log("manifest written: %s" % (OUT / "manifest.json"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
