/* Mr. K's Classroom: optional add-ons for the Interactive Math tools (loaded after lab.js by the
   2026-11-07 tools). Adds Lab.reset(), Lab.numInput(), Lab.notice(), Lab.feedback(), Lab.svgPoint()
   and Lab.drag(): pointer + keyboard dragging for any SVG element. lab.js itself is unchanged. */
(function (G) {
'use strict';
var L = G.Lab;
if (!L) return;
var css = '' +
  '.lp-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}' +
  '.lp-num{display:grid;gap:4px}.lp-num label{font-weight:700}' +
  '.lp-num .lp-in{display:flex;align-items:center;gap:6px}' +
  '.lp-num input{width:6.5em;min-height:40px;border:2px solid var(--ink);border-radius:8px;padding:4px 8px;background:var(--card);font-weight:700;font-size:1.05rem;font-variant-numeric:tabular-nums}' +
  '.lp-num small{color:var(--ink-soft)}' +
  '.lp-feedback{border-radius:10px;padding:8px 12px;font-size:.95rem;background:var(--wash);min-height:1.2em}' +
  '.lp-feedback.good{background:var(--green-tint)}.lp-feedback.warn{background:var(--orange-tint)}.lp-feedback.bad{background:var(--red-tint)}' +
  '.lp-notice{border:2px solid var(--ink);border-radius:12px;background:var(--card);padding:0}' +
  '.lp-notice>summary{cursor:pointer;font-family:var(--display);font-weight:800;padding:10px 14px;list-style:none;min-height:44px;display:flex;align-items:center;gap:8px}' +
  '.lp-notice>summary::-webkit-details-marker{display:none}' +
  '.lp-notice>summary::before{content:"\\25B8";display:inline-block;transition:transform .15s}' +
  '.lp-notice[open]>summary::before{transform:rotate(90deg)}' +
  '.lp-notice .lp-body{padding:0 16px 12px;font-size:.95rem}.lp-notice .lp-body p{margin:.4em 0}' +
  '.lp-drag{cursor:grab;touch-action:none}.lp-drag:active{cursor:grabbing}' +
  '.lp-drag:focus{outline:none}.lp-drag:focus-visible{outline:none;stroke:var(--orange);stroke-width:5}' +
  '.btn,.chip,.nudge,.tab{min-height:40px}' +
  '.lp-mini{font-size:.85rem;color:var(--ink-soft);margin:0}' +
  '.lp-tag{display:inline-block;border:2px solid currentColor;border-radius:999px;padding:0 8px;font-size:.8rem;font-weight:800;margin-left:4px;vertical-align:middle}';
var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

/* Reset button. */
L.reset = function (parent, fn, label) { return L.button(parent, '↺ ' + (label || 'Reset'), fn, true); };

/* Labeled number box. o: {id,label,min,max,step,value,onChange,hint} */
L.numInput = function (parent, o) {
  var wrap = L.h('div', { class: 'lp-num' }, parent);
  var id = 'ni-' + o.id;
  L.h('label', { for: id }, wrap, o.label);
  var row = L.h('div', { class: 'lp-in' }, wrap);
  var inp = L.h('input', { id: id, type: 'number', inputmode: 'decimal', min: o.min, max: o.max, step: o.step || 'any', value: o.value }, row);
  if (o.hint) L.h('small', null, row, o.hint);
  function read() {
    var v = parseFloat(inp.value);
    if (!isFinite(v)) return null;
    if (o.min != null) v = Math.max(o.min, v);
    if (o.max != null) v = Math.min(o.max, v);
    return v;
  }
  inp.addEventListener('change', function () { var v = read(); if (v == null) { inp.value = o.value; return; } inp.value = v; o.value = v; o.onChange && o.onChange(v); });
  inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') inp.blur(); });
  return { el: wrap, input: inp, get: function () { return read(); }, set: function (v) { inp.value = v; o.value = v; } };
};

/* "What should I notice?" panel, closed by default so it doesn't spoil the discovery. */
L.notice = function (parent, html, title) {
  var d = L.h('details', { class: 'lp-notice' }, parent);
  L.h('summary', null, d, title || 'What should I notice? <span class="lp-mini">(open after you explore)</span>');
  L.h('div', { class: 'lp-body' }, d, html);
  return d;
};

/* Live feedback line. set(html, tone) with tone '', 'good', 'warn' or 'bad'. */
L.feedback = function (parent) {
  var el = L.h('div', { class: 'lp-feedback', role: 'status', 'aria-live': 'polite' }, parent);
  return { el: el, set: function (html, tone) { el.className = 'lp-feedback' + (tone ? ' ' + tone : ''); el.innerHTML = html; } };
};

/* SVG user-space point from a pointer event. */
L.svgPoint = function (svg, ev) {
  var pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
  return pt.matrixTransform(svg.getScreenCTM().inverse());
};

/* Make an SVG element draggable with pointer and keyboard.
   o: {svg, label, onMove(x,y) in SVG user units, onKey(dx,dy) (dx,dy = -1/0/1, big = Shift), onEnd} */
L.drag = function (el, o) {
  el.classList.add('lp-drag');
  el.setAttribute('tabindex', '0');
  el.setAttribute('role', 'slider');
  el.setAttribute('aria-label', o.label || 'Draggable');
  if (o.valueText) el.setAttribute('aria-valuetext', o.valueText);
  el.addEventListener('pointerdown', function (ev) {
    ev.preventDefault();
    try { el.focus({ preventScroll: true }); } catch (e) {}
    var move = function (e) { var q = L.svgPoint(o.svg, e); o.onMove && o.onMove(q.x, q.y); };
    var up = function () { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); window.removeEventListener('pointercancel', up); o.onEnd && o.onEnd(); };
    window.addEventListener('pointermove', move); window.addEventListener('pointerup', up); window.addEventListener('pointercancel', up);
    move(ev);
  });
  el.addEventListener('keydown', function (e) {
    var k = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, 1], ArrowDown: [0, -1] }[e.key];
    if (!k || !o.onKey) return;
    e.preventDefault(); o.onKey(k[0], k[1], e.shiftKey);
  });
  return el;
};

/* Keep focus on a redrawn SVG element: call before clearing, then restore(el) after drawing. */
L.focusKeeper = function (svg) {
  var label = null;
  return {
    save: function () { var a = document.activeElement; label = a && svg.contains(a) ? a.getAttribute('aria-label') : null; },
    restore: function (root) {
      if (!label) return;
      var els = (root || svg).querySelectorAll('[aria-label]');
      for (var i = 0; i < els.length; i++) if (els[i].getAttribute('aria-label') === label) { els[i].focus({ preventScroll: true }); break; }
      label = null;
    }
  };
};

/* Change a Lab.graph view and pick grid and label spacing so short graphs don't crowd their labels.
   opts must be the same object that was passed to Lab.graph(). maxY/maxX = most labels wanted on each axis. */
L.setNiceView = function (gr, opts, view, maxY, maxX) {
  function nice(span, n) { var raw = span / n, p = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; }
  var v = Object.assign({}, gr.view, view);
  if (maxY) { var ys = nice(v.ymax - v.ymin, 12), yl = nice(v.ymax - v.ymin, maxY); opts.ystep = ys; opts.ylabelStep = Math.max(ys, Math.ceil(yl / ys - 1e-9) * ys); }
  if (maxX) { var xs = nice(v.xmax - v.xmin, 14), xl = nice(v.xmax - v.xmin, maxX); opts.xstep = xs; opts.xlabelStep = Math.max(xs, Math.ceil(xl / xs - 1e-9) * xs); }
  gr.setView(view);
};
})(window);
