---
title: gateway-lab — raw Netty 게이트웨이 학습 인덱스
tags: [moc, study-index, lab, netty, spring, gateway, networking]
status: draft
source:
  - ~/study/gateway-lab  # 코드·작업 지도·조사 문서 (로컬)
related:
  - ./STATE.md
  - ../../README.md
  - ../../03_network/reactive-net/01-02.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%EA%B3%BC%20BIO%20vs%20NIO.md
  - ../../03_network/reactive-net/01-04.%EC%B1%84%EB%84%90%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%EC%BD%94%EB%8D%B1.md
updated: 2026-09-22
---

# gateway-lab — raw Netty 게이트웨이 학습 인덱스

HTTP 리버스 프록시에서 API 게이트웨이까지 raw Netty 로 단계별로 지으면서 이벤트 루프·버퍼 수명·라우팅·실패 처리를 익히는 랩의 학습 문서 모음입니다. 코드와 작업 지도는 `~/study/gateway-lab` 에 있고, 여기에는 Phase 별 학습 문서와 학습 상태만 둡니다. 진행은 `/learning-session gateway-lab` 으로 엽니다.

## 어떻게 진행하는가

게이트웨이 Phase 하나가 학습 토픽 하나입니다. 각 토픽을 4-Phase 로 돕니다. 개념 이해에서는 코드 전에 그 Phase 의 Netty 개념을 자기 말로 세웁니다. 학습 문서에서 그것을 적습니다. 실습에서는 AI 가 쓴 코드를 학습자가 예측·실행·관찰합니다. 검증에서는 독립 자답으로 닫습니다. 완료 기준은 저장소 지도의 "빌드·테스트·이해 확인" 세 항목입니다. 검증 Phase 가 세 번째 항목입니다.



## Phase 와 문서

| Phase | 학습 질문 | 문서 | 상태 |
|---|---|---|---|
| 1 고정 프록시 | 요청 하나가 두 채널·두 파이프라인을 어떻게 지나며 버퍼는 누구 것인가 | (Phase 2 에서 작성) | 시작 전 |
| 2 경로 라우팅 | 매칭 우선순위와 미일치의 종료 지점 | | |
| 3 타깃 그룹 | 백엔드 선택 상태와 헬스의 소유자 | | |
| 4 장애 처리 | connect 실패와 응답 지연의 구분, 재시도가 안전한 조건 | | |
| 5 요청 식별자 | 동시 요청에서 식별자가 섞이지 않는 자리 | | |
| 6a 로그 스키마 | 실패를 입증하는 필드 | | |
| 6b 비동기 큐 | 로그 I/O 가 루프를 막지 않는 구조와 포화 정책 | | |
| 6c 이력 저장 | DB 지연·장애의 격리 | | |
| 8 관리 API | 처리 중 요청과 새 요청이 보는 라우트 버전 | | |

Phase 7(로그 수집 파이프라인)은 선택이라 표에 두지 않았습니다. 진행하면 그때 행을 추가합니다.



## 기존 노트 흡수 규칙

`03_network/` 의 Netty·실패 처리 노트는 이 랩과 겹칩니다. 겹치는 절은 **이쪽으로 흡수**하고 원본은 링크만 남깁니다. 방향은 한쪽입니다. 랩 문서가 정본이 되고 옛 노트가 stub 가 됩니다.

| 기존 노트 | 겹치는 Phase | 처리 |
|---|---|---|
| `03_network/reactive-net/01-02` 이벤트 기반·BIO vs NIO, `01-03` 부트스트랩, `01-04` 채널 파이프라인과 코덱, `01-05` 바이트 버퍼, `01-06` 서버 구현, `01-07` 클라이언트 구현 | Phase 1 | Phase 1 학습 문서를 쓸 때 절별로 대조해 흡수. `01-01`(Reactor Netty 와 WebFlux 관계)은 Spring 축이라 남긴다 |
| `03_network/resilience/01-03` Retry, `01-05` Time Limiter | Phase 4 | 재시도 조건·예산·타임아웃 절만 흡수. Resilience4j 설정 절은 남긴다 |
| `03_network/resilience/01-02` Circuit Breaker, `01-05` Rate Limiter | 선택 심화 (Phase 4 뒤) | 선택 심화를 실제로 진행할 때만 흡수. 그 전엔 링크 |
| `03_network/feign/01-03` 에러 모델(상태 코드 실패 vs 무응답 실패) | Phase 4 | 502·504 구분 절만 흡수 |
| `03_network/webflux/*`, `03_network/realtime/*` | 없음 | 손대지 않는다 |

절차는 학습 문서 승인 뒤, 같은 세션 안에서 합니다.

1. 흡수 대상 노트를 통째로 열고, 랩 문서와 **절 단위로 코드 토큰까지 대조**합니다. 헤딩만 맞춰 보면 고유 내용을 놓칩니다.
2. 옛 노트에만 있는 고유 내용은 랩 문서의 해당 절로 옮깁니다. 본문 사실은 바꾸지 않습니다.
3. 옛 노트는 frontmatter 와 "이 문서는 `project/gateway-lab/…` 로 흡수됐다" 한 줄 + 링크만 남깁니다.
4. 옛 노트를 가리키던 링크를 셉니다(`03_network/README.md`, `reactive-net/README.md`, `09_spring/README.md`, `roadmap/spring-roadmap.md`). 실측 건수만큼 새 위치로 고칩니다.
5. 로드맵 행은 지도의 W-14 절차대로 그 Phase 개념 행을 랩 문서로 잇습니다.



## 참고

- 학습 상태: [STATE.md](./STATE.md)
- 기존 Netty 노트: `03_network/reactive-net/` 의 01-02(BIO vs NIO), 01-04(채널 파이프라인과 코덱)
