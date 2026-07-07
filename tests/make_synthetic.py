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
    ("synth-14", "abstract",  "",                  "",          ""),  # lane series member
    ("synth-15", "abstract",  "",                  "",          ""),  # lane series member
    ("synth-16", "abstract",  "",                  "",          ""),  # lane series member
    # synth-17..24 added so that CAP (spread+max_unfolds×unfold_step = 10+2×5 = 20) < len(WORKS)
    ("synth-17", "urban",     "Synthetic Arch",    "Berlin",    "DE"),
    ("synth-18", "urban",     "Synthetic Market",  "Paris",     "FR"),
    ("synth-19", "landscape", "",                  "Alps",      "CH"),
    ("synth-20", "landscape", "",                  "Coast",     "ES"),
    ("synth-21", "abstract",  "",                  "",          ""),
    ("synth-22", "abstract",  "",                  "",          ""),
    ("synth-23", "abstract",  "",                  "",          ""),
    ("synth-24", "abstract",  "",                  "",          ""),
]

# Two series:
#   polaroids (8+ members → variant "polaroids"): synth-01..08
#   lane      (3 members → variant "lane"):        synth-14..16
SERIES_POLAROIDS = ["synth-01", "synth-02", "synth-03", "synth-04",
                    "synth-05", "synth-06", "synth-07", "synth-08"]
SERIES_LANE      = ["synth-14", "synth-15", "synth-16"]

# Ten door-pool candidates: 5 dark (luma≈0.15–0.22) + 5 bright (luma≈0.78–0.88).
# Clear dark/bright split so the hour-lean test (night→dark / day→bright) is reliable.
# Pool must exceed door_size (5) so the living-hand law engages.
DOOR_ENTRIES = [
    # dark works
    ("synth-01", 0.15, 0.30),
    ("synth-03", 0.17, 0.55),
    ("synth-06", 0.20, 0.40),
    ("synth-09", 0.18, 0.25),
    ("synth-11", 0.22, 0.35),
    # bright works
    ("synth-02", 0.85, 0.70),
    ("synth-04", 0.80, 0.65),
    ("synth-05", 0.82, 0.75),
    ("synth-07", 0.88, 0.45),
    ("synth-12", 0.78, 0.60),
]

# 26 numeric kinship axes (all scalar)
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
    "A synthetic arch spanning void.",
    "A synthetic market at dawn.",
    "A synthetic alpine field.",
    "A synthetic coast at rest.",
    "An abstract synthetic plane.",
    "A synthetic shadow cast long.",
    "A synthetic blur in motion.",
    "A synthetic edge without end.",
]

# ── 7 synthetic languages for greetings.json ─────────────────────────────────
# All strings are visibly synthetic; 2+ variants per daypart for the date-seeded test.
# RU exit == "выход"; HE dir == "rtl" and ask == "מה קרוב אליך עכשיו".
# All 7 langs must have series + room_back.
GREETINGS = {
    "fallback": "en",
    "aliases": {"iw": "he"},
    "langs": {
        "en": {
            "dir": "ltr",
            "ask": "what feels closer now",
            "greet": {
                "night":   ["A synthetic quiet night", "Another synthetic night"],
                "morning": ["A synthetic morning",     "Another synthetic morning"],
                "day":     ["A synthetic day",          "Another synthetic day"],
                "evening": ["A synthetic evening",      "Another synthetic evening"],
            },
            "exit":         "exit",
            "more":         "{n} more",
            "q_more":       "walk on?",
            "q_spent":      "onward — a new choice",
            "share_label":  "copy the link",
            "share_copied": "link copied",
            "series":       "series",
            "room_back":    "← room",
        },
        "ru": {
            "dir": "ltr",
            "ask": "что ближе сейчас",
            "greet": {
                "night":   ["Синтетическая тихая ночь", "Ещё одна синтетическая ночь"],
                "morning": ["Синтетическое утро",       "Ещё одно синтетическое утро"],
                "day":     ["Синтетический день",        "Ещё один синтетический день"],
                "evening": ["Синтетический вечер",       "Ещё один синтетический вечер"],
            },
            "exit":         "выход",
            "more":         "ещё {n}",
            "q_more":       "идём дальше?",
            "q_spent":      "вперёд — новый выбор",
            "share_label":  "скопировать ссылку",
            "share_copied": "ссылка скопирована",
            "series":       "серия",
            "room_back":    "← комната",
        },
        "he": {
            "dir": "rtl",
            "ask": "מה קרוב אליך עכשיו",
            "greet": {
                "night":   ["לילה שקט סינתטי",  "עוד לילה סינתטי"],
                "morning": ["בוקר סינתטי",       "עוד בוקר סינתטי"],
                "day":     ["יום סינתטי",         "עוד יום סינתטי"],
                "evening": ["ערב סינתטי",         "עוד ערב סינתטי"],
            },
            "exit":         "יציאה",
            "more":         "עוד {n}",
            "q_more":       "ממשיכים?",
            "q_spent":      "קדימה — בחירה חדשה",
            "share_label":  "העתק קישור",
            "share_copied": "הקישור הועתק",
            "series":       "סדרה",
            "room_back":    "← חדר",
        },
        "de": {
            "dir": "ltr",
            "ask": "was fühlt sich näher an",
            "greet": {
                "night":   ["Eine synthetische stille Nacht", "Noch eine synthetische Nacht"],
                "morning": ["Ein synthetischer Morgen",       "Noch ein synthetischer Morgen"],
                "day":     ["Ein synthetischer Tag",           "Noch ein synthetischer Tag"],
                "evening": ["Ein synthetischer Abend",         "Noch ein synthetischer Abend"],
            },
            "exit":         "beenden",
            "more":         "noch {n}",
            "q_more":       "weiter?",
            "q_spent":      "vorwärts — eine neue Wahl",
            "share_label":  "Link kopieren",
            "share_copied": "Link kopiert",
            "series":       "Serie",
            "room_back":    "← Raum",
        },
        "fr": {
            "dir": "ltr",
            "ask": "qu'est-ce qui semble plus proche",
            "greet": {
                "night":   ["Une nuit synthétique tranquille", "Une autre nuit synthétique"],
                "morning": ["Un matin synthétique",            "Un autre matin synthétique"],
                "day":     ["Un jour synthétique",              "Un autre jour synthétique"],
                "evening": ["Un soir synthétique",              "Un autre soir synthétique"],
            },
            "exit":         "quitter",
            "more":         "encore {n}",
            "q_more":       "on continue?",
            "q_spent":      "en avant — un nouveau choix",
            "share_label":  "copier le lien",
            "share_copied": "lien copié",
            "series":       "série",
            "room_back":    "← salle",
        },
        "es": {
            "dir": "ltr",
            "ask": "qué se siente más cercano",
            "greet": {
                "night":   ["Una noche sintética tranquila", "Otra noche sintética"],
                "morning": ["Una mañana sintética",          "Otra mañana sintética"],
                "day":     ["Un día sintético",               "Otro día sintético"],
                "evening": ["Una tarde sintética",            "Otra tarde sintética"],
            },
            "exit":         "salir",
            "more":         "{n} más",
            "q_more":       "¿seguimos?",
            "q_spent":      "adelante — una nueva elección",
            "share_label":  "copiar enlace",
            "share_copied": "enlace copiado",
            "series":       "serie",
            "room_back":    "← sala",
        },
        "uk": {
            "dir": "ltr",
            "ask": "що ближче зараз",
            "greet": {
                "night":   ["Синтетична тиха ніч",  "Ще одна синтетична ніч"],
                "morning": ["Синтетичний ранок",     "Ще один синтетичний ранок"],
                "day":     ["Синтетичний день",       "Ще один синтетичний день"],
                "evening": ["Синтетичний вечір",      "Ще один синтетичний вечір"],
            },
            "exit":         "вихід",
            "more":         "ще {n}",
            "q_more":       "йдемо далі?",
            "q_spent":      "вперед — новий вибір",
            "share_label":  "скопіювати посилання",
            "share_copied": "посилання скопійовано",
            "series":       "серія",
            "room_back":    "← кімната",
        },
    },
}


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

    # gallery/door_candidates.json — 10 entries (5 dark + 5 bright), pool > door_size=5
    door = []
    for wid, luma, warmth in DOOR_ENTRIES:
        it = work_by_id[wid]
        door.append({"id": wid, "img": it["img"], "luma": luma, "warmth": warmth})
    write(FIXTURE / "gallery" / "door_candidates.json",
          json.dumps(door, ensure_ascii=False, indent=2) + "\n")

    # gallery/shared/tokens.css — ALL duration literals use calc(N * var(--tempo)) form
    # so that the motion test's "no rogue literals" scan passes.
    # --ease and all --d-* tokens are required by exhibition.css; without them transitions
    # and animations use var() fallbacks or become invalid (transitionDuration collapses to 0s).
    # --accent: #b3a284 is the "bone" resting value; --tempo base + reduced-motion media query
    # ensures the motion test can read --tempo even when REDUCED (engine skips setProperty).
    write(FIXTURE / "gallery" / "shared" / "tokens.css",
          "/* SYNTH EXHIBITION — synthetic design tokens for engine fixture testing */\n"
          ":root{\n"
          "  /* motion clock */\n"
          "  --tempo:    1.35;\n"
          "  --ease:     cubic-bezier(0.3,0,0.2,1);\n"
          "  /* duration tokens — every literal multiplies var(--tempo) */\n"
          "  --d-cross:  calc(1.2 * var(--tempo) * 1s);\n"
          "  --d-appear: calc(0.4 * var(--tempo) * 1s);\n"
          "  --d-vanish: calc(0.3 * var(--tempo) * 1s);\n"
          "  --d-rise:   calc(1.4 * var(--tempo) * 1s);\n"
          "  --d-reveal: calc(0.8 * var(--tempo) * 1s);\n"
          "  --d-soft:   calc(0.5 * var(--tempo) * 1s);\n"
          "  --d-ground: calc(1.7 * var(--tempo) * 1s);\n"
          "  /* accent: #b3a284 bone at rest; exhibition.js overrides on live work */\n"
          "  --accent:   #b3a284;\n"
          "  /* palette — synthetic near-black surface */\n"
          "  --ink:      #f4f1e8;\n"
          "  --muted:    rgba(244,241,232,0.55);\n"
          "  --muted-2:  rgba(244,241,232,0.35);\n"
          "  --body-2:   rgba(244,241,232,0.70);\n"
          "  --faint:    rgba(244,241,232,0.20);\n"
          "  --hair:     rgba(244,241,232,0.12);\n"
          "  /* typography */\n"
          "  --serif:    Georgia,serif;\n"
          "  --mono:     'Courier New',Courier,monospace;\n"
          "}\n"
          "/* reduced-motion: the CSS clock collapses so --tempo is readable even when\n"
          "   exhibition.js skips setProperty (engine: if(!REDUCED) setProperty) */\n"
          "@media(prefers-reduced-motion:reduce){\n"
          "  :root{ --tempo: 0.05; }\n"
          "}\n")

    # finalist_series.json — polaroids(8) + lane(3)
    # member format: "NNNN_<id>.jpg"  (id_of strips prefix + .jpg suffix)
    pol_members  = [f"{i+1:04d}_{m}.jpg" for i, m in enumerate(SERIES_POLAROIDS)]
    lane_members = [f"{i+1:04d}_{m}.jpg" for i, m in enumerate(SERIES_LANE)]
    write(FIXTURE / "finalist_series.json",
          json.dumps({"series": [{"members": pol_members},
                                  {"members": lane_members}]},
                     ensure_ascii=False, indent=2) + "\n")

    # data/greetings.json — 7 languages; satisfies all greetings() assertions in build.py
    write(FIXTURE / "data" / "greetings.json",
          json.dumps(GREETINGS, ensure_ascii=False, indent=2) + "\n")

    # instance-assets/ — favicons (copied to bundle root by copy_exhibition_assets())
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

    n_pol = len(SERIES_POLAROIDS)
    n_lane = len(SERIES_LANE)
    n_door = len(DOOR_ENTRIES)
    print(f"fixture_content/ → {FIXTURE}")
    print(f"  {len(WORKS)} works  ·  polaroids({n_pol}) + lane({n_lane}) series  "
          f"·  {n_door} door candidates  ·  {len(AXES)} kinship axes  ·  7 languages")


if __name__ == "__main__":
    make()
