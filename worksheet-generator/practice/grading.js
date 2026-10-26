/* Conservative student answer checker. All mathematics uses menu/mathcheck.js. */
(function(G){
'use strict';
var C=G.MKMENU&&G.MKMENU.check, A=(G.MKPRACTICE=G.MKPRACTICE||{});
function clean(s){return String(s||'').replace(/[−–]/g,'-').replace(/≤/g,'<=').replace(/≥/g,'>=').trim();}
function onlyMath(s){var m=/^⟨([\s\S]+)⟩$/.exec(s);return m?m[1]:s;}
function single(p){
 return !!(p&&p.parts&&p.parts.length===1&&!p.parts[0].answerFig);
}
function supports(p){
 if(!C||!single(p))return false;
 var a=onlyMath(String(p.parts[0].answer).trim());
 // Only unambiguous numerical answers, x = number, and solved single inequalities.
 try{
   if(/^x\s*=\s*/i.test(a)){C.readNumber(a.replace(/^x\s*=\s*/i,''));return true;}
   if(/^[+-]?(?:\d|\.)/.test(a)&&!/[a-zA-Z]/.test(a)){C.readNumber(a);return true;}
   if(/^x\s*(?:<|>|\\le|\\ge|≤|≥)/.test(a)||/^(?:-?\d+(?:\.\d+)?|\\frac\{[^{}]+\}\{[^{}]+\})\s*(?:<|>|\\le|\\ge)/.test(a)){C.solutionSet(a,'x');return true;}
 }catch(e){}
 return false;
}
function grade(p,typed){
 if(!supports(p))return {status:'self'};
 var target=onlyMath(String(p.parts[0].answer).trim()),input=clean(typed);
 if(!input)return {status:'empty'};
 if(input.length>140)return {status:'invalid',message:'Answer is too long; enter the final answer only.'};
 try{
   if(/^x\s*(?:<|>|\\le|\\ge|≤|≥)/.test(target)||/^(?:-?\d+(?:\.\d+)?|\\frac\{[^{}]+\}\{[^{}]+\})\s*(?:<|>|\\le|\\ge)/.test(target)){
     if(!/(?:<|>|<=|>=|≤|≥)/.test(input))return {status:'invalid',message:'Enter an inequality such as x < 3.'};
     if(!C.solvedForm('⟨'+input+'⟩','x'))return {status:'invalid',message:'Solve the inequality for x before checking.'};
     return {status:C.setEqual(C.solutionSet(target,'x'),C.solutionSet(input,'x'))?'correct':'incorrect'};
   }
   var val=target.replace(/^x\s*=\s*/i,''),response=input;
   if(/^x\s*=/.test(target)){response=response.replace(/^x\s*=\s*/i,'');if(/[a-zA-Z=]/.test(response))return {status:'invalid',message:'Enter just the value of x.'};}
   else if(/[a-zA-Z=]/.test(response))return {status:'invalid',message:'Enter a numeric answer.'};
   return {status:C.readNumber(val).eq(C.readNumber(response))?'correct':'incorrect'};
 }catch(e){return {status:'invalid',message:'Use a number, fraction (for example 3/4), or a solved inequality.'};}
}
A.supports=supports;A.grade=grade;
})(window);