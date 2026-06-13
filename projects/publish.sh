#!/usr/bin/env bash
#
# Publish the three staged portfolio projects (and your GitHub profile README)
# as standalone PUBLIC repositories under your account.
#
# HOW TO RUN — from your own machine:
#
#     git clone https://github.com/Chin-Way/quantum-study-tool.git
#     cd quantum-study-tool
#     git checkout claude/confident-knuth-cksc2i
#     cd projects
#     bash publish.sh
#
# REQUIREMENTS:
#   - git
#   - the GitHub CLI (https://cli.github.com/), authenticated once with:
#         gh auth login
#
# This script is safe to re-run: repos that already exist are skipped, not
# overwritten. If you don't have `gh`, see PUBLISHING.md for manual steps.
#
set -euo pipefail

PROJECTS=(schrodinger-solver quantum-algorithms ml-ising-phases)

# --- preflight ------------------------------------------------------------
if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: GitHub CLI 'gh' not found -> https://cli.github.com/"
  echo "       (or follow the manual steps in PUBLISHING.md)"
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "ERROR: not logged in. Run:  gh auth login"
  exit 1
fi

GH_USER="$(gh api user --jq .login)"
echo "Publishing as GitHub user: $GH_USER"
echo

# --- one standalone repo per project --------------------------------------
for proj in "${PROJECTS[@]}"; do
  [ -d "$proj" ] || { echo "skip: '$proj' not found"; continue; }

  if gh repo view "$GH_USER/$proj" >/dev/null 2>&1; then
    echo "==> $proj  (repo already exists, skipping)"; echo; continue
  fi

  echo "==> $proj"
  (
    cd "$proj"
    rm -rf .git                       # fresh, clean history for this repo
    git init -q -b main
    git add .
    git commit -q -m "Initial commit: $proj"
    gh repo create "$GH_USER/$proj" --public --source=. --remote=origin --push
  )
  echo "    https://github.com/$GH_USER/$proj"
  echo
done

# --- profile README repo (must be named exactly like your username) -------
if [ -f PROFILE_README.md ]; then
  if gh repo view "$GH_USER/$GH_USER" >/dev/null 2>&1; then
    echo "==> profile README  (repo $GH_USER/$GH_USER already exists, skipping)"
  else
    echo "==> profile README ($GH_USER/$GH_USER)"
    tmp="$(mktemp -d)"
    cp PROFILE_README.md "$tmp/README.md"
    (
      cd "$tmp"
      git init -q -b main
      git add README.md
      git commit -q -m "Add profile README"
      gh repo create "$GH_USER/$GH_USER" --public --source=. --remote=origin --push
    )
    rm -rf "$tmp"
    echo "    https://github.com/$GH_USER  (then fill in the TODO contact lines)"
  fi
  echo
fi

echo "Done. Now pin them: github.com/$GH_USER -> 'Customize your pins'."
