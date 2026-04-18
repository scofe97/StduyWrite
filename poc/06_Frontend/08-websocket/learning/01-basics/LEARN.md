# LEARN: WebSocket 기초

## 학습 목표
HTTP와 WebSocket의 근본적인 차이를 이해하고, 핸드셰이크 과정과 Full-Duplex 통신의 원리를 면접에서 설명할 수 있다.

---

## A1. HTTP vs WebSocket 비교

### HTTP (요청-응답 모델)

HTTP는 클라이언트가 요청을 보내면 서버가 응답하고 연결이 종료되는 **단방향 통신** 프로토콜입니다. 매 요청마다 헤더(쿠키, 인증 정보 등)를 포함한 수백 바이트의 오버헤드가 발생합니다.

**적합한 경우:**
- 일회성 데이터 조회 (사용자 정보, 상품 목록)
- 폼 제출, 파일 업로드
- REST API 호출

### WebSocket (양방향 지속 연결)

WebSocket은 최초 HTTP 핸드셰이크 후 프로토콜을 **업그레이드**하여 지속적인 양방향 연결을 유지합니다. 서버가 클라이언트에게 먼저 데이터를 보낼 수 있으며(서버 푸시), 메시지당 오버헤드가 2~14바이트로 매우 작습니다.

**적합한 경우:**
- 실시간 채팅
- 주식/암호화폐 시세
- 실시간 알림, 로그 스트리밍
- 멀티플레이어 게임

### 비교표

| 특성 | HTTP | WebSocket |
|------|------|-----------|
| 연결 방식 | 요청마다 새 연결 (Stateless) | 한 번 연결 후 지속 (Stateful) |
| 데이터 전송 | 클라이언트 → 서버 (단방향) | 양방향 동시 전송 (Full-Duplex) |
| 오버헤드 | 매 요청마다 수백 바이트 헤더 | 초기 핸드셰이크 후 2~14바이트 |
| 서버 푸시 | 불가능 (SSE로 우회) | 가능 |
| 적합한 케이스 | 일회성 요청, REST API | 실시간 양방향 통신 |

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    rect rgb(255, 230, 230)
        Note over C,S: HTTP - 매번 새 연결
        C->>S: GET /api/data (헤더 포함)
        S-->>C: 200 OK + 데이터
        Note over C,S: 연결 종료
    end

    rect rgb(230, 255, 230)
        Note over C,S: WebSocket - 지속 연결
        C->>S: 핸드셰이크 (HTTP 업그레이드)
        S-->>C: 101 Switching Protocols
        Note over C,S: 연결 유지, 양방향 통신
        C->>S: 메시지 A
        S-->>C: 메시지 B
        S-->>C: 메시지 C (서버가 먼저!)
    end
```

---

## A2. 핸드셰이크 과정

### 프로토콜 업그레이드란?

WebSocket 연결은 **일반 HTTP 요청으로 시작**한 뒤, 서버가 이를 WebSocket 프로토콜로 "업그레이드"합니다. 이 방식 덕분에 기존 HTTP 인프라(80/443 포트, 프록시, 로드밸런서)와 호환됩니다.

### 핸드셰이크 흐름

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    C->>S: HTTP 업그레이드 요청<br/>Upgrade: websocket<br/>Sec-WebSocket-Key: dGhlc2FtcGxl...
    Note over S: Key 검증 및<br/>Accept 값 계산
    S-->>C: HTTP/1.1 101 Switching Protocols<br/>Sec-WebSocket-Accept: s3pPLMBi...
    Note over C,S: WebSocket 프로토콜로 전환!
    C->>S: WebSocket 프레임
    S-->>C: WebSocket 프레임
```

1. **클라이언트**: `Upgrade: websocket` 헤더와 랜덤 키(`Sec-WebSocket-Key`)를 포함한 HTTP GET 요청
2. **서버**: 키를 검증하고 `101 Switching Protocols` 응답과 함께 `Sec-WebSocket-Accept` 반환
3. **결과**: HTTP 연결이 WebSocket 연결로 업그레이드됨

### 핸드셰이크 요청 헤더

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
Origin: https://example.com
```

| 헤더 | 필수 | 설명 |
|------|:----:|------|
| `Upgrade: websocket` | O | WebSocket으로 프로토콜 변경 요청 |
| `Connection: Upgrade` | O | 연결 업그레이드 의사 표시 |
| `Sec-WebSocket-Key` | O | 16바이트 랜덤 값의 Base64 인코딩, 서버 응답 검증용 |
| `Sec-WebSocket-Version` | O | 프로토콜 버전 (현재 13) |
| `Origin` | △ | CORS 검증용, 브라우저가 자동 추가 |

**서버 응답:**
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### 101 Switching Protocols의 의미

**HTTP 상태 코드 101은 "프로토콜 전환 중"을 의미합니다.** 이 응답을 받으면 클라이언트와 서버 간의 통신 프로토콜이 HTTP에서 WebSocket으로 변경됩니다.

| 상태 코드 | 의미 | 설명 |
|:---------:|------|------|
| 101 | Switching Protocols | 클라이언트가 요청한 프로토콜로 전환 성공 |
| 200 | OK | 일반 HTTP 요청 성공 (WebSocket 업그레이드 실패) |
| 400 | Bad Request | 잘못된 핸드셰이크 요청 |
| 403 | Forbidden | Origin 검증 실패 (CORS) |
| 426 | Upgrade Required | 프로토콜 업그레이드 필요 |

**101 응답 이후:**
- 동일한 TCP 연결이 유지됨
- HTTP 프로토콜 → WebSocket 프로토콜로 전환
- 이후 모든 통신은 WebSocket 프레임 형식으로 진행

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    Note over C,S: TCP 연결 수립

    rect rgb(230, 230, 255)
        Note over C,S: HTTP 프로토콜
        C->>S: GET /chat HTTP/1.1<br/>Upgrade: websocket
        S-->>C: HTTP/1.1 101 Switching Protocols
    end

    rect rgb(230, 255, 230)
        Note over C,S: WebSocket 프로토콜 (같은 TCP 연결)
        C->>S: WebSocket 프레임
        S-->>C: WebSocket 프레임
    end
```

### Sec-WebSocket-Accept 상세 설명

**Sec-WebSocket-Accept는 서버가 WebSocket 핸드셰이크를 올바르게 이해했음을 증명하는 값입니다.** 클라이언트는 이 값을 검증하여 서버가 진짜 WebSocket을 지원하는지 확인합니다.

#### 왜 필요한가?

1. **잘못된 서버 방지**: 일반 HTTP 서버가 WebSocket 요청을 잘못 처리하는 것을 방지
2. **캐싱 프록시 우회**: 중간 프록시가 WebSocket 요청을 캐시하지 않도록 함
3. **보안 검증**: 서버가 실제로 WebSocket 프로토콜을 이해하는지 확인

#### 계산 방법

```
Sec-WebSocket-Accept = Base64(SHA-1(Sec-WebSocket-Key + GUID))
```

**GUID (Magic String)**: `258EAFA5-E914-47DA-95CA-C5AB0DC85B11` (RFC 6455에서 정의된 고정 값)

#### 계산 예시

```typescript
// 클라이언트가 보낸 키
const clientKey = "dGhlIHNhbXBsZSBub25jZQ==";

// 서버의 계산 과정
const GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11";
const combined = clientKey + GUID;
// → "dGhlIHNhbXBsZSBub25jZQ==258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

const sha1Hash = SHA1(combined);
// → 바이너리 해시값

const acceptValue = Base64Encode(sha1Hash);
// → "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
```

#### 검증 흐름

```mermaid
flowchart TD
    subgraph Client["클라이언트"]
        C1["16바이트 랜덤 값 생성"]
        C2["Base64 인코딩"]
        C3["Sec-WebSocket-Key로 전송"]
        C4["응답의 Accept 값 검증"]
    end

    subgraph Server["서버"]
        S1["Key 수신"]
        S2["Key + GUID 결합"]
        S3["SHA-1 해시"]
        S4["Base64 인코딩"]
        S5["Sec-WebSocket-Accept로 응답"]
    end

    C1 --> C2 --> C3 --> S1
    S1 --> S2 --> S3 --> S4 --> S5
    S5 --> C4

    C4 -->|"일치"| SUCCESS["WebSocket 연결 성공"]
    C4 -->|"불일치"| FAIL["연결 거부"]
```

#### 실제 구현 (Go 예시)

```go
package main

import (
	"crypto/sha1"
	"encoding/base64"
	"fmt"
)

const GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

func calculateAcceptValue(key string) string {
	// 1. Key + GUID 결합
	combined := key + GUID

	// 2. SHA-1 해시 계산
	hash := sha1.Sum([]byte(combined))

	// 3. Base64 인코딩
	return base64.StdEncoding.EncodeToString(hash[:])
}

func main() {
	clientKey := "dGhlIHNhbXBsZSBub25jZQ=="
	acceptValue := calculateAcceptValue(clientKey)
	fmt.Println(acceptValue) // "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
}
```

**핵심 포인트:**
- `sha1.Sum()`: 20바이트 해시 배열 반환 (`[20]byte`)
- `hash[:]`: 배열을 슬라이스로 변환 (Base64 인코딩에 필요)
- `base64.StdEncoding`: 표준 Base64 인코딩 사용

#### 핸드셰이크 실패 시나리오

| 상황 | 결과 |
|------|------|
| Accept 값이 없음 | 클라이언트가 연결 거부 |
| Accept 값이 틀림 | 클라이언트가 연결 거부 |
| 101이 아닌 응답 | WebSocket 업그레이드 실패 |

---

## A3. 양방향 통신 (Full-Duplex)

### 왜 중요한가?

**Full-Duplex(전이중)는 양쪽이 동시에 데이터를 보내고 받을 수 있는 통신 방식입니다.** 전화 통화처럼 두 사람이 동시에 말할 수 있는 것과 같습니다. 이는 실시간 애플리케이션에서 필수적인 특성입니다.

```mermaid
flowchart LR
    subgraph HalfDuplex["Half-Duplex (HTTP)"]
        H1["클라이언트"] -->|"요청"| H2["서버"]
        H2 -->|"응답"| H1
        Note1["번갈아가며 통신"]
    end

    subgraph FullDuplex["Full-Duplex (WebSocket)"]
        F1["클라이언트"] -->|"동시 전송"| F2["서버"]
        F2 -->|"동시 전송"| F1
        Note2["양방향 동시 통신"]
    end
```

### HTTP의 한계 (Long Polling)

HTTP로 실시간성을 구현하려면 **Long Polling**을 사용해야 합니다:

1. 클라이언트가 요청을 보내고 서버가 응답을 보류
2. 새 데이터가 생기면 서버가 응답
3. 클라이언트가 즉시 다시 요청

**문제점:**
- 매 요청마다 HTTP 헤더 오버헤드 발생
- 서버가 "먼저" 데이터를 보내려면 클라이언트 요청이 필요
- 연결당 리소스 소모가 큼

### WebSocket의 장점

#### 1. 서버 푸시 (Server Push)

**HTTP는 "요청-응답" 모델입니다.** 클라이언트가 먼저 요청해야만 서버가 응답할 수 있습니다. 서버에 새 데이터가 생겨도 클라이언트가 물어보기 전까지는 보낼 수 없습니다.

**WebSocket은 연결이 수립된 후 양쪽이 "대등한 관계"가 됩니다.** 서버도 클라이언트처럼 언제든 먼저 메시지를 보낼 수 있습니다.

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    rect rgb(255, 230, 230)
        Note over C,S: HTTP - 서버가 먼저 못 보냄
        C->>S: "새 데이터 있어?"
        S-->>C: "없어"
        Note over S: 새 데이터 발생!
        Note over S: 보내고 싶지만...<br/>클라이언트 요청이 없음
        C->>S: "새 데이터 있어?"
        S-->>C: "있어! 여기"
    end

    rect rgb(230, 255, 230)
        Note over C,S: WebSocket - 서버가 먼저 보냄
        C->>S: WebSocket 연결
        S-->>C: 연결 OK
        Note over S: 새 데이터 발생!
        S-->>C: "새 데이터야!" (즉시 전송)
    end
```

**왜 가능한가?**
- HTTP: 반이중(Half-Duplex) 통신. 한 번에 한 방향만 데이터 전송
- WebSocket: 전이중(Full-Duplex) 통신. TCP 연결 위에서 양방향 독립 채널 유지
- WebSocket 연결 후에는 HTTP의 "요청-응답" 규칙이 사라지고, 양쪽 모두 자유롭게 메시지 전송 가능

#### 로우레벨에서 Full-Duplex가 가능한 이유

**핵심 질문: TCP는 원래 Full-Duplex인데, 왜 HTTP는 Half-Duplex인가?**

TCP 자체는 양방향 동시 통신을 지원합니다. 하나의 TCP 연결은 두 개의 독립적인 바이트 스트림(클라이언트→서버, 서버→클라이언트)을 가지며, 이 스트림들은 완전히 독립적으로 동작합니다.

```mermaid
flowchart LR
    subgraph TCP["TCP 연결 (Full-Duplex 지원)"]
        direction LR
        C["클라이언트"]
        S["서버"]
        C -->|"송신 버퍼 → 수신 버퍼"| S
        S -->|"송신 버퍼 → 수신 버퍼"| C
    end
```

**그렇다면 문제는 무엇인가?**

문제는 TCP 위에서 동작하는 **HTTP 프로토콜의 규칙**입니다.

```mermaid
flowchart TB
    subgraph Layer["프로토콜 계층"]
        HTTP["HTTP 프로토콜<br/>(요청-응답 규칙 강제)"]
        TCP["TCP 소켓<br/>(Full-Duplex 지원)"]
        HTTP --> TCP
    end

    Rule["HTTP 규칙:<br/>1. 클라이언트가 요청을 보내야 함<br/>2. 서버는 요청에 대해서만 응답<br/>3. 응답 후 다음 요청 대기"]
    Rule -.->|"제약"| HTTP
```

**HTTP의 Half-Duplex 제약:**

| 제약 | 설명 |
|------|------|
| 요청 필수 | 서버는 클라이언트 요청 없이 데이터를 보낼 수 없음 |
| 순차 처리 | 요청 → 응답 → 요청 → 응답 순서 강제 (HTTP/1.1 파이프라이닝은 거의 사용 안 됨) |
| 응답 1회 | 하나의 요청에 하나의 응답만 가능 |

**그럼에도 HTTP가 요청-응답 모델을 채택한 이유:**

HTTP는 1991년 **문서(HTML) 전송**을 위해 설계되었습니다. 당시 웹은 "링크 클릭 → 페이지 로드"가 전부였고, 실시간 통신은 고려 대상이 아니었습니다.

| 이유 | 설명 |
|------|------|
| **단순성** | 구현이 쉬움. 요청 보내고 응답 받으면 끝. 상태 관리 불필요 |
| **무상태(Stateless)** | 서버가 클라이언트 상태를 기억하지 않아 **수평 확장**이 쉬움 |
| **캐싱 용이** | 같은 요청 = 같은 응답. 프록시/CDN에서 캐싱 가능 |
| **신뢰성** | 요청-응답 쌍이 명확해서 "내 요청이 처리됐는지" 확인 쉬움 |
| **방화벽 친화적** | 클라이언트가 먼저 연결하므로 보안 정책 적용이 단순 |

```mermaid
flowchart LR
    subgraph 1991["1991년 웹"]
        User["사용자"] -->|"링크 클릭"| Server["서버"]
        Server -->|"HTML 문서"| User
    end

    subgraph Today["오늘날 웹"]
        User2["사용자"] <-->|"실시간 채팅<br/>주식 시세<br/>알림"| Server2["서버"]
    end

    1991 -.->|"요구사항 변화"| Today
```

**요약:**
> HTTP의 요청-응답 모델은 "문서 전송"에 최적화된 설계입니다. 단순하고, 확장 가능하고, 캐싱이 쉽습니다. 하지만 실시간 양방향 통신이 필요한 현대 웹에서는 한계가 있어 WebSocket이 등장했습니다.

**WebSocket이 Full-Duplex를 가능하게 하는 방법:**

101 Switching Protocols 응답 이후, **동일한 TCP 소켓**에서 HTTP 프로토콜 규칙이 제거됩니다.

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    Note over C,S: TCP 연결 수립 (3-way handshake)

    rect rgb(255, 230, 230)
        Note over C,S: HTTP 모드 - 프로토콜 규칙 적용
        C->>S: HTTP 요청
        Note over S: 서버는 요청에만 응답 가능<br/>(HTTP 규칙)
        S-->>C: HTTP 응답 (101 Switching Protocols)
    end

    rect rgb(230, 255, 230)
        Note over C,S: WebSocket 모드 - 규칙 제거
        Note over C,S: 같은 TCP 소켓, 다른 프로토콜!
        par 동시 전송 가능
            C->>S: 메시지 A
        and
            S->>C: 메시지 B
        end
    end
```

**로우레벨에서 실제로 무엇이 바뀌는가?**

| 계층 | HTTP 모드 | WebSocket 모드 |
|------|----------|---------------|
| **TCP 소켓** | 변화 없음 (그대로 유지) | 변화 없음 |
| **프로토콜 파서** | HTTP 요청/응답 파싱 | WebSocket 프레임 파싱 |
| **전송 규칙** | 요청-응답 순서 강제 | 양쪽 자유롭게 전송 |
| **메시지 경계** | 헤더로 Content-Length 명시 | 프레임 길이 필드 사용 |

**핵심 포인트:**

1. **TCP 연결 자체는 변하지 않습니다.** 같은 파일 디스크립터(fd), 같은 소켓입니다.
2. **변하는 것은 "프로토콜 해석 방식"입니다.** HTTP 파서 → WebSocket 프레임 파서로 전환됩니다.
3. **HTTP의 "요청해야 응답" 규칙이 사라집니다.** WebSocket에는 그런 규칙이 없습니다.

```go
// 개념적 의사 코드
// HTTP 모드
func httpMode(conn net.Conn) {
    for {
        request := readHTTPRequest(conn)   // 요청 대기 (블로킹)
        response := handleRequest(request)
        writeHTTPResponse(conn, response)  // 응답 전송
        // 서버가 먼저 보내는 것 불가능!
    }
}

// WebSocket 모드 - 송신/수신이 독립적
func websocketMode(conn net.Conn) {
    // 수신 고루틴
    go func() {
        for {
            frame := readWebSocketFrame(conn)
            handleMessage(frame)
        }
    }()

    // 송신 - 언제든 가능!
    go func() {
        for msg := range outgoingMessages {
            writeWebSocketFrame(conn, msg)  // 요청 없이도 전송 가능!
        }
    }()
}
```

**요약:**

> TCP는 원래 Full-Duplex입니다. HTTP가 프로토콜 규칙으로 Half-Duplex를 강제했고, WebSocket은 핸드셰이크 후 그 규칙을 제거함으로써 TCP 본연의 Full-Duplex 능력을 활용합니다.

#### 리눅스 소켓 레벨 심층 분석

**핵심 질문: 둘 다 같은 TCP 소켓인데, 왜 HTTP가 대규모 환경에서 더 효율적인가?**

이 질문에 대한 상세한 답변은 별도 문서에서 다룹니다:

> **심화 학습**: [Go 시스템 프로그래밍 - HTTP vs WebSocket 소켓 레벨 분석](../../../02-go/11-system-programming/03-network-io/step4_http_vs_websocket/LEARN.md)

**핵심 요약:**
- 커널은 HTTP인지 WebSocket인지 모릅니다 (동일한 TCP 소켓)
- 차이는 유저 공간에서의 **프로토콜 해석 방식**과 **fd 수명 관리**
- HTTP: fd를 빠르게 순환 → 적은 리소스로 대량 처리
- WebSocket: fd 영구 점유 → 10만 연결 = 10만 fd 필요

#### 2. 낮은 오버헤드

**HTTP 요청마다 발생하는 오버헤드:**

```http
GET /api/messages HTTP/1.1
Host: example.com
Connection: keep-alive
Accept: application/json
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8
Accept-Encoding: gzip, deflate, br
Cookie: session=abc123; user=kim; preferences=...
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
Cache-Control: no-cache
```

**일반적인 HTTP 헤더 크기: 500~2000 바이트** (쿠키, 인증 토큰 포함 시 더 증가)

**WebSocket 프레임 구조:**

WebSocket 메시지는 "프레임"이라는 단위로 전송됩니다. HTTP 헤더와 달리 **바이너리 형식**이며 매우 작습니다.

```
┌─────────────────────────────────────────────────────────────┐
│                    WebSocket 프레임                          │
├──────────┬──────────┬──────────────┬───────────────────────┤
│  1바이트  │  1바이트  │  0/2/8바이트  │      N바이트          │
├──────────┼──────────┼──────────────┼───────────────────────┤
│  FIN +   │  MASK +  │   확장 길이   │     실제 데이터        │
│  Opcode  │  길이    │   (선택적)    │     (Payload)         │
└──────────┴──────────┴──────────────┴───────────────────────┘
```

**각 필드 설명:**

| 필드 | 크기 | 설명 |
|------|:----:|------|
| **FIN** | 1비트 | 마지막 프레임인지 여부 (1=마지막) |
| **Opcode** | 4비트 | 메시지 종류 (1=텍스트, 2=바이너리, 8=종료, 9=핑, 10=퐁) |
| **MASK** | 1비트 | 마스킹 여부 (클라이언트→서버는 반드시 1) |
| **Payload Length** | 7비트 | 데이터 길이 (0~125: 그대로, 126: 2바이트 추가, 127: 8바이트 추가) |
| **Masking Key** | 0 또는 4바이트 | 마스킹 키 (MASK=1일 때만) |
| **Payload Data** | N바이트 | 실제 전송할 데이터 |

**실제 예시: "Hi" 전송**

```
클라이언트가 "Hi" (2바이트)를 서버로 전송:

┌──────────┬──────────┬──────────────┬──────────┐
│ 10000001 │ 10000010 │  마스킹 키    │  Hi      │
│ (0x81)   │ (0x82)   │  (4바이트)    │ (마스킹) │
└──────────┴──────────┴──────────────┴──────────┘
     │          │
     │          └── MASK=1, 길이=2
     └── FIN=1, Opcode=1(텍스트)

총 헤더: 2 + 4(마스킹 키) = 6바이트
```

```
서버가 "Hi" (2바이트)를 클라이언트로 전송:

┌──────────┬──────────┬──────────┐
│ 10000001 │ 00000010 │    Hi    │
│ (0x81)   │ (0x02)   │ (평문)   │
└──────────┴──────────┴──────────┘
     │          │
     │          └── MASK=0, 길이=2
     └── FIN=1, Opcode=1(텍스트)

총 헤더: 2바이트 (마스킹 없음)
```

**왜 클라이언트만 마스킹하는가?**
- 프록시 캐시 오염 공격 방지
- 클라이언트가 악의적 데이터를 보내 중간 프록시를 속이는 것을 막음

| 페이로드 크기 | WebSocket 헤더 크기 |
|:------------:|:------------------:|
| 0~125 바이트 | **2 바이트** |
| 126~65535 바이트 | **4 바이트** |
| 65536+ 바이트 | **10 바이트** |
| 클라이언트→서버 (마스킹) | **+4 바이트** |

**비교:**

| 프로토콜 | 메시지당 오버헤드 | 1000개 메시지 전송 시 |
|---------|:----------------:|:-------------------:|
| HTTP | ~800 바이트 | ~800 KB |
| WebSocket | 2~14 바이트 | ~2~14 KB |

**왜 이렇게 작은가?**
- 핸드셰이크는 최초 1회만 (HTTP 헤더는 그때만)
- 이후 메시지는 WebSocket 프레임 헤더만 사용
- 쿠키, 인증 토큰 등 반복 전송 불필요 (연결 시 이미 인증됨)

#### 3. 낮은 지연 (Low Latency)

**HTTP의 지연 요소:**
1. TCP 3-way 핸드셰이크 (새 연결마다)
2. TLS 핸드셰이크 (HTTPS의 경우)
3. HTTP 요청/응답 왕복
4. Keep-Alive여도 요청 대기 필요

**WebSocket의 지연:**
1. 최초 연결 시에만 핸드셰이크
2. 이후 메시지는 **즉시 전송** (추가 핸드셰이크 없음)

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    rect rgb(255, 230, 230)
        Note over C,S: HTTP - 매번 오버헤드
        C->>S: TCP SYN
        S-->>C: TCP SYN-ACK
        C->>S: TCP ACK + HTTP 요청
        S-->>C: HTTP 응답
        Note over C,S: 왕복 2~3회
    end

    rect rgb(230, 255, 230)
        Note over C,S: WebSocket - 최초 1회 후 즉시
        C->>S: 핸드셰이크 (1회)
        S-->>C: 101 OK
        Note over C,S: 이후...
        C->>S: 메시지 (즉시)
        S-->>C: 메시지 (즉시)
        C->>S: 메시지 (즉시)
    end
```

#### 4. 효율적 자원 사용

**HTTP (Long Polling)의 자원 소모:**
- 매 요청마다 새 HTTP 파싱
- 요청 대기 중에도 서버 스레드/메모리 점유
- 연결 풀 관리 복잡성

**WebSocket의 자원 효율:**
- 하나의 TCP 연결로 무제한 메시지 교환
- 연결당 메모리: 수 KB (HTTP 요청 컨텍스트보다 작음)
- 이벤트 기반 처리로 대기 중 자원 최소화

| 비교 항목 | HTTP Long Polling | WebSocket |
|----------|:-----------------:|:---------:|
| 10,000명 동시 접속 | ~10,000 요청 처리 필요 | ~10,000 연결 유지 |
| 서버 메모리 | 높음 (요청 컨텍스트) | 낮음 (연결 상태만) |
| CPU 사용 | 높음 (매번 파싱) | 낮음 (프레임만 파싱) |
| 네트워크 대역폭 | 높음 (헤더 반복) | 낮음 (최소 헤더) |

---

## A4. TCP 연결과 소켓 관리

### 하나의 포트에 여러 연결이 가능한 이유

**"서버 주소가 하나인데 어떻게 여러 클라이언트를 구분하지?"**

**TCP 연결은 4가지 정보(4-Tuple)로 구분됩니다:**

```
연결 = (서버IP, 서버Port, 클라이언트IP, 클라이언트Port)

서버: 192.168.1.100:8080 에서 listen

연결 1: (192.168.1.100:8080, 10.0.0.50:52341)  ← 클라이언트 A
연결 2: (192.168.1.100:8080, 10.0.0.51:49872)  ← 클라이언트 B
연결 3: (192.168.1.100:8080, 10.0.0.50:52342)  ← 클라이언트 A의 다른 탭

→ 서버 주소는 같지만, 클라이언트 주소가 다르므로 구분 가능
```

---

### 연결 수립 과정

**서버가 클라이언트 연결을 받아들이는 과정은 다음과 같습니다:**

1. **서버 시작**: 서버가 특정 포트(예: 8080)에서 `Listen Socket`을 생성하고 연결 요청을 대기합니다.
2. **클라이언트 연결 요청**: 클라이언트가 서버에 연결을 시도하면, 클라이언트의 OS가 임의의 포트 번호(예: 52341)를 할당합니다.
3. **Accept()**: 서버가 연결 요청을 수락하면 `Accept()` 함수가 호출되어 **새로운 Connection Socket**이 생성됩니다. 이 소켓은 해당 클라이언트 전용입니다.
4. **데이터 통신**: 이후 모든 데이터 송수신은 이 Connection Socket을 통해 이루어집니다.

**중요한 점**: 서버가 메시지를 받을 때, 이미 **어떤 소켓에서 읽었는지** 알고 있으므로 "누가 보냈는지" 별도로 추적할 필요가 없습니다.

```mermaid
sequenceDiagram
    participant S as 서버<br/>192.168.1.100:8080
    participant A as 클라이언트 A<br/>10.0.0.50
    participant B as 클라이언트 B<br/>10.0.0.51

    Note over S: Listen Socket 생성<br/>포트 8080에서 대기 중

    A->>S: 연결 요청 (from 10.0.0.50:52341)
    Note over S: Accept() → Connection Socket 1 생성
    S-->>A: 연결 수락

    B->>S: 연결 요청 (from 10.0.0.51:49872)
    Note over S: Accept() → Connection Socket 2 생성
    S-->>B: 연결 수락

    Note over S: 이제 서버는 2개의 소켓 보유<br/>Socket 1: A와 통신<br/>Socket 2: B와 통신

    A->>S: 메시지 "Hello" (Socket 1로 도착)
    Note over S: Socket 1에서 읽음<br/>→ A가 보낸 것임을 앎
    S-->>A: 응답 (Socket 1로 전송)

    B->>S: 메시지 "Hi" (Socket 2로 도착)
    Note over S: Socket 2에서 읽음<br/>→ B가 보낸 것임을 앎
    S-->>B: 응답 (Socket 2로 전송)
```

---

### 서버 내부 소켓 구조

**서버 내부에는 두 종류의 소켓이 존재합니다:**

**1️⃣ Listen Socket (1개)**
- 서버 시작 시 생성되며, 특정 포트에서 새로운 연결 요청만 대기합니다.
- 실제 데이터 통신은 하지 않습니다. 오직 "새 손님이 왔어요"를 감지하는 역할입니다.
- `Accept()` 함수를 호출하면 Connection Socket을 생성하고 반환합니다.

**2️⃣ Connection Sockets (클라이언트 수만큼)**
- 클라이언트가 연결될 때마다 하나씩 생성됩니다.
- 각 소켓은 **Remote 주소**(클라이언트 IP:Port)를 기억하고 있어 어떤 클라이언트와 연결됐는지 식별합니다.
- 실제 `Read()`, `Write()` 데이터 통신은 이 소켓을 통해 이루어집니다.

**핵심**: 100명이 연결하면 서버는 1개의 Listen Socket + 100개의 Connection Socket을 관리합니다.

```mermaid
flowchart TB
    subgraph Server["서버 (192.168.1.100)"]
        subgraph ListenLayer["1️⃣ Listen Socket"]
            LS["포트 8080에서 대기<br/>새 연결 요청만 처리"]
        end

        subgraph ConnectionLayer["2️⃣ Connection Sockets"]
            CS1["Socket 1<br/>━━━━━━━━━━<br/>Local: :8080<br/>Remote: 10.0.0.50:52341"]
            CS2["Socket 2<br/>━━━━━━━━━━<br/>Local: :8080<br/>Remote: 10.0.0.51:49872"]
            CS3["Socket 3<br/>━━━━━━━━━━<br/>Local: :8080<br/>Remote: 10.0.0.50:52342"]
        end

        LS -->|"Accept()"| CS1
        LS -->|"Accept()"| CS2
        LS -->|"Accept()"| CS3
    end

    subgraph Clients["클라이언트들"]
        C1["클라이언트 A<br/>10.0.0.50:52341<br/>(브라우저 탭 1)"]
        C2["클라이언트 B<br/>10.0.0.51:49872"]
        C3["클라이언트 A<br/>10.0.0.50:52342<br/>(브라우저 탭 2)"]
    end

    CS1 <-->|"TCP 연결"| C1
    CS2 <-->|"TCP 연결"| C2
    CS3 <-->|"TCP 연결"| C3
```

---

### 패킷이 올바른 소켓에 전달되는 과정

**"패킷이 도착했을 때, OS는 어떻게 올바른 소켓에 전달하는가?"**

이 과정은 **운영체제 커널**이 자동으로 처리합니다. 애플리케이션은 신경 쓸 필요가 없습니다.

1. **패킷 도착**: 네트워크 카드가 패킷을 수신합니다. 패킷 헤더에는 출발지(클라이언트 IP:Port)와 목적지(서버 IP:Port) 정보가 포함되어 있습니다.

2. **4-Tuple 조회**: OS 커널은 패킷의 4-Tuple 정보를 확인하고, 내부 테이블에서 **매칭되는 소켓**을 찾습니다.
   - 서버 포트 8080 + 클라이언트 10.0.0.50:52341 → Socket 1
   - 서버 포트 8080 + 클라이언트 10.0.0.51:49872 → Socket 2

3. **버퍼 전달**: 매칭된 소켓의 수신 버퍼에 데이터를 복사합니다.

4. **애플리케이션 읽기**: 애플리케이션이 `socket.Read()`를 호출하면, 해당 소켓의 버퍼에서 데이터를 읽습니다.

**결론**: 애플리케이션은 "이 소켓에서 읽은 데이터 = 이 클라이언트가 보낸 것"이라고 확신할 수 있습니다. OS가 보장합니다.

```mermaid
flowchart TB
    subgraph Network["네트워크"]
        PKT["📦 패킷 도착<br/>━━━━━━━━━━━━━━━━<br/>From: 10.0.0.50:52341<br/>To: 192.168.1.100:8080<br/>Data: CREATE 요청"]
    end

    subgraph OS["운영체제 (커널)"]
        NIC["네트워크 카드"]
        LOOKUP["4-Tuple 조회<br/>━━━━━━━━━━━━━━━━<br/>(8080, 10.0.0.50:52341)<br/>→ Socket 1에 매칭"]
    end

    subgraph Server["서버 프로세스"]
        S1["Socket 1 버퍼<br/>← 여기에 전달!"]
        S2["Socket 2 버퍼"]
        S3["Socket 3 버퍼"]
    end

    subgraph App["애플리케이션"]
        READ["socket1.Read()<br/>→ CREATE 요청 수신"]
        KNOW["발신자 = Socket 1<br/>= 클라이언트 A"]
    end

    PKT --> NIC
    NIC --> LOOKUP
    LOOKUP -->|"Socket 1"| S1
    LOOKUP -.->|"X"| S2
    LOOKUP -.->|"X"| S3
    S1 --> READ
    READ --> KNOW
```

---

### Listen Socket vs Connection Socket

| 구분 | Listen Socket | Connection Socket |
|------|---------------|-------------------|
| **역할** | 새 연결 요청 대기 | 실제 데이터 통신 |
| **개수** | 포트당 1개 | 클라이언트당 1개 |
| **생성 시점** | 서버 시작 시 | Accept() 호출 시 |
| **사용 메서드** | Accept() | Read(), Write() |

**비유: 콜센터**

```
콜센터 대표번호: 1588-1234 (Listen Socket)

고객 A 전화 → 상담원 1에게 연결 (Connection Socket 1)
고객 B 전화 → 상담원 2에게 연결 (Connection Socket 2)
고객 C 전화 → 상담원 3에게 연결 (Connection Socket 3)

- 대표번호는 하나
- 하지만 각 고객은 별도의 상담원(소켓)과 통화
- 고객 A가 말하면 상담원 1만 들음
```

---

### 왜 Listen Socket이 필요한가?

**"어차피 Connection Socket으로 통신하는데, Listen Socket은 왜 필요한가?"**

#### 1. 역할 분리 (Single Responsibility)

| 소켓 | 역할 | 수행 작업 |
|------|------|----------|
| **Listen Socket** | 연결 "감지" | `Accept()` 호출, 새 연결 대기 |
| **Connection Socket** | 데이터 "송수신" | `Read()`, `Write()` 호출 |

하나의 소켓이 두 역할을 동시에 수행하면 복잡해지고, 동시성 처리가 어려워집니다.

#### 2. 동시 연결 처리

**Listen Socket이 없다면:**

```
클라이언트 A와 통신 중...
  → 클라이언트 B가 연결 시도
  → 같은 소켓으로 "연결 수락"과 "데이터 통신"을 동시에 할 수 없음
  → B는 A의 통신이 끝날 때까지 대기해야 함
```

**Listen Socket이 있으면:**

```
Listen Socket: 계속 새 연결 대기 (블로킹되지 않음)
Connection Socket 1: 클라이언트 A와 독립적으로 통신
Connection Socket 2: 클라이언트 B와 독립적으로 통신
  → 동시에 여러 클라이언트 처리 가능
```

#### 3. Accept() 함수의 동작

```go
// 서버 시작: Listen Socket 생성
listenSocket, _ := net.Listen("tcp", ":8080")

for {
    // Accept()는 Listen Socket에서 호출
    // 새 Connection Socket을 반환하고, Listen Socket은 계속 대기
    connSocket, _ := listenSocket.Accept()

    // 각 연결을 별도 고루틴으로 처리
    go handleConnection(connSocket)
}

func handleConnection(conn net.Conn) {
    // 이 Connection Socket으로만 이 클라이언트와 통신
    data := make([]byte, 1024)
    conn.Read(data)   // 이 클라이언트의 데이터만 읽힘
    conn.Write([]byte("응답"))
}
```

**핵심 포인트:**
- `Accept()`는 Listen Socket을 "소비"하지 않습니다
- Listen Socket은 계속 대기 상태를 유지하고, 새로운 Connection Socket만 반환합니다
- 이 덕분에 "연결 수락"과 "데이터 통신"이 분리되어 동시 처리가 가능합니다

#### 결론

> Listen Socket이 없으면 서버는 **한 번에 한 클라이언트만** 처리할 수 있습니다. Listen Socket 덕분에 "연결 수락"과 "데이터 통신"이 분리되어 **동시에 여러 클라이언트**를 처리할 수 있습니다.

---

### 터미널에서 연결 상태 확인

```bash
# 서버 실행 후, 여러 클라이언트 연결 상태 확인
$ netstat -an | grep 8080

tcp  LISTEN     0.0.0.0:8080          *:*              # Listen Socket
tcp  ESTABLISHED 192.168.1.100:8080   10.0.0.50:52341  # 연결 1
tcp  ESTABLISHED 192.168.1.100:8080   10.0.0.51:49872  # 연결 2
tcp  ESTABLISHED 192.168.1.100:8080   10.0.0.50:52342  # 연결 3
```

**Windows에서:**
```powershell
netstat -an | findstr 8080
```

**macOS/Linux에서 더 상세한 정보:**
```bash
# ss 명령어 (더 빠르고 상세함)
ss -tnp | grep 8080

# lsof로 프로세스별 확인
lsof -i :8080
```

---

### 동일 클라이언트에서 여러 WebSocket 연결

**"같은 컴퓨터에서 브라우저 탭을 여러 개 열면, 포트는 어떻게 되나?"**

**각 연결마다 클라이언트 OS가 서로 다른 포트를 자동으로 할당합니다.** 이를 **Ephemeral Port(임시 포트)**라고 합니다.

```
클라이언트 A (IP: 10.0.0.50)에서 3개의 WebSocket 연결:

브라우저 탭 1: new WebSocket('ws://server:8080')
  → OS가 자동 할당: 10.0.0.50:52341

브라우저 탭 2: new WebSocket('ws://server:8080')
  → OS가 자동 할당: 10.0.0.50:52342

같은 탭에서 두 번째 연결: new WebSocket('ws://server:8080')
  → OS가 자동 할당: 10.0.0.50:52343
```

**포트 할당 과정:**

```mermaid
sequenceDiagram
    participant App as 브라우저/앱
    participant OS as 클라이언트 OS
    participant Server as 서버

    App->>OS: new WebSocket('ws://server:8080')
    Note over OS: 사용 가능한 포트 검색<br/>52341 할당
    OS->>Server: TCP 연결 (from 10.0.0.50:52341)

    App->>OS: new WebSocket('ws://server:8080')
    Note over OS: 다음 사용 가능한 포트<br/>52342 할당
    OS->>Server: TCP 연결 (from 10.0.0.50:52342)
```

**Ephemeral Port 범위:**

| OS | 기본 범위 | 총 개수 |
|------|----------|:-------:|
| **Linux** | 32768 - 60999 | ~28,000 |
| **Windows** | 49152 - 65535 | ~16,000 |
| **macOS** | 49152 - 65535 | ~16,000 |

```bash
# Linux에서 확인
cat /proc/sys/net/ipv4/ip_local_port_range
# 출력: 32768    60999

# macOS에서 확인
sysctl net.inet.ip.portrange.first net.inet.ip.portrange.last
# 출력: net.inet.ip.portrange.first: 49152
#       net.inet.ip.portrange.last: 65535

# Windows PowerShell에서 확인
netsh int ipv4 show dynamicport tcp
```

**서버 입장에서 보면:**

```
서버 (192.168.1.100:8080)의 연결 테이블:

┌─────────────────────────────────────────────────────────┐
│ Connection Socket │ 클라이언트 주소        │ 식별     │
├───────────────────┼───────────────────────┼──────────┤
│ Socket 1          │ 10.0.0.50:52341       │ A의 탭1  │
│ Socket 2          │ 10.0.0.50:52342       │ A의 탭2  │
│ Socket 3          │ 10.0.0.50:52343       │ A의 탭1 두번째 │
│ Socket 4          │ 10.0.0.51:49872       │ B        │
└─────────────────────────────────────────────────────────┘

→ 같은 IP(10.0.0.50)지만 포트가 달라서 구분 가능
```

| 질문 | 답변 |
|------|------|
| 같은 클라이언트에서 여러 연결 시 포트? | **각각 다른 포트** (OS가 자동 할당) |
| 누가 포트를 할당하나? | **클라이언트 OS** (애플리케이션이 아님) |
| 포트 번호를 지정할 수 있나? | 일반적으로 불가능 (브라우저는 특히) |
| 포트가 부족하면? | 연결 실패 (드물지만 가능) |

---

### 핵심 정리

| 개념 | 설명 |
|------|------|
| **4-Tuple** | (서버IP, 서버Port, 클라이언트IP, 클라이언트Port)로 연결 구분 |
| **Listen Socket** | 새 연결 요청 대기, 포트당 1개 |
| **Connection Socket** | 실제 통신용, 클라이언트당 1개 |
| **Accept()** | Listen Socket에서 Connection Socket 생성 |

**결론**: 서버 포트는 하나지만, 각 클라이언트 연결은 **클라이언트의 IP:Port가 다르기 때문에** 구분됩니다. OS 커널이 4-Tuple로 패킷을 올바른 소켓에 전달합니다.

---

## A5. 네이티브 WebSocket API

### 표준 규격

**네이티브 WebSocket API는 두 가지 표준에 의해 정의됩니다:**

| 표준 | 담당 기관 | 정의 내용 |
|------|----------|----------|
| **RFC 6455** | IETF | WebSocket **프로토콜** (핸드셰이크, 프레임 형식, Close 코드 등) |
| **WebSocket API** | WHATWG/W3C | JavaScript **인터페이스** (WebSocket 클래스, 이벤트, 메서드) |

```mermaid
flowchart TB
    subgraph Standards["표준 규격"]
        RFC["RFC 6455<br/>(프로토콜 규격)"]
        API["WHATWG WebSocket API<br/>(JavaScript 인터페이스)"]
    end

    subgraph Browser["브라우저 구현"]
        Engine["브라우저 엔진 (C++)<br/>Blink, Gecko, WebKit"]
        Binding["JavaScript 바인딩"]
        JS["JavaScript WebSocket 객체"]
    end

    RFC --> Engine
    API --> Binding
    Engine --> Binding
    Binding --> JS
```

### 브라우저 내부 구현 방식

**JavaScript의 `new WebSocket()`을 호출하면 실제로 무슨 일이 일어나는가?**

```mermaid
sequenceDiagram
    participant JS as JavaScript 코드
    participant V8 as V8 엔진
    participant Blink as Blink (C++)
    participant Net as 네트워크 스택
    participant OS as OS 소켓

    JS->>V8: new WebSocket('wss://...')
    V8->>Blink: WebSocket 바인딩 호출
    Blink->>Blink: WebSocket 객체 생성 (C++)
    Blink->>Net: 연결 요청
    Net->>OS: TCP 소켓 생성 + TLS
    OS-->>Net: 소켓 fd 반환
    Net-->>Blink: 연결 완료
    Blink-->>V8: onopen 이벤트 전달
    V8-->>JS: ws.onopen() 콜백 실행
```

**핵심 포인트:**
1. **JavaScript WebSocket 객체는 껍데기입니다.** 실제 네트워크 작업은 브라우저의 C++ 코드가 수행합니다.
2. **V8(JavaScript 엔진)은 네트워크를 직접 다루지 않습니다.** Blink(렌더링 엔진)에 위임합니다.
3. **이벤트 루프를 통해 비동기 처리됩니다.** 네트워크 I/O가 완료되면 JavaScript 콜백이 실행됩니다.

### Web IDL 인터페이스 정의

**브라우저는 Web IDL(Interface Definition Language)로 JavaScript API를 정의합니다:**

```webidl
// WHATWG WebSocket API 명세 (간략화)
[Exposed=(Window,Worker)]
interface WebSocket : EventTarget {
  constructor(USVString url, optional (DOMString or sequence<DOMString>) protocols = []);

  readonly attribute USVString url;

  // 연결 상태
  const unsigned short CONNECTING = 0;
  const unsigned short OPEN = 1;
  const unsigned short CLOSING = 2;
  const unsigned short CLOSED = 3;
  readonly attribute unsigned short readyState;

  // 이벤트 핸들러
  attribute EventHandler onopen;
  attribute EventHandler onmessage;
  attribute EventHandler onerror;
  attribute EventHandler onclose;

  // 메서드
  undefined send((BufferSource or Blob or USVString) data);
  undefined close(optional unsigned short code, optional USVString reason);
};
```

**IDL → C++ → JavaScript 변환 과정:**

| 단계 | 설명 |
|------|------|
| 1. IDL 작성 | WHATWG 명세에 따라 인터페이스 정의 |
| 2. 바인딩 생성 | IDL을 C++ 바인딩 코드로 자동 변환 |
| 3. 구현 연결 | 바인딩이 실제 C++ WebSocket 구현체를 호출 |
| 4. JS 노출 | V8이 JavaScript에서 접근 가능한 객체로 노출 |

### 브라우저별 구현체

| 브라우저 | 엔진 | WebSocket 구현 위치 |
|---------|------|-------------------|
| Chrome | Blink + V8 | `blink/renderer/modules/websockets/` |
| Firefox | Gecko + SpiderMonkey | `dom/websocket/` |
| Safari | WebKit + JavaScriptCore | `Source/WebCore/Modules/websockets/` |

**Chromium 실제 코드 구조 (참고):**

```
chromium/third_party/blink/renderer/modules/websockets/
├── websocket.h              # WebSocket 클래스 헤더
├── websocket.cc             # WebSocket 구현
├── websocket_channel.h      # 채널 추상화
├── websocket_channel_impl.cc # 실제 네트워크 통신
└── ...
```

### 왜 네이티브 코드로 구현하는가?

| 이유 | 설명 |
|------|------|
| **성능** | JavaScript보다 C++이 네트워크 I/O에 훨씬 빠름 |
| **보안** | 샌드박스 내에서 안전하게 소켓 접근 제어 |
| **OS 통합** | 운영체제의 네트워크 스택(TCP/IP)과 직접 통신 |
| **메모리 효율** | 바이너리 데이터 처리에 C++이 유리 |

**요약:**
> `new WebSocket()`은 JavaScript 문법이지만, 실제로는 브라우저의 C++ 네이티브 코드가 TCP 소켓을 열고, TLS 핸드셰이크를 수행하며, WebSocket 프레임을 파싱합니다. JavaScript는 이벤트 콜백만 처리합니다.

---

### 핵심 메서드

| 메서드 | 설명 | 사용 시점 |
|--------|------|----------|
| `new WebSocket(url)` | WebSocket 객체 생성, 즉시 연결 시도 | 컴포넌트 마운트 시 |
| `send(data)` | 서버로 메시지 전송 (문자열, ArrayBuffer, Blob) | `readyState === OPEN`일 때만 |
| `close(code?, reason?)` | 연결 종료 (코드: 1000=정상, reason: 사유) | 컴포넌트 언마운트 시 |

### 핵심 이벤트 (발생 순서대로)

```typescript
const ws = new WebSocket('wss://example.com/ws');

// 1. 연결 성공
ws.onopen = (event) => {
  console.log('연결됨!');
  ws.send('Hello');  // 이제 send() 호출 가능
};

// 2. 메시지 수신 (여러 번 발생)
ws.onmessage = (event) => {
  console.log('받은 메시지:', event.data);
};

// 3. 에러 발생 (연결 실패 등)
ws.onerror = (event) => {
  console.error('에러 발생');
  // 상세 정보는 보안상 제한됨
};

// 4. 연결 종료 (항상 마지막에 발생)
ws.onclose = (event) => {
  console.log(`연결 종료: 코드=${event.code}, 이유=${event.reason}`);
};
```

### readyState 상태

```mermaid
stateDiagram-v2
    [*] --> CONNECTING: new WebSocket()
    CONNECTING --> OPEN: 연결 성공
    CONNECTING --> CLOSED: 연결 실패
    OPEN --> CLOSING: close() 호출
    OPEN --> CLOSED: 서버가 종료
    CLOSING --> CLOSED: 종료 완료

    note right of CONNECTING: readyState = 0
    note right of OPEN: readyState = 1<br/>send() 가능
    note right of CLOSING: readyState = 2
    note right of CLOSED: readyState = 3
```

### 주의사항

**send()는 반드시 `readyState === OPEN`(1)일 때만 호출해야 합니다.**

```typescript
// ❌ 잘못된 예: 연결 전 send() 호출
const ws = new WebSocket('wss://...');
ws.send('Hello');  // 에러! 아직 CONNECTING 상태

// ✅ 올바른 예: onopen 후 send()
ws.onopen = () => {
  ws.send('Hello');  // 이제 안전
};

// ✅ 또는 readyState 확인
if (ws.readyState === WebSocket.OPEN) {
  ws.send('Hello');
}
```

---

## 핵심 정리 (한 문장으로)

> WebSocket은 **HTTP 핸드셰이크로 시작해 양방향 지속 연결로 업그레이드**되며, 서버 푸시와 낮은 오버헤드로 **실시간 통신에 최적화된 프로토콜**이다.

---

## URL 스킴

| 스킴 | HTTP 대응 | 기본 포트 | 암호화 |
|------|----------|:--------:|:------:|
| `ws://` | `http://` | 80 | X |
| `wss://` | `https://` | 443 | O (TLS) |

### ws:// vs wss:// 연결 과정

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    rect rgb(255, 230, 230)
        Note over C,S: ws:// (암호화 없음)
        C->>S: TCP 연결
        C->>S: WebSocket 핸드셰이크 (평문)
        S-->>C: 101 Switching Protocols
        C->>S: 메시지 (평문으로 전송)
        Note over C,S: ⚠️ 누구나 내용을 볼 수 있음
    end

    rect rgb(230, 255, 230)
        Note over C,S: wss:// (TLS 암호화)
        C->>S: TCP 연결
        C->>S: TLS 핸드셰이크 (인증서 검증)
        S-->>C: TLS 완료
        Note over C,S: 암호화 터널 수립
        C->>S: WebSocket 핸드셰이크 (암호화)
        S-->>C: 101 Switching Protocols
        C->>S: 메시지 (암호화되어 전송)
        Note over C,S: ✅ 중간에서 내용 해독 불가
    end
```

### 중간자 공격 (MITM) 시나리오

**ws://를 사용하면 다음과 같은 공격에 노출됩니다:**

```mermaid
flowchart LR
    subgraph Attack["중간자 공격 (ws://)"]
        C1["클라이언트"] -->|"평문 메시지"| A["공격자<br/>(공용 WiFi)"]
        A -->|"변조된 메시지"| S1["서버"]
        A -.->|"도청/변조"| A
    end
```

| 공격 유형 | 설명 | 예시 |
|----------|------|------|
| **도청 (Eavesdropping)** | 메시지 내용을 그대로 볼 수 있음 | 채팅 내용, 인증 토큰 탈취 |
| **변조 (Tampering)** | 메시지를 중간에서 수정 | 주식 가격 조작, 게임 데이터 변조 |
| **세션 하이재킹** | 연결을 가로채서 대신 통신 | 사용자 행세하여 악성 명령 전송 |

**실제 공격 시나리오:**

```
1. 사용자가 카페 WiFi에 연결
2. 공격자가 같은 네트워크에서 패킷 스니핑
3. ws://로 전송되는 WebSocket 메시지 캡처
4. 채팅 내용, 인증 토큰, 민감한 데이터 탈취
```

### wss://가 필수인 이유

#### 1. 보안 (Security)

| 보호 항목 | ws:// | wss:// |
|----------|:-----:|:------:|
| 데이터 기밀성 | ❌ | ✅ |
| 데이터 무결성 | ❌ | ✅ |
| 서버 인증 | ❌ | ✅ (인증서) |
| 중간자 공격 방지 | ❌ | ✅ |

#### 2. 혼합 콘텐츠 정책 (Mixed Content)

**HTTPS 페이지에서 ws://는 사용할 수 없습니다.**

```javascript
// HTTPS 페이지 (https://example.com)에서:

// ❌ 브라우저가 차단함
const ws1 = new WebSocket('ws://api.example.com/ws');
// Error: Mixed Content: 'https://example.com'이 'ws://api.example.com'에 연결 시도

// ✅ 정상 동작
const ws2 = new WebSocket('wss://api.example.com/ws');
```

**브라우저 정책:**

| 페이지 프로토콜 | ws:// | wss:// |
|:-------------:|:-----:|:------:|
| http:// | ✅ 허용 | ✅ 허용 |
| https:// | ❌ **차단** | ✅ 허용 |

대부분의 프로덕션 사이트는 HTTPS이므로, **wss://만 사용 가능**합니다.

#### 3. 프록시/방화벽 통과

```mermaid
flowchart LR
    subgraph ws["ws:// (포트 80)"]
        C1["클라이언트"] --> F1["방화벽/프록시"]
        F1 -->|"WebSocket?<br/>차단할 수도"| S1["서버"]
    end

    subgraph wss["wss:// (포트 443)"]
        C2["클라이언트"] --> F2["방화벽/프록시"]
        F2 -->|"TLS 암호화<br/>내용 검사 불가"| S2["서버"]
    end
```

| 환경 | ws:// | wss:// |
|------|:-----:|:------:|
| 기업 프록시 | 종종 차단됨 | 대부분 통과 |
| 공용 WiFi | 차단될 수 있음 | 대부분 통과 |
| 일부 ISP | 조작 가능 | 안전 |

**이유:**
- 포트 443(HTTPS)은 거의 모든 환경에서 허용
- TLS 암호화로 인해 프록시가 내용을 검사할 수 없어 차단하기 어려움

### 개발 vs 프로덕션

| 환경 | 권장 스킴 | 이유 |
|------|----------|------|
| 로컬 개발 | `ws://localhost:...` | 인증서 설정 불필요 |
| 개발 서버 | `wss://` (자체 서명 인증서) | 프로덕션과 동일한 환경 |
| **프로덕션** | **`wss://` 필수** | 보안, 혼합 콘텐츠, 호환성 |

```typescript
// 환경별 URL 설정 예시
const WS_URL = process.env.NODE_ENV === 'production'
  ? 'wss://api.example.com/ws'
  : 'ws://localhost:8080/ws';
```

**핵심 요약:**
> `wss://`는 단순히 "더 안전한 옵션"이 아니라, **프로덕션에서 유일하게 실용적인 선택**입니다. HTTPS 사이트에서 `ws://`는 브라우저가 차단하고, 기업 환경에서는 프록시가 차단할 수 있습니다.

---

## A5. Long Polling의 한계와 WebSocket의 해결

### Long Polling의 동작 방식

**Long Polling은 WebSocket 이전에 "실시간"을 구현하던 방식입니다.** 서버가 새 데이터가 생길 때까지 응답을 보류합니다.

```mermaid
sequenceDiagram
    participant C as 클라이언트
    participant S as 서버

    C->>S: GET /events (요청 1)
    Note over S: 대기... (30초까지)
    S-->>C: 새 데이터!
    Note over C: 즉시 다음 요청

    C->>S: GET /events (요청 2)
    Note over S: 대기...
    S-->>C: 새 데이터!

    Note over C,S: 반복...
```

### Long Polling의 한계

| 한계 | 설명 |
|------|------|
| **HTTP 오버헤드** | 매 응답마다 HTTP 헤더 포함 (수백 바이트) |
| **연결 재수립** | 응답 후 새 TCP 연결 또는 재사용 협상 |
| **서버 리소스** | 대기 중에도 연결/스레드 점유 |
| **지연 시간** | 데이터 발생 → 응답 → 재요청 왕복 |
| **Half-Duplex** | 서버가 응답하면 클라이언트는 요청해야 다시 수신 가능 |

### WebSocket이 해결하는 문제

```mermaid
flowchart TB
    subgraph LP["Long Polling"]
        LP1["요청 → 대기 → 응답"]
        LP2["연결 종료"]
        LP3["다시 요청"]
        LP1 --> LP2 --> LP3 --> LP1
    end

    subgraph WS["WebSocket"]
        WS1["핸드셰이크 (1회)"]
        WS2["연결 유지"]
        WS3["양방향 메시지"]
        WS1 --> WS2 --> WS3
        WS3 --> WS3
    end

    LP ---|"개선"| WS
```

| 비교 항목 | Long Polling | WebSocket |
|----------|:------------:|:---------:|
| 연결 수립 | 매번 | 최초 1회 |
| 메시지 오버헤드 | 수백 바이트 | 2~14 바이트 |
| 서버 푸시 | 요청 대기 필요 | 언제든 가능 |
| 양방향 통신 | 불가능 | 가능 (Full-Duplex) |
| 지연 시간 | 높음 | 낮음 |

---

## 운영 및 스케일링

WebSocket의 운영 난이도, 로드밸런싱, 방화벽 대응, 재접속 폭풍 처리 등은 [08. 스케일링 고려사항](../08-scaling-considerations/)을 참조하세요.

---

## 실습으로 이동
→ `practice/native-websocket.ts`
