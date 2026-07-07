#!/usr/bin/env python3
"""Greeting cache validator/generator stub for exhibition-engine.

In the full instance this script would call an AI API to generate greetings;
here it only validates the fixture's greetings.json (the engine has no API key
and no keychain service — that functionality is instance-side).

Contract (what the test suite asserts):
  --check [--cache FILE]  : validate the cache; exit 0 = valid, 1 = invalid
  --keychain-service NAME : must fail (no keychain in the engine); exit 1,
                            message contains "key"

All other flags are silently accepted (forward-compatibility).
"""
import argparse
import json
import sys
from pathlib import Path

# Default cache: the engine fixture's greetings.json
_DEFAULT_CACHE = (
    Path(__file__).resolve().parent.parent
    / "tests" / "fixture_content" / "data" / "greetings.json"
)

DAYPARTS = ["night", "morning", "day", "evening"]
REQUIRED_LANGS = ["ru", "en", "he", "de", "fr", "es", "uk"]


def validate(cache_path):
    """Validate greetings.json.  Returns (ok: bool, reason: str)."""
    try:
        with open(cache_path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except FileNotFoundError:
        return False, f"cache file not found: {cache_path}"
    except json.JSONDecodeError as exc:
        return False, f"JSON decode error: {exc}"

    if doc.get("fallback") != "en":
        return False, f"fallback must be 'en', got {doc.get('fallback')!r}"

    langs = doc.get("langs") or {}

    for code in REQUIRED_LANGS:
        if code not in langs:
            return False, f"language {code!r} missing from langs"
        L = langs[code]

        if "skip" in L:
            return False, f"lang {code}: 'skip' key present (retired)"
        ask = (L.get("ask") or "").strip()
        if not ask:
            return False, f"lang {code}: ask is empty"

        exit_ = (L.get("exit") or "").strip()
        if not exit_:
            return False, f"lang {code}: exit is empty"

        more = L.get("more") or ""
        if "{n}" not in more:
            return False, f"lang {code}: '{{n}}' missing from 'more'"

        if not (L.get("q_more") or "").strip():
            return False, f"lang {code}: q_more is empty"
        if not (L.get("q_spent") or "").strip():
            return False, f"lang {code}: q_spent is empty"

        greet = L.get("greet") or {}
        for part in DAYPARTS:
            strings = greet.get(part)
            if not strings:
                return False, f"lang {code}: greet.{part} is missing or empty"
            for s in strings:
                if not s.strip():
                    return False, f"lang {code}: greet.{part} contains a blank string"

    return True, "greetings.json is valid"


def main():
    ap = argparse.ArgumentParser(description="Greeting cache validator")
    ap.add_argument("--check", action="store_true",
                    help="validate the cache and exit (0=ok, 1=invalid)")
    ap.add_argument("--cache", type=str, default=str(_DEFAULT_CACHE),
                    help="path to greetings.json (default: fixture)")
    ap.add_argument("--keychain-service", type=str, default=None,
                    help="keychain service name (instance-side only — always fails here)")
    # Accept unknown args for forward-compatibility
    args, _ = ap.parse_known_args()

    if args.keychain_service is not None:
        # The engine has no keychain; this flag always fails with "key" in the message.
        print(
            f"ERROR: no keychain access in the engine (key: {args.keychain_service!r}); "
            "this flag is instance-side only.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.check:
        ok, reason = validate(args.cache)
        if ok:
            print(f"OK — {reason}")
            sys.exit(0)
        else:
            print(f"INVALID — {reason}", file=sys.stderr)
            sys.exit(1)

    # No flags: nothing to do (the generator body is instance-side).
    print("gen_greetings.py: no action (generation is instance-side; use --check to validate).")
    sys.exit(0)


if __name__ == "__main__":
    main()
