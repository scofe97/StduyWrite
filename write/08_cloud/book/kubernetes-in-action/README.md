---
title: Kubernetes in Action, 2nd Edition — 정독 인덱스
tags: [moc, study-index, book, kubernetes, k8s, kubernetes-in-action]
status: draft
source:
  - 《Kubernetes in Action, Second Edition》(Marko Lukša, Manning, 2025)
  - https://www.manning.com/books/kubernetes-in-action-second-edition  # 원서 (2026-07-01 조회)
  - https://github.com/luksa/kubernetes-in-action-2nd-edition  # 저자 예제 코드 저장소 (2026-07-01 조회)
related:
  - ./01-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%20%E2%80%94%20%EA%B8%B0%EC%9B%90%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md
  - ./01-02.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%EB%8F%84%EC%9E%85%20%ED%8C%90%EB%8B%A8.md
  - ./02-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0.md
  - ./02-02.Kiada%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EB%B9%8C%EB%93%9C%EC%99%80%20%EB%B0%B0%ED%8F%AC.md
  - ./02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md
  - ./03-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0.md
  - ./03-02.%EC%B2%AB%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EB%B0%B0%ED%8F%AC%EC%99%80%20%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md
  - ./09-01.%EB%B3%BC%EB%A5%A8%20%EC%9D%B4%ED%95%B4%EC%99%80%20emptyDir%EB%A1%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B3%B4%EC%A1%B4%ED%95%98%EA%B8%B0.md
  - ./10-01.PV%C2%B7PVC%C2%B7StorageClass%EC%99%80%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D.md
  - ./11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md
  - ./12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md
  - ./13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md
  - ./14-01.ReplicaSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7%EC%86%8C%EC%9C%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md
  - ./15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md
  - ./18-01.Job%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%8B%A4%ED%96%89%C2%B7%EC%83%81%ED%83%9C%C2%B7suspend%C2%B7%EC%9E%90%EB%8F%99%EC%82%AD%EC%A0%9C.md
  - ../ai-infra-gitaiops/README.md
  - ../../kubernetes/README.md
  - ../../README.md
updated: 2026-07-05
---

# Kubernetes in Action, 2nd Edition — 정독 인덱스
---
> 이 폴더는 『Kubernetes in Action, 2판』(Marko Lukša, Manning)을 장·절 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 본문은 원문을 읽은 뒤 한 편씩 채워 넣습니다.



## 이 노트는 개념 노트와 무엇이 다른가

이 노트는 옆 폴더 `08_cloud/kubernetes/`의 개념 노트 27편과 역할이 다릅니다. 개념 노트가 주제 축으로 묶은 **책-비종속 통합본**이라면, 이 폴더는 한 권의 책을 저자가 짠 순서 그대로 따라가며 정리하는 **책-종속 정독본**입니다. 그래서 개념이 겹치는 지점은 여기서 다시 길게 설명하지 않고, 개념 노트로 링크를 걸어 넘깁니다. 이 폴더에는 그 책만의 관점·예제·흐름에서 새로 얻는 것만 남깁니다.

왜 두 축을 나눌까요? 같은 개념이라도 "주제로 검색해 펼쳐 보는 참조용"과 "책 흐름을 따라 처음부터 쌓아 올리는 학습용"은 읽는 목적이 다르기 때문입니다. 정독본은 저자가 개념을 소개한 순서와 예제 맥락이 학습 자체의 일부라서, 그 순서를 흩뜨리지 않고 보존할 때 가치가 큽니다.



## 이 책을 어떻게 읽는가

『Kubernetes in Action』은 쿠버네티스 입문서 중 예제 중심으로 개념을 쌓아 올리는 구성으로 알려져 있습니다. 저자가 만든 예제 앱(Kubia 등)을 클러스터에 올리고, 파드에서 시작해 서비스·볼륨·컨트롤러로 한 겹씩 기능을 붙여 가며 각 오브젝트가 왜 필요한지를 몸으로 익히게 하는 흐름입니다.

이 정독본은 세 가지 렌즈를 함께 씁니다.

1. **개념 + kubectl/YAML 실습.** 각 오브젝트의 정의와 함께 재현 가능한 `kubectl` 명령·매니페스트를 곁들여, 읽고 나서 바로 손으로 확인할 수 있게 합니다.
2. **Spring 앱 배포·운영 렌즈.** 저는 대부분 Spring 위에서 자바를 씁니다. 그래서 K8s 개념이 "Spring Boot 앱을 배포·운영할 때 어떻게 나타나는가"를 한 줄씩 곁들입니다. 단 Actuator·Micrometer 같은 Spring 전용 주제로 본문을 끌고 가지는 않고, 필요하면 `11_spring` 계열로 링크만 겁니다.
3. **원서 예제 충실.** 저자가 든 예제(Kubia 앱 등)를 그대로 따라가며 저자의 설명 흐름을 보존합니다.



## 챕터 인덱스

> 아래 표는 원문을 정독해 편을 작성하는 대로 채웁니다. 아직 작성하지 않은 장은 상태를 "작성 예정"으로만 표시하고, 본문 내용은 원문 도착 전까지 채우지 않습니다.

진행 현황은 **전체 18장 정독 완료(49편)** 입니다. 표는 원서의 주제 흐름을 따라 다섯 묶음으로 나눠 두었습니다. 각 묶음은 쿠버네티스를 배우는 자연스러운 순서 — 무엇인지 이해하고(기초), 컨테이너를 감싸 배포하고(파드), 설정·저장소를 붙이고(데이터), 밖으로 노출하고(네트워킹), 여러 벌을 자동으로 굴리는(컨트롤러) — 를 그대로 따릅니다.

### 기초 — 쿠버네티스란 무엇이고 어떻게 굴러가는가 (Ch1~4)

| 편 | 제목 | 상태 |
|----|------|------|
| [01-01](./01-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%20%E2%80%94%20%EA%B8%B0%EC%9B%90%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | 쿠버네티스란 무엇인가 — 기원과 아키텍처 (Ch1 §1.1~1.2) | 완료 |
| [01-02](./01-02.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%EB%8F%84%EC%9E%85%20%ED%8C%90%EB%8B%A8.md) | 쿠버네티스 도입 판단 (Ch1 §1.3) | 완료 |
| [02-01](./02-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0.md) | 컨테이너와 가상머신 (Ch2 §2.1) | 완료 |
| [02-02](./02-02.Kiada%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EB%B9%8C%EB%93%9C%EC%99%80%20%EB%B0%B0%ED%8F%AC.md) | Kiada 애플리케이션 빌드와 배포 (Ch2 §2.2) | 완료 |
| [02-03](./02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md) | 네임스페이스와 cgroup으로 보는 컨테이너 격리 (Ch2 §2.3) | 완료 |
| [03-01](./03-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0.md) | 쿠버네티스 클러스터 실행하기 (Ch3 §3.1~3.2) | 완료 |
| [03-02](./03-02.%EC%B2%AB%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EB%B0%B0%ED%8F%AC%EC%99%80%20%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | 첫 애플리케이션 배포와 스케일링 (Ch3 §3.3) | 완료 |
| [04-01](./04-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20API%EC%99%80%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EB%A7%A4%EB%8B%88%ED%8E%98%EC%8A%A4%ED%8A%B8%20%EA%B5%AC%EC%A1%B0.md) | 쿠버네티스 API와 오브젝트 매니페스트 구조 (Ch4 §4.1) | 완료 |
| [04-02](./04-02.Node%EC%99%80%20Event%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%ED%95%84%EB%93%9C%20%EC%8B%A4%EC%8A%B5.md) | Node와 Event 오브젝트로 보는 필드 실습 (Ch4 §4.2~4.3) | 완료 |

### 파드 — 워크로드를 감싸 실행·설정하는 최소 단위 (Ch5~8)

| 편 | 제목 | 상태 |
|----|------|------|
| [05-01](./05-01.Pod%20%EC%9D%B4%ED%95%B4%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B7%B8%EB%A3%B9%ED%99%94%EC%99%80%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4.md) | Pod 이해 — 컨테이너 그룹화와 사이드카 (Ch5 §5.1) | 완료 |
| [05-02](./05-02.Pod%20%EC%83%9D%EC%84%B1%EA%B3%BC%20%EC%83%81%ED%98%B8%EC%9E%91%EC%9A%A9.md) | Pod 생성과 상호작용 (Ch5 §5.2~5.3) | 완료 |
| [05-03](./05-03.%EB%A9%80%ED%8B%B0%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7init%C2%B7%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EC%99%80%20%EC%82%AD%EC%A0%9C.md) | 멀티 컨테이너·init·네이티브 사이드카와 삭제 (Ch5 §5.4~5.6) | 완료 |
| [06-01](./06-01.Pod%20%EC%83%81%ED%83%9C%20%E2%80%94%20phase%C2%B7conditions%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%83%81%ED%83%9C.md) | Pod 상태 — phase·conditions·컨테이너 상태 (Ch6 §6.1) | 완료 |
| [06-02](./06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) | liveness·startup probe로 컨테이너 건강 유지 (Ch6 §6.2) | 완료 |
| [06-03](./06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md) | lifecycle hook과 Pod 생애주기 전체 (Ch6 §6.3~6.4) | 완료 |
| [07-01](./07-01.namespace%EB%A1%9C%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A5%BC%20%EA%B0%80%EC%83%81%20%EB%B6%84%ED%95%A0%ED%95%98%EA%B8%B0.md) | namespace로 클러스터를 가상 분할하기 (Ch7 §7.1) | 완료 |
| [07-02](./07-02.label%EA%B3%BC%20label%20selector%EB%A1%9C%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%A1%B0%EC%A7%81%ED%95%98%EA%B8%B0.md) | label과 label selector로 오브젝트 조직하기 (Ch7 §7.2~7.3) | 완료 |
| [07-03](./07-03.field%20selector%EC%99%80%20annotation.md) | field selector와 annotation (Ch7 §7.4~7.5) | 완료 |
| [08-01](./08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md) | command·args와 환경변수 (Ch8 §8.1) | 완료 |
| [08-02](./08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md) | ConfigMap으로 설정 분리하기 (Ch8 §8.2) | 완료 |
| [08-03](./08-03.Secret%EA%B3%BC%20Downward%20API.md) | Secret과 Downward API (Ch8 §8.3~8.4) | 완료 |

### 데이터 — 파드에 저장소를 붙여 상태를 남기는 법 (Ch9~10)

| 편 | 제목 | 상태 |
|----|------|------|
| [09-01](./09-01.%EB%B3%BC%EB%A5%A8%20%EC%9D%B4%ED%95%B4%EC%99%80%20emptyDir%EB%A1%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B3%B4%EC%A1%B4%ED%95%98%EA%B8%B0.md) | 볼륨 이해와 emptyDir로 데이터 보존하기 (Ch9 §9.1~9.2) | 완료 |
| [09-02](./09-02.image%C2%B7hostPath%20%EB%B3%BC%EB%A5%A8.md) | image·hostPath 볼륨 (Ch9 §9.3~9.4) | 완료 |
| [09-03](./09-03.ConfigMap%C2%B7Secret%C2%B7Downward%20API%C2%B7projected%20%EB%B3%BC%EB%A5%A8.md) | ConfigMap·Secret·Downward API·projected 볼륨 (Ch9 §9.5~9.6) | 완료 |
| [10-01](./10-01.PV%C2%B7PVC%C2%B7StorageClass%EC%99%80%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D.md) | PV·PVC·StorageClass와 동적 프로비저닝 (Ch10 §10.1~10.2) | 완료 |
| [10-02](./10-02.%EC%A0%95%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D%EA%B3%BC%20node-local%20%EB%B3%BC%EB%A5%A8.md) | 정적 프로비저닝과 node-local 볼륨 (Ch10 §10.3) | 완료 |
| [10-03](./10-03.PV%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20%EB%A6%AC%EC%82%AC%EC%9D%B4%EC%A6%88%C2%B7%EC%8A%A4%EB%83%85%EC%83%B7%C2%B7ephemeral.md) | PV 관리 — 리사이즈·스냅샷·ephemeral (Ch10 §10.4~10.5) | 완료 |

### 네트워킹 — 파드를 안팎으로 노출하고 트래픽을 라우팅하는 법 (Ch11~13)

| 편 | 제목 | 상태 |
|----|------|------|
| [11-01](./11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md) | Service 기초 — 파드 통신·ClusterIP·세션 어피니티 (Ch11 §11.1) | 완료 |
| [11-02](./11-02.%EC%99%B8%EB%B6%80%20%EB%85%B8%EC%B6%9C%20%E2%80%94%20NodePort%C2%B7LoadBalancer%C2%B7%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%A0%95%EC%B1%85.md) | 외부 노출 — NodePort·LoadBalancer·트래픽 정책 (Ch11 §11.2) | 완료 |
| [11-03](./11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) | 엔드포인트·DNS·토폴로지·readiness (Ch11 §11.3~11.6) | 완료 |
| [12-01](./12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) | Ingress로 여러 서비스를 한 IP에 노출하기 (Ch12 §12.1~12.2) | 완료 |
| [12-02](./12-02.Ingress%20TLS%C2%B7%EC%84%A4%EC%A0%95%C2%B7IngressClass.md) | Ingress TLS·설정·IngressClass (Ch12 §12.3~12.6) | 완료 |
| [13-01](./13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md) | Gateway API 개념과 Gateway 배포 (Ch13 §13.1~13.2) | 완료 |
| [13-02](./13-02.HTTPRoute%20%E2%80%94%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%ED%95%84%ED%84%B0.md) | HTTPRoute — 라우팅과 필터 (Ch13 §13.3) | 완료 |
| [13-03](./13-03.TLS%C2%B7%EA%B8%B0%ED%83%80%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%C2%B7%ED%81%AC%EB%A1%9C%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7mesh.md) | TLS·기타 프로토콜·크로스 네임스페이스·mesh (Ch13 §13.4~13.7) | 완료 |

### 컨트롤러 — 여러 파드를 자동으로 굴리고 업데이트하는 법 (Ch14~18)

| 편 | 제목 | 상태 |
|----|------|------|
| [14-01](./14-01.ReplicaSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7%EC%86%8C%EC%9C%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | ReplicaSet 기초 — 생성·소유·스케일링 (Ch14 §14.1~14.2) | 완료 |
| [14-02](./14-02.ReplicaSet%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20%E2%80%94%20reconciliation%C2%B7%EC%9E%A5%EC%95%A0%EB%B3%B5%EA%B5%AC%C2%B7%EC%82%AD%EC%A0%9C.md) | ReplicaSet 컨트롤러 — reconciliation·장애복구·삭제 (Ch14 §14.3~14.4) | 완료 |
| [15-01](./15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | Deployment 기초 — 생성·pod-template-hash·스케일링 (Ch15 §15.1) | 완료 |
| [15-02](./15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md) | Deployment 업데이트 — Recreate·RollingUpdate·maxSurge (Ch15 §15.2.1~15.2.3) | 완료 |
| [15-03](./15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md) | rollout 제어와 배포 전략 — pause·faulty·rollback·전략 5종 (Ch15 §15.2.4~15.3) | 완료 |
| [16-01](./16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md) | StatefulSet 기초 — Pets vs Cattle·ordinal·headless Service (Ch16 §16.1) | 완료 |
| [16-02](./16-02.StatefulSet%20%EB%8F%99%EC%9E%91%20%E2%80%94%20%EB%AF%B8%EC%8B%B1%20%ED%8C%8C%EB%93%9C%C2%B7%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%C2%B7retention.md) | StatefulSet 동작 — 미싱 파드·노드 장애·스케일·retention (Ch16 §16.2) | 완료 |
| [16-03](./16-03.StatefulSet%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EC%99%80%20Operator%20%E2%80%94%20partition%C2%B7OnDelete%C2%B7CRD.md) | StatefulSet 업데이트와 Operator — partition·OnDelete·CRD (Ch16 §16.3~16.4) | 완료 |
| [17-01](./17-01.DaemonSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%ED%95%98%EB%82%98%C2%B7node%20selector%C2%B7%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8.md) | DaemonSet 기초 — 노드마다 하나·node selector·업데이트 (Ch17 §17.1) | 완료 |
| [17-02](./17-02.%EB%85%B8%EB%93%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8A%B9%EC%88%98%20%EA%B8%B0%EB%8A%A5%20%E2%80%94%20privileged%C2%B7hostPath%C2%B7hostNetwork%C2%B7PriorityClass.md) | 노드 에이전트 특수 기능 — privileged·hostPath·hostNetwork·PriorityClass (Ch17 §17.2) | 완료 |
| [17-03](./17-03.%EB%A1%9C%EC%BB%AC%20daemon%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%20%E2%80%94%20hostPort%C2%B7hostNetwork%C2%B7internalTrafficPolicy.md) | 로컬 daemon 파드 통신 — hostPort·hostNetwork·internalTrafficPolicy (Ch17 §17.3) | 완료 |
| [18-01](./18-01.Job%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%8B%A4%ED%96%89%C2%B7%EC%83%81%ED%83%9C%C2%B7suspend%C2%B7%EC%9E%90%EB%8F%99%EC%82%AD%EC%A0%9C.md) | Job 기초 — 실행·상태·suspend·자동삭제 (Ch18 §18.1.1) | 완료 |
| [18-02](./18-02.Job%20%EB%B3%91%EB%A0%AC%C2%B7%EC%8B%A4%ED%8C%A8%C2%B7%EC%99%84%EB%A3%8C%20%EB%AA%A8%EB%93%9C.md) | Job 병렬·실패·완료 모드 (Ch18 §18.1.2~18.1.4) | 완료 |
| [18-03](./18-03.work%20queue%C2%B7pod%20%ED%86%B5%EC%8B%A0%C2%B7sidecar%C2%B7CronJob.md) | work queue·pod 통신·sidecar·CronJob (Ch18 §18.1.5~18.2) | 완료 |



## 번호 체계

> 파일명은 `NN-MM.제목.md` 형식입니다. `NN`은 책의 장(chapter) 번호, `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다.

한 장이 짧으면 `03-01.서비스와 디스커버리.md` 한 편으로 끝냅니다. 한 장이 길어 800줄을 넘길 것 같으면 개념 단위로 나눠 `02-01.파드와 첫 배포.md`, `02-02.레플리카셋과 셀프힐링.md`처럼 같은 장 번호 아래 편 번호를 늘립니다. 이렇게 하면 Typora 파일 탐색기에서 책 순서대로 정렬되고, 다른 노트에서 `§02-02`처럼 특정 편을 정확히 가리킬 수 있습니다.

정밀 도식이 필요하면 이 폴더의 `_assets/`에 SVG를 두고 본문에서 `!`` <!-- 링크 끊김(2026-08): _assets/파일명.svg -->`로 참조합니다. 흐름·관계·상태 전이는 Mermaid로 본문에 직접 그립니다.



## 개념 노트와의 관계

> 개념이 겹치면 여기서 다시 설명하지 않고 `../../kubernetes/`의 개념 노트로 링크를 겁니다. 이 폴더에는 책만의 관점·예제 차이분만 남깁니다.

예를 들어 파드·워크로드 개념은 개념 노트 [01-02.핵심 워크로드](../../kubernetes/01_workloads/01-01.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md)에, 서비스·디스커버리는 [02-04.Service와 EndpointSlice](../../kubernetes/04_networking/04-04.Service%EC%99%80%20EndpointSlice.md)에 이미 정리돼 있습니다. 책 편을 쓸 때 해당 개념이 나오면 그 편의 `## 관련 문서`에서 이 노트들로 링크하고, 반대로 개념 노트의 `related`에도 이 책 편을 걸어 양방향을 유지합니다. 통째 병합은 하지 않고 링크로만 잇습니다 — 나중에 이 둘을 한 개념으로 합칠지 판단할 때 연결이 끊기지 않게 하기 위해서입니다.



## 관련 문서

> 같은 `book/` 영역의 다른 정독본과, 이 책이 링크로 위임하는 개념 노트 묶음입니다.

- `notiflex-platform 분석 — GitAIOps 실습 저장소 해부` <!-- 링크 끊김(2026-08): ../ai-infra-gitaiops/README.md --> — 같은 `08_cloud/book/` 영역의 다른 책-종속 노트
- [08_cloud/kubernetes — Kubernetes 실전 운영](../../kubernetes/README.md) — 이 책이 개념 중복을 링크로 위임하는 개념 노트 27편의 인덱스
- [Kubernetes in Action 2판 예제 코드 (luksa/kubernetes-in-action-2nd-edition)](https://github.com/luksa/kubernetes-in-action-2nd-edition) — 저자가 공개한 장별 예제 매니페스트·앱 소스
