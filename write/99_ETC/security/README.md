---
title: 99_ETC/security MOC
tags: [moc, security]
status: final
related:
  - ../../03_architecture/README.md
  - ../../09_spring/README.md
updated: 2026-05-20
---

# 99_ETC/security
---
> 인증·인가, 암호학, OWASP, 위협 모델링을 통합한 보안 문서 묶음.

> ⚠️ **임시 보관 중.** 2026-08-23에 대분류 `10_security/`를 걷어내고 번호를 당기면서 이 묶음을 `99_ETC/security/`로 옮겼다. 아래 "왜 별도 대분류인가"는 *옮기기 전의 근거*를 그대로 남긴 것이다. 3개월 뒤 문서가 늘었으면 대분류로 되돌리고, 그대로면 각 주제를 해당 카테고리로 흩는다.

## 왜 별도 대분류인가

보안과 아키텍처는 "secure by design"처럼 밀접한 영역이지만, 보안에는 고유 이론 깊이(암호학, 프로토콜, 취약점 카탈로그)가 있어 아키텍처 하위에 두면 문서가 몇 개만 쌓여도 경계가 무너진다. 본 카테고리는 "공격/방어 기술"을 다루는 전용 공간이다. `03_architecture/`는 "시스템 설계" 축으로 분리 유지한다.

## 하위

| 폴더 | 범위 |
|------|------|
| [01_concepts/](./01_concepts/) | 프레임워크 독립 이론 — OAuth2, OIDC, JWT, 세션 vs 토큰, 암호학 기초 |
| [05_network/](./05_network/) | 네트워크 계층(L2~L4) 공격과 방어 — ARP 스푸핑·중간자 공격, mTLS가 근본 해법인 이유 |

OWASP 취약점 카탈로그(`03_vulnerabilities/`)와 위협 모델링(`04_threat-modeling/`)은 2026-04-19에 "예정 주제"만 적은 폴더로 만들었다가 2026-09-05에 걷어냈다. 넉 달 반 동안 본문이 한 편도 붙지 않았기 때문이다. 첫 문서를 쓸 때 폴더를 다시 만든다.

## 03_architecture와의 경계 가이드

주제별 배치 기준. 양쪽 tags를 넣어 `related`로 양방향 연결하는 경우가 정상이다.

| 주제 | 배치 | 근거 |
|------|------|------|
| Threat Modeling (STRIDE) | `99_ETC/security/` (폴더 신설) | 공격자 관점 기법 |
| Secure by Design 원칙 | `03_architecture/` (cross-link) | 설계 철학 |
| OAuth2, OIDC, SAML 이론 | `99_ETC/security/01_concepts/` | 프로토콜 기술 |
| Zero Trust Architecture | `99_ETC/security/` (cross-link to 03) | 보안 전략 |
| 권한 경계 설계 (컨텍스트별 권한) | `03_architecture/` | 경계 컨텍스트 관점 |
| mTLS, TLS 핸드셰이크 | `99_ETC/security/05_network/` 또는 `08_cloud/` | 네트워크 보안 |
| OWASP Top 10 | `99_ETC/security/` (폴더 신설) | 취약점 카탈로그 |
| API Gateway 설계 (rate limit) | `03_architecture/` 또는 `08_cloud/` | 아키텍처 패턴 |

## 예정 주제 — 시크릿 관리 (TBD)

> OAuth2·JWT가 *사용자를 인증하는* 이론이라면, 시크릿 관리는 *애플리케이션이 쥔 비밀(DB 비번·API 키·인증서)을 어떻게 안전하게 보관·주입하는가*의 문제다. `01_concepts/`의 프로토콜 이론과 같은 계열로 둔다.

- **Vault** — 시크릿(키·비밀번호·인증서)의 중앙 저장·접근 통제·동적 시크릿(요청 시 발급 후 리스 만료)·감사 로그를 담당하는 인프라. `.env` 파일·K8s ConfigMap 같은 *정적 평문 시크릿*의 한계(유출·회전 부재)를 무엇으로 메우는지가 핵심. (실환경 예시: CMP 3.0.4 dataplatform이 Vault로 토큰 기반 시크릿을 관리.) 본문은 `01_concepts/` 소속으로 예고.

경계: 인증·인가 프로토콜 이론(OAuth2·OIDC·JWT)은 기존 [`01_concepts/`](./01_concepts/). Vault는 *시크릿 저장·주입 인프라* 관점이라 같은 폴더에 두되 주제가 다르다. K8s Secret 리소스 자체의 매니페스트는 [`../08_cloud/kubernetes/`](../../08_cloud/kubernetes/README.md).

## 관련 문서

- [Spring 통합 MOC](../../09_spring/README.md)
- [03_architecture MOC](../../03_architecture/README.md)
