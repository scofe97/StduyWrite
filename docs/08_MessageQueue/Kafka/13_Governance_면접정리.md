# Chapter 13: 거버넌스 (Governance) - 면접 심화 정리

---

## 1. 스키마 관리: 데이터 계약의 핵심

### 1.1 스키마 관리가 필요한 이유

Kafka는 내부적으로 메시지를 바이트 배열로 저장합니다. 직렬화/역직렬화는 클라이언트의 책임이며, Kafka 브로커는 메시지 내용을 이해하지 않습니다. 이는 유연성을 제공하지만, 여러 팀이 같은 토픽을 사용할 때 심각한 문제를 야기할 수 있습니다.

스키마 관리 없이 발생하는 전형적인 시나리오를 생각해봅시다. Producer 팀이 사용자 정보에 `email` 필드를 추가했습니다. 기존 Consumer는 이 필드를 알지 못하므로 역직렬화에 실패하거나, 최악의 경우 잘못된 데이터로 처리를 계속합니다. 반대로 Producer가 필드를 삭제하면, 해당 필드에 의존하는 Consumer가 NullPointerException을 발생시킵니다.

스키마 관리의 핵심 목표는 Producer와 Consumer 간의 데이터 계약(Data Contract)을 명확히 정의하고, 이 계약의 변경이 기존 시스템을 깨뜨리지 않도록 보장하는 것입니다.

### 1.2 호환성 수준의 이해

스키마 호환성은 새 스키마 버전이 이전 또는 이후 버전의 데이터를 처리할 수 있는지를 정의합니다.

**후방 호환성(Backward Compatibility)**은 새 Consumer가 이전 Producer의 데이터를 읽을 수 있음을 보장합니다. 새 스키마로 업그레이드된 Consumer가 업그레이드되지 않은 Producer의 메시지를 처리할 수 있습니다.

후방 호환성에서 허용되는 변경은 필수 필드 삭제와 기본값 있는 선택적 필드 추가입니다. 필수 필드를 추가하면 기존 데이터에 해당 필드가 없으므로 호환성이 깨집니다.

```
후방 호환성 예시:

원본 스키마: { id, name, price, stock }
새 스키마:   { id, name, price }         // stock 삭제 - 허용
새 스키마:   { id, name, price, origin: null }  // 기본값 있는 필드 추가 - 허용
새 스키마:   { id, name, price, origin }        // 필수 필드 추가 - 불허

업그레이드 순서: Consumer 먼저 → Producer 나중
```

**전방 호환성(Forward Compatibility)**은 기존 Consumer가 새 Producer의 데이터를 읽을 수 있음을 보장합니다. Producer가 먼저 업그레이드되어도 기존 Consumer가 계속 동작합니다.

전방 호환성에서 허용되는 변경은 필수 필드 추가와 선택적 필드 삭제입니다. 기존 Consumer는 새 필드를 무시하고, 삭제된 선택적 필드는 기본값으로 처리됩니다.

```
전방 호환성 예시:

원본 스키마: { id, name, price }
새 스키마:   { id, name, price, category }     // 필드 추가 - 허용
새 스키마:   { id, name }                       // 필수 필드 삭제 - 불허

업그레이드 순서: Producer 먼저 → Consumer 나중
```

**전체 호환성(Full Compatibility)**은 양방향 호환성을 모두 보장합니다. 가장 안전하지만 제약도 가장 큽니다. 오직 기본값이 있는 선택적 필드만 추가하거나 삭제할 수 있습니다. 업그레이드 순서에 관계없이 안전합니다.

**Transitive 호환성**은 호환성 검사를 직전 버전뿐만 아니라 모든 이전/이후 버전에 적용합니다. 예를 들어, `BACKWARD_TRANSITIVE`는 새 스키마가 버전 1, 2, 3 모두와 후방 호환됨을 보장합니다.

### 1.3 Schema Registry의 역할과 동작

Schema Registry는 스키마의 중앙 저장소 역할을 합니다. Producer가 메시지를 보낼 때, 전체 스키마를 매번 포함하는 대신 Schema Registry에 스키마를 등록하고 Schema ID만 메시지에 포함합니다. Consumer는 Schema ID로 Schema Registry에서 스키마를 조회합니다.

```
Schema Registry 동작 흐름:

1. Producer → Schema Registry: 스키마 등록 요청
2. Schema Registry: 호환성 검증 후 Schema ID 반환 (또는 거부)
3. Producer → Kafka: [Magic Byte][Schema ID][Avro Data] 전송
4. Consumer → Schema Registry: Schema ID로 스키마 조회
5. Consumer: 스키마를 사용하여 데이터 역직렬화

메시지 구조:
[0] Magic Byte (1 byte) - Confluent Wire Format 식별자
[1-4] Schema ID (4 bytes)
[5+] Avro 페이로드
```

Schema Registry를 사용하면 메시지 크기가 크게 줄어듭니다. 스키마가 292바이트라면, 매 메시지마다 스키마를 포함하는 대신 4바이트의 Schema ID만 포함하면 됩니다.

Schema Registry의 제약사항도 이해해야 합니다. 첫째, Kafka 브로커는 여전히 스키마를 이해하지 못합니다. 악의적이거나 잘못 구성된 Producer가 스키마를 무시하고 잘못된 데이터를 보낼 수 있습니다. 둘째, Schema ID는 의미 없는 순차 번호여서 복구 시 문제가 될 수 있습니다.

이러한 제약을 보완하려면 **Single Producer 패턴**(토픽당 하나의 Producer만 허용), **Broker-side Validation**(Confluent Platform), 또는 **Kafka Proxy**(Conduktor, Kroxylicious)를 고려해야 합니다.

### 1.4 Avro 데이터 형식

Avro는 스키마 기반 이진 직렬화 형식으로, Kafka와 함께 가장 널리 사용됩니다. JSON에 비해 컴팩트하고, 스키마 진화를 잘 지원합니다.

Avro 스키마의 핵심 요소를 이해해야 합니다. `type`은 데이터 타입(record, array, map 등)을 정의합니다. `name`과 `namespace`는 스키마를 고유하게 식별합니다. `fields`는 레코드의 필드 목록을 정의합니다.

Union 타입 `["null", "string"]`은 null 또는 string 값을 허용하며, 선택적 필드를 표현하는 핵심 방법입니다. `default` 값을 지정하면 호환성 있는 스키마 진화가 가능합니다.

```json
{
  "type": "record",
  "name": "User",
  "namespace": "com.example",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

Protobuf도 대안으로 사용됩니다. Avro보다 타입 시스템이 강력하고 다양한 언어 지원이 좋지만, 스키마 진화 규칙이 다르므로 호환성 수준 설정 시 주의가 필요합니다.

---

## 2. Kafka 보안: 계층적 방어

### 2.1 보안 계층 이해

Kafka 보안은 여러 계층으로 구성됩니다. 각 계층은 다른 위협을 방어합니다.

**전송 암호화(TLS)**는 네트워크상의 데이터를 암호화합니다. 중간자 공격(Man-in-the-Middle)으로부터 데이터를 보호합니다. 성능 오버헤드가 있지만 현대 하드웨어에서는 미미합니다.

**인증(Authentication)**은 클라이언트의 신원을 확인합니다. "이 연결이 실제로 결제 서비스인가?"를 검증합니다. mTLS(상호 TLS) 또는 SASL 메커니즘을 사용합니다.

**인가(Authorization)**는 인증된 클라이언트가 특정 작업을 수행할 권한이 있는지 확인합니다. "결제 서비스가 checkout 토픽을 읽을 권한이 있는가?"를 검증합니다. ACL(Access Control List)로 구현합니다.

**저장 암호화(Encryption at Rest)**는 디스크에 저장된 데이터를 암호화합니다. Kafka는 네이티브로 지원하지 않아 OS/Storage 수준이나 Kafka Proxy를 사용합니다.

**종단간 암호화(E2E Encryption)**는 Producer에서 Consumer까지 데이터가 암호화된 상태를 유지합니다. Broker도 데이터를 복호화할 수 없습니다. Custom Serializer로 구현합니다.

### 2.2 TLS 설정 이해

TLS 설정의 핵심은 Keystore와 Truststore의 역할을 이해하는 것입니다.

**Keystore**는 자신의 개인키와 인증서를 저장합니다. Broker는 자신의 키를 사용하여 클라이언트에게 신원을 증명합니다. mTLS에서 클라이언트도 자신의 Keystore가 필요합니다.

**Truststore**는 신뢰할 수 있는 CA의 공개키를 저장합니다. 상대방의 인증서가 신뢰할 수 있는 CA에 의해 서명되었는지 검증합니다.

```
TLS Handshake 과정:

1. Client → Broker: ClientHello (지원하는 암호화 방식)
2. Broker → Client: ServerHello + Broker Certificate
3. Client: Truststore로 Broker Certificate 검증
4. (mTLS의 경우) Client → Broker: Client Certificate
5. (mTLS의 경우) Broker: Truststore로 Client Certificate 검증
6. 양측: 세션 키 생성, 암호화된 통신 시작
```

### 2.3 SASL 인증 메커니즘

SASL(Simple Authentication and Security Layer)은 다양한 인증 방식을 지원하는 프레임워크입니다.

**SASL-GSSAPI(Kerberos)**는 엔터프라이즈 환경에서 널리 사용됩니다. 중앙 집중식 사용자 관리(Active Directory/LDAP)와 통합됩니다. 설정이 복잡하지만 보안성이 높습니다.

**SASL-OAUTHBEARER**는 OAuth 2.0 토큰을 사용합니다. 클라우드 환경이나 마이크로서비스에 적합합니다. Identity Provider(Keycloak, Auth0 등)와 통합됩니다.

**SASL-SCRAM**은 Challenge-Response 방식의 인증입니다. ZooKeeper나 KRaft에 사용자 정보를 저장합니다. 설정이 비교적 간단합니다.

**SASL-PLAIN**은 Username/Password를 평문으로 전송합니다. 반드시 TLS와 함께 사용해야 합니다. 외부 시스템과의 통합을 위해 Callback Handler를 구현할 수 있습니다.

### 2.4 ACL(Access Control List) 심층 이해

ACL은 "누가 무엇을 어디에 할 수 있는가"를 정의합니다.

ACL의 구성 요소는 다음과 같습니다. **Principal**은 권한의 주체(User:alice, Group:team-a)입니다. **Resource Type**은 Cluster, Topic, Group, TransactionalId 중 하나입니다. **Resource Name**은 리소스의 이름이나 패턴입니다. **Operation**은 Read, Write, Create, Delete, Alter, Describe 등입니다. **Permission**은 Allow 또는 Deny입니다.

패턴 타입으로 **Literal**은 정확히 일치하는 리소스에만 적용되고, **Prefixed**는 접두사로 시작하는 모든 리소스에 적용됩니다. 예를 들어, `--resource-pattern-type prefixed --topic orders-`는 orders-created, orders-shipped 등 모든 orders- 토픽에 적용됩니다.

컴포넌트별 필요 권한을 이해해야 합니다.

```
Producer 필요 권한:
- Topic:Write (메시지 발행)
- Topic:Describe (메타데이터 조회)
- Cluster:IdempotentWrite (멱등성 Producer 사용 시)
- TransactionalId:Write (트랜잭션 Producer 사용 시)

Consumer 필요 권한:
- Topic:Read (메시지 소비)
- Topic:Describe (메타데이터 조회)
- Group:Read (Consumer Group 조인)

Kafka Streams 추가 필요 권한:
- Topic:Create (내부 토픽 생성)
- Topic:Write (Changelog 토픽)
- Group:Read (Consumer Group)
```

ACL 설정의 모범 사례는 최소 권한 원칙입니다. 서비스가 필요한 최소한의 권한만 부여합니다. Prefixed 패턴을 사용하여 관련 토픽을 그룹화합니다. 기본적으로 모든 것을 거부하고, 필요한 것만 허용합니다.

---

## 3. 쿼터: 클러스터 보호

### 3.1 쿼터의 필요성

쿼터는 개별 클라이언트가 클러스터 리소스를 과도하게 사용하는 것을 방지합니다. 잘못 구성된 단일 클라이언트가 전체 클러스터를 마비시킬 수 있습니다.

쿼터 없이 발생할 수 있는 시나리오를 생각해봅시다. 새로 배포된 서비스가 실수로 무한 루프에서 메시지를 발행합니다. 이 서비스가 브로커의 모든 I/O 대역폭을 소비합니다. 다른 모든 서비스가 타임아웃을 경험합니다. 연쇄적인 장애(Cascading Failure)가 발생합니다.

쿼터는 이런 상황에서 문제 클라이언트를 자동으로 쓰로틀링하여 다른 클라이언트를 보호합니다.

### 3.2 쿼터의 종류와 동작

**producer_byte_rate**는 초당 Producer가 전송할 수 있는 바이트 수를 제한합니다. 이 제한을 초과하면 Broker가 응답을 지연시킵니다.

**consumer_byte_rate**는 초당 Consumer가 수신할 수 있는 바이트 수를 제한합니다.

**request_percentage**는 브로커 I/O 스레드의 CPU 시간을 제한합니다. 100%는 하나의 I/O 스레드를 완전히 사용할 수 있음을 의미합니다. 8개의 I/O 스레드가 있다면 최대 800%까지 설정 가능합니다.

쿼터 동작 방식을 이해해야 합니다. Broker는 1초 윈도우 내에서 클라이언트의 사용량을 추적합니다. 제한을 초과하면 다음 윈도우까지 응답을 지연시킵니다. 클라이언트는 지연된 응답을 받고 전송 속도를 자동으로 조절합니다.

```
쿼터 동작 예시:

producer_byte_rate = 1MB/s
클라이언트가 0.5초 동안 1MB를 전송

Broker 계산:
- 윈도우 내 전송량: 1MB
- 남은 윈도우: 0.5초
- 허용량: 0.5MB (1MB/s * 0.5s)
- 초과량: 0.5MB
- 쓰로틀 시간: 0.5초 (초과량 / 허용 속도)

Broker는 0.5초 동안 응답을 지연시킴
```

### 3.3 쿼터 설정 전략

쿼터 설정 시 entity 계층을 이해해야 합니다. 가장 구체적인 설정이 우선 적용됩니다.

```
쿼터 우선순위 (높은 → 낮은):
1. /users/{user}/clients/{client-id}
2. /users/{user}/clients/default
3. /users/{user}
4. /users/default/clients/{client-id}
5. /users/default/clients/default
6. /users/default
7. /clients/{client-id}
8. /clients/default
```

**사용자 기반 쿼터**(Principal)가 client.id 기반보다 권장됩니다. client.id는 클라이언트가 임의로 설정할 수 있어 악의적인 우회가 가능하기 때문입니다.

쿼터 도입 전에 반드시 모니터링 체계를 구축해야 합니다. 쿼터 없이 먼저 실제 사용량을 측정하고, 적절한 기본값을 설정한 후, 특정 서비스에 필요한 경우 개별 쿼터를 부여합니다.

---

## 4. 면접 핵심 질문과 모범 답변

### Q1. Schema Registry의 역할과 스키마 호환성 수준에 대해 설명해주세요.

**모범 답변**: Schema Registry는 Kafka 메시지의 스키마를 중앙에서 관리하는 서비스입니다. Producer는 스키마를 등록하고 Schema ID를 받아 메시지에 포함합니다. Consumer는 Schema ID로 스키마를 조회하여 역직렬화합니다. 이를 통해 메시지 크기를 줄이고, Producer-Consumer 간의 데이터 계약을 관리합니다.

호환성 수준은 세 가지가 있습니다. Backward 호환성은 새 Consumer가 이전 데이터를 읽을 수 있음을 보장하며, Consumer를 먼저 업그레이드합니다. Forward 호환성은 기존 Consumer가 새 데이터를 읽을 수 있음을 보장하며, Producer를 먼저 업그레이드합니다. Full 호환성은 양방향을 모두 보장하며, 업그레이드 순서가 자유롭지만 변경 제약이 가장 큽니다.

Transitive 옵션은 직전 버전뿐 아니라 모든 이전/이후 버전과의 호환성을 보장합니다.

### Q2. Kafka의 인증(Authentication)과 인가(Authorization)의 차이와 구현 방법은?

**모범 답변**: 인증은 "당신이 누구인가"를 확인하는 것이고, 인가는 "당신이 무엇을 할 수 있는가"를 결정하는 것입니다.

Kafka의 인증 방법은 크게 두 가지입니다. mTLS는 클라이언트와 브로커가 서로의 인증서를 검증합니다. 인증서의 CN(Common Name)이 Principal로 사용됩니다. SASL은 다양한 메커니즘을 지원하는데, GSSAPI(Kerberos)는 엔터프라이즈 환경에, OAUTHBEARER는 클라우드/마이크로서비스에, SCRAM은 간단한 설정이 필요할 때 적합합니다.

인가는 ACL로 구현합니다. ACL은 Principal(누가), Resource Type/Name(어디에), Operation(무엇을), Permission(허용/거부)으로 구성됩니다. 예를 들어, "User:payment-service가 Topic:checkout을 Read할 수 있다"와 같이 정의합니다. 최소 권한 원칙을 따라 필요한 권한만 부여해야 합니다.

### Q3. Kafka에서 쿼터(Quota)는 왜 필요하고 어떻게 동작하나요?

**모범 답변**: 쿼터는 개별 클라이언트가 클러스터 리소스를 과도하게 사용하는 것을 방지합니다. 잘못 구성된 단일 클라이언트가 전체 클러스터의 성능을 저하시키는 것을 막습니다.

세 가지 종류의 쿼터가 있습니다. producer_byte_rate는 Producer의 초당 전송량을, consumer_byte_rate는 Consumer의 초당 수신량을, request_percentage는 I/O 스레드 CPU 시간을 제한합니다.

동작 방식은 다음과 같습니다. Broker가 1초 윈도우 내 사용량을 추적합니다. 제한을 초과하면 쓰로틀 시간을 계산하여 응답을 지연시킵니다. 클라이언트는 지연된 응답을 받고 자동으로 속도를 조절합니다.

주의할 점은 모니터링 없이 쿼터를 도입하면 안 됩니다. 먼저 실제 사용량을 측정하고, 적절한 기본값을 설정한 후, 필요한 서비스에 개별 쿼터를 부여해야 합니다.

### Q4. Backward와 Forward 호환성에서 각각 어떤 스키마 변경이 허용되나요?

**모범 답변**: Backward 호환성에서는 필드 삭제와 기본값 있는 선택적 필드 추가가 허용됩니다. 새 Consumer가 이전 데이터를 읽을 수 있어야 하므로, 이전 데이터에 없는 필드는 기본값이 있어야 합니다. 반면 필수 필드 추가는 불허됩니다. 이전 데이터에 해당 필드가 없기 때문입니다.

Forward 호환성에서는 필드 추가와 선택적 필드 삭제가 허용됩니다. 기존 Consumer가 새 데이터를 읽을 수 있어야 하므로, 새 필드는 기존 Consumer가 무시하면 됩니다. 반면 필수 필드 삭제는 불허됩니다. 기존 Consumer가 해당 필드를 필요로 하기 때문입니다.

Full 호환성에서는 기본값 있는 선택적 필드만 추가하거나 삭제할 수 있습니다. 양방향 모두 안전해야 하기 때문입니다.

### Q5. Kafka 클러스터를 보안 없는 상태에서 보안 적용 상태로 마이그레이션하는 과정을 설명해주세요.

**모범 답변**: 무중단 마이그레이션을 위해 단계적으로 진행해야 합니다.

1단계로 브로커에 SSL 리스너를 추가합니다. PLAINTEXT:9092와 SSL:9093을 함께 열어두고 Rolling Restart합니다.

2단계로 브로커 간 통신을 암호화합니다. inter.broker.listener.name을 SSL로 변경하고 Rolling Restart합니다.

3단계로 클라이언트를 SSL로 마이그레이션합니다. 각 클라이언트가 SSL 포트로 연결하도록 설정을 변경합니다.

4단계로 PLAINTEXT 리스너를 비활성화합니다. 모든 클라이언트 마이그레이션 확인 후 PLAINTEXT 리스너를 제거하고 Rolling Restart합니다.

5단계로 ACL을 적용합니다. 필요한 모든 ACL을 미리 생성하고, authorizer.class.name을 설정한 후, allow.everyone.if.no.acl.found를 true에서 false로 변경합니다.

각 단계에서 충분히 테스트하고, 문제 발생 시 롤백할 수 있도록 준비해야 합니다.

---

## 5. 실무 체크리스트

- [ ] Schema Registry 도입으로 스키마 중앙 관리 체계 구축
- [ ] 토픽별 적절한 호환성 수준 설정 및 문서화
- [ ] 모든 환경에서 TLS 전송 암호화 적용
- [ ] mTLS 또는 SASL로 클라이언트 인증 구현
- [ ] 최소 권한 원칙에 따른 ACL 설계
- [ ] 쿼터 도입 전 충분한 모니터링 체계 구축
- [ ] 기본 쿼터 설정으로 클러스터 보호
- [ ] 스키마 변경 시 호환성 영향 검토 프로세스 수립

---

## 6. 참고 자료

- [Confluent Schema Registry Documentation](https://docs.confluent.io/platform/current/schema-registry/index.html)
- [Apache Avro Specification](https://avro.apache.org/docs/current/spec.html)
- [Kafka Security Documentation](https://kafka.apache.org/documentation/#security)
- [Kafka Authorization and ACLs](https://kafka.apache.org/documentation/#security_authz)
- [Karapace - Open Source Schema Registry](https://karapace.io/)
