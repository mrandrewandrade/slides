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
if [[ "$branch" == "main" ]]; then
  echo "Pushed. GitHub will build the latest decks, archive today's published versions, refresh the index, and publish gh-pages."
else
  echo "Pushed branch '$branch'. It will be tested, but the live site publishes from main."
fi
