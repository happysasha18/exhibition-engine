/*!pass-layer.js*/
// The drawing layer's own file — the picture half of the transition seam, delivered separately so
// the walk's bundle stays under its byte fence. The client fetches this once, and only when the
// visualLayer setting asks for it, the device reports WebGL2, and the visit runs neither reduced
// motion nor Save-Data.
//
// This is the STUB. It registers itself and declines every command, so the walk's own glide runs
// exactly as it does with no layer at all. It exists so the whole road — setting, probe, fetch,
// registration, decline, fallback — is real and testable before any pixel is drawn.
(function () {
  var join = window.__@@NS@@PassLayer;
  if (typeof join !== "function") return;
  join({
    name: "stub",
    // run(cmd, done) — answer true to take the command, and call done() on the arriving work when
    // the event has finished drawing. Any other answer hands the move straight back to the glide.
    run: function (cmd, done) { return false; },
  });
})();
