/* Verified text-first Geometry Unit 3 starter bank. No diagram is implied. */
(function(G){'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function corresponding(ctx,kind){
 var r=ctx.rng,c=ctx.c,x=r.int(3,c>=5?30:18),a=c>=5?r.int(2,4):1,b=r.int(1,12),value=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+value;
 var feature=kind==='side'?'corresponding sides':'corresponding angles';
 var unit=kind==='side'?' units':' degrees';
 var ex=(a===1?'x':a+'x')+'+'+b;
 return {compactPrompt:'Triangle ABC ≅ triangle DEF. '+(kind==='side'?'AB = '+M(ex)+' and DE = '+value+'.':'m∠B = '+M(ex)+' and m∠E = '+value+' degrees.')+' Find x.',variant:'geo-congruence-'+kind+'-'+c,
 fig:kind==='side'?{kind:'geo-cong-pair',sides:{AB:ex,DE:String(value)},description:'Congruent triangles with corresponding sides AB and DE labelled'}:{kind:'geo-cong-pair',angles:{B:'('+ex+')°',E:value+'°'},arcs:{B:1,E:1},description:'Congruent triangles with corresponding angles B and E labelled'},
 prompt:'Triangles ABC and DEF are congruent, with A corresponding to D, B to E, and C to F. '+(kind==='side'?'AB and DE':'angle B and angle E')+' are '+feature+'. Their measures are '+M((a===1?'x':a+'x')+'+'+b)+' and '+value+unit+'. Find x. Set up an equation and show your reasoning.',
 parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
 steps:[step('Corresponding parts of congruent triangles are congruent.',M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};
}
function thirdAngle(ctx){
 var r=ctx.rng,c=ctx.c,x=r.int(25,85),other=r.int(25,Math.min(85,150-x)),third=180-x-other;
 var eq='x+'+other+'+'+third+'=180';
 return {compactPrompt:'Triangle ABC ≅ triangle DEF. m∠A = '+other+'° and m∠C = '+third+'°. Use '+M(eq)+' to find x, the measure of ∠B.',variant:'geo-congruence-third-angle-'+c,fig:{kind:'geo-cong-pair',angles:{A:other+'°',B:'x°',C:third+'°'},arcs:{A:1,D:1,B:2,E:2},description:'Triangles ABC and DEF with matching marked angles at A, D and B, E'},prompt:'Triangles ABC and DEF have angle A congruent to angle D and angle B congruent to angle E. In triangle ABC, angle A is '+other+'° and angle C is '+third+'°. Find angle B, called x, and explain why angle F must equal angle C. Use '+M(eq)+' to find x.',
 parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
 steps:[step('Use the triangle angle sum.',M(eq)),step('The third angles match because both triangles sum to 180°.',M('x='+x))],space:[1.2,1.5,1.8]};
}
function perimeter(ctx){
 var r=ctx.rng,c=ctx.c,a=r.int(5,16),b=r.int(5,16),x=r.int(Math.abs(a-b)+1,a+b-1),p=x+a+b,eq='x+'+a+'+'+b+'='+p;
 return {compactPrompt:'Triangle ABC ≅ triangle DEF. ABC has sides x, '+a+' and '+b+'. DEF has perimeter '+p+'. Find x.',variant:'geo-congruence-perimeter-'+c,fig:{kind:'geo-cong-pair',sides:{AB:'x',BC:String(a),CA:String(b)},note:'The perimeter of triangle DEF is '+p+' units.',description:'Triangle ABC with side lengths x, '+a+' and '+b+', and congruent triangle DEF'},prompt:'Triangle ABC is congruent to triangle DEF. The side lengths of ABC are x, '+a+', and '+b+' units. The perimeter of DEF is '+p+' units. Find x. Set up an equation and show your reasoning.',
 parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
 steps:[step('Congruent triangles have equal perimeters.',M(eq)),step('Solve for the unknown side.',M('x='+x))],space:[1.2,1.5,1.8]};
}

/* Criterion-specific CPCTC applications. Each question explicitly supplies the
   included angle / corresponding side information required by its criterion. */
function criterion(ctx,kind){
 var r=ctx.rng,c=ctx.c,x=r.int(4,c>=5?42:28),a=c>=5?r.int(2,5):1,b=r.int(1,19);
 var expression=(a===1?'x':a+'x')+'+'+b,measure=a*x+b,eq=expression+'='+measure;
 var letters=['ABC','DEF'],fact='',target='',why='';
 if(kind==='sss'){
  fact='AB = DE, BC = EF, and AC = DF. Thus all three pairs of corresponding sides are equal (SSS).';
  target='AB = '+M(expression)+' units and DE = '+measure+' units.';
  why='SSS establishes triangle congruence; corresponding sides are equal.';
 }else if(kind==='sas'){
  fact='AB = DE and AC = DF, and included angles A and D are congruent (SAS).';
  target='BC = '+M(expression)+' units and EF = '+measure+' units.';
  why='SAS establishes congruence; the remaining corresponding sides are equal.';
 }else if(kind==='asa'){
  fact='Angles A and D are congruent, angles B and E are congruent, and the included sides AB and DE are equal (ASA).';
  target='AC = '+M(expression)+' units and DF = '+measure+' units.';
  why='ASA establishes congruence; corresponding sides are equal.';
 }else if(kind==='aas'){
  fact='Angles A and D are congruent, angles B and E are congruent, and non-included sides AC and DF are equal (AAS).';
  target='BC = '+M(expression)+' units and EF = '+measure+' units.';
  why='AAS establishes congruence; corresponding sides are equal.';
 }else{
  fact='Both triangles are right triangles with right angles at B and E. Their hypotenuses AC and DF are equal, and legs AB and DE are equal (HL).';
  target='BC = '+M(expression)+' units and EF = '+measure+' units.';
  why='HL establishes congruence of right triangles; corresponding legs are equal.';
 }
 var cf=NS.geoFigures&&NS.geoFigures.cong?NS.geoFigures.cong.pair(kind,r.int(0,1)===1):{kind:'geo-triangle-pair',criterion:kind};
 if(cf.kind==='geo-cong'){var tk=kind==='asa'?['AC','DF']:['BC','EF'];if(kind==='sss')tk=['AB','DE'];cf.lab={};cf.lab[tk[0]]=expression;cf.lab[tk[1]]=String(measure);}
 return {compactPrompt:'Triangles ABC and DEF are congruent by '+kind.toUpperCase()+'. '+target+' Find x.',variant:'geo-criterion-'+kind+'-'+c,fig:cf,
  prompt:'Triangles ABC and DEF have the correspondence A to D, B to E, and C to F. '+fact+' '+target+' Find x. State why the triangles are congruent, then set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step(why,M(eq)),step('Solve for the unknown value.',M('x='+x))],
  space:[1.2,1.5,1.8]};
}

function identify(ctx){
 var r=ctx.rng,c=ctx.c,kinds=['sss','sas','asa','aas','hl','ssa','aaa'];
 var kind=kinds[r.int(0,kinds.length-1)],setting=r.int(0,5),answer=(kind==='ssa'||kind==='aaa')?'NOT SUFFICIENT':kind.toUpperCase();
 return {compactPrompt:'Do the markings prove the triangles congruent? Give the criterion (SSS, SAS, ASA, AAS, HL) or NOT SUFFICIENT.',variant:'geo-identify-criterion-'+kind+'-'+c,
  fig:NS.geoFigures&&NS.geoFigures.cong?NS.geoFigures.cong.pair(kind,r.int(0,1)===1):{kind:'geo-triangle-pair',criterion:kind},
  prompt:['Use the marked triangle pairs to determine whether triangle congruence is established.','Examine the two marked triangles and decide whether their congruence is guaranteed.','A student claims the marked triangles must be congruent. Decide whether the markings justify that claim.','Determine what, if anything, the equal sides and angles establish about the triangles.','Inspect the given triangle markings and identify the applicable congruence rule, if one exists.','Consider only the marked information. Is triangle congruence guaranteed?'][setting]+' Identify the criterion (SSS, SAS, ASA, AAS, or HL), or write NOT SUFFICIENT if the markings do not prove congruence. Matching tick marks and angle arcs indicate corresponding equal parts. The diagram is schematic and not to scale.',
  parts:[{answer:answer,check:{type:'geo-congruence-criterion'}}],
  steps:[step(kind==='ssa'?'SSA is not a valid general triangle congruence theorem.':kind==='aaa'?'AAA establishes similarity, not necessarily congruence.':'The marked corresponding parts establish '+answer+' congruence.',answer)],
  space:[1.2,1.5,1.8]};
}

function structuredProof(ctx){
 var r=ctx.rng,c=ctx.c,shared=r.int(0,1)===0,flow=r.int(0,1)===0;
 var a=c>=5?r.int(2,5):1,b=r.int(1,19),x=r.int(5,Math.min(c>=5?48:30,Math.floor((169-b)/a))),v=a*x+b;
 var expression=(a===1?'x':a+'x')+'+'+b,eq=expression+'='+v;
 var givens,first,triangles,consequence,angleEquality;
 if(shared){
  givens='Triangles ABC and ABD share side AB. Given AC = AD and BC = BD.';
  first='AB is congruent to AB';
  triangles='triangle ABC is congruent to triangle ABD';
  consequence='angle ACB = '+M(expression)+' degrees and angle ADB = '+v+' degrees';
  angleEquality='Angle ACB is congruent to angle ADB';
 }else{
  givens='Lines AC and BD intersect at O. Given AO = CO and BO = DO.';
  first='angle AOB is congruent to angle COD';
  triangles='triangle AOB is congruent to triangle COD';
  consequence='angle OAB = '+M(expression)+' degrees and angle OCD = '+v+' degrees';
  angleEquality='Angle OAB is congruent to angle OCD';
 }
 var lead=flow?'Complete the following flow proof.':'Complete the following two-column proof.';
 return {variant:'geo-structured-proof-'+(shared?'shared':'vertical')+'-'+(flow?'flow':'columns')+'-'+c,
  fig:(function(){var f=shared?NS.geoFigures.cong.shared():NS.geoFigures.cong.cross();f.nts=true;f.note='Not drawn to scale.';f.angLab=shared?[{p:'A',v:'C',q:'B',text:expression+'°'},{p:'A',v:'D',q:'B',text:v+'°'}]:[{p:'B',v:'A',q:'O',text:expression+'°'},{p:'D',v:'C',q:'O',text:v+'°'}];return f;})(),
  proofStatements:[first,triangles,angleEquality,'Solve '+M(eq)+' for x'],
  prompt:givens+' '+consequence+'. '+lead+' Establish: (1) '+first+'; (2) '+triangles+'; (3) the listed corresponding angles are congruent. Supply the reason for each step, then write and solve an equation for x.',
  parts:[
   {prompt:'Reason for step 1:',answer:shared?'REFLEXIVE PROPERTY':'VERTICAL ANGLES THEOREM',check:{type:'geo-proof-reason',stage:'first'}},
   {prompt:'Reason for step 2:',answer:shared?'SSS':'SAS',check:{type:'geo-proof-reason',stage:'congruence'}},
   {prompt:'Reason for step 3:',answer:'CPCTC',check:{type:'geo-proof-reason',stage:'consequence'}},
   {prompt:'Find x:',answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}
  ],
  steps:[
   step('Step 1: '+first,shared?'Reflexive Property':'Vertical Angles Theorem'),
   step('Step 2: '+triangles,shared?'SSS':'SAS'),
   step('Step 3: Corresponding angles are congruent.','CPCTC'),
   step('Step 4: Solve the corresponding angle equation.',M(eq)+' '+M('x='+x))
  ],space:[1.8,2.2,2.6]};
}

/* ---------- Multi-step investigations (Honors rigor) ----------
   Each is a four-part Open Response chain: every part needs congruence reasoning AND algebra, and later parts use earlier results.
   Variant names start geo-congruence-investigation-: the verifier lets each part's equation use only printed numbers,
   a standard constant, or an earlier answer. */
function lin(a,b,v){var t=a===1?v:a===-1?'-'+v:a+v;return b>0?t+'+'+b:b<0?t+'-'+(-b):t;}
function geoPair(labels,angLab){
 var f=NS.geoFigures&&NS.geoFigures.cong?NS.geoFigures.cong.pair('sss',false):{kind:'geo-triangle-pair',criterion:'sss'};
 if(f.kind==='geo-cong'){f.lab=labels||{};if(angLab)f.angLab=angLab;f.note='Not drawn to scale.';}
 return f;
}
/* 1: algebra chain on two congruent triangles */
function investigationAlgebra(ctx){
 var r=ctx.rng,c=ctx.c,hi=c>=6;
 var x,y,a2,a1,b2,ab,b1,pc,bc,u,w,ac,tries=0;
 do{x=r.int(4,hi?18:12);y=r.int(3,hi?16:11);a2=r.int(1,4);a1=a2+r.int(1,4);b2=r.int(2,15);ab=a2*x+b2;b1=ab-a1*x;
  pc=r.int(2,5);bc=pc*y+x;u=r.int(2,6);w=r.int(1,3);ac=u*x-w*y;tries++;}
 while((ac<3||ac+ab<=bc||ab+bc<=ac||ac+bc<=ab)&&tries<2000);   // sides must form a real triangle
 var per=ab+bc+ac;
 var g2=r.int(1,3),g1=g2+r.int(1,3),z=r.int(8,hi?32:24),h2=r.int(4,20),fv=g2*z+h2,h1=fv-g1*z;
 var eAB=lin(a1,b1,'x'),eDE=lin(a2,b2,'x'),eBC=lin(pc,0,'y')+'+x',eAC=lin(u,0,'x')+'-'+(w===1?'':w)+'y',eC=lin(g1,h1,'z'),eF=lin(g2,h2,'z');
 var e1=eAB+'='+eDE,e2=pc+'*y+'+x+'='+bc,e3='w='+ab+'+'+bc+'+'+ac;
 var e3b='w=('+a1+'*'+x+(b1<0?'-'+(-b1):'+'+b1)+')+('+pc+'*'+y+'+'+x+')+('+u+'*'+x+'-'+w+'*'+y+')';
 var e4=eC+'='+eF;
 var fig=geoPair({AB:eAB,DE:eDE,BC:eBC,EF:String(bc)},[{p:'A',v:'C',q:'B',text:'('+eC+')°'},{p:'D',v:'F',q:'E',text:'('+eF+')°'}]);
 return {variant:'geo-congruence-investigation-algebra-'+c,fig:fig,
  prompt:'Open Response: Triangle ABC is congruent to triangle DEF with A corresponding to D, B to E, and C to F. AB = '+M(eAB)+' and DE = '+M(eDE)+'. BC = '+M(eBC)+' and EF = '+bc+'. AC = '+M(eAC)+'. The measure of angle C is '+M('('+eC+')')+' degrees and the measure of angle F is '+M('('+eF+')')+' degrees. Use the congruence to answer every part, and show the equation you write.',
  parts:[
   {label:'a',prompt:'Use AB and DE to find x.',answer:M('x='+x),check:{type:'solve',eq:e1,v:'x'}},
   {label:'b',prompt:'Use BC and EF, and your value of x, to find y.',answer:M('y='+y),check:{type:'solve',eq:e2.replace(pc+'*y+'+x,pc+'*y+'+x),v:'y'}},
   {label:'c',prompt:'Find the perimeter of triangle ABC using your values of x and y.',answer:M('w='+per),check:{type:'solve',eq:e3b,v:'w'}},
   {label:'d',prompt:'Use angles C and F to find z.',answer:M('z='+z),check:{type:'solve',eq:e4,v:'z'}}
  ],
  steps:[step('Corresponding sides are congruent, so '+M(e1)+'.',M('x='+x)),step('BC = EF. Substitute x = '+x+': '+M(e2)+'.',M('y='+y)),step('Add the three side lengths: AB = '+ab+', BC = '+bc+', AC = '+ac+'.',M('w='+per)),step('Corresponding angles are congruent, so '+M(e4)+'.',M('z='+z))],
  space:[3,3.6,4.2]};
}
/* 2: isosceles triangle split by a median, SSS then angle chase */
function investigationIsosceles(ctx){
 var r=ctx.rng,c=ctx.c,x=r.int(3,c>=6?16:12),a=r.int(2,5),b=r.int(-9,15),half=a*x+b;
 while(half<18||half>70){x=r.int(3,16);a=r.int(2,5);b=r.int(-9,15);half=a*x+b;}
 var vertex=2*half,base=(180-vertex)/2;
 var tn=Math.tan(half*Math.PI/180),P={B:[-tn,0],C:[tn,0],A:[0,1],D:[0,0]};   // drawn to the printed angle
 var fig={kind:'geo-cong',pts:P,segs:[['A','B'],['B','C'],['C','A'],['A','D']],tris:null,
  sides:[{s:[['A','B'],['A','C']],n:1},{s:[['B','D'],['D','C']],n:2}],angles:[],right:[],
  angLab:[{p:'B',v:'A',q:'D',text:'('+lin(a,b,'x')+')°'},{p:'D',v:'A',q:'C',text:half+'°'}],note:'Not drawn to scale.'};
 var eBAD=lin(a,b,'x');
 return {variant:'geo-congruence-investigation-isosceles-'+c,fig:fig,
  prompt:'Open Response: In triangle ABC, AB = AC. D is the midpoint of BC, and segment AD is drawn. Angle BAD measures '+M('('+eBAD+')')+' degrees and angle CAD measures '+half+' degrees. Triangles ABD and ACD are congruent. Answer every part and name the congruence criterion or theorem you use.',
  parts:[
   {label:'a',prompt:'Use the congruent triangles to find x. (Which criterion proves ABD is congruent to ACD?)',answer:M('x='+x),check:{type:'solve',eq:eBAD+'='+half,v:'x'}},
   {label:'b',prompt:'Find the measure of angle BAC, in degrees.',answer:M('w='+vertex),check:{type:'solve',eq:'w='+half+'+'+half,v:'w'}},
   {label:'c',prompt:'Find the measure of angle B, in degrees. Explain why angle C has the same measure.',answer:M('w='+base),check:{type:'solve',eq:'w+w+'+vertex+'=180',v:'w'}},
   {label:'d',prompt:'Find the measure of angle ADB, in degrees. Explain using corresponding parts.',answer:M('w=90'),check:{type:'solve',eq:'w+w=180',v:'w'}}
  ],
  steps:[step('Corresponding angles of congruent triangles are congruent (SSS: AB = AC, BD = DC, AD = AD), so '+M(eBAD+'='+half)+'.',M('x='+x)),step('The two angles at A together make angle BAC.',M('w='+half+'+'+half)),step('The base angles are equal and the angles of triangle ABC add to 180, so '+M('w+w+'+vertex+'=180')+'.',M('w='+base)),step('Angles ADB and ADC are congruent (CPCTC) and form a linear pair, so '+M('w+w=180')+'.',M('w=90'))],
  space:[3,3.6,4.2]};
}
/* 3: congruence in the coordinate plane (axis-aligned legs, turned a quarter turn) */
function investigationCoordinate(ctx){
 var r=ctx.rng,c=ctx.c,a=r.int(3,c>=6?12:9),b=r.int(3,c>=6?12:9);
 while(a===b){b=r.int(3,12);}
 var px=r.int(-6,3),py=r.int(-6,3),sx=r.int(-5,5),ty=r.int(-6,3);
 var A=[px,py],B=[px+a,py],Cp=[px+a,py+b],D=[sx,ty],E=[sx,ty+a],fx=sx-b;
 var P=function(q){return '('+q[0]+', '+q[1]+')';};
 var fig={kind:'geo-grid',shapes:[{id:'pre',pts:[A,B,Cp],labels:['A','B','C']},{id:'seg',pts:[D,E],labels:['D','E']}],lines:[],alt:'Coordinate plane with triangle ABC and segment DE'};
 var hyp2=a*a+b*b;
 var ptxt=function(q){return q[0]+', '+q[1];};
 var abE='s='+(px+a)+'-'+(px<0?'('+px+')':px),bcE='t='+(py+b)+'-'+(py<0?'('+py+')':py),deE='u='+(ty+a)+'-'+(ty<0?'('+ty+')':ty);
 return {variant:'geo-congruence-investigation-coordinate-'+c,fig:fig,
  prompt:'Open Response: Triangle ABC has vertices A'+P(A)+', B'+P(B)+', and C'+P(Cp)+'. Triangle DEF has vertices D'+P(D)+', E'+P(E)+', and F(x, '+(ty+a)+') with x less than '+sx+'. You will decide whether the triangles can be congruent with D corresponding to A, E to B, and F to C.',
  parts:[
   {label:'a',prompt:'Find the length AB. Segment AB is horizontal.',answer:M('s='+a),check:{type:'solve',eq:abE,v:'s'}},
   {label:'b',prompt:'Find the length BC. Segment BC is vertical.',answer:M('t='+b),check:{type:'solve',eq:bcE,v:'t'}},
   {label:'c',prompt:'Use the distance formula to find '+M('AC^2')+', the square of the length AC. Leave it as a squared length.',answer:M('k='+hyp2),check:{type:'solve',eq:'k='+a+'*'+a+'+'+b+'*'+b,v:'k'}},
   {label:'d',prompt:'Segment DE is vertical with length '+a+' (the same as AB). For triangle DEF to be congruent to triangle ABC, EF must equal BC. Find the x-coordinate of F.',answer:M('x='+fx),check:{type:'solve',eq:sx+'-x='+b,v:'x'}}
  ],
  steps:[step('The x-coordinates give the length of a horizontal segment: '+M(abE)+'.',M('s='+a)),step('The y-coordinates give the length of a vertical segment: '+M(bcE)+'.',M('t='+b)),step('Distance formula: add the squared horizontal and vertical changes, so '+M('k='+a+'*'+a+'+'+b+'*'+b)+'.',M('k='+hyp2)),step('F lies left of E on the same horizontal line, so EF is the difference of the x-coordinates: '+M(sx+'-x='+b)+'.',M('x='+fx))],
  space:[3,3.6,4.2]};
}
/* 4: overlapping triangles in a quadrilateral (AB parallel and equal to CD, diagonal BD shared) */
function investigationOverlap(ctx){
 var r=ctx.rng,c=ctx.c,x=r.int(4,c>=6?16:12),a2=r.int(1,4),a1=a2+r.int(1,4),b2=r.int(2,14),ab=a2*x+b2,b1=ab-a1*x;
 var m=r.int(2,5),y=r.int(5,c>=6?20:14),n=m*y+r.int(-9,-2),k=m*y-n;
 var p=r.int(2,4),z=r.int(6,c>=6?22:16),q2=r.int(3,14),adb=p*z+q2;
 while(n<20||n>70||adb<20||180-n-adb<25){y=r.int(5,20);n=m*y+r.int(-9,-2);k=m*y-n;z=r.int(6,22);adb=p*z+q2;}
 var angA=180-n-adb;
 var rad=Math.PI/180,db=Math.sin(angA*rad)/Math.sin(adb*rad),Bq=[db*Math.cos(n*rad),db*Math.sin(n*rad)],Pp={D:[0,0],C:[1,0],B:Bq,A:[Bq[0]-1,Bq[1]]};   // triangle CDB drawn with the printed angles
 var fig={kind:'geo-cong',pts:Pp,segs:[['A','B'],['B','C'],['C','D'],['D','A'],['B','D']],tris:null,
  sides:[{s:[['A','B'],['C','D']],n:1}],angles:[],right:[],
  lab:{AB:lin(a1,b1,'x'),CD:lin(a2,b2,'x')},
  angLab:[{p:'A',v:'B',q:'D',text:'('+lin(m,-k,'y')+')°'},{p:'C',v:'D',q:'B',text:n+'°'},{p:'A',v:'D',q:'B',text:'('+lin(p,q2,'z')+')°'},{p:'C',v:'B',q:'D',text:adb+'°'}],note:'Not drawn to scale.'};
 var eAB=lin(a1,b1,'x'),eCD=lin(a2,b2,'x'),eY=lin(m,-k,'y'),eZ=lin(p,q2,'z');
 return {variant:'geo-congruence-investigation-overlap-'+c,fig:fig,
  prompt:'Open Response: In quadrilateral ABCD, AB is parallel to CD and AB = CD. Diagonal BD is drawn, so triangles ABD and CDB overlap along BD. AB = '+M(eAB)+' and CD = '+M(eCD)+'. Angle ABD measures '+M('('+eY+')')+' degrees and angle CDB measures '+n+' degrees. Angle ADB measures '+M('('+eZ+')')+' degrees and angle CBD measures '+adb+' degrees. Triangles ABD and CDB are congruent. Answer every part.',
  parts:[
   {label:'a',prompt:'Find x. (Hint: AB = CD is given.)',answer:M('x='+x),check:{type:'solve',eq:eAB+'='+eCD,v:'x'}},
   {label:'b',prompt:'Angles ABD and CDB are alternate interior angles. Find y.',answer:M('y='+y),check:{type:'solve',eq:eY+'='+n,v:'y'}},
   {label:'c',prompt:'Angle ADB and angle CBD are corresponding parts of the congruent triangles. Find z.',answer:M('z='+z),check:{type:'solve',eq:eZ+'='+adb,v:'z'}},
   {label:'d',prompt:'Find the measure of angle A in triangle ABD. Then state the measure of angle C and why.',answer:M('w='+angA),check:{type:'solve',eq:'w+'+n+'+'+adb+'=180',v:'w'}}
  ],
  steps:[step('Corresponding sides of congruent triangles are equal, so '+M(eAB+'='+eCD)+'.',M('x='+x)),step('Alternate interior angles (parallel lines AB and CD, transversal BD) are congruent, so '+M(eY+'='+n)+'.',M('y='+y)),step('CPCTC: angle ADB is congruent to angle CBD, so '+M(eZ+'='+adb)+'.',M('z='+z)),step('The angles of triangle ABD add to 180 (angle C is congruent to angle A by CPCTC), so '+M('w+'+n+'+'+adb+'=180')+'.',M('w='+angA))],
  space:[3,3.6,4.2]};
}
/* 5: kite with a shared diagonal (SSS), two-sided equation, then an angle chase */
function investigationKite(ctx){
 var r=ctx.rng,c=ctx.c,x,a1,a2,b1,b2,tries=0,ab;
 do{x=r.int(4,c>=6?16:12);a2=r.int(1,4);a1=a2+r.int(1,4);b2=r.int(2,14);ab=a2*x+b2;b1=ab-a1*x;tries++;}while(ab<8&&tries<200);
 var m=r.int(3,5),y,n,k,p=r.int(3,5),z,q2,m2;
 tries=0;
 do{y=r.int(8,c>=6?24:18);k=r.int(2,12);n=m*y-k;z=r.int(8,c>=6?24:18);q2=r.int(3,14);m2=p*z+q2;tries++;}while((n<40||n>75||m2<40||m2>75||n+m2>135)&&tries<500);
 var rad=Math.PI/180,sb=Math.sin(m2*rad)/Math.sin((n+m2)*rad),Bx=-sb*Math.sin(n*rad),By=1-sb*Math.cos(n*rad);
 var Pp={A:[0,1],C:[0,0],B:[Bx,By],D:[-Bx,By]},angB=180-n-m2;
 var eAB=lin(a1,b1,'x'),eAD=lin(a2,b2,'x'),eY=lin(m,-k,'y'),eZ=lin(p,q2,'z');
 var fig={kind:'geo-cong',pts:Pp,segs:[['A','B'],['B','C'],['C','D'],['D','A'],['A','C']],tris:null,
  sides:[{s:[['A','B'],['A','D']],n:1},{s:[['B','C'],['D','C']],n:2}],angles:[],right:[],
  lab:{AB:eAB,AD:eAD},angLab:[{p:'B',v:'A',q:'C',text:'('+eY+')°'},{p:'D',v:'A',q:'C',text:n+'°'},{p:'B',v:'C',q:'A',text:'('+eZ+')°'}],note:'Not drawn to scale.'};
 return {variant:'geo-congruence-investigation-kite-'+c,fig:fig,
  prompt:'Open Response: In kite ABCD, AB = AD and BC = DC. Diagonal AC is drawn, so triangles ABC and ADC share side AC and are congruent by SSS. AB = '+M(eAB)+' and AD = '+M(eAD)+'. Angle BAC measures '+M('('+eY+')')+' degrees and angle DAC measures '+n+' degrees. Angle BCA measures '+M('('+eZ+')')+' degrees and angle DCA measures '+m2+' degrees. Answer every part.',
  parts:[
   {label:'a',prompt:'Use AB and AD to find x.',answer:M('x='+x),check:{type:'solve',eq:eAB+'='+eAD,v:'x'}},
   {label:'b',prompt:'Angle BAC and angle DAC are corresponding parts. Find y.',answer:M('y='+y),check:{type:'solve',eq:eY+'='+n,v:'y'}},
   {label:'c',prompt:'Angle BCA and angle DCA are corresponding parts. Find z.',answer:M('z='+z),check:{type:'solve',eq:eZ+'='+m2,v:'z'}},
   {label:'d',prompt:'Find the measure of angle ABC in triangle ABC. Then state the measure of angle ADC and why.',answer:M('w='+angB),check:{type:'solve',eq:'w+'+n+'+'+m2+'=180',v:'w'}}
  ],
  steps:[step('Corresponding sides of congruent triangles are equal, so '+M(eAB+'='+eAD)+'.',M('x='+x)),step('CPCTC: angle BAC is congruent to angle DAC, so '+M(eY+'='+n)+'.',M('y='+y)),step('CPCTC: angle BCA is congruent to angle DCA, so '+M(eZ+'='+m2)+'.',M('z='+z)),step('The angles of triangle ABC add to 180 (angle ADC is congruent to angle ABC by CPCTC), so '+M('w+'+n+'+'+m2+'=180')+'.',M('w='+angB))],
  space:[3,3.6,4.2]};
}
/* 6: right triangles congruent by HL, two-sided hypotenuse equation, then acute angles */
function investigationHL(ctx){
 var r=ctx.rng,c=ctx.c,x,a1,a2,b1,b2,h,tries=0;
 do{x=r.int(4,c>=6?16:12);a2=r.int(1,4);a1=a2+r.int(1,4);b2=r.int(2,14);h=a2*x+b2;b1=h-a1*x;tries++;}while(h<12&&tries<200);
 var m=r.int(2,5),y=r.int(4,c>=6?18:12),cc=r.int(-8,9),leg=m*y+cc;
 while(leg<6||leg>=h-1){m=r.int(2,5);y=r.int(2,18);cc=r.int(-8,9);leg=m*y+cc;}
 var p=r.int(2,4),z=r.int(6,c>=6?20:14),q2=r.int(-6,12),angC=p*z+q2;
 while(angC<20||angC>70){z=r.int(6,20);q2=r.int(-6,12);angC=p*z+q2;}
 var angA=90-angC;
 var eAC=lin(a1,b1,'x'),eDF=lin(a2,b2,'x'),eAB=lin(m,cc,'y'),eC=lin(p,q2,'z');
 var f=NS.geoFigures&&NS.geoFigures.cong?NS.geoFigures.cong.pair('hl',false):{kind:'geo-triangle-pair',criterion:'hl'};
 if(f.kind==='geo-cong'){f.lab={AC:eAC,DF:eDF,AB:eAB,DE:String(leg)};f.note='Not drawn to scale.';}
 return {variant:'geo-congruence-investigation-hl-'+c,fig:f,
  prompt:'Open Response: Triangles ABC and DEF are right triangles with right angles (90 degrees) at B and E. Their hypotenuses are AC = '+M(eAC)+' and DF = '+M(eDF)+', and leg AB = '+M(eAB)+' while leg DE = '+leg+'. The triangles are congruent with A corresponding to D, B to E, and C to F. Angle C measures '+M('('+eC+')')+' degrees and angle F measures '+angC+' degrees. Answer every part.',
  parts:[
   {label:'a',prompt:'The hypotenuses are equal. Find x.',answer:M('x='+x),check:{type:'solve',eq:eAC+'='+eDF,v:'x'}},
   {label:'b',prompt:'Legs AB and DE are corresponding parts. Find y.',answer:M('y='+y),check:{type:'solve',eq:eAB+'='+leg,v:'y'}},
   {label:'c',prompt:'Angles C and F are corresponding parts. Find z.',answer:M('z='+z),check:{type:'solve',eq:eC+'='+angC,v:'z'}},
   {label:'d',prompt:'Find the measure of angle A. Explain why angles A and C are complementary.',answer:M('w='+angA),check:{type:'solve',eq:'w+'+angC+'+90=180',v:'w'}}
  ],
  steps:[step('The hypotenuses are corresponding sides, so '+M(eAC+'='+eDF)+'.',M('x='+x)),step('CPCTC: AB = DE, so '+M(eAB+'='+leg)+'.',M('y='+y)),step('CPCTC: angle C is congruent to angle F, so '+M(eC+'='+angC)+'.',M('z='+z)),step('The angles of right triangle ABC add to 180, so '+M('w+'+angC+'+90=180')+'.',M('w='+angA))],
  space:[3,3.6,4.2]};
}
/* Printables with small boxes ask for a compact prompt: the diagram carries the marks, so the text only needs the givens. */
function C(g){return function(ctx){var p=g(ctx);if(ctx.compact&&p.compactPrompt)p.prompt=p.compactPrompt;delete p.compactPrompt;return p;};}
NS.registerSkillSet({id:'geometry-triangles-congruence',course:'geometry',courseName:'Geometry',unit:'triangles-congruence',unitName:'Triangle Congruence',title:'Triangle Congruence Foundations',
 tags:{CPCTC:'Corresponding parts of congruent triangles',THIRD:'Third angle theorem',PERIMETER:'Congruent triangle perimeters',CRITERIA:'SSS, SAS, ASA, AAS, and HL',PROOFS:'Two-column and flow proof reasoning',CHAIN:'Multi-step congruence investigations'},
 reference:'<div class="mm-refgrid"><section><h4>Correspondence</h4><p>In ABC ≅ DEF, A ↔ D, B ↔ E, and C ↔ F.</p></section><section><h4>CPCTC</h4><p>Corresponding parts of congruent triangles are congruent.</p></section></div>',
 gaps:['Proofs other than the shared-side and vertical-angle formats, and congruence by rigid motions, are not generated.'],
 skills:[
 {id:'congruent-corresponding-sides',tag:'CPCTC',name:'Corresponding side lengths',best:[0,1],generate:C(ctx=>corresponding(ctx,'side'))},
 {id:'congruent-corresponding-angles',tag:'CPCTC',name:'Corresponding angle measures',best:[0,1],generate:C(ctx=>corresponding(ctx,'angle'))},
 {id:'congruent-third-angle',tag:'THIRD',name:'Third angle theorem',best:[0,1],generate:C(thirdAngle)},
 {id:'congruent-perimeters',tag:'PERIMETER',name:'Perimeters of congruent triangles',best:[0,1],generate:C(perimeter)},
 {id:'congruence-sss',tag:'CRITERIA',name:'SSS congruence and CPCTC',best:[0,1],generate:C(ctx=>criterion(ctx,'sss'))},
 {id:'congruence-sas',tag:'CRITERIA',name:'SAS congruence and CPCTC',best:[0,1],generate:C(ctx=>criterion(ctx,'sas'))},
 {id:'congruence-asa',tag:'CRITERIA',name:'ASA congruence and CPCTC',best:[0,1],generate:C(ctx=>criterion(ctx,'asa'))},
 {id:'congruence-aas',tag:'CRITERIA',name:'AAS congruence and CPCTC',best:[0,1],generate:C(ctx=>criterion(ctx,'aas'))},
 {id:'congruence-hl',tag:'CRITERIA',name:'HL congruence and CPCTC',best:[0,1],generate:C(ctx=>criterion(ctx,'hl'))},
 {id:'congruence-identify',tag:'CRITERIA',name:'Identify valid and invalid triangle congruence criteria from markings',best:[0,1,2],generate:C(identify)},
 {id:'congruence-investigation-algebra',tag:'CHAIN',name:'Four-part investigation: algebra on congruent triangles',best:[2],generate:investigationAlgebra},
 {id:'congruence-investigation-isosceles',tag:'CHAIN',name:'Four-part investigation: isosceles triangle and its median',best:[2],generate:investigationIsosceles},
 {id:'congruence-investigation-coordinate',tag:'CHAIN',name:'Four-part investigation: congruence on the coordinate plane',best:[2],generate:investigationCoordinate},
 {id:'congruence-investigation-overlap',tag:'CHAIN',name:'Four-part investigation: overlapping triangles and parallel lines',best:[2],generate:investigationOverlap},
 {id:'congruence-investigation-kite',tag:'CHAIN',name:'Four-part investigation: kite with a shared diagonal',best:[2],generate:investigationKite},
 {id:'congruence-investigation-hl',tag:'CHAIN',name:'Four-part investigation: right triangles congruent by HL',best:[2],generate:investigationHL},
 {id:'congruence-structured-proof',tag:'PROOFS',name:'Complete a two-column or flow proof',best:[0,1,2],generate:structuredProof}
 ]});
})(typeof window!=='undefined'?window:globalThis);
