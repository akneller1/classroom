const F = require('../figs.cjs');
const disc = '<div style="display:flex;gap:4px;justify-content:space-around;font-size:7.5pt;text-align:center">' + [
  ['⟨b^2 - 4ac > 0⟩: 2 solutions', x => x * x - 2], ['⟨= 0⟩: 1 solution', x => x * x], ['⟨< 0⟩: no real solutions', x => x * x + 1.5]].map((t, i) =>
  '<div>' + F.plane({ id: 'qd' + i, xmin: -3, xmax: 3, ymin: -3, ymax: 4, size: 0.72, fns: [{ f: t[1], color: '#db2777' }] }) + '<br>' + ['2 x-intercepts', '1 x-intercept', 'no x-intercepts'][i] + '</div>').join('') + '</div>';
module.exports = {
  name: 'quadratics', course: 'Algebra 1', unitNo: 11, unitName: 'Quadratic Functions',
  focus: 'graphing quadratic functions and their key features',
  morefocus: 'solving quadratic equations: factoring, square roots, completing the square and the formula',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['parabola', 'The U-shaped graph of a quadratic.', '⟨y = x^2⟩'], ['vertex', 'The turning point (maximum or minimum).', '⟨(2, -9)⟩'],
      ['axis of symmetry', 'Vertical line through the vertex.', '⟨x = 2⟩'], ['zeros', 'Where ⟨y = 0⟩: the x-intercepts.', '⟨x = -1,\\ 5⟩'], ['discriminant', '⟨b^2 - 4ac⟩: how many real solutions.', '⟨64 > 0⟩']] },
    { title: 'Three Forms', color: 'blue', kind: 'table', head: ['Form', 'Equation', 'Shows'], rows: [
      ['Standard', '⟨y = ax^2 + bx + c⟩', 'y-intercept ⟨(0, c)⟩'], ['Vertex', '⟨y = a(x - h)^2 + k⟩', 'vertex ⟨(h, k)⟩'], ['Factored', '⟨y = a(x - p)(x - q)⟩', 'zeros ⟨p⟩ and ⟨q⟩']],
      after: '⟨a > 0⟩ opens up (minimum); ⟨a < 0⟩ opens down (maximum).' },
    { title: 'Key Features of a Parabola', color: 'green', kind: 'example', text: 'Axis: ⟨x = -\\dfrac{b}{2a}⟩. Substitute it to find the vertex.',
      example: '⟨y = x^2 - 4x - 5⟩', steps: [['Axis:', '⟨x = \\tfrac{4}{2} = 2⟩'], ['Vertex:', '⟨(2, -9)⟩'], ['Zeros:', '⟨(x - 5)(x + 1) = 0 \\to -1,\\ 5⟩']], answer: 'vertex ⟨(2, -9)⟩, y-intercept ⟨(0, -5)⟩',
      fig: F.plane({ id: 'qk', xmin: -3, xmax: 7, ymin: -10, ymax: 4, size: 1.25, ticks: 2, grid: false, fns: [{ f: x => x * x - 4 * x - 5 }], vlines: [{ x: 2 }], points: [{ x: 2, y: -9, label: '(2,−9)', dy: 12 }, { x: -1, y: 0 }, { x: 5, y: 0 }, { x: 0, y: -5 }] }),
      check: { list: ['2**2-4*2-5', '(-1)**2-4*(-1)-5', '5**2-4*5-5'], is: [-9, 0, 0] } },
    { title: 'Vertex Form & Transformations', color: 'orange', kind: 'words', rows: [
      ['⟨h⟩ in ⟨y = a(x - h)^2 + k⟩', 'shift right ⟨h⟩'], ['⟨k⟩', 'shift up ⟨k⟩'], ['⟨|a| > 1⟩ or ⟨|a| < 1⟩', 'narrower or wider'], ['⟨a < 0⟩', 'opens down'],
      ['⟨y = -2(x + 4)^2 + 5⟩', 'vertex ⟨(-4, 5)⟩']] },
    { title: 'The Discriminant', color: 'pink', kind: 'html', html: 'In ⟨ax^2 + bx + c = 0⟩, the discriminant ⟨b^2 - 4ac⟩ tells how many real solutions.', fig: disc },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Write ⟨= 0⟩ before solving.', 'Square roots give two answers: ⟨\\pm⟩.', 'The y-intercept is ⟨c⟩; the zeros are where ⟨y = 0⟩.'],
      bad: [['⟨x = \\tfrac{b}{2a}⟩', 'the axis is ⟨-\\tfrac{b}{2a}⟩'], ['In ⟨(x - 3)^2⟩, ⟨h = -3⟩', 'it is ⟨h = 3⟩'], ['Dividing only part of the formula by ⟨2a⟩', 'divide all of ⟨-b \\pm \\sqrt{\\ }⟩']] }
  ],
  back: [
    { title: 'Solve by Factoring', color: 'purple', kind: 'example', text: 'Set equal to 0, factor, use the Zero Product Property.',
      example: '⟨x^2 - 5x - 6 = 0⟩', steps: [['Factor:', '⟨(x - 6)(x + 1) = 0⟩']], answer: '⟨x = 6⟩ or ⟨x = -1⟩', check: { list: ['6**2-5*6-6', '(-1)**2-5*(-1)-6'], is: [0, 0] } },
    { title: 'Solve by Square Roots', color: 'blue', kind: 'example', text: 'Isolate the square, then take ⟨\\pm\\sqrt{\\ }⟩. Simplify radicals.',
      example: '⟨(x - 3)^2 = 20⟩', steps: [['Square root:', '⟨x - 3 = \\pm\\sqrt{20} = \\pm 2\\sqrt{5}⟩']], answer: '⟨x = 3 \\pm 2\\sqrt{5}⟩', check: { list: ['(2*Math.sqrt(5))**2', '(-2*Math.sqrt(5))**2'], is: [20, 20] } },
    { title: 'Completing the Square', color: 'green', kind: 'example', text: 'Move ⟨c⟩, add ⟨\\left(\\tfrac{b}{2}\\right)^2⟩ to both sides, write a square, solve.',
      example: '⟨x^2 + 6x - 7 = 0⟩', steps: [['Move 7:', '⟨x^2 + 6x = 7⟩'], ['Add 9:', '⟨(x + 3)^2 = 16⟩'], ['Roots:', '⟨x + 3 = \\pm 4⟩']], answer: '⟨x = 1⟩ or ⟨x = -7⟩', check: { list: ['1+6-7', '49-42-7'], is: [0, 0] } },
    { title: 'Quadratic Formula', color: 'orange', kind: 'example', text: 'For ⟨ax^2 + bx + c = 0⟩: ⟨x = \\dfrac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}⟩',
      example: '⟨2x^2 + 4x - 6 = 0⟩', steps: [['⟨a, b, c⟩:', '⟨2,\\ 4,\\ -6⟩'], ['Substitute:', '⟨\\dfrac{-4 \\pm \\sqrt{16 + 48}}{4} = \\dfrac{-4 \\pm 8}{4}⟩']], answer: '⟨x = 1⟩ or ⟨x = -3⟩', check: { list: ['2+4-6', '18-12-6'], is: [0, 0] } },
    { title: 'Choosing a Method', color: 'pink', kind: 'words', rows: [
      ['No ⟨x⟩-term: ⟨x^2 = k⟩ or ⟨(x - h)^2 = k⟩', 'square roots'], ['Factors easily', 'factoring'], ['⟨a = 1⟩ and ⟨b⟩ is even', 'completing the square'], ['Anything else (always works)', 'quadratic formula']] },
    { title: 'Projectile Motion', color: 'teal', kind: 'example', text: '⟨h(t) = -16t^2 + v_0t + h_0⟩ (feet). Vertex = maximum height; positive zero = landing time.',
      example: '⟨h(t) = -16t^2 + 32t + 48⟩', steps: [['Max at ⟨t = 1⟩:', '⟨h(1) = 64⟩ ft'], ['Lands:', '⟨-16(t - 3)(t + 1) = 0 \\to t = 3⟩']], answer: '64 ft high, lands at 3 s', check: { list: ['-16+32+48', '-16*9+32*3+48'], is: [64, 0] } }
  ]
};
