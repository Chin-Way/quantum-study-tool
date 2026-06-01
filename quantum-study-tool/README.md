# Quantum Mechanics Study Tool

A personal, browser-based study tool for quantum mechanics. Notes are written in
Markdown + LaTeX; problems live in JSON with show/hide solutions. All study
material lives in `content/`, so you add topics **without touching the app code**.

See [`PLAN.md`](./PLAN.md) for the architecture and the phased roadmap.

## Run it

You need **Node.js 18+** installed (https://nodejs.org).

```bash
npm install      # one time: download dependencies
npm run dev      # start the dev server
```

Then open the printed URL (usually http://localhost:5173).

Other commands:

```bash
npm run build    # type-check + produce an optimized build in dist/
npm run preview  # preview that production build locally
```

## Add a topic (no code changes needed)

Create a new folder under `content/`, e.g. `content/03-harmonic-oscillator/`, with
three files:

- `topic.json` — metadata (`id`, `title`, `book`, `chapter`, `level`, `order`, `summary`)
- `notes.md` — the lesson, in Markdown + LaTeX (`$...$` inline, `$$...$$` display)
- `problems.json` — an array of problems (`prompt`, `solution`, `difficulty`, `tags`, `source`)

The app discovers the folder automatically the next time it (re)builds. Use the two
existing topics as templates. Topics are ordered by the `order` field.

## Tech

Vite + React + TypeScript · MathJax (via `rehype-mathjax`) for math · `react-markdown`
+ `remark-math` for Markdown · `react-router` for navigation.
