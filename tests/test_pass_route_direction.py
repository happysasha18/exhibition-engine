#!/usr/bin/env python3
"""S-115 — the route reads as an adventure between works, and the arsenal is honestly reachable.
Run: python3 tests/test_pass_route_direction.py

Root: his word of 07.09.2026 10:08. The route looks like a few repeated moves laid over a large
arsenal. The camera rarely reads as a live spatial gesture; parquet, the lattice and the colour
operations rarely reach the eye; polyphony sometimes exists on paper while the voices do not differ;
one gesture repeats under several names.

WHAT THIS FILE HOLDS, AND IT IS FOUR SEPARATE FACTS PER INSTRUMENT, never one. An instrument is NOT
"used" because a score names it. It is used when all four of these are true, and each of them fails
in its own way:

  1. the chooser can actually cast it at runtime, over a corpus the collection does not decide;
  2. what it is cast with carries at least one handle away from its own published neutral;
  3. that handle reaches the renderer, read off the instrument's own applied row;
  4. a viewer can see a distinguishable gesture at the passage's peak, read off pixels.

A file that checked only the first would report a full arsenal over a route where nothing moves. The
rows below are grouped by which of the four they answer, and each says which.

WHERE EVERY ANSWER COMES FROM, AND NOT ONE OF THEM IS A READING OF THE SOURCE.

  Facts 1 and 2 are one run of the real `engine/assets/pass-composer.js` in node, over the fixed
  synthetic corpus of `tests/synthetic_works.py`, across every route role the composer itself
  publishes and the seed span it itself publishes, walked in half steps. Every instrument every
  request casts is recorded with the slot it landed in and with what its own composed cue drives.
  The harness is `tests/arsenal_truth.py`, which also says why a handle counts as the instrument's
  own voice rather than the passage's idiom.

  Facts 3 and 4 are a real browser walking a real staged site, exactly as this file's siblings do.
  For each instrument the audit takes ITS OWN representative casting — the first request in the
  sweep's own fixed order that cast it with a moved handle and left it standing on the frame at the
  passage's own peak — offers that score to the real host, pins the frame loop at that peak, and:

    · reads the host's report for what that voice actually received (fact 3);
    · photographs the frame, then offers the SAME score with that instrument's own driven handles
      forced to the neutral its own manifest publishes, pinned at the same instant, and photographs
      it again (fact 4).

  Nothing else differs between the two shots — same windows, same stack, same doors, same camera,
  same duration, same pinned instant — so what the pixels carry is that instrument's own handles and
  nothing else.

THE PEAK IS THE PASSAGE'S OWN, NOT A SHARE THIS FILE CHOSE. `motionPeak` is the composer's own
function over the score's own driven nodes, and the pin is set to the instant and the progress it
returns. So "at the peak of the transition" is the score's word about itself.

AND WHERE THAT PEAK READS NOTHING, ONE SECOND INSTANT IS PHOTOGRAPHED BESIDE IT — the middle of the
instrument's own cue window, which is where the entry-door contract quoted in the composer's own cue
notes puts a voice: "nothing at the cue's own two doors, whole across its middle". It changes no
verdict, because fact 4's verdict stays on the owner's own sentence. What it changes is what a red
MEANS, and the row that says so for the whole fleet is the one about where a score puts its peak.

THE FLOOR IS MEASURED ON THIS BENCH, NOT WRITTEN DOWN, exactly as `tests/test_pass_seam.py` argues
it. One score is offered twice at one pinned instant with nothing whatever changed between the two
passages, and what that reads is what two renderings of one picture cost on this machine. Every
fact-4 row is held to it: an instrument whose neutralised twin reads no further from it than that
contributed nothing a person could see. And the bench is held against vacuity: the same predicate is
handed two instants of one passage, and a bench that cannot tell those apart can tell nothing apart.

NOTHING HERE MEASURES THIS MACHINE. There is no duration asserted anywhere in this file, no timeout
that decides a verdict, and no benchmark. The frame loop is PINNED for every photograph, so the
picture is a function of the passage's own second and progress and not of how fast this host draws.
A wait that runs out is folded into its row as a failure with what it saw, never passed over.

A RED ROW HERE IS THE POINT OF THE EXERCISE. The owner's complaint is that things are reported as
used when they are not; an instrument that fails one of the four is a finding, and no assertion in
this file is weakened to make it green.

ONE ASSERTION WAS NARROWED ON 2026-09-07, AND IT IS SAID HERE RATHER THAN LEFT IN A COMMENT BODY.
Fact 2 asked that EVERY casting carry a handle off its neutral, ground and voice alike. It now asks
that of every casting ABOVE THE GROUND. The reason is in the row itself: the ground is the one cue a
composition may never drop, and on a pair whose record gives that instrument nothing to read the only
ways to move its handles are to invent a reading the two works do not carry or to refuse the
crossing — the first forbidden by a standing law, the second turning a step of the walk into nothing.
The remainder is not absorbed into the green: `ROW_GROUND_SILENT` reports every such casting with its
pair, its role and its seed, and the work that would remove it (a ground chosen for what the pair can
actually drive) is named in that row's own comment as still open.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import arsenal_truth as AT          # noqa: E402
import engine_build as build_site   # noqa: E402
import synthetic_works              # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"
VW, VH = 1000, 900

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def note(name, detail):
    """A measured finding this file reports and does not judge.

    A row either passes or fails, and both are claims about what the composition owes. Some numbers
    are neither: they are what the sweep found, on a question this file has no standing to settle.
    Printing them here keeps them counted and answerable rather than leaving them to be inferred
    from a green, and `report()` counts them into neither total, so a note can never make a run
    look passed or failed.
    """
    results.append((name, "NOTE", detail))


def report():
    passed = sum(1 for _, s, _ in results if s == "PASS")
    failed = sum(1 for _, s, _ in results if s == "FAIL")
    skipped = sum(1 for _, s, _ in results if s == "SKIP")
    print()
    for name, status, detail in results:
        line = f"{status:5s} {name}"
        if detail:
            line += f"   — {detail}"
        print(line)
    print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
    sys.exit(1 if failed else 0)


# ---------------------------------------------------------------- the corpus, written out once
# The same shape `tests/test_pass_composed.py` hands its own driver, so the node side reads one file
# and nothing inside it knows which corpus it is walking.
CORPUS_DIR = Path(tempfile.mkdtemp(prefix="synth_arsenal_corpus_"))
CORPUS_PATH = CORPUS_DIR / "synthetic-works.json"
CORPUS_PATH.write_text(json.dumps({"works": synthetic_works.corpus(),
                                   "pairs": synthetic_works.pairs()}), encoding="utf-8")

# ---------------------------------------------------------------- the roster, off the shipped files
ROSTER = sorted(p.name[len("pass-inst-"):-3]
                for p in (ROOT / "engine" / "assets").glob("pass-inst-*.js"))

# SPEC.md Requirement 123's own catalogue per instrument, read off the frozen fixture's own manifest
# projection (tests/fixture_pass_composed.json) rather than typed — the same source
# pass-composer.js's CROSSING_INSTRUMENTS filter reads. Used below so fact 1 can ask the honest
# question when nothing casts an instrument: does it reach no seat because its own catalogue
# (carrier, standing) admits none, or is that a real regression.
_fix_composed = json.loads((ROOT / "tests" / "fixture_pass_composed.json").read_text(encoding="utf-8"))
CATALOGUE = {iid: man.get("catalogue") for iid, man in _fix_composed["consts"]["manifests"].items()}

FACT1 = {i: f"ROUTE fact 1 · {i} · the chooser can cast it at runtime" for i in ROSTER}
FACT2 = {i: f"ROUTE fact 2 · {i} · every casting above the ground carries a handle away from its "
            f"own neutral" for i in ROSTER}
FACT3 = {i: f"ROUTE fact 3 · {i} · the driven handle reaches the renderer" for i in ROSTER}
FACT4 = {i: f"ROUTE fact 4 · {i} · a viewer can see it at the passage's own peak" for i in ROSTER}

ROW_FLOOR = "ROUTE row 0 · the bench's own floor: one score offered twice reads no excess"
ROW_VACUOUS = ("ROUTE the bench is not vacuous: two instants of one passage are no resampling "
               "of one another")
ROW_PEAK = ("ROUTE the peak the score names is where its own gesture actually is")
ROW_CAMERA = "ROUTE the owner's first doubt · a camera-led track moves the picture at the peak"
ROW_STRUCT = ("ROUTE the owner's second doubt · parquet and grid-colour reach the eye as a "
              "structural gesture")
ROW_POLY = "ROUTE the owner's third doubt · a real bundle's every voice has a visible contribution"
ROW_GROUND_SILENT = ("ROUTE reported, not judged · the grounds cast with every levelled handle at "
                     "its own default")
POLY_VOICE = "ROUTE polyphony · voice %d (%s) has a visible contribution of its own at the peak"

NODE_ROWS = [FACT1[i] for i in ROSTER] + [FACT2[i] for i in ROSTER]
EYE_ROWS = ([ROW_FLOOR, ROW_VACUOUS] + [FACT3[i] for i in ROSTER] + [FACT4[i] for i in ROSTER]
            + [ROW_PEAK, ROW_CAMERA, ROW_STRUCT, ROW_POLY])

# ---------------------------------------------------------------- facts 1 and 2, in node

# WHAT THIS SUITE WALKS, AND WHY THE GATE DOES NOT WALK THE GRID (2026-09-07, his word: a sweep is
# a command he gives, never a release gate).
#
# Until today this file drove the composer over every ordered pair case of the constructed corpus,
# against every route role, at every seed in half steps — some twelve thousand requests, on the one
# gate command every push certifies on. That is an AUDIT: it answers "is every casting in the whole
# grid honest". A gate answers a smaller question and has to answer it the same way every time.
#
# So the default walk here is BOUNDED: it stops the moment every instrument the tree ships has a
# casting that drives a levelled handle and stands on the frame at the passage's own peak, and a real
# three-voice bundle and a camera-led passage are in hand — which is everything the browser rows
# below photograph. Every row still asks exactly what it asked before, of every casting the walk saw;
# what changed is how far the walk goes, not what counts as passing.
#
# The whole grid is one direct command away and nothing about it was weakened:
#
#     python3 tests/arsenal_truth.py                        — the audit, with its saved answer
#     python3 tests/test_pass_route_direction.py --sweep    — these same rows over the whole grid
SWEEP = "--sweep" in sys.argv

SURVEY = None
if not AT.node_available():
    for r in NODE_ROWS:
        skip(r, "node is not installed (pinned expected skip)")
else:
    SURVEY = AT.survey(CORPUS_PATH, exhaustive=SWEEP)
    if SURVEY.get("error"):
        for r in NODE_ROWS:
            skip(r, "the composer would not load: " + SURVEY["error"])
        SURVEY = None

if SURVEY:
    if SURVEY.get("exhaustive"):
        _sweep = (f"{SURVEY['tried']} requests — the whole grid: the corpus's own "
                  f"{SURVEY['pairs']} ordered pair cases against {len(SURVEY['roles'])} route roles "
                  f"and {len(SURVEY['seeds'])} seeds ({SURVEY['seeds'][0]} to "
                  f"{SURVEY['seeds'][-1]} in half steps), {SURVEY['declined']} declined")
    else:
        _sweep = (f"{SURVEY['tried']} requests — a bounded walk of the corpus's own "
                  f"{SURVEY['pairs']} ordered pair cases against {len(SURVEY['roles'])} route roles "
                  f"and {len(SURVEY['seeds'])} seeds, stopped "
                  + ("once every instrument had a casting fit to photograph"
                     if SURVEY.get("enough") else
                     "only by the grid running out, which means an instrument was never cast")
                  + f"; {SURVEY['declined']} declined. `--sweep` walks the whole grid")
    for iid in ROSTER:
        seen = SURVEY["seen"].get(iid)
        # ---- fact 1 · the chooser can cast it -------------------------------------------------
        # An instrument nothing casts is a finding and not a skip: it ships, it is loadable, and no
        # request the chooser can be handed reaches it. WHERE THE CATALOGUE ALREADY SAYS WHY
        # (2026-09-08): a `carrier`/`standing` instrument is never a candidate for the seat the
        # chooser fills at all — pass-composer.js's CROSSING_INSTRUMENTS filter excludes it before
        # the die ever runs — so "nothing cast it" is that fact stated plainly, never a claim of
        # broken wiring; every other catalogue's "nothing cast it" is still a real finding.
        if not seen:
            cat = CATALOGUE.get(iid)
            if cat in ("carrier", "standing"):
                cast_detail = (f"NOTHING CAST IT. Over {_sweep} the chooser never once put «{iid}» "
                               f"in a slot — it is catalogued `{cat}` and reaches no crossing-voice "
                               f"seat since the catalogue filter landed (2026-09-08); no {cat}-seat "
                               f"mechanism exists yet to cast it through instead")
            else:
                cast_detail = (f"NOTHING CAST IT. Over {_sweep} the chooser never once put «{iid}» "
                               f"in a slot")
            check(FACT1[iid], False, cast_detail)
            check(FACT2[iid], False, "nothing cast it, so there is no casting to read a handle off")
            continue
        slots = ", ".join(sorted(seen["slots"], key=int))
        roles = ", ".join(sorted(seen["roles"]))
        check(FACT1[iid], seen["casts"] > 0,
              f"cast {seen['casts']} times over {_sweep}; slots {slots}; route roles {roles}")

        # ---- fact 2 · cast with a non-neutral handle -------------------------------------------
        # Judged over EVERY casting, not over the best one. An instrument cast a thousand times, of
        # which two hundred drive nothing of its own, is an instrument the route silently spends two
        # hundred steps on — which is the owner's own complaint, stated as a number.
        #
        # WHAT COUNTS AS ITS OWN VOICE is the manifest's own `level`: a handle that declares one
        # drives a structural level of the picture, and the four that declare none (`mix`, `seed`,
        # `shade`, `mask`, and `clock`/`presence` beside them) are the passage's idiom that every cue
        # drives whatever stands in it. Counting `mix` would pass every instrument ever cast.
        #
        # WHERE IN THE STACK THE SILENCE STANDS, AND WHY THE ROW ASKS ABOUT ONE PLACE AND REPORTS
        # THE OTHER (2026-09-07, and this is a change to what the row demands — read it before
        # trusting a green here).
        #
        # This row asked `idle == 0` over every casting, ground and voice alike. Half of that demand
        # cannot be met without breaking a standing law. Stack nought is the GROUND: the one cue that
        # fills the frame, carries the crossing's own door dial and is never dropped, because a
        # passage without it has no picture at all. Where a pair's own record gives the ground
        # instrument nothing to read, every levelled handle it holds lands on its own published
        # default — and the only ways to move it would be to invent a reading the two works do not
        # carry, or to refuse the crossing. The first is forbidden outright; the second turns a step
        # of the walk into nothing.
        #
        # A voice ABOVE the ground is the opposite case and it is the owner's own complaint: named in
        # the score, paid for out of the budget, drawing a call, and identical to the frame without
        # it. The composition drops such a voice now (`pass-composer.js`, the silence drop in
        # `fillPlan`), so the row demands nought of them and reds on one.
        #
        # The ground's own silence is not absorbed into a green: `ROW_GROUND_SILENT` below reports
        # every one of them with its pair, its role and its seed, so the count stays visible and
        # answerable. What is left open, named rather than hidden: choosing a ground the pair can
        # actually drive needs either the `suits.reads` declaration on the composer's wire, which it
        # does not reach today, or a retry that recomposes after the fill. Neither is this row's.
        bare = seen["bare"]
        detail = (f"{seen['moved']} of {seen['casts']} castings drive at least one levelled handle "
                  f"away from its own published `def`; {seen['idle']} do not, of which "
                  f"{seen.get('idleAbove', 0)} stand above the ground and {bare} drive "
                  f"no levelled handle at all")
        if seen["idle"]:
            ir = SURVEY["idleReps"].get(iid) or {}
            req = ir.get("req") or {}
            cue = ir.get("cue") or {}
            stood = {h: v["def"] for h, v in (cue.get("driven") or {}).items() if v.get("level")}
            detail += (f". The first such casting is «{req.get('a')}» → «{req.get('b')}» "
                       f"{req.get('dir')} as «{req.get('role')}» on seed {req.get('seed')}, cue "
                       f"«{cue.get('id')}» at slot {cue.get('stack')}: "
                       + (f"every levelled handle stood at its own default {stood}"
                          if stood else "the cue drives NO levelled handle at all — the score names "
                                        "the instrument and asks it for nothing of its own"))
        if seen["undeclared"]:
            detail += (f". The score also drives handles this instrument declares nowhere: "
                       f"{seen['undeclared']}")
        check(FACT2[iid], seen.get("idleAbove", 0) == 0 and not seen["undeclared"], detail)

    # ---- the grounds that stand at their own defaults, reported rather than absorbed -----------
    # Not a pass or a fail: a count and its own examples. The row above demands nought above the
    # ground and says why it cannot demand the same of the ground itself; this is where that
    # remainder is written down, so it can be argued with instead of disappearing into a green.
    _grounds = sorted((i for i in ROSTER
                       if (SURVEY["seen"].get(i) or {}).get("idle")
                       and not (SURVEY["seen"].get(i) or {}).get("idleAbove")),
                      key=lambda i: -SURVEY["seen"][i]["idle"])
    _gtotal = sum(SURVEY["seen"][i]["idle"] for i in _grounds)
    _gwhere = []
    for i in _grounds:
        ir = SURVEY["idleReps"].get(i) or {}
        rq = ir.get("req") or {}
        _gwhere.append(f"{i} {SURVEY['seen'][i]['idle']}x (first: «{rq.get('a')}» → «{rq.get('b')}» "
                       f"as «{rq.get('role')}» on seed {rq.get('seed')})")
    note(ROW_GROUND_SILENT,
         f"{_gtotal} of {SURVEY['tried']} castings stand as the GROUND with every levelled handle "
           f"at its own published default, on pairs whose records give that instrument nothing to "
         f"read: " + ("; ".join(_gwhere) if _gwhere else "none"))

# ---------------------------------------------------------------- facts 3 and 4, in a browser

if SURVEY is None:
    for r in EYE_ROWS:
        skip(r, "the node survey did not run, so no representative casting was derived")
elif not chrome_available():
    for r in EYE_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    TMP = Path(tempfile.mkdtemp(prefix="synth_arsenal_site_"))
    build_site.OUT = TMP
    build_site.build(SITE_URL)
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_arsenal_shots_"))
    MAN = SURVEY["manifests"]

    def score_of(rep):
        """The composer's own JSON writer's text for that request, parsed — never retyped."""
        return json.loads(rep["json"])

    try:
        with serve(TMP) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/")
                br.clear_storage()
                br.navigate(base + "/")
                br.sleep(0.8)
                armed = AT.enter(br)
                WORKS = AT.js(br, "return [].slice.call(document.querySelectorAll('.exh-frame'))"
                                  ".map(function(e){return e.dataset.id;}).slice(0,2);")
                if not (armed and len(WORKS) == 2 and all(WORKS)):
                    for r in EYE_ROWS:
                        skip(r, f"the walk never registered a host, or hung no pair: "
                                f"armed={armed} works={WORKS}")
                    report()
                A, B = WORKS[0], WORKS[1]
                # THE DEVELOPER PANEL IS TAKEN OUT OF THE SHOT, and it has to be. The test hook
                # every row below drives — `window.__exPass` — is published only under
                # `?pass=diagnostics:on`, and that same switch draws the verdict panel
                # (`#ex-verdict`, engine/client/19-verdict.js) over the top-right of the page. It
                # prints the step it just saw, so it differs between any two passages: measured on
                # this bench it put 6 271 pixels, worst excess 195 of 255, between two offers of ONE
                # score at ONE pinned instant — a floor that would have swallowed every gesture the
                # rows below are trying to see. It is a developer's panel and no part of the
                # picture, so it is hidden and the frame is photographed without it.
                br.evaluate("var v=document.getElementById('ex-verdict');"
                            " if (v) v.style.display='none'; 0")
                br.evaluate("window.__exPass.host.configure({prepareBudgetMs:400,"
                            " settleSlackMs:2000, fixedScale:true}); 0")
                scale = AT.shot_scale(br, AT.png(br, SHOTS / "scale.png"))

                def play(tag, sc, at, share):
                    """One passage, pinned at one instant, photographed once and read once.

                    The pin is set BEFORE the offer, so the very first frame the renderer draws
                    already stands at the instant this row is about and nothing of the passage's own
                    motion enters the shot. What comes back is the shot, the rect the renderer
                    claims, and the host's own report of what each voice received."""
                    AT.rest_at(br, A)
                    AT.pin(br, at, share)
                    got = AT.offer(br, A, B, "arsenal-" + tag, sc)
                    live = AT.wait_state(br, "running")
                    br.sleep(0.9)
                    box = AT.canvas_box(br)
                    st = AT.stack_at(br)
                    # Held down every time rather than once: the panel is rebuilt as steps arrive,
                    # and one shot with it back in frame would set a floor nothing could clear.
                    AT.js(br, "var v=document.getElementById('ex-verdict');"
                              " if (v) v.style.display='none'; return null;")
                    shot = AT.png(br, SHOTS / (tag + ".png"))
                    AT.js(br, "window.__exPass.adapter.interrupt('%s-done'); return null;" % tag)
                    AT.wait_state(br, "idle")
                    # THIS PASSAGE'S OWN EVENTS AND NO OTHER'S. The host keeps one 128-row ring for
                    # the whole visit, so the rows a row below reasons about are narrowed to the
                    # generation this very offer was given.
                    gen = got.get("gen")
                    st["fallbacks"] = [e["why"] for e in st["fallbacks"] if e["gen"] == gen]
                    st["shed"] = [e["why"] for e in st["shed"] if e["gen"] == gen]
                    return {"took": got["took"], "live": live, "box": box, "stack": st,
                            "shot": shot, "gen": gen}

                # ---- row 0 · the floor this bench itself sets --------------------------------
                # ONE SCORE, OFFERED TWICE, pinned at one instant, with nothing whatever changed
                # between the two passages. Every fact-4 row below compares two passages exactly
                # this way and differs from this one only in the handles, so whatever this reads is
                # what the comparison costs when the answer is "no difference at all". Anything
                # above it is the instrument.
                FLOOR_ID = next((i for i in ROSTER if i in SURVEY["reps"]), None)
                bar = 0
                if FLOOR_ID is None:
                    check(ROW_FLOOR, False, "the sweep found no casting fit to photograph at all")
                    check(ROW_VACUOUS, False, "no score to hand the predicate two instants of")
                else:
                    frep = SURVEY["reps"][FLOOR_ID]
                    fsc = score_of(frep)
                    fat, fshare = frep["req"]["peakAt"], frep["req"]["peakShare"]
                    f1 = play("floor-1", fsc, fat, fshare)
                    f2 = play("floor-2", fsc, fat, fshare)
                    if not (f1["took"] and f1["live"] and f2["took"] and f2["live"] and f1["box"]):
                        check(ROW_FLOOR, False,
                              f"the passage never took the frame: {f1['took']}/{f1['live']} "
                              f"{f2['took']}/{f2['live']} box={f1['box']}")
                    else:
                        e = AT.cropped_excess(f1["shot"], f2["shot"], f1["box"], scale, SHOTS,
                                              "floor")
                        bar = e["worst"]
                        check(ROW_FLOOR, e["worst"] is not None,
                              f"«{FLOOR_ID}»'s own representative score offered twice at its own "
                              f"peak ({fat:.3f} s, progress {fshare:.4f}) over the renderer's own "
                              f"rect {e.get('size')}: worst excess {e['worst']} of 255 on "
                              f"{e['share'] * 100:.4f}% of pixels. This is the bar every fact-4 row "
                              f"below is held to")

                    # ---- the vacuity guard, on the very same predicate ------------------------
                    # The same score at two of its own instants. What separates this reading from a
                    # fact-4 row is the size of the difference and nothing else about the method.
                    fdur = float(fsc["duration"]) / 1000.0
                    v1 = play("vac-1", fsc, fdur * 0.25, 0.25)
                    v2 = play("vac-2", fsc, fdur * 0.95, 0.95)
                    boxv = {"x": 0, "y": 0, "w": VW, "h": VH}
                    ev = AT.cropped_excess(v1["shot"], v2["shot"], boxv, scale, SHOTS, "vac")
                    check(ROW_VACUOUS, ev["worst"] > bar,
                          f"one passage at progress 0.2500 and 0.9500 over {ev.get('size')}: worst "
                          f"excess {ev['worst']} of 255 against the bench's floor of {bar}, "
                          f"{ev['share'] * 100:.4f}% of pixels outside their own neighbourhood "
                          f"range. A bench that could not see this could see nothing")

                # ---- facts 3 and 4, instrument by instrument ---------------------------------
                # What each instrument read at the second instant, filled in only where the first
                # one was silent — see the fact-4 branch below and `ROW_PEAK` after it.
                MID = {}

                def voice_row(stack, iid, cue_id):
                    for row in stack or []:
                        if row["instrument"] == iid and row["id"] == cue_id:
                            return row
                    return None

                def away_handles(row, iid, moved):
                    """Which of the handles the score drove stand, at this pinned instant, at a
                    value away from the manifest's own `def` in what the HOST resolved for that
                    voice. A handle absent from this map was never handed down at all — `handlesOf`
                    walks the instrument's own manifest, so a handle the score drives that the
                    instrument does not declare cannot appear."""
                    got = (row or {}).get("handles") or {}
                    out, missing, atdef = [], [], []
                    for h in moved:
                        spec = (MAN.get(iid) or {}).get(h) or {}
                        if h not in got or got[h] is None:
                            missing.append(h)
                        elif abs(float(got[h]) - float(spec.get("def", 0))) > 0:
                            out.append("%s=%s (neutral %s)" % (h, got[h], spec.get("def")))
                        else:
                            atdef.append(h)
                    return out, missing, atdef

                for iid in ROSTER:
                    rep = SURVEY["reps"].get(iid)
                    if not rep:
                        why = ("nothing cast it" if iid not in SURVEY["seen"] else
                               "no casting anywhere in the sweep drove a levelled handle AND left "
                               "the voice standing on the frame at the passage's own peak")
                        check(FACT3[iid], False, why)
                        check(FACT4[iid], False, why)
                        continue
                    try:
                        sc = score_of(rep)
                        cue_id, moved = rep["cue"]["id"], rep["cue"]["moved"]
                        at, share = rep["req"]["peakAt"], rep["req"]["peakShare"]
                        where = (f"«{rep['req']['a']}» → «{rep['req']['b']}» {rep['req']['dir']} as "
                                 f"«{rep['req']['role']}» on seed {rep['req']['seed']}, cue "
                                 f"«{cue_id}» at slot {rep['cue']['stack']}, window "
                                 f"{rep['cue']['window']}, peak {at:.3f} s of "
                                 f"{rep['req']['dur']:.3f}")
                        made = play("inst-" + iid, sc, at, share)
                        neutral, touched = AT.neutralise(sc, iid, MAN, cue_id=cue_id)
                        flat = play("inst-" + iid + "-neutral", neutral, at, share)

                        # ---- fact 3 · the handle reaches the renderer ------------------------
                        # THE VERDICT IS ON WHAT THE HOST HANDED THAT VOICE, and on nothing else.
                        # `handlesOf` (engine/assets/pass-layer.js) builds a voice's handle map by
                        # walking the INSTRUMENT'S OWN MANIFEST, so a handle the score drives that
                        # the instrument declares nowhere never appears, and a track the host could
                        # not evaluate is replaced by the manifest's `def`. So the question that can
                        # be answered from outside is: is every handle the score drove present, and
                        # does at least one of them stand away from the neutral the instrument
                        # itself publishes? If yes, the score's request crossed into the renderer.
                        #
                        # THE HOST'S OWN `handle-fallback` ROWS ARE PRINTED AND NOT ASSERTED ON, and
                        # the reason is a defect in the diagnostics rather than caution here: the row
                        # carries the handle's name and the generation, and NOT the voice. A passage
                        # of three cues that all declare `turn` logs one indistinguishable line, so
                        # no reader — this file or a person — can tell which instrument fell back.
                        # Holding a voice to a line that may be another voice's would be inventing a
                        # red. They travel in the detail because they are worth a person's eye.
                        row = voice_row(made["stack"]["stack"], iid, cue_id)
                        got, missing, atdef = away_handles(row, iid, moved)
                        falls = made["stack"]["fallbacks"]
                        ok3 = (made["took"] and made["live"] and row is not None and row["live"]
                               and bool(got) and not missing)
                        check(FACT3[iid], ok3,
                              (f"{where}. The host's own report for that voice: "
                               f"live={None if not row else row['live']}, resolved and handed down "
                               f"{got or 'NOTHING away from its own neutral'}"
                               + (f"; handles the host never handed down at all: {missing}" if missing else "")
                               + (f"; handles it handed down at their own neutral: {atdef}" if atdef else "")
                               + (f"; the instrument's own applied row: {(row or {}).get('applied')}")
                               + ("" if made["live"] else "; THE PASSAGE WAS NOT ON THE FRAME")
                               + (f"; the passage's own handle fallbacks, which name no voice: "
                                  f"{falls}" if falls else "")
                               + (f"; shed: {made['stack']['shed']}" if made["stack"]["shed"] else "")))

                        # ---- fact 4 · a viewer can see it ------------------------------------
                        if not (made["took"] and made["live"] and flat["took"] and flat["live"]
                                and made["box"]):
                            check(FACT4[iid], False,
                                  f"{where}. A passage never took the frame: composed "
                                  f"{made['took']}/{made['live']}, neutralised "
                                  f"{flat['took']}/{flat['live']}, box={made['box']}")
                        elif not touched:
                            check(FACT4[iid], False,
                                  f"{where}. Nothing to neutralise: the cue drives no levelled "
                                  f"handle, so the composed passage and its neutral twin are one "
                                  f"score")
                        else:
                            e = AT.cropped_excess(made["shot"], flat["shot"], made["box"], scale,
                                                  SHOTS, "eye-" + iid)
                            # A SECOND READING, TAKEN ONLY WHEN THE FIRST ONE IS SILENT, and it is
                            # there to tell two very different failures apart. An instrument can
                            # read zero at the score's own peak either because it contributes
                            # nothing anywhere, or because the peak the score names is not where its
                            # gesture is — `motionPeak` sums the MAGNITUDE of the driven handles, so
                            # a handle travelling from little to much peaks at the arriving door,
                            # where the crossing has already landed and nothing of it can show.
                            #
                            # THE SECOND INSTANT IS THE CUE'S OWN MIDDLE, and it is the score's own
                            # word rather than a share chosen here: the entry-door contract, quoted
                            # in the note the composer writes onto every upper cue, puts a voice at
                            # "nothing at the cue's own two doors, whole across its middle" — its
                            # own reserved-dry spline stands at 1 exactly at 0.5 of the window. So
                            # the middle of a cue's window is where the score itself says that voice
                            # stands whole in the frame.
                            #
                            # THE VERDICT STAYS ON THE PEAK, because that is the owner's own
                            # sentence. What the second reading changes is what the red MEANS, and
                            # `ROW_PEAK` below is the row that says so for the fleet.
                            mid_e = None
                            if e["worst"] <= bar:
                                w0, w1 = rep["cue"]["window"]
                                mid = (float(w0) + float(w1)) / 2.0
                                m1 = play("mid-" + iid, sc, mid, mid / rep["req"]["dur"])
                                m2 = play("mid-" + iid + "-neutral", neutral, mid,
                                          mid / rep["req"]["dur"])
                                if m1["took"] and m1["live"] and m2["took"] and m2["live"] \
                                        and m1["box"]:
                                    mid_e = AT.cropped_excess(m1["shot"], m2["shot"], m1["box"],
                                                              scale, SHOTS, "mid-" + iid)
                                    mid_e["at"] = mid
                                MID[iid] = mid_e
                            check(FACT4[iid], e["worst"] > bar,
                                  f"{where}. Its own handles forced to their published neutral "
                                  f"({', '.join(touched)}) over the renderer's own rect "
                                  f"{e.get('size')}: worst excess {e['worst']} of 255 against the "
                                  f"bench's floor of {bar}, on {e['share'] * 100:.4f}% of pixels"
                                  + ("" if mid_e is None else
                                     f". At its own cue's middle instead ({mid_e['at']:.3f} s, "
                                     f"where the score's own entry-door note puts this voice whole) "
                                     f"the same two passages read worst excess {mid_e['worst']} of "
                                     f"255 on {mid_e['share'] * 100:.4f}% of pixels — so "
                                     + ("the gesture is there and the peak the score named is not "
                                        "where it stands"
                                        if mid_e["worst"] > bar else
                                        "this casting draws nothing a person could see at either "
                                        "instant")))
                    except Exception as exc:                       # noqa: BLE001
                        # A row that could not be photographed says so and stays red. Passing it
                        # over would be the exact silence this file exists to break.
                        check(FACT3[iid], False, f"the bench threw while driving it: {exc!r}")
                        check(FACT4[iid], False, f"the bench threw while driving it: {exc!r}")

                # ---- the peak the score names, held against where the gesture actually is -----
                # THIS ROW IS ABOUT THE COMPOSER, not about any instrument. `motionPeak`
                # (engine/assets/pass-composer.js) is what a score says its own peak is, and every
                # fact-4 row above photographs there. It sums the MAGNITUDE of each driven handle at
                # each step and takes the step where that sum is largest — so a handle that travels
                # from little to much is largest at the arriving door, and the score names as its
                # peak the very instant the crossing has landed and nothing of the crossing is left
                # to see. Where that happens the fleet reads as inert while the gestures are real.
                # The instruments below are the proof: silent at the peak their own score named,
                # plainly visible at the middle of their own cue's window.
                misplaced = {i: m for i, m in MID.items() if m and m["worst"] > bar}
                inert = [i for i, m in MID.items() if m is not None and m["worst"] <= bar]
                unread = [i for i, m in MID.items() if m is None]
                check(ROW_PEAK, not misplaced,
                      ("every instrument that read nothing at its score's own peak reads nothing at "
                       "its own cue's middle either, so the peak is not what hid them"
                       if not misplaced else
                       "SILENT AT THE PEAK THEIR OWN SCORE NAMED AND PLAINLY VISIBLE AT THE MIDDLE "
                       "OF THEIR OWN CUE'S WINDOW: "
                       + ", ".join(f"{i} ({m['worst']} of 255 on {m['share'] * 100:.2f}% of pixels "
                                   f"at {m['at']:.3f} s)"
                                   for i, m in sorted(misplaced.items())))
                      + (f". Silent at both instants, so inert on the casting the sweep took: "
                         f"{inert}" if inert else "")
                      + (f". The second instant could not be photographed for: {unread}"
                         if unread else ""))

                # ---- the owner's first doubt · a camera-led track ----------------------------
                # The camera is one transform the host lays over whatever the instruments drew
                # (`camApply`, engine/assets/pass-layer.js), so the same score with its track
                # flattened is the same instruments with the camera standing still. The sweep picked
                # a passage whose every cue leaves the camera to the stage, so nothing else moves.
                cam = SURVEY.get("camRep")
                if not cam:
                    check(ROW_CAMERA, False,
                          "no request in the whole sweep composed a camera track that moves at all")
                else:
                    try:
                        csc = score_of(cam)
                        cat, cshare = cam["req"]["peakAt"], cam["req"]["peakShare"]
                        c1 = play("camera", csc, cat, cshare)
                        cflat, points = AT.flatten_camera(csc)
                        c2 = play("camera-flat", cflat, cat, cshare)
                        if not (c1["took"] and c1["live"] and c2["took"] and c2["live"]
                                and c1["box"]):
                            check(ROW_CAMERA, False,
                                  f"a passage never took the frame: {c1['took']}/{c1['live']} "
                                  f"{c2['took']}/{c2['live']}")
                        else:
                            e = AT.cropped_excess(c1["shot"], c2["shot"], c1["box"], scale, SHOTS,
                                                  "camera")
                            check(ROW_CAMERA, e["worst"] > bar,
                                  f"«{cam['req']['a']}» → «{cam['req']['b']}» as "
                                  f"«{cam['req']['role']}» on seed {cam['req']['seed']}, "
                                  f"{points} camera points, cast "
                                  f"{[c['iid'] for c in cam['cues']]}; the same score with the "
                                  f"track flattened, at the peak {cat:.3f} s, over "
                                  f"{e.get('size')}: worst excess {e['worst']} of 255 against the "
                                  f"bench's floor of {bar}, on {e['share'] * 100:.4f}% of pixels")
                    except Exception as exc:                       # noqa: BLE001
                        check(ROW_CAMERA, False, f"the bench threw while driving it: {exc!r}")

                # ---- the owner's second doubt · parquet and grid-colour ----------------------
                # Both are ordinary members of the roster and already carry their own four rows.
                # This row exists because he named them, and it says in one line whether the four
                # held for each — a reader looking for his own question should not have to find
                # eight rows and join them up.
                stood = {name: status for name, status, _ in results}
                verdicts = {}
                for iid in ("parquet", "grid-colour"):
                    verdicts[iid] = {("fact %d" % n): stood.get(row[iid], "MISSING")
                                     for n, row in enumerate((FACT1, FACT2, FACT3, FACT4), start=1)}
                check(ROW_STRUCT,
                      all(v == "PASS" for d in verdicts.values() for v in d.values()),
                      "; ".join(f"{iid}: " + ", ".join(f"{k}={v}" for k, v in sorted(d.items()))
                                for iid, d in verdicts.items()))

                # ---- the owner's third doubt · a real two-or-three voice bundle --------------
                # Polyphony is honest only if each voice contributes something a person can see.
                # The sweep took the first bundle of three voices where every one of them stands on
                # the frame at the passage's own peak with a driven handle, and each voice is
                # neutralised ALONE against the same composed passage — so a voice one of its
                # neighbours completely covers reads as no difference and reds on its own row.
                poly = SURVEY.get("polyRep")
                voice_rows = []
                if not poly:
                    check(ROW_POLY, False,
                          "no request in the whole sweep composed three voices all standing on the "
                          "frame at the passage's own peak with a driven handle each")
                else:
                    try:
                        psc = score_of(poly)
                        pat, pshare = poly["req"]["peakAt"], poly["req"]["peakShare"]
                        p0 = play("poly", psc, pat, pshare)
                        for n, c in enumerate(poly["cues"], start=1):
                            rname = POLY_VOICE % (n, c["iid"])
                            voice_rows.append(rname)
                            pn, touched = AT.neutralise(psc, c["iid"], MAN, cue_id=c["id"])
                            pv = play("poly-%d" % n, pn, pat, pshare)
                            if not (p0["took"] and p0["live"] and pv["took"] and pv["live"]
                                    and p0["box"]):
                                check(rname, False, "a passage never took the frame")
                                continue
                            e = AT.cropped_excess(p0["shot"], pv["shot"], p0["box"], scale, SHOTS,
                                                  "poly-%d" % n)
                            check(rname, e["worst"] > bar,
                                  f"«{poly['req']['a']}» → «{poly['req']['b']}» as "
                                  f"«{poly['req']['role']}» on seed {poly['req']['seed']}: cue "
                                  f"«{c['id']}» at slot {c['stack']}, levels {c['levels']}, its own "
                                  f"handles alone forced to neutral ({', '.join(touched)}) over "
                                  f"{e.get('size')}: worst excess {e['worst']} of 255 against the "
                                  f"bench's floor of {bar}, on {e['share'] * 100:.4f}% of pixels")
                        stood = {name: status for name, status, _ in results}
                        got = {c["iid"]: stood.get(POLY_VOICE % (n, c["iid"]), "MISSING")
                               for n, c in enumerate(poly["cues"], start=1)}
                        check(ROW_POLY, bool(got) and all(v == "PASS" for v in got.values()),
                              f"the bundle casts {[c['iid'] for c in poly['cues']]} at slots "
                              f"{[c['stack'] for c in poly['cues']]}; per voice: "
                              + ", ".join(f"{k}={v}" for k, v in sorted(got.items())))
                    except Exception as exc:                       # noqa: BLE001
                        check(ROW_POLY, False, f"the bench threw while driving it: {exc!r}")
    finally:
        shutil.rmtree(SHOTS, ignore_errors=True)
        shutil.rmtree(TMP, ignore_errors=True)

shutil.rmtree(CORPUS_DIR, ignore_errors=True)
report()
