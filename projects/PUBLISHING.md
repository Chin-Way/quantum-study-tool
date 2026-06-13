# Publishing these projects as their own repositories

These three projects were built and tested here, but they are **staged inside a
branch of `quantum-study-tool`** because the assistant that created them could
only write to that one repository. For your GitHub to look its best, each should
become its **own standalone public repo** (separate repos show up individually,
each with its own README, language stats, and CI badge).

This takes about 5 minutes. You only need to do it once.

> **Fastest path:** if you have the [GitHub CLI](https://cli.github.com/)
> (`gh auth login`), just run **`bash publish.sh`** from this `projects/`
> folder — it creates and pushes all three project repos *and* your profile
> repo in one go. The manual steps below are the fallback if you'd rather not
> use a script.

---

## Step 0 — get the files onto your machine

```bash
git clone https://github.com/Chin-Way/quantum-study-tool.git
cd quantum-study-tool
git checkout claude/confident-knuth-cksc2i
cd projects
ls    # schrodinger-solver  quantum-algorithms  ml-ising-phases  PROFILE_README.md ...
```

(If you already have the repo cloned, just `git fetch origin` and
`git checkout claude/confident-knuth-cksc2i`.)

It's worth running the tests first so you can see them pass on your own machine —
that's the whole point of these being *yours*:

```bash
cd schrodinger-solver && pip install -r requirements.txt && python -m pytest -q && cd ..
```

---

## Step 1 — publish each project

### Easiest: with the GitHub CLI (`gh`)

If you have [`gh`](https://cli.github.com/) installed and logged in
(`gh auth login`), run this from inside the `projects/` folder:

```bash
for proj in schrodinger-solver quantum-algorithms ml-ising-phases; do
  (
    cd "$proj"
    git init -b main
    git add .
    git commit -m "Initial commit: $proj"
    gh repo create "Chin-Way/$proj" --public --source=. --remote=origin --push
  )
done
```

Done — all three are now live at `github.com/Chin-Way/<project>`.

### Manual: GitHub website + git

For each project (repeat three times):

1. Go to <https://github.com/new>. Name it exactly `schrodinger-solver`
   (then `quantum-algorithms`, then `ml-ising-phases`). **Public.** Do **not**
   add a README/license/.gitignore — the project already has them.
2. Then:

   ```bash
   cd schrodinger-solver
   git init -b main
   git add .
   git commit -m "Initial commit: schrodinger-solver"
   git remote add origin https://github.com/Chin-Way/schrodinger-solver.git
   git push -u origin main
   ```

The CI workflow in each repo's `.github/workflows/ci.yml` will run automatically
on first push — you should get a green ✓ and can add the badge to the README.

---

## Step 2 — set up your profile README

A repo named **exactly** the same as your username shows its README at the top of
your profile page (`github.com/Chin-Way`).

1. Open `PROFILE_README.md` and fill in (or delete) the two TODO contact lines.
2. Publish it:

   ```bash
   mkdir Chin-Way && cd Chin-Way
   cp ../PROFILE_README.md README.md
   git init -b main
   git add README.md
   git commit -m "Add profile README"
   gh repo create Chin-Way/Chin-Way --public --source=. --remote=origin --push
   # ...or create the repo on github.com/new (named Chin-Way) and push manually
   ```

---

## Step 3 (optional but recommended) — tidy the existing repos

- **`CSC-111-projects`** has no README. Even a short one ("Coursework for CSC 111
  at Wabash — intro to programming in Python") helps. Consider pinning your best
  course project instead of the whole dump.
- **Pin** your strongest repos on your profile (Customize your pins): put
  `schrodinger-solver`, `quantum-algorithms`, `ml-ising-phases`, and
  `quantum-study-tool` front and center.
- Add the **CI badge** to each new README once it's green:
  `![tests](https://github.com/Chin-Way/<repo>/actions/workflows/ci.yml/badge.svg)`

---

## A note on owning this work

These projects are real, they're tested, and they're a great foundation — but
they're most valuable when you can *speak to every line*. Before you lean on them
in an application or interview:

- Read through each module and run the demos yourself.
- Tweak something: add a new potential to `schrodinger-solver`, a new gate or the
  Bernstein–Vazirani algorithm to `quantum-algorithms`, or a larger lattice /
  different model to `ml-ising-phases`. A commit history that shows *you* growing
  the project is worth far more than a perfect initial drop.
- Each README has a "References" section — those are the sources to read to
  understand the physics behind the code.
