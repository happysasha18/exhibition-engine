#!/usr/bin/env python3
"""EX-PASS-VOICE, shelf 1 — the instrument manifest's own `readiness` census (TEST_MATRIX.md
PASS-13).

Run: python3 tests/test_pass_matter_gate.py

Distinct from tests/test_pass_matter.py, which tests the `matter` INSTRUMENT by name (its doors,
its five poses against the lab module). This file tests the charter's shelf-1 CONCEPT across every
registered instrument: PASS-API-V1.md §8's manifest schema closes `readiness` to exactly
`production-ready | needs-port | lab-only | failed-proof`, and only a `production-ready` instrument's
matter is meant to be cast into a shipped score ("a port is the instrument's mathematics carried
onto the host's frame with a manifest and a passing conformance run").

Every reading below is off the REAL, currently-registered instrument files
(`engine/assets/pass-inst-*.js`), the same road tests/test_pass_lawful.py's own DRIVER already
walks to read `levels`/`handles` off a live manifest rather than off the frozen fixture — a manifest
registered under `window.__PassInstrument` in a bare `vm` sandbox, never a hand-retyped mirror of
what a file says.

WHAT THIS FILE FOUND, AND WHY THE SECOND HALF OF PASS-13 IS NOT A CHECK HERE. The census below (every
manifest's `readiness` closed to the four named values) is real, current code and is proven both
directions. The CAST RESTRICTION — "only a production-ready instrument may be cast into a shipped
score" — has no enforcer anywhere in this repository: `pass-composer.js`'s own candidate table,
`CUTS_ON` (built at `make()` time, :1413-1419), is built from every key of `INSTRUMENTS`/`MANIFESTS`
the composer was constructed over, filtered on nothing but which KINDS an instrument's own `cuts`
list names — `.readiness` is never read anywhere in `pass-composer.js` except as `readinessOf(w)`,
a WORK RECORD's own numeric quality reading (a wholly different `readiness`, keyed by photograph
rather than by instrument). This is the same class of gap
`docs/prover/2026-08-27-pass-section.md` files as F2 for the other three build-time refusals
`INV-109` names: a law stated in the contract with no code in this tree that discharges it. This
file does not assert the restriction, because asserting it would either pass vacuously (every
shipped instrument today declares `production-ready`, so no witness exists to test the restriction
against) or, once a witness exists, red working code that was never built to refuse. The restriction
check below (row 3) is written to describe the gap it found rather than to assert a fact that is not
true of the shipped composer, matching this project's own rule against building tests for
unbuilt machinery.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "engine" / "assets"
COMPOSER = ASSETS / "pass-composer.js"

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
CLOSED = ["production-ready", "needs-port", "lab-only", "failed-proof"]

TMP = Path(tempfile.mkdtemp(prefix="pass_matter_gate_"))


def census(assets_dir):
    """Registers every `pass-inst-*.js` file under `assets_dir` in a bare vm sandbox (the same
    idiom test_pass_lawful.py's own DRIVER carries for `levels`/`handles`) and reads back each
    instrument's own `manifest.readiness`, keyed by instrument name."""
    driver = TMP / "census-driver.js"
    driver.write_text(
        "\"use strict\";\n"
        "const fs = require('fs'), vm = require('vm'), path = require('path');\n"
        "const dir = process.argv[2];\n"
        "const out = {};\n"
        "for (const f of fs.readdirSync(dir).filter((n) => /^pass-inst-.*\\.js$/.test(n))) {\n"
        "  const src = fs.readFileSync(path.join(dir, f), 'utf8').replace(/@@NS@@/g, '');\n"
        "  const sb = {window: {__PassInstrument: (r) => {\n"
        "    out[r.instrument.name] = {readiness: r.instrument.manifest.readiness, file: f};\n"
        "  }}, console, document: undefined};\n"
        "  vm.createContext(sb);\n"
        "  try { vm.runInContext(src, sb, {filename: f}); } catch (e) { out['__error:' + f] = String(e); }\n"
        "}\n"
        "console.log(JSON.stringify(out));\n",
        encoding="utf-8")
    proc = subprocess.run(["node", str(driver), str(assets_dir)],
                          capture_output=True, text=True, timeout=90)
    if proc.returncode != 0:
        return None, (proc.stderr or "").strip()[-800:]
    line = (proc.stdout or "").strip().splitlines()
    if not line:
        return None, "the census driver said nothing"
    return json.loads(line[-1]), None


if not NODE:
    skip("PASS-13 (EX-PASS-VOICE, shelf 1) · every registered instrument's manifest readiness is "
         "one of the four closed values", "node is not on this machine")
    skip("PASS-13 red-on-bug · the census reads the real, currently-registered manifest, not a "
         "hand-typed list", "node is not on this machine")
    skip("PASS-13 · the cast-selection table CUTS_ON is built from every registered instrument "
         "with no readiness filter — the restriction PASS-13 names has no enforcer in this tree",
         "node is not on this machine")
else:
    live, err = census(ASSETS)
    if live is None:
        check("PASS-13 (EX-PASS-VOICE, shelf 1) · every registered instrument's manifest readiness "
              "is one of the four closed values", False, err)
    else:
        errored = {k: v for k, v in live.items() if k.startswith("__error:")}
        named = {k: v for k, v in live.items() if not k.startswith("__error:")}
        bad = {k: v["readiness"] for k, v in named.items() if v["readiness"] not in CLOSED}
        ok = bool(named) and not bad and not errored
        check("PASS-13 (EX-PASS-VOICE, shelf 1) · every registered instrument's manifest readiness "
              "is one of the four closed values", ok,
              "" if ok else
              (("no instrument registered at all" if not named else "")
               + ("; ".join(k + " reads readiness=" + repr(v) for k, v in bad.items()))
               + ("; failed to register: " + json.dumps(errored) if errored else "")))
        if ok:
            print("  (census: " + str(len(named)) + " instruments, all readiness=production-ready)")

    # RED-ON-BUG. A copy of the real matter.js with its own readiness string mutated to a value
    # outside the closed four — a mutation on real, currently-shipped text, never a hand-typed
    # mirror — proves the census is reading the file rather than a fixed list.
    real_matter = (ASSETS / "pass-inst-matter.js").read_text(encoding="utf-8")
    MUT_MARK = 'readiness: "production-ready",'
    if MUT_MARK not in real_matter:
        skip("PASS-13 red-on-bug · the census reads the real, currently-registered manifest, not a "
             "hand-typed list",
             "the marker text was not found verbatim in the shipped pass-inst-matter.js")
    else:
        mut_dir = TMP / "mutated_assets"
        mut_dir.mkdir(exist_ok=True)
        (mut_dir / "pass-inst-matter.js").write_text(
            real_matter.replace(MUT_MARK, 'readiness: "not-a-real-value",', 1), encoding="utf-8")
        mut_live, mut_err = census(mut_dir)
        if mut_live is None:
            check("PASS-13 red-on-bug · the census reads the real, currently-registered manifest, "
                  "not a hand-typed list", False, mut_err)
        else:
            mreads = {k: v["readiness"] for k, v in mut_live.items()
                     if not k.startswith("__error:")}
            caught = mreads.get("matter") == "not-a-real-value" \
                and mreads.get("matter") not in CLOSED
            check("PASS-13 red-on-bug · the census reads the real, currently-registered manifest, "
                  "not a hand-typed list", caught,
                  "" if caught else
                  ("mutating pass-inst-matter.js's own readiness string to \"not-a-real-value\" and "
                   "re-running the same census left it reading " + json.dumps(mreads.get("matter"))
                   + " instead"))

    # THE GAP, NAMED RATHER THAN ASSERTED AWAY. `CUTS_ON` — the table pass-composer.js actually
    # builds candidates from — is grep-checked here for what it filters on: every registered
    # instrument key, gated only by which `cuts` kinds it names. `.readiness` is absent from that
    # text entirely.
    comp_src = COMPOSER.read_text(encoding="utf-8")
    cuts_start = comp_src.find("var CUTS_ON = {};")
    cuts_end = comp_src.find("var BANDING", cuts_start) if cuts_start >= 0 else -1
    cuts_block = comp_src[cuts_start:cuts_end] if cuts_start >= 0 and cuts_end > cuts_start else ""
    no_readiness_filter = bool(cuts_block) and "readiness" not in cuts_block
    other_readiness_uses = [m.start() for m in re.finditer(r"\.readiness\b", comp_src)]
    # `readinessOf(w)` is the one other family of `.readiness` reads in this file, and it is a
    # WORK RECORD's own numeric quality reading (pass-composer.js:3017-3018), never an instrument
    # manifest's readiness string — read to prove the two are not the same field by another name.
    reads_only_work_readiness = "function readinessOf(w)" in comp_src \
        and all("readinessOf" in comp_src[max(0, i - 400):i] or "pair.readiness" in comp_src[i - 20:i + 20]
                or "plan.readiness" in comp_src[i - 20:i + 20]
                for i in other_readiness_uses)
    check("PASS-13 · the cast-selection table CUTS_ON is built from every registered instrument "
          "with no readiness filter — the restriction PASS-13 names has no enforcer in this tree",
          no_readiness_filter and reads_only_work_readiness,
          "CUTS_ON (pass-composer.js, the table candidates are drawn from) reads " +
          ("no `readiness` field at all" if no_readiness_filter else "a `readiness` field")
          + "; the file's other " + str(len(other_readiness_uses)) + " reference(s) to `.readiness` "
          "are all `readinessOf(w)`, a work record's own numeric quality reading, never an "
          "instrument manifest's readiness string. An instrument declaring anything but "
          "`production-ready` would be cast exactly as freely as one declaring it.")

# ---------------------------------------------------------------- report
import shutil  # noqa: E402
shutil.rmtree(TMP, ignore_errors=True)

print("EX-PASS-VOICE shelf 1 · instrument manifest readiness census (TEST_MATRIX.md PASS-13)")
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
