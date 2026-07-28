#!/usr/bin/env python3
"""The corner mark — the guest chooses the tongue (EX-LANG / INV-45) — adapted for
exhibition-engine synthetic fixture. The door carries a quiet corner mark; a tap opens a FEW,
geo-relevant tongues (EX-LANG-GEO / INV-45): English always and first, then the arriving country's
languages (Cloudflare /api/geo, cfg.lang_geo), then the guest's own browser locale — deduped,
capped, NOT all seven baked tongues. An offered tongue need not be baked; a pick re-speaks the
threshold at once (RTL turns the face), persists, and rides the ONE string layer; `?reset` returns
the browser's tongue. Here the arriving country is stubbed to IL (he/ru/ar) with a Polish browser.
Chrome absent → pinned expected SKIPs. Run: python tests/test_lang.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_lang_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_i18n"])

BROWSER_ROWS = [
    "EX-LANG-GEO the mark stands on the threshold, narrowed to the arriving country (IL ⇒ en first + "
    "he/ru/ar + the PL browser; an unbaked geo tongue offered; the baked seven NOT all present; ≥44px)",
    "EX-LANG a pick re-speaks and persists (Hebrew: ask+dir flip at once; survives reload)",
    "EX-LANG the outsider pick rides the one layer (PL in the list; instant baked switch; stub strings back)",
    "EX-LANG reset returns the browser's tongue",
    "EX-LANG the open menu belongs to the mark's family — same width, flush edges, the same curve",
    "EX-LANG/INV-102 a tongue landing while a work is in view speaks the wall label again — the polite "
    "region carries the new tongue's caption, never the tongue the label has left",
]

# ONE injected stub for BOTH edge routes the corner touches: /api/geo → the arriving country (IL),
# so the corner narrows to he/ru/ar; /api/i18n → the outsider-tongue strings, so a PL pick re-speaks.
STUB = """
window.__i18nCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/geo')>=0){
    return Promise.resolve(new Response(JSON.stringify({c:'IL'}),{status:200}));
  }
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

# a tongue whose strings are HELD at the edge until the test lets them land — the guest is already
# walking by then, which is the only way a tongue arrives mid-walk (the corner mark lives at the door)
STUB_HELD = """
window.__i18nCalls=0;
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/geo')>=0){
    return Promise.resolve(new Response(JSON.stringify({c:'IL'}),{status:200}));
  }
  if(String(u).indexOf('/api/i18n')>=0){
    window.__i18nCalls++;
    return new Promise(function(res){
      window.__langLand=function(titles){
        res(new Response(JSON.stringify({
          dir:'ltr',ask:'HELD-ASK',exit:'HELD-EXIT',more:'HELD {n}',q_more:'HELD?',q_spent:'HELD.',
          untitled:'HELD-UNTITLED',
          greet:{night:['HELD-G'],morning:['HELD-G'],day:['HELD-G'],evening:['HELD-G']},
          titles:titles}),{status:200,headers:{'Content-Type':'application/json'}}));
      };
    });
  }
  return _f.apply(this,arguments);};})();
"""
IN_VIEW = ("(()=>{const fs=Array.from(document.querySelectorAll('.exh-frame'));"
           "const f=fs.find(x=>{const r=x.getBoundingClientRect();"
           "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});"
           "const t=document.querySelector('#exh-cap .title');"
           "return JSON.stringify({id:f?f.dataset.id:'',"
           "title:t?t.textContent:'',untitled:!!(t&&t.classList.contains('untitled')),"
           "shown:!!document.querySelector('#exh-cap.show')});})()")
REGION = "(()=>{const e=document.getElementById('ex-live-cap');return e?e.textContent:'';})()"


def poll(br, expr, timeout=8.0, step=0.05):
    """Poll a JS expression until truthy (or the deadline) — no fixed-sleep races."""
    import time
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    return val

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
            geo_langs = {"he", "ru", "ar"}
            check(BROWSER_ROWS[0],
                  bool(geo) and geo["vis"] and geo["w"] >= 44 and geo["h"] >= 44
                  and bool(langs) and langs[0] == "en"          # English first
                  and geo_langs <= set(langs)                   # the arriving country's tongues
                  and "ar" in langs                             # an UNBAKED geo tongue is offered
                  and "pl" in langs                             # the guest's own browser tongue
                  and not seven <= set(langs),                  # NOT all seven — the corner narrowed
                  f"geo={geo} list={langs}")

            # 2 · the outsider layer: instant baked switch, stub strings back on PL
            br.click('#exd-lang .exl-item[data-lang="ru"]', settle=0.5)
            ru_now = br.evaluate(ASK) == "что ближе сейчас?"
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
            he_now = (br.evaluate(ASK) == "מה קרוב אליך עכשיו?"
                      and br.evaluate(DIR) == "rtl")
            br.reload()
            br.sleep(1.2)
            he_kept = (br.evaluate(ASK) == "מה קרוב אליך עכשיו?"
                       and br.evaluate(DIR) == "rtl"
                       and br.evaluate("localStorage.getItem('ex.lang')") == "he")
            check(BROWSER_ROWS[1], he_now and he_kept,
                  f"at_once={he_now} kept={he_kept} ask={br.evaluate(ASK)!r}")

            # 4 · the open menu is the mark's own shape (his find 2026-07-27: a round chip over a
            # squarer, wider menu that hung to one side). Measured, never read off the source.
            br.navigate(base + "/")
            br.sleep(1.0)
            br.click("#exd-lang .exl-cur", settle=0.5)
            shape = br.evaluate(
                "(()=>{const c=document.querySelector('#exd-lang .exl-cur');"
                "const l=document.querySelector('#exd-lang .exl-list');"
                "if(!c||!l||l.hidden)return null;"
                "const rc=c.getBoundingClientRect(),rl=l.getBoundingClientRect();"
                "const sc=getComputedStyle(c),sl=getComputedStyle(l);"
                "return {cw:Math.round(rc.width),lw:Math.round(rl.width),"
                "cright:Math.round(rc.right),lright:Math.round(rl.right),"
                "cleft:Math.round(rc.left),lleft:Math.round(rl.left),"
                "crad:parseFloat(sc.borderTopLeftRadius),lrad:parseFloat(sl.borderTopLeftRadius)};})()")
            check(BROWSER_ROWS[4],
                  bool(shape)
                  and shape["lw"] == shape["cw"]                       # one width, so no overhang
                  and abs(shape["lright"] - shape["cright"]) <= 1      # flush on both sides
                  and abs(shape["lleft"] - shape["cleft"]) <= 1
                  and shape["lrad"] >= shape["cw"] / 2 - 1,            # the chip's own curve, not a squarer corner
                  f"shape={shape}")

            # 3 · reset returns the browser's tongue
            br.navigate(base + "/?reset")
            br.sleep(1.2)
            lang_key = br.evaluate("localStorage.getItem('ex.lang')")
            check(BROWSER_ROWS[3],
                  lang_key is None and br.evaluate(ASK) == "что ближе сейчас?",
                  f"lang_key={lang_key!r} ask={br.evaluate(ASK)!r}")

        # INV-102 — a tongue landing mid-walk speaks the wall label again. The strings are held at the
        # edge while the guest crosses the threshold, then let land: the label's title changes under
        # their eye, so the polite region must carry the new tongue too (EX-HANG).
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_HELD)
            br.pretend("pl-PL", 15)                    # a locale OUTSIDE the baked seven
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo','0.4')")
            br.reload()
            poll(br, "document.querySelectorAll('.exd-window').length>0")
            br.click(".exd-window:nth-child(1)", settle=0.05)
            poll(br, "!!document.querySelector('#exh-cap.show')")
            # The door picks the works, so whether the one in view carries a title is not the
            # test's to choose: BOTH faces of the label re-speak, and the expected word is read off
            # the work in view rather than hunted for (a scroll-until-titled search was this row's
            # own flake on 2026-07-28).
            view = json.loads(poll(br, IN_VIEW) or "null") or {}
            titled = bool(view.get("id")) and not view.get("untitled")
            want = "TITLE-HELD" if titled else "HELD-UNTITLED"
            titles = {view["id"]: "TITLE-HELD"} if titled else {}
            before = br.evaluate(REGION) or ""
            landed = poll(br, "!!window.__langLand")   # the ask leaves 400 ms after arrival
            if not landed or not view.get("id"):
                check(BROWSER_ROWS[5], False,
                      f"the tongue never travelled or no work stood in view: "
                      f"held={landed} view={view}")
            else:
                br.evaluate("window.__langLand(%s)" % json.dumps(titles))
                poll(br, "(document.querySelector('#exh-cap .title')||{}).textContent===%s"
                         % json.dumps(want))
                after = poll(br, "(()=>{const e=document.getElementById('ex-live-cap');"
                                 "return (e&&e.textContent.indexOf(%s)>=0)?e.textContent:'';})()"
                                 % json.dumps(want))
                label = json.loads(br.evaluate(IN_VIEW) or "null") or {}
                check(BROWSER_ROWS[5],
                      bool(after) and want in (after or "")
                      and label.get("title") == want
                      and want not in before,
                      f"want={want!r} titled={titled} region before={before[:80]!r} "
                      f"after={(after or '')[:80]!r} label={label}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
