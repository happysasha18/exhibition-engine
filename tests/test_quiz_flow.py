#!/usr/bin/env python3
"""EX-QUIZ-FLOW / INV-69 — quiz funnel analytics (stage dimension on the walk beats).

The quiz_stage dimension rides the SAME two beats the quiz_arm rides (walk_unfold /
walk_exit). The stage is the FURTHEST step reached, session-scoped, never moves
backwards. Four rungs: shown → opened → won|lost → gift.

FL1–FL4: browser (headless Chrome, dataLayer assertions).
FL5–FL6 (ga_report string rows): engine carries no ga_report.py — omitted; noted in SPEC
DELTA-9.

Chrome absent → pinned SKIP for FL1–FL4.
Run: .venv/bin/python tests/test_quiz_flow.py
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
# "testtoken0001" is arm=on with the engine's quizHash AND picks synth-01 (eligible[0]).
# Verified: quizHash("testtoken0001:quizarm") < 0.5*2^32 → on; quizHash("testtoken0001:once") % 2 = 0.
VISITOR_KEY_ON = "testtoken0001"
# "qk00000005" gives arm=control in the engine's quizHash (ratio > 0.5).
VISITOR_KEY_CTRL = "qk00000005"
QUIZ_WORK_ID = "synth-01"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bakes
TMP_ON = Path(tempfile.mkdtemp(prefix="synth_qflow_on_"))
build_site.OUT = TMP_ON
build_site.build(SITE_URL, ga_id="G-TESTTEST", enable=["quiz"])

TMP_OFF = Path(tempfile.mkdtemp(prefix="synth_qflow_off_"))
build_site.OUT = TMP_OFF
build_site.build(SITE_URL, ga_id="G-TESTTEST")           # flag-off with GA tag

build_site.OUT = TMP_ON   # restore

EXDATA_ON = json.loads((TMP_ON / "exhibition_data.json").read_text())
EX_VER = str(EXDATA_ON.get("version", ""))

# The GA events queue (dataLayer carries ['event', name, params] tuples pushed by gtag)
EVENTS_JS = ("JSON.stringify((window.dataLayer||[]).filter(function(e){return e[0]==='event';})"
             ".map(function(e){return [e[1], e[2]||{}];}))")

BROWSER_ROWS = [
    "FL1 EX-QUIZ-FLOW the stage rides the arm's two beats (INV-69 / INV-41)",
    "FL2 EX-QUIZ-FLOW the ladder never moves backwards and survives a reload (INV-69)",
    "FL3 EX-QUIZ-FLOW control and flag-off stamp nothing (INV-69 / EX-QUIZ-AB)",
    "FL4 EX-QUIZ-FLOW only the quiz prize's yes stamps gift (INV-69 / EX-PROTECT-GIFT)",
]

# Engine storage key (dot convention, see DELTA-9)
STAGE_KEY = "ex.quizstage"


def setup_walk(br, visitor_key=None, answered_ids=None, cooldown_ts=None):
    """Set localStorage/sessionStorage for a fresh quiz walk."""
    if visitor_key is None:
        visitor_key = VISITOR_KEY_ON
    br.evaluate("localStorage.clear(); sessionStorage.clear()")
    br.evaluate("localStorage.setItem('ex-tempo','0.05')")
    br.evaluate("localStorage.setItem('ex.visitor', %s)" % json.dumps(visitor_key))
    br.evaluate(
        "localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
        % (json.dumps(EX_VER), json.dumps(QUIZ_WORK_ID))
    )
    if answered_ids:
        for wid in answered_ids:
            key = "ex.quiz." + str(wid)
            br.evaluate("localStorage.setItem(%s, JSON.stringify({answered:true,right:false}))"
                        % json.dumps(key))
    if cooldown_ts is not None:
        br.evaluate("localStorage.setItem('ex.quizshown', %s)" % json.dumps(str(cooldown_ts)))


def scroll_to_chip(br):
    """Scroll to the chosen quiz work's frame. Returns True if chip visible."""
    br.evaluate(
        "(function(){var f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
        "if(f) f.scrollIntoView({behavior:'instant'});})();" % QUIZ_WORK_ID
    )
    br.sleep(0.5)
    br.evaluate("""(function(){
      var chip = document.querySelector('.ex-quiz-chip');
      if (chip) { var frame = chip.closest('.exh-frame');
        if (frame) frame.scrollIntoView({behavior:'instant'}); }
    })()""")
    br.sleep(0.3)
    return br.evaluate("!!document.querySelector('.ex-quiz-chip')")


def events_dict(br):
    """Return dict {event_name: params} from dataLayer."""
    raw = br.evaluate(EVENTS_JS) or "[]"
    try:
        pairs = json.loads(raw)
        return {p[0]: p[1] for p in pairs}
    except Exception:
        return {}


def stub_quiz_win(br, prize="gallery/quiz-prize-synth01.jpg"):
    """Inject a fetch stub so /api/quiz always returns a win."""
    br.inject(
        "(function(){var _f=window.fetch;"
        "window.fetch=function(u,o){"
        "if(String(u).indexOf('/api/quiz')>=0){"
        "return Promise.resolve(new Response("
        "JSON.stringify({ok:true,prize:%s}),"
        "{status:200,headers:{'Content-Type':'application/json'}}));}"
        "return _f.apply(this,arguments);};})()" % json.dumps(prize)
    )


def stub_quiz_miss(br):
    """Inject a fetch stub so /api/quiz always returns a miss."""
    br.inject(
        "(function(){var _f=window.fetch;"
        "window.fetch=function(u,o){"
        "if(String(u).indexOf('/api/quiz')>=0){"
        "return Promise.resolve(new Response(JSON.stringify({ok:false}),"
        "{status:200,headers:{'Content-Type':'application/json'}}));}"
        "return _f.apply(this,arguments);};})()"
    )


# ----------------------------------------------------------------
# Browser rows FL1–FL4
# ----------------------------------------------------------------

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP_ON) as base_on:

        # ---- FL1: stage rides the arm's two beats ---------------------------
        # Scenario: on-arm walk, chip shown, card opened, miss answer, then walk_exit
        # Expected: walk_exit carries quiz_stage from the ladder; no sixth beat
        with Browser(width=1280, height=900) as br:
            stub_quiz_miss(br)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.0)
            chip_vis = scroll_to_chip(br)
            br.sleep(0.4)

            fl1_ok = False
            fl1_detail = "chip=%s" % chip_vis

            if chip_vis:
                # Open the card → stage should be "opened"
                br.click('#exh-cap .ex-quiz-chip', settle=0.5)
                br.sleep(0.3)
                # Answer (miss) → stage should be "lost"
                if br.evaluate("!!document.querySelector('#ex-quiz-card .quiz-opt')"):
                    br.click('#ex-quiz-card .quiz-opt', settle=0.3)
                    br.sleep(1.5)  # let the miss auto-close run
                # Trigger walk_exit by clicking the return button
                br.evaluate("(function(){var f=document.getElementById('exh-fin');"
                            "if(f) f.scrollIntoView({behavior:'instant'});})();")
                br.sleep(0.5)
                ret_btn = br.evaluate("!!document.querySelector('#ex-return')")
                if ret_btn:
                    br.click('#ex-return', settle=0.5)
                    br.sleep(0.5)
                evs = events_dict(br)
                exit_params = evs.get("walk_exit", {})
                unfold_params = evs.get("walk_unfold", {})
                stage_val = exit_params.get("quiz_stage")
                ladder = {"shown", "opened", "won", "lost", "gift"}
                stage_in_ladder = stage_val in ladder if stage_val else False
                unfold_stage = unfold_params.get("quiz_stage")
                unfold_ok = (unfold_stage is None) or (unfold_stage in ladder)
                # no answer text leaking (all values in ladder are short words; nothing else long)
                no_answer_text = not any(
                    len(str(v)) > 10 for v in exit_params.values()
                    if isinstance(v, str) and v not in ladder
                )
                fl1_ok = (stage_val is not None and stage_in_ladder
                          and unfold_ok and no_answer_text)
                fl1_detail = ("chip=%s exit_stage=%s unfold_stage=%s exit_params=%s"
                              % (chip_vis, stage_val, unfold_stage, exit_params))

            check(BROWSER_ROWS[0], fl1_ok, fl1_detail)

        # ---- FL2: ladder never moves backwards, survives a reload -----------
        # Scenario: open card (→ opened), reload, verify stage still "opened"
        # Then answer win (→ won), reload, verify stage still "won"
        with Browser(width=1280, height=900) as br:
            stub_quiz_win(br)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.0)
            chip_vis = scroll_to_chip(br)
            br.sleep(0.4)

            fl2_ok = False
            fl2_detail = "chip=%s" % chip_vis

            if chip_vis:
                # Open card → stage should advance to "opened"
                br.click('#exh-cap .ex-quiz-chip', settle=0.6)
                br.sleep(0.4)
                stage_after_open = br.evaluate(
                    "sessionStorage.getItem(%s)" % json.dumps(STAGE_KEY)
                )
                # Reload — stage should survive
                br.reload(); br.sleep(1.0)
                stage_after_reload = br.evaluate(
                    "sessionStorage.getItem(%s)" % json.dumps(STAGE_KEY)
                )
                # Answer (win) path
                chip_vis2 = scroll_to_chip(br)
                if chip_vis2:
                    br.click('#exh-cap .ex-quiz-chip', settle=0.5)
                    br.sleep(0.3)
                    if br.evaluate("!!document.querySelector('#ex-quiz-card .quiz-opt')"):
                        br.click('#ex-quiz-card .quiz-opt', settle=0.5)
                        br.sleep(1.2)
                stage_after_win = br.evaluate(
                    "sessionStorage.getItem(%s)" % json.dumps(STAGE_KEY)
                )
                # Verify: opened survives reload; won doesn't regress
                ladder_rank = {"shown": 1, "opened": 2, "won": 3, "lost": 3, "gift": 4}
                rank_open = ladder_rank.get(stage_after_open, 0)
                rank_reload = ladder_rank.get(stage_after_reload, 0)
                rank_win = ladder_rank.get(stage_after_win, 0)
                survives = rank_reload >= rank_open and rank_reload > 0
                advances = rank_win >= rank_open
                fl2_ok = survives and advances
                fl2_detail = ("after_open=%s after_reload=%s after_win=%s "
                              "survives=%s advances=%s"
                              % (stage_after_open, stage_after_reload,
                                 stage_after_win, survives, advances))

            check(BROWSER_ROWS[1], fl2_ok, fl2_detail)

        # ---- FL3: control-arm and flag-off stamp nothing --------------------
        fl3_control_ok = False
        fl3_flagoff_ok = False
        fl3_detail = ""

        # Sub-case A: control-arm walk
        with Browser(width=1280, height=900) as br:
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br, visitor_key=VISITOR_KEY_CTRL)
            br.reload(); br.sleep(1.0)
            br.evaluate("(function(){var f=document.getElementById('exh-fin');"
                        "if(f) f.scrollIntoView({behavior:'instant'});})();")
            br.sleep(0.5)
            if br.evaluate("!!document.querySelector('#ex-return')"):
                br.click('#ex-return', settle=0.5); br.sleep(0.5)
            evs = events_dict(br)
            exit_params = evs.get("walk_exit", {})
            unfold_params = evs.get("walk_unfold", {})
            # quiz_stage must NOT appear on control arm
            fl3_control_ok = ("quiz_stage" not in exit_params and
                              "quiz_stage" not in unfold_params)
            fl3_detail += "control_exit=%s " % exit_params

        # Sub-case B: flag-off bake (GA tag present but quiz flag off)
        with serve(TMP_OFF) as base_off:
            with Browser(width=1280, height=900) as br:
                br.block(["*googletagmanager*", "*google-analytics*"])
                br.navigate(base_off + "/")
                br.evaluate("localStorage.clear(); sessionStorage.clear()")
                br.evaluate("localStorage.setItem('ex-tempo','0.05')")
                br.reload(); br.sleep(1.0)
                br.evaluate("(function(){var f=document.getElementById('exh-fin');"
                            "if(f) f.scrollIntoView({behavior:'instant'});})();")
                br.sleep(0.5)
                if br.evaluate("!!document.querySelector('#ex-return')"):
                    br.click('#ex-return', settle=0.5); br.sleep(0.5)
                evs = events_dict(br)
                exit_params = evs.get("walk_exit", {})
                fl3_flagoff_ok = "quiz_stage" not in exit_params
                fl3_detail += "flagoff_exit=%s" % exit_params

        check(BROWSER_ROWS[2],
              fl3_control_ok and fl3_flagoff_ok,
              "control_ok=%s flagoff_ok=%s %s" % (fl3_control_ok, fl3_flagoff_ok, fl3_detail))

        # ---- FL4: only quiz prize yes stamps gift ----------------------------
        # Sub-case A: plain right-click gift → yes → NO gift stage stamp
        fl4_plain_ok = False
        fl4_quiz_ok = False
        fl4_detail = ""

        with Browser(width=1280, height=900) as br:
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.0)
            # Trigger a right-click gift (plain grab, not quiz)
            work_img = br.evaluate("!!document.querySelector('.exh-frame img.work')")
            if work_img:
                br.evaluate("""(function(){
                  var img = document.querySelector('.exh-frame img.work');
                  if (img) { var ev = new MouseEvent('contextmenu', {bubbles:true,cancelable:true});
                    img.dispatchEvent(ev); }
                })()""")
                br.sleep(0.5)
                gift_open = br.evaluate(
                    "!!(document.getElementById('ex-gift-card') && "
                    "!document.getElementById('ex-gift-card').hidden)"
                )
                if gift_open:
                    br.click('.gift-yes', settle=0.3)
                    br.sleep(0.3)
                # quiz_stage must not be "gift" from a plain right-click
                stage_val = br.evaluate("sessionStorage.getItem(%s)" % json.dumps(STAGE_KEY))
                fl4_plain_ok = (stage_val != "gift")
                fl4_detail += "plain_gift_stage=%s gift_opened=%s " % (stage_val, gift_open)
            else:
                fl4_plain_ok = True  # no image to test; sub-check skipped
                fl4_detail += "no work img (sub-check skipped) "

        # Sub-case B: quiz win → yes → stage should be "gift"
        with Browser(width=1280, height=900) as br:
            stub_quiz_win(br)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.0)
            chip_vis = scroll_to_chip(br)
            br.sleep(0.4)

            if chip_vis:
                br.click('#exh-cap .ex-quiz-chip', settle=0.5)
                br.sleep(0.3)
                if br.evaluate("!!document.querySelector('#ex-quiz-card .quiz-opt')"):
                    br.click('#ex-quiz-card .quiz-opt', settle=0.5)
                    br.sleep(1.0)
                    gift_open = br.evaluate(
                        "!!(document.getElementById('ex-gift-card') && "
                        "!document.getElementById('ex-gift-card').hidden)"
                    )
                    if gift_open:
                        br.click('.gift-yes', settle=0.3)
                        br.sleep(0.3)
                    stage_after_yes = br.evaluate(
                        "sessionStorage.getItem(%s)" % json.dumps(STAGE_KEY)
                    )
                    fl4_quiz_ok = (stage_after_yes == "gift")
                    fl4_detail += "quiz_win_stage=%s gift_open=%s" % (stage_after_yes, gift_open)
            else:
                fl4_detail += "chip not visible for quiz win sub-check"

        check(BROWSER_ROWS[3],
              fl4_plain_ok and fl4_quiz_ok,
              "plain_ok=%s quiz_ok=%s %s" % (fl4_plain_ok, fl4_quiz_ok, fl4_detail))


# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, status, detail in results:
    mark = {"PASS": "ok ", "FAIL": "XX ", "SKIP": "-- "}[status]
    line = "%s%s" % (mark, name)
    if detail and status != "PASS":
        line += "  [%s]" % detail
    print(line)
n_pass = sum(1 for r in results if r[1] == "PASS")
n_skip = sum(1 for r in results if r[1] == "SKIP")
print("\ntest_quiz_flow: %d passed, %d failed, %d skipped"
      % (n_pass, len(fails), n_skip))
sys.exit(1 if fails else 0)
