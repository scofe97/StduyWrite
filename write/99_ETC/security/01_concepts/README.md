---
title: 99_ETC/security/01_concepts — 보안 이론 (프레임워크 독립)
tags: [moc, security, oauth2, oidc, jwt]
status: final
related:
  - ../README.md
updated: 2026-05-29
---

# 99_ETC/security/01_concepts
---
> 특정 프레임워크·언어에 종속되지 않는 순수 보안 이론을 모은다.

## 학습 순서

> 인증·인가의 구분에서 시작해, 그 위에서 토큰을 어떻게 발급·운반·저장할지(OAuth2·JWT·세션), 마지막으로 이 모든 것을 떠받치는 암호학 기초 순으로 읽는다. 5편 모두 프레임워크 독립 이론만 다룬다. 2026-09-05에 파일명을 `날짜_주제`로 바꾸면서 순서가 파일명에서 빠졌으므로, 읽는 순서는 아래 표가 갖는다.

| 순서 | 문서 | 다루는 핵심 |
|------|------|-----------|
| 01 | [인증과 인가](./2026-05-29_%EC%9D%B8%EC%A6%9D%EA%B3%BC%20%EC%9D%B8%EA%B0%80%20%E2%80%94%20Authentication%20vs%20Authorization.md) | 인증 vs 인가 / 401 vs 403 / RBAC·ABAC 모델 / 분리가 설계에 주는 이득 |
| 02 | [OAuth2와 OIDC](./2026-05-29_OAuth2%EC%99%80%20OIDC%20%E2%80%94%20%EC%9C%84%EC%9E%84%20%EC%9D%B8%EA%B0%80%EC%99%80%20%EA%B7%B8%20%EC%9C%84%EC%9D%98%20%EC%9D%B8%EC%A6%9D.md) | 인가 위임 4역할 / Authorization Code Flow / PKCE / OIDC ID Token |
| 03 | [JWT 설계](./2026-05-29_JWT%20%EC%84%A4%EA%B3%84%20%E2%80%94%20%EA%B5%AC%EC%A1%B0%C2%B7%EC%84%9C%EB%AA%85%C2%B7%EC%A0%80%EC%9E%A5%EA%B3%BC%20%ED%8F%90%EA%B8%B0%EC%9D%98%20%EB%94%9C%EB%A0%88%EB%A7%88.md) | header.payload.signature / HS256 vs RS256 / 저장 위치 / 무상태 폐기 딜레마 |
| 04 | [세션 vs 토큰](./2026-05-29_%EC%84%B8%EC%85%98%20vs%20%ED%86%A0%ED%81%B0%20%E2%80%94%20%EC%83%81%ED%83%9C%20%EA%B8%B0%EB%B0%98%EA%B3%BC%20%EB%AC%B4%EC%83%81%ED%83%9C%20%EC%9D%B8%EC%A6%9D%EC%9D%98%20%ED%8A%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%98%A4%ED%94%84.md) | 상태 기반 vs 무상태 / 확장성·폐기·저장 비용 트레이드오프 / 결정 트리 |
| 05 | [암호학 기초](./2026-05-29_%EC%95%94%ED%98%B8%ED%95%99%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EB%8C%80%EC%B9%AD%C2%B7%EB%B9%84%EB%8C%80%EC%B9%AD%C2%B7%ED%95%B4%EC%8B%9C%C2%B7HMAC.md) | 대칭·비대칭 / 해시·솔트·느린 해시 / HMAC / 기밀성·무결성·인증 |

## 경계 — 이론만 다룬다

본 폴더는 프로토콜·모델·트레이드오프 같은 *이론* 만 다룬다. 같은 주제의 Spring 구현 — OAuth2 Login, JWT TokenProvider·필터, Filter Chain — 을 다루던 묶음이 있었으나 제거됐고, 현재 이 저장소에 구현 편은 없다.
