---
title: 05_data/docs MOC — 공식 문서·제품 사이트 정독
tags: [moc, data, official-docs, connection-pool]
status: draft
related:
  - ../README.md
  - connection-pool/README.md
  - ../../08_cloud/docs/README.md
updated: 2026-11-09
---

# 05_data/docs — 공식 문서·제품 사이트 정독

---

> 소장한 책이 다루지 않는 데이터 주제를 공식 문서·소스·제품 사이트를 1차 자료로 삼아 한 편씩 쓰는 자리입니다. 책 한 권을 장 순서대로 따라가는 노트는 [book/](../book/designing-data-intensive-applications/README.md)이 맡습니다.

## 폴더 규칙

> 바로 아래에는 제품마다 폴더를 하나씩 둡니다. 다만 여러 제품을 나란히 비교해야 뜻이 서는 주제는 주제 이름의 폴더 하나로 묶습니다.

| 폴더 | 1차 자료 | 묶는 기준 |
|------|----------|----------|
| [connection-pool/](connection-pool/README.md) | HikariCP·DBCP2·Go `database/sql`·PgBouncer 등의 공식 문서와 소스, DB 서버 매뉴얼 | 주제 |
| [galera/](galera/README.md) | Galera Cluster 공식 문서(복제·쿼럼·상태 전송·상태 변수)와 MariaDB Galera 문서 | 제품 |
| [mariadb-operator/](mariadb-operator/README.md) | MariaDB Operator 공식 문서(Logical·Physical Backup, PITR, API Reference)와 MariaDB Galera 백업 문서 | 제품 |

제품 폴더를 기본으로 두는 까닭은 공식 문서를 다시 폈을 때 그 제품의 노트가 어디 있는지 고민하지 않게 하려는 것입니다. 이 규약은 [08_cloud/docs](../../08_cloud/docs/README.md)와 같습니다. 그런데 커넥션 풀처럼 같은 문제를 여러 제품이 다르게 푸는 주제는, 제품마다 쪼개면 비교가 흩어집니다. 그런 주제만 주제 폴더로 두고, 위 표의 「묶는 기준」 열에 `주제` 라고 적어 예외임을 밝힙니다.



## 문서 목록

> 각 폴더 README 에 예정 편과 읽기 순서가 있습니다.

| 폴더 | 상태 | 예정 편 |
|------|------|--------|
| [connection-pool/](connection-pool/README.md) | 초안 | 8편 중 2편 (01-02·01-03). 앱 안의 풀 5편, 서버 쪽 풀러·과부하·다른 런타임 3편 |
| [galera/](galera/README.md) | 초안 | 3편 (01-01~01-03) |
| [mariadb-operator/](mariadb-operator/README.md) | 초안 | 1편 ([Backup·Restore](mariadb-operator/Backup·Restore.md)) |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [05_data MOC](../README.md) — 데이터 카테고리 전체 지도
- [03_persistence](../03_persistence/README.md) — JDBC·JPA 영속성 계층. 풀 관련 옛 노트가 있는 이관 대상 폴더
- [08_cloud/docs](../../08_cloud/docs/README.md) — 같은 규약을 먼저 쓴 docs 폴더
