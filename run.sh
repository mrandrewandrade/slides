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
    # Slow inspection path: build the complete current site, published archive
    # pages, and future Work in Progress pages, then serve the static result.
    bash scripts/full-build.sh archive
    bash scripts/site.sh snapshot _site/archive
    bash scripts/build-published-extras.sh _site

    if command -v cmd.exe >/dev/null 2>&1; then
      cmd.exe /c start "" "http://localhost:4200/" >/dev/null 2>&1 || true
    fi

    if command -v python >/dev/null 2>&1; then
      exec python -m http.server 4200 --directory _site
    elif command -v py >/dev/null 2>&1; then
      exec py -m http.server 4200 --directory _site
    else
      echo "Full site built in _site/. Open _site/index.html in a browser." >&2
      exit 0
    fi
    ;;
  *)
    echo "Use: bash run.sh <tej|tts|tas|all>" >&2
    exit 1
    ;;
esac
