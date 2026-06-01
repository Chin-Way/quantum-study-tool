import type { Problem, Topic, TopicMeta } from '../types';

// --- Auto-discovery of content -------------------------------------------------
// These globs are resolved by Vite at build time, so dropping a new folder into
// content/ (with topic.json + notes.md + problems.json) adds a topic with no code
// changes. Patterns are relative to the project root.

const metaModules = import.meta.glob('/content/*/topic.json', { eager: true }) as Record<
  string,
  { default: TopicMeta }
>;

const notesModules = import.meta.glob('/content/*/notes.md', {
  eager: true,
  query: '?raw',
  import: 'default',
}) as Record<string, string>;

const problemModules = import.meta.glob('/content/*/problems.json', { eager: true }) as Record<
  string,
  { default: Problem[] }
>;

/** '/content/02-foo/topic.json' -> '/content/02-foo' */
function folderOf(path: string): string {
  return path.slice(0, path.lastIndexOf('/'));
}

function buildTopics(): Topic[] {
  const byFolder = new Map<string, Partial<Topic>>();

  const ensure = (folder: string): Partial<Topic> => {
    let entry = byFolder.get(folder);
    if (!entry) {
      entry = {};
      byFolder.set(folder, entry);
    }
    return entry;
  };

  for (const [path, mod] of Object.entries(metaModules)) {
    Object.assign(ensure(folderOf(path)), mod.default);
  }
  for (const [path, raw] of Object.entries(notesModules)) {
    ensure(folderOf(path)).notes = raw;
  }
  for (const [path, mod] of Object.entries(problemModules)) {
    ensure(folderOf(path)).problems = mod.default;
  }

  return Array.from(byFolder.values())
    .map((t) => ({ notes: '', problems: [], ...t }) as Topic)
    .filter((t) => Boolean(t.id))
    .sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
}

/** All topics, sorted by their `order` field. */
export const topics: Topic[] = buildTopics();

/** Look up a single topic by its `id`. */
export function getTopic(id: string): Topic | undefined {
  return topics.find((t) => t.id === id);
}
