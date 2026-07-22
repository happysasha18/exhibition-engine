#!/usr/bin/env python3
"""EX-SOUND (INV-48): the ambient player — OFF by default, config-driven URL and credit.
Tests: player absent when sound_url is empty; player present when configured; SND_KEY in reset;
pause/resume semantics (pausedOffset/startedAt); EX-ARRIVE for the box; preference persistence.
Run: python tests/test_sound.py
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


# ---------------------------------------------------------------- bake (sound_url empty = default)
TMP = Path(tempfile.mkdtemp(prefix="synth_sound_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

# ---------------------------------------------------------------- bake with sound configured (browser tests)
TMP_SND = Path(tempfile.mkdtemp(prefix="synth_sound_on_"))
build_site.OUT = TMP_SND
build_site.build(SITE_URL)
# Patch config.json to inject a synthetic audio URL (JS reads config.json at runtime)
_cfg_path = TMP_SND / "config.json"
_cfg = json.loads(_cfg_path.read_text())
_cfg["exhibition"]["sound_url"] = "/audio/ambient.m4a"
_cfg["exhibition"]["sound_credit"] = {
    "artist": "Synth Artist",
    "title": "Test Track",
    "url": "https://synth.example.com",
}
_cfg_path.write_text(json.dumps(_cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

# ---------------------------------------------------------------- data rows

# 1 · a knob at its default is SUPPRESSED from the emitted config (2026-07-09 contract: the
#     served config carries only what the instance actually set — no dead keys; every client
#     read is fallback-guarded, sound joins only with a URL)
cfg = json.loads((TMP / "config.json").read_text())
ex = cfg.get("exhibition") or {}
check("EX-SOUND config omits sound knobs when unset (suppressed-at-default contract)",
      "sound_url" not in ex and "sound_credit" not in ex,
      f"exhibition keys: {sorted(ex.keys())}")

# 2 · absent knob reads as OFF (the client's fallback path — same behavior as the old "")
check("EX-SOUND player is OFF by default (no sound_url in config)",
      (ex.get("sound_url") or "") == "",
      f"sound_url={ex.get('sound_url')!r}")

js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")

# 3 · SND_KEY declared and wiped on ?reset
check("EX-SOUND SND_KEY ('ex.sound') declared and cleared on ?reset",
      'const SND_KEY = "@@NS@@.sound"' in js_src
      and "localStorage.removeItem(SND_KEY)" in js_src,
      "SND_KEY declaration or reset removal missing from exhibition.js")

# 4 · early-exit guard when sound_url is empty
check("EX-SOUND IIFE exits early on empty sound_url",
      "if (!SND_URL) return;" in js_src,
      "early-exit guard missing from sound() IIFE")

# 5 · streaming <audio> element — instant start, native loop, no full-decode wait
check("EX-SOUND streams from an <audio> element (createElement('audio'), preload=none, native loop)",
      'createElement("audio")' in js_src
      and "preload" in js_src
      and ".loop = true" in js_src
      and ".play()" in js_src,
      "streaming <audio> element wiring missing from exhibition.js")

# 5a2 · one press starts the sound (his find 2026-07-22: it took TWO taps). The context resume is
#        kicked WITHOUT being awaited first (that older order spent the single activation and play()
#        was refused), and aud.play() is awaited directly. Red before the first fix, when
#        `await ctx.resume()` ran BEFORE `aud.play()` — that order left `await aud.play()` absent.
resume_kicked = "const resuming = (ctx.state === \"suspended\") ? ctx.resume() : null;" in js_src
play_awaited = "await aud.play(); played = true;" in js_src
one_press_ok = resume_kicked and play_awaited
check("EX-SOUND one press plays: ctx.resume() kicked un-awaited, aud.play() awaited (no double-tap)",
      one_press_ok, "start() must kick resume() without awaiting it first, then await aud.play()")

# 5a2b · his 2026-07-22 RESIDUAL: on WebKit the first press STILL only armed — the context was still
#        suspended AT THE aud.play() call (the same-gesture resume had not settled), so play() rejected
#        and the code armed for a second tap. The fix: on a rejected first play, await the resume, then
#        RETRY aud.play() ONCE within the same activation chain. Red before this fix (only one play call).
retry_on_suspended = (js_src.count("await aud.play()") >= 2
                      and "if (resuming) { try { await resuming; } catch (e2) {} }" in js_src)
check("EX-SOUND retries play() once after resume settles (WebKit suspended-at-call → still one press)",
      retry_on_suspended,
      "start() must retry aud.play() after awaiting the resume — else WebKit needs a second tap")

# 5a2c · EX-SOUND-LOADING: between the press and the first sound the note shows a buffering state
#        (a slow stream reads as "loading", never "nothing happened"); it clears on play / fail / arm.
loading_ui = ('box.classList.add("loading")' in js_src
              and 'box.classList.remove("loading")' in js_src)
check("EX-SOUND-LOADING: the note carries a buffering state between press and first sound",
      loading_ui, "start()/stop() must toggle a .loading class on the player box")

# 5a2d · the loading state is a soft, reduced-motion-guarded note pulse in the served CSS
css_src = (ROOT / "engine" / "assets" / "exhibition.css").read_text(encoding="utf-8")
loading_css = ("#ex-sound.loading .exsnd-note" in css_src
               and "@keyframes exsnd-load" in css_src
               and "prefers-reduced-motion:reduce){ #ex-sound.loading .exsnd-note{ animation:none" in css_src)
check("EX-SOUND-LOADING: the buffering note pulse is defined and stands down for reduced motion",
      loading_css, "exsnd-load keyframe or its reduced-motion guard missing from exhibition.css")

# 5b · the old full-decode path is retired — the download-then-decode wait is exactly what the swap removes
check("EX-SOUND retires the full-decode path (no decodeAudioData / createBufferSource)",
      "decodeAudioData" not in js_src
      and "createBufferSource" not in js_src,
      "a full-decode Web Audio path still present — the swap removes the download-then-decode wait")

# 5c · the fade rides a MediaElementSource → gain node so the ramp works on every device (incl. iOS,
#      where the element's own volume cannot be scripted)
check("EX-SOUND fade rides a MediaElementSource → gain node (universal ramp, incl. iOS)",
      "createMediaElementSource" in js_src
      and "createGain" in js_src
      and "linearRampToValueAtTime" in js_src,
      "MediaElementSource/gain fade wiring missing from exhibition.js")

# 5d · pause holds the element's own playhead (currentTime); no manual offset bookkeeping remains
check("EX-SOUND-PAUSE holds the element playhead (currentTime), never manual offset math",
      "currentTime" in js_src
      and "pausedOffset" not in js_src
      and "startedFrom" not in js_src,
      "pause/resume should ride the element's currentTime, not pausedOffset/startedFrom")

# 5e · a failed file fails SILENT via the element error handler (INV-1); the toggle's own aria-pressed
#      stays the visitor's choice (the equalizer bars, not the button, signal actual playback)
_err = js_src[js_src.find('aud.addEventListener("error"'):][:120]
check("EX-SOUND a failed file fails silent through the <audio> error handler (INV-1)",
      "stop();" in _err and 'aud.addEventListener("error"' in js_src,
      "the <audio> element needs an error handler that stops the graph and fails silent")

# 6 · credit HTML is config-driven
check("EX-SOUND credit tray is config-driven (CREDIT.artist/title/url, not hardcoded)",
      "CREDIT.artist" in js_src and "CREDIT.title" in js_src and "CREDIT.url" in js_src,
      "hardcoded credit — should use CREDIT.* from EX.sound_credit")

# 7 · EX-SOUND-GREET (INV-101) — music-note glyph replaced the play triangle
check("EX-SOUND-GREET music-note glyph replaces the play triangle",
      "exsnd-note" in js_src and "exsnd-play" not in js_src,
      "expected .exsnd-note glyph and no leftover .exsnd-play triangle")

# 8 · EX-SOUND-GREET localized word with English fallback
check("EX-SOUND-GREET word localizes via SNDT.sound_greet with SOUND_GREET_EN fallback",
      "sound_greet" in js_src and "SOUND_GREET_EN" in js_src,
      "localized greeting word / English fallback wiring missing")

# 9 · EX-SOUND-GREET once-ness persists in the pref
check("EX-SOUND-GREET once-ness persists in ex.sound (greeted)",
      "greeted: greeted" in js_src and "pref.greeted" in js_src,
      "greeted flag missing from persist()/pref read")

# 10 · EX-SOUND-GREET stands down under reduced motion / Save-Data
check("EX-SOUND-GREET stands down under reduced motion / Save-Data",
      "REDUCED || dataSaver()" in js_src,
      "reduced-motion/Save-Data stand-down guard missing")

# 11 · EX-SOUND-GREET fires only past the door (visible-gate)
check("EX-SOUND-GREET fires only once the player is visible past the door",
      "ex-door" in js_src and "getComputedStyle(box).opacity" in js_src,
      "visible-gate (door check + opacity read) missing from greetOnce/waitVisible")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-SOUND player absent from DOM when sound_url is empty",
    "EX-SOUND player present + EX-ARRIVE (.show + opacity>0) when sound_url is configured",
    "EX-SOUND btn starts aria-pressed=false; after toggle pref persisted in localStorage",
    "EX-SOUND ?reset clears the sound pref (SND_KEY wiped alongside other walk keys)",
    "EX-SOUND-GREET first visit persists greeted:true and renders the note glyph",
    "EX-SOUND-GREET return visit shows no .exsnd-greet element (once-ness held)",
]

SND_OP = ("(()=>{const e=document.getElementById('ex-sound');"
          "return e?getComputedStyle(e).opacity:null;})()")


def enter_walk(br):
    """Leave the cold door for the walk. The player retracts under the door (EX-CHROME / INV-77 scope),
    so the pressable player lives on the walk — every interaction row enters first."""
    if br.evaluate("!!document.querySelector('.exd-window')"):
        br.click(".exd-window:nth-child(1)", settle=1.0)
    for _ in range(30):
        if (not br.evaluate("document.body.classList.contains('ex-door')")
                and br.evaluate(SND_OP) == "1"):
            break
        br.sleep(0.1)


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    # 0 · player absent when sound_url empty
    with serve(TMP) as base, Browser(width=1280, height=900) as br:
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("localStorage.setItem('ex-tempo','0.5')")
        br.reload()
        br.sleep(1.0)
        n_sound = br.evaluate("document.querySelectorAll('#ex-sound').length")
        check(BROWSER_ROWS[0], n_sound == 0, f"#ex-sound count={n_sound} (want 0)")

    with serve(TMP_SND) as base2:
        # 1 · player present + EX-ARRIVE
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            # the player retracts at the door (EX-CHROME) — its pressable, on-the-breath home is the walk
            door_op = br.evaluate(SND_OP)
            enter_walk(br)
            state = br.evaluate(
                "(()=>{const b=document.getElementById('ex-sound');"
                "if(!b)return {present:false};"
                "const op=+getComputedStyle(b).opacity;"
                "return {present:true,opacity:op,show:b.classList.contains('show')};})()")
            check(BROWSER_ROWS[1],
                  door_op == "0" and state.get("present") and state.get("show")
                  and state.get("opacity", 0) > 0.9,
                  f"door_op={door_op} walk_state={state}")

        # 2 · btn off by default; pref persisted on toggle
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)                               # the pressable player lives on the walk
            init = br.evaluate(
                "(()=>{const btn=document.querySelector('.exsnd-btn');"
                "return {pressed: btn ? btn.getAttribute('aria-pressed') : null};})()")
            br.click(".exsnd-btn", settle=0.3)
            after = br.evaluate(
                "(()=>{const btn=document.querySelector('.exsnd-btn');"
                "const pref=JSON.parse(localStorage.getItem('ex.sound')||'null');"
                "return {pressed: btn ? btn.getAttribute('aria-pressed') : null,"
                "pref_on: !!(pref&&pref.on)};})()")
            check(BROWSER_ROWS[2],
                  init.get("pressed") == "false"
                  and after.get("pressed") == "true"
                  and after.get("pref_on"),
                  f"init={init} after={after}")

        # 3 · ?reset clears the sound pref
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            # Pre-plant a sound pref in storage
            br.evaluate("localStorage.setItem('ex.sound',JSON.stringify({v:'1',on:true,vol:0.5}))")
            br.navigate(base2 + "/?reset")
            br.sleep(0.8)
            pref = br.evaluate("localStorage.getItem('ex.sound')")
            check(BROWSER_ROWS[3], pref is None,
                  f"sound pref still in storage after ?reset: {pref!r}")

        # 4/5 · EX-SOUND-GREET (INV-101) — first visit greets + persists once-ness; a return visit
        #        in the SAME browser (reusing the greeted:true the first load wrote) stays quiet
        with Browser(width=1280, height=900) as br:
            br.navigate(base2 + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.5')")
            br.reload()
            br.sleep(1.0)
            enter_walk(br)
            br.sleep(0.5)                                # let the greetOnce()/waitVisible rAF settle
            first = br.evaluate(
                "(()=>{const pref=JSON.parse(localStorage.getItem('ex.sound')||'null');"
                "const note=!!document.querySelector('.exsnd-note');"
                "return {greeted: !!(pref&&pref.greeted===true), note};})()")
            check(BROWSER_ROWS[4],
                  first.get("greeted") is True and first.get("note"),
                  f"first-visit state={first}")

            # return visit: same browser, same storage (greeted:true already persisted above) —
            # reload + re-enter the walk and confirm no .exsnd-greet element ever appears
            br.reload()
            br.sleep(1.0)
            enter_walk(br)
            seen_greet = False
            for _ in range(10):
                if br.evaluate("!!document.querySelector('.exsnd-greet')"):
                    seen_greet = True
                    break
                br.sleep(0.1)
            check(BROWSER_ROWS[5], not seen_greet,
                  "`.exsnd-greet` appeared on a return visit despite greeted:true persisted")

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_SND, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
