---
title: WebSocket·SSE 실시간 통신 학습 MOC
tags: [moc, spring, websocket, stomp, sse, realtime]
status: draft
related:
  - ../README.md
  - ../reactive-net/README.md
updated: 2026-05-30
---

# WebSocket·SSE 실시간 통신 학습 MOC

---

> 같은 03_network 안의 WebClient·OpenFeign 이 *요청을 보내고 응답을 받는* 단방향 호출이라면, 본 묶음은 *연결을 열어 두고 양쪽이 수시로 메시지를 주고받는* 실시간 통신을 다룹니다. 서버가 일방적으로 밀어 주는 SSE(Server-Sent Events)부터, 양방향 WebSocket, 그 위에 메시지 규약을 얹은 STOMP 까지를 한 묶음으로 모읍니다.


## 왜 별도 묶음인가

HTTP 요청-응답은 클라이언트가 물을 때마다 서버가 답하는 구조라, 서버가 먼저 데이터를 보내야 하는 실시간 상황(채팅·알림·시세)에는 맞지 않습니다. 그래서 연결을 유지한 채 메시지를 흘려보내는 별도 패러다임이 필요합니다. WebClient·OpenFeign 의 *클라이언트 선택* 축과도, Reactor Netty 의 *전송 엔진* 축과도 다른, "연결 모델" 자체가 다른 자리라 별도 묶음으로 둡니다.

## 학습 순서 (이관 계획)

> `_notion_import/websocket/` 의 raw 7편을 정식 편으로 한 편씩 재작성해 옮깁니다. 노션 export 라 위젯·이미지 의존이 있어 본문은 완전한 문장과 Mermaid 로 다시 씁니다(`feedback_12spring_full_rewrite_cadence` — 풀 재작성 1편/세션). 본문 편은 아직 작성 전이며, 본 README 가 이관 계획을 담습니다.

| 정식 # (예정) | 주제 | raw 원본 | 상태 |
|---------------|------|---------|------|
| 01-01 | HTTP vs Socket — 통신 모델의 차이 | websocket/01-1, 01-2 | 이관 예정 |
| 01-02 | SSE (Server-Sent Events) 구현 | websocket/02-1 | 이관 예정 |
| 02-01 | WebSocket 구현 | websocket/02-2 | 이관 예정 |
| 02-02 | WebSocket vs STOMP — 메시지 규약 | websocket/03-1 | 이관 예정 |
| 02-03 | STOMP 실무 (Spring Boot + React) | websocket/03-2 | 이관 예정 |

> 순서: 통신 모델(왜 실시간이 필요한가) → SSE(단방향 푸시) → WebSocket(양방향) → STOMP(WebSocket 위 메시지 규약) → 실무. SSE 와 WebSocket 의 선택 기준 — 단방향이면 SSE, 양방향이면 WebSocket — 이 첫 결정 지점입니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-websocket` |
| Spring Framework | 6.2.x | `WebSocketHandler`·STOMP·`SseEmitter` |
| Java | 17+ | |

## 관련 문서

- [Spring 네트워크 통신 학습 MOC](../README.md) — 본 묶음이 속한 03_network 집계점
- [Reactor Netty 학습 MOC](../reactive-net/README.md) — WebSocket 도 결국 같은 전송 계층 위에서 동작
