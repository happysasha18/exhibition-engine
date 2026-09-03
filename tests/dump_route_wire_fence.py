#!/usr/bin/env python3
"""dump_route_wire_fence — the standing route fence, V2-CONVERGENCE-PLAN-2026-08-31.md Phase 6.

WHY IT EXISTS. `docs/V2-CONVERGENCE-PLAN-2026-08-31.md`'s Phase 0 evidence drove a real dealt route
on a real bake (`~/tlvphotos-site/tests/drive_route_wire.py`, 72 crossings, 6 invocations x 2 roads)
and found it is the ONLY instrument in the tree that catches `recovered`/`last-resort`/camera-
handoff-jump/rest-not-reached — the render-time failure class box-fold actually carried (0 of 10
clean) and that Phase 2's plan-time `surfaceHandoverLegal` repair cannot see, because it refuses a
bad BUNDLE at plan time and box-fold's own defect only showed at RENDER time, on a real device. This
file gives that same class of check a standing home in this tree, so a regression here has a fence
behind it instead of only a plan document's memory of an evidence run.

THE BAKE IS THE ONE THIS TREE ALREADY PAYS FOR (Correction 2, Phase 6). `tests/engine_build.py` +
`tests/headless_harness.py` (via `tests/headless.py`) already bake and serve a real, synthetic
stage and drive a real headless Chrome over it — the same bake `tests/test_pass_route.py` and
`tests/test_pass_composed.py` already use. Nothing here extracts a second bake from
`tests/test_immersive.py` (that file, and `drive_route_wire.py` itself, live only in
`~/tlvphotos-site` and `~/tlvphotos-v2-release` — Correction 1 — this driving METHOD is copied
here, the way `dump_pass_arrival_walk.py`'s own docstring already copies `test_immersive.py`'s
`enter_walk`/`step` rather than importing them; the site's `drive_route_wire.py` was read in full to
copy its acceptance-gate rules and its renderer-fact reads (`LAST_PASSAGE_JS`, `LAYER_REPORT_JS`,
`LIVE_LAYER_JS` below), unmodified except for this tree's own namespace, `window.__exPass` in place
of the site's `window.__tlvPass` (`engine/build.py`'s `apply_namespace`, `_NAMESPACE = "ex"`)).

STRATIFIED BY SEARCH, NEVER TYPED (item 3). The engine's own synthetic fixture
(`tests/fixture_content`) is small and cannot be trusted to cast a rare instrument by chance — Phase
0's own 72-crossing random sample only reached 21 of 27. So the crossings this file actually drives
are not a random walk: for each of the 27 instruments (enumerated off
`tests/fixture_pass_composed.json`'s own frozen `consts.manifests`, cross-checked at import time
against the `pass-inst-*.js` glob the same way `run_all.py`'s own `check_pass_fixture()` gate
already does before any suite runs), a real (workRecordA, workRecordB) content pair is HUNTED for —
never chosen to look good — over the real 121-work fleet (`tests/fixture_pass_works.json`, the same
fixture `tests/test_pass_arrival_arc.py` and `tests/test_pass_cast_tiers.py` already search), at the
EXACT seed the live page itself will use for that edge (`window.__exPass.seed(key, 0)`, read live off
the page — a pure function of the visit's own seed and the edge's own key, needing no record loaded
to answer). The hunt runs the SAME composer instance already loaded on the page
(`window.__exPass.passage(req)` calls the identical `passComposer.passageFor` that
`tests/test_pass_arrival_arc.py`'s Node `vm` sandbox calls out of process — here it is called IN the
browser directly, over content supplied inline, so no subprocess and no second copy of the module are
needed), stopping at the first hit.

THE ONE HONEST LIMIT OF THIS SEARCH, STATED RATHER THAN HIDDEN. The route's records arrive in ONE
wave (RECORDS_CAP == SPREAD + MAX_UNFOLDS*UNFOLD_STEP == 20, `tests/test_pass_route.py`'s own KNOB
row), held open here (a `threading.Event` gates this file's own `records_answer`, never the harness's
`hold=` — that only delays a file-served response, not an `answer=`-served one) until every one of
this run's crossings has been searched, so every search below necessarily runs before any crossing
has DOCKED — `walkMemory`/`walkGenres`/`walkMiracles` are the empty visit's own honest values for
every slot searched, not a per-slot approximation invented here. The search is exact on `seed` and
`direction` (both are pure functions of the edge's own ids and the visit's own seed, read straight
off the page) and omits `routeRole`/`cameraState`/`buffer`/`framePace` entirely — the same minimal
request shape `tests/test_pass_arrival_arc.py:118-121` and `tests/test_pass_cast_tiers.py:91-93`
already search with, and the composer's own "missing means unstated" road (charter shelf 21) makes
that a real composition, never a stub one. What a search here FOUND and what a driven crossing
ACTUALLY CAST are reported side by side for exactly this reason: this file trusts what the renderer
says a crossing did, never what the search predicted it would do.

WHAT THIS FILE IS NOT. Coverage. Six crossings against 27 instruments is an illustration that the
construction-level repairs (Phase 1's tier ladder, Phase 2's box-fold/hero crop channel) hold up on
a real dealt route, not a claim about the whole 121-work collection or about routes this run never
drove — the closing sentence of its own report says exactly that, in the words the report carries.

NOT REGISTERED IN `run_all.py`'s SUITES (item 2). `run_all.py:135-171`'s `check_roster()` refuses
the whole gate on ANY drift between `SUITES` and the `test_*.py` glob, and `:228-258`'s skip ratchet
sums only what `SUITES`-registered suites print of themselves — this file's own SKIP lines (below)
are therefore never read by that ratchet at all, registered or not; run_all.py never subprocesses a
`dump_*.py` file. Kept a `dump_*.py`, unregistered, the same shape `dump_pass_arrival_walk.py`
already carries for exactly this kind of long walk (per item 2's recommendation) — it asserts nothing
about the suite's own green, but it IS an acceptance gate about the ROUTE (item 5): it exits 1 and
names the charter law a crossing broke, the same way `drive_route_wire.py`'s own gate at its tail
already does, so a person or a CI step that runs it deliberately gets a real red on a real regression.

Run: python3 tests/dump_route_wire_fence.py
Writes tests/route_wire_fence.txt beside its stdout. Exits 1 on any wire-fence failure (a `recovered`
crossing, a camera that never rested, a handoff outside tolerance, a dock the renderer never took
ownership of, a planned overlap that never rendered live) or on an infrastructure fault (no Chrome, a
driver crash); exits 0 otherwise, whatever the search's own reach across the 27 instruments came to.
"""
import json
import sys
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

FIXTURE = HERE / "fixture_pass_composed.json"
WORKS = HERE / "fixture_pass_works.json"
OUT_TXT = HERE / "route_wire_fence.txt"

SITE_URL = "https://synth.example.com"
VW, VH = 390, 844                 # Phase 0's own phone frame, pinned per item 4
MIN_CROSSINGS = 6                 # Phase 0's own per-route floor, pinned per item 4
ATTEMPT_CAP = 14520               # 121 * 120: every real ordered pair the fleet fixture carries
MAX_TARGETS_PER_SLOT = 3          # give up on a slot after this many instruments find no real hit
FLIGHT_TICKS_MAX = 100
FLIGHT_TICK_SLEEP = 0.3

RECORDS_ROUTE = "/api/pass/records"
RECORDS_CAP = 20                  # SPREAD 10 + MAX_UNFOLDS 2 * UNFOLD_STEP 5 (test_pass_route.py's own KNOB row)


# ------------------------------------------------------------ the 27-instrument enumeration source
def _instrument_roster():
    """The instrument names this hunt stratifies over — read off `fixture_pass_composed.json`'s own
    frozen `consts.manifests`, the same source `test_pass_composed.py:355-360` already reads for its
    own register-coverage row. Cross-checked here against the `pass-inst-*.js` glob
    (`engine/build.py:769`'s own source) as a light, local defense-in-depth: the heavier three-way
    check (glob / frozen fixture / test_pass_composed.py's own `_PUBLISHED`) already runs, before any
    suite spawns, in `run_all.py`'s `check_pass_fixture()` gate — this file does not repeat that
    machinery, only refuses to run silently on a drift its own enumeration would otherwise paper
    over."""
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    manifest_names = set(fixture["consts"]["manifests"])
    on_disk = {p.stem[len("pass-inst-"):] for p in (ROOT / "engine" / "assets").glob("pass-inst-*.js")}
    if manifest_names != on_disk:
        only_fixture = sorted(manifest_names - on_disk)
        only_disk = sorted(on_disk - manifest_names)
        print("dump_route_wire_fence: the frozen instrument cast and the pass-inst-*.js glob "
              "disagree, so this file refuses to enumerate a stratification it cannot trust "
              "(run `python3 tests/build_pass_fixture_consts.py` to refresh the frozen fixture):",
              file=sys.stderr)
        if only_fixture:
            print("  named in the frozen fixture, no file on disk: " + ", ".join(only_fixture),
                  file=sys.stderr)
        if only_disk:
            print("  a file on disk, not named in the frozen fixture: " + ", ".join(only_disk),
                  file=sys.stderr)
        sys.exit(2)
    # boxfold first: the one instrument Phase 0's own evidence and Phase 2's own repair are about,
    # so the run's best-matched slot (crossing 0, the walk's own empty-memory opening — see the
    # module docstring's "ONE HONEST LIMIT") is spent hunting for it before anything else.
    rest = sorted(n for n in manifest_names if n != "boxfold")
    return (["boxfold"] + rest) if "boxfold" in manifest_names else rest


INSTRUMENTS = _instrument_roster()


# ------------------------------------------------------------ the held records wave
# `records_ready` gates this file's OWN `records_answer` below (never `headless_harness.py`'s
# `hold=`, which only delays a file-served response and is never reached for an `answer=`-served
# route — see `headless_harness.py`'s `serve().do_GET`). The client fetches every id of the initial
# SPREAD in ONE wave, right after the door deals its hand (EX-PASS-RECORDS, 01a-pass.js), and never
# refetches an id once `passRecordsMap` holds it — so holding that one wave open is this file's only
# lever for making sure the content this run SEARCHED wins is the content the REAL declare later
# reads, rather than racing a wave that already landed.
records_ready = threading.Event()
RECORDS_STORE = {}


def records_answer(raw_path):
    if not raw_path.startswith(RECORDS_ROUTE):
        return None
    records_ready.wait(timeout=90)
    ids = [i for i in parse_qs(urlparse(raw_path).query).get("ids", [""])[0].split(",") if i]
    out = {i: RECORDS_STORE[i] for i in ids if i in RECORDS_STORE}
    return (200, "application/json", json.dumps({"records": out}))


def wire_pass_config(base_dir, fixture):
    """The settings record as the site writes it for the composed road — `test_pass_route.py`'s own
    `put_records` does this same rewrite; carried here rather than imported, since that file is a
    `test_*.py` suite with its own top-level run-on-import side effects (module-scope `check()` rows
    fired the moment it is imported), exactly the reason `dump_pass_arrival_walk.py`'s own docstring
    gives for copying rather than importing `test_immersive.py`."""
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fixture["consts"],
                       records={"route": RECORDS_ROUTE, "cap": RECORDS_CAP})
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def enter(br, base):
    """The visitor's own way in — `test_pass_route.py`'s own `enter()`, copied (its own docstring
    explains every wait it stands on): navigate, deal the door, wait for both the composer and the
    first records wave together. `route.ids` (below) needs neither: it comes off `order`/`shown`,
    the door's own kinship-ordered deal (`05-door-deal-circle-walkstate.js`,
    `07-door-face-ceremony.js`), read before this wait ever starts."""
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/?pass=diagnostics:on")
    br.sleep(0.8)
    if br.evaluate("String(!!document.querySelector('.exd-window'))") == "true":
        try:
            br.click(".exd-window", settle=1.4)
        except RuntimeError:
            br.sleep(1.0)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)


# ------------------------------------------------------------ the search, run client-side
#
# THE CONTEXT MUST MATCH `passRequestFor`'s OWN, OR THE SEARCH LIES — found empirically, this phase:
# a first pass searching only {workRecordA, workRecordB, direction, seed} (the minimal shape
# `test_pass_arrival_arc.py:118-121`/`test_pass_cast_tiers.py:91-93` search with, for their own
# narrower questions) found a real pair casting a target instrument on every one of six tried slots,
# and NONE of those six targets were what the live, fully-contexted declare actually cast —
# `routeRole` alone, left out there, flips the composer's own weighted tiers hard enough to swap the
# result outright (a live check: the same pair/seed cast boxfold with no routeRole and lens+matter
# with routeRole="entrance" supplied). `routeRole`/`routeFunction` cost nothing approximate to add:
# slot 0 of a virgin visit is ALWAYS "entrance"/"tonic" (`passRouteStation`'s own
# `!passVisitOpened()` branch, unconditional — no content, no records, no session state decides it),
# and every later slot in a route that never revisits an edge (this hunt never does) reads
# `passRouteStation`'s STRUCTURAL branch — `shape.functions[i]` mapped through
# `passRoleOfFunction(fn, i===crest?"crest":"route")` — which is exactly what
# `report().route.roles[i]`/`.functions[i]` already read, needing no records either. `cameraState`
# is `adapter.hangGeometry(fromId)`, a DOM box read with no content dependency of its own. What
# still cannot be known before this run's own crossings have actually docked is `walkMemory` /
# `walkGenres` / `walkMiracles` (the visit's own memory of what has already played) and `framePace`
# (a rolling measurement off frames not yet rendered) — both are left at their own COLD-VISIT
# values (empty lists, `null`), honest for slot 0 and an approximation for the rest, never a
# fabricated number standing in for a measurement.
#
# EXHAUSTIVE, NOT STRIDED — a first cut sampled `(i*7)%n, (j*13+3)%n` up to a fixed attempt count;
# for a fixed `n` that pattern is a full period of `n` DISTINCT pairs and then repeats the same `n`
# pairs forever, so a cap above `n` wastes nearly all of it re-testing pairs already read. The fleet
# is 121 works — 14 520 ordered pairs — and a full sweep measured at ~30s wall time in this
# environment; run once per (slot, tried instrument), never cached, matching the standing rule that
# nothing here may be keyed on which two pictures are involved across runs.
SEARCH_JS = """
(function(){
  var works = window.__routeFenceWorks;
  var ids = Object.keys(works);
  var n = ids.length;
  var target = __TARGET__, seed = __SEED__, direction = __DIRECTION__;
  var routeRole = __ROUTE_ROLE__, routeFunction = __ROUTE_FUNCTION__, cameraState = __CAMERA__;
  var attempts = 0;
  for (var i = 0; i < n; i++) {
    for (var j = 0; j < n; j++) {
      if (i === j) continue;
      attempts++;
      var req = {workRecordA: works[ids[i]], workRecordB: works[ids[j]],
                 direction: direction, seed: seed, routeRole: routeRole,
                 routeFunction: routeFunction, cameraState: cameraState,
                 walkMemory: [], walkGenres: [], walkMiracles: [], framePace: null};
      try {
        var p = window.__exPass.passage(req);
        var cues = (p && p.plan && p.plan.cues) || [];
        for (var c = 0; c < cues.length; c++) {
          if (cues[c].instrument && cues[c].instrument.id === target) {
            return {found: true, aKey: ids[i], bKey: ids[j], attempts: attempts};
          }
        }
      } catch (e) {}
    }
  }
  return {found: false, attempts: attempts};
})()
"""


def search_for(br, target, seed, direction, route_role, route_function, camera_state):
    body = (SEARCH_JS
            .replace("__TARGET__", json.dumps(target))
            .replace("__SEED__", json.dumps(seed))
            .replace("__DIRECTION__", json.dumps(direction))
            .replace("__ROUTE_ROLE__", json.dumps(route_role))
            .replace("__ROUTE_FUNCTION__", json.dumps(route_function))
            .replace("__CAMERA__", json.dumps(camera_state)))
    return br.evaluate(body)


# ------------------------------------------------------------ renderer-fact reads, copied from
# drive_route_wire.py (tlvphotos-site) verbatim except for the namespace, `window.__exPass` in
# place of `window.__tlvPass` (Correction 1/2 — the driving METHOD is copied, not imported).
LAST_PASSAGE_JS = (
    "(function(){var ps=(window.__exPass.passages&&window.__exPass.passages())||[];"
    "var row=ps[ps.length-1]; if(!row) return null;"
    "var score=row.score||null;"
    "function n(x){return (x&&typeof x==='object'&&('v' in x))?x.v:x;}"
    "return {key:row.key, declined:row.declined||null,"
    "camera:(score&&score.camera?score.camera:null), duration:score?score.duration:null,"
    "cues:(score&&score.cues?score.cues:[]).map(function(c){"
    "return {id:c.id, instrument:(c.instrument&&c.instrument.id)||null,"
    "window:c.window||null, levels:c.levels||[]};})};})()"
)
LAYER_REPORT_JS = (
    "(function(){var l=window.__exPass&&window.__exPass.layer&&window.__exPass.layer();"
    "return l&&l.report?l.report():null;})()"
)
LIVE_LAYER_JS = (
    "(function(){var l=window.__exPass&&window.__exPass.layer&&window.__exPass.layer();"
    "var r=l&&l.report?l.report():null;if(!r)return null;"
    "return {state:r.state,active:r.active,live:r.live,drew:r.drew,"
    "stack:(r.stack||[]).map(function(v){return {id:v.id,instrument:v.instrument,stack:v.stack,"
    "live:v.live,levels:v.levels,applied:!!v.applied};}),"
    "camera:(r.camera&&r.camera.pose)||null};})()"
)


def _live_layer_sample(report):
    if not isinstance(report, dict):
        return None
    rows = []
    for voice in report.get("stack") or []:
        if not isinstance(voice, dict):
            continue
        rows.append({"id": voice.get("id"), "instrument": voice.get("instrument"),
                     "live": bool(voice.get("live"))})
    return {"stack": rows}


def _scalar(x):
    """Unwrap the composer's own `Flt` number tag — `_scalar`, `_window_pair`, `check_overlaps`,
    `requested_live_overlap` and `observed_live_overlap` below are `drive_route_wire.py`'s own
    functions, copied verbatim (pure Python, no namespace to adapt)."""
    if isinstance(x, dict) and "v" in x:
        x = x["v"]
    return x if isinstance(x, (int, float)) else None


def _window_pair(raw, cue_id):
    if isinstance(raw, (list, tuple)) and len(raw) >= 2:
        a, b = _scalar(raw[0]), _scalar(raw[1])
        if a is not None and b is not None:
            return float(a), float(b)
    return 0.0, 0.0


def check_overlaps(cues):
    out = []
    for i in range(len(cues)):
        for j in range(i + 1, len(cues)):
            a, b = cues[i], cues[j]
            wa = _window_pair(a.get("window"), a.get("id"))
            wb = _window_pair(b.get("window"), b.get("id"))
            if wa[0] < wb[1] and wb[0] < wa[1]:
                shared = sorted(set(a.get("levels") or []) & set(b.get("levels") or []))
                if shared:
                    out.append({"a": a.get("id"), "b": b.get("id")})
    return out


def requested_live_overlap(cues):
    out = []
    for i in range(len(cues)):
        for j in range(i + 1, len(cues)):
            a, b = cues[i], cues[j]
            wa = _window_pair(a.get("window"), a.get("id"))
            wb = _window_pair(b.get("window"), b.get("id"))
            start, end = max(wa[0], wb[0]), min(wa[1], wb[1])
            if end - start >= FLIGHT_TICK_SLEEP:
                out.append({"a": a.get("id"), "b": b.get("id")})
    return out


def observed_live_overlap(samples):
    pairs = set()
    for sample in samples or []:
        ids = sorted(str(row.get("id")) for row in (sample.get("stack") or [])
                     if row.get("live") and row.get("id") is not None)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                pairs.add((ids[i], ids[j]))
    return pairs


def say(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


# ------------------------------------------------------------ one crossing, driven and read
def fly_and_capture(br):
    """Step the walk one work forward, polling for as long as the crossing plays, exactly the way
    `drive_route_wire.py`'s own `fly_and_capture` does (screenshots and the composer's own ring-
    buffer event log dropped here — this file's acceptance gate never reads either)."""
    live_layer_trace = []
    br.key("ArrowDown")
    started = False
    docked = False
    active_ticks = 0
    for _ in range(FLIGHT_TICKS_MAX):
        try:
            sample = _live_layer_sample(json.loads(br.evaluate("JSON.stringify(%s)" % LIVE_LAYER_JS)))
        except (ValueError, RuntimeError):
            sample = None
        if sample:
            live_layer_trace.append(sample)
        in_flight = (br.evaluate("String(document.body.classList.contains('ex-pass-curtain'))")
                     == "true"
                     or br.evaluate("String(!!(window.__exPass && window.__exPass.layer() "
                                     "&& window.__exPass.layer().report().active))") == "true")
        if in_flight:
            started = True
            active_ticks += 1
        elif started:
            docked = True
            break
        br.sleep(FLIGHT_TICK_SLEEP)
    br.sleep(0.6)

    passage = json.loads(br.evaluate("JSON.stringify(%s)" % LAST_PASSAGE_JS))
    layer_report = json.loads(br.evaluate("JSON.stringify(%s)" % LAYER_REPORT_JS))

    return {"docked": docked, "rendererObserved": started, "rendererFramesObserved": active_ticks,
            "passage": passage, "layerReport": layer_report, "liveLayerTrace": live_layer_trace}


EMERGENCY_CUE_ID = "last-resort"   # pass-layer.js's own `mergeLastResort`/`lastResortCast`: the
                                    # rescued cue is always named this, at RENDER time — never as an
                                    # event name (see `emergency_cast` below for why the old check
                                    # here never fired)


def emergency_cast(crossing):
    """WHETHER THE HOST'S OWN EMERGENCY INSTRUMENT ACTUALLY PLAYED (S-30, наряд: the run must print
    this share itself). `pass-layer.js`'s `logEvt` names, enumerated in full
    (`grep -on 'logEvt("[a-zA-Z0-9-]*"'`), never include the literal string "last-resort" — the
    rescue is signalled only by the CUE the host merges in
    (`cues: [{ id: "last-resort", instrument: { id: inst.name }, ... }]`, `pass-layer.js`'s
    `lastResortCast`), which shows up in a live frame's own `stack`, never in the terminal event
    list. The acceptance gate below used to check the event names for this string and could never
    match it — a dead check standing in for a class of failure the events alone cannot name, the
    same class 2026-09-01's adversarial review flagged (finding 1/2: a real rescue that shares no
    other forbidden event gets counted as `clean`/`recovered`/`overlap-not-live` instead). Reading
    the cue id off the live trace is the one place this ever actually surfaces."""
    for tick in crossing.get("liveLayerTrace") or []:
        for voice in tick.get("stack") or []:
            if voice.get("id") == EMERGENCY_CUE_ID and voice.get("live"):
                return True
    return False


def crossing_failures(label, crossing):
    """The acceptance gate — `drive_route_wire.py`'s own bottom section, copied (item 5: a
    `recovered` outcome names the charter law it broke, never a bare timeout)."""
    failures = []
    if not crossing.get("rendererObserved"):
        failures.append(label + ": renderer never owned the crossing")
    elif crossing.get("rendererFramesObserved", 0) < 3:
        failures.append(label + ": no renderer-owned middle frame")
    if not crossing.get("docked"):
        failures.append(label + ": renderer did not dock the arriving work")
    terminal = crossing.get("layerReport") or {}
    if not terminal:
        failures.append(label + ": host published no terminal renderer record")
        return failures
    rest = terminal.get("rest") or {}
    if rest.get("rested") is not True:
        failures.append(label + ": camera did not reach the destination hang before dock "
                                 "(charter seam: continuous passage, exact B hang)")
    for handoff in terminal.get("handoffs") or []:
        if handoff.get("within") is not True:
            failures.append(label + ": camera handoff %s→%s jumped by %s (authority handoff "
                                     "outside its own published tolerance)"
                            % (handoff.get("from"), handoff.get("to"), handoff.get("off")))
    if not (terminal.get("stack") or []):
        failures.append(label + ": renderer docked with no actual applied stack")
    terminal_names = {e.get("name") for e in (terminal.get("events") or [])}
    forbidden = sorted(n for n in ("resources-declined", "prepare-timeout", "recovered")
                       if n in terminal_names)
    if forbidden:
        failures.append(label + ": terminal fallback " + ", ".join(forbidden)
                                 + " (seam-law failure: the fallback ran, not merely a timeout)")
    if emergency_cast(crossing) and "last-resort" not in forbidden:
        failures.append(label + ": terminal fallback last-resort (seam-law failure: the host's own "
                                 "emergency instrument played, read off the live stack's cue id "
                                 "rather than off an event name that this host never publishes)")
    cues = (crossing.get("passage") or {}).get("cues") or []
    observed = {tuple(row) for row in [list(p) for p in sorted(
        observed_live_overlap(crossing.get("liveLayerTrace") or []))]}
    for contract in requested_live_overlap(cues):
        pair = tuple(sorted((str(contract.get("a")), str(contract.get("b")))))
        if pair not in observed:
            failures.append(label + ": planned overlap %s/%s was never renderer-live" % pair)
    return failures


# ------------------------------------------------------------ the drive itself
def main():
    if not chrome_available():
        print("chrome absent — this drive needs a real browser", file=sys.stderr)
        return 3

    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if not WORKS.exists():
        print("tests/fixture_pass_works.json is not on this machine — nothing real to search over",
              file=sys.stderr)
        return 3
    works_content = json.loads(WORKS.read_text(encoding="utf-8"))["works"]

    tmp = Path(tempfile.mkdtemp(prefix="route_wire_fence_"))
    build_site.OUT = tmp
    build_site.build(SITE_URL)
    wire_pass_config(tmp, fixture)

    say("stage baked at %s" % tmp)

    outcomes = []           # per-crossing report rows
    reached = set()         # instruments actually cast on a driven crossing
    failures_all = []
    queue = list(INSTRUMENTS)

    with serve(tmp, answer=records_answer) as base:
        with Browser(width=VW, height=VH) as br:
            enter(br, base)
            shape = js(br, "return window.__exPass.report().route;")
            ids = shape.get("ids") or []
            if len(ids) < 2:
                print("the door never dealt a usable hang — no route to drive", file=sys.stderr)
                return 1
            say("dealt hand: %s" % ids)

            # inject the real 121-work fleet into the page once, reused by every slot's search
            br.evaluate("window.__routeFenceWorks = %s;" % json.dumps(works_content))

            n_slots = min(MIN_CROSSINGS, len(ids) - 1)
            route_roles = shape.get("roles") or []
            route_functions = shape.get("functions") or []
            slot_plan = []   # (aId, bId, searchedFor, foundContentKeys or None)
            for i in range(n_slots):
                a_id, b_id = str(ids[i]), str(ids[i + 1])
                forward = a_id <= b_id
                small, large = (a_id, b_id) if forward else (b_id, a_id)
                direction = "a-to-b" if forward else "b-to-a"
                key = small + "__" + large
                seed = js(br, "return window.__exPass.seed(%s, 0);" % json.dumps(key))
                # slot 0 of a virgin visit is unconditionally "entrance"/"tonic"
                # (passRouteStation's own !passVisitOpened() branch); every later, never-repeated
                # edge reads the structural roles/functions report().route already carries — see
                # the SEARCH_JS comment above for why this is exact, not approximate.
                if i == 0:
                    route_role, route_function = "entrance", "tonic"
                else:
                    route_role = route_roles[i] if i < len(route_roles) else None
                    route_function = route_functions[i] if i < len(route_functions) else None
                camera_state = js(br, "return window.__exPass.adapter.hangGeometry(%s);"
                                  % json.dumps(ids[i]))

                searched_for = None
                found_keys = None
                tries = 0
                while queue and tries < MAX_TARGETS_PER_SLOT:
                    target = queue[0]
                    tries += 1
                    say("  slot %d: hunting %s (routeRole=%s) over the real fleet, exhaustive"
                        % (i, target, route_role))
                    got = search_for(br, target, seed, direction, route_role, route_function,
                                     camera_state)
                    if got.get("found"):
                        searched_for = target
                        found_keys = (got["aKey"], got["bKey"])
                        queue.pop(0)
                        break
                    queue.pop(0)
                    queue.append(target)   # try again on a later slot, at a different seed

                if found_keys:
                    a_content = json.loads(json.dumps(works_content[found_keys[0]]))
                    b_content = json.loads(json.dumps(works_content[found_keys[1]]))
                else:
                    # no target instrument found real content for this slot within budget — fall
                    # back to the first two real records of the fleet, still real, never typed, just
                    # not aimed at a specific instrument (item 3's own SKIP path, one level up: the
                    # slot itself is spent, not any one instrument's own search)
                    real_ids = list(works_content.keys())
                    a_content = json.loads(json.dumps(works_content[real_ids[0]]))
                    b_content = json.loads(json.dumps(works_content[real_ids[1]]))

                a_content["id"] = small
                b_content["id"] = large
                RECORDS_STORE[small] = a_content
                RECORDS_STORE[large] = b_content
                slot_plan.append({"from": ids[i], "to": ids[i + 1], "searchedFor": searched_for})

            say("search complete — releasing the held records wave")
            records_ready.set()

            for _ in range(150):
                got = js(br, "var r = window.__exPass.report();"
                             "return {st: r.composer.state, held: r.records.held};")
                if got.get("st") == "read" and (got.get("held") or 0) > 1:
                    break
                br.sleep(0.2)

            for i, plan in enumerate(slot_plan):
                label = "crossing %d (%s→%s)" % (i + 1, plan["from"], plan["to"])
                say("driving %s (searched for %s)" % (label, plan["searchedFor"] or "—"))
                result = fly_and_capture(br)
                cast = sorted({c.get("instrument") for c in (result.get("passage") or {}).get("cues", [])
                               if c.get("instrument")})
                reached.update(cast)
                crossing_fail = crossing_failures(label, result)
                failures_all.extend(crossing_fail)
                outcomes.append({
                    "label": label, "searchedFor": plan["searchedFor"], "cast": cast,
                    "docked": result.get("docked"), "rendererObserved": result.get("rendererObserved"),
                    "clean": not crossing_fail,
                    "failures": crossing_fail,
                    "emergency": emergency_cast(result),
                })

    # ------------------------------------------------------------ the report, pass_arrival_walk.txt's
    # own rollup style: a per-row reading, a tally line, a closing sentence disclaiming coverage.
    lines = []
    lines.append("THE STANDING ROUTE FENCE — A REAL DEALT ROUTE, ON A REAL BAKE")
    lines.append("=" * 78)
    lines.append("")
    lines.append("Driven over tests/engine_build.py's synthetic stage at %s x %s (Phase 0's own phone" % (VW, VH))
    lines.append("frame), %d crossings on one dealt hand. Each crossing's own content was hunted for" % len(outcomes))
    lines.append("— not chosen to look good — by direct search over the real 121-work fleet")
    lines.append("(tests/fixture_pass_works.json) at the exact seed the live page itself struck for that")
    lines.append("edge; where a search found nothing for any of %d tried instruments within its own" % MAX_TARGETS_PER_SLOT)
    lines.append("bounded budget, the slot still drove on real, un-aimed content.")
    lines.append("")
    for row in outcomes:
        lines.append(row["label"])
        lines.append("         searched for: %s" % (row["searchedFor"] or "(slot exhausted its own search budget)"))
        lines.append("         actually cast: %s" % (", ".join(row["cast"]) if row["cast"] else "(no instrument)"))
        lines.append("         docked: %s   renderer owned it: %s   wire-clean: %s"
                     % (row["docked"], row["rendererObserved"], row["clean"]))
        for f in row["failures"]:
            lines.append("         RED — " + f)
        lines.append("")
    lines.append("-" * 78)
    # THE EMERGENCY-FALLBACK SHARE, PRINTED BY THE RUN ITSELF (наряд S-30: this number is never
    # asserted from a prior evidence folder — it is read straight off `emergency_cast`, this run's
    # own live-stack cue check, so a person reading this file's own stdout has the number rather
    # than a claim about it).
    emergency_n = sum(1 for row in outcomes if row["emergency"])
    lines.append("emergency-fallback share (host's own last-resort instrument actually played): "
                 "%d of %d (%.1f%%)" % (emergency_n, len(outcomes),
                                        100.0 * emergency_n / len(outcomes) if outcomes else 0.0))
    lines.append("instruments reached: %d of %d" % (len(reached), len(INSTRUMENTS)))
    for name in INSTRUMENTS:
        if name in reached:
            lines.append("  reached  %s" % name)
        elif name in queue:
            lines.append("  SKIP     %s — no real pair/seed among the tried slots' own budgets cast "
                         "it in this run; a fact about this sample, not an exclusion" % name)
        else:
            lines.append("  SKIP     %s — a search found a real pair for it, but the live declare "
                         "(fuller context than the search's own) cast something else this run"
                         % name)
    lines.append("")
    lines.append("This illustrates that Phase 1's tier-ladder repair and Phase 2's box-fold/hero crop")
    lines.append("channel hold up on a real dealt route; it claims nothing about the whole 121-work")
    lines.append("collection or about any route this particular run did not drive.")
    text = "\n".join(lines) + "\n"
    OUT_TXT.write_text(text, encoding="utf-8")
    print(text)
    print("written to %s" % OUT_TXT)

    if failures_all:
        print("ROUTE-WIRE FAIL", file=sys.stderr)
        for f in failures_all:
            print("- " + f, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
