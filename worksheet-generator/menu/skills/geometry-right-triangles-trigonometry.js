/* Geometry Unit 6: integer-answer right triangle and trig starter bank. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
var triples=[[3,4,5],[5,12,13],[8,15,17],[7,24,25],[20,21,29],[9,40,41],[12,35,37],[11,60,61],[28,45,53],[16,63,65],[33,56,65],[48,55,73]];
function make(id,prompt,eq,x,reason,kind){var type=/^geo-right-(hyp|leg|sin|cos|tan|45|30|elevation)-/.exec(id);return {variant:id,fig:type?{kind:'geo-right-triangle',case:type[1]}:(id.indexOf('geo-right-depression-')===0?{kind:'geo-right-triangle',case:'elevation'}:null),prompt:prompt+' Use '+M(eq)+' to find x.',parts:[{answer:M('x='+x),check:kind?{type:'geo-pythagorean',kind:kind,eq:eq}:{type:'solve',eq:eq,v:'x'}}],steps:[step(reason,M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};}
function triple(ctx){var r=ctx.rng,t=triples[r.int(0,ctx.c>=5?triples.length-1:8)],k=r.int(1,ctx.c>=5?12:8);return t.map(n=>n*k);}
function hyp(ctx){var t=triple(ctx),a=t[0],b=t[1],x=t[2],eq='x^2='+a+'^2+'+b+'^2';return make('geo-right-hyp-'+ctx.c,'A right triangle has legs '+a+' and '+b+' units. Find the positive hypotenuse length x.',eq,x,'Apply the Pythagorean theorem.','hyp');}
function leg(ctx){var t=triple(ctx),a=t[0],x=t[1],h=t[2],eq=a+'^2+x^2='+h+'^2';return make('geo-right-leg-'+ctx.c,'A right triangle has hypotenuse '+h+' units and one leg '+a+' units. Find the positive length x of the other leg.',eq,x,'Apply the Pythagorean theorem and take the positive root.','leg');}
function distance(ctx){var t=triple(ctx),dx=t[0],dy=t[1],x=t[2],eq='x^2='+dx+'^2+'+dy+'^2';return make('geo-right-distance-'+ctx.c,'Points A(0, 0) and B('+dx+', '+dy+') lie on a coordinate plane. Find the positive distance x between them.',eq,x,'Use the distance formula (Pythagorean theorem).','distance');}
function trig(ctx,kind){var t=triple(ctx),opp=t[0],adj=t[1],hyp=t[2],x,eq,prompt;
if(kind==='sin'){x=opp;eq=hyp+'*x='+opp+'*'+hyp;prompt='A right triangle has hypotenuse '+hyp+' and an acute angle θ with sin θ = '+opp+'/'+hyp+'. Find the positive length x of the side opposite θ.';}
else if(kind==='cos'){x=adj;eq=hyp+'*x='+adj+'*'+hyp;prompt='A right triangle has hypotenuse '+hyp+' and an acute angle θ with cos θ = '+adj+'/'+hyp+'. Find the positive length x of the side adjacent to θ.';}
else{x=opp;eq=adj+'*x='+opp+'*'+adj;prompt='A right triangle has an acute angle θ with tan θ = '+opp+'/'+adj+'. The adjacent leg is '+adj+'. Find the positive opposite leg length x.';}
return make('geo-right-'+kind+'-'+ctx.c,prompt,eq,x,'Use the definition of '+(kind==='sin'?'sine (opposite/hypotenuse)':kind==='cos'?'cosine (adjacent/hypotenuse)':'tangent (opposite/adjacent)')+'.');}
/* Exact-value special triangles with integer missing sides.
   Radical-valued targets are deferred until symbolic radical checks are supported. */
function special45(ctx){
 var r=ctx.rng,c=ctx.c,n=r.int(3,c>=5?35:18),eq='2*x='+(2*n);
 return make('geo-right-45-'+c,
  'A 45°-45°-90° triangle has one leg of length '+n+' units. Find the other leg x. Explain why the two legs are congruent.',
  eq,n,'The legs opposite equal 45° angles are equal.');
}
function special30(ctx){
 var r=ctx.rng,c=ctx.c,n=r.int(3,c>=5?32:16),whole=r.int(0,1)===0;
 var x=whole?2*n:n,eq=whole?'x=2*'+n:'2*x='+(2*n);
 return make('geo-right-30-'+(whole?'hyp-':'short-')+c,
  whole?'A 30°-60°-90° triangle has a short leg opposite 30° of length '+n+' units. Find the hypotenuse x.':
    'A 30°-60°-90° triangle has a hypotenuse of length '+(2*n)+' units. Find the short leg x opposite 30°.',
  eq,x,'In a 30°-60°-90° triangle the hypotenuse is twice the short leg.');
}
function elevation(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?15:8),rise=3*k,run=4*k,x=rise;
 var eq=run+'*x='+rise+'*'+run;
 return make('geo-right-elevation-'+c,
  'A surveyor observes the top of a building at an angle of elevation θ. The horizontal distance is '+run+' feet and tan θ = '+rise+'/'+run+'. Assuming level ground, find the building height x in feet.',
  eq,x,'Angle of elevation uses tangent = vertical rise / horizontal run.');
}
/* Connected Honors investigation using an exact Pythagorean triple. */
function honorsSurvey(ctx){
 var r=ctx.rng,c=ctx.c,t=triples[r.int(0,Math.min(triples.length-1,8))],k=r.int(2,c>=5?8:4);
 var rise=t[0]*k,run=t[1]*k,hyp=t[2]*k;
 var area=rise*run/2,perimeter=rise+run+hyp,shadow=2*run,tree=2*rise;
 var eq1='x^2='+rise+'^2+'+run+'^2';
 var eq2='2*y='+rise+'*'+run;
 var eq3='z='+rise+'+'+run+'+'+hyp;
 var eq4=run+'*w='+rise+'*'+shadow;
 return {variant:'geo-right-honors-survey-'+c,
  fig:{kind:'geo-right-triangle',case:'elevation'},
  prompt:'Honors survey investigation. A right triangle has legs '+rise+' and '+run+' units. A surveyor stands '+run+' feet horizontally from a building whose roof is '+rise+' feet above the surveyor. The line of sight forms that right triangle. A second building is viewed at the same angle of elevation from '+shadow+' feet away on level ground. Show your reasoning for all four parts.',
  parts:[
   {prompt:'(a) Find the direct line-of-sight distance x. Use '+M(eq1)+' to find x.',answer:M('x='+hyp),check:{type:'geo-pythagorean',kind:'hyp',eq:eq1}},
   {prompt:'(b) Find the area y of the first right triangle. Use '+M(eq2)+' to find y.',answer:M('y='+area),check:{type:'solve',eq:eq2,v:'y'}},
   {prompt:'(c) Find the perimeter z of the first right triangle. Use '+M(eq3)+' to find z.',answer:M('z='+perimeter),check:{type:'solve',eq:eq3,v:'z'}},
   {prompt:'(d) Find the height w of the second building, using the equal angle of elevation. Use '+M(eq4)+' to find w.',answer:M('w='+tree),check:{type:'solve',eq:eq4,v:'w'}}
  ],
  steps:[
   step('Use the Pythagorean theorem for line of sight.',M(eq1)),
   step('Area is half the product of the perpendicular legs.',M(eq2)),
   step('Perimeter is the sum of the three side lengths.',M(eq3)),
   step('Equal angles of elevation produce similar triangles.',M(eq4))
  ],space:[2,2.6,3.2]};
}
function inverseTrig(ctx){
 var r=ctx.rng,c=ctx.c,types=['sin','cos','tan'],kind=types[r.int(0,2)];
 var angle=kind==='sin'?30:kind==='cos'?60:45;
 var ratio=kind==='tan'?'1/1':'1/2';
 return {variant:'geo-right-inverse-'+kind+'-'+c,
  fig:{kind:'geo-right-triangle',case:kind},
  prompt:'Find the acute angle x in degrees if '+kind+' x = '+ratio+'. Use an inverse trigonometric function and explain why your answer is acute.',
  parts:[{answer:M('x='+angle),check:{type:'geo-inverse-trig'}}],
  steps:[step('Use the inverse '+kind+' function on the given ratio.',
      M('x='+angle+'^\\circ'))],
  space:[1.3,1.6,2]};
}
/* Calculator-based inverse trig with a stated rounding convention. */
function inverseTrigDecimal(ctx){
 var r=ctx.rng,c=ctx.c,t=triples[r.int(0,c>=5?triples.length-1:7)];
 var kind=['sin','cos','tan'][r.int(0,2)],a=t[0],b=t[1],h=t[2];
 var num=kind==='sin'?a:kind==='cos'?b:a;
 var den=kind==='tan'?b:h;
 var angle=Math[{'sin':'asin','cos':'acos','tan':'atan'}[kind]](num/den)*180/Math.PI;
 var x=(Math.round(angle*10)/10).toFixed(1);
 return {variant:'geo-right-inverse-decimal-'+kind+'-'+c,
  fig:{kind:'geo-right-triangle',case:kind},
  prompt:'Find the acute angle x in degrees if '+kind+' x = '+num+'/'+den+'. Round your answer to the nearest tenth of a degree. Use a calculator in degree mode.',
  parts:[{answer:M('x='+x),check:{type:'geo-inverse-trig',roundTo:1}}],
  steps:[step('Apply inverse '+kind+' in degree mode.',M('x='+x+'^\\circ'))],
  space:[1.3,1.7,2]};
}
function specialRadical(ctx){
 var r=ctx.rng,c=ctx.c,n=r.int(2,c>=5?24:12),is45=r.int(0,1)===0;
 var rad=is45?2:3,answer='x='+n+'\\sqrt{'+rad+'}';
 return {variant:'geo-right-radical-'+(is45?'45':'30')+'-'+c,
 fig:{kind:'geo-right-triangle',case:is45?'45':'30'},
 prompt:is45?'A 45°-45°-90° triangle has a leg of length '+n+' units. Find the hypotenuse x in simplest radical form.':
 'A 30°-60°-90° triangle has a short leg of length '+n+' units. Find the long leg x in simplest radical form.',
 parts:[{answer:M(answer),check:{type:'geo-special-radical'}}],
 steps:[step('Apply the special right triangle side ratio.',M(answer))],space:[1.4,1.7,2]};
}
function depression(ctx){
 var r=ctx.rng,c=ctx.c,k=r.int(2,c>=5?14:8),drop=3*k,horizontal=4*k,eq=horizontal+'*x='+drop+'*'+horizontal;
 return make('geo-right-depression-'+c,
 'From the top of a cliff, an observer looks down at a boat at angle of depression θ. The horizontal distance to the boat is '+horizontal+' feet, and tan θ = '+drop+'/'+horizontal+'. Find the vertical drop x in feet.',
 eq,drop,'Use the tangent ratio for the angle of depression.');
}
NS.registerSkillSet({id:'geometry-right-triangles-trigonometry',course:'geometry',courseName:'Geometry',unit:'right-triangles-trigonometry',unitName:'Right Triangles and Trigonometry',title:'Right Triangles and Trigonometry',
tags:{PYTH:'Pythagorean theorem',DISTANCE:'Distance formula',TRIG:'Trigonometric side ratios',SPECIAL:'45-45-90 and 30-60-90 triangles',APPLICATION:'Angles of elevation and depression',HONORS:'Multistep surveying investigation',INVERSE:'Inverse trigonometric angles and calculator rounding'},
reference:'<div class="mm-refgrid"><section><h4>Pythagorean theorem</h4><p>a² + b² = c² (c is the hypotenuse).</p></section><section><h4>SOH CAH TOA</h4><p>sin = opposite/hypotenuse; cos = adjacent/hypotenuse; tan = opposite/adjacent.</p></section></div>',
gaps:['Starter bank only: non-integer trig answers, and additional non-integer trigonometry applications remain pending.'],
skills:[
{id:'right-pythagorean-hypotenuse',tag:'PYTH',name:'Find hypotenuse',best:[0,1,2],generate:hyp},
{id:'right-pythagorean-leg',tag:'PYTH',name:'Find missing leg',best:[0,1,2],generate:leg},
{id:'right-distance-formula',tag:'DISTANCE',name:'Distance on a coordinate plane',best:[0,1,2],generate:distance},
{id:'right-sine-side',tag:'TRIG',name:'Sine: missing opposite side',best:[0,1,2],generate:ctx=>trig(ctx,'sin')},
{id:'right-cosine-side',tag:'TRIG',name:'Cosine: missing adjacent side',best:[0,1,2],generate:ctx=>trig(ctx,'cos')},
{id:'right-tangent-side',tag:'TRIG',name:'Tangent: missing opposite side',best:[0,1,2],generate:ctx=>trig(ctx,'tan')},
{id:'right-special-45-45-90',tag:'SPECIAL',name:'Equal legs of a 45-45-90 triangle',best:[0,1,2],generate:special45},
{id:'right-special-30-60-90',tag:'SPECIAL',name:'Short leg and hypotenuse of a 30-60-90 triangle',best:[0,1,2],generate:special30},
{id:'right-angle-elevation',tag:'APPLICATION',name:'Angle of elevation and building height',best:[1,2],generate:elevation},
{id:'right-honors-survey',tag:'HONORS',name:'Four-part surveying and similar triangles investigation',best:[2],generate:honorsSurvey},
{id:'right-inverse-trig',tag:'INVERSE',name:'Find an acute angle using inverse trig',best:[1,2],generate:inverseTrig},
{id:'right-inverse-trig-decimal',tag:'INVERSE',name:'Calculator inverse trig rounded to tenths',best:[1,2],generate:inverseTrigDecimal},
{id:'right-special-radical',tag:'SPECIAL',name:'Exact radical sides in special right triangles',best:[1,2],generate:specialRadical},
{id:'right-angle-depression',tag:'APPLICATION',name:'Angle of depression and vertical drop',best:[1,2],generate:depression}
]});
})(typeof window!=='undefined'?window:globalThis);
