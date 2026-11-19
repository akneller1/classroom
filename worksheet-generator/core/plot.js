/* Shared graph responses. Rational checks are independent of the drawing code. */
(function(G){'use strict';
const statsTools=['histogram','box-plot'];
const functionTools=['exponential-asymptote','log','rational','polynomial','piecewise','sinusoid'];
const displayTools=['picture-graph','bar-graph','line-plot'];
const tools=[...statsTools,...functionTools,...displayTools,'number-line-point','points','number-line-inequality','line','system','region','abs','parabola','sqrt','cbrt','exponential'];
class R{
 constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error('Zero denominator');if(d<0n){n=-n;d=-d}let a=n<0n?-n:n,b=d;while(b){[a,b]=[b,a%b]}this.n=n/(a||1n);this.d=d/(a||1n)}
 add(v){v=F(v);return new R(this.n*v.d+v.n*this.d,this.d*v.d)}sub(v){v=F(v);return this.add(v.neg())}mul(v){v=F(v);return new R(this.n*v.n,this.d*v.d)}div(v){v=F(v);return new R(this.n*v.d,this.d*v.n)}neg(){return new R(-this.n,this.d)}abs(){return this.n<0n?this.neg():this}eq(v){v=F(v);return this.n===v.n&&this.d===v.d}cmp(v){v=F(v);const d=this.n*v.d-v.n*this.d;return d<0n?-1:d>0n?1:0}pow(k){return k<0?new R(this.d,this.n).pow(-k):new R(this.n**BigInt(k),this.d**BigInt(k))}isInt(){return this.d===1n}sign(){return this.n<0n?-1:this.n>0n?1:0}valueOf(){return Number(this.n)/Number(this.d)}toString(){return this.d===1n?String(this.n):this.n+'/'+this.d}
}
function F(v){if(v instanceof R)return v;const s=String(v).trim().replace(/−/g,'-');if(!/^[+-]?\d+(?:\.\d+)?(?:\/\d+)?$/.test(s))throw Error('Invalid coordinate');if(s.includes('/')){const [a,b]=s.split('/');return F(a).div(F(b))}if(s.includes('.')){const [a,b]=s.split('.'),d=10n**BigInt(b.length);return new R(BigInt(a||0)*d+BigInt(b)*(s.startsWith('-')?-1n:1n),d)}return new R(BigInt(s))}
const eq=(a,b)=>F(a).eq(b),pair=(a,b)=>eq(a[0],b[0])&&eq(a[1],b[1]);
function on(kind,t,p){const x=F(p[0]),y=F(p[1]),a=F(t.a??1),h=F(t.h??0),k=F(t.k??0),r=x.sub(h);if(kind==='line')return y.eq(F(t.m).mul(x).add(t.b));if(kind==='abs')return y.eq(a.mul(r.abs()).add(k));if(kind==='parabola')return y.eq(a.mul(r.pow(2)).add(k));if(kind==='sqrt'){const s=Math.round(Math.sqrt(+r));return +r>=0&&r.d===1n&&F(s).pow(2).eq(r)&&y.eq(a.mul(s).add(k))}if(kind==='cbrt'){const c=Math.round(Math.cbrt(+r));return F(c).pow(3).eq(r)&&y.eq(a.mul(c).add(k))}if(kind==='exponential')return x.d===1n&&Math.abs(+x)<1000&&y.eq(F(t.a).mul(F(t.b).pow(+x)));return false}
function check(p,r){try{return statsTools.includes(p.tool)?statsCheck(p,r):functionTools.includes(p.tool)?functionCheck(p,r):displayTools.includes(p.tool)?displayCheck(p,r):rawCheck(p,r)}catch(e){return {ok:false,code:'incomplete'}}}
function rawCheck(p,r){const t=p.target,kind=p.tool,yes={ok:true,code:null},no=code=>({ok:false,code});if(!r)return no('incomplete');
 if(kind==='number-line-point'){const a=t.values.map(F).sort((a,b)=>a.cmp(b)),b=r.values.map(F).sort((a,b)=>a.cmp(b));return a.length===b.length&&a.every((v,i)=>v.eq(b[i]))?yes:no(a.length!==b.length?'count':'position')}
 if(kind==='points'){const keys=pts=>new Set(pts.map(p=>F(p[0])+','+F(p[1]))),a=keys(t.points),b=keys(r.points),same=(a,b)=>a.size===b.size&&[...a].every(v=>b.has(v));return same(a,b)?yes:no(same(a,keys(r.points.map(([x,y])=>[y,x])))?'swapped-coordinates':'position')}
 if(kind==='number-line-inequality'){if('between'in t){if(r.between!==t.between)return no('and-or');for(const s of ['left','right']){if(!eq(r[s].value,t[s].value))return no('boundary');if(r[s].closed!==t[s].closed)return no('closed-open')}return yes}if(!eq(r.boundary,t.boundary))return no('boundary');if(r.direction!==t.direction)return no('direction');return r.closed===t.closed?yes:no('closed-open')}
 if(kind==='line'||kind==='exponential'){const [a,b]=r.points;if(pair(a,b))return no('same-point');if([a,b].every(pt=>on(kind,t,pt)))return yes;if(kind==='line'){const m=!eq(a[0],b[0])?F(b[1]).sub(a[1]).div(F(b[0]).sub(a[0])):null;if(m&&m.eq(t.m))return no('intercept');if(m&&m.eq(F(t.m).neg()))return no('slope-sign');if(m&&!eq(t.m,0)&&m.eq(F(1).div(t.m)))return no('slope-reciprocal');return no('slope')}return no('points-off-curve')}
 if(['abs','parabola','sqrt','cbrt'].includes(kind)){const [ax,ay]=r.anchor,[bx,by]=r.point,h=F(t.h),k=F(t.k);if(!pair([ax,ay],[h,k])){if(pair([ax,ay],[h.neg(),k]))return no('h-sign');if(pair([ax,ay],[h,k.neg()]))return no('k-sign');if(pair([ax,ay],[k,h]))return no('swapped-hk');return no('anchor')}if(eq(bx,h))return no('same-x');if(on(kind,t,[bx,by]))return yes;if(on(kind,{...t,a:F(t.a??1).neg()},[bx,by]))return no('a-sign');return no('stretch')}
 if(kind==='region'){const [a,b]=r.points;if(pair(a,b)||![a,b].every(pt=>on('line',t,pt)))return no('boundary-line');if(r.dashed!==['<','>'].includes(t.op))return no('dashed-solid');return r.shade===(['>','>=','≥'].includes(t.op)?'above':'below')?yes:no('shade-side')}
 if(kind==='system'){if(r.lines.length!==t.lines.length)return no('incomplete');for(let i=0;i<t.lines.length;i++){const result=rawCheck({tool:'line',target:t.lines[i]},{points:r.lines[i]});if(!result.ok)return no('line-'+result.code)}return pair(r.solution,t.solution)?yes:no('solution')}
 return no('incomplete');
}
function valid(p){if(p&&statsTools.includes(p.tool)){try{return !!(Array.isArray(p.target?.data)&&p.target.data.length&&p.answerKey&&/^question-banks\/assets\/[a-zA-Z0-9_/-]+\.png$/.test(p.answerKey.src)&&!p.answerKey.src.includes('..')&&typeof p.answerKey.alt==='string'&&(p.tool==='histogram'?p.bins?.width>0&&p.bins.count>0&&p.valueAxis?.max>0:p.axis&&F(p.axis.max).cmp(p.axis.min)>0))}catch(e){return false}}if(p&&displayTools.includes(p.tool))return validDisplay(p);const axes=p&&(p.grid||p.numberLine);return !!(p&&tools.includes(p.tool)&&p.target&&axes&&Number.isFinite(+axes.min||+axes.xmin||0)&&p.answerKey&&/^question-banks\/assets\/[a-zA-Z0-9_/-]+\.png$/.test(p.answerKey.src)&&!p.answerKey.src.includes('..')&&typeof p.answerKey.alt==='string')}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function geometry(p){const n=p.numberLine,g=p.grid||{},a=n||g;return {xmin:+(n?(a.min??a.xmin):g.xmin),xmax:+(n?(a.max??a.xmax):g.xmax),ymin:n?-1:+g.ymin,ymax:n?1:+g.ymax,snap:Number(F(a.snap??a.tick??a.step??1)),step:Number(F(a.tick??a.step??1)),number:!!n}}
function points(p,r){if(!r)return [];if(p.tool==='number-line-point')return r.values.map(v=>[Number(F(v)),0]);if(p.tool==='number-line-inequality')return 'between'in p.target?[[Number(F(r.left.value)),0],[Number(F(r.right.value)),0]]:[[Number(F(r.boundary)),0]];if(p.tool==='system')return [...r.lines.flat(),r.solution];if(r.anchor)return [r.anchor,r.point];return r.points||[]}
let clipCounter=0;
function blank(p,r,active){if(statsTools.includes(p.tool))return statsBlank(p,r);if(functionTools.includes(p.tool))return functionBlank(p,r,active);if(displayTools.includes(p.tool))return displayBlank(p,r);const clipId="plotClip"+(++clipCounter);const g=geometry(p),w=480,h=g.number?140:400,L=38,T=20,W=420,H=g.number?85:342,x=v=>L+(v-g.xmin)/(g.xmax-g.xmin)*W,y=v=>T+(g.ymax-v)/(g.ymax-g.ymin)*H;
 let out='<svg viewBox="0 0 '+w+' '+h+'" class="mk-plot-svg" role="group" aria-label="'+(g.number?'Interactive number line':'Interactive coordinate grid')+'"><defs><clipPath id="plotClip"><rect x="38" y="20" width="420" height="'+H+'"/></clipPath></defs><rect x="38" y="20" width="420" height="'+H+'" fill="white" stroke="#d5dbe3"/>';
 const y0=y(0);for(let v=g.xmin,i=0;v<=g.xmax+1e-8&&i<100;v+=g.step,i++){out+='<path d="M'+x(v)+' '+(g.number?y0-5:T)+' V'+(g.number?y0+5:T+H)+'" stroke="#d5dbe3"/>';if(g.number||Math.abs(v%2)<1e-8)out+='<text x="'+x(v)+'" y="'+(g.number?y0+24:Math.max(T+14,Math.min(T+H-3,y0+15)))+'" text-anchor="middle" font-size="11" fill="#344054">'+esc(p.numberLine&&p.numberLine.labelFormat==='decimal'?String(+v.toFixed(8)).replace('-','−'):F(v.toFixed(8)).toString())+'</text>'}
 if(!g.number)for(let v=Math.ceil(g.ymin);v<=g.ymax;v++){out+='<path d="M38 '+y(v)+' H458" stroke="#d5dbe3"/>';if(v&&v%2===0)out+='<text x="'+Math.max(15,Math.min(440,x(0)-8))+'" y="'+(y(v)+4)+'" text-anchor="end" font-size="11">'+v+'</text>'}
 out+='<path d="M38 '+y0+' H458'+(!g.number?' M'+x(0)+' 20 V362':'')+'" stroke="#1d2733" stroke-width="1.5"/>'+(g.number?'':'<text x="464" y="'+(y0-5)+'">x</text><text x="'+(x(0)+7)+'" y="15">y</text>');
 if(r){const pts=points(p,r);let paths=[];const line=(a,b)=>{if(a[0]===b[0])return null;const m=(b[1]-a[1])/(b[0]-a[0]),b0=a[1]-m*a[0];return {m,b:b0}};const drawLine=(a,b)=>{const l=line(a,b);if(l)paths.push('M'+x(g.xmin)+' '+y(l.m*g.xmin+l.b)+' L'+x(g.xmax)+' '+y(l.m*g.xmax+l.b))};
 if(['line','region'].includes(p.tool))drawLine(...pts);if(p.tool==='system'){drawLine(...pts.slice(0,2));drawLine(...pts.slice(2,4))}
 if(['abs','parabola','sqrt','cbrt','exponential'].includes(p.tool)){const [a,b]=pts;let fun;if(p.tool==='exponential'){if(a[0]!==b[0]&&a[1]>0&&b[1]>0){const base=(b[1]/a[1])**(1/(b[0]-a[0])),coef=a[1]/base**a[0];fun=x=>coef*base**x}}else if(a[0]!==b[0]){const f=x=>p.tool==='abs'?Math.abs(x):p.tool==='parabola'?x*x:p.tool==='sqrt'?(x<0?NaN:Math.sqrt(x)):Math.cbrt(x),coef=(b[1]-a[1])/f(b[0]-a[0]);fun=x=>coef*f(x-a[0])+a[1]}if(fun){let d='',pen=false;for(let i=0;i<=300;i++){const xx=g.xmin+(g.xmax-g.xmin)*i/300,yy=fun(xx);if(Number.isFinite(yy)){d+=(pen?' L':'M')+x(xx)+' '+Math.max(-10000,Math.min(10000,y(yy)));pen=true}else pen=false}paths.push(d)}}
 if(p.tool==='region'){const l=line(...pts);if(l){const edge=r.shade==='above'?T:T+H;out+='<path clip-path="url(#plotClip)" d="M38 '+edge+' H458 V'+y(l.m*g.xmax+l.b)+' L38 '+y(l.m*g.xmin+l.b)+' Z" fill="#1f5fa822"/>'}}
 if(p.tool==='number-line-inequality'){const segment=(a,b)=>out+='<path d="M'+x(a)+' '+y0+' H'+x(b)+'" stroke="#1f5fa8" stroke-width="6"/>';if('between'in p.target){const a=+F(r.left.value),b=+F(r.right.value);if(r.between)segment(a,b);else{segment(g.xmin,a);segment(b,g.xmax)}}else segment(r.direction==='left'?g.xmin:+F(r.boundary),r.direction==='left'?+F(r.boundary):g.xmax)}
 for(const d of paths)out+='<path clip-path="url(#plotClip)" d="'+d+'" fill="none" stroke="#1f5fa8" stroke-width="3"'+(r.dashed?' stroke-dasharray="7 5"':'')+'/>';
 pts.forEach((pt,i)=>{let closed=true;if(p.tool==='number-line-inequality')closed='between'in p.target?r[i?'right':'left'].closed:r.closed;out+='<circle data-handle="'+i+'" tabindex="0" role="button" aria-label="Point '+String.fromCharCode(65+i)+' at '+esc(pt.join(', '))+'" cx="'+x(pt[0])+'" cy="'+y(pt[1])+'" r="'+(i===active?9:7)+'" stroke="#1f5fa8" stroke-width="3" fill="'+(closed?'#1f5fa8':'white')+'"/><text x="'+(x(pt[0])+12)+'" y="'+(y(pt[1])-10)+'" font-size="13">'+String.fromCharCode(65+i)+'</text>'})}
 return (out+'</svg>').replace(/plotClip/g,clipId);
}
function initial(p){if(statsTools.includes(p.tool))return statsInitial(p);if(functionTools.includes(p.tool))return functionInitial(p);if(displayTools.includes(p.tool))return p.tool==='line-plot'?{marks:[]}:p.tool==='picture-graph'?{symbols:p.categories.map(()=>0)}:{values:p.categories.map(()=>p.valueAxis.min)};const kind=p.tool,zero=[0,0],nl=p.numberLine,z0=nl&&(+nl.min>0||+nl.max<0)?+nl.min:0;if(kind==='number-line-point')return {values:p.target.values.map(()=>z0)};if(kind==='points')return {points:p.target.points.map(()=>zero.slice())};if(kind==='number-line-inequality')return 'between'in p.target?{between:true,left:{value:z0,closed:false},right:{value:z0,closed:false}}:{boundary:z0,closed:false,direction:'right'};if(kind==='system')return {lines:[[[0,0],[1,0]],[[0,1],[1,1]]],solution:[0,0]};if(['line','region','exponential'].includes(kind))return {points:[[0,0],[1,1]],...(kind==='region'?{dashed:false,shade:'above'}:{})};return {anchor:[0,0],point:[1,1]}}
function create(host,p,opts={}){if(statsTools.includes(p.tool))return statsCreate(host,p,opts);if(functionTools.includes(p.tool))return functionCreate(host,p,opts);if(displayTools.includes(p.tool))return displayCreate(host,p,opts);let r=JSON.parse(JSON.stringify(opts.response||initial(p))),active=0;const g=geometry(p);let dragged=false;
 function moved(){opts.onChange?.(JSON.parse(JSON.stringify(r)))}
 function place(i,xx,yy){const snap=v=>Math.round(v/g.snap)*g.snap;xx=+Math.max(g.xmin,Math.min(g.xmax,snap(xx))).toFixed(8);yy=+Math.max(g.ymin,Math.min(g.ymax,snap(yy))).toFixed(8);const pt=[xx,yy];if(p.tool==='number-line-point')r.values[i]=F(String(xx)).toString();else if(p.tool==='number-line-inequality'){if('between'in p.target)r[i?'right':'left'].value=xx;else r.boundary=xx}else if(p.tool==='system'){if(i===4)r.solution=pt;else r.lines[Math.floor(i/2)][i%2]=pt}else if(r.anchor)r[i?'point':'anchor']=pt;else r.points[i]=pt;active=i;moved()}
 function draw(){host.innerHTML='<div class="mk-plot-canvas">'+blank(p,r,active)+'</div><div class="mk-plot-controls"><label>Point <select data-point>'+points(p,r).map((v,i)=>'<option value="'+i+'" '+(i===active?'selected':'')+'>'+String.fromCharCode(65+i)+(p.tool==='system'?(i===4?' · Intersection':i<2?' · Line 1':' · Line 2'):r.anchor?(i?' · Second point':' · Anchor'):'')+'</option>').join('')+'</select></label><label>x <input data-x aria-label="x coordinate" value="'+esc(points(p,r)[active][0])+'" size="5"></label>'+(!g.number?'<label>y <input data-y aria-label="y coordinate" value="'+esc(points(p,r)[active][1])+'" size="5"></label>':'')+'<button type="button" data-set>Place point</button></div><div data-extra></div><p class="mk-plot-live" aria-live="polite">'+esc(points(p,r).map((v,i)=>String.fromCharCode(65+i)+': '+(g.number?v[0]:'('+v.join(', ')+')')).join(' · '))+'</p><p>Drag a dot or choose a point and tap the grid. Arrow keys move a focused dot; Enter checks your graph.</p>';
 const extra=host.querySelector('[data-extra]');function choice(label,field,values,current,fn){const l=G.document.createElement('label');l.textContent=label+' ';const s=G.document.createElement('select');for(const [v,t]of values){const o=G.document.createElement('option');o.value=v;o.textContent=t;o.selected=String(current)===v;s.appendChild(o)}s.onchange=()=>{fn(s.value);moved();draw()};l.appendChild(s);extra.appendChild(l)}
 if(p.tool==='region'){choice('Boundary','dashed',[['false','Solid'],['true','Dashed']],r.dashed,v=>r.dashed=v==='true');choice('Shade','shade',[['above','Above'],['below','Below']],r.shade,v=>r.shade=v)}
 if(p.tool==='number-line-inequality'){if('between'in p.target){choice('Shading','between',[['true','Between (AND)'],['false','Outside (OR)']],r.between,v=>r.between=v==='true');for(const side of ['left','right'])choice(side+' endpoint','closed',[['false','Open'],['true','Closed']],r[side].closed,v=>r[side].closed=v==='true')}else{choice('Endpoint','closed',[['false','Open'],['true','Closed']],r.closed,v=>r.closed=v==='true');choice('Arrow','direction',[['left','Left'],['right','Right']],r.direction,v=>r.direction=v)}}
 host.querySelector('[data-point]').onchange=e=>{active=+e.target.value;draw()};host.querySelector('[data-set]').onclick=()=>{try{place(active,+F(host.querySelector('[data-x]').value),g.number?0:+F(host.querySelector('[data-y]').value));draw()}catch(e){host.querySelector('.mk-plot-live').textContent='Enter a number or fraction, such as 3/4.'}};
 const svg=host.querySelector('svg');let drag=null;function pos(e){const box=svg.getBoundingClientRect(),xx=(e.clientX-box.left)/box.width*480,yy=(e.clientY-box.top)/box.height*(g.number?140:400);return [g.xmin+(xx-38)/420*(g.xmax-g.xmin),g.ymax-(yy-20)/(g.number?85:342)*(g.ymax-g.ymin)]}
 svg.onpointerdown=e=>{const dot=e.target.closest('[data-handle]');active=dot?+dot.dataset.handle:active;drag=active;dragged=false;svg.setPointerCapture(e.pointerId);e.preventDefault()};svg.onpointermove=e=>{if(drag===null)return;place(drag,...pos(e));dragged=true;const canvas=host.querySelector('.mk-plot-canvas');canvas.querySelector('svg').innerHTML=blank(p,r,active).replace(/^<svg[^>]*>|<\/svg>$/g,'')};svg.onpointerup=e=>{if(drag!==null){place(drag,...pos(e));drag=null;draw();host.querySelector('[data-handle="'+active+'"]').focus()}};svg.onpointercancel=()=>{drag=null;draw()};
 svg.onkeydown=e=>{const dot=e.target.closest('[data-handle]');if(!dot)return;active=+dot.dataset.handle;const pt=points(p,r)[active],delta={ArrowLeft:[-g.snap,0],ArrowRight:[g.snap,0],ArrowUp:[0,g.snap],ArrowDown:[0,-g.snap]}[e.key];if(delta){e.preventDefault();place(active,pt[0]+delta[0],pt[1]+delta[1]);draw();host.querySelector('[data-handle="'+active+'"]').focus()}else if(e.key==='Enter'){e.preventDefault();opts.onSubmit?.()}};
 }
 host.classList.add('mk-plot');draw();return {getResponse:()=>JSON.parse(JSON.stringify(r))};
}

function displayCheck(p,r){
 const no=code=>({ok:false,code}),yes={ok:true,code:null},t=p.target.values;
 if(p.tool==='line-plot'){
  if(!Array.isArray(r?.marks))return no('count');
  let m;try{m=r.marks.map(F)}catch(e){return no('count')}
  const n=p.numberLine,lo=F(n.min),hi=F(n.max),snap=F(n.snap),tick=F(n.tick);
  if(m.length!==t.length||m.some(v=>v.cmp(lo)<0||v.cmp(hi)>0||v.sub(lo).div(snap).d!==1n))return no('count');
  const remaining=t.map(F),extra=[];for(const v of m){const i=remaining.findIndex(w=>v.eq(w));if(i<0)extra.push(v);else remaining.splice(i,1)}
  if(!extra.length)return yes;
  const match=fn=>{const pool=remaining.slice();return extra.every(v=>{const i=pool.findIndex(w=>fn(v,w));if(i<0)return false;pool.splice(i,1);return true})};
  if(lo.eq(0)&&match((v,w)=>w.cmp(1)>=0&&w.d!==1n&&v.eq(new R(w.n%w.d,w.d))))return no('whole-part');
  if(match((v,w)=>v.sub(w).abs().eq(tick)))return no('wrong-tick');
  return no('position');
 }
 const pic=p.tool==='picture-graph',a=pic?r?.symbols:r?.values,axis=p.valueAxis,unit=pic?(p.allowHalf?.5:1):axis.snap,min=pic?0:axis.min,max=pic?p.maxSymbols:axis.max;
 if(!Array.isArray(a)||a.length!==t.length||a.some(v=>typeof v!=='number'||!Number.isFinite(v)||v<min||v>max||F(v).sub(min).div(unit).d!==1n))return no('count');
 const expected=pic?t.map(v=>v/p.key.value):t;
 if(a.every((v,i)=>v===expected[i]))return yes;
 if(pic&&p.key.value>1&&a.every((v,i)=>v===t[i]))return no('key-ignored');
 if(!pic&&axis.step>1&&a.every((v,i)=>v===t[i]/axis.step))return no('scale-count');
 const diff=a.map((v,i)=>i).filter(i=>a[i]!==expected[i]);
 if(pic&&diff.every(i=>!Number.isInteger(expected[i])&&Math.abs(a[i]-expected[i])===.5))return no('half-symbol');
 if(diff.length===2&&a[diff[0]]===expected[diff[1]]&&a[diff[1]]===expected[diff[0]])return no('swapped');
 if(diff.length===1&&Math.abs(a[diff[0]]-expected[diff[0]])===(pic?1:unit))return no('off-by-one');
 return no('position');
}
function validDisplay(p){try{
 if(!p.target?.values?.length||!p.answerKey||!/^question-banks\/assets\/[a-zA-Z0-9_/-]+\.png$/.test(p.answerKey.src)||p.answerKey.src.includes('..')||typeof p.answerKey.alt!=='string')return false;
 if(p.tool==='line-plot'){const n=p.numberLine;if(!n||F(n.max).cmp(n.min)<=0||F(n.snap).cmp(0)<=0||F(n.tick).cmp(0)<=0)return false;return displayCheck(p,{marks:p.target.values}).ok}
 if(!Array.isArray(p.categories)||p.categories.length!==p.target.values.length||!p.categories.every(c=>typeof c==='string'))return false;
 if(p.tool==='picture-graph'){if(!(p.key?.value>0&&p.maxSymbols>0))return false;return displayCheck(p,{symbols:p.target.values.map(v=>v/p.key.value)}).ok}
 const a=p.valueAxis;if(!a||!(a.max>a.min&&a.step>0&&a.snap>0))return false;return displayCheck(p,{values:p.target.values}).ok;
 }catch(e){return false}}
function tickValues(p){const n=p.numberLine,out=[];for(let v=F(n.min),i=0;v.cmp(n.max)<=0&&i<200;v=v.add(n.snap),i++)out.push(v.toString());return out}
function mixed(v){const f=F(v);if(f.d===1n||f.n<f.d)return f.toString();return (f.n/f.d)+' '+(f.n%f.d)+'/'+f.d}
function symbolShape(kind,x,y,half){let shape;
 if(kind==='square')shape='<rect x="'+(x-9)+'" y="'+(y-9)+'" width="18" height="18"/>';
 else if(kind==='heart')shape='<path d="M'+x+' '+(y+10)+' C'+(x-25)+' '+(y-6)+' '+(x-7)+' '+(y-20)+' '+x+' '+(y-8)+' C'+(x+7)+' '+(y-20)+' '+(x+25)+' '+(y-6)+' '+x+' '+(y+10)+'Z"/>';
 else if(kind==='star'){let pts=[];for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,r=i%2?4:11;pts.push((x+Math.cos(a)*r)+','+(y+Math.sin(a)*r))}shape='<polygon points="'+pts.join(' ')+'"/>'}
 else shape='<circle cx="'+x+'" cy="'+y+'" r="9"/>';
 const id='symbolClip'+(++clipCounter);return '<g fill="#2467a5">'+(half?'<defs><clipPath id="'+id+'"><rect x="'+(x-14)+'" y="'+(y-15)+'" width="14" height="30"/></clipPath></defs><g clip-path="url(#'+id+')">'+shape+'</g>':shape)+(kind==='smile'&&!half?'<path d="M'+(x-5)+' '+(y+2)+' Q'+x+' '+(y+8)+' '+(x+5)+' '+(y+2)+'" fill="none" stroke="white"/><circle cx="'+(x-3)+'" cy="'+(y-3)+'" r="1" fill="white"/><circle cx="'+(x+3)+'" cy="'+(y-3)+'" r="1" fill="white"/>':'')+'</g>'}
function displayBlank(p,r){const pic=p.tool==='picture-graph',line=p.tool==='line-plot',w=600,h=line?330:pic?100+p.categories.length*55:390;
 let out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '+w+' '+h+'" role="img" aria-label="'+esc(p.title||p.tool)+'"><rect width="600" height="'+h+'" fill="white"/><text x="300" y="25" text-anchor="middle" font-size="18">'+esc(p.title||'')+'</text>';
 if(pic){out+='<text x="20" y="55" font-size="14">Key: one '+esc(p.key.symbol)+' = '+esc(p.key.value)+'</text>';p.categories.forEach((c,i)=>{const y=90+i*55;out+='<text x="10" y="'+(y+5)+'" font-size="14">'+esc(c)+'</text><path d="M130 '+(y+20)+' H580" stroke="#aab5c4"/>';const count=r?.symbols[i]||0;for(let j=0;j<Math.ceil(count);j++)out+=symbolShape(p.key.symbol,145+j*430/p.maxSymbols,y,j>=Math.floor(count))})}
 else if(line){const ticks=tickValues(p),x=i=>40+i*520/Math.max(1,ticks.length-1);out+='<path d="M40 265 H560" stroke="#344054"/>';ticks.forEach((v,i)=>{out+='<path d="M'+x(i)+' 258 V272" stroke="#344054"/>';if(i%(p.numberLine.labelEvery||1)===0)out+='<text x="'+x(i)+'" y="290" text-anchor="middle" font-size="12">'+esc(p.numberLine.labelFormat==='decimal'?String(+F(v)):p.numberLine.labelFormat==='mixed'?mixed(v):v)+'</text>';const count=r?.marks.filter(m=>F(m).eq(v)).length||0;for(let j=0;j<count;j++)out+=p.mark==='dot'?'<circle cx="'+x(i)+'" cy="'+(245-j*17)+'" r="5" fill="#2467a5"/>':'<text x="'+x(i)+'" y="'+(248-j*17)+'" text-anchor="middle" font-size="18" fill="#2467a5">×</text>'});out+='<text x="300" y="320" text-anchor="middle" font-size="14">'+esc(p.units||'')+'</text>'}
 else{const a=p.valueAxis,y=v=>315-(v-a.min)/(a.max-a.min)*260,bw=480/p.categories.length;for(let v=a.min,i=0;v<=a.max&&i<100;v+=a.step,i++){out+='<path d="M65 '+y(v)+' H560" stroke="#d5dbe3"/>';if(i%(a.labelEvery||1)===0)out+='<text x="57" y="'+(y(v)+4)+'" text-anchor="end" font-size="12">'+v+'</text>'}p.categories.forEach((c,i)=>{const x=75+i*bw,v=r?.values[i]??a.min;out+='<rect data-bar="'+i+'" x="'+x+'" y="'+y(v)+'" width="'+(bw*.7)+'" height="'+(315-y(v))+'" fill="#2467a5"/><text x="'+(x+bw*.35)+'" y="338" text-anchor="middle" font-size="12">'+esc(c)+'</text>'});out+='<text transform="translate(18 185) rotate(-90)" text-anchor="middle" font-size="12">'+esc(a.label||'')+'</text><text x="300" y="375" text-anchor="middle" font-size="14">'+esc(p.categoryLabel||'')+'</text>'}
 return out+'</svg>'}
function displaySource(p){const s=p.source;if(!s)return '';if(s.type==='list')return '<p>Data: '+s.values.map(v=>esc(p.numberLine?.labelFormat==='decimal'?+F(v):v)).join(', ')+'</p>';if(s.type==='objects')return '<p>Objects: '+s.items.map(o=>esc(o.color+' '+o.kind)).join(', ')+'</p>';
 const tally=n=>Array.from({length:Math.floor(n/5)},()=> '||||/').concat(n%5?'|'.repeat(n%5):[]).join(' ');
 return '<table class="mk-data-source"><thead><tr><th>Category</th><th>'+(s.type==='tally'?'Tally':'Count')+'</th></tr></thead><tbody>'+p.categories.map((c,i)=>'<tr><th scope="row">'+esc(c)+'</th><td>'+esc(s.type==='tally'?tally(s.counts[i]):s.counts[i])+'</td></tr>').join('')+'</tbody></table>'}
function displayCreate(host,p,opts){let r=JSON.parse(JSON.stringify(opts.response||initial(p))),active=0;const render=opts.render||displayBlank;const line=p.tool==='line-plot',pic=p.tool==='picture-graph',labels=line?tickValues(p):p.categories;
 function change(i,delta){if(line){if(delta>0&&r.marks.length<100)r.marks.push(labels[i]);else if(delta<0){const j=r.marks.findIndex(v=>F(v).eq(labels[i]));if(j>=0)r.marks.splice(j,1)}}else{const a=pic?r.symbols:r.values,lo=pic?0:p.valueAxis.min,hi=pic?p.maxSymbols:p.valueAxis.max;a[i]=Math.max(lo,Math.min(hi,Number(F(a[i]).add(delta))))}opts.onChange?.(JSON.parse(JSON.stringify(r)));draw(i)}
 function draw(focus){host.innerHTML=displaySource(p)+'<div class="mk-plot-canvas">'+render(p,r)+'</div><p>'+(line?(p.mark==='dot'?'Tap + to add a dot; tap − to remove one.':'Tap + to add an X; tap − to remove one.'):pic?'Add or remove symbols in each category.':'Drag a bar or use the + and − buttons.')+' Arrow keys choose a row; + and − adjust it.'+(pic&&p.allowHalf?' H adds half a symbol.':'')+'</p><div class="mk-display-controls">'+labels.map((label,i)=>{const value=line?r.marks.filter(v=>F(v).eq(label)).length:pic?r.symbols[i]:r.values[i];return '<div class="mk-display-row"><strong>'+esc(line?(p.numberLine.labelFormat==='decimal'?String(+F(label)):mixed(label)):label)+'</strong><button type="button" data-index="'+i+'" data-delta="-1" aria-label="Remove from '+esc(label)+'">−</button><output>'+value+'</output><button type="button" data-index="'+i+'" data-delta="1" aria-label="Add to '+esc(label)+'">+</button>'+(pic&&p.allowHalf?'<button type="button" data-index="'+i+'" data-delta="0.5">+½</button><button type="button" data-index="'+i+'" data-delta="-0.5">−½</button>':'')+'</div>'}).join('')+'</div><p aria-live="polite">'+labels.map((l,i)=>esc(l)+': '+(line?r.marks.filter(v=>F(v).eq(l)).length:pic?r.symbols[i]:r.values[i])).join(' · ')+'</p>';
 host.querySelectorAll('[data-delta]').forEach(b=>b.onclick=()=>{active=+b.dataset.index;change(active,+b.dataset.delta*(pic||line?1:p.valueAxis.snap))});
 host.onkeydown=e=>{if(e.target.dataset.index!==undefined)active=+e.target.dataset.index;if(['ArrowLeft','ArrowUp','ArrowRight','ArrowDown'].includes(e.key)){e.preventDefault();active=(active+(['ArrowLeft','ArrowUp'].includes(e.key)?-1:1)+labels.length)%labels.length;host.querySelector('[data-index="'+active+'"][data-delta="1"]').focus()}else if(['+','-','h','H'].includes(e.key)){e.preventDefault();if((e.key==='h'||e.key==='H')&&!(pic&&p.allowHalf))return;change(active,e.key==='-'?-(pic||line?1:p.valueAxis.snap):e.key.toLowerCase()==='h'?.5:pic||line?1:p.valueAxis.snap)}else if(e.key==='Enter'&&e.target.tagName!=='BUTTON'){e.preventDefault();opts.onSubmit?.()}};
 if(!pic&&!line){const svg=host.querySelector('svg');let dragging=false;const set=e=>{const box=svg.getBoundingClientRect(),x=(e.clientX-box.left)/box.width*600,y=(e.clientY-box.top)/box.height*390,a=p.valueAxis;active=Math.max(0,Math.min(labels.length-1,Math.floor((x-(opts.barLeft??75))/(480/labels.length))));const v=a.min+Math.round(((315-y)/260*(a.max-a.min))/a.snap)*a.snap;r.values[active]=Math.max(a.min,Math.min(a.max,v));opts.onChange?.(JSON.parse(JSON.stringify(r)));svg.innerHTML=render(p,r).replace(/^<svg[^>]*>|<\/svg>$/g,'')};svg.onpointerdown=e=>{dragging=true;svg.setPointerCapture(e.pointerId);set(e);e.preventDefault()};svg.onpointermove=e=>{if(dragging)set(e)};svg.onpointerup=()=>{dragging=false;draw(active)};svg.onpointercancel=()=>{dragging=false;draw(active)}}
 if(focus!==undefined)host.querySelector('[data-index="'+focus+'"][data-delta="1"]').focus();}
 host.classList.add('mk-plot');draw();return {getResponse:()=>JSON.parse(JSON.stringify(r))};
}

const pt = p => [F(p[0]), F(p[1])];
const no = code => ({ok: false, code}), yes = {ok: true};

// integer n with base^n == v (|n| <= 12), else null
function logExact(v, base) {
  for (let n = -12; n <= 12; n++) if (base.pow(n).eq(v)) return n;
  return null;
}

// ---------- exponential-asymptote: y = a * b^(x - h) + k
function onExp(t, P) { const [x, y] = P, e = x.sub(t.h); if (!e.isInt() || e.abs().cmp(30) > 0) return false; return y.eq(F(t.a).mul(F(t.b).pow(Number(e.n))).add(t.k)); }
function checkExponentialAsymptote(p, r) {
  const t = {a: F(p.target.a), b: F(p.target.b), h: F(p.target.h), k: F(p.target.k)};
  if (!F(r.asymptote).eq(t.k)) return no('asymptote');
  const [A, B] = r.points.map(pt); if (A[0].eq(B[0])) return no('same-point');
  const both = tt => onExp(tt, A) && onExp(tt, B);
  if (both(t)) return yes;
  if (both({...t, b: new R(1).div(t.b)})) return no('growth-decay');
  if (both({...t, h: t.h.neg()})) return no('h-sign');
  if (both({...t, a: t.a.neg()})) return no('a-sign');
  return no('points-off-curve');
}

// ---------- log: y = a * log_b(x - h) + k
function onLog(t, P) { const [x, y] = P, u = x.sub(t.h); if (u.sign() <= 0) return false; const n = logExact(u, t.b); return n !== null && y.eq(t.a.mul(n).add(t.k)); }
function checkLog(p, r) {
  const t = {a: F(p.target.a), b: F(p.target.b), h: F(p.target.h), k: F(p.target.k)};
  const v = F(r.asymptote);
  if (!v.eq(t.h)) return no(v.eq(t.h.neg()) && !t.h.eq(0) ? 'h-sign' : 'asymptote');
  const [A, B] = r.points.map(pt); if (A[0].eq(B[0])) return no('same-point');
  const both = tt => onLog(tt, A) && onLog(tt, B);
  if (both(t)) return yes;
  if (onLog(t, [A[1], A[0]]) && onLog(t, [B[1], B[0]])) return no('inverse-swapped');
  if (both({...t, a: t.a.neg()})) return no('a-sign');
  if (both({...t, k: t.k.neg()})) return no('k-sign');
  return no('points-off-curve');
}

// ---------- rational: y = a / (x - h) + k
function onRat(t, P) { const [x, y] = P, u = x.sub(t.h); if (u.sign() === 0) return false; return y.eq(t.a.div(u).add(t.k)); }
function checkRational(p, r) {
  const t = {a: F(p.target.a), h: F(p.target.h), k: F(p.target.k)};
  const v = F(r.vAsymptote), hz = F(r.hAsymptote);
  if (!t.h.eq(t.k) && v.eq(t.k) && hz.eq(t.h)) return no('swapped-asymptotes');
  if (!v.eq(t.h)) return no('v-asymptote');
  if (!hz.eq(t.k)) return no('h-asymptote');
  const [A, B] = r.points.map(pt);
  const both = tt => onRat(tt, A) && onRat(tt, B);
  if (both(t)) return A[0].sub(t.h).sign() === B[0].sub(t.h).sign() ? no('same-branch') : yes;
  if (both({...t, a: t.a.neg()})) return no('branch');
  return no('points-off-curve');
}

// ---------- polynomial: y = a * prod (x - r_i)^m_i
function polyFeatures(t) {
  const a = F(t.a), deg = t.factors.reduce((s, f) => s + f.m, 0);
  let y0 = a; for (const f of t.factors) y0 = y0.mul(F(f.r).neg().pow(f.m));
  const right = a.sign() > 0 ? 'up' : 'down', left = deg % 2 === 0 ? right : (right === 'up' ? 'down' : 'up');
  return {deg, yIntercept: y0, ends: {left, right}, zeros: t.factors.map(f => ({x: F(f.r), behavior: f.m % 2 ? 'cross' : 'touch'}))};
}
function checkPolynomial(p, r) {
  const f = polyFeatures(p.target);
  const key = zs => zs.map(z => z.toString()).sort().join(',');
  const rz = r.zeros.map(z => F(z.x));
  if (key(rz) !== key(f.zeros.map(z => z.x)))
    return no(key(rz) === key(f.zeros.map(z => z.x.neg())) ? 'zero-sign' : 'zeros');
  for (const z of f.zeros) { const got = r.zeros.find(w => F(w.x).eq(z.x)); if (got.behavior !== z.behavior) return no('multiplicity'); }
  if (!F(r.yIntercept).eq(f.yIntercept)) return no('y-intercept');
  if (r.ends.left !== f.ends.left || r.ends.right !== f.ends.right) return no('end-behavior');
  return yes;
}

// ---------- piecewise (two linear pieces split at x = c)
function onLine(piece, P) { return P[1].eq(F(piece.m).mul(P[0]).add(piece.b)); }
function checkPiecewise(p, r) {
  const t = p.target, c = F(t.boundary);
  if (!Array.isArray(r.pieces) || r.pieces.length !== 2) return no('incomplete');
  const got = r.pieces.map(g => ({end: pt(g.endpoint), point: pt(g.point), closed: !!g.closed}));
  if (got.some(g => !g.end[0].eq(c))) return no('boundary');
  for (let i = 0; i < 2; i++) {
    const g = got[i], side = i === 0 ? -1 : 1, mine = t.pieces[i], other = t.pieces[1 - i];
    if (g.point[0].sub(c).sign() !== side) return no('wrong-side');
    if (!(onLine(mine, g.end) && onLine(mine, g.point))) {
      if (onLine(other, g.end) && onLine(other, g.point)) return no('pieces-swapped');
      return no(i === 0 ? 'piece-1' : 'piece-2');
    }
  }
  const sameY = got[0].end[1].eq(got[1].end[1]);
  if (!sameY && got[0].closed && got[1].closed) return no('not-a-function');
  if (sameY) { if (!got[0].closed && !got[1].closed) return no('closed-open'); return yes; }
  if (got[0].closed !== !!t.pieces[0].closed || got[1].closed !== !!t.pieces[1].closed) return no('closed-open');
  return yes;
}

// ---------- sinusoid: y = A sin(2pi/P (x - C)) + D  or  A cos(...); x measured in units of pi
function sinMaxX(t) { // one x where the function has a maximum, in pi units
  const A = F(t.A), P = F(t.P), C = F(t.C);
  if (t.fn === 'sin') return C.add(P.mul(A.sign() > 0 ? new R(1, 4) : new R(3, 4)));
  return C.add(A.sign() > 0 ? 0 : P.div(2));
}
function checkSinusoid(p, r) {
  const t = p.target, A = F(t.A).abs(), P = F(t.P), D = F(t.D);
  const mx = pt(r.max), mn = pt(r.min);
  if (mx[1].cmp(mn[1]) < 0) return no('max-min-swapped');
  if (!mx[1].add(mn[1]).div(2).eq(D)) return no('midline');
  if (!mx[1].sub(mn[1]).div(2).eq(A)) return no('amplitude');
  if (!mx[0].sub(mn[0]).abs().eq(P.div(2))) return no('period');
  if (!mx[0].sub(sinMaxX(t)).div(P).isInt()) return no('phase');
  return yes;
}

function functionCheck(p, r) {
  try {
    if (!r || typeof r !== 'object') return no('incomplete');
    switch (p.tool) {
      case 'exponential-asymptote': return checkExponentialAsymptote(p, r);
      case 'log': return checkLog(p, r);
      case 'rational': return checkRational(p, r);
      case 'polynomial': return checkPolynomial(p, r);
      case 'piecewise': return checkPiecewise(p, r);
      case 'sinusoid': return checkSinusoid(p, r);
    }
    throw Error('unknown tool ' + p.tool);
  } catch (e) { if (/unknown tool/.test(e.message)) throw e; return no('incomplete'); }
}

function functionInitial(p){switch(p.tool){case 'polynomial':return {zeros:[],yIntercept:0,ends:{left:'up',right:'up'}};case 'piecewise':return {pieces:[{endpoint:[0,0],point:[-2,1],closed:false},{endpoint:[0,1],point:[2,2],closed:true}]};case 'sinusoid':return {max:[0,1],min:[1,-1]};case 'rational':return {vAsymptote:0,hAsymptote:0,points:[[-1,-1],[1,1]]};default:return {asymptote:0,points:[[1,1],[2,2]]}}}
function functionHandles(p,r){if(!r)return [];if(p.tool==='polynomial')return r.zeros.map((z,i)=>({key:'zero-'+i,label:'Zero '+(i+1),pt:[+F(z.x),0],closed:z.behavior==='cross'})).concat([{key:'intercept',label:'y-intercept',pt:[0,+F(r.yIntercept)]}]);if(p.tool==='piecewise')return r.pieces.flatMap((g,i)=>[{key:'end-'+i,label:(i?'Right':'Left')+' endpoint',pt:g.endpoint.map(v=>+F(v)),closed:g.closed},{key:'point-'+i,label:(i?'Right':'Left')+' point',pt:g.point.map(v=>+F(v))}]);if(p.tool==='sinusoid')return ['max','min'].map(k=>({key:k,label:k==='max'?'Maximum':'Minimum',pt:r[k].map(v=>+F(v))}));return r.points.map((pt,i)=>({key:'point-'+i,label:'Point '+(i+1),pt:pt.map(v=>+F(v))}));}
function piNumber(v){let s=String(v).trim().replace(/pi/gi,'π').replace(/−/g,'-');if(!s.includes('π'))return F(s);s=s.replace(/π/,'');if(!s||s[0]==='/')s='1'+s;if(s==='-'||s.startsWith('-/'))s='-1'+s.slice(1);return F(s)}
function piLabel(v){const f=F(v);if(f.eq(0))return '0';return (f.n===1n?'':f.n===-1n?'-':f.n.toString())+'π'+(f.d===1n?'':'/'+f.d)}
function functionGrid(p){const g={...p.grid};for(const k of ["xmin","xmax","ymin","ymax"])g[k]=+F(g[k]);return g}
function functionBlank(p,r,active){const g=functionGrid(p),W=420,H=342,L=45,T=22,x=v=>L+(v-g.xmin)/(g.xmax-g.xmin)*W,y=v=>T+(g.ymax-v)/(g.ymax-g.ymin)*H,clip='fnClip'+(++clipCounter),step=Number(F(g.step||1)),xs=Number(F(g.xStep||step));let out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 410" class="mk-plot-svg" role="group" aria-label="Interactive function graph"><defs><clipPath id="'+clip+'"><rect x="45" y="22" width="420" height="342"/></clipPath></defs><rect x="45" y="22" width="420" height="342" fill="white" stroke="#ccd5df"/>';
 for(let v=Math.ceil(g.xmin/xs)*xs,i=0;v<=g.xmax+1e-8&&i<150;v+=xs,i++){const f=F(v.toFixed(8));out+='<path d="M'+x(v)+' 22 V364" stroke="#e0e5ed"/>';if(i%(g.xUnit==='pi'?Math.max(1,2**Math.ceil(Math.log2((g.xmax-g.xmin)/xs/8))):2)===0)out+='<text x="'+x(v)+'" y="386" font-size="11" text-anchor="middle">'+esc(g.xUnit==='pi'?piLabel(f):f.toString())+'</text>'}
 const labelY=(g.ymax-g.ymin)>30?4:2;for(let v=Math.ceil(g.ymin/step)*step,i=0;v<=g.ymax&&i<150;v+=step,i++){out+='<path d="M45 '+y(v)+' H465" stroke="#e0e5ed"/>';if(Math.abs(v/labelY-Math.round(v/labelY))<1e-7)out+='<text x="39" y="'+(y(v)+4)+'" font-size="11" text-anchor="end">'+esc(v)+'</text>'}
 out+='<path d="M45 '+y(0)+' H465 M'+x(0)+' 22 V364" stroke="#344054"/><text x="479" y="'+(y(0)-5)+'">'+'x'+'</text><text x="'+(x(0)+7)+'" y="16">y</text>';
 if(g.xUnit==='pi')out+='<text x="255" y="405" text-anchor="middle" font-size="11">x (radians)</text>';if(!r)return out+'</svg>';
 const dash=(v,vertical,key)=>out+='<path data-asym="'+key+'" d="'+(vertical?'M'+x(v)+' 22 V364':'M45 '+y(v)+' H465')+'" stroke="#a64b0a" stroke-width="3" stroke-dasharray="7 5"/><path data-asym="'+key+'" d="'+(vertical?'M'+x(v)+' 22 V364':'M45 '+y(v)+' H465')+'" stroke="transparent" stroke-width="24"/>',curve=(fn,domain)=>{let d='',last=null;for(let i=0;i<=600;i++){const xx=g.xmin+(g.xmax-g.xmin)*i/600,yy=fn(xx);if(!Number.isFinite(yy)||domain&&!domain(xx)||Math.abs(yy)>1e5){last=null;continue}const valid=last&&Math.abs(yy-last)<(g.ymax-g.ymin)*2;d+=(valid?' L':' M')+x(xx)+' '+y(yy);last=yy}out+='<path clip-path="url(#'+clip+')" d="'+d+'" stroke="#1f5fa8" stroke-width="3" fill="none"/>'};
 try{const k=p.tool;if(k==='exponential-asymptote'||k==='log'){const h=+F(r.asymptote),[a,b]=r.points.map(v=>v.map(v=>+F(v)));dash(h,k==='log','asymptote');if(a[0]!==b[0]){if(k==='exponential-asymptote'){const base=((b[1]-h)/(a[1]-h))**(1/(b[0]-a[0]));if(base>0&&Number.isFinite(base)){const coef=(a[1]-h)/base**a[0];curve(xx=>coef*base**xx+h)}}else if(a[0]>h&&b[0]>h){const coef=(b[1]-a[1])/Math.log((b[0]-h)/(a[0]-h));curve(xx=>a[1]+coef*Math.log((xx-h)/(a[0]-h)),xx=>xx>h)}}}
 else if(k==='rational'){const h=+F(r.vAsymptote),v=+F(r.hAsymptote),[a]=r.points.map(v=>v.map(v=>+F(v))),coef=(a[1]-v)*(a[0]-h);dash(h,true,'vAsymptote');dash(v,false,'hAsymptote');curve(xx=>coef/(xx-h)+v,xx=>xx<h);curve(xx=>coef/(xx-h)+v,xx=>xx>h)}
 else if(k==='piecewise'){r.pieces.forEach((g,i)=>{const a=g.endpoint.map(v=>+F(v)),b=g.point.map(v=>+F(v));if(a[0]!==b[0]){const m=(b[1]-a[1])/(b[0]-a[0]);curve(xx=>a[1]+m*(xx-a[0]),xx=>i?xx>=a[0]:xx<=a[0])}})}
 else if(k==='sinusoid'){const a=r.max.map(v=>+F(v)),b=r.min.map(v=>+F(v)),half=Math.abs(b[0]-a[0]);if(half>0)curve(xx=>(a[1]+b[1])/2+(a[1]-b[1])/2*Math.cos(Math.PI*(xx-a[0])/half))}
 else if(k==='polynomial'){const power=z=>{const f=p.target.factors.find(f=>F(f.r).eq(z.x)&&(f.m%2?'cross':'touch')===z.behavior);return f?f.m:z.behavior==='touch'?2:1},prod=xx=>r.zeros.reduce((v,z)=>v*(xx-Number(F(z.x)))**power(z),1),y0=prod(0),coef=y0?+F(r.yIntercept)/y0:Math.abs(+F(p.target.a))*(r.ends.right==='up'?1:-1);if(r.zeros.length)curve(xx=>coef*prod(xx));for(const side of ['left','right']){const xx=side==='left'?g.xmin+.4:g.xmax-.4,up=r.ends[side]==='up',yy=up?g.ymax-.7:g.ymin+.7;out+='<text x="'+x(xx)+'" y="'+y(yy)+'" text-anchor="middle" font-size="25" fill="#1f5fa8">'+(up?'↑':'↓')+'</text>'}}}catch(e){}
 functionHandles(p,r).forEach(h=>{const [xx,yy]=h.pt;out+='<g data-fhandle="'+h.key+'"><circle cx="'+x(xx)+'" cy="'+y(yy)+'" r="22" fill="transparent"/><circle tabindex="0" role="button" aria-label="'+esc(h.label+' at '+h.pt.join(', '))+'" cx="'+x(xx)+'" cy="'+y(yy)+'" r="'+(active===h.key?8:6)+'" fill="'+(h.closed===false?'white':'#1f5fa8')+'" stroke="#1f5fa8" stroke-width="3"/><text x="'+(h.key.startsWith('zero-')?x(xx):x(xx)+(xx>(g.xmin+g.xmax)/2?-10:10))+'" y="'+(y(yy)+(h.key.startsWith('zero-')?20:yy>g.ymax-2?18:-10))+'" text-anchor="'+(h.key.startsWith('zero-')?'middle':xx>(g.xmin+g.xmax)/2?'end':'start')+'" font-size="11">'+esc(h.key.startsWith('zero-')?String(xx):h.label)+'</text></g>'});return out+'</svg>'}
function functionCreate(host,p,opts){let r=JSON.parse(JSON.stringify(opts.response||functionInitial(p))),active=functionHandles(p,r)[0]?.key||'intercept';const grid=functionGrid(p),xsnap=F(grid.xSnap||grid.snap||1),ysnap=F(grid.snap||1);host.onkeydown=null;
 const changed=()=>opts.onChange?.(JSON.parse(JSON.stringify(r))),clamp=(v,lo,hi,snap)=>{const q=snap.mul(Math.round(+F(v).div(snap)));return q.cmp(lo)<0?F(lo).toString():q.cmp(hi)>0?F(hi).toString():q.toString()};
 function set(key,xx,yy){xx=clamp(xx,grid.xmin,grid.xmax,xsnap);yy=clamp(yy,grid.ymin,grid.ymax,ysnap);if(key==='intercept')r.yIntercept=yy;else if(key.startsWith('zero-'))r.zeros[+key.split('-')[1]].x=xx;else if(key==='max'||key==='min')r[key]=[xx,yy];else if(p.tool==='piecewise'){const [part,index]=key.split('-');r.pieces[+index][part==='end'?'endpoint':'point']=[xx,yy]}else r.points[+key.split('-')[1]]=[xx,yy];active=key;changed()}
 function redraw(focus){const handles=functionHandles(p,r);if(!handles.some(h=>h.key===active))active=handles[0].key;const current=handles.find(h=>h.key===active);host.innerHTML='<div class="mk-plot-canvas">'+functionBlank(p,r,active)+'</div><div class="mk-plot-controls"><label>Point <select data-handle>'+handles.map(h=>'<option value="'+h.key+'" '+(h.key===active?'selected':'')+'>'+esc(h.label)+'</option>').join('')+'</select></label><label>x '+(grid.xUnit==='pi'?'(π units) ':'')+'<input data-x aria-label="x coordinate" value="'+esc(current.pt[0])+'"></label><label>y <input data-y aria-label="y coordinate" value="'+esc(current.pt[1])+'"></label><button data-place type="button">Place point</button></div><div class="mk-plot-controls" data-extra></div><p data-live aria-live="polite">'+esc(handles.map(h=>h.label+': ('+h.pt.join(', ')+')').join(' · '))+'</p><p>'+(p.tool==='polynomial'?'Tap the x-axis to add zeros. Tap a zero to switch crossing/touching; set the y-intercept and end arrows.':p.tool==='sinusoid'?'Place a maximum and the next minimum.':p.tool==='piecewise'?'Place each endpoint and one point on its side. Choose whether each endpoint is open or closed.':'Place both points and the dashed asymptote'+(p.tool==='rational'?'s, using one point on each branch.':'.'))+' Drag points or use the coordinate controls. Arrow keys move a focused point; Enter checks your graph.'+(grid.xUnit==='pi'?' Enter x in π units, for example 3/4 or 3π/4.':'')+'</p>';
 const extra=host.querySelector('[data-extra]');function number(label,key){const l=G.document.createElement('label');l.textContent=label+' ';const input=G.document.createElement('input');input.value=r[key];input.setAttribute('aria-label',label);input.onchange=()=>{try{const vertical=key==='vAsymptote'||p.tool==='log';r[key]=clamp(F(input.value),vertical?grid.xmin:grid.ymin,vertical?grid.xmax:grid.ymax,vertical?xsnap:ysnap);changed();redraw()}catch(e){host.querySelector('[data-live]').textContent='Enter a number or fraction.'}};l.appendChild(input);extra.appendChild(l)}function choice(label,values,value,fn){const l=G.document.createElement('label');l.textContent=label+' ';const s=G.document.createElement('select');s.setAttribute('aria-label',label);values.forEach(v=>{const o=G.document.createElement('option');o.value=v;o.textContent=v;o.selected=v===value;s.appendChild(o)});s.onchange=()=>{fn(s.value);changed();redraw()};l.appendChild(s);extra.appendChild(l)}
 if('asymptote'in r)number(p.tool==='log'?'Vertical asymptote x':'Horizontal asymptote y','asymptote');if('vAsymptote'in r){number('Vertical asymptote x','vAsymptote');number('Horizontal asymptote y','hAsymptote')}
 if(p.tool==='polynomial'){const btn=G.document.createElement('button');btn.type='button';btn.textContent='Add zero at entered x';btn.onclick=()=>{try{const x=clamp(piNumber(host.querySelector('[data-x]').value),grid.xmin,grid.xmax,xsnap);if(!r.zeros.some(z=>F(z.x).eq(x)))r.zeros.push({x,behavior:'cross'});changed();active='zero-'+(r.zeros.length-1);redraw()}catch(e){host.querySelector('[data-live]').textContent='Enter a valid x coordinate.'}};extra.appendChild(btn);for(const side of ['left','right'])choice(side+' end',['up','down'],r.ends[side],v=>r.ends[side]=v);r.zeros.forEach((z,i)=>{choice('Zero '+(i+1)+' behavior',['cross','touch'],z.behavior,v=>z.behavior=v);const b=G.document.createElement('button');b.type='button';b.textContent='Remove zero '+(i+1);b.onclick=()=>{r.zeros.splice(i,1);changed();redraw()};extra.appendChild(b)})}
 if(p.tool==='piecewise')r.pieces.forEach((g,i)=>choice((i?'Right':'Left')+' endpoint',['open','closed'],g.closed?'closed':'open',v=>g.closed=v==='closed'));
 host.querySelector('[data-handle]').onchange=e=>{active=e.target.value;redraw()};host.querySelector('[data-place]').onclick=()=>{try{set(active,grid.xUnit==='pi'?piNumber(host.querySelector('[data-x]').value):F(host.querySelector('[data-x]').value),F(host.querySelector('[data-y]').value));redraw()}catch(e){host.querySelector('[data-live]').textContent='Enter a number or fraction, such as 3/4.'}};
 const svg=host.querySelector('svg'),pos=e=>{const b=svg.getBoundingClientRect();return [grid.xmin+((e.clientX-b.left)/b.width*500-45)/420*(grid.xmax-grid.xmin),grid.ymax-((e.clientY-b.top)/b.height*410-22)/342*(grid.ymax-grid.ymin)]};let drag=null,moved=false,origin=null;
 const update=e=>{const [xx,yy]=pos(e);if(drag.startsWith('asym:')){const key=drag.slice(5),vertical=key==='vAsymptote'||p.tool==='log';r[key]=clamp(vertical?xx:yy,vertical?grid.xmin:grid.ymin,vertical?grid.xmax:grid.ymax,vertical?xsnap:ysnap);changed()}else set(drag,xx,yy);svg.innerHTML=functionBlank(p,r,active).replace(/^<svg[^>]*>|<\/svg>$/g,'')};
 svg.onpointerdown=e=>{const dot=e.target.closest('[data-fhandle]'),as=e.target.closest('[data-asym]');drag=as?'asym:'+as.dataset.asym:dot?dot.dataset.fhandle:null;origin=[e.clientX,e.clientY];moved=false;svg.setPointerCapture(e.pointerId);e.preventDefault()};svg.onpointermove=e=>{if(!drag)return;if(Math.hypot(e.clientX-origin[0],e.clientY-origin[1])>3)moved=true;if(moved)update(e)};
 svg.onpointerup=e=>{if(drag){if(moved)update(e);else if(p.tool==='polynomial'&&(drag.startsWith('zero-')||drag==='intercept'&&r.zeros.some(z=>F(z.x).eq(0)))){const z=drag.startsWith('zero-')?r.zeros[+drag.split('-')[1]]:r.zeros.find(z=>F(z.x).eq(0));z.behavior=z.behavior==='cross'?'touch':'cross';changed()}else active=drag.startsWith('asym:')?active:drag}else if(p.tool==='polynomial'){const [xx,yy]=pos(e);if(Math.abs(yy)<(grid.ymax-grid.ymin)/12){const x=clamp(xx,grid.xmin,grid.xmax,xsnap);if(!r.zeros.some(z=>F(z.x).eq(x)))r.zeros.push({x,behavior:'cross'});active='zero-'+(r.zeros.length-1);changed()}}else{const [xx,yy]=pos(e);set(active,xx,yy)}drag=null;redraw(true)};svg.onpointercancel=()=>{drag=null;redraw()};svg.onkeydown=e=>{const dot=e.target.closest('[data-fhandle]');if(!dot)return;active=dot.dataset.fhandle;const h=functionHandles(p,r).find(h=>h.key===active),d={ArrowLeft:[-xsnap,0],ArrowRight:[+xsnap,0],ArrowUp:[0,+ysnap],ArrowDown:[0,-ysnap]}[e.key];if(d){e.preventDefault();set(active,h.pt[0]+d[0],h.pt[1]+d[1]);redraw(true)}else if(e.key==='Enter'){e.preventDefault();opts.onSubmit?.()}};
 if(focus)host.querySelector('[data-fhandle="'+active+'"] circle[tabindex]')?.focus();}
 host.classList.add('mk-plot');redraw();return {getResponse:()=>JSON.parse(JSON.stringify(r))};
}

function median(a) { const s = [...a].sort((x, y) => x - y), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; }
function quartiles(data, method = 'exclusive') {
  const s = [...data].sort((x, y) => x - y), n = s.length, h = Math.floor(n / 2);
  const lower = s.slice(0, method === 'inclusive' && n % 2 ? h + 1 : h), upper = s.slice(n % 2 && method !== 'inclusive' ? h + 1 : h);
  return {q1: median(lower), med: median(s), q3: median(upper)};
}
function fiveNumber(data, outlierRule) {
  const s = [...data].sort((x, y) => x - y), {q1, med, q3} = quartiles(s), iqr = q3 - q1;
  const lo = q1 - 1.5 * iqr, hi = q3 + 1.5 * iqr;
  const outliers = outlierRule ? s.filter(v => v < lo || v > hi) : [];
  const inside = s.filter(v => !outliers.includes(v));
  return {min: inside[0], q1, median: med, q3, max: inside[inside.length - 1], outliers, fences: [lo, hi]};
}
const isNum = v => typeof v === 'number' && Number.isFinite(v);
const sameBag = (a, b) => a.length === b.length && [...a].sort((x, y) => x - y).every((v, i) => v === [...b].sort((x, y) => x - y)[i]);

function checkBoxPlot(p, r) {
  if (!r) return {ok: false, code: 'incomplete'};
  const R = {...r, min: +r.min, q1: +r.q1, median: +r.median, q3: +r.q3, max: +r.max, outliers: (r.outliers || []).map(Number)};
  if (![R.min, R.q1, R.median, R.q3, R.max, ...R.outliers].every(isNum) || !(R.min <= R.q1 && R.q1 <= R.median && R.median <= R.q3 && R.q3 <= R.max)) return {ok: false, code: 'incomplete'};
  const d = p.target.data, t = fiveNumber(d, p.outlierRule);
  if (R.median !== t.median) { const mean = d.reduce((a, b) => a + b, 0) / d.length; return {ok: false, code: R.median === mean ? 'mean-not-median' : 'median'}; }
  if (R.q1 !== t.q1 || R.q3 !== t.q3) { const inc = quartiles(d, 'inclusive'); return {ok: false, code: R.q1 === inc.q1 && R.q3 === inc.q3 ? 'quartile-method' : 'quartile'}; }
  if (!sameBag(R.outliers, t.outliers)) return {ok: false, code: 'outlier'};
  if (R.min !== t.min || R.max !== t.max) return {ok: false, code: 'whisker'};
  return {ok: true};
}

// bins are left-closed [start + i*width, start + (i+1)*width)
function binCounts(data, start, width, nBins, rightClosed = false) {
  const c = Array(nBins).fill(0);
  for (const v of data) {
    let i = rightClosed ? Math.ceil((v - start) / width) - 1 : Math.floor((v - start) / width);
    if (rightClosed && v === start) i = 0;
    if (i >= 0 && i < nBins) c[i]++;
  }
  return c;
}
function checkHistogram(p, r) {
  const b = p.bins, t = binCounts(p.target.data, b.start, b.width, b.count), c = r && r.counts;
  if (!Array.isArray(c) || c.length !== b.count || c.some(v => !Number.isInteger(v) || v < 0 || v > p.valueAxis.max)) return {ok: false, code: 'count'};
  if (c.every((v, i) => v === t[i])) return {ok: true};
  const rc = binCounts(p.target.data, b.start, b.width, b.count, true);
  if (c.every((v, i) => v === rc[i])) return {ok: false, code: 'boundary'};
  if (c.reduce((a, v) => a + v, 0) !== p.target.data.length) return {ok: false, code: 'total'};
  return {ok: false, code: 'position'};
}

function statsCheck(p, r) {
  if (p.tool === 'box-plot') return checkBoxPlot(p, r);
  if (p.tool === 'histogram') return checkHistogram(p, r);
  throw Error('unknown tool ' + p.tool);
}

function statsInitial(p){if(p.tool==='histogram')return {counts:Array(p.bins.count).fill(0)};const a=p.axis,at=f=>+F(a.min).add(F(a.snap).mul(Math.round(+F(a.max).sub(a.min).mul(f).div(a.snap))));return {min:+F(a.min),q1:at('1/4'),median:at('1/2'),q3:at('3/4'),max:+F(a.max),outliers:[]}}
function statsBlank(p,r){if(p.tool==='histogram'){const b=p.bins,a=p.valueAxis,x=v=>65+(v-b.start)/(b.width*b.count)*480,y=v=>315-(v-a.min)/(a.max-a.min)*260;let out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 390" role="img" aria-label="Histogram"><rect width="600" height="390" fill="white"/><text x="300" y="25" text-anchor="middle" font-size="18">'+esc(p.title||'Histogram')+'</text>';for(let v=a.min,i=0;v<=a.max&&i<100;v+=a.step,i++)out+='<path d="M65 '+y(v)+' H545" stroke="#d5dbe3"/><text x="57" y="'+(y(v)+4)+'" text-anchor="end" font-size="12">'+v+'</text>';for(let i=0;i<b.count;i++){const v=r?.counts[i]??0;out+='<rect x="'+x(b.start+i*b.width)+'" y="'+y(v)+'" width="'+(480/b.count)+'" height="'+Math.max(0,315-y(v))+'" fill="#2467a5" stroke="#174c7e"/>'}for(let i=0;i<=b.count;i++)out+='<text x="'+x(b.start+i*b.width)+'" y="338" text-anchor="middle" font-size="12">'+esc(b.start+i*b.width)+'</text>';return out+'<text x="300" y="366" text-anchor="middle" font-size="13">'+esc(p.categoryLabel||'')+' · bins include the left edge, exclude the right</text><text transform="translate(18 180) rotate(-90)" text-anchor="middle" font-size="12">'+esc(a.label||'Frequency')+'</text></svg>'}
 const a=p.axis,x=v=>45+(+F(v)-+F(a.min))/(+F(a.max)-+F(a.min))*510;let out='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 245" role="group" aria-label="Interactive box plot"><rect width="600" height="245" fill="white"/><text x="300" y="25" text-anchor="middle" font-size="18">'+esc(p.title||'Box plot')+'</text><path d="M45 175 H555" stroke="#344054"/>';
 for(let v=F(a.min),i=0;v.cmp(a.max)<=0&&i<150;v=v.add(a.step),i++){out+='<path d="M'+x(v)+' 170 V180" stroke="#344054"/>';if(i%(a.labelEvery||1)===0)out+='<text x="'+x(v)+'" y="202" text-anchor="middle" font-size="12">'+esc(+v)+'</text>'}
 if(r){out+='<path d="M'+x(r.min)+' 110 H'+x(r.max)+' M'+x(r.min)+' 90 V130 M'+x(r.max)+' 90 V130" stroke="#2467a5" stroke-width="3"/><rect x="'+Math.min(x(r.q1),x(r.q3))+'" y="75" width="'+Math.abs(x(r.q3)-x(r.q1))+'" height="70" fill="#dcecfb" stroke="#2467a5" stroke-width="3"/><path d="M'+x(r.median)+' 75 V145" stroke="#174c7e" stroke-width="4"/>';
 for(const key of ['min','q1','median','q3','max'])out+='<g data-box-handle="'+key+'"><circle cx="'+x(r[key])+'" cy="110" r="22" fill="transparent"/><circle tabindex="0" role="button" aria-label="'+key+' at '+esc(r[key])+'" cx="'+x(r[key])+'" cy="110" r="6" fill="#2467a5"/></g>';
 (r.outliers||[]).forEach((v,i)=>{out+='<circle data-outlier="'+i+'" tabindex="0" role="button" aria-label="Remove outlier '+esc(v)+'" cx="'+x(v)+'" cy="110" r="7" fill="white" stroke="#a64b0a" stroke-width="3"/>'})}
 return out+'<text x="300" y="231" text-anchor="middle" font-size="13">'+esc(a.label||'')+'</text></svg>'}
function statsCreate(host,p,opts){if(p.tool==='histogram'){const b=p.bins,proxy={...p,tool:'bar-graph',categories:Array.from({length:b.count},(_,i)=>'['+(b.start+i*b.width)+', '+(b.start+(i+1)*b.width)+')'),target:{values:binCounts(p.target.data,b.start,b.width,b.count)}},widget=displayCreate(host,proxy,{...opts,barLeft:65,response:opts.response?{values:opts.response.counts}:undefined,render:(_p,r)=>statsBlank(p,{counts:r.values}),onChange:r=>opts.onChange?.({counts:r.values})});return {getResponse:()=>({counts:widget.getResponse().values})}}
 let r=JSON.parse(JSON.stringify(opts.response||statsInitial(p))),active='median';const a=p.axis,snap=F(a.snap),keys=['min','q1','median','q3','max'],copy=()=>JSON.parse(JSON.stringify(r)),changed=()=>opts.onChange?.(copy()),snapped=v=>{const q=snap.mul(Math.round(+F(v).sub(a.min).div(snap))).add(a.min);return q.cmp(a.min)<0?+F(a.min):q.cmp(a.max)>0?+F(a.max):+q};
 function draw(focus){host.innerHTML=displaySource(p)+'<div class="mk-plot-canvas">'+statsBlank(p,r)+'</div><div class="mk-plot-controls"><label>Handle <select data-box-select>'+keys.map(k=>'<option '+(k===active?'selected':'')+'>'+k+'</option>').join('')+'</select></label><label>Value <input data-box-value aria-label="Handle value" value="'+r[active]+'"></label><button data-box-place type="button">Place handle</button></div><div class="mk-plot-controls" data-outliers></div><p data-box-live aria-live="polite">'+keys.map(k=>k+': '+r[k]).join(' · ')+' · Outliers: '+esc(r.outliers.join(', ')||'none')+'</p><p>Drag a handle or select it and enter its value. Arrow keys move a focused handle.'+(p.outlierRule?' Tap the axis to add an outlier, or use Add outlier. Tap an outlier to remove it.':'')+'</p>';
 host.querySelector('[data-box-select]').onchange=e=>{active=e.target.value;draw()};host.querySelector('[data-box-place]').onclick=()=>{try{r[active]=snapped(host.querySelector('[data-box-value]').value);changed();draw()}catch(e){host.querySelector('[data-box-live]').textContent='Enter a number or fraction.'}};
 if(p.outlierRule){const div=host.querySelector('[data-outliers]');div.innerHTML='<label>Outlier <input data-new-outlier aria-label="New outlier value" value="'+a.min+'"></label><button type="button" data-add-outlier>Add outlier</button>'+r.outliers.map((v,i)=>'<button type="button" data-remove-outlier="'+i+'">Remove outlier '+esc(v)+'</button>').join('');div.querySelector('[data-add-outlier]').onclick=()=>{try{r.outliers.push(snapped(div.querySelector('[data-new-outlier]').value));changed();draw()}catch(e){host.querySelector('[data-box-live]').textContent='Enter a valid outlier.'}};div.querySelectorAll('[data-remove-outlier]').forEach(b=>b.onclick=()=>{r.outliers.splice(+b.dataset.removeOutlier,1);changed();draw()})}
 const svg=host.querySelector('svg'),value=e=>{const box=svg.getBoundingClientRect(),xx=(e.clientX-box.left)/box.width*600;return snapped(+F(a.min)+(xx-45)/510*(+F(a.max)-+F(a.min)))};let drag=null;
 svg.onpointerdown=e=>{const handle=e.target.closest('[data-box-handle]');drag=handle?.dataset.boxHandle||null;if(drag){active=drag;svg.setPointerCapture(e.pointerId);e.preventDefault()}};svg.onpointermove=e=>{if(!drag)return;r[drag]=value(e);changed();svg.innerHTML=statsBlank(p,r).replace(/^<svg[^>]*>|<\/svg>$/g,'')};svg.onpointerup=e=>{if(drag){r[drag]=value(e);drag=null;changed();draw(true)}else if(p.outlierRule){const dot=e.target.closest('[data-outlier]');if(dot)r.outliers.splice(+dot.dataset.outlier,1);else{const v=value(e),i=r.outliers.indexOf(v);if(i>=0)r.outliers.splice(i,1);else r.outliers.push(v)}changed();draw()}};svg.onpointercancel=()=>{drag=null;draw()};svg.onkeydown=e=>{const h=e.target.closest('[data-box-handle]');if(h){active=h.dataset.boxHandle;if(['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();r[active]=snapped(F(r[active]).add(e.key==='ArrowLeft'?snap.neg():snap));changed();draw(true)}else if(e.key==='Enter'){e.preventDefault();opts.onSubmit?.()}}else if(e.target.dataset.outlier!==undefined&&['Enter','Delete','Backspace'].includes(e.key)){e.preventDefault();r.outliers.splice(+e.target.dataset.outlier,1);changed();draw()}};
 if(focus)host.querySelector('[data-box-handle="'+active+'"] circle[tabindex]')?.focus();}
 host.onkeydown=null;host.classList.add('mk-plot');draw();return {getResponse:copy};
}

G.MK_PLOT={check,valid,blank,create,initial,number:v=>+F(v),tools};
})(typeof window!=='undefined'?window:globalThis);
