/* chart-lite.js: the small part of the Chart.js API this simulator uses (one filled line chart, axis titles,
   update()), drawn on the page's own canvas so the simulator no longer loads a library from an outside site
   that school filters may block (site audit 2 #10, 2026-11-20). */
(function (G) {
  'use strict';
  function fmt(v) {
    if (Math.abs(v) >= 1e6) return (v / 1e6).toFixed(1).replace(/\.0$/, '') + 'M';
    if (Math.abs(v) >= 1e3) return (v / 1e3).toFixed(1).replace(/\.0$/, '') + 'k';
    return String(Math.round(v * 100) / 100);
  }
  function niceMax(v) {
    if (!(v > 0)) return 1;
    var p = Math.pow(10, Math.floor(Math.log10(v))), m = v / p;
    return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 5 ? 5 : 10) * p;
  }
  function Chart(ctx, cfg) {
    this.ctx = ctx; this.canvas = ctx.canvas; this.data = cfg.data; this.options = cfg.options || {};
    var self = this;
    if (G.ResizeObserver) new G.ResizeObserver(function () { self.update(); }).observe(this.canvas.parentNode || this.canvas);
    else G.addEventListener('resize', function () { self.update(); });
    this.update();
  }
  Chart.defaults = { color: '#333', font: { family: 'sans-serif' }, borderColor: 'rgba(0,0,0,0.15)' };
  Chart.prototype.update = function () {
    var c = this.canvas, box = (c.parentNode && c.parentNode.getBoundingClientRect) ? c.parentNode.getBoundingClientRect() : { width: 600, height: 300 };
    var dpr = G.devicePixelRatio || 1, W = Math.max(200, box.width || c.clientWidth || 600), H = Math.max(160, box.height || c.clientHeight || 300);
    c.width = W * dpr; c.height = H * dpr; c.style.width = W + 'px'; c.style.height = H + 'px';
    var x = this.ctx, D = Chart.defaults, ds = this.data.datasets[0], labels = this.data.labels, ys = ds.data.map(Number);
    var sc = (this.options.scales || {}), font = D.font.family;
    x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, W, H);
    var L = 64, R = 30, T = 12, B = 48, pw = W - L - R, ph = H - T - B, max = niceMax(Math.max.apply(null, ys.concat([0])));
    var X = function (i) { return L + (labels.length < 2 ? pw / 2 : i * pw / (labels.length - 1)); }, Y = function (v) { return T + ph - (v / max) * ph; };
    x.font = '12px ' + font; x.fillStyle = D.color; x.strokeStyle = D.borderColor; x.lineWidth = 1;
    for (var k = 0; k <= 5; k++) {                     // horizontal grid and y labels
      var v = max * k / 5, yy = Y(v);
      x.beginPath(); x.moveTo(L, yy); x.lineTo(L + pw, yy); x.stroke();
      x.textAlign = 'right'; x.textBaseline = 'middle'; x.fillText(fmt(v), L - 6, yy);
    }
    var every = Math.ceil(labels.length / 10);
    x.textAlign = 'center'; x.textBaseline = 'top';
    labels.forEach(function (lab, i) { if (i % every === 0) x.fillText(String(lab), X(i), T + ph + 6); });
    if (sc.x && sc.x.title && sc.x.title.display) x.fillText(sc.x.title.text, L + pw / 2, H - 18);
    if (sc.y && sc.y.title && sc.y.title.display) { x.save(); x.translate(14, T + ph / 2); x.rotate(-Math.PI / 2); x.textBaseline = 'middle'; x.fillText(sc.y.title.text, 0, 0); x.restore(); }
    if (!ys.length) return;
    x.beginPath(); ys.forEach(function (v, i) { if (i) x.lineTo(X(i), Y(v)); else x.moveTo(X(i), Y(v)); });
    if (ds.fill) { x.save(); x.lineTo(X(ys.length - 1), Y(0)); x.lineTo(X(0), Y(0)); x.closePath(); x.fillStyle = ds.backgroundColor || 'rgba(0,0,0,0.1)'; x.fill(); x.restore();
      x.beginPath(); ys.forEach(function (v, i) { if (i) x.lineTo(X(i), Y(v)); else x.moveTo(X(i), Y(v)); }); }
    x.strokeStyle = ds.borderColor || '#000'; x.lineWidth = ds.borderWidth || 2; x.stroke();
    x.fillStyle = ds.pointBackgroundColor || x.strokeStyle;
    ys.forEach(function (v, i) { x.beginPath(); x.arc(X(i), Y(v), ds.pointRadius || 3, 0, 2 * Math.PI); x.fill(); });
  };
  G.Chart = Chart;
})(window);
