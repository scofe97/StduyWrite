---
title: 08_cloud/service-mesh — Service Mesh 실전
tags: [moc, service-mesh, istio, linkerd, cilium, mtls]
status: final
source:
  - ../../../poc/03_CloudNative/03-service-mesh/README.md@8ac9e97
related:
  - ../README.md
  - ../kubernetes/README.md
updated: 2026-05-30
---

# 08_cloud/service-mesh

---

> 마이크로서비스 간 통신 문제(보안·신뢰성·관측성)를 인프라 계층에서 푸는 Service Mesh를, 공통 개념에서 시작해 Linkerd·Istio 두 구현체를 깊이 다루고, 경계 확장과 비교·도입 판단으로 마무리합니다. 주제별로 다섯 폴더에 나눠 담았습니다.

이 카테고리는 Kubernetes 기본 네트워킹 위에 한 층 더 올라가는 영역입니다. Pod 네트워크·Service·Ingress·Gateway API의 기본 연결성과 진입 구조는 [`kubernetes`](../kubernetes/README.md) 카테고리에서 먼저 다루고, 여기서는 그 위에 서비스 간 트래픽 정책·mTLS·관측성을 어떻게 얹는지에 집중합니다.

## 폴더 구성

> 평탄하게 쌓여 있던 28편을 주제별 다섯 폴더로 재편했습니다. 각 폴더의 README가 그 묶음의 진입점(MOC)입니다.

| 폴더 | 다루는 범위 | 진입점 |
|------|------------|--------|
| `01_foundation` | 메시 개념·프록시 모델·Gateway API·mTLS — 구현체 무관 공통 토대 | [README](01_foundation/README.md) |
| `02_linkerd` | 단순함을 무기로 한 Linkerd의 구조·설치·트래픽·보안·관측성 | [README](02_linkerd/README.md) |
| `03_istio` | Envoy 기반 Istio의 설치·구조·트래픽·운영·고급 확장(10장) | [README](03_istio/README.md) |
| `04_extension` | 메시 경계 확장 — 멀티클러스터·VM 통합·Ambient Mesh | [README](04_extension/README.md) |
| `05_comparison` | 세 메시 비교·eBPF·프로덕션 패턴·도입 판단·통합 전략 | [README](05_comparison/README.md) |

## 권장 학습 동선

공통 토대인 [`01_foundation`](01_foundation/README.md)을 먼저 잡습니다. 메시가 푸는 문제, 프록시를 어디 두는가, 트래픽을 무슨 API로 다루는가, 통신 신뢰는 어떻게 자동화하는가 네 가지입니다. 그다음 구현체를 봅니다. 단순함을 먼저 맛보려면 [`02_linkerd`](02_linkerd/README.md), 기능 풍부함과 넓은 제어 표면이 필요하면 [`03_istio`](03_istio/README.md)로 갑니다. 단일 클러스터를 넘어서야 할 때 [`04_extension`](04_extension/README.md)을, 무엇을 고를지 결정해야 할 때 [`05_comparison`](05_comparison/README.md)을 봅니다.

## 문서 구성 규약

각 폴더는 본문(`NN-01`)과 그 짝을 같은 폴더에 인접시켰습니다. 개념 장에는 점검 문서(`NN-00.점검.핵심 질문과 답`)가, 운영 장에는 실습 문서(`NN-02.…실습`)가 붙습니다. 점검은 본문을 읽기 전 자기 수준을 가늠하거나 읽은 뒤 복습하는 용도이고, 실습은 본문 개념을 직접 클러스터에서 확인하는 hands-on 단계입니다. 본문은 `kubectl`·istioctl·linkerd CLI 범용 명령으로 쓰고, 환경 특화 명령은 실습 문서의 `## 실습 환경` 섹션에만 둡니다.

## 실습 환경

기초(`01_foundation`)와 Linkerd·Istio 설치·트래픽 실험은 개인 GCP K8s 클러스터(dev-server 1~3)에서 수행합니다. 멀티클러스터·VM 통합은 추가 GCE VM을 스핀업해 진행합니다. 클러스터 상세는 [`gcp` 스킬 문서](../../../../.claude/skills/gcp/SKILL.md)를 참조합니다.

## 관련 문서

> 본 카테고리의 전제가 되는 kubernetes MOC와 진입 계층 문서를 안내합니다.

- [kubernetes MOC](../kubernetes/README.md) — 본 카테고리의 전제. Pod·Service·Ingress 이해가 선행돼야 합니다.
- [Ingress와 Gateway API](../kubernetes/02_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) — `01_foundation/03-01`과 주제가 겹치며, K8s 진입 계층 관점에서 서술합니다.
