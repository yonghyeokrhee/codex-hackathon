#!/usr/bin/env bash

set -euo pipefail

mkdir -p dist

{
  echo "# Linear priority scoring agent briefing"
  echo
  echo "Generated from repository planning artifacts."
  echo
  echo "## spec.md"
  echo
  cat spec.md
  echo
  echo "## plans.md"
  echo
  cat plans.md
  echo
  echo "## implement.md"
  echo
  cat implement.md
  echo
  echo "## documentation.md"
  echo
  cat documentation.md
} > dist/agent-brief.md

echo "Built dist/agent-brief.md"
