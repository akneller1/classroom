(function(root){'use strict';
if(!root.LIBRARY||!Array.isArray(root.LIBRARY.courses))return;
var entries=[
 ['algebra','expressions-equations','rocket','Equation Rocket Rescue','Solve equations to fuel a rocket and reach rescue stations.'],
 ['algebra','inequalities','inequality','Inequality Island','Choose inequality boundaries to make safe paths across a lava island.'],
 ['algebra','systems-of-equations','laser','Laser Intersection','Solve systems to pinpoint where laser beams meet.'],
 ['algebra','quadratics','catapult','Castle Catapult','Identify roots, vertex and castle height for ten quadratic trajectories; six direct hits crumble the enemy castle.'],
 ['geometry','transformations','mirror','Mirror Maze','Use reflection, rotation and translation rules to move an explorer.'],
 ['geometry','right-triangles-trigonometry','cannon','Trig Cannon','Use right-triangle tangent and angles to aim at distant towers.'],
 ['algebra2','functions-transformations','portal','Function Portal','Evaluate transformed quadratic functions to route a ball through energy portals.'],
 ['math6','expressions-equations','equation-launch','Equation Launch Pad','Evaluate expressions and solve one-step equations to fire each stage of a rocket.','2026-11-05'],
 ['prealgebra7','solving-equations-inequalities','lava-bridge','Lava Bridge Builder','Solve two-step equations and inequalities to lay safe stones across a lava river.','2026-11-05'],
 ['prealgebra','systems-linear-equations','system-lasers','Laser Lock: Systems','Find where two lines cross to lock laser beams onto security nodes.','2026-11-05'],
 ['precalculus','functions','function-gates','Function Gates','Evaluate, compose, shift and invert functions to route an energy ball through gates.','2026-11-05'],
 ['calculus','derivatives','tangent-cannon','Tangent Line Cannon','Find derivatives and tangent slopes to aim a cannon at distant towers.','2026-11-05']
];
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
