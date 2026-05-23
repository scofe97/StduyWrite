---
title: 10_security/02_spring-security — Spring Security 구현
tags: [moc, spring, spring-security, security, oauth2, jwt]
status: final
related:
  - ../README.md
  - ../01_concepts/README.md
  - ../../11_spring/README.md
updated: 2026-05-20
---

# 10_security/02_spring-security

---

> Spring Security 6.x 기준 Filter Chain·OAuth2 Login·JWT 인증 구현을 한 묶음으로 정리한다. 시리즈는 8편이며, Spring Boot 3 + Spring Security 6.x 환경 코드를 기준으로 작성됐다.

## 학습 순서

> 1장은 폼 로그인까지의 단일 인증 흐름, 2장은 외부 OAuth2 provider 연동, 3장은 무상태 토큰 기반 인증이다. 8편을 순서대로 따라가면 면접 질문 10개 이상에 답할 수 있는 수준이 목표다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [Spring Security 개념과 Filter Chain](01-01.Spring%20Security%20개념과%20Filter%20Chain.md) | DelegatingFilterProxy → FilterChainProxy 위임 구조, AuthenticationManager 10단계, SecurityFilterChain 내부 필터 |
| 01-02 | [Spring Security 기본 구현](01-02.Spring%20Security%20기본%20구현.md) | SecurityFilterChain 빈 등록, HttpSecurity 람다 DSL, PasswordEncoder, OncePerRequestFilter |
| 01-03 | [Form 로그인 실습](01-03.Form%20로그인%20실습.md) | UserDetailsService 어댑터, PrincipalDetails, Method Security (@Secured / @PreAuthorize) |
| 02-01 | [OAuth2 개념과 흐름](02-01.OAuth2%20개념과%20흐름.md) | 4역할, 인가 코드 그랜트, Access/Refresh Token, OIDC와의 차이 |
| 02-02 | [Google OAuth2 Login](02-02.Google%20OAuth2%20Login.md) | spring-boot-starter-oauth2-client, OAuth2UserService.loadUser, PrincipalDetails 통합 |
| 02-03 | [Facebook OAuth2 Login](02-03.Facebook%20OAuth2%20Login.md) | provider별 attributes 차이, OAuth2UserInfo 전략 패턴 |
| 02-04 | [Naver OAuth2 Login](02-04.Naver%20OAuth2%20Login.md) | 기본 제공이 아닌 provider 직접 등록, response 래핑 풀어내기 |
| 03-01 | [JWT 인증 구현](03-01.JWT%20인증%20구현.md) | jjwt TokenProvider, JwtAuthenticationFilter + JwtAuthorizationFilter, STATELESS 세션 |

## 핵심 객체 한 줄 정리

| 객체 | 역할 |
|------|------|
| `SecurityFilterChain` | 빈 한 개에 인증·인가·세션·CORS·커스텀 필터 정의를 모음 |
| `AuthenticationManager` (ProviderManager) | 인증 시도의 단일 진입점, 적합한 Provider에 위임 |
| `UserDetailsService` | DB에서 사용자 정보를 가져와 `UserDetails`로 반환 |
| `PasswordEncoder` (BCrypt) | 솔트·work factor 포함한 해시 비교 |
| `OAuth2UserService` | OAuth2 토큰 교환 직후 프로필을 우리 DB와 매핑 |
| `OncePerRequestFilter` | 한 요청당 1회 실행이 보장되는 커스텀 필터 베이스 |
| `SecurityContextHolder` | 현재 스레드의 `Authentication` 보관 (ThreadLocal) |

## 학습 출처

원본 학습은 다음 자료를 참고했고, 본 시리즈는 이를 Spring Security 6.x로 갱신하면서 공식 문서 인용을 추가했다.

- [[무료] 스프링부트 시큐리티 & JWT 강의 (인프런)](https://www.inflearn.com/course/스프링부트-시큐리티/dashboard)
- [스프링부트 JUnit 테스트 - 시큐리티 활용 Bank 애플리케이션 (인프런)](https://www.inflearn.com/course/스프링부트-junit-테스트/dashboard)
- [Spring Security Reference (공식)](https://docs.spring.io/spring-security/reference/)

## 5.x에서 6.x로 — 주의할 변경점

> 본 시리즈 작성 시 가장 자주 만난 5.x 패턴과 6.x 대체를 정리한다.

| 5.x 패턴 | 6.x 대체 |
|---------|---------|
| `WebSecurityConfigurerAdapter` 상속 | `SecurityFilterChain` 빈 등록 |
| `http.csrf().disable().and().sessionManagement()...` | 람다 DSL: `http.csrf(csrf -> csrf.disable()).sessionManagement(sm -> ...)` |
| `@EnableGlobalMethodSecurity(prePostEnabled = true)` | `@EnableMethodSecurity` (기본값 prePostEnabled = true) |
| `authorizeRequests()` | `authorizeHttpRequests()` |
| `antMatchers("/admin/**")` | `requestMatchers("/admin/**")` |
| `authorization-grant-type: implicit` | 제거됨, `authorization_code`만 사용 |

## 관련 문서

- [10_security 상위 MOC](../README.md) — 보안 카테고리 전체 진입
- [10_security/01_concepts](../01_concepts/README.md) — OAuth2·JWT·암호학 이론 (프레임워크 독립)
- [11_spring 통합 MOC](../../11_spring/README.md) — Spring 본질 이론 진입점
