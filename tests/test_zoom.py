#!/usr/bin/env python3
"""EX-ZOOM (INV-75 base, INV-76 pan): pinch a picture to inspect it in its own zoom layer;
once enlarged past 1x, a one-finger drag pans it, bounded to the picture's visible overflow.

A two-finger pinch on ANY exhibition picture — a work on the walk, a door window, a side-room
print — opens that picture enlarged over the page; the image scales under the pinch (OUR JS, so
the browser never viewport-zooms), and a x/backdrop/Esc returns with the page beneath exactly as
it was (a face). The browser rows drive a REAL headless Chrome with synthetic touch events;
Chrome absent -> pinned expected SKIPs. Run: python tests/test_zoom.py
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


TMP = Path(tempfile.mkdtemp(prefix="synth_zoom_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
CSS = (TMP / "exhibition.css").read_text(encoding="utf-8")
DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
# a polaroid-table series (any non-lane series lays its members as small prints) — its first member
# is the walk pick that brings the series pill into the caption (INV-81's small-target case)
_POLA_SERIES = next((s for s in (DATA.get("series") or []) if s.get("variant") != "lane"), None)
POLA_PICK = _POLA_SERIES["members"][0] if _POLA_SERIES else None

# ---------------------------------------------------------------- string rows
js_bits = {
    "the zoom layer is created (#ex-zoom)": 'zoom.id = "ex-zoom"' in JS,
    "openZoom + closeZoom": "function openZoom(" in JS and "function closeZoom(" in JS,
    "the pinch trigger over the picture selectors":
        "ZOOM_SEL" in JS and "img.work" in JS and "exd-window img" in JS and "#ex-side img" in JS,
    "our own scale (two-touch distance -> scale, clamped)": "zDist(" in JS and "Math.min(4" in JS,
    "the zoom is a face (faceStands carries zoomOpen)":
        bool(re.search(r"faceStands\(\)\s*\{\s*return[^}]*zoomOpen", JS)),
    "close by x, backdrop, Esc":
        "exz-close" in JS and 'e.key === "Escape" && zoomOpen' in JS,
}
check("EX-ZOOM the pinch-to-inspect layer is built into the client "
      "(overlay + trigger + our own scale + face lock + close)",
      all(js_bits.values()), "missing: " + ", ".join(k for k, v in js_bits.items() if not v))
check("EX-ZOOM the layer refuses the browser's own gesture on itself (touch-action:none)",
      bool(re.search(r"#ex-zoom\s*\{[^}]*touch-action:\s*none", CSS.replace("\n", " "))),
      "no touch-action:none on #ex-zoom")

js_pan_bits = {
    "zClampPan bounds the offset to the visible overflow": "function zClampPan(" in JS,
    "zPanning tracks a one-finger drag on the enlarged picture": "zPanning" in JS,
    "zTx/zTy hold the pan offset, applied via zApply's translate": "zTx" in JS and "zTy" in JS and "function zApply(" in JS,
}
check("EX-ZOOM/INV-76 the pan machinery is built into the client (zClampPan + zPanning + zTx/zTy)",
      all(js_pan_bits.values()), "missing: " + ", ".join(k for k, v in js_pan_bits.items() if not v))
check("EX-ZOOM/INV-77 the zoom carries its own chrome — a close + a share of the inspected work",
      "exz-close" in JS and "exz-share" in JS
      and "shareBtn.dataset.share" in JS and "html.ex-cover" not in CSS,
      "zoom chrome/share not built, or the old ex-cover hide is still present")
check("EX-ZOOM/INV-77 nothing moves: the close is top-left, the share on the walk's own bottom-right rail (css)",
      bool(re.search(r"#ex-zoom \.exz-close\s*\{[^}]*left:", CSS.replace("\n", " ")))
      and bool(re.search(r"#ex-zoom \.exz-share\s*\{[^}]*right:\s*calc\(var\(--ex-rail\)", CSS.replace("\n", " ")))
      and "#ex-zoom .exz-btn" in CSS,
      "close not top-left or share not on the --ex-rail bottom-right")
# INV-81: the trigger's reach + the direct scale (the polaroid small-target case)
inv81_bits = {
    "ZOOM_SEL carries the whole polaroid print (.exs-print)":
        "ZOOM_SEL" in JS and ".exs-print" in JS.split("ZOOM_SEL", 1)[1][:260],
    "either finger anchors the match (the element under each touch point is read)":
        "elementFromPoint" in JS,
    "the zoom's pinch/pan handlers listen at the DOCUMENT, gated on zoomOpen":
        "if (!zoomOpen) return" in JS and 'zoom.addEventListener("touchmove"' not in JS,
    "the opening gesture is seeded so the SAME pinch keeps scaling (no arming tap)":
        "zPinch = zDist(e.touches); zStartS = 1" in JS,
}
check("EX-ZOOM/INV-81 the trigger's reach + the direct scale are built into the client "
      "(print hit-area + either-finger read + document-level gated handlers + gesture seed)",
      all(inv81_bits.values()),
      "missing: " + ", ".join(k for k, v in inv81_bits.items() if not v))

# ---------------------------------------------------------------- browser rows
BROWSER_ROWS = [
    "EX-ZOOM a two-finger pinch on a door window opens the zoom over the frozen page",
    "EX-ZOOM the x returns to the untouched page (the zoom closes)",
    "EX-ZOOM a two-finger pinch on a walk work opens the zoom too",
]
PAN_ROWS = [
    "EX-ZOOM/INV-76 a one-finger drag on a zoomed picture pans it by the drag",
    "EX-ZOOM/INV-76 the pan is bounded to the picture's edge (a huge drag clamps, image never flies off)",
]
COVER_ROWS = [
    "EX-ZOOM/INV-77 with the zoom open the player (if present) stays reachable, not overlapped by the close",
    "EX-ZOOM/INV-77 the zoom offers a share of the inspected work (bottom-right, the walk's own corner)",
]
POLAROID_ROWS = [
    "EX-ZOOM/INV-81 a pinch with ONE finger on a polaroid print opens the zoom with that photograph "
    "(no arming tap) — and a bare-table pinch opens nothing",
    "EX-ZOOM/INV-81 the opening pinch scales the picture DIRECTLY (the same gesture, no second pinch)",
    "EX-ZOOM/INV-76/INV-81 a polaroid-opened zoom pans like a gallery one, and its close returns the "
    "standing room with the lift intact",
]
# a two-finger touchstart whose EVENT lands on the bare table: first both fingers bare (must open
# nothing), then one finger over the first print (must open THAT photograph) — the small-target law
SPLIT = (
    "(()=>{const p=document.querySelector('.exs-print'),st=document.getElementById('exs-stage'),"
    "z=document.getElementById('ex-zoom');if(!p||!st)return JSON.stringify({err:'no-print'});"
    "const img=p.querySelector('img'),r=img.getBoundingClientRect();"
    "const x1=r.left+r.width/2,y1=r.top+r.height/2;"
    "const bare=(x,y)=>{const el=document.elementFromPoint(x,y);"
    "return el&&(!el.closest||!el.closest('.exs-print,.exs-back'));};"
    "let x2=0,y2=0;"
    "for(const cy of [innerHeight-30,innerHeight-80,Math.round(innerHeight*0.5)]){"
    "for(const cx of [innerWidth-30,30,Math.round(innerWidth*0.5)]){"
    "if(bare(cx,cy)&&bare(cx-26,cy)){x2=cx;y2=cy;break;}}if(x2)break;}"
    "if(!x2)return JSON.stringify({err:'no-bare-point'});"
    "const tgt=document.elementFromPoint(x2,y2)||st;"
    "const mk=(id,x,y)=>new Touch({identifier:id,target:tgt,clientX:x,clientY:y});"
    "const start=(ts)=>tgt.dispatchEvent(new TouchEvent('touchstart',{touches:ts,targetTouches:ts,"
    "changedTouches:ts,bubbles:true,cancelable:true}));"
    "const end=()=>document.dispatchEvent(new TouchEvent('touchend',{touches:[],targetTouches:[],"
    "changedTouches:[],bubbles:true}));"
    "start([mk(1,x2,y2),mk(2,x2-26,y2)]);const bareOpened=!!z&&!z.hidden;end();"
    "start([mk(1,x1,y1),mk(2,x2,y2)]);const opened=!!z&&!z.hidden;"
    "const zi=document.querySelector('#ex-zoom .exz-img');"
    "const norm=(u)=>{try{return new URL(u,location.href).href}catch(e){return u}};"
    "const zsrc=zi?(zi.getAttribute('src')||''):'';end();"
    "return JSON.stringify({bare:bareOpened,opened:opened,"
    "match:!!zsrc&&norm(zsrc)===norm(img.getAttribute('src')||'')});})()"
)
# the SAME gesture that opens the layer keeps scaling it: touchstart on the print's own photograph
# (two fingers 40px apart) then a widening touchmove of that gesture — the zoomed image must grow
DIRECT = (
    "(()=>{const img=document.querySelector('.exs-print img');"
    "if(!img)return JSON.stringify({err:'no-img'});"
    "const z=document.getElementById('ex-zoom');"
    "const r=img.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;"
    "const mk=(id,x,y)=>new Touch({identifier:id,target:img,clientX:x,clientY:y});"
    "const fire=(t,ts)=>img.dispatchEvent(new TouchEvent(t,{touches:ts,targetTouches:ts,"
    "changedTouches:ts,bubbles:true,cancelable:true}));"
    "fire('touchstart',[mk(1,cx-20,cy),mk(2,cx+20,cy)]);"
    "fire('touchmove',[mk(1,cx-60,cy),mk(2,cx+60,cy)]);"
    "const zi=document.querySelector('#ex-zoom .exz-img');"
    "const m=/scale\\(([0-9.]+)\\)/.exec(zi?zi.style.transform:'')||[];"
    "fire('touchend',[]);"
    "return JSON.stringify({opened:!!z&&!z.hidden,scale:m[1]?parseFloat(m[1]):null});})()"
)
SIDE_ON = "(()=>{const s=document.getElementById('ex-side');return !!s&&!s.hidden})()"
LIFTED = "(()=>{const p=document.querySelector('.exs-print');return !!p&&p.classList.contains('lift')})()"
# with the zoom open: if a player exists, is it still displayed and clear of the zoom's close?
OVERLAP = ("(()=>{const s=document.getElementById('ex-sound'),x=document.querySelector('#ex-zoom .exz-close');"
           "if(!x)return JSON.stringify({no:1});if(!s)return JSON.stringify({noplayer:1});"
           "const a=s.getBoundingClientRect(),b=x.getBoundingClientRect(),c=getComputedStyle(s);"
           "const over=!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top);"
           "return JSON.stringify({over,disp:c.display,pe:c.pointerEvents});})()")
# is the zoom's share present and offered when there is an in-view work?
ZSHARE = ("(()=>{const x=document.querySelector('#ex-zoom .exz-share');"
          "if(!x)return JSON.stringify({no:1});return JSON.stringify({present:true,hidden:x.hidden});})()")
# scale the open zoom to ~3x via a two-finger pinch, then drag one finger by (dx,dy); return the
# resulting inline translate + scale and the layout metrics needed to compute the bound.
PAN = (
    "(dx,dy)=>{const img=document.querySelector('#ex-zoom .exz-img');"
    "if(!img)return JSON.stringify({err:'no-img'});"
    "const mk=(id,x,y)=>new Touch({identifier:id,target:img,clientX:x,clientY:y});"
    "const fire=(t,ts)=>img.dispatchEvent(new TouchEvent(t,{touches:ts,targetTouches:ts,"
    "changedTouches:ts,bubbles:true,cancelable:true}));"
    "fire('touchstart',[mk(1,120,200),mk(2,210,270)]);"          # start pinch, dist ~114
    "fire('touchmove',[mk(1,60,200),mk(2,402,200)]);"            # dist 342 -> scale clamps to 3
    "fire('touchend',[]);"
    "fire('touchstart',[mk(1,195,420)]);"                        # one finger on the enlarged picture
    "fire('touchmove',[mk(1,195+dx,420+dy)]);"
    "const tr=img.style.transform;fire('touchend',[]);"
    "const m=/translate\\(([-0-9.]+)px,\\s*([-0-9.]+)px\\)\\s*scale\\(([0-9.]+)\\)/.exec(tr)||[];"
    "return JSON.stringify({tx:parseFloat(m[1]),ty:parseFloat(m[2]),scale:parseFloat(m[3]),"
    "ow:img.offsetWidth,iw:window.innerWidth});}"
)
PINCH = (
    "(sel)=>{const el=document.querySelector(sel);if(!el)return 'no-el';"
    "try{const t1=new Touch({identifier:1,target:el,clientX:120,clientY:200});"
    "const t2=new Touch({identifier:2,target:el,clientX:210,clientY:270});"
    "const ev=new TouchEvent('touchstart',{touches:[t1,t2],targetTouches:[t1,t2],"
    "changedTouches:[t1,t2],bubbles:true,cancelable:true});"
    "el.dispatchEvent(ev);return 'ok';}catch(e){return 'err:'+e.message;}}"
)
ZOPEN = ("(()=>{const z=document.getElementById('ex-zoom');"
         "return !!z&&!z.hidden&&z.classList.contains('show');})()")
ZSRC = ("(()=>{const i=document.querySelector('#ex-zoom .exz-img');"
        "return i?(i.getAttribute('src')||''):'';})()")
FACE = "document.documentElement.classList.contains('ex-face')"



def _boot(br, base):
    br.navigate(base + "/")
    br.clear_storage()
    br.evaluate("localStorage.setItem('ex-tempo','0.05')")
    br.reload(); br.sleep(1.1)


if not chrome_available():
    for r in BROWSER_ROWS + PAN_ROWS + COVER_ROWS + POLAROID_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=390, height=844) as br:       # phone
            _boot(br, base)
            fired = br.evaluate("(%s)('.exd-window img')" % PINCH)  # pinch a DOOR window
            br.sleep(0.2)
            opened = br.evaluate(ZOPEN)
            src = br.evaluate(ZSRC) or ""
            face = br.evaluate(FACE)
            check(BROWSER_ROWS[0], fired == "ok" and opened and len(src) > 0 and face,
                  f"fired={fired!r} opened={opened} src_len={len(src)} face={face}")
            br.evaluate("var b=document.querySelector('#ex-zoom .exz-close'); if(b) b.click();")
            br.sleep(0.3)
            closed = not br.evaluate(ZOPEN)
            check(BROWSER_ROWS[1], closed, f"closed={closed}")
        with Browser(width=390, height=844) as br:       # a WALK work
            _boot(br, base)
            br.click(".exd-window:nth-child(1)", settle=0.6)
            br.sleep(0.6)
            # make sure there is an in-view work to share (the observer sets this on the walk)
            br.evaluate("var s=document.getElementById('ex-share'); if(s){s.dataset.share='999';}")
            fired2 = br.evaluate("(%s)('.exh-frame img.work')" % PINCH)
            br.sleep(0.2)
            opened2 = br.evaluate(ZOPEN)
            check(BROWSER_ROWS[2], fired2 == "ok" and opened2,
                  f"fired={fired2!r} opened={opened2}")
            # INV-77: no cover-hide anymore — the player (if the fixture has one) stays reachable and the
            # zoom's close does NOT overlap it. The synthetic fixture configures no audio, so #ex-sound may
            # be absent; then this row asserts only that the zoom's close exists (the instance suite, with a
            # real player, proves the no-overlap on a live #ex-sound).
            ov = json.loads(br.evaluate(OVERLAP))
            check(COVER_ROWS[0],
                  opened2 and not ov.get("no")
                  and (ov.get("noplayer") == 1 or (ov.get("over") is False
                                                   and ov.get("disp") != "none" and ov.get("pe") != "none")),
                  f"overlap={ov}")
            # the zoom offers its own share of the inspected work, top-left
            zs = json.loads(br.evaluate(ZSHARE))
            check(COVER_ROWS[1],
                  opened2 and zs.get("present") and zs.get("hidden") is False,
                  f"zshare={zs}")
        with Browser(width=390, height=844) as br:       # INV-76: drag-to-pan a zoomed picture
            _boot(br, base)
            # the synthetic fixture's placeholder images are tiny (64x64) — far smaller than a real
            # photo, which is always wider than the zoom layer's max-width cap and so already fills
            # it at scale 1. Pin .exz-img's rendered box to that cap so the pinch-to-3x scale produces
            # the SAME real overflow a full-size photo would (the pan math itself, zClampPan/zApply,
            # is untouched — this only compensates for the fixture's undersized asset).
            br.evaluate(
                "(()=>{const st=document.createElement('style');"
                "st.textContent='#ex-zoom .exz-img{width:340px!important;height:340px!important;"
                "object-fit:cover!important;}';document.head.appendChild(st);})()")

            def pan_once(dx):
                br.evaluate("(%s)('.exd-window img')" % PINCH)   # open the zoom (scale resets to 1)
                br.sleep(0.2)
                out = json.loads(br.evaluate("(%s)(%d,0)" % (PAN, dx)))
                br.evaluate("var b=document.querySelector('#ex-zoom .exz-close'); if(b) b.click();")
                br.sleep(0.3)
                return out

            mod = pan_once(60)                           # a moderate drag
            big = pan_once(99999)                        # a drag far past the edge

            def _num(d, k):                              # None on no-pan code (transform has no translate)
                v = d.get(k)
                return float(v) if isinstance(v, (int, float)) else None

            # expected offset = min(drag, overflow); the pan follows the finger, clamped to the edge
            mtx, mty, msc, mow, miw = (_num(mod, "tx"), _num(mod, "ty"), _num(mod, "scale"),
                                       _num(mod, "ow"), _num(mod, "iw"))
            ox_mod = max(0.0, (mow * msc - miw) / 2) if None not in (mow, msc, miw) else 0.0
            mod_ok = (None not in (mtx, mty, msc, mow, miw) and msc > 2 and abs(mty) <= 2
                      and abs(mtx - min(60.0, ox_mod)) <= 3)
            check(PAN_ROWS[0], mod_ok,
                  f"tx={mtx} expected~{round(min(60.0, ox_mod),1)} scale={msc} ty={mty}")
            btx, bsc, bow, biw = (_num(big, "tx"), _num(big, "scale"), _num(big, "ow"), _num(big, "iw"))
            ox_big = max(0.0, (bow * bsc - biw) / 2) if None not in (bow, bsc, biw) else 0.0
            big_ok = (None not in (btx, bsc, bow, biw) and bsc > 2 and ox_big > 0
                      and btx < 99999 and abs(btx - ox_big) <= 3)
            check(PAN_ROWS[1], big_ok,
                  f"tx={btx} clamped_to~{round(ox_big,1)} (raw drag was 99999) scale={bsc}")

        if POLA_PICK is None:
            for r in POLAROID_ROWS:
                skip(r, "no polaroid-table series in the synthetic fixture")
        else:
            with Browser(width=390, height=844) as br:       # INV-81: the polaroid table
                # boot onto the walk with a polaroid-series member in view, open the side room
                br.navigate(base + "/")
                br.evaluate("localStorage.clear();sessionStorage.clear()")
                br.evaluate("localStorage.setItem('ex-tempo','0.05')")
                br.evaluate("localStorage.setItem('ex.exhibition', JSON.stringify({v:%s, pick:%s, shown:10}))"
                            % (json.dumps(VER), json.dumps(str(POLA_PICK))))
                br.reload(); br.sleep(1.2)
                br.evaluate(
                    "(()=>{const f=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                    "if(f)f.scrollIntoView({behavior:'instant'});})()" % str(POLA_PICK))
                br.sleep(0.5)
                try:
                    br.click("#exh-cap .ex-series", settle=0.8)
                except RuntimeError:
                    pass
                br.sleep(0.5)
                room = br.evaluate(SIDE_ON)
                # 1 · a bare-table pinch opens nothing; ONE finger on the print opens THAT photograph
                split = json.loads(br.evaluate(SPLIT)) if room else {"err": "room never opened"}
                check(POLAROID_ROWS[0],
                      room and split.get("bare") is False and split.get("opened") is True
                      and split.get("match") is True,
                      f"room={room} split={split}")
                br.evaluate("var b=document.querySelector('#ex-zoom .exz-close'); if(b) b.click();")
                br.sleep(0.3)
                # 2 · the SAME gesture scales directly — no second pinch, no arming tap
                direct = json.loads(br.evaluate(DIRECT)) if room else {"err": "room never opened"}
                check(POLAROID_ROWS[1],
                      direct.get("opened") is True
                      and isinstance(direct.get("scale"), (int, float)) and direct["scale"] > 1.5,
                      f"direct={direct}")
                br.evaluate("var b=document.querySelector('#ex-zoom .exz-close'); if(b) b.click();")
                br.sleep(0.3)
                # 3 · lift a print, pinch it open, PAN it (the gallery's own machinery), close →
                #     the room still stands, the lift intact (the face law — composition)
                if room:
                    br.evaluate("document.querySelector('.exs-print').click()")
                    br.sleep(0.4)
                lifted0 = br.evaluate(LIFTED) if room else False
                if room:
                    br.evaluate("(%s)('.exs-print img')" % PINCH)
                    br.sleep(0.2)
                pol = json.loads(br.evaluate("(%s)(%d,0)" % (PAN, 60))) if room else {}
                br.evaluate("var b=document.querySelector('#ex-zoom .exz-close'); if(b) b.click();")
                br.sleep(0.4)
                room_after = br.evaluate(SIDE_ON)
                lift_after = br.evaluate(LIFTED)
                zoom_gone = not br.evaluate(ZOPEN)
                ptx, psc, pow_, piw = (_num(pol, "tx"), _num(pol, "scale"),
                                       _num(pol, "ow"), _num(pol, "iw"))
                ox_pol = max(0.0, (pow_ * psc - piw) / 2) if None not in (pow_, psc, piw) else 0.0
                pan_ok = (None not in (ptx, psc, pow_, piw) and psc > 2
                          and abs(ptx - min(60.0, ox_pol)) <= 3)
                check(POLAROID_ROWS[2],
                      lifted0 and pan_ok and zoom_gone and room_after and lift_after,
                      f"lifted0={lifted0} pan={pol} zoom_gone={zoom_gone} "
                      f"room_after={room_after} lift_after={lift_after}")

shutil.rmtree(TMP, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
