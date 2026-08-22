---
title: Spring Validation 학습 MOC
tags: [moc, spring, validation, bean-validation, binding-result]
status: draft
source:
  - https://docs.spring.io/spring-framework/reference/core/validation.html
related:
  - ../README.md
  - ../02_data-binding/README.md
updated: 2026-05-29
---

# Spring Validation 학습 MOC

---

> 바인딩이 끝난 직후 요청이 도메인 규칙을 만족하는지 확인하는 단계가 검증입니다. 가장 원초적인 수동 검증부터 표준 Bean Validation, 그리고 표준으로 안 되는 규칙을 직접 만드는 커스텀 제약까지를 한 묶음으로 모았습니다.


## 왜 02_data-binding 에서 분리했나

바인딩(요청 본문을 객체로 변환)과 검증(그 객체가 제약을 만족하는지 검사)은 `DispatcherServlet` 파이프라인에서 *서로 다른 단계* 입니다. 바인딩은 "값이 들어왔는가" 를, 검증은 "이 값이 비즈니스 규칙에 맞는가" 를 묻습니다. 원래 두 주제가 [`02_data-binding/`](../02_data-binding/README.md) 에 함께 있었지만, 검증만 해도 수동 검증·표준 어노테이션·그룹·커스텀 제약으로 나뉘어 분량이 커졌습니다. 그래서 검증을 별도 카테고리로 떼어, 바인딩 묶음은 요청·응답·파일·국제화에 집중하게 했습니다.

검증 메시지의 언어를 결정하는 국제화(`MessageSource`·`LocaleResolver`)는 검증 전용 주제가 아니라 응답 메시지 전반의 문제라 [`02_data-binding/03-01`](../02_data-binding/03-01.메시지·국제화%20—%20MessageSource와%20LocaleResolver.md) 에 그대로 두고, 본 묶음의 메시지 절이 그쪽을 cross-folder 로 참조합니다.

## 학습 순서

> 수동 검증으로 검증의 본질을 보고, 선언적 Bean Validation 으로 넘어간 뒤, 표준으로 안 되는 규칙을 커스텀 제약으로 만드는 순서입니다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [수동 검증과 BindingResult](01-01.수동%20검증과%20BindingResult.md) | `BindingResult` / `FieldError`·`ObjectError` / `rejectValue`·`reject` / `MessageCodesResolver` / `Validator` 분리 / BindingResult vs `@ControllerAdvice` |
| 01-02 | [Bean Validation과 그룹 검증](01-02.Bean%20Validation과%20그룹%20검증.md) | 표준 제약 어노테이션 / `@Valid` vs `@Validated` / 그룹 검증·Form 객체 분리 / `@RequestBody` 통합·`@ModelAttribute` 비교 / 메시지 외부화 |
| 02-01 | [커스텀 ConstraintValidator](02-01.커스텀%20ConstraintValidator.md) | `@Constraint` 메타 어노테이션 / `ConstraintValidator` `initialize`·`isValid` / `ConstraintValidatorContext` / 클래스 레벨·필드 간 제약 |

처음 보는 학습자는 01-01 부터 순서대로 따라갑니다. `@Valid` 와 `@Validated` 의 차이만 급하면 01-02 의 그룹 절로 직행해도 됩니다. 표준 제약으로 안 되는 규칙을 만들어야 한다면 02-01 을 봅니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-validation` 추가 시 검증 자동 구성 |
| Spring Framework | 6.2.x | `Validator`·`@Validated`·`WebDataBinder` |
| Bean Validation | Jakarta Bean Validation 3.x (Hibernate Validator) | `@NotNull`·`@Size`·`@Pattern` 등 표준 제약 + 커스텀 `ConstraintValidator` |
| Java | 17+ | |

## 관련 문서

- [Spring 통합 MOC](../README.md) — Spring 학습 문서 전체 진입점
- [Spring 데이터 바인딩 학습 MOC](../02_data-binding/README.md) — 검증의 전 단계인 바인딩 묶음
- [메시지·국제화 — MessageSource와 LocaleResolver](../02_data-binding/03-01.메시지·국제화%20—%20MessageSource와%20LocaleResolver.md) — 검증 메시지의 언어를 결정하는 국제화
- [Spring 공식 — Validation](https://docs.spring.io/spring-framework/reference/core/validation.html)
