#!/usr/bin/env bash
set -euo pipefail

site_root="${1:-_site}"
mkdir -p "$site_root"

python scripts/build-archive-pages.py "$site_root"

rm -rf .future-slides-build
if git ls-remote --exit-code --heads origin future-slides >/dev/null 2>&1; then
  # Fetch explicitly into the remote-tracking ref so this also works from
  # clones created with --single-branch, where origin/future-slides does not
  # exist until we create it ourselves.
  git fetch origin future-slides:refs/remotes/origin/future-slides
  git worktree add --detach .future-slides-build refs/remotes/origin/future-slides
  bash scripts/build-wip.sh .future-slides-build "$site_root/wip" "$PWD"
  git worktree remove --force .future-slides-build
else
  mkdir -p "$site_root/wip"
  cat > "$site_root/wip/index.html" <<'EOF'
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Work in Progress</title></head><body><h1>Work in Progress</h1><p>No future-slides branch is available.</p><p><a href="../index.html">Back to Slides Home</a></p></body></html>
EOF
fi
