const Gm = require('../geo.cjs');
const rt = (labels, sides, ang, o) => Gm.triangle([[20, 95], [180, 95], [180, 20]], labels, Object.assign({ w: 210, h: 110, in: 1.5, right: 1, rdx: -12, rdy: -12, sides, angles: ang ? [[0, ang, 30, -6]] : [] }, o || {}));
module.exports = {
  name: 'geometry-right-triangles-trigonometry', course: 'Geometry', unitNo: 6, unitName: 'Right Triangles and Trigonometry',
  focus: 'the Pythagorean Theorem, special right triangles and trig ratios',
  morefocus: 'finding sides and angles with SOH-CAH-TOA, elevation and depression',
  front: [
    { title: 'Pythagorean Theorem', color: 'purple', kind: 'example', text: 'In a right triangle with legs ⟨a, b⟩ and hypotenuse ⟨c⟩ (opposite the right angle): ⟨a^2 + b^2 = c^2⟩.',
      example: 'Legs 7 and 24', steps: [['Substitute:', '⟨49 + 576 = c^2⟩']], answer: '⟨c = 25⟩', fig: rt(['', '', ''], [[0, 1, 'a', 0, 14], [1, 2, 'b', 10, 0], [0, 2, 'c', -6, -8]]), check: { num: 'Math.sqrt(49+576)', is: 25 } },
    { title: 'Converse: Classify by Sides', color: 'blue', kind: 'table', plain: true, head: ['Longest side ⟨c⟩', 'Triangle'], rows: [
      ['⟨c^2 = a^2 + b^2⟩', 'right'], ['⟨c^2 < a^2 + b^2⟩', 'acute'], ['⟨c^2 > a^2 + b^2⟩', 'obtuse']],
      after: 'Sides 6, 8, 11: ⟨121 > 36 + 64 = 100⟩, so obtuse. Common triples: 3-4-5, 5-12-13, 8-15-17.', check: { true: '11**2 > 6**2+8**2 && 13**2 == 5**2+12**2 && 17**2 == 8**2+15**2' } },
    { title: 'Special Right Triangles', color: 'green', kind: 'table', head: ['Triangle', 'Side ratio', 'Example'], rows: [
      ['45°-45°-90°', '⟨x : x : x\\sqrt{2}⟩', 'leg 5 → hyp ⟨5\\sqrt{2}⟩'], ['30°-60°-90°', '⟨x : x\\sqrt{3} : 2x⟩', 'short leg 4 → ⟨4\\sqrt{3}⟩, 8']],
      after: 'In a 30-60-90, the short leg is opposite 30° and the hypotenuse is twice it.', check: { list: ['4**2+(4*Math.sqrt(3))**2', '5**2+5**2'], is: [64, 50] } },
    { title: 'Trig Ratios: SOH-CAH-TOA', color: 'orange', kind: 'table', head: ['Ratio', 'Definition'], rows: [
      ['⟨\\sin\\theta⟩', '⟨\\dfrac{\\text{opposite}}{\\text{hypotenuse}}⟩'], ['⟨\\cos\\theta⟩', '⟨\\dfrac{\\text{adjacent}}{\\text{hypotenuse}}⟩'], ['⟨\\tan\\theta⟩', '⟨\\dfrac{\\text{opposite}}{\\text{adjacent}}⟩']] },
    { title: 'Labeling the Sides', color: 'pink', kind: 'list', items: [
      '<b>Hypotenuse</b>: across from the right angle; always the longest.', '<b>Opposite</b>: across from the angle ⟨\\theta⟩ you are using.', '<b>Adjacent</b>: next to ⟨\\theta⟩, not the hypotenuse.'],
      fig: rt(['', '', ''], [[0, 1, 'adjacent', 0, 14], [1, 2, 'opposite', 30, 0], [0, 2, 'hypotenuse', -16, -10]], 'θ', { in: 1.7, w: 250 }) },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Calculator in <b>degree</b> mode.', 'Label opposite, adjacent and hypotenuse from the angle you are using.', 'Round only at the end.'],
      bad: [['⟨a^2 + c^2 = b^2⟩', '⟨c⟩ must be the hypotenuse'], ['Opposite and adjacent swapped', 'they depend on the angle'], ['⟨\\sin^{-1}⟩ to find a side', 'inverse trig finds angles']] }
  ],
  back: [
    { title: 'Finding a Side with Sine', color: 'purple', kind: 'example', text: 'Opposite and hypotenuse → sine.',
      example: '⟨35^\\circ⟩, hypotenuse 12, find the opposite side ⟨x⟩.', steps: [['Ratio:', '⟨\\sin 35^\\circ = \\tfrac{x}{12}⟩'], ['Solve:', '⟨x = 12\\sin 35^\\circ⟩']], answer: '⟨x \\approx 6.9⟩', check: { num: 'Math.round(12*Math.sin(35*Math.PI/180)*10)/10', is: 6.9 } },
    { title: 'Finding a Side with Cosine', color: 'blue', kind: 'example', text: 'Adjacent and hypotenuse → cosine.',
      example: '⟨40^\\circ⟩, hypotenuse 15, find the adjacent side ⟨x⟩.', steps: [['Ratio:', '⟨\\cos 40^\\circ = \\tfrac{x}{15}⟩'], ['Solve:', '⟨x = 15\\cos 40^\\circ⟩']], answer: '⟨x \\approx 11.5⟩', check: { num: 'Math.round(15*Math.cos(40*Math.PI/180)*10)/10', is: 11.5 } },
    { title: 'Side in the Denominator', color: 'green', kind: 'example', text: 'When the unknown is on the bottom, multiply, then divide.',
      example: '⟨\\tan 28^\\circ = \\tfrac{9}{x}⟩', steps: [['Rearrange:', '⟨x = \\dfrac{9}{\\tan 28^\\circ}⟩']], answer: '⟨x \\approx 16.9⟩', check: { num: 'Math.round(9/Math.tan(28*Math.PI/180)*10)/10', is: 16.9 } },
    { title: 'Finding an Angle (Inverse Trig)', color: 'orange', kind: 'example', text: 'Know two sides, want the angle: use ⟨\\sin^{-1}⟩, ⟨\\cos^{-1}⟩ or ⟨\\tan^{-1}⟩.',
      example: 'Opposite 7, adjacent 24', steps: [['Ratio:', '⟨\\tan\\theta = \\tfrac{7}{24}⟩'], ['Inverse:', '⟨\\theta = \\tan^{-1}\\left(\\tfrac{7}{24}\\right)⟩']], answer: '⟨\\theta \\approx 16.3^\\circ⟩', check: { num: 'Math.round(Math.atan(7/24)*180/Math.PI*10)/10', is: 16.3 } },
    { title: 'Elevation & Depression', color: 'pink', kind: 'example', text: 'Both angles are measured from a <b>horizontal</b> line. Draw the right triangle, then use SOH-CAH-TOA.',
      example: 'From 50 ft away, the angle of elevation to a roof is ⟨32^\\circ⟩. Height?', steps: [['Ratio:', '⟨\\tan 32^\\circ = \\tfrac{h}{50}⟩'], ['Solve:', '⟨h = 50\\tan 32^\\circ⟩']], answer: '⟨h \\approx 31.2⟩ ft', check: { num: 'Math.round(50*Math.tan(32*Math.PI/180)*10)/10', is: 31.2 } },
    { title: 'Choosing the Ratio', color: 'teal', kind: 'words', rows: [
      ['Know or need opposite and hypotenuse', 'sine'], ['Know or need adjacent and hypotenuse', 'cosine'], ['Know or need opposite and adjacent', 'tangent'], ['Know two sides, need the third (right triangle)', 'Pythagorean Thm.']] }
  ]
};
