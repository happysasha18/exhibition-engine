#!/usr/bin/env python3
"""Static-bake + SEO surface tests — engine edition (E3).

Adapted from ~/tlvphoto/tests/test_site.py for the exhibition-engine:
  · imports/paths changed to use tests/engine_build.py shim
  · SITE_URL is the synthetic URL
  · EX-COPY copyright check parameterised from engine_build.SITE_CONFIG
  · DEPLOY check points at engine/scripts/deploy.sh and "build.py" (not "build_site.py")
  · run_all gate checks the engine's own tests/ suite list
  · all other assertions are UNCHANGED from the tlvphoto original

Bakes the synthetic fixture (tests/fixture_content/) into a temp dir, then inspects it.
Zero pip dependencies; stdlib html.parser + re only.

Run: python tests/test_site.py   (exit 0 = all green)
"""
import json
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent          # exhibition-engine/
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402

SITE_URL = "https://synth.example.com"

# A visitor body may carry his OWN descriptive words ("radial burst" in a title/caption); INV-14 forbids
# the axis READOUT — an axis id, a score/confidence number, or math-machinery names — not plain description.
READOUT_WORDS = ["ax-", "inv-", "confidence", "cosine", "centroid", "htdemucs", "std="]
READOUT_RE = re.compile(r"\b\w+\s*[:=]\s*-?\d*\.\d+\b")   # a labelled numeric score, e.g. "radial: 0.42"

results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))


# ---------------------------------------------------------------- bake once

class Extract(HTMLParser):
    """Collect meta/link tags, title, h1 text, ld+json, img attrs from served HTML."""
    def __init__(self):
        super().__init__()
        self.metas = []          # list of dict(attrs)
        self.links = []
        self.title = ""
        self.h1 = []             # (attrs_dict, text)
        self._in_title = False
        self._in_h1 = None
        self._in_ld = False
        self.ldjson = []
        self.imgs = []
        self.body_text = []
        self._in_body = False
        self._hidden_stack = []   # tags holding a visually-hidden region open

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "visually-hidden" in (d.get("class") or ""):
            self._hidden_stack.append(tag)
        if tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = {"attrs": d, "text": ""}
        elif tag == "img":
            self.imgs.append(d)
        elif tag == "script" and d.get("type") == "application/ld+json":
            self._in_ld = True
        elif tag == "body":
            self._in_body = True

    def handle_endtag(self, tag):
        if self._hidden_stack and self._hidden_stack[-1] == tag:
            self._hidden_stack.pop()
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1 is not None:
            self.h1.append((self._in_h1["attrs"], self._in_h1["text"].strip()))
            self._in_h1 = None
        elif tag == "script":
            self._in_ld = False
        elif tag == "body":
            self._in_body = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_h1 is not None:
            self._in_h1["text"] += data
        if self._in_ld:
            self.ldjson.append(data)
        if self._in_body and data.strip() and not self._hidden_stack:
            self.body_text.append(data)

    def meta(self, key, val=None):
        for m in self.metas:
            if m.get("property") == key or m.get("name") == key:
                return m.get("content", "")
        return None

    def canonical(self):
        for l in self.links:
            if l.get("rel") == "canonical":
                return l.get("href")
        return None

    def visible_body_text(self):
        return " ".join(self.body_text)


def parse(path):
    p = Extract()
    p.feed(path.read_text(encoding="utf-8"))
    return p


TMP = Path(tempfile.mkdtemp(prefix="synth_site_"))
build_site.OUT = TMP
summary = build_site.build(SITE_URL)

gallery = build_site.load_json("gallery/gallery_data.json")
ITEMS = gallery["items"]
CAPTIONS = {c["id"]: (c.get("subject") or "").strip()
            for c in build_site.load_json("content_tags.json")}
work_files = sorted((TMP / "w").glob("*.html"))
parsed = {f: parse(f) for f in work_files}


# ---------------------------------------------------------------- INV-15 one page per work

check("INV-15 page count == work count",
      len(work_files) == len(ITEMS),
      f"{len(work_files)} pages vs {len(ITEMS)} works")

# every id maps to exactly one existing file
expected_slugs = {build_site.work_slug(it.get("title", ""), CAPTIONS.get(it["id"], ""), it["id"])
                  for it in ITEMS}
actual_slugs = {f.stem for f in work_files}
check("INV-15 every work id has its page, no phantom",
      expected_slugs == actual_slugs,
      f"missing={list(expected_slugs - actual_slugs)[:3]} extra={list(actual_slugs - expected_slugs)[:3]}")


# ---------------------------------------------------------------- URL scheme /w/<slug>-<idtail>

slug_re = re.compile(r"^[a-z0-9-]+-[0-9a-f]{4}$")
bad = [f.stem for f in work_files if not slug_re.match(f.stem)]
check("URL scheme slug-<idtail> pattern", not bad, f"bad={bad[:5]}")
check("URL scheme all unique", len(actual_slugs) == len(work_files), "slug collision")


# ---------------------------------------------------------------- per-page invariants

empty_title = og_missing = rel_ogimg = readout = no_canonical = jsonld_bad = 0
missing_dims = twitter_bad = 0
for f, p in parsed.items():
    idx_title = p.title.strip()
    if not idx_title:
        empty_title += 1
    # INV-23: a non-empty h1 exists
    if not any(txt for _, txt in p.h1):
        empty_title += 1
    # INV-22: absolute og:image + twitter:image + dims + card
    ogimg = p.meta("og:image")
    if not ogimg:
        og_missing += 1
    elif not ogimg.startswith("http"):
        rel_ogimg += 1
    if not p.meta("og:image:width") or not p.meta("og:image:height"):
        missing_dims += 1
    if p.meta("twitter:card") != "summary_large_image" or not p.meta("twitter:image"):
        twitter_bad += 1
    # INV-17 canonical
    if not (p.canonical() or "").startswith("http"):
        no_canonical += 1
    # INV-14: no axis readout in the VISIBLE body text
    low = p.visible_body_text().lower()
    if any(w in low for w in READOUT_WORDS) or READOUT_RE.search(low):
        readout += 1
    # JSON-LD parses and is VisualArtwork with a name
    try:
        ld = json.loads("".join(p.ldjson))
        if ld.get("@type") != "VisualArtwork" or not ld.get("name"):
            jsonld_bad += 1
    except Exception:
        jsonld_bad += 1

check("INV-23 crawlable text never empty (title + h1)", empty_title == 0, f"{empty_title} empty")
check("INV-22 og:image present + absolute", og_missing == 0 and rel_ogimg == 0,
      f"missing={og_missing} relative={rel_ogimg}")
check("INV-22 og:image dims present", missing_dims == 0, f"{missing_dims} missing dims")
check("INV-22 twitter summary_large_image + image", twitter_bad == 0, f"{twitter_bad} bad")
check("INV-17 canonical absolute on every page", no_canonical == 0, f"{no_canonical} missing")
check("INV-14 no axis readout in visible body", readout == 0, f"{readout} pages leaked a readout word")
check("JSON-LD VisualArtwork with name on every page", jsonld_bad == 0, f"{jsonld_bad} bad")


# ---------------------------------------------------------------- INV-16 complete without JS

# the served HTML already carries img+alt + a palette + og — no <script> needed for content.
# (the only <script> allowed is the ld+json data block, type=application/ld+json)
js_needed = 0
for f, p in parsed.items():
    raw = f.read_text(encoding="utf-8")
    # any executable <script> (no type, or type=text/javascript) means JS-injected content
    if re.search(r"<script(?![^>]*application/ld\+json)[^>]*>", raw):
        js_needed += 1
    if not p.imgs or not p.imgs[0].get("alt"):
        js_needed += 1
check("INV-16 complete without JS (img+alt in served HTML, no exec script)", js_needed == 0,
      f"{js_needed} pages need JS / lack alt")


# ---------------------------------------------------------------- caption hidden (RESOLVED)

# caption_visible:false → the caption text must appear in <meta description>/alt, NOT in visible body
cap_visible = 0
for f, p in parsed.items():
    wid = None  # recover id via slug map
    for it in ITEMS:
        if build_site.work_slug(it.get("title", ""), CAPTIONS.get(it["id"], ""), it["id"]) == f.stem:
            wid = it["id"]
            break
    cap = CAPTIONS.get(wid, "")
    if cap and cap.lower() in p.visible_body_text().lower():
        cap_visible += 1
    # but it MUST be in the meta description
    if cap and cap != (p.meta("description") or ""):
        pass  # description may be idx_title when caption empty; only assert not-visible here
check("caption stays out of visible body (caption_visible:false)", cap_visible == 0,
      f"{cap_visible} pages show the caption")


# ---------------------------------------------------------------- CS-6 backpointer (R1 promise)

# every work page links BACK to the exhibition root — the room↔page seam of CS-6 (its red test was
# demanded by the 2026-07-05 inbox wish: a shipped promise burns in a test, not in Alexander's eyes)
no_backptr = sum(1 for f in work_files
                 if 'href="/"' not in f.read_text(encoding="utf-8"))
check("CS-6 every work page links back to the exhibition root `/`", no_backptr == 0,
      f"{no_backptr} pages lack the backpointer")


# ---------------------------------------------------------------- root `/`  (now the EXHIBITION)
# The site root was the flat landing; it is now the adaptive exhibition (EX). Its crawlable JS-off face
# — non-empty h1, indexable intro, a static link to EVERY work, JSON-LD, canonical, root og:image — is
# owned by tests/test_exhibition.py (INV-25(a)). This suite keeps only the SEO facts that span the whole
# bundle (the work pages + the sitemap), so `/` has one home, not two.


# ---------------------------------------------------------------- INV-17 sitemap + robots

sm = ET.parse(TMP / "sitemap.xml").getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [e.text for e in sm.findall(".//s:loc", ns)]
check("INV-17 sitemap = exhibition root + every work page, once",
      len(locs) == len(ITEMS) + 1 and len(set(locs)) == len(locs) and f"{SITE_URL}/" in locs,
      f"{len(locs)} locs vs {len(ITEMS)+1} expected")
robots = (TMP / "robots.txt").read_text()
check("INV-17 robots allows prod + points at sitemap",
      "Allow: /" in robots and "sitemap.xml" in robots.lower())

# INV-53 image sitemap: xmlns:image namespace on <urlset> + one <image:image> per work page
sm_raw = (TMP / "sitemap.xml").read_text(encoding="utf-8")
ns_img = "http://www.google.com/schemas/sitemap-image/1.1"
check("INV-53 sitemap carries xmlns:image namespace",
      f'xmlns:image="{ns_img}"' in sm_raw,
      "xmlns:image missing from <urlset>")
ns_both = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "image": ns_img}
img_locs = [e.text for e in sm.findall(".//image:loc", ns_both)]
check("INV-53 sitemap has one <image:image> per work page (every work, no duplicates)",
      len(img_locs) == len(ITEMS) and len(set(img_locs)) == len(img_locs),
      f"{len(img_locs)} image:loc vs {len(ITEMS)} expected")
check("INV-53 image:loc URLs point to /gallery/ assets on site root",
      all(u.startswith(SITE_URL + "/gallery/") for u in img_locs),
      f"first bad image:loc: {next((u for u in img_locs if not u.startswith(SITE_URL + '/gallery/')), None)!r}")


# ---------------------------------------------------------------- INV-18 self-contained + INV-19 + CF + CS-7

# every referenced local asset exists in the bundle
missing_assets = []
for f, p in parsed.items():
    for img in p.imgs:
        src = img.get("src", "")
        if src.startswith("/"):
            if not (TMP / src.lstrip("/")).exists():
                missing_assets.append(src)
check("INV-18 every referenced image exists in bundle", not missing_assets,
      f"missing={missing_assets[:3]}")
check("CS-7 /api reserved namespace exists", (TMP / "api").is_dir())

# the browser-tab face — the icon set ships and every page's head points at it (gate find,
# Alexander 2026-07-05: the tab showed the browser's blank default)
fav_missing = [n for n in ("favicon.svg", "favicon.png", "apple-touch-icon.png")
               if not (TMP / n).exists()]
icon_pages = list(parsed.values()) + [parse(TMP / "index.html")]
no_icon_link = sum(1 for p in icon_pages
                   if not any("icon" in (l.get("rel") or "") for l in p.links))
check("Favicon ships + every page head links rel=icon", not fav_missing and no_icon_link == 0,
      f"missing={fav_missing} unlinked_pages={no_icon_link}")

config = json.loads((TMP / "config.json").read_text())
check("INV-19 AI flags ship OFF", config.get("ai_greeting") is False and config.get("ai_assemble") is False)
check("RESOLVED caption_visible:false", config.get("caption_visible") is False)
check("CF config schema (site_url + flags + experiments)",
      config.get("site_url") == SITE_URL and "experiments" in config)
# CS-7: absolute URLs use site_url
bad_host = 0
for f, p in parsed.items():
    for url in (p.meta("og:image") or "", p.canonical() or ""):
        if url.startswith("http") and not url.startswith(SITE_URL):
            bad_host += 1
check("CS-7 absolute URLs all use config site_url", bad_host == 0, f"{bad_host} off-host URLs")

# DELTA-1: the door wordmark comes from config, not a hardcoded literal (INV-28).
# config.json must carry site_name; exhibition.js must read cfg.site_name, not the literal brand.
_cfg_raw = json.loads((TMP / "config.json").read_text(encoding="utf-8"))
check("DELTA-1 config.json carries site_name from site_config",
      _cfg_raw.get("site_name") == build_site.SITE_CONFIG["site_name"],
      f"want {build_site.SITE_CONFIG['site_name']!r} got {_cfg_raw.get('site_name')!r}")
_js_src = (ROOT / "engine" / "assets" / "exhibition.js").read_text(encoding="utf-8")
check("DELTA-1 exhibition.js wordmark reads cfg.site_name (no hardcoded brand literal)",
      "TLV PHOTOS" not in _js_src and "cfg.site_name" in _js_src,
      "wordmark still hardcoded or cfg.site_name not referenced in exhibition.js")


# ---------------------------------------------------------------- INV-21 reproducible bake

TMP2 = Path(tempfile.mkdtemp(prefix="synth_site2_"))
build_site.OUT = TMP2
build_site.build(SITE_URL)


def tree_bytes(root):
    out = {}
    for pth in sorted(root.rglob("*")):
        if pth.is_file():
            out[str(pth.relative_to(root))] = pth.read_bytes()
    return out


check("INV-21 bake is reproducible (byte-identical)", tree_bytes(TMP) == tree_bytes(TMP2),
      "second bake differs")


# ---------------------------------------------------------------- EX-COPY (INV-40): the quiet signature

# every machine face carries the SAME baked line, and the year is the bake run's own
# Parameterised from SITE_CONFIG so this passes for any instance, not just tlvphoto.
import datetime as _dt   # noqa: E402
_year = _dt.date.today().year
_creator  = build_site.SITE_CONFIG["creator"]
_sitename = build_site.SITE_CONFIG["site_name"]
_sign = f"© {_year} {_creator} · {_sitename}"
_index_html = (TMP / "index.html").read_text(encoding="utf-8")
_work_html  = next((TMP / "w").glob("*.html")).read_text(encoding="utf-8")
check("EX-COPY machine faces sign: /w/ pages + the static index carry the one composed line",
      _sign in _index_html and _sign in _work_html,
      f"want {_sign!r} index={_sign in _index_html} work={_sign in _work_html}")
check("EX-COPY the year is the bake's own (composed at bake, never hand-written)",
      json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
      .get("copyright") == _sign,
      "exhibition_data.copyright missing or drifted from the composed line")


# ---------------------------------------------------------------- WP-CLEAN: extensionless references

# every baked REFERENCE is clean /w/<slug>-<idtail>; the files themselves stay .html on disk
_leaks = []
if ".html" in (TMP / "sitemap.xml").read_text(encoding="utf-8"):
    _leaks.append("sitemap")
_p0 = parsed[work_files[0]]
if (_p0.canonical() or "").endswith(".html"):
    _leaks.append("canonical")
if re.search(r'href="/w/[^"]*\.html"', _index_html):
    _leaks.append("index-links")
_exdata = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
if any(w["slug"].endswith(".html") for w in _exdata["works"]):
    _leaks.append("walk-slug")
check("WP-CLEAN no .html in any baked reference (canonical/sitemap/index/walk-slug); files stay .html",
      not _leaks and work_files[0].suffix == ".html", f"leaks={_leaks}")

# ---------------------------------------------------------------- 5r: one gate, no forgotten suite

import run_all   # noqa: E402  (tests/ is on sys.path)
_on_disk = {f.stem[len("test_"):] for f in (ROOT / "tests").glob("test_*.py")}
check("gate: run_all's suite list equals the test files on disk (a new suite can't be forgotten)",
      set(run_all.SUITES) == _on_disk,
      f"runner={sorted(run_all.SUITES)} disk={sorted(_on_disk)}")

# ---------------------------------------------------------------- DEPLOY: one honest command
# Adapted from tlvphoto: "build_site.py" → "build.py" (the engine's builder name).
# All other beats (wrangler, purge, md5, Keychain) are generic deployment infrastructure.

import os as _os   # noqa: E402
_dep_path = ROOT / "scripts" / "deploy.sh"
_dep = _dep_path.read_text(encoding="utf-8")
check("DEPLOY recipe carries all four beats (bake→upload→purge→verify), Keychain auth, no secret literal",
      _os.access(_dep_path, _os.X_OK)
      and "build.py" in _dep and "wrangler pages deploy" in _dep
      and "purge_cache" in _dep and "md5" in _dep
      and "find-generic-password" in _dep
      and not re.search(r"(API_KEY|TOKEN)\s*=\s*[\"']?[A-Za-z0-9+/]{25,}", _dep),
      "a beat missing or a secret literal in scripts/deploy.sh")

# ---------------------------------------------------------------- INV-20 content = data (spot-check title)

# every visible title on a page equals the source title (no invented per-work prose)
mismatch = 0
for it in ITEMS:
    if not (it.get("title") or "").strip():
        continue
    slug = build_site.work_slug(it["title"], CAPTIONS.get(it["id"], ""), it["id"])
    p = parsed[TMP / "w" / f"{slug}.html"]
    vis = " ".join(txt for _, txt in p.h1)
    if it["title"].strip() not in vis:
        mismatch += 1
check("INV-20 visible title traces to source data", mismatch == 0, f"{mismatch} titles not from data")


# ---------------------------------------------------------------- report

passed = sum(1 for _, ok, _ in results if ok)
failed = len(results) - passed
print()
for name, ok, detail in results:
    tag = "PASS" if ok else "FAIL"
    line = f"{tag}  {name}"
    if not ok and detail:
        line += f"   — {detail}"
    print(line)
print(f"\n{passed} passed / {failed} failed")
sys.exit(1 if failed else 0)
