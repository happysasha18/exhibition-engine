"""test_vector.py — invariant checks for fixture vector.json (exhibition-engine adaptation).

The engine has no compute_vector.py (vector computation is instance-side only — gap recorded
below). This suite asserts that the FIXTURE vector.json satisfies the same structural invariants
that the tlvphoto test_vector.py checks.

EXPECTED_N is derived from gallery_data.json at import time so the assertion stays correct
when make_synthetic.py adds works.

Structural gaps (no assertion possible, only fixture):
  - INV-4 radial⟂axial: fixture uses no null radial values (all axes synthetic numeric).
  - INV-10 centre-less→null: fixture has no measured-centre-less images (all axes numeric).
  - SCALAR_NEW_AXES / D_FAMILY: these are instance-specific axis names; fixture has 26 generic axes.
  - No compute_vector.py in the engine: this suite validates the FIXTURE, not computed output.

Run: python tests/test_vector.py
Exits 0 if all pass, 1 if any fail.
"""

import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Locate fixture vector.json
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_FIXTURE = os.path.join(_HERE, "fixture_content")
_VECTOR_PATH = os.path.join(_FIXTURE, "vector.json")

# Work count and axis count are derived from the fixture manifest so the assertion
# automatically stays correct when make_synthetic.py adds more works.
_GALLERY_PATH = os.path.join(_FIXTURE, "gallery", "gallery_data.json")
with open(_GALLERY_PATH) as _fh:
    EXPECTED_N = len(json.load(_fh)["items"])
EXPECTED_AXIS_COUNT = 26


def load_vector():
    with open(_VECTOR_PATH, "r") as fh:
        return json.load(fh)


def _ax_keys(item):
    """Return only the AX- prefixed axis keys for an item."""
    return frozenset(k for k in item["axes"] if k.startswith("AX-"))


# ---------------------------------------------------------------------------
# Test functions — each returns (passed: bool, reason: str)
# ---------------------------------------------------------------------------

def test_inv8_coverage(data):
    """INV-8: EXPECTED_N items; every item has all EXPECTED_AXIS_COUNT AX- axis keys."""
    items = data["items"]

    if len(items) != EXPECTED_N:
        return False, f"item count {len(items)} != {EXPECTED_N}"

    canonical_keys = _ax_keys(items[0])
    if len(canonical_keys) != EXPECTED_AXIS_COUNT:
        return False, (
            f"item[0] has {len(canonical_keys)} AX- keys, expected {EXPECTED_AXIS_COUNT}: "
            f"{sorted(canonical_keys)}"
        )

    missing_report = []
    for item in items:
        item_keys = _ax_keys(item)
        missing = canonical_keys - item_keys
        if missing:
            missing_report.append(f"id={item['id']} missing {sorted(missing)}")
        if len(missing_report) >= 3:
            break

    if missing_report:
        return False, "items missing axis keys: " + " | ".join(missing_report)

    return True, f"all {EXPECTED_N} items present with {EXPECTED_AXIS_COUNT} AX- keys each"


def test_inv9_provenance(data):
    """INV-9: every axis value dict carries both source and confidence."""
    violations = []
    for item in data["items"]:
        for aname, aval in item["axes"].items():
            if not aname.startswith("AX-"):
                continue
            missing_fields = [f for f in ("source", "confidence") if f not in aval]
            if missing_fields:
                violations.append(
                    f"id={item['id']} axis={aname} missing {missing_fields}"
                )
            if len(violations) >= 5:
                break
        if len(violations) >= 5:
            break

    if violations:
        return False, "axes missing provenance: " + " | ".join(violations)
    return True, "all axes carry source and confidence"


def test_inv7_human_wins(data):
    """INV-7: every axis with source=='authored' must have confidence == 1.0.
    (Fixture uses source='synthetic'; this test trivially passes if no authored axes exist.)
    """
    violations = []
    for item in data["items"]:
        for aname, aval in item["axes"].items():
            if not aname.startswith("AX-"):
                continue
            if aval.get("source") == "authored" and aval.get("confidence") != 1.0:
                violations.append(
                    f"id={item['id']} axis={aname} confidence={aval.get('confidence')!r}"
                )
            if len(violations) >= 5:
                break
        if len(violations) >= 5:
            break

    if violations:
        return False, "authored axes with confidence != 1.0: " + " | ".join(violations)
    return True, "all authored axes have confidence == 1.0 (fixture: none present)"


def test_inv6_one_name(data):
    """INV-6: the set of AX- axis keys is identical across all items."""
    items = data["items"]
    canonical_keys = _ax_keys(items[0])
    differing = []
    for item in items[1:]:
        item_keys = _ax_keys(item)
        if item_keys != canonical_keys:
            extra = item_keys - canonical_keys
            absent = canonical_keys - item_keys
            differing.append(
                f"id={item['id']} extra={sorted(extra)} absent={sorted(absent)}"
            )
        if len(differing) >= 5:
            break

    if differing:
        return False, "items with differing key sets: " + " | ".join(differing)
    return True, f"all {len(items)} items share the same {len(canonical_keys)}-key axis schema"


def test_scalar_values_in_range(data):
    """All axis values must be finite floats in [0, 1]."""
    violations = []
    for item in data["items"]:
        for aname, aval in item["axes"].items():
            if not aname.startswith("AX-"):
                continue
            v = aval.get("value")
            if v is None:
                continue  # null values are allowed
            if not isinstance(v, (int, float)) or v != v:
                violations.append(f"id={item['id']} {aname} value={v!r} not a finite number")
            elif not (0.0 <= v <= 1.0):
                violations.append(f"id={item['id']} {aname} value={v!r} out of [0,1]")
            if len(violations) >= 5:
                break
        if len(violations) >= 5:
            break

    if violations:
        return False, "range violations: " + " | ".join(violations)
    return True, "all axis values are finite numbers in [0,1]"


def _pstdev(vals):
    n = len(vals)
    if n == 0:
        return 0.0
    m = sum(vals) / n
    return (sum((v - m) ** 2 for v in vals) / n) ** 0.5


def test_no_dead_axis(data):
    """Every axis must actually vary across works (std >= 0.005).
    A perfectly constant axis indicates a broken formula (or degenerate fixture).
    """
    violations = []
    # Use the axis names from item[0]
    axes = list(_ax_keys(data["items"][0]))
    for aname in axes:
        vals = [
            item["axes"][aname]["value"]
            for item in data["items"]
            if isinstance(item["axes"].get(aname, {}).get("value"), (int, float))
        ]
        if not vals:
            violations.append(f"{aname} — no numeric values at all")
            continue
        std = _pstdev(vals)
        if std < 0.005:
            violations.append(f"{aname} std={std:.4f} (degenerate)")
    if violations:
        return False, "degenerate axes: " + " | ".join(violations)
    return True, f"all {len(axes)} axes vary (std >= 0.005)"


# ---------------------------------------------------------------------------
# Gap notes (recorded but not run as assertions)
# ---------------------------------------------------------------------------
GAP_NOTES = [
    "GAP: engine has no compute_vector.py (vector computation is instance-side only).",
    "GAP: INV-4 radial⟂axial — fixture has no null radial values; not applicable.",
    "GAP: INV-10 centre-less→null (D-family) — instance-specific axes; not in fixture.",
    "GAP: SCALAR_NEW_AXES — instance-specific axis names; fixture uses generic AX-NN names.",
]

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

TESTS = [
    ("INV-8  coverage             ", test_inv8_coverage),
    ("INV-9  provenance           ", test_inv9_provenance),
    ("INV-7  human wins           ", test_inv7_human_wins),
    ("INV-6  one-name             ", test_inv6_one_name),
    ("NEW    scalar range [0,1]   ", test_scalar_values_in_range),
    ("NEW    no dead axis         ", test_no_dead_axis),
]


def main():
    try:
        data = load_vector()
    except FileNotFoundError:
        print(f"FATAL: vector.json not found at {_VECTOR_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"FATAL: vector.json is not valid JSON: {exc}")
        sys.exit(1)

    for note in GAP_NOTES:
        print(f"[NOTE] {note}")
    print()

    passed = 0
    failed = 0

    for label, fn in TESTS:
        ok, reason = fn(data)
        status = "PASS" if ok else "FAIL"
        print(f"{status}  {label} — {reason}")
        if ok:
            passed += 1
        else:
            failed += 1

    print()
    print(f"{passed} passed / {failed} failed")

    if failed:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
