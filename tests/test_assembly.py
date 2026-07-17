#!/usr/bin/env python3
"""tests/test_assembly.py — the client layer-split's safety net (docs/design/
2026-07-17-client-layer-split.md). The served engine/assets/exhibition.js is a committed,
GENERATED file; engine/client/ holds it as ordered raw line-slice fragments. This suite proves
the split is honest: re-assembling the fragments in a clean temp dir reproduces the committed
file byte-for-byte. Any drift here means a fragment boundary dropped or duplicated bytes, or the
manifest and the on-disk fragments have gone out of sync — it reds BEFORE build.py or any of the
source-reading suites would even notice.

Run: .venv/bin/python tests/test_assembly.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENT_DIR = ROOT / "engine" / "client"
ASSEMBLER = ROOT / "engine" / "assemble_client.py"
COMMITTED = ROOT / "engine" / "assets" / "exhibition.js"

sys.path.insert(0, str(ROOT / "engine"))
import assemble_client  # noqa: E402

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def test_fragments_are_all_present_on_disk():
    missing = [name for name in assemble_client.MANIFEST if not (CLIENT_DIR / name).exists()]
    check("ASSEMBLY-MANIFEST every manifest entry exists on disk", not missing,
          f"missing: {missing}" if missing else "")


def test_no_stray_fragments():
    on_disk = {p.name for p in CLIENT_DIR.glob("*.js")}
    in_manifest = set(assemble_client.MANIFEST)
    stray = on_disk - in_manifest
    check("ASSEMBLY-STRAY no unlisted fragment sits in engine/client/", not stray,
          f"stray files not in MANIFEST: {sorted(stray)}" if stray else "")


def test_assemble_matches_committed_file_in_process():
    assembled = assemble_client.assemble()
    committed = COMMITTED.read_text(encoding="utf-8")
    cond = assembled == committed
    detail = ""
    if not cond:
        detail = f"len assembled={len(assembled)} len committed={len(committed)}"
        for i, (a, b) in enumerate(zip(assembled, committed)):
            if a != b:
                detail += f" first diff at char {i}: {assembled[max(0,i-20):i+20]!r} vs {committed[max(0,i-20):i+20]!r}"
                break
    check("ASSEMBLY-BYTE-PARITY assemble_client.assemble() == committed exhibition.js", cond, detail)


def test_assembler_cli_reproduces_committed_file_in_a_clean_tempdir():
    """Re-run the assembler as a subprocess against a temp copy of engine/, writing to a
    temp OUT — the strongest form of the proof: a clean process, clean dir, no import-cache
    or module-level state to quietly paper over a real drift."""
    tmp = Path(tempfile.mkdtemp(prefix="assembly_test_"))
    try:
        tmp_engine = tmp / "engine"
        shutil.copytree(ROOT / "engine" / "client", tmp_engine / "client")
        (tmp_engine / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copy2(ASSEMBLER, tmp_engine / "assemble_client.py")

        proc = subprocess.run(
            [sys.executable, str(tmp_engine / "assemble_client.py")],
            cwd=str(tmp_engine), capture_output=True, text=True,
        )
        ok_run = proc.returncode == 0
        out_path = tmp_engine / "assets" / "exhibition.js"
        assembled_bytes = out_path.read_bytes() if out_path.exists() else b""
        committed_bytes = COMMITTED.read_bytes()
        cond = ok_run and assembled_bytes == committed_bytes
        detail = ""
        if not cond:
            detail = (f"rc={proc.returncode} stderr={proc.stderr[:500]} "
                      f"len assembled={len(assembled_bytes)} len committed={len(committed_bytes)}")
        check("ASSEMBLY-CLEAN-TEMPDIR subprocess assembly in a fresh dir == committed file", cond, detail)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_check_flag_is_clean():
    proc = subprocess.run(
        [sys.executable, str(ASSEMBLER), "--check"],
        cwd=str(ROOT), capture_output=True, text=True,
    )
    check("ASSEMBLY-CHECK-FLAG assemble_client.py --check exits 0 against the committed file",
          proc.returncode == 0, proc.stdout[-500:] if proc.returncode != 0 else "")


test_fragments_are_all_present_on_disk()
test_no_stray_fragments()
test_assemble_matches_committed_file_in_process()
test_assembler_cli_reproduces_committed_file_in_a_clean_tempdir()
test_check_flag_is_clean()

fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))
print(f"\n{len(results)} rows: {len(results)-len(fails)} pass, {len(fails)} fail, 0 skip")
sys.exit(1 if fails else 0)
