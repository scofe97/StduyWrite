---
title: Kubernetes Networking 학습 MOC
tags: [moc, kubernetes, networking, cni, service, dns, ingress]
status: draft
related:
  - ../README.md
  - ../01_foundation/README.md
  - ../03_platform/README.md
updated: 2026-05-30
---

# Kubernetes Networking 학습 MOC

---

> Pod 하나가 다른 Pod 와 통신하고, 끝내 외부 사용자의 요청을 받기까지 트래픽이 거치는 계층을 아래에서 위로 한 폴더에 모았습니다. 이 묶음을 끝내면 "클러스터 밖 브라우저가 친 요청이 어떤 경로로 특정 Pod 안 프로세스에 닿는가" 를 계층별로 설명할 수 있습니다.

## 왜 한 폴더로 묶었는가

네트워킹은 한 장으로 끝내기에 너무 두꺼운 주제라 여섯 편으로 나눴습니다. 다만 여섯 편은 서로 독립이 아니라 한 줄의 계층 상승입니다. Linux 네임스페이스와 veth 같은 커널 기반(02-02)이 맨 아래에 있고, 그 위에 노드를 넘는 오버레이·라우팅(02-03), 변하는 Pod 집합을 안정 진입점으로 묶는 Service(02-04), 이름을 IP 로 푸는 DNS(02-05), 그리고 외부 HTTP 진입을 다루는 Ingress·Gateway(02-06)가 차례로 쌓입니다.

번호 순서대로 읽으면 추상 한 칸씩 위로 올라가므로, 한 편을 건너뛰면 다음 편의 전제가 비어 막힙니다. 그래서 같은 폴더에 묶어 "아래에서 위로" 읽도록 했습니다. 02-01 은 이 여섯 편의 전체 지도 역할을 합니다.

## 학습 순서

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 02-01 | [네트워킹](02-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | Ch04 전체 지도 — 트래픽이 거치는 계층 개관 |
| 02-02 | [Pod 네트워크와 Linux 기반](02-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) | Pause·netns·veth·Pod CIDR·CNI·kube-proxy dataplane ([시각화](02-02-pod-network.html)) |
| 02-03 | [오버레이와 노드 간 트래픽](02-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | VXLAN·네이티브 라우팅·BGP·ECMP·MetalLB ([시각화](02-03-overlay-bgp.html)) |
| 02-04 | [Service와 EndpointSlice](02-04.Service%EC%99%80%20EndpointSlice.md) | ClusterIP·VIP·EndpointSlice·트래픽 정책 |
| 02-05 | [DNS와 CoreDNS](02-05.DNS%EC%99%80%20CoreDNS.md) | Service/Pod DNS 레코드·Headless·CoreDNS ConfigMap |
| 02-06 | [Ingress와 Gateway API](02-06.Ingress%EC%99%80%20Gateway%20API.md) | Ingress·Gateway API·cert-manager TLS 자동화 |

각 본문에는 같은 이름의 ` 점검.md` 가 짝으로 들어 있어 장마다 자가 점검을 할 수 있습니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`01_foundation`](../01_foundation/README.md) 의 Pod·Service 기본 개념을 익혔습니다.
2. IP·포트·TCP/UDP 의 차이를 한 줄로 설명할 수 있습니다.
3. Linux 에서 `ip addr`·`ip route` 출력을 대강 읽을 수 있으면 02-02 가 한결 수월합니다.

## 면접 대비 체크리스트

> 여섯 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. 한 노드 안에서 Pod 두 개는 어떤 커널 장치(veth·bridge)를 거쳐 통신합니까?
2. 노드를 넘는 Pod 트래픽에서 오버레이(VXLAN)와 네이티브 라우팅은 무엇이 다릅니까?
3. Service 의 ClusterIP 는 실재하는 인터페이스입니까, 아니면 kube-proxy/dataplane 규칙입니까?
4. `my-svc.my-ns.svc.cluster.local` 은 어떤 단계를 거쳐 IP 로 해석됩니까?
5. Ingress 와 Gateway API 는 역할 분리·표현력에서 무엇이 다릅니까?

각 질문에 막히면 해당 장 본문으로 돌아가서 다시 읽습니다.
