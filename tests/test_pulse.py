#!/usr/bin/env python3
"""The walk's analytics beats — the EVENT REGISTRY (EX-PULSE / INV-41) — adapted for exhibition-engine.

The registry is the ONE home of what the exhibition measures. With the tag baked, a real walk pushes
its registry beats onto the tag's own queue (dataLayer), each carrying at most the work's public id and
a word from a closed BAKED ladder (a kind, a tongue); baked without the tag, the same walk is totally
silent and never errors. A standing guard holds the registry in BOTH directions: a beat in the code
missing from the registry is red, a registry line with no live emitter is red (born of the real drift
where `series_open` shipped onto the wire with no spec sentence).

The remote tag script is BLOCKED — the inline snippet's own queue is the assertion surface, so the
suite never talks to Google. Chrome absent → pinned expected SKIPs.

Deliberately narrower than an instance: the engine carries no read side (`ga_report.py`,
`ga_register_dimensions.py`), so the reference's "read side keeps pace" string row is omitted here —
the same convention as test_quiz_flow's FL5/FL6 omission (DELTA-9).
Run: python tests/test_pulse.py
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


# ---- the registry: the ONE home of what the exhibition measures (SPEC EX-PULSE table) ----------
REGISTRY = {
    "door_pick", "walk_unfold", "walk_exit", "share_copy", "share_arrive",
    "sound_on", "sound_off", "series_open", "series_lift", "gift_download", "lang_pick",
    # the measurement extension (INV-79), ported with the instance generic layer (de-fork stage 4)
    "viewer_lang", "return_gap", "copy_attempt", "story_told",
    "buy_click",   # the pre-conversion reach (the gift card's buy line)
    "door_ready",  # EX-TIME-READ (INV-41): the arrival's coarse load read — once per arrival
}

TMP = Path(tempfile.mkdtemp(prefix="synth_pulse_"))
build_site.OUT = TMP
build_site.build(SITE_URL, ga_id="G-TESTTEST")

TMP_OFF = Path(tempfile.mkdtemp(prefix="synth_pulse_off_"))
build_site.OUT = TMP_OFF
build_site.build(SITE_URL)                      # no ga_id — the tagless bake

_head = (TMP / "index.html").read_text(encoding="utf-8")
_work = next((TMP / "w").glob("*.html")).read_text(encoding="utf-8")
_off = (TMP_OFF / "index.html").read_text(encoding="utf-8")
JS_SRC = (TMP / "exhibition.js").read_text(encoding="utf-8")


# ---- DOM row: consent speaks first --------------
def _consent_ok(html):
    c = html.find("gtag('consent','default'")
    cfg = html.find("gtag('config'")
    return (c != -1 and cfg != -1 and c < cfg
            and "'ad_storage':'denied'" in html
            and "'ad_user_data':'denied'" in html
            and "'ad_personalization':'denied'" in html
            and "'analytics_storage':'granted'" in html)


check("EX-PULSE consent defaults precede the tag config (ads denied, analytics granted) on every tagged page",
      _consent_ok(_head) and _consent_ok(_work) and "gtag('consent'" not in _off,
      f"index={_consent_ok(_head)} work={_consent_ok(_work)} off_clean={'gtag' not in _off}")


# ---- STRING row: the registry is guarded BOTH ways (the series_open drift class killed) ----
def pulse_beats(src):
    """Every beat NAME a pulse() call names — reads only the FIRST argument of each pulse(...) call
    (a literal or a `cond ? "a" : "b"` ternary), never the extra-params object, so a param value like
    `gift_kind:"quiz_prize"` is not mistaken for a beat."""
    beats = set()
    i = 0
    tok = re.compile(r'"([a-z_]+)"')
    while True:
        j = src.find("pulse(", i)
        if j < 0:
            break
        k = j + len("pulse(")
        depth = 1
        arg = []
        while k < len(src) and depth > 0:
            ch = src[k]
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
                if depth == 0:
                    break
            elif ch == "," and depth == 1:
                break
            arg.append(ch)
            k += 1
        for m in tok.findall("".join(arg)):
            beats.add(m)
        i = j + len("pulse(")
    return beats


_emitted = pulse_beats(JS_SRC)
_strays = _emitted - REGISTRY            # a beat on the wire with no registry line
_orphans = REGISTRY - _emitted           # a registry line with no live emitter (rotting green)
check("EX-PULSE the registry is guarded BOTH ways — every emitter names a registry beat, every beat has an emitter",
      not _strays and not _orphans,
      f"emitted={sorted(_emitted)} strays={sorted(_strays)} orphans={sorted(_orphans)}")


# ---- STRING row: gift_download's kind is wired from the closed pair (quiz_prize / grab) ----
# The grab kind is proven end-to-end in the browser below; the quiz-prize kind rides the same
# giftDownload on `preMarked` (the /api/quiz judge is unreachable in a static bake — no worker).
_gift_emitter = 'pulse("gift_download"' in JS_SRC
_gift_kinds = ('"quiz_prize"' in JS_SRC) and ('"grab"' in JS_SRC)
_gift_by_premarked = "gift_kind" in JS_SRC and "preMarked" in JS_SRC
_win_premarked = "data.prize" in JS_SRC and ", true" in JS_SRC   # the win path opens the gift preMarked
check("EX-PULSE gift_download fires with gift_kind from the closed pair — quiz_prize (the win path) / grab",
      _gift_emitter and _gift_kinds and _gift_by_premarked and _win_premarked,
      f"emitter={_gift_emitter} kinds={_gift_kinds} by_premarked={_gift_by_premarked} win_premarked={_win_premarked}")


# ================= BROWSER rows =================
BROWSER_ROWS = [
    "EX-PULSE the five beats fire (door_pick · walk_unfold · walk_exit · share_copy · share_arrive; params ⊆ {work})",
    "EX-PULSE no tag = total silence (no queue, no pushes, no errors) — new beats included",
    "EX-PULSE gift_download fires on a grab's yes (gift_kind=grab, the work id)",
    "EX-PULSE the side room counts — series_open (the series root's work) + one series_lift per LIFT, none on set-down",
    "EX-PULSE the tongue counts — a baked pick reports its code; an outsider tongue reports `other`",
    "EX-PULSE walk_exit counts every leave — the exit control ONE, a browser-Back leave ONE, a cold door render NONE",
]

# ---- EX-AB / INV-90 / INV-91 — the variant frame (SPEC "Experiments — the variant frame") ------
# NOT YET BUILT: today `quiz_arm` is a hardcoded dimension that rides ONLY walk_unfold/walk_exit
# (exhibition.js pulse()); the spec's registry-driven frame stamps EVERY dealt arm on EVERY
# registry beat (INV-91), and mints the coat-check token (ex.visitor) ahead of the very first
# seed read so the first visit already deals off the token a later visit holds (INV-90). These
# rows are expected RED against current code.
VF_ROWS = [
    "VF-STAMP EX-AB/INV-91 the dealt quiz_arm rides EVERY registry beat, not only walk_unfold/walk_exit",
    "VF-SEED-STABLE EX-AB/INV-90 a fixed seed token deals the same arm across two loads, matching EXQuiz's own hash",
    "VF-MINT-DEAL EX-AB/INV-90 a fresh profile mints ex.visitor at boot and deals off THAT token, not a later-read one",
    "VF-RESET EX-AB/INV-90/EX-RESET ?reset deals a fresh token yet the next walk still stamps quiz_arm on its first beat",
]

EVLIST = ("JSON.stringify((window.dataLayer||[]).filter(e=>e[0]==='event')"
          ".map(e=>[e[1], e[2]||{}]))")
CLIP_STUB = ("window.__copied=[];if(navigator.clipboard)navigator.clipboard.writeText="
             "(t)=>{window.__copied.push(t);return Promise.resolve();};")
GRAB = ("(function(){var im=document.querySelector('.exh-frame img.work');if(!im)return null;"
        "var fr=im.closest('.exh-frame');im.dispatchEvent(new MouseEvent('contextmenu',"
        "{bubbles:true,cancelable:true}));return fr?fr.dataset.id:null;})()")


def evs_of(br):
    return json.loads(br.evaluate(EVLIST) or "[]")


def count_of(evs, beat):
    return sum(1 for n, p in evs if n == beat)


def first_of(evs, beat):
    return next((p for n, p in evs if n == beat), None)


def cold(br, base, visitor=None):
    """A fresh cold arrival at the door, fast tempo, clean storage."""
    br.navigate(base + "/")
    br.evaluate("localStorage.clear();sessionStorage.clear()")
    if visitor:
        br.evaluate("localStorage.setItem('ex.visitor'," + json.dumps(visitor) + ")")
    br.evaluate("localStorage.setItem('ex-tempo','0.2')")
    br.reload()
    br.sleep(1.0)


def enter_walk(br):
    """Pick the first door window → the walk."""
    br.click(".exd-window:nth-child(1)", settle=0.1)
    br.sleep(1.2)


def walk_all(br, base):
    """cold door → pick → unfold → share → exit → arrive by a shared link (the five beats)"""
    cold(br, base)
    enter_walk(br)
    br.click(".ex-share", settle=0.4)
    br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
    br.sleep(0.5)
    br.click("#ex-unfold", settle=0.6)
    br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
    br.sleep(0.5)
    br.click("#ex-return", settle=0.8)
    target = br.evaluate("JSON.parse(localStorage.getItem('ex.exhibition')||'{}').pick")
    br.navigate(base + "/#w-" + str(target))
    br.sleep(1.0)
    return target


if not chrome_available():
    for r in BROWSER_ROWS + VF_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    TMP_I18N = Path(tempfile.mkdtemp(prefix="synth_pulse_i18n_"))
    build_site.OUT = TMP_I18N
    build_site.build(SITE_URL, ga_id="G-TESTTEST", enable=["ai_i18n"])

    # bake for the variant-frame rows: quiz on (so an arm is always dealt) + visitor_memory on
    # (so the coat-check token mint path is live — VF-MINT-DEAL/VF-RESET need it)
    TMP_VF = Path(tempfile.mkdtemp(prefix="synth_pulse_vf_"))
    build_site.OUT = TMP_VF
    build_site.build(SITE_URL, ga_id="G-TESTTEST", enable=["quiz", "visitor_memory"])

    # ---- ROW: the five beats fire (re-scoped under the registry) --------------
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])   # never talk to Google
            target = walk_all(br, base)
            evs = dict(evs_of(br))
            need = {"door_pick", "walk_unfold", "walk_exit", "share_copy", "share_arrive"}
            # params ⊆ {work} is asserted for the FIVE core beats only — the boot beats
            # (viewer_lang) carry their own closed params under INV-79
            params_ok = all(set(evs[b].keys()) <= {"work"} for b in need if b in evs)
            works_ok = (evs.get("door_pick", {}).get("work")
                        and evs.get("share_arrive", {}).get("work") == str(target))
            check(BROWSER_ROWS[0],
                  need.issubset(evs) and params_ok and bool(works_ok),
                  f"events={sorted(evs)} params_ok={params_ok} arrive={evs.get('share_arrive')}")

    # ---- ROW: no tag = total silence, the NEW beats included (a grab under no tag) ----
    with serve(TMP_OFF) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            cold(br, base)
            enter_walk(br)
            br.evaluate(GRAB)                            # a grab fires giftDownload → pulse (silent)
            br.sleep(0.4)
            br.click(".gift-yes", settle=0.3)
            silent = br.evaluate("(window.dataLayer||[]).filter(e=>e[0]==='event').length") == 0
            alive = br.evaluate("1+1") == 2
            check(BROWSER_ROWS[1], silent and alive, f"silent={silent} alive={alive}")

    # ---- ROW: gift_download on a grab's yes (gift_kind=grab, the work id) -------------
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            cold(br, base)
            enter_walk(br)
            grabbed = br.evaluate(GRAB)                  # right-click the work in view → the gift offer
            br.sleep(0.4)
            br.click(".gift-yes", settle=0.4)            # yes → the file leaves → gift_download
            br.sleep(0.3)
            evs = evs_of(br)
            gp = first_of(evs, "gift_download")
            ok = (gp is not None and gp.get("gift_kind") == "grab"
                  and gp.get("work") == str(grabbed) and set(gp.keys()) <= {"work", "gift_kind"})
            check(BROWSER_ROWS[2], ok, f"grabbed={grabbed} gift_download={gp}")

    # ---- ROW: the side room counts — series_open + series_lift (lift only, never set-down) ----
    exdata = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
    _poly = next((s for s in exdata.get("series", []) if s.get("variant") == "polaroids"), None)
    ser_work = _poly["members"][0] if _poly and _poly.get("members") else None
    if not ser_work:
        skip(BROWSER_ROWS[3], "no polaroid series in the bake")
    else:
        with serve(TMP) as base:
            with Browser(width=1280, height=900) as br:
                br.inject(CLIP_STUB)
                br.block(["*googletagmanager*", "*google-analytics*"])
                br.navigate(base + "/")
                br.evaluate("localStorage.clear();sessionStorage.clear()")
                br.evaluate("localStorage.setItem('ex-tempo','0.2')")
                br.navigate(base + "/#w-" + str(ser_work))     # arrive AT the series' work
                br.sleep(1.2)
                has_pill = br.evaluate("!!document.querySelector('.ex-series')")
                br.click(".ex-series", settle=0.5)             # open the side room
                br.sleep(0.4)
                br.click(".exs-print:nth-child(1)", settle=0.3)   # LIFT one polaroid
                br.sleep(0.2)
                br.click(".exs-print:nth-child(1)", settle=0.3)   # set it back DOWN — no beat
                br.sleep(0.2)
                br.click(".exs-print:nth-child(2)", settle=0.3)   # LIFT another
                br.sleep(0.2)
                evs = evs_of(br)
                op = first_of(evs, "series_open")
                open_ok = op is not None and op.get("work") == str(ser_work)
                lift_n = count_of(evs, "series_lift")
                check(BROWSER_ROWS[3],
                      has_pill and open_ok and lift_n == 2,
                      f"pill={has_pill} series_open={op} lift_count={lift_n} (expect 2)")

    # ---- ROW: the tongue counts — a baked pick (he) + an outsider pick (other) --------
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            cold(br, base)                               # at the cold door, browser locale = en (baked)
            br.click("#exd-lang .exl-cur", settle=0.3)   # open the tongue list
            br.click('#exd-lang .exl-item[data-lang="he"]', settle=0.3)
            baked = first_of(evs_of(br), "lang_pick")
    with serve(TMP_I18N) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*", "*/api/*"])
            br.pretend("pl-PL", 15)                      # an OUTSIDE tongue (i18n on ⇒ it joins the list)
            cold(br, base)
            br.click("#exd-lang .exl-cur", settle=0.3)
            outsider_present = br.evaluate("!!document.querySelector('#exd-lang .exl-item[data-lang=\"pl\"]')")
            br.click('#exd-lang .exl-item[data-lang="pl"]', settle=0.3)
            outsider = first_of(evs_of(br), "lang_pick")
    baked_ok = baked is not None and baked.get("lang") == "he" and set(baked.keys()) <= {"lang"}
    outsider_ok = outsider is not None and outsider.get("lang") == "other"
    check(BROWSER_ROWS[4],
          baked_ok and outsider_present and outsider_ok,
          f"baked={baked} outsider_present={outsider_present} outsider={outsider}")

    # ---- ROW: walk_exit counts EVERY leave (exit control · Back · none at a cold door) ----
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            # (a) a cold door render lays NO walk_exit
            cold(br, base)
            cold_zero = count_of(evs_of(br), "walk_exit") == 0
            # (b) the exit control lays ONE
            enter_walk(br)
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.4)
            br.click("#ex-return", settle=0.6)
            exit_ctrl_n = count_of(evs_of(br), "walk_exit")
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            # (c) a browser-Back leave from the walk to the door lays ONE (the funnel's undercount fixed)
            cold(br, base)
            enter_walk(br)
            before_back = count_of(evs_of(br), "walk_exit")     # 0 — no exit yet
            br.evaluate("history.back()")
            br.sleep(0.7)
            at_door = br.evaluate("document.body.classList.contains('ex-door')")
            back_n = count_of(evs_of(br), "walk_exit")
    check(BROWSER_ROWS[5],
          cold_zero and exit_ctrl_n == 1 and before_back == 0 and at_door and back_n == 1,
          f"cold0={cold_zero} exit_ctrl={exit_ctrl_n} before_back={before_back} at_door={at_door} back={back_n}")

    # ================= VF rows: the variant frame (EX-AB / INV-90 / INV-91) =================
    FIXED_SEED_TOKEN = "abcdefgh12345678"    # 16 chars a-z0-9 — passes BOTH the quiz-token regex
                                              # (8-40) and the visitor-memory regex (16-40), so a
                                              # pre-seeded token is never overwritten by a fresh mint

    def _hash_arm_of(br, token):
        """The expected arm for `token`, computed IN-PAGE via the client's own exported hash
        (window.EXQuiz._hash — the quizHash the quiz arm has always drawn from), salt 'quizarm'."""
        return br.evaluate(
            "(()=>{const h=window.EXQuiz._hash(%s+':quizarm');"
            "return (h/4294967296)<0.5?'on':'control';})()" % json.dumps(token))

    with serve(TMP_VF) as base:
        # ---- VF-STAMP: every event on the queue carries the dealt quiz_arm, not only unfold/exit
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            walk_all(br, base)                      # door_pick, share_copy, walk_unfold, walk_exit, share_arrive
            evs = evs_of(br)
            arm = br.evaluate("window.EXQuiz && window.EXQuiz.arm()")
            beats = [n for n, p in evs]
            every_has_arm = bool(evs) and all(p.get("quiz_arm") == arm for n, p in evs)
            first_has_arm = bool(evs) and evs[0][1].get("quiz_arm") == arm
            check(VF_ROWS[0],
                  arm in ("on", "control") and every_has_arm and first_has_arm,
                  f"arm={arm} beats={beats} events={evs}")

        # ---- VF-SEED-STABLE: a fixed seed deals the same arm on both loads, matching the hash --
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base + "/")
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex.visitor', %s)" % json.dumps(FIXED_SEED_TOKEN))
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.reload(); br.sleep(1.0)
            expected_arm = _hash_arm_of(br, FIXED_SEED_TOKEN)
            enter_walk(br)
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.5)
            br.click("#ex-return", settle=0.6)
            exit1 = first_of(evs_of(br), "walk_exit")
            arm1 = exit1.get("quiz_arm") if exit1 else None

            br.navigate(base + "/")
            br.reload(); br.sleep(1.0)
            stored_still = br.evaluate("localStorage.getItem('ex.visitor')")
            enter_walk(br)
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.5)
            br.click("#ex-return", settle=0.6)
            exit2 = first_of(evs_of(br), "walk_exit")
            arm2 = exit2.get("quiz_arm") if exit2 else None
            check(VF_ROWS[1],
                  stored_still == FIXED_SEED_TOKEN
                  and arm1 == expected_arm and arm2 == expected_arm and arm1 == arm2,
                  f"expected={expected_arm} arm1={arm1} arm2={arm2} stored_still={stored_still}")

        # ---- VF-MINT-DEAL: a FRESH profile mints ex.visitor at boot and deals off THAT token ----
        # (today QUIZ_TOKEN/quizArm are computed before the visitor-memory mint runs, so the very
        # first load deals off a throwaway per-tab id while a DIFFERENT token lands in storage)
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            br.navigate(base + "/")
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.reload(); br.sleep(1.0)
            client_token_first = br.evaluate("window.EXQuiz && window.EXQuiz.token")
            stored_token_first = br.evaluate("localStorage.getItem('ex.visitor')")
            valid_stored = bool(stored_token_first) and bool(
                re.match(r"^[a-z0-9]{16,40}$", stored_token_first or ""))
            deals_off_stored = client_token_first == stored_token_first
            arm_first = br.evaluate("window.EXQuiz && window.EXQuiz.arm()")

            br.reload(); br.sleep(1.0)               # a second load, same profile: the token now
            client_token_second = br.evaluate("window.EXQuiz && window.EXQuiz.token")  # persists
            arm_second = br.evaluate("window.EXQuiz && window.EXQuiz.arm()")
            stable_token = client_token_second == stored_token_first
            stable_arm = arm_second == arm_first
            check(VF_ROWS[2],
                  valid_stored and deals_off_stored and stable_token and stable_arm,
                  f"stored_first={stored_token_first} valid={valid_stored} "
                  f"client_first={client_token_first} deals_off_stored={deals_off_stored} "
                  f"arm_first={arm_first} client_second={client_token_second} "
                  f"arm_second={arm_second} stable_token={stable_token} stable_arm={stable_arm}")

        # ---- VF-RESET: ?reset deals a fresh token; the next walk still stamps quiz_arm ----------
        # asserted on the FIRST beat the fresh walk lays (door_pick) — not only unfold/exit — the
        # same "every beat" law VF-STAMP proves, exercised through the reset road (EX-RESET).
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.block(["*googletagmanager*", "*google-analytics*"])
            cold(br, base)                            # a fresh arrival mints a token (memory on)
            token1 = br.evaluate("localStorage.getItem('ex.visitor')")
            br.navigate(base + "/?reset")
            br.sleep(1.0)
            token_after_reset = br.evaluate("localStorage.getItem('ex.visitor')")
            reminted = bool(token_after_reset) and token_after_reset != token1
            enter_walk(br)
            evs = evs_of(br)
            first_beat_arm = evs[0][1].get("quiz_arm") if evs else None
            check(VF_ROWS[3],
                  reminted and first_beat_arm in ("on", "control"),
                  f"token1={token1} token_after_reset={token_after_reset} reminted={reminted} "
                  f"events={evs} first_beat_arm={first_beat_arm}")

    shutil.rmtree(TMP_VF, ignore_errors=True)
    shutil.rmtree(TMP_I18N, ignore_errors=True)

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_OFF, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
