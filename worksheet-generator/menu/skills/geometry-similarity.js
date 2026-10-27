/* Geometry Unit 5: independently verifiable starter questions on similarity. */
(function(G){'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(variant,prompt,eq,x,rule){var kind=/^geo-sim-(aa|sas|sss|side|angle)-/.exec(variant);var fig=kind?{kind:'geo-similar-pair',case:kind[1]==='side'||kind[1]==='angle'?'sides':kind[1]}:null;return {variant:variant,fig:fig,prompt:prompt+' Use '+M(eq)+' to find x.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(rule,M(eq)),step('Solve for x.',M('x='+x))],space:[1.2,1.5,1.8]};}
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
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?7:4),a=r.int(5,11),b=r.int(5,11),d=r.int(5,11),x=k*d;
 var eq=d+'*x='+(d*x);
 return make('geo-sim-sss-'+c,
  'Triangles ABC and DEF have corresponding sides AB = '+a+', DE = '+(k*a)+', BC = '+b+', EF = '+(k*b)+', AC = '+d+', and DF = x. All three side pairs must have the same ratio for SSS similarity. Find x and state why the triangles are similar.',
  eq,x,'SSS similarity requires equality of all three corresponding side ratios.');
}
NS.registerSkillSet({id:'geometry-similarity',course:'geometry',courseName:'Geometry',unit:'similarity',unitName:'Similarity',title:'Similarity Foundations',
tags:{RATIOS:'Corresponding side ratios',DILATION:'Scale factors',PERIMETER:'Similar perimeters',APPLICATION:'Indirect measurement',ANGLES:'Corresponding angles',CRITERIA:'AA, SAS, and SSS similarity'},
reference:'<div class="mm-refgrid"><section><h4>Similar figures</h4><p>Corresponding angles are equal; corresponding side lengths have a constant ratio.</p></section><section><h4>Dilations</h4><p>Image length = scale factor × original length.</p></section></div>',
gaps:['Starter bank only. Proportionality theorems, coordinate dilations, diagrams, and formal proofs remain pending.'],
skills:[
{id:'similarity-missing-side',tag:'RATIOS',name:'Find a corresponding side',best:[0,1,2],generate:missingSide},
{id:'similarity-scale-factor',tag:'DILATION',name:'Find a dilation scale factor',best:[0,1,2],generate:scale},
{id:'similarity-perimeter',tag:'PERIMETER',name:'Scale a perimeter',best:[0,1,2],generate:perimeter},
{id:'similarity-shadow',tag:'APPLICATION',name:'Indirect measurement using shadows',best:[0,1,2],generate:shadow},
{id:'similarity-angle',tag:'ANGLES',name:'Corresponding angle in similar triangles',best:[0,1,2],generate:angle},
{id:'similarity-aa-criterion',tag:'CRITERIA',name:'AA similarity and third-angle correspondence',best:[0,1,2],generate:aaCriterion},
{id:'similarity-sas-criterion',tag:'CRITERIA',name:'SAS similarity with included angles',best:[1,2],generate:sasCriterion},
{id:'similarity-sss-criterion',tag:'CRITERIA',name:'SSS similarity from three side ratios',best:[1,2],generate:sssCriterion}
]});
})(typeof window!=='undefined'?window:globalThis);
