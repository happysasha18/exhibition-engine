#!/usr/bin/env python3
"""Generate tests/fixture_content/ — a synthetic exhibition archive for engine testing.

Run once before the test suite:
    python tests/make_synthetic.py

Completely deterministic (re-running overwrites with identical content).
ALL content is visibly synthetic: IDs are "synth-NN", site title is
"SYNTH EXHIBITION", images are 64×64 solid-colour PNGs with a white diagonal
stripe so they are distinguishable and visibly not real photographs.

Zero pip dependencies — image generation via stdlib zlib+struct only.
"""
import hashlib
import json
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixture_content"

# ── work catalogue ────────────────────────────────────────────────────────────
# (id, section, title_or_empty, city, country)
WORKS = [
    ("synth-01", "urban",     "Synthetic Corner",  "Tel Aviv",  "IL"),
    ("synth-02", "urban",     "Synthetic Alley",   "Tel Aviv",  "IL"),
    ("synth-03", "urban",     "Synthetic Facade",  "Jerusalem", "IL"),
    ("synth-04", "urban",     "Synthetic Window",  "Haifa",     "IL"),
    ("synth-05", "urban",     "Synthetic Rooftop", "Tel Aviv",  "IL"),
    ("synth-06", "urban",     "Synthetic Door",    "",          ""),
    ("synth-07", "urban",     "Synthetic Stairway","",          ""),
    ("synth-08", "landscape", "",                  "Galilee",   "IL"),
    ("synth-09", "landscape", "",                  "Negev",     "IL"),
    ("synth-10", "landscape", "",                  "",          ""),
    ("synth-11", "landscape", "",                  "Dead Sea",  "IL"),
    ("synth-12", "landscape", "",                  "",          ""),
    ("synth-13", "abstract",  "",                  "",          ""),
    ("synth-14", "abstract",  "",                  "",          ""),  # series member
    ("synth-15", "abstract",  "",                  "",          ""),  # series member
    ("synth-16", "abstract",  "",                  "",          ""),  # series member
]

# Three works form one series (>= 3 required by engine; variant → "lane")
SERIES_MEMBERS = ["synth-14", "synth-15", "synth-16"]

# Five door-pool candidates
DOOR_IDS = ["synth-01", "synth-03", "synth-06", "synth-09", "synth-11"]

# 26 numeric kinship axes (all scalar, no special palette axis)
AXES = [
    "AX-01_brightness", "AX-02_key",        "AX-03_contrast",   "AX-04_radial",
    "AX-05_texture",    "AX-07_warmth",      "AX-08_colorful",   "AX-09_edge",
    "AX-10_symmetry",   "AX-11_human",       "AX-12_urban",      "AX-13_nature",
    "AX-14_geometry",   "AX-15_darkness",    "AX-16_grain",      "AX-17_depth",
    "AX-18_motion",     "AX-19_saturation",  "AX-20_hue_shift",  "AX-21_midtone",
    "AX-22_highlight",  "AX-23_shadow",      "AX-24_fine_detail","AX-25_composition",
    "AX-26_mood",       "AX-27_density",
]

CAPTIONS = [
    "A synthetic corner in the urban grid.",
    "A synthetic alley between walls.",
    "A synthetic facade catching light.",
    "A synthetic window framing sky.",
    "A synthetic rooftop at dusk.",
    "A synthetic door in silence.",
    "A synthetic stairway descending.",
    "A synthetic landscape at rest.",
    "A synthetic expanse of sand.",
    "An empty synthetic field.",
    "A synthetic shore at low tide.",
    "A synthetic horizon unmarked.",
    "An abstract synthetic form.",
    "A synthetic shape unresolved.",
    "A synthetic mark without name.",
    "A synthetic trace of light.",
]


# ── minimal PNG generator ─────────────────────────────────────────────────────

def _png(width, height, bg_r, bg_g, bg_b):
    """Return bytes for a valid RGB PNG: solid background + white diagonal stripe (4 px wide).
    The stripe makes every synthetic image visually distinct at a glance."""
    rows = []
    for y in range(height):
        row = bytearray([0])  # filter byte = None (type 0)
        for x in range(width):
            if (x + y) % 20 < 4:          # diagonal stripe, 4-px band
                row += bytes([255, 255, 255])
            else:
                row += bytes([bg_r, bg_g, bg_b])
        rows.append(bytes(row))

    raw = b"".join(rows)
    compressed = zlib.compress(raw, 9)

    def chunk(ctype, data):
        c = ctype + data
        return (struct.pack(">I", len(data)) + c +
                struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF))

    MAGIC = b"\x89PNG\r\n\x1a\n"
    IHDR_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return MAGIC + chunk(b"IHDR", IHDR_data) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")


def _work_color(idx):
    """Deterministic, visually distinct RGB background per work index.
    Uses golden-angle hue spread, then a simple HSV→RGB (s=0.6, v=0.78)."""
    h = (idx * 137) % 360
    s, v = 0.6, 0.78
    hi = h / 60.0
    i = int(hi)
    f = hi - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    rgb_options = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    r, g, b = rgb_options[i % 6]
    return int(r * 255), int(g * 255), int(b * 255)


# ── axis values ───────────────────────────────────────────────────────────────

def _axis_val(work_id, axis_name):
    """Deterministic pseudo-random scalar in [0.05, 0.95].
    Avoids extremes so no axis becomes trivially flat after min-max normalization."""
    digest = hashlib.sha256(f"synth-fixture-v1:{work_id}:{axis_name}".encode()).hexdigest()
    raw = int(digest[:8], 16) / 0xFFFFFFFF   # [0, 1)
    return round(0.05 + raw * 0.90, 4)       # [0.05, 0.95]


# ── file helpers ──────────────────────────────────────────────────────────────

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        path.write_bytes(data)
    else:
        path.write_text(data, encoding="utf-8")


# ── main generator ────────────────────────────────────────────────────────────

def make():
    FIXTURE.mkdir(parents=True, exist_ok=True)

    work_by_id = {}
    gallery_items = []
    vector_items = []
    tags = []

    for idx, (wid, section, title, city, country) in enumerate(WORKS):
        img = f"assets/{section}/{wid}.png"
        r, g, b = _work_color(idx)
        dom = [r, g, b]

        # write the synthetic image file
        write(FIXTURE / "gallery" / img, _png(64, 64, r, g, b))

        item = {"id": wid, "section": section, "img": img, "title": title,
                "w": 64, "h": 64, "dom": dom}
        if city:
            item["city"] = city
        if country:
            item["country"] = country
        gallery_items.append(item)
        work_by_id[wid] = item

        # kinship vector: all 26 axes, each a dict with a numeric value
        axes = {ax: {"value": _axis_val(wid, ax), "source": "synthetic", "confidence": 0.99}
                for ax in AXES}
        vector_items.append({"id": wid, "img": img, "title": title,
                              "section": section, "axes": axes})

        tags.append({"id": wid, "subject": CAPTIONS[idx]})

    # gallery/gallery_data.json
    write(FIXTURE / "gallery" / "gallery_data.json",
          json.dumps({"items": gallery_items}, ensure_ascii=False, indent=2) + "\n")

    # vector.json (top-level key "items")
    write(FIXTURE / "vector.json",
          json.dumps({"items": vector_items}, ensure_ascii=False, indent=2) + "\n")

    # content_tags.json (bare list)
    write(FIXTURE / "content_tags.json",
          json.dumps(tags, ensure_ascii=False, indent=2) + "\n")

    # gallery/door_candidates.json  (5 entries, >= 5 required for door_size=5)
    door = []
    for wid in DOOR_IDS:
        it = work_by_id[wid]
        door.append({"id": wid, "img": it["img"],
                     "luma":   round(_axis_val(wid, "luma"),   3),
                     "warmth": round(_axis_val(wid, "warmth"), 3)})
    write(FIXTURE / "gallery" / "door_candidates.json",
          json.dumps(door, ensure_ascii=False, indent=2) + "\n")

    # gallery/shared/tokens.css  (must exist; exhibition.html links it)
    write(FIXTURE / "gallery" / "shared" / "tokens.css",
          "/* SYNTH EXHIBITION — synthetic design tokens for engine fixture testing */\n"
          ":root{--cross:1.2s;--d-appear:0.4s;--d-vanish:0.3s}\n")

    # finalist_series.json  (one 3-work series → variant "lane")
    # member format: "NNNN_<id>.jpg"  →  id_of() strips prefix+suffix
    members = [f"{i+1:04d}_{m}.jpg" for i, m in enumerate(SERIES_MEMBERS)]
    write(FIXTURE / "finalist_series.json",
          json.dumps({"series": [{"members": members}]}, ensure_ascii=False, indent=2) + "\n")

    # data/greetings.json  (must satisfy the greetings() assertions in build.py)
    greet_doc = {
        "fallback": "en",
        "aliases": {},
        "langs": {
            "en": {
                "dir": "ltr",
                "ask": "what feels closer now",
                "greet": {
                    "night":   ["A synthetic quiet night"],
                    "morning": ["A synthetic morning"],
                    "day":     ["A synthetic day"],
                    "evening": ["A synthetic evening"],
                },
                "exit":         "exit",
                "more":         "{n} more",
                "q_more":       "walk on?",
                "q_spent":      "onward — a new choice",
                "share_label":  "copy the link",
                "share_copied": "link copied",
                "series":       "series",
                "room_back":    "← room",
            }
        },
    }
    write(FIXTURE / "data" / "greetings.json",
          json.dumps(greet_doc, ensure_ascii=False, indent=2) + "\n")

    # instance-assets/  (favicons — copied to bundle root by copy_exhibition_assets())
    fav_svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" fill="#1a1a2e"/>'
        '<text x="16" y="22" font-size="18" text-anchor="middle" fill="#e0e0f0">S</text>'
        '</svg>\n'
    )
    write(FIXTURE / "instance-assets" / "favicon.svg", fav_svg)
    tiny_png = _png(1, 1, 26, 26, 46)   # 1×1 dark-blue pixel — valid PNG
    write(FIXTURE / "instance-assets" / "favicon.png", tiny_png)
    write(FIXTURE / "instance-assets" / "apple-touch-icon.png", tiny_png)

    print(f"fixture_content/ → {FIXTURE}")
    print(f"  {len(WORKS)} works  ·  1 series ({len(SERIES_MEMBERS)} members)  "
          f"·  {len(DOOR_IDS)} door candidates  ·  {len(AXES)} kinship axes")


if __name__ == "__main__":
    make()
