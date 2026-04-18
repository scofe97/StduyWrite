# 12. Schema Registry 운영 정책 및 토픽-이벤트 관계 설계

## 문서 목적

01 문서에서 8개 토픽의 파티션 키/보존 기간을 설계했지만, Schema Registry 운영 정책과 토픽-이벤트 관계 규칙은 다루지 않았다. 이 문서는 TPS의 기존 70개 Avro 스키마 패턴을 분석하고, 프로덕션 운영에 필요한 정책을 정의한다.

---

## 1. Schema Registry 운영 정책

### 1.1 호환성 전략 선택: FULL_TRANSITIVE

Redpanda는 7가지 호환성 모드를 지원한다. TPS에는 **FULL_TRANSITIVE**를 권장한다.

| 모드 | 방향 | 배포 순서 제약 | TPS 적합성 |
|------|------|--------------|-----------|
| BACKWARD | Consumer가 새 스키마로 이전 메시지 읽기 | Consumer 먼저 | 부분적 |
| FORWARD | Producer가 새 스키마로 발행, 이전 Consumer 읽기 | Producer 먼저 | 부분적 |
| FULL | 양방향 호환 | **순서 무관** | 적합 |
| FULL_TRANSITIVE | 모든 이전 버전과 양방향 호환 | **순서 무관** | **권장** |

**FULL_TRANSITIVE 선택 근거**:

1. **배포 순서 독립성** — TPS는 pipeline-api, workflow-api, ppln-logging-api가 독립 배포된다. 한 모듈이 먼저 배포되어도 다른 모듈의 메시지를 읽을 수 있어야 한다. BACKWARD나 FORWARD는 배포 순서를 강제하므로 운영 부담이 크다.

2. **기존 스키마가 이미 호환** — TPS pipeline-api의 70개 스키마는 optional 필드에 `["null", "string"]` + `default: null` 패턴을 사용한다. 이 패턴은 FULL 호환의 요구사항을 이미 충족한다.

3. **TRANSITIVE가 필요한 이유** — 일반 FULL은 직전 버전과만 호환을 검증한다. v1→v3로 건너뛰는 Consumer가 있을 수 있으므로(배포 지연, 롤백 등), 모든 이전 버전과의 호환을 보장하는 TRANSITIVE가 안전하다.

### 1.2 환경별 설정

| 환경 | `auto.register.schemas` | 등록 방식 | Registry 접근 권한 |
|------|------------------------|----------|------------------|
| Development | `true` | 자동 (개발 편의) | Read/Write |
| Staging | `false` | CI/CD 파이프라인 | Limited Write |
| Production | `false` | CI/CD 파이프라인 | **Read-only** |

프로덕션에서 `auto.register.schemas=true`가 위험한 이유는, 호환되지 않는 스키마가 거버넌스 없이 등록될 수 있고, 롤백할 배포 프로세스가 없으며, 누가 언제 왜 변경했는지 감사 추적이 불가능하기 때문이다.

### 1.3 스키마 진화 규칙

FULL_TRANSITIVE 호환성을 유지하면서 스키마를 변경할 때 따라야 할 규칙이다.

**허용되는 변경**:

| 변경 유형 | 조건 | 예시 |
|----------|------|------|
| 필드 추가 | `default` 값 필수 | `{"name":"newField", "type":["null","string"], "default":null}` |
| 타입 확장 | Avro promotion 규칙 내 | `int` → `long`, `float` → `double` |
| doc 변경 | 무제한 | doc 필드는 스키마 호환성에 영향 없음 |

**금지되는 변경**:

| 변경 유형 | 이유 |
|----------|------|
| 필수 필드 추가 (default 없음) | 이전 Producer가 해당 필드 없이 발행 → 역직렬화 실패 |
| 필드 삭제 | 이전 Consumer가 해당 필드 참조 → 역직렬화 실패 |
| 필드 타입 축소 | `long` → `int` 변환 시 데이터 손실 |
| 필드 이름 변경 | Avro alias로 우회 가능하지만 Schema Registry 호환성 검증 미지원 |
| enum 심볼 삭제 | 이전 Producer가 삭제된 심볼로 메시지 발행 가능 |

### 1.4 호환 불가 변경 대응책

스키마 변경이 호환성을 깨뜨릴 때, 우선순위 순서대로 4가지 대응책이 있다.

**전략 A — 호환 변환 (권장)**: 기존 필드를 deprecated 마킹하고, 새 필드를 default와 함께 추가한다. 모든 Consumer가 새 필드로 전환된 후 deprecated 필드를 제거한다.

```json
// Before
{"name": "status", "type": "string"}

// After (FULL compatible)
{"name": "status", "type": ["null","string"], "default": null, "doc": "DEPRECATED: use statusV2"}
{"name": "statusV2", "type": ["null","string"], "default": null, "doc": "신규 상태 필드"}
```

**전략 B — 새 토픽 + 이중 쓰기**: `tps.workflow.ticket` → `tps.workflow.ticket.v2`로 새 토픽을 생성하고, 전환 기간 동안 양쪽에 이중 발행한다. 모든 Consumer가 v2로 전환되면 v1을 폐기한다.

**전략 C — Subject 삭제 후 재등록**: Schema Registry에서 subject를 삭제하고 새 스키마로 재등록한다. 기존 메시지를 역직렬화할 수 없게 되므로 **비프로덕션 전용**.

**전략 D — 일시적 NONE 모드**: 호환성 모드를 NONE으로 변경하고 등록 후 복원한다. **dev 환경 전용**.

---

## 2. CI/CD 스키마 등록 파이프라인

### 2.1 브랜치 전략

```mermaid
graph LR
    A["feature 브랜치<br>MR 생성"] -->|"testCompatibility만<br>(등록 안 함)"| B["CI 검증"]
    B -->|"COMPATIBLE ✓"| C["develop 머지"]
    C -->|"schemaRegistryRegister<br>(Staging Registry)"| D["Staging 등록"]
    D -->|"main 머지"| E["Production 등록"]

    style A fill:#e3f2fd,stroke:#2196f3,color:#333
    style B fill:#fff3e0,stroke:#ff9800,color:#333
    style C fill:#e8f5e9,stroke:#4caf50,color:#333
    style D fill:#e8f5e9,stroke:#4caf50,color:#333
    style E fill:#e8f5e9,stroke:#4caf50,color:#333
```

feature 브랜치에서는 **절대 스키마를 등록하지 않는다**. 호환성 검증만 수행하고, 실제 등록은 develop/main 머지 시점에만 한다. 실험적 스키마로 Registry가 오염되는 것을 방지하기 위해서다.

### 2.2 Gradle Plugin 설정

TPS pipeline-api의 70개 `.avsc` 파일을 동적으로 등록하는 설정이다.

```groovy
plugins {
    id 'com.github.imflog.kafka-schema-registry-gradle-plugin' version '1.12.0'
}

schemaRegistry {
    url = findProperty('schemaRegistryUrl') ?: 'http://localhost:18081'

    register {
        fileTree('src/main/avro/dto').matching { include '**/*.avsc' }.each { file ->
            def subjectName = file.name.replace('.avsc', '-value')
            subject(subjectName, file.path, 'AVRO')
        }
    }

    compatibility {
        fileTree('src/main/avro/dto').matching { include '**/*.avsc' }.each { file ->
            def subjectName = file.name.replace('.avsc', '-value')
            subject(subjectName, file.path, 'AVRO')
        }
    }
}
```

`.avsc` 파일을 추가/삭제해도 `build.gradle` 수정이 필요 없다. `fileTree`가 동적으로 탐색하기 때문이다.

**CI 파이프라인 명령어**:

```bash
# feature 브랜치 (MR): 호환성 검증만
./gradlew schemaRegistryTestCompatibility -PschemaRegistryUrl=$STAGING_REGISTRY

# develop/main 머지: 실제 등록
./gradlew schemaRegistryRegister -PschemaRegistryUrl=$TARGET_REGISTRY
```

---

## 3. 토픽-이벤트 관계 정책

### 3.1 네이밍 컨벤션

01 문서에서 정의한 8개 토픽에, 08/09/13 문서에서 추가된 토픽을 포함한다.

```
패턴: tps.{domain}.{event-category}

기존 (01 문서):
  tps.workflow.approval            결재 라이프사이클
  tps.workflow.ticket              티켓 라이프사이클
  tps.pipeline.execution           파이프라인 실행 상태
  tps.pipeline.integration         티켓-파이프라인 통합
  tps.user.sync                    LDAP 동기화
  tps.notification                 알림 요청
  tps.audit                        통합 감사 로그
  tps.system.config                시스템 설정

신규 (08/09/13 문서):
  tps.async-message.request        비동기 메시지 요청 (08 UC-1)
  tps.async-message.response       비동기 메시지 응답 (08 UC-1)
  tps.pipeline.status-changed      Jenkins/ArgoCD 상태 변경 (08 UC-2)
  tps.audit.ticket-history         감사 이력 (08 UC-3)
  tps.reservation.execute-trigger  예약 실행 (08 UC-4)
  tps.pipeline.analysis-completed  SonarQube 분석 완료 (13 UC-2)
  tps.scm.merge-request            SCM MR 이벤트 (13 UC-3)
```

### 3.2 Subject Name Strategy

| 전략 | 동작 | TPS 적합성 |
|------|------|-----------|
| **TopicNameStrategy** (기본) | `{토픽명}-value` | **권장** — 토픽별 스키마 관리, 단순 |
| RecordNameStrategy | `{네임스페이스}.{레코드명}` | 부적합 — 동일 레코드가 여러 토픽에서 사용될 때만 |
| TopicRecordNameStrategy | `{토픽명}-{레코드명}` | 선택적 — 하나의 토픽에 여러 스키마 타입일 때 |

TPS는 **TopicNameStrategy**를 기본으로 사용한다. 대부분의 토픽이 단일 스키마 타입을 사용하고, pipeline-api의 70개 스키마가 도메인별로 분리되어 있어 토픽-스키마가 1:1 매핑되기 때문이다.

### 3.3 토픽 내 이벤트 구분 정책

하나의 토픽에 여러 이벤트 타입을 넣어야 하는 경우(예: `tps.workflow.ticket`에 생성/완료/삭제), **Kafka 헤더의 `eventType` 필드로 구분**한다.

```
방식 A: 이벤트 타입별 토픽 분리
  tps.workflow.ticket.created / .completed / .deleted
  → 토픽 수 폭증, 관리 부담 증가

방식 B: 도메인 토픽 + 헤더 구분 (TPS 채택)
  tps.workflow.ticket (단일 토픽)
    header: eventType = TICKET_CREATED | TICKET_COMPLETED | TICKET_DELETED
    header: sourceModule = workflow-api
    header: correlationId = UUID
  → 토픽 수 최소화, Consumer 필터링으로 처리
```

01 문서에서 이미 도메인 단위 토픽을 설계했으므로, 방식 B가 자연스럽다. Consumer에서 `eventType` 헤더로 필터링하면 동일한 효과를 얻는다.

### 3.4 파티션 키 정책 종합

01 문서의 개별 토픽 키를 패턴화한다.

| 패턴 | 파티션 키 | 적용 토픽 | 근거 |
|------|----------|----------|------|
| 엔티티 순서 보장 | 엔티티 ID | approval(`atrzId`), ticket(`tcktNo`), execution(`pplnNo`) | 동일 엔티티의 상태 전이 순서 필수 |
| 사용자 기반 | `userId` | user.sync, notification | 동일 사용자 이벤트 순서 보장 |
| 순서 불필요 | `resourceId` 또는 random | audit, system.config | 처리량 분산 우선 |

---

## 4. TPS 기존 70개 스키마 분석

### 4.1 네임스페이스 패턴

```
org.okestro.tps.pipeline.v3.avro.dto.{domain}.{direction}

domain:    pipeline, cluster, application, image, jUnit, manifest, trigger, reservation 등
direction: request, response
```

`v3`가 네임스페이스에 포함되어 있어, 메이저 버전 변경 시 네임스페이스를 올리는 전략이 이미 준비되어 있다.

### 4.2 필드 네이밍 규칙

TPS 스키마는 한글 도메인 용어를 축약한 camelCase를 사용한다.

| 패턴 | 예시 | 원어 |
|------|------|------|
| `{도메인축약}No` | `pplnNo`, `tcktNo` | 파이프라인번호, 티켓번호 |
| `{도메인축약}Nm` | `clustrNm`, `aplcnNm` | 클러스터명, 애플리케이션명 |
| `{도메인축약}Cd` | `taskCd`, `envrnCd`, `bizMngCd` | 업무코드, 환경코드, 비즈니스관리코드 |

새 스키마 작성 시 이 축약 패턴을 따라야 기존 70개 스키마와 일관성이 유지된다.

### 4.3 optional 필드 패턴

```json
{
  "name": "expln",
  "type": ["null", "string"],
  "default": null,
  "doc": "설명 (선택)"
}
```

모든 optional 필드는 `["null", "실제타입"]` union + `default: null` 형태다. 이 패턴이 FULL_TRANSITIVE 호환성의 기반이 된다.

---

## 5. 캐싱과 장애 대응

Confluent/Redpanda 직렬화 라이브러리는 스키마를 프로세스 힙에 자동 캐싱한다. Schema Registry가 다운되어도 이미 캐싱된 스키마로 기존 메시지를 계속 처리할 수 있다. 새로운 Schema ID를 처음 만났을 때만 Registry 조회가 필요하므로, Registry 장애의 영향은 **신규 스키마 버전 배포 시**에만 발생한다.

| 상황 | 영향 | 대응 |
|------|------|------|
| Registry 일시 다운 | 기존 메시지 처리 정상, 신규 스키마만 실패 | 자동 복구 대기 |
| Registry 데이터 손실 | 모든 스키마 재등록 필요 | CI/CD로 `.avsc` 일괄 재등록 |
| 스키마 ID 불일치 | 역직렬화 실패 | Consumer 재시작으로 캐시 갱신 |

Redpanda는 Schema Registry를 브로커 바이너리에 내장하고, 데이터를 `_schemas` 내부 토픽에 Raft 복제하므로 별도 JVM 프로세스 관리가 불필요하다.

---

## 6. 기존 문서 참조

| 이 문서 섹션 | 관련 문서 | 관계 |
|-------------|----------|------|
| 토픽 네이밍 (3.1) | 01 섹션 4 | 01의 8개 토픽을 확장, 08/09/13에서 추가된 토픽 포함 |
| 파티션 키 (3.4) | 01 섹션 4 | 01의 개별 토픽 키를 패턴화 |
| Avro 스키마 분석 (4) | 09 섹션 4.1 | 09의 "가장 준비됨" 평가 근거 상세화 |
| CI/CD 파이프라인 (2) | 09 Phase 1 | Phase 1 인프라 구축의 구체적 실행 계획 |
