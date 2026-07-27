#!/usr/bin/env python3
"""Harness drift guard — the engine's browser test harness IS the live-spec pack's canonical core,
vendored unmodified, with one project layer on top and no second copy anywhere in the tree.

The pack owns the original at ``~/live-spec/templates/headless_harness.py``. The engine vendors it
byte-for-byte at ``tests/headless_harness.py`` and layers its own driving methods in
``tests/headless.py`` by subclassing. Three copies of a hand-written harness is the state this
project came from, and the drift between them cost the run hygiene the core now carries (the
launch-time sweep, the atexit/signal teardown, the unconditional process-group reap, the two-leg
frame probe). This guard holds three facts so that state cannot return:

  * IDENTITY — the vendored core matches the pack's template byte for byte, and its checksum matches
    the pin recorded below. The pin holds on any machine; the byte comparison holds wherever the pack
    tree is present. A pack that moves the template forward reds here, which is the signal to
    re-vendor rather than to hand-patch.
  * ONE CORE — no other file in the tree launches a Chrome of its own. A resurrected copy (the
    retired ``engine/harness/headless.py`` is the one this project deleted) reds at once, naming the
    file.
  * SURFACE — every method and attribute the suites actually drive on a ``Browser`` is present on the
    subclass. A core update that drops a method reds HERE, once, instead of inside thirty suites.

Run: python tests/test_harness_drift.py  (exit 0 = all green)
"""
import ast
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS = ROOT / "tests"

VENDORED = TESTS / "headless_harness.py"
SUBCLASS = TESTS / "headless.py"
PACK_TEMPLATE = Path.home() / "live-spec" / "templates" / "headless_harness.py"

# The checksum of the pack template as vendored (live-spec 4.3.0, template last changed in pack
# commit 38d2488, 2026-07-17). Re-vendoring the template updates this line in the same edit.
VENDORED_MD5 = "8f199e1066dd645450c50bb10c920e99"

# The one file allowed to launch a browser. Everything else that carries a Chrome launch flag beside
# a process-spawn call is a second core.
CORE_REL = "tests/headless_harness.py"

LAUNCH_FLAGS = ("--remote-debugging-port", "--headless")
SPAWN_TOKENS = ("subprocess.Popen", "Popen(", "puppeteer.launch", "chromium.launch")

SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".live-spec"}

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def _md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- source reading, code only

def _strip_comments(text):
    """Drop full-line comments and trailing ``  # ...`` comments, line by line. A trailing comment is
    cut only when the ``#`` follows whitespace, so a ``#`` inside a string literal is left intact."""
    out = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        out.append(re.sub(r"\s+#.*$", "", line))
    return "\n".join(out)


def _code_only(src):
    """The source with every docstring AND every comment removed — real code only. A token that
    lives in prose can then no longer satisfy a check, and deleting the real construct reds the
    check even while a docstring still names it."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return _strip_comments(src)
    segments = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if ast.get_docstring(node, clean=False) is not None and node.body:
                seg = ast.get_source_segment(src, node.body[0])
                if seg:
                    segments.append(seg)
    for seg in segments:
        src = src.replace(seg, "", 1)
    return _strip_comments(src)


# ---------------------------------------------------------------- 1: identity with the pack template

check("harness core vendored at tests/headless_harness.py", VENDORED.is_file(),
      f"missing: {VENDORED}")

if VENDORED.is_file():
    _got = _md5(VENDORED)
    check("harness core matches the recorded pack-template checksum",
          _got == VENDORED_MD5, f"pinned {VENDORED_MD5}, vendored file is {_got}")

    if PACK_TEMPLATE.is_file():
        _same = PACK_TEMPLATE.read_bytes() == VENDORED.read_bytes()
        check("harness core is byte-identical to the pack template",
              _same,
              f"{PACK_TEMPLATE} md5 {_md5(PACK_TEMPLATE)} vs vendored md5 {_md5(VENDORED)} — "
              "re-vendor the template and update VENDORED_MD5 in this file")
    else:
        skip("harness core is byte-identical to the pack template",
             f"pack tree absent on this machine ({PACK_TEMPLATE}) — the checksum pin above still "
             "holds the identity")


# ---------------------------------------------------------------- 2: one core, no second copy

def _launches_a_browser(path):
    """True when a file's CODE carries both a Chrome launch flag and a process-spawn call — the
    signature of a harness that opens a browser of its own."""
    try:
        code = _code_only(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return False
    return (any(f in code for f in LAUNCH_FLAGS)
            and any(t in code for t in SPAWN_TOKENS))


_second_cores = []
for _p in sorted(ROOT.rglob("*.py")):
    if any(part in SKIP_DIRS for part in _p.relative_to(ROOT).parts):
        continue
    rel = _p.relative_to(ROOT).as_posix()
    if rel == CORE_REL or _p.resolve() == Path(__file__).resolve():
        continue
    if _launches_a_browser(_p):
        _second_cores.append(rel)

check("one harness core: no other file in the tree launches its own Chrome",
      not _second_cores,
      "second core(s): " + ", ".join(_second_cores) + " — the harness's one home is "
      + CORE_REL + "; a project layers on it by subclassing tests/headless.py")


# ---------------------------------------------------------------- 3: the subclass carries the surface

sys.path.insert(0, str(TESTS))
import headless  # noqa: E402  — the project layer under test


def _callables(tree):
    """Every function in one file, by the name a call would use: a plain function under its own
    name, a class under the class name mapped to its ``__init__``."""
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out.setdefault(node.name, node)
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and sub.name == "__init__":
                    out.setdefault(node.name, sub)
    return out


def _positional_names(fn):
    return [a.arg for a in (getattr(fn.args, "posonlyargs", []) + fn.args.args)]


def _browser_vars(tree):
    """The variable names that hold a ``Browser`` in ONE file. Seeded from every ``with … Browser(…)
    as NAME``, then widened along the calls in the same file: a suite that hands its browser to a
    helper (``enter(br, base)``) drives the harness through that helper's PARAMETER name, so the
    parameter joins the set and the helper's own calls are counted. Widening repeats until it
    settles, so a helper calling a helper is reached too. Scoping per file keeps an unrelated
    variable of the same name in another file out of the census."""
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                call = item.context_expr
                if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                        and call.func.id == "Browser"
                        and isinstance(item.optional_vars, ast.Name)):
                    names.add(item.optional_vars.id)
    functions = _callables(tree)
    growing = True
    while growing:
        growing = False
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
                continue
            fn = functions.get(node.func.id)
            if fn is None:
                continue
            slots = _positional_names(fn)
            offset = 1 if (slots and slots[0] == "self") else 0   # a class call skips self
            for i, arg in enumerate(node.args):
                j = i + offset
                if (isinstance(arg, ast.Name) and arg.id in names
                        and j < len(slots) and slots[j] not in names):
                    names.add(slots[j])
                    growing = True
            for kw in node.keywords:
                if (kw.arg and isinstance(kw.value, ast.Name) and kw.value.id in names
                        and kw.arg not in names):
                    names.add(kw.arg)
                    growing = True
    return names


_driven = {}          # attribute name → the suites that drive it
_reached = set()      # the suites the census actually read a browser out of
_browser_suites = set()   # the suites that import Browser at all
for _tf in sorted(TESTS.glob("test_*.py")):
    if _tf.name == Path(__file__).name:
        continue
    _src = _tf.read_text(encoding="utf-8")
    _tree = ast.parse(_src)
    for node in ast.walk(_tree):
        if isinstance(node, ast.ImportFrom) and node.module == "headless":
            if any(a.name == "Browser" for a in node.names):
                _browser_suites.add(_tf.name)
    _vars = _browser_vars(_tree)
    if not _vars:
        continue
    _reached.add(_tf.name)
    for node in ast.walk(_tree):
        if (isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
                and node.value.id in _vars):
            _driven.setdefault(node.attr, set()).add(_tf.name)

# The census's own reach, asserted rather than assumed: a suite that imports Browser but out of which
# no browser variable could be read is a suite this guard silently covers nothing of.
_unreached = sorted(_browser_suites - _reached)
check("the surface census reaches every suite that imports Browser",
      not _unreached,
      "no browser variable found in: " + ", ".join(_unreached)
      + " — widen _browser_vars() before trusting the row below")


def _instance_attrs(path):
    """Names assigned as ``self.<name> = …`` inside ``class Browser`` — the instance attributes a
    suite may read, which ``dir()`` on the class alone would not show."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "Browser":
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name)
                        and sub.value.id == "self" and isinstance(sub.ctx, ast.Store)):
                    found.add(sub.attr)
    return found


_provided = set(dir(headless.Browser)) | _instance_attrs(SUBCLASS) | _instance_attrs(VENDORED)
_missing = sorted(n for n in _driven if n not in _provided)

check("the Browser subclass carries every method and attribute the suites drive",
      not _missing,
      "missing from tests/headless.py + its core: "
      + ", ".join(f"{n} (driven by {', '.join(sorted(_driven[n]))})" for n in _missing))


# ---------------------------------------------------------------- gate
fails = [r for r in results if r[1] == "FAIL"]
for name, st, detail in results:
    print(f"[{st}] {name}" + (f"  — {detail}" if detail and st != "PASS" else ""))

print(f"\nDriven Browser surface ({len(_driven)}): {sorted(_driven)}")
print(f"Census reach: {len(_reached)} of {len(_browser_suites)} suites that import Browser")
print(f"\n{len(results)} rows: {len(results) - len(fails) - len([r for r in results if r[1] == 'SKIP'])}"
      f" pass, {len([r for r in results if r[1] == 'SKIP'])} skip, {len(fails)} fail")
sys.exit(1 if fails else 0)
