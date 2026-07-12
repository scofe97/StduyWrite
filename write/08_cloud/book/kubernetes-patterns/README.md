---
title: Kubernetes Patterns, 2nd Edition — 정독 인덱스
tags: [moc, study-index, book, kubernetes, k8s, patterns, cloud-native]
status: draft
source:
  - 《Kubernetes Patterns, Second Edition》(Bilgin Ibryam·Roland Huß, O'Reilly, 2023)
  - https://www.oreilly.com/library/view/kubernetes-patterns-2nd/9781098131678/  # 원서 (2026-07-12 조회)
  - https://github.com/k8spatterns/examples  # 저자 예제 코드 저장소 (2026-07-12 조회)
related:
  - ./01-01.분산 프리미티브 — OOP·Java 개념을 Kubernetes로.md
  - ../kubernetes-in-action/README.md
  - ../../kubernetes/README.md
  - ../../README.md
updated: 2026-07-12
---

# Kubernetes Patterns, 2nd Edition — 정독 인덱스
---
> 이 폴더는 『Kubernetes Patterns, 2판』(Bilgin Ibryam·Roland Huß, O'Reilly)을 장 단위로 정독하며 정리하는 **책-종속 학습노트**입니다. 챕터 본문은 원문을 읽은 뒤 한 편씩 채워 넣습니다.



## 이 노트는 개념 노트와 무엇이 다른가

이 노트는 옆 폴더 `08_cloud/kubernetes/`의 개념 노트와 역할이 다릅니다. 개념 노트가 주제 축으로 묶은 **책-비종속 통합본**이라면, 이 폴더는 한 권의 책을 저자가 짠 순서 그대로 따라가며 정리하는 **책-종속 정독본**입니다. 그래서 개념이 겹치는 지점은 여기서 다시 길게 설명하지 않고, 개념 노트로 링크를 걸어 넘깁니다. 이 폴더에는 그 책만의 관점·예제·흐름에서 새로 얻는 것만 남깁니다.

같은 `book/` 영역의 형제 정독본 [Kubernetes in Action](../kubernetes-in-action/README.md)과도 성격이 다릅니다. Kubernetes in Action이 각 오브젝트를 `kubectl`·YAML로 처음부터 쌓아 올리는 **입문·레퍼런스**라면, 이 책은 오브젝트를 이미 아는 독자에게 "이 오브젝트들을 조합해 어떤 반복 문제를 어떻게 푸는가"를 **패턴 카탈로그**로 정리합니다. 그래서 두 책은 경쟁이 아니라 층이 다릅니다. Kubernetes in Action에서 익힌 오브젝트가 이 책에서 패턴의 재료로 다시 등장하면, 그 오브젝트 자체 설명은 개념 노트나 in-action 편으로 링크하고 여기서는 패턴의 의도·해법·트레이드오프만 남깁니다.



## 이 책을 어떻게 읽는가

『Kubernetes Patterns』는 GoF 디자인 패턴이 객체지향 설계에서 한 것을, 컨테이너 오케스트레이션 층에서 하려는 책입니다. 각 장이 하나의 패턴이고, 대부분 **문제 → 해법 → 논의(Discussion) → 더 알아보기** 구조를 따릅니다. 저자는 패턴을 몇 개 범주(기초·행위·구조·설정·보안·고급)로 묶어, 비슷한 관심사의 패턴을 나란히 견주게 합니다.

이 정독본은 세 가지 렌즈를 함께 씁니다.

1. **패턴의 의도와 트레이드오프.** 각 패턴이 어떤 반복 문제를 푸는지, 언제 쓰고 언제 피하는지, 곁에 있는 다른 패턴과 어떻게 갈리는지를 결정 기준 중심으로 재조직합니다.
2. **Spring 앱 배포·운영 렌즈.** 저는 대부분 Spring 위에서 자바를 씁니다. 그래서 각 패턴이 "Spring Boot 앱을 배포·운영할 때 어떻게 나타나는가"를 곁들입니다. 1장 Table 1-1이 JVM 로컬 프리미티브를 Kubernetes 분산 프리미티브에 대응시키는 것처럼, 이 책 자체가 이미 Java·JVM 렌즈를 깔고 있어 이 관점이 자연스럽습니다.
3. **원서 예제·매니페스트 충실.** 저자가 든 예제와 YAML을 그대로 따라가며 설명 흐름을 보존하고, 재현 가능한 명령을 곁들입니다.



## 파트·범주 구조

> 아래 범주는 원서의 패턴 묶음을 따릅니다. 정확한 파트 제목·경계는 각 파트 디바이더 PDF를 정독하며 확정합니다(현재는 챕터 흐름에서 유추한 잠정 묶음이라 회색지대로 둡니다).

| 범주 | 다루는 패턴(장) | 관심사 |
|------|----------------|--------|
| 기초 (Foundational) | 1~6 | 컨테이너를 잘 굴리기 위한 전제 — 자원 요구·선언적 배포·헬스·생애주기·배치 |
| 행위 (Behavioral) | 7~14 | 컨테이너·Pod의 실행 방식 — 배치/주기 잡·데몬·싱글턴·상태 유무·디스커버리·자기 인식 |
| 구조 (Structural) | 15~18 | Pod 안 컨테이너를 조직하는 법 — Init·Sidecar·Adapter·Ambassador |
| 설정 (Configuration) | 19~22 | 앱과 설정을 분리하는 법 — EnvVar·ConfigMap/Secret·불변 설정·템플릿 |
| 보안 (Security) | 23~26 | 컨테이너를 안전하게 — 프로세스 격리·네트워크 분할·시크릿·접근 제어 |
| 고급 (Advanced) | 27~30 | 플랫폼을 확장하는 법 — Controller·Operator·오토스케일·이미지 빌드 |



## 챕터 인덱스

> 아래 표는 원문을 정독해 편을 작성하는 대로 채웁니다. 아직 작성하지 않은 장은 상태를 "작성 예정"으로만 표시하고, 본문 내용은 원문 도착 전까지 채우지 않습니다.

진행 현황은 **16장 정독 완료(16편)** 입니다.

### 기초 — 컨테이너를 잘 굴리기 위한 전제 (Ch1~6)

| 편 | 제목 | 상태 |
|----|------|------|
| [01-01](./01-01.%EB%B6%84%EC%82%B0%20%ED%94%84%EB%A6%AC%EB%AF%B8%ED%8B%B0%EB%B8%8C%20%E2%80%94%20OOP%C2%B7Java%20%EA%B0%9C%EB%85%90%EC%9D%84%20Kubernetes%EB%A1%9C.md) | 분산 프리미티브 — OOP·Java 개념을 Kubernetes로 (Ch1) | 완료 |
| [02-01](./02-01.Predictable%20Demands%20%E2%80%94%20%EC%9E%90%EC%9B%90%20%EC%9A%94%EA%B5%AC%EB%A5%BC%20%EC%84%A0%EC%96%B8%ED%95%B4%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | Predictable Demands — 자원 요구를 선언해 스케줄러에 알리기 (Ch2) | 완료 |
| [03-01](./03-01.Declarative%20Deployment%20%E2%80%94%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%C2%B7%EB%A1%A4%EB%B0%B1%EC%9D%84%20%EC%84%A0%EC%96%B8%EC%9C%BC%EB%A1%9C.md) | Declarative Deployment — 업그레이드·롤백을 선언으로 (Ch3) | 완료 |
| [04-01](./04-01.Health%20Probe%20%E2%80%94%20%EC%95%B1%EC%9D%B4%20%EC%9E%90%EA%B8%B0%20%EA%B1%B4%EA%B0%95%EC%9D%84%20%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | Health Probe — 앱이 자기 건강을 플랫폼에 알리기 (Ch4) | 완료 |
| [05-01](./05-01.Managed%20Lifecycle%20%E2%80%94%20%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%9D%98%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EC%97%90%20%EB%B0%98%EC%9D%91%ED%95%98%EA%B8%B0.md) | Managed Lifecycle — 플랫폼의 생애주기 이벤트에 반응하기 (Ch5) | 완료 |
| [06-01](./06-01.Automated%20Placement%20%E2%80%94%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EA%B0%80%20Pod%EB%A5%BC%20%EB%85%B8%EB%93%9C%EC%97%90%20%EB%B0%B0%EC%B9%98%ED%95%98%EB%8A%94%20%EB%B2%95.md) | Automated Placement — 스케줄러가 Pod를 노드에 배치하는 법 (Ch6) | 완료 |

### 행위 — 컨테이너·Pod의 실행 방식 (Ch7~14)

| 편 | 제목 | 상태 |
|----|------|------|
| [07-01](./07-01.Batch%20Job%20%E2%80%94%20%EC%9C%A0%ED%95%9C%ED%95%9C%20%EC%9E%91%EC%97%85%EC%9D%84%20%EC%99%84%EB%A3%8C%EA%B9%8C%EC%A7%80%20%EC%95%88%EC%A0%95%EC%A0%81%EC%9C%BC%EB%A1%9C.md) | Batch Job — 유한한 작업을 완료까지 안정적으로 (Ch7) | 완료 |
| [08-01](./08-01.Periodic%20Job%20%E2%80%94%20CronJob%EC%9C%BC%EB%A1%9C%20%EC%8B%9C%EA%B0%84%20%EC%B6%95%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8B%A4.md) | Periodic Job — CronJob으로 시간 축을 더하다 (Ch8) | 완료 |
| [09-01](./09-01.Daemon%20Service%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%EB%8F%84%EB%8A%94%20%EC%9D%B8%ED%94%84%EB%9D%BC%20Pod.md) | Daemon Service — 노드마다 도는 인프라 Pod (Ch9) | 완료 |
| [10-01](./10-01.Singleton%20Service%20%E2%80%94%20%ED%95%9C%20%EB%B2%88%EC%97%90%20%ED%95%98%EB%82%98%EB%A7%8C%20%ED%99%9C%EC%84%B1%EC%9D%B4%EB%90%98%20%EA%B3%A0%EA%B0%80%EC%9A%A9.md) | Singleton Service — 한 번에 하나만 활성이되 고가용 (Ch10) | 완료 |
| [11-01](./11-01.Stateless%20Service%20%E2%80%94%20%EB%8F%99%EC%9D%BC%C2%B7%EA%B5%90%EC%B2%B4%20%EA%B0%80%EB%8A%A5%ED%95%9C%20replica%EB%A1%9C%20%EC%88%98%ED%8F%89%20%ED%99%95%EC%9E%A5.md) | Stateless Service — 동일·교체 가능한 replica로 수평 확장 (Ch11) | 완료 |
| [12-01](./12-01.Stateful%20Service%20%E2%80%94%20StatefulSet%EC%9C%BC%EB%A1%9C%20%EC%83%81%ED%83%9C%EB%A5%BC%20first-class%EB%A1%9C.md) | Stateful Service — StatefulSet으로 상태를 first-class로 (Ch12) | 완료 |
| [13-01](./13-01.Service%20Discovery%20%E2%80%94%20%EA%B3%A0%EC%A0%95%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%EB%A1%9C%20%EB%8F%99%EC%A0%81%20Pod%EB%A5%BC%20%EC%B0%BE%EA%B8%B0.md) | Service Discovery — 고정 엔드포인트로 동적 Pod를 찾기 (Ch13) | 완료 |
| [14-01](./14-01.Self%20Awareness%20%E2%80%94%20downward%20API%EB%A1%9C%20%EC%9E%90%EA%B8%B0%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%96%BB%EA%B8%B0.md) | Self Awareness — downward API로 자기 메타데이터 얻기 (Ch14) | 완료 |

### 구조 — Pod 안 컨테이너 조직 (Ch15~18)

| 편 | 제목 | 상태 |
|----|------|------|
| [15-01](./15-01.Init%20Container%20%E2%80%94%20%EC%B4%88%EA%B8%B0%ED%99%94%EB%A5%BC%20%EC%95%B1%EA%B3%BC%20%EB%B6%84%EB%A6%AC%ED%95%B4%20%EB%B3%84%EB%8F%84%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%EB%A1%9C.md) | Init Container — 초기화를 앱과 분리해 별도 생애주기로 (Ch15) | 완료 |
| [16-01](./16-01.Sidecar%20%E2%80%94%20%EA%B8%B0%EC%A1%B4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EB%A5%BC%20%EB%B0%94%EA%BE%B8%EC%A7%80%20%EC%95%8A%EA%B3%A0%20%ED%99%95%EC%9E%A5.md) | Sidecar — 기존 컨테이너를 바꾸지 않고 확장 (Ch16) | 완료 |
| — | Adapter — 어댑터 (Ch17) | 작성 예정 |
| — | Ambassador — 앰배서더 (Ch18) | 작성 예정 |

### 설정 — 앱과 설정 분리 (Ch19~22)

| 편 | 제목 | 상태 |
|----|------|------|
| — | EnvVar Configuration — 환경변수 설정 (Ch19) | 작성 예정 |
| — | Configuration Resource — ConfigMap·Secret (Ch20) | 작성 예정 |
| — | Immutable Configuration — 불변 설정 (Ch21) | 작성 예정 |
| — | Configuration Template — 설정 템플릿 (Ch22) | 작성 예정 |

### 보안 — 컨테이너를 안전하게 (Ch23~26)

| 편 | 제목 | 상태 |
|----|------|------|
| — | Process Containment — 프로세스 격리 (Ch23) | 작성 예정 |
| — | Network Segmentation — 네트워크 분할 (Ch24) | 작성 예정 |
| — | Secure Configuration — 시크릿 안전 관리 (Ch25) | 작성 예정 |
| — | Access Control — 접근 제어(RBAC) (Ch26) | 작성 예정 |

### 고급 — 플랫폼 확장 (Ch27~30)

| 편 | 제목 | 상태 |
|----|------|------|
| — | Controller — 컨트롤러 (Ch27) | 작성 예정 |
| — | Operator — 오퍼레이터·CRD (Ch28) | 작성 예정 |
| — | Elastic Scale — 오토스케일(HPA·VPA·CA) (Ch29) | 작성 예정 |
| — | Image Builder — 클러스터 내 이미지 빌드 (Ch30) | 작성 예정 |



## 학습 상태

> 학습 워크플로우의 부팅 의례가 세션 시작 때 읽는 칸입니다. 정독본은 STATE.md를 따로 두지 않으므로 이 표가 그 역할을 대신합니다. 매 세션을 닫을 때 갱신합니다.

| 항목 | 현재 값 |
|------|---------|
| 현재 난이도 레벨 (ZPD) | 기본 — 원서 흐름 그대로 진행 |
| 막힌 지점 | 기록 전 |
| 다음 레슨 후보 | Ch17 Adapter |
| 최근 검증 결과 | 기록 전 (Phase 4 자답·퀴즈·복습 결과를 여기에 갱신) |
| 복습 회차 (_review) | 미개시 — 첫 복습 때 `_review/` 폴더 생성 |



## 번호 체계

> 파일명은 `NN-MM.제목.md` 형식입니다. `NN`은 책의 장(chapter) 번호, `MM`은 그 장을 여러 편으로 나눌 때의 편 순번입니다.

한 장이 한 패턴이라 대부분 `NN-01` 한 편으로 끝냅니다. 한 장이 길어 800줄을 넘길 것 같으면 개념 단위로 나눠 같은 장 번호 아래 편 번호를 늘립니다. 이렇게 하면 Typora 파일 탐색기에서 책 순서대로 정렬되고, 다른 노트에서 `§NN-MM`처럼 특정 편을 정확히 가리킬 수 있습니다.

정밀 도식이 필요하면 이 폴더의 `_assets/`에 SVG를 두고 본문에서 `![](_assets/…​.svg)`로 참조합니다. 흐름·관계·상태 전이는 Mermaid로 본문에 직접 그립니다.



## 개념 노트와의 관계

> 개념이 겹치면 여기서 다시 설명하지 않고 `../../kubernetes/`의 개념 노트로 링크를 겁니다. 이 폴더에는 책만의 관점·패턴 차이분만 남깁니다.

예를 들어 Pod·워크로드 개념은 개념 노트 [01-01.핵심 워크로드](../../kubernetes/01_workloads/01-01.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md)에, 서비스·디스커버리는 [04-04.Service와 EndpointSlice](../../kubernetes/04_networking/04-04.Service%EC%99%80%20EndpointSlice.md)에 이미 정리돼 있습니다. 패턴 편을 쓸 때 해당 오브젝트가 재료로 나오면 그 편의 `## 관련 문서`에서 이 노트들로 링크하고, 반대로 개념 노트의 `related`에도 이 책 편을 걸어 양방향을 유지합니다. 통째 병합은 하지 않고 링크로만 잇습니다.



## 관련 문서

> 같은 `book/` 영역의 다른 정독본과, 이 책이 링크로 위임하는 개념 노트 묶음입니다.

- [Kubernetes in Action, 2판 정독 인덱스](../kubernetes-in-action/README.md) — 같은 `08_cloud/book/` 영역의 입문·레퍼런스 정독본(49편). 이 책이 재료로 쓰는 오브젝트 설명을 위임
- [08_cloud/kubernetes — Kubernetes 실전 운영](../../kubernetes/README.md) — 이 책이 개념 중복을 링크로 위임하는 개념 노트 인덱스
- [Kubernetes Patterns 예제 코드 (k8spatterns/examples)](https://github.com/k8spatterns/examples) — 저자가 공개한 장별 예제 매니페스트·앱 소스
