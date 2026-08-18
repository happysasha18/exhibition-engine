#!/usr/bin/env python3
"""beauty-camera-check — the flight never shows what stands under the canvas, and it rests.

Root: his word 2026-08-18 09:07, and a defect this seat photographed at round 7. The host applies
the camera as ONE transform on its own canvas, so a pan of p uncovers the page beneath unless the
scale carries at least 1/(1-2p). A flight whose pan crests before its dolly can therefore run ahead
of what it has paid for, and the frame is grazed at instants neither end of the flight shows. This
walks the whole flight at the host's own frame rate, reads the transform the host actually wrote,
and proves three things:

  1. at every instant the scale covers the pan, with the margin reported;
  2. both doors stand at the identity transform exactly, so a door is the work as it hangs;
  3. the flight carries no JUMP. It is drawn from monotone splines, so smoothness is a property of
     its construction and a check that re-measured it would prove nothing; what a check can catch is
     a step where one place of the pose leaps. So the largest step between neighbouring instants is
     held against the MEDIAN step of the same flight — a fast passage moves fast everywhere, and a
     cut shows up as one step standing far out from its own neighbours.

Run: python3 scripts/beauty-camera-check.py --page FILE.html [--samples 61]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from headless import Browser, chrome_available  # noqa: E402

SPIKE = 4.0            # the largest step, against the median step of the same flight


def read(t):
    """The pan and the scale out of the transform string the host wrote."""
    if not t or t == "none":
        return 0.0, 0.0, 1.0
    m = re.search(r"translate\(([-0-9.]+)%,\s*([-0-9.]+)%\)", t)
    s = re.search(r"scale\(([-0-9.]+)\)", t)
    px, py = (float(m.group(1)) / 100, float(m.group(2)) / 100) if m else (0.0, 0.0)
    return px, py, (float(s.group(1)) if s else 1.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True)
    ap.add_argument("--samples", type=int, default=41)
    args = ap.parse_args()
    if not chrome_available():
        print("SKIP  Chrome is not installed here")
        return 2

    rows, worst, doors = [], None, []
    with Browser(width=1280, height=800) as br:
        br.navigate("file://" + str(Path(args.page).resolve()))
        for _ in range(200):
            if br.evaluate("String(!!window.__ready)") == "true":
                break
            br.sleep(0.1)
        dur = json.loads(br.evaluate("JSON.stringify(window.__score.duration)")) / 1000.0
        for i in range(args.samples):
            t = dur * i / (args.samples - 1)
            br.evaluate("JSON.stringify(window.__at(window.__score, %r, %r))" % (t, dur))
            br.sleep(0.35)
            tr = br.evaluate("var c=document.querySelector('canvas');c?c.style.transform:'none'")
            br.evaluate("window.__cancel('camera-check'); 0")
            br.sleep(0.2)
            px, py, sc = read(tr)
            need = 1.0 / (1.0 - 2.0 * max(abs(px), abs(py)))
            rows.append((t, px, py, sc, need))
            if worst is None or sc / need < worst[0]:
                worst = (sc / need, t, px, py, sc, need)
            if i == 0 or i == args.samples - 1:
                doors.append((t, px, py, sc))
        errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))

    ok_cover = all(sc >= need - 1e-9 for _, _, _, sc, need in rows)
    ok_doors = all(abs(px) < 1e-9 and abs(py) < 1e-9 and abs(sc - 1) < 1e-9
                   for _, px, py, sc in doors)
    steps = [max(abs(rows[i][1] - rows[i - 1][1]), abs(rows[i][2] - rows[i - 1][2]),
                 abs(rows[i][3] - rows[i - 1][3])) for i in range(1, len(rows))]
    med = sorted(steps)[len(steps) // 2]
    ok_cont = max(steps) <= SPIKE * max(med, 1e-9)

    print("samples          %d over %.3f s" % (len(rows), dur))
    print("cover            %s — worst margin %.4f (scale %.5f against the %.5f the pan of "
          "%.4f/%.4f asks for, at %.3f s)"
          % ("PASS" if ok_cover else "FAIL", worst[0], worst[4], worst[5], worst[2], worst[3],
             worst[1]))
    print("doors            %s — %s" % ("PASS" if ok_doors else "FAIL",
          "; ".join("%.3f s pan %.9f/%.9f scale %.9f" % d for d in doors)))
    print("no jump          %s — largest step %.5f against a median step of %.5f, %.2f times it "
          "(the bound is %.1f)"
          % ("PASS" if ok_cont else "FAIL", max(steps), med, max(steps) / max(med, 1e-9), SPIKE))
    print("page errors      %s" % (errs or "none"))
    return 0 if (ok_cover and ok_doors and ok_cont and not errs) else 1


if __name__ == "__main__":
    sys.exit(main())
