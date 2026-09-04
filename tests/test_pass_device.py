#!/usr/bin/env python3
"""Plan row S-110 — the device is read once at load, and the reading sets the crossing's ceiling.

Run: python3 tests/test_pass_device.py

His word of 04.09.2026 16:03: read the processor while the page loads and set the complexity of a
crossing from what was read. Row S-14 had already landed the other half — all twenty-seven
instruments declare their real cost per variant — and nothing anywhere read the machine those costs
would be spent on, so `bundleResourcesLegal` held every candidate bundle against the fleet's own
richest published budget for a phone and for a desk alike.

WHAT THIS FILE READS, AND WHAT IT REFUSES TO READ. The row's own criterion is the CAST: a fed weak
reading gives a smaller set of instruments than a fed strong one, on the same pair, and a planted
ceiling that ignores the reading levels the two sets. So nothing here runs a clock. There is no
frame-rate run, no timing run and no bench: every row below either states a reading and reads the
published budget row it lands on, or states a ceiling and reads which instruments were cast under
it. The functions run are the shipped ones — `ceilingFor`, `readDevice`, `deviceCeiling` and
`variantOf` lifted out of `engine/assets/pass-layer.js` by text and run in a fresh `vm` context, the
road `tests/test_pass_lawful.py` already walks, and the real `passageFor` off `make(consts)` for the
cast, the road `tests/test_pass_bundle.py` already walks.

NO PAIR IS HAND-PICKED. The cast rows sweep the fixture fleet's own ordered pairs in the fixture's
own order and report the first pair on which the two readings part, alongside the sweep's own
totals: under the weak reading no pair is ever cast MORE instruments than under the strong one, and
no pair is ever cast none.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYER = ROOT / "engine" / "assets" / "pass-layer.js"
COMPOSER = ROOT / "engine" / "assets" / "pass-composer.js"
CLIENT = ROOT / "engine" / "client" / "01a-pass.js"
FIXTURE = ROOT / "tests" / "fixture_pass_composed.json"
FIXTURE_WORKS = ROOT / "tests" / "fixture_pass_works.json"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def fail(name, detail):
    results.append((name, "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


LAYER_SRC = LAYER.read_text(encoding="utf-8")
CLIENT_SRC = CLIENT.read_text(encoding="utf-8")
COMPOSER_SRC = COMPOSER.read_text(encoding="utf-8").replace("@@NS@@", "")

# ------------------------------------------------------------------ the shipped slabs, by text
# Each is the whole of one shipped declaration, lifted verbatim. A slab that stops matching is a
# defect in this file's reach and is reported as one, never quietly skipped: a row that cannot find
# the code it judges is a row proving nothing.
SLABS = {
    "RES_KEYS": r"  var RES_KEYS = \[.*?\];",
    "VARIANTS_BUDGET": r"  var VARIANTS = \[.*?\];\n  var BUDGET = \{.*?\n  \};",
    "readDevice": r"  var BYTES_PER_TEXEL = \d+;\n  function readDevice\(\) \{.*?\n  \}",
    "ceilingFor": r"  function ceilingFor\(reading\) \{.*?\n  \}",
    "deviceCeiling": r"  var deviceRead = null;\n  function deviceCeiling\(\) \{.*?\n  \}",
    "variantOf": r"  function variantOf\(cmd\) \{.*?\n  \}",
}
lifted, missing = {}, []
for name, pattern in SLABS.items():
    m = re.search(pattern, LAYER_SRC, re.S)
    if m:
        lifted[name] = m.group(0)
    else:
        missing.append(name)


def node_available():
    return shutil.which("node") is not None


NODE = node_available()
TMP = Path(tempfile.mkdtemp(prefix="pass_device_"))

# ------------------------------------------------------------------ run 1: the reading and the rung
# A FAKE DEVICE, COUNTED. `readDevice` asks a canvas for a WebGL 2 context and reads three published
# parameters off it. Here the canvas and the context are stated, so a reading can be handed in that
# no machine in this room has, and every ask is counted — which is what proves the reading is taken
# ONCE and held, rather than re-taken per crossing.
LAYER_DRIVER = r"""
"use strict";
%(slabs)s

const asked = { contexts: 0, params: 0 };
function fakeDevice(maxSide, slots, combined) {
  const P = { MAX_TEXTURE_SIZE: 1, MAX_TEXTURE_IMAGE_UNITS: 2, MAX_COMBINED_TEXTURE_IMAGE_UNITS: 3 };
  const values = { 1: maxSide, 2: slots, 3: combined };
  return {
    MAX_TEXTURE_SIZE: P.MAX_TEXTURE_SIZE,
    MAX_TEXTURE_IMAGE_UNITS: P.MAX_TEXTURE_IMAGE_UNITS,
    MAX_COMBINED_TEXTURE_IMAGE_UNITS: P.MAX_COMBINED_TEXTURE_IMAGE_UNITS,
    getParameter: (p) => { asked.params += 1; return values[p]; },
    getExtension: () => null,
  };
}
let bench = null;
global.document = { createElement: () => ({ getContext: () => { asked.contexts += 1; return bench; } }) };

// STATED READINGS, never a machine's. Each names what a device published about itself in the very
// fields the budget rows are written in.
const READINGS = %(readings)s;
const ranked = {};
for (const key of Object.keys(READINGS)) ranked[key] = ceilingFor(READINGS[key]);

// ONCE PER VISIT. The bench is asked for, twice, and the count of contexts it handed out is read.
bench = fakeDevice(2048, 8, 8);
const first = deviceCeiling();
const afterFirst = { contexts: asked.contexts, params: asked.params };
bench = fakeDevice(16384, 16, 32);   // a different machine entirely, offered after the reading
const second = deviceCeiling();
const afterSecond = { contexts: asked.contexts, params: asked.params };

// THE RUNG. `variantOf` is the shipped function; `stepIx` is the frame-pace ladder it already read
// before this row, held at nothing here so the only thing moving is the ceiling.
let stepIx = 0;
let ceilingNow = "rich";
function deviceCeilingStub() { return { variant: ceilingNow }; }
const variantOfSrc = %(variantOfSrc)s;
const rungOf = new Function(
  "VARIANTS", "stepIx", "deviceCeiling",
  variantOfSrc + "\nreturn variantOf;");
function rung(asked, source, ceiling) {
  return rungOf(VARIANTS, stepIx, () => ({ variant: ceiling }))(
    { params: { qualityTier: { base: asked, source: source } } });
}

console.log(JSON.stringify({
  ranked: ranked,
  variants: VARIANTS,
  budget: BUDGET,
  onceFirst: first, onceSecond: second, afterFirst: afterFirst, afterSecond: afterSecond,
  rungNamedRichOnLean: rung("rich", "session", "lean"),
  rungNamedRichOnRich: rung("rich", "session", "rich"),
  rungDefaultOnStandard: rung("standard", "default", "standard"),
  rungDefaultOnRich: rung("standard", "default", "rich"),
}));
"""

# ------------------------------------------------------------------ run 2: the cast, under two readings
CAST_DRIVER = r"""
"use strict";
const vm = require("vm");
const source = %(source)s;
const consts = %(consts)s;
const works = %(works)s;
const rows = %(rows)s;
const plants = %(plants)s;

function load(src) {
  let joined = null;
  const sandbox = { window: { __PassComposer: (m) => { joined = m; } }, console: console };
  vm.createContext(sandbox);
  vm.runInContext(src, sandbox, { filename: "pass-composer.js" });
  return joined.make(consts);
}

let planted = source;
const missed = [];
for (const [from, to] of plants) {
  if (planted.indexOf(from) < 0) { missed.push(from); continue; }
  planted = planted.split(from).join(to);
}
if (missed.length) { console.log(JSON.stringify({ missed: missed })); process.exit(0); }

// A COMPOSER PER READING. Each holds the ceiling its own requests carried, so nothing one reading
// decided can ride into the other.
function castsUnder(src, ceiling, limit) {
  const composer = load(src);
  const ids = Object.keys(works);
  // The station a live route step always states in one breath (`passRouteStation`), two of its own
  // pairings, so a bundle that only ever wins at one station is still reached.
  const ROLE_FN = [["culmination", "dominant"], ["entrance", "subdominant"]];
  const out = [];
  for (let i = 0; i < ids.length && out.length < limit; i++) {
    for (let j = 0; j < ids.length && out.length < limit; j++) {
      if (i === j) continue;
      for (const [role, fn] of ROLE_FN) {
        const req = { workRecordA: works[ids[i]], workRecordB: works[ids[j]],
                      direction: "a-to-b", seed: 3, routeRole: role, routeFunction: fn,
                      cameraState: null, walkMemory: [], walkGenres: [], walkMiracles: [],
                      framePace: null, deviceCeiling: ceiling };
        let made = null;
        try { made = composer.passageFor(req); } catch (e) { made = null; }
        const cast = (made && !made.declined && made.plan)
          ? (made.plan.cues || []).map((c) => c.instrument.id) : null;
        out.push({ from: ids[i], to: ids[j], role: role, fn: fn, cast: cast });
      }
    }
  }
  return out;
}

function compare(src) {
  const weak = castsUnder(src, rows.weak, %(limit)d);
  const strong = castsUnder(src, rows.strong, %(limit)d);
  let smaller = null, everBigger = null, everEmpty = null, same = 0;
  for (let k = 0; k < weak.length; k++) {
    const w = weak[k].cast, s = strong[k].cast;
    if (!w || !s) continue;
    if (w.length < s.length && !smaller) smaller = { at: weak[k], weak: w, strong: s };
    if (w.length > s.length && !everBigger) everBigger = { at: weak[k], weak: w, strong: s };
    if (w.length < 1 && !everEmpty) everEmpty = { at: weak[k] };
    if (w.length === s.length) same += 1;
  }
  return { pairs: weak.length, smaller: smaller, everBigger: everBigger, everEmpty: everEmpty,
           same: same };
}

console.log(JSON.stringify({ shipped: compare(source), planted: compare(planted) }));
"""

# THE PLANT: the ceiling stops reading what was fed and goes back to the fleet's own richest row for
# every device, which is exactly what stood before this row. Two lines, named as they ship.
PLANT = [
    ['var ceiling = (deviceCeiling && deviceCeiling.budget) || RESOURCE_CEILING;\n'
     '      var variant = (deviceCeiling && deviceCeiling.variant) || "rich";',
     'var ceiling = RESOURCE_CEILING;\n'
     '      var variant = "rich";'],
]

# The stated readings. Each number is one a device publishes about itself: two texture-unit counts
# straight off the graphics processor, and the bytes of the largest single target it declares it
# will accept — its own `MAX_TEXTURE_SIZE` squared at the four bytes a texel of the one format every
# target on this stage is made in.
READINGS = {
    "a device declaring a 2048 target and eight texture units":
        {"textureSlots": 8, "textures": 8, "bytesEstimate": 4 * 2048 * 2048},
    "a device declaring a 4096 target and sixteen texture units":
        {"textureSlots": 16, "textures": 32, "bytesEstimate": 4 * 4096 * 4096},
    "a device declaring an 8192 target and sixteen texture units":
        {"textureSlots": 16, "textures": 32, "bytesEstimate": 4 * 8192 * 8192},
    "a device that declares nothing at all": {},
}


def run_node(text, name, timeout):
    path = TMP / name
    path.write_text(text, encoding="utf-8")
    proc = subprocess.run(["node", str(path)], capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-1500:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


# ------------------------------------------------------------------ the source rows, run first
check("the walk asks for the reading the moment the drawing layer registers, which is while the "
      "page is still loading",
      "function passDeviceCeiling()" in CLIENT_SRC
      and re.search(r"passState = passLayer \? \"registered\" : \"absent\";\n(?:.*\n)*?"
                    r"\s*passDeviceCeiling\(\);", CLIENT_SRC) is not None,
      "engine/client/01a-pass.js")

check("every compose request carries the reading, beside the frame pace it already carried",
      "deviceCeiling: passDeviceCeiling()," in CLIENT_SRC, "engine/client/01a-pass.js")

check("the composer takes the reading off the request and holds it for the visit",
      "if (req.deviceCeiling && typeof req.deviceCeiling === \"object\"" in COMPOSER_SRC
      and "var deviceCeiling = null;" in COMPOSER_SRC, "engine/assets/pass-composer.js")

check("the cast is held against the row this device published, at the rung it will play",
      'var ceiling = (deviceCeiling && deviceCeiling.budget) || RESOURCE_CEILING;' in COMPOSER_SRC
      and 'var variant = (deviceCeiling && deviceCeiling.variant) || "rich";' in COMPOSER_SRC
      and "var r = resourcesBlock(iid, variant);" in COMPOSER_SRC,
      "engine/assets/pass-composer.js, bundleResourcesLegal")

# NOTHING IN THE READING IS TIMED. The row bans a clock from the acceptance; this holds the reading
# itself to the same bar, because a reading that timed anything would be a benchmark run on every
# visitor's machine at load.
timed = [w for w in ("performance.now", "Date.now", "setTimeout", "requestAnimationFrame", "new Date")
         if any(w in lifted.get(k, "") for k in ("readDevice", "ceilingFor", "deviceCeiling"))]
check("the reading times nothing — it asks the device and reads what it published",
      not missing and not timed,
      ("these slabs are no longer in pass-layer.js: " + ", ".join(missing)) if missing
      else (("the reading names " + ", ".join(timed)) if timed else ""))

if missing:
    fail("the shipped reading, the ceiling and the rung are all reachable from this file",
         "pass-layer.js no longer carries: " + ", ".join(missing))
elif not NODE:
    for _n in ("a weaker published reading lands on a leaner published row than a stronger one",
               "a device that declares nothing keeps the fleet's own richest published row",
               "the reading is taken once and held for the visit",
               "the rung a device plays at is held to the ceiling it published",
               "the same pair is cast fewer instruments under a weak reading than under a strong one",
               "no pair is ever cast more instruments under the weak reading than under the strong",
               "no device is left with nothing — every pair still carries a cast under the weakest "
               "reading",
               "red-on-bug · a ceiling that ignores the reading levels the two casts"):
        skip(_n, "node is not on this machine")
else:
    check("the shipped reading, the ceiling and the rung are all reachable from this file", True)
    layer_out = run_node(LAYER_DRIVER % {
        "slabs": "\n".join(lifted[k] for k in
                           ("RES_KEYS", "VARIANTS_BUDGET", "readDevice", "ceilingFor",
                            "deviceCeiling")),
        "readings": json.dumps(READINGS),
        "variantOfSrc": json.dumps(lifted["variantOf"]),
    }, "layer-driver.js", 60)

    if layer_out.get("error"):
        for _n in ("a weaker published reading lands on a leaner published row than a stronger one",
                   "a device that declares nothing keeps the fleet's own richest published row",
                   "the reading is taken once and held for the visit",
                   "the rung a device plays at is held to the ceiling it published"):
            fail(_n, layer_out["error"])
    else:
        ranked = layer_out["ranked"]
        order = layer_out["variants"]
        names = list(READINGS.keys())
        rungs = [order.index(ranked[n]) for n in names[:3]]
        check("a weaker published reading lands on a leaner published row than a stronger one",
              rungs[0] < rungs[1] < rungs[2],
              "; ".join("%s → «%s»" % (n, ranked[n]) for n in names[:3]))
        check("a device that declares nothing keeps the fleet's own richest published row",
              ranked[names[3]] == order[-1],
              "a device declaring nothing read «%s», and the richest published row is «%s»"
              % (ranked[names[3]], order[-1]))

        one_context = (layer_out["afterFirst"]["contexts"] == 1
                       and layer_out["afterSecond"]["contexts"] == 1
                       and layer_out["afterFirst"]["params"] == layer_out["afterSecond"]["params"]
                       and layer_out["onceFirst"]["variant"] == layer_out["onceSecond"]["variant"])
        check("the reading is taken once and held for the visit",
              one_context,
              "asked twice, with a different machine offered the second time: contexts %s then %s, "
              "parameters %s then %s, answering «%s» then «%s»"
              % (layer_out["afterFirst"]["contexts"], layer_out["afterSecond"]["contexts"],
                 layer_out["afterFirst"]["params"], layer_out["afterSecond"]["params"],
                 layer_out["onceFirst"]["variant"], layer_out["onceSecond"]["variant"]))

        check("the rung a device plays at is held to the ceiling it published",
              layer_out["rungNamedRichOnLean"] == "lean"
              and layer_out["rungNamedRichOnRich"] == "rich"
              and layer_out["rungDefaultOnStandard"] == "standard"
              and layer_out["rungDefaultOnRich"] == "standard",
              "asked «rich» by name on a «lean» device → «%s»; the same ask on a «rich» device → "
              "«%s»; nobody's word on a «standard» device → «%s»; nobody's word on a «rich» device "
              "→ «%s»"
              % (layer_out["rungNamedRichOnLean"], layer_out["rungNamedRichOnRich"],
                 layer_out["rungDefaultOnStandard"], layer_out["rungDefaultOnRich"]))

    cast_names = ("the same pair is cast fewer instruments under a weak reading than under a "
                  "strong one",
                  "no pair is ever cast more instruments under the weak reading than under the "
                  "strong",
                  "no device is left with nothing — every pair still carries a cast under the "
                  "weakest reading",
                  "red-on-bug · a ceiling that ignores the reading levels the two casts")
    if not FIXTURE_WORKS.exists() or not FIXTURE.exists():
        for _n in cast_names:
            skip(_n, "the composed fixture or the works fixture is not on this machine")
    elif layer_out.get("error"):
        for _n in cast_names:
            fail(_n, "the published budget rows could not be read out of pass-layer.js")
    else:
        budget, order = layer_out["budget"], layer_out["variants"]
        cast_out = run_node(CAST_DRIVER % {
            "source": json.dumps(COMPOSER_SRC),
            "consts": json.dumps(json.loads(FIXTURE.read_text(encoding="utf-8"))["consts"]),
            "works": json.dumps(json.loads(FIXTURE_WORKS.read_text(encoding="utf-8"))["works"]),
            "rows": json.dumps({"weak": {"variant": order[0], "budget": budget[order[0]]},
                                "strong": {"variant": order[-1], "budget": budget[order[-1]]}}),
            "plants": json.dumps(PLANT),
            "limit": 60,
        }, "cast-driver.js", 300)

        if cast_out.get("missed"):
            for _n in cast_names:
                fail(_n, "the lines this plant names are not in the shipped source: "
                         + ", ".join(cast_out["missed"]))
        elif cast_out.get("error"):
            for _n in cast_names:
                fail(_n, cast_out["error"])
        else:
            shipped, plantedrun = cast_out["shipped"], cast_out["planted"]
            small = shipped["smaller"]
            check(cast_names[0], bool(small),
                  ("%s→%s at a %s: «%s» read %s, «%s» read %s (over %d station/pair readings)"
                   % (small["at"]["from"], small["at"]["to"], small["at"]["role"], order[0],
                      json.dumps(small["weak"]), order[-1], json.dumps(small["strong"]),
                      shipped["pairs"])) if small else
                  "over %d station/pair readings the two ceilings never once cast differently"
                  % shipped["pairs"])
            check(cast_names[1], shipped["everBigger"] is None,
                  "" if shipped["everBigger"] is None else
                  "%s→%s: «%s» cast %s while «%s» cast %s"
                  % (shipped["everBigger"]["at"]["from"], shipped["everBigger"]["at"]["to"],
                     order[0], json.dumps(shipped["everBigger"]["weak"]),
                     order[-1], json.dumps(shipped["everBigger"]["strong"])))
            check(cast_names[2], shipped["everEmpty"] is None,
                  "" if shipped["everEmpty"] is None else
                  "%s→%s was cast nothing under «%s»"
                  % (shipped["everEmpty"]["at"]["from"], shipped["everEmpty"]["at"]["to"], order[0]))
            check(cast_names[3], plantedrun["smaller"] is None,
                  "with the ceiling planted back to the fleet's own richest row, the two readings "
                  "still parted at %s→%s — the plant is not what the rule holds up"
                  % (plantedrun["smaller"]["at"]["from"], plantedrun["smaller"]["at"]["to"])
                  if plantedrun["smaller"] else
                  "planted, the two readings agree on all %d station/pair readings"
                  % plantedrun["pairs"])

for name, verdict, detail in results:
    print(verdict, name, ("— " + detail) if detail else "")
failed = sum(1 for _, v, _ in results if v == "FAIL")
skipped = sum(1 for _, v, _ in results if v == "SKIP")
print("\n%d passed / %d failed / %d skipped"
      % (len(results) - failed - skipped, failed, skipped))
shutil.rmtree(TMP, ignore_errors=True)
sys.exit(1 if failed else 0)
