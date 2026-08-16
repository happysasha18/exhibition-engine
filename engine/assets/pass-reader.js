/*!pass-reader.js*/
// The delivery pack's reader — the play side of PASS-API-V1 §4.4d. Fetched separately, the way the
// host and the instruments are, so the walk's own bundle carries the door alone and none of this.
//
// WHAT IT CLOSES. The site composes a score for an ordered pair at build time and ships it in a
// PACK: a head, one template per passage shape, one row per ordered pair, and the rows split into
// one file per departing work. The settings record carries the pack's ADDRESSES and no content
// (the site's own lab/build-delivery-v1.py writes them; the block lands under `pass.packs`). Before
// this file no byte a visitor ran read that name, so every crossing fell back to the walk's own
// glide in silence and a whole route drive asked the wire for no shard at all.
//
// THE ROW'S OWN SHAPE PICKS THE TEMPLATE. The client's inline road takes one template per
// INSTRUMENT (`pass.scoreTemplates[<instrument>]`, engine/client/01a-pass.js). A pack does not work
// that way: it carries one template per PASSAGE SHAPE — twenty-five of them in the pack that ships
// today — and each row names its own shape as its first entry, indexing the head's `shapes` list.
// So the template is chosen per row, never per instrument, and a reader that assumed otherwise
// would fill every pair from one shape's score.
//
// NOTHING WAITS ON THE WIRE. `passScoreFor` answers synchronously inside `declare`, so this reader
// only ever hands back what has ALREADY arrived. The shard for a work's outgoing crossings is asked
// for when the walk LANDS on that work; a crossing whose shard has arrived plays, and one whose
// shard has not glides, with the reason on the diagnostic surface. There is no blocking road here
// and no retry: a file that refused once stays refused for the visit, exactly as an instrument file
// does, because a walk that re-asked every step would spend the visit fetching one refusal.
//
// EVERY FETCHED FILE IS WEIGHED BEFORE IT IS READ. The settings record gives each pack a digest,
// and that digest is the SHA-256 of the pack's own manifest, which in turn carries the SHA-256 of
// every other file in the pack. So the manifest is weighed against the record, and every later file
// against the manifest — one chain, rooted in the settings record the bake wrote. A file whose
// bytes weigh to anything else is refused with both digests named, and the crossing glides.
(function () {
  var join = window.__@@NS@@PassReader;
  if (typeof join !== "function") return;

  // The version this file declares, carried onto the diagnostic surface with everything else it
  // reports. This file is the ENGINE'S own, served from the engine's own bake beside the host and
  // fetched at a relative address, so it is pinned the way pass-layer.js is: by the bake that wrote
  // it. The digests below weigh the SITE'S files — the pack — which is a different thing and is why
  // those are checked byte for byte.
  var READER_VERSION = "1";

  function hexOf(buf) {
    var b = new Uint8Array(buf), s = "", i;
    for (i = 0; i < b.length; i++) s += (b[i] < 16 ? "0" : "") + b[i].toString(16);
    return s;
  }

  // WHETHER THIS PAGE CAN READ A PACK AT ALL, asked once and answered in plain words. Three things
  // are needed: a fetch to bring a file, a decoder to read its bytes as text, and a digest engine to
  // weigh them before they are read. Reading unweighed bytes because the scales are missing would
  // make the digest a courtesy, and it is a condition of reading.
  function noRoad() {
    if (typeof fetch !== "function") return "this page cannot fetch a file";
    if (typeof TextDecoder !== "function") return "this page cannot read fetched bytes as text";
    var sub = window.crypto && window.crypto.subtle;
    if (!sub || typeof sub.digest !== "function") {
      return "this page offers no digest engine, so a pack's files cannot be weighed";
    }
    return null;
  }

  // One value written at one leaf of a score, addressed by the path that reaches it. This is the
  // play side of the site's own fill_from_row (lab/build-delivery-v1.py): the same slot paths, the
  // same order, the same assignment. A path that does not reach a record refuses the WHOLE score
  // rather than filling half of one — and the fill runs on a COPY of the template, so a row refused
  // halfway leaves nothing behind, which is the law the inline road already keeps.
  function setAt(doc, path, value) {
    var node = doc, i;
    for (i = 0; i < path.length - 1; i++) {
      node = node[path[i]];
      if (!node || typeof node !== "object") return false;
    }
    if (!node || typeof node !== "object") return false;
    node[path[path.length - 1]] = value;
    return true;
  }

  function make(env) {
    var packs = env && env.packs;
    var note = (env && typeof env.note === "function") ? env.note : function () {};
    // The family roll of §4.4f, handed over by the walk's own bundle. It is the ONE roll both fill
    // roads run on: this file never mints a seed of its own, so a pack-served crossing and an
    // inline one breathe by the same rule, and a pinned visit pins both.
    var breath = (env && typeof env.breath === "function") ? env.breath : null;
    if (!packs || typeof packs !== "object") return null;
    var names = Object.keys(packs);
    if (!names.length) return null;

    var road = noRoad();
    var sub = road ? null : window.crypto.subtle;
    var decoder = road ? null : new TextDecoder();
    var open = {};        // pack name → the pack's own record, below
    var warmed = {};      // departing work id → true, once it has been asked for
    var said = {};        // one reason is put on the surface once, never once per crossing

    function once(name, why) {
      if (said[name]) return;
      said[name] = true;
      note(name, why);
    }

    // ONE FILE OF ONE PACK: fetched, weighed, and read as JSON. `want` is the digest the file must
    // weigh to, in plain hex. Every road ends in `ok` with the document or in `no` with the reason.
    function fetchJson(pk, rel, want, ok, no) {
      var bytes = null;
      fetch(pk.base + rel, { credentials: "omit" }).then(function (r) {
        if (!r.ok) throw new Error("the server answered " + r.status);
        return r.arrayBuffer();
      }).then(function (buf) {
        bytes = buf;
        return sub.digest("SHA-256", buf);
      }).then(function (d) {
        var got = hexOf(d);
        if (want && got !== want) {
          throw new Error("its bytes weigh to " + got.slice(0, 16) + "…, and the pack's manifest "
                        + "says " + String(want).slice(0, 16) + "…");
        }
        ok(JSON.parse(decoder.decode(bytes)));
      })["catch"](function (e) { no(e && e.message ? e.message : String(e)); });
    }

    // The digest the pack's manifest records for one of its files, or null when the manifest names
    // no such file — which is itself an answer: the manifest is the pack's own index of what it
    // serves, so a file missing from it is a file the pack does not have.
    function digestOf(pk, rel) {
      var row = pk.manifest && pk.manifest.files && pk.manifest.files[rel];
      return (row && typeof row.sha256 === "string") ? row.sha256 : null;
    }

    // THE PACK, OPENED ONCE. The manifest is weighed against the digest the settings record carries
    // — the record's digest IS the manifest's own SHA-256 — and every later file against the
    // manifest. The head says which shapes the pack knows; the templates carry one score per shape;
    // `authored.json` carries whole scores that stand as authored rather than being filled from a
    // row, keyed by the ordered pair. A pack whose head names no shapes cannot be FILLED here — its
    // rows are of another form — so it opens for its authored scores alone and says so.
    // A LANDING THAT ARRIVES WHILE THE PACK IS STILL OPENING IS HELD, NEVER DROPPED. The pack is
    // opened by the first landing of the visit, and the walk can land again — a restored place, a
    // step taken while the head is still crossing the wire — before that open has finished. Those
    // landings are the ones whose shards a visitor is most likely to need, so each waits here and
    // is answered the moment the open settles, either way.
    function packSettled(pk, state) {
      pk.state = state;
      var q = pk.waiting;
      pk.waiting = [];
      for (var i = 0; i < q.length; i++) q[i]();
    }
    function packOpen(pk, done) {
      if (pk.state === "read" || pk.state === "refused") return done();
      pk.waiting.push(done);
      if (pk.state === "asked") return;
      pk.state = "asked";
      fetchJson(pk, pk.files.manifest, pk.digest, function (manifest) {
        pk.manifest = manifest;
        pk.hasShard = {};
        var list = manifest && manifest.worksWithAShard;
        if (Object.prototype.toString.call(list) === "[object Array]") {
          for (var i = 0; i < list.length; i++) pk.hasShard[String(list[i])] = true;
        }
        var left = 3;
        function one() {
          if (--left) return;
          pk.fills = !!(pk.head && Object.prototype.toString.call(pk.head.shapes) === "[object Array]"
                        && pk.templates);
          if (!pk.fills) {
            pk.why = pk.why || ("its head names no passage shapes, so its rows fill by another "
                              + "rule than this reader's; only its authored scores are read");
            once(pk.name, pk.why);
          }
          packSettled(pk, "read");
        }
        function part(rel, into, needed) {
          var want = digestOf(pk, rel);
          if (!want) {
            if (needed) pk.why = "its manifest names no «" + rel + "»";
            return one();
          }
          fetchJson(pk, rel, want, function (doc) { pk[into] = doc; one(); },
                    function (why) {
                      if (needed) pk.why = rel + ": " + why;
                      once(pk.name + "/" + rel, why);
                      one();
                    });
        }
        part(pk.files.head, "head", true);
        part(pk.files.templates, "templates", true);
        part(pk.files.authored, "authored", false);
      }, function (why) {
        pk.why = pk.files.manifest + ": " + why;
        once(pk.name, pk.why);
        packSettled(pk, "refused");
      });
    }

    // THE SHARD FOR ONE DEPARTING WORK. A pack that cannot be filled asks for nothing: its rows are
    // of a form this reader does not fill, so a shard of them would be bytes a visitor pays for and
    // nothing reads. A work the manifest does not name carries no shard at all, and that is
    // recorded without a request — the manifest is the pack's own answer to the question.
    function shardAsk(pk, workId) {
      if (!pk.fills || pk.shards[workId]) return;
      var rel = String(pk.files.rows).replace("{departing}", workId);
      if (!pk.hasShard[workId]) {
        pk.shards[workId] = { state: "absent", rows: null,
                              why: "the pack carries no shard for this work — it stands outside the "
                                 + (pk.manifest.counts ? pk.manifest.counts.shards : 0)
                                 + " the pack was built over" };
        return;
      }
      var rec = { state: "asked", rows: null, why: null };
      pk.shards[workId] = rec;
      fetchJson(pk, rel, digestOf(pk, rel), function (rows) {
        rec.state = "read";
        rec.rows = rows;
      }, function (why) {
        rec.state = "refused";
        rec.why = rel + ": " + why;
        once(pk.name + "/" + rel, rec.why);
      });
    }

    // THE ROW'S OWN SHAPE, AND THE TEMPLATE IT NAMES. The row's first entry indexes the head's
    // `shapes`; that name keys the templates. Twenty-five shapes ship today and one row picks one of
    // them, which is the whole difference between a pack and the inline road's one template per
    // instrument.
    function fillFrom(pk, key, row) {
      if (Object.prototype.toString.call(row) !== "[object Array]" || !row.length) {
        return no(pk, key, "its row is no list of values");
      }
      // THE ROW'S FAMILY BOUNDS, WHEN IT CARRIES THEM (§4.4f). A row is a list of numbers, so the
      // bounds travel as its LAST entry and are recognised by being a record rather than a number:
      // the pack keeps one row shape, and a row that carries none is the row it has always been.
      // The values are read here and applied AFTER every measured number is in place, below.
      var fam = null, count = row.length - 1;
      var tail = row[row.length - 1];
      if (tail && typeof tail === "object" && Object.prototype.toString.call(tail) !== "[object Array]") {
        fam = tail;
        count -= 1;
      }
      var shape = pk.head.shapes[row[0]];
      if (shape === undefined) {
        return no(pk, key, "its row names shape " + row[0] + ", and the pack's head names "
                         + pk.head.shapes.length);
      }
      var tpl = pk.templates[shape];
      if (!tpl || !tpl.score || Object.prototype.toString.call(tpl.slots) !== "[object Array]") {
        return no(pk, key, "its shape «" + shape + "» names no template in this pack");
      }
      if (tpl.slots.length !== count) {
        return no(pk, key, "its row carries " + count + " values and the shape «" + shape
                         + "» names " + tpl.slots.length + " slots");
      }
      var score = null;
      try { score = JSON.parse(JSON.stringify(tpl.score)); } catch (e) {}
      if (!score) return no(pk, key, "its shape «" + shape + "» carries no score to fill");
      for (var i = 0; i < tpl.slots.length; i++) {
        if (!setAt(score, tpl.slots[i], row[i + 1])) {
          return no(pk, key, "slot " + i + " of shape «" + shape + "» reaches nothing in its own "
                           + "template");
        }
      }
      // THE ROLL IS THE WALK'S OWN, NEVER THIS FILE'S. The bundle hands it over in this reader's
      // environment record, so the pack road and the inline road roll by one rule and one seed
      // ladder (§4.4f). A row that carries bounds on a walk that hands over no roll is refused
      // whole rather than filled flat: a score that quietly stopped breathing is the very defect
      // this section repairs, and it must never arrive in silence.
      if (fam) {
        if (typeof breath !== "function") {
          return no(pk, key, "its row carries family bounds and this walk hands the reader no roll");
        }
        var got = breath(key, fam);
        if (!got || got.why) return no(pk, key, got ? got.why : "the roll answered nothing");
        var at, ks = Object.keys(got.v);
        for (i = 0; i < ks.length; i++) {
          at = +ks[i];
          if (!(at >= 0) || at !== Math.floor(at) || at >= tpl.slots.length) {
            return no(pk, key, "its family bounds name slot «" + ks[i] + "», and the shape «"
                             + shape + "» names " + tpl.slots.length);
          }
          if (!setAt(score, tpl.slots[at], got.v[ks[i]])) {
            return no(pk, key, "the bounded slot " + at + " of shape «" + shape + "» reaches "
                             + "nothing in its own template");
          }
        }
        if (got.seed !== null && got.seed !== undefined) score.seed = got.seed;
      }
      return score;
    }

    function no(pk, key, why) {
      once(pk.name + ":" + key, why);
      return null;
    }

    // THE PAIR'S OWN SCORE, from what has already arrived. An authored score stands as authored and
    // wins; otherwise the pair's row is looked for in the departing work's shard. The composer keys
    // its rows on the pair in ONE canonical order with a tag saying which way the crossing runs
    // («…__ab» departs from the first id, «…__ba» from the second), and both directions live in the
    // DEPARTING work's shard, so both candidates are looked for there and nothing has to be inferred
    // about which order the two ids were written in.
    function scoreFor(key) {
      var i, ids = String(key).split("__");
      if (ids.length !== 2) return null;
      for (i = 0; i < names.length; i++) {
        var pk = open[names[i]];
        if (!pk || pk.state !== "read") continue;
        var authored = pk.authored && pk.authored[key];
        if (authored) return authored;
        if (!pk.fills) continue;
        var shard = pk.shards[ids[0]];
        if (!shard) { once(pk.name + ":" + ids[0], "no shard was ever asked for this work"); continue; }
        if (shard.state !== "read") {
          once(pk.name + ":" + key, shard.state === "asked"
               ? "its shard had not arrived when the crossing was declared"
               : shard.why);
          continue;
        }
        var row = shard.rows[key] || shard.rows[key + "__ab"]
                || shard.rows[ids[1] + "__" + ids[0] + "__ba"];
        if (row === undefined) {
          once(pk.name + ":" + key, "the pack's shard for this work carries no row for this pair");
          continue;
        }
        var score = fillFrom(pk, key, row);
        if (score) return score;
      }
      return null;
    }

    // THE WALK LANDED ON A WORK, so the shards for the crossings that LEAVE it are asked for now.
    // This is the one moment early enough: `passScoreFor` answers synchronously inside `declare`,
    // and a crossing is declared the instant the visitor moves, so a fetch begun there would always
    // be too late. Asked once per work; a work already asked for is never asked again.
    function warm(workId) {
      workId = String(workId || "");
      if (!workId || warmed[workId]) return;
      warmed[workId] = true;
      if (road) { once("road", road); return; }
      for (var i = 0; i < names.length; i++) {
        (function (pk) {
          packOpen(pk, function () { if (pk.state === "read") shardAsk(pk, workId); });
        })(open[names[i]]);
      }
    }

    // Every pack the settings record names, held as data before anything is fetched. A record entry
    // missing its base, its digest or its file names is refused here rather than at the first
    // crossing, and the pack is simply absent from what the reader can answer with.
    for (var i = 0; i < names.length; i++) {
      var e = packs[names[i]] || {};
      var digest = /^sha256:([0-9a-f]{64})$/.exec(String(e.digest || ""));
      if (typeof e.base !== "string" || !e.base || !digest || typeof e.rows !== "string") {
        once(names[i], "the settings record's entry carries no base address, digest and file names");
        continue;
      }
      open[names[i]] = {
        name: names[i], base: e.base, digest: digest[1], state: "shut", why: null,
        files: { manifest: String(e.manifest || "manifest.json"),
                 head: String(e.head || "head.json"),
                 templates: String(e.templates || "templates.json"),
                 authored: String(e.authored || "authored.json"),
                 rows: String(e.rows) },
        manifest: null, head: null, templates: null, authored: null,
        hasShard: {}, shards: {}, fills: false, waiting: [],
      };
    }
    names = Object.keys(open);
    if (!names.length) return null;

    // The reader's own half of the diagnostic surface: where each pack stands, why when it is
    // refused, and every shard this visit has asked for with its state. A crossing that glided
    // because a shard was missing is readable here without reading anything else.
    function report() {
      return {
        version: READER_VERSION, road: road, breathes: !!breath,
        packs: names.map(function (n) {
          var pk = open[n];
          return { name: n, base: pk.base, state: pk.state, why: pk.why, fills: pk.fills,
                   shapes: pk.head && pk.head.shapes ? pk.head.shapes.length : null,
                   templates: pk.templates ? Object.keys(pk.templates).length : null,
                   authored: pk.authored ? Object.keys(pk.authored).length : null,
                   shards: Object.keys(pk.shards).map(function (w) {
                     return { work: w, state: pk.shards[w].state, why: pk.shards[w].why,
                              rows: pk.shards[w].rows ? Object.keys(pk.shards[w].rows).length : 0 };
                   }) };
        }),
      };
    }

    return { scoreFor: scoreFor, warm: warm, report: report, version: READER_VERSION };
  }

  join({ version: READER_VERSION, make: make });
})();
