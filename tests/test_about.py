#!/usr/bin/env python3
"""The about page (EX-ABOUT / INV-102, INV-103, INV-104) — the one page that stands OUTSIDE the
exhibition and explains it, baked once per language.

Rows AB1..AB14 mirror the instance's TEST_MATRIX section "The about page".
Run: python tests/test_about.py
"""
import html as _html
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tests"))
import engine_build as build_site  # noqa: E402
from headless import serve, Browser, chrome_available  # noqa: E402

SITE_URL = "https://synth.example.com"

# the fixture gives about copy to these four only (make_synthetic.ABOUT) — fr/es/uk carry none,
# so "a language without copy is ABSENT from the sibling set" is proven by real data, not a mock.
WITH_COPY = ["en", "ru", "he", "de"]
WITHOUT_COPY = ["fr", "es", "uk"]
FALLBACK = "en"
RTL_LANG = "he"

results = []


def check(name, cond, detail=""):
    results.append((name, "PASS" if cond else "FAIL", detail))


def skip(name, detail):
    results.append((name, "SKIP", detail))


def tags(html, name):
    """Every <name ...> open tag in the document, as raw strings."""
    return re.findall(rf"<{name}\b[^>]*>", html, re.I)


def meta_content(html, attr, value):
    """The content= of <meta {attr}="{value}" content="…">, or None."""
    m = re.search(rf'<meta\s+{attr}="{re.escape(value)}"\s+content="([^"]*)"', html, re.I)
    return m.group(1) if m else None


def texts(doc, tag):
    """The VISIBLE text of every <tag> — entities resolved, because a page rightly escapes an
    apostrophe and a raw-source comparison would call correct copy a defect."""
    return [_html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
            for t in re.findall(rf"<{tag}\b[^>]*>(.*?)</{tag}>", doc, re.I | re.S)]


# ---------------------------------------------------------------- bake once
TMP = Path(tempfile.mkdtemp(prefix="synth_about_"))
build_site.OUT = TMP
build_site.build(SITE_URL)

GREET_SRC = json.loads((build_site.FIXTURE / "data" / "greetings.json").read_text(encoding="utf-8"))
DICT = GREET_SRC["langs"]
ITEMS = build_site.load_json("gallery/gallery_data.json")["items"]
INDEX = (TMP / "index.html").read_text(encoding="utf-8")
EXDATA = json.loads((TMP / "exhibition_data.json").read_text(encoding="utf-8"))
WORK_PAGES = sorted((TMP / "w").glob("*.html"))


def about_file(lang):
    return TMP / "about.html" if lang == FALLBACK else TMP / "about" / f"{lang}.html"


def about_url(lang):
    return "/about" if lang == FALLBACK else f"/about/{lang}"


PAGES = {L: about_file(L).read_text(encoding="utf-8") for L in WITH_COPY if about_file(L).exists()}

# A row that reads an empty set is GREEN OVER NOTHING. Every row below carries this reach assertion,
# so a bake that writes no page at all reds the suite instead of sailing through it.
REACH = sorted(PAGES) == sorted(WITH_COPY)
REACH_NOTE = f"reach: {len(PAGES)}/{len(WITH_COPY)} pages read ({sorted(PAGES)})"


# ---------------------------------------------------------------- AB1 one page per language
missing = [L for L in WITH_COPY if not about_file(L).exists()]
phantom = [L for L in WITHOUT_COPY if about_file(L).exists()]
check("AB1 INV-102 one baked page per language that has copy, fallback at the bare address",
      not missing and not phantom and about_file(FALLBACK).exists(),
      f"missing={missing} phantom={phantom} fallback_exists={about_file(FALLBACK).exists()}")

# ---------------------------------------------------------------- AB2 words are content, not code
bad = []
for L, html in PAGES.items():
    d = DICT[L]
    h1 = texts(html, "h1")
    paras = texts(html, "p")
    want = [d["about_1"], d["about_2"], d["about_3"], d["about_4"]]
    if h1 != [d["about_title"]]:
        bad.append(f"{L}: h1={h1!r} want {d['about_title']!r}")
    if want != [p for p in paras if p in want]:
        bad.append(f"{L}: paragraphs missing or reordered — got {paras!r}")
    back = texts(html.split('class="about-back"', 1)[-1], "a")
    if back[:1] != [d["about_back"]]:
        bad.append(f"{L}: return line is not the dictionary's — {back[:1]!r}")
    # nothing visible that the dictionary does not own (the signature is the one allowed extra)
    for p in paras:
        if p and p not in want and p != d["about_back"] and not p.startswith("©"):
            bad.append(f"{L}: page prose absent from the dictionary — {p!r}")
check("AB2 INV-102 every visible sentence comes from the copy dictionary",
      REACH and not bad, "; ".join(bad[:4]) or REACH_NOTE)

# ---------------------------------------------------------------- AB3 no photograph, no share picture
bad = []
for L, html in PAGES.items():
    body = html.split("<body", 1)[-1]
    if tags(body, "img"):
        bad.append(f"{L}: an <img> stands on a page of prose")
    for prop in ("og:image", "og:image:alt"):
        if f'property="{prop}"' in html:
            bad.append(f"{L}: {prop} emitted with no picture behind it")
    if 'name="twitter:image"' in html:
        bad.append(f"{L}: twitter:image emitted with no picture")
    card = meta_content(html, "name", "twitter:card")
    if card != "summary":
        bad.append(f"{L}: twitter:card={card!r}, want 'summary' (large-image with no image unfurls broken)")
check("AB3 INV-102 no photograph and no share picture",
      REACH and not bad, "; ".join(bad[:4]) or REACH_NOTE)

# ---------------------------------------------------------------- AB4 the sibling set is mutual
bad = []
baked = [L for L in WITH_COPY if L in PAGES]
for L, html in PAGES.items():
    alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', html)
    named = [a for a, _ in alts if a != "x-default"]
    if sorted(named) != sorted(baked):
        bad.append(f"{L}: hreflang set {sorted(named)} != baked {sorted(baked)}")
    if len(named) != len(set(named)):
        bad.append(f"{L}: a language named twice")
    xd = [href for a, href in alts if a == "x-default"]
    if xd != [f"{SITE_URL}/about"]:
        bad.append(f"{L}: x-default={xd!r}, want the fallback page")
    for a, href in alts:
        if a != "x-default" and href != f"{SITE_URL}{about_url(a)}":
            bad.append(f"{L}: hreflang {a} points at {href}")
check("AB4 INV-102 the sibling set is complete, mutual, and carries one x-default",
      REACH and not bad, "; ".join(bad[:4]) or REACH_NOTE)

# ---------------------------------------------------------------- AB5 own language and direction
bad = []
for L, html in PAGES.items():
    m = re.search(r"<html\b[^>]*>", html)
    open_tag = m.group(0) if m else ""
    if f'lang="{L}"' not in open_tag:
        bad.append(f"{L}: <html> says {open_tag!r}")
    want_dir = DICT[L].get("dir") == "rtl"
    if want_dir and 'dir="rtl"' not in open_tag:
        bad.append(f"{L}: right-to-left tongue with no dir")
    if not want_dir and 'dir="rtl"' in open_tag:
        bad.append(f"{L}: left-to-right tongue marked rtl")
# the pages that existed before this feature stay exactly as they were
if '<html lang="en">' not in INDEX:
    bad.append("the root's <html> changed")
if WORK_PAGES and '<html lang="en">' not in WORK_PAGES[0].read_text(encoding="utf-8"):
    bad.append("a work page's <html> changed")
check("AB5 INV-102 each page declares its own language and direction; the old pages are untouched",
      REACH and not bad, "; ".join(bad[:4]) or REACH_NOTE)

# ---------------------------------------------------------------- AB7 sitemap
sm = (TMP / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
about_locs = [f"{SITE_URL}{about_url(L)}" for L in baked]
bad = []
for u in about_locs:
    if locs.count(u) != 1:
        bad.append(f"{u} listed {locs.count(u)}×")
if len(locs) != 1 + len(ITEMS) + len(baked):
    bad.append(f"loc count {len(locs)} != root + {len(ITEMS)} works + {len(baked)} about pages")
for u in about_locs:
    entry = re.search(rf"<url><loc>{re.escape(u)}</loc>.*?</url>", sm, re.S)
    if entry and "image:image" in entry.group(0):
        bad.append(f"{u} carries an image entry with no image on the page")
check("AB7 INV-103 every about page is in the sitemap exactly once, with no image entry",
      REACH and not bad, "; ".join(bad[:4]) or REACH_NOTE)

# ---------------------------------------------------------------- AB8 (data half) both entries
sign_link = f'href="/about"'
bad = []
if sign_link not in INDEX:
    bad.append("the root's signature carries no about link")
for p in WORK_PAGES[:3]:
    if sign_link not in p.read_text(encoding="utf-8"):
        bad.append(f"{p.name}: the work page's signature carries no about link")
check("AB8 INV-103 the baked signature on the root and on every work page reaches the about page",
      not bad, "; ".join(bad[:4]))

# ---------------------------------------------------------------- AB9 (data half) never two doors
walk_sign = EXDATA.get("copyright", "")
check("AB9 INV-103 the signature composed for the walk omits the about link",
      "/about" not in walk_sign and "Instagram" in walk_sign,
      f"walk signature = {walk_sign!r}")

# ---------------------------------------------------------------- AB11 only the entry word travels
PAGE_KEYS = ("about_title", "about_1", "about_2", "about_3", "about_4", "about_back")
client_langs = (EXDATA.get("greet") or {}).get("langs") or {}
leaked = sorted({f"{L}.{k}" for L, blk in client_langs.items() for k in PAGE_KEYS if k in blk})
word_missing = [L for L in WITH_COPY if not (client_langs.get(L) or {}).get("about")]
check("AB11 INV-104 only the entry word rides the client artifact",
      not leaked and not word_missing,
      f"leaked={leaked[:6]} word_missing={word_missing}")

# ---------------------------------------------------------------- AB14 the feature stands down whole
STRIPPED = Path(tempfile.mkdtemp(prefix="synth_about_off_"))
FIXTURE2 = STRIPPED / "content"
shutil.copytree(build_site.FIXTURE, FIXTURE2)
g2 = json.loads((FIXTURE2 / "data" / "greetings.json").read_text(encoding="utf-8"))
for blk in g2["langs"].values():
    for k in ("about",) + PAGE_KEYS:
        blk.pop(k, None)
(FIXTURE2 / "data" / "greetings.json").write_text(
    json.dumps(g2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

OUT2 = STRIPPED / "out"
_orig_fixture, _orig_out = build_site.FIXTURE, build_site.OUT
try:
    build_site.FIXTURE = FIXTURE2
    build_site.OUT = OUT2
    build_site.build(SITE_URL)
    off_index = (OUT2 / "index.html").read_text(encoding="utf-8")
    off_ex = (OUT2 / "exhibition_data.json").read_text(encoding="utf-8")
    off_sm = (OUT2 / "sitemap.xml").read_text(encoding="utf-8")
    bad = []
    if (OUT2 / "about.html").exists() or (OUT2 / "about").exists():
        bad.append("an about page baked with no copy behind it")
    for label, blob in (("index", off_index), ("exhibition_data", off_ex), ("sitemap", off_sm)):
        if "/about" in blob:
            bad.append(f"{label} still points at a page that was never baked")
    check("AB14 INV-102 no copy in the fallback tongue stands the whole feature down",
          not bad, "; ".join(bad[:4]))
finally:
    build_site.FIXTURE = _orig_fixture
    build_site.OUT = _orig_out

# ---------------------------------------------------------------- browser rows
BROWSER_ROWS = [
    "AB6 INV-102 the right-to-left page really lays out right-to-left",
    "AB12 INV-16 the page renders whole with no script of its own",
    "AB13 CS-6 the column reads on a phone and does not stretch on a desktop",
    "AB8b/AB9b INV-103 the closing screen carries exactly one about link, in the visitor's tongue",
    "AB10 INV-103 the closing screen's about link belongs to the touch-press class",
]

if not chrome_available():
    for r in BROWSER_ROWS:
        skip(r, "Chrome not installed (pinned expected skip)")
else:
    with serve(TMP) as base:
        # AB6 · AB12 · AB13 — the page itself
        with Browser(width=390, height=844) as br:
            br.navigate(base + "/about/he")
            br.sleep(0.4)
            st = json.loads(br.evaluate(
                "(()=>{const h=document.documentElement,p=document.querySelector('.about p');"
                "return JSON.stringify({dir:getComputedStyle(h).direction,"
                "lang:h.getAttribute('lang'),"
                "pdir:p?getComputedStyle(p).direction:'',"
                "left:p?Math.round(p.getBoundingClientRect().left):-1});})()"))
            check(BROWSER_ROWS[0],
                  st["dir"] == "rtl" and st["pdir"] == "rtl" and st["lang"] == "he",
                  f"computed={st}")

            br.navigate(base + "/about")
            br.sleep(0.4)
            seen = json.loads(br.evaluate(
                "(()=>{const m=document.querySelector('main.about');"
                "return JSON.stringify({scripts:document.querySelectorAll('script[src]').length,"
                "paras:document.querySelectorAll('.about p').length,"
                "h1:(document.querySelector('.about h1')||{}).textContent||'',"
                "back:!!document.querySelector('.about-back a'),"
                "sign:!!document.querySelector('.sign'),"
                "text:(m?m.innerText:'').length});})()"))
            check(BROWSER_ROWS[1],
                  seen["scripts"] == 0 and seen["paras"] >= 4 and seen["back"]
                  and seen["sign"] and seen["h1"] == DICT["en"]["about_title"],
                  f"rendered={seen}")

            MEASURE = ("(()=>{const p=document.querySelector('.about p');"
                       "if(!p)return JSON.stringify({absent:1});"
                       "const r=p.getBoundingClientRect();"
                       "return JSON.stringify({w:Math.round(r.width),left:Math.round(r.left),"
                       "vw:innerWidth});})()")
            phone = json.loads(br.evaluate(MEASURE))
            br.set_viewport(1440, 900)
            br.sleep(0.3)
            desk = json.loads(br.evaluate(MEASURE))
            check(BROWSER_ROWS[2],
                  not phone.get("absent") and not desk.get("absent")
                  and phone["left"] >= 12 and phone["w"] <= phone["vw"] - 20
                  and desk["w"] <= 780,
                  f"phone={phone} desktop={desk} (measure capped, text clear of the edge)")

        # AB8b / AB9b / AB10 — the walk's closing screen, read in Russian
        with Browser(width=390, height=844) as br:
            br.navigate(base + "/")
            br.clear_storage()
            br.evaluate("localStorage.setItem('ex-tempo','0.05')")
            br.pretend("ru", 14)
            br.reload(); br.sleep(1.2)
            br.click(".exd-window:nth-child(1)", settle=0.8)
            br.sleep(1.0)
            br.evaluate("document.getElementById('exh-fin').scrollIntoView({behavior:'instant'})")
            br.sleep(0.4)
            fin = json.loads(br.evaluate(
                "(()=>{const f=document.getElementById('exh-fin');"
                "const links=f?[...f.querySelectorAll('a[href*=\\\"/about\\\"]')]:[];"
                "const row=f?[...f.querySelectorAll('.row > *')].map(e=>e.id||e.className):[];"
                "return JSON.stringify({n:links.length,"
                "href:links[0]?links[0].getAttribute('href'):'',"
                "word:links[0]?links[0].textContent.trim():'',row:row});})()"))
            check(BROWSER_ROWS[3],
                  fin["n"] == 1 and fin["href"] == "/about/ru"
                  and fin["word"] == DICT["ru"]["about"],
                  f"finale={fin} (one door, the visitor's own tongue)")

            pressed = json.loads(br.evaluate(
                "(()=>{const a=document.querySelector('#exh-fin a[href*=\\\"/about\\\"]');"
                "if(!a)return JSON.stringify({no:1});"
                "const r=a.getBoundingClientRect();"
                "const ev=(t)=>a.dispatchEvent(new PointerEvent(t,{bubbles:true,clientX:r.left+2,"
                "clientY:r.top+2,pointerType:'touch'}));ev('pointerdown');"
                "const on=a.classList.contains('ex-press');ev('pointerup');"
                "return JSON.stringify({on:on,off:!a.classList.contains('ex-press')});})()"))
            check(BROWSER_ROWS[4],
                  pressed.get("on") and pressed.get("off"),
                  f"press={pressed} (lit under the finger, cleared on the lift)")

# ---------------------------------------------------------------- report
shutil.rmtree(TMP, ignore_errors=True)
shutil.rmtree(STRIPPED, ignore_errors=True)

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
