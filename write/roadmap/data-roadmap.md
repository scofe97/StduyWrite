---
title: 데이터 학습 로드맵
tags: [roadmap, data, database, storage, replication, consensus, stream]
status: final
source:
  - ../05_data/book/designing-data-intensive-applications/README.md
related:
  - README.md
  - spring-roadmap.md
  - observability-roadmap.md
  - ../05_data/README.md
updated: 2026-09-13
---

# 데이터 학습 로드맵
---

> DDIA 2판의 열네 장을 척추로 삼습니다. 데이터 시스템의 축에서 시작해 모델과 저장 엔진과 인코딩을 지나 복제·샤딩·트랜잭션·합의·스트림으로 갑니다.

## 학습 순서

> 단계마다 배우는 개념을 묶음으로 갈랐습니다. 자료 위치는 아래 단계별 표가 짚습니다.

![데이터 시스템의 축에서 배치와 스트림까지 내려가는 학습 순서](_assets/data-roadmap.svg)

| 단계 | 묶음 | 배우는 개념 |
|---|---|---|
| 1 · 데이터 시스템의 축 | 갈래 | 운영 시스템과 분석 시스템 · 분산과 단일 노드 · 클라우드와 셀프 호스팅 |
| 1 · 데이터 시스템의 축 | 비기능 | 응답 시간 · 처리량 · 꼬리 지연 · 신뢰성 · 내결함성 · 확장성 · 유지보수성 |
| 2 · 데이터 모델 | 표현 | 관계형 · 문서 · 그래프 · 정규화 · 비정규화 · 조인 횟수 · 스키마 유연성 |
| 2 · 데이터 모델 | 분석용 | 별 스키마 · 눈송이 · OBT · 이벤트 소싱 · CQRS · DataFrame |
| 3 · 저장 엔진과 인덱스 | 자료구조 | OLTP 저장 · B-tree 기초와 변형 · LSM · 로그 구조 저장 · 페이지 분할 |
| 3 · 저장 엔진과 인덱스 | 지속성 | 파일 포맷 · WAL · 세그먼트 로그 · 복구 · 보조 인덱스 · 인메모리 저장 |
| 3 · 저장 엔진과 인덱스 | 분석과 검색 | 컬럼 지향 저장 · 다차원 · 전문 · 벡터 인덱스 · 역색인 · 텍스트 분석 |
| 4 · 인코딩과 데이터플로우 | 형식 | 인코딩 호환성 · JSON · XML · 이진 변형 · Protocol Buffers · Avro · 스키마 진화 |
| 4 · 인코딩과 데이터플로우 | 전달 | DB 경유 · REST · RPC · 메시지 · durable execution · 이벤트 기반 아키텍처 |
| 5 · 복제와 샤딩 | 복제 | 단일 리더 · 복제 로그 · 복제 지연 · 읽기 후 쓰기 · 다중 리더 · 쓰기 충돌 · 리더리스 · 정족수 |
| 5 · 복제와 샤딩 | 샤딩 | 키 범위 샤딩 · 해시 샤딩 · 일관 해싱 · 요청 라우팅 · 리밸런싱 · 샤딩과 보조 인덱스 |
| 6 · 트랜잭션과 격리 | 격리 | ACID · 약한 격리 수준 · 스냅샷 격리 · Write Skew · 직렬화 가능성 |
| 6 · 트랜잭션과 격리 | 복구와 분산 | 트랜잭션 처리 · 복구 · 분산 트랜잭션 · 2PC · 코디네이터 장애 |
| 7 · 분산의 문제 | 믿을 수 없는 것 | 부분 실패 · 비신뢰 네트워크 · 불신뢰 시계 · 진실과 거짓 · 시스템 모델 · 검증 |
| 7 · 분산의 문제 | 살아 있음 판정 | 장애 감지 · HeartBeat · 리더 선출 · 임차 · 상태 감시 · 가십 전파 |
| 8 · 일관성과 합의 | 일관성 | 선형성 · 선형성의 비용 · CAP · ID 생성기 · 논리 시계 · 하이브리드 시계 |
| 8 · 일관성과 합의 | 합의 | 합의 알고리즘 · 코디네이션 서비스 · Paxos · Replicated Log · 일관 코어 · 버전 벡터 |
| 9 · 배치와 스트림 | 배치 | Unix 도구 · 분산 파일시스템 · 오브젝트 스토어 · MapReduce · 데이터플로우 엔진 |
| 9 · 배치와 스트림 | 스트림 | 메시지 브로커 · 로그 기반 브로커 · CDC · CEP · 윈도우 · 조인 · 시간 추론 |
| 9 · 배치와 스트림 | 통합 | 파생 데이터 · 전순서의 한계 · 배치와 스트림 통합 · DB 언번들링 |



## 책 읽기 흐름

> 위 단계를 무엇으로 배우는가입니다. 소장 책 넷과 DDIA 2판 정독 노트로 한정했습니다.

![데이터 책 읽기 흐름 — 우선순위와 읽을 장](_assets/data-books.svg)

같은 책이 여러 단계에 갈려 걸리므로 행이 단계가 아니라 책의 역할로 묶입니다.

| 책 | 읽을 장 | 우선순위 | 자리 |
|---|---|:---:|---|
| [Designing Data-Intensive Applications, 2판](../05_data/book/designing-data-intensive-applications/README.md) | 전 14장 | 필수 | 1~9단계 |
| Database Internals | 1~7 · 9~14장 | 추천 | 3 · 5~8단계 |
| Patterns of Distributed Systems | 3~7 · 10~12 · 17~29장 | 추천 | 3 · 5 · 7·8단계 |
| Elasticsearch in Action, 2판 | 3·4 · 7~13장 | 선택 | 3단계 |

공식 자료가 빈칸을 메웁니다. [Raft](https://raft.github.io/)가 8단계, [Jepsen 의 일관성 모델 지도](https://jepsen.io/consistency)가 7·8단계, [DDIA 2판 참조 모음](https://github.com/ept/ddia2-references)이 전 단계를 받칩니다.

**자료를 책과 정독 노트로 한정했습니다.** `05_data` 의 자체 노트 여든다섯 편은 SQL·JDBC·JPA·QueryDSL 을 익힌 기록이라 순서의 근거로 쓰지 않습니다. 그 축은 [05_data MOC](../05_data/README.md)와 [Spring 로드맵](spring-roadmap.md)이 맡습니다.



## 노드 한 대 · 1~4단계

> 데이터를 어떻게 표현하고 눕히고 옮기는가입니다. 노드가 하나여도 전부 생기는 문제입니다.

### 1단계 · 데이터 시스템의 축

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 운영 시스템과 분석 시스템 | 필수 | [01-01](../05_data/book/designing-data-intensive-applications/01-01.%EC%9A%B4%EC%98%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20vs%20%EB%B6%84%EC%84%9D%20%EC%8B%9C%EC%8A%A4%ED%85%9C.md) | DDIA 1장 |
| 분산과 단일 노드 | 필수 | [01-04](../05_data/book/designing-data-intensive-applications/01-04.%EB%B6%84%EC%82%B0%20vs%20%EB%8B%A8%EC%9D%BC%20%EB%85%B8%EB%93%9C.md) | DDIA 1장 |
| 클라우드와 셀프 호스팅 | 추천 | [01-03](../05_data/book/designing-data-intensive-applications/01-03.%ED%81%B4%EB%9D%BC%EC%9A%B0%EB%93%9C%20vs%20%EC%85%80%ED%94%84%20%ED%98%B8%EC%8A%A4%ED%8C%85.md) | DDIA 1장 |
| 응답 시간과 처리량 | 필수 | [02-02](../05_data/book/designing-data-intensive-applications/02-02.%EC%84%B1%EB%8A%A5%20%E2%80%94%20%EC%9D%91%EB%8B%B5%20%EC%8B%9C%EA%B0%84%EA%B3%BC%20%EC%B2%98%EB%A6%AC%EB%9F%89.md) | DDIA 2장 |
| 신뢰성과 내결함성 | 필수 | [02-03](../05_data/book/designing-data-intensive-applications/02-03.%EC%8B%A0%EB%A2%B0%EC%84%B1%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1.md) | DDIA 2장 |
| 확장성과 유지보수성 | 필수 | [02-04](../05_data/book/designing-data-intensive-applications/02-04.%ED%99%95%EC%9E%A5%EC%84%B1.md) · [02-05](../05_data/book/designing-data-intensive-applications/02-05.%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98%EC%84%B1.md) | DDIA 2장 |
| 사례로 보는 설계 선택 | 추천 | [02-01](../05_data/book/designing-data-intensive-applications/02-01.%EC%82%AC%EB%A1%80%20%EC%97%B0%EA%B5%AC%20%E2%80%94%20%EC%86%8C%EC%85%9C%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%ED%99%88%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8.md) | DDIA 2장 |
| 데이터와 법 · 사회 | 선택 | [01-05](../05_data/book/designing-data-intensive-applications/01-05.%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%C2%B7%EB%B2%95%C2%B7%EC%82%AC%ED%9A%8C.md) | DDIA 1·14장 |
| 용어를 먼저 고정하기 | 추천 | [00-01](../05_data/book/designing-data-intensive-applications/00-01.%EC%9A%A9%EC%96%B4%EC%A7%91%20%E2%80%94%20DDIA%202%ED%8C%90%20%ED%95%B5%EC%8B%AC%20%EC%9A%A9%EC%96%B4%2050%EC%84%A0.md) | DDIA 서문 |

### 2단계 · 데이터 모델

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 관계형과 문서 모델 | 필수 | [03-01](../05_data/book/designing-data-intensive-applications/03-01.%EA%B4%80%EA%B3%84%ED%98%95%20vs%20%EB%AC%B8%EC%84%9C%20%EB%AA%A8%EB%8D%B8.md) | DDIA 3장 |
| 정규화 · 비정규화 · 조인 | 필수 | [03-02](../05_data/book/designing-data-intensive-applications/03-02.%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EB%B9%84%EC%A0%95%EA%B7%9C%ED%99%94%C2%B7%EC%A1%B0%EC%9D%B8.md) | DDIA 3장 |
| 스키마 유연성과 모델 선택 | 필수 | [03-04](../05_data/book/designing-data-intensive-applications/03-04.%EB%AA%A8%EB%8D%B8%20%EC%84%A0%ED%83%9D%EA%B3%BC%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%EC%9C%A0%EC%97%B0%EC%84%B1.md) | DDIA 3장 |
| 그래프 데이터 모델 | 추천 | [03-05](../05_data/book/designing-data-intensive-applications/03-05.%EA%B7%B8%EB%9E%98%ED%94%84%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%AA%A8%EB%8D%B8.md) | DDIA 3장 |
| 분석용 스키마 — 별 · 눈송이 | 추천 | [03-03](../05_data/book/designing-data-intensive-applications/03-03.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%8A%A4%ED%82%A4%EB%A7%88%20%E2%80%94%20%EB%B3%84%C2%B7%EB%88%88%EC%86%A1%EC%9D%B4%C2%B7OBT.md) | DDIA 3장 |
| 이벤트 소싱 · CQRS | 추천 | [03-06](../05_data/book/designing-data-intensive-applications/03-06.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EC%86%8C%EC%8B%B1%C2%B7CQRS%C2%B7DataFrame.md) | DDIA 3장 |

### 3단계 · 저장 엔진과 인덱스

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| OLTP 저장과 인덱스 기초 | 필수 | [04-01](../05_data/book/designing-data-intensive-applications/04-01.OLTP%20%EC%A0%80%EC%9E%A5%EA%B3%BC%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%20%EA%B8%B0%EC%B4%88.md) | DDIA 4장 |
| B-tree 기초와 구현 | 필수 | | Database Internals 2·4장 |
| LSM 과 로그 구조 저장 | 필수 | [04-02](../05_data/book/designing-data-intensive-applications/04-02.LSM%20%EC%A0%80%EC%9E%A5%20%EC%97%94%EC%A7%84.md) | Database Internals 7장 |
| B-tree 와 LSM 비교 | 필수 | [04-03](../05_data/book/designing-data-intensive-applications/04-03.B-tree%EC%99%80%20LSM%20%EB%B9%84%EA%B5%90.md) | DDIA 4장 |
| 파일 포맷과 B-tree 변형 | 추천 | | Database Internals 3·6장 |
| WAL 과 세그먼트 로그 | 추천 | | PoDS 3·4장 |
| 보조 인덱스와 인메모리 | 필수 | [04-04](../05_data/book/designing-data-intensive-applications/04-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%20%EC%9D%B8%EB%A9%94%EB%AA%A8%EB%A6%AC%20%EC%A0%80%EC%9E%A5.md) | DDIA 4장 |
| 컬럼 지향 저장 | 추천 | [04-05](../05_data/book/designing-data-intensive-applications/04-05.%EB%B6%84%EC%84%9D%EC%9A%A9%20%EC%BB%AC%EB%9F%BC%20%EC%A7%80%ED%96%A5%20%EC%A0%80%EC%9E%A5.md) | DDIA 4장 |
| 다차원 · 전문 · 벡터 인덱스 | 추천 | [04-06](../05_data/book/designing-data-intensive-applications/04-06.%EB%8B%A4%EC%B0%A8%EC%9B%90%C2%B7%EC%A0%84%EB%AC%B8%C2%B7%EB%B2%A1%ED%84%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4.md) | DDIA 4장 |
| 전문 검색 엔진의 색인 | 선택 | | Elasticsearch 3·4 · 7장 |

### 4단계 · 인코딩과 데이터플로우

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 인코딩과 호환성 기초 | 필수 | [05-01](../05_data/book/designing-data-intensive-applications/05-01.%EC%9D%B8%EC%BD%94%EB%94%A9%EA%B3%BC%20%ED%98%B8%ED%99%98%EC%84%B1%20%EA%B8%B0%EC%B4%88.md) | DDIA 5장 |
| JSON · XML · 이진 변형 | 필수 | [05-02](../05_data/book/designing-data-intensive-applications/05-02.JSON%C2%B7XML%C2%B7%EC%9D%B4%EC%A7%84%20%EB%B3%80%ED%98%95.md) | DDIA 5장 |
| Protocol Buffers 와 Avro | 필수 | [05-03](../05_data/book/designing-data-intensive-applications/05-03.Protocol%20Buffers%EC%99%80%20Avro.md) | DDIA 5장 |
| DB · REST · RPC 데이터플로우 | 필수 | [05-04](../05_data/book/designing-data-intensive-applications/05-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%E2%80%94%20DB%C2%B7REST%C2%B7RPC.md) | DDIA 5장 |
| durable execution | 추천 | [05-05](../05_data/book/designing-data-intensive-applications/05-05.durable%20execution%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | DDIA 5장 |
| 이벤트 기반 아키텍처 | 추천 | [05-05](../05_data/book/designing-data-intensive-applications/05-05.durable%20execution%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | DDIA 5장 |



## 노드 둘 이상 · 5~9단계

> 노드가 여럿일 때만 생기는 문제입니다. 대부분 읽어서 배우는 구간이기도 합니다.

### 5단계 · 복제와 샤딩

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 단일 리더 복제 | 필수 | [06-01](../05_data/book/designing-data-intensive-applications/06-01.%EB%B3%B5%EC%A0%9C%20%EA%B0%9C%EC%9A%94%EC%99%80%20%EB%8B%A8%EC%9D%BC%20%EB%A6%AC%EB%8D%94.md) | DDIA 6장 |
| 복제 로그와 노드 장애 | 필수 | [06-02](../05_data/book/designing-data-intensive-applications/06-02.%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%20%EC%B2%98%EB%A6%AC%EC%99%80%20%EB%B3%B5%EC%A0%9C%20%EB%A1%9C%EA%B7%B8.md) | DDIA 6장 |
| 복제 지연과 일관성 보장 | 필수 | [06-03](../05_data/book/designing-data-intensive-applications/06-03.%EB%B3%B5%EC%A0%9C%20%EC%A7%80%EC%97%B0%20%EB%AC%B8%EC%A0%9C%EC%99%80%20%EC%9D%BC%EA%B4%80%EC%84%B1%20%EB%B3%B4%EC%9E%A5.md) | DDIA 6장 |
| 다중 리더와 쓰기 충돌 | 추천 | [06-04](../05_data/book/designing-data-intensive-applications/06-04.%EB%8B%A4%EC%A4%91%20%EB%A6%AC%EB%8D%94%20%EB%B3%B5%EC%A0%9C.md) · [06-05](../05_data/book/designing-data-intensive-applications/06-05.%EC%93%B0%EA%B8%B0%20%EC%B6%A9%EB%8F%8C%20%ED%95%B4%EC%86%8C.md) | DDIA 6장 |
| 리더리스 복제와 정족수 | 필수 | [06-06](../05_data/book/designing-data-intensive-applications/06-06.%EB%A6%AC%EB%8D%94%EB%A6%AC%EC%8A%A4%20%EB%B3%B5%EC%A0%9C%EC%99%80%206%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 6장 |
| 키 범위 샤딩 | 필수 | [07-01](../05_data/book/designing-data-intensive-applications/07-01.%EC%83%A4%EB%94%A9%20%EA%B0%9C%EC%9A%94%EC%99%80%20%ED%82%A4%20%EB%B2%94%EC%9C%84%20%EC%83%A4%EB%94%A9.md) | DDIA 7장 · PoDS 20장 |
| 해시 샤딩과 일관 해싱 | 필수 | [07-02](../05_data/book/designing-data-intensive-applications/07-02.%ED%95%B4%EC%8B%9C%20%EC%83%A4%EB%94%A9%EA%B3%BC%20%EC%9D%BC%EA%B4%80%20%ED%95%B4%EC%8B%B1.md) | DDIA 7장 |
| 요청 라우팅과 리밸런싱 | 필수 | [07-03](../05_data/book/designing-data-intensive-applications/07-03.%EC%9A%94%EC%B2%AD%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%EB%A6%AC%EB%B0%B8%EB%9F%B0%EC%8B%B1.md) | DDIA 7장 · PoDS 19장 |
| 샤딩과 보조 인덱스 | 추천 | [07-04](../05_data/book/designing-data-intensive-applications/07-04.%EB%B3%B4%EC%A1%B0%20%EC%9D%B8%EB%8D%B1%EC%8A%A4%EC%99%80%207%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 7장 |
| 복제 일관성의 구현 | 추천 | | Database Internals 11·12장 |

### 6단계 · 트랜잭션과 격리

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| ACID 와 트랜잭션 개요 | 필수 | [08-01](../05_data/book/designing-data-intensive-applications/08-01.ACID%EC%99%80%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EA%B0%9C%EC%9A%94.md) | DDIA 8장 |
| 약한 격리와 스냅샷 격리 | 필수 | [08-02](../05_data/book/designing-data-intensive-applications/08-02.%EC%95%BD%ED%95%9C%20%EA%B2%A9%EB%A6%AC%20%EC%88%98%EC%A4%80%EA%B3%BC%20%EC%8A%A4%EB%83%85%EC%83%B7%20%EA%B2%A9%EB%A6%AC.md) | DDIA 8장 |
| Write Skew 와 직렬화 | 필수 | [08-03](../05_data/book/designing-data-intensive-applications/08-03.Write%20Skew%EC%99%80%20%EC%A7%81%EB%A0%AC%ED%99%94%20%EA%B0%80%EB%8A%A5%EC%84%B1.md) | DDIA 8장 |
| 분산 트랜잭션과 2PC | 필수 | [08-04](../05_data/book/designing-data-intensive-applications/08-04.%EB%B6%84%EC%82%B0%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%202PC.md) | DDIA 8장 · PoDS 21장 |
| 트랜잭션 처리와 복구 | 추천 | | Database Internals 5장 |
| 분산 트랜잭션 구현 | 추천 | | Database Internals 13장 |

### 7단계 · 분산의 문제

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 부분 실패와 비신뢰 네트워크 | 필수 | [09-01](../05_data/book/designing-data-intensive-applications/09-01.%EB%B6%80%EB%B6%84%20%EC%8B%A4%ED%8C%A8%EC%99%80%20%EB%B9%84%EC%8B%A0%EB%A2%B0%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC.md) | DDIA 9장 |
| 불신뢰 시계 | 필수 | [09-02](../05_data/book/designing-data-intensive-applications/09-02.%EB%B6%88%EC%8B%A0%EB%A2%B0%20%EC%8B%9C%EA%B3%84.md) | DDIA 9장 |
| 진실 · 거짓 · 시스템 모델 | 필수 | [09-03](../05_data/book/designing-data-intensive-applications/09-03.%EC%A7%84%EC%8B%A4%C2%B7%EA%B1%B0%EC%A7%93%C2%B7%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EB%AA%A8%EB%8D%B8.md) | DDIA 9장 |
| 분산 시스템 검증 | 추천 | [09-04](../05_data/book/designing-data-intensive-applications/09-04.%EB%B6%84%EC%82%B0%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B2%80%EC%A6%9D%EA%B3%BC%209%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 9장 |
| 장애 감지 | 필수 | | Database Internals 9장 · PoDS 7장 |
| 리더 선출 | 필수 | | Database Internals 10장 · PoDS 6장 |
| 임차와 상태 감시 | 추천 | | PoDS 26·27장 |
| 가십 전파와 창발 리더 | 선택 | | PoDS 28·29장 |

### 8단계 · 일관성과 합의

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 선형성 | 필수 | [10-01](../05_data/book/designing-data-intensive-applications/10-01.%EC%84%A0%ED%98%95%EC%84%B1.md) | DDIA 10장 |
| 선형성의 비용과 CAP | 필수 | [10-02](../05_data/book/designing-data-intensive-applications/10-02.%EC%84%A0%ED%98%95%EC%84%B1%EC%9D%98%20%EB%B9%84%EC%9A%A9%EA%B3%BC%20CAP.md) | DDIA 10장 |
| ID 생성기와 논리 시계 | 필수 | [10-03](../05_data/book/designing-data-intensive-applications/10-03.ID%20%EC%83%9D%EC%84%B1%EA%B8%B0%EC%99%80%20%EB%85%BC%EB%A6%AC%20%EC%8B%9C%EA%B3%84.md) | DDIA 10장 · PoDS 22·23장 |
| 합의와 코디네이션 서비스 | 필수 | [10-04](../05_data/book/designing-data-intensive-applications/10-04.%ED%95%A9%EC%9D%98%EC%99%80%20%EC%BD%94%EB%94%94%EB%84%A4%EC%9D%B4%EC%85%98%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | DDIA 10장 |
| 합의 알고리즘 | 필수 | | Database Internals 14장 |
| Paxos 와 Replicated Log | 추천 | | PoDS 11·12장 |
| 일관 코어 | 추천 | | PoDS 25장 |
| 버전 값과 버전 벡터 | 추천 | | PoDS 17·18장 |
| 시계 경계 대기 | 선택 | | PoDS 24장 |

### 9단계 · 배치와 스트림

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Unix 도구와 배치 개요 | 필수 | [11-01](../05_data/book/designing-data-intensive-applications/11-01.%EB%B0%B0%EC%B9%98%20%EC%B2%98%EB%A6%AC%20%EA%B0%9C%EC%9A%94%EC%99%80%20Unix%20%EB%8F%84%EA%B5%AC.md) | DDIA 11장 |
| 분산 FS 와 오브젝트 스토어 | 필수 | [11-02](../05_data/book/designing-data-intensive-applications/11-02.%EB%B6%84%EC%82%B0%20%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B3%BC%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%8A%A4%ED%86%A0%EC%96%B4.md) | DDIA 11장 |
| MapReduce 와 잡 오케스트레이션 | 추천 | [11-03](../05_data/book/designing-data-intensive-applications/11-03.%EB%B6%84%EC%82%B0%20%EC%9E%A1%20%EC%98%A4%EC%BC%80%EC%8A%A4%ED%8A%B8%EB%A0%88%EC%9D%B4%EC%85%98%EA%B3%BC%20MapReduce.md) | DDIA 11장 |
| 데이터플로우 엔진 | 추천 | [11-04](../05_data/book/designing-data-intensive-applications/11-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%EC%97%94%EC%A7%84%EA%B3%BC%20%EB%B0%B0%EC%B9%98%20%ED%99%9C%EC%9A%A9.md) | DDIA 11장 |
| 메시지 브로커와 로그 기반 | 필수 | [12-01](../05_data/book/designing-data-intensive-applications/12-01.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%A0%84%EC%86%A1%20%E2%80%94%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EB%B8%8C%EB%A1%9C%EC%BB%A4%EC%99%80%20%EB%A1%9C%EA%B7%B8%20%EA%B8%B0%EB%B0%98%20%EB%B8%8C%EB%A1%9C%EC%BB%A4.md) | DDIA 12장 |
| 데이터베이스와 스트림 · CDC | 필수 | [12-02](../05_data/book/designing-data-intensive-applications/12-02.%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4%EC%99%80%20%EC%8A%A4%ED%8A%B8%EB%A6%BC.md) | DDIA 12장 |
| CEP · 윈도우 · 조인 | 필수 | [12-03](../05_data/book/designing-data-intensive-applications/12-03.%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20CEP%C2%B7%EC%9C%88%EB%8F%84%EC%9A%B0%C2%B7%EC%A1%B0%EC%9D%B8.md) | DDIA 12장 |
| 시간 추론과 내결함성 | 추천 | [12-04](../05_data/book/designing-data-intensive-applications/12-04.%EC%8B%9C%EA%B0%84%20%EC%B6%94%EB%A1%A0%EA%B3%BC%20%EB%82%B4%EA%B2%B0%ED%95%A8%EC%84%B1%C2%B712%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 12장 |
| 파생 데이터와 DB 언번들링 | 추천 | [13-02](../05_data/book/designing-data-intensive-applications/13-02.%EB%B0%B0%EC%B9%98%C2%B7%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%ED%86%B5%ED%95%A9%EA%B3%BC%20DB%20%EC%96%B8%EB%B2%88%EB%93%A4%EB%A7%81.md) | DDIA 13장 |
| 정확성과 신뢰 | 추천 | [13-04](../05_data/book/designing-data-intensive-applications/13-04.%EC%A0%95%ED%99%95%EC%84%B1%EA%B3%BC%20%EC%8B%A0%EB%A2%B0%C2%B713%EC%9E%A5%20%EC%A2%85%ED%95%A9.md) | DDIA 13장 |



## 손으로 확인하는 실습

> 노트 안에 실제로 있는 실습 자리만 적습니다. 지어낸 출처를 채우지 않았습니다.

책으로 배우는 로드맵이라 이 표가 비어 있습니다. DDIA 2판 정독 노트는 개념과 트레이드오프를 정리한 글이고, 복제 지연·합의·리밸런싱은 노드를 여럿 띄워야 재현되며 그 환경은 이 카테고리가 아니라 실제 운영 클러스터에 있습니다. 손으로 밟는 축은 [05_data MOC](../05_data/README.md)의 자체 노트와 [Spring 로드맵](spring-roadmap.md) 9단계가 맡습니다.



## 로드맵에 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| SQL 문법 · MySQL 실행 계획 · 인덱스 튜닝 | 소장 책에 없습니다. `05_data/02_relational` 의 자체 노트가 맡습니다 |
| JDBC · 커넥션 풀 · JPA · QueryDSL | 도구를 익히는 축입니다. `05_data/03_persistence` 와 [Spring 로드맵](spring-roadmap.md) 4단계가 맡습니다 |
| `@Transactional` 과 전파 · 롤백 규칙 | [Spring 로드맵](spring-roadmap.md) 4단계가 맡습니다. 6단계는 격리 수준까지입니다 |
| DB 덤프 · 로컬 이관 · 마이그레이션 도구 | `05_data/06_operations` 가 맡습니다. 순서를 말할 대상이 아닙니다 |
| DDIA 1판 요약 | `05_data/01_foundation` 에 따로 있습니다. 장 번호가 달라 섞으면 찾기 어렵습니다 |
| Kafka 브로커 설계와 운영 | `04_messaging` 이 정본입니다. 9단계는 로그 기반 브로커의 원리까지입니다 |
| 검색 애플리케이션 만들기 | Elasticsearch in Action 의 절반은 제품을 만드는 쪽입니다. 3단계는 색인 구조만 봅니다 |



## 경계

> 이 문서가 정하는 것과 인접 문서에 넘기는 것입니다.

이 문서는 **데이터 시스템의 원리를 여는 순서**를 정합니다. DDIA 2판이 척추이고, Database Internals 가 저장 엔진과 분산의 구현 층을, Patterns of Distributed Systems 가 패턴 카탈로그를 덧댑니다.

**절단선을 4단계 뒤에 그었습니다.** 1~4단계는 노드가 하나여도 생기는 문제이고, 5단계부터는 노드가 둘 이상일 때만 생깁니다. 복제 지연을 모델 설계 문제로 착각하지 않으려면 이 경계가 필요합니다.

**자료를 책과 정독 노트로 한정한 판입니다.** 도구와 프레임워크를 익힌 자체 노트 여든다섯 편은 순서의 근거로 쓰지 않았고, 그 결과 척추가 SQL·JPA·QueryDSL 이 아니라 DDIA 의 열네 장이 됐습니다. 도구 축이 필요하면 [05_data MOC](../05_data/README.md)를 폅니다.

**같은 증상을 세 문서가 다른 층에서 봅니다.** 조회가 느려졌을 때 이 문서는 인덱스 자료구조와 복제 지연을 보고, [Spring 로드맵](spring-roadmap.md)은 N+1 과 커넥션 풀을, [관측 가능성 로드맵](observability-roadmap.md)은 지표 분포와 SLO 를 봅니다.
