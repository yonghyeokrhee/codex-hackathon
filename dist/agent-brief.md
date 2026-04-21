# CS 수집 및 트리아지 워크플로우 브리핑

저장소 계획 산출물에서 생성됨.

## spec.md

# CS 수집 및 트리아지 서비스 명세

## 개요

본 프로젝트는 단일 앱 화면을 만드는 작업이 아니라, 여러 입력 채널에서 고객 문의를 수집하고 이를 Linear 중심으로 정리, 분류, 후속 처리하는 `CS 수집 및 트리아지 워크플로우 서비스`를 구현하는 것을 목표로 한다.

이 서비스는 다음 세 가지 축을 중심으로 동작한다.

- 입력 수집: `Computer Use`를 활용해 여러 운영 채널에서 신규 CS를 가져온다.
- 시스템 오브 레코드: 수집된 모든 티켓은 `Linear` 이슈로 정규화되어 관리된다.
- 후속 알림: 트리아지 및 라우팅 결과는 `Slack`으로 우선 알림하며, 필요 시 이후 `Discord` 확장 가능성을 열어둔다.

## 문제 정의

현재 고객 문의는 개인 이메일, 대표 이메일, 상담 채널, 웹 문의 등 여러 경로로 분산 유입된다. 이 정보는 사람 손으로 엑셀이나 메시지로 옮겨 적고 있으며, 그 과정에서 다음 문제가 반복된다.

- 신규 문의 등록이 늦다.
- 누락과 중복이 발생한다.
- 입력 포맷이 일정하지 않아 후속 처리가 어렵다.
- PM이 티켓을 하나씩 읽고 직접 분류해야 하므로 운영 비용이 크다.
- FAQ 수준 문의와 실제 결함 이슈가 같은 큐에 섞여 우선순위 판단이 흔들린다.
- 반복되는 UX 문의가 쌓여도 제품 개선으로 연결되지 못한다.

본 서비스는 이 수작업 흐름을 `수집 -> 정규화 -> Linear 등록 -> 자동 triage -> 후속 응답/라우팅 -> 반복 UX 개선 트리거`의 형태로 재구성한다.

## 목표 사용자

- HQ Product Manager
  - 아침에 Linear를 열었을 때 밤사이 들어온 티켓이 이미 정리되어 있기를 원한다.
  - 티켓의 카테고리, 심각도, 우선순위 근거를 빠르게 확인하고 싶다.
- AM / CS 운영 담당자
  - 내가 등록한 티켓이 어떻게 처리되었는지 즉시 알고 싶다.
  - FAQ나 UX 안내 수준의 문의는 바로 고객에게 전달 가능한 초안을 받고 싶다.
- 리뷰 담당자
  - 반복되는 UX_GAP이 일정 임계치를 넘으면 Codex가 제안한 수정 PR만 검토하고 싶다.

## 서비스 목표

- 멀티소스 CS를 일관된 구조로 수집한다.
- 모든 입력을 Linear 이슈로 표준화하여 운영 기준점을 하나로 맞춘다.
- 티켓을 자동으로 분류하고, 근거와 함께 우선 처리 방향을 제안한다.
- 분류 결과에 따라 답변 초안, 큐 라우팅, 알림 발송까지 후속 처리를 자동화한다.
- 반복되는 UX_GAP을 단순 분류로 끝내지 않고 실제 제품 개선 PR까지 연결한다.
- 해커톤 데모에서는 전체 워크플로우가 끝까지 이어지는 모습을 재현 가능해야 한다.

## 운영 원칙

- 본 프로젝트의 핵심 산출물은 UI보다 `inspectable workflow`이다.
- 사람이 승인해야 하는 단계와 자동으로 흘러가도 되는 단계를 분리한다.
- Linear는 티켓 상태와 후속 처리를 추적하는 중심 시스템으로 사용한다.
- 외부 연동이 불안정해도 데모는 멈추지 않아야 하므로 mock, seed, pasted input 경로를 반드시 확보한다.
- 모든 자동 판단은 가능한 한 근거와 함께 남겨야 한다.

## 전체 워크플로우

### 1. 멀티소스 CS 수집

- 스케줄 기반 워크플로우가 하루 3회 실행된다.
- `Computer Use`가 입력 채널에 접근해 신규 문의를 수집한다.
- 입력 채널 예시는 다음과 같다.
  - AM 개인 이메일
  - 제품 대표 이메일
  - 상담 채널
  - 홈페이지 도입 문의
- 신규 문의는 공통 포맷으로 정규화된다. 이 것은 skeleton으로 볼 수 있다.
- 수집 후에는 cs_log.markdown 에 수집된 내용을 간단하게 markdown 형식으로 기록한다. 만약 json이 더 적절한 경우라면 json으로 기록한다.
- 초기 상태는 Linear에 등록해도 된다. 하지만 검토 해보고, Triage를 미리 거쳐서 올리는게 좋다면 그렇게 해도 돼.

### 2. Triage

- `Incoming` 상태의 Linear 이슈를 가져온다.
- 필요 시 비영어 티켓을 영어로 번역한다.
- 에이전트가 카테고리와 심각도를 판단한다.
- 판단 근거를 구조화된 형태로 남긴다.
- Linear 라벨, priority, 상태를 갱신하여 `Triaged` 단계로 이동시킨다.
- Triage는 다음 단계를 거치게 되고 이것은 매우 중요한 단계이다.

#### 2-1 Triage Rule

- 먼저 Triage는 다음 단계를 거친다.
- 판단 결과 단순히 기능에 대한 질문인 경우는 CS 문서를 읽는 skill을 사용해서 답변해준다. 과거 이력을 참고 할 수 있다. 이 때 Label에는 "FAQ"라고 주자.
- 하지만 고객의 질문이 구체적인 UI/UX에 대한 질문인 경우 CS 문서에 없기 때문에 Codebase를 확인해야 한다.
- Codebase는 ~/mop-be 와 ~/mop-fe에 있다.
- Codebase를 이해할 수 있는 skill이 있다면 좋다.
- 결과적으로 Triage를 수행할 때 subagent를 사용하게 된다면 더 빠른 작업이 가능하다. CS문서를 읽는 skill은 낮은 상대적으로 Reasoning Effort를 줘도 된다.
- Codebase 확인 후 UI/UX에 대한 상세 설명을 줄 수 있다면 "UX_GAP"이라고 Label 주자.
- Codebase 확인 후 bug로 의심되는 경우라면 "DEFECT"라는 Label 붙이자.
- 2단계 Label이 있는데, P1/P2로 분류한다.
- 2단계 P1은 입찰과 연동에 관련된 이슈로 보인다. P2는 인사이트나 리포트에 관한 이슈로 본다.


### 3. 후속 처리

- 카테고리에 따라 후속 액션이 달라진다.
- FAQ는 기존 FAQ 또는 문서를 바탕으로 답변 초안을 생성한다.
- DEFECT는 severity에 따라 적절한 큐로 라우팅한다.
- UX_GAP은 설명 가능한 답변 초안을 만들고, 동일 영역 누적 건수를 체크한다.
- 모든 결과는 Slack으로 운영 알림을 보낸다.

### 4. 반복 UX 이슈의 자동 개선

- 동일 UX_GAP이 일정 횟수 이상 반복되면 Codex가 제품 개선 작업을 시도한다.
- 대상 컴포넌트를 찾고, 툴팁 또는 가이드 코드를 작성한다.
- 필요한 테스트를 함께 생성한다.
- 브랜치, 커밋, PR 생성까지 자동화한다.
- 생성된 PR 링크를 관련 Linear 이슈에 연결한다.

## 기능 범위

## F1. 멀티소스 CS 수집

### 목적

여러 채널로 흩어진 CS를 사람 손을 거치지 않고 한곳으로 모으는 것이다.

### 입력

- 이메일 계정 화면
- 상담 채널 화면
- 웹 문의 관리 화면
- 기타 운영자가 사용하는 CS 확인 화면

### 처리

- `Computer Use`가 각 채널 UI를 순회하며 신규 항목을 읽는다.
- 신규 여부를 식별한다.
- 다음과 같은 표준 필드를 추출한다.
  - source
  - received_at
  - language
  - customer_name 또는 customer_org
  - AM owner
  - title
  - raw_content
  - attachments summary
- 필드 정규화 후 Linear 이슈를 생성한다.

### 출력

- `Incoming` 상태의 Linear 이슈
- 정규화된 티켓 데이터
- 수집 로그

### 해커톤 범위

- 실제 모든 채널 API 연동은 필수가 아니다.
- 데모에서는 시드 스크립트 또는 샘플 데이터로 4개 내외의 티켓을 주입해도 된다.
- 내레이션에서는 멀티소스 수집이 가능한 구조임을 설명한다.

## F2. 자동 Triage

### 목적

PM이 직접 읽고 판단하던 초기 분류 작업을 자동화하는 것이다.

### 카테고리 체계

- `FAQ`
  - 문서, 가이드, 운영 안내로 해결 가능
  - 제품은 정상 작동
- `UX_GAP`
  - 제품은 동작하지만 사용자가 구조나 표현 때문에 헷갈림
  - 설명, 라벨, 툴팁, 가이드 부족 문제
- `DEFECT`
  - 제품이 의도대로 동작하지 않음
  - 코드 수정 또는 기능 수정이 필요한 결함

### Severity 체계

Severity는 `DEFECT`와 `UX_GAP`에만 적용한다.

- `HIGH`
  - 데이터 손실
  - 매출 영향
  - 핵심 기능 차단
- `MEDIUM`
  - 일부 기능 문제
  - 우회 가능
- `LOW`
  - 경미한 불편
  - 외관 이슈
  - 엣지 케이스

### 처리

- `Incoming` 상태의 Linear 이슈를 읽는다.
- 다국어 티켓은 영어로 번역한다.
- 단일 모델 호출에서 다음을 함께 수행할 수 있다.
  - 번역
  - 카테고리 분류
  - severity 판단
  - 판단 근거 생성
- 결과를 구조화해 Linear 필드와 라벨에 반영한다.
- 상태를 `Triaged`로 변경한다.

### 출력

- category
- severity
- rationale
- evidence
- translated summary
- updated Linear labels
- updated Linear priority

## F3. 후속 응답 및 라우팅

### 목적

트리아지 결과를 실제 운영 액션으로 이어지게 만드는 것이다.

### FAQ 처리

- FAQ 데이터셋에서 유사 항목을 찾는다.
- AM이 고객에게 바로 전달 가능한 답변 초안을 생성한다.
- 초안은 Linear 코멘트에 저장한다.
- 이슈 상태를 `Done`으로 이동할 수 있다.

### DEFECT 처리

- severity에 따라 큐를 나눈다.
- `HIGH` -> `Hotfix Queue`
- `MEDIUM` -> `Sprint Backlog`
- `LOW` -> `Backlog`
- 관련 라우팅 결과를 Linear에 반영한다.
- 운영자와 PM에게 알림을 보낸다.

### UX_GAP 처리

- 설명 가능한 답변 초안을 생성한다.
- 동일 UX 영역의 누적 건수를 확인한다.
- 누적 건수가 임계치를 넘으면 F4를 트리거한다.

### 공통 출력

- Linear 코멘트
- 상태 변경
- 라벨 또는 큐 이동 결과
- Slack 알림 메시지

### 알림 정책

- 기본 알림 채널은 `Slack`이다.
- 메시지 유형 예시:
  - 신규 triage 완료
  - HIGH severity defect 감지
  - FAQ 답변 초안 준비 완료
  - UX_GAP 반복 감지 및 Codex 작업 시작
- 추후 확장 시 Discord를 대체 또는 병행 채널로 붙일 수 있다.

### 해커톤 범위

- FAQ 데이터는 JSON 파일에 소규모 하드코딩으로 시작한다.
- 알림은 Slack webhook 기반으로 구현한다.
- Slack 연동이 막히면 Linear comment를 fallback notification으로 사용할 수 있다.
- 누적 카운팅은 JSON 또는 로컬 스토리지 기반 메모리로 처리해도 된다.

## F4. Codex 자동 PR 생성

### 목적

반복되는 UX_GAP을 사람의 백로그 판단에만 맡기지 않고, 작은 제품 개선은 즉시 코드 제안까지 연결하는 것이다.

### 트리거 조건

- 동일한 UX 영역에서 `3건 이상`의 누적 문의가 감지될 때

### 처리

- 대상 제품 저장소에서 관련 컴포넌트 파일을 식별한다.
- Codex가 현재 코드를 읽고 적절한 안내 UI를 제안한다.
  - 예: tooltip
  - helper text
  - empty-state guidance
  - inline hint
- 변경 코드와 함께 테스트를 생성한다.
- 브랜치를 만들고 커밋 후 PR을 연다.
- PR 링크를 관련 Linear 이슈에 기록한다.

### 실패 처리

- 자동 수정이 실패하거나 자신감이 낮으면 강제로 머지하지 않는다.
- 상태를 `Auto-fix attempted but needs human review`와 같은 검토 대기 상태로 남긴다.
- 실패 원인과 수동 후속 조치를 기록한다.

### 해커톤 범위

- 대상 repo는 사전 준비된 샘플 앱 또는 대시보드로 한정해도 된다.
- 데모에서는 한 개의 대표 UX_GAP 시나리오만 라이브로 시연해도 충분하다.
- Git 작업은 로컬 clone 없이 API 중심 자동화로 대체 가능하다.

## 시스템 구성 요소

- `Computer Use collector`
  - 입력 채널 화면에서 데이터를 수집한다.
- `Normalization layer`
  - 다양한 입력을 공통 티켓 포맷으로 변환한다.
- `Linear adapter`
  - 이슈 생성, 상태 변경, 라벨 변경, 코멘트 작성 담당
- `Triage engine`
  - 번역, 분류, severity 판단, 근거 생성을 담당
- `Response and routing engine`
  - FAQ 초안, 큐 배정, 알림 발송, 누적 카운팅 담당
- `Notification adapter`
  - Slack 우선 알림 채널
- `Codex PR worker`
  - 반복 UX_GAP의 코드 수정 제안과 PR 생성을 담당
- `Audit and logs`
  - 워크플로우 이력과 실패 지점을 기록

## 입력 계약

서비스는 최종적으로 아래 정보를 처리할 수 있어야 한다.

- source channel
- received timestamp
- original language
- customer identity
- account owner
- inquiry title
- inquiry body
- attachments or referenced screenshots
- conversation context if available

해커톤 단계에서는 위 필드 일부가 누락되어도 동작 가능해야 하며, 누락 필드는 `unknown` 또는 명시적 빈값으로 처리한다.

## 출력 계약

각 티켓 처리 결과는 최소한 다음 정보를 남겨야 한다.

- normalized ticket
- Linear issue id
- category
- severity if applicable
- rationale
- evidence
- follow-up action
- notification result
- workflow status
- failure reason if any

## 상태 모델

- `Incoming`
  - 아직 triage 전
- `Triaged`
  - 분류와 severity 판단 완료
- `Done`
  - FAQ 또는 안내 응답까지 완료
- `Hotfix Queue`
  - 즉시 대응 필요한 결함
- `Sprint Backlog`
  - 계획 반영 대상
- `Backlog`
  - 낮은 우선순위 대기
- `Auto-fix attempted but needs human review`
  - Codex 자동 수정은 시도했으나 사람 검토가 필요함

## 의사결정 규칙

- FAQ, UX_GAP, DEFECT는 상호배타적으로 분류한다.
- severity는 모든 티켓에 강제로 붙이지 않는다.
- 근거 없는 HIGH 판정은 허용하지 않는다.
- 사람 승인 없는 외부 write-back은 제한한다.
- Codex가 생성한 PR은 자동 merge하지 않는다.
- 알림 실패가 워크플로우 전체 실패를 의미하지는 않는다.
- 외부 연동 실패 시 다음 fallback이 필요하다.
  - 수집 실패 시 seed ticket 또는 pasted input
  - Slack 실패 시 Linear comment
  - Git 자동화 실패 시 human review 대기 상태

## 외부 연동 범위

### 우선 연동

- `Computer Use`
- `Linear`
- `Slack webhook`

### 후속 확장 가능

- Discord notification
- 실제 이메일 API 연동
- 상담 채널 API 연동
- 홈페이지 문의 백엔드 직접 연동
- GitHub 또는 기타 코드 호스팅 플랫폼 연동 고도화

## 해커톤 범위

- 한 번의 데모에서 전체 워크플로우를 보여줄 수 있어야 한다.
- 샘플 티켓 세트로 수집부터 triage, 응답, 라우팅까지 재현 가능해야 한다.
- 최소 1건의 FAQ, 1건의 DEFECT, 1건의 UX_GAP 시나리오가 필요하다.
- UX_GAP 누적 3건 트리거를 위해 사전 시드 데이터를 둘 수 있다.
- Slack 알림은 실제 webhook 또는 데모용 대체 경로 중 하나로 보여주면 된다.
- Code PR 자동화는 대표 시나리오 1건만 끝까지 보여주면 충분하다.

## 비범위

- 모든 입력 채널의 실서비스 API 완전 연동
- 완전 무인 운영
- 모든 카테고리에 대한 복잡한 ML 학습 파이프라인
- 대규모 백로그 전체 자동 재우선순위화
- 자동 merge 및 자동 배포
- 완전한 운영용 보안/권한 체계 구현

## 제약 조건

- 데모가 외부 인증 문제로 멈추지 않아야 한다.
- 진행 상태는 저장소 내 문서와 로그로 추적 가능해야 한다.
- 판단 결과는 가능한 한 구조화된 형태로 남겨야 한다.
- 워크플로우 각 단계는 재시도 또는 수동 개입이 가능해야 한다.
- 실제 운영 환경으로 확장 가능한 구조를 가져야 하지만, 해커톤 구현은 작은 수직 슬라이스를 우선한다.

## 성공 기준

- 여러 입력 채널의 문의가 하나의 Linear 흐름으로 합쳐진다.
- 신규 티켓이 `Incoming`으로 자동 생성된다.
- triage 결과가 category, severity, 근거와 함께 남는다.
- 후속 처리 결과가 Linear와 Slack에 반영된다.
- FAQ, DEFECT, UX_GAP이 서로 다른 방식으로 처리되는 것이 분명히 보인다.
- 반복되는 UX_GAP이 Codex PR 생성 워크플로우로 연결된다.
- 외부 연동 일부가 막혀도 seed/mock 경로로 데모를 계속 진행할 수 있다.

## 저장소 기준 산출물

- [spec.md](/Users/yong/codex-hackathon/spec.md)
- [plans.md](/Users/yong/codex-hackathon/plans.md)
- [implement.md](/Users/yong/codex-hackathon/implement.md)
- [documentation.md](/Users/yong/codex-hackathon/documentation.md)

## 종료 조건

본 워크플로우 구현은 다음 중 하나를 만족하면 체크포인트 완료로 본다.

- 샘플 티켓 기준으로 수집, triage, 후속 처리, 알림, PR 트리거까지 이어지는 MVP가 동작한다.
- 또는 외부 연동 제약으로 일부 단계가 mock 처리되더라도, 현재 완료 범위, 남은 공백, 다음 액션이 문서에 명확히 기록되어 있다.

## plans.md

# Execution Plan

## Milestone 0: Lock the target

### Goal

Freeze the target problem, constraints, and non-goals for the CS collection and triage workflow.

### Acceptance criteria

- `spec.md` exists and is non-empty.
- Scope, constraints, success criteria, and out-of-scope items are explicit.
- The demo path does not depend on live CS or Linear auth.

## Milestone 1: Define the analysis contract

### Goal

Define the input and output contract for one-ticket collection and triage.

### Acceptance criteria

- Required input fields are enumerated.
- Required output fields are enumerated.
- The collection, triage, and routing fields are explicit and stable.
- Deterministic mapping is described in docs before code is written.

## Milestone 2: Scaffold the implementation slice

### Goal

Create the minimum project structure needed to build the temporary vertical slice.

### Acceptance criteria

- The repo has a clear location for source code, tests, and assets if they are added.
- There is one obvious entry point for running the temporary MVP slice.
- The project can be verified with repeatable commands.

## Milestone 3: Ship the core scoring loop

### Goal

Implement issue normalization, structured extraction, and deterministic triage for one issue.

### Acceptance criteria

- One sample issue can be analyzed end to end.
- The system outputs a category, severity, and rationale breakdown.
- The result includes evidence and missing information.
- The decision is reproducible for the same normalized input.

## Milestone 4: Add the review surface

### Goal

Present the result in a way that a human can approve or reject.

### Acceptance criteria

- The result includes a rationale and confidence explanation.
- A draft comment is generated for Linear or the documented fallback surface.
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
- The demo can clearly show how FAQ, UX_GAP, and DEFECT tickets diverge after triage.
- The repository explains the MVP, known gaps, and next steps.

## Operating rules during the run

- Work one milestone at a time.
- Do not start the next milestone until the current one has explicit evidence in `documentation.md`.
- If external integration blocks progress, fall back to mocked or pasted issue data and continue.
- Prefer small, reviewable patches over broad speculative scaffolding.

## implement.md

# Long-Running Job Runbook

## Purpose

This file tells the agent how to operate while developing the `CS collection and triage workflow` from the current repository spec and checkpoints.

## Before each work session

1. Read [spec.md](/Users/yong/codex-hackathon/spec.md), [plans.md](/Users/yong/codex-hackathon/plans.md), and [documentation.md](/Users/yong/codex-hackathon/documentation.md).
2. Confirm the current milestone and the next acceptance check.
3. Record the session start in `documentation.md`.

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

- Prefer a mocked or pasted CS ticket flow before live integration.
- Keep model outputs structured and deterministic wherever possible.
- Do not allow the model to emit only a raw final decision without intermediate rationale.
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

Build a hackathon-ready `CS collection and triage workflow` with an inspectable, demo-safe workflow that stays aligned with `spec.md`.

## Current status

- State: planning scaffold created
- Current milestone: `Milestone 0: Lock the target`
- Working mode: docs-first, demo-safe, inspectable

## Session log

### 2026-04-21 - Session 3

#### Intent

Ship a temporary runnable slice that proves the new CS collection and triage workflow with seeded tickets and deterministic triage logic.

#### Changes

- Added a stdlib-only pipeline under [src/cs_pipeline.py](/Users/yong/codex-hackathon/src/cs_pipeline.py) for ticket normalization, deterministic classification, scope labeling, routing, and mock Codex PR trigger detection for repeated UX_GAP tickets.
- Added a demo entry point at [src/cs_demo.py](/Users/yong/codex-hackathon/src/cs_demo.py) that reads seeded tickets and writes a markdown report.
- Added seed data at [tests/fixtures/cs_seed.json](/Users/yong/codex-hackathon/tests/fixtures/cs_seed.json) covering FAQ, UX_GAP, HIGH severity DEFECT, and P1 defect routing.
- Added unit coverage at [tests/test_cs_pipeline.py](/Users/yong/codex-hackathon/tests/test_cs_pipeline.py) for normalization, deterministic routing, and report generation.
- Updated repo verification and bundle generation so the temporary CS workflow slice is reflected in the docs and output artifacts.

#### Verification

- `python -m unittest discover -s tests -p 'test_*.py'`: passed

#### Risks

- The temporary slice is mock-backed and does not perform live Computer Use, Linear writes, or Slack delivery yet.
- Dedupe rules and final Linear field mapping remain underspecified in `spec.md`, so the implementation uses local deterministic assumptions only.

#### Next step

Run the full `make verify` and `make demo` flow, then decide whether the next increment should focus on mocked adapter payloads or tighter triage rules for FAQ versus UX_GAP.

### 2026-04-21 - Session 2

#### Intent

Add the temporary implementation slice that will carry the collection, normalization, and triage narrative through the hackathon repo before any source code lands.

#### Changes

- Updated the repo narrative to remove the previous project framing and align every document with the CS collection and triage workflow.
- Reframed the milestone plan around collection, triage, routing, and demo readiness.
- Tightened the runbook language to match the temporary CS ticket flow.
- Revised the verification script to check current document headings and required sections.

#### Verification

- Not run yet; this change is docs and verification narrative only.

#### Risks

- `spec.md` already contains unrelated edits in the worktree, so this pass avoids touching it.
- The temporary slice still depends on later source code work to become executable.

#### Next step

Add the minimal implementation slice in a separate worker while keeping the docs and verification checkpoints stable.

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

- `make test`: passed
- `make lint`: passed
- `make typecheck`: passed
- `make build`: passed
- Build artifact generated at [dist/agent-brief.md](/Users/yong/codex-hackathon/dist/agent-brief.md)

#### Risks

- Product direction is clear, but no application code exists yet.
- Live Linear integration remains intentionally deferred to avoid blocking the MVP path.

#### Next step

Start Milestone 1 by defining the ticket input schema, triage outputs, and deterministic routing rules before any application code is generated.

## dist/cs_demo_report.md

# CS triage demo report

Source seed: `tests/fixtures/cs_seed.json`
Tickets processed: 4

## Summary

| Category | Count |
| --- | ---: |
| FAQ | 1 |
| UX_GAP | 1 |
| DEFECT | 2 |

| Scope | Count |
| --- | ---: |
| P1 | 2 |
| P2 | 2 |

## Routing

| Route | Count |
| --- | ---: |
| Customer Reply Draft | 1 |
| UX Review | 1 |
| Hotfix Queue | 1 |
| Sprint Backlog | 1 |
| Backlog | 0 |

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
