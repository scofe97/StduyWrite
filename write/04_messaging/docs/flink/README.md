---
title: 04_messaging/docs/flink — Apache Flink 공식 문서 읽기 지도
tags: [moc, flink, flink-sql, stream-processing, official-docs]
status: draft
source:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/
related:
  - ../README.md
  - ../../README.md
  - ../../06_StreamProcessing/01-01.Kafka Streams.md
  - ../../08_advanced/01_variants/01-03.스트림 처리 진화.md
updated: 2026-11-18
---

# 04_messaging/docs/flink — Apache Flink 공식 문서 읽기 지도

---

> Apache Flink 2.3 공식 문서에서 SQL·Table API, 배포, 운영 세 갈래만 골라 어느 쪽을 어떤 순서로 읽을지 적은 지도입니다. 정독 편은 아직 한 편도 쓰지 않았고, 스트림 처리 개념은 이웃 노트 링크로 대신합니다.

## 예정 편

> 순서 번호가 읽는 순서이고, 제목은 그 편이 다룰 공식 문서 쪽의 제목을 `·` 로 이었습니다. 묶음 폴더는 아직 만들지 않았고 그 묶음의 첫 편을 쓸 때 만듭니다.

| 순서 | 묶음(예정) | 제목 | 공식 주소 | 한 줄 소개 |
|------|-----------|------|----------|-----------|
| 01-01 | `table-sql/` | Flink SQL·SQL Client | [sql/overview](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/overview/) · [sql/interfaces/sql-client](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/interfaces/sql-client/) | 표준 SQL 로 스트리밍·배치 애플리케이션을 만드는 Flink SQL 개요. Java·Scala 코드 없이 테이블 프로그램을 쓰고 클러스터에 제출하는 SQL Client |
| 01-02 | `table-sql/` | CREATE Statements·INSERT Statement | [sql/reference/ddl/create](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/ddl/create/) · [sql/reference/dml/insert](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/dml/insert/) | 테이블·뷰·함수를 카탈로그에 등록하는 CREATE 문과 테이블에 행을 넣는 INSERT 문 |
| 01-03 | `table-sql/` | Table & SQL Connectors·Apache Kafka SQL Connector | [connectors/table/overview](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/connectors/table/overview/) · [connectors/table/kafka](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/connectors/table/kafka/) | 외부 시스템을 테이블 소스와 싱크로 등록하는 방법. Kafka 토픽을 읽고 쓰는 커넥터 |
| 01-04 | `table-sql/` | Windowing table-valued functions (Windowing TVFs)·Window Aggregation·Joins | [sql/reference/queries/window-tvf](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/window-tvf/) · [sql/reference/queries/window-agg](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/window-agg/) · [sql/reference/queries/joins](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/joins/) | 스트림을 유한한 크기의 버킷으로 나누는 윈도우 함수, `window_start`·`window_end` 열로 묶는 윈도우 집계, dynamic table 위의 여러 조인 유형 |
| 01-05 | `table-sql/` | Concepts & Common API·TableEnvironment | [dev/table/common](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/table/common/) · [dev/table/table_environment](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/table/table_environment/) | Table 을 등록하고 질의하고 내보내는 Table API·SQL 프로그램의 공통 구조. Table API 의 중심 개념인 TableEnvironment 의 공개 인터페이스 |
| 02-01 | `deployment/` | Deployment·Docker Setup | [deployment/overview](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/overview/) · [deployment/resource-providers/standalone/docker](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/resource-providers/standalone/docker/) | Flink 클러스터의 구성 요소와 그 구현을 훑는 배포 개요. Docker 컨테이너로 한 대에 클러스터를 띄우는 설정 |
| 02-02 | `deployment/` | Kubernetes Setup·Native Kubernetes | [deployment/resource-providers/standalone/kubernetes](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/resource-providers/standalone/kubernetes/) · [deployment/resource-providers/native_kubernetes](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/resource-providers/native_kubernetes/) | Kubernetes 위에 standalone 방식으로 Session 클러스터를 올리는 방법과 Flink 를 Kubernetes 에 네이티브로 배포하는 방법 |
| 02-03 | `deployment/` | High Availability·Kubernetes HA Services | [deployment/ha/overview](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/ha/overview/) · [deployment/ha/kubernetes_ha](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/deployment/ha/kubernetes_ha/) | JobManager 가 죽어도 제출된 애플리케이션을 다시 실행하게 하는 고가용성 설정과 Kubernetes 를 쓰는 HA 서비스 |
| 03-01 | `operations/` | Checkpoints·Savepoints·Checkpoints vs. Savepoints | [ops/state/checkpoints](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/checkpoints/) · [ops/state/savepoints](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/savepoints/) · [ops/state/checkpoints_vs_savepoints](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/checkpoints_vs_savepoints/) | 상태와 스트림 위치를 복구할 수 있게 하는 체크포인트, 스트리밍 잡 실행 상태의 일관된 이미지인 세이브포인트, 둘의 차이 |
| 03-02 | `operations/` | State Backends | [ops/state/state_backends](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/state_backends/) | 상태를 내부에서 어떻게 표현하고 체크포인트 때 어디에 저장할지를 정하는 State Backend |
| 03-03 | `operations/` | Task Failure Recovery | [ops/state/task_failure_recovery](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/state/task_failure_recovery/) | 태스크가 실패했을 때 어느 태스크를 언제 다시 시작할지 정하는 재시작 전략과 failover 전략 |
| 03-04 | `operations/` | Metrics·Monitoring Checkpointing·Monitoring Back Pressure | [ops/metrics](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/metrics/) · [ops/monitoring/checkpoint_monitoring](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/monitoring/checkpoint_monitoring/) · [ops/monitoring/back_pressure](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/monitoring/back_pressure/) | 메트릭을 모아 외부 시스템에 내보내는 메트릭 시스템. 웹 화면의 체크포인트 탭과 back pressure 탭 |
| 03-05 | `operations/` | Upgrading Applications and Flink Versions·Production Readiness Checklist | [ops/upgrading](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/upgrading/) · [ops/production_ready](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/ops/production_ready/) | 오래 도는 스트리밍 애플리케이션을 고치거나 다른 Flink 클러스터로 옮기는 방법. 운영에 올리기 전에 검토할 설정 항목 목록 |

묶음 이름은 번호 없는 영어 kebab 이름이고, 배우는 순서는 장 번호 01·02·03 이 맡습니다.

Apache Kafka SQL Connector 쪽의 Dependencies 절에는 2026-11-18 현재 "There is no connector (yet) available for Flink version 2.3." 이라고 적혀 있습니다. 01-03 편을 쓸 때 2.3 용 커넥터가 나왔는지 다시 확인합니다.



## 읽는 순서

> 예정 편보다 공식 튜토리얼과 Hands-On Training 쪽 네 편을 먼저 읽습니다. 각 쪽 끝의 Next Steps·Further Reading 절이 예정 편의 쪽으로 이어지기 때문입니다.

| 차례 | 공식 쪽 | 그 쪽이 다루는 것 | 끝의 링크가 이어지는 예정 편 |
|------|---------|------------------|---------------------------|
| 1 | [Flink SQL Tutorial](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/getting-started/quickstart-sql/) | SQL Client 를 띄워 소스 테이블을 만들고, 연속 쿼리를 돌리고, 결과를 싱크 테이블로 내보내는 실습 | 01-01, 01-02, 01-03 |
| 2 | [Learn the Table API](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/learn-flink/table_api/) | Table API 로 스트리밍 분석 애플리케이션을 쓰기 시작할 만큼의 개요 | 01-03, 01-05 |
| 3 | [Flink Operations Playground](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/getting-started/flink-operations-playground/) | Web UI 로 배포하고 지켜보기, 장애 복구 관찰, savepoint 로 잡 업그레이드, 스케일 조정, REST API 로 메트릭 조회, CLI 사용 | 02-01, 02-03, 03-01, 03-04 |
| 4 | [Fault Tolerance via State Snapshots](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/learn-flink/fault_tolerance/) | state backend, checkpoint storage, 상태 스냅샷 | 03-01, 03-02, 03-03, 03-04 |

차례는 묶음 순서를 따랐습니다. 공식 문서 첫 화면은 튜토리얼인 1번·3번을 먼저 권하고, 더 깊이 볼 때 Hands-On Training 에 속한 2번·4번을 권합니다. 4번은 내비게이션에 Fault Tolerance 라는 짧은 이름으로 나옵니다.

Flink SQL Tutorial 은 실행 중인 클러스터가 있어야 하므로 [First Steps](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/getting-started/local_installation/) 쪽으로 클러스터를 먼저 띄웁니다.

01-04·02-02·03-05 는 네 쪽 어디에서도 바로 이어지지 않습니다. 이 세 편은 같은 묶음의 앞 편을 읽은 뒤 순서 번호대로 읽습니다.



## 이 지도에서 뺀 것

> SQL·Table API, 배포, 운영 세 갈래 밖의 섹션은 예정 표에 올리지 않았습니다.

DataStream API, Concepts 섹션, Internals, CEP 라이브러리, YARN 배포, 배치 전용 섹션, Hive Compatibility 를 뺐습니다. Concepts 섹션이 다루는 상태·시간·내결함성 개념은 아래 이웃 노트가 대신합니다. Concepts 아래에 있는 Dynamic Tables 쪽과 Time Attributes 쪽도 같은 기준으로 표에 올리지 않았습니다. 다만 Flink SQL Tutorial 의 Next Steps 절이 이 두 쪽을 가리키므로 01 묶음 편을 쓸 때 다시 넣을지 정합니다.



## 이웃 노트

> Flink 문서를 읽을 때 필요한 스트림 처리 개념은 이미 쓴 노트 다섯 편에 있어 여기서 다시 쓰지 않습니다.

| 노트 | 자리 | 그 노트에서 볼 것 |
|------|------|------------------|
| [스트림 처리 — CEP·윈도우·조인](../../../05_data/book/designing-data-intensive-applications/12-03.스트림%20처리%20—%20CEP·윈도우·조인.md) | 『Designing Data-Intensive Applications』 12장 정독 노트 | 윈도우 유형과 스트림 조인의 세 가지 유형 |
| [시간 추론과 내결함성·12장 종합](../../../05_data/book/designing-data-intensive-applications/12-04.시간%20추론과%20내결함성·12장%20종합.md) | 같은 책 12장 정독 노트 | 이벤트 시간과 처리 시간, 지각 이벤트 처리, 내결함성과 exactly-once |
| [결정적 스트림 처리 — 워터마크와 스트림 타임](../../../03_architecture/05_edd/02-03.결정적%20스트림%20처리%20—%20워터마크와%20스트림%20타임.md) | 03_architecture/05_edd | 워터마크의 의미와 스트림 타임 |
| [Kafka Streams](../../06_StreamProcessing/01-01.Kafka%20Streams.md) | 04_messaging/06_StreamProcessing | KStream·KTable, State Store, 윈도우 집계를 Kafka Streams 로 본 설명 |
| [스트림 처리 진화](../../08_advanced/01_variants/01-03.스트림%20처리%20진화.md) | 04_messaging/08_advanced | Kafka Streams·ksqlDB·Flink·IVM 스트림 DB 를 나란히 놓은 비교. Flink 는 「단계 4 — Apache Flink」 절 |



## 1차 자료

> 주소는 모두 `flink-docs-release-2.3` 경로로 고정했습니다. 안정판 별칭 주소는 2026-11-18 현재 2.3 문서를 보여 주지만 다음 릴리스가 나오면 대상이 바뀝니다.

### 확인한 주소

위 두 표와 본문에 적은 공식 주소 32개, 그리고 아래 두 주소는 2026-11-18 에 직접 열어 200 응답과 쪽 제목을 확인했습니다.

- 문서 첫 화면: [Apache Flink Documentation](https://nightlies.apache.org/flink/flink-docs-release-2.3/)
- Hands-On Training 개요: [Learn Flink: Hands-On Training](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/learn-flink/overview/)



## 관련 문서

- [docs MOC](../README.md) — 04_messaging/docs 폴더 규칙과 전체 목록
- [04_messaging MOC](../../README.md) — 메시징 카테고리 전체 지도
