---
title: 09_cloud/spring — Spring Cloud
tags: [moc, spring, spring-cloud, gateway]
status: final
related:
  - ../README.md
  - ../../12_spring/README.md
updated: 2026-04-19
---

# 09_cloud/spring
---
> Spring Cloud Gateway, Config Server, Sleuth 후속 같은 클라우드 네이티브 Spring 스택을 모은다.

## 경계

- K8s 매니페스트·Helm 차트 설계는 [`09_cloud/`](../) 직접 하위
- Service Mesh(Istio, Linkerd) 개념도 [`09_cloud/`](../)
- **Spring 애플리케이션이 이들 위에서 돌 때 필요한 Spring 스택**이 여기

## 예정 주제

- Spring Cloud Gateway — 라우팅·필터·Circuit Breaker 통합
- Spring Cloud Config — 중앙 설정 저장소
- Spring Cloud Stream (Kafka·RabbitMQ 추상화) — 주의: 메시징 도메인이면 [`05_messaging/spring/`](../../05_messaging/spring/)도 확인
- K8s 친화적 설정 — `application-k8s.yml`, probes, graceful shutdown

## 관련 문서

- [Spring 통합 MOC](../../12_spring/README.md)
