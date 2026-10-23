/* Systems of Equations — shares the original Linear Functions engine and UI. */
(function(G){
'use strict';
var NS=G.MKWS,T=NS.tex,F=NS.frac.F,Fr=NS.frac.Fr;
var M=T.M,U='algebra1-systems-of-equations';
function pick(r,a){return a[r.int(0,a.length-1)];}
function coeff(ctx){return ctx.rng.int(ctx.difficulty==='honors'?-8:-5,ctx.difficulty==='honors'?8:5);}
function seed(ctx,mode){
 var r=ctx.rng,x=r.int(-6,6),y=r.int(-6,6),a,b,c,d,D;
 for(var i=0;i<100;i++){a=coeff(ctx);b=coeff(ctx);c=coeff(ctx);d=coeff(ctx);D=a*d-b*c;
 if(a&&b&&c&&d&&D&&Math.abs(D)>0)break;}
 NS.gen.need(a&&b&&c&&d&&D);
 if(mode==='none'){c=a;d=b;return {a:a,b:b,c:c,d:d,e:a*x+b*y,f:c*x+d*y+pick(r,[-6,-4,-2,2,4,6]),x:x,y:y,mode:mode};}
 if(mode==='infinite'){c=a*2;d=b*2;return {a:a,b:b,c:c,d:d,e:a*x+b*y,f:2*(a*x+b*y),x:x,y:y,mode:mode};}
 return {a:a,b:b,c:c,d:d,e:a*x+b*y,f:c*x+d*y,x:x,y:y,mode:'unique'};
}
function eq(a,b,c){return T.eqStd(a,b,c)}
function question(s){return '<div>'+M(eq(s.a,s.b,s.e))+'</div><div>'+M(eq(s.c,s.d,s.f))+'</div>';}
function verify(s){
 var det=s.a*s.d-s.b*s.c;
 if(s.mode==='unique') NS.gen.need(det!==0&&s.a*s.x+s.b*s.y===s.e&&s.c*s.x+s.d*s.y===s.f);
 else if(s.mode==='infinite') NS.gen.need(det===0&&s.c*s.e===s.a*s.f);
 else NS.gen.need(det===0&&s.c*s.e!==s.a*s.f);
}
function steps(s,method){
 if(s.mode==='none')return ['Both equations have proportional x- and y-coefficients, but different constants. The lines are parallel, so there is no solution.'];
 if(s.mode==='infinite')return ['The second equation is twice the first equation; the equations describe the same line, so there are infinitely many solutions.'];
 return ['Use '+method+' to solve the pair of equations.','Check in the first equation: '+M(T.lin([[s.a,'('+s.x+')'],[s.b,'('+s.y+')']])+'='+s.e)+'.','Check in the second equation: '+M(T.lin([[s.c,'('+s.x+')'],[s.d,'('+s.y+')']])+'='+s.f)+'.'];
}
function skillSystem(ctx,id,mode){
 var r=ctx.rng,x=r.int(-5,5),y=r.int(-5,5),a,b,c,d;
 if(id==='sys-substitution-easy'){a=1;b=0;c=r.int(2,5);d=r.int(1,5);Ncheck(d); }
 else if(id==='sys-substitution-standard'){a=r.int(2,5);b=r.int(2,5);c=r.int(2,5);d=r.int(2,5);Ncheck(a*d-b*c);}
 else if(id==='sys-elimination-add'){a=r.int(2,5);b=r.int(1,5);c=-a;d=r.int(1,5);Ncheck(b+d);}
 else if(id==='sys-elimination-multiply'){a=r.int(2,4);b=r.int(1,5);c=a*2;d=r.int(1,5);Ncheck(2*b-d);Ncheck(d-b);}
 else return seed(ctx,mode);
 var sys={a:a,b:b,c:c,d:d,e:a*x+b*y,f:c*x+d*y,x:x,y:y,mode:'unique'};
 verify(sys);return sys;
}
function Ncheck(value){NS.gen.need(value!==0);}
function reg(id,num,title,method,mode,layout){
 NS.registerLesson({id:id,unit:U,category:method,num:num,title:title,instruction:'Solve each system. Show your work.',layout:layout||'half',space:[1,1.7,2.5],generate:function(ctx){
 var s=skillSystem(ctx,id,mode||(id==='sys-classify'?pick(ctx.rng,['unique','none','infinite']):'unique'));verify(s);
 return {prompt:'Solve the system '+(method==='substitution'?'using substitution':method==='elimination'?'using elimination':'and classify the solution')+':'+question(s),answer:s.mode==='unique'?M(T.pt(s.x,s.y)):s.mode==='none'?'No solution':'Infinitely many solutions',steps:(id==='sys-elimination-add'?['Add the equations to eliminate x.',M((s.b+s.d)+'y='+(s.e+s.f)),M('y='+s.y),'Substitute to find '+M('x='+s.x)]:id==='sys-elimination-multiply'?['Multiply the first equation by -2, then add the second equation.',M((s.d-2*s.b)+'y='+(s.f-2*s.e)),M('y='+s.y),'Substitute to find '+M('x='+s.x)]:id==='sys-substitution-easy'?['The first equation already gives '+M('x='+s.x)+'.','Substitute into the second equation: '+M(s.c+'('+s.x+')+'+s.d+'y='+s.f),M('y='+s.y)]:steps(s,method)),key:id+'|'+[s.a,s.b,s.e,s.c,s.d,s.f].join('|'),equiv:id+'|'+s.x+'|'+s.y+'|'+s.mode};
 }});
}
reg('sys-substitution-easy',1,'Substitution: an isolated variable','substitution','unique');
reg('sys-substitution-standard',2,'Substitution: solve for a variable','substitution','unique');
reg('sys-elimination-add',3,'Elimination by adding or subtracting','elimination','unique');
reg('sys-elimination-multiply',4,'Elimination with multiplication','elimination','unique');
reg('sys-classify',5,'One, none, or infinitely many solutions','classification',null);
NS.registerLesson({id:'sys-word',unit:U,category:'applications',num:6,title:'Systems of equations word problems',instruction:'Define variables, write a system, and solve.',layout:'full',space:[1.1,2,2.7],generate:function(ctx){
 var r=ctx.rng,kind=r.int(0,4),a=r.int(5,18),b=r.int(4,16),p=r.int(8,16),q=r.int(2,7),n=a+b,v=p*a+q*b,prompt,what,unit1,unit2;
 NS.gen.need(p!==q);
 if(kind===0){prompt='At a school event, adult tickets cost $'+p+' and student tickets cost $'+q+'. A total of '+n+' tickets brought in $'+v+'. How many adult and student tickets were sold?';unit1='adult tickets';unit2='student tickets';}
 if(kind===1){prompt='A school store sells hoodies for $'+p+' and stickers for $'+q+'. It sold '+n+' items for $'+v+'. How many hoodies and stickers were sold?';unit1='hoodies';unit2='stickers';}
 if(kind===2){prompt='A theater sold '+n+' tickets. Reserved seats cost $'+p+' and general seats cost $'+q+'. The revenue was $'+v+'. How many tickets of each type were sold?';unit1='reserved tickets';unit2='general tickets';}
 if(kind===3){prompt='A fundraiser sold '+n+' items: mugs for $'+p+' and keychains for $'+q+'. Sales totaled $'+v+'. How many of each item were sold?';unit1='mugs';unit2='keychains';}
 if(kind===4){prompt='At a fair, meal vouchers cost $'+p+' and drink vouchers cost $'+q+'. A group bought '+n+' vouchers costing $'+v+'. How many of each voucher did they buy?';unit1='meal vouchers';unit2='drink vouchers';}
 return {prompt:prompt,answer:a+' '+unit1+' and '+b+' '+unit2,
 steps:['Let x be the number of '+unit1+' and y the number of '+unit2+'.',M('x+y='+n),M(p+'x+'+q+'y='+v),
 'Subtract '+M(q+'(x+y)='+q*n)+' from the revenue equation: '+M((p-q)+'x='+(v-q*n))+'.',
 'Thus '+M('x='+a)+' and '+M('y='+b)+'.',
 'Check: '+a+' + '+b+' = '+n+' and $'+(p*a)+' + $'+(q*b)+' = $'+v+'.'],
 key:'word|'+kind+'|'+n+'|'+v+'|'+p+'|'+q,equiv:'word|'+kind+'|'+a+'|'+b+'|'+p+'|'+q};
}});
/* Graphing tasks: construct two distinct lines through a lattice-point solution. */
NS.registerLesson({id:'sys-graph',unit:U,category:'graphing',num:7,title:'Solve a system by graphing',instruction:'Graph both lines and identify their intersection.',layout:'row',space:[.2,.4,.8],figWidth:3,generate:function(ctx){
 var r=ctx.rng,x=r.int(-4,4),y=r.int(-4,4),m1=pick(r,[-3,-2,-1,0,1,2,3]),m2=pick(r,[-3,-2,-1,0,1,2,3]);NS.gen.need(m1!==m2);
 var b1=y-m1*x,b2=y-m2*x;NS.gen.need(Math.abs(b1)<=10&&Math.abs(b2)<=10);
 var fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[],points:[]};
 if(ctx.grids)fig.lines=[];else fig=null;
 return {prompt:'Graph both equations and name their intersection:<div>'+M(T.eqSI(m1,b1))+'</div><div>'+M(T.eqSI(m2,b2))+'</div>',fig:fig,answer:M(T.pt(x,y)),steps:['The lines intersect at '+M(T.pt(x,y))+'.','Substitute the coordinates into both equations to verify.'],key:'sg|'+m1+'|'+b1+'|'+m2+'|'+b2,equiv:'sg|'+x+'|'+y+'|'+m1+'|'+m2};
 }});

function graphCase(ctx,kind){
 var r=ctx.rng, x=r.int(-4,4),y=r.int(-4,4), slopes=[-3,-2,-1,0,1,2,3],m=pick(r,slopes),n=pick(r,slopes),b1,b2,lines,ans,steps,signature;
 if(kind==='intersection'||kind==='classify-one'){NS.gen.need(m!==n);b1=y-m*x;b2=y-n*x;NS.gen.need(Math.abs(b1)<=9&&Math.abs(b2)<=9);
 lines=[{kind:'line',m:m,b:b1},{kind:'line',m:n,b:b2}];ans=kind==='intersection'?M(T.pt(x,y)):'One solution: '+M(T.pt(x,y));
 steps=['The lines intersect at '+M(T.pt(x,y))+'.'];signature=[m,b1,n,b2].join(',');}
 else if(kind==='parallel'){b1=r.int(-7,7);b2=r.int(-7,7);NS.gen.need(b1!==b2);
 lines=[{kind:'line',m:m,b:b1},{kind:'line',m:m,b:b2}];ans='No solution';
 steps=['The two lines are parallel and never intersect.'];signature=[m,b1,m,b2].join(',');}
 else {b1=r.int(-7,7);lines=[{kind:'line',m:m,b:b1},{kind:'line',m:m,b:b1}];ans='Infinitely many solutions';
 steps=['Both equations have the same graph, so every point on the line satisfies both.'];signature=[m,b1,m,b1].join(',');}
 return {fig:{xmin:-10,xmax:10,ymin:-10,ymax:10,lines:lines,points:[]},answer:ans,steps:steps,key:'graph-analysis|'+kind+'|'+signature,equiv:'graph-analysis|'+kind+'|'+signature};
}
NS.registerLesson({id:'sys-read-intersection',unit:U,category:'graphing',num:8,title:'Read the intersection from a graph',instruction:'Find the solution by inspecting two graphed lines.',layout:'row',figWidth:3,space:[.25,.5,.85],generate:function(ctx){
 var p=graphCase(ctx,'intersection');p.prompt='The two lines are already graphed. Write the ordered pair that solves the system.';return p;
}});
NS.registerLesson({id:'sys-read-solution-type',unit:U,category:'graphing',num:9,title:'Determine number of solutions from a graph',instruction:'Analyze the lines and justify your conclusion.',layout:'row',figWidth:3,space:[.5,.9,1.3],generate:function(ctx){
 var kind=pick(ctx.rng,['classify-one','parallel','same']);var p=graphCase(ctx,kind);p.prompt='Determine whether the graphed system has one solution, no solution, or infinitely many solutions. Explain your reasoning.';return p;
}});
NS.registerLesson({id:'sys-graph-match-equation',unit:U,category:'graphing',num:10,title:'Write an equation of a line shown in a system',instruction:'Read one line in the graph and write its equation.',layout:'row',figWidth:3,space:[.45,.75,1.1],generate:function(ctx){
 var r=ctx.rng,m=pick(r,[-3,-2,-1,0,1,2,3]),b=r.int(-6,6),n=pick(r,[-3,-2,-1,0,1,2,3]),c=r.int(-6,6);
 NS.gen.need(m!==n&&Math.abs(c-b)>=2);
 return {prompt:'Two lines are graphed. Find the equation of the line that crosses the y-axis at '+M(T.num(b))+'.',fig:{xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[{kind:'line',m:m,b:b},{kind:'line',m:n,b:c}],points:[]},answer:M(T.eqSI(m,b)),steps:['Read the y-intercept: '+M('b='+T.num(b))+'.','Count rise over run to find slope '+M('m='+T.num(m))+'.','Use '+M(T.eqSI(m,b))+'.'],key:'graph-equation|'+m+'|'+b+'|'+n+'|'+c,equiv:'graph-equation|'+m+'|'+b+'|'+n+'|'+c};
}});

NS.registerUnit({id:U,course:'Algebra 1',color:'blue',name:'Systems of Equations',defaultTitle:'Systems of Equations Practice',categories:[
{id:'substitution',letter:'A',name:'Substitution',lessons:['sys-substitution-easy','sys-substitution-standard']},
{id:'elimination',letter:'B',name:'Elimination',lessons:['sys-elimination-add','sys-elimination-multiply']},
{id:'graphing',letter:'C',name:'Graphing',lessons:['sys-graph','sys-read-intersection','sys-read-solution-type','sys-graph-match-equation']},
{id:'classification',letter:'D',name:'Types of Solutions',lessons:['sys-classify']},
{id:'applications',letter:'E',name:'Applications',lessons:['sys-word']}
]});
})(typeof window!=='undefined'?window:globalThis);