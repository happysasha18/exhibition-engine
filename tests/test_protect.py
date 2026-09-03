#!/usr/bin/env python3
"""EX-PROTECT (INV-49): right-click / drag / pinch protection on hung works.
A grabbed work meets a gracious enjoy line (via the shared toast), never the browser's raw
save sheet. The `enjoy` i18n key ships in the locale schema and the validate gate.
Run: python tests/test_protect.py
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image

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


TMP = Path(tempfile.mkdtemp(prefix="synth_protect_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# ---------------------------------------------------------------- carry-home resolution probes
# EX-PROTECT-RES (INV-56): the file a grab hands over is capped at GRAB_MAX_PX on its long edge, so the
# quiz prize (the pre-marked ~1000 px bake) stays the better file on every screen. The synthetic fixture
# hangs 64 px stand-ins, so the rows below hang a probe image of a KNOWN size on the work instead and
# read the dimensions of the real file the browser saved. Two probes: one over the cap, one under it.
GRAB_MAX_PX = 800                      # mirrors the client constant (engine/client/11-protect-gift.js)
PROBE_OVER = ("probe-over.jpg", 1600, 1000)     # a retina-tier grab: must come back capped
PROBE_UNDER = ("probe-under.jpg", 320, 200)     # already inside the cap: must come back untouched


def write_probe(name, w, h):
    """A real JPEG of exactly w x h, served from the bake so the canvas is never tainted."""
    Image.linear_gradient("L").resize((w, h)).convert("RGB").save(TMP / name, "JPEG", quality=88)


for _n, _w, _h in (PROBE_OVER, PROBE_UNDER):
    write_probe(_n, _w, _h)

# ---------------------------------------------------------------- data rows

def zoom_layer_slice(js):
    """The zoom layer's own region of the served client, located by the keep-markers the assembler
    writes around every fragment (`/*!12-zoom-inspect-grab.js*/`, kept through the bake's comment
    strip). A missing marker is a FAILURE of the check itself, never a quiet pass — a gate's verdict
    is worthless without its reach. Until 2026-07-27 the region was found by hunting two SENTENCES
    inside comments, so rewording a comment moved the region silently and stripping the comments
    erased it outright."""
    MARK = "/*!12-zoom-inspect-grab.js*/"
    a = js.find(MARK)
    if a < 0:
        return None
    b = js.find("/*!", a + 3)
    return js[a:(b if b >= 0 else len(js))]


def protect_layer_slice(js):
    """The gift/protect layer's own region of the served client, located by the same keep-marker idiom
    the zoom slice uses (`/*!11-protect-gift.js*/`). A missing marker fails the check that reads it."""
    MARK = "/*!11-protect-gift.js*/"
    a = js.find(MARK)
    if a < 0:
        return None
    b = js.find("/*!", a + 3)
    return js[a:(b if b >= 0 else len(js))]


def between(text, start, end):
    """The region of `text` from `start` up to `end` — both located by their literal opening. Returns
    "" when either anchor is missing, so a row built on it fails rather than passing on nothing."""
    if not text:
        return ""
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i + len(start))
    return text[i:(j if j >= 0 else len(text))]

# 1 · the `enjoy` string is present in the greetings cache and the worker schema
greet = json.loads((TMP / "exhibition_data.json").read_text()).get("greet") or {}
langs = greet.get("langs") or {}
missing_enjoy = [c for c, L in langs.items() if not (L.get("enjoy") or "").strip()]
worker_src = (ROOT / "engine" / "assets" / "worker.js").read_text(encoding="utf-8")
enjoy_in_schema = '"enjoy"' in worker_src and "enjoy" in worker_src
check("EX-PROTECT enjoy string in locale cache (all langs) + worker schema includes enjoy",
      not missing_enjoy and enjoy_in_schema,
      f"missing_enjoy={missing_enjoy} schema_has_enjoy={enjoy_in_schema}")

# 2 · CSS: img.work carries the soft-deter properties, and the axis reading EX-HANG owes
# EVERY READING HERE IS TAKEN INSIDE img.work's OWN BLOCK (2026-09-03, plan row S-79). Until today
# each of these was a substring search over the whole 800-line file, so `touch-action:pan-x pan-y`
# read green off the BODY rule at line 19 no matter what img.work carried — the row named one
# selector and asserted another. Slicing the block first is what makes the row bite on img.work.
css_src = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")


def css_block(selector):
    """Every rule this selector opens, each from its selector to the `}` that closes it, joined.
    All of them and not the first: `.exh-frame img.work` opens two — the deter block and the
    reduced-motion override — and a reading that takes whichever comes first answers about the
    wrong one."""
    out, at = [], css_src.find(selector + "{")
    while at >= 0:
        end = css_src.find("}", at)
        out.append(css_src[at:end + 1] if end > 0 else css_src[at:])
        at = css_src.find(selector + "{", at + 1)
    return "\n".join(out)


work_block = css_block(".exh-frame img.work")
body_block = css_block("body")
css_ok = ("user-select:none" in work_block
          and "-webkit-user-drag:none" in work_block
          and "-webkit-touch-callout:none" in work_block
          # THE AXIS READING (SPEC Requirement 38, "Where the axis law reaches" — EX-HANG bound).
          # `pan-y` and not `pan-x pan-y`: the page keeps the vertical (travel between works) and
          # the work claims the horizontal (travel within one work). It is still narrower than
          # `pan-x pan-y`, so INV-49's pinch and double-tap refusal stands on the work unchanged.
          and "touch-action:pan-y" in work_block
          and "touch-action:pan-x pan-y" not in work_block)
check("EX-PROTECT CSS: img.work carries user-select/user-drag/touch-callout:none, and its axis "
      "reading is touch-action:pan-y — the page's vertical kept, the work's horizontal claimed",
      css_ok, f"img.work's own block reads: {' '.join(work_block.split())[:400]}")

# 2b · the body class rule keeps BOTH axes, and that is EX-SERIES's exemption rather than an oversight
check("EX-PROTECT CSS: the body class rule still yields both axes, so the series side room keeps "
      "the sideways lane its dated exemption names (EX-SERIES, INV-88)",
      "touch-action:pan-x pan-y" in body_block,
      f"body's own block reads: {' '.join(body_block.split())[:400]}")

# 3 · JS: enjoyLine, onGrab, contextmenu/dragstart/gesturestart/gesturechange all present
js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
js_ok = ("function enjoyLine(" in js_src
         and "function onGrab(" in js_src
         and "contextmenu" in js_src
         and "dragstart" in js_src
         and "gesturestart" in js_src
         and "gesturechange" in js_src
         and "ev.preventDefault()" in js_src)
check("EX-PROTECT JS: enjoyLine, onGrab, contextmenu/dragstart/gesturestart/gesturechange wired",
      js_ok, "one or more EX-PROTECT symbols missing from exhibition.js")

# 3b · JS: the pinch-zoom lock is WALK-WIDE (his phone field-find) — a browser zoom on any margin
#      desyncs the JS scroll animator + fixed chrome, so gesture events are refused at the DOCUMENT
#      level (not only the stage/image), gestureend included, and a two-finger touchmove is guarded
#      (Blink's pinch). Red before the walk-wide fix (was stage-scoped, image-only, no multi-touch).
zoom_ok = ('["gesturestart", "gesturechange", "gestureend"]' in js_src
           and "document.addEventListener(g" in js_src
           and "e.touches.length > 1" in js_src)
check("EX-PROTECT JS: pinch-zoom locked walk-wide (document-level gestures + two-finger touchmove guard)",
      zoom_ok, "walk-wide zoom lock missing — gestures still stage/image-scoped or no multi-touch guard")

# 3c · the viewport meta pins the page to scale 1 (helps Blink; Safari is held by the gesture block)
build_src = (ROOT / "engine" / "build.py").read_text(encoding="utf-8")
vp_ok = "maximum-scale=1" in build_src and "user-scalable=no" in build_src
check("EX-PROTECT viewport: the meta pins scale to 1 (maximum-scale=1 + user-scalable=no)",
      vp_ok, "viewport meta does not pin scale — pinch-zoom can still scale the page")

# 3d · the walk-wide zoom/swipe audit fixes (all red before this pass):
#   - double-tap zoom blocked at the touch-action layer (iOS ignores the viewport meta)
#   - a Ctrl/trackpad-pinch wheel is not consumed as a walk step
#   - the volume slider + share button keep native touch (not hijacked by the swipe)
#   - a pinch that drops back to one finger re-takes the paginated walk (no native fly-through)
css_src = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")
audit_ok = ("touch-action:pan-xpan-y" in body_block.replace(" ", "")   # the body class rule kills double-tap too
            and 'if (wheelMode === "zoom") { e.preventDefault(); pinchWheel(e); return; }' in js_src
            and "#ex-sound, .ex-share" in js_src
            and (lambda s: s is not None and "touchcancel" in s)(zoom_layer_slice(js_src))
            and "e.touches.length === 1 && walkOwnsInput()" in js_src)
check("EX-PROTECT touch audit: double-tap lock + ctrl-wheel guard + chrome native-touch + pinch-release re-arm",
      audit_ok, "one of the zoom/swipe audit fixes is missing (double-tap / ctrl-wheel / slider / re-arm)")

_zslice = zoom_layer_slice(js_src)
check("EX-PROTECT the cancel fence reaches the zoom layer's own region (both anchors found)",
      _zslice is not None,
      "the zoom fragment's anchors were not found in the assembled client — the fence read nothing")
check("EX-ZOOM/INV-82 the zoom layer carries its own touchcancel road",
      bool(_zslice) and "touchcancel" in _zslice,
      "no touchcancel handler inside the zoom layer's region")

# ---- 2026-07-22: the deter is a CLASS over every face that shows a picture, not most of them ----
# His find: a pinch-enlarged work and a polaroid could both raise the phone's native «Save to Photos»
# in front of the gift ceremony, because their pictures lacked the callout suppressor the hung work
# and door window carry. Each row asserts the property INSIDE that selector's own rule block, so a
# callout on some OTHER selector cannot green a face that is still unguarded (reach before verdict).
def css_block(css, sel):
    i = css.find(sel + "{")
    if i < 0:
        i = css.find(sel + " {")
    if i < 0:
        return None
    j = css.find("}", i)
    return css[i:j] if j > i else None

# 4 · the polaroid picture wears the same soft deter as the hung work
_print_block = css_block(css_src, ".exs-print img")
check("EX-PROTECT the polaroid rule block is located (reach — the check reads its own subject)",
      _print_block is not None, "'.exs-print img' rule not found in exhibition.css")
check("EX-PROTECT CSS: the polaroid picture (.exs-print img) carries -webkit-touch-callout:none + user-drag/select",
      bool(_print_block) and "-webkit-touch-callout:none" in _print_block
      and "-webkit-user-drag:none" in _print_block and "user-select:none" in _print_block,
      f"polaroid deter missing in its own block: {(_print_block or '')[:140]!r}")

# 5 · the enlarged view — the largest, most saveable face — wears it too (the gap the prover named
#     at the 1.9.0 gate: the enlarged view sat between the deterrent and the four-place set)
_zimg_block = css_block(css_src, "#ex-zoom .exz-img")
check("EX-PROTECT the enlarged-view rule block is located (reach)",
      _zimg_block is not None, "'#ex-zoom .exz-img' rule not found in exhibition.css")
check("EX-PROTECT CSS: the enlarged view (.exz-img) carries -webkit-touch-callout:none + user-drag/select",
      bool(_zimg_block) and "-webkit-touch-callout:none" in _zimg_block
      and "-webkit-user-drag:none" in _zimg_block and "user-select:none" in _zimg_block,
      f"enlarged-view deter missing in its own block: {(_zimg_block or '')[:140]!r}")

# 6 · JS: #ex-zoom lives on document.body, so it binds its OWN raw-save guard — a desktop right-click
#     / drag on the magnified copy is prevented and answered by the gracious toast like every face
zoom_guard_ok = ('zoom.addEventListener("contextmenu"' in js_src
                 and 'zoom.addEventListener("dragstart"' in js_src)
check("EX-PROTECT JS: the enlarged view binds its own contextmenu + dragstart guard",
      zoom_guard_ok, "no contextmenu/dragstart guard bound on #ex-zoom")

# 7 · JS: the handed file reaches the phone's Photos library through the native share sheet — a
#     coarse-pointer device gets navigator.share({files:[File]}) (the one web road into Photos), the
#     desktop keeps the anchor save. Red before 2026-07-22: the save was <a download> only, which iOS
#     drops into Files, not Photos («даунлоадится непонятно куда»).
share_ok = ("navigator.share" in js_src and "navigator.canShare" in js_src
            and "new File(" in js_src and 'matchMedia("(pointer: coarse)")' in js_src
            and "function saveBlob(" in js_src)
check("EX-PROTECT-RES JS: the gift saves to Photos via the share sheet on touch, anchor on desktop",
      share_ok, "the save-to-photos share path is missing (navigator.share / canShare / File / coarse gate)")

# 8 · JS: the watermarked file is rendered AHEAD (renderGiftBlob on openGift) so a yes-tap shares it
#     WITHIN the gesture — iOS refuses a share after an async stamp, so the pre-render keeps activation
prerender_ok = ("function renderGiftBlob(" in js_src
                and "renderGiftBlob(src, preMarked)" in js_src
                and "giftBlobFor === src" in js_src)
check("EX-PROTECT-RES JS: the gift blob is pre-rendered on open so the yes-tap shares within the gesture",
      prerender_ok, "renderGiftBlob is not wired into openGift / not consumed by giftDownload")

# 8b · EX-PROTECT-RES (INV-56): the two handed-over files differ ON PURPOSE, and only ONE of them is
#      capped. The ordinary grab is drawn down to GRAB_MAX_PX and stamped; the quiz prize is the
#      pre-marked bake and travels a road with no canvas on it at all, so winning the quiz always
#      brings home the larger picture. Red before 2026-07-28: no cap existed, so a retina right-click
#      carried away a 1280 px file while the prize stayed ~1000 px.
_pslice = protect_layer_slice(js_src)
_stamp_fn = between(_pslice, "function stampToBlob(", "function renderGiftBlob(")
_deliver = between(_pslice, "function renderGiftBlob(", "function openGift(")
_prize_branch = between(between(_deliver, "function giftDownload(", "\n  }\n"), "if (preMarked) {", "} else {")
prize_bits = {
    "the protect layer's region is located (reach — the row reads its own subject)": _pslice is not None,
    "the cap is a named constant in the fragment": "GRAB_MAX_PX = 800" in (_pslice or ""),
    "the cap is applied where the grabbed file is drawn (inside stampToBlob)":
        "GRAB_MAX_PX" in _stamp_fn and "drawImage(im, 0, 0, cv.width, cv.height)" in _stamp_fn,
    "the cap never enlarges a smaller image (Math.min(1, ...))": "Math.min(1, GRAB_MAX_PX" in _stamp_fn,
    "no cap sits on the delivery routing itself": "GRAB_MAX_PX" not in _deliver,
    "the prize road hands the pre-marked bytes over as they are (fetch → blob → saveBlob, no canvas)":
        bool(_prize_branch) and "fetch(src)" in _prize_branch and "saveBlob(blob" in _prize_branch
        and "stampToBlob" not in _prize_branch,
}
check("EX-PROTECT-RES (INV-56): the ordinary grab is capped at GRAB_MAX_PX (800) on its long edge and "
      "never enlarged, while the quiz prize keeps travelling its own pre-marked road untouched — the "
      "won picture stays the better file on every screen",
      all(prize_bits.values()),
      "failing: " + ", ".join(k for k, v in prize_bits.items() if not v))

# 9 · JS: the buy line stays HIDDEN until a shop exists — an empty content key hides it with NO
#     literal fallback (his word 2026-07-22: rephrase to «buy a larger print», hide until it exists)
buy_ok = ("buyEl.hidden" in js_src and "for a larger print — buy" not in js_src)
check("EX-PROTECT buy line: hidden on an empty key, the old print CTA fallback gone",
      buy_ok, "the buy line still carries a hardcoded fallback / is not hidden on empty")

# 10 · the gift ceremony's wash is a gradient that lets the work show through (his pick 2026-07-22,
#      option C) and STILL preserves the deterrent: the pseudo-layer is pointer-transparent so the full
#      card catches every touch even where the wash is clear, and the quiz prize keeps a near-solid dark
#      stage. Red before this, when the show state was a flat rgba(8,8,7,.88).
_before = css_block(css_src, "#ex-gift-card::before")
_prize = css_block(css_src, "#ex-gift-card.prize.show::before")
check("EX-PROTECT the ceremony wash block is located (reach)", _before is not None,
      "'#ex-gift-card::before' rule not found in exhibition.css")
wash_ok = (bool(_before) and "linear-gradient" in _before and "pointer-events:none" in _before
           and "#ex-gift-card.show::before" in css_src
           and bool(_prize) and "rgba(8,8,7,.92)" in _prize
           and "#ex-gift-card.show{ background:rgba(8,8,7,.88)" not in css_src)
check("EX-PROTECT the ceremony wash is a gradient (option C), pointer-transparent so the card still "
      "catches every touch; the quiz prize keeps a solid dark stage; the old flat scrim is gone",
      wash_ok, f"wash={(_before or '')[:120]!r} prize={(_prize or '')[:80]!r}")

BROWSER_ROWS = [
    "EX-PROTECT-GIFT desktop right-click on a work opens the gift ceremony (not a browser save sheet)",
    "EX-PROTECT drag on a work is prevented (no drag ghost, enjoy toast fires)",
    "EX-PROTECT-GIFT the gift ceremony line carries the site host from ROOT_URL",
    "EX-PROTECT right-click on chrome (share button) is NOT intercepted (browser menu still works)",
    "EX-PROTECT the enlarged view refuses a raw save on Blink (Android's engine): a contextmenu on "
    ".exz-img is prevented and answered by the gracious line, the road Android relies on (iOS uses the "
    "callout instead, which Blink ignores)",
    "EX-PROTECT-RES (INV-56) an ordinary grab of a work shown larger than the cap saves a file whose "
    "long edge is exactly 800 px — the real file the browser wrote, measured on disk",
    "EX-PROTECT-RES (INV-56) a work already shown smaller than the cap is saved at its own size — the "
    "cap shrinks a grab, it never enlarges one",
    "EX-HANG the axis law on the hang: a sideways drag on the work reaches THE WORK and is never "
    "taken for a pan of the browser's own, while an up-and-down drag travels to THE PAGE — and both "
    "still meet the pinch refusal",
]

# ---- EX-PROTECT-RES (INV-56): what the visitor actually carries home -----------------------------
# The rows read the REAL saved file: the harness routes every download into its own throwaway profile
# dir (the idiom test_download_guard pins), so a grab leaves a .jpg on disk that PIL can measure.
SET_PROBE = ("(u)=>{const im=document.querySelector('.exh-frame img.work');"
             "if(!im)return 'no-work';"
             "im.removeAttribute('srcset');im.removeAttribute('sizes');"      # the ladder must not re-pick
             "im.src=u;return 'set';}")
PROBE_STATE = ("(()=>{const im=document.querySelector('.exh-frame img.work');if(!im)return 'null';"
               "return JSON.stringify({w:im.naturalWidth,h:im.naturalHeight,done:!!im.complete,"
               "src:im.currentSrc||im.getAttribute('src')||''});})()")


def wait_for_saved(profile, pattern, timeout=12.0):
    """Poll the throwaway profile dir for the saved gift file (the save is async: load → canvas → blob)."""
    end = time.time() + timeout
    while time.time() < end:
        hits = sorted(f for f in Path(profile).glob(pattern) if not f.name.endswith(".crdownload"))
        if hits:
            return hits[0]
        time.sleep(0.2)
    return None


def grab_probe(br, base, probe):
    """Hang a probe image of a known size on the first work, right-click it, say yes — and return
    (dimensions_of_the_saved_file, detail). None dimensions means no file ever left the browser."""
    name, w, h = probe
    enter(br, base)
    if br.evaluate("(%s)(%s)" % (SET_PROBE, json.dumps("/" + name))) != "set":
        return None, "the probe could not be hung on a work"
    state = {}
    for _ in range(60):
        state = json.loads(br.evaluate(PROBE_STATE) or "null") or {}
        if state.get("done") and state.get("w") == w and state.get("src", "").endswith(name):
            break
        br.sleep(0.1)
    if not (state.get("w") == w and state.get("h") == h):
        return None, f"the probe never became the shown image: {state}"
    br.evaluate("document.querySelector('.exh-frame img.work')"
                ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
    br.sleep(0.5)
    br.click(".gift-yes", settle=0.6)                    # yes → giftDownload → a real file is saved
    saved = wait_for_saved(br._profile, "*" + Path(name).stem + "*")
    if saved is None:
        return None, f"no saved file in the profile dir (shown {w}x{h})"
    with Image.open(saved) as im:
        dims = im.size
    return dims, f"shown={w}x{h} saved={saved.name} dims={dims[0]}x{dims[1]}"

# open the enlarged view by a two-finger pinch on the walk work, then long-press it (contextmenu). On
# Blink — Android Chrome's engine — a picture's native long-press "Save image" menu rides `contextmenu`,
# so proving the zoom's guard prevents it here is the Android proof the iOS callout cannot give.
ZOOM_CTX = (
    "(()=>{const work=document.querySelector('.exh-frame img.work');"
    "if(!work)return JSON.stringify({err:'no-work'});"
    "const r=work.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;"
    "const mk=(id,x,y)=>new Touch({identifier:id,target:work,clientX:x,clientY:y});"
    "const fire=(t,ts)=>work.dispatchEvent(new TouchEvent(t,{touches:ts,targetTouches:ts,"
    "changedTouches:ts,bubbles:true,cancelable:true}));"
    "fire('touchstart',[mk(1,cx-20,cy),mk(2,cx+20,cy)]);"
    "const z=document.getElementById('ex-zoom');const opened=!!z&&!z.hidden;"
    "const zi=document.querySelector('#ex-zoom .exz-img');let prevented=null;"
    "if(zi){const ev=new MouseEvent('contextmenu',{bubbles:true,cancelable:true});"
    "zi.dispatchEvent(ev);prevented=ev.defaultPrevented;}"
    "fire('touchend',[]);"
    "return JSON.stringify({opened:opened,prevented:prevented});})()"
)

TOAST = "(()=>{const t=document.getElementById('ex-toast');return t&&!t.hidden?t.textContent:null;})()"
GIFT = ("(()=>{const g=document.getElementById('ex-gift-card');"
        "return g&&!g.hidden?(g.querySelector('.gift-line')||{}).textContent||'':null;})()")
AT_DOOR = "document.body.classList.contains('ex-door')"
FRAME_IDS = "Array.from(document.querySelectorAll('.exh-frame')).map(f=>f.dataset.id)"


# ---- EX-HANG's axis reading, driven by a real finger ---------------------------------------------
# The phone frame the hang's axis law is read on: one work fills the frame, which is the shape
# Requirement 38's case "Where the axis law reaches" says the law binds.
VW_TOUCH, VH_TOUCH = 390, 844

# The counter is hung at the WINDOW in capture, the same place and the same passive way the walk's
# own normalised hand signal listens, so what it counts is what the signal would have received.
COUNT_POINTERS = """
  window.__axis = {moves: 0, cancel: 0, up: 0};
  ['pointermove', 'pointercancel', 'pointerup'].forEach(function (t) {
    addEventListener(t, function () {
      window.__axis[t === 'pointermove' ? 'moves' : t === 'pointercancel' ? 'cancel' : 'up'] += 1;
    }, {capture: true, passive: true});
  });
  return true;
"""


def work_centre(br):
    box = br.evaluate("(()=>{const w=document.querySelector('.exh-frame img.work');if(!w)return '';"
                      "const r=w.getBoundingClientRect();"
                      "return JSON.stringify({x:r.left+r.width/2,y:r.top+r.height/2});})()")
    return json.loads(box) if box else None


def drag_on_work(br, dx, dy, steps=8):
    """One finger, laid on the photograph and drawn `steps` times by (dx, dy). Hands back how many
    pointer moves the page received and whether the browser took the gesture away mid-drag."""
    br.evaluate("(function(){%s})()" % COUNT_POINTERS.replace("return true;", ""))
    at = work_centre(br)
    if not at:
        return {"moves": 0, "cancel": 0, "up": 0}
    x, y = at["x"], at["y"]
    br._cmd("Input.dispatchTouchEvent", type="touchStart", touchPoints=[{"x": x, "y": y}])
    for i in range(1, steps + 1):
        br._cmd("Input.dispatchTouchEvent", type="touchMove",
                touchPoints=[{"x": x + dx * i, "y": y + dy * i}])
        br.sleep(0.03)
    br._cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])
    br.sleep(0.4)
    return json.loads(br.evaluate("JSON.stringify(window.__axis)"))


def pinch_scale(br):
    """Two fingers spread apart on the photograph, and the viewport's own scale afterwards. The
    refusal INV-49 was written for is this number staying at 1."""
    at = work_centre(br)
    if not at:
        return 1.0
    x, y = at["x"], at["y"]
    br._cmd("Input.dispatchTouchEvent", type="touchStart",
            touchPoints=[{"x": x - 30, "y": y, "id": 1}, {"x": x + 30, "y": y, "id": 2}])
    for i in range(1, 9):
        br._cmd("Input.dispatchTouchEvent", type="touchMove",
                touchPoints=[{"x": x - 30 - i * 12, "y": y, "id": 1},
                             {"x": x + 30 + i * 12, "y": y, "id": 2}])
        br.sleep(0.03)
    br._cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])
    br.sleep(0.5)
    return float(br.evaluate("String((window.visualViewport && window.visualViewport.scale) || 1)"))


def enter(br, base):
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("localStorage.setItem('ex-tempo','0.5')")  # toast lives 1.5s — enough to check
    br.reload()
    br.sleep(0.8)
    br.click(".exd-window:nth-child(1)", settle=0.1)
    br.sleep(1.2)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # 0 · desktop right-click OPENS THE GIFT CEREMONY (offered, never dumped) — EX-PROTECT-GIFT
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            gift = br.evaluate(GIFT)
            # the gift card must be visible with a non-empty gift line
            check(BROWSER_ROWS[0],
                  gift is not None and len(gift.strip()) > 0,
                  f"gift_line={gift!r}")

        # 1 · drag on a work is prevented (dragstart fires toast, no drag ghost)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new DragEvent('dragstart',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            toast = br.evaluate(TOAST)
            check(BROWSER_ROWS[1],
                  toast is not None and len(toast.strip()) > 0,
                  f"toast={toast!r}")

        # 2 · the gift ceremony line carries the site host (stripped of protocol)
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            br.evaluate("document.querySelector('.exh-frame img.work')"
                        ".dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}))")
            br.sleep(0.4)
            gift = br.evaluate(GIFT) or ""
            # site host = hostname from SITE_URL without protocol
            host = SITE_URL.replace("https://", "").replace("http://", "")
            check(BROWSER_ROWS[2],
                  host in gift,
                  f"gift_line={gift!r} want host={host!r}")

        # 3 · right-click on a share button is NOT intercepted
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            # contextmenu on the share button must not produce the enjoy toast
            br.evaluate("(()=>{const b=document.querySelector('.ex-share');"
                        "if(b)b.dispatchEvent(new MouseEvent('contextmenu',{bubbles:true,cancelable:true}));})()")
            br.sleep(0.4)
            toast = br.evaluate(TOAST)
            check(BROWSER_ROWS[3],
                  toast is None,
                  f"toast={toast!r} (should be None — chrome is not protected)")

        # 4 · the enlarged view refuses a raw save on Blink (Android's engine) — the contextmenu road
        import json as _json
        with Browser(width=1280, height=900) as br:
            enter(br, base)
            zc = _json.loads(br.evaluate(ZOOM_CTX) or "{}")
            br.sleep(0.3)
            toast = br.evaluate(TOAST)
            check(BROWSER_ROWS[4],
                  zc.get("opened") is True and zc.get("prevented") is True
                  and toast is not None and len(str(toast).strip()) > 0,
                  f"zoom_open={zc.get('opened')} contextmenu_prevented={zc.get('prevented')} toast={toast!r}")

        # 5 · the carry-home cap: a work shown at 1600x1000 is saved at 800x500 (the long edge lands
        #     exactly on the cap, the shape is kept), so the quiz prize stays the larger picture
        with Browser(width=1280, height=900) as br:
            dims, detail = grab_probe(br, base, PROBE_OVER)
            check(BROWSER_ROWS[5],
                  dims == (800, 500),
                  detail)

        # 6 · the cap only ever shrinks: a work shown at 320x200 is saved at 320x200, not stretched
        with Browser(width=1280, height=900) as br:
            dims, detail = grab_probe(br, base, PROBE_UNDER)
            check(BROWSER_ROWS[6],
                  dims == (320, 200),
                  detail)

        # 7 · EX-HANG's axis reading, driven by real touch (2026-09-03, plan row S-79) ------------
        #
        # WHAT THIS MEASURES, AND WHY IT IS NOT A STYLE READ. `getComputedStyle` would answer
        # `pan-y` off the declaration the CSS row above already holds, and prove nothing about what
        # the browser then DOES with a finger. What the law is about is who receives a sideways drag
        # on a photograph, and the browser answers that by taking the gesture or by leaving it:
        #
        #   · it takes it — the drag matches an axis the element yielded — and two moves in it fires
        #     `pointercancel` and delivers nothing further. The walk's normalised hand signal
        #     (`passInteraction`, exhibition.js) reads `pointermove`, so a cancelled pointer is a
        #     making axis that reaches no instrument. This is what `pan-x pan-y` did.
        #   · it leaves it — the drag crosses no axis the element yielded — and every `pointermove`
        #     of the run arrives, closed by `pointerup`. This is the horizontal the work now owns.
        #
        # The three legs are one visit each, because a drag changes where the page stands.
        with Browser(width=VW_TOUCH, height=VH_TOUCH) as br:
            enter(br, base)
            br.touch(True, 2)
            side = drag_on_work(br, dx=-18, dy=0)
            enter(br, base)
            br.touch(True, 2)
            before_y = float(br.evaluate("String(window.scrollY)"))
            down = drag_on_work(br, dx=0, dy=-18)
            after_y = float(br.evaluate("String(window.scrollY)"))
            enter(br, base)
            br.touch(True, 2)
            scale = pinch_scale(br)
            check(BROWSER_ROWS[7],
                  # the work's horizontal: every move of the run lands on the work, uncancelled
                  side["moves"] >= 5 and side["cancel"] == 0
                  # the page's vertical: the drag travels the walk between works — the door axis,
                  # exactly as before. What carries it is the walk's own paginated swipe rather
                  # than a browser pan, which is why the read is the travel and not a cancelled
                  # pointer: a work's height is what one such drag is worth.
                  and after_y > before_y + VH_TOUCH * 0.5
                  # and the pinch the whole declaration was written for is still refused
                  and abs(scale - 1.0) < 0.01,
                  "sideways on the work: %d pointermove(s), %d pointercancel(s) — the work %s the "
                  "making axis. Up-and-down: the page travelled %.0f px of a %d px work (%d "
                  "pointercancel(s)) — the page %s the door axis. A two-finger spread left the "
                  "viewport at scale %.3f."
                  % (side["moves"], side["cancel"],
                     "owns" if side["cancel"] == 0 else "never receives",
                     after_y - before_y, VH_TOUCH, down["cancel"],
                     "owns" if after_y > before_y + VH_TOUCH * 0.5 else "does not own", scale))

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
