/* Geometry Unit 2: angle relationships with verified numeric answers.
   Do not assume a diagram is present; relationships are stated in text. */
(function(G){
 'use strict';
 var NS=G.MKMENU,K=NS.kit,M=K.M,st=K.step;
 /* Figures come from NS.geoFigures (menu/geometry-figures.js): drawn from the same numbers as the question. */
 function fig(spec){var F=NS.geoFigures;return F&&F.check(spec).ok?spec:undefined}
 function lab(a,k){return (a===1?'x':a+'x')+(k?'+'+k:'')+'°'}
 function labp(a,k){return '('+(a===1?'x':a+'x')+(k?'+'+k:'')+')°'}
 function angle(ctx,kind){
  var r=ctx.rng,c=ctx.c,limit=kind==='complement'?90:180;
  var x=r.int(c<3?8:12,kind==='complement'?65:130),fixed=limit-x;
  var a=c>=5?r.int(2,4):1;
  var target=x;
  if(a>1){target=r.int(8,Math.floor((limit-10)/a));fixed=limit-a*target;}
  var left=a===1?'x':a+'x',eq=left+'+'+fixed+'='+limit;
  var description=kind==='complement'?'Two complementary angles':'Two supplementary angles';
  var prompt=description+' have measures '+M(left)+' degrees and '+fixed+' degrees. Find x by writing and solving an equation.';
  var exprDeg=a*target,flip=r.chance(0.5),pe={text:a===1?'x°':'('+a+'x)°',deg:exprDeg},po={text:fixed+'°',deg:fixed};
  return {variant:'geo-'+kind+'-'+c,prompt,fig:fig({kind:'geo-adjacent',relation:kind==='complement'?'complement':'supplement',parts:flip?[po,pe]:[pe,po]}),parts:[{answer:M('x='+target),check:{type:'solve',eq,v:'x'}}],steps:[st('The two angles add to '+limit+' degrees.',M(eq)),st('Solve for x.',M('x='+target))],space:[1,1.3,1.6]};
 }

 function vertical(ctx){
  var r=ctx.rng,c=ctx.c,x=r.int(8,28),a=c>=5?r.int(2,4):1,b=r.int(1,11),v=a*x+b,eq=(a===1?'x':a+'x')+'+'+b+'='+v;
  var vp=r.chance(0.5)?[1,3]:[2,4],vflip=r.chance(0.5),ve={pos:vp[vflip?1:0],text:labp(a,b),deg:v},vo={pos:vp[vflip?0:1],text:v+'°',deg:v};
  return {variant:'geo-vertical-'+c,prompt:'Two vertical angles are congruent. Their measurements are represented by the two sides of '+M(eq)+'. Find x.',fig:fig({kind:'geo-cross',marks:[ve,vo]}),parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('Vertical angles are congruent.',M(eq)),st('Solve for x.',M('x='+x))],space:[1,1.3,1.6]};
 }
 function linearPair(ctx){
  var r=ctx.rng,c=ctx.c,a=c>=5?r.int(2,4):1,x=r.int(8,Math.floor(140/a)),fixed=180-a*x,eq=(a===1?'x':a+'x')+'+'+fixed+'=180';
  var lflip=r.chance(0.5),le={text:a===1?'x°':'('+a+'x)°',deg:a*x},lo={text:fixed+'°',deg:fixed};
  return {variant:'geo-linear-pair-'+c,fig:fig({kind:'geo-adjacent',relation:'supplement',parts:lflip?[lo,le]:[le,lo]}),prompt:'Two adjacent angles form a linear pair (a straight angle). Their measures are '+M(a===1?'x':a+'x')+' degrees and '+fixed+' degrees. Find x by writing and solving an equation.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('A linear pair sums to 180 degrees.',M(eq)),st('Solve.',M('x='+x))],space:[1,1.3,1.6]};
 }

 function transversal(ctx,relationship){
  var r=ctx.rng,c=ctx.c,a=c>=5?r.int(2,4):1,x=r.int(10,Math.max(11,Math.min(40,Math.floor(139/a))));
  // keep the marked angle between 40 and 140 degrees so the figure can be drawn to scale
  var bLo=Math.max(1,40-a*x),bHi=Math.max(bLo,Math.min(120,140-a*x)),b=r.int(bLo,bHi),base=a*x+b;
  if(base===90){x+=1;base=a*x+b;}
  var supplementary=180-base,same=relationship==='same-side';
  var eq=same?(a===1?'x':a+'x')+'+'+b+'+'+supplementary+'=180':(a===1?'x':a+'x')+'+'+b+'='+base;
  var relationNames={corresponding:'corresponding','alternate-interior':'alternate interior','alternate-exterior':'alternate exterior','same-side':'same-side interior'};
  var relKey={corresponding:'corresponding','alternate-interior':'alternate-interior','alternate-exterior':'alternate-exterior','same-side':'same-side-interior'}[relationship];
  var F=NS.geoFigures,pair=F?F.positionsFor(relKey,r.int(0,3)):[3,6],flip=r.chance(0.5),pe=pair[flip?1:0],po=pair[flip?0:1];
  var figure=fig({kind:'geo-transversal',marks:[{pos:pe,text:labp(a,b),deg:base},{pos:po,text:(same?supplementary:base)+'°',deg:same?supplementary:base}]});
  var text=same?'Same-side interior angles are supplementary':'The two '+relationNames[relationship]+' angles are congruent';
  var prompt=c>=5&&figure
    ?'In the figure, lines ℓ and m are parallel and t is a transversal. Decide how the two marked angles are related, then write and solve an equation to find x.'
    :'Two parallel lines are cut by a transversal'+(figure?' (see the figure)':'')+'. '+text+'. The relevant angle measures are '+M((a===1?'x':a+'x')+'+'+b)+' degrees and '+(same?supplementary:base)+' degrees. Find x by writing and solving an equation.';
  return {variant:'geo-transversal-'+relationship+'-'+c,prompt:prompt,fig:figure,
    parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
    steps:[st(same?'The angle measures add to 180 degrees.':'The angle measures are equal.',M(eq)),st('Solve for x.',M('x='+x))],
    space:[1,1.3,1.6]};
 }
function four(id,c,intro,rows){return {variant:id+'-'+c,prompt:intro,parts:rows.map(function(p,i){return {label:'abcd'[i],prompt:p[0],answer:M(p[1]+'='+p[2]),check:{type:'solve',eq:p[3],v:p[1]}};}),steps:rows.map(function(p){return st(p[4],M(p[3]));}),space:[2.6,3.2,3.9]};}

 function angleInvestigation(ctx){var r=ctx.rng,c=ctx.c,x=r.int(4,c>=5?24:16),k=r.int(2,c>=5?5:3),b=r.int(1,12),M1=k*x+b,y=180-M1,cc=r.int(2,4),e=r.int(1,12),z,ex='('+k+'x+'+b+')°';
  while((y-e)%cc)e++;
  z=(y-e)/cc;
  var zx='('+cc+'z+'+e+')°',w=180-y;
  return {fig:fig({kind:'geo-transversal',names:['ℓ','m'],marks:[{pos:1,text:ex,deg:M1},{pos:5,text:M1+'°',deg:M1},{pos:3,text:'y°',deg:y},{pos:6,text:zx,deg:y},{pos:4,text:'w°',deg:w}]}),
  variant:'geo-angles-investigation-'+c,prompt:'Open Response: Lines ℓ and m are parallel and are cut by a transversal, as shown. Use the angle relationship named in each part and show your reasoning.',
  parts:[
  {label:'a',prompt:'The angles marked '+ex+' and '+M1+'° are corresponding angles. Find x.',answer:M('x='+x),check:{type:'solve',eq:k+'*x+'+b+'='+M1,v:'x'}},
  {label:'b',prompt:'The angle marked y° and the angle marked '+ex+' form a linear pair. Use the angle measure from (a) to find y.',answer:M('y='+y),check:{type:'solve',eq:'y+'+M1+'=180',v:'y'}},
  {label:'c',prompt:'The angle marked '+zx+' and the angle marked y° are alternate interior angles. Find z.',answer:M('z='+z),check:{type:'solve',eq:cc+'*z+'+e+'='+y,v:'z'}},
  {label:'d',prompt:'The angle marked w° and the angle marked '+zx+' are same-side interior angles. Find w.',answer:M('w='+w),check:{type:'solve',eq:'w+'+y+'=180',v:'w'}}],
  steps:[st('Corresponding angles are equal.',M(k+'*x+'+b+'='+M1)),st('A linear pair adds to 180 degrees.',M('y+'+M1+'=180')),st('Alternate interior angles are equal.',M(cc+'*z+'+e+'='+y)),st('Same-side interior angles are supplementary.',M('w+'+y+'=180'))],space:[2.6,3.2,3.9]};}
 NS.registerSkillSet({id:'geometry-angles-parallel-lines',course:'geometry',courseName:'Geometry',unit:'angles-parallel-lines',unitName:'Angles and Parallel Lines',title:'Angle Relationships',
 tags:{INVEST:'Four-part parallel-lines investigation',COMPLEMENT:'Complementary angles',SUPPLEMENT:'Supplementary angles',VERTICAL:'Vertical angles',LINEAR:'Linear pairs',TRANSVERSAL:'Parallel lines and transversal angle pairs'},
 reference:'<div class="mm-refgrid"><section><h4>Complementary angles</h4><p>The measures sum to 90°.</p></section><section><h4>Supplementary angles</h4><p>The measures sum to 180°.</p></section></div>',
 gaps:['Parallel-line proofs, naming angle pairs from a diagram, and figures with more than one transversal are not generated.'],skills:[
 {id:'complementary-angles',tag:'COMPLEMENT',name:'Complementary angles',best:[0,1,2],generate:ctx=>angle(ctx,'complement')},
 {id:'supplementary-angles',tag:'SUPPLEMENT',name:'Supplementary angles',best:[0,1,2],generate:ctx=>angle(ctx,'supplement')},
 {id:'vertical-angles',tag:'VERTICAL',name:'Vertical angles',best:[0,1,2],generate:vertical},
 {id:'linear-pairs',tag:'LINEAR',name:'Linear pairs',best:[0,1,2],generate:linearPair},
 {id:'corresponding-angles',tag:'TRANSVERSAL',name:'Corresponding angles',best:[0,1,2],generate:ctx=>transversal(ctx,'corresponding')},
 {id:'alternate-interior',tag:'TRANSVERSAL',name:'Alternate interior angles',best:[0,1,2],generate:ctx=>transversal(ctx,'alternate-interior')},
 {id:'alternate-exterior',tag:'TRANSVERSAL',name:'Alternate exterior angles',best:[0,1,2],generate:ctx=>transversal(ctx,'alternate-exterior')},
 {id:'same-side-interior',tag:'TRANSVERSAL',name:'Same-side interior angles',best:[0,1,2],generate:ctx=>transversal(ctx,'same-side')},
{id:'angles-open-response-investigation',tag:'INVEST',name:'Four-part parallel lines investigation',best:[2],generate:angleInvestigation}
 ]});
})(typeof window!=='undefined'?window:globalThis);
