# Long-Running Job Runbook

## Purpose

This file tells the agent how to operate while developing the `Linear priority scoring agent` from the storyboard and spec.

## Before each work session

1. Read [spec.md](/Users/yong/codex-hackathon/spec.md), [plans.md](/Users/yong/codex-hackathon/plans.md), and [documentation.md](/Users/yong/codex-hackathon/documentation.md).
2. Confirm the current milestone and the next acceptance check.
3. Keep the Chrome tab `Run long horizon tasks with Codex` available as the execution reference.
4. Record the session start in `documentation.md`.

## Execution loop

1. Pick one milestone-sized task.
2. State the intended change in `documentation.md` before editing.
3. Make the smallest patch that advances the current acceptance criteria.
4. Run the verification commands:
   - `make test`
   - `make lint`
   - `make typecheck`
   - `make build`
5. Record the outcome in `documentation.md`, including failures and follow-up actions.
6. Stop after a clean checkpoint rather than mixing multiple milestones together.

## Decision rules

- Prefer a mocked or pasted Linear issue flow before live integration.
- Keep model outputs structured and deterministic wherever possible.
- Do not allow the model to emit only a raw final priority without intermediate dimensions.
- Preserve human review before any external write-back.
- If a new idea does not help the current milestone, capture it in `documentation.md` and defer it.

## Required implementation qualities

- Every user-visible claim should be traceable to issue evidence or a deterministic rule.
- Every milestone should leave the repo in a runnable, inspectable state.
- Every external dependency or setup step should be documented immediately when introduced.

## Logging requirements

Every meaningful work block should append:

- date or session marker
- milestone being worked
- intended change
- files changed
- verification results
- open risks
- next step

## Safe fallback paths

- If Linear auth is flaky, use a fixture or pasted payload.
- If UI work stalls, ship the scoring loop behind a CLI or API first.
- If model output is unstable, narrow the schema and move more logic into deterministic code.
- If the run runs out of time, stop with a documented checkpoint and explicit next action.

## Definition of done for a checkpoint

A checkpoint is valid only if:

- the current milestone is still coherent,
- the repository passes the relevant verification commands,
- `documentation.md` explains the current state,
- and the next task is obvious to a future resume.
