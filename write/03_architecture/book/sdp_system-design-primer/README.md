---
title: The System Design Primer — 정독 인덱스
tags: [moc, study-index, book, system-design, scalability, interview]
status: draft
source:
  - https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md   # Donne Martin, CC BY 4.0. 2026-09-21 기준 HEAD 로 고정
related:
  - ../system-design/README.md
  - ../../README.md
  - ../../../05_data/README.md
  - ../../../roadmap/data-roadmap.md
  - ../../../roadmap/network-roadmap.md
updated: 2026-09-21
---

# The System Design Primer — 정독 인덱스
---

> Donne Martin 의 GitHub 문서 [The System Design Primer](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md) 를 primer 의 순서대로 따라가는 인덱스입니다. 지금은 본문이 없고, primer 의 각 절이 이 저장소 어디에 이미 있는지와 어디가 비어 있는지만 적어 둡니다.

## 이 자료를 book 폴더에 두는 이유

> 책은 아니지만 하나의 출처를 처음부터 끝까지 따라 읽는 자료라서 단행본과 같은 자리에 둡니다.

primer 는 출판된 책이 아니라 README 한 장입니다. 그래도 `book/` 아래에 두는 까닭은 이 폴더가 하는 일이 다른 정독 노트와 같기 때문입니다. 출처 하나를 정해 그 목차 순서로 읽고, 어디까지 읽었는지를 인덱스가 들고 있습니다. `02_os` 와 `08_cloud` 가 정본을 `book/` 에 모으고 나머지 폴더를 정리해 가는 방향과도 맞습니다.

README 는 계속 고쳐지는 문서라서 출처를 커밋 `ae9bbd7` 로 고정했습니다. 절 이름과 순서는 이 커밋의 헤딩에서 그대로 가져왔고, 나중에 원문이 바뀌면 이 SHA 와 비교해 차이만 반영합니다.

같은 폴더의 [Alex Xu 시리즈](../system-design/README.md) 와는 맡는 축이 다릅니다. 그쪽은 URL 단축기나 채팅처럼 시스템 하나를 끝까지 설계하는 사례 열다섯 편입니다. primer 는 그 사례들이 공통으로 꺼내 쓰는 부품을 하나씩 설명합니다.

그래서 로드 밸런서·캐시·복제·비동기 같은 부품은 primer 순서로 먼저 세우고 사례는 Alex Xu 쪽에서 읽습니다.



## 장 구성과 기존 문서 매핑

> primer 의 38개 절 묶음 가운데 22개는 이미 다른 폴더에 본문이 있습니다. 새로 쓸 곳은 「부분」 10개와 「공백」 5개입니다.

장 번호는 primer 의 헤딩 순서를 주제 묶음으로 나눈 것이고, 나중에 본문을 쓰면 다른 book 폴더처럼 `{장}-{절}.{제목}.md` 로 이 폴더에 평면으로 둡니다. 절의 절반 이상이 기존 문서로 넘어가므로 새 본문은 많아야 스무 편 안쪽이라 하위 폴더는 만들지 않았습니다.

상태는 추측이 아니라 2026-09-21 에 `write/` 전체의 헤딩을 훑고 후보 문서의 절 제목을 열어 본 결과입니다. `_review`·`_company`·`_archive` 는 뺐습니다. 세 값은 이렇게 갈랐습니다.

- 있음: 정의와 메커니즘과 단점까지 절로 세운 문서가 있습니다.
- 부분: 다루긴 하지만 primer 가 묻는 각도가 빠져 있습니다.
- 공백: 대응하는 절이 없습니다.

### 01장 · 접근법

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| 면접 질문 접근 4단계 | [시스템 설계 면접 4단계 프레임워크](../system-design/%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84%20%EB%A9%B4%EC%A0%91%204%EB%8B%A8%EA%B3%84%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC.md) | 있음 | 단계 이름만 다르고 절차는 같습니다 |
| Back-of-the-envelope · Powers of two · Latency numbers | [개략적 규모 추정](../system-design/%EA%B0%9C%EB%9E%B5%EC%A0%81%20%EA%B7%9C%EB%AA%A8%20%EC%B6%94%EC%A0%95.md) | 있음 | 2의 거듭제곱·지연 수치·나인 표가 한 편에 있습니다 |

### 02장 · 트레이드오프

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Performance vs scalability | [DDIA 02-04 확장성](../../../05_data/book/designing-data-intensive-applications/02-04.%ED%99%95%EC%9E%A5%EC%84%B1.md) | 있음 | 부하를 차원으로 기술하는 법까지 다룹니다 |
| Latency vs throughput | [DDIA 02-02 성능](../../../05_data/book/designing-data-intensive-applications/02-02.%EC%84%B1%EB%8A%A5%20%E2%80%94%20%EC%9D%91%EB%8B%B5%20%EC%8B%9C%EA%B0%84%EA%B3%BC%20%EC%B2%98%EB%A6%AC%EB%9F%89.md) | 있음 | 백분위와 꼬리 지연까지 primer 보다 깊습니다 |
| Availability vs consistency (CAP · CP · AP) | [DDIA 10-02 선형성의 비용과 CAP](../../../05_data/book/designing-data-intensive-applications/10-02.%EC%84%A0%ED%98%95%EC%84%B1%EC%9D%98%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20CAP.md) · [NoSQL 비교](../../../05_data/01_foundation/01-06.NoSQL%20%EB%B9%84%EA%B5%90.md) | 있음 | PACELC 까지 있습니다 |
| Consistency patterns (weak · eventual · strong) | [일관성과 합의](../../../05_data/01_foundation/02-06.%EC%9D%BC%EA%B4%80%EC%84%B1%EA%B3%BC%20%ED%95%A9%EC%9D%98.md) · [DDIA 06-03](../../../05_data/book/designing-data-intensive-applications/06-03.%EB%B3%B5%EC%A0%9C%20%EC%A7%80%EC%97%B0%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EC%9D%BC%EA%B4%80%EC%84%B1%20%EB%B3%B4%EC%9E%A5.md) | 부분 | eventual 과 strong 은 있고, weak 를 따로 세운 절은 없습니다 |
| Availability patterns — fail-over (active-passive · active-active) | [DDIA 06-02 노드 장애 처리](../../../05_data/book/designing-data-intensive-applications/06-02.%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%20%EC%B2%98%EB%A6%AC%EC%99%80%20%EB%B3%B5%EC%A0%9C%20%EB%A1%9C%EA%B7%B8.md) | 부분 | DB 리더 failover 만 있고, 서비스 앞단의 두 방식 비교가 없습니다 |
| Availability patterns — replication | [복제](../../../05_data/01_foundation/02-03.%EB%B3%B5%EC%A0%9C.md) | 있음 | 05장 표와 같은 문서입니다 |
| Availability in numbers (나인 · 직렬과 병렬) | [개략적 규모 추정](../system-design/%EA%B0%9C%EB%9E%B5%EC%A0%81%20%EA%B7%9C%EB%AA%A8%20%EC%B6%94%EC%A0%95.md) | 부분 | 나인 표는 있고, 직렬·병렬 구성의 가용성 곱셈이 없습니다 |

### 03장 · 진입 경로

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Domain name system | [cntd 02-03 메일과 이름](../../../02_os/book/cntd_computer-networking-top-down/02-03.%EB%A9%94%EC%9D%BC%EA%B3%BC%20%EC%9D%B4%EB%A6%84%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%B0%BE%EC%95%84%EA%B0%80%EB%8A%94%EA%B0%80.md) · [DNS와 CoreDNS](../../../08_cloud/kubernetes/04_networking/04-05.DNS%EC%99%80%20CoreDNS.md) | 있음 | 가중·지연·지역 기반 라우팅 정책만 빠져 있습니다 |
| Content delivery network (push · pull) | [cntd 02-04 영상](../../../02_os/book/cntd_computer-networking-top-down/02-04.%EC%98%81%EC%83%81%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EB%81%8A%EA%B8%B0%EC%A7%80%20%EC%95%8A%EB%8A%94%EA%B0%80.md) · [0부터 수백만](../system-design/0%EB%B6%80%ED%84%B0%20%EC%88%98%EB%B0%B1%EB%A7%8C%20%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B9%8C%EC%A7%80%20%ED%99%95%EC%9E%A5.md) | 부분 | 배치 철학은 있고, push 와 pull 의 갱신 방식 비교가 없습니다 |
| Load balancer (L4 · L7 · 수평 확장) | [Service 5유형](../../../08_cloud/book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) · [Ingress와 Gateway API](../../../08_cloud/kubernetes/04_networking/04-06.Ingress%EC%99%80%20Gateway%20API.md) | 부분 | Kubernetes 구현은 많지만 분배 알고리즘과 L4·L7 을 일반론으로 세운 문서가 없습니다 |
| Reverse proxy · LB 와의 차이 | — | 공백 | Jenkins·Nexus 설치 문서에서 언급만 됩니다 |

### 04장 · 애플리케이션 계층

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Microservices | [모놀리스에서 마이크로서비스로](../../04_ddd/03-04.%EB%AA%A8%EB%86%80%EB%A6%AC%EC%8A%A4%EC%97%90%EC%84%9C%20%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A1%9C%20%E2%80%94%20%EC%96%B8%EC%A0%9C%2C%20%EC%99%9C.md) · [분산 아키텍처 기초](../../03_distributed/01-01.%EB%B6%84%EC%82%B0%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B8%B0%EC%B4%88.md) | 있음 | 분리 기준과 비용을 다룹니다 |
| Service discovery | [K8s Patterns 13-01](../../../08_cloud/book/kubernetes-patterns/13-01.Service%20Discovery%20%E2%80%94%20%EA%B3%A0%EC%A0%95%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%EB%A1%9C%20%EB%8F%99%EC%A0%81%20Pod%EB%A5%BC%20%EC%B0%BE%EA%B8%B0.md) · [KUAR 07-01](../../../08_cloud/book/kubernetes-up-and-running/07-01.Service%20Discovery%20%E2%80%94%20DNS%EA%B0%80%20%EB%AA%BB%20%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%B0%94%EA%B9%A5%EC%9D%84%20%EC%9E%87%EB%8A%94%20%EB%B2%95.md) | 있음 | Consul·etcd·ZooKeeper 방식은 [일관성과 합의](../../../05_data/01_foundation/02-06.%EC%9D%BC%EA%B4%80%EC%84%B1%EA%B3%BC%20%ED%95%A9%EC%9D%98.md) 의 코디네이션 서비스 절이 받습니다 |

### 05장 · 데이터베이스

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Master-slave · master-master replication | [복제](../../../05_data/01_foundation/02-03.%EB%B3%B5%EC%A0%9C.md) · [DDIA 06-01](../../../05_data/book/designing-data-intensive-applications/06-01.%EB%B3%B5%EC%A0%9C%20%EA%B0%9C%EC%9A%94%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EB%A6%AC%EB%8D%94.md) | 있음 | 단일 리더·다중 리더·리더리스로 이름만 다릅니다 |
| Federation (기능별 DB 분할) | — | 공백 | 저장소의 federation 은 Prometheus 와 Module Federation 뿐입니다 |
| Sharding | [샤딩](../../../05_data/01_foundation/02-04.%EC%83%A4%EB%94%A9.md) · [안정 해시 설계](../system-design/%EC%95%88%EC%A0%95%20%ED%95%B4%EC%8B%9C%20%EC%84%A4%EA%B3%84.md) | 있음 | 리밸런싱과 보조 인덱스까지 있습니다 |
| Denormalization | [정규화와 비정규화](../../../05_data/02_relational/sql-mysql/02-02.%EC%A0%95%EA%B7%9C%ED%99%94%EC%99%80%20%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94.md) · [DDIA 03-02](../../../05_data/book/designing-data-intensive-applications/03-02.%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EC%A1%B0%EC%9D%B8.md) | 있음 |  |
| SQL tuning | [인덱스 이론](../../../05_data/01_foundation/01-05.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%9D%B4%EB%A1%A0.md) · [인덱스 실전](../../../05_data/02_relational/sql-mysql/03-01.%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EC%8B%A4%EC%A0%84%20%E2%80%94%20EXPLAIN%2C%20IOT%2C%20%ED%8E%98%EC%9D%B4%EC%A7%80%EB%84%A4%EC%9D%B4%EC%85%98.md) · [쿼리 최적화 체크리스트](../../../05_data/02_relational/sql-mysql/07-01.%EC%BF%BC%EB%A6%AC%20%EC%B5%9C%EC%A0%81%ED%99%94%20%EC%B2%B4%ED%81%AC%EB%A6%AC%EC%8A%A4%ED%8A%B8.md) | 있음 |  |
| NoSQL 4종 · SQL or NoSQL | [NoSQL 비교](../../../05_data/01_foundation/01-06.NoSQL%20%EB%B9%84%EA%B5%90.md) · [키-값 저장소 설계](../system-design/%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%20%EC%84%A4%EA%B3%84.md) | 있음 | 선택 가이드 절이 SQL or NoSQL 에 대응합니다 |

### 06장 · 캐시

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| 계층별 캐시 (client · CDN · web server · DB · application) | [캐싱 전략](../../../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | 부분 | 다단 캐시 L1·L2·L3 는 있고, 클라이언트·웹 서버 계층은 없습니다 |
| 갱신 전략 — cache-aside · write-through · write-behind | [캐싱 전략](../../../05_data/01_foundation/01-07.%EC%BA%90%EC%8B%B1%20%EC%A0%84%EB%9E%B5.md) | 있음 | stampede·hot key·penetration 까지 primer 보다 넓습니다 |
| 갱신 전략 — refresh-ahead | — | 공백 | 캐싱 전략 문서에 등장 0회입니다 |

### 07장 · 비동기

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Message queues | [메시지 큐 아키텍처](../../../04_messaging/04_BrokerArchitecture/01-01.%EB%A9%94%EC%8B%9C%EC%A7%80%20%ED%81%90%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) · [EDA 기초](../../05_edd/05-01.EDA%20%EA%B8%B0%EC%B4%88.md) | 있음 |  |
| Task queues | [Temporal 핵심 개념](../../../04_messaging/08_advanced/02_workflow/01-02.Temporal%20%ED%95%B5%EC%8B%AC%20%EA%B0%9C%EB%85%90%20-%20Workflow%EC%99%80%20Activity.md) | 부분 | Temporal 의 Task Queue 뿐이고, 메시지 큐와 무엇이 다른지 세운 절이 없습니다 |
| Back pressure | [DDIA 02-02 성능](../../../05_data/book/designing-data-intensive-applications/02-02.%EC%84%B1%EB%8A%A5%20%E2%80%94%20%EC%9D%91%EB%8B%B5%20%EC%8B%9C%EA%B0%84%EA%B3%BC%20%EC%B2%98%EB%A6%AC%EB%9F%89.md) · [EDA + CDC + Temporal](../../../04_messaging/08_advanced/02_workflow/02-01.EDA%20%2B%20CDC%20%2B%20Temporal%20%ED%86%B5%ED%95%A9%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | 부분 | 과부하 대응 넷 중 하나로만 나옵니다 |

### 08장 · 통신

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| HTTP | [cntd 02-02 웹](../../../02_os/book/cntd_computer-networking-top-down/02-02.%EC%9B%B9%EC%9D%80%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%A3%BC%EA%B3%A0%EB%B0%9B%EB%8A%94%EA%B0%80.md) | 있음 |  |
| TCP · UDP | [cntd 03-01 트랜스포트](../../../02_os/book/cntd_computer-networking-top-down/03-01.%ED%8A%B8%EB%9E%9C%EC%8A%A4%ED%8F%AC%ED%8A%B8%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8A%94%EA%B0%80.md) · [cntd 03-03 TCP](../../../02_os/book/cntd_computer-networking-top-down/03-03.TCP%20%EB%8A%94%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EC%84%B8%EA%B3%A0%20%EC%96%B4%EB%96%BB%EA%B2%8C%20%EA%B8%B0%EB%8B%A4%EB%A6%AC%EB%8A%94%EA%B0%80.md) | 있음 |  |
| RPC · REST · 둘의 비교 | [REST, gRPC, Messaging 선택 기준](../../03_distributed/01-03.REST%2C%20gRPC%2C%20Messaging%20%EC%84%A0%ED%83%9D%20%EA%B8%B0%EC%A4%80.md) | 있음 | 선택 기준 중심이고 REST 제약 조건 자체는 얕습니다 |

### 09장 · 보안

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Security (전송·저장 암호화 · 입력 검증 · 파라미터 바인딩 · 최소 권한) | [99_ETC/security](../../../99_ETC/security/README.md) | 부분 | 인증·네트워크 공격은 있고, OWASP 폴더는 README 에 신설 예정으로만 적혀 있습니다 |

### 10장 · 설계 문제 풀이

| primer 절 | 기존 문서 | 상태 | 메모 |
|---|---|---|---|
| Pastebin · Bit.ly | [URL 단축기 설계](../system-design/URL%20%EB%8B%A8%EC%B6%95%EA%B8%B0%20%EC%84%A4%EA%B3%84.md) | 있음 |  |
| Twitter timeline and search | [뉴스 피드 시스템 설계](../system-design/%EB%89%B4%EC%8A%A4%20%ED%94%BC%EB%93%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%84%A4%EA%B3%84.md) · [Fan-out 피드 시스템](../../../05_data/02_relational/sql-mysql/05-01.Fan-out%20%ED%94%BC%EB%93%9C%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) | 부분 | 타임라인은 있고 검색 쪽이 없습니다 |
| Web crawler | [웹 크롤러 설계](../system-design/%EC%9B%B9%20%ED%81%AC%EB%A1%A4%EB%9F%AC%20%EC%84%A4%EA%B3%84.md) | 있음 |  |
| Scales to millions of users on AWS | [0부터 수백만 사용자까지 확장](../system-design/0%EB%B6%80%ED%84%B0%20%EC%88%98%EB%B0%B1%EB%A7%8C%20%EC%82%AC%EC%9A%A9%EC%9E%90%EA%B9%8C%EC%A7%80%20%ED%99%95%EC%9E%A5.md) | 있음 | AWS 서비스 이름으로 옮긴 부분만 다릅니다 |
| Mint.com · Social network 자료구조 · 검색엔진용 key-value 캐시 · Amazon sales ranking | — | 공백 | 네 문제 모두 대응 문서가 없습니다 |
| Object-oriented design 문제 (hash map · LRU cache · call center · deck of cards · parking lot · chat server) | — | 공백 | 시스템 설계와 축이 달라 뒤로 미룹니다 |
| Real world architectures · Company engineering blogs | — | 범위 밖 | 링크 모음이라 본편을 두지 않습니다 |



## 공백 목록

> 새로 쓸 후보를 먼저 쓸 순서로 적었습니다. 다른 폴더의 문서를 고치는 편이 나은 항목은 그렇게 표시했습니다.

앞 순위일수록 Alex Xu 사례를 읽을 때 자주 걸리는 부품입니다. 사례 열다섯 편 대부분이 로드 밸런서와 가용성 구성을 전제로 깔고 시작하는데, 정작 그 둘을 일반론으로 세운 문서가 저장소에 없습니다.

| 순위 | 쓸 내용 | 자리 | 왜 비어 있나 |
|---|---|---|---|
| 1 | 로드 밸런서 일반론과 리버스 프록시 — L4·L7, 분배 알고리즘, 둘의 차이 | 이 폴더 03장 | Kubernetes Service·Ingress 구현 문서만 쌓였고 구현 밖의 개념 문서가 없습니다 |
| 2 | 가용성 패턴 — active-passive·active-active fail-over, 직렬·병렬 가용성 계산 | 이 폴더 02장 | failover 가 DB 리더 교체 맥락에서만 다뤄졌습니다 |
| 3 | CDN push 와 pull | 이 폴더 03장 | cntd 는 서버를 어디에 둘지를 다루고 콘텐츠를 어떻게 채울지는 다루지 않습니다 |
| 4 | Federation — 기능별 DB 분할과 샤딩의 차이 | 이 폴더 05장 | 같은 단어가 Prometheus 와 프론트엔드 문서에만 있습니다 |
| 5 | Task queue 와 back pressure | 이 폴더 07장 | 메시징 폴더가 Kafka 중심이라 작업 큐와 과부하 제어가 곁가지로만 나옵니다 |
| 6 | Refresh-ahead, 클라이언트·웹 서버 캐시 | `05_data/01_foundation/01-07` 보강 | 새 문서보다 기존 캐싱 전략 편에 절을 더하는 쪽이 중복이 없습니다 |
| 7 | Weak consistency | `05_data/01_foundation/02-06` 보강 | 같은 이유로 기존 편에 더합니다 |
| 8 | 보안 기초 — 입력 검증·파라미터 바인딩·최소 권한 | `99_ETC/security/` | 그쪽 README 가 OWASP 폴더 신설을 이미 예정해 두었습니다 |
| 9 | 설계 문제 넷 — Mint.com·소셜 그래프·검색 캐시·판매 순위 | 이 폴더 10장 | Alex Xu 1권에 없는 문제들입니다 |
| 10 | OOD 문제 여섯 | 미정 | 시스템 설계가 아니라 객체 설계라 `01_language` 나 `03_architecture/01_foundation` 이 맞을 수 있습니다 |



## 읽는 순서

> 01장과 02장을 먼저 읽고, 03장부터는 요청이 들어와 데이터에 닿는 순서대로 내려갑니다.

primer 가 권하는 순서도 같습니다. 트레이드오프를 먼저 잡고 나서 DNS·CDN·로드 밸런서 같은 앞단에서 애플리케이션 계층, 데이터베이스, 캐시로 내려간 다음 비동기와 통신으로 옆으로 넓힙니다. 이 순서는 사용자 요청 하나가 시스템을 통과하는 경로와 겹쳐서, 각 부품이 앞 부품의 어떤 한계 때문에 필요해지는지가 자연스럽게 이어집니다.

10장의 설계 문제는 앞 장을 다 읽은 뒤가 아니라 중간중간 꺼내 봅니다. 05장까지 읽었으면 URL 단축기를, 07장까지 읽었으면 뉴스 피드를 풀어 보는 식입니다. 「있음」으로 표시된 절은 링크된 문서를 primer 원문과 나란히 놓고 읽으면 되고, 이 폴더에 새 본문이 생기는 곳은 위 공백 목록뿐입니다.
