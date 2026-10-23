/* Inequalities: solve AND graph from basic through advanced multi-step. */
(function(G){'use strict';
var N=G.MKWS,T=N.tex,M=T.M,U='algebra1-inequalities',unit=N.registry.units[U];if(!unit)return;
function signed(n){return n<0?String(n):'+'+n}
function cmp(c){return c==='>'?'\\gt':c==='<'?'\\lt':c==='>='?'\\ge':'\\le'}
function inverse(c){return {'>':'<','<':'>','>=':'<=','<=':'>='}[c]}
function nl(limit,op,show){
 var min=-9,max=9,W=480,z=240,step=23.3,point=z+limit*step;
 var h=['<svg xmlns="http://www.w3.org/2000/svg" width="4.3in" viewBox="0 0 480 94" role="img" aria-label="number line">','<line x1="15" y1="38" x2="465" y2="38" stroke="#161616" stroke-width="2.4"/>','<path d="M15 38l9 -5v10z M465 38l-9 -5v10z" fill="#161616"/>'];
 for(var t=min;t<=max;t++){var xx=z+step*t;h.push('<path d="M'+xx+' 31v14" stroke="#171717" stroke-width="1.3"/><text x="'+xx+'" y="61" text-anchor="middle" font-size="11" font-family="Arial" fill="#111">'+t+'</text>');}
 if(show){var left=op[0]==='<',closed=op.indexOf('=')>=0,endpoint=left?21:459;
 h.push('<path d="M'+point+' 38H'+endpoint+'" stroke="#111" stroke-width="4.6"/>');
 h.push('<circle cx="'+point+'" cy="38" r="6.3" stroke="#111" stroke-width="2.2" fill="'+(closed?'#111':'white')+'"/>');}
 h.push('</svg>');return h.join('');
}
var modes=[
['One-step inequalities: solve and graph','one'],
['Two-step inequalities: solve and graph','two'],
['Negative coefficients: solve and graph','negative'],
['Variables on both sides: solve and graph','both'],
['Distributive property: solve and graph','distribute'],
['Combine like terms: solve and graph','combine'],
['Variables on both sides with distribution','bothDist'],
['Advanced: distribute, combine like terms, and graph','everything']
];
function generate(mode){return function(ctx){
 var r=ctx.rng,x=r.int(-6,6),a=r.int(2,6),b=r.int(1,7),c=r.int(1,5),d=r.int(1,4),op=['>','<','>=','<='][r.int(0,3)];
 var LC,RC,ls,rs,working=[],difference,finalOp=op;
 if(mode==='one'){LC=a;RC=0;ls=a+'x';rs=String(a*x);working=['Divide both sides by '+a+'.'];}
 if(mode==='two'){LC=a;RC=0;ls=a+'x'+signed(b);rs=String(a*x+b);working=['Subtract '+b+' from both sides.','Divide by '+a+'.'];}
 if(mode==='negative'){LC=-a;RC=0;ls='-'+a+'x'+signed(b);rs=String(-a*x+b);finalOp=inverse(op);working=['Subtract '+b+' from both sides.','Divide by -'+a+' and reverse the inequality.'];}
 if(mode==='both'){LC=a;RC=c;N.gen.need(a!==c);ls=a+'x'+signed(b);rs=c+'x'+signed((a-c)*x+b);difference=a-c;finalOp=difference<0?inverse(op):op;working=['Move x-terms to one side and constants to the other.','Divide by '+difference+(difference<0?', reversing the inequality.':'.')];}
 if(mode==='distribute'){LC=a;RC=0;ls=a+'(x+'+b+')';rs=String(a*(x+b));working=['Distribute '+a+' across the parentheses.','Divide by '+a+' and isolate x.'];}
 if(mode==='combine'){LC=a+c;RC=0;ls=a+'x+'+c+'x'+signed(b);rs=String((a+c)*x+b);working=['Combine '+a+'x and '+c+'x.','Subtract '+b+' and divide by '+(a+c)+'.'];}
 if(mode==='bothDist'){
  LC=a+c;RC=d;N.gen.need(LC!==RC);
  var lconst=a*b,rrconst=(LC-RC)*x+lconst;
  ls=a+'(x+'+b+')+'+c+'x';rs=d+'x'+signed(rrconst);
  difference=LC-RC;finalOp=difference<0?inverse(op):op;
  working=['Distribute '+a+'.','Combine x-terms on the left.','Collect variable terms, then divide by '+difference+'.'];
 }
 if(mode==='everything'){
  LC=a+c;RC=d+b;N.gen.need(LC!==RC);
  var leftConst=a*b+c, rightConst=leftConst+(LC-RC)*x;
  ls=a+'(x+'+b+')+'+c+'x+'+c;
  rs=d+'(x+'+b+')+'+b+'x'+signed(rightConst-d*b);
  difference=LC-RC;finalOp=difference<0?inverse(op):op;
  working=['Distribute on both sides.','Combine like terms on both sides.','Move variable terms to one side and constants to the other.','Divide by '+difference+(difference<0?' and reverse the inequality.':'.')];
 }
 var value=LC*x+(mode==='both'?b:0);
 var tex=ls+cmp(op)+rs;
 var answer='x'+cmp(finalOp)+x;
 var lhsConst=(mode==='one'||mode==='negative'||mode==='combine'||mode==='two')?null:0;
 var finalSteps=working.concat(['Simplified result: '+M(answer),'Graph: '+(finalOp.indexOf('=')>=0?'closed':'open')+' circle at '+x+', shade '+(finalOp[0]==='<'?'left':'right')+'.']);
 return {prompt:'Solve the inequality. Then graph your solution on the number line:<div>'+M(tex)+'</div><div>'+nl(0,'>',false)+'</div>',keyPrompt:'Solve and graph: '+M(tex),answer:M(answer)+'<div>'+nl(x,finalOp,true)+'</div>',steps:finalSteps,key:'sg-ineq|'+mode+'|'+tex,equiv:'sg-ineq|'+mode+'|'+tex};
};}
var cat={id:'solve-graph-advanced',letter:String.fromCharCode(65+unit.categories.length),name:'Solve & Graph Inequalities — Basic to Advanced',lessons:[]};
modes.forEach(function(m,i){var id='a1-inequalities-solve-graph-'+m[1];N.registerLesson({id:id,unit:U,category:cat.id,num:unit.categories.reduce(function(n,c){return n+c.lessons.length},0)+i+1,title:m[0],instruction:'Show algebraic steps, then use an open or closed circle and shade the number line.',layout:'full',space:[.5,.9,1.4],generate:generate(m[1])});cat.lessons.push(id)});
unit.categories.push(cat);
})(typeof window!=='undefined'?window:globalThis);