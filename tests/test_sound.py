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

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-SOUND player absent from DOM when sound_url is empty",
    "EX-SOUND player present + EX-ARRIVE (.show + opacity>0) when sound_url is configured",
    "EX-SOUND btn starts aria-pressed=false; after toggle pref persisted in localStorage",
    "EX-SOUND ?reset clears the sound pref (SND_KEY wiped alongside other walk keys)",
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

shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(TMP_SND, ignore_errors=True)

fails = [r for r in results if r[1] == "FAIL"]
skips = [r for r in results if r[1] == "SKIP"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails) - len(skips)} pass, "
      f"{len(fails)} fail, {len(skips)} skip")
sys.exit(1 if fails else 0)
