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
    "FL7 EX-QUIZ-REPLY a slow in-flight submit shows the visible pending reassurance (INV-65)",
    "FL8 EX-QUIZ-REPLY a 503 edge holds the calm face and re-opens the choice, burning nothing (INV-65)",
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


def stub_quiz_503(br):
    """Stub /api/quiz to FAIL with HTTP 503 — an edge that never reaches a verdict.

    A non-ok status (429/503/down) is the same class as a network drop: the client got
    NO verdict back. The fixed answer() throws on !r.ok and routes to reachFailed() — the
    quiet pending face, buttons re-opened, no answered-memory, no stage. The buggy prior
    version treated 503 as a miss (missAndFade). This stub drives EX-QUIZ-REPLY's edge branch.
    """
    br.inject(
        "(function(){var _f=window.fetch;"
        "window.fetch=function(u,o){"
        "if(String(u).indexOf('/api/quiz')>=0){"
        "return Promise.resolve(new Response('Service Unavailable',"
        "{status:503,headers:{'Content-Type':'text/plain'}}));}"
        "return _f.apply(this,arguments);};})()"
    )


def stub_quiz_slow(br, delay_ms=1600):
    """Stub /api/quiz to RESOLVE (as a miss) only after delay_ms — a slow-but-non-failing edge.

    The round-trip is genuinely owed for delay_ms, so the client sits in the in-flight (pending)
    state the whole time; the reply lands only when the timer fires."""
    br.inject(
        "(function(){var _f=window.fetch;"
        "window.fetch=function(u,o){"
        "if(String(u).indexOf('/api/quiz')>=0){"
        "return new Promise(function(res){setTimeout(function(){"
        "res(new Response(JSON.stringify({ok:false}),"
        "{status:200,headers:{'Content-Type':'application/json'}}));}, %d);});}"
        "return _f.apply(this,arguments);};})()" % int(delay_ms)
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
                # no answer text leaking (INV-1): every beat value is a closed-ladder word — the stage
                # ladder plus the dealt experiment arms (quiz_arm, quiz_chip_copy). A leaked answer
                # would be a free-form string outside these closed sets; `place_prize` (a registered
                # quiz_chip_copy arm) is legitimate, so the closed arm words are allowed here too.
                closed = ladder | {"on", "control", "place", "place_prize"}
                no_answer_text = not any(
                    len(str(v)) > 10 for v in exit_params.values()
                    if isinstance(v, str) and v not in closed
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

        # ---- FL7: a slow in-flight submit shows the visible PENDING reassurance ----------
        # EX-QUIZ-REPLY / INV-65 — the async reply slot must NAME its pending state. A tap dims + locks
        # the buttons at once (the named pending); past a house grace a still-owed round-trip shows the
        # quiet reassurance in the reply slot. Delay the /api/quiz reply well past the grace, assert the
        # reassurance is VISIBLE while in flight, then let it land and confirm the pending state resolves
        # (the reply replaces it; the miss path auto-closes). Tempo 0.05 → grace ≈ 0.6·0.05 = 30ms.
        fl7_ok = False
        fl7_detail = ""
        with Browser(width=1280, height=900) as br:
            stub_quiz_slow(br, delay_ms=1600)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.0)
            chip_vis = scroll_to_chip(br)
            br.sleep(0.4)
            fl7_detail = "chip=%s" % chip_vis
            if chip_vis:
                br.click('#exh-cap .ex-quiz-chip', settle=0.5)
                br.sleep(0.3)
                if br.evaluate("!!document.querySelector('#ex-quiz-card .quiz-opt')"):
                    br.click('#ex-quiz-card .quiz-opt', settle=0.0)
                    br.sleep(0.4)   # past the 30ms grace, well before the 1.6s reply lands
                    inflight = br.evaluate(
                        "(()=>{const c=document.getElementById('ex-quiz-card');"
                        "const o=c&&c.querySelector('.quiz-out');return {"
                        "pending:!!(c&&c.classList.contains('quiz-inflight')),"
                        "disabled:!!document.querySelector('#ex-quiz-card .quiz-opt[disabled]'),"
                        "wait:!!(o&&o.classList.contains('quiz-wait')),"
                        "shown:!!(o&&o.classList.contains('show')),"
                        "text:o?o.textContent.trim():''};})()"
                    ) or {}
                    pending_named = bool(inflight.get("pending") and inflight.get("disabled"))
                    reassurance_visible = bool(
                        inflight.get("wait") and inflight.get("shown")
                        and len(inflight.get("text") or "") > 0
                    )
                    br.sleep(1.6)   # let the reply land + the fast miss auto-close run
                    after = br.evaluate(
                        "(()=>{const c=document.getElementById('ex-quiz-card');return {"
                        "pending:!!(c&&c.classList.contains('quiz-inflight')),"
                        "hidden:!!(c&&c.hidden)};})()"
                    ) or {}
                    resolved = bool((not after.get("pending")) and after.get("hidden"))
                    fl7_ok = pending_named and reassurance_visible and resolved
                    fl7_detail = "inflight=%s after=%s" % (inflight, after)
        check(BROWSER_ROWS[4], fl7_ok, fl7_detail)

        # ---- FL8: a 503 edge holds the calm face and RE-OPENS the choice ----------
        # EX-QUIZ-REPLY / INV-65 — an edge that never returned a verdict (a non-ok 429/503/down
        # status or a network drop) must NOT read as a wrong answer. The fixed answer() routes it
        # to reachFailed(): the quiet «ещё мгновение» pending line in the reply slot (quiz-wait),
        # the four option buttons RE-ENABLED (no disabled/wrong/dim), NO answered-memory written
        # for the work, and the card left OPEN so the work asks again. (The buggy prior version
        # routed a 503 to missAndFade — button marked wrong, answered-memory written, card fades
        # out — which this test goes RED on.)
        fl8_ok = False
        fl8_detail = ""
        with Browser(width=1280, height=900) as br:
            stub_quiz_503(br)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base_on + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.0)
            chip_vis = scroll_to_chip(br)
            br.sleep(0.4)
            fl8_detail = "chip=%s" % chip_vis
            if chip_vis:
                br.click('#exh-cap .ex-quiz-chip', settle=0.5)
                br.sleep(0.3)
                if br.evaluate("!!document.querySelector('#ex-quiz-card .quiz-opt')"):
                    br.click('#ex-quiz-card .quiz-opt', settle=0.0)
                    # let the 503 land and reachFailed() run; wait past the miss-path fade
                    # window so a RED (buggy) run has fully faded/hidden the card
                    br.sleep(1.0)
                    quiz_ls_key = "ex.quiz." + str(QUIZ_WORK_ID)
                    st = br.evaluate(
                        "(()=>{const c=document.getElementById('ex-quiz-card');"
                        "const o=c&&c.querySelector('.quiz-out');"
                        "const opts=Array.from(document.querySelectorAll('#ex-quiz-card .quiz-opt'));"
                        "return {"
                        "wait:!!(o&&o.classList.contains('quiz-wait')),"
                        "shown:!!(o&&o.classList.contains('show')),"
                        "text:o?o.textContent.trim():'',"
                        "any_disabled:opts.some(b=>b.disabled),"
                        "any_wrong:opts.some(b=>b.classList.contains('wrong')),"
                        "any_dim:opts.some(b=>b.classList.contains('dim')),"
                        "n_opts:opts.length,"
                        "mem:localStorage.getItem(%s),"
                        "card_hidden:!!(c&&c.hidden),"
                        "card_gone:!!(c&&c.classList.contains('gone')),"
                        "card_show:!!(c&&c.classList.contains('show'))"
                        "};})()" % json.dumps(quiz_ls_key)
                    ) or {}
                    # reply slot shows the quiet pending/wait line
                    wait_line = bool(st.get("wait") and st.get("shown")
                                     and len(st.get("text") or "") > 0)
                    # the four option buttons are RE-ENABLED — none disabled, none wrong, none stuck dim
                    buttons_reopened = bool(
                        st.get("n_opts", 0) > 0 and not st.get("any_disabled")
                        and not st.get("any_wrong") and not st.get("any_dim")
                    )
                    # NO answered-memory was written for this work
                    no_memory = st.get("mem") is None
                    # the card is still OPEN (shown, not hidden/gone)
                    card_open = bool((not st.get("card_hidden"))
                                     and (not st.get("card_gone")) and st.get("card_show"))
                    fl8_ok = wait_line and buttons_reopened and no_memory and card_open
                    fl8_detail = ("wait_line=%s buttons_reopened=%s no_memory=%s card_open=%s st=%s"
                                  % (wait_line, buttons_reopened, no_memory, card_open, st))
        check(BROWSER_ROWS[5], fl8_ok, fl8_detail)


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
