/* Grade 5 graphing practice for plot-practice.html (2026-11-19, Grade 5 audit #1).
   The Graphing Practice cards for Coordinate Planes and Graphing and for Data, Line Plots, and Problem Solving opened an
   empty page: the Grade 5 banks have no plot items. This module generates them.
   Coordinate Planes (5.G.A.1, 5.G.A.2, 5.OA.B.3): plot named points in the first quadrant, plot the pairs formed by two
   numerical patterns, and place the corners of a rectangle on a map grid.
   Data (5.MD.B.2): make a line plot of measurements in halves, fourths and eighths, and of mixed-number measurements.
   Items use the 'points' and 'line-plot' tools of core/plot.js, so the check is exact; every target is on the snap grid,
   and the answer key is an SVG drawn from the same numbers. */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = R(0, i), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  var pt = function (p) { return '(' + p[0] + ', ' + p[1] + ')'; };
  var Q10 = { xmin: 0, xmax: 10, ymin: 0, ymax: 10, step: 1, snap: 1 };
  var Q20 = { xmin: 0, xmax: 10, ymin: 0, ymax: 20, step: 1, snap: 1 };
  var FB_PTS = { position: 'Not quite. Start at the origin, move across first (the x-coordinate), then up (the y-coordinate).', 'swapped-coordinates': 'One point is at (y, x). The first number tells how far across, the second how far up.', count: 'Check how many points you need to place.' };
  var FB_LP = { count: 'Put one X for each measurement. Count the measurements in the list.', 'wrong-tick': 'At least one X is one tick away from its value. Check the scale: each tick is one ', 'whole-part': 'At least one X is at the fraction part only. Mixed numbers go past 1 on the scale.', position: 'Not quite. Find each measurement on the scale and stack one X for each time it appears.' };
  var svg = function (w, h, body) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '"><rect width="100%" height="100%" fill="#fff"/>' + body + '</svg>'); };
  function gridKey(g, points, labels, poly) {
    var s = g.ymax > 12 ? 16 : 26, W = (g.xmax - g.xmin) * s + 70, H = (g.ymax - g.ymin) * s + 40, X = function (x) { return 26 + (x - g.xmin) * s; }, Y = function (y) { return 14 + (g.ymax - y) * s; }, h = '';
    for (var i = g.xmin; i <= g.xmax; i++) h += '<line x1="' + X(i) + '" y1="' + Y(g.ymin) + '" x2="' + X(i) + '" y2="' + Y(g.ymax) + '" stroke="' + (i ? '#ddd' : '#333') + '"/>' + '<text x="' + X(i) + '" y="' + (Y(g.ymin) + 14) + '" font-size="10" font-family="Arial" text-anchor="middle">' + i + '</text>';
    for (var j = g.ymin; j <= g.ymax; j++) h += '<line x1="' + X(g.xmin) + '" y1="' + Y(j) + '" x2="' + X(g.xmax) + '" y2="' + Y(j) + '" stroke="' + (j ? '#ddd' : '#333') + '"/>' + (j ? '<text x="' + (X(g.xmin) - 5) + '" y="' + (Y(j) + 3) + '" font-size="10" font-family="Arial" text-anchor="end">' + j + '</text>' : '');
    if (poly) h += '<polygon points="' + poly.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" fill="#4f81bd" fill-opacity="0.15" stroke="#2467a5" stroke-width="2"/>';
    points.forEach(function (p, k) { h += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="5" fill="#c0392b"/>' + (labels[k] ? '<text x="' + (X(p[0]) + 7) + '" y="' + (Y(p[1]) - 7) + '" font-size="13" font-family="Arial" font-weight="bold">' + labels[k] + '</text>' : ''); });
    return svg(W, H, h);
  }
  // fractions as [numerator, denominator] in lowest terms; text "3/8", "1 1/4"
  function gcd(a, b) { while (b) { var t = a % b; a = b; b = t; } return a; }
  function ftext(n, d) { var g = gcd(n, d); n /= g; d /= g; if (d === 1) return String(n); var w = Math.floor(n / d), r = n % d; return (w ? w + ' ' : '') + r + '/' + d; }
  function fplain(n, d) { var g = gcd(n, d); n /= g; d /= g; return d === 1 ? String(n) : n + '/' + d; }  // the value core/plot.js stores
  function lineKey(lo, hi, den, values, mixed) {
    var ticks = (hi - lo) * den, W = 560, x = function (k) { return 40 + k * (W - 80) / ticks; }, h = '<line x1="30" y1="200" x2="' + (W - 30) + '" y2="200" stroke="#333" stroke-width="2"/>', count = {};
    for (var k = 0; k <= ticks; k++) {
      var n = lo * den + k;
      h += '<line x1="' + x(k) + '" y1="194" x2="' + x(k) + '" y2="206" stroke="#333"/><text x="' + x(k) + '" y="224" font-size="12" font-family="Arial" text-anchor="middle">' + (mixed ? ftext(n, den) : fplain(n, den)) + '</text>';
    }
    values.forEach(function (n) { var k = n - lo * den, c = count[k] = (count[k] || 0) + 1; h += '<text x="' + x(k) + '" y="' + (192 - (c - 1) * 18) + '" font-size="17" font-family="Arial" font-weight="bold" text-anchor="middle" fill="#c0392b">×</text>'; });
    return svg(W, 240, h);
  }
  var NAMES = ['A', 'B', 'C'];  // core/plot.js names the movable dots A, B, C, so the prompts use the same letters
  var MAKERS = {
    'coordinate-plane-graphing': {
      'plot-points': ['Plot ordered pairs', function (lv) {
        var n = lv === 'cp2' ? 2 : 3, ps = [], seen = {};
        while (ps.length < n) { var p = [R(lv === 'cp2' ? 1 : 0, 9), R(lv === 'cp2' ? 1 : 0, 9)]; if (seen[p] || p[0] === p[1]) continue; seen[p] = 1; ps.push(p); }
        var names = NAMES.slice(0, n), prompt, steps;
        if (lv === 'honors') {
          var s = ps[0], m = [R(1, 4), R(1, 4)], t = [s[0] + m[0], s[1] + m[1]];
          if (t[0] > 10 || t[1] > 10 || seen[t]) return null;
          ps = [s, t, ps[2]];
          prompt = 'Point A is at ' + pt(s) + '. Point B is ' + m[0] + ' units to the right of A and ' + m[1] + ' units up from A. Point C is at ' + pt(ps[2]) + '. Plot A, B and C.';
          steps = ['A: start at the origin, go ' + s[0] + ' across and ' + s[1] + ' up.', 'B: add ' + m[0] + ' to the x-coordinate and ' + m[1] + ' to the y-coordinate: B = (' + s[0] + ' + ' + m[0] + ', ' + s[1] + ' + ' + m[1] + ') = ' + pt(t) + '.', 'C: go ' + ps[2][0] + ' across and ' + ps[2][1] + ' up.'];
        } else {
          prompt = 'Plot ' + names.map(function (nm, k) { return nm + pt(ps[k]); }).join(lv === 'cp2' ? ' and ' : ', ') + '.';
          steps = ['Start at the origin (0, 0) for each point.'].concat(ps.map(function (p, k) { return names[k] + ': go ' + p[0] + ' across (x), then ' + p[1] + ' up (y).'; }));
        }
        return { prompt: prompt, tool: 'points', grid: Q10, labels: names, target: { points: ps }, feedback: FB_PTS, key: gridKey(Q10, ps, names),
          alt: 'First-quadrant grid with ' + ps.map(function (p, k) { return names[k] + ' at ' + pt(p); }).join(', ') + '.', steps: steps };
      }],
      'pattern-pairs': ['Graph two numerical patterns', function (lv) {
        var a = R(1, 3), k = R(2, lv === 'honors' ? 5 : 4), b = a * k, n = lv === 'honors' ? R(3, 4) : 3;
        if (b * n > 20 || a * n > 10) return null;
        var A = [], B = [];
        for (var i = 1; i <= n; i++) { A.push(a * i); B.push(b * i); }
        var ps = A.map(function (x, i) { return [x, B[i]]; });
        var prompt = 'Pattern A starts at 0 and adds ' + a + '. Pattern B starts at 0 and adds ' + b + '. ' + (lv === 'cp2' ? 'Pattern A after 0: ' + A.join(', ') + '. Pattern B after 0: ' + B.join(', ') + '. ' : '') +
          'Make ordered pairs (Pattern A term, Pattern B term) from the ' + (n === 3 ? 'first 3' : 'first 4') + ' terms after 0 and plot them.' + (lv === 'honors' ? ' Then tell how each Pattern B term compares with the matching Pattern A term.' : '');
        return { prompt: prompt, tool: 'points', grid: Q20, labels: ps.map(function () { return ''; }), target: { points: ps }, feedback: FB_PTS, key: gridKey(Q20, [[0, 0]].concat(ps), ps.map(function () { return ''; }).concat('')),
          alt: 'Grid with the points ' + ps.map(pt).join(', ') + ' on a straight line from the origin.',
          steps: ['Pattern A: ' + A.join(', ') + '.', 'Pattern B: ' + B.join(', ') + '.', 'Pairs: ' + ps.map(pt).join(', ') + '.'].concat(lv === 'honors' ? ['Each Pattern B term is ' + k + ' times the matching Pattern A term, because ' + b + ' = ' + k + ' × ' + a + '.'] : []) };
      }],
            'map-rectangle': ['Place a rectangle on a map grid', function (lv) {
        var D = [R(0, 5), R(0, 5)], w = R(2, 5), h = R(2, 5);
        if (w === h || D[0] + w > 10 || D[1] + h > 10) return null;
        // corners A (top left), B (top right), C (bottom right), D (bottom left); D is given, the dots are A, B, C
        var C = [D[0] + w, D[1]], B = [D[0] + w, D[1] + h], A = [D[0], D[1] + h], place = pick(['garden', 'playground', 'parking lot', 'soccer field']);
        var given = lv === 'cp2' ? ' Corner C is at ' + pt(C) + '.' : '';
        var size = lv === 'honors' ? ' Its area is ' + w * h + ' square units and side DC is ' + w + ' units long.' : ' It is ' + w + ' units wide and ' + h + ' units tall.';
        var ask = lv === 'cp2' ? ' Plot A and B.' : ' Plot A, B and C (one dot on each corner, in any order).';
        var tgt = lv === 'cp2' ? [A, B] : [A, B, C], labels = lv === 'cp2' ? ['A', 'B'] : ['A', 'B', 'C'];
        return { prompt: 'A rectangular ' + place + ' on a map grid has corners A, B, C and D. D is at ' + pt(D) + ', C is to the right of D, B is above C, and A is above D.' + size + given + ask,
          tool: 'points', grid: Q10, labels: labels, target: { points: tgt }, feedback: FB_PTS, key: gridKey(Q10, [A, B, C, D], ['A', 'B', 'C', 'D'], [A, B, C, D]),
          alt: 'Rectangle with A at ' + pt(A) + ', B at ' + pt(B) + ', C at ' + pt(C) + ', D at ' + pt(D) + '.',
          steps: (lv === 'honors' ? ['CB = area ÷ DC = ' + w * h + ' ÷ ' + w + ' = ' + h + ' units.'] : []).concat(['C is ' + w + ' units right of D: C = ' + pt(C) + '.', 'B is ' + h + ' units above C: B = ' + pt(B) + '.', 'A is ' + h + ' units above D: A = ' + pt(A) + '.']) };
      }]
    },
    'data-line-plots-problem-solving': {
      'fraction-line-plot': ['Make a line plot of fractions', function (lv) {
        var den = lv === 'cp2' ? pick([2, 4]) : lv === 'cp1' ? pick([4, 8]) : 8, n = lv === 'cp2' ? 6 : 8;
        var ctx = pick([['Lengths of ribbon', 'yard', 'yards'], ['Rainfall each day', 'inch', 'inches'], ['Water in each beaker', 'liter', 'liters'], ['Weights of apples', 'pound', 'pounds']]);
        var vals = []; for (var i = 0; i < n; i++) vals.push(R(lv === 'cp2' ? 1 : 1, den));
        if (new Set(vals).size < 3) return null;
        var list = vals.map(function (v) { return ftext(v, den); });
        var total = vals.reduce(function (s, v) { return s + v; }, 0);
        if (lv === 'honors' && den * n / gcd(total, den * n) > 16) return null;  // keep the fair share a friendly fraction
        var prompt = ctx[0] + ', in ' + ctx[2] + ': ' + list.join(', ') + '. Make a line plot of the data. Put one mark for each measurement.' + (lv === 'honors' ? ' Then find the amount in each if the total were shared equally among all ' + n + '.' : '');
        var steps = ['The scale goes from 0 to 1 in steps of 1/' + den + '.', 'Count each value: ' + Array.from(new Set(vals)).sort(function (a, b) { return a - b; }).map(function (v) { return ftext(v, den) + ' appears ' + vals.filter(function (x) { return x === v; }).length + ' time' + (vals.filter(function (x) { return x === v; }).length === 1 ? '' : 's'); }).join(', ') + '.', 'Stack one X above the value for each time it appears.'];
        if (lv === 'honors') steps.push('Total: ' + ftext(total, den) + ' ' + ctx[2] + '. Shared equally: ' + ftext(total, den) + ' ÷ ' + n + ' = ' + ftext(total, den * n) + ' ' + (total <= den * n ? ctx[1] : ctx[2]) + ' each.');
        return { prompt: prompt, tool: 'line-plot', title: ctx[0], units: ctx[2], mark: 'x', numberLine: { min: '0', max: '1', tick: '1/' + den, snap: '1/' + den, labelEvery: 1, labelFormat: 'fraction' },
          target: { values: vals.map(function (v) { return fplain(v, den); }) }, feedback: Object.assign({}, FB_LP, { 'wrong-tick': FB_LP['wrong-tick'] + '1/' + den + '.' }),
          key: lineKey(0, 1, den, vals, false), alt: 'Line plot from 0 to 1 in ' + (den === 2 ? 'halves' : den === 4 ? 'fourths' : 'eighths') + ' with an X for each of ' + list.join(', ') + '.', steps: steps };
      }],
      'mixed-line-plot': ['Make a line plot of mixed numbers', function (lv) {
        var den = lv === 'cp2' ? 2 : 4, lo = 1, hi = 3, n = lv === 'cp2' ? 6 : lv === 'cp1' ? 8 : 9;
        var ctx = pick([['Heights of seedlings', 'inch', 'inches'], ['Lengths of pencils', 'inch', 'inches'], ['Distances walked', 'mile', 'miles'], ['Weights of pumpkins', 'pound', 'pounds']]);
        var vals = []; for (var i = 0; i < n; i++) vals.push(R(lo * den, hi * den));
        if (new Set(vals).size < 3 || vals.every(function (v) { return v % den === 0; })) return null;
        var list = shuffle(vals).map(function (v) { return ftext(v, den); });
        var mx = Math.max.apply(null, vals), mn = Math.min.apply(null, vals);
        var prompt = ctx[0] + ', in ' + ctx[2] + ': ' + list.join(', ') + '. Make a line plot of the data.' + (lv === 'honors' ? ' Then find the difference between the greatest and least measurement.' : '');
        var steps = ['The scale goes from 1 to 3 in steps of 1/' + den + '. Mixed numbers like ' + ftext(lo * den + 1, den) + ' go between the whole numbers.', 'Stack one X above each measurement. There are ' + n + ' X’s in all.'];
        if (lv === 'honors') steps.push('Greatest ' + ftext(mx, den) + ', least ' + ftext(mn, den) + ': ' + ftext(mx, den) + ' − ' + ftext(mn, den) + ' = ' + ftext(mx - mn, den) + ' ' + (mx - mn <= den ? ctx[1] : ctx[2]) + '.');
        return { prompt: prompt, tool: 'line-plot', title: ctx[0], units: ctx[2], mark: 'x', numberLine: { min: String(lo), max: String(hi), tick: '1/' + den, snap: '1/' + den, labelEvery: 1, labelFormat: 'mixed' },
          target: { values: vals.map(function (v) { return fplain(v, den); }) }, feedback: Object.assign({}, FB_LP, { 'wrong-tick': FB_LP['wrong-tick'] + '1/' + den + '.' }),
          key: lineKey(lo, hi, den, vals, true), alt: 'Line plot from 1 to 3 in ' + (den === 2 ? 'halves' : 'fourths') + ' with an X for each of ' + list.join(', ') + '.', steps: steps };
      }]
    }
  };
  function item(id, skillId, r) {
    var plot = { tool: r.tool, target: r.target, feedback: r.feedback, answerKey: { svg: r.key, alt: r.alt }, check: { type: 'exact-after-snap' } };
    ['grid', 'labels', 'numberLine', 'title', 'units', 'mark'].forEach(function (k) { if (r[k] !== undefined) plot[k] = r[k]; });
    return { id: id, skillId: skillId, prompt: r.prompt, solutionSteps: r.steps, plot: plot };
  }
  G.MK_G5_PLOT = {
    units: Object.keys(MAKERS),
    makers: MAKERS,
    skills: function (unitId) { var m = MAKERS[unitId] || {}; return Object.keys(m).map(function (k) { return { id: k, name: m[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      var m = MAKERS[unitId]; if (!m) return [];
      var ids = skillId ? [skillId] : Object.keys(m), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 3000) {
        var id = ids[out.length % ids.length], r = m[id] && m[id][1](level || 'cp1'); if (!r || seen[r.prompt]) continue; seen[r.prompt] = 1;
        out.push(item('g5-plot-' + id + '-' + out.length, id, r));
      }
      return out;
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
