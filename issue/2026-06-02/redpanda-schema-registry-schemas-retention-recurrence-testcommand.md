# Redpanda Schema Registry `_schemas` retention 손상 재발 — TestCommandAvro 등록 실패 (error 40002)

- **발생일**: 2026-06-02
- **영향 범위**: 로컬 sbh-local 환경(개인 macOS). `message-lib/docker/docker-compose.yml` 로 기동된 Redpanda 단일 컨테이너. 이번에는 operator 가 `tps.v305p.operator.cmd.test` 토픽으로 `TestCommandAvro` 를 발행하는 시점(테스트 파이프라인 실행)에서 Avro 스키마 등록이 실패한다. 선행 사고(05-26)는 executor 의 `BuildResultEventAvro`(result 토픽)에서 났는데, 발현 레코드만 다를 뿐 근본 원인은 동일하다 — SR 백엔드가 깨지면 *어느 레코드든* 등록이 막힌다. dev/prd 는 별도 인프라라 분리.
- **심각도**: 로컬 한정. operator 의 test command 발행이 차단되어 테스트 Job 이 executor 로 전달되지 못한다. Redpanda Console 의 메시지 역직렬화도 `schema id` 조회 타임아웃으로 실패한다.
- **상태**: 원인 확정(선행 이슈의 예고된 재발). 복구 미적용 — 아래 §3 으로 진행 예정.
- **관련 티켓**: 미연결.
- **fix 회차**: 0 (진단까지. 복구·예방은 §3).
- **선행 이슈**: [`2026-05-26/redpanda-schema-registry-schemas-topic-retention-corruption.md`](../2026-05-26/redpanda-schema-registry-schemas-topic-retention-corruption.md) — 동일 근본 원인(`_schemas` 7일 retention 만료)을 진단하고 1차 복구(`down -v`)만 했으며, **"재발 방지 미적용 — 7일 뒤 같은 사고가 반복된다"** 를 명시했다. 그 7일이 지나(05-26 → 06-02) 정확히 재발했다.

---

## 1. 증상

operator 가 테스트 파이프라인 실행 요청을 처리하며 `TestCommandAvro` 를 발행하는 순간 직렬화가 실패한다.

```
org.okestro.tps.messaging.serialization.AvroSerializationException:
  Failed to serialize Avro record: TestCommandAvro
    at AvroSerializer.serialize(AvroSerializer.java:27)
    at EventPublisher.serialize(EventPublisher.java:45)
    at EventPublisher.publish(EventPublisher.java:27)
    at TestJobExecutionTransactionHandler.publishQueueAndMarkQueued(TestJobExecutionTransactionHandler.java:53)
    ... (트랜잭션 커밋 후 AFTER_COMMIT 리스너 경로)
    at TestJobExecutionRequestedEventListener.onTestJobExecutionRequested(...:58)
    ... (PipelineController.execute → PipelineExcnService.executePipeline)
Caused by: SerializationException: Error registering Avro schema {TestCommandAvro ...}
Caused by: RestClientException: Fetch returned with error; error code: 40002
```

발현 경로는 명확하다. `PipelineController.execute` → 트랜잭션 안에서 `executePipeline` → 커밋 직후 `AFTER_COMMIT` 단계로 `onTestJobExecutionRequested` 리스너가 돌고, 그 안에서 `publishQueueAndMarkQueued` 가 `eventType=QUEUE` 인 `TestCommandAvro` 를 발행한다. 스택 가장 안쪽 `error code 40002` 가 선행 사고와 글자 그대로 같다.

Redpanda Console 의 같은 토픽 메시지 역직렬화 진단도 동일한 신호를 준다.

```
Avro: getting avro schema from registry: failed to fetch schema from schema registry:
  unable to GET "http://redpanda:8081/schemas/ids/1":
  context deadline exceeded (Client.Timeout exceeded while awaiting headers)
```

operator(등록)·Console(조회) 양쪽 모두 SR 에 도달은 하지만 요청이 완결되지 않는다. SR 백엔드가 자기 데이터를 못 읽는 선행 사고의 상태와 일치한다.

---

## 2. 근본 원인

**선행 이슈와 동일하다 — `_schemas` 토픽이 SR 전용 정책(`cleanup.policy=compact`, `retention.ms=-1`)이 아닌 클러스터 기본 정책(`delete`, 7일 retention)으로 만들어져 있어, retention 만료로 스키마 등록 메시지가 전부 삭제되고 SR 가 자기 백엔드를 못 읽게 됐다.** 그 상태에서 신규 등록(`auto.register.schemas=true` 경로)을 받으면 SR 가 일관성을 보장할 수 없어 `error code 40002` 로 거부한다.

근본 원인의 상세 진단(토픽 offset `18==18` 로 메시지 0건 확인, `cleanup.policy=delete DEFAULT_CONFIG`, Redpanda 로그의 `offset_out_of_range`, "시간 자체가 트리거")은 선행 문서 §2 에 이미 완결돼 있으므로 여기서 재서술하지 않는다. 본 문서는 그 진단이 **다시 들어맞았다**는 사실과 재발 메커니즘에 집중한다.

### 왜 또 터졌는가 — 재발 메커니즘

선행 복구는 `down -v` 로 볼륨을 초기화했고, 그 직후 `_schemas` 가 *같은 잘못된 기본 정책으로* 재생성됐다(선행 §3.2 가 명시). 영구 예방책(방안 A/B/C)은 셋 다 적용되지 않았다. 확인 결과:

```
message-lib/docker/docker-compose.yml
  → compact / retention=-1 / auto_create_topics_enabled=false / init script 흔적 전무
```

즉 05-26 복구 시점에 7일짜리 retention 시계가 다시 0부터 돌기 시작했고, 06-02 에 만료를 통과하며 동일 사고가 재현됐다. **코드/설정 변경이 없었으므로 재발은 우연이 아니라 예정된 결과다.**

### 발현 레코드가 다른 점에 대하여

선행은 `BuildResultEventAvro`(executor → result 토픽), 이번은 `TestCommandAvro`(operator → command 토픽)다. 레코드·발행 주체·토픽이 다른데도 같은 40002 가 나는 것은, 손상이 *특정 스키마*가 아니라 *SR 백엔드 전체*에 있다는 §2 진단을 오히려 강화한다. 그날 어떤 발행 경로가 먼저 트리거되느냐에 따라 표면에 보이는 레코드 이름만 달라진다.

> 반증해 둔 오답(박제): 처음 탐색에서 "AVDL 의 `enum TestHandlerAvro {...} = JENKINS;` 가 invalid JSON 을 만들어 40002" 라는 가설이 나왔다. 그러나 스택트레이스에 박힌 실제 등록 JSON 의 enum default 가 `{"type":"enum","symbols":["JENKINS","SONARQUBE","JUNIT"],"default":"JENKINS"}` 로 **정상 변환**돼 있고, 동일 AVDL·동일 인프라를 쓰는 BuildCommandAvro 가 멀쩡한 점에서 반증된다. 스키마는 무죄다. 40002 는 스키마 내용 거부(42201/409)가 아니라 SR 백엔드 상태 에러다.

---

## 3. 수정안

### 3.1 1차 복구 (선행과 동일, 즉시 가능)

`down -v` 로 Redpanda 볼륨을 초기화하고 재기동하면 SR 가 회복하고 operator 가 첫 발행 시 `TestCommandAvro` 스키마를 자동 재등록한다(`auto.register.schemas=true`). 단, 이 방법은 7일 뒤 또 재발한다 — 선행이 증명했다. **이번에는 1차 복구로 끝내지 말고 반드시 §3.2 를 함께 적용한다.**

### 3.2 영구 예방 (이번 사이클에서 적용 — 재발 종결 목표)

선행 §3.2 의 방안 A/B/C 중, **사람 손이 안 들고 컨테이너 재생성마다 자동 적용되는 방안 C(또는 B)** 가 재발 종결에 맞다. 방안 A 의 alter-config 4줄은 일회성이라 다음 `down -v` 에서 다시 풀린다 — 이번 재발이 그 한계의 실증이다.

- **방안 C (권장)**: `message-lib/docker/docker-compose.yml` 에 init 컨테이너/`depends_on` + 헬스 게이트로, Redpanda 기동 직후 `_schemas` 정책을 `compact` / `retention.ms=-1` 로 박는 스크립트를 자동 실행. 보호(`kafka_nodelete_topics`) 임시 해제 → alter-config → 보호 복구 시퀀스를 스크립트화.
- **방안 B (병행 검토)**: 부트 args 에 `redpanda.auto_create_topics_enabled=false` 추가로 `_schemas` 가 일반 토픽 정책으로 선점 생성되는 경로를 차단. SR 가 자기 정책으로 토픽을 만들도록 보장(이미지 버전별 옵션명 조사 필요 — 추측 금지).

> 어느 방안이든 `docker-compose.yml` 변경이므로 적용 후 `down -v` → `up` 한 사이클을 돌려 `_schemas` 정책이 `compact/-1` 로 박히는지 직접 확인해야 검증이 닫힌다.

---

## 4. 검증 방법

선행 §4 와 동일 절차에 이번 레코드를 반영한다.

```bash
# 4.1 SR 응답 정상화 — 200 + subject 목록
curl -s -i http://localhost:8084/subjects        # 환경 프로필별 SR URL 확인 후
#   → operator command 발행이 한 번이라도 성공하면
#     org.okestro.tps.avro.operator.TestCommandAvro 가 목록에 등장

# 4.2 _schemas 정책이 영구 정책으로 박혔는지 (예방 검증의 핵심)
docker exec <redpanda> rpk topic describe _schemas -c | grep -iE "cleanup|retention"
#   기대: cleanup.policy=compact, retention.ms=-1  (DEFAULT_CONFIG 가 아니어야 함)

# 4.3 Redpanda 로그에 _schemas offset 경고 없음
docker logs <redpanda> 2>&1 | grep "schema_registry.*_schemas"   # 빈 결과면 OK

# 4.4 operator 재발행 성공 — command 토픽에 메시지
docker exec <redpanda> rpk topic consume tps.v305p.operator.cmd.test --num 1 --offset end -f json
```

완료 판정: 4.1 의 `/subjects` 200 + `TestCommandAvro` subject 등록 + **4.2 가 `compact/-1` 로 확인**되면 이번 사이클은 닫힌다. 4.2 가 여전히 `delete/604800000` 이면 7일 뒤 또 재발하므로 미완료로 본다.

---

## 5. 메모 — 진단 과정에서의 실수 박제

1. **선행 이슈를 못 찾고 "신규·추정"으로 1차 분석을 닫을 뻔했다.** 같은 `issue/` 디렉토리에 동일 근본 원인(`_schemas` retention)이 1주 전 완결 진단돼 있었는데, 처음엔 그걸 모른 채 SR 상태를 "추정"이라고만 적었다. 1차 자료가 바로 옆에 있었다. → 이슈 기록 시 **같은 증상 키워드(40002, _schemas, AvroSerializationException)로 기존 issue/ 를 먼저 grep** 하는 것을 선행 단계로 박는다.
2. **적재 위치를 처음에 틀렸다.** `operator/.sbh/` (코드리뷰용 gitignored 워크스페이스)에 적었는데, 이슈 기록 정본은 `runners-high/issue/<날짜>/` 였다. → 이슈 = `issue/`, 코드리뷰/분석 = `.sbh/` 로 구분.
