#!/usr/bin/env python3
"""exhibition-engine's browser test harness — a thin project layer over the live-spec pack's
CANONICAL headless-Chrome core, vendored unmodified at ``tests/headless_harness.py``.

The core (``headless_harness.py``) owns the generic CDP plumbing: the chrome-headless-shell
preference, muted launch, the launch-time two-leg loopback/frame probe, the launch-time sweep of
profile dirs left by killed runs, the atexit/signal teardown hooks, the unconditional process-group
reap on close, and the per-command deadline — see that file's own docstring. This module owns ONLY
what is specific to the engine's own tests, layered by SUBCLASSING ``Browser`` and passing a
``serve(...)`` hook, exactly as the core's docstring prescribes, so a future core fix lands once by
re-vendoring the template and reaches every suite through this same file:

  * the WP-CLEAN clean-URL road: a baked site is served at extensionless addresses (``/about``),
    mapped here to the ``.html`` file on disk via the core's ``path_rewrite`` hook, so browser rows
    walk a visitor's real addresses;
  * EX-LOAD network shaping: ``block()`` (blocked-URL patterns) and the network-log road
    (``net_capture``/``net_clear``/``net_log``) over ``Network.setBlockedURLs`` and the
    ``requestWillBeSent`` drain, watching the one-ahead preload cross the wire;
  * EX-GREET visitor identity: ``pretend(lang, hour)`` overriding ``navigator.language`` and
    ``Date#getHours`` pre-load, for the greeting/locale rows;
  * storage helpers: ``local_storage()``, ``set_local_storage()``, ``clear_storage()``.

Chrome is located by the core at the standard macOS paths. If it is absent the core raises
``ChromeMissing`` — the caller turns that into an EXPECTED, pinned skip (never a silent pass).

Usage (unchanged for every existing suite):

    from headless import serve, Browser, ChromeMissing
    with serve(site_dir) as base, Browser() as br:
        br.navigate(base + "/")
        n = br.evaluate("document.querySelectorAll('figure').length")
"""
import contextlib
import json
import sys
import time
from pathlib import Path

from headless_harness import (  # noqa: F401  (re-exported for every suite's `from headless import …`)
    CHROME,
    Browser as _CoreBrowser,
    ChromeMissing,
    FrameProbeFailed,
    chrome_available,
    orphan_guard,
    serve as _core_serve,
    surviving_orphans,
)


def _wp_clean_rewrite(root):
    """Bind the WP-CLEAN extensionless-address map to ``root`` for the core's ``path_rewrite`` hook:
    a request for a clean path with no dot in its last segment (``/about``, not ``/style.css``) maps
    to the ``.html`` file of the same name on disk, when that file exists — the way a live host
    resolves the same address for a real visitor."""
    def _rewrite(clean):
        if clean not in ("", "/") and "." not in clean.rsplit("/", 1)[-1]:
            if Path(root + clean + ".html").is_file():
                return clean + ".html"
        return None
    return _rewrite


@contextlib.contextmanager
def serve(root, hold=None, answer=None):
    """The engine's ``serve``: the core server with the WP-CLEAN clean-URL map wired on by default.

    ``hold`` (optional): a MUTABLE dict ``{"match": substring, "delay": seconds}`` — any GET whose
    path contains ``match`` is held ``delay`` seconds before the bytes go out, so the EX-LOAD rows
    meet a slow image DETERMINISTICALLY. Passed straight through to the core.

    ``answer`` (optional, 2026-08-19): a callable ``raw_path -> (status, content_type, body) or None``
    that answers a request path directly, with no file behind it on disk — a project's stand-in for
    an API route a CDN's own Worker serves in production (EX-PASS-RECORDS's ``/api/pass/records``).
    Passed straight through to the core; see ``headless_harness.serve``'s own docstring for the
    contract. ``None`` (the default) leaves every request to the WP-CLEAN map and the file system,
    exactly as before this hook existed."""
    with _core_serve(str(root), hold=hold, path_rewrite=_wp_clean_rewrite(str(root)),
                      answer=answer) as base:
        yield base


class Browser(_CoreBrowser):
    """The engine's ``Browser``: the vendored core plus the project-specific driving methods below.
    None of these ship in the core so it stays generic — this subclass is their one home in this
    tree."""

    def __init__(self, *a, **kw):
        # set BEFORE super().__init__(): the core constructor calls self._cmd(...) internally
        # (Page.enable, Runtime.enable, the frame probe), which polymorphically dispatches to the
        # override below.
        self._net_on = False          # network-log capture (EX-LOAD-3 preload road)
        self._net_urls = []           # every requestWillBeSent URL while capture is on
        super().__init__(*a, **kw)

    # -- CDP plumbing override: drain the network log alongside every other event poll
    def _cmd(self, method, timeout=None, **params):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        self.ws._deadline = time.monotonic() + (
            self.CMD_TIMEOUT if timeout is None else timeout)
        try:
            while True:
                msg = json.loads(self.ws.recv())
                if msg.get("id") == mid:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg.get("result", {})
                # an event: drain the network log if capture is on (events interleave with
                # responses; any _cmd after a request captures it), else poll for state, not listen.
                if self._net_on and msg.get("method") == "Network.requestWillBeSent":
                    try:
                        self._net_urls.append(msg["params"]["request"]["url"])
                    except (KeyError, TypeError):
                        pass
        except ConnectionError as e:
            raise ConnectionError(
                f"{method}: {e} · chrome stderr tail:\n{self._chrome_stderr_tail()}") from e
        finally:
            self.ws._deadline = None

    # -- network shaping (EX-LOAD tests)
    def block(self, patterns):
        """Block matching URLs (CDP wildcard patterns) — requests fail with an ``error`` event,
        the way a dead image really fails. An empty list unblocks."""
        self._cmd("Network.enable")
        self._cmd("Network.setBlockedURLs", urls=list(patterns))

    # -- network log (EX-LOAD-3: watching the one-ahead preload cross the wire)
    def net_capture(self):
        """Start collecting every request URL. Events are drained during any later ``_cmd``,
        so call ``net_log()`` (which polls once) after the window you care about."""
        self._cmd("Network.enable")
        self._net_urls = []
        self._net_on = True

    def net_clear(self):
        """Forget the URLs seen so far — draw a fresh line before a turn/jump."""
        self._net_urls = []

    def net_log(self):
        """Return the request URLs seen since capture/clear. Polls the socket once (a benign
        eval) so events already delivered are drained before the read."""
        try:
            self.evaluate("1")           # drives one _cmd → its recv loop drains pending events
        except RuntimeError:
            pass
        return list(self._net_urls)

    # -- visitor identity (EX-GREET tests)
    def pretend(self, lang, hour):
        """Pre-load override of the visitor's language + clock: every document created after
        this call reports ``navigator.language == lang`` and ``Date#getHours() == hour``.
        Registered via CDP on-new-document script, so it survives navigate/reload within this
        Browser. Calling again re-defines (configurable) — the LAST pretend wins."""
        src = (
            "Object.defineProperty(Navigator.prototype,'language',"
            f"{{get:()=>{json.dumps(lang)},configurable:true}});"
            "Object.defineProperty(Navigator.prototype,'languages',"
            f"{{get:()=>[{json.dumps(lang)}],configurable:true}});"
            f"Date.prototype.getHours=function(){{return {int(hour)};}};"
        )
        self._cmd("Page.addScriptToEvaluateOnNewDocument", source=src)

    # -- storage helpers
    def local_storage(self):
        return self.evaluate("JSON.stringify(window.localStorage)")

    def set_local_storage(self, key, value):
        self.evaluate("localStorage.setItem(%s,%s)" % (json.dumps(key), json.dumps(value)))

    def clear_storage(self):
        self.evaluate("localStorage.clear()")


# THE ONE SHARED BROWSER WAIT (row S-119, provoked 2026-09-09). Nine call sites across this tree
# each kept their own copy of the same poll loop — eight named `wait_for`, one in test_lang.py named
# `poll` — and every copy had the same defect. On the day four suites shared this one machine,
# `pass_hand_profile`'s own local copy of this loop ran out of time before the browser had actually
# reached the state it was polling for, so it read `None` and handed that `None` straight back to
# its caller. The caller could not tell an empty read from a real one, wrote the empty read down as
# a fact about the product, and printed two FAIL rows reading `idled=True cadence_seen=None`. That
# same suite passed 6 of 6 a few minutes later, run on its own, once the host was not carrying three
# other suites at the same time. The machine having been busy is a fact about the machine, never a
# fact about the product, and a suite that can go red on that fact alone is a defect in the suite —
# see `/Users/sashaabramovich/tlvphotos/CLAUDE.md` under "No clock on this machine, and no verdict
# that reads its state."
#
# The repair lives here once, so it reaches every suite that imports it. A wait that finishes in
# time returns exactly what the old per-suite copies returned — the first truthy read — so nothing
# changes on the path where the browser actually got where it was going. A wait that runs OUT of
# time does not return an empty value at all, because an empty value is exactly what let the old
# copies masquerade as a verdict on the product. Instead it prints the expression it was waiting on
# and how long it waited, says in plain words that nothing printed above that line is a verdict on
# the product because the wait itself never finished, says the suite should be run on its own
# machine for a real verdict, and ends the whole process with the same exit code
# `tests/test_pass_reads.py` already uses for a run that did not reach a clean pass — 1, never a
# silent return that a caller could go on to read as a fact.
def wait_for(br, expr, timeout, step=0.05):
    """Poll `expr` in `br` until it reads truthy, or end the run rather than hand back an empty
    read. `timeout` carries no default on purpose: every suite in this tree measured its OWN budget
    for its OWN kind of browser state — a modal opening is fast, a full crossing is slow — and
    folding all of those different numbers into one shared default here would be exactly the
    flattening this row was written to avoid. The caller states its own number; this function only
    watches it honestly."""
    end = time.time() + timeout
    val = None
    while time.time() < end:
        val = br.evaluate(expr)
        if val:
            return val
        br.sleep(step)
    print(f"wait_for: timed out after {timeout}s waiting on: {expr}")
    print("nothing printed above this line is a verdict on the product. the wait itself did not "
          "finish, most likely because this machine was busy running other work at the same time "
          "(row S-119, provoked 2026-09-09 by pass_hand_profile reading a starved wait as two FAIL "
          "rows). run this suite on its own machine before reading anything above as a result.")
    sys.exit(1)


def _selftest_wait():
    """No-browser check for `wait_for`'s timeout path: `python3 tests/headless.py --selftest-wait`.
    A stub stands in for `Browser` — its `evaluate` always answers falsy, so the expression can
    never turn true and the deadline is the only way out. This asserts the run ends by exiting with
    code 1 rather than returning an empty value, and that the printed lines name the expression and
    the timeout and say plainly that nothing above them is a verdict on the product."""
    import io

    class _NeverTrue:
        def evaluate(self, expr):
            return None

        def sleep(self, seconds):
            pass

    captured = io.StringIO()
    real_stdout = sys.stdout
    caught = None
    sys.stdout = captured
    try:
        wait_for(_NeverTrue(), "window.__neverArrives", timeout=0.2, step=0.02)
    except SystemExit as e:
        caught = e
    finally:
        sys.stdout = real_stdout

    assert caught is not None, (
        "wait_for must end the run on timeout, not return an empty value to the caller")
    assert caught.code == 1, f"expected exit code 1 (test_pass_reads.py's own fail code), got {caught.code!r}"
    printed = captured.getvalue()
    assert "window.__neverArrives" in printed, "the timeout line must name the expression it waited on"
    assert "0.2" in printed, "the timeout line must name how long it waited"
    assert "not a verdict" in printed.lower() or "verdict on the product" in printed.lower(), (
        "the timeout must say plainly that nothing above it is a verdict on the product")
    print("selftest-wait: ok — timeout ends the run with exit code 1 and never returns an empty read")


if __name__ == "__main__":
    if "--selftest-wait" in sys.argv:
        _selftest_wait()
        sys.exit(0)
