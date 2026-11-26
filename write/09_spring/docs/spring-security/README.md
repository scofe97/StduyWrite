---
title: spring-security — Spring Security 세션·CSRF·로그인 보호 이론 시리즈 학습 지도
tags: [moc, learning, spring-security, tomcat, session, csrf]
status: draft
related:
  - ../../README.md
  - ../../spring-keywords.md
  - ../../../99_ETC/security/01_concepts/README.md
  - ../../../02_os/docs/reverse-proxy/README.md
updated: 2026-11-26
---

# spring-security

---

> 로그인 기능을 직접 구현하다 보면 "지금 요청의 세션과 인증 정보는 누가 어디에 쥐고 있는가"에서 막힙니다. 이 시리즈는 Tomcat 스레드와 필터 체인, 세션 저장소, CSRF 방어, 다중 세션 만료, 로그인 실패 응답과 프록시 신뢰 경계를 다섯 편으로 나눠 설명합니다.

Spring Boot와 Spring Security로 폼 로그인 없는 세션 기반 인증을 직접 조립하다 보면 같은 질문 세 가지에서 자주 막힙니다.

요청 하나가 Tomcat과 Spring 필터 체인을 어떤 순서로 지나는가, 세션 쿠키와 CSRF 토큰은 어디에 저장되고 언제 지워지는가, 로그인 실패 응답과 프록시 뒤 클라이언트 IP는 어떻게 다루어야 정보가 새지 않는가 하는 질문입니다.

세 질문은 어느 Spring 웹 앱에서나 똑같이 생깁니다. 이 시리즈는 Spring Security 7.1.x와 Tomcat 11.0.x의 공식 문서·소스 근거로 다섯 편을 묶었습니다.



## 읽는 순서

> 앞 편이 다음 편의 실행 구조와 저장소를 세우므로 01-01 편부터 차례로 읽는 것을 권합니다.

| 편 | 이 편이 답하는 질문 | 핵심 개념 |
|---|---|---|
| [01-01 Tomcat과 Spring의 관계](./01-01.Tomcat%20NIO·FilterChainProxy·DispatcherServlet.md) | 요청 하나가 Tomcat에서 컨트롤러까지 어떤 스레드와 필터를 지나며, 연결·세션·인증은 각각 누가 쥐는가? | Tomcat NIO, 서블릿 필터, FilterChainProxy, DispatcherServlet, SecurityContextHolder |
| [01-02 세션 저장소 구조](./01-02.HttpSession·SessionRegistry·SecurityContextHolder.md) | `HttpSession`·`SessionRegistry`·`SecurityContextHolder`는 각각 무엇을 들고 언제 지워지며, 쿠키 `Path`와 `LogoutFilter`는 어떻게 동작하나? | StandardSession, SessionRegistry, SecurityContextHolder, Path 매칭, LogoutFilter |
| [02-01 로그인 인증·CSRF·세션 복원](./02-01.CsrfFilter·CookieCsrfTokenRepository·SecurityContextRepository.md) | 세션 쿠키 인증에 왜 CSRF 방어가 따라오며, 폼 로그인 없이 로그인과 세션 복원을 어떻게 조립하나? | CsrfFilter, CsrfCookieFilter, CookieCsrfTokenRepository, SecurityContextRepository, ROLE_ 접두어 |
| [02-02 세션 끊기와 필터 순서](./02-02.SessionInformation·ConcurrentSessionFilter·LogoutFilter.md) | 다른 기기의 세션을 즉시 지우지 않고 만료 표시로 끊는 이유와, `ConcurrentSessionFilter`·`LogoutFilter` 순서가 응답을 가르는 원리는 무엇인가? | SessionInformation, SessionRegistry, ConcurrentSessionFilter, LogoutFilter, 필터 순서 |
| [03-01 로그인 실패 응답과 시도 제한](./03-01.userNotFoundEncodedPassword·RemoteIpValve·X-Forwarded-For.md) | 실패 응답 코드와 시간 차이로 계정 존재가 새는 것을 어떻게 막고, `X-Forwarded-For` 신뢰 경계와 시도 제한은 어떻게 세우나? | 검사 순서, 더미 해시 타이밍, 계정 잠금 DoS, RemoteIpValve, X-Forwarded-For |



## 다른 문서와의 경계

> 같은 개념을 두 곳에서 길게 설명하지 않도록, 프레임워크 독립 보안 이론과 앞단 프록시 설정은 다른 폴더에 맡깁니다.

인증과 인가의 구분, 세션 기반과 무상태 토큰의 트레이드오프 같은 프레임워크 독립 보안 이론은 [보안 개념 정리](../../../99_ETC/security/01_concepts/README.md)가 맡습니다. 이 시리즈는 그 개념이 Spring Security와 Tomcat 안에서 어떤 필터와 저장소로 구현되는지를 다룹니다.

Nginx와 HAProxy 같은 리버스 프록시가 `X-Forwarded-For` 헤더를 붙이고 위조 헤더를 걸러내는 앞단 설정은 [reverse-proxy 시리즈](../../../02_os/docs/reverse-proxy/README.md)가 맡습니다. 03-01 편은 그 헤더를 넘겨받는 Tomcat과 Spring 앱 쪽의 신뢰 조건에 집중합니다.

Spring 전체 영역에서 보안과 운영이 차지하는 자리는 [Spring 학습 통합 MOC](../../README.md)와 [Spring 개발 키워드](../../spring-keywords.md) 8단계 표가 보여 줍니다.
