# Linear priority scoring agent briefing

Generated from repository planning artifacts.

## spec.md

# Linear Priority Scoring Agent Spec

## Objective

Build a hackathon-ready `Linear priority scoring agent` that turns one Linear issue into a reviewable priority recommendation with evidence, uncertainty, and next actions. The agent should help a team distinguish noisy requests from genuinely urgent work.

## Working premise

The long-running job should treat the local storyboard at `/Users/yong/Downloads/priority-copilot-storyboard.html` as the product narrative source and keep the Chrome reference tab `Run long horizon tasks with Codex` available as the operator playbook for how Codex should execute multi-step work.

## Primary user story

Given a single Linear issue with title, description, labels, and comments, the system should:

1. Normalize the issue into structured input.
2. Extract scoring dimensions from messy stakeholder and engineering context.
3. Compute a deterministic priority result.
4. Explain the reasoning with evidence and confidence.
5. Suggest safe next actions, including a draft comment for Linear.

## In scope

- One-issue analysis flow for Linear
- Manual paste or mocked Linear payload as a valid first milestone
- Structured dimensions:
  - business impact
  - urgency
  - stakeholder pressure
  - delivery risk or technical complexity
  - confidence
- Deterministic score mapping into priority bands such as `P0` to `P3`
- Reviewable outputs:
  - priority band
  - numeric score
  - rationale
  - evidence list
  - missing information
  - suggested next actions
  - draft Linear comment
- Inspectable delivery artifacts and a persistent audit trail

## Out of scope for the first long-running build

- Backlog-wide autonomous reprioritization
- Mandatory live OAuth integration as a blocker for demo progress
- Fully autonomous writes to Linear without human approval
- Historical issue similarity systems
- Deep code graph complexity analysis
- Multi-team workflow automation beyond a single issue loop

## Constraints

- The run must remain inspectable through markdown artifacts in this repository.
- Every milestone must have acceptance criteria before implementation starts.
- External integration risk must not block the demo path; mocked or pasted issue data is acceptable first.
- Any write-back action to Linear should be proposed first and only executed after explicit human approval.
- Verification must run continuously via `test`, `lint`, `typecheck`, and `build` commands.
- The implementation should favor a small, demoable vertical slice over broad architecture.

## Product shape

## Input

- Linear issue identifier or pasted issue payload
- Title
- Description
- Labels
- Comments
- Optional business context
- Optional engineering notes

## Processing

- Parse and normalize issue fields
- Ask a model for structured extraction, not only free-form prose
- Validate the structured output
- Compute a deterministic score from extracted fields
- Generate reviewable output artifacts

## Output

- Priority band
- Numeric score with dimension breakdown
- Explanation and confidence
- Evidence cited from issue content
- Missing information and follow-up questions
- Draft comment suitable for posting back to Linear

## Suggested architecture

- Frontend: lightweight issue input and result review UI
- Backend: issue normalization, model invocation, deterministic scorer, action proposal layer
- Adapters: Linear reader and optional write-back interface
- Storage: local file logs or lightweight persistence for score history if needed
- Verification: scripted checks that keep the run honest

## Success criteria

- A user can analyze one Linear issue end to end.
- The result clearly separates evidence from opinion.
- The final priority is computed deterministically from structured dimensions.
- The system exposes uncertainty instead of pretending certainty.
- The demo can run without live Linear connectivity.
- All progress is traceable through repository docs and verification output.

## Deliverables for this repository

- [spec.md](/Users/yong/codex-hackathon/spec.md)
- [plans.md](/Users/yong/codex-hackathon/plans.md)
- [implement.md](/Users/yong/codex-hackathon/implement.md)
- [documentation.md](/Users/yong/codex-hackathon/documentation.md)
- verification commands and scripts

## Exit condition for the long-running job

The long-running job is complete when the repository contains a working, verifiable MVP or a clearly documented stopping point with completed milestones, open gaps, and the next recommended action.

## plans.md

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

## implement.md

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

## documentation.md

# Live Status and Audit Log

## Mission

Build a hackathon-ready `Linear priority scoring agent` with an inspectable long-running workflow, using the storyboard at `/Users/yong/Downloads/priority-copilot-storyboard.html` as the narrative source.

## Current status

- State: planning scaffold created
- Current milestone: `Milestone 0: Lock the target`
- Working mode: docs-first, demo-safe, inspectable
- Reference browser tab: `Run long horizon tasks with Codex`

## Session log

### 2026-04-20 - Session 1

#### Intent

Create the operating documents and continuous verification scaffold required before the long-running build starts.

#### Changes

- Added `spec.md` with target, scope, constraints, and success criteria.
- Filled `plans.md` with milestone checkpoints and acceptance criteria.
- Filled `implement.md` with the runbook for agent operation.
- Initialized `documentation.md` as the live audit log.
- Added a lightweight verification toolchain and `make` targets.

#### Verification

- Pending until the new verification scripts are written and executed in this session.

#### Risks

- Product direction is clear, but no application code exists yet.
- Live Linear integration remains intentionally deferred to avoid blocking the MVP path.

#### Next step

Finish the verification scaffold, run it, and capture the baseline result.
