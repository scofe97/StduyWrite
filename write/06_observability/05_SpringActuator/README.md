---
title: 스프링 부트 액츄에이터·메트릭 학습 MOC
tags: [moc, spring-boot, actuator, micrometer, prometheus, grafana]
status: draft
related:
  - ../README.md
  - ../02_LGTMStack/02-01.Grafana Core.md
  - ../../11_spring/07_autoconfig/README.md
updated: 2026-05-25
---

# 스프링 부트 액츄에이터·메트릭 학습 MOC
---

> 이 묶음은 *스프링 애플리케이션이 자기 운영 정보를 밖으로 내보내는* 쪽을 다룹니다. 헬스·메트릭을 엔드포인트로 노출하고(액츄에이터), 비즈니스 메트릭을 측정하고(마이크로미터), 그것을 프로메테우스·그라파나가 수집·시각화하게 연동하는 흐름입니다. 같은 06_observability 안의 다른 묶음과 관점이 다르므로, 그 경계를 먼저 잡는 것이 중요합니다.

## 관점 경계 — 내보내는 쪽 vs 수집하는 쪽

06_observability 는 관측 가능성을 두 관점에서 다룹니다.

| 관점 | 묶음 | 다루는 것 |
|------|------|----------|
| 앱이 *내보내는* 쪽 | `05_SpringActuator/` (여기) | 액츄에이터 엔드포인트, 마이크로미터 측정, 프로메테우스 형식 노출 |
| 인프라가 *수집·저장·시각화* 하는 쪽 | `02_LGTMStack/`, `03_Project/` | Grafana·Loki·Tempo·Mimir 운영, 대시보드 설계, 실전 배포 |

액츄에이터가 메트릭을 노출하면 LGTM 스택이 그것을 긁어 갑니다. 두 묶음은 양방향 `related` 로 연결되며, "앱 설정"이 궁금하면 여기를, "수집 인프라"가 궁금하면 02_LGTMStack 을 봅니다.

## 학습 순서

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [액츄에이터 — 운영 엔드포인트](01-01.액츄에이터%20—%20운영%20엔드포인트.md) | 프로덕션 준비 기능, 엔드포인트 종류, 노출 제어, 헬스, 보안 |
| 01-02 | [마이크로미터와 메트릭 — Counter·Gauge·Timer](01-02.마이크로미터와%20메트릭%20—%20Counter·Gauge·Timer.md) | 측정 추상화, 메트릭 세 타입, 태그, @Counted·@Timed |
| 01-03 | [프로메테우스·그라파나 연동](01-03.프로메테우스·그라파나%20연동.md) | 노출-수집-시각화 3단 역할, scrape, PromQL |

처음 보는 학습자는 01-01 부터 순서대로 보면 됩니다. 01-01이 운영 정보를 노출하는 액츄에이터를 다루고, 01-02가 그중 메트릭을 직접 등록하는 방법을, 01-03이 그 메트릭을 프로메테우스·그라파나로 잇는 연동을 다룹니다. "애플리케이션 → 프로메테우스 → 그라파나"의 역할 분담이 묶음 전체를 관통하는 뼈대입니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.x | `spring-boot-starter-actuator` |
| Micrometer | 1.x | `micrometer-registry-prometheus` |
| Java | 17+ | |

## 면접 대비 체크리스트

> 세 편을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. 액츄에이터 엔드포인트를 함부로 다 열면 안 되는 이유는? 노출을 제어하는 방법은?
2. `health` 엔드포인트가 로드밸런서·k8s에서 어떻게 쓰이는가?
3. 마이크로미터가 "측정 추상화"라는 말의 의미는? 모니터링 도구를 바꿔도 측정 코드가 그대로인 이유는?
4. Counter·Timer·Gauge는 각각 언제 쓰는가?
5. 프로메테우스가 pull(scrape) 방식이라는 것의 의미는? 애플리케이션·프로메테우스·그라파나의 역할 분담은?

## 원본 학습 자료

본 묶음은 김영한 인프런 강의 PDF(스프링 부트 8·9·10장)를 source로 재작성한 산출물입니다.

## 관련 문서

- [관측 가능성 통합 MOC](../README.md) — 06_observability 전체 진입점
- [`../02_LGTMStack/02-01.Grafana Core`](../02_LGTMStack/02-01.Grafana%20Core.md) — 메트릭을 수집·시각화하는 인프라
- [`../../11_spring/07_autoconfig/`](../../11_spring/07_autoconfig/) — 액츄에이터 엔드포인트가 자동 등록되는 원리
- [Spring Boot Reference — Actuator](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html) — 공식 문서
