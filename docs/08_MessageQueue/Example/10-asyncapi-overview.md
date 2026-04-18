# AsyncAPI 개요

## AsyncAPI란?

OpenAPI가 REST API의 요청/응답 패턴을 기술하는 것처럼, AsyncAPI는 Kafka, AMQP, MQTT, WebSocket 등 **비동기 프로토콜 기반의 메시지 API를 기술하는 표준 명세**다. 이벤트 드리븐 아키텍처에서 "어떤 토픽에, 어떤 메시지가, 어떤 스키마로 오가는지"를 하나의 문서로 정의한다.

현재 최신 버전은 **3.1.0**이며, 3.0.0에서 채널과 오퍼레이션의 분리라는 핵심 구조 변경이 이루어졌다.

---

## v3의 핵심 변경점: 채널과 오퍼레이션 분리

v2까지는 `publish`/`subscribe`가 채널 안에 내장되어 있었다. v3에서는 **채널은 토픽과 메시지 구조만 담고, 오퍼레이션이 채널을 외부에서 참조**하는 구조로 분리됐다.

```yaml
# v2 (채널 안에 동작이 묶여 있음)
channels:
  orders:
    publish:
      message: ...
    subscribe:
      message: ...

# v3 (채널과 오퍼레이션이 분리됨)
channels:
  ordersTopic:
    address: shop.orders
    messages:
      newOrder:
        $ref: '#/components/messages/newOrder'

operations:
  publishOrder:
    action: send
    channel:
      $ref: '#/channels/ordersTopic'
  consumeOrder:
    action: receive
    channel:
      $ref: '#/channels/ordersTopic'
```

이 분리 덕분에 하나의 채널을 여러 오퍼레이션이 재사용할 수 있다. 실제 EDA에서는 하나의 토픽에 여러 서비스가 다른 역할로 참여하므로 이 구조가 현실에 더 가깝다.

---

## AsyncAPI 문서 구조

```yaml
asyncapi: 3.1.0           # 스펙 버전
info:                       # 메타데이터 (제목, 버전, 설명)
servers:                    # 브로커 접속 정보 (host, protocol, security)
channels:                   # 토픽/큐 정의 (address + messages)
operations:                 # 동작 정의 (send/receive + 채널 참조)
components:                 # 재사용 가능한 스키마, 메시지, 보안, traits
```

### 각 섹션 역할

| 섹션 | OpenAPI 대응 | 역할 |
|------|-------------|------|
| `servers` | `servers` | 브로커 접속 정보 + 프로토콜 + 보안 |
| `channels` | `paths` | 토픽 주소 + 메시지 구조 정의 |
| `operations` | HTTP 메서드 | send/receive 동작 + 채널 참조 |
| `components.messages` | - | 메시지 정의 (헤더 + 페이로드) |
| `components.schemas` | `components.schemas` | 데이터 모델 (JSON Schema / Avro) |
| `components.securitySchemes` | `securitySchemes` | 인증 방식 (SASL, mTLS 등) |
| `components.operationTraits` | - | 오퍼레이션 공통 설정 믹스인 |
| `components.messageTraits` | - | 메시지 공통 설정 믹스인 |

---

## OpenAPI vs AsyncAPI 비교

| 항목 | OpenAPI 3.x | AsyncAPI 3.x |
|------|-------------|--------------|
| **목적** | REST/HTTP API (요청-응답) | 이벤트 드리븐 / 메시징 API |
| **경로 개념** | `paths` (URL 경로) | `channels` (토픽/큐) |
| **동작 개념** | HTTP 메서드 (GET, POST...) | `operations` — `send` / `receive` |
| **동작 분리** | 경로 안에 내장 | 채널과 오퍼레이션 **완전 분리** (v3) |
| **프로토콜** | HTTP/HTTPS 전용 | Kafka, AMQP, MQTT, WebSocket 등 14종+ |
| **서버 정의** | host + scheme | host + `protocol` + `protocolVersion` |
| **스키마** | JSON Schema만 | JSON Schema + **Avro** + Protobuf + RAML |
| **메시지 헤더** | HTTP 헤더 | 프로토콜별 헤더 + 메시지 헤더 분리 |
| **Bindings** | 없음 | 프로토콜별 바인딩 (`kafka:`, `amqp:` 등) |
| **Correlation ID** | 없음 | `correlationId` + `location` (JSONPath) |
| **Traits** | 없음 | `operationTraits` / `messageTraits` |

AsyncAPI만의 고유 기능인 **Bindings**와 **Traits**가 핵심이다. Bindings는 Kafka의 파티션 수, replicas, topicConfiguration 같은 브로커 특화 설정을 명세에 포함시키고, Traits는 여러 오퍼레이션/메시지에 공통으로 적용할 설정을 믹스인 방식으로 재사용한다.

---

## 툴링 생태계

### CLI

```bash
# 설치
npm install -g @asyncapi/cli

# 유효성 검사
asyncapi validate asyncapi.yaml

# HTML 문서 생성
asyncapi generate fromTemplate asyncapi.yaml @asyncapi/html-template -o ./output

# Spring Boot 코드 생성
asyncapi generate fromTemplate asyncapi.yaml @asyncapi/java-spring-template -o ./output

# TypeScript 모델 생성
asyncapi generate models typescript asyncapi.yaml -o ./models
```

### 코드 생성 (AsyncAPI -> 코드)

| 도구 | 언어 | 설명 |
|------|------|------|
| **AsyncAPI Generator** | 다중 언어 | 공식 제너레이터. 템플릿 기반 (Spring, Node.js, Python 등) |
| **AsyncAPI Modelina** | 다중 언어 | 페이로드 모델/클래스 전용 생성 |
| **asyncapi-codegen** | Go | Go 보일러플레이트 생성 |

### 역방향 생성 (코드 -> AsyncAPI)

| 도구 | 언어 | 설명 |
|------|------|------|
| **Springwolf** | Java (Spring) | Spring Boot 어노테이션에서 AsyncAPI 문서 자동 생성 |
| **nestjs-asyncapi** | TypeScript (NestJS) | 데코레이터 기반 자동 생성 |
| **FastStream** | Python | 이벤트 스트림 프레임워크, 문서 자동 생성 내장 |
| **go-asyncapi** | Go | Go 구조체 반영(reflection)으로 스키마 생성 |

Springwolf는 Springdoc(OpenAPI)의 비동기 버전이라고 보면 된다. `@KafkaListener` 등의 어노테이션을 읽어서 AsyncAPI 명세를 자동으로 만들어준다.

### 문서화 및 시각화

| 도구 | 설명 |
|------|------|
| **AsyncAPI Studio** | 브라우저 기반 비주얼 에디터 + 미리보기 (studio.asyncapi.com) |
| **Bump.sh** | 문서 생성 + 변경 로그 자동화 |
| **Microcks** | Mock 서버 + 테스트 플랫폼 (Kafka 포함) |

### IDE 플러그인

| IDE | 플러그인 |
|-----|---------|
| VS Code | asyncapi-preview — 실시간 미리보기 |
| IntelliJ IDEA | jAsyncAPI Plugin — 자동완성 + 유효성 검사 |

---

## 실무 도입 판단 기준

AsyncAPI 도입이 효과적인 경우:

- **팀 간 이벤트 계약이 필요할 때** — Producer와 Consumer 팀이 다르면 명세가 곧 계약서 역할을 한다
- **이벤트 스키마가 자주 변경될 때** — 버전 관리(discriminator, deprecated)와 호환성 추적이 명세 안에서 가능하다
- **Avro 스키마를 이미 사용 중일 때** — `schemaFormat: application/vnd.apache.avro`로 기존 `.avsc` 파일을 직접 참조할 수 있다
- **문서화가 목적일 때** — 코드 생성보다 문서화와 검증이 현재 가장 안정적인 사용 사례다

반대로 단일 팀이 Producer/Consumer를 모두 관리하고, 스키마가 안정적이라면 도입 비용 대비 이점이 크지 않을 수 있다.

---

## 참고

- [AsyncAPI 3.1.0 공식 명세](https://www.asyncapi.com/docs/reference/specification/v3.1.0)
- [AsyncAPI 3.0 릴리즈 노트](https://www.asyncapi.com/blog/release-notes-3.0.0)
- [Coming from OpenAPI — 공식 문서](https://www.asyncapi.com/docs/tutorials/getting-started/coming-from-openapi)
- [AsyncAPI Tools 공식 페이지](https://www.asyncapi.com/tools)
- [AsyncAPI Studio](https://studio.asyncapi.com)
- [Springwolf](https://www.springwolf.dev)
