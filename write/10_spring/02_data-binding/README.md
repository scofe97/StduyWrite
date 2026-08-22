---
title: Spring 데이터 바인딩 학습 MOC
tags: [moc, spring, spring-boot, spring-mvc, data-binding, message-converter, multipart, i18n]
status: draft
source:
  - https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-methods/requestmapping.html
  - https://docs.spring.io/spring-framework/reference/core/validation.html
related:
  - ../README.md
  - ../01_core/
  - ../03_network/
updated: 2026-05-23
---

# Spring 데이터 바인딩 학습 MOC

---

> `DispatcherServlet` 이 받은 HTTP 요청을 컨트롤러 파라미터로 만들고, 컨트롤러 반환값을 HTTP 응답으로 직렬화하는 *바인딩 계층* 을 모은 묶음입니다. `@RequestParam`/`@RequestBody` 가 어떻게 동작하는지부터 Jackson 의 `ObjectMapper`, Multipart 파일 업로드, 그리고 응답·검증 메시지의 언어를 결정하는 메시지·국제화까지 한 흐름으로 정리합니다. 입력 검증(Bean Validation)은 분량이 커져 [`09_validation/`](../09_validation/README.md) 으로 분리했고, 본 묶음의 국제화 편이 검증 메시지를 cross-folder 로 잇습니다.

## 왜 별도 묶음인가

`01_core/` 의 MVC(03장) 묶음은 `DispatcherServlet` 의 *호출 흐름* 과 핸들러 어댑터 구조까지를 다룹니다. 그러나 요청 데이터를 어떻게 받고, 응답을 어떻게 직렬화하는지는 그 자체로 결정해야 할 것이 많아 별도 묶음이 필요합니다. 본 묶음은 다음 질문에 답합니다.

1. JSON 바디는 어떤 경로로 도메인 객체가 되는가? (`HttpMessageConverter` → `ObjectMapper`)
2. 같은 요청 데이터를 `@RequestParam`·`@ModelAttribute`·`@RequestBody` 중 어떤 어노테이션으로 받아야 하는가?
3. 파일 업로드와 일반 JSON 은 왜 처리 경로가 다른가? (`MultipartFile`, `@RequestPart`)
4. 응답·검증 메시지의 언어는 누가·언제·어디서 결정하는가? (`MessageSource`, `LocaleResolver`)

입력 검증을 어디에 둘지 — `BindingResult`·`@Valid`·`@Validated` — 는 별도 카테고리 [`09_validation/`](../09_validation/README.md) 에서 다룹니다.

## 학습 순서

> 1장은 *바인딩 자체* (요청·응답·파일), 3장은 그 위에서 *응답·검증 메시지의 언어를 결정* 하는 국제화입니다. 검증(옛 2장)은 [`09_validation/`](../09_validation/README.md) 으로 분리됐습니다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [HTTP 요청·응답과 메시지 컨버터](01-01.HTTP%20요청·응답과%20메시지%20컨버터.md) | DTO 패턴 / `@RequestParam`·`@PathVariable`·`@ModelAttribute`·`@RequestBody`·`@RequestHeader` / `@ResponseBody`·`@RestController`·`@ResponseStatus` / `Converter`·`Formatter`·`ConversionService` / `HttpMessageConverter` / Jackson `ObjectMapper` |
| 01-02 | [파일 업로드 — Multipart](01-02.파일%20업로드%20—%20Multipart.md) | `multipart/form-data` 바디 / `spring.servlet.multipart.*` 설정 / `MultipartFile` / `@RequestPart` / 파일 저장·다운로드 / WebFlux 와의 차이 |
| 01-03 | [JSON 직렬화 심화 — 커스텀 Serializer·@JsonView·다형성](01-03.JSON%20직렬화%20심화%20—%20커스텀%20Serializer·@JsonView·다형성.md) | 커스텀 `JsonSerializer`/`JsonDeserializer`·`@JsonComponent` / `@JsonView` 화면별 노출 / `@JsonTypeInfo`·`@JsonSubTypes` 다형성 / default typing 보안 주의 |
| 01-04 | [메시지 컨버터 자동 설정 — WebMvcAutoConfiguration과 등록 결정](01-04.메시지%20컨버터%20자동%20설정%20—%20WebMvcAutoConfiguration과%20등록%20결정.md) | `WebMvcAutoConfiguration` 기본 컨버터 / `Jackson2ObjectMapperBuilderCustomizer` / `configureMessageConverters` vs `extendMessageConverters` / `@EnableWebMvc` opt-out 함정 |
| 03-01 | [메시지·국제화 — MessageSource와 LocaleResolver](03-01.메시지·국제화%20—%20MessageSource와%20LocaleResolver.md) | `MessageSource` 자동 구성 / Locale 폴백 체인 / `LocaleResolver` 3종 (Accept-Header·Session·Cookie) / `LocaleChangeInterceptor` / `LocaleContextHolder` ThreadLocal / 검증 메시지와의 연결 |

처음 보는 학습자는 01-01 부터 순서대로 따라갑니다. 파일 업로드만 급하다면 01-02 로 직행해도 됩니다. 입력 검증을 어디에 둘지 헷갈리는 단계라면 [`09_validation/01-01`](../09_validation/01-01.수동%20검증과%20BindingResult.md) 부터 봅니다. 다국어 응답이 *어느 Locale 로 결정되는지* 가 막막하다면 03-01 의 §3 (LocaleResolver 3 종) 과 §5 (한 흐름으로) 를 먼저 봅니다.

## 환경과 버전

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.3.x | `spring-boot-starter-web` 가 Jackson·Bean Validation 자동 구성 |
| Spring Framework | 6.2.x | `HttpMessageConverter`·`HandlerMethodArgumentResolver` API |
| Jakarta | jakarta.* | `javax.validation` 미사용 |
| Jackson | 2.x | `ObjectMapper`·`@JsonProperty`·`@JsonInclude` |
| Bean Validation | Jakarta Bean Validation 3.x (Hibernate Validator) | `@NotNull`·`@Size`·`@Email`·`@Pattern` 등 표준 제약 |

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. `DispatcherServlet` 이 요청을 어떤 흐름으로 컨트롤러까지 보내는지 한 문장으로 설명할 수 있습니다. (모르면 [`../01_core/01-01`](../01_core/03-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) 의 §4 참고)
2. `@Controller`·`@RestController` 의 차이를 알고, 컨트롤러 메서드 시그니처에 어떤 파라미터를 둘 수 있는지 한 가지 이상 떠올릴 수 있습니다.
3. JSON 의 구조(객체·배열·기본 타입)와 Java POJO 의 매핑이 무엇인지 감이 있습니다.

## 면접 대비 체크리스트

> 본 묶음을 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 합니다. (검증 관련 질문은 [`09_validation/`](../09_validation/README.md) 의 면접 체크리스트로 옮겼습니다.)

1. 같은 요청 데이터를 `@RequestParam`·`@ModelAttribute`·`@RequestBody` 중 어떻게 고르나요? 각각 어떤 `HandlerMethodArgumentResolver` 가 처리합니까?
2. `Converter`·`Formatter`·`HttpMessageConverter` 셋의 책임을 한 문장씩으로 구분할 수 있나요?
3. Jackson `ObjectMapper` 의 직렬화·역직렬화 흐름에서 `@JsonProperty`·`@JsonInclude(NON_NULL)` 가 끼어드는 지점은 어디인가요?
4. `multipart/form-data` 바디는 일반 JSON 과 비교해 어디가 다르고, `@RequestPart` 는 `@RequestParam` 과 어떻게 다른가요?
5. `LocaleResolver` 의 기본 구현체 세 가지와 각각의 Locale 출처는? `LocaleChangeInterceptor` 가 `AcceptHeaderLocaleResolver` 와 함께 쓰면 안 되는 이유는?

## 관련 문서

- [Spring 통합 MOC](../README.md) — Spring 학습 문서 전체 진입점
- [Spring MVC — FrontController 에서 DispatcherServlet 까지](../01_core/03-01.Spring%20MVC%20—%20FrontController에서%20DispatcherServlet까지.md) — 본 묶음의 전제. `DispatcherServlet` 흐름과 핸들러 어댑터 구조
- [예외 처리 — 서블릿에서 @ControllerAdvice 까지](../01_core/03-02.예외%20처리%20—%20서블릿에서%20@ControllerAdvice까지.md) — 검증 실패를 전역에서 잡는 방법
- [Spring Validation 학습 MOC](../09_validation/README.md) — 바인딩 다음 단계인 입력 검증 (옛 02-01 이 분리·확장된 자리)
- [Spring WebClient 학습 MOC](../03_network/webflux/README.md) — 반대편(아웃바운드) 의 바디 직렬화·역직렬화

## 후속 편 계획

> 검토하던 두 방향을 모두 작성 완료했습니다. 1장(바인딩) 연장으로 [`01-03`](01-03.JSON%20직렬화%20심화%20—%20커스텀%20Serializer·@JsonView·다형성.md)·[`01-04`](01-04.메시지%20컨버터%20자동%20설정%20—%20WebMvcAutoConfiguration과%20등록%20결정.md) 에 둡니다.

- ✅ **JSON 직렬화 심화** — [`01-03`](01-03.JSON%20직렬화%20심화%20—%20커스텀%20Serializer·@JsonView·다형성.md): 커스텀 `JsonSerializer`/`JsonDeserializer`, `@JsonView`, `@JsonTypeInfo` 다형성.
- ✅ **메시지 컨버터 자동 설정** — [`01-04`](01-04.메시지%20컨버터%20자동%20설정%20—%20WebMvcAutoConfiguration과%20등록%20결정.md): `WebMvcAutoConfiguration` 기본 컨버터, `extendMessageConverters` vs `configureMessageConverters` 결정 트리.
