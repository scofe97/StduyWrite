---
title: hub-lab — 연동 허브 학습 인덱스
tags: [moc, study-index, lab, spring, integration, transaction]
status: draft
source:
  - ~/study/hub-lab  # 코드·로드맵·결정 기록 (로컬)
related:
  - ./STATE.md
  - ../../README.md
  - ../gateway-lab/README.md
updated: 2026-09-26
---

# hub-lab — 연동 허브 학습 인덱스

두 외부 시스템 사이에서 요청을 옮기는 허브를 Spring Boot 위에 단계별로 지으며 경계 설계·연동·트랜잭션·동시성의 실패를 재현하고 고치는 랩의 학습 문서 모음입니다. 코드와 로드맵은 `~/study/hub-lab` 에 있습니다. 여기에는 Phase 별 학습 문서와 학습 상태만 둡니다. 진행은 `/learning-session hub-lab` 으로 엽니다.

## 어떻게 진행하는가

허브 랩 Phase 하나가 학습 토픽 하나입니다. 각 토픽을 4-Phase 로 돕니다. 개념 이해에서 그 Phase 가 막으려는 실패를 자기 말로 세우고 학습 문서에 적습니다. 실습에서는 AI 가 쓴 코드로 재현 실험과 해결 실험을 짝으로 돌립니다. 검증은 독립 자답으로 닫습니다. 완료 기준은 저장소 로드맵의 "빌드·테스트·이해 확인" 세 항목이며, 검증 Phase 가 세 번째 항목입니다.

학습 로드맵은 `~/study/hub-lab/docs/01-01.hub-lab-roadmap.md`, Phase 설명은 같은 폴더의 `02-01`·`02-02` 입니다. 범위와 스택을 정한 이유는 `04-01.hub-lab-decision-log.md` 에 있습니다.



## Phase 와 문서

| Phase | 학습 질문 | 문서 | 상태 |
|---|---|---|---|
| 1 포트와 어댑터 | 외부 시스템이 바뀌어도 코어가 그대로이려면 경계를 어떤 단위로 긋는가 | (Phase 2 에서 작성) | 시작 전 |
| 2 외부 API 클라이언트 | 공통 헤더·오류 분류·타임아웃을 한곳에 모으고, 시간 초과를 따로 나누는 이유 | | |
| 3 다중 데이터소스 | 라우팅 데이터소스가 트랜잭션 시작 시점에 연결을 고정하면 무엇이 깨지는가 | | |
| 4 쓰기 정합성 | 외부 호출과 DB 쓰기가 어긋나지 않게 하는 Outbox 와 멱등키 | | |
| 5 분산 락 | 서버가 둘일 때 배치를 한 번만 돌리는 잠금과 그 만료 | | |
| 6 설정 기반 정책 | 규칙 값을 코드 밖으로 빼고 잘못된 값을 기동 단계에서 막는 법 | | |
| 7 인증 위임 | 허브가 아무 사용자나 흉내 내지 못하게 서비스 인증과 사용자 식별을 나누는 법 | | |

선택 Phase 둘(S1 게이트웨이 연동, S2 WAR·오프라인 빌드)은 표에 두지 않았습니다. 진행하면 그때 행을 추가합니다. S1 은 [gateway-lab](../gateway-lab/README.md) 이 Phase 2 이상 진행된 뒤에 합니다.



## 기존 노트와의 관계

gateway-lab 과 달리 hub-lab 은 기존 노트를 흡수하지 않습니다. 겹치는 노트는 대부분 개념을 정리한 final 문서라서, 랩 문서는 그 개념을 다시 쓰지 않고 링크로 참조합니다. 랩 문서에는 재현·해결 실험에서 관찰한 것과 현행 시스템과의 대응만 적습니다.

| Phase | 먼저 읽을 기존 노트 | 랩 문서가 더하는 것 |
|---|---|---|
| 1 | `09_spring/04_testing/02-03` ArchUnit 으로 아키텍처 가드레일 | 질문 단위 포트, 어댑터를 프로파일로 교체하는 실험 |
| 2 | `09_spring/03_network/feign/01-03` 에러 모델, `01-05` @HttpExchange·RestClient, `04_testing/02-04` WireMock | 오류를 코어 예외로 분류하는 핸들러, 지연·실패 주입 실험 |
| 3 | `05_data/03_persistence/jpa/04-01` 스프링 트랜잭션, `04_testing/02-01` Testcontainers | 라우팅 데이터소스의 연결 고정 재현, 데이터소스별 트랜잭션 매니저 |
| 4 | `04_messaging/05_ConsistencyPattern/02-01` Outbox, `03-02` Inbox 와 멱등 어댑터 | 메시지 브로커 없이 외부 HTTP 호출에 Outbox 를 거는 경우 |
| 5 | `09_spring/05_aop/01-02` 스프링 스케줄링, `05_data/03_persistence/jpa/04-02` 낙관적·비관적 락 | 인스턴스 둘의 중복 실행 재현, 조건부 UPDATE 잠금과 만료 |
| 6 | `09_spring/07_autoconfig/02-02` @ConfigurationProperties, `02-03` 프로필 | 기동 시 검증(fail-fast), 설정 소스를 모르는 정책 객체 |
| 7 | `99_ETC/security/01_concepts/2026-05-29_OAuth2와 OIDC` | 공유 키 대리 발급 재현, 서명된 사용자 식별 |

실험 중 기존 노트의 설명이 틀렸거나 빠진 것을 발견하면, 랩 문서가 아니라 그 노트를 고칩니다. 개념의 정본은 한곳에만 둡니다.



## 참고

- 학습 상태: [STATE.md](./STATE.md)
- 같은 리듬의 짝 랩: [gateway-lab](../gateway-lab/README.md)
