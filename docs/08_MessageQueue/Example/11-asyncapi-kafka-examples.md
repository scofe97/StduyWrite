# AsyncAPI Kafka 완성본 예제 모음

AsyncAPI 3.x로 Kafka 기반 이벤트 통신을 기술한 실제 완성 예제 3개를 정리한다. 각 예제는 서로 다른 패턴을 보여주므로 실무 작성 시 참고할 수 있다.

---

## 예제 1: Adeo Kafka Request-Reply

실제 기업(Adeo 그룹, 유럽 최대 DIY 리테일)이 AsyncAPI 공식 레포에 제출한 케이스 스터디다. 다중 환경 서버, SASL-SSL 보안, Avro 스키마, Kafka bindings, Request-Reply 패턴, correlation ID를 모두 담고 있어서 실전에서 가장 참고할 만한 예제다.

**출처**: [asyncapi/spec — adeo-kafka-request-reply-asyncapi.yml](https://github.com/asyncapi/spec/blob/master/examples/adeo-kafka-request-reply-asyncapi.yml)

### 주목할 패턴

- **Return Address**: `address: null` + `$message.header#/REPLY_TOPIC`으로 Reply 토픽을 런타임에 결정한다. Reply 토픽이 컴파일 타임에 고정되지 않는 EIP 패턴이다.
- **Avro 스키마 참조**: `schemaFormat: application/vnd.apache.avro;version=1.9.0`으로 JSON Schema 대신 `.avsc` 파일을 직접 참조한다.
- **Correlation ID**: `location: $message.header#/REQUEST_ID`로 JSONPath 기반 메시지 추적을 명세에 포함한다.
- **환경별 서버**: production/staging/dev 3개 환경을 각각 정의하고 동일한 보안 설정을 공유한다.

```yaml
asyncapi: 3.1.0
info:
  title: Adeo AsyncAPI Case Study
  version: '%REPLACED_BY_MAVEN%'
  description: >
    This Adeo specification illustrates how ADEO uses AsyncAPI
    to document some of their exchanges.
  contact:
    name: AsyncAPI Community
    email: case-study@asyncapi.com
  tags:
    - name: costing
      description: Costing channels, used by Costing clients.

# ─── 서버 (3개 환경, SASL-SSL 보안) ──────────────────────────
servers:
  production:
    host: prod.url:9092
    protocol: kafka
    description: Kafka PRODUCTION cluster
    security:
      - $ref: '#/components/securitySchemes/sasl-ssl'
    bindings:
      kafka:
        schemaRegistryUrl: https://schema-registry.prod.url/
  staging:
    host: staging.url:9092
    protocol: kafka
    description: Kafka STAGING cluster for uat and preprod
    security:
      - $ref: '#/components/securitySchemes/sasl-ssl'
    bindings:
      kafka:
        schemaRegistryUrl: https://schema-registry.prod.url/
  dev:
    host: dev.url:9092
    protocol: kafka
    description: Kafka DEV cluster for dev and sit
    security:
      - $ref: '#/components/securitySchemes/sasl-ssl'
    bindings:
      kafka:
        schemaRegistryUrl: https://schema-registry.prod.url/

# ─── 채널 (Kafka 토픽 = 채널) ────────────────────────────────
channels:
  costingRequestChannel:
    address: adeo-{env}-case-study-COSTING-REQUEST-{version}
    description: >
      Use this topic to do a Costing Request to Costing product.
      We use the RecordNameStrategy to infer the messages schema.
    parameters:
      env:
        $ref: '#/components/parameters/Env'
      version:
        $ref: '#/components/parameters/Version'
    bindings:
      kafka:
        replicas: 3
        partitions: 3
        topicConfiguration:
          cleanup.policy:
            - delete
          retention.ms: 60000000
    messages:
      CostingRequest:
        $ref: '#/components/messages/costingRequestV1'

  costingResponseChannel:
    address: null    # Reply 토픽은 런타임에 REPLY_TOPIC 헤더로 결정
    description: >
      This topic is used to REPLY Costing Requests and is targeted
      by the REPLY_TOPIC header.
    messages:
      costingResponse:
        $ref: '#/components/messages/costingResponse'

# ─── 오퍼레이션 (채널과 분리 — v3 핵심) ──────────────────────
operations:
  receiveACostingRequest:
    action: receive
    channel:
      $ref: '#/channels/costingRequestChannel'
    reply:
      channel:
        $ref: '#/channels/costingResponseChannel'
      address:
        location: $message.header#/REPLY_TOPIC
    summary: >
      [COSTING] Request one or more Costing calculation
      for any product
    tags:
      - name: costing
    bindings:
      kafka:
        groupId:
          type: string
          description: Must be prefixed by your svc account.
        x-value.subject.name.strategy:
          type: string
          description: Use RecordNameStrategy in your producer.

# ─── 컴포넌트 ────────────────────────────────────────────────
components:
  correlationIds:
    costingCorrelationId:
      description: Correlation ID based on REQUEST_ID for tracing.
      location: $message.header#/REQUEST_ID

  messages:
    costingRequestV1:
      name: CostingRequestV1
      title: Costing Request V1
      correlationId:
        $ref: '#/components/correlationIds/costingCorrelationId'
      headers:
        type: object
        required:
          - REQUESTER_ID
          - REQUESTER_CODE
          - REQUEST_ID
          - REPLY_TOPIC
        properties:
          REQUEST_ID:
            $ref: '#/components/schemas/RequestId'
          REPLY_TOPIC:
            $ref: '#/components/schemas/ReplyTopic'
          REQUESTER_ID:
            $ref: '#/components/schemas/RequesterId'
          REQUESTER_CODE:
            $ref: '#/components/schemas/RequesterCode'
      payload:
        schemaFormat: application/vnd.apache.avro;version=1.9.0
        schema:
          $ref: https://www.asyncapi.com/resources/casestudies/adeo/CostingRequestPayload.avsc

    costingResponse:
      name: CostingResponse
      title: Costing Response
      correlationId:
        $ref: '#/components/correlationIds/costingCorrelationId'
      headers:
        type: object
        properties:
          CALCULATION_ID:
            $ref: '#/components/schemas/MessageId'
          CORRELATION_ID:
            $ref: '#/components/schemas/CorrelationId'
          REQUEST_TIMESTAMP:
            type: string
            format: date-time
          CALCULATION_TIMESTAMP:
            type: string
            format: date-time
      payload:
        schemaFormat: application/vnd.apache.avro;version=1.9.0
        schema:
          $ref: https://www.asyncapi.com/resources/casestudies/adeo/CostingResponsePayload.avsc

  schemas:
    RequesterId:
      type: string
      description: The Costing requester service account.
      examples: [svc-ecollect-app]
    RequesterCode:
      type: string
      description: The Costing requester code (BU Code).
      examples: ["1"]
    MessageId:
      type: string
      format: uuid
      examples: [1fa6ef40-8f47-40a8-8cf6-f8607d0066ef]
    RequestId:
      type: string
      format: uuid
    CorrelationId:
      type: string
      format: uuid
    ReplyTopic:
      type: string
      description: Kafka topic for Costing Response (Return Address EIP).
      examples: [adeo-case-study-COSTING-RESPONSE-V1]

  parameters:
    Env:
      description: Adeo Kafka Environment.
      enum: [dev, sit, uat1, preprod, prod]
    Version:
      description: Topic version.
      default: V1

  securitySchemes:
    sasl-ssl:
      type: plain
      x-sasl.jaas.config: >-
        org.apache.kafka.common.security.plain.PlainLoginModule required
        username="<CLUSTER_API_KEY>" password="<CLUSTER_API_SECRET>";
      x-security.protocol: SASL_SSL
      x-sasl.mechanism: PLAIN
      description: SASL authentication with SSL encryption.
```

---

## 예제 2: Kafka Order Notification (구조 학습용)

IBM Event Streams 엔지니어(Dale Lane)가 작성한 예제로, v3.0.0의 모든 구성 요소를 망라한다. 특히 **스키마 버전 관리**(discriminator + deprecated)와 **Traits 믹스인 패턴**이 잘 드러나 있어서 구조 학습에 적합하다.

**출처**: [asyncapi-v3-example.yaml (dalelane)](https://gist.github.com/dalelane/22e844da6f831a7466cd0bd6550bce18)

### 주목할 패턴

- **스키마 버전 분기**: `discriminator: version`으로 v1/v2 페이로드를 `oneOf`로 분기한다. v1은 `deprecated: true`로 명시하여 하위 호환을 문서화한다.
- **Traits 믹스인**: `operationTraits`와 `messageTraits`로 공통 Kafka 설정(clientId, groupId, 커스텀 헤더)을 한 번 정의하고 여러 곳에서 재사용한다.
- **Kafka 메시지 키**: `bindings.kafka.key`로 메시지 키의 스키마를 명시한다(파티셔닝 전략 문서화).

```yaml
asyncapi: 3.0.0
id: 'https://github.com/dalelane/my-first-asyncapi-v3-doc'
info:
  title: 'Title of my app'
  version: '0.0.1'
  description: 'This is what **my app** does.'
  license:
    name: Apache 2.0
    url: https://www.apache.org/licenses/LICENSE-2.0.html

# ─── 서버 (IBM Event Streams / OpenShift Kafka) ─────────────
servers:
  eventstreams:
    url: es-kafka-bootstrap-eventstreams.{host}:{port}
    protocol: kafka-secure
    protocolVersion: '3.3.0'
    title: Event Streams Kafka cluster
    description: A secure Kafka cluster running in **OpenShift**.
    variables:
      host:
        default: apps.dale-lane.cp.fyre.ibm.com
      port:
        default: 443
    security:
      - $ref: '#/components/securitySchemes/kafkaEventStreams'
    bindings:
      kafka:
        schemaRegistryUrl: https://my-apicurio-schema-registry.com
        schemaRegistryVendor: apicurio
        bindingVersion: '0.4.0'

defaultContentType: application/json

# ─── 채널 ────────────────────────────────────────────────────
channels:
  ordersTopic:
    address: MODO.ORDERS
    messages:
      newOrderMessage:
        $ref: '#/components/messages/newOrder'
    title: Orders Topic
    servers:
      - $ref: '#/servers/eventstreams'
    bindings:
      kafka:
        topic: MODO.ORDERS
        partitions: 3
        replicas: 3
        topicConfiguration:
          retention.bytes: 1000000000
          max.message.bytes: 1048588
        bindingVersion: '0.4.0'

# ─── 오퍼레이션 ──────────────────────────────────────────────
operations:
  newOrderNotification:
    action: 'receive'
    channel:
      - $ref: '#/channels/ordersTopic'
    title: New order notification
    security:
      - $ref: '#/components/securitySchemes/kafkaEventStreams'
    traits:
      - $ref: '#/components/operationTraits/kafka'

# ─── 컴포넌트 ────────────────────────────────────────────────
components:
  securitySchemes:
    kafkaEventStreams:
      type: scramSha512
      description: Event Streams credentials

  messages:
    newOrder:
      messageId: modoJeansOrderMessage
      name: modoJeansOrder
      title: Modo Jeans New Order notification
      headers:
        type: object
        properties:
          orderSource:
            description: Unique ID of the application used to create the order
            type: string
      payload:
        type: object
        order:
          $ref: '#/components/schemas/newOrder'
      contentType: application/json
      bindings:
        kafka:
          key:                        # Kafka 메시지 키 스키마
            type: object
            required: [region]
            properties:
              region:
                type: string
                enum: [west, east, north, south]
          bindingVersion: '0.4.0'
      examples:
        - name: SimpleOrder
          headers:
            orderSource: modo-core-sys
          payload:
            order:
              version: v2
              id: ABCD1234
              catalogid: ABC013312312
              quantity: 3
              cost: 9.99
              customer: bob@customer.com
      traits:
        - $ref: '#/components/messageTraits/kafkaHeaders'

  # ─── 스키마 버전 관리 (discriminator + deprecated) ─────────
  schemas:
    newOrder:
      title: New Order message payload
      type: object
      oneOf:
        - $ref: '#/components/schemas/newOrderV1'
        - $ref: '#/components/schemas/newOrderV2'
      discriminator: version
      required: [version, id]
      properties:
        id:
          type: string
        version:
          type: string
          enum: [v1, v2]

    newOrderV1:
      title: New Order message payload (DEPRECATED)
      deprecated: true              # 하위 호환 스키마 deprecated 처리
      type: object
      required: [version, id, itemid, cost]
      properties:
        id: { type: string }
        version:
          type: string
          enum: [v1]
        itemid: { type: string }
        cost: { type: number, format: double }

    newOrderV2:
      title: Order message payload from new systems
      type: object
      required: [version, id, catalogid, quantity, cost, customer]
      properties:
        id: { type: string }
        version:
          type: string
          enum: [v2]
        catalogid: { type: string }
        quantity:
          type: integer
          format: int32
          default: 1
          minimum: 0
        cost: { type: number, format: double }
        discount: { type: number, format: double }
        customer:
          type: string
          format: email

  # ─── Traits (믹스인 재사용) ────────────────────────────────
  operationTraits:
    kafka:
      bindings:
        kafka:
          clientId: { type: string }
          groupId: { type: string }
          bindingVersion: '0.4.0'

  messageTraits:
    kafkaHeaders:
      headers:
        type: object
        properties:
          someCustomHeader:
            description: A common header included for all Kafka messages
            type: string
```

---

## 예제 3: Streetlights Kafka API (공식 표준 예제)

AsyncAPI 공식 레포의 표준 예제로, 스마트 가로등 제어 시스템을 묘사한다. 4개 채널과 4개 오퍼레이션, SCRAM/mTLS 이중 보안, 파라미터화된 토픽 주소가 특징이다. AsyncAPI를 처음 접할 때 구조를 파악하기 좋은 예제다.

**출처**: [asyncapi/spec — streetlights-kafka-asyncapi.yml](https://github.com/asyncapi/spec/blob/master/examples/streetlights-kafka-asyncapi.yml)

### 주목할 패턴

- **파라미터화된 토픽 주소**: `smartylighting.streetlights.1.0.event.{streetlightId}.lighting.measured`처럼 토픽 이름에 변수를 넣어 동적 라우팅을 표현한다.
- **다중 보안**: 같은 클러스터에 SCRAM(비밀번호)과 X509(인증서) 두 가지 접속 방식을 제공한다.
- **send/receive 분리**: `receiveLightMeasurement`(센서 데이터 수신)와 `turnOn`/`turnOff`/`dimLight`(명령 발송)가 명확히 구분된다.

```yaml
asyncapi: 3.1.0
info:
  title: Smartylighting Streetlights API
  version: '1.0.0'
  description: |
    The Smartylighting Streetlights API allows you to remotely
    manage the city lights.
  license:
    name: Apache 2.0
    url: 'https://www.apache.org/licenses/LICENSE-2.0'

defaultContentType: application/json

# ─── 서버 (2개 보안 방식) ────────────────────────────────────
servers:
  scram-connections:
    host: 'test.mykafkacluster.org:18092'
    protocol: kafka-secure
    description: Test broker secured with scramSha256
    security:
      - $ref: '#/components/securitySchemes/saslScram'
    tags:
      - name: 'env:test'
      - name: 'kind:remote'
      - name: 'visibility:private'

  mtls-connections:
    host: 'test.mykafkacluster.org:28092'
    protocol: kafka-secure
    description: Test broker secured with X509
    security:
      - $ref: '#/components/securitySchemes/certs'
    tags:
      - name: 'env:test'
      - name: 'kind:remote'
      - name: 'visibility:private'

# ─── 채널 (4개 Kafka 토픽) ───────────────────────────────────
channels:
  lightingMeasured:
    address: >-
      smartylighting.streetlights.1.0.event.{streetlightId}.lighting.measured
    messages:
      lightMeasured:
        $ref: '#/components/messages/lightMeasured'
    description: >-
      The channel on which measured values may be produced
      and consumed.
    parameters:
      streetlightId:
        $ref: '#/components/parameters/streetlightId'

  lightTurnOn:
    address: >-
      smartylighting.streetlights.1.0.action.{streetlightId}.turn.on
    messages:
      turnOn:
        $ref: '#/components/messages/turnOnOff'
    parameters:
      streetlightId:
        $ref: '#/components/parameters/streetlightId'

  lightTurnOff:
    address: >-
      smartylighting.streetlights.1.0.action.{streetlightId}.turn.off
    messages:
      turnOff:
        $ref: '#/components/messages/turnOnOff'
    parameters:
      streetlightId:
        $ref: '#/components/parameters/streetlightId'

  lightsDim:
    address: >-
      smartylighting.streetlights.1.0.action.{streetlightId}.dim
    messages:
      dimLight:
        $ref: '#/components/messages/dimLight'
    parameters:
      streetlightId:
        $ref: '#/components/parameters/streetlightId'

# ─── 오퍼레이션 ──────────────────────────────────────────────
operations:
  receiveLightMeasurement:
    action: receive
    channel:
      $ref: '#/channels/lightingMeasured'
    summary: >-
      Inform about environmental lighting conditions
      of a particular streetlight.
    traits:
      - $ref: '#/components/operationTraits/kafka'
    messages:
      - $ref: '#/channels/lightingMeasured/messages/lightMeasured'

  turnOn:
    action: send
    channel:
      $ref: '#/channels/lightTurnOn'
    traits:
      - $ref: '#/components/operationTraits/kafka'
    messages:
      - $ref: '#/channels/lightTurnOn/messages/turnOn'

  turnOff:
    action: send
    channel:
      $ref: '#/channels/lightTurnOff'
    traits:
      - $ref: '#/components/operationTraits/kafka'
    messages:
      - $ref: '#/channels/lightTurnOff/messages/turnOff'

  dimLight:
    action: send
    channel:
      $ref: '#/channels/lightsDim'
    traits:
      - $ref: '#/components/operationTraits/kafka'
    messages:
      - $ref: '#/channels/lightsDim/messages/dimLight'

# ─── 컴포넌트 ────────────────────────────────────────────────
components:
  messages:
    lightMeasured:
      name: lightMeasured
      title: Light measured
      summary: >-
        Inform about environmental lighting conditions
        of a particular streetlight.
      contentType: application/json
      traits:
        - $ref: '#/components/messageTraits/commonHeaders'
      payload:
        $ref: '#/components/schemas/lightMeasuredPayload'

    turnOnOff:
      name: turnOnOff
      title: Turn on/off
      summary: >-
        Command a particular streetlight to turn the lights
        on or off.
      traits:
        - $ref: '#/components/messageTraits/commonHeaders'
      payload:
        $ref: '#/components/schemas/turnOnOffPayload'

    dimLight:
      name: dimLight
      title: Dim light
      summary: >-
        Command a particular streetlight to dim the lights.
      traits:
        - $ref: '#/components/messageTraits/commonHeaders'
      payload:
        $ref: '#/components/schemas/dimLightPayload'

  schemas:
    lightMeasuredPayload:
      type: object
      properties:
        lumens:
          type: integer
          minimum: 0
          description: Light intensity measured in lumens.
        sentAt:
          $ref: '#/components/schemas/sentAt'

    turnOnOffPayload:
      type: object
      properties:
        command:
          type: string
          enum: [on, off]
          description: Whether to turn on or off the light.
        sentAt:
          $ref: '#/components/schemas/sentAt'

    dimLightPayload:
      type: object
      properties:
        percentage:
          type: integer
          description: Percentage to which the light should be dimmed to.
          minimum: 0
          maximum: 100
        sentAt:
          $ref: '#/components/schemas/sentAt'

    sentAt:
      type: string
      format: date-time
      description: Date and time when the message was sent.

  securitySchemes:
    saslScram:
      type: scramSha256
      description: >-
        Provide your username and password for
        SASL/SCRAM authentication
    certs:
      type: X509
      description: >-
        Download the certificate files from service provider

  parameters:
    streetlightId:
      description: The ID of the streetlight.

  messageTraits:
    commonHeaders:
      headers:
        type: object
        properties:
          my-app-header:
            type: integer
            minimum: 0
            maximum: 100

  operationTraits:
    kafka:
      bindings:
        kafka:
          clientId:
            type: string
            enum: [my-app-id]
```

---

## 예제별 패턴 비교

| 패턴 | Adeo (예제 1) | Order (예제 2) | Streetlights (예제 3) |
|------|:---:|:---:|:---:|
| Request-Reply | O | - | - |
| Avro 스키마 | O | - | - |
| Correlation ID | O | - | - |
| 다중 환경 서버 | O (3개) | - | - |
| 스키마 버전 관리 | - | O | - |
| Traits 믹스인 | - | O | O |
| 메시지 키 스키마 | - | O | - |
| 파라미터화 토픽 | O | - | O |
| 다중 보안 방식 | - | - | O (SCRAM+mTLS) |
| send/receive 분리 | receive only | receive only | O (둘 다) |

### 실무 적용 가이드

- **Request-Reply 패턴이 필요하면** → Adeo 예제의 `reply` + `address.location` 구조를 참고
- **메시지 스키마 버전 관리가 필요하면** → Order 예제의 `discriminator` + `deprecated` 패턴을 참고
- **다채널 IoT/명령 시스템이면** → Streetlights 예제의 파라미터화 토픽 + send/receive 분리를 참고
- **Avro + Schema Registry를 쓰고 있으면** → Adeo 예제의 `schemaFormat` + `schemaRegistryUrl` 설정을 참고

---

## 참고

- [asyncapi/spec GitHub — 전체 예제 모음](https://github.com/asyncapi/spec/tree/master/examples)
- [Describing Kafka with AsyncAPI (dalelane.co.uk)](https://dalelane.co.uk/blog/?p=4219)
- [Kafka + Avro AsyncAPI 튜토리얼](https://www.asyncapi.com/docs/tutorials/kafka/configure-kafka-avro)
