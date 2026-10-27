/* Geometry Unit 2: angle relationships with verified numeric answers.
   Do not assume a diagram is present; relationships are stated in text. */
(function(G){
 'use strict';
 var NS=G.MKMENU,K=NS.kit,M=K.M,st=K.step;
 function angle(ctx,kind){
  var r=ctx.rng,c=ctx.c,limit=kind==='complement'?90:180;
  var x=r.int(c<3?8:12,kind==='complement'?65:130),fixed=limit-x;
  var a=c>=5?r.int(2,4):1;
  var target=x;
  if(a>1){target=r.int(8,Math.floor((limit-10)/a));fixed=limit-a*target;}
  var left=a===1?'x':a+'x',eq=left+'+'+fixed+'='+limit;
  var description=kind==='complement'?'Two complementary angles':'Two supplementary angles';
  var prompt=description+' have measures that add to '+limit+' degrees. Find x using '+M(eq)+'.';
  return {variant:'geo-'+kind+'-'+c,prompt,parts:[{answer:M('x='+target),check:{type:'solve',eq,v:'x'}}],steps:[st('The two angles add to '+limit+' degrees.',M(eq)),st('Solve for x.',M('x='+target))],space:[1,1.3,1.6]};
 }

 function vertical(ctx){
  var r=ctx.rng,c=ctx.c,x=r.int(8,28),a=c>=5?r.int(2,4):1,b=r.int(1,11),v=a*x+b,eq=(a===1?'x':a+'x')+'+'+b+'='+v;
  return {variant:'geo-vertical-'+c,prompt:'Two vertical angles are congruent. Their measurements are represented by the two sides of '+M(eq)+'. Find x.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('Vertical angles are congruent.',M(eq)),st('Solve for x.',M('x='+x))],space:[1,1.3,1.6]};
 }
 function linearPair(ctx){
  var r=ctx.rng,c=ctx.c,a=c>=5?r.int(2,4):1,x=r.int(8,Math.floor(140/a)),fixed=180-a*x,eq=(a===1?'x':a+'x')+'+'+fixed+'=180';
  return {variant:'geo-linear-pair-'+c,prompt:'Two adjacent angles form a linear pair (a straight angle). Find x using '+M(eq)+'.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('A linear pair sums to 180 degrees.',M(eq)),st('Solve.',M('x='+x))],space:[1,1.3,1.6]};
 }

 function transversal(ctx,relationship){
  var r=ctx.rng,c=ctx.c,x=r.int(12,32),a=c>=5?r.int(2,4):1,b=r.int(1,9);
  var base=a*x+b, supplementary=180-base;
  // Limit both angle measures to valid, nonzero angles.
  if(base>=165){x=r.int(8,Math.floor((150-b)/a));base=a*x+b;supplementary=180-base;}
  var eq=relationship==='same-side'?(a===1?'x':a+'x')+'+'+b+'+'+supplementary+'=180':(a===1?'x':a+'x')+'+'+b+'='+base;
  var relationNames={corresponding:'corresponding','alternate-interior':'alternate interior','alternate-exterior':'alternate exterior','same-side':'same-side interior'};
  var text=relationship==='same-side'?'Same-side interior angles are supplementary':'The two '+relationNames[relationship]+' angles are congruent';
  return {variant:'geo-transversal-'+relationship+'-'+c,prompt:'Two parallel lines are cut by a transversal. '+text+'. Find x using '+M(eq)+'.',
    parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
    steps:[st(relationship==='same-side'?'The angle measures add to 180 degrees.':'The angle measures are equal.',M(eq)),st('Solve for x.',M('x='+x))],
    space:[1,1.3,1.6]};
 }
 NS.registerSkillSet({id:'geometry-angles-parallel-lines',course:'geometry',courseName:'Geometry',unit:'angles-parallel-lines',unitName:'Angles and Parallel Lines',title:'Angle Relationships',
 tags:{COMPLEMENT:'Complementary angles',SUPPLEMENT:'Supplementary angles',VERTICAL:'Vertical angles',LINEAR:'Linear pairs',TRANSVERSAL:'Parallel lines and transversal angle pairs'},
 reference:'<div class="mm-refgrid"><section><h4>Complementary angles</h4><p>The measures sum to 90°.</p></section><section><h4>Supplementary angles</h4><p>The measures sum to 180°.</p></section></div>',
 gaps:['Diagram-dependent transversal problems still require labeled geometric figures. This bank supplies text-based relationships only.'],skills:[
 {id:'complementary-angles',tag:'COMPLEMENT',name:'Complementary angles',best:[0,1,2],generate:ctx=>angle(ctx,'complement')},
 {id:'supplementary-angles',tag:'SUPPLEMENT',name:'Supplementary angles',best:[0,1,2],generate:ctx=>angle(ctx,'supplement')},
 {id:'vertical-angles',tag:'VERTICAL',name:'Vertical angles',best:[0,1,2],generate:vertical},
 {id:'linear-pairs',tag:'LINEAR',name:'Linear pairs',best:[0,1,2],generate:linearPair},
 {id:'corresponding-angles',tag:'TRANSVERSAL',name:'Corresponding angles',best:[0,1,2],generate:ctx=>transversal(ctx,'corresponding')},
 {id:'alternate-interior',tag:'TRANSVERSAL',name:'Alternate interior angles',best:[0,1,2],generate:ctx=>transversal(ctx,'alternate-interior')},
 {id:'alternate-exterior',tag:'TRANSVERSAL',name:'Alternate exterior angles',best:[0,1,2],generate:ctx=>transversal(ctx,'alternate-exterior')},
 {id:'same-side-interior',tag:'TRANSVERSAL',name:'Same-side interior angles',best:[0,1,2],generate:ctx=>transversal(ctx,'same-side')}
 ]});
})(typeof window!=='undefined'?window:globalThis);
