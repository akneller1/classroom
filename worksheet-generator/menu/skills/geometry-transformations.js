/* Geometry Unit 8: coordinate transformations, text-first verified starter bank. */
(function(G){'use strict';var NS=G.MKMENU,K=NS.kit,M=K.M,step=K.step;
/* The unknown is named for the coordinate asked for (x for an x-coordinate, y for a y-coordinate), so a question never asks for "the y-coordinate x". */
function make(id,prompt,eq,x,reason,fig){var v='x',mm=/Find x, the ([xy])-coordinate/.exec(prompt);if(mm)v=mm[1];else if(/the y-coordinate x\b/.test(prompt))v='y';
 if(v!=='x'){prompt=prompt.replace(/Find x, the/,'Find '+v+', the').replace(/-coordinate x\b/,'-coordinate '+v);eq=eq.replace(/x/g,v);}
 var o={variant:id,prompt:prompt+' Set up and solve an equation for '+v+'.',parts:[{answer:M(v+'='+x),check:{type:'solve',eq:eq,v:v}}],steps:[step(reason,M(eq)),step('Solve for '+v+'.',M(v+'='+x))],space:[1.2,1.5,1.8]};if(fig)o.fig=fig;return o;}
function nz(r){var n=r.int(-9,9);return n===0?4:n;}
function reflect(ctx,axis){var r=ctx.rng,a=nz(r),b=nz(r),x=axis==='x'?-b:-a,eq='x'+((axis==='x'?b:a)>=0?'+':'')+(axis==='x'?b:a)+'=0';
return make('geo-transform-reflect-'+axis+'-'+ctx.c,'Point P('+a+', '+b+') is reflected across the '+axis+'-axis. Find '+(axis==='x'?'the y-coordinate':'the x-coordinate')+' x of the image P′.',eq,x,'Reflection across the '+axis+'-axis changes the sign of the '+(axis==='x'?'y':'x')+'-coordinate.',ptFig(a,b));}
function translate(ctx,axis){var r=ctx.rng,a=nz(r),b=nz(r),shift=nz(r),x=(axis==='x'?a:b)+shift,eq='x'+(shift>=0?'-':'+')+Math.abs(shift)+'='+(axis==='x'?a:b);
return make('geo-transform-translate-'+axis+'-'+ctx.c,'Point P('+a+', '+b+') is translated '+Math.abs(shift)+' units '+(axis==='x'?(shift>0?'right':'left'):(shift>0?'up':'down'))+'. Find the '+(axis==='x'?'x':'y')+'-coordinate x of P′.',eq,x,'A translation adds the signed displacement to the selected coordinate.',ptFig(a,b));}
function rotate(ctx,dir){var r=ctx.rng,a=nz(r),b=nz(r),x=dir==='cw'?b:-b,eq='x'+((dir==='cw'?-b:b)>=0?'+':'')+(dir==='cw'?-b:b)+'=0';
return make('geo-transform-rotate-'+dir+'-'+ctx.c,'Point P('+a+', '+b+') is rotated 90° '+(dir==='cw'?'clockwise':'counterclockwise')+' about the origin. Find the x-coordinate x of P′.',eq,x,'A 90° rotation maps (a,b) to '+(dir==='cw'?'(b,−a).':'(−b,a).'),ptFig(a,b));}
function dilate(ctx){var r=ctx.rng,a=nz(r),b=nz(r),k=r.int(2,ctx.c>=5?5:3),x=k*a,eq='x='+k+'*'+a;
return make('geo-transform-dilate-'+ctx.c,'Point P('+a+', '+b+') is dilated about the origin by a scale factor of '+k+'. Find the x-coordinate x of P′.',eq,x,'Multiply each coordinate by the scale factor.',ptFig(a,b));}

var GR=function(){return NS.geoFigures&&NS.geoFigures.grid;};
function mn(n){return String(n).replace('-','\u2212');}
function addTerm(n){return n>=0?'+'+n:'-'+(-n);}
function ptFig(a,b){return {kind:'geo-grid',shapes:[{id:'pre',pts:[[a,b]],labels:['P('+mn(a)+', '+mn(b)+')']}],alt:'Coordinate plane with point P('+a+', '+b+')'};}
function triPts(r,lim){for(var t=0;t<200;t++){var p=[];for(var i=0;i<3;i++)p.push([r.int(-lim,lim),r.int(-lim,lim)]);var A=p[0],B=p[1],C=p[2],ar=Math.abs((B[0]-A[0])*(C[1]-A[1])-(C[0]-A[0])*(B[1]-A[1]));
 if(ar>=6&&!(A[0]===B[0]&&A[1]===B[1])&&Math.max(Math.abs(B[0]-A[0]),Math.abs(C[0]-A[0]),Math.abs(B[0]-C[0]))>=2)return p;}return [[-3,-2],[3,-2],[1,3]];}
function triText(p){return 'Triangle ABC has vertices A('+p[0][0]+', '+p[0][1]+'), B('+p[1][0]+', '+p[1][1]+'), and C('+p[2][0]+', '+p[2][1]+').';}
function triFig(p,extra,lines,alt){var sh=[{id:'pre',pts:p,labels:['A','B','C']}];if(extra)sh.push(extra);return {kind:'geo-grid',shapes:sh,lines:lines||[],alt:alt};}
function ask(r){var v=r.int(0,2),co=r.int(0,1);return {v:v,co:co,L:'ABC'[v],cn:co?'y':'x'};}
function translateTri(ctx){var r=ctx.rng,p=triPts(r,ctx.c>=5?6:5),dx=nz(r),dy=nz(r);if(ctx.c<5){dx=r.int(1,6)*(r.int(0,1)?1:-1);}
 var img=p.map(function(q){return [q[0]+dx,q[1]+dy];}),a=ask(r),u=p[a.v][a.co],d=a.co?dy:dx,x=u+d;
 return make('geo-transform-fig-translate-'+ctx.c,triText(p)+' It is translated to triangle A\u2032B\u2032C\u2032, shown on the grid. Find x, the '+a.cn+'-coordinate of '+a.L+'\u2032.','x='+u+(d>=0?'+':'-')+Math.abs(d),x,'Compare a vertex with its image to find the shift, then add the shift to the coordinate.',
  triFig(p,{id:'img',pts:img,labels:['A\u2032','B\u2032','C\u2032'],of:'pre',tx:{type:'translate',dx:dx,dy:dy}},[],'Triangle ABC and its translated image'));}
function reflectTri(ctx){var r=ctx.rng,p=triPts(r,5),c=ctx.c>=3?r.int(-3,3):0,vert=r.int(0,1)===1,ln=vert?{x:c}:{y:c},a=ask(r);a.co=vert?0:1;a.cn=vert?'x':'y';var u=p[a.v][a.co],x=2*c-u;
 ln.text=(vert?'x':'y')+' = '+mn(c);
 return make('geo-transform-fig-reflect-'+ctx.c,triText(p)+' It is reflected across the dashed line shown on the grid. Find x, the '+a.cn+'-coordinate of '+a.L+'\u2032.','x'+addTerm(u)+'='+(2*c),x,'A reflection puts each vertex the same distance from the mirror line on the opposite side, so the coordinates add to twice the mirror value.',
  triFig(p,null,[ln],'Triangle ABC and a dashed mirror line '+ln.text));}
function rotateTri(ctx){var r=ctx.rng,p=triPts(r,5),types=ctx.c>=5?['cw','ccw','half']:['cw','ccw'],t=types[r.int(0,types.length-1)],a=ask(r),f=function(q){return t==='cw'?[q[1],-q[0]]:t==='ccw'?[-q[1],q[0]]:[-q[0],-q[1]];},
 q=f(p[a.v]),x=q[a.co],sgn,u;
 if(t==='half'){u=p[a.v][a.co];sgn=-1;}else if(t==='cw'){u=a.co===0?p[a.v][1]:p[a.v][0];sgn=a.co===0?1:-1;}else{u=a.co===0?p[a.v][1]:p[a.v][0];sgn=a.co===0?-1:1;}
 var eq='x'+addTerm(sgn===1?-u:u)+'=0';
 return make('geo-transform-fig-rotate-'+ctx.c,triText(p)+' It is rotated '+(t==='half'?'180\u00b0':'90\u00b0 '+(t==='cw'?'clockwise':'counterclockwise'))+' about the origin. Find x, the '+a.cn+'-coordinate of '+a.L+'\u2032.',eq,x,t==='half'?'A 180\u00b0 rotation about the origin changes the sign of both coordinates.':t==='cw'?'A 90\u00b0 clockwise rotation maps (a, b) to (b, \u2212a).':'A 90\u00b0 counterclockwise rotation maps (a, b) to (\u2212b, a).',
  triFig(p,null,[],'Triangle ABC on the coordinate plane'));}
/* Composition: a reflection or rotation followed by a translation. The middle triangle is drawn dashed so the two steps can be seen. */
function composeTri(ctx){var r=ctx.rng,c=ctx.c,p=triPts(r,3),types=c>=5?['rx','ry','cw','ccw']:['rx','ry'],t=types[r.int(0,types.length-1)],a=ask(r);
 var f=t==='rx'?function(q){return [q[0],-q[1]];}:t==='ry'?function(q){return [-q[0],q[1]];}:t==='cw'?function(q){return [q[1],-q[0]];}:function(q){return [-q[1],q[0]];};
 var tx=t==='rx'?{type:'reflect-x'}:t==='ry'?{type:'reflect-y'}:t==='cw'?{type:'rotate-cw'}:{type:'rotate-ccw'};
 var words=t==='rx'?'reflected across the x-axis':t==='ry'?'reflected across the y-axis':t==='cw'?'rotated 90° clockwise about the origin':'rotated 90° counterclockwise about the origin';
 var dx=r.int(2,4)*(r.int(0,1)?1:-1),dy=r.int(2,4)*(r.int(0,1)?1:-1);
 var mid=p.map(f),img=mid.map(function(q){return [q[0]+dx,q[1]+dy];}),m=mid[a.v][a.co],d=a.co?dy:dx,x=m+d;
 var move='translated '+Math.abs(dx)+' unit'+(Math.abs(dx)===1?'':'s')+' '+(dx>0?'right':'left')+' and '+Math.abs(dy)+' unit'+(Math.abs(dy)===1?'':'s')+' '+(dy>0?'up':'down');
 var fig=triFig(p,{id:'mid',pts:mid,labels:['A′','B′','C′'],of:'pre',tx:tx,dash:true},[],'Triangle ABC, its dashed intermediate image, and its final image');
 fig.shapes.push({id:'img',pts:img,labels:['A″','B″','C″'],of:'mid',tx:{type:'translate',dx:dx,dy:dy}});
 return make('geo-transform-fig-compose-'+c,triText(p)+' It is first '+words+' to form triangle A′B′C′ (dashed), and then '+move+' to form triangle A″B″C″. Find x, the '+a.cn+'-coordinate of '+a.L+'″.','x='+m+(d>=0?'+':'-')+Math.abs(d),x,'Apply the first transformation to get the middle triangle, then add the shift to the coordinate.',fig);}
/* Symmetry of regular polygons: the polygon is only drawn (n is not printed), so the number of sides is read from the figure. */
function symLines(ctx){var r=ctx.rng,ns=ctx.c>=5?[3,4,5,6,7,8,9,10,12]:[3,4,5,6,8],n=ns[r.int(0,ns.length-1)];
 return {variant:'geo-symmetry-lines-'+ctx.c,fig:{kind:'geo-regular',n:n,plain:true},prompt:['The regular polygon shown has x lines of symmetry.','A designer draws the regular polygon shown, which has x lines of symmetry.','The tile shown is a regular polygon with x lines of symmetry.','Folding the regular polygon shown onto itself can be done along x different lines of symmetry.','A logo is shaped like the regular polygon shown, and it has x lines of symmetry.','The regular polygon in the figure has exactly x lines of symmetry.'][r.int(0,5)]+' Count its sides in the figure and find x. Write and solve an equation for x.',
  parts:[{answer:M('x='+n),check:{type:'solve',eq:'x='+n,v:'x'}}],steps:[step('A regular polygon has one line of symmetry through each vertex or side midpoint, and the number of lines equals the number of sides.',M('x='+n)),step('Solve for x.',M('x='+n))],space:[1.2,1.5,1.8]};}
function symRotation(ctx){var r=ctx.rng,ns=ctx.c>=5?[3,4,5,6,8,9,10,12]:[3,4,5,6,8],n=ns[r.int(0,ns.length-1)],x=360/n;
 return {variant:'geo-symmetry-rotation-'+ctx.c,fig:{kind:'geo-regular',n:n,plain:true},prompt:['The regular polygon shown is rotated about its center.','A turntable is shaped like the regular polygon shown and rotates about its center.','The tile shown is a regular polygon, and it is turned about its center.','A designer spins the regular polygon shown about its center.','The regular polygon in the figure is turned about its center.','A logo shaped like the regular polygon shown is rotated about its center.'][r.int(0,5)]+' Count its sides in the figure. Let x be the smallest positive rotation, in degrees, that maps the polygon onto itself. Find x.',
  parts:[{answer:M('x='+x),check:{type:'solve',eq:n+'*x=360',v:'x'}}],steps:[step('Equal turns of 360\u00b0 divided among the n sides give the smallest rotation that maps the polygon onto itself.',M(n+'*x=360')),step('Solve for x.',M('x='+x))],space:[1.2,1.5,1.8]};}
function dilateTri(ctx){var r=ctx.rng,k=r.int(2,ctx.c>=5?4:3),p=triPts(r,Math.min(5,Math.floor(14/k))),a=ask(r),u=p[a.v][a.co],x=k*u;
 return make('geo-transform-fig-dilate-'+ctx.c,triText(p)+' It is dilated about the origin with a scale factor of '+k+'. Find x, the '+a.cn+'-coordinate of '+a.L+'\u2032.','x='+k+'*'+u,x,'Multiply each coordinate by the scale factor.',triFig(p,null,[],'Triangle ABC on the coordinate plane'));}
function four(id,c,intro,rows){return {variant:id+'-'+c,prompt:intro,parts:rows.map(function(p,i){return {label:'abcd'[i],prompt:p[0],answer:M(p[1]+'='+p[2]),check:{type:'solve',eq:p[3],v:p[1]}};}),steps:rows.map(function(p){return step(p[4],M(p[3]));}),space:[2.6,3.2,3.9]};}

function ad(v,n){return v+(n<0?'-'+(-n):'+'+n);}
function transformInvestigation(ctx){var r=ctx.rng,c=ctx.c,a=nz(r),b=nz(r),h=nz(r),k=nz(r),x1=a+h,y1=b+k,x2=-x1,y2=y1,x3=-y2,y3=x2,s=r.int(2,c>=5?5:3),y4=s*y3,x4=s*x3;
 var o7=four('geo-transformations-investigation',c,'Open Response: Track point A('+a+', '+b+') through a sequence of transformations. Each part uses the image from the part before it.',[
 ['Translate A by '+h+' in the x-direction and '+k+' in the y-direction to get A′. Let x be the x-coordinate of A′. Find x.','x',x1,ad('x',-a)+'='+h,'Add the shift to the x-coordinate.'],
 ['Reflect A′ across the y-axis to get A″. Let y be the x-coordinate of A″. Find y.','y',x2,ad('y',x1)+'=0','A reflection across the y-axis changes the sign of x.'],
 ['Rotate A″ 90° counterclockwise about the origin to get A‴, using (x, y) → (−y, x). The y-coordinate of A″ is '+y2+'. Let z be the x-coordinate of A‴. Find z.','z',x3,ad('z',y2)+'=0','The new x-coordinate is the opposite of the old y-coordinate.'],
 ['Dilate A‴ by scale factor '+s+' about the origin. The y-coordinate of A‴ is '+y3+'. Let w be the y-coordinate of the image. Find w.','w',y4,'w='+s+'*'+(y3<0?'(0'+y3+')':y3),'A dilation multiplies each coordinate by the scale factor.']]);o7.fig={kind:'geo-grid',shapes:[{id:'pre',pts:[[a,b]],labels:['A('+mn(a)+', '+mn(b)+')']}],alt:'Coordinate plane with point A('+a+', '+b+')'};return o7;}

function pn(n){return n<0?'(0-'+(-n)+')':String(n);}
function pt2(a,b){return '('+mn(a)+', '+mn(b)+')';}
/* Honors chain 1: find a vertical mirror line from a point and its image, then use it. */
function invMirror(ctx){var r=ctx.rng,c=ctx.c,m=r.int(-4,4),a,b=nz(r),p;do{a=r.int(-8,8);}while(a===m||Math.abs(2*m-a)>10);p=2*m-a;
 var q,d,t=nz(r),u=nz(r);do{q=r.int(-8,8);}while(q===m||Math.abs(2*m-q)>10);d=2*m-q;var fx=d+t,fy=r.int(-6,6),dist=Math.abs(p-a);
 var o=four('geo-transformations-investigation-mirror',c,'Open Response: Point P'+pt2(a,b)+' is reflected across a vertical line x = m to the image P′'+pt2(p,b)+'. Each part uses the answer before it.',[
 ['Because the mirror line is halfway between P and P′, twice the x-coordinate of the line equals the sum of the two x-coordinates. Find m.','m',m,'2*m='+pn(a)+'+'+pn(p),'The line is the midpoint of the x-coordinates, so 2m equals their sum.'],
 ['Point Q'+pt2(q,fy)+' is reflected across the same line. Use the value of m from part a: the new x-coordinate x satisfies x + '+mn(q)+' = 2m. Find x.','x',d,'x+'+pn(q)+'=2*'+pn(m),'A point and its image add to twice the mirror value.'],
 ['Q′ is then translated '+Math.abs(t)+' units '+(t>0?'right':'left')+' and '+Math.abs(u)+' units '+(u>0?'up':'down')+'. The x-coordinate of Q′ is '+mn(d)+'. Find the final x-coordinate y.','y',fx,'y='+pn(d)+'+'+pn(t),'A translation adds the signed shift.'],
 ['The distance between P and P\u2032 is w. The mirror line is x = '+mn(m)+' and P has x-coordinate '+mn(a)+'. Twice the distance from P to the line is 2 times the difference of '+mn(Math.max(m,a))+' and '+mn(Math.min(m,a))+'. Find w.','w',dist,'w=2*('+pn(Math.max(m,a))+'-'+pn(Math.min(m,a))+')','The segment PP′ crosses the mirror at its midpoint, so its length is twice the distance from P to the line.']]);
 o.fig=ptFig(a,b);return o;}
/* Honors chain 2: dilation about a center other than the origin. */
function invDilCenter(ctx){var r=ctx.rng,c=ctx.c,s=r.int(2,c>=5?4:3),h=r.int(-5,5),k=r.int(-5,5),a,b=r.int(-6,6);do{a=r.int(-6,6);}while(a===h);
 var a2=h+s*(a-h),q,q2,len=r.int(2,6),area=r.int(3,9);do{q=r.int(-6,6);}while(q===h);q2=h+s*(q-h);var w=s*s*area,z=s*len;
 return four('geo-transformations-investigation-center',c,'Open Response: A dilation about the center C'+pt2(h,k)+' sends P'+pt2(a,b)+' to P′ whose x-coordinate is '+mn(a2)+'. Each part uses the answer before it.',[
 ['A dilation multiplies the horizontal distance from the center by the scale factor. Write '+mn(a2)+' − '+mn(h)+' = (scale factor)(' +mn(a)+' − '+mn(h)+'). Find the scale factor s.','s',s,'s*('+pn(a)+'-'+pn(h)+')='+pn(a2)+'-'+pn(h),'Distances from the center are multiplied by the scale factor.'],
 ['Point Q has x-coordinate '+mn(q)+'. Using the scale factor s from part a, its image has x-coordinate x = '+mn(h)+' + s('+mn(q)+' − '+mn(h)+'). Find x.','x',q2,'x='+pn(h)+'+'+s+'*('+pn(q)+'-'+pn(h)+')','Move from the center by s times the original horizontal distance.'],
 ['A segment with length '+len+' units is dilated by the same scale factor. Find the length z of its image.','z',z,'z='+s+'*'+len,'Lengths are multiplied by the scale factor.'],
 ['A region with area '+area+' square units is dilated by the same scale factor. Find the area w of its image.','w',w,'w='+s+'*'+s+'*'+area,'Areas are multiplied by the square of the scale factor.']]);}
/* Honors chain 3: a rotation then a translation, worked forwards and backwards. */
function invBackward(ctx){var r=ctx.rng,c=ctx.c,a=nz(r),b=nz(r),T=r.int(-6,6),U=r.int(-6,6),cx=-b+T,cy=a+U,e=nz(r),f=nz(r),ex=-f+T,gy=r.int(-8,8),gx=-gy+T;
 return four('geo-transformations-investigation-backward',c,'Open Response: Point A'+pt2(a,b)+' is rotated 90° counterclockwise about the origin, using (x, y) → (−y, x), and then translated to A″'+pt2(cx,cy)+'. Each part uses the answer before it.',[
 ['The rotation sends A to ('+mn(-b)+', '+mn(a)+'). The translation adds x to the x-coordinate. Find the horizontal shift x.','x',T,'x+'+pn(-b)+'='+pn(cx),'Final x-coordinate = rotated x-coordinate + horizontal shift.'],
 ['The translation also adds y to the y-coordinate. Find the vertical shift y.','y',U,'y+'+pn(a)+'='+pn(cy),'Final y-coordinate = rotated y-coordinate + vertical shift.'],
 ['Point B'+pt2(e,f)+' goes through the same rotation and then the same translation. Its rotated x-coordinate is '+mn(-f)+'. Using the horizontal shift from part a, find the final x-coordinate z.','z',ex,'z='+pn(-f)+'+'+pn(T),'Add the horizontal shift to the rotated x-coordinate.'],
 ['Point D goes through the same two steps and ends with x-coordinate '+mn(gx)+'. Using the horizontal shift '+mn(T)+', the rotation gives (− original y) + shift = '+mn(gx)+'. Find the original y-coordinate w of D.','w',gy,'0-w+'+pn(T)+'='+pn(gx),'Work backwards: undo the shift, then undo the rotation.']]);}
/* Honors chain 4: regular polygons, symmetry and angle measures (no figure). */
function invPolygonSym(ctx){var r=ctx.rng,c=ctx.c,ns=c>=5?[5,6,8,9,10,12,15]:[5,6,8,9,10,12],n=ns[r.int(0,ns.length-1)],d=360/n,S=(n-2)*180,v=S/n,sd=r.int(3,9),per=n*sd;
 return four('geo-transformations-investigation-symmetry',c,'Open Response: A regular polygon maps onto itself when rotated about its center by '+d+'°, and no smaller positive turn works. Each part uses the answer before it.',[
 ['The smallest turn times the number of sides is 360°. Find the number of sides n.','n',n,d+'*n=360','Equal turns around the center add up to 360°.'],
 ['Use the number of sides from part a. The interior angles of a polygon add up to (n − 2) · 180. Find the sum w.','w',S,'w=('+n+'-2)*180','The interior angle sum is (n − 2) times 180.'],
 ['Each interior angle of the regular polygon is equal. Using the sum '+S+' from part b and the number of sides '+n+', find the measure v of one interior angle.','v',v,n+'*v='+S,'Divide the angle sum equally among the n angles.'],
 ['Each side of the polygon is '+sd+' units long. Using the number of sides from part a, find the perimeter p.','p',per,'p='+n+'*'+sd,'Perimeter is the number of sides times the side length.']]);}

NS.registerSkillSet({id:'geometry-transformations',course:'geometry',courseName:'Geometry',unit:'transformations',unitName:'Transformations',title:'Coordinate Transformations',
tags:{INVEST:'Four-part transformation investigation',REFLECTION:'Reflections',TRANSLATION:'Translations',ROTATION:'Rotations',DILATION:'Dilations'},
reference:'<div class="mm-refgrid"><section><h4>Reflections</h4><p>x-axis: (x,y) → (x,−y); y-axis: (x,y) → (−x,y).</p></section><section><h4>90° rotations</h4><p>Clockwise: (x,y) → (y,−x); counterclockwise: (x,y) → (−y,x).</p></section></div>',
gaps:['Rigid-motion proofs and glide reflections are not generated.'],
skills:[
{id:'reflect-x-axis',tag:'REFLECTION',name:'Reflect over x-axis',best:[0,1],generate:ctx=>reflect(ctx,'x')},
{id:'reflect-y-axis',tag:'REFLECTION',name:'Reflect over y-axis',best:[0,1],generate:ctx=>reflect(ctx,'y')},
{id:'translate-horizontal',tag:'TRANSLATION',name:'Horizontal translation',best:[0,1],generate:ctx=>translate(ctx,'x')},
{id:'translate-vertical',tag:'TRANSLATION',name:'Vertical translation',best:[0,1],generate:ctx=>translate(ctx,'y')},
{id:'rotate-90-clockwise',tag:'ROTATION',name:'90° clockwise rotation',best:[0,1],generate:ctx=>rotate(ctx,'cw')},
{id:'rotate-90-counterclockwise',tag:'ROTATION',name:'90° counterclockwise rotation',best:[0,1],generate:ctx=>rotate(ctx,'ccw')},
{id:'dilate-origin',tag:'DILATION',name:'Dilation about origin',best:[0,1],generate:dilate},
{id:'translate-triangle-figure',tag:'TRANSLATION',name:'Translate a triangle (read from the grid)',best:[0,1],generate:translateTri},
{id:'reflect-triangle-figure',tag:'REFLECTION',name:'Reflect a triangle across a mirror line',best:[0,1],generate:reflectTri},
{id:'rotate-triangle-figure',tag:'ROTATION',name:'Rotate a triangle about the origin',best:[0,1],generate:rotateTri},
{id:'compose-triangle-figure',tag:'COMPOSITION',name:'Transform a triangle in two steps',best:[1,2],generate:composeTri},
{id:'symmetry-lines-regular',tag:'SYMMETRY',name:'Lines of symmetry of a regular polygon',best:[0,1],generate:symLines},
{id:'symmetry-rotation-regular',tag:'SYMMETRY',name:'Rotational symmetry of a regular polygon',best:[0,1],generate:symRotation},
{id:'dilate-triangle-figure',tag:'DILATION',name:'Dilate a triangle about the origin',best:[0,1],generate:dilateTri},
{id:'transformations-investigation-mirror',tag:'INVEST',name:'Honors: mirror line from a point and its image',best:[2],generate:invMirror},
{id:'transformations-investigation-center',tag:'INVEST',name:'Honors: dilation about a center that is not the origin',best:[2],generate:invDilCenter},
{id:'transformations-investigation-backward',tag:'INVEST',name:'Honors: rotation and translation worked backwards',best:[2],generate:invBackward},
{id:'transformations-investigation-symmetry',tag:'INVEST',name:'Honors: symmetry and angle measures of a regular polygon',best:[2],generate:invPolygonSym},
{id:'transformations-open-response-investigation',tag:'INVEST',name:'Four-part transformation sequence',best:[2],generate:transformInvestigation}
]});
})(typeof window!=='undefined'?window:globalThis);
