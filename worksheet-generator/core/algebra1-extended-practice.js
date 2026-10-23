(function(G){'use strict';var N=G.MKWS,T=N.tex,M=T.M,u=document.body.getAttribute('data-unit'),unit=N.registry.units[u];if(!unit)return;var titles={"expressions-equations":["Evaluate expressions with negative inputs","Simplify expressions with two variables","Distribute a negative coefficient","Solve equations requiring distribution","Solve multi-step equations","Solve equations with decimals","Solve proportions by cross-multiplication","Solve unit-rate applications","Write equations from word problems","Solve age word problems","Identify infinitely many solutions","Rearrange a literal equation"],"inequalities":["Graph greater-than inequalities on a number line","Graph less-than-or-equal inequalities on a number line","Write an inequality from a number-line graph","Open versus closed endpoint","Solve and graph two-step inequalities","Solve negative-coefficient inequalities","Graph compound AND inequalities","Graph compound OR inequalities","Solve absolute-value less-than inequalities","Solve absolute-value greater-than inequalities","Check a proposed solution","Inequality word problems"],"graphing-inequalities":["Graph a dashed rising boundary","Graph a dashed falling boundary","Graph a solid rising boundary","Graph a solid falling boundary","Graph horizontal inequalities","Graph vertical inequalities","Identify shading above a boundary","Identify shading below a boundary","Read inequality from a graphed dashed line","Read inequality from a graphed solid line","Test a point in a shaded region","Compare dashed and solid boundaries"],"exponents-exponential-functions":["Evaluate products of powers","Simplify powers of products","Simplify powers of quotients","Use zero exponent in a quotient","Simplify negative exponents","Evaluate fractional-base exponents","Write scientific notation","Multiply scientific notation","Classify exponential growth","Classify exponential decay","Find an exponential growth value","Find an exponential decay value"],"polynomials-factoring":["Classify polynomials by degree","Find the leading coefficient","Add polynomial expressions","Subtract polynomial expressions","Multiply monomials","Multiply a monomial and binomial","Multiply two binomials","Factor out the GCF","Factor monic trinomials","Factor nonmonic trinomials","Factor a difference of squares","Solve equations using zero-product property"],"quadratics":["Identify vertex form parameters","Find axis of symmetry from standard form","Evaluate a quadratic function","Create a quadratic table value","Find roots from factored form","Find x-intercepts from factored form","Solve by square roots","Solve by factoring","Find discriminant","Determine number of real roots","Interpret a projectile maximum height","Find a break-even quadratic root"]},short=u.slice(9),names=titles[short];if(!names)return;
function sg(n){return n<0?String(n):'+'+n}
function numberline(n,op){var close=op.indexOf('=')>=0,lt=op[0]==='<',x0=224,step=24,p=[];p.push('<svg class="mk-numberline" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 100" width="4.1in" role="img" aria-label="number line showing x '+op+' '+n+'"><path d="M20 43H438" stroke="#171717" stroke-width="2.7"/><path d="M20 43l10 -5v10z M438 43l-10 -5v10z" fill="#171717"/>');
for(var k=-8;k<=8;k++){var xx=x0+k*step;p.push('<path d="M'+xx+' 37v12" stroke="#222" stroke-width="1.6"/><text x="'+xx+'" y="68" text-anchor="middle" font-size="12" font-family="Arial">'+(n+k)+'</text>');}
p.push('<path d="M'+x0+' 43H'+(lt?28:430)+'" stroke="#111" stroke-width="4.8" stroke-linecap="round"/><circle cx="'+x0+'" cy="43" r="6.5" fill="'+(close?'#111':'white')+'" stroke="#111" stroke-width="2.5"/></svg>');return p.join('');}
function make(i){return function(ctx){var r=ctx.rng,a=r.int(2,6),b=r.int(1,6),c=r.int(1,5),x=r.int(-4,4),t=r.int(-5,5),p,ans,steps=[],fig=null,key;var op=['>','<','>=','<='][r.int(0,3)],m=r.int(1,3)*(r.chance(.5)?1:-1),bb=r.int(-4,4);
if(short==='expressions-equations')switch(i){
case 0:p='Evaluate '+M(a+'x+'+b)+' when '+M('x='+(-c))+'.';ans=M(String(-a*c+b));break;
case 1:p='Simplify '+M(a+'x+'+b+'y-'+c+'x+'+a+'y')+'.';ans=M((a-c)+'x+'+(a+b)+'y');break;
case 2:p='Simplify '+M('-'+a+'(x-'+b+')')+'.';ans=M('-'+a+'x+'+(a*b));break;
case 3:p='Solve '+M(a+'(x+'+b+')='+a*(x+b)) +'.';ans=M('x='+x);break;
case 4:p='Solve '+M(a+'x+'+b+'='+ (a*x+b))+'.';ans=M('x='+x);break;
case 5:p='Solve '+M('0.'+a+'x+'+b+'='+(a*x/10+b).toFixed(1))+'.';ans=M('x='+x);break;
case 6:p='Solve '+M('\\frac{x}{'+a+'}='+b)+'.';ans=M('x='+(a*b));break;
case 7:p='A taxi charges $'+b+' plus $'+a+' per mile. What is the cost for '+c+' miles?';ans='$'+(b+a*c);break;
case 8:p='A fee of $'+b+' plus $'+a+' per ticket totals $'+(b+a*c)+'. Write and solve an equation for the number of tickets.';ans=M('x='+c);break;
case 9:p='A person is '+a+' times as old as a child. Their ages total '+(a+1)*b+'. How old is the child?';ans=b+' years';break;
case 10:p='How many solutions does '+M(a+'(x+'+b+')='+a+'x+'+(a*b))+' have?';ans='Infinitely many solutions';break;
case 11:p='Solve '+M('P=2l+2w')+' for '+M('w')+'.';ans=M('w=\\frac{P-2l}{2}');break;}
else if(short==='inequalities')switch(i){
case 0:case 1:{var o=i===0?'>':'<=';p='Graph '+M('x'+(i===0?'>':'\\le')+x)+' on the number line.';p+='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 90" width="4.1in" aria-label="blank number line" role="img"><path d="M17 37H443" stroke="#111" stroke-width="2.5"/><path d="M17 37l10 -5v10z M443 37l-10 -5v10z" fill="#111"/>';for(var tick=-8;tick<=8;tick++){var loc=224+tick*24;p+='<path d="M'+loc+' 30v14" stroke="#222" stroke-width="1.5"/><text x="'+loc+'" y="64" font-size="12" font-family="Arial" text-anchor="middle">'+(x+tick)+'</text>';}p+='</svg>';ans=i===0?'Open circle at '+x+', shade right':'Closed circle at '+x+', shade left';break;}
case 2:{p='Write the inequality shown on the number line: '+numberline(x,op);ans=M('x'+({'>':'>','<':'<','>=':'\\ge','<=':'\\le'}[op])+x);break;}
case 3:p='For '+M('x\\ge '+x)+', is the endpoint '+x+' open or closed?';ans='Closed';break;
case 4:p='Solve and graph '+M(a+'x+'+b+'>'+ (a*x+b))+'.';ans=M('x>'+x);break;
case 5:p='Solve '+M('-'+a+'x+'+b+'>'+(-a*x+b))+'.';ans=M('x<'+x);break;
case 6:p='Write the solution to the AND inequality '+M('x>'+ (x-a)+'\\text{ and }x<'+(x+a))+'.';ans=M((x-a)+'<x<'+(x+a));break;
case 7:p='Write the solution to '+M('x<'+(x-a)+'\\text{ or }x>'+(x+a))+'.';ans=M('x<'+(x-a)+'\\text{ or }x>'+(x+a));break;
case 8:p='Solve '+M('|x'+sg(-x)+'|<'+a)+'.';ans=M((x-a)+'<x<'+(x+a));break;
case 9:p='Solve '+M('|x'+sg(-x)+'|>'+a)+'.';ans=M('x<'+(x-a)+'\\text{ or }x>' +(x+a));break;
case 10:p='Does '+M('x='+(x+1))+' satisfy '+M('x>'+x)+'?';ans='Yes';break;
case 11:p='Admission costs $'+a+' per person. You have at most $'+(a*b)+'. Write an inequality for the number of people n.';ans=M(a+'n\\le '+(a*b));break;}
else if(short==='graphing-inequalities'){var strict=[0,1,8,10].indexOf(i)>=0,less=[1,3,7,9].indexOf(i)>=0,vertical=i===5,horizontal=i===4,kind=vertical?'vline':'line',ls=vertical?{kind:'vline',x:bb,dashed:strict}:{kind:'line',m:horizontal?0:m,b:bb,dashed:strict};
fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[ls],points:[],shade:vertical?undefined:{m:horizontal?0:m,b:bb,above:!less}};
if(i<=5){fig.shade=undefined;p='Graph '+M((vertical?'x': 'y')+(strict?(less?'<':'>'):(less?'\\le':'\\ge'))+(vertical?bb:(horizontal?bb:m+'x'+sg(bb))))+'.';fig.lines=[];ans=(strict?'Dashed':'Solid')+' boundary; shade '+(vertical?'right':less?'below':'above');}
else if(i===6||i===7){fig.shade=undefined;p='The graphed boundary is '+M('y='+m+'x'+sg(bb))+'. Should the solution for '+M('y'+(i===6?'>':'<')+m+'x'+sg(bb))+' be shaded above or below?';ans=i===6?'Above':'Below';}
else if(i===8||i===9){fig.lines[0].dashed=i===8;p='Write the inequality for this graphed boundary and the shaded region.';ans=M('y'+(i===8?'>':'\\le')+m+'x'+sg(bb));fig.shade.above=i===8;}
else if(i===10){p='Does '+M('(0,'+(bb+2)+')')+' satisfy the inequality represented by the graph?';ans='Yes';fig.shade.above=true;}
else {fig.shade=undefined;p='Does '+M('y='+m+'x'+sg(bb))+' represent a solid or dashed boundary for '+M('y>'+m+'x'+sg(bb))+'?';ans='Dashed';}
}
else if(short==='exponents-exponential-functions')switch(i){
case 0:p='Simplify '+M('x^'+a+'\\cdot x^'+b);ans=M('x^{'+(a+b)+'}');break;
case 1:p='Simplify '+M('('+a+'x)^'+b);ans=M(Math.pow(a,b)+'x^'+b);break;
case 2:p='Simplify '+M('(\\frac{x}{'+a+'})^2');ans=M('\\frac{x^2}{'+(a*a)+'}');break;
case 3:p='Simplify '+M('\\frac{x^'+a+'}{x^'+a+'}')+' for nonzero x.';ans=M('1');break;
case 4:p='Rewrite '+M('x^{-'+a+'}')+' using positive exponents.';ans=M('\\frac{1}{x^'+a+'}');break;
case 5:p='Evaluate '+M('(\\frac{1}{'+a+'})^2');ans=M('\\frac{1}{'+(a*a)+'}');break;
case 6:p='Write '+(a*10000)+' in scientific notation.';ans=M(a+'\\times 10^4');break;
case 7:p='Multiply '+M('('+a+'\\times 10^2)('+b+'\\times 10^3)');ans=M((a*b>=10?(a*b/10)+'\\times 10^6':(a*b)+'\\times 10^5'));break;
case 8:p='Is '+M('P(t)=100(1.'+a+')^t')+' growth or decay?';ans='Growth';break;
case 9:p='Is '+M('P(t)=100(0.'+a+')^t')+' growth or decay?';ans='Decay';break;
case 10:p='An amount of $'+(a*100)+' grows by '+b+'% in one year. Find the new amount.';ans='$'+(a*100*(1+b/100)).toFixed(2);break;
case 11:p='An amount of $'+(a*100)+' depreciates by '+b+'% in one year. Find the new value.';ans='$'+(a*100*(1-b/100)).toFixed(2);break;}
else if(short==='polynomials-factoring')switch(i){
case 0:p='Classify '+M(a+'x^3+'+b+'x')+' by degree.';ans='Cubic (degree 3)';break;
case 1:p='Find the leading coefficient of '+M(a+'x^4+'+b+'x^2+'+c)+'.';ans=M(String(a));break;
case 2:p='Add '+M('('+a+'x+'+b+')+('+c+'x+'+a+')');ans=M((a+c)+'x+'+(a+b));break;
case 3:p='Subtract '+M('('+a+'x+'+b+')-('+c+'x+'+a+')');ans=M((a-c)+'x'+sg(b-a));break;
case 4:p='Multiply '+M(a+'x^2\\cdot '+b+'x^3');ans=M((a*b)+'x^5');break;
case 5:p='Expand '+M(a+'x('+b+'x+'+c+')');ans=M((a*b)+'x^2+'+(a*c)+'x');break;
case 6:p='Expand '+M('(x+'+a+')(x+'+b+')');ans=M('x^2+'+(a+b)+'x+'+(a*b));break;
case 7:{var gg=function(m,n){while(n){var tmp=m%n;m=n;n=tmp;}return m;}(b,c);p='Factor out the GCF: '+M((a*b)+'x^2+'+(a*c)+'x');ans=M((a*gg)+'x('+ (b/gg)+'x+'+(c/gg)+')');break;}
case 8:p='Factor '+M('x^2+'+(a+b)+'x+'+(a*b));ans=M('(x+'+a+')(x+'+b+')');break;
case 9:p='Factor '+M((a*c)+'x^2+'+(a*b+c)+'x+'+b);ans=M('('+a+'x+1)('+c+'x+'+b+')');break;
case 10:p='Factor '+M('x^2-'+a*a);ans=M('(x-'+a+')(x+'+a+')');break;
case 11:p='Solve '+M('(x-'+a+')(x+'+b+')=0');ans=M('x='+a+'\\text{ or }x=-'+b);break;}
else if(short==='quadratics')switch(i){
case 0:p='Find the vertex of '+M('y='+a+'(x-'+x+')^2+'+b);ans=M('('+x+','+b+')');break;
case 1:{var B=-2*a*x;p='Find the axis of symmetry of '+M('y='+a+'x^2'+sg(B)+'x+'+(a*x*x+b));ans=M('x='+x);break;}
case 2:p='Evaluate '+M('f(x)='+a+'x^2+'+b)+' for '+M('x='+x);ans=M(String(a*x*x+b));break;
case 3:p='Complete the table: '+M('f(x)=x^2+'+b)+', find '+M('f('+x+')');ans=M(String(x*x+b));break;
case 4:p='Find the zeros of '+M('y=(x-'+a+')(x+'+b+')');ans=M('x='+a+'\\text{ or }x=-'+b);break;
case 5:p='Find the x-intercepts of the parabola '+M('y=(x-'+a+')(x+'+b+')')+'.';fig=null;ans=M('('+a+',0),(-'+b+',0)');break;
case 6:p='Solve '+M('x^2='+a*a);ans=M('x=\\pm '+a);break;
case 7:p='Solve '+M('(x-'+a+')(x+'+b+')=0');ans=M('x='+a+'\\text{ or }x=-'+b);break;
case 8:{var d=b*b-4*a*c;p='Find the discriminant of '+M(a+'x^2+'+b+'x+'+c+'=0');ans=M(String(d));break;}
case 9:p='How many real solutions does '+M('x^2+'+b+'x+'+(b*b+a)+'=0')+' have?';ans='No real solutions';break;
case 10:p='A projectile reaches height '+b+' meters at the vertex of '+M('h(t)=-'+a+'(t-'+c+')^2+'+b)+'. What is the maximum height?';ans=b+' meters';break;
case 11:p='A profit model is '+M('P(x)=(x-'+a+')(x+'+b+')')+'. At which positive x is break-even?';ans=M('x='+a);break;}
steps=['Correct answer: '+ans];key=short+'|'+i+'|'+p;var answerFig=null;if(short==='graphing-inequalities'&&i<=5){var solVertical=i===5,solHorizontal=i===4,solLess=[1,3].indexOf(i)>=0,solStrict=i<=1;answerFig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[solVertical?{kind:'vline',x:bb,dashed:solStrict}:{kind:'line',m:solHorizontal?0:m,b:bb,dashed:solStrict}],points:[],shade:solVertical?{x:bb,right:true}:{m:solHorizontal?0:m,b:bb,above:!solLess}};}return {prompt:p,answer:ans,steps:steps,fig:fig,answerFig:answerFig,figWhere:fig?'below':'none',key:key,equiv:key};
};}
var cat={id:'extended',letter:String.fromCharCode(65+unit.categories.length),name:'Extended Practice & Applications',lessons:[]};for(var i=0;i<names.length;i++){var id='a1-'+short+'-extended-'+i;N.registerLesson({id:id,unit:u,category:'extended',num:unit.categories.reduce(function(a,c){return a+c.lessons.length},0)+i+1,title:names[i],instruction:names[i],layout:(short==='inequalities'&&i<3?'full':'half'),space:[.5,.85,1.2],generate:make(i)});cat.lessons.push(id);}unit.categories.push(cat);
if(short==='expressions-equations'){
 var harder=[
 ['Variables on both sides: distribute and combine like terms',function(ctx){
   var r=ctx.rng,x=r.int(-9,9),a=r.int(2,6),b=r.int(2,6),c=r.int(1,5),d=r.int(1,5);
   var leftCoef=a+c,rightCoef=b+d;N.gen.need(leftCoef!==rightCoef);
   var leftConst=r.int(-10,10),rightConst=(leftCoef-rightCoef)*x+leftConst;
   var L=a+'(x'+(leftConst>=0?'+':'')+leftConst+')+'+c+'x';
   var R=b+'(x'+(rightConst>=0?'+':'')+rightConst+')+'+d+'x';
   // Adjust constants inside parentheses so solution is exactly x.
   var LC=a*leftConst,RC=LC+(leftCoef-rightCoef)*x;
   N.gen.need(RC%b===0);
   rightConst=RC/b;
   R=b+'(x'+(rightConst>=0?'+':'')+rightConst+')+'+d+'x';
   return {prompt:'Solve and show your work: '+M(L+'='+R),answer:M('x='+x),
   steps:['Distribute: '+M(a+'x'+(LC>=0?'+':'')+LC+'+'+c+'x='+b+'x'+(RC>=0?'+':'')+RC+'+'+d+'x'),
   'Combine like terms: '+M(leftCoef+'x'+(LC>=0?'+':'')+LC+'='+rightCoef+'x'+(RC>=0?'+':'')+RC),
   'Isolate the variable: '+M((leftCoef-rightCoef)+'x='+(RC-LC)),
   'Solution: '+M('x='+x)],key:'both-distribute|'+[a,b,c,d,leftConst,rightConst].join('|'),equiv:'both-distribute|'+[a,b,c,d,x].join('|')};
 }],
 ['Variables on both sides: two distributions and constants',function(ctx){
  var r=ctx.rng,x=r.int(-8,8),a=r.int(2,6),b=r.int(2,6),c=r.int(1,5),d=r.int(1,5);
  var leftCoef=a+c,rightCoef=b+d;N.gen.need(leftCoef!==rightCoef);
  var u=r.int(-7,7),v=r.int(-7,7),k=r.int(-8,8);
  var lhsConst=a*u+k,rhsConst=lhsConst+(leftCoef-rightCoef)*x;
  N.gen.need(rhsConst%b===0);
  var w=rhsConst/b;
  var L=a+'(x'+(u>=0?'+':'')+u+')+'+c+'x'+(k>=0?'+':'')+k;
  var R=b+'(x'+(w>=0?'+':'')+w+')+'+d+'x';
  return {prompt:'Solve the equation. Distribute, combine like terms, and collect variables: '+M(L+'='+R),
  answer:M('x='+x),steps:['Distribute both sides and collect like terms.',
  M(leftCoef+'x'+(lhsConst>=0?'+':'')+lhsConst+'='+rightCoef+'x'+(rhsConst>=0?'+':'')+rhsConst),
  M((leftCoef-rightCoef)+'x='+(rhsConst-lhsConst)),M('x='+x)],
  key:'two-distrib|'+[a,b,c,d,u,w,k].join('|'),equiv:'two-distrib|'+[a,b,c,d,x].join('|')};
 }]
 ];
 var catHard={id:'multi-step-combined',letter:String.fromCharCode(65+unit.categories.length),name:'Advanced Multi-Step Equations',lessons:[]};
 harder.forEach(function(pair,i){var id='a1-expressions-equations-combined-'+i;N.registerLesson({id:id,unit:u,category:catHard.id,num:unit.categories.reduce(function(n,c){return n+c.lessons.length},0)+i+1,title:pair[0],instruction:'Solve, showing distribution and collection of like terms.',layout:'full',space:[1.2,1.8,2.5],generate:pair[1]});catHard.lessons.push(id)});
 unit.categories.push(catHard);
}

})(typeof window!=='undefined'?window:globalThis);