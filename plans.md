# Execution Plan

## Milestone 0: Lock the target

### Goal

Freeze the target problem, constraints, and non-goals for the Linear priority scoring agent.

### Acceptance criteria

- `spec.md` exists and is non-empty.
- Scope, constraints, success criteria, and out-of-scope items are explicit.
- The demo path does not depend on live Linear auth.

## Milestone 1: Define the analysis contract

### Goal

Define the input and output contract for one-issue analysis.

### Acceptance criteria

- Required input fields are enumerated.
- Required output fields are enumerated.
- The scoring dimensions are explicit and stable.
- Deterministic mapping is described in docs before code is written.

## Milestone 2: Scaffold the implementation slice

### Goal

Create the minimum project structure needed to build the vertical slice.

### Acceptance criteria

- The repo has a clear location for source code, tests, and assets if they are added.
- There is one obvious entry point for running the MVP.
- The project can be verified with repeatable commands.

## Milestone 3: Ship the core scoring loop

### Goal

Implement issue normalization, structured extraction, and deterministic scoring for one issue.

### Acceptance criteria

- One sample issue can be analyzed end to end.
- The system outputs a priority band and dimension breakdown.
- The result includes evidence and missing information.
- The score is reproducible for the same normalized input.

## Milestone 4: Add the review surface

### Goal

Present the result in a way that a human can approve or reject.

### Acceptance criteria

- The result includes a rationale and confidence explanation.
- A draft comment is generated for Linear.
- The flow makes it clear that write-back is not automatic.

## Milestone 5: Verification hardening

### Goal

Make the run continuously inspectable and safe to resume.

### Acceptance criteria

- `make test`, `make lint`, `make typecheck`, and `make build` all exist.
- Verification runs locally without undocumented setup.
- The audit log shows what changed, what passed, and what remains.

## Milestone 6: Demo readiness

### Goal

Prepare a clean demo story for the hackathon.

### Acceptance criteria

- There are at least three representative issue scenarios or fixtures.
- The demo can explain why a loud request is not always high priority.
- The repository explains the MVP, known gaps, and next steps.

## Operating rules during the run

- Work one milestone at a time.
- Do not start the next milestone until the current one has explicit evidence in `documentation.md`.
- If external integration blocks progress, fall back to mocked or pasted issue data and continue.
- Prefer small, reviewable patches over broad speculative scaffolding.
