#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
  echo "Usage: bash scripts/new-day.sh <day> <YYYY-MM-DD> <week>" >&2
  echo "Example: bash scripts/new-day.sh 2 2026-09-09 1" >&2
  exit 1
fi

exec bash scripts/slides.sh new "$1" "$2" "$3"
