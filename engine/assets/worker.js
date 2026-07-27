/* tlv i18n worker (EX-I18N / INV-42) — the Pages advanced-mode entry (`_worker.js`), routed by
   `_routes.json` to /api/* ONLY, so every static byte stays pure CDN. It generates a language's
   FULL string set ONCE (Haiku, museum tone, strict shape — a malformed answer is never served),
   keeps it forever in KV under lang+version, and answers everyone after from the cache at $0.
   Bindings the Pages project must carry: @@NS_UPPER@@_I18N (KV) · ANTHROPIC_API_KEY (secret) · ASSETS. */
const TAG_RE = /^[a-z]{2,3}(-[a-z0-9]{2,8})?$/;
const RTL = ["ar", "he", "fa", "ur", "yi", "iw", "dv", "ps", "ckb"];

const TOKEN_RE = /^[a-z0-9]{16,40}$/;
const ID_RE = /^[a-z0-9][a-z0-9_-]{2,60}$/i;

// EX-STORY-EDGE (INV-47, ST3): the PRIVATE per-work story fragments — his own notes among them —
// are BAKED IN here by N10, never a public static byte. `_worker.js` is the one bundle file
// Cloudflare Pages does NOT serve as an asset, so the raw notes never leave the edge; only the
// GENERATED line reaches a guest. The placeholder below is filled at bake time (empty ⇒ the story
// route degrades to silence). STORY_PARAMS_VERSION rides the cache key so a knob/prompt/marks
// change never serves a stale story (the i18n `v` discipline, ST4).
const STORY_FRAGMENTS = /*__STORY_FRAGMENTS__*/{}/*__/STORY_FRAGMENTS__*/;
const STORY_PARAMS_VERSION = /*__STORY_PV__*/"0"/*__/STORY_PV__*/;

// EX-QUIZ-EDGE (INV-59/INV-64): the PRIVATE per-work answer — the ONE correct option (no
// accept-set) plus the prize path — is BAKED IN here by the builder, never a public static byte.
// The placeholder below is filled at bake time (empty ⇒ the quiz route 404s). Map:
// workId → { answer: "raw string", prize: "gallery/…" }; the judge normalizes both sides and compares.
// Like the story fragments, this rides in `_worker.js`, the one bundle file Pages never serves.
const QUIZ_ANSWERS = /*__QUIZ_ANSWERS__*/{}/*__/QUIZ_ANSWERS__*/;

// EX-QUIZ-EDGE (INV-59): the quiz's OWN hourly rate-limit, keyed separately from the model bucket.
// A flood of guesses never touches rl: or the day model-call budget — this is the ONLY key a guess
// increments, and the ceiling is its own (the model allowance is untouched, EX-QUIZ-EDGE F1).
const QUIZ_TRIES_PER_HOUR = 60;

// EX-EDGE-GUARD (INV-51): the model is real money — a bot or a flood must never turn a model route
// into a bill. Three fences, all decided BEFORE any Anthropic call: (1) a bot gets ENGLISH straight
// from the baked source, no model call; (2) a single IP is rate-limited per hour; (3) a hard daily
// cap on model calls degrades gracefully — i18n falls to the English source, the story falls to
// silence (INV-19, absence loses nothing). Counters live in the same KV, self-expiring; a real
// guest crossing normally never meets any of them.
const BOT_RE = /bot|crawl|spider|slurp|curl|wget|python|java|scrapy|headless|phantom|lighthouse|monitor|preview|fetch|http[-_]?client|facebookexternalhit|embedly|bImag/i;
const RL_PER_HOUR = 40;          // model-triggering requests one IP may make in an hour
const DAY_MODEL_CAP = 800;       // hard ceiling on model calls per day, ALL sources together

function isBot(req) {
  const ua = req.headers.get("user-agent") || "";
  return !ua.trim() || BOT_RE.test(ua);          // no UA or a known non-human agent
}
function clientIp(req) {
  return req.headers.get("cf-connecting-ip") || "0.0.0.0";
}
async function overRate(env, req) {
  const win = Math.floor(Date.now() / 3600000);  // hourly bucket
  const k = "rl:" + win + ":" + clientIp(req);
  const n = parseInt((await env.@@NS_UPPER@@_I18N.get(k)) || "0", 10) + 1;
  await env.@@NS_UPPER@@_I18N.put(k, String(n), { expirationTtl: 3600 });
  return n > RL_PER_HOUR;
}
async function overBudget(env) {
  const k = "budget:" + new Date().toISOString().slice(0, 10);
  return parseInt((await env.@@NS_UPPER@@_I18N.get(k)) || "0", 10) >= DAY_MODEL_CAP;
}
async function chargeModelCall(env) {                 // count a call the moment we commit to it
  const k = "budget:" + new Date().toISOString().slice(0, 10);
  const n = parseInt((await env.@@NS_UPPER@@_I18N.get(k)) || "0", 10) + 1;
  await env.@@NS_UPPER@@_I18N.put(k, String(n), { expirationTtl: 172800 });
}
function englishFrom(src, plainGreet) {                // the baked English, served AS the "translation";
  const titles = {};                                   // plainGreet = the dead-account English day —
  for (const id of Object.keys(src.titles || {})) titles[id] = src.titles[id];
  const quizzes = {};                                  // one plain hello, no daypart flourish (INV-68)
  for (const q of (src.quizzes || [])) if (q && q.id) quizzes[q.id] = q;
  const hello = src.plain || "hello";
  const greet = plainGreet
    ? { night: [hello], morning: [hello], day: [hello], evening: [hello] }
    : src.greet;
  return Object.assign({}, src.strings, { greet: greet, titles: titles, dir: "ltr",
                                          quizzes: quizzes });
}

// EX-EDGE-DEAD (INV-68): a dead model ACCOUNT — a billing/credit/auth refusal, i.e. a 4xx other
// than 429 — flags the HOUR in KV; behind the flag no model call is attempted or charged. A 429,
// a 5xx, or a network throw stays transient and never raises the flag. The TTL is the ~1h knob.
const DEAD_KEY = "dead:model";
const DEAD_TTL = 3600;
async function modelDead(env) { return !!(await env.@@NS_UPPER@@_I18N.get(DEAD_KEY)); }
function deathStatus(e) {                              // the throw carries "model <status>"
  const m = /^model (\d{3})/.exec((e && e.message) || "");
  const s = m ? +m[1] : 0;
  // The requirement names the class member by member: the low-balance 400 and a revoked key's
  // 401/403. A 404 names a missing resource — a model id retired out from under the bundle — and a
  // 429 is a flood; both stay transient, so a retirement never darkens every language for an hour.
  return (s >= 400 && s < 500 && s !== 429 && s !== 404) ? s : 0;
}
async function markDead(env) { await env.@@NS_UPPER@@_I18N.put(DEAD_KEY, "1", { expirationTtl: DEAD_TTL }); }

// EX-STORY-FILL (INV-107): the two ways a model call ends without lines. The answer-reader names the
// class it is in as it throws, carrying that name on its own FIELD so the message keeps the plain
// "model <status>" shape the dead-account read above is anchored on. A refusal stop reason and a body
// that does not parse are the EMPTY class — a second ask meets the same fragments and the same prompt.
// A non-ok status and a network throw are the TRANSIENT class — a second ask may pass. (The third
// member of the empty class comes from the route's own line filter, not from here.)
function classed(message, cls) {
  const e = new Error(message);
  e.cls = cls;
  return e;
}
// The refusal record: an empty answer for ONE work, remembered for the hour the dead flag also takes.
const NEG_PREFIX = "neg:";
const NEG_TTL = 3600;
const LOCK_TTL = 60;                                   // the backstop for a worker that dies mid-call
async function rememberEmpty(env, key) {
  await env.@@NS_UPPER@@_I18N.put(NEG_PREFIX + key, "1", { expirationTtl: NEG_TTL });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === "/api/visitor") return visitor(req, env, url);
    if (url.pathname === "/api/story") return story(req, env);
    if (url.pathname === "/api/quiz") return quiz(req, env);
    if (url.pathname === "/api/geo") return geo(req);
    if (url.pathname !== "/api/i18n") return new Response("not found", { status: 404 });
    const lang = (url.searchParams.get("lang") || "").toLowerCase();
    const v = url.searchParams.get("v") || "";
    // sane tags only — a locale code never reaches the prompt as free text (prover I5)
    if (!TAG_RE.test(lang) || !/^[\w.-]{1,40}$/.test(v)) {
      return new Response("bad request", { status: 400 });
    }

    const key = v + ":" + lang;
    const hit = await env.@@NS_UPPER@@_I18N.get(key);            // cache first — one model call per
    if (hit) return json(hit);                          // language-version, ever (prover I6)

    const srcRes = await env.ASSETS.fetch(new URL("/i18n_source.json", url.origin));
    if (!srcRes.ok) return new Response("source missing", { status: 500 });
    const src = await srcRes.json();
    if (v !== String(src.version)) return new Response("stale version", { status: 409 });

    // EX-EDGE-GUARD: a bot, or a day already at its cap, gets ENGLISH from the source — no model
    // call, and NOT cached under this lang (a real speaker of it later still earns a real pass)
    // the death check rides the same pre-call fence line, so the served English is never cached
    // under the asked locale by construction (EX-EDGE-DEAD — the same early return as the bot path)
    if (await modelDead(env)) return json(JSON.stringify(englishFrom(src, true)));
    if (isBot(req) || await overBudget(env)) return json(JSON.stringify(englishFrom(src)));
    if (await overRate(env, req)) {
      return new Response("slow down", { status: 429, headers: { "Retry-After": "60" } });
    }

    const lock = "lock:" + key;                         // best-effort single flight (a burst
    if (await env.@@NS_UPPER@@_I18N.get(lock)) {                 // warms, it never fans out)
      return new Response("warming", { status: 503, headers: { "Retry-After": "3" } });
    }
    await env.@@NS_UPPER@@_I18N.put(lock, "1", { expirationTtl: 60 });

    await chargeModelCall(env);                         // count it the moment we commit to the model
    let out;
    try {
      out = await translate(env.ANTHROPIC_API_KEY, lang, src);
    } catch (e) {
      if (deathStatus(e)) {                             // the ACCOUNT is dead — flag the hour and
        await markDead(env);                            // answer the English day at once (INV-68);
        return json(JSON.stringify(englishFrom(src, true)));   // the dying call stays charged
      }
      // the reason (never a secret): "model 401", "refused", a parse failure — debuggable by curl
      return new Response("model unavailable: " + ((e && e.message) || "?"), { status: 502 });
    }
    if (!validate(out, src)) return new Response("malformed", { status: 502 });
    await env.@@NS_UPPER@@_I18N.put(key, JSON.stringify(out));
    return json(JSON.stringify(out));
  },
};

// EX-LANG-GEO (INV-1): the ARRIVING COUNTRY, and nothing else — Cloudflare already knows it at the
// edge (`request.cf.country`, the `cf-ipcountry` header as the fallback). The client uses it ONLY to
// narrow the language corner to the tongues that country actually speaks; the code never leaves the
// browser after that (never sent to GA, never on a beat — the closed ladder holds, INV-1). No IP, no
// identity, nothing stored. `no-store` because the answer is per-visitor: a shared/CDN cache would
// hand one guest's country to the next, so this route is the ONE /api answer that is never cached.
function geo(req) {
  const cc = (req.cf && req.cf.country) || req.headers.get("cf-ipcountry") || "";
  return new Response(JSON.stringify({ c: cc }), {
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

// EX-MEMORY (INV-43): the coat-check record — seen-work ids under a random token, nothing else.
// MERGE-never-replace (two tabs may write, M3), ~500 newest kept (M2), every write re-arms the
// ~180-day expiry; shaped tokens/ids only — free-form strings never reach KV keys.
async function visitor(req, env, url) {
  if (req.method === "GET") {
    const t = url.searchParams.get("t") || "";
    if (!TOKEN_RE.test(t)) return new Response("bad request", { status: 400 });
    const rec = await env.@@NS_UPPER@@_I18N.get("v:" + t);
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
    const adds = p.add.map(String).filter((x) => ID_RE.test(x)).slice(0, 100);
    let cur;
    try { cur = JSON.parse((await env.@@NS_UPPER@@_I18N.get("v:" + t)) || '{"seen":[]}'); }
    catch (e) { cur = { seen: [] }; }
    const set = new Set(Array.isArray(cur.seen) ? cur.seen : []);
    for (const a of adds) set.add(a);
    const seen = Array.from(set).slice(-500);          // the cap keeps the NEWEST
    await env.@@NS_UPPER@@_I18N.put("v:" + t, JSON.stringify({ seen }),
                           { expirationTtl: 15552000 });
    return json(JSON.stringify({ ok: true, n: seen.length }));
  }
  return new Response("method not allowed", { status: 405 });
}

// EX-STORY-EDGE (INV-47): the told story, written on demand over ONLY the private fragments.
// The guest's POST carries just the ORDERED ids + variant + language; the answer is kept in KV
// forever under a key of that ordered sequence + variant + language + the story-params version
// (ST4) — one model call per distinct walk, $0 after. A malformed answer is never served; if the
// voice cannot speak (no fragments baked, model down/refuses, malformed) the walk simply carries
// no lines and loses nothing (CS-8, INV-19 — the story is enhancement, its absence is silence).
async function story(req, env) {
  if (req.method !== "POST") return new Response("method not allowed", { status: 405 });
  // no fragments baked in (story shipped off / not this bundle) ⇒ silence, never a broken frame
  if (!STORY_FRAGMENTS || !Object.keys(STORY_FRAGMENTS).length) {
    return new Response("no story", { status: 404 });
  }
  const raw = await req.text();
  if (raw.length > 4096) return new Response("too big", { status: 413 });
  let p;
  try { p = JSON.parse(raw); } catch (e) { return new Response("bad request", { status: 400 }); }
  const ids = Array.isArray(p.ids) ? p.ids.map(String) : null;
  const variant = String(p.variant || "");
  const lang = String(p.lang || "").toLowerCase();
  const one = p.one === true;                          // a one-work ask marks itself (EX-STORY-FILL)
  // shaped input only — an id is digits, the variant one of A/B/C, the tag the i18n grammar (ST/I5);
  // free-form text never reaches the prompt or a KV key
  if (!ids || !ids.length || ids.length > 60 || !ids.every((x) => ID_RE.test(x))
      || !/^[ABC]$/.test(variant) || !TAG_RE.test(lang) || (one && ids.length !== 1)) {
    return new Response("bad request", { status: 400 });
  }
  // only ids we actually hold a fragment for — the ORDER the client sent is preserved (the cache key)
  const known = ids.filter((id) => STORY_FRAGMENTS[id]);
  if (!known.length) return new Response("no story", { status: 404 });

  // the ordered sequence hashes into a bounded KV key (a raw join can exceed KV's key limit).
  // EX-STORY-FILL (INV-107): a one-work ask keys under its OWN shape, so a portion that happens to
  // hold that single work and the ask for that same work keep separate entries.
  const seq = await sha256hex(known.join(","));
  const key = (one ? "s1:" : "s:") + STORY_PARAMS_VERSION + ":" + variant + ":" + lang + ":" + seq;
  const hit = await env.@@NS_UPPER@@_I18N.get(key);            // cache first — one model call per walk, ever
  if (hit) return json(hit);

  // EX-STORY-FILL (INV-107): a one-work key whose answer came back empty is remembered for an hour,
  // ahead of every fence and every model call — a work the model keeps leaving wordless costs one
  // call an hour, and no rate slot in between. A PORTION's key carries no such record: an owed
  // portion's re-asks must reach the model (the 2026-07-22 recovery, EX-STORY).
  if (one && await env.@@NS_UPPER@@_I18N.get(NEG_PREFIX + key)) {
    return new Response("no line", { status: 502 });
  }

  // EX-EDGE-GUARD: a cached walk is still served above; an UNCACHED one that would call the model
  // is refused to a bot or a capped day (silence — the story is enhancement, INV-19), and a flooding
  // IP is throttled — the narrator never becomes a money tap.
  if (isBot(req) || await overBudget(env) || await modelDead(env)) {
    return new Response("no story", { status: 404 }); // the dead hour keeps the story's own silence
  }
  if (await overRate(env, req)) {
    return new Response("slow down", { status: 429, headers: { "Retry-After": "60" } });
  }

  // EX-STORY-FILL (INV-107): the single-flight lock lives as long as the MODEL CALL. The request
  // that lays it takes it away at each of its own exits — the served plot, the plot that left no
  // line, and the throw alike; a request that met a standing lock owns none and deletes none, so
  // single flight survives. The expiry is the backstop for a worker that dies with the call in
  // flight. Before this, the lock outlived every call by its full minute and the client's own
  // re-asks (2.5s, 6s) met it instead of the model — the retry ladder had never once run.
  const lock = "lock:" + key;
  if (await env.@@NS_UPPER@@_I18N.get(lock)) {
    return new Response("warming", { status: 503, headers: { "Retry-After": "3" } });
  }
  // The lock's VALUE names the request that laid it, and the delete happens only while that name
  // still stands: a call that outlives the expiry must never take away the lock a later request laid.
  const mine = String(Date.now()) + ":" + Math.random().toString(36).slice(2);
  await env.@@NS_UPPER@@_I18N.put(lock, mine, { expirationTtl: LOCK_TTL });
  let held = true;
  const unlock = async () => {
    if (!held) return;
    held = false;
    try {
      if ((await env.@@NS_UPPER@@_I18N.get(lock)) === mine) await env.@@NS_UPPER@@_I18N.delete(lock);
    } catch (e) {}
  };

  try {
    await chargeModelCall(env);                        // count it the moment we commit to the model
    let out;
    try {
      out = await narrate(env.ANTHROPIC_API_KEY, known, variant, lang);
    } catch (e) {
      // EX-EDGE-DEAD (INV-68): a 4xx other than 429 names a dead ACCOUNT — flag the hour from this
      // route the way the i18n route does, so a failing model stops being paid for.
      if (deathStatus(e)) await markDead(env);
      if (one && e && e.cls === "empty") await rememberEmpty(env, key);
      return new Response("model unavailable: " + ((e && e.message) || "?"), { status: 502 });
    }
    // EX-STORY-FILL (INV-107): the answer is taken line by line — a spoiled entry costs its own work
    // and its neighbours keep their lines. A plot that left no line at all is answered 502 and written
    // nowhere, so the next rung reaches the cache, a fence, or the model.
    const lines = keepLines(out, known);
    if (!lines.length) {
      if (one) await rememberEmpty(env, key);
      return new Response("malformed", { status: 502 });
    }
    const body = JSON.stringify({ story_variant: variant, lines: lines });
    await env.@@NS_UPPER@@_I18N.put(key, body);        // a short plot caches the way a whole one does
    return json(body);
  } finally {
    await unlock();                                    // every exit of the request that laid it, a
  }                                                    // storage fault on the way to the model included
}

async function narrate(apiKey, ids, variant, lang) {
  // ONLY the curated fragments cross to the model — title/place/subject/light are public grounding,
  // the note is his own words (adapted, never quoted). The client already fixed the ORDER (the light
  // lean is deterministic, in the browser — EX-STORY-ORDER); the model writes lines, never sequence.
  const works = ids.map((id, i) => {
    const f = STORY_FRAGMENTS[id] || {};
    return {
      n: i + 1, id: String(id),
      title: f.title || "", place: f.place || "",
      subject: f.subject || "", light: (f.tod || []).join("+"),
      note: f.note || "",
    };
  });
  const prompt =
    'You are a quiet narrator walking beside a visitor through a small photography exhibition. ' +
    'For EACH work write ONE short line — the association the picture leaves, the way one murmurs ' +
    'beside a print. Reply in the language with BCP-47 tag "' + lang + '". Laws: at most a dozen ' +
    'words per line; slightly abstract and associative, never a plain description of the photograph; ' +
    'where a work carries the artist\'s own NOTE, let the line grow from its sense (adapt, never quote ' +
    'it raw); with no note, stay to what the title, place, subject, and light honestly give. NEVER ' +
    'invent a name, person, event, weather, or history the fragments do not hold. NEVER reveal ' +
    'technique — no camera, lens, exposure, editing, filter, montage, or cut is ever named. No ' +
    'exclamation marks, no salesmanship. The works are in walking order and lean into a small arc — a ' +
    'way in, a turn, a quiet close — so let each line sit beside its neighbours. Reply with JSON only: ' +
    '"lines" is an array of {"id","line","source"} covering EVERY work in the given order, ids ' +
    'verbatim; "source" is "note" when the artist\'s note shaped the line, otherwise "facts".\n' +
    'Works, in walking order:\n' + JSON.stringify(works);
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: "claude-haiku-4-5",
      max_tokens: 4000,
      messages: [{ role: "user", content: prompt }],
      output_config: { format: { type: "json_schema", schema: storyShape() } },
    }),
  });
  if (!r.ok) throw classed("model " + r.status, "transient");
  let msg;
  try { msg = await r.json(); } catch (e) { throw classed("unreadable", "empty"); }
  if (msg.stop_reason === "refusal") throw classed("refused", "empty");
  try {
    return JSON.parse(((msg.content || []).find((b) => b.type === "text") || {}).text);
  } catch (e) {
    throw classed("unreadable", "empty");
  }
}

function storyShape() {
  const s = { type: "string" };
  return {
    type: "object",
    properties: {
      lines: {
        type: "array",
        items: {
          type: "object",
          properties: { id: s, line: s, source: { type: "string", enum: ["note", "facts"] } },
          required: ["id", "line", "source"],
          additionalProperties: false,
        },
      },
    },
    required: ["lines"],
    additionalProperties: false,
  };
}

// EX-STORY-FILL (INV-107): the answer is taken LINE BY LINE. Every entry the model wrote that is
// well-formed stands — a line with characters in it, a provenance stamp of "note" or "facts", and an
// id among the ids this request asked for — and the first entry for an id wins. A spoiled entry costs
// its own work alone; its neighbours keep their lines. Before this, one blank line among ten made the
// whole plot malformed and a walk of ten works went silent.
function keepLines(out, ids) {
  try {
    const asked = {};
    for (const id of ids) asked[String(id)] = true;
    const seen = {};
    const kept = [];
    for (const l of (out && Array.isArray(out.lines) ? out.lines : [])) {
      if (!l || typeof l.line !== "string" || !l.line.trim()) continue;
      if (l.source !== "note" && l.source !== "facts") continue;
      const id = String(l.id);
      if (!asked[id] || seen[id]) continue;
      seen[id] = true;
      kept.push({ id: id, line: l.line, source: l.source });
    }
    return kept;
  } catch (e) {
    return [];
  }
}

async function sha256hex(str) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

function json(body) {
  return new Response(body, {
    headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=86400" },
  });
}

// EX-QUIZ-EDGE (INV-59): the quiz's OWN attempt fence — keyed "q:<hour>:<ip>", its own ceiling.
// This is the ONLY rate-limit counter a guess ever touches. The model-path rate-limit ("rl:")
// and the day model-call budget are never incremented here — a guess costs nothing (no model call).
async function overQuizRate(env, req) {
  // No KV bound (e.g. a preview environment with no namespace) ⇒ skip the flood fence rather than
  // throw. A guess is a deterministic compare with no cost, so an unlimited fence loses nothing; this
  // lets /api/quiz JUDGE with zero infra setup. Production keeps @@NS_UPPER@@_I18N and keeps the fence.
  if (!env || !env.@@NS_UPPER@@_I18N) return false;
  const win = Math.floor(Date.now() / 3600000);        // hourly bucket
  const k = "q:" + win + ":" + clientIp(req);
  const n = parseInt((await env.@@NS_UPPER@@_I18N.get(k)) || "0", 10) + 1;
  await env.@@NS_UPPER@@_I18N.put(k, String(n), { expirationTtl: 3600 });
  return n > QUIZ_TRIES_PER_HOUR;
}

// EX-QUIZ-EDGE (INV-59): normalize at the edge — HARD canonicalization so spacing, punctuation,
// hyphens, and case never decide a verdict. NFKC-fold, lower-case, then keep letters only — so
// "New York", "new-york", "newyork", and "NEW YORK" all collapse to one normalized form (and the
// same across Cyrillic and other scripts, the \p{L} property covers them all). This is the ONE
// normalizer the accept-set was baked against; the client never normalizes (it sends the raw typed
// answer), so JS↔worker parity holds by construction.
function normAnswer(s) {
  return (s || "").normalize("NFKC").toLowerCase().replace(/[^\p{L}]/gu, "");
}

// EX-QUIZ-EDGE (INV-64): POST {id, answer} → bare win/miss verdict (no model, no budget touch).
// Shape-check → rate-check → look up the PRIVATE single answer → normalize both sides → compare.
// A hit replies {ok:true, prize:"gallery/…"}; a miss replies {ok:false}.
// Off / no answer baked / unknown id ⇒ 404 and the walk loses nothing (INV-19 / CS-8).
// The 4-option model: the client POSTs the tapped option value; the edge normalizes both sides
// (NFKC-fold, lower-case, letters only) and compares to the ONE private correct answer (INV-64).
async function quiz(req, env) {
  if (req.method !== "POST") return new Response("method not allowed", { status: 405 });
  // no answers baked in (quiz shipped off / nothing baked) ⇒ 404, silence
  if (!QUIZ_ANSWERS || !Object.keys(QUIZ_ANSWERS).length) {
    return new Response("no quiz", { status: 404 });
  }
  const raw = await req.text();
  if (raw.length > 512) return new Response("too big", { status: 413 });
  let p;
  try { p = JSON.parse(raw); } catch (e) { return new Response("bad request", { status: 400 }); }
  // shaped input only — id is the engine's id grammar (same as the story), answer is bounded
  const id = String(p.id || "");
  const answer = String(p.answer || "");
  if (!ID_RE.test(id) || answer.length > 100) {
    return new Response("bad request", { status: 400 });
  }
  // look up the work's private answer; absent id ⇒ 404 (INV-64: one correct option, no accept-set)
  const entry = QUIZ_ANSWERS[id];
  if (!entry) return new Response("no quiz", { status: 404 });
  // the quiz's OWN attempt fence (not the model bucket — a guess never spends a model allowance)
  if (await overQuizRate(env, req)) {
    return new Response("slow down", { status: 429, headers: { "Retry-After": "60" } });
  }
  // compare the tapped option (normalized) against the ONE private correct answer (INV-64)
  const hit = normAnswer(entry.answer) === normAnswer(answer);
  if (hit) return json(JSON.stringify({ ok: true, prize: entry.prize }));
  return json(JSON.stringify({ ok: false }));
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
                      share_copied: s, series: s, room_back: s, enjoy: s, quiz_ask: s,
                      quiz_submit: s, quiz_win: s, quiz_wrong: s, gift_ask: s, gift_yes: s,
                      gift_no: s, gift_buy: s },
        required: ["ask", "exit", "more", "q_more", "q_spent", "share_label", "share_copied",
                   "series", "room_back", "enjoy", "quiz_ask",
                   "quiz_submit", "quiz_win", "quiz_wrong", "gift_ask", "gift_yes", "gift_no",
                   "gift_buy"],
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
    // the always-shown chrome must be filled; gift_buy is the OPTIONAL buy line (empty by default),
    // so it is translatable (in the shape) but never required non-empty (a gallery may not sell)
    for (const k of ["ask", "exit", "q_more", "q_spent", "share_label", "share_copied", "series",
                     "room_back", "enjoy", "quiz_ask",
                     "quiz_submit", "quiz_win", "quiz_wrong", "gift_ask", "gift_yes", "gift_no"]) {
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
