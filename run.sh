#!/usr/bin/env bash
set -euo pipefail

python_flow() {
  bash scripts/python.sh scripts/semester_flow.py "$@"
}

command="${1:-}"
command="${command,,}"

case "$command" in
  tej|tts|tas)
    exec quarto preview "current/${command}.qmd"
    ;;
  all)
    echo "Building full slide site..."
    bash scripts/full-build.sh archive
    bash scripts/build-published-extras.sh _site

    echo
    echo "Full site ready: http://localhost:4200/"
    echo "Press Ctrl+C to stop the local server."
    echo

    exec bash scripts/python.sh -m http.server 4200 --directory _site
    ;;
  review)
    target="${2:-tej}"
    target="${target,,}"
    case "$target" in
      tej|tts|tas)
        exec bash scripts/review.sh "$target"
        ;;
      *)
        echo "Use: bash run.sh review [tej|tts|tas]" >&2
        exit 1
        ;;
    esac
    ;;
  pdf)
    target="${2:-tej}"
    target="${target,,}"
    case "$target" in
      tej|tts|tas|all)
        exec bash scripts/print-pdf.sh "$target"
        ;;
      *)
        echo "Use: bash run.sh pdf [tej|tts|tas|all]" >&2
        exit 1
        ;;
    esac
    ;;
  advance)
    target="${2:-}"
    target="${target,,}"
    case "$target" in
      tej|tts|tas|all)
        python_flow advance "$target"
        echo
        echo "Promotion complete. Run: bash run.sh all"
        ;;
      *)
        echo "Use: bash run.sh advance <tej|tts|tas|all>" >&2
        exit 1
        ;;
    esac
    ;;
  status)
    target="${2:-all}"
    target="${target,,}"
    case "$target" in
      tej|tts|tas|all)
        python_flow status "$target"
        ;;
      *)
        echo "Use: bash run.sh status [tej|tts|tas|all]" >&2
        exit 1
        ;;
    esac
    ;;
  sync)
    target="${2:-all}"
    target="${target,,}"
    case "$target" in
      tej|tts|tas|all)
        python_flow sync "$target"
        ;;
      *)
        echo "Use: bash run.sh sync [tej|tts|tas|all]" >&2
        exit 1
        ;;
    esac
    ;;
  *)
    echo "Use: bash run.sh <tej|tts|tas|all>" >&2
    echo "     bash run.sh all" >&2
    echo "     bash run.sh review [tej|tts|tas]" >&2
    echo "     bash run.sh pdf [tej|tts|tas|all]" >&2
    echo "     bash run.sh status [tej|tts|tas|all]" >&2
    echo "     bash run.sh advance <tej|tts|tas|all>" >&2
    echo "     bash run.sh sync [tej|tts|tas|all]" >&2
    exit 1
    ;;
esac
