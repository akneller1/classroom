/* Verified text-first Geometry Unit 3 starter bank. No diagram is implied. */
(function(G){'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function corresponding(ctx,kind){
 var r=ctx.rng,c=ctx.c,x=r.int(3,c>=5?30:18),a=c>=5?r.int(2,4):1,b=r.int(1,12),value=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+value;
 var feature=kind==='side'?'corresponding sides':'corresponding angles';
 var unit=kind==='side'?' units':' degrees';
 return {variant:'geo-congruence-'+kind+'-'+c,
 prompt:'Triangles ABC and DEF are congruent, with A corresponding to D, B to E, and C to F. '+(kind==='side'?'AB and DE':'angle B and angle E')+' are '+feature+'. Their measures are '+M((a===1?'x':a+'x')+'+'+b)+' and '+value+unit+'. Find x. Set up an equation and show your reasoning.',
 parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
 steps:[step('Corresponding parts of congruent triangles are congruent.',M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};
}
function thirdAngle(ctx){
 var r=ctx.rng,c=ctx.c,x=r.int(25,85),other=r.int(25,Math.min(85,150-x)),third=180-x-other;
 var eq='x+'+other+'+'+third+'=180';
 return {variant:'geo-congruence-third-angle-'+c,prompt:'Triangles ABC and DEF have angle A congruent to angle D and angle B congruent to angle E. In triangle ABC, angle A is '+other+'° and angle C is '+third+'°. Find angle B, called x, and explain why angle F must equal angle C. Use '+M(eq)+' to find x.',
 parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
 steps:[step('Use the triangle angle sum.',M(eq)),step('The third angles match because both triangles sum to 180°.',M('x='+x))],space:[1.2,1.5,1.8]};
}
function perimeter(ctx){
 var r=ctx.rng,c=ctx.c,a=r.int(5,16),b=r.int(5,16),x=r.int(Math.abs(a-b)+1,a+b-1),p=x+a+b,eq='x+'+a+'+'+b+'='+p;
 return {variant:'geo-congruence-perimeter-'+c,prompt:'Triangle ABC is congruent to triangle DEF. The side lengths of ABC are x, '+a+', and '+b+' units. The perimeter of DEF is '+p+' units. Find x. Set up an equation and show your reasoning.',
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
 return {variant:'geo-criterion-'+kind+'-'+c,fig:{kind:'geo-triangle-pair',criterion:kind},
  prompt:'Triangles ABC and DEF have the correspondence A to D, B to E, and C to F. '+fact+' '+target+' Find x. State why the triangles are congruent, then set up and solve an equation for x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step(why,M(eq)),step('Solve for the unknown value.',M('x='+x))],
  space:[1.2,1.5,1.8]};
}

function identify(ctx){
 var r=ctx.rng,c=ctx.c,kinds=['sss','sas','asa','aas','hl','ssa','aaa'];
 var kind=kinds[r.int(0,kinds.length-1)],setting=r.int(0,5),answer=(kind==='ssa'||kind==='aaa')?'NOT SUFFICIENT':kind.toUpperCase();
 return {variant:'geo-identify-criterion-'+kind+'-'+c,
  fig:{kind:'geo-triangle-pair',criterion:kind},
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
  fig:{kind:'geo-proof',case:shared?'shared':'vertical'},
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
NS.registerSkillSet({id:'geometry-triangles-congruence',course:'geometry',courseName:'Geometry',unit:'triangles-congruence',unitName:'Triangle Congruence',title:'Triangle Congruence Foundations',
 tags:{CPCTC:'Corresponding parts of congruent triangles',THIRD:'Third angle theorem',PERIMETER:'Congruent triangle perimeters',CRITERIA:'SSS, SAS, ASA, AAS, and HL',PROOFS:'Two-column and flow proof reasoning'},
 reference:'<div class="mm-refgrid"><section><h4>Correspondence</h4><p>In ABC ≅ DEF, A ↔ D, B ↔ E, and C ↔ F.</p></section><section><h4>CPCTC</h4><p>Corresponding parts of congruent triangles are congruent.</p></section></div>',
 gaps:['More advanced proof structures and fully labeled proof diagrams remain to be developed.'],
 skills:[
 {id:'congruent-corresponding-sides',tag:'CPCTC',name:'Corresponding side lengths',best:[0,1,2],generate:ctx=>corresponding(ctx,'side')},
 {id:'congruent-corresponding-angles',tag:'CPCTC',name:'Corresponding angle measures',best:[0,1,2],generate:ctx=>corresponding(ctx,'angle')},
 {id:'congruent-third-angle',tag:'THIRD',name:'Third angle theorem',best:[0,1,2],generate:thirdAngle},
 {id:'congruent-perimeters',tag:'PERIMETER',name:'Perimeters of congruent triangles',best:[0,1,2],generate:perimeter},
 {id:'congruence-sss',tag:'CRITERIA',name:'SSS congruence and CPCTC',best:[0,1,2],generate:ctx=>criterion(ctx,'sss')},
 {id:'congruence-sas',tag:'CRITERIA',name:'SAS congruence and CPCTC',best:[0,1,2],generate:ctx=>criterion(ctx,'sas')},
 {id:'congruence-asa',tag:'CRITERIA',name:'ASA congruence and CPCTC',best:[0,1,2],generate:ctx=>criterion(ctx,'asa')},
 {id:'congruence-aas',tag:'CRITERIA',name:'AAS congruence and CPCTC',best:[0,1,2],generate:ctx=>criterion(ctx,'aas')},
 {id:'congruence-hl',tag:'CRITERIA',name:'HL congruence and CPCTC',best:[0,1,2],generate:ctx=>criterion(ctx,'hl')},
 {id:'congruence-identify',tag:'CRITERIA',name:'Identify valid and invalid triangle congruence criteria from markings',best:[0,1,2],generate:identify},
 {id:'congruence-structured-proof',tag:'PROOFS',name:'Complete a two-column or flow proof',best:[0,1,2],generate:structuredProof}
 ]});
})(typeof window!=='undefined'?window:globalThis);
