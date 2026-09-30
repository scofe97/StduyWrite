---
topic: gateway-lab
scope: durable
level: 기본
last_verified:
blocked_count: 0
next_lesson: "Phase 1 개념 이해 — 두 채널·두 파이프라인, EventLoop 스레드 배정, ChannelFuture, ByteBuf 소유권(retain/release), 연결 종료. 코드 전에 자기 말로"
updated: 2026-09-22
---

# gateway-lab 학습 상태

## 미션 — 왜 이걸 배우는가

업무에서 만난 API 게이트웨이 제품은 Camel 이 Netty 를 감싸고 있어 요청이 어느 스레드에서, 어떤 버퍼로, 언제 놓이며 전달되는지 보이지 않았다. 같은 기능을 raw Netty 로 손수 지어 **이벤트 루프·버퍼 수명·라우팅·실패 처리**를 설명할 수 있게 되는 것이 미션이다. 제품 복제가 아니라 원리 습득이다.

## 진행 구조

게이트웨이 Phase 하나 = 학습 토픽 하나. 각 Phase 안을 4-Phase(개념 이해 → 학습 문서 → 실습 → 검증)로 돈다. 코드는 `~/study/gateway-lab`, 학습 로드맵은 그 저장소의 `docs/02-lab-plan/01-01.gateway-lab-roadmap.md`(Phase 설명은 02-01·02-02), 범위·결정은 `04-02.gateway-lab-decision-log.md` 가 기준이고, 바로 다음 Phase 의 상세는 `docs/02-lab-plan/03-NN.gateway-lab-phase<N>-plan.md` 다. 이 폴더에는 Phase 별 학습 문서와 이 상태 파일만 둔다.

| 게이트웨이 Phase | 학습 문서 (Phase 2 산출) | 4-Phase 진행 | 검증일 |
|---|---|---|---|
| 1 고정 프록시 | (미작성) | 개념 이해 전 | |
| 2 경로 라우팅 | | | |
| 3 타깃 그룹 | | | |
| 4 장애 처리 | | | |
| 5 요청 식별자 | | | |
| 6a·6b·6c 로그·큐·이력 | | | |
| 8 관리 API | | | |

## 현재 난이도 레벨

기본. Spring·JPA 는 익숙하고 Netty 는 노트로만 봤다(BIO vs NIO, 채널 파이프라인·코덱). 소켓·epoll 은 OS·네트워크 로드맵에서 다뤘다.

## 이해 근거 (선택)

- 프록시는 서버 채널과 클라이언트 채널을 동시에 다루는 프로그램이다. 두 채널을 같은 EventLoop 에 두면 동기화 없이 한 스레드에서 상태를 옮길 수 있다.
- ByteBuf 는 참조 카운트로 산다. 다른 채널에 넘기는 쪽이 retain, 다 쓴 쪽이 release. 예외 경로에서 "마지막으로 잡고 있던 쪽"을 정하지 않으면 누수나 이중 해제가 난다.

## 막힌 지점

- (없음 — 시작 전)

## 미해결 질문

- `HttpObjectAggregator` 는 상한 초과 시 413 을 보내고 연결을 닫는가, `Expect: 100-continue` 에 100 을 자동 응답하는가. Phase 1 실습에서 관찰해 답한다.
- Netty HTTP/1.1 파서는 HTTP/2 사전 지식 바이트(`PRI * HTTP/2.0`)에 400 을 내는가, 연결을 닫는가.

## 다음 레슨 후보 + 고른 이유

- Phase 1 개념 이해. 코드를 쓰기 전에 "요청 하나가 두 채널을 어떻게 지나고 버퍼가 누구 것인가"를 말로 세워야, 실습에서 예측이 가능하다.

## 물어볼 곳

- Netty GitHub Discussions (https://github.com/netty/netty/discussions) — 파이프라인·refCnt 동작이 문서와 다를 때.

## 흡수 대기 (README §기존 노트 흡수 규칙)

- Phase 1 학습 문서 작성 시: `03_network/reactive-net/01-02 ~ 01-07` 6편 — 미착수
- Phase 4 학습 문서 작성 시: `resilience/01-03·01-05` 일부, `feign/01-03` 일부 — 미착수
