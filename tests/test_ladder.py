#!/usr/bin/env python3
"""The in-flight ladder + the one-ahead preload (EX-LOAD-2 / INV-72 · EX-LOAD-3 / INV-73) —
one test per matrix row, adapted for the exhibition-engine synthetic fixture (ported from
an instance). A frame whose pixels are late wears the work's OWN dominant tone (a plate);
on a genuinely long wait a thin wordless bar joins on the plate; the photo fades in over it,
crisp when it beat the plate, graceful when the plate stood. The next walk work quietly preloads
one ahead along the feet. All wordless (INV-1); every wait a beat ×tempo (INV-33).

Asserts the REAL baked bundle in a REAL headless Chrome, on the harness's held-image road
(serve(hold=…)) + the network-log road (net_capture/net_log) for the preload. Baked WITH a
display cap so the srcset tier ladder (INV-63) exists for the tier-composition row — pins all
browser rows SKIP when Pillow (the cap's dependency) is absent. Run: python tests/test_ladder.py
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


try:
    import PIL  # noqa: F401
    _HAVE_PIL = True
except Exception:
    _HAVE_PIL = False

TMP = Path(tempfile.mkdtemp(prefix="synth_ladder_"))
build_site.OUT = TMP
build_site.build(SITE_URL, display_max=(1000 if _HAVE_PIL else None))  # a cap → the srcset tier ladder (INV-63)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
BYID = {str(w["id"]): w for w in DATA["works"]}
PICK = DATA["door"]["pool"][0]["id"]                   # a real curated work — its image really ships
PICK_DOM = BYID[str(PICK)]["dom"]                      # its RAW baked dominant tone [R,G,B]
WALK = json.dumps({"v": VER, "pick": PICK, "shown": 10})

# ---- source traceability (string): every clause has a live code path both directions ----------
JS = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
CSS = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")
check("EX-LOAD-2/-3 traceability: the ladder + preload live in exhibition.js (arm/plate/preloadAhead)",
      all(s in JS for s in ("function arm(", "ex-plate", "load_plate_grace", "load_bar_wait",
                            "load_reveal", "preloadAhead", "travelDir"))
      and all(s in CSS for s in ("#ex-plate", ".ex-bar", "ex-bar-crawl")),
      "one of arm/plate/bar/knobs/preload missing a code path")

# the served images are <id>.png (or a -640/-960/-1280 tier); the fixture ids carry a hyphen
# (synth-01), so strip ONLY a known tier suffix, never the id's own -NN.
WORK_RE = re.compile(r"/gallery/assets/[^/]+/([^/?]+?)(?:-(?:640|960|1280))?\.(?:png|jpe?g)")


def work_ids_in(urls):
    """the distinct work ids among a list of image request URLs (tier suffix stripped)."""
    out = []
    for u in urls:
        m = WORK_RE.search(u)
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


BROWSER_ROWS = [
    "EX-LOAD-2 the plate appears only past the grace (moderate hold plates; a fast link shows none)",
    "EX-LOAD-2 the plate wears the work's OWN baked tone (computed bg == dom, not bone/neighbour)",
    "EX-LOAD-2 the bar joins only past the long wait (long hold → bar; a moderate hold → plate, no bar)",
    "EX-LOAD-2 the bar is wordless (no text/digit/percentage on the plate or bar — INV-1)",
    "EX-LOAD-2 the reveal accelerates on fast arrival (within-grace ⇒ soft token; plate-stood ⇒ reveal token)",
    "EX-LOAD-2 the arm reads the settled state (prover F1): a warm image reveals at once, no plate/clock",
    "EX-LOAD-2 a post-reveal tier swap never re-plates (prover F6): a revealed photo stays painted on resize",
    "EX-LOAD-2 rotation mid-flight keeps the plate (never back to black; the grace clock does not restart)",
    "EX-LOAD-2 the walk overlay + crossing stay off the door (no walk #ex-plate/marks at the door; a warm crossing lays no plate — the door's own windows ladder via .exd-plate, DL1/DL2)",
    "EX-LOAD-2 composes with the tier ladder (the revealed photo is the browser's srcset tier — INV-63)",
    "EX-LOAD-3 the next work actually preloads one-ahead (network log shows an unshown next-arc file)",
    "EX-LOAD-3 exactly one ahead, never the arc (at most preload_ahead unshown next-works requested)",
    "EX-LOAD-3 the preload re-aims on a turn (prover F5): a backward step abandons forward, aims back",
    "EX-LOAD-3 a failed preload is silent (prover F5): the next file blocked errors nothing, the walk lives",
    "EX-LOAD-2 · DL1 a door window rides the ladder (slow ⇒ raw-dom plate + wordless bar; fast ⇒ no plate)",
    "EX-LOAD-2 · DL2 the door ladder composes with the entrance + halo (rise intact, halo liveAccent, plate raw dom; a cached re-render re-flashes no plate)",
    "EX-LADDER a door window rides the ladder — it hands its own small box, so the tier is small, never the display file (INV-63)",
    "EX-LADDER a series lane picture rides the ladder (INV-63)",
    "EX-LADDER a polaroid on the table rides the ladder — the smallest tier for a thumb-sized box (INV-63)",
    "EX-LOAD-FRAME the walk plate raises the loading frame (body.ex-loading-frame) + the counter's loading mark renders while it stands; both clear when the picture lands (his 2026-07-22 note)",
]

# ---- DL1/DL2 helpers: the door's per-window plate (class .exd-plate, five may fly at once) --------
BONE = [179, 162, 132]                                # #b3a284 — the resting accent (exhibition.js)


def live_accent(dom):
    """replica of exhibition.js liveAccent(dom) — the halo's tone, lightness-raised off the raw dom."""
    r, g, b = dom
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if y < 24:
        return list(BONE)
    k = min(170.0 / y, 6)
    return [round(min(255, v * k) * 0.8 + BONE[i] * 0.2) for i, v in enumerate((r, g, b))]


# The door deals a LIVE hand (rotation + novelty), so WHICH work fills a window is not fixed — the
# tests hold EVERY door image (match the shared asset dir) and read whichever window actually renders,
# looking its raw dom up by the window's own data-id. That keeps DL1/DL2 honest against any dealt hand.
DOOR_ASSETS = "/gallery/assets/"

# the first door window whose OWN plate (.exd-plate) stands — its id, computed plate bg, bar/text,
# entrance (animationName) and halo (--glow). '' when no window is plated.
FIRST_DOOR_PLATE = (
    "(()=>{const ws=[...document.querySelectorAll('.exd-window')];"
    "for(const w of ws){const p=w.querySelector('.exd-plate');"
    "if(p && !p.hidden && p.classList.contains('show')){const cs=getComputedStyle(w);"
    "return JSON.stringify({id:w.dataset.id,bg:getComputedStyle(p).backgroundColor,"
    "bar:p.classList.contains('bar'),text:(p.textContent||''),rise:cs.animationName,"
    "glow:(cs.getPropertyValue('--glow')||'').trim()});}}return '';})()")
ANY_DOOR_BAR = ("[...document.querySelectorAll('.exd-window .exd-plate.bar')].length>0")
ANY_DOOR_PLATE = ("document.querySelectorAll('.exd-window .exd-plate.show').length")


def near_rgb(rgb_str, want, tol):
    m = re.findall(r"\d+", rgb_str or "")
    return len(m) >= 3 and all(abs(int(m[i]) - want[i]) <= tol for i in range(3))


def open_cold_door(br, base, tempo="1"):
    """a cold arrival with no stored walk → the standing door deals + breathes its five windows in."""
    br.navigate("about:blank")
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.reload()

# JS reads shared across rows
FIRST_IMG = "document.querySelector('.exh-frame img.work')"
PLATE = "document.getElementById('ex-plate')"
PLATE_SHOW = f"(()=>{{const p={PLATE};return !!p && !p.hidden && p.classList.contains('show')}})()"
PLATE_BAR = f"(()=>{{const p={PLATE};return !!p && p.classList.contains('bar')}})()"
MARKS = ("JSON.stringify(Object.fromEntries(performance.getEntriesByType('mark')"
         ".filter(m=>m.name.startsWith('ex:')).map(m=>[m.name.slice(3),m.startTime])))")


def held_walk(br, base, delay, tempo="1"):
    """boot a stored walk with the first image HELD `delay`s on the wire, at `tempo`."""
    br.navigate("about:blank")
    br.navigate(base + "/")
    br.evaluate(f"localStorage.setItem('ex.exhibition', {json.dumps(WALK)})")
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.reload()


if not chrome_available() or not _HAVE_PIL:
    reason = "Chrome not installed" if not chrome_available() else "Pillow absent (no tier ladder to bake)"
    for r in BROWSER_ROWS:
        skip(r, f"{reason} (pinned expected skip)")
else:
    HOLD = {}
    with serve(TMP, hold=HOLD) as base:
        # 0 · plate past the grace + fast link shows none (grace .35s, bar_wait 1.5s at tempo 1)
        # the plate's appearance is read from the `ex:plate` MARK, not a fixed-time live sample —
        # under parallel-suite CPU load boot can outrun a short sleep (the mark never lies).
        HOLD.update(match=str(PICK), delay=0.9)               # moderate: > grace, < bar_wait
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0.9)
            br.sleep(2.0)                                     # image lands, plate has come and gone
            marks_mod = json.loads(br.evaluate(MARKS) or "{}")
        HOLD.update(match=str(PICK), delay=0.05)              # fast: lands within the grace
        with Browser(width=1280, height=900) as br2:
            held_walk(br2, base, 0.05)
            br2.sleep(1.4)
            marks_fast = json.loads(br2.evaluate(MARKS) or "{}")
            fast_plate_on = br2.evaluate(PLATE_SHOW)
        check(BROWSER_ROWS[0],
              "plate" in marks_mod and "plate" not in marks_fast and not fast_plate_on,
              f"marks_mod={sorted(marks_mod)} marks_fast={sorted(marks_fast)}")

        # 1 · the plate wears the work's OWN baked dom tone (within a small per-channel tolerance)
        HOLD.update(match=str(PICK), delay=3.5)
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 3.5)
            # poll for the plate to stand (robust under load) — the image is held 3.5s, plenty of room
            for _ in range(24):
                br.sleep(0.1)
                if br.evaluate(PLATE_SHOW):
                    break
            bg = br.evaluate(f"(()=>{{const p={PLATE};return p?getComputedStyle(p).backgroundColor:'';}})()")
        m = re.findall(r"\d+", bg or "")
        near = (len(m) >= 3 and all(abs(int(m[i]) - PICK_DOM[i]) <= 6 for i in range(3)))
        check(BROWSER_ROWS[1], near, f"plate bg={bg} vs baked dom={PICK_DOM}")

        # 2 · the bar joins only past the long wait; 3 · it is wordless (same long-hold browser)
        HOLD.update(match=str(PICK), delay=4.0)
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 4.0)
            bar_on = False
            for _ in range(35):                              # poll past bar_wait (1.5s), image still held
                br.sleep(0.1)
                if br.evaluate(PLATE_BAR):
                    bar_on = True
                    break
            plate_text = br.evaluate(f"({PLATE}||{{}}).textContent||''")
            marks_long = json.loads(br.evaluate(MARKS) or "{}")
        check(BROWSER_ROWS[2],
              bar_on and "bar" in marks_long and "bar" not in marks_mod,   # long ⇒ bar; moderate ⇒ none
              f"long bar_on={bar_on} marks_long={sorted(marks_long)} marks_mod={sorted(marks_mod)}")
        check(BROWSER_ROWS[3],
              plate_text.strip() == "" and not re.search(r"\d", plate_text or ""),
              f"plate/bar textContent={plate_text!r} (must be empty, no digit)")

        # 4 · the reveal accelerates: within-grace ⇒ soft token (fast); plate-stood ⇒ reveal token
        REVEALED = f"(()=>{{const i={FIRST_IMG};return !!i && i.dataset.ladder==='done' && i.complete;}})()"
        HOLD.update(match=str(PICK), delay=0.05)
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0.05)
            for _ in range(30):
                br.sleep(0.1)
                if br.evaluate(REVEALED):
                    break
            fast_dur = br.evaluate(f"getComputedStyle({FIRST_IMG}).transitionDuration")
        HOLD.update(match=str(PICK), delay=2.4)               # > bar_wait: the plate stands, then reveals slow
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 2.4)
            for _ in range(50):
                br.sleep(0.1)
                if br.evaluate(REVEALED):
                    break
            slow_dur = br.evaluate(f"getComputedStyle({FIRST_IMG}).transitionDuration")

        def _secs(s):
            try:
                return float(str(s).replace("s", "").strip())
            except Exception:
                return None
        fd, sd = _secs(fast_dur), _secs(slow_dur)
        check(BROWSER_ROWS[4],
              fd is not None and sd is not None and fd < 1.0 and sd > 1.0 and sd > fd + 0.5,
              f"fast reveal={fast_dur} (soft .6s) slow reveal={slow_dur} (reveal 2s)")
        HOLD.clear()

        # 5 · the arm reads the settled state (F1): a warm image reveals at once — no plate, no clock.
        # A healthy local server lands the image fast → warm/within-grace path → the plate never marks.
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0)
            br.sleep(1.4)
            warm = br.evaluate(
                "(()=>{const i=" + FIRST_IMG + ";return {plate:" + PLATE_SHOW + ","
                "op:+getComputedStyle(i).opacity,ok:i&&i.complete&&i.naturalWidth>0};})()")
            marks_warm = json.loads(br.evaluate(MARKS) or "{}")
            check(BROWSER_ROWS[5],
                  not warm["plate"] and "plate" not in marks_warm and warm["ok"] and warm["op"] > 0.5,
                  f"warm={warm} marks={sorted(marks_warm)}")

        # 6 · a post-reveal tier swap never re-plates (F6): reveal warm, then resize (tier changes),
        # the shown photo stays painted — no plate, no re-arm.
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0)
            br.sleep(1.4)                                     # revealed
            br.set_viewport(760, 900)                         # a width change → the browser may pick a new tier
            br.sleep(0.8)
            after = br.evaluate(
                "(()=>{const i=" + FIRST_IMG + ";return {plate:" + PLATE_SHOW + ","
                "op:+getComputedStyle(i).opacity};})()")
            marks_swap = json.loads(br.evaluate(MARKS) or "{}")
            check(BROWSER_ROWS[6],
                  not after["plate"] and "plate" not in marks_swap and after["op"] > 0.5,
                  f"after resize={after} marks={sorted(marks_swap)}")

        # 7 · rotation mid-flight keeps the plate (never back to black; the grace clock does not restart)
        HOLD.update(match=str(PICK), delay=4.0)
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 4.0)
            before = False
            for _ in range(30):                              # poll for the plate to stand (robust under load)
                br.sleep(0.1)
                if br.evaluate(PLATE_SHOW):
                    before = True
                    break
            br.set_viewport(900, 1200)                        # a rotation while the plate stands
            br.sleep(0.4)
            still = br.evaluate(PLATE_SHOW)                   # the plate persists, refit — never re-blacked
            check(BROWSER_ROWS[7], before and still, f"before={before} after_rotate={still}")
        HOLD.clear()

        # 8 · the door + crossing stay unladdered: no plate at a cold door; a warm crossing lays none
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','1')")
            br.reload()
            br.sleep(1.0)
            door_plate = br.evaluate(PLATE_SHOW)              # the threshold: no plate ladder
            br.click(".exd-window:nth-child(1)", settle=0.1)  # a warm crossing (door pre-fetched it)
            br.sleep(2.6)
            cross_marks = json.loads(br.evaluate(MARKS) or "{}")
            check(BROWSER_ROWS[8],
                  not door_plate and "plate" not in cross_marks,
                  f"door_plate={door_plate} crossing marks={sorted(cross_marks)}")

        # 9 · composes with the tier ladder: the revealed photo is the browser's srcset tier (INV-63)
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0)
            br.sleep(1.4)
            cur = br.evaluate(f"({FIRST_IMG}||{{}}).currentSrc||''")
            has_srcset = br.evaluate(f"!!({FIRST_IMG}||{{}}).getAttribute && !!{FIRST_IMG}.getAttribute('srcset')")
            check(BROWSER_ROWS[9],
                  bool(has_srcset) and bool(re.search(r"-(?:640|960|1280)\.png", cur or "")),
                  f"currentSrc={cur} has_srcset={has_srcset}")

        # 10 + 11 · the next work preloads one-ahead, exactly one, never the arc. Rest at the LAST
        # shown frame: its forward next is order[shown], which has NO appended frame — only the
        # preload fetches it, so an image request for a work NOT in the DOM proves the one-ahead.
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0)
            br.sleep(1.4)
            shown_ids = br.evaluate(
                "JSON.stringify([...document.querySelectorAll('.exh-frame')].map(f=>f.dataset.id))")
            shown_ids = set(json.loads(shown_ids or "[]"))
            br.net_capture()                                 # watch the wire from here
            br.evaluate("[...document.querySelectorAll('.exh-frame')].slice(-1)[0]"
                        ".scrollIntoView({block:'center',behavior:'instant'})")
            br.sleep(1.2)                                     # the last frame rests → preload one ahead
            pre = br.evaluate("JSON.stringify(window.__exPreload||null)")
            pre = json.loads(pre or "null")
            log = br.net_log()
            ahead_ids = [i for i in work_ids_in(log) if i not in shown_ids]
            check(BROWSER_ROWS[10],
                  len(ahead_ids) >= 1 and pre and str(pre.get("id")) in ahead_ids,
                  f"ahead_ids={ahead_ids} __exPreload={pre}")
            check(BROWSER_ROWS[11],
                  len(ahead_ids) <= 1,          # preload_ahead=1: never the deeper arc (INV-25/30)
                  f"distinct works fetched ahead={ahead_ids} (want ≤ 1)")

        # 12 · the preload re-aims on a turn (F5): resting forward warms order[+1]; a backward step
        # abandons it and aims the warm-ahead the other way.
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0)
            br.sleep(1.4)
            # step forward twice, then read the forward target
            br.key("ArrowDown"); br.sleep(0.7)
            br.key("ArrowDown"); br.sleep(0.9)
            fwd = json.loads(br.evaluate("JSON.stringify(window.__exPreload||null)") or "null")
            br.key("ArrowUp"); br.sleep(0.9)                 # a TURN — the feet reverse
            back = json.loads(br.evaluate("JSON.stringify(window.__exPreload||null)") or "null")
            check(BROWSER_ROWS[12],
                  fwd and back and fwd.get("dir") == 1 and back.get("dir") == -1
                  and fwd.get("id") != back.get("id"),
                  f"forward={fwd} after_turn={back}")

        # 13 · a failed preload is silent (F5): block the discovered next-work file, re-enter and
        # rest — the blocked preload errors nothing, the walk stays alive, the in-view frame reveals.
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 0)
            br.sleep(1.4)
            br.evaluate("[...document.querySelectorAll('.exh-frame')].slice(-1)[0]"
                        ".scrollIntoView({block:'center',behavior:'instant'})")
            br.sleep(1.0)
            pre = json.loads(br.evaluate("JSON.stringify(window.__exPreload||null)") or "null")
        with Browser(width=1280, height=900) as br:
            if pre and pre.get("id"):
                br.block([f"*{pre['id']}*"])                 # the one-ahead file will fail
            held_walk(br, base, 0)
            br.sleep(1.4)
            br.evaluate("[...document.querySelectorAll('.exh-frame')].slice(-1)[0]"
                        ".scrollIntoView({block:'center',behavior:'instant'})")
            br.sleep(1.2)
            alive = br.evaluate("(()=>{try{return 1+1===2 && !!document.querySelector('.exh-frame');}"
                                "catch(e){return false;}})()")
            in_view_ok = br.evaluate(
                "(()=>{const f=[...document.querySelectorAll('.exh-frame')]"
                ".find(x=>{const r=x.getBoundingClientRect();"
                "return r.top<innerHeight*0.5&&r.bottom>innerHeight*0.5;});"
                "if(!f)return false;const i=f.querySelector('img.work');"
                "return !!i && (+getComputedStyle(i).opacity>0.3 || !i.complete || i.naturalWidth>0);})()")
            br.block([])
            check(BROWSER_ROWS[13],
                  bool(alive) and bool(in_view_ok),
                  f"blocked={pre} alive={alive} in_view_ok={in_view_ok}")

        # 14 · DL1 — a door window rides the ladder. Cold door with EVERY window image held on the
        # wire; we read whichever window renders (the hand is live). (a) moderate hold ⇒ the window
        # wears its OWN raw dom as a plate past the grace, no bar yet; (b) long hold ⇒ the wordless
        # bar joins past bar_wait, plate+bar carry no digit; (c) a healthy (fast) door shows NO plate —
        # the windows reveal at once. The plate is the window's own `.exd-plate` (five may fly at
        # once), never the walk's single `#ex-plate`.
        HOLD.update(match=DOOR_ASSETS, delay=0.9)             # moderate: > grace, < bar_wait, all windows
        with Browser(width=1280, height=900) as br:
            open_cold_door(br, base)
            first = ""
            for _ in range(35):                               # poll for a window to plate
                br.sleep(0.1)
                first = br.evaluate(FIRST_DOOR_PLATE)
                if first:
                    break
        mod = json.loads(first or "{}")
        mod_dom = BYID[str(mod.get("id"))]["dom"] if mod.get("id") in BYID else None
        raw_tone = bool(mod_dom) and near_rgb(mod.get("bg"), mod_dom, 6)
        mod_bar = bool(mod.get("bar"))                        # a moderate hold shows NO bar yet

        HOLD.update(match=DOOR_ASSETS, delay=4.0)             # long: past bar_wait — the bar joins
        with Browser(width=1280, height=900) as br:
            open_cold_door(br, base)
            bar_on = False
            for _ in range(45):
                br.sleep(0.1)
                if br.evaluate(ANY_DOOR_BAR):
                    bar_on = True
                    break
            longp = json.loads(br.evaluate(FIRST_DOOR_PLATE) or "{}")
        plate_text = longp.get("text", "")
        wordless = (plate_text.strip() == "" and not re.search(r"\d", plate_text or ""))
        HOLD.clear()

        with Browser(width=1280, height=900) as br:           # healthy: the windows reveal at once
            open_cold_door(br, base)
            br.sleep(1.6)
            fast_plate = int(br.evaluate(ANY_DOOR_PLATE) or 0)
            fast_revealed = br.evaluate(
                "(()=>{const i=document.querySelector('.exd-window img');"
                "return !!i && i.complete && i.naturalWidth>0 && +getComputedStyle(i).opacity>0.5;})()")
        check(BROWSER_ROWS[14],
              bool(mod.get("id")) and raw_tone and not mod_bar and bar_on and wordless
              and fast_plate == 0 and bool(fast_revealed),
              f"plated_id={mod.get('id')} raw_tone={raw_tone}(bg={mod.get('bg')} vs dom={mod_dom}) "
              f"mod_bar={mod_bar} long_bar={bar_on} wordless={wordless}(text={plate_text!r}) "
              f"fast_plate={fast_plate} fast_revealed={fast_revealed}")

        # 15 · DL2 — the door ladder composes with the entrance + halo, and a cached re-render
        # re-flashes no plate (the settled read, prover seam 5). While a held window's plate stands:
        # the window's breathe-in entrance (exd-rise) is intact, and its halo still speaks liveAccent
        # while the plate speaks the RAW dom — two colour laws on two elements. Then a resize that
        # rebuilds the door over already-cached windows flashes no plate on any window.
        HOLD.update(match=DOOR_ASSETS, delay=0.9)             # hold every window so a plate stands during the read
        with Browser(width=1280, height=900) as br:
            open_cold_door(br, base)
            first = ""
            for _ in range(35):
                br.sleep(0.1)
                first = br.evaluate(FIRST_DOOR_PLATE)
                if first:
                    break
        c = json.loads(first or "{}")
        cdom = BYID[str(c.get("id"))]["dom"] if c.get("id") in BYID else None
        stood = bool(c.get("id"))
        rise_ok = "exd-rise" in (c.get("rise") or "")        # the entrance survives the plate (EX-DOOR-2b)
        halo_ok = bool(cdom) and near_rgb(c.get("glow"), live_accent(cdom), 3)   # halo == liveAccent
        plate_raw = bool(cdom) and near_rgb(c.get("bg"), cdom, 6)                # plate == raw dom
        HOLD.clear()

        with Browser(width=1280, height=900) as br:           # cached re-render: no plate flash
            open_cold_door(br, base)
            br.sleep(1.8)                                      # the windows land + cache
            settled_plate = int(br.evaluate(ANY_DOOR_PLATE) or 0)
            br.set_viewport(820, 1180)                         # portrait → doorRender rebuilds (count change)
            flashed = 0
            for _ in range(10):                                # watch the rebuild settle — cached ⇒ no plate
                br.sleep(0.1)
                flashed = max(flashed, int(br.evaluate(ANY_DOOR_PLATE) or 0))
        check(BROWSER_ROWS[15],
              stood and rise_ok and halo_ok and plate_raw and settled_plate == 0 and flashed == 0,
              f"stood={stood} id={c.get('id')} rise={c.get('rise')!r} "
              f"halo_ok={halo_ok}(glow={c.get('glow')} vs {live_accent(cdom) if cdom else None}) "
              f"plate_raw={plate_raw}(plate={c.get('bg')} vs dom={cdom}) "
              f"settled_plate={settled_plate} rerender_flashed={flashed}")

        # 16–18 · EX-LADDER holds on EVERY surface that hangs a work, not only the walk. A door
        # window and both series faces used to fetch the full display file into a 160px / 64vw /
        # 150px box; each hands its own box now and the browser picks the tier that fits.
        TIER = r"-(?:640|960|1280)\.png"

        def ladder_of(br, sel):
            return json.loads(br.evaluate(
                "(()=>{const i=document.querySelector('%s');if(!i)return JSON.stringify({no:1});"
                "return JSON.stringify({srcset:i.getAttribute('srcset')||'',"
                "sizes:i.getAttribute('sizes')||'',cur:i.currentSrc||''});})()" % sel) or "{}")

        with Browser(width=1280, height=900) as br:
            open_cold_door(br, base)
            br.sleep(1.8)
            win = ladder_of(br, ".exd-window img")
            check(BROWSER_ROWS[16],
                  bool(win.get("srcset")) and win.get("sizes", "").endswith("px")
                  and bool(re.search(TIER, win.get("cur") or "")),
                  f"window={win}")

        SERIES = DATA.get("series") or []
        LANE = next((s for s in SERIES if s["variant"] == "lane"), None)
        PRINTS = next((s for s in SERIES if s["variant"] == "polaroids"), None)

        def open_series(br, member):
            br.navigate(base + "/")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('ex-tempo','0.2')")
            br.evaluate("localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:10}))"
                        % (json.dumps(VER), json.dumps(member)))
            br.reload()
            br.sleep(1.3)
            br.click("#exh-cap .ex-series", settle=0.8)

        if LANE:
            with Browser(width=1280, height=900) as br:
                open_series(br, LANE["members"][0])
                lane = ladder_of(br, ".exs-stage.lane img")
                check(BROWSER_ROWS[17],
                      bool(lane.get("srcset")) and bool(lane.get("sizes"))
                      and bool(re.search(TIER, lane.get("cur") or "")),
                      f"lane={lane}")
        else:
            skip(BROWSER_ROWS[17], "the fixture bakes no lane series")

        if PRINTS:
            with Browser(width=1280, height=900) as br:
                open_series(br, PRINTS["members"][0])
                prints = json.loads(br.evaluate(
                    "JSON.stringify([...document.querySelectorAll('.exs-print img')].map(i=>({"
                    "srcset:i.getAttribute('srcset')||'',sizes:i.getAttribute('sizes')||'',"
                    "cur:i.currentSrc||''})))") or "[]")
                # Every polaroid wears the ladder and its own thumb-sized box. A work already hanging
                # on the walk keeps the big tier it fetched there — the browser is free to reuse a
                # cached candidate — so the saving is read on the COLD ones: a thumb pulls 640.
                all_rigged = bool(prints) and all(p["srcset"] and p["sizes"] for p in prints)
                cold_small = any(re.search(r"-640\.png", p.get("cur") or "") for p in prints)
                tiers = [(re.search(TIER, p.get("cur") or "") or [""])[0] for p in prints]
                check(BROWSER_ROWS[18], all_rigged and cold_small,
                      f"n={len(prints)} rigged={all_rigged} cold_small={cold_small} tiers={tiers}")
        else:
            skip(BROWSER_ROWS[18], "the fixture bakes no polaroid series")

        # 19 · EX-LOAD-FRAME: the walk's plate IS the loading frame (the ex-crossing/ex-cross-cap
        # sibling for the in-walk wait, his 2026-07-22 note). While the walk plate stands, body carries
        # ex-loading-frame — the class that retracts the chrome (share/player/plaque, static CSS) and
        # stands the counter alone with a "loading" mark; the instant the picture lands, the plate
        # retires and the frame clears. Read browser-COMPUTED: the counter's ::after actually RENDERS
        # the "loading" word while the frame stands (the class is live and drives CSS), and clears on
        # land. Held 3.0s so the plate stands well past the .35s grace, then let it land.
        FRAME_PROBE = (
            "(()=>{const b=document.body.classList.contains('ex-loading-frame');"
            "const c=document.getElementById('exh-counter');"
            "const after=c?getComputedStyle(c,'::after').content:'';"
            "return JSON.stringify({frame:b,mark:!!(c&&c.classList.contains('loading')),"
            "markShown:/loading/.test(after||'')});})()")
        HOLD.update(match=str(PICK), delay=3.0)
        with Browser(width=1280, height=900) as br:
            held_walk(br, base, 3.0)
            stood = {}
            for _ in range(30):                          # poll the plate up (held 3.0s, ample room)
                br.sleep(0.1)
                if br.evaluate(PLATE_SHOW):
                    stood = json.loads(br.evaluate(FRAME_PROBE)); break
            landed = {}
            for _ in range(50):                          # then the picture lands → plate + frame retire
                br.sleep(0.1)
                if not br.evaluate(PLATE_SHOW):
                    landed = json.loads(br.evaluate(FRAME_PROBE)); break
        check(BROWSER_ROWS[19],
              bool(stood.get("frame") and stood.get("mark") and stood.get("markShown"))
              and landed.get("frame") is False and landed.get("mark") is False
              and landed.get("markShown") is False,
              f"while the plate stood={stood}  after it landed={landed}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
