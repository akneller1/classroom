const F = require('../figs.cjs');
module.exports = {
  name: 'quadratic-functions-complex-numbers', course: 'Algebra 2', unitNo: 3, unitName: 'Quadratics & Complex Numbers',
  focus: 'parabola forms, completing the square, the quadratic formula and the discriminant',
  morefocus: 'complex numbers, quadratic inequalities, linear-quadratic systems and modeling',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['vertex', 'Turning point ⟨(h, k)⟩: min if ⟨a > 0⟩, max if ⟨a < 0⟩.', '⟨(3, -8)⟩'], ['axis of symmetry', 'Vertical line ⟨x = h⟩ through the vertex.', '⟨x = 3⟩'],
      ['discriminant', '⟨b^2 - 4ac⟩: number and type of solutions.', '⟨40⟩'], ['imaginary unit', '⟨i = \\sqrt{-1}⟩, so ⟨i^2 = -1⟩.', '⟨\\sqrt{-49} = 7i⟩'], ['complex conjugate', '⟨a - bi⟩ for ⟨a + bi⟩; product ⟨a^2 + b^2⟩.', '⟨(3+2i)(3-2i) = 13⟩']] },
    { title: 'Three Forms', color: 'blue', kind: 'table', head: ['Form', 'Equation', 'Shows'], rows: [
      ['Vertex', '⟨a(x - h)^2 + k⟩', 'vertex ⟨(h, k)⟩'], ['Standard', '⟨ax^2 + bx + c⟩', 'axis ⟨-\\tfrac{b}{2a}⟩, y-int ⟨c⟩'], ['Factored', '⟨a(x - p)(x - q)⟩', 'zeros ⟨p, q⟩']],
      after: '⟨2x^2 - 12x + 10 = 2(x - 3)^2 - 8 = 2(x - 1)(x - 5)⟩', check: [{ expr: '2*(x-3)**2-8', is: '2*x**2-12*x+10' }, { expr: '2*(x-1)*(x-5)', is: '2*x**2-12*x+10' }] },
    { title: 'Completing the Square', color: 'green', kind: 'example', text: 'Add ⟨\\left(\\tfrac{b}{2}\\right)^2⟩ to both sides (divide by ⟨a⟩ first in an equation).',
      example: 'Solve ⟨x^2 - 6x + 3 = 0⟩.', steps: [['Move 3, add 9:', '⟨(x - 3)^2 = 6⟩'], ['Roots:', '⟨x - 3 = \\pm\\sqrt{6}⟩']], answer: '⟨x = 3 \\pm \\sqrt{6}⟩', check: { list: ['(3+Math.sqrt(6))**2-6*(3+Math.sqrt(6))+3', '(3-Math.sqrt(6))**2-6*(3-Math.sqrt(6))+3'], is: [0, 0] } },
    { title: 'Quadratic Formula', color: 'orange', kind: 'example', text: '⟨x = \\dfrac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}⟩. Divide every term by ⟨2a⟩.',
      example: '⟨3x^2 - 4x - 2 = 0⟩', steps: [['Discriminant:', '⟨16 + 24 = 40⟩'], ['Formula:', '⟨\\dfrac{4 \\pm 2\\sqrt{10}}{6}⟩']], answer: '⟨x = \\dfrac{2 \\pm \\sqrt{10}}{3}⟩', check: { num: 'Math.round((3*((2+Math.sqrt(10))/3)**2-4*((2+Math.sqrt(10))/3)-2)*1e9)', is: 0 } },
    { title: 'The Discriminant', color: 'pink', kind: 'table', head: ['⟨b^2 - 4ac⟩', 'Solutions', 'Example'], rows: [
      ['positive square', '2 rational', '⟨x^2 - 2x - 3⟩: 16'], ['positive, not square', '2 irrational', '⟨x^2 - 2x - 1⟩: 8'], ['zero', '1 real (double)', '⟨x^2 - 4x + 4⟩: 0'], ['negative', '2 complex conjugates', '⟨x^2 - 4x + 6⟩: ⟨-8⟩']],
      check: { list: ['4+12', '4+4', '16-16', '16-24'], is: [16, 8, 0, -8] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['In ⟨(x + 4)^2⟩ the vertex has ⟨x = -4⟩.', 'Square roots give ⟨\\pm⟩.', 'Factor out ⟨a⟩ before completing the square in vertex form.'],
      bad: [['⟨b^2⟩ for ⟨b = -5⟩ is not ⟨-25⟩', 'it is ⟨(-5)^2 = 25⟩'], ['⟨\\tfrac{4 + 2\\sqrt{10}}{6} \\ne 4 + \\tfrac{\\sqrt{10}}{3}⟩', 'divide both terms'], ['⟨i^2 = 1⟩', 'it is ⟨-1⟩']] }
  ],
  back: [
    { title: 'Powers of the Imaginary Unit', color: 'purple', kind: 'table', head: ['⟨i^1⟩', '⟨i^2⟩', '⟨i^3⟩', '⟨i^4⟩'], rows: [['⟨i⟩', '⟨-1⟩', '⟨-i⟩', '⟨1⟩']],
      after: 'The cycle repeats every 4: use the remainder after dividing the exponent by 4. ⟨i^{47}⟩: ⟨47 = 4(11) + 3⟩, so ⟨i^{47} = -i⟩. ⟨\\sqrt{-18} = 3i\\sqrt{2}⟩.', check: { num: '47 % 4', is: 3 } },
    { title: 'Complex Number Operations', color: 'blue', kind: 'words', rows: [
      ['Add: ⟨(3 + 2i) + (5 - 6i)⟩', '⟨8 - 4i⟩'], ['Subtract: ⟨(3 + 2i) - (5 - 6i)⟩', '⟨-2 + 8i⟩'], ['Multiply: ⟨(3 + 2i)(4 - i) = 12 + 5i - 2i^2⟩', '⟨14 + 5i⟩'],
      ['Divide: ⟨\\tfrac{8 + i}{2 - i} \\cdot \\tfrac{2 + i}{2 + i} = \\tfrac{15 + 10i}{5}⟩', '⟨3 + 2i⟩'], ['⟨|3 + 4i| = \\sqrt{9 + 16}⟩', '⟨5⟩']],
      check: [{ list: ['3*4+2*1', '3*(-1)+2*4'], is: [14, 5] }, { list: ['(3*2-2*(-1))', '(3*(-1)+2*2)'], is: [8, 1] }] },
    { title: 'Complex Roots', color: 'green', kind: 'example', text: 'A negative discriminant gives conjugate roots. Write a quadratic from roots: ⟨a(x - p)(x - q)⟩.',
      example: 'Solve ⟨x^2 - 4x + 13 = 0⟩.', steps: [['Discriminant:', '⟨16 - 52 = -36⟩'], ['Formula:', '⟨\\dfrac{4 \\pm 6i}{2}⟩']], answer: '⟨x = 2 \\pm 3i⟩', check: { list: ['2+2', '2*2+3*3'], is: [4, 13] } },
    { title: 'Quadratic Inequalities', color: 'orange', kind: 'example', text: 'Solve the equation, sketch, and test a point in each region.',
      example: '⟨x^2 - 2x - 8 > 0⟩', steps: [['Zeros:', '⟨(x - 4)(x + 2) = 0 \\to -2,\\ 4⟩'], ['Opens up:', 'positive outside the zeros']], answer: '⟨(-\\infty, -2) \\cup (4, \\infty)⟩',
      fig: F.plane({ id: 'qi', xmin: -4, xmax: 6, ymin: -10, ymax: 8, size: 0.95, fns: [{ f: x => x * x - 2 * x - 8 }], points: [{ x: -2, y: 0, open: true }, { x: 4, y: 0, open: true }] }), check: { list: ['9+6-8', '0-0-8', '25-10-8'], is: [7, -8, 7] } },
    { title: 'Linear-Quadratic Systems', color: 'pink', kind: 'example', text: 'Substitute, get a quadratic = 0, solve, then find each ⟨y⟩. 2, 1 or 0 intersection points.',
      example: '⟨y = x^2 - 4x + 3⟩ and ⟨y = x - 1⟩', steps: [['Set equal:', '⟨x^2 - 5x + 4 = 0⟩'], ['Factor:', '⟨x = 1,\\ 4⟩']], answer: '⟨(1, 0)⟩ and ⟨(4, 3)⟩', check: { list: ['1-4+3', '16-16+3'], is: [0, 3] } },
    { title: 'Quadratic Modeling', color: 'teal', kind: 'example', text: 'Vertex = maximum (the ⟨h⟩-value is the max, ⟨t⟩ is when). Reject negative times.',
      example: '⟨h(t) = -16t^2 + 64t + 80⟩', steps: [['Max at ⟨t = 2⟩:', '⟨h(2) = 144⟩ ft'], ['Lands:', '⟨-16(t - 5)(t + 1) = 0 \\to t = 5⟩']], answer: '144 ft at 2 s; lands at 5 s', check: { list: ['-16*4+128+80', '-16*25+320+80'], is: [144, 0] } }
  ]
};
