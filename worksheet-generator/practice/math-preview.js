/* Student answer preview only. It never grades, parses correctness, or exposes keys. */
(function(G){
'use strict';
var API=G.MKMATHPREVIEW={};
function escape(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function math(s){
 s=String(s==null?'':s).trim().replace(/[−–]/g,'-');
 if(!s)return '';
 // Interpret common student keyboard notation conservatively.
 s=s.replace(/<=|≤/g,'\\le ').replace(/>=|≥/g,'\\ge ').replace(/!=|≠/g,'\\ne ');
 s=s.replace(/\b(sqrt|√)\s*\(\s*([^()]*)\s*\)/gi,'\\sqrt{$2}');
 s=s.replace(/√\s*(\d+(?:\.\d+)?|[a-zA-Z])/g,'\\sqrt{$1}');
 // Fractions should appear stacked, without changing the submitted answer.
 s=s.replace(/(-?\d+(?:\.\d+)?|[a-zA-Z])\s*\/\s*(-?\d+(?:\.\d+)?|[a-zA-Z])/g,'\\frac{$1}{$2}');
 s=s.replace(/\^\s*\(([^()]*)\)/g,'^{$1}').replace(/\^\s*([+-]?\d+(?:\.\d+)?|[a-zA-Z])/g,'^{$1}');
 s=s.replace(/(^|[\s,;])or(?=$|[\s,;])/gi,'$1\\text{ or }').replace(/(^|[\s,;])and(?=$|[\s,;])/gi,'$1\\text{ and }');
 s=s.replace(/\*/g,'\\cdot ');
 return s;
}
API.toTex=math;
API.preview=function(input){
 var raw=String(input==null?'':input).trim();
 if(!raw)return {html:'<span class="pt-preview-empty">Your math appears here as you type.</span>',empty:true};
 var tex=math(raw);
 if(G.katex&&typeof G.katex.renderToString==='function'){
  try{return {html:G.katex.renderToString(tex,{throwOnError:true,output:'html',trust:false,maxExpand:100}),empty:false};}
  catch(e){}
 }
 return {html:'<span class="pt-preview-plain">'+escape(raw)+'</span>',empty:false};
};
API.update=function(input,output){
 if(!output)return;
 var result=API.preview(input.value);
 output.innerHTML=result.html;
 output.classList.toggle('pt-preview-empty-state',result.empty);
};
})(window);