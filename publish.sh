#!/usr/bin/env bash
set -euo pipefail

# Keep the checkout current without losing a small last-minute edit.
git pull --rebase --autostash

git add -A

if ! git diff --cached --quiet; then
  git commit -m "Update slides $(date '+%Y-%m-%d %H:%M')"
fi

git push

branch="$(git branch --show-current)"
if [[ "$branch" == "master" ]]; then
  echo "Pushed master. GitHub will build the complete slide site and refresh the gh-pages branch."
else
  echo "Pushed branch '$branch'. The published site is generated only from master."
fi
