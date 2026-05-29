---
title: Kubernetes Platform 학습 MOC — 패키징과 Operator
tags: [moc, kubernetes, helm, kustomize, operator, crd]
status: draft
related:
  - ../README.md
  - ../02_networking/README.md
  - ../04_devtools/README.md
updated: 2026-05-30
---

# Kubernetes Platform 학습 MOC — 패키징과 Operator

---

> 매니페스트를 손으로 한 장씩 관리하는 단계를 넘어, Helm·Kustomize 로 패키징하고 Operator 로 DB·미들웨어의 운영까지 클러스터에 맡기는 두 축을 한 폴더에 모았습니다. 공통 주제는 "선언적으로 워크로드를 다룬다" 입니다. 이 묶음을 끝내면 "반복되는 배포를 어떻게 재사용 가능한 단위로 묶고, Stateful 한 미들웨어의 Day-2 운영을 어떻게 자동화하는가" 에 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

Helm·Kustomize(Ch05)와 Operator(Ch06)는 표면적으로는 다른 도구지만, 둘 다 "원하는 상태를 선언하면 시스템이 맞춰 준다" 는 같은 철학 위에 있습니다. Helm 은 정적인 매니페스트 묶음을 템플릿으로 재사용하고, Operator 는 거기서 한 발 더 나아가 사람이 하던 운영 판단(백업·페일오버·스케일)까지 컨트롤러 코드에 담습니다.

패키징을 먼저 익혀야 Operator 가 배포하는 CR(Custom Resource)이 결국 어떤 매니페스트로 펼쳐지는지 읽을 수 있습니다. 그래서 Ch05(패키징)를 앞에, Ch06(Operator)를 뒤에 두고 한 폴더로 묶었습니다.

## 학습 순서

### 패키지 관리 (Ch05)

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 05-01 | [Helm 기초](05-01.Helm%20%EA%B8%B0%EC%B4%88.md) | 왜 매니페스트 대신 Helm 인가 — Chart·Release·values |
| 05-02 | [Helm 고급](05-02.Helm%20%EA%B3%A0%EA%B8%89.md) | 재사용 가능한 차트 설계 — 템플릿 함수·의존성·hooks |
| 05-03 | [Kustomize](05-03.Kustomize.md) | 템플릿 없이 base/overlay 로 환경 차이 관리 |
| 05-04 | [K8s 환경변수와 Spring 설정 주입](05-04.K8s%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EC%99%80%20Spring%20%EC%84%A4%EC%A0%95%20%EC%A3%BC%EC%9E%85.md) | ConfigMap 환경변수가 Spring YAML 에 적용되는 경로 |

### Operator 패턴과 DB·미들웨어 (Ch06)

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 06-01 | [Operator 패턴](06-01.Operator%20%ED%8C%A8%ED%84%B4.md) | CRD + Controller 연동, reconcile 루프 |
| 06-02 | [MySQL Operator](06-02.MySQL%20Operator.md) | MySQL HA 자동화 |
| 06-03 | [PostgreSQL Operator](06-03.PostgreSQL%20Operator.md) | CloudNativePG 복제·백업 전략 |
| 06-04 | [Redis Operator](06-04.Redis%20Operator.md) | Cluster vs Sentinel 선택 기준 |
| 06-05 | [Kafka Operator](06-05.Kafka%20Operator.md) | Strimzi 로 Kafka 선언적 관리 |
| 06-06 | [Redpanda Operator](06-06.Redpanda%20Operator.md) | Strimzi 와 Redpanda Operator 비교 |

각 본문에는 같은 이름의 ` 점검.md` 가 짝으로 들어 있습니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`01_foundation`](../01_foundation/README.md) 의 Deployment·Service·ConfigMap 을 직접 작성해 봤습니다.
2. YAML 매니페스트를 `kubectl apply` 로 적용해 본 경험이 있습니다.
3. DB 의 복제(replication)·페일오버 개념을 한 줄로 설명할 수 있으면 Ch06 이 수월합니다.

## 면접 대비 체크리스트

> 두 축을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Helm 의 Chart·Release·values 는 각각 무엇입니까? `helm upgrade` 가 보장하는 것은?
2. Helm 과 Kustomize 는 환경별 차이를 다루는 방식이 어떻게 다릅니까?
3. CRD 와 Controller 는 어떻게 연동됩니까? reconcile 루프는 무엇을 반복합니까?
4. Operator 가 "사람이 하던 운영" 을 대신한다는 말의 구체적 예(백업·페일오버)는?
5. Strimzi(Kafka)와 Redpanda Operator 는 운영 모델에서 무엇이 다릅니까?

각 질문에 막히면 해당 장 본문으로 돌아가서 다시 읽습니다.
