const F = require('../figs.cjs');
const gal = [['y = x', x => x], ['y = x²', x => x * x], ['y = x³', x => x * x * x], ['y = |x|', x => Math.abs(x)], ['y = √x', x => x >= 0 ? Math.sqrt(x) : NaN, 0], ['y = 1/x', x => Math.abs(x) < 0.05 ? NaN : 1 / x]];
const gallery = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;font-size:7.5pt;text-align:center">' + gal.map((g, i) =>
  '<div>' + F.plane({ id: 'pg' + i, xmin: -3, xmax: 3, ymin: -3, ymax: 3, size: 0.66, fns: i === 5 ? [{ f: g[1], from: -3, to: -0.34 }, { f: g[1], from: 0.34, to: 3 }] : [{ f: g[1], from: g[2] !== undefined ? 0 : undefined }] }) + '<br>' + g[0] + '</div>').join('') + '</div>';
module.exports = {
  name: 'functions-transformations', course: 'Algebra 2', unitNo: 1, unitName: 'Functions & Transformations',
  focus: 'function notation, domain and range, parent functions and transformations',
  morefocus: 'operations, composition, piecewise functions and inverses',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['function', 'Each input has exactly one output.', '⟨\\{(1,3),(2,5)\\}⟩'], ['domain / range', 'All inputs / all outputs.', '⟨[2, \\infty)⟩'],
      ['parent function', 'Simplest function of a family.', '⟨y = x^2⟩'], ['composite', '⟨(f \\circ g)(x) = f(g(x))⟩', 'g first'], ['inverse', '⟨f^{-1}⟩ undoes ⟨f⟩; reflect over ⟨y = x⟩.', '⟨(a,b) \\to (b,a)⟩']] },
    { title: 'Notation, Domain & Range', color: 'blue', kind: 'example', text: 'Interval notation: [ ] includes, ( ) excludes, ∞ always gets ( ). Radicand ⟨\\ge 0⟩; denominator ⟨\\ne 0⟩.',
      example: '⟨f(x) = 2x^2 - 3x + 1⟩. Find ⟨f(-2)⟩.', steps: [['Substitute:', '⟨2(-2)^2 - 3(-2) + 1 = 8 + 6 + 1⟩'], ['Domain of ⟨\\sqrt{x - 2} + 1⟩:', '⟨[2, \\infty)⟩, range ⟨[1, \\infty)⟩']], answer: '⟨f(-2) = 15⟩', check: { num: '2*4+6+1', is: 15 } },
    { title: 'Parent Functions', color: 'green', kind: 'html', html: 'Domains: all reals except ⟨\\sqrt{x}⟩ ⟨[0, \\infty)⟩ and ⟨\\tfrac{1}{x}⟩ ⟨x \\ne 0⟩.', fig: gallery, figFirst: true },
    { title: 'Transformation Rules', color: 'orange', kind: 'words', rows: [
      ['⟨f(x) + k⟩', 'up ⟨k⟩'], ['⟨f(x - h)⟩', 'right ⟨h⟩ (⟨f(x + 3)⟩: left 3)'], ['⟨-f(x)⟩ / ⟨f(-x)⟩', 'reflect in x-axis / y-axis'], ['⟨a \\cdot f(x)⟩, ⟨|a| > 1⟩', 'vertical stretch'], ['⟨f(bx)⟩, ⟨|b| > 1⟩', 'horizontal compression by ⟨\\tfrac{1}{b}⟩']] },
    { title: 'Transformation Example', color: 'pink', kind: 'example', text: 'Move key points: ⟨(x, y) \\to (x - 3,\\ -2y + 1)⟩.',
      example: '⟨g(x) = -2\\sqrt{x + 3} + 1⟩ from ⟨\\sqrt{x}⟩', steps: [['Left 3,', 'reflect, stretch by 2, up 1'], ['Points:', '⟨(0,0) \\to (-3,1)⟩, ⟨(1,1) \\to (-2,-1)⟩, ⟨(4,2) \\to (1,-3)⟩']], answer: 'D ⟨[-3, \\infty)⟩, R ⟨(-\\infty, 1]⟩',
      check: { list: ['-2*Math.sqrt(-3+3)+1', '-2*Math.sqrt(-2+3)+1', '-2*Math.sqrt(1+3)+1'], is: [1, -1, -3] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Horizontal changes do the opposite: ⟨f(x + 3)⟩ moves left.', 'Stretch/reflect before shifting up or down.', 'Track key points ⟨(x, y) \\to (\\text{new } x, \\text{new } y)⟩.'],
      bad: [['⟨f(x) + 3⟩ vs ⟨f(x + 3)⟩', 'up 3 vs left 3'], ['⟨-f(x)⟩ vs ⟨f(-x)⟩', 'x-axis vs y-axis'], ['⟨f(x)⟩ as ⟨f \\cdot x⟩', 'it is the output at ⟨x⟩']] }
  ],
  back: [
    { title: 'Operations on Functions', color: 'purple', kind: 'table', head: ['Operation', 'For ⟨f(x) = 2x + 1⟩ and ⟨g(x) = x^2 - 3⟩'], rows: [
      ['⟨(f + g)(x)⟩', '⟨x^2 + 2x - 2⟩'], ['⟨(f - g)(x)⟩', '⟨-x^2 + 2x + 4⟩'], ['⟨(f \\cdot g)(x)⟩', '⟨2x^3 + x^2 - 6x - 3⟩'], ['⟨\\left(\\tfrac{f}{g}\\right)(x)⟩', '⟨\\tfrac{2x + 1}{x^2 - 3},\\ x \\ne \\pm\\sqrt{3}⟩']],
      check: [{ expr: '(2*x+1)+(x**2-3)', is: 'x**2+2*x-2' }, { expr: '(2*x+1)-(x**2-3)', is: '-(x**2)+2*x+4' }, { expr: '(2*x+1)*(x**2-3)', is: '2*x**3+x**2-6*x-3' }] },
    { title: 'Composition', color: 'blue', kind: 'example', text: 'Inside out: do ⟨g⟩ first, then put its output into ⟨f⟩. Order matters.',
      example: '⟨f(g(x))⟩ and ⟨g(f(x))⟩', steps: [['⟨f(g(x))⟩:', '⟨2(x^2 - 3) + 1 = 2x^2 - 5⟩'], ['⟨g(f(x))⟩:', '⟨(2x + 1)^2 - 3 = 4x^2 + 4x - 2⟩'], ['⟨(f \\circ g)(2)⟩:', '⟨f(1) = 3⟩']], answer: '⟨f \\circ g \\ne g \\circ f⟩',
      check: [{ expr: '2*(x**2-3)+1', is: '2*x**2-5' }, { expr: '(2*x+1)**2-3', is: '4*x**2+4*x-2' }, { num: '2*(2**2-3)+1', is: 3 }] },
    { title: 'Piecewise Functions', color: 'green', kind: 'example', text: 'Use the rule whose condition the input meets. Graph each piece only on its interval (open circle for ⟨<⟩, closed for ⟨\\le⟩).',
      example: '⟨h(x) = x + 3⟩ if ⟨x < 1⟩; ⟨(x - 2)^2⟩ if ⟨x \\ge 1⟩', steps: [['⟨h(0)⟩:', '⟨0 + 3 = 3⟩'], ['⟨h(4)⟩:', '⟨(4 - 2)^2 = 4⟩']], answer: '⟨h(0) = 3,\\ h(4) = 4⟩',
      fig: F.plane({ id: 'pw', xmin: -3, xmax: 5, ymin: -1, ymax: 6, size: 1.0, fns: [{ f: x => x + 3, to: 1 }, { f: x => (x - 2) * (x - 2), from: 1, color: '#16a34a' }], points: [{ x: 1, y: 4, open: true, color: '#2563eb' }, { x: 1, y: 1, color: '#16a34a' }] }) },
    { title: 'Finding an Inverse', color: 'orange', kind: 'example', text: 'Write ⟨y⟩, swap ⟨x⟩ and ⟨y⟩, solve for ⟨y⟩. Verify: ⟨f(f^{-1}(x)) = x⟩.',
      example: '⟨f(x) = 3x - 5⟩', steps: [['Swap:', '⟨x = 3y - 5⟩'], ['Solve:', '⟨y = \\dfrac{x + 5}{3}⟩']], answer: '⟨f^{-1}(x) = \\dfrac{x + 5}{3}⟩', check: { expr: '3*((x+5)/3)-5', is: 'x' } },
    { title: 'Inverses & One-to-One', color: 'pink', kind: 'list', items: [
      '⟨(a, b)⟩ on ⟨f⟩ means ⟨(b, a)⟩ on ⟨f^{-1}⟩; graphs mirror over ⟨y = x⟩.', 'Domain and range swap.', '<b>Horizontal line test</b>: if a horizontal line hits twice, there is no inverse function.', '⟨y = x^2⟩ needs ⟨x \\ge 0⟩ to have the inverse ⟨\\sqrt{x}⟩. ⟨f^{-1}(x) \\ne \\tfrac{1}{f(x)}⟩.'] },
    { title: 'Writing the Equation of a Graph', color: 'teal', kind: 'example', text: 'Name the parent, read the vertex for ⟨h, k⟩, use one more point for ⟨a⟩.',
      example: 'Parabola, vertex ⟨(1, 4)⟩, through ⟨(0, 2)⟩.', steps: [['Form:', '⟨y = a(x - 1)^2 + 4⟩'], ['Use ⟨(0, 2)⟩:', '⟨2 = a + 4,\\ a = -2⟩']], answer: '⟨y = -2(x - 1)^2 + 4⟩', check: { num: '-2*(0-1)**2+4', is: 2 } }
  ]
};
