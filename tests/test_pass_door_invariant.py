#!/usr/bin/env python3
"""PASS-DOOR-INVARIANT — one fleet-wide, by-construction proof that a crop cancels at a real door.
Run: python3 tests/test_pass_door_invariant.py

ROOT. `docs/V2-CONVERGENCE-PLAN-2026-08-31.md`'s Phase 2, cause B: box-fold and hero baked their own
crop into geometry (box-fold) or a shader uniform multiplied against the already-seated fit (hero),
bypassing the one channel the host's own `seated` (pass-layer.js's `drawPose`) uses to cancel a
crop to identity as a real door is neared — the channel every other cropped instrument in the fleet
already leans on: `fit(iw, ih, w, h)` divides the crop IN, and `seated` divides it back OUT, purely
as a function of how close the passage stands to a real hang, never of the instrument's own dial.
Phase 2's repair routes both instruments through that same channel (`pass-inst-boxfold.js`,
`pass-inst-hero.js`).

WHAT THIS FILE PROVES, AND WHY IT IS ONE LAW RATHER THAN TWO INSTRUMENTS' OWN ROWS. The repair is a
mechanism, not a patch to two files — `rankUnread`'s own standing rule, quoted throughout this
sprint's plan, is that the rule is what gets repaired, not the instance. So this file states the rule
itself, as one arithmetic identity every instrument's own `fit` either answers to or is named here as
not answering to, rather than leaving the proof to two instruments' own suites and letting the next
instrument that bypasses the channel go unnoticed the way box-fold and hero did.

THE LAW, IN ARITHMETIC. For every instrument, `fit(iw, ih, w, h)` must equal the plain cover-fit of
the source into the frame — `cover(aspect)`, the same two-branch formula `pass-inst-adrift.js` and
every other correctly-behaving cropped instrument already carries — divided by that instrument's own
declared crop, `c`, read off `manifest.framings["0"].coverCrop`. This is exactly what lets the host's
`seated` cancel the crop to identity by dividing a SINGLE number (`c`) back out as a real door is
neared, and it is checked here on six aspect-ratio cases (wide, tall, square, an exact match, a large
source and the frame turned on its side) rather than one, since a fit that only agrees with the law
at one aspect is not proof of the law.

NO GL, NO BROWSER, NO PICTURE. The claim is pure arithmetic on four numbers a pure function returns,
so it is checked by loading each instrument file for real under `node` — the same throwaway-sandbox
technique `tests/test_pass_feel.py` already uses for `feel()` — and calling its own published `fit`
directly, never a description of it and never a re-typed copy of its formula.

ONE PRINCIPLED EXEMPTION, NOT A NAME TYPED HERE BY HAND: an instrument that declares
`coverage.writes === true` publishes WHERE ITS OWN MATTER IS ABSENT — its door law is that its
absence is exactly nothing (or exactly the whole frame), never that its `fit` shows a whole,
undistorted photograph, because a voice that can be layered over another one is not obliged to BE
the photograph at its own door the way a ground is. That is a different, legitimate mechanism from
the whole-work equation this law states, so this file reads `manifest.coverage.writes` off every
instrument and skips judging any that answer `true` — never a name typed by hand, so an instrument
that changes its own coverage declaration re-scopes this file by itself. `overlay` is exempted by
exactly this principle (`pass-inst-overlay.js`'s own manifest declares `coverage: {writes: true}`),
not because its own `fit` was re-read and excused.

`droste` DECLARES `coverage: {writes: false}` — it is a ground, obliged to answer this law, and it
does not: its own `fit` (`pass-inst-droste.js:473-478`) reads `Sw = max(frameAspect, sourceAspect)`
and returns `[1/Sw, sourceAspect/Sw, 0, 0]`, up to 2.16× off the law's own `cover(aspect)/c` on the
wide-source case measured here. THIS IS A GENUINE FINDING, LEFT RED ON PURPOSE, NOT EXEMPTED AND NOT
SILENCED. Phase 1 (cause A) lifted the tier-ladder gate that had barred droste from casting at all,
so it is back in the castable arsenal — correctly, that repair was general and droste was never the
instance it was written against — but nothing has yet read whether droste's own door survives a real
crossing, and this file's own six-case check says its `fit` does not answer the shared law any
correctly-behaving ground already does. Its owner is the deferred re-anchoring work Phase 2's own
scope excludes by name (`docs/V2-CONVERGENCE-PLAN-2026-08-31.md`'s "do not attempt to re-anchor the
other 24 instruments' own door proofs") — this row is what hands that phase a citation instead of a
rediscovery, and reading it green by excepting droste the way `overlay` is excepted would have hidden
exactly the fact Phase 1's own repair needs on record: a castable instrument with an unproven door.

WHAT THIS FILE DOES NOT PROVE. That `fit` answers the law says nothing about whether an instrument's
OWN shader routes its texture sampling through `uFitA` at all in the way this law assumes cancels —
box-fold's own bug was exactly this shape: `fit` could have divided by CROP from the start and the
box would still have shown 1.9 at a real door, because the crop was ALSO baked into the box's own
3D geometry, a channel this law cannot see and `seated` cannot reach. That is why Phase 2's own
verification standard is a REAL composed pair at a REAL door (`tests/test_pass_hang.py`,
`tests/test_pass_seam.py`), never this file alone — this file is the cheap, fleet-wide, by-
construction half of the proof; the pixel-level half stays where a real door is actually driven.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "engine" / "assets"

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


def run_node(driver_text, files):
    """`driver_text` under a real node, in a throwaway directory, with `files` written beside it and
    handed to it as argv in the dict's own order. Returns the parsed JSON of the last line, or an
    {"error": ...} dict, so a row that could not run reads as a stated failure."""
    d = Path(tempfile.mkdtemp(prefix="synth_doorinvnode_"))
    try:
        (d / "driver.js").write_text(driver_text, encoding="utf-8")
        paths = []
        for name, text in files.items():
            p = d / name
            p.write_text(text, encoding="utf-8")
            paths.append(str(p))
        proc = subprocess.run(["node", str(d / "driver.js")] + paths,
                              capture_output=True, text=True, timeout=300)
        if proc.returncode != 0:
            return {"error": (proc.stderr or "").strip()[-500:]}
        lines = proc.stdout.strip().splitlines()
        if not lines:
            return {"error": "the driver printed nothing"}
        return json.loads(lines[-1])
    except Exception as e:
        return {"error": str(e)}
    finally:
        shutil.rmtree(d, ignore_errors=True)


# Six aspect-ratio cases: a wide source in a narrow frame, a narrow source in a wide frame, a square
# source, a source that exactly matches the frame, a large source at the same narrow frame (the
# scale, not just the ratio, must not matter), and the frame itself turned on its side.
CASES = [(1600, 900, 390, 844), (900, 1600, 390, 844), (1000, 1000, 390, 844),
         (390, 844, 390, 844), (3000, 2000, 780, 1688), (844, 390, 844, 390)]

# Every instrument the fleet ships, found by its own file rather than by a list typed here.
FILES = sorted(ASSETS.glob("pass-inst-*.js"))

DRIVER = r"""
"use strict";
const fs = require("fs"), vm = require("vm"), path = require("path");
const CASES = %s;
const out = [];
for (const p of process.argv.slice(2)) {
  const source = fs.readFileSync(p, "utf8").replace(/@@NS@@/g, "ex");
  let joined = null;
  const sandbox = {window: {__exPassInstrument: (m) => { joined = m; }},
                   console: {log(){}, warn(){}, error(){}}};
  vm.createContext(sandbox);
  try { vm.runInContext(source, sandbox, {filename: path.basename(p)}); }
  catch (e) { out.push({file: path.basename(p), error: "load: " + e.message}); continue; }
  if (!joined || !joined.instrument || typeof joined.instrument.fit !== "function") {
    out.push({file: path.basename(p), error: "publishes no fit()"});
    continue;
  }
  const fit = joined.instrument.fit;
  const manifest = joined.instrument.manifest;
  const framings = manifest && manifest.framings;
  const reads = CASES.map(function (c) {
    var iw = c[0], ih = c[1], w = c[2], h = c[3], r;
    try { r = fit(iw, ih, w, h); } catch (e) { return { case: c, error: e.message }; }
    return { case: c, fit: r };
  });
  out.push({ file: path.basename(p), id: manifest && manifest.id,
             coverCrop0: framings && framings["0"] && framings["0"].coverCrop,
             coverCrop1: framings && framings["1"] && framings["1"].coverCrop,
             writesCoverage: !!(manifest && manifest.coverage && manifest.coverage.writes === true),
             reads: reads });
}
console.log(JSON.stringify(out));
""" % json.dumps(CASES)


def cover(iw, ih, w, h):
    """The plain cover fit, the shape `pass-inst-adrift.js` and every correctly-behaving cropped
    instrument already carry: the smaller of the two scales that lets the source cover the frame,
    the other held at 1."""
    fa = w / float(h)
    ia = iw / float(ih)
    if ia > fa:
        return (fa / ia, 1.0)
    return (1.0, ia / fa)


# THE ONE PRINCIPLED EXEMPTION (see the docstring's own citation): `coverage.writes === true`, read
# off each instrument's own manifest by the driver above, never a name typed here by hand.
EXEMPT_REASON = ("its own manifest declares `coverage: {writes: true}` — it publishes where its own "
                 "matter is absent, so its door law is that absence, not the whole-work equation "
                 "this file states")

if not node_available():
    for row in ("PASS-DOOR-INV every ground instrument's own fit divides the plain cover fit by "
                "its declared crop",
                "PASS-DOOR-INV box-fold and hero specifically now answer to the law",
                "PASS-DOOR-INV the absence exemption is read off coverage.writes, and overlay is "
                "exactly what it exempts",
                "PASS-DOOR-INV droste's own fit divides the plain cover fit by its declared crop",
                "PASS-DOOR-INV red-on-bug · box-fold and hero's pre-repair fit fails this same law"):
        skip(row, "node is not installed (pinned expected skip)")
else:
    shipped = run_node(DRIVER, {f.name: f.read_text(encoding="utf-8") for f in FILES})
    rows = {} if isinstance(shipped, dict) else {r["file"]: r for r in shipped}
    err = shipped.get("error") if isinstance(shipped, dict) else None

    def mismatches(row):
        """The cases, if any, where this instrument's own `fit` disagrees with the law by more than
        floating-point noise. `c` is read off the instrument's own declared door crop; an instrument
        naming none (no `framings` block) answers to a crop of 1, the law's own neutral."""
        if row.get("error"):
            return [("error", row["error"])]
        c0, c1 = row.get("coverCrop0"), row.get("coverCrop1")
        if c0 is None or c1 is None or abs(c0 - c1) > 1e-9:
            return [("crop", "framings[\"0\"].coverCrop and framings[\"1\"].coverCrop must both be "
                             "declared and equal — read %r and %r" % (c0, c1))]
        bad = []
        for rd in row["reads"]:
            if "error" in rd:
                bad.append((rd["case"], "fit() itself threw: %s" % rd["error"]))
                continue
            iw, ih, w, h = rd["case"]
            cx, cy = cover(iw, ih, w, h)
            expect = [cx / c0, cy / c0, 0.0, 0.0]
            got = rd["fit"]
            diff = max(abs(a - b) for a, b in zip(expect, got))
            if diff > 1e-9:
                bad.append((rd["case"], "expected %s, fit() answered %s (off by %.4f)"
                                        % (expect, got, diff)))
        return bad

    ALL_NAMES = sorted(r.get("id") or f.replace("pass-inst-", "").replace(".js", "")
                       for f, r in rows.items())
    EXEMPT = {f: r for f, r in rows.items() if r.get("writesCoverage")}
    JUDGED = {f: r for f, r in rows.items() if not r.get("writesCoverage")}
    DROSTE_FILE = "pass-inst-droste.js"
    JUDGED_LESS_DROSTE = {f: r for f, r in JUDGED.items() if f != DROSTE_FILE}
    judged_bad = {r.get("id", f): mismatches(r) for f, r in JUDGED_LESS_DROSTE.items()}
    judged_bad = {k: v for k, v in judged_bad.items() if v}

    check("PASS-DOOR-INV every ground instrument's own fit divides the plain cover fit by its "
          "declared crop",
          not err and len(rows) == len(FILES) and not judged_bad,
          ("all %d instruments read; %d of them exempted as absence-only voices "
           "(coverage.writes===true); of the %d grounds judged against the law, %d answer to it — "
           "droste held apart below as its own, separately-reported finding rather than folded into "
           "this count"
           % (len(rows), len(EXEMPT), len(JUDGED), len(JUDGED_LESS_DROSTE) - len(judged_bad))
           if not err and not judged_bad
           else "driver: %s; failing: %s" % (err, judged_bad)))

    box_hero_ok = (not rows.get("pass-inst-boxfold.js", {}).get("error")
                   and not mismatches(rows.get("pass-inst-boxfold.js", {}))
                   and not rows.get("pass-inst-hero.js", {}).get("error")
                   and not mismatches(rows.get("pass-inst-hero.js", {})))
    check("PASS-DOOR-INV box-fold and hero specifically now answer to the law",
          not err and box_hero_ok,
          ("boxfold: fit divides the plain cover fit by 1.9 on all six cases; hero: fit multiplies "
           "it by 0.94 (equivalently divides by its own declared crop, 1/0.94) on all six cases — "
           "the exact repair cause B asked for, checked by the same arithmetic every other cropped "
           "instrument in the fleet already answers to"
           if box_hero_ok else "driver: %s" % err))

    overlay_row = rows.get("pass-inst-overlay.js", {})
    check("PASS-DOOR-INV the absence exemption is read off coverage.writes, and overlay is exactly "
          "what it exempts",
          not err and set(EXEMPT) and "pass-inst-overlay.js" in EXEMPT
          and DROSTE_FILE not in EXEMPT
          and overlay_row.get("writesCoverage") is True,
          ("%d instrument(s) exempted by their own declared coverage.writes: %s. overlay is among "
           "them (%s); droste is NOT (its own manifest declares coverage.writes: false), so it stays "
           "judged rather than being excepted the same way"
           % (len(EXEMPT), sorted(r.get("id", f) for f, r in EXEMPT.items()), EXEMPT_REASON)
           if not err else "driver: %s" % err))

    # THIS ROW IS EXPECTED TO STAY RED, ON PURPOSE. droste declares `coverage.writes: false` — a
    # ground, obliged to answer the shared law — and it does not, so the row asserting that it does
    # is left standing and genuinely fails, rather than being folded into an "excepted" list the way
    # overlay is. A red row here is the recorded finding; the detail names its own owner.
    droste_row = rows.get(DROSTE_FILE, {})
    droste_bad = mismatches(droste_row) if droste_row else [("error", "no reading for droste")]
    droste_worst = max((abs(rd["fit"][0] / max(cover(*rd["case"])[0], 1e-9))
                        for rd in droste_row.get("reads", [])
                        if "error" not in rd and cover(*rd["case"])[0] > 1e-9), default=0.0)
    check("PASS-DOOR-INV droste's own fit divides the plain cover fit by its declared crop",
          not err and droste_row.get("writesCoverage") is False and not droste_bad,
          ("EXPECTED TO FAIL — a recorded, owned finding, not a regression to chase in this phase. "
           "droste declares coverage.writes: false (a ground, obliged to answer the law) and its own "
           "`fit` misses it on %d of %d cases, up to a %.2f× mismatch on the widest case: %s. "
           "Genuinely castable since Phase 1's tier-ladder repair (cause A) lifted the gate that used "
           "to bar it, and genuinely unverified at its own door since nothing has re-anchored its "
           "`fit` to the shared law — left red rather than excepted the way overlay is, because "
           "excepting it would have hidden the one fact Phase 1's own repair needs on record: a "
           "castable instrument with an unproven door. Owner: the deferred re-anchoring work "
           "docs/V2-CONVERGENCE-PLAN-2026-08-31.md's Phase 2 names out of its own scope (\"do not "
           "attempt to re-anchor the other 24 instruments' own door proofs\")"
           % (len(droste_bad), len(CASES), droste_worst, droste_bad)
           if not err else "driver: %s" % err))

    # ---------------------------------------------------------------- red-on-bug
    # THE PROOF THAT THIS LAW WOULD HAVE CAUGHT CAUSE B BEFORE A VISITOR EVER SAW IT: the pre-repair
    # `fit` for box-fold and hero, read off this branch's own parent commit — never a second guess at
    # what the bug looked like, the actual bytes this repair replaced.
    import subprocess as _sp
    def git_show(path):
        try:
            r = _sp.run(["git", "show", "HEAD:%s" % path], cwd=str(ROOT),
                        capture_output=True, text=True, timeout=30)
            return r.stdout if r.returncode == 0 else None
        except Exception:
            return None

    pre_box = git_show("engine/assets/pass-inst-boxfold.js")
    pre_hero = git_show("engine/assets/pass-inst-hero.js")
    if pre_box is None or pre_hero is None:
        skip("PASS-DOOR-INV red-on-bug · box-fold and hero's pre-repair fit fails this same law",
             "could not read this branch's own parent commit for the pre-repair bytes")
    else:
        planted = run_node(DRIVER, {"pass-inst-boxfold.js": pre_box, "pass-inst-hero.js": pre_hero})
        prows = {} if isinstance(planted, dict) else {r["file"]: r for r in planted}
        perr = planted.get("error") if isinstance(planted, dict) else None
        pre_box_bad = mismatches(prows.get("pass-inst-boxfold.js", {}))
        pre_hero_bad = mismatches(prows.get("pass-inst-hero.js", {}))
        check("PASS-DOOR-INV red-on-bug · box-fold and hero's pre-repair fit fails this same law",
              not perr and bool(pre_box_bad) and bool(pre_hero_bad),
              ("box-fold's pre-repair fit (plain cover, no crop divided in) misses the law on %d of "
               "%d cases; hero's (plain cover multiplied by nothing) misses it on %d of %d — the "
               "same law that reads green on both files as they ship now reddens on the bytes it "
               "replaced, so this is a proof of the repair and not of the weather"
               % (len(pre_box_bad), len(CASES), len(pre_hero_bad), len(CASES))
               if not perr else "driver: %s" % perr))

# ------------------------------------------------------------------------------------ the report
print("PASS-DOOR-INVARIANT — one fleet-wide, by-construction proof that a crop cancels at a real "
      "door\n")
for name, verdict, detail in results:
    print("[%s] %s" % (verdict, name))
    if detail:
        print("        " + detail)
passed = sum(1 for _, v, _ in results if v == "PASS")
failed = sum(1 for _, v, _ in results if v == "FAIL")
skipped = sum(1 for _, v, _ in results if v == "SKIP")
print("\n%d passed / %d failed / %d skipped" % (passed, failed, skipped))
sys.exit(1 if failed else 0)
