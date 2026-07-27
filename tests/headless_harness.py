#!/usr/bin/env python3
"""The live-spec pack's CANONICAL headless-Chrome test harness, shipped ONCE as a template.

This is the one home of the browser test harness [SPEC INV-158]: a zero-dependency, standard-library
driver for a real headless Chrome over the DevTools Protocol (CDP) — no selenium, no playwright, no
pip. It exists so a project's browser-level interaction facts can be asserted in a REAL browser, the
way a visitor meets them, rather than string-matched in source.

Four run-hygiene properties are baked in [SPEC INV-157]:

  * it PREFERS chrome-headless-shell over Chrome for Testing over a system Chrome (``_find_chrome``,
    newest install first within each road) and PROBES A LOOPBACK PAGE at launch
    (``_probe_for_a_frame``, ``frame_probe=True`` by default): a throwaway page served from the
    loopback address (127.0.0.1), covering BOTH browser faults the 2026-07-16 incident carried — a
    LOAD leg (Chrome for Testing 151: renders frames fine but stalls loading any 127.0.0.1 page,
    ``Page.navigate`` never completing) and a FRAME leg (Chrome for Testing 150, machine-wide: opens
    its debug port and answers CDP commands but never actually paints). Either fault bleeds false reds
    through every paint-waiting (frame leg) or every page-loading (load leg) test in the run; the probe
    fails LOUDLY at launch instead, naming the browser and the failing leg, and the shell build showed
    neither fault [SPEC INV-157, ROADMAP row 364, matrix M-343];
  * it launches Chrome MUTED — the launch carries ``--mute-audio``, so a test run makes no sound on
    the machine it runs on, silencing the browser at its source and leaving system volume alone;
  * on teardown it REAPS THE WHOLE PROCESS GROUP of the Chrome it launched (helper, renderer, gpu
    children included) with a ``killpg`` SIGKILL, so a run leaves no orphan alive to accumulate
    across runs and saturate the machine (``start_new_session=True`` puts Chrome in its own group).
    Teardown runs on the CATCHABLE exits too: ``close()`` is registered on ``atexit`` and on
    ``SIGINT``/``SIGTERM`` (``_install_teardown_hooks``), so Ctrl-C and most kills still reap. For the
    UNCATCHABLE ones (``SIGKILL``, power loss, machine sleep mid-run) — which never run teardown — a
    LAUNCH-TIME SWEEP (``_sweep_stale_profiles``) is the backstop: each launch records its Chrome pid
    AND a boot identifier in its throwaway profile dir and, before opening its own, reaps any prior
    profile dir under the system temp. A dir from the CURRENT boot whose recorded owner is dead has
    its lingering process group killed, then its dir removed; a dir from a PRIOR boot needs no kill —
    a reboot already killed every process, and its recorded pid could even be reused by an unrelated
    live group, so it is only removed, never signalled. So a killed run's orphans are cleaned on the
    NEXT launch. The sweep never touches a concurrent live run — a dir whose recorded pid is still
    alive (same boot) is skipped, and a dir with no recorded owner yet is skipped, so a sibling is safe;
  * it bounds each command it sends the browser with a real PER-COMMAND DEADLINE (``CMD_TIMEOUT`` set
    on ``self._deadline``, over a blocking socket left at ``settimeout(None)``), so a slow machine
    waits patiently while a genuine hang still fails with a clear bounded error — never a blanket I/O
    timeout that fires under load and reads a slow machine as a failed test.

A consuming project adopts this harness by UPDATING THE PACK — the catch-up walk that brings a package
update onto a host — never by writing a private copy, so a fix to the core (launch flags, teardown,
deadline) lands once and reaches every consumer. A project layers its own project-specific driving
methods on top by SUBCLASSING ``Browser`` and passing ``serve(...)`` hooks. What a project layers on,
by example: EX-LOAD network shaping (``block``/network-log capture over ``Network.setBlockedURLs`` and
the ``requestWillBeSent`` drain, plus a ``serve(hold=...)`` slow-response seam); EX-GREET storage and
language/clock overrides (localStorage helpers, a pre-load ``navigator.language``/``Date#getHours``
override); EX-SHARE clipboard payload capture (pre-loading a stub over ``navigator.clipboard.writeText``
via ``inject``). None of those ship in this core — it stays generic so it cannot drift into divergent
copies. This is the pack's one-home law applied to test infrastructure [SPEC INV-158].

This module is a TEMPLATE: it is importable (no syntax errors) but is not run by live-spec's own suite.

Two pieces:
  * a tiny http server thread rooted at a project's baked site dir, so ``/``, sub-paths and
    ``fetch()`` of baked JSON all resolve over http (file:// would block the fetch);
  * a minimal CDP client over a raw-socket WebSocket: navigate, evaluate JS, dispatch NATIVE mouse
    events (so :hover and hit-testing are the browser's, not synthetic), read the DOM, set the viewport.

Chrome is located at the standard macOS path. If it is absent the harness raises ``ChromeMissing`` —
the caller turns that into an EXPECTED, pinned skip (never a silent pass).

Usage:

    from headless_harness import serve, Browser, ChromeMissing
    with serve(site_dir) as base, Browser() as br:
        br.navigate(base + "/")
        n = br.evaluate("document.querySelectorAll('figure').length")
"""
import atexit
import base64
import contextlib
import glob
import json
import os
import re
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen


def _cleanup_notice(ended, what, owned_via):
    """Say what this cleanup ended [SPEC INV-204]. The harness reaps a process group, so every reap
    reports WHAT it ended and the PROOF the run owned it (the process group it launched, or the owner
    pid it recorded), making an ending nobody expected visible the moment it happens rather than at the
    next unexplained loss. Emitted to stderr, beside the run's own diagnostics.

    This is the inline twin of the pack's shared shape ``guardrails/cleanup_notice.py`` — the ``CLEANUP-
    NOTICE`` marker's one home — carried here because the template is vendored standalone and cannot
    import the pack. Failure to emit never blocks a reap: the ending still runs."""
    with contextlib.suppress(Exception):
        sys.stderr.write("CLEANUP-NOTICE ended=%s what=%s owned-via=%s\n" % (ended, what, owned_via))
        sys.stderr.flush()


def _find_chrome():
    """Resolution order, newest install first within each road [SPEC INV-157, ROADMAP row 364]:

      1. chrome-headless-shell — the dedicated headless build, preferred FIRST. Incident 2026-07-16:
         Chrome for Testing 150 went frame-dead machine-wide (opened its debug port, accepted every CDP
         command, but never produced a single compositor frame), bleeding false reds through every
         paint-waiting test; chrome-headless-shell 151 showed no such fault. Install it with
         ``npx @puppeteer/browsers install chrome-headless-shell@stable --path ~/.cache/puppeteer``.
      2. Chrome for Testing — an automation-only build that never touches the user's own Chrome
         profile, does not coordinate with a running user browser, and is safe to hard-kill by its
         own path.
      3. the user's installed Chrome, as the last resort.
    """
    candidates = sorted(glob.glob(os.path.expanduser(
        "~/.cache/puppeteer/chrome-headless-shell/*/chrome-headless-shell-mac*/chrome-headless-shell")),
        reverse=True)
    candidates += sorted(glob.glob(os.path.expanduser(
        "~/.cache/puppeteer/chrome/*/chrome-mac*/Google Chrome for Testing.app"
        "/Contents/MacOS/Google Chrome for Testing")), reverse=True)
    candidates += [
        "/Applications/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
    return candidates[-1]   # the standard path even if absent — ChromeMissing handles it


def _is_headless_shell(path):
    """True when the resolved binary is the dedicated chrome-headless-shell build — headless by
    construction, so its launch must OMIT ``--headless=new`` (a Chrome-for-Testing/system-Chrome-only
    flag the shell does not accept) [SPEC INV-157, ROADMAP row 364]."""
    return "chrome-headless-shell" in path


CHROME = _find_chrome()


class ChromeMissing(Exception):
    """Chrome is not installed — the caller converts this into a pinned, expected skip."""


class FrameProbeFailed(Exception):
    """The launch frame probe (matrix M-343) never observed a compositor frame within its bound —
    distinct from a TEST failure: the BROWSER itself is frame-dead, so every paint-waiting test in the
    run would red falsely against it [SPEC INV-157, ROADMAP row 364]. The caller sees this loud,
    named failure instead of a mystifying wall of unrelated test reds."""


def chrome_available():
    return Path(CHROME).exists()


# ---------------------------------------------------------------- killed-run backstops [INV-157]
#
# close() reaps the process group on a NORMAL teardown, but a run KILLED before teardown (SIGKILL,
# power loss, machine sleep mid-run, a Chrome crash that takes the harness with it) never reaches it,
# so its Chrome group and its throwaway profile dir leak and pile up across runs — the machine
# saturation the invariant forbids. Two guards close that gap: teardown on the CATCHABLE signals, and
# a launch-time sweep of this harness's own crash leftovers as the backstop for the uncatchable ones.

PROFILE_PREFIX = "livespec_cdp_"       # the mkdtemp prefix every run's profile dir carries
OWNER_PID_FILE = "OWNER_PID"           # each run records "<chrome pid>\n<boot id>" here so the sweep
                                       # can tell a crash leftover (owner dead, SAME boot) from a live
                                       # concurrent run (owner alive) and from a prior-boot dir (a
                                       # reboot already killed everything — the pid is meaningless)
OWNERLESS_STALE_AGE = 3600             # an ownerless profile dir older than this (seconds) is a killed
                                       # run's leftover, not a live mid-launch sibling — safe to reap [333]
PROFILE_GLUT_WARN = 50                 # this many of the harness's own dirs still under the temp roots is
                                       # a leak surfacing loudly, so a full temp never reads as product reds


def _boot_id():
    """A best-effort identifier of the CURRENT boot, so the sweep can tell a profile dir left by THIS
    boot (its recorded pid still names a real process) from one left by a PRIOR boot (a reboot already
    killed every process, so the pid is meaningless — and a dead pid can be reused post-reboot as an
    unrelated live group leader, which must never be signalled). Linux: the ``btime`` line of
    ``/proc/stat``. macOS: the ``sec = N`` field of ``sysctl -n kern.boottime``. Neither obtainable →
    ``None`` (the sweep then treats every recorded pid as meaningless and only rmtree's, never kills)."""
    with contextlib.suppress(Exception):                       # Linux
        with open("/proc/stat") as f:
            for line in f:
                if line.startswith("btime"):
                    return line.split()[1]
    with contextlib.suppress(Exception):                       # macOS
        out = subprocess.run(["sysctl", "-n", "kern.boottime"],
                             capture_output=True, text=True, timeout=5).stdout
        m = re.search(r"sec\s*=\s*(\d+)", out)                 # "{ sec = 1720000000, usec = ... } ..."
        if m:
            return m.group(1)
    return None


def _pid_alive(pid):
    """True if a process with this pid is live. ``os.kill(pid, 0)`` probes WITHOUT signalling:
    ProcessLookupError → the pid is dead; PermissionError → alive but not ours (treat as alive)."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return True
    return True


def _temp_roots():
    """Every temp workspace this harness could have dropped a profile dir in — not only the CURRENT
    session's ``tempfile.gettempdir()`` [INV-157, Fable F5]. On macOS each login/launchd context gets
    its OWN per-user temp (``/var/folders/<xx>/<yyy>/T``), so a terminal run and a launchd run never
    share a root; a sweep that scanned only the current root would leave the other context's crash
    orphans alive forever. Collect: the current ``gettempdir()``, the classic ``/tmp`` and ``/var/tmp``,
    and every per-user macOS temp under ``/var/folders/*/*/T``. Deduped by REAL path (so a symlinked
    ``/tmp`` → ``/private/tmp`` is not scanned twice); a root that is missing or unreadable simply
    yields nothing in the later glob, so it costs nothing to list."""
    roots = {tempfile.gettempdir(), "/tmp", "/var/tmp"}
    roots.update(glob.glob("/var/folders/*/*/T"))
    seen, out = set(), []
    for r in roots:
        with contextlib.suppress(OSError):
            rp = os.path.realpath(r)
            if rp not in seen and os.path.isdir(rp):
                seen.add(rp)
                out.append(rp)
    return out


def _sweep_stale_profiles(exclude=None):
    """Launch-time backstop: reap ONLY this harness's own provable crash leftovers — profile dirs
    matching ``PROFILE_PREFIX`` under EVERY temp workspace the harness could have used (``_temp_roots``,
    not just the current tempdir). Each run's dir is unique (``mkdtemp``) and
    records ``"<chrome pid>\\n<boot id>"`` in ``OWNER_PID_FILE`` at launch. Three cases:

      * SAME BOOT, owner dead  → a genuine crash leftover: kill any process group still bound to the
        recorded pid (``killpg`` SIGKILL), then remove the dir.
      * SAME BOOT, owner alive → a live concurrent run: SKIP — never reaped, so a sibling is safe.
      * CROSS BOOT (or either boot id unknown/None) → a reboot already killed every process, so the
        recorded pid names nothing live — and could have been reused post-reboot by an UNRELATED live
        group. So the dir is only removed, NEVER signalled: killpg on a reused pid would kill innocents.

    An OWNERLESS dir (no ``OWNER_PID_FILE`` yet, or unparseable) is SKIPPED entirely — a dir caught
    between ``mkdtemp`` and a slow/failed pid write could still belong to a live sibling, so it is
    never rmtree'd and never killed. ``exclude`` (the current run's own dir) is never touched."""
    exclude_abs = os.path.realpath(exclude) if exclude else None
    current_boot = _boot_id()
    candidates = []
    for root in _temp_roots():
        candidates += glob.glob(os.path.join(root, PROFILE_PREFIX + "*"))
    for path in candidates:
        if not os.path.isdir(path):
            continue
        if exclude_abs is not None and os.path.realpath(path) == exclude_abs:
            continue
        owner, boot = None, None
        try:
            with open(os.path.join(path, OWNER_PID_FILE)) as f:
                owner = int(f.readline().strip())
                boot = f.readline().strip() or None
        except (FileNotFoundError, ValueError, OSError):
            owner, boot = None, None
        if owner is None:
            # ownerless: no OWNER_PID written — yet, or ever. A dir caught mid-launch (its pid write
            # not landed) could be a LIVE sibling, so a YOUNG ownerless dir is left alone. But the
            # system temp is NOT self-purging (macOS /var/folders survives across runs and days), so an
            # OLD ownerless dir is a killed run's leftover — or a process-less baked dir — that would
            # accumulate forever; once it is well past any mid-launch window it is stale litter, removed
            # (never signalled — there is no pid to signal) [INV-100, INV-157, ROADMAP 333].
            with contextlib.suppress(OSError):
                if time.time() - os.path.getmtime(path) > OWNERLESS_STALE_AGE:
                    shutil.rmtree(path, ignore_errors=True)
            continue
        same_boot = current_boot is not None and boot is not None and boot == current_boot
        if not same_boot:
            # a prior (or unknown) boot: the recorded pid is meaningless and possibly reused by an
            # unrelated live group. Remove the dir only — NEVER killpg.
            shutil.rmtree(path, ignore_errors=True)
            continue
        # same boot: the recorded pid is meaningful.
        if _pid_alive(owner):
            continue        # a live owner — a concurrent run; NEVER reaped
        with contextlib.suppress(Exception):
            _cleanup_notice("pgid=%s" % owner,
                            "a prior run's lingering Chrome process group (this harness launched it)",
                            "recorded owner pid in %s, same boot, owner now dead" % path)
            os.killpg(owner, signal.SIGKILL)   # dead owner, same boot: reap its lingering group
        shutil.rmtree(path, ignore_errors=True)
    # Surface a glut loudly: many of the harness's own dirs still under the temp roots means a run is
    # leaking (or the temp is filling), so it never masquerades as product test reds [ROADMAP 333].
    if len(candidates) > PROFILE_GLUT_WARN:
        with contextlib.suppress(Exception):
            sys.stderr.write(
                "live-spec harness: WARNING — %d of the harness's own profile dirs under the temp roots "
                "(prefix %r) at launch; a healthy run reaps its own, so a persistently high count means "
                "the temp home is filling and a run is leaking.\n" % (len(candidates), PROFILE_PREFIX))


# Registry of live Browsers so a single atexit / signal handler can tear every one of them down.
_LIVE_BROWSERS = set()
_TEARDOWN_HOOKS_INSTALLED = False

# Every Chrome owner pid THIS PROCESS launched, recorded at each Browser launch. The by-deed orphan
# net scopes to this set rather than a machine-wide temp census, so a concurrent sibling suite running
# in ANOTHER process — even one whose browser is born mid-window — is never mistaken for this suite's
# own leaked orphan [INV-157, Fable/prover F1].
_LAUNCHED_OWNERS = set()


def _teardown_all_browsers():
    """Close every still-live Browser — the body atexit and the signal handlers run."""
    for br in list(_LIVE_BROWSERS):
        with contextlib.suppress(Exception):
            br.close()


def _install_teardown_hooks():
    """Register _teardown_all_browsers on atexit and on SIGINT/SIGTERM (once per process), so the
    CATCHABLE exits — Ctrl-C, a plain ``kill`` — still run close() and reap the process group. The
    launch sweep covers the uncatchable ones. Signal handlers only install on the main thread; off
    the main thread the ValueError is swallowed and atexit alone carries the teardown."""
    global _TEARDOWN_HOOKS_INSTALLED
    if _TEARDOWN_HOOKS_INSTALLED:
        return
    _TEARDOWN_HOOKS_INSTALLED = True
    atexit.register(_teardown_all_browsers)
    for _sig in (signal.SIGINT, signal.SIGTERM):
        prev = signal.getsignal(_sig)
        if prev is signal.SIG_IGN:
            # the host DELIBERATELY ignored this signal — respect that intent; do not resurrect it into
            # a process-killing handler [INV-157, Fable F8]. atexit still carries teardown on a normal
            # exit, and a host that ignores SIGTERM has already chosen to stay alive through it.
            continue

        def _handler(signum, frame, _prev=prev):
            _teardown_all_browsers()
            # chain to whatever was there before so the normal exit still happens
            if callable(_prev) and _prev not in (signal.SIG_DFL, signal.SIG_IGN):
                _prev(signum, frame)
            else:
                signal.signal(signum, signal.SIG_DFL)
                os.kill(os.getpid(), signum)

        with contextlib.suppress(ValueError, OSError):
            signal.signal(_sig, _handler)


# ---------------------------------------------------------------- by-deed orphan net [INV-157, F7]
#
# The teardown reap and the launch sweep are the harness's OWN guards; a consumer still owes a net that
# PROVES, by deed, that a suite left no Chrome group behind — a post-run process census that reads live
# OS state, not the harness code by eye. The pack ships that net HERE, in the harness's one home, so a
# consumer adopts it with the template instead of writing a private copy [INV-158]. It is scoped to this
# harness's own profile dirs (the OWNER_PID marker), so it never counts the user's own Chrome.

def _own_live_owners():
    """The Chrome owner pids THIS PROCESS launched (recorded in ``_LAUNCHED_OWNERS`` at each Browser
    launch) that are STILL ALIVE right now. Reading live process state through ``_pid_alive`` keeps it a
    by-deed census; scoping to this process's own launches — never a machine-wide temp-dir census —
    means a concurrent sibling suite in ANOTHER process is never counted, even one whose browser is born
    mid-window [F1]."""
    return {pid for pid in set(_LAUNCHED_OWNERS) if _pid_alive(pid)}


def surviving_orphans():
    """A consumer's by-deed orphan census: the pids of THIS process's own harness Chromes still alive
    now. Call it AFTER a suite's browser teardown — a clean run returns ``[]``, a teardown regression
    returns the live owners this process launched, so a consumer writes ``assert not surviving_orphans()``
    as a net that reads real OS state instead of trusting the teardown code by eye. It counts only
    browsers this process launched, so a concurrent sibling suite in another process never false-reds
    it."""
    return sorted(_own_live_owners())


@contextlib.contextmanager
def orphan_guard():
    """A by-deed post-run orphan net for a consumer's suite. Wrap the browser tests (or a session-scoped
    fixture) in it::

        with orphan_guard():
            run_the_browser_tests()

    On exit it RAISES ``AssertionError`` if any Chrome THIS PROCESS launched DURING the window is still
    alive — a reaped-teardown regression goes red HERE, where a docstring cannot satisfy it. It scopes to
    this process's own launches (the ``_LAUNCHED_OWNERS`` set), so a concurrent sibling suite in another
    process — even one that starts its browser mid-window — never false-reds this guard [F1]; a browser
    launched before the window is left to that outer scope."""
    before = set(_LAUNCHED_OWNERS)
    try:
        yield
    finally:
        leaked = sorted(pid for pid in set(_LAUNCHED_OWNERS)
                        if pid not in before and _pid_alive(pid))
        if leaked:
            raise AssertionError(
                "browser-harness orphans survived the run — teardown did not reap [INV-157]: "
                + ", ".join("pid %d" % p for p in leaked))


# ---------------------------------------------------------------- local http server

@contextlib.contextmanager
def serve(root, hold=None, path_rewrite=None):
    """Serve ``root`` over http on a free port; yields the base URL. Quiet, threaded.

    Two OPTIONAL project hooks, both inert by default so the template ships generic:

    ``hold`` (optional): a MUTABLE dict ``{"match": substring, "delay": seconds}`` — any GET whose
    path contains ``match`` is held ``delay`` seconds before the bytes go out. A project passes it to
    meet a slow response DETERMINISTICALLY (a real request, really late) without CDP throttling
    starving the boot's own fetches. The dict is read per-request, so a test may relax it mid-run.

    ``path_rewrite`` (optional): a callable ``clean_path -> new_path_or_None``. A project passes it to
    remap a request path before it is served — e.g. a live host that serves clean extensionless
    addresses maps ``/about`` to ``/about.html`` on disk, so browser rows walk a visitor's real
    addresses. Returning ``None`` leaves the path untouched. Off by default."""
    root = str(root)
    hold = hold if hold is not None else {}

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=root, **k)

        def do_GET(self):
            # optional project path remap (e.g. extensionless clean address → .html on disk)
            if path_rewrite is not None:
                clean = self.path.split("?", 1)[0].split("#", 1)[0]
                new = path_rewrite(clean)
                if new:
                    self.path = new
            m = hold.get("match")
            if m and m in self.path:
                time.sleep(float(hold.get("delay", 0)))
            # never let Chrome revalidate to a 304 — a config.json patched between reloads (an A/B
            # test) must be read fresh, not served from the browser cache.
            for h in ("If-Modified-Since", "If-None-Match"):
                if h in self.headers:
                    del self.headers[h]
            try:
                return super().do_GET()
            except (ConnectionResetError, BrokenPipeError):
                pass    # the browser left mid-transfer (e.g. teardown during a held response)

        def end_headers(self):
            self.send_header("Cache-Control", "no-store, must-revalidate")
            super().end_headers()

        def log_message(self, *a):  # silence
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        httpd.shutdown()
        httpd.server_close()


# ---------------------------------------------------------------- raw WebSocket (client)

class _WS:
    """The few WebSocket frames CDP needs: masked text out, unmasked text in, ping→pong."""

    def __init__(self, url):
        # url: ws://host:port/devtools/page/<id>
        assert url.startswith("ws://")
        hostport, _, path = url[len("ws://"):].partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port or 80)), timeout=10)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET /{path} HTTP/1.1\r\n"
            f"Host: {hostport}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        self._buf = b""
        # read handshake response up to end of headers
        while b"\r\n\r\n" not in self._buf:
            self._buf += self.sock.recv(4096)
        head, self._buf = self._buf.split(b"\r\n\r\n", 1)
        if b"101" not in head.split(b"\r\n")[0]:
            raise RuntimeError("websocket upgrade failed: " + head.decode(errors="replace"))
        # After the handshake, reads BLOCK by default (create_connection left a fixed 10s timeout
        # on the socket — under parallel-suite CPU load a CDP response slower than 10s used to throw
        # socket.timeout and read as a suite FAILURE; that false red is what forced --jobs 1). A real
        # per-command deadline (set by _cmd via self._deadline) governs each wait instead, so a slow
        # answer is patient while a genuine hang still fails with a clear, bounded error.
        self._deadline = None
        self.sock.settimeout(None)

    def send(self, text):
        data = text.encode()
        header = bytearray([0x81])  # FIN + text
        n = len(data)
        mask = os.urandom(4)
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
        self.sock.sendall(bytes(header) + masked)

    def _read(self, n):
        while len(self._buf) < n:
            if self._deadline is not None:
                remaining = self._deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("CDP read exceeded its deadline (chrome unresponsive)")
                self.sock.settimeout(remaining)
            chunk = self.sock.recv(65536)
            if not chunk:
                raise ConnectionError("websocket closed")
            self._buf += chunk
        out, self._buf = self._buf[:n], self._buf[n:]
        return out

    def recv(self):
        """Return the next text-message payload (reassembling fragments, answering pings)."""
        payload = b""
        while True:
            b0, b1 = self._read(2)
            fin = b0 & 0x80
            opcode = b0 & 0x0F
            ln = b1 & 0x7F
            if ln == 126:
                ln = struct.unpack(">H", self._read(2))[0]
            elif ln == 127:
                ln = struct.unpack(">Q", self._read(8))[0]
            data = self._read(ln)
            if opcode == 0x9:      # ping → pong
                self._pong(data)
                continue
            if opcode == 0x8:      # close
                raise ConnectionError("websocket closed by peer")
            payload += data
            if fin:
                if opcode in (0x1, 0x0):
                    return payload.decode(errors="replace")
                payload = b""      # ignore non-text, keep reading

    def _pong(self, data):
        header = bytearray([0x8A])
        mask = os.urandom(4)
        header.append(0x80 | len(data))
        header += mask
        self.sock.sendall(bytes(header) + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def close(self):
        with contextlib.suppress(Exception):
            self.sock.close()


# ---------------------------------------------------------------- CDP browser

class Browser:
    """A driven headless Chrome page — the shared CORE. Context manager: launches on enter, kills on
    exit. A project layers its own driving methods on top by SUBCLASSING this, never by editing it."""

    def __init__(self, width=1280, height=900, frame_probe: bool = True):
        if not chrome_available():
            raise ChromeMissing(CHROME)
        # Backstop for a run KILLED before teardown: before opening our own profile, sweep this
        # harness's stale leftovers from prior runs killed by SIGKILL/power loss (they never ran
        # close()). Runs BEFORE mkdtemp, so our own dir does not exist yet and cannot be swept
        # [INV-157]. Also arm the catchable-signal + atexit teardown so Ctrl-C/kill reap too.
        _sweep_stale_profiles()
        _install_teardown_hooks()
        self.width, self.height = width, height
        self._id = 0
        self._profile = tempfile.mkdtemp(prefix=PROFILE_PREFIX)
        _LIVE_BROWSERS.add(self)
        # Seed the owner marker with THIS harness process's own pid IMMEDIATELY — before Chrome even
        # launches — so a live run is NEVER ownerless. If the Chrome-pid overwrite below fails (a full
        # temp swallowing the write, the very ENOSPC condition the age sweep targets), the dir still
        # names a live owner (this process), so a sibling's launch sweep sees a live owner and leaves it
        # alone rather than reaping a live run's profile by age. The write after launch overwrites this
        # with Chrome's own group pid. The dead-owner branch only ever killpg's a DEAD pid (a no-op on
        # this provisional pid if the process is gone), so seeding it is safe [INV-157, ROADMAP 333 / prover F1].
        with contextlib.suppress(Exception):
            with open(os.path.join(self._profile, OWNER_PID_FILE), "w") as f:
                f.write("%s\n%s\n" % (os.getpid(), _boot_id() or ""))
        # Chrome's own stderr goes to a file in the throwaway profile (not /dev/null): when the CDP
        # pipe dies, _chrome_stderr_tail() reads the crash reason out of it, so a renderer/browser
        # crash names itself instead of surfacing as a bare "websocket closed".
        self._stderr_path = os.path.join(self._profile, "chrome-stderr.log")
        self._stderr_f = open(self._stderr_path, "wb")
        # --remote-debugging-port=0: Chrome picks its OWN free port atomically and writes it to
        # <profile>/DevToolsActivePort — no TOCTOU race with sibling suites launching at the same
        # instant (a pre-picked port two launches could both grab was the "no CDP page target" flake).
        # --mute-audio: the run makes no sound on the machine — muted at the browser's source, system
        # volume untouched [INV-157]. start_new_session puts Chrome in its own process group so close()
        # reaps every helper child (the orphan Chromes that used to accumulate and compound saturation).
        # --headless=new is a Chrome-for-Testing/system-Chrome flag only — chrome-headless-shell is
        # headless by construction and does not accept it, so the shell road drops it [ROADMAP row 364].
        args = [CHROME]
        if not _is_headless_shell(CHROME):
            args.append("--headless=new")
        args += [
            "--disable-gpu", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
            "--mute-audio", "--remote-debugging-port=0",
            f"--user-data-dir={self._profile}",
            f"--window-size={width},{height}", "about:blank",
        ]
        self.proc = subprocess.Popen(
            args, stdout=subprocess.DEVNULL, stderr=self._stderr_f, start_new_session=True,
        )
        # Record Chrome's pid (its own process-group leader) AND the current boot id in the profile
        # dir, so a later run's launch sweep can tell this dir's owner is dead-but-same-boot (a crash
        # leftover, safe to reap) from a live concurrent run (owner alive) and from a prior-boot dir
        # (a reboot killed everything; the pid is meaningless and must never be signalled) [INV-157].
        with contextlib.suppress(Exception):
            with open(os.path.join(self._profile, OWNER_PID_FILE), "w") as f:
                f.write("%s\n%s\n" % (self.proc.pid, _boot_id() or ""))
        # Record this launch in the process's own owner set so the by-deed orphan net can scope to what
        # THIS process launched, never a machine-wide census that a sibling process would pollute [F1].
        _LAUNCHED_OWNERS.add(self.proc.pid)
        self.port = self._read_devtools_port()
        self.ws = self._connect_page()
        self._cmd("Page.enable")
        self._cmd("Runtime.enable")
        # A real <a download> click without this drops files into the user's ~/Downloads on every
        # run. Route downloads into the throwaway profile dir instead — close() rmtree's it.
        try:
            self._cmd("Browser.setDownloadBehavior",
                      behavior="allow", downloadPath=self._profile)
        except RuntimeError:
            self._cmd("Page.setDownloadBehavior",
                      behavior="allow", downloadPath=self._profile)
        # Launch frame probe [SPEC INV-157, ROADMAP row 364, matrix M-343] — the LAST step before this
        # Browser hands itself to the calling suite: catch a frame-dead browser HERE, loudly, instead
        # of letting it bleed false reds through every paint-waiting test that follows.
        if frame_probe:
            try:
                self._probe_for_a_frame()
            except BaseException:
                # a failed probe reaps the just-launched Chrome at once; the atexit hook stays the
                # backstop for interpreter exit only [2.3.0 audit, finding 4]
                self.close()
                raise

    # -- lifecycle
    def _read_devtools_port(self, timeout=20):
        # Chrome launched with --remote-debugging-port=0 writes the port it actually bound to the
        # first line of <profile>/DevToolsActivePort once its debug server is up. Reading it there
        # (instead of pre-picking a port) removes the launch race entirely. A Chrome that dies before
        # writing the file is caught by proc.poll() and names its own reason from stderr.
        pf = os.path.join(self._profile, "DevToolsActivePort")
        end = time.time() + timeout
        while time.time() < end:
            if self.proc.poll() is not None:
                raise RuntimeError("chrome exited before opening a debug port · stderr:\n"
                                   + self._chrome_stderr_tail())
            try:
                with open(pf) as f:
                    first = f.readline().strip()
                if first:
                    return int(first)
            except (FileNotFoundError, ValueError):
                pass
            time.sleep(0.05)
        raise RuntimeError("chrome never wrote DevToolsActivePort · stderr:\n"
                           + self._chrome_stderr_tail())

    def _connect_page(self):
        base = f"http://127.0.0.1:{self.port}"
        target = None
        for _ in range(100):                       # up to ~10s for Chrome to open the port
            try:
                data = json.load(urlopen(base + "/json", timeout=1))
                pages = [t for t in data if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
                if pages:
                    target = pages[0]
                    break
            except Exception:
                time.sleep(0.1)
        if not target:
            raise RuntimeError("no CDP page target appeared")
        return _WS(target["webSocketDebuggerUrl"])

    def _chrome_stderr_tail(self, n=2500):
        try:
            with contextlib.suppress(Exception):
                self._stderr_f.flush()
            with open(self._stderr_path, "rb") as f:
                data = f.read()
            tail = data[-n:].decode(errors="replace").strip()
            return tail or "(chrome stderr empty — a clean process exit, not a logged crash)"
        except Exception:
            return "(chrome stderr unavailable)"

    def close(self):
        with contextlib.suppress(Exception):
            self.ws.close()
        with contextlib.suppress(Exception):
            self.proc.terminate()
            self.proc.wait(timeout=5)
        # Reap the whole process group UNCONDITIONALLY (Chrome spawns helper/renderer/gpu children):
        # a SIGKILL to the group. NOT gated on poll() — when the leader exits within the graceful
        # wait but a renderer/gpu child is still wedged, the group must STILL be killed, or that child
        # orphans forever (the profile dir marker is rmtree'd just below, so the launch sweep can't
        # find it either — a permanent orphan). start_new_session=True guarantees pid==pgid, so killpg
        # on the leader pid reaches any surviving child even when the leader itself is gone [INV-157].
        with contextlib.suppress(ProcessLookupError, OSError):
            _cleanup_notice("pgid=%s" % self.proc.pid,
                            "the Chrome process group this run launched (leader + renderer/gpu children)",
                            "process group this run created (start_new_session, pid==pgid)")
            os.killpg(self.proc.pid, signal.SIGKILL)
        with contextlib.suppress(Exception):
            self._stderr_f.close()
        shutil.rmtree(self._profile, ignore_errors=True)
        _LIVE_BROWSERS.discard(self)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

    # -- CDP plumbing
    CMD_TIMEOUT = 60           # generous per-command deadline: a slow answer is patient, a hang fails clearly
    FRAME_PROBE_TIMEOUT = 2.0  # bounded default for the launch frame probe [INV-157, ROADMAP row 364]

    def _cmd(self, method, timeout=None, **params):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        self.ws._deadline = time.monotonic() + (self.CMD_TIMEOUT if timeout is None else timeout)
        try:
            while True:
                msg = json.loads(self.ws.recv())
                if msg.get("id") == mid:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg.get("result", {})
                # else: an event. We poll for state, not listen. A project that needs to drain a
                # particular event stream (e.g. a network log) overrides this in its subclass.
        except ConnectionError as e:
            # A TCP FIN means Chrome itself closed the pipe — a renderer/browser crash. Name its
            # cause: surface the tail of Chrome's own stderr (captured to the profile dir) so the
            # crash reason travels with the error instead of a mystery "websocket closed".
            raise ConnectionError(f"{method}: {e} · chrome stderr tail:\n{self._chrome_stderr_tail()}") from e
        finally:
            self.ws._deadline = None

    def _probe_for_a_frame(self, timeout=FRAME_PROBE_TIMEOUT):
        """Launch-time TWO-LEG probe, served from the loopback address [SPEC INV-157, ROADMAP row 364,
        matrix M-343]. The 2026-07-16 incident carried two distinct browser faults, and a probe that
        only used a ``data:`` page (which loads even when 127.0.0.1 itself is stalled) would catch one
        and miss the other entirely:

          * leg LOAD — Chrome for Testing 151: renders frames fine but STALLS loading any 127.0.0.1
            page (``Page.navigate`` never completes, though ``data:`` URLs load fine on it);
          * leg FRAME — Chrome for Testing 150, machine-wide: opens its debug port and answers CDP
            commands but never actually paints (``requestAnimationFrame`` never fires).

        A tiny one-shot HTTP server is bound to 127.0.0.1 (port 0) for the duration of the probe; each
        leg is bounded by its OWN deadline (``timeout``), reusing the same per-command deadline
        machinery every other CDP wait in this file uses (INV-155: a real bounded deadline, never a
        blanket sleep). A failing leg raises ``FrameProbeFailed`` naming ITS OWN fault shape, the
        resolved browser, and the fix — loud, at launch, instead of bleeding false reds through every
        later page-loading or paint-waiting test. The server is always shut down and its thread joined
        in a ``finally``, so the probe leaves nothing running whatever the outcome [INV-100]. If
        binding the loopback listener itself fails (a sandboxed/offline host with no loopback
        available), the probe falls back to the previous ``data:`` road for the FRAME leg only — the
        LOAD leg needs a real loopback page, so it is skipped on that fallback."""
        class _ProbeHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                body = b"<!doctype html><html></html>"
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):  # silence
                pass

        def _await_frame():
            try:
                self._cmd(
                    "Runtime.evaluate", timeout=timeout,
                    expression="new Promise(resolve => requestAnimationFrame(resolve))",
                    awaitPromise=True, returnByValue=True,
                )
            # socket.timeout: on Python < 3.10 the deadline machinery's expiry raises it with no
            # TimeoutError kinship (they merged in 3.10) — catching both keeps the probe's loud
            # named failure on every interpreter this template ships to [2.3.0 audit, finding 1].
            except (TimeoutError, socket.timeout):
                raise FrameProbeFailed(
                    "FRAME PROBE FAILED: %s — the browser produced no compositor frame within %.1f s. "
                    "paint-waiting tests would red falsely on this browser. "
                    "Fix: install the dedicated headless build: "
                    "npx @puppeteer/browsers install chrome-headless-shell@stable --path ~/.cache/puppeteer"
                    % (CHROME, timeout)
                ) from None

        try:
            server = HTTPServer(("127.0.0.1", 0), _ProbeHandler)
        except OSError:
            # fallback road: the loopback listener itself would not bind — skip the LOAD leg (it needs
            # a real loopback page) and fall back to the previous data: page for the FRAME leg only.
            self._cmd("Page.navigate", timeout=timeout, url="data:text/html,<!doctype html><html></html>")
            _await_frame()
            return
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            # leg LOAD: Chrome for Testing 151 renders frames but stalls loading any 127.0.0.1 page.
            try:
                self._cmd("Page.navigate", timeout=timeout, url="http://127.0.0.1:%d/" % port)
            except (TimeoutError, socket.timeout):
                raise FrameProbeFailed(
                    "FRAME PROBE FAILED: %s stalls loading loopback pages — Page.navigate to a "
                    "127.0.0.1 page never completed within %.1f s (data: URLs load fine on this "
                    "browser). paint-waiting tests would red falsely on this browser. "
                    "Fix: install the dedicated headless build: "
                    "npx @puppeteer/browsers install chrome-headless-shell@stable --path ~/.cache/puppeteer"
                    % (CHROME, timeout)
                ) from None
            # leg FRAME: the browser opens its debug port and answers commands but never paints.
            _await_frame()
        finally:
            server.shutdown()
            thread.join()

    # -- page control
    def navigate(self, url):
        self.set_viewport(self.width, self.height)
        self._cmd("Page.navigate", url=url)
        self._wait_ready()

    def reload(self):
        self._cmd("Page.reload")
        self._wait_ready()

    def _wait_ready(self, timeout=10):
        end = time.time() + timeout
        while time.time() < end:
            try:
                if self.evaluate("document.readyState") == "complete":
                    # one extra tick so first requestAnimationFrame render settles
                    self.sleep(0.15)
                    return
            except RuntimeError:
                pass                                # navigation in flight; retry
            time.sleep(0.05)
        raise TimeoutError("page did not reach readyState=complete")

    def set_viewport(self, width, height, mobile=False):
        self.width, self.height = width, height
        self._cmd("Emulation.setDeviceMetricsOverride",
                  width=width, height=height, deviceScaleFactor=1, mobile=mobile)

    def emulate_media(self, **features):
        """Emulate CSS media features for documents created after the call, e.g.
        ``emulate_media(prefers_reduced_motion="reduce")`` (underscores map to hyphens);
        no arguments clears the emulation. Both CSS media queries and matchMedia honor it."""
        feats = [{"name": k.replace("_", "-"), "value": v} for k, v in features.items()]
        self._cmd("Emulation.setEmulatedMedia", media="", features=feats)

    def sleep(self, seconds):
        time.sleep(seconds)

    # -- evaluation
    def evaluate(self, expr, awaitp=False):
        """Evaluate a JS expression, return the value by value (JSON-able)."""
        res = self._cmd("Runtime.evaluate", expression=expr, returnByValue=True,
                         awaitPromise=awaitp, userGesture=True)
        if "exceptionDetails" in res:
            raise RuntimeError("JS exception: " + json.dumps(res["exceptionDetails"])[:400])
        return res.get("result", {}).get("value")

    # -- native input (real hit-testing + real :hover)
    def _center(self, selector, wait=6.0):
        # scroll the element into the viewport first — native mouse events use viewport coords,
        # so an off-screen target would silently receive no click. The element is POLLED into
        # clickability (up to ``wait``s): fixed sleeps lie under parallel-suite CPU load (a click
        # racing the door's own render).
        end = time.time() + wait
        while True:
            box = self.evaluate(
                "(()=>{const e=document.querySelector(%s);if(!e)return null;"
                "e.scrollIntoView({block:'center',inline:'center',behavior:'instant'});"  # never let CSS
                "const r=e.getBoundingClientRect();"   # smooth-scroll race the coordinate read
                "return {x:r.left+r.width/2,y:r.top+r.height/2,w:r.width,h:r.height};})()"
                % json.dumps(selector))
            if box and box["w"] > 0:
                return box["x"], box["y"]
            if time.time() >= end:
                raise RuntimeError(f"element not clickable: {selector}")
            time.sleep(0.1)

    def _mouse(self, kind, x, y, buttons=0, button="none", clicks=0):
        self._cmd("Input.dispatchMouseEvent", type=kind, x=x, y=y,
                  buttons=buttons, button=button, clickCount=clicks)

    def hover(self, selector):
        """Native mouse move to the element's centre — triggers real CSS :hover."""
        x, y = self._center(selector)
        self._mouse("mouseMoved", x, y)
        self.sleep(0.05)

    def click(self, selector, settle=0.7):
        """Native press+release at the element centre (real hit-testing), then let a
        reflow/transition settle. Returns after ``settle`` seconds."""
        x, y = self._center(selector)
        self._mouse("mouseMoved", x, y)
        self._mouse("mousePressed", x, y, buttons=1, button="left", clicks=1)
        self._mouse("mouseReleased", x, y, buttons=1, button="left", clicks=1)
        self.sleep(settle)

    def wheel(self, x=None, y=None, delta_y=400):
        """A real mouse-wheel tick at (x,y) — the USER's scroll, the one an overflow lock
        must stop (programmatic scrollTo bypasses locks and is not a visitor's road)."""
        x = self.width // 2 if x is None else x
        y = self.height // 2 if y is None else y
        self._cmd("Input.dispatchMouseEvent", type="mouseWheel", x=x, y=y,
                  deltaX=0, deltaY=delta_y, buttons=0, button="none", clickCount=0)

    def click_xy(self, x, y, settle=0.7):
        self._mouse("mouseMoved", x, y)
        self._mouse("mousePressed", x, y, buttons=1, button="left", clicks=1)
        self._mouse("mouseReleased", x, y, buttons=1, button="left", clicks=1)
        self.sleep(settle)

    # -- pre-load instrumentation (a generic seam a project builds on, e.g. clipboard capture)
    def inject(self, src):
        """Run ``src`` in every document created after this call (survives navigate/reload) —
        the road for stubbing browser APIs BEFORE the page's own script wakes, e.g. capturing
        ``navigator.clipboard.writeText`` into a window array."""
        self._cmd("Page.addScriptToEvaluateOnNewDocument", source=src)

    def key(self, key, code=None):
        """Dispatch a real key press (down+up), e.g. key('Escape') or key('Tab')."""
        code = code or key
        for kind in ("rawKeyDown", "keyUp"):
            self._cmd("Input.dispatchKeyEvent", type=kind, key=key, code=code,
                      windowsVirtualKeyCode={"Tab": 9, "Escape": 27, "Enter": 13}.get(key, 0))

    def touch(self, enabled=True, points=1):
        """Emulate a touch device — flips the CSS `(hover:none)`/`(pointer:coarse)` media the
        way a real phone reports them (setEmulatedMedia alone does not). Reload to re-evaluate."""
        self._cmd("Emulation.setTouchEmulationEnabled", enabled=enabled, maxTouchPoints=points)

    def swipe(self, dy, x=None, y0=None, steps=6, settle=0.6):
        """A real one-finger swipe of `dy` px as touchStart→touchMove*→touchEnd CDP events.
        `dy` negative = the finger moves UP the screen (the walk reads that as advance forward)."""
        x = self.width // 2 if x is None else x
        y0 = self.height // 2 if y0 is None else y0
        self._cmd("Input.dispatchTouchEvent", type="touchStart", touchPoints=[{"x": x, "y": y0}])
        for i in range(1, steps + 1):
            self._cmd("Input.dispatchTouchEvent", type="touchMove",
                      touchPoints=[{"x": x, "y": y0 + dy * i / steps}])
        self._cmd("Input.dispatchTouchEvent", type="touchEnd", touchPoints=[])
        self.sleep(settle)
