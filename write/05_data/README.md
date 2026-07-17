---
title: 05_data — 데이터·데이터베이스 학습 MOC
tags: [moc, data, database, sql, persistence, distributed-systems, processing]
status: final
source:
  - https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/
related:
  - ./roadmap.md
  - ../04_messaging/README.md
  - ../11_spring/README.md
updated: 2026-07-15
---

# 05_data
---
> 데이터 모델과 관계형 DB부터 JDBC·JPA·QueryDSL, Redis, 배치 처리, 분산 데이터 이론과 DB 운영까지를 다룹니다. Kafka·Redpanda·CDC의 구체 구현과 운영은 `04_messaging/`에 두고, 이 카테고리에서는 데이터의 저장·조회·처리·일관성 원리를 다룹니다.

처음에는 [통합 학습 로드맵](./roadmap.md)을 읽습니다. 폴더 이름이나 도구가 아니라, Spring 백엔드가 데이터를 저장하고 조회하고 운영하는 흐름으로 자료를 연결합니다.

## 주제군

| 주제군 | 범위 | 진입점 |
|---|---|---|
| [01_foundation/](./01_foundation/README.md) | 데이터 모델·저장·트랜잭션·분산·배치·스트림의 공통 이론과 DDIA 정독 | [README](./01_foundation/README.md) |
| [02_relational/](./02_relational/README.md) | SQL·MySQL·InnoDB와 PostgreSQL의 관계형 DB 원리·제품 기능 | [README](./02_relational/README.md) |
| [03_persistence/](./03_persistence/README.md) | JDBC·JPA·Spring Data JPA·MyBatis·QueryDSL의 애플리케이션 영속성 계층 | [README](./03_persistence/README.md) |
| [04_processing/](./04_processing/README.md) | Spring Batch, Airflow·Spark 비교, 유한 데이터 처리의 구현과 운영 | [README](./04_processing/README.md) |
| [05_nonrelational/](./05_nonrelational/README.md) | Redis의 자료구조·캐시·세션·백업 | [README](./05_nonrelational/README.md) |
| [06_operations/](./06_operations/README.md) | 덤프·로컬 이관·테스트 DB·테스트 트랜잭션 | [README](./06_operations/README.md) |

## 경계 기준

`01_foundation/`은 제품 선택에 앞서는 공통 원리를 담당합니다. SQL·인덱스·MVCC 같은 관계형 DB의 동작은 `02_relational/`, 그 DB를 Spring 애플리케이션에서 다루는 방식은 `03_persistence/`에 둡니다.

Redis는 단순 캐시가 아니라 별도 저장소이므로 `05_nonrelational/`에서 다룹니다. Spring Batch와 Airflow·Spark의 책임 분담은 `04_processing/`에 두되, 스트림 처리의 일반 이론은 `01_foundation/`, 브로커·Kafka Streams·CDC의 구현은 `04_messaging/`이 SSOT입니다.

## 후속 후보

MinIO 같은 오브젝트 스토리지는 분산 파일시스템·오브젝트 스토어 이론을 넘어 제품 운영 문서가 다섯 편 이상 쌓일 때 별도 묶음으로 승격합니다. 그 전까지는 `01_foundation/`의 관련 정독 노트와 다른 카테고리의 활용 사례를 교차참조합니다.

## 관련 문서

- [통합 학습 로드맵](./roadmap.md) — Spring 백엔드 기준 추천 읽기 순서
- [04_messaging](../04_messaging/README.md) — Kafka·Redpanda·CDC 구현과 운영
- [11_spring](../11_spring/README.md) — Spring 프레임워크 전반의 진입점
