/* Geometry Unit 9: exact-answer, text-first circle relationships. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
function fig(spec){var F=NS.geoFigures;return spec&&F&&F.check(spec).ok?spec:undefined}
var CF=function(){return NS.geoFigures&&NS.geoFigures.circ};
/* Same as make() with a named unknown (r for a radius, h for a center coordinate, s for r²), so the circle's own x and y stay the coordinate variables. */
function makeV(id,prompt,v,eq,val,reason){return {variant:id,prompt:prompt,parts:[{answer:M(v+'='+val),check:{type:'solve',eq:eq,v:v}}],steps:[step(reason,M(eq)),step('Solve.',M(v+'='+val))],space:[1.2,1.5,1.8]};}
function make(id,prompt,eq,x,reason,f){return {fig:fig(f),variant:id,prompt:prompt+(/^geo-circle-(diameter|radius)-/.test(id)?'':' Set up and solve an equation for x.'),parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[step(reason,M(eq)),step('Solve.',M('x='+x))],space:[1.2,1.5,1.8]};}
function central(ctx){var r=ctx.rng,c=ctx.c,a=r.int(25,c>=5?170:140);if(c>=5){var x=r.int(8,70),offset=r.int(5,30),angle=2*x+offset;return make('geo-circle-central-expression-'+c,'A minor arc has measure (2x+'+offset+') degrees, and its central angle measures '+angle+' degrees. Find x and explain why the two measures are equal.','2*x+'+offset+'='+angle,x,'A central angle equals the measure of its intercepted minor arc, so set the algebraic arc expression equal to the given central angle.',CF().central(angle,angle+'°','(2x+'+offset+')°'));}return make('geo-circle-central-'+c,'A minor arc is intercepted by a central angle measuring '+a+'°. Find the measure x of the arc, in degrees.','x='+a,a,'A minor arc has the same measure as its central angle.',CF().central(a,a+'°','x°'));}
function inscribed(ctx){var r=ctx.rng,c=ctx.c,x=r.int(15,c>=5?85:65),arc=2*x;if(c>=5){var offset=r.int(2,Math.min(20,x-1));return make('geo-circle-inscribed-expression-'+c,'An inscribed angle has measure (x+'+offset+') degrees and intercepts an arc measuring '+arc+' degrees. Find x, the unknown part of the angle expression. Explain why the intercepted arc is twice the entire inscribed angle.', '2*(x+'+offset+')='+arc,x-offset,'Double the entire angle expression and set it equal to the intercepted arc measure.',CF().inscribed(arc,'(x+'+offset+')°',arc+'°'));}return make('geo-circle-inscribed-'+c,'An inscribed angle intercepts an arc measuring '+arc+'°. Find the inscribed angle measure x in degrees.','2*x='+arc,x,'An inscribed angle measures half its intercepted arc.',CF().inscribed(arc,'x°',arc+'°'));}
function intercepted(ctx){var r=ctx.rng,c=ctx.c,a=r.int(15,75),x=2*a;if(c>=5){var offset=2*r.int(2,12),arc=2*a;return make('geo-circle-intercepted-expression-'+c,'An inscribed angle measures '+a+' degrees. Its intercepted arc is labeled (2x+'+offset+') degrees. Find x, the unknown part of the arc expression. Explain why the entire arc measure is twice the inscribed angle.','2*x+'+offset+'='+arc,(arc-offset)/2,'The intercepted arc measures twice the inscribed angle, so equate the full arc expression to '+arc+' degrees.',CF().inscribed(arc,a+'°','(2x+'+offset+')°'));}return make('geo-circle-intercepted-'+c,'An inscribed angle measures '+a+'°. Find the measure x, in degrees, of its intercepted arc.','x=2*'+a,x,'An intercepted arc has twice the measure of its inscribed angle.',CF().inscribed(2*a,a+'°','x°'));}
function tangent(ctx){var r=ctx.rng,a=r.int(12,72),x=90-a;return make('geo-circle-tangent-'+ctx.c,'At a point of tangency T, radius OT is perpendicular to a tangent. A ray inside the right angle makes '+a+'° with OT. Find its angle x with the tangent.','x+'+a+'=90',x,'The two adjacent angles form a right angle.',CF().tangentRadius(a,a+'°','x°'));}
function diameter(ctx){var r=ctx.rng,x=r.int(3,ctx.c>=5?85:75);if(ctx.c>=5&&r.next()<0.6){var cc=2*x;return make('geo-circle-diameter-circ-'+ctx.c,'A circle has circumference '+cc+'π cm. Find its diameter x, in centimeters.','x='+cc,cc,'Circumference is π times the diameter, so the diameter is the circumference divided by π.',CF().diameter('','x',false));}return make('geo-circle-diameter-'+ctx.c,'A circle has radius '+x+' cm. Find its diameter x, in centimeters.','x=2*'+x,2*x,'Diameter is twice the radius.',CF().diameter(x+' cm','x',true));}
function radius(ctx){var r=ctx.rng,x=r.int(3,ctx.c>=5?85:75),d=2*x;if(ctx.c>=5&&r.next()<0.6)return make('geo-circle-radius-circ-'+ctx.c,'A circle has circumference '+d+'π cm. Find its radius x, in centimeters.','2*x='+d,x,'Circumference is 2πr: divide out π, then divide by 2.',CF().diameter('x','',true));return make('geo-circle-radius-'+ctx.c,'A circle has diameter '+d+' cm. Find its radius x, in centimeters.','2*x='+d,x,'Radius is half the diameter.',CF().diameter('x',d+' cm',false));}
function chord(ctx){var r=ctx.rng,a=r.int(22,68),x=90-a;return make('geo-circle-semicircle-'+ctx.c,'Triangle ABC is inscribed in a circle, and AB is a diameter. Angle A measures '+a+'°. Find angle B, called x, in degrees.','x+'+a+'=90',x,'Angle C is 90° because it subtends a diameter; the two remaining angles total 90°.',CF().semicircle(a,a+'°','x°'));}

function intersectingChords(ctx){var r=ctx.rng,c=ctx.c,a=r.int(2,c>=5?9:6),factor=r.int(2,c>=5?4:3),b=a*factor,other=r.int(a+1,a*(c>=5?4:3)+2),answer=factor*other;   /* both chords within a factor of 3 of each other (2026-11-17) */
 K.need((a+answer)/(b+other)<=3&&(b+other)/(a+answer)<=3);if(c>=5){var shift=r.int(2,Math.min(answer-1,20)),unknown=answer-shift;return make('geo-circle-intersecting-chords-expression-'+c,'Two chords AB and CD intersect inside a circle at P. PA measures '+a+' cm, PB measures (x+'+shift+') cm, PC measures '+b+' cm, and PD measures '+other+' cm. Find x using the intersecting chords theorem. Explain why the entire PB segment is x+'+shift+'.',a+'*(x+'+shift+')='+b+'*'+other,unknown,'Multiply the two segments of each chord. PB is x+'+shift+', so '+a+'(x+'+shift+')='+b+'·'+other+'.',CF().chords({PA:String(a),PB:'(x+'+shift+')',PC:String(b),PD:String(other)},{PA:a,PB:answer,PC:b,PD:other}));}return make('geo-circle-intersecting-chords-'+c,'Two chords AB and CD intersect inside a circle at P. PA measures '+a+' cm, PB measures x cm, PC measures '+b+' cm, and PD measures '+other+' cm. Find x using the intersecting chords theorem.',a+'*x='+b+'*'+other,answer,'For two intersecting chords, PA times PB equals PC times PD.',CF().chords({PA:String(a),PB:'x',PC:String(b),PD:String(other)},{PA:a,PB:answer,PC:b,PD:other}));}
function gcd(x,y){while(y){var t=y;y=x%y;x=t;}return x;}
function twoSecants(ctx){var r=ctx.rng,c=ctx.c,a,b,wholeA,wholeB,ok=false;for(var tries=0;tries<200&&!ok;tries++){a=r.int(2,c>=5?12:8);b=r.int(a+1,2*a);var L=a*b/gcd(a,b),ks=[];for(var k=1;L*k<=8*a*a;k++)if(L*k>=b*(b+2))ks.push(k);if(!ks.length)continue;var pw=L*ks[r.int(0,ks.length-1)];wholeA=pw/a;wholeB=pw/b;ok=true;}if(!ok){a=4;b=6;wholeA=24;wholeB=16;}if(c>=5){var insideB=wholeB-b,insideA=wholeA-a;return make('geo-circle-two-secants-inside-'+c,'Two secants start at exterior point P. On the first secant, the external segment measures '+a+' cm and the segment inside the circle measures x cm. On the second secant, the external segment measures '+b+' cm and the segment inside the circle measures '+insideB+' cm. Find x, the internal segment of the first secant. Explain why each whole secant includes its external segment.',a+'*(x+'+a+')='+b+'*('+b+'+'+insideB+')',insideA,'For each secant, multiply the external segment by the entire secant: external plus internal.',CF().secants({ext1:String(a),ext2:String(b),in1:'x',in2:String(insideB)},{ext1:a,whole1:wholeA,ext2:b,whole2:wholeB}));}return make('geo-circle-two-secants-'+c,'Two secants are drawn from the same exterior point P. On the first secant, the external segment measures '+a+' cm and the entire secant measures x cm. On the second secant, the external segment measures '+b+' cm and the entire secant measures '+wholeB+' cm. Find x using the secant-secant theorem.',a+'*x='+b+'*'+wholeB,wholeA,'For two secants from one exterior point, external length times whole secant length is equal for both secants.',CF().secants({ext1:String(a),ext2:String(b),whole1:'x',whole2:String(wholeB)},{ext1:a,whole1:wholeA,ext2:b,whole2:wholeB}));}
function tangentSecant(ctx){var r=ctx.rng,c=ctx.c,external,tangent,whole,ok=false;for(var tries=0;tries<200&&!ok;tries++){external=r.int(3,c>=5?30:20);tangent=r.int(external+1,Math.floor(2.8*external));if(tangent*tangent%external)continue;whole=tangent*tangent/external;ok=whole-external>=2;}if(!ok){external=4;tangent=6;whole=9;}if(c>=5){var inside=whole-external;return make('geo-circle-tangent-secant-inside-'+c,'From exterior point P, a tangent PT has length '+tangent+' cm. A secant from P has an external segment of '+external+' cm and an internal segment of x cm. Find x, the segment inside the circle. Explain why the whole secant is x plus its external segment.',external+'*(x+'+external+')='+tangent+'*'+tangent,inside,'The tangent length squared equals external secant times the entire secant, which is the external segment plus x.',CF().tangentSecant({tan:String(tangent),ext:String(external),inside:'x'},{tan:tangent,ext:external,whole:whole}));}return make('geo-circle-tangent-secant-'+c,'From exterior point P, a tangent PT has length '+tangent+' cm. A secant from P has an external segment of '+external+' cm and a total length of x cm. Find x using the tangent-secant theorem. Explain why x represents the whole secant, not just the segment inside the circle.',external+'*x='+tangent+'*'+tangent,whole,'The tangent length squared equals the external secant length multiplied by the entire secant length.',CF().tangentSecant({tan:String(tangent),ext:String(external),whole:'x'},{tan:tangent,ext:external,whole:whole}));}

function arcLength(ctx){var r=ctx.rng,c=ctx.c,parts=[2,3,4,5,6,8,9,10,12],k=parts[r.int(0,parts.length-1)],angle=360/k,radius=k*r.int(2,c>=5?45:32),x=2*radius/k;if(c>=5){return make('geo-circle-arc-length-inverse-'+c,'A circle has radius '+radius+' cm. An arc has exact length '+x+' times pi centimeters. Find x, the central angle in degrees, without rounding. Explain how the fraction of the circumference determines the angle.', '2*'+radius+'*x=360*'+x,angle,'Arc length divided by circumference equals the central angle divided by 360 degrees. Cancel pi and solve for the central angle.',CF().sector(angle,'x°',radius+' cm',x+'π','arc'));}return make('geo-circle-arc-length-'+c,'A circle has radius '+radius+' cm. An arc has central angle '+angle+'°. The exact arc length is x times pi centimeters. Find x without rounding.', '360*x=2*'+radius+'*'+angle,x,'Arc length is (central angle / 360) times the circumference 2 pi r. Divide out pi to find its coefficient.',CF().sector(angle,angle+'°',radius+' cm','xπ','arc'));}
function sectorArea(ctx){var r=ctx.rng,c=ctx.c,parts=[2,3,4,5,6,8,9,10,12],k=parts[r.int(0,parts.length-1)],angle=360/k,radius=k*r.int(2,c>=5?36:28),x=radius*radius/k;if(c>=5){return make('geo-circle-sector-area-inverse-'+c,'A circle has radius '+radius+' cm. A sector has exact area '+x+' times pi square centimeters. Find x, its central angle in degrees, without rounding. Explain why the area fraction equals the angle fraction.', radius+'*'+radius+'*x=360*'+x,angle,'Divide sector area by full circle area, cancel pi, and multiply by 360 degrees.',CF().sector(angle,'x°',radius+' cm',x+'π','inside'));}return make('geo-circle-sector-area-'+c,'A circle has radius '+radius+' cm. A sector has central angle '+angle+'°. The exact sector area is x times pi square centimeters. Find x without rounding.', '360*x='+radius+'*'+radius+'*'+angle,x,'Sector area is (central angle / 360) times the circle area pi r squared. Divide out pi to find its coefficient.',CF().sector(angle,angle+'°',radius+' cm','xπ','inside'));}
function circleRadiusSquared(ctx){var r=ctx.rng,c=ctx.c,h=r.int(-15,15),k=r.int(-15,15),dx=r.int(3,c>=5?25:18),dy=r.int(4,c>=5?26:19),sx=r.int(0,1)?1:-1,sy=r.int(0,1)?1:-1,px=h+sx*dx,py=k+sy*dy,answer=dx*dx+dy*dy;
return makeV('geo-circle-coordinate-radius-squared-'+c,'A circle has center ('+h+', '+k+') and passes through point ('+px+', '+py+'). Its equation in standard form is (x − h)² + (y − k)² = r². Find s = r², the radius squared. Show how the distance formula gives it.','s','s='+dx+'*'+dx+'+'+dy+'*'+dy,answer,'The radius squared is the sum of the squared horizontal and vertical distances between the center and the point.');}
function chordLengthFromDistance(ctx){var r=ctx.rng,c=ctx.c,triples=[[3,4,5],[5,12,13],[8,15,17],[7,24,25],[20,21,29],[9,40,41],[12,35,37],[11,60,61],[16,63,65]],t=triples[r.int(0,triples.length-1)],scale=r.int(1,c>=5?8:6),distance=t[0]*scale,half=t[1]*scale,radius=t[2]*scale,whole=2*half;
if(c>=5){return make('geo-circle-chord-distance-inverse-'+c,'A circle has radius '+radius+' cm and a chord of length '+whole+' cm. Find x, the perpendicular distance from the center to the chord in centimeters. Explain why the half-chord forms a right triangle with the radius.', 'x='+distance,distance,'The perpendicular bisects the chord, so half the chord is '+half+' cm. Apply Pythagoras and take the positive square root.',CF().chordDistance(distance/radius,radius+' cm','x',whole+' cm'));}return make('geo-circle-chord-distance-'+c,'A circle has radius '+radius+' cm. The perpendicular distance from the center to a chord is '+distance+' cm. Find x, the entire length of the chord in centimeters. Explain why the perpendicular from the center bisects the chord.', 'x=2*'+half,whole,'The perpendicular from the center bisects the chord. Apply the Pythagorean theorem: half the chord is '+half+' cm, then double it.',CF().chordDistance(distance/radius,radius+' cm',distance+' cm','x'));}

function centerFromExpandedEquation(ctx){var r=ctx.rng,c=ctx.c,h=r.int(3,c>=5?70:48),k=r.int(3,c>=5?55:40),radius=r.int(3,c>=5?32:24),constant=h*h+k*k-radius*radius,sign=constant<0?' - ':' + ',eqText='x^2 - '+2*h+'x + y^2 - '+2*k+'y'+sign+Math.abs(constant)+' = 0';
return makeV('geo-circle-expanded-center-'+c,'A circle has equation '+eqText+'. The center is (h, k). Complete the square in x to find h.','h','2*h='+2*h,h,'The coefficient of x is −2h, so h is half of '+2*h+'. Completing the square gives (x − '+h+')².');}

function radiusFromExpandedEquation(ctx){var r=ctx.rng,c=ctx.c,h=r.int(3,c>=5?45:35),k=r.int(3,c>=5?45:35),radius=r.int(3,c>=5?65:48),constant=h*h+k*k-radius*radius,sign=constant<0?' - ':' + ',eqText='x^2 - '+2*h+'x + y^2 - '+2*k+'y'+sign+Math.abs(constant)+' = 0',square=radius*radius;
if(c>=5){var mixedConstant=h*h+k*k-radius*radius,mixedSign=mixedConstant<0?' - ':' + ',mixedEq='x^2 + '+2*h+'x + y^2 - '+2*k+'y'+mixedSign+Math.abs(mixedConstant)+' = 0';return makeV('geo-circle-expanded-radius-mixed-'+c,'A circle has equation '+mixedEq+'. Complete the square in both variables. Find the radius r, and explain why the x-coordinate of the center is negative.','r','r='+radius,radius,'Completing the square gives (x + '+h+')² + (y − '+k+')² = '+square+'. The center is (−'+h+', '+k+') and the radius is '+radius+'.');}return makeV('geo-circle-expanded-radius-'+c,'A circle has equation '+eqText+'. Complete the square in x and y. Find the radius r (not the radius squared).','r','r='+radius,radius,'Completing the square gives (x − '+h+')² + (y − '+k+')² = '+square+'. The radius is the positive square root, '+radius+'.');}
function four(id,c,intro,rows){return {variant:id+'-'+c,prompt:intro,parts:rows.map(function(p,i){return {label:'abcd'[i],prompt:p[0],answer:M(p[1]+'='+p[2]),check:{type:'solve',eq:p[3],v:p[1]}};}),steps:rows.map(function(p){return step(p[4],M(p[3]));}),space:[2.6,3.2,3.9]};}

function circleInvestigation(ctx){var r=ctx.rng,c=ctx.c,m=r.int(20,c>=5?80:60),arc=2*m,major=360-arc,pa=r.int(3,c>=5?12:9),pb=r.int(3,c>=5?12:9),pc=r.int(2,8),pd=pa*pb/pc;
 while(pa*pb%pc||pd===pa||pd===pb){pa=r.int(3,12);pb=r.int(3,12);pc=r.int(2,8);pd=pa*pb/pc;}
 var t,d;do{t=r.int(4,c>=5?18:12);d=[];for(var k=2;k<t;k++)if(t*t%k===0)d.push(k);}while(!d.length);var a=d[r.int(0,d.length-1)],sec=t*t/a;
 var o6=four('geo-circles-investigation',c,'Open Response: Investigate arcs, chords, and tangents. Use the figure for part (c) and show the theorem you use in every part.',[
 ['An inscribed angle in the circle measures '+m+' degrees. Find the measure x, in degrees, of the arc it intercepts.','x',arc,'x=2*'+m,'An inscribed angle is half its intercepted arc.'],
 ['The arc from (a) is a minor arc. Find the measure y of the matching major arc.','y',major,'y+'+arc+'=360','A circle has 360 degrees of arc.'],
 ['In the figure, chords AB and CD intersect at P. PA = '+pa+', PB = '+pb+', PC = '+pc+', and PD = z. Find z.','z',pd,pc+'*z='+pa+'*'+pb,'Products of the segments of intersecting chords are equal.'],
 ['From an outside point, a tangent segment has length '+t+'. The secant from the same point has an outside part of '+a+'. Find the length w of the whole secant.','w',sec,'w*'+a+'='+t+'*'+t,'The tangent squared equals the outside part times the whole secant.']]);o6.fig=fig(CF().chords({PA:String(pa),PB:String(pb),PC:String(pc),PD:'z'},{PA:pa,PB:pb,PC:pc,PD:pd}));return o6;}

function pn(n){return n<0?'(0-'+(-n)+')':String(n);}
function mn(n){return String(n).replace('-','−');}
function divisors(n,lo,hi){var d=[];for(var k=lo;k<=hi;k++)if(n%k===0)d.push(k);return d;}
/* Honors chain 1: inscribed angle and arc written as expressions, then major arc and tangent-chord angle. */
function invAngles(ctx){var r=ctx.rng,c=ctx.c,m=r.int(3,4),x=r.int(15,45),a=r.int(2,Math.max(2,Math.floor(x/2)-1)),b=m*x-2*(x+a),arc=2*(x+a);
 while(b<2||b>60){x=r.int(15,45);a=r.int(2,Math.max(2,Math.floor(x/2)-1));b=m*x-2*(x+a);arc=2*(x+a);}
 var major=360-arc,tc=arc/2;
 var o=four('geo-circles-investigation-angles',c,'Open Response: An inscribed angle measures (x + '+a+')° and intercepts an arc measuring ('+m+'x − '+b+')°. Each part uses the answer before it.',[
 ['An inscribed angle is half its intercepted arc, so twice the angle equals the arc. Find x.','x',x,'2*(x+'+a+')='+m+'*x-'+b,'Twice the inscribed angle equals the intercepted arc.'],
 ['Use the value of x from part a to find the measure y of the intercepted arc, in degrees.','y',arc,'y='+m+'*'+pn(x)+'-'+b,'Substitute x into the arc expression.'],
 ['Find the measure w of the major arc that completes the circle.','w',major,'w+'+arc+'=360','A circle has 360 degrees of arc.'],
 ['A tangent and a chord meet at a point on the circle and intercept the minor arc from part b. A tangent-chord angle is half its intercepted arc. Find the angle z.','z',tc,'2*z='+arc,'A tangent-chord angle is half its intercepted arc.']]);
 o.fig=fig(CF().inscribed(arc,'(x+'+a+')°','('+m+'x−'+b+')°'));return o;}
/* Honors chain 2: intersecting chords, the chord length reused as a tangent, then tangent-secant and a second secant. */
function invPower(ctx){var r=ctx.rng,c=ctx.c,t,a,pb,b,cc,k,x,e,f,ok=false;
 for(var tries=0;tries<400&&!ok;tries++){t=r.int(9,c>=5?24:18);a=r.int(3,t-4);pb=t-a;var prod=a*pb,dv=divisors(prod,2,20).filter(function(d){return prod/d>=2&&prod/d<=30&&d!==prod/d;});if(!dv.length)continue;
  b=dv[r.int(0,dv.length-1)];cc=prod/b;if(pb<4)continue;k=r.int(1,pb-2);x=pb-k;
  var es=divisors(t*t,2,t-1).filter(function(d){return t*t/d-d>=2;});if(es.length<2)continue;e=es[r.int(0,es.length-1)];var fs=es.filter(function(d){return d!==e;});f=fs[r.int(0,fs.length-1)];ok=true;}
 if(!ok){t=12;a=4;pb=8;b=4;cc=8;k=3;x=5;e=4;f=6;}
 var inside=t*t/e-e,whole2=t*t/f;
 var o=four('geo-circles-investigation-power',c,'Open Response: Two chords AB and CD intersect inside a circle at P. Each part uses the answer before it.',[
 ['PA = '+a+', PB = (x + '+k+'), PC = '+b+', and PD = '+cc+'. Use the intersecting chords theorem to find x.','x',x,a+'*(x+'+k+')='+b+'*'+cc,'The products of the segments of the two chords are equal.'],
 ['Chord AB is made of PA and PB. Use x from part a to find the length w of chord AB.','w',t,'w='+a+'+('+pn(x)+'+'+k+')','The chord is the sum of its two segments.'],
 ['From an exterior point, a tangent segment has the same length as chord AB from part b. A secant from the same point has an external segment of '+e+'. Find the internal segment y of the secant.','y',inside,e+'*(y+'+e+')='+pn(t)+'*'+pn(t),'The tangent squared equals the external segment times the whole secant.'],
 ['A second secant from the same point has an external segment of '+f+'. Using the tangent length from part b, find the length z of this whole secant.','z',whole2,f+'*z='+pn(t)+'*'+pn(t),'The tangent squared equals the external segment times the whole secant.']]);
 o.fig=fig(CF().chords({PA:String(a),PB:'(x+'+k+')',PC:String(b),PD:String(cc)},{PA:a,PB:pb,PC:b,PD:cc}));return o;}
/* Honors chain 3: expanded circle equation, center, radius and area. */
function invCoord(ctx){var r=ctx.rng,c=ctx.c,h=r.int(-12,12),k=r.int(-12,12),rad=r.int(3,c>=5?14:11);
 while(h===0||k===0||h*h+k*k-rad*rad===0){h=r.int(-12,12);k=r.int(-12,12);}
 var cs=h*h+k*k-rad*rad;
 var lx=-2*h,ly=-2*k,text='x² '+(lx<0?'− ':'+ ')+Math.abs(lx)+'x + y² '+(ly<0?'− ':'+ ')+Math.abs(ly)+'y '+(cs<0?'− ':'+ ')+Math.abs(cs)+' = 0';
 return four('geo-circles-investigation-coordinate',c,'Open Response: A circle has equation '+text+'. Complete the square to find its features. Each part uses the answer before it.',[
 ['The x terms give (x − h)² = x² − 2hx + h², so −2h equals the coefficient '+mn(lx)+'. Find h, the x-coordinate of the center.','h',h,'-2*h='+pn(lx),'The linear coefficient equals −2 times the center coordinate.'],
 ['The y terms give −2k equal to the coefficient '+mn(ly)+'. Find k, the y-coordinate of the center.','k',k,'-2*k='+pn(ly),'The linear coefficient equals −2 times the center coordinate.'],
 ['Completing the square gives r² = h² + k² − ('+mn(cs)+'). Use h = '+mn(h)+' and k = '+mn(k)+' from parts a and b. Find the radius w.','w',rad,'w^2='+pn(h)+'*'+pn(h)+'+'+pn(k)+'*'+pn(k)+'-'+pn(cs),'The radius squared is h squared plus k squared minus the constant term.'],
 ['The area of this circle is z times π square units. Use the radius from part c. Find z.','z',rad*rad,'z='+rad+'*'+rad,'Area is π times the radius squared.']]);}
/* Honors chain 4: arc and sector built from an angle written as an expression. */
function invSector(ctx){var r=ctx.rng,c=ctx.c,ks=[3,4,5,6,8,9,10,12],k,th,aa,x,b,ok=false;
 for(var i=0;i<300&&!ok;i++){k=ks[r.int(0,ks.length-1)];th=360/k;aa=r.int(2,3);var lo=Math.ceil((th-40)/aa),hi=Math.floor((th-2)/aa);if(lo<3)lo=3;if(hi<lo)continue;x=r.int(lo,hi);b=th-aa*x;if(b>=2&&b<=40)ok=true;}
 if(!ok){k=4;th=90;aa=2;x=35;b=20;}
 var rad=k*r.int(2,c>=5?12:9),L=2*rad/k,A=rad*rad/k;
 var o=four('geo-circles-investigation-sector',c,'Open Response: A sector of a circle with radius '+rad+' cm has a central angle of ('+aa+'x + '+b+')°, which is exactly '+(k===2?'half':'one-'+['','','','third','fourth','fifth','sixth','','eighth','ninth','tenth','','twelfth'][k])+' of the circle. Each part uses the answer before it.',[
 ['The angle is one-'+['','','','third','fourth','fifth','sixth','','eighth','ninth','tenth','','twelfth'][k]+' of 360°, so '+k+' times the angle equals 360. Find x.','x',x,k+'*('+aa+'*x+'+b+')=360','The whole circle is '+k+' copies of the sector angle.'],
 ['Use x from part a to find the central angle y, in degrees.','y',th,'y='+aa+'*'+pn(x)+'+'+b,'Substitute x into the angle expression.'],
 ['The exact arc length is z times π centimeters. Use the angle from part b. Find z.','z',L,'360*z=2*'+rad+'*'+th,'Arc length is the angle fraction of the circumference 2πr; divide out π.'],
 ['The exact area of the sector is w times π square centimeters. Use the angle from part b. Find w.','w',A,'360*w='+rad+'*'+rad+'*'+th,'Sector area is the angle fraction of the circle area πr²; divide out π.']]);
 o.fig=fig(CF().sector(th,'('+aa+'x+'+b+')°',rad+' cm','zπ','arc'));return o;}

/* Coverage additions: circle equations from three points or a tangent line, tangent lines at a point, and arc length or sector area to the nearest tenth. */
var LATT={25:[[3,4],[4,3],[5,0],[0,5]],100:[[6,8],[8,6],[10,0],[0,10]],169:[[5,12],[12,5],[13,0],[0,13]],50:[[1,7],[7,1],[5,5]],65:[[1,8],[8,1],[4,7],[7,4]]};
function allOff(r2){var o=[];LATT[r2].forEach(function(q){[[1,1],[1,-1],[-1,1],[-1,-1]].forEach(function(s){var t=[q[0]*s[0],q[1]*s[1]];if(!o.some(function(u){return u[0]===t[0]&&u[1]===t[1];}))o.push(t);});});return o;}
function sgn(n){return n<0?'+'+(-n):n>0?'-'+n:'';}
function circEq(h,k,r2){return (h?'(x'+sgn(h)+')':'x')+'^2+'+(k?'(y'+sgn(k)+')':'y')+'^2='+r2;}
function circleEquations(ctx){var r=ctx.rng,c=ctx.c,h=r.int(-6,6),k=r.int(-6,6),kind=c<=3?'tangent-line':c<=5?r.pick(['tangent-line','three','tangent-at']):r.pick(['three','tangent-at','three']),r2,pr,ans,steps,alts;
 if(kind==='tangent-line'){var ax=r.pick(['x','y']),d=K.nz(r,-8,8),cv=(ax==='x'?h:k)+d;r2=d*d;
  pr='A circle has center ('+h+', '+k+') and is tangent to the line '+ax+' = '+cv+'. Write an equation of the circle.';ans=circEq(h,k,r2);alts=[circEq(h,k,Math.abs(d)),circEq(-h,-k,r2),circEq(h,k,cv*cv===r2?r2+1:cv*cv)];
  steps=[step('The radius is the distance from the center to the tangent line: |'+(ax==='x'?h:k)+' − '+cv+'| = '+Math.abs(d)+'.',''),step('Equation:',M(ans))];}
 else if(kind==='three'){r2=r.pick(c>=6?[25,50,65,100,169]:[25,100,169]);var offs=r.shuffle(allOff(r2)).slice(0,3),pts=offs.map(function(o){return [h+o[0],k+o[1]];});
  pr='A circle passes through the points ('+pts[0].join(', ')+'), ('+pts[1].join(', ')+') and ('+pts[2].join(', ')+'). Write an equation of the circle.';ans=circEq(h,k,r2);alts=[circEq(-h,-k,r2),circEq(h,k,Math.round(Math.sqrt(r2))),circEq(k,h,r2===25?169:25)];
  steps=[step('The center is equidistant from the three points: it lies on the perpendicular bisector of each chord.',''),step('Solving the two perpendicular bisector equations gives the center ('+h+', '+k+').',''),step('The radius squared is the squared distance to any point: '+r2+'.',M(ans))];}
 else{r2=r.pick([25,100,169]);var o=r.pick(allOff(r2)),px=h+o[0],py=k+o[1],line;
  if(o[1]===0)line='x='+px;else if(o[0]===0)line='y='+py;else{var g=K.gcd(Math.abs(o[0]),Math.abs(o[1])),n=-o[0]/g,dn=o[1]/g;if(dn<0){n=-n;dn=-dn;}var mT=dn===1?String(n):(n<0?'-':'')+'\\frac{'+Math.abs(n)+'}{'+dn+'}';line='y'+sgn(py)+'='+(mT==='1'?'':mT==='-1'?'-':mT)+'(x'+sgn(px)+')';}
  pr='The circle with center ('+h+', '+k+') passes through ('+px+', '+py+'). Write an equation of the line tangent to the circle at ('+px+', '+py+').';ans=line;
  alts=[o[0]&&o[1]?'y'+sgn(py)+'='+(o[1]/o[0]===1?'':o[1]/o[0]===-1?'-':(o[1]*o[0]<0?'-':'')+'\\frac{'+Math.abs(o[1])+'}{'+Math.abs(o[0])+'}')+'(x'+sgn(px)+')':(o[1]===0?'y='+py:'x='+px),o[1]===0?'x='+h:o[0]===0?'y='+k:'y'+sgn(k)+'='+line.split('=')[1].replace('(x'+sgn(px)+')','(x'+sgn(h)+')')];
  steps=[step('A tangent line is perpendicular to the radius at the point of tangency.',''),step('The radius has slope '+(o[0]?o[1]+'/'+o[0]:'undefined')+', so the tangent has the opposite reciprocal slope.',''),step('Line through ('+px+', '+py+'):',M(line))];}
 var gf;if(kind==='tangent-line'){var ln={text:ax+' = '+cv};ln[ax]=cv;gf={kind:'geo-grid',shapes:[{id:'ctr',pts:[[h,k]],labels:['C']}],lines:[ln],circles:[{c:[h,k],r:Math.abs(d)}],alt:'Center C and the tangent line on a coordinate grid'};}
 else if(kind==='three')gf={kind:'geo-grid',shapes:pts.map(function(q,i){return {id:'p'+i,pts:[q]};}),alt:'Three points of the circle on a coordinate grid'};
 else gf={kind:'geo-grid',shapes:[{id:'rad',pts:[[h,k],[px,py]],labels:['C','P']}],circles:[{c:[h,k],r:Math.sqrt(r2)}],alt:'A circle, its center C and the point of tangency P'};
 return {fig:fig(gf),variant:'geo-circeq-'+kind+'-'+c,prompt:pr,parts:[{answer:M(ans),check:{type:'derive',kind:'circle-eq',alts:alts.filter(function(a){return a!==ans;}).map(M)}}],steps:steps,space:[1.2,1.5,1.8]};}
function arcDecimal(ctx){var r=ctx.rng,c=ctx.c,sector=r.chance(0.5),useD=c>=4&&r.chance(0.4),rad=r.int(3,c>=5?20:12),th=r.pick([30,40,45,50,60,72,75,80,100,110,120,135,140,150,210,225,240,270,300]);
 var val=sector?Math.PI*rad*rad*th/360:2*Math.PI*rad*th/360,t=val*10;K.need(Math.abs(t-Math.floor(t)-0.5)>1e-4);var out=(Math.round(t)/10).toFixed(1),unit=r.pick(['centimeters','inches','feet','meters']);
 var pr='A circle has '+(useD?'diameter '+2*rad:'radius '+rad)+' '+unit+'. Find the '+(sector?'area of a sector':'length of an arc')+' with a central angle of '+th+'°. Round to the nearest tenth.';
 var ab={centimeters:'cm',inches:'in.',feet:'ft',meters:'m'}[unit];
 return {fig:fig(CF().sector(th,th+'°',useD?'':rad+' '+ab,'?',sector?'inside':'arc')),variant:'geo-arcdec-'+(sector?'sector':'arc')+'-'+c,prompt:pr,parts:[{answer:M(out)+' '+(sector?'square '+unit:unit),check:{type:'derive',kind:'arc-dec',alts:[(Math.round((sector?2*Math.PI*rad*th/360:Math.PI*rad*rad*th/360)*10)/10).toFixed(1),(Math.round(val*20)/10).toFixed(1),(Math.round(val*5)/10).toFixed(1)].filter(function(z){return z!==out;}).map(M)}}],
  steps:[step((useD?'The radius is half the diameter: '+rad+'. ':'')+(sector?'Sector area = (θ/360)·πr².':'Arc length = (θ/360)·2πr.'),''),step('Compute and round: '+out+'.','')],space:[0.9,1.1,1.3]};}

/* ---- 2026-11-17 audit: inscribed quadrilaterals (G-C.A.3) and parabolas from focus and directrix (G-GPE.A.2) ---- */
function inscribedQuad(ctx){var r=ctx.rng,c=ctx.c,pair=r.pick([['A','C'],['B','D']]),P=pair[0],Qn=pair[1],angP,pr,ans,alts,st,lab={};
 var ex=function(k,b){return (k===1?'x':k+'x')+(b<0?' − '+(-b):b>0?' + '+b:'');};
 if(c<=2){angP=r.int(45,135);K.need(angP!==90);pr='Quadrilateral ABCD is inscribed in a circle. m∠'+P+' = '+angP+'°. Find m∠'+Qn+'.';ans=(180-angP)+'°';alts=[angP+'°',(360-angP)+'°'];lab[P]=angP+'°';lab[Qn]='?';
  st=[step('Opposite angles of an inscribed quadrilateral are supplementary.',M('m\\angle '+Qn+'=180-'+angP)),step('m∠'+Qn+' = '+(180-angP)+'°.')];}
 else{var x=r.int(5,30),p1=r.int(1,c>=6?5:3),q1=r.int(1,c>=6?5:3),b1=r.int(-20,40);angP=p1*x+b1;var angQ=180-angP,b2=angQ-q1*x;K.need(angP>=45&&angP<=135&&angP!==90&&b2>-40&&b2<80);
  var askAngle=c>=6;pr='Quadrilateral ABCD is inscribed in a circle. m∠'+P+' = ('+ex(p1,b1)+')° and m∠'+Qn+' = ('+ex(q1,b2)+')°. Find '+(askAngle?'m∠'+P:'x')+'.';
  ans=askAngle?angP+'°':M('x='+x);alts=askAngle?[angQ+'°',x+'°']:[M('x='+(x+1)),M('x='+Math.round((90-b1-b2)/(p1+q1)))].filter(function(z){return z!==ans;});lab[P]='('+ex(p1,b1)+')°';lab[Qn]='('+ex(q1,b2)+')°';
  st=[step('Opposite angles of an inscribed quadrilateral are supplementary.',M('('+ex(p1,b1).replace(/ /g,'')+')+('+ex(q1,b2).replace(/ /g,'')+')=180')),step('Solve: '+(p1+q1)+'x + '+(b1+b2)+' = 180, so x = '+x+'.'),askAngle?step('m∠'+P+' = '+p1+'('+x+') '+(b1<0?'− '+(-b1):'+ '+b1)+' = '+angP+'°.'):step('x = '+x+'.')];}
 // true figure: arcs AB, BC, CD, DA with the angle at the first vertex of the pair equal to angP
 var angA=P==='A'?angP:null,ok=false,al,be,ga,de;for(var t=0;t<60&&!ok;t++){var sA=P==='A'?2*angP:2*r.int(50,130);be=r.int(40,sA-40);ga=sA-be;al=r.int(40,320-sA);de=360-sA-al;
  if(P==='B'){// angle B = (ga+de)/2 = angP
   var sB=2*angP;ga=r.int(40,sB-40);de=sB-ga;al=r.int(40,320-sB);be=360-sB-al;}
  ok=Math.min(al,be,ga,de)>=40;}
 K.need(ok);var t0=r.int(0,359),pos={A:t0,B:t0+al,C:t0+al+be,D:t0+al+be+ga},pts={};['A','B','C','D'].forEach(function(n){pts[n]=NS.geoFigures.on(pos[n]);});
 var nb={A:['B','D'],B:['A','C'],C:['B','D'],D:['A','C']},angles=[P,Qn].map(function(n){return {v:n,a:nb[n][0],b:nb[n][1],label:lab[n]};});
 var fig0={kind:'geo-circle',exact:true,pts:pts,onCircle:['A','B','C','D'],segs:[{p:'A',q:'B'},{p:'B',q:'C'},{p:'C',q:'D'},{p:'D',q:'A'}],angles:angles,alt:'Quadrilateral ABCD inscribed in a circle'};
 return {variant:'geo-inscribed-quad-'+(c<=2?'value':'expr')+'-'+c,prompt:pr,fig:fig(fig0),parts:[{answer:ans,check:{type:'derive',kind:'inscribed-quad',alts:alts}}],steps:st,space:[1.1,1.5,1.9]};}
function parabola(ctx){var r=ctx.rng,c=ctx.c,p=r.pick([1,2,3,4,-1,-2,-3,-4,1.5,-1.5].filter(function(v){return c>=6||Number.isInteger(v);})),h=c<=2?0:r.int(-6,6),k=c<=2?r.int(-3,3):r.int(-6,6),horiz=c>=6&&r.chance(0.5),f4=4*p;
 var coef=Number.isInteger(f4)?(f4<0?'-':'')+'\\frac{1}{'+Math.abs(f4)+'}':(f4<0?'-':'')+'\\frac{1}{'+Math.abs(f4)+'}';
 var sq=function(v,a){return a===0?v+'^2':'('+v+(a>0?'-'+a:'+'+(-a))+')^2';},cst=function(b){return b===0?'':b>0?'+'+b:'-'+(-b);};
 var fmt=function(n){return String(n).replace('-','−');},focus,dir,ans,alts;
 if(!horiz){focus='('+fmt(h)+', '+fmt(k+p)+')';dir='y = '+fmt(k-p);ans=M('y='+coef+sq('x',h)+cst(k));alts=[M('y='+(f4<0?'-':'')+'\\frac{1}{'+Math.abs(2*p)+'}'+sq('x',h)+cst(k)),M('y='+(f4<0?'':'-')+'\\frac{1}{'+Math.abs(f4)+'}'+sq('x',h)+cst(k))];}
 else{focus='('+fmt(h+p)+', '+fmt(k)+')';dir='x = '+fmt(h-p);ans=M('x='+coef+sq('y',k)+cst(h));alts=[M('y='+coef+sq('x',h)+cst(k)),M('x='+(f4<0?'':'-')+'\\frac{1}{'+Math.abs(f4)+'}'+sq('y',k)+cst(h))];}
 alts=alts.filter(function(z){return z!==ans;});
 var pr='A parabola has focus '+focus+' and directrix '+dir+'. Write an equation of the parabola.';
 var st=[step('Every point on a parabola is the same distance from the focus and the directrix.'),step('The vertex is halfway between them: ('+fmt(h)+', '+fmt(k)+'), and p = '+fmt(p)+' is the directed distance from the vertex to the focus.'),
  step(horiz?'For a horizontal parabola: x = (1/(4p))(y − k)² + h.':'For a vertical parabola: y = (1/(4p))(x − h)² + k.',ans)];
 var gr={kind:'geo-grid',shapes:[{id:'f',pts:[horiz?[h+p,k]:[h,k+p]],labels:['F']}],lines:[horiz?{x:h-p,text:dir.replace(/ /g,'')}:{y:k-p,text:dir.replace(/ /g,'')}],alt:'Focus F and the directrix on a coordinate grid'};
 if(!Number.isInteger(p))gr=null;
 return {variant:'geo-parabola-'+(horiz?'horizontal':'vertical')+'-'+c,prompt:pr,fig:gr?fig(gr):undefined,parts:[{answer:ans,check:{type:'derive',kind:'parabola',alts:alts}}],steps:st,space:[1.4,1.8,2.2]};}
/* ---- 2026-11-20 audit 2: tangent segments from an exterior point (G-C.A.4) and ellipses/hyperbolas from foci (G-GPE.A.3) ---- */
var TRIPLES=[[3,4,5],[5,12,13],[8,15,17],[7,24,25],[20,21,29],[6,8,10],[9,12,15]];
function tangentExt(ctx){var r=ctx.rng,c=ctx.c,tr=r.pick(TRIPLES),k=r.int(1,c>=5?3:2),legs=r.chance(0.5)?[tr[0],tr[1]]:[tr[1],tr[0]],R=legs[0]*k,T=legs[1]*k,D=tr[2]*k,unit=r.pick(['cm','ft','m']);
 var why='Construction: bisect OP at M and draw the circle centered at M through O and P. It meets circle O at the point of tangency T, so ∠OTP is inscribed in a semicircle and measures 90°.';
 var pr,ans,alts,st;
 if(c<=2){pr='Point P is outside circle O, which has radius '+R+' '+unit+'. OP = '+D+' '+unit+'. You construct a tangent from P that touches the circle at T. Find PT.';ans=T;alts=[D-R,R+D,Math.round(Math.sqrt(D*D+R*R))];
  st=[step(why),step('Use the Pythagorean theorem in right triangle OTP.',M('PT^2+'+R+'^2='+D+'^2')),step('PT = '+T+' '+unit+'.')];}
 else if(c<=4){pr='Point P is outside circle O. A tangent constructed from P touches the circle at T. PT = '+T+' '+unit+' and OP = '+D+' '+unit+'. Find the radius of circle O.';ans=R;alts=[D-T,T,Math.round(Math.sqrt(D*D+T*T))];
  st=[step(why),step('Use the Pythagorean theorem in right triangle OTP.',M('r^2+'+T+'^2='+D+'^2')),step('r = '+R+' '+unit+'.')];}
 else{pr='Point P is outside circle O, which has radius '+R+' '+unit+'. OP = '+D+' '+unit+'. You construct both tangents from P; they touch the circle at T and U. Find the perimeter of quadrilateral OTPU.';ans=2*R+2*T;alts=[R+T,2*R+2*D,2*T+D];
  st=[step(why),step('In right triangle OTP, PT² = '+D+'² − '+R+'² so PT = '+T+'. The two tangent segments from P are congruent, so PU = '+T+' too.'),step('Perimeter = '+R+' + '+T+' + '+T+' + '+R+' = '+ans+' '+unit+'.')];}
 alts=alts.filter(function(a,i,arr){return a>0&&a!==ans&&arr.indexOf(a)===i;}).map(function(a){return M(String(a))+' '+unit;});
 return {variant:'geo-tangent-ext-'+(c<=2?'pt':c<=4?'r':'kite')+'-'+c,prompt:pr,parts:[{answer:M(String(ans))+' '+unit,check:{type:'derive',kind:'tangent-ext',alts:alts}}],steps:st,space:[1.2,1.5,1.8]};}
function conicFoci(ctx){var r=ctx.rng,c=ctx.c,hyp=r.chance(0.5),tr=r.pick([[3,4,5],[5,12,13],[8,15,17],[7,24,25]]),sc=tr[2]<=5?r.int(1,3):1,vert=r.chance(0.5),h=c>=4?r.int(-5,5):0,kk=c>=4?r.int(-5,5):0;tr=tr.map(function(z){return z*sc;});
 var a,b,f;if(hyp){var p=r.chance(0.5)?[tr[0],tr[1]]:[tr[1],tr[0]];a=p[0];b=p[1];f=tr[2];}else{var q=r.chance(0.5)?[tr[0],tr[1]]:[tr[1],tr[0]];b=q[0];f=q[1];a=tr[2];}
 K.need(a<=25&&f<=25&&(c>=4||h===0));
 var fm=function(n){return String(n).replace('-','−');},F1=vert?[h,kk-f]:[h-f,kk],F2=vert?[h,kk+f]:[h+f,kk],pt=function(P){return '('+fm(P[0])+', '+fm(P[1])+')';};
 var sq=function(v,s){return s===0?v+'^2':'('+v+(s>0?'-'+s:'+'+(-s))+')^2';},X=sq('x',h),Y=sq('y',kk);
 var main=vert?'\\frac{'+Y+'}{'+a*a+'}':'\\frac{'+X+'}{'+a*a+'}',other=vert?'\\frac{'+X+'}{'+b*b+'}':'\\frac{'+Y+'}{'+b*b+'}';
 var eq=function(m,o,sign){return M((vert&&!hyp?o+sign+m:m+sign+o)+'=1');};
 var ans=eq(main,other,hyp?'-':'+');
 var mainS=vert?'\\frac{'+Y+'}{'+b*b+'}':'\\frac{'+X+'}{'+b*b+'}',otherS=vert?'\\frac{'+X+'}{'+a*a+'}':'\\frac{'+Y+'}{'+a*a+'}',otherC=vert?'\\frac{'+X+'}{'+f*f+'}':'\\frac{'+Y+'}{'+f*f+'}';
 var alts=[eq(mainS,otherS,hyp?'-':'+'),eq(main,other,hyp?'+':'-'),eq(main,otherC,hyp?'-':'+')].filter(function(z,i,arr){return z!==ans&&arr.indexOf(z)===i;});
 var name=hyp?'A hyperbola':'An ellipse',rule=hyp?'The difference of the distances from any point on the hyperbola to the foci is '+2*a+'.':'The sum of the distances from any point on the ellipse to the foci is '+2*a+'.';
 var pr=name+' has foci '+pt(F1)+' and '+pt(F2)+'. '+rule+' Write an equation of the '+(hyp?'hyperbola':'ellipse')+'.';
 var st=[step('The center is the midpoint of the foci: '+pt([h,kk])+', and c = '+f+' is the distance from the center to each focus.'),
  step((hyp?'The constant difference is 2a':'The constant sum is 2a')+', so a = '+a+' and a² = '+a*a+'.'),
  step(hyp?'For a hyperbola c² = a² + b², so b² = '+f*f+' − '+a*a+' = '+b*b+'.':'For an ellipse a² = b² + c², so b² = '+a*a+' − '+f*f+' = '+b*b+'.'),
  step('The '+(vert?'vertical':'horizontal')+' axis goes with a².',ans)];
 return {variant:'geo-conic-'+(hyp?'hyperbola':'ellipse')+'-'+(vert?'v':'h')+'-'+c,prompt:pr,parts:[{answer:ans,check:{type:'derive',kind:'conic-foci',alts:alts}}],steps:st,space:[1.4,1.8,2.2]};}

NS.registerSkillSet({id:'geometry-circles',course:'geometry',courseName:'Geometry',unit:'circles',unitName:'Circles',title:'Circle Relationships',
tags:{INVEST:'Four-part circle investigation',INSQUAD:'Inscribed quadrilaterals',PARABOLA:'Parabolas from focus and directrix',TANCON:'Constructing tangents from an exterior point',CONIC:'Ellipses and hyperbolas from their foci',CENTRAL:'Central angles and arcs',INSCRIBED:'Inscribed angles',TANGENT:'Tangents and radii',MEASURE:'Radius and diameter',SEMICIRCLE:'Angles in a semicircle',CHORDS:'Intersecting chord products',SECANTS:'Two-secant power theorem',TANSEC:'Tangent-secant power theorem',ARC:'Exact arc length',SECTOR:'Exact sector area',COORD:'Circle equations from coordinates',CHORDDIST:'Chord length from center distance',EXPANDED:'Circle center and radius from expanded equation'},
reference:'<div class="mm-refgrid"><section><h4>Arcs and angles</h4><p>A central angle equals its intercepted minor arc; an inscribed angle is half its intercepted arc.</p></section><section><h4>Tangents</h4><p>A tangent is perpendicular to the radius at the point of tangency.</p></section></div>',
gaps:[],
skills:[
{id:'circle-equation-three-points-tangent',tag:'COORD',name:'Circle equations from three points or a tangent line; tangent lines',best:[1,2],generate:ctx=>K.retry(()=>circleEquations(ctx))},
{id:'circle-arc-sector-decimal',tag:'ARC',name:'Arc length and sector area to the nearest tenth',best:[0,1,2],generate:ctx=>K.retry(()=>arcDecimal(ctx))},
{id:'circle-central-arc',tag:'CENTRAL',name:'Central angle and minor arc',best:[0,1],generate:central},
{id:'circle-inscribed-angle',tag:'INSCRIBED',name:'Inscribed angle from arc',best:[0,1],generate:inscribed},
{id:'circle-inscribed-quadrilateral',tag:'INSQUAD',name:'Opposite angles of an inscribed quadrilateral',best:[0,1,2],generate:ctx=>K.retry(()=>inscribedQuad(ctx))},
{id:'circle-intercepted-arc',tag:'INSCRIBED',name:'Intercepted arc from inscribed angle',best:[0,1],generate:intercepted},
{id:'circle-tangent-radius',tag:'TANGENT',name:'Radius and tangent angle',best:[0,1],generate:tangent},
{id:'circle-diameter',tag:'MEASURE',name:'Diameter from radius',best:[0,1],generate:diameter},
{id:'circle-radius',tag:'MEASURE',name:'Radius from diameter',best:[0,1],generate:radius},
{id:'circle-semicircle-angle',tag:'SEMICIRCLE',name:'Angle inscribed in a semicircle',best:[0,1],generate:chord},
{id:'circle-intersecting-chords',tag:'CHORDS',name:'Intersecting chord segment products',best:[0,1],generate:intersectingChords},
{id:'circle-two-secants',tag:'SECANTS',name:'Two secants from an exterior point',best:[0,1],generate:twoSecants},
{id:'circle-tangent-secant',tag:'TANSEC',name:'Tangent and secant from an exterior point',best:[0,1],generate:tangentSecant},
{id:'circle-arc-length-exact',tag:'ARC',name:'Arc length in exact pi form',best:[0,1],generate:arcLength},
{id:'circle-sector-area-exact',tag:'SECTOR',name:'Sector area in exact pi form',best:[0,1],generate:sectorArea},
{id:'circle-radius-squared-from-point',tag:'COORD',name:'Radius squared from a center and point',best:[0,1],generate:circleRadiusSquared},
{id:'circle-chord-length-from-distance',tag:'CHORDDIST',name:'Chord length from radius and center distance',best:[0,1],generate:chordLengthFromDistance},
{id:'circle-center-expanded-equation',tag:'EXPANDED',name:'Center coordinate by completing the square',best:[0,1],generate:centerFromExpandedEquation},
{id:'circle-radius-expanded-equation',tag:'EXPANDED',name:'Radius from expanded circle equation',best:[0,1],generate:radiusFromExpandedEquation},
{id:'circle-tangent-exterior-construction',tag:'TANCON',name:'Tangent segments constructed from an exterior point',best:[0,1,2],generate:ctx=>K.retry(()=>tangentExt(ctx))},
{id:'conic-foci-ellipse-hyperbola',tag:'CONIC',name:'Ellipses and hyperbolas from foci and a constant sum or difference',best:[2],generate:ctx=>K.retry(()=>conicFoci(ctx))},
{id:'parabola-focus-directrix',tag:'PARABOLA',name:'Equation of a parabola from its focus and directrix',best:[1,2],generate:ctx=>K.retry(()=>parabola(ctx))},
{id:'circles-investigation-angles',tag:'INVEST',name:'Honors: inscribed angle and arc expressions, major arc, tangent-chord angle',best:[2],generate:invAngles},
{id:'circles-investigation-power',tag:'INVEST',name:'Honors: chords, tangent-secant and secant-secant lengths',best:[2],generate:invPower},
{id:'circles-investigation-coordinate',tag:'INVEST',name:'Honors: expanded circle equation, center, radius and area',best:[2],generate:invCoord},
{id:'circles-investigation-sector',tag:'INVEST',name:'Honors: arc length and sector area from an angle expression',best:[2],generate:invSector},
{id:'circle-open-response-investigation',tag:'INVEST',name:'Four-part circle investigation',best:[2],generate:circleInvestigation}
]});
})(typeof window!=='undefined'?window:globalThis);
