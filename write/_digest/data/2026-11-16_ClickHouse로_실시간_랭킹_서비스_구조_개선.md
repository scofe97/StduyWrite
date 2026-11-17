> 출처: NotebookLM · 2026-11-16 · ClickHouse 기반 실시간 랭킹 서비스 아키텍처 심층 분석 리포트 (국내 증권 서비스 컨퍼런스 발표 자막 분석) · 분야: data-keywords · 미검증

## 요점

한 줄: 분석용 DW 를 함께 쓰며 Airflow 배치로 10~20초씩 걸리던 랭킹 집계를 서비스 전용 ClickHouse 로 옮기고, 데이터가 들어오는 순간 Materialized View 로 미리 집계해 응답을 200~300 ms 로 줄인 사례입니다.

- 출발 문제:
  - 1분마다 도는 Impala 집계 쿼리 하나가 10~20초 걸려 초 단위 랭킹이 불가능했습니다.
  - 기간·시장·카테고리 조합마다 Airflow Job 을 따로 만들어야 해서 랭킹 종류만큼 DAG 가 늘었습니다.
  - 분석가의 애드혹 쿼리와 같은 클러스터를 써서, 분석 부하가 몰리면 랭킹 갱신이 늦거나 실패했습니다.
- 바꾼 구조: 서비스 전용 ClickHouse 클러스터를 두고, Kafka(시세·체결·로그)는 Sink Connector 로, MySQL 종목 메타데이터는 Debezium CDC 로 넣습니다.
- 수집 방식 선택:
  - 내장 Kafka Engine 은 초당 60만 건 적재를 검증했지만, 컨슈머가 ClickHouse 서버 안에서 돌아 조회와 자원을 나눠 씁니다.
  - 토픽마다 Kafka Engine 테이블·MV·대상 테이블 3~4개를 관리해야 해서, 자체 수정한 Sink Connector 로 바꿨습니다.
- CDC 선택: ClickHouse 의 `MaterializedMySQL` 은 binlog 를 직접 읽어 복제하지만 당시 실험 기능이라 Debezium 을 골랐습니다.
- 최신 값 랭킹: 급상승·급하락처럼 마지막 시세만 중요한 데이터는 `ReplacingMergeTree` 로 정렬 키당 최신 버전만 남겨 훑는 행 수를 줄였습니다.
- 누적 랭킹:
  - 거래대금·거래량·인기(조회 UV)는 시간당 약 1억 건 로그가 들어옵니다. 원본을 바로 집계하면 쿼리당 600~700 ms 가 걸렸습니다.
  - Materialized View 가 insert 시점에 거래유의 종목을 거르고 분·시간·일 버킷으로 롤업해, 집계 상태를 `AggregatingMergeTree` 에 넣습니다.
  - 장 시작 1시간 로그 1억여 건이 중간 테이블에서 약 46만 건이 되고, 조회는 200~300 ms 가 됐습니다.
- 서빙: ClickHouse 는 높은 동시 요청에 약하므로 홈 차트는 캐시 층으로 받고, 조건 조합이 많은 상세·더보기만 ClickHouse 에 바로 묻습니다.
- 리포트 보완: `ReplacingMergeTree` 는 병합 전 중복 행이 남으므로 `FINAL` 이나 `argMax` 로 읽어야 한다고 덧붙입니다. DDL 골격(원본 MergeTree + TTL → MV → `countState`·`uniqState` → `countMerge`·`uniqMerge` 조회)도 보입니다.



## 핵심 키워드

| 키워드 | 한 줄 | 이미 있음 |
| :--- | :--- | :--- |
| 실시간 분석 시스템 (제품 분석) | 분석용 집계 쿼리를 사용자 대면 제품에서 저지연으로 답하는 DB 부류(ClickHouse·Druid·Pinot) | [운영 시스템 vs 분석 시스템](../../05_data/book/designing-data-intensive-applications/01-01.운영 시스템 vs 분석 시스템.md) |
| 분석·서비스 워크로드 격리 | 애드혹 분석 쿼리가 서비스 응답을 늦추지 않게 클러스터를 나누는 결정 | [운영 시스템 vs 분석 시스템](../../05_data/book/designing-data-intensive-applications/01-01.운영 시스템 vs 분석 시스템.md) (일부: 운영·분석 시스템을 나누는 이유, 서비스 전용 분석 클러스터 분리 없음) |
| 컬럼 지향 저장 | 쓰는 컬럼만 읽고 압축·벡터화로 대량 집계를 빠르게 하는 저장 방식 | [분석용 컬럼 지향 저장](../../05_data/book/designing-data-intensive-applications/04-05.분석용 컬럼 지향 저장.md) |
| MergeTree part 와 백그라운드 병합 | 작은 part 로 빠르게 쓰고 뒤에서 큰 part 로 합치며 정렬·압축하는 엔진 수명 주기 | [LSM 저장 엔진](../../05_data/book/designing-data-intensive-applications/04-02.LSM 저장 엔진.md) (일부: SSTable 컴팩션 원리, ClickHouse part·정렬 키 없음) |
| `ReplacingMergeTree` | 병합 때 정렬 키가 같은 행 중 버전이 가장 큰 행만 남기는 엔진 | |
| `FINAL`·`argMax` 조회 | 병합 전 남은 중복을 조회 시점에 걸러 최신 값을 보장하는 방법 | |
| `AggregatingMergeTree`·`-State`/`-Merge` | 집계 중간 상태를 저장하고 조회 때 합쳐 최종 값을 내는 엔진과 함수 짝 | |
| Materialized View (insert 트리거) | 원본에 insert 될 때마다 변환·집계 결과를 대상 테이블에 쓰는 ClickHouse 뷰 | [분석용 컬럼 지향 저장](../../05_data/book/designing-data-intensive-applications/04-05.분석용 컬럼 지향 저장.md) (일부: 결과를 복사해 두는 materialized view·data cube, insert 시점 증분 갱신 없음) |
| Kafka Engine vs Sink Connector | DB 안 내장 컨슈머와 DB 밖 Kafka Connect 사이의 자원 격리·운영 부담 비교 | [Kafka Connect 아키텍처와 운영 모드](../../04_messaging/01_Connect/04-01.Kafka Connect 아키텍처와 운영 모드.md) (일부: Connect 구조와 운영 모드, DB 내장 컨슈머와의 비교 없음) |
| Debezium CDC | DB 트랜잭션 로그를 읽어 변경을 Kafka 이벤트로 내보내는 커넥터 | [JDBC Source vs Debezium CDC 실전](../../04_messaging/01_Connect/04-03.JDBC Source vs Debezium CDC 실전.md) |
| `MaterializedMySQL` | ClickHouse 가 MySQL binlog 를 직접 읽어 데이터베이스를 복제하는 실험 기능 | |
| 컨슈머 랙 | 컨슈머가 읽은 위치가 최신 오프셋보다 뒤처진 정도로, 유입 급증 때 커지는 지표 | [신뢰성 검증과 모니터링](../../04_messaging/04_BrokerArchitecture/07-01.신뢰성 검증과 모니터링.md) |
| 샤딩 키와 핫스팟 | 인기 종목처럼 키가 몰리면 한 샤드에 부하가 쏠리는 문제와 키 설계 | [샤딩 개요와 키 범위 샤딩](../../05_data/book/designing-data-intensive-applications/07-01.샤딩 개요와 키 범위 샤딩.md) |
| 캐시 층·cache stampede | OLAP 앞에 캐시를 두어 동시 요청을 받고, 만료 순간 요청이 몰리는 문제를 막는 설계 | [캐싱 전략](../../05_data/01_foundation/01-07.캐싱 전략.md) |
| Redis Sorted Set 랭킹 | 점수 순 정렬 집합으로 단순 순위를 ms 단위로 답하는 방식 | [NoSQL 비교](../../05_data/01_foundation/01-06.NoSQL 비교.md) (일부: Sorted Set 리더보드 용도 한 줄, 다차원 필터·시간 창 재계산과의 비교 없음) |



## 자료와 실습

- 자료:
  - [AggregatingMergeTree 문서](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree): 집계 상태 저장 규격과 병합 동작을 봅니다. 같은 MergeTree 계열 문서에서 `ReplacingMergeTree`·`FINAL` 도 확인합니다.
  - [Incremental Materialized View 가이드](https://clickhouse.com/docs/en/materialized-view/incremental-materialized-view): MV 가 insert 시점 트리거로 동작하는 원리와 체이닝을 봅니다.
  - [ClickHouse Kafka 연동 문서](https://clickhouse.com/docs/en/integrations/kafka): Kafka Engine 과 Kafka Connect 를 비교합니다.
  - 『데이터 중심 애플리케이션 설계』 2판 4장(컬럼 지향 저장)과 12장(CDC·스트림 처리): 사전 집계가 왜 빠른지 원리를 봅니다. 정독 노트는 [designing-data-intensive-applications](../../05_data/book/designing-data-intensive-applications/README.md) 입니다.
  - 『Kafka: The Definitive Guide』 2판 컨슈머·Kafka Connect·스트림 처리 장: 랙 관리와 Sink Connector 분리 이유를 봅니다.
  - 코드: [ClickHouse/examples](https://github.com/ClickHouse/examples)(롤업·`uniqState` 스키마 예제)와 [clickhouse-kafka-connect](https://github.com/ClickHouse/clickhouse-kafka-connect)를 봅니다. 커넥터는 `src/main/java/com/clickhouse/kafka/connect/sink/`(배치·오프셋 커밋)를 봅니다.
  - 코드: ClickHouse 본체 `src/Storages/MergeTree/MergeTreeDataMergerMutator.cpp` 는 part 병합과 중복·집계 상태 축소를 실행하는 곳입니다.
- 실습:
  - Level 1: Docker 단일 노드에 모의 조회 로그 100만 건을 MergeTree 와 `AggregatingMergeTree` + MV 에 각각 넣어 행 수·용량·응답을 비교합니다. 함정은 병합 전 `ReplacingMergeTree` 에 중복이 보이는 것이라 `OPTIMIZE ... FINAL` 전후와 `system.parts` 를 봅니다. 완료: 집계 테이블이 수천 건 이하로 줄고 집계 쿼리가 50 ms 안에 끝납니다.
  - Level 2: Docker Compose 로 MySQL·Debezium·Kafka·Connect(ClickHouse Sink)·ClickHouse 를 잇고, MySQL 에서 종목을 거래유의로 바꾸면 랭킹에서 빠지게 합니다. 함정은 Debezium 의 `op`·`before`/`after` 중첩 구조를 스키마에 매핑할 때 나는 파싱 오류입니다. 완료: 메타 변경 뒤 1초 안에 랭킹 결과가 바뀝니다.
  - Level 3: k6 나 Go 로 이벤트 폭주와 동시 조회를 걸고, 홈 랭킹은 Redis 캐시(TTL 1~2초), 상세 필터는 ClickHouse 직접 조회로 나눈 API 를 만듭니다. 함정은 캐시 만료 순간의 stampede 와 인기 종목 키 쏠림입니다. 완료: `system.query_log` 로 보며 P99 응답이 300 ms 이하로 유지됩니다.



## 경고

- ⚠ 수치: 10~20초 → 200~300 ms, 초당 60만~70만 건, 1억 건 → 46만 건은 발표 수치를 리포트가 옮긴 것입니다. "약 50배", "약 217배" 는 리포트가 나눗셈으로 붙인 값입니다.
- ⚠ CPU 해석 충돌: 2절은 초당 70만 건 유입 때 CPU 가 30% 까지 올랐다고만 적습니다. 4절은 같은 현상을 샤딩 키에 따른 일부 노드 편중으로 다시 해석합니다. 발표 원문이 편중을 말했는지 확인하지 않았습니다.
- ⚠ 리포트 보완 주장: `FINAL`·`argMax` 권고, `rand()` 샤딩 권고, DDL 골격, Redis `ZSET` 비교는 발표가 아니라 리포트가 덧붙인 내용입니다.
- ⚠ 장 번호: 리포트는 『데이터 중심 애플리케이션 설계』를 1판 기준(3장·11장)으로 적었습니다. 정독 노트는 2판이라 컬럼 지향 저장이 4장, CDC 가 12장입니다. 『Kafka: The Definitive Guide』 2판의 "4장·8장·11장" 은 목차로 대조하지 않았습니다.
- ⚠ 자료 제목: "ClickHouse in Action / 공식 아키텍처 가이드" 는 책처럼 적혔지만 공식 웹 문서를 가리킵니다. 그래서 책 목록에서 뺐습니다. "Altinity Knowledge Base" 라고 단 링크도 실제로는 ClickHouse 공식 Kafka 연동 문서입니다.
- ⚠ `MaterializedMySQL` 상태: "당시 실험 기능" 은 발표 시점 기준입니다. 지금 상태는 공식 문서로 확인하지 않았습니다.
- ⚠ 이름: 발표 회사·발표자 이름과 행사 이름은 뺐습니다.
