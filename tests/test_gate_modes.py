#!/usr/bin/env python3
"""S-114 — the gate's own laws: what proof a fact owes, and what a mode may and may not leave out.
Run: python3 tests/test_gate_modes.py

Root: his word of 06.09.2026 22:14. `TEST_MATRIX.md` holds a catalogue of requirements and of the
proof each one owes; it was being read as a list of runs owed after every commit, so a change to a
document stood behind the whole browser roster. The repair names five PROOF LAYERS and three MODES.
This file is what keeps both honest.

WHY THIS SUITE EXISTS RATHER THAN A SENTENCE IN A COMMENT. Every claim below was, before this file,
a sentence somewhere asserting itself: the five layer names "are the same words" in three documents,
the narrow modes "never skip a check in silence", the full gate "builds one base stage". A gate
anchored on comment text passes vacuously — this tree has reopened rows for exactly that twice — so
each of those sentences is read here against the thing it describes.

WHAT THIS FILE IS NOT. It is at the `static/source contract` layer and it starts no browser, with one
exception it names out loud: the base-stage law is a claim about what BAKING does, so it bakes twice
and reads what the cache did. That is a bake, not a browser, and it is the cheapest honest proof of
the claim.

NOTHING HERE MEASURES THIS MACHINE. Not one row reads a clock, and the one row that runs work counts
BUILDS rather than seconds. That is the whole point of the row this file belongs to (S-113 before it,
S-114 around it): how fast the builder host happens to be is never a product fact.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / "tests"
sys.path.insert(0, str(HERE))

import run_all  # noqa: E402 — the runner is the thing under test

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


PROFILE = ROOT / ".live-spec" / "profile.md"
MATRIX = ROOT / "TEST_MATRIX.md"
RUNNER = HERE / "run_all.py"


# ---------------------------------------------------------------- one vocabulary, three homes
# THE FIVE NAMES ARE THE JOINT between a document a person reads and a program that selects. If the
# runner's `LAYER_PIXEL` said "pixel tests" while the matrix said "pixel/WebGL/layout/interaction",
# both would be right about themselves and the pair would be useless: nobody could check one against
# the other, and the drift would only show as an argument months later about what a row meant.
prof, mat, run = (p.read_text(encoding="utf-8") for p in (PROFILE, MATRIX, RUNNER))

check("GATE the five proof layers are five, and the runner names exactly them",
      len(run_all.PROOF_LAYERS) == 5 and len(set(run_all.PROOF_LAYERS)) == 5,
      f"the runner declares {list(run_all.PROOF_LAYERS)}")

missing = {layer: [n for n, t in (("profile", prof), ("matrix", mat), ("runner", run))
                   if layer not in t]
           for layer in run_all.PROOF_LAYERS}
check("GATE every proof layer is stated in the same words in the profile, the matrix and the runner",
      not any(missing.values()),
      "; ".join(f"«{k}» missing from {', '.join(v)}" for k, v in missing.items() if v)
      or "all five stand verbatim in all three")

# HIS OWN WORD, RECORDED VERBATIM. The kind line stood open as ⟨owner⟩ from adoption because ADOPT.md
# asks it and never infers it; it was answered on 06.09.2026 and the answer is his sentence, not a
# reading of the tree. A row that let the sentence drift, or let the placeholder come back, would be
# a row that let an agent decide what this project IS.
KIND = ("reusable browser-based generative exhibition/rendering engine with a static site shell, "
        "compile-time per-image WorkRecords, and runtime WebGL composition")
check("GATE the host profile carries the owner's own project kind, and no placeholder stands",
      KIND in " ".join(prof.split()) and "project.kind: ⟨owner⟩" not in prof,
      "the kind line reads his sentence" if KIND in " ".join(prof.split())
      else "the kind line does not carry his sentence verbatim")


# ---------------------------------------------------------------- the layer of a suite is read
# A SUITE'S LAYER IS A FACT ABOUT WHAT IT DOES, not an entry in a table. These rows check the reading
# against suites whose behaviour is not in doubt, and then check that the reading answers for every
# suite on the roster — a suite the reading cannot place would be a suite no mode could reason about.
placed = {}
unplaceable = []
for suite in run_all.SUITES:
    try:
        placed[suite] = run_all.layer_of(suite)
    except Exception as exc:  # pragma: no cover — a missing file is check_roster's own red
        unplaceable.append(f"{suite}: {exc}")
check("GATE every suite on the roster is placed at one of the five layers",
      not unplaceable and set(placed.values()) <= set(run_all.PROOF_LAYERS),
      f"{len(placed)} suites placed; " + ("none unplaceable" if not unplaceable
                                          else "; ".join(unplaceable))
      + "; the roster stands at "
      + ", ".join(f"{lay}: {sum(1 for v in placed.values() if v == lay)}"
                  for lay in run_all.PROOF_LAYERS))

# THE READING IS DELIBERATELY CONSERVATIVE IN ONE DIRECTION. It looks for the constructor's own
# spelling in the source, so a suite that only MENTIONS it in a comment is placed at a browser layer
# and runs where it need not. That costs a Chrome. The other direction — a suite that really drives a
# browser being placed below one — would let a mode skip a real check, and this rule cannot make that
# mistake: the constructor cannot be called without the spelling being there. When the two errors are
# a wasted browser and a missed proof, the reading must be able to make only the first.
#
# This file spells the constructor as two pieces for exactly that reason: it needs to talk ABOUT the
# spelling without being read as using it, and it stands at the static layer so the gate's own laws
# cost no browser.
CTOR = "Browser" + "("
check("GATE a suite that drives a browser is never placed below the browser layers",
      all(placed.get(s) in (run_all.LAYER_RUNTIME, run_all.LAYER_PIXEL)
          for s in run_all.SUITES
          if CTOR in (HERE / f"test_{s}.py").read_text(encoding="utf-8", errors="replace")),
      "every suite constructing the headless driver stands at «browser runtime contract» or "
      "«pixel/WebGL/layout/interaction»")

check("GATE this suite itself is at the static layer, so the gate's own laws cost no browser",
      placed.get("gate_modes") == run_all.LAYER_STATIC,
      f"gate_modes stands at «{placed.get('gate_modes')}»")

# NO SUITE MAY CLAIM THE LIVE-DEVICE LAYER. That layer is read in the visitor's own browser after a
# deploy; a suite in this tree claiming it would be claiming the very measurement S-113 banned — the
# builder host standing in for a phone.
check("GATE no suite in this tree claims the live-device layer, because the builder is not a device",
      run_all.LAYER_DEVICE not in placed.values(),
      "the live-device layer is declared and deliberately carries no suite (S-113)")


# ---------------------------------------------------------------- what the three modes select
def sel(mode, acceptance=(), changed=()):
    return run_all.select(mode, list(acceptance), list(changed))


chosen, why, omitted = sel("release")
check("GATE release covers the whole roster and leaves nothing out",
      chosen == list(run_all.SUITES) and omitted is None,
      f"{len(chosen)} of {len(run_all.SUITES)}")

# THE DEFAULT IS THE SAFE ANSWER. Read off the runner's own argument parser rather than asserted: a
# default nobody has to remember to ask for is the only kind that survives a tired evening.
check("GATE naming no mode is the full gate",
      re.search(r'--mode[\s\S]*?default="release"', run) is not None,
      "the runner's own parser defaults --mode to release")

# A CROSS-CUTTING CHANGE WIDENS. Each name on that list is a file literally every suite of some layer
# loads or is built by, so a narrow run over one of them would be a narrow run over everything.
for shared in run_all.CROSS_CUTTING:
    chosen, why, omitted = sel("row", ("pass_seam",), (shared,))
    ok = chosen == list(run_all.SUITES)
    check(f"GATE a change to {shared} widens even a row gate to the whole roster", ok,
          (why[chosen[0]] if ok else f"only {len(chosen)} suite(s) selected, which is a hole"))

# A CHANGE NOBODY CAN ATTRIBUTE WIDENS. This is the clause that makes the selector safe to trust: it
# cannot narrow over a file it does not understand, so a new component arriving with no suite naming
# it gets the whole roster rather than silence.
# THE PATH IS ASSEMBLED RATHER THAN TYPED, because the reader searches every suite's source for it
# and this file is one of those suites: written out whole, the name would be found here and the very
# case the row is testing would never arise.
STRANGER = "engine/assets/" + "a-file-no-suite" + "-has-ever-heard-of.js"
chosen, why, omitted = sel("row", (), (STRANGER,))
check("GATE a changed path no suite's source names widens to the whole roster rather than narrowing",
      chosen == list(run_all.SUITES),
      (why[chosen[0]] if chosen else "nothing selected, which is the hole this row exists to close"))

# DOCUMENTS REACH NO SUITE'S SOURCE, so a docs-only change owes the architectural invariants and
# nothing browser-heavy. This is the row his complaint actually names: an edit to a document standing
# behind the whole browser roster.
chosen, why, omitted = sel("row", (), ("README.md", "TEST_MATRIX.md", "docs/V2-STATUS.md"))
docs_only_ok = (set(chosen) == {s for s in run_all.ARCH_INVARIANTS if s in run_all.SUITES}
                and chosen != list(run_all.SUITES))
check("GATE a docs-only change selects the architectural invariants and not the browser roster",
      docs_only_ok,
      f"{len(chosen)} suite(s): {', '.join(chosen)}")

browser_layers = {run_all.LAYER_RUNTIME, run_all.LAYER_PIXEL}
check("GATE a docs-only selection is genuinely cheap: it is a small set, not the roster in disguise",
      len(chosen) < len(run_all.SUITES) / 4,
      f"{len(chosen)} of {len(run_all.SUITES)} suite(s), of which "
      f"{sum(1 for s in chosen if placed[s] in browser_layers)} need a browser")

# EVERY MODE CARRIES THE INVARIANTS. A narrow mode with nothing constant in it proves only what its
# author already suspected.
for mode in ("row", "integration"):
    chosen, why, omitted = sel(mode, (), ("tests/fixture_pass_works.json",))
    have = [s for s in run_all.ARCH_INVARIANTS if s in run_all.SUITES]
    check(f"GATE the {mode} gate carries every architectural invariant, whatever changed",
          all(s in chosen for s in have),
          f"carries {', '.join(have)}")

# INTEGRATION IS WIDER THAN A ROW GATE BY CONSTRUCTION, not by having more names typed into it: it
# takes the WHOLE of every layer the change touches.
touching = ("engine/assets/pass-inst-hero.js",)
row_sel, _, _ = sel("row", ("pass_hero",), touching)
int_sel, int_why, _ = sel("integration", ("pass_hero",), touching)
check("GATE the integration gate is a superset of the row gate on the same change",
      set(row_sel) <= set(int_sel),
      f"row {len(row_sel)} ⊆ integration {len(int_sel)}")
# THE LAYERS THIS CHANGE TOUCHES are the layers of the suites the change itself reached — its
# acceptance and the suites whose source names it. The architectural invariants a row gate always
# carries are not "touched" by anything; they ride along in every mode, and asking integration to
# widen to their layers too would make every change a full gate and the mode meaningless.
_touched = {placed[s] for s in row_sel if s not in run_all.ARCH_INVARIANTS}
check("GATE the integration gate takes every proof at each layer the change touches",
      len(int_sel) > len(row_sel)
      and all(s in int_sel for s in run_all.SUITES if placed[s] in _touched),
      f"integration selected {len(int_sel)} against the row gate's {len(row_sel)}, taking every "
      f"proof at {', '.join(sorted(_touched))}")

# NOTHING IS EVER LEFT OUT IN SILENCE. Every selected suite carries the sentence that put it there,
# and any omission carries one sentence of its own.
chosen, why, omitted = sel("row", ("pass_seam",), ("engine/assets/pass-inst-hero.js",))
check("GATE every selected suite carries the reason it was selected",
      all(why.get(s) for s in chosen), f"{len(chosen)} suite(s), {len(why)} reason(s)")
check("GATE a narrow selection states its own omission",
      bool(omitted) and str(len(run_all.SUITES) - len(chosen)) in omitted,
      (omitted or "no omission stated")[:160])

# AN ACCEPTANCE NAMING NOTHING RUNNABLE IS REFUSED rather than quietly ignored — a row whose
# acceptance names a suite that does not exist has no acceptance at all.
try:
    sel("row", ("a_suite_that_does_not_exist",), ())
    refused = False
except SystemExit:
    refused = True
check("GATE an acceptance naming a suite that does not exist refuses the run",
      refused, "the runner exits rather than running a row with no acceptance behind it")


# ---------------------------------------------------------------- the two gates that already stood
# THE ROSTER GATE AND THE SKIP RATCHET SURVIVE THE MODES. Both are whole-roster facts and both run
# before a single suite is spawned, in every mode — a narrow run over a wrong roster is as worthless
# as a full one. These rows read that they are still the runner's own and still load-bearing.
check("GATE the roster gate still stands and still runs in every mode",
      callable(getattr(run_all, "check_roster", None))
      and "check_roster()" in run.split("def main(")[1],
      "check_roster is called from main, before the queue is built")
check("GATE the skip ratchet still stands",
      callable(getattr(run_all, "check_skip_ratchet", None)),
      "check_skip_ratchet is the runner's own")

# PLANTED: a roster with a name behind no file must refuse the run. The plant is put on the module's
# own list and taken off again, so nothing on disk is touched.
_real = run_all.SUITES
try:
    run_all.SUITES = list(_real) + ["a_suite_with_no_file"]
    try:
        run_all.check_roster()
        caught = False
    except SystemExit:
        caught = True
finally:
    run_all.SUITES = _real
check("GATE planted · a roster naming a suite with no file behind it refuses the run",
      caught, "the roster gate reds on the plant, so it is not asserting itself")

# PLANTED: a skip count above the recorded one must refuse the run.
ratchet = json.loads(run_all.SKIP_RATCHET_PATH.read_text())["total_skips"] \
    if run_all.SKIP_RATCHET_PATH.exists() else None
if ratchet is None:
    skip("GATE planted · a run that skips more than the record allows may not go green",
         "no tests/skip_ratchet.json stands yet, so there is nothing to plant against")
else:
    grew = run_all.check_skip_ratchet(ratchet + 1)
    run_all.SKIP_RATCHET_PATH.write_text(json.dumps({"total_skips": ratchet}, indent=2) + "\n")
    check("GATE planted · a run that skips more than the record allows may not go green",
          grew is False, f"the ratchet refuses {ratchet + 1} against its own {ratchet}")


# ---------------------------------------------------------------- one immutable base stage
# THE ONE ROW HERE THAT DOES WORK. Every browser suite used to bake the whole site into its own
# temp directory; there are more of those calls than there are suites. The repair is a content-keyed
# cache holding ONE immutable stage per distinct bake request, with every suite handed its own copy.
# Three things have to be true and a sentence can prove none of them: the second identical bake adds
# no stage, the two callers get independent trees, and a caller that writes into its own tree cannot
# reach the cache. So this bakes twice and reads what happened.
import engine_build  # noqa: E402

if not hasattr(engine_build, "stages_built") or not hasattr(engine_build, "BASE_STAGE_CACHE"):
    skip("GATE the full gate bakes one base stage per request, and every suite gets its own copy",
         "tests/engine_build.py exposes no stage cache, so this run cannot say what it bakes")
    skip("GATE a suite writing into its own stage cannot reach the shared one", "same")
else:
    _tmp = Path(tempfile.mkdtemp(prefix="gate_modes_"))
    try:
        a, b = _tmp / "a", _tmp / "b"
        before = engine_build.stages_built()
        engine_build.OUT = a
        engine_build.build("https://synth.example.com")
        after_first = engine_build.stages_built()
        engine_build.OUT = b
        engine_build.build("https://synth.example.com")
        after_second = engine_build.stages_built()

        check("GATE the full gate bakes one base stage per request, and every suite gets its own "
              "copy",
              after_second == after_first and a.exists() and b.exists() and a != b,
              f"the cache held {before} stage(s), the first bake made it {after_first}, and the "
              f"second identical bake added {after_second - after_first} — two callers, two "
              f"independent trees, one stage")

        # THE PLANT. A suite proving a defect writes into the stage it was handed. If that write
        # reached the shared stage, every later suite would stand on a poisoned copy and the gate
        # would report on code nobody wrote. So: plant into one copy, bake a third, and read the
        # third back.
        victim = next(p for p in sorted(a.rglob("*.js")) if p.is_file())
        rel = victim.relative_to(a)
        victim.write_text("/* planted */\n", encoding="utf-8")
        c = _tmp / "c"
        engine_build.OUT = c
        engine_build.build("https://synth.example.com")
        clean = (c / rel).read_text(encoding="utf-8", errors="replace")
        check("GATE a suite writing into its own stage cannot reach the shared one",
              "/* planted */" not in clean and (c / rel).stat().st_size > 32,
              f"a defect planted in one copy's {rel} is absent from a stage baked after it")
    finally:
        shutil.rmtree(_tmp, ignore_errors=True)


# ---------------------------------------------------------------- no product pair table
# HIS STANDING DECISION, held by a check rather than by everyone remembering it: no product pair
# tables and no precomputed transitions. A WorkRecord is per-image and prepared at compile time; the
# composer receives TWO of them at runtime and composes on demand. A table keyed by an ordered pair
# would be the whole architecture inverted, and it is the kind of thing that arrives as a
# well-meaning cache.
#
# WHAT IS READ. Every JSON the engine ships and every asset it serves, for an object whose KEYS are
# ordered pairs of work ids — the shape such a table would have to take. The `pair: {a, b}` field a
# score carries is not that: it is one composed passage saying which two works it was composed FOR,
# which is a passage's provenance and not an index anything is looked up in.
PAIR_KEY = re.compile(r'"\d{6,}(?:__|--|\|)\d{6,}"')
offenders = []
for path in sorted(list((ROOT / "engine").rglob("*.json")) + list((ROOT / "engine").rglob("*.js"))):
    text = path.read_text(encoding="utf-8", errors="replace")
    if PAIR_KEY.search(text):
        offenders.append(str(path.relative_to(ROOT)))
check("GATE nothing the engine ships is keyed by an ordered pair of works",
      not offenders,
      "no precomputed pair table in engine/" if not offenders
      else f"a pair-keyed object stands in {', '.join(offenders)}")

composer = (ROOT / "engine" / "assets" / "pass-composer.js").read_text(encoding="utf-8")
check("GATE the composer still composes on demand from two records handed to it",
      "passageFor" in composer
      and re.search(r"workRecordA[\s\S]{0,400}workRecordB", composer) is not None,
      "passageFor takes the two records, the direction, the seed and the role, and answers")


# ---------------------------------------------------------------- no builder-host clock judges
# S-113'S OWN BAN, kept from creeping back. What was removed then is named here so a reader can see
# what the check actually covers, and so its return is a red rather than an argument.
BANNED = {
    "P95_BAR": "a lab check refusing a run on a frame time read on the builder",
    '"firstCrossing"': "the front door's stopwatch, which measured the builder and not the door",
    "keeps a frame under 33 ms": "a lab driver judging the ladder by this machine's frame time",
    "proves it under load": "a live document ordering a phase proven under load on the builder",
}
back = []
_scan = list((ROOT / "tests").rglob("*.py"))
if (ROOT / "lab").exists():
    _scan += list((ROOT / "lab").rglob("*.py"))
for path in sorted(_scan):
    text = path.read_text(encoding="utf-8", errors="replace")
    for phrase, meaning in BANNED.items():
        if phrase in text and path.name != Path(__file__).name:
            back.append(f"{path.relative_to(ROOT)}: {phrase} — {meaning}")
check("GATE no check judges a run by a clock read on the builder host",
      not back, "none of S-113's removed measurements has come back" if not back
      else "; ".join(back))

# THE SEAM'S OWN CUT, which is what S-113's last red actually was: the interruption rows used to cut
# in after a wall-clock nap on this machine, so a loaded gate could let a short passage end before
# the nap did. The cut is taken inside the browser now, on the passage's own drawn frame.
seam = (HERE / "test_pass_seam.py").read_text(encoding="utf-8")
check("GATE the seam's interruption is cut by the passage's own frame, not by this machine's clock",
      "CUT_WATCH" in seam and "requestAnimationFrame" in seam
      and not re.search(r"^CUT_AT\s*=", seam, re.M),
      "the cut is an in-browser watch on the passage's own door-to-door travel, and the wall-clock "
      "nap it replaced is gone rather than merely unused")


# ---------------------------------------------------------------- the two heavy suites
# THEY MAY NOT SCALE WITH THE COLLECTION. A law proven by sweeping today's photographs is not a law:
# the collection can change under it, and hanging one more photograph makes the proof cost more
# without making it prove more. The law rows stand on a constructed corpus — boundary values of each
# measurement and one representative of each behaviour class — and the real records are kept only for
# a small schema-and-wiring smoke.
SYNTH = HERE / "synthetic_works.py"
if not SYNTH.exists():
    skip("GATE the composer's and the readers' laws stand on a constructed corpus",
         "tests/synthetic_works.py does not stand yet")
    skip("GATE the constructed corpus is not read out of the real collection", "same")
else:
    # THE READING IS BEHAVIOURAL, NOT A GREP. A first pass here searched the module's text for the
    # fixture's name and reddened on the SENTENCE that explains what the corpus replaced — a check
    # that cannot tell prose about a file from a read of it is a check that reds on its own
    # documentation. So the corpus is built with every file-opening door in the process watched, and
    # what is read is what it opened.
    import builtins
    import synthetic_works
    opened = []
    _open, _rt, _rb = builtins.open, Path.read_text, Path.read_bytes

    def _watch(fn, first_is_self):
        def wrapper(*a, **kw):
            opened.append(str(a[0]))
            return fn(*a, **kw)
        return wrapper

    builtins.open = _watch(_open, False)
    Path.read_text, Path.read_bytes = _watch(_rt, True), _watch(_rb, True)
    try:
        corpus = synthetic_works.corpus()
        pairs = synthetic_works.pairs()
    finally:
        builtins.open, Path.read_text, Path.read_bytes = _open, _rt, _rb
    touched = [p for p in opened if "fixture_pass_works" in p]
    check("GATE the constructed corpus is not read out of the real collection",
          not touched,
          f"{len(corpus)} records and {len(pairs)} ordered pair cases were built without the "
          f"collection's own fixture being opened once" if not touched
          else f"the corpus opened {', '.join(sorted(set(touched)))}, so it is the collection "
               f"wearing another name and still grows with it")

    # AND THE SIZE IS A CONSTANT OF THE DESIGN, not of how many photographs are hung. The corpus is
    # one record per boundary and per behaviour class and the pair cases are named contrasts plus a
    # control column against the neutral record, so hanging a photograph changes neither number.
    real = json.loads((HERE / "fixture_pass_works.json").read_text(encoding="utf-8"))
    real_n = len(real.get("works", real))
    check("GATE the corpus does not grow with the collection",
          len(corpus) < real_n and len(pairs) < real_n * (real_n - 1),
          f"{len(corpus)} constructed records against the collection's {real_n}, and "
          f"{len(pairs)} ordered pair cases against the {real_n * (real_n - 1)} the collection "
          f"itself would offer")
    heavy = {n: (HERE / f"test_{n}.py").read_text(encoding="utf-8")
             for n in ("pass_composed", "pass_reads")}
    check("GATE the composer's and the readers' laws stand on a constructed corpus",
          all("synthetic_works" in t for t in heavy.values()),
          "; ".join(f"{n}: {'takes' if 'synthetic_works' in t else 'DOES NOT take'} the constructed "
                    f"corpus" for n, t in heavy.items()))


# ---------------------------------------------------------------- verdict
passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    print(f"{status:5s} {name}   — {detail}")
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
