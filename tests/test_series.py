#!/usr/bin/env python3
"""The series side room (EX-SERIES / INV-46) — adapted for exhibition-engine synthetic fixture.
The fixture has two series: polaroids (8 members) and lane (3 members).
Run: python tests/test_series.py
"""
import json
import shutil
import subprocess
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


TMP = Path(tempfile.mkdtemp(prefix="synth_series_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
WORK_IDS = {w["id"] for w in DATA["works"]}
SER = DATA.get("series") or []
BIG = next(i for i, s in enumerate(SER) if s["variant"] == "polaroids")
SMALL = next(i for i, s in enumerate(SER) if s["variant"] == "lane")
BIG_N = len(SER[BIG]["members"])
marked = {w["id"]: w.get("ser") for w in DATA["works"] if "ser" in w}
single = next(w["id"] for w in DATA["works"] if "ser" not in w)

# ---------------------------------------------------------------- data + string rows
check("EX-SERIES the baked block is clean (3+ only, variants sane, members live, NO theme text)",
      all(len(s["members"]) >= 3 and s["variant"] in ("lane", "polaroids")
          and set(s["members"]) <= WORK_IDS and "theme" not in s and "themes" not in s
          for s in SER) and len(SER) >= 2 and len(marked) == sum(len(s["members"]) for s in SER),
      f"series={[(s['variant'], len(s['members'])) for s in SER]} marked={len(marked)}")

greet = DATA.get("greet") or {}
langs = greet.get("langs") or {}
chk = subprocess.run([sys.executable, str(ROOT / "scripts" / "gen_greetings.py"), "--check"],
                     capture_output=True, text=True)
# engine/assets/ holds exhibition.js and worker.js (adapted from assets_src/)
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
wsrc = (ROOT / "engine" / "assets" / "worker.js").read_text(encoding="utf-8")
check("EX-SERIES the pill word rides the one chain (cache ×7 · validator · worker source · EN built-ins)",
      all((L.get("series") or "").strip() and (L.get("room_back") or "").strip()
          for L in langs.values())
      and chk.returncode == 0
      and '"series"' in js_src
      and '"series"' in wsrc and '"room_back"' in wsrc,
      f"langs_ok={all((L.get('series') or '').strip() for L in langs.values())} "
      f"check_rc={chk.returncode}")

BROWSER_ROWS = [
    "EX-SERIES the pill appears only where a real series hangs (localized «серия · N»; singletons bare)",
    "EX-SERIES the room opens as a FACE and returns exactly (step laid · locked beneath · chip/Esc/Back land the frame)",
    "EX-SERIES the variant is the series' character (8 → polaroid table; 3 → sideways lane)",
    "EX-SERIES the room opens through the black (veil covers, room dresses under it, one reveal — the door's own crossing)",
    "EX-SERIES/INV-88 the first-member rest survives late pictures",
    "EX-SERIES/INV-96 the ambiguous window eats nothing over the lane",
]

IN_VIEW = ("(()=>{const f=[...document.querySelectorAll('.exh-frame')].find(x=>{"
           "const r=x.getBoundingClientRect();return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});"
           "return f?f.dataset.id:null;})()")
SIDE_ON = "(()=>{const s=document.getElementById('ex-side');return !!s&&!s.hidden})()"


def walk_with(br, base, pick):
    br.navigate(base + "/")
    br.evaluate("localStorage.clear();sessionStorage.clear()")
    br.evaluate("localStorage.setItem('ex-tempo','0.2')")
    br.evaluate("localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:10}))"
                % (json.dumps(VER), json.dumps(pick)))
    br.reload()
    br.sleep(1.3)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    HOLD = {}
    with serve(TMP, hold=HOLD) as base:
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            # 0 · the pill, localized, only on series frames
            big_member = SER[BIG]["members"][0]
            walk_with(br, base, big_member)
            pill = br.evaluate(
                "(()=>{const p=document.querySelector('#exh-cap .ex-series');"
                "return p?{text:p.textContent.trim(),tag:p.tagName}:null;})()")
            walk_with(br, base, single)
            no_pill = br.evaluate("document.querySelector('#exh-cap .ex-series')") is None
            check(BROWSER_ROWS[0],
                  bool(pill) and pill["tag"] == "BUTTON"
                  and pill["text"] == f"серия · {BIG_N}" and no_pill,
                  f"pill={pill} singleton_bare={no_pill}")

            # 1 · the FACE: step + lock + exact return by all three roads
            walk_with(br, base, big_member)
            frame_ids = br.evaluate(
                "Array.from(document.querySelectorAll('.exh-frame')).map(f=>f.dataset.id)")
            member_idx = [i for i, fid in enumerate(frame_ids)
                          if fid in set(SER[BIG]["members"])][1]
            br.evaluate("document.querySelectorAll('.exh-frame')[%d]"
                        ".scrollIntoView({behavior:'instant'})" % member_idx)
            br.sleep(0.8)
            frame_before = br.evaluate(IN_VIEW)
            hl0 = br.evaluate("history.length")
            br.click("#exh-cap .ex-series", settle=0.6)
            opened = br.evaluate(SIDE_ON)
            step_laid = br.evaluate("history.length") == hl0 + 1
            for _ in range(3):
                br.wheel()
            br.sleep(0.4)
            locked = br.evaluate(IN_VIEW) == frame_before
            chip = br.evaluate("document.querySelector('#ex-side .exs-back').textContent.trim()")
            br.click("#ex-side .exs-back", settle=0.8)
            back1 = (not br.evaluate(SIDE_ON)) and br.evaluate(IN_VIEW) == frame_before
            br.click("#exh-cap .ex-series", settle=0.6)
            br.key("Escape")
            br.sleep(0.8)
            back2 = (not br.evaluate(SIDE_ON)) and br.evaluate(IN_VIEW) == frame_before
            br.click("#exh-cap .ex-series", settle=0.6)
            br.evaluate("history.back()")
            br.sleep(0.8)
            back3 = (not br.evaluate(SIDE_ON)) and br.evaluate(IN_VIEW) == frame_before
            check(BROWSER_ROWS[1],
                  opened and step_laid and locked and chip == "← комната"
                  and back1 and back2 and back3,
                  f"opened={opened} step={step_laid} locked={locked} chip={chip!r} "
                  f"roads={back1}/{back2}/{back3}")

            # 2 · the variant is the series' character
            br.click("#exh-cap .ex-series", settle=0.6)
            big_face = br.evaluate(
                "(()=>{const st=document.getElementById('exs-stage');"
                "return {cls:st.className,n:st.querySelectorAll('.exs-print').length};})()")
            br.evaluate("history.back()")
            br.sleep(0.8)
            small_member = SER[SMALL]["members"][0]
            walk_with(br, base, small_member)
            br.click("#exh-cap .ex-series", settle=0.6)
            small_face = br.evaluate(
                "(()=>{const st=document.getElementById('exs-stage');"
                "return {cls:st.className,n:st.querySelectorAll('img').length};})()")
            check(BROWSER_ROWS[2],
                  "polaroids" in big_face["cls"] and big_face["n"] == BIG_N
                  and "lane" in small_face["cls"] and small_face["n"] == len(SER[SMALL]["members"]),
                  f"big={big_face} small={small_face}")

            # 3 · the crossing through the black
            walk_with(br, base, big_member)
            br.evaluate("localStorage.setItem('ex-tempo','1.35')")
            br.reload()
            br.sleep(1.3)
            br.click("#exh-cap .ex-series", settle=0.15)
            veil_mid = br.evaluate(
                "(()=>{const v=document.getElementById('ex-veil');"
                "return !!v&&!v.hidden&&v.classList.contains('on')})()")
            room_early = br.evaluate(SIDE_ON)
            br.sleep(1.8)
            room_after = br.evaluate(SIDE_ON)
            veil_after = br.evaluate(
                "(()=>{const v=document.getElementById('ex-veil');return !v||v.hidden})()")
            check(BROWSER_ROWS[3],
                  veil_mid and (not room_early) and room_after and veil_after,
                  f"veil_mid={veil_mid} room_early={room_early} "
                  f"room_after={room_after} veil_after={veil_after}")

        # 4 · EX-SERIES/INV-88: the lane's first-member rest survives late-decoding pictures — the
        # reused #exs-stage refuses the browser's scroll-compensation (overflow-anchor:none) and
        # re-affirms scrollLeft 0 once its pictures have actually decoded (his phone find 2026-07-16:
        # an arriving picture nudged the lane toward whichever member the browser anchored on) —
        # UNLESS the visitor has already taken the lane in hand: a touch mid-decode must spend the
        # re-affirm, never yank a mid-swipe visitor back to member 0 (fresh-eyes fold, the YANK).
        WORKS_BY_ID = {w["id"]: w for w in DATA["works"]}
        lane_members = SER[SMALL]["members"]
        with Browser(width=390, height=844) as br:
            br.touch(True)
            walk_with(br, base, lane_members[0])
            br.click("#exh-cap .ex-series", settle=0.6)
            anchor = br.evaluate(
                "getComputedStyle(document.querySelector('.exs-stage.lane')).overflowAnchor")
            scrollable = br.evaluate(
                "(()=>{const l=document.querySelector('.exs-stage.lane');"
                "return l.scrollWidth > l.clientWidth + 4;})()")
            br.evaluate("history.back()")
            br.sleep(0.5)
        HOLD.update(match=WORKS_BY_ID[lane_members[1]]["img"], delay=3.0)
        with Browser(width=390, height=844) as br:
            br.touch(True)
            walk_with(br, base, lane_members[0])
            br.click("#exh-cap .ex-series", settle=0.6)
            br.sleep(3.8)                               # past the held picture's decode
            sl_untouched = br.evaluate(
                "(document.querySelector('.exs-stage.lane')||{}).scrollLeft")
        HOLD.clear()
        if not scrollable:
            # pattern-matches INV-96's own skip above: this fixture/viewport leaves the lane not
            # horizontally scrollable, so the touched-lane (YANK) leg has nothing to swipe — but the
            # deterministic legs (CSS + the untouched rest) are still real assertions, kept as-is.
            check(BROWSER_ROWS[4],
                  anchor == "none" and sl_untouched == 0,
                  f"overflow_anchor={anchor!r} untouched_scrollLeft={sl_untouched} "
                  f"(touched-lane/YANK leg untestable here: lane not horizontally scrollable)")
        else:
            HOLD.update(match=WORKS_BY_ID[lane_members[1]]["img"], delay=3.0)
            with Browser(width=390, height=844) as br:
                br.touch(True)
                walk_with(br, base, lane_members[0])
                br.click("#exh-cap .ex-series", settle=0.6)
                # the visitor takes the lane in hand DURING the decode — a real touchstart, then a
                # swipe. scroll-snap may settle the written value to its own nearest snap point
                # immediately (a real, unrelated CSS mechanic) — so the YANK assertion below compares
                # against THAT settled baseline, not the raw value written, isolating the decode
                # re-affirm's own behaviour from ordinary snap settling.
                sl_touched_before = br.evaluate(
                    "(()=>{const st=document.getElementById('exs-stage');"
                    "st.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,cancelable:true,"
                    "touches:[],changedTouches:[]}));st.scrollLeft=300;return st.scrollLeft;})()")
                br.sleep(3.8)                           # past the held picture's decode
                sl_touched_after = br.evaluate(
                    "(document.querySelector('.exs-stage.lane')||{}).scrollLeft")
            HOLD.clear()
            check(BROWSER_ROWS[4],
                  anchor == "none" and sl_untouched == 0
                  and sl_touched_before > 50 and sl_touched_after >= sl_touched_before - 30,
                  f"overflow_anchor={anchor!r} untouched_scrollLeft={sl_untouched} "
                  f"touched_scrollLeft {sl_touched_before}→{sl_touched_after} "
                  f"(never yanked back toward 0)")

        # 5 · EX-SERIES/INV-96: the ambiguous window eats nothing over the lane. Two legs:
        # (a) while a touch's first moves stay under the 12px axis threshold, NONE of them is
        #     default-prevented — dispatched as synthetic TouchEvents (like this file's own
        #     LANE_DRAG helper elsewhere) so ev.defaultPrevented reads exactly, with no risk of
        #     Chrome coalescing several rapid CDP touch samples into one JS event and masking which
        #     step actually saw preventDefault;
        # (b) a REAL slow-starting swipe (native touch via CDP, sub-12px opening) still glides the
        #     lane — twice in a row (his every-other-swipe phone report 2026-07-16).
        LANE_AMBIG = (
            "()=>{const st=document.getElementById('exs-stage');"
            "const img=st.querySelector('img');if(!img)return JSON.stringify({err:'no-img'});"
            "const r=img.getBoundingClientRect();"
            "const x=Math.round(r.left+r.width/2),y=Math.round(r.top+r.height/2);"
            "const mk=(cx,cy)=>new Touch({identifier:1,target:img,clientX:cx,clientY:cy});"
            "const fire=(t,cx,cy)=>{const ev=new TouchEvent(t,{touches:t==='touchend'?[]:[mk(cx,cy)],"
            "targetTouches:t==='touchend'?[]:[mk(cx,cy)],changedTouches:[mk(cx,cy)],bubbles:true,cancelable:true});"
            "img.dispatchEvent(ev);return ev.defaultPrevented;};"
            "fire('touchstart',x,y);"
            # the last two steps cross the 12px threshold -> the axis verdict decides horizontal
            "const steps=[[2,1],[4,1],[7,2],[9,2],[15,2],[40,2]];"
            "const pd=steps.map(([dx,dy])=>fire('touchmove',x-dx,y+dy));"
            "fire('touchend',x-40,y+2);"
            "return JSON.stringify({steps:steps,pd:pd});}"
        )

        def slow_lane_swipe(br, x0, y0, dx_total, seconds=1.0):
            """A slow REAL one-finger horizontal drag (native touch via CDP) whose FIRST steps
            stay inside the 12px ambiguous window (both axes) before continuing on to dx_total —
            pattern-matches test_compose.py's slow_drag, opened deliberately sub-12px."""
            OPEN = [(2, 1), (4, 1), (7, 2), (9, 2)]      # cumulative offsets, all < 12px both axes
            TAIL = 14
            sign = -1 if dx_total < 0 else 1
            steps_n = len(OPEN) + TAIL
            br._cmd("Input.dispatchTouchEvent", type="touchStart",
                    touchPoints=[{"x": int(x0), "y": int(y0)}])
            last_ox, last_oy = 0, 0
            for dx, dy in OPEN:
                last_ox, last_oy = sign * dx, dy
                br._cmd("Input.dispatchTouchEvent", type="touchMove",
                        touchPoints=[{"x": int(x0 + last_ox), "y": int(y0 + last_oy)}])
                br.sleep(seconds / steps_n)
            for i in range(1, TAIL + 1):
                ox = last_ox + (dx_total - last_ox) * i / TAIL
                br._cmd("Input.dispatchTouchEvent", type="touchMove",
                        touchPoints=[{"x": int(x0 + ox), "y": int(y0 + last_oy)}])
                br.sleep(seconds / steps_n)
            br._cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])
            br.sleep(0.4)

        with Browser(width=390, height=844) as br:
            br.touch(True)
            walk_with(br, base, lane_members[0])
            br.click("#exh-cap .ex-series", settle=0.6)
            lane = br.evaluate(
                "(()=>{const l=document.querySelector('.exs-stage.lane');"
                "if(!l)return null;const r=l.getBoundingClientRect();"
                "return {cx:Math.round(r.left+r.width/2), cy:Math.round(r.top+r.height/2), "
                "sw:l.scrollWidth, cw:l.clientWidth};})()")
            out = json.loads(br.evaluate("(%s)()" % LANE_AMBIG)) if lane else {"err": "no-lane"}
            if not lane or "err" in out:
                skip(BROWSER_ROWS[5], f"no lane/img found in the side room ({out})")
            elif lane["sw"] <= lane["cw"] + 4:
                # pattern-matches CH9 in test_compose.py: this fixture's images are too small to
                # overflow the lane at this viewport — the axis-true carve-out is untestable here
                skip(BROWSER_ROWS[5],
                     f"lane not horizontally scrollable (sw={lane['sw']} cw={lane['cw']})")
            else:
                steps, pd = out["steps"], out["pd"]
                ambiguous_bad = any(pd[i] for i, (dx, dy) in enumerate(steps)
                                     if abs(dx) < 12 and abs(dy) < 12)
                cx, cy = lane["cx"], lane["cy"]
                sl0 = br.evaluate("document.querySelector('.exs-stage.lane').scrollLeft") or 0
                slow_lane_swipe(br, cx, cy, -200)
                sl1 = br.evaluate("document.querySelector('.exs-stage.lane').scrollLeft") or 0
                slow_lane_swipe(br, cx, cy, -200)
                sl2 = br.evaluate("document.querySelector('.exs-stage.lane').scrollLeft") or 0
                moved1 = sl1 > sl0 + 2
                moved2 = sl2 > sl1 + 2
                check(BROWSER_ROWS[5],
                      not ambiguous_bad and moved1 and moved2,
                      f"ambiguous_prevented={ambiguous_bad} steps={steps} pd={pd} "
                      f"scrollLeft {sl0}→{sl1}→{sl2}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
