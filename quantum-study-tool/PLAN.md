# Quantum Mechanics Study Tool — PLAN

A personal, browser-based study tool for quantum mechanics, meant to grow from
undergraduate (Griffiths) through graduate (Sakurai, Shankar) into research-level
topics. All study material lives in plain, editable files so the library can grow
without touching the application code.

This project lives in its **own dedicated repository** (suggested name:
`quantum-study-tool`). The plan and the app — `package.json`, `src/`, and
`content/` — all sit at the repository root, so it has its own dependencies,
build, and deployment (e.g. GitHub Pages), fully independent of your coursework.

---

## 1. Tech stack & rationale

**Vite + React + TypeScript** for the app; **MathJax** (via `rehype-mathjax`) for
LaTeX; **`react-markdown` + `remark-math`** to render Markdown notes with embedded
math; **`react-router`** for topic navigation; **Vite's `import.meta.glob`** to
auto-discover content files; and **Plotly (`react-plotly.js`)** for the interactive
visualizations in a later phase. The tradeoffs: React + TypeScript gives the
largest ecosystem and the strongest learning resources (a real help while you're
early in programming) plus type safety that catches mistakes before runtime, at the
cost of more boilerplate than a lighter setup; MathJax gives the broadest LaTeX
coverage — more environments, packages, and custom macros for research-level
notation — at the cost of being slower than KaTeX, which barely matters for mostly
static study pages; the Markdown-notes + JSON-problems split keeps prose pleasant to
write while giving problems clean, filterable metadata (book, difficulty, tags), at
the cost of maintaining two formats; and `import.meta.glob` means adding a topic is
just dropping a folder — content stays fully decoupled from code — with the only
cost being a quick rebuild to pick up new files, which is fine for local use.

---

## 2. Architecture

### Content model — the heart of "editable files, not hardcoded"

Every topic is a folder under `content/`. The app discovers these folders
automatically at build time (`import.meta.glob`), so **adding material never
requires editing application code** — you add or edit files and rebuild.

```
content/
  02-infinite-square-well/
    topic.json      # metadata: id, title, book, chapter, level, order, summary
    notes.md        # the lesson: Markdown + LaTeX ($...$ inline, $$...$$ display)
    problems.json   # array of problems with show/hide solutions
```

**`topic.json`**

```json
{
  "id": "infinite-square-well",
  "title": "The Infinite Square Well",
  "book": "Griffiths",
  "chapter": "2.2",
  "level": "undergraduate",
  "order": 2,
  "summary": "A particle confined to a 1-D box: the simplest bound-state problem."
}
```

**`problems.json`**

```json
[
  {
    "id": "isw-1",
    "prompt": "For the infinite square well of width $a$, compute $\\langle x \\rangle$ in the $n$-th stationary state.",
    "solution": "By symmetry about the center, $\\langle x \\rangle = a/2$ for every $n$. ...",
    "difficulty": "easy",
    "tags": ["expectation-values", "stationary-states"],
    "source": "Griffiths 2.4",
    "viz": null
  }
]
```

Text fields (`summary`, `prompt`, `solution`, and all of `notes.md`) may contain
LaTeX and are all rendered through the **same** pipeline, so math looks identical
everywhere.

### Rendering pipeline

A single `<Content>` component renders any Markdown-or-text string:
`react-markdown` → `remark-math` (parses `$...$`) → `rehype-mathjax` (typesets with
MathJax). Useful physics macros (e.g. `\bra`, `\ket`, `\braket`) are defined once in
the MathJax config so they work in every file.

### Visualizations (declarative reference)

Because content is data, it can't contain React components. Instead a problem or
topic references a visualization by id (`"viz": "isw-eigenstates"`), and a registry
in code (`src/viz/registry.ts`) maps that id to a Plotly-based component. Content
stays declarative; the plotting code stays in the app.

---

## 3. Folder structure

```
quantum-study-tool/                  # the repository root
├── PLAN.md
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
│
├── content/                     ← all study material (NOT code; edit freely)
│   ├── 01-postulates/
│   │   ├── topic.json
│   │   ├── notes.md
│   │   └── problems.json
│   └── 02-infinite-square-well/
│       └── ...
│
└── src/
    ├── main.tsx                 # entry
    ├── App.tsx                  # routes: "/" list, "/topic/:id" page
    ├── types.ts                 # Topic, Problem types
    ├── content/
    │   └── loader.ts            # import.meta.glob → sorted Topic[] index
    ├── components/
    │   ├── Layout.tsx
    │   ├── TopicList.tsx        # the topic list (home)
    │   ├── TopicPage.tsx        # one topic: notes + problems
    │   ├── Content.tsx          # Markdown + LaTeX renderer
    │   └── ProblemCard.tsx      # show/hide solution
    ├── viz/                     # added in Phase 2
    │   ├── registry.ts          # viz id → component
    │   └── plots/
    └── styles/
```

---

## 4. Phased build order (smallest useful version first)

**Phase 0 — Scaffold & de-risk math (tiny).**
Stand up Vite + React + TS; wire MathJax; render one hard-coded equation correctly
(e.g. the time-dependent Schrödinger equation). This proves the riskiest piece — the
LaTeX pipeline — before any content exists.

**Phase 1 — Minimal working tool (your defined milestone).**
- Content loader (`import.meta.glob`) builds the topic index from `content/`.
- A **topic list** on the home page.
- **One fully written topic** (the Infinite Square Well) with real `notes.md`.
- **A few problems** with **show/hide solutions**.
- Markdown + LaTeX rendering everywhere; basic routing, layout, and styling.
This proves the whole architecture end-to-end with real material.

**Phase 2 — Interactive visualizations (your top growth priority).**
Add Plotly + the viz registry; embed a first interactive plot — infinite-square-well
eigenstates $\psi_n(x)$ and $|\psi_n(x)|^2$ with a slider for $n$ — then the harmonic
oscillator. Establish the content→viz reference mechanism.

**Phase 3 — Scale content & navigation.**
Multiple books and levels (Griffiths / Sakurai / Shankar), sections and ordering,
prev/next navigation, a table of contents, and cross-links between topics — the
structure needed to grow undergrad → grad → research.

**Phase 4 — Quality-of-life (the lower-ranked features, as the library grows).**
Full-text search; filter by book / difficulty / tag; progress tracking in
`localStorage` (solved/unsolved, bookmarks).

**Phase 5 — Authoring & polish.**
A schema check so a typo in `problems.json` fails loudly instead of silently
breaking a page; an `AUTHORING.md` describing the content format; optional GitHub
Pages deploy; print/PDF export; a KaTeX fallback if MathJax ever feels slow.

---

## 5. Open questions / future

- Numerical needs at research level (eigenvalue solvers, complex linear algebra) may
  warrant a small library like `mathjs`; deferred until a topic actually needs it.
- If the content library gets very large, consider generating a static index at
  build time instead of globbing everything eagerly.
