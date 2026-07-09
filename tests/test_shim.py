#!/usr/bin/env python3
"""Shim completeness: every symbol that any test file accesses on the engine_build shim must
actually be present on the shim module (EX-SHIM-COMPLETE).

Uses AST parsing to collect, without executing test code:
  · every attribute name used as `build_site.<name>` or `engine_build.<name>`
  · every name imported with `from engine_build import <name>`

Then asserts getattr(engine_build, symbol) does not raise AttributeError for each collected name.

Run: python tests/test_shim.py  (exit 0 = all green)
"""
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(TESTS_DIR))
import engine_build  # noqa: E402  — the shim under test

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


# ---------------------------------------------------------------- static collection
# Walk every test_*.py (not this file) and collect symbols accessed via build_site.<sym>
# or engine_build.<sym>, plus `from engine_build import <sym>`.

SHIM_ALIASES = {"build_site", "engine_build"}  # names that refer to the shim in tests

def _collect_symbols(src_path: Path) -> set:
    """Return the set of symbol names accessed on the shim in one source file."""
    try:
        tree = ast.parse(src_path.read_text(encoding="utf-8"))
    except SyntaxError:
        return set()

    # Determine local aliases: `import engine_build as X` or `import engine_build`
    local_aliases = set(SHIM_ALIASES)  # start with canonical names

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in SHIM_ALIASES:
                    local_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module in SHIM_ALIASES:
                local_aliases.add(node.module)

    syms = set()
    for node in ast.walk(tree):
        # `build_site.foo` → Attribute(value=Name(id='build_site'), attr='foo')
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id in local_aliases:
                syms.add(node.attr)
        # `from engine_build import foo, bar`
        if isinstance(node, ast.ImportFrom) and node.module in SHIM_ALIASES:
            for alias in node.names:
                syms.add(alias.name)

    return syms


collected: set = set()
test_files = sorted(TESTS_DIR.glob("test_*.py"))
# Exclude this test file itself — it imports engine_build bare, no dot-access of interest
for tf in test_files:
    if tf.name == "test_shim.py":
        continue
    collected |= _collect_symbols(tf)

# "py" appears from lines like `engine_build.py` in comments parsed as code — filter junk
# (a module attribute named "py" never exists on the shim and is not a real usage)
EXCLUDE = {"py"}
collected -= EXCLUDE

# ---------------------------------------------------------------- assertions
for sym in sorted(collected):
    present = hasattr(engine_build, sym)
    check(
        f"EX-SHIM-COMPLETE engine_build.{sym} re-exported",
        present,
        "" if present else f"'{sym}' missing from tests/engine_build.py",
    )

# ---------------------------------------------------------------- gate
fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))

print(f"\nChecked {len(collected)} symbols: {sorted(collected)}")
print(f"\n{len(results)} rows: {len(results) - len(fails)} pass, {len(fails)} fail")
sys.exit(1 if fails else 0)
