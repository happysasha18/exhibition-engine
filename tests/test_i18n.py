#!/usr/bin/env python3
"""Any-locale strings (EX-I18N / INV-42) — adapted for exhibition-engine synthetic fixture.
The worker is STUBBED — the suite never talks to Anthropic.
If the engine does not yet produce _worker.js / i18n_source.json, the contract rows
FAIL and that gap is recorded in E3_REPORT.md (do not weaken the assertions).
Chrome absent → pinned expected SKIPs. Run: python tests/test_i18n.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_i18n_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_i18n"])

TMP_OFF = Path(tempfile.mkdtemp(prefix="synth_i18n_off_"))
build_site.OUT = TMP_OFF
build_site.build(SITE_URL)          # shipped default: flag false

# ---------------------------------------------------------------- contract rows (string+function)
_worker_path = TMP / "_worker.js"
_routes_path = TMP / "_routes.json"
_src_path = TMP / "i18n_source.json"

_worker_exists = _worker_path.exists()
_routes_exists = _routes_path.exists()
_src_exists = _src_path.exists()

worker_src = _worker_path.read_text(encoding="utf-8") if _worker_exists else ""
routes = json.loads(_routes_path.read_text(encoding="utf-8")) if _routes_exists else {}
src = json.loads(_src_path.read_text(encoding="utf-8")) if _src_exists else {}
vals = json.dumps(src, ensure_ascii=False)

kv_pos = worker_src.find("TLV_I18N.get")
model_pos = worker_src.find("api.anthropic.com")

check("EX-I18N worker contract: routes only /api, sane-tag guard, cache before model, strict shape",
      _worker_exists and _routes_exists
      and routes.get("include") == ["/api/*"]
      and "^[a-z]{2,3}(-[a-z0-9]{2,8})?$" in worker_src.lower()
      and 0 < kv_pos < model_pos
      and '"dir"' in worker_src,
      f"worker_exists={_worker_exists} routes={routes} kv@{kv_pos} model@{model_pos}")
check("EX-I18N brand + © never enter the translatable set",
      _src_exists
      and "SYNTH EXHIBITION" not in vals and "©" not in vals and src.get("version"),
      "brand or signature leaked into i18n_source.json (or file missing)")
check("EX-I18N flagged-off bundle ships NO worker",
      not (TMP_OFF / "_worker.js").exists() and not (TMP_OFF / "_routes.json").exists(),
      "worker artifacts present despite ai_i18n:false")

BROWSER_ROWS = [
    "EX-I18N an outside locale re-speaks quietly (fallback instant → stub strings; no re-fetch on return; baked-7 never fetch)",
    "EX-I18N a dead worker changes nothing (fallback stands, no error face)",
    "EX-I18N the flag is the law (flag off ⇒ no /api fetch for any locale)",
]

STUB_OK = """
window.__i18nCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/i18n')>=0){
    window.__i18nCalls++;
    return Promise.resolve(new Response(JSON.stringify({
      dir:'ltr',ask:'STUB-ASK',exit:'STUB-EXIT',more:'STUB {n}',q_more:'STUB?',q_spent:'STUB.',
      share_label:'stub-label',share_copied:'STUB-COPIED',
      greet:{night:['STUB-G'],morning:['STUB-G'],day:['STUB-G'],evening:['STUB-G']},
      titles:{}}),{status:200,headers:{'Content-Type':'application/json'}}));
  }
  return _f.apply(this,arguments);};})();
"""
STUB_DEAD = """
window.__i18nCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/i18n')>=0){window.__i18nCalls++;return Promise.reject(new Error('down'));}
  return _f.apply(this,arguments);};})();
"""
ASK = "document.querySelector('.exd-ask').textContent"

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_OK)
            br.pretend("pl-PL", 15)                    # a locale OUTSIDE the baked seven
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.reload()
            br.sleep(1.6)
            spoke = br.evaluate(ASK) == "STUB-ASK"
            calls1 = br.evaluate("window.__i18nCalls")
            br.reload()                                # the browser copy serves — no re-fetch
            br.sleep(1.4)
            calls2 = br.evaluate("window.__i18nCalls")
            spoke2 = br.evaluate(ASK) == "STUB-ASK"
            check(BROWSER_ROWS[0],
                  spoke and calls1 == 1 and calls2 == 0 and spoke2,
                  f"ask={br.evaluate(ASK)!r} calls first={calls1} reload={calls2} "
                  "(the counter is per-document: 0 on reload = the browser copy served)")
        with Browser(width=1280, height=900) as br:    # baked-7 visitor never fetches
            br.inject(STUB_OK)
            br.pretend("ru-RU", 15)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear()")
            br.reload()
            br.sleep(1.4)
            ru_clean = (br.evaluate("window.__i18nCalls") == 0
                        and br.evaluate(ASK) == "что ближе сейчас?")
            check("EX-I18N baked-seven visitors never touch the worker", ru_clean,
                  f"calls={br.evaluate('window.__i18nCalls')} ask={br.evaluate(ASK)!r}")
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_DEAD)
            br.pretend("pl-PL", 15)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear()")
            br.reload()
            br.sleep(1.6)
            check(BROWSER_ROWS[1],
                  br.evaluate(ASK) == "what feels closer now?"
                  and br.evaluate("document.querySelectorAll('.exd-window').length") > 0
                  and br.evaluate("1+1") == 2,
                  f"ask={br.evaluate(ASK)!r}")
    with serve(TMP_OFF) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_OK)
            br.pretend("pl-PL", 15)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear()")
            br.reload()
            br.sleep(1.6)
            check(BROWSER_ROWS[2],
                  br.evaluate("window.__i18nCalls") == 0
                  and br.evaluate(ASK) == "what feels closer now?",
                  f"calls={br.evaluate('window.__i18nCalls')} ask={br.evaluate(ASK)!r}")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_OFF, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
