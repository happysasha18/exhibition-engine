#!/usr/bin/env python3
"""Batch-C — the screen-reader pole of the input-modality axis (CS-9 / INV-102, N7-A11Y).

Asserts the accessibility contract the walk owes a screen reader, all against the REAL baked bundle
and a REAL headless Chrome:
  · C-BAKE  every walk `works` record carries a non-empty `desc` = the work's /w-page / static-index alt
  · C1      every walk frame <img> speaks a real alt = the work's desc (never the always-`alt=""` defect)
  · C3      the walk frame names itself a photograph (role + aria-label present)
  · C2      two polite live regions exist beside the toast, distinct nodes/ids (three live nodes total)
  · C2/F5   a walk step REPLACES the caption region; a story portion APPENDS; results ride a SEPARATE region
  · C4/C5   the four modal layers (gift·zoom·quiz·series) each carry an accessible name (aria-label)
  · C6      the series polaroids + lane images speak (alt = the work's desc)
  · C7      the inspected (zoomed) image speaks (alt = the inspected work's desc)
  · C8      the gift prize / won-wallpaper thumbnail speaks (non-empty alt)

Chrome absent → pinned expected SKIPs, like every browser suite. Run: python tests/test_a11y.py
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

SITE_URL = "https://synth.example.com"
NS_UPPER = "EX"                       # the engine bake's global namespace (localStorage 'ex-tempo', window.EXQuiz)
results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def wait_for(br, expr, timeout=5.0, step=0.2):
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


# ---------------------------------------------------------------- bake once (story + quiz on)
TMP = Path(tempfile.mkdtemp(prefix="synth_a11y_"))
build_site.OUT = TMP
build_site.build(SITE_URL, enable=["ai_story", "quiz"])

EXDATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
WORKS = EXDATA["works"]
DESC_BY_ID = {str(w["id"]): (w.get("desc") or "") for w in WORKS}
QUIZ_IDS = [str(w["id"]) for w in WORKS if w.get("quiz")]
SERIES = EXDATA.get("series") or []
INDEX = (TMP / "index.html").read_text(encoding="utf-8")

# ---------------------------------------------------------------- data rows (always run)

# C-BAKE (OS-A2): every walk record carries a non-empty `desc`
no_desc = [str(w["id"]) for w in WORKS if not (w.get("desc") or "").strip()]
check("C-BAKE every walk `works` record carries a non-empty `desc` (OS-A2 / CS-5) — the alt source the "
      "client helper reads at every img site",
      len(WORKS) > 0 and not no_desc,
      f"works={len(WORKS)} without_desc={no_desc[:8]}")

# C-BAKE cross-check: each work's `desc` equals the SAME work's alt on the crawlable static index
# (render_exhibition's grid — an independent build path), so the walk speaks the /w-page description
import re  # noqa: E402
index_alt = {}
for m in re.finditer(r'<img src="/gallery/([^"]+)" alt="([^"]*)"', INDEX):
    index_alt[m.group(1)] = m.group(2)
mismatched = []
for w in WORKS:
    img_rel = (w.get("img") or "").split("/gallery/")[-1]
    want = index_alt.get(img_rel)
    if want is not None:
        # the static index escapes for HTML; unescape the few entities the alt can carry
        un = (want.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
        if (w.get("desc") or "") != un:
            mismatched.append(str(w["id"]))
check("C-BAKE the walk `desc` equals the work's static-index alt (the same description its /w page renders, "
      "CS-5) — one string across surfaces, not a divergent second copy",
      len(index_alt) > 0 and not mismatched,
      f"index_alts={len(index_alt)} mismatched={mismatched[:8]}")

# ---------------------------------------------------------------- Batch-D — the ENGINE SIBLING pole
# The engine forks D1-D3 of the input-modality axis (CS-9 / INV-102, N7-A11Y). String level against the
# SHIPPED baked bundle — exactly test_beat_css.py's level (substring/regex on the served exhibition.css +
# exhibition.js text). One CSS owner (engine/assets/exhibition.css) carries the viewport metric and the
# safe insets; the one series-lane decode is guarded in engine/client/16-renderhang-series.js.
#   · D1  the viewport-height metric follows the dynamic viewport — 100dvh with a 100vh fallback FIRST
#         (the fallback line BEFORE the dvh line, so a non-supporting engine keeps the old value), on the
#         body, the walk frame (.exh-frame), and the finale (.exh-fin)
#   · D2  every fixed control honours env(safe-area-inset-*) — the sound control top, the share control
#         bottom, the toast bottom — matching the pattern the zoom-close × already carries (css:659)
#   · D3  the series-lane img.decode() is feature-guarded (if (im.decode)) like its three siblings
# D1's iOS no-jump proof is a REAL-DEVICE walk (his phone, pinned in the skip-set) — NOT asserted here.
D_CSS = (TMP / "exhibition.css").read_text(encoding="utf-8")
D_JS = (TMP / "exhibition.js").read_text(encoding="utf-8")


def _css_block(selector):
    """The FIRST `selector{ ... }` declaration block body — the primary rule, never a .show/@media variant."""
    m = re.search(re.escape(selector) + r"\s*\{([^}]*)\}", D_CSS)
    return m.group(1) if m else None


# D1 — the dynamic-viewport metric, the vh fallback FIRST, on the three height metrics
for _sel, _prop in (("body", "min-height"), (".exh-frame", "height"), (".exh-fin", "height")):
    _b = _css_block(_sel)
    _ok = (_b is not None and "100dvh" in _b and "100vh" in _b
           and _b.index("100vh") < _b.index("100dvh"))
    check(f"D1 the {_prop} metric on `{_sel}` follows the dynamic viewport — 100dvh with a 100vh fallback FIRST "
          f"(engine sibling; EX-HANG / INV-102)",
          bool(_ok),
          f"block={(_b or '')[:120]!r}")

# D2 — env(safe-area-inset-*) on every fixed control, generalizing the zoom-close pattern (css:659)
for _sel, _inset in (("#ex-sound", "safe-area-inset-top"), (".ex-share", "safe-area-inset-bottom"),
                     ("#ex-toast", "safe-area-inset-bottom")):
    _b = _css_block(_sel)
    check(f"D2 the fixed control `{_sel}` honours env({_inset}) — no notch / home-indicator overlap "
          f"(engine sibling; EX-SOUND / EX-SHARE-BTN / INV-102)",
          _b is not None and ("env(" + _inset) in _b,
          f"block={(_b or '')[:160]!r}")

# D3-readout (movement folded decision, decided 2026-07-21) — the fixed READOUTS honour the safe insets
# too: the top-left work counter and the door corner language marker, generalizing D2's control class to
# readout chrome. A readout under the notch is unreadable — the same env() fix as the D2 controls.
for _sel, _inset in ((".exh-counter", "safe-area-inset-top"), (".exd-lang", "safe-area-inset-top")):
    _b = _css_block(_sel)
    check(f"D3-readout the fixed readout `{_sel}` honours env({_inset}) — no notch overlap "
          f"(engine sibling; EX-HANG / EX-LANG / INV-102)",
          _b is not None and ("env(" + _inset) in _b,
          f"block={(_b or '')[:160]!r}")

# D3 — the series-lane img.decode() is feature-guarded like its three siblings (06/07/12), no bare decode
_push = re.findall(r"decodes\.push\(\s*im\.decode\(", D_JS)
_guarded = re.findall(r"if\s*\(\s*im\.decode\s*\)\s*decodes\.push\(\s*im\.decode\(", D_JS)
check("D3 the series-lane img.decode() is feature-guarded (if (im.decode)) — no bare decode "
      "(engine sibling; EX-SERIES / INV-102)",
      len(_push) >= 1 and len(_guarded) == len(_push),
      f"push_sites={len(_push)} guarded={len(_guarded)}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "C1 every walk frame <img> carries a non-empty alt = the work's desc (never alt=\"\")",
    "C3 the walk frame names itself a photograph (non-empty role + aria-label)",
    "C2 three distinct polite live nodes exist (#ex-toast + #ex-live-cap + #ex-live-result, aria-live=polite)",
    "C2 a walk step REPLACES the caption region (the prior work's caption is gone, one caption node)",
    "C2/F5 a story portion APPENDS to the caption region (the caption stands; two portions accumulate)",
    "C2/F5 a gift result rides the SEPARATE result region while a story portion holds the caption region "
    "(a result and a story portion never share a node)",
    "C4/C5 the four modal layers (gift·zoom·quiz·series) each carry a non-empty accessible name (aria-label)",
    "C6 the series polaroids + lane images speak (each img's alt = its work's desc)",
    "C7 the inspected (zoomed) image speaks (alt = the inspected work's desc)",
    "C8 the gift prize / won-wallpaper thumbnail carries a non-empty alt",
]


def enter(br, base, tempo="0.4"):
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("sessionStorage.clear()")
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.reload()
    br.sleep(0.9)
    br.click(".exd-window:nth-child(1)", settle=0.1)
    br.sleep(1.2)


# --- JS probes ------------------------------------------------------------
FRAMES_ALT = (
    "JSON.stringify(Array.from(document.querySelectorAll('.exh-frame')).slice(0,4).map(f=>({"
    "id:f.dataset.id, alt:(f.querySelector('img.work')||{}).alt||'', "
    "role:f.getAttribute('role')||'', label:f.getAttribute('aria-label')||'', "
    "rdesc:f.getAttribute('aria-roledescription')||''})))"
)
LIVE_NODES = (
    "JSON.stringify(['ex-toast','ex-live-cap','ex-live-result'].map(id=>{"
    "const e=document.getElementById(id);return e?{id:id,live:e.getAttribute('aria-live')||''}:null;}))"
)
CAP_STATE = (
    "(()=>{const e=document.getElementById('ex-live-cap');if(!e)return 'null';"
    "return JSON.stringify({cap:Array.from(e.querySelectorAll('.ex-sr-cap')).map(x=>x.textContent),"
    "portions:Array.from(e.querySelectorAll('.ex-sr-portion')).map(x=>x.textContent),"
    "all:e.textContent||''});})()"
)
RESULT_STATE = "(()=>{const e=document.getElementById('ex-live-result');return e?(e.textContent||''):null;})()"
MODAL_LABELS = (
    "JSON.stringify(['ex-gift-card','ex-zoom','ex-quiz-card','ex-side'].map(id=>{"
    "const e=document.getElementById(id);return {id:id,"
    "label:e?(e.getAttribute('aria-label')||e.getAttribute('aria-labelledby')||''):null};}))"
)
# stub /api/story so a portion actually resolves under the static server (a deterministic line per id)
STUB_STORY = """
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/story')>=0){
    let ids=[];try{ids=JSON.parse(o.body).ids;}catch(e){}
    return Promise.resolve(new Response(JSON.stringify({
      story_variant:'B', lines: ids.map(id=>({id:String(id),line:'told '+id,source:'facts'}))
    }),{status:200,headers:{'Content-Type':'application/json'}}));
  }
  return _f.apply(this,arguments);};})();
"""
STUB_QUIZ_WIN = """
(function(){const _f=window.fetch;
window.fetch=function(u,o){
  if(String(u).indexOf('/api/quiz')>=0){
    return Promise.resolve(new Response(JSON.stringify({ok:true,prize:'gallery/quiz-prize-001.jpg'}),
      {status:200,headers:{'Content-Type':'application/json'}}));
  }
  return _f.apply(this,arguments);};})();
"""
# pinch a walk work open (two-finger touch) and read the zoom image's alt
PINCH_WORK_ZOOM = (
    "(()=>{const img=document.querySelector('.exh-frame img.work');"
    "if(!img)return JSON.stringify({err:'no-work'});"
    "const r=img.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;"
    "const id=img.closest('.exh-frame').dataset.id;"
    "const mk=(i,x,y)=>new Touch({identifier:i,target:img,clientX:x,clientY:y});"
    "const fire=(t,ts)=>img.dispatchEvent(new TouchEvent(t,{touches:ts,targetTouches:ts,"
    "changedTouches:ts,bubbles:true,cancelable:true}));"
    "fire('touchstart',[mk(1,cx-20,cy),mk(2,cx+20,cy)]);"
    "fire('touchmove',[mk(1,cx-60,cy),mk(2,cx+60,cy)]);"
    "const z=document.getElementById('ex-zoom');const zi=document.querySelector('#ex-zoom .exz-img');"
    "const out={opened:!!z&&!z.hidden,alt:zi?(zi.getAttribute('alt')||''):null,id:id};"
    "fire('touchend',[]);return JSON.stringify(out);})()"
)
# force-open a given series by injecting its chip into the caption and clicking it (fires the real
# delegated openSide handler), then read every room image's alt against its work's desc
OPEN_SERIES = (
    "(idx)=>{const c=document.getElementById('exh-cap');if(!c)return false;"
    "const b=document.createElement('button');b.className='ex-series';b.dataset.ser=String(idx);"
    "b.textContent='s';c.appendChild(b);b.click();return true;}"
)
ROOM_IMGS = (
    "(()=>{const st=document.getElementById('exs-stage');if(!st)return 'null';"
    "return JSON.stringify(Array.from(st.querySelectorAll('img')).map(im=>({"
    "id:(im.dataset.id||(im.closest('[data-id]')?im.closest('[data-id]').dataset.id:'')),"
    "alt:im.getAttribute('alt')||''})));})()"
)

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # C1 + C3 — the walk frames speak an alt and name themselves a photograph
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            frames = json.loads(br.evaluate(FRAMES_ALT) or "[]")
            c1_ok = len(frames) >= 2 and all(
                f["alt"].strip() and f["alt"] == DESC_BY_ID.get(str(f["id"]), "\0") for f in frames)
            check(BROWSER_ROWS[0], c1_ok, f"frames={frames[:3]}")
            c3_ok = len(frames) >= 2 and all(
                f["role"].strip() and f["label"].strip() and f["rdesc"].strip() for f in frames)
            check(BROWSER_ROWS[1], c3_ok, f"frames={frames[:3]}")

        # C2 — three distinct polite live nodes
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            nodes = json.loads(br.evaluate(LIVE_NODES) or "[]")
            ok = (len(nodes) == 3 and all(n and n.get("live") == "polite" for n in nodes)
                  and len({n["id"] for n in nodes if n}) == 3)
            check(BROWSER_ROWS[2], ok, f"nodes={nodes}")

        # C2 — a walk step REPLACES the caption region
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            st0 = json.loads(br.evaluate(CAP_STATE) or "null")
            # step to the second frame
            br.evaluate("(()=>{const fs=document.querySelectorAll('.exh-frame');"
                        "if(fs[1])fs[1].scrollIntoView({block:'center',behavior:'instant'});})()")
            br.sleep(0.6)
            st1 = json.loads(br.evaluate(CAP_STATE) or "null")
            prior = (st0 or {}).get("cap", [""])[0] if st0 else ""
            now = (st1 or {}).get("cap", [""])
            ok = (isinstance(st1, dict) and len(now) == 1 and now[0].strip()
                  and now[0] != prior and prior not in (st1.get("all") or "").replace(now[0], ""))
            check(BROWSER_ROWS[3], ok, f"before={st0} after={st1}")

        # C2/F5 — a story portion APPENDS (the caption stands above; a second portion accumulates). Each
        # «ещё N» opens a new story portion with NO caption replace after (focus stays), so the appended
        # portions stand together — the append discipline, shown across two portions.
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_STORY)
            enter(br, base)
            br.sleep(0.6)
            br.evaluate("(()=>{const u=document.getElementById('ex-unfold');if(u)u.click();})()")
            br.sleep(0.9)
            a = json.loads(br.evaluate(CAP_STATE) or "null")
            br.evaluate("(()=>{const u=document.getElementById('ex-unfold');if(u)u.click();})()")
            br.sleep(0.9)
            b = json.loads(br.evaluate(CAP_STATE) or "null")
            append_ok = (isinstance(a, dict) and isinstance(b, dict)
                         and len(a.get("portions", [])) >= 1
                         and len(b.get("portions", [])) >= 2
                         and len(b.get("cap", [])) == 1                # the caption still stands, one node
                         and a["portions"][0] in b["portions"])        # the earlier portion still stands
            check(BROWSER_ROWS[4], append_ok, f"after_unfold1={a} after_unfold2={b}")

        # C2/F5 — a gift result rides the SEPARATE result region while a story portion holds the caption
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_STORY)
            enter(br, base)
            br.sleep(0.6)
            # a story portion stands in the caption region (an «ещё N» opens one, no caption replace after)
            br.evaluate("(()=>{const u=document.getElementById('ex-unfold');if(u)u.click();})()")
            br.sleep(0.9)
            # open the gift ceremony on the in-view work (a grab) — its result speaks in the result region
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            cap = json.loads(br.evaluate(CAP_STATE) or "null")
            res = br.evaluate(RESULT_STATE)
            portion = (cap or {}).get("portions", [""])
            portion0 = portion[0] if portion else ""
            sep_ok = (isinstance(cap, dict) and portion0
                      and isinstance(res, str) and res.strip()
                      and portion0 not in res                       # the story portion is NOT in the result node
                      and res not in (cap.get("all") or ""))        # the result is NOT in the caption node
            check(BROWSER_ROWS[5], sep_ok, f"cap={cap} result={res!r}")

        # C4/C5 — the four modal layers each carry an accessible name
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            labels = json.loads(br.evaluate(MODAL_LABELS) or "[]")
            ok = len(labels) == 4 and all(m.get("label") and str(m["label"]).strip() for m in labels)
            check(BROWSER_ROWS[6], ok, f"labels={labels}")

        # C6 — the series room's images speak (open a real series by its own chip)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            if not SERIES:
                skip(BROWSER_ROWS[7], "the fixture bakes no series (3+)")
            else:
                try:
                    br.evaluate("(%s)(0)" % OPEN_SERIES)
                    br.sleep(1.4)                       # the veil crossing settles
                    imgs = json.loads(br.evaluate(ROOM_IMGS) or "null")
                    ok = (isinstance(imgs, list) and len(imgs) >= 1
                          and all(im["alt"].strip() and im["alt"] == DESC_BY_ID.get(str(im["id"]), "\0")
                                  for im in imgs))
                    check(BROWSER_ROWS[7], ok, f"room_imgs={imgs}")
                except Exception as e:
                    check(BROWSER_ROWS[7], False, f"exception={e!r}")

        # C7 — the inspected image speaks (pinch a walk work open, read the zoom img alt)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            enter(br, base)
            out = json.loads(br.evaluate(PINCH_WORK_ZOOM) or "null")
            ok = (isinstance(out, dict) and out.get("opened")
                  and (out.get("alt") or "").strip()
                  and out["alt"] == DESC_BY_ID.get(str(out.get("id")), "\0"))
            check(BROWSER_ROWS[8], ok, f"zoom={out}")

        # C8 — the gift prize / won-wallpaper thumbnail speaks. Driven deterministically: a KNOWN quiz
        # work's chip is injected into the caption and clicked (the real delegated opener quizCardOpen —
        # it needs only the baked quiz field, not the work rendered/focused, so the random door pick can't
        # make this flaky), an option is answered under the stubbed win, and the prize gift opens.
        with Browser(width=1280, height=900) as br:
            br.inject(STUB_QUIZ_WIN)
            enter(br, base)
            if not QUIZ_IDS:
                skip(BROWSER_ROWS[9], "the fixture bakes no quiz works")
            else:
                try:
                    qid = QUIZ_IDS[0]
                    br.evaluate(
                        "(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                        "const b=document.createElement('button');b.className='ex-quiz-chip';"
                        "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(qid))
                    wait_for(br, "!!document.querySelector('#ex-quiz-card .quiz-opt')")   # the card opens
                    br.evaluate("(()=>{const o=document.querySelector('#ex-quiz-card .quiz-opt');"
                                "if(o)o.click();})()")
                    # the win line lingers, the card closes, then the prize gift opens with its thumb
                    alt = wait_for(br, "(()=>{const t=document.querySelector('#ex-gift-card .gift-thumb');"
                                       "return t?(t.getAttribute('alt')||'@empty'):'';})()", timeout=6.0)
                    ok = (isinstance(alt, str) and alt not in ("@empty", "")
                          and alt == DESC_BY_ID.get(qid, "\0"))
                    check(BROWSER_ROWS[9], ok, f"qid={qid} thumb_alt={alt!r} want={DESC_BY_ID.get(qid)!r}")
                except Exception as e:
                    check(BROWSER_ROWS[9], False, f"exception={e!r}")

# ======================= Batch-B — the KEYBOARD + FOCUS-MANAGEMENT pole =======================
# B1-B5 + the modal-role / aria-modal / Escape class of the input-modality axis (CS-9 / INV-102,
# N7-A11Y). REAL key events drive every row (Tab / Enter / arrows / Escape) — never a synthetic
# shortcut; the focus rows read document.activeElement against the REAL headless focus. ONE focus-trap
# in the prelude (00-prelude.js) serves the four modal layers — the gift ceremony (#ex-gift-card), the
# closer look (#ex-zoom), the quiz card (#ex-quiz-card), and the series room (#ex-side).
#   · B-role  role=dialog + aria-modal on all four (one drop reds the row) — the design-review D1 class
#   · B-esc   a real Escape closes each of the four (D2)
#   · B1      focus enters each layer on open · Tab is trapped inside · close restores focus BY ORIGIN
#             (a keyboard-open zoom returns focus to its opener; a pointer/touch open forces none, so the
#             zoom's exact-restore INV-74/INV-83 is left untouched)
#   · B-walk  a real ArrowDown steps the walk one frame, centered (the work being focusable is B3)
#   · B2/B3   a key opens the closer look and the gift ceremony from a focused walk work
#   · quiz    the chip + four choices keyboard-reachable, the card takes focus on open, Esc dismisses
#   · B4      the series polaroids + lane focusable + key-open, the lane scrolls by key
#   · B5      the tongue list closes on Escape AND on focus leaving it
#   · finale / share / door / sound — reachability + accessible-name fences (already shipped)

# --- the sound :focus-within reveal is already shipped (css) — a fence at the D-row string level
check("B-sound the volume-and-credit tray reveals on keyboard focus (#ex-sound:focus-within .exsnd-tray, "
      "EX-SOUND / INV-102) — the keyboard reach already shipped — fence",
      bool(re.search(r"#ex-sound:focus-within\s+\.exsnd-tray\s*\{[^}]*(?:max-width|opacity)", D_CSS)),
      "css :focus-within reveal rule")

B_ROWS = [
    "B-role the four modal layers each declare role=dialog + aria-modal (gift·zoom·quiz·series; one drop reds it)",
    "B-esc the four modal layers each close on a real Escape (gift·zoom·quiz·series)",
    "B1 focus enters each modal layer on open (the active element is inside the layer)",
    "B1 Tab is trapped inside an open layer (repeated real Tab never reaches the walk behind)",
    "B1 close restores focus by origin (keyboard-open zoom → the opener; pointer-open zoom → no forced focus)",
    "B-walk a real ArrowDown steps the walk one frame and lands it centered, across 2 consecutive steps",
    "B3 the current walk work is keyboard-focusable (tabIndex>=0, focus lands on it)",
    "B2 a real key opens the closer look from a focused walk work",
    "B3 a real key opens the gift ceremony from a focused walk work (the imageless clean-source path)",
    "quiz the chip + four choices are keyboard-focusable, the card takes focus on open, a real Esc dismisses it",
    "B4 the series polaroids + lane images are keyboard-focusable + key-open, and the lane scrolls by key",
    "B5 the tongue list closes on a real Escape AND when focus leaves it",
    "finale the continuation + exit controls are keyboard-reachable and named (focusable + accessible name)",
    "share the round share control is keyboard-reachable and named (focusable button + accessible name)",
    "door the door windows are keyboard buttons named by title (tabIndex>=0 + non-empty alt + aria-label) — fence",
]

MODAL_ROLE = (
    "JSON.stringify(['ex-gift-card','ex-zoom','ex-quiz-card','ex-side'].map(id=>{"
    "const e=document.getElementById(id);return {id:id,"
    "role:e?(e.getAttribute('role')||''):null,modal:e?(e.getAttribute('aria-modal')||''):null};}))")
INSIDE = ("(id)=>{const l=document.getElementById(id),a=document.activeElement;"
          "return !!(l&&!l.hidden&&a&&a!==document.body&&l.contains(a));}")
OPEN_STATE = "(id)=>{const e=document.getElementById(id);return !!(e&&!e.hidden);}"
IN_WALK = ("()=>{const a=document.activeElement;return !!(a&&a.closest&&a.closest('.exh-frame'));}")
CTX_GIFT = ("(()=>{const w=document.querySelector('.exh-frame img.work');if(!w)return false;"
            "w.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}));return true;})()")
FOCUS_FRAME = ("(()=>{const f=document.querySelector('.exh-frame');if(!f)return JSON.stringify({no:1});"
               "f.focus();return JSON.stringify({ti:f.tabIndex,is:document.activeElement===f});})()")
STEP_STATE = ("(()=>{const fs=[...document.querySelectorAll('.exh-frame')];const vh=innerHeight;"
              "let idx=-1,best=1e9;fs.forEach((f,i)=>{const r=f.getBoundingClientRect();"
              "const c=Math.abs((r.top+r.bottom)/2-vh/2);if(c<best){best=c;idx=i;}});"
              "return JSON.stringify({idx:idx,off:Math.round(best)});})()")
QUIZ_FOCUSABLE = ("(()=>{const opts=[...document.querySelectorAll('#ex-quiz-card .quiz-opt')];"
                  "return JSON.stringify({n:opts.length,foc:opts.every(b=>b.tabIndex>=0&&"
                  "(b.getAttribute('aria-label')||b.textContent||'').trim().length>0)});})()")

if not chrome_available():
    for r in B_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # B-role — role=dialog + aria-modal on all four modal layers (read at construction)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            roles = json.loads(br.evaluate(MODAL_ROLE) or "[]")
            ok = (len(roles) == 4 and all(m.get("role") == "dialog" and m.get("modal") == "true" for m in roles))
            check(B_ROWS[0], ok, f"roles={roles}")

        # B-esc — a real Escape closes each of the four layers
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            esc = {}
            # gift (desktop right-click → the ceremony)
            br.evaluate(CTX_GIFT); br.sleep(0.4)
            br.key("Escape"); br.sleep(0.5)
            esc["gift"] = not br.evaluate("(%s)('ex-gift-card')" % OPEN_STATE)
            # quiz (inject the chip + click)
            if QUIZ_IDS:
                br.evaluate("(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                            "const b=document.createElement('button');b.className='ex-quiz-chip';"
                            "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(QUIZ_IDS[0]))
                br.sleep(0.5); br.key("Escape"); br.sleep(0.5)
                esc["quiz"] = not br.evaluate("(%s)('ex-quiz-card')" % OPEN_STATE)
            else:
                esc["quiz"] = True
            # series (open by its own chip)
            if SERIES:
                br.evaluate("(%s)(0)" % OPEN_SERIES); br.sleep(1.4)
                br.key("Escape"); br.sleep(1.2)
                esc["series"] = not br.evaluate("(%s)('ex-side')" % OPEN_STATE)
            else:
                esc["series"] = True
            check(B_ROWS[1], all(esc.values()), f"closed={esc}")

        # B-esc for the zoom (a touch pinch opens it, Escape closes)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            br.evaluate(PINCH_WORK_ZOOM); br.sleep(0.5)
            opened = br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            br.key("Escape"); br.sleep(0.6)
            zesc = opened and not br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            # fold the zoom result into B-esc: re-report only if it failed (the row already checked 3/4)
            if not zesc:
                for i, (n, s, d) in enumerate(results):
                    if n == B_ROWS[1]:
                        results[i] = (n, "FAIL", d + f" zoom_escape={zesc}")
                        break

        # B1 focus-in — opening each of the four moves focus INTO the layer
        with Browser(width=1280, height=900) as br:
            fin = {}
            # gift
            enter(br, base); br.evaluate(CTX_GIFT); br.sleep(0.6)
            fin["gift"] = br.evaluate("(%s)('ex-gift-card')" % INSIDE)
            br.key("Escape"); br.sleep(0.5)
            # quiz
            if QUIZ_IDS:
                br.evaluate("(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                            "const b=document.createElement('button');b.className='ex-quiz-chip';"
                            "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(QUIZ_IDS[0]))
                br.sleep(0.7)
                fin["quiz"] = br.evaluate("(%s)('ex-quiz-card')" % INSIDE)
                br.key("Escape"); br.sleep(0.5)
            else:
                fin["quiz"] = True
            # series
            if SERIES:
                br.evaluate("(%s)(0)" % OPEN_SERIES); br.sleep(1.6)
                fin["series"] = br.evaluate("(%s)('ex-side')" % INSIDE)
                br.key("Escape"); br.sleep(1.2)
            else:
                fin["series"] = True
            check(B_ROWS[2], all(fin.values()), f"focus_inside={fin}")

        # B1 focus-in for the zoom (pointer/touch open still moves focus in)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            br.evaluate(PINCH_WORK_ZOOM); br.sleep(0.7)
            zin = br.evaluate("(%s)('ex-zoom')" % INSIDE)
            if not zin:
                for i, (n, s, d) in enumerate(results):
                    if n == B_ROWS[2]:
                        results[i] = (n, "FAIL", d + f" zoom_focus_in={zin}")
                        break

        # B1 Tab-trap — repeated REAL Tab keeps the active element inside the open gift ceremony
        with Browser(width=1280, height=900) as br:
            enter(br, base); br.evaluate(CTX_GIFT); br.sleep(0.6)
            for _ in range(6):
                br.key("Tab"); br.sleep(0.08)
            inside = br.evaluate("(%s)('ex-gift-card')" % INSIDE)
            in_walk = br.evaluate("(%s)()" % IN_WALK)
            check(B_ROWS[3], bool(inside) and not in_walk, f"inside={inside} in_walk={in_walk}")

        # B1 origin-restore — a KEYBOARD-opened zoom returns focus to its opener; a POINTER open forces none
        with Browser(width=1280, height=900) as br:
            enter(br, base, tempo="0.05")
            # keyboard route: focus a work, press the inspect key, close, focus must return to that work
            br.evaluate("document.querySelector('.exh-frame').focus()")
            fid = br.evaluate("(()=>{const f=document.querySelector('.exh-frame');return f?f.dataset.id:'';})()")
            br.key("Enter"); br.sleep(0.6)
            kopen = br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            br.key("Escape"); br.sleep(0.7)
            restored = br.evaluate("(()=>{const a=document.activeElement;"
                                   "return !!(a&&a.classList&&a.classList.contains('exh-frame')&&a.dataset.id==='%s');})()" % fid)
            key_ok = kopen and restored
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base, tempo="0.05")
            br.evaluate(PINCH_WORK_ZOOM); br.sleep(0.5)
            popen = br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            br.key("Escape"); br.sleep(0.7)
            # a pointer/touch open forces no focus: the active element is NOT a walk work
            no_forced = not br.evaluate("(%s)()" % IN_WALK)
            ptr_ok = popen and no_forced
        check(B_ROWS[4], bool(key_ok) and bool(ptr_ok),
              f"keyboard_open={kopen} keyboard_restored={restored} pointer_open={popen} pointer_no_forced={no_forced}")

        # B-walk — a real ArrowDown steps the walk one frame and lands it centered (2 steps)
        with Browser(width=1280, height=900) as br:
            enter(br, base, tempo="0.05")
            br.evaluate("document.querySelector('.exh-frame').focus()")
            s0 = json.loads(br.evaluate(STEP_STATE))
            br.key("ArrowDown"); br.sleep(0.5)
            br.key("ArrowDown"); br.sleep(0.5)
            s2 = json.loads(br.evaluate(STEP_STATE))
            stepped = s2["idx"] == s0["idx"] + 2 and s2["off"] <= 8
            check(B_ROWS[5], stepped, f"from={s0} to={s2}")

        # B3 — the current walk work is keyboard-focusable
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            ff = json.loads(br.evaluate(FOCUS_FRAME))
            check(B_ROWS[6], not ff.get("no") and ff.get("ti", -1) >= 0 and ff.get("is"), f"frame={ff}")

        # B2 — a real key opens the closer look from a focused walk work
        with Browser(width=1280, height=900) as br:
            enter(br, base, tempo="0.05")
            br.evaluate("document.querySelector('.exh-frame').focus()")
            br.key("Enter"); br.sleep(0.6)
            check(B_ROWS[7], bool(br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)), "inspect key → #ex-zoom")

        # B3 — a real key opens the gift ceremony from a focused walk work (imageless clean-source path)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame').focus()")
            br.key("g"); br.sleep(0.5)
            gopen = br.evaluate("(%s)('ex-gift-card')" % OPEN_STATE)
            # the grab ceremony carries NO clean picture (INV-49) — no visible .gift-thumb
            imageless = br.evaluate("(()=>{const t=document.querySelector('#ex-gift-card .gift-thumb');"
                                    "return !t||t.hidden||!t.getAttribute('src');})()")
            check(B_ROWS[8], bool(gopen) and bool(imageless), f"open={gopen} imageless={imageless}")

        # quiz — the chip + four choices keyboard-reachable, the card takes focus on open, Esc dismisses
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            if not QUIZ_IDS:
                skip(B_ROWS[9], "the fixture bakes no quiz works")
            else:
                br.evaluate("(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                            "const b=document.createElement('button');b.className='ex-quiz-chip';"
                            "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(QUIZ_IDS[0]))
                br.sleep(0.7)
                took = br.evaluate("(%s)('ex-quiz-card')" % INSIDE)
                qf = json.loads(br.evaluate(QUIZ_FOCUSABLE))
                br.key("Escape"); br.sleep(0.6)
                dismissed = not br.evaluate("(%s)('ex-quiz-card')" % OPEN_STATE)
                check(B_ROWS[9], bool(took) and qf.get("n", 0) >= 2 and qf.get("foc") and dismissed,
                      f"focus_on_open={took} opts={qf} esc_dismissed={dismissed}")

        # B4 — the series polaroids + lane images focusable + key-open, and the lane scrolls by key
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            if not SERIES:
                skip(B_ROWS[10], "the fixture bakes no series (3+)")
            else:
                allfoc = True
                lane_scroll = None      # None = no lane series met; else True/False
                lift_ok = None          # None = no polaroid series met; else True/False
                for si in range(len(SERIES)):
                    br.evaluate("(%s)(%d)" % (OPEN_SERIES, si)); br.sleep(1.5)
                    # a LANE room's focusables are its direct <img> photos; a POLAROID room's are the
                    # .exs-print buttons (the polaroid's inner <img> is decoration, not a tab stop)
                    room = json.loads(br.evaluate(
                        "(()=>{const st=document.getElementById('exs-stage');if(!st)return 'null';"
                        "const lane=st.classList.contains('lane');"
                        "const laneImgs=lane?[...st.children].filter(e=>e.tagName==='IMG'):[];"
                        "const prints=[...st.querySelectorAll('.exs-print')];"
                        "return JSON.stringify({lane:lane,"
                        "foc:lane?(laneImgs.length>0&&laneImgs.every(i=>i.tabIndex>=0)):"
                        "(prints.length>0&&prints.every(p=>p.tabIndex>=0)),"
                        "nimgs:laneImgs.length,nprints:prints.length});})()") or "null")
                    if room == "null":
                        continue
                    allfoc = allfoc and room.get("foc")
                    if room.get("lane") and room.get("nimgs"):
                        # a real lane of photographs overflows; the synthetic fixture's tiny placeholders
                        # do not, so widen them to the width real photos carry — the precondition an
                        # overflowing lane has — then drive REAL arrow keys and watch scrollLeft grow
                        br.evaluate("(()=>{const st=document.getElementById('exs-stage');"
                                    "[...st.children].forEach(e=>{if(e.tagName==='IMG'){"
                                    "e.style.minWidth='900px';e.style.flex='none';}});})()")
                        br.sleep(0.2)
                        br.evaluate("(()=>{const im=document.querySelector('#exs-stage > img');if(im)im.focus();})()")
                        x0 = br.evaluate("document.getElementById('exs-stage').scrollLeft")
                        for _ in range(3):
                            br.key("ArrowRight"); br.sleep(0.15)
                        x1 = br.evaluate("document.getElementById('exs-stage').scrollLeft")
                        lane_scroll = (x1 or 0) > (x0 or 0)
                    if room.get("nprints"):
                        # focus a polaroid, press Enter → it lifts
                        br.evaluate("(()=>{const p=document.querySelector('#exs-stage .exs-print');if(p)p.focus();})()")
                        br.key("Enter"); br.sleep(0.4)
                        lift_ok = br.evaluate("!!document.querySelector('#exs-stage .exs-print.lift')")
                    br.key("Escape"); br.sleep(1.2)
                ok = allfoc and (lane_scroll in (None, True)) and (lift_ok in (None, True)) \
                    and (lane_scroll is not None or lift_ok is not None)
                check(B_ROWS[10], bool(ok),
                      f"all_focusable={allfoc} lane_scroll={lane_scroll} polaroid_lift={lift_ok}")

        # B5 — the tongue list closes on a real Escape AND when focus leaves it (tested at the door)
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/"); br.clear_storage(); br.reload(); br.sleep(1.0)
            has_box = br.evaluate("!!document.querySelector('#exd-lang .exl-cur')")
            if not has_box:
                skip(B_ROWS[11], "the fixture bakes no tongue corner (needs GREET.langs)")
            else:
                LIST_OPEN = "(()=>{const l=document.querySelector('#exd-lang .exl-list');return !!(l&&!l.hidden);})()"
                # Escape closes an open list
                br.evaluate("document.querySelector('#exd-lang .exl-cur').click()"); br.sleep(0.3)
                open1 = br.evaluate(LIST_OPEN)
                br.key("Escape"); br.sleep(0.9)
                esc_closed = not br.evaluate(LIST_OPEN)
                # focus leaving the box closes it — a FRESH door so no prior toggle-close timer contaminates
                br.navigate(base + "/"); br.clear_storage(); br.reload(); br.sleep(1.0)
                # focus the corner button as a keyboard user would, THEN open — so focus sits inside the box
                br.evaluate("(()=>{const c=document.querySelector('#exd-lang .exl-cur');c.focus();c.click();})()")
                br.sleep(0.3)
                open2 = br.evaluate(LIST_OPEN)
                br.evaluate("(()=>{const w=document.querySelector('.exd-window');if(w)w.focus();})()")
                br.sleep(0.9)
                out_closed = not br.evaluate(LIST_OPEN)
                check(B_ROWS[11], open1 and esc_closed and open2 and out_closed,
                      f"opened={open1}/{open2} esc_closed={esc_closed} focusout_closed={out_closed}")

        # finale — the continuation + exit controls are keyboard-reachable and named (fence)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("(()=>{const f=document.getElementById('exh-fin');"
                        "if(f)f.scrollIntoView({behavior:'instant'});})()")
            br.sleep(0.4)
            fin_ctrl = json.loads(br.evaluate(
                "(()=>{const g=id=>{const e=document.getElementById(id);if(!e)return null;"
                "return {tab:e.tabIndex>=0||e.tagName==='BUTTON',"
                "name:((e.getAttribute('aria-label')||e.textContent||'').trim().length>0)};};"
                "return JSON.stringify({more:g('ex-unfold'),ret:g('ex-return')});})()") or "{}")
            present = [c for c in (fin_ctrl.get("more"), fin_ctrl.get("ret")) if c]
            ok = len(present) >= 1 and all(c["tab"] and c["name"] for c in present)
            check(B_ROWS[12], ok, f"controls={fin_ctrl}")

        # share — the round share control is keyboard-reachable and named (fence)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            sh = json.loads(br.evaluate(
                "(()=>{const e=document.getElementById('ex-share');if(!e)return 'null';"
                "return JSON.stringify({btn:e.tagName==='BUTTON',tab:e.tabIndex>=0||e.tagName==='BUTTON',"
                "name:((e.getAttribute('aria-label')||'').trim().length>0)});})()") or "null")
            check(B_ROWS[13], isinstance(sh, dict) and sh.get("btn") and sh.get("tab") and sh.get("name"),
                  f"share={sh}")

        # door — the windows are keyboard buttons named by title (fence, mirrors test_door #7)
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/"); br.clear_storage(); br.reload(); br.sleep(1.0)
            dk = json.loads(br.evaluate(
                "(()=>{const ws=[...document.querySelectorAll('.exd-window')];"
                "return JSON.stringify({n:ws.length,kb:ws.every(b=>b.tabIndex>=0),"
                "alts:ws.every(b=>((b.querySelector('img')||{}).alt||'').trim().length>0),"
                "labels:ws.every(b=>((b.getAttribute('aria-label'))||'').trim().length>0)});})()") or "{}")
            check(B_ROWS[14], dk.get("n", 0) >= 1 and dk.get("kb") and dk.get("alts") and dk.get("labels"),
                  f"door={dk}")

# ---------------------------------------------------------------- Batch-A — the touch pole (A1) + D4
# The touch long-press grab and its disambiguation (matrix Batch-A A1 rows), driven by REAL synthesized
# PointerEvents — a pointerdown held past the ~500ms arm, a drift, a second finger — plus the D4
# origin-conditioned gift focus-restore (keyboard-open → the opener; touch-open → none), uniform with the
# zoom. The grab reuses the imageless clean-source openGift path (INV-49); the leak row is the hard one.
A_ROWS = [
    "A1 a touch long-press opens the gift ceremony via the reused imageless clean-source openGift path (walk · finger)",
    "A1 the touch grab leaks no clean source — the open ceremony holds zero <img> and no clean-src reference (walk · finger · copy-leak-safe INV-49)",
    "A1 a door-window long-press keeps the gracious toast, never the ceremony (door · finger · F1)",
    "A1 the ~500ms arm gate — a full hold fires, a short tap does not (walk · finger · F8 default)",
    "A1 the px-drift cancel — a small drift still fires, a large drift and a second finger both cancel (walk · finger · F8 default)",
    "A1 the detector coexists with the swipe glide and the inspect pinch — a swipe still steps, a pinch still zooms, a hold still grabs (walk · finger)",
    "D4 the gift restores focus by origin — a keyboard-open returns to the opener, a touch-open forces none even off a focused work (gift · D4 · OS-A1)",
]

LP_START = ("(sel)=>{const el=document.querySelector(sel);if(!el)return false;"
            "const r=el.getBoundingClientRect();const x=r.left+r.width/2,y=r.top+r.height/2;"
            "window.__lpx=x;window.__lpy=y;"
            "el.dispatchEvent(new PointerEvent('pointerdown',{pointerId:1,pointerType:'touch',"
            "clientX:x,clientY:y,isPrimary:true,bubbles:true,cancelable:true}));return true;}")
LP_MOVE = ("(dx)=>{const x=window.__lpx+dx,y=window.__lpy;"
           "document.dispatchEvent(new PointerEvent('pointermove',{pointerId:1,pointerType:'touch',"
           "clientX:x,clientY:y,isPrimary:true,bubbles:true,cancelable:true}));return true;}")
LP_SECOND = ("()=>{document.dispatchEvent(new PointerEvent('pointerdown',{pointerId:2,pointerType:'touch',"
             "clientX:window.__lpx+40,clientY:window.__lpy,isPrimary:false,bubbles:true,cancelable:true}));return true;}")
LP_END = ("()=>{document.dispatchEvent(new PointerEvent('pointerup',{pointerId:1,pointerType:'touch',"
          "clientX:window.__lpx,clientY:window.__lpy,isPrimary:true,bubbles:true,cancelable:true}));"
          "document.dispatchEvent(new PointerEvent('pointerup',{pointerId:2,pointerType:'touch',"
          "clientX:window.__lpx+40,clientY:window.__lpy,isPrimary:false,bubbles:true,cancelable:true}));return true;}")
GIFT_OPEN = "(()=>{const g=document.getElementById('ex-gift-card');return !!(g&&!g.hidden);})()"
IN_FRAME = ("(()=>{const a=document.activeElement;return !!(a&&a.closest&&a.closest('.exh-frame'));})()")

if not chrome_available():
    for r in A_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # A1 · a touch long-press on a walk work opens the gift ceremony (imageless clean-source path)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.75)                                # past the ~500ms arm
            opened = br.evaluate(GIFT_OPEN)
            ask = br.evaluate("(()=>{const a=document.querySelector('#ex-gift-card .gift-ask');"
                              "return a?(a.textContent||'').trim():'';})()")
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[0], bool(opened) and len(ask) > 0, f"opened={opened} ask={ask!r}")

        # A1 · the touch grab leaks no clean source — the open ceremony holds zero <img>, no clean-src ref
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.75)
            leak = json.loads(br.evaluate(
                "(()=>{const g=document.getElementById('ex-gift-card');"
                "const w=document.querySelector('.exh-frame img.work');"
                "const src=w?(w.currentSrc||w.getAttribute('src')||w.src||''):'';"
                "const nb=(src.split('?')[0].split('/').pop())||'\\0';"
                "let ref=false;g.querySelectorAll('*').forEach(el=>{for(const a of el.attributes){"
                "if(a.value&&nb&&a.value.indexOf(nb)>=0)ref=true;}});"
                "return JSON.stringify({open:!g.hidden,nimgs:g.querySelectorAll('img').length,ref:ref,nb:nb});})()") or "{}")
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[1], bool(leak.get("open")) and leak.get("nimgs") == 0 and not leak.get("ref"),
                  f"leak={leak}")

        # A1 · a door-window long-press keeps the gracious toast, never the ceremony (F1 exception)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            br.navigate(base + "/"); br.clear_storage(); br.evaluate("sessionStorage.clear()")
            br.evaluate("localStorage.setItem('%s-tempo','1.0')" % NS_UPPER.lower()); br.reload(); br.sleep(1.1)
            began = br.evaluate("(%s)('.exd-window img')" % LP_START)
            br.sleep(0.75)
            gift = br.evaluate(GIFT_OPEN)
            toast = br.evaluate("(()=>{const t=document.getElementById('ex-toast');"
                                "return !!(t&&!t.hidden&&(t.textContent||'').trim());})()")
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[2], bool(began) and (not gift) and bool(toast),
                  f"began={began} gift_open={gift} toast={toast}")

        # A1 · the ~500ms arm gate — a short tap does NOT open, a full hold DOES
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.15); br.evaluate("(%s)()" % LP_END)   # released well before the arm — a tap
            br.sleep(0.6)
            short = br.evaluate(GIFT_OPEN)                    # must be False
            br.key("Escape"); br.sleep(0.3)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.75)                                    # a full hold past the arm
            full = br.evaluate(GIFT_OPEN)                     # must be True
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[3], (not short) and bool(full), f"short_tap_open={short} full_hold_open={full}")

        # A1 · the px-drift cancel — a small drift still fires; a large drift / a second finger cancel
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.1); br.evaluate("(%s)(4)" % LP_MOVE)   # 4px — within threshold, still a hold
            br.sleep(0.7)
            steady = br.evaluate(GIFT_OPEN)                   # must be True
            br.evaluate("(%s)()" % LP_END); br.key("Escape"); br.sleep(0.3)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.1); br.evaluate("(%s)(40)" % LP_MOVE)  # 40px — a swipe, cancels
            br.sleep(0.7)
            drift = br.evaluate(GIFT_OPEN)                    # must be False
            br.evaluate("(%s)()" % LP_END); br.key("Escape"); br.sleep(0.3)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.1); br.evaluate("(%s)()" % LP_SECOND)  # a second finger — the pinch wins
            br.sleep(0.7)
            pinch = br.evaluate(GIFT_OPEN)                    # must be False
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[4], bool(steady) and (not drift) and (not pinch),
                  f"steady_fires={steady} large_drift_open={drift} second_finger_open={pinch}")

        # A1 · coexistence — a swipe still steps, a pinch still zooms, a hold still grabs (all live together)
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base)
            s0 = json.loads(br.evaluate(STEP_STATE))
            br.swipe(-320); br.sleep(0.9)
            s1 = json.loads(br.evaluate(STEP_STATE))
            swipe_ok = s1["idx"] > s0["idx"]                  # the walk glide is not clobbered
            z = json.loads(br.evaluate(PINCH_WORK_ZOOM) or "null")
            pinch_ok = bool(z and z.get("opened"))            # the inspect pinch is not clobbered
            br.key("Escape"); br.sleep(0.6)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.75)
            grab_ok = br.evaluate(GIFT_OPEN)                  # the detector itself is live
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[5], swipe_ok and pinch_ok and bool(grab_ok),
                  f"swipe_steps={swipe_ok} pinch_zooms={pinch_ok} longpress_grabs={grab_ok}")

        # D4 · the gift restores focus by origin — keyboard-open → the opener; touch-open → none
        with Browser(width=1280, height=900) as br:
            enter(br, base, tempo="0.05")
            br.evaluate("document.querySelector('.exh-frame').focus()")
            fid = br.evaluate("(()=>{const f=document.querySelector('.exh-frame');return f?f.dataset.id:'';})()")
            br.key("g"); br.sleep(0.5)
            kopen = br.evaluate(GIFT_OPEN)
            br.key("Escape"); br.sleep(0.6)
            krestored = br.evaluate("(()=>{const a=document.activeElement;"
                                    "return !!(a&&a.classList&&a.classList.contains('exh-frame')&&a.dataset.id==='%s');})()" % fid)
            key_ok = kopen and krestored
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2); enter(br, base, tempo="0.05")
            # a work is focused (as a keyboard user leaves it) BEFORE the TOUCH grab — a touch open must
            # still force NO restore (origin-conditioned like the zoom), so focus is off the work after close
            br.evaluate("document.querySelector('.exh-frame').focus()")
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.75)
            topen = br.evaluate(GIFT_OPEN)
            br.evaluate("(%s)()" % LP_END)
            br.key("Escape"); br.sleep(0.6)
            no_forced = not br.evaluate(IN_FRAME)             # a touch open leaves focus off the walk work
            touch_ok = topen and no_forced
        check(A_ROWS[6], bool(key_ok) and bool(touch_ok),
              f"keyboard_open={kopen} keyboard_restored={krestored} touch_open={topen} touch_no_forced={no_forced}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, stt, detail in results:
    print(f"[{stt}] {name}" + (f"  — {detail}" if detail and stt != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
