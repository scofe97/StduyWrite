---
title: 12_AI MOC
tags: [moc, ai, llm]
status: final
related:
  - roadmap.md
updated: 2026-06-25
---

# 12_AI
---
> AI 모델과 도구를 다루는 카테고리입니다. LLM 모델 릴리스 정리, 에이전트 도구, 프롬프트 설계 같은 주제를 모읍니다.

> AI Engineering 딥다이브 로드맵의 **섹션별 키워드 전체**(모델 특성·Prompt·Context·Token·RAG·Tool Calling·MCP·Harness·Agent·Evaluation·Guardrail·Observability 18주제)는 [roadmap.md](roadmap.md)에 원문 그대로 정리해 두었습니다. 아래 "등록된 절"이 *이미 작성된 문서*(Claude/Anthropic 관점)라면, roadmap.md는 *다뤄야 할 전체 범위*(벤더 중립·OpenAI 관점 보완)의 SSOT입니다.

## 등록된 절

`01-xx`는 모델별 릴리스 정리, `02-xx`는 AI Engineering 핵심 개념(시험 대비 5축)입니다.

| 절 | 제목 | 다루는 범위 |
|----|------|-----------|
| 01-01 | [Claude Opus 4.8 — 4.7에서 무엇이 달라졌나](./01-01.Claude%20Opus%204.8%20—%204.7에서%20무엇이%20달라졌나.md) | 정직성 개선, 벤치마크, mid-conversation system 메시지, fast mode, effort 기본값, 4.7 대비 API 변화 |
| 02-01 | [LLM 모델의 특성과 활용](./02-01.LLM%20모델의%20특성과%20활용%20—%20선택·사고·구조화·마이그레이션.md) | 모델 선택·라우팅, adaptive thinking·effort, 능력 조회·구조화 출력, 모델 마이그레이션, 거부·폴백 |
| 02-02 | [Harness Engineering](./02-02.Harness%20Engineering%20—%20모델을%20감싸는%20오케스트레이션%20층.md) | 모델 vs 하네스 책임, 도구 사용·tool_choice, 에이전트 루프, 도구 표면 설계(bash vs 전용), 권한 게이팅, 스킬·멀티에이전트, 컨텍스트 관리 |
| 02-03 | [Token Optimization](./02-03.Token%20Optimization%20—%20비용·지연·context%20rot를%20줄이는%20법.md) | 프롬프트 캐싱(prefix match), 컨텍스트 격리, compact/clear/rewind, 출력 토큰 제어(max_tokens·effort·task budget), tool search·PTC, 배치 |
| 02-04 | [MCP 설계](./02-04.MCP%20설계%20—%20외부%20도구·데이터를%20표준으로%20연결하기.md) | N×M 통합, Tools/Resources/Prompts, Host/Client/Server, 인증·vault 격리, 도구 설계, 프롬프트 주입 방어 |
| 02-05 | [AI Agentization](./02-05.AI%20Agentization%20—%20워크플로우와%20에이전트%20사이.md) | 워크플로우 vs 에이전트, 에이전트 판단 4기준, 티어, 상태·메모리, 완료 검증(루브릭), 환각 통제, 관찰성·스티어링 |

## 경계 기준

특정 프레임워크에 종속된 AI 활용(예: Spring AI, LangChain4j 연동)은 해당 언어·프레임워크 카테고리로 보내고, 모델 자체의 특성·릴리스·API와 모델 독립적인 에이전트 도구만 여기에 둡니다. Claude Code 같은 CLI 도구 설정은 `09_tools/`와 겹칠 수 있는데, *도구 설치·키맵*은 09_tools, *모델 능력·API 동작*은 본 카테고리로 나눕니다.

## 향후 추가 후보

- 01-02: 다른 LLM 벤더(OpenAI·Gemini) 특성 비교 — 시험이 벤더 중립이면 보강
- 02-06: RAG와 긴 컨텍스트의 트레이드오프 — 검색이냐 컨텍스트 주입이냐 (02-03과 짝)
- 02-07: 비용·지연 운영 — 스트리밍·캐시 프리워밍·에러 재시도 (횡단 주제, 02-03 심화)
