const F = require('../figs.cjs');
module.exports = {
  name: 'polynomial-functions', course: 'Algebra 2', unitNo: 4, unitName: 'Polynomial Functions',
  focus: 'operations, factoring patterns, polynomial division and the remainder and factor theorems',
  morefocus: 'zeros and multiplicity, end behavior, graphing, the Fundamental Theorem and applications',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['degree', 'Highest exponent of the variable.', '⟨4x^3 - x⟩: 3'], ['leading coefficient', 'Coefficient of the highest-degree term.', '⟨-2x^4 + x⟩: ⟨-2⟩'],
      ['zero (root)', 'An input with ⟨P(a) = 0⟩; an x-intercept if real.', '⟨x = 3⟩'], ['multiplicity', 'How many times a factor repeats.', '⟨(x - 1)^2⟩: 2'],
      ['end behavior', 'What ⟨P(x)⟩ does as ⟨x \\to \\pm\\infty⟩.', 'up / down']] },
    { title: 'Operations', color: 'blue', kind: 'words', rows: [
      ['Add: ⟨(3x^3 - 2x + 5) + (x^3 + 4x^2 - 7)⟩', '⟨4x^3 + 4x^2 - 2x - 2⟩'], ['Subtract: ⟨(2x^2 - x) - (5x^2 - 3x + 1)⟩', '⟨-3x^2 + 2x - 1⟩'],
      ['Multiply: ⟨(x + 3)(x^2 - 2x + 5)⟩', '⟨x^3 + x^2 - x + 15⟩'], ['Cube: ⟨(x - 2)^3⟩', '⟨x^3 - 6x^2 + 12x - 8⟩']],
      check: [{ expr: '(3*x**3-2*x+5)+(x**3+4*x**2-7)', is: '4*x**3+4*x**2-2*x-2' }, { expr: '(2*x**2-x)-(5*x**2-3*x+1)', is: '-3*x**2+2*x-1' }, { expr: '(x+3)*(x**2-2*x+5)', is: 'x**3+x**2-x+15' }, { expr: '(x-2)**3', is: 'x**3-6*x**2+12*x-8' }] },
    { title: 'Factoring Patterns', color: 'green', kind: 'table', plain: true, rows: [
      ['Sum of cubes', '⟨a^3 + b^3 = (a + b)(a^2 - ab + b^2)⟩'], ['Difference of cubes', '⟨x^3 - 8 = (x - 2)(x^2 + 2x + 4)⟩'],
      ['Quadratic form', '⟨x^4 - 5x^2 + 4 = (x - 1)(x + 1)(x - 2)(x + 2)⟩'], ['Grouping', '⟨x^3 + 2x^2 - 9x - 18 = (x + 2)(x - 3)(x + 3)⟩']],
      check: [{ expr: '(x+y)*(x*x-x*y+y*y)', is: 'x**3+y**3' }, { expr: '(x-2)*(x*x+2*x+4)', is: 'x**3-8' }, { expr: '(x-1)*(x+1)*(x-2)*(x+2)', is: 'x**4-5*x**2+4' }, { expr: '(x+2)*(x-3)*(x+3)', is: 'x**3+2*x**2-9*x-18' }] },
    { title: 'Synthetic Division', color: 'orange', kind: 'example', text: 'Divide by ⟨x - a⟩: bring down, multiply by ⟨a⟩, add. Write 0 for missing terms.',
      example: '⟨(x^3 - 4x^2 + x + 6) \\div (x - 2)⟩', steps: [['Row:', '⟨2 \\mid 1 \\;\\; -4 \\;\\; 1 \\;\\; 6 \\to 1 \\;\\; -2 \\;\\; -3 \\;\\; 0⟩'], ['Quotient:', '⟨x^2 - 2x - 3⟩, remainder ⟨0⟩']],
      answer: '⟨(x - 2)(x - 3)(x + 1)⟩', check: { expr: '(x-2)*(x-3)*(x+1)', is: 'x**3-4*x**2+x+6' } },
    { title: 'Remainder & Factor Theorems', color: 'pink', kind: 'example', text: 'Remainder of ⟨P(x) \\div (x - a)⟩ is ⟨P(a)⟩. ⟨x - a⟩ is a factor exactly when ⟨P(a) = 0⟩.',
      example: '⟨P(x) = 2x^3 - 3x^2 + 4x - 5⟩ divided by ⟨x - 2⟩', steps: [['Evaluate:', '⟨P(2) = 16 - 12 + 8 - 5⟩'], ['Factor?', 'no, since ⟨P(2) \\ne 0⟩']], answer: 'remainder ⟨7⟩',
      check: { num: '2*8-3*4+4*2-5', is: 7 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Write terms in descending order before dividing.', 'Use ⟨a⟩, not ⟨-a⟩, in synthetic division by ⟨x - a⟩.', 'Factor out a GCF first.'],
      bad: [['⟨(x + 2)^3 = x^3 + 8⟩', 'expand: ⟨x^3 + 6x^2 + 12x + 8⟩'], ['Subtracting only the first term', 'distribute the minus sign to every term'], ['⟨x^3 + 8 = (x + 2)^3⟩', 'it is ⟨(x + 2)(x^2 - 2x + 4)⟩']] }
  ],
  back: [
    { title: 'Zeros & Multiplicity', color: 'purple', kind: 'html', html: 'Odd multiplicity: the graph <b>crosses</b>. Even multiplicity: it <b>touches</b> and turns. ⟨f(x) = (x + 2)(x - 1)^2⟩: crosses at ⟨-2⟩, touches at ⟨1⟩.',
      fig: F.plane({ id: 'pm', xmin: -3, xmax: 3, ymin: -3, ymax: 6, size: 1.4, ticks: 1, fns: [{ f: x => (x + 2) * (x - 1) * (x - 1) }], points: [{ x: -2, y: 0 }, { x: 1, y: 0 }] }),
      check: { list: ['(-2+2)*9', '3*0'], is: [0, 0] } },
    { title: 'End Behavior', color: 'blue', kind: 'table', head: ['Degree', '⟨a_n > 0⟩', '⟨a_n < 0⟩'], rows: [
      ['even', 'up, up', 'down, down'], ['odd', 'down left, up right', 'up left, down right']],
      after: 'A degree-⟨n⟩ polynomial has at most ⟨n⟩ real zeros and at most ⟨n - 1⟩ turning points. ⟨-x^4 + 3x⟩: down, down.' },
    { title: 'Graphing a Polynomial', color: 'green', kind: 'example', text: 'Factor, plot zeros, use end behavior and the y-intercept.',
      example: '⟨f(x) = x^3 - 4x⟩', steps: [['Factor:', '⟨x(x - 2)(x + 2)⟩'], ['Zeros:', '⟨-2, 0, 2⟩; odd degree, ⟨a > 0⟩: down left, up right']], answer: 'crosses at ⟨-2, 0, 2⟩',
      fig: F.plane({ id: 'pg', xmin: -3, xmax: 3, ymin: -4, ymax: 4, size: 1.05, fns: [{ f: x => x * x * x - 4 * x }], points: [{ x: -2, y: 0 }, { x: 0, y: 0 }, { x: 2, y: 0 }] }),
      check: { expr: 'x*(x-2)*(x+2)', is: 'x**3-4*x' } },
    { title: 'Fundamental Theorem of Algebra', color: 'orange', kind: 'example', text: 'Degree ⟨n⟩ means exactly ⟨n⟩ complex zeros (counting multiplicity). With real coefficients, complex zeros come in conjugate pairs ⟨a \\pm bi⟩.',
      example: 'Write a cubic with zeros ⟨2⟩ and ⟨3i⟩.', steps: [['Conjugate:', '⟨-3i⟩ is also a zero'], ['Multiply:', '⟨(x - 2)(x^2 + 9)⟩']], answer: '⟨x^3 - 2x^2 + 9x - 18⟩',
      check: { expr: '(x-2)*(x*x+9)', is: 'x**3-2*x**2+9*x-18' } },
    { title: 'Rational Root Theorem', color: 'pink', kind: 'example', text: 'Possible rational zeros: ⟨\\pm\\tfrac{\\text{factors of constant}}{\\text{factors of leading coeff.}}⟩. Test, then divide.',
      example: '⟨2x^3 - 3x^2 - 11x + 6 = 0⟩', steps: [['Test ⟨x = 3⟩:', '⟨54 - 27 - 33 + 6 = 0⟩'], ['Divide:', '⟨2x^2 + 3x - 2 = (2x - 1)(x + 2)⟩']], answer: '⟨x = 3,\\ \\tfrac{1}{2},\\ -2⟩',
      check: [{ expr: '(x-3)*(2*x-1)*(x+2)', is: '2*x**3-3*x**2-11*x+6' }] },
    { title: 'Application: Open Box', color: 'teal', kind: 'example', text: 'Cut ⟨x⟩-in. squares from the corners of a 12 × 10 in. sheet: ⟨V = x(12 - 2x)(10 - 2x)⟩, ⟨0 < x < 5⟩.',
      example: 'When is ⟨V = 96⟩ in.³?', steps: [['Simplify:', '⟨x^3 - 11x^2 + 30x - 24 = 0⟩'], ['Factor:', '⟨(x - 2)(x^2 - 9x + 12) = 0⟩']], answer: '⟨x = 2⟩ or ⟨x = \\tfrac{9 - \\sqrt{33}}{2} \\approx 1.63⟩',
      check: [{ expr: 'x*(12-2*x)*(10-2*x)-96', is: '4*(x**3-11*x**2+30*x-24)' }, { expr: '(x-2)*(x*x-9*x+12)', is: 'x**3-11*x**2+30*x-24' }, { num: 'Math.round((9-Math.sqrt(33))/2*100)/100', is: 1.63 }, { true: '(9+Math.sqrt(33))/2 > 5' }] }
  ]
};
