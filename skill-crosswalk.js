/* Curriculum crosswalk: candidate overlaps only. Does NOT approve or enable math generators. */
(function(root){
'use strict';
var catalog=root.MK_COURSE_CATALOG;
var definitions=[
 {key:'evaluating-expressions',source:['algebra','foundations-algebra','Order of Operations and Evaluating Expressions'],targets:[['math6','expressions-equations','Writing and Evaluating Algebraic Expressions'],['prealgebra7','algebraic-expressions-integers','Writing and Evaluating Expressions']]},
 {key:'distributive-property',source:['algebra','foundations-algebra','Distributive Property and Combining Like Terms'],targets:[['prealgebra7','one-step-equations-inequalities','The Distributive Property'],['prealgebra','equations-expressions','Solving equations using the distributive property']]},
 {key:'equations-both-sides',source:['algebra','expressions-equations','Equations with Variables on Both Sides'],targets:[['prealgebra7','solving-equations-inequalities','Solving Equations with Variables on Both Sides'],['prealgebra','equations-expressions','Solving equations with variables on both sides']]},
 {key:'systems-graphing',source:['algebra','systems-of-equations','Solving Systems by Graphing'],targets:[['prealgebra7','linear-functions-graphing','Solving Systems of Linear Equations by Graphing'],['prealgebra','systems-linear-equations','Solving systems by graphing']]},
 {key:'systems-substitution',source:['algebra','systems-of-equations','Solving Systems by Substitution'],targets:[['prealgebra7','linear-functions-graphing','Solving Systems of Linear Equations by Substitution'],['prealgebra','systems-linear-equations','Solving systems by substitution']]},
 {"key":"scientific-notation","source":["algebra","exponents-exponential-functions","Scientific Notation"],"targets":[["prealgebra7","factors-fractions-exponents","Scientific Notation"],["prealgebra","real-numbers-exponents","Scientific notation"]]},
 {"key":"mean-median-mode","source":["algebra","statistics-data-modeling","Mean, Median, and Mode"],"targets":[["prealgebra7","decimals-equations","Mean, Median, and Mode"],["math6","data-displays","Mean and Median"]]},
 {"key":"scatter-plots","source":["algebra","statistics-data-modeling","Scatter Plots and Association"],"targets":[["prealgebra7","linear-functions-graphing","Scatter Plots"],["prealgebra","patterns-bivariate-data","Constructing scatter plots"]]},
 {"key":"pythagorean-theorem","source":["geometry","right-triangles-trigonometry","Pythagorean Theorem"],"targets":[["prealgebra7","right-triangles-algebra","The Pythagorean Theorem"],["prealgebra","geometry-applications","Pythagorean theorem and its converse"]]},
 {"key":"transformations-translations","source":["geometry","transformations","Translations on the Coordinate Plane"],"targets":[["prealgebra7","spatial-thinking","Translations"],["prealgebra","congruence-similarity","Translations and their properties"]]},
 {"key":"transformations-rotations","source":["geometry","transformations","Rotations about the Origin"],"targets":[["prealgebra7","spatial-thinking","Rotations"],["prealgebra","congruence-similarity","Rotations and their properties"]]},
 {"key":"transformations-reflections","source":["geometry","transformations","Reflections over Axes and Lines"],"targets":[["prealgebra","congruence-similarity","Reflections and their properties"]]},
 {"key":"circle-area","source":["geometry","area-surface-area-volume","Circumference and Area of Circles"],"targets":[["prealgebra7","area-volume","Area of Circles"]]},
 {"key":"slope","source":["algebra","linear-equations-slope","Rate of Change and Slope"],"targets":[["prealgebra7","linear-functions-graphing","Slope and y-intercept"],["prealgebra","linear-functional-relationships","Interpreting rates of change"]]},
 {"key":"systems-elimination","source":["algebra","systems-of-equations","Solving Systems by Elimination (Add/Subtract)"],"targets":[["prealgebra","systems-linear-equations","Solving systems by elimination"]]}
];
function find(tuple){
 var records=catalog.getSkillRecords(tuple[0],tuple[1]);
 var match=records.filter(function(x){return x.name.toLowerCase()===tuple[2].toLowerCase()});
 return match.length===1?{courseId:tuple[0],unitId:tuple[1],skillId:match[0].id,name:match[0].name}:null;
}
function matches(){
 return definitions.map(function(d){return {key:d.key,source:find(d.source),targets:d.targets.map(find),status:'candidate',enabled:false};});
}
function valid(){return matches().every(function(m){return !!m.source&&m.targets.every(Boolean)});}
root.MK_SKILL_CROSSWALK={version:1,matches:matches,valid:valid};
})(typeof window!=='undefined'?window:globalThis);
