#!/usr/bin/env bash
set -euo pipefail

archive_root="${1:-archive}"

# Build the normal current site first.
bash scripts/site.sh index "$archive_root"
quarto render

# Build the draft/alternate views that appear under Work in Progress.
for course in tej tts tas; do
  quarto render "2026-27/semester-1/period-1/${course}/index.qmd"
  quarto render "2026-27/semester-1/period-1/${course}/semester.qmd"
  quarto render "2026-27/semester-1/period-1/${course}/week-01/index.qmd"
  quarto render "2026-27/semester-1/period-1/${course}/week-01/day-01.qmd"
done
