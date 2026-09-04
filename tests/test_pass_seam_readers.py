#!/usr/bin/env python3
"""PASS-SEAM-READERS (shelf 8/9, the 2026-09-01 repair) — a seam declaration nobody reads is dead
paper, whatever number it carries.

Run: python3 tests/test_pass_seam_readers.py

ROOT. `test_pass_static.py`'s own STATIC row already forces every instrument in the fleet to declare
a `manifest.seams` — a non-empty list naming where it cuts the frame, or an empty list said outright
with the reason (`adrift`, `livemirror`, `pour`, `strata-light`, `strata-scale`). `pass-layer.js`'s
own `seamsOf` reads that declaration off the handles a frame stands at and hands the result to every
voice's `frameState.seams` (`docs design`'s own comment there: «the seam widths §8's `seams` block
asks for, read once here off the handles this frame stands at, so kaleidoscope's crease, planet's
wrap and tunnel's ring-join draw one shared shape apiece instead of the number each used to carry on
its own»). That half of наряд S-?? landed. The other half did not: the declaration only means
anything the moment an instrument's OWN draw code reads `state.seams` back out and shapes its own
blend width by it — and this file's own hunt through every instrument's shipped source finds
`.seams` referenced in exactly seven of the twenty-two that declare a non-empty list
(`gears`, `kaleidoscope`, `matter`, `overlay`, `planet`, `liquid`, `tunnel`). The other fifteen —
`beat`, `boxfold`, `droste`, `gates`, `grid-colour`, `hero`, `lens`, `parquet`, `studio`, `tilt`,
`unfold`, `veil`, `waterline`, `weave`, `wind` — publish a real seam declaration the host faithfully
computes every frame and hands to a draw call that never once looks at it: dead paper, exactly the
finding Phase 8's own brief names.

WHAT THIS ROW DOES, AND WHAT IT DOES NOT. It is a SOURCE-TEXT check, in the same spirit as
`test_pass_static.py`'s own shelf-21 row: an instrument whose manifest names a non-empty `seams`
list must reference `.seams` somewhere in that SAME shipped file, because a declaration read
nowhere in the file that made it computes exactly what no declaration at all would. It does not
judge WHETHER the read is correct, or PIXEL-verify the seam actually narrows or widens on screen —
that is a per-instrument claim (matching `test_pass_veil.py`'s own arithmetic-and-pixel doors rows)
for the fifteen repairs this row now names, and building fifteen real, verified per-instrument
shader consumers is core rendering logic for each instrument's own draw math, outside this phase's
write-set (an enforcer for a promise, per this phase's own title, not the promise's own fulfilment).
This row's own job is narrower and non-negotiable: make the gap impossible to miss again, the way
Phase 7's `test_pass_feel.py` names its own twelve known dead-band instruments rather than leaving
them unnamed. Repairing a name off KNOWN_UNREAD below and this row goes on checking the rest.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INST_DIR = ROOT / "engine" / "assets"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


ROW_KNOWN = "PASS-SEAM-READERS the fifteen known dead-paper declarations are still dead paper " \
            "(tracked, not fixed, in this phase's write-set) — a silent repair or a silent new " \
            "casualty both red here"
ROW_NO_NEW = "PASS-SEAM-READERS no instrument beyond the known fifteen has grown a new " \
             "declared-but-unread seam"

# The fifteen this hunt found on 2026-09-01, each with a non-empty `manifest.seams` and zero
# references to `.seams` anywhere in its own shipped file. Named here exactly as
# `test_pass_feel.py`'s own KNOWN_JERK names its twelve, so a repair (or a regression naming a new
# sixteenth) is a fact this row states rather than a silence nobody notices.
#
# What each of the fifteen would cost to connect is sorted once in
# docs/design/SEAM-DECLARATIONS.md (2026-09-04), so a reader arriving here stops re-deriving it:
# eleven carry a flat constant and wait on the same decision PLAN.md row S-99 holds for three others,
# two are a design question rather than a wiring job, `hero` holds a deliberately wider crease the
# shared clamp would shrink, and `parquet` closes its seam by exact coordinate agreement and has no
# width to receive. That document also records the defect this set cannot see: `seamsOf` keys its
# output by `kind` alone, and the key `ring` carries two incompatible units across the fleet.
KNOWN_UNREAD = {
    "beat", "boxfold", "droste", "gates", "grid-colour", "hero", "lens", "parquet", "studio",
    "tilt", "unfold", "veil", "waterline", "weave", "wind",
}
# The seven that already read their own declaration back — a positive fact, checked the same way,
# so a regression here (one of these losing its own `.seams` reference) reds too.
KNOWN_READ = {"gears", "kaleidoscope", "matter", "overlay", "planet", "liquid", "tunnel"}


def declares_nonempty_seams(text):
    # `seams:` followed, before the next top-level manifest key a real declaration always has one
    # of, by at least one `{` — an empty list (`seams: [],`) never opens a brace before its own
    # closing bracket.
    i = text.find("seams:")
    if i < 0:
        return False
    j = text.find("]", i)
    if j < 0:
        return False
    body = text[i:j]
    return "{" in body


def main():
    if not INST_DIR.exists():
        skip(ROW_KNOWN, "the instrument files are not on this machine")
        skip(ROW_NO_NEW, "the instrument files are not on this machine")
        return

    unread_now, read_now, missing = set(), set(), []
    for f in sorted(INST_DIR.glob("pass-inst-*.js")):
        name = f.stem[len("pass-inst-"):]
        text = f.read_text(encoding="utf-8")
        if not declares_nonempty_seams(text):
            continue
        if ".seams" in text:
            read_now.add(name)
        else:
            unread_now.add(name)

    still_unread = KNOWN_UNREAD & unread_now
    repaired = KNOWN_UNREAD - unread_now  # known names that now DO read .seams (or vanished)
    for n in repaired:
        if n in read_now:
            missing.append(f"«{n}» now reads its own seam declaration — repaired; move it from "
                            f"KNOWN_UNREAD to KNOWN_READ above")
        else:
            missing.append(f"«{n}» no longer declares a non-empty seam at all — check the manifest "
                            f"still asks §8's question")
    check(ROW_KNOWN, still_unread == KNOWN_UNREAD and not missing,
          f"{len(still_unread)} of {len(KNOWN_UNREAD)} known dead-paper declarations still "
          f"unread: {', '.join(sorted(still_unread))}"
          + (f"; {'; '.join(missing)}" if missing else ""))

    unexpected_unread = unread_now - KNOWN_UNREAD
    lost_read = KNOWN_READ - read_now
    check(ROW_NO_NEW, not unexpected_unread and not lost_read,
          ("no instrument beyond the known fifteen declares a non-empty seam its own file never "
           "reads back, and all seven known readers still do"
           if not unexpected_unread and not lost_read else
           (f"newly unread: {', '.join(sorted(unexpected_unread))}. " if unexpected_unread else "")
           + (f"newly lost their own read: {', '.join(sorted(lost_read))}." if lost_read else "")))


main()

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
