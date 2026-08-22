---
title: 11_AI MOC
tags: [moc, ai, llm]
status: final
related:
  - roadmap.md
updated: 2026-06-25
---

# 11_AI
---
> AI 모델과 도구를 다루는 카테고리입니다. LLM 모델 릴리스 정리, 에이전트 도구, 프롬프트 설계 같은 주제를 모읍니다.

주요 LLM 모델의 특성과 활용 방식을 이해하고, AI 기반 개발 환경에서 요구되는 Harness Engineering, Token Optimization, MCP 설계 등 핵심 AI 엔지니어링 기술을 습득하여 AI Agentization하는 실무 역량을 함양하고자 함

> AI Engineering 딥다이브 로드맵의 **섹션별 키워드 전체**(모델 특성·Prompt·Context·Token·RAG·Tool Calling·MCP·Harness·Agent·Evaluation·Guardrail·Observability 18주제)는 [roadmap.md](roadmap.md)에 원문 그대로 정리해 두었습니다. 아래 "등록된 절"이 *이미 작성된 문서*(Claude/Anthropic 관점)라면, roadmap.md는 *다뤄야 할 전체 범위*(벤더 중립·OpenAI 관점 보완)의 SSOT입니다.

## 등록된 절

`01-xx`는 모델별 릴리스 정리, `02-xx`는 AI Engineering 핵심 개념입니다. 02-01~05는 Claude 관점 5축(모델특성·Harness·Token·MCP·Agentization), 02-06~10은 roadmap 18주제의 나머지 갭을 벤더 중립으로 메운 5편(Prompt·Context·RAG·Evaluation·Guardrail/Observability)입니다.

| 절 | 제목 | 다루는 범위 |
|----|------|-----------|
| 01-01 | [Claude Opus 4.8 — 4.7에서 무엇이 달라졌나](./01-01.Claude%20Opus%204.8%20—%204.7에서%20무엇이%20달라졌나.md) | 정직성 개선, 벤치마크, mid-conversation system 메시지, fast mode, effort 기본값, 4.7 대비 API 변화 |
| 02-01 | [LLM 모델의 특성과 활용](./02-01.LLM%20모델의%20특성과%20활용%20—%20선택·사고·구조화·마이그레이션.md) | 모델 선택·라우팅, adaptive thinking·effort, 능력 조회·구조화 출력, 모델 마이그레이션, 거부·폴백 |
| 02-02 | [Harness Engineering](./02-02.Harness%20Engineering%20—%20모델을%20감싸는%20오케스트레이션%20층.md) | 모델 vs 하네스 책임, 도구 사용·tool_choice, 에이전트 루프, 도구 표면 설계(bash vs 전용), 권한 게이팅, 스킬·멀티에이전트, 컨텍스트 관리 |
| 02-03 | [Token Optimization](./02-03.Token%20Optimization%20—%20비용·지연·context%20rot를%20줄이는%20법.md) | 프롬프트 캐싱(prefix match), 컨텍스트 격리, compact/clear/rewind, 출력 토큰 제어(max_tokens·effort·task budget), tool search·PTC, 배치 |
| 02-04 | [MCP 설계](./02-04.MCP%20설계%20—%20외부%20도구·데이터를%20표준으로%20연결하기.md) | N×M 통합, Tools/Resources/Prompts, Host/Client/Server, 인증·vault 격리, 도구 설계, 프롬프트 주입 방어 |
| 02-05 | [AI Agentization](./02-05.AI%20Agentization%20—%20워크플로우와%20에이전트%20사이.md) | 워크플로우 vs 에이전트, 에이전트 판단 4기준, 티어, 상태·메모리, 완료 검증(루브릭), 환각 통제, 관찰성·스티어링 |
| 02-06 | [Prompt Engineering](./02-06.Prompt%20Engineering%20—%20지시·역할·형식·예시로%20모델을%20조종하기.md) | System/Developer/User 3계층 권한 위계, 구성요소(role·task·constraint·output format), zero/few-shot·negative example, 구조화 출력(JSON Schema), 프롬프트 회귀 테스트 |
| 02-07 | [Context Engineering](./02-07.Context%20Engineering%20—%20모델이%20보는%20세계를%20설계하기.md) | 프롬프트 vs 컨텍스트, 컨텍스트 윈도우 구성, working↔long-term memory, 압축·우선순위·축출, reasoning token 공간, context rot |
| 02-08 | [RAG · Retrieval 설계](./02-08.RAG%20·%20Retrieval%20설계%20—%20임베딩·검색·근거로%20답을%20붙들기.md) | RAG 파이프라인, embedding·vector DB, semantic/keyword/hybrid 검색, chunking·top-K·reranking, recall↔precision, grounding·citation, RAG vs 롱컨텍스트 |
| 02-09 | [Evaluation · Test Harness](./02-09.Evaluation%20·%20Test%20Harness%20—%20비결정적%20시스템을%20채점하기.md) | 골든 데이터셋·회귀 테스트, groundedness↔faithfulness↔answer relevance, task success rate·latency·cost, LLM-as-a-judge, CI gate |
| 02-10 | [Guardrail · Safety & Observability](./02-10.Guardrail%20·%20Safety%20&%20Observability%20—%20권한·방어·관측.md) | 주입 3종(prompt/tool/data exfiltration), 권한 경계(read-only↔write↔approval gate), redaction·PII masking·sandbox·budget limit, 관측 지표, audit log·trace |

## 하위 폴더

| 폴더 | 편수 | 다루는 범위 |
|------|------|------------|
| [`hermes/`](hermes/) | 1편 | Hermes 에이전트 하네스 사례 — 자기개선 로컬 에이전트의 루프와 메모리 구조 |
| [`quiz/`](quiz/) | 4편 | 학습 퀴즈 축적본, AI 엔지니어링·Agentization 각 100문항, 오답 노트 |

위 "등록된 절"이 개념 본문이라면 이 둘은 사례와 자가 점검입니다. 본문 개정 시 함께 보지 않아도 되도록 분리해 둡니다.



## 경계 기준

특정 프레임워크에 종속된 AI 활용(예: Spring AI, LangChain4j 연동)은 해당 언어·프레임워크 카테고리로 보내고, 모델 자체의 특성·릴리스·API와 모델 독립적인 에이전트 도구만 여기에 둡니다. Claude Code 같은 CLI 도구 설정은 `09_tools/`와 겹칠 수 있는데, *도구 설치·키맵*은 09_tools, *모델 능력·API 동작*은 본 카테고리로 나눕니다.

## 향후 추가 후보

> 02-06~10 신규 5편으로 roadmap 18주제의 개념 갭(Prompt·Context·RAG·Evaluation·Guardrail·Observability)은 메웠습니다. RAG↔롱컨텍스트 트레이드오프는 02-08 §7에, 프롬프트 구조화 출력은 02-06 §4에 흡수됐습니다. 남은 후보는 아래와 같습니다.

- 01-02: 다른 LLM 벤더(OpenAI·Gemini) 모델 라인업·가격 비교 — 벤더별 모델명 문제 대비
- 02-11: Tool/Function Calling 심화 전용편 — 현재 02-02(tool_use)·02-08(retrieval tool)·02-10(permission)에 분산 흡수. 시험이 tool schema·retry·timeout을 깊게 물으면 분리
- 02-12: 비용·지연 운영 — 스트리밍·캐시 프리워밍·에러 재시도 (횡단 주제, 02-03 심화)
- 추천 프로젝트 5종(roadmap §16) 실습 노트 — 코드 리뷰/Jenkins 분석/MCP 서버/Token Optimizer/Eval Harness
