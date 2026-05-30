# Jenkins 실행 엔진 (operator-api · executor · message-lib) — 작업 정리

> 저장소: GitLab `PPP/operator-api`, `PPP/executor`, `PPP/message-lib`
> 기간: 2026-04 ~ 2026-05 · 본인 커밋 약 460건 (operator 213 · executor 194 · message-lib 56)
> 주요 티켓: IGMU-512/540/543/545/596/598/600, IGMU-1039~1060
> 스택: Spring Boot · 헥사고날 아키텍처 · Redpanda(Kafka) · Avro(avdl) · Outbox · QueryDSL · JPA

RESUME.md "Jenkins 파이프라인 실행 엔진" 섹션의 실제 근거 저장소입니다. 외부 시스템(Jenkins)에 강하게 의존하는 모듈을 설계하면서 "외부 장애는 내부 트랜잭션을 잠그면 안 된다", "동시성은 식별 단위에서 봉합한다" 두 원칙을 끝까지 끌고 갔습니다.

---

## executor — UC 기반 실행 엔진

> 2026-04 ~ 2026-05 · 약 194건

Jenkins 호출과 상태 추적을 담당하는 신규 실행 엔진을 유즈케이스(UC) 단위로 구축했습니다. UC01(작업 접수) → UC02(디스패치 평가) → UC03(Jenkins Submit) → UC04(빌드 라이프사이클 감지)를 처음엔 동기 흐름으로 짠 뒤, 이벤트 드리븐(Redpanda Consumer)으로 전환했습니다. UC03 는 config.xml 생성·빌드 트리거·queueId 캡처·재시도를 포함하고, UC04 는 Jenkins webhook 을 받아 상태를 전환합니다. 실행 이력(TB_TPS_EC_002, 이후 TB_TRB prefix 로 정합)을 전 구간 기록합니다.

동시성 제어가 이 모듈의 핵심입니다. Submit 단계에 비관적 락을 걸고, save 후 낙관적 락 버전을 동기화해 StaleObjectStateException 을 막았습니다. SUBMITTING 상태를 도입해 claim/release 로 같은 작업의 중복 디스패치를 직렬화하고, dispatch gate 의 capacity 산출을 초기 "토폴로지 인지" 방식에서 executor-pool free slot 기준으로 단순화했습니다. 외부 장애 대비로는 SUBMITTED 24시간 timeout safety-net(좀비 Job 자동 종료), aged SUBMITTING recovery, Jenkins terminal recovery, cancel command flow, fail reason 코드를 갖췄습니다.

## operator-api — 결재 도메인 헥사고날·DDD

> 2026-04 ~ 2026-05 · 약 213건 · IGMU-512/596/598/600

operator-api 에 결재(AtrzMng/AtrzExcn) 도메인을 신규 구축하면서 헥사고날 아키텍처와 DDD 로 재설계했습니다. 결재 모델을 Aggregate Root + Value Object 로 잡고 invariants 를 엔티티에 흡수했으며(Phase B~N 단계적 진행), Aggregate facade 를 통해서만 상태를 바꾸도록 했습니다.

의존 방향을 Port 로 정리한 것이 특징입니다. inbound port(UseCase 인터페이스)와 outbound port(domain/port/out 의 Read/Write/Allocation Port)를 분리하고, Reader/Writer/IdAllocator 가 Port 를 통해 어댑터에 위임하도록 바꿔 도메인이 영속·인프라를 모르게 했습니다. layer 위반(AtrzMngPort 직접 호출 등)을 정리하고 도메인 단위 테스트를 신설했습니다. CQRS 로 Command 는 JPA Repository, Read 는 QueryDSL 로 나눴습니다.

## message-lib — Outbox 메시징 · Avro 계약

> 2026-04 ~ 2026-05 · 약 56건

executor 와 operator 가 공유하는 Outbox 메시징 라이브러리입니다. Outbox 테이블(TB_TPS_OX_001 → TB_TRB 정합)과 메시지 발행 인프라를 구성하고, JENKINS_EVT_JOB_LIFECYCLE 등 토픽과 두 모듈의 메시지 스키마를 정의했습니다. Avro 계약을 avdl 로 마이그레이션하고 `*Avro` suffix 네이밍 규약을 확립했으며, 이벤트 enum 을 operator job status 코드와 정합시켰습니다. IGMU-1040 의 Outbox 메트릭(published/failed/dead/pending)이 이 라이브러리에서 나옵니다.
