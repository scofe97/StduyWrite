---
title: Spring 학습 통합 MOC
tags: [moc, spring, spring-boot]
status: final
related:
  - ../README.md
  - ../../../03_architecture/README.md
  - ../../../05_messaging/spring/README.md
  - ../../../06_data/spring/README.md
  - ../../../07_observability/spring/README.md
  - ../../../09_cloud/spring/README.md
  - ../../../11_security/02_spring-security/README.md
updated: 2026-05-09
---

# Spring 학습 통합 MOC
---
> Spring 문서는 주제별로 분산 배치된다. 이 페이지가 전 카테고리 집계점이 되어 Spring 공부자의 진입점 역할을 한다.

## 왜 분산 배치인가

하네스 §4.1은 "언어/프레임워크 중심 분류를 금지"한다. Spring Kafka 문서를 `05_messaging/`이 아닌 `spring/` 전용 폴더에 두면, "Kafka로 메시징을 구현하는 방법 비교"라는 주제 축이 깨진다. 대신 본 페이지가 논리층에서 모든 Spring 문서를 엮는다.

## 카테고리별 배치

### 여기 (`01_language/java/spring/`) — 언어·프레임워크 중립 지식

| 폴더 | 범위 |
|------|------|
| [01_core/](01_core/) | IoC, DI, AOP, Bean Lifecycle, ApplicationContext |
| [02_boot/](02_boot/) | auto-configuration, starter, profiles, properties |
| [03_web/](03_web/) | Spring MVC, Controller, Filter/Interceptor |
| [04_webflux/](04_webflux/) | Reactive, WebClient, Mono/Flux (2026-05-09 WebClient 11편 묶음 추가) |
| [05_testing/](05_testing/) | JUnit5/Mockito/MockMvc/@SpringBootTest/Testcontainers/EmbeddedKafka/ArchUnit/WireMock (2026-05-09 9편 묶음 추가) |
| [05_internals/](05_internals/) | Proxy 기반 AOP, ClassLoader, Reflection 심화 |

### 도메인별 통합 (다른 카테고리)

| 주제 | 경로 | 다루는 내용 |
|------|------|------------|
| 설계 철학 | [`03_architecture/`](../../../03_architecture/README.md) "10. 후속 주제" | IoC를 설계 패턴 관점으로, AOP의 Decorator 해석 (예정) |
| 메시징 | [`05_messaging/spring/`](../../../05_messaging/spring/) | `@KafkaListener`, Producer Config, Error Handler |
| 영속성 | [`06_data/spring/`](../../../06_data/spring/) | Spring Data JPA, R2DBC, `@Transactional`, [QueryDSL 6.12 학습 묶음](../../../06_data/spring/querydsl/README.md) |
| 관측성 | [`07_observability/spring/`](../../../07_observability/spring/) | Spring Actuator, Micrometer 통합 |
| 클라우드 | [`09_cloud/spring/`](../../../09_cloud/spring/) | Spring Cloud, Gateway, Config Server |
| 보안 | [`11_security/02_spring-security/`](../../../11_security/02_spring-security/) | Filter Chain, AuthenticationManager, Method Security |

## 전체 Spring 문서 목록 집계

태그 기반으로 전 카테고리에서 Spring 문서를 집계한다.

```bash
grep -rl "^  - spring$\|tags:.*spring" write/ --include="*.md" | sort
```

결과는 월간 리뷰에서 이 MOC 하단에 스냅샷으로 기록한다.

## 학습 경로 추천

처음 Spring을 배운다면 다음 순서를 권장한다.

1. **`01_core/`** — IoC와 DI를 왜 쓰는지부터. Pure Java로 같은 구조 구현 후 비교
2. **`02_boot/`** — Spring Boot가 설정을 어떻게 숨기는지 (auto-config 메커니즘)
3. **`03_web/`** — 가장 흔히 만나는 MVC 흐름
4. **도메인별** — 본인 관심 영역 선택. 메시징이면 `05_messaging/spring/`, 데이터면 `06_data/spring/`

## 이관 진척

`poc/10_Spring/` → 여기로의 이관은 청크 단위로 진행한다. 진척 상태는 `STUDY_INDEX.md` 하단의 이관 표에서 확인한다.
