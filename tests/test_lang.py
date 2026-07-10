#!/usr/bin/env python3
"""The corner mark — the guest chooses the tongue (EX-LANG / INV-45) — adapted for
exhibition-engine synthetic fixture. The door carries a quiet corner mark; a tap opens
the seven (+ the guest's own outsider tongue when the any-locale layer is on); a pick
re-speaks the threshold at once (RTL turns the face), persists, and rides the ONE string
layer; `?reset` returns the browser's tongue.
Chrome absent → pinned expected SKIPs. Run: python tests/test_lang.py
"""
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


TMP = Path(tempfile.mkdtemp(prefix="synth_lang_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_i18n"])

BROWSER_ROWS = [
    "EX-LANG the mark stands on the threshold (cold + re-opened; the list = seven + the outsider; ≥44px)",
    "EX-LANG a pick re-speaks and persists (Hebrew: ask+dir flip at once; survives reload)",
    "EX-LANG the outsider pick rides the one layer (PL in the list; instant baked switch; stub strings back)",
    "EX-LANG reset returns the browser's tongue",
]

STUB = """
window.__i18nCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/i18n')>=0){
    window.__i18nCalls++;
    return Promise.resolve(new Response(JSON.stringify({
      dir:'ltr',ask:'STUB-ASK',exit:'STUB-EXIT',more:'STUB {n}',q_more:'STUB?',q_spent:'STUB.',
      share_label:'stub',share_copied:'STUB-C',
      greet:{night:['SG'],morning:['SG'],day:['SG'],evening:['SG']},titles:{}}),{status:200}));
  }
  return _f.apply(this,arguments);};})();
"""
ASK = "document.querySelector('.exd-ask').textContent"
DIR = "document.getElementById('ex-door').getAttribute('dir')"
LIST = "Array.from(document.querySelectorAll('#exd-lang .exl-item')).map(b=>b.dataset.lang)"

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(STUB)
            br.pretend("pl-PL", 15)                    # an outsider tongue
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(1.6)
            geo = br.evaluate(
                "(()=>{const m=document.getElementById('exd-lang');if(!m)return null;"
                "const r=m.getBoundingClientRect();const s=getComputedStyle(m);"
                "return {w:r.width,h:r.height,vis:s.display!=='none'&&+s.opacity>0.05,"
                "mark:m.querySelector('.exl-cur').textContent.trim()};})()")
            br.click("#exd-lang .exl-cur", settle=0.4)
            langs = br.evaluate(LIST) or []
            seven = {"ru", "en", "he", "de", "fr", "es", "uk"}
            check(BROWSER_ROWS[0],
                  bool(geo) and geo["vis"] and geo["w"] >= 44 and geo["h"] >= 44
                  and seven <= set(langs) and "pl" in langs,
                  f"geo={geo} list={langs}")

            # 2 · the outsider layer: instant baked switch, stub strings back on PL
            br.click('#exd-lang .exl-item[data-lang="ru"]', settle=0.5)
            ru_now = br.evaluate(ASK) == "что ближе сейчас"
            br.click("#exd-lang .exl-cur", settle=0.4)
            br.click('#exd-lang .exl-item[data-lang="pl"]', settle=0.9)
            pl_now = br.evaluate(ASK) == "STUB-ASK"
            check(BROWSER_ROWS[2], ru_now and pl_now,
                  f"ru_switch={ru_now} pl_stub={pl_now} calls={br.evaluate('window.__i18nCalls')}")

        with Browser(width=1280, height=900) as br:
            br.inject(STUB)
            br.pretend("ru-RU", 15)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(1.2)
            br.click("#exd-lang .exl-cur", settle=0.4)
            br.click('#exd-lang .exl-item[data-lang="he"]', settle=0.6)
            he_now = (br.evaluate(ASK) == "מה קרוב אליך עכשיו"
                      and br.evaluate(DIR) == "rtl")
            br.reload()
            br.sleep(1.2)
            he_kept = (br.evaluate(ASK) == "מה קרוב אליך עכשיו"
                       and br.evaluate(DIR) == "rtl"
                       and br.evaluate("localStorage.getItem('ex.lang')") == "he")
            check(BROWSER_ROWS[1], he_now and he_kept,
                  f"at_once={he_now} kept={he_kept} ask={br.evaluate(ASK)!r}")

            # 3 · reset returns the browser's tongue
            br.navigate(base + "/?reset")
            br.sleep(1.2)
            lang_key = br.evaluate("localStorage.getItem('ex.lang')")
            check(BROWSER_ROWS[3],
                  lang_key is None and br.evaluate(ASK) == "что ближе сейчас",
                  f"lang_key={lang_key!r} ask={br.evaluate(ASK)!r}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
