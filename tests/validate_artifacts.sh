#!/usr/bin/env bash

set -euo pipefail

required_files=(
  "README.md"
  "spec.md"
  "plans.md"
  "implement.md"
  "documentation.md"
  "Makefile"
  "scripts/lint_markdown.sh"
  "scripts/typecheck_artifacts.sh"
  "scripts/build_bundle.sh"
)

for file in "${required_files[@]}"; do
  [[ -e "$file" ]] || { echo "Required artifact missing: $file" >&2; exit 1; }
done

echo "Artifact presence checks passed."
