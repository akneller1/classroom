const Gm = require('../geo.cjs');
const Lshape = Gm.svg(130, 125, '<polygon points="15,110 105,110 105,50 75,50 75,5 45,5 45,50 15,50" fill="#e6f8ec" stroke="#16a34a" stroke-width="2"/>' +
  Gm.line(45, 50, 75, 50, '#999', 1, true) + Gm.t(60, 123, '6', { c: '#2563eb', fs: 10 }) + Gm.t(7, 84, '4', { c: '#2563eb', fs: 10 }) + Gm.t(60, 0 + 16, '2', { c: '#2563eb', fs: 10 }) + Gm.t(84, 30, '3', { c: '#2563eb', fs: 10 }), 1.15);
module.exports = {
  name: 'geometry-area-surface-area-volume', course: 'Geometry', unitNo: 10, unitName: 'Area, Surface Area and Volume',
  focus: 'area formulas, composite figures and units',
  morefocus: 'surface area and volume of prisms, cylinders, pyramids, cones and spheres',
  front: [
    { title: 'Area & Units', color: 'purple', kind: 'words', rows: [
      ['<b>Area</b>: space inside a 2-D figure', 'square units (cm², ft²)'], ['<b>Perimeter</b>: distance around', 'linear units (cm, ft)'], ['<b>Surface area</b>: total area of the outside faces', 'square units'], ['<b>Volume</b>: space inside a 3-D figure', 'cubic units (cm³, ft³)']] },
    { title: 'Polygon Area Formulas', color: 'blue', kind: 'table', head: ['Figure', 'Area'], rows: [
      ['rectangle', '⟨A = lw⟩'], ['square', '⟨A = s^2⟩'], ['triangle', '⟨A = \\tfrac{1}{2}bh⟩'], ['parallelogram', '⟨A = bh⟩'], ['trapezoid', '⟨A = \\tfrac{1}{2}(b_1 + b_2)h⟩'], ['circle', '⟨A = \\pi r^2⟩']],
      after: 'Height ⟨h⟩ is always perpendicular to the base (not a slanted side).' },
    { title: 'Trapezoid Example', color: 'green', kind: 'example', text: 'Average the two parallel bases, then multiply by the height.',
      example: 'Bases 6 cm and 10 cm, height 4 cm', steps: [['Formula:', '⟨\\tfrac{1}{2}(6 + 10)(4) = \\tfrac{1}{2}(16)(4)⟩']], answer: '⟨32 \\text{ cm}^2⟩', check: { num: '0.5*(6+10)*4', is: 32 } },
    { title: 'Composite Figures', color: 'orange', kind: 'example', text: 'Split into simple shapes; add (or subtract) their areas.',
      example: 'A 6 × 4 rectangle with a 2 × 3 rectangle on top', steps: [['Areas:', '⟨6 \\times 4 = 24⟩ and ⟨2 \\times 3 = 6⟩'], ['Add:', '⟨24 + 6⟩']], answer: '30 square units', fig: Lshape, check: { num: '6*4+2*3', is: 30 } },
    { title: 'Circles', color: 'pink', kind: 'table', head: ['Find', 'Formula', 'r = 3'], rows: [
      ['circumference', '⟨C = 2\\pi r⟩', '⟨6\\pi \\approx 18.8⟩'], ['area', '⟨A = \\pi r^2⟩', '⟨9\\pi \\approx 28.3⟩']], check: { list: ['Math.round(6*Math.PI*10)/10', 'Math.round(9*Math.PI*10)/10'], is: [18.8, 28.3] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Square units for area, cubic units for volume.', 'Use the perpendicular height.', 'Keep ⟨\\pi⟩ unless asked to round.'],
      bad: [['Slant side as height', 'use the perpendicular height'], ['Diameter for ⟨r⟩', 'halve it'], ['Forgetting a face', 'list every face for surface area']] }
  ],
  back: [
    { title: 'Prisms', color: 'purple', kind: 'example', text: '⟨V = Bh⟩ (⟨B⟩ = base area). ⟨SA = Ph + 2B⟩ (⟨P⟩ = base perimeter).',
      example: 'Rectangular prism 5 × 3 × 4', steps: [['Volume:', '⟨5 \\cdot 3 \\cdot 4 = 60⟩'], ['SA:', '⟨2(15 + 20 + 12) = 94⟩']], answer: '⟨V = 60⟩ units³, ⟨SA = 94⟩ units²', check: { list: ['5*3*4', '2*(5*3+5*4+3*4)'], is: [60, 94] } },
    { title: 'Cylinders', color: 'blue', kind: 'example', text: '⟨V = \\pi r^2 h⟩. ⟨SA = 2\\pi r^2 + 2\\pi rh⟩ (two circles + the curved side).',
      example: '⟨r = 3⟩, ⟨h = 8⟩', steps: [['Volume:', '⟨\\pi(9)(8) = 72\\pi⟩'], ['SA:', '⟨18\\pi + 48\\pi = 66\\pi⟩']], answer: '⟨72\\pi⟩ units³, ⟨66\\pi⟩ units²', check: { list: ['9*8', '2*9+2*3*8'], is: [72, 66] } },
    { title: 'Pyramids & Cones', color: 'green', kind: 'table', head: ['Solid', 'Volume', 'Surface area'], rows: [
      ['pyramid', '⟨\\tfrac{1}{3}Bh⟩', '⟨B + \\tfrac{1}{2}P\\ell⟩'], ['cone', '⟨\\tfrac{1}{3}\\pi r^2 h⟩', '⟨\\pi r^2 + \\pi r\\ell⟩']],
      after: '⟨h⟩ = vertical height; ⟨\\ell⟩ = slant height (on the face). A pyramid holds ⟨\\tfrac{1}{3}⟩ of the matching prism.' },
    { title: 'Spheres', color: 'orange', kind: 'example', text: '⟨V = \\tfrac{4}{3}\\pi r^3⟩. ⟨SA = 4\\pi r^2⟩.',
      example: '⟨r = 3⟩', steps: [['Volume:', '⟨\\tfrac{4}{3}\\pi(27) = 36\\pi⟩'], ['SA:', '⟨4\\pi(9) = 36\\pi⟩']], answer: '⟨36\\pi⟩ units³ and ⟨36\\pi⟩ units²', check: { list: ['4/3*27', '4*9'], is: [36, 36] } },
    { title: 'Volume Example', color: 'pink', kind: 'example', text: 'Find the base area first, then multiply by the height.',
      example: 'Cylinder ⟨r = 4⟩, ⟨h = 10⟩', steps: [['Base:', '⟨\\pi(4)^2 = 16\\pi⟩'], ['Volume:', '⟨16\\pi(10)⟩']], answer: '⟨160\\pi \\approx 502.7⟩ units³', check: { num: 'Math.round(160*Math.PI*10)/10', is: 502.7 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I use the radius (not the diameter)?', 'Vertical height for volume; slant height for surface area of pyramids and cones.', 'Did I include every face?', 'Are my units squared (area) or cubed (volume)?'] }
  ]
};
