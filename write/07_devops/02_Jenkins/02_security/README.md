---
title: Jenkins 보안과 설정 코드화 학습 MOC
tags: [moc, jenkins, security, secret, jcasc, gitops]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
  - ../04_api/README.md
  - ../05_operations/README.md
updated: 2026-05-28
---

# Jenkins 보안과 설정 코드화 학습 MOC

---

> Jenkins 를 "누가 무엇을 할 수 있는가" 의 인증·인가 축과 "그 설정을 어떻게 코드로 다루는가" 의 JCasC 축으로 묶었습니다. 두 축을 끝내면 "방금 만든 시크릿이 누구의 손에 들어가고, 그 설정이 어떻게 GitOps 흐름에 올라가는가" 를 한 흐름으로 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

인증·인가(구 03) 와 JCasC(구 06) 는 표면적으로 다른 주제처럼 보이지만, 실제 운영에서는 한 쌍입니다. "Admin 권한을 가진 사람이 누구인가" 는 인증·인가가 답하고, "그 권한 부여를 코드로 재현 가능하게 두는 방법" 은 JCasC 가 답합니다. 한쪽만 알면 운영 사고가 사람 한 명의 기억에 갇히고, 양쪽을 묶어 두면 설정 자체가 PR 단위로 추적됩니다.

01장이 "권한 모델·시크릿 격리" 라는 *원칙* 을 세우고, 02장이 그 원칙을 *코드* 로 구현합니다. 학습 순서도 같은 방향으로 흐릅니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 인증·인가 | 01-00 | [점검 — 핵심 질문과 답 (인증·인가)](01-00.점검.핵심%20질문과%20답%20%28인증·인가%29.md) | 01장 진입 전 자가 점검 |
| 01 인증·인가 | 01-01 | [인증과 인가 — 누가 무엇을 할 수 있는가](01-01.인증과%20인가%20—%20누가%20무엇을%20할%20수%20있는가.md) | Security Realm, Authorization Strategy, Matrix-based / Role-based, Project-based |
| 01 인증·인가 | 01-02 | [시크릿 관리와 최소 권한 원칙](01-02.시크릿%20관리와%20최소%20권한%20원칙.md) | Credentials Provider, 도메인 분리, 자격증명 바인딩, 최소 권한 적용 |
| 02 JCasC | 02-00 | [점검 — 핵심 질문과 답 (JCasC)](02-00.점검.핵심%20질문과%20답%20%28JCasC%29.md) | 02장 진입 전 자가 점검 |
| 02 JCasC | 02-01 | [설정을 코드로 — JCasC](02-01.설정을%20코드로%20—%20JCasC.md) | JCasC 도입 동기, YAML 구조, 적용 시점, jenkins.yaml 핵심 섹션 |
| 02 JCasC | 02-02 | [JCasC 운영과 GitOps](02-02.JCasC%20운영과%20GitOps.md) | Git 저장, PR 리뷰, configure-as-code reload, 환경별 분리 |
| 02 JCasC | 02-03 | [JCasC 시크릿과 실전 패턴](02-03.JCasC%20시크릿과%20실전%20패턴.md) | `${SECRET}` 치환, 외부 Vault 연동, 실수 사례와 회피책 |

처음 진입자는 01-00 자가 점검부터 풀고 막히는 항목만 01-01·01-02 로 보강합니다. JCasC 를 이미 쓰고 있는 사람은 02-03 의 실수 사례를 먼저 훑고 자기 환경과 대조하는 편이 학습 효과가 큽니다.

## 환경과 버전

> 본 묶음 예제는 다음 조합 기준입니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Jenkins | LTS 2.426.x 이상 | configuration-as-code 플러그인 동봉 |
| Credentials Plugin | 1300+ | Domain·Folder 단위 격리 지원 |
| Configuration as Code | 1750+ | reload-existing-configuration 엔드포인트 |
| Matrix Authorization | 3.x | Project-based 권한 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`../01_core/`](../01_core/README.md) 의 Jenkins 제어 영역과 Pipeline 기본 구조를 알고 있습니다.
2. YAML 문법(`key: value`, 들여쓰기, 리스트) 을 읽을 수 있습니다.
3. Git PR 흐름(브랜치 → 리뷰 → 머지) 으로 변경을 관리해 본 경험이 있습니다.

위 항목 중 막히는 부분이 있으면 [`../01_core/`](../01_core/README.md) 를 먼저 보고 돌아오는 편이 빠릅니다.

## 면접 대비 체크리스트

> 두 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. Security Realm 과 Authorization Strategy 는 각각 무엇을 결정합니까? 둘이 분리된 이유는?
2. Matrix-based 와 Role-based 권한 전략의 차이는? 어떤 규모에서 어느 쪽이 유리합니까?
3. Credentials Plugin 의 Domain 분리는 무엇을 격리합니까? Folder 스코프와 Global 스코프의 차이는?
4. JCasC 의 `jenkins.yaml` 이 무엇을 표현하지 못합니까? — 즉, JCasC 한계 영역은?
5. JCasC 적용 시 시크릿이 평문 노출되지 않게 하는 두 가지 패턴은?

각 질문에 막히면 해당 절로 돌아갑니다.
