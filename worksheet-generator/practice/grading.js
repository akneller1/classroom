/* Exact student answer grading using the existing independent math checker.
   Never use eval or floating point; unsupported question types remain self-checked. */
(function(G){
'use strict';
var C=G.MKMENU&&G.MKMENU.check, API=(G.MKPRACTICE=G.MKPRACTICE||{});
function unwrap(s){s=String(s||'').trim();return s.replace(/⟨([^⟩]+)⟩/g,'$1').trim();}
function normalize(s){return String(s||'').replace(/[−–]/g,'-').replace(/≥|>=/g,'\\ge ').replace(/≤|<=/g,'\\le ').replace(/\\text\s*\{\s*or\s*\}/gi,' or ').replace(/\\text\s*\{\s*and\s*\}/gi,' and ').trim();}
function rational(s){return C.readNumber(normalize(s));}
function isPair(s){return /^\(\s*[^(),]+\s*,\s*[^(),]+\s*\)$/.test(s);}
function pair(s){var m=/^\(\s*([^(),]+)\s*,\s*([^(),]+)\s*\)$/.exec(s);if(!m)throw Error('not an ordered pair');return [rational(m[1]),rational(m[2])];}
function roots(s){var arr=s.split(/\s+(?:or|and)\s+|[,;]\s*(?=x\s*=)/i);if(arr.length<2)return null;return arr.map(function(part){if(!/^x\s*=\s*/i.test(part))throw Error('not an x-value list');return rational(part.replace(/^x\s*=\s*/i,''));});}
function sameRoots(a,b){return a.length===b.length&&a.every(function(x){return b.some(function(y){return x.eq(y);});})&&b.every(function(y){return a.some(function(x){return x.eq(y);});});}
function special(s){var t=s.toLowerCase().replace(/\s+/g,' ').trim();if(/^(?:no solution|no real solutions|none)$/.test(t))return 'none';if(/^(?:infinitely many solutions|all real numbers|all real x|all real values)$/.test(t))return 'all';return null;}
function relation(s){var match=/^\s*(y)\s*=\s*(.+)$/i.exec(s);if(!match)return null;return match[2];}
function inequality(s){return /(?:<|>|\\le|\\ge|≤|≥)/.test(s);}
function solutionSet(s){return C.solutionSet(s,'x');}
function classify(s){
 s=normalize(unwrap(s));
 if(G.MKRADICAL&&G.MKRADICAL.supports(s))return 'radical';
 if(special(s))return 'special';
 if(isPair(s)){pair(s);return 'pair';}
 if(/\s+(?:or|and)\s+|[,;]\s*(?=x\s*=)/i.test(s)&&roots(s))return 'roots';
 if(inequality(s)){solutionSet(s);return 'inequality';}
 if(relation(s)){C.parseExpr(relation(s));return 'function';}
 if(/^x\s*=/i.test(s)){rational(s.replace(/^x\s*=\s*/i,''));return 'number';}
 try{rational(s);return 'number';}catch(e){}
 if(!/[=<>]/.test(s)&&/[a-zA-Z]/.test(s)){C.parseExpr(s);return 'expression';}
 return null;
}
function supports(problem){
 if(!C||!problem||!problem.parts||problem.parts.length!==1||problem.parts[0].answerFig)return false;
 try{return !!classify(problem.parts[0].answer);}catch(e){return false;}
}
function grade(problem,typed){
 if(!supports(problem))return {status:'self'};
 var answer=normalize(unwrap(problem.parts[0].answer)),input=normalize(unwrap(typed));
 if(!input)return {status:'empty'};
 if(input.length>180)return {status:'invalid',message:'Enter only your final answer (180 characters maximum).'};
 var kind=classify(answer);
 try{
   if(kind==='radical')return G.MKRADICAL.grade(answer,input);
   if(kind==='special'){var sp=special(input);return sp?{status:sp===special(answer)?'correct':'incorrect'}:{status:'invalid',message:'Enter “No solution” or “All real numbers” as appropriate.'};}
   if(kind==='pair'){var a=pair(answer),b=pair(input);return {status:a[0].eq(b[0])&&a[1].eq(b[1])?'correct':'incorrect'};}
   if(kind==='roots'){var aRoots=roots(answer),bRoots=roots(input);if(!bRoots)return {status:'invalid',message:'List all solutions, such as x = 2 or x = -3.'};return {status:sameRoots(aRoots,bRoots)?'correct':'incorrect'};}
   if(kind==='inequality'){
     if(!inequality(input))return {status:'invalid',message:'Enter a solved inequality such as x <= 3.'};
     if(!C.solvedForm('⟨'+input+'⟩','x'))return {status:'invalid',message:'Solve the inequality for x before checking.'};
     return {status:C.setEqual(solutionSet(answer),solutionSet(input))?'correct':'incorrect'};
   }
   if(kind==='number'){
     var aNum=rational(answer.replace(/^x\s*=\s*/i,'')),bNum=rational(input.replace(/^x\s*=\s*/i,''));
     return {status:aNum.eq(bNum)?'correct':'incorrect'};
   }
   if(kind==='function'){
     if(!relation(input))return {status:'invalid',message:'Enter a function equation, such as y = 2x + 3.'};
     return {status:C.equivalent(relation(answer),relation(input))?'correct':'incorrect'};
   }
   if(kind==='expression'){
     if(/[=<>]/.test(input))return {status:'invalid',message:'Enter an algebraic expression without an equals sign.'};
     return {status:C.equivalent(answer,input)?'correct':'incorrect'};
   }
 }catch(e){return {status:'invalid',message:'Answer format could not be read. Use fractions such as 3/4, ordered pairs (2, -3), or standard algebra notation.'};}
 return {status:'self'};
}
API.supports=supports;API.grade=grade;
})(window);
