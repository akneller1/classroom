const F = require('../figs.cjs');
const tri = [[1, 1], [4, 1], [1, 3]];
const map = f => tri.map(p => f(p[0], p[1]));
const pl = (id, img, o) => F.plane(Object.assign({ id, xmin: -5, xmax: 5, ymin: -5, ymax: 5, size: 1.05, polys: [{ pts: tri, fill: '#2563eb', color: '#2563eb' }, { pts: img, fill: '#db2777', color: '#db2777' }] }, o || {}));
module.exports = {
  name: 'geometry-coordinate-transformations', course: 'Geometry', unitNo: 8, unitName: 'Coordinate Geometry & Transformations',
  focus: 'distance, midpoint, slope and translations',
  morefocus: 'reflections, rotations, dilations and sequences of transformations',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['pre-image / image', 'The figure before / after a transformation.', '⟨A \\to A\'⟩'], ['rigid motion', 'Keeps size and shape: translation, reflection, rotation.', 'congruent'],
      ['dilation', 'Changes size by a scale factor ⟨k⟩; keeps shape.', 'similar'], ['quadrants', 'I ⟨(+,+)⟩, II ⟨(-,+)⟩, III ⟨(-,-)⟩, IV ⟨(+,-)⟩.', '⟨(-2, 3)⟩ in II']] },
    { title: 'Distance & Midpoint', color: 'blue', kind: 'table', plain: true, head: ['Formula', 'Example'], rows: [
      ['⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩', '⟨(1, 2), (5, 5)⟩: ⟨\\sqrt{16 + 9} = 5⟩'], ['⟨M = \\left(\\tfrac{x_1 + x_2}{2}, \\tfrac{y_1 + y_2}{2}\\right)⟩', '⟨(2, 1), (8, 5)⟩: ⟨(5, 3)⟩']],
      check: { list: ['Math.sqrt(16+9)', '(2+8)/2', '(1+5)/2'], is: [5, 5, 3] } },
    { title: 'Slope, Parallel & Perpendicular', color: 'green', kind: 'list', items: [
      '⟨m = \\dfrac{y_2 - y_1}{x_2 - x_1}⟩: ⟨(1, 2)⟩ to ⟨(4, 6)⟩ gives ⟨\\tfrac{4}{3}⟩.', 'Parallel lines: equal slopes.', 'Perpendicular lines: ⟨m_1 m_2 = -1⟩ (opposite reciprocals).', 'Use slopes to show a quadrilateral is a parallelogram or has right angles.'],
      check: { num: '(6-2)/(4-1)', is: 4 / 3 } },
    { title: 'Translations', color: 'orange', kind: 'example', text: 'Slide every point the same way: ⟨(x, y) \\to (x + a, y + b)⟩.',
      example: 'Translate right 2, down 5.', steps: [['Rule:', '⟨(x, y) \\to (x + 2, y - 5)⟩'], ['⟨(1, 3)⟩:', '⟨\\to (3, -2)⟩']], answer: 'blue → pink', fig: pl('tr', map((x, y) => [x + 2, y - 5])), check: { list: ['1+2', '3-5'], is: [3, -2] } },
    { title: 'Reflections', color: 'pink', kind: 'table', head: ['Over', 'Rule'], rows: [
      ['x-axis', '⟨(x, y) \\to (x, -y)⟩'], ['y-axis', '⟨(x, y) \\to (-x, y)⟩'], ['⟨y = x⟩', '⟨(x, y) \\to (y, x)⟩'], ['⟨y = -x⟩', '⟨(x, y) \\to (-y, -x)⟩']],
      fig: pl('rf', map((x, y) => [-x, y]), { vlines: [{ x: 0, color: '#999' }] }) },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Write points as ⟨(x, y)⟩: ⟨x⟩ first.', 'Transform every vertex, then connect.', 'Label images with primes: ⟨A\'⟩, ⟨A\'\'⟩.'],
      bad: [['Reflecting over the wrong axis', 'x-axis changes ⟨y⟩'], ['Over ⟨y = x⟩: keep the signs', 'swap the coordinates'], ['Mixing 90° and 270°', 'check the direction']] }
  ],
  back: [
    { title: 'Rotations About the Origin', color: 'purple', kind: 'table', head: ['Counterclockwise', 'Rule'], rows: [
      ['⟨90^\\circ⟩', '⟨(x, y) \\to (-y, x)⟩'], ['⟨180^\\circ⟩', '⟨(x, y) \\to (-x, -y)⟩'], ['⟨270^\\circ⟩ (= 90° clockwise)', '⟨(x, y) \\to (y, -x)⟩']],
      fig: pl('ro', map((x, y) => [-y, x])), check: { list: ['-1', '4'], is: [-1, 4] } },
    { title: 'Dilations', color: 'blue', kind: 'example', text: 'From the origin: ⟨(x, y) \\to (kx, ky)⟩. ⟨k > 1⟩ enlarges, ⟨0 < k < 1⟩ shrinks.',
      example: 'Dilate ⟨A(2, 3)⟩ by ⟨k = 2⟩.', steps: [['Multiply:', '⟨(2 \\cdot 2, 2 \\cdot 3)⟩']], answer: '⟨A\'(4, 6)⟩', check: { list: ['2*2', '2*3'], is: [4, 6] } },
    { title: 'Congruent or Similar?', color: 'green', kind: 'words', rows: [
      ['Translation, reflection, rotation (rigid motions)', 'congruent'], ['Dilation with ⟨k \\ne 1⟩', 'similar'], ['Rigid motions followed by a dilation', 'similar']] },
    { title: 'Sequences of Transformations', color: 'orange', kind: 'example', text: 'Do them in order; each image is the next pre-image.',
      example: '⟨A(1, 2)⟩: right 3, then reflect over the x-axis.', steps: [['Translate:', '⟨A_1(4, 2)⟩'], ['Reflect:', '⟨A_2(4, -2)⟩']], answer: '⟨A\'\'(4, -2)⟩', check: { list: ['1+3', '-2'], is: [4, -2] } },
    { title: 'Coordinate Proofs', color: 'pink', kind: 'list', items: [
      '<b>Parallelogram</b>: both pairs of opposite sides have equal slopes.', '<b>Rectangle</b>: also adjacent slopes multiply to ⟨-1⟩.', '<b>Rhombus</b>: all four side lengths equal (distance formula).', '<b>Right triangle</b>: two sides with perpendicular slopes.'] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I apply the rule to every vertex?', 'Is my rotation counterclockwise unless told otherwise?', 'For a sequence, did I use the first image as the next pre-image?', 'Does my image have the right orientation?'] }
  ]
};
