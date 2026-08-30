---
title: Mastering Prometheus (정독 노트 MOC)
tags: [moc, observability, prometheus, thanos, promql, book]
status: draft
related:
  - ../../README.md
  - ../dgos_opensearch/README.md
updated: 2026-07-10
---

# Mastering Prometheus
---
> Packt 단행본(ISBN 9781805125662)입니다. Prometheus 를 *설치하는 법*이 아니라 **운영하고 확장하는 법**에 무게를 둡니다. 데이터 모델·PromQL·서비스 디스커버리·Alertmanager 로 기초를 세운 뒤, 샤딩·페더레이션·HA 로 규모를 키우고, 원격 저장소(VictoriaMetrics·Mimir)와 Thanos·Jsonnet·SLO·OpenTelemetry 로 Prometheus 바깥까지 넓히는 **15개 장(3개 파트)** 구성입니다.

## 이 책을 여기 두는 이유

> 상위 README 가 예고해 둔 "관측 저장소 심화" 를 이 폴더가 실현합니다. 단일 Prometheus 의 한계를 원격 저장소로 미느냐 Thanos 로 합치느냐 — 그 두 갈래가 이 책을 여기 두는 이유입니다.

상위 [`06_observability/README.md`](../../README.md) 의 "예정 주제 — 관측 저장소 심화(TBD)" 절이 **Thanos** 를 예고해 두었습니다. "Prometheus 의 한계(단일 노드 보존·수평 확장 부재)를 메우는 장기보존·다중 클러스터 글로벌 쿼리 계층" 이라는 표현입니다. 이 폴더가 그 예고를 실현합니다. 같은 절의 다른 축인 OpenSearch 는 형제 폴더 [`dgos_opensearch/`](../dgos_opensearch/README.md) 가 이미 맡고 있습니다. 둘이 짝을 이룹니다.

핵심 대비는 **"단일 Prometheus 의 한계를 어느 방향으로 푸는가"** 입니다. 이 책은 그 답을 두 갈래로 나눠 보여줍니다. 9장의 원격 저장소(VictoriaMetrics·Mimir)는 메트릭을 *중앙의 큰 저장소로 remote write 해 밀어 넣는* 해법이고, 10장의 Thanos 는 *각 Prometheus 옆에 사이드카를 붙여 오브젝트 스토리지에 블록을 올리고 쿼리 시점에 합치는* 분산형 해법입니다. 이미 정리해 둔 [`02-05.Grafana Mimir`](../../02_LGTMStack/02-05.Grafana%20Mimir.md) 편이 전자에 해당하므로, 10장을 읽을 때 후자와 나란히 놓고 보면 저장·쿼리 비용의 트레이드오프가 선명해집니다.

책의 뒷부분은 기존 노트와 직접 이어집니다. 13장(SLO)은 [`01-04.SLO와 알림 — Error Budget, Burn Rate`](../../01_Foundations/01-04.SLO와%20알림%20—%20Error%20Budget,%20Burn%20Rate.md) 의 개념을 Sloth·Pyrra 라는 실제 도구로 내려보내고, 14장(OpenTelemetry)은 [`03-11.305P OpenTelemetry 도입 고려사항`](../../03_Project/03-11.305P%20OpenTelemetry%20도입%20고려사항.md) 에서 검토한 내용을 Collector 설정 수준에서 다시 짚습니다. 노트를 쓸 때 이 지점마다 교차참조를 남깁니다.



## 파트 구조

> 15개 장이 세 파트로 갈립니다. Part 1 의 제목만 디바이더 PDF 가 없어 확인되지 않았고, 장 범위는 확정입니다.

| 파트 | 제목 | 장 |
|------|------|----|
| Part 1 | (제목 미확인 — 본문은 "Prometheus 기초" 로 지칭) | 1–5 |
| Part 2 | Scaling Prometheus | 6–8 |
| Part 3 | Extending Prometheus | 9–15 |

> Part 2·3 의 제목과 장 범위는 참고 폴더의 `Part 2_*.pdf`·`Part 3_*.pdf` 디바이더 원문에서 확인했습니다. **Part 1 디바이더 PDF 는 참고 폴더에 없어** 처음에는 장 범위를 역산한 추정으로 두었으나, 5장 요약이 "This is also the conclusion of the first part of our journey, in which we focused on the fundamentals of Prometheus" 와 "Next, we'll dive into part two" 로 못 박아 **1–5장 범위는 확정**되었습니다. 파트 제목만 여전히 확인되지 않았습니다.



## 장별 목표

> 각 장 앞머리의 "we'll be covering these main topics" 목록을 그대로 옮긴 표입니다. 무엇을 읽게 되는지 먼저 보고 순서를 고르는 자리입니다.

각 장 앞머리의 "we'll be covering these main topics" 목록을 근거로 정리했습니다.

| 장 | 제목 | 주요 토픽 |
|----|------|----------|
| 1 | Observability, Monitoring, and Prometheus | 모니터링 약사(Nagios 계보) · 관측성 개념 입문 · 관측성 속 Prometheus 의 역할 |
| 2 | Deploying Prometheus | Prometheus 스택 구성요소 · Kubernetes 프로비저닝 · Prometheus Operator 배포 |
| 3 | The Prometheus Data Model and PromQL | 데이터 모델 · TSDB · PromQL 기초 |
| 4 | Using Service Discovery | 서비스 디스커버리 개요 · 클라우드 프로바이더 SD · HTTP SD 커스텀 엔드포인트 |
| 5 | Effective Alerting with Prometheus | Alertmanager 설정·라우팅 · 템플릿팅 · HA 알림 · 견고한 알림 설계 · 알림 룰 단위 테스트 |
| 6 | Advancing Prometheus: Sharding, Federation, and HA | Prometheus 의 한계 · 샤딩 · 페더레이션 · 고가용성 확보 |
| 7 | Optimizing and Debugging Prometheus | 카디널리티 제어 · recording rule · scrape jitter · pprof · 쿼리 로깅 · GC 튜닝 |
| 8 | Enabling Systems Monitoring with the Node Exporter | Node Exporter 개요 · 기본 collector · textfile collector · 트러블슈팅 |
| 9 | Utilizing Remote Storage Systems with Prometheus | remote write·remote read 이해 · VictoriaMetrics · Grafana Mimir |
| 10 | Extending Prometheus Globally with Thanos | Thanos 개요 · Sidecar · Compactor · Query · Query Frontend · Store · Ruler · Receiver · Thanos tools |
| 11 | Jsonnet and Monitoring Mixins | Jsonnet 개요 · Jsonnet 사용 · Monitoring Mixins |
| 12 | Utilizing CI Pipelines with Prometheus | GitHub Actions · CI 에서의 검증 · Pint 로 Prometheus 룰 린팅 |
| 13 | Defining and Alerting on SLOs | SLI·SLO·SLA 이해 · Prometheus 데이터로 SLO 정의 · Sloth 와 Pyrra |
| 14 | Integrating Prometheus with OpenTelemetry | OpenTelemetry 소개 · OTel Collector 로 Prometheus 메트릭 수집 · OTel Collector 로 Prometheus 에 전송 |
| 15 | Beyond Prometheus | Prometheus 너머로 관측성 확장 · 관측 시스템 간 점 잇기(메트릭·로그·트레이스) |



## 작성된 정독 노트

> PDF 를 장별로 읽는 대로 `NN-NN.제목.md` 형식으로 채웁니다.

| 노트 | 범위 |
|------|------|
| [00-01 용어집](./00-01.용어집.md) | 15개 장 20편의 핵심 용어 색인 + 정오표·버전 드리프트 색인. 각 용어의 홈 편 링크 |
| [00-02 결정 치트시트](./00-02.결정%20치트시트.md) | "X 냐 Y 냐" 결정 축 모음 — 저장 계층·SLO 타입·CI 계층·pull vs push·수신구 플래그 계열 |
| [01-01 관측 가능성·모니터링·Prometheus의 자리](./01-01.관측%20가능성·모니터링·Prometheus의%20자리.md) | 1장 전체 — 체크 기반(Nagios)의 알려진 미지 · SNMP 는 대체 아닌 흡수 · 제어 이론에서 온 관측 가능성 · 신호 6종(메트릭·로그·트레이스·이벤트·프로파일)의 상세도↔비용 · pull 모델과 조용한 실패 · `for` 기간과 Prometheus 가 아닌 것 |
| [02-01 Prometheus 배포 — 스택 구성요소와 Operator](./02-01.Prometheus%20배포%20—%20스택%20구성요소와%20Operator.md) | 2장 전체 — 스택 4요소 · 내부 4부품(TSDB 중심) · Alertmanager 분리 이유 · Node Exporter 와 textfile collector · Operator CRD 4종(+`PodMonitor`) · kube-prometheus 와 Helm 배포 · 원문 네임스페이스 오타 |
| [03-01 데이터 모델 — 메트릭·시계열·샘플](./03-01.데이터%20모델.md) | 3장 앞부분 — 메트릭·시계열·샘플 3층 · 무엇이 시계열 하나를 정하는가(라벨 셋) · `HELP`/`TYPE` 은 주석이 아니라 메타데이터 · 메트릭 타입 4종 · 분위수와 꼬리 지연 · 히스토그램 대 서머리(합산 가능 여부) |
| [03-02 TSDB 쓰기 경로](./03-02.TSDB%20쓰기%20경로.md) | 3장 쓰기 — 샘플이 WAL·head chunk 두 갈래로(WAL 이 먼저) · 같은 시스템콜 다른 준비 · WAL 자르기와 체크포인트 · 재시작 복구 3단계 · head 3이름과 chunk 일생(`head` 는 상태 이름) |
| [03-03 TSDB 저장 구조](./03-03.TSDB%20저장%20구조.md) | 3장 저장 — 블록 네 조각(chunk·인덱스·`meta.json`·툼스톤) · 불변성이 낳은 툼스톤 · 델타-오브-델타·XOR 압축 · 역색인(포스팅·시리즈) 5단계 · 컴팩션과 보존 · **mmap 세 단계** · 직접 열어 보기 · 언제 TSDB 를 고르나(설득용 5전제·쓰기 증폭·RDB 대비) |
| [03-04 PromQL 기초](./03-04.PromQL%20기초.md) | 3장 뒷부분 — 순간 vs 범위 벡터(대괄호가 경계) · `/query` vs `/query_range` · offset·서브쿼리 · staleness 와 lookback delta · `by`/`without` · `group_left` 와 `_info` 조인 · `and`/`or`/`unless` · `rate`·`irate`·`increase`·`changes`·`delta` |
| [04-01 서비스 디스커버리와 relabeling](./04-01.서비스%20디스커버리와%20relabeling.md) | 4장 전체 — `<type>_sd_configs` 규칙 · SD 는 후보 주소만 내주고 값은 exporter 가 냄 · 표준 relabeling(스크레이프 전) vs 메트릭 relabeling(후) · 자리에 따라 읽히는 라벨(`__meta_`·`__address__`·`__name__`) · 규칙 부품 넷과 후보 수를 바꾸는 `keep`·`drop` · Operator 의 두 경로와 사용자 규칙의 삽입 위치 · `/service-discovery` vs `/targets` 디버깅 · `http_sd` 세 요구와 빈 배열 계약 · `instance` 와 `__address__` 분리. 압축 전 정독 노트는 [`_archive/04-01`](./_archive/04-01.서비스%20디스커버리와%20relabeling.md) |
| [05-01 Alertmanager — 라우팅·그룹핑·억제·HA](./05-01.Alertmanager%20—%20라우팅·그룹핑·억제·HA.md) | 5장 앞부분 — Prometheus 는 알림을 보내지 않는다 · 라우트 트리와 `continue` · `group_wait`/`group_interval`/`repeat_interval` · 시간 구간(최상위 불가·해소 알림도 막힘) · 억제 규칙의 source/target · `amtool` 검증 · Go 템플릿과 `__subject` · 가십은 침묵만, 받은 알림은 아님 → 로드밸런서 금지 · 원문 라우팅 표 셋째 행 모순 |
| [05-02 견고한 알림과 룰 단위 테스트](./05-02.견고한%20알림과%20룰%20단위%20테스트.md) | 5장 뒷부분 — `unless` 로 재부팅 오탐 제거 · `_info` 패턴 · `for` 경험칙(warning ≥15m, critical ≤15m)과 평가 주기 제약 · 스크레이프 실패가 `for` 를 지운다 → `last_over_time` · `max_over_time` 의 추가 지연 · `promtool test rules` 로 14분 발화 단언 · 원문 확장 표기법이 시작 값 누락 |
| [06-01 샤딩·페더레이션·고가용성](./06-01.샤딩·페더레이션·고가용성.md) | 6장 전체 (2부 첫 장) — 두 한계(카디널리티·장기보존) · 라벨 값 100 상한과 단일 스레드 PromQL 엔진 · 샤딩은 데이터가 아니라 스크레이프 잡 · `hashmod` 두 단계와 8 대 16 불균등 · 페더레이션은 열에 아홉 답이 아니다 · `honor_labels` 와 `exported_` 개명 · HA 는 복제 + `alert_relabel_configs` 로 `prometheus_replica` `labeldrop` · 세 번째 relabeling 등장 · Thanos Sidecar/Query |
| [07-01 최적화와 디버깅](./07-01.최적화와%20디버깅.md) | 7장 전체 — `/tsdb-status` 네 표와 신뢰도(셋째·넷째는 카디널리티 진단용 아님) · `sort_desc(count by (__name__))` 로 범인 찾기 · `metric_relabel_configs` 의 `drop`·`labeldrop` 주의 · 네 리밋은 relabeling 후 평가, 위반 시 스크레이프 전체 실패 · `level:metric:operations` 규약 · rule manager 가 RAM 1/4 · 지터와 델타의 델타 · pprof·`promtool debug all` · `query_log_file` vs `queries.active` · `GOGC`/`GOMEMLIMIT` 과 OOM 킬러 |
| [08-01 Node Exporter — exporter 의 해부와 collector](./08-01.Node%20Exporter%20—%20exporter%20의%20해부와%20collector.md) | 8장 전체 (2부 마지막 장) — exporter 세 부품(정의·collector·레지스트리)과 최소 Go exporter · collector 마다 고루틴이라 개수가 스크레이프 속도를 좌우하지 않음 · `mode="idle"` 이 코어 수 `count` 의 필수 조건인 이유 · loadavg 대신 PSI(waiting/stalled, CPU 엔 stalled 없음) · textfile collector 의 glob 은 디렉토리에 맞고 `.prom` 은 코드에 박힘 · `node_textfile_mtime_seconds` 로 조용한 실패 차단 · 트러블슈팅은 `success` 가 아니라 `duration` | **책 정정 3건** — 기본 collector 는 49개가 아니라 **45개**(책 표는 43개, 누락은 `netstat`·`zfs`) · glob 은 `.prom` *파일* 이 아니라 *디렉토리* 에 맞음(`filepath.Glob` → `os.ReadDir` → `.prom` 필터) · `--collector.textfile.directory` 는 **v1.9.0 부터 반복 가능**(v1.6.1 은 `.String()`) · 커널 `psi.rst`: "CPU full is undefined at the system level" · `ErrNoData` 도 `success=0` 이라 하드웨어 부재와 오류가 구분 안 됨 |
| [09-01 remote write 와 remote read — 프로토콜·에이전트·튜닝](./09-01.remote%20write%20와%20remote%20read%20—%20프로토콜·에이전트·튜닝.md) | 9장 전반 (3부 첫 장) — 두 원격 저장소 API 는 protobuf + snappy over HTTP · remote read 는 쿼리 시점을 통제 못 해 실무에서 드묾, Thanos Sidecar 는 방향을 뒤집어 씀 · 한 Prometheus 가 두 API 의 클라이언트이자 서버 · 에이전트 모드는 쿼리·알림·로컬저장을 끔(WAL 2시간 한계) · `write_relabel_configs` 는 기본이 "전부 보냄" 이라 federation 과 반대 · 큐 1개 → 동적 샤드 N개, **샤드 하나만 차도 WAL 읽기 전체가 정지** | **책 정정 2건 + 보강 2건** — 큐 기본값이 `200/2500/500` → **`50/10000/2000`**(v2.44.0 에서 변경, 책의 값은 v2.26~v2.43 대) · 에이전트 모드는 **v3.0.0 에서 정식 승격**되며 플래그가 `--enable-feature=agent`→`--agent` · 공식 문서의 capacity 권장은 3배가 아니라 **3~10배** · 샤드 메모리 `샤드 수 × (capacity + max_samples_per_send)`, 뒤처짐은 `prometheus_remote_storage_samples_pending` (둘 다 책에 없음) |
| [09-02 VictoriaMetrics 와 Grafana Mimir](./09-02.VictoriaMetrics%20와%20Grafana%20Mimir.md) | 9장 후반 — VM 은 자원 효율(샘플당 0.3B vs 2.1B) 이 무기이나 오픈소스 모델·PromQL 호환이 걸림돌 · MetricsQL 은 `rate`/`increase` 에서 구간 **직전 샘플까지** 포함해 PromQL 과 값이 갈림 · 단일 노드로 초당 150만 샘플까지 감당 · **VM=블록 스토리지 / Mimir=오브젝트 스토리지** 가 비용을 가름 · HA 중복 제거가 정반대 — VM 은 external label 이 *같아야* 하고(`replicaExternalLabelNameClear`), Mimir 는 리더 선출 후 나머지를 버림(30초 페일오버, Consul/etcd 필요) · Mimir 는 `X-Scope-OrgID` 테넌트 헤더 필수 | **출처 성격 구분** — 디스크 7배·메모리 5배(vs Prometheus)와 저장 3배·CPU 1.7배(vs Mimir) 는 모두 **VictoriaMetrics 자사 벤치마크**(2020-11) · PromQL 준수 **72.78%** 는 Prometheus v2.30.0 + VM v1.67.0 **고정 버전**의 값이라 현재치로 인용 금지 · 룰·알림은 별도 컴포넌트 `vmalert` 가 맡음(책에 없는 내용으로 명시) |
| [10-01 Thanos 저장 경로 — Sidecar·Compactor·Store](./10-01.Thanos%20저장%20경로%20—%20Sidecar·Compactor·Store.md) | 10장 전반 — Thanos 의 세 목표(전역 쿼리 뷰·무제한 보존·고가용성), 전 컴포넌트가 `thanos` 바이너리의 서브커맨드 · StoreAPI 는 gRPC RPC 4개(`Info`·`Series`·`LabelNames`·`LabelValues`) · Sidecar 는 Prometheus 가 쓴 TSDB 블록을 그대로 올리므로 **로컬 압축을 반드시 꺼야** 함(`compaction.level > 1` 이면 무시) · 수평 압축 vs 수직 압축(위험·파괴적) · **다운샘플링은 용량을 줄이지 않고 늘림**(raw+5m+1h 블록이 공존, 인덱스는 그대로) · Store 는 `meta.json` 의 `thanos` 절로 꺼낼 블록을 고르고 시간·external label 로 수동 파티셔닝 | **책 정정 1건 + 보강 3건** — 40시간·10일은 데이터의 *나이* 가 아니라 **블록의 시간 폭(`MaxTime-MinTime`)**, "청크 2개는 나오도록" 보장하려는 것이라 수평 압축이 선행돼야 함 · `--retention.resolution-raw` 를 40h 보다(5m 을 10d 보다) 짧게 주면 Compactor 가 **기동 실패**(단 `0`=무제한은 검사 제외) · `--wait-interval` 은 `--wait` 를 함께 줘야 작동 · `--shipper.upload-compacted` 는 업로드를 *활성화* 하는 플래그(책 표현은 반대로 읽힘) |
| [10-02 Thanos 쿼리 경로 — Query·Query Frontend·Ruler·Receiver](./10-02.Thanos%20쿼리%20경로%20—%20Query·Query%20Frontend·Ruler·Receiver.md) | 10장 후반 — Query 는 StoreAPI 엔드포인트로 부채꼴 질의(`dns+`·`dnssrv+`), Query 자신도 StoreAPI 를 구현해 Query 를 Query 에 붙일 수 있음 · 기본 PromQL 엔진은 단일 스레드이고 **모든 시계열을 끌어온 뒤** 집계 — `avg` 는 내려보낼 수 없기 때문(평균의 평균 ≠ 평균) · `--query.promql-engine=thanos` 는 멀티 스레드 + 분산 실행(실험적, 실패 시 기본 엔진으로 폴백) · Query Frontend 는 시간 분할(기본 `24h`)·수직 샤딩(집계 연산자 필수)·결과 캐싱(**range 쿼리만**) · Ruler 는 Query 에 의존하므로 **대체가 아니라 보완**, stateless 모드는 StoreAPI 를 잃고 WAL-only 로 · Receiver 는 Ketama 해시링, **중복 제거 기능 없음**(수직 압축으로 우회) | **책 정정 1건 + 보강 3건** — 쿼럼이 책의 `(RF+1)/2` 가 아니라 소스는 **`floor(RF/2)+1`**(`uint64` 버림 나눗셈). 홀수 RF 는 일치, **짝수 RF 는 전부 불일치**(RF=4 → 소스 3, 책 2). 책의 예시(RF=3→2)는 옳음 · `seriesReplicated` 면 쿼럼이 1 로 내려가 복제 증폭을 막음 · `--query-range.min/max-split-interval` 은 `--query-range.split-interval` 과 병용 불가 · Receive `--tsdb.retention=0d` 는 무한 보존, 해시링 설정의 테넌트별 알고리즘이 플래그를 덮어씀 |
| [11-01 Jsonnet — YAML 을 손으로 쓰지 않기 위한 언어](./11-01.Jsonnet%20—%20YAML%20을%20손으로%20쓰지%20않기%20위한%20언어.md) | 11장 앞부분 — 모든 JSON 은 유효한 Jsonnet · 키는 알파벳순 정렬 · 숨은 필드 `::` 와 병합 `+:` 가 언어의 핵심 · `self`/`super`/`$` · 컴프리헨션·함수·에러 · 검증은 `promtool` 에 맡길 것. 책의 `assert.jsonnet` 은 쉼표 누락으로 실행 불가(정오표) |
| [11-02 모니터링 믹스인 — 규칙과 대시보드를 패키지로](./11-02.모니터링%20믹스인%20—%20규칙과%20대시보드를%20패키지로.md) | 11장 뒷부분 — 필드는 넷, 산출물은 셋(`_config` 는 손잡이) · `jb` 가 의존성까지 vendor/ 로 · 컴포넌트를 `null` 로 지우면 규칙·대시보드가 사라짐 · `kube-prometheus` 는 이미 k8s 믹스인 사용 중. 책의 렌더링 명령은 `-c` 누락으로 실패(정오표) |
| [12-01 CI 파이프라인으로 Prometheus 검증 — promtool·amtool·Pint](./12-01.CI%20파이프라인으로%20Prometheus%20검증%20—%20promtool·amtool·Pint.md) | 12장 전체 — GitHub Actions 용어(workflow·job·step·runner) · `act` 로 로컬 실행 · `promtool check config/rules`·`test rules` · `amtool check-config`·`config routes test` · Pint 는 살아있는 Prometheus 에 붙어 시계열 존재까지 검사(promtool 은 못 함). 책의 summary 정규식은 `!`·`?` 를 못 막음(실측 정오표) |
| [13-01 SLO 를 Prometheus 로 정의하고 알림하기 — 요청·윈도우 기반과 Sloth·Pyrra](./13-01.SLO%20를%20Prometheus%20로%20정의하고%20알림하기%20—%20요청·윈도우%20기반과%20Sloth·Pyrra.md) | 13장 전체 — SLI·SLO·SLA 층위 · 요청 기반 vs 윈도우 기반(이상 트래픽 회복: 16일 vs 3.75시간) · `clamp_min` 안전장치와 엣지 케이스 · `>= bool` + `[30d:5m]` 윈도우 구성 · Sloth 17규칙/3그룹(실측)·Pyrra 28일 창. burn rate 이론은 01-04 참조. 책의 알림은 성공비율 `>` 로 부호 뒤집힘(정오표) |
| [14-01 Prometheus 와 OpenTelemetry 통합 — 규격·Collector·OTLP 수신구](./14-01.Prometheus%20와%20OpenTelemetry%20통합%20—%20규격·Collector·OTLP%20수신구.md) | 14장 전체 — OTel 은 실행 기술이 아니라 규격(API·SDK·시맨틱 컨벤션+OTLP) · OpenCensus+OpenTracing→2019 CNCF · Collector = receiver·processor·exporter 파이프라인 · prometheus receiver 로 긁고 otlphttp 로 밀기 · push 경로의 `up` 은 전송 성공 아님. 책의 `otlp-write-receiver`(2.47.0 실험)는 3.0 에서 `--web.enable-otlp-receiver` 로 승격(버전 드리프트) |
| [15-01 Prometheus 너머 — 세 신호를 잇는 관측 가능성과 exemplar](./15-01.Prometheus%20너머%20—%20세%20신호를%20잇는%20관측%20가능성과%20exemplar.md) | 15장 전체(마지막 장) — Prometheus 는 관측의 3분의 1 · unknown unknown · 로그(신호대잡음 최악·최후의 보루)·트레이스(최상·샘플링) · 로그에서 메트릭 추출 금지 · "잇되 의존시키지 않는다" · 라벨 일관성·exemplar(메트릭→트레이스 다리) · Loki/Tempo/LGTM. exemplar 는 아직 실험(승격 안 됨). Loki·Tempo 내부는 02-03·02-04 참조 |



## 학습 프레젠테이션

> 3·4·5·8장의 데이터 모델, 수집·저장, 알림, Node Exporter 흐름을 기초 용어에서 운영 판단까지 한 흐름으로 연결한 발표·복습 자료입니다. 역색인·mmap·staleness·벡터 매칭, promtool 룰 단위 테스트와 Alertmanager HA 까지 다룹니다. `~/notification-lab/observability/experiments/`와 내부 Kind 실습 결과를 핵심 장표에 대조했으며, 모든 HTML은 외부 네트워크 없이 열립니다.

- [2주차 발표자료 PDF (40장)](./_study/2%EC%A3%BC%EC%B0%A8%20%EB%B0%9C%ED%91%9C%EC%9E%90%EB%A3%8C.pdf)
- [02-01 스크레이프와 저장 흐름 (인터랙티브)](./_study/02-01.%EC%8A%A4%ED%81%AC%EB%A0%88%EC%9D%B4%ED%94%84%EC%99%80%20%EC%A0%80%EC%9E%A5%20%ED%9D%90%EB%A6%84.html)
- [02-02 알림 흐름 (인터랙티브)](./_study/02-02.%EC%95%8C%EB%A6%BC%20%ED%9D%90%EB%A6%84.html)
- [2주차 발표 흐름 (발표자 노트)](./_study/2%EC%A3%BC%EC%B0%A8%20%EB%B0%9C%ED%91%9C%20%ED%9D%90%EB%A6%84.md) — 각 장이 무엇을 전달하는지, 시연 지점, 시간이 부족할 때 줄일 순서



## 출처·톤 메모

> 원본 판본과 예제 저장소, 그리고 이 폴더가 따르는 어체와 편 구조를 적어 둡니다. 확정하지 못한 것은 확정하지 못했다고 남깁니다.

- 원본: Packt — *Mastering Prometheus* (ISBN 9781805125662). O'Reilly 학습 플랫폼 경로는 각 장 PDF 하단 URL 에서 확인했습니다(`learning.oreilly.com/library/view/mastering-prometheus/9781805125662`). 예제 코드 저장소는 본문이 반복해 안내하는 `github.com/PacktPublishing/Mastering-Prometheus` 입니다.
- 장별 목표·토픽은 각 챕터 PDF 앞머리의 "covering these main topics" 목록에서 추출했습니다. 저자명은 PDF 본문에서 확정하지 못해 적지 않았습니다.
- 정독 노트는 **합니다체**로 쓰고, 형제 단행본 폴더(`dgos_opensearch/`, `07_devops/04_cicd/book/*`)와 동일하게 07-04 책 요약 템플릿 구조(핵심 요약 → 학습 목표 → 본문 정리 → 심화 학습 → 실무 적용 → 체크리스트 → 면접 관점 → 참고 자료)를 따릅니다. 각 편에 Mermaid 1장 이상을 두고, 책 밖 조사분은 본문 정리와 섹션을 분리해 출처 링크를 남깁니다.
