#!/usr/bin/env python3
"""EX-PASS — the transition seam: live settings, one command, one landing owner.
Run: python tests/test_pass.py

The seam carries no drawing. These rows prove the CONTRACT: every setting resolves through a named
ladder with an observable applied value, a refused value falls back and says so, the landing moment
is the exact number the setting names, a score is data with an allow-list, and every road between
two works — the stepping input and the programmatic jumps alike — declares the same command.
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


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_pass_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- string rows

check("EX-PASS the seam ships: its region survives the bake with its keep-marker",
      "/*!01a-pass.js*/" in JS and "passLandGate" in JS and "passStart" in JS,
      "the fragment must reach the served client as its own region")

check("EX-PASS the landing moment is a SETTING, never a literal in the watcher",
      "threshold: t }" in JS and "threshold: 0.55" not in JS and "landProgress: { kind" in SRC,
      "the in-view watcher must take its threshold from the register")

check("EX-PASS one owner of the landing: the watcher hands the arriving work to landOn",
      'passLandGate(x.target, "observe", landOn)' in JS and "function landOn(" in JS,
      "the watcher must commit nothing itself")

# Every road between two works declares a command. The stepping road plus the six programmatic
# landings; a clamped no-move step declares nothing, which is why the count is of CALL SITES.
JUMP_CAUSES = ["rotate", "recentre", "restore", "hash", "series", "hang", "popstate"]
missing = [c for c in JUMP_CAUSES if ('passJump(' not in JS or '"%s"' % c not in JS)]
check("EX-PASS every programmatic landing carries the same command",
      not missing and 'kind: "step", cause: "step"' in JS,
      f"causes absent from the served client: {missing}")

check("EX-PASS the flight stops for EVERY standing face (one predicate, not three flags)",
      "if (faceStands()) { glideCancel(); glideGoal = null; passAbortNow" in JS
      and "if (atDoor || busy || sideOpen) { glideCancel(); glideGoal = null; return; }" not in JS,
      "a closer look or a question card opening mid-flight must stop the flight")

check("EX-PASS the score is data: an allow-list of fields, no executable one among them",
      'PASS_SCORE_FIELDS = ["schema", "intent", "seed", "pair", "params"]' in SRC
      and "eval(" not in SRC and "new Function" not in SRC,
      "a score names data only")

check("EX-PASS the driver graph is declared whole, and only the static kind is built",
      'PASS_DRIVERS = ["static", "phase", "velocity", "pointer", "capability"]' in SRC
      and 'PASS_DRIVERS_BUILT = ["static"]' in SRC,
      "the schema carries all five kinds; the unbuilt ones fall back to their base")

check("EX-PASS the drawing layer travels as its own file, and the bake ships it",
      (TMP / "pass-layer.js").exists() and "__exPassLayer" in (TMP / "pass-layer.js").read_text(encoding="utf-8")
      and 'PASS_SRC = "pass-layer.js"' in SRC,
      "the picture's file must reach the site beside the bundle")

interaction = SRC[SRC.index("const passInteraction ="):SRC.index("function passWhere")]
check("EX-PASS the host owns one passive normalized pointer signal without stealing navigation",
      "interaction: interaction" in SRC
      and "pointerdown" in interaction and "pointermove" in interaction
      and "passive: true" in interaction and "preventDefault" not in interaction,
      "the host may observe pointer/tap/drag, but the motion layer keeps navigation ownership")

check("EX-PASS the marks keep their own prefix, so the walk's own timings stay exact",
      '"@@NS@@-pass:"' in SRC and "ex-pass:nav-start" not in JS.replace("@@NS@@", "ex"),
      "the seam must not enter the tlv:/ex: timing stream")

# ---------------------------------------------------------------- browser rows

BROWSER_ROWS = [
    "EX-PASS the diagnostic surface is off by default",
    "EX-PASS a session override turns diagnostics on and the address strips itself",
    "EX-PASS every setting reports its applied value and the source that won",
    "EX-PASS a refused value falls back to the default and records why",
    "EX-PASS the landing moment applies EXACTLY as asked (0.531 stays 0.531)",
    "EX-PASS a score naming an unknown field has that field cut and noted, and still plays",
    "EX-PASS a score may not set a name closed to it",
    "EX-PASS one step declares one command and lands it",
    "EX-PASS a second input supersedes the first, which ends as aborted",
    "EX-PASS entering the walk declares a jump command",
    "EX-PASS the command's parameters are frozen at the start",
    "EX-PASS a closer look opening mid-flight stops the flight",
    "EX-PASS the drawing layer's file is never fetched while the setting stands off",
    "EX-PASS the setting preloads the layer before the gesture and the walk keeps stepping",
    "EX-PASS reduced motion plays the charter's pardoned floor rather than refusing the layer",
    "EX-PASS the walk's rest record follows the dock: the turn after a crossing holds the arriving work",
    "EX-PASS a second gesture while a renderer holds the command chains to the NEXT frame",
    "EX-PASS the pardoned floor names one voice, no miracle and no camera flight, at the quiet "
    "tier's own duration floor",
    "EX-PASS the composer's file still never reaches a reduced visit, even one whose floor plays",
    "EX-PASS the register names nothing the settings record already owns, so real refusals stand",
    "EX-PASS RED-ON-BUG · reverting the pardon (charter shelf 19, naряд S-08) makes reduced motion "
    "refuse the layer again",
]

# A HOST THAT TAKES THE COMMAND AND HOLDS IT, registered through the seam's own door — the same
# function the drawing file registers itself with. It draws nothing, which is why these three rows
# need no WebGL and no score: what they read is the WALK's side of the seam — where the walk stands
# while a renderer holds the command, what a device change does to it, and what a second gesture
# declares. The renderer's own picture has its own suites.
STUB_HOST = """
(function () {
  if (typeof window.__exPassLayer !== 'function') return 'no door';
  window.__stub = { active: false, cmd: null, hooks: null, resized: 0, offers: 0 };
  window.__exPassLayer({
    offer: function (cmd, hooks) {
      var s = window.__stub;
      s.active = true; s.cmd = cmd; s.hooks = hooks; s.offers++;
      hooks.curtain(true);
      return true;                       // the host takes responsibility for this landing
    },
    resize: function () { window.__stub.resized++; },
    cancel: function () { window.__stub.active = false; },
    report: function () { return { active: window.__stub.active }; }
  });
  return 'registered';
})()
"""

# The settle a real host runs at the end of a passage (§2.2): the DOM is revealed and the walk
# placed, the canvas comes down, and the command docks.
STUB_SETTLE = """
(function () {
  var s = window.__stub;
  if (!s || !s.cmd) return 'nothing in flight';
  s.hooks.handoff(s.cmd);
  s.hooks.curtain(false);
  s.active = false;
  s.hooks.dock(s.cmd);
  return String(s.cmd.to.id);
})()
"""

WHERE = ("var els=[].slice.call(document.querySelectorAll('.exh-frame'));"
         "var mid=innerHeight/2, best=-1, bd=1e9;"
         "els.forEach(function(e,i){var r=e.getBoundingClientRect();"
         "var d=Math.abs(r.top+r.height/2-mid); if(d<bd){bd=d;best=i;}});"
         "return {i:best, id:best>=0?els[best].dataset.id:null, off:Math.round(bd),"
         " y:Math.round(scrollY)};")


def where(br):
    """The work the walk actually stands on: the frame whose centre is nearest the eye."""
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % WHERE))


# the two-finger touch that opens the closer look, the road tests/test_zoom.py drives it by
PINCH = (
    "(sel)=>{const el=document.querySelector(sel);if(!el)return 'no-el';"
    "try{const t1=new Touch({identifier:1,target:el,clientX:120,clientY:200});"
    "const t2=new Touch({identifier:2,target:el,clientX:210,clientY:270});"
    "const ev=new TouchEvent('touchstart',{touches:[t1,t2],targetTouches:[t1,t2],"
    "changedTouches:[t1,t2],bubbles:true,cancelable:true});"
    "el.dispatchEvent(ev);return 'ok';}catch(e){return 'err:'+e.message;}}"
)


def ready(br, tries=25):
    """The walk owns the input only once the door ceremony has finished; a key pressed before that
    is absorbed by the ceremony and steps nothing. Poll for the walk's own face standing alone."""
    for _ in range(tries):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            return True
        br.sleep(0.2)
    return False


def enter(br, base, pass_arg=None):
    """A fresh visitor who opens the door and stands in the walk, ready to step."""
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
    br.click(".exd-window", settle=1.4)                 # the door ceremony hands over to the walk
    ready(br)
    br.sleep(0.4)


def report(br):
    return json.loads(br.evaluate("JSON.stringify(window.__exPass.report())"))


def row(rep, name):
    for s in rep["settings"]:
        if s and s["name"] == name:
            return s
    return None


def gen_now(br):
    """The newest generation the walk has declared. The event ring holds the last 64 rows, so a
    slice by index lies once entering has filled it; a slice by generation never does."""
    return int(br.evaluate(
        "(()=>{const e=window.__exPass.report().events;"
        "return String(e.length?Math.max.apply(null,e.map(r=>r.gen)):0);})()") or 0)


def since(rep, gen0):
    return [e for e in rep["events"] if e["gen"] > gen0]


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            # 0 · off by default
            br.navigate(base + "/")
            br.clear_storage()
            br.reload()
            br.sleep(0.8)
            absent = br.evaluate("String(typeof window.__exPass)")
            check(BROWSER_ROWS[0], absent == "undefined", f"typeof __exPass={absent}")

            # 1 · the session override, and the address cleaning itself
            br.navigate(base + "/?pass=diagnostics:on")
            br.sleep(0.8)
            there = br.evaluate("String(typeof window.__exPass)")
            addr = br.evaluate("location.search")
            stored = br.evaluate("sessionStorage.getItem('ex-pass')")
            check(BROWSER_ROWS[1],
                  there == "object" and "pass=" not in addr and "diagnostics" in (stored or ""),
                  f"typeof={there} search={addr!r} stored={stored!r}")

            # 2 · every name reports its stand
            rep = report(br)
            names = sorted(s["name"] for s in rep["settings"] if s)
            lp = row(rep, "landProgress")
            whole = all(k in (lp or {}) for k in ("asked", "source", "applied", "fallback", "driver"))
            check(BROWSER_ROWS[2],
                  "landProgress" in names and "visualLayer" in names and whole
                  and lp["applied"] == 0.55 and lp["source"] == "default"
                  and rep["layer"] == "absent",
                  f"names={names} landProgress={lp} layer={rep.get('layer')}")

            # 3 · a value outside the range falls back, loudly
            br.navigate(base + "/?pass=landProgress:9")
            br.sleep(0.8)
            rep = report(br)
            lp = row(rep, "landProgress")
            said = [r for r in rep["refusals"] if r.get("name") == "landProgress"]
            check(BROWSER_ROWS[3],
                  lp["applied"] == 0.55 and lp["fallback"] is True and bool(said)
                  and "0…1" in (said[0].get("why") or ""),
                  f"applied={lp['applied']} fallback={lp['fallback']} refusals={said[:1]}")

            # 4 · the exact float, unrounded, and the watcher built on it
            br.navigate(base + "/?pass=landProgress:0.531")
            br.sleep(0.8)
            rep = report(br)
            lp = row(rep, "landProgress")
            check(BROWSER_ROWS[4],
                  lp["applied"] == 0.531 and lp["source"] == "session" and lp["fallback"] is False,
                  f"applied={lp['applied']} source={lp['source']}")

            # 5 · AN UNKNOWN FIELD IS CUT AND NOTED, NOT A REFUSAL OF THE WHOLE SCORE (2026-08-24) —
            # the same conversion the weight fence and the intent-length fence took on 2026-08-18. A
            # score is composed by the collection's own composer, and a field the client's own
            # allow-list has not yet learned about used to cost the visitor the whole crossing over
            # one name. So the field is cut, the cut is recorded on `noted`, and the passage plays.
            # What is still refused whole stands beside it here, so the conversion is read as the
            # narrowing it is rather than as a fence that stopped fencing: a record naming no schema
            # is refused, and so is a name closed to a score (the row below).
            bad = br.evaluate(
                "JSON.stringify(window.__exPass.score({schema:1,intent:'a',shader:'x'}))")
            good = br.evaluate(
                "JSON.stringify(window.__exPass.score({schema:1,intent:'a',"
                "params:{flightMs:900}}))")
            noschema = br.evaluate("JSON.stringify(window.__exPass.score({intent:'a'}))")
            cut = json.loads(bad)
            check(BROWSER_ROWS[5],
                  cut["ok"] is True
                  and "shader" not in cut["score"]
                  and any("shader" in n for n in (cut["noted"] or []))
                  and json.loads(good)["ok"] is True
                  and json.loads(good)["noted"] is None
                  and json.loads(noschema)["ok"] is False,
                  f"bad={bad} good={good} noschema={noschema}")

            # 6 · diagnostics and the quality tier are closed to a score
            closed = br.evaluate(
                "JSON.stringify(window.__exPass.score({schema:1,params:{diagnostics:'on'}}))")
            check(BROWSER_ROWS[6],
                  json.loads(closed)["ok"] is False and "closed to a score" in json.loads(closed)["why"],
                  f"closed={closed}")

            # 7 · one step, one command, one landing
            enter(br, base, "diagnostics:on")
            g0 = gen_now(br)
            br.key("ArrowDown")
            br.sleep(1.6)
            rep = report(br)
            fresh = since(rep, g0)
            starts = [e for e in fresh if e["name"] == "nav-start" and e["kind"] == "step"]
            lands = [e for e in fresh if e["name"] == "nav-land"]
            paired = bool(starts) and bool(lands) and lands[-1]["gen"] == starts[-1]["gen"]
            check(BROWSER_ROWS[7],
                  paired and starts[-1]["cause"] == "step" and starts[-1]["to"],
                  f"starts={starts[-1:]} lands={lands[-1:]}")

            # 8 · a second input supersedes the first
            g0 = gen_now(br)
            br.key("ArrowDown")
            br.sleep(0.08)
            br.key("ArrowDown")
            br.sleep(1.6)
            rep = report(br)
            fresh = since(rep, g0)
            aborts = [e for e in fresh if e["name"] == "nav-abort" and e["why"] == "superseded"]
            gens = [e["gen"] for e in fresh if e["name"] == "nav-start"]
            check(BROWSER_ROWS[8],
                  bool(aborts) and len(gens) >= 2 and gens[-1] > gens[0],
                  f"aborts={aborts[:1]} gens={gens}")

            # 9 · the walk's own arrival is a jump, declared like any other move
            enter(br, base, "diagnostics:on")
            rep = report(br)
            hangs = [e for e in rep["events"] if e["kind"] == "jump" and e["cause"] == "hang"]
            check(BROWSER_ROWS[9], bool(hangs), f"jump events={[e['cause'] for e in rep['events']][:8]}")

            # 10 · the snapshot is frozen: a value changed mid-flight leaves the running command
            # alone and lands on the NEXT one.
            # a slow clock keeps the flight in the air long enough to be read while it runs
            br.evaluate("localStorage.setItem('ex-tempo','3')")
            br.reload()
            ready(br)
            br.sleep(0.4)
            br.evaluate("sessionStorage.setItem('ex-pass',JSON.stringify({diagnostics:'on',flightMs:1200}))")
            before = row(report(br), "flightMs")["applied"]
            br.key("ArrowDown")
            br.evaluate("sessionStorage.setItem('ex-pass',JSON.stringify({diagnostics:'on',flightMs:300}))")
            inflight = br.evaluate(
                "(()=>{const n=window.__exPass.report().nav;"
                "return n?String(n.params.flightMs):'none';})()")
            br.sleep(1.6)
            after = row(report(br), "flightMs")["applied"]
            if inflight == "none":
                skip(BROWSER_ROWS[10], "the flight had already landed at the read — no command to read")
            else:
                check(BROWSER_ROWS[10],
                      before == 1200 and inflight == "1200" and after == 300,
                      f"before={before} in-flight={inflight} after={after}")

            # 11 · a closer look opening mid-flight stops the flight (red on the three-flag bug)
            enter(br, base, "diagnostics:on")
            br.evaluate("localStorage.setItem('ex-tempo','3')")
            br.reload()
            ready(br)
            br.sleep(0.4)
            g0 = gen_now(br)
            br.key("ArrowDown")
            br.sleep(0.08)
            # the closer look opens on a two-finger touch, the road test_zoom drives it by
            br.evaluate("(%s)('.exh-frame img.work')" % PINCH)
            br.sleep(0.6)
            opened = br.evaluate("String(document.documentElement.classList.contains('ex-face'))") == "true"
            rep = report(br)
            fresh = since(rep, g0)
            # PASS-API §10.3 adds adapter.interrupt("zoom"), called the instant the closer look opens
            # — before the per-frame faceStands() guard this row was written against (the three-flag
            # bug) even gets a tick, so it now wins the abort's reason. Both stop the SAME flight; the
            # row's own guarantee (a closer look mid-flight stops it) keeps its full force either way.
            faced = [e for e in fresh if e["name"] == "nav-abort" and e["why"] in ("a face stands", "zoom")]
            if not opened:
                skip(BROWSER_ROWS[11], "the closer look did not open on a plain click in this build")
            else:
                check(BROWSER_ROWS[11], bool(faced),
                      f"events={[(e['name'], e['why']) for e in fresh]}")

            # 12 · the layer's file stays unfetched while the setting is off
            br.net_capture()
            enter(br, base, "diagnostics:on")
            br.net_clear()
            br.key("ArrowDown")
            br.sleep(1.2)
            asked = [u for u in br.net_log() if "pass-layer" in u]
            check(BROWSER_ROWS[12],
                  not asked and report(br)["layer"] == "absent",
                  f"requests={asked} layer={report(br)['layer']}")

            # 13 · the setting preloads it while the room is built, and the walk still steps
            enter(br, base, "diagnostics:on,visualLayer:pass")
            br.net_clear()
            y0 = int(br.evaluate("String(Math.round(scrollY))") or 0)
            br.key("ArrowDown")
            br.sleep(1.6)
            rep = report(br)
            got = [u for u in br.net_log() if "pass-layer" in u]
            y1 = int(br.evaluate("String(Math.round(scrollY))") or 0)
            check(BROWSER_ROWS[13],
                  not got and rep["layer"] == "registered" and y1 > y0
                  and rep["device"]["webgl2"] is True,
                  f"requests-after-gesture={len(got)} layer={rep['layer']} scroll {y0}->{y1} webgl2={rep['device']['webgl2']}")

            # 14 · a visitor who asked for less motion is still sent the picture's file (charter
            # shelf 19's pardoned floor, naряд S-08, 2026-08-26). Before this naряд the layer refused
            # itself outright here and pass-layer.js was never asked for; the walk fell through to
            # its own glide at TEMPO 0.05, which reads as breaking rather than a passage playing
            # calmly. Now the layer is offered exactly as for any other visitor — it is the SCORE
            # that stays calm (row 17 below), not the layer refusing itself.
            #
            # THE GROUND TRUTH IS `rep["layer"]`, NOT THE NETWORK LOG. Row 13, right above, already
            # fetched pass-layer.js in this same browser session — a fresh `enter()` re-executes the
            # module from scratch (`passState`/`passLayer` reset with the navigation), but the file
            # itself may now answer from the browser's own disk cache with no new entry on
            # `net_log()`, so a row asking whether the FILE WAS EVER REQUESTED must not read that log
            # a second time. `rep["layer"]` is the one fact the module itself reports and it answers
            # for a fresh navigation regardless of the wire under it.
            #
            # THE REFUSAL FILTER NAMES THE LAYER, NOT ONLY THE REASON. `passRecordsAskFor` (the
            # composed-pass records wave, a wholly different subsystem — it never needed the layer to
            # begin with) also stands down for "reduced motion", on its own unrelated row of the
            # refusal ring, and reading the reason alone caught that row instead of the layer's own.
            # `what == "layer"` is `passOpen`'s own refusal shape (`passNote(passRefusals, {what:
            # "layer", ...})`), so this reads exactly the fact this row is about.
            br.emulate_media(prefers_reduced_motion="reduce")
            enter(br, base, "diagnostics:on,visualLayer:pass")
            br.key("ArrowDown")
            br.sleep(1.6)
            rep = report(br)
            said = [r for r in rep["refusals"]
                    if r.get("what") == "layer" and r.get("why") == "reduced motion"]
            check(BROWSER_ROWS[14],
                  rep["layer"] == "registered" and not said
                  and rep["device"]["reduced"] is True,
                  f"refusals={said[:1]} layer={rep['layer']} device={rep['device']}")
            br.emulate_media()

            # 15 · the rest record follows the dock — red on U10 §4b's five rows.
            #
            # THE SCENARIO IS THE MATRIX'S OWN: a device change arrives while a renderer holds the
            # command, and the NEXT one throws the walk back to the work it came from. The frame
            # heights here are chosen so the turn reproduces the road exactly. The walk's sections
            # are one viewport tall, so a walk resting on frame 1 stands at scrollY = 900; halving
            # the height mid-crossing puts that same offset on frame 2 — the ARRIVING work — inside
            # the watcher's own 250 ms reflow guard, which is the one report that would have named
            # it. The handoff then places the walk at the very same offset, so no threshold is
            # crossed and no second report ever comes. With the record left uncorrected the next
            # turn honours the departing work.
            #
            # THE CROSSING IS DRIVEN UNDER REDUCED MOTION, WHICH IS THE ONLY ROAD ON THIS BAKE THAT
            # PUTS A SCORE ON A STEP. `passOffer` declines a scoreless command before the layer is
            # ever asked (Phase 3c, 2026-08-31 — «no score composed for this pair, the walk's own
            # glide»), and this suite's site carries no `pass.records.route`, so every ordinary step
            # here composes nothing and no host is ever offered anything: the stub below would take
            # no command at all and the row would read as a walk that never crossed. Reduced motion
            # composes `passReducedScore` from the direction alone, needing no record and no
            # composer file, so the step reaches the stub exactly as any scored step would. Row 17
            # below already drives the stub this way for the same reason. What this row measures —
            # where the walk rests after a device change lands mid-crossing — reads nothing about
            # motion preference, so the vehicle changes and the law does not.
            br.emulate_media(prefers_reduced_motion="reduce")
            enter(br, base, "diagnostics:on,visualLayer:pass")
            br.key("ArrowDown")                     # the step that fetches the picture's own file
            br.sleep(1.8)
            door = br.evaluate(STUB_HOST)
            if door != "registered":
                for i in (15, 16):
                    skip(BROWSER_ROWS[i], f"the seam's registration door never opened: {door}")
            else:
                start = where(br)
                ids = json.loads(br.evaluate(
                    "JSON.stringify([].slice.call(document.querySelectorAll('.exh-frame'))"
                    ".map(function(e){return e.dataset.id;}))"))
                br.key("ArrowDown")                 # the crossing the host takes and holds
                br.sleep(0.5)
                held = br.evaluate("String(!!(window.__stub && window.__stub.active))")
                br.set_viewport(1280, 450)          # the device changes mid-crossing (INV-86)
                br.sleep(0.5)
                arrived = br.evaluate(STUB_SETTLE)
                br.sleep(0.7)
                docked = where(br)
                br.set_viewport(1280, 900)          # and the NEXT device change, at the rest
                br.sleep(0.8)
                after = where(br)
                check(BROWSER_ROWS[15],
                      held == "true" and start["i"] == 1 and arrived == ids[2]
                      and docked["id"] == ids[2] and after["id"] == ids[2],
                      f"the walk rested on {start['id']} (frame {start['i']}), the host held the "
                      f"crossing to {arrived}, a turn arrived mid-crossing, the crossing docked on "
                      f"{docked['id']} and the next turn left the walk on {after['id']} — the work "
                      f"it came from is {start['id']}")

                # 16 · a second gesture mid-crossing chains — red on U10 §3's four rows.
                # EX-GLIDE (SPEC.md:1329-1331): a new input mid-transition chains to the NEXT frame
                # and never re-rounds backward. While a renderer holds the command the walk's own
                # scroll has not moved, so a step counted from it re-declares the very crossing
                # already in flight — the visitor's second swipe buys a shortened passage and no
                # progress. The two declarations are read off the seam's own event ring.
                enter(br, base, "diagnostics:on,visualLayer:pass")
                br.key("ArrowDown")
                br.sleep(1.8)
                br.evaluate(STUB_HOST)
                # the walk deals its works afresh every visit, so this visit's order is read again
                ids = json.loads(br.evaluate(
                    "JSON.stringify([].slice.call(document.querySelectorAll('.exh-frame'))"
                    ".map(function(e){return e.dataset.id;}))"))
                stood = where(br)
                g0 = gen_now(br)
                br.key("ArrowDown")                 # the crossing, taken and held
                br.sleep(0.5)
                br.key("ArrowDown")                 # the second gesture, mid-crossing
                br.sleep(0.6)
                starts = [e for e in since(report(br), g0)
                          if e["name"] == "nav-start" and e["kind"] == "step"]
                first = starts[0]["to"] if starts else None
                second = starts[1]["to"] if len(starts) > 1 else None
                check(BROWSER_ROWS[16],
                      stood["i"] == 1 and len(starts) >= 2 and first == ids[2]
                      and second == ids[3],
                      f"from {stood['id']} the walk declared {len(starts)} steps while the host "
                      f"held the command: first to {first}, then to {second}; the frames in order "
                      f"are {ids[1:4]}")
                br.set_viewport(1280, 900)

            # 17 · the pardoned floor itself: one voice, no miracle, no camera flight, a duration at
            # the quiet tier's own floor (charter shelf 19, naряд S-08). STUB_HOST intercepts the
            # real `cmd` the host is offered — the score `passReducedScore` composes — without
            # needing the real drawing layer's own WebGL instruments to be loaded at all.
            br.emulate_media(prefers_reduced_motion="reduce")
            enter(br, base, "diagnostics:on,visualLayer:pass")
            br.net_clear()
            br.key("ArrowDown")                     # fetches pass-layer.js (row 14 above)
            br.sleep(1.6)
            door = br.evaluate(STUB_HOST)
            if door != "registered":
                for i in (17, 18):
                    skip(BROWSER_ROWS[i], f"the seam's registration door never opened: {door}")
            else:
                br.key("ArrowDown")                 # the reduced-motion crossing the stub captures
                br.sleep(0.6)
                got = json.loads(br.evaluate(
                    "JSON.stringify({active: !!(window.__stub && window.__stub.active), "
                    "score: (window.__stub && window.__stub.cmd) ? window.__stub.cmd.score : null})"))
                score = got.get("score") or {}
                cues = score.get("cues") or []
                camera = score.get("camera") or {}
                voices = [c.get("voice") for c in cues]
                check(BROWSER_ROWS[17],
                      got.get("active") is True and len(cues) == 1 and voices == ["letter"]
                      and not camera.get("lead") and not camera.get("track")
                      and score.get("duration") == 2000,
                      f"active={got.get('active')} cues={voices} camera={camera} "
                      f"duration={score.get('duration')}")

                # 18 · the same crossing never asked for the composer's own file (EX-COMPOSED's law
                # holds even here: the floor is a fixed grammar, never a genre pass-composer.js
                # picks, so a reduced visit whose floor actually plays still never fetches it).
                rep = report(br)
                asked_composer = [u for u in br.net_log() if "pass-composer" in u]
                check(BROWSER_ROWS[18],
                      not asked_composer and rep["composer"]["state"] == "absent",
                      f"requests={asked_composer} composer.state={rep['composer']['state']}")
            br.emulate_media()

            # 19 · the register names nothing the settings record already owns — red on U8's find,
            # still standing at U10 §5. The bake writes the instrument ADDRESS record into the
            # settings block under `pass.instruments`; a register setting of that same name read the
            # record off the site rung and refused it, «wants a list», about four times per step.
            # The ring holds 64 rows, so within ten steps every real refusal had been pushed off it
            # — which is why U10 had to read the layer's own word one step into the visit. Both
            # halves are read here: no such note is minted, and the layer's own refusal, minted at
            # the first step, still stands ten steps later.
            #
            # THE STANDING NOTE IS SAVE-DATA, NOT REDUCED MOTION, SINCE THIS naряд (S-08, 2026-08-26,
            # charter shelf 19's pardoned floor): reduced motion no longer refuses the layer at all —
            # it plays the floor grammar instead (row 14 above), which is exactly why it can no
            # longer serve as this row's long-lived refusal. Save-Data is the one decline this naряд
            # left untouched, so it takes over the same job here.
            br.inject("Object.defineProperty(navigator, 'connection', "
                      "{get: function () { return {saveData: true}; }, configurable: true});")
            enter(br, base, "diagnostics:on,visualLayer:pass")
            for _ in range(10):
                br.key("ArrowDown")
                br.sleep(0.25)
            rep = report(br)
            owned = [r for r in rep["refusals"]
                     if r.get("what") == "setting" and r.get("name") in ("instruments",
                                                                         "instrumentNames")]
            layer_said = [r for r in rep["refusals"] if r.get("why") == "save data"]
            names = sorted(s["name"] for s in rep["settings"] if s)
            check(BROWSER_ROWS[19],
                  not owned and bool(layer_said) and "instruments" not in names
                  and "instrumentNames" in names,
                  f"after ten steps the ring carries {len(rep['refusals'])} refusals; notes about a "
                  f"setting the record owns: {owned[:2]}; the layer's own «save data» note "
                  f"still on the ring: {bool(layer_said)}; the register's names are {names}")

    # 20 · RED-ON-BUG. Naряд S-08's own two decline-lines are reverted in a COPY of the built
    # artifact — never the source tree, never git (the same convention tests/test_pass_coverage.py
    # documents over its own `red_pack`) — and the row passes when the answer MOVES: with the
    # naряд's text in place a reduced visit's layer takes the crossing; reverted to the pre-S-08
    # text, the same visit's registration door never opens at all, which is the bug rows 14/17/18
    # above exist to have fixed.
    import shutil  # noqa: E402

    def stub_gets_offered(served_base):
        with Browser(width=1280, height=900) as brx:
            brx.emulate_media(prefers_reduced_motion="reduce")
            enter(brx, served_base, "diagnostics:on,visualLayer:pass")
            brx.key("ArrowDown")
            brx.sleep(1.6)
            door = brx.evaluate(STUB_HOST)
            if door != "registered":
                return {"door": door, "active": False}
            brx.key("ArrowDown")
            brx.sleep(0.6)
            got = json.loads(brx.evaluate(
                "JSON.stringify({active: !!(window.__stub && window.__stub.active)})"))
            got["door"] = door
            return got

    with serve(TMP) as base_now:
        now = stub_gets_offered(base_now)

    HURT = JS.replace(
        'if (cmd.saveData) {\n      passMark("visual-declined", cmd, "save data");',
        'if (cmd.reduced || cmd.saveData) {\n      passMark("visual-declined", cmd, '
        'cmd.reduced ? "reduced motion" : "save data");',
        1,
    ).replace(
        'const no = dataSaver() ? "save data" : passCan() ? null : "no webgl2";',
        'const no = REDUCED ? "reduced motion" : dataSaver() ? "save data" : passCan() ? '
        'null : "no webgl2";',
        1,
    )
    moved = HURT != JS
    HURT_DIR = Path(tempfile.mkdtemp(prefix="synth_pass_hurt_"))
    shutil.copytree(TMP, HURT_DIR, dirs_exist_ok=True)
    (HURT_DIR / "exhibition.js").write_text(HURT, encoding="utf-8")
    with serve(HURT_DIR) as base_hurt:
        hurt = stub_gets_offered(base_hurt)
    shutil.rmtree(HURT_DIR, ignore_errors=True)

    check(BROWSER_ROWS[20],
          moved and now.get("active") is True and hurt.get("active") is not True,
          f"with naряд S-08's two lines in place a reduced visit's layer took the crossing "
          f"({now}); reverted to the pre-S-08 text the same visit's door read "
          f"{hurt.get('door')!r} and active={hurt.get('active')}")

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
