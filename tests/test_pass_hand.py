#!/usr/bin/env python3
"""EX-HAND — the touch hand overlay's own file, its reach, its voice and its six verbs
(Requirement 38 criterion 9 — unit U1; Requirement 37's band and Requirement 38's six verbs and
chart law — unit U3).

U1's rows are the plumbing: its own file travels beside pass-layer.js in the bake (row 1), it
attaches on the walk's standing work and nowhere else Requirement 38 criterion 9 names outside
(rows 2/3/5), it steps off while the closer look (EX-ZOOM) covers the same picture and returns the
instant that layer clears (row 4), and the walk's own navigation is unchanged by its presence
(row 6).

U3 adds the whisper voice on `unfold`'s `tilt` handle (Requirement 37 case "the band", row 7) and
the six verbs of Requirement 38 criterion 1 — arrive, attend, lean, hold, release, strike — answered
by mouse and touch alike (rows 8-15), plus the chart law of criterion 4 (row 14) and a fresh proof
that the walk's own frame index still never moves under any of it (row 16).

Run: python tests/test_pass_hand.py
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
import build as _engine  # noqa: E402 — engine/build.py, already on sys.path via engine_build
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def wait_for(br, expr, timeout=6.0, step=0.05):
    """Poll a JS expression until it returns truthy (or the deadline) — no fixed-sleep races."""
    import time
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    return val


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_pass_hand_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# The sound tray (98-sound.js) stays hidden without a configured sound_url; the client reads
# config.json at RUNTIME, so the already-baked file can be edited in place — the exact road
# tests/test_share.py and tests/test_sound.py already use, no rebuild needed.
_cfg_path = TMP / "config.json"
_cfg = json.loads(_cfg_path.read_text(encoding="utf-8"))
_cfg["exhibition"]["sound_url"] = "/gallery/audio/ambient.m4a"
_cfg_path.write_text(json.dumps(_cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps(json.dumps({"v": VER, "pick": PICK, "shown": 10}))

ROWS = [
    "EX-HAND row1 the bake serves pass-hand.js beside pass-layer.js, byte-identical to "
    "strip_js_comments(apply_namespace(source)) — the same computation build.py:995 itself runs",
    "EX-HAND row2 a pointerdown on the walk's standing work (.exh-frame img.work) attaches the hand; "
    "report() names the work",
    "EX-HAND row3 the hand never attaches off the reach Requirement 38 criterion 9 names: the "
    "threshold window, the quiz chip, the share control, the sound tray's volume slider",
    "EX-HAND row4 the hand detaches while the closer look (EX-ZOOM) stands and re-attaches the "
    "instant it closes, with no fresh press",
    "EX-HAND row5 the hand never attaches inside the series side room (#ex-side)",
    "EX-HAND row6 the walk is unchanged: a tap-sized nudge (below the swipe floor) moves no frame, "
    "one wheel turn still advances exactly one",
    # ---- U3: Requirement 37's band, Requirement 38's six verbs and chart law ----------------------
    "EX-HAND row7 Requirement 37 c1 the band: while the hand is on the work, the breath's amplitude "
    "on tilt stays at or under R/32, R read off the instrument's own declared span and never typed in",
    "EX-HAND row8 Requirement 38 c1 both input kinds: twelve driven gestures (six mouse, six touch) "
    "each print the verb that fired, and all six verb names appear under each input kind",
    "EX-HAND row9 Requirement 38 c1 arrive: it fires on pointer entry, and the breath's phase after "
    "it differs from the phase before it",
    "EX-HAND row10 Requirement 38 c1 attend: the matter's free point moves toward the hand under an "
    "unpressed hover move and under a drag alike",
    "EX-HAND row11 Requirement 38 c1 lean: total travel on mix never exceeds R/8, one direction "
    "toward the source and the other into the construction, and the handle springs back to rest "
    "once the finger leaves",
    "EX-HAND row12 Requirement 38 c1 hold / c2: the breath's gain reads a quarter with the press "
    "held still and the voice keeps running; the run prints the stretch of the hand in the deep "
    "fold that the code itself measured",
    "EX-HAND row13 Requirement 38 c1 release: the ring plays, the return path is curved, and the "
    "afterglow mark is still readable once the resolve is finished",
    "EX-HAND row14 Requirement 38 c4 the chart law: the run prints the two unfold parameters the "
    "hand's position maps onto, both moving with their own axis, and no third handle moves under "
    "the hand",
    "EX-HAND row15 Requirement 38 c1 strike: it fires only on a single tap, where the page holds no "
    "prior claim on it",
    "EX-HAND row16 the walk's frame index is unchanged across all twelve gestures, and one wheel "
    "turn still advances exactly one frame",
]

# ---------------------------------------------------------------- row 1: the bake, a string proof
SRC = (ROOT / "engine" / "assets" / "pass-hand.js").read_text(encoding="utf-8")
expected = _engine.strip_js_comments(_engine.apply_namespace(SRC, _engine._NAMESPACE))
served_path = TMP / "pass-hand.js"
served = served_path.read_text(encoding="utf-8") if served_path.exists() else None
check(ROWS[0],
      served is not None and served == expected and (TMP / "pass-layer.js").exists(),
      f"pass-hand.js exists={served_path.exists()} pass-layer.js exists={(TMP / 'pass-layer.js').exists()} "
      f"bytes match={served == expected if served is not None else None}")

# ---------------------------------------------------------------- browser rows
HAND_READY = "!!(window.__exPass && window.__exPass.hand && window.__exPass.hand())"
HAND_REPORT = "(()=>window.__exPass.hand().report())()"
HAND_ATTACHED = "(()=>{const r=window.__exPass.hand().report();return r.attached!=null;})()"
HAND_DETACHED = "(()=>{const r=window.__exPass.hand().report();return r.attached==null;})()"


def hand_report(br):
    return json.loads(br.evaluate("JSON.stringify(%s)" % HAND_REPORT))


def pointerdown(br, selector):
    """Dispatch a synthetic touch pointerdown at `selector`'s own centre, targeting that element
    directly (works whether or not it is on-screen — the window/capture listener reads e.target,
    never a hit-test) — modeled on tests/test_a11y.py's PointerEvent rows (:968-981)."""
    return br.evaluate(
        "(sel=>{const el=document.querySelector(sel);if(!el)return false;"
        "const r=el.getBoundingClientRect();"
        "el.dispatchEvent(new PointerEvent('pointerdown',{pointerId:7,pointerType:'touch',"
        "clientX:r.left+r.width/2,clientY:r.top+r.height/2,isPrimary:true,bubbles:true,cancelable:true}));"
        "return true;})(%s)" % json.dumps(selector))


# a two-finger pinch-out on the standing work — EX-ZOOM's own opening road, dispatched exactly as
# tests/test_a11y.py's PINCH_WORK_ZOOM does (real TouchEvents, the only events that layer reads)
PINCH_OPEN_ZOOM = (
    "(()=>{const img=document.querySelector('.exh-frame img.work');if(!img)return false;"
    "const r=img.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;"
    "const mk=(i,x,y)=>new Touch({identifier:i,target:img,clientX:x,clientY:y});"
    "const fire=(t,ts)=>img.dispatchEvent(new TouchEvent(t,{touches:ts,targetTouches:ts,"
    "changedTouches:ts,bubbles:true,cancelable:true}));"
    "fire('touchstart',[mk(1,cx-20,cy),mk(2,cx+20,cy)]);"
    "fire('touchmove',[mk(1,cx-60,cy),mk(2,cx+60,cy)]);"
    "fire('touchend',[]);return true;})()"
)
ZOOM_UP = "(()=>{const z=document.getElementById('ex-zoom');return !!(z&&!z.hidden);})()"
ZOOM_GONE = "(()=>{const z=document.getElementById('ex-zoom');return !!(z&&z.hidden);})()"

# force-open a series room deterministically, exactly as tests/test_a11y.py's OPEN_SERIES does (an
# injected .ex-series chip through the real delegated openSide handler — never the random door pick)
OPEN_SERIES = (
    "(idx)=>{const c=document.getElementById('exh-cap');if(!c)return false;"
    "const b=document.createElement('button');b.className='ex-series';b.dataset.ser=String(idx);"
    "b.textContent='s';c.appendChild(b);b.click();return true;}"
)
ROOM_READY = ("(()=>{const s=document.getElementById('ex-side'),v=document.getElementById('ex-veil'),"
              "st=document.getElementById('exs-stage');if(!(s&&!s.hidden&&(!v||v.hidden)&&st))return false;"
              "const im=[...st.querySelectorAll('img')];"
              "return im.length>=1&&im.every(i=>i.complete&&i.naturalWidth>0);})()")

SECTIONS = "[...document.querySelectorAll('#ex-stage .exh-frame, #ex-stage .exh-fin')]"


def cur(br):
    """index of the section holding the viewport's centre line — the frame the eye is on (the same
    geometry read tests/test_glide.py uses, never an arithmetic guess)."""
    return br.evaluate(
        "(()=>{const s=%s;return s.findIndex(x=>{const r=x.getBoundingClientRect();"
        "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});})()" % SECTIONS)


def room(br, base, tempo="0.2"):
    """A stored walk straight into the room, diagnostics on — READY by condition, not a fixed sleep
    (tests/test_glide.py's own `room`, plus the diagnostics session key test_pass.py already reads)."""
    br.navigate(base + "/")
    br.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics: 'on'}))")
    br.reload()
    for _ in range(40):
        br.sleep(0.15)
        if br.evaluate("document.documentElement.classList.contains('ex-walk')"
                       "&&document.querySelectorAll('.exh-frame').length>0"
                       "&&scrollY===0"):
            break
    br.sleep(0.3)


# ---------------------------------------------------------------- U3 helpers: the six verbs
def fire(br, selector, kind_of_event, pointer_kind, nx=0.5, ny=0.5, pointer_id=9):
    """Dispatch one synthetic PointerEvent at a normalised (nx, ny) fraction of `selector`'s own
    box — mouse and touch alike are the same call with a different `pointer_kind`, modeled on
    tests/test_a11y.py's PointerEvent rows (:968-981)."""
    return br.evaluate(
        "(()=>{const el=document.querySelector(%s);if(!el)return false;"
        "const r=el.getBoundingClientRect();"
        "const x=r.left+r.width*%s, y=r.top+r.height*%s;"
        "el.dispatchEvent(new PointerEvent(%s,{pointerId:%s,pointerType:%s,"
        "clientX:x,clientY:y,isPrimary:true,bubbles:true,cancelable:true}));"
        "return true;})()"
        % (json.dumps(selector), nx, ny, json.dumps(kind_of_event), pointer_id, json.dumps(pointer_kind)))


def verb_expr(name):
    return "(()=>window.__exPass.hand().report().verb===%s)()" % json.dumps(name)


def wait_span(br, handle, timeout=6.0):
    """R, read through the hand's own `handleSpan("unfold", handle)` — the same two fields
    01a-pass.js:1358-1368's `passHandleSpan` reads, never typed into this test."""
    ok = wait_for(br, "(()=>!!window.__exPass.hand().handleSpan('unfold',%s))()" % json.dumps(handle),
                  timeout=timeout)
    if not ok:
        return None
    return json.loads(br.evaluate(
        "JSON.stringify(window.__exPass.hand().handleSpan('unfold',%s))" % json.dumps(handle)))


WORK = ".exh-frame img.work"


def drive_verbs(br, kind, pid):
    """The six verbs, driven in order (arrive, attend, lean, hold, release, strike) by one input
    kind, each confirmed on `report().verb` before the next gesture fires. Returns the six verb
    names actually read back, in the order they were confirmed."""
    log = []
    fire(br, WORK, "pointerover", kind, 0.5, 0.5, pid)
    wait_for(br, verb_expr("arrive"))
    log.append(hand_report(br)["verb"])

    fire(br, WORK, "pointermove", kind, 0.6, 0.5, pid)
    wait_for(br, verb_expr("attend"))
    log.append(hand_report(br)["verb"])

    fire(br, WORK, "pointerdown", kind, 0.5, 0.5, pid)
    fire(br, WORK, "pointermove", kind, 0.9, 0.5, pid)
    wait_for(br, verb_expr("lean"))
    log.append(hand_report(br)["verb"])

    wait_for(br, verb_expr("hold"), timeout=3.0)
    log.append(hand_report(br)["verb"])

    fire(br, WORK, "pointerup", kind, 0.9, 0.5, pid)
    wait_for(br, verb_expr("release"))
    log.append(hand_report(br)["verb"])

    fire(br, WORK, "pointerdown", kind, 0.5, 0.5, pid)
    fire(br, WORK, "pointerup", kind, 0.5, 0.5, pid)
    wait_for(br, verb_expr("strike"))
    log.append(hand_report(br)["verb"])
    return log


if not chrome_available():
    for r in ROWS[1:]:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # row 2 — attaches on the standing work
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            ready = wait_for(br, HAND_READY)
            before = hand_report(br) if ready else None
            work_id = br.evaluate("(()=>{const f=document.querySelector('.exh-frame');"
                                   "return f&&f.dataset.id;})()")
            pointerdown(br, ".exh-frame img.work")
            wait_for(br, HAND_ATTACHED)
            after = hand_report(br)
            check(ROWS[1],
                  bool(ready) and before and before.get("attached") is None
                  and after.get("attached") == work_id,
                  f"ready={ready} before={before} after={after} work_id={work_id!r}")

        # row 3 — absent off the four named surfaces
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            wait_for(br, "!!document.querySelector('.exsnd-vol')", timeout=6.0)
            br.evaluate(
                "(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                "const b=document.createElement('button');b.className='ex-quiz-chip';"
                "b.textContent='q';c.appendChild(b);})()")
            targets = ["#ex-door", ".ex-quiz-chip", "#ex-share", ".exsnd-vol"]
            found = [t for t in targets if br.evaluate("!!document.querySelector(%s)" % json.dumps(t))]
            bad = []
            for sel in targets:
                pointerdown(br, sel)
                rep = hand_report(br)
                if rep.get("attached") is not None:
                    bad.append((sel, rep))
            check(ROWS[2],
                  set(found) == set(targets) and not bad,
                  f"present={found} (want all 4) unexpected attachment on: {bad}")

        # row 4 — detaches under EX-ZOOM, re-attaches on close, no fresh press
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            work_id = br.evaluate("(()=>{const f=document.querySelector('.exh-frame');"
                                   "return f&&f.dataset.id;})()")
            pointerdown(br, ".exh-frame img.work")
            wait_for(br, HAND_ATTACHED)
            before_zoom = hand_report(br)
            br.evaluate(PINCH_OPEN_ZOOM)
            wait_for(br, ZOOM_UP)
            during_zoom = hand_report(br)
            # a press on the zoom's OWN picture while it stands — #ex-zoom covers the full viewport
            # (pointer-events:auto the instant it stands) so a real press never reaches the covered
            # work underneath; still driven here to prove the hand reads no attachment out of it.
            pointerdown(br, "#ex-zoom .exz-img")
            during_zoom_press = hand_report(br)
            br.key("Escape")
            wait_for(br, ZOOM_GONE)
            after_zoom = wait_for(br, HAND_ATTACHED) and hand_report(br)
            check(ROWS[3],
                  before_zoom.get("attached") == work_id and during_zoom.get("attached") is None
                  and during_zoom_press.get("attached") is None
                  and after_zoom and after_zoom.get("attached") == work_id,
                  f"before_zoom={before_zoom} during_zoom={during_zoom} "
                  f"during_zoom_press={during_zoom_press} after_zoom={after_zoom}")

        # row 5 — never inside the series side room
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            br.evaluate("(%s)(0)" % OPEN_SERIES)
            room_ready = wait_for(br, ROOM_READY, timeout=8.0)
            pointerdown(br, "#exs-stage img, #exs-stage .exs-print img")
            rep = hand_report(br)
            check(ROWS[4],
                  bool(room_ready) and rep.get("attached") is None,
                  f"room_ready={room_ready} report={rep}")

        # row 6 — the walk itself is unchanged. Touch and wheel are the two separate input
        # modalities the walk already tells apart (test_glide.py runs them the same way, never
        # together in one browser) — a tap-sized nudge is asked of a touch-emulated browser, a
        # wheel notch of a plain one.
        with Browser(width=1280, height=900) as br:
            br.touch(True)
            room(br, base, "0.2")
            idx0 = cur(br)
            br.swipe(-10)                  # a tap-sized nudge — below the swipe floor (test_glide.py)
            idx1 = cur(br)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            idxw0 = cur(br)
            br.wheel(delta_y=400)          # one notch — the established one-frame wheel unit
            br.sleep(0.5)
            idxw1 = cur(br)
        check(ROWS[5],
              idx1 == idx0 and idxw1 == idxw0 + 1,
              f"touch: before={idx0} after_nudge={idx1} (want {idx0}) — "
              f"wheel: before={idxw0} after={idxw1} (want {idxw0 + 1})")

        # row 7 — Requirement 37 c1, the band: the breath's amplitude on tilt never exceeds R/32
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            fire(br, WORK, "pointerover", "mouse")
            wait_for(br, verb_expr("arrive"))
            sp = wait_span(br, "tilt")
            R = (sp["hi"] - sp["lo"]) if sp else None
            bad = None
            for _ in range(8):
                amp = hand_report(br)["tilt"]["breathAmplitude"]
                if R is not None and amp > R / 32 + 1e-9:
                    bad = amp
                br.sleep(0.15)
            check(ROWS[6],
                  sp is not None and bad is None,
                  f"span={sp} R={R} R/32={None if R is None else R / 32} bad_amplitude={bad}")

        # row 8 — Requirement 38 c1, both input kinds: twelve driven gestures, six verbs each
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            mouse_log = drive_verbs(br, "mouse", 21)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            touch_log = drive_verbs(br, "touch", 31)
        print("\ntwelve driven gestures:")
        print(f"  mouse: {mouse_log}")
        print(f"  touch: {touch_log}")
        SIX_VERBS = {"arrive", "attend", "lean", "hold", "release", "strike"}
        check(ROWS[7],
              set(mouse_log) == SIX_VERBS and set(touch_log) == SIX_VERBS,
              f"mouse={mouse_log} touch={touch_log}")

        # row 9 — arrive: fires on pointer entry, and resets the breath's phase
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 41)
            arrived1 = wait_for(br, verb_expr("arrive"))
            br.sleep(1.0)   # let the phase move well away from its just-reset value
            before = hand_report(br)["tilt"]["phase"]
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 42)
            arrived2 = wait_for(br, verb_expr("arrive"))
            after = hand_report(br)["tilt"]["phase"]
            check(ROWS[8],
                  bool(arrived1) and bool(arrived2) and abs(after - before) > 0.01,
                  f"arrived1={arrived1} arrived2={arrived2} phase_before={before} phase_after={after}")

        # row 10 — attend: the free point moves toward the hand, hover and drag alike
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 51)
            fire(br, WORK, "pointermove", "mouse", 0.9, 0.2, 51)
            hover_converged = wait_for(
                br, "(()=>{const r=window.__exPass.hand().report();const t=r.attend.target;"
                    "return !!t&&Math.hypot(r.attend.x-t.x,r.attend.y-t.y)<0.02;})()", timeout=6.0)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 52)
            fire(br, WORK, "pointermove", "mouse", 0.1, 0.9, 52)
            drag_converged = wait_for(
                br, "(()=>{const r=window.__exPass.hand().report();const t=r.attend.target;"
                    "return !!t&&Math.hypot(r.attend.x-t.x,r.attend.y-t.y)<0.02;})()", timeout=6.0)
            check(ROWS[9],
                  bool(hover_converged) and bool(drag_converged),
                  f"hover_converged={hover_converged} drag_converged={drag_converged}")

        # row 11 — lean: the mix band, its two directions, and the spring return
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            wait_span(br, "mix")
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 61)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 61)
            fire(br, WORK, "pointermove", "mouse", 0.95, 0.5, 61)
            wait_for(br, verb_expr("lean"))
            rep1 = hand_report(br)
            cap = rep1["lean"]["cap"]
            v1, dir1 = rep1["lean"]["value"], rep1["lean"]["direction"]
            fire(br, WORK, "pointermove", "mouse", 0.05, 0.5, 61)
            wait_for(br, verb_expr("lean"))
            rep2 = hand_report(br)
            v2, dir2 = rep2["lean"]["value"], rep2["lean"]["direction"]
            fire(br, WORK, "pointerup", "mouse", 0.05, 0.5, 61)
            wait_for(br, verb_expr("release"))
            returned = wait_for(
                br, "(()=>Math.abs(window.__exPass.hand().report().lean.value)<0.001)()", timeout=6.0)
            check(ROWS[10],
                  cap > 0 and 0 < abs(v1) <= cap + 1e-9 and 0 < abs(v2) <= cap + 1e-9
                  and dir1 == "toward-source" and dir2 == "into-construction" and bool(returned),
                  f"v1={v1} dir1={dir1} v2={v2} dir2={dir2} cap={cap} returned={returned}")

        # row 12 — hold: the breath dims to a quarter, keeps running, and its measured stretch prints
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 71)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 71)
            held = wait_for(br, verb_expr("hold"), timeout=3.0)
            rep = hand_report(br)
            gain, running, stretch = rep["tilt"]["gain"], rep["tilt"]["running"], rep["hold"]["stretch"]
            print(f"\nhold — the deep fold's own measured stretch: {stretch}")
            fire(br, WORK, "pointerup", "mouse", 0.5, 0.5, 71)
            check(ROWS[11],
                  bool(held) and abs(gain - 0.25) < 1e-9 and running is True,
                  f"held={held} gain={gain} running={running} stretch={stretch}")

        # row 13 — release: the ring, the curved return, and the afterglow past the resolve
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            wait_span(br, "mix")
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 81)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 81)
            fire(br, WORK, "pointermove", "mouse", 0.95, 0.5, 81)
            wait_for(br, verb_expr("lean"))
            fire(br, WORK, "pointerup", "mouse", 0.95, 0.5, 81)
            wait_for(br, verb_expr("release"))
            rep0 = hand_report(br)
            br.sleep(0.4)
            rep_mid = hand_report(br)
            br.sleep(0.5)
            rep_late = hand_report(br)
            ring0 = bool(rep0["release"] and rep0["release"]["ring"])
            v0, vmid = abs(rep0["lean"]["value"]), abs(rep_mid["lean"]["value"])
            curved = v0 > vmid > 0 and v0 > 1e-6
            late = rep_late["release"]
            late_ok = bool(late and late["resolved"] and late["afterglow"])
            check(ROWS[12],
                  ring0 and curved and late_ok,
                  f"ring0={ring0} v0={v0} vmid={vmid} late={late}")

        # row 14 — Requirement 38 c4, the chart law: two unfold parameters, each on its own axis
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            wait_span(br, "mix")
            wait_span(br, "tilt")
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 91)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 91)
            fire(br, WORK, "pointermove", "mouse", 0.9, 0.1, 91)
            wait_for(br, verb_expr("lean"))
            converged = wait_for(
                br, "(()=>{const r=window.__exPass.hand().report();const t=r.attend.target;"
                    "return !!t&&Math.hypot(r.attend.x-t.x,r.attend.y-t.y)<0.02;})()", timeout=6.0)
            chart = hand_report(br)["chart"]
            print(f"\nchart law — unfold's own mapping: "
                  f"x -> {chart['unfold']['x']['handle']} = {chart['unfold']['x']['value']:.4f}, "
                  f"y -> {chart['unfold']['y']['handle']} = {chart['unfold']['y']['value']:.4f}")
            moves = sorted(chart["moves"])
            fire(br, WORK, "pointerup", "mouse", 0.9, 0.1, 91)
            check(ROWS[13],
                  bool(converged) and moves == ["mix", "tilt"]
                  and chart["unfold"]["x"]["handle"] == "mix" and chart["unfold"]["y"]["handle"] == "tilt"
                  and abs(chart["unfold"]["x"]["value"]) > 0 and abs(chart["unfold"]["y"]["value"]) > 0,
                  f"moves={moves} chart={chart}")

        # row 15 — strike: a single tap on the work fires it; the same tap on a claimed surface does not
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 101)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 102)
            fire(br, WORK, "pointerup", "mouse", 0.5, 0.5, 102)
            struck = wait_for(br, verb_expr("strike"))
            verb_on_work = hand_report(br)["verb"]
            wait_for(br, "!!document.querySelector('.exsnd-vol')", timeout=6.0)
            before_off_work = hand_report(br)["verb"]
            fire(br, ".exsnd-vol", "pointerdown", "mouse", 0.5, 0.5, 103)
            fire(br, ".exsnd-vol", "pointerup", "mouse", 0.5, 0.5, 103)
            br.sleep(0.2)
            after_off_work = hand_report(br)["verb"]
            check(ROWS[14],
                  bool(struck) and verb_on_work == "strike" and after_off_work == before_off_work,
                  f"struck={struck} verb_on_work={verb_on_work} "
                  f"before_off_work={before_off_work} after_off_work={after_off_work}")

        # row 16 — the walk's own frame index never moves under any of the twelve gestures
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base, "0.2")
            idxt0 = cur(br)
            wait_for(br, HAND_READY)
            drive_verbs(br, "touch", 111)
            idxt1 = cur(br)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            idxm0 = cur(br)
            wait_for(br, HAND_READY)
            drive_verbs(br, "mouse", 121)
            idxm1 = cur(br)
        with Browser(width=1280, height=900) as br:
            room(br, base, "0.2")
            idxw0 = cur(br)
            br.wheel(delta_y=400)
            br.sleep(0.5)
            idxw1 = cur(br)
        check(ROWS[15],
              idxt1 == idxt0 and idxm1 == idxm0 and idxw1 == idxw0 + 1,
              f"touch: {idxt0}->{idxt1} (want unchanged) — mouse: {idxm0}->{idxm1} (want unchanged) — "
              f"wheel: {idxw0}->{idxw1} (want {idxw0 + 1})")

# ---------------------------------------------------------------- report
import shutil  # noqa: E402

shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
