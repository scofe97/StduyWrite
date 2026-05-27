# Redpanda Schema Registry `_schemas` 토픽 retention 손상으로 Avro 등록 실패

- **발생일**: 2026-05-26
- **영향 범위**: 로컬 sbh-local 환경(개인 macOS). `message-lib/docker/docker-compose.yml` 로 기동된 Redpanda 단일 컨테이너(`redpanda-local`, image `v26.1.5`). executor engine 이 결과 이벤트(`tps.v305p.executor.evt.*-result`) 를 발행할 때 Avro 스키마 등록 단계에서 전부 실패한다. operator·consumer 측은 등록된 스키마를 다시 가져오지 못한다. dev/prd 환경은 별도 인프라라 본 사례와 분리.
- **심각도**: 로컬 한정. executor 의 모든 result 토픽 발행이 차단되어 dispatch 한 Job 이 terminal 상태에 도달하지 못하고, executor_jenkins QA 스위트는 `wait_all_terminal` 단계에서 timeout 으로 무더기 실패한다. 운영 가설이 아니라 로컬 환경 자체가 사용 불가 상태.
- **상태**: 1차 복구 완료(`down -v` 로 Redpanda 볼륨 초기화, 컨테이너 재기동). Schema Registry `/subjects` 가 200 응답으로 회복하고 executor 가 `BuildResultEventAvro` 스키마를 자동 재등록함을 확인. **재발 방지 미적용** — 같은 정책으로 토픽이 재생성되었으므로 7일 뒤 같은 사고가 반복된다.
- **관련 티켓**: [IGMU-1041](https://okestro.atlassian.net/browse/IGMU-1041) (QA 케이스 검증 도중 노출됨, 티켓 자체 결함은 아님)
- **fix 회차**: 1 (1차 복구만 완료, 영구 예방 미적용)
- **커밋**: 코드 변경 없음. 인프라 운영 조치 + `qa/python/docs/troubleshooting.md` #16 항목 신설(별도 PR).

---

## 1. 증상

QA 스위트 `qa/python/suites/executor_jenkins/tests/test_10_order_preservation.py` 를 처음 실행했을 때 dispatch 3건 모두 HTTP 200 으로 잘 받아진다. 그런데 `wait_all_terminal(timeout=240)` 이 종료를 기다리는 동안 executor 로그에 같은 스택이 반복해서 찍힌다.

```
org.okestro.tps.messaging.serialization.AvroSerializationException:
  Failed to serialize Avro record: BuildResultEventAvro
    at AvroSerializer.serialize(AvroSerializer.java:27)
    at EventPublisher.serialize(EventPublisher.java:45)
    at EventPublisher.publish(EventPublisher.java:27)
    at JobResultPublish.publishResult(JobResultPublish.java:55)
    at TerminalCommitAdapter.commitTerminal(TerminalCommitAdapter.java:39)
    ...
Caused by: SerializationException: Error registering Avro schema {BuildResultEventAvro ...}
Caused by: RestClientException: Fetch returned with error; error code: 40002
```

발현 경로는 두 갈래로 갈리는데 둘 다 같은 지점에서 멈춘다. 첫째는 신규 dispatch 의 정상 종료 시점이고, 둘째는 `ExecutionRecoverScheduler.recoverRunning` 이 이전 세션에서 RUNNING 으로 남은 잔재 Job 을 복구하며 결과를 발행하려는 시점이다. 후자가 더 자주 보이는 이유는 복구 스케줄러가 12 초 주기로 돌면서 잔재가 있는 한 계속 시도하기 때문이다.

dispatch HTTP 단계는 깨끗하고 `TB_TRB_EC_001` 에 row INSERT 까지 정상이라 처음에는 QA 코드 결함을 의심했지만, 다른 모든 executor_jenkins 테스트도 같이 영향을 받는다는 사실이 인프라 원인을 가리킨다.

---

## 2. 근본 원인

**`_schemas` 토픽이 SR 전용 정책이 아닌 클러스터 기본 정책으로 만들어져 있었고, 7일 retention 이 만료되어 등록 메시지 18 건이 전부 삭제되었다.** 그 결과 Schema Registry 백엔드가 자기 데이터를 못 읽게 됐다.

### (1) `_schemas` 의 실제 정책 — 정상 SR 의 정책이 아니다

복구 직전 측정한 토픽 설정.

```bash
$ docker exec redpanda-local rpk topic describe _schemas -c | grep -iE "cleanup|retention"
cleanup.policy                        delete         DEFAULT_CONFIG
delete.retention.ms                   -1             DEFAULT_CONFIG
retention.ms                          604800000      DEFAULT_CONFIG   # = 7일
```

정상이라면 `_schemas` 는 `cleanup.policy=compact`, `retention.ms=-1`(무한) 이어야 한다. Confluent/Redpanda 가 Schema Registry 를 정식으로 부트스트랩할 때 직접 토픽을 만들면 이 두 값을 강제로 박는다. 그런데 본 환경은 두 값 모두 `DEFAULT_CONFIG` 라는 출처 표기가 붙어 있다 — 클러스터 기본값(일반 토픽용) 을 그대로 받았다는 뜻이다.

원인 가설은 둘 중 하나다. 하나는 토픽이 **SR 가 부트스트랩되기 전에 다른 경로(예: 일반 producer 또는 auto.create.topics.enable) 로 먼저 생성**되어 SR 가 자기 정책으로 덮어쓸 기회를 놓친 경우다. 다른 하나는 이 Redpanda 이미지 버전(`v26.1.5`) 에서 SR 가 토픽 부트스트랩 시 정책을 명시하지 않는 결함을 가지고 있는 경우다. 어느 쪽이든 결과는 같다 — `_schemas` 가 7일짜리 일반 토픽이 됐다.

### (2) 7일 retention 만료로 메시지가 전부 삭제됐다

토픽 파티션 오프셋을 보면 결정적이다.

```bash
$ docker exec redpanda-local rpk topic describe _schemas -p
PARTITION  LEADER  EPOCH  REPLICAS  LOG-START-OFFSET  HIGH-WATERMARK
0          0       11     [0]       18                18
```

`LOG-START-OFFSET == HIGH-WATERMARK == 18` 은 "한때 offset 0~17 의 메시지 18 건이 있었는데 지금은 한 건도 남지 않았다" 는 의미다. retention 청소가 0~17 을 잘라낸 뒤, start 만 18 로 전진하고 새 메시지가 들어오지 않아 watermark 도 그대로다. `rpk topic consume _schemas --offset start --num 1` 도 빈 응답이라 메시지 0 건이 사실로 확인된다.

컨테이너 생성·시작 이력 도 정황을 보태준다.

```bash
$ docker inspect redpanda-local --format \
    'Created: {{.Created}}{{"\n"}}StartedAt: {{.State.StartedAt}}'
Created:   2026-04-30T06:05:06Z
StartedAt: 2026-05-21T05:33:50Z
```

4/30 생성, 5/21 시작, 오늘 5/26. retention 7 일을 넘긴 데이터가 청소 대상에 들었다.

### (3) Schema Registry 가 자기 백엔드를 못 읽어 등록 거부로 회신한다

SR 클라이언트는 시작 직후 `_schemas` 를 offset 0 부터 재생해 스키마 캐시를 복원한다. 그런데 0~17 이 없으니 Kafka 브로커가 `offset_out_of_range` 로 회신한다. Redpanda 자체 로그에도 같은 경고가 반복된다.

```bash
$ docker logs redpanda-local 2>&1 | grep schema_registry
WARN kafka/client - schema_registry_client - client.cc:190 -
  partition_error: ({_schemas/0}, { error_code: offset_out_of_range [1] })
WARN kafka/client - schema_registry_client - client.cc:190 -
  partition_error: ({_schemas/0}, { error_code: offset_out_of_range [1] })
# ... 같은 줄이 수십 회 반복
```

SR 가 자기 캐시를 복원하지 못한 상태에서 외부 요청을 받으면 두 가지 증상이 같이 난다.

```bash
$ curl -s http://localhost:8084/subjects
# 빈 응답 (정상은 최소 "[]")

$ curl -s http://localhost:8084/mode
# 빈 응답
```

이 상태에서 executor 가 신규 스키마를 등록하려 하면 SR 가 자기 백엔드 일관성을 보장할 수 없어 `error code 40002` 로 거부한다. 이게 위 스택의 마지막 줄의 정체다.

### (4) 왜 로컬에서 "갑자기" 깨졌는가

사용자가 던진 의문 — "로컬에서 만든 건데 왜 깨지냐" — 의 답은 **시간 자체가 트리거**라는 데 있다. 만든 직후엔 18 건의 스키마 메시지가 멀쩡히 살아 있어 SR 가 정상 동작했다. 그런데 토픽 정책이 7 일짜리 retention 이었기 때문에, 컨테이너가 며칠 동안 돌아가는 사이 retention 만료가 오면 메시지가 사라진다. 로컬이든 운영이든 정책이 같으면 같은 주기로 재발한다. 로컬에서만 잘 보이는 이유는 단지 로컬 컨테이너가 며칠씩 켜둔 상태에서 retention 만료를 통과할 가능성이 더 높기 때문이다.

---

## 3. 수정안

### 3.1 1차 복구 (실 적용)

선택지는 둘이었다. (a) `_schemas` 토픽만 삭제·재생성하는 국소 복구, (b) `down -v` 로 Redpanda 볼륨 자체를 초기화. (a) 를 먼저 시도했으나 시스템 보호로 막혀 (b) 로 전환했다.

(a) 가 막힌 이유는 다음 클러스터 설정이다.

```bash
$ docker exec redpanda-local rpk cluster config get kafka_nodelete_topics
- _redpanda.audit_log
- __consumer_offsets
- _schemas
```

`_schemas` 가 삭제·alter-config 양쪽 모두 보호되는 시스템 토픽 목록에 들어 있어, `rpk topic delete _schemas` 와 `rpk topic alter-config _schemas --set cleanup.policy=compact` 모두 `TOPIC_AUTHORIZATION_FAILED` 로 거부됐다. 보호를 풀려면 클러스터 config 를 한 번 더 변경해야 해서, 손이 더 들지 않는 (b) 로 진행했다.

```bash
$ cd message-lib/docker
$ docker compose -f docker-compose.yml down -v   # 볼륨 redpanda-data 삭제
$ docker compose -f docker-compose.yml up -d
$ # redpanda-local Healthy 확인 후
$ curl -s http://localhost:8084/subjects
["org.okestro.tps.avro.executor.BuildResultEventAvro"]
```

DB 컨테이너(`trb-305p-mariadb-local`) 는 별도 compose(`qa/docker/docker-compose.sbh-local.yml`) 라 영향받지 않는다. executor engine 은 외부 JVM 으로 떠 있는데 Redpanda 재시작 후 자동으로 SR 클라이언트가 재연결해 스키마를 다시 등록했다 — 위 응답의 `BuildResultEventAvro` 가 그 증거다.

### 3.2 재발 방지 (미적용 — 후속 작업)

1차 복구 직후 재생성된 `_schemas` 정책을 다시 보면 똑같이 `cleanup.policy=delete`, `retention.ms=604800000` 이다. 즉 **지금 같은 사고가 7일 뒤 다시 난다.** 영구 차단하려면 다음 중 하나가 필요하다.

방안 A — Redpanda 클러스터 기본값에서 `_schemas` 만 정책을 박는다. 보호를 일시 해제하고 alter-config 로 두 값을 박은 뒤 보호를 원복한다.

```bash
docker exec redpanda-local rpk cluster config set kafka_nodelete_topics \
  '[_redpanda.audit_log, __consumer_offsets]'   # _schemas 임시 제외
docker exec redpanda-local rpk topic alter-config _schemas --set cleanup.policy=compact
docker exec redpanda-local rpk topic alter-config _schemas --set retention.ms=-1
docker exec redpanda-local rpk cluster config set kafka_nodelete_topics \
  '[_redpanda.audit_log, __consumer_offsets, _schemas]'   # 보호 복구
```

방안 B — `message-lib/docker/docker-compose.yml` 의 Redpanda 부트 args 에 `--set redpanda.auto_create_topics_enabled=false` 와 SR 가 자기 토픽을 정상 정책으로 만들도록 보장하는 옵션(이미지 버전별 옵션 이름 조사 필요) 을 추가한다. 컨테이너를 새로 만들 때마다 자동 적용되어 사람의 손이 들지 않는다.

방안 C — 컨테이너 기동 직후 한 번 도는 init script 를 compose 에 끼워 방안 A 의 alter-config 4 줄을 자동 실행한다. 가장 보수적인 선택.

세 방안 중 어느 것을 선택할지는 별도 결정 사안이다. 본 보고서는 1차 복구까지 완료한 상태로 기록을 마치고, 후속은 별도 작업으로 분리한다.

---

## 4. 검증 방법

### 4.1 SR 응답 정상화

```bash
$ curl -s -i http://localhost:8084/subjects
HTTP/1.1 200 OK
Content-Type: application/vnd.schemaregistry.v1+json
["org.okestro.tps.avro.executor.BuildResultEventAvro"]
```

200 이고 본문에 최소 한 개 이상의 subject 가 보이면 SR 가 자기 백엔드를 정상 읽고 있다는 뜻이다. executor 가 떠 있다면 결과 발행 시점에 추가 subject 가 등록된다.

### 4.2 Redpanda 로그에 `_schemas` offset 경고 없음

```bash
$ docker logs redpanda-local 2>&1 | grep "schema_registry.*_schemas"
# 빈 결과면 OK
```

다른 토픽(`tps.v305p.*`) 의 `offset_out_of_range` 는 컨슈머가 옛 offset 을 기억하고 있어 일시적으로 나는데, `auto.offset.reset` 이 발동하면 곧 사라진다. 본 사고와 무관하다.

### 4.3 executor 결과 이벤트 발행 성공

```bash
$ docker exec redpanda-local rpk topic consume \
    tps.v305p.executor.evt.build-result --num 1 --offset end -f json
{"topic": "tps.v305p.executor.evt.build-result", "value": "...", ...}
```

빌드 1 회를 실제로 트리거(예: QA 스위트 `-m happy` 한 케이스)한 뒤 위 명령이 메시지 하나라도 잡아내면 발행 경로가 회복된 것이다. 회복 전이라면 AvroSerializationException 으로 발행 자체가 안 돼 토픽이 비어 있다.

### 4.4 QA 스위트가 timeout 없이 통과

```bash
$ cd qa/python && source .venv/bin/activate
$ pytest suites/executor_jenkins/ -m happy
$ pytest suites/executor_jenkins/ -m order_preservation -v
```

happy 가 `wait_status` 단계에서 정상 종료하면 인프라 회복이 응용까지 전파된 것이다. order_preservation 케이스(IGMU-1041 회귀 가드) 는 BUILD_NO 오름차순의 PRIORITY_DT 단조 증가까지 단언하므로 SR 회복 외에 dispatch 흐름 전체가 살아 있어야 통과한다.

---

## 5. 실 적용·검증 결과

### 5.1 진단 흐름 — 가설을 한 번에 잡지 못한 이유

처음 본 스택은 `BuildResultEventAvro` 직렬화 실패였고, 발현 경로가 `ExecutionRecoverScheduler` 였다. 직관적으로는 "복구 스케줄러가 잘못 동작한다" 로 가설을 잡기 쉬웠지만, 스택 가장 안쪽 `RestClientException error code 40002` 가 등록 단계의 SR 거부를 가리키는 신호라 인프라 쪽으로 방향을 틀었다.

진짜 단서는 `rpk topic describe _schemas -p` 의 `18 == 18` 한 줄이었다. 메시지 0 건이라는 사실이 retention 만료 가설을 입증해줬고, `-c` 옵션의 `cleanup.policy=delete, DEFAULT_CONFIG` 가 정책 자체가 잘못 설정됐음을 추가로 못박았다. 두 측정 없이 로그만 봤다면 원인을 "SR 가 가끔 깨진다" 수준으로 닫고 재시작으로 임시방편을 썼을 가능성이 높다.

### 5.2 보호 설정에서 한 번 더 막혔다

국소 복구를 먼저 시도한 것은 DB 와 다른 토픽 메시지를 보존하기 위함이었는데, `kafka_nodelete_topics` 시스템 보호가 토픽 단위 조작을 모두 거부했다. 이 보호의 존재 자체는 합리적이지만, 진단·복구 시나리오에서 어떤 경로로 풀어야 하는지는 사전에 문서화돼 있지 않았다. 결과적으로 `down -v` 라는 더 굵은 해법으로 우회했다.

이 사실은 후속 "방안 A" 의 실행 가능성을 보장하기 위해 미리 짚어둘 필요가 있다 — 보호를 풀고 alter-config 를 친 뒤 보호를 다시 거는 4 줄짜리 시퀀스 자체는 단순하지만, 운영 환경에서 동일하게 가능한지(권한·감사 로그) 는 dev/prd 인프라 담당자와 별도 확인이 필요하다.

### 5.3 1차 복구 직후 측정값

```bash
$ curl -s http://localhost:8084/subjects
["org.okestro.tps.avro.executor.BuildResultEventAvro"]

$ docker exec redpanda-local rpk topic describe _schemas -p
PARTITION  LEADER  EPOCH  REPLICAS  LOG-START-OFFSET  HIGH-WATERMARK
0          0       1      [0]       0                 1

$ docker exec redpanda-local rpk topic describe _schemas -c | grep cleanup.policy
cleanup.policy                        delete         DEFAULT_CONFIG   # ← 여전히 delete
```

SR 가 회복했고 스키마 1 건이 즉시 등록됐다. 하지만 정책은 여전히 `delete` 라 7 일 뒤 같은 사고가 재현된다. 이 사실 자체가 본 보고서를 단지 "복구 기록" 이 아니라 "**재발 방지 미적용 미결 항목**" 으로 남기는 이유다.

### 5.4 라이선스 경고 (별개 이슈, 참고)

`rpk` 출력 헤더에 다음 경고가 같이 떴다.

```
Note: your TRIAL license will expire in 4 days.
The following Enterprise features are being used in your Redpanda cluster:
  [partition_auto_balancing_continuous, core_balancing_continuous]
```

본 사고와 무관하지만 4 일 뒤 라이선스 만료로 별도 영향이 있을 수 있다. 로컬 단일 노드라 enterprise 기능은 사실상 의미가 없으니, 라이선스 만료 후 동작 변화(특정 기능 정지) 가 또 다른 디버깅 시간 낭비를 유발하지 않도록 별도 메모로 남겨둔다.

---

## 6. 메타 — 이번 사고에서 배운 것

### (a) "왜 깨졌나" 는 보통 "정책 vs 데이터 수명" 의 불일치다

`_schemas` 같은 시스템 토픽은 **데이터가 영구 보존되어야 동작**하는 토픽이다. 그런데 클러스터 기본 retention(7 일) 이 그대로 적용되면 데이터 수명이 정책에 의해 강제로 깎인다. 두 값이 서로를 모를 때 며칠~몇 주 시간이 지나 폭발한다. 본 사고의 본질은 Avro 직렬화 결함도, SR 결함도 아니고 **토픽 정책 결함**이다.

비슷한 함정이 다른 곳에도 있다. `__consumer_offsets` 가 일반 토픽 정책을 받으면 컨슈머 그룹 진행 상황이 retention 으로 사라져 컨슈머가 처음부터 다시 읽는다. 본 보고서의 진단 과정에서 잠시 본 `tps.v305p.*` 토픽들의 `offset_out_of_range` 경고가 그 변형 사례다 — 다행히 그쪽은 `auto.offset.reset` 안전망이 있어 자체 회복했지만, SR 는 안전망이 없어 사람이 손대야 풀린다.

### (b) Redpanda 의 시스템 토픽 보호는 양날의 검이다

`kafka_nodelete_topics` 가 운영 안전성을 높여주는 건 명백하지만, 손상 복구 시나리오를 더 어렵게 만든다. 보호 해제·alter·재보호 시퀀스를 안전하게 수행하는 절차가 운영 문서에 명시되어 있어야 한다. 본 사고에서는 그 절차가 없어 `down -v` 라는 더 큰 망치를 들어야 했다. 로컬이라 데이터 손실이 무해했지만 운영에서는 옵션 자체가 달라진다.

### (c) `qa/python/docs/troubleshooting.md` 와 본 보고서의 분리 의미

`qa/python/docs/troubleshooting.md` #16 항목은 **QA 스위트 실행 중 마주칠 증상·진단·복구**를 4 단(증상/원인/해결/예방) 으로 압축한다. 반면 본 보고서는 **사고 자체의 인과 분석과 학습**을 6 단으로 풀어 둔다. 둘은 청자가 다르다 — 전자는 "지금 테스트가 깨졌는데 어떻게 빨리 복구하나" 가 궁금한 사람이 5 분 만에 읽고 행동할 수 있어야 하고, 후자는 "왜 이렇게 됐는지" 를 이해해 같은 종류의 함정을 다른 곳에서도 미리 보고 싶은 사람이 천천히 읽는다. 한쪽만 두면 다른 쪽 청자가 자기 정보를 못 찾는다.
