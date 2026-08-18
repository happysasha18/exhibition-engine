#!/usr/bin/env python3
"""engine/assemble_client.py — assembles the served client from engine/client/ fragments.

The client (engine/assets/exhibition.js) is one async IIFE with pervasive shared state and
deliberate forward references (declarations are read by handlers that run only after full
evaluation). Reordering declarations is the risk the split must never take, so the fragments
below are raw, unedited LINE SLICES of the file in the order they already appear — no
wrappers, no headers, no per-file changes. Joining them with the empty string reproduces the
served file byte-for-byte.

MANIFEST is an explicit ordered list (never a glob): a fragment is invisible to the build
unless it is named here, so a stray or misordered file in engine/client/ cannot silently
change what gets served.

Usage:
  python engine/assemble_client.py                 # writes engine/assets/exhibition.js
"""
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
CLIENT_DIR = HERE / "client"
OUT_PATH = HERE / "assets" / "exhibition.js"

# Explicit order. Each name is a raw line-slice of the served file — see docs/design/
# 2026-07-17-client-layer-split.md for the conceptual layer each fragment covers.
MANIFEST = [
    "00-prelude.js",
    "01-knobs-lang-history.js",
    "01a-pass.js",
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
    """One concatenation, in MANIFEST order, each fragment opened by a keep-marker.

    The marker is a `/*! ... */` comment — the convention for a mark that survives minification, and
    the bake's comment strip (build.py: strip_js_comments) keeps exactly that form. It gives every
    fragment a real boundary in the served file. Before it, a test that needed to scope itself to one
    fragment's region hunted for a SENTENCE inside a comment, so rewording a comment silently moved
    the region and stripping the comments erased it entirely.
    """
    parts = []
    for name in MANIFEST:
        path = CLIENT_DIR / name
        parts.append(f"/*!{name}*/\n")
        parts.append(path.read_text(encoding="utf-8"))
    return "".join(parts)


def fragment_slice(js, name):
    """The served region of one fragment, located by its keep-markers. Returns None when the marker
    is absent, so a caller can report a lost region rather than pass on an empty read."""
    start = js.find(f"/*!{name}*/")
    if start < 0:
        return None
    nxt = js.find("/*!", start + 3)
    return js[start:(nxt if nxt >= 0 else len(js))]


def main():
    argparse.ArgumentParser().parse_args()

    assembled = assemble()
    OUT_PATH.write_text(assembled, encoding="utf-8")
    print(f"wrote {OUT_PATH} ({len(assembled)} bytes, {len(MANIFEST)} fragments)")


if __name__ == "__main__":
    main()
