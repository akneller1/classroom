const Gm = require('../geo.cjs');
const iso = Gm.triangle([[20, 85], [80, 14], [140, 85]], ['B', 'A', 'C'], { w: 160, h: 100, ticks: [[1, 0, 1], [1, 2, 1]], angles: [[1, '40°', -12, 34], [0, '70°', 22, -6], [2, '70°', -26, -6]], lo: [[-8, 11], [0, -6], [8, 11]] });
const mid = Gm.triangle([[15, 105], [105, 24], [195, 105]], ['A', 'B', 'C'], { w: 210, h: 125, lo: [[-8, 8], [0, -7], [8, 8]], sides: [[0, 2, '18', 0, 16]] })
  .replace('</svg>', Gm.line(60, 64.5, 150, 64.5, Gm.B, 2.4) + Gm.t(105, 57, '9', { c: Gm.B }) + Gm.dot(60, 64.5, Gm.B) + Gm.dot(150, 64.5, Gm.B) + '</svg>');
module.exports = {
  name: 'geometry-triangle-relationships', course: 'Geometry', unitNo: 4, unitName: 'Triangle Relationships',
  focus: 'angle facts, inequalities and special segments in triangles',
  morefocus: 'midsegments, medians, bisectors, altitudes and points of concurrency',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['median', 'Vertex to the midpoint of the opposite side.', 'three in every triangle'], ['altitude', 'Vertex perpendicular to the opposite side.', '⟨AD \\perp BC⟩'],
      ['midsegment', 'Joins the midpoints of two sides.', '⟨DE \\parallel BC⟩'], ['exterior angle', 'Side and the extension of another side.', 'outside the triangle']] },
    { title: 'Angle Facts', color: 'blue', kind: 'list', items: [
      'The three angles add to ⟨180^\\circ⟩.', 'Exterior angle = the sum of the two remote interior angles.', 'Isosceles: the angles opposite the equal sides are equal.', 'Equilateral: every angle is ⟨60^\\circ⟩.'] },
    { title: 'Exterior Angle Theorem', color: 'green', kind: 'example', text: 'An exterior angle equals the sum of the two remote interior angles.',
      example: 'Remote interior angles are ⟨50^\\circ⟩ and ⟨65^\\circ⟩.', steps: [['Add:', '⟨50 + 65⟩']], answer: 'exterior angle = ⟨115^\\circ⟩', check: { num: '50+65', is: 115 } },
    { title: 'Isosceles Triangles', color: 'orange', kind: 'example', text: 'Base angles are equal. Subtract the vertex angle from 180, then split the rest.',
      example: 'The vertex angle is ⟨40^\\circ⟩. Find each base angle.', steps: [['Subtract:', '⟨180 - 40 = 140⟩'], ['Split:', '⟨\\tfrac{140}{2}⟩']], answer: 'each base angle = ⟨70^\\circ⟩', fig: iso, check: { num: '(180-40)/2', is: 70 } },
    { title: 'Triangle Inequality', color: 'pink', kind: 'example', text: 'Any two sides must add to more than the third. The third side is between the difference and the sum.',
      example: 'Two sides are 4 and 7. What can the third side be?', steps: [['Difference:', '⟨7 - 4 = 3⟩'], ['Sum:', '⟨4 + 7 = 11⟩']], answer: '⟨3 < x < 11⟩', check: { list: ['7-4', '4+7'], is: [3, 11] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Angles of a triangle add to ⟨180^\\circ⟩.', 'Exterior angle uses the two remote angles.', 'Check the triangle inequality with the two shorter sides.'],
      bad: [['Adding the adjacent interior angle to the exterior angle', 'they add to 180, they are not equal'], ['Using the sum only for the third side', 'it is also more than the difference'], ['Calling any median an altitude', 'a median goes to the midpoint']] }
  ],
  back: [
    { title: 'Sides and Angles', color: 'purple', kind: 'example', text: 'The longest side is opposite the largest angle. The shortest side is opposite the smallest angle.',
      example: 'Angles are ⟨50^\\circ⟩, ⟨60^\\circ⟩, ⟨70^\\circ⟩. Which side is longest?', steps: [['Largest angle:', '⟨70^\\circ⟩']], answer: 'the side opposite the ⟨70^\\circ⟩ angle', check: { true: 'Math.max(50,60,70) === 70' } },
    { title: 'Midsegment Theorem', color: 'blue', kind: 'example', text: 'A midsegment is parallel to the third side and half as long.',
      example: 'The third side is 18. How long is the midsegment?', steps: [['Halve:', '⟨\\tfrac{18}{2}⟩']], answer: 'midsegment = ⟨9⟩', fig: mid, check: { num: '18/2', is: 9 } },
    { title: 'Medians and the Centroid', color: 'green', kind: 'example', text: 'The medians meet at the centroid. It is ⟨\\tfrac{2}{3}⟩ of the way from each vertex to the midpoint.',
      example: 'A median is 12 long. How far is the centroid from the vertex?', steps: [['Multiply:', '⟨\\tfrac{2}{3} \\cdot 12⟩']], answer: '⟨8⟩ from the vertex, ⟨4⟩ from the midpoint', check: { list: ['2/3*12', '12-8'], is: [8, 4] } },
    { title: 'Perpendicular Bisector', color: 'orange', kind: 'example', text: 'Every point on the perpendicular bisector of a segment is the same distance from both endpoints.',
      example: '⟨PA = 3x + 2⟩ and ⟨PB = 5x - 6⟩ for a point ⟨P⟩ on the bisector of ⟨AB⟩.', steps: [['Set equal:', '⟨3x + 2 = 5x - 6⟩'], ['Solve:', '⟨x = 4⟩'], ['Substitute:', '⟨PA = 3(4) + 2⟩']], answer: '⟨PA = PB = 14⟩', check: { list: ['(2+6)/(5-3)', '3*4+2', '5*4-6'], is: [4, 14, 14] } },
    { title: 'Points of Concurrency', color: 'pink', kind: 'table', head: ['Point', 'Lines that meet', 'Property'], rows: [
      ['centroid', 'medians', '⟨\\tfrac{2}{3}⟩ from each vertex'], ['circumcenter', 'perpendicular bisectors', 'equal distance to the vertices'], ['incenter', 'angle bisectors', 'equal distance to the sides'], ['orthocenter', 'altitudes', 'inside, on or outside the triangle']] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Do the angles add to ⟨180^\\circ⟩?', 'Is the longest side opposite the largest angle?', 'Did I use the two remote angles for the exterior angle?', 'Which special segment is it: median, altitude or bisector?'] }
  ]
};
