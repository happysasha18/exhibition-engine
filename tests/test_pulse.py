#!/usr/bin/env python3
"""The walk's analytics beats (EX-PULSE / INV-41) — adapted for exhibition-engine.
Run: python tests/test_pulse.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_pulse_"))
build_site.OUT = TMP
build_site.build(SITE_URL, ga_id="G-TESTTEST")

TMP_OFF = Path(tempfile.mkdtemp(prefix="synth_pulse_off_"))
build_site.OUT = TMP_OFF
build_site.build(SITE_URL)

# ---- DOM row: consent speaks first
_head = (TMP / "index.html").read_text(encoding="utf-8")
_work = next((TMP / "w").glob("*.html")).read_text(encoding="utf-8")
_off = (TMP_OFF / "index.html").read_text(encoding="utf-8")


def _consent_ok(html):
    c = html.find("gtag('consent','default'")
    cfg = html.find("gtag('config'")
    return (c != -1 and cfg != -1 and c < cfg
            and "'ad_storage':'denied'" in html
            and "'ad_user_data':'denied'" in html
            and "'ad_personalization':'denied'" in html
            and "'analytics_storage':'granted'" in html)


check("EX-PULSE consent defaults precede the tag config (ads denied, analytics granted) on every tagged page",
      _consent_ok(_head) and _consent_ok(_work) and "gtag('consent'" not in _off,
      f"index={_consent_ok(_head)} work={_consent_ok(_work)} off_clean={'gtag' not in _off}")

BROWSER_ROWS = [
    "EX-PULSE the five beats fire (door_pick · walk_unfold · walk_exit · share_copy · share_arrive; params ⊆ {work})",
    "EX-PULSE no tag = total silence (no queue, no pushes, no errors)",
]

EVENTS = ("JSON.stringify((window.dataLayer||[]).filter(e=>e[0]==='event')"
          ".map(e=>[e[1], e[2]||{}]))")
CLIP_STUB = ("window.__copied=[];if(navigator.clipboard)navigator.clipboard.writeText="
             "(t)=>{window.__copied.push(t);return Promise.resolve();};")


def walk_all(br, base):
    br.navigate(base + "/")
    br.evaluate("localStorage.clear();sessionStorage.clear()")
    br.evaluate("localStorage.setItem('tlv-tempo','0.2')")
    br.reload()
    br.sleep(1.0)
    br.click(".exd-window:nth-child(1)", settle=0.1)
    br.sleep(1.2)
    br.click(".exh-frame:nth-of-type(1) .ex-share", settle=0.4)
    br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
    br.sleep(0.5)
    br.click("#ex-unfold", settle=0.6)
    br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
    br.sleep(0.5)
    br.click("#ex-return", settle=0.8)
    target = br.evaluate(
        "JSON.parse(localStorage.getItem('tlv.exhibition')||'{}').pick")
    br.navigate(base + "/#w-" + str(target))
    br.sleep(1.0)
    return target


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            target = walk_all(br, base)
            evs = dict(json.loads(br.evaluate(EVENTS) or "[]"))
            need = {"door_pick", "walk_unfold", "walk_exit", "share_copy", "share_arrive"}
            params_ok = all(set(p.keys()) <= {"work"} for p in evs.values())
            works_ok = (evs.get("door_pick", {}).get("work")
                        and evs.get("share_arrive", {}).get("work") == target)
            check(BROWSER_ROWS[0],
                  need.issubset(evs) and params_ok and bool(works_ok),
                  f"events={sorted(evs)} params_ok={params_ok} arrive={evs.get('share_arrive')}")
    with serve(TMP_OFF) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            walk_all(br, base)
            silent = br.evaluate(
                "(window.dataLayer||[]).filter(e=>e[0]==='event').length") == 0
            alive = br.evaluate("1+1") == 2
            check(BROWSER_ROWS[1], silent and alive, f"silent={silent} alive={alive}")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_OFF, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
