---
title: Cilium Up and Running — 정독 인덱스
tags: [moc, study-index, book, cilium, ebpf, cni, kubernetes, hubble]
status: draft
source:
  - 《Cilium: Up and Running》(Nico Vibert · Filip Nikolic · James Laverack, O'Reilly, 2026, ISBN 979-8-341-62299-9) — 장 단위 PDF 16편
  - 챕터 PDF 폴더 — GoogleDrive/내 드라이브/book/Cilium Up and Running/
  - https://docs.cilium.io/en/stable/
related:
  - ./01-01.Cilium%20은%20eBPF%20데이터패스로%20iptables%20기반%20CNI%20의%20한계를%20넘는다.md
  - ./02-01.Cilium%20은%20에이전트·CNI%20플러그인·오퍼레이터로%20나눠%20노드와%20클러스터를%20맡는다.md
  - ../networking-and-kubernetes/README.md
  - ../istio-in-action/README.md
  - ../../README.md
learning:
  topic: cilium-up-and-running
  scope: durable
  level: 기본
  last_verified:            # Phase 4 자답·_review 회차 미실시 — 원문 대조일로 대신 채우지 않는다
  blocked_count:
  next_lesson: "03-01 Getting Started with Cilium — 3장 원문에서 절 범위를 정한다"
updated: 2026-10-10
---

# Cilium Up and Running — 정독 인덱스

---

> 이 폴더는 『Cilium: Up and Running』(Vibert · Nikolic · Laverack, O'Reilly)을 장 단위로 정독하며 정리하는 책-종속 학습노트입니다. 16장 가운데 1·2장을 먼저 썼습니다.

## 이 책을 여기 두는 이유

> 같은 폴더의 정독본들이 쿠버네티스 네트워킹의 원리와 사이드카 메시를 세웠다면, 이 책은 그 일을 커널 안 eBPF 데이터패스 하나로 옮기면 무엇이 바뀌는지를 맡습니다.

`08_cloud` 는 클러스터 안에서 무엇이 어떻게 돌아가는지를 다루는 카테고리입니다. [『Networking and Kubernetes』 정독본](../networking-and-kubernetes/README.md)은 iptables·IPVS·eBPF 가 무엇인지, CNI 와 kube-proxy 가 Pod 네트워크를 어떻게 잇는지를 이미 다룹니다. [『Istio in Action』 정독본](../istio-in-action/README.md)은 사이드카 프록시를 요청 경로에 얹었을 때 얻는 것과 잃는 것을 다룹니다.

이 책은 두 정독본 사이에 놓입니다. 같은 Pod 연결·서비스 부하 분산·정책·관측을 Cilium 이라는 CNI 하나가 eBPF 프로그램과 맵으로 처리할 때 구성 요소가 어떻게 나뉘고, 무엇을 커널에 두고 무엇을 Envoy 에 넘기는지가 이 폴더의 몫입니다.

경계는 한 문장으로 긋습니다. 개념 자체(iptables 체인, CNI 명세, 사이드카 모델)는 저쪽 정독본으로 링크하고, 여기에는 Cilium 이 그 개념을 어떻게 구현하고 어디서 다르게 결정했는지만 남깁니다.



## 범위와 읽는 순서

> 1·2장이 왜 Cilium 인가와 내부 구성 요소를 세우고, 3장부터 설치·IPAM·데이터패스·서비스·정책·관측을 장마다 하나씩 맡습니다.

| 장 | 제목 | 상태 |
|---|---|---|
| 1 | Why Cilium? | 작성 |
| 2 | Inside Cilium | 작성 |
| 3 | Getting Started with Cilium | 다음 |
| 4 | IP Address Management | — |
| 5 | The Cilium Datapath | — |
| 6 | Service Networking | — |
| 7 | Ingress and Gateway API | — |
| 8 | Performance Networking and Traffic Optimization | — |
| 9 | Multicluster Networking | — |
| 10 | Cluster Access | — |
| 11 | Cluster Egress | — |
| 12 | Network Policy | — |
| 13 | Layer 7 and FQDN Policy | — |
| 14 | Transparent Encryption | — |
| 15 | Observability with Hubble | — |
| 16 | Operations | — |

장 제목은 챕터 PDF 파일명에서 옮겼습니다.



## 작성된 정독 노트

> 편마다 원문 장과 한 줄 핵심을 둡니다.

| 편 | 원문 | 한 줄 핵심 |
|---|---|---|
| [01-01 Cilium 은 eBPF 데이터패스로 iptables 기반 CNI 의 한계를 넘는다](./01-01.Cilium%20은%20eBPF%20데이터패스로%20iptables%20기반%20CNI%20의%20한계를%20넘는다.md) | 1장 | eBPF 맵 조회가 iptables 규칙의 선형 탐색을 대신하고, CNI 하나가 서비스·Ingress·정책·암호화·관측까지 맡게 된 흐름 |
| [02-01 Cilium 은 에이전트·CNI 플러그인·오퍼레이터로 나눠 노드와 클러스터를 맡는다](./02-01.Cilium%20은%20에이전트·CNI%20플러그인·오퍼레이터로%20나눠%20노드와%20클러스터를%20맡는다.md) | 2장 | 패킷 처리가 필요한 노드 영역(에이전트·CNI 플러그인·Envoy·DNS 프록시)과 전역 일관성이 필요한 클러스터 영역(오퍼레이터·Hubble Relay)을 나눈 구성 |



## 학습 상태

> 세션을 새로 열 때 이 표부터 읽습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 1~2장 완료 (장마다 1편) |
| 난이도 레벨 | 기본. 학습자 자답 전이라 조정 근거는 아직 없습니다 |
| 막힌 지점 | 아직 없음 |
| 다음 레슨 후보 | 03-01 — 3장 설치. 절 범위는 원문을 읽고 정합니다 |
| 최근 검증 결과 | 2026-10-10 2편 작성. 원문·docs.cilium.io·소스와 대조하는 적대적 검증에서 1차 오류 16건과 의심 16건이 나왔습니다. Hubble Relay 포트, Envoy DaemonSet 기본값 전환 버전, ipcache 맵 이름과 종류 등을 고쳤고, 재검증과 최종 검증 뒤 미해결 0입니다. 게이트 실패 0, 도식 11장 글자 예산 통과 |
| 복습 회차 | 없음 |



## 출처와 톤

- 원문(챕터 PDF)이 1차 자료입니다. 사실·수치·이름은 원문에서만 가져오고, 책 밖 보강은 [Cilium 공식 문서](https://docs.cilium.io/en/stable/) 같은 1차 자료를 그 사실이 쓰이는 절에 링크로 녹입니다.
- 노트는 책 없이 읽히게 씁니다. 본문에 그림 번호·쪽·절 번호 같은 책 지칭을 두지 않고, 출처는 frontmatter 와 `## 참고 자료` 에만 적습니다.
- 책과 현재 동작이 다르면 그 절의 설명 안에 현재 동작을 1차 자료 링크와 함께 씁니다.
- 톤은 합니다체입니다. 도식 생성기는 `_assets/_gen/` 에 있고 `_assets/` 에서 실행합니다. `dd.py` 는 TII 정독본 `_assets/dd.py` 의 사본입니다.
- 이 저장소의 원격은 공개 저장소이므로 클러스터 실습을 붙일 때 사내 주소·이름을 쓰지 않습니다.
