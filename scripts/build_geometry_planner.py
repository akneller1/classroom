#!/usr/bin/env python3
"""Builds the Geometry Daily Lesson Planner data (DRAFT scope and sequence, edit the lessons below and rerun):

  worksheet-generator/planner/geometry_scope_sequence.json   source of truth (same shape as algebra1_scope_sequence.json)
  worksheet-generator/planner/scope-geometry.js              window.MKPLAN_SCOPE_GEOMETRY
  worksheet-generator/planner/lesson-skills-geometry.js      window.MKPLAN_SKILLS_GEOMETRY (lesson -> verified skills + coverage)
  worksheet-generator/planner/notes-data-geometry.js         window.MKPLAN_GEOMETRY_NOTES: glossary + key ideas (planner/notes-geometry.js applies them)

Pacing: 180 days. Each unit alternates Lesson and Practice days, then Quiz, Review, Test and Flex days. Extra mixed-practice
days are added until the year totals 180. Standards are CCSS-M high-school geometry (HSG) codes."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'worksheet-generator', 'planner')
algebra = json.load(open(os.path.join(D, 'algebra1_scope_sequence.json'), encoding='utf-8'))

SETS = {'B': 'geometry-basics-reasoning', 'A': 'geometry-angles-parallel-lines', 'C': 'geometry-triangles-congruence',
        'T': 'geometry-triangle-relationships', 'S': 'geometry-similarity', 'R': 'geometry-right-triangles-trigonometry',
        'Q': 'geometry-quadrilaterals-polygons', 'X': 'geometry-transformations', 'K': 'geometry-circles',
        'M': 'geometry-area-surface-area-volume'}
UNIT_SET = {1: 'B', 2: 'A', 3: 'C', 4: 'T', 5: 'S', 6: 'R', 7: 'Q', 8: 'X', 9: 'K', 10: 'M'}
FILL, EXPLORE, PRE = 'Guided fill-in notes', 'Exploration, then guided notes', 'Pre-filled reference notes'

# ---------------------------------------------------------------- vocabulary (plain text; one definition per word)
V = {
 'point': 'A location with no size. Example: point A.',
 'line': 'A straight path that goes on forever in both directions. Example: line AB.',
 'plane': 'A flat surface that goes on forever in every direction. Example: a tabletop that never ends.',
 'segment': 'Part of a line with two endpoints. Example: segment AB has length AB.',
 'ray': 'Part of a line with one endpoint that goes on forever in one direction. Example: ray AB starts at A.',
 'collinear': 'Points that lie on the same line.',
 'postulate': 'A statement accepted as true without proof. Example: two points determine exactly one line.',
 'conditional statement': 'An if–then statement. Example: If a shape is a square, then it has four sides.',
 'converse': 'The statement made by swapping the if and the then parts of a conditional.',
 'counterexample': 'One example that makes a statement false. Example: 2 is prime but not odd.',
 'midpoint': 'The point that divides a segment into two equal parts.',
 'congruent': 'Having the same size and shape; matching parts are equal. Symbol: ≅.',
 'segment addition postulate': 'If B is between A and C, then AB + BC = AC.',
 'angle': 'Two rays with a common endpoint (the vertex). It is measured in degrees.',
 'vertex': 'The point where two sides of an angle or a polygon meet.',
 'angle addition postulate': 'If a ray is inside angle ABC, the two smaller angles add to the whole angle.',
 'angle bisector': 'A ray that splits an angle into two equal angles.',
 'acute': 'An angle less than 90°.',
 'obtuse': 'An angle greater than 90° and less than 180°.',
 'right angle': 'An angle that measures exactly 90°.',
 'straight angle': 'An angle that measures exactly 180°.',
 'distance formula': 'The distance between (x₁, y₁) and (x₂, y₂) is the square root of (x₂ − x₁)² + (y₂ − y₁)².',
 'midpoint formula': 'The midpoint of (x₁, y₁) and (x₂, y₂) is the average of the x-values and the average of the y-values.',
 'coordinate plane': 'A flat grid with a horizontal x-axis and a vertical y-axis; each point is an ordered pair (x, y).',
 'complementary': 'Two angles whose measures add to 90°.',
 'supplementary': 'Two angles whose measures add to 180°.',
 'vertical angles': 'The pair of opposite angles formed by two intersecting lines; they are equal.',
 'linear pair': 'Two adjacent angles that form a straight line; they add to 180°.',
 'adjacent angles': 'Two angles that share a vertex and a side but do not overlap.',
 'parallel lines': 'Lines in the same plane that never meet; they stay the same distance apart.',
 'transversal': 'A line that crosses two or more other lines.',
 'corresponding angles': 'Angles in matching positions at the two intersections of a transversal. Equal when the lines are parallel.',
 'alternate interior angles': 'Angles between the two lines on opposite sides of the transversal. Equal when the lines are parallel.',
 'alternate exterior angles': 'Angles outside the two lines on opposite sides of the transversal. Equal when the lines are parallel.',
 'same-side interior angles': 'Angles between the two lines on the same side of the transversal. They add to 180° when the lines are parallel.',
 'converse of a theorem': 'The reverse of a theorem. If the angles are equal, then the lines are parallel.',
 'corresponding parts': 'Sides or angles in matching positions of two congruent or similar figures.',
 'CPCTC': 'Corresponding parts of congruent triangles are congruent. Use it after proving the triangles congruent.',
 'third angle theorem': 'If two angles of one triangle equal two angles of another, the third angles are equal too.',
 'perimeter': 'The distance around a shape; the sum of its side lengths.',
 'SSS': 'Side-Side-Side: three pairs of equal sides make two triangles congruent.',
 'SAS': 'Side-Angle-Side: two pairs of equal sides and the equal angle between them make two triangles congruent.',
 'ASA': 'Angle-Side-Angle: two pairs of equal angles and the equal side between them make two triangles congruent.',
 'AAS': 'Angle-Angle-Side: two pairs of equal angles and an equal side that is not between them make two triangles congruent.',
 'HL': 'Hypotenuse-Leg: for right triangles, equal hypotenuses and one pair of equal legs make the triangles congruent.',
 'included angle': 'The angle formed by two sides. Example: the angle between sides AB and AC is angle A.',
 'two-column proof': 'A proof written as a table of statements and the reason for each one.',
 'flow proof': 'A proof drawn as boxes and arrows showing how each statement follows from the ones before it.',
 'reflexive property': 'Any figure is congruent to itself. Example: AB = AB (a shared side).',
 'interior angle': 'An angle inside a polygon formed by two sides.',
 'exterior angle': 'An angle formed by one side of a polygon and the extension of the next side.',
 'remote interior angles': 'The two interior angles of a triangle that are not next to a given exterior angle.',
 'isosceles triangle': 'A triangle with at least two equal sides. The angles opposite those sides are equal.',
 'base angles': 'The two equal angles of an isosceles triangle, opposite the equal sides.',
 'triangle inequality': 'Any two sides of a triangle add to more than the third side.',
 'midsegment': 'A segment joining the midpoints of two sides of a triangle. It is parallel to the third side and half as long.',
 'median': 'A segment from a vertex of a triangle to the midpoint of the opposite side.',
 'centroid': 'The point where the three medians meet. It is two-thirds of the way from each vertex to the opposite side.',
 'perpendicular bisector': 'A line that cuts a segment in half at a right angle. Every point on it is the same distance from both endpoints.',
 'altitude': 'A segment from a vertex perpendicular to the opposite side (or its extension). It is the height of the triangle.',
 'similar': 'Having the same shape but not necessarily the same size. Corresponding angles are equal and sides are proportional.',
 'ratio': 'A comparison of two quantities by division. Example: 3 to 4, or 3:4.',
 'proportion': 'An equation saying two ratios are equal. Example: 3/4 = 6/8.',
 'scale factor': 'The ratio of corresponding side lengths of two similar figures.',
 'dilation': 'A transformation that enlarges or shrinks a figure by a scale factor from a center point.',
 'AA similarity': 'Two pairs of equal angles are enough to make two triangles similar.',
 'SAS similarity': 'Two pairs of proportional sides and the equal angle between them make two triangles similar.',
 'SSS similarity': 'Three pairs of proportional sides make two triangles similar.',
 'triangle proportionality theorem': 'A line parallel to one side of a triangle divides the other two sides proportionally.',
 'indirect measurement': 'Finding a length that is hard to measure by using similar triangles. Example: finding a tree height from its shadow.',
 'hypotenuse': 'The longest side of a right triangle, opposite the right angle.',
 'leg': 'One of the two sides of a right triangle that form the right angle.',
 'Pythagorean theorem': 'In a right triangle, a² + b² = c², where c is the hypotenuse.',
 'Pythagorean triple': 'Three whole numbers that satisfy a² + b² = c². Example: 3, 4, 5.',
 '45-45-90 triangle': 'A right triangle with two equal legs. The hypotenuse is the leg times √2.',
 '30-60-90 triangle': 'A right triangle whose hypotenuse is twice the short leg; the long leg is the short leg times √3.',
 'sine': 'In a right triangle, sin of an angle = opposite side ÷ hypotenuse.',
 'cosine': 'In a right triangle, cos of an angle = adjacent side ÷ hypotenuse.',
 'tangent': 'In a right triangle, tan of an angle = opposite side ÷ adjacent side.',
 'tangent|circle': 'A line that touches a circle at exactly one point; it is perpendicular to the radius at that point.',
 'opposite side': 'The side across from the angle you are using.',
 'adjacent side': 'The leg next to the angle you are using (not the hypotenuse).',
 'inverse trigonometric function': 'Finds the angle from a ratio. Example: if sin A = 0.5, then A = sin⁻¹(0.5) = 30°.',
 'angle of elevation': 'The angle above the horizontal when you look up at an object.',
 'angle of depression': 'The angle below the horizontal when you look down at an object.',
 'polygon': 'A closed flat shape made of straight sides. Example: triangle, hexagon.',
 'convex': 'A polygon with no inward dents; every diagonal stays inside.',
 'diagonal': 'A segment joining two vertices of a polygon that are not next to each other.',
 'regular polygon': 'A polygon with all sides equal and all angles equal.',
 'parallelogram': 'A quadrilateral with both pairs of opposite sides parallel. Opposite sides and angles are equal.',
 'rectangle': 'A parallelogram with four right angles. Its diagonals are equal.',
 'rhombus': 'A parallelogram with four equal sides. Its diagonals are perpendicular bisectors of each other.',
 'square': 'A shape that is both a rectangle and a rhombus.',
 'trapezoid': 'A quadrilateral with exactly one pair of parallel sides (the bases).',
 'trapezoid midsegment': 'The segment joining the midpoints of the legs; its length is the average of the bases.',
 'quadrilateral': 'A polygon with four sides. Its interior angles add to 360°.',
 'transformation': 'A rule that moves or resizes a figure on the plane.',
 'image': 'The figure after a transformation. The original is the preimage.',
 'translation': 'A slide: every point moves the same distance in the same direction.',
 'reflection': 'A flip across a line; each point goes to the opposite side at the same distance.',
 'rotation': 'A turn about a fixed point by a given angle and direction.',
 'rigid motion': 'A transformation that keeps size and shape (translation, reflection, rotation).',
 'composition': 'Doing one transformation and then another.',
 'line of symmetry': 'A line that splits a figure into two mirror images.',
 'rotational symmetry': 'A figure looks the same after a turn of less than 360° about its center.',
 'circle': 'All points in a plane that are the same distance from a center.',
 'radius': 'A segment from the center of a circle to a point on it.',
 'diameter': 'A chord through the center of a circle; it is twice the radius.',
 'chord': 'A segment with both endpoints on a circle.',
 'secant': 'A line that crosses a circle at two points.',
 'central angle': 'An angle whose vertex is the center of the circle. It equals its intercepted arc.',
 'inscribed angle': 'An angle whose vertex is on the circle. It is half its intercepted arc.',
 'arc': 'A part of a circle between two points.',
 'intercepted arc': 'The arc that lies inside an angle.',
 'semicircle': 'Half of a circle; an arc of 180°.',
 'arc length': 'The distance along an arc: (arc angle ÷ 360°) × circumference.',
 'sector': 'A slice of a circle bounded by two radii and an arc.',
 'circumference': 'The distance around a circle: 2πr.',
 'area': 'The amount of flat space inside a shape, in square units.',
 'base': 'A side or face used as the bottom when measuring height or area.',
 'height': 'The perpendicular distance from a base to the opposite side, vertex or face.',
 'surface area': 'The total area of all the faces of a solid.',
 'volume': 'The amount of space inside a solid, in cubic units.',
 'prism': 'A solid with two parallel, congruent bases and rectangle sides.',
 'cylinder': 'A solid with two parallel circular bases and one curved side.',
 'pyramid': 'A solid with one base and triangular faces that meet at a point.',
 'cone': 'A solid with one circular base and a curved side that comes to a point.',
 'sphere': 'A solid where every point is the same distance from the center.',
 'net': 'A flat pattern that folds up into a solid. Its area is the surface area.',
 'composite solid': 'A solid made by joining two or more simpler solids.',
 'lateral area': 'The area of the sides of a solid, not counting its bases.',
 'completing the square': 'Rewriting x² + bx as (x + b/2)² − (b/2)² to read the center and radius of a circle.',
 'equation of a circle': '(x − h)² + (y − k)² = r² has center (h, k) and radius r.',
 'exact answer': 'An answer left in terms of π or a radical instead of a rounded decimal.',
}

# ---------------------------------------------------------------- lessons
# (title, standards, objective, language objective, sentence frame, [vocab], misconception, notes_style, cover, [skills], note, key idea)
def L(title, std, obj, lang, frame, vocab, mis, style, cover, skills, note, idea):
    return dict(title=title, std=std, obj=obj, lang=lang, frame=frame, vocab=vocab, mis=mis, style=style, cover=cover, skills=skills, note=note, idea=idea)

UNITS = [
 (1, 'Foundations of Geometry', [
  L('Points, Lines, Planes and Postulates', 'G-CO.A.1', 'name and describe points, lines, segments, rays and planes and use basic postulates.',
    'Students will describe in writing how two figures are different using precise vocabulary (point, line, plane, segment, ray).', 'A ___ has ___ but a ___ has ___.',
    ['point', 'line', 'plane', 'segment', 'ray', 'collinear', 'postulate'], 'Treating a line and a segment as the same thing; a line has no endpoints.', FILL, 'none',
    [('B', 'segment-addition', 1, 2)], 'Naming figures and postulates has no generator yet; the practice below reviews segment lengths. Add 4–5 naming and notation items.',
    'A line goes on forever; a segment has two endpoints; a ray has one. Name figures with capital letters.'),
  L('Segments and Midpoints', 'G-CO.D.12, G-GPE.B.6', 'use the segment addition postulate and the midpoint to find missing lengths.',
    'Students will explain orally how a midpoint divides a segment using the words midpoint and congruent.', 'Because M is the midpoint, ___ = ___, so ___.',
    ['segment addition postulate', 'midpoint', 'congruent'], 'Assuming a point is the midpoint because it looks halfway; it must be stated or marked.', FILL, 'full',
    [('B', 'segment-addition', 1, 7), ('B', 'midpoint', 1, 7)], '', 'If B is between A and C, then AB + BC = AC. A midpoint makes the two pieces equal.'),
  L('Angles and Angle Bisectors', 'G-CO.A.1, G-CO.C.9', 'use the angle addition postulate and angle bisectors to find missing angle measures.',
    'Students will write a sentence that tells how an angle bisector splits an angle.', 'Ray BD bisects angle ABC, so angle ___ = angle ___.',
    ['angle', 'vertex', 'angle addition postulate', 'angle bisector', 'acute', 'obtuse', 'right angle', 'straight angle'], 'Adding the whole angle to its parts; the parts add up to the whole.', FILL, 'full',
    [('B', 'angle-addition', 1, 7), ('B', 'angle-bisector', 1, 7)], '', 'The two smaller angles add to the whole angle. A bisector makes the two smaller angles equal.'),
  L('Distance and Midpoint on the Coordinate Plane', 'G-GPE.B.7, G-GPE.B.6', 'find distances and midpoints on the coordinate plane.',
    'Students will describe the steps for finding a midpoint using the words average and coordinate.', 'To find the midpoint, I ___ the x-values and ___ the y-values.',
    ['coordinate plane', 'distance formula', 'midpoint formula'], 'Subtracting the coordinates for the midpoint; the midpoint is an average, not a difference.', EXPLORE, 'full',
    [('B', 'coordinate-distance', 1, 7), ('B', 'coordinate-midpoint', 1, 7)], '', 'Midpoint: average the coordinates. Distance: the Pythagorean theorem on the horizontal and vertical changes.'),
  L('Coordinate Geometry Investigation', 'G-GPE.B.4, G-GPE.B.6', 'connect midpoints, endpoints and distances in a multi-step coordinate problem.',
    'Students will explain in writing how each step of a four-part coordinate problem depends on the one before it.', 'First I found ___, which let me find ___ because ___.',
    ['midpoint', 'distance formula', 'coordinate plane'], 'Starting the next part before checking the previous answer; each part builds on the last.', EXPLORE, 'full',
    [('B', 'coordinate-investigation', 1, 7), ('B', 'coordinate-midpoint', 5, 7)], '', 'A multi-part problem is a chain: check each answer before using it in the next part.'),
  L('Reasoning: If–Then Statements and Counterexamples', 'G-CO.C.9, MP.3', 'write conditional statements and their converses and use a counterexample to show a statement is false.',
    'Students will justify in writing why one counterexample disproves a statement.', 'The statement is false because ___ is a counterexample.',
    ['conditional statement', 'converse', 'counterexample'], 'Believing a true conditional must have a true converse; check the converse separately.', FILL, 'none',
    [('B', 'angle-addition', 1, 2)], 'Conditional statements, converses and counterexamples have no generator yet. Add 4–5 statements for students to rewrite and test.',
    'A conditional is true only if it is always true; one counterexample shows it is false. The converse may be false.'),
 ]),
 (2, 'Angles and Parallel Lines', [
  L('Complementary and Supplementary Angles', 'G-CO.C.9', 'use complementary and supplementary angle relationships to find missing angles.',
    'Students will compare complementary and supplementary angles using the words add and degrees.', 'Complementary angles add to ___ and supplementary angles add to ___.',
    ['complementary', 'supplementary', 'adjacent angles'], 'Mixing up 90° and 180°: complementary is 90°, supplementary is 180°.', FILL, 'full',
    [('A', 'complementary-angles', 1, 7), ('A', 'supplementary-angles', 1, 7)], '', 'Complementary angles add to 90°. Supplementary angles add to 180°.'),
  L('Vertical Angles and Linear Pairs', 'G-CO.C.9', 'use vertical angles and linear pairs to find missing angles.',
    'Students will explain why vertical angles are equal using the words intersect and opposite.', 'Angles ___ and ___ are vertical, so they are ___.',
    ['vertical angles', 'linear pair', 'adjacent angles'], 'Calling any two adjacent angles a linear pair; they must form a straight line.', EXPLORE, 'full',
    [('A', 'vertical-angles', 1, 7), ('A', 'linear-pairs', 1, 7)], '', 'Vertical angles are equal. A linear pair adds to 180°.'),
  L('Parallel Lines: Corresponding Angles', 'G-CO.C.9', 'identify corresponding angles and use them with parallel lines to find missing angles.',
    'Students will describe where corresponding angles are located using the words transversal and parallel.', 'Corresponding angles are in the ___ position, so they are ___ when the lines are ___.',
    ['parallel lines', 'transversal', 'corresponding angles'], 'Assuming the lines are parallel when the figure does not say so.', EXPLORE, 'full',
    [('A', 'corresponding-angles', 1, 7)], '', 'When parallel lines are cut by a transversal, corresponding angles are equal.'),
  L('Alternate Interior and Alternate Exterior Angles', 'G-CO.C.9', 'use alternate interior and alternate exterior angles with parallel lines to find missing angles.',
    'Students will explain in writing how alternate interior angles are located relative to the transversal.', 'Alternate interior angles are ___ the lines and on ___ sides of the transversal.',
    ['alternate interior angles', 'alternate exterior angles'], 'Mixing up interior and exterior: interior is between the lines.', FILL, 'full',
    [('A', 'alternate-interior', 1, 7), ('A', 'alternate-exterior', 1, 7)], '', 'Alternate interior angles are equal. Alternate exterior angles are equal.'),
  L('Same-Side Interior Angles and Mixed Angle Pairs', 'G-CO.C.9', 'identify every angle pair formed by a transversal and use it to find missing angles.',
    'Students will choose the correct angle relationship and justify the choice in a sentence.', 'I know the angles are ___ because they are ___ angles.',
    ['same-side interior angles', 'corresponding angles', 'alternate interior angles'], 'Setting same-side interior angles equal; they add to 180°.', FILL, 'full',
    [('A', 'same-side-interior', 1, 7), ('A', 'corresponding-angles', 3, 7), ('A', 'alternate-interior', 3, 7)], '', 'Same-side interior angles are supplementary. Name the pair first, then pick equal or supplementary.'),
  L('Proving Lines Are Parallel', 'G-CO.C.9', 'use the converse of the angle theorems to decide whether two lines are parallel.',
    'Students will write a justification that uses the converse of a theorem.', 'The lines are parallel because ___ angles are ___.',
    ['converse of a theorem', 'parallel lines', 'transversal'], 'Using the theorem when the converse is needed: equal angles prove the lines are parallel.', FILL, 'none',
    [('A', 'corresponding-angles', 4, 7), ('A', 'alternate-interior', 4, 7)], 'Deciding whether lines are parallel has no generator yet; the practice below uses the angle theorems. Add 4–5 questions: given the angle measures, are the lines parallel?',
    'If a transversal makes equal corresponding, alternate interior or alternate exterior angles, or supplementary same-side interior angles, the lines are parallel.'),
  L('Algebraic Angle Relationships', 'G-CO.C.9, A-CED.A.1', 'write and solve equations to find angles formed by parallel lines and a transversal.',
    'Students will explain how they chose the equation for an angle pair using the angle relationship.', 'I set the expressions ___ because the angles are ___.',
    ['transversal', 'supplementary', 'vertical angles'], 'Forgetting to substitute x back in to find the angle.', FILL, 'full',
    [('A', 'corresponding-angles', 5, 7), ('A', 'alternate-interior', 5, 7), ('A', 'alternate-exterior', 5, 7), ('A', 'same-side-interior', 5, 7)], '', 'Name the relationship, write the equation, solve for x, then find the angle.'),
 ]),
 (3, 'Triangle Congruence', [
  L('Congruent Figures and Corresponding Parts', 'G-CO.B.7, G-CO.B.8', 'identify corresponding parts of congruent triangles and use them to find missing sides and angles.',
    'Students will explain how congruence statements show which parts match.', 'Triangle ABC ≅ triangle DEF, so side ___ matches side ___.',
    ['congruent', 'corresponding parts', 'CPCTC'], 'Matching parts by position on the page instead of by the order of the letters.', EXPLORE, 'full',
    [('C', 'congruent-corresponding-sides', 1, 7), ('C', 'congruent-corresponding-angles', 1, 7)], '', 'In a congruence statement, the letters line up in order: the first letters match, the second letters match, and so on.'),
  L('Third Angle Theorem and Perimeter', 'G-CO.C.10, G-CO.B.7', 'use the third angle theorem and equal perimeters of congruent triangles.',
    'Students will explain why the third angles must be equal using the angle sum of a triangle.', 'The third angles are equal because ___.',
    ['third angle theorem', 'perimeter', 'congruent'], 'Thinking congruent triangles can have different perimeters; they are always equal.', FILL, 'full',
    [('C', 'congruent-third-angle', 1, 7), ('C', 'congruent-perimeters', 1, 7)], '', 'Triangle angles sum to 180°, so two equal angles force the third pair to be equal. Congruent triangles have equal perimeters.'),
  L('SSS and SAS Congruence', 'G-CO.B.8', 'use SSS and SAS to show triangles are congruent and then use CPCTC.',
    'Students will state the congruence criterion and name the three matching parts.', 'The triangles are congruent by ___ because ___.',
    ['SSS', 'SAS', 'included angle', 'CPCTC'], 'Using SAS when the equal angle is not between the two equal sides.', EXPLORE, 'full',
    [('C', 'congruence-sss', 1, 7), ('C', 'congruence-sas', 1, 7)], '', 'SSS: three pairs of equal sides. SAS: two pairs of equal sides with the equal angle between them. Then CPCTC.'),
  L('ASA and AAS Congruence', 'G-CO.B.8', 'use ASA and AAS to show triangles are congruent and then use CPCTC.',
    'Students will explain the difference between ASA and AAS in a sentence.', 'In ASA the side is ___ the angles; in AAS the side is ___.',
    ['ASA', 'AAS', 'included angle', 'CPCTC'], 'Mixing up ASA and AAS: the side is between the angles in ASA.', EXPLORE, 'full',
    [('C', 'congruence-asa', 1, 7), ('C', 'congruence-aas', 1, 7)], '', 'ASA: the equal side is between the two equal angles. AAS: the equal side is not between them.'),
  L('HL Congruence and Choosing a Criterion', 'G-CO.B.8', 'use HL for right triangles and decide which criterion, if any, proves congruence from marked figures.',
    'Students will explain why SSA and AAA do not prove congruence.', 'This is not enough because ___.',
    ['HL', 'hypotenuse', 'leg', 'SSS', 'SAS', 'ASA', 'AAS'], 'Thinking SSA or AAA proves congruence; neither is a valid criterion.', FILL, 'full',
    [('C', 'congruence-hl', 1, 7), ('C', 'congruence-identify', 1, 7)], '', 'HL needs a right angle, equal hypotenuses and one pair of equal legs. SSA and AAA do not prove congruence.'),
  L('Triangle Congruence Proofs', 'G-CO.B.8, G-CO.C.10', 'complete a two-column or flow proof that two triangles are congruent.',
    'Students will write a reason for each statement of a proof.', 'Statement ___ is true because ___.',
    ['two-column proof', 'flow proof', 'reflexive property', 'vertical angles', 'CPCTC'], 'Skipping the reason column; every statement needs a reason.', FILL, 'full',
    [('C', 'congruence-structured-proof', 1, 7)], '', 'Start with the givens, add facts from the diagram (shared side, vertical angles), prove the triangles congruent, then use CPCTC.'),
  L('CPCTC Applications', 'G-CO.B.7, G-CO.B.8', 'combine a congruence criterion with CPCTC to find unknown sides and angles.',
    'Students will explain the order: prove congruent first, then use CPCTC.', 'I proved the triangles congruent by ___, so ___ by CPCTC.',
    ['CPCTC', 'congruent', 'corresponding parts'], 'Using CPCTC before the triangles are proven congruent.', FILL, 'full',
    [('C', 'congruence-sss', 4, 7), ('C', 'congruence-sas', 4, 7), ('C', 'congruence-asa', 4, 7), ('C', 'congruence-aas', 4, 7), ('C', 'congruence-hl', 4, 7)], '', 'CPCTC can only be used after the triangles are proven congruent.'),
 ]),
 (4, 'Triangle Relationships', [
  L('Interior and Exterior Angles of Triangles', 'G-CO.C.10', 'use the triangle angle sum and the exterior angle theorem to find missing angles.',
    'Students will explain how an exterior angle relates to the remote interior angles.', 'The exterior angle equals the sum of ___.',
    ['interior angle', 'exterior angle', 'remote interior angles'], 'Adding the adjacent interior angle to find the exterior angle; use the two remote angles.', FILL, 'full',
    [('T', 'triangle-interior-sum', 1, 7), ('T', 'triangle-exterior-angle', 1, 7)], '', 'Interior angles add to 180°. An exterior angle equals the sum of the two remote interior angles.'),
  L('Isosceles Triangles', 'G-CO.C.10', 'use the base angles theorem to find missing angles of isosceles triangles.',
    'Students will describe which angles are equal in an isosceles triangle.', 'The base angles are ___ because the sides are ___.',
    ['isosceles triangle', 'base angles'], 'Marking the vertex angle equal to a base angle.', FILL, 'full',
    [('T', 'triangle-isosceles-angles', 1, 7)], '', 'Equal sides have equal angles opposite them.'),
  L('Triangle Inequality and Side–Angle Order', 'G-CO.C.10', 'use the triangle inequality and the order of sides and angles.',
    'Students will explain why three lengths may not make a triangle.', 'These lengths cannot form a triangle because ___.',
    ['triangle inequality'], 'Checking only one pair of sides; the largest side must be less than the sum of the other two.', EXPLORE, 'full',
    [('T', 'triangle-inequality-max-integer', 1, 7), ('T', 'triangle-side-angle-order', 1, 7)], '', 'Two sides must add to more than the third. The longest side is opposite the largest angle.'),
  L('Midsegments of Triangles', 'G-CO.C.10, G-GPE.B.4', 'use the midsegment theorem to find lengths.',
    'Students will describe the relationship between a midsegment and the third side.', 'The midsegment is ___ to the third side and ___ as long.',
    ['midsegment', 'midpoint', 'parallel lines'], 'Doubling when you should halve: the midsegment is half the third side.', EXPLORE, 'full',
    [('T', 'triangle-midsegment-length', 1, 7)], '', 'A midsegment is parallel to the third side and half its length.'),
  L('Medians and the Centroid', 'G-CO.C.10', 'use the 2:1 ratio of the centroid to find lengths on a median.',
    'Students will explain how the centroid divides a median.', 'The centroid is ___ of the way from the vertex.',
    ['median', 'centroid'], 'Putting the 2:1 ratio the wrong way; the longer part is next to the vertex.', FILL, 'full',
    [('T', 'triangle-centroid-median', 1, 7)], '', 'The centroid splits each median 2:1, with the longer part toward the vertex.'),
  L('Perpendicular Bisectors and Altitudes', 'G-CO.C.9, G-CO.C.10', 'use the perpendicular bisector theorem and altitudes to find lengths and areas.',
    'Students will explain what is true about points on a perpendicular bisector.', 'Any point on the perpendicular bisector is ___ from the endpoints.',
    ['perpendicular bisector', 'altitude', 'height'], 'Drawing the altitude to the midpoint of the side; the altitude is only perpendicular.', FILL, 'full',
    [('T', 'triangle-perpendicular-bisector', 1, 7), ('T', 'triangle-altitude-area', 1, 7)], '', 'Points on a perpendicular bisector are equally far from the endpoints. The altitude is the height used in the area formula.'),
  L('Triangle Relationships Investigation', 'G-CO.C.10, MP.1', 'solve a multi-part problem combining midsegments, centroids and the triangle inequality.',
    'Students will explain in writing how each part of an investigation connects to the next.', 'I used ___ in part (a) to find ___ in part (b).',
    ['midsegment', 'centroid', 'triangle inequality'], 'Treating each part as a separate problem; later parts use earlier answers.', EXPLORE, 'full',
    [('T', 'triangle-open-response-investigation', 1, 7), ('T', 'triangle-honors-connected-investigation', 5, 7)], '', 'Plan the chain of facts first, then solve each part in order.'),
 ]),
 (5, 'Similarity', [
  L('Ratios and Proportions in Similar Figures', 'G-SRT.A.2, G-SRT.B.5', 'set up and solve proportions to find missing sides of similar triangles.',
    'Students will explain which sides correspond and how they know.', 'Side ___ corresponds to side ___ because they are opposite ___.',
    ['similar', 'ratio', 'proportion', 'corresponding parts'], 'Matching sides by position instead of by equal angles.', FILL, 'full',
    [('S', 'similarity-missing-side', 1, 7), ('S', 'similarity-angle', 1, 7)], '', 'Similar figures have equal angles and proportional sides. Match sides by the angles they are opposite.'),
  L('Scale Factor and Dilations', 'G-SRT.A.1', 'find and use the scale factor of a dilation.',
    'Students will describe what a scale factor greater than 1 and less than 1 does to a figure.', 'A scale factor of ___ makes the figure ___.',
    ['dilation', 'scale factor', 'similar'], 'Putting the original length over the new length; the scale factor is image ÷ original.', EXPLORE, 'full',
    [('S', 'similarity-scale-factor', 1, 7)], '', 'Scale factor = image length ÷ original length. More than 1 enlarges; less than 1 shrinks.'),
  L('Perimeter of Similar Figures', 'G-SRT.A.2', 'use the scale factor to find the perimeter of a similar figure.',
    'Students will explain how perimeters of similar figures compare.', 'The perimeters are in the ratio ___, the same as ___.',
    ['perimeter', 'scale factor', 'ratio'], 'Squaring the scale factor for perimeter; that is for area.', FILL, 'full',
    [('S', 'similarity-perimeter', 1, 7)], '', 'Perimeters of similar figures are in the same ratio as corresponding sides.'),
  L('AA Similarity', 'G-SRT.A.3', 'use AA to prove triangles are similar and find corresponding angles.',
    'Students will explain why two pairs of equal angles are enough.', 'The triangles are similar by AA because ___.',
    ['AA similarity', 'similar', 'third angle theorem'], 'Looking for a third pair of angles; two pairs are enough.', EXPLORE, 'full',
    [('S', 'similarity-aa-criterion', 1, 7)], '', 'Two pairs of equal angles make triangles similar, because the third pair must be equal too.'),
  L('SAS and SSS Similarity', 'G-SRT.B.4, G-SRT.B.5', 'use SAS and SSS similarity to decide whether triangles are similar.',
    'Students will compare the side ratios and state the criterion.', 'The side ratios are ___, ___ and ___, so the triangles are similar by ___.',
    ['SAS similarity', 'SSS similarity', 'ratio', 'included angle'], 'Checking that sides are equal instead of proportional.', FILL, 'full',
    [('S', 'similarity-sas-criterion', 1, 7), ('S', 'similarity-sss-criterion', 1, 7)], '', 'SSS: all three ratios are equal. SAS: two ratios are equal and the angle between them is equal.'),
  L('The Triangle Proportionality Theorem', 'G-SRT.B.4', 'use a line parallel to one side of a triangle to find lengths on the other two sides.',
    'Students will explain why a parallel line divides two sides proportionally.', 'Since DE is parallel to BC, ___ / ___ = ___ / ___.',
    ['triangle proportionality theorem', 'parallel lines', 'proportion'], 'Setting a part over the whole on one side and part over part on the other.', EXPLORE, 'full',
    [('S', 'similarity-parallel-segment', 1, 7)], '', 'A line parallel to one side cuts the other two sides in the same ratio.'),
  L('Indirect Measurement', 'G-SRT.B.5, G-MG.A.3', 'use similar triangles to find heights from shadows.',
    'Students will explain why shadows of objects at the same time form similar triangles.', 'The triangles are similar because the sun rays are ___.',
    ['indirect measurement', 'similar', 'proportion'], 'Mixing the units or putting the object height over the other shadow.', FILL, 'full',
    [('S', 'similarity-shadow', 1, 7)], '', 'At the same time of day, height ÷ shadow is the same for every object.'),
  L('Similarity Investigation', 'G-SRT.B.4, MP.1', 'solve a multi-part problem about a line parallel to a side of a triangle.',
    'Students will explain in writing how each part of the investigation uses similarity.', 'I used the proportion ___ to find ___.',
    ['triangle proportionality theorem', 'similar', 'proportion'], 'Starting a proportion with sides that do not correspond.', EXPLORE, 'full',
    [('S', 'similarity-parallel-honors', 1, 7), ('S', 'similarity-parallel-segment', 5, 7)], '', 'Draw both similar triangles separately and label corresponding sides before writing the proportion.'),
 ]),
 (6, 'Right Triangles and Trigonometry', [
  L('The Pythagorean Theorem', 'G-SRT.C.8, 8.G.B.7', 'use the Pythagorean theorem to find a missing side of a right triangle.',
    'Students will explain which side is the hypotenuse and how they know.', 'The hypotenuse is the side ___ the right angle.',
    ['hypotenuse', 'leg', 'Pythagorean theorem', 'Pythagorean triple'], 'Adding the squares when the unknown is a leg; subtract for a leg.', FILL, 'full',
    [('R', 'right-pythagorean-hypotenuse', 1, 7), ('R', 'right-pythagorean-leg', 1, 7)], '', 'a² + b² = c², where c is the hypotenuse. For a missing leg, subtract.'),
  L('Distance on the Coordinate Plane', 'G-GPE.B.7', 'use the distance formula as the Pythagorean theorem.',
    'Students will describe the right triangle hidden in a distance problem.', 'The horizontal change is ___ and the vertical change is ___.',
    ['distance formula', 'coordinate plane', 'Pythagorean theorem'], 'Forgetting to take the square root at the end.', EXPLORE, 'full',
    [('R', 'right-distance-formula', 1, 7)], '', 'The distance between two points is the hypotenuse of a right triangle with the horizontal and vertical changes as legs.'),
  L('Special Right Triangles', 'G-SRT.C.6, G-SRT.C.8', 'use the side ratios of 45-45-90 and 30-60-90 triangles.',
    'Students will state the side ratios of each special right triangle.', 'In a 30-60-90 triangle the short leg is ___, the long leg is ___ and the hypotenuse is ___.',
    ['45-45-90 triangle', '30-60-90 triangle', 'hypotenuse', 'leg'], 'Putting √3 on the wrong leg; the long leg is opposite 60°.', EXPLORE, 'full',
    [('R', 'right-special-45-45-90', 1, 7), ('R', 'right-special-30-60-90', 1, 7), ('R', 'right-special-radical', 1, 7)], '', '45-45-90: legs equal, hypotenuse = leg × √2. 30-60-90: hypotenuse = 2 × short leg, long leg = short leg × √3.'),
  L('Sine, Cosine and Tangent', 'G-SRT.C.6', 'name the sides of a right triangle and write the three trigonometric ratios.',
    'Students will explain the meaning of opposite, adjacent and hypotenuse for a chosen angle.', 'For angle A, the opposite side is ___ and the adjacent side is ___.',
    ['sine', 'cosine', 'tangent', 'opposite side', 'adjacent side', 'hypotenuse'], 'Labeling opposite and adjacent from the right angle; they depend on the angle you use.', EXPLORE, 'full',
    [('R', 'right-sine-side', 1, 3), ('R', 'right-cosine-side', 1, 3), ('R', 'right-tangent-side', 1, 3)], '', 'SOH-CAH-TOA: sin = opposite ÷ hypotenuse, cos = adjacent ÷ hypotenuse, tan = opposite ÷ adjacent.'),
  L('Solving for Sides with Trigonometry', 'G-SRT.C.8', 'use sine, cosine and tangent to find missing sides of right triangles.',
    'Students will explain how they chose the ratio for a given side.', 'I used ___ because I know ___ and want ___.',
    ['sine', 'cosine', 'tangent', 'opposite side', 'adjacent side'], 'Using the wrong ratio; label the sides first.', FILL, 'full',
    [('R', 'right-sine-side', 3, 7), ('R', 'right-cosine-side', 3, 7), ('R', 'right-tangent-side', 3, 7)], '', 'Label the sides from the angle, choose the ratio that uses the given and wanted sides, then solve.'),
  L('Inverse Trigonometric Functions', 'G-SRT.C.8', 'use inverse trigonometric functions to find an acute angle.',
    'Students will describe when to use an inverse trigonometric function.', 'I use the inverse function when I know ___ and want ___.',
    ['inverse trigonometric function', 'sine', 'cosine', 'tangent'], 'Dividing instead of using the inverse key on the calculator.', FILL, 'full',
    [('R', 'right-inverse-trig', 1, 7), ('R', 'right-inverse-trig-decimal', 1, 7)], '', 'When the sides are known and the angle is wanted, use sin⁻¹, cos⁻¹ or tan⁻¹.'),
  L('Angles of Elevation and Depression', 'G-SRT.C.8, G-MG.A.1', 'use trigonometry to solve problems with angles of elevation and depression.',
    'Students will explain how the angle of elevation and the angle of depression are related.', 'The angle of depression equals the angle of ___ because ___.',
    ['angle of elevation', 'angle of depression', 'tangent'], 'Measuring the angle from the vertical; it is measured from the horizontal.', EXPLORE, 'full',
    [('R', 'right-angle-elevation', 1, 7), ('R', 'right-angle-depression', 1, 7)], '', 'Draw the horizontal line and the right triangle. The angle of depression equals the angle of elevation from the other end.'),
  L('Right Triangle Investigation', 'G-SRT.C.8, MP.1', 'solve a multi-part surveying problem using similar triangles and trigonometry.',
    'Students will explain in writing how each part of the investigation uses a right triangle.', 'In part ___ I used ___ to find ___.',
    ['tangent', 'similar', 'angle of elevation'], 'Rounding in the middle of the problem; keep full values until the end.', EXPLORE, 'full',
    [('R', 'right-honors-survey', 1, 7), ('R', 'right-angle-elevation', 5, 7)], '', 'Draw one clear diagram with every right triangle labeled, then solve one triangle at a time.'),
  L('Applications of Right Triangles', 'G-SRT.C.8, G-MG.A.1', 'solve applications that need the Pythagorean theorem, special triangles or trigonometry.',
    'Students will explain why they chose a method for a word problem.', 'I used ___ because I know ___ and need ___.',
    ['Pythagorean theorem', 'sine', 'cosine', 'tangent', 'hypotenuse'], 'Choosing trigonometry when the Pythagorean theorem is faster (two sides known).', FILL, 'full',
    [('R', 'right-pythagorean-hypotenuse', 5, 7), ('R', 'right-pythagorean-leg', 5, 7), ('R', 'right-tangent-side', 5, 7), ('R', 'right-special-radical', 4, 7)], '', 'Two sides known: Pythagorean theorem. An angle and a side known: trigonometry. Special angle: special-triangle ratios.'),
 ]),
 (7, 'Quadrilaterals and Polygons', [
  L('Interior Angles of Polygons', 'G-CO.C.11, G-CO.C.10', 'use the angle sum of a polygon to find missing angles and the number of sides.',
    'Students will explain how the number of sides gives the angle sum.', 'The interior angles add to ___ because the polygon splits into ___ triangles.',
    ['polygon', 'convex', 'interior angle', 'quadrilateral'], 'Using n × 180° instead of (n − 2) × 180°.', EXPLORE, 'full',
    [('Q', 'quadrilateral-angle-sum', 1, 7), ('Q', 'polygon-interior-sum', 1, 7)], '', 'The interior angles of an n-sided polygon add to (n − 2) × 180°.'),
  L('Exterior Angles and Regular Polygons', 'G-CO.C.11', 'use exterior angles and regular polygons to find angle measures and the number of sides.',
    'Students will explain why exterior angles of a polygon add to 360°.', 'Each exterior angle of a regular polygon is ___ divided by ___.',
    ['exterior angle', 'regular polygon', 'diagonal'], 'Thinking the exterior angle sum depends on the number of sides; it is always 360°.', FILL, 'full',
    [('Q', 'regular-polygon-exterior', 1, 7), ('Q', 'polygon-diagonal-count', 1, 7)], '', 'Exterior angles of any convex polygon add to 360°. Each one in a regular polygon is 360° ÷ n.'),
  L('Parallelograms', 'G-CO.C.11', 'use the properties of parallelograms to find missing sides and angles.',
    'Students will list the properties of a parallelogram using precise vocabulary.', 'In a parallelogram, opposite ___ are ___ and consecutive angles are ___.',
    ['parallelogram', 'diagonal', 'supplementary'], 'Setting consecutive angles equal; they add to 180°.', EXPLORE, 'full',
    [('Q', 'parallelogram-opposite-sides', 1, 7), ('Q', 'parallelogram-opposite-angles', 1, 7), ('Q', 'parallelogram-consecutive-angles', 1, 7), ('Q', 'parallelogram-algebraic-consecutive-angles', 4, 7)], '', 'Opposite sides and angles are equal; consecutive angles add to 180°; diagonals bisect each other.'),
  L('Rectangles, Rhombi and Squares', 'G-CO.C.11', 'use the diagonal properties of rectangles, rhombi and squares.',
    'Students will compare the diagonals of a rectangle and a rhombus.', 'The diagonals of a rectangle are ___; the diagonals of a rhombus are ___.',
    ['rectangle', 'rhombus', 'square', 'diagonal'], 'Believing every rhombus has equal diagonals; only a square (or rectangle) does.', EXPLORE, 'full',
    [('Q', 'rectangle-diagonal-bisectors', 1, 7), ('Q', 'rhombus-diagonal-bisectors', 1, 7)], '', 'Rectangle: equal diagonals that bisect each other. Rhombus: perpendicular diagonals that bisect each other.'),
  L('Trapezoids', 'G-CO.C.11, G-GPE.B.4', 'use the midsegment of a trapezoid to find lengths.',
    'Students will explain how the midsegment length relates to the bases.', 'The midsegment equals the ___ of the two bases.',
    ['trapezoid', 'trapezoid midsegment', 'midpoint'], 'Subtracting the bases instead of averaging them.', FILL, 'full',
    [('Q', 'trapezoid-midsegment', 1, 7)], '', 'The midsegment is parallel to the bases and equals half the sum of the bases.'),
  L('Classifying and Proving Quadrilaterals', 'G-CO.C.11, G-GPE.B.4', 'classify quadrilaterals from their properties and use converses to prove a quadrilateral is a parallelogram.',
    'Students will justify a classification using the converse of a parallelogram property.', 'It is a parallelogram because ___.',
    ['parallelogram', 'rhombus', 'square', 'converse'], 'Calling a shape a rectangle because it has one right angle.', FILL, 'full',
    [('Q', 'classify-square-rhombus', 1, 7), ('Q', 'parallelogram-diagonal-bisection-converse', 1, 7)], '', 'If both diagonals bisect each other, the quadrilateral is a parallelogram. Check every property before naming it a rectangle, rhombus or square.'),
 ]),
 (8, 'Transformations', [
  L('Translations', 'G-CO.A.2, G-CO.A.5', 'translate points and figures on the coordinate plane.',
    'Students will describe a translation using the words left, right, up and down.', 'The figure moves ___ units ___ and ___ units ___.',
    ['transformation', 'image', 'translation', 'rigid motion'], 'Moving up when the rule says subtract; read the signs carefully.', EXPLORE, 'full',
    [('X', 'translate-horizontal', 1, 7), ('X', 'translate-vertical', 1, 7), ('X', 'translate-triangle-figure', 1, 7)], '', 'A translation adds the same amount to every x and the same amount to every y.'),
  L('Reflections', 'G-CO.A.2, G-CO.A.5', 'reflect points and figures across the axes and other lines.',
    'Students will explain how a reflection changes the coordinates.', 'Reflecting over the ___-axis changes the sign of the ___-coordinate.',
    ['reflection', 'image', 'rigid motion'], 'Changing the wrong coordinate; reflecting over the x-axis changes y.', EXPLORE, 'full',
    [('X', 'reflect-x-axis', 1, 7), ('X', 'reflect-y-axis', 1, 7), ('X', 'reflect-triangle-figure', 1, 7)], '', 'Over the x-axis (x, y) → (x, −y). Over the y-axis (x, y) → (−x, y). Each point is the same distance from the mirror line.'),
  L('Rotations', 'G-CO.A.2, G-CO.A.4', 'rotate points and figures 90° and 180° about the origin.',
    'Students will describe a rotation using the angle and direction.', 'The figure is rotated ___° ___ about the ___.',
    ['rotation', 'image', 'rigid motion'], 'Mixing up clockwise and counterclockwise.', EXPLORE, 'full',
    [('X', 'rotate-90-clockwise', 1, 7), ('X', 'rotate-90-counterclockwise', 1, 7), ('X', 'rotate-triangle-figure', 1, 7)], '', '90° clockwise: (x, y) → (y, −x). 90° counterclockwise: (x, y) → (−y, x). 180°: (x, y) → (−x, −y).'),
  L('Dilations', 'G-SRT.A.1', 'dilate points and figures about the origin by a scale factor.',
    'Students will explain how a dilation changes the size but not the shape.', 'A dilation with scale factor ___ makes each distance ___ times as long.',
    ['dilation', 'scale factor', 'image', 'similar'], 'Adding the scale factor instead of multiplying.', FILL, 'full',
    [('X', 'dilate-origin', 1, 7), ('X', 'dilate-triangle-figure', 1, 7)], '', 'A dilation about the origin multiplies both coordinates by the scale factor.'),
  L('Compositions of Transformations', 'G-CO.A.5', 'perform a sequence of two transformations and find the final image.',
    'Students will explain the order in which the two transformations are done.', 'First I ___, then I ___, so the final image is ___.',
    ['composition', 'transformation', 'image'], 'Doing the two steps in the wrong order; the order can change the answer.', FILL, 'full',
    [('X', 'compose-triangle-figure', 1, 7)], '', 'Apply the first transformation, mark the middle image, then apply the second transformation to that image.'),
  L('Symmetry', 'G-CO.A.3', 'find the lines of symmetry and the angle of rotational symmetry of regular polygons.',
    'Students will describe the symmetry of a regular polygon using the number of sides.', 'A regular ___-gon has ___ lines of symmetry and rotates onto itself every ___°.',
    ['line of symmetry', 'rotational symmetry', 'regular polygon'], 'Counting only the lines through vertices.', EXPLORE, 'full',
    [('X', 'symmetry-lines-regular', 1, 7), ('X', 'symmetry-rotation-regular', 1, 7)], '', 'A regular n-gon has n lines of symmetry and rotates onto itself every 360° ÷ n.'),
  L('Transformations and Congruence', 'G-CO.B.6, G-SRT.A.2', 'use rigid motions and dilations to explain congruent and similar figures.',
    'Students will explain whether a sequence of transformations produces a congruent or a similar figure.', 'The figures are ___ because the transformations are ___.',
    ['rigid motion', 'dilation', 'congruent', 'similar'], 'Thinking a dilation keeps the figure congruent; it only keeps it similar.', EXPLORE, 'partial',
    [('X', 'compose-triangle-figure', 3, 7), ('X', 'dilate-triangle-figure', 3, 7)], 'Deciding congruent or similar from a described transformation sequence has no generator yet. Add 3–4 sequences and ask for the relationship.',
    'Translations, reflections and rotations keep size and shape (congruent). A dilation keeps shape but changes size (similar).'),
 ]),
 (9, 'Circles', [
  L('Parts of a Circle', 'G-C.A.1', 'name the parts of a circle and relate the radius and diameter.',
    'Students will describe each part of a circle using precise vocabulary.', 'A ___ is a segment with ___ on the circle.',
    ['circle', 'radius', 'diameter', 'chord', 'secant', 'tangent|circle'], 'Mixing up a radius and a diameter in a formula.', FILL, 'full',
    [('K', 'circle-diameter', 1, 7), ('K', 'circle-radius', 1, 7)], '', 'The diameter is twice the radius. A chord has both endpoints on the circle; a diameter is the longest chord.'),
  L('Central Angles and Arcs', 'G-C.A.2', 'use central angles to find the measure of an arc.',
    'Students will explain how a central angle and its arc are related.', 'The central angle is ___ the measure of its ___.',
    ['central angle', 'arc', 'intercepted arc', 'semicircle'], 'Halving the central angle; the central angle equals its arc.', FILL, 'full',
    [('K', 'circle-central-arc', 1, 7)], '', 'A central angle has the same measure as its intercepted arc.'),
  L('Inscribed Angles', 'G-C.A.2', 'use inscribed angles and intercepted arcs, including angles in a semicircle.',
    'Students will explain how an inscribed angle compares to its intercepted arc.', 'The inscribed angle is ___ of the intercepted arc.',
    ['inscribed angle', 'intercepted arc', 'semicircle'], 'Setting the inscribed angle equal to its arc; it is half.', EXPLORE, 'full',
    [('K', 'circle-inscribed-angle', 1, 7), ('K', 'circle-intercepted-arc', 1, 7), ('K', 'circle-semicircle-angle', 1, 7)], '', 'An inscribed angle is half its intercepted arc. An angle inscribed in a semicircle is 90°.'),
  L('Tangents', 'G-C.A.2', 'use the fact that a tangent is perpendicular to the radius at the point of tangency.',
    'Students will explain the angle between a tangent and a radius.', 'The tangent is ___ to the radius at the point of ___.',
    ['tangent|circle', 'radius', 'right angle'], 'Drawing the radius to a different point than the point of tangency.', EXPLORE, 'full',
    [('K', 'circle-tangent-radius', 1, 7)], '', 'A tangent meets the radius at the point of tangency at 90°.'),
  L('Chords', 'G-C.A.2', 'use intersecting chords and distance from the center to find lengths.',
    'Students will explain how the segments of two intersecting chords are related.', 'The product of the parts of one chord equals the product of the parts of the ___.',
    ['chord', 'radius', 'Pythagorean theorem'], 'Adding the parts instead of multiplying them.', FILL, 'full',
    [('K', 'circle-intersecting-chords', 1, 7), ('K', 'circle-chord-length-from-distance', 1, 7)], '', 'For two chords crossing inside a circle, (part)(part) = (part)(part). A radius perpendicular to a chord bisects it.'),
  L('Secants and Tangent–Secant Segments', 'G-C.A.2', 'use secant and tangent segments drawn from a point outside a circle.',
    'Students will explain how the outside part and whole secant are used in the equation.', 'Outside part × whole secant = ___.',
    ['secant', 'tangent|circle'], 'Using only the outside part of the secant instead of the whole secant.', FILL, 'full',
    [('K', 'circle-two-secants', 1, 7), ('K', 'circle-tangent-secant', 1, 7)], '', 'Two secants: (outside)(whole) = (outside)(whole). Tangent and secant: (tangent)² = (outside)(whole).'),
  L('Arc Length and Sector Area', 'G-C.B.5', 'find arc length and sector area in exact form.',
    'Students will explain how the fraction of the circle is used in the formulas.', 'The arc is ___ of the circle, so its length is ___ of the circumference.',
    ['arc length', 'sector', 'circumference', 'exact answer'], 'Using the diameter in the area formula.', FILL, 'full',
    [('K', 'circle-arc-length-exact', 1, 7), ('K', 'circle-sector-area-exact', 1, 7)], '', 'Arc length = (angle ÷ 360°) × 2πr. Sector area = (angle ÷ 360°) × πr².'),
  L('Equations of Circles', 'G-GPE.A.1', 'find the center and radius of a circle from its equation.',
    'Students will explain how to read the center and radius from the equation.', 'The center is (___, ___) and the radius is ___.',
    ['equation of a circle', 'completing the square', 'radius'], 'Using the opposite sign for the center; (x − 3) means the center has x = 3.', FILL, 'full',
    [('K', 'circle-radius-squared-from-point', 1, 7), ('K', 'circle-center-expanded-equation', 1, 7), ('K', 'circle-radius-expanded-equation', 1, 7)], '', '(x − h)² + (y − k)² = r² has center (h, k) and radius r. Complete the square to rewrite an expanded equation.'),
 ]),
 (10, 'Area, Surface Area and Volume', [
  L('Area of Rectangles and Triangles', 'G-GMD.A.1, 6.G.A.1', 'find the area of rectangles and triangles.',
    'Students will explain why the triangle area formula has a one-half.', 'A triangle is ___ of a rectangle with the same ___ and ___.',
    ['area', 'base', 'height'], 'Using a slanted side as the height; height is perpendicular to the base.', FILL, 'full',
    [('M', 'measure-rectangle-area', 1, 7), ('M', 'measure-triangle-area', 1, 7)], '', 'Rectangle: A = bh. Triangle: A = ½bh. The height is perpendicular to the base.'),
  L('Area of Parallelograms and Trapezoids', 'G-GMD.A.1, 6.G.A.1', 'find the area of parallelograms and trapezoids.',
    'Students will explain how the trapezoid area formula uses both bases.', 'The area of a trapezoid is half the ___ of the bases times the ___.',
    ['parallelogram', 'trapezoid', 'base', 'height'], 'Multiplying the bases instead of adding them.', FILL, 'full',
    [('M', 'measure-parallelogram-area', 1, 7), ('M', 'measure-trapezoid-area', 1, 7)], '', 'Parallelogram: A = bh. Trapezoid: A = ½(b₁ + b₂)h.'),
  L('Prisms: Volume and Surface Area', 'G-GMD.A.3, 6.G.A.2', 'find the volume and surface area of rectangular prisms.',
    'Students will explain the difference between volume and surface area using units.', 'Volume is measured in ___ units and surface area in ___ units.',
    ['prism', 'volume', 'surface area', 'area'], 'Using square units for volume.', FILL, 'full',
    [('M', 'measure-prism-volume', 1, 7), ('M', 'measure-prism-surface', 1, 7)], '', 'Volume: V = lwh. Surface area: add the areas of all six faces.'),
  L('Cylinders', 'G-GMD.A.3', 'find the volume and surface area of cylinders.',
    'Students will explain where each part of the cylinder surface area comes from.', 'The surface area is two ___ plus one ___.',
    ['cylinder', 'circumference', 'lateral area', 'exact answer'], 'Forgetting the two circular bases in the surface area.', FILL, 'full',
    [('M', 'measure-cylinder-volume', 1, 7), ('M', 'measure-cylinder-surface', 1, 7)], '', 'Volume: V = πr²h. Surface area: S = 2πr² + 2πrh.'),
  L('Pyramids and Cones', 'G-GMD.A.3', 'find the volume of pyramids and cones.',
    'Students will explain how a pyramid or cone compares to a prism or cylinder with the same base and height.', 'The volume is ___ of the matching prism or cylinder.',
    ['pyramid', 'cone', 'base', 'height'], 'Leaving out the one-third.', EXPLORE, 'full',
    [('M', 'measure-pyramid-volume', 1, 7), ('M', 'measure-cone-volume', 1, 7)], '', 'A pyramid or cone holds one-third as much as the prism or cylinder with the same base and height.'),
  L('Spheres', 'G-GMD.A.3', 'find the volume and surface area of spheres.',
    'Students will explain the roles of the radius in each formula.', 'The radius is ___ in the volume formula and ___ in the surface area formula.',
    ['sphere', 'radius', 'surface area', 'volume', 'exact answer'], 'Using the diameter in place of the radius.', FILL, 'full',
    [('M', 'measure-sphere-volume', 1, 7), ('M', 'measure-sphere-surface', 1, 7)], '', 'Volume: V = (4/3)πr³. Surface area: S = 4πr².'),
  L('Nets and Composite Solids', 'G-GMD.B.4, G-MG.A.1', 'use a net to find surface area and add volumes to find the volume of a composite solid.',
    'Students will describe how a net folds into a solid and name its faces.', 'The net has ___ faces; the faces that match are ___.',
    ['net', 'composite solid', 'surface area', 'volume'], 'Counting a hidden face twice or leaving one out.', EXPLORE, 'full',
    [('M', 'measure-net-surface', 1, 7), ('M', 'measure-composite-volume', 1, 7)], '', 'The area of a net is the surface area. Split a composite solid into simple solids, find each volume and add.'),
  L('Missing Dimensions from Volume', 'G-GMD.A.3, A-CED.A.4', 'find a missing height of a prism or cylinder from its volume.',
    'Students will explain how to rearrange the volume formula to find a missing dimension.', 'To find the height I ___ the volume by ___.',
    ['volume', 'height', 'base'], 'Dividing by only one dimension of the base.', FILL, 'full',
    [('M', 'measure-prism-height', 1, 7), ('M', 'measure-cylinder-height', 1, 7)], '', 'Set the volume formula equal to the given volume, then solve for the unknown dimension.'),
 ]),
]

DAYS_TOTAL = 180
# formula-reference lessons print with pre-filled notes (students annotate rather than copy)
for _u, _t, _ls in UNITS:
    for _l in _ls:
        if _l['title'] in ('Special Right Triangles', 'Rotations', 'Arc Length and Sector Area', 'Spheres'):
            _l['style'] = PRE
for _u, _t, _ls in UNITS:
    for _l in _ls:
        _l['vocab_raw'] = _l['vocab']
        _l['vocab'] = [w.split('|')[0] for w in _l['vocab_raw']]   # words as students see them ('tangent|circle' is the circle meaning of 'tangent')
ID = lambda u, n: 'U%d-L%d' % (u, n)


def standards_of(lessons):
    seen = []
    for l in lessons:
        for s in [x.strip() for x in l['std'].split(',')]:
            if s and s not in seen:
                seen.append(s)
    return ', '.join(seen)


def objective(l):
    return 'Students will be able to ' + l['obj']


def build():
    days = []

    def add(**k):
        days.append(k)

    # launch + diagnostic
    add(day_type='Launch', lesson_id='LAUNCH-1', unit=None, unit_title='Course Launch', title='Welcome, Norms, and Classroom Routines',
        standards='SMP 1–8', content_objective='Students will be able to establish classroom norms, routines, and expectations for Do Nows, notes, and exit tickets.',
        language_objective='Students will describe orally their mathematical strengths and goals using complete sentences.',
        sentence_frame='One thing I am good at in math is ___. This year I want to ___.', key_vocabulary='', common_misconception='', notes_style='',
        do_now_strategy='None / routine', dn=[], sp=[], cov=[])
    add(day_type='Diagnostic', lesson_id='LAUNCH-2', unit=None, unit_title='Course Launch', title='Diagnostic Pre-Assessment',
        standards='SMP 1–8', content_objective='Students will be able to show what they already know about angles, lengths, and algebra skills needed for Geometry.',
        language_objective='Students will rate their confidence on each skill and explain one skill they want to strengthen.',
        sentence_frame='I feel confident about ___. I want to practice ___.', key_vocabulary='', common_misconception='', notes_style='',
        do_now_strategy='Readiness check: skills needed for Geometry', dn=[], sp=[], cov=[])
    add(day_type='Launch', lesson_id='LAUNCH-3', unit=None, unit_title='Course Launch', title='Math Mindset and Problem-Solving Launch Task',
        standards='SMP 1–8', content_objective='Students will be able to use a problem-solving routine to work through a challenging task with a group.',
        language_objective='Students will explain their group strategy using complete sentences and mathematical vocabulary.',
        sentence_frame='Our strategy was ___. It worked (or did not work) because ___.', key_vocabulary='', common_misconception='', notes_style='',
        do_now_strategy='None / routine', dn=[], sp=[], cov=[])

    unit_plans = []
    for (u, utitle, lessons) in UNITS:
        n = len(lessons)
        ids = [ID(u, i + 1) for i in range(n)]
        seq = []   # list of dicts describing each day in the unit
        done = []
        for i, l in enumerate(lessons):
            seq.append(('Lesson', i))
            done.append(i)
            if (i + 1) % 2 == 0 and i + 1 < n:
                seq.append(('Practice', list(done[-2:])))
            if i + 1 == (n + 1) // 2 + 1 and n >= 6:
                seq.append(('Quiz', list(done)))
        if n % 2 == 1:
            seq.append(('Practice', [n - 2, n - 1]))
        seq.append(('Review', None)); seq.append(('Assessment', None)); seq.append(('Flex', None))
        unit_plans.append([u, utitle, lessons, ids, seq])

    base = 3 + sum(len(p[4]) for p in unit_plans) + 2 + 4 + 1     # launch + units + semester (2 review + exam) ... + final (4 review + exam)
    extra = DAYS_TOTAL - base - 1                                    # spare days -> mixed practice (the +1 above is the semester exam)
    # distribute extra mixed-practice days over the units, longest first
    order = sorted(range(len(unit_plans)), key=lambda k: -len(unit_plans[k][4]))
    k = 0
    while extra > 0:
        unit_plans[order[k % len(order)]][4].insert(len(unit_plans[order[k % len(order)]][4]) - 3, ('Mixed', None))
        extra -= 1; k += 1

    unit_ranges = []
    for pi, (u, utitle, lessons, ids, seq) in enumerate(unit_plans):
        total = len(seq)
        start = len(days) + 1
        practice_no = 0; mixed_no = 0
        prev_lesson_id = None
        for di, (kind, ref) in enumerate(seq):
            ud = '%d of %d' % (di + 1, total)
            uset = 'unit'
            if kind == 'Lesson':
                l = lessons[ref]; lid = ids[ref]
                prior_unit = [ID(unit_plans[pi - 1][0], len(unit_plans[pi - 1][2]))] if pi > 0 else []
                spiral = []
                if pi > 0:
                    spiral = [ID(unit_plans[pi - 1][0], len(unit_plans[pi - 1][2]) - 1), ID(unit_plans[pi - 1][0], len(unit_plans[pi - 1][2]))]
                    spiral = spiral[-1:] if ref else spiral[-1:]
                dn = [prev_lesson_id] if prev_lesson_id else (prior_unit if prior_unit else [])
                strat = 'Retrieval: previous lesson' if prev_lesson_id else ('Spiral review (earlier units)' if prior_unit else 'Retrieval: previous lessons (spiral pool not yet available)')
                add(day_type='Lesson', lesson_id=lid, unit=u, unit_title=utitle, unit_day=ud, title=l['title'], standards=l['std'],
                    content_objective=objective(l), language_objective=l['lang'], sentence_frame=l['frame'], key_vocabulary=', '.join(l['vocab']),
                    common_misconception=l['mis'], notes_style=l['style'], do_now_strategy=strat, dn=dn, sp=spiral if ref else [], cov=[lid])
                prev_lesson_id = lid
            elif kind in ('Practice', 'Mixed'):
                if kind == 'Practice':
                    practice_no += 1; c = [ids[i] for i in ref]
                    lid = 'U%d-P%d' % (u, practice_no)
                    title = 'Practice Day: ' + ' & '.join(lessons[i]['title'] for i in ref)
                else:
                    mixed_no += 1; c = ids[:]
                    lid = 'U%d-M%d' % (u, mixed_no)
                    title = 'Mixed Practice: Unit %d' % u
                add(day_type='Practice', lesson_id=lid, unit=u, unit_title=utitle, unit_day=ud, title=title, standards=standards_of([lessons[ids.index(x)] for x in c]),
                    content_objective='Students will be able to apply skills from %s to solve problems of increasing complexity and analyze errors.' % ', '.join(c),
                    language_objective='Students will explain orally to a partner the strategy used to solve a problem and critique a sample error using unit vocabulary.',
                    sentence_frame='I solved this by ___ because ___. The error in this work is ___.', key_vocabulary=', '.join(dict.fromkeys(w for x in c for w in lessons[ids.index(x)]['vocab'])),
                    common_misconception='', notes_style='', do_now_strategy='Retrieval: lessons being practiced', dn=c[-2:], sp=[], cov=c)
            elif kind == 'Quiz':
                c = [ids[i] for i in ref]
                add(day_type='Quiz', lesson_id='U%d-Q' % u, unit=u, unit_title=utitle, unit_day=ud, title='Unit %d Quiz (Lessons %s)' % (u, 'L1–L%d' % len(c)),
                    standards=standards_of([lessons[i] for i in ref]), content_objective='Students will be able to demonstrate understanding of %s on a mid-unit quiz.' % ', '.join(c),
                    language_objective='Students will read and interpret word problems independently and justify at least one answer in writing.',
                    sentence_frame='My answer is reasonable because ___.', key_vocabulary=', '.join(dict.fromkeys(w for i in ref for w in lessons[i]['vocab']))[:400], common_misconception='',
                    notes_style='', do_now_strategy='Light confidence warm-up', dn=c[-1:], sp=[], cov=c)
            else:
                c = ids[:]
                vocab = ', '.join(list(dict.fromkeys(w for l in lessons for w in l['vocab']))[:10])
                common = dict(day_type=kind, unit=u, unit_title=utitle, unit_day=ud, standards=standards_of(lessons), key_vocabulary=vocab, common_misconception='', notes_style='', sp=[], cov=c)
                if kind == 'Review':
                    add(lesson_id='U%d-R' % u, title='Unit %d Review' % u, content_objective='Students will be able to review and synthesize all Unit %d skills (%s) and identify areas for further study.' % (u, utitle),
                        language_objective='Students will summarize in writing the key ideas of Unit %d and explain one problem type to a peer.' % u,
                        sentence_frame='The most important idea in this unit is ___. To solve ___ problems, I ___.', do_now_strategy='Spiral review (earlier units)', dn=[], **common)
                elif kind == 'Assessment':
                    add(lesson_id='U%d-T' % u, title='Unit %d Test: %s' % (u, utitle), content_objective='Students will be able to demonstrate mastery of Unit %d: %s.' % (u, utitle),
                        language_objective='Students will justify solutions in writing using precise unit vocabulary.', sentence_frame='I know my answer is correct because ___.',
                        do_now_strategy='None / calm start', dn=[], **common)
                else:
                    add(lesson_id='U%d-F' % u, title='Unit %d Flex: Test Corrections, Reteach & Enrichment' % u,
                        content_objective='Students will be able to correct errors from the Unit %d test and strengthen understanding through targeted reteaching or enrichment.' % u,
                        language_objective='Students will explain in writing the error made on a test item and the correct reasoning.',
                        sentence_frame='My error was ___. The correct approach is ___ because ___.', do_now_strategy='Spiral review targeting most-missed items', dn=[], **common)
        unit_ranges.append((u, utitle, start, len(days), ids))
        # semester review / exam after Unit 5
        if u == 5:
            cov = [i for (uu, _, _, _, ids2) in unit_ranges for i in ids2]
            for k2, (title, covs) in enumerate([('Semester Review: Units 1–3 (Foundations, Angles, Congruence)', [i for i in cov if i.startswith(('U1-', 'U2-', 'U3-'))]),
                                                 ('Semester Review: Units 4–5 (Triangle Relationships, Similarity)', [i for i in cov if i.startswith(('U4-', 'U5-'))])]):
                add(day_type='Exam Review', lesson_id='SEM-%d' % (k2 + 1), unit=None, unit_title='Semester 1 Exam', title=title, standards='G-CO, G-SRT, G-GPE',
                    content_objective='Students will be able to review and practice key skills from %s and identify personal areas for growth.' % title.split(': ')[1].split(' (')[0],
                    language_objective='Students will explain to a partner how to solve a review problem using precise unit vocabulary.', sentence_frame='To solve this type of problem, I ___ because ___.',
                    key_vocabulary='', common_misconception='', notes_style='', do_now_strategy='Cumulative spiral review', dn=covs[-2:], sp=[], cov=covs)
            add(day_type='Exam', lesson_id='SEM-3', unit=None, unit_title='Semester 1 Exam', title='Semester Exam (Units 1–5)', standards='G-CO, G-SRT, G-GPE',
                content_objective='Students will be able to demonstrate mastery of Geometry content from Units 1–5 on a cumulative semester exam.',
                language_objective='Students will justify solutions in writing using precise mathematical vocabulary.', sentence_frame='I know my answer is correct because ___.',
                key_vocabulary='', common_misconception='', notes_style='', do_now_strategy='None / routine', dn=[], sp=[], cov=cov)

    allc = [i for (_, _, _, _, ids2) in unit_ranges for i in ids2]
    groups = [('Final Review: Foundations, Angles, and Congruence (Units 1–3)', ('U1-', 'U2-', 'U3-')), ('Final Review: Triangles and Similarity (Units 4–5)', ('U4-', 'U5-')),
              ('Final Review: Right Triangles, Quadrilaterals, and Transformations (Units 6–8)', ('U6-', 'U7-', 'U8-')), ('Final Review: Circles and Measurement (Units 9–10)', ('U9-', 'U10-'))]
    for k2, (title, pre) in enumerate(groups):
        covs = [i for i in allc if i.startswith(pre)]
        add(day_type='Exam Review', lesson_id='END-%d' % (k2 + 1), unit=None, unit_title='Final Exam', title=title, standards='G-CO, G-SRT, G-C, G-GPE, G-GMD',
            content_objective='Students will be able to review and practice key skills from %s and identify personal areas for growth.' % title.split(': ')[1],
            language_objective='Students will explain to a partner how to solve a review problem using precise unit vocabulary.', sentence_frame='To solve this type of problem, I ___ because ___.',
            key_vocabulary='', common_misconception='', notes_style='', do_now_strategy='Cumulative spiral review', dn=covs[-2:], sp=[], cov=covs)
    add(day_type='Exam', lesson_id='END-5', unit=None, unit_title='Final Exam', title='Final Exam (Cumulative)', standards='G-CO, G-SRT, G-C, G-GPE, G-GMD',
        content_objective='Students will be able to demonstrate mastery of Geometry content on a cumulative final exam.',
        language_objective='Students will justify solutions in writing using precise mathematical vocabulary.', sentence_frame='I know my answer is correct because ___.',
        key_vocabulary='', common_misconception='', notes_style='', do_now_strategy='None / routine', dn=[], sp=[], cov=allc)

    out = []
    for i, d in enumerate(days):
        n = i + 1
        rec = dict(day=n, quarter=min(4, (n - 1) * 4 // DAYS_TOTAL + 1), week=(n - 1) // 5 + 1, unit=d['unit'], unit_title=d['unit_title'], unit_day=d.get('unit_day', ''),
                   day_type=d['day_type'], lesson_id=d['lesson_id'], title=d['title'], standards=d['standards'], content_objective=d['content_objective'],
                   language_objective=d['language_objective'], sentence_frame=d['sentence_frame'], key_vocabulary=d['key_vocabulary'], common_misconception=d['common_misconception'],
                   notes_style=d['notes_style'], do_now_strategy=d['do_now_strategy'], do_now_source_ids=d['dn'], spiral_review_ids=d['sp'], lessons_covered=d['cov'])
        out.append(rec)
    units = [dict(unit=u, title=t, start_day=s, end_day=e, total_days=e - s + 1, lesson_ids=ids) for (u, t, s, e, ids) in unit_ranges]
    return out, units


def main():
    days, units = build()
    assert len(days) == DAYS_TOTAL, len(days)
    scope = dict(meta=dict(course='Geometry', total_days=DAYS_TOTAL, standards_framework='Common Core State Standards (CCSS-M)', version='0.1-draft',
                           diagnostic_label='Skills needed for Geometry (angles, lengths, equations)',
                           notes='DRAFT pacing written for the Geometry generators; edit geometry_scope_sequence.json or scripts/build_geometry_planner.py and rerun. One record per instructional day.'),
                 day_types=algebra['day_types'], units=units, days=days)
    with open(os.path.join(D, 'geometry_scope_sequence.json'), 'w', encoding='utf-8') as f:
        json.dump(scope, f, ensure_ascii=False, indent=1); f.write('\n')
    compact = json.loads(json.dumps(scope))
    with open(os.path.join(D, 'scope-geometry.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generated by scripts/build_geometry_planner.py. Do not edit by hand. */\n')
        f.write('window.MKPLAN_SCOPE_GEOMETRY = ' + json.dumps(compact, ensure_ascii=False, separators=(',', ':')) + ';\n')

    lessons = {}
    for (u, _, ls) in UNITS:
        for i, l in enumerate(ls):
            entry = dict(cover=l['cover'], skills=[list(s) for s in l['skills']])
            if l['note']:
                entry['note'] = l['note']
            lessons[ID(u, i + 1)] = entry
    lessons['LAUNCH-2'] = dict(cover='full', skills=[['B', 'segment-addition', 1, 2], ['B', 'angle-addition', 1, 2], ['A', 'complementary-angles', 1, 1], ['A', 'vertical-angles', 1, 1], ['T', 'triangle-interior-sum', 1, 1], ['B', 'midpoint', 1, 1]])
    with open(os.path.join(D, 'lesson-skills-geometry.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generated by scripts/build_geometry_planner.py. Lesson id -> verified Geometry skills and how fully they cover the objective. */\n')
        f.write('window.MKPLAN_SKILLS_GEOMETRY = ' + json.dumps(dict(SETS=SETS, UNIT_SET=UNIT_SET, lessons=lessons), ensure_ascii=False, indent=1) + ';\n')

    # glossary + key ideas
    words = {}
    for (u, _, ls) in UNITS:
        for l in ls:
            for w in l['vocab_raw']:
                key = w.lower().replace('|circle', '|u9')
                words[key] = V[w]
    ideas = {ID(u, i + 1): l['idea'] for (u, _, ls) in UNITS for i, l in enumerate(ls)}
    with open(os.path.join(D, 'notes-data-geometry.js'), 'w', encoding='utf-8') as f:
        f.write('/* Generated by scripts/build_geometry_planner.py. Definitions and key ideas for the Geometry planner (used only when the course is Geometry). */\n')
        f.write('window.MKPLAN_GEOMETRY_NOTES = ' + json.dumps(dict(glossary=words, ideas=ideas), ensure_ascii=False, indent=1) + ';\n')
    print('geometry: %d days, %d units, %d lessons, %d words' % (len(days), len(units), len(ideas), len(words)))
    from collections import Counter
    print(Counter(d['day_type'] for d in days))


if __name__ == '__main__':
    main()
