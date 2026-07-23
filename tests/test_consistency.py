#!/usr/bin/env python3
"""EX-CONSISTENCY: cross-cutting parity that no single feature suite owns —
  A. the walk-pager PLATFORM PARITY (EX-GLIDE / INV-39): window.EXMotion must install BOTH the
     touch pager and the wheel pager on a hybrid device (touch AND hover), and only its own pager
     on a pure-touch or pure-desktop device.
  B. the EX-BUSY ring (INV-48) shared by chrome controls: present on the sound button, shows while
     the player is loading, holds static (no spin) under reduced motion.
  C. the FOCUS/TAP policy (his blue-ring bug): the iOS tap-highlight is transparent on chrome
     controls (the sound button, the language chip) — never the platform's default blue flash.
  D. the EX-SKEL picture skeleton: animates by default, stands still under reduced motion.
Run: python tests/test_consistency.py
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


def is_transparent(color):
    """True if a getComputedStyle color string reads as fully transparent — either the literal
    keyword or an rgba(...) with alpha 0 (the exact channel values are not the point; the alpha is)."""
    if not color:
        return False
    if color.strip() == "transparent":
        return True
    m = re.search(r"rgba?\(([^)]+)\)", color)
    if not m:
        return False
    parts = [p.strip() for p in m.group(1).split(",")]
    if len(parts) != 4:
        return False
    try:
        return float(parts[3]) == 0
    except ValueError:
        return False


# ---------------------------------------------------------------- bake (default, no sound configured)
TMP = Path(tempfile.mkdtemp(prefix="synth_consistency_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# ---------------------------------------------------------------- bake with sound configured (the busy
# ring + tap-highlight rows need the sound player mounted — patch config.json exactly as test_sound.py does)
TMP_SND = Path(tempfile.mkdtemp(prefix="synth_consistency_snd_"))
build_site.OUT = TMP_SND
build_site.build(SITE_URL)
_cfg_path = TMP_SND / "config.json"
_cfg = json.loads(_cfg_path.read_text())
_cfg["exhibition"]["sound_url"] = "/audio/ambient.m4a"
_cfg["exhibition"]["sound_credit"] = {
    "artist": "Synth Artist",
    "title": "Test Track",
    "url": "https://synth.example.com",
}
_cfg_path.write_text(json.dumps(_cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-MOTION hybrid (touch+hover) installs BOTH the touch pager and the wheel pager",
    "EX-MOTION pure touch (coarse, no hover) installs only the touch pager",
    "EX-MOTION desktop (fine pointer, hover) installs only the wheel pager",
    "EX-BUSY the sound button carries a .ex-busy-ring element",
    "EX-BUSY the ring shows (opacity>0.5) while the player is loading",
    "EX-BUSY reduced motion holds the ring static (no spin/fill animation on the circle)",
    "EX-FOCUS the sound button's iOS tap-highlight is transparent",
    "EX-FOCUS the language chip's iOS tap-highlight is transparent",
    "EX-SKEL the picture skeleton animates by default",
    "EX-SKEL the picture skeleton stands still under reduced motion",
    # E. touch-behaviour parity (his 2026-07-23): a finger never hover-reveals, never sticks a tan
    #    fill, and a playing loop rides a walk swipe.
    "EX-SOUND the tray HOVER reveal is gated to @media(hover:hover) — a finger cannot hover-open it",
    "EX-SOUND the tray reveal on .playing / :focus-within is unconditional (touch opens it by playing)",
    "EX-SOUND adding .playing reveals the credit tray (first tap starts → tray opens)",
    "EX-SOUND a PLAYING player rides a walk crossing (opacity 1 under body.ex-crossing)",
    "EX-SOUND a SILENT player still retracts on a walk crossing (opacity 0, loading frame stands alone)",
    "EX-FOCUS the exit accent fill is HOVER-gated, its focus-visible fill unconditional (keyboard keeps the mark)",
    "EX-FOCUS the share accent fill is HOVER-gated (a finger tap leaves no sticky tan circle)",
    # touch-press feedback (his 2026-07-23): a finger gets the response a mouse gets from hover — a
    #    press lights the control's engaged affordance for the touch's duration, cleared on lift.
    "EX-CHROME a coarse-pointer press adds .ex-press to a chrome control and a lift clears it (the touch response the hover-gating withholds from a finger)",
    "EX-CHROME every chrome control carries a .ex-press engaged-fill rule under @media(hover:none) (a mouse keeps its own hover fill)",
]

SND_OP = ("(()=>{const e=document.getElementById('ex-sound');"
          "return e?getComputedStyle(e).opacity:null;})()")


def enter_walk(br):
    """Leave the cold door for the walk — the sound player + its chrome controls mount there
    (same shape as test_sound.py's helper: advance the door window, then poll off-door + arrived)."""
    if br.evaluate("!!document.querySelector('.exd-window')"):
        br.click(".exd-window:nth-child(1)", settle=1.0)
    for _ in range(30):
        if (not br.evaluate("document.body.classList.contains('ex-door')")
                and br.evaluate(SND_OP) == "1"):
            break
        br.sleep(0.1)


def read_motion(br):
    """window.EXMotion is set at script load (module top-level, from media queries at boot);
    poll briefly for it to appear rather than assume it beat the first evaluate()."""
    m = None
    for _ in range(20):
        m = br.evaluate("window.EXMotion || null")
        if m:
            return m
        br.sleep(0.1)
    return m


SKEL_PROBE_JS = """(()=>{document.body.insertAdjacentHTML('beforeend','<div class="ex-skel" id="skelprobe" style="width:20px;height:20px"></div>');const r=getComputedStyle(document.getElementById('skelprobe')).animationName;document.getElementById('skelprobe').remove();return r;})()"""


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    # ---------------------------------------------------------- Group A: walk-pager PARITY
    # (EX-GLIDE / INV-39) — the headline row: a hybrid must install BOTH pagers.
    with serve(TMP) as base:
        # 1 · HYBRID (touch AND hover, e.g. a Surface) — BOTH pagers install. Headless keeps its
        # desktop media (fine pointer, hover:hover) while we give it a real touch count via
        # navigator.maxTouchPoints — the exact hybrid a Surface reports, and the case the old
        # `hover:none`-only flag silently dropped the touch pager on. (CDP setEmulatedMedia does not
        # move the pointer/hover features in this build, so maxTouchPoints is the honest lever.)
        with Browser(width=1280, height=900) as br:
            br.inject("Object.defineProperty(navigator,'maxTouchPoints',{get:()=>5,configurable:true});")
            br.navigate(base + "/")
            m = read_motion(br)
            check(BROWSER_ROWS[0],
                  bool(m) and m.get("hasTouch") and m.get("hasWheel")
                  and m.get("touchPager") and m.get("wheelPager"),
                  f"EXMotion={m}")

        # 2 · PURE TOUCH (phone) — touch pager only. setTouchEmulationEnabled flips the phone media
        # (coarse pointer, hover:none) AND the touch count, so the wheel pager stands down.
        with Browser(width=1280, height=900) as br:
            br.touch(True, 5)
            br.navigate(base + "/")
            m = read_motion(br)
            check(BROWSER_ROWS[1],
                  bool(m) and m.get("touchPager") and not m.get("wheelPager"),
                  f"EXMotion={m}")

        # 3 · DESKTOP (mouse) — wheel pager only. Headless default is a fine pointer with hover.
        with Browser(width=1280, height=900) as br:
            br.navigate(base + "/")
            m = read_motion(br)
            check(BROWSER_ROWS[2],
                  bool(m) and not m.get("touchPager") and m.get("wheelPager"),
                  f"EXMotion={m}")

    # ---------------------------------------------------------- Group B: the EX-BUSY ring on
    # chrome controls (bake WITH sound configured — the player mounts .exsnd-btn on the walk)
    with serve(TMP_SND) as base2:
        # 4 · the ring element itself
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)
            has_ring = br.evaluate("!!document.querySelector('.exsnd-btn .ex-busy-ring')")
            check(BROWSER_ROWS[3], bool(has_ring), f"has_ring={has_ring}")

        # 5 · the ring shows while the player is loading
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)
            # add the loading state, then let the opacity transition (calc(.3s*tempo)) settle before
            # the read — the ring fades in, it is not instantaneous
            br.evaluate("document.getElementById('ex-sound').classList.add('loading')")
            br.sleep(0.6)
            op = br.evaluate(
                "(()=>{var r=document.querySelector('#ex-sound .ex-busy-ring');"
                "return r?getComputedStyle(r).opacity:null;})()")
            ok = op is not None
            try:
                ok = ok and float(op) > 0.5
            except (TypeError, ValueError):
                ok = False
            check(BROWSER_ROWS[4], ok, f"opacity={op!r}")

        # 6 · reduced motion holds the ring static (no spin/fill animation)
        with Browser(width=1280, height=900) as br:
            br.emulate_media(prefers_reduced_motion="reduce")
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)
            anim = br.evaluate(
                "(()=>{const c=document.querySelector('#ex-sound .ex-busy-ring circle');"
                "return c?getComputedStyle(c).animationName:null;})()")
            check(BROWSER_ROWS[5], anim == "none", f"animationName={anim!r}")

        # ---------------------------------------------------------- Group C: the FOCUS/TAP
        # policy (his blue-ring bug) — the iOS tap-highlight is transparent on chrome controls.
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)

            # 7 · the sound button
            snd_hl = br.evaluate(
                "(()=>{const e=document.querySelector('.exsnd-btn');"
                "return e?getComputedStyle(e).webkitTapHighlightColor:null;})()")
            check(BROWSER_ROWS[6], is_transparent(snd_hl), f"webkitTapHighlightColor={snd_hl!r}")

            # 8 · the language chip (present on every bake — greetings.json is a committed cache)
            chip_hl = br.evaluate(
                "(()=>{const e=document.querySelector('.exl-cur');"
                "return e?getComputedStyle(e).webkitTapHighlightColor:null;})()")
            check(BROWSER_ROWS[7], is_transparent(chip_hl), f"webkitTapHighlightColor={chip_hl!r}")

    # ---------------------------------------------------------- Group D: the picture SKELETON
    # (light proof — a probe element, no series-room navigation needed)
    with serve(TMP) as base3:
        # 9 · animates by default
        with Browser(width=1280, height=900) as br:
            br.navigate(base3 + "/")
            anim = br.evaluate(SKEL_PROBE_JS)
            check(BROWSER_ROWS[8], anim != "none", f"animationName={anim!r}")

        # 10 · static under reduced motion
        with Browser(width=1280, height=900) as br:
            br.emulate_media(prefers_reduced_motion="reduce")
            br.navigate(base3 + "/")
            anim = br.evaluate(SKEL_PROBE_JS)
            check(BROWSER_ROWS[9], anim == "none", f"animationName={anim!r}")

    # ---------------------------------------------------------- Group E: TOUCH-behaviour parity
    # (his 2026-07-23) — a finger never hover-reveals a tray, never sticks a tan fill on a control,
    # and a playing loop rides a walk swipe. The hover-gating is proven STRUCTURALLY over the CSSOM
    # (this build cannot emulate hover:none — see Group A's note), the playing/crossing behaviour by
    # class toggle on the real booted walk.
    RULE_MEDIA = r"""(sel, prop) => {
      // 'hover' if the matching style rule sits under @media(...hover:hover...), 'bare' if
      // unconditional, null if not found. Walks top-level rules and one level of media nesting.
      for (const sheet of document.styleSheets) {
        let top; try { top = sheet.cssRules; } catch (e) { continue; }
        const scan = (list, underHover) => {
          for (const r of list) {
            if (r.type === 1 && r.selectorText && r.selectorText.indexOf(sel) !== -1
                && (!prop || r.cssText.indexOf(prop) !== -1)) return underHover ? 'hover' : 'bare';
            if (r.type === 4) {
              const isHover = /hover\s*:\s*hover/.test(r.media.mediaText);
              const got = scan(r.cssRules, isHover); if (got) return got;
            }
          }
          return null;
        };
        const got = scan(top, false); if (got) return got;
      }
      return null;
    }"""
    with serve(TMP_SND) as base5:
        with Browser(width=1280, height=900) as br:
            br.navigate(base5 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)

            # 11 · the tray HOVER reveal is gated to @media(hover:hover) — the swallow fix
            m = br.evaluate("(%s)('#ex-sound:hover .exsnd-tray', null)" % RULE_MEDIA)
            check(BROWSER_ROWS[10], m == "hover", f"media={m!r}")

            # 12 · the .playing / :focus-within reveal stays unconditional (touch opens by playing)
            m = br.evaluate("(%s)('#ex-sound.playing .exsnd-tray', 'max-width')" % RULE_MEDIA)
            check(BROWSER_ROWS[11], m == "bare", f"media={m!r}")

            # 13 · adding .playing reveals the credit tray (first tap starts → .playing → tray open).
            # The tray max-width transitions (calc(.5s*tempo)) — settle it before the read.
            br.evaluate("document.getElementById('ex-sound').classList.add('playing')")
            br.sleep(0.8)
            tw = br.evaluate(
                "(()=>{const t=document.querySelector('#ex-sound .exsnd-tray');"
                "return getComputedStyle(t).maxWidth;})()")
            ok13 = tw not in (None, "0px", "0", "none")
            check(BROWSER_ROWS[12], ok13, f"tray max-width with .playing = {tw!r}")

            # 14 · a PLAYING player rides a walk crossing (opacity stays 1 under body.ex-crossing)
            br.evaluate("document.body.classList.add('ex-crossing')")
            br.sleep(0.6)
            op_play = br.evaluate("(()=>getComputedStyle(document.getElementById('ex-sound')).opacity)()")
            check(BROWSER_ROWS[13], op_play == "1", f"opacity(.playing+crossing)={op_play!r}")

            # 15 · a SILENT player still retracts on a crossing (loading frame stands alone). Drop
            # .playing and let the opacity transition (var(--d-soft)) settle before the read.
            br.evaluate("document.getElementById('ex-sound').classList.remove('playing')")
            br.sleep(0.8)
            op_silent = br.evaluate("(()=>getComputedStyle(document.getElementById('ex-sound')).opacity)()")
            check(BROWSER_ROWS[14], op_silent == "0", f"opacity(silent+crossing)={op_silent!r}")
            br.evaluate("document.body.classList.remove('ex-crossing')")

            # 16 · the exit accent fill is HOVER-gated; its focus-visible fill is unconditional
            mh = br.evaluate("(%s)('#ex-zoom .exz-btn:hover', 'accent')" % RULE_MEDIA)
            mf = br.evaluate("(%s)('#ex-zoom .exz-btn:focus-visible', 'accent')" % RULE_MEDIA)
            check(BROWSER_ROWS[15], mh == "hover" and mf == "bare", f"hover={mh!r} focus-visible={mf!r}")

            # 17 · the share accent fill is HOVER-gated (a finger tap leaves no sticky tan circle)
            ms = br.evaluate("(%s)('.ex-share:hover', 'accent')" % RULE_MEDIA)
            check(BROWSER_ROWS[16], ms == "hover", f"media={ms!r}")

            # 18 · a coarse-pointer press adds .ex-press to a control (the prelude's delegated driver),
            #      and a lift clears it — the touch response that hover-gating withholds from a finger
            press = br.evaluate(
                "(()=>{const b=document.querySelector('.ex-share');"
                "if(!b)return JSON.stringify({err:'no-share'});"
                "b.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));"
                "const on=b.classList.contains('ex-press');"
                "b.dispatchEvent(new PointerEvent('pointerup',{bubbles:true}));"
                "const off=b.classList.contains('ex-press');"
                "return JSON.stringify({on:on,off:off});})()")
            pj = json.loads(press)
            check(BROWSER_ROWS[17], pj.get("on") is True and pj.get("off") is False, f"press={press!r}")

            # 19 · each chrome control has a .ex-press engaged rule under @media(hover:none), so a mouse
            #      (hover:hover) keeps its own hover fill and only a finger sees the press flash
            PRESS_UNDER_HOVERNONE = r"""(sel) => {
              for (const sheet of document.styleSheets) {
                let top; try { top = sheet.cssRules; } catch (e) { continue; }
                for (const r of top) {
                  if (r.type === 4 && /hover\s*:\s*none/.test(r.media.mediaText)) {
                    for (const inner of r.cssRules) {
                      if (inner.type === 1 && inner.selectorText
                          && inner.selectorText.indexOf(sel) !== -1
                          && inner.selectorText.indexOf('ex-press') !== -1) return true;
                    }
                  }
                }
              }
              return false;
            }"""
            controls = [".ex-share", ".exz-btn", ".exsnd-btn", ".quiz-opt",
                        ".exl-cur", ".exl-item", ".exd-window", ".gift-yes"]
            missing = [s for s in controls
                       if not br.evaluate("(%s)('%s')" % (PRESS_UNDER_HOVERNONE, s))]
            check(BROWSER_ROWS[18], not missing, f"controls with no hover:none .ex-press rule: {missing}")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_SND, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
