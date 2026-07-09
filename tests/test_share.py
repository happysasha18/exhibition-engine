#!/usr/bin/env python3
"""Sharing from the walk (EX-SHARE / EX-SHARE-BTN / EX-SHARE-IN, INV-36) — adapted for
exhibition-engine synthetic fixture. Run: python tests/test_share.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_share_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
ALL_IDS = [w["id"] for w in DATA["works"]]
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps(json.dumps({"v": VER, "pick": PICK, "shown": 10}))

# ---------------------------------------------------------------- data + string rows
greet = DATA.get("greet") or {}
langs = (greet.get("langs") or {})
missing = [c for c, L in langs.items() if not (L.get("share_copied") or "").strip()]
chk = subprocess.run([sys.executable, str(ROOT / "scripts" / "gen_greetings.py"), "--check"],
                     capture_output=True, text=True)
# engine/assets/ has exhibition.js (adapted from assets_src/)
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
check("EX-SHARE toast strings ride the one cache (7 langs baked · validator knows the field · RU built-in)",
      len(langs) == 7 and not missing and chk.returncode == 0
      and "ссылка скопирована" in js_src,
      f"langs={len(langs)} missing={missing} check_rc={chk.returncode} "
      f"builtin={'ссылка скопирована' in js_src}")

BROWSER_ROWS = [
    "EX-SHARE-BTN one FLOATING button copies, never navigates (fixed chrome above the room; toast; no ↗/`/w/`)",
    "EX-SHARE-BTN the copied line is canonical AND follows the eye (root + house utm + #w-<work IN VIEW>)",
    "EX-SHARE-BTN touch vs hover (hover:none → present ≥44px; hover:hover → rests QUIET, lifts on hover+focus)",
    "EX-SHARE-BTN clipboard refusal → the toast CARRIES the link and stays until dismissed (Esc)",
    "EX-SHARE-BTN the chrome leaves off the works (closing screen + door → the floating button hides)",
    "EX-SHARE-IN cold `/#w-<id>` = handed-over pick (inside the room AT the work; no door/greeting/ceremony)",
    "EX-SHARE-IN shown-frame jump never tears (instant, the arc unchanged, walk continues)",
    "EX-SHARE-IN unshown work acts as a pick (arc re-seeds fresh-top; budget stays derived+capped)",
    "EX-SHARE-IN the hash is consumed once (reload honors the place; no history step; the address keeps the line)",
    "EX-SHARE-IN unknown id is silence (bare arrival, no error face)",
    "EX-SHARE-IN composes with the wipe (?reset#w-<id> → wipe first, then the hash seeds the arrival)",
]

CLIP_STUB = (
    "window.__copied=[];"
    "if(navigator.clipboard)navigator.clipboard.writeText="
    "(t)=>{window.__copied.push(t);return Promise.resolve();};"
)
CLIP_REFUSE = (
    "window.__copied=[];"
    "if(navigator.clipboard)navigator.clipboard.writeText="
    "(t)=>Promise.reject(new Error('denied'));"
)
AT_DOOR = "document.body.classList.contains('ex-door')"
GREETED = "(()=>{const g=document.getElementById('exd-greet');return !!g && !g.hidden})()"
FRAME_IDS = ("JSON.stringify([...document.querySelectorAll('.exh-frame')]"
             ".map(f=>f.dataset.id))")
IN_VIEW = ("(()=>{const f=[...document.querySelectorAll('.exh-frame')].find(f=>{"
           "const r=f.getBoundingClientRect();"
           "return r.top<innerHeight*0.5 && r.bottom>innerHeight*0.5;});"
           "return f?f.dataset.id:null;})()")
TOAST = "(()=>{const t=document.getElementById('ex-toast');return t&&!t.hidden?t.textContent:null;})()"


def enter(br, base, tempo="0.2"):
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("sessionStorage.clear()")
    br.evaluate(f"localStorage.setItem('tlv-tempo','{tempo}')")
    br.reload()
    br.sleep(1.0)
    br.click(".exd-window:nth-child(1)", settle=0.1)
    br.sleep(1.2)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # 0+1 · the button copies (never navigates), the line is canonical
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.navigate(base + "/?x=1")
            br.evaluate("localStorage.clear();sessionStorage.clear()")
            br.evaluate("localStorage.setItem('tlv-tempo','0.2')")
            br.reload()
            br.sleep(1.0)
            br.click(".exd-window:nth-child(1)", settle=0.1)
            br.sleep(1.2)
            frames = json.loads(br.evaluate(FRAME_IDS) or "[]")
            chrome = br.evaluate(
                "(()=>{const bs=[...document.querySelectorAll('.ex-share')];const b=bs[0];"
                "return JSON.stringify({count:bs.length,tag:b?b.tagName:'',"
                "fixed:b?getComputedStyle(b).position:'',"
                "in_frame:!!document.querySelector('.exh-frame .ex-share'),"
                "label:((b&&b.getAttribute('aria-label'))||'').length>0,"
                "shown:b?+getComputedStyle(b).opacity:0,"
                "opens:document.querySelectorAll('#ex-stage a[href*=\"/w/\"], .ex-open').length});})()")
            chrome = json.loads(chrome)
            path0 = br.evaluate("location.pathname")
            first_in_view = br.evaluate(IN_VIEW)
            br.click(".ex-share", settle=0.4)
            copied = json.loads(br.evaluate("JSON.stringify(window.__copied)") or "[]")
            toast = br.evaluate(TOAST)
            same_place = (br.evaluate("location.pathname") == path0
                          and br.evaluate(IN_VIEW) == first_in_view)
            check(BROWSER_ROWS[0],
                  len(frames) == 10 and chrome["count"] == 1 and chrome["tag"] == "BUTTON"
                  and chrome["fixed"] == "fixed" and not chrome["in_frame"]
                  and chrome["label"] and chrome["shown"] > 0.3 and chrome["opens"] == 0
                  and len(copied) == 1 and toast is not None and same_place,
                  f"frames={len(frames)} chrome={chrome} copied={copied} "
                  f"toast={toast!r} same_place={same_place}")
            # …and the target FOLLOWS THE EYE: step to the next work, copy again → its id;
            # the utm rides before the hash so shared arrivals separate from Direct/bot noise
            br.key("ArrowDown")
            br.sleep(0.6)
            second_in_view = br.evaluate(IN_VIEW)
            br.click(".ex-share", settle=0.4)
            copied = json.loads(br.evaluate("JSON.stringify(window.__copied)") or "[]")
            check(BROWSER_ROWS[1],
                  copied == [f"{SITE_URL}/?utm_source=share&utm_medium=referral#w-{frames[0]}",
                             f"{SITE_URL}/?utm_source=share&utm_medium=referral#w-{second_in_view}"]
                  and second_in_view == frames[1],
                  f"copied={copied} in_view={second_in_view} (page had ?x=1; the second copy "
                  f"must carry the work in view)")

            # 4 · the chrome leaves off the works: closing screen + door hide the floating button
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.6)
            fin_op = br.evaluate("+getComputedStyle(document.querySelector('.ex-share')).opacity")
            br.click("#ex-return", settle=0.8)
            door_op = br.evaluate("+getComputedStyle(document.querySelector('.ex-share')).opacity")
            check(BROWSER_ROWS[4], fin_op < 0.05 and door_op < 0.05,
                  f"fin_opacity={fin_op} door_opacity={door_op} (want both ≈0)")

        # 2 · touch vs hover faces
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.touch(True)
            enter(br, base)
            touch = br.evaluate(
                "(()=>{const b=document.querySelector('.ex-share');"
                "const s=getComputedStyle(b);const r=b.getBoundingClientRect();"
                "const w=document.querySelector('.exh-frame img.work').getBoundingClientRect();"
                "const overlap=!(r.right<w.left||r.left>w.right||r.bottom<w.top||r.top>w.bottom);"
                "return {op:+s.opacity,w:r.width,h:r.height,overlap};})()")
            br.touch(False)
            br.reload()
            br.sleep(1.2)
            rest_op = br.evaluate(
                "+getComputedStyle(document.querySelector('.ex-share')).opacity")
            br.hover(".ex-share")
            br.sleep(0.4)
            hover_op = br.evaluate(
                "+getComputedStyle(document.querySelector('.ex-share')).opacity")
            br.evaluate("document.querySelector('.ex-share').focus()")
            focus_vis = br.evaluate(
                "document.querySelector('.ex-share')===document.activeElement")
            check(BROWSER_ROWS[2],
                  touch["op"] > 0.7 and touch["w"] >= 44 and touch["h"] >= 44
                  and not touch["overlap"]
                  and 0.3 < rest_op < 0.8 and hover_op > 0.9 and focus_vis,
                  f"touch={touch} rest={rest_op} hover={hover_op} focusable={focus_vis}")

        # 3 · clipboard refusal → the toast carries the link, stays until dismissed
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_REFUSE)
            enter(br, base)
            frames = json.loads(br.evaluate(FRAME_IDS) or "[]")
            br.click(".ex-share", settle=0.5)
            toast1 = br.evaluate(TOAST) or ""
            br.sleep(2.5)
            toast2 = br.evaluate(TOAST) or ""
            br.key("Escape")
            br.sleep(0.4)
            gone = br.evaluate(TOAST) is None
            link = f"{SITE_URL}/?utm_source=share&utm_medium=referral#w-{frames[0]}"
            check(BROWSER_ROWS[3],
                  link in toast1 and link in toast2 and gone,
                  f"toast1={toast1!r} still={toast2!r} gone_after_esc={gone}")

        # 5 · cold arrival with the hash = handed-over pick
        target = ALL_IDS[len(ALL_IDS) // 2]
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.navigate(base + "/#w-" + target)
            br.sleep(1.4)
            state = br.evaluate(
                "(()=>{return {door:" + AT_DOOR + ",greet:" + GREETED + ","
                "crossing:document.body.classList.contains('ex-crossing'),"
                "inview:" + IN_VIEW + ","
                "first:(document.querySelector('.exh-frame')||{dataset:{}}).dataset.id};})()")
            check(BROWSER_ROWS[5],
                  not state["door"] and not state["greet"] and not state["crossing"]
                  and state["first"] == target and state["inview"] == target,
                  f"state={state} target={target}")

        # 6+7+8 · a stored walk
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.navigate(base + "/")
            br.evaluate(f"localStorage.setItem('tlv.exhibition', {WALK})")
            br.evaluate("localStorage.setItem('tlv-tempo','0.2')")
            br.reload()
            br.sleep(1.2)
            shown_ids = json.loads(br.evaluate(FRAME_IDS) or "[]")
            jump_to = shown_ids[3]
            br.navigate(base + "/#w-" + jump_to)
            br.sleep(1.0)
            after_ids = json.loads(br.evaluate(FRAME_IDS) or "[]")
            walk_kept = json.loads(br.evaluate(
                "localStorage.getItem('tlv.exhibition')") or "{}")
            check(BROWSER_ROWS[6],
                  after_ids == shown_ids and br.evaluate(IN_VIEW) == jump_to
                  and walk_kept.get("pick") == PICK,
                  f"arc_same={after_ids == shown_ids} inview={br.evaluate(IN_VIEW)} "
                  f"want={jump_to} pick={walk_kept.get('pick')}")

            unshown = next(i for i in ALL_IDS if i not in shown_ids)
            br.navigate(base + "/#w-" + unshown)
            br.sleep(1.2)
            re_ids = json.loads(br.evaluate(FRAME_IDS) or "[]")
            walk_new = json.loads(br.evaluate(
                "localStorage.getItem('tlv.exhibition')") or "{}")
            check(BROWSER_ROWS[7],
                  re_ids and re_ids[0] == unshown and len(re_ids) == 10
                  and walk_new.get("pick") == unshown and walk_new.get("shown") == 10,
                  f"first={re_ids[:2]} n={len(re_ids)} walk={walk_new}")

            hl = br.evaluate("history.length")
            hash_kept = br.evaluate("location.hash") == "#w-" + unshown
            br.evaluate(
                "document.querySelectorAll('.exh-frame')[3]"
                ".scrollIntoView({behavior:'instant'})")
            br.sleep(0.8)
            walked_to = br.evaluate(IN_VIEW)
            br.reload()
            br.sleep(1.2)
            landed = br.evaluate(IN_VIEW)
            hash_still = br.evaluate("location.hash") == "#w-" + unshown
            check(BROWSER_ROWS[8],
                  hash_kept and hash_still and landed == walked_to != unshown
                  and br.evaluate("history.length") == hl,
                  f"hash={hash_kept}/{hash_still} walked_to={walked_to} landed={landed} "
                  f"hlen={hl}→{br.evaluate('history.length')}")

        # 9 · unknown id is silence
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.navigate(base + "/#w-nonsense")
            br.sleep(1.2)
            n_win = br.evaluate("document.querySelectorAll('.exd-window').length")
            check(BROWSER_ROWS[9],
                  br.evaluate(AT_DOOR) and n_win > 0 and br.evaluate("1+1") == 2,
                  f"door={br.evaluate(AT_DOOR)} windows={n_win}")

        # 10 · ?reset#w-<id>
        with Browser(width=1280, height=900) as br:
            br.inject(CLIP_STUB)
            br.navigate(base + "/")
            br.evaluate(f"localStorage.setItem('tlv.exhibition', {WALK})")
            br.navigate(base + "/?reset#w-" + target)
            br.sleep(1.4)
            walk_now = json.loads(br.evaluate(
                "localStorage.getItem('tlv.exhibition')") or "{}")
            check(BROWSER_ROWS[10],
                  not br.evaluate(AT_DOOR)
                  and br.evaluate(IN_VIEW) == target
                  and walk_now.get("pick") == target
                  and br.evaluate("location.search") == ""
                  and br.evaluate("location.hash") == "#w-" + target,
                  f"inview={br.evaluate(IN_VIEW)} walk={walk_now} "
                  f"search={br.evaluate('location.search')!r} hash={br.evaluate('location.hash')!r}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
