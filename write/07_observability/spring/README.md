---
title: 07_observability/spring — Spring 관측성
tags: [moc, spring, actuator, micrometer]
status: final
related:
  - ../README.md
  - ../../01_language/java/spring/README.md
updated: 2026-04-19
---

# 07_observability/spring
---
> Spring Actuator, Micrometer, Spring Boot의 메트릭·헬스체크·트레이싱 자동 연동을 모은다.

## 경계

- OpenTelemetry 자체 규격, Tempo·Loki·Prometheus 설정은 [`07_observability/`](../) 직접 하위
- Spring Boot가 이들과 **자동 통합**되는 지점은 여기

## 예정 주제

- Actuator 엔드포인트 커스터마이즈·보안
- Micrometer와 Prometheus 연결
- Spring Boot 3.x의 자동 트레이싱 (Brave → OpenTelemetry 전환)
- `/actuator/health` 그룹·프로브 설계

## 관련 문서

- [Spring 통합 MOC](../../01_language/java/spring/README.md)
