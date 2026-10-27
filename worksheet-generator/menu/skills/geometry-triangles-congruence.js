/* Verified text-first Geometry Unit 3 starter bank. No diagram is implied. */
(function(G){'use strict';
var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function corresponding(ctx,kind){
 var r=ctx.rng,c=ctx.c,x=r.int(3,c>=5?30:18),a=c>=5?r.int(2,4):1,b=r.int(1,12),value=a*x+b;
 var eq=(a===1?'x':a+'x')+'+'+b+'='+value;
 var feature=kind==='side'?'corresponding sides':'corresponding angles';
 var unit=kind==='side'?' units':' degrees';
 return {variant:'geo-congruence-'+kind+'-'+c,
 prompt:'Triangles ABC and DEF are congruent, with A corresponding to D, B to E, and C to F. '+(kind==='side'?'AB and DE':'angle B and angle E')+' are '+feature+'. Their measures are '+M((a===1?'x':a+'x')+'+'+b)+' and '+value+unit+'. Find x. Use '+M(eq)+' to find x.',
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
 var r=ctx.rng,c=ctx.c,x=r.int(3,18),a=r.int(2,12),b=r.int(2,12),p=x+a+b,eq='x+'+a+'+'+b+'='+p;
 return {variant:'geo-congruence-perimeter-'+c,prompt:'Triangle ABC is congruent to triangle DEF. The side lengths of ABC are x, '+a+', and '+b+' units. The perimeter of DEF is '+p+' units. Find x.',
 parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
 steps:[step('Congruent triangles have equal perimeters.',M(eq)),step('Solve for the unknown side.',M('x='+x))],space:[1.2,1.5,1.8]};
}
NS.registerSkillSet({id:'geometry-triangles-congruence',course:'geometry',courseName:'Geometry',unit:'triangles-congruence',unitName:'Triangle Congruence',title:'Triangle Congruence Foundations',
 tags:{CPCTC:'Corresponding parts of congruent triangles',THIRD:'Third angle theorem',PERIMETER:'Congruent triangle perimeters'},
 reference:'<div class="mm-refgrid"><section><h4>Correspondence</h4><p>In ABC ≅ DEF, A ↔ D, B ↔ E, and C ↔ F.</p></section><section><h4>CPCTC</h4><p>Corresponding parts of congruent triangles are congruent.</p></section></div>',
 gaps:['Starter bank does not yet assess SSS, SAS, ASA, AAS, HL, invalid SSA/AAA, formal proofs, or diagram-based congruence.'],
 skills:[
 {id:'congruent-corresponding-sides',tag:'CPCTC',name:'Corresponding side lengths',best:[0,1,2],generate:ctx=>corresponding(ctx,'side')},
 {id:'congruent-corresponding-angles',tag:'CPCTC',name:'Corresponding angle measures',best:[0,1,2],generate:ctx=>corresponding(ctx,'angle')},
 {id:'congruent-third-angle',tag:'THIRD',name:'Third angle theorem',best:[0,1,2],generate:thirdAngle},
 {id:'congruent-perimeters',tag:'PERIMETER',name:'Perimeters of congruent triangles',best:[0,1,2],generate:perimeter}
 ]});
})(typeof window!=='undefined'?window:globalThis);
