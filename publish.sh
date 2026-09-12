#!/usr/bin/env bash
set -euo pipefail

# Keep the local checkout current without losing small local edits.
git pull --rebase --autostash

# Fast validation build. Archived slides are not re-rendered.
quarto render

# Commit and push any slide/source changes. GitHub Actions deploys main to Pages.
git add -A

if ! git diff --cached --quiet; then
  git commit -m "Update slides $(date '+%Y-%m-%d %H:%M')"
fi

git push

branch="$(git branch --show-current)"
if [[ "$branch" == "main" ]]; then
  echo "Published source changes. GitHub Actions will deploy the site to Pages."
else
  echo "Pushed branch '$branch'. Pages deployment occurs when the changes reach main."
fi
