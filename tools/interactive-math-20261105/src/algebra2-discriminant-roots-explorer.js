var st = { a: 1, b: -2, c: -3, seen: {} };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Graph of the quadratic' });
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>' + L.V('y') + ' = ' + L.V('ax') + '² + ' + L.V('bx') + ' + ' + L.V('c') + '</span><span><i style="background:var(--green)"></i>real roots</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
L.slider(P.panel, { id: 'a', label: 'a', min: -3, max: 3, step: 0.5, value: st.a, color: 'purple', format: function (v) { return L.nice(v); }, onInput: function (v) { st.a = v; draw(); } });
L.slider(P.panel, { id: 'b', label: 'b', min: -8, max: 8, value: st.b, color: 'orange', format: L.num, onInput: function (v) { st.b = v; draw(); } });
L.slider(P.panel, { id: 'c', label: 'c', min: -8, max: 12, value: st.c, color: 'green', format: L.num, onInput: function (v) { st.c = v; draw(); } });
L.h('h2', null, P.panel, 'Roots on the complex plane');
var cp = L.graph(P.panel, { xmin: -6, xmax: 6, ymin: -4.5, ymax: 4.5, width: 400, height: 300, xstep: 1, ystep: 1, label: 'Complex plane: real part across, imaginary part up', yfmt: function (t) { return L.num(t) + 'i'; } });
var ch = L.challenges(P.panel, [
  { text: 'Make a quadratic with two real roots.', check: function () { return st.seen.two; } },
  { text: 'Make the discriminant exactly 0. How many roots are there?', check: function () { return st.seen.one; } },
  { text: 'Lift the parabola off the ' + L.V('x') + '-axis so the roots become complex.', check: function () { return st.seen.complex; } },
  { text: 'Make the roots ±2' + L.V('i') + '.', check: function () { return st.a !== 0 && st.b === 0 && Math.abs(st.c / st.a - 4) < 1e-9; } },
  { text: 'Make the roots 1 ± ' + L.V('i') + '.', check: function () { return st.a !== 0 && Math.abs(st.b / st.a + 2) < 1e-9 && Math.abs(st.c / st.a - 2) < 1e-9; } }
]);
function sqrtParts(n) { // √n = out·√inside for a positive integer n
  var out = 1, inside = n;
  for (var f = 2; f * f <= inside; f++) while (inside % (f * f) === 0) { inside /= f * f; out *= f; }
  return [out, inside];
}
var draw = L.scheduler(function () {
  var a = st.a, b = st.b, c = st.c;
  g.clear(); cp.clear();
  if (a === 0) { g.fn(function (x) { return b * x + c; }, { color: 'blue' }); read.innerHTML = '<span class="c-red">With ' + L.V('a') + ' = 0 there is no ' + L.V('x') + '² term, so it isn\'t quadratic.</span>'; ch.update(); return; }
  g.fn(function (x) { return a * x * x + b * x + c; }, { color: 'blue' });
  var D = b * b - 4 * a * c, re = -b / (2 * a), roots;
  if (D > 1e-9) { var r = Math.sqrt(D) / (2 * Math.abs(a)); roots = [[re - r, 0], [re + r, 0]]; st.seen.two = true; }
  else if (Math.abs(D) <= 1e-9) { roots = [[re, 0]]; st.seen.one = true; }
  else { var im = Math.sqrt(-D) / (2 * Math.abs(a)); roots = [[re, im], [re, -im]]; st.seen.complex = true; }
  roots.forEach(function (z) {
    if (!z[1]) g.dot(z[0], 0, { color: 'green', r: 9, stroke: 'ink', strokeWidth: 2 });
    cp.dot(z[0], z[1], { color: z[1] ? 'purple' : 'green', r: 8, stroke: 'ink', strokeWidth: 2 });
  });
  if (roots.length === 2 && roots[0][1]) cp.line(roots[0][0], roots[0][1], roots[1][0], roots[1][1], { color: 'purple', width: 2, dash: '5 5' });
  // exact form when 2a divides nicely
  var twoA = 2 * a, rootText;
  var Dint = Math.abs(D - Math.round(D)) < 1e-9 && Number.isInteger(a) && Number.isInteger(b);
  if (Dint) {
    var Dabs = Math.round(Math.abs(D)), sp = sqrtParts(Dabs), out = sp[0], ins = sp[1];
    var nm = -b, dn = 2 * a; if (dn < 0) { nm = -nm; dn = -dn; }
    if (D !== 0 && ins === 1 && D > 0) rootText = L.V('x') + ' = ' + L.nice(roots[0][0]) + ' or ' + L.V('x') + ' = ' + L.nice(roots[1][0]);
    else if (D === 0) rootText = L.V('x') + ' = ' + L.nice(re);
    else {
      var gg = L.gcd(L.gcd(nm, out), dn); nm /= gg; out /= gg; dn /= gg;
      var rad = (ins === 1 ? (out === 1 && D < 0 ? '' : out) : (out === 1 ? '' : out) + '√' + ins) + (D < 0 ? L.V('i') : '');
      var top = (nm ? L.num(nm) + ' ± ' : '±') + rad;
      rootText = L.V('x') + ' = ' + (dn === 1 ? top : L.frac(top, dn));
    }
  } else rootText = roots.map(function (z) { return L.num(z[0]) + (z[1] ? (z[1] > 0 ? ' + ' : ' − ') + L.num(Math.abs(z[1])) + L.V('i') : ''); }).join(', ');
  read.innerHTML = L.V('y') + ' = ' + L.terms([[a, 'x²'], [b, 'x'], [c, '']]) +
    '<div class="sub" style="margin-top:6px">Discriminant ' + L.V('b') + '² − 4' + L.V('ac') + ' = ' + L.num(b * b) + ' − ' + (4 * a * c < 0 ? '(' + L.num(4 * a * c) + ')' : L.num(4 * a * c)) + ' = <b>' + L.num(D) + '</b></div>' +
    '<div style="margin-top:6px">' + (D > 0 ? 'Two real roots' : D === 0 ? 'One repeated real root' : 'Two complex roots, a conjugate pair') + '</div><div style="margin-top:4px">' + rootText + '</div>';
  ch.update();
});
draw();
