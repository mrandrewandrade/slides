#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "Usage: scripts/archive-current.sh <tej|tts|tas> <week-number> <day-number> <YYYY-MM-DD>" >&2
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

rm -rf "$tmp_dir"
mkdir -p "$archive_dir"

quarto render "$source_file" \
  --output-dir "$tmp_dir" \
  -M embed-resources:true

rendered_file="$(find "$tmp_dir" -type f -name "${course}.html" -print -quit)"

if [[ -z "$rendered_file" ]]; then
  echo "Could not find rendered ${course}.html." >&2
  rm -rf "$tmp_dir"
  exit 1
fi

cp "$rendered_file" "$archive_file"

# The current deck links one level up to the site index. Archived decks live
# deeper, so use the deployed /slides/ root instead.
sed -i 's#href="../index.html"#href="/slides/"#g' "$archive_file"

rm -rf "$tmp_dir"

echo "Archived: $archive_file"
