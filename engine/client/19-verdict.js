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
    let verdictN = 0;
    let verdictPending = null; // {from, to, road, cues, durationMs} — the crossing awaiting a verdict

    // ---- one small stylesheet, scoped to the panel's own id — no other file's CSS is touched ----
    const style = document.createElement("style");
    style.textContent =
      "#ex-verdict{position:fixed;right:12px;bottom:12px;z-index:2147483647;" +
      "background:rgba(20,20,20,.92);color:#fff;font:12px/1.4 system-ui,sans-serif;" +
      "padding:10px;border-radius:8px;max-width:280px;box-shadow:0 2px 12px rgba(0,0,0,.4)}" +
      "#ex-verdict .exv-info{opacity:.8;margin-bottom:6px;word-break:break-word}" +
      "#ex-verdict .exv-note{width:100%;box-sizing:border-box;margin-bottom:6px;padding:4px}" +
      "#ex-verdict .exv-btns{display:flex;gap:6px;margin-bottom:6px}" +
      "#ex-verdict .exv-btn{flex:1;padding:6px 4px;cursor:pointer}" +
      "#ex-verdict .exv-dump{width:100%;padding:6px 4px;cursor:pointer}" +
      "#ex-verdict[data-pending=\"0\"] .exv-info,#ex-verdict[data-pending=\"0\"] .exv-note," +
      "#ex-verdict[data-pending=\"0\"] .exv-btns{display:none}";
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

    panel.appendChild(info);
    panel.appendChild(note);
    panel.appendChild(btnRow);
    panel.appendChild(dumpBtn);
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
      const out = { walk: verdictWalk, startedAt: verdictStartedAt, rows: verdictRows.slice() };
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

    function verdictOnDock(cmd) {
      if (!cmd || cmd.kind !== "step" || !cmd.from || !cmd.to) return;
      const from = cmd.from.id, to = cmd.to.id;
      if (!from || !to || from === "door" || to === "door") return;   // a door is not a work
      const rc = verdictRoadAndCues(cmd);
      verdictPending = { from: String(from), to: String(to), road: rc.road, cues: rc.cues,
                        durationMs: Math.round(passCrossingMsOf(cmd)) };
      verdictShowPending();
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
