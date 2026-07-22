  // ---- EX-SOUND (INV-48): the ambient loop walks beside the guest ----------------------------
  // OFF by default — a fresh visit is silent and the audio loads ONLY on the first turn-on
  // (the perf fence), never on cold load. STREAMS from a <audio> element (preload none, native
  // loop): it plays as the first fragments arrive, so the press is answered at once rather than
  // after the whole file downloads and decodes. The native loop carries a faint seam at the wrap —
  // the accepted cost of the instant start. The fade rides a MediaElementSource → gain node so the
  // ramp works on every device (iOS included, where the element's own volume cannot be scripted):
  // in ~0.7s ×tempo, out ~0.8s and on leaving / unload (pagehide, best-effort). Volume default 0.3
  // with a ≥44px touch-friendly slider. The on/off + volume persist in ex.sound (versioned); a
  // return ON ARMS on the first gesture (autoplay is blocked without one) rather than loading on
  // cold arrival. A missing/failed file fails SILENT (INV-1). Two beats ride the EXISTING EX-PULSE
  // wire: sound_on / sound_off (no new analytics plumbing).
  // EX-SOUND-PAUSE (INV-52): off is a PAUSE that holds the moment on the element's own currentTime,
  // on RESUMES from it — a fresh page load builds a new element and starts from the top.
  // Config keys (config.json → exhibition): sound_url (audio file, empty = player hidden),
  // sound_credit.artist / sound_credit.title / sound_credit.url (the credit tray text + link).
  (function sound() {
    const SND_URL = (EX.sound_url || "").trim();
    if (!SND_URL) return;                                // no audio configured — player stays hidden
    const CREDIT = EX.sound_credit || {};
    const FADE_IN = 0.7, FADE_OUT = 0.8, DEFAULT_VOL = 0.3;

    const box = document.createElement("div");
    box.id = "ex-sound";
    // aria-labels localize through EX-I18N like every other chrome string; the fallback is ENGLISH
    // (source tongue), never a hardcoded locale literal
    const SNDT = (greetLang() || { t: {} }).t;
    // the tray sits to the LEFT of the button (slides out on hover / while playing / focus-within);
    // the credit uses config-driven artist/title/url — never hardcoded content (INV-1)
    const artistHtml = CREDIT.artist ? `<span class="t"><b>${CREDIT.artist}</b></span>` : "";
    const titleHtml = CREDIT.title ? `<span class="t">«${CREDIT.title}»</span>` : "";
    const linkHtml = CREDIT.url
      ? `<a href="${CREDIT.url}" target="_blank" rel="noopener">${CREDIT.url.replace(/^https?:\/\//, "")}</a>`
      : "";
    box.innerHTML =
      '<div class="exsnd-tray">' +
        '<span class="exsnd-cred">' + artistHtml + titleHtml + linkHtml + '</span>' +
        '<input class="exsnd-vol" type="range" min="0" max="1" step="0.01" value="0.3"' +
          ' aria-label="' + (SNDT.a11y_volume || A11Y_VOLUME_EN) + '">' +
      '</div>' +
      '<button class="exsnd-btn" type="button" aria-pressed="false"' +
        ' aria-label="' + (SNDT.a11y_sound || A11Y_SOUND_EN) +
        '"><span class="exsnd-note"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
          '<path d="M6.3 4.1 L12.9 3" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"/>' +
          '<path d="M6.3 4.1 V12 M12.9 3 V11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>' +
          '<circle cx="4.2" cy="12" r="2.35" fill="currentColor"/><circle cx="10.8" cy="11" r="2.35" fill="currentColor"/>' +
        '</svg></span><span class="exsnd-eq"><i></i><i></i><i></i></span></button>';
    document.body.appendChild(box);
    requestAnimationFrame(() => box.classList.add("show"));   // EX-ARRIVE: arrives on the breath

    const btn = box.querySelector(".exsnd-btn");
    const vol = box.querySelector(".exsnd-vol");

    // The player STREAMS: a single <audio> element (preload none, native loop) plays as soon as the
    // first fragments arrive and fetches the rest on the fly, so the press is answered at once — no
    // download-then-decode wait. The element routes through a MediaElementAudioSourceNode → gain so
    // the fade ramps on every device, iOS included, where the element's own volume cannot be scripted.
    let ctx = null, srcNode = null, gain = null;
    let aud = null, wired = false, pauseTimer = 0;
    let target = DEFAULT_VOL, desired = false, playing = false, armed = false;
    let ready = false, loading = false;
    // EX-SOUND-PAUSE (INV-52): off is a PAUSE, on RESUMES — never a within-session restart. The
    // element OWNS the playhead (aud.currentTime), so a pause holds the moment natively and a resume
    // continues from it; no manual offset bookkeeping. A fresh page load builds a new element at 0.

    // the remembered choice (versioned like the walk)
    let pref = null;
    try { pref = JSON.parse(localStorage.getItem(SND_KEY) || "null"); } catch (e) {}
    if (!pref || pref.v !== VER) pref = null;
    if (pref && Number.isFinite(+pref.vol)) target = Math.min(1, Math.max(0, +pref.vol));
    vol.value = String(target);

    function persist() {
      try {
        localStorage.setItem(SND_KEY, JSON.stringify({ v: VER, on: desired, vol: target, greeted: greeted }));
      } catch (e) {}
    }

    // EX-SOUND-GREET (INV-101): on the FIRST visit only, a localized word greets beside the note,
    // holds, then settles away — leaving the bare note. It fires the first frame the player is truly
    // VISIBLE (the control retracts under the door, so a greeting on cold load would breathe out of
    // sight; this waits for the walk), robust to every entry — the door, a shared work, a resumed walk.
    // The once-ness is consumed only when the word actually shows and persists in ex.sound (`greeted`),
    // so a return meets only the quiet note. Reduced motion / Save-Data stand the choreography down (the
    // note rests, unmarked, so a later ordinary visit may still greet once). The word is a greeting,
    // never a control — aria-hidden, pointer-off; the button keeps its label and stays pressable.
    let greeted = !!(pref && pref.greeted);
    function greetOnce() {
      if (greeted || REDUCED || dataSaver()) return;
      greeted = true;
      persist();                                          // consume the first arrival on show
      const g = document.createElement("span");
      g.className = "exsnd-greet";
      g.setAttribute("aria-hidden", "true");              // a greeting, never a control
      g.textContent = SNDT.sound_greet || SOUND_GREET_EN;
      box.appendChild(g);
      requestAnimationFrame(() => g.classList.add("greet"));
      g.addEventListener("animationend", () => { try { g.remove(); } catch (e) {} });
    }
    if (!greeted && !REDUCED && !dataSaver()) {
      let tries = 0;
      (function waitVisible() {
        if (greeted) return;
        const shown = parseFloat(getComputedStyle(box).opacity || "0") > 0.5
                      && !document.body.classList.contains("ex-door");
        if (shown) { greetOnce(); return; }
        if (++tries > 600) return;                        // ~10s cap — the visitor never left the door
        requestAnimationFrame(waitVisible);
      })();
    }

    function prepare() {
      if (ready || loading) return ready;
      loading = true;
      try {
        aud = document.createElement("audio");
        aud.src = SND_URL;
        aud.loop = true;                                 // native loop — a faint seam at the wrap
        aud.preload = "none";                            // stream on play, never a cold-load fetch
        // NO crossOrigin: the audio is same-origin, and a MediaElementSource over a CORS request the
        // static host does not answer (Cloudflare Pages sends no ACAO on static assets) would taint
        // the node and output SILENCE — same-origin needs no CORS and must not opt into it
        // a failed file fails SILENT (INV-1): stop the graph so no equalizer shows, and leave the
        // button's own aria-pressed as the visitor's CHOICE (the equalizer bars, not the button,
        // signal actual playback) — desired and aria-pressed stay coherent, no false sound_off beat
        aud.addEventListener("error", () => { stop(); });
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        gain = ctx.createGain(); gain.gain.value = 0; gain.connect(ctx.destination);
        // one MediaElementSource per element, created once; the element's output now routes ONLY
        // through the graph, so the gain MUST reach the destination (wired just above)
        srcNode = ctx.createMediaElementSource(aud);
        srcNode.connect(gain);
        wired = true;
        ready = true;
      } catch (e) { ready = false; }
      loading = false;
      return ready;
    }

    function arm() {
      if (armed || playing) return;
      armed = true;
      ["pointerdown", "touchstart", "scroll", "keydown"].forEach((e) =>
        addEventListener(e, onGesture, { once: true, passive: true, capture: true }));
    }
    function disarm() {
      if (!armed) return;
      armed = false;
      ["pointerdown", "touchstart", "scroll", "keydown"].forEach((e) =>
        removeEventListener(e, onGesture, { capture: true }));
    }
    function onGesture() { disarm(); if (desired) start(); }

    function setDesired(on) {
      if (on === desired) return;
      desired = on;
      btn.setAttribute("aria-pressed", on ? "true" : "false");
      pulse(on ? "sound_on" : "sound_off");
      persist();
      if (on) start(); else stop();
    }

    async function start() {
      if (playing) return;
      const ok = prepare();
      if (!desired) return;
      if (!ok) { box.classList.remove("playing"); return; }
      if (pauseTimer) { clearTimeout(pauseTimer); pauseTimer = 0; }   // cancel a pending pause
      // EX-SOUND-LOADING (INV-48): the press is taken the instant it lands — the note breathes
      // softly (CSS .loading) while the stream buffers, so a slow first fetch reads as "loading",
      // never as "nothing happened". It clears the moment sound begins, the file fails, or a still-
      // blocked press falls back to arming.
      box.classList.add("loading");
      // ONE press is ONE user-activation, and BOTH the context resume and the element play need it.
      // The old order awaited ctx.resume() FIRST, which spent the activation, so aud.play() was then
      // refused and the code armed and waited — the first press only armed, a SECOND actually played
      // (his find 2026-07-22). Kick both synchronously — create both promises before any await — so a
      // single press starts the sound. The element resumes from its own playhead (EX-SOUND-PAUSE/INV-52).
      const resuming = (ctx.state === "suspended") ? ctx.resume() : null;
      let played = false;
      try { await aud.play(); played = true; }
      catch (e) {
        // WebKit still refused the FIRST play() because the context was suspended AT THE CALL —
        // the resume kicked in the same gesture had not settled yet, so the two promises raced and
        // the element lost (his 2026-07-22 same-browser "only the second tap" find survived the
        // first fix). Wait for the resume to settle, then RETRY play() ONCE: the retry rides the
        // same activation chain (a transient activation outlives the short resume await), so the
        // FIRST press now sounds. A genuine block (no activation at all) still fails and arms below.
        if (resuming) { try { await resuming; } catch (e2) {} }
        try { await aud.play(); played = true; } catch (e2) { played = false; }
      }
      if (resuming) { try { await resuming; } catch (e) {} }
      if (!desired) { box.classList.remove("loading"); try { aud.pause(); } catch (e) {} return; }
      if (!played || ctx.state === "suspended") { box.classList.remove("loading"); arm(); return; }   // still blocked → wait for the next gesture
      box.classList.remove("loading");
      const now = ctx.currentTime;
      gain.gain.cancelScheduledValues(now);
      gain.gain.setValueAtTime(Math.max(0.0001, gain.gain.value), now);
      gain.gain.linearRampToValueAtTime(target, now + FADE_IN * TEMPO);
      playing = true; armed = false;
      box.classList.add("playing");
    }

    function stop() {
      disarm();
      if (wired && ctx && gain) {
        const now = ctx.currentTime;
        gain.gain.cancelScheduledValues(now);
        gain.gain.setValueAtTime(gain.gain.value, now);
        gain.gain.linearRampToValueAtTime(0, now + FADE_OUT * TEMPO);
        // pause AFTER the fade so the ramp is heard; the element holds currentTime for a resume.
        // re-read `desired` at fire time — a fast off→on toggle must not pause the re-enabled player.
        if (pauseTimer) clearTimeout(pauseTimer);
        pauseTimer = setTimeout(() => {
          pauseTimer = 0;
          if (!desired && aud) { try { aud.pause(); } catch (e) {} }
        }, Math.round(FADE_OUT * TEMPO * 1000) + 80);
      }
      playing = false;
      box.classList.remove("playing");
      box.classList.remove("loading");   // a file error / off during buffer clears the loading note
    }

    btn.addEventListener("click", () => { setDesired(!desired); });
    vol.addEventListener("input", () => {
      target = Math.min(1, Math.max(0, parseFloat(vol.value) || 0));
      if (playing && ctx) {
        const now = ctx.currentTime;
        gain.gain.cancelScheduledValues(now);
        gain.gain.setValueAtTime(gain.gain.value, now);
        gain.gain.linearRampToValueAtTime(target, now + 0.15);
      }
      persist();
    });
    addEventListener("pagehide", () => {
      if (playing) stop();
      if (aud) { try { aud.pause(); } catch (e) {} }   // best-effort immediate silence on leave
    });

    // a return visit with the pref ON: ARM on the first gesture — never a cold-load fetch
    if (pref && pref.on) { desired = true; btn.setAttribute("aria-pressed", "true"); arm(); }

    // the player's own reachable surface, for the suite
    try {
      window.@@NS_UPPER@@Sound = { state: () => ({ desired, playing, armed, ready, loading,
                                         currentTime: aud ? aud.currentTime : 0 }),
                         url: SND_URL };
    } catch (e) {}
  })();
