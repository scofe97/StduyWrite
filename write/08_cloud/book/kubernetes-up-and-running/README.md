---
title: Kubernetes — Up and Running, 3rd Edition — 정독 인덱스
tags: [moc, study-index, book, kubernetes, k8s, up-and-running, cloud-native]
status: draft
source:
  - 《Kubernetes: Up and Running, 3rd Edition》(O'Reilly) — 챕터별 PDF
  - https://openlibrary.org/search?q=kubernetes+up+and+running  # 1·2판 서지 확인 (2026-08-17 조회)
related:
  - ../kubernetes-in-action/README.md
  - ../kubernetes-patterns/README.md
  - ../networking-and-kubernetes/README.md
  - ../../kubernetes/README.md
updated: 2026-08-17
---

# Kubernetes — Up and Running, 3rd Edition — 정독 인덱스

> 이 폴더는 『Kubernetes: Up and Running』 3판을 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 PDF를 한 편씩 받아 원문을 1차 자료로 삼고 채워 넣습니다.

## 이 정독본은 형제 세 권과 무엇이 다른가

> 같은 `book/` 아래 Kubernetes 정독본이 이미 셋입니다. 네 번째를 여는 이유를 먼저 적어 둡니다.

이 책은 오브젝트를 **운영자가 실제로 굴리는 최소 경로**로 훑습니다. "이 오브젝트가 왜 있는지"를 길게 논증하기보다 "지금 클러스터에서 이걸 어떻게 만들고 확인하고 되돌리는지"를 먼저 보여 줍니다. 그래서 같은 오브젝트를 다루더라도 형제 정독본과 층이 갈립니다.

[Kubernetes in Action](../kubernetes-in-action/README.md)은 오브젝트를 `kubectl`·YAML로 바닥부터 쌓아 올리는 입문·레퍼런스라 한 오브젝트에 여러 편을 씁니다. [Kubernetes Patterns](../kubernetes-patterns/README.md)는 오브젝트를 이미 아는 독자에게 "이것들을 조합해 어떤 반복 문제를 푸는가"를 패턴 카탈로그로 정리합니다. [Networking and Kubernetes](../networking-and-kubernetes/README.md)는 네트워크 계층 하나를 수직으로 파고듭니다. 이 책은 그 셋과 달리 **폭이 넓고 깊이가 얕은 대신, 운영 동작과 확인 절차가 함께 붙어 있습니다**.

그래서 이 폴더의 편집 방침은 하나입니다. 개념 설명이 형제 노트와 겹치면 여기서 다시 길게 쓰지 않고 링크로 넘기고, **그 책이 운영 관점에서 새로 주는 것만 남깁니다**. 겹침을 감수하고 자립적으로 쓰면 네 번째 K8s 폴더는 중복 더미가 됩니다.



## 장 구성

> 장 번호와 제목은 원서 챕터 PDF에서 그대로 옮겼습니다. 주요 토픽은 각 챕터 도입 문단에서 추출한 것이며, 추측으로 채우지 않았습니다.

이 책은 챕터 앞머리에 "In this chapter we'll cover" 형태의 **학습 목표를 선언하지 않고** 곧바로 산문으로 들어갑니다. 그래서 목표 칸을 따로 두지 않고, 도입 문단이 실제로 무엇을 예고하는지만 적었습니다. 파트 구분도 원서에 없으므로 아래 묶음은 읽기 편하도록 제가 나눈 것입니다.

### 기초 — 컨테이너에서 클러스터까지 (Ch1~4)

| 장 | 제목 | 도입 문단이 예고하는 것 |
|----|------|------------------------|
| 1 | Introduction | Google이 컨테이너로 확장 가능한 시스템을 운영한 경험에서 나온 오케스트레이터라는 출발점 |
| 2 | Creating and Running Containers | 분산 애플리케이션이 결국 개별 머신에서 도는 프로그램들이라는 전제에서 이미지 만들기로 |
| 3 | Deploying a Kubernetes Cluster | 만든 컨테이너를 신뢰할 수 있는 분산 시스템으로 바꾸려면 동작하는 클러스터가 먼저 필요하다는 순서 |
| 4 | Common kubectl Commands | 이후 장에서 계속 쓸 `kubectl`의 공통 명령을 미리 훑기 |

### 워크로드 — Pod에서 Job까지 (Ch5~12)

| 장 | 제목 | 도입 문단이 예고하는 것 |
|----|------|------------------------|
| 5 | Pods | 여러 애플리케이션을 한 머신에 배치되는 원자 단위로 묶어야 하는 실제 배포 상황 |
| 6 | Labels and Annotations | 애플리케이션이 커질 때 "내가 생각하는 묶음"대로 오브젝트를 다루게 해 주는 기본 개념 |
| 7 | Service Discovery | Pod를 배치·재배치하는 동적 시스템에서 대상을 찾는 문제 |
| 8 | HTTP Load Balancing with Ingress | 7장의 노출 방식으로 부족한 사용자·사례를 위한 HTTP 계층 |
| 9 | ReplicaSets | 일회성 Pod가 아니라 여러 복제본이 필요한 이유(중복·장애 감내 등) |
| 10 | Deployments | Pod·ReplicaSet·Service를 조합해 실제 서비스를 만들고 갱신하기 |
| 11 | DaemonSets | 복제의 다른 목적 — 모든 노드마다 Pod를 하나씩 두는 경우 |
| 12 | Jobs | 계속 도는 프로세스가 아니라 끝나는 작업 |

### 설정·보안·확장 (Ch13~20)

| 장 | 제목 | 도입 문단이 예고하는 것 |
|----|------|------------------------|
| 13 | ConfigMaps and Secrets | 같은 이미지를 개발·스테이징·운영에 재사용하려면 런타임에 무엇을 특화해야 하는가 |
| 14 | Role-Based Access Control for Kubernetes | 거의 모든 클러스터가 RBAC을 켜 두었지만 무엇을 위한 것인지 이해할 기회는 적었다는 문제 제기 |
| 15 | Service Meshes | 컨테이너 다음으로 클라우드 네이티브와 동의어가 된 용어의 실체 정리 |
| 16 | Integrating Storage Solutions and Kubernetes | 상태를 분리해도 결국 어딘가에는 남는 상태를 다루기 |
| 17 | Extending Kubernetes | 핵심 API 바깥의 도구·유틸리티를 API 오브젝트로 표현하기 |
| 18 | Accessing Kubernetes from Common Programming Languages | 선언적 YAML 대신 코드에서 API를 직접 다뤄야 하는 상황 |
| 19 | Securing Applications in Kubernetes | 운영에서 널리 쓰이기 위해 필요한 보안 중심 API들 |
| 20 | Policy and Governance for Kubernetes Clusters | 리소스가 수십에서 수백으로 늘어날 때 생기는 통제 문제 |

### 규모 확장 (Ch21~22, 부록)

| 장 | 제목 | 도입 문단이 예고하는 것 |
|----|------|------------------------|
| 21 | Multicluster Application Deployments | 한 클러스터에서 앱을 운영하는 복잡도를 지나 여러 클러스터로 |
| 22 | Organizing Your Application | 책 전체에서 다룬 구성 요소들을 실제 애플리케이션으로 조직하기 |
| A | Building Your Own Kubernetes Cluster | Raspberry Pi 같은 저가 보드로 베어메탈 클러스터를 직접 만들어 보기 |



## 작성된 정독 노트

> 원문 PDF를 받은 장만 채웁니다. 받지 않은 장은 이 표에 올리지 않습니다.

| 편 | 제목 | 상태 |
|----|------|------|
| [07-01](./07-01.Service%20Discovery%20%E2%80%94%20DNS%EA%B0%80%20%EB%AA%BB%20%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%B0%94%EA%B9%A5%EC%9D%84%20%EC%9E%87%EB%8A%94%20%EB%B2%95.md) | Service Discovery — DNS가 못 하는 일과 바깥을 잇는 법 (Ch7) | 완료 · 델타 |
| [14-01](./14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md) | RBAC — 인가를 설계하고 운영하는 법 (Ch14) | 완료 |

"델타" 표시는 기존 노트와 겹침이 커서 **이 책이 새로 주는 것만** 남긴 편이라는 뜻입니다. 그 편의 맨 아래 위임 표가 나머지를 어디서 읽을지 가리킵니다.



## 학습 상태

> 세션을 시작할 때 읽는 칸입니다. 정독본은 `STATE.md`를 따로 두지 않으므로 이 표가 그 역할을 합니다.

| 항목 | 현재 값 |
|------|---------|
| 현재 난이도 레벨 (ZPD) | 기본 — 관심 있는 장부터 선택 진행 |
| 막힌 지점 | 기록 전 |
| 다음 레슨 후보 | 미정 — 다음 챕터 PDF를 받는 시점에 결정 |
| 최근 검증 결과 | 7장 — 전항 통과, 원문 오류·버전 차이 4건 병기, 적대적 검증 지적 5건 반영 · 14장 — 전항 통과, 원문 오류 5건 병기, 지적 4건 반영 |
| 복습 회차 (_review) | 미개시 |

14장에서 원서 오류가 다섯 나왔습니다. 그중 하나는 보안 권고가 뒤집히는 문장이고 둘은 그대로 옮겨 적으면 동작하지 않는 식별자입니다. 모두 노트에 `> **원문 정오**` 로 병기했습니다. 다음 장을 읽을 때도 공식 문서 대조를 같은 강도로 겁니다.

이 시리즈는 1장부터 순서대로가 아니라 **필요한 장을 골라 진행**합니다. 14장이 첫 편인 이유도 그것입니다. 순서를 따라 쌓아 올리는 학습은 형제 정독본 [Kubernetes in Action](../kubernetes-in-action/README.md)이 이미 맡고 있습니다.



## 번호 체계

> 파일명은 `NN-MM.제목.md` 형식입니다. `NN`은 원서 장 번호, `MM`은 한 장을 여러 편으로 나눌 때의 편 순번입니다.

한 장이 800줄을 넘길 것 같으면 개념 단위로 나눠 같은 장 번호 아래 편 번호를 늘립니다. 부록은 `A`가 아니라 장 번호를 이어 붙이지 않고 별도 판단합니다.

흐름·관계·상태 전이 도식은 이 폴더의 `_assets/`에 Archify JSON을 SSOT로 두고 SVG를 본문에 삽입합니다. 원서에 도식이 없는 장이 많아 대부분 새로 그리게 됩니다.



## 개념 노트와의 관계

> 개념이 겹치면 여기서 다시 설명하지 않고 `../../kubernetes/`의 개념 노트로 링크를 겁니다.

RBAC처럼 이미 여러 문서가 다룬 주제는 축을 나눠 씁니다. 클러스터 보안 전체에서의 위치는 개념 노트 [07-01.RBAC과 보안](../../kubernetes/07_security/07-01.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md)이, 권한 설계 판단은 [Kubernetes Patterns 26-01.Access Control](../kubernetes-patterns/26-01.Access%20Control%20%E2%80%94%20RBAC%EC%9C%BC%EB%A1%9C%20%EB%88%84%EA%B0%80%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8A%94%EC%A7%80.md)이 맡고, 이 폴더는 **만든 권한을 검증·버전관리·복구하는 운영 축**을 맡습니다. 같은 판단을 다른 장에도 적용합니다.



## 관련 문서

> 같은 `book/` 영역의 형제 정독본과, 이 책이 링크로 위임하는 개념 노트입니다.

- [Kubernetes in Action, 2판 정독 인덱스](../kubernetes-in-action/README.md) — 오브젝트를 바닥부터 쌓는 입문·레퍼런스 정독본
- [Kubernetes Patterns, 2판 정독 인덱스](../kubernetes-patterns/README.md) — 오브젝트 조합으로 반복 문제를 푸는 패턴 카탈로그
- [Networking and Kubernetes 정독 인덱스](../networking-and-kubernetes/README.md) — 네트워크 계층 수직 심화
- [08_cloud/kubernetes — Kubernetes 실전 운영](../../kubernetes/README.md) — 개념 축 노트 인덱스



## 출처 확인 메모

> 서지 정보 중 확인하지 못한 항목을 남겨 둡니다. 추측으로 채우지 않습니다.

확인한 것과 확인하지 못한 것을 나눠 둡니다.

- **확인함**: 책 제목과 판차. 원서 챕터 PDF 본문에서 읽었습니다
- **확인함**: 발행사 O'Reilly. PDF와 Open Library 양쪽에 있습니다
- **확인함**: 1·2판 저자는 Brendan Burns · Joe Beda · Kelsey Hightower입니다
- **확인 못 함**: 3판의 저자 구성과 발행 연도입니다

O'Reilly 도서 페이지는 접근이 차단됩니다(HTTP 403). Open Library에는 1판과 2판 기록만 있고 3판 항목이 없습니다. 판이 바뀌며 저자가 추가되거나 교체되는 일이 흔하므로 1·2판 저자를 3판 저자로 옮겨 적지 않았습니다. 확인되면 프론트매터 `source`를 채웁니다.
