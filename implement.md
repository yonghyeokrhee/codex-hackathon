# Long-Running Job Runbook

## 목적

이 문서는 CS 수집 및 트리아지 자동화가 어떤 순서로 작업해야 하는지 정리한다.

## 작업 전 확인

1. `spec.md`, `plans.md`, `documentation.md`를 읽는다.
2. 최근 automation memory와 documentation 로그를 확인한다.
3. 이미 생성된 Linear 이슈와 Slack 알림이 있는지 dedupe 기준으로 확인한다.

## 실행 순서

1. Computer Use로 접근 가능한 입력 채널을 확인한다.
2. 신규 CS를 수집하거나 fallback sample을 사용한다.
3. 티켓을 정규화하고 triage한다.
4. 실제 Linear write와 Slack 전송을 수행한다.
5. 결과를 `documentation.md`에 기록한다.

## 기록 원칙

- source
- dedupe 기준
- category / severity / route
- Linear 링크
- Slack 전송 결과
- 실패와 fallback
