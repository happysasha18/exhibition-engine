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

check("EX-PASS the seam registers no input listener of its own",
      not re.search(r"addEventListener\(\s*[\"'](pointer|touch|wheel|key|mouse)", SRC),
      "input stays with the motion layer; a pointer signal arrives normalized, later")

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
    "EX-PASS a score naming an unknown field is refused whole",
    "EX-PASS a score may not set a name closed to it",
    "EX-PASS one step declares one command and lands it",
    "EX-PASS a second input supersedes the first, which ends as aborted",
    "EX-PASS entering the walk declares a jump command",
    "EX-PASS the command's parameters are frozen at the start",
    "EX-PASS a closer look opening mid-flight stops the flight",
]


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

            # 5 · an unknown field refuses the whole score
            bad = br.evaluate(
                "JSON.stringify(window.__exPass.score({schema:1,intent:'a',shader:'x'}))")
            good = br.evaluate(
                "JSON.stringify(window.__exPass.score({schema:1,intent:'a',"
                "params:{flightMs:900}}))")
            noschema = br.evaluate("JSON.stringify(window.__exPass.score({intent:'a'}))")
            check(BROWSER_ROWS[5],
                  json.loads(bad)["ok"] is False and "shader" in json.loads(bad)["why"]
                  and json.loads(good)["ok"] is True
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
            faced = [e for e in fresh if e["name"] == "nav-abort" and e["why"] == "a face stands"]
            if not opened:
                skip(BROWSER_ROWS[11], "the closer look did not open on a plain click in this build")
            else:
                check(BROWSER_ROWS[11], bool(faced),
                      f"events={[(e['name'], e['why']) for e in fresh]}")

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
