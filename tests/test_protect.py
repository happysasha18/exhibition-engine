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


TMP = Path(tempfile.mkdtemp(prefix="synth_protect_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# ---------------------------------------------------------------- data rows

def zoom_layer_slice(js):
    """The assembled client is one concatenation with no fragment markers, so the zoom layer's own
    region is located by two anchors it alone carries. A missing anchor is a FAILURE of the check
    itself, never a quiet pass — a gate's verdict is worthless without its reach."""
    a = js.find("a pinch over the OPEN zoom scales the picture")
    b = js.find("Every way out is the same road")
    if a < 0 or b < 0 or b <= a:
        return None
    return js[a:b]

# 1 · the `enjoy` string is present in the greetings cache and the worker schema
greet = json.loads((TMP / "exhibition_data.json").read_text()).get("greet") or {}
langs = greet.get("langs") or {}
missing_enjoy = [c for c, L in langs.items() if not (L.get("enjoy") or "").strip()]
worker_src = (ROOT / "engine" / "assets" / "worker.js").read_text(encoding="utf-8")
enjoy_in_schema = '"enjoy"' in worker_src and "enjoy" in worker_src
check("EX-PROTECT enjoy string in locale cache (all langs) + worker schema includes enjoy",
      not missing_enjoy and enjoy_in_schema,
      f"missing_enjoy={missing_enjoy} schema_has_enjoy={enjoy_in_schema}")

# 2 · CSS: img.work carries the soft-deter properties
css_src = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")
css_ok = ("user-select:none" in css_src
          and "-webkit-user-drag:none" in css_src
          and "-webkit-touch-callout:none" in css_src
          and "touch-action:pan-x pan-y" in css_src)
check("EX-PROTECT CSS: img.work carries user-select/user-drag/touch-callout:none + touch-action:pan-x pan-y",
      css_ok, f"css_src snippet not found (see exhibition.css img.work block)")

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
audit_ok = ("touch-action:pan-xpan-y" in css_src.replace(" ", "")   # body-level class rule kills double-tap too
            and "if (e.ctrlKey) { e.preventDefault(); return; }" in js_src
            and "#ex-sound, .ex-share" in js_src
            and (lambda s: s is not None and "touchcancel" in s)(zoom_layer_slice(js_src))
            and "re-take the gesture" in js_src)
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
]

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

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)-len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
