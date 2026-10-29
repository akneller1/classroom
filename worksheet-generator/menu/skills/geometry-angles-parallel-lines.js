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

/* ---------- Honors investigations (two-sided algebra, chained answers) ----------
   Variants geo-angles-investigation-<name>-<c> use the shared investigation verifier. */
function lin(a,b,v){var t=a===1?v:a+v;return b>0?t+'+'+b:b<0?t+'-'+(-b):t;}
function cn(b){return b<0?'-'+(-b):'+'+b;}
/* build expressions that evaluate to `val` at `x`, with a coefficient in [lo,hi] and a bounded constant */
function expr(r,x,val,lo,hi,lim){var a=r.int(lo,hi),b=val-a*x;return {a:a,b:b,ok:Math.abs(b)<=lim,e:lin(a,b,'x')};}
/* 1: corresponding angles, a linear pair, alternate exterior angles, same-side interior angles */
function invCorresponding(ctx){
 var r=ctx.rng,c=ctx.c,tries=0,x,phi,A,B,y,C,z,D,v,ey,ez;
 do{x=r.int(4,c>=6?24:16);phi=r.int(44,136);A=expr(r,x,phi,2,5,40);B=expr(r,x,phi,1,6,40);
  y=r.int(3,c>=6?20:14);var cy=r.int(2,5),dy=180-phi-cy*y;z=r.int(3,c>=6?20:14);var ez2=r.int(2,5),fz=phi-ez2*z;
  C={a:cy,b:dy,e:lin(cy,dy,'y')};D={a:ez2,b:fz,e:lin(ez2,fz,'z')};tries++;
  if(phi===90||A.a===B.a)A.ok=false;}
 while((!A.ok||!B.ok||Math.abs(dy)>60||Math.abs(fz)>60)&&tries<8000);
 var eA=A.e,eB=B.e,eC=C.e,eD=D.e,other=180-phi;
 var fg=fig({kind:'geo-transversal',names:['ℓ','m'],marks:[{pos:2,text:'('+eA+')°',deg:phi},{pos:6,text:'('+eB+')°',deg:phi},{pos:1,text:'('+eC+')°',deg:other},{pos:7,text:'('+eD+')°',deg:phi},{pos:4,text:'v°',deg:other}]});
 var phiExpr='('+A.a+'*'+x+cn(A.b)+')';
 return {variant:'geo-angles-investigation-corresponding-'+c,fig:fg,
  prompt:'Open Response: Lines ℓ and m are parallel and are cut by a transversal, as shown. Use the angle relationship named in each part and show the equation you write.',
  parts:[
   {label:'a',prompt:'The angles marked '+M('('+eA+')')+'° and '+M('('+eB+')')+'° are corresponding angles. Find x.',answer:M('x='+x),check:{type:'solve',eq:eA+'='+eB,v:'x'}},
   {label:'b',prompt:'The angle marked '+M('('+eC+')')+'° forms a linear pair with the angle marked '+M('('+eA+')')+'°. Use your value of x to find y.',answer:M('y='+y),check:{type:'solve',eq:'('+eC+')+'+phiExpr+'=180',v:'y'}},
   {label:'c',prompt:'The angle marked '+M('('+eD+')')+'° and the angle marked '+M('('+eA+')')+'° are alternate exterior angles. Find z.',answer:M('z='+z),check:{type:'solve',eq:eD+'='+phiExpr,v:'z'}},
   {label:'d',prompt:'The angle marked v° and the angle marked '+M('('+eB+')')+'° are same-side interior angles. Find v.',answer:M('v='+other),check:{type:'solve',eq:'v=180-('+B.a+'*'+x+cn(B.b)+')',v:'v'}}
  ],
  steps:[st('Corresponding angles are congruent, so '+M(eA+'='+eB)+'.',M('x='+x)),st('A linear pair adds to 180, so '+M('('+eC+')+'+phiExpr+'=180')+'.',M('y='+y)),st('Alternate exterior angles are congruent, so '+M(eD+'='+phiExpr)+'.',M('z='+z)),st('Same-side interior angles add to 180, so '+M('v=180-('+B.a+'*'+x+cn(B.b)+')')+'.',M('v='+other))],
  space:[3,3.6,4.2]};
}
/* 2: alternate interior angles, same-side interior angles, vertical angles, a linear pair */
function invAlternate(ctx){
 var r=ctx.rng,c=ctx.c,tries=0,x,phi,A,B,y,cy,dy,z,ez,fz,other;
 do{x=r.int(4,c>=6?24:16);phi=r.int(44,136);A=expr(r,x,phi,2,5,40);B=expr(r,x,phi,1,6,40);other=180-phi;
  y=r.int(3,c>=6?20:14);cy=r.int(2,5);dy=other-cy*y;z=r.int(3,c>=6?20:14);ez=r.int(2,5);fz=other-ez*z;tries++;
  if(phi===90||A.a===B.a)A.ok=false;}
 while((!A.ok||!B.ok||Math.abs(dy)>60||Math.abs(fz)>60)&&tries<8000);
 var eA=A.e,eB=B.e,eC=lin(cy,dy,'y'),eD=lin(ez,fz,'z');
 var fg=fig({kind:'geo-transversal',names:['ℓ','m'],marks:[{pos:3,text:'('+eA+')°',deg:phi},{pos:6,text:'('+eB+')°',deg:phi},{pos:5,text:'('+eC+')°',deg:other},{pos:8,text:'('+eD+')°',deg:other},{pos:2,text:'w°',deg:phi}]});
 var phiExpr='('+A.a+'*'+x+cn(A.b)+')',oth='('+cy+'*'+y+cn(dy)+')';
 return {variant:'geo-angles-investigation-alternate-'+c,fig:fg,
  prompt:'Open Response: Lines ℓ and m are parallel and are cut by a transversal, as shown. Use the angle relationship named in each part and show the equation you write.',
  parts:[
   {label:'a',prompt:'The angles marked '+M('('+eA+')')+'° and '+M('('+eB+')')+'° are alternate interior angles. Find x.',answer:M('x='+x),check:{type:'solve',eq:eA+'='+eB,v:'x'}},
   {label:'b',prompt:'The angle marked '+M('('+eC+')')+'° and the angle marked '+M('('+eA+')')+'° are same-side interior angles. Use your value of x to find y.',answer:M('y='+y),check:{type:'solve',eq:'('+eC+')+'+phiExpr+'=180',v:'y'}},
   {label:'c',prompt:'The angle marked '+M('('+eD+')')+'° is vertical to the angle marked '+M('('+eC+')')+'°. Use your value of y to find z.',answer:M('z='+z),check:{type:'solve',eq:eD+'='+oth,v:'z'}},
   {label:'d',prompt:'The angle marked w° and the angle marked '+M('('+eC+')')+'° form a linear pair. Find w.',answer:M('w='+phi),check:{type:'solve',eq:'w=180-'+oth,v:'w'}}
  ],
  steps:[st('Alternate interior angles are congruent, so '+M(eA+'='+eB)+'.',M('x='+x)),st('Same-side interior angles add to 180, so '+M('('+eC+')+'+phiExpr+'=180')+'.',M('y='+y)),st('Vertical angles are congruent, so '+M(eD+'='+oth)+'.',M('z='+z)),st('A linear pair adds to 180, so '+M('w=180-'+oth)+'.',M('w='+phi))],
  space:[3,3.6,4.2]};
}
/* 3: complementary, supplementary and vertical angle relationships with algebra (no transversal) */
function invRelations(ctx){
 var r=ctx.rng,c=ctx.c,tries=0,x,a1,b1,a2,b2,ang1,ang2,y,c1,d1,ang3,z,e1,f1;
 do{x=r.int(4,c>=6?20:14);ang1=r.int(20,70);a1=r.int(2,5);b1=ang1-a1*x;ang2=90-ang1;a2=r.int(1,5);b2=ang2-a2*x;
  y=r.int(3,c>=6?20:14);ang3=180-ang1;c1=r.int(2,5);d1=ang3-c1*y;z=r.int(3,c>=6?20:14);e1=r.int(2,5);f1=ang3-e1*z;tries++;}
 while((Math.abs(b1)>50||Math.abs(b2)>50||a1===a2||Math.abs(d1)>60||Math.abs(f1)>60||ang1<15||ang2<15||a1*x+a2*x>200)&&tries<8000);
 var e1x=lin(a1,b1,'x'),e2x=lin(a2,b2,'x'),e3y=lin(c1,d1,'y'),e4z=lin(e1,f1,'z');
 var diff=ang3-ang2;
 return {variant:'geo-angles-investigation-relations-'+c,
  prompt:'Open Response: Angle 1 and angle 2 are complementary. Angle 1 measures '+M('('+e1x+')')+' degrees and angle 2 measures '+M('('+e2x+')')+' degrees. Angle 3 is supplementary to angle 1 and measures '+M('('+e3y+')')+' degrees. Angle 4 is vertical to angle 3 and measures '+M('('+e4z+')')+' degrees. Name the angle relationship you use in every part and show the equation you write.',
  parts:[
   {label:'a',prompt:'Angles 1 and 2 are complementary. Find x.',answer:M('x='+x),check:{type:'solve',eq:'('+e1x+')+('+e2x+')=90',v:'x'}},
   {label:'b',prompt:'Angle 3 is supplementary to angle 1. Use your value of x to find y.',answer:M('y='+y),check:{type:'solve',eq:'('+e3y+')+('+a1+'*'+x+cn(b1)+')=180',v:'y'}},
   {label:'c',prompt:'Angle 4 is vertical to angle 3. Use your value of y to find z.',answer:M('z='+z),check:{type:'solve',eq:e4z+'=('+c1+'*'+y+cn(d1)+')',v:'z'}},
   {label:'d',prompt:'Find how many degrees larger angle 3 is than angle 2.',answer:M('w='+diff),check:{type:'solve',eq:'w=('+c1+'*'+y+cn(d1)+')-('+a2+'*'+x+cn(b2)+')',v:'w'}}
  ],
  steps:[st('Complementary angles add to 90, so '+M('('+e1x+')+('+e2x+')=90')+'.',M('x='+x)),st('Supplementary angles add to 180, so '+M('('+e3y+')+('+a1+'*'+x+cn(b1)+')=180')+'.',M('y='+y)),st('Vertical angles are congruent, so '+M(e4z+'=('+c1+'*'+y+cn(d1)+')')+'.',M('z='+z)),st('Subtract the measure of angle 2 from the measure of angle 3: '+M('w=('+c1+'*'+y+cn(d1)+')-('+a2+'*'+x+cn(b2)+')')+'.',M('w='+diff))],
  space:[3,3.6,4.2]};
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
 {id:'complementary-angles',tag:'COMPLEMENT',name:'Complementary angles',best:[0,1],generate:ctx=>angle(ctx,'complement')},
 {id:'supplementary-angles',tag:'SUPPLEMENT',name:'Supplementary angles',best:[0,1],generate:ctx=>angle(ctx,'supplement')},
 {id:'vertical-angles',tag:'VERTICAL',name:'Vertical angles',best:[0,1],generate:vertical},
 {id:'linear-pairs',tag:'LINEAR',name:'Linear pairs',best:[0,1],generate:linearPair},
 {id:'corresponding-angles',tag:'TRANSVERSAL',name:'Corresponding angles',best:[0,1],generate:ctx=>transversal(ctx,'corresponding')},
 {id:'alternate-interior',tag:'TRANSVERSAL',name:'Alternate interior angles',best:[0,1],generate:ctx=>transversal(ctx,'alternate-interior')},
 {id:'alternate-exterior',tag:'TRANSVERSAL',name:'Alternate exterior angles',best:[0,1],generate:ctx=>transversal(ctx,'alternate-exterior')},
 {id:'same-side-interior',tag:'TRANSVERSAL',name:'Same-side interior angles',best:[0,1],generate:ctx=>transversal(ctx,'same-side')},
{id:'angles-investigation-corresponding',tag:'INVEST',name:'Honors: corresponding, linear pair, alternate exterior and same-side angles',best:[2],generate:invCorresponding},
 {id:'angles-investigation-alternate',tag:'INVEST',name:'Honors: alternate interior, same-side, vertical angles and a linear pair',best:[2],generate:invAlternate},
 {id:'angles-investigation-relations',tag:'INVEST',name:'Honors: complementary, supplementary and vertical angles with algebra',best:[2],generate:invRelations},
 {id:'angles-open-response-investigation',tag:'INVEST',name:'Four-part parallel lines investigation',best:[2],generate:angleInvestigation}
 ]});
})(typeof window!=='undefined'?window:globalThis);
