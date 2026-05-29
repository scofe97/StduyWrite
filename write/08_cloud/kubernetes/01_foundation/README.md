---
title: Kubernetes Foundation 학습 MOC
tags: [moc, kubernetes, pod, deployment, storage, foundation]
status: draft
related:
  - ../README.md
  - ../02_networking/README.md
  - ../03_platform/README.md
updated: 2026-05-30
---

# Kubernetes Foundation 학습 MOC

---

> 클러스터를 직접 띄우고, 그 위에서 가장 먼저 마주치는 세 가지 — 워크로드를 어떻게 굴리고(Pod·Deployment), 어떻게 노출하며(Service), 상태를 어디에 두는가(Storage) — 를 한 폴더에 모았습니다. 이 묶음을 끝내면 "내 컨테이너 하나가 클러스터 위에서 실행되어 외부에서 닿기까지 어떤 리소스를 거치는가" 에 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

Kubernetes 입문에서 가장 먼저 필요한 것은 실습할 클러스터입니다. 클러스터가 없으면 어떤 개념도 손으로 확인할 수 없기 때문에 로컬 클러스터 구성(01)을 맨 앞에 둡니다. 클러스터가 생기면 그 위에 무엇을 올릴지가 문제이고, 그 답이 Pod·Deployment·Service 같은 핵심 워크로드(02)입니다. 워크로드가 재시작되어도 데이터가 살아남아야 하는 순간 스토리지(03)가 등장합니다.

세 주제는 "클러스터를 띄우고 → 워크로드를 올리고 → 상태를 보존한다" 는 한 줄의 흐름으로 이어집니다. 다른 폴더(02_networking 이후)는 이 세 가지를 안다고 전제하므로 가장 먼저 읽는 묶음으로 두었습니다.

## 학습 순서

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 01 | [로컬 클러스터 구성](01-01.%EB%A1%9C%EC%BB%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B5%AC%EC%84%B1.md) | Minikube·KinD로 프로덕션 유사 환경을 빠르게 재현하는 법 |
| 01 | [로컬 클러스터 구성 점검](01-01.%EB%A1%9C%EC%BB%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EA%B5%AC%EC%84%B1%20%EC%A0%90%EA%B2%80.md) | 01장 자가 점검 |
| 02 | [핵심 워크로드](01-02.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | Pod·ReplicaSet·Deployment·Service·ConfigMap·Probe의 역할 분담 |
| 02 | [핵심 워크로드 점검](01-02.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C%20%EC%A0%90%EA%B2%80.md) | 02장 자가 점검 |
| 03 | [스토리지와 상태](01-03.%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%83%81%ED%83%9C.md) | PV·PVC·StorageClass·StatefulSet — Stateful 워크로드 전략 |
| 03 | [스토리지와 상태 점검](01-03.%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%83%81%ED%83%9C%20%EC%A0%90%EA%B2%80.md) | 03장 자가 점검 |

처음 보는 학습자는 01부터 순서대로 읽습니다. 이미 `kubectl run`·`kubectl apply` 로 Pod 를 띄워 본 사람은 02 부터 진입해도 흐름이 끊기지 않습니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. 컨테이너와 이미지의 차이를 한 줄로 설명할 수 있습니다 — "이미지는 정적 패키지, 컨테이너는 그 실행 인스턴스".
2. `docker run` 으로 컨테이너를 띄워 본 경험이 있습니다.
3. YAML 문법(들여쓰기, 리스트, 맵)을 읽을 수 있습니다.

## 면접 대비 체크리스트

> 세 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Pod 와 컨테이너는 무엇이 다릅니까? 왜 Pod 라는 한 단계가 더 필요할까요?
2. Deployment 가 ReplicaSet 을, ReplicaSet 이 Pod 를 관리하는 계층 구조에서 롤링 업데이트는 어느 계층이 책임집니까?
3. ClusterIP·NodePort·LoadBalancer Service 는 각각 언제 적절합니까?
4. Deployment 와 StatefulSet 은 Pod 식별성·스토리지 측면에서 무엇이 다릅니까?
5. PV 와 PVC 의 관계는? StorageClass 의 동적 프로비저닝은 무엇을 자동화합니까?

각 질문에 막히면 해당 장 본문으로 돌아가서 다시 읽습니다.
