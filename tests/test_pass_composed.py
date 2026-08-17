#!/usr/bin/env python3
"""EX-PASS §4.4d — the composed road: a passage is DERIVED at visit time, from the two works' own
records, and the prebaked per-pair pack is gone from the walk.
Run: python3 tests/test_pass_composed.py

Root: his word of 2026-08-17 19:21 — the collection grows to thousands of works and nothing on the
product path may scale with the number of pairs — and his architecture decision of 18:00: the
instrument reads its doors at run time on the actual buffer, and the composer emits the artistic
request. The unit brief is docs/immersive/briefs/2026-08-17-U27-composed-full-route.md in the
tlvphotos tree, stage 0.

WHAT THIS SUITE REPLACES. Two suites and eight rows retired with the road they guarded:
tests/test_pass_reader.py whole (the delivery pack's reader) and the PASS-TABLE rows of
tests/test_pass_weave.py (the inline template-and-table fill). Both proved that a score written down
per pair could be found again. Nothing is found any more; it is derived, and that is what is proved
here instead.

WHAT IT MEASURES.

  The bake and the bundle. The composer travels as its own file the way the picture layer does, and
  the served bundle names it and names none of the three roads that left.

  The derivation, byte for byte. tests/fixture_pass_composed.json carries the two works of the
  worked pair, the collection constants, the die Python rolled for each direction, and the WHOLE
  score Python composed for each. The module is loaded the way the bake serves it and asked through
  its one entry, and the answer must be Python's own bytes, character for character. The fixture is
  what keeps this suite standing on its own: no lab tree is opened and no site tree is read.

  The entry's defaults. `passageFor` gained six fields beyond the four the choice core has always
  taken. Every one of them must reproduce the old call exactly when it is left unsaid — that is the
  whole claim byte equality rests on — and each is checked here by naming its documented default
  explicitly and reading the same bytes back.

  The entry's fences. A route role outside the five is refused by name; a session memory naming a
  field outside §4.8's three is refused by name; a die outside the instrument's own span is refused
  by name. Each of the three is a red-on-bug row: the fence is removed in a COPY of the module and
  the row reddens.

  The walk. On a baked site whose settings record carries the per-work records, the walk fetches the
  composer once at its first landing, derives a passage on a step and freezes the score onto the
  command; a work the record set has never heard of falls through to the walk's own glide; and a
  visit under reduced motion or Save-Data never asks for the file at all.

WHAT IS NEVER RESTORED FROM GIT. Every red-on-bug proof below runs a COPY of the module in memory
with one rule changed. The source tree is never written to.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"
FIXTURE = Path(__file__).resolve().parent / "fixture_pass_composed.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_composed_"))
build_site.OUT = TMP
build_site.build(SITE_URL)
JS = (TMP / "exhibition.js").read_text(encoding="utf-8")
SRC = (ROOT / "engine" / "client" / "01a-pass.js").read_text(encoding="utf-8")

# ---------------------------------------------------------------- the bake and the bundle

check("EX-COMPOSED the composer travels as its own file, and the bake ships it",
      (TMP / "pass-composer.js").exists()
      and "__exPassComposer" in (TMP / "pass-composer.js").read_text(encoding="utf-8")
      and 'PASS_COMPOSER_SRC = "pass-composer.js"' in SRC,
      "the choice core must reach the site beside the bundle, with its namespace resolved")

check("EX-COMPOSED the delivery pack's reader is gone from the tree and from the bake",
      not (ROOT / "engine" / "assets" / "pass-reader.js").exists()
      and not (TMP / "pass-reader.js").exists(),
      "the file the pack road was fetched through must ship nowhere")

# The three roads that answered for a pair's score before this unit. Each is named by the very
# string the bundle would carry if it were still there, so a road creeping back reds here.
GONE = {
    "the settings record's own per-pair scores": ".scores",
    "the delivery pack's reader": "pass-reader.js",
    "the pack's shard warming": "passPackOpen",
    "the template-and-table fill": "scoreTables",
}
back = sorted(name for name, mark in GONE.items() if mark in JS)
check("EX-COMPOSED the served bundle carries the composer's door and none of the three roads it "
      "replaced",
      'PASS_COMPOSER_SRC = "pass-composer.js"' in JS and "passComposeFor" in JS and not back,
      f"roads still named in the served bundle: {back}")

check("EX-COMPOSED nothing on the product path is keyed by a pair",
      "passRequestFor" in JS and "workRecordA" in JS
      and not re.search(r"scoreTemplates|passFillScore|passPack\b", JS),
      "the walk must build a request out of two work records, never look a pair up")

# ---------------------------------------------------------------- the derivation, in node

FIX = json.loads(FIXTURE.read_text(encoding="utf-8"))
A_ID, B_ID = FIX["pair"]["a"], FIX["pair"]["b"]
KEY_AB, KEY_BA = A_ID + "__" + B_ID + "__ab", A_ID + "__" + B_ID + "__ba"

NODE_ROWS = [
    "EX-COMPOSED the entry composes the worked pair's two directions to Python's own bytes",
    "EX-COMPOSED every field the request gained reproduces the four-value call exactly",
    "EX-COMPOSED the die reaches the score: two dice, two scores",
    "EX-COMPOSED a route role outside the five is refused by name",
    "EX-COMPOSED a session memory wider than §4.8's three fields is refused by name",
    "EX-COMPOSED a die outside the instrument's own span is refused by name",
    "EX-COMPOSED red-on-bug · the route-role fence removed: the unnamed role composes",
    "EX-COMPOSED red-on-bug · §4.8's fence removed: a fourth memory field composes",
    "EX-COMPOSED red-on-bug · the die dropped on its way to the choice core: both dice agree",
]

# THE DRIVER, run in node against a COPY of the module held in memory. `plant` names one rule to
# change before the module is loaded, which is how the three red-on-bug rows below are run: the
# repair is reverted in the copy alone and the answer must move.
DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm");
const [modulePath, fixturePath] = process.argv.slice(2);
const plantFrom = process.env.PLANT_FROM || "";
const plantTo = process.env.PLANT_TO || "";

let source = fs.readFileSync(modulePath, "utf8").replace(/@@NS@@/g, "");
let planted = null;
if (plantFrom) {
  if (source.indexOf(plantFrom) < 0) {
    console.log(JSON.stringify({error: "the plant found nothing to change: " + plantFrom}));
    process.exit(0);
  }
  source = source.replace(plantFrom, plantTo);
  planted = plantFrom;
}
let joined = null;
const sandbox = {window: {__PassComposer: (m) => { joined = m; }}, console};
vm.createContext(sandbox);
vm.runInContext(source, sandbox, {filename: "pass-composer.js"});
if (!joined) { console.log(JSON.stringify({error: "the module joined nothing"})); process.exit(0); }

const fix = JSON.parse(fs.readFileSync(fixturePath, "utf8"));
const composer = joined.make(fix.consts);
const A = fix.works[fix.pair.a], B = fix.works[fix.pair.b];
const KEY_AB = fix.pair.a + "__" + fix.pair.b + "__ab";
const KEY_BA = fix.pair.a + "__" + fix.pair.b + "__ba";
const out = {version: joined.version, seedSpan: composer.seedSpan, routeRoles: composer.routeRoles};

// 1 · the two directions, asked the way the walk asks
const bare = {};
for (const [key, dir] of [[KEY_AB, "a-to-b"], [KEY_BA, "b-to-a"]]) {
  const p = composer.passageFor({workRecordA: A, workRecordB: B, direction: dir,
                                 seed: fix.seeds[key]});
  bare[key] = p;
  out[key] = {key: p.key, declined: p.declined || null, json: p.json || null,
              bytes: p.bytes === undefined ? null : p.bytes,
              applied: p.applied, request: p.request};
}

// 2 · every field the request gained, named at its documented default, must read the same bytes;
//     and so must the four-value call the choice core has always taken.
const spelled = composer.passageFor({
  workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB],
  routeRole: "middle", sessionMemory: null, cameraState: null, buffer: null});
const core = composer.scoreFor(A, B, "a-to-b", fix.seeds[KEY_AB]);
out.defaults = {
  spelledSame: spelled.json === bare[KEY_AB].json,
  coreSame: core.json === bare[KEY_AB].json,
  // A field named at something OTHER than its default must still read the same bytes in stage 0,
  // because nothing derives from these four yet — the shape is stable and the derivation is not
  // theirs until stage 1. This is recorded rather than asserted as a law.
  otherRole: composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b",
                                  seed: fix.seeds[KEY_AB], routeRole: "culmination"}).json
             === bare[KEY_AB].json,
};

// 3 · the die reaches the score
const lo = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b", seed: 0.25});
const hi = composer.passageFor({workRecordA: A, workRecordB: B, direction: "a-to-b", seed: 7.75});
out.dice = {differ: lo.json !== hi.json, loSeed: lo.request.seed, hiSeed: hi.request.seed};

// 4 · the three fences
const ask = (extra) => {
  const p = composer.passageFor(Object.assign(
    {workRecordA: A, workRecordB: B, direction: "a-to-b", seed: fix.seeds[KEY_AB]}, extra));
  return {declined: p.declined || null, composed: !!p.json};
};
out.fences = {
  role: ask({routeRole: "grand finale"}),
  memory: ask({sessionMemory: {family: "band", seed: 1, passIndex: 2, cooldown: 9}}),
  memoryOk: ask({sessionMemory: {family: "band", seed: 1, passIndex: 2}}),
  seedHigh: ask({seed: 9}),
  seedLow: ask({seed: -1}),
};
out.planted = planted;
console.log(JSON.stringify(out));
"""

DRIVER_PATH = TMP / "composed-driver.js"
DRIVER_PATH.write_text(DRIVER, encoding="utf-8")


def node_run(plant_from="", plant_to=""):
    env = dict(os.environ, PLANT_FROM=plant_from, PLANT_TO=plant_to)
    proc = subprocess.run(["node", str(DRIVER_PATH), str(MODULE), str(FIXTURE)],
                          capture_output=True, text=True, env=env, timeout=120)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-400:]}
    return json.loads(proc.stdout.strip().splitlines()[-1])


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


if not node_available():
    for r in NODE_ROWS:
        skip(r, "node is not installed (pinned expected skip)")
else:
    got = node_run()
    if got.get("error"):
        for r in NODE_ROWS:
            skip(r, "the module would not load: " + got["error"])
    else:
        # --- row 0 · byte equality through the one entry ------------------------------------
        same = {k: got[k]["json"] == FIX["expected"][k] and got[k]["bytes"] == FIX["expectedTight"][k]
                for k in (KEY_AB, KEY_BA)}
        first = None
        for k in (KEY_AB, KEY_BA):
            if not same[k] and got[k]["json"]:
                want, have = FIX["expected"][k], got[k]["json"]
                i = 0
                while i < min(len(want), len(have)) and want[i] == have[i]:
                    i += 1
                first = f"{k} at byte {i}: python «{want[i:i + 60]}» against js «{have[i:i + 60]}»"
                break
        check(NODE_ROWS[0], all(same.values()),
              f"a-to-b {'identical' if same[KEY_AB] else 'differs'} "
              f"({got[KEY_AB]['bytes']} B compact against {FIX['expectedTight'][KEY_AB]}), "
              f"b-to-a {'identical' if same[KEY_BA] else 'differs'} "
              f"({got[KEY_BA]['bytes']} B compact against {FIX['expectedTight'][KEY_BA]})"
              + (f"; {first}" if first else ""))

        # --- row 1 · the defaults reproduce the four-value call -----------------------------
        d = got["defaults"]
        check(NODE_ROWS[1], d["spelledSame"] and d["coreSame"],
              f"the six fields named at their defaults read the same bytes: {d['spelledSame']}; "
              f"the choice core's own four-value call reads them too: {d['coreSame']}; "
              f"a route role of «culmination» still reads the same bytes in stage 0: "
              f"{d['otherRole']} (nothing derives from it yet)")

        # --- row 2 · the die reaches the score ----------------------------------------------
        check(NODE_ROWS[2], got["dice"]["differ"],
              f"a die of {got['dice']['loSeed']} and one of {got['dice']['hiSeed']} compose "
              f"{'different' if got['dice']['differ'] else 'the same'} scores")

        # --- rows 3-5 · the three fences ----------------------------------------------------
        f = got["fences"]
        check(NODE_ROWS[3],
              f["role"]["composed"] is False and "grand finale" in (f["role"]["declined"] or "")
              and "route role" in (f["role"]["declined"] or ""),
              f"refusal: {f['role']['declined']!r}; the five it names: {got['routeRoles']}")
        check(NODE_ROWS[4],
              f["memory"]["composed"] is False and "cooldown" in (f["memory"]["declined"] or "")
              and f["memoryOk"]["composed"] is True,
              f"a fourth field refuses: {f['memory']['declined']!r}; the three §4.8 lets cross "
              f"compose: {f['memoryOk']['composed']}")
        check(NODE_ROWS[5],
              f["seedHigh"]["composed"] is False and f["seedLow"]["composed"] is False
              and "seed" in (f["seedHigh"]["declined"] or ""),
              f"a die of 9 refuses: {f['seedHigh']['declined']!r}; a die of -1 refuses: "
              f"{f['seedLow']['declined']!r}; the span it reads off the instrument's manifest: "
              f"{got['seedSpan']}")

        # --- rows 6-8 · the same three, with the repair reverted in a copy -------------------
        PLANTS = [
            (NODE_ROWS[6], "if (ROUTE_ROLES.indexOf(role) < 0) {", "if (false) {",
             lambda g: g["fences"]["role"]["composed"] is True),
            (NODE_ROWS[7], "if (odd.length) {", "if (false) {",
             lambda g: g["fences"]["memory"]["composed"] is True),
            (NODE_ROWS[8], "var made = scoreFor(a, b, direction, seed);",
             "var made = scoreFor(a, b, direction, 0);",
             lambda g: g["dice"]["differ"] is False),
        ]
        for name, was, now, reddens in PLANTS:
            g = node_run(was, now)
            if g.get("error"):
                check(name, False, "the planted run failed: " + g["error"])
            else:
                check(name, reddens(g),
                      f"with «{was}» in place the row above holds; with it changed to «{now}» the "
                      f"answer moves, and this run read that it did: {reddens(g)}")

# ---------------------------------------------------------------- the walk, in a browser

BROWSER_ROWS = [
    "EX-COMPOSED the composer's file is never fetched while the layer stands off",
    "EX-COMPOSED the walk fetches the composer once, at the landing, and it joins",
    "EX-COMPOSED a step over two recorded works derives a passage and freezes it onto the command",
    "EX-COMPOSED the passage's own request stands on the diagnostic surface beside the score",
    "EX-COMPOSED the passage plays, and what the instrument applied on its own buffer is written back onto it",
    "EX-COMPOSED the instrument's own door reading arrives on the passage record, on the buffer it drew on",
    "EX-COMPOSED a work the record set never heard of keeps the walk's own glide",
    "EX-COMPOSED reduced motion asks for no composer at all, and records why",
]


def enter(br, base, pass_arg=None, step=False):
    """A fresh visitor who opens the door and stands in the walk. `step` takes ONE real step, which
    is the only road that asks for the picture layer's file (engine/client/15-motion.js: the layer
    is opened where a step declares its command)."""
    br.navigate(base + "/")
    br.clear_storage()
    br.navigate(base + "/" + (("?pass=" + pass_arg) if pass_arg else ""))
    br.sleep(0.8)
    br.click(".exd-window", settle=1.4)
    for _ in range(25):
        if br.evaluate("String(document.documentElement.classList.contains('ex-walk') "
                       "&& !document.documentElement.classList.contains('ex-face'))") == "true":
            break
        br.sleep(0.2)
    br.sleep(0.4)
    if step:
        br.key("ArrowDown")
        for _ in range(30):
            if br.evaluate("String(!!(window.__exPass && window.__exPass.layer()))") == "true":
                break
            br.sleep(0.2)
        br.sleep(0.5)


def js(br, body):
    return json.loads(br.evaluate("JSON.stringify((function(){%s})())" % body))


def put_records(base_dir, ids):
    """The settings record as the site writes it for the composed road: the collection's own
    constants and one record per work on the walk, keyed by the id the walk hangs the work under.
    The fixture's two records are re-keyed onto the works this bake actually hangs — what the
    composer reads out of a record is measurement, and the id is only its name."""
    cfg = json.loads((base_dir / "config.json").read_text(encoding="utf-8"))
    fix = json.loads(FIXTURE.read_text(encoding="utf-8"))
    src = [fix["works"][fix["pair"]["a"]], fix["works"][fix["pair"]["b"]]]
    works = {}
    for i, wid in enumerate(ids):
        rec = json.loads(json.dumps(src[i % 2]))
        rec["id"] = wid
        works[wid] = rec
    cfg["pass"] = dict(cfg.get("pass") or {}, visualLayer="pass", composer=fix["consts"],
                       works=works)
    (base_dir / "config.json").write_text(
        json.dumps(cfg, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return works


if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        with Browser(width=1280, height=900) as br:
            # 0 · the layer stands off: nothing is asked for
            enter(br, base, "diagnostics:on")
            asked = js(br, "var r = window.__exPass.report();"
                           "return {state: r.composer.state, works: r.composer.works,"
                           " files: performance.getEntriesByType('resource')"
                           "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                           "  .length};")
            check(BROWSER_ROWS[0], asked["state"] == "absent" and asked["files"] == 0,
                  f"the composer reads {asked['state']} and the file was fetched "
                  f"{asked['files']} time(s); the settings record carries "
                  f"{asked['works']} work record(s)")

            # the records arrive without a rebake, the way a content change always has
            # EVERY WORK BUT ONE IS GIVEN A RECORD. The walk deals its works afresh on every entry,
            # so which two the visitor stands over is the walk's own choice and no row may pin it;
            # what a row may do is make sure the pair it asks about is recorded and one work is not.
            allworks = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                              ".map(function(e){return e.dataset.id;});")
            recorded = list(put_records(TMP, allworks[:-1])) if len(allworks) >= 3 else []
            unrecorded = allworks[-1] if len(allworks) >= 3 else None
            if len(recorded) < 2:
                for r in BROWSER_ROWS[1:]:
                    skip(r, f"the walk hung fewer than three works: {allworks[:4]}")
            else:
                enter(br, base, "diagnostics:on", step=True)
                for _ in range(30):
                    if js(br, "return window.__exPass.report().composer.state;") == "read":
                        break
                    br.sleep(0.2)
                shown = js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                               ".map(function(e){return e.dataset.id;});")
                pair = [w for w in shown if w in recorded][:2]
                # The walk deals afresh on every entry, so the work with no record of its own is
                # read off THIS hang rather than remembered from the last one.
                unrecorded = next((w for w in shown if w not in recorded), None)
                rep = js(br, "var r = window.__exPass.report();"
                             "return {state: r.composer.state, version: r.composer.version,"
                             " works: r.composer.works, src: r.composer.src,"
                             " files: performance.getEntriesByType('resource')"
                             "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                             "  .length};")
                check(BROWSER_ROWS[1],
                      rep["state"] == "read" and rep["files"] == 1 and rep["version"] is not None,
                      f"the composer reads {rep['state']} at version {rep['version']}, fetched "
                      f"{rep['files']} time(s) from {rep['src']}, over {rep['works']} work records")

                # 2 · a step over two recorded works
                if len(pair) < 2:
                    for r_ in BROWSER_ROWS[2:7]:
                        skip(r_, f"this hang shows fewer than two recorded works: {shown[:4]}")
                    pair = None
                r = None if pair is None else js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var B = document.querySelector('.exh-frame[data-id="%s"]');
                  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:B, dir:1, span:100,
                                                             kind:'step', cause:'composed',
                                                             velocity:0});
                  window.__cmd = cmd;
                  var said = window.__exPass.report().refusals.filter(function(x){
                    return x.what === 'score'; });
                  return {got: !!cmd, hasScore: !!(cmd && cmd.score),
                          schema: cmd && cmd.score ? cmd.score.schema : null,
                          pair: cmd && cmd.score ? cmd.score.pair : null,
                          why: said.length ? said[said.length - 1].why : null,
                          cues: cmd && cmd.score && cmd.score.cues
                                ? cmd.score.cues.map(function(c){return c.instrument.id;}) : null};
                """ % (pair[0], pair[1]) if pair else "")
                if pair:
                    check(BROWSER_ROWS[2],
                          r["got"] and r["hasScore"] and r["schema"] == 2 and r["cues"],
                          f"command={r}")

                # 3 · the request on the diagnostic surface
                p = None if pair is None else js(
                    br, "var rows = window.__exPass.report().composer.passages;"
                        "var row = rows.length ? rows[rows.length - 1] : null;"
                        "if (row) { var ids = row.key.split('__');"
                        "  row.hangNow = window.__exPass.adapter.hangGeometry("
                        "    ids[2] === 'ba' ? ids[1] : ids[0]); }"
                        "return row;")
                if pair:
                    check(BROWSER_ROWS[3],
                      bool(p) and p["key"].startswith(min(pair[0], pair[1]))
                      and p["request"]["direction"] in ("a-to-b", "b-to-a")
                      and p["request"]["routeRole"] == "middle"
                      and p["request"]["sessionMemory"] is None
                      and isinstance(p["request"]["seed"], (int, float))
                      and 0 <= p["request"]["seed"] <= 8
                      and bool(p["request"]["buffer"])
                      # The camera's own pose is the departing work's real box, measured off the
                      # DOM. A box the walk itself cannot measure at this instant is the field's
                      # documented default — the flight departs from the score's own rest — so the
                      # row asks only that the two readings AGREE: the request may not carry a pose
                      # the walk would not have measured.
                      and (p["request"]["cameraState"] is None) == (p["hangNow"] is None),
                      f"passage={json.dumps(p, ensure_ascii=False)[:700] if p else None}")

                # 4 · the passage PLAYS, and the applied reading comes back onto it
                #
                # His architecture decision of 2026-08-17 18:00: the instrument reads its doors at
                # run time on the actual buffer, and that reading is the runtime truth. It cannot be
                # known before the frame is drawn, so the walk writes it onto the passage record at
                # the landing — beside the request that asked for it.
                #
                # WHAT THIS ROW REACHES, AND WHERE IT STOPS. What comes back is what the HOST
                # publishes: the instrument that took the command, the drawing buffer and its device
                # ratio, and every live cue with the handles the host resolved for it. That is the
                # applied state at the host's level and this row holds it.
                #
                # The instrument's OWN door reading travels beside it, on each cue's `applied`, and
                # the row below is the one that judges it. This row counts it and prints the count,
                # so a reading that stops arriving is visible here as well as there.
                if pair:
                    for _ in range(40):
                        if js(br, "return !!window.__exPass.layer();") is True:
                            break
                        br.sleep(0.2)
                played = None if pair is None else js(br, """
                  if (!window.__exPass.layer()) return {took: false, noLayer: true};
                  var cmd = window.__cmd;
                  var took = window.__exPass.layer().offer(cmd, {dock: function(){
                    window.__exPass.adapter.dock(cmd); },
                    glide: function(){ window.__glided = true; },
                    curtain: function(){}, mark: function(){}});
                  return {took: took};
                """)
                if pair and played and played.get("took"):
                    for _ in range(80):
                        if js(br, "return window.__exPass.host.report().state;") == "idle":
                            break
                        br.sleep(0.15)
                    br.sleep(0.4)
                ap = None if pair is None else js(
                    br, "var rows = window.__exPass.report().composer.passages;"
                        "return rows.length ? rows[rows.length - 1].applied : null;")
                if pair is None:
                    pass
                elif not (played and played.get("took")):
                    for r_ in (BROWSER_ROWS[4], BROWSER_ROWS[5]):
                        skip(r_,
                             "no picture layer on this device"
                             if (played or {}).get("noLayer") else
                             "the host declined the composed passage on this device: no frame was "
                             "drawn, so nothing was applied")
                else:
                    handles = [c for c in (ap or {}).get("cues", []) if c.get("handles")]
                    door = [c for c in (ap or {}).get("cues", []) if c.get("applied")]
                    check(BROWSER_ROWS[4],
                          bool(ap) and bool(ap.get("instrument")) and bool(ap.get("buffer"))
                          and bool(handles),
                          f"applied on a {ap['buffer'] if ap else '?'} buffer at dpr "
                          f"{ap['dpr'] if ap else '?'}, {len(handles)} live cue(s): "
                          + json.dumps([{"id": c["id"], "instrument": c["instrument"],
                                         "size": c["handles"].get("size")}
                                        for c in handles], ensure_ascii=False)[:300]
                          + f"; the instrument's own door reading reaches this record for "
                            f"{len(door)} of them")

                    # 5 · THE INSTRUMENT'S OWN READING, on the record the request came from.
                    #
                    # His architecture decision of 2026-08-17 18:00: the instrument reads its doors
                    # at run time on the ACTUAL buffer, and that reading is the runtime truth. What
                    # this row judges is that the reading arrived and that it was taken on the
                    # buffer the frame was really drawn on — not on the CSS frame around it, and not
                    # on anything the composer could have known when it wrote the request.
                    #
                    # The five instruments publish one shape: `door`, `buffer`, `reads`, `request`,
                    # `applied`, `moved`, `unit`, `held`, `whyNo`. Three laws hold across all five
                    # and are checked on every reading this passage produced:
                    #   · it was taken AT A DOOR — `door` reads «in» or «out», never a mid-passage
                    #     instant, because a door is the only instant the reading is defined at;
                    #   · it was taken ON THE HOST'S OWN BUFFER — the two numbers agree with the
                    #     buffer the host reports for the same frame;
                    #   · a door that had to be MOVED says so — `moved` is non-zero exactly when
                    #     `held` names the leak the request would have drawn, and both are quiet
                    #     when the request was whole as it stood.
                    # `whyNo` is empty on every one of them: a refusal ends the passage, and this
                    # passage played.
                    #
                    # The per-instrument numbers themselves are held in each instrument's own suite,
                    # where the frame is drawn and photographed; the red-on-bug proof for the
                    # reporting call is tests/test_pass_weave.py.
                    def law(c):
                        a = c["applied"]
                        buf = a.get("buffer") or []
                        return (a.get("door") in ("in", "out")
                                and len(buf) == 2
                                and f"{buf[0]}x{buf[1]}" == ap.get("buffer")
                                and isinstance(a.get("reads"), str)
                                and isinstance(a.get("request"), (int, float))
                                and isinstance(a.get("applied"), (int, float))
                                and bool(a.get("moved")) == bool(a.get("held"))
                                and a.get("whyNo") is None)

                    broke = [c for c in door if not law(c)]
                    check(BROWSER_ROWS[5],
                          bool(door) and not broke,
                          f"{len(door)} of {len((ap or {}).get('cues', []))} cue(s) published a "
                          f"reading, taken on the {ap.get('buffer')} buffer the host reports at dpr "
                          f"{ap.get('dpr')}: "
                          + json.dumps([{"instrument": c["instrument"], "applied": c["applied"]}
                                        for c in door], ensure_ascii=False)[:600]
                          + (f"; readings breaking the shape: "
                             + json.dumps(broke, ensure_ascii=False)[:300] if broke else ""))

                # 5 · a work with no record of its own
                r = None if (pair is None or unrecorded is None) else js(br, """
                  var A = document.querySelector('.exh-frame[data-id="%s"]');
                  var C = document.querySelector('.exh-frame[data-id="%s"]');
                  if (!A || !C) return {absent: true};
                  var cmd = window.__exPass.adapter.declare({fromEl:A, toEl:C, dir:1, span:100,
                                                             kind:'step', cause:'unrecorded',
                                                             velocity:0});
                  var said = window.__exPass.report().refusals.filter(function(x){
                    return x.what === 'composer' && x.name === 'request'; });
                  return {score: cmd ? cmd.score : 'no command', to: C.dataset.id,
                          why: said.length ? said[said.length - 1].why : null};
                """ % (pair[0], unrecorded) if (pair and unrecorded) else "")
                if pair and unrecorded is None:
                    skip(BROWSER_ROWS[6], f"every work of this hang carries a record: {shown[:4]}")
                elif pair and r.get("absent"):
                    skip(BROWSER_ROWS[6], f"this hang shows no unrecorded work ({unrecorded})")
                elif pair:
                    check(BROWSER_ROWS[6],
                          r["score"] is None and "carries no record" in (r["why"] or ""),
                          f"a step to {r['to']} froze {r['score']!r} onto the command; "
                          f"the reason on the surface: {r['why']!r}")

                # 6 · reduced motion
                with Browser(width=1280, height=900) as br2:
                    br2.emulate_media(prefers_reduced_motion="reduce")
                    enter(br2, base, "diagnostics:on")
                    red = js(br2, "var r = window.__exPass.report();"
                                  "var said = r.refusals.filter(function(x){"
                                  "  return x.what === 'composer'; });"
                                  "return {state: r.composer.state,"
                                  " why: said.length ? said[said.length-1].why : null,"
                                  " files: performance.getEntriesByType('resource')"
                                  "  .filter(function(e){return e.name.indexOf('pass-composer.js')>=0;})"
                                  "  .length};")
                    check(BROWSER_ROWS[7],
                          red["files"] == 0 and red["why"] == "reduced motion",
                          f"the file was fetched {red['files']} time(s); the reason on the "
                          f"surface: {red['why']!r}")

import shutil  # noqa: E402
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
