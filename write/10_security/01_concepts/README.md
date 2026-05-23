---
title: 10_security/01_concepts — 보안 이론 (프레임워크 독립)
tags: [moc, security, oauth2, oidc, jwt]
status: final
related:
  - ../README.md
updated: 2026-04-19
---

# 10_security/01_concepts
---
> 특정 프레임워크·언어에 종속되지 않는 순수 보안 이론을 모은다.

## 예정 주제

- `01_authentication-vs-authorization.md` — 인증과 인가의 구분, RBAC·ABAC 모델
- `02_oauth2-oidc.md` — Authorization Code Flow, PKCE, 토큰 수명 전략
- `03_jwt-design.md` — JWT 구조, 서명·검증, 저장 위치(쿠키 vs 로컬스토리지)
- `04_session-vs-token.md` — 상태 기반 vs 무상태 인증의 트레이드오프
- `05_cryptography-basics.md` — 대칭/비대칭, 해시, HMAC, 솔트·페퍼

## 경계

Spring Security 구현은 [`../02_spring-security/`](../02_spring-security/)로. 공격 기법 카탈로그는 [`../03_vulnerabilities/`](../03_vulnerabilities/)로.
