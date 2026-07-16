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
            # the farewell waits for the SECOND real exit (INV-78): the first leave is silent
            first = None
            for leave in (1, 2):
                br.click(".exd-window:nth-child(1)", settle=0.6)
                br.sleep(0.9)
                br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
                br.sleep(0.3)
                br.click("#ex-return", settle=0.6)
                br.sleep(0.6)
                if leave == 1:
                    first = json.loads(br.evaluate(MORE))
            m = json.loads(br.evaluate(MORE))
            check(BROWSER_ROWS[0],
                  first is not None and first["hidden"]
                  and m["atDoor"] and not m["hidden"] and m["text"].strip() == EN_EXIT.strip(),
                  f"first_exit={first} second_exit={m} expected={EN_EXIT!r} "
                  f"(silent on the 1st leave, the line from the 2nd)")
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            # a walked-before browser returning INSIDE the 6h–14d window (INV-78): the flag plus a
            # last-visit clock ~7h old — sooner is a reload (silent), later is met as new (silent)
            br.evaluate("localStorage.setItem('ex.been','1');"
                        "localStorage.setItem('ex.last', String(Date.now() - 7*60*60*1000))")
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

# ---------------------------------------------------------------- EX-RETURN/INV-94 wake-reset row
# a tab idle past the return window's lower bound wakes AT THE DOOR (a reload), not wherever it
# stood — the reload lands cold, and the prior load's ex.last still puts it inside the welcome-back
# window (INV-78's own machinery, untouched). A wake UNDER the bound, or while offline, never reloads.
WAKE_ROW = "EX-RETURN/INV-94 a tab idle past the bound wakes at the door"
WAKE_GUARD_ROW = "EX-RETURN/INV-94 the minute backstop is a wake detector (string)"
# an overdue minute tick (after a real system sleep) must run the wake check itself, not just
# re-stamp the clock — else a tab that never sees a visibilitychange (a lid-close wake) never resets
check(WAKE_GUARD_ROW,
      "if (!document.hidden) wakeGate()" in JS,
      "the visibility-guarded wake-detector line is missing from the baked client")
HOUR_MS = 60 * 60 * 1000
DAY_MS = 24 * HOUR_MS


def _enter_walk(br):
    """a pick into the walk, standing mid-walk (never exited)."""
    br.click(".exd-window:nth-child(1)", settle=0.6)
    br.sleep(0.6)


def _walk_and_exit(br):
    """enter through a pick, run to the closing screen, and take the exit control back to the door
    (mirrors the farewell rows' own inline exit pattern above, factored out for reuse here)."""
    br.click(".exd-window:nth-child(1)", settle=0.6)
    br.sleep(0.9)
    br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
    br.sleep(0.3)
    br.click("#ex-return", settle=0.6)
    br.sleep(0.6)


def _wake(br, shift_ms, offline=False):
    """stamp a pre-wake marker (destroyed by a real navigation), optionally force navigator.onLine
    false, shift Date.now forward by shift_ms (the page's own last-waking stamp was left at load
    time — this simulates the idle gap), then fire visibilitychange->visible, the real wake trigger."""
    br.evaluate("window.__preWake = true")
    if offline:
        br.evaluate("Object.defineProperty(navigator,'onLine',{get:()=>false,configurable:true})")
    br.evaluate(f"Date.now = (o => () => o() + {shift_ms})(Date.now)")
    try:
        br.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
    except RuntimeError:
        pass    # a genuine reload can tear the execution context down mid-dispatch
    br.sleep(1.0)


if not chrome_available():
    skip(WAKE_ROW, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # 1 · a 7h idle (past RETURN_MIN_MS=6h) reloads to the door, once, no loop — NO 'ex.been' seed
        #     here on purpose: a first-session walker never exits, so it never got that flag any other
        #     way; the wake itself must stamp it (the coordinator's second hole), or no welcome-back
        #     line could ever show for a walker asleep on their very first walk
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            _enter_walk(br)
            # ex.last is consumed-and-overwritten on EVERY boot (INV-78/79's own gap capture, at
            # module load) — seed it fresh right here so the WAKE's own reload (the one boot that
            # matters) is the one that reads it, not an earlier seeding reload
            br.evaluate(f"localStorage.setItem('ex.last', String(Date.now() - {DAY_MS}))")  # inside the welcome-back window too
            _wake(br, 7 * HOUR_MS)
            reloaded = br.evaluate("window.__preWake") is not True   # the marker did not survive
            at_door = br.evaluate("document.body.classList.contains('ex-door')")
            m = json.loads(br.evaluate(MORE))                        # welcome-back still joins the ask
            br.evaluate("window.__stillHere = true")
            br.sleep(0.6)                                            # no second, unprompted reload
            no_loop = br.evaluate("window.__stillHere") is True
            over_bound = (reloaded and at_door and no_loop
                          and m["atDoor"] and not m["hidden"] and m["text"].strip() == EN_RETURN.strip())
        # 4 · a tab asleep on a RETURNED door (walked, exited, held on reload) wakes cold too — an
        #     ordinary reload HOLDS history.state.returned (INV-54), so an unfixed wake used to land
        #     right back on the silent held-door branch: no greeting, no welcome-back line
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            _walk_and_exit(br)                                        # walk in, exit — the door is now "held"
            br.evaluate(f"localStorage.setItem('ex.last', String(Date.now() - {DAY_MS}))")  # inside the window
            _wake(br, 7 * HOUR_MS)
            reloaded4 = br.evaluate("window.__preWake") is not True
            m4 = json.loads(br.evaluate(MORE))
            returned_door_wakes_greeted = (reloaded4 and m4["atDoor"] and not m4["greetHidden"]
                                            and not m4["hidden"] and m4["text"].strip() == EN_RETURN.strip())
        # 2 · a 1h idle (under the bound) never reloads — the walk stands exactly as it stood
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            _enter_walk(br)
            before_walk = br.evaluate("!!document.querySelector('.exh-frame')")
            _wake(br, 1 * HOUR_MS)
            under_bound = (br.evaluate("window.__preWake") is True   # the marker survived — no navigation
                           and (not br.evaluate("document.body.classList.contains('ex-door')"))
                           and br.evaluate("!!document.querySelector('.exh-frame')") == before_walk)
        # 3 · a 7h idle while OFFLINE never reloads (never lands the wake in a browser error)
        with Browser(width=390, height=844) as br:
            _boot(br, base)
            _enter_walk(br)
            _wake(br, 7 * HOUR_MS, offline=True)
            offline_no_reload = (br.evaluate("window.__preWake") is True
                                  and (not br.evaluate("document.body.classList.contains('ex-door')")))
        check(WAKE_ROW,
              over_bound and returned_door_wakes_greeted and under_bound and offline_no_reload,
              f"over_bound(7h→door,no-loop,welcome-back)={over_bound} "
              f"returned_door_wakes_greeted={returned_door_wakes_greeted} "
              f"under_bound(1h→no-nav)={under_bound} offline(7h→no-nav)={offline_no_reload}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
