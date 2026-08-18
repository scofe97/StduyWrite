---
title: 04_networking — 네트워킹
tags: [moc, kubernetes, service, dns, ingress, gateway-api, networkpolicy, dual-stack]
status: final
source:
  - https://kubernetes.io/docs/concepts/services-networking/
related:
  - ../README.md
updated: 2026-08-06
---

# 04_networking — 네트워킹
---
> Pod IP가 바뀐다는 전제에서 출발해 Linux 네트워크, Service discovery, 트래픽 정책, 외부 진입, 혼합 OS 운영 순서로 학습합니다. 04-01에서 전체 지도를 잡고 04-02부터 04-10까지 구현과 정책을 확장합니다.



## 권장 학습 순서
> 04-01~04-03은 패킷 경로의 기반을, 04-04~04-10은 Kubernetes 공식 Services, Load Balancing, and Networking 개념을 다룹니다.

| 번호 | 본문 | 점검 | 학습 초점 |
|------|------|------|-----------|
| 04-01 | [네트워킹](04-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | 본문 내 점검 | 전체 책임 경계와 장애 진입 순서를 고정합니다. |
| 04-02 | [Pod 네트워크와 Linux 기반](04-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) | 본문 내 점검 | netns·veth·Pod CIDR·CNI·Service dataplane을 연결합니다. ([시각화](04-02-pod-network.html)) |
| 04-03 | [오버레이와 노드 간 트래픽](04-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | 본문 내 점검 | VXLAN·네이티브 라우팅·BGP·MetalLB를 비교합니다. ([시각화](04-03-overlay-bgp.html)) |
| 04-04 | [Service와 EndpointSlice](04-04.Service%EC%99%80%20EndpointSlice.md) | 본문 내 점검 | Service 타입, backend 추적, ClusterIP 할당, 내부 트래픽 정책을 다룹니다. |
| 04-05 | [DNS와 CoreDNS](04-05.DNS%EC%99%80%20CoreDNS.md) | 본문 내 점검 | Service·Pod DNS 레코드와 이름 해석 정책을 다룹니다. |
| 04-06 | [Ingress와 Gateway API](04-06.Ingress%EC%99%80%20Gateway%20API.md) | 본문 내 점검 | Ingress, Controller, Gateway API의 선언과 구현 경계를 다룹니다. |
| 04-07 | [NetworkPolicy](04-07.NetworkPolicy.md) | 본문 내 점검 | ingress·egress 격리와 additive 허용 모델을 다룹니다. |
| 04-08 | [IPv4와 IPv6 이중 스택](04-08.IPv4%EC%99%80%20IPv6%20%EC%9D%B4%EC%A4%91%20%EC%8A%A4%ED%83%9D.md) | 본문 내 점검 | Pod·Service IP family 정책과 전환 제약을 다룹니다. |
| 04-09 | [토폴로지 인지 라우팅](04-09.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EC%9D%B8%EC%A7%80%20%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | 본문 내 점검 | EndpointSlice hint와 zone 선호·fallback을 다룹니다. |
| 04-10 | [Windows 네트워킹](04-10.Windows%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | 본문 내 점검 | HNS·HCS·Windows CNI와 Linux 대비 제약을 다룹니다. |

각 본문의 점검 절에서는 정답을 바로 확인하기 전에 질문에 먼저 답합니다. 이렇게 하면 익숙함과 실제 기억 인출을 분리할 수 있습니다.



## Kubernetes v1.36 공식 문서 커버리지
> Services, Load Balancing, and Networking의 직접 하위 페이지 12개를 하나의 로컬 정본에 대응시켜 누락과 중복을 방지합니다.

| 공식 페이지 | 주요 개념 | 로컬 정본 |
|---------------|-----------|-------------|
| [Service](https://kubernetes.io/docs/concepts/services-networking/service/) | Service 타입·port·VIP·headless Service | [04-04 Service와 EndpointSlice](04-04.Service%EC%99%80%20EndpointSlice.md) |
| [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) | HTTP(S) host·path 라우팅 | [04-06 Ingress와 Gateway API](04-06.Ingress%EC%99%80%20Gateway%20API.md) |
| [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) | Ingress 규칙을 구현하는 controller | [04-06 Ingress와 Gateway API](04-06.Ingress%EC%99%80%20Gateway%20API.md) |
| [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) | GatewayClass·Gateway·Route 책임 분리 | [04-06 Ingress와 Gateway API](04-06.Ingress%EC%99%80%20Gateway%20API.md) |
| [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/) | backend endpoint·condition·slice 분할 | [04-04 Service와 EndpointSlice](04-04.Service%EC%99%80%20EndpointSlice.md) |
| [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) | Pod ingress·egress 격리와 허용 합집합 | [04-07 NetworkPolicy](04-07.NetworkPolicy.md) |
| [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) | Service·Pod DNS 레코드와 정책 | [04-05 DNS와 CoreDNS](04-05.DNS%EC%99%80%20CoreDNS.md) |
| [IPv4/IPv6 dual-stack](https://kubernetes.io/docs/concepts/services-networking/dual-stack/) | `ipFamilyPolicy`·`ipFamilies`·ClusterIP 순서 | [04-08 IPv4와 IPv6 이중 스택](04-08.IPv4%EC%99%80%20IPv6%20%EC%9D%B4%EC%A4%91%20%EC%8A%A4%ED%83%9D.md) |
| [Topology Aware Routing](https://kubernetes.io/docs/concepts/services-networking/topology-aware-routing/) | EndpointSlice zone hint·휴리스틱·fallback | [04-09 토폴로지 인지 라우팅](04-09.%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%20%EC%9D%B8%EC%A7%80%20%EB%9D%BC%EC%9A%B0%ED%8C%85.md) |
| [Networking on Windows](https://kubernetes.io/docs/concepts/services-networking/windows-networking/) | HNS·HCS·Windows CNI·Service 제약 | [04-10 Windows 네트워킹](04-10.Windows%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) |
| [Service ClusterIP allocation](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/) | 동적·정적 ClusterIP 할당과 충돌 | [04-04 Service와 EndpointSlice](04-04.Service%EC%99%80%20EndpointSlice.md) |
| [Service Internal Traffic Policy](https://kubernetes.io/docs/concepts/services-networking/service-traffic-policy/) | `internalTrafficPolicy: Local`과 로컬 endpoint 부재 | [04-04 Service와 EndpointSlice](04-04.Service%EC%99%80%20EndpointSlice.md) |



## 관련 문서
> 이 폴더는 Kubernetes 전체 지도와 Service Mesh의 L7 정책 학습으로 이어집니다.

- [Kubernetes MOC](../README.md) — 스토리지·스케줄링·보안을 포함한 전체 대주제 지도입니다.
- `서비스 메시 기초` <!-- 링크 끊김(2026-08): ../../service-mesh/01_foundation/01-01.서비스 메시 기초.md --> — 기본 연결성 위에 L7 트래픽 정책·mTLS·관측성을 추가합니다.
