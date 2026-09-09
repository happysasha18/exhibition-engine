#!/usr/bin/env python3
"""EX-FAMILIES — the six matter families breathe, each by its own row of the matter table.

SPEC.md Requirement 39 case "the five families" (criteria 1 to 5) names five matters and their
sixth, the multi-exposure; Requirement 37 case "the screenshot law" (criteria 4 and 5) says what a
still of any of them must be. This suite holds those two sentences together on drawn frames: a work
of each family, standing at rest, moves — and the frame it moves to is still publishable as the
work.

WHERE THE NUMBERS COME FROM.

  The families, their instruments, the letter each moves and its ring: engine/assets/matter-response.json,
  the matter table Requirement 37 criterion 11 asks to be the one home. Nothing about a family is
  typed in this file; the rows below read that table and would read six other families the day it
  named six other families.

  R, a letter's full crossing travel. Requirement 37 criterion 1 carries a gap — no measured value
  for R exists — and tests/test_pass_whisper.py's own reading stands here unchanged: R is the
  handle's declared span, `max - min`, off the instrument's own manifest, which is the one place a
  handle's travel is already written down. The whisper band's ceiling is criterion 1's own
  thirty-second of it, and no row here types a fraction of its own.

  The screenshot bar, read for the first time in this tree as criterion 4 states it. Criterion 4
  asks a frame at rest to differ from the canonical work "by under 1 % of frame width in any pixel's
  displacement". tests/test_pass_whisper.py stood a colour distance in for that, because nothing
  here measured a displacement, and named the substitution. This suite measures the displacement:
  every pixel of the breathing frame has to be found somewhere in the canonical work inside 1 % of
  the frame's own width, and what is left over after that search has to stand under the charter's
  own door bar of 6 of 255, read out of the instrument's own file rather than typed. Two numbers,
  each off something already written: criterion 4's own one per cent, and the charter's own bar.

  WHY THE DISPLACEMENT READING IS THE ONE THIS ROW NEEDS, and not a softer bar chosen to pass. Two
  of the six families — the yarn and the corridor — breathe by sliding the picture rather than by
  recolouring it: weave re-tensions its strips, tunnel walks its walls. A colour distance reads a
  one-pixel slide of a detailed photograph as twenty of 255 and calls a lawful whisper a broken
  frame, while criterion 4's own words call it a quarter of a per cent of frame width and lawful.
  The row measures what the criterion measures.

WHAT A FAMILY'S ROW READS, in three parts, all on frames the bench drew.

  Its resting point. The far edge of the plateau its letter opens with: the furthest that letter
  travels from its own door while the frame is still, to the last bit of it, the canonical work.
  Six instruments open with no plateau at all and rest at their door; two carry one the module's own
  response curve puts there (Requirement 34 law 4's dead bands), and a breath inside such a plateau
  is a work that does not move. The run prints what it found.

  It breathes. From that resting point the letter is granted a travel — the furthest it opens while
  the frame still passes criterion 4's reading, bisected on the drawn frame and capped at criterion
  1's own ceiling — and at that travel the frame is not the frame it started from.

  It is not vacuous. The same letter at the middle of its own declared travel fails criterion 4's
  reading, so the bar the family passes is a bar that can be failed.

WHAT THE CRYSTAL CARRIES BESIDES. Requirement 37 criterion 5 was left to this row: for the
self-similar family the comparison runs against the canonical work at the nearest self-similar
level. The level is `droste`'s own published `period`, and how far into the dive a pose stands is
its own published `front`, both out of the instrument's `values()` block. Two rows read it. The
first settles which level a standing work's comparison runs at: the travel the breath is granted
moves the front by less than one whole level, so the nearest level at rest is the work's own door,
and the crystal's screenshot comparison is the same comparison the other five families take. The
second holds the level to the instrument's own arithmetic — the log of its declared fall over the
number of copies standing inside it — so the level the comparison is taken at is a published
quantity rather than a word.

NO CLOCK IS DRIVEN. Every row reads a frame the bench drew at a pose handed in, or a number the
instrument published for that pose. Nothing here times a run, counts frames or measures a speed.

Run: python tests/test_pass_families.py
"""
import base64
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available, wait_for  # noqa: E402

SITE_URL = "https://synth.example.com"
LAB = Path(__import__("os").environ.get("TLVPHOTOS_ROOT", "/Users/sashaabramovich/tlvphotos")) / "lab"
PHOTOS = [LAB / "photos" / "towers.jpg", LAB / "photos" / "glassgrid.jpg"]
TABLE = ROOT / "engine" / "assets" / "matter-response.json"
VW, VH = 390, 844          # the phone frame lab/carrier-check.py measures on

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# `wait_for` used to be a local copy of the same poll loop headless.py now carries once, shared
# across every suite (row S-119, 2026-09-09 — see the long comment on the shared copy for the
# incident). This suite's own measured budget was 40.0s and stays 40.0s here, bound once so every
# bare call below keeps that number without retyping it, and any call that states its own timeout
# keeps overriding it exactly as before.
import functools
wait_for = functools.partial(wait_for, timeout=40.0, step=0.05)


# ---------------------------------------------------------------- the two numbers, off the files
# The charter's own door bar, read out of an instrument's own source rather than typed. Its comment
# states it for exactly this question — how much may stand in the frame at a door and it still BE
# the photograph — and nine instrument files carry the same sentence (S-71, 2026-09-03).
_BAR_SRC = ROOT / "engine" / "assets" / "pass-inst-unfold.js"
_bar = re.search(r"door bar is\s*\n?\s*//\s*(\d+(?:\.\d+)?) of 255",
                 _BAR_SRC.read_text(encoding="utf-8")) if _BAR_SRC.exists() else None
if _bar is None and _BAR_SRC.exists():
    _bar = re.search(r"door bar is (\d+(?:\.\d+)?) of 255",
                     _BAR_SRC.read_text(encoding="utf-8").replace("\n", " ").replace("//", " "))
DOOR_BAR = float(_bar.group(1)) if _bar else None

# Criterion 4's own reach: one per cent of frame width, in whole pixels of this frame.
REACH = int(0.01 * VW)

TABLE_ROWS = None
if TABLE.exists():
    try:
        TABLE_ROWS = json.loads(TABLE.read_text(encoding="utf-8"))
    except ValueError:
        TABLE_ROWS = None

ROWS = [
    "EX-FAMILIES row1 the matter table names one row per family, each carrying its matter, the "
    "instruments that draw it, the letter a work of it moves at rest and its own ring",
    "EX-FAMILIES row2 the table's instruments are instruments this engine ships, each standing in "
    "exactly one family",
]
FAMILY_ROW = ("EX-FAMILIES row{n} Requirement 39 c1 and Requirement 37 c4 — «{matter}»: at its own "
              "resting point the family's letter is granted a travel under criterion 1's ceiling, "
              "the frame moves there, and every pixel of it is found in the canonical work inside "
              "criterion 4's own one per cent of frame width")
VACUOUS_ROW = ("EX-FAMILIES row{n} the bar is not vacuous — «{matter}»: the same letter at the "
               "middle of its own declared travel fails criterion 4's reading")
CRYSTAL_NEAR = ("EX-FAMILIES row{n} Requirement 37 c5 — the crystal's nearest self-similar level at "
                "rest is its own door, because the granted breath advances the dive front by less "
                "than the one level the instrument publishes")
CRYSTAL_LEVEL = ("EX-FAMILIES row{n} Requirement 37 c5 — the level the crystal's comparison runs "
                 "against is the instrument's own arithmetic: one level is the log of its declared "
                 "fall over the number of copies standing in it, and the dive's whole reach is "
                 "several of them")


def all_rows(fams):
    out = list(ROWS)
    n = 3
    for f in fams:
        out.append(FAMILY_ROW.format(n=n, matter=f["matter"]))
        n += 1
    for f in fams:
        out.append(VACUOUS_ROW.format(n=n, matter=f["matter"]))
        n += 1
    out.append(CRYSTAL_NEAR.format(n=n))
    out.append(CRYSTAL_LEVEL.format(n=n + 1))
    return out


_why = None
if not chrome_available():
    _why = "chrome is not available on this machine"
elif TABLE_ROWS is None:
    _why = "the matter table engine/assets/matter-response.json is absent or is not readable JSON"
elif DOOR_BAR is None:
    _why = "the charter's own door bar could not be read out of pass-inst-unfold.js"
elif [p for p in PHOTOS if not p.exists()]:
    _why = "the bench's photographs are absent: " + ", ".join(str(p) for p in PHOTOS if not p.exists())

if _why:
    for r in all_rows((TABLE_ROWS or {}).get("families", []) or [{"matter": "?"}]):
        skip(r, _why)
else:
    FAMS = TABLE_ROWS.get("families") or []
    ROWNAMES = all_rows(FAMS)

    # ---- row 1 and row 2: the table itself, read before a browser is opened --------------------
    shipped = {p.name[len("pass-inst-"):-len(".js")]
               for p in (ROOT / "engine" / "assets").glob("pass-inst-*.js")}
    whole = [f for f in FAMS
             if f.get("matter") and f.get("instruments") and f.get("letter") and f.get("ring")]
    check(ROWNAMES[0],
          len(FAMS) == 6 and len(whole) == 6,
          f"the table names {len(FAMS)} families, {len(whole)} of them carrying a matter, "
          f"instruments, a letter and a ring: "
          + ", ".join(f"{f.get('matter')!r} on {f.get('instruments')!r} by {f.get('letter')!r}"
                      for f in FAMS))
    named = [i for f in FAMS for i in (f.get("instruments") or [])]
    check(ROWNAMES[1],
          bool(named) and len(named) == len(set(named)) and set(named) <= shipped,
          f"the table names {len(named)} instruments across its families, {len(set(named))} of them "
          f"distinct; those this engine does not ship: {sorted(set(named) - shipped)!r}")

    # ---- the bench ------------------------------------------------------------------------------
    build_site.SITE_CONFIG = dict(build_site.SITE_CONFIG)
    build_site.SITE_CONFIG["pass"] = {"visualLayer": "pass", "diagnostics": "on"}
    OUT_TMP = Path(tempfile.mkdtemp(prefix="synth_families_build_"))
    build_site.OUT = OUT_TMP
    build_site.build(SITE_URL)

    BENCH = Path(tempfile.mkdtemp(prefix="synth_families_bench_"))
    shutil.copy2(OUT_TMP / "pass-layer.js", BENCH / "pass-layer.js")
    for _inst in sorted(OUT_TMP.glob("pass-inst-*.js")):
        shutil.copy2(_inst, BENCH / _inst.name)
    shutil.copy2(OUT_TMP / "config.json", BENCH / "config.json")
    (BENCH / "photos").mkdir()
    for _p in PHOTOS:
        shutil.copy2(_p, BENCH / "photos" / _p.name)
    shutil.copy2(ROOT / "tests" / "fixture_pass_families.html", BENCH / "index.html")
    SHOTS = Path(tempfile.mkdtemp(prefix="synth_families_shots_"))

    def mean_of(img):
        from PIL import ImageStat
        return sum(ImageStat.Stat(img).mean) / 3.0

    def flat(a, b):
        """Mean channel distance between two frames, of 255 — the idiom every instrument suite in
        this tree already carries for «is this frame that work»."""
        from PIL import Image, ImageChops
        x = Image.open(a).convert("RGB")
        y = Image.open(b).convert("RGB")
        if x.size != y.size:
            return 255.0
        return mean_of(ImageChops.difference(x, y))

    def displaced(a, b, reach=REACH):
        """Criterion 4's own reading: what is left of frame `b` once every pixel of it is allowed
        to be found in frame `a` within `reach` pixels. The smallest difference any shift inside the
        reach leaves, taken point by point, then averaged. The frame's own border is where the shift
        wraps, so the reading is taken inside it."""
        from PIL import Image, ImageChops
        x = Image.open(a).convert("RGB")
        y = Image.open(b).convert("RGB")
        if x.size != y.size:
            return 255.0
        best = None
        for dx in range(-reach, reach + 1):
            for dy in range(-reach, reach + 1):
                d = ImageChops.difference(y, ImageChops.offset(x, dx, dy))
                best = d if best is None else ImageChops.darker(best, d)
        w, h = x.size
        return mean_of(best.crop((reach, reach, w - reach, h - reach)))

    printed = []
    try:
        with serve(BENCH) as base:
            with Browser(width=VW, height=VH) as br:
                br.navigate(base + "/index.html")
                if not wait_for(br, "String(!!window.__ready)==='true'", timeout=60.0):
                    for r in ROWNAMES[2:]:
                        skip(r, "the families bench never became ready: "
                                + str(br.evaluate("JSON.stringify(window.__errs||[])")))
                else:
                    def png(name):
                        d = br._cmd("Page.captureScreenshot", format="png",
                                    captureBeyondViewport=False)
                        p = SHOTS / name
                        p.write_bytes(base64.b64decode(d["data"]))
                        return p

                    def draw(iid, over, name="frame.png"):
                        br.evaluate("window.__drawAt(%s,%s); 0"
                                    % (json.dumps(iid), json.dumps(over)))
                        br.sleep(0.30)
                        return png(name)

                    def manifest(iid):
                        got = br.evaluate("JSON.stringify(window.__manifest(%s))" % json.dumps(iid))
                        return json.loads(got) if got and got != "null" else None

                    def letter_of(man, letter):
                        """The letter's declared span, its own rest, and which way it travels."""
                        sp = (man.get("handles") or {}).get(letter)
                        if not sp:
                            return None
                        lo, hi = float(sp["min"]), float(sp["max"])
                        rest = float((man.get("neutral") or {}).get(letter, sp.get("def", lo)))
                        sign = 1.0 if abs(hi - rest) >= abs(rest - lo) else -1.0
                        return {"lo": lo, "hi": hi, "rest": rest, "span": hi - lo, "sign": sign}

                    n = 2
                    vacuous = []
                    for fam in FAMS:
                        row = ROWNAMES[n]
                        n += 1
                        iids = fam.get("instruments") or []
                        letter = fam.get("letter")
                        reads = []
                        ok = bool(iids)
                        for iid in iids:
                            man = manifest(iid)
                            L = letter_of(man, letter) if man else None
                            if not L:
                                ok = False
                                reads.append(f"{iid}: the table's letter {letter!r} is no declared "
                                             f"handle of it")
                                continue
                            ceiling = L["span"] / 32.0     # criterion 1's own thirty-second
                            door = draw(iid, {}, f"{iid}-door.png")
                            # the resting point: the far edge of the plateau the letter opens with
                            a, b = 0.0, L["span"]
                            for _ in range(14):
                                mid = (a + b) / 2.0
                                if flat(door, draw(iid, {letter: L["rest"] + L["sign"] * mid})) == 0.0:
                                    a = mid
                                else:
                                    b = mid
                            plateau = a
                            stand = L["rest"] + L["sign"] * plateau
                            # the granted travel: the furthest the letter opens from there while the
                            # frame still passes criterion 4's reading, capped at criterion 1's own
                            # ceiling
                            c, d = 0.0, ceiling
                            for _ in range(10):
                                mid = (c + d) / 2.0
                                if displaced(door, draw(iid, {letter: stand + L["sign"] * mid})) < DOOR_BAR:
                                    c = mid
                                else:
                                    d = mid
                            granted = c
                            at = draw(iid, {letter: stand + L["sign"] * granted}, f"{iid}-breath.png")
                            moved, held = flat(door, at), displaced(door, at)
                            good = granted > 0 and granted <= ceiling and moved > 0 and held < DOOR_BAR
                            ok = ok and good
                            reads.append(f"{iid} on {letter!r}: rests at {stand:.6f} after a plateau "
                                         f"of {plateau:.6f}, granted {granted:.6f} of a ceiling of "
                                         f"{ceiling:.6f}; the frame moves {moved:.3f} of 255 and "
                                         f"stands {held:.3f} inside criterion 4's reach")
                            printed.append((fam["matter"], iid, letter, plateau, granted, ceiling,
                                            moved, held))
                            # the vacuity reading, taken on the same door
                            mid_v = (L["lo"] + L["hi"]) / 2.0
                            far = displaced(door, draw(iid, {letter: mid_v}, f"{iid}-mid.png"))
                            vacuous.append((fam["matter"], iid, mid_v, far))
                        check(row, ok, " · ".join(reads))

                    by_family = {}
                    for matter, iid, mid_v, far in vacuous:
                        by_family.setdefault(matter, []).append((iid, mid_v, far))
                    for fam in FAMS:
                        row = ROWNAMES[n]
                        n += 1
                        got = by_family.get(fam["matter"], [])
                        check(row,
                              bool(got) and all(far >= DOOR_BAR for _, _, far in got),
                              " · ".join(f"{iid} at the middle of its travel ({mid_v:g}) stands "
                                         f"{far:.3f} inside criterion 4's reach, the bar being "
                                         f"{DOOR_BAR}" for iid, mid_v, far in got))

                    # ---- the crystal, Requirement 37 criterion 5 --------------------------------
                    crystal = next((f for f in FAMS if f.get("selfSimilar")), None)

                    def values(iid, over):
                        got = br.evaluate(
                            "JSON.stringify((function(){var b=window.__exPass.bench,"
                            "m=b.manifest(%s),p={};for(var k in m.neutralPose)p[k]=m.neutralPose[k];"
                            "p.aw=1000;p.ah=1000;p.bw=1000;p.bh=1000;var o=%s;for(var k in o)p[k]=o[k];"
                            "return b.values(%s,p);})())"
                            % (json.dumps(iid), json.dumps(over), json.dumps(iid)))
                        return json.loads(got) if got and got != "null" else {}

                    if not crystal:
                        skip(ROWNAMES[n], "no family in the table names a self-similar level")
                        skip(ROWNAMES[n + 1], "no family in the table names a self-similar level")
                    else:
                        iid = crystal["selfSimilar"]["instrument"]
                        level_key = crystal["selfSimilar"]["level"]
                        letter = crystal["letter"]
                        man = manifest(iid)
                        L = letter_of(man, letter)
                        period = values(iid, {}).get(level_key)
                        front0 = values(iid, {}).get("front")
                        gr = next((g for m, i, lt, pl, g, ce, mv, hd in printed if i == iid), None)
                        front_at_breath = values(iid, {letter: L["rest"] + L["sign"] * (gr or 0)}) \
                            .get("front") if L else None
                        travelled = (abs(front0 - front_at_breath)
                                     if front0 is not None and front_at_breath is not None else None)
                        check(ROWNAMES[n],
                              period is not None and travelled is not None and travelled < period,
                              f"{iid} publishes one self-similar level as {period!r}; the granted "
                              f"breath of {gr!r} moves the dive front from {front0!r} to "
                              f"{front_at_breath!r}, a travel of {travelled!r}")
                        n += 1

                        # WHAT ONE LEVEL IS, off the instrument's own arithmetic rather than off a
                        # number written here. The `size` handle publishes the count of copies
                        # standing inside one fall, and its own `applied` block publishes the fall
                        # and the sentence «one period is log(40) over the count». The row multiplies
                        # the two out and holds the published level to it.
                        #
                        # WHAT THIS ROW DOES NOT CLAIM, and why. A stronger form would photograph the
                        # dive one whole level on and read the picture back unchanged. The dive does
                        # not repeat to the pixel and is not built to: the module winds the copies
                        # into a spiral and wanders its centre on three unaligned periods
                        # (Requirement 34 law 1, which this very instrument plays), so a frame one
                        # level in is the same picture at another turn and another centre. The level
                        # is what the comparison is TAKEN AT, and this row proves the level is the
                        # instrument's own declared quantity; the row above proves which level a
                        # standing work's comparison actually runs at, which is what criterion 5 was
                        # left open to settle.
                        size_block = (man.get("handles") or {}).get("size") or {}
                        applied = size_block.get("applied") or {}
                        fall = applied.get("fallOfForty")
                        copies = values(iid, {}).get("copies")
                        import math
                        want = (math.log(fall) / copies) if (fall and copies) else None
                        reach = values(iid, {letter: L["hi"]}).get("front")
                        levels = (abs(reach - front0) / period) if (reach is not None and period) else None
                        check(ROWNAMES[n],
                              want is not None and period is not None
                              and abs(period - want) < 1e-12
                              and levels is not None and levels > 1,
                              f"{iid} stands {copies!r} copies inside a declared fall of {fall!r}, so "
                              f"one level is {want!r} and the instrument publishes {period!r}; the "
                              f"dive's whole reach is {levels!r} such levels")

                    if printed:
                        print("\nthe run's own numbers, on a %d x %d frame:" % (VW, VH))
                        print("  criterion 4's own reach: %d px, one per cent of the frame's width"
                              % REACH)
                        print("  the charter's door bar, read out of pass-inst-unfold.js: %.1f of 255"
                              % DOOR_BAR)
                        for matter, iid, letter, plateau, granted, ceiling, moved, held in printed:
                            print("  %-22s %-13s %-4s plateau %-9.6f granted %-9.6f of %-8.5f  "
                                  "moves %7.3f  holds %6.3f"
                                  % (matter, iid, letter, plateau, granted, ceiling, moved, held))

                    errs = json.loads(br.evaluate("JSON.stringify(window.__errs||[])"))
                    if errs:
                        print("  the bench reported: %r" % (errs,))
    finally:
        shutil.rmtree(OUT_TMP, ignore_errors=True)
        shutil.rmtree(BENCH, ignore_errors=True)
        shutil.rmtree(SHOTS, ignore_errors=True)

# ---------------------------------------------------------------- report
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
