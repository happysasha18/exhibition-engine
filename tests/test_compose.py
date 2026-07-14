#!/usr/bin/env python3
"""EX-COMPOSE / INV-67 — The faces meet (the 2026-07-09 bug class closed as law).
Ten browser rows, one per engine SPEC "The faces meet" clause.

Ported from an instance's tests/test_compose.py — adapted for the engine:
- import engine_build as build_site (the engine shim)
- SITE_URL is the synthetic site URL
- quiz works and series come from the engine's synthetic fixture

Run: .venv/bin/python tests/test_compose.py
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
from quiz_util import arm_of, find_token_arm_on  # noqa: E402

SITE_URL = "https://synth.example.com"
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once (quiz on)
TMP = Path(tempfile.mkdtemp(prefix="synth_compose_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["quiz"])

EXDATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
EX_VER = str(EXDATA["version"])

# quiz works in bake order
quiz_works = [w for w in EXDATA.get("works", []) if w.get("quiz")]
# QUIZ_WORK_ID is determined at browser runtime via EXQuiz.chosen() — the arc order from a given
# pick decides which quiz work is chosen, and we discover it after each setup_walk + reload.
# We pre-compute it once here for skip-gate logic (not None check), then re-read in each row.
QUIZ_WORK_ID = str(quiz_works[0]["id"]) if quiz_works else None

# token with arm=on — any arm-on token works; the chosen work is read from EXQuiz.chosen()
TOKEN_ARM_ON = find_token_arm_on() if quiz_works else None

# series data
SERIES = EXDATA.get("series", [])
# polaroid series: variant != "lane"
POLAROID_SERIES = next((s for s in SERIES if s.get("variant") != "lane"), None)
# lane series: the horizontal polaroid lane (its own native overflow-x scroll — EX-CHROME CH6)
LANE_SERIES = next((s for s in SERIES if s.get("variant") == "lane"), None)
ANY_SERIES = SERIES[0] if SERIES else None

# ---------------------------------------------------------------- second bake WITH the ambient player
# The default synthetic fixture ships no audio, so #ex-sound never renders on it. The EX-CHROME
# player-retraction rows (SND1–4) need a rendered player, so a second bake injects a synthetic
# sound_url into config.json (the JS reads config.json at runtime) — same pattern as test_sound.py.
TMP_SND = Path(tempfile.mkdtemp(prefix="synth_compose_snd_"))
build_site.OUT = TMP_SND
build_site.build(SITE_URL, enable=["quiz"])
_snd_cfg_path = TMP_SND / "config.json"
_snd_cfg = json.loads(_snd_cfg_path.read_text())
_snd_cfg["exhibition"]["sound_url"] = "/audio/ambient.m4a"
_snd_cfg["exhibition"]["sound_credit"] = {
    "artist": "Synth Artist", "title": "Test Track", "url": "https://synth.example.com",
}
_snd_cfg_path.write_text(json.dumps(_snd_cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

# ---------------------------------------------------------------- snippets shared with test_share.py / test_quiz_pick.py
IN_VIEW = ("(()=>{const f=[...document.querySelectorAll('.exh-frame')].find(f=>{"
           "const r=f.getBoundingClientRect();"
           "return r.top<innerHeight*0.5 && r.bottom>innerHeight*0.5;});"
           "return f?f.dataset.id:null;})()")

# EX-CHROME (audio-player retraction): probe whether the ambient player is PRESSABLE — its computed
# pointer-events/opacity and whether elementFromPoint at its centre still lands inside #ex-sound.
SND_PROBE = ("(()=>{const s=document.getElementById('ex-sound');"
             "if(!s)return JSON.stringify({no:1});"
             "const cs=getComputedStyle(s);const r=s.getBoundingClientRect();"
             "const cx=r.left+r.width/2,cy=r.top+r.height/2;"
             "const el=document.elementFromPoint(cx,cy);"
             "return JSON.stringify({pe:cs.pointerEvents,op:parseFloat(cs.opacity),"
             "hit:!!(el&&el.closest&&el.closest('#ex-sound'))});})()")

# a two-finger pinch on `sel` opens the zoom over that picture (mirrors test_zoom's trigger)
PINCH = ("(sel)=>{const el=document.querySelector(sel);if(!el)return 'no-el';"
         "try{const t1=new Touch({identifier:1,target:el,clientX:120,clientY:200});"
         "const t2=new Touch({identifier:2,target:el,clientX:210,clientY:270});"
         "el.dispatchEvent(new TouchEvent('touchstart',{touches:[t1,t2],targetTouches:[t1,t2],"
         "changedTouches:[t1,t2],bubbles:true,cancelable:true}));return 'ok';}"
         "catch(e){return 'err:'+e.message;}}")
ZOPEN = ("(()=>{const z=document.getElementById('ex-zoom');"
         "return !!z&&!z.hidden&&z.classList.contains('show');})()")


def snd_retracted(br):
    """True when the player is present but NOT pressable (pointer-events none or opacity 0, and no hit)."""
    d = json.loads(br.evaluate(SND_PROBE))
    if d.get("no"):
        return False, d
    return (d["pe"] == "none" or d["op"] == 0) and d["hit"] is False, d


def snd_pressable(br):
    """True when the player IS pressable (pointer-events not none, opacity > 0, and it takes the hit)."""
    d = json.loads(br.evaluate(SND_PROBE))
    if d.get("no"):
        return False, d
    return d["pe"] != "none" and d["op"] > 0 and d["hit"] is True, d


BROWSER_ROWS = [
    "CMP1 EX-COMPOSE a standing question card owns the keys",
    "CMP2 EX-COMPOSE a standing gift card owns the keys",
    "CMP3 EX-COMPOSE the side room already held the keys",
    "CMP4 EX-COMPOSE the last face leaves into a fresh-measured room (gift card over a DEEP frame)",
    "CMP5 EX-COMPOSE the re-centre survives the side room's close after a rotation (Back restore)",
    "CMP6 EX-COMPOSE the card is viewport-honest",
    "CMP7 EX-COMPOSE the side room covers the walk's chrome",
    "CMP8 EX-COMPOSE no question in the side room",
    "CMP9 EX-COMPOSE a lifted print re-centres",
    "CMP10 EX-COMPOSE the closing screen is a stop",
]

# ε for centring asserts (px)
EPSILON = 30

# EX-CHROME / INV-70 — one page shape for the browser (seven CH rows, matrix order)
CH_ROWS = [
    "CH1 EX-CHROME the page root stays scrollable under every face",
    "CH2 EX-CHROME the standing door rests the walk's input",
    "CH3 EX-CHROME the guard snaps back foreign scroll",
    "CH4 EX-CHROME the house's own writes pass the guard",
    "CH5 EX-CHROME the scrollbar hides gutter-stable",
    "CH6 EX-CHROME the face's own scroll survives the rest",
    "CH7 EX-CHROME the guard holds under a resting finger",
    "CH8 EX-CHROME a moving finger cannot drag the walk from under a face",
    "CH9 EX-CHROME the narrowed carve-out keeps the lane alive, axis-true",
]

# EX-CHROME — the ambient audio player retracts under a covering face, stays reachable in the zoom
# (proven on the sound-configured bake TMP_SND; the default fixture ships no audio)
SND_ROWS = [
    "SND-RETRACT the ambient player retracts under the door (not pressable)",
    "SND-RETRACT the ambient player retracts under the side room (not pressable)",
    "SND-RETRACT the ambient player retracts under the gift card (not pressable)",
    "SND-RETRACT the ambient player retracts under the question card (not pressable)",
    "SND-RETRACT INV-77 the ambient player stays reachable during the zoom (regression guard)",
]


# A slow REAL finger drag (touchStart → many small moves over ≥1s → lift), no rubber-band stand-in:
# this proves the SOURCE-eating (CH7 owns the foreign-scroll guard). Steps are ~15px each, so the
# first move already crosses the axis-pick threshold — a normal deliberate drag. Returns the max
# page-scroll drift while held and whether the page jerked after lift.
DRAG_INSTR = (
    "(()=>{window.__held=window.scrollY;window.__drift=0;window.__after=[];window.__lift=false;"
    "addEventListener('scroll',()=>{const d=Math.abs(window.scrollY-window.__held);"
    "if(window.__lift){window.__after.push(Math.round(window.scrollY));}"
    "else if(d>window.__drift){window.__drift=d;}},{passive:true});})()"
)


def slow_drag(br, x0, y0, dx_total, dy_total, steps=16, seconds=1.1):
    """Drive a slow real drag from (x0,y0) by (dx_total,dy_total) over `seconds`. NO foreign scroll.
    Returns (held, max_drift_while_held, jerked_after_lift)."""
    br.evaluate(DRAG_INSTR)
    held = br.evaluate("window.scrollY") or 0
    br._cmd("Input.dispatchTouchEvent", type="touchStart",
            touchPoints=[{"x": int(x0), "y": int(y0)}])
    for i in range(1, steps + 1):
        br._cmd("Input.dispatchTouchEvent", type="touchMove",
                touchPoints=[{"x": int(x0 + dx_total * i / steps),
                              "y": int(y0 + dy_total * i / steps)}])
        br.sleep(seconds / steps)
    drift = br.evaluate("window.__drift") or 0
    br.evaluate("window.__lift=true")
    br._cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])
    br.sleep(0.4)
    after = json.loads(br.evaluate("JSON.stringify(window.__after)") or "[]")
    final = br.evaluate("window.scrollY") or 0
    jerked = len(set(after)) > 1 or abs(final - held) > 2
    return held, drift, jerked


def setup_walk(br, quiz_work_pick=None, tempo="0.3"):
    """Set localStorage for a fresh walk with TOKEN_ARM_ON visitor token.

    quiz_work_pick: override the pick work (useful when you need the chip to appear for a specific
    work). If None, uses the second quiz work as the pick — this makes the arc order start from a
    quiz work that is NOT the chosen one, so the chosen (EXQuiz.chosen()) lands at a different arc
    position. The actual chosen work is always discovered after reload via get_quiz_work_id(br).
    """
    # Use the second quiz work as the arc pick by default; this avoids the case where the pick
    # IS the chosen work and the chip doesn't appear at frame-0 (the scroll target).
    default_pick = (str(quiz_works[1]["id"]) if len(quiz_works) > 1
                    else str(quiz_works[0]["id"]) if quiz_works else None)
    pick = quiz_work_pick if quiz_work_pick is not None else default_pick
    br.evaluate("localStorage.clear(); sessionStorage.clear()")
    br.evaluate(f"localStorage.setItem('ex-tempo', {json.dumps(tempo)})")
    br.evaluate(f"localStorage.setItem('ex.visitor', {json.dumps(TOKEN_ARM_ON)})")
    if pick:
        br.evaluate(
            "localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
            % (json.dumps(EX_VER), json.dumps(str(pick)))
        )


def get_quiz_work_id(br):
    """Return the quiz work the browser has chosen (from window.EXQuiz.chosen()).
    Call after reload + sleep so the walk is initialised."""
    return br.evaluate("window.EXQuiz && window.EXQuiz.chosen()")


def open_quiz_card(br):
    """Scroll the browser's chosen quiz work into view, click the chip, wait for card to open.
    Returns True if the card has class 'show'."""
    chosen_id = get_quiz_work_id(br)
    if not chosen_id:
        return False
    br.evaluate(
        "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
        "if(f)f.scrollIntoView({behavior:'instant'});})()" % str(chosen_id)
    )
    br.sleep(0.7)
    try:
        br.click(".ex-quiz-chip", settle=0.5)
    except RuntimeError:
        return False
    return br.evaluate("document.querySelector('#ex-quiz-card')?.classList.contains('show')")


def open_gift_card(br):
    """Dispatch contextmenu on a work image to open the gift card.
    Returns True if the gift card has class 'show'."""
    br.evaluate(
        "document.querySelector('.exh-frame img.work')"
        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))"
    )
    br.sleep(0.6)
    return br.evaluate("document.querySelector('#ex-gift-card')?.classList.contains('show')")


def open_side_room(br, series=None, member_pick=None):
    """Set walk pick to a member of the series, enter the walk, scroll to that member,
    click .ex-series in the caption. Returns True if body has class ex-side."""
    s = series if series is not None else ANY_SERIES
    if s is None:
        return False
    pick_id = member_pick if member_pick is not None else s["members"][0]
    # set the walk with the series member as the pick so the series pill appears
    br.evaluate("localStorage.clear(); sessionStorage.clear()")
    br.evaluate("localStorage.setItem('ex-tempo', '0.3')")
    br.evaluate(f"localStorage.setItem('ex.visitor', {json.dumps(TOKEN_ARM_ON)})")
    br.evaluate(
        "localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
        % (json.dumps(EX_VER), json.dumps(str(pick_id)))
    )
    br.reload()
    br.sleep(1.2)
    # scroll to the member frame so its series pill appears in the caption
    br.evaluate(
        "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
        "if(f)f.scrollIntoView({behavior:'instant'});})()" % str(pick_id)
    )
    br.sleep(0.5)
    br.click(".ex-series", settle=1.5)
    return br.evaluate("document.body.classList.contains('ex-side')")


def frame_centre_offset(br, work_id):
    """Return the vertical distance (px) between the work frame centre and the viewport centre."""
    return br.evaluate(
        "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
        "if(!f)return 9999;"
        "const r=f.getBoundingClientRect();"
        "const fc=r.top+r.height/2;"
        "return Math.abs(fc-innerHeight/2);})()" % str(work_id)
    )


def reach_reopened_door(br):
    """From a fresh walk, scroll to the finale and click the exit — the door RE-OPENS over the
    still-built walk (EX-CHROME: a standing face like the others). True if body.ex-door stands."""
    setup_walk(br)
    br.reload()
    br.sleep(1.2)
    br.evaluate("document.getElementById('exh-fin')?.scrollIntoView({behavior:'instant'})")
    br.sleep(0.5)
    if not br.evaluate("!!document.getElementById('ex-return')"):
        return False
    br.click("#ex-return", settle=1.2)
    return br.evaluate("document.body.classList.contains('ex-door')")


def root_overflow_vertical(br):
    """The LOCKING axis: computed overflow-y of html and body (the retired cut locked scroll here;
    body's baseline overflow-x:hidden is a horizontal-scroll guard, not the lock, so it is skipped)."""
    return br.evaluate(
        "(()=>{const h=getComputedStyle(document.documentElement),"
        "b=getComputedStyle(document.body);"
        "return {html_y:h.overflowY, body_y:b.overflowY};})()"
    )


def overflow_free(ov):
    return ov and ov.get("html_y") not in ("hidden", "clip") \
        and ov.get("body_y") not in ("hidden", "clip")


if not chrome_available() or QUIZ_WORK_ID is None or TOKEN_ARM_ON is None or ANY_SERIES is None:
    reason = ("chrome absent" if not chrome_available()
              else "no quiz works" if QUIZ_WORK_ID is None
              else "arm-on token not found" if TOKEN_ARM_ON is None
              else "no series in bake")
    for r in BROWSER_ROWS + CH_ROWS + SND_ROWS:
        skip(r, f"{reason} — browser rows pinned SKIP")
else:
    with serve(TMP) as base:

        # ---- CMP1: question card owns keys ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            card_open = open_quiz_card(br)
            scroll_y_before = br.evaluate("window.scrollY")
            in_view_before = br.evaluate(IN_VIEW)
            br.key("ArrowDown")
            br.key("PageDown")
            br.sleep(0.9)
            scroll_y_after = br.evaluate("window.scrollY")
            in_view_after = br.evaluate(IN_VIEW)
            card_still = br.evaluate("document.querySelector('#ex-quiz-card')?.classList.contains('show')")
            scroll_moved = abs((scroll_y_after or 0) - (scroll_y_before or 0)) > 2
            view_changed = in_view_after != in_view_before
            check(
                BROWSER_ROWS[0],
                card_open and not scroll_moved and not view_changed and card_still,
                f"card_open={card_open} scrollY={scroll_y_before}→{scroll_y_after} "
                f"scroll_moved={scroll_moved} in_view={in_view_before}→{in_view_after} "
                f"card_still={card_still}",
            )

        # ---- CMP2: gift card owns keys ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            gift_open = open_gift_card(br)
            scroll_y_before = br.evaluate("window.scrollY")
            in_view_before = br.evaluate(IN_VIEW)
            br.key("ArrowDown")
            br.key("PageDown")
            br.sleep(0.9)
            scroll_y_after = br.evaluate("window.scrollY")
            in_view_after = br.evaluate(IN_VIEW)
            gift_still = br.evaluate("document.querySelector('#ex-gift-card')?.classList.contains('show')")
            scroll_moved = abs((scroll_y_after or 0) - (scroll_y_before or 0)) > 2
            view_changed = in_view_after != in_view_before
            check(
                BROWSER_ROWS[1],
                gift_open and not scroll_moved and not view_changed and gift_still,
                f"gift_open={gift_open} scrollY={scroll_y_before}→{scroll_y_after} "
                f"scroll_moved={scroll_moved} in_view={in_view_before}→{in_view_after} "
                f"gift_still={gift_still}",
            )

        # ---- CMP3: side room already holds keys ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            side_open = open_side_room(br)
            scroll_y_before = br.evaluate("window.scrollY")
            br.key("ArrowDown")
            br.sleep(0.6)
            scroll_y_after = br.evaluate("window.scrollY")
            room_still = br.evaluate("document.body.classList.contains('ex-side')")
            scroll_moved = abs((scroll_y_after or 0) - (scroll_y_before or 0)) > 2
            check(
                BROWSER_ROWS[2],
                side_open and not scroll_moved and room_still,
                f"side_open={side_open} scrollY={scroll_y_before}→{scroll_y_after} "
                f"scroll_moved={scroll_moved} room_still={room_still}",
            )

        # ---- CMP4: gift card over a DEEP frame — last face leaves into fresh-measured room
        # (the pick frame sits at scrollY=0 where both orientations centre trivially, so the
        #  defect only shows on a frame deeper in the arc — frame index 4 here)
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            br.evaluate(
                "(()=>{const f=document.querySelectorAll('.exh-frame')[4];"
                "if(f)f.scrollIntoView({behavior:'instant'});})()")
            br.sleep(0.8)
            target_id = br.evaluate(
                "(document.querySelectorAll('.exh-frame')[4]||{dataset:{}}).dataset.id")
            br.evaluate(
                "document.querySelectorAll('.exh-frame img.work')[4]"
                ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.6)
            gift_open = br.evaluate(
                "document.querySelector('#ex-gift-card')?.classList.contains('show')")
            br.set_viewport(900, 1280)
            br.sleep(0.4)
            br.key("Escape")
            br.sleep(0.15)
            offset_015 = frame_centre_offset(br, target_id) if target_id else 9999
            scroll_y_015 = br.evaluate("window.scrollY")
            br.sleep(0.5)
            scroll_y_065 = br.evaluate("window.scrollY")
            scroll_stable = abs((scroll_y_065 or 0) - (scroll_y_015 or 0)) <= 2
            check(
                BROWSER_ROWS[3],
                gift_open and offset_015 <= EPSILON and scroll_stable,
                f"gift_open={gift_open} target={target_id} offset_px={offset_015:.1f} "
                f"(want≤{EPSILON}) scroll_y @+0.15s={scroll_y_015} @+0.65s={scroll_y_065} "
                f"stable={scroll_stable}",
            )

        # ---- CMP5: the side room closes after a rotation — the walk re-centres (Back restore)
        # The room is a face too; a rotation under it must be honoured when the visitor returns.
        # Depth hunted honestly: prefer a series member sitting at arc index ≥2 (a deep frame);
        # with none in this bake the frame-0 member still fences the restore path.
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            room_open = open_side_room(br)
            if room_open:
                br.key("Escape")               # back out — we may find a deeper member below
                br.sleep(1.0)
                members_union = set()
                for s in SERIES:
                    members_union |= {str(m) for m in s["members"]}
                frames = json.loads(br.evaluate(
                    "JSON.stringify([...document.querySelectorAll('.exh-frame')]"
                    ".map(f=>f.dataset.id))") or "[]")
                deep = next(((i, fid) for i, fid in enumerate(frames)
                             if i >= 2 and fid in members_union), None)
                member_id = None
                if deep:
                    idx, member_id = deep
                    br.evaluate(
                        "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                        "if(f)f.scrollIntoView({behavior:'instant'});})()" % member_id)
                    br.sleep(0.8)
                    br.click(".ex-series", settle=1.5)
                else:
                    member_id = frames[0] if frames else None
                    br.click(".ex-series", settle=1.5) if br.evaluate(
                        "!!document.querySelector('.ex-series')") else open_side_room(br)
                reopened = br.evaluate("document.body.classList.contains('ex-side')")
                br.set_viewport(900, 1280)
                br.sleep(0.5)
                br.key("Escape")               # Esc = history.back → the restore path
                br.sleep(1.0)
                closed = br.evaluate("!document.body.classList.contains('ex-side')")
                offset_r = frame_centre_offset(br, member_id) if member_id else 9999
                check(
                    BROWSER_ROWS[4],
                    reopened and closed and offset_r <= EPSILON,
                    f"deep={deep} reopened={reopened} closed={closed} member={member_id} "
                    f"offset_px={offset_r:.1f} (want≤{EPSILON})",
                )
            else:
                check(BROWSER_ROWS[4], False, "side room did not open")

        # ---- CMP6: card is viewport-honest (DEFAULT tempo — do not set ex-tempo) ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            # No tempo set for this row (default); pick = second quiz work so the chip appears
            _cmp6_pick = (str(quiz_works[1]["id"]) if len(quiz_works) > 1
                          else str(quiz_works[0]["id"]) if quiz_works else None)
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate(f"localStorage.setItem('ex.visitor', {json.dumps(TOKEN_ARM_ON)})")
            if _cmp6_pick:
                br.evaluate(
                    "localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
                    % (json.dumps(EX_VER), json.dumps(str(_cmp6_pick)))
                )
            # A definitive server verdict (a miss) so the tapped choice LOCKS. Without a stubbed
            # verdict, a tap now correctly re-opens the choice on the reach-failure path
            # (EX-QUIZ-REPLY / INV-138: an edge that never returns a verdict burns nothing), so the
            # lock this row asserts is the lock after a real answer, not after an unanswered blip.
            # inject runs on documents created after the call, so it must precede the reload.
            br.inject(
                "(function(){const _f=window.fetch;"
                "window.fetch=function(u,o){"
                "if(String(u).includes('/api/quiz')){"
                "return Promise.resolve(new Response(JSON.stringify({ok:false}),"
                "{status:200,headers:{'Content-Type':'application/json'}}));}"
                "return _f.apply(this,arguments);};})();"
            )
            br.reload()
            br.sleep(1.5)
            card_open = open_quiz_card(br)
            # record stamp before any viewport change
            stamp_before = br.evaluate("localStorage.getItem('ex.quizshown')")
            # change viewport while card is open
            br.set_viewport(900, 1280)
            br.sleep(0.4)
            # check card centring (both axes)
            inner_rect = br.evaluate(
                "(()=>{const c=document.querySelector('.quiz-inner');"
                "if(!c)return null;"
                "const r=c.getBoundingClientRect();"
                "return {cx:r.left+r.width/2,cy:r.top+r.height/2};})()"
            )
            vp_cx = br.evaluate("innerWidth/2")
            vp_cy = br.evaluate("innerHeight/2")
            opts_count = br.evaluate("document.querySelectorAll('.quiz-opt').length")
            stamp_after_rotation = br.evaluate("localStorage.getItem('ex.quizshown')")
            centred_x = abs((inner_rect or {}).get("cx", 9999) - (vp_cx or 0)) <= EPSILON if inner_rect else False
            centred_y = abs((inner_rect or {}).get("cy", 9999) - (vp_cy or 0)) <= EPSILON if inner_rect else False
            stamp_unchanged = stamp_before == stamp_after_rotation
            # now tap one option; then rotate back and check disabled
            br.click(".quiz-opt", settle=0.3)
            br.set_viewport(1280, 900)
            br.sleep(0.3)
            opts_disabled = br.evaluate(
                "[...document.querySelectorAll('.quiz-opt')].every(b=>b.disabled)"
            )
            check(
                BROWSER_ROWS[5],
                card_open and centred_x and centred_y and opts_count == 4
                and stamp_unchanged and opts_disabled,
                f"card_open={card_open} inner={inner_rect} vp=({vp_cx},{vp_cy}) "
                f"centred_x={centred_x} centred_y={centred_y} opts={opts_count} "
                f"stamp_unchanged={stamp_unchanged} opts_disabled={opts_disabled}",
            )

        # ---- CMP7: side room covers walk's chrome; sound player stays above ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            side_open = open_side_room(br)
            results_cmp7 = {}
            if side_open:
                # share button: elementFromPoint at its centre must be inside #ex-side
                share_rect = br.evaluate(
                    "(()=>{const b=document.querySelector('.ex-share');"
                    "if(!b)return null;const r=b.getBoundingClientRect();"
                    "return {cx:r.left+r.width/2,cy:r.top+r.height/2};})()"
                )
                if share_rect:
                    cx, cy = share_rect["cx"], share_rect["cy"]
                    share_probe = br.evaluate(
                        f"(()=>{{const el=document.elementFromPoint({cx},{cy});"
                        f"return el?el.closest('#ex-side')!==null:false;}})()"
                    )
                    results_cmp7["share_covered"] = share_probe
                else:
                    results_cmp7["share_covered"] = True  # hidden entirely = covered

                # caption zone: covered by #ex-side
                cap_rect = br.evaluate(
                    "(()=>{const c=document.querySelector('.exh-capzone');"
                    "if(!c)return null;const r=c.getBoundingClientRect();"
                    "return {cx:r.left+r.width/2,cy:r.top+r.height/2};})()"
                )
                if cap_rect:
                    cx, cy = cap_rect["cx"], cap_rect["cy"]
                    cap_probe = br.evaluate(
                        f"(()=>{{const el=document.elementFromPoint({cx},{cy});"
                        f"return el?el.closest('#ex-side')!==null:false;}})()"
                    )
                    results_cmp7["cap_covered"] = cap_probe

                # counter: covered by #ex-side
                ctr_rect = br.evaluate(
                    "(()=>{const c=document.querySelector('.exh-counter');"
                    "if(!c)return null;const r=c.getBoundingClientRect();"
                    "return {cx:r.left+r.width/2,cy:r.top+r.height/2};})()"
                )
                if ctr_rect:
                    cx, cy = ctr_rect["cx"], ctr_rect["cy"]
                    ctr_probe = br.evaluate(
                        f"(()=>{{const el=document.elementFromPoint({cx},{cy});"
                        f"return el?el.closest('#ex-side')!==null:false;}})()"
                    )
                    results_cmp7["counter_covered"] = ctr_probe

                # sound player: elementFromPoint at its button centre must be INSIDE #ex-sound;
                # absent in the synthetic fixture (no sound_url) → treat as not applicable (pass)
                sound_rect = br.evaluate(
                    "(()=>{const s=document.querySelector('#ex-sound');"
                    "if(!s)return null;const r=s.getBoundingClientRect();"
                    "return {cx:r.left+r.width/2,cy:r.top+r.height/2};})()"
                )
                if sound_rect:
                    cx, cy = sound_rect["cx"], sound_rect["cy"]
                    sound_probe = br.evaluate(
                        f"(()=>{{const el=document.elementFromPoint({cx},{cy});"
                        f"return el?el.closest('#ex-sound')!==null:false;}})()"
                    )
                    results_cmp7["sound_reachable"] = sound_probe
                else:
                    results_cmp7["sound_reachable"] = True   # absent = not a coverage point here

            check(
                BROWSER_ROWS[6],
                side_open
                and results_cmp7.get("share_covered", False)
                and results_cmp7.get("cap_covered", False)
                and results_cmp7.get("counter_covered", False)
                and results_cmp7.get("sound_reachable", False),
                f"side_open={side_open} {results_cmp7}",
            )

        # ---- CMP8: no question chip/card reachable in the side room ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            # set up walk with quiz work as pick; open side room from a series member
            # (the pick is the quiz work; the series member is different — use any_series)
            s = ANY_SERIES
            pick_id = s["members"][0]
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo', '0.3')")
            br.evaluate(f"localStorage.setItem('ex.visitor', {json.dumps(TOKEN_ARM_ON)})")
            br.evaluate(
                "localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
                % (json.dumps(EX_VER), json.dumps(str(pick_id)))
            )
            br.reload()
            br.sleep(1.2)
            # scroll to member frame so series pill appears
            br.evaluate(
                "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                "if(f)f.scrollIntoView({behavior:'instant'});})()" % str(pick_id)
            )
            br.sleep(0.5)
            br.click(".ex-series", settle=1.5)
            side_open = br.evaluate("document.body.classList.contains('ex-side')")
            # check all quiz chips are unreachable (elementFromPoint on each chip centre
            # must not land on the chip itself)
            chips_unreachable = br.evaluate(
                "(()=>{const chips=[...document.querySelectorAll('.ex-quiz-chip')];"
                "if(!chips.length)return true;"
                "return chips.every(chip=>{"
                "const r=chip.getBoundingClientRect();"
                "const cx=r.left+r.width/2,cy=r.top+r.height/2;"
                "const el=document.elementFromPoint(cx,cy);"
                "return !el||el.closest('.ex-quiz-chip')===null;"
                "})})()"
            )
            card_hidden = br.evaluate(
                "(()=>{const c=document.querySelector('#ex-quiz-card');"
                "return !c||c.hidden||getComputedStyle(c).display==='none';})()"
            )
            check(
                BROWSER_ROWS[7],
                side_open and chips_unreachable and card_hidden,
                f"side_open={side_open} chips_unreachable={chips_unreachable} "
                f"card_hidden={card_hidden}",
            )

        # ---- CMP9: lifted print re-centres on rotation ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            if POLAROID_SERIES is None:
                skip(BROWSER_ROWS[8], "no polaroid series in bake")
            else:
                side_open = open_side_room(br, series=POLAROID_SERIES)
                # click the first print to lift it
                br.click(".exs-print", settle=0.5)
                lifted = br.evaluate("!!document.querySelector('.exs-print.lift')")
                # change viewport
                br.set_viewport(900, 1280)
                br.sleep(0.5)
                # measure lifted print centre vs new viewport centre
                lift_rect = br.evaluate(
                    "(()=>{const p=document.querySelector('.exs-print.lift');"
                    "if(!p)return null;"
                    "const r=p.getBoundingClientRect();"
                    "return {cx:r.left+r.width/2,cy:r.top+r.height/2};})()"
                )
                vp_cx = br.evaluate("innerWidth/2")
                vp_cy = br.evaluate("innerHeight/2")
                if lift_rect:
                    off_x = abs(lift_rect["cx"] - (vp_cx or 0))
                    off_y = abs(lift_rect["cy"] - (vp_cy or 0))
                    centred = off_x <= EPSILON and off_y <= EPSILON
                else:
                    off_x = off_y = 9999
                    centred = False
                check(
                    BROWSER_ROWS[8],
                    side_open and lifted and centred,
                    f"side_open={side_open} lifted={lifted} "
                    f"lift_centre=({(lift_rect or {}).get('cx', '?')},{(lift_rect or {}).get('cy', '?')}) "
                    f"vp_centre=({vp_cx},{vp_cy}) "
                    f"off=({off_x:.1f}px,{off_y:.1f}px) (want≤{EPSILON})",
                )

        # ---- CMP10: closing screen is a stop ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo', '0.2')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=0.1)
            br.sleep(1.2)
            # scroll to the closing screen
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.8)
            # change viewport
            br.set_viewport(900, 1280)
            br.sleep(1.2)
            # the closing screen must still cover the viewport centre
            fin_covers_centre = br.evaluate(
                "(()=>{const f=document.getElementById('exh-fin');"
                "if(!f)return false;"
                "const r=f.getBoundingClientRect();"
                "const cx=innerWidth/2,cy=innerHeight/2;"
                "return r.left<=cx&&r.right>=cx&&r.top<=cy&&r.bottom>=cy;})()"
            )
            check(
                BROWSER_ROWS[9],
                fin_covers_centre,
                f"fin_covers_viewport_centre={fin_covers_centre}",
            )

        # ================= EX-CHROME / INV-70 — one page shape for the browser =================

        # ---- CH1: the page root stays scrollable under EVERY face (no overflow cut) ----
        faces = {}
        # cold door — the browser's own moment; still no root overflow cut
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.reload()
            br.sleep(1.2)
            faces["cold_door"] = {
                "stands": br.evaluate("document.body.classList.contains('ex-door')"),
                "ov": root_overflow_vertical(br)}
        # re-opened door standing over the built walk — tall doc + held place
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            door_stands = reach_reopened_door(br)
            ov_door = root_overflow_vertical(br)
            tall = br.evaluate("document.documentElement.scrollHeight > innerHeight + 100")
            sy0 = br.evaluate("window.scrollY")
            br.sleep(0.4)
            sy1 = br.evaluate("window.scrollY")
            faces["reopened_door"] = {"stands": door_stands, "ov": ov_door, "tall": tall,
                                      "held": abs((sy1 or 0) - (sy0 or 0)) <= 2}
        # side room standing
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            faces["side"] = {"stands": open_side_room(br),
                             "ov": root_overflow_vertical(br)}
        # quiz card standing
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            faces["quiz"] = {"stands": open_quiz_card(br),
                             "ov": root_overflow_vertical(br)}
        # gift card standing
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            faces["gift"] = {"stands": open_gift_card(br),
                             "ov": root_overflow_vertical(br)}

        all_free = all(overflow_free(f["ov"]) for f in faces.values())
        all_stand = all(f["stands"] for f in faces.values())
        reopen = faces["reopened_door"]
        check(
            CH_ROWS[0],
            all_stand and all_free and reopen["tall"] and reopen["held"],
            f"all_stand={all_stand} all_overflow_free={all_free} "
            f"reopened_tall={reopen['tall']} reopened_held={reopen['held']} :: {faces}",
        )

        # ---- CH2: the standing (re-opened) door rests the walk's input ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            door_stands = reach_reopened_door(br)
            sy_before = br.evaluate("window.scrollY")
            # a REAL wheel tick over the door
            br.wheel(delta_y=600)
            br.sleep(0.4)
            sy_wheel = br.evaluate("window.scrollY")
            # a REAL touch swipe (finger up = advance) — rested behind the veil / guard-corrected
            br.swipe(-300)
            br.sleep(0.4)
            sy_swipe = br.evaluate("window.scrollY")
            wheel_held = abs((sy_wheel or 0) - (sy_before or 0)) <= 2
            swipe_held = abs((sy_swipe or 0) - (sy_before or 0)) <= 2
            # the door's own controls stay live — a window answers a click → the walk opens
            answered = False
            if br.evaluate("!!document.querySelector('.exd-window')"):
                br.click(".exd-window:nth-child(1)", settle=1.4)
                answered = br.evaluate(
                    "document.documentElement.classList.contains('ex-walk') && "
                    "!document.body.classList.contains('ex-door')")
            check(
                CH_ROWS[1],
                door_stands and wheel_held and swipe_held and answered,
                f"door_stands={door_stands} scrollY base={sy_before} "
                f"wheel={sy_wheel}(held={wheel_held}) swipe={sy_swipe}(held={swipe_held}) "
                f"window_answered={answered}",
            )

        # ---- CH3: the guard snaps back foreign scroll (a dragged scrollbar stand-in) ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            card_open = open_quiz_card(br)          # a face stands over a scrolled walk
            held = br.evaluate("window.scrollY") or 0
            # a scroll the house did NOT write (synthetic scrollTo standing in for a scrollbar drag)
            br.evaluate("window.scrollTo(0, %d)" % (held + 450))
            corrected = False
            snapped_y = None
            for _ in range(20):                     # poll ≤ ~1s for the correction
                br.sleep(0.05)
                snapped_y = br.evaluate("window.scrollY") or 0
                if abs(snapped_y - held) <= 2:
                    corrected = True
                    break
            check(
                CH_ROWS[2],
                card_open and corrected,
                f"card_open={card_open} held={held} after_foreign_scroll→{snapped_y} "
                f"corrected={corrected}",
            )

        # ---- CH4: the house's OWN writes pass the guard (ceremony centre + Back/leave re-centre) ----
        # Part A — the door ceremony lands the picked work centred (the guard must not fight the glide).
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo', '0.2')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=1.4)
            first_id = br.evaluate(
                "(document.querySelectorAll('.exh-frame')[0]||{dataset:{}}).dataset.id")
            ceremony_off = frame_centre_offset(br, first_id) if first_id else 9999
        # Part B — a face over a DEEP frame leaves into a fresh-measured room after a rotation:
        # closeGift → recentreUnder writes scrollY to the frame's NEW centre; the guard, which froze
        # guardHold at the pre-rotation place, must NOT snap that house write back (mirrors CMP4).
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            br.evaluate(
                "(()=>{const f=document.querySelectorAll('.exh-frame')[4];"
                "if(f)f.scrollIntoView({behavior:'instant'});})()")
            br.sleep(0.8)
            deep_id = br.evaluate(
                "(document.querySelectorAll('.exh-frame')[4]||{dataset:{}}).dataset.id")
            br.evaluate(
                "document.querySelectorAll('.exh-frame img.work')[4]"
                ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.6)
            gift_up = br.evaluate("document.querySelector('#ex-gift-card')?.classList.contains('show')")
            br.set_viewport(900, 1280)
            br.sleep(0.4)
            br.key("Escape")
            br.sleep(0.15)
            leave_off_015 = frame_centre_offset(br, deep_id) if deep_id else 9999
            br.sleep(0.6)
            leave_off_075 = frame_centre_offset(br, deep_id) if deep_id else 9999
            settled = abs(leave_off_075 - leave_off_015) <= 2  # the guard did not drag it afterward
        check(
            CH_ROWS[3],
            first_id and ceremony_off <= EPSILON
            and gift_up and leave_off_075 <= EPSILON and settled,
            f"ceremony_first={first_id} centred_off={ceremony_off:.1f} gift_up={gift_up} "
            f"deep={deep_id} leave_off @+.15s={leave_off_015:.1f} @+.75s={leave_off_075:.1f} "
            f"settled={settled} (want≤{EPSILON})",
        )

        # ---- CH5: the scrollbar hides gutter-stable (client width identical open↔close) ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            setup_walk(br)
            br.reload()
            br.sleep(1.2)
            cw_before = br.evaluate("document.documentElement.clientWidth")
            q_open = open_quiz_card(br)
            cw_open = br.evaluate("document.documentElement.clientWidth")
            br.key("Escape")
            br.sleep(0.6)
            cw_after = br.evaluate("document.documentElement.clientWidth")
            stable = cw_before == cw_open == cw_after
            check(
                CH_ROWS[4],
                q_open and stable,
                f"card_open={q_open} clientWidth before={cw_before} open={cw_open} "
                f"after={cw_after} stable={stable}",
            )

        # ---- CH6: the face's OWN scroll survives the rest (the side room's lane scrolls native) ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            if LANE_SERIES is None:
                skip(CH_ROWS[5], "no lane series in bake")
            else:
                side_open = open_side_room(br, series=LANE_SERIES)
                lane = br.evaluate(
                    "(()=>{const l=document.querySelector('.exs-stage.lane');"
                    "if(!l)return null;const r=l.getBoundingClientRect();"
                    "return {sl:l.scrollLeft, sw:l.scrollWidth, cw:l.clientWidth,"
                    "cx:r.left+r.width/2, cy:r.top+r.height/2};})()"
                )
                if not lane or lane["sw"] <= lane["cw"] + 4:
                    skip(CH_ROWS[5],
                         f"lane not horizontally scrollable (sw={lane and lane['sw']} "
                         f"cw={lane and lane['cw']}) — carve-out untestable here")
                else:
                    # a REAL horizontal wheel over the lane — the carve-out lets it scroll the lane
                    # natively (the lane is overflow-x:auto; deltaX drives its own scrollLeft)
                    br._cmd("Input.dispatchMouseEvent", type="mouseWheel",
                            x=int(lane["cx"]), y=int(lane["cy"]),
                            deltaX=600, deltaY=0, buttons=0, button="none", clickCount=0)
                    br.sleep(0.4)
                    sl_after = br.evaluate(
                        "document.querySelector('.exs-stage.lane').scrollLeft")
                    moved = (sl_after or 0) > (lane["sl"] or 0) + 2
                    check(
                        CH_ROWS[5],
                        side_open and moved,
                        f"side_open={side_open} lane_scrollLeft {lane['sl']}→{sl_after} "
                        f"moved={moved} (sw={lane['sw']} cw={lane['cw']})",
                    )

        # ---- CH7: the guard HOLDS under a resting finger (a standing finger is not input rest) ----
        # His 2026-07-10 phone find: in the side room, a finger left resting on the glass made the
        # WHOLE screen tremble. An active touch drags the page a few px (iOS rubber-band); the guard,
        # correcting mid-touch, snapped it back every frame — a per-frame fight = the shimmer. The
        # guard must HOLD while a touch is DOWN and settle ONCE on lift. (The rubber-band drag is
        # stood in for by a foreign scrollTo during the held touch, as CH3 stands in for a scrollbar.)
        with Browser(width=390, height=844) as br:
            br.touch(True)
            br.navigate(base + "/")
            side_open = open_side_room(br)          # a face stands over the walk
            held = br.evaluate("window.scrollY") or 0
            maxs = br.evaluate("document.documentElement.scrollHeight - innerHeight") or 0
            nudge = held + 30 if held + 30 <= maxs else max(0, held - 30)
            # record only the HOUSE's own scrollTo (the guard), tagged by whether a finger is down
            br.evaluate(
                "(()=>{window.__gw=[];window.__holding=false;"
                "window.__native=window.scrollTo.bind(window);const _st=window.__native;"
                "window.scrollTo=function(x,y){window.__gw.push({y:y,hold:window.__holding});"
                "return _st(x,y);};})()")
            x, y0 = br.width // 2, br.height // 2
            br._cmd("Input.dispatchTouchEvent", type="touchStart",
                    touchPoints=[{"x": x, "y": y0}])
            br.evaluate("window.__holding=true")
            # ~1s of a finger at rest: tiny ±6px drift + the rubber-band drag it causes (foreign scroll)
            for i in range(10):
                yy = y0 + (6 if i % 2 else -6)
                br._cmd("Input.dispatchTouchEvent", type="touchMove",
                        touchPoints=[{"x": x, "y": yy}])
                br.evaluate("window.__native(0, %d)" % nudge)   # iOS rubber-band stand-in
                br.sleep(0.05)
            writes_hold = br.evaluate(
                "window.__gw.filter(w=>w.hold && Math.abs(w.y-%d)<=2).length" % held)
            br.evaluate("window.__holding=false")
            br._cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])
            br.sleep(0.3)
            settle = br.evaluate(
                "window.__gw.filter(w=>!w.hold && Math.abs(w.y-%d)<=2).length" % held)
            final_off = abs((br.evaluate("window.scrollY") or 0) - held)
            check(
                CH_ROWS[6],
                side_open and writes_hold == 0 and settle >= 1 and final_off <= 2,
                f"side_open={side_open} guard_writes_during_hold={writes_hold} (want 0) "
                f"settle_after_lift={settle} (want ≥1) final_off={final_off} held={held}",
            )

        # ---- CH8: a moving finger cannot drag the walk from under a face (source-eating) ----
        # A slow REAL drag on a translucent part of a standing face — (a) the question card's scrim,
        # (b) the side room's backdrop OFF the lane — must write ZERO page scroll while held and leave
        # NO jerk on lift: the face eats the drag at the source, so the guard has nothing to settle.
        # (The 2026-07-11 field find: a drag on the quiz scrim slid the walk hundreds of px behind it.)
        DRIFT_EPS = 5
        with Browser(width=390, height=844) as br:
            br.touch(True)
            br.navigate(base + "/")
            # (a) the question card's translucent scrim (y=150 sits above the centred .quiz-inner).
            # The chip is JS-clicked (native hit-testing flakes on the mobile caption layout); the
            # chip lives on the browser's CHOSEN quiz work, discovered after reload.
            setup_walk(br)
            br.reload()
            br.sleep(1.3)
            chosen = get_quiz_work_id(br)
            if chosen:
                br.evaluate(
                    "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                    "if(f)f.scrollIntoView({behavior:'instant'});})()" % str(chosen))
                br.sleep(0.8)
                br.evaluate("(()=>{const c=document.querySelector('.ex-quiz-chip');if(c)c.click();})()")
                br.sleep(0.6)
            q_open = br.evaluate(
                "document.querySelector('#ex-quiz-card')?.classList.contains('show')")
            scrim_tag = br.evaluate(
                "(()=>{const e=document.elementFromPoint(195,150);"
                "return e&&e.closest('#ex-quiz-card')?e.tagName+'.'+e.className:null;})()")
            _, drift_a, jerk_a = slow_drag(br, 195, 150, 0, -300)
            # (b) the side room's backdrop, off the lane — found by scan (a non-scrollable #ex-side pt)
            side_open = open_side_room(br)
            bpt = br.evaluate(
                "(()=>{const x=Math.round(innerWidth/2);"
                "for(let y=Math.round(innerHeight*0.85);y>innerHeight*0.12;y-=18){"
                "const el=document.elementFromPoint(x,y);"
                "if(el&&el.closest&&el.closest('#ex-side')&&!el.closest('.exs-stage.lane')"
                "&&!el.closest('input,textarea,button,a,[role=button]')"
                "&&el.scrollHeight<=el.clientHeight+1)"
                "return {x:x,y:y,tag:el.tagName+'.'+el.className};}return null;})()")
            if not bpt:
                skip(CH_ROWS[7], "no off-lane backdrop point found in the side room")
            else:
                _, drift_b, jerk_b = slow_drag(br, bpt["x"], bpt["y"], 0, -300)
                check(
                    CH_ROWS[7],
                    q_open and side_open
                    and drift_a <= DRIFT_EPS and not jerk_a
                    and drift_b <= DRIFT_EPS and not jerk_b,
                    f"quiz_open={q_open} scrim={scrim_tag} scrim_drift={drift_a} jerk={jerk_a} | "
                    f"side_open={side_open} backdrop={bpt['tag']}@{bpt['y']} "
                    f"back_drift={drift_b} jerk={jerk_b} (eps={DRIFT_EPS})",
                )

        # ---- CH9: the narrowed carve-out keeps the lane alive, axis-true ----
        # With the side room standing: a drag ALONG the polaroid lane still scrolls it natively
        # (scrollLeft moves — the face's own scroll survives the narrowing); a drag ACROSS it
        # (vertical, ON the lane) moves neither the lane nor the page (the leftover never chains).
        with Browser(width=390, height=844) as br:
            br.touch(True)
            br.navigate(base + "/")
            if LANE_SERIES is None:
                skip(CH_ROWS[8], "no lane series in bake")
            else:
                side_open = open_side_room(br, series=LANE_SERIES)
                lane = br.evaluate(
                    "(()=>{const l=document.querySelector('.exs-stage.lane');"
                    "if(!l)return null;const r=l.getBoundingClientRect();"
                    "return {sl:l.scrollLeft, sw:l.scrollWidth, cw:l.clientWidth,"
                    "cx:r.left+r.width/2, cy:r.top+r.height/2};})()")
                if not lane or lane["sw"] <= lane["cw"] + 4:
                    skip(CH_ROWS[8],
                         f"lane not horizontally scrollable (sw={lane and lane['sw']} "
                         f"cw={lane and lane['cw']}) — axis-true carve-out untestable here")
                else:
                    cx, cy = int(lane["cx"]), int(lane["cy"])
                    # ALONG: a horizontal drag scrolls the lane natively (finger left → scrollLeft up)
                    sl0 = br.evaluate(
                        "document.querySelector('.exs-stage.lane').scrollLeft") or 0
                    slow_drag(br, cx, cy, -240, 0)
                    sl_along = br.evaluate(
                        "document.querySelector('.exs-stage.lane').scrollLeft") or 0
                    along_moved = sl_along > sl0 + 2
                    br.evaluate(
                        "document.querySelector('.exs-stage.lane').scrollLeft=%d" % sl0)
                    br.sleep(0.2)
                    # ACROSS: a vertical drag ON the lane moves neither the lane nor the page
                    sl_before = br.evaluate(
                        "document.querySelector('.exs-stage.lane').scrollLeft") or 0
                    _, page_drift, _ = slow_drag(br, cx, cy, 0, -300)
                    sl_after = br.evaluate(
                        "document.querySelector('.exs-stage.lane').scrollLeft") or 0
                    across_lane_moved = abs(sl_after - sl_before) > 2
                    check(
                        CH_ROWS[8],
                        side_open and along_moved
                        and not across_lane_moved and page_drift <= 5,
                        f"side_open={side_open} along scrollLeft {sl0}→{sl_along} "
                        f"moved={along_moved} | across lane {sl_before}→{sl_after} "
                        f"lane_moved={across_lane_moved} page_drift={page_drift} (want≤5)",
                    )

    # ============ EX-CHROME — the ambient audio player retracts under a covering face ============
    # The player is fixed at z-index 130 on document.body; nothing hid it, so it floated PRESSABLE over
    # the door, the side room, the gift card, and the question card. It now retracts (opacity:0;
    # pointer-events:none) under those four, scoped to their body/element state — NEVER html.ex-face,
    # because of the zoom exception (INV-77): while inspecting a picture the music stays reachable.
    # These rows run on TMP_SND (the sound-configured bake); the default fixture ships no audio.
    with serve(TMP_SND) as snd_base:
        # SND1 — under the (re-opened) door
        with Browser(width=1280, height=900) as br:
            br.navigate(snd_base + "/")
            door_stands = reach_reopened_door(br)
            retracted, snd = snd_retracted(br)
            check(SND_ROWS[0], door_stands and retracted,
                  f"door_stands={door_stands} snd={snd}")

        # SND2 — under the side room
        with Browser(width=1280, height=900) as br:
            br.navigate(snd_base + "/")
            side_open = open_side_room(br)
            retracted, snd = snd_retracted(br)
            check(SND_ROWS[1], side_open and retracted,
                  f"side_open={side_open} snd={snd}")

        # SND3 — under the gift / farewell card
        with Browser(width=1280, height=900) as br:
            br.navigate(snd_base + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.2)
            gift_open = open_gift_card(br)
            retracted, snd = snd_retracted(br)
            check(SND_ROWS[2], gift_open and retracted,
                  f"gift_open={gift_open} snd={snd}")

        # SND4 — under the question card (parity with the gift card — a compact cover)
        with Browser(width=1280, height=900) as br:
            br.navigate(snd_base + "/")
            setup_walk(br)
            br.reload(); br.sleep(1.2)
            card_open = open_quiz_card(br)
            retracted, snd = snd_retracted(br)
            check(SND_ROWS[3], card_open and retracted,
                  f"card_open={card_open} snd={snd}")

        # SND5 — INV-77 regression guard: during the ZOOM (over the walk) the player STAYS reachable
        with Browser(width=390, height=844) as br:
            br.navigate(snd_base + "/")
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo', '0.05')")
            br.reload(); br.sleep(1.1)
            br.click(".exd-window:nth-child(1)", settle=0.6)   # leave the door → the walk (no face)
            br.sleep(0.6)
            br.evaluate("var s=document.getElementById('ex-share'); if(s){s.dataset.share='999';}")
            fired = br.evaluate("(%s)('.exh-frame img.work')" % PINCH)  # pinch a walk work → zoom
            br.sleep(0.3)
            zoom_open = br.evaluate(ZOPEN)
            no_face = not br.evaluate(
                "document.body.classList.contains('ex-door') || "
                "document.body.classList.contains('ex-side')")
            pressable, snd = snd_pressable(br)
            check(SND_ROWS[4], fired == "ok" and zoom_open and no_face and pressable,
                  f"fired={fired!r} zoom_open={zoom_open} no_covering_face={no_face} snd={snd}")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_SND, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
