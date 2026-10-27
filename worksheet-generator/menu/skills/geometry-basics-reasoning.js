/* Geometry Unit 1: foundational segment and angle measurements.
   Every answer is independently checked by the existing equation verifier. */
(function(G){
 'use strict';
 var NS=G.MKMENU,K=NS.kit,M=K.M,st=K.step;
 function question(ctx,kind){
  var r=ctx.rng,c=ctx.c,x=r.int(c<3?2:3,c<3?12:24),a=c>4?r.int(2,5):1,b=r.int(2,12),total=a*x+b;
  var eq=a===1?'x+'+b+'='+total:a+'x+'+b+'='+total;
  var text=kind==='segment'
    ? 'Point B lies between A and C on a straight segment. The sum of AB and BC equals AC. Find x using '
    : 'A ray divides a larger angle into two adjacent angles. Their measures add to the whole angle. Find x using ';
  return {variant:'geo-'+kind+'-'+c,prompt:text+M(eq)+'.',fig:kind==='segment'?{kind:'geo-segment',labels:['A','B','C'],measures:[(a===1?'x':a+'x'),String(b),String(total)],description:'Collinear points A, B, C with algebraic segment lengths'}:{kind:'geo-angle',labels:['A','B','C'],measures:[(a===1?'x':a+'x')+'°',b+'°',total+'°'],description:'Adjacent angles whose measures sum to the whole angle'},parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('Apply the '+(kind==='segment'?'segment addition postulate':'angle addition postulate')+'.',M(eq)),st('Subtract the known part, then divide by the coefficient.',M('x='+x))],space:[1,1.3,1.6]};
 }

 function midpoint(ctx){
  var r=ctx.rng,c=ctx.c,x=r.int(3,22),a=c>=5?r.int(2,4):1,b=r.int(1,10),left=a*x+b;
  var eq=(a===1?'x':a+'x')+'+'+b+'='+left;
  return {variant:'geo-midpoint-'+c,prompt:'B is the midpoint of segment AC, so AB = BC. Find x using '+M(eq)+'.',fig:{kind:'geo-segment',labels:['A','B','C'],measures:[(a===1?'x':a+'x')+'+'+b,String(left),'AB = BC'],description:'B is midpoint of AC; two equal segments'},parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('A midpoint makes the adjacent segments congruent.',M(eq)),st('Solve the equation.',M('x='+x))],space:[1,1.3,1.6]};
 }
 function bisector(ctx){
  var r=ctx.rng,c=ctx.c,x=r.int(3,22),a=c>=5?r.int(2,4):1,b=r.int(1,10),side=a*x+b,eq=(a===1?'x':a+'x')+'+'+b+'='+side;
  return {variant:'geo-bisector-'+c,prompt:'Ray BD bisects angle ABC, so its two adjacent angles are congruent. Find x using '+M(eq)+'.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('An angle bisector creates two equal angles.',M(eq)),st('Solve.',M('x='+x))],space:[1,1.3,1.6]};
 }

 function coordinateMidpoint(ctx){
  var r=ctx.rng,c=ctx.c,a=r.int(-12,10),x=r.int(-12,16),middle=(a+x)/2;
  // Use a whole-number midpoint by giving endpoint coordinates of equal parity.
  x=a+2*r.int(c>=5?-9:1,c>=5?9:12);
  middle=(a+x)/2;
  var eq='x+'+a+'='+2*middle;
  if(a<0)eq='x'+a+'='+2*middle;
  return {variant:'geo-coordinate-midpoint-'+c,
   prompt:'On a number line, point A has coordinate '+a+' and point M is the midpoint of segment AB at coordinate '+middle+'. Point B has coordinate x. Find x using '+M(eq)+'.',
   parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
   steps:[st('Twice the midpoint coordinate equals the sum of endpoint coordinates.',M(eq)),st('Solve for the missing endpoint.',M('x='+x))],
   space:[1,1.3,1.6]};
 }
 function distanceCoordinate(ctx){
  var r=ctx.rng,c=ctx.c,left=r.int(c>=4?-15:0,10),distance=r.int(2,c>=5?24:15),right=left+distance;
  var eq='x-'+left+'='+distance;
  if(left<0)eq='x+'+(-left)+'='+distance;
  return {variant:'geo-coordinate-distance-'+c,
    prompt:'Points A and B lie on a horizontal line at A = ('+left+', 3) and B = (x, 3). B lies to the right of A and AB = '+distance+' units. Find x using '+M(eq)+'.',
    parts:[{answer:M('x='+right),check:{type:'solve',eq:eq,v:'x'}}],
    steps:[st('For points on a horizontal line, subtract their x-coordinates.',M(eq)),st('Solve for x.',M('x='+right))],
    space:[1,1.3,1.6]};
 }
 NS.registerSkillSet({id:'geometry-basics-reasoning',course:'geometry',courseName:'Geometry',unit:'basics-reasoning',unitName:'Foundations of Geometry',title:'Geometry Foundations',
 tags:{SEGMENT:'Segment addition and lengths',ANGLE:'Angle addition and measures',MIDPOINT:'Midpoints',BISECTOR:'Angle bisectors',COORD:'Coordinate geometry'},
 reference:'<div class="mm-refgrid"><section><h4>Segment addition</h4><p>When B is between A and C, AB + BC = AC.</p></section><section><h4>Angle addition</h4><p>Adjacent angles add to the measure of their whole angle.</p></section></div>',
 gaps:['Diagram-based constructions and measurement remain pending.'],skills:[
 {id:'segment-addition',tag:'SEGMENT',name:'Find missing segment length',best:[0,1,2],generate:ctx=>question(ctx,'segment')},
 {id:'angle-addition',tag:'ANGLE',name:'Find missing angle measure',best:[0,1,2],generate:ctx=>question(ctx,'angle')},
 {id:'midpoint',tag:'MIDPOINT',name:'Midpoint and equal segments',best:[0,1,2],generate:midpoint},
 {id:'angle-bisector',tag:'BISECTOR',name:'Angle bisectors',best:[0,1,2],generate:bisector},
 {id:'coordinate-midpoint',tag:'COORD',name:'Midpoint with missing endpoint coordinate',best:[0,1,2],generate:coordinateMidpoint},
 {id:'coordinate-distance',tag:'COORD',name:'Horizontal distance and missing coordinate',best:[0,1,2],generate:distanceCoordinate}
 ]});
})(typeof window!=='undefined'?window:globalThis);
