#!/usr/bin/env bash
set -euo pipefail

archive_root="${1:-archive}"

# The site index is generated for full builds, but index.qmd is tracked source.
# Preserve whatever is currently in the working tree so a local full preview
# never leaves the repository dirty or blocks the next git pull.
tmp_index="$(mktemp)"
had_index=0

if [[ -f index.qmd ]]; then
  cp index.qmd "$tmp_index"
  had_index=1
fi

restore_index() {
  if [[ "$had_index" -eq 1 ]]; then
    cp "$tmp_index" index.qmd
  else
    rm -f index.qmd
  fi
  rm -f "$tmp_index"
}

trap restore_index EXIT

bash scripts/site.sh index "$archive_root"
quarto render --profile full
