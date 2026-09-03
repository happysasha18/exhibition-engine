#!/usr/bin/env python3
"""build_pass_fixture_consts — the collection constants of the two pass fixtures, rebuilt from the
instrument files this tree ships rather than hand-written beside them.

WHY THIS FILE EXISTS. `tests/fixture_pass_works.json` and `tests/fixture_pass_composed.json` each
carry a `consts` block, and the half of that block that describes the cast — `instruments` and
`manifests` — is a CAPTURE of what the site's staging step harvests out of
`engine/assets/pass-inst-<name>.js`. A capture goes stale the moment an instrument lands, and both
fixtures had: the works fixture froze sixteen instruments and the composed fixture twenty-two while
the tree ships twenty-seven. Nothing in the tree held them in step, so this file is the thing that
does. It does not restate a single manifest fact; it calls the site's own reader and writes what
that reader answers.

THE READER IS THE SITE'S, NOT A SECOND ONE. `lab/work-readings-v1.py` in the tlvphotos tree is the
step that harvests the manifests, and its module level does the whole harvest on import —
`discover_instrument_ids()`, `read_manifests()`, the cut table, the published fences. This file
imports it with `EXHIBITION_ENGINE_ROOT` pinned at THIS engine tree and takes `INSTRUMENTS` and
`MANIFESTS` off it verbatim. Where the site's reader and this file disagree about a bound, the
site's reader wins, because it is the one the shipped composer is built against.

THE HANDLE RECORD IS THE READER'S, WHOLE, AND NOTHING HERE PATCHES IT. This file briefly read
`level:` back off each instrument source itself, because the reader stopped at seven fields per
handle and dropped it. That compensation is gone: the reader now publishes eleven — min, max, def,
open, banding, rungs, applied, level, kind, step, names — and a copy kept here would be a second
home for a fact that has one, which is the defect this whole file exists to close rather than to
repeat. What the reader answers is what the fixture carries.

The only thing asked of the record here is that it be WHOLE. Every handle must carry all eleven
keys, holding null where the instrument declares nothing, because a handle that declares no
positions and a handle nobody read are different things and a missing key cannot tell them apart. A
gap is named and refuses the write rather than being filled in.

WHAT IS AND IS NOT REWRITTEN. Three things are replaced: `consts.instruments`, `consts.manifests`
and `works` — the cast and the per-work records, which are the two halves the composer is driven by
and which went stale together. Each fixture keeps exactly the work ids it already keeps; widening
that set is a decision about what a fixture is FOR and is not this file's. The `source` sentence is
rewritten to say what this file did, because a provenance line kept by hand beside a rebuild done by
script is one more copy that goes stale. Everything else stands as captured: the floors, thresholds,
ready floor, fences, the reading sentence, the pair, the two dice, and `expected`/`expectedTight` —
the record of the stage-0 landing, which no row reads and which re-basing would turn from a record
of where the road was into a claim about where it is. Run with `--check` to compare without writing.

WHAT THE EXIT CODE MEANS, because a gate calls this: 0 the fixture matches the site, 1 it has
drifted, 3 the site's staging step could not be reached, 4 the handle record came back incomplete or
a fixture holds a work the site no longer publishes, 5 the harvest is reading a published field as
absent. Only 1 means «rebuild me»; 3 and 5 are faults upstream of this tree and nothing is written
under either.

Run:
  python3 tests/build_pass_fixture_consts.py            # rewrite both fixtures
  python3 tests/build_pass_fixture_consts.py --check    # say what would move, write nothing
"""

import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = (ROOT / "tests" / "fixture_pass_works.json",
            ROOT / "tests" / "fixture_pass_composed.json")

# THE SITE'S STAGING STEP. Its home is the tlvphotos tree beside this one; a checkout that stands
# elsewhere names it with PASS_FIXTURE_READER. Nothing is written there — this file only imports it.
DEFAULT_READER = Path.home() / "tlvphotos-site" / "lab" / "work-readings-v1.py"

# THE PER-WORK RECORDS, WHICH ARE THE OTHER HALF OF THIS FIXTURE AND WENT STALE THE SAME WAY.
#
# The cast says what the instruments can do; these say what each picture is, and the composer reads
# both. This file rebuilt only the cast at first, and the split cost exactly what a half-rebuild
# always costs: a repair went to read `structure.regions.line`, found it in no record, and could not
# tell a field the site had never published from a field the fixture had simply not been refreshed
# for. One capture, both halves, one command.
#
# The records are taken from the staging step's own OUTPUT rather than recomputed here. The reader
# imported above answers for the manifests because it reads the engine tree this fixture describes;
# the records are reductions over the pictures themselves, which live in the site's tree and are not
# this tree's to recompute. Copying the file the site already wrote is the same discipline by the
# other road: one home for the fact, and this end reads it.
DEFAULT_RECORDS = (Path.home() / "tlvphotos-site" / "lab" / "data" / "jscomposer"
                   / "work-records.json")


class ReaderUnreachable(Exception):
    """The site's staging step could not be reached, so this run answered nothing.

    Kept apart from a drift verdict on purpose. A caller that treats "the fixture is stale" and "I
    could not find out" as one answer either refuses runs it should allow or allows runs it should
    refuse, and the exit codes below keep the two apart: 0 the cast matches, 1 the cast has drifted,
    3 no answer was reached.
    """


def load_reader():
    """The site's own manifest harvest, run against THIS engine tree."""
    path = Path(os.environ.get("PASS_FIXTURE_READER") or DEFAULT_READER)
    if not path.exists():
        raise ReaderUnreachable(
            "the site's staging step is not at %s. It is the one home for what a manifest says, "
            "and this file reads rather than restates it. Name it with PASS_FIXTURE_READER."
            % path)
    # The reader refuses to choose between engine trees that publish different manifests, so the
    # tree is named: the fixture describes THIS tree's cast and no other.
    os.environ["EXHIBITION_ENGINE_ROOT"] = str(ROOT)
    spec = importlib.util.spec_from_file_location("pass_fixture_reader", str(path))
    module = importlib.util.module_from_spec(spec)
    cwd = os.getcwd()
    try:
        os.chdir(str(path.parent.parent))
        spec.loader.exec_module(module)
    finally:
        os.chdir(cwd)
    return module, path


# EVERY KEY A HANDLE RECORD CARRIES. Not a schema this file imposes — a roll call of what the site's
# reader publishes, so that a field the reader GAINS is noticed here instead of travelling unread,
# and a field it silently stops publishing refuses the write instead of leaving a hole the shape of
# a declaration. `applied`, then `level`, then `kind`/`step`/`names` all reached the wire late and
# each was invisible until something asked for it by name. This is that something.
HANDLE_KEYS = ("min", "max", "def", "open", "banding", "rungs", "applied",
               "level", "kind", "step", "names")


def _without_comments(text):
    """The same JavaScript with its `//` comments removed, quoting respected.

    Used ONLY to ask the reader the same question twice — see `fields_lost_to_comments`. It parses
    nothing and decides nothing.
    """
    out, quote, i = [], None, 0
    while i < len(text):
        c = text[i]
        if quote:
            out.append(c)
            if c == "\\":
                out.append(text[i + 1:i + 2])
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in "\"'":
            quote = c
            out.append(c)
            i += 1
            continue
        if text[i:i + 2] == "//":
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            continue
        out.append(c)
        i += 1
    return "".join(out)


def fields_lost_to_comments(reader):
    """Fields an instrument publishes that the harvest silently reads as absent.

    THE HARVEST'S OWN READER, ASKED THE SAME QUESTION TWICE — once against the file as written, once
    against the same file with its comments removed. Where the two answers differ, the field is
    there and the harvest did not see it. This keeps no parser of its own and states no manifest
    fact: the reader answers both times, and only the DISAGREEMENT is this file's.

    Why it is needed. `_entry_value` cuts a handle's record at top-level commas, and
    `_split_top_level` honours quoting but not `//` comments — so a comma inside a comment splits
    the record there, and every key standing AFTER that comment falls into a fragment with no name
    on it. The handles this bites are the well-documented ones, and the key it takes is whichever
    stands last, which in this fleet is `level` — the field shelf 17's levels law is written on. It
    fails silent and reads exactly like an instrument declaring nothing.

    A DECLARED «NONE» AND AN UNREAD FIELD MUST NOT BE THE SAME ANSWER, which is the rule the harvest
    itself states for these keys. This is the check that the rule held.
    """
    lost = []
    for iid, path in sorted(reader.MANIFEST_SOURCE.items()):
        src = Path(path).read_text(encoding="utf-8")
        at = src.find('id: "%s", api' % iid)
        head = src.find("handles: {", at)
        block = reader._block_at(src, head + len("handles: ") - 1)
        for name, inner in reader._entries(block):
            bare = _without_comments(inner)
            for key in HANDLE_KEYS:
                got = (reader._entry_value(inner, key) or "null").strip()
                published = (reader._entry_value(bare, key) or "null").strip()
                if got != published:
                    lost.append("%s.%s · %s reads as %s and the file publishes %s"
                                % (iid, name, key, got[:40], published[:60]))
    return lost


def build_cast(reader):
    """The two halves of the `consts` block that describe the cast, as the reader answers them."""
    manifests = json.loads(json.dumps(reader.MANIFESTS))
    instruments = json.loads(json.dumps(reader.INSTRUMENTS))
    # `port` and `cutsFrom` are the reader's absolute path into THIS checkout's
    # engine/assets/pass-inst-<id>.js. This tree is routinely worked from sibling worktrees with
    # different directory names, and the absolute path is a fact about where the run happened to
    # sit, not about the instrument — so it is rewritten relative to ROOT before it is frozen or
    # compared. Without this, two checkouts of the identical commit read as a drifted cast.
    root_prefix = str(ROOT) + os.sep
    for entry in instruments.values():
        if isinstance(entry.get("port"), str) and entry["port"].startswith(root_prefix):
            entry["port"] = entry["port"][len(root_prefix):]
        if isinstance(entry.get("cutsFrom"), str):
            entry["cutsFrom"] = entry["cutsFrom"].replace(root_prefix, "")
    gaps, surplus = [], set()
    for iid, entry in sorted(manifests.items()):
        for name, spec in sorted((entry.get("handles") or {}).items()):
            missing = [k for k in HANDLE_KEYS if k not in spec]
            if missing:
                gaps.append("%s.%s has no %s" % (iid, name, ", ".join(missing)))
            surplus |= set(spec) - set(HANDLE_KEYS)
    return instruments, manifests, gaps, sorted(surplus)


def load_records():
    """The site's per-work records, as the staging step last wrote them."""
    path = Path(os.environ.get("PASS_FIXTURE_RECORDS") or DEFAULT_RECORDS)
    if not path.exists():
        raise ReaderUnreachable(
            "the site's per-work records are not at %s. Name them with PASS_FIXTURE_RECORDS."
            % path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    return doc, path


def works_delta(was, now):
    """Which record fields appeared, went, or moved — by field path, never by picture.

    A path is counted once however many records carry it. What this answers is «which READING
    changed», which is a question about the measuring code; how many pictures a reading touches is a
    fact about the collection and is deliberately not what comes back here.
    """
    def paths(o, p=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from paths(v, p + "." + str(k))
        elif isinstance(o, list):
            yield p + "[]"
            for v in o[:1]:
                yield from paths(v, p + "[]")
        else:
            yield p

    def leaves(o, p=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from leaves(v, p + "." + str(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from leaves(v, "%s[%d]" % (p, i))
        else:
            yield p, o

    appeared, went, moved = set(), set(), set()
    for wid in sorted(set(was) & set(now)):
        pa, pb = set(paths(was[wid])), set(paths(now[wid]))
        appeared |= pb - pa
        went |= pa - pb
        la, lb = dict(leaves(was[wid])), dict(leaves(now[wid]))
        for k in set(la) & set(lb):
            if la[k] != lb[k]:
                moved.add(k)
    return sorted(appeared), sorted(went), sorted(moved)


def rewrite(path, instruments, manifests, records, reader_name, records_name, check):
    """Replace the cast AND the per-work records in one fixture, and say how what stood there differs.

    THE COMPARISON IS THE WHOLE CAST, NOT ITS ROLL OF NAMES. This read the two name lists and
    nothing else, and it was wrong in the way this file keeps finding elsewhere: a check whose reach
    is narrower than the thing it certifies. `level`, `kind`, `step` and `names` all reached the
    handle record while the roll of names stood still, so `--check` answered 0 over a fixture whose
    every handle had gone stale. A gate that can only see instruments arriving cannot see the
    manifest beneath them changing, and it is the manifest the composer is driven by.
    """
    raw = path.read_text(encoding="utf-8")
    trailing = "\n" if raw.endswith("\n") else ""
    doc = json.loads(raw)
    before_names = sorted(doc["consts"]["manifests"])
    was = {"instruments": doc["consts"].get("instruments"),
           "manifests": doc["consts"].get("manifests")}
    doc["consts"]["instruments"] = instruments
    doc["consts"]["manifests"] = manifests
    after_names = sorted(manifests)
    added = [i for i in after_names if i not in before_names]
    dropped = [i for i in before_names if i not in after_names]
    # Held instruments whose own record moved — the drift a roll call cannot see.
    reworked = sorted(i for i in after_names if i in before_names
                      and (was["manifests"] or {}).get(i) != manifests[i])
    changed = was != {"instruments": instruments, "manifests": manifests}

    # THE PER-WORK RECORDS. Each fixture keeps the ids it already keeps — the works fixture carries
    # the whole set the site publishes, the composed one carries only its worked pair — so this
    # refreshes what stands there and never widens or narrows which pictures a fixture is about.
    # Widening that set is a decision about what a fixture is FOR, and it is not this file's.
    held = sorted(doc.get("works") or {})
    absent = [wid for wid in held if wid not in records["works"]]
    if absent:
        raise ReaderUnreachable(
            "%s keeps %d work record(s) the site no longer publishes: %s. Refreshing would drop "
            "them silently, so nothing is written." % (path.name, len(absent), ", ".join(absent)))
    old_works = doc.get("works") or {}
    new_works = {wid: records["works"][wid] for wid in held}
    appeared, went, moved = works_delta(old_works, new_works)
    if old_works != new_works:
        changed = True
    doc["works"] = new_works

    # THE PROVENANCE SENTENCE, WRITTEN BY THE THING THAT DOES THE REBUILDING. It said the fixture
    # was captured on 2026-08-17 and that every field not named in a list of patches stood untouched
    # from that capture — true when hand-patching was how this file changed, and false of every
    # record the moment a whole-fixture rebuild existed. A provenance line maintained by hand beside
    # a rebuild done by script is one more copy that goes stale, so it is written here: whatever
    # this file did is what the sentence says.
    doc["source"] = (
        "Rebuilt by tests/build_pass_fixture_consts.py from the site's own staging step — the cast "
        "(consts.instruments and consts.manifests) read from the instrument files this tree ships "
        "through %s, and the per-work records copied from %s. Nothing here is hand-written and "
        "nothing else in this file is rebuilt: %s"
        % (reader_name, records_name,
           ("the collection's floors, thresholds, fences and provenance stand as captured."
            if "expected" not in doc else
            "the pair, the two dice, the collection's floors, thresholds and fences stand as "
            "captured, and `expected`/`expectedTight` remain the record of the stage-0 landing "
            "that no row reads.")))

    body = json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + trailing
    if not check:
        path.write_text(body, encoding="utf-8")
    print("%s — %d instrument(s) before, %d after%s%s%s"
          % (path.name, len(before_names), len(after_names),
             ("; added " + ", ".join(added)) if added else "",
             ("; DROPPED " + ", ".join(dropped)) if dropped else "",
             ("; record moved on %d held instrument(s): %s"
              % (len(reworked), ", ".join(reworked))) if reworked else ""))
    print("%s — %d work record(s) held; %d reading(s) appeared, %d went, %d moved"
          % (path.name, len(held), len(appeared), len(went), len(moved)))
    for label, rows in (("appeared", appeared), ("WENT", went), ("moved", moved)):
        for row in rows:
            print("    %-9s %s" % (label, row))
    return changed


def main(argv):
    check = "--check" in argv
    try:
        reader, reader_path = load_reader()
        records, records_path = load_records()
    except ReaderUnreachable as why:
        print(str(why))
        return 3
    instruments, manifests, gaps, surplus = build_cast(reader)
    print("read %s against %s" % (reader_path, ROOT))
    print("cast: %d instrument(s) — %s" % (len(instruments), ", ".join(sorted(instruments))))
    handles = sum(len(m["handles"]) for m in manifests.values())
    print("handle record: %d handle(s), %d key(s) each — %s"
          % (handles, len(HANDLE_KEYS), ", ".join(HANDLE_KEYS)))
    if reader.UNPLACED_IDS:
        print("instruments the reader found but did not cast: %s"
              % ", ".join(reader.UNPLACED_IDS))
    if surplus:
        # A GAINED FIELD IS NEWS, NOT AN ERROR. It travels into the fixture either way — the record
        # is the reader's, whole — and it is said out loud so it is never carried unnoticed.
        print("the reader now publishes key(s) this file had not seen before, and they travel "
              "into the fixture: %s" % ", ".join(surplus))
    if gaps:
        # A MISSING KEY REFUSES THE WRITE. Half a handle record on the wire reads as a declaration
        # of nothing, and a fixture that says a handle declares nothing when nobody read it is worse
        # than one that admits it could not answer.
        print("the handle record came back incomplete, so nothing is written:")
        for gap in gaps[:12]:
            print("  " + gap)
        if len(gaps) > 12:
            print("  … and %d more" % (len(gaps) - 12))
        return 4
    lost = fields_lost_to_comments(reader)
    if lost:
        # A FIELD THE HARVEST LOSES REFUSES THE WRITE TOO, and for the same reason: what would land
        # in the fixture is not «this instrument declares nothing here», it is «nobody read it», and
        # those two must never arrive as one value. Writing it anyway and printing a warning beside
        # it would put the true state in a note and the false state on the wire — which is the exact
        # shape this file exists to close.
        #
        # The repair belongs in the harvest, not here. A copy kept on this side would be a second
        # home for a fact that has one, and the last such copy is what this file just deleted.
        print("the harvest reads %d field(s) as absent that the instrument publishes, so nothing "
              "is written:" % len(lost))
        for line in lost:
            print("  " + line)
        print("`_split_top_level` in the harvest honours quoting but not `//` comments, so a comma "
              "inside a comment cuts the handle record there and every key after it is lost. "
              "Fixing that one helper fixes all of the above at once.")
        return 5
    print("records: %s — %d work record(s) the site publishes" % (records_path, len(records["works"])))
    drifted = False
    try:
        for path in FIXTURES:
            if rewrite(path, instruments, manifests, records,
                       reader_path.name, records_path.name, check):
                drifted = True
    except ReaderUnreachable as why:
        print(str(why))
        return 4
    # THE EXIT CODE CARRIES THE ANSWER, which is the whole of what makes this callable from a gate.
    # A --check that always exits 0 is a check nothing can act on, and that is the shape this file
    # was written to close rather than to repeat.
    if check and drifted:
        print("the frozen cast has drifted from the fleet. Run this file with no argument to "
              "rebuild both fixtures from the site's own staging step.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
