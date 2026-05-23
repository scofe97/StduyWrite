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

| 폴더 | 시리즈 | .md 수 | 자산 폴더 수 |
|------|--------|-------|------------|
| `study/` | `[Spring Study]` — Spring 본질 이론(IoC/DI, MVC, AOP, 예외처리) | 51 | 45 |
| `security/` | `[Spring Security]` — 인증·OAuth2·JWT | 9 | 7 |
| `msa/` | `[Spring MSA]` — Actuator/Cloud Config/Eureka/Kafka/DDD | 30 | 26 |
| `netty/` | `[Spring Netty]` — Reactor Netty, 채널 파이프라인, NIO | 10 | 7 |
| `websocket/` | `[Spring WebSocket]` — STOMP, SSE | 7 | 6 |
| `tdd/` | `[Spring TDD]` — JUnit/Mockito, 테스트 격리 | 6 | 5 |
| `_unsorted/` | 분류 보류 — 카프카 1/2, 이벤트 소싱, 게시판 진화, 도메인 서적 등 | 22 | 8 |
|      | **합계** | **135** | **104** |

## 정식 카테고리 이관 매핑

후속 세션에서 각 시리즈를 다음 정식 위치로 흡수한다. 본 매핑은 정보용이며, 실제 이관은 시리즈별 풀 재작성 단계에서 진행한다.

| raw 시리즈 | 정착 카테고리 | 비고 |
|-----------|--------------|------|
| `study/` 01-* (스프링 역사, OOP/SOLID, DI/IoC) | `11_spring/01_container/` (신설) | 본 README 와 같은 세션의 1편 재작성 대상 |
| `study/` 02-* (WAS, Servlet, Cookie/Session) | `11_spring/02_servlet/` (신설 예정) | |
| `study/` 04-* (MVC, FrontController) | `11_spring/03_mvc/` (신설 예정) | |
| `study/` 05-* (HTTP 어노테이션, Converter, Validation, 파일 업로드) | `11_spring/03_mvc/` 또는 `04_data-binding/` | |
| `study/` 06-* (Validation, Bean Validation) | `11_spring/03_mvc/` 또는 `04_data-binding/` | |
| `study/` 07-* (예외 처리) | `11_spring/08_exception-handling/` (신설 예정) | |
| `study/` 08-* / 09-* (필터/인터셉터, AOP, Pointcut/Advice) | `11_spring/06_aop/` (신설 예정) | |
| `security/` | `10_security/02_spring-security/` | 기존 폴더와 합류 |
| `msa/` 05-* (Hexagonal, DDD, Aggregate) | `03_architecture/03_ddd/` | 기존 `02-03.헥사고날 아키텍처.md` 와 인접 |
| `msa/` xx-Kafka, xx-CQRS | `04_messaging/spring/` | |
| `msa/` 02-* (Cloud Config) / 03-* (Actuator) | `11_spring/` 또는 `06_observability/` | |
| `msa/` 04-* (OpenFeign, Eureka, Gateway) | `11_spring/` 신규 또는 `04_messaging/spring/` | |
| `netty/` | `11_spring/06_reactive-net/` (신설 예정) | `04_webflux/` 와 인접 |
| `websocket/` | `11_spring/09_websocket/` (신설 예정) | |
| `tdd/` | `11_spring/05_testing/` 보완 | 기존 폴더와 합류 |
| `_unsorted/` | 사용자 검토 후 분류 또는 폐기 | 카프카 메모는 `04_messaging/` 후보 |

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

## 작업 규약

- 본 영역의 `.md` 본문은 **수정 금지**. 노션 마크업(`<aside>`, `![...](폴더/...)`) 을 그대로 둔다. 재작성은 정식 폴더의 신규 파일에서만 진행한다. (`feedback_learning_doc_body_immutable`)
- 이관 시 파일명에서 32자 hex hash 접미사만 제거. 동명 자산 폴더도 같은 규칙으로 rename 하여 마크다운 상대경로가 깨지지 않도록 한다.
- 재작성 산출물은 `_meta/conventions.md` 의 프론트매터 5필드(title, tags, status, related, updated) 와 파일명 컨벤션 `NN-MM.제목.md` 를 지킨다.
- 재작성 시 노션 원본의 코드 스니펫·URL·인용은 사실 변경 금지(`feedback_learning_doc_body_immutable`). 단, 노션 위젯(`<aside>`) 은 산문으로 풀고 어미는 한 톤으로 통일한다.
