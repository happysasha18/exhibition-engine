/* tlv i18n worker (EX-I18N / INV-42) — the Pages advanced-mode entry (`_worker.js`), routed by
   `_routes.json` to /api/* ONLY, so every static byte stays pure CDN. It generates a language's
   FULL string set ONCE (Haiku, museum tone, strict shape — a malformed answer is never served),
   keeps it forever in KV under lang+version, and answers everyone after from the cache at $0.
   Bindings the Pages project must carry: TLV_I18N (KV) · ANTHROPIC_API_KEY (secret) · ASSETS. */
const TAG_RE = /^[a-z]{2,3}(-[a-z0-9]{2,8})?$/;
const RTL = ["ar", "he", "fa", "ur", "yi", "iw", "dv", "ps", "ckb"];

const TOKEN_RE = /^[a-z0-9]{16,40}$/;

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === "/api/visitor") return visitor(req, env, url);
    if (url.pathname !== "/api/i18n") return new Response("not found", { status: 404 });
    const lang = (url.searchParams.get("lang") || "").toLowerCase();
    const v = url.searchParams.get("v") || "";
    // sane tags only — a locale code never reaches the prompt as free text (prover I5)
    if (!TAG_RE.test(lang) || !/^[\w.-]{1,40}$/.test(v)) {
      return new Response("bad request", { status: 400 });
    }

    const key = v + ":" + lang;
    const hit = await env.TLV_I18N.get(key);            // cache first — one model call per
    if (hit) return json(hit);                          // language-version, ever (prover I6)

    const srcRes = await env.ASSETS.fetch(new URL("/i18n_source.json", url.origin));
    if (!srcRes.ok) return new Response("source missing", { status: 500 });
    const src = await srcRes.json();
    if (v !== String(src.version)) return new Response("stale version", { status: 409 });

    const lock = "lock:" + key;                         // best-effort single flight (a burst
    if (await env.TLV_I18N.get(lock)) {                 // warms, it never fans out)
      return new Response("warming", { status: 503, headers: { "Retry-After": "3" } });
    }
    await env.TLV_I18N.put(lock, "1", { expirationTtl: 60 });

    let out;
    try {
      out = await translate(env.ANTHROPIC_API_KEY, lang, src);
    } catch (e) {
      // the reason (never a secret): "model 401", "refused", a parse failure — debuggable by curl
      return new Response("model unavailable: " + ((e && e.message) || "?"), { status: 502 });
    }
    if (!validate(out, src)) return new Response("malformed", { status: 502 });
    await env.TLV_I18N.put(key, JSON.stringify(out));
    return json(JSON.stringify(out));
  },
};

// EX-MEMORY (INV-43): the coat-check record — seen-work ids under a random token, nothing else.
// MERGE-never-replace (two tabs may write, M3), ~500 newest kept (M2), every write re-arms the
// ~180-day expiry; shaped tokens/ids only — free-form strings never reach KV keys.
async function visitor(req, env, url) {
  if (req.method === "GET") {
    const t = url.searchParams.get("t") || "";
    if (!TOKEN_RE.test(t)) return new Response("bad request", { status: 400 });
    const rec = await env.TLV_I18N.get("v:" + t);
    return json(rec || '{"seen":[]}');
  }
  if (req.method === "PUT" || req.method === "POST") {
    const body = await req.text();
    if (body.length > 2048) return new Response("too big", { status: 413 });
    let p;
    try { p = JSON.parse(body); } catch (e) { return new Response("bad request", { status: 400 }); }
    const t = String(p.t || "");
    if (!TOKEN_RE.test(t) || !Array.isArray(p.add)) {
      return new Response("bad request", { status: 400 });
    }
    const adds = p.add.map(String).filter((x) => /^\d{5,25}$/.test(x)).slice(0, 100);
    let cur;
    try { cur = JSON.parse((await env.TLV_I18N.get("v:" + t)) || '{"seen":[]}'); }
    catch (e) { cur = { seen: [] }; }
    const set = new Set(Array.isArray(cur.seen) ? cur.seen : []);
    for (const a of adds) set.add(a);
    const seen = Array.from(set).slice(-500);          // the cap keeps the NEWEST
    await env.TLV_I18N.put("v:" + t, JSON.stringify({ seen }),
                           { expirationTtl: 15552000 });
    return json(JSON.stringify({ ok: true, n: seen.length }));
  }
  return new Response("method not allowed", { status: 405 });
}

function json(body) {
  return new Response(body, {
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=86400" },
  });
}

async function translate(apiKey, lang, src) {
  const prompt =
    'You localize the interface of a quiet photography museum site into the language with ' +
    'BCP-47 tag "' + lang + '". Museum tone: reserved, natural, native-sounding; no exclamation ' +
    'marks, no salesmanship. Translate the UI strings, the greeting lines (short, what a reserved ' +
    'native speaker actually says at that hour), and the artwork titles. Keep every "{n}" ' +
    'placeholder verbatim. A title that is a proper name or untranslatable wordplay stays as it ' +
    'is. Reply with JSON only; return "titles" as an ARRAY of {"id","title"} pairs covering ' +
    'every source title, ids verbatim.\nSource (English):\n' +
    JSON.stringify({ strings: src.strings, greet: src.greet, titles: src.titles });
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-haiku-4-5",
      max_tokens: 16000,
      messages: [{ role: "user", content: prompt }],
      output_config: { format: { type: "json_schema", schema: shape() } },
    }),
  });
  if (!r.ok) throw new Error("model " + r.status);
  const msg = await r.json();
  if (msg.stop_reason === "refusal") throw new Error("refused");
  const text = (msg.content || []).find((b) => b.type === "text");
  const out = JSON.parse(text.text);
  // "dir" is OURS, never the model's guess — the curated RTL list decides (prover I1);
  // titles arrive as an ARRAY (strict schemas forbid free-key maps) and fold back to a map
  const titles = {};
  for (const t of out.titles || []) titles[t.id] = t.title;
  const flat = Object.assign({}, out.strings, {
    greet: out.greet, titles: titles,
    dir: RTL.indexOf(lang.slice(0, 2)) >= 0 ? "rtl" : "ltr",
  });
  return flat;
}

function shape() {
  const s = { type: "string" };
  const pool = { type: "array", items: s };
  return {
    type: "object",
    properties: {
      strings: {
        type: "object",
        properties: { ask: s, exit: s, more: s, q_more: s, q_spent: s, share_label: s,
                      share_copied: s, series: s, room_back: s },
        required: ["ask", "exit", "more", "q_more", "q_spent", "share_label", "share_copied",
                   "series", "room_back"],
        additionalProperties: false,
      },
      greet: {
        type: "object",
        properties: { night: pool, morning: pool, day: pool, evening: pool },
        required: ["night", "morning", "day", "evening"],
        additionalProperties: false,
      },
      titles: {
        type: "array",
        items: {
          type: "object",
          properties: { id: s, title: s },
          required: ["id", "title"],
          additionalProperties: false,
        },
      },
    },
    required: ["strings", "greet", "titles"],
    additionalProperties: false,
  };
}

function validate(out, src) {
  try {
    const filled = (x) => typeof x === "string" && x.trim().length > 0;
    if (!["ltr", "rtl"].includes(out.dir)) return false;
    for (const k of ["ask", "exit", "q_more", "q_spent", "share_label", "share_copied", "series", "room_back"]) {
      if (!filled(out[k])) return false;
    }
    if (!filled(out.more) || out.more.indexOf("{n}") < 0) return false;
    for (const p of ["night", "morning", "day", "evening"]) {
      if (!Array.isArray(out.greet[p]) || !out.greet[p].length || !out.greet[p].every(filled)) return false;
    }
    for (const id of Object.keys(src.titles)) {
      if (!filled((out.titles || {})[id])) return false;
    }
    return true;
  } catch (e) {
    return false;
  }
}
