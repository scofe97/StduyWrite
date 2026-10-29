---
title: 04_networking — 네트워킹
tags: [moc, kubernetes, windows]
status: final
source:
  - https://kubernetes.io/docs/concepts/services-networking/
related:
  - ../README.md
updated: 2026-10-29
---

# 04_networking — 네트워킹
---
> 이 폴더에는 book 노트가 다루지 않는 Windows 네트워킹(04-10)만 남아 있습니다. Pod 네트워크·Service·DNS·Ingress·NetworkPolicy 같은 개념은 2026-10-29 정리 때 book 노트로 옮기고 원 문서 9편을 지웠습니다.



## 학습 대상

| 번호 | 본문 | 점검 | 학습 초점 |
|------|------|------|-----------|
| 04-10 | [Windows 네트워킹](04-10.Windows%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | 본문 내 점검 | HNS·HCS·Windows CNI와 Linux 대비 제약을 다룹니다. |

각 본문의 점검 절에서는 정답을 바로 확인하기 전에 질문에 먼저 답합니다. 이렇게 하면 익숙함과 실제 기억 인출을 분리할 수 있습니다.



## Kubernetes v1.36 공식 문서 커버리지
> Services, Load Balancing, and Networking의 직접 하위 페이지 12개가 지금 어느 노트에 있는지 대응시킵니다.

| 공식 페이지 | 주요 개념 | 정본 |
|---------------|-----------|-------------|
| [Service](https://kubernetes.io/docs/concepts/services-networking/service/) | Service 타입·port·VIP·headless Service | [Service 5유형](../../book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) |
| [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) | HTTP(S) host·path 라우팅 | [Ingress](../../book/kubernetes-in-action/12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) |
| [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) | Ingress 규칙을 구현하는 controller | [Ingress](../../book/kubernetes-in-action/12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) |
| [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) | GatewayClass·Gateway·Route 책임 분리 | [Gateway API](../../book/kubernetes-in-action/13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md) |
| [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/) | backend endpoint·condition·slice 분할 | [EndpointSlices](../../book/networking-and-kubernetes/05-01.StatefulSet%C2%B7Endpoints%C2%B7EndpointSlices%20%E2%80%94%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%98%20%EC%9E%AC%EB%A3%8C.md) |
| [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) | Pod ingress·egress 격리와 허용 합집합 | [NetworkPolicy와 DNS](../../book/networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) |
| [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) | Service·Pod DNS 레코드와 정책 | [CoreDNS 레코드](../../book/learning-coredns/06-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%84%A0%EC%96%B8%ED%96%88%EB%8A%90%EB%83%90%EA%B0%80%20%EB%A0%88%EC%BD%94%EB%93%9C%20%EB%AA%A8%EC%96%91%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) |
| [IPv4/IPv6 dual-stack](https://kubernetes.io/docs/concepts/services-networking/dual-stack/) | `ipFamilyPolicy`·`ipFamilies`·ClusterIP 순서 | [NetworkPolicy와 DNS](../../book/networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) |
| [Topology Aware Routing](https://kubernetes.io/docs/concepts/services-networking/topology-aware-routing/) | EndpointSlice zone hint·휴리스틱·fallback | [엔드포인트·DNS·토폴로지](../../book/kubernetes-in-action/11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) |
| [Networking on Windows](https://kubernetes.io/docs/concepts/services-networking/windows-networking/) | HNS·HCS·Windows CNI·Service 제약 | [04-10 Windows 네트워킹](04-10.Windows%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) |
| [Service ClusterIP allocation](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/) | 동적·정적 ClusterIP 할당과 충돌 | [Service 5유형](../../book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) |
| [Service Internal Traffic Policy](https://kubernetes.io/docs/concepts/services-networking/service-traffic-policy/) | `internalTrafficPolicy: Local`과 로컬 endpoint 부재 | [Service 5유형](../../book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) |



## 관련 문서
> 이 폴더는 Kubernetes 전체 지도와 Service Mesh의 L7 정책 학습으로 이어집니다.

- [Kubernetes MOC](../README.md) — 스토리지·스케줄링·보안을 포함한 전체 대주제 지도입니다.
- `서비스 메시 기초` <!-- 링크 끊김(2026-08): ../../service-mesh/01_foundation/01-01.서비스 메시 기초.md --> — 기본 연결성 위에 L7 트래픽 정책·mTLS·관측성을 추가합니다.
