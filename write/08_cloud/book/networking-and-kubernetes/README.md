---
title: Networking and Kubernetes — 정독 인덱스
tags: [moc, study-index, book, kubernetes, networking, linux-networking, cni, kube-proxy]
status: draft
source:
  - 《Networking and Kubernetes: A Layered Approach》(James Strong·Vallery Lancey, O'Reilly, 2021, ISBN 978-1492081654)
  - https://www.amazon.com/Networking-Kubernetes-Approach-James-Strong/dp/1492081655  # 서지 확인 (2026-07-16 조회)
related:
  - ../kubernetes-in-action/README.md
  - ../../kubernetes/README.md
  - ../../service-mesh/README.md
  - ../../README.md
updated: 2026-07-16
---

# Networking and Kubernetes — 정독 인덱스
---
> 이 폴더는 『Networking and Kubernetes: A Layered Approach』(James Strong·Vallery Lancey, O'Reilly, 2021)를 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 PDF를 하나씩 읽은 뒤 한 편씩 채워 넣습니다.

## 이 책을 여기 두는 이유

`08_cloud`는 "클러스터 내부에서 어떻게 돌아가는가"를 다루는 카테고리입니다. 이 책은 그 질문을 네트워킹 축으로 파고듭니다 — TCP/IP와 Linux 네트워킹이라는 바닥에서 출발해, 컨테이너·CNI를 거쳐 kube-proxy·Service·Ingress, 마지막으로 클라우드 관리형 K8s의 네트워크까지 층(layer)을 하나씩 쌓아 올리는 구성입니다. 제목의 "A Layered Approach"가 곧 책의 목차 구조입니다.

같은 폴더의 [『Kubernetes in Action』 정독본](../kubernetes-in-action/README.md)이 오브젝트 중심(무엇을 배포하는가)이라면, 이 책은 패킷 중심(그 오브젝트 사이를 트래픽이 실제로 어떻게 흐르는가)입니다. 그래서 Service·Ingress처럼 겹치는 주제가 나와도 관점이 다릅니다 — 저쪽이 사용법이라면 여기는 구현 원리입니다. 개념이 겹치는 지점은 [`../../kubernetes/`](../../kubernetes/README.md) 개념 노트와 [`../../service-mesh/`](../../service-mesh/README.md)로 링크를 걸어 넘기고, 이 폴더에는 이 책만의 계층 관점과 예제에서 새로 얻는 것만 남깁니다.

## 장별 목표

> 각 장 PDF 앞머리의 저자 선언("In this chapter, we will…")을 근거로 채웠습니다. 원문에 없는 목표를 추측해 넣지 않습니다.

| 장 | 제목 | 저자가 선언한 목표 | 주요 토픽 |
|----|------|------------------|----------|
| 1 | Networking Introduction | 네트워킹 기술·표준의 발전사를 훑고, 지배적 네트워킹 이론을 개관하며, 책 전체 예제의 기반이 될 Go 웹 서버를 소개 | 네트워킹 역사, OSI·TCP/IP 모델, Go 웹 서버 |
| 2 | Linux Networking | K8s 네트워크 스택 이해에 필요한 Linux 네트워킹 기초 — K8s에서 주목할 지점 중심의 스택 개요 | Linux 네트워크 스택, 인터페이스, 네트워크 관리 도구 |
| 3 | Container Networking Basics | 컨테이너의 역사와 실행 옵션·네트워킹 셋업을 살피고, Docker 네트워킹 모델과 CNI의 차이를 설명한 뒤 Docker 네트워킹 모드 예제로 마무리 | 컨테이너 역사, Docker 네트워킹 모델, CNI |
| 4 | Kubernetes Networking Introduction | Pod가 클러스터 내부·외부와 연결되는 방식과 K8s 내부 컴포넌트의 연결을 다룸 — K8s가 푸는 네트워킹 문제 4가지(컨테이너 간·Pod 간·Pod-Service·외부-Service) | Pod 네트워킹, kubelet·kube-proxy, CNI 플러그인 |
| 5 | Kubernetes Networking Abstractions | 서비스 디스커버리와 로드밸런싱 추상화 — 가장 가시적인 네트워크 스택인 Service와 Ingress의 동작 원리 | Service 유형, Endpoints, Ingress |
| 6 | Kubernetes and Cloud Networking | AWS·Azure·GCP의 네트워크 서비스가 그 클라우드 안에서 K8s 클러스터 운영에 필요한 네트워킹에 어떤 영향을 주는지, 각 프로바이더 CNI와 함께 탐구 | AWS·Azure·GCP 네트워크, 관리형 K8s, 클라우드 CNI |

## 작성된 정독 노트

> 원문을 정독해 편을 작성하는 대로 채웁니다. 아직 작성하지 않은 장은 상태만 "작성 예정"으로 표시하고, 본문 내용은 원문 도착 전까지 채우지 않습니다.

| 편 | 제목 | 상태 |
|----|------|------|
| [01-01](./01-01.%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EC%97%AD%EC%82%AC%EC%99%80%20OSI%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EC%9C%BC%EB%A1%9C%20%EB%82%98%EB%88%88%20%EC%9D%B4%EC%9C%A0.md) | 네트워킹 역사와 OSI 모델 — 계층으로 나눈 이유 (Ch1 역사·OSI·TCP/IP 개관) | 완료 |
| [01-02](./01-02.HTTP%EC%97%90%EC%84%9C%20TCP%C2%B7TLS%C2%B7UDP%EA%B9%8C%EC%A7%80%20%E2%80%94%20Transport%20%EA%B3%84%EC%B8%B5%20%ED%95%B4%EB%B6%80.md) | HTTP에서 TCP·TLS·UDP까지 — Transport 계층 해부 (Ch1 Application·Transport) | 완료 |
| [01-03](./01-03.IP%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85%C2%B7Ethernet%20%E2%80%94%20%ED%8C%A8%ED%82%B7%EC%9D%B4%20%EA%B8%B8%EC%9D%84%20%EC%B0%BE%EB%8A%94%20%EB%B2%95.md) | IP·라우팅·Ethernet — 패킷이 길을 찾는 법 (Ch1 Network·Link·재조립) | 완료 |
| [02-01](./02-01.%EC%BB%A4%EB%84%90%EC%9D%B4%20%ED%8C%A8%ED%82%B7%EC%9D%84%20%EB%8B%A4%EB%A3%A8%EB%8A%94%20%EB%B2%95%20%E2%80%94%20%EC%86%8C%EC%BC%93%C2%B7Netfilter%C2%B7Conntrack%C2%B7%EB%9D%BC%EC%9A%B0%ED%8C%85.md) | 커널이 패킷을 다루는 법 — 소켓·Netfilter·Conntrack·라우팅 (Ch2 Basics·Kernel) | 완료 |
| [02-02](./02-02.iptables%C2%B7IPVS%C2%B7eBPF%20%E2%80%94%20kube-proxy%EB%A5%BC%20%EC%9D%B4%ED%95%B4%ED%95%98%EB%8A%94%20%EC%84%B8%20%EA%B8%B0%EC%88%A0.md) | iptables·IPVS·eBPF — kube-proxy를 이해하는 세 기술 (Ch2 High-Level Routing) | 완료 |
| [02-03](./02-03.Linux%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EC%A7%84%EB%8B%A8%20%EB%8F%84%EA%B5%AC%20%E2%80%94%20%EA%B3%84%EC%B8%B5%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%EC%88%98%EC%82%AC%ED%95%98%EA%B8%B0.md) | Linux 네트워크 진단 도구 — 계층 순서대로 수사하기 (Ch2 Troubleshooting Tools) | 완료 |
| [03-01](./03-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%9D%98%20%ED%83%84%EC%83%9D%20%E2%80%94%20%EC%95%B1%20%EC%8B%A4%ED%96%89%EC%9D%98%20%EC%A7%84%ED%99%94%EC%99%80%20%EA%B2%A9%EB%A6%AC%20%ED%94%84%EB%A6%AC%EB%AF%B8%ED%8B%B0%EB%B8%8C.md) | 컨테이너의 탄생 — 앱 실행의 진화와 격리 프리미티브 (Ch3 Intro·Primitives·실습) | 완료 |
| [03-02](./03-02.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%93%9C%EC%99%80%20CNI%20%E2%80%94%20%EA%B2%A9%EB%A6%AC%EC%99%80%20%EC%97%B0%EA%B2%B0%EC%9D%98%20%EA%B1%B0%EB%9E%98.md) | 컨테이너 네트워킹 모드와 CNI — 격리와 연결의 거래 (Ch3 모드·CNM·VXLAN·CNI) | 완료 |
| [03-03](./03-03.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%97%B0%EA%B2%B0%20%EC%8B%A4%EC%8A%B5%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%ED%98%B8%EC%8A%A4%ED%8A%B8%2C%20%EB%8B%A4%EB%A5%B8%20%ED%98%B8%EC%8A%A4%ED%8A%B8.md) | 컨테이너 연결 실습 — 같은 호스트, 다른 호스트 (Ch3 Connectivity) | 완료 |
| [04-01](./04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) | Kubernetes 네트워킹 모델 — Pod IP·레이아웃·Probe (Ch4 Model·Kubelet·Probes) | 완료 |
| [04-02](./04-02.CNI%EC%99%80%20kube-proxy%20%E2%80%94%20Pod%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98%20%EB%B0%B0%EC%84%A0%EA%B3%B5%EA%B3%BC%20%EB%A1%9C%EB%93%9C%EB%B0%B8%EB%9F%B0%EC%84%9C.md) | CNI와 kube-proxy — Pod 네트워크의 배선공과 로드밸런서 (Ch4 CNI·kube-proxy) | 완료 |
| [04-03](./04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) | NetworkPolicy와 DNS — 클러스터 안의 방화벽과 이름 (Ch4 Policy·DNS·Dual Stack) | 완료 |
| [05-01](./05-01.StatefulSet%C2%B7Endpoints%C2%B7EndpointSlices%20%E2%80%94%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%98%20%EC%9E%AC%EB%A3%8C.md) | StatefulSet·Endpoints·EndpointSlices — 서비스의 재료 (Ch5 앞부분) | 완료 |
| [05-02](./05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) | Service 5유형 — ClusterIP에서 LoadBalancer까지 (Ch5 Services) | 완료 |
| [05-03](./05-03.Ingress%EC%99%80%20Service%20Mesh%20%E2%80%94%20L7%EC%9D%98%20%EB%91%90%20%EC%B8%B5.md) | Ingress와 Service Mesh — L7의 두 층 (Ch5 Ingress·Service Meshes) | 완료 |
| [06-01](./06-01.AWS%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%EA%B3%BC%20EKS%20%E2%80%94%20VPC%20%EB%B6%80%ED%92%88%EC%9C%BC%EB%A1%9C%20%EC%A1%B0%EB%A6%BD%ED%95%98%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0.md) | AWS 네트워킹과 EKS — VPC 부품으로 조립하는 클러스터 (Ch6 AWS) | 완료 |
| [06-02](./06-02.GCP%C2%B7Azure%EC%99%80%203%EC%82%AC%20%EB%B9%84%EA%B5%90%20%E2%80%94%20%EA%B0%99%EC%9D%80%20%EB%AC%B8%EC%A0%9C%2C%20%EB%8B%A4%EB%A5%B8%20%EA%B8%B0%EB%B3%B8%EA%B0%92.md) | GCP·Azure와 3사 비교 — 같은 문제, 다른 기본값 (Ch6 GCP·Azure·비교) | 완료 |
| [00-01](./00-01.%EC%9A%A9%EC%96%B4%EC%A7%91.md) | 용어집 — 핵심 용어 + 한 문장 정의 + 등장 편 (시리즈 산출물) | 완료 |
| [00-02](./00-02.%EA%B2%B0%EC%A0%95%20%EC%B9%98%ED%8A%B8%EC%8B%9C%ED%8A%B8.md) | 결정 치트시트 통합본 — 17편의 판단 규칙 모음 (시리즈 산출물) | 완료 |

## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다. 정독본의 STATE.md 대용입니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 6/6 장 완주 — 정독 노트 17편 + 시리즈 산출물 2편(용어집·결정 치트시트) |
| 난이도 레벨 | 6장은 3사 대응이 핵심 — EKS 최대 Pod 공식·VPC-native/NEG·kubenet vs Azure CNI가 복습 포인트 |
| 막힌 지점 | 없음 |
| 다음 레슨 후보 | 복습 1회차 — 00-02 결정 치트시트로 판단 규칙 회상 후 막히는 편 재독 |
| 최근 검증 결과 | 6장 §16 통과(한다체·AI 강조어 0, 시각화 각 1+, 링크 깨짐 0), §18 적대 검증 수행 (2026-07-17). 원문 정오 누적 9건 |
| 복습 회차 | 0 |

## 번호 체계와 작성 규약

파일명은 `NN-MM.제목.md` 형식입니다. `NN`은 책의 장 번호, `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다. 모든 장이 45~64쪽으로 길기 때문에 장마다 PDF 목차를 보고 분할안을 정한 뒤 작성합니다. 정밀 도식은 `_assets/`에 SVG로 두고, 흐름·관계는 Mermaid로 본문에 직접 그립니다.

작성 규약은 writing 스킬의 책 요약 템플릿(07-04)과 정독 노트 세션 규약(07-04b)을 따르되, 한 가지를 이 책에 맞게 바꿨습니다 — "Spring 앱 개발 관점" 섹션은 매 장 필수가 아니라 **Spring 접점이 자연스러운 장에만 선별 적용**합니다(합의 2026-07-16). 이 책은 TCP/IP·Linux·CNI 같은 인프라 계층이 본체라, 순수 네트워킹 장에 Spring을 붙이면 연결이 억지스러워지기 때문입니다.

## 관련 문서

- [『Kubernetes in Action, 2판』 정독본](../kubernetes-in-action/README.md) — 같은 `book/` 영역, 오브젝트 중심 관점의 짝
- [08_cloud/kubernetes — 개념 노트](../../kubernetes/README.md) — 개념 중복을 링크로 위임하는 대상
- [08_cloud/service-mesh](../../service-mesh/README.md) — 이 책 이후 계층(L7 프록시·mTLS)을 다루는 이웃 카테고리
