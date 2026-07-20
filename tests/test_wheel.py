#!/usr/bin/env python3
"""EX-GLIDE / INV-84 — the wheel re-arm verdict is PURE and SETTINGS-INDEPENDENT (his 2026-07-16
word): macOS scales every wheel |deltaY| by the user's own trackpad-speed setting, so the one-swipe-
one-frame verdict may read only TIME and RATIOS — never an absolute |deltaY| magnitude. The client
holds that verdict in one DOM-free function, `wheelWalkStep({t, dy}, state) -> -1|0|+1`; this suite
extracts it (with its constants) straight from exhibition.js and REPLAYS realistic recorded-shape
trackpad envelopes through it in node — sample by sample, deterministic timestamps, no browser, no
sleeps (the same extract-and-run pattern as test_parity).

The envelopes are the shape a real macOS trackpad emits — a sharp spike then a LONG decaying
momentum tail with micro-humps — never the too-clean monotonic ramps a synthetic fixture tends to
draw. The two recorded defects both live in that bumpiness: a tail hump used to cross the old
absolute FLOOR/RISE rails (a false second step), and a genuine second swipe over a HIGH tail never
saw the absolute dip (swallowed).

Rows:
  WHL1  the pure block (six constants + wheelWalkStep) is extractable from the client
  WHL2  one realistic bumpy swipe -> EXACTLY one step (the tail hump never re-steps)
  WHL3  a decaying tail then a SHARP relative re-acceleration -> two steps (never eaten)
  WHL4  a real >=100ms pause in the stream, then a push -> two steps (the gap re-arms)
  WHL5  a slow continuous drag -> exactly one step
  WHL6  SCALE INVARIANCE: every waveform x2 and x0.5 -> the SAME steps (the owner's constraint
        as a test — an absolute-|deltaY|-threshold implementation cannot pass all three scales)
  WHL7  the old absolute thresholds (RESWIPE_PEAK/FLOOR/RISE, wheelQuiet) are GONE from the client
  WHL8  mouse notches (one event each, real gaps) step one frame per notch, both directions

node is a hard dependency (the replay cannot run without it) — its absence FAILS, never skips.
Run: .venv/bin/python tests/test_wheel.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS_PATH = ROOT / "engine" / "assets" / "exhibition.js"
JS_SRC = JS_PATH.read_text(encoding="utf-8")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


# ---------------------------------------------------------------- WHL1: extract the pure block
# the six constants and the function travel together — the function reads the constants, so the
# extracted block is runnable as-is in a bare node context (no DOM, no timers, no outer state)
m = re.search(r"const WHEEL_IDLE_MS.*?function wheelWalkStep.*?\n  \}", JS_SRC, re.S)
BLOCK = m.group(0) if m else None
check("WHL1 EX-GLIDE the pure wheel verdict (constants + wheelWalkStep) is extractable",
      BLOCK is not None,
      "" if BLOCK else "no `const WHEEL_IDLE_MS ... function wheelWalkStep(){...}` block in exhibition.js")

# ---------------------------------------------------------------- WHL7: the absolute rails are gone
# hunt live DECLARATIONS, not the history comment that names the removed rails for the record
LEFTOVERS = [w for w in ("const RESWIPE_PEAK", "const RESWIPE_FLOOR", "const RESWIPE_RISE",
                         "let wheelQuiet", "wheelQuiet =", "wheelQuiet)")
             if w in JS_SRC]
check("WHL7 EX-GLIDE no absolute |deltaY| rail survives (RESWIPE_PEAK/FLOOR/RISE, wheelQuiet gone)",
      not LEFTOVERS, f"still declared/used in exhibition.js: {', '.join(LEFTOVERS)}" if LEFTOVERS else "")


# ---------------------------------------------------------------- the recorded-shape waveforms
def cadence(mags, gap_ms, t0=0.0):
    """a momentum stream as (t, dy) samples at a device cadence"""
    return [[t0 + i * gap_ms, m] for i, m in enumerate(mags)]


# one realistic swipe at ~120Hz: sharp spike, long bumpy decaying tail. The 12->21 hump at ~264ms
# is a modest wobble at a scaled-up speed setting — exactly what crossed the old absolute rails.
BUMPY_ONE = cadence([5, 16, 42, 98, 145, 126, 99, 108, 82, 66, 71, 53, 44, 37, 40, 31,
                     26, 22, 24, 18, 15, 12, 21, 14, 10, 8, 7, 5, 4, 4, 3, 3, 2, 2], 12)

# a full swipe + its bumpy tail flowing on, then a SHARP re-acceleration ~430ms in (a deliberate
# second swipe: the surge is judged RELATIVE to the decayed envelope, so any speed setting agrees)
REACCEL = (cadence([6, 22, 58, 112, 140, 118, 96, 81, 69, 74, 58, 49, 42, 45, 36, 30, 26,
                    28, 22, 19, 16, 17, 13, 11, 10, 8, 9, 7, 6, 5, 5, 4, 4, 3, 3], 12)
           + cadence([34, 105, 150, 110], 12, t0=35 * 12))

# a swipe whose stream truly STOPS (a 110ms hole — macOS momentum ticks far faster, so a hole
# this long means the prior gesture ended), then a fresh push inside the same 150ms idle window
PAUSE_PUSH = (cadence([8, 30, 70, 90, 60, 40, 26, 17, 11, 7, 5, 4, 3, 3], 12)
              + cadence([50, 80, 40], 12, t0=13 * 12 + 110))

# a slow continuous two-finger drag: sparse-ish events, near-constant small deltas, ~765ms long
SLOW_DRAG = cadence([7, 8, 7, 9, 8, 7, 8, 9, 8, 7, 8, 7, 9, 8, 7, 8, 7, 8], 45)

# a mouse notch is ONE event with a real gap before the next
NOTCHES_FWD = [[0, 120], [400, 120], [800, 120]]
NOTCHES_BACK = [[0, -120], [400, -120]]


def vcadence(mags, gaps, t0=0.0):
    """a momentum stream at a VARIABLE cadence — real macOS momentum spaces its events out as it
    decays (the tail's gaps grow), which the fixed-cadence waveforms above never exercise."""
    out, t = [], t0
    for i, m in enumerate(mags):
        out.append([t, m])
        t += gaps[i] if i < len(gaps) else 0.0
    return out


# ONE swipe whose momentum tail SPACES OUT as it decays — the gap grows 12ms → 130ms. The bare
# time-gap re-arm read each late tail event (gap ≥ 90ms) as a fresh gesture and stepped again and
# again: one swipe read as FOUR steps. The verdict must not read a growing tail gap as a new gesture.
SPARSE_TAIL = vcadence(
    [6, 28, 74, 132, 150, 124, 98, 80, 66, 54, 45, 37, 30, 24, 20, 16, 13, 11, 9, 7, 6, 5, 4, 3, 3, 2],
    [12, 12, 12, 12, 12, 14, 16, 18, 20, 24, 28, 34, 40, 48, 58, 70, 84, 96, 104, 110, 116, 120, 124, 128, 130, 132])

# TWO deliberate swipes only ~200ms apart (a fast browse: finger lift + re-swipe, a ~110ms hole).
# The old STEP_MIN_MS=250 human-rhythm floor swallowed the second — one gesture too FEW.
FAST_RESWIPE = (cadence([8, 30, 70, 90, 60, 40, 26, 17, 11, 7], 12)
                + cadence([50, 90, 120, 80, 40], 12, t0=10 * 12 + 110))

# ONE swipe whose tail carries a tiny two-event ripple (quantization wobble, 14→17→19, ~10% of peak):
# NOISE, not a re-engagement — must stay one step. Contrast REACCEL (a real relative surge → two).
RIPPLE_TAIL = vcadence(
    [6, 30, 80, 140, 150, 120, 90, 64, 44, 30, 20, 14, 17, 19, 12, 8, 6, 4, 3],
    [12, 12, 12, 12, 12, 14, 16, 20, 26, 34, 44, 56, 60, 58, 54, 50, 48, 46, 44])

# An adversarial audit (2026-07-20) broke an earlier fix on these: in the FAR tail the envelope decays so
# much across a wide gap that it catches the live value, and the bare ratio test degenerates — a tiny
# multi-event uptick then clears it. The physical tell the fix now reads: a re-swipe onset climbs on the
# finger's OWN dense cadence (~12ms), while these ripples climb across 50-130ms tail gaps. All must stay ONE.
RIPPLE_GENTLE = vcadence(   # the same 14→17→19 ripple on a GENTLE flick (peak 60) — the envelope no longer masks it
    [4, 18, 40, 60, 52, 40, 30, 22, 16, 14, 17, 19, 12, 8, 5, 3],
    [12, 12, 12, 12, 14, 16, 20, 26, 34, 44, 56, 60, 58, 54, 50])
RIPPLE_FAR = vcadence(      # the ripple pushed further out into the sparse tail (same peak 150)
    [6, 30, 80, 140, 150, 120, 90, 64, 44, 30, 20, 14, 10, 8, 10, 12, 8, 6, 4, 3],
    [12, 12, 12, 12, 12, 14, 16, 20, 26, 34, 44, 56, 60, 58, 56, 54, 52, 50, 48])
FARTAIL_UPTICK = vcadence(  # a 2→3→4 quantization uptick in the far tail (gaps ~120ms)
    [6, 30, 80, 140, 150, 120, 90, 66, 48, 34, 24, 17, 12, 9, 6, 4, 3, 2, 3, 4, 3, 2],
    [12, 12, 12, 12, 12, 14, 16, 20, 26, 34, 44, 56, 66, 76, 86, 96, 104, 112, 118, 122, 126])
DRAG_RELEASE = vcadence(    # ONE continuous drag that eases off (crests) then re-accelerates — one contact, no lift
    [8, 10, 9, 11, 10, 9, 8, 7, 6, 5, 4, 3, 4, 5, 3, 2],
    [40, 40, 42, 44, 46, 50, 54, 58, 64, 70, 80, 92, 100, 104, 100, 96])

# A second audit (2026-07-20) broke the gap-gate-only fix on THIS: a continuous drag whose re-accel is
# DENSE (<35ms) rides the gap gate exactly like a re-swipe onset. The physical tell the fix now reads:
# a re-swipe follows a momentum END (the stream DIES to near-zero), whereas a within-drag ease only slows
# to a fraction of its peak. This drag eases to ~25% and re-accels dense — one contact, ONE step.
DRAG_REACCEL_DENSE = vcadence(
    [9, 11, 10, 12, 11, 9, 7, 5, 4, 3, 5, 9, 13, 8, 4],
    [16, 16, 18, 18, 20, 24, 30, 38, 44, 40, 22, 14, 14, 20, 26])
SCRUB_REACCEL = vcadence(
    [7, 9, 8, 10, 9, 7, 5, 4, 3, 6, 10, 7, 4],
    [18, 18, 20, 22, 26, 30, 34, 32, 28, 20, 16, 22, 28])


def scaled(samples, k):
    """the SAME finger at a different macOS trackpad-speed setting: |deltaY| scales, time does not"""
    return [[t, dy * k] for t, dy in samples]


CASES = {
    "bumpy_one": BUMPY_ONE,
    "reaccel": REACCEL,
    "pause_push": PAUSE_PUSH,
    "slow_drag": SLOW_DRAG,
    "notches_fwd": NOTCHES_FWD,
    "notches_back": NOTCHES_BACK,
    "sparse_tail": SPARSE_TAIL,
    "fast_reswipe": FAST_RESWIPE,
    "ripple_tail": RIPPLE_TAIL,
    "ripple_gentle": RIPPLE_GENTLE,
    "ripple_far": RIPPLE_FAR,
    "fartail_uptick": FARTAIL_UPTICK,
    "drag_release": DRAG_RELEASE,
    "drag_reaccel_dense": DRAG_REACCEL_DENSE,
    "scrub_reaccel": SCRUB_REACCEL,
}
for name in list(CASES):
    CASES[name + "@x2"] = scaled(CASES[name], 2.0)
    CASES[name + "@x0.5"] = scaled(CASES[name], 0.5)

WANT = {
    "bumpy_one": [1],
    "reaccel": [1, 1],
    "pause_push": [1, 1],
    "slow_drag": [1],
    "notches_fwd": [1, 1, 1],
    "notches_back": [-1, -1],
    "sparse_tail": [1],
    "fast_reswipe": [1, 1],
    "ripple_tail": [1],
    "ripple_gentle": [1],
    "ripple_far": [1],
    "fartail_uptick": [1],
    "drag_release": [1],
    "drag_reaccel_dense": [1],
    "scrub_reaccel": [1],
}

# ---------------------------------------------------------------- replay in node
node = shutil.which("node")
STEPS = None
if node is None:
    check("WHL2-8 EX-GLIDE waveform replay", False,
          "node not found on PATH — the replay cannot run (hard dependency)")
elif BLOCK is not None:
    runner = (
        BLOCK
        + "\nconst cases = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));\n"
        + "const out = {};\n"
        + "for (const [name, samples] of Object.entries(cases)) {\n"
        + "  const st = { env: 0, peak: 0, crested: false, stepT: 0, lastT: null, fresh: true, prev: 0, rises: 0 };\n"
        + "  const steps = [];\n"
        + "  for (const [t, dy] of samples) {\n"
        + "    const s = wheelWalkStep({ t, dy }, st);\n"
        + "    if (s) steps.push(s);\n"
        + "  }\n"
        + "  out[name] = steps;\n"
        + "}\n"
        + "process.stdout.write(JSON.stringify(out));\n")
    with tempfile.TemporaryDirectory(prefix="wheel_replay_") as td:
        js = Path(td) / "replay.js"
        data = Path(td) / "cases.json"
        js.write_text(runner, encoding="utf-8")
        data.write_text(json.dumps(CASES), encoding="utf-8")
        proc = subprocess.run([node, str(js), str(data)],
                              capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        check("WHL2-8 EX-GLIDE waveform replay", False,
              f"node rc={proc.returncode}: {proc.stderr[:400]}")
    else:
        STEPS = json.loads(proc.stdout)

if STEPS is not None:
    rows = [
        ("WHL2 EX-GLIDE one realistic bumpy swipe -> EXACTLY one step (the hump never re-steps)",
         "bumpy_one"),
        ("WHL3 EX-GLIDE a decaying tail then a sharp RELATIVE re-acceleration -> two steps",
         "reaccel"),
        ("WHL4 EX-GLIDE a real >=100ms pause in the stream, then a push -> two steps",
         "pause_push"),
        ("WHL5 EX-GLIDE a slow continuous drag -> exactly one step",
         "slow_drag"),
        ("WHL9 EX-GLIDE a momentum tail that spaces out (growing gaps) -> ONE step, never re-armed by a tail gap",
         "sparse_tail"),
        ("WHL10 EX-GLIDE two fast swipes ~200ms apart -> TWO steps (the second not swallowed)",
         "fast_reswipe"),
        ("WHL11 EX-GLIDE a tiny two-event tail ripple (noise) -> ONE step (contrast a real surge)",
         "ripple_tail"),
        ("WHL12 EX-GLIDE the same ripple on a gentle flick (no peak to mask it) -> ONE step",
         "ripple_gentle"),
        ("WHL13 EX-GLIDE a ripple pushed out into the sparse tail -> ONE step",
         "ripple_far"),
        ("WHL14 EX-GLIDE a far-tail quantization uptick (wide gaps) -> ONE step (never a re-swipe onset)",
         "fartail_uptick"),
        ("WHL15 EX-GLIDE one slow continuous drag that eases then re-accelerates -> ONE step",
         "drag_release"),
        ("WHL16 EX-GLIDE one continuous drag with a DENSE re-accel (no lift, momentum never died) -> ONE step",
         "drag_reaccel_dense"),
        ("WHL17 EX-GLIDE a gentle scrub that eases then re-accelerates dense -> ONE step",
         "scrub_reaccel"),
    ]
    for title, key in rows:
        check(title, STEPS.get(key) == WANT[key],
              f"steps {STEPS.get(key)} (want {WANT[key]})")
    # WHL6: the same finger at any speed setting sees the same walk — pure ratios+time
    bad = [f"{n}: base {STEPS.get(n)} x2 {STEPS.get(n + '@x2')} x0.5 {STEPS.get(n + '@x0.5')}"
           for n in WANT
           if not (STEPS.get(n) == STEPS.get(n + "@x2") == STEPS.get(n + "@x0.5") == WANT[n])]
    check("WHL6 EX-GLIDE scale invariance: x2 and x0.5 speed settings walk IDENTICALLY",
          not bad, " · ".join(bad))
    check("WHL8 EX-GLIDE mouse notches step one frame per notch, both directions",
          STEPS.get("notches_fwd") == WANT["notches_fwd"]
          and STEPS.get("notches_back") == WANT["notches_back"],
          f"fwd {STEPS.get('notches_fwd')} back {STEPS.get('notches_back')} "
          f"(want {WANT['notches_fwd']} / {WANT['notches_back']})")

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail, 0 skip")
sys.exit(1 if fails else 0)
