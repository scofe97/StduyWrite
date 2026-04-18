# TPS 비동기 메시지 흐름도: REST → Redpanda 전환

TPS의 pipeline-api ↔ ppln-logging-api 간 REST 기반 비동기 통신의 실제 전체 흐름과, Redpanda 메시지큐로 대체했을 때의 개선 흐름을 비교하는 문서.

> 매핑 테이블은 [README.md](README.md#tps-패턴-매핑-ch07) 참고

---

## 메시지 상태 생명주기

ppln-logging-api는 `TB_TPS_MS_021`(상태 테이블)과 `TB_TPS_MS_022`(이력 감사 로그, append-only)로 메시지를 관리한다. 모든 상태 전이마다 MS_022에 이력이 기록된다.

```mermaid
stateDiagram-v2
    [*] --> PNDNG: POST /v3/message/register
    PNDNG --> FRWRD: Forward 성공 (TPS200)
    PNDNG --> FAIL: Forward 실패

    FRWRD --> RSPND: Destination 응답 성공 (stts=true)
    FRWRD --> FAIL: Destination 응답 실패 (stts=false)

    FAIL --> FRWRD: 재시도 성공 (nowMxmmNmtm < dmndMxmmNmtm)
    FAIL --> CSPNF: 최대 재시도 초과 → Source에 실패 통보 실패
    FAIL --> CSPNT: 최대 재시도 초과 → Source에 실패 통보 성공

    RSPND --> CSPNT: Source 응답 전달 성공 (TPS200)
    RSPND --> CSPNF: Source 응답 전달 실패

    CSPNF --> CSPNT: Source 재전달 성공 (5회 이내)
    CSPNF --> END: 5회 모두 실패 → 강제 종료

    CSPNT --> END: 완료

    note right of PNDNG: 스케줄러 5순위 처리
    note right of FAIL: 스케줄러 3순위 처리
    note right of RSPND: 스케줄러 4순위 처리
    note right of CSPNF: 스케줄러 1순위 처리
```

| 상태 | 코드 | 설명 | 스케줄러 우선순위 |
|------|------|------|------------------|
| PNDNG | PENDING | 메시지 등록 완료, Forward 대기 | 5순위 |
| FRWRD | FORWARD | Destination으로 전달 완료, 응답 대기 | - |
| RSPND | RESPOND | Destination에서 응답 수신, Source 전달 대기 | 4순위 |
| CSPNT | COMPLETE | Source에 최종 응답 전달 성공 | - |
| CSPNF | RESPONSE_FAILED | Source 응답 전달 실패 (최대 5회 재시도) | 1순위 |
| FAIL | FAILURE | Destination Forward 실패 (재시도 가능) | 3순위 |
| END | END | 종료 (최종 상태) | - |

> Timeout 처리는 2순위로, 어떤 상태에서든 `mxmmRspnsWaitTermDt < NOW()` 이면 Source에 타임아웃 응답을 보낸다.

---

## AS-IS: 전체 상세 시퀀스 (소스코드 기반)

### Phase 1: 메시지 등록

Source 모듈(예: 외부 시스템)이 ppln-logging-api에 비동기 메시지를 등록한다. 이 시점에서 어디로 Forward할지(`dmndPath`), 결과를 어디로 돌려줄지(`rspnsPath`), 최대 재시도 횟수(`dmndMxmmNmtm`), 타임아웃(`mxmmRspnsWaitTerm`)이 함께 등록된다.

```mermaid
sequenceDiagram
    participant SRC as Source 모듈
    participant CTL as AsyncMessageController<br>/v3/message
    participant UC as MessageUseCase
    participant VAL as MessageValidator
    participant DAO as MessageRegistrationDao
    participant MS21 as TB_TPS_MS_021<br>(상태)
    participant MS22 as TB_TPS_MS_022<br>(이력)

    SRC->>CTL: POST /v3/message/register<br>(AsyncMessageRequest, Avro)
    CTL->>UC: registerAsyncMessage()
    UC->>UC: AsyncMessageMapper: Avro → AsyncMessageVo
    UC->>VAL: validate(request)

    UC->>DAO: registerMessage()
    DAO->>MS21: INSERT (dmndId 자동생성,<br>linkSttsCd=PNDNG,<br>dmndPath, rspnsPath,<br>dmndMxmmNmtm, mxmmRspnsWaitTermDt)
    DAO->>MS22: INSERT (dmndId, linkSttsCd=PNDNG)

    UC-->>CTL: 등록 완료
    CTL-->>SRC: 200 OK (dmndId 반환)

    Note over MS21: 상태: PNDNG<br>스케줄러 5순위 처리 대기
```

### Phase 2: 스케줄러 Forward (PNDNG → FRWRD/FAIL)

`MessageTaskScheduler`가 10초 간격으로 실행되며, 분산 락(`TB_TPS_PL_099`)을 획득한 인스턴스만 처리한다. 5개 우선순위 태스크를 순차 실행하며, PNDNG 처리는 5순위(마지막)이다.

```mermaid
sequenceDiagram
    participant SCH as MessageTaskScheduler<br>(10초 간격)
    participant LOCK as TB_TPS_PL_099<br>(분산 락)
    participant MS21 as TB_TPS_MS_021
    participant MS22 as TB_TPS_MS_022
    participant FC as MessageFeignClient
    participant DST as pipeline-api<br>(Destination, dmndPath)

    SCH->>LOCK: MESSAGE_GROUP 락 획득 시도
    alt 락 획득 실패
        SCH-->>SCH: skip (다른 인스턴스가 처리 중)
    end

    Note over SCH: 5순위 태스크 실행 순서:<br>1. CSPNF 재시도<br>2. Timeout 처리<br>3. FAIL 재시도<br>4. RSPND 처리<br>5. PNDNG 처리

    SCH->>MS21: SELECT WHERE linkSttsCd=PNDNG
    MS21-->>SCH: PNDNG 메시지 목록

    loop 각 PNDNG 메시지
        SCH->>FC: forwardToDestination(dmndPath, messageVo)
        FC->>DST: POST {dmndPath}
        alt rsltCd == TPS200 (성공)
            DST-->>FC: TpsResponse(rsltCd=TPS200)
            SCH->>MS21: UPDATE linkSttsCd=FRWRD,<br>nowMxmmNmtm=1
            SCH->>MS22: INSERT (FRWRD)
        else rsltCd != TPS200 (실패)
            DST-->>FC: TpsResponse(rsltCd=TPS500)
            SCH->>MS21: UPDATE linkSttsCd=FAIL,<br>nowMxmmNmtm=1
            SCH->>MS22: INSERT (FAIL)
        else Exception 발생
            SCH->>MS21: UPDATE linkSttsCd=FAIL
            SCH->>MS22: INSERT (FAIL)
        end
    end

    SCH->>LOCK: 락 해제
```

### Phase 3: pipeline-api Jenkins 실행

ppln-logging-api 스케줄러가 dmndPath(예: `/jenkins/v1/execute/pipeline/async`)로 Forward하면, pipeline-api가 수신하여 Jenkins 빌드를 트리거한다. **HTTP 200을 즉시 반환**한 뒤, `CompletableFuture.runAsync()`로 비동기 실행하고 **Thread.sleep(10000)으로 10초 하드코딩 대기** 후 결과를 ppln-logging-api에 통보한다.

```mermaid
sequenceDiagram
    participant LOG as ppln-logging-api<br>(스케줄러 Forward)
    participant CTL as JenkinsPipelineController<br>/jenkins/v1
    participant SVC as JenkinsServiceImpl
    participant JFC as JenkinsFeignClient
    participant JK as Jenkins 서버
    participant AFC as AsyncMessageFeignClient<br>(→ ppln-logging-api)
    participant RESP as ppln-logging-api<br>/v3/message/response

    LOG->>CTL: POST /execute/pipeline/async<br>(AsyncMessageForwardRequest)
    CTL->>SVC: executePipelineAsync()

    SVC->>JFC: getPipelineInfo(pipelineStruct)
    JFC->>JK: GET /{pipelineStruct}/api/json
    JK-->>JFC: {inQueue, nextBuildNumber}

    alt inQueue=true 또는 inProgress=true
        SVC-->>CTL: 이미 실행 중, 거부
        CTL-->>LOG: TpsResponse(실패)
    else 실행 가능
        SVC-->>CTL: TpsResponse(TPS200,<br>"파이프라인 실행 요청 접수")
        CTL-->>LOG: HTTP 200 (즉시 반환)

        Note over SVC: CompletableFuture.runAsync() 시작<br>(ForkJoinPool 스레드)

        SVC->>JFC: getCrumb()
        JFC->>JK: GET /crumbIssuer/api/json
        JK-->>JFC: {crumb, cookie}

        alt 파라미터 있음
            SVC->>JFC: executePipelineWithParameter(<br>jenkinsUrl, auth, crumb,<br>pipelineStruct, params)
            JFC->>JK: POST /{pipelineStruct}/buildWithParameters
        else 파라미터 없음
            SVC->>JFC: executePipeline(<br>jenkinsUrl, auth, crumb,<br>pipelineStruct)
            JFC->>JK: POST /{pipelineStruct}/build
        end

        JK-->>JFC: 202 Accepted (빌드 큐 등록)

        Note over SVC: Thread.sleep(10000)<br>10초 하드코딩 대기<br>(실제 빌드 완료 확인 없음)

        SVC->>SVC: NotifyCommand 생성<br>{dmndId, stts:true,<br>sttsDtl:{code:TPS200},<br>rspnsData}

        SVC->>AFC: notifyProcessStatus(NotifyCommand)
        AFC->>RESP: POST /v3/message/response<br>(AsyncMessageResponse, Avro)

        Note over SVC: catch Exception → log.error<br>(재시도 없음, fire-and-forget)
    end
```

### Phase 4: 응답 수신 및 Source 전달 (RSPND → CSPNT → END)

ppln-logging-api가 pipeline-api로부터 응답을 받으면 RSPND로 전이하고, 스케줄러 4순위 태스크가 Source에 최종 응답을 전달한다.

```mermaid
sequenceDiagram
    participant PIPE as pipeline-api
    participant CTL as AsyncMessageController<br>/v3/message
    participant UC as MessageUseCase
    participant MS21 as TB_TPS_MS_021
    participant MS22 as TB_TPS_MS_022
    participant SCH as 스케줄러 4순위<br>processRespondMessages
    participant FC as MessageFeignClient
    participant SRC as Source 모듈<br>(rspnsPath)

    PIPE->>CTL: POST /v3/message/response<br>(AsyncMessageResponse, Avro)
    CTL->>UC: processAsyncMessageResponse()
    UC->>UC: Avro → AsyncMessageResponseVo
    UC->>MS21: UPDATE rspnsData = 응답 데이터

    alt stts=true (성공)
        UC->>MS21: UPDATE linkSttsCd=RSPND
        UC->>MS22: INSERT (RSPND)
    else stts=false (실패)
        UC->>MS21: UPDATE linkSttsCd=FAIL
        UC->>MS22: INSERT (FAIL, rspnsData 포함)
    end

    Note over SCH: 다음 스케줄러 사이클 (10초 후)

    SCH->>MS21: SELECT WHERE linkSttsCd=RSPND
    MS21-->>SCH: RSPND 메시지 목록
    SCH->>MS22: 해당 dmndId의 최신 응답 조회

    loop 각 RSPND 메시지
        SCH->>FC: sendResponseToSource(rspnsPath,<br>AsyncMessageFinalResponse)
        FC->>SRC: POST {rspnsPath}

        alt rsltCd == TPS200 (성공)
            SRC-->>FC: TpsResponse(TPS200)
            SCH->>MS21: UPDATE linkSttsCd=CSPNT
            SCH->>MS22: INSERT (CSPNT)
            SCH->>MS21: UPDATE linkSttsCd=END
            SCH->>MS22: INSERT (END)
            Note over MS21: RSPND → CSPNT → END (정상 완료)
        else 실패
            SRC-->>FC: TpsResponse(TPS500) 또는 Exception
            SCH->>MS21: UPDATE linkSttsCd=CSPNF
            SCH->>MS22: INSERT (CSPNF)
            Note over MS21: RSPND → CSPNF (1순위 재시도 대기)
        end
    end
```

### Phase 5: 재시도 흐름

#### 5-1. CSPNF 재시도 (1순위, Source 응답 전달 재시도)

Source에 응답 전달이 실패하면 최대 5회 재시도한다. 5회 모두 실패하면 강제 END 처리된다.

```mermaid
sequenceDiagram
    participant SCH as 스케줄러 1순위<br>processCspnfRetryMessages
    participant MS21 as TB_TPS_MS_021
    participant MS22 as TB_TPS_MS_022
    participant FC as MessageFeignClient
    participant SRC as Source 모듈<br>(rspnsPath)

    SCH->>MS21: SELECT WHERE linkSttsCd=CSPNF
    SCH->>MS22: COUNT(CSPNF) for dmndId

    alt CSPNF 횟수 < 4 (1~4차 시도)
        SCH->>FC: sendResponseToSource(rspnsPath, response)
        FC->>SRC: POST {rspnsPath}
        alt 성공
            SRC-->>FC: TPS200
            SCH->>MS21: UPDATE CSPNT → END
            SCH->>MS22: INSERT (CSPNT), INSERT (END)
        else 실패
            SRC-->>FC: 실패
            SCH->>MS22: INSERT (CSPNF,<br>"원천지 응답 전송 실패(X/5)")
        end
    else CSPNF 횟수 >= 4 (5차, 최종 시도)
        SCH->>FC: sendResponseToSource(rspnsPath, 최대재시도초과응답)
        FC->>SRC: POST {rspnsPath}
        alt 성공
            SCH->>MS21: UPDATE CSPNT → END
        else 최종 실패
            SCH->>MS22: INSERT (CSPNF, "5/5")
            SCH->>MS21: UPDATE linkSttsCd=END (강제 종료)
            SCH->>MS22: INSERT (END)
            Note over MS21: 5회 모두 실패 → 강제 END
        end
    end
```

#### 5-2. FAIL 재시도 (3순위, Destination Forward 재시도)

Destination으로의 Forward가 실패하면 `dmndMxmmNmtm`(메시지별 설정)까지 재시도한다. 최대 횟수를 초과하면 Source에 실패 결과를 통보한다.

```mermaid
sequenceDiagram
    participant SCH as 스케줄러 3순위<br>processFailedMessages
    participant MS21 as TB_TPS_MS_021
    participant MS22 as TB_TPS_MS_022
    participant FC as MessageFeignClient
    participant DST as Destination<br>(dmndPath)
    participant SRC as Source 모듈<br>(rspnsPath)

    SCH->>MS21: SELECT WHERE linkSttsCd=FAIL

    loop 각 FAIL 메시지
        alt nowMxmmNmtm < dmndMxmmNmtm (재시도 가능)
            SCH->>FC: forwardToDestination(dmndPath, messageVo)
            FC->>DST: POST {dmndPath}
            SCH->>MS21: nowMxmmNmtm++
            alt 성공
                DST-->>FC: TPS200
                SCH->>MS21: UPDATE linkSttsCd=FRWRD
                SCH->>MS22: INSERT (FRWRD)
            else 실패
                DST-->>FC: 실패
                SCH->>MS22: INSERT (FAIL)
                Note over MS21: 다음 사이클에 재시도
            end
        else nowMxmmNmtm >= dmndMxmmNmtm (최대 재시도 초과)
            SCH->>MS22: 최신 실패 응답 조회
            SCH->>FC: sendResponseToSource(rspnsPath, 실패응답)
            FC->>SRC: POST {rspnsPath}
            alt Source 통보 성공
                SCH->>MS21: UPDATE CSPNT → END
            else Source 통보 실패
                SCH->>MS21: UPDATE linkSttsCd=CSPNF
                Note over MS21: 1순위 CSPNF 재시도 대기
            end
        end
    end
```

### Phase 6: 타임아웃 처리 (2순위)

등록 시 설정한 `mxmmRspnsWaitTermDt` 시간을 초과하면 어떤 상태에서든(END, CSPNT, CSPNF 제외) 타임아웃으로 처리한다.

```mermaid
sequenceDiagram
    participant SCH as 스케줄러 2순위<br>processTimeoutMessages
    participant MS21 as TB_TPS_MS_021
    participant FC as MessageFeignClient
    participant SRC as Source 모듈<br>(rspnsPath)

    SCH->>MS21: SELECT WHERE<br>linkSttsCd NOT IN (CSPNT, CSPNF, END)<br>AND mxmmRspnsWaitTermDt < NOW()

    loop 각 타임아웃 메시지
        SCH->>FC: sendTimeoutResponseToSource(rspnsPath)
        FC->>SRC: POST {rspnsPath}<br>(sttsDtl: {code:TPS408, message:"타임아웃"})

        alt 성공
            SCH->>MS21: UPDATE CSPNT → END
        else 실패
            SCH->>MS21: UPDATE linkSttsCd=CSPNF
            Note over MS21: 1순위 CSPNF 재시도 대기
        end
    end
```

---

## AS-IS 문제점 분석

소스코드에서 확인된 핵심 문제:

| # | 문제 | 위치 | 영향 |
|---|------|------|------|
| 1 | **Thread.sleep(10000) 하드코딩** | `JenkinsServiceImpl:237` | Jenkins 빌드 완료 여부와 무관하게 10초 후 성공으로 통보. 실제 빌드가 10초 이상 걸리면 거짓 성공 |
| 2 | **Jenkins 상태 폴링 미구현** | `LoggingComponentV4` (주석 처리) | 빌드 진행률 추적 불가, 실패 감지 불가 |
| 3 | **fire-and-forget 패턴** | `CompletableFuture.runAsync()` | 통보 실패 시 재시도 없음, 예외는 로그만 남김 |
| 4 | **10초 폴링 지연** | `MessageTaskScheduler` | 최악의 경우 메시지 하나에 상태 전이마다 10초 지연 (등록→전달→응답→완료: 최소 30~40초) |
| 5 | **단일 스레드 스케줄러** | `SchedulerConfig(poolSize=1)` | 메시지 수 증가 시 병목, 5개 태스크가 순차 실행 |
| 6 | **DB 폴링 부하** | 매 10초마다 5개 SELECT | 메시지 누적 시 DB 부하 증가 |
| 7 | **Jenkins Webhook 미사용** | pipeline-api 전체 | 빌드 완료 이벤트를 받지 않고 하드코딩 대기 |

---

## TO-BE: Redpanda 이벤트 드리븐 흐름

AS-IS의 문제점을 해결하는 이벤트 기반 아키텍처. DB 폴링과 스케줄러를 토픽 기반 즉시 전달로 대체하고, Thread.sleep을 이벤트 구독으로 대체한다.

```mermaid
sequenceDiagram
    participant SRC as Source 모듈
    participant SVC as PipelineService
    participant PRD as PipelineProducer
    participant RP1 as pipeline.request<br>(Redpanda 토픽)
    participant WKR as JenkinsWorkerConsumer
    participant JK as Jenkins 서버
    participant RP2 as pipeline.result<br>(Redpanda 토픽)
    participant LGC as LoggingConsumer
    participant STS as MessageStatusService<br>(인메모리)
    participant RP3 as pipeline.notification<br>(Redpanda 토픽)

    SRC->>SVC: 파이프라인 실행 요청
    SVC->>PRD: produce(PipelineRequestEvent)
    PRD->>RP1: publish
    SVC-->>SRC: 202 Accepted (즉시 반환)

    Note over RP1: 이벤트 발행 즉시 전달<br>(폴링 지연 없음)

    RP1-->>WKR: consume (자동 구독)
    WKR->>STS: updateStatus(PROCESSING)
    WKR->>JK: POST /{pipelineStruct}/build
    JK-->>WKR: 202 Accepted

    Note over WKR,JK: Jenkins 빌드 완료까지<br>비동기 대기<br>(Thread.sleep 없음)

    JK-->>WKR: 빌드 완료 (Webhook 또는 폴링)
    WKR->>PRD: produce(PipelineResultEvent)
    PRD->>RP2: publish(결과)

    RP2-->>LGC: consume (자동 구독)
    LGC->>STS: updateStatus(COMPLETED/FAILED)

    LGC->>PRD: produce(NotificationEvent)
    PRD->>RP3: publish(Source 통보)

    RP3-->>SRC: consume (Source가 직접 구독)<br>또는 REST callback

    rect rgb(255, 235, 235)
        Note over WKR,RP2: 실패 시 자동 재시도
        Note over WKR: @RetryableTopic<br>exponential backoff<br>(1s, 2s, 4s, 8s...)
        WKR-->>RP1: retry 토픽으로 이동
        Note over WKR: maxAttempts 초과 시<br>DLQ 토픽으로 격리
        Note over LGC: DLQ 모니터링 →<br>알림/수동 처리
    end
```

---

## AS-IS vs TO-BE 비교

```mermaid
flowchart LR
    subgraph ASIS["AS-IS: REST + Quartz + DB 폴링"]
        A1[Source] -->|REST POST| A2[ppln-logging-api]
        A2 -->|INSERT| A3[(TB_TPS_MS_021<br>TB_TPS_MS_022)]
        A4[스케줄러<br>10초 폴링<br>5개 우선순위] -->|SELECT| A3
        A4 -->|REST Forward| A5[pipeline-api]
        A5 -->|Thread.sleep<br>10초 하드코딩| A5
        A5 -->|REST POST| A2
        A4 -->|REST POST| A1
    end

    subgraph TOBE["TO-BE: Redpanda 이벤트 드리븐"]
        B1[Source] -->|publish| B2[[pipeline.request<br>토픽]]
        B2 -->|consume| B3[JenkinsWorker<br>Consumer]
        B3 -->|실행| B4[Jenkins]
        B3 -->|publish| B5[[pipeline.result<br>토픽]]
        B5 -->|consume| B6[LoggingConsumer]
        B6 -->|publish| B7[[pipeline.notification<br>토픽]]
    end

    ASIS -.->|전환| TOBE

    style ASIS fill:#fff3e0,stroke:#e65100
    style TOBE fill:#e8f5e9,stroke:#2e7d32
    style A3 fill:#ffcdd2,stroke:#c62828
    style B2 fill:#c8e6c9,stroke:#2e7d32
    style B5 fill:#c8e6c9,stroke:#2e7d32
    style B7 fill:#c8e6c9,stroke:#2e7d32
```

| 비교 항목 | AS-IS (REST + Quartz) | TO-BE (Redpanda) |
|-----------|----------------------|------------------|
| **통신 방식** | REST 동기 호출 + DB 폴링 (10초 간격) | 토픽 기반 이벤트 구독 (즉시 전달) |
| **메시지 전달 지연** | 최소 10초 (스케줄러 사이클 대기) | 수 밀리초 (이벤트 발행 즉시) |
| **Jenkins 대기** | `Thread.sleep(10000)` 하드코딩 (빌드 완료 확인 없음) | 이벤트 기반 비동기 대기 (실제 완료 시점 감지) |
| **상태 관리** | DB 2개 테이블 (MS_021 상태 + MS_022 이력) | 인메모리 (PoC) / 토픽 오프셋 기반 |
| **재시도 (Destination)** | 스케줄러 3순위, `dmndMxmmNmtm`까지 10초 간격 | `@RetryableTopic` exponential backoff |
| **재시도 (Source)** | 스케줄러 1순위, 최대 5회 10초 간격 | `@RetryableTopic` + DLQ 자동 격리 |
| **타임아웃** | `mxmmRspnsWaitTermDt` 비교 (스케줄러 2순위) | Consumer timeout + DLQ |
| **동시 처리** | 단일 스레드 (poolSize=1), 5태스크 순차 실행 | Consumer 파티션별 병렬 처리 |
| **결합도** | FeignClient 강결합 (URL 직접 지정) | 토픽으로 느슨한 결합 (Producer/Consumer 독립) |
| **분산 락** | TB_TPS_PL_099 (DB 기반 분산 락) | Kafka Consumer Group (내장 파티션 할당) |
| **감사 로그** | TB_TPS_MS_022 append-only | 토픽 자체가 이벤트 로그 (retention 설정) |
| **확장성** | 스케줄러 인스턴스 1개만 처리 가능 | Consumer 인스턴스 추가로 수평 확장 |
