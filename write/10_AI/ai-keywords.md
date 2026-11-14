---
title: AI 개발 키워드 — DevOps 축
tags: [keywords, ai, llm, agent, mcp, gitops, devops]
status: final
source:
  - ../10_AI/README.md
  - ../07_devops/book/aic_ai-infra-claude/README.md
related:
  - ../README.md
  - ../08_cloud/k8s-keywords.md
  - ../06_observability/observability-keywords.md
updated: 2026-10-10
---

# AI 개발 키워드 — DevOps 축
---

> AI 개발 키워드 표. 문서를 쓸 때 참고합니다.



## 1단계 · 모델을 도구로 쓰기

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 모델 종류와 선택 기준 | 필수 | [LLM 모델 활용](../10_AI/02-01.LLM%20%EB%AA%A8%EB%8D%B8%EC%9D%98%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%ED%99%9C%EC%9A%A9%20%E2%80%94%20%EC%84%A0%ED%83%9D%C2%B7%EC%82%AC%EA%B3%A0%C2%B7%EA%B5%AC%EC%A1%B0%ED%99%94%C2%B7%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98.md) | AI Engineering 1장 |
| 추론 노력과 사고 깊이 조절 | 필수 | [LLM 모델 활용](../10_AI/02-01.LLM%20%EB%AA%A8%EB%8D%B8%EC%9D%98%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%ED%99%9C%EC%9A%A9%20%E2%80%94%20%EC%84%A0%ED%83%9D%C2%B7%EC%82%AC%EA%B3%A0%C2%B7%EA%B5%AC%EC%A1%B0%ED%99%94%C2%B7%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98.md) | |
| 구조화 출력과 JSON Schema | 필수 | [LLM 모델 활용](../10_AI/02-01.LLM%20%EB%AA%A8%EB%8D%B8%EC%9D%98%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%ED%99%9C%EC%9A%A9%20%E2%80%94%20%EC%84%A0%ED%83%9D%C2%B7%EC%82%AC%EA%B3%A0%C2%B7%EA%B5%AC%EC%A1%B0%ED%99%94%C2%B7%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98.md) | |
| 토큰 넷 — 입력 · 출력 · 추론 · 캐시 | 필수 | [Token Optimization](../10_AI/02-03.Token%20Optimization%20%E2%80%94%20%EB%B9%84%EC%9A%A9%C2%B7%EC%A7%80%EC%97%B0%C2%B7context%20rot%EB%A5%BC%20%EC%A4%84%EC%9D%B4%EB%8A%94%20%EB%B2%95.md) | AI Engineering 1장 |
| 비용과 지연의 셈법 | 필수 | [Token Optimization](../10_AI/02-03.Token%20Optimization%20%E2%80%94%20%EB%B9%84%EC%9A%A9%C2%B7%EC%A7%80%EC%97%B0%C2%B7context%20rot%EB%A5%BC%20%EC%A4%84%EC%9D%B4%EB%8A%94%20%EB%B2%95.md) | |
| 토크나이저 — BPE · 언어마다 토큰 수가 다른 이유 | 선택 | | |
| 모델 교체와 거부 · 폴백 | 추천 | [LLM 모델 활용](../10_AI/02-01.LLM%20%EB%AA%A8%EB%8D%B8%EC%9D%98%20%ED%8A%B9%EC%84%B1%EA%B3%BC%20%ED%99%9C%EC%9A%A9%20%E2%80%94%20%EC%84%A0%ED%83%9D%C2%B7%EC%82%AC%EA%B3%A0%C2%B7%EA%B5%AC%EC%A1%B0%ED%99%94%C2%B7%EB%A7%88%EC%9D%B4%EA%B7%B8%EB%A0%88%EC%9D%B4%EC%85%98.md) | |
| 모델 캐스케이드 — 값싼 분류기로 거르고 필요할 때만 큰 모델 | 추천 | | |
| 세대별로 무엇이 달라지는가 | 선택 | [Opus 4.8 변화](../10_AI/01-01.Claude%20Opus%204.8%20%E2%80%94%204.7%EC%97%90%EC%84%9C%20%EB%AC%B4%EC%97%87%EC%9D%B4%20%EB%8B%AC%EB%9D%BC%EC%A1%8C%EB%82%98.md) | |



## 2단계 · 프롬프트와 컨텍스트

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 지시 3계층 — 시스템 · 개발자 · 사용자 | 필수 | [Prompt Engineering](../10_AI/02-06.Prompt%20Engineering%20%E2%80%94%20%EC%A7%80%EC%8B%9C%C2%B7%EC%97%AD%ED%95%A0%C2%B7%ED%98%95%EC%8B%9D%C2%B7%EC%98%88%EC%8B%9C%EB%A1%9C%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EC%A1%B0%EC%A2%85%ED%95%98%EA%B8%B0.md) | AI Engineering 5장 |
| 출력 형식과 예시 설계 | 필수 | [Prompt Engineering](../10_AI/02-06.Prompt%20Engineering%20%E2%80%94%20%EC%A7%80%EC%8B%9C%C2%B7%EC%97%AD%ED%95%A0%C2%B7%ED%98%95%EC%8B%9D%C2%B7%EC%98%88%EC%8B%9C%EB%A1%9C%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EC%A1%B0%EC%A2%85%ED%95%98%EA%B8%B0.md) | AI Engineering 5장 |
| 컨텍스트 윈도우 구성 | 필수 | [Context Engineering](../10_AI/02-07.Context%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%B4%20%EB%B3%B4%EB%8A%94%20%EC%84%B8%EA%B3%84%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B8%B0.md) | |
| 압축 · 우선순위 · 축출 | 필수 | [Context Engineering](../10_AI/02-07.Context%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%B4%20%EB%B3%B4%EB%8A%94%20%EC%84%B8%EA%B3%84%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B8%B0.md) | |
| 프롬프트 캐싱과 접두 일치 | 필수 | [Token Optimization](../10_AI/02-03.Token%20Optimization%20%E2%80%94%20%EB%B9%84%EC%9A%A9%C2%B7%EC%A7%80%EC%97%B0%C2%B7context%20rot%EB%A5%BC%20%EC%A4%84%EC%9D%B4%EB%8A%94%20%EB%B2%95.md) | |
| 컨텍스트 격리와 토큰 예산 | 추천 | [Token Optimization](../10_AI/02-03.Token%20Optimization%20%E2%80%94%20%EB%B9%84%EC%9A%A9%C2%B7%EC%A7%80%EC%97%B0%C2%B7context%20rot%EB%A5%BC%20%EC%A4%84%EC%9D%B4%EB%8A%94%20%EB%B2%95.md) | |
| 컨텍스트 부패와 롱컨텍스트 한계 | 추천 | [Context Engineering](../10_AI/02-07.Context%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%B4%20%EB%B3%B4%EB%8A%94%20%EC%84%B8%EA%B3%84%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B8%B0.md) | |
| RAG — 런북과 매니페스트를 근거로 | 추천 | [RAG 설계](../10_AI/02-08.RAG%20%C2%B7%20Retrieval%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%9E%84%EB%B2%A0%EB%94%A9%C2%B7%EA%B2%80%EC%83%89%C2%B7%EA%B7%BC%EA%B1%B0%EB%A1%9C%20%EB%8B%B5%EC%9D%84%20%EB%B6%99%EB%93%A4%EA%B8%B0.md) | AI Engineering 6장 |
| 프롬프트 회귀 시험 | 추천 | [Prompt Engineering](../10_AI/02-06.Prompt%20Engineering%20%E2%80%94%20%EC%A7%80%EC%8B%9C%C2%B7%EC%97%AD%ED%95%A0%C2%B7%ED%98%95%EC%8B%9D%C2%B7%EC%98%88%EC%8B%9C%EB%A1%9C%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EC%A1%B0%EC%A2%85%ED%95%98%EA%B8%B0.md) | |



## 3단계 · 도구 연결과 MCP

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 도구 호출과 도구 스키마 | 필수 | [Harness Engineering](../10_AI/02-02.Harness%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EA%B0%90%EC%8B%B8%EB%8A%94%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%EC%B8%B5.md) | AI Agents 4장 |
| 도구 표면 설계 — 범용 셸과 전용 도구 | 필수 | [Harness Engineering](../10_AI/02-02.Harness%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EA%B0%90%EC%8B%B8%EB%8A%94%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%EC%B8%B5.md) | AI Agents 4장 |
| 결과 압축과 오류 · 재시도 | 필수 | [Token Optimization](../10_AI/02-03.Token%20Optimization%20%E2%80%94%20%EB%B9%84%EC%9A%A9%C2%B7%EC%A7%80%EC%97%B0%C2%B7context%20rot%EB%A5%BC%20%EC%A4%84%EC%9D%B4%EB%8A%94%20%EB%B2%95.md) | |
| JSON-RPC 와 도구 스키마 | 추천 | [flats: MCP·JSON-RPC](../10_AI/project/flats/04-01.MCP%C2%B7JSON-RPC%C2%B7Same-origin%C2%B7CSRF%C2%B7DNS%20rebinding.md) | Claude Code 7장 |
| MCP 삼자 — 호스트 · 클라이언트 · 서버 | 필수 | [MCP 설계](../10_AI/02-04.MCP%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%99%B8%EB%B6%80%20%EB%8F%84%EA%B5%AC%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%ED%91%9C%EC%A4%80%EC%9C%BC%EB%A1%9C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0.md) | Claude Code 7장 |
| Tools · Resources · Prompts | 필수 | [MCP 설계](../10_AI/02-04.MCP%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%99%B8%EB%B6%80%20%EB%8F%84%EA%B5%AC%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%ED%91%9C%EC%A4%80%EC%9C%BC%EB%A1%9C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0.md) | Claude Code 7장 |
| 전송 방식과 인증 | 추천 | [MCP 설계](../10_AI/02-04.MCP%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%99%B8%EB%B6%80%20%EB%8F%84%EA%B5%AC%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%ED%91%9C%EC%A4%80%EC%9C%BC%EB%A1%9C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0.md) | |
| 읽기 전용과 쓰기의 분리 | 필수 | [MCP 설계](../10_AI/02-04.MCP%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%99%B8%EB%B6%80%20%EB%8F%84%EA%B5%AC%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%ED%91%9C%EC%A4%80%EC%9C%BC%EB%A1%9C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0.md) | Claude Code 5장 |
| 승인 게이트와 감사 로그 | 필수 | [Guardrail](../10_AI/02-10.Guardrail%20%C2%B7%20Safety%20%26%20Observability%20%E2%80%94%20%EA%B6%8C%ED%95%9C%C2%B7%EB%B0%A9%EC%96%B4%C2%B7%EA%B4%80%EC%B8%A1.md) · [flats: 승인·신뢰 모델](../10_AI/project/flats/04-04.approval%C2%B7trust%20model.md) | |



## 4단계 · 하네스와 에이전트

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 에이전트 루프의 뼈대 | 필수 | [Harness Engineering](../10_AI/02-02.Harness%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EA%B0%90%EC%8B%B8%EB%8A%94%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%EC%B8%B5.md) | AI Agents 2장 |
| 워크플로우로 고정할 자리 | 필수 | [AI Agentization](../10_AI/02-05.AI%20Agentization%20%E2%80%94%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0%EC%99%80%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%82%AC%EC%9D%B4.md) | AI Agents 2장 |
| 상태 · 메모리 · 중단과 재개 | 필수 | [AI Agentization](../10_AI/02-05.AI%20Agentization%20%E2%80%94%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0%EC%99%80%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%82%AC%EC%9D%B4.md) | AI Agents 6장 |
| 오케스트레이션 패턴 | 필수 | [오케스트레이션 모델](../10_AI/docs/orca/03-01.%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20%EB%A9%94%EC%8B%9C%EC%A7%80%C2%B7%ED%83%9C%EC%8A%A4%ED%81%AC%C2%B7%EA%B2%8C%EC%9D%B4%ED%8A%B8.md) | AI Agents 5장 |
| 하나에서 여럿으로 — 서브에이전트 | 추천 | [Harness Engineering](../10_AI/02-02.Harness%20Engineering%20%E2%80%94%20%EB%AA%A8%EB%8D%B8%EC%9D%84%20%EA%B0%90%EC%8B%B8%EB%8A%94%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%20%EC%B8%B5.md) | AI Agents 8장 |
| 사람이 끼는 지점 | 필수 | [AI Agentization](../10_AI/02-05.AI%20Agentization%20%E2%80%94%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0%EC%99%80%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%82%AC%EC%9D%B4.md) | AI Agents 13장 |
| 완료 검증과 루브릭 | 필수 | [AI Agentization](../10_AI/02-05.AI%20Agentization%20%E2%80%94%20%EC%9B%8C%ED%81%AC%ED%94%8C%EB%A1%9C%EC%9A%B0%EC%99%80%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%82%AC%EC%9D%B4.md) | AI Agents 9장 |
| 하네스 사례 하나 뜯어보기 | 선택 | 자료 미연결 | |
| ReAct — 추론과 도구 호출을 번갈아 반복 | 추천 | [당근 발표 정리](../_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [ReAct 논문](https://arxiv.org/abs/2210.03629) |



## 5단계 · AI 개발 환경

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 에이전틱 개발이 바꾼 것 | 필수 | [ADE란 무엇인가](../10_AI/docs/orca/01-01.ADE%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%20%E2%80%94%20IDE%EC%97%90%EC%84%9C%20ADE%EA%B9%8C%EC%A7%80.md) | Claude Code 1장 |
| 행동 규칙 · 스킬 · 훅 | 필수 | | Claude Code 6장 |
| 맥락 주입 시점 — 항상 · 트리거 뒤 · 세션 시작 선택 | 선택 |  |  |
| 권한과 신뢰 경계 | 필수 | [운영과 권한 경계](../10_AI/docs/orca/05-01.%EC%9A%B4%EC%98%81%EA%B3%BC%20%EA%B6%8C%ED%95%9C%20%EA%B2%BD%EA%B3%84%20%E2%80%94%20%ED%99%98%EA%B2%BD%20%EB%A0%88%EC%8B%9C%ED%94%BC%C2%B7%EC%9B%90%EA%B2%A9%20%EB%9F%B0%ED%83%80%EC%9E%84%C2%B7%EB%B3%B4%EC%95%88.md) | Claude Code 5장 |
| 분위기 코딩이 막히는 자리 | 추천 | | Claude Code 4장 |
| 워크트리로 작업 공간 가르기 | 추천 | [워크트리](../10_AI/docs/orca/02-01.Repo%C2%B7%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%C2%B7%EC%9B%8C%ED%81%AC%ED%8A%B8%EB%A6%AC%20%E2%80%94%20%EC%9E%91%EC%97%85%20%EA%B3%B5%EA%B0%84%EC%9D%84%20%EA%B0%80%EB%A5%B4%EB%8A%94%20%EB%B2%95.md) | |
| 여러 에이전트 동시 운전 | 추천 | [에이전트 운전](../10_AI/docs/orca/02-02.%ED%84%B0%EB%AF%B8%EB%84%90%EA%B3%BC%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%EC%9A%B4%EC%A0%84%20%E2%80%94%20%EC%A7%80%EC%8B%9C%C2%B7%EB%8C%80%EA%B8%B0%C2%B7%EC%99%84%EB%A3%8C%20%ED%8C%90%EC%A0%95.md) | |
| 이슈에서 PR 까지 한 줄기 | 추천 | [실전 파이프라인](../10_AI/docs/orca/03-02.%EC%8B%A4%EC%A0%84%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%E2%80%94%20%EC%9D%B4%EC%8A%88%EC%97%90%EC%84%9C%20PR%EA%B9%8C%EC%A7%80.md) | |
| 거짓 성공과 개입 신호 | 필수 | [실패와 복구](../10_AI/docs/orca/05-02.%EC%8B%A4%ED%8C%A8%EC%99%80%20%EB%B3%B5%EA%B5%AC%20%E2%80%94%20%EA%B1%B0%EC%A7%93%20%EC%84%B1%EA%B3%B5%EA%B3%BC%20%EA%B0%9C%EC%9E%85%20%EC%8B%A0%ED%98%B8.md) | |
| 화면 밖 자동화 | 선택 | [화면 밖 자동화](../10_AI/docs/orca/04-02.%ED%99%94%EB%A9%B4%20%EB%B0%96%20%EC%9E%90%EB%8F%99%ED%99%94%20%E2%80%94%20%EC%BB%B4%ED%93%A8%ED%84%B0%20%EC%9C%A0%EC%A6%88%C2%B7%EC%97%90%EB%AE%AC%EB%A0%88%EC%9D%B4%ED%84%B0%C2%B7%EC%98%88%EC%95%BD%20%EC%8B%A4%ED%96%89.md) | |



## 6단계 · GitAIOps — 인프라를 AI 와 짓기

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| GitOps 선언과 드리프트 | 필수 | [GitOps에서 GitAIOps로](../07_devops/book/aic_ai-infra-claude/01-02.GitOps%EC%97%90%EC%84%9C%20GitAIOps%EB%A1%9C.md) | AI 인프라 1장 |
| ArgoCD Application 과 롤백 | 필수 | [ArgoCD GitOps](../07_devops/book/aic_ai-infra-claude/03-01.%ED%91%B8%EC%8B%9C%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20ArgoCD%20GitOps%20%E2%80%94%20%EC%84%A4%EC%B9%98%C2%B7%EC%97%B0%EA%B2%B0%C2%B7%EB%A1%A4%EB%A7%81%C2%B7%EB%A1%A4%EB%B0%B1.md) | AI 인프라 3장 |
| CI 연결과 무한 루프 방어 | 필수 | [Actions CI와 ArgoCD](../07_devops/book/aic_ai-infra-claude/03-02.%EA%B9%83%ED%97%88%EB%B8%8C%20%EC%95%A1%EC%85%98%20CI%EC%99%80%20ArgoCD%20%EC%97%B0%EA%B2%B0%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) | AI 인프라 3장 |
| 관측을 한 번에 세우기 | 필수 | [메트릭 관측](../07_devops/book/aic_ai-infra-claude/04-01.%EA%B4%80%EC%B8%A1%20%EA%B0%80%EB%8A%A5%EC%84%B1%EA%B3%BC%20%EB%A9%94%ED%8A%B8%EB%A6%AD%20%E2%80%94%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4%C2%B7%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98.md) | AI 인프라 4장 |
| 로그와 알림 규칙 | 필수 | [로그와 알림](../07_devops/book/aic_ai-infra-claude/04-02.%EB%A1%9C%EA%B7%B8%EC%99%80%20%EC%95%8C%EB%A6%BC%20%E2%80%94%20Loki%C2%B7Fluent%20Bit%C2%B7PrometheusRule.md) | AI 인프라 4장 |
| 롤링 업데이트의 빈틈과 Gateway API | 필수 | [Rolling Update 한계](../07_devops/book/aic_ai-infra-claude/05-01.Rolling%20Update%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20Gateway%20API.md) | AI 인프라 5장 |
| Blue/Green 무중단 전환 | 필수 | [Blue/Green 전환](../07_devops/book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md) | AI 인프라 5장 |
| 점진적 배포 Canary | 필수 | [Canary 배포](../07_devops/book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) | AI 인프라 6장 |
| 상태 공유와 시크릿 관리 | 추천 | [Valkey·Secret Manager](../07_devops/book/aic_ai-infra-claude/06-01.Valkey%20%EC%BA%90%EC%8B%9C%EC%99%80%20Google%20Secret%20Manager.md) | AI 인프라 6장 |
| 멀티 노드풀과 Spot VM | 추천 | [멀티 노드풀](../07_devops/book/aic_ai-infra-claude/07-01.SMB%20%EA%B5%AC%EC%A1%B0%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20%EB%A9%80%ED%8B%B0%20%EB%85%B8%EB%93%9C%ED%92%80.md) | AI 인프라 7장 |
| App of Apps 와 멀티테넌시 | 추천 | [App of Apps와 멀티테넌시](../07_devops/book/aic_ai-infra-claude/07-02.App%20of%20Apps%EC%99%80%20%EB%A9%80%ED%8B%B0%ED%85%8C%EB%84%8C%EC%8B%9C.md) | AI 인프라 7장 |
| 이벤트 드리븐과 분산 트레이싱 | 추천 | [Kafka·Tempo](../07_devops/book/aic_ai-infra-claude/08-01.Kafka%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EB%93%9C%EB%A6%AC%EB%B8%90%EA%B3%BC%20Tempo%20%EB%B6%84%EC%82%B0%20%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%8B%B1.md) | AI 인프라 8장 |
| 행동 규칙 · 메모리 · 결정 기록 | 필수 | [Actions CI와 ArgoCD](../07_devops/book/aic_ai-infra-claude/03-02.%EA%B9%83%ED%97%88%EB%B8%8C%20%EC%95%A1%EC%85%98%20CI%EC%99%80%20ArgoCD%20%EC%97%B0%EA%B2%B0%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) | AI 인프라 3~6장 |
| 위험 명령 가드레일 | 필수 | [CronJob·가드레일](../07_devops/book/aic_ai-infra-claude/08-02.CronJob%20%EB%B0%B0%EC%B9%98%20%EC%9E%90%EB%8F%99%ED%99%94%EC%99%80%20command-guardrails.md) | AI 인프라 8장 |
| 살아있는 운영 표준으로 굳히기 | 필수 | [GitAIOps 운영 표준](../07_devops/book/aic_ai-infra-claude/09-01.GitAIOps%20%E2%80%94%20%EC%82%B4%EC%95%84%EC%9E%88%EB%8A%94%20%EC%9A%B4%EC%98%81%20%ED%91%9C%EC%A4%80%EC%9D%98%20%ED%83%84%EC%83%9D.md) | AI 인프라 9장 |



## 7단계 · 평가와 가드레일

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 골든 데이터셋과 회귀 시험 | 필수 | [Evaluation](../10_AI/02-09.Evaluation%20%C2%B7%20Test%20Harness%20%E2%80%94%20%EB%B9%84%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84%20%EC%B1%84%EC%A0%90%ED%95%98%EA%B8%B0.md) | AI Engineering 3장 |
| confidence 보정과 임계값 설계 — false positive 와 negative 의 교환 | 추천 | | |
| 무엇을 잴 것인가 | 필수 | [Evaluation](../10_AI/02-09.Evaluation%20%C2%B7%20Test%20Harness%20%E2%80%94%20%EB%B9%84%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84%20%EC%B1%84%EC%A0%90%ED%95%98%EA%B8%B0.md) | AI Engineering 4장 |
| 심판 모델과 그 한계 | 추천 | [Evaluation](../10_AI/02-09.Evaluation%20%C2%B7%20Test%20Harness%20%E2%80%94%20%EB%B9%84%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84%20%EC%B1%84%EC%A0%90%ED%95%98%EA%B8%B0.md) | AI Agents 9장 |
| 공개 벤치마크와 reward hacking — 점수가 오르는데 좋아지지 않을 때 | 선택 | | [SWE-bench](https://www.swebench.com/) |
| CI 게이트로 굳히기 | 필수 | [Evaluation](../10_AI/02-09.Evaluation%20%C2%B7%20Test%20Harness%20%E2%80%94%20%EB%B9%84%EA%B2%B0%EC%A0%95%EC%A0%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84%20%EC%B1%84%EC%A0%90%ED%95%98%EA%B8%B0.md) | |
| 주입 3종 — 프롬프트 · 도구 · 유출 | 필수 | [Guardrail](../10_AI/02-10.Guardrail%20%C2%B7%20Safety%20%26%20Observability%20%E2%80%94%20%EA%B6%8C%ED%95%9C%C2%B7%EB%B0%A9%EC%96%B4%C2%B7%EA%B4%80%EC%B8%A1.md) | AI Agents 12장 |
| 외부 데이터를 지시로 읽지 않기 | 필수 | [MCP 설계](../10_AI/02-04.MCP%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EC%99%B8%EB%B6%80%20%EB%8F%84%EA%B5%AC%C2%B7%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC%20%ED%91%9C%EC%A4%80%EC%9C%BC%EB%A1%9C%20%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0.md) | AI Agents 12장 |
| 샌드박스와 최소 권한 | 필수 | [Guardrail](../10_AI/02-10.Guardrail%20%C2%B7%20Safety%20%26%20Observability%20%E2%80%94%20%EA%B6%8C%ED%95%9C%C2%B7%EB%B0%A9%EC%96%B4%C2%B7%EA%B4%80%EC%B8%A1.md) | AI Agents 12장 |
| 시크릿 가리기와 개인정보 마스킹 | 필수 | [Guardrail](../10_AI/02-10.Guardrail%20%C2%B7%20Safety%20%26%20Observability%20%E2%80%94%20%EA%B6%8C%ED%95%9C%C2%B7%EB%B0%A9%EC%96%B4%C2%B7%EA%B4%80%EC%B8%A1.md) | |
| 예산 한도와 속도 제한 | 추천 | [Guardrail](../10_AI/02-10.Guardrail%20%C2%B7%20Safety%20%26%20Observability%20%E2%80%94%20%EA%B6%8C%ED%95%9C%C2%B7%EB%B0%A9%EC%96%B4%C2%B7%EA%B4%80%EC%B8%A1.md) | |



## 8단계 · 운영

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 에이전트 지표와 감사 로그 | 필수 | [Guardrail](../10_AI/02-10.Guardrail%20%C2%B7%20Safety%20%26%20Observability%20%E2%80%94%20%EA%B6%8C%ED%95%9C%C2%B7%EB%B0%A9%EC%96%B4%C2%B7%EA%B4%80%EC%B8%A1.md) | AI Agents 10장 |
| 과업당 비용과 병목 | 필수 | [Token Optimization](../10_AI/02-03.Token%20Optimization%20%E2%80%94%20%EB%B9%84%EC%9A%A9%C2%B7%EC%A7%80%EC%97%B0%C2%B7context%20rot%EB%A5%BC%20%EC%A4%84%EC%9D%B4%EB%8A%94%20%EB%B2%95.md) | AI Agents 10장 |
| 모델 공급자 실패 구분 — 401 · 403 · 429 · 쿼터 · BYOK 키 만료와 교체 | 선택 | | |
| 개선 루프 | 추천 | | AI Agents 11장 |
| 사람과 에이전트의 협업 | 추천 | | AI Agents 13장 |
| 프로덕션 준비와 배포 | 추천 | | Introducing MLOps 5·6장 |
| 모니터링과 되먹임 | 추천 | | Introducing MLOps 7장 |
| 모델 거버넌스 | 추천 | | Introducing MLOps 8장 |
| 추론 서빙 비용 | 선택 | | AI Engineering 9장 |
| 아키텍처와 사용자 피드백 | 선택 | | AI Engineering 10장 |
| 운영 에이전트 협업 — 경보 분석에서 수정 PR 까지 | 선택 | [당근 발표 정리](../_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | |



## 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| 사전학습 · 파인튜닝 · 데이터셋 구축 | 모델을 만드는 쪽입니다. AI Engineering 7·8장과 Build a LLM (From Scratch) 를 걸지 않았습니다 |
| 모델 아키텍처와 어텐션 내부 | 같은 이유입니다. 모델은 이 로드맵에서 고르고 부르는 대상입니다. AI Engineering 2장도 걸지 않았습니다 |
| 임베딩 모델 학습과 벡터 DB 운영 | 2단계는 검색을 쓰는 쪽만 봅니다. 벡터 DB 자체의 운영은 자료가 생기면 별도로 답니다 |
| 에이전트 제품의 화면 설계 | AI Agents 3·7장은 사용자 경험과 학습 루프 쪽입니다. 직무 축이 다릅니다 |
| 쿠버네티스 오브젝트와 내부 구조 | [Kubernetes 로드맵](../08_cloud/k8s-keywords.md)이 맡습니다. 6단계는 그 위에 배포 흐름을 얹는 자리입니다 |
| 지표 · 로그 · 트레이스의 일반 이론 | [관측 가능성 로드맵](../06_observability/observability-keywords.md)이 맡습니다. 8단계는 에이전트 고유 축만 봅니다 |
| MLOps 의 모델 개발 절차 | Introducing MLOps 4장과 9~11장 사례는 모델을 만드는 팀의 일입니다 |
| GPU 스케줄링과 학습 클러스터 | 소장 자료가 없습니다. 추론 서빙 인프라를 실제로 맡게 되면 그때 엽니다 |
| ML 플랫폼 — 피처 스토어 | 백엔드 키워드 목록이 백엔드 밖 심화로 따로 뺀 키워드 |
