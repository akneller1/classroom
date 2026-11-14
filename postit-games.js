/* Reviewed Claude games. Keep these unit placements shared by runtime and release builds. */
(function(root){
'use strict';
var games=[
 {
  "id": "a1-equation-steps",
  "course": "algebra",
  "units": [
   "expressions-equations"
  ],
  "title": "Equation Step Stack",
  "description": "Stack the steps of each solution in the right order.",
  "topics": [
   "A.REI.1, A.REI.3",
   "inverse operations",
   "distributing",
   "variables on both sides",
   "clearing fractions"
  ]
 },
 {
  "id": "a1-factor-builder",
  "course": "algebra",
  "units": [
   "factoring-zero-product"
  ],
  "title": "Factor Builder",
  "description": "Drag number cards into the factors so they multiply back to the polynomial.",
  "topics": [
   "A.SSE.2, A.SSE.3a",
   "factoring trinomials",
   "a ≠ 1",
   "greatest common factor",
   "difference of squares"
  ]
 },
 {
  "id": "a1-growth-sort",
  "course": "algebra",
  "units": [
   "exponential-functions"
  ],
  "title": "Linear or Exponential?",
  "description": "Sort tables, equations, graphs and stories by how they grow.",
  "topics": [
   "F.LE.1–2, F.IF.8b",
   "equal differences vs equal ratios",
   "growth and decay",
   "percent change"
  ]
 },
 {
  "id": "a1-line-labeler",
  "course": "algebra",
  "units": [
   "linear-equations-slope"
  ],
  "title": "Line Labeler",
  "description": "Label each line on the graph with its equation.",
  "topics": [
   "F.IF.7a, A.CED.2, F.LE.2",
   "slope-intercept, standard and point-slope form",
   "horizontal and vertical lines"
  ]
 },
 {
  "id": "a1-polynomial-groups",
  "course": "algebra",
  "units": [
   "polynomials-factoring"
  ],
  "title": "Polynomial Groups",
  "description": "Find the groups of expressions that are the same polynomial in disguise.",
  "topics": [
   "A.APR.1, A.SSE.2",
   "combining like terms",
   "adding and subtracting polynomials",
   "multiplying binomials"
  ]
 },
 {
  "id": "a2-complex-groups",
  "course": "algebra2",
  "units": [
   "quadratic-functions-complex-numbers"
  ],
  "title": "Complex Number Groups",
  "description": "Group the expressions that equal the same complex number.",
  "topics": [
   "N.CN.1–3",
   "powers of i",
   "adding, subtracting, multiplying and dividing complex numbers",
   "conjugates"
  ]
 },
 {
  "id": "a2-end-behavior",
  "course": "algebra2",
  "units": [
   "polynomial-functions"
  ],
  "title": "End Behavior Sort",
  "description": "Where do the ends of the graph go? Sort each polynomial.",
  "topics": [
   "F.IF.7c, A.APR.3",
   "degree and leading coefficient",
   "end behavior",
   "factored form",
   "reading graphs"
  ]
 },
 {
  "id": "a2-log-lineup",
  "course": "algebra2",
  "units": [
   "exponential-logarithmic-functions"
  ],
  "title": "Logarithm Line-Up",
  "description": "Order the logs and powers without a calculator.",
  "topics": [
   "F.LE.4, F.BF.5",
   "evaluating logarithms",
   "negative and fractional values",
   "estimating logs",
   "log properties"
  ]
 },
 {
  "id": "a2-sequence-snap",
  "course": "algebra2",
  "units": [
   "sequences-series"
  ],
  "title": "Sequence Snap",
  "description": "Snap the next term of the sequence before it falls.",
  "topics": [
   "F.BF.2, F.LE.2",
   "arithmetic and geometric sequences",
   "negative and fractional ratios",
   "recursive rules"
  ]
 },
 {
  "id": "a2-transform-match",
  "course": "algebra2",
  "units": [
   "functions-transformations"
  ],
  "title": "Transformation Match",
  "description": "Match each transformed function to its graph or description.",
  "topics": [
   "F.BF.3, F.IF.7",
   "shifts, reflections and stretches of x², |x|, √x, x³ and 2ˣ",
   "inside vs outside changes"
  ]
 },
 {
  "id": "g1-number-bonds",
  "course": "grade1",
  "units": [
   "add-subtract-20"
  ],
  "title": "Number Bond Builder",
  "description": "Pick the cards that add up to the target number.",
  "topics": [
   "1.OA.6",
   "make ten",
   "sums to 20",
   "meaning of the equal sign"
  ]
 },
 {
  "id": "g1-number-lineup",
  "course": "grade1",
  "units": [
   "count-120",
   "compare-numbers"
  ],
  "title": "Number Line-Up",
  "description": "Put the number cards in order.",
  "topics": [
   "1.NBT.1, 1.NBT.3",
   "counting to 120",
   "comparing two-digit numbers"
  ]
 },
 {
  "id": "g1-shape-sorter",
  "course": "grade1",
  "units": [
   "shapes-equal-shares"
  ],
  "title": "Shape Sorter",
  "description": "Sort shapes by sides, corners and other attributes.",
  "topics": [
   "1.G.1, 2.G.1",
   "defining attributes",
   "sides and corners",
   "turned shapes are the same shape"
  ]
 },
 {
  "id": "g1-tens-ones",
  "course": "grade1",
  "units": [
   "tens-ones"
  ],
  "title": "Tens & Ones Match",
  "description": "Match each number to its tens and ones.",
  "topics": [
   "1.NBT.2–3",
   "tens and ones",
   "comparing digits",
   "regrouping ten ones as a ten"
  ]
 },
 {
  "id": "g2-coin-counter",
  "course": "grade2",
  "units": [
   "time-money"
  ],
  "title": "Coin Counter",
  "description": "Pick coins that make the amount exactly.",
  "topics": [
   "2.MD.8",
   "pennies, nickels, dimes, quarters, dollars",
   "counting on",
   "fewest coins"
  ]
 },
 {
  "id": "g2-equation-builder",
  "course": "grade2",
  "units": [
   "add-subtract-100"
  ],
  "title": "Equation Builder",
  "description": "Drag number cards into the boxes to make each equation true.",
  "topics": [
   "2.NBT.5, 2.OA.1, 1.OA.7",
   "add and subtract within 100",
   "unknowns in any position",
   "balanced equations"
  ]
 },
 {
  "id": "g2-place-value-groups",
  "course": "grade2",
  "units": [
   "place-value-1000"
  ],
  "title": "Place Value Groups",
  "description": "Find the cards that show the same number in different ways.",
  "topics": [
   "2.NBT.1, 2.NBT.3",
   "standard, expanded and word form",
   "hundreds, tens and ones",
   "zeros as placeholders"
  ]
 },
 {
  "id": "g2-skip-snap",
  "course": "grade2",
  "units": [
   "count-compare-1000",
   "odd-even-arrays"
  ],
  "title": "Skip-Count Snap",
  "description": "Snap up the cards that follow the counting rule before they fall.",
  "topics": [
   "2.OA.3, 2.NBT.2, 2.NBT.8",
   "even and odd",
   "skip-count by 5s, 10s, 100s",
   "10 or 100 more"
  ]
 },
 {
  "id": "g3-area-perimeter",
  "course": "grade3",
  "units": [
   "area",
   "perimeter-shapes"
  ],
  "title": "Area or Perimeter?",
  "description": "Sort the shapes by their area, their perimeter, or both.",
  "topics": [
   "3.MD.5–8",
   "area by counting squares and multiplying",
   "perimeter",
   "same area, different perimeter"
  ]
 },
 {
  "id": "g3-array-match",
  "course": "grade3",
  "units": [
   "multiplication-meaning"
  ],
  "title": "Array Match",
  "description": "Match each array or fact to its partner.",
  "topics": [
   "3.OA.1, 3.OA.6, 3.OA.7, 3.OA.5",
   "arrays",
   "repeated addition",
   "unknown factors",
   "break-apart (distributive) strategy"
  ]
 },
 {
  "id": "g3-fraction-line",
  "course": "grade3",
  "units": [
   "understanding-fractions",
   "equivalent-comparing-fractions"
  ],
  "title": "Fraction Number Line",
  "description": "Drop each fraction card on its point on the number line.",
  "topics": [
   "3.NF.2, 3.NF.3",
   "fractions on a number line",
   "whole numbers as fractions",
   "equivalent fractions"
  ]
 },
 {
  "id": "g3-round-up",
  "course": "grade3",
  "units": [
   "addition-subtraction-1000"
  ],
  "title": "Rounding Rush",
  "description": "Snap every number that rounds to the target.",
  "topics": [
   "3.NBT.1",
   "round to the nearest 10 or 100",
   "halfway numbers round up"
  ]
 },
 {
  "id": "g4-angle-lineup",
  "course": "grade4",
  "units": [
   "geometry-angles-symmetry"
  ],
  "title": "Angle Line-Up",
  "description": "Order the angles from smallest turn to biggest turn.",
  "topics": [
   "4.MD.5–6, 4.G.1",
   "angle as a turn",
   "acute, right, obtuse, straight",
   "longer rays don't make bigger angles"
  ]
 },
 {
  "id": "g4-area-model",
  "course": "grade4",
  "units": [
   "multiplication-strategies"
  ],
  "title": "Area Model Multiplier",
  "description": "Fill the area model with partial products, then the total.",
  "topics": [
   "4.NBT.5",
   "place value",
   "partial products",
   "area model",
   "4-digit × 1-digit and 2-digit × 2-digit"
  ]
 },
 {
  "id": "g4-equivalent-fractions",
  "course": "grade4",
  "units": [
   "fractions-equivalent-fractions"
  ],
  "title": "Equivalent Fraction Groups",
  "description": "Find the groups of fractions that are worth the same amount.",
  "topics": [
   "4.NF.1, 4.NF.5–6",
   "equivalent fractions",
   "fraction models",
   "tenths and hundredths as decimals"
  ]
 },
 {
  "id": "g4-prime-sprint",
  "course": "grade4",
  "units": [
   "factors-multiples-patterns"
  ],
  "title": "Prime Time Sprint",
  "description": "Sort each number fast: prime or composite?",
  "topics": [
   "4.OA.4",
   "factor pairs",
   "prime and composite numbers to 100",
   "square numbers have an odd number of factors"
  ]
 },
 {
  "id": "g5-decimal-lineup",
  "course": "grade5",
  "units": [
   "place-value-number-sense"
  ],
  "title": "Decimal Line-Up",
  "description": "Order the decimals from least to greatest.",
  "topics": [
   "5.NBT.3",
   "read, write and compare decimals to thousandths",
   "more digits doesn't mean bigger"
  ]
 },
 {
  "id": "g5-fraction-match",
  "course": "grade5",
  "units": [
   "fraction-addition-subtraction",
   "fraction-multiplication-division"
  ],
  "title": "Fraction Operation Match",
  "description": "Match each fraction problem to its answer.",
  "topics": [
   "5.NF.1, 5.NF.4, 5.NF.7",
   "add and subtract unlike denominators",
   "mixed numbers",
   "multiply and divide fractions"
  ]
 },
 {
  "id": "g5-point-plotter",
  "course": "grade5",
  "units": [
   "coordinate-plane-graphing"
  ],
  "title": "Point Plotter",
  "description": "Drop each ordered pair on its point.",
  "topics": [
   "5.G.1–2",
   "ordered pairs",
   "x first, then y",
   "points on the axes",
   "coordinates from rules"
  ]
 },
 {
  "id": "g5-target-expression",
  "course": "grade5",
  "units": [
   "numerical-expressions-patterns"
  ],
  "title": "Target Expression",
  "description": "Drag numbers (and operations) into the boxes to hit the target exactly.",
  "topics": [
   "5.OA.1–2",
   "order of operations",
   "parentheses",
   "writing and evaluating expressions"
  ]
 },
 {
  "id": "g6-data-designer",
  "course": "math6",
  "units": [
   "data-displays"
  ],
  "title": "Data Set Designer",
  "description": "Build a data set that has exactly the stats on the order.",
  "topics": [
   "6.SP.3, 6.SP.5",
   "mean, median, mode and range",
   "how one value changes a statistic"
  ]
 },
 {
  "id": "g6-expression-groups",
  "course": "math6",
  "units": [
   "expressions-equations"
  ],
  "title": "Equivalent Expression Groups",
  "description": "Group the expressions that are equal for every value of the variable.",
  "topics": [
   "6.EE.3–4",
   "distributive property",
   "combining like terms",
   "factoring out a GCF"
  ]
 },
 {
  "id": "g6-fdp-oddout",
  "course": "math6",
  "units": [
   "ratios-rates-percent-proportions"
  ],
  "title": "Fraction · Decimal · Percent Odd One Out",
  "description": "Three cards are worth the same. Find the impostor.",
  "topics": [
   "6.RP.3c, 6.NS",
   "fractions, decimals and percents",
   "common conversion mistakes"
  ]
 },
 {
  "id": "g6-integer-line",
  "course": "math6",
  "units": [
   "rational-numbers"
  ],
  "title": "Integer Number Line",
  "description": "Drop each card where its value lives on the number line.",
  "topics": [
   "6.NS.5–7",
   "integers and opposites",
   "absolute value",
   "rational numbers on the line"
  ]
 },
 {
  "id": "g6-ratio-table",
  "course": "math6",
  "units": [
   "ratios-rates-percent-proportions"
  ],
  "title": "Ratio Table Fill-In",
  "description": "Complete the ratio tables. Watch out for adding instead of multiplying!",
  "topics": [
   "6.RP.1–3",
   "equivalent ratios",
   "ratio tables",
   "unit rates",
   "multiplicative (not additive) reasoning"
  ]
 },
 {
  "id": "g7-equation-match",
  "course": "prealgebra7",
  "units": [
   "solving-equations-inequalities"
  ],
  "title": "Equation Solution Match",
  "description": "Match each equation or inequality to its solution.",
  "topics": [
   "7.EE.4",
   "two-step equations",
   "distributive property",
   "inequalities and the sign flip",
   "graphing solutions"
  ]
 },
 {
  "id": "g7-integer-drop",
  "course": "prealgebra7",
  "units": [
   "algebraic-expressions-integers"
  ],
  "title": "Integer Drop",
  "description": "Snap every expression that equals the target. Sign errors are everywhere!",
  "topics": [
   "7.NS.1–3",
   "add, subtract, multiply and divide integers and rational numbers",
   "sign rules"
  ]
 },
 {
  "id": "g7-probability-line",
  "course": "prealgebra7",
  "units": [
   "data-analysis-probability"
  ],
  "title": "Probability Line",
  "description": "Place each event on the probability line from impossible to certain.",
  "topics": [
   "7.SP.5–8",
   "probability from 0 to 1",
   "theoretical probability",
   "complements",
   "compound events"
  ]
 },
 {
  "id": "g7-proportional-sort",
  "course": "prealgebra7",
  "units": [
   "ratios-proportions-percentages"
  ],
  "title": "Proportional or Not?",
  "description": "Is it a proportional relationship? Sort equations, tables, graphs and stories.",
  "topics": [
   "7.RP.2",
   "constant of proportionality",
   "y = kx",
   "graphs through the origin",
   "tables with a constant ratio"
  ]
 },
 {
  "id": "g8-function-sort",
  "course": "prealgebra",
  "units": [
   "linear-functional-relationships"
  ],
  "title": "Function or Not?",
  "description": "Does every input have exactly one output? Sort fast.",
  "topics": [
   "8.F.1, 8.F.3",
   "definition of a function",
   "mapping diagrams",
   "vertical line test",
   "linear vs nonlinear"
  ]
 },
 {
  "id": "g8-irrational-drop",
  "course": "prealgebra",
  "units": [
   "real-numbers-exponents"
  ],
  "title": "Rational or Irrational?",
  "description": "Snap the numbers that fit the rule: rational, or irrational. The rule switches!",
  "topics": [
   "8.NS.1–2",
   "rational vs irrational",
   "perfect squares",
   "repeating decimals",
   "square roots and π"
  ]
 },
 {
  "id": "g8-pythagorean",
  "course": "prealgebra",
  "units": [
   "geometry-applications"
  ],
  "title": "Pythagorean Picker",
  "description": "Pick the side lengths that make a right triangle.",
  "topics": [
   "8.G.6–7",
   "a² + b² = c²",
   "missing hypotenuse or leg",
   "converse of the theorem",
   "irrational side lengths"
  ]
 },
 {
  "id": "g8-sci-lineup",
  "course": "prealgebra",
  "units": [
   "real-numbers-exponents"
  ],
  "title": "Scientific Notation Line-Up",
  "description": "Order very big and very small numbers.",
  "topics": [
   "8.EE.3–4",
   "scientific notation",
   "negative exponents",
   "comparing magnitudes",
   "multiplying and dividing in scientific notation"
  ]
 },
 {
  "id": "g8-slope-match",
  "course": "prealgebra",
  "units": [
   "linear-functional-relationships"
  ],
  "title": "Slope Match",
  "description": "Match each line to its slope or equation.",
  "topics": [
   "8.EE.5–6, 8.F.4",
   "slope as rise over run",
   "negative and fractional slopes",
   "y = mx + b from graphs, points and tables"
  ]
 },
 {
  "id": "geo-congruence-sort",
  "course": "geometry",
  "units": [
   "triangle-congruence"
  ],
  "title": "Congruence Criteria Sort",
  "description": "Read the markings. Which shortcut proves the triangles congruent, if any?",
  "topics": [
   "G.CO.7–8, G.SRT.5",
   "SSS, SAS, ASA, AAS, HL",
   "why SSA and AAA don't work",
   "shared sides and vertical angles"
  ]
 },
 {
  "id": "geo-quad-oddout",
  "course": "geometry",
  "units": [
   "quadrilaterals-polygons"
  ],
  "title": "Quadrilateral Odd One Out",
  "description": "Three quadrilaterals share a property. Which one doesn't?",
  "topics": [
   "G.CO.11, G.GPE.4",
   "parallelograms, rectangles, rhombuses, squares, trapezoids, kites",
   "diagonals",
   "symmetry"
  ]
 },
 {
  "id": "geo-transversal",
  "course": "geometry",
  "units": [
   "angles-parallel-lines"
  ],
  "title": "Parallel Lines Angle Fill",
  "description": "Fill in every angle around the transversal.",
  "topics": [
   "G.CO.9",
   "vertical angles",
   "linear pairs",
   "corresponding, alternate interior/exterior and same-side angles"
  ]
 },
 {
  "id": "geo-trig-builder",
  "course": "geometry",
  "units": [
   "right-triangles-trigonometry"
  ],
  "title": "Trig Ratio Builder",
  "description": "Build each trig ratio from the triangle's sides.",
  "topics": [
   "G.SRT.6–8",
   "sine, cosine and tangent",
   "opposite, adjacent, hypotenuse",
   "cofunctions",
   "tan = sin ÷ cos"
  ]
 },
 {
  "id": "geo-volume-lineup",
  "course": "geometry",
  "units": [
   "area-surface-area-volume"
  ],
  "title": "Volume Line-Up",
  "description": "Order the solids from least to greatest volume.",
  "topics": [
   "G.GMD.3",
   "volume of prisms, cylinders, pyramids, cones and spheres",
   "the ⅓ factor",
   "radius vs diameter"
  ]
 }
];
function add(course){
 games.filter(function(g){return g.course===course.id;}).forEach(function(g){
  g.units.forEach(function(id){
   var u=(course.units||[]).find(function(u){return u.id===id;});if(!u)return;
   var level=g.id==='g5-fraction-match'?(id==='fraction-multiplication-division'?3:0):0;
   var path='artifacts/postit-games/'+g.id+'/index.html#level='+level;
   if(u.artifacts.some(function(a){return a.path===path;}))return;
   u.artifacts.push({title:g.title,path:path,thumb:'artifacts/postit-games/'+g.id+'/thumb.jpg',type:'Game',bankFormat:'topic-games',gameMode:'Individual Review',description:'Individual Review: '+g.description,topics:g.topics,added:'2026-11-14'});
  });
 });return course;
}
root.MK_POSTIT_GAMES={games:games,add:add};
if(root.LIBRARY)(root.LIBRARY.courses||[]).forEach(add);
if(typeof module==='object'&&module.exports)module.exports={games:games,add:add};
})(typeof window==='object'?window:globalThis);
