#!/usr/bin/env python3
"""engine/assemble_client.py — assembles the served client from engine/client/ fragments.

The client (engine/assets/exhibition.js) is one async IIFE with pervasive shared state and
deliberate forward references (declarations are read by handlers that run only after full
evaluation). Reordering declarations is the risk the split must never take, so the fragments
below are raw, unedited LINE SLICES of the file in the order they already appear — no
wrappers, no headers, no per-file changes. Joining them with the empty string reproduces the
served file byte-for-byte; that reproduction (not the names below) is what proves the split
correct — see tests/test_assembly.py.

MANIFEST is an explicit ordered list (never a glob): a fragment is invisible to the build
unless it is named here, so a stray or misordered file in engine/client/ cannot silently
change what gets served.

Usage:
  python engine/assemble_client.py                 # writes engine/assets/exhibition.js
  python engine/assemble_client.py --check         # writes nowhere; exits 1 on any diff
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLIENT_DIR = HERE / "client"
OUT_PATH = HERE / "assets" / "exhibition.js"

# Explicit order. Each name is a raw line-slice of the served file — see docs/design/
# 2026-07-17-client-layer-split.md for the conceptual layer each fragment covers.
MANIFEST = [
    "00-prelude.js",
    "01-knobs-lang-history.js",
    "02-kinship-orderings.js",
    "03-quiz-seed-ab-story.js",
    "04-arrival-facts.js",
    "05-door-deal-circle-walkstate.js",
    "06-ground-load-doorwarm.js",
    "07-door-face-ceremony.js",
    "08-plaque-caption-io.js",
    "09-story-voice.js",
    "10-share-toast.js",
    "11-protect-gift.js",
    "12-zoom-inspect-grab.js",
    "13-quiz-card.js",
    "14-walk-render.js",
    "15-motion.js",
    "16-renderhang-series.js",
    "17-place-hash-boot.js",
    "18-i18n-memory-lang.js",
    "98-sound.js",
    "99-close.js",
]


def assemble():
    parts = []
    for name in MANIFEST:
        path = CLIENT_DIR / name
        parts.append(path.read_text(encoding="utf-8"))
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                     help="don't write; exit 1 if the assembled bytes differ from the committed file")
    args = ap.parse_args()

    assembled = assemble()

    if args.check:
        current = OUT_PATH.read_text(encoding="utf-8") if OUT_PATH.exists() else None
        if assembled != current:
            print("DRIFT: assembling engine/client/ no longer reproduces engine/assets/exhibition.js")
            sys.exit(1)
        print("OK: assembly matches the committed exhibition.js byte-for-byte")
        return

    OUT_PATH.write_text(assembled, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(assembled)} bytes, {len(MANIFEST)} fragments)")


if __name__ == "__main__":
    main()
