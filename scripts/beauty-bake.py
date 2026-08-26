#!/usr/bin/env python3
"""beauty-bake — one crossing, one file, playable by a double-click.

Root: his word 2026-08-18 09:07 — «пока ты мне не показал проход что он красивый мы это не
включаем». One crossing has to be watchable without a server, a route or a control to find.

WHAT THIS BAKES. The real built host (engine/assets/pass-layer.js) and the real built instrument
files, inlined into one HTML file together with the two photographs as data URIs and the site's own
instrument record. The host's two fetches — the record and each instrument file — are answered from
the page itself by a shim installed before the host's own script tag, so the digest weighing, the
registration and the transaction all run exactly as they do on a served site. Nothing about the
renderer is stubbed.

Run: python3 scripts/beauty-bake.py --score PATH --a PHOTO --b PHOTO --out FILE.html
"""
import argparse
import base64
import hashlib
import json
import mimetypes
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402

PAGE = ROOT / "scripts" / "beauty-page.html"


def data_uri(path):
    mime = mimetypes.guess_type(str(path))[0] or "image/jpeg"
    return "data:%s;base64,%s" % (mime, base64.b64encode(Path(path).read_bytes()).decode("ascii"))


def build():
    """The engine's own bake, into a throwaway directory: the built host, the built instrument files
    and the site's settings record, exactly as a served site carries them."""
    tmp = Path(tempfile.mkdtemp(prefix="beauty_bake_"))
    build_site.OUT = tmp
    build_site.build("https://beauty.example.com")
    return tmp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--score", required=True)
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    tmp = build()
    try:
        layer = (tmp / "pass-layer.js").read_text(encoding="utf-8")
        settings = json.loads((tmp / "config.json").read_text(encoding="utf-8"))
        rows = (settings.get("pass") or {}).get("instruments") or {}
        record = {"pass": {"instruments": {}}}
        files = {}
        for name, e in sorted(rows.items()):
            text = (tmp / e["src"]).read_text(encoding="utf-8")
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            record["pass"]["instruments"][name] = {
                "src": e["src"], "version": e["version"], "digest": digest}
            files[e["src"]] = text
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    score = json.loads(Path(args.score).read_text(encoding="utf-8"))
    page = PAGE.read_text(encoding="utf-8")
    page = page.replace("/*@@RECORD@@*/null", json.dumps(record))
    page = page.replace("/*@@FILES@@*/null", json.dumps(files))
    page = page.replace("/*@@SCORE@@*/null", json.dumps(score))
    page = page.replace("/*@@LAYER@@*/", layer)
    page = page.replace("@@IMG_A@@", data_uri(args.a))
    page = page.replace("@@IMG_B@@", data_uri(args.b))
    page = page.replace("@@TITLE@@", args.title or score.get("intent", "one crossing")[:80])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print("%s  %.1f MB" % (out, out.stat().st_size / 1e6))


if __name__ == "__main__":
    main()
