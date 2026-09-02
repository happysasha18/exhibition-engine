#!/usr/bin/env python3
"""PASS-VOICE-DOOR-SNAP — his own report, checked against the real code: "sometimes I don't see
voice-leading, especially colors."

Run: python3 tests/test_pass_voice_cadence_walk.py

THE MECHANISM (`engine/assets/pass-layer.js`). `runFrame`'s cadence branch calls `cadenceHandles`
every frame an interruption is walking to its door, then `playFrame(rec, ..., walk.handles)` — the
fourth argument, `hold`, is truthy for exactly those frames. Inside `playFrame`'s per-voice loop,
the PRIMARY voice (the score's line-0 "miracle") is handed `hold` directly — the handles
`cadenceHandles` walked smoothly from where the primary stood to its own door, over the cadence's
own budget (`cadenceStart`'s `from`/`to`, up to `CADENCE_MAX` = 2000 ms). Before this repair, EVERY
OTHER voice was handed `doorHandles(rec, v, cadence.door)` instead — the door's value OUTRIGHT, on
the very first cadence frame, with no walk at all. The entry-door contract (`standsOver`, read in
`frameState`) already requires a voice standing over another to be ABSENT at its own door — that
part was never wrong — but absent-over-the-cadence's-own-budget and absent-in-this-one-frame are two
different laws, and only the primary ever got the first one. A colour-carrying accompaniment
visible the instant before an interruption (a swipe, the settle-rest road, the finish-rest road —
every one of them calls `cancel`, which calls `cadenceStart`) blinked out in one frame while the
primary kept walking for up to two seconds: his "sometimes I don't see voice-leading" from the
renderer's own numbers, not a description this file invented.

THE FIX. `cadenceStart` now freezes a `cadenceFrom`/`cadenceTo` pair on every OTHER live voice too,
the same way it always froze `from`/`to` for the primary. `cadenceHandles` walks them on the SAME
shared `u` (the cadence's own elapsed-over-budget fraction) through the SAME per-handle envelope
mechanism (`envelopeFor`) the primary already used — no new curve, no new number. `playFrame` reads
`v.cadenceWalked` in place of the old instant `doorHandles` snap; `cadenceLand`'s own final frame
(which wants every voice AT its door exactly, not mid-walk) clears it first, so the landing frame is
untouched.

THE PROOF BELOW is not a screenshot: it drives the real host through a real, planner-composed score
(`boxfold`, `REAL_SCORES` in `tests/test_pass_hang.py`, cast [boxfold, matter, strata-light] — not
hand-typed) with a real browser, waits for `arrival`'s own `presence` handle (strata-light, the
LIGHT-COLOUR accompaniment — his own words were "especially colors") to stand near its own peak
mid-window, fires the SAME public interruption entry point a swipe uses
(`window.__exPass.adapter.interrupt`), and reads the renderer's own diagnostic surface
(`host.report().stack`) a short interval later, comfortably inside the score's own 500 ms cadence
budget and nowhere near its landing. `arrival`'s own window ends exactly where the primary's own
door does (both at 7.377 s, the pass's own end) — chosen over `matter` for exactly this reason: its
own window never closes early on the cadence's own compressed clock, so it stays genuinely live for
the cadence's WHOLE walk and the sampled instant is never confused with the ordinary, correct
"this voice's window has simply ended" road.

Neither `boxfold`'s nor `strata-light`'s cue names a per-handle cadence curve, so both the primary's
own `mix` handle and the accompaniment's own `presence` handle walk on the identical default
envelope (`CURVES.smooth`) driven by the identical shared `u` — so the FRACTION of its own
door-bound distance each has covered by the sampled instant must read the same, to the frame's own
precision, once the fix is in place. Before it, the accompaniment's fraction reads ~1 (already at
its door) regardless of how little of the budget has actually elapsed, while the primary's own
fraction reads whatever `u` actually is — the mismatch between the two fractions is the whole bug,
read as one number rather than asserted.

THE RED-ON-BUG ROW reproduces the pre-repair behaviour without touching git history: it takes this
worktree's OWN already-built (fixed) `pass-layer.js`, reverts the one expression the repair changed
back to the bare `doorHandles(...)` snap it replaced, serves that as a second site, and drives the
identical measurement through it. A defect this narrow does not need a second browser flavour or a
second score to prove; it needs the one line put back.
"""
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 1000, 900

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- the real score, read off disk
# `tests/test_pass_hang.py` already carries this exact composer-derived, three-voice score
# (`REAL_SCORES["boxfold"]`, cast [boxfold, matter, strata-light]) as its own `REAL_SCORE_JSON`
# literal. That file is a flat script that runs its whole browser suite on import, so it is not
# something this file can import — the ONE JSON block this row needs is pulled off its source text
# instead, unexecuted, which is the same "found by the real composer, never hand-typed" score
# either way.
_HANG_SRC = (HERE / "test_pass_hang.py").read_text(encoding="utf-8")
_m = re.search(r'"boxfold":\s*r\'\'\'(.*?)\'\'\'', _HANG_SRC, re.S)
if _m is None:
    print("PASS-VOICE-DOOR-SNAP could not find REAL_SCORE_JSON['boxfold'] in test_pass_hang.py")
    sys.exit(1)
BOXFOLD_SCORE = json.loads(_m.group(1))

check("PASS-VOICE-DOOR-SNAP the real score casts a primary and a colour-carrying accompaniment",
      any(c["id"] == "pivot" and c["instrument"]["id"] == "boxfold" for c in BOXFOLD_SCORE["cues"])
      and any(c["id"] == "arrival" and c["instrument"]["id"] == "strata-light"
              for c in BOXFOLD_SCORE["cues"]),
      "this row's whole measurement stands on `pivot` (primary) and `arrival` — strata-light, the "
      "LIGHT-COLOUR accompaniment his own report names ('especially colors') — being exactly what "
      "REAL_SCORE_JSON['boxfold'] casts")

# ---------------------------------------------------------------- bake once
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_voicedoor_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
LAYER_FIXED = (TMP / "pass-layer.js").read_text(encoding="utf-8")

check("PASS-VOICE-DOOR-SNAP mechanism · every voice's own from/to walk is frozen at cadence start, "
      "not only the primary's",
      all(s in LAYER_FIXED for s in ["v.cadenceFrom", "v.cadenceTo", "v.cadenceWalked"]),
      "cadenceStart must build the same from/to pair for every other voice that it always built "
      "for the primary")

check("PASS-VOICE-DOOR-SNAP mechanism · a cadence frame reads a voice's own walked handles in "
      "place of the instant door snap",
      "hold ? (v.cadenceWalked || doorHandles(rec, v," in LAYER_FIXED,
      "the old line handed every non-primary voice `doorHandles(...)` outright; the walked value "
      "must be read first, with the snap kept only as the landing frame's own fallback")

# ---------------------------------------------------------------- the buggy twin, by one reverted line
# The one expression the repair changed, read back to what it replaced — not a second hand-typed
# copy of it, so the needle and the replacement can never quietly drift apart from the real diff.
FIXED_NEEDLE = 'hold ? (v.cadenceWalked || doorHandles(rec, v, (rec.cadence && rec.cadence.door) || "out"))'
BUGGY_LINE = 'hold ? doorHandles(rec, v, (rec.cadence && rec.cadence.door) || "out")'
NEEDLE_COUNT = LAYER_FIXED.count(FIXED_NEEDLE)

TMP_BUG = None
if NEEDLE_COUNT == 1:
    TMP_BUG = Path(tempfile.mkdtemp(prefix="synth_voicedoor_bug_"))
    shutil.copytree(TMP, TMP_BUG, dirs_exist_ok=True)
    (TMP_BUG / "pass-layer.js").write_text(
        LAYER_FIXED.replace(FIXED_NEEDLE, BUGGY_LINE, 1), encoding="utf-8")

# ---------------------------------------------------------------- browser harness (test_pass_hang.py's own pattern)
HOOKS = """window.HOOKS = function () {
  var A = window.__exPass.adapter;
  return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
           hangGeometry: A.hangGeometry, handoff: A.handoff };
};
0"""


def js(br, expr):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % expr))


def wait_state(br, want, tries=80):
    for _ in range(tries):
        if js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(0.05)
    return False


def enter(br, base):
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    br.key("ArrowDown")            # the one step that makes the client fetch pass-layer.js
    for _ in range(30):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            br.evaluate(HOOKS)
            return True
        br.sleep(0.2)
    return False


def declare_and_offer(br, a, b, cause, score_obj):
    br.evaluate("window.__hangScore = " + json.dumps(score_obj) + "; 0")
    return js(br, """
      var A = document.querySelector('.exh-frame[data-id="%s"]');
      var B = document.querySelector('.exh-frame[data-id="%s"]');
      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                 kind:'step', cause:'%s', velocity:0,
                                                 score: window.__hangScore || null});
      window.__cmd = cmd;
      var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
      return {got: !!cmd, took: took, gen: cmd ? cmd.gen : null};
    """ % (a, b, cause))


READ_VOICES = """
  var rep = window.__exPass.host.report();
  var m = null, p = null;
  (rep.stack || []).forEach(function (v) {
    if (v.id === 'arrival') m = v;
    if (v.id === 'pivot') p = v;
  });
  return {state: rep.state,
          cadence: !!rep.cadence, ended: rep.cadence ? rep.cadence.ended : null,
          mLive: m ? !!m.live : null, mPresence: (m && m.handles) ? m.handles.presence : null,
          pMix: (p && p.handles) ? p.handles.mix : null};
"""


def measure_snap(br, base, tag):
    """Run the real, three-voice `boxfold` score to a resting departure, run it, wait for
    `arrival` (strata-light)'s own presence to stand near its own peak, fire the same public
    interruption a swipe uses, and read both the primary's and the accompaniment's own handles a
    few frames later, well inside the cadence's own budget. Returns a dict of readings, or None
    with the reason logged by the caller.

    `arrival`'s own window is [3.2274, 7.377] s of this 7.377 s pass — its own upper edge is
    exactly `pivot` (the primary)'s own door second, since `pivot`'s window spans the whole pass.
    So the cadence's own compressed clock, which always walks toward THAT door second, can never
    carry `arrival` past its own window edge before the cadence itself lands — it stays genuinely
    live for the cadence's whole walk, so a sample taken anywhere inside the budget is never
    confused with the separate, correct "this voice's window simply ended" road, the one voices
    with an earlier-closing window (`matter`) legitimately take instead."""
    # Arming is retried whole (a fresh navigate each time), not just polled longer in place: under
    # a loaded machine (this suite is one of several run_all.py starts at once) the FIRST load can
    # wedge in a state `enter()`'s own in-page polling never recovers from, and a fresh navigate is
    # what a real reload gives a page that seems stuck, not a longer wait on the same one.
    armed, works = False, []
    for _ in range(3):
        br.navigate(base + "/")
        br.clear_storage()
        br.navigate(base + "/")
        br.sleep(0.8)
        armed = enter(br, base)
        works = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                       ".map(function(e){return e.dataset.id;}).slice(0,2);")
        if armed and len(works) == 2 and all(works):
            break
    if not (armed and len(works) == 2 and all(works)):
        return None, f"the walk never registered a host, or hung no pair: armed={armed} works={works}"
    a, b = works
    # A cold session occasionally answers `declare` before its own DOM has settled — the same
    # startup jitter `enter()`'s own retry loops already ride out elsewhere in this harness, just
    # met one call later. Retried a few times, short backoff, before this row gives up on it.
    r, running = None, False
    for _ in range(4):
        r = declare_and_offer(br, a, b, tag, BOXFOLD_SCORE)
        running = r["took"] and wait_state(br, "running", tries=20)
        if running:
            break
        br.sleep(0.3)
    if not running:
        return None, f"the real score never started running: {r}"

    # Poll for the accompaniment's own presence near its peak (its window's own midpoint, ~5.30 s
    # of the 7.377 s pass). Real time, no clock pin — the cadence's own internal walk always runs
    # on the wall clock regardless of a pin, so this row measures exactly what a real interruption
    # meets.
    baseline = None
    for _ in range(160):
        st = js(br, READ_VOICES)
        if st["mLive"] and st["mPresence"] is not None and st["mPresence"] > 0.8:
            baseline = st
            break
        br.sleep(0.05)
    if baseline is None:
        return None, "the accompaniment's own presence never rose above 0.8 while live"

    # The interrupt call and the pre-interrupt reading stand in the SAME synchronous JS turn, so
    # no frame can have been drawn between the reading and the cadence actually starting.
    before = js(br, "var rep=window.__exPass.host.report();"
                     "var m=null,p=null;"
                     "(rep.stack||[]).forEach(function(v){"
                     " if(v.id==='arrival') m=v; if(v.id==='pivot') p=v;});"
                     "var before={mPresence:(m&&m.handles)?m.handles.presence:null,"
                     " pMix:(p&&p.handles)?p.handles.mix:null, mLive:m?!!m.live:null};"
                     "window.__exPass.adapter.interrupt('%s-mid'); return before;" % tag)

    # The EARLIEST reading that actually reflects a drawn cadence frame — not the latest reachable
    # one: the bug this row exists to catch is at its most visible in the cadence's own first
    # frames (his own report was "sometimes", not "at the very end"), and `arrival`'s own presence
    # asymptotically converges toward the primary's own fraction as u approaches 1 even on the
    # pre-repair line (both readings are heading toward "fully at the door" by then), which would
    # quietly hide the mismatch behind a late sample. A handful of small waits, not one guessed
    # delay, rides out whatever CDP round-trip and scheduling jitter a real, possibly loaded
    # machine adds; the first one that lands inside a live, unlanded cadence is kept.
    after = None
    for step in (0.0, 0.005, 0.01, 0.02, 0.03):
        if step:
            br.sleep(step)
        st = js(br, READ_VOICES)
        if st["cadence"] and st["ended"] is False and st["mLive"]:
            after = st
            break

    # A second `interrupt()` while a cadence is already running is a no-op (`cancel`'s own
    # `if (cur.cadence) { ...; return; }`, no `immediate` flag) — so this just waits out the
    # cadence's own natural landing, and the reading right after is the accompaniment AT REST,
    # for the entry-door contract check (ROW_LAND): the walk changed, the contract did not.
    js(br, "window.__exPass.adapter.interrupt('%s-done'); return null;" % tag)
    landed = wait_state(br, "idle", tries=60)
    at_rest = js(br, READ_VOICES)["mPresence"] if landed else None

    if not (before["mLive"] and before["mPresence"] is not None and before["pMix"] is not None):
        return None, f"the pre-interrupt reading was incomplete: {before}"
    if after is None:
        return None, "no reading caught the accompaniment still live inside an unlanded cadence"
    if after["mPresence"] is None or after["pMix"] is None:
        return None, f"the post-interrupt reading was incomplete: {after}"
    return {"pres_before": before["mPresence"], "pres_after": after["mPresence"],
            "mix_before": before["pMix"], "mix_after": after["pMix"],
            "landed": landed, "pres_at_rest": at_rest}, None


ROW_MECH = ("PASS-VOICE-DOOR-SNAP row 1 · interrupted mid-window, the colour-carrying accompaniment "
            "walks the SAME shared fraction of its own door-bound distance the primary voice walks")
ROW_LAND = ("PASS-VOICE-DOOR-SNAP row 2 · the accompaniment still lands exactly on its own door "
            "once the cadence completes — the entry-door contract is kept, only the walk changed")
ROW_BUG = ("PASS-VOICE-DOOR-SNAP red-on-bug · the reverted line snaps the same accompaniment to its "
           "door in the cadence's own first sampled frame, regardless of how little of the budget "
           "has elapsed")

ROWS = [ROW_MECH, ROW_LAND, ROW_BUG]

if not chrome_available():
    for r in ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
elif TMP_BUG is None:
    for r in ROWS:
        skip(r, f"the fixed line was not found exactly once in the built pass-layer.js "
                f"(found {NEEDLE_COUNT}); the mechanism string this row reverts to build the "
                f"pre-repair twin has drifted")
else:
    # ---- the fixed build: a small mismatch, and a clean landing -------------------------------
    with serve(TMP) as base:
        with Browser(width=VW, height=VH) as br:
            reading, why = measure_snap(br, base, "voice-fixed")
    if reading is None:
        skip(ROW_MECH, why)
        skip(ROW_LAND, why)
    else:
        primary_frac = ((reading["mix_after"] - reading["mix_before"])
                        / max(1.0 - reading["mix_before"], 1e-9))
        companion_frac = ((reading["pres_before"] - reading["pres_after"])
                          / max(reading["pres_before"], 1e-9))
        mismatch = abs(companion_frac - primary_frac)
        check(ROW_MECH, mismatch < 0.1,
              f"primary walked {primary_frac:.4f} of its own door distance, the accompaniment "
              f"{companion_frac:.4f} of its own — mismatch {mismatch:.4f}, presence "
              f"{reading['pres_before']:.4f} -> {reading['pres_after']:.4f}, mix "
              f"{reading['mix_before']:.4f} -> {reading['mix_after']:.4f}")

        # The SAME session, continued past the mismatch reading above: `measure_snap` already let
        # the cadence land naturally (a second `interrupt()` while one is running is a no-op, so
        # `wait_state(..., "idle")` there waits out the real landing) and read the accompaniment's
        # own presence at rest. One session proves both the walk changed AND the contract it walks
        # toward did not — no second browser needed, and nothing left to race.
        check(ROW_LAND, reading.get("landed") and reading.get("pres_at_rest") is not None
              and abs(reading["pres_at_rest"]) < 0.02,
              f"landed={reading.get('landed')}, the accompaniment's own presence at rest after "
              f"the cadence reads {reading.get('pres_at_rest')} — the contract still asks for "
              f"exactly 0")

    # ---- the pre-repair twin: the same measurement must reproduce the snap -------------------
    with serve(TMP_BUG) as bug_base:
        with Browser(width=VW, height=VH) as br3:
            reading, why = measure_snap(br3, bug_base, "voice-bug")
    if reading is None:
        skip(ROW_BUG, why)
    else:
        primary_frac = ((reading["mix_after"] - reading["mix_before"])
                        / max(1.0 - reading["mix_before"], 1e-9))
        companion_frac = ((reading["pres_before"] - reading["pres_after"])
                          / max(reading["pres_before"], 1e-9))
        mismatch = abs(companion_frac - primary_frac)
        check(ROW_BUG, mismatch > 0.3,
              f"primary walked {primary_frac:.4f} of its own door distance, the accompaniment "
              f"{companion_frac:.4f} of its own — mismatch {mismatch:.4f} — reproduced against "
              f"the exact pre-repair line iff this mismatch stands well over the 0.1 the "
              f"repaired build must read under")

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
