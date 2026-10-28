const Gm = require('../geo.cjs');
const par = Gm.svg(220, 100, '<polygon points="20,85 60,20 200,20 160,85" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/>' + Gm.line(20, 85, 200, 20, '#999', 1.3, true) + Gm.line(60, 20, 160, 85, '#999', 1.3, true) + Gm.t(10, 95, 'A', { fs: 10 }) + Gm.t(56, 14, 'D', { fs: 10 }) + Gm.t(208, 14, 'C', { fs: 10 }) + Gm.t(168, 97, 'B', { fs: 10 }) + Gm.t(30, 60, '70°', { c: '#db2777', fs: 10 }) + Gm.t(146, 76, '?', { c: '#db2777', fs: 10 }), 2.0);
const trap = Gm.svg(220, 100, '<polygon points="20,85 70,20 150,20 200,85" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/>' + Gm.line(45, 52, 175, 52, '#db2777', 2.4) + Gm.t(110, 14, '10', { c: '#2563eb' }) + Gm.t(110, 97, '16', { c: '#2563eb' }) + Gm.t(110, 45, 'm', { c: '#db2777' }), 2.0);
module.exports = {
  name: 'geometry-quadrilaterals-polygons', course: 'Geometry', unitNo: 7, unitName: 'Quadrilaterals and Polygons',
  focus: 'polygon angle sums and the properties of quadrilaterals',
  morefocus: 'parallelograms, rectangles, rhombuses, trapezoids, kites and coordinate proofs',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['parallelogram', 'Quadrilateral with both pairs of opposite sides parallel.', '⟨AB \\parallel DC⟩'], ['rhombus', 'Parallelogram with four congruent sides.', 'diagonals are perpendicular'],
      ['trapezoid', 'Quadrilateral with exactly one pair of parallel sides.', 'bases and legs'], ['kite', 'Two pairs of adjacent congruent sides.', 'diagonals are perpendicular']] },
    { title: 'Polygon Angle Sums', color: 'blue', kind: 'table', head: ['Sides', 'Interior angle sum'], rows: [
      ['3', '⟨180^\\circ⟩'], ['4', '⟨360^\\circ⟩'], ['5', '⟨540^\\circ⟩'], ['⟨n⟩', '⟨(n - 2) \\cdot 180^\\circ⟩']],
      after: 'The exterior angles of any convex polygon add to ⟨360^\\circ⟩.', check: { list: ['(3-2)*180', '(4-2)*180', '(5-2)*180'], is: [180, 360, 540] } },
    { title: 'Interior Angle Sum', color: 'green', kind: 'example', text: 'Use ⟨(n - 2) \\cdot 180⟩.',
      example: 'Find the interior angle sum of a hexagon.', steps: [['Sides:', '⟨n = 6⟩'], ['Multiply:', '⟨(6 - 2) \\cdot 180⟩']], answer: '⟨720^\\circ⟩', check: { num: '(6-2)*180', is: 720 } },
    { title: 'Regular Polygons', color: 'orange', kind: 'example', text: 'Each exterior angle is ⟨\\tfrac{360}{n}⟩. Each interior angle is 180 minus that.',
      example: 'A regular octagon: find one exterior and one interior angle.', steps: [['Exterior:', '⟨\\tfrac{360}{8} = 45⟩'], ['Interior:', '⟨180 - 45⟩']], answer: 'exterior ⟨45^\\circ⟩, interior ⟨135^\\circ⟩', check: { list: ['360/8', '180-360/8', '(8-2)*180/8'], is: [45, 135, 135] } },
    { title: 'Parallelogram Properties', color: 'pink', kind: 'list', items: [
      'Opposite sides are parallel and congruent.', 'Opposite angles are congruent.', 'Consecutive angles are supplementary (add to ⟨180^\\circ⟩).', 'The diagonals bisect each other.'] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Count the sides to find ⟨n⟩ first.', 'Consecutive angles of a parallelogram add to ⟨180^\\circ⟩.', 'Exterior angles add to ⟨360^\\circ⟩ for every convex polygon.'],
      bad: [['Using ⟨n \\cdot 180⟩', 'subtract 2 from ⟨n⟩ first'], ['Thinking diagonals of every parallelogram are congruent', 'only in a rectangle'], ['Calling every trapezoid a parallelogram', 'a trapezoid has only one pair of parallel sides']] }
  ],
  back: [
    { title: 'Special Parallelograms', color: 'purple', kind: 'table', head: ['Shape', 'Extra properties'], rows: [
      ['rectangle', 'four right angles; diagonals congruent'], ['rhombus', 'four congruent sides; diagonals perpendicular and bisect the angles'], ['square', 'all of the above: a rectangle and a rhombus']] },
    { title: 'Angles in a Parallelogram', color: 'blue', kind: 'example', text: 'Consecutive angles are supplementary; opposite angles are equal.',
      example: '⟨\\angle A = 70^\\circ⟩. Find ⟨\\angle B⟩ (next to ⟨A⟩).', steps: [['Subtract:', '⟨180 - 70⟩']], answer: '⟨\\angle B = 110^\\circ⟩', fig: par, check: { num: '180-70', is: 110 } },
    { title: 'Algebra with Sides', color: 'green', kind: 'example', text: 'Opposite sides are congruent. Set them equal and solve.',
      example: 'Opposite sides: ⟨3x + 1⟩ and ⟨2x + 6⟩.', steps: [['Set equal:', '⟨3x + 1 = 2x + 6⟩'], ['Solve:', '⟨x = 5⟩'], ['Substitute:', '⟨3(5) + 1⟩']], answer: 'each side is ⟨16⟩', check: { list: ['6-1', '3*5+1', '2*5+6'], is: [5, 16, 16] } },
    { title: 'Trapezoid Midsegment', color: 'orange', kind: 'example', text: 'The midsegment is parallel to the bases and its length is the mean of the bases.',
      example: 'The bases are 10 and 16. Find the midsegment ⟨m⟩.', steps: [['Average:', '⟨m = \\tfrac{10 + 16}{2}⟩']], answer: '⟨m = 13⟩', fig: trap, check: { num: '(10+16)/2', is: 13 } },
    { title: 'Rhombus Diagonals', color: 'pink', kind: 'example', text: 'The diagonals are perpendicular and bisect each other, so half-diagonals are the legs of a right triangle.',
      example: 'Diagonals are 6 and 8. Find the side and the area.', steps: [['Half-diagonals 3 and 4:', '⟨3^2 + 4^2 = 25⟩'], ['Area:', '⟨\\tfrac{6 \\cdot 8}{2}⟩']], answer: 'side ⟨5⟩, area ⟨24⟩', check: { list: ['Math.sqrt(3**2+4**2)', '6*8/2'], is: [5, 24] } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I use ⟨(n - 2) \\cdot 180⟩ for the interior sum?', 'Is the shape a parallelogram first, then a special one?', 'Did I check slopes for parallel and distances for equal sides?', 'Do the answers fit the figure (angles add to ⟨360^\\circ⟩)?'] }
  ]
};
