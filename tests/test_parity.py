#!/usr/bin/env python3
"""EX-QUIZ-AB hash parity — the client's quizHash() and the test util's jhash() must agree.

The A/B arm is drawn client-side by `quizHash(token + ":quizarm")` (exhibition.js) and mirrored
in Python by `quiz_util.jhash` for the browser-test fixtures (find_token_arm_on / arm_of). If the
two formulas diverge, the SAME token lands in different arms on the two sides and the quiz suites
seed themselves with a token the client disagrees with (a recorded defect).

This suite runs the client's OWN exported hash — `window.EXQuiz._hash` (exported for exactly this
check) — in node against the Python util over a spread of tokens. The export is mandatory: if the
client does not export `_hash`, the parity row FAILS (it never skips past a missing export).

Rows:
  PAR1  the client exports its hash as window.EXQuiz._hash (string contract)
  PAR2  the exported JS hash == Python jhash for every token (numeric parity, run in node)
  PAR3  the A/B arm agrees on both sides, and the two anchor tokens land where the quiz
        suites pin them (testtoken0001 -> on, qk00000005 -> control)

node is a hard dependency here (the parity cannot be asserted without it) — its absence FAILS,
never skips. Run: .venv/bin/python tests/test_parity.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
from quiz_util import jhash, arm_of  # noqa: E402

JS_PATH = ROOT / "engine" / "assets" / "exhibition.js"
JS_SRC = JS_PATH.read_text(encoding="utf-8")

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


# ---------------------------------------------------------------- token spread
TOKENS = []
for i in range(60):
    TOKENS.append("qk%08d" % i)
TOKENS += ["testtoken0001", "qk00000005", "hello", "anon",
           "abc123def456", "z9y8x7w6v5u4", "aaaaaaaa", "0000000000"]
# both salts the client uses
SALTED = []
for t in TOKENS:
    SALTED.append(t + ":quizarm")
    SALTED.append(t + ":once")

# ---------------------------------------------------------------- PAR1: the export contract
export_present = bool(re.search(r"window\.EXQuiz\s*=\s*\{[^}]*_hash\s*:\s*quizHash", JS_SRC))
check("PAR1 EX-QUIZ-AB the client exports its hash as window.EXQuiz._hash",
      export_present,
      "no `_hash: quizHash` on the window.EXQuiz export in exhibition.js"
      if not export_present else "")

# ---------------------------------------------------------------- extract the exported quizHash source
m = re.search(r"function quizHash\(str\)\s*\{.*?\n  \}", JS_SRC, re.S)
quiz_hash_src = m.group(0) if m else None
check("PAR1b EX-QUIZ-AB quizHash() source is extractable from the client",
      quiz_hash_src is not None,
      "could not locate function quizHash(str){...} in exhibition.js" if not quiz_hash_src else "")

# ---------------------------------------------------------------- PAR2 + PAR3: run the exported hash in node
node = shutil.which("node")
if node is None:
    # node absence cannot mask the parity — it is a hard dependency, so this is a FAIL not a skip
    check("PAR2 EX-QUIZ-AB exported JS hash == Python jhash for every token",
          False, "node not found on PATH — parity cannot be verified (hard dependency)")
    check("PAR3 EX-QUIZ-AB the A/B arm agrees on both sides (+ anchor tokens)",
          False, "node not found on PATH — parity cannot be verified (hard dependency)")
elif quiz_hash_src is None:
    check("PAR2 EX-QUIZ-AB exported JS hash == Python jhash for every token",
          False, "quizHash source not extractable")
    check("PAR3 EX-QUIZ-AB the A/B arm agrees on both sides (+ anchor tokens)",
          False, "quizHash source not extractable")
else:
    # Build a node program that wires the exact client function through the SAME export shape
    # (window.EXQuiz._hash) and prints hash + arm for each salted token as JSON.
    tmp = Path(tempfile.mkdtemp(prefix="parity_"))
    js = tmp / "parity.js"
    prog = (
        quiz_hash_src + "\n"
        + "var window = {};\n"
        + "window.EXQuiz = { _hash: quizHash };\n"  # the export the client ships (verified in PAR1)
        + "var toks = " + json.dumps(SALTED) + ";\n"
        + "var out = {};\n"
        + "for (var i = 0; i < toks.length; i++) {\n"
        + "  var h = window.EXQuiz._hash(toks[i]);\n"
        + "  out[toks[i]] = [h, (h / 4294967296) < 0.5 ? 'on' : 'control'];\n"
        + "}\n"
        + "process.stdout.write(JSON.stringify(out));\n"
    )
    js.write_text(prog, encoding="utf-8")
    proc = subprocess.run([node, str(js)], capture_output=True, text=True)
    shutil.rmtree(tmp, ignore_errors=True)

    if proc.returncode != 0:
        check("PAR2 EX-QUIZ-AB exported JS hash == Python jhash for every token",
              False, "node run failed: " + (proc.stderr.strip()[:300] or "rc=%d" % proc.returncode))
        check("PAR3 EX-QUIZ-AB the A/B arm agrees on both sides (+ anchor tokens)",
              False, "node run failed")
    else:
        js_out = json.loads(proc.stdout)

        # PAR2: numeric hash parity over every salted token
        hash_mismatch = []
        for tok in SALTED:
            js_h = js_out[tok][0]
            py_h = jhash(tok)
            if js_h != py_h:
                hash_mismatch.append((tok, js_h, py_h))
        check("PAR2 EX-QUIZ-AB exported JS hash == Python jhash for every token",
              not hash_mismatch,
              ("%d/%d tokens diverge, first: %r JS=%d PY=%d"
               % (len(hash_mismatch), len(SALTED), *hash_mismatch[0]))
              if hash_mismatch else "")

        # PAR3: arm parity over the ":quizarm"-salted tokens, plus the two anchors the quiz
        # suites pin (testtoken0001 -> on, qk00000005 -> control).
        arm_mismatch = []
        for tok in TOKENS:
            js_arm = js_out[tok + ":quizarm"][1]
            py_arm = arm_of(tok)
            if js_arm != py_arm:
                arm_mismatch.append((tok, js_arm, py_arm))
        anchors_ok = (arm_of("testtoken0001") == "on"
                      and arm_of("qk00000005") == "control"
                      and js_out["testtoken0001:quizarm"][1] == "on"
                      and js_out["qk00000005:quizarm"][1] == "control")
        check("PAR3 EX-QUIZ-AB the A/B arm agrees on both sides (+ anchor tokens)",
              not arm_mismatch and anchors_ok,
              ("arm diverges on %d token(s), first: %r JS=%s PY=%s; anchors_ok=%s"
               % (len(arm_mismatch), *(arm_mismatch[0] if arm_mismatch else ("-", "-", "-")),
                  anchors_ok))
              if (arm_mismatch or not anchors_ok) else "")

# ---------------------------------------------------------------- report
fails = [r for r in results if r[1] == "FAIL"]
for name, status, detail in results:
    mark = {"PASS": "ok ", "FAIL": "XX ", "SKIP": "-- "}[status]
    line = "%s%s" % (mark, name)
    if detail and status != "PASS":
        line += "  [%s]" % detail
    print(line)
n_pass = sum(1 for r in results if r[1] == "PASS")
n_skip = sum(1 for r in results if r[1] == "SKIP")
print("\ntest_parity: %d passed, %d failed, %d skipped"
      % (n_pass, len(fails), n_skip))
sys.exit(1 if fails else 0)
