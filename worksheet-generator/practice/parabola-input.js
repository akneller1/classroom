/* Five-point parabola plotting for verified vertex-form and standard-form graph questions. */
(function(G){
'use strict';
var API=G.MKPARABOLA={};
function number(s){if(s===''||s==='+')return 1;if(s==='-')return -1;if(!/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)$/.test(s))return null;var n=Number(s);return Number.isFinite(n)?n:null;}
function target(q){
 var p=q.problem;if(!p||!p.parts||p.parts.length!==1||!/\b(graph|plot|draw)\b/i.test((p.prompt||'')+' '+(p.parts[0].prompt||'')))return null;
 var source=(p.parts[0].check&&p.parts[0].check.type==='quad-graph'&&p.parts[0].check.eq)||p.parts[0].answer||'';
 var s=String(source).replace(/[⟨⟩]/g,'').replace(/\\left|\\right|\\,/g,'')
 .replace(/\\cdot/g,'').replace(/\\frac\{(-?\d+)\}\{(\d+)\}/g,(_,a,b)=>String(Number(a)/Number(b)))
 .replace(/\s+/g,'').replace(/−/g,'-').replace(/\^\{2\}/g,'^2');
 if(!s.startsWith('y='))return null;
 var rhs=s.slice(2),m,coef,h,k;
 // a(x-h)^2+k (also a(x)^2+k and (x+h)^2)
 m=/^([+-]?(?:\d+(?:\.\d+)?|\.\d+)?)\((x(?:[+-]\d+(?:\.\d+)?)?)\)\^2([+-]\d+(?:\.\d+)?)?$/.exec(rhs);
 if(m){coef=number(m[1]);h=-(Number(m[2].slice(1))||0);k=Number(m[3]||0);if(coef&&Number.isFinite(h)&&Number.isFinite(k))return {a:coef,h:h,k:k};}
 // ax^2+bx+c where either b or c may be absent.
 m=/^([+-]?(?:\d+(?:\.\d+)?|\.\d+)?)x\^2((?:[+-](?:\d+(?:\.\d+)?|\.\d+)?)x)?([+-]\d+(?:\.\d+)?)?$/.exec(rhs);
 if(!m)return null;
 coef=number(m[1]);if(!coef)return null;
 var term=m[2]||'',b=term?number(term.slice(0,-1)):0,c=Number(m[3]||0);
 if(b===null||!Number.isFinite(c))return null;
 h=-b/(2*coef);k=coef*h*h+b*h+c;
 return Number.isFinite(h)&&Number.isFinite(k)?{a:coef,h:h,k:k}:null;
}
API.target=target;
function read(q){if(typeof q.response!=='string'||!q.response.startsWith('parabola:'))return [];try{var p=JSON.parse(q.response.slice(9));return Array.isArray(p)?p:[];}catch(e){return [];}}
function plotSVG(points){
 var s='<svg class="pt-parabola-svg" viewBox="0 0 340 340" role="img" aria-label="Interactive grid for plotting five parabola points">';
 for(var i=-10;i<=10;i++){var v=170+i*15;s+='<path d="M'+v+' 20V320 M20 '+v+'H320" stroke="#e0e8ef"/>';}
 s+='<path d="M170 20V320 M20 170H320" stroke="#667b8d" stroke-width="2"/>';
 if(points.length===5){
 var sorted=points.slice().sort((a,b)=>a[0]-b[0]),path='';
 // A quadratic through the 5-point set is drawn only if all x-values differ.
 if(new Set(sorted.map(p=>p[0])).size===5){
 var p0=sorted[0],p1=sorted[1],p2=sorted[2],u=(p1[1]-p0[1])/(p1[0]-p0[0]),v=(p2[1]-p1[1])/(p2[0]-p1[0]),a=(v-u)/(p2[0]-p0[0]),b=u-a*(p0[0]+p1[0]),c=p0[1]-a*p0[0]*p0[0]-b*p0[0];
 for(var x=-10;x<=10.00001;x+=.1){var y=a*x*x+b*x+c;if(Math.abs(y)>15)continue;path+=(path?'L':'M')+(170+x*15)+' '+(170-y*15)+' ';}
 s+='<path d="'+path+'" fill="none" stroke="#2263ac" stroke-width="2.5"/>';
 }
 }
 points.forEach(function(p,j){s+='<circle cx="'+(170+p[0]*15)+'" cy="'+(170-p[1]*15)+'" r="5.5" fill="'+(j===0?'#d86728':'#2362ab')+'" stroke="white" stroke-width="2"/>';});
 return s+'</svg>';
}
API.render=function(q,i){var pts=read(q);return '<div class="pt-parabola-editor" data-parabola="'+i+'"><strong>Plot five points: vertex first, then two on each side.</strong><p class="pt-muted">Click grid intersections or enter coordinates. Choose the vertex as point 1. Points may be entered in any order after the vertex.</p>'+plotSVG(pts)+'<div class="pt-actions"><button type="button" data-clear-parabola class="pt-secondary">Erase and start over</button><button type="button" data-undo-parabola class="pt-secondary">Undo point</button></div><p class="pt-muted">'+pts.length+' of 5 points plotted</p><div class="pt-interval-row"><label>x<input type="text" inputmode="decimal" data-px></label><label>y<input type="text" inputmode="decimal" data-py></label><button type="button" data-add-parabola-point>Add point</button></div></div>';};
API.grade=function(q){var t=target(q),p=read(q);if(!t||p.length!==5)return {status:'incorrect'};if(!p.every(v=>Array.isArray(v)&&v.length===2&&v.every(Number.isFinite)))return {status:'incorrect'};
 var xs=p.map(v=>v[0]);if(new Set(xs).size!==5)return {status:'incorrect'};
 var vertex=p[0],tol=1e-7;if(Math.abs(vertex[0]-t.h)>tol||Math.abs(vertex[1]-t.k)>tol)return {status:'incorrect'};
 if(p.filter(v=>v[0]<t.h).length!==2||p.filter(v=>v[0]>t.h).length!==2)return {status:'incorrect'};
 return {status:p.every(v=>Math.abs(v[1]-(t.a*(v[0]-t.h)**2+t.k))<tol)?'correct':'incorrect'};
};
API.bind=function(root,state,save){
 root.querySelectorAll('[data-parabola]').forEach(function(box){var i=+box.dataset.parabola,q=state.questions[i];
 function redraw(pts){q.response='parabola:'+JSON.stringify(pts);save();box.outerHTML=API.render(q,i);API.bind(root,state,save);}
 function add(x,y){var pts=read(q);if(pts.length>=5||pts.some(p=>p[0]===x))return;pts.push([x,y]);redraw(pts);}
 box.querySelector('svg').onclick=function(e){var rect=this.getBoundingClientRect(),x=Math.round(((e.clientX-rect.left)/rect.width*340-170)/15),y=Math.round((170-(e.clientY-rect.top)/rect.height*340)/15);add(Math.max(-10,Math.min(10,x)),Math.max(-10,Math.min(10,y)));};
 box.querySelector('[data-clear-parabola]').onclick=()=>redraw([]);
 box.querySelector('[data-undo-parabola]').onclick=()=>{var p=read(q);p.pop();redraw(p);};
 box.querySelectorAll('[data-negative]').forEach(btn=>btn.onclick=function(){var el=box.querySelector(btn.dataset.negative==='x'?'[data-px]':'[data-py]');el.value=el.value.startsWith('-')?el.value.slice(1):'-'+el.value;});box.querySelector('[data-add-parabola-point]').onclick=()=>{var x=box.querySelector('[data-px]').value,y=box.querySelector('[data-py]').value;if(x!==''&&y!==''&&Number.isFinite(+x)&&Number.isFinite(+y))add(+x,+y);};
 });
};
})(window);