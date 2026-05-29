---
title: Reactor Netty 학습 MOC
tags: [moc, spring, reactor-netty, netty, reactive, nio]
status: draft
source:
  - https://projectreactor.io/docs/netty/release/reference/
  - https://godekdls.github.io/Reactor%20Netty/gettingstarted/
related:
  - ../README.md
  - ../../01_core/04-01.WebFlux 서버 — 리액티브 스택과 어노테이션 모델.md
  - ../webflux/README.md
updated: 2026-05-30
---

# Reactor Netty 학습 MOC

---

> [`01_core/04-01`](../../01_core/04-01.WebFlux%20서버%20—%20리액티브%20스택과%20어노테이션%20모델.md) 에서 "WebFlux 의 기본 서버는 톰캣이 아니라 Netty 다" 라고 했습니다. 그 Netty 를 한 겹 아래에서 들여다보는 묶음입니다. WebFlux 가 컨트롤러·라우터로 *요청을 어떻게 다룰지* 를 정한다면, 그 요청이 실제로 소켓을 타고 오가는 *전송 계층* 을 Reactor Netty 가 맡습니다.


## 왜 별도 묶음인가

04장(WebFlux 서버)은 *애플리케이션 모델* 입니다. `@RestController` 와 `RouterFunction` 으로 요청 처리를 선언하는 자리입니다. 그러나 그 아래에는 소켓을 열고, 바이트를 읽고, 이벤트 루프로 다중 연결을 굴리는 *전송 계층* 이 있습니다. 그 계층이 Reactor Netty 이고, 채널·이벤트루프·버퍼·코덱 같은 개념은 애플리케이션 모델과 관심사가 다릅니다. 그래서 한 단계 더 내려가는 본 묶음을 따로 둡니다.

WebClient([`../webflux/`](../webflux/README.md))도 기본 전송으로 Reactor Netty 를 씁니다. 즉 인바운드(WebFlux 서버)든 아웃바운드(WebClient)든, Spring 의 리액티브 HTTP 는 같은 Reactor Netty 위에서 돕니다.

## 학습 순서

> `_notion_import/netty/` 의 raw 10편을 정식 편으로 한 편씩 재작성해 옮깁니다. 노션 export 라 위젯 마크업·이미지 의존이 있어, 본문은 완전한 문장과 Mermaid 로 다시 씁니다(`feedback_12spring_full_rewrite_cadence` — 풀 재작성 1편/세션).

| 정식 # | 주제 | raw 원본 | 상태 |
|--------|------|---------|------|
| 01-01 | [Reactor Netty 입문 — WebFlux의 하부 전송 계층](01-01.Reactor%20Netty%20입문%20—%20WebFlux의%20하부%20전송%20계층.md) | netty/01 | 작성 완료 |
| 01-02 | [이벤트 기반 프로그래밍과 BIO vs NIO](01-02.이벤트%20기반%20프로그래밍과%20BIO%20vs%20NIO.md) | netty/02, NIO/BIO Connector | 작성 완료 |
| (예정) | 부트스트랩 | netty/03 | 이관 예정 |
| (예정) | 채널 파이프라인과 코덱 ⭐ | netty/04 | 이관 예정 |
| (예정) | 바이트 버퍼 (ByteBuf) | netty/05 | 이관 예정 |
| (예정) | Component·Architecture (Server/Client 구현) | netty/06-1, 06-2 | 이관 예정 |

## 이관 방침

raw 원본은 [`../../_notion_import/netty/`](../../_notion_import/) 에 보존합니다. 노션 위젯(`<aside>💡`)·이미지·키워드 단편은 정식 문서 컨벤션에 맞지 않으므로, 그대로 옮기지 않고 한 편씩 *재작성* 합니다. 이미지에 담겼던 내용(논블로킹 동작도 등)은 Mermaid·산문으로 다시 풉니다. 전체 이관이 끝나면 raw 는 archive 로 옮기거나 폐기합니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-webflux` 가 Reactor Netty 를 기본 서버로 가져옴 |
| Reactor Netty | Boot 가 관리하는 버전 | Netty 기반 논블로킹 TCP·HTTP·UDP·QUIC, backpressure 지원 |
| Java | 17+ | NIO 채널 |

## 관련 문서

- [Spring 네트워크 통신 학습 MOC](../README.md) — 본 묶음이 속한 03_network 집계점
- [WebFlux 서버 — 리액티브 스택과 어노테이션 모델](../../01_core/04-01.WebFlux%20서버%20—%20리액티브%20스택과%20어노테이션%20모델.md) — 본 전송 계층 위의 애플리케이션 모델
- [Spring WebClient 학습 MOC](../webflux/README.md) — 아웃바운드도 같은 Reactor Netty 위
- [Reactor Netty 공식 레퍼런스](https://projectreactor.io/docs/netty/release/reference/)
