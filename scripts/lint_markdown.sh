#!/usr/bin/env bash

set -euo pipefail

files=(
  "README.md"
  "spec.md"
  "plans.md"
  "implement.md"
  "documentation.md"
)

for file in "${files[@]}"; do
  [[ -f "$file" ]] || { echo "Missing file: $file" >&2; exit 1; }

  if grep -n '[[:space:]]$' "$file" >/dev/null; then
    echo "Trailing whitespace found in $file" >&2
    exit 1
  fi

  if [[ ! -s "$file" ]]; then
    echo "Empty markdown file: $file" >&2
    exit 1
  fi
done

echo "Markdown lint checks passed."
