---
title: Notion → write/ 이관 manifest (2026-05-20)
tags: [meta, migration, notion]
status: final
related:
  - conventions.md
updated: 2026-05-20
---

# Notion → write/ 이관 manifest (2026-05-20)

---

> Notion export(`~/Downloads/개인 페이지 & 공유된 페이지 4/기술 블로그/공부 데이터베이스/`)에서 `write/`로 이관한 문서를 기록한다. second-brain-harness §9.1.8의 "원본 추적" 의무를 충족하기 위한 manifest다. Downloads 폴더는 git 추적 밖이라 원본에 주석을 남길 수 없어 본 파일이 그 역할을 대신한다.

## 1차 이관 — Spring Security 9편 → 10_security/02_spring-security/ (2026-05-20)

총 9편 중 8편을 본문 문서로 이관, 1편(`00 Spring Security 시작`)은 출처 정보만 담긴 진입 페이지라 `02_spring-security/README.md` 학습 출처 섹션으로 흡수.

| Notion 원본 | 이관 후 |
|------------|---------|
| `[Spring Security] 00 Spring Security 시작 627ce4f9....md` | `02_spring-security/README.md` § 학습 출처에 흡수 |
| `[Spring Security] 01-1 Spring Security 개념 ⭐ 42ec449e....md` | `02_spring-security/01-01.Spring Security 개념과 Filter Chain.md` |
| `[Spring Security] 01-2 Spring Security 구현 60fcc0e7....md` | `02_spring-security/01-02.Spring Security 기본 구현.md` |
| `[Spring Security] 01-3 실습 - form 회원가입 2cbe801d....md` | `02_spring-security/01-03.Form 로그인 실습.md` |
| `[Spring Security] 02-1 OAuth2 0 개념이해 ⭐ 98f464e4....md` | `02_spring-security/02-01.OAuth2 개념과 흐름.md` |
| `[Spring Security] 02-2 Google Login ⭐ 2dfaf019....md` | `02_spring-security/02-02.Google OAuth2 Login.md` |
| `[Spring Security] 02-3 Facebook Login 7fdaaa65....md` | `02_spring-security/02-03.Facebook OAuth2 Login.md` |
| `[Spring Security] 02-4 Naver Login 8cec4834....md` | `02_spring-security/02-04.Naver OAuth2 Login.md` |
| `[Spring Security] 04 Spring Security + JWT 구현 a183712d....md` | `02_spring-security/03-01.JWT 인증 구현.md` |

### 적용한 §9 재구성 규칙

- Notion `<aside>` callout과 이모지(💡 ✍️) 제거, 본문 평탄화
- 본인 메모(예: "그냥 참고용.. 봐도 모르겠다", "ㅋㅋㅋㅋㅋ") 제거 또는 정제
- `Untitled.png` 시리즈 첨부 이미지는 보존하지 않음 (텍스트·Mermaid로 재구성)
- 6섹션 구조 적용: 한 줄 정의 → 왜 필요 → 아키텍처 → 핵심 객체 → 실습 → 면접 요약
- Spring Security 6.x 기준 갱신 (`WebSecurityConfigurerAdapter` deprecated, `authorizeHttpRequests`, 람다 DSL)
- 공식 문서 출처 추가 (docs.spring.io/spring-security/reference, datatracker.ietf.org RFC 6749/7519)

### 결과

- 영향 받은 파일: 본문 8편 신규 + `02_spring-security/README.md` MOC 갱신 + `10_security/README.md` 카운트 갱신 = 10개 파일
- 카테고리 완결성: 이전에는 README만 있는 placeholder, 현재는 8편 본문 + MOC 살아 있음

## 2차 이관 (예정)

인덱싱 보고서(`~/.claude-work/plans/notion-export-index.md`)의 우선순위에 따라 사용자 결정 후 진행.

- ★★ Spring WebSocket 7편 → `11_spring/06_websocket/` 신설 후보
- ★★ Spring TDD 6편 → `11_spring/04_testing/tdd/` 하위 폴더 흡수 후보
- ★★ Spring Netty 10편 → `11_spring/05_internals/` 신설 후보
- ★ Spring MSA 30편 — 카테고리 분산 이관 (도메인·메시징·관측성·클라우드)
- ★ Spring Study 51편 — 신설 폴더 다수 필요, 대규모

## 원본 보존

Notion export 원본(`~/Downloads/개인 페이지 & 공유된 페이지 4/`)은 삭제하지 않는다. 이관 완료된 문서도 원본은 그대로 두며, 본 manifest로 이관 여부와 매핑을 추적한다. 6개월 후 원본 자체를 archive 처리할 시점은 `_meta/conventions.md`의 정기 트리거에서 결정한다.
