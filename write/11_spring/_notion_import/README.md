---
title: 노션 import raw 보관소
tags: [meta, notion-import, spring]
status: draft
related:
  - ../README.md
  - ../../STUDY_INDEX.md
updated: 2026-05-23
---

# 노션 import raw 보관소
---
> 2026-05-23 노션에서 export 한 "기술 블로그/공부 데이터베이스" 135개 마크다운을 시리즈별로 보관한 raw 영역이다. 본문은 그대로 두고, 파일명과 동명 자산 폴더에서 32자 hex hash 접미사만 제거했다. 컨벤션상 정식 폴더가 아니므로 `_` prefix 를 붙였다. 재작성을 통해 카테고리별 정식 문서로 흡수되는 과정이 끝나면 폐기 또는 archive 로 옮긴다.

## 왜 별도 영역인가

write/ 컨벤션(`_meta/conventions.md`)은 `NN-MM.제목.md` 형식과 프론트매터 5필드를 강제한다. 노션 export 는 둘 다 만족하지 못한다 — 파일명 끝에 hash 가 붙고, 본문은 `<aside>💡 NOTE` 같은 노션 위젯 마크업으로 채워져 있다. 이를 정식 카테고리에 바로 푸는 대신 한 번 raw 로 받은 뒤 1편씩 재작성하는 흐름을 둔다. `feedback_12spring_full_rewrite_cadence` 원칙대로 풀 재작성은 1편/세션으로 제한한다.

## 디렉토리 구성

> 2026-05-24 이관 완료분 삭제 반영. 최초 수입 135개 중 study 01~09 시리즈(이전 세션)와 security·tdd·msa DDD/Kafka·_unsorted 중복분(2026-05-24)이 정식 문서로 흡수되어 제거됐다. 아래는 *보존 중인 미이관* 분량이다.

| 폴더 | 시리즈 | 현재 .md 수 | 상태 |
|------|--------|------------|------|
| `study/` | `[Spring Study]` — LDAP·Node.js·yaml·Swagger·JASYPT·00 인덱스 | 6 | 01~09 본질 이론 이관 완료, 부록 xx만 잔존 |
| `msa/` | `[Spring MSA]` — Cloud Config·Actuator·OpenFeign/Eureka/Gateway·모니터링·00 인덱스 | 14 | DDD/Kafka 이관 완료, 부트설정·모니터링 미이관 |
| `netty/` | `[Spring Netty]` — Reactor Netty, 채널 파이프라인, NIO | 10 | 01 이관 완료(2026-05-30 → `03_network/reactive-net/01-01`), 나머지 9편 이관 예정 |
| `websocket/` | `[Spring WebSocket]` — STOMP, SSE | 7 | 미이관, `03_network/websocket/` 폴더·README 예약 완료(2026-05-30), 본문 7편 이관 예정 |
| `_unsorted/` | 복원력·패키지 구조·실용주의(2) | 4 | 이벤트 리스너 4편 이관 완료(2026-05-24 → `06_events/`), DDD/카프카/MSA 중복분 제거 |
|      | **합계 (보존)** | **41** | security·tdd 폴더 전체 삭제됨 |

## 정식 카테고리 이관 매핑

후속 세션에서 각 시리즈를 다음 정식 위치로 흡수한다. 본 매핑은 정보용이며, 실제 이관은 시리즈별 풀 재작성 단계에서 진행한다.

| raw 시리즈 | 정착 카테고리 | 상태 |
|-----------|--------------|------|
| `study/` 01-* (스프링 역사, OOP/SOLID, DI/IoC) | `11_spring/01_container/` | ✅ 이관·삭제 완료 |
| `study/` 02-* (WAS, Servlet, Cookie/Session) | `11_spring/02_servlet/` | ✅ 이관·삭제 완료 |
| `study/` 04-* (MVC, FrontController) | `11_spring/03_mvc/` | ✅ 이관·삭제 완료 |
| `study/` 05-* (HTTP 어노테이션, Converter, Validation, 파일 업로드) | `11_spring/04_data-binding/` | ✅ 이관·삭제 완료 |
| `study/` 06-* (Validation, Bean Validation) | `11_spring/04_data-binding/` | ✅ 이관·삭제 완료 |
| `study/` 07-* (예외 처리) | `11_spring/03_mvc/02-01` | ✅ 이관·삭제 완료 (08_exception-handling 은 2026-05-24 03_mvc 로 통합) |
| `study/` 08-* / 09-* (필터/인터셉터, AOP, Pointcut/Advice) | `11_spring/06_aop/` | ✅ 이관·삭제 완료 |
| `security/` | `10_security/02_spring-security/` | ✅ 이관·삭제 완료 (폴더 전체 삭제) |
| `tdd/` | `11_spring/05_testing/` | ✅ 이관·삭제 완료 (폴더 전체 삭제) |
| `msa/` 05-* (Hexagonal, DDD, Aggregate) | `03_architecture/04_ddd/` | ✅ 주제 중복 삭제 완료 |
| `msa/` xx-Kafka, xx-CQRS, 멀티모듈 | `04_messaging/`, `03_architecture/` | ✅ 주제 중복 삭제 완료 |
| `msa/` 01-1 (모놀리틱 vs MSA) | `03_architecture/03_distributed/` | ✅ 주제 중복 삭제 완료 |
| `msa/` 02-* (Cloud Config) / 03-* (Actuator) / xx 모니터링 | `06_observability/05_SpringActuator/` (신설 예정) | ⏸ 미이관 — boot zip 과 동일 주제, 함께 source |
| `msa/` 04-* (OpenFeign, Eureka, Gateway) | `11_spring/` 신규 또는 `04_messaging/` | ⏸ 미이관 |
| `msa/` 00 학습내용 | — | ⏸ 보존 (남은 미이관 노트의 시리즈 인덱스) |
| `netty/` | `11_spring/03_network/reactive-net/` | 01 이관 완료(2026-05-30), 나머지 9편 보존 |
| `websocket/` | `11_spring/03_network/websocket/` | 폴더·README 예약(2026-05-30), 본문 7편 보존 |
| `study/` xx (LDAP·Node.js·yaml·Swagger·JASYPT) | 단편 부록 (분류 보류) | ⏸ 미이관 |
| `_unsorted/` 이벤트 리스너 1~3 + 스프링 이벤트 동기/비동기 | `11_spring/06_events/` (신설) | ✅ 이관·삭제 완료 (2026-05-24, 4편 묶음) |
| `_unsorted/` 복원력·패키지 구조·실용주의(2) | `05_aop/` 또는 신규 영역 | ⏸ 미이관 — 고유 콘텐츠 보존 |
| `_unsorted/` DDD·이벤트소싱·카프카·마이크로서비스 | `03_architecture/`, `04_messaging/` | ✅ 주제 중복 삭제 완료 |

## 재작성 진척표

풀 재작성이 완료된 묶음만 행을 추가한다. "Source" 는 본 raw 영역의 노트, "Target" 은 정식 폴더의 산출 파일이다.

| 일자 | Target | Source | 상태 |
|------|--------|--------|------|
| 2026-05-23 | `11_spring/01_container/01-01.객체지향 원리 적용 — DI와 IoC.md` | `study/[Spring Study] 01-4 ...`, `study/[Spring Study] 03-1 ~ 03-4` (5편) | draft (어미 합니다체 변환 완료) |
| 2026-05-23 | `11_spring/02_servlet/01-01.WAS와 서블릿 — HTTP 처리의 토대.md` | `study/[Spring Study] 02-1 ~ 02-4` (4편) + 부록 `study/[Spring Study] xx 스프링 부트와 내장 톰캣`, `xx 웹 서버와 서블릿 컨테이너(WAR 배포방식)` | draft |
| 2026-05-23 | `11_spring/03_mvc/01-01.Spring MVC — FrontController에서 DispatcherServlet까지.md` | `study/[Spring Study] 04, 04-1 ~ 04-7` (8편) + 부록 `study/[Spring Study] xx WebMvcConfigurer - CORS 설정` | draft |
| 2026-05-23 | `11_spring/06_aop/01-01.횡단 관심사와 AOP — 프록시로 풀어내기.md` | `study/[Spring Study] 08-1 ~ 08-6, 09-6, 09-7, 09-8, 09-99` (10편) | draft |
| 2026-05-23 | `11_spring/06_aop/01-02.스프링 스케줄링 — @Scheduled에서 Quartz까지.md` | `study/[Spring Study] Xx 스프링 스케줄링` (1편) | draft |
| 2026-05-23 | `11_spring/08_exception-handling/01-01.예외 처리 — 서블릿에서 @ControllerAdvice까지.md` | `study/[Spring Study] 07-1, 07-2` (2편) | draft |
| 2026-05-23 | `11_spring/04_data-binding/01-01.HTTP 요청·응답과 메시지 컨버터.md` | `study/[Spring Study] 05 DTO, 05-1 ~ 05-5` (6편) | draft |
| 2026-05-23 | `11_spring/04_data-binding/01-02.파일 업로드 — Multipart.md` | `study/[Spring Study] 05-xx 파일 업로드` (1편) | draft |
| 2026-05-23 | `11_spring/04_data-binding/02-01.Validation — BindingResult에서 Bean Validation까지.md` | `study/[Spring Study] 06-1, 06-2` (2편) | draft |

## 강의 PDF 기반 신규 작성 대기열

노션 재작성과 별개로, 김영한 인프런 강의 PDF 두 묶음을 source 로 한 신규 작성 계획이 있다. 2026-05-24 커버리지 대조 결과 **basic(스프링 핵심 원리)은 `01_container/01-01` 이 거의 완전히 커버**하지만 **boot(스프링 부트)는 14개 핵심 개념 중 13개가 미커버**다. 설계 전문은 plan 파일 `~/.claude-work/plans/vast-mixing-wozniak.md` 가 SSOT 다.

| 우선순위 | 작성 대상 | source |
|---------|----------|--------|
| 1 | `11_spring/07_autoconfig/01-02.자동 구성 — @AutoConfiguration과 @Conditional.md` (신설) | boot PDF 5장 + `msa/ 02-*` |
| 2 | `07_autoconfig/02-01~02-03.외부 설정·@ConfigurationProperties·프로필` | boot PDF 6·7장 + `msa/ 02-*` |
| 3 | `02_servlet/02-01.내장 톰캣과 SpringApplication` | boot PDF 3장 |
| 4 | `06_observability/05_SpringActuator/01-01~01-03.액츄에이터·마이크로미터·프로메테우스/그라파나` (신설) | boot PDF 8·9·10장 + `msa/ 03-*·xx 모니터링` |
| 5 | `01_container` 분할(01-01 §1~6 / 신규 01-02 빈의 생명) + ComponentScan 필터 보강 | basic PDF 6장 |

boot 신규 작성 시 `msa/ 02-*·03-*·xx 모니터링` 노션 노트가 동일 주제를 다루므로 PDF 와 함께 source 로 쓴다. 따라서 해당 msa 노트는 이관 완료 전까지 보존한다.

## 작업 규약

- 본 영역의 `.md` 본문은 **수정 금지**. 노션 마크업(`<aside>`, `![...](폴더/...)`) 을 그대로 둔다. 재작성은 정식 폴더의 신규 파일에서만 진행한다. (`feedback_learning_doc_body_immutable`)
- 이관 시 파일명에서 32자 hex hash 접미사만 제거. 동명 자산 폴더도 같은 규칙으로 rename 하여 마크다운 상대경로가 깨지지 않도록 한다.
- 재작성 산출물은 `_meta/conventions.md` 의 프론트매터 5필드(title, tags, status, related, updated) 와 파일명 컨벤션 `NN-MM.제목.md` 를 지킨다.
- 재작성 시 노션 원본의 코드 스니펫·URL·인용은 사실 변경 금지(`feedback_learning_doc_body_immutable`). 단, 노션 위젯(`<aside>`) 은 산문으로 풀고 어미는 한 톤으로 통일한다.
