/* Daily Lesson Planner — which verified skills practice each Algebra 1 lesson.

   lesson_id → { cover, skills, note }
     cover   'full'    the generators practice the whole objective
             'partial' they practice part of it (note says what is missing)
             'none'    no generator covers it yet (note says what to use instead)
     skills  [setKey, skillId, cmin, cmax]   cmin/cmax (optional) clamp the difficulty c (1–7) so the problem
             matches the lesson (e.g. U2-L1 one-step equations = the two-step skill at c = 1 only).
   setKey is a short name for a skill set in worksheet-generator/menu/skills/ (SETS below).
   tests/planner-tests.cjs checks every lesson in the scope & sequence is listed here and every skill exists. */
(function (G) {
  'use strict';
  var SETS = {
    F: 'algebra1-foundations', E: 'algebra1-expressions-equations', I: 'algebra1-inequalities',
    R: 'algebra1-relations-functions', L: 'algebra1-linear-equations-slope', S: 'algebra1-systems-of-equations',
    X: 'algebra1-exponents-scientific-notation', P: 'algebra1-exponential-functions', Y: 'algebra1-polynomials',
    Z: 'algebra1-factoring-zero-product', Q: 'algebra1-quadratics', D: 'algebra1-statistics-data-modeling'
  };
  /* The unit's own skill set (for links to the unit's Worksheet / Assessment / Printable generators). */
  var UNIT_SET = { 1: 'F', 2: 'E', 3: 'I', 4: 'R', 5: 'L', 6: 'S', 7: 'X', 8: 'P', 9: 'Y', 10: 'Z', 11: 'Q', 12: 'D' };
  function full(skills) { return { cover: 'full', skills: skills }; }
  function part(skills, note) { return { cover: 'partial', skills: skills, note: note }; }
  function none(note, related) { return { cover: 'none', skills: related || [], note: note }; }

  var L = {
    /* Unit 1 · Foundations of Algebra */
    'U1-L1': full([['F', 'verbal', 1, 7], ['F', 'evaluate', 1, 2]]),
    'U1-L2': full([['F', 'evaluate', 1, 7]]),
    'U1-L3': full([['F', 'real-numbers', 1, 7]]),
    'U1-L4': part([['F', 'evaluate', 2, 4]], 'Integer and fraction operations appear inside evaluating expressions; there is no generator for bare real-number arithmetic yet.'),
    'U1-L5': part([['F', 'distribute', 1, 3], ['F', 'like-terms', 1, 2]], 'Naming the property (commutative, associative, identity) has no generator yet; the problems use the properties.'),
    'U1-L6': full([['F', 'distribute', 1, 7], ['F', 'like-terms', 1, 7]]),
    'U1-L7': none('Interpreting the parts of an expression in context has no generator yet. The practice below reviews simplifying; add 2–3 context expressions to interpret.', [['F', 'like-terms', 2, 4], ['F', 'distribute', 2, 4]]),
    /* Unit 2 · Solving Linear Equations */
    'U2-L1': full([['E', 'two-step', 1, 1], ['E', 'fraction-eq', 1, 1]]),
    'U2-L2': full([['E', 'two-step', 2, 7], ['E', 'fraction-eq', 2, 3]]),
    'U2-L3': full([['E', 'multi-step', 1, 7], ['E', 'fraction-eq', 4, 7]]),
    'U2-L4': full([['E', 'both-sides', 1, 7]]),
    'U2-L5': full([['E', 'special-solutions', 1, 7]]),
    'U2-L6': full([['E', 'model', 1, 7]]),
    'U2-L7': full([['E', 'proportion', 1, 7], ['E', 'percent', 1, 7]]),
    'U2-L8': full([['E', 'literal', 1, 7]]),
    'U2-L9': full([['E', 'units', 1, 7]]),
    /* Unit 3 · Linear Inequalities */
    'U3-L1': full([['I', 'graph-read', 1, 5], ['I', 'check-values', 1, 3], ['I', 'apply', 1, 2]]),
    'U3-L2': full([['I', 'ineq-solve', 1, 7]]),
    'U3-L3': full([['I', 'ineq-multi', 1, 7], ['I', 'ineq-special', 1, 7]]),
    'U3-L4': full([['I', 'compound-and', 1, 7], ['I', 'compound-or', 1, 7]]),
    'U3-L5': full([['I', 'abs-eq', 1, 7], ['I', 'abs-ineq', 1, 7]]),
    'U3-L6': full([['I', 'apply', 1, 7]]),
    /* Unit 4 · Relations and Functions */
    'U4-L1': full([['R', 'domain-range', 1, 3], ['R', 'is-function', 1, 3]]),
    'U4-L2': full([['R', 'domain-range', 1, 7]]),
    'U4-L3': full([['R', 'is-function', 1, 7]]),
    'U4-L4': full([['R', 'func-eval', 1, 7], ['R', 'read-func', 1, 4]]),
    'U4-L5': full([['R', 'graph-behavior', 1, 7], ['R', 'read-func', 3, 7], ['R', 'curve-behavior', 1, 7]]),
    'U4-L6': part([['R', 'graph-behavior', 1, 7]], 'Students sketch graphs from stories; the generator only interprets graphs. Add 2 short stories to sketch.'),
    'U4-L7': part([['R', 'domain-range', 4, 7]], 'Discrete vs. continuous has no generator yet; ask whether each graphed domain makes sense as whole numbers or all reals.'),
    'U4-L8': full([['R', 'sequence', 1, 7]]),
    /* Unit 5 · Linear Functions and Graphing */
    'U5-L1': full([['R', 'rate-of-change', 1, 4], ['L', 'slope', 1, 3]]),
    'U5-L2': full([['L', 'slope', 1, 7]]),
    'U5-L3': full([['L', 'forms', 1, 2], ['L', 'write-line', 1, 1]]),
    'U5-L4': part([['L', 'forms', 1, 2], ['L', 'write-line', 5, 5]], 'Hand-drawn graphs are not checked; have students graph each line on the coordinate grid.'),
    'U5-L5': full([['L', 'forms', 4, 6]]),
    'U5-L6': full([['L', 'forms', 3, 3], ['L', 'write-line', 3, 4], ['L', 'write-line', 6, 6]]),
    'U5-L7': full([['L', 'write-line', 1, 7], ['R', 'linear-rule', 1, 7]]),
    'U5-L8': full([['L', 'parperp', 1, 7]]),
    'U5-L9': full([['L', 'lin-transform', 1, 7]]),
    'U5-L10': full([['L', 'line-model', 1, 7]]),
    'U5-L11': part([['R', 'linear-rule', 1, 7], ['R', 'rate-of-change', 3, 5]], 'Comparing two functions given in different forms has no generator yet; pair two of the problems and ask which grows faster.'),
    /* Unit 6 · Systems of Equations and Inequalities */
    'U6-L1': full([['S', 'sys-graph', 1, 3]]),
    'U6-L2': full([['S', 'sys-subst', 1, 7]]),
    'U6-L3': full([['S', 'sys-elim', 1, 2]]),
    'U6-L4': full([['S', 'sys-elim', 3, 5], ['S', 'sys-elim', 7, 7]]),
    'U6-L5': full([['S', 'sys-graph', 4, 4], ['S', 'sys-graph', 6, 7], ['S', 'sys-elim', 6, 6]]),
    'U6-L6': full([['S', 'sys-subst', 2, 5], ['S', 'sys-elim', 2, 5], ['S', 'sys-apply', 1, 3]]),
    'U6-L7': full([['S', 'sys-apply', 1, 7]]),
    'U6-L8': full([['S', 'sys-ineq', 1, 2], ['S', 'graph-hand', 1, 2]]),
    'U6-L9': full([['S', 'sys-ineq', 3, 6], ['S', 'graph-hand', 5, 7]]),
    'U6-L10': part([['S', 'sys-ineq', 7, 7], ['S', 'sys-apply', 2, 4], ['S', 'graph-hand', 5, 6]], 'Writing a constraint system from a situation is generated; graphing it in context (labelled axes, only whole-number points) is not. Have students graph one scenario.'),
    /* Unit 7 · Exponents and Scientific Notation */
    'U7-L1': full([['X', 'pow-product', 1, 7]]),
    'U7-L2': full([['X', 'pow-quotient', 1, 7], ['X', 'pow-eval', 2, 5]]),
    'U7-L3': full([['X', 'pow-product', 4, 7], ['X', 'pow-quotient', 5, 7]]),
    'U7-L4': full([['X', 'pow-eval', 6, 7], ['X', 'radicals', 1, 7]]),
    'U7-L5': full([['X', 'sci-convert', 1, 7]]),
    'U7-L6': full([['X', 'sci-ops', 1, 7]]),
    /* Unit 8 · Exponential Functions */
    'U8-L1': full([['P', 'lin-vs-exp', 1, 7]]),
    'U8-L2': full([['P', 'exp-graph', 1, 7], ['P', 'exp-eval', 1, 4]]),
    'U8-L3': full([['P', 'exp-identify', 1, 6], ['P', 'exp-apply', 1, 6]]),
    'U8-L4': full([['P', 'exp-identify', 1, 7], ['P', 'exp-apply', 2, 7]]),
    'U8-L5': full([['P', 'exp-write', 1, 7]]),
    'U8-L6': full([['P', 'exp-identify', 3, 5], ['P', 'exp-apply', 3, 5], ['P', 'compound', 1, 7]]),
    'U8-L7': full([['P', 'geo-seq', 1, 7]]),
    'U8-L8': part([['P', 'lin-vs-exp', 1, 7], ['P', 'exp-apply', 4, 6]], 'Comparing when an exponential model overtakes a linear one is not generated; add one table comparison.'),
    'U8-L9': full([['P', 'exp-solve', 1, 7]]),
    /* Unit 9 · Polynomials */
    'U9-L1': full([['Y', 'poly-classify', 1, 7]]),
    'U9-L2': full([['Y', 'poly-addsub', 1, 7]]),
    'U9-L3': full([['Y', 'poly-mult', 1, 1], ['Y', 'poly-mult', 3, 3]]),
    'U9-L4': full([['Y', 'poly-mult', 2, 2], ['Y', 'poly-mult', 4, 5]]),
    'U9-L5': full([['Y', 'poly-mult', 6, 7], ['Y', 'poly-special', 1, 7]]),
    'U9-L6': full([['Y', 'poly-closure', 1, 7], ['Y', 'poly-apply', 1, 7], ['Y', 'poly-divide', 1, 4]]),
    /* Unit 10 · Factoring and Zero Product Property */
    'U10-L1': full([['Z', 'gcf', 1, 2], ['Z', 'gcf', 4, 4]]),
    'U10-L2': full([['Z', 'gcf', 3, 3], ['Z', 'gcf', 5, 6]]),
    'U10-L3': full([['Z', 'tri-a1', 1, 4]]),
    'U10-L4': full([['Z', 'tri-a', 1, 7]]),
    'U10-L5': full([['Z', 'special', 1, 7]]),
    'U10-L6': full([['Z', 'gcf', 7, 7], ['Z', 'tri-a1', 5, 7], ['Z', 'special', 5, 7], ['Z', 'two-var', 1, 7], ['Z', 'cubes', 1, 7]]),
    'U10-L7': full([['Z', 'zero-product', 1, 2]]),
    'U10-L8': full([['Z', 'zero-product', 3, 7]]),
    'U10-L9': full([['Z', 'factor-apply', 1, 7]]),
    /* Unit 11 · Quadratic Functions and Equations */
    'U11-L1': full([['Q', 'q-features', 1, 2], ['Q', 'q-features', 4, 4]]),
    'U11-L2': full([['Q', 'q-features', 3, 3], ['Q', 'q-features', 6, 7], ['Q', 'q-graph', 5, 7]]),
    'U11-L3': full([['Q', 'q-features', 5, 5], ['Q', 'q-complete', 6, 7], ['Q', 'q-transform', 1, 7], ['Q', 'q-graph', 1, 4]]),
    'U11-L4': part([['Q', 'q-features', 2, 2], ['Z', 'zero-product', 3, 4]], 'Converting between forms is only partly generated (zeros from factored form).'),
    'U11-L5': part([['Q', 'q-features', 2, 2]], 'Solving by graphing uses graphed parabolas only; have students check each zero by substitution.'),
    'U11-L6': full([['Q', 'q-roots', 1, 4], ['Q', 'q-roots', 6, 6]]),
    'U11-L7': full([['Q', 'q-complete', 1, 5]]),
    'U11-L8': full([['Q', 'q-formula', 3, 7]]),
    'U11-L9': full([['Q', 'q-formula', 1, 2]]),
    'U11-L10': full([['Q', 'q-roots', 1, 7], ['Q', 'q-formula', 3, 7], ['Q', 'q-complete', 2, 5]]),
    'U11-L11': full([['Q', 'q-apply', 1, 7], ['Z', 'factor-apply', 3, 5]]),
    'U11-L12': part([['P', 'lin-vs-exp', 1, 7]], 'Quadratic patterns (constant second differences) are not generated; add one table that is quadratic.'),
    /* Unit 12 · Statistics and Data Modeling */
    'U12-L1': full([['D', 'center', 1, 3]]),
    'U12-L2': full([['D', 'boxplot', 1, 7], ['D', 'histogram', 1, 7]]),
    'U12-L3': full([['D', 'boxplot', 5, 7], ['D', 'spread', 4, 7]]),
    'U12-L4': full([['D', 'twoway', 1, 7]]),
    'U12-L5': full([['D', 'scatter', 1, 1]]),
    'U12-L6': full([['D', 'scatter', 2, 5]]),
    'U12-L7': full([['D', 'causation', 1, 7], ['D', 'scatter', 1, 1], ['D', 'regression', 2, 3]]),
    'U12-L8': full([['D', 'scatter', 4, 4], ['D', 'scatter', 6, 7], ['D', 'regression', 4, 7]]),
  };
  /* Day 2's diagnostic (and Do Nows that point back to it): pre-algebra readiness. */
  L['LAUNCH-2'] = { cover: 'full', skills: [['F', 'evaluate', 1, 2], ['F', 'like-terms', 1, 1], ['F', 'distribute', 1, 1], ['E', 'two-step', 1, 2], ['E', 'proportion', 1, 1]] };

  G.MKPLAN_SKILLS = { SETS: SETS, UNIT_SET: UNIT_SET, lessons: L };
})(typeof window !== 'undefined' ? window : globalThis);
