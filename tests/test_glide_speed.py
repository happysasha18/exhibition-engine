#!/usr/bin/env python3
"""EX-GLIDE / INV-84 — the glide's SPEED is continuous across a re-time.

His 2026-07-27 report: a slow two-finger trackpad drag on the desktop feels steppy — the picture
crawls, stalls, crawls. The cause was in the transition curve, not in the step count. A rising wheel
sample re-times the glide in flight, and the old curve (a sine in-out) leaves at ZERO speed, so every
re-time decelerated the walk to a dead stop and re-accelerated from rest. A slow drag re-times four
or five times inside one step, which is the stall the eye reads. The second half of the same cause:
each re-time asked for a FULL calm duration over a shrinking gap, so the landing kept being pushed
out and one frame took far longer than the gesture asked for.

Nothing in the suite could see either one. test_wheel asserts how many frames a gesture advances,
test_glide asserts which frame it lands on and how centred, test_gesture asserts a coarse
calm-vs-sharp duration difference. A curve that stops dead four times mid-travel passes all three.
This suite closes that gap at the level the defect lives on — the per-frame speed of the travel.

The client holds the decision in two DOM-free, clock-free functions, `glideCurve(m)` and
`glidePlan({dist, want, span, carry, leftMs})`; this suite extracts them straight from exhibition.js
and replays the recorded slow-drag trackpad envelope through them in node — sample by sample,
deterministic timestamps, no browser, no sleeps (the extract-and-run pattern of test_wheel).

Rows:
  GSP1  the pure block (glideCurve + glidePlan + its two bounds) is extractable from the client
  GSP2  a glide from REST is unchanged: m=0 is exactly smoothstep, both ends soft
  GSP3  every curve in the allowed entry-speed range is monotonic and cannot overshoot the frame
  GSP4  the curve enters at the speed it was handed — position AND speed are continuous at a re-time
  GSP5  an entry speed pushing the OTHER way starts from rest rather than lurching backward
  GSP6  a re-time may only bring the landing nearer, never push it out
  GSP7  the recorded SLOW DRAG replay: the travel never stalls mid-frame (the reported defect)
  GSP8  the same replay lands inside a bounded time — one frame stays one gesture's worth of travel
  GSP9  the zero-speed restart is GONE from the client (no sine in-out driving the glide)

node is a hard dependency (the replay cannot run without it) — its absence FAILS, never skips.
Run: .venv/bin/python tests/test_glide_speed.py
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


# ---------------------------------------------------------------- GSP1: extract the pure block
# the two functions and their two bounds travel together — glidePlan reads GLIDE_M_MAX and
# GLIDE_MIN_MS, so the extracted block runs as-is in a bare node context (no DOM, no timers).
m = re.search(r"const GLIDE_M_MAX.*?function glidePlan\(a\).*?\n  \}", JS_SRC, re.S)
BLOCK = m.group(0) if m else None
check("GSP1 EX-GLIDE the pure glide math (glideCurve + glidePlan + bounds) is extractable",
      BLOCK is not None,
      "" if BLOCK else "no `const GLIDE_M_MAX ... function glidePlan(a){...}` block in exhibition.js")

# ---------------------------------------------------------------- GSP9: the zero-speed restart is gone
# hunt the LIVE driver, not the history comment that names the retired curve for the record
SINE = re.search(r"scrollTo\(0, from \+ d \* [^)]*cos", JS_SRC)
check("GSP9 EX-GLIDE no zero-entry sine drives the glide any more",
      SINE is None,
      "a cosine curve still writes the glide position" if SINE else "")

if BLOCK is None:
    for n, s, d in results:
        print(f"{s}  {n}" + (f"   — {d}" if d else ""))
    sys.exit(1)

NODE = shutil.which("node")
if not NODE:
    check("GSP node present (the replay is the test)", False, "node not on PATH")
    for n, s, d in results:
        print(f"{s}  {n}" + (f"   — {d}" if d else ""))
    sys.exit(1)


# ---------------------------------------------------------------- the recorded waveform
# A slow continuous two-finger drag: sparse-ish events, near-constant small deltas, ~765ms long —
# the same recorded shape test_wheel replays as SLOW_DRAG, which reads as EXACTLY one step. This
# suite asks the other half of the question: what the travel of that one step FEELS like.
SLOW_DRAG = [[i * 45.0, m] for i, m in
             enumerate([7, 8, 7, 9, 8, 7, 8, 9, 8, 7, 8, 7, 9, 8, 7, 8, 7, 8])]

# One frame of travel on a 900px-tall viewport, and the client's own force→duration map.
FRAME_PX = 900.0

DRIVER = r"""
// ---- the extracted client block ----
__BLOCK__
// ---- the client's force→duration map, mirrored with the shipped defaults (INV-84) ----
const GLIDE_MS = 520, GLIDE_MS_SHARP = 260, VEL_CALM = 40, VEL_SHARP = 480;
function glideDur(v) {
  const f = Math.max(0, Math.min(1, ((+v || 0) - VEL_CALM) / (VEL_SHARP - VEL_CALM)));
  return GLIDE_MS - f * (GLIDE_MS - GLIDE_MS_SHARP);
}

// ---- a deterministic replay of the walk's animator ----
// The wheel listener's own re-time rule (INV-84): a NON-stepping sample whose magnitude rises above
// the running peak re-times the glide in flight to the same goal at the new speed; a sample at or
// below the peak decays the peak 5% and changes nothing.
function replay(env, framePx, frameMs) {
  let pos = 0, goal = framePx;
  let glide = null;                       // {from, dist, dur, t0, curve, endAt, span}
  const samples = [];                     // [t, pos] at every animation frame
  let peak = 0, t = 0;
  const evs = env.slice();
  // the first sample steps one frame from rest (test_wheel pins SLOW_DRAG at exactly one step)
  const start = (dist, want, carry, leftMs, span) => {
    const p = glidePlan({ dist: dist, want: want, span: span, carry: carry, leftMs: leftMs });
    if (!p.dur) { pos += dist; glide = null; return; }
    glide = { from: pos, dist: dist, dur: p.dur, t0: t, curve: glideCurve(p.m),
              endAt: t + p.dur, span: p.span };
  };
  const speedNow = () => {
    if (!glide) return 0;
    const q = Math.max(0, Math.min(1, (t - glide.t0) / glide.dur));
    return glide.dist * glide.curve.dat(q) / glide.dur;
  };
  const advanceTo = (until) => {           // run the animator at a fixed frame cadence
    while (t < until) {
      t = Math.min(until, t + frameMs);
      if (glide) {
        const q = Math.min(1, (t - glide.t0) / glide.dur);
        pos = glide.from + glide.dist * glide.curve.at(q);
        samples.push([t, pos]);
        if (q >= 1) glide = null;
      } else samples.push([t, pos]);
    }
  };
  for (let i = 0; i < evs.length; i++) {
    advanceTo(evs[i][0]);
    const mag = evs[i][1];
    if (i === 0) { peak = mag; start(goal - pos, glideDur(mag), 0, Infinity, 0); continue; }
    if (mag > peak) {
      peak = mag;
      if (glide) {
        const carry = speedNow();
        start(goal - pos, glideDur(peak), carry, glide.endAt - t, glide.span);
      }
    } else peak = Math.max(mag, peak * 0.95);
  }
  advanceTo(t + 3000);                     // let it land
  return { samples: samples, landed: pos, endT: t };
}

const OUT = {};
// GSP2 — m=0 is exactly smoothstep
{
  const c = glideCurve(0);
  OUT.rest = { at0: c.at(0), at1: c.at(1), athalf: c.at(0.5), d0: c.dat(0), d1: c.dat(1) };
}
// GSP3 — monotonic, never above 1, over the whole allowed entry range
{
  let worstSlope = Infinity, worstOver = 0;
  for (let k = 0; k <= 20; k++) {
    const c = glideCurve(k / 10);          // 0 .. 2.0
    for (let j = 0; j <= 200; j++) {
      const tt = j / 200;
      worstSlope = Math.min(worstSlope, c.dat(tt));
      worstOver = Math.max(worstOver, c.at(tt) - 1);
    }
  }
  OUT.mono = { worstSlope: worstSlope, worstOver: worstOver };
  OUT.clamped = { above: glideCurve(9).m, below: glideCurve(-4).m };
}
// GSP4 — the curve enters at the speed it was handed
{
  const dist = 450, want = 400, span = 900, carry = 1.2, leftMs = 900;
  const p = glidePlan({ dist: dist, want: want, span: span, carry: carry, leftMs: leftMs });
  const entry = dist * glideCurve(p.m).dat(0) / p.dur;    // px/ms the new curve leaves at
  OUT.entry = { asked: carry, got: entry, m: p.m, dur: p.dur };
}
// GSP5 — a carry pushing the other way starts from rest
{
  const p = glidePlan({ dist: 450, want: 400, span: 900, carry: -1.2, leftMs: 900 });
  OUT.backward = p.m;
}
// GSP6 — a re-time may only bring the landing nearer
{
  const near = glidePlan({ dist: 450, want: 520, span: 900, carry: 0.5, leftMs: 120 });
  const far  = glidePlan({ dist: 450, want: 520, span: 900, carry: 0.5, leftMs: 9000 });
  OUT.deadline = { clamped: near.dur, free: far.dur };
}
// GSP7/GSP8 — the recorded slow drag
OUT.drag = replay(__ENV__, __FRAME__, 16.7);
console.log(JSON.stringify(OUT));
"""

src = (DRIVER.replace("__BLOCK__", BLOCK)
       .replace("__ENV__", json.dumps(SLOW_DRAG))
       .replace("__FRAME__", repr(FRAME_PX)))
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
    f.write(src)
    path = f.name
run = subprocess.run([NODE, path], capture_output=True, text=True)
if run.returncode != 0:
    check("GSP the extracted block runs in node", False, run.stderr.strip()[:400])
    for n, s, d in results:
        print(f"{s}  {n}" + (f"   — {d}" if d else ""))
    sys.exit(1)
OUT = json.loads(run.stdout)

# ---------------------------------------------------------------- GSP2
r = OUT["rest"]
check("GSP2 EX-GLIDE a glide from rest is unchanged — m=0 is exactly smoothstep, both ends soft",
      abs(r["at0"]) < 1e-9 and abs(r["at1"] - 1) < 1e-9 and abs(r["athalf"] - 0.5) < 1e-9
      and abs(r["d0"]) < 1e-9 and abs(r["d1"]) < 1e-9,
      f"{r}")

# ---------------------------------------------------------------- GSP3
mo = OUT["mono"]
check("GSP3 INV-39 every entry speed in range keeps the curve monotonic — it cannot overshoot",
      mo["worstSlope"] >= -1e-9 and mo["worstOver"] <= 1e-9,
      f"least slope {mo['worstSlope']:.4f}, worst overshoot {mo['worstOver']:.6f}")
cl = OUT["clamped"]
check("GSP3 an out-of-range entry speed is clamped into the safe band, never trusted raw",
      cl["above"] == 2 and cl["below"] == 0, f"{cl}")

# ---------------------------------------------------------------- GSP4
en = OUT["entry"]
check("GSP4 EX-GLIDE the new curve leaves at the speed the running glide was at (no dead stop)",
      abs(en["got"] - en["asked"]) < 1e-6,
      f"asked {en['asked']} px/ms, curve leaves at {en['got']:.6f} (m={en['m']:.4f})")

# ---------------------------------------------------------------- GSP5
check("GSP5 a carry pushing the other way starts from rest rather than lurching backward",
      OUT["backward"] == 0, f"m={OUT['backward']}")

# ---------------------------------------------------------------- GSP6
dl = OUT["deadline"]
check("GSP6 EX-GLIDE a re-time may only bring the landing NEARER, never push it out",
      dl["clamped"] <= 120 + 1e-9 and dl["free"] > dl["clamped"],
      f"kept deadline {dl['clamped']}ms vs free {dl['free']}ms")

# ---------------------------------------------------------------- GSP7 the reported defect
# The travel must never stall mid-frame. Walk the sampled positions: from the first frame that
# actually moves until the landing, no window may crawl below a floor share of the travel's own
# average speed. The old curve dropped to a true 0 px/ms at every re-time — four or five times
# inside this one drag — which is what the eye read as steps.
dr = OUT["drag"]
S = dr["samples"]
moving = [i for i in range(1, len(S)) if abs(S[i][1] - S[i - 1][1]) > 1e-9]
STALL_FLOOR = 0.12          # share of the travel's own mean speed a frame may not fall below
worst = None
if moving:
    a, b = moving[0], moving[-1]
    span_px = abs(S[b][1] - S[a - 1][1])
    span_ms = S[b][0] - S[a - 1][0]
    mean = span_px / span_ms if span_ms else 0
    # ignore the last 6% of the travel: a soft landing is the point, not a stall
    tail = S[b][1] - 0.06 * (S[b][1] - S[a - 1][1])
    for i in range(a, b + 1):
        if S[i][1] >= tail:
            break
        v = abs(S[i][1] - S[i - 1][1]) / (S[i][0] - S[i - 1][0])
        if worst is None or v < worst[0]:
            worst = (v, S[i][0], S[i][1])
    check("GSP7 EX-GLIDE the slow drag never stalls mid-frame (his 2026-07-27 report)",
          worst is not None and worst[0] >= STALL_FLOOR * mean,
          f"slowest frame {worst[0]:.4f} px/ms at t={worst[1]:.0f}ms, "
          f"floor {STALL_FLOOR * mean:.4f} (mean {mean:.4f})" if worst else "no travel sampled")
else:
    check("GSP7 EX-GLIDE the slow drag never stalls mid-frame (his 2026-07-27 report)",
          False, "the replay never moved")

# ---------------------------------------------------------------- GSP8 bounded landing
# One frame must stay one gesture's worth of travel. The calm glide is 520ms; a drag that re-times
# five times may stretch it a little, never fold it into a second of crawling.
BOUND_MS = 520 * 1.25
land_t = S[moving[-1]][0] - S[moving[0] - 1][0] if moving else 0
check("GSP8 INV-84 one frame lands inside a bounded time, however often the drag re-times",
      moving and land_t <= BOUND_MS and abs(dr["landed"] - FRAME_PX) < 1.0,
      f"travel took {land_t:.0f}ms (bound {BOUND_MS:.0f}ms), landed at {dr['landed']:.2f} "
      f"of {FRAME_PX:.0f}")

Path(path).unlink(missing_ok=True)

# ---------------------------------------------------------------- report
for n, s, d in results:
    print(f"{s}  {n}" + (f"   — {d}" if d else ""))
bad = sum(1 for _, s, _ in results if s == "FAIL")
print(f"\n{len(results) - bad} passed / {bad} failed")
sys.exit(1 if bad else 0)
