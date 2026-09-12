#!/usr/bin/env bash
set -euo pipefail

course="${1:-}"
course="${course,,}"

case "$course" in
  tej|tts|tas) ;;
  *)
    echo "Use: bash run.sh <tej|tts|tas>" >&2
    exit 1
    ;;
esac

# Fast classroom path: preview only the latest deck for this course.
exec quarto preview "current/${course}.qmd"
