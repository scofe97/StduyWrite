---
title: 05_data/docs/mariadb-operator — MariaDB Operator 공식 문서 정독 계획
tags: [moc, mariadb-operator, mariadb, kubernetes, backup, restore, official-docs]
status: draft
related:
  - ../README.md
  - ../galera/README.md
  - ../galera/01-02.State Transfers·Restarting the Cluster.md
  - ../../../08_cloud/docs/kubernetes/operations/클러스터 업그레이드·ETCD 백업·복구.md
review:
  status: pending
updated: 2026-11-17
---

# 05_data/docs/mariadb-operator — MariaDB Operator 공식 문서 정독 계획

---

> Kubernetes 환경에서 MariaDB 의 수명주기와 고가용성 및 백업·복구를 선언적으로 관리하는 MariaDB Operator 공식 문서를 정독하는 공간입니다. Operator 패턴에 기반한 컨트롤러 리콘사일 메커니즘과 커스텀 리소스(CR) 구조, 장애 시나리오별 복구 전략을 다룹니다.

## 왜 공식 문서로 쓰는가

> 분산 데이터베이스의 운영 자동화는 일반 서적에 없으며 컨트롤러 구현체와 CRD 명세에만 정의되어 있습니다.

전통적인 데이터베이스 서적은 셸 스크립트 기반의 수동 백업이나 물리 복제 원리만을 설명합니다. 반면 컨테이너 환경에서는 파드 재시작, 동적 IP 변경, 볼륨 마운트 격리라는 분산 제약이 추가됩니다. MariaDB Operator 는 이러한 제약을 커스텀 리소스 정의(CRD)와 리콘사일 제어 루프로 해결합니다.

백업 주기와 S3 스토리지 연동, 임시 스테이징 볼륨 지정은 공식 문서와 CRD 스키마에서만 검증할 수 있습니다. Galera 환경의 비복제 시스템 테이블 격리 역시 구현체 매뉴얼 확인이 필수적입니다. 운영 환경의 데이터 유실을 막으려면 구현체가 보장하는 API 계약을 정확히 확인해야 합니다.



## 문서 목록

> MariaDB Operator 가 제공하는 선언적 백업 및 복구 메커니즘을 단독 편으로 구성하여 집중적으로 다룹니다.

| 번호 | 제목 | 다룰 내용 | 주 1차 자료 |
|---|---|---|---|
| [단독](./Backup·Restore.md) | [Backup·Restore](./Backup·Restore.md) | Operator 리콘사일 루프, Backup CR 과 스토리지 구성, Restore CR 과 복구 흐름, 시나리오별 복구 전략(물리 백업 기반 PITR 과 그 지원 토폴로지 포함), Galera 단일 백업 원칙 | MariaDB Operator 공식 문서(Logical Backup, Physical Backup, PITR), CRD API Reference, MariaDB Galera 백업 문서 |



## 1차 자료

> 공식 문서와 GitHub 저장소 구현 명세를 확인된 자료와 검토 후보로 나누어 관리합니다. 저장소 주소는 릴리스 버전 태그를 고정하여 기록합니다.

### 확인한 주소

아래는 2026-11-17 에 직접 열어 확인한 공식 문서 및 저장소 주소입니다. 버전 태그는 `v26.10.2` 기준입니다.

- GitHub 저장소: [mariadb-operator/mariadb-operator](https://github.com/mariadb-operator/mariadb-operator)
- 논리 백업 가이드: [Logical Backups](https://github.com/mariadb-operator/mariadb-operator/blob/v26.10.2/docs/logical_backup.md)
- 물리 백업 가이드: [Physical Backups](https://github.com/mariadb-operator/mariadb-operator/blob/v26.10.2/docs/physical_backup.md)
- 시점 복구 가이드: [Point-In-Time-Recovery](https://github.com/mariadb-operator/mariadb-operator/blob/v26.10.2/docs/pitr.md)
- CRD API 레퍼런스: [CRD API Reference](https://github.com/mariadb-operator/mariadb-operator/blob/v26.10.2/docs/api_reference.md)
- Galera 토폴로지 연동: [Galera](https://github.com/mariadb-operator/mariadb-operator/blob/v26.10.2/docs/galera.md)
- MariaDB 공식 문서: [mariadb-dump](https://mariadb.com/docs/server/clients-and-utilities/backup-restore-and-import-clients/mariadb-dump)
- MariaDB 공식 문서: [Full Backup and Restore with mariadb-backup](https://mariadb.com/docs/server/server-usage/backup-and-restore/mariadb-backup/full-backup-and-restore-with-mariadb-backup)
- MariaDB 공식 문서: [Backing Up a MariaDB Galera Cluster](https://mariadb.com/docs/galera-cluster/galera-management/general-operations/backing-up-a-mariadb-galera-cluster)
- Kubernetes 공식 문서: [Operator Pattern](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/)

MariaDB Knowledge Base 주소(mariadb.com/kb)는 일부가 문서 첫 화면으로 떨어집니다. 그래서 위 MariaDB 주소는 넘어간 뒤의 mariadb.com/docs 주소로 적었습니다.

### 확인 전 후보

- MariaDB Operator 저장소의 [Physical Backups 「Target policy」](https://github.com/mariadb-operator/mariadb-operator/blob/v26.10.2/docs/physical_backup.md#target-policy) 가 Galera 에서 어느 Pod 를 replica 로 보는지 — 소스로 확인 전



## 참고할 책 장

> 분산 데이터베이스 이론과 Kubernetes 확장 패턴을 다룬 책 장을 연결합니다. 본문에서 기초 배경 개념을 참조할 때 맥락 링크로 활용합니다.

| 책 | 장 | 다루는 개념과 연계 |
|---|---|---|
| Kubernetes Patterns | [28장 Operator](../../../08_cloud/book/kubernetes-patterns/28-01.Operator%20—%20CRD로%20도메인%20지식을%20자동화하기.md) | 컨트롤러 감시 루프와 커스텀 리소스 기반 상태 수렴 메커니즘 |
| 데이터 중심 애플리케이션 설계 | 6장 복제 (06-02) | 노드 장애 처리와 복제 로그 및 백업 스냅샷의 한계 |
| 데이터 중심 애플리케이션 설계 | 9장 일관성과 합의 (09-03) | 단일 진실 정의와 스플릿 브레인 방지 원리 |



## 관련 문서

> 저장소 내에 이미 정리된 데이터베이스 복제 및 분산 인프라 관련 노트입니다.

- [docs MOC](../README.md) — 05_data/docs 폴더 규칙과 전체 목록
- [Backup·Restore](./Backup·Restore.md) — MariaDB Operator 백업 및 복구 단독 편
- [01-02.State Transfers·Restarting the Cluster](../galera/01-02.State%20Transfers·Restarting%20the%20Cluster.md) — Galera 복구 및 단일 백업 연계
- [클러스터 업그레이드와 ETCD 백업·복구](../../../08_cloud/docs/kubernetes/operations/클러스터%20업그레이드·ETCD%20백업·복구.md) — Kubernetes 상태 백업
