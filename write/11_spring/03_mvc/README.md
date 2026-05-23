---
title: Spring MVC 학습 MOC
tags: [moc, spring, spring-boot, spring-mvc, dispatcher-servlet, front-controller, mvc]
status: draft
related:
  - ../README.md
  - ../02_servlet/README.md
  - ../08_exception-handling/README.md
updated: 2026-05-23
---

# Spring MVC 학습 MOC
---

> Spring MVC 의 핵심은 `DispatcherServlet` 한 클래스에 압축되어 있고, 그 클래스의 모든 부품은 FrontController 패턴이 V1 부터 V5 까지 진화하면서 만든 압력으로 설명됩니다. 본 폴더는 그 진화 과정과 도착점을 따라가도록 묶입니다.

## 왜 별도 묶음인가

`02_servlet/` 까지는 "한 서블릿이 한 URL 을 처리한다" 라는 1:1 모델이 통합니다. 그러나 컨트롤러가 늘어나면 동일한 보일러플레이트가 모든 컨트롤러에 반복되고, 그 반복을 앞단에서 한 번에 처리하려는 욕구가 FrontController 패턴과 Spring MVC 의 출발점이 됩니다.

본 폴더는 그 출발점부터 종착점인 `DispatcherServlet` 까지를 한 흐름으로 묶습니다. "MVC 패턴이 왜 필요한가" 에서 "왜 `DispatcherServlet` 이 그 모양인가" 까지를 한 편 안에서 답하는 것이 목표입니다.

## 학습 순서

> 1편(현재)이 Spring MVC 전체를 한 흐름으로 압축합니다. 후속 편은 노션 raw 가 재작성되는 대로 추가됩니다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [Spring MVC — FrontController에서 DispatcherServlet까지](01-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) | MVC 등장, FrontController V1~V5 진화, DispatcherServlet 8단계, HandlerMapping/Adapter/ViewResolver, Controller 인터페이스 vs `@Controller`, PRG 패턴 |

처음 보는 학습자는 1편을 순서대로 따라가면 됩니다. Servlet 만 써 본 사람이라면 1편 §2 (MVC 패턴의 한계) 부터, FrontController 패턴은 들어 봤는데 흐름이 안 그려진다면 §3 (V1~V5) 부터 진입하는 편이 빠릅니다. `@Controller` / `@RequestMapping` 만 익숙한 입장이라면 §4 (DispatcherServlet) 와 §5 (세 인터페이스) 를 먼저 본 뒤 §3 로 되돌아가 부품 이름의 출처를 확인하는 경로가 잘 맞습니다.

## 환경과 버전

> 본 묶음의 코드 예제는 다음 조합을 기준으로 합니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Framework | 6.2.x | `DispatcherServlet`, `HandlerMapping`, `HandlerAdapter` 인터페이스 동일 |
| Spring Boot | 3.3.x | `DispatcherServlet` 을 `AutoConfiguration` 으로 자동 등록 |
| Java | 17+ | `jakarta.servlet.*` 네임스페이스 사용 |
| Servlet API | 5.0+ | `javax.servlet.*` 미사용 |
| JSP / View | JSP + `InternalResourceViewResolver` | Thymeleaf 환경이면 `ThymeleafViewResolver` 자동 등록 |

레거시 `web.xml` 기반 예제는 별도 표기합니다. Boot 환경에서는 동등한 자동 설정이 무엇인지를 본문에 함께 명시합니다.

## 사전 지식

> 본 묶음은 다음을 안다고 가정합니다.

1. Servlet 의 `service()` / `doGet()` / `doPost()` 가 어떤 순서로 호출되는지 한 문장으로 말할 수 있습니다.
2. `HttpServletRequest.setAttribute()` / `getAttribute()` 와 `RequestDispatcher.forward()` 가 어떻게 데이터를 다음 자원으로 넘기는지 압니다.
3. `web.xml` 의 `<servlet>` / `<servlet-mapping>` 이 어떤 역할인지 압니다(Spring Boot 환경이라면 `AutoConfiguration` 으로 대체된다는 사실까지 알면 충분합니다).
4. JSP 가 서버에서 어떻게 렌더링되어 HTML 로 응답되는지 압니다.

위 항목 중 막히는 부분이 있다면 [`../02_servlet/`](../02_servlet/) 을 먼저 읽고 돌아오는 편이 빠릅니다.

## 면접 대비 체크리스트

> 1편을 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. MVC 패턴이 등장한 이유와 MVC 패턴 1 / 2 의 차이는 무엇입니까?
2. MVC 패턴 적용 후에도 남은 4가지 중복은 무엇입니까? 그중 어느 하나가 FrontController 도입의 직접 원인입니까?
3. FrontController V1 → V2 → V3 → V4 → V5 각 단계가 직전 단계의 어떤 한계를 풀었습니까?
4. V5 의 `HandlerMapping`, `HandlerAdapter`, `MyView`, `ModelView`, `ViewResolver` 가 Spring MVC 의 어떤 부품에 각각 대응됩니까?
5. `DispatcherServlet.doDispatch()` 의 8단계를 순서대로 말할 수 있습니까?
6. `org.springframework.web.servlet.mvc.Controller` 인터페이스 구현체와 `@Controller` 어노테이션 기반 컨트롤러는 각각 어떤 `HandlerMapping` / `HandlerAdapter` 를 사용합니까?
7. `InternalResourceView` 가 다른 View 와 다르게 `forward()` 를 거치는 이유는 무엇입니까?
8. PRG 패턴이 풀고자 한 문제와 `RedirectAttributes` 가 단순 문자열 연결 대신 필요한 이유는 무엇입니까?

각 질문에 막히면 1편 본문의 해당 절(§2 ~ §6) 로 돌아갑니다.

## 후속 편 예정

> 노션 raw 가 재작성되면 본 표에 행이 추가됩니다.

- `@ControllerAdvice` / `@ExceptionHandler` — `DispatcherServlet` 흐름의 예외 경로 ([`../08_exception-handling/`](../08_exception-handling/) 와 교차 인용)
- 메시지 컨버터 (`HttpMessageConverter`) — `@RequestBody` / `@ResponseBody` 가 JSON 으로 변환되는 위치
- 인터셉터 / 필터 — `DispatcherServlet` 앞단과 안쪽에서 공통 처리가 끼어드는 지점
- 정적 리소스 매핑 — `ResourceHandlerRegistry` 와 기본 핸들러

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [`../02_servlet/`](../02_servlet/) — Servlet 기초, WAS / Servlet Container, `HttpServletRequest`/`Response`
- [`../08_exception-handling/`](../08_exception-handling/) — `DispatcherServlet` 흐름 안에서 예외가 잡히는 위치(`@ControllerAdvice`, `HandlerExceptionResolver`)
- [Spring Framework Reference — Web MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html) — 공식 문서 진입점
- [Spring Framework Reference — DispatcherServlet](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet.html) — 본 묶음의 핵심 부품에 대한 공식 레퍼런스
