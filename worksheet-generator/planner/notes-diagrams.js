/* Daily Lesson Planner — teaching-notes diagrams and fill-in text (no DOM needed).

   MKPLAN.noteText(s, mode)     text with ⟨TeX⟩ math and {{blanks}} → HTML
   MKPLAN.diagram(spec, mode)   a small, exact SVG diagram → HTML (<figure>)
   mode: 'completed'  everything printed
         'guided'     every {{…}} becomes a blank to fill in (diagram labels become empty boxes)
         'key'        printed, with the parts that are blank on guided notes highlighted

   Diagram specs (all coordinates are math coordinates; y points up):
     nl     number line      {t:'nl', min, max, step, pts:[[x,'o'|'c',label]], seg:[[a,b]], ray:[[x,'<'|'>']], lab:[[x,text]]}
     plane  coordinate plane {t:'plane', x:[lo,hi], y:[lo,hi], fns:[{f:'2*x+1', dash, lab, at:[x,y], dom:[a,b], color}],
                              par:[{p:'[cos(t),sin(t)]', t:[a,b]}], pts:[[x,y,label,'o']], segs:[[x1,y1,x2,y2,dash]],
                              shade:[{f, side:'>'|'<'}], vl:[[x,dash,label]], hl:[[y,dash,label]], polys:[[[x,y],…]], txt:[[x,y,text]],
                              step (grid step, default 1), nums:false}
     geo    figure           {t:'geo', P:{A:[x,y],…}, seg:['AB','CD:dash'], line:['AB'], ray:['AB'], poly:[['A','B','C']],
                              circ:[['O',r]], ang:[['A','B','C',label,n]], right:[['A','B','C']], tick:[['A','B',n]], par:[['A','B',n]],
                              slab:[['A','B',label,side]], txt:[[x,y,text]], fill:[['A','B','C',color]], hide:['X'], w}
     area   area model       {t:'area', top:['x','3'], side:['x','2'], cells:[['x²','3x'],['2x','6']]}
     chain  operation chain  {t:'chain', nodes:['x','3x','3x + 5'], ops:['× 3','+ 5'], back:['÷ 3','− 5']}
     tbl    table            {t:'tbl', head:['x','y'], rows:[[…]], ...}
     box    box plot         {t:'box', v:[min,q1,med,q3,max], axis:[lo,hi,step]}
     dot    dot plot         {t:'dot', data:[…], axis:[lo,hi,step]}
     hist   histogram        {t:'hist', bins:[[lo,hi,count],…], ymax}
   Every spec may carry cap (caption, may hold ⟨math⟩ and {{blanks}}) and w (width in px). */
(function (G) {
  'use strict';
  var P = (G.MKPLAN = G.MKPLAN || {});
  var INK = '#111', BLUE = '#1f5fbf', ORANGE = '#c0561b', GREEN = '#2f7a50', SOFT = '#dce8fb', GRID = '#d6d6d6', KEYC = '#0b6e6e';
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function ms(s) { return G.MKMENU && G.MKMENU.mathSafe ? G.MKMENU.mathSafe(s) : esc(String(s).replace(/[⟨⟩]/g, '')); }
  function r2(n) { return Math.round(n * 100) / 100; }

  /* ---------- text with blanks ---------- */
  function blankWidth(inner) { var t = String(inner).replace(/⟨|⟩|\\[a-z]+|[{}^_]/g, ''); return Math.max(3.2, Math.min(16, t.length * 0.62 + 1.6)); }
  /* Split into text, ⟨math⟩ and {{blank}} pieces. A blank ends at the first "}}" that is not closing one of its own
     braces, so {{\frac{P-2w}{2}}} is one blank; a blank may hold math, and math may hold blanks. */
  function closeBlank(s, i) {   // i = index just after "{{"; returns the index of the closing "}}"
    var depth = 0;
    for (var k = i; k < s.length; k++) {
      var ch = s.charAt(k);
      if (ch === '\\') { k++; continue; }
      if (ch === '{') depth++;
      else if (ch === '}') { if (depth > 0) depth--; else if (s.charAt(k + 1) === '}') return k; }
    }
    return -1;
  }
  function tokens(s) {
    var out = [], buf = '', i = 0;
    function flush() { if (buf) out.push({ k: 'text', v: buf }); buf = ''; }
    while (i < s.length) {
      if (s.charAt(i) === '{' && s.charAt(i + 1) === '{') { var e = closeBlank(s, i + 2); if (e > 0) { flush(); out.push({ k: 'blank', v: s.slice(i + 2, e) }); i = e + 2; continue; } }
      if (s.charAt(i) === '⟨') { var m = s.indexOf('⟩', i + 1); if (m > 0) { flush(); out.push({ k: 'math', v: s.slice(i + 1, m) }); i = m + 1; continue; } }
      buf += s.charAt(i); i++;
    }
    flush(); return out;
  }
  function mathWithBlanks(tex, mode) {
    var out = '', i = 0;
    while (i < tex.length) {
      if (tex.charAt(i) === '{' && tex.charAt(i + 1) === '{') {
        var e = closeBlank(tex, i + 2);
        if (e > 0) {
          var inner = tex.slice(i + 2, e);
          out += mode === 'plain-guided' ? '{\\text{____}}' : mode === 'guided' ? '{\\underline{\\hspace{' + blankWidth(inner).toFixed(1) + 'em}}}' : mode === 'key' ? '{\\textcolor{#0b6e6e}{' + inner + '}}' : '{' + inner + '}';
          i = e + 2; continue;
        }
      }
      out += tex.charAt(i); i++;
    }
    return out;
  }
  P.noteText = function (s, mode) {
    s = String(s === undefined || s === null ? '' : s);
    return tokens(s).map(function (t) {
      if (t.k === 'text') return esc(t.v);
      if (t.k === 'math') return ms('⟨' + mathWithBlanks(t.v, mode) + '⟩');
      if (mode === 'guided') return '<span class="nt-blank" style="min-width:' + blankWidth(t.v).toFixed(1) + 'em" aria-label="blank"></span>';
      return '<span class="nt-fill' + (mode === 'key' ? ' key' : '') + '">' + ms(t.v) + '</span>';
    }).join('');
  };
  P.plainNoteText = function (s, mode) {   // for slides: no HTML; guided blanks become ______
    return tokens(String(s || '')).map(function (t) {
      if (t.k === 'text') return t.v;
      if (t.k === 'math') return '⟨' + mathWithBlanks(t.v, mode === 'guided' ? 'plain-guided' : 'completed').replace(/\{\{[\s\S]*?\}\}/g, '') + '⟩';
      return mode === 'guided' ? '________' : t.v;
    }).join('');
  };
  P.hasBlanks = function (s) { return /\{\{[\s\S]*?\}\}/.test(String(s || '')); };

  /* ---------- SVG helpers ---------- */
  function svgOpen(w, h, label) { return '<svg class="nt-svg" viewBox="0 0 ' + r2(w) + ' ' + r2(h) + '" width="' + r2(w) + '" role="img" aria-label="' + esc(label || 'diagram') + '" font-family="Inter, Arial, sans-serif">'; }
  function line(x1, y1, x2, y2, o) { o = o || {}; return '<line x1="' + r2(x1) + '" y1="' + r2(y1) + '" x2="' + r2(x2) + '" y2="' + r2(y2) + '" stroke="' + (o.c || INK) + '" stroke-width="' + (o.w || 1.4) + '"' + (o.dash ? ' stroke-dasharray="5 4"' : '') + (o.cap ? ' stroke-linecap="round"' : '') + '/>'; }
  /* A label; {{x}} in the text is a blank on guided notes (an empty box of the same size keeps the figure readable). */
  function label(x, y, s, mode, o) {
    o = o || {}; s = String(s); var m = /^\{\{([\s\S]*)\}\}$/.exec(s), size = o.size || 12, anchor = o.anchor || 'middle';
    var txt = m ? m[1] : s, w = Math.max(14, txt.length * size * 0.56 + 6);
    if (m && mode === 'guided') {
      var bx = anchor === 'start' ? x - 2 : anchor === 'end' ? x - w + 2 : x - w / 2;
      return '<rect x="' + r2(bx) + '" y="' + r2(y - size + 1) + '" width="' + r2(w) + '" height="' + r2(size + 5) + '" fill="#fff" stroke="' + INK + '" stroke-width="0.9" rx="2"/>';
    }
    var color = m && mode === 'key' ? KEYC : (o.c || INK);
    var halo = o.halo === false ? '' : ' paint-order="stroke" stroke="#fff" stroke-width="3" stroke-linejoin="round"';
    return '<text x="' + r2(x) + '" y="' + r2(y) + '" font-size="' + size + '" text-anchor="' + anchor + '" fill="' + color + '"' + (o.bold || (m && mode === 'key') ? ' font-weight="700"' : '') + (o.italic ? ' font-style="italic"' : '') + halo + '>' + esc(txt) + '</text>';
  }
  function arrowHead(x, y, ang, c, s) { s = s || 7; var a1 = ang + Math.PI * 0.85, a2 = ang - Math.PI * 0.85; return '<path d="M' + r2(x) + ' ' + r2(y) + ' L' + r2(x + s * Math.cos(a1)) + ' ' + r2(y + s * Math.sin(a1)) + ' L' + r2(x + s * Math.cos(a2)) + ' ' + r2(y + s * Math.sin(a2)) + ' Z" fill="' + (c || INK) + '"/>'; }
  function fmtNum(n) { n = Math.round(n * 1000) / 1000; return n < 0 ? '−' + Math.abs(n) : String(n); }

  /* ---------- number line ---------- */
  function numberLine(s, mode) {
    var W = s.w || 330, H = 58, pad = 18, min = s.min, max = s.max, step = s.step || 1, n = Math.round((max - min) / step);
    function X(v) { return pad + (v - min) / (max - min) * (W - 2 * pad); }
    var y = 28, out = svgOpen(W, H + (s.lab ? 14 : 0), 'number line');
    out += line(4, y, W - 4, y) + arrowHead(W - 2, y, 0) + arrowHead(2, y, Math.PI);
    var every = n > 16 ? 2 : 1;
    for (var i = 0; i <= n; i++) { var v = min + i * step, x = X(v); out += line(x, y - 5, x, y + 5); if (i % every === 0) out += label(x, y + 19, fmtNum(v), mode, { size: 10 }); }
    (s.seg || []).forEach(function (g) { out += line(X(g[0]), y, X(g[1]), y, { c: BLUE, w: 4.5 }); });
    (s.ray || []).forEach(function (g) { var x = X(g[0]), end = g[1] === '<' ? 6 : W - 6; out += line(x, y, end, y, { c: BLUE, w: 4.5 }) + arrowHead(g[1] === '<' ? 3 : W - 3, y, g[1] === '<' ? Math.PI : 0, BLUE, 9); });
    (s.pts || []).forEach(function (p) {
      var x = X(p[0]);
      out += '<circle cx="' + r2(x) + '" cy="' + y + '" r="5" fill="' + (p[1] === 'o' ? '#fff' : BLUE) + '" stroke="' + BLUE + '" stroke-width="2"/>';
      if (p[2]) out += label(x, y - 10, p[2], mode, { size: 11, bold: true, c: BLUE });
    });
    (s.lab || []).forEach(function (l) { out += label(X(l[0]), H + 8, l[1], mode, { size: 11, c: ORANGE, bold: true }); });
    return out + '</svg>';
  }

  /* ---------- coordinate plane ---------- */
  var MATHFN = 'var sqrt=Math.sqrt,abs=Math.abs,sin=Math.sin,cos=Math.cos,tan=Math.tan,PI=Math.PI,log=Math.log,ln=Math.log,log10=Math.log10,log2=Math.log2,exp=Math.exp,pow=Math.pow,cbrt=Math.cbrt,floor=Math.floor,E=Math.E;';
  function fn(src, v) { return new Function(v || 'x', MATHFN + 'return (' + src + ');'); }   // diagram specs are authored in this repository only
  function plane(s, mode) {
    var xr = s.x || [-6, 6], yr = s.y || [-6, 6], st = s.step || 1, sy = s.ystep || st, W = s.w || 230;
    var ylab = s.nums === false ? 1 : Math.max(String(Math.round(Math.abs(yr[0]))).length + (yr[0] < 0 ? 1 : 0), String(Math.round(Math.abs(yr[1]))).length), ox = Math.max(19, 6 + ylab * 5.6);
    var sc = (W - ox - 15) / (xr[1] - xr[0]), scy = Math.min(sc, (s.maxH || W * 1.05) / (yr[1] - yr[0])), H = (yr[1] - yr[0]) * scy + 30, oy = 15;
    function X(v) { return ox + (v - xr[0]) * sc; } function Y(v) { return oy + (yr[1] - v) * scy; }
    var out = svgOpen(W, H, 'coordinate plane'), i;
    out += '<defs><clipPath id="ntc' + (plane.n = (plane.n || 0) + 1) + '"><rect x="' + ox + '" y="' + oy + '" width="' + r2((xr[1] - xr[0]) * sc) + '" height="' + r2((yr[1] - yr[0]) * scy) + '"/></clipPath></defs>';
    var clip = ' clip-path="url(#ntc' + plane.n + ')"';
    if (s.grid !== false) {
      for (i = Math.ceil(xr[0] / st) * st; i <= xr[1] + 1e-9; i += st) out += line(X(i), Y(yr[0]), X(i), Y(yr[1]), { c: GRID, w: 0.7 });
      for (i = Math.ceil(yr[0] / sy) * sy; i <= yr[1] + 1e-9; i += sy) out += line(X(xr[0]), Y(i), X(xr[1]), Y(i), { c: GRID, w: 0.7 });
    }
    // shading for inequalities (drawn under everything)
    (s.shade || []).forEach(function (sh) {
      var f = fn(sh.f), pts = [], k, N = 120;
      for (k = 0; k <= N; k++) { var x = xr[0] + (xr[1] - xr[0]) * k / N; pts.push([x, f(x)]); }
      var edge = sh.side === '>' ? yr[1] + 50 : yr[0] - 50;
      var d = 'M' + r2(X(xr[0])) + ' ' + r2(Y(edge)) + pts.map(function (p) { return ' L' + r2(X(p[0])) + ' ' + r2(Y(Math.max(yr[0] - 50, Math.min(yr[1] + 50, p[1])))); }).join('') + ' L' + r2(X(xr[1])) + ' ' + r2(Y(edge)) + ' Z';
      out += '<path d="' + d + '" fill="' + (sh.color || SOFT) + '" fill-opacity="' + (sh.op || 0.75) + '"' + clip + '/>';
    });
    (s.region || []).forEach(function (poly) { out += '<path d="' + poly.map(function (p, j) { return (j ? 'L' : 'M') + r2(X(p[0])) + ' ' + r2(Y(p[1])); }).join(' ') + ' Z" fill="' + SOFT + '" fill-opacity="0.8"' + clip + '/>'; });
    // axes
    if (yr[0] <= 0 && yr[1] >= 0) out += line(X(xr[0]) - 4, Y(0), X(xr[1]) + 6, Y(0), { w: 1.3 }) + arrowHead(X(xr[1]) + 8, Y(0), 0, INK, 6) + label(X(xr[1]) + 8, Y(0) - 7, s.xl || 'x', mode, { size: 11, italic: true, anchor: 'end' });
    if (xr[0] <= 0 && xr[1] >= 0) out += line(X(0), Y(yr[0]) + 4, X(0), Y(yr[1]) - 6, { w: 1.3 }) + arrowHead(X(0), Y(yr[1]) - 8, -Math.PI / 2, INK, 6) + label(X(0) + 9, Y(yr[1]) - 1, s.yl || 'y', mode, { size: 11, italic: true, anchor: 'start' });
    if (s.nums !== false) {
      var nx = s.numEvery || (xr[1] - xr[0] > 12 ? 2 : 1), ny = s.numEveryY || nx;
      for (i = Math.ceil(xr[0] / st) * st; i <= xr[1] + 1e-9; i += st) if (Math.abs(i) > 1e-9 && Math.round(i / st) % nx === 0) out += label(X(i), Y(Math.max(yr[0], Math.min(yr[1], 0))) + 12, fmtNum(i), mode, { size: 8.5 });
      for (i = Math.ceil(yr[0] / sy) * sy; i <= yr[1] + 1e-9; i += sy) if (Math.abs(i) > 1e-9 && Math.round(i / sy) % ny === 0) out += label(X(Math.max(xr[0], Math.min(xr[1], 0))) - 4, Y(i) + 3, fmtNum(i), mode, { size: 8.5, anchor: 'end' });
    }
    (s.vl || []).forEach(function (v) { out += line(X(v[0]), Y(yr[0]), X(v[0]), Y(yr[1]), { c: v[3] || ORANGE, w: 1.5, dash: v[1] !== false }); if (v[2]) out += label(X(v[0]) + 4, oy + 12, v[2], mode, { size: 10.5, anchor: 'start', c: v[3] || ORANGE, bold: true }); });
    (s.hl || []).forEach(function (v) { out += line(X(xr[0]), Y(v[0]), X(xr[1]), Y(v[0]), { c: v[3] || ORANGE, w: 1.5, dash: v[1] !== false }); if (v[2]) out += label(X(xr[1]) - 4, Y(v[0]) - 5, v[2], mode, { size: 10.5, anchor: 'end', c: v[3] || ORANGE, bold: true }); });
    (s.polys || []).forEach(function (pl) { var pts = pl.pts || pl; out += '<path d="' + pts.map(function (p, j) { return (j ? 'L' : 'M') + r2(X(p[0])) + ' ' + r2(Y(p[1])); }).join(' ') + ' Z" fill="' + (pl.fill || 'rgba(31,95,191,.14)') + '" stroke="' + (pl.c || BLUE) + '" stroke-width="1.8"' + (pl.dash ? ' stroke-dasharray="5 4"' : '') + '/>'; });
    function curve(pts, o) {
      var d = '', pen = false, prev = null, span = (yr[1] - yr[0]);
      pts.forEach(function (p) {
        var ok = isFinite(p[1]) && isFinite(p[0]) && p[1] > yr[0] - span && p[1] < yr[1] + span;
        if (ok && prev && Math.abs(p[1] - prev[1]) > span * 0.9) ok = 'break';
        if (ok === true) { d += (pen ? ' L' : ' M') + r2(X(p[0])) + ' ' + r2(Y(p[1])); pen = true; }
        else if (ok === 'break') { d += ' M' + r2(X(p[0])) + ' ' + r2(Y(p[1])); pen = true; }
        else pen = false;
        prev = isFinite(p[1]) ? p : null;
      });
      return '<path d="' + d + '" fill="none" stroke="' + (o.color || BLUE) + '" stroke-width="2.2"' + (o.dash ? ' stroke-dasharray="6 4"' : '') + ' stroke-linejoin="round"' + clip + '/>';
    }
    (s.fns || []).forEach(function (o) {
      var f = fn(o.f), dom = o.dom || xr, N = 480, pts = [];
      for (var k = 0; k <= N; k++) { var x = dom[0] + (dom[1] - dom[0]) * k / N; var yv; try { yv = f(x); } catch (e) { yv = NaN; } pts.push([x, yv]); }
      out += curve(pts, o);
      if (o.lab) { var at = o.at || [dom[1] - (dom[1] - dom[0]) * 0.12, f(dom[1] - (dom[1] - dom[0]) * 0.12)]; out += label(X(at[0]), Y(at[1]) - 6, o.lab, mode, { size: 10.5, c: o.color || BLUE, bold: true, anchor: o.anchor || 'middle' }); }
    });
    (s.par || []).forEach(function (o) {
      var f = fn(o.p, 't'), N = 360, pts = [];
      for (var k = 0; k <= N; k++) { var t = o.t[0] + (o.t[1] - o.t[0]) * k / N, q = f(t); pts.push(q); }
      out += curve(pts, o);
      if (o.lab && o.at) out += label(X(o.at[0]), Y(o.at[1]), o.lab, mode, { size: 10.5, c: o.color || BLUE, bold: true });
    });
    (s.segs || []).forEach(function (g) { out += line(X(g[0]), Y(g[1]), X(g[2]), Y(g[3]), { c: g[5] || ORANGE, w: 1.8, dash: !!g[4] }); });
    (s.vec || []).forEach(function (g) { var a = Math.atan2(Y(g[3]) - Y(g[1]), X(g[2]) - X(g[0])); out += line(X(g[0]), Y(g[1]), X(g[2]) - 6 * Math.cos(a), Y(g[3]) - 6 * Math.sin(a), { c: g[4] || ORANGE, w: 1.8 }) + arrowHead(X(g[2]), Y(g[3]), a, g[4] || ORANGE, 8); });
    (s.pts || []).forEach(function (p) {
      out += '<circle cx="' + r2(X(p[0])) + '" cy="' + r2(Y(p[1])) + '" r="3.6" fill="' + (p[3] === 'o' ? '#fff' : (p[4] || INK)) + '" stroke="' + (p[4] || INK) + '" stroke-width="1.6"/>';
      if (p[2]) { var dx = p[5] !== undefined ? p[5] : 6, dy = p[6] !== undefined ? p[6] : -7; out += label(X(p[0]) + dx, Y(p[1]) + dy, p[2], mode, { size: 10.5, anchor: dx < 0 ? 'end' : dx === 0 ? 'middle' : 'start', bold: true }); }
    });
    (s.txt || []).forEach(function (t) { out += label(X(t[0]), Y(t[1]), t[2], mode, { size: t[3] || 10.5, c: t[4] || INK, bold: true, anchor: t[5] || 'middle' }); });
    return out + '</svg>';
  }

  /* ---------- geometry figure ---------- */
  function geo(s, mode) {
    var P0 = s.P || {}, names = Object.keys(P0), xs = [], ys = [];
    names.forEach(function (k) { xs.push(P0[k][0]); ys.push(P0[k][1]); });
    (s.circ || []).forEach(function (c) { var o = P0[c[0]], r = typeof c[1] === 'number' ? c[1] : dist(o, P0[c[1]]); xs.push(o[0] - r, o[0] + r); ys.push(o[1] - r, o[1] + r); });
    (s.ell || []).forEach(function (e) { var o = P0[e[0]]; xs.push(o[0] - e[1], o[0] + e[1]); ys.push(o[1] - e[2], o[1] + e[2]); });
    (s.txt || []).forEach(function (t) { xs.push(t[0]); ys.push(t[1]); });
    var minX = Math.min.apply(null, xs), maxX = Math.max.apply(null, xs), minY = Math.min.apply(null, ys), maxY = Math.max.apply(null, ys);
    var W = s.w || 240, pad = s.pad || 26, sc = (W - 2 * pad) / Math.max(1e-6, maxX - minX);
    if ((maxY - minY) * sc > (s.maxH || 210)) { sc = ((s.maxH || 210)) / (maxY - minY); }
    var H = (maxY - minY) * sc + 2 * pad, Wd = (maxX - minX) * sc + 2 * pad;
    function X(p) { return pad + (p[0] - minX) * sc; } function Y(p) { return pad + (maxY - p[1]) * sc; }
    function Q(n) { var p = P0[n]; if (!p) throw new Error('No point ' + n); return p; }
    var out = svgOpen(Wd, H, s.alt || 'geometry figure');
    (s.fill || []).forEach(function (f) { var pts = f.slice(0, -1); out += '<path d="' + pts.map(function (n, j) { return (j ? 'L' : 'M') + r2(X(Q(n))) + ' ' + r2(Y(Q(n))); }).join(' ') + ' Z" fill="' + f[f.length - 1] + '" stroke="none"/>'; });
    (s.circ || []).forEach(function (c) { var o = Q(c[0]), r = typeof c[1] === 'number' ? c[1] : dist(o, Q(c[1])); out += '<circle cx="' + r2(X(o)) + '" cy="' + r2(Y(o)) + '" r="' + r2(r * sc) + '" fill="' + (c[2] || 'none') + '" stroke="' + INK + '" stroke-width="1.5"' + (c[3] ? ' stroke-dasharray="5 4"' : '') + '/>'; });
    (s.ell || []).forEach(function (e) { var o = Q(e[0]); out += '<ellipse cx="' + r2(X(o)) + '" cy="' + r2(Y(o)) + '" rx="' + r2(e[1] * sc) + '" ry="' + r2(e[2] * sc) + '" fill="' + (e[4] || 'none') + '" stroke="' + INK + '" stroke-width="1.5"' + (e[3] ? ' stroke-dasharray="5 4"' : '') + '/>'; });
    (s.arc || []).forEach(function (a) {   // highlighted arc of a circle: [center, from, to, color] counter-clockwise from→to
      var o = Q(a[0]), p1 = Q(a[1]), p2 = Q(a[2]), r = dist(o, p1) * sc, t1 = Math.atan2(p1[1] - o[1], p1[0] - o[0]), t2 = Math.atan2(p2[1] - o[1], p2[0] - o[0]);
      var sweep = t2 - t1; while (sweep <= 0) sweep += 2 * Math.PI;
      out += '<path d="M' + r2(X(p1)) + ' ' + r2(Y(p1)) + ' A' + r2(r) + ' ' + r2(r) + ' 0 ' + (sweep > Math.PI ? 1 : 0) + ' 0 ' + r2(X(p2)) + ' ' + r2(Y(p2)) + '" fill="none" stroke="' + (a[3] || BLUE) + '" stroke-width="4" stroke-opacity=".75"/>';
    });
    (s.poly || []).forEach(function (pl) { var c = typeof pl[pl.length - 1] === 'string' && pl[pl.length - 1].charAt(0) === '#' ? pl[pl.length - 1] : null, pts = c ? pl.slice(0, -1) : pl; out += '<path d="' + pts.map(function (n, j) { return (j ? 'L' : 'M') + r2(X(Q(n))) + ' ' + r2(Y(Q(n))); }).join(' ') + ' Z" fill="' + (c || 'none') + '" fill-opacity="' + (c ? 0.18 : 0) + '" stroke="' + INK + '" stroke-width="1.6" stroke-linejoin="round"/>'; });
    function segParse(spec) { var m = String(spec).split(':'), ab = m[0]; var a, b; if (ab.indexOf(',') > 0) { var q = ab.split(','); a = q[0]; b = q[1]; } else { a = ab.charAt(0); b = ab.slice(1); } return { a: a, b: b, dash: /dash/.test(m[1] || ''), c: /blue/.test(m[1] || '') ? BLUE : /orange/.test(m[1] || '') ? ORANGE : /green/.test(m[1] || '') ? GREEN : INK, w: /bold/.test(m[1] || '') ? 3 : 1.6 }; }
    (s.seg || []).forEach(function (sp) { var g = segParse(sp); out += line(X(Q(g.a)), Y(Q(g.a)), X(Q(g.b)), Y(Q(g.b)), { c: g.c, w: g.w, dash: g.dash, cap: true }); });
    (s.line || []).forEach(function (sp) { var g = segParse(sp), a = Q(g.a), b = Q(g.b), dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy), e = 18 / sc; var p1 = [a[0] - dx / L * e, a[1] - dy / L * e], p2 = [b[0] + dx / L * e, b[1] + dy / L * e]; var ang = Math.atan2(Y(p2) - Y(p1), X(p2) - X(p1)); out += line(X(p1), Y(p1), X(p2), Y(p2), { c: g.c, w: g.w, dash: g.dash }) + arrowHead(X(p2), Y(p2), ang, g.c, 7) + arrowHead(X(p1), Y(p1), ang + Math.PI, g.c, 7); });
    (s.ray || []).forEach(function (sp) { var g = segParse(sp), a = Q(g.a), b = Q(g.b), dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy), e = 18 / sc; var p2 = [b[0] + dx / L * e, b[1] + dy / L * e], ang = Math.atan2(Y(p2) - Y(a), X(p2) - X(a)); out += line(X(a), Y(a), X(p2), Y(p2), { c: g.c, w: g.w, dash: g.dash }) + arrowHead(X(p2), Y(p2), ang, g.c, 7); });
    (s.right || []).forEach(function (r) { var a = Q(r[0]), b = Q(r[1]), c = Q(r[2]), k = 9; var u = unit([X(a) - X(b), Y(a) - Y(b)]), v = unit([X(c) - X(b), Y(c) - Y(b)]); var bx = X(b), by = Y(b); out += '<path d="M' + r2(bx + u[0] * k) + ' ' + r2(by + u[1] * k) + ' L' + r2(bx + u[0] * k + v[0] * k) + ' ' + r2(by + u[1] * k + v[1] * k) + ' L' + r2(bx + v[0] * k) + ' ' + r2(by + v[1] * k) + '" fill="none" stroke="' + INK + '" stroke-width="1.2"/>'; });
    (s.ang || []).forEach(function (a) {
      var A = Q(a[0]), B = Q(a[1]), C = Q(a[2]), n = a[4] || 1, col = a[5] || (n > 1 ? ORANGE : BLUE), bx = X(B), by = Y(B);
      var t1 = Math.atan2(Y(A) - by, X(A) - bx), t2 = Math.atan2(Y(C) - by, X(C) - bx), d = t2 - t1; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI;
      for (var k = 0; k < n; k++) { var rr = (a[6] || 16) + k * 4; out += '<path d="M' + r2(bx + rr * Math.cos(t1)) + ' ' + r2(by + rr * Math.sin(t1)) + ' A' + rr + ' ' + rr + ' 0 0 ' + (d > 0 ? 1 : 0) + ' ' + r2(bx + rr * Math.cos(t1 + d)) + ' ' + r2(by + rr * Math.sin(t1 + d)) + '" fill="none" stroke="' + col + '" stroke-width="1.6"/>'; }
      if (a[3]) { var mid = t1 + d / 2, lr = (a[6] || 16) + 4 * (n - 1) + (a[7] || 15); out += label(bx + lr * Math.cos(mid), by + lr * Math.sin(mid) + 4, a[3], mode, { size: 11, c: col, bold: true }); }
    });
    (s.tick || []).forEach(function (t) { var a = Q(t[0]), b = Q(t[1]), n = t[2] || 1, mx = (X(a) + X(b)) / 2, my = (Y(a) + Y(b)) / 2, u = unit([X(b) - X(a), Y(b) - Y(a)]), v = [-u[1], u[0]]; for (var k = 0; k < n; k++) { var off = (k - (n - 1) / 2) * 4; out += line(mx + u[0] * off - v[0] * 5, my + u[1] * off - v[1] * 5, mx + u[0] * off + v[0] * 5, my + u[1] * off + v[1] * 5, { w: 1.4 }); } });
    (s.par || []).forEach(function (t) { var a = Q(t[0]), b = Q(t[1]), n = t[2] || 1, mx = (X(a) + X(b)) / 2, my = (Y(a) + Y(b)) / 2, ang = Math.atan2(Y(b) - Y(a), X(b) - X(a)); for (var k = 0; k < n; k++) { var off = (k - (n - 1) / 2) * 6; out += '<path d="M' + r2(mx + Math.cos(ang) * off - 5 * Math.cos(ang) - 4 * Math.sin(ang)) + ' ' + r2(my + Math.sin(ang) * off - 5 * Math.sin(ang) + 4 * Math.cos(ang)) + ' L' + r2(mx + Math.cos(ang) * off) + ' ' + r2(my + Math.sin(ang) * off) + ' L' + r2(mx + Math.cos(ang) * off - 5 * Math.cos(ang) + 4 * Math.sin(ang)) + ' ' + r2(my + Math.sin(ang) * off - 5 * Math.sin(ang) - 4 * Math.cos(ang)) + '" fill="none" stroke="' + INK + '" stroke-width="1.4"/>'; } });
    (s.slab || []).forEach(function (t) { var a = Q(t[0]), b = Q(t[1]), mx = (X(a) + X(b)) / 2, my = (Y(a) + Y(b)) / 2, u = unit([X(b) - X(a), Y(b) - Y(a)]), v = [u[1], -u[0]], side = t[3] === undefined ? 1 : t[3], off = t[4] || 12; out += label(mx + v[0] * off * side, my + v[1] * off * side + 4, t[2], mode, { size: 11, bold: true, c: t[5] || INK }); });
    var hide = {}; (s.hide || []).forEach(function (n) { hide[n] = 1; });
    var cx = 0, cy = 0; names.forEach(function (n) { cx += P0[n][0]; cy += P0[n][1]; }); cx /= names.length || 1; cy /= names.length || 1;
    names.forEach(function (n) {
      if (hide[n] || n.charAt(0) === '_') return;
      var p = P0[n], off = s.loff && s.loff[n], dx, dy;
      if (off) { dx = off[0]; dy = off[1]; } else { var u = unit([p[0] - cx, -(p[1] - cy)]); if (!u[0] && !u[1]) u = [0, -1]; dx = u[0] * 12; dy = u[1] * 12 + 4; }
      if (s.dots !== false) out += '<circle cx="' + r2(X(p)) + '" cy="' + r2(Y(p)) + '" r="2.4" fill="' + INK + '"/>';
      out += label(X(p) + dx, Y(p) + dy, n.replace(/\d+$/, function (d) { return d; }), mode, { size: 12, bold: true, italic: false });
    });
    (s.txt || []).forEach(function (t) { out += label(X(t), Y(t), t[2], mode, { size: t[3] || 11, c: t[4] || INK, bold: true, anchor: t[5] || 'middle' }); });
    return out + '</svg>';
  }
  function dist(a, b) { return Math.hypot(a[0] - b[0], a[1] - b[1]); }
  function unit(v) { var L = Math.hypot(v[0], v[1]) || 1; return [v[0] / L, v[1] / L]; }

  /* ---------- area model ---------- */
  function area(s, mode) {
    var cw = s.cw || 64, ch = s.ch || 44, cols = s.top.length, rows = s.side.length, ox = 34, oy = 24, W = ox + cols * cw + 6, H = oy + rows * ch + 6;
    var out = svgOpen(W, H, 'area model');
    s.top.forEach(function (t, j) { out += label(ox + j * cw + cw / 2, 16, t, mode, { size: 12, bold: true, c: BLUE }); });
    s.side.forEach(function (t, i) { out += label(ox - 14, oy + i * ch + ch / 2 + 4, t, mode, { size: 12, bold: true, c: BLUE }); });
    for (var i = 0; i < rows; i++) for (var j = 0; j < cols; j++) {
      out += '<rect x="' + (ox + j * cw) + '" y="' + (oy + i * ch) + '" width="' + cw + '" height="' + ch + '" fill="' + ((i + j) % 2 ? '#fff' : '#f2f6ff') + '" stroke="' + INK + '" stroke-width="1.3"/>';
      out += label(ox + j * cw + cw / 2, oy + i * ch + ch / 2 + 4, s.cells[i][j], mode, { size: 12, bold: true });
    }
    return out + '</svg>';
  }
  /* ---------- operation chain (inverse operations, composition) ---------- */
  function chain(s, mode) {
    var n = s.nodes.length, bw = s.bw || 62, gap = s.gap || 58, W = n * bw + (n - 1) * gap + 8, H = s.back ? 92 : 50, y = 10, out = svgOpen(W, H, 'operation chain');
    s.nodes.forEach(function (t, i) { var x = 4 + i * (bw + gap); out += '<rect x="' + x + '" y="' + y + '" width="' + bw + '" height="28" rx="6" fill="#f2f6ff" stroke="' + INK + '" stroke-width="1.3"/>' + label(x + bw / 2, y + 19, t, mode, { size: 12, bold: true }); });
    (s.ops || []).forEach(function (t, i) { var x1 = 4 + i * (bw + gap) + bw + 3, x2 = x1 + gap - 6; out += line(x1, y + 14, x2 - 4, y + 14, { c: BLUE, w: 1.8 }) + arrowHead(x2, y + 14, 0, BLUE, 7) + label((x1 + x2) / 2, y + 8, t, mode, { size: 11, c: BLUE, bold: true }); });
    (s.back || []).forEach(function (t, i) { var x2 = 4 + i * (bw + gap) + bw + 3, x1 = x2 + gap - 6; out += '<path d="M' + x1 + ' ' + (y + 30) + ' Q' + ((x1 + x2) / 2) + ' ' + (y + 66) + ' ' + (x2 + 4) + ' ' + (y + 32) + '" fill="none" stroke="' + ORANGE + '" stroke-width="1.8"/>' + arrowHead(x2 + 1, y + 30, -Math.PI * 0.62, ORANGE, 7) + label((x1 + x2) / 2, y + 66, t, mode, { size: 11, c: ORANGE, bold: true }); });
    return out + '</svg>';
  }
  /* ---------- statistics ---------- */
  function axis(out, a, X, y, mode) { out.s += line(X(a[0]) - 6, y, X(a[1]) + 6, y); for (var v = a[0]; v <= a[1] + 1e-9; v += a[2]) { out.s += line(X(v), y, X(v), y + 5) + label(X(v), y + 16, fmtNum(v), mode, { size: 9.5 }); } }
  function boxplot(s, mode) {
    var W = s.w || 320, a = s.axis, v = s.v, pad = 16, out = { s: svgOpen(W, 82, 'box plot') };
    function X(t) { return pad + (t - a[0]) / (a[1] - a[0]) * (W - 2 * pad); }
    var y = 26, h = 24;
    out.s += line(X(v[0]), y + h / 2, X(v[1]), y + h / 2) + line(X(v[3]), y + h / 2, X(v[4]), y + h / 2) + line(X(v[0]), y + 4, X(v[0]), y + h - 4) + line(X(v[4]), y + 4, X(v[4]), y + h - 4);
    out.s += '<rect x="' + r2(X(v[1])) + '" y="' + y + '" width="' + r2(X(v[3]) - X(v[1])) + '" height="' + h + '" fill="#f2f6ff" stroke="' + INK + '" stroke-width="1.5"/>' + line(X(v[2]), y, X(v[2]), y + h, { w: 2.2, c: BLUE });
    (s.labs || []).forEach(function (l, i) { if (l) out.s += label(X(v[i]), y - 6, l, mode, { size: 10, bold: true, c: i === 2 ? BLUE : INK }); });
    axis(out, a, X, 62, mode);
    return out.s + '</svg>';
  }
  function dotplot(s, mode) {
    var W = s.w || 320, a = s.axis, pad = 16, cnt = {}, out, top = 0;
    s.data.forEach(function (d) { cnt[d] = (cnt[d] || 0) + 1; top = Math.max(top, cnt[d]); });
    var H = 40 + top * 12; out = { s: svgOpen(W, H, 'dot plot') };
    function X(t) { return pad + (t - a[0]) / (a[1] - a[0]) * (W - 2 * pad); }
    Object.keys(cnt).forEach(function (k) { for (var i = 0; i < cnt[k]; i++) out.s += '<circle cx="' + r2(X(+k)) + '" cy="' + (H - 32 - i * 12) + '" r="4.5" fill="' + BLUE + '"/>'; });
    if (s.mark) s.mark.forEach(function (m) { out.s += line(X(m[0]), 6, X(m[0]), H - 26, { c: ORANGE, dash: true, w: 1.4 }) + label(X(m[0]) + 3, 12, m[1], mode, { size: 10, c: ORANGE, bold: true, anchor: 'start' }); });
    axis(out, a, X, H - 24, mode);
    return out.s + '</svg>';
  }
  function hist(s, mode) {
    var W = s.w || 300, H = 150, b = s.bins, lo = b[0][0], hi = b[b.length - 1][1], ymax = s.ymax || Math.max.apply(null, b.map(function (x) { return x[2]; })), pad = 28, out = { s: svgOpen(W, H, 'histogram') };
    function X(t) { return pad + (t - lo) / (hi - lo) * (W - pad - 10); } function Y(c) { return H - 26 - c / ymax * (H - 44); }
    for (var c = 0; c <= ymax; c += (s.ystep || 1)) out.s += line(pad, Y(c), W - 10, Y(c), { c: GRID, w: 0.7 }) + label(pad - 5, Y(c) + 3, String(c), mode, { size: 9, anchor: 'end' });
    b.forEach(function (x) { out.s += '<rect x="' + r2(X(x[0])) + '" y="' + r2(Y(x[2])) + '" width="' + r2(X(x[1]) - X(x[0])) + '" height="' + r2(Y(0) - Y(x[2])) + '" fill="#cfe0fa" stroke="' + INK + '" stroke-width="1.2"/>'; });
    out.s += line(pad, Y(0), W - 10, Y(0));
    b.forEach(function (x) { out.s += label(X(x[0]), H - 10, fmtNum(x[0]), mode, { size: 9 }); }); out.s += label(X(hi), H - 10, fmtNum(hi), mode, { size: 9 });
    if (s.xl) out.s += label(W / 2, H + 2, s.xl, mode, { size: 9.5 });
    return out.s + '</svg>';
  }
  /* ---------- table (HTML) ---------- */
  function table(s, mode) {
    var h = '<table class="nt-tbl">';
    if (s.head) h += '<thead><tr>' + s.head.map(function (c) { return '<th>' + P.noteText(c, mode) + '</th>'; }).join('') + '</tr></thead>';
    h += '<tbody>' + s.rows.map(function (r) { return '<tr>' + r.map(function (c, j) { return (j === 0 && s.rowHead ? '<th>' : '<td>') + P.noteText(c, mode) + (j === 0 && s.rowHead ? '</th>' : '</td>'); }).join('') + '</tr>'; }).join('') + '</tbody></table>';
    return h;
  }

  var KINDS = { nl: numberLine, plane: plane, geo: geo, area: area, chain: chain, box: boxplot, dot: dotplot, hist: hist, tbl: table };
  P.diagramSvg = function (spec, mode) { var f = KINDS[spec && spec.t]; return f ? f(spec, mode || 'completed') : ''; };
  P.diagram = function (spec, mode) {
    if (!spec) return '';
    var body;
    try { body = P.diagramSvg(spec, mode); } catch (e) { body = '<p class="nt-err">Diagram unavailable (' + esc(e.message) + ')</p>'; }
    return '<figure class="nt-figure nt-k-' + esc(spec.t) + '">' + body + (spec.cap ? '<figcaption>' + P.noteText(spec.cap, mode) + '</figcaption>' : '') + '</figure>';
  };
})(typeof window !== 'undefined' ? window : globalThis);
