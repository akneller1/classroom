/* Exact comparison for real numeric radical expressions, with no floating-point approximations. */
(function(G){
'use strict';
var API=G.MKRADICAL={};
function rat(n,d){n=BigInt(n);d=BigInt(d===undefined?1:d);if(!d)throw Error('division by zero');if(d<0n){n=-n;d=-d;}var a=n<0n?-n:n,b=d;while(b){var t=a%b;a=b;b=t;}var g=a||1n;return [n/g,d/g];}
function plus(a,b){return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function times(a,b){return rat(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return rat(a[0]*b[1],a[1]*b[0]);}
function num(s){s=s.trim();if(!/^\d+(?:\.\d+)?$/.test(s))throw Error('not a number');var parts=s.split('.'),fraction=parts[1]||'';return rat(BigInt(parts[0]+fraction),10n**BigInt(fraction.length));}
function normalize(s){
 return String(s||'').replace(/[⟨⟩]/g,'').replace(/[−–]/g,'-').replace(/\\left|\\right|\\,/g,'').replace(/\\cdot|\\times/g,'*').replace(/\s+/g,'')
 .replace(/\\frac\{(\d+)\}\{(\d+)\}/g,'($1/$2)')
 .replace(/\\sqrt\{([^{}]+)\}/g,'sqrt($1)').replace(/√\(([^()]+)\)/g,'sqrt($1)').replace(/√(\d+)/g,'sqrt($1)')
 .replace(/^x=/,'');
}
function sqrtPart(r){ // Rational radicand; keep a square-free integer radicand and exact rational coefficient.
 if(r[0]<0n)throw Error('negative radicand');
 if(r[0]>1000000n||r[1]>1000000n)throw Error('radicand too large');
 var n=r[0]*r[1],coef=rat(1n,r[1]);
 var outside=1n,inside=n;
 for(var f=2n;f*f<=inside;f++){while(inside%(f*f)===0n){inside/=f*f;outside*=f;}}
 return {rad:String(inside),coef:times(coef,rat(outside))};
}
function parse(s){
 s=normalize(s);
 if(!s||s.length>180||/[^0-9a-z()+*/.^-]/i.test(s))throw Error('unsupported expression');
 // Only additive combinations of numeric rational terms and square roots.
 // Prevent implied functions, variables, powers, and unsafe parentheses.
 var result={};
 var terms=s.replace(/^\+/,'').replace(/-/g,'+-').split('+').filter(Boolean);
 if(!terms.length)throw Error('missing expression');
 terms.forEach(function(term){
  var sign=1n;
  if(term[0]==='-'){sign=-1n;term=term.slice(1);}
  var m=/^(?:(\d+(?:\.\d+)?)(?:\*?)?)?sqrt\((\d+(?:\.\d+)?(?:\/\d+(?:\.\d+)?)?)\)(?:\/(\d+(?:\.\d+)?))?$/.exec(term);
  // Simplified fractions on their own, including fraction templates 3/4.
  var normal=/^(\d+(?:\.\d+)?)(?:\/(\d+(?:\.\d+)?))?$/.exec(term);
  var rad='1',coef;
  if(m){
   var r=m[2].split('/'),radicand=r.length===2?div(num(r[0]),num(r[1])):num(r[0]);
   var part=sqrtPart(radicand);rad=part.rad;
   coef=times(part.coef,m[1]?num(m[1]):rat(1n));
   if(m[3])coef=div(coef,num(m[3]));
  }else if(normal){
   coef=normal[2]?div(num(normal[1]),num(normal[2])):num(normal[1]);
  }else throw Error('unsupported term');
  if(sign<0n)coef=times(coef,rat(-1n));
  result[rad]=plus(result[rad]||rat(0n),coef);
 });
 return result;
}
function same(a,b){
 var keys=new Set(Object.keys(a).concat(Object.keys(b)));
 for(var key of keys){
  var x=a[key]||rat(0n),y=b[key]||rat(0n);
  if(x[0]!==y[0]||x[1]!==y[1])return false;
 }
 return true;
}
API.supports=function(s){try{var source=normalize(s);if(!/sqrt|√/.test(source))return false;parse(source);return true;}catch(e){return false;}};
API.grade=function(answer,input){
 try{return {status:same(parse(answer),parse(input))?'correct':'incorrect'};}
 catch(e){return {status:'invalid',message:'Enter radicals as sqrt(12), 2sqrt(3), or sqrt(8)/2. Use + or - to combine terms.'};}
};
})(window);