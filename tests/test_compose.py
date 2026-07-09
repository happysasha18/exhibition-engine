#!/usr/bin/env python3
"""EX-COMPOSE / INV-67 — The faces meet (the 2026-07-09 bug class closed as law).
Ten browser rows, one per engine SPEC "The faces meet" clause.

Ported from tlvphoto cbab752 tests/test_compose.py — adapted for the engine:
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
ANY_SERIES = SERIES[0] if SERIES else None

# ---------------------------------------------------------------- snippets shared with test_share.py / test_quiz_pick.py
IN_VIEW = ("(()=>{const f=[...document.querySelectorAll('.exh-frame')].find(f=>{"
           "const r=f.getBoundingClientRect();"
           "return r.top<innerHeight*0.5 && r.bottom>innerHeight*0.5;});"
           "return f?f.dataset.id:null;})()")

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
    br.evaluate(f"localStorage.setItem('tlv-tempo', {json.dumps(tempo)})")
    br.evaluate(f"localStorage.setItem('tlv.visitor', {json.dumps(TOKEN_ARM_ON)})")
    if pick:
        br.evaluate(
            "localStorage.setItem('tlv.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
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
    br.evaluate("localStorage.setItem('tlv-tempo', '0.3')")
    br.evaluate(f"localStorage.setItem('tlv.visitor', {json.dumps(TOKEN_ARM_ON)})")
    br.evaluate(
        "localStorage.setItem('tlv.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
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


if not chrome_available() or QUIZ_WORK_ID is None or TOKEN_ARM_ON is None or ANY_SERIES is None:
    reason = ("chrome absent" if not chrome_available()
              else "no quiz works" if QUIZ_WORK_ID is None
              else "arm-on token not found" if TOKEN_ARM_ON is None
              else "no series in bake")
    for r in BROWSER_ROWS:
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

        # ---- CMP6: card is viewport-honest (DEFAULT tempo — do not set tlv-tempo) ----
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            # No tempo set for this row (default); pick = second quiz work so the chip appears
            _cmp6_pick = (str(quiz_works[1]["id"]) if len(quiz_works) > 1
                          else str(quiz_works[0]["id"]) if quiz_works else None)
            br.evaluate("localStorage.clear(); sessionStorage.clear()")
            br.evaluate(f"localStorage.setItem('tlv.visitor', {json.dumps(TOKEN_ARM_ON)})")
            if _cmp6_pick:
                br.evaluate(
                    "localStorage.setItem('tlv.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
                    % (json.dumps(EX_VER), json.dumps(str(_cmp6_pick)))
                )
            br.reload()
            br.sleep(1.5)
            card_open = open_quiz_card(br)
            # record stamp before any viewport change
            stamp_before = br.evaluate("localStorage.getItem('tlv.quizshown')")
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
            stamp_after_rotation = br.evaluate("localStorage.getItem('tlv.quizshown')")
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
            br.evaluate("localStorage.setItem('tlv-tempo', '0.3')")
            br.evaluate(f"localStorage.setItem('tlv.visitor', {json.dumps(TOKEN_ARM_ON)})")
            br.evaluate(
                "localStorage.setItem('tlv.exhibition', JSON.stringify({v:%s, pick:%s, shown:999}))"
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
            br.evaluate("localStorage.setItem('tlv-tempo', '0.2')")
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

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
