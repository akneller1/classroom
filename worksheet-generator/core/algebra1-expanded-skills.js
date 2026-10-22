/* Additional Algebra 1 skill families. Shared UI and problem engine remain unchanged. */
(function(G){'use strict';
var N=G.MKWS,T=N.tex,M=T.M,u=document.body.getAttribute('data-unit'),unit=N.registry.units[u];
if(!unit)return;
var configs={
'expressions-equations':[
['Simplifying & Evaluating',['terms','distribute','evaluate','verbal'],[['Nested distribution','nested'],['Evaluate a formula','formulaEval']]],
['Solving Equations',['equation','both','paren'],[['Solve fraction equations','fractionEq'],['Identify equations with no solution','noSolution']]],
['Proportions & Applications',['proportion'],[['Solve percent problems','percent']]]],
'inequalities':[
['Solving Inequalities',['inequality','inequalityMulti','negative'],[['Translate words into inequalities','words'],['Include or exclude an endpoint','inclusive']]],
['Compound Inequalities',['compoundAnd','compoundOr'],[['Solve compound AND inequalities','solveAnd'],['Solve compound OR inequalities','solveOr']]],
['Absolute Value Inequalities',['absolute','absGreater'],[['Absolute value inequalities with offsets','absShift']]]],
'graphing-inequalities':[
['Boundary Lines',['boundary','graphBoundary','boundaryRead'],[['Solid or dashed boundary?','lineType']]],
['Graphing & Shading',['graphInequality','shading'],[['Graph strict inequalities','strict'],['Graph horizontal inequalities','horizontal']]],
['Analyzing Solutions',['testPoint'],[['Test a point outside the region','pointNo'],['Read a graph to write an inequality','readGraph']]]],
'exponents-exponential-functions':[
['Exponent Laws',['multiplyPowers','dividePowers','powerPower','negExp','zeroExp'],[['Multiply monomials with exponents','coeffPower'],['Evaluate negative powers','negativeValue']]],
['Exponential Functions',['expEval','growth'],[['Write an exponential decay model','decayModel'],['Evaluate exponential models','evaluateModel']]],
['Growth vs. Decay',[],[['Identify growth and decay factors','growthFactor']]]],
'polynomials-factoring':[
['Polynomial Operations',['addPoly','multiplyBinomials'],[['Subtract polynomials','subtractPoly'],['Distribute a monomial','distributePoly']]],
['Factoring',['factor','diffSquares','gcf','group'],[['Factor perfect square trinomials','perfectSquare'],['Factor trinomials with leading coefficients','nonmonic']]],
['Solving by Factoring',['solveFactor'],[['Solve differences of squares','solveDifference']]]],
'quadratics':[
['Forms & Graph Features',['vertex','axis','discriminant'],[['Identify maximum or minimum','maxMin'],['Find a quadratic y-intercept','yIntercept']]],
['Solving Quadratic Equations',['roots','formula','sqrt'],[['Solve by completing the square','complete'],['Classify real solutions using discriminant','numberRoots']]],
['Evaluating & Rewriting',['quadEval','expandQuad'],[['Evaluate quadratic expressions from values','tableValue'],['Match roots to factored form','matchRoots']]]]
};
var short=u.replace('algebra1-',''),cfg=configs[short];if(!cfg)return;
function val(r,a,b){return r.int(a,b)}
function signed(n){return n<0?String(n):'+'+n}
function make(type){return function(ctx){
var r=ctx.rng,a=val(r,2,6),b=val(r,1,7),c=val(r,1,6),x=val(r,-5,5),p,ans,steps=[],fig=null,layout;
switch(type){
case 'nested':p='Simplify '+M(a+'(2x+'+b+')-'+c+'(x-'+b+')')+'.';ans=M((2*a-c)+'x'+signed(a*b+c*b));steps=['Distribute each term, then combine like terms.'];break;
case 'formulaEval':p='Use '+M('A=lw')+' to find area when '+M('l='+a+',\\ w='+b)+'.';ans=M('A='+(a*b));steps=['Substitute '+a+' and '+b+' into '+M('A=lw')+'.'];break;
case 'fractionEq':p='Solve '+M('\\frac{x+'+(a*b)+'}{'+a+'}=\\frac{'+(x+a*b)+'}{'+a+'}')+'.';ans=M('x='+x);steps=['Multiply both sides by '+a+', then subtract '+(a*b)+'.'];break;
case 'noSolution':p='How many solutions? '+M(a+'(x+'+b+')='+a+'x+'+(a*b+c));ans='No solution';steps=['Expanding gives '+M(a+'x+'+(a*b)+'='+a+'x+'+(a*b+c))+'.','Subtracting '+M(a+'x')+' leaves a false equality.'];break;
case 'percent':p='Find '+a*10+'% of '+b*10+'.';ans=M(String(a*b));steps=[M('\\frac{'+a*10+'}{100}\\times '+b*10+'='+a*b)];break;
case 'words':p='Write an inequality: a number x decreased by '+a+' is at least '+b+'.';ans=M('x-'+a+'\\ge '+b);steps=['At least means greater than or equal to.'];break;
case 'inclusive':p='Does '+M('x\\le '+a)+' include '+M('x='+a)+' in its solution set?';ans='Yes';steps=['The less-than-or-equal sign includes the endpoint.'];break;
case 'solveAnd':p='Solve '+M((x-a+b)+'<t+'+b+'\\le '+(x+a+b))+'.';ans=M((x-a)+'<t\\le '+(x+a));steps=['Subtract '+b+' from all three parts.'];break;
case 'solveOr':p='Solve '+M('t+'+b+'<'+(x-a+b)+'\\text{ or }t+'+b+'>'+(x+a+b))+'.';ans=M('t<'+(x-a)+'\\text{ or }t>'+(x+a));steps=['Subtract '+b+' from both inequalities.'];break;
case 'absShift':p='Solve '+M('|x-'+x+'|+'+b+'\\le '+(a+b))+'.';ans=M((x-a)+'\\le x\\le '+(x+a));steps=['Subtract '+b+', then keep x within '+a+' units of '+x+'.'];break;
case 'lineType':p='For '+M('y\\ge '+a+'x-'+b)+', is the boundary solid or dashed?';ans='Solid';steps=['The equality bar includes the boundary line.'];break;
case 'strict':p='Graph '+M('y>'+a+'x-'+b)+' on the coordinate plane.';ans='Dashed boundary, shade above';fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[],points:[]};steps=['Use a dashed line because the inequality is strict, and shade above.'];break;
case 'horizontal':p='Graph '+M('y\\le '+b)+' on the coordinate plane.';ans='Solid horizontal line at y='+b+', shade below';fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[],points:[]};steps=['Draw the horizontal boundary at '+b+'; shade the region below.'];break;
case 'pointNo':p='Does the point '+M('('+x+','+(a*x-b-1)+')')+' satisfy '+M('y\\ge '+a+'x-'+b)+'?';ans='No';steps=['The point is exactly one unit below the boundary.'];break;
case 'readGraph':p='Write an inequality for the solid line shown, shading below it.';fig={xmin:-10,xmax:10,ymin:-10,ymax:10,lines:[{kind:'line',m:a,b:-b}],points:[]};ans=M('y\\le '+a+'x-'+b);steps=['Read the slope and y-intercept, then include the boundary because it is solid.'];break;
case 'coeffPower':p='Simplify '+M(a+'x^'+b+'\\cdot '+c+'x^'+a)+'.';ans=M((a*c)+'x^{'+(a+b)+'}');steps=['Multiply coefficients and add exponents of like bases.'];break;
case 'negativeValue':p='Evaluate '+M(a+'^{-2}')+'.';ans=M('\\frac{1}{'+(a*a)+'}');steps=['Use a reciprocal and square the base.'];break;
case 'decayModel':p='A machine worth $'+a*100+' loses '+b+'% of its value each year. Write V(t).';ans=M('V(t)='+(a*100)+'(1-\\frac{'+b+'}{100})^t');steps=['Multiply starting value by the decay factor to the time exponent.'];break;
case 'evaluateModel':p='For '+M('f(t)='+a+'\\cdot 2^t')+', calculate '+M('f('+b+')')+'.';ans=M(String(a*Math.pow(2,b)));steps=['Substitute '+b+' and evaluate the power first.'];break;
case 'growthFactor':p='Does '+M('f(t)='+a+'(0.'+b+')^t')+' represent growth or decay?';ans='Decay';steps=['A factor between 0 and 1 represents decay.'];break;
case 'subtractPoly':p='Subtract '+M('('+b+'x^2+'+c+'x+'+a+')-('+a+'x^2+'+b+'x+'+c+')')+'.';ans=M((b-a)+'x^2'+signed(c-b)+'x'+signed(a-c));steps=['Distribute the negative sign, then combine like terms.'];break;
case 'distributePoly':p='Expand '+M(a+'x('+b+'x^2+'+c+'x+'+b+')')+'.';ans=M((a*b)+'x^3+'+(a*c)+'x^2+'+(a*b)+'x');steps=['Multiply every term by '+M(a+'x')+'.'];break;
case 'perfectSquare':p='Factor '+M('x^2+'+(2*b)+'x+'+(b*b))+'.';ans=M('(x+'+b+')^2');steps=['This is a perfect square trinomial.'];break;
case 'nonmonic':p='Factor '+M((a*c)+'x^2+'+(a*b+c)+'x+'+b)+'.';ans=M('('+a+'x+1)('+c+'x+'+b+')');steps=['Check using distributive multiplication.'];break;
case 'solveDifference':p='Solve '+M('x^2-'+(a*a)+'=0')+'.';ans=M('x=\\pm '+a);steps=['Factor as a difference of two squares and set each factor to zero.'];break;
case 'maxMin':p='Does '+M('y=-'+a+'(x-'+x+')^2+'+b)+' have a maximum or minimum? Give the value.';ans='Maximum value '+b;steps=['Negative leading coefficient means the parabola opens downward.'];break;
case 'yIntercept':p='Find the y-intercept of '+M('y='+a+'x^2+'+b+'x+'+c)+'.';ans=M('(0,'+c+')');steps=['Set x equal to zero.'];break;
case 'complete':p='Solve '+M('(x-'+x+')^2='+a*a)+'.';ans=M('x='+(x-a)+'\\text{ or }x='+(x+a));steps=['Take positive and negative square roots, then isolate x.'];break;
case 'numberRoots':p='How many real solutions does '+M('x^2+'+b+'x+'+(b*b+a)+'=0')+' have?';ans='No real solutions';steps=['The discriminant is '+(b*b-4*(b*b+a))+', which is negative.'];break;
case 'tableValue':p='For '+M('f(x)='+a+'x^2-'+b)+' find '+M('f('+x+')')+'.';ans=M(String(a*x*x-b));steps=['Square the input before multiplying by '+a+'.'];break;
case 'matchRoots':p='Write a monic quadratic with roots '+M(x)+' and '+M(-a)+', in factored form.';ans=M('(x'+signed(-x)+')(x+'+a+')');steps=['A root r contributes a factor (x-r).'];break;
default:throw Error('Unknown problem '+type);
}
return {prompt:p,answer:ans,steps:steps,fig:fig,figWhere:fig?'below':'none',key:type+'|'+p,equiv:type+'|'+p};
};}
var orig=unit.categories.reduce(function(a,c){return a.concat(c.lessons)},[]);
var used={},cats=[],count=orig.length;
cfg.forEach(function(group,i){
var ids=[];
group[1].forEach(function(key){var id='a1-'+short+'-'+key;if(N.registry.lessons[id]){ids.push(id);used[id]=true;}});
group[2].forEach(function(pair){var id='a1-'+short+'-'+pair[1];N.registerLesson({id:id,unit:u,category:'group'+i,num:++count,title:pair[0],instruction:pair[0],layout:'half',space:[.7,1.1,1.6],generate:make(pair[1])});ids.push(id);used[id]=true;});
cats.push({id:'group'+i,letter:String.fromCharCode(65+i),name:group[0],lessons:ids});
});
var leftover=orig.filter(function(id){return !used[id]});
if(leftover.length)cats.push({id:'additional',letter:String.fromCharCode(65+cats.length),name:'Additional Practice',lessons:leftover});
unit.categories=cats;
})(typeof window!=='undefined'?window:globalThis);