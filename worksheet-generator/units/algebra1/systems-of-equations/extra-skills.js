/* Systems of Equations: additional independent skill families. */
(function(G){'use strict';
var N=G.MKWS,T=N.tex,M=T.M,u='algebra1-systems-of-equations',unit=N.registry.units[u];if(!unit)return;
var groups=[
['Substitution & Rearranging',[['Substitute an isolated x variable','subX'],['Substitute an isolated y variable','subY'],['Rearrange before substitution','rearrange']]],
['Elimination Strategies',[['Eliminate by adding','add'],['Eliminate by subtracting','subtract'],['Multiply one equation before eliminating','scale'],['Multiply both equations before eliminating','bothScale']]],
['Graph Interpretation',[['Read the solution from a graph','read'],['Recognize parallel lines on a graph','parallel'],['Recognize coincident lines on a graph','same'],['Find a line equation from a graph','lineEq']]],
['Classifying & Checking',[['Check an ordered pair in both equations','check'],['Determine if a system is inconsistent','inconsistent'],['Determine if a system is dependent','dependent']]],
['Word Problems & Modeling',[['Ticket sales with two prices','tickets'],['Coins: nickels and dimes','coins'],['Two numbers given sum and difference','numbers'],['Two pricing plans at break-even','plans'],['Mixtures with two concentrations','mixture'],['Distance with opposite directions','distance']]]
];
function sign(v){return v<0?String(v):'+'+v}
function line(m,b){return {kind:'line',m:m,b:b}}
function renderPair(a,b,c,d,e,f){return '<div>'+M(T.eqStd(a,b,c))+'</div><div>'+M(T.eqStd(d,e,f))+'</div>'}
function build(type){return function(ctx){
var r=ctx.rng,x=r.int(-5,5),y=r.int(-5,5),a=r.int(2,5),b=r.int(1,5),c=r.int(1,5),p,ans,steps=[],fig=null,layout='half';
var result=function(pp,aa,st){p=pp;ans=aa;steps=st||['Substitute the solution into both equations to verify.']};
if(type==='subX'||type==='subY'||type==='rearrange'){
var v=type==='subX'?'x':'y',s=type==='subX'?x:y;
if(type==='subX')result('Solve by substitution: '+M('x=y'+sign(x-y))+' and '+M('2x+y='+(2*x+y)),M(T.pt(x,y)),['Replace x with y'+sign(x-y)+' in the second equation.','Solve for y, then back-substitute.']);
else if(type==='subY')result('Solve by substitution: '+M('y='+a+'x'+sign(y-a*x))+' and '+M('x+y='+(x+y)),M(T.pt(x,y)),['Replace y using the first equation.','Solve for x, then find y.']);
else result('Solve by substitution: '+renderPair(a,1,a*x+y,1,-1,x-y),M(T.pt(x,y)),['Isolate y in one equation, then substitute into the other.']);
}
else if(type==='add'||type==='subtract'||type==='scale'||type==='bothScale'){
if(type==='add')result('Solve by elimination: '+renderPair(a,b,a*x+b*y,-a,c,-a*x+c*y),M(T.pt(x,y)),['Add the two equations to eliminate x.','Solve for y, then back-substitute.']);
if(type==='subtract')result('Solve by elimination: '+renderPair(a,b,a*x+b*y,a,-c,a*x-c*y),M(T.pt(x,y)),['Subtract the equations to eliminate x.','Solve for y, then back-substitute.']);
if(type==='scale')result('Solve by elimination: '+renderPair(a,b,a*x+b*y,2*a,-c,2*a*x-c*y),M(T.pt(x,y)),['Multiply the first equation by -2, then add.','Solve and back-substitute.']);
if(type==='bothScale')result('Solve by elimination: '+renderPair(2,b,2*x+b*y,3,-c,3*x-c*y),M(T.pt(x,y)),['Multiply the first equation by 3 and the second by -2, then add.','Solve and back-substitute.']);
}
else if(['read','parallel','same','lineEq'].indexOf(type)>=0){
layout='row';
var m1=r.int(-3,3),m2=r.int(-3,3),k1=y-m1*x,k2=y-m2*x;N.gen.need(Math.abs(k1)<=9);
if(type==='read'){N.gen.need(m1!==m2&&Math.abs(k2)<=9);result('The two lines are already graphed. Name their intersection point.',M(T.pt(x,y)),['The solution is where the two lines cross.']);fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[line(m1,k1),line(m2,k2)],points:[]};}
if(type==='parallel'){var k3=k1+r.pick([-4,-3,-2,2,3,4]);N.gen.need(Math.abs(k3)<=9);result('How many solutions does this graphed system have? Explain.', 'No solution',['Parallel lines have equal slopes and different intercepts.']);fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[line(m1,k1),line(m1,k3)],points:[]};}
if(type==='same'){result('The graph shows two equations that coincide. How many solutions?', 'Infinitely many solutions',['Every point on the shared line satisfies both equations.']);fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[line(m1,k1),line(m1,k1)],points:[]};}
if(type==='lineEq'){result('Find the equation of the graphed line with y-intercept '+M(String(k1))+'.',M(T.eqSI(m1,k1)),['Read the slope from the grid and use the given intercept.']);fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[line(m1,k1)],points:[]};}
}
else if(['check','inconsistent','dependent'].indexOf(type)>=0){
if(type==='check'){result('Does '+M(T.pt(x,y))+' satisfy both equations? '+renderPair(a,b,a*x+b*y,a,-b,a*x-b*y),'Yes',['Substitution gives true statements in both equations.']);}
if(type==='inconsistent'){result('Classify this system: '+renderPair(a,b,a*x+b*y,2*a,2*b,2*(a*x+b*y)+c),'No solution',['The coefficients are proportional but the constants are not.']);}
if(type==='dependent'){result('Classify this system: '+renderPair(a,b,a*x+b*y,2*a,2*b,2*(a*x+b*y)),'Infinitely many solutions',['One equation is a multiple of the other.']);}
}
else{
layout='full';
if(type==='tickets'){var n=a+b,v=8*a+5*b;result('At a school event, adult tickets cost $8 and student tickets cost $5. '+n+' tickets brought in $'+v+'. Find the number of each.',a+' adult and '+b+' student',['Let x and y count the two ticket types.',M('x+y='+n),M('8x+5y='+v)]);}
if(type==='coins'){var total=a+b,value=5*a+10*b;result('A jar has '+total+' nickels and dimes worth '+value+' cents. How many of each coin are there?',a+' nickels and '+b+' dimes',['Let n be nickels and d be dimes.',M('n+d='+total),M('5n+10d='+value)]);}
if(type==='numbers'){result('Two numbers have sum '+(a+b)+' and difference '+(a-b)+'. Find both numbers.',a+' and '+b,['Let x and y represent the numbers.',M('x+y='+(a+b)),M('x-y='+(a-b))]);}
if(type==='plans'){var t=r.int(2,7),base1=10+a*t,base2=10,rate1=3,rate2=3+a;result('Plan A costs $'+base1+' plus $'+rate1+' per month. Plan B costs $'+base2+' plus $'+rate2+' per month. After how many months are costs equal?',t+' months',[M(base1+'+3t='+base2+'+'+(3+a)+'t')]);}
if(type==='mixture'){var n=a+b,amount=10*a+30*b;result('Mix '+n+' liters of solutions containing 10% and 30% salt to obtain '+amount/ n+'% salt. How many liters of each?',a+' L at 10% and '+b+' L at 30%',[M('x+y='+n),M('10x+30y='+amount)]);}
if(type==='distance'){var h=r.int(2,5),speed1=a*10,speed2=b*10;result('Two cyclists leave in opposite directions at '+speed1+' km/h and '+speed2+' km/h. They are '+((speed1+speed2)*h)+' km apart. How long have they ridden?',h+' hours',[M('('+speed1+'+'+speed2+')t='+((speed1+speed2)*h))]);}
}
return {prompt:p,answer:ans,steps:steps,fig:fig,figWhere:fig?'right':'none',key:type+'|'+p,equiv:type+'|'+p};
};}
var newCats=[];var n=10;
groups.forEach(function(group,gi){var ids=[];group[1].forEach(function(d){var id='sys-extra-'+d[1];N.registerLesson({id:id,unit:u,category:'more'+gi,num:++n,title:d[0],instruction:d[0],layout:['read','parallel','same','lineEq'].includes(d[1])?'row':'half',figWidth:3,space:[.5,.85,1.4],generate:build(d[1])});ids.push(id)});newCats.push({id:'more'+gi,letter:String.fromCharCode(70+gi),name:group[0],lessons:ids})});
unit.categories=unit.categories.concat(newCats);
})(typeof window!=='undefined'?window:globalThis);