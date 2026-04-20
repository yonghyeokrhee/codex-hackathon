#!/usr/bin/env bash

set -euo pipefail

require_pattern() {
  local file="$1"
  local pattern="$2"

  if ! grep -F "$pattern" "$file" >/dev/null; then
    echo "Missing required section '$pattern' in $file" >&2
    exit 1
  fi
}

require_pattern "spec.md" "# Linear Priority Scoring Agent Spec"
require_pattern "spec.md" "## Objective"
require_pattern "spec.md" "## Constraints"
require_pattern "spec.md" "## Success criteria"

require_pattern "plans.md" "# Execution Plan"
require_pattern "plans.md" "## Milestone 0: Lock the target"
require_pattern "plans.md" "## Milestone 5: Verification hardening"

require_pattern "implement.md" "# Long-Running Job Runbook"
require_pattern "implement.md" "## Execution loop"
require_pattern "implement.md" "## Logging requirements"

require_pattern "documentation.md" "# Live Status and Audit Log"
require_pattern "documentation.md" "## Current status"
require_pattern "documentation.md" "## Session log"

echo "Artifact type checks passed."
