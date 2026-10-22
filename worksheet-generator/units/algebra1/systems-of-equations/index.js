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
function reg(id,num,title,method,mode,layout){
 NS.registerLesson({id:id,unit:U,category:method,num:num,title:title,instruction:'Solve each system. Show your work.',layout:layout||'half',space:[1,1.7,2.5],generate:function(ctx){
 var s=seed(ctx,mode||(ctx.rng.chance(.08)?pick(ctx.rng,['none','infinite']):'unique'));verify(s);
 return {prompt:'Solve the system '+(method==='graphing'?'by graphing':method==='substitution'?'using substitution':method==='elimination'?'using elimination':'and classify the solution')+':'+question(s),answer:s.mode==='unique'?M(T.pt(s.x,s.y)):s.mode==='none'?'No solution':'Infinitely many solutions',steps:steps(s,method),key:id+'|'+[s.a,s.b,s.e,s.c,s.d,s.f].join('|'),equiv:id+'|'+s.x+'|'+s.y+'|'+s.mode};
 }});
}
reg('sys-substitution-easy',1,'Substitution: an isolated variable','substitution','unique');
reg('sys-substitution-standard',2,'Substitution: solve for a variable','substitution','unique');
reg('sys-elimination-add',3,'Elimination by adding or subtracting','elimination','unique');
reg('sys-elimination-multiply',4,'Elimination with multiplication','elimination','unique');
reg('sys-classify',5,'One, none, or infinitely many solutions','classification',null);
NS.registerLesson({id:'sys-word',unit:U,category:'applications',num:6,title:'Ticket sales word problems',instruction:'Write and solve a system of equations.',layout:'full',space:[1.1,2,2.7],generate:function(ctx){
var r=ctx.rng,a=r.int(5,20),s=r.int(4,16),pa=r.int(8,15),ps=r.int(3,7),n=a+s,v=a*pa+s*ps;
return {prompt:'Adult tickets cost '+pa+' dollars and student tickets cost '+ps+' dollars. A total of '+n+' tickets brought in '+v+' dollars. How many of each were sold?',answer:'Adults: '+a+', students: '+s,steps:['Let a represent adult tickets and s represent student tickets.',M('a+s='+n),M(pa+'a+'+ps+'s='+v),'The solution is '+M(T.pt(a,s))+'.'],key:'word|'+n+'|'+v+'|'+pa+'|'+ps,equiv:'word|'+a+'|'+s+'|'+pa+'|'+ps};
}});
/* Graphing tasks: construct two distinct lines through a lattice-point solution. */
NS.registerLesson({id:'sys-graph',unit:U,category:'graphing',num:7,title:'Solve a system by graphing',instruction:'Graph both lines and identify their intersection.',layout:'row',space:[.2,.4,.8],figWidth:3,generate:function(ctx){
 var r=ctx.rng,x=r.int(-4,4),y=r.int(-4,4),m1=pick(r,[-3,-2,-1,0,1,2,3]),m2=pick(r,[-3,-2,-1,0,1,2,3]);NS.gen.need(m1!==m2);
 var b1=y-m1*x,b2=y-m2*x;NS.gen.need(Math.abs(b1)<=10&&Math.abs(b2)<=10);
 var fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[],points:[]};
 if(ctx.grids)fig.lines=[];else fig=null;
 return {prompt:'Graph both equations and name their intersection:<div>'+M(T.eqSI(m1,b1))+'</div><div>'+M(T.eqSI(m2,b2))+'</div>',fig:fig,answer:M(T.pt(x,y)),steps:['The lines intersect at '+M(T.pt(x,y))+'.','Substitute the coordinates into both equations to verify.'],key:'sg|'+m1+'|'+b1+'|'+m2+'|'+b2,equiv:'sg|'+x+'|'+y+'|'+m1+'|'+m2};
 }});
NS.registerUnit({id:U,course:'Algebra 1',color:'blue',name:'Systems of Equations',defaultTitle:'Systems of Equations Practice',categories:[
{id:'substitution',letter:'A',name:'Substitution',lessons:['sys-substitution-easy','sys-substitution-standard']},
{id:'elimination',letter:'B',name:'Elimination',lessons:['sys-elimination-add','sys-elimination-multiply']},
{id:'graphing',letter:'C',name:'Graphing',lessons:['sys-graph']},
{id:'classification',letter:'D',name:'Types of Solutions',lessons:['sys-classify']},
{id:'applications',letter:'E',name:'Applications',lessons:['sys-word']}
]});
})(typeof window!=='undefined'?window:globalThis);