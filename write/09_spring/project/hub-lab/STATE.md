---
topic: hub-lab
scope: durable
level: 기본
last_verified:
blocked_count: 0
next_lesson: "Phase 1 개념 이해 — 포트와 어댑터, 충돌방지계층(ACL), 질문 단위 포트. 외부 이름이 코어에 새면 무엇이 깨지는지 자기 말로"
updated: 2026-09-26
---

# hub-lab 학습 상태

## 미션 — 왜 이걸 배우는가

트럼본 HUB를 분석해 보니 문제는 대부분 기능이 아니라 경계에서 났다. 외부 시스템 이름이 코어에 박혀 있고, 데이터소스가 여럿인데 트랜잭션은 하나만 지키고, 외부 호출과 DB 쓰기가 어긋나고, 서버가 둘이면 배치가 두 번 돈다. 이 실패를 작은 허브 위에서 **직접 재현하고 표준 해법으로 고쳐** 재구축 설계를 손으로 익히는 것이 미션이다. 업무 도메인 복제가 아니라 경계 설계 습득이다.

## 진행 구조

허브 랩 Phase 하나 = 학습 토픽 하나. 각 Phase 안을 4-Phase(개념 이해 → 학습 문서 → 실습 → 검증)로 돈다. 실습은 늘 재현 실험과 해결 실험이 짝이다. 코드는 `~/study/hub-lab`, 학습 로드맵은 그 저장소의 `docs/01-01.hub-lab-roadmap.md`(Phase 설명은 02-01·02-02), 범위·결정은 `docs/04-01.hub-lab-decision-log.md` 가 기준이고, 바로 다음 Phase 의 상세는 `docs/03-NN.hub-lab-phase<N>-plan.md` 다. 이 폴더에는 Phase 별 학습 문서와 이 상태 파일만 둔다.

| 허브 랩 Phase | 학습 문서 (Phase 2 산출) | 4-Phase 진행 | 검증일 |
|---|---|---|---|
| 1 포트와 어댑터 | (미작성) | 개념 이해 전 | |
| 2 외부 API 클라이언트 | | | |
| 3 다중 데이터소스 | | | |
| 4 쓰기 정합성 | | | |
| 5 분산 락 | | | |
| 6 설정 기반 정책 | | | |
| 7 인증 위임 | | | |

## 현재 난이도 레벨

기본. Spring·JPA·트랜잭션 기본은 익숙하다. 헥사고날·ArchUnit은 노트로 봤고, Outbox·분산 락·토큰 교환은 개념만 안다.

## 이해 근거 (선택)

- (시작 전)

## 막힌 지점

- (없음 — 시작 전)

## 미해결 질문

- ShedLock·Testcontainers·WireMock이 Spring Boot 4.1.1과 Java 25에서 문제없이 도는가. 해당 Phase 직전에 확인한다.

## 다음 레슨 후보 + 고른 이유

- Phase 1 개념 이해. 포트 구조가 서야 Phase 2~4를 어댑터 쪽에서만 풀 수 있다. 코드 전에 "코어가 외부 이름을 모르게 한다"는 말이 무엇을 막는지 설명할 수 있어야 한다.

## 물어볼 곳

- Spring Framework 레퍼런스 (https://docs.spring.io/spring-framework/reference/) — RestClient·트랜잭션 매니저 동작이 기대와 다를 때.
