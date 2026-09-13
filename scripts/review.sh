#!/usr/bin/env bash
set -euo pipefail

target="${1:-tej}"
target="${target,,}"

case "$target" in
  tej|tts|tas) ;;
  *)
    echo "Use: bash scripts/review.sh <tej|tts|tas>" >&2
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

open_url() {
  local browser="$1"
  local url="$2"

  if command -v cmd.exe >/dev/null 2>&1; then
    local native_browser
    native_browser="$(native_path "$browser")"
    cmd.exe /c start "" "$native_browser" "$url" >/dev/null 2>&1 || true
  else
    "$browser" "$url" >/dev/null 2>&1 &
  fi
}

browser="$(find_browser || true)"
if [[ -z "$browser" ]]; then
  echo "Could not find Chrome, Chromium, or Edge." >&2
  exit 1
fi

echo "Building full slide site..."
bash scripts/full-build.sh archive
bash scripts/build-published-extras.sh _site

port=4202
server_log="${TMPDIR:-/tmp}/slides-review-server.log"
bash scripts/python.sh -m http.server "$port" --directory _site >"$server_log" 2>&1 &
server_pid=$!

profile_dir="$(mktemp -d)"
cleanup() {
  kill "$server_pid" >/dev/null 2>&1 || true
  wait "$server_pid" 2>/dev/null || true
  rm -rf "$profile_dir"
}
trap cleanup EXIT INT TERM

sleep 1
if ! kill -0 "$server_pid" >/dev/null 2>&1; then
  echo "Could not start local review server on port $port." >&2
  cat "$server_log" >&2 || true
  exit 1
fi

base_url="http://127.0.0.1:${port}/2026-27/semester-1/period-1/${target}/full.html"
review_dir="$(pwd)/_site/review"
mkdir -p "$review_dir"

# Capture the actual browser presentation viewport, not the PDF print layout.
for slide in 0 1; do
  number=$((slide + 1))
  output="$review_dir/${target}-slide-0${number}.png"
  native_output="$(native_path "$output")"
  native_profile="$(native_path "$profile_dir")"

  "$browser" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --force-device-scale-factor=1 \
    --window-size=1440,960 \
    --virtual-time-budget=1800 \
    --user-data-dir="$native_profile" \
    --screenshot="$native_output" \
    "${base_url}#/${slide}" >/dev/null 2>&1 || true

done

open_url "$browser" "$base_url"

echo
echo "Live deck opened:"
echo "  $base_url"
echo
echo "Browser screenshots for layout review:"
echo "  _site/review/${target}-slide-01.png"
echo "  _site/review/${target}-slide-02.png"
echo
echo "This live browser view is the authority for what students see."
echo "Press Ctrl+C here when you are finished reviewing."
echo

wait "$server_pid"
