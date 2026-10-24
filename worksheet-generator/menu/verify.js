/* Menu Assessment Generator — problem verification.

   verifyProblem(problem, policy) re-derives every answer from what the STUDENT sees:
   the math named by a part's `check` must appear verbatim (inside ⟨…⟩) in the student
   prompt, and is then parsed and solved by menu/mathcheck.js (independent parser and
   BigInt arithmetic; no generator code). Word problems are re-solved from the numbers
   and words printed in the prompt by the scenario checkers below.

   Result: { ok, status, issues:[…], computed:[per-part computed answer text] }
     status: 'verified' | 'mismatch' | 'invalid' | 'manual' (no automatic check possible)
*/
(function (G) {
  'use strict';
  var NS = (G.MKMENU = G.MKMENU || {});
  var C = NS.check, Q = C.Q;

  function studentText(p) {
    return [p.prompt || ''].concat((p.work || []).map(function (w) { return '⟨' + w + '⟩'; })).concat((p.parts || []).map(function (pt) { return pt.prompt || ''; })).join(' ');
  }
  function shown(p, tex) {
    return C.snippets(studentText(p)).some(function (s) { return norm(s) === norm(tex); });
  }
  function norm(s) { return String(s).replace(/\s+/g, ''); }
  function qText(q) { return q.isInt() ? String(q.n) : (q.n < 0n ? '-' : '') + '\\frac{' + (q.n < 0n ? -q.n : q.n) + '}{' + q.d + '}'; }
  function firstMath(markup) { var s = C.snippets(markup); return s.length ? s[0] : null; }
  function valueFromAnswer(markup, v) {
    var m = firstMath(markup);
    if (m === null) { var nums = C.numbersInText(markup); if (!nums.length) throw new C.CheckError('no number in answer'); return nums[0]; }
    if (/[=<>]/.test(m)) {
      var rel = C.parseRelation(m);
      if (v && !(rel.lhs.k === 'var' && rel.lhs.v === v)) throw new C.CheckError('answer should start with ' + v + ' =');
      return C.readNumber(texOf(rel.rhs, m));
    }
    return C.readNumber(m);
  }
  function texOf(node, whole) { return whole.slice(whole.indexOf('=') + 1); }

  /* ---------- scenario checkers (word problems) ---------- */
  var WORDS = { two: 2, three: 3, four: 4, five: 5 };
  var SCEN = {
    'fee-rate': function (p) {
      var n = C.numbersInText(p.prompt); if (n.length < 3) throw new C.CheckError('expected fee, rate and total in the text');
      var x = n[2].sub(n[0]).div(n[1]); return { n: x, ok: x.isInt() && x.n > 0n };
    },
    'spend': function (p) {
      var n = C.numbersInText(p.prompt); if (n.length < 3) throw new C.CheckError('expected start, rate and remaining amount');
      var x = n[0].sub(n[2]).div(n[1]); return { n: x, ok: x.isInt() && x.n > 0n };
    },
    'two-plans': function (p) {
      var n = C.numbersInText(p.prompt); if (n.length < 4) throw new C.CheckError('expected two fees and two rates');
      var f1 = n[0], r1 = n[1], f2 = n[2], r2 = n[3];
      if (r1.eq(r2)) return { ok: false };
      var x = f2.sub(f1).div(r1.sub(r2));
      var names = []; String(C.plainText(p.prompt)).replace(/(?:^|\.\s+)([^.]*?) charges a \$/g, function (m, nm) { names.push(nm.trim()); });
      return { n: x, cost: f1.add(r1.mul(x)), ok: x.isInt() && x.n > 0n, costAt: function (k) { return [f1.add(r1.mul(k)), f2.add(r2.mul(k))]; }, names: names };
    },
    'perimeter': function (p) {
      var t = C.plainText(p.prompt), n = C.numbersInText(p.prompt);
      var m = /is\s+(\d+)\s+\S+\s+(more|less) than\s+(\d+)\s+times its width.*?perimeter is\s+(\d+)/.exec(t);
      if (!m) throw new C.CheckError('could not read the rectangle description');
      var k = new Q(m[1]), mult = new Q(m[3]), P = new Q(m[4]); if (m[2] === 'less') k = k.neg();
      var w = P.div(new Q(2)).sub(k).div(mult.add(Q.ONE)), L = mult.mul(w).add(k);
      return { w: w, L: L, P: P, ok: w.isInt() && w.n > 0n && L.n > 0n, nums: n };
    },
    'consecutive': function (p) {
      var t = C.plainText(p.prompt), m = /sum of (\w+) consecutive (even |odd )?integers is (-?\d+)/.exec(t);
      if (!m) throw new C.CheckError('could not read the consecutive-integer sentence');
      var k = WORDS[m[1]], gap = m[2] ? 2 : 1, S = new Q(m[3]);
      var first = S.sub(new Q(gap * k * (k - 1) / 2)).div(new Q(k));
      var ok = first.isInt();
      if (ok && m[2] === 'even ') ok = first.n % 2n === 0n;
      if (ok && m[2] === 'odd ') ok = first.n % 2n !== 0n;
      var list = []; for (var i = 0; i < k; i++) list.push(first.add(new Q(gap * i)));
      return { list: list, ok: ok };
    }
  };

  /* ---------- inequalities ---------- */
  function figSet(spec) {
    if (!NS.fig) throw new C.CheckError('figures module not loaded');
    var r = NS.fig.readNumberLine(NS.fig.numberLine(spec));
    return { min: r.min, max: r.max, set: r.pieces.map(function (pc) {
      return { lo: pc.lo ? new Q(pc.lo[0], pc.lo[1]) : null, loC: !!pc.loC, hi: pc.hi ? new Q(pc.hi[0], pc.hi[1]) : null, hiC: !!pc.hiC };
    }) };
  }
  function endpoints(set) { var e = []; set.forEach(function (I) { if (I.lo) e.push(I.lo); if (I.hi) e.push(I.hi); }); return e; }
  function intEnds(set) { return endpoints(set).every(function (q) { return q.isInt(); }); }
  function fitsWindow(set, fig) {
    return endpoints(set).every(function (q) { var v = Number(q.n) / Number(q.d); return v > fig.min + 0.4 && v < fig.max - 0.4; });
  }
  /* word problems with inequalities: re-solved from the printed numbers and words */
  var ISCEN = {
    'buy-max': function (t, n) { var b = n[1].div(n[0]); return { set: C.solutionSet('x\\le ' + qText(b)), best: floorQ(b), dir: 'max' }; },
    'fee-max': function (t, n) { var b = n[2].sub(n[0]).div(n[1]); return { set: C.solutionSet('x\\le ' + qText(b)), best: floorQ(b), dir: 'max' }; },
    'save-min': function (t, n) { var b = n[2].sub(n[0]).div(n[1]); return { set: C.solutionSet('x\\ge ' + qText(b)), best: ceilQ(b), dir: 'min' }; },
    'plans': function (t, n) {
      // "Plan A … $f1 … $r1 per … Plan B … $f2 … $r2 per …" — when is the FIRST plan cheaper?
      var f1 = n[0], r1 = n[1], f2 = n[2], r2 = n[3], k = f2.sub(f1).div(r1.sub(r2));
      var set = r1.sub(r2).n > 0n ? C.solutionSet('x<' + qText(k)) : C.solutionSet('x>' + qText(k));
      var best = r1.sub(r2).n > 0n ? (k.isInt() ? k.sub(Q.ONE) : floorQ(k)) : (k.isInt() ? k.add(Q.ONE) : ceilQ(k));
      return { set: set, best: best, dir: r1.sub(r2).n > 0n ? 'max' : 'min', k: k };
    },
    'range': function (t, n) { var lo = n[2].sub(n[0]).div(n[1]), hi = n[3].sub(n[0]).div(n[1]); return { set: C.solutionSet(qText(lo) + '\\le x\\le ' + qText(hi)), lo: lo, hi: hi }; },
    'average': function (t, n) {
      var m = /average of at least (\d+)/.exec(t); var target = new Q(m[1]), scores = n.slice(0, n.length - 1), sum = Q.ZERO;
      var count = new Q(scores.length + 1); scores.forEach(function (q) { sum = sum.add(q); });
      var b = target.mul(count).sub(sum);
      return { set: C.solutionSet('x\\ge ' + qText(b)), best: ceilQ(b), dir: 'min' };
    }
  };
  function floorQ(q) { var f = q.n / q.d; if (q.n < 0n && f * q.d !== q.n) f -= 1n; return new Q(f); }
  function ceilQ(q) { var f = floorQ(q); return f.eq(q) ? f : f.add(Q.ONE); }

  function checkPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '';
    if (!chk || chk.type === 'none') return { status: 'manual', msg: 'No automatic check for this answer.' };
    var t = chk.type;
    if (t === 'ineq' || t === 'read-graph' || t === 'ineq-members' || t === 'error-line' || t === 'iscenario' || t === 'model-ineq') return checkIneqPart(p, part, policy);
    if ((t === 'solve' || t === 'classify' || t === 'literal' || t === 'literal-eval') && !shown(p, chk.eq)) return { status: 'invalid', msg: 'The equation being checked is not the one printed for students.' };
    if ((t === 'simplify' || t === 'evaluate') && !shown(p, chk.expr)) return { status: 'invalid', msg: 'The expression being checked is not the one printed for students.' };

    if (t === 'solve') {
      var s = C.solveLinear(chk.eq, chk.v);
      if (s.kind !== 'one') return { status: 'invalid', msg: s.kind === 'none' ? 'This equation has no solution.' : 'Every number is a solution of this equation.' };
      if (policy && policy.intOnly && !s.value.isInt()) return { status: 'invalid', msg: 'The solution is not a whole number.', computed: chk.v + '=' + qText(s.value) };
      var got = valueFromAnswer(ans, chk.v);
      return got.eq(s.value) ? { status: 'verified', computed: chk.v + '=' + qText(s.value) } : { status: 'mismatch', msg: 'Correct answer is ' + chk.v + ' = ' + s.value + '.', computed: chk.v + '=' + qText(s.value) };
    }
    if (t === 'classify') {
      var k = C.solveLinear(chk.eq, chk.v), said = C.classifyText(C.plainText(ans));
      var comp = k.kind === 'none' ? 'No solution' : k.kind === 'all' ? 'Infinitely many solutions' : 'One solution: ⟨' + chk.v + '=' + qText(k.value) + '⟩';
      if (k.kind === 'one') {
        if (said) return { status: 'mismatch', msg: 'This equation has exactly one solution.', computed: comp };
        if (policy && policy.intOnly && !k.value.isInt()) return { status: 'invalid', msg: 'The solution is not a whole number.', computed: comp };
        return valueFromAnswer(ans, chk.v).eq(k.value) ? { status: 'verified', computed: comp } : { status: 'mismatch', msg: 'Correct: ' + comp, computed: comp };
      }
      return said === k.kind ? { status: 'verified', computed: comp } : { status: 'mismatch', msg: 'Correct: ' + comp, computed: comp };
    }
    if (t === 'simplify') {
      var am = firstMath(ans); if (am === null) return { status: 'mismatch', msg: 'No simplified expression in the answer.' };
      if (!C.equivalent(chk.expr, am)) return { status: 'mismatch', msg: 'The answer is not equivalent to the expression.' };
      var form = C.simplifiedForm(am);
      if (!form.ok) return { status: 'mismatch', msg: 'The answer is not fully simplified (' + form.problems.join(', ') + ').' };
      return { status: 'verified' };
    }
    if (t === 'evaluate') {
      var env = {}, vals = chk.values || {};
      Object.keys(vals).forEach(function (v) {
        if (!shown(p, v + '=' + vals[v])) throw new C.CheckError('value ' + v + ' is not printed in the problem');
        env[v] = C.readNumber(vals[v]);
      });
      var val = C.evalNode(C.parseExpr(chk.expr), env);
      if (policy && policy.intOnly && !val.isInt()) return { status: 'invalid', msg: 'The value is not a whole number.', computed: qText(val) };
      return valueFromAnswer(ans).eq(val) ? { status: 'verified', computed: qText(val) } : { status: 'mismatch', msg: 'Correct value is ' + val + '.', computed: qText(val) };
    }
    if (t === 'literal') {
      var am2 = firstMath(ans); if (am2 === null) return { status: 'mismatch', msg: 'No equation in the answer.' };
      var lr = C.checkLiteral(chk.eq, chk.v, am2);
      return lr.ok ? { status: 'verified' } : { status: 'mismatch', msg: lr.reason };
    }
    if (t === 'literal-eval') {
      if (!shown(p, chk.given)) return { status: 'invalid', msg: 'The given values are not the ones printed.' };
      var rel = C.parseRelation(chk.eq), env2 = {};
      chk.given.split(',').forEach(function (g) { var rr = C.parseRelation(g); env2[rr.lhs.v] = C.readNumber(g.slice(g.indexOf('=') + 1)); });
      function sub(n) {
        if (n.k === 'var' && env2[n.v]) return { k: 'num', v: env2[n.v] };
        var c2 = Object.assign({}, n); if (c2.a) c2.a = sub(c2.a); if (c2.b) c2.b = sub(c2.b); return c2;
      }
      var s2 = C.solveLinear({ lhs: sub(rel.lhs), rhs: sub(rel.rhs), rel: '=' }, chk.v);
      if (s2.kind !== 'one') return { status: 'invalid', msg: 'These values do not give one answer.' };
      if (policy && policy.intOnly && !s2.value.isInt()) return { status: 'invalid', msg: 'The value is not a whole number.' };
      return valueFromAnswer(ans, chk.v).eq(s2.value) ? { status: 'verified', computed: chk.v + '=' + qText(s2.value) } : { status: 'mismatch', msg: 'Correct value: ' + chk.v + ' = ' + s2.value + '.', computed: chk.v + '=' + qText(s2.value) };
    }
    if (t === 'model-eq') {
      var sc = SCEN[chk.scenario](p); if (!sc.ok) return { status: 'invalid', msg: 'The word problem does not have a whole-number answer.' };
      var em = firstMath(ans); if (em === null) return { status: 'mismatch', msg: 'No equation in the answer.' };
      var sol = C.solveLinear(em, chk.v);
      return sol.kind === 'one' && sol.value.eq(sc.n) ? { status: 'verified' } : { status: 'mismatch', msg: 'The equation does not model the situation.' };
    }
    if (t === 'scenario') {
      var S = SCEN[chk.scenario](p); if (!S.ok) return { status: 'invalid', msg: 'The word problem does not have a whole-number answer.' };
      var nums = C.numbersInText(ans).concat(C.snippets(ans).map(function (m) { try { return valueFromAnswer('⟨' + m + '⟩'); } catch (e) { return null; } }).filter(Boolean));
      function has(q) { return nums.some(function (z) { return z.eq(q); }); }
      if (chk.want === 'n') return has(S.n) ? { status: 'verified', computed: String(S.n) } : { status: 'mismatch', msg: 'Correct answer: ' + S.n + '.' };
      if (chk.want === 'cost') return has(S.cost) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct cost: $' + S.cost + '.' };
      if (chk.want === 'compare') {
        var cs = S.costAt(new Q(chk.n)), cheaper = cs[0].n < cs[1].n ? 0 : 1, diff = cs[0].sub(cs[1]); if (diff.n < 0n) diff = diff.neg();
        var nameOk = S.names.length === 2 && C.plainText(ans).indexOf(S.names[cheaper]) === 0;
        return nameOk && has(diff) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + (S.names[cheaper] || '') + ', by $' + diff + '.' };
      }
      if (chk.want === 'wl') { var a = C.numbersInText(ans); return a.length >= 2 && a[0].eq(S.w) && a[1].eq(S.L) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: width ' + S.w + ', length ' + S.L + '.' }; }
      if (chk.want === 'square') {
        var side = S.P.div(new Q(4)), sq = side.mul(side), rec = S.w.mul(S.L), d = sq.sub(rec), word = d.n > 0n ? 'square' : 'rectangle'; if (d.n < 0n) d = d.neg();
        return C.plainText(ans).toLowerCase().indexOf(word) >= 0 && has(d) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: the ' + word + ', by ' + d + '.' };
      }
      if (chk.want === 'list') {
        var got = C.numbersInText(ans);
        return got.length === S.list.length && got.every(function (g, i) { return g.eq(S.list[i]); }) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + S.list.join(', ') + '.' };
      }
    }
    return { status: 'manual', msg: 'Unknown check type ' + t };
  }

  function checkIneqPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '', t = chk.type, v = chk.v || 'x', res;
    function figOk(set) {
      if (!part.answerFig) return null;
      var fs = figSet(part.answerFig);
      if (!C.setEqual(fs.set, set)) return { status: 'mismatch', msg: 'The number line in the key does not match the answer.' };
      if (!fitsWindow(set, fs)) return { status: 'invalid', msg: 'The number line in the key does not show every endpoint.' };
      return null;
    }
    function blankOk(set) {
      if (!p.fig || (p.fig.pieces && p.fig.pieces.length)) return null;
      return fitsWindow(set, figSet(p.fig)) ? null : { status: 'invalid', msg: 'The printed number line does not reach the answer’s endpoints.' };
    }
    if (t === 'ineq') {
      if (!shown(p, chk.ineq)) return { status: 'invalid', msg: 'The inequality being checked is not the one printed for students.' };
      var set = C.solutionSet(chk.ineq, v), comp = C.setText(set, v);
      if (policy && policy.intOnly && !intEnds(set)) return { status: 'invalid', msg: 'The boundary is not a whole number.', computed: comp };
      if (!chk.allowSpecial && (!set.length || (set.length === 1 && !set[0].lo && !set[0].hi))) return { status: 'invalid', msg: 'The solution is ' + comp.toLowerCase() + ' (not intended here).', computed: comp };
      var got = C.setFromAnswer(ans, v);
      if (!C.setEqual(got, set)) return { status: 'mismatch', msg: 'Correct solution: ' + comp, computed: comp };
      if (!C.solvedForm(ans, v)) return { status: 'mismatch', msg: 'The answer is not written with ' + v + ' by itself.', computed: comp };
      return figOk(set) || blankOk(set) || { status: 'verified', computed: comp };
    }
    if (t === 'read-graph') {
      if (!p.fig || !p.fig.pieces || !p.fig.pieces.length) return { status: 'invalid', msg: 'There is no graph to read.' };
      var gs = figSet(p.fig).set, gt = C.setText(gs, v);
      if (!fitsWindow(gs, figSet(p.fig))) return { status: 'invalid', msg: 'The printed graph does not show its endpoints clearly.' };
      if (policy && policy.intOnly && !intEnds(gs)) return { status: 'invalid', msg: 'The graph has a non-integer endpoint.' };
      var formOk = chk.form === 'abs' ? C.snippets(ans).some(function (x) { return /\|/.test(x); }) : C.solvedForm(ans, v);
      return C.setEqual(C.setFromAnswer(ans, v), gs) && formOk ? { status: 'verified', computed: gt } : { status: 'mismatch', msg: 'The graph shows ' + gt + (chk.form === 'abs' ? ' (answer must use absolute value)' : ''), computed: gt };
    }
    if (t === 'ineq-members') {
      if (!shown(p, chk.ineq)) return { status: 'invalid', msg: 'The inequality being checked is not the one printed for students.' };
      var cond = C.parseCondition(chk.ineq), yes = [];
      chk.values.forEach(function (vt) {
        if (!shown(p, vt)) throw new C.CheckError('value ' + vt + ' is not printed');
        var q = C.readNumber(vt); if (C.truth(cond, v, q)) yes.push(q);
      });
      var said = /none/i.test(C.plainText(ans)) && !C.snippets(ans).length ? [] : C.snippets(ans).map(function (x) { return C.readNumber(x.replace(/^[a-z]=/, '')); });
      var same = said.length === yes.length && said.every(function (q) { return yes.some(function (y) { return y.eq(q); }); });
      return same ? { status: 'verified' } : { status: 'mismatch', msg: 'Solutions: ' + (yes.length ? yes.join(', ') : 'none') + '.' };
    }
    if (t === 'error-line') {
      if (!shown(p, chk.ineq)) return { status: 'invalid', msg: 'The original inequality is not printed.' };
      var base = C.solutionSet(chk.ineq, v), first = 0;
      chk.lines.forEach(function (ln, i) { if (!shown(p, ln)) throw new C.CheckError('work line not printed: ' + ln); if (!first && !C.setEqual(C.solutionSet(ln, v), base)) first = i + 1; });
      if (!first) return { status: 'invalid', msg: 'The shown work has no mistake.' };
      var m = /line\s*(\d+)/i.exec(C.plainText(ans));
      return m && +m[1] === first ? { status: 'verified', computed: 'Line ' + first } : { status: 'mismatch', msg: 'The first wrong line is line ' + first + '.', computed: 'Line ' + first };
    }
    if (t === 'model-ineq' || t === 'iscenario') {
      var text = C.plainText(p.prompt), sc = ISCEN[chk.scenario](text, C.numbersInText(p.prompt));
      if (t === 'model-ineq') {
        var em = C.snippets(ans)[0]; if (!em) return { status: 'mismatch', msg: 'No inequality in the answer.' };
        var mset = C.solutionSet(em, chk.v);
        return C.setEqual(mset, sc.set) ? { status: 'verified' } : { status: 'mismatch', msg: 'The inequality does not model the situation.' };
      }
      if (chk.want === 'set') {
        var aset = C.setFromAnswer(ans, chk.v);
        return C.setEqual(aset, sc.set) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: ' + C.setText(sc.set, chk.v) };
      }
      var nums = C.numbersInText(ans);
      if (chk.want === 'best') {
        // the solved inequality written in the answer must also be right
        var sn = C.snippets(ans);
        if (sn.length) { var sset; try { sset = C.solutionSet(sn[0], chk.v); } catch (e) { return { status: 'mismatch', msg: 'Could not read the inequality in the answer.' }; }
          if (!C.setEqual(sset, sc.set)) return { status: 'mismatch', msg: 'The solved inequality should be ' + C.setText(sc.set, chk.v) + '.' }; }
      }
      if (chk.want === 'best') return nums.some(function (q) { return q.eq(sc.best); }) && new RegExp(sc.dir === 'max' ? 'at most|maximum|up to|no more' : 'at least|minimum|no fewer', 'i').test(C.plainText(ans)) ? { status: 'verified' } : { status: 'mismatch', msg: 'The ' + (sc.dir === 'max' ? 'most' : 'least') + ' is ' + sc.best + '.' };
      if (chk.want === 'range') { var ints = C.numbersInText(ans), a0 = ceilQ(sc.lo), b0 = floorQ(sc.hi); return ints.length >= 2 && ints[0].eq(a0) && ints[1].eq(b0) ? { status: 'verified' } : { status: 'mismatch', msg: 'Correct: from ' + a0 + ' to ' + b0 + '.' }; }
    }
    return { status: 'manual', msg: 'Unknown check ' + t };
  }

  /* Worked-solution steps must agree with the problem (same solution set / same expression). */
  function checkSteps(p) {
    var issues = [], first = (p.parts || [])[0];
    if (!first || !first.check) return issues;
    (p.steps || []).forEach(function (st, i) {
      if (!st.m || st.partial) return;
      try {
        if ((first.check.type === 'solve' || first.check.type === 'classify') && /=/.test(st.m) && !/[<>]/.test(st.m)) {
          var vars = Object.keys(Object.assign(C.varsOf(C.parseRelation(st.m).lhs), C.varsOf(C.parseRelation(st.m).rhs)));
          if (vars.length === 1 && vars[0] === first.check.v) {
            var a = C.solveLinear(first.check.eq, first.check.v), b = C.solveLinear(st.m, first.check.v);
            if (a.kind !== b.kind || (a.kind === 'one' && !a.value.eq(b.value))) issues.push('Step ' + (i + 1) + ' changes the solution.');
          }
        } else if (first.check.type === 'ineq' && /[<>]|\\le|\\ge/.test(st.m)) {
          if (!C.setEqual(C.solutionSet(st.m, first.check.v || 'x'), C.solutionSet(first.check.ineq, first.check.v || 'x'))) issues.push('Step ' + (i + 1) + ' changes the solution set.');
        } else if (first.check.type === 'simplify' && !/=/.test(st.m)) {
          if (!C.equivalent(first.check.expr, st.m)) issues.push('Step ' + (i + 1) + ' is not equivalent to the expression.');
        }
      } catch (e) { issues.push('Step ' + (i + 1) + ' could not be read: ' + e.message); }
    });
    return issues;
  }

  NS.verifyProblem = function (p, policy) {
    var issues = [], computed = [], statuses = [];
    (p.parts || []).forEach(function (part, i) {
      var res;
      try { res = checkPart(p, part, policy); }
      catch (e) { res = { status: 'invalid', msg: (e && e.message) || String(e) }; }
      statuses.push(res.status); computed.push(res.computed || null);
      if (res.msg && res.status !== 'verified') issues.push(((p.parts.length > 1 && part.label) ? '(' + part.label + ') ' : '') + res.msg);
    });
    if (!p.parts || !p.parts.length) { statuses.push('manual'); issues.push('No answer has been entered.'); }
    if (!p.edited) issues = issues.concat(checkSteps(p));
    var status = statuses.indexOf('invalid') >= 0 ? 'invalid' : statuses.indexOf('mismatch') >= 0 ? 'mismatch'
      : statuses.indexOf('manual') >= 0 ? 'manual' : 'verified';
    if (status === 'verified' && issues.length) status = 'mismatch';
    return { ok: status === 'verified', status: status, issues: issues, computed: computed };
  };
  NS.studentText = studentText;
})(typeof window !== 'undefined' ? window : globalThis);
