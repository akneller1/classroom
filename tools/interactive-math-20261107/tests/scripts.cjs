// One step per "Try this" challenge, in order. Each step uses the real controls a student would use.
const R = 'ArrowRight', Lf = 'ArrowLeft', U = 'ArrowUp', D = 'ArrowDown';
module.exports = {
  'math6-ratio-double-number-line': [
    async (p, H) => H.keys(p, 'Marker on the double number line', Lf, 10),          // k = 1/3: top = 1
    async (p, H) => H.keys(p, 'Marker on the double number line', Lf, 2),           // k = 1/5: bottom = 1
    async (p, H) => { await H.num(p, 'test-top', 24); await H.num(p, 'test-bottom', 40); },
    async (p, H) => { await H.num(p, 'test-top', 5); await H.num(p, 'test-bottom', 7); },
    async (p, H) => H.slider(p, 'top-amount', 4)
  ],
  'math6-fraction-division-groups': [
    async (p, H) => H.slider(p, 'divisor-numerator', 1),                               // 3 ÷ 1/2 = 6
    async (p, H) => {},                                                                 // 6 > 3 already a counterexample
    async (p, H) => { await H.slider(p, 'dividend-numerator', 2); await H.slider(p, 'divisor-numerator', 3); await H.slider(p, 'divisor-denominator', 4); },
    async (p, H) => { await H.slider(p, 'dividend-denominator', 2); await H.slider(p, 'dividend-numerator', 1); },
    async (p, H) => { await H.slider(p, 'dividend-denominator', 1); await H.slider(p, 'dividend-numerator', 4); await H.slider(p, 'divisor-numerator', 3); await H.slider(p, 'divisor-denominator', 2); }
  ],
  'math6-area-shear-lab': [
    async (p, H) => H.keys(p, 'Top corner (lean and height)', R, 3),
    async (p, H) => {},                                                                 // 6 × 4 with a lean of 3
    async (p, H) => { await H.slider(p, 'base', 8); await H.slider(p, 'height', 1); await H.slider(p, 'lean', 8); },
    async (p, H) => { await H.chip(p, 'Triangle'); await H.btn(p, 'Show the copy'); },
    async (p, H) => { await H.slider(p, 'base', 6); await H.slider(p, 'height', 4); await H.slider(p, 'lean', 8); }
  ],
  'math6-balance-point-dot-plot': [
    async (p, H) => H.keys(p, 'Data value 9', R, 7),
    async (p, H) => { await H.keys(p, 'Data value 8', R, 1); await H.keys(p, 'Data value 1', R, 10); },
    async (p, H) => H.btn(p, 'Show distances from the mean'),
    async (p, H) => { await H.btn(p, '↺ Reset'); await H.keys(p, 'Data value 1', Lf, 5); await H.keys(p, 'Data value 9', R, 5); await H.keys(p, 'Data value 2', Lf, 5); await H.keys(p, 'Data value 8', R, 5); await H.keys(p, 'Data value 3', Lf, 4); await H.keys(p, 'Data value 7', R, 4); },
    async (p, H) => { await H.btn(p, '↺ Reset'); await H.keys(p, 'Data value 1', Lf, 5); await H.keys(p, 'Data value 2', Lf, 6); await H.keys(p, 'Data value 3', Lf, 6); await H.keys(p, 'Data value 4', Lf, 7);
      await H.keys(p, 'Data value 5', R, 4); await H.keys(p, 'Data value 6', R, 4); await H.keys(p, 'Data value 7', R, 3); await H.keys(p, 'Data value 8', R, 2); await H.keys(p, 'Data value 9', Lf, 1); }
  ],
  'prealgebra7-proportional-relationships': [
    async (p, H) => H.keys(p, 'Point on your line', Lf, 4),
    async (p, H) => H.slider(p, 'price-per-pound', 2.5),
    async (p, H) => { await H.slider(p, 'bag-fee', 2); await H.keys(p, 'Point on your line', R, 2); await H.keys(p, 'Point on your line', R, 2); },
    async (p, H) => {},                                                                 // $2.50/lb + $2 fee crosses Store B at 4 lb
    async (p, H) => { await H.slider(p, 'bag-fee', 0); await H.slider(p, 'price-per-pound', 3); }
  ],
  'prealgebra7-percent-change-bar': [
    async (p, H) => { await H.chip(p, 'Decrease (discount)'); await H.slider(p, 'first-percent', 30); },
    async (p, H) => { await H.chip(p, 'Increase (markup, tax, tip)'); await H.slider(p, 'first-percent', 30); await H.slider(p, 'original-amount', 120); await H.slider(p, 'first-percent', 20); },
    async (p, H) => { await H.chip(p, 'Then decrease'); await H.slider(p, 'second-percent', 20); },
    async (p, H) => { await H.slider(p, 'first-percent', 25); },
    async (p, H) => { await H.chip(p, 'Then increase'); await H.slider(p, 'first-percent', 10); await H.slider(p, 'second-percent', 20); }
  ],
  'prealgebra7-spinner-probability-lab': [
    async (p, H) => H.slider(p, 'red-parts', 1),
    async (p, H) => { for (let i = 0; i < 40; i++) { await H.btn(p, 'Clear results'); await H.btn(p, 'Spin 10'); const d = await H.done(p); if (d[1]) break; } },
    async (p, H) => { await H.btn(p, 'Clear results'); await H.btn(p, 'Spin 100'); await H.btn(p, 'Spin 100'); },
    async (p, H) => { for (let i = 0; i < 40; i++) { await H.btn(p, 'Spin 1,000'); const d = await H.done(p); if (d[3]) break; } },
    async (p, H) => { await H.slider(p, 'blue-parts', 0); await H.slider(p, 'blue-parts', 1); await H.slider(p, 'red-parts', 0); await H.slider(p, 'green-parts', 0); }
  ],
  'prealgebra-pythagorean-squares': [
    async (p, H) => H.keys(p, 'Corner C', Lf, 2),
    async (p, H) => { await H.keys(p, 'Corner B', Lf, 3); await H.keys(p, 'Corner B', U, 1); await H.keys(p, 'Corner C', Lf, 1); await H.keys(p, 'Corner C', D, 2); await H.btn(p, 'Show the tilted-square trick'); },
    async (p, H) => { await H.keys(p, 'Corner C', R, 10); await H.keys(p, 'Corner C', D, 1); },
    async (p, H) => { await H.keys(p, 'Corner C', Lf, 7); await H.keys(p, 'Corner C', U, 1); },
    async (p, H) => { await H.keys(p, 'Corner B', D, 1); await H.keys(p, 'Corner B', R, 5); await H.keys(p, 'Corner C', Lf, 2); await H.keys(p, 'Corner C', U, 3); },
    async (p, H) => { await H.keys(p, 'Corner B', Lf, 7); await H.keys(p, 'Corner C', D, 5); }
  ],
  'prealgebra-square-roots-number-line': [
    async (p, H) => H.slider(p, 'square-area', 64),
    async (p, H) => { await H.slider(p, 'square-area', 20); await H.btn(p, '🔍 Zoom in'); },
    async (p, H) => { await H.num(p, 'area-box', 50); await H.btn(p, '🔍 Zoom in'); },
    async (p, H) => { await H.slider(p, 'square-area', 20); await H.num(p, 'estimate', 4.47); },
    async (p, H) => { await H.slider(p, 'square-area', 2); for (let i = 0; i < 3; i++) await H.btn(p, '🔍 Zoom in'); }
  ],
  'precalculus-vector-explorer': [
    async (p, H) => H.keys(p, 'Tip of u', U, 4),
    async (p, H) => { await H.keys(p, 'Tip of v', Lf, 10); await H.keys(p, 'Tip of v', D, 12); },
    async (p, H) => { await H.keys(p, 'Tip of v', R, 12); await H.keys(p, 'Tip of v', U, 9); },
    async (p, H) => { await H.keys(p, 'Tip of v', Lf, 10); await H.keys(p, 'Tip of v', D, 8); },
    async (p, H) => { await H.chip(p, 'u − v'); await H.keys(p, 'Tip of v', R, 6); await H.keys(p, 'Tip of v', U, 11); },
    async (p, H) => { await H.keys(p, 'Tip of u', D, 6); await H.chip(p, 'k · u'); await H.slider(p, 'scalar-k', 0.25); }
  ],
  'calculus-limit-explorer': [
    async (p, H) => H.slider(p, 'distance-h', 3),
    async (p, H) => { await H.chip(p, 'Moved point'); await H.slider(p, 'value-at-a', 4); await H.slider(p, 'value-at-a', 6); },
    async (p, H) => H.slider(p, 'value-at-a', 3),
    async (p, H) => { await H.chip(p, 'Jump'); await H.btn(p, 'Reveal the limits'); },
    async (p, H) => { await H.chip(p, 'Oscillation'); for (let i = 0; i < 4; i++) await H.btn(p, '🔍 Zoom in'); },
    async (p, H) => { await H.chip(p, 'Vertical asymptote'); await H.slider(p, 'distance-h', 4); }
  ],
  'calculus-secant-to-tangent': [
    async (p, H) => H.slider(p, 'step-h', 6),                                           // h = 0.01
    async (p, H) => H.slider(p, 'step-h', 3),                                           // h = -0.01 at the same a
    async (p, H) => { await H.chip(p, 'x³ − 3x'); await H.slider(p, 'point-a', 1); await H.slider(p, 'point-a', -1); },
    async (p, H) => { await H.chip(p, '|x|'); await H.slider(p, 'point-a', 0); await H.slider(p, 'step-h', 6); await H.slider(p, 'step-h', 3); },
    async (p, H) => { await H.chip(p, 'sin x'); for (const a of [-3, -2, -1, 0, 1, 2, 3, 0.5]) await H.slider(p, 'point-a', a); },
    async (p, H) => { await H.chip(p, 'eˣ'); for (const a of [0, 1, 2]) await H.slider(p, 'point-a', a); }
  ],
  'calculus-riemann-sum-lab': [
    async (p, H) => H.slider(p, 'subintervals-n', 100),
    async (p, H) => { await H.chip(p, '4 − x²'); await H.slider(p, 'subintervals-n', 4); await H.slider(p, 'upper-limit-b', 2); },
    async (p, H) => { await H.chip(p, 'sin x'); await H.slider(p, 'lower-limit-a', -3); await H.slider(p, 'upper-limit-b', 3); },
    async (p, H) => { await H.chip(p, '4 − x²'); await H.slider(p, 'lower-limit-a', 2); await H.slider(p, 'upper-limit-b', 4); },
    async (p, H) => { await H.chip(p, 'Midpoint'); await H.slider(p, 'subintervals-n', 4); }
  ],
  'calculus-accumulation-ftc': [
    async (p, H) => H.slider(p, 'upper-x', 2),
    async (p, H) => H.slider(p, 'upper-x', 4),
    async (p, H) => { await H.chip(p, '2 sin t'); await H.slider(p, 'upper-x', 1.6); },
    async (p, H) => H.slider(p, 'lower-a', 0.5),
    async (p, H) => { await H.chip(p, 'piecewise'); await H.slider(p, 'lower-a', 0); await H.slider(p, 'upper-x', 1.7); }
  ]
};
