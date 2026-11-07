// One step per "Try this" challenge, in order, using the real controls. Pages load with ?seed=20261108 so runs repeat exactly.
const R = 'ArrowRight', Lf = 'ArrowLeft', U = 'ArrowUp', D = 'ArrowDown';
module.exports = {
  'statistics-random-assignment-lab': [
    async (p, H) => { await H.chip(p, 'Students choose'); await H.btn(p, 'Repeat 100 times'); await H.btn(p, 'Repeat 100 times'); },
    async (p, H) => { await H.chip(p, 'Random assignment'); await H.btn(p, 'Repeat 100 times'); await H.btn(p, 'Repeat 100 times'); },
    async (p, H) => { for (let i = 0; i < 80; i++) { await H.btn(p, 'Assign once'); if ((await H.done(p))[2]) break; } },
    async (p, H) => { await H.chip(p, 'Randomized pairs (matched on GPA)'); await H.btn(p, 'Repeat 100 times'); await H.btn(p, 'Repeat 100 times'); },
    async (p, H) => { await H.tab(p, 'Randomization test'); await H.btn(p, 'Run a new experiment'); await H.btn(p, 'Re-randomize 1,000 times'); },
    async (p, H) => { await H.slider(p, 'true-effect', 12); for (let i = 0; i < 10; i++) { await H.btn(p, 'Run a new experiment'); await H.btn(p, 'Re-randomize 1,000 times'); if ((await H.done(p))[5]) break; } }
  ],
  'statistics-sampling-distribution-lab': [
    async (p, H) => { await H.slider(p, 'sample-size', 1); await H.btn(p, 'Draw 1,000'); },
    async (p, H) => { await H.slider(p, 'sample-size', 100); await H.btn(p, 'Draw 1,000'); },
    async (p, H) => { await H.slider(p, 'sample-size', 25); await H.btn(p, 'Draw 1,000'); },
    async (p, H) => { await H.chip(p, 'Bimodal'); await H.slider(p, 'sample-size', 50); await H.btn(p, 'Draw 1 sample'); },
    async (p, H) => { await H.chip(p, 'Sample proportion p̂'); await H.slider(p, 'population-p', 0.1); await H.slider(p, 'sample-size', 20); await H.btn(p, 'Draw 1,000'); await H.slider(p, 'sample-size', 100); await H.btn(p, 'Draw 1,000'); }
  ],
  'statistics-confidence-interval-lab': [
    async (p, H) => H.btn(p, 'Make 100'),
    async (p, H) => { await H.chip(p, '90%'); await H.btn(p, 'Make 20'); await H.chip(p, '99%'); await H.btn(p, 'Make 20'); },
    async (p, H) => { await H.slider(p, 'sample-size', 160); await H.btn(p, 'Make 20'); },
    async (p, H) => { await H.chip(p, '95%'); await H.slider(p, 'true-p', 0.05); await H.slider(p, 'sample-size', 40); await H.btn(p, 'Make 100'); await H.btn(p, 'Make 100'); },
    async (p, H) => { await H.chip(p, 'Mean μ'); await H.slider(p, 'sample-size', 5); await H.chip(p, 'z* with s'); await H.btn(p, 'Make 100'); await H.btn(p, 'Make 100'); await H.chip(p, 't* (df = n − 1)'); await H.btn(p, 'Make 100'); await H.btn(p, 'Make 100'); }
  ],
  'statistics-significance-power-explorer': [
    async (p, H) => H.slider(p, 'successes', 60),
    async (p, H) => H.chip(p, 'p ≠ p₀'),
    async (p, H) => { await H.chip(p, 'p > p₀'); await H.slider(p, 'successes', 55); await H.slider(p, 'sample-size', 400); },
    async (p, H) => { await H.tab(p, 'Errors & power'); await H.slider(p, 'true-p', 0.6); for (let n = 10; n <= 400; n += 10) { await H.slider(p, 'sample-size', n); if ((await H.done(p))[3]) break; } },
    async (p, H) => H.chip(p, 'α = 0.01'),
    async (p, H) => H.slider(p, 'true-p', 0.5)
  ],
  'statistics-sampling-methods-lab': [
    async (p, H) => { for (let i = 0; i < 3; i++) await H.btn(p, 'Take 1 sample'); },
    async (p, H) => { await H.chip(p, 'Convenience (nearest the door)'); await H.btn(p, 'Take 100 samples'); await H.btn(p, 'Take 100 samples'); },
    async (p, H) => { await H.chip(p, '64'); await H.btn(p, 'Take 100 samples'); await H.btn(p, 'Take 100 samples'); },
    async (p, H) => { await H.chip(p, 'Simple random sample'); await H.chip(p, '16'); await H.btn(p, 'Take 100 samples'); await H.btn(p, 'Take 100 samples'); await H.chip(p, 'Stratified by grade'); await H.btn(p, 'Take 100 samples'); await H.btn(p, 'Take 100 samples'); },
    async (p, H) => { await H.chip(p, 'Cluster (whole homerooms)'); await H.btn(p, 'Take 100 samples'); await H.btn(p, 'Take 100 samples'); }
  ],
  'statistics-conditional-probability-explorer': [
    async (p, H) => { await H.slider(p, 'prevalence', 3); await H.slider(p, 'sensitivity', 99); await H.slider(p, 'specificity', 99); },
    async (p, H) => H.slider(p, 'prevalence', 6),
    async (p, H) => { await H.slider(p, 'prevalence', 3); await H.slider(p, 'specificity', 90); },
    async (p, H) => { await H.slider(p, 'prevalence', 5); await H.slider(p, 'specificity', 99.5); },
    async (p, H) => { await H.slider(p, 'sensitivity', 50); await H.slider(p, 'specificity', 50); }
  ],
  'statistics-regression-influence-lab': [
    async (p, H) => H.chip(p, 'Age and height (one child)'),
    async (p, H) => { await H.chip(p, 'Study time and test score'); await H.btn(p, 'Add an extra point'); await H.keys(p, 'Extra point', Lf, 2); },
    async (p, H) => { await H.keys(p, 'Extra point', R, 8); await H.keys(p, 'Extra point', D, 30); },
    async (p, H) => H.keys(p, 'Extra point', U, 97),
    async (p, H) => H.chip(p, 'minutes')
  ]
};
