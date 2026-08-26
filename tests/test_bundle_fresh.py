#!/usr/bin/env python3
"""EX-BUNDLE-FRESH — the served client never lags its own source fragments.

engine/assets/exhibition.js is the served client bundle, built by concatenating fragments from
engine/client/ via engine/assemble_client.py's assemble() (an explicit MANIFEST, joined in
order). Nothing enforced that the committed exhibition.js actually matched what assemble()
would produce right now — a fragment could change and the served file would silently go
stale until someone remembered to re-run the assembler by hand. That happened for real: a
correct fix in engine/client/01a-pass.js and engine/client/15-motion.js was hand-verified
correct, but the browser kept loading an hours-stale bundle for hours because nobody re-ran
`python engine/assemble_client.py`.

This suite calls assemble() fresh and asserts it is byte-for-byte identical to what is
currently on disk at engine/assets/exhibition.js. RED means the committed bundle has drifted
from its fragments — the fix is `python engine/assemble_client.py`, never a hand-edit of the
served file.

Run: python tests/test_bundle_fresh.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engine"))
from assemble_client import assemble, OUT_PATH  # noqa: E402

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


on_disk = OUT_PATH.read_text(encoding="utf-8")
freshly_assembled = assemble()

match = on_disk == freshly_assembled
detail = ""
if not match:
    detail = (
        f"engine/assets/exhibition.js ({len(on_disk)} bytes) does not match what "
        f"assemble() would produce right now ({len(freshly_assembled)} bytes) — the served "
        f"bundle has drifted from engine/client/ fragments. Fix: "
        f"`python engine/assemble_client.py` to reassemble, then commit the result."
    )
check("EX-BUNDLE-FRESH exhibition.js matches assemble() of its own fragments", match, detail)

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
