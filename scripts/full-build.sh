#!/usr/bin/env bash
set -euo pipefail

archive_root="${1:-archive}"

# index.qmd is generated for the full site, but it is tracked source.
# Restore the working copy after the render so local builds do not leave git dirty.
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

# Full is generated from the current pointer before every complete local build.
bash scripts/python.sh scripts/semester_flow.py sync all

# Remove stale output from the older per-day/semester layout.
for course in tej tts tas; do
  rm -rf "_site/2026-27/semester-1/period-1/${course}"
done

bash scripts/site.sh index "$archive_root"
quarto render --profile full
