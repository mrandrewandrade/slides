#!/usr/bin/env bash
set -euo pipefail

course="${1:-}"
course="${course,,}"

case "$course" in
  tej|tts|tas)
    exec quarto preview "current/${course}.qmd"
    ;;
  all)
    bash scripts/site.sh index archive
    exec quarto preview --profile full
    ;;
  *)
    echo "Use: bash run.sh <tej|tts|tas|all>" >&2
    exit 1
    ;;
esac
