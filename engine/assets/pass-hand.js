/*!pass-hand.js*/
// The hand overlay's own file — EX-HAND (Requirement 38 criterion 9), the touch affordance over the
// walk's own standing work. Fetched separately, the same shape as pass-layer.js (PASS-API's classic-
// script join): the client asks for this file once the walk lands, installs its receiver global
// first, and this script hands the join one plain object of named functions once it runs.
//
// THE REACH IS DECIDED BY THE CLIENT, NOT HERE (engine/client/01a-pass.js): its window-capture
// pointerdown listener tests `e.target.closest(".exh-frame img.work")` and calls `attach` for
// nothing else, so the threshold window, the quiz chip, the share control, the sound tray and the
// series room never reach this file at all — and it detaches on its own while the closer look
// (EX-ZOOM) covers the same picture, re-attaching the moment that layer clears. This file holds only
// the attachment itself: which work, if any, the hand currently stands on. It keeps no input
// listener of its own, and it draws nothing — a later unit's own concern.
(function () {
  var join = window.__@@NS@@PassHand;
  if (typeof join !== "function") return;

  var attached = null;   // the standing work's own id, or null

  function attach(el, workRecord) {
    attached = (workRecord && workRecord.id != null) ? workRecord.id : null;
  }
  function detach() {
    attached = null;
  }
  function report() {
    return { attached: attached };
  }

  join({ attach: attach, detach: detach, report: report });
})();
