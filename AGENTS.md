# Repository Guidelines

## Project Structure & Module Organization
This repository is intentionally minimal at the moment. The top level currently contains only [README.md](/Users/yong/codex-hackathon/README.md). Add new application code under a dedicated source directory such as `src/`, place tests in `tests/`, and keep static assets in `assets/` if they are introduced. Avoid mixing implementation, fixtures, and documentation at the repository root.

## Build, Test, and Development Commands
There is no build or test toolchain configured yet. For now, the main inspection commands are:

- `ls -la` to inspect the repository contents
- `rg --files` to list tracked files quickly
- `git status` to review local changes before committing

When adding tooling, document the canonical commands here and in `README.md` (for example `npm test`, `pytest`, or `make build`).

## Coding Style & Naming Conventions
Keep files and directories consistently named and easy to scan. Use:

- `snake_case` for Markdown or data filenames where appropriate
- short, descriptive directory names such as `src/`, `tests/`, and `docs/`
- Markdown headings in sentence case or title case, used consistently within a file

Prefer ASCII unless a file already requires Unicode. Keep formatting automated once a formatter is introduced, and record the formatter and config file in this guide.

## Testing Guidelines
No test framework is configured yet. When tests are added, keep them in `tests/` and mirror the source layout. Name test files after the unit they cover, such as `tests/test_parser.py` or `src/foo.test.ts`. Every new feature or bug fix should include a reproducible test when practical.

## Commit & Pull Request Guidelines
The current Git history uses short, plain commit messages such as `first commit`. Prefer concise, imperative commit subjects going forward, for example:

- `Add AGENTS contributor guide`
- `Create initial src and tests layout`

Pull requests should explain the change, note any setup or follow-up work, and link related issues when available. Include screenshots only for UI changes.

## Documentation Expectations
Keep `README.md` focused on project usage and setup, and use this file for contributor workflow. Update both when introducing new structure, tooling, or conventions so the repository stays self-describing.
