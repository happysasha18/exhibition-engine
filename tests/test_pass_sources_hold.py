#!/usr/bin/env python3
"""PASS-SOURCES-HOLD (P1.1/A5) — no loading UI inside a live route.

Run: python3 tests/test_pass_sources_hold.py

Root: this наряд's own file:line evidence. `armSources(cmd)` (pass-layer.js) decodes both works'
pictures before an instrument is ever asked to prepare, and until now that wait shared ONE clock
with the instrument's own compute-bound `prepare()` budget — `prepareBudgetMs`, 120ms by default.
A newly-in-view photograph that simply had not finished DOWNLOADING yet (a network wait, not a slow
instrument) timed out exactly as a stalled instrument would, `declineCurrent` fell the crossing to
the plain glide (a DOM-level crossfade of the `<img>` elements themselves), and the glide exposed
whatever the arriving `<img>` was doing on its own — the per-work loading plate
`06-ground-load-doorwarm.js` arms on exactly this condition. Two things on screen both say
"loading" and only one is the bug; this is that one, because it fires MID-ROUTE, not once at the
door.

THE FIX holds instead of dropping: the wait for the pictures is bounded by the transaction's own
outer arithmetic (`duration + slack`, already-clamped values the running watchdog already answers
to — no new numeric constant), and the instrument's own `prepareBudgetMs` starts only once the
pictures are actually in hand.

WHAT THIS FILE MEASURES. One work's real image is held on the wire for a full second — comfortably
past the OLD 120ms budget and comfortably under the NEW bound — by the test's own server (the same
`hold=` mechanism `tests/test_load.py` already drives real image waits through). A real declare+
offer is driven at a real instrument with a real manifest (so `armSources` is genuinely on the road
to takeover), and the row proves: the crossing is not yet declined a third of a second in (the old
budget would already have killed it), it eventually takes over for real once the picture lands (a
real instrument, never a decline to the glide), and no loading plate joins the frame it is still
standing on while any of this happens.
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
VW, VH = 1000, 900
DUR = 2400          # the pass this file measures, in milliseconds — the SAME shape test_pass_hang.py
                    # already reads its own score by, so this file invents no new fixture grammar
HOLD_DELAY = 1.0    # seconds the arriving work's own picture is held on the wire — well past the
                    # OLD 120ms compute budget and well under the transaction's own outer bound below
SETTLE_SLACK_MS = 3000

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROWS = [
    "PASS-SOURCES-HOLD a crossing whose arriving picture is still on the wire is not yet declined "
    "a third of a second in, well past the old compute-only budget",
    "PASS-SOURCES-HOLD the same crossing takes over for real once the picture lands — a real "
    "instrument, never a decline to the plain glide",
    "PASS-SOURCES-HOLD no per-work loading plate ever joins the frame the walk is still standing "
    "on while the arriving picture is held",
]


def score(duration=DUR):
    """The same weave-instrument fixture shape `tests/test_pass_hang.py` already reads its scores
    by: a real manifest instrument, so `armSources` genuinely sits on the road to takeover."""
    return {
        "schema": 2,
        "intent": "a picture held on the wire, read against the prepare budget",
        "pair": {"a": "a", "b": "b"},
        "seed": 3,
        "duration": duration,
        "interruption": {"withinMs": 200, "resolve": "nearest-door"},
        "failLand": "arrive",
        "cues": [{
            "id": "hold-main",
            "instrument": {"id": "weave", "api": 1},
            "voice": "letter",
            "roles": ["disassembly", "assembly"],
            "levels": ["SURFACE", "CELL"],
            "window": [0, duration / 1000.0],
            "works": ["a", "b"],
            "cameraAuthority": "stage",
            "nodes": {"prog": {"source": "progress"}, "zero": {"op": "static", "value": 0},
                      "one": {"op": "static", "value": 1}, "many": {"op": "static", "value": 28}},
            "tracks": {"mix": {"node": "prog"}, "strips": {"node": "many"}, "axis": {"node": "zero"},
                       "speed": {"node": "one"}, "seed": {"node": "zero"}, "nMul": {"node": "one"},
                       "press": {"node": "one"}},
        }],
        "provenance": {"source": "tests/test_pass_sources_hold.py", "measuredAt": "2026-08-28",
                       "by": "the sources-hold row"},
    }


def png_free_js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def wait_state(br, want, tries=200, nap=0.05):
    for _ in range(tries):
        if png_free_js(br, "return window.__exPass.host.report().state;") == want:
            return True
        br.sleep(nap)
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
    br.key("ArrowDown")
    for _ in range(30):
        if br.evaluate("String(!!(window.__exPass && window.__exPass.host))") == "true":
            HOOKS = """window.HOOKS = function () {
              var A = window.__exPass.adapter;
              return { dock: A.dock, glide: A.glide, curtain: A.curtain, mark: A.mark,
                       hangGeometry: A.hangGeometry, handoff: A.handoff };
            };
            0"""
            br.evaluate(HOOKS)
            return True
        br.sleep(0.2)
    return False


def rest_at(br, a):
    png_free_js(br, "window.__exPass.adapter.interrupt('rest'); return null;")
    wait_state(br, "idle")
    for _ in range(10):
        png_free_js(br, "var A=document.querySelector('.exh-frame[data-id=\"%s\"]');"
                        "A.classList.add('seen');"
                        "scrollTo(0, Math.round(scrollY + A.getBoundingClientRect().top"
                        " + (A.getBoundingClientRect().height - innerHeight)/2)); return null;" % a)
        br.sleep(0.35)
        top = float(png_free_js(br, "return document.querySelector('.exh-frame[data-id=\"%s\"]')"
                                    ".getBoundingClientRect().top;" % a))
        if abs(top) < 3:
            return True
    return False


def declare_and_offer(br, a, b, cause):
    return png_free_js(br, """
      var A = document.querySelector('.exh-frame[data-id="%s"]');
      var B = document.querySelector('.exh-frame[data-id="%s"]');
      var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                 kind:'step', cause:'%s', velocity:0,
                                                 score: window.__holdScore || null});
      window.__cmd = cmd;
      var took = cmd ? window.__exPass.layer().offer(cmd, window.HOOKS()) : false;
      return {got: !!cmd, took: took, gen: cmd ? cmd.gen : null};
    """ % (a, b, cause))


if not chrome_available():
    for r in ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    TMP = Path(tempfile.mkdtemp(prefix="synth_sourceshold_"))
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    build_site.OUT = TMP
    build_site.build(SITE_URL)

    HOLD = {}
    with serve(TMP, hold=HOLD) as base:
        with Browser(width=VW, height=VH) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.navigate(base + "/")
            br.sleep(0.8)
            armed = enter(br, base)
            WORKS = png_free_js(
                br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                    ".map(function(e){return e.dataset.id;}).slice(0,2);")
            ok_pair = armed and len(WORKS) == 2 and all(WORKS)

            if not ok_pair:
                for r in ROWS:
                    skip(r, f"the walk never registered a host, or hung no pair: "
                            f"armed={armed} works={WORKS}")
            else:
                A, B = WORKS[0], WORKS[1]
                br.evaluate("window.__holdScore = " + json.dumps(score()) + "; 0")
                rest_at(br, A)
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:120,"
                            " settleSlackMs:%d, clockPin:null, progressPin:null,"
                            " fixedScale:true}); 0" % SETTLE_SLACK_MS)

                # ---- arm the hold on B's own real picture, then swap its <img> onto it -------------
                # A cache-busted copy of the SAME URL the DOM already carries, so the bytes that
                # eventually land are a real photograph and the request is genuinely a fresh one
                # the browser has never resolved — never a URL this file invents.
                b_url = png_free_js(
                    br, "var i=document.querySelector('.exh-frame[data-id=\"%s\"] img.work');"
                        "return i.currentSrc || i.src;" % B)
                held_url = b_url + (("&" if "?" in b_url else "?") + "holdtest=1")
                HOLD.update(match="holdtest=1", delay=HOLD_DELAY)
                png_free_js(br, "var i=document.querySelector('.exh-frame[data-id=\"%s\"] img.work');"
                                "i.removeAttribute('srcset'); i.src = %s; return null;"
                                % (B, json.dumps(held_url)))

                got = declare_and_offer(br, A, B, "hold-sources")

                # ---- row 0 · not yet declined, well past the old 120ms budget ----------------------
                plate_seen = False
                checked_mid = None
                for _ in range(6):
                    br.sleep(0.05)
                    st = png_free_js(br, "return {state: window.__exPass.host.report().state,"
                                         " events: window.__exPass.host.report().events"
                                         "   .filter(function(e){return e.gen===%s;})"
                                         "   .map(function(e){return e.name;}),"
                                         " plateShown: (function(){var p=document.getElementById"
                                         "   ('ex-plate'); return !!(p && p.classList.contains"
                                         "   ('show'));})()};" % json.dumps(got.get("gen")))
                    if st.get("plateShown"):
                        plate_seen = True
                    checked_mid = st
                bad_names = {"declined", "recovered"}
                mid_ok = (got.get("took") and checked_mid is not None
                          and checked_mid.get("state") != "idle"
                          and not (bad_names & set(checked_mid.get("events") or []))
                          and "prepare-timeout" not in (checked_mid.get("events") or [])
                          and "sources-timeout" not in (checked_mid.get("events") or []))
                check(ROWS[0], mid_ok,
                      f"took={got.get('took')} ~0.3s in: {checked_mid}")

                # ---- row 1 · takes over for real once the picture lands -----------------------------
                instrument_while_running = None
                for _ in range(200):
                    rep_now = png_free_js(br, "return {state: window.__exPass.host.report().state,"
                                              " instrument: window.__exPass.host.report()"
                                              "   .instrument};")
                    if rep_now.get("state") == "running":
                        instrument_while_running = rep_now.get("instrument")
                        break
                    if rep_now.get("state") == "idle":
                        break
                    br.sleep(0.05)
                landed = wait_state(br, "idle", tries=200, nap=0.05)
                last_run = png_free_js(br, "return window.__exPass.host.report();")
                rep = png_free_js(br, "return window.__exPass.report();")
                gen = got.get("gen")
                client_events = [e for e in (rep.get("events") or []) if e.get("gen") == gen] \
                    if isinstance(rep.get("events"), list) else []
                never_declined = not any(e.get("name") == "host-declined" for e in client_events)
                real_instrument = bool(instrument_while_running) or bool(
                    (last_run.get("stack") or [None])
                    and any((v or {}).get("instrument") for v in (last_run.get("stack") or [])))
                check(ROWS[1],
                      landed and never_declined and real_instrument,
                      f"instrument while running: {instrument_while_running}; landed: {landed}; "
                      f"never host-declined for gen {gen}: {never_declined}; "
                      f"stack after landing: {last_run.get('stack')}")

                # ---- row 2 · no loading plate joined the frame throughout -----------------------
                final_plate = png_free_js(
                    br, "var p=document.getElementById('ex-plate');"
                        "return !!(p && p.classList.contains('show'));")
                check(ROWS[2], not plate_seen and not final_plate,
                      f"plate shown at any poll during the hold: {plate_seen}; "
                      f"plate shown at the end: {final_plate}")

                HOLD.clear()

    shutil.rmtree(TMP, ignore_errors=True)

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
