# 1. 전체 아키텍처 및 Webhook 등록

## 1-1. Jenkins Webhook → Kafka 전체 아키텍처

```mermaid
flowchart TB
    subgraph Jenkins["Jenkins Server"]
        JOB[Jenkins Job]
        WH_CONFIG[Webhook 설정]
    end

    subgraph SpringBoot["Spring Boot Application"]
        subgraph WebhookLayer["Webhook 수신 계층"]
            WH_CTRL[WebhookController]
            WH_VALID[Payload Validator]
        end
        
        subgraph KafkaProducer["Kafka Producer 계층"]
            EVENT_CONV[Event Converter]
            KAFKA_TPL[KafkaTemplate]
        end
        
        subgraph KafkaConsumer["Kafka Consumer 계층"]
            LIFECYCLE[BuildLifecycleConsumer]
            ORCHESTRATION[OrchestrationConsumer]
            METRICS[MetricsConsumer]
            NOTIFICATION[NotificationConsumer]
            FAILURE[FailureAnalysisConsumer]
            ARTIFACT[ArtifactConsumer]
            DEPLOY[DeploymentConsumer]
            APPROVAL[ApprovalConsumer]
        end
    end

    subgraph Kafka["Apache Kafka"]
        TOPIC1[devops.jenkins.events]
        TOPIC2[pipeline.build.success]
        TOPIC3[pipeline.build.failure]
        TOPIC4[pipeline.state.changes]
        TOPIC5[deployment.requests]
        TOPIC6[deployment.results]
    end

    %% Jenkins → Spring Boot 흐름
    JOB -->|빌드 이벤트 발생| WH_CONFIG
    WH_CONFIG -->|HTTP POST| WH_CTRL
    WH_CTRL --> WH_VALID
    WH_VALID --> EVENT_CONV
    EVENT_CONV --> KAFKA_TPL
    KAFKA_TPL -->|Produce| TOPIC1

    %% Kafka → Consumers 흐름
    TOPIC1 -->|Consume| LIFECYCLE
    TOPIC1 -->|Consume| METRICS
    
    LIFECYCLE -->|Produce| TOPIC2
    LIFECYCLE -->|Produce| TOPIC3
    
    TOPIC2 -->|Consume| ORCHESTRATION
    TOPIC2 -->|Consume| ARTIFACT
    TOPIC2 -->|Consume| NOTIFICATION
    
    TOPIC3 -->|Consume| FAILURE
    TOPIC3 -->|Consume| NOTIFICATION
    
    ORCHESTRATION -->|Produce| TOPIC4
    ORCHESTRATION -->|Produce| TOPIC5
    
    TOPIC5 -->|Consume| DEPLOY
    DEPLOY -->|Produce| TOPIC6
```

---

## 1-2. Jenkins Webhook 등록 상세 흐름

```mermaid
sequenceDiagram
    autonumber
    participant Admin as 관리자
    participant Jenkins as Jenkins
    participant SB as Spring Boot
    participant Kafka as Kafka

    rect rgb(200, 220, 240)
        Note over Admin,Jenkins: Phase 1: Webhook 설정
        Admin->>Jenkins: Jenkins 관리 접속
        Admin->>Jenkins: Job 설정 > Webhook 추가
        Admin->>Jenkins: URL 입력: http://springboot:8080/webhooks/jenkins
        Admin->>Jenkins: 이벤트 선택 (Started, Completed, Finalized)
        Jenkins-->>Admin: Webhook 설정 완료
    end

    rect rgb(220, 240, 200)
        Note over Jenkins,SB: Phase 2: Spring Boot 준비
        Note right of SB: @PostMapping("/webhooks/jenkins")<br/>WebhookController 준비
        Note right of SB: KafkaTemplate&lt;String, DevOpsEvent&gt;<br/>Producer 설정
        Note right of SB: @KafkaListener 어노테이션<br/>Consumer 설정
    end

    rect rgb(240, 220, 200)
        Note over Jenkins,Kafka: Phase 3: 이벤트 발생 시 흐름
        Jenkins->>Jenkins: 빌드 시작/완료/종료
        Jenkins->>SB: POST /webhooks/jenkins (JSON Payload)
        SB->>SB: Payload 검증
        SB->>SB: DevOpsEvent 변환
        SB->>Kafka: kafkaTemplate.send("devops.jenkins.events", event)
        Kafka-->>SB: ACK
        SB-->>Jenkins: HTTP 200 OK
    end
```
