/* Helpers shared by the Linear Functions lessons. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, T = NS.tex, gen = NS.gen;
  var M = T.M, num = T.num, numP = T.numP, pt = T.pt, lin = T.lin;

  var LF = NS.lf = {};
  LF.UNIT = 'algebra1-linear-functions';
  LF.W10 = { xmin: -10, xmax: 10, ymin: -10, ymax: 10 };
  LF.W8 = { xmin: -8, xmax: 8, ymin: -8, ymax: 8 };

  LF.spec = function (win, lines, points) {
    return { xmin: win.xmin, xmax: win.xmax, ymin: win.ymin, ymax: win.ymax, lines: lines || [], points: points || [] };
  };
  LF.line = function (m, b) { return { kind: 'line', m: Fr.of(m), b: Fr.of(b) }; };
  LF.vline = function (x) { return { kind: 'vline', x: Fr.of(x) }; };
  LF.yAt = function (m, b, x) { return Fr.of(m).mul(x).add(b); };

  /* "(x, 16)" style points where one coordinate may be a variable letter */
  LF.ptVar = function (a, b) {
    function c(v) { return typeof v === 'string' ? v : num(v); }
    return '(' + c(a) + ',\\,' + c(b) + ')';
  };
  /* n(inner) with 1 and -1 handled */
  LF.coefTimes = function (n, inner) {
    n = Fr.of(n);
    if (n.eq(1)) return inner;
    if (n.eq(-1)) return '-(' + inner + ')';
    return num(n) + '(' + inner + ')';
  };

  /* Worked steps for the slope formula between two lattice points. */
  LF.slopeSteps = function (p1, p2) {
    var x1 = p1[0], y1 = p1[1], x2 = p2[0], y2 = p2[1];
    var dy = Fr.of(y2).sub(y1), dx = Fr.of(x2).sub(x1), m = dy.div(dx);
    var third = 'm=' + T.litFrac(num(dy), num(dx));
    var steps = [
      'Use the slope formula: ' + M('m=\\frac{y_2-y_1}{x_2-x_1}'),
      'Substitute ' + M('(x_1,\\,y_1)=' + pt(x1, y1)) + ' and ' + M('(x_2,\\,y_2)=' + pt(x2, y2)) + ': ' +
        M('m=\\frac{' + num(y2) + '-' + numP(y1) + '}{' + num(x2) + '-' + numP(x1) + '}'),
      'Simplify: ' + M(third + (T.litFrac(num(dy), num(dx)) !== num(m) ? '=' + num(m) : ''))
    ];
    return steps;
  };

  /* Steps that find b from m and a point, ending in y = mx + b.  Returns {steps, b}. */
  LF.findBSteps = function (m, x1, y1) {
    m = Fr.of(m);
    var prod = m.mul(x1), b = Fr.of(y1).sub(prod);
    var steps = [];
    steps.push('Substitute the slope and the point ' + M(pt(x1, y1)) + ' into ' + M('y=mx+b') + ': ' +
      M(num(y1) + '=' + num(m) + '(' + num(x1) + ')+b'));
    steps.push('Multiply: ' + M(num(y1) + '=' + (prod.isZero() ? '0' : num(prod)) + '+b'));
    if (prod.isZero()) steps.push('Solve for ' + M('b') + ': ' + M('b=' + num(b)));
    else steps.push('Solve for ' + M('b') + ': ' + M('b=' + num(y1) + (prod.sign() < 0 ? '+' + num(prod.abs()) : '-' + num(prod)) + '=' + num(b)));
    steps.push('Write the equation: ' + M(T.eqSI(m, b)));
    return { steps: steps, b: b };
  };

  /* Rise/run phrase for a slope n/d: "up 3, right 2" */
  LF.riseRun = function (m) {
    m = Fr.of(m);
    return (m.n >= 0 ? 'up ' : 'down ') + Math.abs(m.n) + ' and right ' + m.d;
  };

  /* Unit-fraction display used for perpendicular slopes. */
  LF.negRecip = function (m) { return Fr.of(m).inv().neg(); };

  LF.pairKey = function (pts) { return pts.map(function (p) { return p.join(','); }).sort().join('|'); };
})(typeof window !== 'undefined' ? window : globalThis);
