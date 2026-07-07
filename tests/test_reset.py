#!/usr/bin/env python3
"""Asking the museum to forget (EX-RESET / INV-35) — adapted for exhibition-engine.
Run: python tests/test_reset.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_reset_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

BROWSER_ROWS = [
    "INV-35(a) reset wipes the own trace (walk · place · tempo) and lands the COLD door, greeted",
    "INV-35(b) the param strips itself and lays NO history step; a reload re-wipes nothing",
    "INV-35(c) reset with nothing stored is the same cold door, never an error",
    "INV-35(d) the strip eats only `reset` — sibling params and the hash survive",
]

AT_DOOR = "document.body.classList.contains('ex-door')"
GREETED = "(()=>{const g=document.getElementById('exd-greet');return !!g && !g.hidden})()"
KEYS_GONE = ("localStorage.getItem('tlv.exhibition')===null"
             "&&sessionStorage.getItem('tlv.place')===null"
             "&&localStorage.getItem('tlv-tempo')===null")

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    def pick(br, nth=1):
        try:
            br.click(f".exd-window:nth-child({nth})", settle=0.1)
        except RuntimeError:
            return
        br.sleep(1.6)

    with serve(TMP) as base, Browser(width=1280, height=900) as br:
        # a · a stored walk + a tempo override + a place marker, then /?reset
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("sessionStorage.clear()")
        br.evaluate("localStorage.setItem('tlv-tempo','0.2')")
        br.reload()
        br.sleep(1.0)
        pick(br)
        walked = not br.evaluate(AT_DOOR)
        br.evaluate("sessionStorage.setItem('tlv.place','{\"v\":\"x\",\"id\":\"y\"}')")
        br.navigate(base + "/?reset")
        br.sleep(1.2)
        check(BROWSER_ROWS[0],
              walked and br.evaluate(AT_DOOR) and br.evaluate(GREETED)
              and br.evaluate(KEYS_GONE),
              f"walked={walked} at_door={br.evaluate(AT_DOOR)} "
              f"greeted={br.evaluate(GREETED)} keys_gone={br.evaluate(KEYS_GONE)}")

        # b · the strip: no `reset` in the address, ONE history entry per navigation
        hl_before = br.evaluate("history.length")
        br.navigate(base + "/?reset")
        br.sleep(1.2)
        hl_after = br.evaluate("history.length")
        stripped = br.evaluate("location.search") == ""
        br.evaluate("localStorage.setItem('tlv-tempo','0.2')")
        br.reload()
        br.sleep(1.0)
        pick(br)
        br.reload()
        br.sleep(1.2)
        survives = (not br.evaluate(AT_DOOR)
                    and br.evaluate("localStorage.getItem('tlv.exhibition')") is not None)
        check(BROWSER_ROWS[1],
              stripped and (hl_after - hl_before == 1) and survives,
              f"search='{br.evaluate('location.search')}' hlen {hl_before}→{hl_after} "
              f"reload_survives={survives}")

        # c · idempotent: nothing stored, /?reset → the same cold door, no error
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("sessionStorage.clear()")
        br.navigate(base + "/?reset")
        br.sleep(1.2)
        n_win = br.evaluate("document.querySelectorAll('.exd-window').length")
        check(BROWSER_ROWS[2],
              br.evaluate(AT_DOOR) and br.evaluate(GREETED) and n_win > 0,
              f"at_door={br.evaluate(AT_DOOR)} greeted={br.evaluate(GREETED)} windows={n_win}")

        # d · only `reset` leaves the address
        br.navigate(base + "/?x=1&reset#foo")
        br.sleep(1.2)
        check(BROWSER_ROWS[3],
              br.evaluate("location.search") == "?x=1"
              and br.evaluate("location.hash") == "#foo",
              f"search='{br.evaluate('location.search')}' hash='{br.evaluate('location.hash')}'")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
