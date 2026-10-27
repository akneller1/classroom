/* Geometry Unit 6: integer-answer right triangle and trig starter bank. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
var triples=[[3,4,5],[5,12,13],[8,15,17],[7,24,25],[20,21,29],[9,40,41],[12,35,37],[11,60,61],[28,45,53],[16,63,65],[33,56,65],[48,55,73]];
function make(id,prompt,eq,x,reason,kind){return {variant:id,prompt:prompt+' Use '+M(eq)+' to find x.',parts:[{answer:M('x='+x),check:kind?{type:'geo-pythagorean',kind:kind}:{type:'solve',eq:eq,v:'x'}}],steps:[step(reason,M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};}
function triple(ctx){var r=ctx.rng,t=triples[r.int(0,ctx.c>=5?triples.length-1:8)],k=r.int(1,ctx.c>=5?12:8);return t.map(n=>n*k);}
function hyp(ctx){var t=triple(ctx),a=t[0],b=t[1],x=t[2],eq='x^2='+a+'^2+'+b+'^2';return make('geo-right-hyp-'+ctx.c,'A right triangle has legs '+a+' and '+b+' units. Find the positive hypotenuse length x.',eq,x,'Apply the Pythagorean theorem.','hyp');}
function leg(ctx){var t=triple(ctx),a=t[0],x=t[1],h=t[2],eq=a+'^2+x^2='+h+'^2';return make('geo-right-leg-'+ctx.c,'A right triangle has hypotenuse '+h+' units and one leg '+a+' units. Find the positive length x of the other leg.',eq,x,'Apply the Pythagorean theorem and take the positive root.','leg');}
function distance(ctx){var t=triple(ctx),dx=t[0],dy=t[1],x=t[2],eq='x^2='+dx+'^2+'+dy+'^2';return make('geo-right-distance-'+ctx.c,'Points A(0, 0) and B('+dx+', '+dy+') lie on a coordinate plane. Find the positive distance x between them.',eq,x,'Use the distance formula (Pythagorean theorem).','distance');}
function trig(ctx,kind){var t=triple(ctx),opp=t[0],adj=t[1],hyp=t[2],x,eq,prompt;
if(kind==='sin'){x=opp;eq=hyp+'*x='+opp+'*'+hyp;prompt='A right triangle has hypotenuse '+hyp+' and an acute angle θ with sin θ = '+opp+'/'+hyp+'. Find the positive length x of the side opposite θ.';}
else if(kind==='cos'){x=adj;eq=hyp+'*x='+adj+'*'+hyp;prompt='A right triangle has hypotenuse '+hyp+' and an acute angle θ with cos θ = '+adj+'/'+hyp+'. Find the positive length x of the side adjacent to θ.';}
else{x=opp;eq=adj+'*x='+opp+'*'+adj;prompt='A right triangle has an acute angle θ with tan θ = '+opp+'/'+adj+'. The adjacent leg is '+adj+'. Find the positive opposite leg length x.';}
return make('geo-right-'+kind+'-'+ctx.c,prompt,eq,x,'Use the definition of '+(kind==='sin'?'sine (opposite/hypotenuse)':kind==='cos'?'cosine (adjacent/hypotenuse)':'tangent (opposite/adjacent)')+'.');}
NS.registerSkillSet({id:'geometry-right-triangles-trigonometry',course:'geometry',courseName:'Geometry',unit:'right-triangles-trigonometry',unitName:'Right Triangles and Trigonometry',title:'Right Triangles and Trigonometry',
tags:{PYTH:'Pythagorean theorem',DISTANCE:'Distance formula',TRIG:'Trigonometric side ratios'},
reference:'<div class="mm-refgrid"><section><h4>Pythagorean theorem</h4><p>a² + b² = c² (c is the hypotenuse).</p></section><section><h4>SOH CAH TOA</h4><p>sin = opposite/hypotenuse; cos = adjacent/hypotenuse; tan = opposite/adjacent.</p></section></div>',
gaps:['Starter bank only: special right triangles, inverse trig, angle of elevation/depression, non-integer trig answers, diagrams, and multistep Honors applications remain pending.'],
skills:[
{id:'right-pythagorean-hypotenuse',tag:'PYTH',name:'Find hypotenuse',best:[0,1,2],generate:hyp},
{id:'right-pythagorean-leg',tag:'PYTH',name:'Find missing leg',best:[0,1,2],generate:leg},
{id:'right-distance-formula',tag:'DISTANCE',name:'Distance on a coordinate plane',best:[0,1,2],generate:distance},
{id:'right-sine-side',tag:'TRIG',name:'Sine: missing opposite side',best:[0,1,2],generate:ctx=>trig(ctx,'sin')},
{id:'right-cosine-side',tag:'TRIG',name:'Cosine: missing adjacent side',best:[0,1,2],generate:ctx=>trig(ctx,'cos')},
{id:'right-tangent-side',tag:'TRIG',name:'Tangent: missing opposite side',best:[0,1,2],generate:ctx=>trig(ctx,'tan')}
]});
})(typeof window!=='undefined'?window:globalThis);
