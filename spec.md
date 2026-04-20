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
