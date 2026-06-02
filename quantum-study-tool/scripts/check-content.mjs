// Content schema check: validates every topic under content/ so a typo in
// topic.json / problems.json fails loudly (here, and in CI via `npm run build`)
// instead of silently breaking a page at runtime. No dependencies.
//
// Run directly with:  npm run check:content
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const CONTENT_DIR = 'content';
const DIFFICULTIES = new Set(['easy', 'medium', 'hard']);
const LEVELS = new Set(['undergraduate', 'graduate', 'research']);

const errors = [];
const fail = (where, msg) => errors.push(`${where}: ${msg}`);
const isStr = (v) => typeof v === 'string' && v.trim() !== '';

// Best-effort: read the viz ids registered in src/viz/registry.ts so a typo in a
// content `viz` reference is caught too.
const vizIds = new Set();
try {
  for (const m of readFileSync('src/viz/registry.ts', 'utf8').matchAll(/'([^']+)':\s*lazy\(/g)) {
    vizIds.add(m[1]);
  }
} catch {
  // registry optional; skip viz-id validation if it can't be read
}

function readJson(path, where) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (e) {
    fail(where, `invalid JSON (${e.message})`);
    return undefined;
  }
}

const folders = existsSync(CONTENT_DIR)
  ? readdirSync(CONTENT_DIR).filter((f) => statSync(join(CONTENT_DIR, f)).isDirectory())
  : [];

const topicIds = new Set();
const problemOwners = new Map(); // problem id -> folder
const topicsMeta = []; // { folder, meta }
let problemCount = 0;

for (const folder of folders) {
  const base = join(CONTENT_DIR, folder);
  const topicPath = join(base, 'topic.json');
  const notesPath = join(base, 'notes.md');
  const problemsPath = join(base, 'problems.json');

  if (!existsSync(topicPath)) {
    fail(folder, 'missing topic.json');
    continue;
  }
  if (!existsSync(notesPath) || readFileSync(notesPath, 'utf8').trim() === '') {
    fail(folder, 'missing or empty notes.md');
  }

  // --- topic.json ---
  const meta = readJson(topicPath, `${folder}/topic.json`);
  if (meta === undefined) continue;
  const at = `${folder}/topic.json`;

  if (!isStr(meta.id)) fail(at, 'missing/empty "id" (string)');
  else if (topicIds.has(meta.id)) fail(at, `duplicate topic id "${meta.id}"`);
  else topicIds.add(meta.id);

  if (!isStr(meta.title)) fail(at, 'missing/empty "title" (string)');
  if (typeof meta.order !== 'number') fail(at, '"order" must be a number');

  for (const k of ['book', 'chapter', 'level', 'summary']) {
    if (meta[k] != null && typeof meta[k] !== 'string') fail(at, `"${k}" must be a string`);
  }
  if (isStr(meta.level) && !LEVELS.has(meta.level)) {
    fail(at, `unknown level "${meta.level}" (expected: ${[...LEVELS].join(', ')})`);
  }
  if (meta.viz != null) {
    if (!isStr(meta.viz)) fail(at, '"viz" must be a string or null');
    else if (vizIds.size && !vizIds.has(meta.viz)) {
      fail(at, `viz "${meta.viz}" is not registered in src/viz/registry.ts`);
    }
  }
  if (meta.related != null && !Array.isArray(meta.related)) {
    fail(at, '"related" must be an array of topic ids');
  }

  topicsMeta.push({ folder, meta });

  // --- problems.json (optional) ---
  if (existsSync(problemsPath)) {
    const problems = readJson(problemsPath, `${folder}/problems.json`);
    if (problems === undefined) continue;
    if (!Array.isArray(problems)) {
      fail(`${folder}/problems.json`, 'must be a JSON array');
      continue;
    }
    problems.forEach((p, i) => {
      const pat = `${folder}/problems.json[${i}]`;
      if (!isStr(p.id)) fail(pat, 'missing/empty "id"');
      else if (problemOwners.has(p.id)) fail(pat, `duplicate problem id "${p.id}" (also in ${problemOwners.get(p.id)})`);
      else problemOwners.set(p.id, folder);

      if (!isStr(p.prompt)) fail(pat, 'missing/empty "prompt"');
      if (!isStr(p.solution)) fail(pat, 'missing/empty "solution"');
      if (p.difficulty != null && !DIFFICULTIES.has(p.difficulty)) {
        fail(pat, `"difficulty" must be one of: ${[...DIFFICULTIES].join(', ')}`);
      }
      if (p.tags != null && (!Array.isArray(p.tags) || p.tags.some((t) => typeof t !== 'string'))) {
        fail(pat, '"tags" must be an array of strings');
      }
      if (p.source != null && typeof p.source !== 'string') fail(pat, '"source" must be a string');
      if (p.viz != null) {
        if (!isStr(p.viz)) fail(pat, '"viz" must be a string or null');
        else if (vizIds.size && !vizIds.has(p.viz)) fail(pat, `viz "${p.viz}" is not registered`);
      }
      problemCount += 1;
    });
  }
}

// --- cross-references: related ids must point to real topics ---
for (const { folder, meta } of topicsMeta) {
  if (Array.isArray(meta.related)) {
    for (const r of meta.related) {
      if (!isStr(r)) fail(`${folder}/topic.json`, '"related" entries must be non-empty strings');
      else if (!topicIds.has(r)) fail(`${folder}/topic.json`, `related id "${r}" does not match any topic`);
    }
  }
}

if (errors.length) {
  console.error(`\n✗ Content check failed — ${errors.length} issue${errors.length === 1 ? '' : 's'}:\n`);
  for (const e of errors) console.error(`  • ${e}`);
  console.error('');
  process.exit(1);
}

console.log(`✓ Content OK — ${topicsMeta.length} topics, ${problemCount} problems.`);
