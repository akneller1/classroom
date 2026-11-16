'use strict';
const fs=require('node:fs'),path=require('node:path');
function localTarget(root,href,base){
 const url=new URL(href,base),origin=new URL(base).origin;
 if(url.origin!==origin)throw Error('Off-site resource: '+href);
 let file=path.resolve(root,'.'+decodeURIComponent(url.pathname));
 if(file!==root&&!file.startsWith(root+path.sep))throw Error('Resource escapes site root');
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)||!fs.statSync(file).isFile())throw Error('Missing resource: '+url.pathname);
 return file;
}
function browserSample(links,base,limit=96,courseByHref=new Map()){
 const html=links.filter(h=>! /\.(pdf|docx|pptx|zip)(?:[?#]|$)/i.test(h));
 const selected=new Set(),courses=new Map(),engines=new Map();
 for(const href of html){const u=new URL(href,base),course=courseByHref.get(href)||u.searchParams.get('course')||u.pathname.match(/^\/(grade[1-5])\//)?.[1]||'shared';
 const list=courses.get(course)||[];list.push(href);courses.set(course,list);
 const engine=u.pathname.replace(/grade[1-5]/g,'grade')+'|'+(u.searchParams.get('game')||'');
 if(!engines.has(engine))engines.set(engine,href);
 }
 // Cover each course, then each distinct player/tool. Keep routine work bounded.
 for(const list of courses.values())if(selected.size<limit)selected.add(list[0]);
 for(const href of engines.values())if(selected.size<limit)selected.add(href);
 for(let i=1;i<3;i++)for(const list of courses.values())if(list[i]&&selected.size<limit)selected.add(list[i]);
 return [...selected];
}
module.exports={localTarget,browserSample};
