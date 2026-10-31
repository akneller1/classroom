/* Manifest-driven loading of independently approved question-bank files.
 * Manifest entries must be explicitly approved during editorial review.
 * No unreviewed bank is made available to student-facing consumers.
 */
(function(root){
'use strict';
var adapter=root.MK_QUESTION_BANKS;
function load(manifest, fetchJSON){
 if(!adapter||typeof fetchJSON!=='function') return Promise.reject(new Error('Question bank adapter or fetcher unavailable'));
 if(!manifest||manifest.version!==1||!Array.isArray(manifest.banks)) return Promise.reject(new Error('Invalid bank manifest'));
 var allowed=Object.create(null),entries=[];
 manifest.banks.forEach(function(item){
  if(!item||!item.courseId||!item.unitId||typeof item.path!=='string'||!/^question-banks\/[a-z0-9/_-]+\.json$/.test(item.path))
   throw new Error('Invalid manifest entry');
  var id=item.courseId+'/'+item.unitId;
  if(allowed[id])throw new Error('Duplicate manifest entry '+id);
  allowed[id]=true;
  if(item.approved===true)entries.push(item);
 });
 return Promise.all(entries.map(function(item){
  return Promise.resolve().then(function(){return fetchJSON(item.path)}).then(function(bank){
   if(!bank||bank.courseId!==item.courseId||bank.unitId!==item.unitId) throw new Error('Course/unit mismatch: '+item.path);
   var validation=adapter.validate(bank);
   if(!validation.ok)throw new Error(item.path+': '+validation.errors.join('; '));
   return {item:item,bank:bank};
  });
 })).then(function(results){
  // Validate every approved file before registering any, to avoid partial loads on validation failure.
  return results.map(function(result){
   var applied=adapter.register(result.bank,{verified:true});
   if(!applied.ok)throw new Error(result.item.path+': '+applied.errors.join('; '));
   return result.item.courseId+'/'+result.item.unitId;
  });
 });
}
function loadFromSite(path,base){
 base=base||'';
 if(base!==''&&base!=='../')return Promise.reject(new Error('Invalid bank base path'));
 path=path||'question-banks/manifest.json';
 if(!/^question-banks\/[a-z0-9/_-]+\.json$/.test(path))return Promise.reject(new Error('Invalid manifest path'));
 if(typeof root.fetch!=='function')return Promise.reject(new Error('Fetch unavailable'));
 function read(url){return root.fetch(base+url,{cache:'no-store'}).then(function(res){if(!res.ok)throw new Error('Unable to load '+url);return res.json()});}
 return read(path).then(function(manifest){return load(manifest,read)});
}
root.MK_BANK_LOADER={version:1,load:load,loadFromSite:loadFromSite};
})(typeof window!=='undefined'?window:globalThis);
