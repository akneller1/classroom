'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),{execFileSync}=require('node:child_process');
test('final generator versions replace stale overlay tags and change when asset contents change',()=>{
 const out=fs.mkdtempSync(path.join(os.tmpdir(),'generator-version-'));
 try{
  const dir=path.join(out,'worksheet-generator','menu');fs.mkdirSync(dir,{recursive:true});
  const script=path.join(dir,'app.js'),page=path.join(out,'worksheet-generator','worksheet.html');
  fs.writeFileSync(script,'first release');
  fs.writeFileSync(page,'<script src="menu/app.js?v=solo-20261116"></script><script src="https://other.example/menu/app.js?v=external"></script>');
  fs.writeFileSync(path.join(out,'index.html'),'<script src="/worksheet-generator/menu/app.js?v=old"></script>');
  const run=()=>execFileSync(process.execPath,['scripts/version-generator-assets.mjs',out]);run();
  const read=()=>fs.readFileSync(page,'utf8'),first=read();assert.match(first,/menu\/app\.js\?v=[a-f0-9]{16}/);
  assert.ok(!first.includes('solo-20261116'));assert.ok(first.includes('https://other.example/menu/app.js?v=external'));
  const version=/menu\/app\.js\?v=([a-f0-9]{16})/.exec(first)[1];assert.ok(fs.readFileSync(path.join(out,'index.html'),'utf8').includes(version));
  run();assert.equal(read(),first);fs.writeFileSync(script,'corrected release');run();assert.notEqual(read(),first);
 }finally{fs.rmSync(out,{recursive:true,force:true});}
});
