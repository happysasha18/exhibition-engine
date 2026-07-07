#!/usr/bin/env python3
"""The coat-check token (EX-MEMORY / INV-43) — adapted for exhibition-engine synthetic fixture.
With the memory flag on, a first visit mints a random token and the walk reports the frames
it met in ONE debounced call; a reload keeps the token; `?reset` drops it (forgetting is whole);
the edge contract merges-never-replaces, caps the record, guards its inputs.
The edge is STUBBED — the suite never leaves the machine.
If the engine does not yet produce _worker.js for visitor_memory, the contract rows
FAIL and the gap is recorded in E3_REPORT.md.
Chrome absent → pinned expected SKIPs. Run: python tests/test_memory.py
"""
import json
import re
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


TMP = Path(tempfile.mkdtemp(prefix="synth_mem_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["visitor_memory"])

TMP_OFF = Path(tempfile.mkdtemp(prefix="synth_mem_off_"))
build_site.OUT = TMP_OFF
build_site.build(SITE_URL)

# ---------------------------------------------------------------- the edge contract (string)
_worker_path = TMP / "_worker.js"
_worker_exists = _worker_path.exists()
w = _worker_path.read_text(encoding="utf-8") if _worker_exists else ""

check("EX-MEMORY edge contract: merge-not-replace, ~500 cap, 2KB guard, shaped tokens/ids, 180d expiry",
      _worker_exists
      and "/api/visitor" in w
      and "new Set" in w and ".add(" in w                      # merge into the stored set
      and "slice(-500)" in w and "2048" in w
      and "expirationTtl: 15552000" in w
      and bool(re.search(r"\^\[a-z0-9\]\{16,40\}\$", w))      # token shape
      and '"v:"' in w,                                          # prefixed keys, one namespace
      f"worker_exists={_worker_exists}" + (
          " a contract clause missing from the shipped worker" if _worker_exists else ""))
check("EX-MEMORY the flagged-off bundle mints nothing server-side",
      not (TMP_OFF / "_worker.js").exists(),
      "worker shipped without any worker flag")

BROWSER_ROWS = [
    "EX-MEMORY token mints once + ONE debounced report of walked frames; reload keeps the token",
    "EX-MEMORY forgetting is whole (?reset drops the token; a new arrival mints a NEW one)",
]

STUB = """
window.__mem = [];
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/visitor')>=0){
    window.__mem.push({u:String(u),body:(o&&o.body)||null,method:(o&&o.method)||'GET'});
    return Promise.resolve(new Response('{"seen":[]}',{status:200}));
  }
  return _f.apply(this,arguments);};})();
"""
TOKEN = "localStorage.getItem('tlv.visitor')"

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(STUB)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('tlv-tempo','0.2')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=0.1)
            br.sleep(1.2)
            tok1 = br.evaluate(TOKEN)
            first_id = br.evaluate("document.querySelector('.exh-frame').dataset.id")
            # walk two more frames, then let the debounce flush
            br.evaluate("document.querySelectorAll('.exh-frame')[1].scrollIntoView({behavior:'instant'})")
            br.sleep(0.8)
            br.evaluate("document.querySelectorAll('.exh-frame')[2].scrollIntoView({behavior:'instant'})")
            br.sleep(4.0)
            calls = json.loads(br.evaluate("JSON.stringify(window.__mem)") or "[]")
            puts = [c for c in calls if c["method"] in ("PUT", "POST")]
            body = json.loads(puts[0]["body"]) if puts and puts[0]["body"] else {}
            token_ok = bool(tok1) and re.fullmatch(r"[a-z0-9]{16,40}", tok1 or "")
            one_call = len(puts) == 1
            payload_ok = (body.get("t") == tok1
                          and isinstance(body.get("add"), list)
                          and first_id in body["add"]
                          and set(body.keys()) <= {"t", "add"})
            br.reload()
            br.sleep(1.0)
            same = br.evaluate(TOKEN) == tok1
            check(BROWSER_ROWS[0],
                  bool(token_ok) and one_call and payload_ok and same,
                  f"tok={tok1!r} puts={len(puts)} body={body} same_after_reload={same}")

            # 1 · forgetting is whole
            br.navigate(base + "/?reset")
            br.sleep(1.2)
            tok2 = br.evaluate(TOKEN)
            check(BROWSER_ROWS[1],
                  bool(tok2) and tok2 != tok1 and re.fullmatch(r"[a-z0-9]{16,40}", tok2 or ""),
                  f"tok1={tok1!r} tok2={tok2!r}")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_OFF, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
