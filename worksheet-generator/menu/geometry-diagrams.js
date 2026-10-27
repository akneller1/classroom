/* Shared Geometry SVG renderer. Data-only specifications; no DOM dependencies.
   Figures are explicitly not to scale when their labels represent algebraic unknowns. */
(function(G){
'use strict';
var NS=G.MKMENU=(G.MKMENU||{}), D=NS.geoDiagram={};
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function positive(n){return Number.isFinite(n)&&n>0}
function svg(inner,description){return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 155" width="4.1in" style="max-width:100%;height:auto" role="img" aria-label="'+esc(description)+'"><rect width="430" height="155" fill="white"/>'+inner+'</svg>'}
function tx(x,y,s,anchor){return '<text x="'+x+'" y="'+y+'" text-anchor="'+(anchor||'middle')+'" font-family="Arial,sans-serif" font-size="15" fill="#111">'+esc(s)+'</text>'}
D.render=function(spec){
 if(!spec||!['geo-segment','geo-angle','geo-angle-pair','geo-triangle-pair'].includes(spec.kind))return '';
 var h='',a=spec.labels||[],m=spec.measures||[];
 if(spec.kind==='geo-triangle-pair'){
   if(!['sss','sas','asa','aas','hl','ssa','aaa'].includes(spec.criterion))return '';
   var right=spec.criterion==='hl';
   var A=[65,30],B=right?[65,122]:[48,122],C=[187,122];
   var D=[253,30],E=right?[253,122]:[236,122],F=[375,122];
   function line(p,q){return '<path d="M'+p[0]+' '+p[1]+' L'+q[0]+' '+q[1]+'" stroke="#111" stroke-width="2.5" fill="none"/>';}
   function mark(p,q,n){var mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2,dx=q[0]-p[0],dy=q[1]-p[1],len=Math.hypot(dx,dy),nx=-dy/len,ny=dx/len,out='';
     for(var j=0;j<n;j++){var t=j-(n-1)/2,xx=mx+t*6*dx/len,yy=my+t*6*dy/len;out+='<path d="M'+(xx-6*nx)+' '+(yy-6*ny)+' L'+(xx+6*nx)+' '+(yy+6*ny)+'" stroke="#111" stroke-width="1.7"/>';}return out;}
   h=line(A,B)+line(B,C)+line(C,A)+line(D,E)+line(E,F)+line(F,D);
   var k=spec.criterion;
   if(k==='sss'||k==='sas'||k==='hl')h+=mark(A,B,1)+mark(D,E,1);
   if(k==='sss'||k==='sas'||k==='hl')h+=mark(A,C,2)+mark(D,F,2);
   if(k==='sss')h+=mark(B,C,3)+mark(E,F,3);
   if(k==='asa'||k==='aas')h+=mark(A,C,1)+mark(D,F,1);
   if(k==='ssa')h+=mark(A,B,1)+mark(D,E,1)+mark(B,C,2)+mark(E,F,2);
   if(k==='asa')h+=mark(A,B,2)+mark(D,E,2);
   function arc(p,q,v,rank){var ux=(p[0]-v[0])/Math.hypot(p[0]-v[0],p[1]-v[1]),uy=(p[1]-v[1])/Math.hypot(p[0]-v[0],p[1]-v[1]);var vx=(q[0]-v[0])/Math.hypot(q[0]-v[0],q[1]-v[1]),vy=(q[1]-v[1])/Math.hypot(q[0]-v[0],q[1]-v[1]);var rr=17+rank*5;return '<path d="M'+(v[0]+rr*ux)+' '+(v[1]+rr*uy)+' A'+rr+' '+rr+' 0 0 1 '+(v[0]+rr*vx)+' '+(v[1]+rr*vy)+'" fill="none" stroke="#111" stroke-width="1.5"/>';}
   if(['sas','asa','aas','ssa','aaa'].includes(k))h+=arc(B,C,A,0)+arc(E,F,D,0);
   if(['asa','aas','aaa'].includes(k))h+=arc(A,C,B,1)+arc(D,F,E,1);
   if(k==='aaa')h+=arc(A,B,C,2)+arc(D,E,F,2);
   if(right)h+='<path d="M65 110 H77 V122 M253 110 H265 V122" stroke="#111" fill="none" stroke-width="1.6"/>';
   h+=tx(65,20,'A')+tx(B[0]-12,139,'B')+tx(193,139,'C')+tx(253,20,'D')+tx(E[0]-12,139,'E')+tx(381,139,'F');
   return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,'Two triangles ABC and DEF; the given congruence relationships are stated in the question')+'<div style="font-size:10px;color:#555">Schematic, not to scale. Matching marks indicate equal corresponding sides or angles.</div></div>';
 }
 if(spec.kind==='geo-segment'){
   if(a.length!==3||m.length!==3||!m.every(x=>typeof x==='string'&&x.length<50))return '';
   h='<path d="M54 76 H376" fill="none" stroke="#111" stroke-width="2.5"/>'+
     '<circle cx="54" cy="76" r="4" fill="#111"/><circle cx="198" cy="76" r="4" fill="#111"/><circle cx="376" cy="76" r="4" fill="#111"/>'+
     tx(54,105,a[0])+tx(198,105,a[1])+tx(376,105,a[2])+
     tx(125,59,m[0])+tx(287,59,m[1])+tx(215,139,m[2]);
 }else if(spec.kind==='geo-angle'){
   if(a.length!==3||m.length!==3)return '';
   h='<path d="M68 125 L215 125 L356 37 M215 125 L239 29" fill="none" stroke="#111" stroke-width="2.5"/>'+
     '<path d="M184 125 A31 31 0 0 1 224 95" fill="none" stroke="#111" stroke-width="1.6"/>'+
     '<path d="M244 107 A31 31 0 0 1 237 94" fill="none" stroke="#111" stroke-width="1.6"/>'+
     tx(50,130,a[0])+tx(206,148,a[1])+tx(375,32,a[2])+
     tx(165,88,m[0])+tx(275,88,m[1])+tx(362,111,m[2]);
 }else{
   if(m.length!==3)return '';
   var right=spec.relationship==='complement';
   h='<path d="M90 126 H355 M90 126 V25 M90 126 L'+(right?'278 36':'165 29')+'" fill="none" stroke="#111" stroke-width="2.5"/>'+
    tx(245,108,m[0])+tx(123,77,m[1])+tx(347,45,m[2]);
   if(right)h+='<path d="M90 111 H105 V126" fill="none" stroke="#111" stroke-width="1.5"/>';
 }
 return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,spec.description||'Geometry schematic; not drawn to scale')+'<div style="font-size:10px;color:#555">Schematic, not to scale</div></div>';
};
D.validate=function(spec){
 if(!spec||!D.render(spec))return false;
 if(spec.kind==='geo-segment')return spec.labels.length===3&&spec.labels.every(x=>/^[A-Z]$/.test(x))&&spec.labels[0]!==spec.labels[1]&&spec.labels[1]!==spec.labels[2]&&spec.labels[0]!==spec.labels[2];
 return true;
};
var prior=NS.figHtml;
NS.figHtml=function(spec){return D.render(spec)||(prior?prior(spec):'')};
})(typeof window!=='undefined'?window:globalThis);
