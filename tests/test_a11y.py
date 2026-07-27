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


def wait_settled(br, expr, start, timeout=6.0, step=0.05, stable=2):
    """Poll a moving number until it has LEFT `start` and then reads the SAME twice — a real
    motion coming to rest (a walk glide, a lane scroll), in place of a fixed sleep. Returns the
    resting value, or the last one read at the deadline."""
    import time
    end = time.time() + timeout
    last, same = start, 0
    while time.time() < end:
        v = br.evaluate(expr)
        if v != start:
            same = same + 1 if v == last else 1
            if same >= stable:
                return v
        last = v
        br.sleep(step)
    return last


# ---------------------------------------------------------------- the conditions the rows wait on
# Every wait below names the state the next line reads, taken from the client's own markers.


class shared:
    """Hand a row an already-open Browser and leave it open — ONE Chrome serves a whole group of
    rows instead of one cold launch per row. Per-row isolation is enter()/at_door(): navigate,
    clear localStorage AND sessionStorage, reload. Only BROWSER-level state survives that — an
    injected on-new-document script (Page.addScriptToEvaluateOnNewDocument is never removed) and
    touch emulation — so each of those gets a browser of its own."""
    __slots__ = ("br",)

    def __init__(self, br):
        self.br = br

    def __enter__(self):
        return self.br

    def __exit__(self, *a):
        return False


# the door stands ready to be clicked: its windows are rendered AND their pictures have landed
# (a window whose img has not settled reports a currentSrc the K rows would compare against a
# later, different one)
DOOR_READY = ("(()=>{const ws=[...document.querySelectorAll('.exd-window')];"
              "return ws.length>=1&&ws.every(w=>{const i=w.querySelector('img');"
              "return !!(i&&i.complete&&i.naturalWidth>0);});})()")
# the door→walk crossing has LANDED: none of the three body classes 07-door-face-ceremony.js sets
# is left (ex-door while the door stands, ex-crossing during the crossing, ex-cross-cap while the
# caption waits its beat — dropped in capBeat, the same tick that frees the ceremony lock) and the
# first work's picture stands
WALK_LANDED = ("(()=>{const b=document.body.classList;"
               "return !b.contains('ex-door')&&!b.contains('ex-crossing')&&!b.contains('ex-cross-cap')"
               "&&!!document.querySelector('.exh-frame img.work');})()")
# the series room stands REVEALED: the shared veil crossing is over (veil hidden = the ceremony
# lock released) and the stage carries its pictures, landed
ROOM_READY = ("(()=>{const s=document.getElementById('ex-side'),v=document.getElementById('ex-veil'),"
              "st=document.getElementById('exs-stage');if(!(s&&!s.hidden&&(!v||v.hidden)&&st))return false;"
              "const im=[...st.querySelectorAll('img')];"
              "return im.length>=1&&im.every(i=>i.complete&&i.naturalWidth>0);})()")
# the room has LEFT and its exit crossing is over (the veil is back down), so the next open is free
ROOM_GONE = ("(()=>{const s=document.getElementById('ex-side'),v=document.getElementById('ex-veil');"
             "return !!(s&&s.hidden&&(!v||v.hidden));})()")
TOAST_UP = ("(()=>{const t=document.getElementById('ex-toast');"
            "return !!(t&&!t.hidden&&(t.textContent||'').trim());})()")


def layer_up(el_id):
    """The layer stands (its element is present and not hidden)."""
    return "(()=>{const e=document.getElementById(%s);return !!(e&&!e.hidden);})()" % json.dumps(el_id)


def layer_gone(el_id):
    """The layer is gone (hidden) — the state a close leaves behind, after any focus restore."""
    return "(()=>{const e=document.getElementById(%s);return !!(e&&e.hidden);})()" % json.dumps(el_id)


def focus_inside(el_id):
    """Focus has landed INSIDE the layer (openTrap seats it on the frame after the open)."""
    return ("(()=>{const l=document.getElementById(%s),a=document.activeElement;"
            "return !!(l&&!l.hidden&&a&&a!==document.body&&l.contains(a));})()" % json.dumps(el_id))


def counter_at(n):
    """The walk's own work counter reads `n` — the in-view observer has run for that frame."""
    return ("(()=>{const e=document.querySelector('#exh-counter .now');"
            "return !!e&&e.textContent.trim()===%s;})()" % json.dumps("%02d" % n))


def portions_at_least(n):
    """At least `n` story portions stand in the caption live region."""
    return ("(()=>{const e=document.getElementById('ex-live-cap');"
            "return !!e&&e.querySelectorAll('.ex-sr-portion').length>=%d;})()" % n)


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
    wait_for(br, DOOR_READY, timeout=8.0)          # the door's windows are up and pictured
    br.click(".exd-window:nth-child(1)", settle=0.05)
    wait_for(br, WALK_LANDED, timeout=8.0)         # the crossing has landed on the first work


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
    # Four groups, one Chrome each, held open across every row of the group (the plain rows, the
    # touch-emulated row, and one per injected on-new-document stub — neither resets with enter()).
    with serve(TMP) as base, \
            Browser(width=1280, height=900) as plain_br, \
            Browser(width=1280, height=900) as touch_br, \
            Browser(width=1280, height=900) as story_br, \
            Browser(width=1280, height=900) as quizwin_br:
        touch_br.touch(True, 2)
        story_br.inject(STUB_STORY)
        quizwin_br.inject(STUB_QUIZ_WIN)

        # C1 + C3 — the walk frames speak an alt and name themselves a photograph
        with shared(plain_br) as br:
            enter(br, base)
            frames = json.loads(br.evaluate(FRAMES_ALT) or "[]")
            c1_ok = len(frames) >= 2 and all(
                f["alt"].strip() and f["alt"] == DESC_BY_ID.get(str(f["id"]), "\0") for f in frames)
            check(BROWSER_ROWS[0], c1_ok, f"frames={frames[:3]}")
            c3_ok = len(frames) >= 2 and all(
                f["role"].strip() and f["label"].strip() and f["rdesc"].strip() for f in frames)
            check(BROWSER_ROWS[1], c3_ok, f"frames={frames[:3]}")

        # C2 — three distinct polite live nodes
        with shared(plain_br) as br:
            enter(br, base)
            nodes = json.loads(br.evaluate(LIVE_NODES) or "[]")
            ok = (len(nodes) == 3 and all(n and n.get("live") == "polite" for n in nodes)
                  and len({n["id"] for n in nodes if n}) == 3)
            check(BROWSER_ROWS[2], ok, f"nodes={nodes}")

        # C2 — a walk step REPLACES the caption region
        with shared(plain_br) as br:
            enter(br, base)
            st0 = json.loads(br.evaluate(CAP_STATE) or "null")
            # step to the second frame
            br.evaluate("(()=>{const fs=document.querySelectorAll('.exh-frame');"
                        "if(fs[1])fs[1].scrollIntoView({block:'center',behavior:'instant'});})()")
            # the second frame's in-view callback has run — it moves the counter, and announces
            # the caption in the same pass (08-plaque-caption-io.js)
            wait_for(br, counter_at(2))
            st1 = json.loads(br.evaluate(CAP_STATE) or "null")
            prior = (st0 or {}).get("cap", [""])[0] if st0 else ""
            now = (st1 or {}).get("cap", [""])
            ok = (isinstance(st1, dict) and len(now) == 1 and now[0].strip()
                  and now[0] != prior and prior not in (st1.get("all") or "").replace(now[0], ""))
            check(BROWSER_ROWS[3], ok, f"before={st0} after={st1}")

        # C2/F5 — a story portion APPENDS (the caption stands above; a second portion accumulates). Each
        # «ещё N» opens a new story portion with NO caption replace after (focus stays), so the appended
        # portions stand together — the append discipline, shown across two portions.
        with shared(story_br) as br:
            enter(br, base)
            wait_for(br, "!!document.getElementById('ex-unfold')")   # the finale's control stands
            br.evaluate("(()=>{const u=document.getElementById('ex-unfold');if(u)u.click();})()")
            wait_for(br, portions_at_least(1))
            a = json.loads(br.evaluate(CAP_STATE) or "null")
            br.evaluate("(()=>{const u=document.getElementById('ex-unfold');if(u)u.click();})()")
            wait_for(br, portions_at_least(2))
            b = json.loads(br.evaluate(CAP_STATE) or "null")
            append_ok = (isinstance(a, dict) and isinstance(b, dict)
                         and len(a.get("portions", [])) >= 1
                         and len(b.get("portions", [])) >= 2
                         and len(b.get("cap", [])) == 1                # the caption still stands, one node
                         and a["portions"][0] in b["portions"])        # the earlier portion still stands
            check(BROWSER_ROWS[4], append_ok, f"after_unfold1={a} after_unfold2={b}")

        # C2/F5 — a gift result rides the SEPARATE result region while a story portion holds the caption
        with shared(story_br) as br:
            enter(br, base)
            wait_for(br, "!!document.getElementById('ex-unfold')")   # the finale's control stands
            # a story portion stands in the caption region (an «ещё N» opens one, no caption replace after)
            br.evaluate("(()=>{const u=document.getElementById('ex-unfold');if(u)u.click();})()")
            wait_for(br, portions_at_least(1))
            # open the gift ceremony on the in-view work (a grab) — its result speaks in the result region
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            # openGift announces the result BEFORE it unhides the card (11-protect-gift.js), so a
            # standing card is proof the result region has been written
            wait_for(br, layer_up("ex-gift-card"))
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
        with shared(plain_br) as br:
            enter(br, base)
            labels = json.loads(br.evaluate(MODAL_LABELS) or "[]")
            ok = len(labels) == 4 and all(m.get("label") and str(m["label"]).strip() for m in labels)
            check(BROWSER_ROWS[6], ok, f"labels={labels}")

        # C6 — the series room's images speak (open a real series by its own chip)
        with shared(plain_br) as br:
            enter(br, base)
            if not SERIES:
                skip(BROWSER_ROWS[7], "the fixture bakes no series (3+)")
            else:
                try:
                    br.evaluate("(%s)(0)" % OPEN_SERIES)
                    wait_for(br, ROOM_READY)            # the veil crossing is over, the room dressed
                    imgs = json.loads(br.evaluate(ROOM_IMGS) or "null")
                    ok = (isinstance(imgs, list) and len(imgs) >= 1
                          and all(im["alt"].strip() and im["alt"] == DESC_BY_ID.get(str(im["id"]), "\0")
                                  for im in imgs))
                    check(BROWSER_ROWS[7], ok, f"room_imgs={imgs}")
                except Exception as e:
                    check(BROWSER_ROWS[7], False, f"exception={e!r}")

        # C7 — the inspected image speaks (pinch a walk work open, read the zoom img alt)
        with shared(touch_br) as br:
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
        with shared(quizwin_br) as br:
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
    # Two groups, one Chrome each: the plain rows, and the touch-emulated ones (touch emulation is
    # set on the BROWSER and does not reset with enter()).
    with serve(TMP) as base, \
            Browser(width=1280, height=900) as plain_br, \
            Browser(width=1280, height=900) as touch_br:
        touch_br.touch(True, 2)

        # B-role — role=dialog + aria-modal on all four modal layers (read at construction)
        with shared(plain_br) as br:
            enter(br, base)
            roles = json.loads(br.evaluate(MODAL_ROLE) or "[]")
            ok = (len(roles) == 4 and all(m.get("role") == "dialog" and m.get("modal") == "true" for m in roles))
            check(B_ROWS[0], ok, f"roles={roles}")

        # B-esc — a real Escape closes each of the four layers
        with shared(plain_br) as br:
            enter(br, base)
            esc = {}
            # gift (desktop right-click → the ceremony)
            br.evaluate(CTX_GIFT); wait_for(br, layer_up("ex-gift-card"))
            br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            esc["gift"] = not br.evaluate("(%s)('ex-gift-card')" % OPEN_STATE)
            # quiz (inject the chip + click)
            if QUIZ_IDS:
                br.evaluate("(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                            "const b=document.createElement('button');b.className='ex-quiz-chip';"
                            "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(QUIZ_IDS[0]))
                wait_for(br, layer_up("ex-quiz-card"))
                br.key("Escape"); wait_for(br, layer_gone("ex-quiz-card"))
                esc["quiz"] = not br.evaluate("(%s)('ex-quiz-card')" % OPEN_STATE)
            else:
                esc["quiz"] = True
            # series (open by its own chip)
            if SERIES:
                br.evaluate("(%s)(0)" % OPEN_SERIES); wait_for(br, ROOM_READY)
                br.key("Escape"); wait_for(br, ROOM_GONE)
                esc["series"] = not br.evaluate("(%s)('ex-side')" % OPEN_STATE)
            else:
                esc["series"] = True
            check(B_ROWS[1], all(esc.values()), f"closed={esc}")

        # B-esc for the zoom (a touch pinch opens it, Escape closes)
        with shared(touch_br) as br:
            enter(br, base)
            br.evaluate(PINCH_WORK_ZOOM); wait_for(br, layer_up("ex-zoom"))
            opened = br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            br.key("Escape"); wait_for(br, layer_gone("ex-zoom"))
            zesc = opened and not br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            # fold the zoom result into B-esc: re-report only if it failed (the row already checked 3/4)
            if not zesc:
                for i, (n, s, d) in enumerate(results):
                    if n == B_ROWS[1]:
                        results[i] = (n, "FAIL", d + f" zoom_escape={zesc}")
                        break

        # B1 focus-in — opening each of the four moves focus INTO the layer
        with shared(plain_br) as br:
            fin = {}
            # gift
            enter(br, base); br.evaluate(CTX_GIFT); wait_for(br, focus_inside("ex-gift-card"))
            fin["gift"] = br.evaluate("(%s)('ex-gift-card')" % INSIDE)
            br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            # quiz
            if QUIZ_IDS:
                br.evaluate("(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                            "const b=document.createElement('button');b.className='ex-quiz-chip';"
                            "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(QUIZ_IDS[0]))
                wait_for(br, focus_inside("ex-quiz-card"))
                fin["quiz"] = br.evaluate("(%s)('ex-quiz-card')" % INSIDE)
                br.key("Escape"); wait_for(br, layer_gone("ex-quiz-card"))
            else:
                fin["quiz"] = True
            # series
            if SERIES:
                br.evaluate("(%s)(0)" % OPEN_SERIES); wait_for(br, focus_inside("ex-side"))
                fin["series"] = br.evaluate("(%s)('ex-side')" % INSIDE)
                br.key("Escape"); wait_for(br, ROOM_GONE)
            else:
                fin["series"] = True
            check(B_ROWS[2], all(fin.values()), f"focus_inside={fin}")

        # B1 focus-in for the zoom (pointer/touch open still moves focus in)
        with shared(touch_br) as br:
            enter(br, base)
            br.evaluate(PINCH_WORK_ZOOM); wait_for(br, focus_inside("ex-zoom"))
            zin = br.evaluate("(%s)('ex-zoom')" % INSIDE)
            if not zin:
                for i, (n, s, d) in enumerate(results):
                    if n == B_ROWS[2]:
                        results[i] = (n, "FAIL", d + f" zoom_focus_in={zin}")
                        break

        # B1 Tab-trap — repeated REAL Tab keeps the active element inside the open gift ceremony
        with shared(plain_br) as br:
            enter(br, base); br.evaluate(CTX_GIFT); wait_for(br, focus_inside("ex-gift-card"))
            for _ in range(6):
                br.key("Tab"); br.sleep(0.08)
            inside = br.evaluate("(%s)('ex-gift-card')" % INSIDE)
            in_walk = br.evaluate("(%s)()" % IN_WALK)
            check(B_ROWS[3], bool(inside) and not in_walk, f"inside={inside} in_walk={in_walk}")

        # B1 origin-restore — a KEYBOARD-opened zoom returns focus to its opener; a POINTER open forces none
        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            # keyboard route: focus a work, press the inspect key, close, focus must return to that work
            br.evaluate("document.querySelector('.exh-frame').focus()")
            fid = br.evaluate("(()=>{const f=document.querySelector('.exh-frame');return f?f.dataset.id:'';})()")
            br.key("Enter"); wait_for(br, layer_up("ex-zoom"))
            kopen = br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            # the close hands focus back BEFORE the layer's own flight hides it (closeTrap runs at the
            # top of closeZoom, the hidden flag lands with the teardown), so a hidden layer is proof
            # the restore has already happened
            br.key("Escape"); wait_for(br, layer_gone("ex-zoom"))
            restored = br.evaluate("(()=>{const a=document.activeElement;"
                                   "return !!(a&&a.classList&&a.classList.contains('exh-frame')&&a.dataset.id==='%s');})()" % fid)
            key_ok = kopen and restored
        with shared(touch_br) as br:
            enter(br, base, tempo="0.05")
            br.evaluate(PINCH_WORK_ZOOM); wait_for(br, layer_up("ex-zoom"))
            popen = br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)
            # at OPEN time a touch/pointer open must NOT force focus onto the close control — that is
            # what lit the × on a tan fill + the browser's blue ring on a finger open (his 2026-07-23).
            # The trap anchors the LAYER instead, so the control stays unlit until a real Tab lands it.
            open_no_ctrl = not br.evaluate(
                "(()=>document.activeElement===document.querySelector('#ex-zoom .exz-close'))()")
            br.key("Escape"); wait_for(br, layer_gone("ex-zoom"))
            # a pointer/touch open forces no focus: the active element is NOT a walk work
            no_forced = not br.evaluate("(%s)()" % IN_WALK)
            ptr_ok = popen and no_forced and open_no_ctrl
        check(B_ROWS[4], bool(key_ok) and bool(ptr_ok),
              f"keyboard_open={kopen} keyboard_restored={restored} pointer_open={popen} "
              f"pointer_no_forced={no_forced} pointer_open_no_control_focus={open_no_ctrl}")

        # B-walk — a real ArrowDown steps the walk one frame and lands it centered (2 steps)
        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            br.evaluate("document.querySelector('.exh-frame').focus()")
            s0 = json.loads(br.evaluate(STEP_STATE))
            # each step is a real glide — wait for the scroll to LEAVE where it stood and come to
            # rest, which is exactly the state the centred-frame measure below reads
            y0 = br.evaluate("Math.round(scrollY)")
            br.key("ArrowDown"); y1 = wait_settled(br, "Math.round(scrollY)", y0)
            br.key("ArrowDown"); wait_settled(br, "Math.round(scrollY)", y1)
            s2 = json.loads(br.evaluate(STEP_STATE))
            stepped = s2["idx"] == s0["idx"] + 2 and s2["off"] <= 8
            check(B_ROWS[5], stepped, f"from={s0} to={s2}")

        # B3 — the current walk work is keyboard-focusable
        with shared(plain_br) as br:
            enter(br, base)
            ff = json.loads(br.evaluate(FOCUS_FRAME))
            check(B_ROWS[6], not ff.get("no") and ff.get("ti", -1) >= 0 and ff.get("is"), f"frame={ff}")

        # B2 — a real key opens the closer look from a focused walk work
        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            br.evaluate("document.querySelector('.exh-frame').focus()")
            br.key("Enter"); wait_for(br, layer_up("ex-zoom"))
            check(B_ROWS[7], bool(br.evaluate("(%s)('ex-zoom')" % OPEN_STATE)), "inspect key → #ex-zoom")

        # B3 — a real key opens the gift ceremony from a focused walk work (imageless clean-source path)
        with shared(plain_br) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame').focus()")
            br.key("y"); wait_for(br, layer_up("ex-gift-card"))
            gopen = br.evaluate("(%s)('ex-gift-card')" % OPEN_STATE)
            # the grab ceremony carries NO clean picture (INV-49) — no visible .gift-thumb
            imageless = br.evaluate("(()=>{const t=document.querySelector('#ex-gift-card .gift-thumb');"
                                    "return !t||t.hidden||!t.getAttribute('src');})()")
            check(B_ROWS[8], bool(gopen) and bool(imageless), f"open={gopen} imageless={imageless}")

        # quiz — the chip + four choices keyboard-reachable, the card takes focus on open, Esc dismisses
        with shared(plain_br) as br:
            enter(br, base)
            if not QUIZ_IDS:
                skip(B_ROWS[9], "the fixture bakes no quiz works")
            else:
                br.evaluate("(()=>{const c=document.getElementById('exh-cap');if(!c)return;"
                            "const b=document.createElement('button');b.className='ex-quiz-chip';"
                            "b.dataset.quiz=%s;b.textContent='q';c.appendChild(b);b.click();})()" % json.dumps(QUIZ_IDS[0]))
                wait_for(br, focus_inside("ex-quiz-card"))
                took = br.evaluate("(%s)('ex-quiz-card')" % INSIDE)
                qf = json.loads(br.evaluate(QUIZ_FOCUSABLE))
                br.key("Escape"); wait_for(br, layer_gone("ex-quiz-card"))
                dismissed = not br.evaluate("(%s)('ex-quiz-card')" % OPEN_STATE)
                check(B_ROWS[9], bool(took) and qf.get("n", 0) >= 2 and qf.get("foc") and dismissed,
                      f"focus_on_open={took} opts={qf} esc_dismissed={dismissed}")

        # B4 — the series polaroids + lane images focusable + key-open, and the lane scrolls by key
        with shared(plain_br) as br:
            enter(br, base)
            if not SERIES:
                skip(B_ROWS[10], "the fixture bakes no series (3+)")
            else:
                allfoc = True
                lane_scroll = None      # None = no lane series met; else True/False
                lift_ok = None          # None = no polaroid series met; else True/False
                for si in range(len(SERIES)):
                    br.evaluate("(%s)(%d)" % (OPEN_SERIES, si)); wait_for(br, ROOM_READY)
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
                        # the widened lane really overflows — the precondition a scroll needs
                        wait_for(br, "(()=>{const st=document.getElementById('exs-stage');"
                                     "return !!st&&st.scrollWidth>st.clientWidth;})()")
                        br.evaluate("(()=>{const im=document.querySelector('#exs-stage > img');if(im)im.focus();})()")
                        x0 = br.evaluate("document.getElementById('exs-stage').scrollLeft")
                        for _ in range(3):
                            br.key("ArrowRight"); br.sleep(0.15)
                        x1 = wait_settled(br, "document.getElementById('exs-stage').scrollLeft", x0)
                        lane_scroll = (x1 or 0) > (x0 or 0)
                    if room.get("nprints"):
                        # focus a polaroid, press Enter → it lifts
                        br.evaluate("(()=>{const p=document.querySelector('#exs-stage .exs-print');if(p)p.focus();})()")
                        br.key("Enter"); wait_for(br, "!!document.querySelector('#exs-stage .exs-print.lift')")
                        lift_ok = br.evaluate("!!document.querySelector('#exs-stage .exs-print.lift')")
                    br.key("Escape"); wait_for(br, ROOM_GONE)
                ok = allfoc and (lane_scroll in (None, True)) and (lift_ok in (None, True)) \
                    and (lane_scroll is not None or lift_ok is not None)
                check(B_ROWS[10], bool(ok),
                      f"all_focusable={allfoc} lane_scroll={lane_scroll} polaroid_lift={lift_ok}")

        # B5 — the tongue list closes on a real Escape AND when focus leaves it (tested at the door)
        with shared(plain_br) as br:
            br.navigate(base + "/"); br.clear_storage(); br.reload(); wait_for(br, DOOR_READY, timeout=8.0)
            has_box = br.evaluate("!!document.querySelector('#exd-lang .exl-cur')")
            if not has_box:
                skip(B_ROWS[11], "the fixture bakes no tongue corner (needs GREET.langs)")
            else:
                LIST_OPEN = "(()=>{const l=document.querySelector('#exd-lang .exl-list');return !!(l&&!l.hidden);})()"
                LIST_SHUT = "(()=>{const l=document.querySelector('#exd-lang .exl-list');return !!(l&&l.hidden);})()"
                # Escape closes an open list
                br.evaluate("document.querySelector('#exd-lang .exl-cur').click()"); wait_for(br, LIST_OPEN)
                open1 = br.evaluate(LIST_OPEN)
                br.key("Escape"); wait_for(br, LIST_SHUT)
                esc_closed = not br.evaluate(LIST_OPEN)
                # focus leaving the box closes it — a FRESH door so no prior toggle-close timer contaminates
                br.navigate(base + "/"); br.clear_storage(); br.reload(); wait_for(br, DOOR_READY, timeout=8.0)
                # focus the corner button as a keyboard user would, THEN open — so focus sits inside the box
                br.evaluate("(()=>{const c=document.querySelector('#exd-lang .exl-cur');c.focus();c.click();})()")
                wait_for(br, LIST_OPEN)
                open2 = br.evaluate(LIST_OPEN)
                br.evaluate("(()=>{const w=document.querySelector('.exd-window');if(w)w.focus();})()")
                wait_for(br, LIST_SHUT)
                out_closed = not br.evaluate(LIST_OPEN)
                check(B_ROWS[11], open1 and esc_closed and open2 and out_closed,
                      f"opened={open1}/{open2} esc_closed={esc_closed} focusout_closed={out_closed}")

        # finale — the continuation + exit controls are keyboard-reachable and named (fence)
        with shared(plain_br) as br:
            enter(br, base)
            br.evaluate("(()=>{const f=document.getElementById('exh-fin');"
                        "if(f)f.scrollIntoView({behavior:'instant'});})()")
            # the finale's own controls stand — the elements the read below names
            wait_for(br, "!!(document.getElementById('ex-unfold')||document.getElementById('ex-return'))")
            fin_ctrl = json.loads(br.evaluate(
                "(()=>{const g=id=>{const e=document.getElementById(id);if(!e)return null;"
                "return {tab:e.tabIndex>=0||e.tagName==='BUTTON',"
                "name:((e.getAttribute('aria-label')||e.textContent||'').trim().length>0)};};"
                "return JSON.stringify({more:g('ex-unfold'),ret:g('ex-return')});})()") or "{}")
            present = [c for c in (fin_ctrl.get("more"), fin_ctrl.get("ret")) if c]
            ok = len(present) >= 1 and all(c["tab"] and c["name"] for c in present)
            check(B_ROWS[12], ok, f"controls={fin_ctrl}")

        # share — the round share control is keyboard-reachable and named (fence)
        with shared(plain_br) as br:
            enter(br, base)
            sh = json.loads(br.evaluate(
                "(()=>{const e=document.getElementById('ex-share');if(!e)return 'null';"
                "return JSON.stringify({btn:e.tagName==='BUTTON',tab:e.tabIndex>=0||e.tagName==='BUTTON',"
                "name:((e.getAttribute('aria-label')||'').trim().length>0)});})()") or "null")
            check(B_ROWS[13], isinstance(sh, dict) and sh.get("btn") and sh.get("tab") and sh.get("name"),
                  f"share={sh}")

        # door — the windows are keyboard buttons named by title (fence, mirrors test_door #7)
        with shared(plain_br) as br:
            br.navigate(base + "/"); br.clear_storage(); br.reload(); wait_for(br, DOOR_READY, timeout=8.0)
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
    # Two groups, one Chrome each: the touch-emulated rows and the one keyboard leg.
    with serve(TMP) as base, \
            Browser(width=1280, height=900) as plain_br, \
            Browser(width=1280, height=900) as touch_br:
        touch_br.touch(True, 2)

        # A1 · a touch long-press on a walk work opens the gift ceremony (imageless clean-source path)
        with shared(touch_br) as br:
            enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            wait_for(br, GIFT_OPEN)                       # the ~500ms arm fires the ceremony
            opened = br.evaluate(GIFT_OPEN)
            ask = br.evaluate("(()=>{const a=document.querySelector('#ex-gift-card .gift-ask');"
                              "return a?(a.textContent||'').trim():'';})()")
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[0], bool(opened) and len(ask) > 0, f"opened={opened} ask={ask!r}")

        # A1 · the touch grab leaks no clean source — the open ceremony holds zero <img>, no clean-src ref
        with shared(touch_br) as br:
            enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            wait_for(br, GIFT_OPEN)                       # the ~500ms arm fires the ceremony
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
        with shared(touch_br) as br:
            br.navigate(base + "/"); br.clear_storage(); br.evaluate("sessionStorage.clear()")
            br.evaluate("localStorage.setItem('%s-tempo','1.0')" % NS_UPPER.lower()); br.reload()
            wait_for(br, DOOR_READY, timeout=8.0)
            began = br.evaluate("(%s)('.exd-window img')" % LP_START)
            wait_for(br, TOAST_UP)                        # the door's gracious line is the answer here
            gift = br.evaluate(GIFT_OPEN)
            toast = br.evaluate("(()=>{const t=document.getElementById('ex-toast');"
                                "return !!(t&&!t.hidden&&(t.textContent||'').trim());})()")
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[2], bool(began) and (not gift) and bool(toast),
                  f"began={began} gift_open={gift} toast={toast}")

        # A1 · the ~500ms arm gate — a short tap does NOT open, a full hold DOES
        with shared(touch_br) as br:
            enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.15); br.evaluate("(%s)()" % LP_END)   # released well before the arm — a tap
            br.sleep(0.6)   # a NOTHING-happens wait: no condition can name a ceremony that must not open
            short = br.evaluate(GIFT_OPEN)                    # must be False
            br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            wait_for(br, GIFT_OPEN)                           # a full hold past the arm
            full = br.evaluate(GIFT_OPEN)                     # must be True
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[3], (not short) and bool(full), f"short_tap_open={short} full_hold_open={full}")

        # A1 · the px-drift cancel — a small drift still fires; a large drift / a second finger cancel
        with shared(touch_br) as br:
            enter(br, base)
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.1); br.evaluate("(%s)(4)" % LP_MOVE)   # 4px — within threshold, still a hold
            wait_for(br, GIFT_OPEN)
            steady = br.evaluate(GIFT_OPEN)                   # must be True
            br.evaluate("(%s)()" % LP_END); br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.1); br.evaluate("(%s)(40)" % LP_MOVE)  # 40px — a swipe, cancels
            br.sleep(0.7)   # a NOTHING-happens wait: the cancelled hold has no state to poll for
            drift = br.evaluate(GIFT_OPEN)                    # must be False
            br.evaluate("(%s)()" % LP_END); br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            br.sleep(0.1); br.evaluate("(%s)()" % LP_SECOND)  # a second finger — the pinch wins
            br.sleep(0.7)   # a NOTHING-happens wait: the cancelled hold has no state to poll for
            pinch = br.evaluate(GIFT_OPEN)                    # must be False
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[4], bool(steady) and (not drift) and (not pinch),
                  f"steady_fires={steady} large_drift_open={drift} second_finger_open={pinch}")

        # A1 · coexistence — a swipe still steps, a pinch still zooms, a hold still grabs (all live together)
        with shared(touch_br) as br:
            enter(br, base)
            s0 = json.loads(br.evaluate(STEP_STATE))
            y0 = br.evaluate("Math.round(scrollY)")
            br.swipe(-320, settle=0.05)
            wait_settled(br, "Math.round(scrollY)", y0)       # the glide comes to rest
            s1 = json.loads(br.evaluate(STEP_STATE))
            swipe_ok = s1["idx"] > s0["idx"]                  # the walk glide is not clobbered
            z = json.loads(br.evaluate(PINCH_WORK_ZOOM) or "null")
            pinch_ok = bool(z and z.get("opened"))            # the inspect pinch is not clobbered
            br.key("Escape"); wait_for(br, layer_gone("ex-zoom"))
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            wait_for(br, GIFT_OPEN)
            grab_ok = br.evaluate(GIFT_OPEN)                  # the detector itself is live
            br.evaluate("(%s)()" % LP_END)
            check(A_ROWS[5], swipe_ok and pinch_ok and bool(grab_ok),
                  f"swipe_steps={swipe_ok} pinch_zooms={pinch_ok} longpress_grabs={grab_ok}")

        # D4 · the gift restores focus by origin — keyboard-open → the opener; touch-open → none
        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            br.evaluate("document.querySelector('.exh-frame').focus()")
            fid = br.evaluate("(()=>{const f=document.querySelector('.exh-frame');return f?f.dataset.id:'';})()")
            br.key("y"); wait_for(br, GIFT_OPEN)
            kopen = br.evaluate(GIFT_OPEN)
            # closeGift hands focus back before it hides the card, so a hidden card is proof the
            # restore has already run
            br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            krestored = br.evaluate("(()=>{const a=document.activeElement;"
                                    "return !!(a&&a.classList&&a.classList.contains('exh-frame')&&a.dataset.id==='%s');})()" % fid)
            key_ok = kopen and krestored
        with shared(touch_br) as br:
            enter(br, base, tempo="0.05")
            # a work is focused (as a keyboard user leaves it) BEFORE the TOUCH grab — a touch open must
            # still force NO restore (origin-conditioned like the zoom), so focus is off the work after close
            br.evaluate("document.querySelector('.exh-frame').focus()")
            br.evaluate("(%s)('.exh-frame img.work')" % LP_START)
            wait_for(br, GIFT_OPEN)
            topen = br.evaluate(GIFT_OPEN)
            br.evaluate("(%s)()" % LP_END)
            br.key("Escape"); wait_for(br, layer_gone("ex-gift-card"))
            no_forced = not br.evaluate(IN_FRAME)             # a touch open leaves focus off the walk work
            touch_ok = topen and no_forced
        check(A_ROWS[6], bool(key_ok) and bool(touch_ok),
              f"keyboard_open={kopen} keyboard_restored={krestored} touch_open={topen} touch_no_forced={no_forced}")

# ======================= Batch-K — the KEY ROADS AT ALL FOUR HANGING PLACES =======================
# CS-9 / INV-102 (B2/B3) extended to the four places a work HANGS: a walk photograph (.exh-frame), a
# door window (.exd-window), a polaroid on the table (.exs-print) and a lane picture in the series room
# (a direct <img> child of #exs-stage). The defect these rows exist over: the single keyboard opener was
# gated twice to the walk (faceStands() + .exh-frame), so three of the four places answered no key at
# all; and the gift ceremony was unreachable from a polaroid and from a lane picture on EVERY input.
#   · K1-K3  `z` opens the closer look at the door window / the polaroid / the lane picture
#   · K4     close restores focus to the opener at ALL FOUR places, four independently-reported legs
#   · K5     a standing closer look owns its own keys (z/y pass nothing through; Escape still leaves)
#   · K6-K8  the three grab roads (right-click · long press · `y`) at the polaroid / the lane / the door
#   · K9     every place ANNOUNCES its keys (aria-keyshortcuts) in the live DOM
#   · K10    close falls back to the standing surface when the opener has left the page
# Every browser row asserts its OWN REACH first: an element not found, not focusable, or a precondition
# layer that never opened FAILS the row with a detail saying so — never a quiet pass.
K_ROWS = [
    "K1 a real `z` on a focused DOOR WINDOW opens the closer look on that window's picture (door standing)",
    "K2 a real `z` on a focused POLAROID opens the closer look on that print's photograph, and Enter still "
    "lifts the print (room standing)",
    "K3 a real `z` on a focused LANE picture opens the closer look on it (a lane-variant room standing)",
    "K4 close restores focus to the OPENER at all four hanging places (walk frame · door window · polaroid · "
    "lane picture) — four independently-reported legs",
    "K5 a standing closer look owns its keys — `z` opens nothing further, `y` opens no ceremony over it, "
    "and a real Escape still leaves",
    "K6 a POLAROID reaches the gift ceremony by all three roads (right-click · real long press · real `y`)",
    "K7 a LANE picture reaches the gift ceremony by all three roads (right-click · real long press · real `y`)",
    "K8 a DOOR WINDOW answers all three roads with the gracious toast and NO ceremony (right-click · real "
    "long press · real `y`)",
    "K9 all four hanging places announce their keys in the live DOM (aria-keyshortcuts: walk/polaroid/lane "
    "`z y`, the door window `z` only — the door offers no ceremony to announce)",
    "K10 close falls back to the standing surface when the opener has left the page (never the document body)",
    "K11 Escape over a closer look opened FROM the series room leaves the closer look only — the room "
    "still stands beneath it and keeps its focused polaroid (a standing layer owns its keys)",
]

LANE_IDX = next((i for i, s in enumerate(SERIES) if s.get("variant") == "lane"), None)
POLA_IDX = next((i for i, s in enumerate(SERIES) if s.get("variant") != "lane"), None)

# focus a hanging place, stash it as the expected opener, and report the reach + its picture's basename
FOCUS_PLACE = ("(sel)=>{const e=document.querySelector(sel);"
               "if(!e)return JSON.stringify({found:false,focused:false,pic:''});"
               "window.__opener=e;e.focus();"
               "const im=(e.tagName==='IMG')?e:e.querySelector('img');"
               "const s=im?(im.currentSrc||im.getAttribute('src')||''):'';"
               "return JSON.stringify({found:true,focused:document.activeElement===e,"
               "pic:((s.split('?')[0].split('/').pop())||'')});}")
ZOOM_PIC = ("(()=>{const i=document.querySelector('#ex-zoom .exz-img');if(!i)return '';"
            "const s=i.currentSrc||i.getAttribute('src')||'';"
            "return (s.split('?')[0].split('/').pop())||'';})()")
ZOOM_OPEN = "(()=>{const e=document.getElementById('ex-zoom');return !!(e&&!e.hidden);})()"
ZOOM_CLOSE_X = ("(()=>{const b=document.querySelector('#ex-zoom .exz-close');"
                "if(!b)return false;b.click();return true;})()")
IS_OPENER = "(()=>document.activeElement===window.__opener)()"
TOAST_ON = ("(()=>{const t=document.getElementById('ex-toast');"
            "return !!(t&&!t.hidden&&(t.textContent||'').trim());})()")
CTX_ON = ("(sel)=>{const e=document.querySelector(sel);if(!e)return false;"
          "e.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}));return true;}")
KEYSHORTCUTS = ("(sel)=>{const e=document.querySelector(sel);"
                "return e?(e.getAttribute('aria-keyshortcuts')===null?'@none':"
                "e.getAttribute('aria-keyshortcuts')):'@missing';}")


def at_door(br, base, tempo="0.4"):
    """Land on the FRONT DOOR, standing — no pick, so the door face holds."""
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("sessionStorage.clear()")
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.reload()
    wait_for(br, DOOR_READY, timeout=8.0)          # the door's windows are up and pictured


def in_room(br, base, idx):
    """Land in the walk, then open the series room at `idx` and let its veil crossing settle."""
    enter(br, base)
    br.evaluate("(%s)(%d)" % (OPEN_SERIES, idx))
    wait_for(br, ROOM_READY)


if not chrome_available():
    for r in K_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    # Two groups, one Chrome each: the plain rows and the touch-emulated long-press roads.
    with serve(TMP) as base, \
            Browser(width=1280, height=900) as plain_br, \
            Browser(width=1280, height=900) as touch_br:
        touch_br.touch(True, 2)

        # K1 — `z` on a focused door window opens the closer look on that window's picture
        with shared(plain_br) as br:
            at_door(br, base)
            reach = json.loads(br.evaluate("(%s)('.exd-window')" % FOCUS_PLACE))
            if not (reach.get("found") and reach.get("focused") and reach.get("pic")):
                check(K_ROWS[0], False, f"REACH FAILED — the door window was not found/focusable/pictured: {reach}")
            else:
                br.key("z")
                wait_for(br, ZOOM_OPEN)
                opened = br.evaluate(ZOOM_OPEN)
                pic = br.evaluate(ZOOM_PIC)
                check(K_ROWS[0], bool(opened) and pic == reach["pic"],
                      f"zoom_open={opened} zoom_pic={pic!r} window_pic={reach['pic']!r}")

        # K2 — `z` on a focused polaroid opens the closer look; Enter on the same print still LIFTS it
        with shared(plain_br) as br:
            if POLA_IDX is None:
                skip(K_ROWS[1], "the fixture bakes no polaroid-variant series")
            else:
                in_room(br, base, POLA_IDX)
                reach = json.loads(br.evaluate("(%s)('#exs-stage .exs-print')" % FOCUS_PLACE))
                if not (reach.get("found") and reach.get("focused") and reach.get("pic")):
                    check(K_ROWS[1], False,
                          f"REACH FAILED — the polaroid was not found/focusable/pictured: {reach}")
                else:
                    br.key("z")
                    wait_for(br, ZOOM_OPEN)
                    zopen = br.evaluate(ZOOM_OPEN)
                    zpic = br.evaluate(ZOOM_PIC)
                    br.evaluate(ZOOM_CLOSE_X)
                    wait_for(br, layer_gone("ex-zoom"))
                    # Enter on the print keeps its own meaning — the lift, never the closer look
                    br.evaluate("(()=>{const p=document.querySelector('#exs-stage .exs-print');"
                                "if(p)p.focus();})()")
                    br.key("Enter")
                    wait_for(br, "!!document.querySelector('#exs-stage .exs-print.lift')")
                    lifted = br.evaluate("!!document.querySelector('#exs-stage .exs-print.lift')")
                    check(K_ROWS[1], bool(zopen) and zpic == reach["pic"] and bool(lifted),
                          f"zoom_open={zopen} zoom_pic={zpic!r} print_pic={reach['pic']!r} enter_lifts={lifted}")

        # K3 — `z` on a focused lane picture opens the closer look on it
        with shared(plain_br) as br:
            if LANE_IDX is None:
                skip(K_ROWS[2], "the fixture bakes no lane-variant series")
            else:
                in_room(br, base, LANE_IDX)
                reach = json.loads(br.evaluate("(%s)('#exs-stage > img')" % FOCUS_PLACE))
                if not (reach.get("found") and reach.get("focused") and reach.get("pic")):
                    check(K_ROWS[2], False,
                          f"REACH FAILED — the lane picture was not found/focusable/pictured: {reach}")
                else:
                    br.key("z")
                    wait_for(br, ZOOM_OPEN)
                    opened = br.evaluate(ZOOM_OPEN)
                    pic = br.evaluate(ZOOM_PIC)
                    check(K_ROWS[2], bool(opened) and pic == reach["pic"],
                          f"zoom_open={opened} zoom_pic={pic!r} lane_pic={reach['pic']!r}")

        # K4 — close restores focus to the OPENER at all four places, each leg reported on its own
        legs = {}

        def restore_leg(br, sel):
            """Focus `sel`, open the closer look with `z`, close by the ×, report whether focus came home."""
            reach = json.loads(br.evaluate("(%s)(%s)" % (FOCUS_PLACE, json.dumps(sel))))
            if not (reach.get("found") and reach.get("focused")):
                return {"reach": False, "detail": f"not found/focusable: {reach}"}
            br.key("z")
            wait_for(br, ZOOM_OPEN)
            if not br.evaluate(ZOOM_OPEN):
                return {"reach": False, "detail": "the closer look never opened on `z`"}
            br.evaluate(ZOOM_CLOSE_X)
            # the close hands focus back before the layer's flight hides it — a hidden layer is proof
            # the restore has already run
            wait_for(br, layer_gone("ex-zoom"))
            return {"reach": True, "restored": bool(br.evaluate(IS_OPENER))}

        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            legs["walk frame"] = restore_leg(br, ".exh-frame")
        with shared(plain_br) as br:
            at_door(br, base, tempo="0.05")
            legs["door window"] = restore_leg(br, ".exd-window")
        if POLA_IDX is not None:
            with shared(plain_br) as br:
                in_room(br, base, POLA_IDX)
                legs["polaroid"] = restore_leg(br, "#exs-stage .exs-print")
        if LANE_IDX is not None:
            with shared(plain_br) as br:
                in_room(br, base, LANE_IDX)
                legs["lane picture"] = restore_leg(br, "#exs-stage > img")
        k4_ok = len(legs) == 4 and all(v.get("reach") and v.get("restored") for v in legs.values())
        check(K_ROWS[3], k4_ok, "legs=" + json.dumps(legs))

        # K5 — a standing closer look owns its keys: z opens nothing further, y no ceremony, Esc leaves
        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            reach = json.loads(br.evaluate("(%s)('.exh-frame')" % FOCUS_PLACE))
            br.key("z")
            wait_for(br, ZOOM_OPEN)
            if not (reach.get("focused") and br.evaluate(ZOOM_OPEN)):
                check(K_ROWS[4], False,
                      f"REACH FAILED — the closer look never stood to be guarded: reach={reach} "
                      f"zoom_open={br.evaluate(ZOOM_OPEN)}")
            else:
                pic0 = br.evaluate(ZOOM_PIC)
                br.key("z")
                br.sleep(0.5)   # a NOTHING-happens wait: a second layer must never appear to poll for
                still = br.evaluate(ZOOM_OPEN)
                pic1 = br.evaluate(ZOOM_PIC)
                nzooms = br.evaluate("document.querySelectorAll('#ex-zoom').length")
                br.key("y")
                br.sleep(0.5)   # a NOTHING-happens wait: the ceremony must never open over the layer
                gift = br.evaluate(GIFT_OPEN)
                br.key("Escape")
                wait_for(br, layer_gone("ex-zoom"))
                left = not br.evaluate(ZOOM_OPEN)
                check(K_ROWS[4],
                      bool(still) and pic0 == pic1 and nzooms == 1 and (not gift) and left,
                      f"still_open={still} pic_before={pic0!r} pic_after={pic1!r} zoom_layers={nzooms} "
                      f"gift_over_it={gift} escape_left={left}")

        # K6/K7 — a polaroid and a lane picture each reach the gift ceremony by all THREE roads
        def three_roads(idx, place_sel, pic_sel, focus_sel):
            """right-click (desktop) · real long press (touch) · real `y` — the fine-pointer roads on
            the plain browser, the long press on the touch-emulated one."""
            out = {}
            with shared(plain_br) as br:                           # right-click, fine pointer
                in_room(br, base, idx)
                if not br.evaluate("!!document.querySelector(%s)" % json.dumps(pic_sel)):
                    out["right-click"] = "REACH FAILED — no picture at " + pic_sel
                else:
                    br.evaluate("(%s)(%s)" % (CTX_ON, json.dumps(pic_sel)))
                    wait_for(br, GIFT_OPEN)
                    out["right-click"] = bool(br.evaluate(GIFT_OPEN))
            with shared(touch_br) as br:                           # a real long press, coarse pointer
                in_room(br, base, idx)
                began = br.evaluate("(%s)(%s)" % (LP_START, json.dumps(pic_sel)))
                if not began:
                    out["long press"] = "REACH FAILED — no picture at " + pic_sel
                else:
                    wait_for(br, GIFT_OPEN)                        # past the ~500ms arm
                    out["long press"] = bool(br.evaluate(GIFT_OPEN))
                    br.evaluate("(%s)()" % LP_END)
            with shared(plain_br) as br:                           # the real `y` key from the focused place
                in_room(br, base, idx)
                reach = json.loads(br.evaluate("(%s)(%s)" % (FOCUS_PLACE, json.dumps(focus_sel))))
                if not (reach.get("found") and reach.get("focused")):
                    out["y key"] = f"REACH FAILED — not found/focusable: {reach}"
                else:
                    br.key("y")
                    wait_for(br, GIFT_OPEN)
                    out["y key"] = bool(br.evaluate(GIFT_OPEN))
            return out

        if POLA_IDX is None:
            skip(K_ROWS[5], "the fixture bakes no polaroid-variant series")
        else:
            r6 = three_roads(POLA_IDX, ".exs-print", "#exs-stage .exs-print img", "#exs-stage .exs-print")
            check(K_ROWS[5], all(v is True for v in r6.values()), "roads=" + json.dumps(r6))
        if LANE_IDX is None:
            skip(K_ROWS[6], "the fixture bakes no lane-variant series")
        else:
            r7 = three_roads(LANE_IDX, "#exs-stage > img", "#exs-stage > img", "#exs-stage > img")
            check(K_ROWS[6], all(v is True for v in r7.values()), "roads=" + json.dumps(r7))

        # K8 — a door window answers all three roads with the gracious toast and NO ceremony
        r8 = {}
        with shared(plain_br) as br:                               # right-click, fine pointer
            at_door(br, base)
            if not br.evaluate("!!document.querySelector('.exd-window img')"):
                r8["right-click"] = "REACH FAILED — no door window picture"
            else:
                br.evaluate("(%s)('.exd-window img')" % CTX_ON)
                wait_for(br, TOAST_ON)                             # the gracious line is the answer
                r8["right-click"] = {"toast": bool(br.evaluate(TOAST_ON)), "gift": bool(br.evaluate(GIFT_OPEN))}
        with shared(touch_br) as br:                               # a real long press, coarse pointer
            at_door(br, base, tempo="1.0")
            began = br.evaluate("(%s)('.exd-window img')" % LP_START)
            if not began:
                r8["long press"] = "REACH FAILED — no door window picture"
            else:
                wait_for(br, TOAST_ON)
                r8["long press"] = {"toast": bool(br.evaluate(TOAST_ON)), "gift": bool(br.evaluate(GIFT_OPEN))}
                br.evaluate("(%s)()" % LP_END)
        with shared(plain_br) as br:                               # the real `y` key from the focused window
            at_door(br, base)
            reach = json.loads(br.evaluate("(%s)('.exd-window')" % FOCUS_PLACE))
            if not (reach.get("found") and reach.get("focused")):
                r8["y key"] = f"REACH FAILED — not found/focusable: {reach}"
            else:
                br.key("y")
                wait_for(br, TOAST_ON)
                r8["y key"] = {"toast": bool(br.evaluate(TOAST_ON)), "gift": bool(br.evaluate(GIFT_OPEN))}
        k8_ok = (len(r8) == 3 and all(isinstance(v, dict) and v.get("toast") and not v.get("gift")
                                      for v in r8.values()))
        check(K_ROWS[7], k8_ok, "roads=" + json.dumps(r8))

        # K9 — every hanging place ANNOUNCES its keys in the live DOM
        ks = {}
        with shared(plain_br) as br:
            at_door(br, base)
            ks["door window (z)"] = br.evaluate("(%s)('.exd-window')" % KEYSHORTCUTS)
            enter(br, base)
            ks["walk frame (z y)"] = br.evaluate("(%s)('.exh-frame')" % KEYSHORTCUTS)
        if POLA_IDX is not None:
            with shared(plain_br) as br:
                in_room(br, base, POLA_IDX)
                ks["polaroid (z y)"] = br.evaluate("(%s)('#exs-stage .exs-print')" % KEYSHORTCUTS)
        if LANE_IDX is not None:
            with shared(plain_br) as br:
                in_room(br, base, LANE_IDX)
                ks["lane picture (z y)"] = br.evaluate("(%s)('#exs-stage > img')" % KEYSHORTCUTS)
        k9_ok = (len(ks) == 4
                 and ks.get("walk frame (z y)") == "z y"
                 and ks.get("polaroid (z y)") == "z y"
                 and ks.get("lane picture (z y)") == "z y"
                 and ks.get("door window (z)") == "z")
        check(K_ROWS[8], k9_ok, "announced=" + json.dumps(ks))

        # K10 — the opener has LEFT the page by the time the layer closes: focus lands on the surface
        # still standing beneath it (the walk stage here), never on the document body
        with shared(plain_br) as br:
            enter(br, base, tempo="0.05")
            reach = json.loads(br.evaluate("(%s)('.exh-frame')" % FOCUS_PLACE))
            br.key("z")
            wait_for(br, ZOOM_OPEN)
            if not (reach.get("focused") and br.evaluate(ZOOM_OPEN)):
                check(K_ROWS[9], False, f"REACH FAILED — the closer look never opened: reach={reach}")
            else:
                br.evaluate("(()=>{window.__opener.remove();})()")   # the opener leaves the page
                br.evaluate(ZOOM_CLOSE_X)
                wait_for(br, layer_gone("ex-zoom"))
                landed = json.loads(br.evaluate(
                    "(()=>{const a=document.activeElement;return JSON.stringify({"
                    "body:a===document.body,id:a?(a.id||''):'',tag:a?a.tagName:''});})()"))
                check(K_ROWS[9], (not landed.get("body")) and landed.get("id") == "ex-stage",
                      f"landed={landed}")

        # K11 — the new nesting road (a closer look opened by `z` from a polaroid, over the standing
        # room) must exit ONE layer at a time. The room's own Escape and the closer look's own Escape
        # are two independent document listeners, so an unguarded room takes a step back of its own and
        # the single key tears down both layers, landing the visitor out on the walk.
        with shared(plain_br) as br:
            if POLA_IDX is None:
                skip(K_ROWS[10], "the fixture bakes no polaroid-variant series")
            else:
                in_room(br, base, POLA_IDX)
                reach = json.loads(br.evaluate("(%s)('#exs-stage .exs-print')" % FOCUS_PLACE))
                br.key("z")
                wait_for(br, ZOOM_OPEN)
                if not (reach.get("focused") and br.evaluate(ZOOM_OPEN)):
                    check(K_ROWS[10], False,
                          f"REACH FAILED — the closer look never stood over the room: reach={reach}")
                else:
                    br.key("Escape")
                    wait_for(br, layer_gone("ex-zoom"))
                    after = json.loads(br.evaluate(
                        "(()=>{const z=document.getElementById('ex-zoom'),s=document.getElementById('ex-side');"
                        "return JSON.stringify({zoom:!!(z&&!z.hidden),room:!!(s&&!s.hidden),"
                        "on_print:document.activeElement===window.__opener});})()"))
                    check(K_ROWS[10],
                          (not after.get("zoom")) and after.get("room") and after.get("on_print"),
                          f"after_escape={after}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, stt, detail in results:
    print(f"[{stt}] {name}" + (f"  — {detail}" if detail and stt != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
