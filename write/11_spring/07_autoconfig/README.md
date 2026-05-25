---
title: 스프링 부트 자동 구성과 외부 설정 학습 MOC
tags: [moc, spring-boot, auto-configuration, starter, external-config, profile]
status: draft
related:
  - ../README.md
  - ../01_core/README.md
updated: 2026-05-25
---

# 스프링 부트 자동 구성과 외부 설정 학습 MOC
---

> 스프링 부트가 "설정 없이 그냥 돌아가는" 경험을 만드는 두 축을 다룹니다. 하나는 라이브러리만 추가하면 빈이 자동 등록되는 *자동 구성*(01장), 다른 하나는 한 번 빌드한 산출물을 환경마다 다르게 동작시키는 *외부 설정*(02장)입니다. `01_core/` 가 "내가 직접 빈을 등록하고 주입하는" 스프링 컨테이너의 기본이라면, 본 묶음은 "스프링 부트가 빈을 자동으로 등록·설정하는" 메커니즘입니다.

## 왜 별도 묶음인가

`01_core/` 의 컨테이너는 개발자가 `@Bean` 이나 `@Component` 로 *직접* 빈을 등록하는 세계입니다. 그런데 실무에서 쓰는 스프링 부트 프로젝트는 `DataSource` 를 등록한 적이 없는데도 쓸 수 있습니다. 이 간극을 메우는 것이 자동 구성이고, 그 자동 구성을 환경별로 조정하는 것이 외부 설정과 프로필입니다. 경계를 한 문장으로 정하면 "01_core는 빈을 직접 등록·주입, 07_autoconfig는 부트가 빈을 자동 등록·설정"입니다.

## 학습 순서

| 장 | # | 문서 | 다루는 핵심 |
|----|---|------|-----------|
| 01 자동 구성 | 01-01 | [스타터와 라이브러리 버전 관리](01-01.스타터와%20라이브러리%20버전%20관리.md) | 라이브러리 직접 관리의 고통, BOM 버전 관리, 스타터 묶음 제공 |
| 01 자동 구성 | 01-02 | [자동 구성 — @AutoConfiguration과 @Conditional](01-02.자동%20구성%20—%20@AutoConfiguration과%20@Conditional.md) | 등록 안 한 빈이 존재하는 미스터리, @Conditional, ImportSelector, @EnableAutoConfiguration |
| 01 자동 구성 | 01-03 | [커스텀 스타터 만들기](01-03.커스텀%20스타터%20만들기.md) | 자동 구성 원리를 내 라이브러리에 적용, AutoConfiguration.imports 등록 |
| 02 외부 설정 | 02-01 | [외부 설정 — 커맨드라인부터 application.yml까지](02-01.외부%20설정%20—%20커맨드라인부터%20application.yml까지.md) | 네 가지 설정 통로, Environment 단일 창구, 우선순위 |
| 02 외부 설정 | 02-02 | [@ConfigurationProperties와 타입 안전 설정](02-02.@ConfigurationProperties와%20타입%20안전%20설정.md) | @Value vs @ConfigurationProperties, 생성자 바인딩, 시작 시점 검증 |
| 02 외부 설정 | 02-03 | [프로필 — 환경별 설정 분리](02-03.프로필%20—%20환경별%20설정%20분리.md) | 프로필별 파일, YAML 문서 분리, @Profile 빈 등록 |

처음 보는 학습자는 01-01 부터 순서대로 보면 됩니다. 01장이 "라이브러리만 넣으면 빈이 생기는" 자동 구성을 스타터 → 조건부 등록 → 커스텀 스타터 순으로 풀고, 02장이 "그 빈을 환경마다 다르게 설정하는" 외부 설정·프로필을 다룹니다. 01장 01-02(자동 구성 원리)가 본 묶음의 핵심이며, 면접에서 "스프링 부트의 자동 구성은 어떻게 동작하나"를 물으면 그 문서의 흐름이 답입니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.x | `AutoConfiguration.imports` 방식 (2.7+ 표준) |
| Spring Framework | 6.x | `@Conditional`, `Environment` |
| Java | 17+ | |
| 빌드 | Gradle + `io.spring.dependency-management` | BOM 적용(01-01) |

## 사전 지식

> 본 묶음은 다음을 안다고 가정합니다.

1. `@Bean` / `@Component` 로 빈을 직접 등록하는 방법 — 막히면 [`../01_core/01-01`](../01_core/01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) §5 를 봅니다.
2. 생성자 주입을 권장하는 이유 — [`../01_core/01-01`](../01_core/01-01.객체지향%20원리%20적용%20—%20DI와%20IoC.md) §6 (02-02 생성자 바인딩과 연결).

## 면접 대비 체크리스트

> 여섯 편을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. 스타터와 BOM은 각각 무엇을 책임지는가? 버전을 안 적어도 정해지는 이유는?
2. `DataSource` 를 등록한 적 없는데 주입되는 이유는? `@ConditionalOnClass`·`@ConditionalOnMissingBean` 의 역할은?
3. `ImportSelector` 와 `AutoConfiguration.imports` 는 자동 구성에서 무엇을 하는가?
4. 외부 설정의 네 통로와 우선순위는? `Environment` 는 무엇을 통일하는가?
5. `@Value` 와 `@ConfigurationProperties` 의 차이는? 후자가 타입 안전·검증에서 나은 이유는?
6. 프로필별 설정 파일 규칙과 `@Profile` 빈 등록은 어떻게 동작하는가?

## 원본 학습 자료

본 묶음은 김영한 인프런 강의 PDF(스프링 부트 4·5·6·7장)를 source로 재작성한 산출물입니다. 같은 주제를 다루던 노션 `_notion_import/msa/` 의 Cloud Config·외부설정 노트는 향후 통합 검토 대상입니다.

## 관련 문서

- [Spring 통합 MOC](../README.md) — 분산 배치된 Spring 문서 전체 진입점
- [`../01_core/`](../01_core/) — 빈을 직접 등록·주입하는 컨테이너 기본
- [Spring Boot Reference — Auto-configuration](https://docs.spring.io/spring-boot/reference/using/auto-configuration.html) — 공식 문서
- [Spring Boot Reference — External Config](https://docs.spring.io/spring-boot/reference/features/external-config.html) — 공식 문서
