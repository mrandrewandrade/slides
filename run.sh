#!/usr/bin/env bash
set -euo pipefail

course="${1:-}"

if [[ -z "$course" ]]; then
  echo "Choose a class:"
  select choice in TEJ TTS TAS; do
    case "$REPLY" in
      1) course="tej"; break ;;
      2) course="tts"; break ;;
      3) course="tas"; break ;;
      *) echo "Enter 1, 2, or 3." ;;
    esac
  done
fi

course="${course,,}"
case "$course" in
  tej|tts|tas) ;;
  *)
    echo "Use: bash run.sh tej   (or tts / tas)" >&2
    exit 1
    ;;
esac

# Fast classroom path: preview only the latest deck for this course.
exec quarto preview "current/${course}.qmd"
