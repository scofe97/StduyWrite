---
title: Jenkins REST API 학습 MOC
tags: [moc, jenkins, api, rest, crumb, blue-ocean, wfapi, tps]
status: final
related:
  - ../README.md
  - ../01_core/README.md
  - ../02_security/README.md
  - ../05_operations/README.md
updated: 2026-05-30
---

# Jenkins REST API 학습 MOC

---

> Jenkins UI 가 하는 일 — Job 생성·빌드 실행·로그 조회·크레덴셜 관리 — 을 코드로 자동화하기 위한 REST API 문서를 한 폴더로 묶었습니다. 본 묶음을 끝내면 "TPS 같은 외부 시스템이 Jenkins 를 호출해 빌드를 던지고 결과를 적재할 때, 어떤 엔드포인트를 어떤 인증으로 어떻게 호출해야 하는지" 를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

REST API 묶음은 책 한 권 분량(약 280KB) 입니다. 다른 주제(보안·Agent·운영)와 한 폴더에 두면 카테고리가 비대해져 진입점이 흐려집니다. API 만 분리해 두면 "Jenkins 를 자동화하려는 사람" 의 동선이 명확해지고, 짝 문서(스펙 / TPS 패턴 / 현대화) 가 한 폴더 안에서 인접해 학습 비용이 줄어듭니다.

폴더 안은 주제 묶음별로 장번호를 나눴습니다. 환경·개요(`01`·`02`) 다음에 인증(`03`), Job CRUD(`04`), 빌드 실행·큐(`05`), 상태 추적(`06`), 로그(`07`), 크레덴셜(`08`), 운영(`09`) 순으로 이어집니다. 각 장 안에서 표준 REST 스펙이 `NN-01`, 그 위에 얹는 TPS 운영 패턴·현대화 해석이 `NN-02`·`NN-03`으로 따라옵니다. 스펙과 패턴을 짝으로 인접시켜, 스펙을 먼저 보고 막힐 때 같은 장의 패턴 문서로 바로 넘어갈 수 있게 했습니다.

## 학습 순서

| 묶음 | # | 문서 | 다루는 핵심 |
|------|---|------|-----------|
| 점검 | 00-01 | [핵심 질문과 답](00-01.핵심%20질문과%20답.md) | API 묶음 진입 전 자가 점검 |
| 환경 | 01-01 | [API 실습 환경 설정](01-01.API%20실습%20환경%20설정.md) | 후속 모든 절의 전제 — Jenkins URL·계정·플러그인 |
| 개요 | 02-01 | [API 개요와 활용 판단](02-01.API%20개요와%20활용%20판단.md) | API 카테고리, "이게 API 로 풀 문제인가" 판단 기준 |
| 개요 | 02-02 | [REST API 구조와 연동](02-02.REST%20API%20구조와%20연동.md) | URL 체계, 응답 포맷, 외부 시스템 연동 시나리오 |
| 인증 | 03-01 | [인증 API 스펙 (ID-Password + Crumb)](03-01.인증%20API%20스펙%20%28ID-Password%20+%20Crumb%29.md) | Basic 인증, CSRF crumb 발급, 세션 라이프사이클 |
| 인증 | 03-02 | [인증 모델과 TPS 패턴 (2.222+)](03-02.인증%20모델과%20TPS%20패턴%20%282.222+%29.md) | TPS 가 실제 적용하는 인증 흐름 |
| 인증 | 03-03 | [API 토큰 발급·회전·수명 점검](03-03.API%20토큰%20발급·회전·수명%20점검.md) | 토큰 발급 API, 회전 정책, 수명 만료 시 동작 |
| Job | 04-01 | [파이프라인 CRUD API 스펙](04-01.파이프라인%20CRUD%20API%20스펙.md) | createItem·config.xml POST·doDelete |
| Job | 04-02 | [파이프라인 CRUD 모델과 TPS 패턴 (2.222+)](04-02.파이프라인%20CRUD%20모델과%20TPS%20패턴%20%282.222+%29.md) | TPS Job 생성/수정 실제 호출 흐름 |
| Build | 05-01 | [빌드 실행·큐 API 스펙](05-01.빌드%20실행·큐%20API%20스펙.md) | build·buildWithParameters·queue/item 추적 |
| Build | 05-02 | [빌드 실행·큐 모델과 TPS 패턴 (2.222+)](05-02.빌드%20실행·큐%20모델과%20TPS%20패턴%20%282.222+%29.md) | TPS 빌드 트리거의 queueId → buildNumber 전환 |
| Build | 05-03 | [Queue 적재 이후 실행 흐름과 데이터 추적](05-03.Queue%20적재%20이후%20실행%20흐름과%20데이터%20추적.md) | VM/K8s 실행기 차이, TPS 최소 저장 데이터 |
| Build | 05-04 | [큐 내부 흐름과 실행 순서](05-04.큐%20내부%20흐름과%20실행%20순서.md) | 큐 내부 자료구조와 실행 순서 결정 알고리즘 |
| Build | 05-04 | [큐 내부 인터랙티브 시각화](05-04-queue-internals.html) | 시간 흐름 시각화 (HTML) |
| Build | 05-05 | [빌드 중지·취소 API 스펙](05-05.빌드%20중지·취소%20API%20스펙.md) | stop·cancelItem, 취소 동작 |
| Build | 05-06 | [큐·실행기 조회 API 스펙](05-06.큐·실행기%20조회%20API%20스펙.md) | queue·computer, executor 조회 |
| 상태 | 06-01 | [빌드 상태 추적 API 스펙](06-01.빌드%20상태%20추적%20API%20스펙.md) | api/json, lastBuild, result, duration |
| 상태 | 06-02 | [빌드 상태 추적 모델과 TPS 패턴 (2.222+)](06-02.빌드%20상태%20추적%20모델과%20TPS%20패턴%20%282.222+%29.md) | TPS 상태 폴링 vs 콜백 패턴 |
| 상태 | 06-03 | [상태 추적 API 현대화와 Blue Ocean 해석](06-03.상태%20추적%20API%20현대화와%20Blue%20Ocean%20해석.md) | Blue Ocean API 가 노출하는 상태 모델 차이 |
| 로그 | 07-01 | [API 로그 조회와 적재](07-01.API%20로그%20조회와%20적재.md) | consoleText, progressiveText, TPS 적재 패턴 |
| 로그 | 07-02 | [Blue Ocean 폐기 흐름과 wfapi 전환](07-02.Blue%20Ocean%20폐기%20흐름과%20wfapi%20전환.md) | 폐기 사유·시점, UI 대안, stage 조회는 무엇으로 |
| 로그 | 07-03 | [wfapi 상세 스펙과 활용](07-03.wfapi%20상세%20스펙과%20활용.md) | wfapi(workflow API) 의 stage 트리 모델 |
| 로그 | 07-04 | [wfapi 로그 모델과 Blue Ocean 구현 판단](07-04.wfapi%20로그%20모델과%20Blue%20Ocean%20구현%20판단.md) | wfapi vs Blue Ocean — TPS 구현 선택 |
| 크레덴셜 | 08-01 | [API 크레덴셜 관리](08-01.API%20크레덴셜%20관리.md) | credentials API, store/domain 모델 |
| 크레덴셜 | 08-02 | [API 크레덴셜 관리 현대화 (2.222+)](08-02.API%20크레덴셜%20관리%20현대화%20%282.222+%29.md) | 권한 모델, 도메인 분리, upsert 패턴 |
| 크레덴셜 | 08-03 | [SSL 적용과 인증서 관리](08-03.SSL%20적용과%20인증서%20관리.md) | TLS 종단, 자기서명 인증서 처리 |
| 운영 | 09-01 | [API 배포 승인과 운영 관리](09-01.API%20배포%20승인과%20운영%20관리.md) | input step, approval API, 운영 패턴 |
| 운영 | 09-02 | [API 배포 승인과 운영 관리 현대화](09-02.API%20배포%20승인과%20운영%20관리%20현대화.md) | PAUSED_PENDING_INPUT 해석, liveness/readiness |
| 운영 | 09-03 | [API 쿼리 최적화와 운영](09-03.API%20쿼리%20최적화와%20운영.md) | tree/exclude 파라미터, 부하 줄이기 |

처음 진입자는 01-01 환경 설정과 02-01 개요를 먼저 본 뒤, 자기 자동화 목적에 해당하는 묶음(인증/Job/Build/상태/로그/크레덴셜/운영) 으로 점프합니다. TPS 통합 작업자는 각 장의 패턴 문서(`03-02`, `05-02` 등) 부터 보고 막힐 때만 표준 스펙(`03-01`, `05-01`) 으로 거슬러 올라가는 편이 빠릅니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.426.x 이상 | wfapi, blueocean 플러그인 포함 |
| Blue Ocean | 1.27.x | stage 트리 모델 |
| Workflow API | 2.x | wfapi 엔드포인트 |
| TPS | v3.0.5P | 짝 문서의 *TPS 패턴* 적용 대상 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`../01_core/`](../01_core/README.md) 의 Pipeline 기본과 Jenkins 가 빌드를 어떻게 실행하는지를 알고 있습니다.
2. [`../02_security/`](../02_security/README.md) 의 인증·인가 모델을 한 줄로 설명할 수 있습니다.
3. `curl` 또는 비슷한 HTTP 클라이언트로 REST 호출을 보내 본 경험이 있습니다.

위 항목 중 막히는 부분이 있으면 [`../01_core/`](../01_core/README.md), [`../02_security/`](../02_security/README.md) 를 먼저 본 뒤 돌아옵니다.

## 면접 대비 체크리스트

> 묶음을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Jenkins API 에서 CSRF crumb 가 필요한 이유는? crumb 와 API 토큰의 역할 차이는?
2. `build` 와 `buildWithParameters` 가 응답하는 식별자는 무엇입니까? queueId 가 buildNumber 로 전환되는 시점은?
3. `consoleText` 와 `progressiveText` 의 차이는? 적재 측면에서 각각의 약점은?
4. wfapi 가 노출하는 stage 트리는 어떤 자료구조로 보이며, Blue Ocean API 의 응답과 무엇이 다릅니까?
5. `tree=` 와 `exclude=` 파라미터가 호출 부하를 줄이는 메커니즘은?

각 질문에 막히면 해당 절로 돌아갑니다.
