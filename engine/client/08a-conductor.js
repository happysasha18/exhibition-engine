  // ---- EX-CONDUCTOR (S-39): the gallery conductor -----------------------------------------------
  // SPEC.md Requirement 39, case "the conductor". Per viewport one work is the soloist at full
  // whisper, at most two neighbours ride the cheapest register, every other work the viewport holds
  // stands as a screenshot-perfect still, and every work outside the viewport pauses — three live
  // surfaces or fewer (criteria 15 and 16). While a crossing runs, the crossing is the soloist and
  // every work drops to its still (criterion 17). Succession keeps the incumbent for two of its own
  // breath periods and lands on an exhale, and a hand on a work takes the seat at once (c18).
  //
  // WHAT A SEAT IS FOR. The seat is what the whisper reads for its own gain: `pass-hand.js` asks
  // this file which register the voice it plays is seated at, and a register with no voice writes a
  // breath of zero. Requirement 39 criterion 20 names the conductor as the one new piece standing
  // over the contract that already exists, and this is that piece: it decides who plays, and the
  // voice, the future renderer and the row below all read one seating.
  //
  // NOTHING RUNS IN THE BACKGROUND. The seating is computed at the instant somebody reads it — the
  // whisper asking for its gain, or a row asking for the report — so between reads the conductor
  // costs a phone nothing, and it owns no loop, no timer and no scroll listener. Its one standing
  // cost is one IntersectionObserver at threshold 0, which is the platform's own answer to "is this
  // frame in the viewport" and takes no layout read per work. That is the whole of the battery
  // argument: the number of surfaces given a voice is bounded by construction, and the count below
  // is what a run reads rather than a clock anybody drives.
  //
  // WHERE EVERY NUMBER COMES FROM. One soloist, at most two neighbours, at most three live surfaces:
  // criterion 15's own counts, named once each below. Two breath periods of tenure: criterion 18's
  // own count, taken on the period the voice itself publishes (`pass-hand.js`, Requirement 37
  // criterion 1) rather than on any period written here. The exhale is read off the voice's own
  // curve — the half of the breath where its value is falling, which the sine's own slope names. The
  // cheapest register's own gain is not here at all: `pass-hand.js` owns every gain, because the
  // residual quarter-breath Requirement 38 criterion 1's hold verb names already lives there, and a
  // second copy of it in this file would be a second home for one number.
  const CONDUCTOR_NEIGHBOURS = 2;      // criterion 15 — "at most two neighbours"
  const CONDUCTOR_LIVE = 3;            // criterion 15 — "keeping to 3 live surfaces or fewer"
  const CONDUCTOR_TENURE = 2;          // criterion 18 — "at least two breath periods"

  // The frames this file conducts, in hang order, and which of them the viewport currently holds.
  // The list is built as the walk appends its frames (14-walk-render.js calls `condWatch`), so a
  // read never queries the document: the walk's closing screen is not a work and never enters here.
  const condFrames = [];
  const condInView = new Set();
  const condIO = ("IntersectionObserver" in window)
    ? new IntersectionObserver((es) => {
        es.forEach((x) => {
          if (x.isIntersecting) condInView.add(x.target);
          else condInView.delete(x.target);
        });
      }, { threshold: 0 })
    : null;
  function condWatch(frame) {
    if (!frame || !frame.classList || !frame.classList.contains("exh-frame")) return;
    if (condFrames.indexOf(frame) >= 0) return;
    condFrames.push(frame);
    if (condIO) condIO.observe(frame);
  }

  let condSolo = null;                 // the work id holding the soloist's seat, or null
  let condSoloAt = 0;                  // when it took the seat, on the clock the voice also runs on
  let condHandover = null;             // how the seat last changed hands — criterion 18's own trace

  function condIdOf(frame) {
    return (frame && frame.dataset && frame.dataset.id != null) ? String(frame.dataset.id) : null;
  }
  function condFrameOf(id) {
    if (id == null) return null;
    for (let i = 0; i < condFrames.length; i++) if (condIdOf(condFrames[i]) === id) return condFrames[i];
    return null;
  }
  // The voice's own reading, taken through the hand's narrow door rather than through its whole
  // report: `report()` computes the breath, and the breath asks this file for its gain, so reading
  // the report from here would close a ring. `voice()` carries the phase, the period and the work
  // the hand stands on, and none of the three depends on a gain.
  function condVoice() {
    if (!passHand || typeof passHand.voice !== "function") return null;
    try { return passHand.voice(); } catch (e) { return null; }
  }

  // WHO THE EYE IS ON. The walk already names its own answer and writes the wall label for it:
  // `restingEl`, the section under the eye (08-plaque-caption-io.js). The conductor seats that work
  // rather than measuring a second opinion beside it, so the work that is spoken for and the work
  // that breathes can never be two different works. A resting mark that is not a work in view — the
  // closing screen, or a mark left behind by a scroll the house wrote — falls back to the first
  // frame the viewport actually holds.
  function condCandidate() {
    if (restingEl && restingEl.classList && restingEl.classList.contains("exh-frame")
        && condInView.has(restingEl)) return condIdOf(restingEl);
    for (let i = 0; i < condFrames.length; i++) {
      if (condInView.has(condFrames[i])) return condIdOf(condFrames[i]);
    }
    return null;
  }

  // Criterion 18, whole. The incumbent keeps the seat for two of its own breath periods and hands
  // it over on an exhale; a hand on a work takes it instantly, and the work it takes it from is
  // still in view, so the ordinary rule below seats that one as a neighbour and it finishes its
  // cadence at the cheapest register rather than being cut dead. An incumbent the viewport no
  // longer holds has no cadence left to protect and yields at once — otherwise criterion 16's own
  // pause would be owed to a work still holding full whisper off-screen.
  function condExhale(voice) {
    // The breath is a sine of its own phase, so it is falling — the outbreath — exactly where the
    // sine's own slope is negative. Read off the voice's curve; no phase is typed here.
    return !voice || Math.cos(2 * Math.PI * voice.phase) < 0;
  }
  function condSeatSoloist() {
    const voice = condVoice();
    const held = (voice && voice.attached != null) ? String(voice.attached) : null;
    const candidate = condCandidate();
    const t = performance.now();
    let next = condSolo;
    let why = null;
    if (held !== null && held !== condSolo) {
      next = held; why = "hand";
    } else if (held === null && candidate !== null && condSolo === null) {
      next = candidate; why = "first";
    } else if (held === null && candidate !== null && candidate !== condSolo) {
      const seat = condFrameOf(condSolo);
      // With no voice joined there is no period to serve and no exhale to land on; the seat then
      // follows the eye directly, which is what the walk did before this file existed.
      const grown = !voice || (t - condSoloAt) >= CONDUCTOR_TENURE * voice.periodMs;
      if (!seat || !condInView.has(seat)) { next = candidate; why = "gone"; }
      else if (grown && condExhale(voice)) { next = candidate; why = "cadence"; }
    }
    if (next !== condSolo) {
      // The hand-over's own trace: what it cost the incumbent and where the breath stood when the
      // seat passed. Criterion 18's two clauses are read off these two numbers rather than guessed
      // at from outside, and `reason` says which of the criterion's roads the seat took.
      condHandover = { from: condSolo, to: next, reason: why, afterMs: t - condSoloAt,
                       periodMs: voice ? voice.periodMs : null, onExhale: condExhale(voice) };
      condSolo = next;
      condSoloAt = t;
    }
    return condSolo;
  }

  // The seating itself: one pass down the hang, each work reading its register off where it stands.
  // Criterion 15's "one soloist" needs no counter: the seat is one work id, so one row can match it.
  function condSeating() {
    const crossing = passRunning();
    const solo = condSeatSoloist();
    let neighbours = 0;
    const seats = condFrames.map((f) => {
      const id = condIdOf(f);
      const inView = condInView.has(f);
      let register;
      if (!inView) register = "paused";                                       // criterion 16
      else if (crossing) register = "still";                                  // criterion 17
      else if (id === solo) register = "solo";   // criterion 15 — one seat, and one id holds it
      else if (neighbours < CONDUCTOR_NEIGHBOURS) { register = "neighbour"; neighbours++; }
      else register = "still";                                                // criterion 15
      return { id: id, register: register, inView: inView };
    });
    return { crossing: crossing, solo: crossing ? null : solo, seats: seats };
  }

  // What `pass-hand.js` asks for. The voice belongs to the work the hand stands on, and with no
  // hand anywhere it is the soloist's — which is the one work Requirement 37's own title, standing
  // life at rest, is about. The hand turns this name into its own gain.
  // `seating` is handed in by the report, which has one already; every other caller — the voice
  // asking for its gain — takes a fresh one, which is the same one read a moment later.
  function conductorVoiceRegister(seating) {
    seating = seating || condSeating();
    if (seating.crossing) return "still";
    const voice = condVoice();
    const id = (voice && voice.attached != null) ? String(voice.attached) : seating.solo;
    if (id == null) return "still";
    for (let i = 0; i < seating.seats.length; i++) {
      if (seating.seats[i].id === id) return seating.seats[i].register;
    }
    return "still";
  }

  // The report, on the diagnostic surface beside the rest (01a-pass.js). A LIVE SURFACE IS ONE THAT
  // MOVES: a work the conductor has given a voice to, and the crossing's own canvas while it draws.
  // Criterion 15's ceiling is three of them, and `live` against `liveMax` is the row's own reading.
  function conductorReport() {
    const seating = condSeating();
    const voiced = seating.seats.filter(
      (s) => s.register === "solo" || s.register === "neighbour").length;
    const voice = condVoice();
    return {
      version: 1,
      crossing: seating.crossing,
      soloist: seating.crossing ? { kind: "crossing", id: null } : { kind: "work", id: seating.solo },
      live: voiced + (seating.crossing ? 1 : 0),
      liveMax: CONDUCTOR_LIVE,
      neighbourMax: CONDUCTOR_NEIGHBOURS,
      works: seating.seats.length,
      inView: seating.seats.filter((s) => s.inView).length,
      paused: seating.seats.filter((s) => s.register === "paused").length,
      seats: seating.seats,
      voice: voice ? { attached: voice.attached, phase: voice.phase, periodMs: voice.periodMs,
                       register: conductorVoiceRegister(seating) } : null,
      tenure: { periods: CONDUCTOR_TENURE, heldMs: performance.now() - condSoloAt,
                exhale: voice ? condExhale(voice) : null, handover: condHandover },
    };
  }
