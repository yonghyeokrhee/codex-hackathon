# COD-7 Keyword Monitoring Missing-Hour Mitigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Human review gate:** Do not move `COD-7` to `In Progress` until a human confirms that a UI mitigation is an acceptable first fix even if the root cause remains in the collection pipeline.

**Goal:** Surface a clear degraded-data state for keyword rank monitoring when hourly monitoring rows are missing, instead of silently rendering blanks or zero-like dashboard output.

**Architecture:** Start with a front-end mitigation in `mop-fe` because the current issue evidence shows the UI hides missing monitoring hours even when the backend returns partial data. Keep backend work optional and gated: only add a BE summary field if the existing table and dashboard payloads are not sufficient to detect missing-hour windows safely on the client.

**Tech Stack:** React 17, TypeScript, Material-UI 4, Jest/React Testing Library in `mop-fe`; optional Spring Boot/MyBatis follow-up in `mop-be`.

---

## File Map

- Modify: `/Users/yong/mop-fe/src/components/rankMaintenance/KeywordRankMonitoringTable.tsx`
- Modify: `/Users/yong/mop-fe/src/components/dashboard/detail/flight/SaMaintenance.tsx`
- Modify: `/Users/yong/mop-fe/src/models/rankMaintenance/KeywordRankMonitoring.ts`
- Create: `/Users/yong/mop-fe/src/components/rankMaintenance/KeywordRankMonitoringTable.spec.tsx`
- Create: `/Users/yong/mop-fe/src/components/dashboard/detail/flight/SaMaintenance.spec.tsx`
- Create: `/Users/yong/mop-fe/src/utils/rankMonitoring/missingHours.ts`
- Create: `/Users/yong/mop-fe/src/utils/rankMonitoring/missingHours.spec.ts`
- Optional modify: `/Users/yong/mop-be/src/main/java/com/mop/be/service/RankMaintenanceServiceImpl.java`
- Optional modify: `/Users/yong/mop-be/src/main/resources/sql/RankMaintenance.xml`

### Task 1: Lock The UI Detection Contract

**Files:**
- Create: `/Users/yong/mop-fe/src/utils/rankMonitoring/missingHours.ts`
- Test: `/Users/yong/mop-fe/src/utils/rankMonitoring/missingHours.spec.ts`
- Reference: `/Users/yong/mop-fe/src/models/rankMaintenance/KeywordRankMonitoring.ts`

- [ ] **Step 1: Write the failing utility tests**

```ts
import { summarizeMissingMonitoringHours } from './missingHours';

describe('summarizeMissingMonitoringHours', () => {
  it('flags a consecutive 3-hour gap as degraded monitoring', () => {
    const summary = summarizeMissingMonitoringHours([
      { date: '2026.04.21', ranks: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, null, null, null, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] },
    ]);

    expect(summary.maxConsecutiveMissingHours).toBe(3);
    expect(summary.hasActionableGap).toBe(true);
  });
});
```

- [ ] **Step 2: Run the utility test to verify it fails**

Run: `cd /Users/yong/mop-fe && CI=true yarn test:unit --runInBand --runTestsByPath src/utils/rankMonitoring/missingHours.spec.ts`

Expected: FAIL with `Cannot find module './missingHours'` or missing export errors.

- [ ] **Step 3: Write the minimal gap-summary helper**

```ts
export interface MissingHoursSummary {
  hasActionableGap: boolean;
  maxConsecutiveMissingHours: number;
  affectedDates: string[];
}
```

Implement the helper so that:
- `null` ranks count as missing hourly data
- isolated single gaps are informational only
- consecutive gaps of `>= 3` hours set `hasActionableGap` to `true`

- [ ] **Step 4: Run the utility test to verify it passes**

Run: `cd /Users/yong/mop-fe && CI=true yarn test:unit --runInBand --runTestsByPath src/utils/rankMonitoring/missingHours.spec.ts`

Expected: PASS

- [ ] **Step 5: Commit the utility contract**

```bash
cd /Users/yong/mop-fe
git add src/utils/rankMonitoring/missingHours.ts src/utils/rankMonitoring/missingHours.spec.ts
git commit -m "feat: detect missing keyword monitoring hours"
```

### Task 2: Expose Missing-Hour State In The Table View

**Files:**
- Modify: `/Users/yong/mop-fe/src/components/rankMaintenance/KeywordRankMonitoringTable.tsx`
- Test: `/Users/yong/mop-fe/src/components/rankMaintenance/KeywordRankMonitoringTable.spec.tsx`
- Reference: `/Users/yong/mop-fe/src/api/rankMaintenance/KeywordRankMonitoring.spec.ts`

- [ ] **Step 1: Write the failing component test**

```tsx
it('shows a degraded-data notice when the table response has a 3-hour gap', async () => {
  mockGetTableTypeKeywordRankMonitorings.mockResolvedValue([
    { date: '2026.04.21', ranks: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, null, null, null, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], targetRanks: Array(24).fill(1) },
  ]);

  render(<KeywordRankMonitoringTable keywordMonitoringId={1} startDate="20260421" endDate="20260421" />);

  expect(await screen.findByText(/missing monitoring data/i)).toBeInTheDocument();
});
```

- [ ] **Step 2: Run the table test to verify it fails**

Run: `cd /Users/yong/mop-fe && CI=true yarn test:unit --runInBand --runTestsByPath src/components/rankMaintenance/KeywordRankMonitoringTable.spec.tsx`

Expected: FAIL because no degraded-data notice is rendered.

- [ ] **Step 3: Implement the minimal table warning**

Add a small warning block above the table that:
- appears only when `summarizeMissingMonitoringHours(tableData).hasActionableGap` is `true`
- includes the maximum consecutive missing hours
- avoids changing the raw table cell rendering, so existing operators can still inspect partial rows

- [ ] **Step 4: Run the targeted tests**

Run: `cd /Users/yong/mop-fe && CI=true yarn test:unit --runInBand --runTestsByPath src/utils/rankMonitoring/missingHours.spec.ts src/components/rankMaintenance/KeywordRankMonitoringTable.spec.tsx src/api/rankMaintenance/KeywordRankMonitoring.spec.ts`

Expected: PASS

- [ ] **Step 5: Commit the table mitigation**

```bash
cd /Users/yong/mop-fe
git add src/components/rankMaintenance/KeywordRankMonitoringTable.tsx src/components/rankMaintenance/KeywordRankMonitoringTable.spec.tsx src/utils/rankMonitoring/missingHours.ts src/utils/rankMonitoring/missingHours.spec.ts
git commit -m "feat: warn when keyword monitoring hours are missing"
```

### Task 3: Stop The Dashboard From Hiding Collection Gaps

**Files:**
- Modify: `/Users/yong/mop-fe/src/components/dashboard/detail/flight/SaMaintenance.tsx`
- Test: `/Users/yong/mop-fe/src/components/dashboard/detail/flight/SaMaintenance.spec.tsx`

- [ ] **Step 1: Write the failing dashboard test**

```tsx
it('shows a monitoring gap note when recent dashboard values are missing or zeroed for 3+ hours', () => {
  render(<SaMaintenance maintenance={maintenanceWithGap} />);

  expect(screen.getByText(/monitoring data may be delayed/i)).toBeInTheDocument();
});
```

- [ ] **Step 2: Run the dashboard test to verify it fails**

Run: `cd /Users/yong/mop-fe && CI=true yarn test:unit --runInBand --runTestsByPath src/components/dashboard/detail/flight/SaMaintenance.spec.tsx`

Expected: FAIL because no gap note exists.

- [ ] **Step 3: Implement the minimal dashboard note**

Show a compact note below the realtime chart when the most recent window contains a repeated run of missing or zero-only monitoring values that lines up with the issue symptom.

- [ ] **Step 4: Run the targeted dashboard tests**

Run: `cd /Users/yong/mop-fe && CI=true yarn test:unit --runInBand --runTestsByPath src/components/dashboard/detail/flight/SaMaintenance.spec.tsx`

Expected: PASS

- [ ] **Step 5: Commit the dashboard mitigation**

```bash
cd /Users/yong/mop-fe
git add src/components/dashboard/detail/flight/SaMaintenance.tsx src/components/dashboard/detail/flight/SaMaintenance.spec.tsx
git commit -m "feat: surface keyword monitoring gaps on dashboard"
```

### Task 4: Human-Gated Backend Follow-Up

**Files:**
- Optional modify: `/Users/yong/mop-be/src/main/java/com/mop/be/service/RankMaintenanceServiceImpl.java`
- Optional modify: `/Users/yong/mop-be/src/main/resources/sql/RankMaintenance.xml`

- [ ] **Step 1: Confirm whether FE-only detection is sufficient**

Run: inspect the live payload captured in `COD-7` artifacts and compare it with the UI expectations.

Expected: Human confirmation that the FE can distinguish true missing-hour gaps from intentionally absent data.

- [ ] **Step 2: Only if FE cannot decide safely, write the failing BE contract test or fixture**

Target: add a response flag or summary such as `missingMonitoringHours` or `hasMonitoringGap`.

- [ ] **Step 3: Implement the minimal BE summary field**

Keep the SQL row set intact; compute the summary in service code so existing consumers do not lose compatibility.

- [ ] **Step 4: Run relevant BE tests**

Run: `cd /Users/yong/mop-be && ./gradlew test --tests '*RankMaintenance*'`

Expected: PASS

- [ ] **Step 5: Commit the BE follow-up**

```bash
cd /Users/yong/mop-be
git add src/main/java/com/mop/be/service/RankMaintenanceServiceImpl.java src/main/resources/sql/RankMaintenance.xml
git commit -m "feat: summarize missing keyword monitoring hours"
```

## Execution Notes

- Current automation confidence is **not high enough** to auto-execute this plan end-to-end because:
  - `COD-7` is a `DEFECT`, not a repeated `UX_GAP`, so the intended auto-dev scope is ambiguous.
  - `/Users/yong/mop-fe` and `/Users/yong/mop-be` both have pre-existing local changes.
  - The root cause may still be an upstream collection outage rather than a UI-only defect.
- If a human approves UI mitigation as the first slice, start with **Task 1 -> Task 3** in `mop-fe` and keep `COD-7` in `Backlog` until ownership is explicit.
