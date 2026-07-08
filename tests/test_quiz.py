#!/usr/bin/env python3
"""EX-QUIZ / EX-PROTECT-GIFT / EX-PROTECT-RES — the work's question and its gift.

Ports the tlvphoto quiz + gift-ceremony + mark-split features into the engine, GENERALIZED:
no work id, host, or filename is hardcoded — quiz data is an instance-supplied
<content>/quiz.json, the mark text is the site host from config, the download name is a slug
of the site name, and the chip PLACEMENT + PROBABILITY are config knobs.

String/data rows read the real baked artifacts (a quiz-ON bake vs the default OFF bake).
Browser rows drive headless Chrome; Chrome absent → pinned SKIP, never a silent pass.

Run: python tests/test_quiz.py
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
QUIZ_WORK_ID = "synth-01"
# Strings that are UNIQUELY quiz answers — NOT section/place metadata ("urban" is a section name,
# so it legitimately appears in served bytes; "the urban family" only ever exists as an accept form).
ACCEPT_UNIQUE = ["the urban family"]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- two bakes
TMP_OFF = Path(tempfile.mkdtemp(prefix="synth_quiz_off_"))
build_site.OUT = TMP_OFF
build_site.build(SITE_URL)                      # quiz ships false by default

TMP_ON = Path(tempfile.mkdtemp(prefix="synth_quiz_on_"))
build_site.OUT = TMP_ON
build_site.build(SITE_URL, enable=["quiz"])     # the feature on

EXDATA_OFF = json.loads((TMP_OFF / "exhibition_data.json").read_text())
EXDATA_ON = json.loads((TMP_ON / "exhibition_data.json").read_text())
CONFIG_OFF = json.loads((TMP_OFF / "config.json").read_text())
CONFIG_ON = json.loads((TMP_ON / "config.json").read_text())
worker_on = (TMP_ON / "_worker.js").read_text(encoding="utf-8") if (TMP_ON / "_worker.js").exists() else ""

css_src = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
build_src = (ROOT / "engine" / "build.py").read_text(encoding="utf-8")

# ---------------------------------------------------------------- data rows

# 1 · EX-QUIZ-EDGE (INV-59): the verdict is judged at the edge
qa_embedded = ("QUIZ_ANSWERS" in worker_on and "__QUIZ_ANSWERS__" not in worker_on
               and QUIZ_WORK_ID in worker_on)
route_wired = '"/api/quiz"' in worker_on
norm_present = "normAnswer" in worker_on and r"\p{L}" in worker_on
quiz_fn = "async function quiz(" in worker_on
fence_present = "overQuizRate" in worker_on
ok_true = "ok: true" in worker_on
ok_false = "ok: false" in worker_on
check("EX-QUIZ-EDGE verdict judged at the edge (INV-59): normAnswer, route, answers baked, ok:true/false",
      qa_embedded and route_wired and norm_present and quiz_fn and fence_present and ok_true and ok_false,
      f"baked={qa_embedded} route={route_wired} norm={norm_present} fn={quiz_fn} "
      f"fence={fence_present} ok_true={ok_true} ok_false={ok_false}")

# 2 · EX-QUIZ-EDGE (INV-59 safety): the accept-set is NEVER a served byte
served_blob = "\n".join(
    p.read_text(errors="ignore") for p in TMP_ON.rglob("*")
    if p.is_file() and p.name != "_worker.js"
    and p.suffix in (".json", ".js", ".html", ".css", ".xml", ".txt"))
leaked = next((s for s in ACCEPT_UNIQUE if s.lower() in served_blob.lower()), None)
in_worker = all(s.lower() in worker_on.lower() for s in ACCEPT_UNIQUE)
check("EX-QUIZ-EDGE accept strings absent from every served static byte, present only in _worker.js (INV-59)",
      leaked is None and in_worker, f"leaked={leaked!r} in_worker={in_worker}")

# 3 · EX-QUIZ-EDGE (F1): the quiz's OWN attempt fence — the model bucket untouched
quiz_key = '"q:"' in worker_on
tries_const = "QUIZ_TRIES_PER_HOUR" in worker_on
# the quiz function body ONLY — bounded at the next top-level function so translate()'s api call
# (which legitimately mentions anthropic.com) is never swept into the "no model touch" check
quiz_section = (re.split(r"\n(?:async )?function ", worker_on.split("async function quiz(", 1)[1])[0]
                if "async function quiz(" in worker_on else "")
no_budget = "overBudget" not in quiz_section
no_charge = "chargeModelCall" not in quiz_section
no_api = "anthropic.com" not in quiz_section
check("EX-QUIZ-EDGE own attempt fence (q: key, own ceiling), no model/budget touch (F1)",
      quiz_key and tries_const and no_budget and no_charge and no_api,
      f"key={quiz_key} tries={tries_const} no_budget={no_budget} no_charge={no_charge} no_api={no_api}")

# 4 · EX-QUIZ (INV-60/INV-19/CS-8): flag-off is byte-identical, silence is graceful
config_quiz_off = CONFIG_OFF.get("quiz") is False
config_quiz_on = CONFIG_ON.get("quiz") is True
any_quiz_off = any(w.get("quiz") for w in EXDATA_OFF.get("works", []))
quiz_work_on = next((w for w in EXDATA_ON["works"] if str(w.get("id")) == QUIZ_WORK_ID), None)
quiz_data_on = (quiz_work_on is not None and isinstance(quiz_work_on.get("quiz"), dict)
                and "prompt" in quiz_work_on["quiz"] and "hints" in quiz_work_on["quiz"]
                and "accept" not in quiz_work_on["quiz"] and "prize" not in quiz_work_on["quiz"])
worker_off_absent = not (TMP_OFF / "_worker.js").exists()
off_no_quiz = [{k: v for k, v in w.items() if k != "quiz"} for w in EXDATA_OFF["works"]]
on_no_quiz = [{k: v for k, v in w.items() if k != "quiz"} for w in EXDATA_ON["works"]]
works_identical = off_no_quiz == on_no_quiz
check("EX-QUIZ flag-off byte-identity + no accept/prize on any public work (INV-60/INV-19/CS-8)",
      config_quiz_off and config_quiz_on and not any_quiz_off and quiz_data_on
      and worker_off_absent and works_identical,
      f"cfg_off={config_quiz_off} cfg_on={config_quiz_on} no_quiz_off={not any_quiz_off} "
      f"data_on={quiz_data_on} worker_off_absent={worker_off_absent} works_same={works_identical}")

# 5 · GENERALIZATION: placement + probability are config knobs; quiz data is instance-supplied
qcfg = CONFIG_ON.get("exhibition", {}).get("quiz", {})
placement_ok = isinstance(qcfg.get("placement"), list) and set(qcfg["placement"]) <= {"plaque", "door"}
probability_ok = isinstance(qcfg.get("probability"), (int, float)) and 0 <= qcfg["probability"] <= 1
# no hardcoded work id / host / brand in the builder's quiz path (data comes from <content>/quiz.json)
no_hardcoded_quiz = ("quiz.json" in build_src and QUIZ_WORK_ID not in build_src
                     and "tlvphoto" not in build_src.lower())
js_reads_knobs = "QUIZ_PLACE" in js_src and "QUIZ_P" in js_src and "QUIZ_WALK" in js_src
check("EX-QUIZ generalized: placement+probability are config knobs, data is instance-supplied (INV-28)",
      placement_ok and probability_ok and no_hardcoded_quiz and js_reads_knobs,
      f"placement={placement_ok} prob={probability_ok} no_hardcode={no_hardcoded_quiz} knobs={js_reads_knobs}")

# 6 · EX-QUIZ chip + card + door chip obey the house breath (EX-ARRIVE) and tongue (EX-I18N)
chip_css = ".ex-quiz-chip" in css_src
card_css = "#ex-quiz-card" in css_src
door_chip_css = ".exd-quiz" in css_src
chip_opacity0 = "ex-quiz-chip" in css_src and "opacity:0" in css_src
dtoken = "var(--d-" in css_src
quiz_ask_js = "quiz_ask" in js_src
chip_js = "ex-quiz-chip" in js_src
card_js = "ex-quiz-card" in js_src
door_chip_js = "exd-quiz" in js_src and "QUIZ_AT" in js_src
esc_js = "Escape" in js_src and "quiz" in js_src.lower()
ls_solved = "tlv.quiz." in js_src
en = (json.loads((TMP_ON / "exhibition_data.json").read_text()).get("greet") or {}).get("langs", {}).get("en", {})
quiz_ask_baked = "quiz_ask" in en
check("EX-QUIZ chip + card + door chip obey house breath (EX-ARRIVE) and tongue (EX-I18N)",
      chip_css and card_css and door_chip_css and chip_opacity0 and dtoken and quiz_ask_js
      and chip_js and card_js and door_chip_js and esc_js and ls_solved and quiz_ask_baked,
      f"chip_css={chip_css} card_css={card_css} door_css={door_chip_css} op0={chip_opacity0} "
      f"dtok={dtoken} quiz_ask_js={quiz_ask_js} chip_js={chip_js} card_js={card_js} "
      f"door_js={door_chip_js} esc={esc_js} ls={ls_solved} baked={quiz_ask_baked}")

# 7 · EX-QUIZ-PRIZE / EX-PROTECT-RES (INV-56/INV-18): prize is a marked gallery derivative
prize_in_worker = "gallery/quiz-prize" in worker_on
prize_files = list((TMP_ON / "gallery").glob("quiz-prize-*.jpg")) if (TMP_ON / "gallery").exists() else []
prize_in_bundle = len(prize_files) > 0
check("EX-QUIZ-PRIZE prize is a display-grade gallery derivative in the bundle, master never shipped (INV-18)",
      prize_in_worker and prize_in_bundle,
      f"prize_in_worker={prize_in_worker} prize_in_bundle={prize_in_bundle} files={[p.name for p in prize_files]}")

# 8 · EX-QUIZ a miss nudges (never scolds); the answer is never in the client JS
hints_indexed = "hints" in js_src and "quizMissCount" in js_src
quiet_retry = "one moment" in js_src
accept_in_client = any(s in js_src for s in ACCEPT_UNIQUE)
check("EX-QUIZ a miss shows the next public hint; network error = quiet retry; answer never in client",
      hints_indexed and quiet_retry and not accept_in_client,
      f"hints={hints_indexed} retry={quiet_retry} accept_in_client={accept_in_client}")

# 9 · EX-PROTECT-GIFT + EX-PROTECT-RES: the gift ceremony + client-side mark-split on TAKE
gift_card_js = "ex-gift-card" in js_src and "function openGift(" in js_src
gift_yes_only = "yes.onclick" in js_src and "giftDownload" in js_src  # download only on the yes
mark_split = ("function giftDownload(" in js_src and "canvas" in js_src
              and "fillText(host" in js_src and "preMarked" in js_src)
dl_from_slug = "DL_BASE" in js_src and "cfg.site_name" in js_src        # filename generalized
gift_css = "#ex-gift-card" in css_src and ".gift-inner" in css_src
# the SHOWN served image is CLEAN (tests bake without display_max ⇒ no baked host mark on served copies);
# the mark rides the TAKEN copy only (client canvas above / prize derivative)
served_gallery_unmarked = not (TMP_ON / "gallery" / "assets").glob("**/*marked*")  # no marked served asset naming
check("EX-PROTECT-GIFT gift ceremony hands over only on a yes; EX-PROTECT-RES marks the TAKEN copy client-side",
      gift_card_js and gift_yes_only and mark_split and dl_from_slug and gift_css,
      f"gift_js={gift_card_js} yes_only={gift_yes_only} mark_split={mark_split} "
      f"dl_slug={dl_from_slug} gift_css={gift_css}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-QUIZ browser: the plaque chip renders for a quizzed work; the card opens on the tempo; Esc closes",
    "EX-QUIZ browser: a wrong answer shows the next hint; a right answer opens the gift ceremony; answer never in DOM",
]

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    ver = EXDATA_ON.get("version", "")
    with serve(TMP_ON) as base:
        # row A — chip renders + card opens/closes
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('tlv-tempo','0.1')")
            br.evaluate("localStorage.setItem('tlv.exhibition', JSON.stringify({v:%s, pick:%s, shown:10}))"
                        % (json.dumps(ver), json.dumps(QUIZ_WORK_ID)))
            br.reload()
            br.sleep(1.2)
            br.evaluate("const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                        "if(f) f.scrollIntoView({behavior:'instant'})" % QUIZ_WORK_ID)
            br.sleep(0.6)
            has_chip = br.evaluate("!!(document.querySelector('#exh-cap .ex-quiz-chip'))")
            card_open = None
            closed = None
            if has_chip:
                br.click('#exh-cap .ex-quiz-chip', settle=0.5)
                card_open = br.evaluate("""(()=>{const c=document.getElementById('ex-quiz-card');
                  const s=c?getComputedStyle(c):null;
                  return {present:!!c, visible: c&&s&&s.opacity!=='0'&&s.display!=='none',
                          hasShow: c&&c.classList.contains('show')};})()""")
                br.key("Escape")
                br.sleep(0.4)
                closed = br.evaluate("(()=>{const c=document.getElementById('ex-quiz-card');"
                                     "return {hidden: !c||c.hidden||getComputedStyle(c).opacity==='0'};})()")
            check(BROWSER_ROWS[0],
                  has_chip is True and card_open is not None and card_open.get("present") is True
                  and card_open.get("visible") is True
                  and (closed is None or closed.get("hidden") is True),
                  f"chip={has_chip} card={card_open} closed={closed}")

        # row B — miss shows a hint, win opens the gift ceremony (fetch stubbed)
        with Browser(width=1280, height=900) as br:
            br.inject("""
            window.__qc=0;
            (function(){const _f=window.fetch;window.fetch=function(u,o){
              if(String(u).indexOf('/api/quiz')>=0){window.__qc++;
                const body=JSON.stringify(window.__qc===1?{ok:false}:{ok:true,prize:'gallery/quiz-prize-001.jpg'});
                return Promise.resolve(new Response(body,{status:200,headers:{'Content-Type':'application/json'}}));}
              return _f.apply(this,arguments);};})();
            """)
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('tlv-tempo','0.1')")
            br.evaluate("localStorage.setItem('tlv.exhibition', JSON.stringify({v:%s, pick:%s, shown:10}))"
                        % (json.dumps(ver), json.dumps(QUIZ_WORK_ID)))
            br.reload()
            br.sleep(1.2)
            br.evaluate("const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                        "if(f) f.scrollIntoView({behavior:'instant'})" % QUIZ_WORK_ID)
            br.sleep(0.6)
            after_miss = None
            after_win = None
            try:
                if not br.evaluate("!!(document.querySelector('#exh-cap .ex-quiz-chip'))"):
                    raise RuntimeError("chip absent")
                br.click('#exh-cap .ex-quiz-chip', settle=0.6)
                br.evaluate("(()=>{var i=document.querySelector('#ex-quiz-card .quiz-input');"
                            "if(i)i.value='nope';})()")
                br.evaluate("(()=>{var f=document.querySelector('#ex-quiz-card .quiz-form');"
                            "if(f)f.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));})()")
                br.sleep(0.8)
                after_miss = br.evaluate("(()=>{var o=document.querySelector('#ex-quiz-card .quiz-out');"
                                         "var dom=document.body.innerText.indexOf('the urban family')>=0;"
                                         "return {outText:o?o.textContent.trim():null, acceptInDom:dom};})()")
                br.evaluate("(()=>{var i=document.querySelector('#ex-quiz-card .quiz-input');"
                            "if(i)i.value='urban';})()")
                br.evaluate("(()=>{var f=document.querySelector('#ex-quiz-card .quiz-form');"
                            "if(f)f.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true}));})()")
                br.sleep(0.9)
                after_win = br.evaluate("(()=>{var g=document.getElementById('ex-gift-card');"
                                        "if(!g||g.hidden)return {shown:false};"
                                        "var t=g.querySelector('.gift-thumb'),y=g.querySelector('.gift-yes');"
                                        "return {shown:!!(t&&t.getAttribute('src'))&&!!y};})()")
            except Exception:
                import traceback
                traceback.print_exc()
            hint_shown = after_miss is not None and after_miss.get("outText") not in (None, "")
            accept_not_in_dom = after_miss is None or not after_miss.get("acceptInDom", False)
            prize_shown = after_win is not None and after_win.get("shown")
            check(BROWSER_ROWS[1],
                  hint_shown and accept_not_in_dom and prize_shown,
                  f"hint={hint_shown} accept_not_in_dom={accept_not_in_dom} prize={prize_shown} "
                  f"miss={after_miss} win={after_win}")

shutil.rmtree(TMP_OFF, ignore_errors=True)
shutil.rmtree(TMP_ON, ignore_errors=True)

# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
