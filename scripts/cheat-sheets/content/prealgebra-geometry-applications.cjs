/* Pre-Algebra (8th Grade) Unit 7 cheat sheet. Every worked example is checked by build.cjs; figures are drawn from the same numbers. */
const F = require('../figs.cjs'), Gm = require('../geo.cjs');
const right = Gm.triangle([[20, 95], [140, 95], [140, 25]], ['', '', ''], { sides: [[0, 1, 'a = 9', 0, 14], [1, 2, 'b = 12', 26, 0], [0, 2, 'c', -8, -8]], right: 1, rdx: -12, w: 200, h: 110, in: 1.6 });
const dist = F.plane({ id: 'g7a', xmin: -1, xmax: 6, ymin: -1, ymax: 6, size: 1.25, ticks: 1,
  segments: [{ x1: 1, y1: 1, x2: 5, y2: 4, color: '#2563eb', w: 2.4 }, { x1: 1, y1: 1, x2: 5, y2: 1, color: '#db2777', dashed: true, w: 1.6 }, { x1: 5, y1: 1, x2: 5, y2: 4, color: '#db2777', dashed: true, w: 1.6 }],
  points: [{ x: 1, y: 1, label: '(1, 1)', dx: -8, dy: 14 }, { x: 5, y: 4, label: '(5, 4)', dx: -20, dy: -7 }], labels: [{ x: 3, y: 0.45, t: '4', color: '#db2777' }, { x: 5.4, y: 2.4, t: '3', color: '#db2777' }] });
const solids = Gm.svg(300, 92,
  // cylinder
  '<ellipse cx="50" cy="20" rx="34" ry="9" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/><path d="M16 20 V70 A34 9 0 0 0 84 70 V20" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/>' + Gm.line(50, 20, 84, 20, '#db2777', 1.5) + Gm.t(66, 15, 'r', { c: '#db2777', fs: 10 }) + Gm.t(94, 48, 'h', { c: '#2563eb', fs: 10 }) + Gm.t(50, 90, 'cylinder', { fs: 10 }) +
  // cone
  '<path d="M116 70 L150 12 L184 70" fill="#fde8f1" stroke="#1f2a6b" stroke-width="2"/><ellipse cx="150" cy="70" rx="34" ry="9" fill="#fde8f1" stroke="#1f2a6b" stroke-width="2"/>' + Gm.line(150, 12, 150, 70, '#2563eb', 1.5, true) + Gm.line(150, 70, 184, 70, '#db2777', 1.5) + Gm.t(156, 46, 'h', { c: '#2563eb', fs: 10 }) + Gm.t(168, 66, 'r', { c: '#db2777', fs: 10 }) + Gm.t(150, 90, 'cone', { fs: 10 }) +
  // sphere
  '<circle cx="250" cy="44" r="32" fill="#e6f8ec" stroke="#1f2a6b" stroke-width="2"/><ellipse cx="250" cy="44" rx="32" ry="8" fill="none" stroke="#1f2a6b" stroke-width="1" stroke-dasharray="4 3"/>' + Gm.line(250, 44, 282, 44, '#db2777', 1.5) + Gm.t(266, 39, 'r', { c: '#db2777', fs: 10 }) + Gm.t(250, 90, 'sphere', { fs: 10 }), 2.9);
module.exports = {
  name: 'prealgebra-geometry-applications', course: 'Pre-Algebra (8th Grade)', unitNo: 7, unitName: 'Geometry',
  focus: 'the Pythagorean theorem and its converse in 2-D, 3-D and on the coordinate plane',
  morefocus: 'volume of cylinders, cones, spheres and composite solids',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['legs', 'The two sides that form the right angle.', '⟨a⟩ and ⟨b⟩'],
      ['hypotenuse', 'The longest side, across from the right angle.', '⟨c⟩'],
      ['Pythagorean triple', 'Whole-number sides of a right triangle.', '3-4-5, 5-12-13, 8-15-17'],
      ['converse', 'If ⟨a^2 + b^2 = c^2⟩, the triangle is right.', '6, 8, 10 is right']] },
    { title: 'The Pythagorean Theorem', color: 'blue', kind: 'example', text: 'In a right triangle, ⟨a^2 + b^2 = c^2⟩ (⟨c⟩ is the hypotenuse).',
      example: 'Legs 9 and 12. Find ⟨c⟩.', steps: [['Substitute:', '⟨9^2 + 12^2 = 81 + 144 = 225⟩'], ['Square root:', '⟨c = \\sqrt{225}⟩']], answer: '⟨c = 15⟩', fig: right,
      check: { num: 'Math.hypot(9,12)', is: 15 } },
    { title: 'Finding a Leg', color: 'green', kind: 'example', text: 'Subtract: ⟨a^2 = c^2 - b^2⟩.',
      example: 'A 13-ft ladder reaches 12 ft up a wall. How far is its base from the wall?', steps: [['Subtract:', '⟨a^2 = 13^2 - 12^2 = 169 - 144 = 25⟩']], answer: '⟨a = 5⟩ ft',
      check: { num: 'Math.sqrt(13**2-12**2)', is: 5 } },
    { title: 'Is It a Right Triangle?', color: 'orange', kind: 'table', plain: true, head: ['Sides', 'Test ⟨a^2 + b^2 \\stackrel{?}{=} c^2⟩', 'Right?'], rows: [
      ['7, 24, 25', '⟨49 + 576 = 625⟩', 'yes'], ['5, 9, 11', '⟨25 + 81 = 106 \\ne 121⟩', 'no'], ['10, 24, 26', '⟨100 + 576 = 676⟩', 'yes']],
      after: 'Always use the <b>longest</b> side as ⟨c⟩.', check: [{ num: '7**2+24**2', is: 625 }, { num: '5**2+9**2', is: 106 }, { num: '10**2+24**2', is: 676 }] },
    { title: 'Distance Between Points', color: 'pink', kind: 'example', text: 'Draw a right triangle: the legs are the horizontal and vertical distances. ⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩.',
      example: 'From ⟨(1, 1)⟩ to ⟨(5, 4)⟩', steps: [['Legs:', '⟨5 - 1 = 4⟩ and ⟨4 - 1 = 3⟩'], ['Theorem:', '⟨d = \\sqrt{16 + 9}⟩']], answer: '⟨d = 5⟩', fig: dist,
      check: { num: 'Math.hypot(5-1,4-1)', is: 5 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['The hypotenuse is always the longest side.', 'Round only at the end; ⟨\\sqrt{50} \\approx 7.07⟩.', 'Draw a picture for word problems.'],
      bad: [['⟨a + b = c⟩', 'square first: ⟨a^2 + b^2 = c^2⟩'], ['Adding when finding a leg', 'subtract from ⟨c^2⟩'], ['Stopping at ⟨c^2 = 225⟩', 'take the square root']] }
  ],
  back: [
    { title: 'Pythagorean Theorem in 3-D', color: 'purple', kind: 'example', text: 'The diagonal of a box: use the theorem twice, or ⟨d = \\sqrt{\\ell^2 + w^2 + h^2}⟩.',
      example: 'A box is 3 by 4 by 12. Find the longest diagonal.', steps: [['Base diagonal:', '⟨\\sqrt{3^2 + 4^2} = 5⟩'], ['Space diagonal:', '⟨\\sqrt{5^2 + 12^2} = \\sqrt{169}⟩']], answer: '⟨d = 13⟩',
      check: [{ num: 'Math.hypot(3,4)', is: 5 }, { num: 'Math.hypot(3,4,12)', is: 13 }] },
    { title: 'Volume Formulas', color: 'blue', kind: 'table', plain: true, head: ['Solid', 'Volume'], rows: [
      ['cylinder', '⟨V = \\pi r^2 h⟩'], ['cone', '⟨V = \\tfrac{1}{3}\\pi r^2 h⟩'], ['sphere', '⟨V = \\tfrac{4}{3}\\pi r^3⟩']], fig: solids,
      after: 'A cone holds ⟨\\tfrac{1}{3}⟩ of the cylinder with the same base and height. Answers are in cubic units.' },
    { title: 'Volume Examples', color: 'green', kind: 'table', plain: true, head: ['Solid', 'Work', 'Volume'], rows: [
      ['cylinder ⟨r = 3, h = 5⟩', '⟨\\pi(9)(5)⟩', '⟨45\\pi \\approx 141.4⟩'], ['cone ⟨r = 3, h = 5⟩', '⟨\\tfrac{1}{3}\\pi(9)(5)⟩', '⟨15\\pi \\approx 47.1⟩'], ['sphere ⟨r = 3⟩', '⟨\\tfrac{4}{3}\\pi(27)⟩', '⟨36\\pi \\approx 113.1⟩']],
      after: 'Leave answers in terms of ⟨\\pi⟩ or round as the problem asks. Diameter 10 means ⟨r = 5⟩.',
      check: [{ num: 'Math.PI*9*5', is: 141.3716694115407 }, { num: 'Math.PI*9*5/3', is: 47.12388980384689 }, { num: '4/3*Math.PI*27', is: 113.09733552923255 }] },
    { title: 'Solving for a Missing Dimension', color: 'orange', kind: 'example', text: 'Substitute what you know into the formula, then solve.',
      example: 'A cylinder has volume ⟨72\\pi⟩ and radius 3. Find the height.', steps: [['Formula:', '⟨72\\pi = \\pi(3)^2 h = 9\\pi h⟩'], ['Divide by ⟨9\\pi⟩:', '⟨h = 8⟩']], answer: '⟨h = 8⟩',
      check: { num: '72/9', is: 8 } },
    { title: 'Composite Solids', color: 'pink', kind: 'example', text: 'Split into familiar solids. Add the parts (or subtract a hole).',
      example: 'An ice-cream cone: a cone (⟨r = 2, h = 6⟩) topped with a half sphere (⟨r = 2⟩).', steps: [['Cone:', '⟨\\tfrac{1}{3}\\pi(4)(6) = 8\\pi⟩'], ['Half sphere:', '⟨\\tfrac{1}{2} \\cdot \\tfrac{4}{3}\\pi(8) = \\tfrac{16}{3}\\pi⟩']], answer: '⟨\\tfrac{40}{3}\\pi \\approx 41.9⟩ cubic units',
      check: { num: 'Math.PI*4*6/3 + 0.5*4/3*Math.PI*8', is: 41.88790204786391 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Is ⟨c⟩ the longest side (across from the right angle)?', 'Did I use the radius, not the diameter?', 'Did I cube the radius for a sphere and square it for a cylinder or cone?', 'Are my units cubic for volume?'] }
  ]
};
