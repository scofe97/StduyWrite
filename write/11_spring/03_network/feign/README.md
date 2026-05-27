---
title: Spring Cloud OpenFeign 학습 묶음 (압축본)
tags: [moc, spring, spring-boot, spring-cloud, openfeign, http-client, declarative]
status: draft
source:
  - https://docs.spring.io/spring-cloud-openfeign/docs/current/reference/html/
related:
  - ../README.md
  - ../webflux/README.md
updated: 2026-05-27
---

# Spring Cloud OpenFeign 학습 묶음 (압축본)

---

> Spring Cloud OpenFeign 은 "HTTP 호출 코드를 직접 쓰지 않는다" 라는 한 줄로 요약됩니다. 인터페이스 한 장에 어노테이션을 붙이면 Spring 이 런타임 프록시로 구현체를 만들어 줍니다. WebClient 가 *빌더로 호출을 조립* 하는 자리라면, OpenFeign 은 *시그니처로 호출을 선언* 하는 자리입니다.



## 왜 별도 묶음인가

> 같은 외부 HTTP 호출이지만 OpenFeign 은 *MSA 내부 서비스 호출* 자리를 중심으로 설계됐습니다. WebClient 한 묶음으로 외부 호출 전체를 덮기에는 두 패러다임이 너무 다르고, 한 자리에서 비교하는 편이 결정 트리가 명확해지기 때문에 본 묶음을 따로 둡니다.

본 묶음은 *압축본 2편* 으로 시작합니다. 풀 학습 묶음(설정·요청·응답·에러·인터셉터·테스트·실무사례 8~10편) 은 본인 프로젝트에서 OpenFeign 을 실제로 도입하기로 결정한 시점에 진행하는 편이 비용 대비 효과가 좋습니다. 압축본 2편을 다 읽으면 의사결정 — "지금 우리 프로젝트에 도입할 가치가 있는가" — 에 답할 수 있습니다.



## 학습 순서

> 두 편을 순서대로 따라가면 OpenFeign 의 본질과 진입 비용을 1시간 안에 손에 익힐 수 있습니다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [OpenFeign 입문과 WebClient 비교](01-01.OpenFeign%20입문과%20WebClient%20비교.md) | 등장 동기, WebClient·RestClient·OpenFeign 결정 트리, 의존성과 활성화, 최소 예제 |
| 01-02 | [기본 설정과 인터페이스 선언](01-02.기본%20설정과%20인터페이스%20선언.md) | `@FeignClient` 5속성, Spring MVC 어노테이션 재사용, application.yml 설정 (timeout·logging·retryer) |



## 환경과 버전

> 모든 코드 예제는 다음 조합에서 검증합니다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | 3.3.0 (2024-05) 이후 LTS 라인 |
| Spring Cloud | 2023.0.x | OpenFeign 4.x 라인이 묶여 있음 |
| spring-cloud-starter-openfeign | 4.x | Spring Cloud BOM 으로 버전 관리 |
| Java | 17+ | 21까지 호환 |



## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. Spring MVC 의 `@GetMapping`, `@PathVariable`, `@RequestBody` 어노테이션이 어떻게 동작하는지 한 문장으로 설명할 수 있다.
2. Spring Boot 프로젝트에 의존성을 추가하고 `@SpringBootApplication` 부트스트랩이 어떻게 작동하는지 안다.
3. RestTemplate 이나 WebClient 중 하나로 외부 HTTP 호출을 해 본 적이 있다 (비교 기준이 있어야 OpenFeign 의 가치가 보입니다).



## 면접 대비 체크리스트

> 2편을 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 합니다.

1. OpenFeign 은 어떤 자리에서 WebClient 보다 권장되는가? 결정의 핵심 기준은 무엇인가?
2. `@FeignClient(contextId=...)` 가 필요한 자리는 언제이며, 같은 `name` 으로 여러 인터페이스를 만들 때 어떤 충돌이 일어나는가?
3. `application.yml` 의 `spring.cloud.openfeign.client.config.{name}.*` 와 `@FeignClient(url=...)` 가 동시에 있으면 어느 쪽이 이깁니까?
4. OpenFeign 인터페이스에 Spring MVC 어노테이션 (`@GetMapping` 등) 을 그대로 쓸 수 있는 이유는 무엇인가?



## 관련 문서

- [Spring 네트워크 통신 학습 MOC](../README.md) — 두 갈래 (WebClient·OpenFeign) 진입점
- [Spring WebClient 학습 MOC](../webflux/README.md) — 같은 폴더의 반대편 갈래
- [Spring Cloud OpenFeign Reference](https://docs.spring.io/spring-cloud-openfeign/docs/current/reference/html/) — 본 묶음이 따라가는 공식 문서
