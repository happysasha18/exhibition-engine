#!/usr/bin/env python3
"""beauty-film — photograph one crossing across its own length, so the eye can judge it.

Root: his word 2026-08-18 09:07. A crossing is judged by watching it; the frames are how this seat
judges its own work between showings, round by round.

The baked page (scripts/beauty-bake.py) carries the bench road `__at(score, seconds, duration)`,
which offers the pass with its clock and its progress pinned at the instant asked for. The host runs
its real frame loop against those pins, so the same instant photographs identically every time.

Run: python3 scripts/beauty-film.py --page FILE.html --out DIR [--frames 13] [--w 390] [--h 844]
"""
import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from headless import Browser, chrome_available  # noqa: E402


def png(br, path):
    d = br._cmd("Page.captureScreenshot", format="png", captureBeyondViewport=False)
    Path(path).write_bytes(base64.b64decode(d["data"]))
    return str(path)


def ready(br, tries=200):
    for _ in range(tries):
        if br.evaluate("String(!!window.__ready)") == "true":
            return True
        br.sleep(0.1)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--frames", type=int, default=13)
    ap.add_argument("--w", type=int, default=390)
    ap.add_argument("--h", type=int, default=844)
    args = ap.parse_args()

    if not chrome_available():
        print("Chrome is not installed here")
        return 2
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()

    with Browser(width=args.w, height=args.h) as br:
        br.navigate("file://" + str(Path(args.page).resolve()))
        if not ready(br):
            print("the page never came up: " + br.evaluate("JSON.stringify(window.__errs||[])"))
            return 1
        dur = json.loads(br.evaluate("JSON.stringify(window.__score.duration)")) / 1000.0
        for i in range(args.frames):
            s = dur * i / (args.frames - 1)
            br.evaluate("JSON.stringify(window.__at(window.__score, %r, %r))" % (s, dur))
            br.sleep(0.55)
            png(br, out / ("%02d-%.2fs.png" % (i, s)))
            br.evaluate("window.__cancel('film'); 0")
            br.sleep(0.35)
        errs = br.evaluate("JSON.stringify(window.__errs||[])")
        rep = json.loads(br.evaluate("JSON.stringify(window.__report())"))
    print("frames: %s" % out)
    print("errors: %s" % errs)
    print("state: %s  drew: %s  live: %s" % (rep.get("state"), rep.get("drew"), rep.get("live")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
