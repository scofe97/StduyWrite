---
title: Jenkins Core 학습 MOC
tags: [moc, jenkins, ci-cd, pipeline, declarative]
status: draft
related:
  - ../README.md
  - ../02_security/README.md
  - ../03_agent/README.md
  - ../04_api/README.md
  - ../05_operations/README.md
updated: 2026-05-28
---

# Jenkins Core 학습 MOC

---

> Jenkins 가 실제로 무엇을 제어하는지, 그리고 그 제어 규약을 "코드로" 쓰는 Declarative Pipeline 두 축을 한 폴더에 모았습니다. 본 묶음을 끝내면 "내가 푸시한 커밋이 Jenkins 의 어떤 부품을 거쳐 빌드 실행으로 이어지는가" 와 "그 흐름을 어떻게 텍스트 한 장으로 박제하는가" 에 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

Jenkins 입문에서 가장 자주 막히는 두 지점은 "이게 도대체 어디서 무엇을 한다는 건가" 와 "스크립트가 왜 갑자기 안 돌아가나" 입니다. 앞쪽은 Jenkins 의 제어 영역(빌드 트리거, 실행 컨텍스트, 결과 적재) 이해로 풀리고, 뒤쪽은 Pipeline 문법과 패턴 — 특히 Declarative Pipeline 의 블록 구조 — 으로 풀립니다.

두 주제를 인접한 장 번호로 두면 흐름이 자연스럽습니다. 01장이 "Jenkins 가 무엇을 제어하는가" 를 답하고, 그 위에서 02장이 "그 제어를 어떻게 코드로 표현하는가" 로 이어집니다. 다른 폴더(02_security, 03_agent, 04_api)는 이 두 장을 전제로 합니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 제어 | 01-00 | [점검 — 핵심 질문과 답](01-00.점검.핵심%20질문과%20답.md) | 01장 진입 전 자가 점검 질문 |
| 01 제어 | 01-01 | [Jenkins가 제어하는 것](01-01.Jenkins가%20제어하는%20것.md) | Jenkins 의 제어 영역 — Job, Build, Trigger, Artifact, Workspace |
| 01 제어 | 01-02 | [빌드 요청에서 실행까지](01-02.빌드%20요청에서%20실행까지.md) | 트리거 종류·Queue·Executor·실행 컨텍스트, 한 요청이 결과까지 가는 전체 경로 |
| 02 파이프라인 | 02-00 | [점검 — 핵심 질문과 답](02-00.점검.핵심%20질문과%20답.md) | 02장 진입 전 자가 점검 |
| 02 파이프라인 | 02-01 | [코드로 파이프라인 정의하기](02-01.코드로%20파이프라인%20정의하기.md) | UI 설정 한계, Pipeline as Code 가 등장한 동기, Scripted vs Declarative |
| 02 파이프라인 | 02-02 | [Declarative Pipeline 핵심 구조](02-02.Declarative%20Pipeline%20핵심%20구조.md) | pipeline / agent / stages / steps 블록, 환경·옵션·트리거 |
| 02 파이프라인 | 02-03 | [Pipeline 패턴](02-03.Pipeline%20패턴.md) | 자주 쓰는 합성 패턴 — 매트릭스, 병렬, 조건부, 재사용 |
| 02 파이프라인 | 02-04 | [실패 대응과 파이프라인 원칙](02-04.실패%20대응과%20파이프라인%20원칙.md) | post 블록, retry, timeout, 실패 격리 전략 |

처음 보는 학습자는 01-00 자가 점검부터 풀고 막힌 만큼 01-01·01-02 로 보강합니다. UI 로 Job 을 만들어 본 사람은 02-01 부터 진입해도 흐름이 끊기지 않습니다. 이미 Declarative 를 쓰고 있다면 02-03·02-04 에서 평소 자기 파이프라인의 약한 지점을 점검합니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.426.x 이상 | Pipeline 플러그인 기본 동봉 |
| Pipeline 문법 | Declarative 우선 | Scripted 는 비교 목적으로만 등장 |
| JDK | 17 | Jenkins 2.426+ 의 권장 런타임 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. Git 원격 저장소에 푸시·풀을 해 본 경험이 있습니다.
2. CI/CD 라는 용어를 한 줄로 설명할 수 있습니다 — "코드 변경을 자동으로 빌드·검증·배포한다".
3. 셸 명령(`./gradlew build`, `npm run build` 등) 으로 빌드를 돌려 본 적이 있습니다.

위 셋 중 막히는 항목이 있으면 [`../README.md`](../README.md) 의 Jenkins 입문 자료를 먼저 훑고 돌아오는 편이 빠릅니다.

## 면접 대비 체크리스트

> 두 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Jenkins 가 "제어한다" 는 다섯 가지 대상은 무엇입니까? Workspace 와 Artifact 의 차이는?
2. 한 푸시가 Webhook 으로 들어왔을 때 Executor 가 일을 받기까지 거치는 Queue 단계는 무엇입니까?
3. Scripted Pipeline 과 Declarative Pipeline 의 가장 큰 구조적 차이는? Declarative 가 강제하는 블록 순서는 왜 강제될까요?
4. `agent` 블록을 `pipeline` 레벨에 두는 것과 `stage` 레벨에 두는 것의 차이는?
5. `post { failure { ... } }` 와 `catchError` 는 언제 각각 적절합니까?

각 질문에 막히면 해당 장 본문으로 돌아가서 해당 절을 다시 읽습니다.
