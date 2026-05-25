---
title: Spring Core 학습 MOC
tags: [moc, spring, spring-boot, ioc, di, container, servlet, mvc]
status: draft
related:
  - ../README.md
  - ../02_data-binding/README.md
  - ../05_aop/README.md
updated: 2026-05-24
---

# Spring Core 학습 MOC
---

> Spring 프레임워크의 토대 세 가지 — IoC 컨테이너, 서블릿/WAS, MVC — 를 한 폴더에 모았습니다. 컨테이너가 객체를 만들어 주입하고(01장), 그 객체들이 서블릿 컨테이너 위에서 HTTP 요청을 받고(02장), DispatcherServlet 이 요청을 컨트롤러로 분배하는(03장) 흐름이 Spring 애플리케이션의 척추입니다. 본 묶음을 끝내면 "요청 한 건이 톰캣 소켓에서 시작해 내 컨트롤러 메서드까지 어떻게 도달하고, 그 컨트롤러가 의존하는 빈은 누가 언제 만들어 주입했는가"를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

컨테이너·서블릿·MVC 는 따로 떼면 각각 입문 주제처럼 보이지만, 실제로는 한 요청을 처리하기 위해 맞물려 도는 톱니입니다. `DispatcherServlet` 은 서블릿이면서(02장) 동시에 Spring 빈으로 등록되어 컨테이너의 관리를 받고(01장), 그 안에서 핸들러를 찾아 호출하는 구조가 MVC(03장)입니다. 세 주제를 인접한 장 번호로 두면 "어디까지가 서블릿 표준이고 어디부터가 Spring 의 손길인가"라는 경계가 선명해집니다.

번호는 학습 순서이자 의존 방향입니다. 01장(컨테이너) → 02장(서블릿) → 03장(MVC) 순으로, 앞 장이 뒷 장의 전제가 됩니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 컨테이너 | 01-01 | [객체지향 원리 적용 — DI와 IoC](01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) | AppConfig 등장 배경, IoC 와 DI 의 관계, BeanFactory / ApplicationContext, 빈 등록 세 방식, 생성자 주입 권장 이유, 다중 빈 처리(@Qualifier·@Primary·Map/List), CGLIB 싱글톤 보장, 생명주기 7단계, 스코프 7종과 프록시 |
| 01 컨테이너 | 01-02 | [Spring과 디자인 패턴](01-02.Spring과%20디자인%20패턴.md) | 컨테이너가 구현하는 디자인 패턴 — 싱글톤·프록시·전략·팩토리 등 |
| 02 서블릿 | 02-01 | [WAS와 서블릿 — HTTP 처리의 토대](02-01.WAS와%20서블릿%20—%20HTTP%20처리의%20토대.md) | Web Server vs WAS, 서블릿 표준과 라이프사이클, 멀티 스레드·스레드 풀, 쿠키/세션 |
| 02 서블릿 | 02-02 | [내장 톰캣과 SpringApplication — JAR로 WAS를 품다](02-02.내장%20톰캣과%20SpringApplication%20—%20JAR로%20WAS를%20품다.md) | WAR 배포 단점, 내장 톰캣 원리, SpringApplication.run(), ServletWebServerFactory, 실행 가능 JAR |
| 03 MVC | 03-01 | [Spring MVC — FrontController에서 DispatcherServlet까지](03-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) | MVC 패턴 등장, FrontController V1~V5 진화, DispatcherServlet 8단계, HandlerMapping/Adapter/ViewResolver, Controller 인터페이스 vs @Controller, PRG 패턴 |
| 03 MVC | 03-02 | [예외 처리 — 서블릿에서 @ControllerAdvice까지](03-02.예외%20처리%20—%20서블릿에서%20@ControllerAdvice까지.md) | 서블릿 재디스패치, BasicErrorController, HandlerExceptionResolver 체인 4종, @ExceptionHandler / @ControllerAdvice / @ResponseStatus |

처음 보는 학습자는 01-01 부터 순서대로 따라가면 됩니다. 이미 `@Autowired` 로 빈을 주입받아 본 입장이라면 01장은 빠르게 훑고 02장(서블릿)부터 진입해도 됩니다. `@RestController` 로 API 만 만들어 본 사람이라면 03-01 §4(DispatcherServlet)에서 출발해 03-02(예외 처리)로 이어 본 뒤, 부품 이름의 출처가 궁금할 때 02장과 03장 §3(FrontController)으로 거슬러 올라가는 경로가 빠릅니다.

03-02(예외 처리)는 03-01 의 `DispatcherServlet.doDispatch()` 가 예외를 만났을 때 어디로 흐르는지를 이어 받습니다. `doDispatch` 안의 `processDispatchResult` 가 `HandlerExceptionResolver` 체인을 호출하는 자리가 출발점이므로, 03-01 §4 를 먼저 본 뒤 03-02 로 넘어가는 순서가 자연스럽습니다.

## 환경과 버전

> 본 묶음의 코드 예제는 다음 조합을 기준으로 합니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Framework | 6.2.x | `ApplicationContext`, `DispatcherServlet`, `HandlerMapping` 인터페이스 동일 |
| Spring Boot | 3.3.x | `DispatcherServlet` 을 `AutoConfiguration` 으로 자동 등록 |
| Java | 17+ | `jakarta.servlet.*` 네임스페이스 사용 |
| Servlet API | 5.0+ | `javax.servlet.*` 미사용 |

## 면접 대비 체크리스트

> 세 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. IoC 와 DI 는 어떤 층위에서 다른 개념입니까? 생성자 주입을 권장하는 네 가지 이유는?
2. `@Configuration` 이 CGLIB 프록시로 싱글톤을 보장하는 메커니즘은? 빈 생명주기 7단계를 순서대로 말할 수 있습니까?
3. Web Server 와 WAS 를 분리하는 이유는? 서블릿 컨테이너가 요청을 스레드 풀로 받아 우리 코드까지 전달하는 5단계는?
4. FrontController V1 → V5 각 단계가 직전의 어떤 한계를 풀었습니까? V5 의 부품이 Spring MVC 의 무엇에 대응됩니까?
5. `DispatcherServlet.doDispatch()` 의 8단계는? `HandlerExceptionResolver` 가 끼어드는 자리는 그중 어디입니까?
6. `@ExceptionHandler` 와 `@ControllerAdvice` 의 차이는? `@RestControllerAdvice` 가 따로 있는 이유는?

각 질문에 막히면 해당 장의 본문으로 돌아갑니다.

## 원본 학습 자료

본 묶음은 노션 학습 노트(`_notion_import/study/`)를 통합 재작성한 산출물입니다. 원본 study 시리즈는 재작성 완료 후 제거됐고, 재작성 이력은 [`_notion_import/README.md`](../_notion_import/README.md) 의 진척표에 있습니다.

## 후속 묶음

- [`../02_data-binding/`](../02_data-binding/) — HTTP 요청·응답·메시지 컨버터·Validation. MVC 가 받은 요청 본문을 객체로 바인딩하는 다음 단계
- [`../05_aop/`](../05_aop/) — 횡단 관심사·프록시·@Aspect. 01장의 CGLIB 프록시가 AOP 프록시로 확장되는 흐름

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [Spring Framework Reference — Core](https://docs.spring.io/spring-framework/reference/core.html) — IoC 컨테이너 공식 문서
- [Spring Framework Reference — Web MVC](https://docs.spring.io/spring-framework/reference/web/webmvc.html) — MVC 공식 문서
