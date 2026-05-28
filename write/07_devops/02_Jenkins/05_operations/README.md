---
title: Jenkins 운영·커스텀 학습 MOC
tags: [moc, jenkins, durability, shared-library, groovy, hook, webhook]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
  - ../03_agent/README.md
  - ../04_api/README.md
updated: 2026-05-28
---

# Jenkins 운영·커스텀 학습 MOC

---

> Jenkins 를 "오래, 안정적으로, 우리 팀에 맞게" 굴리기 위한 두 축 — 내구성·가용성과 공유 라이브러리·Groovy 커스텀·Hook — 을 한 폴더로 모았습니다. 본 묶음을 끝내면 "운영 중 재기동·장애가 발생해도 빌드가 어떻게 살아남는가" 와 "팀 공통 로직을 어떻게 한 곳에 두고 모든 파이프라인이 재사용하게 만드는가" 를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

내구성(구 07, 2편) 만으로는 단독 폴더로 두기에 분량이 적고, 커스텀·Hook(구 09, 9편) 만으로는 "운영" 이라는 맥락이 빠집니다. 두 축은 결국 *팀 단위 운영* 이라는 같은 목적을 가집니다 — 내구성 절이 "장애에도 흐름이 끊기지 않게" 하고, 커스텀 절이 "팀 규칙을 일회성 스크립트가 아닌 공유 자산으로" 옮깁니다. 한 폴더에 두면 "운영을 진지하게 하려면 무엇이 필요한가" 의 답이 한 페이지에 잡힙니다.

01장이 내구성·가용성, 02장이 공유 라이브러리·Groovy·Hook 으로 갈라집니다. 두 장은 독립적이므로 관심 있는 쪽부터 진입해도 됩니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 내구성 | 01-00 | [점검 — 핵심 질문과 답 (내구성)](01-00.점검.핵심%20질문과%20답%20%28내구성%29.md) | 01장 진입 전 자가 점검 |
| 01 내구성 | 01-01 | [Pipeline 내구성과 재기동](01-01.Pipeline%20내구성과%20재기동.md) | durability hint, CPS 직렬화, controller 재기동 시 빌드 복구 |
| 01 내구성 | 01-02 | [가용성 테스트 시나리오](01-02.가용성%20테스트%20시나리오.md) | controller 다운, agent 단절, 디스크 풀 — 실패 주입 시나리오 |
| 02 커스텀·Hook | 02-00 | [점검 — 핵심 질문과 답 (커스텀·Hook)](02-00.점검.핵심%20질문과%20답%20%28커스텀·Hook%29.md) | 02장 진입 전 자가 점검 |
| 02 커스텀·Hook | 02-01 | [공유 라이브러리](02-01.공유%20라이브러리.md) | Shared Library 구조, vars/src/resources, @Library |
| 02 커스텀·Hook | 02-01a | [공유 라이브러리 실전 패턴](02-01a.공유%20라이브러리%20실전%20패턴.md) | 버전 고정, 테스트, 권한 모델 |
| 02 커스텀·Hook | 02-02 | [Jenkins 커스텀이란?](02-02.Jenkins%20커스텀이란.md) | 플러그인 vs 공유 라이브러리 vs Groovy 스크립트 — 경계 결정 |
| 02 커스텀·Hook | 02-03 | [groovy 커스텀터마이징 한계](02-03.groovy%20커스텀터마이징%20한계.md) | CPS 변환의 제약, 직렬화 불가 객체, sandbox |
| 02 커스텀·Hook | 02-04 | [Groovy 기본 문법](02-04.Groovy%20기본%20문법.md) | Closure, MetaClass, Builder — Pipeline 에서 자주 쓰는 부분 |
| 02 커스텀·Hook | 02-04a | [Groovy로 Jenkins 내부 조회하기](02-04a.Groovy로%20Jenkins%20내부%20조회하기.md) | Jenkins.getInstance(), Item·Run 트리 탐색, Script Console |
| 02 커스텀·Hook | 02-05 | [전역 파이프라인 Hook](02-05.전역%20파이프라인%20Hook.md) | Global Pipeline Library, Pre/Post 전역 Hook |
| 02 커스텀·Hook | 02-05a | [RunListener와 FlowExecutionListener](02-05a.RunListener와%20FlowExecutionListener.md) | 빌드 시작·종료·단계 전이 이벤트 후킹 |
| 02 커스텀·Hook | 02-06 | [GCP K8s Jenkins 실전](02-06.GCP%20K8s%20Jenkins%20실전.md) | GCP 환경에서 K8s Jenkins 운영 — 노드 풀, IAM, 비용 |
| 02 커스텀·Hook | 02-06a | [Webhook과 외부 연동](02-06a.Webhook과%20외부%20연동.md) | SCM Webhook, Generic Webhook Trigger, 외부 시스템 콜백 |

내구성 쪽에 관심이 있으면 01-01 부터, 팀 공통 로직을 정리하려면 02-01·02-01a 부터 진입합니다. RunListener 같은 고급 Hook 까지 가는 길은 02-04(Groovy 기본) → 02-05(전역 Hook) → 02-05a(RunListener) 순으로 단계가 자연스럽습니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.426.x 이상 | Pipeline durability, CPS 표준 |
| Groovy | 3.x | CPS 변환 대상 |
| Workflow | 2.x | CPS DSL |
| Generic Webhook Trigger | 1.86+ | 외부 시스템 연동용 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`../01_core/`](../01_core/README.md) 의 Pipeline 기본 구조와 [`../03_agent/`](../03_agent/README.md) 의 실행 환경을 알고 있습니다.
2. Java 또는 Kotlin 같은 JVM 언어 한 종을 읽을 수 있습니다(Groovy 절 진입 조건).
3. 한 번이라도 운영 중 Jenkins controller 재기동을 경험했거나, 그 상황을 상상할 수 있습니다.

위 항목 중 막히는 부분이 있으면 [`../01_core/`](../01_core/README.md), [`../03_agent/`](../03_agent/README.md) 를 먼저 보고 돌아옵니다.

## 면접 대비 체크리스트

> 두 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Pipeline durability hint 세 가지(PERFORMANCE_OPTIMIZED·SURVIVABLE_NONATOMIC·MAX_SURVIVABILITY) 의 트레이드오프는?
2. CPS 변환이 어떤 객체를 직렬화 불가로 만듭니까? 그 한계를 우회하는 패턴은?
3. Shared Library 의 `vars/`, `src/`, `resources/` 가 각각 노출하는 것은 무엇입니까? `@Library` 어노테이션의 버전 고정 권장 이유는?
4. RunListener 와 FlowExecutionListener 가 잡는 이벤트는 어떻게 다릅니까? 둘 다 필요한 시나리오는?
5. Generic Webhook Trigger 와 SCM Webhook 의 차이는? 외부 시스템 콜백이 SCM Webhook 로 풀리지 않는 경우는?

각 질문에 막히면 해당 절로 돌아갑니다.
