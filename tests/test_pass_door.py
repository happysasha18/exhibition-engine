#!/usr/bin/env python3
"""EX-PASS-DOOR — a score naming a door its instrument never published (TEST_MATRIX.md PASS-14).

Run: python3 tests/test_pass_door.py

WHAT THIS ROW IS ABOUT, AND WHAT IT IS NOT. PASS-14's own words ask that a pass naming a door the
instrument's manifest leaves blank be REFUSED before it plays. That refusal has no enforcer in this
repository and this file does not pretend otherwise: `pass-layer.js`'s `manifestWhyNo` judges a
manifest's own shape at registration and never reads a score's `doors`, `scoreWhyNo` names five
refusals and none of them is this one, and the gate that does carry the row stands in the tlvphotos
tree and reads that tree's own builder's plans (`SPEC.md`, `INV-109`). So a score naming an
undeclared door reaches the host today, and the question this file answers is the one that follows
from it: what does the host DO when one arrives?

WHAT IT DID, AND WHAT THE FIX IS. `landingDoorOf` (`engine/assets/pass-layer.js`) is the host's
reckoning of where an interrupted crossing lands: it reads the cue's two doors, takes the handle
they name, and pins that handle to the door's own value inside the manifest's published bounds. It
read `v.inst.manifest.handles[k].min` with no guard on `k` being published, so the blank door cost a
TypeError inside the interruption cadence — the one moment the visitor is already leaving — rather
than the plain landing the cadence already has for a cue that names no usable door. The prover's own
verification pass named it as an observation for a bug row
(`docs/prover/2026-08-27-pass-section-verify.md`, under "Verified clean"); this file is that row.

The guard is the one `doorHandles` beside it has always carried: ask whether the manifest publishes
the handle, and where it does not, answer the way the function already answers a cue whose doors
cannot be used — with no landing door at all, which `cadenceStart` handles by holding every handle
where it stands. What the fix adds beyond `doorHandles`' silence is a named row on the diagnostic
surface, so the score that did it can be found and mended.

HOW IT IS TESTED. The REAL, currently-shipped `landingDoorOf` and the `clampNum` it calls are
extracted out of `engine/assets/pass-layer.js` by balanced-brace text extraction — the same idiom
`tests/test_pass_levels.py` and `tests/test_pass_lawful.py` already carry for the composer's own
functions — and run in a bare Node `vm` sandbox. Two of the function's neighbours are stubbed
rather than extracted, and named here so nothing reads as more than it is: `handlesOf`, which walks
every handle's own track through the evaluator (the row judges nothing it returns, only that the
door handle is pinned on top of it), and `logEvt`, which is the host's diagnostic log and is
captured here so the refusal's own words can be read back.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LAYER = ROOT / "engine" / "assets" / "pass-layer.js"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def node_available():
    try:
        return subprocess.run(["node", "--version"], capture_output=True).returncode == 0
    except Exception:
        return False


def extract_function(text, name, after_idx=0):
    marker = "function %s(" % name
    idx = text.index(marker, after_idx)
    brace = text.index("{", idx)
    depth, i = 0, brace
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[idx:i + 1]
        i += 1
    raise ValueError("unbalanced braces for function %s" % name)


NODE = node_available()
RAW = LAYER.read_text(encoding="utf-8").replace("@@NS@@", "")
CLAMP_SRC = extract_function(RAW, "clampNum")
DOOR_SRC = extract_function(RAW, "landingDoorOf")

TMP = Path(tempfile.mkdtemp(prefix="pass_door_"))
DRIVER = TMP / "door-driver.js"

# The stubs, and nothing else. `handlesOf` answers the way the real one does for a cue that drives
# no track of its own — every published handle at its declared default — and `logEvt` keeps the
# rows it is handed so the refusal's own words can be read back.
DRIVER_HEAD = """"use strict";
const job = JSON.parse(process.env.JOB || "{}");
const log = [];
function logEvt(name, gen, why) { log.push({name: name, gen: gen, why: why == null ? null : why}); }
function handlesOf(rec, v, progress, seconds, dt) {
  const m = v.inst.manifest, out = {};
  Object.keys(m.handles).forEach(function (h) { out[h] = m.handles[h]["def"]; });
  v.lastHandles = out;
  return out;
}
"""

DRIVER_TAIL = """
// A MANIFEST THAT PUBLISHES ONE HANDLE, and a score that names its doors on another. Nothing in
// this tree refuses such a score, so this is the record the host is actually handed.
const manifest = {handles: {reveal: {min: 0, max: 1, "def": 0}}};
const cue = {id: "pivot", window: [0, 2],
             doors: {"in": {handle: job.handle, value: 0}, out: {handle: job.handle, value: 1}}};
const rec = {duration: 2000, cmd: {gen: 4},
             primary: {cue: cue, inst: {name: "weave", manifest: manifest}, said: {}}};
const live = {}; live[job.handle] = 0.25;
let threw = null, door = null;
try { door = landingDoorOf(rec, live); }
catch (e) { threw = {name: e.name, why: String(e.message)}; }
console.log(JSON.stringify({threw: threw, door: door, log: log}));
"""


def run(handle, plants=()):
    src = DOOR_SRC
    missed = []
    for frm, to in plants:
        if frm not in src:
            missed.append(frm)
            continue
        src = src.replace(frm, to)
    DRIVER.write_text(DRIVER_HEAD + CLAMP_SRC + "\n" + src + "\n" + DRIVER_TAIL, encoding="utf-8")
    if missed:
        return {"missed": missed}
    proc = subprocess.run(["node", str(DRIVER)], capture_output=True, text=True,
                          env=dict(os.environ, JOB=json.dumps({"handle": handle})),
                          timeout=60)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-600:]}
    lines = (proc.stdout or "").strip().splitlines()
    if not lines:
        return {"error": "the driver said nothing"}
    return json.loads(lines[-1])


R_LANDS = "PASS-14 · a cue naming its doors on a published handle still gets its landing door"
R_NULL = ("PASS-14 (EX-PASS-DOOR) · a cue naming its doors on a handle the instrument never "
          "published gets no landing door, and no TypeError")
R_SAYS = ("PASS-14 · the refusal names the cue, the handle and the instrument on the diagnostic "
          "surface")
R_RED = "PASS-14 red-on-bug · the guard is what stands between that score and the TypeError"

if not NODE:
    for r in (R_LANDS, R_NULL, R_SAYS, R_RED):
        skip(r, "node is not on this machine")
else:
    # The working path first: the guard must not have taken the door away from a lawful score.
    ok = run("reveal")
    if ok.get("error"):
        check(R_LANDS, False, ok["error"])
    else:
        door = ok.get("door")
        lands = (not ok.get("threw") and door is not None and door.get("handle") == "reveal"
                 and door.get("handles", {}).get("reveal") == 1)
        check(R_LANDS, lands,
              "" if lands else "landingDoorOf on a published door handle read "
              + json.dumps({"threw": ok.get("threw"), "door": door}))

    blank = run("uWorld")
    if blank.get("error"):
        check(R_NULL, False, blank["error"])
        check(R_SAYS, False, blank["error"])
    else:
        clean = (blank.get("threw") is None and blank.get("door") is None)
        check(R_NULL, clean,
              "" if clean else
              ("a cue naming its doors on «uWorld», which the manifest does not publish, read "
               + json.dumps({"threw": blank.get("threw"), "door": blank.get("door")})))
        rows = [r for r in blank.get("log", []) if r.get("name") == "cadence-door-unpublished"]
        why = rows[0]["why"] if rows else ""
        said = bool(rows) and all(w in why for w in ("pivot", "uWorld", "weave"))
        check(R_SAYS, said,
              "" if said else
              ("the diagnostic surface carried " + json.dumps(blank.get("log", []))
               + ", which does not name the cue, the handle and the instrument together"))

    # RED ON BUG. Taking the guard back out must put the rows above into the red with the very
    # TypeError they were written against — a reader of `undefined.min` inside the cadence.
    PLANT = [("    if (!(v.inst.manifest.handles || {})[k]) {", "    if (false) {")]
    bug = run("uWorld", PLANT)
    if bug.get("missed"):
        skip(R_RED, "pass-layer.js no longer carries the guard this plant names, so there is "
                    "nothing to remove")
    elif bug.get("error"):
        check(R_RED, False, bug["error"])
    else:
        t = bug.get("threw") or {}
        red = t.get("name") == "TypeError" and "min" in (t.get("why") or "")
        check(R_RED, red,
              "" if red else
              ("removing the guard left the same score answering "
               + json.dumps({"threw": bug.get("threw"), "door": bug.get("door")})
               + ", so the rows above are not what the guard holds up"))

print("EX-PASS-DOOR · the blank door at the interruption cadence")
print("module: " + str(LAYER))
print("")
worst = 0
for name, verdict, detail in results:
    print("  " + verdict.ljust(5) + " " + name)
    if detail:
        for ln in detail.split("\n"):
            print("        " + ln)
    if verdict == "FAIL":
        worst = 1
print("")
print("  " + str(sum(1 for r in results if r[1] == "PASS")) + " pass, "
      + str(sum(1 for r in results if r[1] == "FAIL")) + " fail, "
      + str(sum(1 for r in results if r[1] == "SKIP")) + " skip")
sys.exit(worst)
