# 보안 비교: Basic Auth + Crumb vs TLS + SASL + ACL

> **한줄 요약**: TPS의 Jenkins Basic Auth + Crumb Token 기반 인증을 Kafka/RedPanda의 TLS 암호화 + SASL 인증 + ACL 권한 관리로 대체하여, 전송 계층부터 애플리케이션 계층까지 3단계 보안을 확보한다.

---

## 1. AS-IS: TPS 보안 방식

### 1.1 Jenkins 통신 보안

**Basic Authentication (기본 인증)**
```
요청: POST http://jenkins.example.com/api
헤더: Authorization: Basic base64(username:password)
```

- Base64 인코딩된 인증 정보를 HTTP 헤더에 포함
- HTTP 평문 전송 가능 (HTTPS 미설정 시)
- 매 요청마다 인증 정보 전송

**Crumb Token (CSRF 토큰)**
```
1단계: GET /crumbIssuer/api/xml → Crumb 토큰 획득
2단계: POST /job/build
       헤더: X-Crumb-Header: [token]
```

- CSRF(Cross-Site Request Forgery) 방지용
- 클라이언트가 getCrumb() → 토큰 획득 → 매 POST 요청에 포함
- Jenkins는 토큰 검증 후 요청 승인

### 1.2 REST 서비스 간 보안

**내부 네트워크 신뢰 모델**
```
Service A → (Basic Auth) → Service B
           (FeignClient)
```

- 인트라넷 가정: 같은 네트워크 내 서비스는 신뢰
- 서비스 간 인증 없음 (또는 선택적)
- 토큰/Basic Auth 헤더로 처리

**로그에 인증 정보 노출**
```
2024-02-16 10:30:45 [INFO] GET http://admin:password123@service-b.local/api
```
- URL에 인증 정보 포함 → 로그, 모니터링, 감사 추적에 평문 노출
- 버전 관리 시스템에 실수로 커밋될 위험

### 1.3 문제점 분석

| # | 문제 | 위험도 | 영향 |
|---|------|--------|------|
| 1 | HTTP 평문 전송 | **높음** | 네트워크 스니핑으로 Base64 인증 정보 쉽게 탈취 |
| 2 | 인증 정보 URL 포함 | **높음** | 로그, 모니터링, 감사 추적에 평문 노출 |
| 3 | 서비스 간 인증 없음 | **높음** | 네트워크 침입 시 무제한 API 접근 가능 |
| 4 | 세분화된 권한 없음 | **중간** | 사용자별 읽기/쓰기 구분 불가능 |
| 5 | Crumb 토큰 저장 문제 | **중간** | 토큰 탈취 시 CSRF 공격 가능 |
| 6 | 감사 추적 부재 | **중간** | 누가 언제 무엇을 했는지 추적 불가 |

**현실 예시**:
```
공격 시나리오:
1. 공격자가 내부 네트워크에 침입
2. 스니핑으로 admin:password123 탈취
3. 모든 서비스에 무제한 접근 가능
4. 토픽 삭제, 데이터 수정 등 악의적 행위
```

---

## 2. TO-BE: TLS + SASL + ACL (RedPanda 보안)

### 2.1 3단계 보안 계층 아키텍처

```
┌─────────────────────────────────────────┐
│ Application Layer                       │
│ ┌─────────────────────────────────────┐ │
│ │ ACL (Access Control List)           │ │
│ │ • 토픽별 read/write/create/delete   │ │
│ │ • 사용자별 권한 세분화               │ │
│ │ • rpk acl create로 관리              │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ Authentication Layer                    │
│ ┌─────────────────────────────────────┐ │
│ │ SASL (Simple Authentication...)     │ │
│ │ • SCRAM-SHA-256/512                 │ │
│ │ • 클라이언트 신원 검증               │ │
│ │ • Kubernetes Secret 관리            │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│ Transport Layer                         │
│ ┌─────────────────────────────────────┐ │
│ │ TLS (Encryption)                    │ │
│ │ • AES-256 암호화                    │ │
│ │ • mTLS (mutual TLS)                 │ │
│ │ • cert-manager 자동 갱신            │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

각 계층의 역할:
- **TLS**: 네트워크 전송 데이터 암호화 (도청 방지)
- **SASL**: 클라이언트 신원 인증 (인증 없는 접근 방지)
- **ACL**: 인증된 클라이언트의 작업 권한 제한 (권한 초과 방지)

### 2.2 TLS (Transport Layer Security) 설정

**목표**: 전송 계층 암호화로 통신 도청 방지

**구현 방식**
```yaml
# RedPanda broker 설정
redpanda:
  kafka_api:
    - address: 0.0.0.0
      port: 9092
      name: internal
  kafka_api_tls:
    - address: 0.0.0.0
      port: 9093
      name: internal_tls
      enabled: true
      cert_file: /etc/certs/broker.crt
      key_file: /etc/certs/broker.key
      truststore_file: /etc/certs/ca.crt
      require_client_auth: true  # mTLS: 클라이언트도 인증서 제시
```

**인증서 관리 (Kubernetes)**
```bash
# 1. cert-manager로 자동 인증서 생성/갱신
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: redpanda-broker-cert
spec:
  secretName: redpanda-broker-tls
  issuerRef:
    name: selfsigned-issuer
  commonName: redpanda-broker.default.svc.cluster.local
  dnsNames:
    - redpanda-broker.default.svc.cluster.local
    - redpanda-broker

# 2. 인증서 자동 갱신 (만료 30일 전)
```

**클라이언트 설정 (Spring Boot)**
```properties
# src/main/resources/application.yml
spring.kafka.security.protocol=SSL
spring.kafka.ssl.trust-store-location=classpath:kafka.client.truststore.jks
spring.kafka.ssl.trust-store-password=truststore_password
spring.kafka.ssl.key-store-location=classpath:kafka.client.keystore.jks
spring.kafka.ssl.key-store-password=keystore_password
spring.kafka.ssl.key-password=key_password
```

**TLS 수준별 보안 강화**
| 수준 | 설정 | 도청 방지 | 인증 |
|------|------|---------|------|
| 1 | TLS (단방향) | ✓ | Broker만 인증 |
| 2 | TLS + SASL | ✓ | Broker + Client |
| 3 | mTLS + SASL | ✓ | 양방향 인증 + 비밀번호 |

### 2.3 SASL (Simple Authentication and Security Layer) 인증

**목표**: 클라이언트 신원 검증 (인증 없는 접근 방지)

**SASL 메커니즘 비교**
| 메커니즘 | 구현 | 강도 | Kafka 지원 | 선택 이유 |
|---------|------|------|-----------|---------|
| PLAIN | 평문 비밀번호 | 약함 | ✓ | PoC 개발 |
| SCRAM-SHA-256 | 해시(256bit) | 중간 | ✓ | 표준 |
| SCRAM-SHA-512 | 해시(512bit) | 강함 | ✓ | **프로덕션 권장** |
| OAUTHBEARER | OAuth2 토큰 | 강함 | ✓ | 클라우드 환경 |

**SCRAM-SHA-512 동작 원리**
```
클라이언트                           Broker
   │                                  │
   ├─ SaslAuthenticateRequest ──────> │
   │  (username, mechanism)            │
   │                                  │
   │ <──── SCRAM Challenge ────────── │
   │       (salt, iterations)          │
   │                                  │
   │ ClientProof = PBKDF2(           │
   │   password, salt, iterations,    │
   │   SHA-512                        │
   │ )                                │
   │                                  │
   ├─ SaslAuthenticateRequest ──────> │
   │  (ClientProof)                    │
   │                                  │
   │ <──── Success ────────────────── │
   │
```

**RedPanda SASL 설정**
```yaml
# redpanda.yaml
redpanda:
  kafka_api_tls:
    - address: 0.0.0.0
      port: 9093
      enabled: true
      require_client_auth: true

# SASL 메커니즘 활성화
security:
  sasl:
    enabled: true
    mechanism: SCRAM
    hash_algorithm: SHA512
```

**사용자 관리**
```bash
# 1. admin 사용자 생성 (비밀번호 관리)
rpk acl user create admin --password [strong_password]

# 2. producer 사용자
rpk acl user create producer --password [strong_password]

# 3. consumer 사용자
rpk acl user create consumer --password [strong_password]

# 4. Kubernetes Secret으로 비밀번호 관리
kubectl create secret generic redpanda-credentials \
  --from-literal=admin-password=<pwd> \
  --from-literal=producer-password=<pwd> \
  --from-literal=consumer-password=<pwd>
```

**Spring Boot SASL 설정**
```properties
# Producer 설정
spring.kafka.security.protocol=SASL_SSL
spring.kafka.sasl.mechanism=SCRAM-SHA-512
spring.kafka.sasl.jaas.config=\
  org.apache.kafka.common.security.scram.ScramLoginModule required \
  username="producer" \
  password="${KAFKA_PRODUCER_PASSWORD}";

# Consumer 설정도 동일하게 username만 변경
# username="consumer"
```

### 2.4 ACL (Access Control List) 권한 관리

**목표**: 세분화된 권한으로 최소 권한 원칙(PoLP) 구현

**권한 종류**
```
• All: 모든 권한
• Read: 토픽 읽기, Consumer Group 읽기
• Write: 토픽 쓰기
• Create: 토픽/파티션 생성
• Delete: 토픽/파티션 삭제
• Alter: 토픽 설정 변경
• Describe: 토픽 메타데이터 조회
• ClusterAction: Broker 명령어 실행
```

**실무 ACL 설계**
```bash
# 1. Producer 권한: topic-events에 write만 허용
rpk acl create \
  --allow-principal=User:producer \
  --operation=write \
  --topic=topic-events

# 2. Consumer 권한: topic-events 읽기 + consumer-group 읽기
rpk acl create \
  --allow-principal=User:consumer \
  --operation=read \
  --topic=topic-events

rpk acl create \
  --allow-principal=User:consumer \
  --operation=read \
  --group=consumer-group-1

# 3. Admin 권한: 모든 토픽 모든 작업
rpk acl create \
  --allow-principal=User:admin \
  --operation=all \
  --topic='*'

# 4. ACL 확인
rpk acl list

# 5. ACL 삭제
rpk acl delete \
  --allow-principal=User:producer \
  --operation=write \
  --topic=topic-events
```

**권한 구조 다이어그램**
```
┌────────────────────────────────────────────┐
│ RedPanda Broker                            │
├────────────────────────────────────────────┤
│ Topic: topic-events                        │
│ ┌──────────────────────────────────────┐   │
│ │ admin (User)                         │   │
│ │ ├─ Read: ✓                           │   │
│ │ ├─ Write: ✓                          │   │
│ │ ├─ Create: ✓                         │   │
│ │ └─ Delete: ✓                         │   │
│ ├──────────────────────────────────────┤   │
│ │ producer (User)                      │   │
│ │ ├─ Read: ✗                           │   │
│ │ └─ Write: ✓                          │   │
│ ├──────────────────────────────────────┤   │
│ │ consumer (User)                      │   │
│ │ ├─ Read: ✓                           │   │
│ │ └─ Write: ✗                          │   │
│ └──────────────────────────────────────┘   │
└────────────────────────────────────────────┘
```

**최소 권한 원칙 (Principle of Least Privilege)**
| 역할 | 필요 권한 | ACL 설정 |
|------|---------|---------|
| Producer | Topic write | write: topic-events |
| Consumer | Topic + Group read | read: topic-events, consumer-group-1 |
| Monitor | 읽기 전용 | describe: '*' |
| Admin | 모든 작업 | all: '*' |

---

## 3. PoC vs 프로덕션 비교

### 3.1 보안 설정 단계별 진화

| 항목 | Phase 1 (현재 PoC) | Phase 2 (준프로덕션) | Phase 3 (프로덕션) |
|------|-------------------|-------------------|------------------|
| **TLS** | ❌ 비활성화 | ⚠️ 자체 서명 인증서 | ✅ 신뢰된 CA |
| **SASL** | ❌ 비활성화 | ⚠️ SCRAM-SHA-256 | ✅ SCRAM-SHA-512 |
| **ACL** | ❌ 비활성화 (allow.all) | ⚠️ 기본 권한만 | ✅ 세분화된 권한 |
| **인증서 관리** | - | ⚠️ 수동 갱신 | ✅ cert-manager |
| **Secret 관리** | application.yml | ⚠️ ConfigMap | ✅ Kubernetes Secret |
| **감사 추적** | ❌ 없음 | ⚠️ 로그만 | ✅ 중앙 감사 로그 |
| **mTLS** | ❌ 없음 | ❌ 없음 | ✅ 클라이언트도 인증 |

### 3.2 현재 PoC 설정 (보안 비활성화)

**이유**: 빠른 개발/테스트, 복잡도 최소화

```yaml
# current-poc.yaml
broker:
  listeners:
    kafka:
      - address: 0.0.0.0:9092
        security_protocol: PLAINTEXT  # 평문 전송

  # SASL 비활성화
  # ACL 비활성화 (모든 요청 허용)
```

**위험성**
```
prod 환경에 PoC 코드 배포 시:
→ 모든 서비스 무제한 접근 가능
→ 악의적 사용자 토픽 삭제/수정 가능
→ 규제 위반 (PCI-DSS, HIPAA 등)
→ 보안 감사 실패
```

### 3.3 프로덕션 마이그레이션 체크리스트

```yaml
보안 전환 작업:
□ 1. TLS 인증서 발급 (cert-manager)
□ 2. SASL 사용자 생성 (admin, producer, consumer)
□ 3. Kubernetes Secret에 비밀번호 저장
□ 4. ACL 규칙 정의 및 적용
□ 5. Spring Boot 클라이언트 설정 업데이트
□ 6. 로컬/스테이징 테스트
□ 7. 모니터링 및 감사 로그 설정
□ 8. 인증서 갱신 프로세스 자동화
□ 9. 팀 교육 (보안 best practices)
□ 10. 정기적 보안 감사 (분기마다)
```

---

## 4. Spring Boot 보안 설정 실행 가이드

### 4.1 프로덕션 SASL_SSL 설정

**application-prod.yml**
```yaml
spring:
  kafka:
    bootstrap-servers: redpanda-broker-0.redpanda.default.svc.cluster.local:9093

    security:
      protocol: SASL_SSL

    sasl:
      mechanism: SCRAM-SHA-512
      jaas:
        config: |
          org.apache.kafka.common.security.scram.ScramLoginModule required
          username="${KAFKA_USERNAME}"
          password="${KAFKA_PASSWORD}";

    ssl:
      trust-store-location: classpath:kafka.client.truststore.jks
      trust-store-password: ${KAFKA_TRUSTSTORE_PASSWORD}
      trust-store-type: JKS

      # mTLS용 클라이언트 인증서 (선택사항)
      key-store-location: classpath:kafka.client.keystore.jks
      key-store-password: ${KAFKA_KEYSTORE_PASSWORD}
      key-password: ${KAFKA_KEY_PASSWORD}
```

**환경변수 관리**
```bash
# Kubernetes Secret 생성
kubectl create secret generic kafka-credentials \
  --from-literal=username=producer \
  --from-literal=password=<strong_pwd> \
  --from-literal=truststore-password=<pwd> \
  --from-literal=keystore-password=<pwd> \
  --from-literal=key-password=<pwd>

# Pod에 주입
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
  - name: app
    env:
    - name: KAFKA_USERNAME
      valueFrom:
        secretKeyRef:
          name: kafka-credentials
          key: username
    - name: KAFKA_PASSWORD
      valueFrom:
        secretKeyRef:
          name: kafka-credentials
          key: password
```

### 4.2 truststore 생성 및 관리

**Java Keystore에 CA 인증서 임포트**
```bash
# 1. RedPanda 브로커의 CA 인증서 추출
kubectl get secret redpanda-broker-tls -o jsonpath='{.data.ca\.crt}' | \
  base64 -d > ca.crt

# 2. Keystore 생성
keytool -import \
  -alias redpanda-ca \
  -file ca.crt \
  -keystore kafka.client.truststore.jks \
  -storepass truststore_password \
  -noprompt

# 3. 인증서 확인
keytool -list -v -keystore kafka.client.truststore.jks \
  -storepass truststore_password

# 4. Kubernetes ConfigMap으로 배포
kubectl create configmap kafka-truststore \
  --from-file=kafka.client.truststore.jks
```

### 4.3 클라이언트 코드 예시

**Producer 설정**
```java
@Configuration
public class KafkaProducerConfig {

    @Bean
    public ProducerFactory<String, EventMessage> producerFactory(
            @Value("${spring.kafka.bootstrap-servers}") String bootstrapServers,
            @Value("${kafka.producer.username}") String username,
            @Value("${kafka.producer.password}") String password) {

        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);

        // SASL_SSL 설정
        configProps.put(ProducerConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        configProps.put(ProducerConfig.SASL_MECHANISM, "SCRAM-SHA-512");
        configProps.put(
            ProducerConfig.SASL_JAAS_CONFIG,
            "org.apache.kafka.common.security.scram.ScramLoginModule required " +
            "username=\"" + username + "\" " +
            "password=\"" + password + "\";"
        );

        // TLS 설정
        configProps.put(ProducerConfig.SSL_TRUSTSTORE_LOCATION_CONFIG,
            "classpath:kafka.client.truststore.jks");
        configProps.put(ProducerConfig.SSL_TRUSTSTORE_PASSWORD_CONFIG,
            System.getenv("KAFKA_TRUSTSTORE_PASSWORD"));

        // 기타 설정
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG,
            JsonSerializer.class);
        configProps.put(ProducerConfig.ACKS_CONFIG, "all");
        configProps.put(ProducerConfig.RETRIES_CONFIG, 3);

        return new DefaultProducerFactory<>(configProps);
    }

    @Bean
    public KafkaTemplate<String, EventMessage> kafkaTemplate(
            ProducerFactory<String, EventMessage> producerFactory) {
        return new KafkaTemplate<>(producerFactory);
    }
}
```

**Consumer 설정**
```java
@Configuration
public class KafkaConsumerConfig {

    @Bean
    public ConsumerFactory<String, EventMessage> consumerFactory(
            @Value("${spring.kafka.bootstrap-servers}") String bootstrapServers,
            @Value("${kafka.consumer.username}") String username,
            @Value("${kafka.consumer.password}") String password) {

        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configProps.put(ConsumerConfig.GROUP_ID_CONFIG, "event-consumer-group");

        // SASL_SSL 설정 (Producer와 동일)
        configProps.put(ConsumerConfig.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
        configProps.put(ConsumerConfig.SASL_MECHANISM, "SCRAM-SHA-512");
        configProps.put(
            ConsumerConfig.SASL_JAAS_CONFIG,
            "org.apache.kafka.common.security.scram.ScramLoginModule required " +
            "username=\"" + username + "\" " +
            "password=\"" + password + "\";"
        );

        // TLS 설정
        configProps.put(ConsumerConfig.SSL_TRUSTSTORE_LOCATION_CONFIG,
            "classpath:kafka.client.truststore.jks");
        configProps.put(ConsumerConfig.SSL_TRUSTSTORE_PASSWORD_CONFIG,
            System.getenv("KAFKA_TRUSTSTORE_PASSWORD"));

        // Consumer 설정
        configProps.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        configProps.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
            JsonDeserializer.class);
        configProps.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        configProps.put(JsonDeserializer.VALUE_DEFAULT_TYPE, "com.example.EventMessage");

        return new DefaultConsumerFactory<>(configProps);
    }

    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, EventMessage>
    kafkaListenerContainerFactory(ConsumerFactory<String, EventMessage> consumerFactory) {
        ConcurrentKafkaListenerContainerFactory<String, EventMessage> factory =
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setCommonErrorHandler(new DefaultErrorHandler());
        factory.setConcurrency(3);
        factory.getContainerProperties().setPollTimeout(3000);
        factory.setConsumerFactory(consumerFactory);
        return factory;
    }
}
```

---

## 5. 면접 예상 질문 & 답변

### Q1: Kafka/RedPanda의 3단계 보안 계층을 설명해주세요.

**답변 구조**: 계층별 목표 → 역할 → 장점

**상세 답변**:

Kafka 보안은 네트워크부터 애플리케이션까지 3단계로 구성됩니다.

**첫 번째, 전송 계층(Transport Layer) - TLS 암호화**
- **목표**: 네트워크 통신 도청 방지
- **구현**: AES-256 기반 암호화, 인증서 기반 신원 확인
- **예시**: Broker-Client 간 모든 데이터가 암호화되어 스니핑 불가능

**두 번째, 인증 계층(Authentication Layer) - SASL**
- **목표**: 클라이언트 신원 검증
- **구현**: SCRAM-SHA-512 (Salted Challenge Response Authentication Mechanism)
- **프로세스**:
  - 클라이언트 username/password 제시
  - Broker가 해시 비교로 검증
  - 검증 성공 시에만 접속 허용
- **예시**: 인증되지 않은 사용자 접근 차단

**세 번째, 인가 계층(Authorization Layer) - ACL**
- **목표**: 인증된 사용자의 작업 권한 제한
- **구현**: Role-based Access Control (RBAC)
- **예시**:
  - Producer 사용자: topic-events write만 허용
  - Consumer 사용자: topic-events read만 허용
  - Admin 사용자: 모든 토픽 모든 작업 허용
- **효과**: 한 사용자 침해 시에도 다른 토픽 보호

**결론**: 이 3단계가 "심층 방어(Defense in Depth)"를 구현하여, 한 계층이 침해되어도 다른 계층으로 보호된다는 점이 중요합니다.

**예상 Follow-up 질문**:
- "TLS 없이 SASL만 사용해도 되지 않을까요?" → "비밀번호가 평문으로 네트워크에 노출됩니다."
- "PLAIN 대신 SCRAM을 쓰는 이유?" → "PLAIN은 평문 비밀번호를 보내는 반면, SCRAM은 Challenge-Response로 비밀번호를 보내지 않습니다."

---

### Q2: SASL 메커니즘 종류와 선택 기준은?

**답변 구조**: 메커니즘 종류 → 비교표 → 선택 기준 → 우리 선택

**상세 답변**:

Kafka가 지원하는 SASL 메커니즘은 크게 4가지입니다.

**1. PLAIN (평문 기반)**
```
장점: 구현 간단, 이해하기 쉬움
단점: 비밀번호를 평문으로 전송 (TLS 필수)
사용 시점: 개발/테스트 환경
```

**2. SCRAM (권장)**
```
특징:
- Challenge-Response 기반 인증
- 비밀번호를 평문으로 전송하지 않음
- SCRAM-SHA-256 vs SCRAM-SHA-512 (해시 강도 차이)

동작 원리:
1. Client → "SCRAM-SHA-512, username"
2. Broker ← "salt + iterations 보내기"
3. Client: PBKDF2(password, salt) → ClientProof 계산
4. Broker: 저장된 ClientProof와 비교 → 검증

장점: 비밀번호 평문 전송 없음, 표준 프로토콜
단점: 구현 복잡도 약간 높음
추천: 프로덕션 표준
```

**3. OAUTHBEARER (클라우드 환경)**
```
특징: OAuth2 기반, JWT 토큰 사용
장점: 클라우드 환경 (AWS/GCP) 통합 쉬움
단점: OAuth2 서버 필수, 복잡도 높음
사용 시점: 클라우드 Kafka 서비스 (Confluent Cloud, AWS MSK)
```

**4. GSSAPI (Kerberos)**
```
특징: 엔터프라이즈 SSO
장점: Active Directory 통합
단점: Kerberos 인프라 필수
사용 시점: 대규모 엔터프라이즈 환경
```

**선택 기준 매트릭스**:
| 환경 | 권장 메커니즘 | 이유 |
|------|-----------|------|
| PoC/개발 | PLAIN | 빠른 테스트 |
| 프로덕션 온-프레미스 | SCRAM-SHA-512 | 표준, 보안 강함 |
| 클라우드 (AWS/GCP) | OAUTHBEARER | 클라우드 통합 |
| 엔터프라이즈 | GSSAPI/SCRAM | SSO + 보안 |

**우리 선택 (RedPanda PoC → 프로덕션)**:
- PoC: PLAINTEXT (보안 비활성화, 빠른 개발)
- 프로덕션: SCRAM-SHA-512 (보안 + 운영 복잡도 적절한 균형)

이유: Kubernetes 환경에서 Secret 관리 용이하고, 별도의 SSO/OAuth 인프라가 없기 때문입니다.

---

### Q3: ACL을 실무에서 어떻게 관리하나요?

**답변 구조**: 설계 원칙 → 구체적 예시 → 운영 절차

**상세 답변**:

ACL 관리는 "최소 권한 원칙(Principle of Least Privilege)"을 기반으로 합니다.

**설계 원칙**:

1. **역할별 권한 분리**
```
Producer: write만 (read 불필요)
Consumer: read + describe만
Monitor: describe only (읽기 전용)
Admin: 모든 권한
```

2. **토픽 그룹화**
```
토픽명: topic-{domain}-{type}
예시:
  - topic-order-events (주문 도메인)
  - topic-payment-events (결제 도메인)

권한 설정:
  producer-order: topic-order-* write
  consumer-order: topic-order-* read
```

**구체적 예시 (실무)**:

```bash
# 시나리오: order-service, payment-service 운영

# 1. 사용자 생성
rpk acl user create order-producer --password pwd1
rpk acl user create order-consumer --password pwd2
rpk acl user create payment-producer --password pwd3
rpk acl user create payment-consumer --password pwd4

# 2. 권한 설정
# order-producer: order 토픽에만 write
rpk acl create \
  --allow-principal=User:order-producer \
  --operation=write \
  --topic=topic-order-events

# order-consumer: order 토픽 read + consumer group read
rpk acl create \
  --allow-principal=User:order-consumer \
  --operation=read \
  --topic=topic-order-events

rpk acl create \
  --allow-principal=User:order-consumer \
  --operation=read \
  --group=order-consumer-group

# payment-producer: payment 토픽에만 write
rpk acl create \
  --allow-principal=User:payment-producer \
  --operation=write \
  --topic=topic-payment-events

# 3. 감시/모니터링 권한 (describe only)
rpk acl create \
  --allow-principal=User:monitor \
  --operation=describe \
  --topic='*'

# 4. ACL 확인
rpk acl list
rpk acl list --principal=User:order-producer

# 5. 문제 발생 시 수정
rpk acl delete \
  --allow-principal=User:order-producer \
  --operation=write \
  --topic=topic-order-events

rpk acl create \
  --allow-principal=User:order-producer \
  --operation=write \
  --topic=topic-order-events,topic-payment-events  # 추가 권한
```

**운영 절차 (DevOps 관점)**:

1. **설계 단계**:
   - 서비스별 필요 권한 문서화
   - 역할-권한 매트릭스 작성

2. **배포 단계**:
   ```yaml
   # acl-config.yaml (IaC)
   users:
     - name: order-producer
       password: ${ORDER_PRODUCER_PASSWORD}
       acls:
         - principal: User:order-producer
           operations: [write]
           resources:
             - topic: topic-order-events

   - name: order-consumer
     password: ${ORDER_CONSUMER_PASSWORD}
     acls:
       - principal: User:order-consumer
         operations: [read]
         resources:
           - topic: topic-order-events
           - group: order-consumer-group
   ```

3. **감시 단계**:
   ```bash
   # 권한 변경 감시
   watch -n 5 'rpk acl list'

   # 권한 위반 로그 확인
   kubectl logs -f deployment/redpanda-broker | grep "not authorized"
   ```

4. **리뷰 단계** (분기마다):
   - 불필요한 권한 제거
   - 새 서비스 권한 추가
   - 보안 감시 보고서 작성

**실제 실수 사례**:

```bash
# 잘못된 예 1: 모든 사용자에게 모든 권한
rpk acl create \
  --allow-principal='*' \
  --operation='*' \
  --topic='*'
# → 보안 완전 실패

# 잘못된 예 2: 토픽명 와일드카드 오버 설정
rpk acl create \
  --allow-principal=User:producer \
  --operation=write \
  --topic='*'  # 모든 토픽에 write
# → 우도 내부 토픽 손상 가능

# 올바른 예:
rpk acl create \
  --allow-principal=User:producer \
  --operation=write \
  --topic=topic-app-events  # 명확한 토픽명
```

---

### Q4: PoC에서 보안을 비활성화한 이유와 프로덕션 전환 시 고려사항은?

**답변 구조**: PoC 목표 → 비활성화 이유 → 프로덕션 전환 전략

**상세 답변**:

**PoC 목표**:

PoC (Proof of Concept)는 기술 가능성을 검증하는 단계입니다. 우리 PoC 목표는:

1. RedPanda 메시지 큐 기본 기능 동작 확인
2. Spring Boot 통합 (Producer/Consumer)
3. 아키텍처 적합성 검증
4. 성능/안정성 기초 테스트

이 목표들을 **빠르게** 달성하기 위해 보안을 임시 비활성화했습니다.

**비활성화 이유**:

1. **개발 속도**
   ```
   보안 활성화 시:
   - 인증서 생성 (cert-manager)
   - SASL 사용자 설정
   - ACL 규칙 정의
   - 클라이언트 TLS 설정
   → 초기 1-2주 추가 소요

   보안 비활성화 시:
   - RedPanda 설치 후 즉시 사용
   → 즉시 검증 가능
   ```

2. **복잡도 최소화**
   ```
   보안 활성화 시 디버깅 어려움:
   - TLS 인증서 오류
   - SASL 권한 문제
   - ACL 거부됨 오류
   → 원인 파악 어려움

   보안 비활성화 시:
   - 메시지 송수신만 집중
   → 핵심 문제 파악 용이
   ```

3. **PoC 특성**
   ```
   PoC는 일회용이 아닐 수도 있지만,
   아키텍처 검증에 중점
   → 보안은 검증 후 추가
   ```

**프로덕션 전환 체크리스트**:

**Phase 1: 사전 준비 (1주)**
```yaml
□ 1. 보안 요구사항 정의
     - 데이터 분류 (공개/내부/민감)
     - 규제 요구사항 (GDPR, PCI-DSS 등)
     - 조직 보안 정책 검토

□ 2. 인증서 전략 수립
     - CA 선택 (selfsigned/Let's Encrypt/자체 CA)
     - 인증서 갱신 프로세스 (자동화)
     - mTLS 필요성 판단

□ 3. 사용자/권한 설계
     - 역할 분류 (admin/producer/consumer/monitor)
     - 각 역할별 필요 권한 나열
     - 토픽 그룹화 전략
```

**Phase 2: 기술 구현 (2주)**
```yaml
□ 4. Kubernetes 인증서 인프라 구축
     - cert-manager 설치
     - Certificate 리소스 정의
     - truststore 생성 및 배포

□ 5. RedPanda SASL/ACL 활성화
     - redpanda.yaml에서 security 설정
     - 사용자 생성 (rpk acl user create)
     - ACL 규칙 적용 (rpk acl create)

□ 6. Spring Boot 설정 업데이트
     - application-prod.yml SASL_SSL 설정
     - Kubernetes Secret 연동
     - 환경변수 주입 설정

□ 7. 클라이언트 코드 수정
     - KafkaProducerConfig/ConsumerConfig 업데이트
     - SASL 설정 추가
     - TLS truststore 경로 설정
```

**Phase 3: 검증 (1주)**
```yaml
□ 8. 로컬 테스트
     - docker-compose로 SASL_SSL RedPanda 실행
     - Spring Boot 애플리케이션 연동 테스트
     - 권한 거부 시나리오 테스트

□ 9. 스테이징 환경 배포
     - 프로덕션 config와 동일하게 설정
     - 부하 테스트 수행
     - 성능 영향 측정 (지연시간, 처리량)

□ 10. 모니터링 설정
      - Prometheus 메트릭 수집
      - 인증 실패 로그 모니터링
      - 감사 로그 중앙화 (ELK Stack)
```

**Phase 4: 배포 및 롤백 계획 (3일)**
```yaml
□ 11. 배포 전략
      - Blue-Green 배포 (현재 prod + 신규 prod)
      - 또는 Canary 배포 (10% → 50% → 100%)
      - 롤백 계획 (이전 버전 즉시 복구 가능)

□ 12. 사고 대응 계획
      - TLS 인증서 만료 시 대응
      - SASL 사용자 비밀번호 분실 시 대응
      - ACL 설정 오류로 서비스 중단 시 대응
```

**프로덕션 전환 리스크 및 대응**:

| 리스크 | 원인 | 대응 |
|--------|------|------|
| TLS 인증서 만료 | 갱신 누락 | cert-manager 자동 갱신 + 모니터링 알림 |
| SASL 비밀번호 유출 | 부주의한 Secret 공개 | Secret 암호화 + RBAC + 감시 |
| ACL 설정 오류 | 과도한 권한 부여 | 검토 프로세스 + 정기 감사 |
| 성능 저하 | TLS 암호화 오버헤드 | CPU 리소스 추가 + 모니터링 |
| 클라이언트 연결 실패 | 버전 호환성 문제 | 호환성 테스트 + 문서화 |

**실제 전환 사례**:

```
우리 프로젝트 타임라인:

Month 1-2: PoC (PLAINTEXT)
  ✓ RedPanda 기본 기능 검증
  ✓ Spring Boot 통합 성공
  ✓ 아키텍처 적합성 확인

Month 3: 프로덕션 준비
  ✓ 보안 요구사항 정의
  ✓ 인증서/SASL/ACL 설계
  ✓ 클라이언트 코드 리팩토링

Month 4: 스테이징 검증
  ✓ SASL_SSL 설정 테스트
  ✓ 성능 영향 측정
  ✓ 운영 절차 검증

Month 5: 프로덕션 배포
  ✓ Blue-Green 배포
  ✓ 모니터링 활성화
  ✓ 정기 보안 감사
```

---

## 6. 심화 시나리오 및 트러블슈팅

### 6.1 SASL 인증 실패 디버깅

**현상**: "Authentication failed"
```
ERROR org.apache.kafka.common.KafkaException:
  org.apache.kafka.common.errors.SaslAuthenticationException:
  Authentication failed: Invalid username or password
```

**진단 단계**:
```bash
# 1. RedPanda 로그 확인
kubectl logs -f redpanda-broker-0 | grep -i "sasl\|auth"

# 2. 사용자 존재 확인
rpk acl user list | grep producer

# 3. 사용자 비밀번호 재설정
rpk acl user create producer --password [new_password] --overwrite

# 4. 클라이언트 설정 확인
# Spring Boot 환경변수가 제대로 설정되었는지 확인
echo $KAFKA_USERNAME
echo $KAFKA_PASSWORD  # (실제로는 마스킹되어 보이지 않음)

# 5. 간단한 CLI 클라이언트로 테스트
rpk topic list --brokers=redpanda-broker:9093 \
  --sasl-mechanism=SCRAM-SHA-512 \
  --user=producer \
  --password=[password]
```

### 6.2 ACL 거부됨 (Permission Denied)

**현상**: "Not authorized to access topic"
```
org.apache.kafka.common.errors.TopicAuthorizationException:
  Not authorized to access Topic: [topic-events]
```

**진단 단계**:
```bash
# 1. 해당 사용자의 ACL 확인
rpk acl list --principal=User:producer

# 2. 필요한 ACL 추가
rpk acl create \
  --allow-principal=User:producer \
  --operation=write \
  --topic=topic-events

# 3. Consumer Group 권한도 확인
rpk acl list --group=consumer-group-1

# 필요 시 추가
rpk acl create \
  --allow-principal=User:consumer \
  --operation=read \
  --group=consumer-group-1
```

### 6.3 TLS 인증서 오류

**현상**: "CERTIFICATE_VERIFY_FAILED"
```
WARN io.netty.handler.ssl.SslHandler:
  Failed to parse a received packet:
  ssl_error_rx_record_too_long
```

**원인 분석**:
- truststore에 CA 인증서가 없음
- 또는 인증서 포맷 오류
- 또는 CA 인증서가 만료됨

**해결**:
```bash
# 1. truststore 내용 확인
keytool -list -v -keystore kafka.client.truststore.jks \
  -storepass truststore_password

# 2. CA 인증서 다시 임포트
kubectl get secret redpanda-broker-tls -o jsonpath='{.data.ca\.crt}' | \
  base64 -d > ca.crt

keytool -import \
  -alias redpanda-ca \
  -file ca.crt \
  -keystore kafka.client.truststore.jks \
  -storepass truststore_password \
  -noprompt

# 3. 인증서 검증
openssl x509 -in ca.crt -text -noout
```

---

## 7. 관련 문서 및 참고

### 7.1 내부 문서
- [12. 마이그레이션 전략](./12-migration-strategy.md) - PoC → 프로덕션 전환 가이드
- [09. 모니터링 및 관찰성](./09-monitoring-observability.md) - SASL 인증 로그, 감사 추적
- [03. RedPanda 클러스터 구성](./03-redpanda-cluster-setup.md) - 보안 설정 상세

### 7.2 공식 문서
- [RedPanda Security Documentation](https://docs.redpanda.com/current/security/)
- [Kafka SASL/SSL](https://kafka.apache.org/documentation/#security_sasl)
- [Spring Kafka Security](https://spring.io/blog/2021/04/13/the-apache-kafka-brokers-startup-security-check-explained)

### 7.3 면접 대비 키워드
```
TLS, SASL, ACL, mTLS, SCRAM-SHA-512, Crumb Token
심층 방어(Defense in Depth), 최소 권한 원칙(PoLP)
인증(Authentication) vs 인가(Authorization)
```

---

## 8. 요약 및 정리

### 8.1 3단계 보안 구조 (최종 정리)

```
┌─────────────────────────────────────────────────┐
│ ACL: 누가 무엇을 할 수 있는가                    │
│ (토픽별 read/write/create/delete 권한)         │
├─────────────────────────────────────────────────┤
│ SASL: 당신이 누구인가                           │
│ (SCRAM-SHA-512로 신원 검증)                    │
├─────────────────────────────────────────────────┤
│ TLS: 통신이 안전한가                           │
│ (AES-256으로 암호화, 도청 방지)                 │
├─────────────────────────────────────────────────┤
│ Network: 인프라 계층                           │
│ (Kubernetes, 네트워크 정책)                     │
└─────────────────────────────────────────────────┘
```

### 8.2 면접 5분 핵심 설명

```
"Kafka 보안은 3단계입니다.

첫째, TLS로 전송 데이터를 암호화하여 도청을 방지합니다.

둘째, SASL로 클라이언트를 인증하여 인증되지 않은 접근을 차단합니다.

셋째, ACL로 세분화된 권한을 관리하여, 한 사용자 침해 시에도 다른 토픽을 보호합니다.

우리 PoC는 빠른 검증을 위해 보안을 임시 비활성화했으나,
프로덕션 전환 시 이 3단계를 모두 활성화하여
금융 규제 요구사항(PCI-DSS 등)을 충족합니다."
```

---

**마지막 체크**: 이 문서는 인터뷰 준비용으로 다음을 포함합니다.
- 기술 구조 설명 (다이어그램 포함)
- 실무 예시 (bash 명령어, 설정 파일)
- 면접 예상 질문과 상세 답변
- 트러블슈팅 가이드
- 프로덕션 전환 전략

**복습 추천**:
1. 3단계 보안 구조를 그림으로 직접 그려보기
2. SCRAM-SHA-512 Challenge-Response 프로세스 따라 그려보기
3. ACL 설정 명령어들 직접 실행해보기
4. "면접 예상 질문"을 읽고 답변을 자신의 말로 재작성하기
