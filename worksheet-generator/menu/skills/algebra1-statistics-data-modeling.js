/* Menu Assessment Generator — Algebra 1 · Unit 12 Statistics and Data Modeling (roadmap days 163–174).
   Skill groups: CENTER (mean, median, mode, MAD), SPREAD (range, quartiles, IQR, outliers), DISPLAY (dot plots and
   box plots), TWOWAY (two-way tables and relative frequency), SCATTER (correlation, lines of fit, residuals).
   Dot plots, box plots, scatter plots and two-way tables are drawn from specs; the verifier reads them back.
   Quartiles use the medians of the lower and upper halves, leaving out the median when the count is odd. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num, lin = K.lin, Fr = K.Fr;
  var need = K.need, nz = K.nz, step = K.step, F = K.F;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function list(a) { return a.map(function (v) { return dec(v); }).join(',\\ '); }
  function dec(v) { return typeof v === 'number' ? (v < 0 ? '-' : '') + String(Math.round(Math.abs(v) * 1000) / 1000) : num(v); }
  function sorted(a) { return a.slice().sort(function (x, y) { return x - y; }); }
  function median(s) { s = sorted(s); var n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; }
  function quart(a) { var s = sorted(a), n = s.length, h = Math.floor(n / 2); return [s[0], median(s.slice(0, h)), median(s), median(s.slice(n - h)), s[n - 1]]; }
  function mean(a) { return a.reduce(function (x, y) { return x + y; }, 0) / a.length; }
  function mad(a) { var m = mean(a); return mean(a.map(function (x) { return Math.abs(x - m); })); }
  function outl(a) { var q = quart(a), i = q[3] - q[1]; return a.filter(function (x) { return x < q[1] - 1.5 * i || x > q[3] + 1.5 * i; }); }
  function rnd(r, n, lo, hi) { var a = []; for (var i = 0; i < n; i++) a.push(r.int(lo, hi)); return a; }
  function exact(x, places) { return Math.abs(x * Math.pow(10, places) - Math.round(x * Math.pow(10, places))) < 1e-9; }
  function r1(x) { return Math.round(x * 10 + 1e-9) / 10; }
  var CTX = [['quiz scores', ''], ['minutes spent on homework', ' minutes'], ['points scored in a game', ' points'], ['hours of sleep', ' hours'], ['books read this year', ' books']];

  /* ================= CENTER · mean, median, mode, MAD ================= */
  skill({
    id: 'center', best: [0, 1], tag: 'CENTER', name: 'Mean, median, mode and MAD',
    blurb: 'Mean and median (CP2) → MAD, a missing value, dot plots (CP1) → a new value added, comparing two groups by MAD (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 2, 6, 3, 4, 5, 7][ctx.c], steps = [], cx = r.pick(CTX), data, D;
      if (c === 1) { data = rnd(r, 4, 2, 20); var m1 = r.int(5, 15), l1 = 5 * m1 - sum(data); need(l1 >= 1 && l1 <= 25); data.push(l1); data = r.shuffle(data); D = list(data);
        steps.push(step('Add the values: ' + sum(data) + '.', '', 1), step('Divide by how many values there are (5).', String(sum(data) / 5), 2));
        return out('ce1', 'Find the mean of the ' + cx[0] + ': ' + M(D) + '.', [{ answer: M(String(sum(data) / 5)), check: { type: 'stat', want: 'mean', data: D } }], steps); }
      if (c === 2) { var n2 = r.pick([6, 8]); data = rnd(r, n2, 1, 30); D = list(data); var md = median(data);
        steps.push(step('Order the values.', list(sorted(data)), 1), step('With an even count, the median is the mean of the two middle values.', dec(md), 2));
        return out('ce2', 'Find the median of the ' + cx[0] + ': ' + M(D) + '.', [{ answer: M(dec(md)), check: { type: 'stat', want: 'median', data: D } }], steps); }
      if (c === 3) { var n3 = r.int(5, 7), m3 = r.int(70, 92); data = rnd(r, n3 - 1, 60, 100); var miss = m3 * n3 - sum(data); need(miss >= 50 && miss <= 100); D = list(data);
        steps.push(step('The total of all ' + n3 + ' scores is ' + n3 + ' × ' + m3 + ' = ' + n3 * m3 + '.', '', 2), step('Subtract the scores you know (' + sum(data) + ').', String(miss), 2));
        return out('ce3', 'The mean of ' + n3 + ' test scores is ' + m3 + '. Here are ' + (n3 - 1) + ' of the scores: ' + M(D) + '. What is the missing score?', [{ answer: M(String(miss)), check: { type: 'stat', want: 'missing', data: D, count: 0, mean: 1 } }], steps); }
      if (c === 4) { var lo = r.int(0, 4), counts = {}, vals = []; for (var v = lo; v <= lo + 8; v++) { var k = r.int(0, 4); if (k) { counts[v] = k; for (var j = 0; j < k; j++) vals.push(v); } }
        need(vals.length >= 9 && vals.length <= 18); var best = 0, modes = []; Object.keys(counts).forEach(function (kk) { if (counts[kk] > best) { best = counts[kk]; modes = [+kk]; } else if (counts[kk] === best) modes.push(+kk); }); need(modes.length === 1 && best >= 2);
        var fig = { kind: 'dotplot', min: lo, max: lo + 8, counts: counts, label: cx[0] };
        steps.push(step('Read every dot as one value (' + vals.length + ' values).', '', 1), step('Mean = total ÷ count; median = middle of the ordered values; mode = the tallest stack.', '', 2));
        var rd4 = !exact(mean(vals), 1), ck4 = { type: 'stat', want: 'mean' }; if (rd4) ck4.round = 1;
        return out('ce4', 'The dot plot shows ' + cx[0] + '.', [{ label: 'a', prompt: 'Find the mean.' + (rd4 ? ' Round to the nearest tenth.' : ''), answer: M(dec(rd4 ? r1(mean(vals)) : mean(vals))), check: ck4 },
          { label: 'b', prompt: 'Find the median.', answer: M(dec(median(vals))), check: { type: 'stat', want: 'median' } }, { label: 'c', prompt: 'Find the mode.', answer: M(String(modes[0])), check: { type: 'stat', want: 'mode' } }], steps, fig); }
      if (c === 5) { data = rnd(r, r.pick([4, 9]), 10, 40); var add = r.int(41, 80); var nm = mean(data.concat([add])); need(exact(nm, 1)); D = list(data);
        steps.push(step('Old total: ' + sum(data) + '. New total: ' + (sum(data) + add) + '.', '', 1), step('Divide by the new count (' + (data.length + 1) + ').', dec(nm), 2));
        return out('ce5', 'The data set is ' + M(D) + '. The value ' + add + ' is added to the data set.', [{ label: 'a', prompt: 'Find the new mean.', answer: M(dec(nm)), check: { type: 'stat', want: 'newmean', data: D, add: 0 } }, { label: 'b', prompt: 'Find the new median.', answer: M(dec(median(data.concat([add])))), check: { type: 'stat', want: 'newmean', stat: 'median', data: D, add: 0 } }], steps); }
      if (c === 6) { var n6 = r.pick([4, 5, 8]), m6 = r.int(8, 22); data = rnd(r, n6 - 1, 2, 30); var l6 = n6 * m6 - sum(data); need(l6 >= 1 && l6 <= 35); data.push(l6); data = r.shuffle(data); need(exact(mad(data), 2)); D = list(data); var mm = mean(data), mv = mad(data), rnd1 = !exact(mv, 1);
        steps.push(step('Mean: ' + mm + '.', '', 1), step('Distances from the mean: ' + M(list(data.map(function (x) { return Math.abs(x - mm); }))) + '.', '', 2), step('MAD = mean of the distances.', dec(rnd1 ? r1(mv) : mv), 2));
        return out('ce6', 'Find the mean absolute deviation (MAD) of ' + M(D) + '.' + (rnd1 ? ' Round to the nearest tenth.' : ''), [{ answer: M(dec(rnd1 ? r1(mv) : mv)), check: rnd1 ? { type: 'stat', want: 'mad', data: D, round: 1 } : { type: 'stat', want: 'mad', data: D } }], steps); }
      var mk7 = function (lo, hi) { var a = rnd(r, 4, lo, hi), mm7 = r.int(70, 90), l = 5 * mm7 - sum(a); need(l >= 55 && l <= 100); a.push(l); return r.shuffle(a); }, A = mk7(60, 100), Bd = mk7(75, 92); if (r.chance(0.5)) { var tmp = A; A = Bd; Bd = tmp; } need(Math.abs(mad(A) - mad(Bd)) >= 2);
      var DA = list(A), DB = list(Bd), lab = r.pick([['Class A', 'Class B'], ['Team Red', 'Team Blue'], ['Monday', 'Friday']]), more = mad(A) > mad(Bd) ? lab[0] : lab[1];
      steps.push(step('Find each mean, then each MAD: ' + lab[0] + ' ' + dec(mad(A)) + ', ' + lab[1] + ' ' + dec(mad(Bd)) + '.', '', 3), step('The greater MAD means the values are more spread out.', '', 1));
      return out('ce7', 'Scores for ' + lab[0] + ': ' + M(DA) + '. Scores for ' + lab[1] + ': ' + M(DB) + '.', [{ label: 'a', prompt: 'Find the MAD for ' + lab[0] + '.', answer: M(dec(mad(A))), check: { type: 'stat', want: 'mad', data: DA } },
        { label: 'b', prompt: 'Find the MAD for ' + lab[1] + '.', answer: M(dec(mad(Bd))), check: { type: 'stat', want: 'mad', data: DB } },
        { label: 'c', prompt: 'Which group’s scores are more spread out? Give both MADs.', answer: more + ' (MADs ' + M(dec(mad(A))) + ' and ' + M(dec(mad(Bd))) + ')', check: { type: 'stat', want: 'compare-mad', data: DA, data2: DB, labels: lab } }], steps);
    }
  });
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }
  function out(variant, prompt, parts, steps, fig) { return { variant: variant, prompt: prompt, fig: fig || null, parts: parts, steps: steps, space: [0.7, 0.9, 1.1] }; }

  /* ================= SPREAD · range, quartiles, IQR, outliers ================= */
  skill({
    id: 'spread', best: [0, 1, 2], tag: 'SPREAD', name: 'Range, quartiles, IQR and outliers',
    blurb: 'Range and IQR (CP2) → the five-number summary, outliers by the 1.5 × IQR rule (CP1) → mean or median, the effect of an outlier, fences (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 3, 2, 4, 6, 5, 7][ctx.c], steps = [], n = c <= 2 ? r.pick([7, 9]) : c === 3 ? r.pick([8, 10]) : r.int(8, 11), data = rnd(r, n, 10, 50), D, q;
      if (c >= 4 && (c >= 5 || r.chance(0.6))) data[r.int(0, n - 1)] = r.chance(0.5) ? r.int(80, 120) : r.int(-30, -5) + 10;
      D = list(data); q = quart(data); var iqr = q[3] - q[1], ol = outl(data);
      steps.push(step('Order the data.', list(sorted(data)), 1));
      if (c === 1) { steps.push(step('Range = greatest − least.', String(q[4] - q[0]), 2)); return out('sp1', 'Find the range of ' + M(D) + '.', [{ answer: M(String(q[4] - q[0])), check: { type: 'stat', want: 'range', data: D } }], steps); }
      if (c === 2) { steps.push(step('The median splits the data; Q1 and Q3 are the medians of the lower and upper halves.', list(q), 3));
        return out('sp2', 'Find the five-number summary (minimum, Q1, median, Q3, maximum) of ' + M(D) + '.', [{ answer: M(list(q)), check: { type: 'stat', want: 'five', data: D } }], steps); }
      if (c === 3) { steps.push(step('Q1 = ' + dec(q[1]) + ', Q3 = ' + dec(q[3]) + '.', '', 2), step('IQR = Q3 − Q1.', dec(iqr), 1));
        return out('sp3', 'Find the interquartile range (IQR) of ' + M(D) + '.', [{ answer: M(dec(iqr)), check: { type: 'stat', want: 'iqr', data: D } }], steps); }
      var lo = q[1] - 1.5 * iqr, hi = q[3] + 1.5 * iqr;
      steps.push(step('Q1 = ' + dec(q[1]) + ', Q3 = ' + dec(q[3]) + ', IQR = ' + dec(iqr) + '.', '', 1), step('Fences: ' + M('Q1-1.5\\cdot IQR=' + dec(lo)) + ' and ' + M('Q3+1.5\\cdot IQR=' + dec(hi)) + '.', '', 2));
      var olAns = ol.length ? sorted(ol).map(function (x) { return M(String(x)); }).join(' and ') : 'None';
      if (c === 4) { steps.push(step('Values outside the fences are outliers.', '', 1));
        return out('sp4', 'Use the 1.5 × IQR rule to find any outliers in ' + M(D) + '. If there are none, write “none.”', [{ answer: olAns, check: { type: 'stat', want: 'outliers', data: D } }], steps); }
      need(ol.length === 1);
      if (c === 5) { var wo = data.filter(function (x) { return x !== ol[0]; }), rA = !exact(mean(data), 1), rB = !exact(mean(wo), 1), kA = { type: 'stat', want: 'mean', data: D }, kB = { type: 'stat', want: 'without', data: D }; if (rA) kA.round = 1; if (rB) kB.round = 1;
        steps.push(step('The outlier is ' + ol[0] + '. Remove it and recompute.', '', 1));
        return out('sp5', 'The data set ' + M(D) + ' has one outlier.', [{ label: 'a', prompt: 'Find the outlier.', answer: M(String(ol[0])), check: { type: 'stat', want: 'outliers', data: D } },
          { label: 'b', prompt: 'Find the mean with the outlier.' + (rA ? ' Round to the nearest tenth.' : ''), answer: M(dec(rA ? r1(mean(data)) : mean(data))), check: kA },
          { label: 'c', prompt: 'Find the mean without the outlier.' + (rB ? ' Round to the nearest tenth.' : ''), answer: M(dec(rB ? r1(mean(wo)) : mean(wo))), check: kB }], steps); }
      if (c === 6) { steps.push(step('The data have an outlier (' + ol[0] + '), which pulls the mean; the median resists it.', '', 2));
        return out('sp6', 'The data set is ' + M(D) + '.', [{ label: 'a', prompt: 'Which better describes the center: the mean or the median? Explain.', answer: 'Median, because the data have an outlier (' + M(String(ol[0])) + ') that pulls the mean.', check: { type: 'stat', want: 'better', data: D } },
          { label: 'b', prompt: 'Find that measure.', answer: M(dec(q[2])), check: { type: 'stat', want: 'median', data: D } }], steps); }
      return out('sp7', 'For the data ' + M(D) + ':', [{ label: 'a', prompt: 'Find the lower and upper fences, ' + M('Q1-1.5\\cdot IQR') + ' and ' + M('Q3+1.5\\cdot IQR') + '.', answer: M(dec(lo)) + ' and ' + M(dec(hi)), check: { type: 'stat', want: 'fences', data: D } },
        { label: 'b', prompt: 'Which values are outliers?', answer: olAns, check: { type: 'stat', want: 'outliers', data: D } }], steps);
    }
  });

  /* ================= DISPLAY · box plots ================= */
  skill({
    id: 'boxplot', best: [0, 1, 2], tag: 'DISPLAY', name: 'Read and compare box plots',
    blurb: 'The median from a box plot (CP2) → quartiles, IQR, range, the percent of data between values (CP1) → compare two box plots by median, IQR and spread (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], cx = r.pick([['test scores', 50, 100, 5], ['heights (inches)', 50, 75, 1], ['minutes to get to school', 0, 60, 5], ['daily high temperatures (°F)', 40, 90, 5]]);
      var mk = function () { var st = cx[3], lo = cx[1], hi = cx[2], k = (hi - lo) / st; var t = [r.int(0, 2), 0, 0, 0, 0]; t[1] = t[0] + r.int(1, 3); t[2] = t[1] + r.int(1, 3); t[3] = t[2] + r.int(1, 3); t[4] = t[3] + r.int(1, 3); need(t[4] <= k); return t.map(function (x) { return lo + x * st; }); };
      var A = mk(), lab = r.pick([['Class A', 'Class B'], ['Morning', 'Evening'], ['Last year', 'This year']]), boxes = [{ label: c >= 5 ? lab[0] : '', q: A }], B = null;
      if (c >= 5) { B = mk(); boxes.push({ label: lab[1], q: B }); }
      var fig = { kind: 'boxplot', min: cx[1], max: cx[2], step: cx[3], boxes: boxes };
      var nm = { min: 'minimum', q1: 'first quartile (Q1)', median: 'median', q3: 'third quartile (Q3)', max: 'maximum', range: 'range', iqr: 'interquartile range (IQR)' };
      var val = function (q, w) { return { min: q[0], q1: q[1], median: q[2], q3: q[3], max: q[4], range: q[4] - q[0], iqr: q[3] - q[1] }[w]; };
      var ask = function (w, lbl) { return { label: lbl || '', prompt: 'Find the ' + nm[w] + '.', answer: M(String(val(A, w))), check: { type: 'stat-box', want: w } }; };
      steps.push(step('Box plot parts: whisker ends are the minimum and maximum, the box edges are Q1 and Q3, the line in the box is the median.', '', 2));
      if (c === 1) return out('bp1', 'The box plot shows ' + cx[0] + '. Find the median.', [{ answer: M(String(A[2])), check: { type: 'stat-box', want: 'median' } }], steps, fig);
      if (c === 2) return out('bp2', 'The box plot shows ' + cx[0] + '.', [ask('q1', 'a'), ask('q3', 'b')], steps, fig);
      if (c === 3) { steps.push(step('IQR = Q3 − Q1; range = maximum − minimum.', '', 1)); return out('bp3', 'The box plot shows ' + cx[0] + '.', [ask('median', 'a'), ask('iqr', 'b'), ask('range', 'c')], steps, fig); }
      if (c === 4) { var pr = r.pick([['q1', 'max', 75], ['min', 'q3', 75], ['median', 'max', 50], ['q1', 'q3', 50], ['min', 'median', 50], ['q3', 'max', 25]]);
        steps.push(step('Each section of a box plot holds about 25% of the data.', '', 2));
        return out('bp4', 'The box plot shows ' + cx[0] + '.', [{ label: 'a', prompt: 'About what percent of the data are between ' + M(String(val(A, pr[0]))) + ' and ' + M(String(val(A, pr[1]))) + '?', answer: pr[2] + '%', check: { type: 'stat-box', want: 'percent', from: pr[0], to: pr[1], fromTeX: String(val(A, pr[0])), toTeX: String(val(A, pr[1])) } }, ask('iqr', 'b')], steps, fig); }
      var fs = function (q, st) { return st === 'iqr' ? q[3] - q[1] : st === 'range' ? q[4] - q[0] : q[2]; };
      var cmp = function (st, lbl, withDiff) { var fa = fs(A, st), fb = fs(B, st); need(fa !== fb); var big = fa > fb ? lab[0] : lab[1];
        return { label: lbl, prompt: 'Which group has the greater ' + nm[st] + '?' + (withDiff ? ' By how much?' : st === 'iqr' ? ' Which group is more consistent?' : ''),
          answer: withDiff ? big + ', by ' + M(String(Math.abs(fa - fb))) : big + (st === 'iqr' ? ' has the greater IQR, so ' + (big === lab[0] ? lab[1] : lab[0]) + ' is more consistent.' : ' has the greater ' + nm[st] + '.'), check: { type: 'stat-box', want: 'compare', stat: st, diff: !!withDiff } }; };
      var askB = function (w, lbl) { return { label: lbl, prompt: 'Find the ' + nm[w] + ' of ' + lab[1] + '.', answer: M(String(val(B, w))), check: { type: 'stat-box', want: w, box: 1 } }; };
      steps.push(step('Compare the same part of each box plot: the median line, the box width (IQR) or the whisker-to-whisker length (range).', '', 2));
      var intro = 'The box plots compare ' + cx[0] + ' for ' + lab[0] + ' and ' + lab[1] + '.';
      if (c === 5) return out('bp5', intro, [cmp('median', 'a', true), { label: 'b', prompt: 'Find the IQR of ' + lab[0] + '.', answer: M(String(A[3] - A[1])), check: { type: 'stat-box', want: 'iqr' } }], steps, fig);
      if (c === 6) return out('bp6', intro, [cmp('iqr', 'a'), askB('range', 'b'), askB('median', 'c')], steps, fig);
      return out('bp7', intro, [cmp('median', 'a', true), cmp('iqr', 'b'), askB('q3', 'c')], steps, fig);
    }
  });

  /* ================= TWOWAY · two-way tables ================= */
  var TW = [['Ninth graders', 'Tenth graders', 'Plays a sport', 'No sport', 'students'], ['Cats', 'Dogs', 'Indoor pet', 'Outdoor pet', 'pets'], ['Juniors', 'Seniors', 'Drives to school', 'Takes the bus', 'students'], ['Adults', 'Teens', 'Prefers movies', 'Prefers games', 'people']];
  skill({
    id: 'twoway', best: [0, 1, 2], tag: 'TWOWAY', name: 'Two-way tables and relative frequency',
    blurb: 'Joint and marginal relative frequencies, completing a table (CP2) → conditional relative frequencies (CP1) → rounding, is there an association? (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 2, 3, 1, 4, 5, 6, 7][ctx.c], steps = [], t = r.pick(TW), goodTot = [20, 25, 40, 50, 100];
      var a = r.int(3, 30), b = r.int(3, 30), d = r.int(3, 30), e = r.int(3, 30);
      if (c <= 5 && c >= 2) { var tot = r.pick([50, 100, 200]); need(a + b + d + e < tot); e = tot - a - b - d; need(e >= 3); }
      if (c === 4) { var rt = r.pick(goodTot); need(rt > 4); a = r.int(2, rt - 2); b = rt - a; }
      if (c === 5) { var ct = r.pick(goodTot); a = r.int(2, ct - 2); d = ct - a; need(d >= 2); e = r.int(3, 40); b = r.int(3, 40); }
      if (c === 7) { var p1 = r.chance(0.5) ? r.pick([0.2, 0.3, 0.4]) : 0.5, p2 = r.chance(0.5) ? p1 : p1 + r.pick([0.2, 0.3, 0.4]); var n1 = r.pick([40, 50, 60]), n2 = r.pick([40, 50, 60]); a = Math.round(n1 * p1) + r.int(-1, 1); b = n1 - a; d = Math.round(n2 * Math.min(p2, 0.9)) + r.int(-1, 1); e = n2 - d; need(b > 0 && e > 0); }
      var rows = [[a, b], [d, e]], R = [a + b, d + e], Cc = [a + d, b + e], T = a + b + d + e;
      var cells = [[a, b, R[0]], [d, e, R[1]], [Cc[0], Cc[1], T]], blank = cells.map(function (rw) { return rw.slice(); });
      var fig = function (cs) { return { kind: 'twoway', corner: '', cols: [t[2], t[3], 'Total'], rows: [{ label: t[0], cells: cs[0] }, { label: t[1], cells: cs[1] }, { label: 'Total', cells: cs[2] }] }; };
      if (c === 1) { var hide = r.shuffle([[0, 0], [0, 1], [1, 0], [1, 1], [0, 2], [1, 2], [2, 0], [2, 1]]).slice(0, 2).sort(function (x, y) { return x[0] - y[0] || x[1] - y[1]; });
        hide.forEach(function (h) { blank[h[0]][h[1]] = '?'; });
        var vals = hide.map(function (h) { return cells[h[0]][h[1]]; });
        steps.push(step('Each row adds to its total, and each column adds to its total.', '', 2), step('Use a row or column with only one missing value first.', '', 1));
        return out('tw1', 'Complete the two-way table about ' + t[4] + '. List the missing values from left to right, top to bottom.', [{ answer: vals.map(function (v) { return M(String(v)); }).join(', '), check: { type: 'twoway', want: 'fill' } }], steps, fig(blank)); }
      var F2 = fig(cells), pc = function (x, y) { return x / y * 100; };
      if (c === 2 || c === 3) { var ri = r.int(0, 1), cj = r.int(0, 1), joint = c === 2;
        var val = joint ? pc(rows[ri][cj], T) : r.chance(0.5) ? pc(R[ri], T) : pc(Cc[cj], T), useRow = !joint && val === pc(R[ri], T);
        need(exact(val, 0) || exact(val, 1));
        steps.push(step(joint ? 'Joint relative frequency = cell ÷ grand total.' : 'Marginal relative frequency = row or column total ÷ grand total.', '', 2), step('Write it as a percent.', dec(val) + '\\%', 1));
        var q = joint ? 'What percent of all the ' + t[4] + ' are in the group “' + t[ri] + '” and “' + t[2 + cj] + '”?' : 'What percent of all the ' + t[4] + ' are ' + (useRow ? 'in the group “' + t[ri] + '”' : '“' + t[2 + cj] + '”') + '?';
        var chk = joint ? { type: 'twoway', want: 'joint', row: t[ri], col: t[2 + cj] } : useRow ? { type: 'twoway', want: 'marginal', row: t[ri] } : { type: 'twoway', want: 'marginal', col: t[2 + cj] };
        return out('tw' + c, 'The two-way table shows data about ' + t[4] + '. ' + q, [{ answer: dec(val) + '%', check: chk }], steps, F2); }
      if (c === 4 || c === 5 || c === 6) { var byRow = c !== 5, i4 = c === 4 ? 0 : r.int(0, 1), j4 = c === 5 ? 0 : r.int(0, 1), v4 = byRow ? pc(rows[i4][j4], R[i4]) : pc(rows[i4][j4], Cc[j4]), round = !exact(v4, 1);
        if (c !== 6) need(!round);
        steps.push(step('Conditional relative frequency: divide by the total of the group you are told about (' + (byRow ? t[i4] : t[2 + j4]) + ': ' + (byRow ? R[i4] : Cc[j4]) + ').', '', 2), step('Write it as a percent' + (round ? ' and round.' : '.'), dec(round ? r1(v4) : v4) + '\\%', 1));
        var q4 = byRow ? 'Of the ' + t[4] + ' in the group “' + t[i4] + '”, what percent are “' + t[2 + j4] + '”?' : 'Of the ' + t[4] + ' who are “' + t[2 + j4] + '”, what percent are in the group “' + t[i4] + '”?';
        var ck = { type: 'twoway', want: byRow ? 'cond-row' : 'cond-col', row: t[i4], col: t[2 + j4] }; if (round) ck.round = 1;
        return out('tw' + c, 'The two-way table shows data about ' + t[4] + '. ' + q4 + (round ? ' Round to the nearest tenth of a percent.' : ''), [{ answer: dec(round ? r1(v4) : v4) + '%', check: ck }], steps, F2); }
      var P1 = pc(a, R[0]), P2 = pc(d, R[1]), diff = Math.abs(P1 - P2); need(diff <= 5 || diff >= 15);
      var yes = diff >= 15;
      steps.push(step('Compare the conditional relative frequencies of “' + t[2] + '” in each row: ' + Math.round(P1 + 1e-9) + '% and ' + Math.round(P2 + 1e-9) + '%.', '', 2), step(yes ? 'They are very different, so there is an association.' : 'They are about the same, so there is no clear association.', '', 2));
      return out('tw7', 'The two-way table shows data about ' + t[4] + '. Is there an association between the group (' + t[0] + ' or ' + t[1] + ') and “' + t[2] + '”? Support your answer with the percent of each group, rounded to the nearest percent.',
        [{ answer: (yes ? 'Yes: ' : 'No: ') + Math.round(P1 + 1e-9) + '% of ' + t[0] + ' and ' + Math.round(P2 + 1e-9) + '% of ' + t[1] + ' are “' + t[2] + '”.', check: { type: 'twoway', want: 'assoc', rows: [t[0], t[1]], col: t[2] } }], steps, F2);
    }
  });

  /* ================= SCATTER · correlation, lines of fit, residuals ================= */
  var SC = [['Hours studied', 'Test score', 0, 10, 1, 40, 100, 10, 'hour of study', 'points', 'hours studied', 'the test score'], ['Temperature (°F)', 'Drinks sold', 50, 100, 5, 0, 120, 20, 'degree', 'drinks', 'the temperature', 'drinks sold'], ['Practice (hours)', 'Free throws made', 0, 10, 1, 0, 50, 5, 'hour of practice', 'free throws', 'hours of practice', 'free throws made'], ['Age of car (years)', 'Value ($1000s)', 0, 12, 1, 0, 40, 5, 'year', 'thousand dollars', 'the age of the car', 'the value of the car']];
  skill({
    id: 'scatter', best: [0, 1, 2], tag: 'SCATTER', name: 'Scatter plots, lines of fit and residuals',
    blurb: 'Positive, negative or no correlation, the line through two points (CP2) → predictions and residuals (CP1) → interpreting slope and intercept, over- or under-estimates, two-part models (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 4, 2, 3, 5, 6, 7][ctx.c], steps = [], s = r.pick(SC), neg = /Age of car/.test(s[0]);
      var span = s[3] - s[2], yspan = s[6] - s[5];
      var m = (neg ? -1 : 1) * r.pick([0.5, 1, 1.5, 2, 2.5, 3, 4, 5]) * (yspan / span) / 4, b;
      m = Math.round(m * 2) / 2; need(m !== 0);
      b = Math.round(s[5] + yspan * (neg ? 0.85 : 0.15) - m * s[2]);
      var line = 'y=' + (m === 1 ? '' : m === -1 ? '-' : dec(m)) + 'x' + (b ? (b < 0 ? '-' : '+') + Math.abs(b) : ''), f = function (x) { return m * x + b; };
      var pts = [];
      for (var i = 0; i < 10; i++) { var x = s[2] + Math.round((span * (i + 0.5) / 10) / s[4]) * s[4]; var y = Math.round(f(x) + r.int(-1, 1) * yspan / 12); if (y >= s[5] && y <= s[6]) pts.push([x, y]); }
      need(pts.length >= 7);
      var fig = { kind: 'scatter', xmin: s[2], xmax: s[3], xstep: s[4] * (span / s[4] > 12 ? 2 : 1), ymin: s[5], ymax: s[6], ystep: s[7], xlabel: s[0], ylabel: s[1], points: pts };
      if (c === 1) { var kind = r.pick(['positive', 'negative', 'no']); if (kind === 'no') { var pat = r.pick([[0,8,7,1,9,2,4,5,6,3],[2,7,6,9,1,4,0,3,8,5],[0,9,7,2,4,5,8,3,1,6],[6,1,5,8,0,7,2,9,4,3],[1,0,8,9,6,7,3,5,4,2],[8,6,0,1,3,5,9,2,7,4],[1,5,3,4,9,6,7,8,0,2],[3,7,0,9,5,4,1,8,6,2]]);
          fig.points = []; for (var k1 = 0; k1 < 10; k1++) fig.points.push([s[2] + Math.round((span * (k1 + 0.5) / 10) / s[4]) * s[4], s[5] + Math.round(yspan * (0.15 + 0.07 * pat[k1]))]); }
        else if ((kind === 'negative') !== (m < 0)) fig.points = pts.map(function (p) { return [s[2] + s[3] - p[0], p[1]]; });
        steps.push(step('Look at the overall pattern from left to right.', '', 1), step('Rising: positive. Falling: negative. No pattern: no correlation.', '', 2));
        return out('sc1', 'Describe the correlation shown in the scatter plot.', [{ answer: (kind === 'no' ? 'No' : kind.charAt(0).toUpperCase() + kind.slice(1)) + ' correlation', check: { type: 'scatter-corr' } }], steps, fig); }
      var xs = s[2] + r.int(1, Math.floor(span / s[4]) - 1) * s[4], yhat = f(xs);
      if (c === 2) { steps.push(step('Substitute x = ' + xs + ' into the line of fit.', 'y=' + dec(yhat), 2));
        return out('sc2', 'The line of fit for the data is ' + M(line) + ', where x is ' + s[10] + ' and y is ' + s[11] + '. Predict y when ' + M('x=' + xs) + '.', [{ answer: M('y=' + dec(yhat)), check: { type: 'stat-line', rule: line, want: 'predict', at: String(xs) } }], steps, fig); }
      var pt = pts[r.int(0, pts.length - 1)], res = pt[1] - f(pt[0]); need(res !== 0);
      var ptTeX = '(' + pt[0] + ',\\ ' + pt[1] + ')';
      if (c === 3) { steps.push(step('Predicted value: ' + M('y=' + dec(f(pt[0]))) + '.', '', 1), step('Residual = actual − predicted.', dec(res), 2));
        return out('sc3', 'The line of fit is ' + M(line) + '. One data point is ' + M(ptTeX) + '.', [{ label: 'a', prompt: 'What does the line predict for ' + M('x=' + pt[0]) + '?', answer: M('y=' + dec(f(pt[0]))), check: { type: 'stat-line', rule: line, want: 'predict', at: String(pt[0]) } },
          { label: 'b', prompt: 'Find the residual for this data point.', answer: M(dec(res)), check: { type: 'stat-line', rule: line, want: 'residual', x: String(pt[0]), y: String(pt[1]) } }], steps, fig); }
      if (c === 4 || c === 7) { var x1 = s[2] + s[4] * r.int(1, 2), x2 = s[3] - s[4] * r.int(1, 2), y1 = f(x1), y2 = f(x2);
        var pairs = '(' + x1 + ',\\ ' + dec(y1) + '),\\ (' + x2 + ',\\ ' + dec(y2) + ')';
        fig.line = [[x1, y1], [x2, y2]];
        steps.push(step('Slope from the two points: ' + M('m=\\frac{' + y2 + '-' + (y1 < 0 ? '(' + y1 + ')' : y1) + '}{' + x2 + '-' + x1 + '}=' + dec(m)) + '.', '', 2), step('Find b and write the equation.', line, 2));
        var p4 = { answer: M(line), check: { type: 'linear-rule', pairs: pairs } };
        if (c === 4) return out('sc4', 'A line of fit passes through ' + M(pairs) + '. Write its equation in slope-intercept form.', [p4], steps, fig);
        steps.push(step('(b) Substitute x = ' + xs + '.', 'y=' + dec(yhat), 1));
        steps.push(step('(c) The slope is the change in ' + s[11] + ' for each 1-unit increase in ' + s[10] + '.', '', 1));
        return out('sc7', 'A line of fit for the data passes through ' + M(pairs) + '.', [{ label: 'a', prompt: 'Write the equation of the line.', answer: p4.answer, check: p4.check },
          { label: 'b', prompt: 'Use your line to predict y when ' + M('x=' + xs) + '.', answer: M('y=' + dec(yhat)), check: { type: 'linear-rule', pairs: pairs, predict: String(xs) } },
          { label: 'c', prompt: 'Find the residual for the data point ' + M(ptTeX) + ' using your line.', answer: M(dec(res)), check: { type: 'stat-line', pairs: pairs, want: 'residual', x: String(pt[0]), y: String(pt[1]) } },
          { label: 'd', prompt: 'Interpret the slope in this situation.', answer: 'For each additional ' + s[8] + ', ' + s[11] + ' ' + (m > 0 ? 'increases' : 'decreases') + ' by about ' + M(dec(Math.abs(m))) + ' ' + s[9] + '.', check: { type: 'stat-line', pairs: pairs, want: 'slope' } }], steps, fig); }
      if (c === 5) { var unitY = s[9], unitX = s[8]; need(s[2] === 0 && b >= 0);
        steps.push(step('The slope is the change in y for each 1-unit increase in x.', '', 2), step('Say it in words with units.', '', 1));
        return out('sc5', 'The line of fit ' + M(line) + ' models ' + s[11] + ' (y) from ' + s[10] + ' (x).',
          [{ label: 'a', prompt: 'Interpret the slope.', answer: 'For each additional ' + unitX + ', ' + s[11] + ' ' + (m > 0 ? 'increases' : 'decreases') + ' by about ' + M(dec(Math.abs(m))) + ' ' + unitY + '.', check: { type: 'stat-line', rule: line, want: 'slope' } },
           { label: 'b', prompt: 'Interpret the y-intercept.', answer: 'When ' + s[10] + ' is ' + M('0') + ', the model predicts ' + s[11] + ' of about ' + M(dec(b)) + ' ' + s[9] + '.', check: { type: 'stat-line', rule: line, want: 'intercept' } }], steps, fig); }
      var word = res > 0 ? 'underestimates' : 'overestimates';
      steps.push(step('Predicted: ' + dec(f(pt[0])) + '. Actual: ' + pt[1] + '.', '', 1), step('A positive residual means the line is too low (underestimate); a negative residual means it is too high (overestimate).', dec(res), 2));
      return out('sc6', 'The line of fit is ' + M(line) + '. One data point is ' + M(ptTeX) + '.', [{ label: 'a', prompt: 'What does the line predict for ' + M('x=' + pt[0]) + '?', answer: M('y=' + dec(f(pt[0]))), check: { type: 'stat-line', rule: line, want: 'predict', at: String(pt[0]) } },
        { label: 'b', prompt: 'Find the residual.', answer: M(dec(res)), check: { type: 'stat-line', rule: line, want: 'residual', x: String(pt[0]), y: String(pt[1]) } },
        { label: 'c', prompt: 'Does the line overestimate or underestimate the actual value?', answer: 'It ' + word + '; the residual is ' + M(dec(res)) + '.', check: { type: 'stat-line', rule: line, want: 'over-under', x: String(pt[0]), y: String(pt[1]) } }], steps, fig);
    }
  });

  /* ================= SPREAD · standard deviation (population, σ) ================= */
  function sd(a) { var m = mean(a); return Math.sqrt(mean(a.map(function (x) { return (x - m) * (x - m); }))); }
  function rTo(x, k) { var s = Math.pow(10, k); return Math.round(x * s + 1e-9) / s; }
  function safeRound(x, k) { var s = Math.pow(10, k), f = x * s - Math.floor(x * s); return Math.abs(f - 0.5) > 1e-6; }
  var ROUND = ['to the nearest whole number', 'to the nearest tenth', 'to the nearest hundredth'];
  skill({
    id: 'stdev', best: [1, 2], tag: 'SPREAD', name: 'Standard deviation',
    blurb: 'Which data set is more spread out (CP2) → the standard deviation of a small data set (CP1) → adding to or multiplying every value, data from a dot plot (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], cx = r.pick(CTX), data, D, k = c <= 3 ? 1 : 2;
      var sdNote = ' Use the population standard deviation, ⟨\\sigma⟩.';
      if (c === 1) {
        var ctr = r.int(10, 20), A = [], B = [];
        for (var i = 0; i < 5; i++) { A.push(ctr + r.int(-2, 2)); B.push(ctr + r.int(-9, 9)); }
        need(Math.abs(sd(A) - sd(B)) > 1.5); var lab = r.chance(0.5) ? ['Class A', 'Class B'] : ['Class B', 'Class A'];
        var DA = list(A), DB = list(B), more = sd(A) > sd(B) ? lab[0] : lab[1];
        steps.push(step('Standard deviation measures how far the values typically are from the mean.', '', 1), step('The values of ' + more + ' are more spread out.', '', 2));
        return out('sd-cmp', lab[0] + ': ' + M(DA) + '. ' + lab[1] + ': ' + M(DB) + '. Which data set has the larger standard deviation? Explain without calculating.',
          [{ answer: more + ': its values are more spread out from the mean.', check: { type: 'stat', want: 'sd-compare', data: DA, data2: DB, labels: lab } }], steps);
      }
      var n = c === 2 ? 4 : c === 3 ? 5 : r.int(6, 8);
      data = rnd(r, n, 1, c <= 3 ? 20 : 60); D = list(data); var s0 = sd(data); need(s0 > 0.5 && safeRound(s0, k));
      if (c <= 4) {
        steps.push(step('Find the mean: ' + dec(rTo(mean(data), 3)) + '.', '', 1), step('Square each distance from the mean and find the mean of the squares (the variance).', '', 2), step('Take the square root: ⟨\\sigma\\approx ' + rTo(s0, k) + '⟩.', '', 2));
        return out('sd' + c, 'Find the standard deviation of the ' + cx[0] + ': ' + M(D) + '.' + sdNote + ' Round ' + ROUND[k] + '.',
          [{ answer: 'σ ≈ ' + M(String(rTo(s0, k))), check: { type: 'stat', want: 'sd', data: D, round: k } }], steps);
      }
      if (c === 5 || c === 6) {
        var add = c === 5, kk = add ? r.int(2, 15) : r.int(2, 5), s1 = add ? s0 : s0 * kk; need(safeRound(s1, k));
        steps.push(step('The standard deviation of the data is about ' + rTo(s0, 3) + '.', '', 1));
        steps.push(step(add ? 'Adding the same number to every value moves the data but does not spread it out, so σ stays the same.' : 'Multiplying every value by ' + kk + ' multiplies every distance from the mean by ' + kk + ', so σ is ' + kk + ' times as large.', '', 3));
        return out('sd-' + (add ? 'add' : 'mul'), 'Here are the ' + cx[0] + ': ' + M(D) + '. ' + (add ? 'Every value is increased by ' + kk + '.' : 'Every value is multiplied by ' + kk + '.') + ' What is the standard deviation of the new data?' + sdNote + ' Round ' + ROUND[k] + '.',
          [{ answer: 'σ ≈ ' + M(String(rTo(s1, k))), check: { type: 'stat', want: 'sd', data: D, round: k, transform: add ? 'add' : 'mul' } }], steps);
      }
      var lo = r.int(0, 4), counts = {}, vals = []; for (var v = lo; v <= lo + 8; v++) { var cnt = r.int(0, 4); if (cnt) { counts[v] = cnt; for (var j = 0; j < cnt; j++) vals.push(v); } }
      need(vals.length >= 10 && vals.length <= 22); var s7 = sd(vals); need(safeRound(s7, 2));
      steps.push(step('Read every value from the dot plot (' + vals.length + ' values).', '', 1), step('Find the mean, then the mean of the squared distances, then the square root.', '\\sigma\\approx ' + rTo(s7, 2), 3));
      return out('sd-dot', 'The dot plot shows the ' + cx[0] + ' for a group. Find the standard deviation of the data.' + sdNote + ' Round to the nearest hundredth.',
        [{ answer: 'σ ≈ ' + M(String(rTo(s7, 2))), check: { type: 'stat', want: 'sd', round: 2 } }], steps, { kind: 'dotplot', min: lo, max: lo + 8, counts: counts, label: cx[0] });
    }
  });

  /* ================= DISPLAY · histograms ================= */
  var HCTX = [['Test scores', 50, 10], ['Minutes of exercise', 0, 15], ['Heights of plants (cm)', 10, 5], ['Commute time (minutes)', 0, 10], ['Points per game', 0, 5], ['Ages of museum visitors', 10, 10]];
  skill({
    id: 'histogram', best: [0, 1, 2], tag: 'DISPLAY', name: 'Histograms',
    blurb: 'How many in an interval, how many in all (CP2) → “at least” and percent questions (CP1) → the interval with the median, an estimated mean from the midpoints (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], hc = r.pick(HCTX), nb = r.int(5, 7), counts = [];
      for (var i = 0; i < nb; i++) counts.push(r.int(c <= 2 ? 1 : 0, c <= 2 ? 9 : 14));
      need(counts[0] > 0 && counts[nb - 1] > 0);
      var st = hc[1], w = hc[2], tot = sum(counts), edge = function (k) { return st + k * w; }, fig = { kind: 'histogram', start: st, width: w, counts: counts, label: hc[0] };
      var intro = 'The histogram shows ' + hc[0].charAt(0).toLowerCase() + hc[0].slice(1) + '. Each bar includes its left edge but not its right edge.';
      if (c === 1) { var b = r.int(0, nb - 1); need(counts[b] > 0);
        steps.push(step('Read the height of the bar from ' + edge(b) + ' to ' + edge(b + 1) + '.', String(counts[b]), 3));
        return out('hg1', intro + ' How many values are from ' + edge(b) + ' up to ' + edge(b + 1) + '?', [{ answer: M(String(counts[b])), check: { type: 'hist', want: 'count', lo: edge(b), hi: edge(b + 1) } }], steps, fig); }
      if (c === 2) { steps.push(step('Add the heights of all the bars.', counts.join('+') + '=' + tot, 3));
        return out('hg2', intro + ' How many values are shown in all?', [{ answer: M(String(tot)), check: { type: 'hist', want: 'count', lo: edge(0), hi: edge(nb) } }], steps, fig); }
      if (c === 3) { var b3 = r.int(1, nb - 2), k3 = sum(counts.slice(b3)); need(k3 > 0);
        steps.push(step('Add the bars from ' + edge(b3) + ' up.', counts.slice(b3).join('+') + '=' + k3, 3));
        return out('hg3', intro + ' How many values are at least ' + edge(b3) + '?', [{ answer: M(String(k3)), check: { type: 'hist', want: 'count', lo: edge(b3), hi: edge(nb) } }], steps, fig); }
      if (c === 4 || c === 5) { var b4 = r.int(1, nb - 1), below = c === 4 ? r.chance(0.5) : r.chance(0.5), part = below ? sum(counts.slice(0, b4)) : sum(counts.slice(b4)), rk = c === 4 ? 0 : 1, pc = 100 * part / tot;
        need(part > 0 && part < tot && safeRound(pc, rk));
        steps.push(step('Count the values ' + (below ? 'below ' : 'at least ') + edge(b4) + ': ' + part + '. Total: ' + tot + '.', '', 2), step('Divide and write as a percent.', '\\frac{' + part + '}{' + tot + '}\\approx ' + rTo(pc, rk) + '\\%', 2));
        return out('hg-pct', intro + ' What percent of the values are ' + (below ? 'less than ' : 'at least ') + edge(b4) + '? Round ' + (rk ? 'to the nearest tenth of a percent.' : 'to the nearest whole percent.'),
          [{ answer: rTo(pc, rk) + '%', check: { type: 'hist', want: 'percent', lo: below ? edge(0) : edge(b4), hi: below ? edge(b4) : edge(nb), round: rk } }], steps, fig); }
      if (c === 6) { var cum = 0, mid = tot / 2, mb = -1; need(tot % 2 === 1);
        for (var k = 0; k < nb; k++) { if (cum < mid + 0.5 && cum + counts[k] >= mid + 0.5) mb = k; cum += counts[k]; }
        need(mb >= 0);
        steps.push(step('There are ' + tot + ' values, so the median is value number ' + (tot + 1) / 2 + '.', '', 2), step('Count up the bars until you pass it.', '', 2));
        return out('hg-med', intro + ' Which interval contains the median?', [{ answer: 'From ' + edge(mb) + ' up to ' + edge(mb + 1), check: { type: 'hist', want: 'median-bin' } }], steps, fig); }
      var est = 0; counts.forEach(function (n0, k7) { est += n0 * (edge(k7) + w / 2); }); est /= tot; need(safeRound(est, 1));
      steps.push(step('Use the midpoint of each interval for its values.', '', 1), step('Multiply each midpoint by its count, add, and divide by ' + tot + '.', '\\approx ' + rTo(est, 1), 3));
      return out('hg-mean', intro + ' Estimate the mean using the midpoint of each interval. Round to the nearest tenth.', [{ answer: M(String(rTo(est, 1))), check: { type: 'hist', want: 'est-mean', round: 1 } }], steps, fig);
    }
  });

  /* ================= SCATTER · least-squares regression ================= */
  var LS = [['Hours studied', 'Test score', 0, 6, 55, 8], ['Temperature (°F)', 'Drinks sold', 60, 5, 20, 3], ['Age of car (years)', 'Value (thousands of $)', 1, 1, 30, -2.5], ['Minutes practiced', 'Free throws made', 10, 10, 4, 0.12]];
  function fmtN(v, k) { var x = rTo(v, k); return (x < 0 ? '-' : '') + String(Math.abs(x)); }
  function lineTex(m, b, k) { var bb = rTo(b, k); return 'y=' + fmtN(m, k) + 'x' + (bb < 0 ? '-' : '+') + String(Math.abs(bb)); }
  function lsq(pts) { var n = pts.length, sx = 0, sy = 0, sxx = 0, sxy = 0, syy = 0; pts.forEach(function (p) { sx += p[0]; sy += p[1]; sxx += p[0] * p[0]; sxy += p[0] * p[1]; syy += p[1] * p[1]; });
    var Sxx = sxx - sx * sx / n, Sxy = sxy - sx * sy / n, Syy = syy - sy * sy / n, m = Sxy / Sxx; return { m: m, b: (sy - m * sx) / n, r: Sxy / Math.sqrt(Sxx * Syy) }; }
  function strength(rv) { var a = Math.abs(rv); return (a >= 0.8 ? 'strong' : a >= 0.5 ? 'moderate' : 'weak') + ' ' + (rv > 0 ? 'positive' : 'negative'); }
  skill({
    id: 'regression', best: [1, 2], tag: 'SCATTER', name: 'Least-squares regression and correlation',
    blurb: 'Predict with a regression line, describe r (CP2) → find r and the least-squares line with a calculator (CP1) → predictions and residuals from the line you found (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], L = r.pick(LS), n = c <= 3 ? 6 : r.int(6, 8), pts = [], xs = [];
      for (var i = 0; i < n; i++) xs.push(L[2] + i * L[3] + (c >= 5 ? r.int(0, 1) * L[3] / 2 : 0));
      xs = xs.filter(function (x, j) { return xs.indexOf(x) === j; });
      var noise = Math.abs(L[5]) * 1.4 * (c === 2 ? r.pick([0.2, 1, 2.5]) : 1);
      xs.forEach(function (x, j) { pts.push([x, Math.round((L[4] + L[5] * (x - L[2])) / (Math.abs(L[5]) < 1 ? 1 : 1) + r.int(-1, 1) * noise) ]); });
      var R = lsq(pts); need(Math.abs(R.r) > 0.3 && Math.abs(R.r) < 0.999 && safeRound(R.m, 2) && safeRound(R.b, 2) && safeRound(R.r, 2));
      var fig = { kind: 'table', vertical: true, head: [L[0], L[1]], rows: pts.map(function (p) { return [p[0], p[1]]; }) };
      var calc = ' Use a calculator.', ln = lineTex(R.m, R.b, 2);
      if (c === 1) { var xg = L[2] + r.int(1, n) * L[3] + L[3] / 2, mm = rTo(R.m, 2), bb = rTo(R.b, 2), y1 = mm * xg + bb; need(safeRound(y1, 1));
        steps.push(step('Substitute ⟨x=' + xg + '⟩ into the regression line.', 'y=' + mm + '(' + xg + ')' + (bb < 0 ? '-' : '+') + Math.abs(bb) + '\\approx ' + rTo(y1, 1), 3));
        return out('ls-use', 'The least-squares regression line for the data is ' + M(ln) + '. Predict ⟨y⟩ when ' + M('x=' + xg) + '. Round to the nearest tenth.', [{ answer: 'y ≈ ' + M(String(rTo(y1, 1))), check: { type: 'lsrl', want: 'use', line: ln, at: 'x=' + xg, round: 1 } }], steps, fig); }
      if (c === 2) { var rv = rTo(R.r, 2); need(Math.abs(Math.abs(rv) - 0.8) > 0.02 && Math.abs(Math.abs(rv) - 0.5) > 0.02);
        steps.push(step('The sign of r gives the direction; how close |r| is to 1 gives the strength.', '', 2), step('|r| ≥ 0.8 strong, 0.5–0.8 moderate, below 0.5 weak.', '', 1));
        return out('ls-desc', 'The correlation coefficient for the data is ' + M('r=' + fmtN(rv, 2)) + '. Describe the strength and direction of the correlation (strong: |r| ≥ 0.8, moderate: 0.5 ≤ |r| < 0.8, weak: |r| < 0.5).',
          [{ answer: strength(rv).charAt(0).toUpperCase() + strength(rv).slice(1) + ' correlation', check: { type: 'lsrl', want: 'describe', r: 'r=' + fmtN(rv, 2) } }], steps, fig); }
      if (c === 3) { steps.push(step('Enter the data in two lists and run linear regression (LinReg).', '', 2), step('Read r.', 'r\\approx ' + fmtN(R.r, 2), 2));
        return out('ls-r', 'Find the correlation coefficient ⟨r⟩ for the data.' + calc + ' Round to the nearest hundredth.', [{ answer: 'r ≈ ' + M(fmtN(R.r, 2)), check: { type: 'lsrl', want: 'r', round: 2 } }], steps, fig); }
      if (c === 4) { steps.push(step('Enter the data and run linear regression.', '', 2), step('Write ⟨y=ax+b⟩ with a and b rounded.', ln, 2));
        return out('ls-line', 'Find the least-squares regression line for the data.' + calc + ' Round the slope and the y-intercept to the nearest hundredth.', [{ answer: M(ln), check: { type: 'lsrl', want: 'line', round: 2 } }], steps, fig); }
      var x5 = xs[xs.length - 1] + L[3], mm5 = rTo(R.m, 2), bb5 = rTo(R.b, 2), y5 = mm5 * x5 + bb5; need(safeRound(y5, 1));
      if (c === 5) { steps.push(step('Find the regression line.', ln, 2), step('Substitute ⟨x=' + x5 + '⟩.', 'y\\approx ' + rTo(y5, 1), 2));
        return out('ls-pred', 'Find the least-squares regression line for the data (round the slope and intercept to the nearest hundredth), then use it to predict ⟨y⟩ when ' + M('x=' + x5) + '. Round the prediction to the nearest tenth.' + calc,
          [{ label: 'a', answer: M(ln), check: { type: 'lsrl', want: 'line', round: 2 } }, { label: 'b', answer: 'y ≈ ' + M(String(rTo(y5, 1))), check: { type: 'lsrl', want: 'predict', at: 'x=' + x5, round: 1 } }], steps, fig); }
      var pi = r.int(0, pts.length - 1), P0 = pts[pi], res = P0[1] - (mm5 * P0[0] + bb5); need(safeRound(res, 2) && Math.abs(res) > 0.05);
      var parts = [{ label: 'a', answer: M(ln), check: { type: 'lsrl', want: 'line', round: 2 } }, { label: 'b', answer: M(fmtN(res, 2)), check: { type: 'lsrl', want: 'residual', at: 'x=' + P0[0], round: 2 } }];
      steps.push(step('Find the regression line.', ln, 2), step('Predicted value at ⟨x=' + P0[0] + '⟩, then residual = actual − predicted.', String(P0[1]) + '-' + rTo(mm5 * P0[0] + bb5, 2) + '\\approx ' + fmtN(res, 2), 2));
      if (c === 7) { parts.push({ label: 'c', answer: 'r ≈ ' + M(fmtN(R.r, 2)) + ': a ' + strength(rTo(R.r, 2)) + ' correlation', check: { type: 'lsrl', want: 'r', round: 2, describe: true } }); steps.push(step('Find r and describe it.', 'r\\approx ' + fmtN(R.r, 2), 2)); }
      return out('ls-res' + c, 'Find the least-squares regression line for the data (round the slope and intercept to the nearest hundredth). Then find the residual for the point with ' + M('x=' + P0[0]) + ', using the rounded line. Round to the nearest hundredth.' + (c === 7 ? ' Also find ⟨r⟩ to the nearest hundredth and describe the strength and direction of the correlation (strong: |r| ≥ 0.8, moderate: 0.5 ≤ |r| < 0.8, weak: |r| < 0.5).' : '') + calc, parts, steps, fig);
    }
  });

  /* ================= SCATTER · correlation and causation ================= */
  // observational studies: who was studied, the two variables, the sign of the correlation, a lurking variable
  var OBS = [
    ['months at a beach town', 'ice cream sales', 'the number of drownings', 1, 'Hot weather (temperature): more people swim and buy ice cream in summer.', 'buying ice cream causes drownings'],
    ['elementary school students', 'shoe size', 'reading score', 1, 'Age: older students have bigger feet and read better.', 'bigger feet cause better reading'],
    ['house fires', 'the number of firefighters sent', 'the amount of damage', 1, 'The size of the fire: bigger fires get more firefighters and cause more damage.', 'sending more firefighters causes more damage'],
    ['countries', 'the number of TVs per household', 'life expectancy', 1, 'Wealth (income): richer countries have more TVs and better health care.', 'owning TVs makes people live longer'],
    ['cities', 'the number of churches', 'the number of crimes', 1, 'Population: bigger cities have more churches and more crimes.', 'churches cause crime'],
    ['days in one city', 'umbrellas sold', 'car accidents', 1, 'Rain (the weather): rainy days bring umbrella sales and slippery roads.', 'selling umbrellas causes car accidents'],
    ['weeks of the year', 'hot chocolate sales', 'flu cases', 1, 'Cold weather (winter): people drink hot chocolate and catch the flu in winter.', 'hot chocolate causes the flu'],
    ['used cars', 'the number of miles driven', 'the price', -1, 'Age of the car: older cars have more miles and sell for less.', 'driving more miles lowers the price'],
    ['towns', 'the number of swimming pools', 'the average temperature', 1, 'Location (climate): warm places build more pools.', 'building pools raises the temperature']];
  // randomized experiments: what was assigned, the result, the claim
  var EXP = [
    ['tomato plants', 'either a new fertilizer or no fertilizer', 'The fertilized plants grew taller on average.', 'the fertilizer makes plants grow taller'],
    ['students', 'either a flashcard app or no app for two weeks', 'The app group scored higher on a vocabulary quiz.', 'the app raises quiz scores'],
    ['volunteers', 'to sleep either 5 hours or 8 hours', 'The 5-hour group had slower reaction times.', 'less sleep slows reaction time'],
    ['patients with headaches', 'either a new pill or a placebo', 'More patients in the pill group reported relief.', 'the pill relieves headaches'],
    ['runners', 'either a sports drink or water during a race', 'The sports-drink group finished faster on average.', 'the sports drink makes runners faster']];
  function rStr(v) { return (v < 0 ? '-' : '') + String(Math.abs(v)).replace(/^0/, '0'); }
  function obsText(o, n, rv) { return 'A study of ' + n + ' ' + o[0] + ' found ' + (rv === null ? 'a strong ' + (o[3] > 0 ? 'positive' : 'negative') + ' correlation' : 'a correlation of ' + M('r=' + rStr(rv))) + ' between ' + o[1] + ' and ' + o[2] + '.'; }
  function expText(e, n) { return 'Researchers randomly assigned ' + n + ' ' + e[0] + (/^to /.test(e[1]) ? ' ' : ' to get ') + e[1] + '. ' + e[2]; }
  var NO_WHY = 'No. Correlation does not show causation; a lurking variable could cause both.', YES_WHY = 'Yes. The subjects were randomly assigned, so the treatment is the likely cause.';
  skill({
    id: 'causation', print: ['who', 'stations'], best: [0, 1, 2], tag: 'SCATTER', name: 'Correlation and causation',
    blurb: 'Does a correlation show causation? Name a lurking variable (CP2) → describe r, observational study or experiment (CP1) → compare two studies and decide which one can show cause and effect (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 2, 4, 5, 3, 6, 7][ctx.c], steps = [], o = r.pick(OBS), e = r.pick(EXP), n = r.int(3, /months|weeks/.test(o[0]) ? 5 : 12) * 10, parts = [];
      var rv = Math.round((r.int(c === 3 ? 30 : 75, 97) / 100) * 100) / 100 * o[3];
      if (c <= 3) {
        var t = obsText(o, n, c === 1 ? null : rv);
        if (c === 3) parts.push({ label: 'a', prompt: 'Describe the strength and direction of the correlation (strong: |r| ≥ 0.8, moderate: 0.5 ≤ |r| < 0.8, weak: |r| < 0.5).', answer: strength(rv).charAt(0).toUpperCase() + strength(rv).slice(1), check: { type: 'lsrl', want: 'describe', r: 'r=' + rStr(rv) } });
        parts.push({ label: c > 1 ? (c === 3 ? 'b' : 'a') : undefined, prompt: 'Does this show that ' + o[5] + '? Explain.', answer: NO_WHY, check: { type: 'causation', want: 'cause' } });
        if (c >= 2) parts.push({ label: c === 3 ? 'c' : 'b', prompt: 'Name a lurking variable that could explain the correlation.', answer: o[4], check: { type: 'causation', want: 'lurk' } });
        steps.push(step('An observational study only shows that the variables move together.', '', 2), step('Look for a third variable that could drive both.', '', 2));
        if (c === 1) { parts[0].label = undefined; return out('cz1', t + ' ' + parts[0].prompt, [{ answer: NO_WHY, check: parts[0].check }], steps); }
        return out('cz' + c, t, parts, steps);
      }
      if (c <= 6) {
        var isExp = r.chance(0.5), t2 = isExp ? expText(e, n) : obsText(o, n, c === 6 ? rv : null), claim = isExp ? e[3] : o[5];
        parts.push({ label: 'a', prompt: 'Is this an observational study or an experiment?', answer: isExp ? 'An experiment (the treatments were randomly assigned).' : 'An observational study (nothing was assigned).', check: { type: 'causation', want: 'type' } });
        if (c === 6 && !isExp) parts.push({ label: 'b', prompt: 'Describe the strength and direction of the correlation (strong: |r| ≥ 0.8, moderate: 0.5 ≤ |r| < 0.8, weak: |r| < 0.5).', answer: strength(rv).charAt(0).toUpperCase() + strength(rv).slice(1), check: { type: 'lsrl', want: 'describe', r: 'r=' + rStr(rv) } });
        parts.push({ label: String.fromCharCode(97 + parts.length), prompt: 'Can you conclude that ' + claim + '? Explain.', answer: isExp ? YES_WHY : NO_WHY, check: { type: 'causation', want: 'cause' } });
        if (c >= 5) parts.push(isExp ? { label: String.fromCharCode(97 + parts.length), prompt: 'What part of the design makes a cause-and-effect conclusion possible?', answer: 'Random assignment: the groups are alike except for the treatment.', check: { type: 'causation', want: 'why' } }
          : { label: String.fromCharCode(97 + parts.length), prompt: 'Name a lurking variable that could explain the correlation.', answer: o[4], check: { type: 'causation', want: 'lurk' } });
        steps.push(step('Were the treatments randomly assigned? Then it is an experiment.', '', 2), step(isExp ? 'Random assignment lets you conclude cause and effect.' : 'Without random assignment, a lurking variable could explain the link.', '', 2));
        return out('cz' + c + (isExp ? 'e' : 'o'), t2, parts, steps);
      }
      var expFirst = r.chance(0.5), sA = expFirst ? expText(e, n) : obsText(o, n, rv), sB = expFirst ? obsText(o, r.int(3, 12) * 10, rv) : expText(e, r.int(3, 12) * 10), win = expFirst ? 'A' : 'B';
      parts.push({ label: 'a', prompt: 'Which study can show cause and effect? Explain.', answer: 'Study ' + win + ', because the subjects were randomly assigned.', check: { type: 'causation', want: 'which' } });
      parts.push({ label: 'b', prompt: 'Describe the strength and direction of the correlation in Study ' + (win === 'A' ? 'B' : 'A') + ' (strong: |r| ≥ 0.8, moderate: 0.5 ≤ |r| < 0.8, weak: |r| < 0.5).', answer: strength(rv).charAt(0).toUpperCase() + strength(rv).slice(1), check: { type: 'lsrl', want: 'describe', r: 'r=' + rStr(rv) } });
      parts.push({ label: 'c', prompt: 'For Study ' + (win === 'A' ? 'B' : 'A') + ', name a lurking variable that could explain the correlation.', answer: o[4], check: { type: 'causation', want: 'lurk' } });
      steps.push(step('Only a randomized experiment can show cause and effect.', '', 2), step('In the observational study, look for a third variable.', '', 2));
      return out('cz7', 'Study A: ' + sA + ' Study B: ' + sB, parts, steps);
    }
  });

  NS.registerSkillSet({
    id: 'algebra1-statistics-data-modeling', course: 'algebra1', courseName: 'Algebra 1', unit: 'statistics-data-modeling', unitName: 'Statistics and Data Modeling',
    title: 'The Data Deli',
    tags: { CENTER: 'Measures of center', SPREAD: 'Spread and outliers', DISPLAY: 'Box plots and histograms', TWOWAY: 'Two-way tables', SCATTER: 'Scatter plots, lines of fit; correlation vs causation' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Center</h4><p>Mean = sum ÷ count. Median = middle value (mean of the two middle values for an even count). Mode = most frequent.</p></section>' +
      '<section><h4>Spread</h4><p>Range = max − min. Q1 and Q3 are the medians of the lower and upper halves (leave out the median when the count is odd). ⟨IQR=Q3-Q1⟩.</p><p>MAD = mean of the distances from the mean.</p></section>' +
      '<section><h4>Outliers</h4><p>Outside ⟨Q1-1.5\\cdot IQR⟩ or ⟨Q3+1.5\\cdot IQR⟩. With outliers, the median describes the center better than the mean.</p></section>' +
      '<section><h4>Box plots</h4><p>Each of the four parts holds about 25% of the data.</p></section>' +
      '<section><h4>Two-way tables</h4><p>Joint: cell ÷ grand total. Marginal: row or column total ÷ grand total. Conditional: cell ÷ the total of the given group.</p></section>' +
      '<section><h4>Lines of fit</h4><p>Residual = actual − predicted. Positive: the line underestimates. Negative: it overestimates.</p></section></div>',
    gaps: [],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
