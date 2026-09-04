#!/usr/bin/env python3
"""Generates the *.json frames in this directory — the prepared grayscale frames
darkroom-measure.js and recipes.py are both measured against (DR-5).

Runs recipes.py's OWN preparation (load_image, to_gray, normalise) over ten of the collection's
photographs in ~/tlvphotos/lab/photos — the same BIG=512 working frame analyse() itself measures
from (recipes.py:600-602), before the resize to the SMALL search scale and before find_centre;
neither is ported, so neither is needed here. Each frame is saved as {width, height, data}, data
being the flat row-major grayscale array darkroom-measure.js's functions take directly.

Ten frames, fixed by the survey below (best_axis(g, axis=1, chance_diff(g)) over all 26 photos):
five hold the centred axis (position 0.500) a symmetric facade gives, five carry a real off-centre
axis, so the mirror-scan-narrowed-to-0.5 planted defect (DR-5) has something to red on.

Run: python3 tests/fixtures/darkroom-frames/make_frames.py
"""
import glob
import json
import os
import sys

TLVPHOTOS_ANALYZE = os.path.expanduser("~/tlvphotos/lab/analyze")
PHOTOS_DIR = os.path.expanduser("~/tlvphotos/lab/photos")
sys.path.insert(0, TLVPHOTOS_ANALYZE)
import recipes as R  # noqa: E402  (path inserted above; that copy's absolute path is the source)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# name -> whether the survey found its best_axis(axis=1) position away from 0.5 (off-centre).
FRAMES = [
    ("balconies.jpg", False),
    ("concrete-dishes.jpg", False),
    ("glass-drum.jpg", False),
    ("shalom-meir.jpg", False),
    ("twin-towers.jpg", False),
    ("columns.jpg", True),
    ("glassgrid.jpg", True),
    ("cranes-dusk.jpg", True),
    ("round-tower.jpg", True),
    ("tower-sky.jpg", True),
]


def main():
    all_photos = {os.path.basename(p) for p in glob.glob(os.path.join(PHOTOS_DIR, "*.jpg"))}
    missing = [name for name, _off in FRAMES if name not in all_photos]
    if missing:
        raise SystemExit("missing from %s: %s" % (PHOTOS_DIR, missing))

    report = []
    for name, expect_off in FRAMES:
        path = os.path.join(PHOTOS_DIR, name)
        rgb, _w0, _h0 = R.load_image(path, R.BIG)
        g = R.normalise(R.to_gray(rgb))
        h, w = g.shape
        base = R.chance_diff(g)
        score, pos = R.best_axis(g, 1, base)
        data = [round(float(v), 3) for v in g.ravel()]
        stem = os.path.splitext(name)[0]
        with open(os.path.join(OUT_DIR, stem + ".json"), "w", encoding="utf-8") as f:
            json.dump({"width": int(w), "height": int(h), "data": data}, f)
        report.append((name, w, h, pos, score, expect_off))

    off_axis = []
    for name, w, h, pos, score, expect_off in report:
        off = abs(pos - 0.5) > 0.03
        if off != expect_off:
            raise SystemExit("%s: expected off-centre=%s, best_axis says pos=%.3f"
                              % (name, expect_off, pos))
        if off:
            off_axis.append((name, pos))
        print("%-22s %4dx%-4d best_axis pos=%.3f score=%.3f%s"
              % (name, w, h, pos, score, "  (off-centre)" if off else ""))

    print("\noff-centre (>=3 required): %s"
          % ", ".join("%s=%.3f" % (n, p) for n, p in off_axis))
    if len(off_axis) < 3:
        raise SystemExit("need at least 3 off-centre frames, found %d" % len(off_axis))


if __name__ == "__main__":
    main()
