#!/usr/bin/env bash
set -euo pipefail

target="${1:-tej}"
target="${target,,}"

case "$target" in
  tej|tts|tas)
    courses=("$target")
    ;;
  all)
    courses=(tej tts tas)
    ;;
  *)
    echo "Use: bash scripts/print-pdf.sh <tej|tts|tas|all>" >&2
    exit 1
    ;;
esac

find_browser() {
  local candidate

  for candidate in \
    "$(command -v google-chrome 2>/dev/null || true)" \
    "$(command -v google-chrome-stable 2>/dev/null || true)" \
    "$(command -v chromium 2>/dev/null || true)" \
    "$(command -v chromium-browser 2>/dev/null || true)" \
    "$(command -v chrome 2>/dev/null || true)" \
    "$(command -v msedge 2>/dev/null || true)" \
    "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
    "/c/Program Files/Microsoft/Edge/Application/msedge.exe" \
    "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"; do
    if [[ -n "$candidate" && -f "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return 0
    fi
  done

  return 1
}

native_path() {
  local path="$1"
  if command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$path"
  else
    printf '%s\n' "$path"
  fi
}

browser="$(find_browser || true)"
if [[ -z "$browser" ]]; then
  echo "Could not find Chrome, Chromium, or Edge." >&2
  echo "Install one of those browsers or add it to PATH." >&2
  exit 1
fi

echo "NOTE: headless PDF output is for rough export only."
echo "      Use 'bash run.sh review <course>' to judge the actual browser layout."
echo

echo "Building full slide site..."
bash scripts/full-build.sh archive
bash scripts/build-published-extras.sh _site

mkdir -p _site/pdfs

port=4201
server_log="${TMPDIR:-/tmp}/slides-pdf-server.log"
bash scripts/python.sh -m http.server "$port" --directory _site >"$server_log" 2>&1 &
server_pid=$!

cleanup() {
  kill "$server_pid" >/dev/null 2>&1 || true
  wait "$server_pid" 2>/dev/null || true
}
trap cleanup EXIT

sleep 1
if ! kill -0 "$server_pid" >/dev/null 2>&1; then
  echo "Could not start temporary local server on port $port." >&2
  cat "$server_log" >&2 || true
  exit 1
fi

for course in "${courses[@]}"; do
  output="$(pwd)/_site/pdfs/${course}-full.pdf"
  native_output="$(native_path "$output")"
  url="http://127.0.0.1:${port}/2026-27/semester-1/period-1/${course}/full.html?print-pdf"

  rm -f "$output"
  echo "Printing ${course^^} Full deck..."

  "$browser" \
    --headless=new \
    --disable-gpu \
    --no-pdf-header-footer \
    --print-to-pdf="$native_output" \
    "$url" >/dev/null 2>&1

  if [[ ! -s "$output" ]]; then
    echo "Browser did not create $output" >&2
    exit 1
  fi

  echo "Created: _site/pdfs/${course}-full.pdf"
done
