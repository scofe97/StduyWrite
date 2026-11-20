---
title: 02_os/docs/pacemaker — Pacemaker 와 Corosync 고가용성 클러스터
tags: [moc, pacemaker, corosync, high-availability, official-docs]
status: draft
source:
  - https://clusterlabs.org/projects/pacemaker/doc/2.1/Pacemaker_Explained/html/
  - https://clusterlabs.org/projects/pacemaker/doc/2.1/Clusters_from_Scratch/html/
related:
  - ../../README.md
  - ../../os-keywords.md
review:
  status: pending
updated: 2026-11-17
---

# 02_os/docs/pacemaker — Pacemaker 와 Corosync 고가용성 클러스터
---
> Pacemaker 와 Corosync 는 리눅스 환경에서 무중단 고가용성 서비스를 구현하는 표준 클러스터 스택으로, 노드 간 멤버십 통신과 과반 쿼럼 판정, CIB 기반 리소스 제약 조건 스케줄링 및 STONITH 펜싱 격리를 계층별로 나누어 수행합니다.

## 폴더 소개

> 리눅스 커널과 네트워크 계층 위에서 2대 이상의 서버를 하나로 묶어 서비스 가용성을 보장하는 Pacemaker·Corosync 공식 문서를 정독하고 핵심 동작 원리를 정리합니다.

단일 서버 인프라는 하드웨어 결함이나 프로세스 비정상 종료 시 서비스 중단을 피할 수 없습니다.
고가용성 클러스터는 여러 대의 서버를 묶어 운영합니다.
한 노드에 장애가 생기더라도 다른 정상 노드로 서비스를 넘겨 가용성을 유지합니다.

이 폴더에서는 Corosync 와 Pacemaker, 그리고 에이전트의 상호작용을 공식 문서 규약에 따라 분석합니다.
각 컴포넌트가 맡은 책임과 통신 방식을 명확히 구분합니다.
스플릿 브레인을 방지하는 STONITH 펜싱 순서와 2노드 쿼럼 계산을 다룹니다.
가상 IP 이동과 Gratuitous ARP, 리소스 제약 조건과 장애 복구 흐름을 연재 순서대로 학습합니다.



## 문서 목록

> 01 번대는 Pacemaker 와 Corosync 클러스터의 핵심 원리와 운영 기법을 다루는 연재입니다. 번호가 읽기 순서입니다.

| 번호 | 제목 | 핵심 내용 | 주 1차 자료 |
|---|---|---|---|
| 01-01 | [Cluster Architecture·Quorum·Fencing](./01-01.Cluster%20Architecture·Quorum·Fencing.md) | Corosync 와 Pacemaker 및 리소스 에이전트 계층 분담, 2노드 쿼럼 한계와 `two_node: 1`, `no-quorum-policy` 설정값, STONITH 펜싱 격리 원리와 `stonith-enabled=false` 의 위험성, 가상 IP(`IPaddr2`) 이동과 Gratuitous ARP 전송 | ClusterLabs Pacemaker Explained 2.1 §1.2·§3.3·§8, Corosync `man votequorum`, Resource Agents `IPaddr2` |
| 01-02 | [Cluster Status·Resource Constraints·Failure Handling](./01-02.Cluster%20Status·Resource%20Constraints·Failure%20Handling.md) | 클러스터 상태 확인과 CIB 구조, 리소스 제약 조건(location, colocation, order), 장애 감지와 모니터링 동작, failcount 누적과 migration-threshold 기반 페일오버 및 리소스 정리 절차 | ClusterLabs Pacemaker Explained 2.1 §6·§7, Clusters from Scratch 2.1 §6·§7 |



## 1차 자료

> ClusterLabs 공식 문서 및 시스템 매뉴얼입니다. Pacemaker 문서는 2.1 판 기준으로 검증했습니다.

### Pacemaker 공식 문서
- [Pacemaker Explained (2.1)](https://clusterlabs.org/projects/pacemaker/doc/2.1/Pacemaker_Explained/html/): 클러스터 아키텍처, CIB 속성, 리소스 제약 조건, 펜싱 설정 및 옵션 규약
- [Clusters from Scratch (2.1)](https://clusterlabs.org/projects/pacemaker/doc/2.1/Clusters_from_Scratch/html/): 활성/수동 2노드 클러스터 구축, pcs 명령 체계, 아파치 및 DRBD 연동 절차

### Corosync 공식 문서 및 매뉴얼
- [votequorum(5) 매뉴얼](https://manpages.debian.org/testing/corosync/votequorum.5.en.html): `two_node`, `wait_for_all`, `last_man_standing` 쿼럼 산출 규약
- [corosync.conf(5) 매뉴얼](https://manpages.debian.org/testing/corosync/corosync.conf.5.en.html): 토템 통신 설정 및 노드 리스트 구성

### 리소스 에이전트 소스 및 표준
- [ClusterLabs resource-agents IPaddr2](https://github.com/ClusterLabs/resource-agents/blob/main/heartbeat/IPaddr2): `ocf:heartbeat:IPaddr2` 의 Gratuitous ARP 전송 로직 및 매개변수
- [Open Cluster Framework(OCF) Resource Agent 표준](https://clusterlabs.org/projects/pacemaker/doc/2.1/Pacemaker_Explained/html/resources.html#resource-standards): 에이전트 명령 인자와 반환 코드 규약



## 관련 문서

> 고가용성 인프라 및 운영체제 네트워크 상위 문서입니다.

- [02_os/ MOC](../../README.md) — OS 공통 기반 및 네트워크
- [OS 학습 로드맵](../../os-keywords.md) — 고가용성 클러스터 및 네트워크 L2/L3 계층 키워드
