/* Geometry Unit 4: independently solvable triangle relationships.
   These are text-first starter questions. Diagram-based applications remain a documented gap. */
(function(G){
'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(ctx,kind){
 var r=ctx.rng,c=ctx.c,x,eq,prompt,reason;
 if(kind==='sum'){
   x=r.int(c<=3?30:18,c<=3?85:100);
   var a=r.int(18,Math.min(155-x,65)),b=180-x-a;
   eq='x+'+a+'+'+b+'=180';
   prompt='A triangle has interior angles measuring '+M('x^\\circ')+', '+a+'° and '+b+'°. Find x.';
   reason='Interior angles of a triangle sum to 180°.';
 } else if(kind==='exterior'){
   x=r.int(18,78);
   var remote=r.int(15,84),ext=x+remote;
   eq='x+'+remote+'='+ext;
   prompt='An exterior angle of a triangle measures '+ext+'°. Its two remote interior angles measure '+M('x^\\circ')+' and '+remote+'°. Find x.';
   reason='An exterior angle equals the sum of its remote interior angles.';
 } else if(kind==='isosceles'){
   x=r.int(31,77);var vertex=180-2*x;
   eq='2x+'+vertex+'=180';
   prompt='An isosceles triangle has two congruent base angles, each measuring '+M('x^\\circ')+'. Its vertex angle measures '+vertex+'°. Find x.';
   reason='The two base angles are congruent, and all three angles total 180°.';
 }
 return {variant:'geo-triangle-'+kind+'-'+c,prompt:prompt+' Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq,v:'x'}}],
  steps:[step(reason,M(eq)),step('Solve for the unknown angle.',M('x='+x))],
  space:[1.1,1.4,1.7]};
}

/* The next families deliberately require students to choose the geometric
   relationship rather than copying an equation supplied in the prompt. */
function triangleInequality(ctx) {
 var r=ctx.rng,c=ctx.c,a=r.int(5,c>=5?25:16),b=r.int(5,c>=5?25:16);
 var lo=Math.abs(a-b),hi=a+b;
 var x=hi-1;
 var eq='x+1='+hi;
 return {variant:'geo-triangle-inequality-'+c,
  prompt:'Two sides of a triangle measure '+a+' and '+b+' units. What is the greatest INTEGER length x that the third side can have? Explain why the triangle inequality is strict. Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The third side must be less than the sum of the other two and greater than their difference.',M(lo+'<x<'+hi)),step('The greatest possible integer is one less than the sum.',M('x='+x))],
  space:[1.2,1.6,2]}; 
}
function midsegment(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(5,c>=5?35:18),a=c>=5?r.int(2,4):1,b=r.int(1,8);
 var small=a*x+b,full=2*small,eq=(a===1?'x':a+'x')+'+'+b+'='+full+'/2';
 return {variant:'geo-triangle-midsegment-'+c,
  fig:{kind:'geo-triangle-landmark',case:'midsegment'},
  prompt:'In triangle ABC, D and E are the midpoints of AB and AC. Segment DE is parallel to BC. DE measures '+M((a===1?'x':a+'x')+'+'+b)+' units and BC measures '+full+' units. Find x and explain the midsegment relationship. Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('A triangle midsegment is half the length of the third side.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.3,1.8,2.2]};
}
function centroid(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(4,c>=5?30:16),a=c>=5?r.int(2,3):1,b=r.int(1,8),near=a*x+b,whole=3*near;
 var eq='3*'+(a===1?'x':a+'x')+'+3*'+b+'='+whole;
 return {variant:'geo-triangle-centroid-'+c,
  fig:{kind:'geo-triangle-landmark',case:'centroid'},
  prompt:'In triangle ABC, M is the midpoint of BC and G is the centroid on median AM. The shorter segment GM measures '+M((a===1?'x':a+'x')+'+'+b)+' units. The full median AM measures '+whole+' units. Find x. Explain the 2:1 centroid ratio. Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The centroid divides a median 2:1, so the shorter segment is one-third of the full median.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.3,1.8,2.2]};
}
function sideAngleOrder(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(7,c>=5?30:20),a=c>=5?r.int(2,4):1,b=r.int(1,9),largest=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+largest;
 return {variant:'geo-triangle-side-angle-order-'+c,
  prompt:'In triangle ABC, angle A is the largest angle. Side BC, opposite angle A, measures '+M((a===1?'x':a+'x')+'+'+b)+' units. The longest side is '+largest+' units. Find x and explain how the side-angle ordering theorem identifies BC. Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The longest side lies opposite the largest angle.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.3,1.8,2.2]};
}

function perpendicularBisector(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(3,c>=5?26:14),a=c>=5?r.int(2,4):1,b=r.int(1,9),distance=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+distance;
 return {variant:'geo-triangle-perpendicular-bisector-'+c,
  fig:{kind:'geo-triangle-landmark',case:'bisector'},
  prompt:'Point P lies on the perpendicular bisector of segment AB. PA measures '+M((a===1?'x':a+'x')+'+'+b)+' units and PB measures '+distance+' units. Find x. State the perpendicular bisector theorem. Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('Every point on a perpendicular bisector is equidistant from the endpoints.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.2,1.7,2.2]};
}
function altitudeArea(ctx) {
 var r=ctx.rng,c=ctx.c,base=2*r.int(3,c>=5?17:11),x=r.int(4,c>=5?28:17),area=base*x/2;
 var eq='x='+2*area+'/'+base;
 // The altitude is perpendicular to the base; it is not necessarily a side.
 return {variant:'geo-triangle-altitude-area-'+c,
  fig:{kind:'geo-triangle-landmark',case:'altitude'},
  prompt:'Triangle ABC has base BC of '+base+' cm and area '+area+' square centimeters. Altitude AD is perpendicular to the line containing BC (D may lie outside segment BC). Find the altitude length x. Use '+M(eq)+' to find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The perpendicular altitude determines the area even for an obtuse triangle.',M(area+'='+base+'x/2')),step('Solve for the height.',M('x='+x))],
  space:[1.2,1.7,2.2]};
}
function triangleInvestigation(ctx) {
 var r=ctx.rng,c=ctx.c,a=r.int(7,14),b=r.int(7,14),hi=a+b,lo=Math.abs(a-b),third=hi-1;
 var half=2*r.int(4,c>=5?17:10),mid=half/2;
 var median=3*r.int(3,c>=5?15:9),near=median/3;
 var e1='x+1='+hi,e2='2y='+half,e3='3z='+median,e4='w='+hi;
 return {variant:'geo-triangle-investigation-'+c,
  prompt:'Open Response: Investigate triangle side lengths, midsegments, and medians. Show the theorem or relationship used for every part.',
  parts:[
   {label:'a',prompt:'A triangle has sides '+a+' and '+b+' units. Find the greatest integer third side x. Use '+M(e1)+'.',answer:M('x='+third),check:{type:'solve',eq:e1,v:'x'}},
   {label:'b',prompt:'In a different triangle, a midsegment is parallel to a side measuring '+half+' units. Find midsegment length y. Use '+M(e2)+'.',answer:M('y='+mid),check:{type:'solve',eq:e2,v:'y'}},
   {label:'c',prompt:'A median has total length '+median+' units. Find the shorter segment z from the centroid to the midpoint. Use '+M(e3)+'.',answer:M('z='+near),check:{type:'solve',eq:e3,v:'z'}},
   {label:'d',prompt:'For the triangle in (a), find the greatest possible integer third side w when one of the given sides increases by 1 unit. Use '+M(e4)+'.',answer:M('w='+hi),check:{type:'solve',eq:e4,v:'w'}}
  ],
  steps:[step('Triangle inequality',M(e1)),step('Midsegment theorem',M(e2)),step('Centroid ratio',M(e3)),step('Triangle inequality with the modified side',M(e4))],
  space:[2.5,3.1,3.8]};
}
NS.registerSkillSet({id:'geometry-triangle-relationships',course:'geometry',courseName:'Geometry',
 unit:'triangle-relationships',unitName:'Triangle Relationships',title:'Triangle Angle Relationships',
 tags:{SUM:'Triangle angle sum',EXTERIOR:'Exterior angle theorem',ISOSCELES:'Isosceles triangle angle relationships',INEQUALITY:'Triangle inequality',MIDSEGMENT:'Triangle midsegment theorem',CENTROID:'Centroids and medians',ORDER:'Side and angle order',BISECTOR:'Perpendicular bisector theorem',ALTITUDE:'Altitudes and area',INVESTIGATION:'Four-part triangle investigation'},
 reference:'<div class="mm-refgrid"><section><h4>Interior angle sum</h4><p>Every triangle has an angle sum of 180°.</p></section><section><h4>Exterior angle theorem</h4><p>An exterior angle equals the sum of the two remote interior angles.</p></section></div>',
 gaps:['Labeled diagrams, richer inequality cases, and non-routine multistep Honors reasoning remain to be developed.'],
 skills:[
  {id:'triangle-interior-sum',tag:'SUM',name:'Find a missing interior angle',best:[0,1,2],generate:ctx=>make(ctx,'sum')},
  {id:'triangle-exterior-angle',tag:'EXTERIOR',name:'Exterior angle theorem',best:[0,1,2],generate:ctx=>make(ctx,'exterior')},
  {id:'triangle-isosceles-angles',tag:'ISOSCELES',name:'Isosceles triangle base angles',best:[0,1,2],generate:ctx=>make(ctx,'isosceles')},
  {id:'triangle-inequality-max-integer',tag:'INEQUALITY',name:'Triangle inequality: greatest possible integer side',best:[0,1,2],generate:triangleInequality},
  {id:'triangle-midsegment-length',tag:'MIDSEGMENT',name:'Triangle midsegment theorem',best:[0,1,2],generate:midsegment},
  {id:'triangle-centroid-median',tag:'CENTROID',name:'Centroid and median 2:1 ratio',best:[0,1,2],generate:centroid},
  {id:'triangle-side-angle-order',tag:'ORDER',name:'Longest side opposite largest angle',best:[0,1,2],generate:sideAngleOrder},
  {id:'triangle-perpendicular-bisector',tag:'BISECTOR',name:'Perpendicular bisector equidistance',best:[0,1,2],generate:perpendicularBisector},
  {id:'triangle-altitude-area',tag:'ALTITUDE',name:'Triangle altitude from area',best:[0,1,2],generate:altitudeArea},
  {id:'triangle-open-response-investigation',tag:'INVESTIGATION',name:'Four-part triangle relationships investigation',best:[2],generate:triangleInvestigation}
 ]});
})(typeof window!=='undefined'?window:globalThis);
