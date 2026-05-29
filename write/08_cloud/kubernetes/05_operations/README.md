---
title: Kubernetes Operations 학습 MOC — 운영·스케줄링·관측
tags: [moc, kubernetes, scheduling, rbac, monitoring, autoscaling, cka]
status: draft
related:
  - ../README.md
  - ../04_devtools/README.md
  - ../02_networking/README.md
updated: 2026-05-30
---

# Kubernetes Operations 학습 MOC — 운영·스케줄링·관측

---

> 클러스터를 일단 띄운 뒤 "안정적으로 계속 굴리는" Day-2 운영 주제를 한 폴더에 모았습니다. 유지보수·인증(Ch08), 워크로드를 어디에 어떻게 둘지(Ch09), 관측·보안·자원·스케일링(Ch10)이 차례로 이어집니다. 이 묶음을 끝내면 "운영 중인 클러스터에서 장애를 진단하고, 워크로드를 의도대로 배치하고, 자원과 보안을 통제하는" 실무 감각을 갖추게 됩니다.

## 왜 한 폴더로 묶었는가

Ch08·09·10 은 각각 단독으로는 한 폴더를 이루기엔 작고, 성격은 모두 "운영" 으로 같습니다. 클러스터를 업그레이드하고 인증서를 관리하는 유지보수(Ch08), 스케줄러에게 배치 의도를 전달하는 스케줄링(Ch09), 그리고 관측성·RBAC·자원 관리·오토스케일링(Ch10)은 "Day-1(구축)" 이후 "Day-2(운영)" 단계에서 함께 마주치는 주제입니다. 그래서 하나의 운영 폴더로 합쳤습니다. CKA 시험 범위도 대부분 이 묶음과 겹칩니다.

## 학습 순서

### 운영 심화 (Ch08)

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 08-01 | [클러스터 업그레이드와 ETCD 백업·복구](08-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | kubeadm 업그레이드·etcd 스냅샷 백업/복구 |
| 08-02 | [TLS와 API 접근 보안](08-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | 컨트롤 플레인 PKI — API 서버·etcd·kubelet 인증서 |
| 08-03 | [JSONPath와 kubectl 고급 조회](08-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | 출력 제어·반복 조회 스크립팅 |
| 08-04 | [CKA 대비와 문제 풀이 전략](08-04.CKA%20%EB%8C%80%EB%B9%84%EC%99%80%20%EB%AC%B8%EC%A0%9C%20%ED%92%80%EC%9D%B4%20%EC%A0%84%EB%9E%B5.md) | 시험 범위와 실무 문서 연결 |

### 스케줄링과 배치 (Ch09)

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 09-01 | [스케줄링과 노드 선택](09-01.%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%EA%B3%BC%20%EB%85%B8%EB%93%9C%20%EC%84%A0%ED%83%9D.md) | Filter·Score, nodeAffinity·Taint/Toleration |
| 09-02 | [토폴로지 분산과 중단 정책](09-02.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EB%B6%84%EC%82%B0%EA%B3%BC%20%EC%A4%91%EB%8B%A8%20%EC%A0%95%EC%B1%85.md) | Topology Spread·PDB·PriorityClass·Eviction |
| 09-03 | [배치 워크로드](09-03.%EB%B0%B0%EC%B9%98%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | Job·CronJob·DaemonSet·Init/Sidecar |

### 관측·보안·자원·스케일링 (Ch10)

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 10-01 | [모니터링과 트러블슈팅](10-01.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) | 장애 체계적 진단 — 메트릭·로그·이벤트 |
| 10-02 | [RBAC과 보안](10-02.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md) | RBAC·SA 토큰·Admission·NetworkPolicy |
| 10-03 | [자원 관리](10-03.%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC.md) | Requests/Limits·QoS 클래스 |
| 10-04 | [오토스케일링](10-04.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | HPA·VPA·KEDA 역할 분담 |
| 10-05 | [OOMKilled 사례 분석](10-05.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) | JVM heap vs cgroup 메모리 불일치 (Endowus 사례) |

각 본문에는 같은 이름의 ` 점검.md` 가 짝으로 들어 있습니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`01_foundation`](../01_foundation/README.md)~[`04_devtools`](../04_devtools/README.md) 의 핵심 개념을 익혔습니다.
2. `kubectl get`·`describe`·`logs` 로 클러스터 상태를 조회해 본 경험이 있습니다.
3. 자원(CPU·메모리) 단위(m·Mi·Gi)를 읽을 수 있습니다.

## 면접 대비 체크리스트

> 세 장 묶음을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. kube-scheduler 의 Filter 와 Score 단계는 각각 무엇을 합니까? Taint 와 nodeAffinity 는 어떻게 보완됩니까?
2. PodDisruptionBudget 은 무엇을 막습니까? 노드 드레인 시 어떻게 동작합니까?
3. Requests 와 Limits 의 차이는? QoS 클래스(Guaranteed/Burstable/BestEffort)는 어떻게 갈립니까?
4. HPA·VPA·KEDA 는 각각 무엇을 기준으로 스케일합니까?
5. JVM 컨테이너가 cgroup 메모리 한계를 넘겨 OOMKilled 되는 전형적 원인은?

각 질문에 막히면 해당 장 본문으로 돌아가서 다시 읽습니다.
