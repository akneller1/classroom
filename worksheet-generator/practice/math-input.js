/* Editable math templates for student input: never changes grading rules. */
(function(G){
'use strict';
var API=G.MKMATHINPUT={};
API.insert=function(value,start,end,kind){
 value=String(value||'');start=Math.max(0,Math.min(value.length,start|0));end=Math.max(start,Math.min(value.length,end|0));
 var chosen=value.slice(start,end),before=value.slice(0,start),after=value.slice(end),insert='',a=0,b=0;
 if(kind==='fraction'){
   insert=(chosen||'0')+'/1';
   a=start+(chosen?chosen.length+1:0);b=a+1; // denominator selected; numerator is a usable placeholder
   if(!chosen){a=start;b=start+1;} // first edit numerator
 }else if(kind==='sqrt'){
   insert='sqrt('+(chosen||'0')+')';
   a=start+5;b=a+(chosen?chosen.length:1);
 }else if(kind==='power'){
   insert='^('+ (chosen||'2') +')';
   a=start+2;b=a+(chosen?chosen.length:1);
 }else if(kind==='square'){
   insert='^2';a=b=start+insert.length;
 }else if(kind==='next'){
   var from=end;
   var m=/\/1\b/.exec(value.slice(from));
   if(m)return {text:value,start:from+m.index+1,end:from+m.index+2};
   return {text:value,start:end,end:end};
 }else if(kind==='backspace'){
   if(start===end&&start>0)start--;
   return {text:value.slice(0,start)+value.slice(end),start:start,end:start};
 }else{
   insert=String(kind);a=b=start+insert.length;
 }
 return {text:before+insert+after,start:a,end:b};
};
})(window);