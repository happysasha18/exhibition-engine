#!/usr/bin/env python3
"""capture-weave — photograph the woven instrument as the host actually plays it.

Root: his word 2026-08-13 23:03 — carry the woven instrument across first, with a real pair score
feeding a real instrument. PASS-API-V1 §9 row 16: captures exist for every landed instrument.

WHAT IS PHOTOGRAPHED. The real pair of the walk's first chain step (lab/data/walk-v1.json steps[0]),
played through the BUILT pass-layer.js by a real command carrying that pair's own score. Both doors
and five instants between them. The run is pinned — the clock and the travel are held at each
instant — so the same seven frames come back identically on every run.

The frame is the phone's own: 390 x 844 points, the frame lab/carrier-check.py measures on.

Run: python3 scripts/capture-weave.py [--out DIR]
"""
import argparse
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

IMMERSIVE = Path("/Users/sashaabramovich/tlvphotos-immersive")
LAB = IMMERSIVE / "lab"
SCORE = LAB / "data" / "scores" / "17847744487144891__17897050660015868.json"
WALK = LAB / "data" / "walk-v1.json"
OUT_DEFAULT = IMMERSIVE / "docs" / "immersive" / "captures" / "weave"

VW, VH = 390, 844
# Both doors and five instants between them. The name carries the travel, so a reader can put the
# seven frames in order without opening a single one.
POSES = [(0.00, "door-a"), (0.15, ""), (0.35, ""), (0.50, "the-woven-middle"),
         (0.65, ""), (0.85, ""), (1.00, "door-b")]


def scored(a, b):
    """The lab's own score for this pair, with the four handles its generator left untracked wired to
    the static nodes it already wrote — the same treatment tests/test_pass_weave.py gives it, for the
    same reason (§4.4b: every handle a score can drive, a score does drive)."""
    s = json.loads(SCORE.read_text(encoding="utf-8"))["score"]
    s["pair"] = {"a": a, "b": b}
    cue = s["cues"][0]
    cue["nodes"]["axisStatic"] = {"op": "static", "value": 0}
    for h, n in (("strips", "stripsStatic"), ("speed", "speedStatic"),
                 ("seed", "seedStatic"), ("axis", "axisStatic")):
        cue["tracks"][h] = {"node": n}
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    args = ap.parse_args()

    if not chrome_available():
        print("Chrome is not installed — nothing photographed.")
        return 2
    for p in (SCORE, WALK, LAB / "effects" / "weave.js"):
        if not p.exists():
            print("missing source material:", p)
            return 2

    step = json.loads(WALK.read_text(encoding="utf-8"))["steps"][0]
    works = [(step["a"]["id"], IMMERSIVE / "gallery" / "assets" / "constructed" / (step["a"]["id"] + ".jpg")),
             (step["b"]["id"], IMMERSIVE / "gallery" / "assets" / "coda" / (step["b"]["id"] + ".jpg"))]
    for _, p in works:
        if not p.exists():
            print("missing photograph:", p)
            return 2

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    tmp = Path(tempfile.mkdtemp(prefix="weave_capture_site_"))
    build_site.OUT = tmp
    build_site.build("https://synth.example.com")

    bench = Path(tempfile.mkdtemp(prefix="weave_capture_bench_"))
    # THE PACK STANDS FIRST, AND THE HOST SECOND. Since 2026-08-14 the instruments and their
    # manifests live in pass-pack.js, which the host fetches by address and weighs against the digest
    # the build stamped; the host itself carries the machinery and names no instrument. So a reader
    # looking for an instrument's manifest reads the pack, and while both files stand the pack is the
    # one named first. The bench root serves both, the same two files a visitor gets.
    shutil.copy2(tmp / "pass-pack.js", bench / "pass-pack.js")
    shutil.copy2(tmp / "pass-layer.js", bench / "pass-layer.js")
    shutil.copy2(LAB / "effects" / "weave.js", bench / "weave.js")
    (bench / "photos").mkdir()
    # The bench page names its two pictures by the lab's own file names; the real pair takes those
    # places, so the page needs no edit to photograph a different pair.
    shutil.copy2(works[0][1], bench / "photos" / "towers.jpg")
    shutil.copy2(works[1][1], bench / "photos" / "glassgrid.jpg")
    shutil.copy2(ROOT / "tests" / "fixture_pass_weave.html", bench / "index.html")

    score = json.dumps(scored("a", "b"))
    made = []
    try:
        with serve(bench) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                for _ in range(60):
                    if br.evaluate("String(!!window.__ready)") == "true":
                        break
                    br.sleep(0.25)
                if br.evaluate("String(!!window.__ready)") != "true":
                    print("the bench never came up:", br.evaluate("JSON.stringify(window.__errs||[])"))
                    return 1
                br.evaluate("window.__show('host'); 0")
                for travel, word in POSES:
                    # the clock a run of this length would be showing at this instant, so a pinned
                    # frame is the frame the visitor would actually meet there
                    clock = travel * 3.0
                    br.evaluate("window.__offer(%s, {clock: %r, progress: %r}); 0"
                                % (score, clock, travel))
                    br.sleep(0.7)
                    name = "weave-%03d%s.png" % (round(travel * 100), ("-" + word) if word else "")
                    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
                    (out / name).write_bytes(base64.b64decode(d["data"]))
                    made.append(name)
                    br.evaluate("window.__cancel('between captures'); 0")
                errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
    finally:
        shutil.rmtree(bench, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)

    print("pair: %s -> %s" % (works[0][0], works[1][0]))
    print("frame: %d x %d points" % (VW, VH))
    for n in made:
        print("  ", out / n)
    if errs:
        print("console said:", "; ".join(errs)[:300])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
