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
    return [p.prompt || ''].concat((p.parts || []).map(function (pt) { return pt.prompt || ''; })).join(' ');
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

  function checkPart(p, part, policy) {
    var chk = part.check, ans = part.answer || '';
    if (!chk || chk.type === 'none') return { status: 'manual', msg: 'No automatic check for this answer.' };
    var t = chk.type;
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

  /* Worked-solution steps must agree with the problem (same solution set / same expression). */
  function checkSteps(p) {
    var issues = [], first = (p.parts || [])[0];
    if (!first || !first.check) return issues;
    (p.steps || []).forEach(function (st, i) {
      if (!st.m) return;
      try {
        if ((first.check.type === 'solve' || first.check.type === 'classify') && /=/.test(st.m) && !/[<>]/.test(st.m)) {
          var vars = Object.keys(Object.assign(C.varsOf(C.parseRelation(st.m).lhs), C.varsOf(C.parseRelation(st.m).rhs)));
          if (vars.length === 1 && vars[0] === first.check.v) {
            var a = C.solveLinear(first.check.eq, first.check.v), b = C.solveLinear(st.m, first.check.v);
            if (a.kind !== b.kind || (a.kind === 'one' && !a.value.eq(b.value))) issues.push('Step ' + (i + 1) + ' changes the solution.');
          }
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
