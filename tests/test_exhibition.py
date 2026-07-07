#!/usr/bin/env python3
"""Adaptive exhibition (EX) tests — adapted for exhibition-engine synthetic fixture.
One test per TEST_MATRIX "Adaptive exhibition" row.

Run: python tests/test_exhibition.py   (exit 0 = all green)
"""
import json
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"

AXIS_ID_RE = re.compile(r"\b(?:ax|inv)-\d")
READOUT_WORDS = ["confidence", "cosine", "centroid", "kinship distance", "numeric axis"]
READOUT_RE = re.compile(r"\b\w+\s*[:=]\s*-?\d*\.\d+\b")
TS_FORBIDDEN = ["data-story", "reveal story", "reveal-story", "told-story", "told story", "narrative"]

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


# ---------------------------------------------------------------- bake once

TMP = Path(tempfile.mkdtemp(prefix="synth_ex_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

INDEX = TMP / "index.html"
EXDATA = json.loads((TMP / "exhibition_data.json").read_text())
WORKS = EXDATA["works"]
VEC = EXDATA["v"]
CONFIG_PATH = TMP / "config.json"
CONFIG0 = CONFIG_PATH.read_text()
EXCFG = json.loads(CONFIG0)["exhibition"]
SPREAD = EXCFG["spread_size"]
UNFOLD = EXCFG["unfold_step"]


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def nearest_ids(pick_id, k):
    others = [w["id"] for w in WORKS if w["id"] != pick_id]
    others.sort(key=lambda i: dist(VEC[i], VEC[pick_id]))
    return others[:k]


# ---------------------------------------------------------------- HTML parse

class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.metas, self.links, self.h1, self.imgs, self.anchors = [], [], [], [], []
        self.title = ""
        self._in_title = False
        self._in_h1 = None
        self._in_ld = False
        self.ldjson = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)
        elif tag == "a":
            self.anchors.append(d)
        elif tag == "img":
            self.imgs.append(d)
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = {"attrs": d, "text": ""}
        elif tag == "script" and d.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1 is not None:
            self.h1.append(self._in_h1["text"].strip())
            self._in_h1 = None
        elif tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1 is not None:
            self._in_h1["text"] += data
        if self._in_ld:
            self.ldjson.append(data)

    def meta(self, key):
        for m in self.metas:
            if m.get("property") == key or m.get("name") == key:
                return m.get("content", "")
        return None

    def canonical(self):
        for l in self.links:
            if l.get("rel") == "canonical":
                return l.get("href")
        return None


P = Extract()
P.feed(INDEX.read_text(encoding="utf-8"))
INDEX_RAW = INDEX.read_text(encoding="utf-8")


# ================================================================ STATIC rows

work_links = [a["href"] for a in P.anchors if (a.get("href") or "").startswith("/w/")]
work_ids_linked = len(work_links)
try:
    ld = json.loads("".join(P.ldjson))
    ld_types = json.dumps(ld)
    has_ld = ("WebSite" in ld_types) or ("CollectionPage" in ld_types)
except Exception:
    has_ld = False
og_image = P.meta("og:image") or ""
check("INV-25(a) JS-off crawlable face (h1+intro+all work links+JSON-LD+abs og:image+canonical)",
      bool(P.h1 and P.h1[0])
      and work_ids_linked == len(WORKS)
      and has_ld
      and og_image.startswith("http")
      and bool(P.meta("og:title"))
      and (P.canonical() or "").startswith("http"),
      f"h1={P.h1[:1]} links={work_ids_linked}/{len(WORKS)} ld={has_ld} ogimg={og_image[:40]}")

sm = ET.parse(TMP / "sitemap.xml").getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [e.text for e in sm.findall(".//s:loc", ns)]
robots = (TMP / "robots.txt").read_text().lower()
check("INV-24 sitemap lists exhibition root `/` exactly once + robots→sitemap",
      locs.count(f"{SITE_URL}/") == 1 and "sitemap.xml" in robots,
      f"root count={locs.count(f'{SITE_URL}/')}")

low_raw = INDEX_RAW.lower()
js_raw = (TMP / "exhibition.js").read_text().lower()
check("TS deferred — no told-story control in exhibition (html + client js)",
      not any(t in low_raw for t in TS_FORBIDDEN) and not any(t in js_raw for t in TS_FORBIDDEN),
      f"hits={[t for t in TS_FORBIDDEN if t in low_raw or t in js_raw]}")

attr_vals = " ".join(v or "" for a in (P.anchors + P.imgs + P.metas) for v in a.values()).lower()
data_star = re.findall(r'data-[a-z-]+="([^"]*)"', INDEX_RAW)
vector_in_dom = any(re.search(r"\d+\.\d+.*\d+\.\d+", d) for d in data_star)
readout = (AXIS_ID_RE.search(low_raw) or any(w in low_raw for w in READOUT_WORDS)
           or READOUT_RE.search(attr_vals) or vector_in_dom)
check("INV-1 on EX — no axis name/score/confidence in served exhibition HTML/attrs/data-*",
      not readout,
      f"axis_id={bool(AXIS_ID_RE.search(low_raw))} words={[w for w in READOUT_WORDS if w in low_raw]} vec_in_data={vector_in_dom}")


# ================================================================ BROWSER rows

BROWSER_ROWS = [
    "INV-25(b) JS-on live face arrives — cold visitor meets the DOOR, static hidden",
    "EX-ALL tombstone — no full-dump control; static index stays hidden while live",
    "INV-25 FOUC guard — pre-paint hide in head + css rule + static hidden while live",
    "INV-1 on EX live DOM — caption speaks his words only, no axis readout",
    "INV-25/CS-8 broken walk data → static face returns, never a blank page",
]

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base, Browser(width=1280, height=900) as br:
        br.navigate(base + "/")
        br.clear_storage()
        br.evaluate("localStorage.setItem('tlv-tempo','0.05')")
        br.reload(); br.sleep(1.0)
        st = br.evaluate(
            "(()=>{return {live:document.body.classList.contains('ex-live'),"
            "door:document.body.classList.contains('ex-door'),"
            "staticShown:getComputedStyle(document.getElementById('ex-static')).display!=='none'};})()")
        check(BROWSER_ROWS[0], st["live"] and st["door"] and not st["staticShown"], f"{st}")

        br.click(".exd-window:nth-child(1)", settle=1.0)
        tomb = br.evaluate(
            "(()=>{return {allBtn:!!document.getElementById('ex-all'),"
            "live:document.body.classList.contains('ex-live'),"
            "staticShown:getComputedStyle(document.getElementById('ex-static')).display!=='none'};})()")
        check(BROWSER_ROWS[1], not tomb["allBtn"] and tomb["live"] and not tomb["staticShown"], f"{tomb}")

        raw_head = INDEX_RAW.split("</head>")[0]
        guard_in_head = ('classList.add("js")' in raw_head)
        css_rule = "html.js #ex-static" in (TMP / "exhibition.css").read_text()
        check(BROWSER_ROWS[2], guard_in_head and css_rule and not tomb["staticShown"],
              f"head_guard={guard_in_head} css_rule={css_rule} hidden_live={not tomb['staticShown']}")

        br.evaluate("document.querySelectorAll('.exh-frame')[1].scrollIntoView()")
        br.sleep(0.6)
        live_text = br.evaluate("document.body.innerText") or ""
        cap_ok = br.evaluate(
            "(()=>{const c=document.getElementById('exh-cap');if(!c)return false;"
            "const t=c.querySelector('.title');return !!t && t.textContent.trim().length>0;})()")
        low = live_text.lower()
        check(BROWSER_ROWS[3],
              cap_ok and not AXIS_ID_RE.search(low)
              and not any(w in low for w in READOUT_WORDS) and not READOUT_RE.search(low),
              f"cap={cap_ok} axis_id={bool(AXIS_ID_RE.search(low))}")

    BROKEN = Path(tempfile.mkdtemp(prefix="synth_ex_broken_"))
    import shutil as _sh
    _sh.copytree(TMP, BROKEN, dirs_exist_ok=True)
    (BROKEN / "exhibition_data.json").unlink()
    with serve(BROKEN) as base2, Browser(width=1280, height=900) as br2:
        br2.navigate(base2 + "/")
        br2.sleep(3.0)
        rec = br2.evaluate(
            "(()=>{return {live:document.body.classList.contains('ex-live'),"
            "staticShown:getComputedStyle(document.getElementById('ex-static')).display!=='none',"
            "links:document.querySelectorAll('#ex-static a[href^=\"/w/\"]').length};})()")
        check(BROWSER_ROWS[4],
              not rec["live"] and rec["staticShown"] and rec["links"] == len(WORKS), f"{rec}")


# ---------------------------------------------------------------- report

import shutil
shutil.rmtree(TMP, ignore_errors=True)
try:
    shutil.rmtree(BROKEN, ignore_errors=True)
except NameError:
    pass

passed = sum(1 for _, s, _ in results if s == "PASS")
failed = sum(1 for _, s, _ in results if s == "FAIL")
skipped = sum(1 for _, s, _ in results if s == "SKIP")
print()
for name, status, detail in results:
    line = f"{status}  {name}"
    if status != "PASS" and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed / {skipped} skipped")
sys.exit(1 if failed else 0)
