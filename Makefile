SHELL := /bin/bash

.PHONY: test lint typecheck build verify

test:
	bash tests/validate_artifacts.sh

lint:
	bash scripts/lint_markdown.sh

typecheck:
	bash scripts/typecheck_artifacts.sh

build:
	bash scripts/build_bundle.sh

verify: test lint typecheck build
