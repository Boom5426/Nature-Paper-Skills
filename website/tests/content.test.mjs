import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {parseArray,frontmatter,generate} from '../scripts/generate-content.mjs';
import {buildInstallation,agents,operatingSystems,methods,profileFlags} from '../src/lib/installation.mjs';
const data=await generate();
test('installer arrays are explicit, safe, nonempty and unique',()=>{
 assert.deepEqual(parseArray('SKILLS=(\n  core/one\n  core/two # note\n)\n','SKILLS'),['core/one','core/two']);
 for(const source of ['SKILLS=()','SKILLS=(\n core/one\n core/one\n)','SKILLS=(\n $(unsafe)\n)','NOT_SKILLS=(\n core/one\n)'])assert.throws(()=>parseArray(source,'SKILLS'));
});
test('YAML frontmatter preserves folded descriptions',()=>{
 assert.deepEqual(frontmatter('---\nname: example\ndescription: >-\n  First line\n  second line.\n---\n'),{name:'example',description:'First line second line.'});
 assert.throws(()=>frontmatter('name: example'));assert.throws(()=>frontmatter('---\nname: 12\ndescription: hi\n---'));
});
test('every source skill has a unique ID and correct profile memberships',()=>{
 assert.equal(data.skills.length,new Set(data.skills.map(s=>s.id)).size);
 for(const profile of ['all','recommended','figures'])assert.equal(data.skills.filter(s=>s.profiles.includes(profile)).length,data.counts[profile]);
 assert.ok(data.counts.all>=data.counts.figures&&data.counts.figures>data.counts.recommended);
 assert.ok(data.skills.find(s=>s.id==='paper-workflow')?.profiles.includes('recommended'));
 assert.ok(data.skills.find(s=>s.id==='nature-figure')?.profiles.includes('figures'));
 assert.ok(!data.skills.find(s=>s.id==='nature-figure')?.profiles.includes('recommended'));
});
test('teaching example uses exact source paragraphs and preserves the numeric record',async()=>{
 assert.ok(data.example.raw.draft.includes(data.example.draft));assert.ok(data.example.raw.expected.includes(data.example.revision));
 assert.ok(data.example.draft.endsWith(data.example.claim));assert.ok(data.example.revision.endsWith(data.example.summary));
 const numbers=s=>s.match(/[−-]?\d+(?:\.\d+)?/g).sort();assert.deepEqual(numbers(data.example.draft),numbers(data.example.revision));
 const stored=JSON.parse(await readFile(new URL('../src/data/repository.json',import.meta.url),'utf8'));assert.equal(stored.sourceFingerprint,data.sourceFingerprint);
});
for(const locale of ['en','zh'])for(const agent of agents)for(const os of operatingSystems)for(const profile of Object.keys(profileFlags))for(const method of methods){
 test(`installation ${locale}/${agent}/${os}/${profile}/${method}`,()=>{
  const result=buildInstallation({agent,os,profile,method,locale},data.counts);
  const blocked=method!=='prompt'&&(agent==='web'||os==='windows');assert.equal(result.blocked,blocked);assert.ok(result.text);
  if(blocked){assert.ok(!result.text.includes('bash -s'));assert.equal(result.verification,'');return;}
  if(method==='prompt'){assert.ok(result.text.includes(`${data.counts[profile]}`));assert.ok(result.text.includes(profileFlags[profile]));assert.ok(result.text.includes('/blob/main/INSTALL.md'));}
  else {assert.ok(result.text.includes(`--agent ${agent} ${profileFlags[profile]}`));assert.ok(result.text.includes('--on-conflict keep'));assert.ok(result.verification.includes(`${profileFlags[profile]} --doctor`));}
  if(agent==='web')assert.ok(!result.text.includes('curl -fsSL'));
  if(method==='clone')assert.ok(result.text.includes('&&\ncd Nature-Paper-Skills &&\n'));
 });
}
test('bad selections are rejected rather than interpolated into shell commands',()=>{
 const good={locale:'en',agent:'codex',os:'linux',profile:'all',method:'command'};
 for(const [key,value]of Object.entries({agent:'codex; rm -rf /',os:'unknown',profile:'21',method:'run',locale:'xx'}))assert.throws(()=>buildInstallation({...good,[key]:value},data.counts));
 assert.throws(()=>buildInstallation(good,{...data.counts,all:0}));
});
test('installation text follows changed source counts, not hardcoded 19/21/27',()=>{
 const result=buildInstallation({locale:'en',agent:'claude',os:'macos',profile:'all',method:'prompt'},{all:30,recommended:20,figures:22});assert.ok(result.text.includes('30 skills'));assert.ok(!result.text.includes('27 skills'));
});
