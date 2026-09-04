#!/usr/bin/env python3
"""EX-HAND — the touch hand overlay's own file and its reach (Requirement 38 criterion 9, unit U1).

The hand carries no input listener of its own and draws nothing yet — this unit is the plumbing: its
own file travels beside pass-layer.js in the bake (row 1), it attaches on the walk's standing work
and nowhere else Requirement 38 criterion 9 names outside (rows 2/3/5), it steps off while the closer
look (EX-ZOOM) covers the same picture and returns the instant that layer clears (row 4), and the
walk's own navigation is unchanged by its presence (row 6).

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
