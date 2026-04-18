---
title: 11_security/02_spring-security — Spring Security 구현
tags: [moc, spring, spring-security, security]
status: final
related:
  - ../README.md
  - ../01_concepts/README.md
  - ../../01_language/java/spring/README.md
updated: 2026-04-19
---

# 11_security/02_spring-security
---
> Spring Security 프레임워크 구현 문서. Filter Chain, AuthenticationManager, Method Security 등.

## 예정 주제

- `01_filter-chain.md` — Security Filter 체인 구조와 커스텀 필터 주입
- `02_authentication-manager.md` — AuthenticationManager·Provider·Token 체계
- `03_method-security.md` — `@PreAuthorize`, `@PostAuthorize`, SpEL
- `04_oauth2-client.md` — Spring Security OAuth2 Client 설정
- `05_resource-server.md` — JWT 검증, 리소스 서버 구성

## 읽는 순서

1. [`../01_concepts/`](../01_concepts/)에서 OAuth2·JWT 이론 먼저
2. 이 폴더의 Filter Chain 개념으로 Spring이 이를 어떻게 구현하는지
3. 실전: Controller 단 `@PreAuthorize` 적용

## 관련 문서

- [Spring 통합 MOC](../../01_language/java/spring/README.md)
