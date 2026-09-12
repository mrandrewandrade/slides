#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "Usage: scripts/archive-current.sh <tej|tts|tas> <week-number> <day-number> <YYYY-MM-DD>" >&2
  echo "Example: scripts/archive-current.sh tej 01 01 2026-09-08" >&2
  exit 1
fi

course="${1,,}"
week="$2"
day="$3"
date="$4"

case "$course" in
  tej|tts|tas) ;;
  *)
    echo "Course must be tej, tts, or tas." >&2
    exit 1
    ;;
esac

source_file="current/${course}.qmd"
archive_dir="archive/2026-27/semester-1/${course}/week-${week}"
archive_file="${archive_dir}/${date}-day-${day}.html"
tmp_dir=".archive-build"

if [[ ! -f "$source_file" ]]; then
  echo "Missing current deck: $source_file" >&2
  exit 1
fi

rm -rf "$tmp_dir"
mkdir -p "$archive_dir"

# Archive builds are self-contained so old decks do not depend on future site assets.
quarto render "$source_file" \
  --output-dir "$tmp_dir" \
  -M embed-resources:true

rendered_file="$(find "$tmp_dir" -type f -name "${course}.html" -print -quit)"

if [[ -z "$rendered_file" ]]; then
  echo "Could not find the rendered ${course}.html file." >&2
  rm -rf "$tmp_dir"
  exit 1
fi

cp "$rendered_file" "$archive_file"

# Daily source uses a relative home link while it lives under current/.
# Archived files live deeper, so make the home link stable for /slides/ deployment.
python - "$archive_file" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
text = text.replace('href="../index.html"', 'href="/slides/"')
path.write_text(text, encoding="utf-8")
PY

rm -rf "$tmp_dir"

echo "Archived: $archive_file"
echo "Next: change that day's link in index.qmd from current/${course}.html to ${archive_file}."
