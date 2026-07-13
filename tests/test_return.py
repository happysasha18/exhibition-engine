#!/usr/bin/env python3
"""EX-RETURN (INV-78): the door says there is more.

Leaving a walk to the door shows a quiet farewell; a COLD arrival from a browser that has walked here
before shows a welcome-back line in the greeting's place; a brand-new visitor sees only the ordinary
greeting. Localized site copy, English fallback, museum-quiet. Browser rows drive a REAL headless Chrome;
Chrome absent -> pinned expected SKIPs. Run: python tests/test_return.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_return_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
CSS = (TMP / "exhibition.css").read_text(encoding="utf-8")
GREET = json.loads((ROOT / "tests" / "fixture_content" / "data" / "greetings.json").read_text(encoding="utf-8"))
LANGS = GREET["langs"]
EN_EXIT = LANGS["en"]["more_exit"]
EN_RETURN = LANGS["en"]["more_return"]

# ---------------------------------------------------------------- string / copy rows
check("EX-RETURN the door builds the 'there is more' slot (#exd-more)",
      'id="exd-more"' in JS and "exd-more" in CSS, "no #exd-more slot in door html/css")
check("EX-RETURN the client sets a local 'has walked' flag on exit and reads it on a cold arrival",
      'BEEN_KEY = "ex.been"' in JS and "L.t.more_exit" in JS and "L.t.more_return" in JS,
      "BEEN_KEY / more_exit / more_return logic missing")
missing = [lg for lg, t in LANGS.items() if not t.get("more_exit") or not t.get("more_return")]
check("EX-RETURN both lines are localized across every covered tongue (English fallback)",
      not missing, f"languages missing a line: {missing}")

# ---------------------------------------------------------------- browser rows
BROWSER_ROWS = [
    "EX-RETURN leaving a walk to the door shows the farewell line",
    "EX-RETURN a cold arrival from a browser that has walked before shows the welcome-back line (greeting yields)",
    "EX-RETURN a brand-new visitor sees neither line",
]
MORE = ("(()=>{const m=document.getElementById('exd-more'),g=document.getElementById('exd-greet'),"
        "d=document.getElementById('ex-door');"
        "return JSON.stringify({text:m?m.textContent:'',hidden:m?m.hidden:true,"
        "greetHidden:g?g.hidden:true,atDoor:!!d&&!d.hidden});})()")


def _boot(br, base):
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("localStorage.setItem('ex-tempo','0.05')")
    br.reload(); br.sleep(1.1)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            br.click(".exd-window:nth-child(1)", settle=0.6)
            br.sleep(0.9)
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.3)
            br.click("#ex-return", settle=0.6)
            br.sleep(0.6)
            m = json.loads(br.evaluate(MORE))
            check(BROWSER_ROWS[0],
                  m["atDoor"] and not m["hidden"] and m["text"].strip() == EN_EXIT.strip(),
                  f"more={m} expected={EN_EXIT!r}")
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            br.evaluate("localStorage.setItem('ex.been','1')")
            br.reload(); br.sleep(1.1)
            m = json.loads(br.evaluate(MORE))
            # the welcome-back is an ADDED quiet line; the daypart greeting is kept (EX-GREET stands)
            check(BROWSER_ROWS[1],
                  m["atDoor"] and not m["hidden"] and m["text"].strip() == EN_RETURN.strip(),
                  f"more={m} expected={EN_RETURN!r}")
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            m = json.loads(br.evaluate(MORE))
            check(BROWSER_ROWS[2], m["atDoor"] and m["hidden"], f"more={m}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
