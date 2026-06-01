import { topics } from './loader';

/** Active search box + filter state. Empty string means "no filter". */
export interface SearchFilters {
  query: string;
  book: string;
  difficulty: string;
  tag: string;
}

interface IndexEntry {
  id: string;
  /** Lowercased blob of all searchable text for the topic and its problems. */
  haystack: string;
  book?: string;
  difficulties: Set<string>;
  tags: Set<string>;
}

// Built once at load: topics are eager-imported, so the index is static.
const index: IndexEntry[] = topics.map((t) => {
  const parts: (string | undefined)[] = [t.title, t.summary, t.book, t.chapter, t.level, t.notes];
  const difficulties = new Set<string>();
  const tags = new Set<string>();

  for (const p of t.problems) {
    parts.push(p.prompt, p.solution, p.source);
    if (p.difficulty) difficulties.add(p.difficulty);
    for (const tag of p.tags ?? []) {
      tags.add(tag);
      parts.push(tag);
    }
  }

  return {
    id: t.id,
    haystack: parts.filter(Boolean).join('\n').toLowerCase(),
    book: t.book,
    difficulties,
    tags,
  };
});

/** Ids of topics matching every query term (AND) and all active filters. */
export function searchTopics({ query, book, difficulty, tag }: SearchFilters): Set<string> {
  const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
  const ids = new Set<string>();

  for (const e of index) {
    if (book && e.book !== book) continue;
    if (difficulty && !e.difficulties.has(difficulty)) continue;
    if (tag && !e.tags.has(tag)) continue;
    if (terms.length && !terms.every((term) => e.haystack.includes(term))) continue;
    ids.add(e.id);
  }

  return ids;
}

const DIFFICULTY_ORDER = ['easy', 'medium', 'hard'];

/** Distinct books, difficulties, and tags present in the library, for the filter menus. */
export function filterOptions(): { books: string[]; difficulties: string[]; tags: string[] } {
  const books = new Set<string>();
  const difficulties = new Set<string>();
  const tags = new Set<string>();

  for (const e of index) {
    if (e.book) books.add(e.book);
    e.difficulties.forEach((d) => difficulties.add(d));
    e.tags.forEach((t) => tags.add(t));
  }

  return {
    books: [...books].sort(),
    difficulties: [...difficulties].sort(
      (a, b) => DIFFICULTY_ORDER.indexOf(a) - DIFFICULTY_ORDER.indexOf(b),
    ),
    tags: [...tags].sort(),
  };
}
