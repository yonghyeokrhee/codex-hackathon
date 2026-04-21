SHELL := /bin/bash

.PHONY: test demo verify lint typecheck build

test:
	python -m unittest discover -s tests -p 'test_*.py'

demo:
	python src/cs_demo.py tests/fixtures/cs_seed.json --output dist/cs_demo_report.md

lint:
	@echo "No additional lint step configured."

typecheck:
	@echo "No additional typecheck step configured."

build:
	@mkdir -p dist
	@echo "Build step is artifact generation via make demo."

verify: test demo
