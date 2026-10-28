/* Geometry Unit 4: independently solvable triangle relationships.
   These are text-first starter questions. Diagram-based applications remain a documented gap. */
(function(G){
'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(ctx,kind){
 var r=ctx.rng,c=ctx.c,x,eq,prompt,reason,a,b,remote,ext,vertex;
 if(kind==='sum'){
   x=r.int(c<=3?30:18,c<=3?85:100);
   a=r.int(18,Math.min(155-x,65));b=180-x-a;
   eq='x+'+a+'+'+b+'=180';
   prompt='A triangle has interior angles measuring '+M('x^\\circ')+', '+a+'° and '+b+'°. Find x.';
   reason='Interior angles of a triangle sum to 180°.';
 } else if(kind==='exterior'){
   x=r.int(18,78);
   remote=r.int(15,84);ext=x+remote;
   eq='x+'+remote+'='+ext;
   prompt='An exterior angle of a triangle measures '+ext+'°. Its two remote interior angles measure '+M('x^\\circ')+' and '+remote+'°. Find x.';
   reason='An exterior angle equals the sum of its remote interior angles.';
 } else if(kind==='isosceles'){
   x=r.int(31,77);vertex=180-2*x;
   eq='2x+'+vertex+'=180';
   prompt='An isosceles triangle has two congruent base angles, each measuring '+M('x^\\circ')+'. Its vertex angle measures '+vertex+'°. Find x.';
   reason='The two base angles are congruent, and all three angles total 180°.';
 }
 var fig=kind==='sum'?{kind:'geo-tri',mode:'angles',angles:[x,a,b],lab:{A:'x°',B:a+'°',C:b+'°'}}:kind==='exterior'?{kind:'geo-tri',mode:'angles',angles:[x,180-ext,remote],lab:{A:'x°',C:remote+'°'},ext:{vertex:'B',lab:ext+'°'}}:{kind:'geo-tri',mode:'angles',angles:[x,x,vertex],lab:{A:'x°',B:'x°',C:vertex+'°'},ticks:['AC','BC']};
 return {variant:'geo-triangle-'+kind+'-'+c,fig:fig,prompt:prompt+' Set up and solve an equation for x.',
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
  fig:{kind:'geo-tri',mode:'sides',sides:[a,b,Math.max(a,b)],sideLab:{AB:String(a),BC:String(b),CA:'x'}},
  prompt:'Two sides of a triangle measure '+a+' and '+b+' units. What is the greatest INTEGER length x that the third side can have? Explain why the triangle inequality is strict. Set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The third side must be less than the sum of the other two and greater than their difference.',M(lo+'<x<'+hi)),step('The greatest possible integer is one less than the sum.',M('x='+x))],
  space:[1.2,1.6,2]}; 
}
function midsegment(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(5,c>=5?35:18),a=c>=5?r.int(2,4):1,b=r.int(1,8);
 var small=a*x+b,full=2*small,eq=(a===1?'x':a+'x')+'+'+b+'='+full+'/2';
 return {variant:'geo-triangle-midsegment-'+c,
  fig:{kind:'geo-tri',mode:'midseg',lab:{DE:(a===1?'x':a+'x')+'+'+b,BC:String(full)}},
  prompt:'In triangle ABC, D and E are the midpoints of AB and AC. Segment DE is parallel to BC. DE measures '+M((a===1?'x':a+'x')+'+'+b)+' units and BC measures '+full+' units. Find x and explain the midsegment relationship. Set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('A triangle midsegment is half the length of the third side.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.3,1.8,2.2]};
}
function centroid(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(4,c>=5?30:16),a=c>=5?r.int(2,3):1,b=r.int(1,8),near=a*x+b,whole=3*near;
 var eq='3*'+(a===1?'x':a+'x')+'+3*'+b+'='+whole;
 return {variant:'geo-triangle-centroid-'+c,
  fig:{kind:'geo-tri',mode:'centroid',lab:{GM:(a===1?'x':a+'x')+'+'+b,AM:String(whole)}},
  prompt:'In triangle ABC, M is the midpoint of BC and G is the centroid on median AM. The shorter segment GM measures '+M((a===1?'x':a+'x')+'+'+b)+' units. The full median AM measures '+whole+' units. Find x. Explain the 2:1 centroid ratio. Set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The centroid divides a median 2:1, so the shorter segment is one-third of the full median.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.3,1.8,2.2]};
}
function sideAngleOrder(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(7,c>=5?30:20),a=c>=5?r.int(2,4):1,b=r.int(1,9),largest=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+largest;
 var bigA=r.int(70,100),rest=180-bigA,angB=r.int(Math.ceil(rest*0.35),Math.floor(rest*0.65));
 return {variant:'geo-triangle-side-angle-order-'+c,
  fig:{kind:'geo-tri',mode:'angles',angles:[bigA,angB,rest-angB],lab:{A:'largest'},sideLab:{BC:(a===1?'x':a+'x')+'+'+b}},
  prompt:'In triangle ABC, angle A is the largest angle. Side BC, opposite angle A, measures '+M((a===1?'x':a+'x')+'+'+b)+' units. The longest side is '+largest+' units. Find x and explain how the side-angle ordering theorem identifies BC. Set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The longest side lies opposite the largest angle.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.3,1.8,2.2]};
}

function perpendicularBisector(ctx) {
 var r=ctx.rng,c=ctx.c,x=r.int(3,c>=5?26:14),a=c>=5?r.int(2,4):1,b=r.int(1,9),distance=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+distance;
 return {variant:'geo-triangle-perpendicular-bisector-'+c,
  fig:{kind:'geo-tri',mode:'perpbis',lab:{PA:(a===1?'x':a+'x')+'+'+b,PB:String(distance)}},
  prompt:'Point P lies on the perpendicular bisector of segment AB. PA measures '+M((a===1?'x':a+'x')+'+'+b)+' units and PB measures '+distance+' units. Find x. State the perpendicular bisector theorem. Set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('Every point on a perpendicular bisector is equidistant from the endpoints.',M(eq)),step('Solve for x.',M('x='+x))],
  space:[1.2,1.7,2.2]};
}
function altitudeArea(ctx) {
 var r=ctx.rng,c=ctx.c,base=2*r.int(3,c>=5?17:11),x=r.int(4,c>=5?28:17),area=base*x/2;
 var eq='x='+2*area+'/'+base;
 // The altitude is perpendicular to the base; it is not necessarily a side.
 return {variant:'geo-triangle-altitude-area-'+c,
  fig:{kind:'geo-tri',mode:'altitude',obtuse:r.int(0,1)===1,lab:{BC:base+' cm',AD:'x'}},
  prompt:'Triangle ABC has base BC of '+base+' cm and area '+area+' square centimeters. Altitude AD is perpendicular to the line containing BC (D may lie outside segment BC). Find the altitude length x. Set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('The perpendicular altitude determines the area even for an obtuse triangle.',M(area+'='+base+'x/2')),step('Solve for the height.',M('x='+x))],
  space:[1.2,1.7,2.2]};
}
function triangleInvestigation(ctx) {
 var r=ctx.rng,c=ctx.c,a=r.int(7,14),b=r.int(7,14),hi=a+b,lo=Math.abs(a-b),third=hi-1;
 var half=2*r.int(4,c>=5?17:10),mid=half/2;
 var median=3*r.int(3,c>=5?15:9),near=median/3;
 var e1='x+1='+hi,e2='2y='+half,e3='3z='+median,e4='w+1='+(hi+1);
 return {variant:'geo-triangle-investigation-'+c,
  prompt:'Open Response: Investigate triangle side lengths, midsegments, and medians. Show the theorem or relationship used for every part.',
  parts:[
   {label:'a',prompt:'A triangle has sides '+a+' and '+b+' units. Find the greatest integer third side x. Show the relationship you use.',answer:M('x='+third),check:{type:'solve',eq:e1,v:'x'}},
   {label:'b',prompt:'In a different triangle, a midsegment is parallel to a side measuring '+half+' units. Find midsegment length y. Show the relationship you use.',answer:M('y='+mid),check:{type:'solve',eq:e2,v:'y'}},
   {label:'c',prompt:'A median has total length '+median+' units. Find the shorter segment z from the centroid to the midpoint. Show the relationship you use.',answer:M('z='+near),check:{type:'solve',eq:e3,v:'z'}},
   {label:'d',prompt:'For the triangle in (a), find the greatest possible integer third side w when the side of length '+a+' increases by 1 unit. Show the relationship you use.',answer:M('w='+hi),check:{type:'solve',eq:e4,v:'w'}}
  ],
  steps:[step('Triangle inequality',M(e1)),step('Midsegment theorem',M(e2)),step('Centroid ratio',M(e3)),step('Triangle inequality with the modified side',M(e4))],
  space:[2.5,3.1,3.8]};
}

/* A single connected Honors investigation: each later result depends on
   the geometry established in an earlier part. */
function honorsChain(ctx) {
 var r=ctx.rng,c=ctx.c,half=r.int(5,c>=5?22:13),side=2*half;
 var median=3*r.int(4,c>=5?17:10),short=median/3,long=2*median/3;
 var max=side+median-1;
 var e1='x=2*'+half,e2='3y='+median,e3='z=2*'+short,e4='w+1='+side+'+'+median;
 return {variant:'geo-triangle-honors-chain-'+c,
  prompt:'Open Response — Connected triangle investigation. In triangle ABC, D and E are the midpoints of AB and AC, so DE is a midsegment parallel to BC. M is the midpoint of BC and G is the centroid on median AM. DE is '+half+' cm and AM is '+median+' cm. For part (d), consider a NEW triangle whose first two sides have lengths BC and AM from this figure. Show and explain your reasoning in all four parts.',
  parts:[
   {label:'a',prompt:'Determine the length x of BC using the midsegment theorem. Show the relationship you use.',answer:M('x='+side),check:{type:'solve',eq:e1,v:'x'}},
   {label:'b',prompt:'Determine the length y of GM using the centroid theorem. Show the relationship you use.',answer:M('y='+short),check:{type:'solve',eq:e2,v:'y'}},
   {label:'c',prompt:'Determine the length z of AG using your result from (b). Show the relationship you use.',answer:M('z='+long),check:{type:'solve',eq:e3,v:'z'}},
   {label:'d',prompt:'For the new triangle with sides BC and AM, determine the greatest integer third side w allowed by the triangle inequality. Show the relationship you use.',answer:M('w='+max),check:{type:'solve',eq:e4,v:'w'}}
  ],
  steps:[
   step('DE is half of BC.',M(e1)),
   step('GM is one-third of AM.',M(e2)),
   step('AG is twice GM.',M(e3)),
   step('The third side is strictly less than the sum of the two known sides.',M(e4))
  ],space:[3,3.6,4.2]};
}
NS.registerSkillSet({id:'geometry-triangle-relationships',course:'geometry',courseName:'Geometry',
 unit:'triangle-relationships',unitName:'Triangle Relationships',title:'Triangle Angle Relationships',
 tags:{SUM:'Triangle angle sum',EXTERIOR:'Exterior angle theorem',ISOSCELES:'Isosceles triangle angle relationships',INEQUALITY:'Triangle inequality',MIDSEGMENT:'Triangle midsegment theorem',CENTROID:'Centroids and medians',ORDER:'Side and angle order',BISECTOR:'Perpendicular bisector theorem',ALTITUDE:'Altitudes and area',INVESTIGATION:'Four-part triangle investigation',HONORS:'Connected Honors triangle investigation'},
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
  {id:'triangle-open-response-investigation',tag:'INVESTIGATION',name:'Four-part triangle relationships investigation',best:[2],generate:triangleInvestigation},
  {id:'triangle-honors-connected-investigation',tag:'HONORS',name:'Honors: connected midsegment, centroid and inequality investigation',best:[2],generate:honorsChain}
 ]});
})(typeof window!=='undefined'?window:globalThis);
