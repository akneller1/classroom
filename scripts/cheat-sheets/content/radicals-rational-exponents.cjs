const F = require('../figs.cjs');
module.exports = {
  name: 'radicals-rational-exponents', course: 'Algebra 2', unitNo: 5, unitName: 'Radicals & Rational Exponents',
  focus: 'simplifying radicals, radical operations, rational exponents and converting between forms',
  morefocus: 'radical equations, extraneous solutions, and square-root and cube-root graphs',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['index', 'The small ⟨n⟩ in ⟨\\sqrt[n]{a}⟩ (2 if not written).', '⟨\\sqrt[3]{8}⟩: 3'], ['radicand', 'The expression under the radical sign.', '⟨\\sqrt{5x}⟩: ⟨5x⟩'],
      ['rational exponent', '⟨a^{m/n} = \\sqrt[n]{a^m} = (\\sqrt[n]{a})^m⟩.', '⟨8^{2/3} = 4⟩'], ['like radicals', 'Same index and same radicand.', '⟨2\\sqrt{3},\\ 7\\sqrt{3}⟩'],
      ['extraneous solution', 'Solves a step but not the original equation.', 'check it!']], check: { num: 'Math.round(Math.cbrt(8)**2)', is: 4 } },
    { title: 'Simplifying Radicals', color: 'blue', kind: 'words', rows: [
      ['⟨\\sqrt{72} = \\sqrt{36 \\cdot 2}⟩', '⟨6\\sqrt{2}⟩'], ['⟨\\sqrt[3]{54} = \\sqrt[3]{27 \\cdot 2}⟩', '⟨3\\sqrt[3]{2}⟩'], ['⟨\\sqrt{50x^3}⟩ ⟨(x \\ge 0)⟩', '⟨5x\\sqrt{2x}⟩'], ['⟨\\sqrt[4]{32} = \\sqrt[4]{16 \\cdot 2}⟩', '⟨2\\sqrt[4]{2}⟩']],
      check: [{ num: 'Math.sqrt(72)', is: 6 * Math.SQRT2 }, { num: 'Math.cbrt(54)', is: 3 * Math.cbrt(2) }, { num: 'Math.sqrt(50*2.3**3)', is: 5 * 2.3 * Math.sqrt(4.6) }, { num: '32**0.25', is: 2 * 2 ** 0.25 }] },
    { title: 'Radical Operations', color: 'green', kind: 'words', rows: [
      ['Add: ⟨3\\sqrt{12} + \\sqrt{27} = 6\\sqrt{3} + 3\\sqrt{3}⟩', '⟨9\\sqrt{3}⟩'], ['Multiply: ⟨(2 + \\sqrt{3})(2 - \\sqrt{3})⟩', '⟨1⟩'],
      ['Rationalize: ⟨\\tfrac{6}{\\sqrt{3}} \\cdot \\tfrac{\\sqrt{3}}{\\sqrt{3}}⟩', '⟨2\\sqrt{3}⟩'], ['Conjugate: ⟨\\tfrac{4}{3 - \\sqrt{5}} \\cdot \\tfrac{3 + \\sqrt{5}}{3 + \\sqrt{5}} = \\tfrac{4(3 + \\sqrt{5})}{4}⟩', '⟨3 + \\sqrt{5}⟩']],
      check: [{ num: '3*Math.sqrt(12)+Math.sqrt(27)', is: 9 * Math.sqrt(3) }, { num: '(2+Math.sqrt(3))*(2-Math.sqrt(3))', is: 1 }, { num: '6/Math.sqrt(3)', is: 2 * Math.sqrt(3) }, { num: '4/(3-Math.sqrt(5))', is: 3 + Math.sqrt(5) }] },
    { title: 'Rational Exponents', color: 'orange', kind: 'table', head: ['Expression', 'Meaning', 'Value'], rows: [
      ['⟨27^{1/3}⟩', '⟨\\sqrt[3]{27}⟩', '⟨3⟩'], ['⟨8^{2/3}⟩', '⟨(\\sqrt[3]{8})^2⟩', '⟨4⟩'], ['⟨16^{-3/4}⟩', '⟨\\dfrac{1}{(\\sqrt[4]{16})^3}⟩', '⟨\\tfrac{1}{8}⟩'], ['⟨(-32)^{3/5}⟩', '⟨(\\sqrt[5]{-32})^3⟩', '⟨-8⟩']],
      after: 'Take the root first: the numbers stay small.', check: { list: ['Math.round(Math.cbrt(27))', 'Math.round(Math.cbrt(8)**2)', '16**-0.75', '(-2)**3'], is: [3, 4, 0.125, -8] } },
    { title: 'Converting & Exponent Rules', color: 'pink', kind: 'words', rows: [
      ['⟨\\sqrt[3]{x^2}⟩ as a power', '⟨x^{2/3}⟩'], ['⟨x^{5/4}⟩ as a radical', '⟨\\sqrt[4]{x^5} = x\\sqrt[4]{x}⟩'], ['⟨x^{1/2} \\cdot x^{1/3}⟩', '⟨x^{5/6}⟩'], ['⟨(x^{2/3})^{6}⟩', '⟨x^4⟩'], ['⟨\\dfrac{x^{3/4}}{x^{1/4}}⟩', '⟨x^{1/2} = \\sqrt{x}⟩']],
      check: [{ num: '1/2+1/3', is: 5 / 6 }, { num: '2/3*6', is: 4 }, { num: '3/4-1/4', is: 0.5 }] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['⟨\\sqrt{x^2} = |x|⟩; even roots of negatives are not real.', 'Odd roots of negatives are real: ⟨\\sqrt[3]{-8} = -2⟩.', 'Simplify before adding radicals.'],
      bad: [['⟨\\sqrt{9 + 16} = 3 + 4⟩', 'it is ⟨\\sqrt{25} = 5⟩'], ['⟨2\\sqrt{3} + 3\\sqrt{2} = 5\\sqrt{5}⟩', 'unlike radicals do not combine'], ['⟨8^{-1/3} = -2⟩', 'it is ⟨\\tfrac{1}{2}⟩']],
      check: { list: ['Math.cbrt(-8)', '8**(-1/3)'], is: [-2, 0.5] } }
  ],
  back: [
    { title: 'Solving Radical Equations', color: 'purple', kind: 'example', text: 'Isolate the radical, raise both sides to the index, solve, then <b>check every answer</b> in the original.',
      example: '⟨\\sqrt{2x + 3} = x⟩', steps: [['Square:', '⟨2x + 3 = x^2 \\to (x - 3)(x + 1) = 0⟩'], ['Check ⟨-1⟩:', '⟨\\sqrt{1} = 1 \\ne -1⟩ ✘']], answer: '⟨x = 3⟩', check: { list: ['Math.sqrt(9)', 'Math.sqrt(1)'], is: [3, 1] } },
    { title: 'Extraneous Solutions', color: 'blue', kind: 'example', text: 'Squaring can create solutions that do not work. Two radicals: isolate one, square, isolate the other, square again.',
      example: '⟨\\sqrt{x + 7} - 1 = x⟩', steps: [['Square:', '⟨x + 7 = (x + 1)^2 \\to x^2 + x - 6 = 0⟩'], ['Check:', '⟨x = 2⟩ ✔, ⟨x = -3⟩: ⟨\\sqrt{4} - 1 = 1 \\ne -3⟩ ✘']], answer: '⟨x = 2⟩',
      check: [{ expr: '(x+1)**2-(x+7)', is: '(x-2)*(x+3)' }, { num: 'Math.sqrt(9)-1', is: 2 }, { num: 'Math.sqrt(4)-1', is: 1 }] },
    { title: 'Rational-Exponent Equations', color: 'green', kind: 'example', text: 'Isolate the power, then raise both sides to the reciprocal exponent. An even root gives ⟨\\pm⟩.',
      example: '⟨(x + 1)^{2/3} = 4⟩', steps: [['Raise to ⟨\\tfrac{3}{2}⟩:', '⟨x + 1 = \\pm 4^{3/2} = \\pm 8⟩'], ['Check:', '⟨\\sqrt[3]{8}^{\\,2} = 4⟩, ⟨\\sqrt[3]{-8}^{\\,2} = 4⟩ ✔']], answer: '⟨x = 7⟩ or ⟨x = -9⟩',
      check: { list: ['Math.cbrt(8)**2', 'Math.cbrt(-8)**2'], is: [4, 4] } },
    { title: 'Square- & Cube-Root Graphs', color: 'orange', kind: 'table', head: ['Parent', 'Domain', 'Range', 'Key points'], rows: [
      ['⟨y = \\sqrt{x}⟩', '⟨x \\ge 0⟩', '⟨y \\ge 0⟩', '⟨(0,0), (1,1), (4,2)⟩'], ['⟨y = \\sqrt[3]{x}⟩', 'all reals', 'all reals', '⟨(-8,-2), (0,0), (8,2)⟩']],
      fig: F.plane({ id: 'rr', xmin: -8, xmax: 9, ymin: -3, ymax: 4, size: 2.6, ticks: 2, fns: [{ f: x => x >= 0 ? Math.sqrt(x) : NaN, from: 0, color: '#2563eb' }, { f: x => Math.cbrt(x), color: '#db2777' }], labels: [{ x: 6.5, y: 3.4, t: '√x', color: '#2563eb' }, { x: -5, y: -2.4, t: '∛x', color: '#db2777' }] }),
      check: { list: ['Math.sqrt(4)', 'Math.cbrt(-8)'], is: [2, -2] } },
    { title: 'Transformations', color: 'pink', kind: 'example', text: '⟨y = a\\sqrt{x - h} + k⟩ starts at ⟨(h, k)⟩. ⟨a < 0⟩ reflects over the x-axis; ⟨|a| > 1⟩ stretches.',
      example: '⟨y = -2\\sqrt{x + 3} + 1⟩', steps: [['Start:', '⟨(-3, 1)⟩; next point ⟨(-2, -1)⟩'], ['Domain / range:', '⟨x \\ge -3⟩, ⟨y \\le 1⟩']], answer: 'left 3, up 1, reflected, stretched ×2',
      fig: F.plane({ id: 'rt', xmin: -4, xmax: 5, ymin: -5, ymax: 2, size: 1.5, ticks: 1, fns: [{ f: x => x >= -3 ? -2 * Math.sqrt(x + 3) + 1 : NaN, from: -3 }], points: [{ x: -3, y: 1 }, { x: -2, y: -1 }, { x: 1, y: -3 }] }),
      check: { list: ['-2*Math.sqrt(1)+1', '-2*Math.sqrt(4)+1'], is: [-1, -3] } },
    { title: 'Application: Pendulum', color: 'teal', kind: 'example', text: 'Period (seconds) of a pendulum ⟨L⟩ feet long: ⟨T = 2\\pi\\sqrt{\\tfrac{L}{32}}⟩.',
      example: 'Find ⟨T⟩ for ⟨L = 8⟩. What ⟨L⟩ gives ⟨T = 2\\pi⟩?', steps: [['⟨L = 8⟩:', '⟨T = 2\\pi\\sqrt{\\tfrac{1}{4}} = \\pi⟩'], ['⟨T = 2\\pi⟩:', '⟨\\sqrt{\\tfrac{L}{32}} = 1 \\to L = 32⟩']], answer: '⟨T \\approx 3.14⟩ s; ⟨L = 32⟩ ft',
      check: { list: ['Math.round(2*Math.PI*Math.sqrt(8/32)*100)/100', '2*Math.PI*Math.sqrt(32/32)/(2*Math.PI)'], is: [3.14, 1] } }
  ]
};
