/* Run: node worksheet-generator/tests/math-audit.cjs
   Deterministic regression checks for every registered Algebra 1 worksheet bank.
   Verifies generation, graph rendering, and key method-specific invariants.
   This is NOT a proof of every answer's mathematical correctness. */
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const core=['rng','frac','tex','graph','framework','render'];
const units=['expressions-equations','inequalities','graphing-inequalities','exponents-exponential-functions','polynomials-factoring','quadratics','systems-of-equations','linear-functions'];
function load(name){
  const id='algebra1-'+name,env={document:{body:{getAttribute:()=>id}},console};
  env.window=env;env.globalThis=env;vm.createContext(env);
  const run=(src,file)=>vm.runInContext(src,env,{filename:file,timeout:10000});
  core.forEach(f=>run(read('core/'+f+'.js'),f));
  if(name==='linear-functions'){
    ['common','lessons-slope','lessons-graphing','lessons-writing','lessons-forms','lessons-applications','index'].forEach(f=>run(read('units/algebra1/linear-functions/'+f+'.js'),f));
  }else{
    const html=read('algebra1-'+name+'.html');
    const m=html.match(/<script>\s*([\s\S]*?)\s*<\/script>/);
    assert(m,'Missing embedded lesson registration for '+name);
    run(m[1],name+'-inline');
    if(name==='systems-of-equations')run(read('units/algebra1/systems-of-equations/extra-skills.js'),'systems-extra');
    else{
      run(read('core/algebra1-expanded-skills.js'),'algebra1-expanded');
      run(read('core/algebra1-extended-practice.js'),'algebra1-extended');
      if(name==='inequalities')run(read('units/algebra1/inequalities/solve-graph.js'),'ineq-solve-graph');
    }
  }
  assert(env.MKWS.registry.units[id],'Missing registered unit '+id);
  return env.MKWS;
}
function mathSnippets(prompt){return [...prompt.matchAll(/⟨([^⟩]*)⟩/g)].map(m=>m[1]);}
function evaluate(expr,x,y){
  const converted=expr.replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g,'(($1)/($2))').replace(/\\,/g,'').replace(/(\d)([xy])/g,'$1*$2').replace(/\s/g,'');
  assert(/^[xy0-9+*/().\-]+$/.test(converted),'Unsupported linear equation '+expr);
  return new Function('x','y','return '+converted)(x,y);
}
function coefficients(tex){
  const lr=tex.split('=');
  assert.equal(lr.length,2,'Expected an equation '+tex);
  const f=(x,y)=>evaluate(lr[0],x,y)-evaluate(lr[1],x,y);
  return {a:f(1,0)-f(0,0),b:f(0,1)-f(0,0),c:-f(0,0)};
}
function verifySystems(p,id){
  const s=mathSnippets(p.prompt);
  if(['sys-substitution-easy','sys-substitution-standard','sys-elimination-add','sys-elimination-multiply'].includes(id)){
    const e1=coefficients(s[0]),e2=coefficients(s[1]);
    assert.notEqual(e1.a*e2.b-e2.a*e1.b,0,'System must have unique solution');
    if(id==='sys-substitution-easy')assert(/^y=/.test(s[0]),'Easy substitution must isolate y');
    if(id==='sys-substitution-standard')assert(/^x=/.test(s[0]),'Standard substitution must isolate x');
    if(id==='sys-elimination-add')assert(e1.a+e2.a===0||e1.b+e2.b===0||e1.a===e2.a||e1.b===e2.b,'Adding/subtracting cannot immediately eliminate either variable');
    if(id==='sys-elimination-multiply'){assert.equal(e2.a,2*e1.a);assert.notEqual(Math.abs(e1.b),Math.abs(e2.b),'Multiplication example also has a direct elimination shortcut');}
    const tuple=p.answer.match(/⟨\((-?\d+),\\,(-?\d+)\)⟩/);
    assert(tuple,'Missing ordered-pair answer');
    const x=+tuple[1],y=+tuple[2];
    for(const e of [e1,e2])assert.equal(e.a*x+e.b*y,e.c,'Wrong ordered-pair answer');
  }
  if(['sys-extra-add','sys-extra-subtract','sys-extra-scale','sys-extra-bothScale'].includes(id)){
    const [e1,e2]=s.slice(0,2).map(coefficients);
    if(id==='sys-extra-add')assert.equal(e1.a+e2.a,0);
    if(id==='sys-extra-subtract')assert.equal(e1.a,e2.a);
    if(id==='sys-extra-scale'){assert.equal(e2.a,2*e1.a);assert.notEqual(Math.abs(e1.b),Math.abs(e2.b));}
    if(id==='sys-extra-bothScale'){assert.equal(e1.a,2);assert.equal(e2.a,3);assert.notEqual(Math.abs(e1.b),Math.abs(e2.b));}
  }
}
let total=0,skills=0;
for(const name of units){
  const NS=load(name),unit=NS.registry.units['algebra1-'+name],ids=unit.categories.flatMap(c=>c.lessons);
  assert.equal(ids.length,new Set(ids).size,'Duplicate lesson listed for '+name);
  for(const id of ids){
    for(let seed=1;seed<=100;seed++){
      const p=NS.generateOne(id,{seed,difficulty:'standard',grids:true});
      assert(p.prompt&&p.answer,'Missing question or answer: '+id);
      if(p.fig)assert(NS.graph(p.fig).includes('<svg'),'Broken student figure '+id);
      if(p.answerFig)assert(NS.graph(p.answerFig).includes('<svg'),'Broken answer figure '+id);
      if(name==='systems-of-equations')verifySystems(p,id);
      if(name==='expressions-equations'&&['a1-expressions-equations-proportion','a1-expressions-equations-fractionEq'].includes(id)){
        const question=mathSnippets(p.prompt)[0],answer=mathSnippets(p.answer)[0];
        const eq=question.split('='),solution=Number(answer.replace('x=',''));
        assert.equal(eq.length,2);
        const residual=x=>evaluate(eq[0],x,0)-evaluate(eq[1],x,0);
        assert(Math.abs(residual(solution))<1e-8,'Proportion answer is wrong');
        assert(Math.abs(residual(solution+1))>1e-8,'Proportion is an identity, not a unique equation');
      }

      if(id==='a1-polynomials-factoring-extended-7'){
        const lhs=mathSnippets(p.prompt)[0],rhs=mathSnippets(p.answer)[0];
        const a=/^(\d+)x\^2\+(\d+)x$/.exec(lhs);
        const b=/^(\d+)x\((\d+)x\+(\d+)\)$/.exec(rhs);
        assert(a&&b,'Unexpected GCF problem format');
        const gcd=(x,y)=>y?gcd(y,x%y):x;
        assert.equal(+b[1],gcd(+a[1],+a[2]),'GCF not fully factored');
        assert.equal(+b[1]* +b[2],+a[1]);
        assert.equal(+b[1]* +b[3],+a[2]);
      }
      if(name==='graphing-inequalities'){
        const n=/^a1-graphing-inequalities-extended-(\d+)$/.exec(id);
        if(n&&+n[1]<=5){
          assert(p.fig&&!p.fig.shade&&!p.fig.lines.length,'Graphing question already shows the answer '+id);
          assert(p.answerFig&&p.answerFig.lines.length,'Graph answer missing '+id);
        }
      }
      total++;
    }
    skills++;
  }
  console.log(name+': '+ids.length+' skills verified');
}
console.log('PASS: '+skills+' skills, '+total+' seeded generation/graph checks.');
