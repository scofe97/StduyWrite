---
title: Service Mesh 경계 확장 학습 MOC
tags: [moc, service-mesh, istio, multicluster, vm, ambient]
status: final
related:
  - ../README.md
  - ../03_istio/README.md
  - ../05_comparison/README.md
updated: 2026-05-30
---

# Service Mesh 경계 확장 학습 MOC

---

> 단일 클러스터 안에 머물던 메시 경계를 바깥으로 넓히는 세 가지 확장 토픽 — 여러 클러스터, K8s 바깥 VM, 사이드카 없는 Ambient — 을 한 폴더에 모았습니다. 본 묶음을 끝내면 "메시 경계를 어디까지·어떻게 넓힐 수 있고, 그때 각각 무엇을 감수해야 하는가" 를 판단할 수 있습니다.

## 왜 한 폴더로 묶었는가

`03_istio`가 단일 클러스터 안에서의 Istio 운영을 다룬다면, 이 폴더는 그 경계를 넘어서는 순간을 다룹니다. 세 토픽은 "메시의 경계를 어디에 그을 것인가"라는 같은 질문의 세 방향입니다. 멀티클러스터는 경계를 여러 클러스터로 옆으로 넓히고, VM 통합은 K8s 바깥 워크로드까지 아래로 넓히며, Ambient Mesh는 사이드카라는 경계 자체를 노드 단위로 다시 긋습니다.

셋 다 단일 클러스터 운영(03_istio)을 전제로 하므로 그 뒤에 두었습니다. 모두 "더 넓히면 무엇을 얻고 무엇을 잃는가"라는 트레이드오프 판단이 핵심이라, 도입 결정 프레임은 [`05_comparison`](../05_comparison/README.md)의 도입 전략 문서와 함께 봅니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 멀티클러스터 | 01-00 | [점검](01-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28%EB%A9%80%ED%8B%B0%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%29.md) | 01장 진입 전 자가 점검 |
| 01 멀티클러스터 | 01-01 | [멀티클러스터](01-01.%EB%A9%80%ED%8B%B0%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | 메시 경계를 여러 클러스터로 확장 |
| 01 멀티클러스터 | 01-02 | [멀티클러스터 실습](01-02.%EB%A9%80%ED%8B%B0%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%8B%A4%EC%8A%B5.md) | 클러스터 간 연결 hands-on |
| 02 VM 통합 | 02-00 | [점검](02-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28Istio%20VM%20%ED%86%B5%ED%95%A9%29.md) | 02장 진입 전 자가 점검 |
| 02 VM 통합 | 02-01 | [Istio VM 통합](02-01.Istio%20VM%20%ED%86%B5%ED%95%A9.md) | K8s 바깥 워크로드를 메시에 합류 |
| 02 VM 통합 | 02-02 | [VM 통합 실습](02-02.Istio%20VM%20%ED%86%B5%ED%95%A9%20%EC%8B%A4%EC%8A%B5.md) | WorkloadEntry hands-on |
| 03 Ambient | 03-00 | [점검](03-00.%EC%A0%90%EA%B2%80.%ED%95%B5%EC%8B%AC%20%EC%A7%88%EB%AC%B8%EA%B3%BC%20%EB%8B%B5%20%28Istio%20Ambient%20Mesh%29.md) | 03장 진입 전 자가 점검 |
| 03 Ambient | 03-01 | [Istio Ambient Mesh](03-01.Istio%20Ambient%20Mesh.md) | ztunnel·waypoint, 사이드카리스 전환 |
| 03 Ambient | 03-02 | [Ambient Mesh 실습](03-02.Istio%20Ambient%20Mesh%20%EC%8B%A4%EC%8A%B5.md) | Ambient 모드 hands-on |

세 토픽은 독립적이라 관심 순서대로 읽어도 됩니다. 다만 Ambient(03)는 [`02_linkerd`](../02_linkerd/README.md)·`03_istio`의 사이드카 모델을 이해한 뒤 보면 "무엇을 바꾸는가"가 또렷해집니다. 멀티클러스터·VM 실습은 추가 GCE VM 스핀업이 필요합니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Istio | 1.30 (현재 안정) | Ambient 1.24 GA, 멀티클러스터 Ambient는 1.27 알파 |
| Kubernetes | 1.28 이상 | 멀티클러스터는 2개 이상 클러스터 |
| 실습 환경 | 개인 GCP K8s + 추가 GCE VM | [`gcp` 스킬](../../../../.claude/skills/gcp/SKILL.md) |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`03_istio`](../03_istio/README.md)의 설치·아키텍처·트래픽 관리를 이해하고 있습니다.
2. 단일 클러스터에서 Istio mTLS를 적용해 본 경험이 있습니다.

## 면접 대비 체크리스트

> 세 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. 멀티클러스터 메시의 모델(primary-remote vs multi-primary)은 무엇이 다르고 각각 언제 적합합니까?
2. VM을 메시에 합류시킬 때 WorkloadEntry·신원·네트워크 측면에서 무엇이 필요합니까?
3. Ambient Mesh가 사이드카를 ztunnel(L4)과 waypoint(L7)로 쪼갠 이유는? 사이드카리스 전환의 득과 실은?
4. Ambient 멀티클러스터가 아직 알파인 점은 도입 판단에 어떤 영향을 줍니까?

각 질문에 막히면 해당 장으로 돌아갑니다.
