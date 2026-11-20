/* Motion diagrams for Interactive Math (2026-11-20): a play/pause timeline shared by the animated labs, plus small
   3D helpers (rotation about a line, projection, painter's sort) for the folding nets.
   Motion respects prefers-reduced-motion: Play jumps to the end instead of animating, and the slider still scrubs. */
(function (G) {
'use strict';
var L = G.Lab;
var reduce = false;
try { reduce = G.matchMedia && G.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { reduce = false; }

/* A timeline from 0 to 1 with Play, Pause, Back to start, and a scrubber.
   o: { label, seconds, value, loop ('bounce' | false), onChange(t), steps (optional tick count for keyboard) } */
function timeline(parent, o) {
  var t = o.value || 0, playing = false, dir = 1, last = 0, raf = 0;
  var wrap = L.h('div', { class: 'motion-timeline' }, parent);
  var sl = L.slider(wrap, { id: o.id || 'time', label: o.label || 'Animation', min: 0, max: 100, step: 1, value: Math.round(t * 100), color: o.color || 'purple',
    format: o.format || function (v) { return v + '%'; }, onInput: function (v) { stop(); set(v / 100, true); } });
  var row = L.h('div', { class: 'motion-buttons', role: 'group', 'aria-label': 'Animation controls' }, wrap);
  var play = L.button(row, '▶ Play', function () { playing ? stop() : start(); });
  play.setAttribute('aria-pressed', 'false');
  L.button(row, '⟲ Start', function () { stop(); set(0); }, true);
  L.button(row, 'End ⟶', function () { stop(); set(1); }, true);
  var speed = 1;
  if (o.speeds !== false) {
    L.chips(wrap, { label: 'Speed', value: '1', options: [{ value: '0.5', label: 'Slow' }, { value: '1', label: 'Normal' }, { value: '2', label: 'Fast' }],
      onChange: function (v) { speed = +v; } });
  }
  function set(v, fromSlider) {
    t = Math.max(0, Math.min(1, v));
    if (!fromSlider) sl.set(Math.round(t * 100), true);
    o.onChange && o.onChange(t);
  }
  function frame(now) {
    if (!playing) return;
    var dt = Math.min(0.1, (now - last) / 1000); last = now;
    var nt = t + dir * dt * speed / (o.seconds || 4);
    if (nt >= 1 || nt <= 0) {
      nt = Math.max(0, Math.min(1, nt));
      if (o.loop === 'bounce') dir = -dir; else { set(nt); stop(); return; }
    }
    set(nt);
    raf = requestAnimationFrame(frame);
  }
  function start() {
    if (reduce) { set(t >= 1 ? 0 : 1); return; }
    if (t >= 1 && o.loop !== 'bounce') set(0);
    playing = true; play.textContent = '❚❚ Pause'; play.setAttribute('aria-pressed', 'true');
    last = performance.now(); raf = requestAnimationFrame(frame);
  }
  function stop() {
    playing = false; cancelAnimationFrame(raf); play.textContent = '▶ Play'; play.setAttribute('aria-pressed', 'false');
  }
  return { el: wrap, get: function () { return t; }, set: function (v) { stop(); set(v); }, play: start, stop: stop };
}

/* Smoothstep easing and a helper that maps a global t to stage k of n (0..1 inside that stage). */
function ease(x) { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); }
function stage(t, k, n) { return Math.max(0, Math.min(1, t * n - k)); }
function lerp(a, b, x) { return a + (b - a) * x; }
function lerpPt(p, q, x) { return [lerp(p[0], q[0], x), lerp(p[1], q[1], x)]; }

/* ---------- 3D ---------- */
function sub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
function add(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
function scale(a, k) { return [a[0] * k, a[1] * k, a[2] * k]; }
function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
function norm(a) { var l = Math.sqrt(dot(a, a)) || 1; return scale(a, 1 / l); }
/* Rodrigues: rotate point p about the line through a with unit direction u by angle th. */
function rotateAbout(p, a, u, th) {
  var v = sub(p, a), c = Math.cos(th), s = Math.sin(th);
  var r = add(add(scale(v, c), scale(cross(u, v), s)), scale(u, dot(u, v) * (1 - c)));
  return add(r, a);
}
/* View: yaw about the vertical axis, then pitch; returns [x, y, depth] in screen units with mild perspective. */
function project(p, view) {
  var cy = Math.cos(view.yaw), sy = Math.sin(view.yaw), cp = Math.cos(view.pitch), sp = Math.sin(view.pitch);
  var x = p[0] * cy - p[1] * sy, y = p[0] * sy + p[1] * cy, z = p[2];
  var y2 = y * cp - z * sp, z2 = y * sp + z * cp;
  var k = view.dist / (view.dist + y2);
  return [view.cx + x * view.s * k, view.cy - z2 * view.s * k, y2];
}
/* Light: brighter when a face turns toward the viewer and the light. Returns 0.55..1 for a face normal. */
function shade(n, view) {
  var cy = Math.cos(view.yaw), sy = Math.sin(view.yaw), cp = Math.cos(view.pitch), sp = Math.sin(view.pitch);
  var y = n[0] * sy + n[1] * cy, z = n[2], x = n[0] * cy - n[1] * sy;
  var y2 = y * cp - z * sp, z2 = y * sp + z * cp;
  var l = norm([-0.35, -0.75, 0.55]);
  return 0.62 + 0.38 * Math.abs(x * l[0] + y2 * l[1] + z2 * l[2]);
}
/* Drag on an SVG to turn the view; arrow keys do the same when the SVG has focus. */
function orbit(svg, view, redraw) {
  var down = null;
  svg.setAttribute('tabindex', '0');
  svg.addEventListener('pointerdown', function (e) { down = [e.clientX, e.clientY, view.yaw, view.pitch]; try { svg.setPointerCapture(e.pointerId); } catch (x) {} });
  svg.addEventListener('pointermove', function (e) {
    if (!down) return;
    view.yaw = down[2] + (e.clientX - down[0]) * 0.01;
    view.pitch = Math.max(-1.45, Math.min(1.45, down[3] + (e.clientY - down[1]) * 0.01));
    redraw();
  });
  svg.addEventListener('pointerup', function () { down = null; });
  svg.addEventListener('pointercancel', function () { down = null; });
  svg.addEventListener('keydown', function (e) {
    var k = { ArrowLeft: [-0.12, 0], ArrowRight: [0.12, 0], ArrowUp: [0, -0.1], ArrowDown: [0, 0.1] }[e.key];
    if (!k) return; e.preventDefault();
    view.yaw += k[0]; view.pitch = Math.max(-1.45, Math.min(1.45, view.pitch + k[1])); redraw();
  });
}
/* Remove the shared "keep your printed worksheet" note on labs that have no worksheet yet. */
function noWorksheetNote(P) {
  var n = P.below && P.below.querySelector('.note');
  if (n && /Worksheet/.test(n.textContent)) n.remove();
}
var css = '.motion-buttons{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 10px}.motion-timeline{border-bottom:1px solid var(--line);padding-bottom:8px;margin-bottom:8px}' +
  '.motion-readout{font-variant-numeric:tabular-nums}.motion-readout b{font-family:var(--display)}.motion-step{font-weight:700;color:var(--purple);min-height:1.4em;margin:4px 6px}';
var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

G.Motion = { timeline: timeline, ease: ease, stage: stage, lerp: lerp, lerpPt: lerpPt, reduce: reduce,
  v3: { sub: sub, add: add, scale: scale, dot: dot, cross: cross, norm: norm }, rotateAbout: rotateAbout, project: project, shade: shade, orbit: orbit,
  noWorksheetNote: noWorksheetNote };
})(window);
