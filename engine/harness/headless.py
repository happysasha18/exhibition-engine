#!/usr/bin/env python3
"""Zero-dependency headless-Chrome harness for browser-level tests (tlvphoto).

Drives a real headless Chrome over the DevTools Protocol (CDP) with nothing but the
standard library — no selenium, no playwright, no pip. It exists so the exhibition's
interaction facts (a tap reassembles the arc, a reflow is not a reload, hover highlights
without re-sorting, state persists across a reload) can be asserted in a REAL browser,
the way a visitor meets them — not string-matched in source.

Two pieces:
  * a tiny http server thread rooted at the baked ``site/`` dir, so ``/``, ``/w/<id>``
    and ``fetch()`` of the baked JSON all resolve over http (file:// would block the fetch);
  * a minimal CDP client over a raw-socket WebSocket: navigate, evaluate JS, dispatch
    NATIVE mouse events (so :hover and hit-testing are the browser's, not synthetic),
    read localStorage, set the viewport.

Chrome is located at the standard macOS path. If it is absent the harness raises
``ChromeMissing`` — the caller turns that into an EXPECTED, pinned skip (never a silent pass).

Usage (see tests/test_exhibition.py):

    from headless import serve, Browser, ChromeMissing
    with serve(site_dir) as base, Browser() as br:
        br.navigate(base + "/")
        n = br.evaluate("document.querySelectorAll('figure').length")
"""
import base64
import contextlib
import json
import os
import shutil
import socket
import struct
import subprocess
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


class ChromeMissing(Exception):
    """Chrome is not installed — the caller converts this into a pinned, expected skip."""


def chrome_available():
    return Path(CHROME).exists()


# ---------------------------------------------------------------- local http server

@contextlib.contextmanager
def serve(root):
    """Serve ``root`` over http on a free port; yields the base URL. Quiet, threaded."""
    root = str(root)

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=root, **k)

        def do_GET(self):
            # never let Chrome revalidate to a 304 — a config.json patched between reloads (the A/B
            # test) must be read fresh, not served from the browser cache.
            for h in ("If-Modified-Since", "If-None-Match"):
                if h in self.headers:
                    del self.headers[h]
            return super().do_GET()

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
    """A driven headless Chrome page. Context manager: launches on enter, kills on exit."""

    def __init__(self, width=1280, height=900):
        if not chrome_available():
            raise ChromeMissing(CHROME)
        self.width, self.height = width, height
        self._id = 0
        self._profile = tempfile.mkdtemp(prefix="tlv_cdp_")
        self.port = self._free_port()
        self.proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             "--no-default-browser-check", "--disable-extensions",
             f"--remote-debugging-port={self.port}",
             f"--user-data-dir={self._profile}",
             f"--window-size={width},{height}", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.ws = self._connect_page()
        self._cmd("Page.enable")
        self._cmd("Runtime.enable")

    # -- lifecycle
    def _free_port(self):
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        return port

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

    def close(self):
        with contextlib.suppress(Exception):
            self.ws.close()
        with contextlib.suppress(Exception):
            self.proc.terminate()
            self.proc.wait(timeout=5)
        shutil.rmtree(self._profile, ignore_errors=True)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

    # -- CDP plumbing
    def _cmd(self, method, **params):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            # else: an event — ignore (we poll for state instead of listening)

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
    def _center(self, selector):
        # scroll the element into the viewport first — native mouse events use viewport coords,
        # so an off-screen target would silently receive no click.
        box = self.evaluate(
            "(()=>{const e=document.querySelector(%s);if(!e)return null;"
            "e.scrollIntoView({block:'center',inline:'center'});"
            "const r=e.getBoundingClientRect();"
            "return {x:r.left+r.width/2,y:r.top+r.height/2,w:r.width,h:r.height};})()"
            % json.dumps(selector))
        if not box or box["w"] == 0:
            raise RuntimeError(f"element not clickable: {selector}")
        return box["x"], box["y"]

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

    def click_xy(self, x, y, settle=0.7):
        self._mouse("mouseMoved", x, y)
        self._mouse("mousePressed", x, y, buttons=1, button="left", clicks=1)
        self._mouse("mouseReleased", x, y, buttons=1, button="left", clicks=1)
        self.sleep(settle)

    # -- storage helpers
    def local_storage(self):
        return self.evaluate("JSON.stringify(window.localStorage)")

    def set_local_storage(self, key, value):
        self.evaluate("localStorage.setItem(%s,%s)" % (json.dumps(key), json.dumps(value)))

    def clear_storage(self):
        self.evaluate("localStorage.clear()")
