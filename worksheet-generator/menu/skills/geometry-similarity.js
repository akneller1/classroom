/* Geometry Unit 5: independently verifiable starter questions on similarity. */
(function(G){'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(variant,prompt,eq,x,rule){var kind=/^geo-sim-(aa|sas|sss|side|angle)-/.exec(variant);var fig=kind?{kind:'geo-similar-pair',case:kind[1]==='side'||kind[1]==='angle'?'sides':kind[1]}:null;return {variant:variant,fig:fig,prompt:prompt,parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(rule,M(eq)),step('Solve for x.',M('x='+x))],space:[1.2,1.5,1.8]};}
function missingSide(ctx){var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?6:4),a=r.int(3,12),b=r.int(3,12),x=k*b;
return make('geo-sim-side-'+c,'Triangles ABC and DEF are similar with A corresponding to D, B to E, and C to F. AB = '+a+', DE = '+(k*a)+', BC = '+b+', and EF = x. Find x.',a+'*x='+(k*a*b),x,'Corresponding side lengths have the same ratio.');}
function scale(ctx){var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:5),a=r.int(3,14),x=k;
return make('geo-sim-scale-'+c,'A triangle has a side of length '+a+'. Its image after a dilation has the corresponding side of length '+(a*k)+'. Find the scale factor x.',a+'*x='+(a*k),x,'Image length = scale factor × original length.');}
function perimeter(ctx){var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?6:4),p=r.int(18,45),x=k*p;
return make('geo-sim-perimeter-'+c,'Two similar polygons have corresponding side lengths 5 and '+(5*k)+'. The smaller polygon has perimeter '+p+'. Find the larger perimeter x.', '5*x='+(5*x),x,'Perimeters of similar figures have the same ratio as corresponding sides.');}
function shadow(ctx){var r=ctx.rng,c=ctx.c,h=r.int(3,8),s=r.int(2,6),k=r.int(2,c>=5?7:5),x=h*k;
return make('geo-sim-shadow-'+c,'At the same time of day, a vertical pole '+h+' feet tall casts a '+s+'-foot shadow. A nearby tree casts a '+(s*k)+'-foot shadow on level ground. Assuming parallel sun rays, find the tree height x in feet.',s+'*x='+(h*s*k),x,'The height-to-shadow ratios are equal for the similar right triangles.');}
function angle(ctx){var r=ctx.rng,c=ctx.c,x=r.int(30,90),a=r.int(25,Math.min(75,155-x)),b=180-x-a;
return make('geo-sim-angle-'+c,'Triangles ABC and DEF are similar, with A corresponding to D, B to E, and C to F. In ABC, angle A = '+a+'° and angle B = '+b+'°. Find angle F, called x.', 'x+'+a+'+'+b+'=180',x,'Corresponding angles match; angles in a triangle sum to 180°.');}
/* Similarity criteria: the hypotheses are explicitly stated so students
   must distinguish AA, SAS and SSS rather than infer similarity from a sketch. */
function aaCriterion(ctx){
 var r=ctx.rng,c=ctx.c,a=r.int(25,60),b=r.int(25,Math.min(75,145-a)),x=180-a-b;
 var eq='x+'+a+'+'+b+'=180';
 return make('geo-sim-aa-'+c,
  'Triangles ABC and DEF have angle A congruent to angle D and angle B congruent to angle E. In triangle ABC, angles A and B measure '+a+'° and '+b+'°. By AA, the triangles are similar. Find the measure x of angle F and explain the correspondence.',
  eq,x,'Two pairs of equal angles establish AA similarity; corresponding third angles are equal.');
}
function sasCriterion(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:4),a=r.int(3,11),b=r.int(4,12),x=k*b;
 var eq=a+'*x='+(a*x);
 return make('geo-sim-sas-'+c,
  'Triangles ABC and DEF have congruent included angles A and D. The sides enclosing those angles are AB = '+a+', AC = '+b+', DE = '+(a*k)+', and DF = x. The two enclosing side pairs are proportional, establishing SAS similarity. Find x and name the criterion.',
  eq,x,'SAS similarity requires proportional sides surrounding a congruent included angle.');
}
function sssCriterion(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:4),a=r.int(5,11),b=r.int(5,11),d=r.int(Math.abs(a-b)+1,a+b-1),x=k*d;
 var eq=d+'*x='+(d*x);
 return make('geo-sim-sss-'+c,
  'Triangles ABC and DEF have corresponding sides AB = '+a+', DE = '+(k*a)+', BC = '+b+', EF = '+(k*b)+', AC = '+d+', and DF = x. All three side pairs must have the same ratio for SSS similarity. Find x and state why the triangles are similar.',
  eq,x,'SSS similarity requires equality of all three corresponding side ratios.');
}
/* Triangle proportionality: DE parallel BC, with D on AB and E on AC. */
function parallelSegment(ctx){
 var r=ctx.rng,c=ctx.c,ad=r.int(3,9),db=r.int(2,7),factor=r.int(2,c>=5?6:4);
 var ae=ad*factor,x=db*factor,eq=ad+'*x='+(db*ae);
 return {variant:'geo-sim-parallel-'+c,
  fig:{kind:'geo-similar-pair',case:'parallel'},
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
  fig:{kind:'geo-similar-pair',case:'parallel'},
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
NS.registerSkillSet({id:'geometry-similarity',course:'geometry',courseName:'Geometry',unit:'similarity',unitName:'Similarity',title:'Similarity Foundations',
tags:{RATIOS:'Corresponding side ratios',DILATION:'Scale factors',PERIMETER:'Similar perimeters',APPLICATION:'Indirect measurement',ANGLES:'Corresponding angles',CRITERIA:'AA, SAS, and SSS similarity',PARALLEL:'Triangle proportionality and parallel segments'},
reference:'<div class="mm-refgrid"><section><h4>Similar figures</h4><p>Corresponding angles are equal; corresponding side lengths have a constant ratio.</p></section><section><h4>Dilations</h4><p>Image length = scale factor × original length.</p></section></div>',
gaps:['Starter bank only. Coordinate dilations and formal proofs remain pending.'],
skills:[
{id:'similarity-missing-side',tag:'RATIOS',name:'Find a corresponding side',best:[0,1,2],generate:missingSide},
{id:'similarity-scale-factor',tag:'DILATION',name:'Find a dilation scale factor',best:[0,1,2],generate:scale},
{id:'similarity-perimeter',tag:'PERIMETER',name:'Scale a perimeter',best:[0,1,2],generate:perimeter},
{id:'similarity-shadow',tag:'APPLICATION',name:'Indirect measurement using shadows',best:[0,1,2],generate:shadow},
{id:'similarity-angle',tag:'ANGLES',name:'Corresponding angle in similar triangles',best:[0,1,2],generate:angle},
{id:'similarity-aa-criterion',tag:'CRITERIA',name:'AA similarity and third-angle correspondence',best:[0,1,2],generate:aaCriterion},
{id:'similarity-sas-criterion',tag:'CRITERIA',name:'SAS similarity with included angles',best:[1,2],generate:sasCriterion},
{id:'similarity-sss-criterion',tag:'CRITERIA',name:'SSS similarity from three side ratios',best:[1,2],generate:sssCriterion},
{id:'similarity-parallel-segment',tag:'PARALLEL',name:'Triangle proportionality theorem',best:[0,1,2],generate:parallelSegment},
{id:'similarity-parallel-honors',tag:'PARALLEL',name:'Four-part Honors proportionality investigation',best:[2],generate:parallelHonors}
]});
})(typeof window!=='undefined'?window:globalThis);
