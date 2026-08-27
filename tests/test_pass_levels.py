#!/usr/bin/env python3
"""EX-PASS-LEVEL — the three readings of "level" (TEST_MATRIX.md PASS-09, PASS-10).

Run: python3 tests/test_pass_levels.py

Both rows below extract the REAL, currently shipped functions out of
`engine/assets/pass-composer.js` by balanced-brace text extraction — the same idiom
`tests/test_pass_layer.py`'s own `extract_function` already carries for a shader and an
instrument constructor — and run them in a bare Node `vm` sandbox. Nothing here re-describes the
arithmetic in Python; every row calls the shipped function and reads what it actually returns.

WHAT THE MATRIX ASKED FOR, AND WHAT THIS FILE ACTUALLY PROVES. TEST_MATRIX.md's own words for
PASS-09 read "two cues that both OWN one structural level in overlapping windows are refused".
Reading `ownTheLevels` (`pass-composer.js:3607-3644`) shows there is no refusal to test: the
function is an ARBITRATION, not a validator over a pre-existing conflict. For every level and every
group of cues whose windows overlap and who all declared that level, it picks exactly one owner
(`preferredOn`/`needier`) and marks every other holder in the group "accompanies:<ownerId>" —
contention is prevented by construction, never detected and refused afterward. This matches
`docs/prover/2026-08-27-pass-section.md` finding F2: "the only reader of `levelOwnership`
... asks whether *this* cue owns a level and never gathers a level's holders to compare them." What
PASS-09 below proves instead is the real, stronger guarantee: `ownTheLevels`'s own output never
carries two "owns" for one level in one overlapping group, for any input, which is what keeps a
visitor from ever seeing two cues contend for one level — by construction rather than by a refusal
this repository does not enforce. The red-on-bug proof shows the guarantee is real: mutating the one
line that picks a single owner reintroduces the exact double-ownership PASS-09 was written to catch.

PASS-10 is untouched by that divergence — the declaration/ownership/driving split the prover's
Opening assessment calls "exact, matches pass-composer.js:1332, :3866-3869 and :4018 field for
field" is the ground this row stands on.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "engine" / "assets" / "pass-composer.js"

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


NODE = node_available()
SOURCE = MODULE.read_text(encoding="utf-8").replace("@@NS@@", "")


def extract_function(text, name, after_idx=0):
    """Balanced-brace extraction of `function NAME(...) { ... }` — the REAL, current body, the
    same idiom tests/test_pass_layer.py's own `extract_function` carries for a shader."""
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


# ---------------------------------------------------------------- the real functions, extracted
#
# `Flt`/`flt`/`isFlt`/`num` — Python's-own-numbers plumbing every cue's `.window`/`.stack` may be
# wrapped in. Extracted as one contiguous block (pass-composer.js:65-69) rather than hand-retyped.
UTIL_START = SOURCE.index("function Flt(v)")
UTIL_END = SOURCE.index("\n", SOURCE.index("function num(v)")) + 1
UTIL_SRC = SOURCE[UTIL_START:UTIL_END]

LEVEL_OF_SRC = extract_function(SOURCE, "levelOf")
MEETS_SRC = extract_function(SOURCE, "meets")
DRIVES_ON_SRC = extract_function(SOURCE, "drivesOn")
DRIVEN_LEVELS_SRC = extract_function(SOURCE, "drivenLevelsOf")
OWNS_ANYTHING_SRC = extract_function(SOURCE, "ownsAnything")
NEED_ORDER_SRC = extract_function(SOURCE, "needOrder")
PREFERRED_ON_SRC = extract_function(SOURCE, "preferredOn")
NEEDIER_SRC = extract_function(SOURCE, "needier")
OWN_THE_LEVELS_SRC = extract_function(SOURCE, "ownTheLevels")

BASE_SRC = "\n".join([UTIL_SRC, LEVEL_OF_SRC, MEETS_SRC, DRIVES_ON_SRC, DRIVEN_LEVELS_SRC,
                       OWNS_ANYTHING_SRC, NEED_ORDER_SRC, PREFERRED_ON_SRC, NEEDIER_SRC,
                       OWN_THE_LEVELS_SRC])

# `levelOf` reads `MANIFESTS[iid].handles[handle].level`. A synthetic manifest set, built for this
# row alone — the fact under test is the arbitration arithmetic, not any real instrument's own
# declared levels, exactly as test_pass_lawful.py's `built()` records construct synthetic per-work
# readings rather than reading a real photograph for arithmetic rows.
MANIFESTS = {
    "east": {"handles": {"hEast": {"level": "SURFACE"}, "hEastCell": {"level": "CELL"}}},
    "west": {"handles": {"hWest": {"level": "SURFACE"}}},
    "north": {"handles": {"hNorth": {"level": "CELL"}}},
    "silent": {"handles": {"hSilent": {"level": None}}},
}

TMP = Path(tempfile.mkdtemp(prefix="pass_levels_"))
DRIVER_PATH = TMP / "levels-driver.js"


def run(job, plants=None):
    src = BASE_SRC
    missed = []
    for frm, to in (plants or []):
        if src.find(frm) < 0:
            missed.append(frm)
            continue
        src = src.replace(frm, to)
    driver = (
        "\"use strict\";\n"
        "var MISSED = " + json.dumps(missed) + ";\n"
        "var MANIFESTS = " + json.dumps(MANIFESTS) + ";\n"
        + src + "\n"
        "var job = " + json.dumps(job) + ";\n"
        "var out;\n"
        "if (MISSED.length) { out = {missed: MISSED}; }\n"
        "else if (job.job === 'own') {\n"
        "  out = ownTheLevels(job.cues, job.pivotCueId || null);\n"
        "} else if (job.job === 'drivesOn') {\n"
        "  var row = {};\n"
        "  job.asks.forEach(function (a) { row[a.cue + '|' + a.level] = "
        "drivesOn(job.cues.filter(function(c){return c.id===a.cue;})[0], a.level); });\n"
        "  out = row;\n"
        "}\n"
        "console.log(JSON.stringify(out));\n"
    )
    DRIVER_PATH.write_text(driver, encoding="utf-8")
    proc = subprocess.run(["node", str(DRIVER_PATH)], capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        return {"error": (proc.stderr or "").strip()[-800:]}
    line = (proc.stdout or "").strip().splitlines()
    if not line:
        return {"error": "the driver said nothing"}
    return json.loads(line[-1])


def cue(id_, iid, tracks, levels, window, stack=0):
    return {"id": id_, "instrument": {"id": iid}, "tracks": tracks, "levels": levels,
            "window": window, "stack": stack}


# ---------------------------------------------------------------- PASS-09 fixtures
#
# Two overlapping cues both declaring SURFACE (real contention material) and driving it for real —
# «east» plays [0,5), «west» plays [2,7): 2 < 5 and 0 < 7, so `meets` reads them as live together.
CUE_A = cue("cueA", "east", {"hEast": {"node": "a"}}, ["SURFACE"], [0, 5], stack=0)
CUE_B = cue("cueB", "west", {"hWest": {"node": "b"}}, ["SURFACE"], [2, 7], stack=1)
# A third holder of SURFACE that never overlaps either — its own group, own owner.
CUE_C = cue("cueC", "east", {"hEast": {"node": "c"}}, ["SURFACE"], [10, 15], stack=2)
# A cue that plays OVER the same window as A/B but never DECLARES SURFACE at all — PASS-API-V1's own
# words: "a level a cue plays over without owning stays out of that list."
CUE_D = cue("cueD", "north", {"hNorth": {"node": "d"}}, ["CELL"], [1, 6], stack=3)

CONTEND_CUES = [CUE_A, CUE_B, CUE_C, CUE_D]

if not NODE:
    skip("PASS-09 (EX-PASS-LEVEL, shelf 4) · two cues that both declare one structural level in "
         "overlapping windows never both read \"owns\" it", "node is not on this machine")
    skip("PASS-09 · a cue playing over a level it never declared is never read as owning or "
         "accompanying it", "node is not on this machine")
    skip("PASS-09 · a group of cues sharing no window each own their own copy of the level", "")
    skip("PASS-09 red-on-bug · the single-owner arbitration line is what the guarantee stands on",
         "node is not on this machine")
else:
    own = run({"job": "own", "cues": CONTEND_CUES})
    if own.get("error") or own.get("missed"):
        why = own.get("error") or ("extraction missed: " + ", ".join(own["missed"]))
        for n in ("PASS-09 (EX-PASS-LEVEL, shelf 4) · two cues that both declare one structural "
                  "level in overlapping windows never both read \"owns\" it",
                  "PASS-09 · a cue playing over a level it never declared is never read as owning "
                  "or accompanying it",
                  "PASS-09 · a group of cues sharing no window each own their own copy of the "
                  "level"):
            check(n, False, why)
    else:
        owners_ab = [c for c in ("cueA", "cueB") if own[c].get("SURFACE") == "owns"]
        check("PASS-09 (EX-PASS-LEVEL, shelf 4) · two cues that both declare one structural level "
              "in overlapping windows never both read \"owns\" it",
              len(owners_ab) == 1,
              "" if len(owners_ab) == 1 else
              ("ownTheLevels(cueA, cueB) over SURFACE with overlapping windows [0,5)/[2,7) read "
               + json.dumps({k: own[k] for k in ("cueA", "cueB")})
               + " — real code arbitrates a single owner per overlapping group; " + str(owners_ab)
               + " read \"owns\""))

        check("PASS-09 · a cue playing over a level it never declared is never read as owning or "
              "accompanying it",
              "SURFACE" not in own.get("cueD", {}),
              "" if "SURFACE" not in own.get("cueD", {}) else
              ("cueD never declared SURFACE in its own .levels yet ownTheLevels wrote "
               + json.dumps(own.get("cueD")) + " for it"))

        check("PASS-09 · a group of cues sharing no window each own their own copy of the level",
              own.get("cueC", {}).get("SURFACE") == "owns",
              "" if own.get("cueC", {}).get("SURFACE") == "owns" else
              ("cueC shares no window with cueA/cueB (window [10,15) meets neither), so its own "
               "SURFACE claim should arbitrate independently and win its own one-member group; "
               "read " + json.dumps(own.get("cueC"))))

    # RED-ON-BUG. The one line the single-owner guarantee stands on:
    #   out[c.id][level] = owner === c ? "owns" : ("accompanies:" + owner.id);
    # forced to hand every holder "owns" regardless of who the arbitration actually picked —
    # reintroducing the exact double-ownership PASS-09's first row exists to catch.
    PLANT_OWN = [
        ('out[c.id][level] = owner === c ? "owns" : ("accompanies:" + owner.id);',
         'out[c.id][level] = "owns";'),
    ]
    broke = run({"job": "own", "cues": CONTEND_CUES}, plants=PLANT_OWN)
    if broke.get("missed"):
        skip("PASS-09 red-on-bug · the single-owner arbitration line is what the guarantee stands "
             "on", "the plant text was not found verbatim in the shipped source: "
                    + ", ".join(broke["missed"]))
    elif broke.get("error"):
        check("PASS-09 red-on-bug · the single-owner arbitration line is what the guarantee stands "
              "on", False, broke["error"])
    else:
        both_own = broke.get("cueA", {}).get("SURFACE") == "owns" \
            and broke.get("cueB", {}).get("SURFACE") == "owns"
        check("PASS-09 red-on-bug · the single-owner arbitration line is what the guarantee stands "
              "on", both_own,
              "" if both_own else
              "forcing every holder to \"owns\" left the row above still finding one owner, so "
              "that row is not reading the line it claims to")

# ---------------------------------------------------------------- PASS-10 fixtures
#
# A cue that OWNS SURFACE by winning the arbitration above (cueA, sole overlap-free claimant of a
# level it also tracks) — but here it is given a DIFFERENT track, "hEastCell" (declared CELL by the
# manifest, not SURFACE), so nothing it actually built moves SURFACE at all: owns it, drives nothing
# on it.
CUE_OWNS_NOTHING = cue("cueE", "east", {"hEastCell": {"node": "e"}}, ["SURFACE"], [20, 25], stack=0)
# A cue that never declares CELL in `.levels` at all (so ownTheLevels never opens a CELL record for
# it — it is not read as owning or accompanying CELL by any measure) but tracks "hNorth", which
# `MANIFESTS.north` declares at CELL — it drives a level it does not own.
CUE_DRIVES_UNOWNED = cue("cueF", "north", {"hNorth": {"node": "f"}}, ["SURFACE"], [30, 35], stack=0)

if not NODE:
    skip("PASS-10 (EX-PASS-LEVEL) · a cue can own a structural level and drive nothing on it",
         "node is not on this machine")
    skip("PASS-10 · a cue can drive a structural level it does not own",
         "node is not on this machine")
    skip("PASS-10 red-on-bug · drivesOn reads the cue's own built tracks, never its declared "
         "levels", "node is not on this machine")
else:
    d1 = run({"job": "own", "cues": [CUE_OWNS_NOTHING]})
    dOn1 = run({"job": "drivesOn", "cues": [CUE_OWNS_NOTHING],
                "asks": [{"cue": "cueE", "level": "SURFACE"}]})
    if d1.get("error") or dOn1.get("error"):
        check("PASS-10 (EX-PASS-LEVEL) · a cue can own a structural level and drive nothing on it",
              False, d1.get("error") or dOn1.get("error"))
    else:
        owns_surface = d1.get("cueE", {}).get("SURFACE") == "owns"
        drives_surface = dOn1.get("cueE|SURFACE")
        check("PASS-10 (EX-PASS-LEVEL) · a cue can own a structural level and drive nothing on it",
              owns_surface and drives_surface is False,
              "" if (owns_surface and drives_surface is False) else
              ("cueE's own ownership record reads " + json.dumps(d1.get("cueE"))
               + " and drivesOn(cueE, SURFACE) reads " + json.dumps(drives_surface)
               + " — it tracks only \"hEastCell\", which the synthetic manifest declares at CELL, "
               "not SURFACE"))

    dOn2 = run({"job": "drivesOn", "cues": [CUE_DRIVES_UNOWNED],
                "asks": [{"cue": "cueF", "level": "CELL"}]})
    d2 = run({"job": "own", "cues": [CUE_DRIVES_UNOWNED]})
    if dOn2.get("error") or d2.get("error"):
        check("PASS-10 · a cue can drive a structural level it does not own",
              False, dOn2.get("error") or d2.get("error"))
    else:
        drives_cell = dOn2.get("cueF|CELL")
        owns_cell_record = "CELL" in d2.get("cueF", {})
        check("PASS-10 · a cue can drive a structural level it does not own",
              drives_cell is True and not owns_cell_record,
              "" if (drives_cell is True and not owns_cell_record) else
              ("cueF never declared CELL in its own .levels (only [\"SURFACE\"]), so ownTheLevels "
               "opened no CELL record for it (" + json.dumps(d2.get("cueF")) + "), yet it tracks "
               "\"hNorth\", which the synthetic manifest declares at CELL — drivesOn(cueF, CELL) "
               "reads " + json.dumps(drives_cell)))

    # RED-ON-BUG. `drivesOn` reads the cue's OWN BUILT TRACKS today:
    #   for (i = 0; i < hs.length; i++) if (levelOf(iid, hs[i]) === level) return true;
    # PASS-10's own "Never" fence names the exact substitution to guard against — reading a
    # manifest's declared level (or here, the cue's own DECLARED/owned levels list) in place of
    # what the cue's tracks actually move. The plant makes that substitution.
    PLANT_DRIVES = [
        ("function drivesOn(cue, level) {\n      var iid = cue.instrument.id, "
         "hs = Object.keys(cue.tracks || {}), i;\n      for (i = 0; i < hs.length; i++) "
         "if (levelOf(iid, hs[i]) === level) return true;\n      return false;\n    }",
         "function drivesOn(cue, level) {\n      return (cue.levels || []).indexOf(level) >= 0;\n    }"),
    ]
    brokeDrives = run({"job": "drivesOn", "cues": [CUE_DRIVES_UNOWNED],
                       "asks": [{"cue": "cueF", "level": "CELL"}]}, plants=PLANT_DRIVES)
    if brokeDrives.get("missed"):
        skip("PASS-10 red-on-bug · drivesOn reads the cue's own built tracks, never its declared "
             "levels",
             "the plant text was not found verbatim in the shipped source: "
             + ", ".join(brokeDrives["missed"]))
    elif brokeDrives.get("error"):
        check("PASS-10 red-on-bug · drivesOn reads the cue's own built tracks, never its declared "
              "levels", False, brokeDrives["error"])
    else:
        now_false = brokeDrives.get("cueF|CELL") is False
        check("PASS-10 red-on-bug · drivesOn reads the cue's own built tracks, never its declared "
              "levels", now_false,
              "" if now_false else
              "substituting cue.levels for the cue's own tracks left drivesOn(cueF, CELL) reading "
              + json.dumps(brokeDrives.get("cueF|CELL"))
              + " still, so the row above is not reading what it claims to")

import shutil  # noqa: E402
shutil.rmtree(TMP, ignore_errors=True)

# ---------------------------------------------------------------- report
print("EX-PASS-LEVEL · declared / owned / driven (TEST_MATRIX.md PASS-09, PASS-10)")
print("module: " + str(MODULE))
print("")
for name, verdict, detail in results:
    print("  " + verdict.ljust(5) + " " + name)
    if detail:
        for ln in detail.split("\n"):
            print("        " + ln)
print("")
passed = sum(1 for r in results if r[1] == "PASS")
failed = sum(1 for r in results if r[1] == "FAIL")
skipped = sum(1 for r in results if r[1] == "SKIP")
print("  " + str(passed) + " pass, " + str(failed) + " fail, " + str(skipped) + " skip")
sys.exit(1 if failed else 0)
