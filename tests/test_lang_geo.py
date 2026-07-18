#!/usr/bin/env python3
"""The corner narrows to the arriving country (EX-LANG-GEO / INV-45 · INV-1) — adapted for the
exhibition-engine synthetic fixture.

The language corner mark no longer offers ALL baked tongues. It offers English (always, first) +
the languages of the visitor's ARRIVING COUNTRY (Cloudflare geo, cfg.lang_geo.country_langs) + the
guest's own browser locale — deduped, English-first, capped. An offered tongue need NOT be baked:
ai_i18n's edge-translate layer speaks an outsider on pick. The country is used ONLY to pick chips —
it never rides a beat and never reaches GA (INV-1).

Three levels, each isolated:
  1. the pure narrowing law — extracted from the client fragment and run in node (no Chrome)
  2. the /api/geo worker contract — asserted on the BUILT _worker.js (no Chrome)
  3. the end-to-end corner — a stubbed /api/geo drives the real client in headless Chrome

Chrome absent → the browser rows become pinned expected SKIPs; the node + worker rows always run.
Run: python tests/test_lang_geo.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
import build as _engine            # noqa: E402 — engine/build.py (on path via engine_build)
import assemble_client             # noqa: E402 — engine/assemble_client.py
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
FRAGMENT = ROOT / "engine" / "client" / "18-i18n-memory-lang.js"
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- 1 · the pure narrowing law (node)
# The client carries the narrowing as one pure function between named markers (the codebase's own
# /*__ __*/ marker idiom). We slice it out and exercise it in node, so the LAW is covered
# deterministically without a browser: given a country, the map, the browser locale, and the cap →
# ordered, deduped codes, English first, geo langs next, browser locale last, overflow off the END.
def extract_narrow(src):
    m = re.search(r"/\*\s*__EX_LANG_GEO_NARROW__\s*\*/(.*?)/\*\s*__/EX_LANG_GEO_NARROW__\s*\*/",
                  src, re.S)
    return m.group(1).strip() if m else ""


NARROW_JS = extract_narrow(FRAGMENT.read_text(encoding="utf-8"))

# (name, country, country_langs, browser, cap, expected)
CASES = [
    ("EX-LANG-GEO narrowing: English first + the arriving country's tongues (IL)",
     "IL", {"IL": ["he", "ru", "ar"]}, "en", 4, ["en", "he", "ru", "ar"]),
    ("EX-LANG-GEO narrowing: an unknown country falls to [en, browser]",
     "ZZ", {"IL": ["he", "ru", "ar"]}, "fr", 4, ["en", "fr"]),
    ("EX-LANG-GEO narrowing: the cap bounds the chips, overflow drops from the END",
     "IL", {"IL": ["he", "ru", "ar"]}, "fr", 3, ["en", "he", "ru"]),
    ("EX-LANG-GEO narrowing: browser locale equal to a geo lang is not duplicated",
     "IL", {"IL": ["he", "ru", "ar"]}, "ru", 4, ["en", "he", "ru", "ar"]),
    ("EX-LANG-GEO narrowing: browser locale equal to English is not duplicated",
     "DE", {"DE": ["de"]}, "en", 4, ["en", "de"]),
    ("EX-LANG-GEO narrowing: English is the client's, never trusted from the map (US:[en])",
     "US", {"US": ["en"]}, "es", 4, ["en", "es"]),
    ("EX-LANG-GEO narrowing: the cap defaults to 4 when absent",
     "IL", {"IL": ["he", "ru", "ar", "fa", "tr"]}, "en", None, ["en", "he", "ru", "ar"]),
    ("EX-LANG-GEO narrowing: first paint (no country yet) is [en, browser]",
     "", {"IL": ["he"]}, "fr", 4, ["en", "fr"]),
    ("EX-LANG-GEO narrowing: no country and an English browser is just [en]",
     "", {"IL": ["he"]}, "en", 4, ["en"]),
]

if not NARROW_JS:
    for c in CASES:
        check(c[0], False, "narrowLangCodes markers not found in the client fragment")
    check("EX-LANG-GEO narrowing: English is always present and first", False,
          "narrowLangCodes markers not found in the client fragment")
else:
    payload = [{"country": c[1], "map": c[2], "browser": c[3], "cap": c[4]} for c in CASES]
    runner = (NARROW_JS + "\nconst CS=" + json.dumps(payload) + ";\n"
              "console.log(JSON.stringify(CS.map(c=>"
              "narrowLangCodes(c.country,c.map,c.browser,c.cap))));\n")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(runner)
        runner_path = fh.name
    proc = subprocess.run(["node", runner_path], capture_output=True, text=True)
    Path(runner_path).unlink(missing_ok=True)
    if proc.returncode != 0:
        for c in CASES:
            check(c[0], False, "node error: " + proc.stderr.strip()[:200])
        check("EX-LANG-GEO narrowing: English is always present and first", False,
              "node error: " + proc.stderr.strip()[:200])
    else:
        got = json.loads(proc.stdout.strip())
        for c, out in zip(CASES, got):
            check(c[0], out == c[5], f"got={out} want={c[5]}")
        # a standing property over EVERY case: English present and index 0 (INV: en always, first)
        en_first = all(out and out[0] == "en" for out in got)
        check("EX-LANG-GEO narrowing: English is always present and first", en_first,
              f"first-codes={[o[0] if o else None for o in got]}")

# ------------------------------------------------------------ 2 · the /api/geo worker contract (str)
TMP_W = Path(tempfile.mkdtemp(prefix="synth_geo_worker_"))
build_site.OUT = TMP_W
build_site.build(SITE_URL, enable=["ai_i18n"])
worker_src = (TMP_W / "_worker.js").read_text(encoding="utf-8") if (TMP_W / "_worker.js").exists() else ""

geo_dispatch = worker_src.find('=== "/api/geo"')
i18n_gate = worker_src.find('!== "/api/i18n"')
check("EX-LANG-GEO worker: /api/geo returns {c:CC} from request.cf.country + the cf-ipcountry "
      "fallback, no-store, dispatched BEFORE the /api/i18n 404 gate",
      bool(worker_src)
      and "/api/geo" in worker_src
      and "req.cf" in worker_src and "cf.country" in worker_src
      and "cf-ipcountry" in worker_src
      and "no-store" in worker_src
      and 0 <= geo_dispatch < i18n_gate,
      f"geo@{geo_dispatch} i18nGate@{i18n_gate} no_store={'no-store' in worker_src}")
shutil.rmtree(TMP_W, ignore_errors=True)

# ---------------------------------------------------------------- 3 · the end-to-end corner (Chrome)
BROWSER_ROWS = [
    "EX-LANG-GEO a known country narrows the corner (IL ⇒ en+he+ru+ar+fr; en first; the baked "
    "seven are NOT all offered)",
    "EX-LANG-GEO a failed geo never touches the box (the corner stands at [en, browser])",
]

STUB_GEO_OK = """
window.__geoCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/geo')>=0){window.__geoCalls++;
    return Promise.resolve(new Response(JSON.stringify({c:'IL'}),
      {status:200,headers:{'Content-Type':'application/json'}}));}
  return _f.apply(this,arguments);};})();
"""
STUB_GEO_DEAD = """
window.__geoCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/geo')>=0){window.__geoCalls++;return Promise.reject(new Error('down'));}
  return _f.apply(this,arguments);};})();
"""
LIST = "Array.from(document.querySelectorAll('#exd-lang .exl-item')).map(b=>b.dataset.lang)"

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    TMP = Path(tempfile.mkdtemp(prefix="synth_geo_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL, enable=["ai_i18n"])
    # The served client is the assembled + namespaced fragments — reproduce it into THIS temp bake so
    # the browser exercises the real fragment under edit (the committed exhibition.js is the lead's to
    # reassemble; this never touches it). Same road build takes: assemble → apply the namespace.
    assembled = _engine.apply_namespace(assemble_client.assemble(), _engine._NAMESPACE)
    (TMP / "exhibition.js").write_text(assembled, encoding="utf-8")
    # The owner's lang_geo map — patched into THIS bake's config only (config.json source is untouched).
    cfg_path = TMP / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["lang_geo"] = {"cap": 5, "country_langs": {"IL": ["he", "ru", "ar"], "DE": ["de"]}}
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_GEO_OK)
            br.pretend("fr-FR", 15)                     # an outsider browser locale, not baked
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(1.8)
            langs = br.evaluate(LIST) or []
            baked_seven = {"ru", "en", "he", "de", "fr", "es", "uk"}
            geo_langs = {"he", "ru", "ar"}
            narrowed = (bool(langs) and langs[0] == "en"                       # English first
                        and geo_langs <= set(langs)                            # the country's tongues
                        and "fr" in langs                                      # the guest's own tongue
                        and "ar" in langs                                      # an UNBAKED geo tongue is offered
                        and not baked_seven <= set(langs))                     # NOT all seven — it narrowed
            check(BROWSER_ROWS[0], narrowed, f"list={langs} geoCalls={br.evaluate('window.__geoCalls')}")

        with Browser(width=1280, height=900) as br:
            br.inject(STUB_GEO_DEAD)
            br.pretend("fr-FR", 15)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload()
            br.sleep(1.8)
            langs = br.evaluate(LIST) or []
            stood = (langs == ["en", "fr"]                                     # exactly [en, browser]
                     and br.evaluate("window.__geoCalls") >= 1                 # geo WAS asked
                     and br.evaluate("1+1") == 2)                              # no error face
            check(BROWSER_ROWS[1], stood, f"list={langs} geoCalls={br.evaluate('window.__geoCalls')}")

    shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
