#!/usr/bin/env bash
set -euo pipefail

course="${1:-}"
course="${course,,}"

case "$course" in
  tej|tts|tas)
    # Fast classroom path: only the latest deck for this course.
    exec quarto preview "current/${course}.qmd"
    ;;
  all)
    echo "Building full slide site..."
    bash scripts/full-build.sh archive
    bash scripts/site.sh snapshot _site/archive
    bash scripts/build-published-extras.sh _site

    echo
    echo "Full site ready: http://localhost:4200/"
    echo "Press Ctrl+C to stop the local server."
    echo

    # On Windows, the Python launcher is usually the most reliable option.
    if command -v py >/dev/null 2>&1; then
      exec py -m http.server 4200 --directory _site
    elif command -v python >/dev/null 2>&1; then
      exec python -m http.server 4200 --directory _site
    else
      echo "Could not start a local server automatically." >&2
      echo "Open _site/index.html directly in your browser." >&2
      exit 0
    fi
    ;;
  *)
    echo "Use: bash run.sh <tej|tts|tas|all>" >&2
    exit 1
    ;;
esac
