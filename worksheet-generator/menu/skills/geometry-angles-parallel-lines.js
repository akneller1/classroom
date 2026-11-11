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

/* Angle pairs named from a numbered figure, and the converse theorems (are the lines parallel?).
   The verifier reads the pair from the figure positions (NS.geoFigures.relationship) or the printed measures (reader "angle-pair"). */
var PAIRNAME={'corresponding':'Corresponding angles','alternate-interior':'Alternate interior angles','alternate-exterior':'Alternate exterior angles','same-side-interior':'Same-side interior angles','same-side-exterior':'Same-side exterior angles','vertical':'Vertical angles','linear-pair':'A linear pair'};
function anglePairs(ctx){var r=ctx.rng,c=ctx.c,F=NS.geoFigures,rels=c<=2?['corresponding','vertical','linear-pair','alternate-interior']:['corresponding','alternate-interior','alternate-exterior','same-side-interior','same-side-exterior','vertical','linear-pair'],rel=r.pick(rels),pr=F.positionsFor(rel,r.int(0,3)),a=pr[0],b=pr[1];
 if(r.chance(0.5)){var t=a;a=b;b=t;}
 var nmz=r.pick([['ℓ','m'],['p','q'],['j','k']]),f=fig({kind:'geo-transversal',numbered:true,marks:[],names:nmz}),ask=c>=3&&rel!=='linear-pair'&&r.chance(0.45),others=Object.keys(PAIRNAME).filter(function(k){return k!==rel;});
 if(ask){var phrase=rel==='linear-pair'?'a linear pair':PAIRNAME[rel].toLowerCase();
  return {variant:'geo-pairs-find-'+rel+'-'+c,prompt:'In the figure, lines '+nmz[0]+' and '+nmz[1]+' are parallel and t is a transversal. Name an angle that forms '+phrase+' with ∠'+a+'.',fig:f,
   parts:[{answer:'∠'+b,check:{type:'derive',kind:'angle-pair',alts:[1,2,3,4,5,6,7,8].filter(function(q){return q!==a&&F.relationship(q,a)!==rel;}).slice(0,4).map(function(q){return '∠'+q;})}}],
   steps:[st(PAIRNAME[rel]+(rel==='linear-pair'?' is two adjacent angles that form a straight line.':rel==='vertical'?' are across from each other at the same intersection.':' sit in matching positions as described by the name.'),''),st('One answer: ∠'+b+'.','')],space:[0.5,0.6,0.7]};}
 return {variant:'geo-pairs-name-'+rel+'-'+c,prompt:'In the figure, lines '+nmz[0]+' and '+nmz[1]+' are parallel and t is a transversal. Name the relationship between ∠'+a+' and ∠'+b+'.',fig:f,
  parts:[{answer:PAIRNAME[rel],check:{type:'derive',kind:'angle-pair',alts:r.shuffle(others.slice()).slice(0,4).map(function(k){return PAIRNAME[k];})}}],
  steps:[st(rel==='vertical'||rel==='linear-pair'?'Both angles are at the same intersection.':'One angle is at each intersection.',''),st(/interior/.test(rel)?'Both are between the two lines.':/exterior/.test(rel)?'Both are outside the two lines.':rel==='corresponding'?'They are in the same position at each intersection.':'',''),st('They are '+PAIRNAME[rel].replace(/^A /,'a ').toLowerCase()+'.','')],space:[0.5,0.6,0.7]};}
function parallelConverse(ctx){var r=ctx.rng,c=ctx.c,kinds=c<=2?['corresponding','alternate-interior']:['corresponding','alternate-interior','alternate-exterior','same-side-interior'],k=r.pick(kinds),supp=/same-side/.test(k),name=PAIRNAME[k].toLowerCase().replace(/ angles$/,''),algebra=c>=4&&r.chance(0.55);
 var lead='Lines m and n are cut by transversal t. ∠1 and ∠2 are '+name+' angles. ',conv={'corresponding':'Corresponding Angles Converse','alternate-interior':'Alternate Interior Angles Converse','alternate-exterior':'Alternate Exterior Angles Converse','same-side-interior':'Same-Side Interior Angles Converse'}[k];
 if(algebra){var x=r.int(3,c>=6?20:14),v=r.int(40,140),e1=expr(r,x,v,1,6,60),e2=expr(r,x,supp?180-v:v,1,6,60);K.need(e1.ok&&e2.ok&&e1.e!==e2.e);
  var eq=supp?'('+e1.e+')+('+e2.e+')=180':e1.e+'='+e2.e;
  return {variant:'geo-converse-x-'+k+'-'+c,prompt:lead+'m∠1 = '+M(e1.e)+'° and m∠2 = '+M(e2.e)+'°. Find the value of '+M('x')+' that makes m ∥ n.',
   parts:[{answer:M('x='+x),check:{type:'derive',kind:'angle-pair',alts:['x='+(x+2),'x='+(x-1),'x='+(2*x)]}}],steps:[st('By the '+conv+', m ∥ n when the angles are '+(supp?'supplementary':'congruent')+'.',M(eq)),st('Solve.',M('x='+x))],space:[1.0,1.2,1.4]};}
 var par=r.chance(0.5),a=r.int(35,145),b=supp?(par?180-a:180-a+r.pick([-6,-4,4,6,10])):(par?a:a+r.pick([-5,-3,3,5,8]));K.need(b>0&&b<180);
 return {variant:'geo-converse-yn-'+(par?'y':'n')+'-'+k+'-'+c,prompt:lead+'m∠1 = '+a+'° and m∠2 = '+b+'°. Are lines m and n parallel? Explain.',
  parts:[{answer:par?'Yes. The '+name+' angles are '+(supp?'supplementary':'congruent')+', so m ∥ n by the '+conv+'.':'No. '+(supp?'The angles are not supplementary':'The angles are not congruent')+', so the lines are not parallel.',check:{type:'derive',kind:'angle-pair'}}],
  steps:[st('If the lines were parallel, '+name+' angles would be '+(supp?'supplementary (sum 180°)':'congruent')+'.',''),st(supp?'Here the sum is '+(a+b)+'°.':'Here the measures are '+a+'° and '+b+'°.',''),st(par?'So m ∥ n by the '+conv+'.':'So the lines are not parallel.','')],space:[0.8,1.0,1.2]};}

/* Two transversals that meet on one parallel line, and two-column parallel-line proofs on the numbered figure. */
function twoTrans(ctx){var r=ctx.rng,c=ctx.c,a=r.int(30,95),b=r.int(30,95);K.need(a+b<=150&&a!==b);
 var sets=c<=2?[['Q','R','PM']]:c<=4?[['Q','R','PM'],['PL','PM','R'],['Q','PR','PM']]:[['PL','PM','R'],['Q','PM','PR'],['PL','PR','PM'],['PM','R','Q']],pick=r.pick(sets),V={Q:a,R:b,PL:a,PR:b,PM:180-a-b},lab={};
 lab[pick[0]]=V[pick[0]]+'°';lab[pick[1]]=V[pick[1]]+'°';lab[pick[2]]='x°';
 var where={Q:'at Q',R:'at R',PL:'at P (left of the transversals)',PR:'at P (right of the transversals)',PM:'at P (between the transversals)'};
 var why=[];if(pick.indexOf('PL')>=0||pick.indexOf('Q')>=0)why.push(st('The angle at Q and the left angle at P are alternate interior angles, so they are congruent ('+a+'°).'));
 if(pick.indexOf('PR')>=0||pick.indexOf('R')>=0)why.push(st('The angle at R and the right angle at P are alternate interior angles ('+b+'°).'));
 why.push(st('The three angles at P form a straight angle on line m: '+a+'° + (middle) + '+b+'° = 180°.'));
 return {variant:'geo-two-trans-'+pick.join('-')+'-'+c,prompt:'Lines m and n are parallel, and two transversals meet at point P on line m. Find the value of '+M('x')+'.',fig:{kind:'geo-two-trans',a:a,b:b,lab:lab},
  parts:[{answer:M('x='+V[pick[2]]),check:{type:'derive',kind:'two-trans',alts:[M('x='+(180-V[pick[2]])),M('x='+(V[pick[0]]+V[pick[1]])),M('x='+Math.abs(V[pick[0]]-V[pick[1]]))].filter(function(z,i,arr){return z!==M('x='+V[pick[2]])&&arr.indexOf(z)===i;})}}],
  steps:why.concat([st('So x = '+V[pick[2]]+'.')]),space:[0.9,1.1,1.3]};}
var PR_NAME={'corresponding':'Corresponding Angles Postulate','alternate-interior':'Alternate Interior Angles Theorem','alternate-exterior':'Alternate Exterior Angles Theorem','same-side-interior':'Same-Side Interior Angles Theorem'};
var PR_CONV={'corresponding':'Corresponding Angles Converse','alternate-interior':'Alternate Interior Angles Converse','alternate-exterior':'Alternate Exterior Angles Converse','same-side-interior':'Same-Side Interior Angles Converse'};
function parProof(ctx){var r=ctx.rng,c=ctx.c,F=NS.geoFigures,REL=function(a,b){return F.relationship(a,b);},nm=r.pick([['ℓ','m'],['p','q'],['j','k']]),P=nm[0]+' ∥ '+nm[1],A=[1,2,3,4,5,6,7,8],t,rows,given,prove;
 var find=function(test){var all=[];A.forEach(function(a){A.forEach(function(b){A.forEach(function(z){if(a!==b&&b!==z&&a!==z&&test(a,b,z))all.push([a,b,z]);});});});K.need(all.length);return r.pick(all);};
 var kinds=c<=2?['vt']:c<=4?['vt','pv']:['vt','pv','ssi','supp'];t=r.pick(kinds);
 var cg=function(a,b){return '∠'+a+' ≅ ∠'+b;},sp=function(a,b){return '∠'+a+' and ∠'+b+' are supplementary';},lp=function(a,b){return '∠'+a+' and ∠'+b+' form a linear pair';};
 if(t==='vt'){var q=find(function(a,b,z){return REL(b,z)==='vertical'&&['corresponding','alternate-interior','alternate-exterior'].indexOf(REL(a,z))>=0&&REL(a,b)!=='none';}),rel=REL(q[0],q[2]);
  given=cg(q[0],q[1]);prove=P;rows=[[given,'Given'],[cg(q[1],q[2]),'Vertical Angles Theorem'],[cg(q[0],q[2]),'Transitive Property of Congruence'],[P,PR_CONV[rel]]];}
 else if(t==='pv'){var q2=find(function(a,b,z){return ['corresponding','alternate-interior','alternate-exterior'].indexOf(REL(a,b))>=0&&REL(b,z)==='vertical'&&REL(a,z)!=='vertical';});
  given=P;prove=cg(q2[0],q2[2]);rows=[[P,'Given'],[cg(q2[0],q2[1]),PR_NAME[REL(q2[0],q2[1])]],[cg(q2[1],q2[2]),'Vertical Angles Theorem'],[cg(q2[0],q2[2]),'Transitive Property of Congruence']];}
 else if(t==='ssi'){var q3=find(function(a,b,z){return ['corresponding','alternate-interior'].indexOf(REL(a,b))>=0&&REL(b,z)==='linear-pair'&&REL(a,z)!=='none'&&REL(a,z)!=='linear-pair';});
  given=P;prove=sp(q3[0],q3[2]);rows=[[P,'Given'],[cg(q3[0],q3[1]),PR_NAME[REL(q3[0],q3[1])]],[lp(q3[1],q3[2]),'Definition of a linear pair'],[sp(q3[1],q3[2]),'Linear Pair Theorem'],[sp(q3[0],q3[2]),'Substitution Property']];}
 else {var q4=find(function(a,b,z){return REL(a,b)==='same-side-interior'&&REL(b,z)==='linear-pair'&&['corresponding','alternate-interior','alternate-exterior'].indexOf(REL(a,z))>=0;});
  given=sp(q4[0],q4[1]);prove=P;rows=[[given,'Given'],[lp(q4[1],q4[2]),'Definition of a linear pair'],[sp(q4[1],q4[2]),'Linear Pair Theorem'],[cg(q4[0],q4[2]),'Congruent Supplements Theorem'],[P,PR_CONV[REL(q4[0],q4[2])]]];}
 if(c>=7&&r.next()<0.45){var f0=fig({kind:'geo-transversal',numbered:true,marks:[],names:nm});f0.proof={rows:rows.map(function(){return {s:'',r:''};}),write:true};
  return {variant:'geo-par-proof-write-'+t+'-'+c,prompt:'Given: '+given+'. Prove: '+prove+'. Write a two-column proof. Give a statement and a reason in each row.',fig:f0,
   parts:[{prompt:'Write the complete proof.',answer:rows.map(function(x,i){return (i+1)+'. '+x[0]+' — '+x[1];}).join('; '),check:{type:'derive',kind:'par-proof'}}],steps:rows.map(function(x){return st(x[0]+' — '+x[1]);}),space:[0.2,0.3,0.4]};}
 var n=c<=2?2:c<=4?3:rows.length-1,cells=r.shuffle(rows.map(function(x,i){return i;}).slice(1)).slice(0,n).sort(),LAB='abcdef',table=rows.map(function(x){return {s:x[0],r:x[1]};}),parts=[];
 cells.forEach(function(ri,i){table[ri].r='';table[ri].rb=LAB[i];parts.push({label:LAB[i],prompt:'Reason for step '+(ri+1),answer:rows[ri][1],check:{type:'derive',kind:'par-proof'}});});
 var para=c>=4&&r.next()<0.35,f=fig({kind:'geo-transversal',numbered:true,marks:[],names:nm});f.proof=para?{rows:table,paragraph:true}:{rows:table};
 return {variant:'geo-par-proof-'+(para?'para-':'')+t+'-'+c,prompt:'Given: '+given+'. Prove: '+prove+'. '+(para?'Complete the paragraph proof by writing each missing reason.':'Complete the two-column proof by writing each missing reason.'),fig:f,parts:parts,
  steps:rows.map(function(x){return st(x[0]+' — '+x[1]);}),space:[0.2,0.3,0.4]};}
 NS.registerSkillSet({id:'geometry-angles-parallel-lines',course:'geometry',courseName:'Geometry',unit:'angles-parallel-lines',unitName:'Angles and Parallel Lines',title:'Angle Relationships',
 tags:{PAIRS:'Angle pairs and the converse theorems',INVEST:'Four-part parallel-lines investigation',COMPLEMENT:'Complementary angles',SUPPLEMENT:'Supplementary angles',VERTICAL:'Vertical angles',LINEAR:'Linear pairs',TRANSVERSAL:'Parallel lines and transversal angle pairs'},
 reference:'<div class="mm-refgrid"><section><h4>Complementary angles</h4><p>The measures sum to 90°.</p></section><section><h4>Supplementary angles</h4><p>The measures sum to 180°.</p></section></div>',
 gaps:['Parallel-line proofs are completed as two-column or paragraph proofs (missing reasons), or written in full as a two-column proof at the top Honors level. Paragraph proofs written from scratch are not generated.'],skills:[
 {id:'two-transversals',tag:'PAIRS',name:'Two transversals between parallel lines',best:[0,1,2],generate:ctx=>K.retry(()=>twoTrans(ctx))},
 {id:'parallel-lines-proof',tag:'PAIRS',name:'Two-column parallel-line proofs (missing reasons)',best:[1,2],generate:ctx=>K.retry(()=>parProof(ctx))},
 {id:'complementary-angles',tag:'COMPLEMENT',name:'Complementary angles',best:[0,1],generate:ctx=>angle(ctx,'complement')},
 {id:'supplementary-angles',tag:'SUPPLEMENT',name:'Supplementary angles',best:[0,1],generate:ctx=>angle(ctx,'supplement')},
 {id:'vertical-angles',tag:'VERTICAL',name:'Vertical angles',best:[0,1],generate:vertical},
 {id:'linear-pairs',tag:'LINEAR',name:'Linear pairs',best:[0,1],generate:linearPair},
 {id:'corresponding-angles',tag:'TRANSVERSAL',name:'Corresponding angles',best:[0,1],generate:ctx=>transversal(ctx,'corresponding')},
 {id:'alternate-interior',tag:'TRANSVERSAL',name:'Alternate interior angles',best:[0,1],generate:ctx=>transversal(ctx,'alternate-interior')},
 {id:'alternate-exterior',tag:'TRANSVERSAL',name:'Alternate exterior angles',best:[0,1],generate:ctx=>transversal(ctx,'alternate-exterior')},
 {id:'same-side-interior',tag:'TRANSVERSAL',name:'Same-side interior angles',best:[0,1],generate:ctx=>transversal(ctx,'same-side')},
 {id:'angle-pairs-figure',tag:'PAIRS',name:'Name angle pairs from a diagram',best:[0,1],generate:ctx=>K.retry(()=>anglePairs(ctx))},
 {id:'parallel-lines-converse',tag:'PAIRS',name:'Converse theorems: decide whether lines are parallel',best:[0,1,2],generate:ctx=>K.retry(()=>parallelConverse(ctx))},
{id:'angles-investigation-corresponding',tag:'INVEST',name:'Honors: corresponding, linear pair, alternate exterior and same-side angles',best:[2],generate:invCorresponding},
 {id:'angles-investigation-alternate',tag:'INVEST',name:'Honors: alternate interior, same-side, vertical angles and a linear pair',best:[2],generate:invAlternate},
 {id:'angles-investigation-relations',tag:'INVEST',name:'Honors: complementary, supplementary and vertical angles with algebra',best:[2],generate:invRelations},
 {id:'angles-open-response-investigation',tag:'INVEST',name:'Four-part parallel lines investigation',best:[2],generate:angleInvestigation}
 ]});
})(typeof window!=='undefined'?window:globalThis);
