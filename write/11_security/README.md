---
title: 11_security MOC
tags: [moc, security]
status: final
related:
  - ../03_architecture/README.md
  - ../01_language/java/spring/README.md
updated: 2026-04-19
---

# 11_security
---
> 인증·인가, 암호학, OWASP, 위협 모델링, Spring Security 구현을 통합한 보안 전용 카테고리.

## 왜 별도 대분류인가

보안과 아키텍처는 "secure by design"처럼 밀접한 영역이지만, 보안에는 고유 이론 깊이(암호학, 프로토콜, 취약점 카탈로그)가 있어 아키텍처 하위에 두면 문서가 몇 개만 쌓여도 경계가 무너진다. 본 카테고리는 "공격/방어 기술"을 다루는 전용 공간이다. `03_architecture/`는 "시스템 설계" 축으로 분리 유지한다.

## 하위

| 폴더 | 범위 |
|------|------|
| [01_concepts/](01_concepts/) | 프레임워크 독립 이론 — OAuth2, OIDC, JWT, 세션 vs 토큰, 암호학 기초 |
| [02_spring-security/](02_spring-security/) | Spring Security Filter Chain, AuthenticationManager, Method Security |
| [03_vulnerabilities/](03_vulnerabilities/) | OWASP Top 10 — SQL Injection, XSS, CSRF 등 |
| [04_threat-modeling/](04_threat-modeling/) | STRIDE, Attack Tree, 공격자 관점 설계 분석 |

## 03_architecture와의 경계 가이드

주제별 배치 기준. 양쪽 tags를 넣어 `related`로 양방향 연결하는 경우가 정상이다.

| 주제 | 배치 | 근거 |
|------|------|------|
| Threat Modeling (STRIDE) | `11_security/04_threat-modeling/` | 공격자 관점 기법 |
| Secure by Design 원칙 | `03_architecture/` (cross-link) | 설계 철학 |
| OAuth2, OIDC, SAML 이론 | `11_security/01_concepts/` | 프로토콜 기술 |
| Zero Trust Architecture | `11_security/` (cross-link to 03) | 보안 전략 |
| 권한 경계 설계 (컨텍스트별 권한) | `03_architecture/` | 경계 컨텍스트 관점 |
| mTLS, TLS 핸드셰이크 | `11_security/` 또는 `09_cloud/` | 네트워크 보안 |
| OWASP Top 10 | `11_security/03_vulnerabilities/` | 취약점 카탈로그 |
| API Gateway 설계 (rate limit) | `03_architecture/` 또는 `09_cloud/` | 아키텍처 패턴 |

## 관련 문서

- [Spring 통합 MOC](../01_language/java/spring/README.md)
- [03_architecture MOC](../03_architecture/README.md)
