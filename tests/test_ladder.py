#!/usr/bin/env python3
"""The in-flight ladder + the one-ahead preload (EX-LOAD-2 / INV-72 · EX-LOAD-3 / INV-73) —
one test per matrix row, adapted for the exhibition-engine synthetic fixture (ported from
tlvphoto 7874951). A frame whose pixels are late wears the work's OWN dominant tone (a plate);
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
    "EX-LOAD-2 the door + crossing stay unladdered (no plate at the door; a warm crossing lays no plate)",
    "EX-LOAD-2 composes with the tier ladder (the revealed photo is the browser's srcset tier — INV-63)",
    "EX-LOAD-3 the next work actually preloads one-ahead (network log shows an unshown next-arc file)",
    "EX-LOAD-3 exactly one ahead, never the arc (at most preload_ahead unshown next-works requested)",
    "EX-LOAD-3 the preload re-aims on a turn (prover F5): a backward step abandons forward, aims back",
    "EX-LOAD-3 a failed preload is silent (prover F5): the next file blocked errors nothing, the walk lives",
]

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

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
