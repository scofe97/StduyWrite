---
title: Spring 예외 처리 학습 MOC
tags: [moc, spring, spring-boot, exception-handling, controller-advice]
status: draft
source:
  - https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-exceptionhandler.html
  - https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/exceptionhandlers.html
related:
  - ../README.md
  - ../03_mvc/01-01.Spring MVC — FrontController에서 DispatcherServlet까지.md
updated: 2026-05-23
---

# Spring 예외 처리 학습 MOC
---

> Spring 의 예외 처리는 서블릿 컨테이너의 재디스패치 흐름 위에 `HandlerExceptionResolver` 체인이 올라가고, 그 위에 다시 `@ExceptionHandler` / `@ControllerAdvice` / `@ResponseStatus` 가 얹혀 있는 구조입니다. 본 묶음은 그 구조를 한 흐름으로 따라가도록 묶었습니다.

## 왜 별도 묶음인가

> 예외 처리는 "에러 분기" 라는 한 가지 관심사가 코드 곳곳에 흩어지기 쉬운 영역입니다. Spring 이 그 분산을 막기 위해 단계별로 어떤 도구를 도입했는지를 한 흐름으로 보지 않으면, 어떤 도구가 어떤 자리를 메우는지 헷갈리기 쉽습니다.

서블릿 표준은 예외 발생 시 `web.xml` 의 `<error-page>` 매핑을 따라 별도 요청을 다시 만들어 오류 페이지로 디스패치합니다. Spring Boot 는 그 매핑을 `WebServerFactoryCustomizer` 와 `ErrorMvcAutoConfiguration` 으로 자동화했고, Spring MVC 는 그 위에 "컨트롤러 안에서 예외를 처리해 정상 응답으로 바꾸는" 진입점 `HandlerExceptionResolver` 를 두었습니다. 이 진입점이 있어서 `@ExceptionHandler`, `@ControllerAdvice`, `@ResponseStatus` 같은 어노테이션이 동작할 자리가 생깁니다.

본 묶음은 이 네 단계 — 서블릿, Spring Boot 자동화, `HandlerExceptionResolver` 체인, 어노테이션 — 를 한 문서에서 차례로 보여 줍니다.

## 학습 순서

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [예외 처리 — 서블릿에서 @ControllerAdvice까지](01-01.예외%20처리%20—%20서블릿에서%20@ControllerAdvice까지.md) | 서블릿 재디스패치, `BasicErrorController`, `HandlerExceptionResolver` 체인 4종, `@ExceptionHandler` / `@ControllerAdvice` / `@ResponseStatus` |

01-01 한 편으로 시작합니다. 추가 편(예: `@Valid` 검증 예외 묶음, 도메인 예외 설계, WebFlux 예외 처리)은 작성 시 본 표에 행을 추가합니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `BasicErrorController`, `ErrorMvcAutoConfiguration` 기준 |
| Spring Framework | 6.2.x | `HandlerExceptionResolver`, `@RestControllerAdvice` |
| Java | 17+ | 21 까지 호환 |
| Jakarta | jakarta.* | 원문 노션 코드의 `javax.servlet.error.*` 상수 키는 호환을 위해 그대로 보존 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. `DispatcherServlet` 이 무엇인지, FrontController 패턴이 왜 등장했는지 한 문장으로 설명할 수 있습니다.
2. 필터와 인터셉터가 어느 시점에 호출되는지 구분할 수 있습니다.
3. `@RestController` 가 `@Controller + @ResponseBody` 라는 점을 압니다.

위 항목 중 막히는 부분이 있다면 [Spring MVC — FrontController에서 DispatcherServlet까지](../03_mvc/01-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) 를 먼저 보고 돌아오는 편이 빠릅니다.

## 면접 대비 체크리스트

> 본 묶음을 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 합니다.

1. 서블릿 컨테이너가 예외를 받았을 때 어떤 흐름으로 오류 페이지를 보여 주는가? 필터와 인터셉터가 중복 호출되는 이유는?
2. Spring Boot 는 어떤 자동 설정으로 오류 페이지 처리를 자동화하는가? `BasicErrorController` 가 응답에 담는 키는?
3. `HandlerExceptionResolver` 의 기본 구현체 4 종과 적용 우선순위는?
4. `@ExceptionHandler` 와 `@ControllerAdvice` 의 차이는? `@RestControllerAdvice` 가 따로 있는 이유는?
5. `@ResponseStatus` 와 `ResponseStatusException` 은 언제 갈리는가? 실무에서 `@ExceptionHandler` 가 가장 많이 쓰이는 이유는?

각 질문에 막히면 01-01 의 해당 절을 다시 봅니다.

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [Spring MVC 01-01](../03_mvc/01-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) — `DispatcherServlet` 의 구조를 먼저 잡고 본 묶음으로 진입
- [Spring Framework Reference — Exception Handling](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/exceptionhandlers.html) — 본 묶음이 따라가는 공식 문서 진입점
