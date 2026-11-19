/* Statistics graphing practice for plot-practice.html (2026-11-18, Statistics audit #9).
   Generated number-line items for two Statistics units: shade a Normal area, mark the center and ±2 standard deviations of a
   sampling distribution, graph a confidence interval, and shade the p-value or rejection region of a test. Each item uses
   the 'number-line-inequality' or 'number-line-point' tool of core/plot.js, so the check is exact; every target value is
   on the number line's snap grid, and the answer key is an SVG of the Normal curve (or interval) with the answer drawn on it. */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  function rnd(v, d) { var f = Math.pow(10, d); return Math.round(v * f + (v >= 0 ? 1e-9 : -1e-9)) / f; }
  var M = function (v) { return String(v).replace('-', '−'); };
  /* Table A convention: z rounded to two decimals; Φ by a series accurate to 1e-7 */
  function phi(z) { var t = 1 / (1 + 0.2316419 * Math.abs(z)), d = 0.3989422804014327 * Math.exp(-z * z / 2), p = d * t * (0.31938153 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429)))); return z >= 0 ? 1 - p : p; }
  function tableA(z) { return rnd(phi(rnd(z, 2)), 4); }
  var svgUrl = function (w, h, body) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '"><rect width="100%" height="100%" fill="#fff"/>' + body + '</svg>'); };
  /* Answer key: a number line from lo to hi (ticks every tick), an optional Normal curve N(mu, sd) with the shaded region
     (an array of [a, b] pieces), an optional interval bar and marked points. */
  function key(o) {
    var W = 560, H = o.mu === undefined ? 110 : 230, L = 30, Rr = 530, base = o.mu === undefined ? 55 : 170, X = function (v) { return L + (v - o.lo) / (o.hi - o.lo) * (Rr - L); }, h = '';
    if (o.mu !== undefined) {
      var top = 120, pk = 1 / (o.sd * Math.sqrt(2 * Math.PI)), Y = function (v) { var z = (v - o.mu) / o.sd; return base - top * Math.exp(-z * z / 2); };
      (o.shade || []).forEach(function (seg) {
        var a = Math.max(o.lo, seg[0]), b = Math.min(o.hi, seg[1]), d = 'M' + X(a).toFixed(1) + ' ' + base;
        for (var i = 0; i <= 80; i++) { var v = a + (b - a) * i / 80; d += ' L' + X(v).toFixed(1) + ' ' + Y(v).toFixed(1); }
        h += '<path d="' + d + ' L' + X(b).toFixed(1) + ' ' + base + ' Z" fill="#4f81bd" fill-opacity="0.45"/>';
      });
      var c = '';
      for (var j = 0; j <= 200; j++) { var v2 = o.lo + (o.hi - o.lo) * j / 200; c += (j ? ' L' : 'M') + X(v2).toFixed(1) + ' ' + Y(v2).toFixed(1); }
      h += '<path d="' + c + '" fill="none" stroke="#1f4e79" stroke-width="2"/>';
      void pk;
    }
    h += '<line x1="' + L + '" y1="' + base + '" x2="' + Rr + '" y2="' + base + '" stroke="#333" stroke-width="1.5"/>';
    for (var t = o.lo, k = 0; t <= o.hi + 1e-9 && k < 60; t = rnd(t + o.tick, 6), k++) {
      h += '<line x1="' + X(t) + '" y1="' + (base - 5) + '" x2="' + X(t) + '" y2="' + (base + 5) + '" stroke="#333"/><text x="' + X(t) + '" y="' + (base + 20) + '" font-size="11" text-anchor="middle" font-family="Arial">' + M(t) + '</text>';
    }
    if (o.bar) h += '<line x1="' + X(o.bar[0]) + '" y1="' + (base - 18) + '" x2="' + X(o.bar[1]) + '" y2="' + (base - 18) + '" stroke="#c0392b" stroke-width="5"/>';
    (o.points || []).forEach(function (p) { h += '<circle cx="' + X(p) + '" cy="' + base + '" r="6" fill="' + (o.open ? '#fff' : '#c0392b') + '" stroke="#c0392b" stroke-width="2.5"/>'; });
    if (o.label) h += '<text x="' + (W / 2) + '" y="' + (H - 8) + '" font-size="12" text-anchor="middle" font-family="Arial">' + o.label + '</text>';
    return svgUrl(W, H, h);
  }
  var FB_SHADE = { boundary: 'Check where your boundary sits: it is the value named in the question.', direction: 'You shaded the wrong side. "Greater than" shades to the right; "less than" to the left.',
    'closed-open': 'Use an open dot for < or > and a closed dot for ≤ or ≥.', 'and-or': 'Between two values shades the middle; "outside" shades both tails.' };
  var FB_PTS = { count: 'Mark exactly three points: the center and two standard deviations on each side.', position: 'Check each point: center = mean of the sampling distribution; the others are center ± 2 × standard deviation.' };
  var QUANT = [['heights of adult women', 'inches', 64, 2.5], ['scores on a reading test', 'points', 500, 100], ['times to run a mile', 'minutes', 9, 1.5], ['weights of apples', 'grams', 150, 20],
    ['battery lives', 'hours', 40, 4], ['commute times', 'minutes', 30, 8], ['IQ scores', 'points', 100, 15], ['resting pulse rates', 'beats per minute', 72, 8]];
  var MAKERS = {
    'anticipating-patterns': {
      'normal-area': ['Shade a Normal area', function (lv) {
        var c = pick(QUANT), mu = c[2], sd = c[3], half = sd / 2, lo = mu - 3.5 * sd, hi = mu + 3.5 * sd, ka = R(-5, 5), kb = ka + R(1, 4);
        var a = rnd(mu + ka * half, 4), b = rnd(mu + kb * half, 4), kind = lv === 'cp2' ? pick(['>', '<']) : lv === 'cp1' ? pick(['>', '<', 'between']) : pick(['between', 'outside', '>']);
        if (kb > 6) return null;
        var za = (a - mu) / sd, zb = (b - mu) / sd, target, prompt, prob, shade, steps;
        var line = { min: lo, max: hi, tick: half, labelEvery: 1, labelFormat: 'decimal', snap: half };
        if (kind === '>' || kind === '<') {
          target = { boundary: a, closed: false, direction: kind === '>' ? 'right' : 'left' };
          prob = kind === '>' ? rnd(1 - tableA(za), 4) : tableA(za);
          prompt = 'The ' + c[0] + ' are approximately Normal with mean ' + M(mu) + ' and standard deviation ' + M(sd) + ' ' + c[1] + '. On the number line, shade the values ' + (kind === '>' ? 'greater than ' : 'less than ') + M(a) + ' ' + c[1] + ' (X ' + kind + ' ' + M(a) + ').';
          shade = [kind === '>' ? [a, hi] : [lo, a]];
          steps = ['"' + (kind === '>' ? 'Greater' : 'Less') + ' than" is a strict inequality: open dot at ' + M(a) + ', shading to the ' + (kind === '>' ? 'right' : 'left') + '.',
            'z = (' + M(a) + ' − ' + M(mu) + ')/' + M(sd) + ' = ' + M(rnd(za, 2)) + '.', 'The shaded area is P(X ' + kind + ' ' + M(a) + ') = ' + (kind === '>' ? '1 − ' + tableA(za).toFixed(4) + ' = ' : '') + prob.toFixed(4) + ' (Table A).'];
        } else if (kind === 'between') {
          target = { between: true, left: { value: a, closed: true }, right: { value: b, closed: true } };
          prob = rnd(tableA(zb) - tableA(za), 4);
          prompt = 'The ' + c[0] + ' are approximately Normal with mean ' + M(mu) + ' and standard deviation ' + M(sd) + ' ' + c[1] + '. Shade the values from ' + M(a) + ' to ' + M(b) + ' ' + c[1] + ' (' + M(a) + ' ≤ X ≤ ' + M(b) + ').';
          shade = [[a, b]];
          steps = ['"From … to …" includes both ends: closed dots at ' + M(a) + ' and ' + M(b) + ', shading between them.', 'z-scores: ' + M(rnd(za, 2)) + ' and ' + M(rnd(zb, 2)) + '.',
            'The shaded area is ' + tableA(zb).toFixed(4) + ' − ' + tableA(za).toFixed(4) + ' = ' + prob.toFixed(4) + ' (Table A).'];
        } else {
          var w = R(2, 4), a2 = rnd(mu - w * half, 4), b2 = rnd(mu + w * half, 4);
          a = a2; b = b2; za = (a - mu) / sd; zb = (b - mu) / sd;
          target = { between: false, left: { value: a, closed: false }, right: { value: b, closed: false } };
          prob = rnd(tableA(za) + 1 - tableA(zb), 4);
          prompt = 'The ' + c[0] + ' are approximately Normal with mean ' + M(mu) + ' and standard deviation ' + M(sd) + ' ' + c[1] + '. Shade the values more than ' + M(rnd(w * half, 4)) + ' ' + c[1] + ' away from the mean (X < ' + M(a) + ' or X > ' + M(b) + ').';
          shade = [[lo, a], [b, hi]];
          steps = ['"More than … away" means both tails: open dots at ' + M(a) + ' and ' + M(b) + ', shading outward (OR).', 'z = ±' + M(rnd(zb, 2)) + '.',
            'The shaded area is 2 × ' + tableA(za).toFixed(4) + ' = ' + prob.toFixed(4) + ' (Table A).'];
        }
        return { prompt: prompt, tool: 'number-line-inequality', line: line, target: target, feedback: FB_SHADE, steps: steps,
          key: key({ lo: lo, hi: hi, tick: half, mu: mu, sd: sd, shade: shade, label: 'Shaded area ≈ ' + prob.toFixed(4) }), alt: 'Normal curve with mean ' + M(mu) + ' and SD ' + M(sd) + '; the shaded area is ' + prob.toFixed(4) + '.' };
      }],
      'sampling-distribution': ['Mark a sampling distribution (center ± 2 SD)', function (lv) {
        var isP = lv === 'cp2' ? false : lv === 'honors' ? true : Math.random() < 0.5, mu, sd, desc, steps, lo, hi, tick, snap;
        if (isP) {
          var o = pick([[0.5, 100, 0.05], [0.2, 100, 0.04], [0.9, 100, 0.03], [0.6, 150, 0.04], [0.3, 84, 0.05], [0.5, 400, 0.025], [0.1, 225, 0.02], [0.8, 400, 0.02]]);
          mu = o[0]; sd = o[2]; tick = sd; snap = rnd(sd / 5, 4) >= 0.005 ? 0.005 : 0.001;
          desc = 'In a large population, p = ' + M(mu) + '. Random samples of n = ' + o[1] + ' are taken and p̂ is computed for each. On the number line, mark the mean of the sampling distribution of p̂ and the two values 2 standard deviations below and above it.';
          steps = ['Mean of p̂: μ_p̂ = p = ' + M(mu) + '.', 'Standard deviation: σ_p̂ = √(p(1 − p)/n) = √(' + M(mu) + ' × ' + M(rnd(1 - mu, 2)) + '/' + o[1] + ') = ' + M(sd) + '.',
            'Mark ' + M(rnd(mu - 2 * sd, 4)) + ', ' + M(mu) + ' and ' + M(rnd(mu + 2 * sd, 4)) + '. About 95% of sample proportions fall between the outer marks (Large Counts holds: np and n(1 − p) ≥ 10).'];
        } else {
          var c = pick(QUANT), opts = [4, 9, 16, 25, 64, 100].filter(function (n) { var v = c[3] / Math.sqrt(n); return Math.abs(v * 2 - Math.round(v * 2)) < 1e-9 && v >= 0.5; });
          if (!opts.length) return null;
          var nn = pick(opts);
          mu = c[2]; sd = c[3] / Math.sqrt(nn); tick = sd; snap = 0.5;
          desc = 'The ' + c[0] + ' in a population have mean ' + M(mu) + ' and standard deviation σ = ' + M(c[3]) + ' ' + c[1] + '. For random samples of n = ' + nn + ', mark the mean of the sampling distribution of x̄ and the two values 2 standard deviations below and above it.';
          steps = ['Mean of x̄: μ_x̄ = μ = ' + M(mu) + '.', 'Standard deviation: σ_x̄ = σ/√n = ' + M(c[3]) + '/√' + nn + ' = ' + M(sd) + '.', 'Mark ' + M(mu - 2 * sd) + ', ' + M(mu) + ' and ' + M(mu + 2 * sd) + '. About 95% of sample means fall between the outer marks.'];
        }
        lo = rnd(mu - 4 * sd, 4); hi = rnd(mu + 4 * sd, 4);
        if (isP) { lo = Math.max(0, lo); hi = Math.min(1, hi); }
        var pts = [rnd(mu - 2 * sd, 4), mu, rnd(mu + 2 * sd, 4)];
        return { prompt: desc, tool: 'number-line-point', line: { min: lo, max: hi, tick: tick, labelEvery: 1, labelFormat: 'decimal', snap: snap }, target: { values: pts }, feedback: FB_PTS, steps: steps,
          key: key({ lo: lo, hi: hi, tick: tick, mu: mu, sd: sd, points: pts, label: 'center ' + M(mu) + ', standard deviation ' + M(sd) }), alt: 'Normal-shaped sampling distribution centered at ' + M(mu) + ' with points at ' + pts.map(M).join(', ') + '.' };
      }]
    },
    'statistical-inference': {
      'confidence-interval': ['Graph a confidence interval', function (lv) {
        var lo, hi, tick, snap, a, b, prompt, steps, center, me;
        if (lv === 'cp2') {
          var c = pick(QUANT); center = c[2]; me = pick([1, 2, 3, 4]) * (c[3] >= 5 ? c[3] / 4 : 0.5);
          tick = me / 2; snap = me / 2; lo = rnd(center - 4 * me, 4); hi = rnd(center + 4 * me, 4);
          prompt = 'A 95% confidence interval for the mean ' + c[0].replace(/s$/, '') + ' is ' + M(center) + ' ± ' + M(me) + ' ' + c[1] + '. Graph the interval on the number line (both endpoints included).';
          steps = ['Lower endpoint: ' + M(center) + ' − ' + M(me) + ' = ' + M(rnd(center - me, 4)) + '.', 'Upper endpoint: ' + M(center) + ' + ' + M(me) + ' = ' + M(rnd(center + me, 4)) + '.', 'Closed dots at both endpoints and shading between them (AND).'];
        } else {
          var ph = pick([0.42, 0.55, 0.61, 0.36, 0.48, 0.72]), n = pick([400, 500, 600]), z = lv === 'honors' ? pick([1.645, 1.96, 2.576]) : 1.96, se = Math.sqrt(ph * (1 - ph) / n);
          center = ph; me = rnd(z * se, 2); tick = 0.02; snap = 0.01; lo = rnd(ph - 0.1, 2); hi = rnd(ph + 0.1, 2);
          prompt = 'In a random sample of ' + n + ', p̂ = ' + M(ph) + '. Build the ' + ({ 1.645: '90', 1.96: '95', 2.576: '99' })[z] + '% confidence interval for p (z* = ' + z + '), round the margin of error to two decimal places, and graph the interval (both endpoints included).';
          steps = ['SE = √(p̂(1 − p̂)/n) = √(' + M(ph) + ' × ' + M(rnd(1 - ph, 2)) + '/' + n + ') ≈ ' + se.toFixed(4) + '.', 'ME = z* × SE = ' + z + ' × ' + se.toFixed(4) + ' ≈ ' + (z * se).toFixed(4) + ', which rounds to ' + me.toFixed(2) + '.',
            'Interval: ' + M(ph) + ' ± ' + me.toFixed(2) + ' = (' + M(rnd(ph - me, 2)) + ', ' + M(rnd(ph + me, 2)) + '). Closed dots at both endpoints, shading between.'];
        }
        a = rnd(center - me, 4); b = rnd(center + me, 4);
        return { prompt: prompt, tool: 'number-line-inequality', line: { min: lo, max: hi, tick: tick, labelEvery: 1, labelFormat: 'decimal', snap: snap }, target: { between: true, left: { value: a, closed: true }, right: { value: b, closed: true } }, feedback: FB_SHADE, steps: steps,
          key: key({ lo: lo, hi: hi, tick: tick, bar: [a, b], points: [a, b], label: 'Interval (' + M(a) + ', ' + M(b) + ')' }), alt: 'Number line with the interval from ' + M(a) + ' to ' + M(b) + ' marked with closed dots.' };
      }],
      'p-value-region': ['Shade the p-value region', function (lv) {
        var z = rnd(pick([1, -1]) * (1 + R(2, 18) / 10), 1), alt = lv === 'cp2' ? (z > 0 ? '>' : '<') : lv === 'cp1' ? pick(['>', '<']) : '≠', target, pv, shade, steps;
        if (lv === 'cp1' && ((alt === '>' && z < 0) || (alt === '<' && z > 0))) z = -z;
        var line = { min: -4, max: 4, tick: 0.5, labelEvery: 1, labelFormat: 'decimal', snap: 0.1 };
        if (alt === '≠') {
          var az = Math.abs(z);
          target = { between: false, left: { value: -az, closed: false }, right: { value: az, closed: false } };
          pv = rnd(2 * (1 - tableA(az)), 4); shade = [[-4, -az], [az, 4]];
          steps = ['A two-sided test counts results at least as extreme in either direction: z ≤ −' + M(az) + ' or z ≥ ' + M(az) + '.', 'Shade both tails (OR), with open dots at ±' + M(az) + '.', 'p-value = 2 × (1 − ' + tableA(az).toFixed(4) + ') = ' + pv.toFixed(4) + '.'];
        } else {
          target = { boundary: z, closed: false, direction: alt === '>' ? 'right' : 'left' };
          pv = alt === '>' ? rnd(1 - tableA(z), 4) : tableA(z); shade = [alt === '>' ? [z, 4] : [-4, z]];
          steps = ['Hₐ uses ' + alt + ', so the p-value is the area to the ' + (alt === '>' ? 'right' : 'left') + ' of the observed z = ' + M(z) + '.', 'Open dot at ' + M(z) + ', shading to the ' + (alt === '>' ? 'right' : 'left') + '.', 'p-value = ' + pv.toFixed(4) + ' (Table A).'];
        }
        var who = pick(['voters who support a new park', 'students who walk to school', 'customers who return an item', 'flights that leave on time']);
        return { prompt: 'A one-proportion z test about the proportion of ' + who + ' uses Hₐ: p ' + alt + ' p₀ and gives z = ' + M(z) + '. On the z number line, shade the values of the test statistic that make up the p-value.', tool: 'number-line-inequality', line: line, target: target, feedback: FB_SHADE, steps: steps,
          key: key({ lo: -4, hi: 4, tick: 0.5, mu: 0, sd: 1, shade: shade, label: 'p-value ≈ ' + pv.toFixed(4) }), alt: 'Standard Normal curve with the p-value region shaded; area ' + pv.toFixed(4) + '.' };
      }],
      'rejection-region': ['Shade the rejection region', function (lv) {
        var o = lv === 'cp2' ? pick([['>', 0.05, 1.645], ['<', 0.05, -1.645]]) : pick([['>', 0.05, 1.645], ['<', 0.05, -1.645], ['≠', 0.05, 1.96], ['≠', 0.01, 2.576], ['>', 0.01, 2.326], ['<', 0.10, -1.282]]);
        var alt = o[0], a = o[1], zc = o[2], target, shade;
        var line = { min: -3.5, max: 3.5, tick: 0.5, labelEvery: 1, labelFormat: 'decimal', snap: 0.001 };
        if (alt === '≠') { target = { between: false, left: { value: -zc, closed: true }, right: { value: zc, closed: true } }; shade = [[-3.5, -zc], [zc, 3.5]]; }
        else { target = { boundary: zc, closed: true, direction: alt === '>' ? 'right' : 'left' }; shade = [alt === '>' ? [zc, 3.5] : [-3.5, zc]]; }
        var topic = pick(['voters who support a bond', 'parts that are defective', 'students who own a tablet', 'adults who exercise daily', 'seeds that sprout', 'shoppers who use coupons']);
        return { prompt: 'A z test about the proportion of ' + topic + ' uses Hₐ: p ' + alt + ' p₀ at significance level α = ' + a + '. Shade the values of z that lead to rejecting H₀ (use closed dots at the critical value' + (alt === '≠' ? 's' : '') + ').', tool: 'number-line-inequality', line: line, target: target, feedback: FB_SHADE,
          steps: [(alt === '≠' ? 'Split α between the two tails: ' + a / 2 + ' in each.' : 'Put all of α = ' + a + ' in the ' + (alt === '>' ? 'right' : 'left') + ' tail.'), 'Critical value' + (alt === '≠' ? 's: z* = ±' + zc : ': z* = ' + M(zc)) + ' (Table A or invNorm).', 'Reject H₀ when z is ' + (alt === '≠' ? 'at or beyond ±' + zc : (alt === '>' ? 'at or above ' : 'at or below ') + M(zc)) + '.'],
          key: key({ lo: -3.5, hi: 3.5, tick: 0.5, mu: 0, sd: 1, shade: shade, label: 'Rejection region: area α = ' + a }), alt: 'Standard Normal curve with the rejection region (area ' + a + ') shaded beyond ' + (alt === '≠' ? '±' + zc : M(zc)) + '.' };
      }]
    }
  };
  function item(id, skillId, r) {
    return { id: id, skillId: skillId, prompt: r.prompt, solutionSteps: r.steps, plot: { tool: r.tool, numberLine: r.line, target: r.target, feedback: r.feedback, answerKey: { svg: r.key, alt: r.alt }, check: { type: 'exact-after-snap' } } };
  }
  G.MK_STAT_PLOT = {
    units: Object.keys(MAKERS),
    makers: MAKERS,
    skills: function (unitId) { var m = MAKERS[unitId] || {}; return Object.keys(m).map(function (k) { return { id: k, name: m[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      var m = MAKERS[unitId]; if (!m) return [];
      var ids = skillId ? [skillId] : Object.keys(m), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 2000) {
        var id = ids[out.length % ids.length], r = m[id] && m[id][1](level || 'cp1'); if (!r || seen[r.prompt]) continue; seen[r.prompt] = 1;
        out.push(item('stat-plot-' + id + '-' + out.length, id, r));
      }
      return out;
    },
    phi: phi
  };
})(typeof window !== 'undefined' ? window : globalThis);
