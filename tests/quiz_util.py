#!/usr/bin/env python3
"""Quiz utilities shared across test suites — ported from an instance.

find_token_shows and the quiz_chip_copy helpers live HERE (one home); test suites import from
this module. The jhash replica is the authoritative Python mirror of the JS quizHash() finalizer.

The quiz_arm split (on/control, salt "quizarm") RETIRED 2026-07-28 on the owner's word (first said
2026-07-23): traffic is small, no split test is needed, so every visitor with the quiz flag on is
now eligible — arm_of/find_token_arm_on are gone with it (SPEC.md carries the dated tombstone).

REAL JS quizHash() at three sample inputs; any divergence goes RED.
"""


def find_token_shows(n=1000000, eligible_count=None):
    """Find a token where the chosen eligible index is 0 — the pick work at arc position 0.

    Every visitor whose walk has a non-empty eligible set now shows the chip (the quiz_arm split
    that once gated this on an "on" arm is retired), so the only free variable left is which
    eligible work the once-hash lands on. eligible_idx=0 means the chosen work is the FIRST quiz
    work in the arc order — the pick work itself — which guarantees the chosen work is always in
    the first rendered frames, so the intersection observer can fire for it. With no eligible_count
    given, any token shows the chip on a walk with an eligible pick, so a fixed token suffices.
    """
    if eligible_count is not None:
        for i in range(n):
            tok = "qk%08d" % i
            if jhash(tok + ":once") % eligible_count == 0:
                return tok
        return None
    return "qk00000000"


def chip_copy_arm_of(tok):
    """The quiz_chip_copy arm ('place' | 'place_prize') a visitor token deals (salt 'quizcopy').

    Mirrors the client's abArms draw for the quiz_chip_copy experiment (arms ["place","place_prize"],
    equal split in order): arm = arms[floor(u*2)] where u = quizHash(tok+":quizcopy")/2^32.
    """
    return ["place", "place_prize"][0 if jhash(tok + ":quizcopy") / 4294967296 < 0.5 else 1]


def find_token_copy_arm(want_arm, eligible_count=None, n=2000000):
    """Find a token that deals quiz_chip_copy=want_arm.

    When eligible_count is given, also require the chosen quiz work to be eligible[0] (the pick work
    at arc position 0), so scrolling to the pick frame reliably places the chip — the same
    guarantee find_token_shows gives. want_arm is 'place' or 'place_prize'.
    """
    for i in range(n):
        tok = "qc%08d" % i
        if chip_copy_arm_of(tok) != want_arm:
            continue
        if eligible_count is not None and jhash(tok + ":once") % eligible_count != 0:
            continue
        return tok
    return None


def jhash(s):
    """Python mirror of the client's quizHash(str) — exhibition.js, exported as EXQuiz._hash.

    Byte-for-byte the same formula the client draws the A/B arm and the per-work pick from:

        let s = 0;
        for (const c of String(str)) s = (s * 31 + c.charCodeAt(0)) >>> 0;
        s = Math.imul(s ^ (s >>> 16), 0x45d9f3b) >>> 0;
        s = Math.imul(s ^ (s >>> 16), 0x45d9f3b) >>> 0;
        return (s ^ (s >>> 16)) >>> 0;

    `Math.imul(a, b)` is the low 32 bits of the product, so `(a * b) & 0xFFFFFFFF` matches it.
    test_parity.py runs the exported JS hash in node against this over a token spread; any
    divergence goes RED.
    """
    h = 0
    for ch in s:
        h = ((h * 31 + ord(ch)) & 0xFFFFFFFF)
    h = ((h ^ (h >> 16)) * 0x45d9f3b) & 0xFFFFFFFF
    h = ((h ^ (h >> 16)) * 0x45d9f3b) & 0xFFFFFFFF
    h = (h ^ (h >> 16)) & 0xFFFFFFFF
    return h


if __name__ == "__main__":
    # Smoke-check the replica against pinned values
    cases = [
        ("qk00000000:quizcopy", None),
        ("qk00000001:quizcopy", None),
        ("hello:quizcopy", None),
    ]
    print("jhash smoke-check (value/quiz_chip_copy arm):")
    for s, _ in cases:
        v = jhash(s)
        arm = "place" if v / 4294967296 < 0.5 else "place_prize"
        print(f"  jhash({s!r}) = {v} → {arm}")
    print("chip_copy_arm_of spot-check:")
    for i in range(5):
        tok = "qk%08d" % i
        print(f"  chip_copy_arm_of({tok!r}) = {chip_copy_arm_of(tok)}")
    tok = find_token_shows(eligible_count=2)
    print(f"find_token_shows(eligible_count=2) = {tok!r} → chip_copy_arm={chip_copy_arm_of(tok) if tok else 'N/A'}")
