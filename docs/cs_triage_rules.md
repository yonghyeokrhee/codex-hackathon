# CS Triage Rules

This document is the source of truth for the `cs-collection` automation's `2-1` triage behavior.
Use it before broad interpretation of [spec.md](/Users/yong/codex-hackathon/spec.md).

## Goal

Turn each incoming CS ticket into a reviewable triage result that follows a fixed decision path:

`FAQ 가능성 확인 -> support 문서 조회 -> 부족하면 코드베이스 탐색 -> UX_GAP/DEFECT 판정 -> P1/P2 부여`

## Inputs

- Linear `Incoming` or workflow-equivalent backlog issue
- Live intake artifact or fallback sample row
- Existing automation memory and prior issue history for dedupe
- Support site: `https://support.mop.co.kr/`
- Codebases:
  - `/Users/yong/mop-fe`
  - `/Users/yong/mop-be`
- Codebase source context:
  - `/Users/yong/mop-fe/AGENTS.md`
  - `/Users/yong/mop-be/AGENTS.md`

## Required Decision Flow

1. Start with the normalized customer question, translated summary, and dedupe result.
2. Judge whether the ticket looks like a simple feature/how-to question.
3. If it may be answerable from documentation, read `https://support.mop.co.kr/` first and look for prior history.
4. If support evidence is sufficient, stop code exploration and classify the ticket as `FAQ`.
5. If the question is UI/UX-specific, asks for the actual product behavior, or suggests a bug, inspect `/Users/yong/mop-fe` and `/Users/yong/mop-be`.
   - Read the repo-specific `AGENTS.md` files first and use `/Users/yong/.codex/skills/mop-codebase-triage/SKILL.md` to structure the inspection.
6. After codebase inspection:
   - If the product behavior appears intentional but the wording, information architecture, guidance, or affordance is weak, classify as `UX_GAP`.
   - If the observed behavior appears broken, inconsistent with implementation intent, or likely to be a defect, classify as `DEFECT`.
7. After category classification, assign the second-stage scope label:
   - `P1`: bids, partner sync, external integrations, API/webhook or other integration-heavy paths
   - `P2`: insights, reports, dashboards, analytics, exports, or other reporting paths

## FAQ Rules

- `FAQ` means the product is behaving as intended and the answer can be grounded in support guidance or a stable usage explanation.
- A `FAQ` triage result must include:
  - `FAQ` label
  - `reply_draft`
  - support evidence or citation notes
  - operator-facing note describing why code exploration was not required
- If support center evidence is sufficient to answer confidently, the automation may send an `즉시 답변` to Slack channel `#cs-intake` using the prepared `reply_draft`.
- When an immediate `#cs-intake` reply is sent, still record the reply target and link in automation memory and preserve the triage evidence.
- If support access fails or the evidence is incomplete, record that failure and escalate to codebase inspection rather than guessing.

## Codebase Inspection Triggers

Inspect the codebase when any of the following are true:

- The customer asks about a specific screen, label, report, dashboard, or UI flow.
- The response requires explaining real product behavior rather than policy text.
- The customer describes missing data, delayed sync, failed actions, or suspected bugs.
- Support guidance is absent, stale, contradictory, or too generic.

## Subagent Guidance

- Support-site lookup can use lower reasoning effort.
- Codebase checks can be split across FE and BE in parallel when helpful.
- The preferred codebase-inspection skill is `/Users/yong/.codex/skills/mop-codebase-triage/SKILL.md`.
- If subagents are used, record each role clearly, for example:
  - `support-doc lookup`
  - `mop-fe behavior check`
  - `mop-be integration check`

## Output Contract

Every triage result must produce these fields:

- `category`: `FAQ` | `UX_GAP` | `DEFECT`
- `scope_label`: `P1` | `P2`
- `severity`: required for `UX_GAP` and `DEFECT`, omitted or `-` for `FAQ`
- `evidence`: structured bullet list of support findings, code references, issue history, or fallback notes
- `rationale`: short explanation of the decision path taken
- `reply_draft`: customer-facing answer draft
- `operator_note`: internal note for PM/CS/AM
- `next_action`: routing, escalation, or follow-up step
- `next_action` may be `send immediate FAQ reply to #cs-intake` when support center evidence is sufficient.

## Evidence and Rationale Format

Use concise, inspectable evidence. Prefer this structure:

- `support:` what page or article was checked, or why support lookup was insufficient
- `codebase:` which repo or file area was inspected, or why code inspection was skipped
- `history:` prior similar issues or dedupe context
- `fallback:` workflow limitations, label/state failures, or unavailable evidence

Rationale should explicitly mention the branch taken, for example:

- `FAQ because support guidance answered the resend flow and no product inconsistency was found.`
- `UX_GAP because the report filter label is implemented as designed but the wording mismatches the user's mental model.`
- `DEFECT because the integration path appears to fail or lag beyond intended behavior.`

## Fallback Rules

- If support.mop.co.kr cannot be accessed, record that as `fallback` evidence and do not fabricate support citations.
- If the codebases cannot be inspected, record the missing repo access and keep the result provisional.
- If Linear labels or workflow states cannot be applied, preserve the triage result in the issue body or comments.
- If no live intake source yields a new item, use the allowed fallback sample only after dedupe.
- If a case cannot be confidently resolved after support and codebase review, prefer an explicit operator note over an overconfident label.
- If `#cs-intake` write fails, record the failure as `fallback` evidence and continue with the normal Linear comment plus `#cs-alarm` notification path.

## Review Checklist

- Support lookup attempted before declaring `FAQ`
- Codebase lookup attempted for UI/UX-specific or bug-like tickets
- Category chosen from `FAQ`, `UX_GAP`, `DEFECT`
- Scope label chosen from `P1`, `P2`
- `evidence`, `rationale`, `reply_draft`, `operator_note`, and `next_action` present
- Fallbacks recorded when evidence or writes are unavailable
