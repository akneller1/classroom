/* Three-point exponential graphs: x=-1,0,1 are graded against the verified function. */
(function(G){
'use strict';
var API=G.MKEXPGRAPH={};
function target(q){var p=q.problem,chk=p&&p.parts&&p.parts[0]&&p.parts[0].check;return p&&p.parts&&p.parts.length===1&&chk&&chk.type==='exp-graph-points'?chk:null;}
API.target=target;
function get(q){if(!(q.response||'').startsWith('expplot:'))return {};try{var v=JSON.parse(q.response.slice(8));return v&&typeof v==='object'&&!Array.isArray(v)?v:{};}catch(e){return {};}}
function graphic(q){
 var answers=get(q),h='<svg class="pt-line-svg" viewBox="0 0 340 340" role="img" aria-label="Plot three exponential points">';
 for(var v=-10;v<=10;v++){var p=170+v*15;h+='<path d="M'+p+' 20V320 M20 '+p+'H320" stroke="#dce6ee"/>';}
 h+='<path d="M170 20V320 M20 170H320" stroke="#617c92" stroke-width="2"/>';
 var pts=[-1,0,1].filter(x=>Number.isFinite(+answers[x])).map(x=>[x,+answers[x]]);
 pts.forEach(function(p){h+='<circle cx="'+(170+p[0]*15)+'" cy="'+(170-p[1]*15)+'" r="6" fill="#286ab6" stroke="white" stroke-width="2"/>';});
 if(pts.length===3){
   var y0=+answers[0],y1=+answers[1],ym=+answers[-1];
   var chk=target(q),k=chk?Number(chk.k||0):0;
   var b=y0!==k?(y1-k)/(y0-k):0;
   if(b>0&&Math.abs(ym-(y0-k)/b-k)<1e-6){
      var path='';
      for(var x=-10;x<=10;x+=.06){var y=(y0-k)*Math.pow(b,x)+k;if(y<-10||y>10||!Number.isFinite(y))continue;path+=(path?'L':'M')+(170+15*x)+' '+(170-15*y)+' ';}
      h+='<path d="'+path+'" stroke="#286ab6" fill="none" stroke-width="2.5"/>';
   }
 }
 return h+'</svg>';
}
API.render=function(q,i){
 var a=get(q);return '<div class="pt-exp-editor" data-expgraph="'+i+'"><strong>Graph using three points</strong><p class="pt-muted">Plot the y-values at x = −1, 0, and 1. Tap the grid at x = −1, 0, and 1 to plot points, or enter each y-value below.</p>'+graphic(q)+
 '<div class="pt-interval-row">'+[-1,0,1].map(x=>'<label>x = '+x+'<input inputmode="decimal" type="text" data-exp-x="'+x+'" value="'+(a[x]===undefined?'':a[x])+'" placeholder="y-value"></label>').join('')+'</div></div>';
};
API.grade=function(q){
 var chk=target(q),a=get(q);if(!chk)return {status:'incorrect'};
 for(var x of [-1,0,1]){var want=chk.a*Math.pow(chk.n/chk.d,x)+Number(chk.k||0);if(a[x]===undefined||!Number.isFinite(+a[x])||Math.abs(+a[x]-want)>1e-7)return {status:'incorrect'};}
 return {status:'correct'};
};
API.bind=function(root,state,save){root.querySelectorAll('[data-expgraph]').forEach(function(box){var i=+box.dataset.expgraph,q=state.questions[i];
 box.onclick=function(e){var svg=e.target.closest('svg');if(!svg||!box.contains(svg))return;
 var rect=svg.getBoundingClientRect(),x=Math.max(-1,Math.min(1,Math.round(((e.clientX-rect.left)/rect.width*340-170)/15))),y=Math.round((170-(e.clientY-rect.top)/rect.height*340)/15);
 var a=get(q);a[x]=Math.max(-10,Math.min(10,y));q.response='expplot:'+JSON.stringify(a);save();svg.outerHTML=graphic(q);box.querySelector('[data-exp-x="'+x+'"]').value=a[x];
 };
 box.querySelectorAll('[data-exp-x]').forEach(function(el){
  el.oninput=function(){var a=get(q),raw=el.value.trim().replace(/−/g,'-');if(raw===''||raw==='-'){delete a[el.dataset.expX];}else if(/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(raw)){a[el.dataset.expX]=+raw;}else return;
    q.response='expplot:'+JSON.stringify(a);save();box.querySelector('svg').outerHTML=graphic(q);};
 });});};
})(window);