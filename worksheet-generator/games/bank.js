/* Game question bank.
   Turns the verified Menu Assessment skills into game items. One item is one part of one generated
   problem. Every item carries:
     - the student-facing question (prompt, figure and that part's own prompt)
     - the key answer and worked steps
     - multiple-choice options: the key plus distractors. A distractor is only used when the
       independent verifier REJECTS it as an answer to the printed problem.
     - for answers that can be typed, a checker that runs the student's typed answer through the
       same verifier (nothing is compared as a string).
   Works in the browser and in Node (tests/games-tests.cjs). */
(function (G) {
  'use strict';
  var NS = G.MKMENU, C = NS.check;
  var GB = (G.MKGAMES = G.MKGAMES || {});

  var LEVELS = { cp2: { name: 'CP2', tiers: [1, 2, 3], intOnly: true }, cp1: { name: 'CP1', tiers: [3, 4, 5], intOnly: true }, honors: { name: 'Honors', tiers: [5, 6, 7], intOnly: false } };
  GB.LEVELS = LEVELS;
  var LOOSE = { intOnly: false };

  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function snippets(m) { return C.snippets(m || ''); }

  /* Does the answer to part k stay correct if we write `answer` instead? */
  function answerOk(p, k, answer) {
    var q = clone(p); q.parts[k].answer = answer;
    var v = NS.verifyProblem(q, LOOSE);
    return { ok: v.ok, status: v.status };
  }
  GB.answerOk = answerOk;

  /* ---------------- distractors ---------------- */
  function tidy(t) { return t.replace(/\+\s*-/g, '-').replace(/-\s*-/g, '+').replace(/=\s*\+/g, '=').replace(/^\+/, ''); }
  // every way to change one number, one relation symbol or one key word in the answer
  function mutations(ans, negOk) {
    var out = [], parts = ans.split(/(⟨[^⟩]*⟩)/);
    parts.forEach(function (seg, si) {
      if (!/^⟨/.test(seg)) return;
      var tex = seg.slice(1, -1), re = /(^|[^\d_{a-zA-Z^.])(-?)(\d+)(?![\d}])/g, m, valueFrom = tex.lastIndexOf('=') + 1;
      while ((m = re.exec(tex))) {
        if (m.index + m[1].length < valueFrom) continue;    // keep the question side (f(3)=…, a_{10}=…) as printed
        var start = m.index + m[1].length, end = start + m[2].length + m[3].length, n = +(m[2] + m[3]);
        if (/_\{?$/.test(tex.slice(0, start)) || /\^$/.test(tex.slice(0, start))) continue;   // subscripts and exponents stay
        [n + 1, n - 1, -n, n + 2, n - 2, 2 * n].forEach(function (v) {
          if (v === n || (v < 0 && n > 0 && !negOk)) return;
          var nt = tidy(tex.slice(0, start) + String(v) + tex.slice(end));
          var cp = parts.slice(); cp[si] = '⟨' + nt + '⟩'; out.push({ a: cp.join(''), w: Math.abs(v) === Math.abs(n) ? 3 : Math.abs(v - n) === 1 ? 2 : 1 });
        });
      }
      var rels = [['\\le ', '<'], ['\\ge ', '>'], ['<', '>'], ['\\le ', '\\ge ']];
      rels.forEach(function (pr) {
        [[pr[0], pr[1]], [pr[1], pr[0]]].forEach(function (ab) {
          var i = tex.indexOf(ab[0]); if (i < 0) return;
          if (ab[0] === '<' && tex.slice(i - 3, i) === '\\le') return;
          var cp = parts.slice(); cp[si] = '⟨' + tex.slice(0, i) + ab[1] + tex.slice(i + ab[0].length) + '⟩'; out.push({ a: cp.join(''), w: 3 });
        });
      });
      // reciprocal of a fraction
      var fm = /\\frac\{(\d+)\}\{(\d+)\}/.exec(tex);
      if (fm) { var cp2 = parts.slice(); cp2[si] = '⟨' + tex.replace(fm[0], '\\frac{' + fm[2] + '}{' + fm[1] + '}') + '⟩'; out.push({ a: cp2.join(''), w: 3 }); }
    });
    // percents written in plain text ("25%"): the complement, ±5, ±10
    var pm = /(^|[^\d.])(\d+(?:\.\d+)?)%/.exec(ans);
    if (pm) { var pv = +pm[2]; [100 - pv, pv + 5, pv - 5, pv + 10, pv - 10].forEach(function (v) { if (v > 0 && v < 100 && v !== pv) out.push({ a: ans.replace(pm[0], pm[1] + (Math.round(v * 10) / 10) + '%'), w: v === 100 - pv ? 4 : 2 }); }); }
    if (/^\s*Yes:/.test(ans)) out.push({ a: ans.replace(/^\s*Yes:/, 'No:'), w: 4 });
    if (/^\s*No:/.test(ans)) out.push({ a: ans.replace(/^\s*No:/, 'Yes:'), w: 4 });
    if (/^\s*(Median|Mean)\b/.test(ans)) out.push({ a: /^\s*Median/.test(ans) ? 'Mean, because it uses every value.' : 'Median, because the data have an outlier.', w: 4 });
    if (/^\s*Yes\b/.test(ans) && !/^\s*Yes:/.test(ans) && !/solution/i.test(ans)) out.push({ a: 'No, some input has two different outputs.', w: 4 });
    if (/^\s*No\b/.test(ans) && !/^\s*No:/.test(ans) && !/solution/i.test(ans)) out.push({ a: 'Yes, every input has exactly one output.', w: 4 });
    if (/^\s*Not linear/.test(ans)) out.push({ a: 'Linear: the y-values change by the same amount.', w: 1 });
    if (/\bfirst\b/.test(ans)) out.push({ a: ans.replace(/\bfirst\b/, 'second'), w: 4 });
    else if (/\bsecond\b/.test(ans)) out.push({ a: ans.replace(/\bsecond\b/, 'first'), w: 4 });
    var k1 = (snippets(ans)[0] || '');
    if (/^\s*Linear\b/.test(ans)) { out.push({ a: 'Exponential: each y-value is ⟨' + k1 + '⟩ times the one before.', w: 4 }); out.push({ a: 'Neither: there is no constant difference or constant factor.', w: 2 }); }
    if (/^\s*Exponential\b/.test(ans)) { out.push({ a: 'Linear: the y-values change by ⟨' + k1 + '⟩ each time.', w: 4 }); out.push({ a: 'Neither: there is no constant difference or constant factor.', w: 2 }); }
    if (/^\s*Neither\b/.test(ans)) { out.push({ a: 'Linear: the y-values change by a constant amount.', w: 3 }); out.push({ a: 'Exponential: the y-values change by a constant factor.', w: 3 }); }
    if (/\bincreases\b/.test(ans)) out.push({ a: ans.replace('increases', 'decreases'), w: 3 });
    if (/\bdecreases\b/.test(ans)) out.push({ a: ans.replace('decreases', 'increases'), w: 3 });
    var CW = [['One solution', 'One solution: the slopes are different.'], ['No solution', 'No solution: the lines are parallel.'], ['Infinitely many solutions', 'Infinitely many solutions: the equations describe the same line.']];
    if (/^\s*(One solution|No solution|Infinitely many solutions)\b/.test(ans)) CW.forEach(function (cw) { if (ans.indexOf(cw[0]) !== 0) out.push({ a: cw[1], w: 4 }); });
    if (/^\s*Undefined\b/.test(ans)) { out.push({ a: '⟨m=0⟩', w: 5 }); out.push({ a: '⟨m=1⟩', w: 1 }); }
    if (/^⟨m=0⟩$/.test(ans.trim())) out.push({ a: 'Undefined', w: 5 });
    ['Parallel', 'Perpendicular', 'Neither'].forEach(function (wd) { if (new RegExp('^\\s*(Parallel|Perpendicular|Neither)\\s*$').test(ans) && ans.trim() !== wd) out.push({ a: wd, w: 4 }); });
    if (/increased/.test(ans)) out.push({ a: ans.replace('increased', 'decreased'), w: 2 });
    if (/decreased/.test(ans)) out.push({ a: ans.replace('decreased', 'increased'), w: 2 });
    return out;
  }
  function norm(a) { return a.replace(/\s+/g, ''); }
  function uniq(a) { return a.filter(function (x, i) { return a.indexOf(x) === i && isFinite(x); }); }
  function shape(t) { return /\\\{/.test(t) ? 'set' : /<|>|\\le|\\ge/.test(t) ? 'ineq' : /^\s*\(/.test(t) ? 'point' : /=/.test(t) ? 'eq' : 'num'; }
  /* An option must look like something a student could write: sets sorted without repeats,
     intervals that run from smaller to larger, no "1x", "0x", "+ 0" or "+5". */
  function wellFormed(a) {
    var ok = true;
    snippets(a).forEach(function (t0) {
      var t = t0.replace(/\\[ ,;!]/g, '').replace(/\s+/g, '');
      if (/(^|[^\d.])[01](?=[a-z(])|[+-]0(?![\d.])|(^|[{,=(<>])\+|\\cdot-|\\frac\{[^{}]*\}\{1\}/.test(t)) ok = false;
      var set = /\\\{(.*)\\\}/.exec(t);
      if (set) { var v = set[1].split(',').map(Number); for (var i = 1; i < v.length; i++) if (!(v[i] > v[i - 1])) ok = false; }
      var ch = /^(-?[\d.]+)(\\le|\\ge|<|>)[a-z](\\le|\\ge|<|>)(-?[\d.]+)$/.exec(t);
      if (ch) { var up = function (r) { return r === '<' || r === '\\le'; }; if (up(ch[2]) !== up(ch[3]) || !up(ch[2]) || !(+ch[1] < +ch[4])) ok = false; }
    });
    return ok;
  }
  GB.wellFormed = wellFormed;
  // intervals read from a drawn graph stay on the drawing (no “−8 < x < 9” for a graph that starts at 0)
  function onFigure(p, a) {
    var f = p.fig; if (!f || f.kind !== 'plane') return true;
    var lo = Math.min(f.xmin, f.ymin), hi = Math.max(f.xmax, f.ymax), ok = true;
    snippets(a).forEach(function (t) { if (!/<|>|\\le|\\ge/.test(t)) return; (t.match(/-?\d+(\.\d+)?/g) || []).forEach(function (x) { if (+x < lo || +x > hi) ok = false; }); });
    return ok;
  }
  GB.distractors = function (p, k, rng, want) {
    var key = p.parts[k].answer, seen = {}, good = [];
    seen[norm(key)] = 1;
    var negOk = /-/.test(snippets(NS.studentText(p)).join(' ') + snippets(key).join(' '));
    var cands = mutations(key, negOk);
    // a "prime" key: offer factorizations a student might try (each one is checked and rejected)
    var ch0 = p.parts[k].check || {};
    if (ch0.type === 'factor' && /^\s*prime/i.test(key)) {
      try { var v0 = ch0.v || 'x', rf = C.toRF(C.parseExpr(ch0.expr)).asPoly(), A = Number(rf.coeffOf(v0, 2).constVal().n), Bc = Number(rf.coeffOf(v0, 1).constVal().n), Cc = Number(rf.coeffOf(v0, 0).constVal().n);
        var lin1 = function (a, b) { return '(' + (a === 1 ? '' : a) + v0 + (b < 0 ? '-' : '+') + Math.abs(b) + ')'; };
        for (var d = 1; d <= Math.abs(Cc); d++) if (Cc % d === 0) [[d, Cc / d], [-d, -Cc / d]].forEach(function (pq) { cands.push({ a: '⟨' + lin1(A, pq[0]) + lin1(1, pq[1]) + '⟩', w: 3 }); });
        var sa = Math.round(Math.sqrt(A)), sc = Math.round(Math.sqrt(Math.abs(Cc)));
        if (sa * sa === A && sc * sc === Math.abs(Cc)) { cands.push({ a: '⟨' + lin1(sa, sc) + lin1(sa, -sc) + '⟩', w: 5 }); cands.push({ a: '⟨' + lin1(sa, sc) + '^2⟩', w: 4 }); }
        void Bc;
      } catch (e) { /* not a quadratic */ }
    }
    if (ch0.type === 'factor' && !/^\s*prime/i.test(key)) cands.push({ a: 'Prime', w: 1 });
    // statistics: the classic mix-ups are other statistics of the same data (mean for median, Q1 for the median, range for IQR, …)
    var ks = snippets(key);
    if (ks.length === 1 && /^-?[\d.]+$/.test(ks[0].trim()) && (ch0.type === 'stat' || ch0.type === 'stat-box')) {
      var vals = [], r2 = function (x) { return Math.round(x * 100) / 100; };
      var srt = function (a) { return a.slice().sort(function (x, y) { return x - y; }); }, med = function (a) { a = srt(a); var n = a.length; return n % 2 ? a[(n - 1) / 2] : (a[n / 2 - 1] + a[n / 2]) / 2; };
      if (ch0.type === 'stat') { var data = ch0.data ? ch0.data.replace(/\\[ ,;!]/g, ' ').split(',').map(Number) : (p.fig && p.fig.kind === 'dotplot' ? NS.fig.readDotplot(NS.fig.dotplot(p.fig)) : []);
        if (data.length && data.every(isFinite)) { var sd = srt(data), n = sd.length, h = Math.floor(n / 2), mean = sd.reduce(function (x, y) { return x + y; }, 0) / n;
          vals = [mean, med(sd), sd[n - 1] - sd[0], med(sd.slice(0, h)), med(sd.slice(n - h)), med(sd.slice(n - h)) - med(sd.slice(0, h)), sd[n - 1], sd[0]]; } }
      else if (p.fig && p.fig.kind === 'boxplot') { var q = p.fig.boxes[ch0.box || 0].q; vals = [q[0], q[1], q[2], q[3], q[4], q[4] - q[0], q[3] - q[1], q[2] - q[1]]; }
      uniq(vals.map(r2)).forEach(function (v) { cands.push({ a: key.replace('⟨' + ks[0] + '⟩', '⟨' + String(v).replace(/^-/, '-') + '⟩'), w: 5 }); });
    }
    // slopes: the reciprocal and the opposite (the parallel/perpendicular mix-up), also for unit fractions
    if (ch0.type === 'slope' || ch0.type === 'line-eq') {
      var fm = (ch0.type === 'slope' ? /(-?)\\frac\{(\d+)\}\{(\d+)\}/ : /(-?)\\frac\{(\d+)\}\{(\d+)\}(?=x)/).exec(key);
      if (fm) { var rec = fm[2] === '1' ? fm[3] : '\\frac{' + fm[3] + '}{' + fm[2] + '}', opp = fm[1] ? '' : '-';
        cands.push({ a: key.replace(fm[0], fm[1] + rec), w: 5 }); cands.push({ a: key.replace(fm[0], opp + rec), w: 5 }); cands.push({ a: key.replace(fm[0], opp + '\\frac{' + fm[2] + '}{' + fm[3] + '}'), w: 4 }); }
    }
    // exponents: the classic slips are in the exponents themselves (added instead of multiplied, off by one, wrong sign)
    if (ch0.type === 'pow-simplify' || ch0.type === 'sci' || ch0.type === 'pow-eval') {
      var re2 = /\^\{(-?\d+)\}/g, m2, kk = 0;
      while ((m2 = re2.exec(key)) && kk < 4) { kk++; var e0 = +m2[1], at = m2.index;
        [e0 + 1, e0 - 1, -e0, ch0.type === 'sci' ? e0 + 2 : e0 * 2].forEach(function (v) { if (v === e0 || (ch0.type !== 'sci' && v < 2)) return; cands.push({ a: key.slice(0, at) + '^{' + v + '}' + key.slice(at + m2[0].length), w: v === -e0 ? 4 : 3 }); });
      }
      var uf = /^⟨(-?)\\frac\{1\}\{(\d+)\}⟩$/.exec(key.trim()); if (uf) { cands.push({ a: '⟨' + uf[2] + '⟩', w: 4 }); cands.push({ a: '⟨-' + uf[2] + '⟩', w: 3 }); cands.push({ a: '⟨' + (uf[1] ? '' : '-') + '\\frac{1}{' + uf[2] + '}⟩', w: 3 }); }
      var lv = /^⟨([a-z])⟩$/.exec(key.trim()); if (lv) { cands.push({ a: '⟨' + lv[1] + '^{2}⟩', w: 3 }); cands.push({ a: '⟨1⟩', w: 2 }); cands.push({ a: '⟨\\frac{1}{' + lv[1] + '}⟩', w: 3 }); }
      if (ch0.type === 'pow-simplify') { var fr = /\\frac\{([^{}]*)\}\{([^{}]*)\}/.exec(key); if (fr) cands.push({ a: key.replace(fr[0], '\\frac{' + fr[2] + '}{' + fr[1] + '}'), w: 3 }); }
    }
    if (ch0.type === 'stat-line' && ch0.want === 'over-under') cands.push({ a: key.replace(/under|over/, function (m) { return m === 'under' ? 'over' : 'under'; }), w: 5 });
    // a classic slip: the answer to another part of the same problem (the range given as the domain)
    p.parts.forEach(function (o, j) {
      if (j === k) return; var a = snippets(key), b = snippets(o.answer); if (a.length !== 1 || b.length !== 1) return;
      var dr = p.parts[k].check && p.parts[k].check.type === 'domain-range', nb = dr ? b[0].replace(/(^|[^a-z])[xy](?![a-z])/g, '$1' + (/(^|[^a-z])x(?![a-z])/.test(a[0]) ? 'x' : 'y')) : b[0];
      if (shape(nb) !== shape(a[0])) return;
      cands.push({ a: key.replace('⟨' + a[0] + '⟩', '⟨' + nb + '⟩'), w: 4 });
    });
    cands.forEach(function (m) {
      if (seen[norm(m.a)]) return; seen[norm(m.a)] = 1;
      if (!wellFormed(m.a) || !onFigure(p, m.a)) return;
      var r = answerOk(p, k, m.a);
      if (!r.ok && r.status === 'mismatch') good.push(m);   // the verifier read it and says it is wrong
    });
    // prefer the classic slips (sign, relation, off by one), keep some variety
    good = rng.shuffle(good).sort(function (x, y) { return y.w - x.w; });
    var pick = [], pool = good.slice();
    while (pick.length < (want || 3) && pool.length) {
      var i = pool.length > 3 && rng.chance(0.35) ? rng.int(0, pool.length - 1) : 0;
      pick.push(pool.splice(i, 1)[0].a);
    }
    return pick;
  };

  /* ---------------- typed answers ---------------- */
  function typedKind(part) {
    var ch = part.check || {}, t = ch.type, plain = C.plainText(part.answer.replace(/⟨[^⟩]*⟩/g, ' ')).trim().toLowerCase();
    if (t === 'factor' && /^\s*prime\b/i.test(part.answer)) return 'factor';
    if (/^\s*-?\d+(\.\d+)?%\s*$/.test(part.answer)) return 'percent';
    if (t === 'stat' && /better|compare/.test(ch.want) || t === 'scatter-corr' || (t === 'stat-box' && ch.want === 'compare') || (t === 'twoway' && ch.want === 'assoc') || (t === 'stat-line' && /over|slope|intercept/.test(ch.want))) return null;
    if (t === 'pow-simplify') return 'pexpr';
    if (t === 'pow-eval') return 'number';
    if (t === 'sci') return ch.want === 'to-std' ? 'number' : 'sci';
    if (t === 'system') return ch.want === 'is-solution' || ch.want === 'count' || !snippets(part.answer).length ? null : ch.want === 'param' ? 'number' : 'point';
    if (t === 'sys-apply') return ch.want === 'model' ? 'eqs' : ch.want === 'x' || ch.want === 'y' ? 'number' : 'list';
    if (t === 'ineq2') return ch.want === 'is-solution' ? null : ch.want === 'point-in' ? 'point' : snippets(part.answer).length > 1 ? 'ineqs' : 'ineq';
    if ((t === 'stat' && /five|outliers|fences|mode/.test(ch.want)) || (t === 'twoway' && ch.want === 'fill')) return snippets(part.answer).length ? 'list' : null;
    if (!snippets(part.answer).length) return null;
    if (!/^((domain|range|initial value|growth factor|decay factor):|term|and|or|after|years?|mg|bacteria|followers|the integers are|width|length|feet|inches|meters|seconds|minutes?|hours?|weeks?|months?|per|\.|,|\s)*$/.test(plain)) return null;
    if (t === 'is-function' || t === 'graph-behavior' || (t === 'rate' && (ch.words || ch.intervals)) || (t === 'linear-rule' && /not/.test(plain))) return null;
    if (t === 'sequence' && (ch.want === 'recursive' || ch.yesno)) return null;
    if (/^(ineq|read-graph|error-line|model-ineq|iscenario|classify|scenario|model-eq|literal-eval)$/.test(t)) return t === 'ineq' ? 'ineq' : null;
    if (t === 'factor') return 'factor';
    if (t === 'quad-roots') return 'list';
    if (t === 'quad-apply') return ch.form === 'consec' || ch.form === 'rect' ? 'list' : 'number';
    if (t === 'slope') return ch.want === 'collinear' || ch.want === 'relation' ? null : 'number';
    if (t === 'line-eq') return 'rule';
    if (t === 'intercepts') return 'point';
    if (t === 'line-apply') return ch.want === 'equation' ? 'rule' : 'number';
    if (t === 'exp-model') return null;
    if (t === 'exp-identify') return ch.want === 'initial' || ch.want === 'factor' ? 'number' : null;
    if (t === 'exp-features') return ch.want === 'asymptote' ? 'eq' : ch.want === 'range' ? 'ineq' : null;
    if (t === 'exp-rule') return ch.predict !== undefined ? 'number' : 'rule';
    if (t === 'exp-apply') return ch.want === 'rule' ? 'rule' : 'number';
    if (t === 'exp-solve') return 'solve';
    if (t === 'domain-range') return /\\le|\\ge|<|>/.test(part.answer) ? 'interval' : 'set';
    if (t === 'read-fig' && ch.want === 'inputs') return 'list';
    if (t === 'table-fill' || t === 'ineq-members') return 'list';
    if (t === 'sequence' && ch.want === 'next') return 'list';
    if (t === 'sequence' && ch.want === 'formula') return 'formula';
    if (t === 'linear-rule' && ch.predict === undefined) return 'rule';
    if ((t === 'func-eval' && ch.symbolic) || t === 'simplify') return 'expr';
    if (t === 'literal') return 'literal';
    if (t === 'solve') return 'solve';
    return 'number';
  }
  GB.HINTS = {
    number: 'Type a number, like -4 or 2/3.',
    list: 'Type the values separated by commas, like 3, -1, 5.',
    set: 'Type a set in braces, like {-2, 0, 3}.',
    interval: 'Type an inequality, like -2 <= x < 5 (use <= for ≤ and >= for ≥).',
    ineq: 'Type an inequality, like x >= -3 (use <= for ≤ and >= for ≥).',
    formula: 'Type the formula, like a_n = 3n - 2 (or just 3n - 2).',
    rule: 'Type the rule, like y = 2x - 3 or y = 5*2^x (use ^ for exponents).',
    eq: 'Type an equation, like y = 3.',
    percent: 'Type the percent as a number, like 37.5 (the % sign is optional).',
    factor: 'Type the factored form, like 3x(x - 4) or (2x + 1)(x - 5). Use ^ for powers. Type “prime” if it does not factor.',
    expr: 'Type the simplified expression, like 3a + 7 (use ^ for powers).',
    literal: 'Type the formula, like h = (A - 2b)/3.',
    solve: 'Type the solution, like x = 4 (or just 4).',
    point: 'Type a point, like (0, -3).',
    pexpr: 'Type like 4x^6 or (3x^2)/(4y^3). Use ^ for powers and positive exponents only.',
    sci: 'Type scientific notation like 4.2 x 10^-4 (or 4.2*10^-4).',
    eqs: 'Type both equations separated by “and”, like x + y = 10 and 2x + 3y = 24.',
    ineqs: 'Type both inequalities separated by “and”, like y > 2x - 1 and y <= -x + 4 (use <= for ≤ and >= for ≥).'
  };
  function texOf(s) {
    return s.replace(/[−–]/g, '-').replace(/≤|<=|=</g, '\\le ').replace(/≥|>=|=>/g, '\\ge ')
      .replace(/\*/g, '\\cdot ').replace(/(\([^()]*\)|[A-Za-z0-9.]+)\s*\/\s*(\([^()]*\)|[A-Za-z0-9.]+)/g, function (w, a, b) {
        var tail = '', m = /^(\d+(?:\.\d+)?)([A-Za-z].*)$/.exec(b);
        if (m && /^-?[\d.]+$/.test(a)) { b = m[1]; tail = m[2]; }    // 1/2x means one half of x
        return '\\frac{' + a.replace(/^\((.*)\)$/, '$1') + '}{' + b.replace(/^\((.*)\)$/, '$1') + '}' + tail; }).replace(/\s+/g, ' ').trim();
  }
  GB.toMarkup = function (raw, kind) {
    var s = String(raw || '').trim(); if (!s) return '';
    if (kind === 'factor' && /^prime$/i.test(s)) return 'Prime';
    if (kind === 'percent') return '⟨' + texOf(s.replace(/%/g, '')) + '⟩%';
    if (kind === 'ineq' && /\s(or|and)\s/.test(s)) return s.split(/\s+(or|and)\s+/).map(function (x, i) { return i % 2 ? x : '⟨' + texOf(x) + '⟩'; }).join(' ');
    if (kind === 'sci') return '⟨' + s.replace(/\s*(?:x|×|\*|\\times|\\cdot)\s*10\s*\^\s*\(?\s*\{?(-?\s*\d+)\}?\s*\)?/i, function (w, e) { return '\\times10^{' + e.replace(/\s/g, '') + '}'; }).replace(/^\s*10\s*\^\s*\(?(-?\d+)\)?/, '10^{$1}').trim() + '⟩';
    if (kind === 'eqs' || kind === 'ineqs') return s.split(/\s*(?:\band\b|;)\s*/).filter(Boolean).map(function (x) { return '⟨' + texOf(x) + '⟩'; }).join(' and ');
    if (kind === 'list') return s.split(/\s*(?:,|;|\band\b|\bor\b)\s*/).filter(Boolean).map(function (x) { return '⟨' + texOf(x) + '⟩'; }).join(' and ');
    if (kind === 'set') { var body = s.replace(/^\{|\}$/g, '').replace(/^\\\{|\\\}$/g, ''); return '⟨\\{' + body.split(/\s*,\s*/).map(texOf).join(',\\ ') + '\\}⟩'; }
    if (kind === 'interval' && !/x|y/.test(s)) return '⟨' + texOf(s) + '⟩';
    return '⟨' + texOf(s) + '⟩';
  };
  // the key written the way a student would type it (used by the tests and the "show me" button)
  GB.typedForm = function (part) {
    function plain(t) {
      return t.replace(/\\text\{\s*(or|and)\s*\}/g, ' $1 ').replace(/\\left|\\right/g, '').replace(/\\le\s*/g, '<=').replace(/\\ge\s*/g, '>=').replace(/\\frac\{(-?\d+)\}\{(\d+)\}/g, '$1/$2').replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, '($1)/($2)').replace(/\\times\s*/g, ' x ').replace(/\\cdot\s*/g, '*').replace(/\^\{([^{}]*)\}/g, '^($1)').replace(/\\\{/g, '{').replace(/\\\}/g, '}')
        .replace(/\\[ ,;!]/g, ' ').replace(/\s+/g, ' ').trim();
    }
    // keep the connecting words "or"/"and" between answers; drop labels and units
    var bits = String(part.answer).split(/(⟨[^⟩]*⟩)/), out = '', pend = '';
    bits.forEach(function (b) {
      if (/^⟨/.test(b)) { if (out) out += pend || ', '; out += plain(b.slice(1, -1)); pend = ''; }
      else { var m = /\b(or|and)\b/.exec(b); if (m && out) pend = ' ' + m[1] + ' '; }
    });
    return out;
  };
  /* what a student would type for the key of an item */
  GB.keyTyped = function (it) { var a = it.p.parts[it.k].answer; return /^\s*prime/i.test(a) ? 'prime' : it.typed === 'percent' ? a.trim() : GB.typedForm(it.p.parts[it.k]); };
  GB.checkTyped = function (item, raw) {
    if (!item.typed) return { ok: false, msg: 'This question is multiple choice.' };
    var m = GB.toMarkup(raw, item.typed); if (!m) return { ok: false, msg: 'Type an answer first.' };
    var r; try { r = answerOk(item.p, item.k, m); } catch (e) { r = { ok: false }; }
    return { ok: r.ok, markup: m };
  };

  /* ---------------- items ---------------- */
  GB.partQuestion = function (p, k) {
    var pt = p.parts[k], multi = p.parts.length > 1, ask = pt.prompt || '';
    if (!ask && multi) { var lab = /^\s*([A-Z][a-z]+):/.exec(pt.answer); if (lab) ask = 'Find the ' + lab[1].toLowerCase() + '.'; }
    return { prompt: p.prompt, fig: p.fig || null, work: p.work || null, ask: ask, label: multi && pt.label ? pt.label : '' };
  };
  GB.makeItems = function (setId, skillId, c, policy, seed, used) {
    var p = NS.generateProblem(setId, skillId, c, policy, seed, used);
    if (p.failed) return [];
    var set = NS.skillSets[setId], rng = G.MKWS.rng.make(G.MKWS.rng.hash(seed + '|mc'));
    var items = [];
    p.parts.forEach(function (pt, k) {
      if (!pt.check) return;
      var ds = GB.distractors(p, k, rng, 3);
      if (!ds.length) return;    // an item with no verified wrong options cannot be multiple choice
      var opts = rng.shuffle([{ a: pt.answer, ok: true }].concat(ds.map(function (d) { return { a: d, ok: false }; })));
      items.push({ id: p.uid + '-' + k, p: p, k: k, skill: skillId, skillName: set.byId[skillId].name, tag: p.tag, tagName: set.tags[p.tag] || p.tag, c: c,
        q: GB.partQuestion(p, k), answer: pt.answer, steps: p.steps || [], options: opts, typed: typedKind(pt) });
    });
    return items;
  };
  /* A deck: `slots` is a list of {skill, c}; each slot yields one item (a random part of the problem). */
  GB.buildDeck = function (setId, slots, opts, done) {
    opts = opts || {}; var used = { keys: new Set(), sigs: new Set() }, out = [], i = 0, seed = opts.seed || String(Date.now()) + Math.random();
    var rng = G.MKWS.rng.make(G.MKWS.rng.hash(seed + '|deck'));
    function one(slot, n) {
      var policy = { intOnly: slot.c <= 5, level: 'game' };
      for (var tries = 0; tries < 10; tries++) {
        var its = GB.makeItems(setId, slot.skill, slot.c, policy, seed + '|' + n + '|' + tries, used);
        if (opts.typedOnly) its = its.filter(function (it) { return it.typed; });
        if (opts.preferTyped && its.some(function (it) { return it.typed; })) its = its.filter(function (it) { return it.typed; });
        if (its.length) return rng.pick(its);
      }
      return null;
    }
    function step() {
      var t0 = Date.now();
      while (i < slots.length && Date.now() - t0 < 40) { var it = one(slots[i], i); if (it) { it.slot = slots[i]; out.push(it); } i++; }
      if (opts.progress) opts.progress(i, slots.length);
      if (i < slots.length) { if (G.setTimeout && !opts.sync) G.setTimeout(step, 0); else step(); }
      else done(out);
    }
    step();
  };
  GB.skillsOf = function (setId) { return NS.skillSets[setId].skills.map(function (s) { return s.id; }); };
})(typeof window !== 'undefined' ? window : globalThis);
