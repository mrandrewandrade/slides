#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

branch="$(git branch --show-current)"
if [[ "$branch" != "master" ]]; then
  echo "Publish from master only. Current branch: $branch" >&2
  echo "Run: git switch master" >&2
  exit 1
fi

# Keep master current without losing a small last-minute edit.
git pull --rebase --autostash

echo "Building the complete slide site locally..."
rm -rf _site
bash scripts/full-build.sh archive
bash scripts/build-published-extras.sh _site
touch _site/.nojekyll

# The full build may regenerate tracked cumulative decks, so commit after building.
git add -A
if ! git diff --cached --quiet; then
  git commit -m "Update slides $(date '+%Y-%m-%d %H:%M')"
fi

# Pushing master triggers the publishing workflow. The workflow mirrors the exact
# generated site to gh-pages and deploys the same build through GitHub Pages.
git push origin master

echo
echo "Pushed master. The workflow will update gh-pages and deploy GitHub Pages."
