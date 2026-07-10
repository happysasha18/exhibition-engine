#!/usr/bin/env python3
"""Motion & accent (EX-MOTION / EX-MOTION-R / EX-ACCENT, INV-33) — adapted for exhibition-engine.
Run: python tests/test_motion.py
"""
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
BONE = (179, 162, 132)  # #b3a284

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_motion_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
CONFIG_PATH = TMP / "config.json"
CONFIG0 = CONFIG_PATH.read_text()
CSS_FILES = [TMP / "exhibition.css", TMP / "gallery" / "shared" / "tokens.css"]

# ---------------------------------------------------------------- data + string rows

cfg_ex = json.loads(CONFIG0)["exhibition"]
check("EX-MOTION tempo is config: knob present (1.35), transition_ms tombstoned",
      cfg_ex.get("tempo") == 1.35 and "transition_ms" not in cfg_ex,
      f"tempo={cfg_ex.get('tempo')} keys={sorted(cfg_ex)}")

rogue = []
for f in CSS_FILES:
    css = re.sub(r"/\*.*?\*/", "", f.read_text(encoding="utf-8"), flags=re.S)
    for m in re.finditer(r"\b\d*\.?\d+m?s\b", css):
        ctx = css[max(0, m.start() - 90):m.end() + 60]
        if "var(--tempo)" in ctx or "var(--d-" in ctx:
            continue
        rogue.append(f"{f.name}: …{css[max(0, m.start() - 30):m.end() + 10]}…")
check("EX-MOTION no rogue literals: every shipped duration/delay multiplies by the tempo",
      not rogue, " | ".join(rogue[:4]))

orange = [f.name for f in CSS_FILES if "c96442" in f.read_text(encoding="utf-8").lower()]
check("EX-ACCENT string sweep: the old brand orange #c96442 is gone from the shipped css",
      not orange, f"found in {orange}")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-MOTION one clock ships (tempo 1.35 computed; ground/rise/reveal ride it; crossing waits the cross span)",
    "EX-MOTION tempo is config (flip 0.5 → computed durations halve)",
    "EX-MOTION-R reduced-motion collapses (tempo 0.05, near-instant crossing)",
    "EX-MOTION-R override clamped (0.2 honored; banana ignored; 9000 → 3)",
    "EX-ACCENT rests bone at the cold door",
    "EX-ACCENT lives in the hang (raised tone, fin wears it), rests again at the exit",
    "EX-MOTION fade-only entries (door windows + hang frames never lift)",
]

TEMPO_NOW = "getComputedStyle(document.documentElement).getPropertyValue('--tempo').trim()"
BODY_GROUND_S = "getComputedStyle(document.body).transitionDuration"
ACCENT_LIVE = "document.documentElement.style.getPropertyValue('--accent').trim()"
ACCENT_COMPUTED = "getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()"
AT_DOOR = "document.body.classList.contains('ex-door')"


def fresh(br, base, tempo=None):
    br.navigate(base + "/")
    br.clear_storage()
    if tempo is not None:
        br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.reload()
    br.sleep(1.0)


def secs(s):
    return float(s.replace("s", "").split(",")[0])


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # 0 · one clock at defaults
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base)
            tempo = br.evaluate(TEMPO_NOW)
            ground_d = secs(br.evaluate(BODY_GROUND_S))
            rise_d = secs(br.evaluate(
                "getComputedStyle(document.querySelector('.exd-window')).animationDuration"))
            br.click(".exd-window", settle=0.3)
            still_door = br.evaluate(AT_DOOR)
            check(BROWSER_ROWS[0],
                  tempo == "1.35"
                  and abs(ground_d - 2.295) < 0.01 and abs(rise_d - 1.89) < 0.01
                  and still_door,
                  f"tempo={tempo} ground={ground_d} rise={rise_d} door@0.3={still_door}")

        # 1 · the knob is config
        cfg = json.loads(CONFIG0)
        cfg["exhibition"]["tempo"] = 0.5
        CONFIG_PATH.write_text(json.dumps(cfg))
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base)
            tempo = br.evaluate(TEMPO_NOW)
            ground_d = secs(br.evaluate(BODY_GROUND_S))
        CONFIG_PATH.write_text(CONFIG0)
        check(BROWSER_ROWS[1], tempo == "0.5" and abs(ground_d - 0.85) < 0.01,
              f"tempo={tempo} ground={ground_d}")

        # 2 · reduced motion wins
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            br.emulate_media(prefers_reduced_motion="reduce")
            fresh(br, base)
            tempo = br.evaluate(TEMPO_NOW)
            br.click(".exd-window", settle=0.9)
            in_hang = not br.evaluate(AT_DOOR)
            check(BROWSER_ROWS[2], tempo == "0.05" and in_hang,
                  f"tempo={tempo} hang@0.9={in_hang}")

        # 3 · the localStorage override: honored, ignored, clamped
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base, tempo="0.2")
            t_02 = br.evaluate(TEMPO_NOW)
            br.click(".exd-window", settle=1.8)
            in_hang = not br.evaluate(AT_DOOR)
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base, tempo="banana")
            t_bad = br.evaluate(TEMPO_NOW)
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base, tempo="9000")
            t_big = br.evaluate(TEMPO_NOW)
        check(BROWSER_ROWS[3],
              t_02 == "0.2" and in_hang and t_bad == "1.35" and t_big == "3",
              f"0.2→{t_02} hang={in_hang} banana→{t_bad} 9000→{t_big}")

        # 4 · the accent rests as bone at the cold door
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base)
            resting = br.evaluate(ACCENT_COMPUTED)
            no_live = br.evaluate(ACCENT_LIVE) == ""
            check(BROWSER_ROWS[4], resting == "#b3a284" and no_live,
                  f"computed={resting!r} live-empty={no_live}")

        # 5 · the accent LIVES from the pick, fin wears it, exit rests it
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base, tempo="0.2")
            first_id = br.evaluate(
                "document.querySelector('.exd-window').dataset.id")
            works = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))["works"]
            dom = tuple(next(w["dom"] for w in works if w["id"] == first_id))
            y = 0.2126 * dom[0] + 0.7152 * dom[1] + 0.0722 * dom[2]
            if y < 24:
                expect = BONE
            else:
                k = min(170 / y, 6)
                expect = tuple(int(min(255, v * k) * 0.8 + BONE[i] * 0.2 + 0.5)
                               for i, v in enumerate(dom))
            br.click(".exd-window", settle=1.8)
            live = br.evaluate(ACCENT_LIVE)
            got = tuple(int(x) for x in re.findall(r"\d+", live)[:3]) if live else ()
            fin_rides = br.evaluate(
                "(()=>{const f=document.getElementById('exh-fin');if(!f)return null;"
                "const m=f.querySelector('.more');"
                "return m?getComputedStyle(m).color:'no-more';})()")
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.3)
            br.click("#ex-return", settle=0.6)
            rested = br.evaluate(ACCENT_LIVE) == ""
            back_door = br.evaluate(AT_DOOR)
            check(BROWSER_ROWS[5],
                  live != "" and got == expect
                  and fin_rides == f"rgb({got[0]}, {got[1]}, {got[2]})"
                  and back_door and rested,
                  f"dom={dom} expect={expect} got={got} fin={fin_rides!r} "
                  f"door={back_door} rested={rested}")

        # 6 · fade-only entries
        with Browser(width=1280, height=900) as br:
            br.pretend("ru-RU", 15)
            fresh(br, base, tempo="0.2")
            win_tf = br.evaluate(
                "getComputedStyle(document.querySelector('.exd-window')).transform")
            br.click(".exd-window", settle=1.8)
            frame_tf = br.evaluate(
                "getComputedStyle(document.querySelector('.exh-frame img.work')).transform")
            check(BROWSER_ROWS[6], win_tf == "none" and frame_tf == "none",
                  f"window={win_tf} frame={frame_tf}")


# ---------------------------------------------------------------- report
import shutil
shutil.rmtree(TMP, ignore_errors=True)

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
