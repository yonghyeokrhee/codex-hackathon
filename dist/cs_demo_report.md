# CS triage demo report

Source seed: `tests/fixtures/cs_seed.json`
Tickets processed: 4

## Tickets

### seed-1 - How do I resend the onboarding email?

- Source: email
- Customer: Atlas Ads
- Received: 2026-04-20T08:30:00+09:00
- Language: ko
- Category: FAQ
- Severity: -
- Scope: P2
- Route: Customer Reply Draft
- Codex PR candidate: no
- Evidence: how do i, documented, document, defaulted-to-p2
- Rationale: FAQ phrasing matched: how do i, documented, document. No explicit bid/integration or reporting cues were found, so the ticket defaults to P2.
- Attachments: one screenshot of the inbox

### seed-2 - The report filter label is confusing

- Source: web
- Customer: Northwind
- Received: 2026-04-20T09:10:00+09:00
- Language: en
- Category: UX_GAP
- Severity: LOW
- Scope: P2
- Route: UX Review
- Codex PR candidate: yes
- Evidence: confusing, unclear, label, dashboard, report, filter
- Rationale: UX gap signals matched: confusing, unclear, label, dashboard, report, filter. P2 scope was selected because the ticket touches: report, dashboard, filter. UX area 'report-filter-label' already had 2 similar cases, so this ticket crosses the Codex PR trigger threshold.
- Attachments: none

### seed-3 - Checkout fails when I click Pay

- Source: chat
- Customer: Bluebird
- Received: 2026-04-20T09:45:00+09:00
- Language: en
- Category: DEFECT
- Severity: HIGH
- Scope: P1
- Route: Hotfix Queue
- Codex PR candidate: no
- Evidence: error, fails, 500, never completes, checkout, pay, payment
- Rationale: Defect signals matched: error, fails, 500, never completes. P1 scope was selected because the ticket touches: checkout, pay, payment.
- Attachments: screen recording

### seed-4 - Bid sync is delayed after integration

- Source: email
- Customer: Signal Labs
- Received: 2026-04-20T10:05:00+09:00
- Language: en
- Category: DEFECT
- Severity: MEDIUM
- Scope: P1
- Route: Sprint Backlog
- Codex PR candidate: no
- Evidence: delayed, lags, late, bid, bidding, integration, sync
- Rationale: Defect signals matched: delayed, lags, late. P1 scope was selected because the ticket touches: bid, bidding, integration, sync.
- Attachments: log excerpt
