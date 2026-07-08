#!/usr/bin/env python3
"""EX-PROTECT (INV-49): right-click / drag / pinch protection on hung works.
A grabbed work meets a gracious enjoy line (via the shared toast), never the browser's raw
save sheet. The `enjoy` i18n key ships in the locale schema and the validate gate.
Run: python tests/test_protect.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_protect_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# ---------------------------------------------------------------- data rows

# 1 · the `enjoy` string is present in the greetings cache and the worker schema
greet = json.loads((TMP / "exhibition_data.json").read_text()).get("greet") or {}
langs = greet.get("langs") or {}
missing_enjoy = [c for c, L in langs.items() if not (L.get("enjoy") or "").strip()]
worker_src = (ROOT / "engine" / "assets" / "worker.js").read_text(encoding="utf-8")
enjoy_in_schema = '"enjoy"' in worker_src and "enjoy" in worker_src
check("EX-PROTECT enjoy string in locale cache (all langs) + worker schema includes enjoy",
      not missing_enjoy and enjoy_in_schema,
      f"missing_enjoy={missing_enjoy} schema_has_enjoy={enjoy_in_schema}")

# 2 · CSS: img.work carries the soft-deter properties
css_src = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")
css_ok = ("user-select:none" in css_src
          and "-webkit-user-drag:none" in css_src
          and "-webkit-touch-callout:none" in css_src
          and "touch-action:pan-x pan-y" in css_src)
check("EX-PROTECT CSS: img.work carries user-select/user-drag/touch-callout:none + touch-action:pan-x pan-y",
      css_ok, f"css_src snippet not found (see exhibition.css img.work block)")

# 3 · JS: enjoyLine, onGrab, contextmenu/dragstart/gesturestart/gesturechange all present
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
js_ok = ("function enjoyLine(" in js_src
         and "function onGrab(" in js_src
         and "contextmenu" in js_src
         and "dragstart" in js_src
         and "gesturestart" in js_src
         and "gesturechange" in js_src
         and "ev.preventDefault()" in js_src)
check("EX-PROTECT JS: enjoyLine, onGrab, contextmenu/dragstart/gesturestart/gesturechange wired",
      js_ok, "one or more EX-PROTECT symbols missing from exhibition.js")

BROWSER_ROWS = [
    "EX-PROTECT-GIFT desktop right-click on a work opens the gift ceremony (not a browser save sheet)",
    "EX-PROTECT drag on a work is prevented (no drag ghost, enjoy toast fires)",
    "EX-PROTECT-GIFT the gift ceremony line carries the site host from ROOT_URL",
    "EX-PROTECT right-click on chrome (share button) is NOT intercepted (browser menu still works)",
]

TOAST = "(()=>{const t=document.getElementById('ex-toast');return t&&!t.hidden?t.textContent:null;})()"
GIFT = ("(()=>{const g=document.getElementById('ex-gift-card');"
        "return g&&!g.hidden?(g.querySelector('.gift-line')||{}).textContent||'':null;})()")
AT_DOOR = "document.body.classList.contains('ex-door')"
FRAME_IDS = "Array.from(document.querySelectorAll('.exh-frame')).map(f=>f.dataset.id)"


def enter(br, base):
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("localStorage.setItem('tlv-tempo','0.5')")  # toast lives 1.5s — enough to check
    br.reload()
    br.sleep(0.8)
    br.click(".exd-window:nth-child(1)", settle=0.1)
    br.sleep(1.2)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # 0 · desktop right-click OPENS THE GIFT CEREMONY (offered, never dumped) — EX-PROTECT-GIFT
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            gift = br.evaluate(GIFT)
            # the gift card must be visible with a non-empty gift line
            check(BROWSER_ROWS[0],
                  gift is not None and len(gift.strip()) > 0,
                  f"gift_line={gift!r}")

        # 1 · drag on a work is prevented (dragstart fires toast, no drag ghost)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new DragEvent('dragstart',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            toast = br.evaluate(TOAST)
            check(BROWSER_ROWS[1],
                  toast is not None and len(toast.strip()) > 0,
                  f"toast={toast!r}")

        # 2 · the gift ceremony line carries the site host (stripped of protocol)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            gift = br.evaluate(GIFT) or ""
            # site host = hostname from SITE_URL without protocol
            host = SITE_URL.replace("https://", "").replace("http://", "")
            check(BROWSER_ROWS[2],
                  host in gift,
                  f"gift_line={gift!r} want host={host!r}")

        # 3 · right-click on a share button is NOT intercepted
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            # contextmenu on the share button must not produce the enjoy toast
            br.evaluate("(()=>{const b=document.querySelector('.ex-share');"
                        "if(b)b.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}));})()")
            br.sleep(0.4)
            toast = br.evaluate(TOAST)
            check(BROWSER_ROWS[3],
                  toast is None,
                  f"toast={toast!r} (should be None — chrome is not protected)")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
