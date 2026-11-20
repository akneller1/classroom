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
/* Authored-bank short answers (Algebra 2 audit, 2026-11-17). Bank keys are plain text such as "24 years", "$1,647.01",
   "(5, 2)" or "x = 1 or x = 5". Only kinds that cannot be gamed are graded automatically: a number (with an optional unit,
   dollar sign or thousands commas), an ordered pair, a list of x-values or no solution / all real numbers. Expressions are
   left to self-check because equivalence would accept the unfactored or unsimplified form a question asks to rewrite. */
var BANK_KINDS={number:1,pair:1,roots:1,special:1};
var UNIT=/^(\$?)\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?|-?\d+\/\d+)\s*(%|°|[a-zA-Z][a-zA-Z .\/²³-]{0,30})?$/;
function bankCore(s){
 s=String(s==null?'':s).replace(/[−–]/g,'-').trim().replace(/\.$/,'');
 var m=UNIT.exec(s);
 if(m&&(m[1]||m[3]))return {text:m[2].replace(/,/g,''),unit:(m[3]||'').trim(),money:!!m[1]};
 return {text:s.replace(/(\d),(?=\d{3}\b)/g,'$1'),unit:'',money:false};
}
function bankAnswer(answer){
 if(typeof answer!=='string'||!C)return null;
 if(/≈|\b(?:and|or)\b.*[a-wyz]\s*=|[;:]/i.test(answer)&&!/^\s*x\s*=.*\bor\b/i.test(answer))return null;
 var core=bankCore(answer);
 if(core.unit&&(!/^(?:%|°|[a-z.\/²³-]+(?: [a-z.\/²³-]+)?)$/i.test(core.unit)||/\b(?:above|below|left|right|up|down|before|after|from|to|of|than|more|less|units?)\b/i.test(core.unit)))return null;
 try{var kind=classify(core.text);}catch(e){return null;}
 if(!BANK_KINDS[kind])return null;
 if(kind!=='number'&&core.unit)return null;
 return core.text;
}
/* Precalculus audit #2 (2026-11-18): keys the rational grader cannot read (exact values with √ and π, complex numbers,
   vectors, matrices, intervals, exact solution lists and rounded "≈" answers) go to exact-grading.js, which also insists on
   simplest form. Equations and expressions in x stay self-checked. */
function exactKey(answer){return typeof answer==='string'&&G.MKEXACT&&G.MKEXACT.supports(answer)?answer:null;}
/* Discrete Math audit #3 (2026-11-18): sets, truth columns and rows, lists, statement forms and one-word answers go to
   discrete-grading.js. */
function discreteKey(answer){return typeof answer==='string'&&G.MKDISCRETE&&G.MKDISCRETE.supports(answer)?answer:null;}
/* Calculus audit #2 (2026-11-18): expressions, antiderivatives (+ C), differential-equation families and constants with
   e, ln and trig go to calculus-grading.js when none of the graders above reads the key. */
/* Only on Calculus practice tests: elsewhere a form question ("Simplify", "prime factorization") must not accept any
   equivalent expression. practice.js sets MK_PRACTICE_COURSE; tests that load the graders without it get the grader. */
function calcOn(){return !!G.MKCALC&&(!G.MK_PRACTICE_COURSE||G.MK_PRACTICE_COURSE==='calculus');}
function calcKey(answer){return typeof answer==='string'&&calcOn()&&G.MKCALC.supports(answer)?answer:null;}
/* Statistics audit #7 (2026-11-18): labelled numbers and number lists ("Min = 15, Q1 = 25, …", "μ = 1.80, σ ≈ 1.208")
   go to stat-grading.js when no grader above reads the key. Only on Statistics practice tests, like the Calculus grader. */
function statOn(){return !!G.MKSTAT&&(!G.MK_PRACTICE_COURSE||G.MK_PRACTICE_COURSE==='statistics');}
function statKey(answer){return typeof answer==='string'&&statOn()&&G.MKSTAT.supports(answer)?answer:null;}
/* 8th Grade Math audit #4 and #20 (2026-11-19): classification words, numbers with unit phrases, scientific notation,
   line equations, expanded expressions and modelling equations go to grade8-grading.js, and typed ±, e-notation, ^ and
   sqrt( ) are read. Only on 8th Grade Math practice tests, like the Calculus grader. */
function gr8On(){return !!G.MKGRADE8&&(!G.MK_PRACTICE_COURSE||G.MK_PRACTICE_COURSE==='prealgebra');}
function gr8Key(answer,prompt){return typeof answer==='string'&&gr8On()&&G.MKGRADE8.supports(answer,prompt)?answer:null;}
/* Grade 7 audit #1 (2026-11-19): mixed numbers ("-8 2/3" is -26/3, not -8 × 2/3), one-variable inequalities in any
   letter ("m >= 23", "x>-2", "-2 < x") and repeating decimals ("0.8333… (3 repeats)"). Mixed numbers become improper
   fractions in both the key and the typed answer, so 5/4, 1.25 and 1 1/4 all match 1 1/4; when the question asks for a
   mixed number, the typed answer must be one. */
var MIXED=/(^|[^\d.\/])(-?)(\d+)[  ]+(\d+)\/(\d+)(?![\d\/.])/g;
function improper(s){return String(s).replace(/[−–]/g,'-').replace(MIXED,function(m,pre,sg,w,n,d){return pre+sg+(BigInt(w)*BigInt(d)+BigInt(n))+'/'+d;});}
function hasMixed(s){MIXED.lastIndex=0;var r=MIXED.test(String(s).replace(/[−–]/g,'-'));MIXED.lastIndex=0;return r;}
var REP=/^\s*(-?)(\d*)\.(\d*?)(\d+)(?:…|\.\.\.)\s*\((\d+) repeats?\)\s*$/;
function repeatingKey(answer){
 var m=REP.exec(String(answer).replace(/[−–]/g,'-'));if(!m)return null;
 var rep=m[5],dec=m[3]+m[4];if(dec.slice(-rep.length)!==rep)return null;
 while(dec.length>=rep.length&&dec.slice(-rep.length)===rep)dec=dec.slice(0,-rep.length);
 var whole=m[2]||'0',k=dec.length,r=rep.length;
 var a=BigInt(whole+dec+rep)-BigInt(whole+dec),d=(10n**BigInt(k+r))-(10n**BigInt(k));
 return {neg:m[1]==='-',whole:whole,nonrep:dec,rep:rep,num:(m[1]==='-'?-a:a),den:d};
}
function gradeRepeating(R,typed){
 var t=String(typed||'').replace(/[−–]/g,'-').replace(/\s+/g,'').replace(/repeating$/i,'').replace(/\(\d+repeats?\)$/i,'');
 if(!t)return {status:'empty'};
 var f=/^(-?)(\d+)\/(\d+)$/.exec(t);
 if(f){var n=BigInt(f[2]),d=BigInt(f[3]);if(d===0n)return {status:'invalid',message:'The denominator cannot be 0.'};if(f[1])n=-n;return {status:n*R.den===R.num*d?'correct':'incorrect'};}
 var bar=/^(-?)(\d*)\.(\d*?)((?:\d̅)+)$/.exec(t)||/^(-?)(\d*)\.(\d*?)\((\d+)\)$/.exec(t);
 var sign=R.neg?'-':'';
 if(bar){var rep=bar[4].replace(/̅/g,'');return {status:(bar[1]===sign&&(bar[2]||'0')===R.whole&&bar[3]===R.nonrep&&rep===R.rep)?'correct':'incorrect'};}
 var dots=/^(-?)(\d*)\.(\d+)(?:…|\.\.\.)$/.exec(t);
 if(dots){var want=R.nonrep;while(want.length<dots[3].length+R.rep.length)want+=R.rep;var ok=dots[1]===sign&&(dots[2]||'0')===R.whole&&dots[3].length>=R.nonrep.length+2*R.rep.length&&want.indexOf(dots[3])===0;return {status:ok?'correct':'incorrect'};}
 if(/^-?\d*\.\d+$/.test(t))return {status:'invalid',message:'This decimal repeats. Show the repeating digits (for example 0.83… or 0.8(3)) or give the fraction.'};
 return {status:'invalid',message:'Enter a fraction, or the decimal with its repeating digits shown.'};
}
var INEQ=/^\s*(?:([a-z])\s*(<=|>=|<|>|≤|≥)\s*(-?[\d.]+(?:\/\d+)?)|(-?[\d.]+(?:\/\d+)?)\s*(<=|>=|<|>|≤|≥)\s*([a-z]))\s*$/i;
function inequalityKey(answer){var m=INEQ.exec(String(answer).replace(/[−–]/g,'-'));return m?(m[1]||m[6]).toLowerCase():null;}
function gradeInequality(answer,typed,letter){
 var t=String(typed||'').replace(/[−–]/g,'-').trim();
 if(!t)return {status:'empty'};
 var m=INEQ.exec(t);
 if(!m)return {status:'invalid',message:'Enter a solved inequality such as '+letter+' >= 3.'};
 if((m[1]||m[6]).toLowerCase()!==letter)return {status:'incorrect'};
 var sub=function(s){return normalize(String(s).replace(/[−–]/g,'-').replace(new RegExp('\\b'+letter+'\\b','gi'),'x'));};
 return {status:C.setEqual(solutionSet(sub(answer)),solutionSet(sub(t)))?'correct':'incorrect'};
}
function grade7(answer,typed,prompt){
 if(typeof answer!=='string'||!C)return null;
 var R=repeatingKey(answer);if(R)return gradeRepeating(R,typed);
 var v=inequalityKey(answer);if(v)return gradeInequality(answer,typed,v);
 if(hasMixed(answer)){
   var t=String(typed||'').trim();
   if(t&&/mixed number/i.test(prompt||'')&&!hasMixed(t)&&/\d\/\d/.test(t))return {status:'invalid',message:'Write your answer as a mixed number, such as 2 1/3.'};
   return gradeBank(improper(answer),improper(t),prompt);
 }
 return null;
}
function grade7Supports(answer){if(typeof answer!=='string')return false;if(repeatingKey(answer)||inequalityKey(answer))return true;if(hasMixed(answer))return API.bankAnswer(improper(answer))!==null;return false;}
/* Grade 6 audit #1 (2026-11-19): short answers that used to be self-checked.
   - "Quadrant IV", "x-axis", "origin": IV, 4, Q4 and "quadrant 4" are accepted.
   - Comparison symbols for "Compare using <, >, or =": the symbol, or the words "less than", "greater than", "equal".
   - A named choice that appears in the prompt ("Mix A", "Town B"): the same name, any case.
   - Equations in letters ("c = 12n", "11n = 605", "k - 13 = 83"): any equation whose two sides differ by the same
     expression, so 12n = c and c = n × 12 match c = 12n; an equation scaled by a number is a different equation.
   - Expressions: for "Write an expression" any equivalent expression; for "Simplify" or "Use the Distributive Property"
     the typed answer must be equivalent AND simplified (no parentheses, one term per variable and one constant).
   - Compound answers "-10 < -9; the diver" and "Femi, $20": each part is graded, in order. */
var ROMAN={i:1,ii:2,iii:3,iv:4,'1':1,'2':2,'3':3,'4':4};
function quadrant(s){var t=String(s||'').toLowerCase().replace(/[−–]/g,'-').replace(/\s+/g,' ').trim();if(/^(the )?origin$/.test(t))return 'origin';if(/^(the )?x[- ]?axis$/.test(t))return 'x-axis';if(/^(the )?y[- ]?axis$/.test(t))return 'y-axis';var m=/^(?:quadrant|q)? ?(iv|iii|ii|i|[1-4])$/.exec(t);return m?'Q'+ROMAN[m[1]]:null;}
function symbolWord(s){var t=String(s||'').trim().toLowerCase();return {'<':'<','>':'>','=':'=','less than':'<','is less than':'<','greater than':'>','is greater than':'>','equal':'=','equals':'=','equal to':'=','is equal to':'='}[t]||null;}
function label(s){return String(s||'').toLowerCase().replace(/^the\s+/,'').replace(/\s+/g,' ').trim();}
function isLabel(answer,prompt){return /^[A-Z][a-z]+(?: [A-Z0-9])?$|^[A-Z]$/.test(answer)&&new RegExp('\\b'+answer.replace(/\s+/g,'\\s+')+'\\b').test(prompt||'');}
function letterEq(s){var t=normalize(String(s||'')).replace(/×|\*/g,'*');var m=/^([^=<>]+)=([^=<>]+)$/.exec(t);return m&&/[a-zA-Z]/.test(t)&&!/\\/.test(t)?[m[1].trim(),m[2].trim()]:null;}
function simplified(t){t=String(t).replace(/\s+/g,'');if(/[()]/.test(t))return false;var terms=t.replace(/^\+/,'').split(/(?=[+-])/).filter(Boolean),seen={},consts=0;for(var i=0;i<terms.length;i++){var v=terms[i].replace(/[^a-z]/gi,'');if(!v){if(++consts>1)return false;}else{if(seen[v])return false;seen[v]=1;}}return true;}
function numCmp(s){var m=/^\s*(-?[\d.]+(?:\/\d+)?)\s*(<=|>=|<|>|≤|≥|=)\s*(-?[\d.]+(?:\/\d+)?)\s*$/.exec(String(s||'').replace(/[−–]/g,'-').replace(/\$/g,''));return m?[rational(m[1]),m[2].replace('<=','≤').replace('>=','≥'),rational(m[3])]:null;}
/* Grade 6 and Grade 7 practice tests only (Grade 6 audit #1): an equivalent expression or equation is not always the
   answer in later courses (vertex form, function notation), and 8th Grade Math has its own grader (grade8-grading.js),
   which requires the setup equation ("33 + 20c = 133", not "20c = 100"). practice.js sets MK_PRACTICE_COURSE; tests that
   load the graders without it get this grader. */
function grade6On(){return !G.MK_PRACTICE_COURSE||G.MK_PRACTICE_COURSE==='math6'||G.MK_PRACTICE_COURSE==='prealgebra7';}
/* Grade 5 audit (2026-11-19, #2 and #3): Grade 5 answers that used to fall back to self-checking.
   - "greater than", "less than 1", "equal to" and the symbols: the words and the symbols are the same answer.
   - Remainders "90 R 2": also 90 r 2, 90 remainder 2.  Compound measures "5 feet 3 inches": also 5 ft 3 in.
   - A number with a unit the other graders do not know ("32 cubic units"): the number, with or without the unit.
   - A word answer named in the prompt or a Grade 5 term (acute, scalene, rhombus, overestimate, the x-axis, point D).
   - "Write ... in simplest form": an equal fraction that is not fully reduced (4/6 for 2/3) or a decimal is "not in the form
     asked"; an improper fraction in lowest terms (5/4 for 1 1/4) is accepted. "As a mixed number" requires a mixed number. */
var G5WORDS=/^(acute|right|obtuse|scalene|isosceles|equilateral|square|rectangle|rhombus|parallelogram|trapezoid|kite|quadrilateral|triangle|pentagon|hexagon|octagon|polygon|overestimate|underestimate|(?:acute|right|obtuse) (?:scalene|isosceles|equilateral))$/;
var G5UNIT='(?:cubic|square) (?:units?|inch(?:es)?|feet|foot|yards?|meters?|centimeters?)|units?|inch(?:es)?|feet|foot|yards?|miles?|ounces?|fluid ounces?|pounds?|tons?|cups?|pints?|quarts?|gallons?|grams?|kilograms?|milligrams?|meters?|centimeters?|millimeters?|kilometers?|liters?|milliliters?|minutes?|hours?|seconds?|days?|weeks?|sides?|cubes?|layers?|pieces?|students?|people|boxes|bags|teams|tables|buses|vans|cars|rows';
var G5ABBR={ft:'foot','in':'inch',yd:'yard',mi:'mile',lb:'pound',lbs:'pound',oz:'ounce','fl oz':'fluid ounce',qt:'quart',pt:'pint',gal:'gallon',c:'cup',t:'ton',g:'gram',kg:'kilogram',mg:'milligram',m:'meter',cm:'centimeter',mm:'millimeter',km:'kilometer',l:'liter',ml:'milliliter',min:'minute',hr:'hour',h:'hour',sec:'second',s:'second','cu units':'cubic unit','sq units':'square unit'};
function g5unit(u){var w=String(u||'').toLowerCase().replace(/\./g,'').replace(/\s+/g,' ').trim();w=G5ABBR[w]||w.replace(/^cu /,'cubic ').replace(/^sq /,'square ');return w.replace(/feet/g,'foot').replace(/inches/g,'inch').replace(/people/,'person').replace(/(ch|sh|x|bus)es\b/g,'$1').replace(/s\b/g,'');}
function g5cmp(s){var t=String(s||'').toLowerCase().replace(/[−–]/g,'-').replace(/\s+/g,' ').trim(),W={'greater than':'>','more than':'>','less than':'<','equal to':'=','equals':'=','the same as':'='};for(var w in W)if(t===w||t.indexOf(w+' ')===0)return W[w]+t.slice(w.length).replace(/\s/g,'');return /^[<>=]/.test(t)?t.replace(/\s/g,''):null;}
function g5num(s){var m=/^\s*\$?\s*(\d[\d,]*\s+\d+\/\d+|\d+\/\d+|\d[\d,]*(?:\.\d+)?|\.\d+)\s*(.*)$/.exec(String(s||'').replace(/[‑]/g,'-'));if(!m)return null;var n=m[1].replace(/,/g,''),mx=/^(\d+)\s+(\d+)\/(\d+)$/.exec(n);if(mx)n=(+mx[1]*+mx[3]+ +mx[2])+'/'+mx[3];try{return {v:rational(n),u:m[2].trim()};}catch(e){return null;}}
function g5form(prompt){var t=String(prompt||'').toLowerCase();return /simplest form|lowest terms|\bsimplify\b/.test(t)?'simplest':/as a mixed number/.test(t)?'mixed':'';}
function g5formOk(t,key,form){var mt=/^\s*\d+\s+(\d+)\s*\/\s*(\d+)\s*$/.exec(t),ft=/^\s*(\d+)\s*\/\s*(\d+)\s*$/.exec(t),mixedKey=/^\d+ \d+\/\d+$/.test(key),fracKey=/^\d+\/\d+$/.test(key),gcd=function(a,b){return b?gcd(b,a%b):a;};
 if(form==='mixed')return !!mt||(!ft&&!/\./.test(t));
 if(!mixedKey&&!fracKey)return !mt&&!ft;var n=mt?+mt[1]:ft?+ft[1]:null,d=mt?+mt[2]:ft?+ft[2]:null;if(n===null)return false;return gcd(n,d)===1&&(!mt||n<d);}
/* Elementary, Grade 6 and Grade 7 practice tests only, like the Grade 6 reader: in later courses a number without its
   unit or a word named in the prompt is not always the answer, and 8th Grade Math has its own grader. practice.js sets
   MK_PRACTICE_COURSE; tests that load the graders without it get this grader. */
function grade5On(){var c=G.MK_PRACTICE_COURSE;return !c||/^grade[1-5]$|^math[1-6]$|^prealgebra7$/.test(c);}
function grade5Kind(answer,prompt){
 if(typeof answer!=='string'||!grade5On())return null;var a=answer.trim(),p=String(prompt||'');
 if(g5form(p)&&(/^\d+ \d+\/\d+$|^\d+\/\d+$/.test(a)||(/^\d+$/.test(a)&&/\d\/\d/.test(p))))return 'form';
 if(/^(greater|less|more) than(?: \S+)?$|^equal to$/.test(a)||(/^[<>=]$/.test(a)&&!/compare using/i.test(p)))return 'cmp';
 if(/^\d[\d,]* R \d+$/.test(a))return 'remainder';
 if(new RegExp('^\\d[\\d,]* (?:'+G5UNIT+') \\d+ (?:'+G5UNIT+')$').test(a))return 'compound';
 if(/^(?:the )?[xy][‑-]axis$/.test(a))return 'axis';
 if(/^point [A-Z]$/.test(a))return 'point';
 if(G5WORDS.test(a)||(/^[a-z][a-z ‑-]{1,30}$/.test(a)&&a.split(' ').length<=3&&new RegExp('\\b'+a.replace(/[‑-]/g,'[‑-]')+'\\b','i').test(p)&&/\bor\b|which|classify|name/i.test(p)))return 'word';
 if(new RegExp('^\\$?\\d[\\d,]*(?:\\.\\d+)?(?: \\d+/\\d+)? (?:'+G5UNIT+')$').test(a)&&bankAnswer(a)===null)return 'num-unit';
 return null;
}
function grade5(answer,typed,prompt){
 var kind=grade5Kind(answer,prompt);if(!kind)return null;
 var t=String(typed==null?'':typed).trim(),a=answer.trim();if(!t)return {status:'empty'};
 if(t.length>120)return {status:'invalid',message:'Enter only your final answer.'};
 var norm=function(s){return String(s).toLowerCase().replace(/[‑–]/g,'-').replace(/^(the|a|an) /,'').replace(/[.!]+$/,'').replace(/\s+/g,' ').trim();};
 try{
  if(kind==='form'){var kn=g5num(a),tn=g5num(t);if(!tn||tn.u)return {status:'invalid',message:'Enter a number such as 2/3 or 1 1/2.'};if(!kn.v.eq(tn.v))return {status:'incorrect'};return g5formOk(t,a,g5form(prompt))?{status:'correct'}:{status:'invalid',message:g5form(prompt)==='mixed'?'Write your answer as a mixed number.':'That is equal, but not in simplest form. Simplify completely.'};}
  if(kind==='cmp'){var c=g5cmp(t);return c?{status:c===g5cmp(a)?'correct':'incorrect'}:{status:'invalid',message:'Answer with greater than, less than or equal to (or >, <, =).'};}
  if(kind==='remainder'){var r=/^([\d,]+)\s*(?:r|rem|remainder)\.?\s*(\d+)$/i.exec(t),k=/^([\d,]+) R (\d+)$/.exec(a);return r?{status:+r[1].replace(/,/g,'')===+k[1].replace(/,/g,'')&&+r[2]===+k[2]?'correct':'incorrect'}:{status:'invalid',message:'Write the quotient and remainder, such as 12 R 3.'};}
  if(kind==='compound'){var re=/^([\d,]+)\s*([a-z. ]+?)\s*,?\s*(?:and\s+)?([\d,]+)\s*([a-z. ]+)$/i,x=re.exec(t),y=re.exec(a);if(!x)return {status:'invalid',message:'Give both parts, such as 5 feet 3 inches.'};return {status:+x[1].replace(/,/g,'')===+y[1].replace(/,/g,'')&&+x[3]===+y[3]&&g5unit(x[2])===g5unit(y[2])&&g5unit(x[4])===g5unit(y[4])?'correct':'incorrect'};}
  if(kind==='axis'){var q=/^(?:the )?([xy])[\s‑-]*axis$/i.exec(t);return q?{status:q[1].toLowerCase()===/([xy])/.exec(a)[1]?'correct':'incorrect'}:{status:'invalid',message:'Answer x-axis or y-axis.'};}
  if(kind==='point'){var pt=/^(?:point\s+)?([A-Z])$/i.exec(t);return pt?{status:pt[1].toUpperCase()===a.slice(-1)?'correct':'incorrect'}:{status:'invalid',message:'Give the letter of the point.'};}
  if(kind==='word')return {status:norm(t)===norm(a)?'correct':'incorrect'};
  if(kind==='num-unit'){var kv=g5num(a),tv=g5num(t);if(!tv)return {status:'invalid',message:'Enter a number, with or without its unit.'};if(tv.u&&g5unit(tv.u)!==g5unit(kv.u))return {status:'incorrect'};return {status:tv.v.eq(kv.v)?'correct':'incorrect'};}
 }catch(e){return {status:'invalid',message:'Answer format could not be read.'};}
 return null;
}
function grade6Kind(answer,prompt){
 if(typeof answer!=='string'||!C||!grade6On())return null;
 var a=answer.trim();
 if(/[a-zA-Z]\s*\(/.test(a)&&!/^\s*\(/.test(a)&&/[a-zA-Z]\s*\([^)]*\)\s*[=<>]|=\s*[a-zA-Z]\s*\(/.test(a))return null;   // function notation (T(2) = 61, f(-x) = f(x)) is not a product
 if(quadrant(a)&&/quadrant|where is the point/i.test(prompt||''))return 'quadrant';
 if(/^[<>=]$/.test(a)&&/compare using/i.test(prompt||''))return 'symbol';
 if(isLabel(a,prompt))return 'label';
 var parts=a.split(/\s*;\s*/);
 if(parts.length===2&&numCmp(parts[0])&&/^(?:the )?[A-Za-z]+(?: [A-Z])?$/.test(parts[1]))return 'cmp-label';
 if(/^[A-Z][a-z]+, \$\d+(?:\.\d\d)?$/.test(a))return 'name-amount';
 var e=/^[\da-z\s+\-*/().=×]+$/i.test(a)&&!/^\s*[a-z]\s*=\s*-?[\d.\/\s]+$/i.test(a)&&!/^\s*y\s*=/i.test(a)&&!/[a-z]{2}/i.test(a)?letterEq(a):null;if(e){try{C.parseExpr(e[0]);C.parseExpr(e[1]);return 'equation';}catch(x){return null;}}
 if(/[a-z]/i.test(a)&&!/[a-z]{2}/i.test(a)&&!/\bi\b|[a-z]\s*\(/i.test(a)&&!/[=<>;,]/.test(a)&&/^[\d\sa-z+\-*/().×÷]+$/i.test(a)&&/\b(?:write an? (?:algebraic )?expression|simplify|distributive property)\b/i.test(prompt||'')){try{C.parseExpr(normalize(a));return 'expression';}catch(x){return null;}}
 return null;
}
function grade6(answer,typed,prompt){
 var kind=grade6Kind(answer,prompt);if(!kind)return null;
 var t=String(typed==null?'':typed).trim();if(!t)return {status:'empty'};
 if(t.length>180)return {status:'invalid',message:'Enter only your final answer (180 characters maximum).'};
 try{
  if(kind==='quadrant'){var q=quadrant(t);return q?{status:q===quadrant(answer)?'correct':'incorrect'}:{status:'invalid',message:'Name the quadrant, such as Quadrant II, or say x-axis, y-axis or origin.'};}
  if(kind==='symbol'){var y=symbolWord(t);return y?{status:y===answer.trim()?'correct':'incorrect'}:{status:'invalid',message:'Enter <, > or =.'};}
  if(kind==='label')return {status:label(t)===label(answer)?'correct':'incorrect'};
  if(kind==='name-amount'){var p=t.split(/\s*[,;]\s*|\s+by\s+|\s+and\s+/);if(p.length!==2)return {status:'invalid',message:'Give the name and the amount, separated by a comma, such as Kai, $5.'};var k=answer.split(/,\s*/);return {status:label(p[0])===label(k[0])&&rational(p[1].replace(/\$/g,'')).eq(rational(k[1].replace(/\$/g,'')))?'correct':'incorrect'};}
  if(kind==='cmp-label'){var tp=t.split(/\s*;\s*|\s*,\s*(?=[a-z])/i);if(tp.length!==2)return {status:'invalid',message:'Write the inequality, then a semicolon, then the answer to the question, such as -4 < 2; Town B.'};var ka=answer.split(/\s*;\s*/),kc=numCmp(ka[0]),tc=numCmp(tp[0]);if(!tc)return {status:'invalid',message:'Write the inequality with the two numbers, such as -4 < 2.'};var sameOp=function(a,b){return a.replace('≤','<').replace('≥','>')===b.replace('≤','<').replace('≥','>');};return {status:kc[0].eq(tc[0])&&kc[2].eq(tc[2])&&sameOp(kc[1],tc[1])&&label(tp[1])===label(ka[1])?'correct':'incorrect'};}
  if(kind==='equation'){var ke=letterEq(answer),te=letterEq(t);if(!te)return {status:'invalid',message:'Enter an equation with an equals sign, such as c = 12n.'};var kd='('+ke[0]+')-('+ke[1]+')',td='('+te[0]+')-('+te[1]+')';return {status:C.equivalent(kd,td)||C.equivalent(kd,'-('+td+')')?'correct':'incorrect'};}
  if(kind==='expression'){var n=normalize(t).replace(/×/g,'*').replace(/÷/g,'/');if(/[=<>]/.test(n))return {status:'invalid',message:'Enter an expression without an equals sign.'};var ok=C.equivalent(normalize(answer),n);if(ok&&/\b(?:simplify|distributive property)\b/i.test(prompt||'')&&simplified(normalize(answer))&&!simplified(n))return {status:'invalid',message:'Simplify completely: multiply out and combine like terms.'};return {status:ok?'correct':'incorrect'};}
 }catch(e){return {status:'invalid',message:'Answer format could not be read.'};}
 return null;
}
/* Matrix dimensions ("What are the dimensions of A = [...]?" -> "2 × 3"): rows by columns, in that order. Read as a product,
   2 × 3 would accept 3 × 2 and 6 × 1. */
var DIMS=/^\s*(\d+)\s*(?:[×xX*]|by)\s*(\d+)\s*$/;
function gradeDims(answer,typed,prompt){
 if(typeof answer!=='string'||!/\bdimensions?\b/i.test(prompt||''))return null;var k=DIMS.exec(answer);if(!k)return null;
 var t=String(typed==null?'':typed).trim();if(!t)return {status:'empty'};var m=DIMS.exec(t);
 if(!m)return {status:'invalid',message:'Give the dimensions as rows × columns, such as 2 × 3.'};
 return {status:+m[1]===+k[1]&&+m[2]===+k[2]?'correct':'incorrect'};
}
function gradeBank(answer,typed,prompt){
 var gd=gradeDims(answer,typed,prompt);if(gd)return gd;
 var g5=grade5(answer,typed,prompt);if(g5)return g5;
 var g6=grade6(answer,typed,prompt);if(g6)return g6;
 var g7=grade7(answer,typed,prompt);if(g7)return g7;
 if(gr8On()&&typeof answer==='string'){if(G.MKGRADE8.preferred(answer,prompt))return G.MKGRADE8.grade(answer,typed,prompt);typed=G.MKGRADE8.normalizeTyped(typed);}
 if(calcOn()&&typeof answer==='string'&&(G.MKCALC.preferred(answer)||(/Factor completely/i.test(prompt||'')&&G.MKCALC.supports(answer))))return G.MKCALC.grade(answer,typed,prompt);
 var key=bankAnswer(answer);
 if(key===null)return exactKey(answer)!==null?G.MKEXACT.grade(answer,typed):discreteKey(answer)!==null?G.MKDISCRETE.grade(answer,typed):calcKey(answer)!==null?G.MKCALC.grade(answer,typed,prompt):statKey(answer)!==null?G.MKSTAT.grade(answer,typed,prompt):gr8Key(answer,prompt)!==null?G.MKGRADE8.grade(answer,typed,prompt):{status:'self'};
 var input=bankCore(typed).text;
 return grade({parts:[{answer:key}]},input);
}
API.supports=supports;API.grade=grade;API.bankAnswer=function(answer,prompt){if(grade5Kind(answer,prompt))return answer;if(grade6Kind(answer,prompt))return answer;if(grade7Supports(answer))return answer;var k=bankAnswer(answer);if(k!==null)return k;k=exactKey(answer);if(k!==null)return k;k=discreteKey(answer);if(k!==null)return k;k=calcKey(answer);if(k!==null)return k;k=statKey(answer);return k!==null?k:gr8Key(answer,prompt);};API.gradeBank=gradeBank;
})(window);
