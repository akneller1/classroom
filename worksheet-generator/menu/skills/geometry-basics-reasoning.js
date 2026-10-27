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
  return {variant:'geo-'+kind+'-'+c,prompt:text+M(eq)+'.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('Apply the '+(kind==='segment'?'segment addition postulate':'angle addition postulate')+'.',M(eq)),st('Subtract the known part, then divide by the coefficient.',M('x='+x))],space:[1,1.3,1.6]};
 }
 NS.registerSkillSet({id:'geometry-basics-reasoning',course:'geometry',courseName:'Geometry',unit:'basics-reasoning',unitName:'Foundations of Geometry',title:'Geometry Foundations',
 tags:{SEGMENT:'Segment addition and lengths',ANGLE:'Angle addition and measures'},
 reference:'<div class="mm-refgrid"><section><h4>Segment addition</h4><p>When B is between A and C, AB + BC = AC.</p></section><section><h4>Angle addition</h4><p>Adjacent angles add to the measure of their whole angle.</p></section></div>',
 gaps:['Diagram-based constructions and measurement remain pending.'],skills:[
 {id:'segment-addition',tag:'SEGMENT',name:'Find missing segment length',best:[0,1,2],generate:ctx=>question(ctx,'segment')},
 {id:'angle-addition',tag:'ANGLE',name:'Find missing angle measure',best:[0,1,2],generate:ctx=>question(ctx,'angle')}
 ]});
})(typeof window!=='undefined'?window:globalThis);
