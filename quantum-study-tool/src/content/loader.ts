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

// --- Grouping for the home page ------------------------------------------------
// Topics are grouped by book and ordered by level (undergraduate -> graduate ->
// research) then by `order`, so the library scales from Griffiths toward
// Sakurai/Shankar just by adding content — no code changes needed.

/** Display ranking for levels (lowest first); unknown/absent levels sort last. */
const LEVEL_RANK: Record<string, number> = {
  undergraduate: 0,
  graduate: 1,
  research: 2,
};
const levelRank = (level?: string): number =>
  level !== undefined && level in LEVEL_RANK ? LEVEL_RANK[level] : 99;

/** A book's worth of topics, for sectioned display on the home page. */
export interface BookSection {
  /** Book display name, or 'Other' for topics with no `book`. */
  book: string;
  /** Distinct levels present in this book, ordered low → high. */
  levels: string[];
  /** Topics in this book, sorted by `order`. */
  topics: Topic[];
}

/** Topics grouped into book sections, ordered for the home page. */
export function getBookSections(): BookSection[] {
  const byBook = new Map<string, Topic[]>();
  for (const t of topics) {
    const key = t.book ?? 'Other';
    const list = byBook.get(key);
    if (list) list.push(t);
    else byBook.set(key, [t]);
  }

  const sections: BookSection[] = Array.from(byBook, ([book, ts]) => {
    const sorted = [...ts].sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
    const levels = Array.from(
      new Set(sorted.map((t) => t.level).filter((l): l is string => Boolean(l))),
    ).sort((a, b) => levelRank(a) - levelRank(b));
    return { book, levels, topics: sorted };
  });

  const minLevelRank = (s: BookSection) => Math.min(...s.topics.map((t) => levelRank(t.level)));
  const minOrder = (s: BookSection) => Math.min(...s.topics.map((t) => t.order ?? 0));

  return sections.sort(
    (a, b) =>
      minLevelRank(a) - minLevelRank(b) ||
      minOrder(a) - minOrder(b) ||
      a.book.localeCompare(b.book),
  );
}

/** All topics in home-page reading order (book sections, flattened). */
export function getOrderedTopics(): Topic[] {
  return getBookSections().flatMap((s) => s.topics);
}

/** The previous and next topics around `id` in reading order. */
export function getAdjacentTopics(id: string): { prev?: Topic; next?: Topic } {
  const ordered = getOrderedTopics();
  const index = ordered.findIndex((t) => t.id === id);
  if (index === -1) return {};
  return { prev: ordered[index - 1], next: ordered[index + 1] };
}
