---
title: Spring Servlet 학습 MOC
tags: [moc, spring, spring-boot, servlet, was, tomcat, http]
status: draft
source:
  - https://docs.oracle.com/javaee/7/api/javax/servlet/Servlet.html
  - https://tomcat.apache.org/tomcat-10.1-doc/
  - https://jakarta.ee/specifications/servlet/
related:
  - ../README.md
  - ../03_mvc/01-01.Spring MVC — FrontController에서 DispatcherServlet까지.md
updated: 2026-05-23
---

# Spring Servlet 학습 MOC

---

> 스프링의 모든 HTTP 처리는 결국 톰캣이 받은 소켓 한 건을 서블릿 컨테이너가 풀에서 꺼낸 스레드에 실어 우리 코드까지 가져다 주는 흐름 위에 올라가 있습니다. 이 토대를 한 편에 묶어 정리한 묶음이며, 스프링 MVC 묶음으로 넘어가기 전 마지막 토대 정리 문서로 읽으면 됩니다.

## 왜 별도 묶음인가

> 스프링 부트를 처음 잡으면 `@RestController` 한 줄로 응답이 나가니까, 그 아래에 톰캣·서블릿·스레드 풀·세션이 깔려 있다는 사실이 가려집니다. 이 묶음은 그 가려진 토대를 다시 드러내, 컨트롤러 메서드의 동시성 주의점이나 세션 사용 시 트레이드오프를 스스로 설명할 수 있게 만드는 것을 목표로 합니다.

본 묶음의 1편은 다섯 주제(WAS의 등장, Servlet API, 멀티 스레드, 톰캣 스레드 풀, 쿠키와 세션)를 한 흐름으로 이어 붙였습니다. 순수 Socket으로 HTTP를 직접 짜 본 다음에 서블릿 API가 어떤 비용을 떼어 가는지 체감하는 흐름이며, 마지막에 `HttpSession`과 `@SessionAttribute`까지 풀어내 다음 묶음(MVC)에서 바로 컨트롤러 입력으로 받아 쓸 수 있게 합니다.

## 학습 순서

> 1편을 다 읽으면 03_mvc 묶음의 FrontController·DispatcherServlet 흐름이 자연스럽게 이어집니다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [WAS와 서블릿 — HTTP 처리의 토대](01-01.WAS와%20서블릿%20—%20HTTP%20처리의%20토대.md) | WAS 등장 배경, Web Server 분리 이유, Socket 직접 구현의 통증, Servlet API/컨테이너/라이프사이클, `HttpServletRequest`/`HttpServletResponse`, 1요청=1스레드와 톰캣 스레드 풀, `maxThreads` 튜닝, 쿠키/세션/`HttpSession`/`@SessionAttribute` |

처음 보는 학습자는 01-01부터 순서대로 보시면 됩니다. 컨트롤러는 짜 봤지만 동시성 주의점이 헷갈리는 분은 4장(멀티 스레드)부터, 로그인 구현 중이라면 5장(쿠키/세션)부터 진입해도 흐름이 끊기지 않게 구성했습니다.

## 환경과 버전

> 본문 코드 예시는 다음 환경 기준으로 검증 가능합니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | 임베디드 톰캣 기준 |
| Spring Framework | 6.2.x | `@WebServlet`/`@WebListener` 어노테이션 동작 |
| Java | 17+ | 21까지 호환 |
| Tomcat | 10.1.x | Jakarta Servlet 6.0 |
| Servlet API | jakarta.servlet.* | `javax.servlet` 미사용 |

3.x 이전 환경에서는 `javax.servlet` 네임스페이스를 그대로 쓰면 됩니다. 본문은 노션 원본 코드를 사실 그대로 인용하므로 일부 예시는 `javax`/`jakarta` 양쪽 표기가 섞일 수 있는데, 동작 의미는 동일합니다.

## 사전 지식

> 이 묶음은 다음을 알고 있다고 가정합니다.

1. HTTP 요청과 응답의 기본 구조(메서드, URI, 헤더, 바디)를 한 문장으로 설명할 수 있습니다.
2. 스프링 부트 프로젝트에 `spring-boot-starter-web` 의존성을 추가하고 `@RestController`로 간단한 엔드포인트를 노출해 본 경험이 있습니다.
3. 스레드와 동시성의 기본 개념(공유 상태가 race condition을 일으킬 수 있다는 점)에 익숙합니다.

위 항목 중 막히는 부분이 있다면 [`../README.md`](../README.md)의 학습 경로 추천에서 진입점을 다시 고르는 편이 빠릅니다.

## 다음 묶음 예정

- **03_mvc**: FrontController 패턴이 V1→V5로 진화하며 DispatcherServlet에 이르는 흐름. 본 묶음 3장의 `@WebServlet`을 한 단계 추상화한 결과물입니다.
- **08_exception-handling**: 서블릿 예외 흐름(WAS의 ErrorPage)과 스프링 예외 처리(`@ControllerAdvice`)의 비교.

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [Spring WebClient 학습 MOC](../04_webflux/README.md) — 같은 묶음 형태의 톤·구조 모델
- [Apache Tomcat 10.1 Documentation](https://tomcat.apache.org/tomcat-10.1-doc/) — `Connector`/`Executor` 설정과 스레드 풀 튜닝 1차 자료
- [Jakarta Servlet Specification](https://jakarta.ee/specifications/servlet/) — Servlet API 공식 명세
