/* Geometry Unit 5: independently verifiable starter questions on similarity. */
(function(G){'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(variant,prompt,eq,x,rule,df){var kind=/^geo-sim-(aa|sas|sss|side|angle)-/.exec(variant);var fig=df?df:kind?{kind:'geo-similar-pair',case:kind[1]==='side'||kind[1]==='angle'?'sides':kind[1]}:null;return {variant:variant,fig:fig,prompt:prompt,parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(rule,M(eq)),step('Solve for x.',M('x='+x))],space:[1.2,1.5,1.8]};}
function missingSide(ctx){var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?6:4),a=r.int(3,12),b=r.int(3,12),x;while(b>a*1.6||a>b*1.6){a=r.int(3,12);b=r.int(3,12);}x=k*b;
return make('geo-sim-side-'+c,'Triangles ABC and DEF are similar with A corresponding to D, B to E, and C to F. AB = '+a+', DE = '+(k*a)+', BC = '+b+', and EF = x. Find x.',a+'*x='+(k*a*b),x,'Corresponding side lengths have the same ratio.',{kind:'geo-sim',sides:[a,b,Math.max(Math.abs(a-b)+1,Math.min(a+b-1,Math.round((a+b)*0.75)))],k:k,show:['AB','BC','DE'],lab:{EF:'x'},marks:true});}
function scale(ctx){var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:5),a=r.int(3,14),x=k;
return make('geo-sim-scale-'+c,'A triangle has a side of length '+a+'. Its image after a dilation has the corresponding side of length '+(a*k)+'. Find the scale factor x.',a+'*x='+(a*k),x,'Image length = scale factor × original length.',{kind:'geo-sim',sides:[a,a+r.int(0,2)||a,Math.max(1,a-1)],k:k,show:['AB','DE'],note:'Not drawn to scale. Triangle DEF is the image of triangle ABC.'});}
function perimeter(ctx){var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?6:4),p=r.int(18,45),x=k*p;
return make('geo-sim-perimeter-'+c,'Two similar triangles have corresponding side lengths 5 and '+(5*k)+'. The smaller triangle has perimeter '+p+'. Find the larger perimeter x.', '5*x='+(5*x),x,'Perimeters of similar figures have the same ratio as corresponding sides.',{kind:'geo-sim',sides:[5,r.int(4,7),r.int(4,7)],k:k,show:['AB','DE'],note:'Not drawn to scale. The triangles are similar.'});}
function shadow(ctx){var r=ctx.rng,c=ctx.c,h=r.int(3,8),s=r.int(2,6),k=r.int(2,c>=5?7:5),x=h*k;
return make('geo-sim-shadow-'+c,'At the same time of day, a vertical pole '+h+' feet tall casts a '+s+'-foot shadow. A nearby tree casts a '+(s*k)+'-foot shadow on level ground. Assuming parallel sun rays, find the tree height x in feet.',s+'*x='+(h*s*k),x,'The height-to-shadow ratios are equal for the similar right triangles.',{kind:'geo-shadow',h:h,s:s,H:x,S:s*k,names:['pole','tree'],unit:'ft',lab:{H:'x'}});}
function angle(ctx){var r=ctx.rng,c=ctx.c,x=r.int(30,90),a=r.int(25,Math.min(75,155-x)),b=180-x-a;
return make('geo-sim-angle-'+c,'Triangles ABC and DEF are similar, with A corresponding to D, B to E, and C to F. In ABC, angle A = '+a+'° and angle B = '+b+'°. Find angle F, called x.', 'x+'+a+'+'+b+'=180',x,'Corresponding angles match; angles in a triangle sum to 180°.',{kind:'geo-sim',angles:[a,b,180-a-b],k:1.3,ang:{A:a,B:b,F:'x'},marks:true});}
/* Similarity criteria: the hypotheses are explicitly stated so students
   must distinguish AA, SAS and SSS rather than infer similarity from a sketch. */
function aaCriterion(ctx){
 var r=ctx.rng,c=ctx.c,a=r.int(25,60),b=r.int(25,Math.min(75,145-a)),x=180-a-b;
 var eq='x+'+a+'+'+b+'=180';
 return make('geo-sim-aa-'+c,
  'Triangles ABC and DEF have angle A congruent to angle D and angle B congruent to angle E. In triangle ABC, angles A and B measure '+a+'° and '+b+'°. By AA, the triangles are similar. Find the measure x of angle F and explain the correspondence.',
  eq,x,'Two pairs of equal angles establish AA similarity; corresponding third angles are equal.',{kind:'geo-sim',angles:[a,b,x],k:1.3,ang:{A:a,B:b,F:'x'},marks:true});
}
function sasCriterion(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:4),a=r.int(3,11),b=r.int(4,12),x=k*b;
 var eq=a+'*x='+(a*x);
 return make('geo-sim-sas-'+c,
  'Triangles ABC and DEF have congruent included angles A and D. The sides enclosing those angles are AB = '+a+', AC = '+b+', DE = '+(a*k)+', and DF = x. The two enclosing side pairs are proportional, establishing SAS similarity. Find x and name the criterion.',
  eq,x,'SAS similarity requires proportional sides surrounding a congruent included angle.',{kind:'geo-sim',sas:[a,b,55],k:k,show:['AB','CA','DE'],lab:{FD:'x'},marks:['A','D']});
}
function sssCriterion(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:4),a=r.int(5,11),b=r.int(5,11),d=r.int(Math.abs(a-b)+1,a+b-1),x;for(var tr=0;tr<60;tr++){var sd=[a,b,d].sort(function(u,v){return u-v}),big=sd[2];if(big<=sd[0]*1.6&&sd[0]+sd[1]>=big*1.25)break;a=r.int(5,11);b=r.int(5,11);d=r.int(Math.abs(a-b)+1,a+b-1);}x=k*d;
 var eq=d+'*x='+(d*x);
 return make('geo-sim-sss-'+c,
  'Triangles ABC and DEF have corresponding sides AB = '+a+', DE = '+(k*a)+', BC = '+b+', EF = '+(k*b)+', AC = '+d+', and DF = x. All three side pairs must have the same ratio for SSS similarity. Find x and state why the triangles are similar.',
  eq,x,'SSS similarity requires equality of all three corresponding side ratios.',{kind:'geo-sim',sides:[a,b,d],k:k,show:['AB','BC','CA','DE','EF'],lab:{FD:'x'},marks:false});
}
/* Triangle proportionality: DE parallel BC, with D on AB and E on AC. */
function parallelSegment(ctx){
 var r=ctx.rng,c=ctx.c,ad=r.int(3,9),db=r.int(2,7),factor=r.int(2,c>=5?6:4);
 var ae=ad*factor,x=db*factor,eq=ad+'*x='+(db*ae);
 return {variant:'geo-sim-parallel-'+c,
  fig:{kind:'geo-tri-par',v:{AD:ad,DB:db,AE:ae,EC:x},angA:65,schem:true,note:'Not drawn to scale.',show:['AD','DB','AE'],lab:{EC:'x'}},
  prompt:'In triangle ABC, D lies on AB and E lies on AC, with DE parallel to BC. AD = '+ad+', DB = '+db+', and AE = '+ae+'. Find EC = x. Explain why the two sides are divided proportionally.',
  parts:[{prompt:'Find EC.',answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
  steps:[step('Triangle proportionality theorem: AD/DB = AE/EC.',M(ad+'/'+db+'='+ae+'/x')),
         step('Cross multiply.',M(eq)),step('Solve.',M('x='+x))],
  space:[1.5,1.8,2]};
}
/* Four connected answers, each computed from independent equations.
   No final-answer equation is displayed in the student question. */
function parallelHonors(ctx){
 var r=ctx.rng,c=ctx.c,ad=r.int(3,8),db=r.int(2,7),factor=r.int(2,5);
 var ae=ad*factor,ec=db*factor,ab=ad+db,ac=ae+ec;
 /* Keep all four answers integral, including BC and the perimeter, even at tier 1. */
 var de=ae,bc=de*ab/ad; // ADE is isosceles (AD, AE, DE): strict triangle inequality always holds.
 var p=ab+ac+bc;
 return {variant:'geo-sim-parallel-honors-'+c,
  fig:{kind:'geo-tri-par',v:{AD:ad,DB:db,AE:ae,EC:ec},BC:bc,schem:true,note:'Not drawn to scale.',show:['AD','DB','AE'],lab:{EC:'x',DE:String(de)}},
  prompt:'Honors investigation: In triangle ABC, D is on AB and E is on AC, with DE parallel to BC. AD = '+ad+', DB = '+db+', AE = '+ae+', and DE = '+de+'. Answer all four parts. Show proportional reasoning and justify each result.',
  parts:[
   {prompt:'(a) Find EC = x using the triangle proportionality theorem. Show the proportion you use.',answer:M('x='+ec),check:{type:'solve',eq:ad+'*x='+(db*ae),v:'x'}},
   {prompt:'(b) Find the full side AC = y. Show how the segment lengths combine.',answer:M('y='+ac),check:{type:'solve',eq:'y='+ae+'+'+ec,v:'y'}},
   {prompt:'(c) Find BC = z using similarity of triangles ADE and ABC. Set up the proportion.',answer:M('z='+bc),check:{type:'solve',eq:ad+'*z='+(de*ab),v:'z'}},
   {prompt:'(d) Find the perimeter of triangle ABC = w. Explain which lengths you add.',answer:M('w='+p),check:{type:'solve',eq:'w='+ab+'+'+ac+'+'+bc,v:'w'}}
  ],
  steps:[
   step('Parallel lines divide sides proportionally.',M(ad+'*x='+(db*ae))),
   step('Find the full side AC.',M('y='+ae+'+'+ec)),
   step('Corresponding sides in similar triangles are proportional.',M(ad+'*z='+(de*ab))),
   step('Add the three sides of ABC.',M('w='+ab+'+'+ac+'+'+bc))
  ],space:[2.1,2.6,3.1]};
}

/* ---------- Honors investigations (algebra, ratios and several theorems per problem) ----------
   Four-part chains; variants geo-similarity-investigation-* use the shared investigation verifier. */
function lin(a,b,v){var t=a===1?v:a+v;return b>0?t+'+'+b:b<0?t+'-'+(-b):t;}
function sg(n){return n<0?'('+n+')':String(n);}
function ge(a,b){while(b){var t=a%b;a=b;b=t;}return a;}
function triOk(a,b,c){return a+b>c&&a+c>b&&b+c>a;}
/* 1: similar triangles with a ratio, algebraic sides, perimeter of the larger triangle */
function invRatio(ctx){
 var r=ctx.rng,c=ctx.c,tries=0,p,q,x,y,a1,b1,a2,b2,c1,d1,c2,d2,ab,ac,m,m0,bc;
 do{q=r.int(2,4);p=q+r.int(1,3);tries++;}while(ge(p,q)!==1&&tries<200);
 tries=0;
 do{x=r.int(3,c>=6?14:10);a1=r.int(1,4);ab=q*r.int(2,6);b1=ab-a1*x;a2=r.int(1,5);b2=p*ab/q-a2*x;
  y=r.int(3,c>=6?14:10);c1=r.int(1,4);ac=q*r.int(2,6);d1=ac-c1*y;c2=r.int(1,5);d2=p*ac/q-c2*y;
  m0=r.int(2,6);m=q*m0;bc=m;tries++;}
 while((q*a2===p*a1||q*c2===p*c1||!triOk(ab,ac,bc)||Math.abs(b1)>30||Math.abs(b2)>40||Math.abs(d1)>30||Math.abs(d2)>40)&&tries<4000);
 var eAB=lin(a1,b1,'x'),eDE=lin(a2,b2,'x'),eAC=lin(c1,d1,'y'),eDF=lin(c2,d2,'y');
 var per=p*(ab+ac+bc)/q;
 var cxx=(ab*ab+ac*ac-bc*bc)/(2*ab),cyy=Math.sqrt(ac*ac-cxx*cxx),sc=3/Math.max(ab,bc,ac),kk=p/q,off=3.6;
 var fig={kind:'geo-cong',pts:{A:[0,0],B:[ab*sc,0],C:[cxx*sc,cyy*sc],D:[off,0],E:[off+ab*sc*kk,0],F:[off+cxx*sc*kk,cyy*sc*kk]},segs:[['A','B'],['B','C'],['C','A'],['D','E'],['E','F'],['F','D']],tris:[['A','B','C'],['D','E','F']],sides:[],angles:[],right:[],lab:{AB:eAB,DE:eDE,AC:eAC,DF:eDF,BC:String(bc),EF:'w'},note:'Not drawn to scale. The triangles are similar.'};
 var eP='q*v=p*(('+a1+'*'+x+(b1<0?'-'+(-b1):'+'+b1)+')+'+bc+'+('+c1+'*'+y+(d1<0?'-'+(-d1):'+'+d1)+'))';
 eP=eP.replace('q*',q+'*').replace('p*',p+'*');
 return {variant:'geo-similarity-investigation-ratio-'+c,fig:fig,
  prompt:'Open Response: Triangle ABC is similar to triangle DEF with A corresponding to D, B to E, and C to F. The ratio of corresponding sides DE to AB is '+p+' to '+q+'. AB = '+M(eAB)+' and DE = '+M(eDE)+'. AC = '+M(eAC)+' and DF = '+M(eDF)+'. BC = '+bc+' and EF = w. Write a proportion and show the equation you solve in every part.',
  parts:[
   {label:'a',prompt:'Use the sides AB and DE to find x.',answer:M('x='+x),check:{type:'solve',eq:q+'*('+eDE+')='+p+'*('+eAB+')',v:'x'}},
   {label:'b',prompt:'Use the sides AC and DF to find y.',answer:M('y='+y),check:{type:'solve',eq:q+'*('+eDF+')='+p+'*('+eAC+')',v:'y'}},
   {label:'c',prompt:'Find the length EF = w.',answer:M('w='+p*m0),check:{type:'solve',eq:q+'*w='+p+'*'+bc,v:'w'}},
   {label:'d',prompt:'Find the perimeter of triangle DEF, using your values of x and y.',answer:M('v='+per),check:{type:'solve',eq:eP,v:'v'}}
  ],
  steps:[step('Corresponding sides are in the ratio '+p+':'+q+', so '+M(q+'*('+eDE+')='+p+'*('+eAB+')')+'.',M('x='+x)),step('The same ratio holds for AC and DF: '+M(q+'*('+eDF+')='+p+'*('+eAC+')')+'.',M('y='+y)),step('For BC and EF: '+M(q+'*w='+p+'*'+bc)+'.',M('w='+p*m0)),step('Scale the perimeter of ABC (AB + BC + AC) by '+p+':'+q+': '+M(eP)+'.',M('v='+per))],
  space:[3,3.6,4.2]};
}
/* 2: triangle proportionality with algebraic segments */
function invParallel(ctx){
 var r=ctx.rng,c=ctx.c,tries=0,s1,s2,t,u,w0,x,a1,a2,b1,b2,ad,db,ae,ec,de,ab,ac,bc;
 do{s1=r.int(1,4);s2=r.int(1,4);t=r.int(2,6);u=r.int(2,6);w0=r.int(2,6);x=r.int(3,c>=6?13:9);a1=r.int(1,4);a2=r.int(1,4);
  ad=s1*t;db=s2*t;b1=ad-a1*x;b2=db-a2*x;ae=s1*u;ec=s2*u;de=s1*w0;ab=ad+db;ac=ae+ec;bc=(s1+s2)*w0;tries++;}
 while((ec*a1===ae*a2||s1===s2&&0||!triOk(t,u,w0)||Math.abs(b1)>30||Math.abs(b2)>30||ad<3||db<3||ae<3||ec<3)&&tries<4000);
 var eAD=lin(a1,b1,'x'),eDB=lin(a2,b2,'x');
 var Pp={A:[0,2.2],B:[-1.7,0],C:[1.9,0]};var fr=ad/ab,fe=ae/ac;Pp.D=[Pp.A[0]+(Pp.B[0]-Pp.A[0])*fr,Pp.A[1]+(Pp.B[1]-Pp.A[1])*fr];Pp.E=[Pp.A[0]+(Pp.C[0]-Pp.A[0])*fe,Pp.A[1]+(Pp.C[1]-Pp.A[1])*fe];
 var fig={kind:'geo-cong',pts:Pp,segs:[['A','B'],['A','C'],['B','C'],['D','E']],tris:null,sides:[],angles:[],right:[],lab:{AD:eAD,DB:eDB,DE:String(de),AE:String(ae),EC:String(ec),BC:'z'},note:'Not drawn to scale.'};
 return {variant:'geo-similarity-investigation-parallel-'+c,fig:fig,
  prompt:'Open Response: In triangle ABC, D is on AB and E is on AC, with DE parallel to BC. AD = '+M(eAD)+' and DB = '+M(eDB)+'. AE = '+ae+', EC = '+ec+', and DE = '+de+'. Name the theorem you use in every part and show the equation you write.',
  parts:[
   {label:'a',prompt:'Use the triangle proportionality theorem to find x.',answer:M('x='+x),check:{type:'solve',eq:ec+'*('+eAD+')='+ae+'*('+eDB+')',v:'x'}},
   {label:'b',prompt:'Find the length AB, using your value of x.',answer:M('w='+ab),check:{type:'solve',eq:'w=('+a1+'*'+x+(b1<0?'-'+(-b1):'+'+b1)+')+('+a2+'*'+x+(b2<0?'-'+(-b2):'+'+b2)+')',v:'w'}},
   {label:'c',prompt:'Triangle ADE is similar to triangle ABC. Use this to find BC = z.',answer:M('z='+bc),check:{type:'solve',eq:'('+a1+'*'+x+(b1<0?'-'+(-b1):'+'+b1)+')*z='+de+'*'+ab,v:'z'}},
   {label:'d',prompt:'Find the perimeter of triangle ABC.',answer:M('v='+(ab+ac+bc)),check:{type:'solve',eq:'v='+ab+'+'+bc+'+('+ae+'+'+ec+')',v:'v'}}
  ],
  steps:[step('Parallel lines cut the sides proportionally, so '+M(ec+'*('+eAD+')='+ae+'*('+eDB+')')+'.',M('x='+x)),step('AB is AD plus DB.',M('w='+ab)),step('Triangles ADE and ABC are similar, so AD:AB = DE:BC: '+M('('+a1+'*'+x+(b1<0?'-'+(-b1):'+'+b1)+')*z='+de+'*'+ab)+'.',M('z='+bc)),step('AC = AE + EC, so add the three sides.',M('v='+(ab+ac+bc)))],
  space:[3,3.6,4.2]};
}
/* 3: dilation about the origin on the coordinate plane */
function invDilation(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=6?4:3),a=r.int(2,4),b=r.int(2,4),px=r.int(-4,0),py=r.int(-4,0);
 var A=[px,py],B=[px+a,py],Cp=[px+a,py+b];
 if(B[0]===0||Cp[1]===0){px-=1;py-=1;A=[px,py];B=[px+a,py];Cp=[px+a,py+b];}
 var Pt=function(q){return '('+q[0]+', '+q[1]+')';},w=k*a,area=w*k*b/2;
 var fig={kind:'geo-grid',shapes:[{id:'pre',pts:[A,B,Cp],labels:['A','B','C']}],lines:[],alt:'Coordinate plane with triangle ABC'};
 return {variant:'geo-similarity-investigation-dilation-'+c,fig:fig,
  prompt:'Open Response: Triangle ABC has vertices A'+Pt(A)+', B'+Pt(B)+', and C'+Pt(Cp)+'. It is dilated about the origin by a scale factor of '+k+' to form triangle A′B′C′. Show the rule or formula you use in every part.',
  parts:[
   {label:'a',prompt:'Find the x-coordinate of B′.',answer:M('p='+k*B[0]),check:{type:'solve',eq:'p='+k+'*'+sg(B[0]),v:'p'}},
   {label:'b',prompt:'Find the y-coordinate of C′.',answer:M('q='+k*Cp[1]),check:{type:'solve',eq:'q='+k+'*'+sg(Cp[1]),v:'q'}},
   {label:'c',prompt:'Find the length of A′B′. (AB is horizontal. Lengths scale by the scale factor.)',answer:M('t='+w),check:{type:'solve',eq:'t='+k+'*('+sg(B[0])+'-'+sg(A[0])+')',v:'t'}},
   {label:'d',prompt:'Triangle A′B′C′ has a right angle at B′. Find its area, using your answer to (c).',answer:M('v='+area),check:{type:'solve',eq:'2*v='+w+'*('+k+'*('+sg(Cp[1])+'-'+sg(B[1])+'))',v:'v'}}
  ],
  steps:[step('A dilation about the origin multiplies each coordinate by the scale factor: '+M('p='+k+'*'+sg(B[0]))+'.',M('p='+k*B[0])),step('Do the same to the y-coordinate of C: '+M('q='+k+'*'+sg(Cp[1]))+'.',M('q='+k*Cp[1])),step('The original length AB is the difference of the x-coordinates, multiplied by '+k+': '+M('t='+k+'*('+sg(B[0])+'-'+sg(A[0])+')')+'.',M('t='+w)),step('Area of a right triangle is half the product of its legs. B′C′ is '+k+' times BC: '+M('2*v='+w+'*('+k+'*('+sg(Cp[1])+'-'+sg(B[1])+'))')+'.',M('v='+area))],
  space:[3,3.6,4.2]};
}
/* 4: altitude to the hypotenuse of a right triangle (geometric means) */
function invAltitude(ctx){
 var r=ctx.rng,c=ctx.c,tries=0,g,pp,qq,ad,db,cd,x,a,b,ab;
 do{g=r.int(1,3);pp=r.int(1,4);qq=r.int(1,4);ad=g*pp*pp;db=g*qq*qq;cd=g*pp*qq;x=r.int(3,c>=6?14:10);a=r.int(1,4);b=ad-a*x;ab=ad+db;tries++;}
 while((pp===qq||ge(pp,qq)!==1||ad<4||db<4||Math.abs(b)>30||tries<1)&&tries<4000);
 var eAD=lin(a,b,'x'),s=ab/3.2;
 var P={A:[0,0],B:[ab/s,0],D:[ad/s,0],C:[ad/s,cd/s]};
 var fig={kind:'geo-cong',pts:P,segs:[['A','B'],['A','C'],['C','B'],['C','D']],tris:[['A','C','D'],['C','D','B']],sides:[],angles:[],right:[['A','C','B'],['C','D','B']],lab:{AD:eAD,BD:String(db),CD:String(cd)},note:'Not drawn to scale.'};
 var ADs='('+a+'*'+x+(b<0?'-'+(-b):'+'+b)+')';
 return {variant:'geo-similarity-investigation-altitude-'+c,fig:fig,
  prompt:'Open Response: In right triangle ABC, the right angle is at C and CD is the altitude to hypotenuse AB. AD = '+M(eAD)+', DB = '+db+', and CD = '+cd+'. Name the similarity relationship you use in every part and show the equation you write.',
  parts:[
   {label:'a',prompt:'Triangles ACD and CBD are similar, so CD is the geometric mean of AD and DB. Find x.',answer:M('x='+x),check:{type:'solve',eq:db+'*('+eAD+')='+cd+'*'+cd,v:'x'}},
   {label:'b',prompt:'Find the length of the hypotenuse AB, using your value of x.',answer:M('w='+ab),check:{type:'solve',eq:'w='+ADs+'+'+db,v:'w'}},
   {label:'c',prompt:'Each leg is the geometric mean of the hypotenuse and the part next to it. Find AC squared.',answer:M('k='+ad*ab),check:{type:'solve',eq:'k='+ADs+'*'+ab,v:'k'}},
   {label:'d',prompt:'Find the area of triangle ABC, using AB as the base.',answer:M('t='+ab*cd/2),check:{type:'solve',eq:'2*t='+ab+'*'+cd,v:'t'}}
  ],
  steps:[step('CD² = AD · DB, so '+M(db+'*('+eAD+')='+cd+'*'+cd)+'.',M('x='+x)),step('AB = AD + DB.',M('w='+ab)),step('AC² = AD · AB, so '+M('k='+ADs+'*'+ab)+'.',M('k='+ad*ab)),step('The altitude CD is the height to base AB: '+M('2*t='+ab+'*'+cd)+'.',M('t='+ab*cd/2))],
  space:[3,3.6,4.2]};
}
NS.registerSkillSet({id:'geometry-similarity',course:'geometry',courseName:'Geometry',unit:'similarity',unitName:'Similarity',title:'Similarity Foundations',
tags:{RATIOS:'Corresponding side ratios',DILATION:'Scale factors',PERIMETER:'Similar perimeters',APPLICATION:'Indirect measurement',ANGLES:'Corresponding angles',CRITERIA:'AA, SAS, and SSS similarity',PARALLEL:'Triangle proportionality and parallel segments',HONORS:'Multi-step Honors similarity investigations'},
reference:'<div class="mm-refgrid"><section><h4>Similar figures</h4><p>Corresponding angles are equal; corresponding side lengths have a constant ratio.</p></section><section><h4>Dilations</h4><p>Image length = scale factor × original length.</p></section></div>',
gaps:['Coordinate dilations, similarity proofs, and area and volume ratios of similar figures are not generated.'],
skills:[
{id:'similarity-missing-side',tag:'RATIOS',name:'Find a corresponding side',best:[0,1],generate:missingSide},
{id:'similarity-scale-factor',tag:'DILATION',name:'Find a dilation scale factor',best:[0,1],generate:scale},
{id:'similarity-perimeter',tag:'PERIMETER',name:'Scale a perimeter',best:[0,1],generate:perimeter},
{id:'similarity-shadow',tag:'APPLICATION',name:'Indirect measurement using shadows',best:[0,1],generate:shadow},
{id:'similarity-angle',tag:'ANGLES',name:'Corresponding angle in similar triangles',best:[0,1],generate:angle},
{id:'similarity-aa-criterion',tag:'CRITERIA',name:'AA similarity and third-angle correspondence',best:[0,1],generate:aaCriterion},
{id:'similarity-sas-criterion',tag:'CRITERIA',name:'SAS similarity with included angles',best:[1],generate:sasCriterion},
{id:'similarity-sss-criterion',tag:'CRITERIA',name:'SSS similarity from three side ratios',best:[1],generate:sssCriterion},
{id:'similarity-parallel-segment',tag:'PARALLEL',name:'Triangle proportionality theorem',best:[0,1],generate:parallelSegment},
{id:'similarity-investigation-ratio',tag:'HONORS',name:'Honors: similar triangles with algebraic sides and perimeter',best:[2],generate:invRatio},
{id:'similarity-investigation-parallel',tag:'HONORS',name:'Honors: triangle proportionality with algebra',best:[2],generate:invParallel},
{id:'similarity-investigation-dilation',tag:'HONORS',name:'Honors: dilation on the coordinate plane, lengths and area',best:[2],generate:invDilation},
{id:'similarity-investigation-altitude',tag:'HONORS',name:'Honors: altitude to the hypotenuse and geometric means',best:[2],generate:invAltitude},
{id:'similarity-parallel-honors',tag:'PARALLEL',name:'Four-part Honors proportionality investigation',best:[2],generate:parallelHonors}
]});
})(typeof window!=='undefined'?window:globalThis);
