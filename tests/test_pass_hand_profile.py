#!/usr/bin/env python3
"""EX-HAND U5 — Requirement 40's own hand-as-clock: pass-hand.js's `clockCurve`/`clockProfile`.
Run: python tests/test_pass_hand_profile.py

Requirement 40 is the darkroom, and the darkroom is unbuilt. What this unit builds is the one shelf
the plan carves out of it now: a pure, stateless response curve — hand position in, progress out —
that pass-hand.js publishes for driving `unfold`'s progress pin (`pass-layer.js`'s own testing seam,
`configure({progressPin})`) across its FULL declared range. It is a second, separate road from the
chart law U3 already shipped (`lean`'s R/8 ceiling on the walk's own drag): nothing here is wired to
a listener, and the shipped walk never reaches this curve on its own. A test drives it directly.

ROWS 1/2/5 drive a real `unfold` crossing, offered straight to `pass-layer.js`'s own host (the
diagnostics-only seam 01a-pass.js documents as such — "adapter and layer are a TESTING seam... let a
conformance row construct a real command and drive the host directly") — never through the walk's
own composer, and never touching a `pass-inst-*.js` file. Rows 3/4 release it and read the layer's
OWN cadence machinery, unmodified, resolving the handle home. Row 6 is a second, ordinary browser
that never once calls into any of this: the shipped drag's R/8 lean ceiling, driven the way U3 always
drove it.

WHAT ROW 2 (criterion 10, equal felt change) READS, AND WHY IT CANNOT BE A COMPARISON OF RAW
PROGRESS. `unfold`'s own `mix` handle is a bare passthrough of `progress` (`unfold_cue`'s own node,
`source: "progress"`), so reading `mix` back is reading exactly what was pinned — an affine
(straight-line) drive of N equally spaced hand positions therefore ALWAYS produces perfectly equal
`mix` steps, the mathematical floor no curved drive can beat. Comparing raw `mix` spreads would make
the straight line win by construction, every time. What criterion 10 asks for — equal hand movement,
equal FELT change — is a claim about a THIRD quantity, the felt magnitude of a change, and this row
supplies the one fixed, generic model criterion 10's own text names: "perception is logarithmic in
many dimensions." `felt(p) = ((1+K)^p - 1) / K` is that model's own inverse, paired with
`clockCurve`'s `log(1+K*u)/log(1+K)` by construction (`felt(clockCurve(u)) == u`, exactly, for the
same `K`) — never read off `unfold`'s own shader, which is exactly what the brief this unit answers
to says has no curve to compare against. Both `mix` sequences are read off the SAME running
transaction in the SAME run; `felt` is arithmetic this file does on numbers it read off `report()`,
the same road tests/test_pass_feel.py already takes to turn a raw reading into a measured step.
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

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def wait_for(br, expr, timeout=6.0, step=0.05):
    """Poll a JS expression until it returns truthy (or the deadline) — no fixed-sleep races."""
    import time
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    return val


ROWS = [
    "EX-HAND-CLOCK row1 Requirement 40 c1 the hand as clock: a drag of equal hand steps writes "
    "monotone values into unfold's progress pin, read back through report(), standing exactly at "
    "both ends of the handle's own declared range",
    "EX-HAND-CLOCK row2 Requirement 40 c10 equal felt change: the drawn profile's felt-step spread "
    "on the same handle is strictly below the straight line's, both read in the same run",
    "EX-HAND-CLOCK row3 Requirement 40 c2/c3 the release: the pin clears, the layer's own cadence "
    "plays (not forced, within the exhale's own ~700 ms budget) and report() names the door it "
    "resolved to",
    "EX-HAND-CLOCK row4 Requirement 40 c11 nothing snaps: the resolve passes through intermediate "
    "values on its way to the resting door rather than jumping there",
    "EX-HAND-CLOCK row5 Requirement 40 c9 the profile: polarity, curve, range, neutral and resting "
    "point all read back off the one published object",
    "EX-HAND-CLOCK row6 the walk is unchanged: with the clock drive never touched, a full "
    "press-drag-release on the standing work still moves mix by no more than R/8 and returns",
]

# ---------------------------------------------------------------- bake once, the drawing layer on
build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}

TMP = Path(tempfile.mkdtemp(prefix="synth_pass_hand_profile_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

DATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
VER = str(DATA["version"])
PICK = DATA["door"]["pool"][0]["id"]
WALK = json.dumps(json.dumps({"v": VER, "pick": PICK, "shown": 10}))

# R, read off the instrument's own served file — never typed in, the same road pass-hand.js's own
# `readHandle` already takes for `mix`/`tilt`.
UNFOLD_SRC = (TMP / "pass-inst-unfold.js").read_text(encoding="utf-8")


def declared_span(handle):
    m = re.search(r"\b%s\s*:\s*\{\s*min\s*:\s*([0-9.]+)\s*,\s*max\s*:\s*([0-9.]+)" % re.escape(handle),
                   UNFOLD_SRC)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


MIX_MIN, MIX_MAX = declared_span("mix") or (0.0, 1.0)

# ---------------------------------------------------------------- browser plumbing (test_pass_hand.py's own)
HAND_READY = "!!(window.__exPass && window.__exPass.hand && window.__exPass.hand())"
LAYER_READY = "!!(window.__exPass && window.__exPass.host)"
WORK = ".exh-frame img.work"


def hand_report(br):
    return json.loads(br.evaluate("JSON.stringify(window.__exPass.hand().report())"))


def host_report(br):
    return json.loads(br.evaluate("JSON.stringify(window.__exPass.host.report())"))


def room(br, base, tempo="0.2"):
    """A stored walk straight into the room, diagnostics on — READY by condition, not a fixed sleep
    (tests/test_pass_hand.py's own `room`)."""
    br.navigate(base + "/")
    br.evaluate(f"localStorage.setItem('ex.exhibition', {WALK})")
    br.evaluate(f"localStorage.setItem('ex-tempo','{tempo}')")
    br.evaluate("sessionStorage.setItem('ex-pass', JSON.stringify({diagnostics: 'on'}))")
    br.reload()
    for _ in range(40):
        br.sleep(0.15)
        if br.evaluate("document.documentElement.classList.contains('ex-walk')"
                       "&&document.querySelectorAll('.exh-frame').length>0"
                       "&&scrollY===0"):
            break
    br.sleep(0.3)


def fire(br, selector, kind_of_event, pointer_kind, nx=0.5, ny=0.5, pointer_id=9):
    """One synthetic PointerEvent at a normalised (nx, ny) fraction of `selector`'s own box
    (tests/test_pass_hand.py's own `fire`)."""
    return br.evaluate(
        "(()=>{const el=document.querySelector(%s);if(!el)return false;"
        "const r=el.getBoundingClientRect();"
        "const x=r.left+r.width*%s, y=r.top+r.height*%s;"
        "el.dispatchEvent(new PointerEvent(%s,{pointerId:%s,pointerType:%s,"
        "clientX:x,clientY:y,isPrimary:true,bubbles:true,cancelable:true}));"
        "return true;})()"
        % (json.dumps(selector), nx, ny, json.dumps(kind_of_event), pointer_id, json.dumps(pointer_kind)))


def verb_expr(name):
    return "(()=>window.__exPass.hand().report().verb===%s)()" % json.dumps(name)


def wait_span(br, handle, timeout=6.0):
    ok = wait_for(br, "(()=>!!window.__exPass.hand().handleSpan('unfold',%s))()" % json.dumps(handle),
                  timeout=timeout)
    if not ok:
        return None
    return json.loads(br.evaluate(
        "JSON.stringify(window.__exPass.hand().handleSpan('unfold',%s))" % json.dumps(handle)))


# ---------------------------------------------------------------- the score: one unfold voice
# Modelled on tests/test_pass_unfold.py's own `unfold_cue`/`unfold_score` — the real schema the host
# reads — trimmed to what this bench needs: no second voice, no camera pan, a `mix` handle wired
# straight to `progress` (`source: "progress"`) so `report().handles.mix` echoes exactly what this
# file pins, and no `cue.cadence` named for any handle, so `envelopeFor` resolves every one of them
# through the fleet's own default, `smooth` — the same envelope the crossing already uses, built
# fresh nowhere by this file.
DURATION_MS = 4000
WITHIN_MS = 700   # Requirement 40 c3's own "about 700 ms"
DIE = 1.0


def _static(v):
    return {"op": "static", "value": v}


def unfold_cue(id_a, id_b):
    p = {"tilt": 0.5, "shade": 1, "depth": 0.5, "stagger": 0.34, "panels": 1, "mask": 0,
         "field": 0, "parquetPeriod": 0.5, "parquetTurn": 0}
    nodes = {"u-mix": {"source": "progress"}, "u-clock": {"source": "time"}}
    tracks = {"mix": {"node": "u-mix"}, "clock": {"node": "u-clock"}}
    for k, v in p.items():
        nodes["u-" + k] = _static(v)
        tracks[k] = {"node": "u-" + k}
    return {
        "id": "unfold-main", "instrument": {"id": "unfold", "api": 1},
        "voice": "letter", "roles": ["disassembly", "mystery", "assembly"],
        "levels": ["CELL", "CELL CONTENT"],
        "levelOwnership": {"CELL": "owns", "CELL CONTENT": "owns"},
        "window": [0, DURATION_MS / 1000.0], "works": [id_a, id_b], "stack": 0,
        "cameraAuthority": "stage",
        "doors": {"in": {"handle": "mix", "value": 0, "measured": True},
                  "out": {"handle": "mix", "value": 1, "measured": True}},
        "nodes": nodes, "tracks": tracks,
        "resources": {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0,
                      "programs": 1, "passes": 1, "bytesEstimate": 0, "variant": "standard"},
    }


def unfold_score(id_a, id_b):
    cue = unfold_cue(id_a, id_b)
    res = {"textures": 0, "textureSlots": 2, "framebuffers": 0, "pingPong": 0, "programs": 1,
           "passes": 1, "bytesEstimate": 0}
    return {
        "schema": 2,
        "intent": "tests/test_pass_hand_profile.py's own bench: the hand drives unfold's progress "
                  "pin across its full range",
        "pair": {"a": id_a, "b": id_b}, "seed": DIE, "duration": DURATION_MS,
        "direction": "a-to-b",
        "interruption": {"withinMs": WITHIN_MS, "resolve": "nearest-door"},
        "failLand": "arrive",
        "camera": {"owner": "stage", "rests": "b",
                   "track": [{"at": "b", "pan": {"x": 0, "y": 0}, "logScale": 0,
                              "pitch": 0, "yaw": 0, "roll": 0, "fov": None, "owner": "stage"}]},
        "cues": [cue],
        "quality": {v: {"renderScale": None, "cues": {cue["id"]: {"resources": dict(res, variant=v)}}}
                    for v in ("lean", "standard", "rich")},
        "provenance": {"source": "lab/effects/unfold.js's own declared defaults and constants",
                       "measuredAt": None, "by": "tests/test_pass_hand_profile.py"},
    }


# felt(p) = ((1+K)^p - 1) / K — the fixed inverse of pass-hand.js's own `clockCurve`
# (log(1+K*u)/log(1+K)), for the SAME K (15) both files carry as their own paired constant. Neither
# number is read off `unfold`; `felt` never touches a `pass-inst-*.js` file, and it exists only to
# turn a raw `mix` reading into criterion 10's own "felt" magnitude.
CLOCK_K = 15.0


def felt(p):
    return ((1.0 + CLOCK_K) ** p - 1.0) / CLOCK_K


def spread(vals):
    deltas = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    return max(deltas) - min(deltas)


if not chrome_available():
    for r in ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # ---- rows 1, 2, 3, 4, 5 — a real `unfold` crossing, driven entirely off the hand's clock ---
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            ready = bool(wait_for(br, HAND_READY)) and bool(wait_for(br, LAYER_READY, timeout=8.0))
            ids = br.evaluate(
                "[...document.querySelectorAll('.exh-frame')].slice(0,2).map(f=>f.dataset.id)")
            id_a, id_b = (ids or [None, None])[0], (ids or [None, None])[1]

            # row 5 — the published profile, read whole
            profile = (json.loads(br.evaluate("JSON.stringify(window.__exPass.hand().clockProfile())"))
                       if ready else None)
            check(ROWS[4],
                  bool(profile) and isinstance(profile.get("polarity"), str)
                  and isinstance(profile.get("curve"), str)
                  and isinstance(profile.get("range"), dict)
                  and isinstance(profile["range"].get("min"), (int, float))
                  and isinstance(profile["range"].get("max"), (int, float))
                  and profile["range"]["min"] < profile["range"]["max"]
                  and isinstance(profile.get("neutral"), (int, float))
                  and isinstance(profile.get("resting"), (int, float)),
                  f"ready={ready} profile={profile}")

            SCORE = json.dumps(unfold_score(id_a, id_b))
            offered = bool(br.evaluate("""(()=>{
              window.__hpGen = (window.__hpGen || 1000) + 1;
              window.__exPass.host.configure({prepareBudgetMs: 120, settleSlackMs: 2000,
                                               progressPin: 0, clockPin: null});
              var hooks = { dock: function(){}, glide: function(){}, curtain: function(){},
                            mark: function(){}, hangGeometry: function(){}, handoff: function(){} };
              var cmd = { gen: window.__hpGen, from: {id: %s}, to: {id: %s}, kind: 'step',
                          cause: 'hand-clock-test', dir: 1, span: 100, velocity: 0,
                          reduced: false, saveData: false, rtl: false,
                          dpr: window.devicePixelRatio || 1,
                          viewport: {w: innerWidth, h: innerHeight},
                          params: {flightMs: {base: %d}, qualityTier: {base: 'standard'}},
                          score: %s };
              return window.__exPass.host.offer(cmd, hooks) === true;
            })()""" % (json.dumps(id_a), json.dumps(id_b), DURATION_MS, SCORE)))
            running = bool(wait_for(br, "(()=>window.__exPass.host.report().state==='running')()",
                                     timeout=8.0))

            # ---- rows 1, 2: N equally spaced hand positions, driven two ways on the same handle ----
            N = 9
            us = [i / (N - 1) for i in range(N)]

            def drive(mode):
                mixes = []
                for u in us:
                    p = (float(br.evaluate("window.__exPass.hand().clockCurve(%r)" % u))
                         if mode == "profile" else u)
                    br.evaluate("window.__exPass.host.configure({progressPin: %r}); 0" % p)
                    m = br.evaluate("window.__exPass.host.report().handles.mix")
                    mixes.append(float(m))
                return mixes

            profile_mix = drive("profile") if running else []
            straight_mix = drive("straight") if running else []

            mono = bool(profile_mix) and all(
                profile_mix[i] <= profile_mix[i + 1] + 1e-9 for i in range(len(profile_mix) - 1))
            ends_ok = bool(profile_mix) and abs(profile_mix[0] - MIX_MIN) < 1e-6 \
                and abs(profile_mix[-1] - MIX_MAX) < 1e-6
            check(ROWS[0],
                  running and mono and ends_ok,
                  f"offered={offered} running={running} profile_mix={profile_mix} "
                  f"declared_span=({MIX_MIN},{MIX_MAX})")

            profile_spread = spread([felt(m) for m in profile_mix]) if profile_mix else None
            straight_spread = spread([felt(m) for m in straight_mix]) if straight_mix else None
            check(ROWS[1],
                  profile_spread is not None and straight_spread is not None
                  and profile_spread < straight_spread,
                  f"profile_spread={profile_spread} straight_spread={straight_spread} "
                  f"profile_mix={profile_mix} straight_mix={straight_mix}")

            # ---- rows 3, 4: release — clear the pin and let it go, the layer's own road only -------
            mid_p = float(br.evaluate("window.__exPass.hand().clockCurve(0.5)")) if running else None
            cadence_seen = None
            samples = []
            resting = None
            idled = False
            if running and mid_p is not None:
                br.evaluate("window.__exPass.host.configure({progressPin: %r}); 0" % mid_p)
                start_mix = float(br.evaluate("window.__exPass.host.report().handles.mix"))
                br.evaluate("window.__exPass.host.configure({progressPin: null}); "
                            "window.__exPass.host.cancel('hand release'); 0")
                for _ in range(800):
                    rep = host_report(br)
                    if rep.get("cadence") and cadence_seen is None:
                        cadence_seen = rep["cadence"]
                    if rep.get("state") != "running":
                        break
                    h = rep.get("handles")
                    if h and "mix" in h:
                        samples.append(float(h["mix"]))
                idled = bool(wait_for(br, "(()=>window.__exPass.host.report().state==='idle')()",
                                       timeout=8.0))
                final_rep = host_report(br)
                final_cadence = final_rep.get("cadence")
                h = final_rep.get("handles")
                resting = h.get("mix") if h else None
            else:
                start_mix = None
                final_cadence = None

            check(ROWS[2],
                  idled and cadence_seen is not None and cadence_seen.get("forced") is False
                  and cadence_seen.get("reason") == "hand release"
                  and cadence_seen.get("door") in ("in", "out")
                  and cadence_seen.get("budget") == WITHIN_MS
                  and final_cadence is not None and final_cadence.get("ended") is True,
                  f"idled={idled} cadence_seen={cadence_seen} final_cadence={final_cadence}")

            distinct = sorted(set(round(s, 6) for s in samples))
            lo = min(start_mix, resting) if (start_mix is not None and resting is not None) else None
            hi = max(start_mix, resting) if (start_mix is not None and resting is not None) else None
            passed_through = (lo is not None
                               and any(lo + 1e-4 < s < hi - 1e-4 for s in samples))
            at_rest = resting is not None and abs(resting - round(resting)) < 1e-6
            check(ROWS[3],
                  idled and at_rest and len(distinct) >= 3 and passed_through,
                  f"idled={idled} start_mix={start_mix} resting={resting} samples_n={len(samples)} "
                  f"distinct_n={len(distinct)} passed_through={passed_through}")

        # ---- row 6 — a second, ordinary browser: the shipped drag, the clock drive never touched ---
        with Browser(width=1280, height=900) as br:
            br.touch(True, 2)
            room(br, base)
            wait_for(br, HAND_READY)
            wait_span(br, "mix")
            fire(br, WORK, "pointerover", "mouse", 0.5, 0.5, 81)
            fire(br, WORK, "pointerdown", "mouse", 0.5, 0.5, 81)
            fire(br, WORK, "pointermove", "mouse", 0.95, 0.5, 81)
            wait_for(br, verb_expr("lean"))
            rep1 = hand_report(br)
            cap = rep1["lean"]["cap"]
            v1 = rep1["lean"]["value"]
            fire(br, WORK, "pointerup", "mouse", 0.95, 0.5, 81)
            wait_for(br, verb_expr("release"))
            returned = wait_for(
                br, "(()=>Math.abs(window.__exPass.hand().report().lean.value)<0.001)()", timeout=6.0)
            check(ROWS[5],
                  cap > 0 and 0 < abs(v1) <= cap + 1e-9 and bool(returned),
                  f"cap={cap} v1={v1} returned={returned}")

# ---------------------------------------------------------------- report
import shutil  # noqa: E402

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
