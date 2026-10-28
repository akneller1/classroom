/* Procedural Geometry figures (inline SVG), data-driven.
   Every figure is drawn from the same numbers the question uses, so the picture, the labels and the
   answer cannot drift apart. Specs are plain JSON (no DOM): they survive the engine's dedupe/hash step,
   saved assessments and the answer key.

   Kinds: geo-transversal, geo-adjacent, geo-cross, geo-quad, geo-regular, geo-circle
   F.render(spec) -> html | ''      F.check(spec) -> {ok, msg}      F.owns(spec) -> boolean
   Figures are black-on-white with solid strokes so they survive photocopying. A figure is labelled
   "not to scale" whenever its picture is a standard layout rather than the true shape. */
(function (G) {
  'use strict';
  var NS = G.MKMENU = (G.MKMENU || {}), F = NS.geoFigures = {};
  var KINDS = ['geo-transversal', 'geo-quad', 'geo-circle', 'geo-adjacent', 'geo-cross', 'geo-regular'];
  var W = 430, FS = 14, INK = '#111';

  /* ---------- small helpers ---------- */
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function r1(n) { return Math.round(n * 10) / 10; }
  function rad(d) { return d * Math.PI / 180; }
  function dir(d) { return [Math.cos(rad(d)), -Math.sin(rad(d))]; }            // math degrees (CCW) -> screen unit vector
  function ang(from, to) { return Math.atan2(-(to[1] - from[1]), to[0] - from[0]) * 180 / Math.PI; }   // screen points -> math degrees
  function norm(d) { d = d % 360; return d < 0 ? d + 360 : d; }
  function dist(p, q) { return Math.hypot(p[0] - q[0], p[1] - q[1]); }
  function textW(s) { return String(s).length * FS * 0.56; }
  function wrap(inner, h, desc, note, vx, vw) {
    vx = vx || 0; vw = vw || W;
    return '<div class="mm-geometry-figure" style="break-inside:avoid"><svg xmlns="http://www.w3.org/2000/svg" viewBox="' + r1(vx) + ' 0 ' + r1(vw) + ' ' + h + '" width="' + r1(4.1 * vw / W) + 'in" style="max-width:100%;height:auto" role="img" aria-label="' + esc(desc) + '"><rect x="' + r1(vx) + '" width="' + r1(vw) + '" height="' + h + '" fill="white"/>' + inner + '</svg>' +
      (note ? '<div style="font-size:10px;color:#555">' + esc(note) + '</div>' : '') + '</div>';
  }
  function T(x, y, s, anchor, italic, rot) {
    return '<text x="' + r1(x) + '" y="' + r1(y + FS * 0.35) + '" text-anchor="' + (anchor || 'middle') + '" font-family="Arial,sans-serif" font-size="' + FS + '"' + (italic ? ' font-style="italic"' : '') + (rot ? ' transform="rotate(' + r1(rot) + ' ' + r1(x) + ' ' + r1(y) + ')"' : '') + ' fill="' + INK + '">' + esc(s) + '</text>';
  }
  function L(p, q, w, dash) {
    return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' L' + r1(q[0]) + ' ' + r1(q[1]) + '" stroke="' + INK + '" stroke-width="' + (w || 2.4) + '" fill="none"' + (dash ? ' stroke-dasharray="6 4"' : '') + ' stroke-linecap="round"/>';
  }
  function dot(p, r) { return '<circle cx="' + r1(p[0]) + '" cy="' + r1(p[1]) + '" r="' + (r || 3) + '" fill="' + INK + '"/>'; }
  /* arc of radius r about v from math direction a1 sweeping CCW to a2 */
  function arcPath(v, a1, a2, r, w) {
    var s = dir(a1), e = dir(a2), span = norm(a2 - a1);
    return '<path d="M' + r1(v[0] + r * s[0]) + ' ' + r1(v[1] + r * s[1]) + ' A' + r + ' ' + r + ' 0 ' + (span > 180 ? 1 : 0) + ' 0 ' + r1(v[0] + r * e[0]) + ' ' + r1(v[1] + r * e[1]) + '" stroke="' + INK + '" stroke-width="' + (w || 1.5) + '" fill="none"/>';
  }
  /* the short way from direction a to direction b: returns [start, end] sweeping CCW */
  function shortWedge(a, b) { var d = norm(b - a); return d <= 180 ? [a, b] : [b, a]; }
  function rightMark(v, a, b, s) {
    s = s || 10; var u = dir(a), w = dir(b), p = [v[0] + s * u[0], v[1] + s * u[1]], q = [p[0] + s * w[0], p[1] + s * w[1]], z = [v[0] + s * w[0], v[1] + s * w[1]];
    return '<path d="M' + r1(p[0]) + ' ' + r1(p[1]) + ' L' + r1(q[0]) + ' ' + r1(q[1]) + ' L' + r1(z[0]) + ' ' + r1(z[1]) + '" stroke="' + INK + '" stroke-width="1.5" fill="none"/>';
  }
  function ticks(p, q, n, at) {
    var t = at === undefined ? 0.5 : at, m = [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t], d = dist(p, q) || 1, ux = (q[0] - p[0]) / d, uy = (q[1] - p[1]) / d, o = '';
    for (var j = 0; j < n; j++) { var k = (j - (n - 1) / 2) * 6, x = m[0] + k * ux, y = m[1] + k * uy; o += '<path d="M' + r1(x - 6 * uy) + ' ' + r1(y + 6 * ux) + ' L' + r1(x + 6 * uy) + ' ' + r1(y - 6 * ux) + '" stroke="' + INK + '" stroke-width="1.7"/>'; }
    return o;
  }
  /* parallel-line chevrons ">" (n of them) at fraction t along p->q */
  function chevrons(p, q, n, t) {
    var m = [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t], a = ang(p, q), u = dir(a), o = '';
    for (var j = 0; j < n; j++) {
      var k = (j - (n - 1) / 2) * 7, c = [m[0] + k * u[0], m[1] + k * u[1]], b1 = dir(a + 150), b2 = dir(a - 150);
      o += '<path d="M' + r1(c[0] + 6 * b1[0]) + ' ' + r1(c[1] + 6 * b1[1]) + ' L' + r1(c[0]) + ' ' + r1(c[1]) + ' L' + r1(c[0] + 6 * b2[0]) + ' ' + r1(c[1] + 6 * b2[1]) + '" stroke="' + INK + '" stroke-width="1.6" fill="none"/>';
    }
    return o;
  }
  function inBox(x, y, b) { return x > b[0] && x < b[2] && y > b[1] && y < b[3]; }
  /* Find a spot for text inside the wedge a1..a2 (math degrees, CCW) at vertex v, clear of the bounding rays.
     Steps outward until the text box (padded) touches neither ray. */
  function boxHit(a, b) { return a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1]; }
  function placeInWedge(v, a1, a2, text, rays, used, poly) {
    var w = textW(text) + 9, h = FS + 7, span = norm(a2 - a1), mid = a1 + span / 2, offs = [0], k;
    for (k = 1; k <= 6; k++) { var o = k * span / 14; offs.push(o, -o); }      // bisector first, then toward either ray
    for (var r = 26; r <= 100; r += 2) {
      for (var j = 0; j < offs.length; j++) {
        var u = dir(mid + offs[j]), cx = v[0] + r * u[0], cy = v[1] + r * u[1], box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], hit = false;
        (rays || [a1, a2]).forEach(function (d) {
          var e = dir(d);
          for (var s = 0; s <= 110 && !hit; s += 2) if (inBox(v[0] + s * e[0], v[1] + s * e[1], box)) hit = true;
        });
        if (!hit && used) used.forEach(function (q) { if (boxHit(box, q)) hit = true; });
        if (!hit && poly && !(inPoly([box[0], box[1]], poly) && inPoly([box[2], box[1]], poly) && inPoly([box[0], box[3]], poly) && inPoly([box[2], box[3]], poly))) hit = true;
        if (!hit) { if (used) used.push(box); return [cx, cy]; }
      }
    }
    // nothing fits inside a narrow wedge: sit just outside it and join the label to the arc with a leader
    var target = [v[0] + 17 * dir(mid)[0], v[1] + 17 * dir(mid)[1]];
    for (var r2 = 30; r2 <= 52; r2 += 4) for (var e = span / 2 + 18; e <= span / 2 + 110; e += 14) for (var sg = -1; sg <= 1; sg += 2) {
      var u3 = dir(mid + sg * e), cx2 = v[0] + r2 * u3[0], cy2 = v[1] + r2 * u3[1], bx = [cx2 - w / 2, cy2 - h / 2, cx2 + w / 2, cy2 + h / 2], bad = false;
      [a1, a2].concat(rays || []).forEach(function (d) { var ee = dir(d); for (var s2 = 0; s2 <= 110 && !bad; s2 += 2) if (inBox(v[0] + s2 * ee[0], v[1] + s2 * ee[1], bx)) bad = true; });
      if (!bad && used) used.forEach(function (q) { if (boxHit(bx, q)) bad = true; });
      if (!bad && poly && !(inPoly([bx[0], bx[1]], poly) && inPoly([bx[2], bx[1]], poly) && inPoly([bx[0], bx[3]], poly) && inPoly([bx[2], bx[3]], poly))) bad = true;
      if (!bad) { if (used) used.push(bx); return [cx2, cy2, target]; }
    }
    var u2 = dir(mid); return [v[0] + 40 * u2[0], v[1] + 40 * u2[1]];
  }
  /* text with an optional short leader to the arc it labels (when placeInWedge had to sit outside the wedge) */
  function TL(pos, text) {
    var o = '';
    if (pos[2]) { var d = [pos[2][0] - pos[0], pos[2][1] - pos[1]], n = Math.hypot(d[0], d[1]) || 1, a0 = [pos[0] + d[0] / n * Math.min(textW(text) / 2 + 2, n - 3), pos[1] + d[1] / n * (FS / 2)]; o = L(a0, pos[2], 0.9); }
    return o + T(pos[0], pos[1], text);
  }
  /* label beside the middle of segment p->q, on the left (side=1) or right (side=-1) of the direction p->q */
  function sideLabel(p, q, text, side, off) {
    var m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], a = ang(p, q), n = dir(a + 90 * (side || 1)), o = (off || 12) + Math.abs(n[0]) * textW(text) / 2 + Math.abs(n[1]) * 3;
    return T(m[0] + n[0] * o, m[1] + n[1] * o, text);
  }
  function boxOf(x, y, text) { var w = textW(text) + 6, h = FS + 4; return [x - w / 2, y - h / 2, x + w / 2, y + h / 2]; }

  function inPoly(pt, poly) {
    var c = false, i, j;
    for (i = 0, j = poly.length - 1; i < poly.length; j = i++)
      if (((poly[i][1] > pt[1]) !== (poly[j][1] > pt[1])) && (pt[0] < (poly[j][0] - poly[i][0]) * (pt[1] - poly[i][1]) / (poly[j][1] - poly[i][1]) + poly[i][0])) c = !c;
    return c;
  }
  function boxTouchesLine(box, p, q) {
    var n = Math.max(2, Math.ceil(dist(p, q) / 3));
    for (var i = 0; i <= n; i++) if (inBox(p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n, box)) return true;
    return false;
  }
  /* Label for segment p->q: tries positions beside it (preferred side first, then the other; nearer first;
     fractions along the segment around `t`) and takes the first whose box touches no drawn line and no other label. */
  function placeBeside(p, q, text, o) {
    o = o || {}; var used = o.used || [], t0 = o.t === undefined ? 0.5 : o.t, side = o.side || 1, a = ang(p, q), w = textW(text) + 8, h = FS + 6, ts = [0, 0.1, -0.1, 0.2, -0.2, 0.3, -0.3], rot = null;
    var lines = (o.lines || []).filter(function (l) { return !(o.rotate && ((l[0] === p && l[1] === q) || (l[0] === q && l[1] === p))); });
    if (o.rotate) { rot = a; if (rot > 90) rot -= 180; if (rot < -90) rot += 180; rot = -rot; var cr = Math.abs(Math.cos(rad(rot))), sr = Math.abs(Math.sin(rad(rot))), w0 = w, h0 = h; w = w0 * cr + h0 * sr; h = w0 * sr + h0 * cr; }
    if (o.rotate) { var nr = dir(a + 90 * side), mr = [p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0]; return { x: mr[0] + nr[0] * 11, y: mr[1] + nr[1] * 11, rot: rot }; }
    for (var off = 8; off <= 30; off += 3) for (var ti = 0; ti < ts.length; ti++) {
      var t = t0 + ts[ti]; if (t < 0.12 || t > 0.88) continue;
      for (var sd = 0; sd < 2; sd++) {
        var sg = sd ? -side : side, n = dir(a + 90 * sg), m = [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t], e = off + Math.abs(n[0]) * w / 2 + Math.abs(n[1]) * h / 2, cx = m[0] + n[0] * e, cy = m[1] + n[1] * e;
        var box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], hit = box[0] < 2 || box[2] > W - 2 || box[1] < 2 || box[3] > (o.H || 170) - 2;
        for (var li = 0; li < lines.length && !hit; li++) if (boxTouchesLine(box, lines[li][0], lines[li][1])) hit = true;
        for (var ui = 0; ui < used.length && !hit; ui++) if (boxHit(box, used[ui])) hit = true;
        if (!hit) { used.push(box); return { x: cx, y: cy, rot: rot }; }
      }
    }
    var n2 = dir(a + 90 * side), m2 = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2]; return { x: m2[0] + n2[0] * 18, y: m2[1] + n2[1] * 18, rot: rot };
  }

  /* =====================================================================
     1. Parallel lines and a transversal
     spec: { kind:'geo-transversal', marks:[{pos:1..8, text:'(3x+5)°', deg:98}], numbered:bool, names:['ℓ','m'] }
     Positions: at the upper intersection 1=upper-left, 2=upper-right, 3=lower-left, 4=lower-right;
                at the lower intersection 5,6,7,8 the same way.
     If the upper-right wedge measures phi: positions 2,3,6,7 measure phi, positions 1,4,5,8 measure 180-phi.
     ===================================================================== */
  var SAME_PHI = { 2: 1, 3: 1, 6: 1, 7: 1 };
  function posDeg(pos, phi) { return SAME_PHI[pos] ? phi : 180 - phi; }
  /* relationship between two positions (for tests and for skill prompts) */
  F.relationship = function (p, q) {
    var k = Math.min(p, q) + '-' + Math.max(p, q), t = {
      '1-5': 'corresponding', '2-6': 'corresponding', '3-7': 'corresponding', '4-8': 'corresponding',
      '3-6': 'alternate-interior', '4-5': 'alternate-interior', '1-8': 'alternate-exterior', '2-7': 'alternate-exterior',
      '3-5': 'same-side-interior', '4-6': 'same-side-interior', '1-7': 'same-side-exterior', '2-8': 'same-side-exterior',
      '1-4': 'vertical', '2-3': 'vertical', '5-8': 'vertical', '6-7': 'vertical',
      '1-2': 'linear-pair', '1-3': 'linear-pair', '2-4': 'linear-pair', '3-4': 'linear-pair', '5-6': 'linear-pair', '5-7': 'linear-pair', '6-8': 'linear-pair', '7-8': 'linear-pair'
    };
    return t[k] || 'none';
  };
  /* equal measures or supplementary (sum 180)? */
  F.relationEquals = function (rel) { return /corresponding|alternate|vertical/.test(rel); };
  F.relationSupplementary = function (rel) { return /same-side|linear-pair/.test(rel); };
  F.positionsFor = function (rel, pick) {
    var m = { 'corresponding': [[1, 5], [2, 6], [3, 7], [4, 8]], 'alternate-interior': [[3, 6], [4, 5]], 'alternate-exterior': [[1, 8], [2, 7]], 'same-side-interior': [[3, 5], [4, 6]], 'same-side-exterior': [[1, 7], [2, 8]], 'vertical': [[1, 4], [2, 3]], 'linear-pair': [[1, 2], [3, 4], [1, 3], [2, 4]] }[rel];
    return m[pick % m.length];
  };
  function impliedPhi(marks) {
    var ps = [];
    (marks || []).forEach(function (m) { if (typeof m.deg === 'number') ps.push(SAME_PHI[m.pos] ? m.deg : 180 - m.deg); });
    return ps;
  }
  function transversal(spec) {
    var phis = impliedPhi(spec.marks), phi = phis.length ? phis[0] : 65, toScale = true, shown = phi;
    if (shown < 35) { shown = 35; toScale = false; } if (shown > 145) { shown = 145; toScale = false; }
    var y1 = 44, y2 = 124, gap = y2 - y1, dxh = gap / Math.tan(rad(shown)), P = [215 + dxh / 2, y1], Q = [215 - dxh / 2, y2], u = dir(shown), ext = 26;
    var topEnd = [P[0] + ext * u[0], P[1] + ext * u[1]], botEnd = [Q[0] - ext * u[0], Q[1] - ext * u[1]], nm = spec.names || ['ℓ', 'm'];
    var h = L([40, y1], [392, y1]) + L([40, y2], [392, y2]) + L(botEnd, topEnd) + chevrons([40, y1], [392, y1], 1, 0.1) + chevrons([40, y2], [392, y2], 1, 0.1) +
      T(24, y1, nm[0], 'middle', true) + T(24, y2, nm[1], 'middle', true) + T(topEnd[0] + 13 * u[0], topEnd[1] + 13 * u[1], 't', 'middle', true);
    var wedge = { 1: [shown, 180], 2: [0, shown], 3: [180, 180 + shown], 4: [180 + shown, 360] };
    function at(pos) { var up = pos <= 4, w = wedge[up ? pos : pos - 4]; return { v: up ? P : Q, a1: w[0], a2: w[1] }; }
    var marked = {}, used = [boxOf(topEnd[0] + 13 * u[0], topEnd[1] + 13 * u[1], 't')];
    (spec.marks || []).forEach(function (m) { marked[m.pos] = m; });
    (spec.marks || []).forEach(function (m) {
      var g = at(m.pos), rays = [0, 180, shown, 180 + shown], pos;
      h += arcPath(g.v, g.a1, g.a2, 16, 1.6);
      pos = placeInWedge(g.v, g.a1, g.a2, m.text, [g.a1, g.a2], used);
      h += TL(pos, m.text);
    });
    if (spec.numbered) for (var k = 1; k <= 8; k++) {
      if (marked[k]) continue;
      var g = at(k), pos = placeInWedge(g.v, g.a1, g.a2, '8', [g.a1, g.a2], used);
      h += '<circle cx="' + r1(pos[0]) + '" cy="' + r1(pos[1]) + '" r="8.5" fill="white" stroke="' + INK + '" stroke-width="1.2"/>' + TL(pos, String(k));
    }
    return wrap(h, 160, 'Parallel lines ' + nm[0] + ' and ' + nm[1] + ' cut by a transversal t' + (spec.marks && spec.marks.length ? ', with angles marked' : ''),
      'Lines ' + nm[0] + ' and ' + nm[1] + ' are parallel (marked >).' + (toScale ? '' : ' Not drawn to scale.'));
  }
  function checkTransversal(spec) {
    var m = spec.marks || [], seen = {};
    if (!m.length) return { ok: !!spec.numbered, msg: 'no angles marked' };
    for (var i = 0; i < m.length; i++) {
      if (!(m[i].pos >= 1 && m[i].pos <= 8) || seen[m[i].pos]) return { ok: false, msg: 'bad or duplicate angle position' };
      seen[m[i].pos] = 1; if (!m[i].text) return { ok: false, msg: 'blank angle label' };
      if (typeof m[i].deg === 'number' && !(m[i].deg > 0 && m[i].deg < 180)) return { ok: false, msg: 'angle outside 0–180' };
    }
    var ph = impliedPhi(m);
    for (var j = 1; j < ph.length; j++) if (Math.abs(ph[j] - ph[0]) > 0.01) return { ok: false, msg: 'marked angle measures do not agree with parallel lines' };
    return { ok: true };
  }

  /* =====================================================================
     1b. Adjacent angles (complementary / supplementary) and crossing lines (vertical angles, linear pairs)
     geo-adjacent: { relation:'complement'|'supplement', parts:[{text,deg},{text,deg}] }
                   parts[0] is beside the right-hand ray, parts[1] beside the up (complement) or left (supplement) ray
     geo-cross:    { marks:[{pos:1..4,text,deg}] }  wedge 1 is between the two lines' first rays (counterclockwise),
                   2 next, 3 is vertical to 1, 4 is vertical to 2
     ===================================================================== */
  function clampShown(d, lo, hi) { return d < lo ? [lo, false] : d > hi ? [hi, false] : [d, true]; }
  function adjacent(spec) {
    var comp = spec.relation === 'complement', p = spec.parts, c = clampShown(p[0].deg, comp ? 22 : 28, comp ? 68 : 152), d1 = c[0], O = comp ? [120, 138] : [215, 138], used = [];
    var right = [comp ? 310 : 372, 138], other = comp ? [120, 24] : [58, 138], tip = [O[0] + 150 * dir(d1)[0], O[1] + 150 * dir(d1)[1]];
    if (tip[1] < 18) { var k = (O[1] - 18) / (O[1] - tip[1]); tip = [O[0] + (tip[0] - O[0]) * k, O[1] + (tip[1] - O[1]) * k]; }
    var h = L(O, right) + L(O, other) + L(O, tip) + dot(O, 3);
    var w2 = comp ? 90 : 180;
    if (comp) h += rightMark(O, 0, 90, 11);
    h += arcPath(O, 0, d1, comp ? 24 : 22, 1.6) + arcPath(O, d1, w2, comp ? 24 : 22, 1.6);
    var q1 = placeInWedge(O, 0, d1, p[0].text, [0, d1], used), q2 = placeInWedge(O, d1, w2, p[1].text, [d1, w2], used);
    h += TL(q1, p[0].text) + TL(q2, p[1].text);
    return wrap(h, 160, comp ? 'A right angle split into two adjacent angles' : 'A straight angle split into two adjacent angles', c[1] ? '' : 'Not drawn to scale.');
  }
  function checkAdjacent(spec) {
    var p = spec.parts, tot = spec.relation === 'complement' ? 90 : spec.relation === 'supplement' ? 180 : 0;
    if (!tot || !p || p.length !== 2 || !p[0].text || !p[1].text) return { ok: false, msg: 'adjacent angles need a relation and two labelled parts' };
    if (!(p[0].deg > 0 && p[1].deg > 0) || Math.abs(p[0].deg + p[1].deg - tot) > 0.01) return { ok: false, msg: 'adjacent angle measures do not add to ' + tot };
    return { ok: true };
  }
  function crossImplied(marks) { return (marks || []).filter(function (m) { return typeof m.deg === 'number'; }).map(function (m) { return m.pos % 2 ? m.deg : 180 - m.deg; }); }
  function cross(spec) {
    var im = crossImplied(spec.marks), w1 = im.length ? im[0] : 65, c = clampShown(w1, 35, 145), a = 12, b = a + c[0], O = [215, 84], used = [], h = '';
    var ends = [a, b, a + 180, b + 180].map(function (d) { var u = dir(d), len = Math.abs(u[0]) > 0.001 ? Math.min(150 / Math.abs(u[0]), 70 / Math.max(Math.abs(u[1]), 0.001)) : 70; return [O[0] + len * u[0], O[1] + len * u[1]]; });
    h += L(ends[2], ends[0]) + L(ends[3], ends[1]) + dot(O, 3);
    var wedges = { 1: [a, b], 2: [b, a + 180], 3: [a + 180, b + 180], 4: [b + 180, a + 360] };
    (spec.marks || []).forEach(function (m) {
      var w = wedges[m.pos], q = placeInWedge(O, w[0], w[1], m.text, [w[0], w[1]], used);
      h += arcPath(O, w[0], w[1], 16, 1.6) + TL(q, m.text);
    });
    return wrap(h, 170, 'Two intersecting lines forming four angles', c[1] ? '' : 'Not drawn to scale.');
  }
  function checkCross(spec) {
    var m = spec.marks || [], seen = {};
    if (!m.length) return { ok: false, msg: 'no angles marked' };
    for (var i = 0; i < m.length; i++) {
      if (!(m[i].pos >= 1 && m[i].pos <= 4) || seen[m[i].pos] || !m[i].text) return { ok: false, msg: 'bad or duplicate angle' };
      seen[m[i].pos] = 1; if (typeof m[i].deg === 'number' && !(m[i].deg > 0 && m[i].deg < 180)) return { ok: false, msg: 'angle outside 0–180' };
    }
    var im = crossImplied(m); for (var j = 1; j < im.length; j++) if (Math.abs(im[j] - im[0]) > 0.01) return { ok: false, msg: 'marked angle measures do not agree with the crossing lines' };
    return { ok: true };
  }
  /* which relationship do two wedge numbers of geo-cross show? */
  F.crossRelationship = function (p, q) { return (p - q) % 2 === 0 ? 'vertical' : 'linear-pair'; };

  /* =====================================================================
     2. Quadrilaterals
     spec: { kind:'geo-quad', shape, diagonals, ticks:[{segs:['AB','CD'], n}], arcs:[{v:'A', n, between?:['B','D']}],
             right:[['A','B','D']], parallel:[['AB','DC',n]], seg:{AB:'3x+2', AE:'x'}, angle:{A:'(2x+10)°'},
             mid:true (trapezoid midsegment MN), showE:bool }
     Vertices are always A (lower-left) B (lower-right) C (upper-right) D (upper-left), counterclockwise.
     ===================================================================== */
  var QUAD = {
    parallelogram: { A: [80, 138], B: [290, 138], C: [352, 32], D: [142, 32] },
    rectangle: { A: [90, 138], B: [340, 138], C: [340, 32], D: [90, 32] },
    rhombus: { A: [66, 85], B: [215, 142], C: [364, 85], D: [215, 28] },
    square: { A: [150, 142], B: [262, 142], C: [262, 30], D: [150, 30] },
    trapezoid: { A: [66, 138], B: [364, 138], C: [300, 32], D: [130, 32] },
    kite: { A: [215, 20], B: [335, 80], C: [215, 150], D: [95, 80] }
  };
  F.quadShapes = Object.keys(QUAD);
  function intersect(p1, p2, p3, p4) {
    var d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0]);
    if (Math.abs(d) < 1e-9) return null;
    var a = p1[0] * p2[1] - p1[1] * p2[0], b = p3[0] * p4[1] - p3[1] * p4[0];
    return [(a * (p3[0] - p4[0]) - (p1[0] - p2[0]) * b) / d, (a * (p3[1] - p4[1]) - (p1[1] - p2[1]) * b) / d];
  }
  /* A convex quadrilateral with the four given interior angles (degrees, in order A,B,C,D), drawn to scale in angle. */
  /* How well does the quadrilateral with side lengths Ls along unit directions U use the 290 x 104 drawing area?
     Score = its drawn area in px^2 after fitting, 0 if any side would be drawn shorter than 38px. */
  function roundness(Ls, U) {
    var pts = [[0, 0]], i, area = 0;
    for (i = 0; i < 3; i++) pts.push([pts[i][0] + Ls[i] * U[i][0], pts[i][1] + Ls[i] * U[i][1]]);
    var xs = pts.map(function (q) { return q[0]; }), ys = pts.map(function (q) { return q[1]; });
    var sc = Math.min(290 / ((Math.max.apply(null, xs) - Math.min.apply(null, xs)) || 1), 104 / ((Math.max.apply(null, ys) - Math.min.apply(null, ys)) || 1));
    for (i = 0; i < 4; i++) { var a = pts[i], b = pts[(i + 1) % 4]; area += a[0] * b[1] - b[0] * a[1]; if (Ls[i] * sc < 38) return 0; }
    return Math.abs(area) / 2 * sc * sc / 10000;
  }
  function generalQuad(an, wantQ) {
    if (!an || an.length !== 4 || an.some(function (a) { return !(a > 0 && a < 180); }) || Math.abs(an[0] + an[1] + an[2] + an[3] - 360) > 0.01) return null;
    var d2 = 180 - an[1], d3 = d2 + 180 - an[2], d4 = d3 + 180 - an[3], u = [dir(0), dir(d2), dir(d3), dir(d4)], best = null;
    // dir() is in screen coordinates (y down); the construction below is done in math coordinates, so flip y back
    function m(v) { return [v[0], -v[1]]; }
    var U = u.map(m);
    for (var t = 0.35; t <= 3.01; t += 0.05) {
      var rx = -(1 + t * U[1][0]), ry = -(t * U[1][1]), det = U[2][0] * U[3][1] - U[3][0] * U[2][1];
      if (Math.abs(det) < 1e-9) continue;
      var L3 = (rx * U[3][1] - U[3][0] * ry) / det, L4 = (U[2][0] * ry - rx * U[2][1]) / det;
      if (L3 <= 0.15 || L4 <= 0.15) continue;
      var Ls = [1, t, L3, L4], q = roundness(Ls, U);
      if (!best || q > best.q) best = { q: q, L: Ls };
    }
    if (!best) return null;
    if (wantQ) return { q: best.q };
    var pts = [[0, 0]], i; for (i = 0; i < 3; i++) pts.push([pts[i][0] + best.L[i] * U[i][0], pts[i][1] + best.L[i] * U[i][1]]);
    var xs = pts.map(function (p) { return p[0]; }), ys = pts.map(function (p) { return p[1]; }), x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var sc = Math.min(290 / (x1 - x0 || 1), 104 / (y1 - y0 || 1)), ox = 215 - sc * (x0 + x1) / 2, oy = 85 + sc * (y0 + y1) / 2, out = {};
    ['A', 'B', 'C', 'D'].forEach(function (k, j) { out[k] = [ox + sc * pts[j][0], oy - sc * pts[j][1]]; });
    return out;
  }
  /* roundness of the best quadrilateral with these interior angles (0 if there is none) */
  F.quadRoundness = function (an) {
    var q = generalQuad(an, true); return q ? q.q : 0;
  };
  /* the ordering of four angle values (as indices) that draws the roundest quadrilateral */
  F.bestQuadOrder = function (vals) {
    var best = null, idx = [0, 1, 2, 3];
    (function perm(a, k) {
      if (k === a.length) { var q = F.quadRoundness(a.map(function (i) { return vals[i]; })); if (!best || q > best.q) best = { q: q, order: a.slice() }; return; }
      for (var i = k; i < a.length; i++) { var t = a[k]; a[k] = a[i]; a[i] = t; perm(a, k + 1); t = a[k]; a[k] = a[i]; a[i] = t; }
    })(idx, 0);
    return best;
  };
  function quadPoints(spec) {
    var base = spec.shape === 'general' ? generalQuad(spec.angles) : QUAD[spec.shape]; if (!base) return null;
    var P = {}; ['A', 'B', 'C', 'D'].forEach(function (k) { P[k] = base[k].slice(); });
    P.E = intersect(P.A, P.C, P.B, P.D);
    P.M = [(P.A[0] + P.D[0]) / 2, (P.A[1] + P.D[1]) / 2]; P.N = [(P.B[0] + P.C[0]) / 2, (P.B[1] + P.C[1]) / 2];
    return P;
  }
  var NEIGH = { A: ['B', 'D'], B: ['C', 'A'], C: ['D', 'B'], D: ['A', 'C'] };
  function quad(spec) {
    var P = quadPoints(spec); if (!P) return '';
    var cx = (P.A[0] + P.B[0] + P.C[0] + P.D[0]) / 4, cy = (P.A[1] + P.B[1] + P.C[1] + P.D[1]) / 4, h = '', used = [], lines = [], poly = [P.A, P.B, P.C, P.D];
    ['AB', 'BC', 'CD', 'DA'].forEach(function (k) { h += L(P[k[0]], P[k[1]]); lines.push([P[k[0]], P[k[1]]]); });
    if (spec.diagonals) { h += L(P.A, P.C, 1.9) + L(P.B, P.D, 1.9); lines.push([P.A, P.C], [P.B, P.D]); }
    if (spec.mid) { h += L(P.M, P.N, 2.2, true) + dot(P.M, 2.6) + dot(P.N, 2.6); lines.push([P.M, P.N]); }
    (spec.ticks || []).forEach(function (g) { g.segs.forEach(function (k) { h += ticks(P[k[0]], P[k[1]], g.n || 1); }); });
    (spec.parallel || []).forEach(function (g) { for (var i = 0; i < 2; i++) h += chevrons(P[g[i][0]], P[g[i][1]], g[2] || 1, 0.5); });
    (spec.right || []).forEach(function (r) { var v = P[r[0]]; h += rightMark(v, ang(v, P[r[1]]), ang(v, P[r[2]]), 10); });
    (spec.arcs || []).forEach(function (a) {
      var v = P[a.v], nb = a.between || NEIGH[a.v], w = shortWedge(ang(v, P[nb[0]]), ang(v, P[nb[1]]));
      for (var i = 0; i < (a.n || 1); i++) h += arcPath(v, w[0], w[1], 15 + 4 * i, 1.5);
    });
    // vertex letters, just outside each corner
    ['A', 'B', 'C', 'D'].forEach(function (k) {
      var d = [P[k][0] - cx, P[k][1] - cy], n = Math.hypot(d[0], d[1]) || 1, x = P[k][0] + 15 * d[0] / n, y = P[k][1] + 15 * d[1] / n;
      h += T(x, y, k); used.push(boxOf(x, y, k));
    });
    if (spec.mid) {
      h += T(P.M[0] - 13, P.M[1], 'M') + T(P.N[0] + 13, P.N[1], 'N'); used.push(boxOf(P.M[0] - 13, P.M[1], 'M'), boxOf(P.N[0] + 13, P.N[1], 'N'));
    }
    if (spec.diagonals) {
      // E goes in the widest free wedge between the diagonals (not one holding a right-angle mark)
      var rays = ['A', 'B', 'C', 'D'].map(function (k) { return ang(P.E, P[k]); }).sort(function (x, y) { return norm(x) - norm(y); }), best = null;
      for (var i = 0; i < 4; i++) {
        var a1 = rays[i], a2 = rays[(i + 1) % 4], span = norm(a2 - a1), mid = norm(a1 + span / 2), taken = false;
        (spec.right || []).forEach(function (r) { if (r[0] === 'E') { var w = shortWedge(ang(P.E, P[r[1]]), ang(P.E, P[r[2]])); if (norm(mid - w[0]) < norm(w[1] - w[0])) taken = true; } });
        if (!taken && (!best || span > best.span + 1e-6)) best = { a1: a1, a2: a2, span: span };
      }
      var ep = best ? placeInWedge(P.E, best.a1, best.a2, 'E', [best.a1, best.a2], used) : [P.E[0] + 11, P.E[1] + 12];
      h += dot(P.E, 2.6) + TL(ep, 'E');
    }
    // segment labels
    Object.keys(spec.seg || {}).forEach(function (k) {
      var p = P[k[0]], q = P[k[1]], m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2], a = ang(p, q), n = dir(a + 90), side = 1;
      var isSide = ['AB', 'BC', 'CD', 'DA', 'BA', 'CB', 'DC', 'AD'].indexOf(k) >= 0, whole = (k === 'AC' || k === 'BD' || k === 'CA' || k === 'DB') && spec.diagonals;
      if (isSide) { if ((n[0] * (m[0] - cx) + n[1] * (m[1] - cy)) < 0) side = -1; }
      else if (n[1] > 0.05 || (Math.abs(n[1]) <= 0.05 && n[0] < 0)) side = -1;
      if (whole) side = -side;
      var t = (spec.segAt && spec.segAt[k] !== undefined) ? spec.segAt[k] : whole ? 0.27 : 0.5;
      var pos = placeBeside(p, q, spec.seg[k], { t: t, side: side, lines: whole ? [] : lines, used: used, rotate: whole });
      h += T(pos.x, pos.y, spec.seg[k], 'middle', false, pos.rot);
    });
    // angle labels (inside the corner; with diagonals drawn, in the half-wedge beside the first neighbour)
    Object.keys(spec.angle || {}).forEach(function (k) {
      var v = P[k], nb = (spec.angleBetween && spec.angleBetween[k]) || NEIGH[k], w = shortWedge(ang(v, P[nb[0]]), ang(v, P[nb[1]])), drawn = false;
      (spec.arcs || []).forEach(function (a) { if (a.v === k) drawn = true; });
      if (spec.diagonals && !spec.angleBetween) {
        var opp = { A: 'C', B: 'D', C: 'A', D: 'B' }[k], dd = ang(v, P[opp]);
        if (norm(dd - w[0]) < norm(w[1] - w[0])) { var w1 = shortWedge(ang(v, P[nb[0]]), dd); w = [w1[0], w1[1]]; }
      }
      if (!drawn) h += arcPath(v, w[0], w[1], 15, 1.5);
      var pos = placeInWedge(v, w[0], w[1], spec.angle[k], [w[0], w[1]], used, poly);
      h += TL(pos, spec.angle[k]);
    });
    return wrap(h, 170, 'Quadrilateral ABCD (' + spec.shape + ')' + (spec.diagonals ? ' with diagonals AC and BD meeting at E' : ''), 'Not drawn to scale. Use the markings and labels.');
  }
  /* Every mark must be true of the figure as drawn: tick groups equal in length, same-count angle arcs equal,
     right-angle marks 90 degrees, parallel marks parallel. A mark that the drawing contradicts is a wrong figure. */
  function checkQuad(spec) {
    var P = quadPoints(spec); if (!P) return { ok: false, msg: 'unknown quadrilateral shape' };
    var bad = null;
    function seg(s) { return typeof s === 'string' && s.length === 2 && !!P[s[0]] && !!P[s[1]] && s[0] !== s[1]; }
    function len(s) { return dist(P[s[0]], P[s[1]]); }
    function angleAt(v, a, b) { var d = Math.abs(norm(ang(P[v], P[a]) - ang(P[v], P[b]))); return d > 180 ? 360 - d : d; }
    (spec.ticks || []).forEach(function (g) {
      if (!g.segs || g.segs.length < 1 || !g.segs.every(seg)) { bad = 'bad tick segment'; return; }
      g.segs.forEach(function (s) { if (Math.abs(len(s) - len(g.segs[0])) > 1.5) bad = 'tick marks on ' + g.segs[0] + ' and ' + s + ', which are not equal in this figure'; });
    });
    Object.keys(spec.seg || {}).forEach(function (s) {
      if (!seg(s)) bad = 'bad segment label ' + s;
      else if (/E/.test(s) && !spec.diagonals) bad = 'segment ' + s + ' needs the diagonals drawn';
      else if (s === 'MN' && !spec.mid) bad = 'MN needs the midsegment drawn';
    });
    Object.keys(spec.angle || {}).forEach(function (k) { if (!NEIGH[k] && !(spec.angleBetween && spec.angleBetween[k])) bad = 'bad angle label vertex'; });
    var byN = {};
    (spec.arcs || []).forEach(function (a) {
      var nb = a.between || NEIGH[a.v]; if (!nb) { bad = 'bad arc vertex'; return; }
      var m = angleAt(a.v, nb[0], nb[1]), n = a.n || 1;
      if (byN[n] !== undefined && Math.abs(byN[n] - m) > 0.8) bad = 'angle arcs marked alike are not equal in this figure';
      byN[n] = m;
    });
    (spec.right || []).forEach(function (r) {
      if (!r.every(function (x) { return !!P[x]; })) { bad = 'bad right angle'; return; }
      if (Math.abs(angleAt(r[0], r[1], r[2]) - 90) > 0.8) bad = 'right-angle mark at ' + r[0] + ' but the angle is not 90 degrees in this figure';
    });
    (spec.parallel || []).forEach(function (g) {
      if (!seg(g[0]) || !seg(g[1])) { bad = 'bad parallel marks'; return; }
      var a = ang(P[g[0][0]], P[g[0][1]]), b = ang(P[g[1][0]], P[g[1][1]]), d = Math.abs(norm(a - b)); d = Math.min(d, Math.abs(d - 180), Math.abs(d - 360));
      if (d > 0.8) bad = g[0] + ' and ' + g[1] + ' are marked parallel but are not parallel in this figure';
    });
    return bad ? { ok: false, msg: bad } : { ok: true };
  }

  /* =====================================================================
     2b. Regular polygon with one exterior angle marked
     spec: { kind:'geo-regular', n:3..24, label:'x°' }
     ===================================================================== */
  function regular(spec) {
    var n = spec.n, R = 58, cx = 215, cy = 88, V = [], i, h = '';
    for (i = 0; i < n; i++) { var d = dir(90 + 360 * i / n); V.push([cx + R * d[0], cy + R * d[1]]); }
    for (i = 0; i < n; i++) { h += L(V[i], V[(i + 1) % n]) + (n <= 12 ? ticks(V[i], V[(i + 1) % n], 1) : ''); }
    if (spec.plain) { for (i = 0; i < n; i++) h += dot(V[i], 3); return wrap(h, 160, 'A regular polygon', 'Regular polygon: all sides and angles are equal.'); }
    var v = V[0], prev = V[n - 1], ex = ang(prev, v), ext = [v[0] + 40 * dir(ex)[0], v[1] + 40 * dir(ex)[1]];
    h += L(v, ext, 2.2, true) + dot(v, 3);
    var side = ang(v, V[1]), w = shortWedge(ex, side);
    h += arcPath(v, w[0], w[1], 18, 1.6);
    var q = placeInWedge(v, w[0], w[1], spec.label, [w[0], w[1]], []);
    h += TL(q, spec.label);
    return wrap(h, 160, 'A regular polygon with ' + n + ' sides and one exterior angle marked', 'Regular polygon: all sides and angles are equal. Not drawn to scale.');
  }
  function checkRegular(spec) {
    return (Number.isInteger(spec.n) && spec.n >= 3 && spec.n <= 24 && (spec.label || spec.plain)) ? { ok: true } : { ok: false, msg: 'regular polygon needs 3 to 24 sides and a label' };
  }

  /* =====================================================================
     3. Circles
     spec: { kind:'geo-circle', pts:{ A:[x,y] ... } (unit circle coordinates, y up, centre O at 0,0),
             onCircle:['A','B'] (names that must lie on the circle), showCenter:bool,
             segs:[{p,q,label,tick,dash,side}], arcs:[{p,q,label,major,bold}], angles:[{v,a,b,label}],
             right:[['P','O','T']], labels:{ T:{dx,dy} }, hide:['X'] (points drawn without dot/label),
             note:'...' (override note), exact:bool }
     ===================================================================== */
  var CX = 215, CY = 99, S = 66;
  function C2P(p) { return [CX + S * p[0], CY - S * p[1]]; }
  F.on = function (deg) { return [Math.cos(rad(deg)), Math.sin(rad(deg))]; };
  function circlePoints(spec) {
    var P = { O: [0, 0] }, k; for (k in (spec.pts || {})) P[k] = spec.pts[k]; return P;
  }
  function circle(spec) {
    var P = circlePoints(spec), Q = {}, h = '', k, used = [], lines = [], i;
    for (k in P) Q[k] = C2P(P[k]);
    h = '<circle cx="' + CX + '" cy="' + CY + '" r="' + S + '" fill="none" stroke="' + INK + '" stroke-width="2.4"/>';
    for (i = 0; i < 36; i++) lines.push([[CX + S * Math.cos(rad(i * 10)), CY - S * Math.sin(rad(i * 10))], [CX + S * Math.cos(rad(i * 10 + 10)), CY - S * Math.sin(rad(i * 10 + 10))]]);
    (spec.arcs || []).forEach(function (a) {
      var pa = ang(Q.O, Q[a.p]), pb = ang(Q.O, Q[a.q]), w = shortWedge(pa, pb);
      if (a.major) w = [w[1], w[0]];
      var span = norm(w[1] - w[0]), m = w[0] + span / 2, lp = dir(m);
      h += arcPath(Q.O, w[0], w[1], S, a.bold === false ? 2.4 : 5);
      if (a.label) { var t = [CX + (S + 17 + textW(a.label) / 2 * Math.abs(lp[0])) * lp[0], CY + (S + 14) * lp[1]]; h += TL(t, a.label); used.push(boxOf(t[0], t[1], a.label)); }
    });
    (spec.segs || []).forEach(function (sg) {
      h += L(Q[sg.p], Q[sg.q], sg.w || 2.2, sg.dash); lines.push([Q[sg.p], Q[sg.q]]);
      if (sg.tick) h += ticks(Q[sg.p], Q[sg.q], sg.tick);
    });
    (spec.right || []).forEach(function (r) { var v = Q[r[0]]; h += rightMark(v, ang(v, Q[r[1]]), ang(v, Q[r[2]]), 9); });
    // points: dots and letters
    var hidden = {}; (spec.hide || []).forEach(function (x) { hidden[x] = 1; });
    Object.keys(Q).forEach(function (n) {
      if (hidden[n] || (n === 'O' && !spec.showCenter)) return;
      var p = Q[n], d = [p[0] - CX, p[1] - CY], len = Math.hypot(d[0], d[1]), o = (spec.labels && spec.labels[n]) || {}, lab;
      if (len < 3) lab = [p[0] + 10, p[1] + 14]; else if (len < S - 3) lab = [p[0] + 12, p[1] - 10]; else lab = [p[0] + 15 * d[0] / len, p[1] + 15 * d[1] / len];
      lab = [lab[0] + (o.dx || 0), lab[1] + (o.dy || 0)];
      h += dot(p, 3) + TL(lab, n); used.push(boxOf(lab[0], lab[1], n));
    });
    // free text (unit coordinates)
    (spec.texts || []).forEach(function (t) { var p = C2P(t.at); h += TL(p, t.text); used.push(boxOf(p[0], p[1], t.text)); });
    // dimension lines: a bracket parallel to p->q, offset to one side, carrying a label
    (spec.dims || []).forEach(function (d) {
      var p = Q[d.p], q = Q[d.q], a = ang(p, q), n = dir(a + 90 * (d.side || 1)), off = d.off || 22, p2 = [p[0] + n[0] * off, p[1] + n[1] * off], q2 = [q[0] + n[0] * off, q[1] + n[1] * off];
      h += L(p, p2, 0.8, true) + L(q, q2, 0.8, true) + L(p2, q2, 1.3);
      var m = [(p2[0] + q2[0]) / 2 + n[0] * (9 + Math.abs(n[0]) * textW(d.label) / 2), (p2[1] + q2[1]) / 2 + n[1] * (9 + Math.abs(n[0]) * 0 + 4)];
      h += TL(m, d.label); used.push(boxOf(m[0], m[1], d.label));
    });
    // segment labels avoid every drawn line, the circle and earlier labels
    (spec.segs || []).forEach(function (sg) {
      if (!sg.label) return;
      var pos = placeBeside(Q[sg.p], Q[sg.q], sg.label, { t: sg.t, side: sg.side || 1, lines: lines, used: used, H: 200 });
      h += T(pos.x, pos.y, sg.label);
    });
    (spec.angles || []).forEach(function (a) {
      var v = Q[a.v], w = shortWedge(ang(v, Q[a.a]), ang(v, Q[a.b]));
      h += arcPath(v, w[0], w[1], 15, 1.6);
      if (a.label) { var pos = placeInWedge(v, w[0], w[1], a.label, [w[0], w[1]], used); h += TL(pos, a.label); }
    });
    var lo = CX - S, hi = CX + S;
    Object.keys(Q).forEach(function (n) { lo = Math.min(lo, Q[n][0]); hi = Math.max(hi, Q[n][0]); });
    (spec.texts || []).forEach(function (t) { var p = C2P(t.at); lo = Math.min(lo, p[0] - textW(t.text) / 2); hi = Math.max(hi, p[0] + textW(t.text) / 2); });
    lo -= 64; hi += 64; if (hi - lo < 300) { var mid = (lo + hi) / 2; lo = mid - 150; hi = mid + 150; }
    return wrap(h, 200, spec.alt || 'Circle with labelled points and segments', spec.note === undefined ? (spec.exact ? '' : 'Not drawn to scale.') : spec.note, lo, hi - lo);
  }

  /* ---------- builders for the circle skills (all geometry computed exactly) ---------- */
  function lineHits(P, u) {   // intersections of the line P + t u with the unit circle: [near, far] points
    var b = P[0] * u[0] + P[1] * u[1], c = P[0] * P[0] + P[1] * P[1] - 1, d = b * b - c; if (d <= 0) return null;
    var t1 = -b - Math.sqrt(d), t2 = -b + Math.sqrt(d);
    return [[P[0] + t1 * u[0], P[1] + t1 * u[1]], [P[0] + t2 * u[0], P[1] + t2 * u[1]]];
  }
  function mathDir(d) { return [Math.cos(rad(d)), Math.sin(rad(d))]; }
  var CIRC = F.circ = {
    central: function (angDeg, angText, arcText) {
      return { kind: 'geo-circle', exact: true, showCenter: true, pts: { A: F.on(-angDeg / 2), B: F.on(angDeg / 2) }, onCircle: ['A', 'B'], labels: { O: { dx: -22, dy: 2 } }, segs: [{ p: 'O', q: 'A' }, { p: 'O', q: 'B' }], arcs: [{ p: 'A', q: 'B', label: arcText }], angles: [{ v: 'O', a: 'A', b: 'B', label: angText }], alt: 'Circle with a central angle and its intercepted arc' };
    },
    inscribed: function (arcDeg, angText, arcText) {
      return { kind: 'geo-circle', exact: true, pts: { A: F.on(-arcDeg / 2), B: F.on(arcDeg / 2), P: F.on(180) }, onCircle: ['A', 'B', 'P'], segs: [{ p: 'P', q: 'A' }, { p: 'P', q: 'B' }], arcs: [{ p: 'A', q: 'B', label: arcText }], angles: [{ v: 'P', a: 'A', b: 'B', label: angText }], alt: 'Circle with an inscribed angle and its intercepted arc' };
    },
    tangentRadius: function (aDeg, aText, xText) {
      var T0 = [0, 1], q = mathDir(270 + aDeg);
      return { kind: 'geo-circle', exact: true, showCenter: true, pts: { T: T0, R: [1.7, 1], L: [-1.7, 1], Q: [T0[0] + 1.5 * q[0], T0[1] + 1.5 * q[1]] }, onCircle: ['T'], hide: ['R', 'L', 'Q'], segs: [{ p: 'L', q: 'R' }, { p: 'O', q: 'T' }, { p: 'T', q: 'Q' }], right: [], angles: [{ v: 'T', a: 'O', b: 'Q', label: aText }, { v: 'T', a: 'Q', b: 'R', label: xText }], alt: 'Circle, radius OT and tangent at T with a ray between them' };
    },
    diameter: function (radText, diaText, givenRadius) {
      var segs = givenRadius
        ? [{ p: 'A', q: 'B', label: diaText, side: -1, t: 0.5 }, { p: 'O', q: 'A', label: radText, side: 1, t: 0.5 }]
        : [{ p: 'A', q: 'B', label: diaText, side: 1, t: 0.5 }, { p: 'O', q: 'B', label: radText, side: -1, t: 0.5 }];
      return { kind: 'geo-circle', showCenter: true, pts: { A: [-1, 0], B: [1, 0] }, onCircle: ['A', 'B'], segs: segs, alt: 'Circle with a diameter and a radius' };
    },
    semicircle: function (aDeg, aText, xText) {
      return { kind: 'geo-circle', exact: true, pts: { A: [-1, 0], B: [1, 0], C: F.on(2 * aDeg) }, onCircle: ['A', 'B', 'C'], segs: [{ p: 'A', q: 'B' }, { p: 'A', q: 'C' }, { p: 'B', q: 'C' }], right: [['C', 'A', 'B']], angles: [{ v: 'A', a: 'B', b: 'C', label: aText }, { v: 'B', a: 'A', b: 'C', label: xText }], alt: 'Triangle ABC inscribed in a circle with AB a diameter' };
    },
    chords: function (lab) {   // lab: {PA,PB,PC,PD}
      var A = F.on(200), B = F.on(30), C = F.on(125), D = F.on(300), d = (A[0] - B[0]) * (C[1] - D[1]) - (A[1] - B[1]) * (C[0] - D[0]);
      var a1 = A[0] * B[1] - A[1] * B[0], b1 = C[0] * D[1] - C[1] * D[0], Pp = [(a1 * (C[0] - D[0]) - (A[0] - B[0]) * b1) / d, (a1 * (C[1] - D[1]) - (A[1] - B[1]) * b1) / d];
      return { kind: 'geo-circle', pts: { A: A, B: B, C: C, D: D, P: Pp }, onCircle: ['A', 'B', 'C', 'D'], segs: [{ p: 'P', q: 'A', label: lab.PA, t: 0.55 }, { p: 'P', q: 'B', label: lab.PB, t: 0.55 }, { p: 'P', q: 'C', label: lab.PC, t: 0.55 }, { p: 'P', q: 'D', label: lab.PD, t: 0.55 }], labels: { P: { dx: 10, dy: 0 } }, alt: 'Two chords intersecting inside a circle at P' };
    },
    secants: function (a) {   // a: {ext1, ext2, in1, in2, whole1, whole2} labels (text); whole* uses a dimension line
      var P = [-2.4, 0], u1 = mathDir(14), u2 = mathDir(-10), h1 = lineHits(P, u1), h2 = lineHits(P, u2);
      var spec = { kind: 'geo-circle', pts: { P: P, A: h1[0], B: h1[1], C: h2[0], D: h2[1] }, onCircle: ['A', 'B', 'C', 'D'], segs: [{ p: 'P', q: 'A', label: a.ext1, side: 1 }, { p: 'P', q: 'C', label: a.ext2, side: -1 }], dims: [], alt: 'Two secants from an exterior point P' };
      if (a.in1) spec.segs.push({ p: 'A', q: 'B', label: a.in1, side: 1 }); else spec.segs.push({ p: 'A', q: 'B' }), spec.dims.push({ p: 'P', q: 'B', label: a.whole1, side: 1, off: 20 });
      if (a.in2) spec.segs.push({ p: 'C', q: 'D', label: a.in2, side: -1 }); else spec.segs.push({ p: 'C', q: 'D' }), spec.dims.push({ p: 'P', q: 'D', label: a.whole2, side: -1, off: 20 });
      return spec;
    },
    tangentSecant: function (a) {   // a: {tan, ext, in? , whole?}
      var d = 2.3, P = [-d, 0], Tt = [-1 / d, Math.sqrt(1 - 1 / (d * d))], u = mathDir(-9), h1 = lineHits(P, u);
      var spec = { kind: 'geo-circle', showCenter: false, pts: { P: P, T: Tt, A: h1[0], B: h1[1] }, onCircle: ['T', 'A', 'B'], segs: [{ p: 'P', q: 'T', label: a.tan, side: -1 }, { p: 'P', q: 'A', label: a.ext, side: 1 }], dims: [], right: [], alt: 'A tangent and a secant from an exterior point P' };
      if (a.inside) spec.segs.push({ p: 'A', q: 'B', label: a.inside, side: 1 }); else spec.segs.push({ p: 'A', q: 'B' }), spec.dims.push({ p: 'P', q: 'B', label: a.whole, side: -1, off: 22 });
      return spec;
    },
    sector: function (angDeg, angText, radText, text, where) {   // text: arc length (where 'arc') or sector area (where 'inside')
      var spec = { kind: 'geo-circle', exact: true, showCenter: true, labels: { O: { dx: -22, dy: -12 } }, pts: { A: F.on(-angDeg / 2), B: F.on(angDeg / 2) }, onCircle: ['A', 'B'], segs: [{ p: 'O', q: 'A', label: radText, side: -1 }, { p: 'O', q: 'B' }], arcs: [{ p: 'A', q: 'B', label: where === 'arc' ? text : 'A = ' + text }], angles: [{ v: 'O', a: 'A', b: 'B', label: angText }], texts: [], alt: 'Circle with a sector' };
      return spec;
    },
    chordDistance: function (ratio, radText, distText, chordText) {   // ratio = distance / radius (true proportions)
      var hh = Math.sqrt(1 - ratio * ratio), A = [-hh, -ratio], B = [hh, -ratio], M0 = [0, -ratio];
      return { kind: 'geo-circle', showCenter: true, pts: { A: A, B: B, M: M0, R: F.on(35) }, hide: ['M', 'R'], onCircle: ['A', 'B', 'R'], labels: { O: { dx: 12, dy: -4 } }, texts: [{ at: [0, ratio + 0.2 <= 0.78 ? -ratio - 0.2 : -1.24], text: chordText }, { at: [-(0.1 + 0.066 * String(distText).length), -ratio / 2 + 0.03], text: distText }], segs: [{ p: 'A', q: 'B' }, { p: 'O', q: 'M' }, { p: 'O', q: 'R', label: radText, side: 1 }], right: [['M', 'O', 'B']], alt: 'Circle with a chord and the perpendicular from the center' };
    }
  };

  function checkCircle(spec) {
    var P = circlePoints(spec), bad = null, tol = 1e-6;
    (spec.onCircle || []).forEach(function (n) { if (!P[n] || Math.abs(Math.hypot(P[n][0], P[n][1]) - 1) > tol) bad = n + ' is not on the circle'; });
    function has(n) { return !!P[n]; }
    (spec.segs || []).forEach(function (s) { if (!has(s.p) || !has(s.q) || s.p === s.q) bad = 'bad segment'; });
    (spec.arcs || []).forEach(function (a) { if (!has(a.p) || !has(a.q) || Math.abs(Math.hypot(P[a.p][0], P[a.p][1]) - 1) > tol || Math.abs(Math.hypot(P[a.q][0], P[a.q][1]) - 1) > tol) bad = 'arc endpoints must lie on the circle'; });
    (spec.angles || []).forEach(function (a) { if (!has(a.v) || !has(a.a) || !has(a.b)) bad = 'bad angle'; });
    (spec.right || []).forEach(function (r) {
      if (!r.every(has)) { bad = 'bad right angle'; return; }
      var v = P[r[0]], a = P[r[1]], b = P[r[2]], d = (a[0] - v[0]) * (b[0] - v[0]) + (a[1] - v[1]) * (b[1] - v[1]);
      if (Math.abs(d) > 1e-6) bad = 'right-angle mark at ' + r[0] + ' but the segments are not perpendicular';
    });
    // to-scale figures: a numeric angle or arc label must equal what is drawn
    if (spec.exact && !bad) {
      function drawn(v, a, b) { var d = Math.abs(norm(Math.atan2(P[a][1] - P[v][1], P[a][0] - P[v][0]) * 180 / Math.PI - Math.atan2(P[b][1] - P[v][1], P[b][0] - P[v][0]) * 180 / Math.PI)); return d > 180 ? 360 - d : d; }
      (spec.angles || []).forEach(function (a) { var m = /^(\d+)°$/.exec(a.label || ''); if (m && Math.abs(drawn(a.v, a.a, a.b) - Number(m[1])) > 0.6) bad = 'angle labelled ' + a.label + ' is drawn as ' + Math.round(drawn(a.v, a.a, a.b)) + '°'; });
      (spec.arcs || []).forEach(function (a) { var m = /^(\d+)°$/.exec(a.label || ''); if (m && Math.abs(drawn('O', a.p, a.q) - Number(m[1])) > 0.6) bad = 'arc labelled ' + a.label + ' is drawn as ' + Math.round(drawn('O', a.p, a.q)) + '°'; });
    }
    return bad ? { ok: false, msg: bad } : { ok: true };
  }

  /* ---------- public API ---------- */
  /* extension point: other files add figure kinds (geo-plane, geo-solid ...) with their own render/check */
  var EXT = {};
  F.extend = function (kind, impl) { EXT[kind] = impl; if (KINDS.indexOf(kind) < 0) KINDS.push(kind); };
  F.h = { wrap: wrap, T: T, L: L, dot: dot, rightMark: rightMark, esc: esc, r1: r1, textW: textW, W: W, INK: INK };
  F.owns = function (spec) { return !!spec && KINDS.indexOf(spec.kind) >= 0; };
  F.render = function (spec) {
    if (!F.owns(spec) || !F.check(spec).ok) return '';
    if (EXT[spec.kind]) return EXT[spec.kind].render(spec);
    return spec.kind === 'geo-transversal' ? transversal(spec) : spec.kind === 'geo-adjacent' ? adjacent(spec) : spec.kind === 'geo-cross' ? cross(spec) : spec.kind === 'geo-quad' ? quad(spec) : spec.kind === 'geo-regular' ? regular(spec) : circle(spec);
  };
  F.check = function (spec) {
    if (!F.owns(spec)) return { ok: false, msg: 'not a geometry figure' };
    if (EXT[spec.kind]) return EXT[spec.kind].check(spec);
    return spec.kind === 'geo-transversal' ? checkTransversal(spec) : spec.kind === 'geo-adjacent' ? checkAdjacent(spec) : spec.kind === 'geo-cross' ? checkCross(spec) : spec.kind === 'geo-quad' ? checkQuad(spec) : spec.kind === 'geo-regular' ? checkRegular(spec) : checkCircle(spec);
  };

  /* chain into the shared renderer and validator */
  var prior = NS.figHtml;
  NS.figHtml = function (spec) { return F.render(spec) || (prior ? prior(spec) : ''); };
  var D = NS.geoDiagram;
  if (D) { var pv = D.validate; D.validate = function (spec) { return F.owns(spec) ? F.check(spec).ok : (pv ? pv(spec) : false); }; }
})(typeof window !== 'undefined' ? window : globalThis);
