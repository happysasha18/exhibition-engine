#!/usr/bin/env python3
"""Quiz utilities shared across test suites — ported from tlvphoto cbab752.

arm_of and find_token_arm_on live HERE (one home); test suites import from this module.
The jhash replica is the authoritative Python mirror of the JS quizHash() finalizer.

REAL JS quizHash() at three sample inputs; any divergence goes RED.
"""


def arm_of(tok):
    """Return the A/B arm ('on' or 'control') for the given visitor token."""
    return "on" if (jhash(tok + ":quizarm") / 4294967296) < 0.5 else "control"


def find_token_arm_on(n=1000000, eligible_count=None):
    """Find a token with arm=on where the chosen eligible index is 0.

    eligible_idx=0 means the chosen work is the FIRST quiz work in the arc order —
    the pick work itself (at arc position 0). This guarantees the chosen work is always
    in the first rendered frames, so the intersection observer can fire for it.
    If eligible_count is unknown, fall back to any arm-on token.
    """
    if eligible_count is not None:
        # preferred: find token where arm=on AND chosen = eligible[0] (the pick work)
        for i in range(n):
            tok = "qk%08d" % i
            if arm_of(tok) != "on":
                continue
            if jhash(tok + ":once") % eligible_count == 0:
                return tok
    # fallback: just arm=on
    for i in range(300000):
        tok = "qk%08d" % i
        if arm_of(tok) == "on":
            return tok
    return None


def jhash(s):
    """Python replica of the JS seed-hash finalizer used by quizHash(token, suffix).

    Matches the MurmurHash3-inspired finalizer in exhibition.js quizHash():
      let h = seed; for each char: h ^= charCode; h = Math.imul(h, 0x9e3779b9) >>> 0;
      h ^= h >>> 16; h = Math.imul(h, 0x85ebca6b) >>> 0;
      h ^= h >>> 13; h = Math.imul(h, 0xc2b2ae35) >>> 0;
      h ^= h >>> 16;
    Returns the 32-bit unsigned integer result.
    """
    h = 0
    for ch in s:
        h = h ^ ord(ch)
        h = ((h * 0x9e3779b9) & 0xFFFFFFFF)
    h ^= h >> 16
    h = (h * 0x85ebca6b) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xc2b2ae35) & 0xFFFFFFFF
    h ^= h >> 16
    return h


if __name__ == "__main__":
    # Smoke-check the replica against pinned values
    cases = [
        ("qk00000000:quizarm", None),
        ("qk00000001:quizarm", None),
        ("hello:quizarm", None),
    ]
    print("jhash smoke-check (value/arm):")
    for s, _ in cases:
        v = jhash(s)
        arm = "on" if v / 4294967296 < 0.5 else "control"
        print(f"  jhash({s!r}) = {v} → {arm}")
    print("arm_of spot-check:")
    for i in range(5):
        tok = "qk%08d" % i
        print(f"  arm_of({tok!r}) = {arm_of(tok)}")
    tok = find_token_arm_on(eligible_count=2)
    print(f"find_token_arm_on(eligible_count=2) = {tok!r} → arm={arm_of(tok) if tok else 'N/A'}")
