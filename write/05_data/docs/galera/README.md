---
title: 05_data/docs/galera — Galera Cluster 공식 문서 정독 계획
tags: [moc, galera, mariadb, replication, quorum, official-docs]
status: draft
related:
  - ../README.md
  - ../../book/designing-data-intensive-applications/06-01.복제%20개요와%20단일%20리더.md
  - ../../book/designing-data-intensive-applications/06-02.노드%20장애%20처리와%20복제%20로그.md
  - ../../book/designing-data-intensive-applications/09-03.진실·거짓·시스템%20모델.md
review:
  status: pending
updated: 2026-11-17
---

# 05_data/docs/galera — Galera Cluster 공식 문서 정독 계획

---

> 관계형 데이터베이스의 동기식 다중 마스터 복제를 구현하는 Galera Cluster 의 공식 문서를 정독하고 정리하는 공간입니다. 복제 원리와 쿼럼 판정, 장애 복구와 상태 전송, 흐름 제어와 상태 진단까지 세 편의 연재로 다룹니다.

## 왜 공식 문서로 쓰는가

> 일반 분산 시스템 서적은 비동기 복제나 2단계 커밋을 주로 다루고, 인증 기반 동기 복제의 구체적 동작은 라이브러리 매뉴얼에만 있습니다.

Galera 는 커밋 시점에 쓰기 집합을 검증하는 인증 기반 복제를 사용합니다. 쿼럼 상실 기준, 캐시 크기에 따른 복구 방식 전환, 느린 노드가 전체 클러스터를 멈추는 흐름 제어는 공식 문서와 구현 소스에만 기술되어 있습니다. 운영 환경의 장애를 진단하려면 매뉴얼에 명시된 상태 변수와 시스템 매개변수의 기준값을 확인해야 합니다.



## 문서 목록

> 01 번대는 클러스터 핵심 복제 메커니즘과 운영 흐름을 순서대로 다루는 연재입니다. 앞 편의 개념이 뒤 편의 동작 원리로 이어집니다.

| 번호 | 제목 | 다룰 내용 | 주 1차 자료 |
|---|---|---|---|
| [01-01](./01-01.Certification-Based%20Replication·Quorum%20Components.md) | Certification-Based Replication·Quorum Components | 커밋 시점 충돌 검사와 과반수 쿼럼 판정, 2노드 구성 한계와 garbd 중재자, 단일 쓰기 집중화 이유 | Certification-Based Replication, Understanding Quorum, Quorum Control with Weighted Votes |
| [01-02](./01-02.State%20Transfers·Restarting%20the%20Cluster.md) | State Transfers·Restarting the Cluster | IST 와 SST 전송 방식 비교, gcache 크기와 이탈 허용 시간, 전체 정지 뒤 안전한 부트스트랩 순서 | Rapid Node Recovery with IST and the GCache, Introduction to SSTs, Resetting the Quorum |
| [01-03](./01-03.Database%20Server%20Status%20Variables·Flow%20Control.md) | Database Server Status Variables·Flow Control | wsrep 상태 변수로 읽는 클러스터 건강, 수신 큐 임계값과 흐름 제어 메커니즘 | Galera Status Variables, Monitoring the Cluster, Flow Control |



## 1차 자료

> 공식 문서와 구현 소스 주소를 확인된 자료와 검토 후보로 나누어 관리합니다. MariaDB 문서 주소에는 버전이 없으므로 직접 열어 본 날짜를 함께 적습니다.

### 확인한 주소

옛 Galera 문서 주소(galeracluster.com/library)는 2026-11 현재 mariadb.com/docs 로 넘어갑니다. MariaDB Knowledge Base 주소(mariadb.com/kb)는 일부가 문서 첫 화면으로 떨어집니다. 아래는 2026-11-17 에 직접 열어 확인한 주소입니다.

- Galera 구조: [Certification-Based Replication](https://mariadb.com/docs/galera-cluster/galera-architecture/certification-based-replication), [Introduction to Galera Architecture](https://mariadb.com/docs/galera-cluster/galera-architecture/introduction-to-galera-architecture), [Quorum Control with Weighted Votes](https://mariadb.com/docs/galera-cluster/galera-architecture/quorum-control-with-weighted-votes)
- 쿼럼과 운영: [Understanding Quorum, Monitoring, and Recovery](https://mariadb.com/docs/galera-cluster/high-availability/understanding-quorum-monitoring-and-recovery)(garbd 포함), [Monitoring MariaDB Galera Cluster](https://mariadb.com/docs/galera-cluster/high-availability/monitoring-mariadb-galera-cluster)(노드 상태 전이), [Resetting the Quorum](https://mariadb.com/docs/galera-cluster/high-availability/resetting-the-quorum-cluster-bootstrap)
- 상태 전송: [Rapid Node Recovery with IST and the GCache](https://mariadb.com/docs/galera-cluster/high-availability/rapid-node-recovery-with-ist-and-the-gcache), [Introduction to State Snapshot Transfers (SSTs)](https://mariadb.com/docs/galera-cluster/high-availability/state-snapshot-transfers-ssts-in-galera-cluster/introduction-to-state-snapshot-transfers-ssts)
- 장애 복구와 백업: [Recovering a Primary Component](https://mariadb.com/docs/galera-cluster/high-availability/recovering-a-primary-component), [Backing Up a MariaDB Galera Cluster](https://mariadb.com/docs/galera-cluster/galera-management/general-operations/backing-up-a-mariadb-galera-cluster)
- 변수: [Galera Cluster System Variables](https://mariadb.com/docs/galera-cluster/reference/galera-cluster-system-variables)(`wsrep_retry_autocommit`), [Galera Cluster Status Variables](https://mariadb.com/docs/galera-cluster/reference/galera-cluster-status-variables)

### 확인 전 후보

- Percona XtraDB Cluster 공식 매뉴얼: Galera 4 기반 다중 마스터 운영 가이드와 성능 튜닝 권장안
- Codership wsrep API 저장소: 트랜잭션 수명주기 훅과 복제 공급자 인터페이스 정의



## 참고할 책 장

> 분산 데이터베이스의 기본 이론을 다룬 책 장을 연결합니다. 본문에서 기초 배경 개념을 참조할 때 맥락 링크로 활용합니다.

| 책 | 장 | 다루는 개념과 연계 |
|---|---|---|
| 데이터 중심 애플리케이션 설계 | 6장 복제 (06-01·06-02·06-04) | 단일 리더와 다중 리더의 쓰기 충돌 기초 |
| 데이터 중심 애플리케이션 설계 | 8장 트랜잭션 (08-04) | 2단계 커밋(2PC) 분산 트랜잭션과의 구조적 차이 |
| 데이터 중심 애플리케이션 설계 | 9장 일관성과 합의 (09-03) | 불신뢰 네트워크에서 과반수 쿼럼으로 진실을 정의하는 원리 |



## 관련 문서

> 저장소 내에 이미 정리된 분산 데이터베이스 및 복제 관련 노트입니다.

- [docs MOC](../README.md) — 05_data/docs 폴더 규칙과 전체 목록
- [01-01.Certification-Based Replication·Quorum Components](./01-01.Certification-Based%20Replication·Quorum%20Components.md) — Galera 1편
- [01-02.State Transfers·Restarting the Cluster](./01-02.State%20Transfers·Restarting%20the%20Cluster.md) — Galera 2편
- [01-03.Database Server Status Variables·Flow Control](./01-03.Database%20Server%20Status%20Variables·Flow%20Control.md) — Galera 3편
- [DDIA 06-01 복제 개요와 단일 리더](../../book/designing-data-intensive-applications/06-01.복제%20개요와%20단일%20리더.md) — 단일 리더 복제 모델
- [DDIA 09-03 진실·거짓·시스템 모델](../../book/designing-data-intensive-applications/09-03.진실·거짓·시스템%20모델.md) — 과반수 투표와 쿼럼 성립 조건
