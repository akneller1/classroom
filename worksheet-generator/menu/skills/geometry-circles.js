/* Geometry Unit 9: exact-answer, text-first circle relationships. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(id,prompt,eq,x,reason){return {variant:id,prompt:prompt+' Set up and solve an equation for x.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(reason,M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};}
function central(ctx){var r=ctx.rng,a=r.int(25,ctx.c>=5?170:140);return make('geo-circle-central-'+ctx.c,'A minor arc is intercepted by a central angle measuring '+a+'°. Find the measure x of the arc, in degrees.','x='+a,a,'A minor arc has the same measure as its central angle.');}
function inscribed(ctx){var r=ctx.rng,x=r.int(15,ctx.c>=5?85:65),arc=2*x;return make('geo-circle-inscribed-'+ctx.c,'An inscribed angle intercepts an arc measuring '+arc+'°. Find the inscribed angle measure x in degrees.','2*x='+arc,x,'An inscribed angle measures half its intercepted arc.');}
function intercepted(ctx){var r=ctx.rng,a=r.int(15,75),x=2*a;return make('geo-circle-intercepted-'+ctx.c,'An inscribed angle measures '+a+'°. Find the measure x, in degrees, of its intercepted arc.','x=2*'+a,x,'An intercepted arc has twice the measure of its inscribed angle.');}
function tangent(ctx){var r=ctx.rng,a=r.int(12,72),x=90-a;return make('geo-circle-tangent-'+ctx.c,'At a point of tangency T, radius OT is perpendicular to a tangent. A ray inside the right angle makes '+a+'° with OT. Find its angle x with the tangent.','x+'+a+'=90',x,'The two adjacent angles form a right angle.');}
function diameter(ctx){var r=ctx.rng,x=r.int(3,ctx.c>=5?85:75);return make('geo-circle-diameter-'+ctx.c,'A circle has radius '+x+' cm. Find its diameter, in centimeters.','x=2*'+x,2*x,'Diameter is twice the radius.');}
function radius(ctx){var r=ctx.rng,x=r.int(3,ctx.c>=5?85:75),d=2*x;return make('geo-circle-radius-'+ctx.c,'A circle has diameter '+d+' cm. Find its radius, in centimeters.','2*x='+d,x,'Radius is half the diameter.');}
function chord(ctx){var r=ctx.rng,a=r.int(12,75),x=90-a;return make('geo-circle-semicircle-'+ctx.c,'Triangle ABC is inscribed in a circle, and AB is a diameter. Angle A measures '+a+'°. Find angle B, called x, in degrees.','x+'+a+'=90',x,'Angle C is 90° because it subtends a diameter; the two remaining angles total 90°.');}

function intersectingChords(ctx){var r=ctx.rng,c=ctx.c,a=r.int(2,c>=5?9:6),factor=r.int(2,7),b=a*factor,other=r.int(4,c>=5?65:45),answer=factor*other;return make('geo-circle-intersecting-chords-'+c,'Two chords AB and CD intersect inside a circle at P. PA measures '+a+' cm, PB measures x cm, PC measures '+b+' cm, and PD measures '+other+' cm. Find x using the intersecting chords theorem.',a+'*x='+b+'*'+other,answer,'For two intersecting chords, PA times PB equals PC times PD.');}
function twoSecants(ctx){var r=ctx.rng,c=ctx.c,a=r.int(2,c>=5?9:6),factor=r.int(2,7),b=a*factor,wholeB=r.int(b+3,b+(c>=5?80:55)),wholeA=factor*wholeB;return make('geo-circle-two-secants-'+c,'Two secants are drawn from the same exterior point P. On the first secant, the external segment measures '+a+' cm and the entire secant measures x cm. On the second secant, the external segment measures '+b+' cm and the entire secant measures '+wholeB+' cm. Find x using the secant-secant theorem.',a+'*x='+b+'*'+wholeB,wholeA,'For two secants from one exterior point, external length times whole secant length is equal for both secants.');}
NS.registerSkillSet({id:'geometry-circles',course:'geometry',courseName:'Geometry',unit:'circles',unitName:'Circles',title:'Circle Relationships',
tags:{CENTRAL:'Central angles and arcs',INSCRIBED:'Inscribed angles',TANGENT:'Tangents and radii',MEASURE:'Radius and diameter',SEMICIRCLE:'Angles in a semicircle',CHORDS:'Intersecting chord products',SECANTS:'Two-secant power theorem'},
reference:'<div class="mm-refgrid"><section><h4>Arcs and angles</h4><p>A central angle equals its intercepted minor arc; an inscribed angle is half its intercepted arc.</p></section><section><h4>Tangents</h4><p>A tangent is perpendicular to the radius at the point of tangency.</p></section></div>',
gaps:['Intersecting chord products and two-secant products added. Circle equations, chord distance properties, tangent-secant applications, arc lengths, sectors, and all diagrams remain pending.'],
skills:[
{id:'circle-central-arc',tag:'CENTRAL',name:'Central angle and minor arc',best:[0,1,2],generate:central},
{id:'circle-inscribed-angle',tag:'INSCRIBED',name:'Inscribed angle from arc',best:[0,1,2],generate:inscribed},
{id:'circle-intercepted-arc',tag:'INSCRIBED',name:'Intercepted arc from inscribed angle',best:[0,1,2],generate:intercepted},
{id:'circle-tangent-radius',tag:'TANGENT',name:'Radius and tangent angle',best:[0,1,2],generate:tangent},
{id:'circle-diameter',tag:'MEASURE',name:'Diameter from radius',best:[0,1,2],generate:diameter},
{id:'circle-radius',tag:'MEASURE',name:'Radius from diameter',best:[0,1,2],generate:radius},
{id:'circle-semicircle-angle',tag:'SEMICIRCLE',name:'Angle inscribed in a semicircle',best:[0,1,2],generate:chord},
{id:'circle-intersecting-chords',tag:'CHORDS',name:'Intersecting chord segment products',best:[0,1,2],generate:intersectingChords},
{id:'circle-two-secants',tag:'SECANTS',name:'Two secants from an exterior point',best:[0,1,2],generate:twoSecants}
]});
})(typeof window!=='undefined'?window:globalThis);
