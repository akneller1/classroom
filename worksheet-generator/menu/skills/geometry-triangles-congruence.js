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
 return {compactPrompt:'Triangle ABC ≅ triangle DEF. m∠A = '+other+'° and m∠C = '+third+'°. Use '+M(eq)+' to find x, the measure of ∠B.',variant:'geo-congruence-third-angle-'+c,fig:{kind:'geo-cong-pair',angles:{A:other+'°',B:'x°',C:third+'°'},arcs:{A:1,D:1,B:2,E:2},description:'Triangles ABC and DEF with matching marked angles at A, D and B, E'},prompt:'Triangles ABC and DEF have angle A congruent to angle D and angle B congruent to angle E. In triangle ABC, angle A is '+other+'° and angle C is '+third+'°. Find angle B, called x, and explain why angle F must equal angle C. Use '+M(eq)+' to find x.',flashcardPrompt:'Triangles ABC and DEF have angle A congruent to angle D and angle B congruent to angle E. In triangle ABC, angle A is '+other+'° and angle C is '+third+'°. Find angle B, called x, and explain why angle F must equal angle C.',
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
  flashcardPrompt:'Use the diagram to state which congruence postulate proves triangle ABC congruent to triangle DEF. Then solve for x.',
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
/* ---------- Two-column congruence proofs (statements and reasons) ----------
   Each diagram is built by an exact construction (reflection, half-turn, parallelogram, isosceles triangle,
   shared angle, translation), so every Given is true of the drawn coordinates and the two triangles really
   are congruent. The proof table is printed under the diagram (fig.proof); each blank is one part.
   The verifier (check 'geo-proof-blank' / 'geo-proof-write') re-reads the printed Given/Prove text, the
   coordinates and every row, and decides independently whether the completed proof is valid. */
var PR_REASON={given:'Given',reflexive:'Reflexive Property of Congruence',vertical:'Vertical angles are congruent',
 altint:'Alternate interior angles are congruent',corresp:'Corresponding angles are congruent',midpoint:'Definition of midpoint',
 bisector:'Definition of angle bisector',perp:'Definition of perpendicular lines',rightcong:'All right angles are congruent',
 segadd:'Segment Addition Postulate',SSS:'SSS',SAS:'SAS',ASA:'ASA',AAS:'AAS',HL:'HL',cpctc:'CPCTC'};
function prR(r,a,b){return a+(b-a)*r.next();}
function prD(p,q){return Math.hypot(p[0]-q[0],p[1]-q[1]);}
function prAng(P,V,Q){var u=[P[0]-V[0],P[1]-V[1]],w=[Q[0]-V[0],Q[1]-V[1]];return Math.acos(Math.max(-1,Math.min(1,(u[0]*w[0]+u[1]*w[1])/(Math.hypot(u[0],u[1])*Math.hypot(w[0],w[1])))))*180/Math.PI;}
function prMin(P,a,b,c){return Math.min(prAng(P[b],P[a],P[c]),prAng(P[a],P[b],P[c]),prAng(P[a],P[c],P[b]));}
var S_=function(a,b){return {t:'seg',a:a.split(''),b:b.split('')};},A_=function(a,b){return {t:'ang',a:a.split(''),b:b.split('')};};
/* templates: roles -> coordinates, drawn segments, givens, support facts [statement, reason], triangles, CPCTC options */
var PR_T={
 kite:function(r,v){var P;for(var i=0;i<200;i++){var c=prR(r,6,8),bx=prR(r,1.8,c-1.6),by=prR(r,2.2,3.6);P={A:[0,0],C:[c,0],B:[bx,by],D:[bx,-by]};
   if(Math.abs(prD(P.A,P.B)-prD(P.C,P.B))>0.9&&prAng(P.A,P.B,P.C)>40&&prAng(P.A,P.B,P.C)<140&&prMin(P,'A','B','C')>24)break;}
  var sAB=S_('AB','AD'),sCB=S_('CB','CD'),refl=S_('AC','AC'),bisA=A_('BAC','DAC'),bisC=A_('BCA','DCA'),angB=A_('ABC','ADC'),gA={t:'bis',ray:['A','C'],ang:['B','A','D']},gC={t:'bis',ray:['C','A'],ang:['B','C','D']};
  var T={points:P,segs:[['A','B'],['B','C'],['C','D'],['D','A'],['A','C']],tri:[['A','B','C'],['A','D','C']]};
  if(v==='SSS'){T.givens=[sAB,sCB];T.facts=[[sAB,'given'],[sCB,'given'],[refl,'reflexive']];}
  if(v==='SAS'){T.givens=[sAB,gA];T.facts=[[sAB,'given'],[bisA,'bisector'],[refl,'reflexive']];}
  if(v==='ASA'){T.givens=[gA,gC];T.facts=[[bisA,'bisector'],[refl,'reflexive'],[bisC,'bisector']];}
  if(v==='AAS'){T.givens=[angB,gA];T.facts=[[angB,'given'],[bisA,'bisector'],[refl,'reflexive']];}
  T.cpctc=[S_('BC','DC'),A_('ABC','ADC'),A_('BCA','DCA'),S_('AB','AD')];return T;},
 bowtie:function(r,v){var P;for(var i=0;i<200;i++){var a=prR(r,3,4.6),b=prR(r,2.4,4.2),t1=prR(r,2.3,2.9),t2=t1+prR(r,0.75,1.5),A=[a*Math.cos(t1),a*Math.sin(t1)],B=[b*Math.cos(t2),b*Math.sin(t2)];
   P={M:[0,0],A:A,B:B,D:[-A[0],-A[1]],E:[-B[0],-B[1]]};var g=prAng(P.A,P.M,P.B);
   if(g>45&&g<120&&Math.abs(a-b)>0.6&&prD(A,B)>2.2&&prAng(P.M,P.A,P.B)>30&&prAng(P.M,P.B,P.A)>30)break;}
  var vert=A_('AMB','DME'),mA=S_('AM','DM'),mB=S_('BM','EM'),aiA=A_('BAM','EDM'),aiB=A_('ABM','DEM'),sAB=S_('AB','DE'),par={t:'par',a:['A','B'],b:['D','E']};
  var T={points:P,segs:[['A','D'],['B','E'],['A','B'],['D','E']],tri:[['A','M','B'],['D','M','E']]};
  var midA={t:'mid',m:'M',a:'A',b:'D'},midB={t:'mid',m:'M',a:'B',b:'E'};
  if(v==='SAS'){T.givens=[midA,midB];T.facts=[[mA,'midpoint'],[vert,'vertical'],[mB,'midpoint']];}
  if(v==='ASA'){T.givens=[par,midA];T.facts=[[aiA,'altint'],[mA,'midpoint'],[vert,'vertical']];}
  if(v==='AAS'){T.givens=[par,sAB];T.facts=[[aiB,'altint'],[vert,'vertical'],[sAB,'given']];}
  T.cpctc=[sAB,aiA,aiB,mB,mA];return T;},
 para:function(r,v){var P;for(var i=0;i<200;i++){var w=prR(r,5.5,7.5),s=prR(r,1.2,2.6)*(r.next()<0.5?1:-1),h=prR(r,3.2,4.4);P={A:[0,0],B:[w,0],C:[w+s,h],D:[s,h]};
   if(Math.abs(prD(P.A,P.D)-w)>1.2&&prMin(P,'A','B','C')>24&&prMin(P,'C','D','A')>24)break;}
  var refl=S_('AC','CA'),ai1=A_('BAC','DCA'),ai2=A_('BCA','DAC'),sAB=S_('AB','CD'),sBC=S_('BC','DA'),p1={t:'par',a:['A','B'],b:['D','C']},p2={t:'par',a:['A','D'],b:['B','C']};
  var T={points:P,segs:[['A','B'],['B','C'],['C','D'],['D','A'],['A','C']],tri:[['A','B','C'],['C','D','A']]};
  if(v==='SAS'){T.givens=[p1,sAB];T.facts=[[sAB,'given'],[ai1,'altint'],[refl,'reflexive']];}
  if(v==='ASA'){T.givens=[p1,p2];T.facts=[[ai1,'altint'],[refl,'reflexive'],[ai2,'altint']];}
  if(v==='SSS'){T.givens=[sAB,sBC];T.facts=[[sAB,'given'],[sBC,'given'],[refl,'reflexive']];}
  T.cpctc=[A_('ABC','CDA'),sBC,ai2,sAB,ai1];return T;},
 iso:function(r,v){var b=prR(r,2.4,3.6),h=prR(r,3.8,5.2),P={A:[0,h],B:[-b,0],C:[b,0],D:[0,0]};
  var refl=S_('AD','AD'),sAB=S_('AB','AC'),sBD=S_('BD','CD'),bis=A_('BAD','CAD'),rt=A_('ADB','ADC'),mid={t:'mid',m:'D',a:'B',b:'C'},perp={t:'perp',a:['A','D'],b:['B','C']};
  var T={points:P,segs:[['A','B'],['A','C'],['B','C'],['A','D']],tri:[['A','D','B'],['A','D','C']]};
  if(v==='SSS'){T.givens=[sAB,mid];T.facts=[[sAB,'given'],[sBD,'midpoint'],[refl,'reflexive']];}
  if(v==='SAS'){T.givens=[sAB,{t:'bis',ray:['A','D'],ang:['B','A','C']}];T.facts=[[sAB,'given'],[bis,'bisector'],[refl,'reflexive']];}
  if(v==='SAS2'){T.givens=[perp,mid];T.facts=[[sBD,'midpoint'],[rt,'perp'],[refl,'reflexive']];}
  if(v==='HL'){T.givens=[perp,sAB];T.facts=[[{t:'right',a:['A','D','B'],b:['A','D','C']},'perp'],[sAB,'given'],[refl,'reflexive']];}
  T.cpctc=[A_('ABD','ACD'),sBD,bis,sAB];return T;},
 shared:function(r){var P;for(var i=0;i<200;i++){var open=prR(r,48,72)*Math.PI/180,base=prR(r,-0.4,0.4),p=prR(r,6.5,8),q=p*prR(r,0.45,0.6),u1=[Math.cos(base+open/2),Math.sin(base+open/2)],u2=[Math.cos(base-open/2),Math.sin(base-open/2)];
   P={A:[0,0],B:[p*u1[0],p*u1[1]],D:[q*u1[0],q*u1[1]],C:[p*u2[0],p*u2[1]],E:[q*u2[0],q*u2[1]]};if(prD(P.B,P.C)>3)break;}
  var sAB=S_('AB','AC'),sAE=S_('AE','AD');
  return {points:P,segs:[['A','B'],['A','C'],['B','E'],['C','D']],tri:[['A','B','E'],['A','C','D']],givens:[sAB,sAE],facts:[[sAB,'given'],[A_('BAE','CAD'),'reflexive'],[sAE,'given']],
   cpctc:[S_('BE','CD'),A_('ABE','ACD'),A_('AEB','ADC')]};},
 slide:function(r,v){var P;for(var i=0;i<200;i++){var t=prR(r,1.6,2.4),c=prR(r,4.2,5.4),ex=prR(r,0.8,c-0.8),ey=prR(r,2.6,3.6);P={A:[0,0],B:[t,0],C:[c,0],D:[c+t,0],E:[ex,ey],F:[ex+t,ey]};
   if(prAng(P.E,P.A,P.C)>35&&prAng(P.E,P.C,P.A)>35)break;}
  var sAC=S_('AC','BD'),cA=A_('EAC','FBD'),cC=A_('ECA','FDB'),sAE=S_('AE','BF'),sCE=S_('CE','DF'),gAB=S_('AB','CD'),pA={t:'par',a:['A','E'],b:['B','F']},pC={t:'par',a:['C','E'],b:['D','F']};
  var T={points:P,segs:[['A','D'],['A','E'],['E','C'],['B','F'],['F','D']],tri:[['A','C','E'],['B','D','F']]};
  if(v==='SAS'){T.givens=[gAB,pA,sAE];T.facts=[[sAC,'segadd'],[cA,'corresp'],[sAE,'given']];}
  if(v==='ASA'){T.givens=[gAB,pA,pC];T.facts=[[cA,'corresp'],[sAC,'segadd'],[cC,'corresp']];}
  if(v==='SSS'){T.givens=[gAB,sAE,sCE];T.facts=[[sAE,'given'],[sCE,'given'],[sAC,'segadd']];}
  T.cpctc=[sCE,cC,A_('AEC','BFD'),sAE];return T;}
};
var PR_POOLS={easy:[['kite','SSS'],['para','SSS'],['iso','SSS'],['bowtie','SAS'],['iso','SAS'],['kite','SAS'],['iso','HL']],
 medium:[['para','ASA'],['kite','ASA'],['bowtie','ASA'],['iso','SAS2'],['para','SAS'],['slide','SSS'],['kite','AAS']],
 hard:[['bowtie','AAS'],['shared','SAS'],['slide','SAS'],['slide','ASA']]};
function prPool(c){var E=PR_POOLS.easy,Me=PR_POOLS.medium,H=PR_POOLS.hard;return c<=2?E:c===3?E.concat(Me):c===4?Me.concat(E.slice(0,3)):c===5?Me.concat(H):H.concat(Me.slice(0,4));}
var PR_LET='ABCDEFGHJKLMNPQRSTUVWXYZ'.split('');
function prShow(st){var g=function(p){return '∠'+p.join('');};
 if(st.t==='seg')return st.a.join('')+' ≅ '+st.b.join('');if(st.t==='ang')return g(st.a)+' ≅ '+g(st.b);
 if(st.t==='tri')return '△'+st.a.join('')+' ≅ △'+st.b.join('');if(st.t==='right')return g(st.a)+' and '+g(st.b)+' are right angles';
 if(st.t==='par')return st.a.join('')+' ∥ '+st.b.join('');if(st.t==='perp')return st.a.join('')+' ⊥ '+st.b.join('');
 if(st.t==='mid')return st.m+' is the midpoint of '+st.a+st.b;if(st.t==='bis')return st.ray.join('')+' bisects ∠'+st.ang.join('');return '';}
function prMap(st,L){var o=JSON.parse(JSON.stringify(st)),m=function(x){return Array.isArray(x)?x.map(m):typeof x==='string'&&x.length===1&&L[x]?L[x]:x;};
 Object.keys(o).forEach(function(k){if(k!=='t')o[k]=m(o[k]);});return o;}
/* build one proof: {pts, segs, givens, prove, rows:[{st,rk}], tri, cp} */
function prBuild(r,c,opts){
 var pool=opts.pool||prPool(c),choice=r.pick(pool),T=PR_T[choice[0]](r,choice[1]),post=choice[1]==='SAS2'?'SAS':choice[1];
 var roles=Object.keys(T.points),letters=c<=2&&r.next()<0.6?null:r.shuffle(PR_LET).slice(0,roles.length),L={};
 roles.forEach(function(k,i){L[k]=letters?letters[i]:k;});
 var th=prR(r,-Math.PI,Math.PI),flip=r.next()<0.5,pts={};
 if(choice[0]==='iso'||choice[0]==='slide')th=prR(r,-0.35,0.35)+(r.next()<0.25?Math.PI:0);   // keep the base roughly level
 roles.forEach(function(k){var p=T.points[k];if(flip)p=[-p[0],p[1]];pts[L[k]]=[p[0]*Math.cos(th)-p[1]*Math.sin(th),p[0]*Math.sin(th)+p[1]*Math.cos(th)];});
 var rows=T.facts.map(function(f){return {st:prMap(f[0],L),rk:f[1]};}),tri={t:'tri',a:T.tri[0].map(function(x){return L[x];}),b:T.tri[1].map(function(x){return L[x];})};
 rows.push({st:tri,rk:post});
 var prove=tri,cp=null;
 if(opts.cpctc){
  var used=T.facts.map(function(f){return JSON.stringify(f[0]);}).concat(T.givens.map(function(g){return JSON.stringify(g);}));
  var opt=T.cpctc.filter(function(s){return used.indexOf(JSON.stringify(s))<0&&used.indexOf(JSON.stringify({t:s.t,a:s.b,b:s.a}))<0;});
  cp=prMap(r.pick(opt),L);if(r.next()<0.5)cp={t:cp.t,a:cp.b,b:cp.a};rows.push({st:cp,rk:'cpctc'});prove=cp;}
 return {template:choice[0],variant:choice[1],post:post,pts:pts,segs:T.segs.map(function(s){return [L[s[0]],L[s[1]]];}),
  givens:T.givens.map(function(g){return prMap(g,L);}),prove:prove,rows:rows,tri:tri,cpctc:!!cp};
}
/* marks for the givens: ticks, arcs, parallel arrows, right-angle marks */
function prFig(B){
 var f={kind:'geo-cong',pts:B.pts,segs:B.segs,tris:[B.tri.a.slice(),B.tri.b.slice()],sides:[],angles:[],right:[],par:[],w:300,h:175};
 var ns=0,na=0,np=0;
 B.givens.forEach(function(g){
  if(g.t==='seg')f.sides.push({s:[g.a.slice(),g.b.slice()],n:++ns});
  else if(g.t==='ang')f.angles.push({a:[g.a.slice(),g.b.slice()],n:++na});
  else if(g.t==='mid')f.sides.push({s:[[g.a,g.m],[g.m,g.b]],n:++ns});
  else if(g.t==='bis')f.angles.push({a:[[g.ang[0],g.ang[1],g.ray[1]],[g.ray[1],g.ang[1],g.ang[2]]],n:++na});
  else if(g.t==='par')f.par.push({s:[g.a.slice(),g.b.slice()],n:++np});
  else if(g.t==='perp'){var X=g.a[1];f.right.push([g.a[0],X,g.b[1]]);}   // in the isosceles template the foot is the second letter of the first line
 });
 return f;
}
var PR_MODE={reasons:'Complete the two-column proof by writing each missing reason.',statements:'Complete the two-column proof by writing each missing statement.',
 mixed:'Complete the two-column proof by writing each missing statement and reason.',one:'Complete the two-column proof by writing the missing reason.',
 write:'Write a two-column proof. Give a statement and a reason in each row.'};
/* blanks: list of [row, 's'|'r'] */
function prProblem(ctx,B,mode,blanks,kind){
 var c=ctx.c,fig=prFig(B),LAB='abcdefghijklmnop',rows=B.rows.map(function(x){return {s:prShow(x.st),r:PR_REASON[x.rk]};});
 var given='Given: '+B.givens.map(prShow).join('; ')+'. Prove: '+prShow(B.prove)+'.';
 var parts=[],table=rows.map(function(x){return {s:x.s,r:x.r};});
 if(mode==='write'){
  table=rows.map(function(){return {s:'',r:''};});
  parts=[{prompt:'Write the complete proof.',answer:rows.map(function(x,i){return (i+1)+'. '+x.s+' — '+x.r;}).join('; '),check:{type:'geo-proof-write'}}];
  fig.proof={rows:table,write:true};
 } else {
  blanks.sort(function(p,q){return p[0]-q[0]||(p[1]==='s'?-1:1);});
  blanks.forEach(function(bk,i){var lab=LAB[i];table[bk[0]][bk[1]]='';table[bk[0]][bk[1]+'b']=lab;
   parts.push({label:lab,prompt:(bk[1]==='s'?'Statement for step ':'Reason for step ')+(bk[0]+1),answer:rows[bk[0]][bk[1]],check:{type:'geo-proof-blank',row:bk[0],field:bk[1]}});});
  fig.proof={rows:table};
 }
 var steps=rows.map(function(x){return step(x.s+' — '+x.r);});
 steps.push(step(B.cpctc?'The triangles are proved congruent first; only then does CPCTC give the Prove statement.':'Three pairs of corresponding parts ('+B.post+') prove the triangles congruent.'));
 return {variant:'geo-proof-table-'+kind+'-'+B.template+'-'+B.variant.toLowerCase()+(B.cpctc?'-cpctc':'')+'-'+c,
  prompt:given+' '+PR_MODE[mode],fig:fig,parts:parts,steps:steps,space:[0.2,0.3,0.4]};
}
function prPickBlanks(r,B,mode,n){
 var nr=B.rows.length,cells=[];
 for(var i=0;i<nr;i++){if(mode!=='statements')cells.push([i,'r']);if(mode!=='reasons')cells.push([i,'s']);}
 if(mode==='mixed'){   // never blank both cells of one row; at least one of each kind
  var out=[],rowsUsed={},sh=r.shuffle(cells);
  var firstS=sh.filter(function(x){return x[1]==='s';})[0],firstR=sh.filter(function(x){return x[1]==='r'&&x[0]!==firstS[0];})[0];
  [firstS,firstR].forEach(function(x){out.push(x);rowsUsed[x[0]]=1;});
  sh.forEach(function(x){if(out.length<n&&!rowsUsed[x[0]]){out.push(x);rowsUsed[x[0]]=1;}});
  return out;}
 return r.shuffle(cells).slice(0,Math.min(n,cells.length));
}
function proofSkill(mode,cp){
 return function(ctx){
  var r=ctx.rng,c=ctx.c,cpctc=cp==='always'||(cp==='hi'&&c>=5&&r.next()<0.5);
  var B=prBuild(r,c,{cpctc:cpctc}),nr=B.rows.length,n,kind;
  if(mode==='one'){n=1;kind='one';}
  else if(mode==='write'||(cp==='always'&&c>=6)){return prProblem(ctx,B,'write',[],cp==='always'?'cpctc-write':'write');}
  else if(mode==='reasons'){n=c<=2?2:c<=4?3:nr;kind='reasons';}
  else if(mode==='statements'){n=c<=2?2:c<=4?3:Math.min(nr,4);kind='statements';}
  else {n=c<=2?2:c<=4?3:c<=5?4:nr;kind=cp==='always'?'cpctc':'mixed';}
  var bl=prPickBlanks(r,B,mode==='one'?'reasons':mode==='cpctc'?'mixed':mode,n);
  if(cp==='always'&&!bl.some(function(x){return x[0]===nr-1;}))bl[bl.length-1]=[nr-1,r.next()<0.5?'s':'r'];   // the CPCTC step is always part of the work
  var seenRow={};bl=bl.filter(function(x){var k=x.join();if(seenRow[k])return false;seenRow[k]=1;return true;});
  return prProblem(ctx,B,mode==='one'?'one':mode==='cpctc'?'mixed':mode,bl,kind);
 };
}

NS.registerSkillSet({id:'geometry-triangles-congruence',course:'geometry',courseName:'Geometry',unit:'triangles-congruence',unitName:'Triangle Congruence',title:'Triangle Congruence Foundations',
 tags:{RIGID:'Congruence and rigid motions',CPCTC:'Corresponding parts of congruent triangles',THIRD:'Third angle theorem',PERIMETER:'Congruent triangle perimeters',CRITERIA:'SSS, SAS, ASA, AAS, and HL',PROOFS:'Two-column and flow proof reasoning',CHAIN:'Multi-step congruence investigations'},
 reference:'<div class="mm-refgrid"><section><h4>Correspondence</h4><p>In ABC ≅ DEF, A ↔ D, B ↔ E, and C ↔ F.</p></section><section><h4>CPCTC</h4><p>Corresponding parts of congruent triangles are congruent.</p></section></div>',
 gaps:['Flow-chart and paragraph proofs are generated only in the shared-side and vertical-angle formats. Congruence by rigid motions is asked from a described sequence of transformations, not from a drawn figure.'],
 skills:[
  {id:'congruence-rigid-motions',tag:'RIGID',name:'Congruence by rigid motions (described transformation sequences)',best:[0,1,2],generate:K.rigidSequence},
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
 {id:'congruence-structured-proof',tag:'PROOFS',name:'Complete a two-column or flow proof',best:[0,1,2],generate:structuredProof},
 {id:'congruence-proof-missing-reason',tag:'PROOFS',name:'Proof: supply the missing reason',best:[0,1],generate:proofSkill('one','hi')},
 {id:'congruence-proof-reasons',tag:'PROOFS',name:'Proof: fill in the missing reasons',best:[0,1],generate:proofSkill('reasons','hi')},
 {id:'congruence-proof-statements',tag:'PROOFS',name:'Proof: fill in the missing statements',best:[0,1],generate:proofSkill('statements','hi')},
 {id:'congruence-proof-mixed',tag:'PROOFS',name:'Proof: missing statements and reasons',best:[1,2],generate:proofSkill('mixed','hi')},
 {id:'congruence-proof-write',tag:'PROOFS',name:'Write a triangle congruence proof',best:[2],generate:proofSkill('write','no')},
 {id:'congruence-proof-cpctc',tag:'PROOFS',name:'CPCTC proofs (prove parts congruent)',best:[1,2],generate:proofSkill('cpctc','always')}
 ]});
})(typeof window!=='undefined'?window:globalThis);
