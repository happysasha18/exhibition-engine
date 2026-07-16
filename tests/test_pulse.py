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
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    TMP_I18N = Path(tempfile.mkdtemp(prefix="synth_pulse_i18n_"))
    build_site.OUT = TMP_I18N
    build_site.build(SITE_URL, ga_id="G-TESTTEST", enable=["ai_i18n"])

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
