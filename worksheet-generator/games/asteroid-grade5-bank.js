/* Grade 5 Asteroid: deterministic, answer-verified mental-math multiple choice.
   Dedicated arcade pool, not a replacement for the Grade 5 curriculum bank. */
(function(G){'use strict';
const units={
 'place-value-number-sense':[['place','Place Value'],['round','Rounding'],['compare','Comparing Numbers']],
 'multi-digit-multiplication-division':[['multiply','Multiplication Facts'],['divide','Division Facts'],['tens','Multiplying by Tens']],
 'decimal-operations':[['decimal-add','Decimal Addition'],['decimal-sub','Decimal Subtraction'],['decimal-place','Decimal Place Value']]
};
const levels=['cp2','cp1','honors'];
const mod=(n,m)=>((n%m)+m)%m;
const rnd=(seed)=>{let x=seed>>>0;return()=>{x=(Math.imul(x,1664525)+1013904223)>>>0;return x/4294967296}};
const fmt=n=>String(Math.round(n*1000)/1000);
function make(unit,skill,level,i){
 const tier=levels.indexOf(level),r=rnd((i+1)*7919+(tier+1)*104729+skill.length*997);
 const int=(a,b)=>a+Math.floor(r()*(b-a+1));
 let q,a;
 if(skill==='place'){
   const power=int(1,3),digit=int(1,9),tail=int(0,Math.pow(10,power)-1);
   const n=digit*Math.pow(10,power)+tail;
   q='What is the value of the digit in the '+({1:'tens',2:'hundreds',3:'thousands'}[power])+' place of '+n.toLocaleString('en-US')+'?';a=digit*Math.pow(10,power);
 }else if(skill==='round'){
   const p=[10,100,1000][tier],n=int(100,9999);
   q='Round '+n.toLocaleString('en-US')+' to the nearest '+p+'.';a=Math.round(n/p)*p;
 }else if(skill==='compare'){
   const a0=int(10,999),b0=a0+int(1,90)*(r()<.5?-1:1);
   q='Which number is greater: '+a0+' or '+b0+'?';a=Math.max(a0,b0);
 }else if(skill==='multiply'){
   const x=int(2,7+tier*2),y=int(2,7+tier*2);q=x+' × '+y+' = ?';a=x*y;
 }else if(skill==='divide'){
   const y=int(2,7+tier*2),x=int(2,7+tier*2);q=(x*y)+' ÷ '+y+' = ?';a=x;
 }else if(skill==='tens'){
   const x=int(2,12+tier*4),y=[10,20,50][tier];q=x+' × '+y+' = ?';a=x*y;
 }else if(skill==='decimal-add'){
   const scale=[10,10,100][tier],x=int(1,9*scale)/scale,y=int(1,9*scale)/scale;
   q=fmt(x)+' + '+fmt(y)+' = ?';a=Math.round((x+y)*100)/100;
 }else if(skill==='decimal-sub'){
   const scale=[10,10,100][tier],x=int(2,9*scale)/scale,y=int(1,Math.floor(x*scale))/scale;
   q=fmt(x)+' − '+fmt(y)+' = ?';a=Math.round((x-y)*100)/100;
 }else{
   const p=[10,100,1000][tier],n=int(1,9*p)/p;
   q='What is '+fmt(n)+' × 10?';a=Math.round(n*10*100)/100;
 }
 const step=skill==='decimal-add'||skill==='decimal-sub'?1/(tier===2?100:10):Math.max(1,Math.round(Math.abs(a)/10));
 const choices=[a,a+step,a-step,a+2*step].map(fmt);
 if(new Set(choices).size!==4||choices.some(x=>!Number.isFinite(Number(x))))throw Error('Bad choices');
 const order=[0,1,2,3].sort((x,y)=>mod((i+3*x)*13,17)-mod((i+3*y)*13,17));
 const options=order.map(k=>({text:choices[k],correct:k===0}));
 if(options.filter(o=>o.correct).length!==1)throw Error('Bad key');
 return {id:'asteroid-g5-'+unit+'-'+skill+'-'+level+'-'+i,skillId:skill,format:'multiple-choice',prompt:q,answer:fmt(a),options,quickAnswer:true,solutionSteps:[q.replace('?',fmt(a))]};
}
const pool={};
Object.keys(units).forEach(unit=>{pool[unit]={};units[unit].forEach(([id])=>{pool[unit][id]={};levels.forEach(level=>{const questions=[];const seen=new Set();for(let i=0;i<700&&questions.length<90;i++){const q=make(unit,id,level,i),key=q.prompt+'|'+q.answer;if(seen.has(key))continue;seen.add(key);questions.push(q)}if(questions.length<30)throw Error('Insufficient unique Grade 5 Asteroid questions '+unit+'/'+id+'/'+level);pool[unit][id][level]=questions})})});
G.MK_ASTEROID_GRADE5={
 records:unit=>(units[unit]||[]).map(([id,name])=>({id,name})),
 select:(unit,level,ids,n)=>{
   const sets=ids.filter(id=>pool[unit]?.[id]?.[level]).map(id=>pool[unit][id][level]);
   const out=[],index=sets.map(()=>0);
   while(out.length<n&&sets.some((a,j)=>index[j]<a.length))for(let j=0;j<sets.length&&out.length<n;j++)if(index[j]<sets[j].length)out.push(sets[j][index[j]++]);
   return out;
 }
};
})(window);
