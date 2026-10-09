import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..');
const dist=resolve(root,'website/dist');
const base='/Nature-Paper-Skills/';
const origin='https://boom5426.github.io';
const failures=[];let checked=0;
async function walk(path){return(await Promise.all((await readdir(path,{withFileTypes:true})).map(e=>e.isDirectory()?walk(resolve(path,e.name)):[resolve(path,e.name)]))).flat();}
async function file(path){try{return await stat(path);}catch{return undefined;}}
const htmlFiles=(await walk(dist)).filter(p=>p.endsWith('.html'));
for(const path of htmlFiles){
 const html=await readFile(path,'utf8');
 if((html.match(/<h1[\s>]/g)||[]).length!==1)failures.push(`${relative(dist,path)}: needs exactly one H1`);
 if(!html.includes('rel="canonical"')||!html.includes('hreflang="zh-CN"'))failures.push(`${path}: SEO language metadata missing`);
 for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  const href=match[1].replaceAll('&amp;','&');
  if(!href||href.startsWith('javascript:')||href==='#'){failures.push(`${path}: empty or nonfunctional link ${href}`);continue;}
  if(href.startsWith('data:')||href.startsWith('mailto:'))continue;
  if(href.startsWith('https://github.com/Boom5426/Nature-Paper-Skills/blob/main/')){
   const source=decodeURIComponent(new URL(href).pathname.split('/blob/main/')[1]);
   if(!await file(resolve(root,source)))failures.push(`${path}: missing repository source ${source}`);
   checked++;continue;
  }
  const pageURL=new URL(base+relative(dist,path).replace(/index\.html$/,''),origin);
  const target=new URL(href,pageURL);
  if(target.origin!==origin)continue;
  if(!target.pathname.startsWith(base)){failures.push(`${path}: internal URL escapes Pages base ${href}`);continue;}
  let targetPath=resolve(dist,decodeURIComponent(target.pathname.slice(base.length)));
  const st=await file(targetPath);if(st?.isDirectory())targetPath=resolve(targetPath,'index.html');
  if(!await file(targetPath)){failures.push(`${path}: broken internal link ${href}`);continue;}
  if(target.hash&&targetPath.endsWith('.html')){
   const id=decodeURIComponent(target.hash.slice(1));const content=await readFile(targetPath,'utf8');
   if(!content.includes(`id="${id}"`))failures.push(`${path}: missing anchor ${href}`);
  }
  checked++;
 }
 for(const match of html.matchAll(/property="og:image" content="([^"]+)"/g)){
  const asset=resolve(dist,new URL(match[1]).pathname.slice(base.length));
  if(!await file(asset))failures.push(`${path}: missing social preview ${asset}`);
 }
}
const expected=['','workflow','tasks','examples/first-revision','skills','install','docs'];
for(const locale of ['','zh/'])for(const route of expected){const path=resolve(dist,locale,route,'index.html');if(!await file(path))failures.push(`Missing bilingual route ${path}`);}
if(failures.length){console.error(failures.join('\n'));process.exit(1);}
console.log(`PASS: ${htmlFiles.length} HTML pages, ${checked} internal/source references, bilingual routes and social previews.`);
