#!/usr/bin/env python3
"""EX-STANDING — the standing work no longer breathes at rest (SPEC.md Requirement 37, retired
2026-09-06).

RETIRED 2026-09-06 on the owner's word: a work that moves while nobody is touching it is excess,
and the motion belongs under the hand instead (`pass-hand.js`'s own `paint()`, unchanged by this).
`engine/client/08b-standing.js`'s `standDraw()` now returns `false` unconditionally, right after
`standClear()`, so the renderer this suite once proved never draws again and `standTick` stops
re-arming its own loop for good. The renderer's own code is kept, not deleted — a later "bring the
ambient breath back" has a real body to re-enable — but this suite now asserts the PRODUCT it left
behind rather than the one it retired: a resting work carries no inline `scale`, and no loop is
running to put one there.

This is a product-level rewrite, not a masked skip: the old suite's own proof (two photographs of
one work, taken at two moments of its breath, compared byte-for-byte through Pillow) proved a
renderer that no longer runs, so it is gone along with the Pillow dependency it alone needed — a
suite that asserts absence reads the DOM directly and needs no camera.

WHAT WOULD REDDEN THIS SUITE NOW: `engine/client/08b-standing.js`'s stand-down lifted, or a stray
inline `scale` left on a picture by anything else.

Run: python3 tests/test_pass_standing.py
"""
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available, wait_for  # noqa: E402

SITE_URL = "https://synth.example.com"
PHONE = (390, 844)     # the phone frame lab/carrier-check.py measures on
DESK = (1280, 900)     # the desk frame every other walk row reads

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# `wait_for` used to be a local copy of the same poll loop headless.py now carries once, shared
# across every suite (row S-119, 2026-09-09 — see the long comment on the shared copy for the
# incident). This suite's own measured budget was 8.0s and stays 8.0s here, bound once so every
# bare call below keeps that number without retyping it, and any call that states its own timeout
# keeps overriding it exactly as before.
import functools
wait_for = functools.partial(wait_for, timeout=8.0, step=0.05)


ROWS = [
    "EX-STANDING row1 a resting work carries no inline scale: every hung work's own picture, at "
    "rest after the walk has settled, reads an empty style.scale",
    "EX-STANDING row2 the renderer's own loop never arms: standingReport() names no work being "
    "drawn and reports its loop not running",
    "EX-STANDING row3 the stand-down survives a scroll: paging through several works in turn "
    "leaves every one of them without a scale the whole way, seated or not",
    "EX-TILT row4 on a phone, a tilt slides the standing work on a mass and it comes home when the phone levels",
]

if not chrome_available():
    for r in ROWS:
        skip(r, "chrome is not available on this machine")
else:
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on",
                                      "composer": build_site.manifest_block("unfold")}
    TMP = Path(tempfile.mkdtemp(prefix="synth_standing_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL)

    DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
    SHOWN = 10
    WALK = json.dumps(json.dumps({"v": str(DATA["version"]),
                                  "pick": DATA["door"]["pool"][0]["id"], "shown": SHOWN}))

    def room(br, base):
        """The walk itself, hung and standing still at its first work — no door, no gesture."""
        br.navigate(base + "/")
        br.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
        br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics: 'on'}))")
        br.reload()
        for _ in range(40):
            br.sleep(0.15)
            if br.evaluate("document.documentElement.classList.contains('ex-walk')"
                           "&&document.querySelectorAll('.exh-frame').length>0"
                           "&&scrollY===0"):
                break
        br.sleep(0.6)

    def standing(br):
        return json.loads(br.evaluate("JSON.stringify(window.__exPass.standing())"))

    def scales(br):
        """What breath each picture on the walk is carrying this instant, by work — empty on
        every one of them is the whole of this suite's own reading now."""
        return json.loads(br.evaluate(
            "JSON.stringify(Object.fromEntries([...document.querySelectorAll('.exh-frame')]"
            ".map(f=>[f.dataset.id, f.querySelector('img.work').style.scale||''])))"))

    try:
        with serve(TMP) as base:
            # ------------------------------------------------------- row 1: a resting work, both forms
            all_empty = {}
            for tag, (w, h) in (("phone", PHONE), ("desk", DESK)):
                with Browser(width=w, height=h) as br:
                    room(br, base)
                    wait_for(br, "!!(window.__exPass && window.__exPass.standing)")
                    br.sleep(0.5)   # give a stray rAF every chance to have already run once
                    all_empty[tag] = scales(br)
            bad = {tag: {k: v for k, v in sc.items() if v}
                   for tag, sc in all_empty.items()}
            bad = {tag: v for tag, v in bad.items() if v}
            print("\nscale carried by every hung work, phone and desk forms: %r" % all_empty)
            check(ROWS[0],
                  not bad and all(all_empty.values()),
                  f"non-empty scale found: {bad!r}" if bad else "no works read (empty walk?)")

            # ------------------------------------------------------------ row 2: the report is honest
            with Browser(width=DESK[0], height=DESK[1]) as br:
                room(br, base)
                wait_for(br, "!!(window.__exPass && window.__exPass.standing)")
                br.sleep(0.5)
                rep = standing(br)
                print("standingReport() at rest: %r" % rep)
                check(ROWS[1],
                      rep["drawing"] is None and rep["running"] is False,
                      f"standingReport()={rep!r}")

            # -------------------------------------------------- row 3: survives a scroll, several works
            with Browser(width=DESK[0], height=DESK[1]) as br:
                room(br, base)
                wait_for(br, "!!(window.__exPass && window.__exPass.standing)")
                seen_nonempty = None
                for _ in range(4):
                    br.wheel(delta_y=500)
                    br.sleep(0.5)
                    sc = scales(br)
                    if any(sc.values()):
                        seen_nonempty = sc
                        break
                rep_after = standing(br)
                print("scale after four page turns: %r; standingReport(): %r"
                      % (seen_nonempty, rep_after))
                check(ROWS[2],
                      seen_nonempty is None and rep_after["drawing"] is None
                      and rep_after["running"] is False,
                      f"non-empty scale mid-scroll: {seen_nonempty!r}; report: {rep_after!r}")
            # ------------------------------------------------ row 4: the tilt of the phone, the slide
            with Browser(width=PHONE[0], height=PHONE[1]) as br:
                br.set_viewport(PHONE[0], PHONE[1], mobile=True)
                br.touch(True)                       # a phone's own pointer is coarse: the tilt arms on one
                room(br, base)
                wait_for(br, "!!(window.__exPass && window.__exPass.standing)")
                br.sleep(0.5)
                tilt = lambda b, g: br.evaluate(
                    "window.dispatchEvent(new DeviceOrientationEvent('deviceorientation',"
                    "{alpha:0,beta:%s,gamma:%s})),1" % (b, g))
                tilt(40, 0)               # where the phone is held: the zero
                br.sleep(0.3)
                tilt(40, 18)              # tipped a full tilt to the right
                br.sleep(1.8)
                rep = standing(br)["tilt"]
                w = br.evaluate("(function(){var f=document.querySelector('.exh-frame img.work');return f?f.getBoundingClientRect().width:0})()")
                slid = rep["translate"] or ""
                x = float(slid.split("px")[0]) if slid else 0.0
                tilt(40, 0)               # levelled again
                br.sleep(2.2)
                rep2 = standing(br)["tilt"]
                print("tilt report tipped: %r; levelled: %r; first work width %s" % (rep, rep2, w))
                check(ROWS[3],
                      rep["armed"] and rep["on"] and rep["drawing"] is not None
                      and w > 0 and abs(x - w * rep["law"]["reachOfWidth"]) < w * 0.01
                      and abs(rep2["at"]["x"]) < 0.01
                      and (not rep2["translate"] or abs(float(rep2["translate"].split("px")[0])) < w * 0.002),
                      f"tipped translate={slid!r} against a reach of {w * 0.04:.1f}px; levelled: {rep2!r}")
    finally:
        import shutil
        shutil.rmtree(TMP, ignore_errors=True)

# ---------------------------------------------------------------- report
passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
