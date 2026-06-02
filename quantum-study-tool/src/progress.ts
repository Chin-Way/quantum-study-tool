import { useSyncExternalStore } from 'react';

/**
 * Progress tracking, persisted in localStorage:
 *   - solved problem ids
 *   - bookmarked topic ids
 *
 * A tiny external store (subscribe + snapshot) lets any component read or toggle
 * state via useSyncExternalStore, so a solved toggle in one place updates the
 * progress badges everywhere. Writes degrade silently if storage is unavailable.
 */

const SOLVED_KEY = 'qst:solved';
const BOOKMARKS_KEY = 'qst:bookmarks';

type Listener = () => void;
const listeners = new Set<Listener>();

function load(key: string): Set<string> {
  try {
    const raw = localStorage.getItem(key);
    const parsed = raw ? JSON.parse(raw) : null;
    return Array.isArray(parsed) ? new Set(parsed as string[]) : new Set();
  } catch {
    return new Set();
  }
}

function save(key: string, value: Set<string>): void {
  try {
    localStorage.setItem(key, JSON.stringify([...value]));
  } catch {
    // ignore (private mode, quota, etc.)
  }
}

let solved = load(SOLVED_KEY);
let bookmarks = load(BOOKMARKS_KEY);

function emit(): void {
  for (const l of listeners) l();
}

function subscribe(listener: Listener): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function toggle(set: Set<string>, id: string): Set<string> {
  const next = new Set(set);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  return next;
}

export function toggleSolved(id: string): void {
  solved = toggle(solved, id);
  save(SOLVED_KEY, solved);
  emit();
}

export function toggleBookmark(id: string): void {
  bookmarks = toggle(bookmarks, id);
  save(BOOKMARKS_KEY, bookmarks);
  emit();
}

/** Subscribe to the live set of solved problem ids. */
export function useSolved(): Set<string> {
  return useSyncExternalStore(subscribe, () => solved, () => solved);
}

/** Subscribe to the live set of bookmarked topic ids. */
export function useBookmarks(): Set<string> {
  return useSyncExternalStore(subscribe, () => bookmarks, () => bookmarks);
}
