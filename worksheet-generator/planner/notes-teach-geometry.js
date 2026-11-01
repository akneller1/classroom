/* Teaching notes for the Geometry lesson planner (see notes-teach.js for the format).
   Figures are built from exact coordinates (pol() places a point at a given angle), so every angle and length that is
   labeled is drawn to that size unless the caption says otherwise. */
(function (G) {
  'use strict';
  var T = (G.MKPLAN_TEACH = G.MKPLAN_TEACH || {}), N = T.geometry = T.geometry || {};
  function pol(r, deg, o) { o = o || [0, 0]; var a = deg * Math.PI / 180; return [o[0] + r * Math.cos(a), o[1] + r * Math.sin(a)]; }
  function mid(a, b) { return [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]; }
  /* Two parallel lines cut by a transversal; angles 1–4 at the top crossing, 5–8 at the bottom.
     hi: { '1': label, '5': label, … } marks and labels those angles. */
  function transversal(hi, cap, marks) {
    var P = { _a: [-1, 3], _b: [7, 3], _c: [-1, 0], _d: [7, 0], _e: [1, -1.5], _f: [5, 4.5], _p: [4, 3], _q: [2, 0] };
    // helper points one unit along each ray from the two crossings
    P._m1 = [0.2, 3]; P._m2 = [1.2, 3]; P._n1 = [5.6, 0]; P._n2 = [6.6, 0]; P._pr = [5, 3]; P._pl = [3, 3]; P._pu = pol(1, 56.31, [4, 3]); P._pd = pol(1, 236.31, [4, 3]);
    P._qr = [3, 0]; P._ql = [1, 0]; P._qu = pol(1, 56.31, [2, 0]); P._qd = pol(1, 236.31, [2, 0]);
    var where = { 1: ['_pl', '_p', '_pu'], 2: ['_pu', '_p', '_pr'], 3: ['_pd', '_p', '_pl'], 4: ['_pr', '_p', '_pd'], 5: ['_ql', '_q', '_qu'], 6: ['_qu', '_q', '_qr'], 7: ['_qd', '_q', '_ql'], 8: ['_qr', '_q', '_qd'] };
    var bis = { 1: 118, 2: 28, 3: 208, 4: 298, 5: 118, 6: 28, 7: 208, 8: 298 };
    var txt = [], ang = [];
    for (var k = 1; k <= 8; k++) {
      var o = k <= 4 ? [4, 3] : [2, 0], p = pol(0.62, bis[k], o);
      if (hi && hi[k] !== undefined) { var w = where[k]; ang.push([w[0], w[1], w[2], '', 1, (marks && marks[k]) || '#1f5fbf', 13]); txt.push([p[0], p[1] - 0.12, hi[k] === true ? String(k) : hi[k], 10.5, (marks && marks[k]) || '#1f5fbf']); }
      else txt.push([p[0], p[1] - 0.12, String(k), 9.5, '#666']);
    }
    return { t: 'geo', w: 250, dots: false, P: P, line: ['_a,_b', '_c,_d', '_e,_f'], ang: ang, txt: txt.concat([[7.2, 3.35, 'm', 11], [7.2, 0.35, 'n', 11], [5.3, 4.55, 't', 11]]), par: [['_m1', '_m2', 1], ['_n1', '_n2', 1]], cap: cap };
  }

  /* ---------- Unit 1 · Foundations of Geometry ---------- */
  N['U1-L1'] = [{
    h: 'Points, lines, planes, segments and rays',
    big: 'A {{point}} is a location. A {{line}} is straight and goes on forever in both directions (no endpoints). A {{segment}} is part of a line with {{two}} endpoints; a {{ray}} has {{one}} endpoint and goes on forever in one direction. Points on the same line are {{collinear}}.',
    steps: ['Name a line with two points on it: ⟨\\overleftrightarrow{AB}⟩.', 'Name a segment by its endpoints: ⟨\\overline{AB}⟩; a ray starting at A: ⟨\\overrightarrow{AB}⟩.', 'A postulate is accepted without proof: through any two points there is exactly {{one}} line.'],
    figs: [{ t: 'geo', w: 240, P: { A: [0, 3], B: [3, 3], C: [0, 1.5], D: [3, 1.5], E: [0, 0], F: [3, 0] }, line: ['AB'], seg: ['CD'], ray: ['EF'], txt: [[4.3, 3, '{{line AB}}', 10, null, 'start'], [4.3, 1.5, '{{segment CD}}', 10, null, 'start'], [4.3, 0, '{{ray EF}}', 10, null, 'start']], loff: { A: [-8, 4], B: [8, -6], C: [-8, 4], D: [8, 4], E: [-8, 4], F: [6, -6] } }]
  }];
  N['U1-L2'] = [{
    h: 'Segment addition and midpoints',
    big: 'If B is between A and C, the two parts add to the whole: ⟨AB + BC = {{AC}}⟩. A {{midpoint}} splits a segment into two {{congruent}} parts, so each part is half the whole.',
    steps: ['Write the equation from the picture: part + part = whole.', 'Midpoint: set the two parts equal: ⟨3x + 1 = 5x - 7⟩, ⟨x = {{4}}⟩.', 'Substitute back to find the lengths: each part ⟨= {{13}}⟩, whole ⟨= {{26}}⟩.'],
    figs: [{ t: 'geo', w: 270, P: { A: [0, 0], B: [4, 0], C: [10, 0] }, seg: ['AB', 'BC'], slab: [['A', 'B', '4', 1], ['B', 'C', '6', 1], ['A', 'C', '{{AC = 10}}', -1, 14]], cap: '⟨AB + BC = AC⟩' },
      { t: 'geo', w: 270, P: { A: [0, 0], M: [5, 0], B: [10, 0] }, seg: ['AM', 'MB'], tick: [['A', 'M', 1], ['M', 'B', 1]], slab: [['A', 'M', '3x + 1', 1], ['M', 'B', '5x − 7', 1]], cap: 'M is the midpoint: the tick marks show ⟨AM = MB⟩' }]
  }];
  N['U1-L3'] = [{
    h: 'Angles and angle bisectors',
    big: 'An angle is two rays with a common endpoint, the {{vertex}}. If point D is inside ∠ABC, the two smaller angles add to the whole: ⟨m\\angle ABD + m\\angle DBC = {{m\\angle ABC}}⟩. An {{angle bisector}} splits an angle into two equal angles.',
    steps: ['Acute < 90°, right = 90°, obtuse between 90° and 180°, straight = 180°.', 'Part + part = whole: ⟨35° + 50° = {{85°}}⟩.', 'Bisector: each half is ⟨\\frac{1}{2}⟩ of the whole angle.'],
    figs: [{ t: 'geo', w: 220, P: { B: [0, 0], A: pol(4, 0), D: pol(4, 35), C: pol(4, 85) }, ray: ['BA', 'BD', 'BC'], ang: [['A', 'B', 'D', '35°', 1, '#1f5fbf', 22], ['D', 'B', 'C', '50°', 1, '#c0561b', 30]], cap: '⟨m\\angle ABC = 35° + 50° = {{85°}}⟩' }]
  }];
  N['U1-L4'] = [{
    h: 'Midpoint and distance on the coordinate plane',
    big: 'The {{midpoint}} is the average of the coordinates: ⟨M = \\left(\\frac{x_1 + x_2}{2}, \\frac{y_1 + y_2}{2}\\right)⟩. The {{distance}} uses the Pythagorean theorem on the horizontal and vertical changes: ⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩.',
    steps: ['⟨A(1, 1)⟩ and ⟨B(7, 9)⟩: ⟨M = \\left(\\frac{1+7}{2}, \\frac{1+9}{2}\\right) = ({{4, 5}})⟩.', 'Changes: ⟨\\Delta x = 6⟩, ⟨\\Delta y = 8⟩.', '⟨d = \\sqrt{36 + 64} = \\sqrt{100} = {{10}}⟩.'],
    figs: [{ t: 'plane', x: [-1, 9], y: [-1, 10], segs: [[1, 1, 7, 9, false, '#1f5fbf'], [1, 1, 7, 1, true], [7, 1, 7, 9, true]], pts: [[1, 1, 'A(1, 1)', null, null, -4, 13], [7, 9, 'B(7, 9)', null, null, -6, -5], [4, 5, '{{M(4, 5)}}', null, '#c0561b', -6, -5]], txt: [[4, 0.3, 'Δx = 6', 10], [8.1, 5, '{{Δy = 8}}', 10]], cap: 'Distance ⟨AB = {{10}}⟩' }]
  }];
  N['U1-L5'] = [{
    h: 'Multi-step coordinate problems',
    big: 'A coordinate investigation is a {{chain}} of small steps: find a midpoint or a distance, {{check}} it, then use it in the next part. Draw and label the figure first.',
    steps: ['Plot every given point and label it.', 'Write the formula before substituting.', 'Use an earlier answer only after checking it (e.g., ⟨AM = MB⟩ for a midpoint).', 'Reverse midpoint: if M is the midpoint of ⟨\\overline{AB}⟩, then ⟨B = (2M_x - A_x, 2M_y - A_y)⟩. ⟨A(1, 2)⟩, ⟨M(4, 3)⟩ → ⟨B = ({{7, 4}})⟩.'],
    figs: [{ t: 'plane', x: [-1, 8], y: [-1, 6], segs: [[1, 2, 7, 4, false, '#1f5fbf']], pts: [[1, 2, 'A(1, 2)', null, null, -4, 13], [4, 3, 'M(4, 3)', null, '#c0561b', -4, -6], [7, 4, '{{B(7, 4)}}', null, null, -10, -7]], vec: [[1, 2, 4, 2, '#888'], [4, 2, 4, 3, '#888'], [4, 3, 7, 3, '#888'], [7, 3, 7, 4, '#888']], cap: 'Same move from A to M and from M to B: right 3, up 1' }]
  }];
  N['U1-L6'] = [{
    h: 'Conditional statements',
    big: 'A {{conditional}} is an if–then statement: “If ⟨p⟩, then ⟨q⟩.” The part after “if” is the {{hypothesis}}; the part after “then” is the {{conclusion}}. A conditional is true only if it is always true: one {{counterexample}} proves it false.',
    steps: ['Conditional: If an angle measures 30°, then it is acute. ({{true}})', 'Converse (switch the parts): If an angle is acute, then it measures 30°. ({{false}}: a 50° angle is a counterexample.)', 'A counterexample makes the hypothesis {{true}} and the conclusion {{false}}.'],
    figs: [{ t: 'tbl', head: ['Statement', 'Form', 'True?'], rows: [['Conditional', 'If ⟨p⟩, then ⟨q⟩.', 'given'], ['Converse', '{{If ⟨q⟩, then ⟨p⟩.}}', 'check it'], ['Counterexample', '⟨p⟩ true but ⟨q⟩ false', 'shows false']] }]
  }];
  /* ---------- Unit 2 · Angles and Parallel Lines ---------- */
  N['U2-L1'] = [{
    h: 'Complementary and supplementary angles',
    big: '{{Complementary}} angles add to {{90°}}. {{Supplementary}} angles add to {{180°}}. They can be adjacent (sharing a side) or separate.',
    steps: ['Complement of 35°: ⟨90° - 35° = {{55°}}⟩.', 'Supplement of 35°: ⟨180° - 35° = {{145°}}⟩.', 'With algebra: ⟨(2x + 10) + (x + 20) = 90⟩, ⟨x = {{20}}⟩.'],
    figs: [{ t: 'geo', w: 150, P: { B: [0, 0], A: pol(4, 0), D: pol(4, 35), C: pol(4, 90) }, ray: ['BA', 'BD', 'BC'], right: [], ang: [['A', 'B', 'D', '35°', 1, '#1f5fbf', 24], ['D', 'B', 'C', '{{55°}}', 1, '#c0561b', 30]], hide: ['A', 'B', 'C', 'D'], cap: 'Complementary: sum 90°' },
      { t: 'geo', w: 190, P: { B: [0, 0], A: pol(4, 0), D: pol(4, 35), C: pol(4, 180) }, ray: ['BA', 'BD', 'BC'], ang: [['A', 'B', 'D', '35°', 1, '#1f5fbf', 24], ['D', 'B', 'C', '{{145°}}', 1, '#c0561b', 20]], hide: ['A', 'B', 'C', 'D'], cap: 'Supplementary: sum 180°' }]
  }];
  N['U2-L2'] = [{
    h: 'Vertical angles and linear pairs',
    big: 'When two lines cross they make two pairs of {{vertical angles}} (opposite each other), and vertical angles are {{equal}}. Two adjacent angles that form a straight line are a {{linear pair}} and add to {{180°}}.',
    steps: ['Find the pair: across from each other → vertical (equal). Side by side on a line → linear pair (sum 180°).', 'If one angle is 60°: its vertical angle is {{60°}} and each angle in a linear pair with it is {{120°}}.'],
    figs: [{ t: 'geo', w: 230, dots: false, P: { O: [0, 0], A: pol(3.4, 30), B: pol(3.4, 210), C: pol(3.4, 150), D: pol(3.4, 330) }, line: ['BA', 'DC'], ang: [['D', 'O', 'A', '60°', 1, '#1f5fbf', 18], ['C', 'O', 'B', '{{60°}}', 1, '#1f5fbf', 18], ['A', 'O', 'C', '{{120°}}', 2, '#c0561b', 14]], hide: ['A', 'B', 'C', 'D', 'O'], cap: 'Vertical angles: 60° and 60°. Linear pair: 60° + 120° = 180°' }]
  }];
  N['U2-L3'] = [{
    h: 'Corresponding angles',
    big: 'A {{transversal}} crosses two lines. {{Corresponding}} angles are in the same position at each crossing (both upper-right, both lower-left…). When the lines are {{parallel}}, corresponding angles are {{equal}}.',
    steps: ['Find the crossing points and match the positions.', 'Pairs here: 1 & 5, 2 & 6, 3 & 7, 4 & 8.', 'Use it only when the lines are marked or stated parallel.'],
    figs: [transversal({ 2: '{{2}}', 6: '{{6}}' }, '⟨m \\parallel n⟩: ⟨\\angle 2⟩ and ⟨\\angle 6⟩ are corresponding, so ⟨m\\angle 2 = {{m\\angle 6}}⟩')]
  }];
  N['U2-L4'] = [{
    h: 'Alternate interior and alternate exterior angles',
    big: '{{Interior}} angles are between the two lines; {{exterior}} angles are outside them. “Alternate” means on {{opposite}} sides of the transversal. With parallel lines, alternate interior angles are equal and alternate exterior angles are equal.',
    steps: ['Alternate interior: 3 & 6, 4 & 5.', 'Alternate exterior: 1 & 8, 2 & 7.', 'Equal angles → set the expressions equal.'],
    figs: [transversal({ 4: '4', 5: '5', 1: '1', 8: '8' }, 'Alternate interior: ⟨\\angle 4 = \\angle 5⟩ (blue). Alternate exterior: ⟨\\angle 1 = \\angle 8⟩ (orange)', { 1: '#c0561b', 8: '#c0561b' })]
  }];
  N['U2-L5'] = [{
    h: 'Same-side interior angles',
    big: '{{Same-side interior}} angles are between the lines and on the {{same}} side of the transversal (3 & 5, 4 & 6). With parallel lines they are {{supplementary}}: they add to 180°.',
    steps: ['Name the pair first.', 'Corresponding, alternate interior, alternate exterior → {{equal}}.', 'Same-side interior → {{add to 180°}}: if ⟨m\\angle 4 = 124°⟩ then ⟨m\\angle 6 = {{56°}}⟩.'],
    figs: [transversal({ 4: '124°', 6: '{{56°}}' }, '⟨\\angle 4⟩ and ⟨\\angle 6⟩: same side, between the lines', { 6: '#c0561b' })]
  }];
  N['U2-L6'] = [{
    h: 'Proving lines are parallel',
    big: 'The {{converses}} work backward: if a transversal makes corresponding angles equal, alternate interior angles equal, alternate exterior angles equal, or same-side interior angles {{supplementary}}, then the lines are {{parallel}}.',
    steps: ['Identify the angle pair.', 'Show the needed relationship with the given measures (equal, or sum 180°).', 'Conclude ⟨m \\parallel n⟩ and name the converse you used.', 'Example: ⟨m\\angle 3 = 56°⟩ and ⟨m\\angle 6 = 56°⟩ are alternate interior, so ⟨m \\parallel n⟩ by the {{Converse of the Alternate Interior Angles Theorem}}.'],
    figs: [transversal({ 3: '56°', 6: '56°' }, 'Equal alternate interior angles → {{the lines are parallel}}')]
  }];
  N['U2-L7'] = [{
    h: 'Writing equations from angle pairs',
    big: 'Step 1: {{name the relationship}}. Step 2: write an equation — equal pairs: set the expressions {{equal}}; supplementary pairs: add them and set the sum to {{180}}. Step 3: solve for ⟨x⟩, then {{substitute}} to find the angle.',
    steps: ['Corresponding angles ⟨(3x + 10)°⟩ and ⟨(5x - 30)°⟩: ⟨3x + 10 = 5x - 30⟩, ⟨x = {{20}}⟩.', 'Angle: ⟨3(20) + 10 = {{70°}}⟩. Check: ⟨5(20) - 30 = 70°⟩ ✓'],
    figs: [transversal({ 2: '2', 6: '6' }, '⟨m\\angle 2 = (3x + 10)°⟩ and ⟨m\\angle 6 = (5x - 30)°⟩ are corresponding, so they are {{equal}}')]
  }];
  /* ---------- Unit 3 · Congruent Triangles ---------- */
  var TRI1 = { A: [0, 0], B: [4, 0], C: pol(3.686, 50) }, TRI2 = { D: [6, 0], E: [10, 0], F: pol(3.686, 50, [6, 0]) };
  function two(extra) { var P = {}; for (var k in TRI1) P[k] = TRI1[k]; for (k in TRI2) P[k] = TRI2[k]; var s = { t: 'geo', w: 300, P: P, poly: [['A', 'B', 'C'], ['D', 'E', 'F']] }; for (k in extra) s[k] = extra[k]; return s; }
  N['U3-L1'] = [{
    h: 'Congruent figures',
    big: '{{Congruent}} figures have the same size and shape: every pair of {{corresponding}} sides and angles is equal. In ⟨\\triangle ABC \\cong \\triangle DEF⟩ the letters match in {{order}}: A↔D, B↔E, C↔F.',
    steps: ['Read the statement letter by letter: ⟨\\angle B \\cong {{\\angle E}}⟩.', 'Sides use pairs of letters: ⟨\\overline{AC} \\cong {{\\overline{DF}}}⟩.', 'Match by the statement or the marks, not by how the picture looks.'],
    figs: [two({ tick: [['A', 'B', 1], ['D', 'E', 1], ['B', 'C', 2], ['E', 'F', 2], ['A', 'C', 3], ['D', 'F', 3]], ang: [['C', 'B', 'A', '', 1, '#1f5fbf', 14], ['F', 'E', 'D', '', 1, '#1f5fbf', 14]], cap: '⟨\\triangle ABC \\cong \\triangle DEF⟩: matching marks show the corresponding parts' })]
  }];
  N['U3-L2'] = [{
    h: 'Third Angle Theorem and perimeter',
    big: 'The angles of a triangle add to {{180°}}. So if two angles of one triangle equal two angles of another, the {{third}} angles are equal too. Congruent triangles have {{equal}} perimeters.',
    steps: ['⟨m\\angle C = 180° - 50° - 60° = {{70°}}⟩, so ⟨m\\angle F = 70°⟩ as well.', 'Perimeter = sum of the three sides; corresponding sides are equal, so the perimeters match.'],
    figs: [two({ ang: [['B', 'A', 'C', '50°', 1, '#1f5fbf', 16], ['C', 'B', 'A', '60°', 1, '#1f5fbf', 16], ['A', 'C', 'B', '{{70°}}', 1, '#c0561b', 14], ['E', 'D', 'F', '50°', 1, '#1f5fbf', 16], ['F', 'E', 'D', '60°', 1, '#1f5fbf', 16], ['D', 'F', 'E', '{{70°}}', 1, '#c0561b', 14]], cap: 'Corresponding angles 50°, 60°, 70°' })]
  }];
  N['U3-L3'] = [{
    h: 'SSS and SAS',
    big: '{{SSS}}: if all three pairs of sides are equal, the triangles are congruent. {{SAS}}: two pairs of sides and the {{included}} angle (the angle {{between}} those sides) are equal.',
    steps: ['Mark what is given (ticks for sides, arcs for angles).', 'Look for a shared side (reflexive property) or vertical angles.', 'For SAS, check that the angle is between the two sides.'],
    figs: [two({ tick: [['A', 'B', 1], ['D', 'E', 1], ['A', 'C', 2], ['D', 'F', 2]], ang: [['B', 'A', 'C', '', 1, '#1f5fbf', 14], ['E', 'D', 'F', '', 1, '#1f5fbf', 14]], cap: 'SAS: the marked angle is {{between}} the two marked sides' })]
  }];
  N['U3-L4'] = [{
    h: 'ASA and AAS',
    big: '{{ASA}}: two angles and the side {{between}} them. {{AAS}}: two angles and a side that is {{not}} between them. Both prove congruence.',
    steps: ['Mark the two equal angles in each triangle.', 'Is the equal side between them? Yes → ASA. No → AAS.'],
    figs: [two({ tick: [['A', 'B', 1], ['D', 'E', 1]], ang: [['B', 'A', 'C', '', 1, '#1f5fbf', 14], ['E', 'D', 'F', '', 1, '#1f5fbf', 14], ['C', 'B', 'A', '', 2, '#c0561b', 12], ['F', 'E', 'D', '', 2, '#c0561b', 12]], cap: '{{ASA}}: side ⟨\\overline{AB}⟩ is between ⟨\\angle A⟩ and ⟨\\angle B⟩' })]
  }];
  N['U3-L5'] = [{
    h: 'HL, and choosing a criterion',
    big: '{{HL}} works only for {{right}} triangles: equal hypotenuses and one pair of equal legs. The five valid criteria are SSS, SAS, ASA, AAS and HL. {{SSA}} and {{AAA}} do not prove congruence.',
    steps: ['Mark everything given and anything from the diagram.', 'Match the marks to a criterion; check the order (included or not).', 'If only AAA or SSA is available, the triangles are not proven congruent.'],
    figs: [{ t: 'geo', w: 280, P: { A: [0, 0], B: [3, 0], C: [0, 2.4], D: [5, 0], E: [8, 0], F: [5, 2.4] }, poly: [['A', 'B', 'C'], ['D', 'E', 'F']], right: [['B', 'A', 'C'], ['E', 'D', 'F']], tick: [['B', 'C', 2], ['E', 'F', 2], ['A', 'C', 1], ['D', 'F', 1]], cap: 'HL: hypotenuse and a leg' }]
  }];
  N['U3-L6'] = [{
    h: 'Writing a congruence proof',
    big: 'A proof is a chain of {{statements}}, each with a {{reason}} (given, a definition, a postulate or a theorem). Prove the triangles congruent first; then {{CPCTC}} gives any other matching parts.',
    steps: ['Start with the given facts.', 'Add facts from the diagram: a shared side (reflexive property), vertical angles, right angles.', 'State the criterion (SSS, SAS, ASA, AAS, HL).', 'Use CPCTC last.'],
    figs: [{ t: 'tbl', head: ['Statement', 'Reason'], rows: [['⟨\\overline{AB} \\cong \\overline{CB}⟩, ⟨\\overline{AD} \\cong \\overline{CD}⟩', 'Given'], ['⟨\\overline{BD} \\cong \\overline{BD}⟩', '{{Reflexive property}}'], ['⟨\\triangle ABD \\cong \\triangle CBD⟩', '{{SSS}}'], ['⟨\\angle A \\cong \\angle C⟩', '{{CPCTC}}']] },
      { t: 'geo', w: 190, P: { B: [2, 3], A: [0, 0], D: [2, -0.6], C: [4, 0] }, poly: [['A', 'B', 'C', 'D']], seg: ['BD'], tick: [['A', 'B', 1], ['C', 'B', 1], ['A', 'D', 2], ['C', 'D', 2]] }]
  }];
  N['U3-L7'] = [{
    h: 'Using CPCTC',
    big: '{{CPCTC}} means “corresponding parts of congruent triangles are congruent.” It can be used only {{after}} the triangles have been proven congruent. Then any matching side or angle is equal, and you can solve for unknowns.',
    steps: ['Prove ⟨\\triangle ABC \\cong \\triangle DEF⟩ (SSS, SAS, ASA, AAS or HL).', 'Match the parts with the letter order.', 'Set the matching expressions equal: ⟨BC = 2x + 3⟩ and ⟨EF = 15⟩ gives ⟨x = {{6}}⟩.'],
    figs: []
  }];
  /* ---------- Unit 4 · Triangle Relationships ---------- */
  N['U4-L1'] = [{
    h: 'Interior and exterior angles',
    big: 'The three interior angles of a triangle add to {{180°}}. An {{exterior angle}} is formed by extending a side; it equals the sum of the two {{remote}} (non-adjacent) interior angles.',
    steps: ['Missing interior angle: ⟨180° - 50° - 70° = {{60°}}⟩.', 'Exterior angle at C: ⟨50° + 70° = {{120°}}⟩ (also ⟨180° - 60°⟩).'],
    figs: [{ t: 'geo', w: 250, P: { A: [0, 0], B: [5, 0], C: pol(4.076, 60), E: pol(5.676, 60) }, poly: [['A', 'B', 'C']], ray: ['CE'], hide: ['E'],
      ang: [['B', 'A', 'C', '{{60°}}', 1, '#1f5fbf', 16], ['C', 'B', 'A', '50°', 1, '#1f5fbf', 16], ['A', 'C', 'B', '70°', 1, '#1f5fbf', 14], ['B', 'C', 'E', '{{110°}}', 1, '#c0561b', 14]], cap: 'Exterior angle at C = ⟨60° + 50° = {{110°}}⟩' }]
  }];
  N['U4-L2'] = [{
    h: 'Isosceles triangles',
    big: 'An isosceles triangle has two equal sides (the {{legs}}). The angles opposite them, the {{base angles}}, are {{equal}}. The third angle is the vertex angle.',
    steps: ['Vertex angle 40°: base angles ⟨\\frac{180° - 40°}{2} = {{70°}}⟩ each.', 'Base angle 65°: vertex angle ⟨180° - 2(65°) = {{50°}}⟩.'],
    figs: [{ t: 'geo', w: 180, P: { A: [0, 0], B: [4, 0], C: [2, 2 * Math.tan(70 * Math.PI / 180)] }, poly: [['A', 'B', 'C']], tick: [['A', 'C', 1], ['B', 'C', 1]], ang: [['B', 'A', 'C', '{{70°}}', 1, '#1f5fbf', 16], ['C', 'B', 'A', '{{70°}}', 1, '#1f5fbf', 16], ['A', 'C', 'B', '40°', 1, '#c0561b', 18]], cap: 'Equal legs → equal base angles' }]
  }];
  N['U4-L3'] = [{
    h: 'Triangle inequality; side–angle order',
    big: 'Any two sides of a triangle must add to {{more than}} the third side. For sides ⟨a⟩ and ⟨b⟩, the third side is between ⟨|a - b|⟩ and ⟨a + b⟩. The {{longest}} side is opposite the {{largest}} angle.',
    steps: ['Can 4, 6, 11 be a triangle? ⟨4 + 6 = 10 < 11⟩ → {{no}}.', 'Sides 5 and 9: third side ⟨4 < x < {{14}}⟩.', 'Order the sides by the angles opposite them.'],
    figs: [{ t: 'geo', w: 230, P: { A: [0, 0], B: [6, 0], C: [1.5, 2.6] }, poly: [['A', 'B', 'C']], ang: [['A', 'C', 'B', 'largest', 1, '#c0561b', 14]], slab: [['A', 'B', '{{longest side}}', -1]], cap: 'The longest side is across from the largest angle' }]
  }];
  N['U4-L4'] = [{
    h: 'Midsegments',
    big: 'A {{midsegment}} joins the midpoints of two sides of a triangle. It is {{parallel}} to the third side and {{half}} as long.',
    steps: ['Third side 18 → midsegment ⟨= {{9}}⟩.', 'Midsegment ⟨2x + 1⟩, third side ⟨6x - 4⟩: ⟨2(2x + 1) = 6x - 4⟩, ⟨x = {{3}}⟩.'],
    figs: [{ t: 'geo', w: 230, P: { A: [0, 0], B: [6, 0], C: [2, 3.6], M: [1, 1.8], N: [4, 1.8] }, poly: [['A', 'B', 'C']], seg: ['MN:blue'], tick: [['A', 'M', 1], ['M', 'C', 1], ['C', 'N', 2], ['N', 'B', 2]], par: [['M', 'N', 1], ['A', 'B', 1]], slab: [['A', 'B', '18', -1], ['M', 'N', '{{9}}', 1, 9, '#1f5fbf']], cap: '⟨MN = \\frac{1}{2}AB⟩ and ⟨\\overline{MN} \\parallel \\overline{AB}⟩' }]
  }];
  N['U4-L5'] = [{
    h: 'Medians and the centroid',
    big: 'A {{median}} goes from a vertex to the {{midpoint}} of the opposite side. The three medians meet at the {{centroid}}, which divides each median in a {{2 : 1}} ratio: the longer part is next to the vertex.',
    steps: ['The vertex-to-centroid part is ⟨\\frac{2}{3}⟩ of the median.', 'Median 18 → ⟨AG = {{12}}⟩ and ⟨GM = {{6}}⟩.'],
    figs: [{ t: 'geo', w: 230, P: { A: [0, 0], B: [6, 0], C: [2, 4.5], M: [4, 2.25], N: [1, 2.25], L: [3, 0], G: [8 / 3, 1.5] }, poly: [['A', 'B', 'C']], seg: ['AM:blue', 'BN', 'CL'], loff: { G: [10, 12] }, cap: '⟨AG : GM = {{2 : 1}}⟩' }]
  }];
  N['U4-L6'] = [{
    h: 'Perpendicular bisectors and altitudes',
    big: 'A {{perpendicular bisector}} crosses a segment at its midpoint at 90°; every point on it is {{equally far}} from the segment’s endpoints. An {{altitude}} goes from a vertex perpendicular to the opposite side (not necessarily to its midpoint); it is the height in ⟨A = \\frac{1}{2}bh⟩.',
    steps: ['Point P on the perpendicular bisector of ⟨\\overline{AB}⟩: ⟨PA = {{PB}}⟩.', 'Area with base 10 and altitude 6: ⟨\\frac{1}{2}(10)(6) = {{30}}⟩.'],
    figs: [{ t: 'geo', w: 170, P: { A: [0, 0], B: [4, 0], M: [2, 0], P: [2, 3], _u: [2, 3.6], _d: [2, -0.6] }, seg: ['AB', 'PA:dash', 'PB:dash', '_u,_d:blue'], right: [['B', 'M', 'P']], tick: [['A', 'M', 1], ['M', 'B', 1], ['P', 'A', 2], ['P', 'B', 2]], cap: '⟨PA = PB⟩' },
      { t: 'geo', w: 190, P: { A: [0, 0], B: [5, 0], C: [1.5, 3], H: [1.5, 0] }, poly: [['A', 'B', 'C']], seg: ['CH:dash'], right: [['B', 'H', 'C']], slab: [['C', 'H', '{{h}}', 1, 9]], cap: 'Altitude: perpendicular to the base' }]
  }];
  N['U4-L7'] = [{
    h: 'Combining triangle relationships',
    big: 'Multi-part triangle problems link the facts from this unit: midsegments (half and parallel), the centroid (2 : 1), isosceles base angles, the angle sum (180°) and the triangle inequality. Plan the {{chain}} of facts before calculating.',
    steps: ['Mark every given fact on the diagram.', 'List which theorem connects each given to the next unknown.', 'Solve in order and check each answer before the next part.'],
    figs: [{ t: 'tbl', head: ['If you see…', 'Use…'], rows: [['midpoints of two sides', '{{midsegment: half, parallel}}'], ['medians meeting', '{{centroid: 2 : 1}}'], ['two equal sides', '{{equal base angles}}'], ['three side lengths', '{{triangle inequality}}']] }]
  }];
  /* ---------- Unit 5 · Similarity ---------- */
  var SM = { A: [0, 0], B: [3, 0], C: [0.9, 1.8] }, LG = { D: [4.5, 0], E: [9, 0], F: [5.85, 2.7] };
  function sim(extra) { var P = {}; for (var k in SM) P[k] = SM[k]; for (k in LG) P[k] = LG[k]; var s = { t: 'geo', w: 300, P: P, poly: [['A', 'B', 'C'], ['D', 'E', 'F']] }; for (k in extra) s[k] = extra[k]; return s; }
  N['U5-L1'] = [{
    h: 'Similar figures',
    big: '{{Similar}} figures have the same shape: corresponding angles are {{equal}} and corresponding sides are {{proportional}}. In ⟨\\triangle ABC \\sim \\triangle DEF⟩ the letters match in order.',
    steps: ['Match sides that are opposite equal angles.', 'Write a proportion with the same triangle on top: ⟨\\frac{AB}{DE} = \\frac{BC}{EF}⟩.', '⟨\\frac{6}{9} = \\frac{4}{x}⟩, ⟨6x = 36⟩, ⟨x = {{6}}⟩.'],
    figs: [sim({ slab: [['A', 'B', '6', -1], ['D', 'E', '9', -1], ['B', 'C', '4', 1], ['E', 'F', '{{x = 6}}', 1]], ang: [['B', 'A', 'C', '', 1, '#1f5fbf', 12], ['E', 'D', 'F', '', 1, '#1f5fbf', 12]], cap: '⟨\\triangle ABC \\sim \\triangle DEF⟩ (scale factor 1.5)' })]
  }];
  N['U5-L2'] = [{
    h: 'Scale factor and dilations',
    big: 'A {{dilation}} makes a similar copy. The {{scale factor}} is ⟨\\frac{\\text{image length}}{\\text{original length}}⟩: greater than 1 {{enlarges}}, between 0 and 1 {{shrinks}}.',
    steps: ['Original side 4, image side 10: scale factor ⟨\\frac{10}{4} = {{2.5}}⟩.', 'Multiply every original length by the scale factor to get the image.'],
    figs: [{ t: 'plane', x: [-1, 9], y: [-1, 7], polys: [{ pts: [[0, 0], [2, 0], [0, 2]] }, { pts: [[0, 0], [6, 0], [0, 6]], fill: 'rgba(192,86,27,.10)', c: '#c0561b', dash: true }], segs: [[0, 0, 6, 0, false, '#c0561b']], txt: [[0.6, 0.35, '2', 10], [3.6, 0.35, '{{6}}', 10, '#c0561b'], [3.9, 3.6, 'image', 10, '#c0561b']], cap: 'Dilation with center ⟨(0, 0)⟩ and scale factor {{3}}' }]
  }];
  N['U5-L3'] = [{
    h: 'Perimeters of similar figures',
    big: 'If two figures are similar with scale factor ⟨k⟩, their perimeters are in the {{same ratio}} ⟨k⟩. (Areas are in the ratio ⟨k^2⟩ — not used for perimeter.)',
    steps: ['Scale factor ⟨\\frac{9}{6} = 1.5⟩.', 'Small perimeter 20 → large perimeter ⟨20 \\times 1.5 = {{30}}⟩.'],
    figs: [sim({ slab: [['A', 'B', '6', -1], ['D', 'E', '9', -1]], cap: 'Perimeter ratio = side ratio = {{3 : 2}}' })]
  }];
  N['U5-L4'] = [{
    h: 'AA similarity',
    big: 'If two angles of one triangle are equal to two angles of another, the triangles are {{similar}} (the third angles must match too, because the sum is 180°). Look for {{vertical angles}}, shared angles and parallel lines.',
    steps: ['Find two pairs of equal angles.', 'Write the similarity statement in matching order.', 'Then use proportions for missing sides.'],
    figs: [sim({ ang: [['B', 'A', 'C', '40°', 1, '#1f5fbf', 14], ['E', 'D', 'F', '40°', 1, '#1f5fbf', 14], ['C', 'B', 'A', '60°', 2, '#c0561b', 12], ['F', 'E', 'D', '60°', 2, '#c0561b', 12]], cap: 'Two pairs of equal angles → ⟨\\triangle ABC \\sim {{\\triangle DEF}}⟩. Not drawn to scale' })]
  }];
  N['U5-L5'] = [{
    h: 'SSS and SAS similarity',
    big: '{{SSS similarity}}: all three pairs of sides have the {{same ratio}}. {{SAS similarity}}: two pairs of sides have the same ratio and the {{included angles}} are equal. Sides must be proportional, not equal.',
    steps: ['Order each triangle’s sides from shortest to longest.', 'Divide matching sides: ⟨\\frac{4}{6}, \\frac{6}{9}, \\frac{8}{12}⟩ all ⟨= {{\\frac{2}{3}}}⟩ → similar by SSS.'],
    figs: [{ t: 'tbl', head: ['Small', 'Large', 'Ratio'], rows: [['4', '6', '{{⟨\\frac{2}{3}⟩}}'], ['6', '9', '{{⟨\\frac{2}{3}⟩}}'], ['8', '12', '{{⟨\\frac{2}{3}⟩}}']] }]
  }];
  N['U5-L6'] = [{
    h: 'The Triangle Proportionality Theorem',
    big: 'If a line is {{parallel}} to one side of a triangle, it cuts the other two sides {{proportionally}}: ⟨\\frac{AD}{DB} = \\frac{AE}{EC}⟩ (part over part on both sides).',
    steps: ['Mark the parallel segment.', 'Write part/part = part/part in the same order: ⟨\\frac{4}{6} = \\frac{5}{x}⟩.', '⟨4x = 30⟩, ⟨x = {{7.5}}⟩.'],
    figs: [{ t: 'geo', w: 230, P: { A: [2, 4], B: [0, 0], C: [6, 0], D: [1.2, 2.4], E: [3.6, 2.4] }, poly: [['A', 'B', 'C']], seg: ['DE:blue'], par: [['D', 'E', 1], ['B', 'C', 1]], slab: [['A', 'D', '4', 1], ['D', 'B', '6', 1], ['A', 'E', '5', -1], ['E', 'C', '{{x = 7.5}}', -1]], cap: '⟨\\overline{DE} \\parallel \\overline{BC}⟩. Not drawn to scale' }]
  }];
  N['U5-L7'] = [{
    h: 'Indirect measurement',
    big: 'At the same time of day, sun rays make the same angle with the ground, so an object and its shadow form a triangle {{similar}} to any other object and its shadow. Set up ⟨\\frac{\\text{height}}{\\text{shadow}} = \\frac{\\text{height}}{\\text{shadow}}⟩ with matching {{units}}.',
    steps: ['A 6-ft person casts a 4-ft shadow; a tree casts a 30-ft shadow.', '⟨\\frac{6}{4} = \\frac{h}{30}⟩, ⟨4h = 180⟩, ⟨h = {{45}}⟩ ft.'],
    figs: [{ t: 'geo', w: 280, P: { A: [0, 0], B: [0, 3], C: [2, 0], D: [4, 0], E: [4, 9], F: [10, 0] }, poly: [['A', 'B', 'C'], ['D', 'E', 'F']], right: [['C', 'A', 'B'], ['F', 'D', 'E']], hide: ['A', 'B', 'C', 'D', 'E', 'F'], slab: [['A', 'B', '6', 1], ['A', 'C', '4', -1], ['D', 'E', '{{h = 45}}', 1, 20], ['D', 'F', '30', -1]], cap: 'Person and tree: similar right triangles. Not drawn to scale' }]
  }];
  N['U5-L8'] = [{
    h: 'Similarity investigations',
    big: 'In a complicated figure, {{redraw}} the similar triangles separately, side by side and facing the same way. Label the {{corresponding}} sides, then write the proportion. When a part and a whole are both involved, use the {{whole}} side lengths for the big triangle.',
    steps: ['Identify why the triangles are similar (AA from parallel lines or a shared angle).', 'Draw them separately with all lengths.', 'Write and solve the proportion; check that the answer is reasonable.'],
    figs: [{ t: 'geo', w: 230, P: { A: [2, 4], B: [0, 0], C: [6, 0], D: [1.2, 2.4], E: [3.6, 2.4] }, poly: [['A', 'B', 'C']], seg: ['DE:blue'], par: [['D', 'E', 1], ['B', 'C', 1]], slab: [['D', 'E', '6', 1, 9], ['B', 'C', 'x', -1], ['A', 'D', '4', 1], ['D', 'B', '6', 1]], cap: '⟨\\triangle ADE \\sim \\triangle ABC⟩: ⟨\\frac{4}{10} = \\frac{6}{x}⟩, ⟨x = {{15}}⟩' }]
  }];
  /* ---------- Unit 6 · Right Triangles and Trigonometry ---------- */
  N['U6-L1'] = [{
    h: 'The Pythagorean theorem',
    big: 'In a right triangle with legs ⟨a⟩ and ⟨b⟩ and {{hypotenuse}} ⟨c⟩ (the side across from the right angle, the longest side): ⟨a^2 + b^2 = c^2⟩. For a missing hypotenuse {{add}} the squares; for a missing leg {{subtract}}.',
    steps: ['Legs 6 and 8: ⟨c = \\sqrt{36 + 64} = {{10}}⟩.', 'Hypotenuse 13, leg 5: ⟨b = \\sqrt{169 - 25} = {{12}}⟩.', 'Whole-number sides like 3-4-5 are Pythagorean triples.'],
    figs: [{ t: 'geo', w: 220, P: { A: [0, 0], B: [8, 0], C: [0, 6] }, poly: [['A', 'B', 'C']], right: [['B', 'A', 'C']], slab: [['A', 'B', '8', -1], ['A', 'C', '6', 1], ['C', 'B', '{{c = 10}}', 1]], cap: '⟨6^2 + 8^2 = 10^2⟩' }]
  }];
  N['U6-L2'] = [{
    h: 'Distance with the Pythagorean theorem',
    big: 'To find the distance between two points, draw a {{right triangle}}: the legs are the horizontal change and the vertical change, and the distance is the {{hypotenuse}}.',
    steps: ['⟨(-2, 1)⟩ to ⟨(4, 9)⟩: horizontal change ⟨= 6⟩, vertical change ⟨= 8⟩.', '⟨d = \\sqrt{6^2 + 8^2} = {{10}}⟩.', 'Do not forget the {{square root}} at the end.'],
    figs: [{ t: 'plane', x: [-3, 5], y: [0, 10], segs: [[-2, 1, 4, 9, false, '#1f5fbf'], [-2, 1, 4, 1, true], [4, 1, 4, 9, true]], pts: [[-2, 1, '(−2, 1)', null, null, -2, 13], [4, 9, '(4, 9)', null, null, -6, -5]], txt: [[1, 0.4, '6', 10], [4.5, 5, '8', 10], [0.4, 5.9, '{{10}}', 11, '#1f5fbf']] }]
  }];
  N['U6-L3'] = [{
    h: 'Special right triangles',
    big: 'In a {{45°-45°-90°}} triangle the legs are equal and the hypotenuse is ⟨\\text{leg} \\cdot \\sqrt{2}⟩. In a {{30°-60°-90°}} triangle the hypotenuse is {{twice}} the short leg, and the long leg (opposite 60°) is ⟨\\text{short leg} \\cdot {{\\sqrt{3}}}⟩.',
    steps: ['45-45-90 with leg 5: hypotenuse ⟨= {{5\\sqrt{2}}}⟩.', '30-60-90 with short leg 4: hypotenuse ⟨= {{8}}⟩, long leg ⟨= {{4\\sqrt{3}}}⟩.'],
    figs: [{ t: 'geo', w: 160, P: { A: [0, 0], B: [3, 0], C: [0, 3] }, poly: [['A', 'B', 'C']], right: [['B', 'A', 'C']], hide: ['A', 'B', 'C'], ang: [['C', 'B', 'A', '45°', 1, '#1f5fbf', 18], ['A', 'C', 'B', '45°', 1, '#1f5fbf', 18]], slab: [['A', 'B', 'x', -1], ['A', 'C', 'x', 1], ['C', 'B', '{{x√2}}', 1]] },
      { t: 'geo', w: 190, P: { A: [0, 0], B: [Math.sqrt(3) * 2, 0], C: [0, 2] }, poly: [['A', 'B', 'C']], right: [['B', 'A', 'C']], hide: ['A', 'B', 'C'], ang: [['C', 'B', 'A', '30°', 1, '#1f5fbf', 22], ['A', 'C', 'B', '60°', 1, '#c0561b', 14]], slab: [['A', 'C', 'x', 1], ['A', 'B', '{{x√3}}', -1], ['C', 'B', '{{2x}}', 1]] }]
  }];
  N['U6-L4'] = [{
    h: 'Sine, cosine and tangent',
    big: 'For an acute angle θ in a right triangle, name the sides {{from that angle}}: the {{opposite}} side is across from θ, the {{adjacent}} side touches θ (not the hypotenuse). SOH-CAH-TOA: ⟨\\sin\\theta = \\frac{\\text{opp}}{\\text{hyp}}⟩, ⟨\\cos\\theta = \\frac{\\text{adj}}{\\text{hyp}}⟩, ⟨\\tan\\theta = \\frac{\\text{opp}}{\\text{adj}}⟩.',
    steps: ['Triangle 3-4-5 with θ opposite the side 3:', '⟨\\sin\\theta = \\frac{3}{5}⟩, ⟨\\cos\\theta = {{\\frac{4}{5}}}⟩, ⟨\\tan\\theta = {{\\frac{3}{4}}}⟩.'],
    figs: [{ t: 'geo', w: 250, pad: 48, P: { A: [0, 0], B: [4, 0], C: [4, 3] }, poly: [['A', 'B', 'C']], right: [['A', 'B', 'C']], hide: ['A', 'B', 'C'], ang: [['B', 'A', 'C', 'θ', 1, '#1f5fbf', 22]], slab: [['A', 'B', '{{adjacent 4}}', -1], ['B', 'C', '{{opposite 3}}', -1, 36], ['A', 'C', '{{hypotenuse 5}}', 1, 14]] }]
  }];
  N['U6-L5'] = [{
    h: 'Finding a side with trigonometry',
    big: 'Label the sides from the given angle. Choose the ratio that uses the side you {{know}} and the side you {{want}}. Write the equation and solve: if the unknown is on top, {{multiply}}; if it is on the bottom, divide.',
    steps: ['Angle 35°, hypotenuse 12, want the opposite side: use {{sine}}.', '⟨\\sin 35° = \\frac{x}{12}⟩, ⟨x = 12\\sin 35° \\approx {{6.88}}⟩.', 'Calculator in {{degree}} mode.'],
    figs: [{ t: 'geo', w: 250, pad: 44, P: { A: [0, 0], B: [12 * Math.cos(35 * Math.PI / 180), 0], C: [12 * Math.cos(35 * Math.PI / 180), 12 * Math.sin(35 * Math.PI / 180)] }, poly: [['A', 'B', 'C']], right: [['A', 'B', 'C']], hide: ['A', 'B', 'C'], ang: [['B', 'A', 'C', '35°', 1, '#1f5fbf', 30]], slab: [['A', 'C', '12', 1], ['B', 'C', '{{x ≈ 6.88}}', -1, 30]] }]
  }];
  N['U6-L6'] = [{
    h: 'Finding an angle: inverse trig',
    big: 'When you know two sides and want the {{angle}}, use an {{inverse}} trig function: ⟨\\theta = \\tan^{-1}\\left(\\frac{\\text{opp}}{\\text{adj}}\\right)⟩ (or ⟨\\sin^{-1}⟩, ⟨\\cos^{-1}⟩). It answers “which angle has this ratio?”',
    steps: ['Opposite 5, adjacent 8: ⟨\\tan\\theta = \\frac{5}{8}⟩.', '⟨\\theta = \\tan^{-1}(0.625) \\approx {{32.0°}}⟩.', 'Check: the angle should be smaller than 45° because opp < adj.'],
    figs: [{ t: 'geo', w: 220, P: { A: [0, 0], B: [8, 0], C: [8, 5] }, poly: [['A', 'B', 'C']], right: [['A', 'B', 'C']], hide: ['A', 'B', 'C'], ang: [['B', 'A', 'C', '{{32.0°}}', 1, '#1f5fbf', 32]], slab: [['A', 'B', '8', -1], ['B', 'C', '5', -1]] }]
  }];
  N['U6-L7'] = [{
    h: 'Angles of elevation and depression',
    big: 'Both angles are measured from a {{horizontal}} line. Looking up from the horizontal is an angle of {{elevation}}; looking down is an angle of {{depression}}. The angle of depression from the top equals the angle of elevation from the bottom ({{alternate interior}} angles).',
    steps: ['Draw the horizontal, the line of sight and the right triangle.', 'A ramp: 50 ft from the base, elevation 28°: ⟨h = 50\\tan 28° \\approx {{26.6}}⟩ ft.'],
    figs: [{ t: 'geo', w: 260, dots: false, P: { A: [0, 0], B: [8, 0], C: [8, 4.25], D: [2, 4.25] }, poly: [['A', 'B', 'C']], seg: ['CD:dash'], right: [['A', 'B', 'C']], hide: ['A', 'B', 'C', 'D'], ang: [['B', 'A', 'C', '{{elevation}}', 1, '#1f5fbf', 36, 26], ['D', 'C', 'A', '{{depression}}', 1, '#c0561b', 36, 26]], slab: [['A', 'B', '50 ft', -1], ['B', 'C', 'h', -1]], cap: 'Same angle (28°): alternate interior angles' }]
  }];
  N['U6-L8'] = [{
    h: 'Right-triangle investigations',
    big: 'A survey or investigation problem often has {{two}} right triangles that share a side. Solve the triangle with enough information {{first}}, then use the shared side in the second. Keep full calculator values until the {{end}}.',
    steps: ['Draw one diagram and mark every right angle.', 'Find the shared side from the first triangle.', 'Use it in the second triangle; round only the final answer.'],
    figs: [{ t: 'geo', w: 260, dots: false, P: { A: [0, 0], B: [4, 0], C: [10, 0], D: [10, 5] }, poly: [['A', 'C', 'D']], seg: ['BD'], right: [['A', 'C', 'D']], ang: [['C', 'A', 'D', '25°', 1, '#1f5fbf', 30], ['C', 'B', 'D', '40°', 1, '#c0561b', 20]], slab: [['A', 'B', '40 m', -1], ['C', 'D', '{{h}}', -1]], hide: ['A', 'B', 'C', 'D'], cap: 'Two angles of elevation from two spots. Not drawn to scale' }]
  }];
  N['U6-L9'] = [{
    h: 'Choosing a right-triangle tool',
    big: 'Two sides known, third side wanted → {{Pythagorean theorem}}. An angle and a side known → {{trig ratio}}. Two sides known, angle wanted → {{inverse trig}}. A 30°, 45° or 60° angle → special right triangle (exact answer).',
    steps: ['Draw and label the right triangle.', 'List what is known and what is wanted.', 'Pick the tool from the table and solve.'],
    figs: [{ t: 'tbl', head: ['Know', 'Want', 'Tool'], rows: [['2 sides', 'side', '{{⟨a^2 + b^2 = c^2⟩}}'], ['angle + side', 'side', '{{sin, cos, tan}}'], ['2 sides', 'angle', '{{⟨\\sin^{-1}⟩, ⟨\\cos^{-1}⟩, ⟨\\tan^{-1}⟩}}'], ['30°, 45°, 60°', 'exact side', '{{special triangles}}']] }]
  }];
  /* ---------- Unit 7 · Polygons and Quadrilaterals ---------- */
  N['U7-L1'] = [{
    h: 'Interior angle sum',
    big: 'Diagonals from one vertex split an ⟨n⟩-sided polygon into ⟨n - 2⟩ {{triangles}}, so its interior angles add to ⟨{{(n - 2) \\cdot 180°}}⟩. Each angle of a {{regular}} polygon is that sum ÷ ⟨n⟩.',
    steps: ['Hexagon: ⟨(6 - 2) \\cdot 180° = {{720°}}⟩.', 'Regular hexagon: each angle ⟨720° \\div 6 = {{120°}}⟩.', 'Quadrilateral: ⟨360°⟩.'],
    figs: [{ t: 'geo', w: 190, P: { A: pol(2, 90), B: pol(2, 150), C: pol(2, 210), D: pol(2, 270), E: pol(2, 330), F: pol(2, 30) }, poly: [['A', 'B', 'C', 'D', 'E', 'F']], seg: ['AC:dash', 'AD:dash', 'AE:dash'], hide: ['B', 'C', 'D', 'E', 'F'], cap: 'A hexagon splits into {{4}} triangles' }]
  }];
  N['U7-L2'] = [{
    h: 'Exterior angles; diagonals',
    big: 'The exterior angles of any convex polygon (one at each vertex) add to {{360°}}, no matter how many sides. Each exterior angle of a regular ⟨n⟩-gon is ⟨{{\\frac{360°}{n}}}⟩. A polygon has ⟨\\frac{n(n - 3)}{2}⟩ {{diagonals}}.',
    steps: ['Regular octagon: exterior angle ⟨360° \\div 8 = {{45°}}⟩; interior ⟨180° - 45° = {{135°}}⟩.', 'Exterior angle 24° → ⟨n = 360 \\div 24 = {{15}}⟩ sides.', 'Pentagon diagonals: ⟨\\frac{5 \\cdot 2}{2} = {{5}}⟩.'],
    figs: [{ t: 'geo', w: 200, P: { A: pol(2, 90), B: pol(2, 162), C: pol(2, 234), D: pol(2, 306), E: pol(2, 18), X: pol(1.4, 36, pol(2, 90)) }, poly: [['A', 'B', 'C', 'D', 'E']], seg: ['AX:dash'], ang: [['X', 'A', 'E', '{{72°}}', 1, '#c0561b', 14]], hide: ['B', 'C', 'D', 'E', 'X'], cap: 'Regular pentagon: exterior angle ⟨360° \\div 5⟩' }]
  }];
  N['U7-L3'] = [{
    h: 'Properties of parallelograms',
    big: 'In a parallelogram: opposite sides are {{parallel}} and {{equal}}; opposite angles are {{equal}}; consecutive angles are {{supplementary}} (add to 180°); the diagonals {{bisect}} each other.',
    steps: ['One angle 70° → the opposite angle 70°, each consecutive angle {{110°}}.', 'Diagonal pieces: ⟨AE = EC⟩, so ⟨2x + 1 = 9⟩, ⟨x = {{4}}⟩.'],
    figs: [{ t: 'geo', w: 240, P: { A: [0, 0], B: [5, 0], C: [5 + 2.6 / Math.tan(70 * Math.PI / 180), 2.6], D: [2.6 / Math.tan(70 * Math.PI / 180), 2.6], E: [2.5 + 1.3 / Math.tan(70 * Math.PI / 180), 1.3] }, poly: [['A', 'B', 'C', 'D']], seg: ['AC:dash', 'BD:dash'], tick: [['A', 'B', 1], ['D', 'C', 1], ['A', 'D', 2], ['B', 'C', 2]], ang: [['B', 'A', 'D', '70°', 1, '#1f5fbf', 16], ['D', 'C', 'B', '{{70°}}', 1, '#1f5fbf', 16], ['C', 'B', 'A', '{{110°}}', 2, '#c0561b', 12]], loff: { E: [0, 16] } }]
  }];
  N['U7-L4'] = [{
    h: 'Rectangles, rhombi and squares',
    big: 'They are all parallelograms with extra properties. A {{rectangle}} has four right angles and {{equal}} diagonals. A {{rhombus}} has four equal sides and {{perpendicular}} diagonals that bisect its angles. A {{square}} has all of these.',
    steps: ['Rectangle diagonal pieces are all equal: ⟨AE = BE = CE = DE⟩.', 'Rhombus: diagonals meet at 90°, so use the Pythagorean theorem on the four right triangles.'],
    figs: [{ t: 'geo', w: 170, P: { A: [0, 0], B: [4, 0], C: [4, 2.4], D: [0, 2.4], E: [2, 1.2] }, poly: [['A', 'B', 'C', 'D']], seg: ['AC:dash', 'BD:dash'], right: [['B', 'A', 'D']], hide: ['A', 'B', 'C', 'D', 'E'], tick: [['A', 'E', 1], ['B', 'E', 1], ['C', 'E', 1], ['D', 'E', 1]], cap: 'Rectangle: {{equal}} diagonals' },
      { t: 'geo', w: 170, P: { A: [0, 1.5], B: [2, 0], C: [4, 1.5], D: [2, 3], E: [2, 1.5] }, poly: [['A', 'B', 'C', 'D']], seg: ['AC:dash', 'BD:dash'], right: [['C', 'E', 'D']], hide: ['A', 'B', 'C', 'D', 'E'], tick: [['A', 'B', 1], ['B', 'C', 1], ['C', 'D', 1], ['D', 'A', 1]], cap: 'Rhombus: {{perpendicular}} diagonals' }]
  }];
  N['U7-L5'] = [{
    h: 'Trapezoids',
    big: 'A {{trapezoid}} has exactly one pair of parallel sides, the {{bases}}. Its {{midsegment}} joins the midpoints of the legs; it is parallel to the bases and equals the {{average}} of the bases: ⟨\\frac{b_1 + b_2}{2}⟩.',
    steps: ['Bases 8 and 14: midsegment ⟨\\frac{8 + 14}{2} = {{11}}⟩.', 'Midsegment 15, one base 12: ⟨\\frac{12 + b}{2} = 15⟩, ⟨b = {{18}}⟩.'],
    figs: [{ t: 'geo', w: 240, P: { A: [0, 0], B: [7, 0], C: [5, 3], D: [1, 3], M: [0.5, 1.5], N: [6, 1.5] }, poly: [['A', 'B', 'C', 'D']], seg: ['MN:blue'], par: [['D', 'C', 1], ['A', 'B', 1], ['M', 'N', 1]], hide: ['A', 'B', 'C', 'D', 'M', 'N'], slab: [['D', 'C', '8', 1], ['A', 'B', '14', -1], ['M', 'N', '{{11}}', 1, 9, '#1f5fbf']], cap: 'Midsegment = average of the bases' }]
  }];
  N['U7-L6'] = [{
    h: 'Classifying quadrilaterals',
    big: 'Use the converses to prove a shape. If both pairs of opposite sides are equal, or the diagonals {{bisect each other}}, it is a parallelogram. A parallelogram with a right angle (or equal diagonals) is a {{rectangle}}; with perpendicular diagonals (or four equal sides) a {{rhombus}}; with both, a {{square}}.',
    steps: ['First show it is a parallelogram.', 'Then test the extra property with slopes (perpendicular: product −1) or lengths (distance formula).', 'Name the most specific shape that every test supports.'],
    figs: [{ t: 'tbl', head: ['Shape', 'Must have'], rows: [['Parallelogram', '{{diagonals bisect each other}}'], ['Rectangle', 'parallelogram + {{equal diagonals}}'], ['Rhombus', 'parallelogram + {{perpendicular diagonals}}'], ['Square', '{{rectangle and rhombus}}']] }]
  }];
  /* ---------- Unit 8 · Transformations ---------- */
  var TRI = [[1, 1], [4, 1], [2, 3]];
  function tf(img, cap, extra) { var s = { t: 'plane', x: [-6, 6], y: [-6, 6], numEvery: 2, polys: [{ pts: TRI }, { pts: img, c: '#c0561b', fill: 'rgba(192,86,27,.12)', dash: true }], pts: [[2, 3, 'A', null, null, -4, -6], [img[2][0], img[2][1], '{{A′}}', null, '#c0561b', -4, -6]], cap: cap }; for (var k in extra) s[k] = extra[k]; return s; }
  N['U8-L1'] = [{
    h: 'Translations',
    big: 'A {{translation}} slides every point the same distance in the same direction. The rule ⟨(x, y) \\to (x + a, y + b)⟩ adds ⟨a⟩ to every ⟨x⟩ (right if positive) and ⟨b⟩ to every ⟨y⟩ (up if positive). The image is {{congruent}} to the original.',
    steps: ['⟨(x, y) \\to (x - 5, y - 4)⟩: left 5, down 4.', '⟨A(2, 3) \\to A′({{-3}}, {{-1}})⟩.'],
    figs: [tf(TRI.map(function (p) { return [p[0] - 5, p[1] - 4]; }), '⟨(x, y) \\to (x - 5, y - 4)⟩', { vec: [[2, 3, -3, -1, '#888']] })]
  }];
  N['U8-L2'] = [{
    h: 'Reflections',
    big: 'A {{reflection}} flips a figure over a line; each image point is the {{same distance}} from the line as the original. Over the ⟨x⟩-axis: ⟨(x, y) \\to (x, {{-y}})⟩. Over the ⟨y⟩-axis: ⟨(x, y) \\to ({{-x}}, y)⟩.',
    steps: ['Over the ⟨x⟩-axis, ⟨A(2, 3) \\to A′(2, {{-3}})⟩.', 'Over the ⟨y⟩-axis, ⟨A(2, 3) \\to A′({{-2}}, 3)⟩.'],
    figs: [tf(TRI.map(function (p) { return [p[0], -p[1]]; }), 'Reflection over the ⟨x⟩-axis', { segs: [[2, 3, 2, -3, true, '#888']] })]
  }];
  N['U8-L3'] = [{
    h: 'Rotations about the origin',
    big: 'A {{rotation}} turns a figure about a center. About the origin: 90° counterclockwise ⟨(x, y) \\to ({{-y}}, x)⟩; 90° clockwise ⟨(x, y) \\to (y, {{-x}})⟩; 180° ⟨(x, y) \\to (-x, -y)⟩.',
    steps: ['90° counterclockwise: ⟨A(2, 3) \\to A′({{-3}}, {{2}})⟩.', 'Check with the picture: the segment from the origin to A turns a quarter turn.'],
    figs: [tf(TRI.map(function (p) { return [-p[1], p[0]]; }), '90° counterclockwise about ⟨(0, 0)⟩', { segs: [[0, 0, 2, 3, true, '#888'], [0, 0, -3, 2, true, '#888']] })]
  }];
  N['U8-L4'] = [{
    h: 'Dilations about the origin',
    big: 'A {{dilation}} with center the origin and scale factor ⟨k⟩ multiplies {{both}} coordinates by ⟨k⟩: ⟨(x, y) \\to (kx, ky)⟩. The image is {{similar}}, not congruent (unless ⟨k = 1⟩).',
    steps: ['⟨k = 2⟩: ⟨A(2, 3) \\to A′({{4}}, {{6}})⟩.', '⟨k = \\frac{1}{2}⟩: ⟨(4, 2) \\to ({{2}}, {{1}})⟩.'],
    figs: [{ t: 'plane', x: [-1, 9], y: [-1, 7], polys: [{ pts: TRI }, { pts: TRI.map(function (p) { return [2 * p[0], 2 * p[1]]; }), c: '#c0561b', fill: 'rgba(192,86,27,.12)', dash: true }], segs: [[0, 0, 4, 6, true, '#888']], pts: [[2, 3, 'A(2, 3)', null, null, -6, -4], [4, 6, '{{A′(4, 6)}}', null, '#c0561b', 6, 4]], cap: 'Scale factor 2, center ⟨(0, 0)⟩' }]
  }];
  N['U8-L5'] = [{
    h: 'Compositions',
    big: 'A {{composition}} is one transformation followed by another. Do them in the given {{order}}, writing the middle image ⟨A′⟩ before the final image ⟨A″⟩. Changing the order can change the result.',
    steps: ['Reflect over the ⟨y⟩-axis, then translate ⟨(x, y) \\to (x, y - 4)⟩.', '⟨A(2, 3) \\to A′(-2, 3) \\to A″({{-2}}, {{-1}})⟩.'],
    figs: [{ t: 'plane', x: [-6, 6], y: [-6, 6], numEvery: 2, polys: [{ pts: TRI }, { pts: TRI.map(function (p) { return [-p[0], p[1]]; }), c: '#888', fill: 'rgba(0,0,0,.05)', dash: true }, { pts: TRI.map(function (p) { return [-p[0], p[1] - 4]; }), c: '#c0561b', fill: 'rgba(192,86,27,.12)' }], pts: [[2, 3, 'A'], [-2, 3, 'A′', null, '#666', -6, -6], [-2, -1, '{{A″}}', null, '#c0561b', -6, 12]], cap: 'Reflect, then translate down 4' }]
  }];
  N['U8-L6'] = [{
    h: 'Symmetry',
    big: 'A figure has {{line symmetry}} if a reflection over a line maps it onto itself. It has {{rotational symmetry}} if a rotation of less than 360° maps it onto itself. A regular ⟨n⟩-gon has {{n}} lines of symmetry and rotational symmetry every ⟨{{\\frac{360°}{n}}}⟩.',
    steps: ['Regular hexagon: 6 lines; rotations of 60°, 120°, 180°, … map it onto itself.', 'Count lines through vertices AND lines through midpoints of sides.'],
    figs: [{ t: 'geo', w: 190, dots: false, P: { A: pol(2, 90), B: pol(2, 162), C: pol(2, 234), D: pol(2, 306), E: pol(2, 18), a: pol(2.4, 270), b: pol(2.4, 342), c: pol(2.4, 54), d: pol(2.4, 126), e: pol(2.4, 198), a2: pol(2.4, 90), b2: pol(2.4, 162), c2: pol(2.4, 234), d2: pol(2.4, 306), e2: pol(2.4, 18) }, poly: [['A', 'B', 'C', 'D', 'E']], seg: ['a2,a:dash:blue', 'b2,b:dash:blue', 'c2,c:dash:blue', 'd2,d:dash:blue', 'e2,e:dash:blue'], hide: ['A', 'B', 'C', 'D', 'E', 'a', 'b', 'c', 'd', 'e', 'a2', 'b2', 'c2', 'd2', 'e2'], cap: 'Regular pentagon: {{5}} lines of symmetry; rotation {{72°}}' }]
  }];
  N['U8-L7'] = [{
    h: 'Transformations and congruence',
    big: '{{Rigid motions}} — translations, reflections and rotations — keep lengths and angles, so the image is {{congruent}}. A {{dilation}} keeps angles but multiplies lengths, so the image is only {{similar}}. Two figures are congruent if a sequence of rigid motions maps one onto the other.',
    steps: ['Describe a sequence: e.g., rotate 90° counterclockwise, then translate right 2.', 'If any step is a dilation (scale factor ≠ 1), the figures are similar, not congruent.'],
    figs: [{ t: 'tbl', head: ['Transformation', 'Lengths', 'Angles', 'Result'], rows: [['translation', 'same', 'same', '{{congruent}}'], ['reflection', 'same', 'same', '{{congruent}}'], ['rotation', 'same', 'same', '{{congruent}}'], ['dilation', '{{× k}}', 'same', '{{similar}}']] }]
  }];
  /* ---------- Unit 9 · Circles ---------- */
  var O = [0, 0];
  N['U9-L1'] = [{
    h: 'Parts of a circle',
    big: 'A {{radius}} goes from the center to the circle; a {{diameter}} goes across through the center, so ⟨d = {{2r}}⟩. A {{chord}} joins two points of the circle (the diameter is the longest chord). A {{secant}} is a line through two points of the circle; a {{tangent}} touches it at exactly one point.',
    steps: ['Diameter 18 → radius ⟨= {{9}}⟩.', 'Radius 7 → diameter ⟨= {{14}}⟩.'],
    figs: [{ t: 'geo', w: 240, P: { O: O, A: pol(3, 200), B: pol(3, 20), C: pol(3, 110), D: pol(3, 250), E: pol(3, 320), F: [3, 0], _t1: [3, -2.5], _t2: [3, 2.5] }, circ: [['O', 3]], seg: ['AB', 'OC:blue', 'DE:orange', '_t1,_t2:green'], hide: ['A', 'B', 'C', 'D', 'E', 'F', '_t1', '_t2'], txt: [[-0.5, 1.6, '{{radius}}', 10, '#1f5fbf'], [-2.0, -1.2, '{{diameter}}', 10], [0.3, -2.75, '{{chord}}', 10, '#c0561b'], [4.2, 2.1, '{{tangent}}', 10, '#2f7a50']] }]
  }];
  N['U9-L2'] = [{
    h: 'Central angles and arcs',
    big: 'A {{central angle}} has its vertex at the center. Its {{intercepted arc}} has the {{same}} measure. A minor arc is less than 180°, a semicircle is 180°, and the whole circle is {{360°}}.',
    steps: ['Central angle 80° → minor arc ⟨\\overset{\\frown}{AB} = {{80°}}⟩.', 'Major arc ⟨= 360° - 80° = {{280°}}⟩.'],
    figs: [{ t: 'geo', w: 200, P: { O: O, A: pol(3, 10), B: pol(3, 90) }, circ: [['O', 3]], arc: [['O', 'A', 'B']], seg: ['OA', 'OB'], ang: [['A', 'O', 'B', '80°', 1, '#c0561b', 16]], txt: [[2.9, 2.6, '{{80°}}', 11, '#1f5fbf']], cap: 'Central angle = its arc' }]
  }];
  N['U9-L3'] = [{
    h: 'Inscribed angles',
    big: 'An {{inscribed angle}} has its vertex on the circle. It is {{half}} of its intercepted arc. An angle inscribed in a {{semicircle}} is a right angle (90°).',
    steps: ['Arc 100° → inscribed angle ⟨= {{50°}}⟩.', 'Inscribed angle 35° → arc ⟨= {{70°}}⟩.', 'Two inscribed angles on the same arc are equal.'],
    figs: [{ t: 'geo', w: 200, P: { O: O, A: pol(3, -10), B: pol(3, 90), C: pol(3, 220) }, circ: [['O', 3]], arc: [['O', 'A', 'B']], seg: ['CA', 'CB'], dots: true, ang: [['A', 'C', 'B', '{{50°}}', 1, '#c0561b', 22]], txt: [[2.9, 2.5, '100°', 11, '#1f5fbf']], hide: ['O'], cap: 'Inscribed angle = ½ arc' }]
  }];
  N['U9-L4'] = [{
    h: 'Tangents',
    big: 'A {{tangent}} touches the circle at one point. The radius to the point of tangency is {{perpendicular}} to the tangent (90°). Two tangent segments from the same outside point are {{equal}}.',
    steps: ['The right angle makes a right triangle: use the {{Pythagorean theorem}}.', 'Radius 5, distance from the center to P is 13: tangent ⟨= \\sqrt{169 - 25} = {{12}}⟩.'],
    figs: [{ t: 'geo', w: 230, P: { O: O, T: [0, 2], P: [Math.sqrt(13 * 13 - 25) * 2 / 5, 2] }, circ: [['O', 2]], seg: ['OT', 'TP:blue', 'OP:dash'], right: [['O', 'T', 'P']], slab: [['O', 'T', '5', 1], ['T', 'P', '{{12}}', 1, 10], ['O', 'P', '13', -1]], cap: 'Radius ⟂ tangent' }]
  }];
  N['U9-L5'] = [{
    h: 'Chords',
    big: 'When two chords cross inside a circle, the products of their pieces are equal: ⟨a \\cdot b = {{c \\cdot d}}⟩. A radius {{perpendicular}} to a chord {{bisects}} it, which makes a right triangle with the radius.',
    steps: ['Pieces 4 and 6 on one chord, 3 and ⟨x⟩ on the other: ⟨4 \\cdot 6 = 3x⟩, ⟨x = {{8}}⟩.', 'Chord 16 at distance 6 from the center: radius ⟨= \\sqrt{8^2 + 6^2} = {{10}}⟩.'],
    figs: [{ t: 'geo', w: 200, P: { O: O, A: pol(3, 150), B: pol(3, -20), C: pol(3, 70), D: pol(3, 245) }, circ: [['O', 3]], seg: ['AB', 'CD'], hide: ['O', 'A', 'B', 'C', 'D'], txt: [[-1.4, 1.0, 'a', 11, '#1f5fbf'], [1.5, -0.15, 'b', 11, '#1f5fbf'], [0.25, 1.9, 'c', 11, '#c0561b'], [-1, -1.6, 'd', 11, '#c0561b']], cap: '⟨ab = cd⟩' }]
  }];
  N['U9-L6'] = [{
    h: 'Secants and tangents from an outside point',
    big: 'From a point outside a circle: two secants → ⟨(\\text{outside})(\\text{whole}) = (\\text{outside})(\\text{whole})⟩. A tangent and a secant → ⟨(\\text{tangent})^2 = (\\text{outside})({{\\text{whole}}})⟩. Use the {{whole}} secant, not just its inside part.',
    steps: ['Tangent ⟨x⟩, secant outside part 4, whole 9: ⟨x^2 = 4 \\cdot 9 = 36⟩, ⟨x = {{6}}⟩.', 'Secants: outside 3, whole 12; outside 4, whole ⟨y⟩: ⟨3 \\cdot 12 = 4y⟩, ⟨y = {{9}}⟩.'],
    figs: [{ t: 'geo', w: 260, P: { O: O, P: [6, 0], A: [2, 0], B: [-2, 0], T: [2 / 3, Math.sqrt(4 - 4 / 9)] }, circ: [['O', 2]], seg: ['PB', 'PT:blue'], right: [], hide: ['O'], slab: [['P', 'A', 'outside', -1], ['P', 'T', '{{tangent}}', 1]], cap: '⟨PT^2 = PA \\cdot PB⟩' }]
  }];
  N['U9-L7'] = [{
    h: 'Arc length and sector area',
    big: 'An arc or sector is a {{fraction}} of the whole circle: ⟨\\frac{\\theta}{360°}⟩. Arc length ⟨= \\frac{\\theta}{360°} \\cdot {{2\\pi r}}⟩ (part of the circumference). Sector area ⟨= \\frac{\\theta}{360°} \\cdot {{\\pi r^2}}⟩ (part of the area).',
    steps: ['⟨r = 6⟩, ⟨\\theta = 60°⟩: fraction ⟨\\frac{60}{360} = \\frac{1}{6}⟩.', 'Arc length ⟨= \\frac{1}{6}(12\\pi) = {{2\\pi}}⟩.', 'Sector area ⟨= \\frac{1}{6}(36\\pi) = {{6\\pi}}⟩.'],
    figs: [{ t: 'geo', w: 200, P: { O: O, A: pol(3, 0), B: pol(3, 60) }, fill: [['O', 'A', 'B', '#dce8fb']], circ: [['O', 3]], arc: [['O', 'A', 'B']], seg: ['OA', 'OB'], ang: [['A', 'O', 'B', '60°', 1, '#c0561b', 14]], slab: [['O', 'A', '6', -1]], hide: ['A', 'B'], cap: 'The sector is ⟨\\frac{1}{6}⟩ of the circle' }]
  }];
  N['U9-L8'] = [{
    h: 'Equations of circles',
    big: 'A circle with center ⟨(h, k)⟩ and radius ⟨r⟩: ⟨(x - h)^2 + (y - k)^2 = r^2⟩. The signs inside are {{opposite}} to the center’s coordinates. For an expanded equation, {{complete the square}} in ⟨x⟩ and in ⟨y⟩.',
    steps: ['⟨(x - 2)^2 + (y + 1)^2 = 9⟩: center ⟨({{2, -1}})⟩, radius ⟨{{3}}⟩.', '⟨x^2 + y^2 - 4x + 2y - 4 = 0⟩ → ⟨(x - 2)^2 + (y + 1)^2 = 4 + 4 + 1 = 9⟩.'],
    figs: [{ t: 'plane', x: [-3, 7], y: [-6, 4], par: [{ p: '[2+3*cos(t), -1+3*sin(t)]', t: [0, 6.2832] }], segs: [[2, -1, 5, -1, false, '#c0561b']], pts: [[2, -1, '{{(2, −1)}}', null, null, -6, -6]], txt: [[3.5, -0.6, 'r = 3', 10, '#c0561b']] }]
  }];
  /* ---------- Unit 10 · Area, Surface Area and Volume ---------- */
  N['U10-L1'] = [{
    h: 'Area of rectangles and triangles',
    big: 'Rectangle: ⟨A = bh⟩. Triangle: ⟨A = {{\\frac{1}{2}}}bh⟩, because a triangle is half of a rectangle with the same base and height. The {{height}} is always {{perpendicular}} to the base, not a slanted side.',
    steps: ['Base 10, height 6: triangle area ⟨= \\frac{1}{2}(10)(6) = {{30}}⟩ square units.', 'Area is measured in {{square}} units.'],
    figs: [{ t: 'geo', w: 230, P: { A: [0, 0], B: [10, 0], C: [3, 6], H: [3, 0], R1: [0, 6], R2: [10, 6] }, fill: [['A', 'B', 'C', '#dce8fb']], poly: [['A', 'B', 'C']], seg: ['CH:dash', 'AR1:dash', 'R1,R2:dash', 'R2,B:dash'], right: [['B', 'H', 'C']], hide: ['A', 'B', 'C', 'H', 'R1', 'R2'], slab: [['A', 'B', '10', -1], ['H', 'C', '6', 1, 8]], cap: 'The triangle is half the rectangle: {{30}}' }]
  }];
  N['U10-L2'] = [{
    h: 'Parallelograms and trapezoids',
    big: 'Parallelogram: ⟨A = bh⟩ — cut off a triangle and slide it over to make a {{rectangle}}. Trapezoid: ⟨A = \\frac{1}{2}({{b_1 + b_2}})h⟩ — the {{average}} of the bases times the height.',
    steps: ['Parallelogram, base 8, height 5: ⟨A = {{40}}⟩.', 'Trapezoid, bases 6 and 10, height 4: ⟨A = \\frac{1}{2}(16)(4) = {{32}}⟩.'],
    figs: [{ t: 'geo', w: 180, P: { A: [0, 0], B: [8, 0], C: [10, 5], D: [2, 5], H: [2, 0] }, poly: [['A', 'B', 'C', 'D']], seg: ['DH:dash'], right: [['B', 'H', 'D']], hide: ['A', 'B', 'C', 'D', 'H'], slab: [['A', 'B', '8', -1], ['H', 'D', '5', -1, 8]], cap: 'Height ⟂ base' },
      { t: 'geo', w: 180, P: { A: [0, 0], B: [10, 0], C: [8, 4], D: [2, 4], H: [2, 0] }, poly: [['A', 'B', 'C', 'D']], seg: ['DH:dash'], right: [['B', 'H', 'D']], hide: ['A', 'B', 'C', 'D', 'H'], slab: [['A', 'B', '10', -1], ['D', 'C', '6', 1], ['H', 'D', '4', -1, 8]], cap: '⟨A = \\frac{1}{2}(6 + 10)(4)⟩' }]
  }];
  function box(l, w, h, labs) {   // an oblique drawing of a rectangular prism
    var dx = w * 0.5, dy = w * 0.35, P = { A: [0, 0], B: [l, 0], C: [l, h], D: [0, h], E: [dx, dy], F: [l + dx, dy], G: [l + dx, h + dy], H: [dx, h + dy] };
    return { t: 'geo', w: 230, dots: false, P: P, seg: ['AB', 'BC', 'CD', 'DA', 'BF', 'FG', 'GC', 'GH', 'HD', 'AE:dash', 'EF:dash', 'EH:dash'], hide: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], slab: [['A', 'B', labs[0], -1], ['B', 'F', labs[1], -1, 12], ['F', 'G', labs[2], -1]] };
  }
  N['U10-L3'] = [{
    h: 'Prisms',
    big: 'Volume of a prism ⟨= Bh⟩: the {{base area}} times the height; for a box ⟨V = lwh⟩ in {{cubic}} units. Surface area is the total area of all the {{faces}}: for a box ⟨S = 2lw + 2lh + 2wh⟩.',
    steps: ['Box 5 by 3 by 4: ⟨V = 5 \\cdot 3 \\cdot 4 = {{60}}⟩ cubic units.', '⟨S = 2(15) + 2(20) + 2(12) = {{94}}⟩ square units.'],
    figs: [Object.assign(box(5, 3, 4, ['5', '3', '4']), { cap: 'Three pairs of matching faces' })]
  }];
  N['U10-L4'] = [{
    h: 'Cylinders',
    big: 'Volume ⟨V = \\pi r^2 h⟩ (circle base area × height). Surface area ⟨S = {{2\\pi r^2}} + {{2\\pi rh}}⟩: two circles plus the curved side, which unrolls into a rectangle with length equal to the {{circumference}} ⟨2\\pi r⟩.',
    steps: ['⟨r = 3⟩, ⟨h = 10⟩: ⟨V = \\pi(9)(10) = {{90\\pi}}⟩.', '⟨S = 2\\pi(9) + 2\\pi(3)(10) = {{78\\pi}}⟩.'],
    figs: [{ t: 'geo', w: 150, dots: false, P: { A: [-3, 0], B: [3, 0], C: [3, 7], D: [-3, 7], O: [0, 7], O2: [0, 0], R: [3, 7] }, seg: ['AD', 'BC', 'O,R:blue'], ell: [['O', 3, 0.9], ['O2', 3, 0.9, true]], hide: ['A', 'B', 'C', 'D', 'O', 'O2', 'R'], txt: [[1.5, 7.35, 'r = 3', 10, '#1f5fbf'], [4.3, 3.5, 'h = 10', 10]], cap: 'Not drawn to scale' },
      { t: 'geo', w: 190, dots: false, P: { A: [0, 0], B: [6, 0], C: [6, 3], D: [0, 3], E: [3, 4.2], F: [3, -1.2] }, poly: [['A', 'B', 'C', 'D']], circ: [['E', 1.2], ['F', 1.2]], hide: ['A', 'B', 'C', 'D', 'E', 'F'], txt: [[3, 1.5, '{{length 2πr}}', 10], [6.5, 1.5, 'h', 10, null, 'start']], cap: 'The net of a cylinder' }]
  }];
  N['U10-L5'] = [{
    h: 'Pyramids and cones',
    big: 'A pyramid or cone holds {{one-third}} of the prism or cylinder with the same base and height: ⟨V = \\frac{1}{3}Bh⟩. Cone: ⟨V = \\frac{1}{3}\\pi r^2 h⟩. The height ⟨h⟩ is {{perpendicular}} to the base (not the slant height).',
    steps: ['Cone ⟨r = 3⟩, ⟨h = 8⟩: ⟨V = \\frac{1}{3}\\pi(9)(8) = {{24\\pi}}⟩.', 'Square pyramid, base 6 by 6, height 10: ⟨V = \\frac{1}{3}(36)(10) = {{120}}⟩.'],
    figs: [{ t: 'geo', w: 170, dots: false, P: { A: [-3, 0], B: [3, 0], V: [0, 8], O: [0, 0] }, ell: [['O', 3, 0.9]], seg: ['AV', 'BV', 'VO:dash', 'O,B:blue'], right: [['B', 'O', 'V']], hide: ['A', 'B', 'V', 'O'], txt: [[1.5, -0.6, 'r = 3', 10, '#1f5fbf'], [0.8, 4, 'h = 8', 10]], cap: '⟨V = \\frac{1}{3}\\pi r^2 h⟩' }]
  }];
  N['U10-L6'] = [{
    h: 'Spheres',
    big: 'Volume ⟨V = {{\\frac{4}{3}}}\\pi r^3⟩. Surface area ⟨S = {{4}}\\pi r^2⟩. Use the {{radius}}: if you are given the diameter, halve it first.',
    steps: ['Diameter 12 → ⟨r = 6⟩.', '⟨V = \\frac{4}{3}\\pi(216) = {{288\\pi}}⟩.', '⟨S = 4\\pi(36) = {{144\\pi}}⟩.'],
    figs: [{ t: 'geo', w: 150, dots: false, P: { O: [0, 0], R: [3, 0] }, circ: [['O', 3]], ell: [['O', 3, 0.8, true]], seg: ['OR:blue'], txt: [[1.5, 0.45, 'r', 11, '#1f5fbf']], hide: ['R'], cap: '⟨V = \\frac{4}{3}\\pi r^3⟩, ⟨S = 4\\pi r^2⟩' }]
  }];
  N['U10-L7'] = [{
    h: 'Nets and composite solids',
    big: 'A {{net}} is a solid unfolded flat; the total area of the net is the {{surface area}}. For a {{composite}} solid, split it into simple solids, find each volume, and {{add}} (or subtract a hollow part).',
    steps: ['A cylinder topped by a cone: ⟨V = \\pi r^2h_1 + \\frac{1}{3}\\pi r^2h_2⟩.', 'For surface area count only the faces on the outside.'],
    figs: [{ t: 'geo', w: 240, dots: false, P: { A: [0, 2], B: [2, 2], C: [2, 4], D: [0, 4], E: [4, 2], F: [4, 4], G: [6, 2], H: [6, 4], I: [8, 2], J: [8, 4], K: [2, 0], L: [4, 0], M: [2, 6], N: [4, 6] }, poly: [['A', 'B', 'C', 'D'], ['B', 'E', 'F', 'C'], ['E', 'G', 'H', 'F'], ['G', 'I', 'J', 'H'], ['K', 'L', 'E', 'B'], ['C', 'F', 'N', 'M']], hide: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'], cap: 'Net of a cube: {{6}} square faces' }]
  }];
  N['U10-L8'] = [{
    h: 'Finding a missing dimension',
    big: 'Write the volume formula, {{substitute}} what you know, and solve for the missing dimension with inverse operations. Divide by the {{whole base area}}, not by just one of its numbers.',
    steps: ['Box: ⟨V = 120⟩, ⟨l = 5⟩, ⟨w = 4⟩: ⟨120 = 20h⟩, ⟨h = {{6}}⟩.', 'Cylinder: ⟨V = 72\\pi⟩, ⟨r = 3⟩: ⟨72\\pi = 9\\pi h⟩, ⟨h = {{8}}⟩.'],
    figs: [Object.assign(box(5, 4, 3.2, ['5', '4', '{{h = 6}}']), { cap: '⟨V = 120⟩. Not drawn to scale' })]
  }];
})(typeof window !== 'undefined' ? window : globalThis);
