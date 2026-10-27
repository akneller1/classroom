/* Geometry Unit 10: text-first exact-answer area, surface area and volume. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(id,prompt,eq,x,reason){return {variant:id,prompt:prompt+' Use '+M(eq)+' to find x.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(reason,M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};}
function rect(ctx){var r=ctx.rng,w=r.int(3,14),h=r.int(3,ctx.c>=5?22:14),x=w*h;return make('geo-measure-rectangle-'+ctx.c,'A rectangle has width '+w+' cm and length '+h+' cm. Find its area x in square centimeters.', 'x='+w+'*'+h,x,'Area of a rectangle is length times width.');}
function triangle(ctx){var r=ctx.rng,b=2*r.int(3,13),h=r.int(3,ctx.c>=5?20:13),x=b*h/2;return make('geo-measure-triangle-'+ctx.c,'A triangle has base '+b+' cm and perpendicular height '+h+' cm. Find its area x in square centimeters.','2*x='+b+'*'+h,x,'Area of a triangle is half the base times perpendicular height.');}
function parallelogram(ctx){var r=ctx.rng,b=r.int(4,18),h=r.int(3,15),x=b*h;return make('geo-measure-parallelogram-'+ctx.c,'A parallelogram has base '+b+' m and perpendicular height '+h+' m. Find its area x in square meters.','x='+b+'*'+h,x,'Area of a parallelogram is base times perpendicular height.');}
function trapezoid(ctx){var r=ctx.rng,a=r.int(4,13),b=r.int(4,16),h=2*r.int(2,8),x=(a+b)*h/2;return make('geo-measure-trapezoid-'+ctx.c,'A trapezoid has parallel bases '+a+' and '+b+' cm and perpendicular height '+h+' cm. Find its area x in square centimeters.','2*x=('+a+'+'+b+')*'+h,x,'Area of a trapezoid is one-half the sum of its bases times its height.');}
function prismVolume(ctx){var r=ctx.rng,a=r.int(2,9),b=r.int(3,10),h=r.int(2,ctx.c>=5?13:9),x=a*b*h;return make('geo-measure-prism-volume-'+ctx.c,'A rectangular prism has length '+a+' cm, width '+b+' cm, and height '+h+' cm. Find its volume x in cubic centimeters.','x='+a+'*'+b+'*'+h,x,'Volume is length times width times height.');}
function prismSurface(ctx){var r=ctx.rng,a=r.int(2,8),b=r.int(2,9),h=r.int(2,ctx.c>=5?11:8),x=2*(a*b+a*h+b*h);return make('geo-measure-prism-surface-'+ctx.c,'A closed rectangular prism has dimensions '+a+' cm by '+b+' cm by '+h+' cm. Find its total surface area x in square centimeters.','x=2*('+a+'*'+b+'+'+a+'*'+h+'+'+b+'*'+h+')',x,'Add the areas of all six faces.');}
function cylinderVolume(ctx){var r=ctx.rng,rad=r.int(2,ctx.c>=5?10:7),h=r.int(3,12),x=rad*rad*h;return make('geo-measure-cylinder-volume-'+ctx.c,'A right circular cylinder has radius '+rad+' cm and height '+h+' cm. Its volume is xπ cubic centimeters. Find the coefficient x (do not include π).','x='+rad+'*'+rad+'*'+h,x,'Cylinder volume is πr²h.');}
function cylinderSurface(ctx){var r=ctx.rng,rad=r.int(2,ctx.c>=5?9:6),h=r.int(3,11),x=2*rad*(rad+h);return make('geo-measure-cylinder-surface-'+ctx.c,'A closed right circular cylinder has radius '+rad+' cm and height '+h+' cm. Its total surface area is xπ square centimeters. Find the coefficient x (do not include π).','x=2*'+rad+'*('+rad+'+'+h+')',x,'Total surface area is 2πr² + 2πrh.');}
function pyramid(ctx){var r=ctx.rng,a=r.int(3,9),b=r.int(3,9),h=3*r.int(2,8),x=a*b*h/3;return make('geo-measure-pyramid-'+ctx.c,'A right rectangular pyramid has base dimensions '+a+' cm by '+b+' cm and perpendicular height '+h+' cm. Find its volume x in cubic centimeters.','3*x='+a+'*'+b+'*'+h,x,'Pyramid volume is one-third the base area times the perpendicular height.');}
NS.registerSkillSet({id:'geometry-area-surface-area-volume',course:'geometry',courseName:'Geometry',unit:'area-surface-area-volume',unitName:'Area, Surface Area and Volume',title:'Area, Surface Area and Volume',
tags:{AREA:'Area of plane figures',VOLUME:'Volume of solids',SURFACE:'Surface area of solids',CIRCULAR:'Circular solids'},
reference:'<div class="mm-refgrid"><section><h4>Plane area</h4><p>Rectangle: lw; triangle: bh/2; trapezoid: (b₁+b₂)h/2.</p></section><section><h4>Solids</h4><p>Prism: Bh; pyramid: Bh/3; cylinder: πr²h.</p></section></div>',
gaps:['Starter bank only. Composite figures, cones, spheres, nets, cross-sections, unit conversions, scale factors for area/volume, and diagram-based Honors tasks remain pending.'],
skills:[
{id:'measure-rectangle-area',tag:'AREA',name:'Area of a rectangle',best:[0,1,2],generate:rect},
{id:'measure-triangle-area',tag:'AREA',name:'Area of a triangle',best:[0,1,2],generate:triangle},
{id:'measure-parallelogram-area',tag:'AREA',name:'Area of a parallelogram',best:[0,1,2],generate:parallelogram},
{id:'measure-trapezoid-area',tag:'AREA',name:'Area of a trapezoid',best:[0,1,2],generate:trapezoid},
{id:'measure-prism-volume',tag:'VOLUME',name:'Volume of a rectangular prism',best:[0,1,2],generate:prismVolume},
{id:'measure-prism-surface',tag:'SURFACE',name:'Surface area of a rectangular prism',best:[0,1,2],generate:prismSurface},
{id:'measure-cylinder-volume',tag:'CIRCULAR',name:'Cylinder volume (coefficient of π)',best:[0,1,2],generate:cylinderVolume},
{id:'measure-cylinder-surface',tag:'CIRCULAR',name:'Cylinder surface area (coefficient of π)',best:[0,1,2],generate:cylinderSurface},
{id:'measure-pyramid-volume',tag:'VOLUME',name:'Volume of a rectangular pyramid',best:[0,1,2],generate:pyramid}
]});
})(typeof window!=='undefined'?window:globalThis);
