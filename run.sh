#!/usr/bin/env bash
set -euo pipefail

python_cmd() {
  if command -v py >/dev/null 2>&1; then
    py -3 "$@"
  elif command -v python3 >/dev/null 2>&1; then
    python3 "$@"
  elif command -v python >/dev/null 2>&1; then
    python "$@"
  else
    echo "Python was not found." >&2
    exit 1
  fi
}

command="${1:-}"
command="${command,,}"

case "$command" in
  tej|tts|tas)
    # Fast classroom path: only the latest deck for this course.
    exec quarto preview "current/${command}.qmd"
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
  advance)
    target="${2:-}"
    target="${target,,}"
    case "$target" in
      tej|tts|tas|all)
        python_cmd scripts/semester_flow.py advance "$target"
        echo
        echo "Promotion complete. Review with: bash run.sh all"
        echo "When it looks right, commit the changed current/full files and archive HTML."
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
        python_cmd scripts/semester_flow.py status "$target"
        ;;
      *)
        echo "Use: bash run.sh status [tej|tts|tas|all]" >&2
        exit 1
        ;;
    esac
    ;;
  *)
    echo "Use: bash run.sh <tej|tts|tas|all>" >&2
    echo "     bash run.sh status [tej|tts|tas|all]" >&2
    echo "     bash run.sh advance <tej|tts|tas|all>" >&2
    exit 1
    ;;
esac
