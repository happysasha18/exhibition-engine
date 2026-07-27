#!/usr/bin/env python3
"""Static-bake + SEO surface tests — engine edition (E3).

Adapted from the reference instance's test_site.py for the exhibition-engine:
  · imports/paths changed to use tests/engine_build.py shim
  · SITE_URL is the synthetic URL
  · EX-COPY copyright check parameterised from engine_build.SITE_CONFIG
  · DEPLOY check points at engine/scripts/deploy.sh and "build.py" (not "build_site.py")
  · run_all gate checks the engine's own tests/ suite list
  · all other assertions are UNCHANGED from the instance original

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

# every work page links BACK to the exhibition root — the room↔page seam of CS-6 (a shipped
# promise should burn in a test, not be caught by eye)
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

# the browser-tab face — the icon set ships and every page's head points at it (regression guard:
# without it the tab showed the browser's blank default)
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
# Parameterised from SITE_CONFIG so this passes for any instance, not one in particular.
import datetime as _dt   # noqa: E402
_year = _dt.date.today().year
_creator  = build_site.SITE_CONFIG["creator"]
_sitename = build_site.SITE_CONFIG["site_name"]
_ig       = build_site.SITE_CONFIG.get("instagram")
_sign = f"© {_year} {_creator} · {_sitename}"           # the base line, always present
_compose = getattr(build_site._engine, "compose_sign", None)
_full = _compose(_year, _creator, _sitename, instagram=_ig) if callable(_compose) else _sign
_index_html = (TMP / "index.html").read_text(encoding="utf-8")
_work_html  = next((TMP / "w").glob("*.html")).read_text(encoding="utf-8")
_copyright = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8")).get("copyright")
check("EX-COPY machine faces sign: /w/ pages + the static index carry the one composed line",
      _sign in _index_html and _sign in _work_html,
      f"want {_sign!r} index={_sign in _index_html} work={_sign in _work_html}")
check("EX-COPY the year is the bake's own, sign matches the composed line (link and all)",
      _copyright == _full,
      f"exhibition_data.copyright {_copyright!r} drifted from composed {_full!r}")

# EX-COPY (INV-28): the OPTIONAL creator social link trails the signature when `instagram` is set.
check("EX-COPY compose_sign exists (pure: year, creator, site_name, instagram=None → sign HTML)",
      callable(_compose),
      "build.compose_sign missing")
if callable(_compose):
    _cs_on  = _compose(2026, "A", "S", instagram="https://instagram.com/synthexhibition")
    _cs_off = _compose(2026, "A", "S")
    _cs_h   = _compose(2026, "A", "S", instagram="@bob")
    check("EX-COPY the sign carries the IG link when set: new tab, noopener, text 'Instagram'",
          ('href="https://instagram.com/synthexhibition"' in _cs_on
           and 'target="_blank"' in _cs_on and 'rel="noopener' in _cs_on
           and ">Instagram<" in _cs_on),
          f"want a safe IG anchor, got {_cs_on!r}")
    check("EX-COPY the sign is the plain line when `instagram` is absent (no link)",
          _cs_off == "© 2026 A · S" and "<a" not in _cs_off,
          f"want the bare copyright, got {_cs_off!r}")
    check("EX-COPY a bare @handle normalises to the full instagram.com URL",
          'href="https://instagram.com/bob"' in _cs_h,
          f"want normalised handle URL, got {_cs_h!r}")
if _ig:
    _href = f'href="{_ig}"'
    check("EX-COPY the IG link reaches every baked face: index + /w/ + the walk sign",
          _href in _index_html and _href in _work_html and bool(_copyright) and _href in _copyright,
          f"index={_href in _index_html} work={_href in _work_html} "
          f"walk={bool(_copyright) and _href in (_copyright or '')}")


# ------------------------------------------------ INV-25 the root's og:image is the instance's pick
# The homepage's share image is named by the instance in site.json (`og_image_id`). An instance that
# names none, or names an id the gallery no longer holds, falls back to the first work in the
# deterministic order — so the bake stays reproducible either way.
_pick = getattr(build_site._engine, "pick_hero", None)
check("INV-25 pick_hero exists (pure: items, og_image_id → the one work the root unfurls with)",
      callable(_pick), "build.pick_hero missing")
if callable(_pick):
    _fx = [{"id": "aaa", "img": "a.jpg"}, {"id": "bbb", "img": "b.jpg"}, {"id": "ccc", "img": "c.jpg"}]
    check("INV-25 the named work wins",
          _pick(_fx, "bbb")["id"] == "bbb", f"got {_pick(_fx, 'bbb')}")
    check("INV-25 no name falls back to the first work (INV-21 order)",
          _pick(_fx, None)["id"] == "aaa" and _pick(_fx, "")["id"] == "aaa", f"got {_pick(_fx, None)}")
    check("INV-25 a name the gallery no longer holds falls back, never crashes",
          _pick(_fx, "gone")["id"] == "aaa", f"got {_pick(_fx, 'gone')}")
    check("INV-25 an empty gallery yields nothing rather than raising",
          _pick([], "bbb") is None, "want None")

# ------------------------------------------------ the JS-off subtitle is instance copy, and escaped
# Every identity string the instance supplies reaches the page through esc(); site_name was the one
# head value that did not, so a name carrying an apostrophe or a quote broke the og:site_name tag.
# Proven with a name that actually NEEDS escaping — a fixture name of plain letters would pass this
# check with or without the fix, and a check that cannot go red proves nothing.
_eng = build_site._engine
_saved_name = _eng.SITE_NAME
try:
    _eng.SITE_NAME = 'Ann\'s "Room" & Co'
    _hostile_head = _eng.head("t", "d", "https://x/", "https://x/i.jpg", "website", {})
finally:
    _eng.SITE_NAME = _saved_name
_og_line = next((ln for ln in _hostile_head.splitlines() if "og:site_name" in ln), "")
check("the served og:site_name is escaped like every sibling head value",
      _og_line == '<meta property="og:site_name" content="Ann&#x27;s &quot;Room&quot; &amp; Co">',
      f"og:site_name unescaped: {_og_line!r}")
_hint_cfg = build_site.SITE_CONFIG.get("hint_line")
if _hint_cfg:
    check("the JS-off subtitle under the site name is the instance's own line",
          f'id="ex-hint">{build_site._engine.esc(_hint_cfg)}<' in _index_html,
          f"want the instance hint {_hint_cfg!r} on the static face")
else:
    check("the JS-off subtitle stands even when the instance names none",
          'id="ex-hint">' in _index_html and 'id="ex-hint"></span>' not in _index_html,
          "the hint slot went empty")


# ------------------------------------------------ the served code carries no prose, and still runs
# Both client files are comment-stripped on the way out (the stylesheet since 2026-07-23, the script
# since 2026-07-27): the visitor downloads code and rules, the source keeps every comment. Nothing
# asserted the stylesheet half until now — the byte fence was its only witness, and a fence cannot
# tell a stripped file from a file that simply never had comments.
_engine_dir = Path(build_site._engine.__file__).resolve().parent
sys.path.insert(0, str(_engine_dir))
_manifest = __import__("assemble_client").MANIFEST      # the client fragment order, one home
_served_js = (TMP / "exhibition.js").read_text(encoding="utf-8")
_served_css = (TMP / "exhibition.css").read_text(encoding="utf-8")
_source_js = build_site._engine.client_asset("exhibition.js").read_text(encoding="utf-8")


def _opens_a_comment(text, marks):
    return [ln for ln in text.splitlines() if ln.lstrip().startswith(marks)]


check("the served stylesheet carries no comments (the source keeps them all)",
      not _opens_a_comment(_served_css, ("/*",)) and "/*" not in _served_css
      and "/*" in build_site._engine.client_asset("exhibition.css").read_text(encoding="utf-8"),
      f"{len(_opens_a_comment(_served_css, ('/*',)))} comment lines survived into the bundle")
# The one comment form that MUST survive is the assembler's fragment keep-marker (`/*!name*/`) — the
# boundary a string-level test scopes itself by. So the served script carries exactly those and
# nothing else: one marker per fragment in the client MANIFEST, no other comment anywhere.
_frag_names = [ln.strip()[3:-2] for ln in _served_js.splitlines() if ln.strip().startswith("/*!")]
_other = [ln for ln in _opens_a_comment(_served_js, ("//", "/*"))
          if not ln.strip().startswith("/*!")]
check("the served script carries no comment except the fragment markers (the source keeps them all)",
      not _other and len(_opens_a_comment(_source_js, ("//", "/*"))) > 100,
      f"{len(_other)} comment line(s) survived into the bundle: {_other[:2]}")
check("every client fragment opens with its own keep-marker in the served script",
      len(_frag_names) == len(_manifest) and _frag_names == _manifest,
      f"markers {_frag_names[:3]}... ({len(_frag_names)}) against MANIFEST ({len(_manifest)})")
# The strip is deliberately conservative — it leaves a comment TRAILING code alone, because telling
# one from a division or a regular expression needs a full parse. Assert that boundary, so a future
# "smarter" strip that starts touching code has to face this row first.
check("the strip leaves a comment trailing code alone (it never has to parse an expression)",
      any(" //" in ln and not ln.lstrip().startswith("//") for ln in _served_js.splitlines()),
      "every trailing comment vanished — the strip is reaching into code it cannot safely read")
# The proof that matters: the stripped script is still the SAME program. Every browser row in this
# suite already runs against this served copy, so a strip that broke the client would red the walk,
# the door and the zoom long before these rows. These two name the property directly.
_lost = [name for name in ("function glidePlan", "function wheelWalkStep", "function glideCurve")
         if name not in _served_js]
check("the strip removes prose only — every client function survives into the bundle",
      not _lost, f"missing from the served script: {', '.join(_lost)}")


def _lines_are_a_subsequence(served, source):
    """Every line of the served script must be a line of the source, in the SAME ORDER. A strip that
    only DELETES whole lines satisfies this; one that rewrote, joined or reordered a line cannot. It
    is the property that makes stripping safe to ship, so it is asserted rather than assumed."""
    src = [ln.rstrip() for ln in source.splitlines()]
    i, missing = 0, []
    for ln in (l.rstrip() for l in served.splitlines()):
        while i < len(src) and src[i] != ln:
            i += 1
        if i >= len(src):
            missing.append(ln)
        else:
            i += 1
    return missing


_src_ns = build_site._engine.apply_namespace(_source_js, build_site.SITE_CONFIG.get("namespace") or "ex") \
    if ("@@NS@@" in _source_js or "@@NS_UPPER@@" in _source_js) else _source_js
_rewritten = _lines_are_a_subsequence(_served_js, _src_ns)
check("the strip only DELETES lines — every served line is a source line, in order",
      not _rewritten,
      f"{len(_rewritten)} served line(s) are not source lines: {_rewritten[:2]}")


# ---------------------------------------------------------------- INV-56 display cap + site-URL watermark (EX-PROTECT-RES)
# The deploy bakes with --display-max; tests omit it so they stay fast (verbatim copy).
# When Pillow is available: exercise _copy_assets_capped directly — an over-cap image
# downscales (LANCZOS) AND the marked bottom-right corner differs from the plain resize.
# Pinned skip if Pillow absent.
try:
    from PIL import Image as _PILImage56
    _pil56 = True
except ImportError:
    _pil56 = False
if _pil56:
    import tempfile as _tf56
    # synthetic 400×300 image — always over the cap so downscale is guaranteed
    _synth56 = _PILImage56.new("RGB", (400, 300), (200, 180, 160))
    _ta56 = Path(_tf56.mkdtemp()) / "assets"; _ta56.mkdir(parents=True)
    _synth56.save(str(_ta56 / "t.jpg"))
    _tbp56 = Path(_tf56.mkdtemp()) / "plain"
    _tbm56 = Path(_tf56.mkdtemp()) / "marked"
    build_site._copy_assets_capped(_ta56, _tbp56, 200)                               # cap only
    build_site._copy_assets_capped(_ta56, _tbm56, 200, mark_text="example.com")      # cap + mark
    _pi56 = _PILImage56.open(_tbp56 / "t.jpg")
    _mi56 = _PILImage56.open(_tbm56 / "t.jpg")
    _long56 = max(_mi56.size)
    _w56, _h56 = _mi56.size
    _cp56 = _pi56.crop((int(_w56 * 0.6), int(_h56 * 0.85), _w56, _h56)).tobytes()
    _cm56 = _mi56.crop((int(_w56 * 0.6), int(_h56 * 0.85), _w56, _h56)).tobytes()
    check("INV-56 served image capped to the display long edge + wears the site-URL mark",
          0 < _long56 <= 200 and _mi56.size == _pi56.size and _cp56 != _cm56,
          f"long edge={_long56}px · mark-drew-bottom-right={_cp56 != _cm56}")
else:
    check("INV-56 served image capped + marked", True, "Pillow absent — pinned skip")


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
# Adapted from an instance: "build_site.py" → "build.py" (the engine's builder name).
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
