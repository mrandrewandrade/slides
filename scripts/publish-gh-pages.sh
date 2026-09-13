#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if [[ ! -d _site ]]; then
  echo "_site does not exist. Build the site before publishing." >&2
  exit 1
fi

remote_url="$(git remote get-url origin)"
source_sha="$(git rev-parse --short HEAD)"
tmp_dir="$(mktemp -d "${TMPDIR:-/tmp}/slides-gh-pages.XXXXXX")"

cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

echo "Preparing gh-pages from _site..."

if git ls-remote --exit-code --heads origin gh-pages >/dev/null 2>&1; then
  git clone --quiet --branch gh-pages --single-branch "$remote_url" "$tmp_dir"
  find "$tmp_dir" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
else
  git clone --quiet --no-checkout "$remote_url" "$tmp_dir"
  (
    cd "$tmp_dir"
    git checkout --orphan gh-pages
    git rm -rf . >/dev/null 2>&1 || true
  )
fi

cp -a _site/. "$tmp_dir"/

(
  cd "$tmp_dir"
  git add -A

  if git diff --cached --quiet; then
    echo "gh-pages is already up to date."
    exit 0
  fi

  git commit -m "Publish slides ${source_sha}"
  git push origin gh-pages
)

echo "Published _site to gh-pages."
