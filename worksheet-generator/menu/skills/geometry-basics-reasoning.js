/* Geometry Unit 1: foundational segment and angle measurements.
   Every answer is independently checked by the existing equation verifier. */
(function(G){
 'use strict';
 var NS=G.MKMENU,K=NS.kit,M=K.M,st=K.step;
 function question(ctx,kind){
  var r=ctx.rng,c=ctx.c,x=r.int(c<3?2:3,c<3?12:24),a=c>4?r.int(2,5):1,b=r.int(2,12),total=a*x+b;
  var eq=a===1?'x+'+b+'='+total:a+'x+'+b+'='+total;
  var text=kind==='segment'
    ? 'Point B lies between A and C on a straight segment. The sum of AB and BC equals AC. Find x by writing an equation. '
    : 'A ray divides a larger angle into two adjacent angles. Their measures add to the whole angle. Find x by writing an equation. ';
  return {variant:'geo-'+kind+'-'+c,prompt:text+M(eq)+'.',flashcardPrompt:text+' Set up and solve an equation to find x.',fig:kind==='segment'?{kind:'geo-segment',labels:['A','B','C'],measures:[(a===1?'x':a+'x'),String(b),String(total)],description:'Collinear points A, B, C with algebraic segment lengths'}:{kind:'geo-angle',labels:['A','B','C'],measures:[(a===1?'x':a+'x')+'°',b+'°',total+'°'],description:'Adjacent angles whose measures sum to the whole angle'},parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('Apply the '+(kind==='segment'?'segment addition postulate':'angle addition postulate')+'.',M(eq)),st('Subtract the known part, then divide by the coefficient.',M('x='+x))],space:[1,1.3,1.6]};
 }

 function midpoint(ctx){
  var r=ctx.rng,c=ctx.c,x=r.int(3,22),a=c>=5?r.int(2,4):1,b=r.int(1,10),left=a*x+b;
  var eq=(a===1?'x':a+'x')+'+'+b+'='+left;
  return {variant:'geo-midpoint-'+c,prompt:'B is the midpoint of segment AC, so AB = BC. Find x by writing and solving an equation.',fig:{kind:'geo-segment',labels:['A','B','C'],measures:[(a===1?'x':a+'x')+'+'+b,String(left),'AB = BC'],description:'B is midpoint of AC; two equal segments'},parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('A midpoint makes the adjacent segments congruent.',M(eq)),st('Solve the equation.',M('x='+x))],space:[1,1.3,1.6]};
 }
 function bisector(ctx){
  var r=ctx.rng,c=ctx.c,x=r.int(3,22),a=c>=5?r.int(2,4):1,b=r.int(1,10),side=a*x+b,eq=(a===1?'x':a+'x')+'+'+b+'='+side;
  return {variant:'geo-bisector-'+c,fig:{kind:'geo-angle',labels:['A','B','C'],measures:['('+(a===1?'x':a+'x')+'+'+b+')°',side+'°',''],mid:'D',equal:true,description:'Ray BD bisects angle ABC into two equal angles'},prompt:'Ray BD bisects angle ABC. Angle ABD measures '+M((a===1?'x':a+'x')+'+'+b)+' degrees, and angle DBC measures '+side+' degrees. Find x by writing and solving an equation.',parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],steps:[st('An angle bisector creates two equal angles.',M(eq)),st('Solve.',M('x='+x))],space:[1,1.3,1.6]};
 }

 function coordinateMidpoint(ctx){
  var r=ctx.rng,c=ctx.c,a=r.int(-12,10),x=r.int(-12,16),middle=(a+x)/2;
  // Use a whole-number midpoint by giving endpoint coordinates of equal parity.
  var off=0;while(!off)off=r.int(c>=5?-9:1,c>=5?9:12);x=a+2*off;
  middle=(a+x)/2;
  var eq='x+'+a+'='+2*middle;
  if(a<0)eq='x'+a+'='+2*middle;
  return {variant:'geo-coordinate-midpoint-'+c,
   fig:{kind:'geo-numline',pts:[{n:'A',v:a,l:String(a)},{n:'M',v:middle,l:String(middle)},{n:'B',v:x,l:'x'}],ticks:[['A','M'],['M','B']],description:'Number line: M is the midpoint of AB'},
   prompt:'On a number line, point A has coordinate '+a+' and point M is the midpoint of segment AB at coordinate '+middle+'. Point B has coordinate x. Find x by writing and solving an equation.',
   parts:[{answer:M('x='+x),check:{type:'solve',eq:eq,v:'x'}}],
   steps:[st('Twice the midpoint coordinate equals the sum of endpoint coordinates.',M(eq)),st('Solve for the missing endpoint.',M('x='+x))],
   space:[1,1.3,1.6]};
 }
 function distanceCoordinate(ctx){
  var r=ctx.rng,c=ctx.c,left=r.int(c>=4?-15:0,10),distance=r.int(2,c>=5?24:15),right=left+distance;
  var eq='x-'+left+'='+distance;
  if(left<0)eq='x+'+(-left)+'='+distance;
  return {variant:'geo-coordinate-distance-'+c,
    fig:{kind:'geo-numline',pts:[{n:'A',v:left,l:String(left)},{n:'B',v:right,l:'x'}],brackets:[{from:'A',to:'B',l:distance+' units'}],description:'Number line: A and B are '+distance+' units apart'},
    prompt:'Points A and B lie on a horizontal line at A = ('+left+', 3) and B = (x, 3). B lies to the right of A and AB = '+distance+' units. Find x by writing and solving an equation.',
    parts:[{answer:M('x='+right),check:{type:'solve',eq:eq,v:'x'}}],
    steps:[st('For points on a horizontal line, subtract their x-coordinates.',M(eq)),st('Solve for x.',M('x='+right))],
    space:[1,1.3,1.6]};
 }

 function coordinateInvestigation(ctx) {
   // Four connected, fully checked parts; no illustrative diagram is required.
   // Coordinate order A(0) < B(x) < C(t). Divisibility makes every midpoint integral.
   var r=ctx.rng,c=ctx.c,x=4*r.int(2,c>=5?25:20),b=4*r.int(2,c>=5?25:20),t=x+b;
   var m=x/2,n=(x+t)/2,w=(m+n)/2;
   var e1='x+'+b+'='+t,e2='2y='+x,e3='2z='+(x+t),e4='2w='+(m+n);
   return {
     variant:'geo-coordinate-investigation-'+c,
     fig:{kind:'geo-numline',pts:[{n:'A',v:0,l:'0'},{n:'B',v:x,l:'x'},{n:'C',v:t,l:String(t)}],brackets:[{from:'B',to:'C',l:b+' units'}],description:'Number line with points A, B and C in order'},
     prompt:'Four-part coordinate geometry investigation. Points A, B, and C lie in that order on a horizontal number line. A is at 0, B is at x, C is at '+t+', and BC is '+b+' units. For each part, use the stated geometric relationship and explain your calculation.',
     parts:[
       {label:'a',prompt:'Use segment addition to find coordinate x of B. Show the segment-addition equation.',answer:M('x='+x),check:{type:'solve',eq:e1,v:'x'}},
       {label:'b',prompt:'M is the midpoint of AB. Find its coordinate y using your result from (a).',answer:M('y='+m),check:{type:'solve',eq:e2,v:'y'}},
       {label:'c',prompt:'N is the midpoint of BC. Find its coordinate z: '+M(e3)+'.',answer:M('z='+n),check:{type:'solve',eq:e3,v:'z'}},
       {label:'d',prompt:'P is the midpoint of MN. Find its coordinate w: '+M(e4)+'.',answer:M('w='+w),check:{type:'solve',eq:e4,v:'w'}}
     ],
     steps:[st('Segment addition',M(e1)),st('Midpoint of AB',M(e2)),st('Midpoint of BC',M(e3)),st('Midpoint of MN',M(e4))],
     space:[2.8,3.5,4.3]
   };
 }

 /* ---------- Honors investigations (algebra and several relationships per problem) ----------
    Four-part chains; variants geo-basics-investigation-<name>-<c> use the shared investigation verifier. */
 function lin(a,b,v){var t=a===1?v:a+v;return b>0?t+'+'+b:b<0?t+'-'+(-b):t;}
 function cn(b){return b<0?'-'+(-b):'+'+b;}
 /* 1: segment addition and midpoints with algebraic lengths */
 function invSegment(ctx){
  var r=ctx.rng,c=ctx.c,tries=0,x,a1,b1,a2,b2,a3,b3,ab,bc,ac,ad,cd;
  do{x=r.int(3,c>=6?15:11);a1=r.int(1,4);b1=r.int(1,12);a2=r.int(1,4);b2=r.int(-4,10);ab=a1*x+b1;bc=a2*x+b2;ac=ab+bc;a3=a1+a2+r.int(1,3);b3=ac-a3*x;
   cd=r.int(4,20);ad=ac+cd;if(ad%2)ad+=1,cd+=1;tries++;}
  while((bc<3||Math.abs(b3)>40||a3===a1+a2)&&tries<5000);
  var eAB=lin(a1,b1,'x'),eBC=lin(a2,b2,'x'),eAC=lin(a3,b3,'x');
  return {variant:'geo-basics-investigation-segment-'+c,
   prompt:'Open Response: Points A, B, C, and D lie on a line in that order. AB = '+M(eAB)+', BC = '+M(eBC)+', and AC = '+M(eAC)+'. AD = '+ad+'. Name the relationship you use in every part and show the equation you write.',
   parts:[
    {label:'a',prompt:'Use segment addition to find x.',answer:M('x='+x),check:{type:'solve',eq:eAC+'=('+eAB+')+('+eBC+')',v:'x'}},
    {label:'b',prompt:'Find the length AC, using your value of x.',answer:M('w='+ac),check:{type:'solve',eq:'w='+a3+'*'+x+cn(b3),v:'w'}},
    {label:'c',prompt:'Find the length CD, using your answer to (b).',answer:M('v='+cd),check:{type:'solve',eq:'v='+ad+'-'+ac,v:'v'}},
    {label:'d',prompt:'N is the midpoint of AD. Find AN.',answer:M('u='+ad/2),check:{type:'solve',eq:'2*u='+ad,v:'u'}}
   ],
   steps:[st('Segment addition: AB + BC = AC, so '+M(eAC+'=('+eAB+')+('+eBC+')')+'.',M('x='+x)),st('Substitute x into AC.',M('w='+a3+'*'+x+cn(b3))),st('AC + CD = AD, so '+M('v='+ad+'-'+ac)+'.',M('v='+cd)),st('A midpoint splits AD into two equal parts, so '+M('2*u='+ad)+'.',M('u='+ad/2))],
   space:[3,3.6,4.2]};
 }
 /* 2: angle addition and an angle bisector with algebraic measures */
 function invAngle(ctx){
  var r=ctx.rng,c=ctx.c,tries=0,x,a1,b1,a2,b2,a3,b3,abd,dbc,abc,half,ebd;
  do{x=r.int(3,c>=6?15:11);a1=r.int(2,5);b1=r.int(-4,14);abd=a1*x+b1;a2=r.int(1,4);b2=r.int(-4,14);dbc=a2*x+b2;abc=abd+dbc;a3=a1+a2+r.int(1,3);b3=abc-a3*x;half=abc/2;ebd=abd-half;tries++;}
  while((abc%2||abc<50||abc>170||abd<=half+1||dbc<10||Math.abs(b3)>60||a3===a1+a2)&&tries<8000);
  var eABD=lin(a1,b1,'x'),eDBC=lin(a2,b2,'x'),eABC=lin(a3,b3,'x'),rad=Math.PI/180;
  var P={B:[0,0],A:[Math.cos(0),0],D:[Math.cos(abd*rad),Math.sin(abd*rad)],C:[Math.cos(abc*rad),Math.sin(abc*rad)]};
  var fig={kind:'geo-cong',pts:P,segs:[['B','A'],['B','D'],['B','C']],tris:null,sides:[],angles:[],right:[],angLab:[{p:'A',v:'B',q:'D',text:'('+eABD+')°'},{p:'D',v:'B',q:'C',text:'('+eDBC+')°'}],note:'Not drawn to scale.'};
  return {variant:'geo-basics-investigation-angle-'+c,fig:fig,
   prompt:'Open Response: Ray BD lies inside angle ABC. Angle ABD measures '+M('('+eABD+')')+' degrees, angle DBC measures '+M('('+eDBC+')')+' degrees, and angle ABC measures '+M('('+eABC+')')+' degrees. Ray BE bisects angle ABC. Name the relationship you use in every part and show the equation you write.',
   parts:[
    {label:'a',prompt:'Use angle addition to find x.',answer:M('x='+x),check:{type:'solve',eq:eABC+'=('+eABD+')+('+eDBC+')',v:'x'}},
    {label:'b',prompt:'Find the measure of angle ABC, using your value of x.',answer:M('w='+abc),check:{type:'solve',eq:'w='+a3+'*'+x+cn(b3),v:'w'}},
    {label:'c',prompt:'Ray BE bisects angle ABC. Find the measure of angle ABE.',answer:M('v='+half),check:{type:'solve',eq:'2*v='+abc,v:'v'}},
    {label:'d',prompt:'Ray BE lies inside angle ABD. Find the measure of angle EBD.',answer:M('u='+ebd),check:{type:'solve',eq:'u=('+a1+'*'+x+cn(b1)+')-'+half,v:'u'}}
   ],
   steps:[st('Angle addition: the parts add to the whole, so '+M(eABC+'=('+eABD+')+('+eDBC+')')+'.',M('x='+x)),st('Substitute x into angle ABC.',M('w='+a3+'*'+x+cn(b3))),st('A bisector splits the angle into two equal angles, so '+M('2*v='+abc)+'.',M('v='+half)),st('Angle EBD is angle ABD minus angle ABE, so '+M('u=('+a1+'*'+x+cn(b1)+')-'+half)+'.',M('u='+ebd))],
   space:[3,3.6,4.2]};
 }
 /* 3: coordinate plane: missing endpoint from a midpoint, then the length by the distance formula */
 function invCoordinate(ctx){
  var r=ctx.rng,c=ctx.c,T=[[3,4,5]],t=T[0],k=r.int(1,c>=5?2:1),sw=r.int(0,1),sx=r.int(0,1)?1:-1,sy=r.int(0,1)?1:-1;
  var dx=sx*2*t[sw]*k,dy=sy*2*t[1-sw]*k,len=2*t[2]*k,ax,ay,bx,by,mx,my,tr=0;
  do{ax=r.int(-6,6);ay=r.int(-3,3);bx=ax+dx;by=ay+dy;mx=(ax+bx)/2;my=(ay+by)/2;tr++;}while((Math.abs(ax)>10||Math.abs(mx)>10||Math.abs(ay)>5||Math.abs(my)>5)&&tr<3000);
  var Pt=function(q){return '('+q[0]+', '+q[1]+')';},sg=function(n){return n<0?'('+n+')':String(n);};
  var fig={kind:'geo-grid',shapes:[{id:'seg',pts:[[ax,ay],[mx,my]],labels:['A','M']}],lines:[],alt:'Coordinate plane with points A and M'};
  return {variant:'geo-basics-investigation-coordinate-'+c,fig:fig,
   prompt:'Open Response: Point A is at '+Pt([ax,ay])+' and M is at '+Pt([mx,my])+'. M is the midpoint of segment AB, and B is at (p, q). Show the formula you use in every part.',
   parts:[
    {label:'a',prompt:'Use the midpoint formula to find p, the x-coordinate of B.',answer:M('p='+bx),check:{type:'solve',eq:'p=2*'+sg(mx)+'-'+sg(ax),v:'p'}},
    {label:'b',prompt:'Find q, the y-coordinate of B.',answer:M('q='+by),check:{type:'solve',eq:'q=2*'+sg(my)+'-'+sg(ay),v:'q'}},
    {label:'c',prompt:'Use the distance formula to find the length AB, using your values of p and q.',answer:M('w='+len),check:{type:'solve',eq:'w^2=('+sg(bx)+'-'+sg(ax)+')*('+sg(bx)+'-'+sg(ax)+')+('+sg(by)+'-'+sg(ay)+')*('+sg(by)+'-'+sg(ay)+')',v:'w'}},
    {label:'d',prompt:'Find the length AM.',answer:M('v='+len/2),check:{type:'solve',eq:'2*v='+len,v:'v'}}
   ],
   steps:[st('The midpoint coordinate is the average of the endpoints, so '+M('p=2*'+sg(mx)+'-'+sg(ax))+'.',M('p='+bx)),st('Do the same for the y-coordinates: '+M('q=2*'+sg(my)+'-'+sg(ay))+'.',M('q='+by)),st('Distance formula: '+M('w^2=('+sg(bx)+'-'+sg(ax)+')*('+sg(bx)+'-'+sg(ax)+')+('+sg(by)+'-'+sg(ay)+')*('+sg(by)+'-'+sg(ay)+')')+'.',M('w='+len)),st('A midpoint splits AB into equal halves, so '+M('2*v='+len)+'.',M('v='+len/2))],
   space:[3,3.6,4.2]};
 }
 /* 4: intersecting lines: linear pair, vertical angles, bisector */
 function invLines(ctx){
  var r=ctx.rng,c=ctx.c,tries=0,x,a1,b1,a2,b2,aoc,boc,half;
  do{x=r.int(3,c>=6?20:16);a1=r.int(2,6);b1=r.int(-10,30);aoc=a1*x+b1;boc=180-aoc;a2=r.int(1,a1+2);b2=boc-a2*x;half=boc/2;tries++;}
  while((aoc<35||aoc>145||boc%2||a2===a1||Math.abs(b2)>70||tries<1)&&tries<8000);
  var eAOC=lin(a1,b1,'x'),eBOC=lin(a2,b2,'x'),rad=Math.PI/180;
  var P={O:[0,0],A:[-Math.cos(aoc*rad),-Math.sin(aoc*rad)],B:[1,0],C:[-1,0],D:[Math.cos(aoc*rad),Math.sin(aoc*rad)]};
  // line AB through O: B at angle 0, A opposite; line CD: D at angle aoc... re-label so angle AOC is aoc and angle BOC is the supplement
  var P2={O:[0,0],A:[1,0],B:[-1,0],C:[Math.cos(aoc*rad),Math.sin(aoc*rad)],D:[-Math.cos(aoc*rad),-Math.sin(aoc*rad)]};
  var fig={kind:'geo-cong',pts:P2,segs:[['A','B'],['C','D']],tris:null,sides:[],angles:[],right:[],angLab:[{p:'A',v:'O',q:'C',text:'('+eAOC+')°'},{p:'B',v:'O',q:'C',text:'('+eBOC+')°'}],note:'Not drawn to scale.'};
  return {variant:'geo-basics-investigation-lines-'+c,fig:fig,
   prompt:'Open Response: Lines AB and CD intersect at point O. Angle AOC measures '+M('('+eAOC+')')+' degrees and angle BOC measures '+M('('+eBOC+')')+' degrees. Ray OE bisects angle BOC. Name the relationship you use in every part and show the equation you write.',
   parts:[
    {label:'a',prompt:'Angles AOC and BOC form a linear pair. Find x.',answer:M('x='+x),check:{type:'solve',eq:'('+eAOC+')+('+eBOC+')=180',v:'x'}},
    {label:'b',prompt:'Angle BOD is vertical to angle AOC. Find the measure of angle BOD.',answer:M('w='+aoc),check:{type:'solve',eq:'w='+a1+'*'+x+cn(b1),v:'w'}},
    {label:'c',prompt:'Find the measure of angle BOC, using your value of x.',answer:M('v='+boc),check:{type:'solve',eq:'v='+a2+'*'+x+cn(b2),v:'v'}},
    {label:'d',prompt:'Ray OE bisects angle BOC. Find the measure of angle BOE.',answer:M('u='+half),check:{type:'solve',eq:'2*u='+boc,v:'u'}}
   ],
   steps:[st('A linear pair adds to 180, so '+M('('+eAOC+')+('+eBOC+')=180')+'.',M('x='+x)),st('Vertical angles are congruent, so angle BOD equals angle AOC: '+M('w='+a1+'*'+x+cn(b1))+'.',M('w='+aoc)),st('Substitute x into angle BOC.',M('v='+a2+'*'+x+cn(b2))),st('A bisector splits the angle into two equal angles, so '+M('2*u='+boc)+'.',M('u='+half))],
   space:[3,3.6,4.2]};
 }

 /* ---- coverage additions: reading a protractor, conditional statements, undefined terms and postulates, constructions ---- */
 function protractor(ctx){var r=ctx.rng,c=ctx.c,a,b,m;
  a=c<=2?0:5*r.int(0,30);b=5*r.int(1,36);if(c<=2&&r.next()<0.5){a=180;}m=Math.abs(a-b);K.need(a!==b&&m>=10);
  var cls=c>=3&&r.next()<0.35,kind=m<90?'acute':m===90?'right':m<180?'obtuse':'straight';
  var fig={kind:'geo-protractor',a:a,b:b};
  if(cls)return {variant:'geo-protractor-classify-'+c,prompt:'Use the protractor to find m∠AOB. Classify ∠AOB as acute, right, obtuse, or straight.',fig:fig,
   parts:[{answer:kind.charAt(0).toUpperCase()+kind.slice(1)+' ('+m+'°)',check:{type:'derive',kind:'protractor',alts:['acute','right','obtuse','straight'].filter(function(k){return k!==kind;}).map(function(k){return k.charAt(0).toUpperCase()+k.slice(1)+' ('+m+'°)';})}}],
   steps:[st('Read both rays on the same scale: '+a+'° and '+b+'°.'),st('Subtract: |'+b+' − '+a+'| = '+m+'°, so the angle is '+kind+'.')],space:[0.6,0.7,0.8]};
  return {variant:'geo-protractor-read-'+c,prompt:'Use the protractor to find m∠AOB.',fig:fig,
   parts:[{answer:M(String(m))+'°',check:{type:'derive',kind:'protractor',alts:[M(String(180-m>0?180-m:m+10))+'°',M(String(b))+'°',M(String(a+b<=180?a+b:m+5))+'°'].filter(function(z){return z!==M(String(m))+'°';})}}],
   steps:[st('Ray OA crosses the scale at '+a+'° and ray OB at '+b+'° (same scale).'),st('The angle is the difference: |'+b+' − '+a+'| = '+m+'°.')],space:[0.6,0.7,0.8]};}
 var CONDS=[['a quadrilateral is a square','it is a rectangle',false],['an angle is a right angle','its measure is 90°',true],['a triangle is equilateral','it is isosceles',false],['two angles are vertical angles','they are congruent',false],
  ['a number is divisible by 4','it is even',false],['a polygon is a triangle','it has three sides',true],['a quadrilateral is a rectangle','its diagonals are congruent',false],['two lines are perpendicular','they form right angles',true],
  ['an animal is a dog','it is a mammal',false],['a figure is a rhombus','its sides are all congruent',true],['an angle is obtuse','its measure is greater than 90° and less than 180°',true],['a point is the midpoint of a segment','it divides the segment into two congruent segments',true],
  ['a number is a multiple of 10','it is a multiple of 5',false],['a polygon is a hexagon','it has six sides',true],['an angle is acute','its measure is less than 90°',true],['a quadrilateral is a parallelogram','its opposite sides are parallel',true],['a triangle is a right triangle','it has one right angle',true]];
 function neg(cl){return cl.replace(/^(.*?)\b(is|are)\b/,'$1$2 not').replace(/^(it|they) has /,'$1 does not have ').replace(/^(.*?)\b(has)\b/,'$1does not have').replace(/\b(form|divides)\b/,function(w){return w==='form'?'do not form':'does not divide';});}
 function cond(ctx){var r=ctx.rng,c=ctx.c,cd=r.pick(CONDS),P=cd[0],Q=cd[1],stmt='If '+P+', then '+Q+'.';
  var ok=function(x){return / not\b/.test(x)&&!/ not .* not /.test(x);};K.need(ok(neg(P))&&ok(neg(Q)));
  var F={converse:'If '+Q+', then '+P+'.',inverse:'If '+neg(P)+', then '+neg(Q)+'.',contrapositive:'If '+neg(Q)+', then '+neg(P)+'.'};
  var kinds=c<=1?['converse','identify']:c<=2?['converse','identify','inverse']:c<=4?['converse','inverse','contrapositive','identify']:['contrapositive','inverse','identify','truth'].concat(cd[2]?['bicond']:[]),k=r.pick(kinds),lead='Statement: '+stmt+' ';
  if(k==='identify'){var f=r.pick(c<=2?['converse']:['converse','inverse','contrapositive']);if(c<=2&&r.next()<0.5)f='converse';
   return {variant:'geo-cond-identify-'+f+'-'+c,prompt:lead+'Which form of the statement is "'+F[f]+'"?',parts:[{answer:f.charAt(0).toUpperCase()+f.slice(1),check:{type:'derive',kind:'conditional',alts:['Converse','Inverse','Contrapositive','Biconditional'].filter(function(x){return x.toLowerCase()!==f;})}}],
    steps:[st('Converse: switch the hypothesis and conclusion. Inverse: negate both. Contrapositive: switch and negate both.'),st('This is the '+f+'.')],space:[0.5,0.6,0.7]};}
  if(k==='truth'){var sT=true,cT=cd[2],ask=r.pick(['inverse','contrapositive']),truth=ask==='contrapositive'?sT:cT;
   return {variant:'geo-cond-truth-'+ask+'-'+c,prompt:lead+'The statement is '+(sT?'true':'false')+' and its converse is '+(cT?'true':'false')+'. Is its '+ask+' true or false?',
    parts:[{answer:(truth?'True':'False')+': the '+ask+' has the same truth value as the '+(ask==='contrapositive'?'statement':'converse')+'.',check:{type:'derive',kind:'conditional',alts:[(truth?'False':'True')+': the '+ask+' has the opposite truth value.']}}],
    steps:[st('A statement and its contrapositive are logically equivalent; so are the converse and the inverse.'),st('The '+ask+' is '+(truth?'true':'false')+'.')],space:[0.6,0.7,0.8]};}
  if(k==='bicond'){var bi=P.charAt(0).toUpperCase()+P.slice(1)+' if and only if '+Q+'.';
   return {variant:'geo-cond-bicond-'+c,prompt:lead+'Both the statement and its converse are true. Write them together as a biconditional.',parts:[{answer:bi,check:{type:'derive',kind:'conditional'}}],
    steps:[st('A biconditional joins a true statement and its true converse with “if and only if”.'),st(bi)],space:[0.7,0.8,0.9]};}
  return {variant:'geo-cond-write-'+k+'-'+c,prompt:lead+'Write the '+k+'.',parts:[{answer:F[k],check:{type:'derive',kind:'conditional',alts:Object.keys(F).filter(function(x){return x!==k;}).map(function(x){return F[x];}).concat([stmt])}}],
   steps:[st(k==='converse'?'Switch the hypothesis and the conclusion.':k==='inverse'?'Negate both the hypothesis and the conclusion.':'Switch the hypothesis and the conclusion, and negate both.'),st(F[k])],space:[0.7,0.8,0.9]};}
 var TERM_BANK=[[1,"Points {P} and {Q} are distinct. How many lines pass through both of them?","Exactly one","Two","None","Infinitely many"],[1,"Planes {P} and {Q} are distinct and intersect. What is their intersection?","A line","A point","A plane","A segment"],[1,"Lines {P}{Q} and {R}{S} are distinct and intersect. What is their intersection?","A point","A line","A plane","A ray"],[2,"Which three terms are left undefined in geometry?","Point, line, and plane","Point, segment, and ray","Line, angle, and plane","Segment, ray, and angle"],[3,"Points {P}, {Q}, and {R} do not lie on one line. How many planes pass through all three?","Exactly one","Two","Three","Infinitely many"],[1,"How many endpoints does ray {P}{Q} have?","One","Two","None","Three"],[1,"How many endpoints does segment {P}{Q} have?","Two","One","None","Three"],[1,"How many endpoints does line {P}{Q} have?","None","One","Two","Infinitely many"],[2,"Points {P}, {Q}, and {R} lie on the same line. What are they called?","Collinear","Coplanar","Congruent","Parallel"],[2,"Points {P}, {Q}, {R}, and {S} lie in the same plane. What are they called?","Coplanar","Collinear","Concurrent","Congruent"],[3,"{Q} is between {P} and {R}, so {P}{Q} + {Q}{R} = {P}{R}. Which postulate is this?","Segment Addition Postulate","Angle Addition Postulate","Ruler Postulate","Midpoint Postulate"],[3,"{S} is in the interior of ∠{P}{Q}{R}, so m∠{P}{Q}{S} + m∠{S}{Q}{R} = m∠{P}{Q}{R}. Which postulate is this?","Angle Addition Postulate","Segment Addition Postulate","Protractor Postulate","Linear Pair Postulate"],[1,"{M} divides segment {P}{Q} into two congruent segments. What is {M} called?","The midpoint of the segment","A bisecting ray","A vertex","An endpoint"],[2,"Ray {Q}{S} divides ∠{P}{Q}{R} into two congruent angles. What is ray {Q}{S} called?","The angle bisector","A midpoint","A perpendicular bisector","An opposite ray"],[1,"The measures of ∠{P} and ∠{Q} add to 90°. What are the two angles called?","Complementary angles","Supplementary angles","Vertical angles","Adjacent angles"],[1,"The measures of ∠{P} and ∠{Q} add to 180°. What are the two angles called?","Supplementary angles","Complementary angles","Vertical angles","Congruent angles"],[2,"∠{P}{Q}{S} and ∠{S}{Q}{R} are adjacent, and rays {Q}{P} and {Q}{R} are opposite rays. What do the two angles form?","A linear pair","Vertical angles","Complementary angles","An angle bisector"],[1,"Which figure extends without end in exactly one direction?","A ray","A line","A segment","A plane"],[2,"Lines {P}{Q} and {R}{S} meet to form right angles. What are they called?","Perpendicular lines","Parallel lines","Skew lines","Collinear lines"],[2,"Lines {P}{Q} and {R}{S} lie in the same plane and never intersect. What are they called?","Parallel lines","Skew lines","Perpendicular lines","Intersecting lines"],[4,"Lines {P}{Q} and {R}{S} do not lie in the same plane and never intersect. What are they called?","Skew lines","Parallel lines","Perpendicular lines","Coplanar lines"]];
 var CONST_BANK=[[3,"Segment {P}{Q} is drawn. Arcs of the same radius are drawn from {P} and from {Q}, and a line is drawn through the two points where the arcs cross. Which construction is this?","The perpendicular bisector of the segment","An angle bisector","A copy of an angle","An equilateral triangle"],[3,"An arc centered at the vertex {Q} of ∠{P}{Q}{R} crosses both sides. Equal arcs are drawn from those two crossing points, and a ray is drawn from {Q} through where they meet. Which construction is this?","The angle bisector","The perpendicular bisector of a segment","A copy of a segment","A parallel line"],[2,"The compass is opened to the length of segment {P}{Q}. Keeping that opening, an arc is drawn from {R} on a ray to mark point {S}. Which construction is this?","Copying a segment","Bisecting an angle","Copying an angle","Constructing a regular hexagon"],[5,"Point {P} is on line ℓ. Arcs from {P} mark two points on ℓ; equal arcs from those points cross above {P} at {Q}, and line {P}{Q} is drawn. Which construction is this?","The perpendicular to ℓ through a point on ℓ","An angle bisector","A parallel line through a point","Copying a segment"],[5,"Point {P} is not on line ℓ. A line through {P} crosses ℓ, and the angle it makes with ℓ is copied at {P} as a corresponding angle. Which construction is this?","A line through the point parallel to ℓ","A perpendicular bisector","An angle bisector","An equilateral triangle"],[4,"The compass is set to the length of segment {P}{Q}. Arcs are drawn from {P} and from {Q}; they cross at {R}, and {R} is joined to {P} and {Q}. Which construction is this?","An equilateral triangle","A perpendicular bisector","A regular hexagon","A copy of an angle"],[6,"A circle with center {O} is drawn. Keeping the same compass opening, the radius is marked off six times around the circle and consecutive marks are joined. Which construction is this?","A regular hexagon inscribed in the circle","An equilateral triangle","A square inscribed in the circle","A perpendicular bisector"],[1,"In a construction of segment {P}{Q}, which tool draws arcs and transfers lengths?","The compass","The straightedge","The protractor","The ruler"],[1,"In a construction of segment {P}{Q}, which tool draws lines and segments without measuring?","The straightedge","The compass","The protractor","The ruler"],[6,"The perpendicular bisectors of the sides of △{P}{Q}{R} are constructed. Their intersection is the center of which circle?","The circumscribed circle (circumcircle)","The inscribed circle (incircle)","A circle through the midpoints only","The unit circle"],[6,"The angle bisectors of △{P}{Q}{R} are constructed. Their intersection is the center of which circle?","The inscribed circle (incircle)","The circumscribed circle (circumcircle)","A circle through the vertices","The unit circle"]];
 function bankSkill(bank,tag){return function(ctx){var r=ctx.rng,c=ctx.c,pool=bank.filter(function(b){return b[0]<=c;});K.need(pool.length);var b=r.pick(pool),L=r.shuffle('ABCDEFGHJKLNPQRSTUVWXYZ'.split('')),i=0,map={};
  var q=b[1].replace(/\{([A-Z])\}/g,function(w,k){if(!map[k])map[k]=L[i++];return map[k];});
  return {variant:'geo-'+tag+'-'+bank.indexOf(b)+'-'+c,prompt:q,parts:[{answer:b[2],check:{type:'derive',kind:'term',alts:b.slice(3)}}],steps:[st('Answer: '+b[2]+'.')],space:[0.4,0.5,0.6]};};}
 NS.registerSkillSet({id:'geometry-basics-reasoning',course:'geometry',courseName:'Geometry',unit:'basics-reasoning',unitName:'Foundations of Geometry',title:'Geometry Foundations',
 tags:{LOGIC:'Conditional statements',TERMS:'Terms, postulates and constructions',SEGMENT:'Segment addition and lengths',ANGLE:'Angle addition and measures',MIDPOINT:'Midpoints',BISECTOR:'Angle bisectors',COORD:'Coordinate geometry'},
 reference:'<div class="mm-refgrid"><section><h4>Segment addition</h4><p>When B is between A and C, AB + BC = AC.</p></section><section><h4>Angle addition</h4><p>Adjacent angles add to the measure of their whole angle.</p></section></div>',
 gaps:['Students do not carry out compass-and-straightedge constructions here: construction steps and tools are asked in words, and drawing is left to class. Formal proofs begin in Unit 2.'],skills:[
 {id:'protractor-reading',tag:'ANGLE',name:'Measure and classify angles with a protractor',best:[0,1],generate:ctx=>K.retry(()=>protractor(ctx))},
 {id:'conditional-statements',tag:'LOGIC',name:'Conditional statements: converse, inverse, contrapositive, biconditional',best:[0,1,2],generate:ctx=>K.retry(()=>cond(ctx))},
 {id:'undefined-terms-postulates',tag:'TERMS',name:'Undefined terms, definitions and postulates',best:[0,1],generate:ctx=>K.retry(()=>bankSkill(TERM_BANK,'terms')(ctx))},
 {id:'constructions-concepts',tag:'TERMS',name:'Constructions: tools and steps',best:[0,1,2],generate:ctx=>K.retry(()=>bankSkill(CONST_BANK,'constructions')(ctx))},
 {id:'segment-addition',tag:'SEGMENT',name:'Find missing segment length',best:[0,1],generate:ctx=>question(ctx,'segment')},
 {id:'angle-addition',tag:'ANGLE',name:'Find missing angle measure',best:[0,1],generate:ctx=>question(ctx,'angle')},
 {id:'midpoint',tag:'MIDPOINT',name:'Midpoint and equal segments',best:[0,1],generate:midpoint},
 {id:'angle-bisector',tag:'BISECTOR',name:'Angle bisectors',best:[0,1],generate:bisector},
 {id:'coordinate-midpoint',tag:'COORD',name:'Midpoint with missing endpoint coordinate',best:[0,1],generate:coordinateMidpoint},
 {id:'coordinate-distance',tag:'COORD',name:'Horizontal distance and missing coordinate',best:[0,1],generate:distanceCoordinate},
 {id:'basics-investigation-segment',tag:'COORD',name:'Honors: segment addition and midpoints with algebra',best:[2],generate:invSegment},
 {id:'basics-investigation-angle',tag:'ANGLE',name:'Honors: angle addition and bisectors with algebra',best:[2],generate:invAngle},
 {id:'basics-investigation-coordinate',tag:'COORD',name:'Honors: midpoint and distance formulas on the coordinate plane',best:[2],generate:invCoordinate},
 {id:'basics-investigation-lines',tag:'ANGLE',name:'Honors: linear pairs, vertical angles and a bisector',best:[2],generate:invLines},
 {id:'coordinate-investigation',tag:'COORD',name:'Four-part coordinate midpoint investigation',best:[2],generate:coordinateInvestigation}
 ]});
})(typeof window!=='undefined'?window:globalThis);
