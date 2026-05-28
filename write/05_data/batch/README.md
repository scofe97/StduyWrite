---
title: 05_data/batch — Spring Batch 중심 배치 처리 시리즈
tags: [moc, batch, spring-batch, airflow, spark]
status: draft
source:
  - https://docs.spring.io/spring-batch/reference/
related:
  - ../theory/03-01.배치 처리.md
  - ../theory/03-02.스트림 처리.md
  - ../../11_spring/05_aop/01-02.스프링 스케줄링 — @Scheduled에서 Quartz까지.md
updated: 2026-05-28
---

# 05_data/batch — Spring Batch 중심 배치 처리 시리즈

---

> 유한한 입력을 받아 새 출력을 만드는 *오프라인 처리* 를 Spring Batch 5.x 로 구현하는 방법을 정리합니다. 이론 측 *왜 배치인가* 는 [`../theory/03-01.배치 처리.md`](../theory/03-01.배치%20처리.md) 가 다루고, 여기는 *어떻게 짜는가* 만 담당합니다. Airflow·Spark 는 비교 축으로만 한 편씩 등장합니다.

## 왜 별도 묶음인가

`05_data/theory/03-01` 은 DDIA Ch.11 기준으로 *Unix → MapReduce → Dataflow 엔진* 의 진화와 Shuffle·분산 JOIN 같은 일반 메커니즘을 다룹니다. 그 다음 단계는 *그래서 내 Spring Boot 앱에서 배치를 어떻게 짜는가* 입니다. Spring Batch 가 그 자리를 채웁니다.

본 묶음은 면접에서 *Job·Step·Chunk·Tasklet 이 각자 무엇을 책임지는지, 왜 chunk 단위 트랜잭션이 디폴트인지, 재시작 시 어디서부터 다시 도는지* 를 설명할 수 있는 수준까지 끌어올립니다. 그 다음 *Spring Batch 가 못 푸는 자리* 를 Airflow 와 Spark 가 어떻게 받는지 1편씩 비교합니다.

## 학습 순서

1장 *Spring Batch 본편* 7편 → 2장 *Airflow 비교* 1편 → 3장 *Spark 비교* 1편 순서로 읽습니다. 1장만 끝내도 *현장에서 배치 잡 한 개를 처음부터 운영까지* 끌고 갈 수 있는 골격이 잡힙니다. 2·3장은 *언제 Spring Batch 를 벗어나는가* 의 결정 기준만 짚습니다.

| # | 문서 | 다루는 핵심 질문 |
|---|------|----------------|
| 01-01 | [Spring Batch 골격 — Job·Step·Chunk·Tasklet](01-01.Spring%20Batch%20골격%20—%20Job·Step·Chunk·Tasklet.md) | Job 이 Step 을 어떻게 담고, Step 안에서 Chunk 와 Tasklet 이 언제 갈리는가 |
| 01-02 | ItemReader·ItemProcessor·ItemWriter 3종 — 기본 구현체와 커스텀 | 3단 모델이 풀고자 한 문제, 기본 구현체 카탈로그, 언제 커스텀 |
| 01-03 | JobRepository 와 메타테이블 — JobInstance·JobExecution·StepExecution | 메타테이블 6개의 역할, 실패 추적·재실행이 왜 가능한가 |
| 01-04 | 재시작과 Checkpoint — ExecutionContext·Restartable·idempotent Step | 재시작 시작점, ExecutionContext 시리얼라이제이션, 멱등 Step 설계 |
| 01-05 | Parallel·Partition Batch — TaskExecutor·PartitionStep·Remote Partitioning | 단일 JVM 병렬 vs 다중 JVM 파티셔닝 선택 기준 |
| 01-06 | Bulk Insert·Update — JdbcBatchItemWriter 와 JPA batch_size 함정 | JdbcBatchItemWriter 의 진짜 batch 동작, JPA `hibernate.jdbc.batch_size`·`order_inserts` 함정 |
| 01-07 | 스케줄링과 운영 — @Scheduled·Quartz·Argo Workflows 연결 | `@Scheduled` 한계 → Quartz → Argo Workflows. Spring Batch 의 운영 인프라 경계 (ETL 패턴은 여기서 흡수) |
| 02-01 | Airflow DAG 모델 — Spring Batch 와의 책임 분담 비교 | Job 외부 오케스트레이션 (Airflow) vs Job 내부 처리 (Spring Batch). 둘은 계층이 다름 |
| 03-01 | Apache Spark 입문 — Spring Batch 한계와 분산 처리 전환점 | RDD·DataFrame·Structured Streaming 3 모델, 수직 확장 한계, 메모리·셔플 비용 트레이드오프 |

## 경계 기준

이 폴더는 *애플리케이션 안에서 돌리는 배치* 만 다룹니다. 다른 자리는 다음과 같이 갈립니다.

| 영역 | 다루는 것 | 위치 |
|------|---------|------|
| 본 폴더 (`batch/`) | Spring Batch 5.x 구현·운영, Airflow·Spark 와의 비교 | 여기 |
| 일반 이론 (DDIA) | 배치 vs 스트림 vs 온라인 모델, MapReduce, Shuffle | [`../theory/03-01.배치 처리.md`](../theory/03-01.배치%20처리.md) |
| 스트리밍 | 무한 이벤트 흐름 처리, Kafka Streams | [`../theory/03-02.스트림 처리.md`](../theory/03-02.스트림%20처리.md), [`../../04_messaging/06_StreamProcessing/`](../../04_messaging/06_StreamProcessing/) |
| Spring 스케줄러 | `@Scheduled`·Quartz 일반 | [`../../11_spring/05_aop/01-02.스프링 스케줄링 — @Scheduled에서 Quartz까지.md`](../../11_spring/05_aop/01-02.스프링%20스케줄링%20—%20%40Scheduled에서%20Quartz까지.md) |
| 메시지 큐 기반 배치 분산 | Kafka 위에서 도는 배치성 워크로드 | [`../../04_messaging/`](../../04_messaging/) |

ETL 패턴 자체는 *도구가 아닌 패턴* 이라 단독 편으로 두지 않고, `01-07` 의 운영 섹션과 `02-01` Airflow 비교 안에서 흡수합니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.2.x ~ 3.4.x | Spring Batch 5.x 자동 구성 |
| Spring Batch | 5.x | Jakarta 네임스페이스, 빌더 기반 DSL |
| Java | 17 / 21 | LTS 기준. virtual thread 사용처는 21+ |
| Airflow | 2.x (개념만) | 02-01 비교 한정 |
| Apache Spark | 3.x (개념만) | 03-01 비교 한정 |

## 사전 지식

본 카테고리는 다음을 가정합니다.

1. Spring Boot 3.x 의 빈 등록과 `@Configuration` 기본을 압니다. 모르면 [`../../11_spring/01_core/`](../../11_spring/01_core/) 를 먼저 읽습니다.
2. JDBC 트랜잭션과 `PlatformTransactionManager` 가 어떤 역할인지 한 문장으로 답할 수 있습니다. 모르면 [`../jdbc/01-01.커넥션 풀과 DataSource.md`](../jdbc/01-01.커넥션%20풀과%20DataSource.md) 와 [`../jpa/04-01.스프링 트랜잭션.md`](../jpa/04-01.스프링%20트랜잭션.md) 가 시작점입니다.
3. DDIA Ch.11 기준 *배치 vs 스트림* 의 차이를 한 줄로 답할 수 있습니다. 모르면 [`../theory/03-01`](../theory/03-01.배치%20처리.md) 부터입니다.
