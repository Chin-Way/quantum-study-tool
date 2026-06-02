# Authoring content

All study material lives under `content/` as plain, editable files — **no code
changes are needed to add or edit a topic.** Vite discovers folders at build time
(`import.meta.glob`), so you just drop a folder in and rebuild.

A content check (`npm run check:content`, also run automatically by `npm run
build`) validates every topic and **fails loudly** on a typo, so a malformed file
never silently breaks a page.

## Folder layout

Each topic is one folder under `content/`. The numeric prefix only controls the
order folders are listed on disk; the actual ordering in the app comes from the
`order` field (see below).

```
content/
  02-infinite-square-well/
    topic.json      # metadata (required)
    notes.md        # the lesson: Markdown + LaTeX (required)
    problems.json   # array of problems (optional)
```

## `topic.json`

```json
{
  "id": "infinite-square-well",
  "title": "The Infinite Square Well",
  "book": "Griffiths",
  "chapter": "2.2",
  "level": "undergraduate",
  "order": 2,
  "summary": "A particle confined to a 1-D box.",
  "viz": "isw-eigenstates",
  "related": ["harmonic-oscillator", "postulates"]
}
```

| Field     | Type             | Required | Notes |
|-----------|------------------|----------|-------|
| `id`      | string           | ✅       | Unique across all topics; used in the URL (`#/topic/<id>`). |
| `title`   | string           | ✅       | Display title. |
| `order`   | number           | ✅       | Sort order **within a book**. |
| `book`    | string           |          | Groups topics into a section on the home page (e.g. `Griffiths`, `Sakurai`). |
| `chapter` | string           |          | Free-form, e.g. `2.2`. |
| `level`   | string           |          | One of `undergraduate`, `graduate`, `research`. Books are ordered by level. |
| `summary` | string           |          | One-line description shown on the home page. |
| `viz`     | string \| null   |          | Id of a visualization to embed (must exist in `src/viz/registry.ts`). |
| `related` | string[]         |          | Ids of related topics; rendered as cross-links. Each must be a real topic id. |

## `notes.md`

Markdown with embedded LaTeX, rendered through MathJax:

- Inline math: `$ ... $` &nbsp;·&nbsp; Display math: `$$ ... $$`
- `##` / `###` headings become the in-topic **table of contents** (the leading
  `#` title is not listed).
- Link to another topic with an in-app hash route so navigation stays client-side:
  `[harmonic oscillator](#/topic/harmonic-oscillator)`. External `http(s)` links
  open in a new tab.

## `problems.json`

An array of problems with hideable solutions. Optional — a topic can be notes-only.

```json
[
  {
    "id": "isw-1",
    "prompt": "Compute $\\langle x \\rangle$ in the $n$-th stationary state.",
    "solution": "By symmetry, $\\langle x \\rangle = a/2$ ...",
    "difficulty": "easy",
    "tags": ["expectation-values"],
    "source": "Griffiths 2.4",
    "viz": null
  }
]
```

| Field        | Type           | Required | Notes |
|--------------|----------------|----------|-------|
| `id`         | string         | ✅       | Unique across **all** problems (progress tracking keys off it). |
| `prompt`     | string         | ✅       | Markdown + LaTeX. |
| `solution`   | string         | ✅       | Markdown + LaTeX; hidden until "Show solution". |
| `difficulty` | string         |          | One of `easy`, `medium`, `hard`. |
| `tags`       | string[]       |          | Used by the home-page tag filter and search. |
| `source`     | string         |          | e.g. `Griffiths 2.4`. |
| `viz`        | string \| null |          | Id of a visualization to embed under the prompt. |

> In JSON, every LaTeX backslash must be escaped: write `\\langle`, `\\frac`, and
> `\\\\` for a matrix row break.

## Visualizations

Content references a plot by string id only — the React/Plotly code lives in
`src/viz/`. To add one: create a component under `src/viz/plots/`, register it in
`src/viz/registry.ts`, then reference its id from a topic's or problem's `viz`
field. Unknown ids degrade to a small inline notice (and the content check flags
them).

## Checklist before committing

- [ ] `npm run check:content` passes (run automatically by `npm run build`).
- [ ] New `id`s are unique; `related` and `viz` ids exist.
- [ ] Math renders (no stray `$`), and headings read well in the table of contents.
