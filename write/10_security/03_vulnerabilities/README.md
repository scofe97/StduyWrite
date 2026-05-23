---
title: 10_security/03_vulnerabilities — OWASP·취약점 카탈로그
tags: [moc, security, owasp, vulnerabilities]
status: final
related:
  - ../README.md
updated: 2026-04-19
---

# 10_security/03_vulnerabilities
---
> OWASP Top 10을 중심으로 실제 발생하는 공격 기법과 방어 코드를 모은다. 이론만 나열하지 않고 **실제 취약 코드 → 수정 코드**를 짝으로 다룬다.

## 예정 주제

- `01_sql-injection.md` — Prepared Statement, 입력 검증, ORM 남용 사례
- `02_xss.md` — Reflected·Stored·DOM-based, CSP, 출력 인코딩
- `03_csrf.md` — SameSite 쿠키, CSRF 토큰, Spring Security 기본 동작
- `04_ssrf.md` — 외부 URL 호출의 함정
- `05_deserialization.md` — Jackson·ObjectInputStream의 위험
- `06_authentication-flaws.md` — 세션 고정, 브루트포스 완화
- `07_access-control-flaws.md` — IDOR, 권한 상승

## 원칙

공격 코드는 "어떻게 뚫리는가"를 이해할 정도로만 기술한다. 실제 악용 가능한 페이로드·스캐닝 도구 사용법은 범위 밖이다. 방어·완화가 주된 서술 대상이다.
