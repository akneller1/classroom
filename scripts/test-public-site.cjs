/* Validate only the generated public-site contract; existing activity mathematics has separate checks. */
'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const out=path.resolve('_site'),home=fs.readFileSync(path.join(out,'index.html'),'utf8');
assert(home.includes('mk-static'),'Missing crawlable catalog');assert(home.includes('og:image'),'Missing link-preview metadata');
assert(home.includes('assets/fonts/classroom-fonts.css'),'Homepage fonts must be local');
for(const dir of ['.git','.github','scripts','audits','incoming','docs','tools','patches'])assert(!fs.existsSync(path.join(out,dir)),'Working files published: '+dir);
assert(!home.includes('u/math6/')&&!home.includes('u/prealgebra7/'),'Hidden courses exposed in catalog');
const sitemap=fs.readFileSync(path.join(out,'sitemap.xml'),'utf8');
assert(!sitemap.includes('/u/math6/')&&!sitemap.includes('/u/prealgebra7/'),'Hidden courses exposed in sitemap');
const courses=fs.readdirSync(path.join(out,'u'));assert.equal(courses.length,4);let count=0;
const checkLinks=(file,text)=>{for(const match of text.matchAll(/(?:href|src)="([^"<>]+)"/g)){
 const link=match[1].replace(/&amp;/g,'&');if(/^(?:https?:|data:|mailto:|#)/.test(link))continue;
 const raw=link.split(/[?#]/)[0];if(!raw)continue;
 const target=path.resolve(path.dirname(file),decodeURIComponent(raw));assert(target===out||target.startsWith(out+path.sep),'Link escapes site: '+link);assert(fs.existsSync(target),'Missing generated link '+path.relative(out,file)+': '+link);
}};
checkLinks(path.join(out,'index.html'),home);
for(const course of courses)for(const unit of fs.readdirSync(path.join(out,'u',course))){
 const file=path.join(out,'u',course,unit,'index.html'),html=fs.readFileSync(file,'utf8');
 assert(html.includes('../../../#'+course+'.'+unit),'Incorrect app route: '+course+'/'+unit);
 for(const page of ['lesson-planner.html','worksheet.html','printables.html','menu-assessment.html'])assert(html.includes('worksheet-generator/'+page),'Missing generator '+page+' in '+course+'/'+unit);
 checkLinks(file,html);count++;
}
assert.equal(count,40);assert.equal((sitemap.match(/<loc>/g)||[]).length,41);
for(const file of ['favicon.svg','social-preview.png','apple-touch-icon.png'])assert(fs.existsSync(path.join(out,'assets',file)),'Missing branding asset '+file);
assert(fs.existsSync(path.join(out,'schemas')),'Runtime schemas missing');assert(fs.existsSync(path.join(out,'legacy-crosswalk-audit.js')),'Runtime grade bridge dependency missing');
console.log('PASS public build: four visible courses, 40 unit pages, generator links, sitemap, local fonts, metadata, assets and excluded working files');
