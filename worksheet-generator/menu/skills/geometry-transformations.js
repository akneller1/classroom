/* Geometry Unit 8: coordinate transformations, text-first verified starter bank. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function make(id,prompt,eq,x,reason){return {variant:id,prompt:prompt+' Use '+M(eq)+' to find x.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(reason,M(eq)),step('Solve for x.',M('x='+x))],space:[1.2,1.5,1.8]};}
function nz(r){var n=r.int(-9,9);return n===0?4:n;}
function reflect(ctx,axis){var r=ctx.rng,a=nz(r),b=nz(r),x=axis==='x'?-b:-a,eq='x'+((axis==='x'?b:a)>=0?'+':'')+(axis==='x'?b:a)+'=0';
return make('geo-transform-reflect-'+axis+'-'+ctx.c,'Point P('+a+', '+b+') is reflected across the '+axis+'-axis. Find '+(axis==='x'?'the y-coordinate':'the x-coordinate')+' x of the image P′.',eq,x,'Reflection across the '+axis+'-axis changes the sign of the '+(axis==='x'?'y':'x')+'-coordinate.');}
function translate(ctx,axis){var r=ctx.rng,a=nz(r),b=nz(r),shift=nz(r),x=(axis==='x'?a:b)+shift,eq='x'+(shift>=0?'-':'+')+Math.abs(shift)+'='+(axis==='x'?a:b);
return make('geo-transform-translate-'+axis+'-'+ctx.c,'Point P('+a+', '+b+') is translated '+Math.abs(shift)+' units '+(axis==='x'?(shift>0?'right':'left'):(shift>0?'up':'down'))+'. Find the '+(axis==='x'?'x':'y')+'-coordinate x of P′.',eq,x,'A translation adds the signed displacement to the selected coordinate.');}
function rotate(ctx,dir){var r=ctx.rng,a=nz(r),b=nz(r),x=dir==='cw'?b:-b,eq='x'+((dir==='cw'?-b:b)>=0?'+':'')+(dir==='cw'?-b:b)+'=0';
return make('geo-transform-rotate-'+dir+'-'+ctx.c,'Point P('+a+', '+b+') is rotated 90° '+(dir==='cw'?'clockwise':'counterclockwise')+' about the origin. Find the x-coordinate x of P′.',eq,x,'A 90° rotation maps (a,b) to '+(dir==='cw'?'(b,−a).':'(−b,a).'));}
function dilate(ctx){var r=ctx.rng,a=nz(r),b=nz(r),k=r.int(2,ctx.c>=5?5:3),x=k*a,eq='x='+k+'*'+a;
return make('geo-transform-dilate-'+ctx.c,'Point P('+a+', '+b+') is dilated about the origin by a scale factor of '+k+'. Find the x-coordinate x of P′.',eq,x,'Multiply each coordinate by the scale factor.');}
NS.registerSkillSet({id:'geometry-transformations',course:'geometry',courseName:'Geometry',unit:'transformations',unitName:'Transformations',title:'Coordinate Transformations',
tags:{REFLECTION:'Reflections',TRANSLATION:'Translations',ROTATION:'Rotations',DILATION:'Dilations'},
reference:'<div class="mm-refgrid"><section><h4>Reflections</h4><p>x-axis: (x,y) → (x,−y); y-axis: (x,y) → (−x,y).</p></section><section><h4>90° rotations</h4><p>Clockwise: (x,y) → (y,−x); counterclockwise: (x,y) → (−y,x).</p></section></div>',
gaps:['Starter bank only. Full ordered-pair responses, graphing figures, composition of transformations, rigid-motion proofs, symmetry, and diagram-based items remain pending.'],
skills:[
{id:'reflect-x-axis',tag:'REFLECTION',name:'Reflect over x-axis',best:[0,1,2],generate:ctx=>reflect(ctx,'x')},
{id:'reflect-y-axis',tag:'REFLECTION',name:'Reflect over y-axis',best:[0,1,2],generate:ctx=>reflect(ctx,'y')},
{id:'translate-horizontal',tag:'TRANSLATION',name:'Horizontal translation',best:[0,1,2],generate:ctx=>translate(ctx,'x')},
{id:'translate-vertical',tag:'TRANSLATION',name:'Vertical translation',best:[0,1,2],generate:ctx=>translate(ctx,'y')},
{id:'rotate-90-clockwise',tag:'ROTATION',name:'90° clockwise rotation',best:[0,1,2],generate:ctx=>rotate(ctx,'cw')},
{id:'rotate-90-counterclockwise',tag:'ROTATION',name:'90° counterclockwise rotation',best:[0,1,2],generate:ctx=>rotate(ctx,'ccw')},
{id:'dilate-origin',tag:'DILATION',name:'Dilation about origin',best:[0,1,2],generate:dilate}
]});
})(typeof window!=='undefined'?window:globalThis);
