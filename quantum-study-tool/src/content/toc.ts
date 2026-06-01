/**
 * Helpers for building a per-topic table of contents from Markdown notes.
 * The same `slugify` sets heading ids (see Markdown.tsx) and builds the ToC
 * links, so a ToC entry always resolves to its rendered section heading.
 */

/** Turn heading text into a URL-safe slug, e.g. "The potential" -> "the-potential". */
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export interface Heading {
  /** 2 for `##`, 3 for `###`. */
  depth: number;
  text: string;
  slug: string;
}

/** Extract h2/h3 section headings from a Markdown string (ignoring code fences). */
export function extractHeadings(markdown: string): Heading[] {
  const headings: Heading[] = [];
  let inFence = false;

  for (const line of markdown.split('\n')) {
    if (/^\s*(```|~~~)/.test(line)) {
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;

    const match = /^(#{2,3})\s+(.+?)\s*#*\s*$/.exec(line);
    if (match) {
      const text = match[2].trim();
      headings.push({ depth: match[1].length, text, slug: slugify(text) });
    }
  }

  return headings;
}
