#!/usr/bin/env bash
set -euo pipefail

if command -v py >/dev/null 2>&1; then
  exec py -3 "$@"
elif command -v python3 >/dev/null 2>&1; then
  exec python3 "$@"
elif command -v python >/dev/null 2>&1; then
  exec python "$@"
else
  echo "Python 3 was not found. Install Python 3 or add it to PATH." >&2
  exit 1
fi
