  // ---- EX-VERDICT (S-01): the diagnostics-only crossing verdict panel ---------------------------
  // Draws NOTHING and adds NOTHING to the DOM unless the address already carries
  // ?pass=diagnostics:on — the same key 01a-pass.js reads into the settings register and the same
  // register `passGet("diagnostics")` resolves off (session → site → default). A visitor without the
  // key runs none of the code below: the `if` guard is the whole of the fence, so a route walked
  // without the key leaves no element, no listener and no stored row behind.
  //
  // WHAT IT WATCHES. Every real, ANIMATED crossing (`cmd.kind === "step"`, never a `jump` — a jump
  // lands instantly and the picture layer declines to draw it by kind, so there is nothing on screen
  // for a person to judge) between two works (`cmd.from`/`cmd.to` both carry a work id — a door
  // landing is not a work and is left out, exactly as PASS-API leaves it out of a passage request).
  // The hook is a wrap of `passMark`, not of `dock`: `dock` is handed out BY VALUE on the diagnostic
  // adapter (`window.__@@NS@@Pass.adapter.dock`) the moment that object is built, so a later
  // reassignment of the `dock` binding would never reach a caller already holding that copy — the
  // very road this file's own test drives a landing through. `dock` itself calls the free variable
  // `passMark("dock", cmd, …)` on every real landing (01a-pass.js), and nothing anywhere holds a
  // captured copy of `passMark` the way it holds one of `dock`, so wrapping the FREE VARIABLE here
  // reaches every road to a landing there is, real gesture and adapter call alike.
  //
  // WHERE from/to/road/cues COME FROM. `cmd.from.id` / `cmd.to.id` are the two work ids the walk
  // itself named for this crossing (passWhere, 01a-pass.js). `road` and the cue list are not on the
  // command — the command carries only the SCORE (PASS_SCORE_FIELDS2 has no `road`) — so the matching
  // row of `passPassages` is found the same way `passEdgeRemember` already finds it (by the identity
  // of the score that played), and `road` is read straight off that row: the composer hands the genre
  // back under that exact name (`pass-composer.js`, `scoreFor`: `road: plan.road`), and his own word
  // is what keeps it — "this file called them «roads» until then; the word is his and it stays."
  // Each cue is named `<slot>:<instrument>` (`CUE_IDS` is `["pivot","travel","arrival"]`), which is
  // the same pair a person can actually see repeat. `durationMs` is `passCrossingMsOf(cmd)` — the
  // very reading the walk's own dwell classifier already takes, so the number a note is judged
  // against is the number the person actually watched.
  if (passGet("diagnostics") === "on") {
    const VERDICT_DEFS = [
      { key: "fire", label: "огонь" },
      { key: "ok", label: "ок" },
      { key: "skip", label: "мимо" },
    ];
    const verdictWalk = location.href;
    const verdictStartedAt = new Date().toISOString();
    const verdictRows = [];
    // A2/A1: one joined record per played step, in the order they landed — read by both the
    // collapsed-row list below and `verdictDump`'s export, so a number can never differ between
    // what a person sees in the panel and what the export hands them.
    const verdictHistory = [];
    let verdictN = 0;
    let verdictPending = null; // {from, to, road, cues, durationMs} — the crossing awaiting a verdict

    // ---- one small stylesheet, scoped to the panel's own id — no other file's CSS is touched ----
    //
    // WHY THE TOP, NOT THE BOTTOM (found the hard way, 2026-08-26/27). The bottom-right corner is
    // not free ground: `.ex-share` rides the shared `--ex-rail` there, and `.exh-capzone` (title,
    // told line, the quiz chip) spans the WHOLE width of the bottom band on a phone frame. A panel
    // anchored `bottom:12px;right:12px` sat its own real buttons — `.exv-dump` among them — directly
    // over both, at the very coordinate a real press would land on `#ex-share` or `.ex-quiz-chip`.
    // The browser's own hit test always resolves to whichever element is topmost there, so the two
    // suites reading this build measured a press to the SITE's controls landing on the PANEL's
    // instead — a verdict-JSON clipboard write where a room permalink was asked for, and a quiz
    // card that never opened because the chip's press never reached it.
    // `pointer-events` cannot fix this: the collision is not the panel's inert padding sitting over
    // live ground, it is one real, working button (`.exv-dump`) physically covering another
    // (`#ex-share`), and both must stay clickable at their own press.
    // Measured at 390×844 (the phone frame every row of this suite is taken on), the gap above
    // the hung work's own frame and below the top chrome (`#ex-sound`, the visit counter) is real
    // but short — about 130px between them — so the panel is also trimmed to fit inside it without
    // reaching into the picture: the verdict buttons and the dump control now share ONE row
    // instead of two, which is the height this docking spent to clear both the top controls and
    // the frame beneath it. `.exv-dump` keeps its own row-independent visibility (see the
    // `data-pending="0"` rule below) — the export stays reachable with no crossing pending, exactly
    // as it did before this row merged, because `.exv-row` itself is never hidden, only `.exv-btns`
    // inside it. The shadow is trimmed the same way: a wide blur painted past the panel's own box
    // still reads on the pixels just below it, which is the frame's own top edge — the byte-compare
    // this suite runs there caught it at a single channel step before the row above did.
    const style = document.createElement("style");
    style.textContent =
      "#ex-verdict{position:fixed;right:12px;" +
      "top:calc(env(safe-area-inset-top,0px) + 58px);z-index:2147483647;" +
      // THE VIEWPORT IS THE WRONG CEILING, and it was the ceiling until 2026-09-01. The docking
      // above trimmed the panel's own fixed rows to clear the picture, and then let the STEP LIST
      // grow to the bottom of the screen: with `flex:1 1 auto` on `.exv-list` and the whole
      // viewport allowed here, the panel reached the picture again as soon as a walk landed enough
      // crossings to fill it — which is every real walk, and which is why the byte-compare this
      // suite runs over the arriving work's own box read the panel's own rows as the difference
      // between the two roads. The ceiling is not a number this file can type: where the gap ends
      // is the hung picture's own top edge, and that moves with the viewport, the safe area, the
      // frame's aspect and the layout. So it is MEASURED, in `verdictFit` below, and this rule
      // carries only the fallback for the instant before the first measurement lands.
      "max-height:calc(100dvh - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px)" +
      " - 58px - 12px);display:flex;flex-direction:column;" +
      "background:rgba(20,20,20,.92);color:#fff;font:12px/1.4 system-ui,sans-serif;" +
      // THE EDGE IS PAINTED INSIDE THE PANEL'S OWN BOX. An outer shadow is by definition ink
      // outside that box, and the box now ends exactly at the picture's own top edge — so however
      // narrow the blur is trimmed to, it lands on the picture, and the byte-compare over the
      // arriving work's box reads it (2026-09-01: three rows deep across the panel's own columns,
      // the last of this row's difference once the height was bounded). `inset` keeps the edge the
      // shadow was there to draw and paints none of it outside.
      "padding:8px;border-radius:8px;max-width:280px;" +
      "box-shadow:inset 0 0 0 1px rgba(255,255,255,.16)}" +
      // THE TWO WORKING CONTROLS, IN THE PANEL'S OWN CORNER RATHER THAN IN ITS BUTTON ROW. The row
      // below already carries four buttons inside 280px; two more would ellipsise «выгрузить» to
      // nothing. These are chips over the panel's own top-right corner, and they are the two things
      // this наряд owes a person and a capture harness alike (S-115):
      //   ⤢ — the FULL VIEW. Compact is the default and it is right for the gap the panel lives in;
      //       truncated is not. Full lets the panel take the whole screen and opens every step's
      //       detail at once, which is how the whole chain is read on a 390px phone.
      //   ✕ — OUT OF THE FRAME'S WAY. The audit measured this panel putting 6 271 pixels, worst 195
      //       of 255, between two offers of one score at one pinned instant: any pixel reading taken
      //       while it is up is polluted by it. Hidden it takes no layout and paints nothing, and the
      //       hiding is STICKY — the next landing must not bring it back over the very capture it was
      //       hidden for. It comes back on the `d` key (`в` on his own layout) or through
      //       `window.__@@NS@@Pass.verdict.away(false)`, which is the road a harness drives.
      "#ex-verdict .exv-tools{position:absolute;top:4px;right:4px;display:flex;gap:4px;z-index:1}" +
      "#ex-verdict .exv-tool{padding:2px 6px;cursor:pointer;font:12px/1 system-ui,sans-serif}" +
      "#ex-verdict[data-full=\"1\"]{left:12px;max-width:none;" +
      "top:calc(env(safe-area-inset-top,0px) + 8px);" +
      "max-height:calc(100dvh - env(safe-area-inset-top,0px)" +
      // Full screen means the picture is BEHIND the panel rather than beside it, and the compact
      // dock's .92 ground let the work read straight through the JSON. Nearly opaque here, and only
      // here — the compact panel keeps the lighter ground it was measured on.
      " - env(safe-area-inset-bottom,0px) - 16px);background:rgba(12,12,12,.98)}" +
      "#ex-verdict[data-full=\"1\"] .exv-step-detail{display:block}" +
      "#ex-verdict[data-full=\"1\"] .exv-step-sum{white-space:normal;overflow:visible}" +
      "#ex-verdict .exv-info{opacity:.8;margin-bottom:6px;word-break:break-word;flex:none;" +
      "padding-right:58px;min-height:16px}" +
      "#ex-verdict .exv-note{width:100%;box-sizing:border-box;margin-bottom:6px;padding:4px;" +
      "flex:none}" +
      "#ex-verdict .exv-row{display:flex;gap:6px;flex:none}" +
      "#ex-verdict .exv-btns{display:flex;gap:6px;flex:2}" +
      "#ex-verdict .exv-btn{flex:1;padding:6px 4px;cursor:pointer}" +
      "#ex-verdict .exv-dump{flex:1;padding:6px 4px;cursor:pointer}" +
      // `#ex-verdict{display:flex}` above is an ID-selector rule, and an ID selector's author
      // style always wins over the UA stylesheet's own `[hidden]{display:none}` — an attribute
      // selector with no `!important` — so stating `display` here at all UNHIDES the panel
      // before the first crossing ever lands, `hidden` attribute or not (found the hard way, this
      // наряд: PASS-01's own pixel row read a permanently-visible empty panel as a huge, constant
      // seam against a walk with diagnostics off at all). `[hidden]` is restated explicitly, on a
      // selector one step more specific than the bare ID it has to outrank.
      "#ex-verdict[hidden]{display:none}" +
      "#ex-verdict[data-pending=\"0\"] .exv-info,#ex-verdict[data-pending=\"0\"] .exv-note," +
      "#ex-verdict[data-pending=\"0\"] .exv-btns{display:none}" +
      // With nothing pending the info line is gone and the button row rises to the top, straight
      // under the two corner chips — so it keeps their width clear of itself.
      "#ex-verdict[data-pending=\"0\"] .exv-row{padding-right:58px}" +
      "#ex-verdict .exv-list{flex:1 1 auto;min-height:0;overflow-y:auto;" +
      "overscroll-behavior:contain;-webkit-overflow-scrolling:touch;margin-top:6px}" +
      "#ex-verdict .exv-list:empty{display:none}" +
      "#ex-verdict .exv-step{padding:4px 2px;border-top:1px solid rgba(255,255,255,.14);" +
      "cursor:pointer}" +
      "#ex-verdict .exv-step:first-child{border-top:none}" +
      "#ex-verdict .exv-step-sum{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}" +
      "#ex-verdict .exv-step-detail{display:none;white-space:pre-wrap;word-break:break-word;" +
      "opacity:.82;margin-top:3px;font-size:11px}" +
      "#ex-verdict .exv-step[data-open=\"1\"] .exv-step-detail{display:block}";
    document.head.appendChild(style);

    const panel = document.createElement("div");
    panel.id = "ex-verdict";
    panel.hidden = true;                     // nothing to show before the first real crossing lands
    panel.dataset.pending = "0";

    const info = document.createElement("div");
    info.className = "exv-info";

    const note = document.createElement("input");
    note.type = "text";
    note.className = "exv-note";
    note.placeholder = "заметка";
    note.setAttribute("aria-label", "заметка о переходе");

    const btnRow = document.createElement("div");
    btnRow.className = "exv-btns";
    VERDICT_DEFS.forEach((def) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "exv-btn";
      b.textContent = def.label;
      b.dataset.verdict = def.key;
      b.addEventListener("click", () => verdictRecord(def.label));
      btnRow.appendChild(b);
    });

    const dumpBtn = document.createElement("button");
    dumpBtn.type = "button";
    dumpBtn.className = "exv-dump";
    dumpBtn.textContent = "копия отладки";
    dumpBtn.addEventListener("click", verdictDump);

    const row = document.createElement("div");
    row.className = "exv-row";
    row.appendChild(btnRow);
    row.appendChild(dumpBtn);

    const list = document.createElement("div");
    list.className = "exv-list";

    // A HIDDEN PANEL STAYS HIDDEN THROUGH THE NEXT LANDING. Without this flag `verdictShowPending`
    // would unhide it at the very next dock, which is the one instant a capture is being taken.
    let verdictAway = false;
    function verdictSetAway(on) {
      verdictAway = !!on;
      panel.hidden = verdictAway || !verdictHistory.length;
      if (!panel.hidden) verdictFit();
      return verdictAway;
    }
    function verdictSetFull(on) {
      panel.dataset.full = on ? "1" : "0";
      verdictFit();
      return panel.dataset.full === "1";
    }
    const tools = document.createElement("div");
    tools.className = "exv-tools";
    const fullBtn = document.createElement("button");
    fullBtn.type = "button";
    fullBtn.className = "exv-tool";
    fullBtn.textContent = "⤢";
    fullBtn.title = "во весь экран — вся цепочка каждого шага, без обрезания";
    fullBtn.setAttribute("aria-label", fullBtn.title);
    fullBtn.addEventListener("click", () => verdictSetFull(panel.dataset.full !== "1"));
    const hideBtn = document.createElement("button");
    hideBtn.type = "button";
    hideBtn.className = "exv-tool";
    hideBtn.textContent = "✕";
    hideBtn.title = "убрать панель с кадра — вернуть клавишей d";
    hideBtn.setAttribute("aria-label", hideBtn.title);
    hideBtn.addEventListener("click", () => verdictSetAway(true));
    tools.appendChild(fullBtn);
    tools.appendChild(hideBtn);

    panel.appendChild(tools);
    panel.appendChild(info);
    panel.appendChild(note);
    panel.appendChild(row);
    panel.appendChild(list);
    document.body.appendChild(panel);

    // THE PANEL STOPS WHERE THE PICTURE STARTS. Its own docking comment above states the rule —
    // it lives in the gap between the top chrome and the hung work's frame and never reaches into
    // the picture — and this is the reading that keeps it. The floor is the top edge of the
    // nearest hung picture standing BELOW the panel's own top; where the walk is scrolled so that
    // no picture's top edge falls below it (the work fills the frame, or the walk has run past its
    // last one), there is no picture edge to stop at and the stylesheet's own viewport ceiling
    // stands. Nothing is typed here: both numbers are read off the two boxes themselves.
    function verdictFit() {
      // THE FULL VIEW IS THE ONE PLACE THE PICTURE IS NOT THE CEILING. It is asked for by hand, by a
      // person reading the whole chain, and the stylesheet's own full-view height stands instead.
      if (panel.dataset.full === "1") { panel.style.maxHeight = ""; return; }
      let floor = null;
      try {
        const top = panel.getBoundingClientRect().top;
        const imgs = (stage || document).querySelectorAll(".exh-frame img.work");
        for (let i = 0; i < imgs.length; i++) {
          const t = imgs[i].getBoundingClientRect().top;
          if (t > top && (floor === null || t < floor)) floor = t;
        }
        if (floor !== null) panel.style.maxHeight = (floor - top) + "px";
        else panel.style.maxHeight = "";
      } catch (e) { panel.style.maxHeight = ""; }
    }

    // THE PICTURE MOVES UNDER A FIXED PANEL, so the reading is re-taken whenever it can have moved
    // — the walk scrolls between landings, and a turn or a resize re-lays every frame. Coalesced
    // onto one frame so a scroll writes the height once per paint rather than once per event.
    let verdictFitQueued = false;
    function verdictRefit() {
      if (verdictFitQueued) return;
      verdictFitQueued = true;
      requestAnimationFrame(() => { verdictFitQueued = false; verdictFit(); });
    }
    addEventListener("scroll", verdictRefit, { passive: true });
    addEventListener("resize", verdictRefit);

    function verdictShowPending() {
      if (!verdictAway) panel.hidden = false;
      panel.dataset.pending = verdictPending ? "1" : "0";
      info.textContent = verdictPending
        ? verdictPending.from + " → " + verdictPending.to
          + (verdictPending.road ? " · " + verdictPending.road : "")
        : "";
      verdictFit();
    }

    function verdictRecord(label) {
      if (!verdictPending) return;
      verdictN += 1;
      verdictRows.push({ n: verdictN, from: verdictPending.from, to: verdictPending.to,
                         road: verdictPending.road, cues: verdictPending.cues.slice(),
                         durationMs: verdictPending.durationMs, verdict: label,
                         note: note.value || "" });
      note.value = "";
      verdictPending = null;
      verdictShowPending();               // the panel stays mounted; only the pending row clears
    }

    // Two carriers, on one click, exactly as the наряд asks — the buffer AND a file, never one
    // instead of the other. Neither failing (a denied clipboard permission, a download the browser
    // blocks) touches the other.
    function verdictDump() {
      // ONE COPY CARRIES THE WHOLE DEBUG READING OF THIS VISIT (2026-09-11, his word: a neat button
      // that copies everything, and says which page and which part of the walk it came from). The
      // passages are the very rows the walk derived — request (the die, the role, the walk's own
      // memory) and the score the layer played — so the Lab (tlvphotos.com/lab/) replays any one of
      // them as the site played it; the score's byte image and the plan's own copy of the cues are
      // left out, and a request's two work records travel as their ids.
      const passages = (typeof passPassages !== "undefined" ? passPassages : []).map((r) => {
        const o = {};
        Object.keys(r || {}).forEach((k) => { if (k !== "json" && k !== "bytes" && k !== "plan") o[k] = r[k]; });
        if (o.request) {
          const q = {};
          Object.keys(o.request).forEach((k) => {
            q[k] = (k === "workRecordA" || k === "workRecordB") ? { id: o.request[k] && o.request[k].id } : o.request[k];
          });
          o.request = q;
        }
        return o;
      });
      let host = null, layer = null;
      try { host = passReport(); } catch (e) {}
      try { layer = passLayer && passLayer.report ? passLayer.report() : null; } catch (e) {}
      const hang = (typeof order !== "undefined" && Array.isArray(order)) ? order.map(String) : [];
      const standing = (typeof pick !== "undefined" && pick) ? String(pick) : null;
      const out = {
        page: { href: location.href, path: location.pathname, title: document.title,
                openedAt: verdictStartedAt, copiedAt: new Date().toISOString(),
                viewport: { w: innerWidth, h: innerHeight }, dpr: devicePixelRatio || 1,
                userAgent: navigator.userAgent },
        walk: { entered: standing, hang: hang, hangLength: hang.length,
                stepsPlayed: verdictHistory.length,
                lastStep: verdictHistory.length ? { from: verdictHistory[verdictHistory.length - 1].from,
                                                    to: verdictHistory[verdictHistory.length - 1].to } : null },
        rows: verdictRows.slice(),
        steps: verdictHistory.slice(),
        passages: passages,
        host: host, layer: layer,
      };
      const text = JSON.stringify(out, null, 2);
      dumpBtn.textContent = "скопировано · " + passages.length;
      setTimeout(() => { dumpBtn.textContent = "копия отладки"; }, 2500);
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text);
        }
      } catch (e) {}
      try {
        const blob = new Blob([text], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        const d = new Date();
        const pad = (n) => String(n).padStart(2, "0");
        a.href = url;
        a.download = "verdicts-" + d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-"
          + pad(d.getDate()) + ".json";
        document.body.appendChild(a);
        a.click();
        a.remove();
        setTimeout(() => { try { URL.revokeObjectURL(url); } catch (e2) {} }, 1000);
      } catch (e) {}
    }

    // THE ROAD AND THE CUES COME OFF THE JOINED RECORD, and off nothing else (S-115). This file used
    // to keep its own second lookup into `passPassages` by score identity — which is exactly the
    // lookup that comes back empty on a step the host rescued, because the score that docks then is
    // one no passage row was ever written under. `passStepJoinedRecord` now answers that case (by
    // generation, and off the score that actually played), so reading it here removes the second copy
    // rather than repairing it twice. Where a rescue means there IS no composer road, the panel says
    // where the score came from instead of showing a blank.
    function verdictRoadOf(joined) {
      if (!joined) return null;
      return joined.road || (joined.played ? joined.played.source : null) || null;
    }
    function verdictCuesOf(joined) {
      return (joined && Array.isArray(joined.voices) ? joined.voices : [])
        .map((v) => String((v && v.id) || "?") + ":" + String((v && v.instrument) || "?"));
    }

    // Any dock that is not itself a judgeable crossing (a jump, or a landing on the door) still
    // ENDS whatever crossing was pending before it — the panel is about the pair on screen NOW,
    // and once a jump or the door has moved the visitor past it, the old pair is not on screen any
    // more for a judge to press a button on. Clearing it here, in the one place every dock passes
    // through, is what keeps a stray click from ever writing a verdict against a crossing nobody is
    // looking at (P6). The same clear covers the ordinary case of two judgeable crossings landing
    // back to back with no button pressed between them: the second dock discards the first pending
    // row's note along with its `from`/`to`, rather than letting an unsent note ride into the row
    // the SECOND crossing eventually gets (P5) — a judge who typed a note and then let the pair
    // scroll past never gets that note reattributed; it is dropped exactly as the missed verdict is.
    function verdictClearPending() {
      verdictPending = null;
      note.value = "";
      // Only an ALREADY-SHOWN panel is touched here — a dock arriving before the first judgeable
      // crossing (a jump or the door landing right after the visitor walks in) must not be the
      // reason the panel first appears; it stays exactly as hidden as it was.
      if (!panel.hidden) {
        panel.dataset.pending = "0";
        info.textContent = "";
      }
    }

    // A1/A2: one collapsed row for a played step, appended to the list in landing order and never
    // rebuilt afterwards — an already-open row stays open under a later step landing beside it.
    // `passStepJoinedRecord` (01a-pass.js) is the single joined shape both this row and the export
    // read; nothing here re-derives any of its fields.
    function verdictAppendStep(cmd) {
      let joined = null;
      try { joined = passStepJoinedRecord(cmd); } catch (e) {}
      if (!joined) return null;
      verdictHistory.push(joined);
      const el = document.createElement("div");
      el.className = "exv-step";
      el.dataset.open = "0";
      const sum = document.createElement("div");
      sum.className = "exv-step-sum";
      const summaryRoad = verdictRoadOf(joined);
      sum.textContent = joined.from + " → " + joined.to
        + (summaryRoad ? " · " + summaryRoad : "") + " · " + joined.durationMs + "мс";
      el.appendChild(sum);
      // WHAT MOVED, AND WHAT READ IT (S-115, work order item 5) — one line per handle the fill
      // actually asked a value of, off `joined.drove` (pass-composer.js's own ledger, carried
      // through by `passStepJoinedRecord` unchanged): the cue and handle, what was requested and
      // what the handle's own published range let through, and the register's own sentence naming
      // the measurement that handle reads. Rendered only where the ledger is non-empty, and in the
      // same `.exv-step-detail` class the raw dump below already uses, so it opens and closes on the
      // same row click and the same full-view chip — no new toggle.
      const drovenLines = [];
      (joined.drove || []).forEach((c) => {
        (c.handles || []).forEach((h) => {
          const req = Array.isArray(h.requested) ? "[" + h.requested.join(", ") + "]"
                     : String(h.requested);
          const app = Array.isArray(h.applied) ? "[" + h.applied.join(", ") + "]"
                     : String(h.applied);
          drovenLines.push(c.cue + "." + h.handle + " · " + req + " → " + app + " · " + h.reads);
        });
      });
      if (drovenLines.length) {
        const moved = document.createElement("div");
        moved.className = "exv-step-detail";
        moved.textContent = "what moved, and what read it:\n" + drovenLines.join("\n");
        el.appendChild(moved);
      }
      // VOICES DROPPED (S-115, work order item 5) — one line per voice seated and then dropped, off
      // `joined.silenced`: which instrument, its own id, and why; the occlusion drop's own
      // `hiddenBy` named where present. Same non-empty guard and the same shared class as above.
      const silencedLines = (joined.silenced || []).map((s) =>
        s.instrument + " («" + s.id + "») — " + s.why
        + (s.hiddenBy ? " (hidden by " + s.hiddenBy + ")" : ""));
      if (silencedLines.length) {
        const dropped = document.createElement("div");
        dropped.className = "exv-step-detail";
        dropped.textContent = "voices dropped:\n" + silencedLines.join("\n");
        el.appendChild(dropped);
      }
      const detail = document.createElement("div");
      detail.className = "exv-step-detail";
      detail.textContent = JSON.stringify(joined, null, 1);
      el.appendChild(detail);
      el.addEventListener("click", () => {
        el.dataset.open = el.dataset.open === "1" ? "0" : "1";
        verdictFit();
      });
      list.appendChild(el);
      verdictFit();                        // the list just grew — re-read where the picture starts
      return joined;
    }

    function verdictOnDock(cmd) {
      verdictClearPending();
      if (!cmd || cmd.kind !== "step" || !cmd.from || !cmd.to) return;   // a jump judges nothing
      const from = cmd.from.id, to = cmd.to.id;
      if (!from || !to || from === "door" || to === "door") return;   // a door is not a work
      // The record is built FIRST and the pending row reads it, so the panel's own line and the
      // exported step can never say two different things about one landing.
      const joined = verdictAppendStep(cmd);
      verdictPending = { from: String(from), to: String(to), road: verdictRoadOf(joined),
                        cues: verdictCuesOf(joined),
                        durationMs: Math.round(passCrossingMsOf(cmd)) };
      verdictShowPending();
    }

    // THE PANEL'S OWN TWO CONTROLS, REACHABLE WITHOUT IT (S-115). `d` — `в` on his own layout — is
    // the way back for a person who put the panel out of a capture's way; the surface below is the
    // way a capture harness drives the same two states, and the way it reads the whole chain without
    // going through the clipboard at all.
    addEventListener("keydown", (e) => {
      if (e.key !== "d" && e.key !== "D" && e.key !== "в" && e.key !== "В") return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
      verdictSetAway(!verdictAway);
    });
    try {
      const diagSurface = window.__@@NS@@Pass;
      if (diagSurface) {
        diagSurface.verdict = {
          away: (on) => verdictSetAway(on === undefined ? !verdictAway : on),
          full: (on) => verdictSetFull(on === undefined ? panel.dataset.full !== "1" : on),
          dump: verdictDump,
          steps: () => verdictHistory.slice(),
          rows: () => verdictRows.slice(),
        };
      }
    } catch (e) {}

    // `passMark` is a plain top-level binding every fragment (this one included) reaches by name,
    // and `dock` calls it as that free variable on every real landing regardless of which reference
    // was used to call `dock` itself — see the note at the top of this file for why the wrap sits
    // here and not on `dock`.
    const verdictBaseMark = passMark;
    passMark = function (name, cmd, extra) {
      verdictBaseMark(name, cmd, extra);
      if (name === "dock") { try { verdictOnDock(cmd); } catch (e) {} }
    };
  }
