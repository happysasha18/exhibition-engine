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
      "max-height:calc(100dvh - env(safe-area-inset-top,0px) - env(safe-area-inset-bottom,0px)" +
      " - 58px - 12px);display:flex;flex-direction:column;" +
      "background:rgba(20,20,20,.92);color:#fff;font:12px/1.4 system-ui,sans-serif;" +
      "padding:8px;border-radius:8px;max-width:280px;box-shadow:0 1px 3px rgba(0,0,0,.4)}" +
      "#ex-verdict .exv-info{opacity:.8;margin-bottom:6px;word-break:break-word;flex:none}" +
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
    dumpBtn.textContent = "выгрузить";
    dumpBtn.addEventListener("click", verdictDump);

    const row = document.createElement("div");
    row.className = "exv-row";
    row.appendChild(btnRow);
    row.appendChild(dumpBtn);

    const list = document.createElement("div");
    list.className = "exv-list";

    panel.appendChild(info);
    panel.appendChild(note);
    panel.appendChild(row);
    panel.appendChild(list);
    document.body.appendChild(panel);

    function verdictShowPending() {
      panel.hidden = false;
      panel.dataset.pending = verdictPending ? "1" : "0";
      info.textContent = verdictPending
        ? verdictPending.from + " → " + verdictPending.to
          + (verdictPending.road ? " · " + verdictPending.road : "")
        : "";
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
      const out = { walk: verdictWalk, startedAt: verdictStartedAt, rows: verdictRows.slice(),
                   steps: verdictHistory.slice() };
      const text = JSON.stringify(out, null, 2);
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

    // Read the passage row a landed command played, the same way `passEdgeRemember` finds it —
    // by the identity of the score, never by re-deriving one. A declined or still-forming crossing
    // (no score at all) reads back a bare road/cues, which is the honest answer: nothing drew.
    function verdictRoadAndCues(cmd) {
      if (!cmd.score) return { road: null, cues: [] };
      for (let i = passPassages.length - 1; i >= 0; i--) {
        const r = passPassages[i];
        if (r.score === cmd.score || r.played === cmd.score) {
          const cues = (r.score && Array.isArray(r.score.cues)) ? r.score.cues : [];
          return {
            road: r.road || null,
            cues: cues.map((c) => String((c && c.id) || "?") + ":"
              + String((c && c.instrument && c.instrument.id) || "?")),
          };
        }
      }
      return { road: null, cues: [] };
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
      if (!joined) return;
      verdictHistory.push(joined);
      const el = document.createElement("div");
      el.className = "exv-step";
      el.dataset.open = "0";
      const sum = document.createElement("div");
      sum.className = "exv-step-sum";
      sum.textContent = joined.from + " → " + joined.to
        + (joined.road ? " · " + joined.road : "") + " · " + joined.durationMs + "мс";
      const detail = document.createElement("div");
      detail.className = "exv-step-detail";
      detail.textContent = JSON.stringify(joined, null, 1);
      el.appendChild(sum);
      el.appendChild(detail);
      el.addEventListener("click", () => {
        el.dataset.open = el.dataset.open === "1" ? "0" : "1";
      });
      list.appendChild(el);
    }

    function verdictOnDock(cmd) {
      verdictClearPending();
      if (!cmd || cmd.kind !== "step" || !cmd.from || !cmd.to) return;   // a jump judges nothing
      const from = cmd.from.id, to = cmd.to.id;
      if (!from || !to || from === "door" || to === "door") return;   // a door is not a work
      const rc = verdictRoadAndCues(cmd);
      verdictPending = { from: String(from), to: String(to), road: rc.road, cues: rc.cues,
                        durationMs: Math.round(passCrossingMsOf(cmd)) };
      verdictShowPending();
      verdictAppendStep(cmd);
    }

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
