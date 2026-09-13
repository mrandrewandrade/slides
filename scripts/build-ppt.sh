#!/usr/bin/env bash
set -euo pipefail

target="${1:-tej}"
target="${target,,}"
mode="${2:-all}"
mode="${mode,,}"

case "$target" in
  tej|tts|tas) courses=("$target") ;;
  all) courses=(tej tts tas) ;;
  *)
    echo "Use: bash run.sh ppt <tej|tts|tas|all> [current|full|future|all]" >&2
    exit 1
    ;;
esac

case "$mode" in
  current|full|future|all) ;;
  *)
    echo "Use: bash run.sh ppt <tej|tts|tas|all> [current|full|future|all]" >&2
    exit 1
    ;;
esac

mkdir -p _site/pptx

render_pptx() {
  local course="$1"
  local kind="$2"
  local source="$3"
  local output_name="__${course}-${kind}.pptx"
  local source_dir
  source_dir="$(dirname "$source")"

  rm -f \
    "$source_dir/$output_name" \
    "$output_name" \
    "_site/$output_name" \
    "_site/pptx/${course}-${kind}.pptx"

  echo "Rendering ${course^^} ${kind} PPTX..."
  quarto render "$source" --to pptx --output "$output_name"

  local rendered=""
  for candidate in \
    "_site/$output_name" \
    "$source_dir/$output_name" \
    "$output_name"; do
    if [[ -f "$candidate" ]]; then
      rendered="$candidate"
      break
    fi
  done

  if [[ -z "$rendered" ]]; then
    echo "Could not find rendered PPTX for $source" >&2
    exit 1
  fi

  mv "$rendered" "_site/pptx/${course}-${kind}.pptx"
  echo "Created: _site/pptx/${course}-${kind}.pptx"
}

make_future_qmd() {
  local course="$1"
  local output="$2"

  bash scripts/python.sh - "$course" "$output" <<'PY'
from pathlib import Path
import sys

sys.path.insert(0, "scripts")
import semester_flow

course = sys.argv[1]
output = Path(sys.argv[2])
document = semester_flow.future_document(course)

if document is None:
    current = semester_flow.current_day(course)
    document = f'''---
course: "{course.upper()}"
---

# {course.upper()} Future Slide Deck

No staged slides exist after Day {current.day} yet.
'''

output.write_text(document, encoding="utf-8")
PY
}

for course in "${courses[@]}"; do
  if [[ "$mode" == "current" || "$mode" == "all" ]]; then
    render_pptx "$course" current "current/${course}.qmd"
  fi

  if [[ "$mode" == "full" || "$mode" == "all" ]]; then
    bash scripts/python.sh scripts/semester_flow.py sync "$course" >/dev/null
    render_pptx "$course" full "2026-27/semester-1/period-1/${course}/full.qmd"
  fi

  if [[ "$mode" == "future" || "$mode" == "all" ]]; then
    temp_qmd="__${course}-future.ppt.qmd"
    make_future_qmd "$course" "$temp_qmd"
    render_pptx "$course" future "$temp_qmd"
    rm -f "$temp_qmd"
  fi
done

echo
echo "PPTX files are in: _site/pptx/"
