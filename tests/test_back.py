#!/usr/bin/env python3
"""Honest Back (INV-32) — adapted for exhibition-engine synthetic fixture.
Run: python tests/test_back.py
"""
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
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


TMP = Path(tempfile.mkdtemp(prefix="synth_back_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

CFG = json.loads((TMP / "config.json").read_text())["exhibition"]
SPREAD = CFG["spread_size"]
SLUG = {w["id"]: w["slug"]
        for w in json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))["works"]}

BROWSER_ROWS = [
    "INV-32(a) crossing lays a step: Back from the hang re-shows the door AS IT STOOD",
    "INV-32(b) re-opened door: Back returns to the walk untouched, closing screen in view",
    "INV-32(c) the place survives any return (the walk tracks the frame in view); marker per-tab, never localStorage",
    "INV-32(d) superseded arc never renders: fresh-top pick; old walk step renders the walk as it now is",
    "INV-32(e) «ещё 5» lays NO history step",
    "INV-32(f) work-page return is a plain script-free link that still keeps the place",
]

DOOR_IDS = "Array.from(document.querySelectorAll('.exd-window')).map(b=>b.dataset.id)"
FRAME_IDS = "Array.from(document.querySelectorAll('.exh-frame')).map(f=>f.dataset.id)"
AT_DOOR = "document.body.classList.contains('ex-door')"
N_FRAMES = "document.querySelectorAll('.exh-frame').length"
FRAME_IN_VIEW = ("(()=>{const els=[...document.querySelectorAll('.exh-frame')];"
                 "const m=els.find(f=>{const r=f.getBoundingClientRect();"
                 "return r.top<innerHeight*.5&&r.bottom>innerHeight*.5});"
                 "return m?m.dataset.id:null})()")

work_html = next((TMP / "w").glob("*.html")).read_text(encoding="utf-8")
check("INV-32(f/DOM) backpointer stays a plain link; no ex.place script leaks onto /w/",
      'href="/"' in work_html and "ex.place" not in work_html)

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    def fresh(br, base):
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("sessionStorage.clear()")
        br.evaluate("localStorage.setItem('ex-tempo','0.2')")
        br.reload()
        br.sleep(1.0)

    def pick(br, nth=1):
        br.click(f".exd-window:nth-child({nth})", settle=0.1)
        br.sleep(1.6)

    def to_fin(br):
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.5)

    def go_back(br, wait=1.2):
        try:
            br.evaluate("history.back()")
        except RuntimeError:
            pass
        br.sleep(wait)

    def safe(br, expr, dflt=None):
        try:
            return br.evaluate(expr)
        except RuntimeError:
            return dflt

    with serve(TMP) as base, Browser(width=1280, height=900) as br:
        # a · Back from the hang → the door as it stood
        fresh(br, base)
        stood = br.evaluate(DOOR_IDS)
        pick(br)
        in_hang = not br.evaluate(AT_DOOR) and br.evaluate(N_FRAMES) == SPREAD
        go_back(br)
        check(BROWSER_ROWS[0],
              in_hang and br.evaluate(AT_DOOR) and br.evaluate(DOOR_IDS) == stood,
              f"at_door={br.evaluate(AT_DOOR)} same_spread={br.evaluate(DOOR_IDS) == stood}")

        # b · fin's «⟲», then Back: walk untouched, closing screen in view
        fresh(br, base)
        pick(br)
        arc = br.evaluate(FRAME_IDS)
        stored = br.evaluate("localStorage.getItem('ex.exhibition')")
        to_fin(br)
        br.click("#ex-return", settle=1.0)
        at_door_mid = br.evaluate(AT_DOOR)
        go_back(br)
        fin_vis = br.evaluate("(()=>{const f=document.getElementById('exh-fin');if(!f)return false;"
                              "const r=f.getBoundingClientRect();return r.top<innerHeight&&r.bottom>0})()")
        check(BROWSER_ROWS[1],
              at_door_mid and (not br.evaluate(AT_DOOR))
              and br.evaluate(FRAME_IDS) == arc
              and br.evaluate("localStorage.getItem('ex.exhibition')") == stored
              and fin_vis,
              f"door_opened={at_door_mid} fin_in_view={fin_vis}")

        # c · the place survives any return
        fresh(br, base)
        pick(br)
        target = br.evaluate("document.querySelectorAll('.exh-frame')[3].dataset.id")
        br.evaluate("document.querySelectorAll('.exh-frame')[3].scrollIntoView({behavior:'instant'})")
        br.sleep(0.8)
        marker_home_ok = br.evaluate(
            "!!sessionStorage.getItem('ex.place') && !localStorage.getItem('ex.place')")
        br.reload()
        br.sleep(1.4)
        check(BROWSER_ROWS[2],
              marker_home_ok and br.evaluate(FRAME_IN_VIEW) == target,
              f"per_tab={marker_home_ok} "
              f"in_view={br.evaluate(FRAME_IN_VIEW)} want={target}")

        # d · superseded arc: fresh-top; the old walk step renders the walk as it now is
        fresh(br, base)
        pick(br, 1)
        to_fin(br)
        br.click("#ex-return", settle=1.0)
        stood2 = br.evaluate(DOOR_IDS)
        pick(br, 2)
        new_arc = br.evaluate(FRAME_IDS)
        fresh_top = br.evaluate("scrollY") < 5 and not br.evaluate(AT_DOOR)
        go_back(br)
        door_ok = br.evaluate(AT_DOOR) and br.evaluate(DOOR_IDS) == stood2
        go_back(br)
        check(BROWSER_ROWS[3],
              fresh_top and door_ok
              and (not br.evaluate(AT_DOOR))
              and br.evaluate(FRAME_IDS) == new_arc
              and br.evaluate(N_FRAMES) > 0,
              f"fresh_top={fresh_top} door_as_stood={door_ok} "
              f"renders_current={br.evaluate(FRAME_IDS) == new_arc}")

        # e · «ещё 5» lays no history step
        fresh(br, base)
        pick(br)
        hl0 = br.evaluate("history.length")
        n0 = br.evaluate(N_FRAMES)
        to_fin(br)
        br.click("#ex-unfold", settle=0.8)
        check(BROWSER_ROWS[4],
              br.evaluate(N_FRAMES) > n0 and br.evaluate("history.length") == hl0,
              f"frames {n0}→{br.evaluate(N_FRAMES)} hlen {hl0}→{br.evaluate('history.length')}")

        # f · work page: plain link, keeps place
        fresh(br, base)
        pick(br)
        target = br.evaluate("document.querySelectorAll('.exh-frame')[2].dataset.id")
        br.evaluate("document.querySelectorAll('.exh-frame')[2].scrollIntoView({behavior:'instant'})")
        br.sleep(0.8)
        br.navigate(base + SLUG[target])
        br.sleep(0.6)
        work_url = br.evaluate("location.href")
        no_script = br.evaluate(
            "[...document.scripts].every(s=>s.type==='application/ld+json')")
        br.click(".enter", settle=2.0)
        link_keeps_place = (br.evaluate("location.pathname") == "/"
                            and br.evaluate(FRAME_IN_VIEW) == target)
        br.navigate(work_url)
        br.evaluate("localStorage.clear();sessionStorage.clear()")
        br.click(".enter", settle=2.0)
        cold_plain = (br.evaluate("location.pathname") == "/"
                      and br.evaluate(AT_DOOR))
        check(BROWSER_ROWS[5], no_script and link_keeps_place and cold_plain,
              f"no_script={no_script} link_keeps_place={link_keeps_place} cold_plain={cold_plain}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
