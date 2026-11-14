'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function boot(){
 const fields=Object.fromEntries(['title','url','details','problem','provider'].map(k=>[k,{value:k==='provider'?'native':''}]));
 const listeners={},opened=[],fallback={},form={elements:fields};let dialog;
 const document={title:'Student practice',head:{appendChild(){}},body:{appendChild(){}},getElementById(){return null;},querySelector(){return {};},addEventListener(t,f){listeners[t]=f;},createElement(type){
  if(type!=='dialog')return {style:{},appendChild(){}};
  dialog={setAttribute(){},querySelector(s){if(s==='form')return form;if(s==='[data-close]')return {};if(s==='[data-fallback]')return fallback;const m=/\[name=(\w+)\]/.exec(s);return fields[m[1]];},addEventListener(t,f){this[t]=f;},dispatchEvent(e){this[e.type]?.();},showModal(){this.open=true;},close(){this.open=false;}};return dialog;
 }};
 const location={href:'https://mrksclassroom.com/worksheet-generator/course-game.html?student=1'};
 const window={open(...args){opened.push(args);}};
 vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../feedback.js'),'utf8'),{window,document,location,URL,URLSearchParams,Event:class{constructor(type){this.type=type}}});
 return {window,location,document,fields,form,opened,fallback,listeners,get dialog(){return dialog;}};
}
test('student reports preserve the assigned URL and open a draft without site navigation',()=>{
 const t=boot(),url='https://mrksclassroom.com//grade5/worksheet-generator/grade5-flashcards.html?unit=decimal-operations&student=1&skills=a';
 t.window.MK_FEEDBACK.open('Decimal flashcards',url);
 assert.equal(t.dialog.open,true);assert.equal(t.fields.title.value,'Decimal flashcards');
 assert.equal(t.fields.url.value,url.replace('.com//','.com/'));
 assert(t.fallback.href.startsWith('mailto:akneller@gmail.com?'));
 t.fields.problem.value='wrong answer';t.fields.details.value='Question 4: A & B\nPlease check.';t.fields.provider.value='gmail';
 t.form.onsubmit({preventDefault(){}});
 const draft=new URL(t.opened[0][0]);assert.equal(draft.searchParams.get('to'),'akneller@gmail.com');
 assert.match(draft.searchParams.get('body'),/Question 4: A & B\nPlease check\./);
 assert(draft.searchParams.get('body').includes('student=1&skills=a'));
 assert.equal(t.opened[0][2],'noopener,noreferrer');
});
test('existing card email links use the same dialog with the original resource context',()=>{
 const t=boot();let prevented=false;
 const source={dataset:{},getAttribute(){return 'mailto:akneller@gmail.com?body='+encodeURIComponent('Activity: My activity\nLink: https://mrksclassroom.com//financial/games/index.html?unit=income\n');},matches(){return true;}};
 t.listeners.click({target:{closest(){return source;}},preventDefault(){prevented=true;}});
 assert.equal(prevented,true);assert.equal(t.fields.title.value,'My activity');assert.equal(t.fields.url.value,'https://mrksclassroom.com/financial/games/index.html?unit=income');
 t.fields.provider.value='outlook';t.form.onsubmit({preventDefault(){}});
 assert.equal(new URL(t.opened[0][0]).hostname,'outlook.live.com');
});
