---
title: 04_networking — 네트워킹
tags: [moc, kubernetes, service, dns, ingress, gateway-api, cni]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 04_networking — 네트워킹

> Pod IP는 바뀐다는 전제에서 출발해, 트래픽이 Linux netns부터 외부 진입까지 어떤 계층을 거쳐 흐르는지 한 단씩 올라갑니다. 파일 번호 순서가 곧 추상화 상승 순서입니다.



## 문서 목록
> 공식 concepts의 Services, Load Balancing, and Networking에 대응합니다. 파일 번호(`04-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 04-01 | [네트워킹](04-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9.md) | 트래픽이 거치는 계층 전체를 조망해 이후 문서의 지도를 그립니다. |
| 04-02 | [Pod 네트워크와 Linux 기반](04-02.Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%99%80%20Linux%20%EA%B8%B0%EB%B0%98.md) | pause·netns·veth·Pod CIDR·CNI·kube-proxy dataplane이 실제로 어떻게 동작하는지 Linux 수준까지 내려가 봅니다. ([인터랙티브 시각화](04-02-pod-network.html)) |
| 04-03 | [오버레이와 노드 간 트래픽](04-03.%EC%98%A4%EB%B2%84%EB%A0%88%EC%9D%B4%EC%99%80%20%EB%85%B8%EB%93%9C%20%EA%B0%84%20%ED%8A%B8%EB%9E%98%ED%94%BD.md) | VXLAN·네이티브 라우팅·BGP·ECMP·MetalLB가 노드 간 Pod 트래픽과 외부 LoadBalancer를 어떻게 만드는지 봅니다. ([인터랙티브 시각화](04-03-overlay-bgp.html)) |
| 04-04 | [Service와 EndpointSlice](04-04.Service%EC%99%80%20EndpointSlice.md) | 변하는 Pod 집합을 안정적인 진입점으로 노출하는 추상화를 EndpointSlice 단위로 봅니다. |
| 04-05 | [DNS와 CoreDNS](04-05.DNS%EC%99%80%20CoreDNS.md) | Service 이름이 어떻게 IP로 해석되는지, CoreDNS가 이름 해석을 어떻게 책임지는지 봅니다. |
| 04-06 | [Ingress와 Gateway API](04-06.Ingress%EC%99%80%20Gateway%20API.md) | 외부 HTTP 트래픽 라우팅이 Ingress에서 Gateway API로 어떻게 진화하고, cert-manager가 인증서를 어떻게 자동화하는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
