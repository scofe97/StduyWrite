---
title: 실시간 통신 학습 MOC — SSE·WebSocket·STOMP
tags: [moc, spring, websocket, stomp, sse, realtime]
status: draft
related:
  - ../README.md
  - ../reactive-net/README.md
updated: 2026-05-30
---

# 실시간 통신 학습 MOC — SSE·WebSocket·STOMP

---

> 같은 03_network 안의 WebClient·OpenFeign 이 *요청을 보내고 응답을 받는* 단방향 호출이라면, 본 묶음은 *연결을 열어 두고 서버가 밀어 주거나 양쪽이 수시로 주고받는* 실시간 통신을 다룹니다. 서버가 일방적으로 밀어 주는 SSE(Server-Sent Events)부터, 양방향 WebSocket, 그 위에 메시지 규약을 얹은 STOMP 까지, 그리고 연결 관리·메시지 동기화 같은 운영 패턴을 한 묶음으로 모읍니다.


## 왜 별도 묶음인가

HTTP 요청-응답은 클라이언트가 물을 때마다 서버가 답하는 구조라, 서버가 먼저 데이터를 보내야 하는 실시간 상황(채팅·알림·시세)에는 맞지 않습니다. 그래서 연결을 유지한 채 메시지를 흘려보내는 별도 패러다임이 필요합니다. WebClient·OpenFeign 의 *클라이언트 선택* 축과도, Reactor Netty 의 *전송 엔진* 축과도 다른, "연결 모델" 자체가 다른 자리라 별도 묶음으로 둡니다.

## 학습 순서

> 번호 체계는 주제 축입니다. 01 은 공통 기반, 02 는 SSE, 03 은 WebSocket·STOMP, 04 는 연결 관리·동기화 운영 패턴입니다. 본문은 React·JS 프론트 구현을 제외하고 *프로토콜 원리와 Spring 구현* 에 집중합니다.

| 정식 # | 주제 | 다루는 핵심 |
|--------|------|-----------|
| 01-01 | [HTTP·TCP 통신과 HTTP vs Socket](01-01.HTTP·TCP%20통신과%20HTTP%20vs%20Socket.md) | OSI 계층, TCP·HTTP 차이, 실시간 흉내 3종, 4기술 비교 |
| 01-02 | [HTTP2와 실시간 통신 기반](01-02.HTTP2와%20실시간%20통신%20기반.md) | HTTP/1.1 연결 제한·HOL, HTTP/2 멀티플렉싱·프레임, SSE 시너지 |
| 02-01 | [SSE 원리와 Spring 구현](02-01.SSE%20원리와%20Spring%20구현.md) | Keep-Alive·Chunked·필수 헤더, 이벤트 스트림 포맷, `SseEmitter` |
| 02-02 | [SSE 신뢰성 — 재연결과 손실 복구](02-02.SSE%20신뢰성%20—%20재연결과%20손실%20복구.md) | retry·Last-Event-ID 복구, 손실 시나리오, 하트비트, 재접속 폭풍 |
| 03-01 | [WebSocket 프로토콜과 핸드셰이크](03-01.WebSocket%20프로토콜과%20핸드셰이크.md) | Sec-WebSocket-Accept 계산, 프레임·마스킹, Full-Duplex, 소켓 관리 |
| 03-02 | [WebSocket 구현](03-02.WebSocket%20구현.md) | `WebSocketHandler` 4콜백, 세션 관리, CORS |
| 03-03 | [WebSocket vs STOMP](03-03.WebSocket%20vs%20STOMP.md) | 핸드셰이크 헤더, WebSocket 한계, STOMP pub/sub·프레임 |
| 03-04 | [STOMP 실무 — Spring 구현](03-04.STOMP%20실무%20—%20Spring%20구현.md) | 브로커·prefix·엔드포인트, `@MessageMapping`·`@SendTo`, SockJS |
| 04-01 | [연결 관리와 재연결 전략](04-01.연결%20관리와%20재연결%20전략.md) | Close Code, 지수 백오프·Thundering Herd, 에러 분류, Fallback |
| 04-02 | [실시간 메시지 동기화 패턴](04-02.실시간%20메시지%20동기화%20패턴.md) | SNAPSHOT/DELTA, 버전·갭 감지, 메시지 타입 설계, STOMP 매핑 |

> 진입은 상황에 따라 갈립니다. 단방향 알림이면 01-01 에서 02 계열로, 양방향 채팅이면 01-01 에서 03 계열로 들어갑니다. 04 계열(연결 관리·동기화)은 SSE·WebSocket 어느 쪽을 골랐든 운영 단계에서 함께 봅니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-websocket` |
| Spring Framework | 6.2.x | `WebSocketHandler`·STOMP·`SseEmitter` |
| Java | 17+ | |

## 관련 문서

- [Spring 네트워크 통신 학습 MOC](../README.md) — 본 묶음이 속한 03_network 집계점
- [Reactor Netty 학습 MOC](../reactive-net/README.md) — WebSocket·SSE 도 결국 같은 전송 계층 위에서 동작
