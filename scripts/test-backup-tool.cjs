#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync('backup.html','utf8');
const match=html.match(/<script>([\s\S]*?)<\/script>/i);
assert(match,'Backup tool must include its application script');

function setup(initial){
 const handlers={},data=new Map(Object.entries(initial||{})),downloads=[];
 const elements={};
 for(const id of ['file','import','export','replace','status','summary','preview']){
  elements[id]={id,disabled:id==='import',checked:false,textContent:'',files:[],addEventListener(type,fn){handlers[id+':'+type]=fn}};
 }
 const doc={
  getElementById(id){return elements[id]},
  createElement(tag){assert.equal(tag,'a');return {click(){downloads.push({href:this.href,download:this.download})},remove(){}}},
  body:{appendChild(){}}
 };
 const storage={
  get length(){return data.size},
  key(i){return Array.from(data.keys())[i]||null},
  getItem(k){return data.has(k)?data.get(k):null},
  setItem(k,v){data.set(k,String(v))}
 };
 const mockURL={createObjectURL(){return 'blob:backup'},revokeObjectURL(){}};
 const sandbox={document:doc,localStorage:storage,location:{origin:'https://mrksclassroom.com'},URL:mockURL,Blob,Date,setTimeout(){},console};
 vm.runInNewContext(match[1],sandbox,{filename:'backup.html script'});
 return {handlers,elements,data,downloads};
}
async function run(){
 const saved=['worksheet-1','worksheet-2'];
 const src=setup({'mrk-saved':JSON.stringify(saved),'lesson-draft':'saved work'});
 assert(src.elements.summary.textContent.includes('2 browser storage entries'));
 src.handlers['export:click']();
 assert.equal(src.downloads.length,1,'Export must initiate one download');
 assert(src.downloads[0].download.endsWith('.json'));
 const json=JSON.stringify({format:'mrks-classroom-browser-backup',version:1,origin:'https://mrksclassroom.com',storage:{'mrk-saved':'["restored"]','lesson-draft':'restored draft','extra':'new'}});
 const dest=setup({'mrk-saved':'["keep-existing"]'});
 dest.elements.file.files=[{size:json.length,text:async()=>json}];
 dest.handlers['file:change']();
 await Promise.resolve();await Promise.resolve();
 assert.equal(dest.elements.import.disabled,false,'Valid backup should unlock import');
 dest.handlers['import:click']();
 assert.equal(dest.data.get('mrk-saved'),'["keep-existing"]','Default import must preserve existing work');
 assert.equal(dest.data.get('lesson-draft'),'restored draft');
 assert.equal(dest.data.get('extra'),'new');
 dest.elements.replace.checked=true;
 dest.handlers['import:click']();
 assert.equal(dest.data.get('mrk-saved'),'["restored"]','Overwrite should require explicit choice');
 const bad=setup({});
 bad.elements.file.files=[{size:100,text:async()=>JSON.stringify({format:'mrks-classroom-browser-backup',version:1,origin:'https://other.example',storage:{x:'bad'}})}];
 bad.handlers['file:change']();
 await Promise.resolve();await Promise.resolve();
 assert.equal(bad.elements.import.disabled,true,'Foreign-origin data must be rejected');
 assert.equal(bad.data.size,0);
 console.log('PASS backup export/import: download, preserve existing, explicit overwrite and domain validation');
}
run().catch(e=>{console.error(e);process.exitCode=1});
