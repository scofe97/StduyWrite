---
title: 10_security/01_concepts — 보안 이론 (프레임워크 독립)
tags: [moc, security, oauth2, oidc, jwt]
status: final
related:
  - ../README.md
updated: 2026-05-29
---

# 10_security/01_concepts
---
> 특정 프레임워크·언어에 종속되지 않는 순수 보안 이론을 모은다.

## 학습 순서

> 인증·인가의 구분에서 시작해, 그 위에서 토큰을 어떻게 발급·운반·저장할지(OAuth2·JWT·세션), 마지막으로 이 모든 것을 떠받치는 암호학 기초 순으로 읽는다. 5편은 프레임워크 독립 이론만 다루고, 구현은 02_spring-security 로 위임한다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01 | [인증과 인가](01_authentication-vs-authorization.md) | 인증 vs 인가 / 401 vs 403 / RBAC·ABAC 모델 / 분리가 설계에 주는 이득 |
| 02 | [OAuth2와 OIDC](02_oauth2-oidc.md) | 인가 위임 4역할 / Authorization Code Flow / PKCE / OIDC ID Token |
| 03 | [JWT 설계](03_jwt-design.md) | header.payload.signature / HS256 vs RS256 / 저장 위치 / 무상태 폐기 딜레마 |
| 04 | [세션 vs 토큰](04_session-vs-token.md) | 상태 기반 vs 무상태 / 확장성·폐기·저장 비용 트레이드오프 / 결정 트리 |
| 05 | [암호학 기초](05_cryptography-basics.md) | 대칭·비대칭 / 해시·솔트·느린 해시 / HMAC / 기밀성·무결성·인증 |

## 경계 — 이론은 여기, 구현은 02_spring-security

본 폴더는 프로토콜·모델·트레이드오프 같은 *이론* 만 다룬다. 같은 주제의 Spring 구현 — OAuth2 Login, JWT TokenProvider·필터, Filter Chain — 은 [`../02_spring-security/`](../02_spring-security/) 에 있고, 각 개념 편이 해당 구현 편을 링크로 가리킨다. 공격 기법 카탈로그는 [`../03_vulnerabilities/`](../03_vulnerabilities/) 로.
