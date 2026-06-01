export type Difficulty = 'easy' | 'medium' | 'hard';

/** One practice problem with a hideable solution. Lives in a topic's problems.json. */
export interface Problem {
  id: string;
  prompt: string;
  solution: string;
  difficulty?: Difficulty;
  tags?: string[];
  source?: string;
  /** Optional id of a visualization to embed (used from Phase 2 onward). */
  viz?: string | null;
}

/** Topic metadata, authored in a topic's topic.json. */
export interface TopicMeta {
  id: string;
  title: string;
  book?: string;
  chapter?: string;
  level?: string;
  order: number;
  summary?: string;
  /** Optional id of a visualization to embed in the topic (see src/viz/registry.ts). */
  viz?: string | null;
}

/** A fully loaded topic: its metadata plus the notes and problems on disk. */
export interface Topic extends TopicMeta {
  notes: string;
  problems: Problem[];
}
