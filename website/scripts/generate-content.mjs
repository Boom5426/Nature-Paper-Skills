import { readdir, readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { parse } from 'yaml';

export const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
export function parseArray(text, name) {
  const match = text.match(new RegExp(`^${name}=\\(\\s*([\\s\\S]*?)^\\)`, 'm'));
  if (!match) throw new Error(`Installer array missing: ${name}`);
  const entries = match[1].split('\n').map(x => x.replace(/#.*/, '').trim()).filter(Boolean);
  if (!entries.length || entries.some(x => !/^[a-z][a-z0-9-]*\/[a-z][a-z0-9-]*$/.test(x)))
    throw new Error(`Unsupported syntax in ${name}; update the parser against install.sh.`);
  if (new Set(entries).size !== entries.length) throw new Error(`Duplicate skill in ${name}`);
  return entries;
}
export function frontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!match) throw new Error('Missing YAML frontmatter');
  const value = parse(match[1]);
  if (!value || typeof value.name !== 'string' || typeof value.description !== 'string')
    throw new Error('Skill must have a string name and description');
  return { name: value.name, description: value.description.trim() };
}
const read = p => readFile(resolve(ROOT, p), 'utf8');
export async function generate() {
  const installer = await read('install.sh');
  const recommended = parseArray(installer, 'RECOMMENDED_SKILLS');
  const figure = parseArray(installer, 'FIGURE_SKILLS');
  const skills = [];
  for (const category of (await readdir(resolve(ROOT, 'skills'), { withFileTypes: true })).filter(d => d.isDirectory()).sort((a,b) => a.name.localeCompare(b.name))) {
    for (const folder of (await readdir(resolve(ROOT, 'skills', category.name), { withFileTypes: true })).filter(d => d.isDirectory()).sort((a,b) => a.name.localeCompare(b.name))) {
      const path = `skills/${category.name}/${folder.name}/SKILL.md`;
      let contents;
      try { contents = await read(path); } catch (error) { if (error.code === 'ENOENT') continue; throw error; }
      const meta = frontmatter(contents);
      if (meta.name !== folder.name) throw new Error(`Skill name/path disagree: ${path}`);
      const relative = `${category.name}/${folder.name}`;
      skills.push({ id: meta.name, description: meta.description, category: category.name, path,
        profiles: ['all', ...(recommended.includes(relative) ? ['recommended', 'figures'] : figure.includes(relative) ? ['figures'] : [])] });
    }
  }
  const paths = new Set(skills.map(s => s.path.replace(/^skills\//, '').replace(/\/SKILL.md$/, '')));
  for (const p of [...recommended, ...figure]) if (!paths.has(p)) throw new Error(`Installer names a missing skill: ${p}`);
  if (skills.length !== new Set(skills.map(s => s.id)).size) throw new Error('Duplicate skill identifiers');
  const raw = Object.fromEntries(await Promise.all(['draft', 'evidence', 'expected'].map(async name => [name, await read(`examples/first-run/${name}.md`)])));
  const paragraph = value => value.trim().split(/\r?\n\s*\r?\n/).find(p => !p.startsWith('#') && !p.startsWith('This '));
  const draft = paragraph(raw.draft), revision = paragraph(raw.expected);
  if (!draft || !revision) throw new Error('First-run example paragraph cannot be resolved');
  const evidence = raw.evidence.split('\n').filter(l => l.startsWith('- ')).map(l => l.slice(2));
  const lastSentence = p => p.match(/[^.!?]+[.!?]\s*$/)?.[0].trim() || p;
  const contracts = await read('skills/core/paper-workflow/references/section-contracts.md');
  for (const section of ['Abstract', 'Results', 'Discussion', 'Methods']) if (!contracts.includes(`## ${section}\n`)) throw new Error(`Section contract absent: ${section}`);
  const version = (await read('VERSION')).trim();
  const data = {
    version, skills, counts: { all: skills.length, recommended: recommended.length, figures: new Set([...recommended, ...figure]).size },
    example: { draft, revision, evidence, claim: lastSentence(draft), summary: lastSentence(revision), raw },
    sourceFingerprint: createHash('sha256').update(JSON.stringify({ installer, raw, contracts, skills, version })).digest('hex'),
  };
  const destination = resolve(ROOT, 'website/src/data/repository.json');
  await mkdir(dirname(destination), { recursive: true });
  await writeFile(destination, `${JSON.stringify(data, null, 2)}\n`);
  console.log(`Source-bound content: ${data.counts.all} skills / ${data.counts.recommended} recommended / ${data.counts.figures} with figures; v${version}`);
  return data;
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) await generate();
