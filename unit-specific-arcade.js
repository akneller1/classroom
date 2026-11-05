(function(root){'use strict';
/* Unit-specific Math Arcade games.
   Original games (Algebra 1, Geometry, Algebra 2): [course, unit, game, title, description].
   Bank games (newer courses): each reuses one of the arcade engines (its scene and motion) with questions from
   that unit's own question bank: single-answer multiple choice only, so every answer is checked against the key.
   The arcade page (artifacts/math-arcade/index.html) loads this file too and reads MK_UNIT_GAMES. */
var MS=['Remedial','Standard','Advanced'],HS=['CP2','CP1','Honors'];
var G=function(engine,course,unit,title,courseName,topic,intro,added){return {engine:engine,bank:{course:course,unit:unit,skills:[]},levels:/^(math6|prealgebra7?)$/.test(course)?MS:HS,title:title,course:courseName,topic:topic,intro:intro,added:added||'2026-11-05'};};
var UG={
 // 6th Grade
 'ratio-rocket-relay':G('rocket','math6','ratios-rates-percent-proportions','Ratio Rocket Relay','6th Grade Math','Ratios, Rates, Percent and Proportions','Use ratios, unit rates and percents to fuel each stage of the relay rocket.'),
 'decimal-gate-dash':G('portal','math6','fractions-decimals-operations','Decimal Gate Dash','6th Grade Math','Operations with Fractions and Decimals','Divide fractions and compute with decimals to send the energy ball through each gate.'),
 'number-line-crossing':G('inequality','math6','rational-numbers','Number Line Lava Crossing','6th Grade Math','Rational Numbers','Compare, order and locate positive and negative numbers to cross the lava.'),
 'equation-launch':G('rocket','math6','expressions-equations','Equation Launch Pad','6th Grade Math','Expressions and Equations','Evaluate expressions and solve one-step equations to fuel a rocket for its trip to the space station.'),
 'inequality-stepping-stones':G('inequality','math6','inequalities','Inequality Stepping Stones','6th Grade Math','Inequalities','Write, solve and graph inequalities to find the safe stones across the lava.'),
 'polygon-explorer':G('mirror','math6','geometry','Polygon Explorer','6th Grade Math','Geometry','Find areas, volumes and coordinates to guide the explorer through the mirror hall.'),
 'statistic-sharpshooter':G('cannon','math6','data-displays','Statistic Sharpshooter','6th Grade Math','Data Displays','Read dot plots, histograms and box plots and find centers and spreads to hit each target.'),
 // Pre-Algebra (7th)
 'integer-launch-control':G('rocket','prealgebra7','algebraic-expressions-integers','Integer Launch Control','Pre-Algebra (7th)','Algebraic Expressions and Integers','Evaluate expressions and compute with integers to clear each launch check.'),
 'one-step-lava-hop':G('inequality','prealgebra7','one-step-equations-inequalities','One-Step Lava Hop','Pre-Algebra (7th)','Solving One-Step Equations and Inequalities','Solve one-step equations and inequalities to hop across the lava.'),
 'decimal-docking':G('rocket','prealgebra7','decimals-equations','Decimal Docking Mission','Pre-Algebra (7th)','Decimals and Equations','Estimate, use formulas and solve decimal equations to dock with the space station.'),
 'prime-factor-portals':G('portal','prealgebra7','factors-fractions-exponents','Prime Factor Portals','Pre-Algebra (7th)','Factors, Fractions, and Exponents','Factor, simplify fractions and use exponent rules to open each portal.'),
 'fraction-fusion-lab':G('laser','prealgebra7','operations-fractions','Fraction Fusion Lab','Pre-Algebra (7th)','Operations with Fractions','Compute with fractions and mixed numbers to lock the fusion lasers.'),
 'lava-bridge':G('inequality','prealgebra7','solving-equations-inequalities','Lava Bridge Builder','Pre-Algebra (7th)','Solving Equations and Inequalities','Solve two-step equations and inequalities to lay safe stones across the lava river.'),
 'proportion-cannon':G('cannon','prealgebra7','ratios-proportions-percentages','Proportion Cannon','Pre-Algebra (7th)','Ratios, Proportions, and Percentages','Use rates, proportions and percents to aim the cannon at each tower.'),
 'slope-laser-lab':G('laser','prealgebra7','linear-functions-graphing','Slope Laser Lab','Pre-Algebra (7th)','Linear Functions and Graphing','Find slopes, function rules and intersections to line up the lasers.'),
 'symmetry-mirror-maze':G('mirror','prealgebra7','spatial-thinking','Symmetry Mirror Maze','Pre-Algebra (7th)','Spatial Thinking','Use angles, polygons, translations, reflections and rotations to guide the explorer.'),
 'cargo-capacity-launch':G('rocket','prealgebra7','area-volume','Cargo Capacity Launch','Pre-Algebra (7th)','Area and Volume','Find areas, surface areas and volumes to load the rocket and launch it.'),
 'pythagoras-cannon':G('cannon','prealgebra7','right-triangles-algebra','Pythagoras Cannon','Pre-Algebra (7th)','Right Triangles in Algebra','Use square roots, the Pythagorean Theorem and trig ratios to aim at each tower.'),
 'probability-portals':G('portal','prealgebra7','data-analysis-probability','Probability Portals','Pre-Algebra (7th)','Data Analysis and Probability','Read data displays and find probabilities to open each portal.'),
 'growth-curve-lasers':G('laser','prealgebra7','nonlinear-functions-polynomials','Growth Curve Lasers','Pre-Algebra (7th)','Nonlinear Functions and Polynomials','Extend patterns, graph nonlinear functions and work with polynomials to lock each beam.'),
 // Pre-Algebra (8th)
 'exponent-escape-velocity':G('rocket','prealgebra','real-numbers-exponents','Exponent Escape Velocity','Pre-Algebra (8th)','Real Numbers and Exponents','Work with rational and irrational numbers and exponents to reach escape velocity.'),
 'equation-lava-path':G('inequality','prealgebra','equations-expressions','Equation Lava Path','Pre-Algebra (8th)','Equations and Expressions','Simplify exponent expressions and solve multi-step equations to cross the lava.'),
 'function-rule-gates':G('portal','prealgebra','linear-functional-relationships','Function Rule Gates','Pre-Algebra (8th)','Linear and Functional Relationships','Write, graph and interpret functions to open each gate.'),
 'system-lasers':G('laser','prealgebra','systems-linear-equations','Laser Lock: Systems','Pre-Algebra (8th)','Systems of Linear Equations','Two laser beams are lines. Find where they cross to lock onto each security node.'),
 'best-fit-lasers':G('laser','prealgebra','patterns-bivariate-data','Best-Fit Beam Lab','Pre-Algebra (8th)','Patterns and Bivariate Data','Read scatter plots, lines of best fit and two-way tables to aim the beams.'),
 'transformation-mirror-maze':G('mirror','prealgebra','congruence-similarity','Transformation Mirror Maze','Pre-Algebra (8th)','Congruence and Similarity','Translate, reflect, rotate and dilate to guide the explorer through the mirrors.'),
 'pythagorean-cannon':G('cannon','prealgebra','geometry-applications','Pythagorean Cannon','Pre-Algebra (8th)','Geometry','Use the Pythagorean Theorem, distance and volume to aim at each tower.'),
 // Precalculus
 'interval-lava-bridge':G('inequality','precalculus','equations-inequalities','Interval Lava Bridge','Precalculus','Equations and Inequalities','Solve equations and inequalities and write intervals to cross the lava.'),
 'function-gates':G('portal','precalculus','functions','Function Gates','Precalculus','Functions','Evaluate, compose, shift and invert functions to route the energy ball through each gate.'),
 'orbit-gates':G('portal','precalculus','conics','Conic Orbit Gates','Precalculus','Conics','Find centers, foci, vertices and equations of conics to steer through each orbit gate.'),
 'radian-cannon':G('cannon','precalculus','trigonometric-functions','Radian Cannon','Precalculus','Trigonometric Functions','Use radians, the unit circle and trig graphs to aim at each tower.'),
 'law-of-sines-lasers':G('laser','precalculus','general-triangle-trigonometry','Triangulation Lasers','Precalculus','Trigonometry of General Triangles','Use the Laws of Sines and Cosines to triangulate each target with two beams.'),
 'matrix-mission-control':G('rocket','precalculus','matrices','Matrix Mission Control','Precalculus','Matrices','Add, multiply and row-reduce matrices to clear each launch stage.'),
 'vector-navigator':G('mirror','precalculus','vectors','Vector Navigator','Precalculus','Vectors','Use vectors and complex numbers to steer the explorer through the hall.'),
 'odds-gates':G('portal','precalculus','probability','Odds Gates','Precalculus','Probability','Find probabilities, odds and counts to open each gate.'),
 // Calculus
 'function-review-gates':G('portal','calculus','precalculus-review','Function Review Gates','Calculus','Precalculus Review','Factor, use exponentials, logarithms and the unit circle to open each gate.'),
 'limit-lava-bridge':G('inequality','calculus','limits-continuity','Limit Lava Bridge','Calculus','Limits and Continuity','Approach the edge: find limits and check continuity to cross the lava.'),
 'tangent-cannon':G('cannon','calculus','derivatives','Tangent Line Cannon','Calculus','Derivatives','Every shot follows a tangent line. Find derivatives and slopes to hit each tower.'),
 'optimization-rocket':G('rocket','calculus','applications-derivatives','Optimization Rocket','Calculus','Applications of Derivatives','Use extrema, concavity and related rates to fly the rocket at its best.'),
 'riemann-lasers':G('laser','calculus','antiderivatives-definite-integrals','Riemann Laser Grid','Calculus','Antiderivatives and Definite Integrals','Find antiderivatives and Riemann sums to lock each laser.'),
 'accumulation-gates':G('portal','calculus','fundamental-theorem-calculus','Accumulation Gates','Calculus','The Fundamental Theorem of Calculus','Use accumulation functions and the Fundamental Theorem to open each gate.'),
 'displacement-explorer':G('mirror','calculus','applications-integrals','Displacement Explorer','Calculus','Applications of Integrals','Use net change, average value, displacement and area to guide the explorer.'),
 'growth-decay-bridge':G('inequality','calculus','differential-equations','Growth and Decay Bridge','Calculus','Differential Equations','Verify solutions, read slope fields and separate variables to cross the lava.'),
 'ap-exam-launch':G('rocket','calculus','ap-review','AP Exam Launch','Calculus','AP Calculus Review','Mixed AP review: limits, derivatives, integrals and differential equations to reach orbit.')
};
['equation-launch','lava-bridge','system-lasers','function-gates','tangent-cannon'].forEach(function(k){UG[k].added='2026-11-05';});
root.MK_UNIT_GAMES=UG;
if(!root.LIBRARY||!Array.isArray(root.LIBRARY.courses))return;
var entries=[
 ['algebra','expressions-equations','rocket','Equation Rocket Rescue','Solve equations to fuel a rocket and reach rescue stations.'],
 ['algebra','inequalities','inequality','Inequality Island','Choose inequality boundaries to make safe paths across a lava island.'],
 ['algebra','systems-of-equations','laser','Laser Intersection','Solve systems to pinpoint where laser beams meet.'],
 ['algebra','quadratics','catapult','Castle Catapult','Identify roots, vertex and castle height for ten quadratic trajectories; six direct hits crumble the enemy castle.'],
 ['geometry','transformations','mirror','Mirror Maze','Use reflection, rotation and translation rules to move an explorer.'],
 ['geometry','right-triangles-trigonometry','cannon','Trig Cannon','Use right-triangle tangent and angles to aim at distant towers.'],
 ['algebra2','functions-transformations','portal','Function Portal','Evaluate transformed quadratic functions to route a ball through energy portals.']
];
Object.keys(UG).forEach(function(k){var g=UG[k];entries.push([g.bank.course,g.bank.unit,k,g.title,g.intro,g.added]);});
entries.forEach(function(e){
 var course=root.LIBRARY.courses.find(function(c){return c.id===e[0]});
 var unit=course&&course.units.find(function(u){return u.id===e[1]});
 if(!unit)return;
 unit.artifacts=unit.artifacts||[];
 var path='artifacts/math-arcade/index.html?game='+e[2];
 if(unit.artifacts.some(function(a){return a.path===path}))return;
 unit.artifacts.push({title:e[3],path:path,thumb:'thumbs/arcade-'+e[2]+'.svg',type:'Game',bankFormat:'topic-games',unitSpecific:true,description:e[4],topics:[e[1].replace(/-/g,' '),'Interactive math game'],added:(e[5]||'2026-10-31')});
});
})(window);
