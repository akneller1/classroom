/* Matching kinds for Discrete Math and transformations:
     logic   Compound statements: English sentence ↔ symbolic form ↔ truth table ↔ an equivalent symbolic form
     xform   Transformations: picture (pre-image and image) ↔ coordinate rule ↔ words ↔ image coordinates
   A logic set is one truth function of p and q: every card is checked by computing its truth table.
   A transformation set is one mapping of the shared triangle ABC: every card is checked by applying it.
   Needs: menu/match-kinds.js. */
(function (G) {
  'use strict';
  var MK = G.MKMATCH, U = MK.util, SV = MK.svg, k = U.k;

  /* ======================= LOGIC ======================= */
  var V = function (n) { return { op: 'var', n: n }; }, N = function (a) { return { op: 'not', a: a }; }, B2 = function (op) { return function (a, b) { return { op: op, a: a, b: b }; }; };
  var AND = B2('and'), OR = B2('or'), IMP = B2('imp'), IFF = B2('iff'), XOR = B2('xor'), p = V('p'), q = V('q');
  function ev(f, P, Q) {
    switch (f.op) {
      case 'var': return f.n === 'p' ? P : Q;
      case 'not': return !ev(f.a, P, Q);
      case 'and': return ev(f.a, P, Q) && ev(f.b, P, Q);
      case 'or': return ev(f.a, P, Q) || ev(f.b, P, Q);
      case 'imp': return !ev(f.a, P, Q) || ev(f.b, P, Q);
      case 'iff': return ev(f.a, P, Q) === ev(f.b, P, Q);
      case 'xor': return ev(f.a, P, Q) !== ev(f.b, P, Q);
    }
  }
  var ROWS = [[true, true], [true, false], [false, true], [false, false]];
  function tt(f) { return ROWS.map(function (r) { return ev(f, r[0], r[1]) ? 'T' : 'F'; }).join(''); }
  var SYM = { and: '\\wedge', or: '\\vee', imp: '\\rightarrow', iff: '\\leftrightarrow', xor: '\\oplus' };
  function tex(f, top) {
    if (f.op === 'var') return f.n;
    if (f.op === 'not') return '\\neg ' + (f.a.op === 'var' || f.a.op === 'not' ? tex(f.a) : '(' + tex(f.a, true) + ')');
    var s = tex(f.a) + ' ' + SYM[f.op] + ' ' + tex(f.b);
    return top ? s : '(' + s + ')';
  }
  /* English from a formula; S = { p, q, np, nq } clauses */
  function eng(f, S) {
    var cl = function (g) { if (g.op === 'var') return S[g.n]; if (g.op === 'not' && g.a.op === 'var') return S['n' + g.a.n]; return null; };
    var c = cl(f); if (c) return cap(c) + '.';
    if (f.op === 'not') {
      var a = f.a;
      if (a.op === 'or' && cl(a.a) && cl(a.b) && a.a.op === 'var' && a.b.op === 'var') return 'Neither ' + S[a.a.n] + ' nor ' + S[a.b.n] + '.';
      var inner = eng(a, S).replace(/\.$/, ''); return 'It is not true that ' + inner.charAt(0).toLowerCase() + inner.slice(1) + '.';
    }
    var A = cl(f.a), Bc = cl(f.b); if (!A || !Bc) return null;
    if (f.op === 'and') return cap(A) + ' and ' + Bc + '.';
    if (f.op === 'or') return 'Either ' + A + ' or ' + Bc + ' (or both).';
    if (f.op === 'imp') return 'If ' + A + ', then ' + Bc + '.';
    if (f.op === 'iff') return cap(A) + ' if and only if ' + Bc + '.';
    if (f.op === 'xor') return 'Either ' + A + ' or ' + Bc + ', but not both.';
  }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  var LIB = [
    [0, AND(p, q)], [0, AND(q, p)], [0, OR(p, q)], [0, OR(q, p)], [0, N(AND(p, q))], [0, OR(N(p), N(q))], [0, N(OR(p, q))], [0, AND(N(p), N(q))],
    [0, AND(p, N(q))], [0, AND(N(q), p)], [0, AND(N(p), q)], [0, AND(q, N(p))], [0, N(OR(N(p), q))], [0, N(OR(p, N(q)))], [0, OR(N(p), q)], [0, N(AND(p, N(q)))], [0, OR(p, N(q))], [0, N(AND(N(p), q))],
    [1, IMP(p, q)], [1, IMP(N(q), N(p))], [1, IMP(q, p)], [1, IMP(N(p), N(q))], [1, N(IMP(p, q))], [1, N(IMP(q, p))],
    [1, IFF(p, q)], [1, AND(IMP(p, q), IMP(q, p))], [1, IFF(N(p), N(q))],
    [2, XOR(p, q)], [2, N(IFF(p, q))], [2, IFF(N(p), q)], [2, AND(OR(p, q), N(AND(p, q)))], [2, IMP(N(p), q)], [2, IMP(p, N(q))], [2, IMP(N(q), p)], [2, IMP(q, N(p))]
  ];
  var CTX = [
    { p: 'it is raining', q: 'the game is canceled', np: 'it is not raining', nq: 'the game is not canceled' },
    { p: 'the store is open', q: 'Ana buys bread', np: 'the store is not open', nq: 'Ana does not buy bread' },
    { p: 'the light is on', q: 'the door is locked', np: 'the light is off', nq: 'the door is unlocked' },
    { p: 'Sam studies', q: 'Sam passes the test', np: 'Sam does not study', nq: 'Sam does not pass the test' },
    { p: 'the number is even', q: 'the number is greater than 10', np: 'the number is odd', nq: 'the number is not greater than 10' },
    { p: 'the alarm rings', q: 'Jo wakes up early', np: 'the alarm does not ring', nq: 'Jo does not wake up early' }
  ];
  MK.register({
    id: 'logic', name: 'Compound Statement Matching', short: 'Compound Statements', noun: 'statement', anchor: 'sym',
    anchorText: 'Start with each symbolic statement already in its set', anchorHint: 'Recommended: students build each truth table, then find the matching sentence and equivalent statement.',
    blurb: 'Match each <b>symbolic statement</b> to its <b>English sentence</b>, its <b>truth table</b> and a logically <b>equivalent statement</b> (De Morgan’s laws, the contrapositive, a conditional as a disjunction, …). Look-alikes include the converse and the inverse.',
    tip: 'Fill in a truth table for each card (rows TT, TF, FT, FF). Two statements are equivalent exactly when their truth tables match. A conditional is false only when the hypothesis is true and the conclusion is false.',
    types: [{ id: 'sym', L: 'S', name: 'Symbols', plural: 'Symbols' }, { id: 'words', L: 'W', name: 'Sentence', plural: 'Sentences' }, { id: 'table', L: 'T', name: 'Truth table', plural: 'Truth tables' }, { id: 'equiv', L: 'Q', name: 'Equivalent statement', plural: 'Equivalent' }],
    units: { 'discrete-compound-statements-logic': {} },
    maxSets: 8, setOptions: [4, 6, 8],
    context: function (rng) { return { S: rng.pick(CTX) }; },
    gen: function (rng, L, cfg, Un, sets) {
      var lv = L === 'cp2' ? 0 : L === 'cp1' ? 1 : 2, pool = LIB.filter(function (x) { return x[0] <= lv; }).map(function (x) { return x[1]; });
      var f = rng.pick(pool), t = tt(f), same = pool.filter(function (g) { return tt(g) === t && tex(g, true) !== tex(f, true); });
      if (!same.length || t === 'TTTT' || t === 'FFFF') return null;
      var g = rng.pick(same), ws = [f].concat(same).map(function (h) { return eng(h, cfg.ctx.S); }).filter(Boolean).sort(function (a, b) { return a.length - b.length; }), w = ws[0];
      if (!w) return null;
      if (lv >= 1 && /^[pq]$|^\\neg [pq]$/.test(tex(f, true)) && rng.next() < 0.7) return null;   // single letters are too easy above the first level
      return { f: f, g: g, t: t, sym: tex(f, true), equiv: tex(g, true), words: w };
    },
    key: function (t, s) { return s.t; },
    face: function (s, t, mode, B) {
      if (t === 'sym') return U.bigTex(s.sym);
      if (t === 'equiv') return U.bigTex(s.equiv);
      if (t === 'words') return '<div class="mk-txt">' + U.esc(s.words) + '</div>';
      return '<table class="mk-tt"><tr><th>' + k('p') + '</th><th>' + k('q') + '</th><th>?</th></tr>' + ROWS.map(function (r, i) { return '<tr><td>' + (r[0] ? 'T' : 'F') + '</td><td>' + (r[1] ? 'T' : 'F') + '</td><td><b>' + s.t[i] + '</b></td></tr>'; }).join('') + '</table>';
    },
    legend: function (B) { var S = B.ctx.S; return '<p><b>' + k('p') + ':</b> ' + U.esc(cap(S.p)) + '. &nbsp; <b>' + k('q') + ':</b> ' + U.esc(cap(S.q)) + '.</p>'; },
    summary: function (s) { return k(s.sym); },
    noGrid: true
  });
  MK.logic = { tt: tt, ev: ev, tex: tex };

  /* ======================= TRANSFORMATIONS ======================= */
  var XF = {
    translate: function (rng) { var a = rng.int(-6, 6), b = rng.int(-6, 6); if (!a && !b) return null; return { f: function (P) { return [P[0] + a, P[1] + b]; }, rule: '(' + (a ? 'x' + (a > 0 ? ' + ' + a : ' - ' + -a) : 'x') + ',\\ ' + (b ? 'y' + (b > 0 ? ' + ' + b : ' - ' + -b) : 'y') + ')', words: 'Translate ' + (a ? Math.abs(a) + ' unit' + (Math.abs(a) > 1 ? 's' : '') + (a > 0 ? ' right' : ' left') : '') + (a && b ? ' and ' : '') + (b ? Math.abs(b) + ' unit' + (Math.abs(b) > 1 ? 's' : '') + (b > 0 ? ' up' : ' down') : '') }; },
    reflect: function (rng, L) {
      var ch = rng.pick(L === 'cp2' ? ['x', 'y', 'xk', 'yk'] : ['x', 'y', 'yx', 'ynx', 'xk', 'yk']), kk = rng.pick([-2, -1, 1, 2, 3]);
      if (ch === 'x') return { f: function (P) { return [P[0], -P[1]]; }, rule: '(x,\\ -y)', words: 'Reflect across the x-axis' };
      if (ch === 'y') return { f: function (P) { return [-P[0], P[1]]; }, rule: '(-x,\\ y)', words: 'Reflect across the y-axis' };
      if (ch === 'yx') return { f: function (P) { return [P[1], P[0]]; }, rule: '(y,\\ x)', words: 'Reflect across the line y = x' };
      if (ch === 'ynx') return { f: function (P) { return [-P[1], -P[0]]; }, rule: '(-y,\\ -x)', words: 'Reflect across the line y = −x' };
      if (ch === 'xk') return { f: function (P) { return [2 * kk - P[0], P[1]]; }, rule: '(' + 2 * kk + ' - x,\\ y)', words: 'Reflect across the line x = ' + U.txt(kk) };
      return { f: function (P) { return [P[0], 2 * kk - P[1]]; }, rule: '(x,\\ ' + 2 * kk + ' - y)', words: 'Reflect across the line y = ' + U.txt(kk) };
    },
    rotate: function (rng, L) {
      var d = rng.pick(L === 'cp2' ? [180, 90] : [90, 180, 270]), cw = rng.next() < 0.5;
      if (d === 180) return { f: function (P) { return [-P[0], -P[1]]; }, rule: '(-x,\\ -y)', words: 'Rotate 180° about the origin' };
      var ccw90 = (d === 90) !== cw;   // 90° counterclockwise = 270° clockwise
      return ccw90 ? { f: function (P) { return [-P[1], P[0]]; }, rule: '(-y,\\ x)', words: 'Rotate ' + d + '° ' + (cw ? 'clockwise' : 'counterclockwise') + ' about the origin' }
        : { f: function (P) { return [P[1], -P[0]]; }, rule: '(y,\\ -x)', words: 'Rotate ' + d + '° ' + (cw ? 'clockwise' : 'counterclockwise') + ' about the origin' };
    },
    dilate: function (rng, L, tri) {
      var even = tri.every(function (P) { return P[0] % 2 === 0 && P[1] % 2 === 0; }), sc = rng.pick(even ? [2, 0.5] : [2]);
      if (L === 'honors' && rng.next() < 0.3) sc = -1 * sc;
      return { f: function (P) { return [sc * P[0], sc * P[1]]; }, rule: '(' + U.tex(sc) + 'x,\\ ' + U.tex(sc) + 'y)', words: 'Dilate by a scale factor of ' + U.txt(sc) + ' centered at the origin' };
    }
  };
  function rule(t) { return t.replace(/\+ -/g, '- ').replace(/(\d)x/, '$1x'); }
  MK.register({
    id: 'xform', name: 'Transformation Matching', short: 'Transformations', noun: 'transformation', anchor: 'words',
    anchorText: 'Start with each description already in its set', anchorHint: 'Recommended: students apply each transformation to triangle ABC.',
    blurb: 'Every set transforms the same triangle ABC. Match each <b>description</b> to its <b>coordinate rule</b>, the <b>image coordinates</b> of A′, B′ and C′, and the <b>picture</b>. Look-alikes include a reflection and a rotation that land in the same quadrant.',
    tip: 'Apply the rule to each vertex of triangle ABC and compare the coordinates. Watch the order of the letters: a reflection reverses the order A → B → C around the triangle, a rotation keeps it.',
    fams: { translate: 'Translations', reflect: 'Reflections', rotate: 'Rotations', dilate: 'Dilations', compose: 'Compositions (two steps)' }, famLabel: 'Transformations',
    types: [{ id: 'words', L: 'W', name: 'Description', plural: 'Descriptions' }, { id: 'rule', L: 'R', name: 'Rule', plural: 'Rules' }, { id: 'img', L: 'C', name: 'Image coordinates', plural: 'Coordinates' }, { id: 'pic', L: 'G', name: 'Picture', plural: 'Pictures' }],
    units: {
      'geometry-transformations': { fams: ['translate', 'reflect', 'rotate', 'dilate', 'compose'], def: ['translate', 'reflect', 'rotate', 'compose'] },
      'prealgebra-congruence-similarity': { fams: ['translate', 'reflect', 'rotate', 'dilate'], def: ['translate', 'reflect', 'rotate', 'dilate'] }
    },
    maxSets: 8, setOptions: [4, 6, 8], optionalFamFail: ['rotate', 'dilate'],   // only three rotations (and four dilations) exist
    context: function (rng) {
      for (var t = 0; t < 200; t++) {   // a scalene, non-right triangle near the origin, so every image stays on the grid
        var tri = [[rng.int(1, 4), rng.int(1, 3)], [rng.int(1, 4), rng.int(1, 4)], [rng.int(1, 4), rng.int(1, 4)]];
        var d = function (a, b) { return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]); }, s = [d(tri[0], tri[1]), d(tri[1], tri[2]), d(tri[0], tri[2])].sort(function (a, b) { return a - b; });
        var area2 = Math.abs((tri[1][0] - tri[0][0]) * (tri[2][1] - tri[0][1]) - (tri[2][0] - tri[0][0]) * (tri[1][1] - tri[0][1]));
        if (area2 < 3 || s[0] === s[1] || s[1] === s[2] || s[0] + s[1] === s[2]) continue;
        return { tri: tri };
      }
      return null;
    },
    gen: function (rng, L, cfg, Un, sets) {
      var tri = cfg.ctx.tri, fam = rng.pick(cfg.fams), T;
      if (fam === 'compose') {
        var f1 = rng.pick(['reflect', 'rotate']), a = XF[f1](rng, L, tri), b = XF.translate(rng); if (!a || !b) return null;
        T = { f: function (P) { return b.f(a.f(P)); }, words: a.words + ', then ' + b.words.charAt(0).toLowerCase() + b.words.slice(1), rule: null };
        var img0 = tri.map(T.f), A0 = a.f([0, 0]), dx = T.f([0, 0])[0], dy = T.f([0, 0])[1];   // rule from the composed linear part + shift
        var ex = a.f([1, 0]), ey = a.f([0, 1]), lx = [ex[0] - A0[0], ey[0] - A0[0]], ly = [ex[1] - A0[1], ey[1] - A0[1]];
        var term = function (c, v) { return c === 0 ? '' : (c === 1 ? v : c === -1 ? '-' + v : c + v); }, comb = function (l, sh) { var s0 = [term(l[0], 'x'), term(l[1], 'y')].filter(Boolean).join(' + ').replace(/\+ -/g, '- '); return s0 + (sh ? (sh > 0 ? ' + ' + sh : ' - ' + -sh) : ''); };
        T.rule = '(' + comb(lx, dx) + ',\\ ' + comb(ly, dy) + ')';
        if (img0.some(function (P) { return isNaN(P[0]); })) return null;
      } else { T = XF[fam](rng, L, tri); if (!T) return null; }
      var img = tri.map(T.f);
      if (img.some(function (P) { return Math.abs(P[0]) > 8 || Math.abs(P[1]) > 8; })) return null;
      if (img.every(function (P, i) { return P[0] === tri[i][0] && P[1] === tri[i][1]; })) return null;
      // independent check: the printed rule, read back, sends A, B, C to the image
      var check = readRule(rule(T.rule)); if (!check || !tri.every(function (P, i) { var Q = check(P); return U.near(Q[0], img[i][0]) && U.near(Q[1], img[i][1]); })) return null;
      return { fam: fam, words: T.words, rule: rule(T.rule), img: img, key: img.map(function (P) { return P.join(','); }).join(';') };
    },
    key: function (t, s) { return s.key; },
    face: function (s, t, mode, B) {
      if (t === 'words') return '<div class="mk-txt">' + U.esc(s.words) + '</div>';
      if (t === 'rule') return U.bigTex('(x,\\ y) \\to ' + s.rule);
      if (t === 'img') return '<div class="mk-txt">' + s.img.map(function (P, i) { return k('ABC'[i] + "'(" + U.tex(P[0]) + ',\\ ' + U.tex(P[1]) + ')'); }).join('<br>') + '</div>';
      var tri = B.ctx.tri;
      return SV.plane({ xmin: -8, xmax: 8, ymin: -8, ymax: 8, xstep: 1, ystep: 1, items: [{ kind: 'poly', pts: tri, labels: ['A', 'B', 'C'], color: '#64748b', dash: '5 4' }, { kind: 'poly', pts: s.img, labels: ["A′", "B′", "C′"], color: SV.colors.blue, fill: SV.colors.shade }] }, { big: mode === 'big' });
    },
    legend: function (B) { var t = B.ctx.tri; return '<p>Every set transforms triangle ' + k('ABC') + ' with ' + t.map(function (P, i) { return k('ABC'[i] + '(' + P[0] + ',\\ ' + P[1] + ')'); }).join(', ') + '.</p>'; },
    summary: function (s) { return U.esc(s.words); },
    wide: []
  });
  /* read a printed rule "(…,\ …)" back into a function (only x, y, integers, + − and coefficients) */
  function readRule(r) {
    var m = /^\((.*),\\ (.*)\)$/.exec(r); if (!m) return null;
    var part = function (e) {
      e = e.replace(/\s+/g, ''); var terms = e.match(/[+-]?[^+-]+/g) || [], cx = 0, cy = 0, c0 = 0;
      for (var i = 0; i < terms.length; i++) {
        var tm = terms[i], mm = /^([+-]?)(\d*(?:\.\d+)?|\\frac\{(\d+)\}\{(\d+)\})([xy]?)$/.exec(tm); if (!mm) return null;
        var sg = mm[1] === '-' ? -1 : 1, num = mm[3] ? mm[3] / mm[4] : mm[2] === '' ? 1 : +mm[2], v = mm[5];
        if (!v && mm[2] === '' && !mm[3]) return null;
        if (v === 'x') cx += sg * num; else if (v === 'y') cy += sg * num; else c0 += sg * num;
      }
      return [cx, cy, c0];
    };
    var a = part(m[1]), b = part(m[2]); if (!a || !b) return null;
    return function (P) { return [a[0] * P[0] + a[1] * P[1] + a[2], b[0] * P[0] + b[1] * P[1] + b[2]]; };
  }
})(typeof window !== 'undefined' ? window : globalThis);
