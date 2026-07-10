#!/usr/bin/env python3
"""The threshold + the hang + the loop (EX-DOOR/EX-DOOR-2, EX-HANG) — adapted for exhibition-engine
synthetic fixture. One test per TEST_MATRIX row. Asserts the REAL baked bundle in a REAL
headless Chrome. Chrome absent → pinned expected SKIPs. Run: python tests/test_door.py
"""
import json
import re as _re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
import engine_build  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
BONE = (179, 162, 132)

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_door_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

EXDATA = json.loads((TMP / "exhibition_data.json").read_text())
WORKS = EXDATA["works"]
WORK_IDS = {w["id"] for w in WORKS}
BY_ID = {w["id"]: w for w in WORKS}
CONFIG_PATH = TMP / "config.json"
CONFIG0 = CONFIG_PATH.read_text()
EXCFG = json.loads(CONFIG0)["exhibition"]
INDEX_RAW = (TMP / "index.html").read_text(encoding="utf-8")

SPREAD = EXCFG["spread_size"]
UNFOLD = EXCFG["unfold_step"]
DOOR_SIZE = EXCFG["door_size"]
MAXU = EXCFG["max_unfolds"]
CAP = SPREAD + MAXU * UNFOLD

# ---------------------------------------------------------------- data rows

door = EXDATA.get("door") or {}
pool = door.get("pool") or []
# Read door candidates from the fixture (engine_build.FIXTURE, not ROOT)
src_order = [e.get("id") for e in json.loads(
    (engine_build.FIXTURE / "gallery" / "door_candidates.json").read_text(encoding="utf-8"))]
living_order = [i for i in src_order if i in WORK_IDS]
check("Door pool baked IN CANDIDATES ORDER (the order IS the curation) + knobs; tombstoned knobs gone",
      len(pool) >= DOOR_SIZE
      and [e.get("id") for e in pool] == living_order
      and all((e.get("alt") or "").strip() for e in pool)
      and "row_size" not in EXCFG and "transition_ms" not in EXCFG,
      f"pool={len(pool)} ordered={[e.get('id') for e in pool] == living_order} "
      f"tombstones_gone={'row_size' not in EXCFG and 'transition_ms' not in EXCFG}")

check("EX-DOOR lives only in the live face (no door markup in served index.html)",
      "ex-skip" not in INDEX_RAW and "ex-door" not in INDEX_RAW and "exd-" not in INDEX_RAW)

check("GA tag absent when no --ga-id (this bundle)",
      "googletagmanager" not in INDEX_RAW and json.loads(CONFIG0).get("ga_measurement_id") == "")
TMP_GA = Path(tempfile.mkdtemp(prefix="synth_ga_"))
build_site.OUT = TMP_GA
build_site.build(SITE_URL, ga_id="G-TEST12345")
build_site.OUT = TMP
ga_root = (TMP_GA / "index.html").read_text(encoding="utf-8")
ga_work = next((TMP_GA / "w").glob("*.html")).read_text(encoding="utf-8")
check("GA tag from config: --ga-id reaches root + work pages + config.json",
      "gtag/js?id=G-TEST12345" in ga_root and "gtag/js?id=G-TEST12345" in ga_work
      and json.loads((TMP_GA / "config.json").read_text()).get("ga_measurement_id") == "G-TEST12345")


def door_layout(W, H, door_size=None, pool_n=None):
    door_size = DOOR_SIZE if door_size is None else door_size
    pool_n = len(pool) if pool_n is None else pool_n
    col = W / H <= 1.02
    if not col:
        gap = max(16, min(44, W * 0.03))
        cap = min(190, H * 0.42)
        n = min(door_size, pool_n)
        while n > 3:
            size = min(cap, (W * 0.88 - (n - 1) * gap) / n)
            if size >= 118:
                break
            n -= 1
        size = min(cap, (W * 0.88 - (n - 1) * gap) / n)
    else:
        gap = max(14, min(30, H * 0.025))
        cap = min(190, W * 0.62)
        n = min(3, pool_n)
        size = min(cap, (H * 0.52 - (n - 1) * gap) / n)
        if size < 104 and n > 2:
            n = 2
            size = min(cap, (H * 0.52 - gap) / 2)
    return n, col, max(76.0, size)


# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-DOOR cold face speaks the question (ask + full-bright windows, NO silent entry, no hang)",
    "EX-DOOR pick = seed (ceremony lands the gallery, picked first; in-flight tap ignored)",
    "EX-DOOR-2b one line always — the viewport sweep (count by the algorithm, nothing clipped)",
    "EX-DOOR the share is ONE floating button: hidden at the door, shown in the hang (fixed chrome, 2026-07-09)",
    "EX-DOOR missing/thin pool degrades to the diverse hang directly (no blank, no error)",
    "EX-DOOR-2d the pool is curated; the STANDING set holds (exit re-shows the same hand; hand ⊆ pool)",
    "EX-DOOR return visit sees no door",
    "EX-DOOR keyboard + alt (windows are real buttons, focus-reachable, alts non-empty)",
    "INV-28 door_size is the ceiling (flip to 3 → 3 windows on a wide viewport)",
    "EX-HANG one work per viewport (frames ≈ viewport, image inside, nothing clipped; no CSS latch — EX-GLIDE owns the settle)",
    "EX-HANG caption zone + counter follow the scroll; phone caption clears the image (H1)",
    "EX-HANG the ground breathes between frames",
    "EX-HANG spread_size is config (flip → frame count changes)",
    "INV-29/30 closing screen: «ещё N» extends without reshuffle, retires at the cap, exit stays",
    "INV-30 budget derived on restore (tampered shown clamped)",
    "INV-30/31 fresh pick at the door = fresh budget",
    "INV-26 walk persists across reload (same hang, no door)",
    "INV-26 bad stored state → the door proves the discard",
    "INV-31 the loop: exit → the same curated door; a pick REPLACES the arc",
    "EX-DOOR-2c full-bright windows; the halo answers from ZERO, in liveAccent's color",
    "EX-DOOR-2e ceremony B: veil → the name alone → tone first → work after; one step; Back cancels",
    "EX-COPY the walk signs off (one quiet © line on the closing screen; door + frames bare)",
    "EX-DOOR-2f the door locks the page (nothing scrolls behind the threshold, cold or re-opened)",
    "EX-DOOR-2g the door hints by behavior (idle cold door: the first halo breathes; interaction retires it; re-opened door never hints)",
    "EX-DOOR-RELOAD a reload of the returned door holds the door (≥60% kept, ≤40% new; repeated reloads still hold)",
]

DOOR_IDS = "Array.from(document.querySelectorAll('.exd-window')).map(b=>b.dataset.id)"
FRAME_IDS = "Array.from(document.querySelectorAll('.exh-frame')).map(f=>f.dataset.id)"
AT_DOOR = "document.body.classList.contains('ex-door')"
N_FRAMES = "document.querySelectorAll('.exh-frame').length"

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    def fresh(br, base, tempo="0.05"):
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
        br.reload()
        br.sleep(1.0)

    def enter(br, nth=1, settle=1.0):
        br.click(f".exd-window:nth-child({nth})", settle=settle)

    def to_fin(br):
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.3)

    with serve(TMP) as base, Browser(width=1280, height=900) as br:
        br.pretend("ru-RU", 15)

        # 0 · the cold face speaks the question
        fresh(br, base)
        exp_n, _, _ = door_layout(1280, 900)
        face = br.evaluate(
            "(()=>{const ask=[...document.querySelectorAll('#ex-door div')]"
            ".find(d=>d.textContent.includes('что ближе сейчас?'));"
            "return {door:" + AT_DOOR + ",ask:!!ask,askVis:ask?getComputedStyle(ask).display!=='none':false,"
            "wins:document.querySelectorAll('.exd-window').length,"
            "skip:!!document.getElementById('ex-skip'),frames:" + N_FRAMES + ","
            "bright:[...document.querySelectorAll('.exd-window img')]"
            ".every(i=>getComputedStyle(i).filter==='none')};})()")
        check(BROWSER_ROWS[0],
              face["door"] and face["ask"] and face["askVis"] and face["wins"] == exp_n
              and not face["skip"] and face["frames"] == 0 and face["bright"],
              f"exp_n={exp_n} {face}")

        # 1 · pick = seed; a second tap mid-ceremony is ignored
        fresh(br, base, tempo="0.5")
        door_ids = br.evaluate(DOOR_IDS)
        br.click(".exd-window:nth-child(1)", settle=0.1)
        br.click(".exd-window:nth-child(3)", settle=0.05)
        br.sleep(2.0)
        frames = br.evaluate(FRAME_IDS)
        check(BROWSER_ROWS[1],
              (not br.evaluate(AT_DOOR)) and len(frames) == SPREAD and frames[0] == door_ids[0],
              f"n={len(frames)} first_is_pick={frames[0] == door_ids[0] if frames else None}")

        # 3 · the share is ONE floating button: hidden at the door, shown in the hang
        #     (fixed chrome above the room — 2026-07-09; nothing on a frame leads away)
        fresh(br, base)
        door_op = br.evaluate(
            "(()=>{const b=document.querySelector('.ex-share');"
            "return b?+getComputedStyle(b).opacity:0;})()")
        enter(br)
        hang = br.evaluate(
            "(()=>{const bs=[...document.querySelectorAll('.ex-share')];const b=bs[0];"
            "return JSON.stringify({n:bs.length,tag:b?b.tagName:'',"
            "fixed:b?getComputedStyle(b).position:'',op:b?+getComputedStyle(b).opacity:0,"
            "in_frame:!!document.querySelector('.exh-frame .ex-share')});})()")
        import json as _j; hang = _j.loads(hang)
        nothing_out = br.evaluate(
            "document.querySelectorAll('.ex-open, #ex-stage a[href*=\"/w/\"]').length") == 0
        check(BROWSER_ROWS[3],
              door_op < 0.05 and hang["n"] == 1 and hang["tag"] == "BUTTON"
              and hang["fixed"] == "fixed" and hang["op"] > 0.3
              and not hang["in_frame"] and nothing_out,
              f"door_opacity={door_op} hang={hang} nothing_out={nothing_out}")

        # 5 · the pool is curated; the STANDING set holds
        fresh(br, base)
        set1 = br.evaluate(DOOR_IDS)
        pool_ids = {e["id"] for e in pool}
        enter(br)
        to_fin(br)
        br.click("#ex-return", settle=0.6)
        set3 = br.evaluate(DOOR_IDS)
        check(BROWSER_ROWS[5],
              len(set1) > 0 and set(set1) <= pool_ids and set3 == set1,
              f"hand_in_pool={set(set1) <= pool_ids} exit_same={set3 == set1}")

        # 6 · return visit sees no door
        fresh(br, base)
        enter(br)
        br.reload(); br.sleep(1.0)
        check(BROWSER_ROWS[6],
              (not br.evaluate(AT_DOOR)) and br.evaluate(N_FRAMES) == SPREAD,
              f"frames={br.evaluate(N_FRAMES)}")

        # 7 · keyboard + alt
        fresh(br, base)
        kb = br.evaluate(
            "(()=>{const ws=[...document.querySelectorAll('.exd-window')];"
            "return {kb:ws.every(b=>b.tabIndex>=0),"
            "alts:ws.every(b=>((b.querySelector('img').alt)||'').trim().length>0),"
            "labels:ws.every(b=>((b.getAttribute('aria-label'))||'').trim().length>0)};})()")
        check(BROWSER_ROWS[7], kb["kb"] and kb["alts"] and kb["labels"], f"{kb}")

        # 8 · door_size is the ceiling
        cfg = json.loads(CONFIG0)
        cfg["exhibition"]["door_size"] = 3
        CONFIG_PATH.write_text(json.dumps(cfg))
        fresh(br, base)
        n3 = br.evaluate("document.querySelectorAll('.exd-window').length")
        CONFIG_PATH.write_text(CONFIG0)
        check(BROWSER_ROWS[8], br.evaluate(AT_DOOR) and n3 == 3, f"windows={n3}")

        # 9 · EX-HANG geometry
        fresh(br, base)
        enter(br)
        geo = br.evaluate(
            "(()=>{const ih=window.innerHeight,iw=window.innerWidth;"
            "const fs=[...document.querySelectorAll('.exh-frame')];"
            "const heights=fs.every(f=>Math.abs(f.getBoundingClientRect().height-ih)<=2);"
            "const noLatch=getComputedStyle(document.documentElement).scrollSnapType==='none';"
            "const img=fs[0].querySelector('img');const r=img.getBoundingClientRect();"
            "const inside=r.height<=ih*0.84&&r.width<=iw*0.9;"
            "return {n:fs.length,heights,noLatch,inside,noX:document.documentElement.scrollWidth<=iw+1};})()")
        check(BROWSER_ROWS[9],
              geo["n"] == SPREAD and geo["heights"] and geo["noLatch"] and geo["inside"] and geo["noX"],
              f"{geo}")

        # 10 · caption + counter follow the scroll; phone caption clears the image
        br.evaluate("document.querySelectorAll('.exh-frame')[1].scrollIntoView()")
        br.sleep(0.7)
        capst = br.evaluate(
            "(()=>{const c=document.getElementById('exh-cap'),k=document.getElementById('exh-counter');"
            "const t=c.querySelector('.title');"
            "return {shown:getComputedStyle(c).opacity>'0.5',title:t?t.textContent.trim():'',"
            "now:k.querySelector('.now').textContent,tot:k.querySelector('.tot').textContent};})()")
        br.set_viewport(375, 720, mobile=True)
        br.sleep(0.6)
        overlap = br.evaluate(
            "(()=>{const c=document.getElementById('exh-cap').getBoundingClientRect();"
            "const f=[...document.querySelectorAll('.exh-frame')]"
            ".find(x=>{const r=x.getBoundingClientRect();return r.top<window.innerHeight/2&&r.bottom>window.innerHeight/2;});"
            "if(!f)return null;const i=f.querySelector('img').getBoundingClientRect();"
            "return !(c.top>=i.bottom||c.bottom<=i.top||c.right<=i.left||c.left>=i.right);})()")
        br.set_viewport(1280, 900)
        check(BROWSER_ROWS[10],
              capst["shown"] and capst["now"] == "02"
              and capst["tot"] == f"{SPREAD:02d}" and overlap is False,
              f"{capst} phone_overlap={overlap}")

        # 11 · the ground breathes between frames
        fresh(br, base)
        enter(br)
        ids = br.evaluate(FRAME_IDS)
        doms = {w["id"]: w.get("dom") for w in WORKS}
        k = next(i for i in range(1, len(ids)) if doms.get(ids[i]) != doms.get(ids[0]))
        g1 = br.evaluate("document.body.style.getPropertyValue('--ground')")
        br.evaluate(f"document.querySelectorAll('.exh-frame')[{k}].scrollIntoView()")
        br.sleep(0.6)
        g2 = br.evaluate("document.body.style.getPropertyValue('--ground')")
        check(BROWSER_ROWS[11], g1 != "" and g2 != "" and g1 != g2, f"g1={g1} g2={g2}")

        # 12 · spread_size is config
        cfg = json.loads(CONFIG0)
        cfg["exhibition"]["spread_size"] = 5
        CONFIG_PATH.write_text(json.dumps(cfg))
        fresh(br, base)
        enter(br)
        n5 = br.evaluate(N_FRAMES)
        CONFIG_PATH.write_text(CONFIG0)
        check(BROWSER_ROWS[12], n5 == 5, f"frames={n5}")

        # 13 · the closing screen: unfold extends without reshuffle, retires at the cap, exit stays
        fresh(br, base)
        enter(br)
        before = br.evaluate(FRAME_IDS)
        to_fin(br); br.click("#ex-unfold", settle=0.5)
        mid = br.evaluate(FRAME_IDS)
        to_fin(br); br.click("#ex-unfold", settle=0.5)
        after = br.evaluate(FRAME_IDS)
        fin = br.evaluate(
            "(()=>{return {more:!!document.getElementById('ex-unfold'),"
            "back:!!document.getElementById('ex-return'),"
            "q:document.querySelector('.exh-fin .q').textContent};})()")
        check(BROWSER_ROWS[13],
              len(mid) == SPREAD + UNFOLD and mid[:SPREAD] == before
              and len(after) == CAP and after[:len(mid)] == mid
              and not fin["more"] and fin["back"] and "новый выбор" in fin["q"]
              and CAP < len(WORKS),
              f"mid={len(mid)} after={len(after)} fin={fin}")

        # 14 · budget derived on restore
        fresh(br, base)
        enter(br)
        ver = EXDATA["version"]
        br.set_local_storage("ex.exhibition",
                             json.dumps({"v": ver, "pick": WORKS[0]["id"], "shown": 4 * CAP}))
        br.reload(); br.sleep(1.0)
        shown = br.evaluate(N_FRAMES)
        more = br.evaluate("!!document.getElementById('ex-unfold')")
        check(BROWSER_ROWS[14], shown == CAP and not more, f"shown={shown} more={more}")

        # 15 · fresh pick at the door = fresh budget
        to_fin(br)
        br.click("#ex-return", settle=0.6)
        br.click(".exd-window:nth-child(2)", settle=1.2)
        n = br.evaluate(N_FRAMES)
        rearmed = br.evaluate("!!document.getElementById('ex-unfold')")
        check(BROWSER_ROWS[15], n == SPREAD and rearmed, f"n={n} rearmed={rearmed}")

        # 16 · walk persists across reload
        fresh(br, base)
        enter(br)
        arc = br.evaluate(FRAME_IDS)
        br.reload(); br.sleep(1.0)
        again = br.evaluate(FRAME_IDS)
        check(BROWSER_ROWS[16],
              again == arc and again != [] and not br.evaluate(AT_DOOR), f"same={again==arc}")

        # 17 · bad stored state → the DOOR proves the discard
        fresh(br, base)
        br.set_local_storage("ex.exhibition", json.dumps({"v": "OLDVER", "pick": WORKS[0]["id"], "shown": 6}))
        br.reload(); br.sleep(1.0)
        old_ver_door = br.evaluate(AT_DOOR)
        br.clear_storage()
        br.evaluate("localStorage.setItem('ex-tempo','0.05')")
        br.set_local_storage("ex.exhibition", json.dumps({"v": EXDATA["version"], "pick": "999999", "shown": 6}))
        br.reload(); br.sleep(1.0)
        missing_id_door = br.evaluate(AT_DOOR)
        check(BROWSER_ROWS[17], old_ver_door and missing_id_door,
              f"old_ver={old_ver_door} missing_id={missing_id_door}")

        # 18 · the loop: exit → the SAME curated door; a pick REPLACES the arc
        fresh(br, base)
        enter(br)
        to_fin(br); br.click("#ex-unfold", settle=0.5)
        walk = br.evaluate(FRAME_IDS)
        to_fin(br); br.click("#ex-return", settle=0.6)
        at_door = br.evaluate(AT_DOOR)
        new_pick = br.evaluate(DOOR_IDS)[1]
        br.click(".exd-window:nth-child(2)", settle=1.2)
        arc_new = br.evaluate(FRAME_IDS)
        br.reload(); br.sleep(1.0)
        persisted = br.evaluate(FRAME_IDS)
        check(BROWSER_ROWS[18],
              at_door
              and arc_new != walk and arc_new[0] == new_pick and len(arc_new) == SPREAD
              and persisted == arc_new,
              f"door={at_door} replaced={arc_new != walk} leads={arc_new[0] == new_pick} "
              f"persisted={persisted == arc_new}")

        # 19 · full-bright windows; the halo answers from ZERO, colored by liveAccent
        fresh(br, base)
        look = br.evaluate(
            "(()=>{const w=document.querySelector('.exd-window');"
            "const s=getComputedStyle(w.querySelector('img'));"
            "const a=getComputedStyle(w,'::after');"
            "return {filter:s.filter,transform:s.transform,halo:+a.opacity,"
            "glow:w.style.getPropertyValue('--glow').trim(),"
            "canHover:matchMedia('(hover: hover)').matches};})()")
        first_id = br.evaluate(DOOR_IDS)[0]
        dom = BY_ID[first_id]["dom"]
        y = 0.2126 * dom[0] + 0.7152 * dom[1] + 0.0722 * dom[2]
        if y < 24:
            exp_glow = BONE
        else:
            kk = min(170 / y, 6)
            exp_glow = tuple(int(min(255, v * kk) * 0.8 + BONE[i] * 0.2 + 0.5)
                             for i, v in enumerate(dom))
        br.hover(".exd-window")
        br.sleep(0.6)
        hov = br.evaluate(
            "(()=>{const w=document.querySelector('.exd-window');"
            "const s=getComputedStyle(w.querySelector('img'));const a=getComputedStyle(w,'::after');"
            "return {filter:s.filter,halo:+a.opacity};})()")
        work_still = (look["filter"] == "none" and hov["filter"] == "none"
                      and look["transform"] == "none")
        halo_zero_to = (abs(look["halo"]) < 0.01
                        and ((hov["halo"] > 0.5) if look["canHover"] else True))
        glow_ok = look["glow"] == f"rgb({exp_glow[0]},{exp_glow[1]},{exp_glow[2]})"
        check(BROWSER_ROWS[19], work_still and halo_zero_to and glow_ok,
              f"rest={look} hover={hov} exp_glow={exp_glow}")

        # 20 · ceremony B at a WATCHABLE tempo
        fresh(br, base, tempo="0.5")
        br.click(".exd-window:nth-child(1)", settle=0.3)
        ph1 = br.evaluate(
            "(()=>{const v=document.getElementById('ex-veil');"
            "return {veil:v&&!v.hidden&&+getComputedStyle(v).opacity>0.05,"
            "door:" + AT_DOOR + ",leaving:document.getElementById('ex-door').classList.contains('leaving')};})()")
        br.sleep(0.4)
        ph2 = br.evaluate(
            "(()=>{return {door:" + AT_DOOR + ",crossing:document.body.classList.contains('ex-crossing'),"
            "work:+getComputedStyle(document.querySelector('.exh-frame img.work')).opacity,"
            "frames:" + N_FRAMES + "};})()")
        br.sleep(1.2)
        ph3 = br.evaluate(
            "(()=>{const v=document.getElementById('ex-veil');"
            "return {veilGone:!v||v.hidden,crossing:document.body.classList.contains('ex-crossing'),"
            "face:history.state&&history.state.ex?history.state.ex.face:null,"
            "work:+getComputedStyle(document.querySelector('.exh-frame img.work')).opacity};})()")
        ceremony_ok = (ph1["veil"] and ph1["door"] and ph1["leaving"]
                       and (not ph2["door"]) and ph2["crossing"] and ph2["work"] < 0.05
                       and ph2["frames"] == SPREAD
                       and ph3["veilGone"] and not ph3["crossing"]
                       and ph3["face"] == "walk" and ph3["work"] > 0.1)
        to_fin(br)
        br.click("#ex-return", settle=0.6)
        br.click(".exd-window:nth-child(1)", settle=0.3)
        br.evaluate("history.back()")
        br.sleep(0.8)
        cancel = br.evaluate(
            "(()=>{const v=document.getElementById('ex-veil');"
            "return {veilGone:!v||v.hidden,crossing:document.body.classList.contains('ex-crossing'),"
            "door:" + AT_DOOR + ",walkVisible:" + N_FRAMES + ">0};})()")
        cancel_ok = cancel["veilGone"] and not cancel["crossing"] and not cancel["door"] and cancel["walkVisible"]
        check(BROWSER_ROWS[20], ceremony_ok and cancel_ok,
              f"ph1={ph1} ph2={ph2} ph3={ph3} cancel={cancel}")

        # 2 · the viewport sweep — one line always
        sweep_fail = []
        for (W, H) in [(1280, 900), (700, 500), (700, 900), (320, 480), (800, 400)]:
            exp_n, exp_col, exp_size = door_layout(W, H)
            br.set_viewport(W, H, mobile=(W < 500))
            fresh(br, base)
            got = br.evaluate(
                "(()=>{const ih=window.innerHeight,iw=window.innerWidth;"
                "const ws=[...document.querySelectorAll('.exd-window')].map(w=>w.getBoundingClientRect());"
                "return {n:ws.length,"
                "tops:[...new Set(ws.map(r=>Math.round(r.top)))].length,"
                "lefts:[...new Set(ws.map(r=>Math.round(r.left)))].length,"
                "whole:ws.every(r=>r.top>=-1&&r.bottom<=ih+1&&r.left>=-1&&r.right<=iw+1),"
                "size:ws.length?Math.round(ws[0].width):0};})()")
            one_line = (got["tops"] == 1) if not exp_col else (got["lefts"] == 1)
            if not (got["n"] == exp_n and one_line and got["whole"]
                    and abs(got["size"] - exp_size) <= 2 and got["size"] >= 76):
                sweep_fail.append(f"{W}x{H}: exp(n={exp_n},col={exp_col},size={exp_size:.0f}) got={got}")
        br.set_viewport(1280, 900)
        check(BROWSER_ROWS[2], not sweep_fail, " | ".join(sweep_fail))

        # 21 · the walk signs off (EX-COPY): one quiet © line on the closing screen
        # Sign format: © YEAR Creator · SITE_NAME (parameterized from SITE_CONFIG)
        fresh(br, base)
        door_signs = br.evaluate("document.querySelectorAll('#ex-door .exh-sign').length")
        enter(br)
        frame_signs = br.evaluate("document.querySelectorAll('.exh-frame .exh-sign').length")
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.5)
        sign = br.evaluate(
            "(()=>{const s=document.querySelectorAll('.exh-fin .exh-sign');"
            "return {n:s.length,text:s.length?s[0].textContent.trim():''};})()")
        creator = build_site.SITE_CONFIG["creator"]
        site_name = build_site.SITE_CONFIG["site_name"]
        sign_ok = bool(_re.fullmatch(
            r"© \d{4} " + _re.escape(creator) + r" · " + _re.escape(site_name),
            sign["text"]))
        check(BROWSER_ROWS[21],
              door_signs == 0 and frame_signs == 0 and sign["n"] == 1 and sign_ok,
              f"door={door_signs} frames={frame_signs} fin={sign}")

        # 22 · the door locks the page behind it
        fresh(br, base)
        for _ in range(3):
            br.wheel()
        br.sleep(0.4)
        cold_locked = br.evaluate("scrollY") == 0
        enter(br)
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.5)
        fin_y = br.evaluate("scrollY")
        br.click("#ex-return", settle=0.8)
        for _ in range(3):
            br.wheel()
        br.sleep(0.4)
        reopened_locked = br.evaluate("scrollY") == 0 and br.evaluate(AT_DOOR)
        br.evaluate("history.back()")
        br.sleep(1.0)
        back_kept = abs(br.evaluate("scrollY") - fin_y) <= 2
        check(BROWSER_ROWS[22], cold_locked and reopened_locked and back_kept,
              f"cold_locked={cold_locked} reopened_locked={reopened_locked} "
              f"back {br.evaluate('scrollY')} want {fin_y}")

        # 23 · the idle hint
        fresh(br, base, tempo="0.2")
        br.sleep(1.0)
        mid = br.evaluate(
            "(()=>{const w=document.querySelector('.exd-window');"
            "return {hint:w.classList.contains('hint'),"
            "halo:+getComputedStyle(w,'::after').opacity};})()")
        hinted = mid["hint"] or mid["halo"] > 0.1
        br.hover(".exd-window:nth-child(2)")
        br.sleep(2.2)
        after = br.evaluate(
            "(()=>{const w=document.querySelector('.exd-window');"
            "return {hint:w.classList.contains('hint'),halo:+getComputedStyle(w,'::after').opacity};})()")
        retired = (not after["hint"]) and after["halo"] < 0.1
        enter(br)
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.4)
        br.click("#ex-return", settle=0.8)
        br.sleep(1.4)
        reopened = br.evaluate(
            "document.querySelector('.exd-window').classList.contains('hint')")
        check(BROWSER_ROWS[23], hinted and retired and not reopened,
              f"mid={mid} after={after} reopened_hints={reopened}")

        # 24 · EX-DOOR-RELOAD: reload of a returned door holds the door
        # walk → exit (returned:true in history.state) → reload → still at door; ≥60% kept, ≤40% new
        fresh(br, base)
        enter(br)                                        # pick, enter the walk
        br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
        br.sleep(0.4)
        first_hand = json.loads(br.evaluate(
            "localStorage.getItem('ex.hand')") or "null") or {}
        first_ids = set(first_hand.get("ids", []))
        br.click("#ex-return", settle=0.8)               # exit → doorReturn() pushes returned:true
        state_before = br.evaluate(
            "(()=>{const s=history.state; return s&&s.ex?JSON.stringify(s.ex):null;})()")
        st_before = json.loads(state_before or "null") or {}
        returned_marker = st_before.get("returned") is True
        br.reload(); br.sleep(1.2)                       # reload the returned door
        after_door = br.evaluate(AT_DOOR)
        after_frames = br.evaluate(N_FRAMES)
        after_hand = json.loads(br.evaluate(
            "localStorage.getItem('ex.hand')") or "null") or {}
        after_ids = set(after_hand.get("ids", []))
        # ≥60% must be kept from the first hand when there is room to swap
        kept = first_ids & after_ids
        n_hand = len(after_ids)
        enough_kept = len(kept) >= int(n_hand * 0.6) if n_hand else True
        # reload again — must still hold the door, not drop into the walk
        br.reload(); br.sleep(1.2)
        still_at_door = br.evaluate(AT_DOOR)
        check(BROWSER_ROWS[24],
              returned_marker and after_door and after_frames == 0
              and enough_kept and still_at_door,
              f"returned={returned_marker} door={after_door} frames={after_frames} "
              f"kept={len(kept)}/{n_hand}≥60%={enough_kept} 2nd_reload={still_at_door}")

    # 4 · missing pool degrades to the diverse hang
    BROKEN = Path(tempfile.mkdtemp(prefix="synth_door_broken_"))
    shutil.copytree(TMP, BROKEN, dirs_exist_ok=True)
    exd = json.loads((BROKEN / "exhibition_data.json").read_text())
    exd.pop("door", None)
    (BROKEN / "exhibition_data.json").write_text(json.dumps(exd))
    with serve(BROKEN) as base2, Browser(width=1280, height=900) as br2:
        br2.pretend("ru-RU", 15)
        br2.navigate(base2 + "/")
        br2.evaluate("localStorage.clear()")
        br2.reload(); br2.sleep(1.2)
        live = br2.evaluate("document.body.classList.contains('ex-live')")
        at_door = br2.evaluate(AT_DOOR)
        n = br2.evaluate(N_FRAMES)
        check(BROWSER_ROWS[4], live and (not at_door) and n == SPREAD,
              f"live={live} door={at_door} frames={n}")


# ---------------------------------------------------------------- report
shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_GA, ignore_errors=True)
try:
    shutil.rmtree(BROKEN, ignore_errors=True)
except NameError:
    pass

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
