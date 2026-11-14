---
title: Spring 개발 키워드
tags: [keywords, spring, spring-boot, aop, transaction, webflux, security]
status: final
source:
  - ../09_spring/README.md
  - ../09_spring/books/spring-start-here/README.md
related:
  - ../README.md
  - ../01_language/jvm-keywords.md
  - ../05_data/data-keywords.md
  - ../06_observability/observability-keywords.md
updated: 2026-11-03
---

# Spring 개발 키워드
---

> Spring 개발 키워드 표. 문서를 쓸 때 참고합니다.



## 1단계 · 컨테이너와 빈

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| IoC 와 DI — 제어의 역전 | 필수 | [DI와 IoC](../09_spring/01_core/01-01.%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%20%EC%9B%90%EB%A6%AC%20%EC%A0%81%EC%9A%A9%20%E2%80%94%20DI%EC%99%80%20IoC.md) | Spring Start Here 2·3장 |
| BeanDefinition 이 먼저다 | 필수 | [DI와 IoC](../09_spring/01_core/01-01.%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%20%EC%9B%90%EB%A6%AC%20%EC%A0%81%EC%9A%A9%20%E2%80%94%20DI%EC%99%80%20IoC.md) | |
| 빈 팩토리와 컨텍스트 | 필수 | [Context와 Bean](../09_spring/books/spring-start-here/02.Spring%20Context%EC%99%80%20Bean%20%EB%93%B1%EB%A1%9D.md) | Spring Start Here 2장 |
| 컴포넌트 스캔과 등록 | 필수 | [Context와 Bean](../09_spring/books/spring-start-here/02.Spring%20Context%EC%99%80%20Bean%20%EB%93%B1%EB%A1%9D.md) | Spring Start Here 2장 |
| 주입 방식과 순환 참조 | 필수 | [와이어링](../09_spring/books/spring-start-here/03.Bean%20%EC%99%80%EC%9D%B4%EC%96%B4%EB%A7%81%EA%B3%BC%20%EC%9D%98%EC%A1%B4%EC%84%B1%20%EC%A3%BC%EC%9E%85.md) | Spring Start Here 3장 |
| 스코프와 생명주기 | 필수 | [스코프와 생애주기](../09_spring/books/spring-start-here/05.Bean%20%EC%8A%A4%EC%BD%94%ED%94%84%EC%99%80%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0.md) | Spring Start Here 5장 |
| 추상화로 갈아 끼우기 | 추천 | [추상화와 DI](../09_spring/books/spring-start-here/04.%EC%B6%94%EC%83%81%ED%99%94%EC%99%80%20%EC%9D%98%EC%A1%B4%EC%84%B1%20%EC%A3%BC%EC%9E%85.md) | Spring Start Here 4장 |
| Spring 이 쓰는 디자인 패턴 | 추천 | [Spring과 디자인 패턴](../09_spring/01_core/01-02.Spring%EA%B3%BC%20%EB%94%94%EC%9E%90%EC%9D%B8%20%ED%8C%A8%ED%84%B4.md) | |
| 웹 스코프와 로그인 | 선택 | [웹 스코프](../09_spring/books/spring-start-here/09.%EC%9B%B9%20%EC%8A%A4%EC%BD%94%ED%94%84%EC%99%80%20%EB%A1%9C%EA%B7%B8%EC%9D%B8.md) | Spring Start Here 9장 |
| 옵저버 패턴 · 메디에이터 패턴 · 커맨드 패턴 · 쿼리 패턴 · 이벤트 패턴 · 체인 오브 리스폰시빌리티 · 정책 패턴 | 선택 | [옵저버 패턴](../01_language/java/03_DesignPatterns/01-04.%ED%96%89%EB%8F%99%20%ED%8C%A8%ED%84%B4.md) · [체인 오브 리스폰시빌리티](../01_language/java/03_DesignPatterns/01-04.%ED%96%89%EB%8F%99%20%ED%8C%A8%ED%84%B4.md) | |
| 퍼사드 패턴 · 어댑터 패턴 · 브리지 패턴 · 프록시 패턴 · 데코레이터 패턴 | 선택 | [퍼사드 패턴](../01_language/java/03_DesignPatterns/01-03.%EA%B5%AC%EC%A1%B0%20%ED%8C%A8%ED%84%B4.md) · [어댑터 패턴](../01_language/java/03_DesignPatterns/01-03.%EA%B5%AC%EC%A1%B0%20%ED%8C%A8%ED%84%B4.md) | |
| 플라이웨이트 패턴 · 컴포지트 패턴 | 선택 | | |
| 빌더 패턴 · 싱글턴 패턴 | 선택 | | |
| 함수형 프로그래밍 · 객체지향 프로그래밍 · 순수 함수 · 불변성 · 고차 함수 · 함수 합성 · 참조 투명성 · 부수 효과 제어 · 메서드 체이닝 · 객체 수명주기 | 선택 | | |
| 전략 패턴 | 선택 | [전략 패턴](../01_language/java/03_DesignPatterns/01-04.%ED%96%89%EB%8F%99%20%ED%8C%A8%ED%84%B4.md) | |



## 2단계 · 프록시와 AOP

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 횡단 관심사란 무엇인가 | 필수 | [횡단 관심사와 AOP](../09_spring/05_aop/01-01.%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC%EC%99%80%20AOP%20%E2%80%94%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%ED%92%80%EC%96%B4%EB%82%B4%EA%B8%B0.md) | Spring Start Here 6장 |
| 동적 프록시와 CGLIB | 필수 | [횡단 관심사와 AOP](../09_spring/05_aop/01-01.%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC%EC%99%80%20AOP%20%E2%80%94%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%ED%92%80%EC%96%B4%EB%82%B4%EA%B8%B0.md) | |
| 빈 후처리기가 끼워 넣는다 | 필수 | [횡단 관심사와 AOP](../09_spring/05_aop/01-01.%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC%EC%99%80%20AOP%20%E2%80%94%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%ED%92%80%EC%96%B4%EB%82%B4%EA%B8%B0.md) | |
| @Aspect 와 포인트컷 | 필수 | [Spring AOP](../09_spring/books/spring-start-here/06.Spring%20AOP%EC%99%80%20Aspect.md) | Spring Start Here 6장 |
| 자기 호출이 프록시를 지나침 | 필수 | [횡단 관심사와 AOP](../09_spring/05_aop/01-01.%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC%EC%99%80%20AOP%20%E2%80%94%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%ED%92%80%EC%96%B4%EB%82%B4%EA%B8%B0.md) | |
| 템플릿·콜백과 ThreadLocal | 추천 | [템플릿·ThreadLocal](../09_spring/05_aop/01-03.%ED%85%9C%ED%94%8C%EB%A6%BF%C2%B7%EC%BD%9C%EB%B0%B1%EA%B3%BC%20ThreadLocal%20%E2%80%94%20AOP%20%EB%93%B1%EC%9E%A5%20%EC%A7%81%EC%A0%84%EC%9D%98%20%EB%91%90%20%EC%8B%9C%EB%8F%84.md) | |
| 어노테이션 기반 응용 | 추천 | [어노테이션 AOP](../09_spring/05_aop/01-04.%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EA%B8%B0%EB%B0%98%20AOP%20%EC%9D%91%EC%9A%A9%20%E2%80%94%20%40Async%C2%B7%40Cacheable%C2%B7%40Retryable.md) | |
| 감사 로그 — 마커 어노테이션 · AOP · ThreadLocal 로 변경 전후 값 남기기 | 선택 |  |  |
| 위빙 네 방식과 AspectJ | 선택 | | |
| 미들웨어 · 인터셉터 | 선택 | [미들웨어](../01_language/book/lgo_learning-go/13-04.net-http%20%EB%8A%94%20%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%84%20%EC%A7%81%EC%A0%91%20%EC%A0%95%ED%95%98%EA%B3%A0%20%EB%AF%B8%EB%93%A4%EC%9B%A8%EC%96%B4%EB%8A%94%20Handler%20%EB%A5%BC%20%EA%B0%90%EC%8B%B8%EB%A9%B0%20slog%20%EB%A1%9C%20%EA%B5%AC%EC%A1%B0%ED%99%94%20%EB%A1%9C%EA%B7%B8%EB%A5%BC%20%EB%82%A8%EA%B9%81%EB%8B%88%EB%8B%A4.md) · [인터셉터](../09_spring/05_aop/01-01.%ED%9A%A1%EB%8B%A8%20%EA%B4%80%EC%8B%AC%EC%82%AC%EC%99%80%20AOP%20%E2%80%94%20%ED%94%84%EB%A1%9D%EC%8B%9C%EB%A1%9C%20%ED%92%80%EC%96%B4%EB%82%B4%EA%B8%B0.md) | |



## 3단계 · 요청 처리

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| WAS 와 서블릿 컨테이너 | 필수 | [WAS와 서블릿](../09_spring/01_core/02-01.WAS%EC%99%80%20%EC%84%9C%EB%B8%94%EB%A6%BF%20%E2%80%94%20HTTP%20%EC%B2%98%EB%A6%AC%EC%9D%98%20%ED%86%A0%EB%8C%80.md) | |
| 내장 톰캣과 SpringApplication | 필수 | [내장 톰캣](../09_spring/01_core/02-02.%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3%EA%B3%BC%20SpringApplication%20%E2%80%94%20JAR%EB%A1%9C%20WAS%EB%A5%BC%20%ED%92%88%EB%8B%A4.md) | Spring in Action 부록 |
| DispatcherServlet 흐름 | 필수 | [Spring MVC](../09_spring/01_core/03-01.Spring%20MVC%20%E2%80%94%20FrontController%EC%97%90%EC%84%9C%20DispatcherServlet%EA%B9%8C%EC%A7%80.md) | Spring in Action 2장 |
| 핸들러 매핑과 어댑터 | 필수 | [Spring MVC](../09_spring/01_core/03-01.Spring%20MVC%20%E2%80%94%20FrontController%EC%97%90%EC%84%9C%20DispatcherServlet%EA%B9%8C%EC%A7%80.md) | |
| 메시지 컨버터와 Jackson | 필수 | [메시지 컨버터](../09_spring/02_data-binding/01-01.HTTP%20%EC%9A%94%EC%B2%AD%C2%B7%EC%9D%91%EB%8B%B5%EA%B3%BC%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EC%BB%A8%EB%B2%84%ED%84%B0.md) | Spring in Action 7장 |
| 예외 처리 — @ControllerAdvice | 필수 | [예외 처리](../09_spring/01_core/03-02.%EC%98%88%EC%99%B8%20%EC%B2%98%EB%A6%AC%20%E2%80%94%20%EC%84%9C%EB%B8%94%EB%A6%BF%EC%97%90%EC%84%9C%20%40ControllerAdvice%EA%B9%8C%EC%A7%80.md) | |
| 검증 · 바인딩 · 타입 변환 | 필수 | [메시지 컨버터](../09_spring/02_data-binding/01-01.HTTP%20%EC%9A%94%EC%B2%AD%C2%B7%EC%9D%91%EB%8B%B5%EA%B3%BC%20%EB%A9%94%EC%8B%9C%EC%A7%80%20%EC%BB%A8%EB%B2%84%ED%84%B0.md) | Spring in Action 2장 |
| 파일 업로드와 멀티파트 | 추천 | [파일 업로드](../09_spring/02_data-binding/01-02.%ED%8C%8C%EC%9D%BC%20%EC%97%85%EB%A1%9C%EB%93%9C%20%E2%80%94%20Multipart.md) | |
| JSON 직렬화 심화 | 추천 | [JSON 직렬화 심화](../09_spring/02_data-binding/01-03.JSON%20%EC%A7%81%EB%A0%AC%ED%99%94%20%EC%8B%AC%ED%99%94%20%E2%80%94%20%EC%BB%A4%EC%8A%A4%ED%85%80%20Serializer%C2%B7%40JsonView%C2%B7%EB%8B%A4%ED%98%95%EC%84%B1.md) | |
| 컨버터 자동 설정 | 추천 | [컨버터 자동 설정](../09_spring/02_data-binding/01-04.%EB%A9%94%EC%8B%9C%EC%A7%80%20%EC%BB%A8%EB%B2%84%ED%84%B0%20%EC%9E%90%EB%8F%99%20%EC%84%A4%EC%A0%95%20%E2%80%94%20WebMvcAutoConfiguration%EA%B3%BC%20%EB%93%B1%EB%A1%9D%20%EA%B2%B0%EC%A0%95.md) | |
| REST 서비스 만들고 소비하기 | 필수 | [REST 서비스](../09_spring/books/spring-start-here/10.REST%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) | Spring Start Here 10·11장 |
| 메시지와 국제화 | 선택 | [메시지·국제화](../09_spring/02_data-binding/03-01.%EB%A9%94%EC%8B%9C%EC%A7%80%C2%B7%EA%B5%AD%EC%A0%9C%ED%99%94%20%E2%80%94%20MessageSource%EC%99%80%20LocaleResolver.md) | |
| 리소스 지향 설계 · 액션 지향 설계 · HATEOAS · 하이퍼미디어 · 콘텐츠 타입 협상 | 선택 | | |
| GraphQL · 데이터 로더 · 프로토콜 버퍼 | 선택 | [GraphQL](../03_architecture/book/bytebytego-system-design/03-02.API%20%EB%8A%94%20SOAP%C2%B7REST%C2%B7GraphQL%C2%B7RPC%20%EB%A1%9C%20%EA%B0%88%EB%A6%AC%EA%B3%A0%20%ED%86%A0%ED%81%B0%C2%B7HMAC%C2%B7SSO%C2%B7%EC%86%94%ED%8A%B8%20%ED%95%B4%EC%8B%9C%EA%B0%80%20%EC%A0%91%EA%B7%BC%EA%B3%BC%20%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%EB%A5%BC%20%EC%A7%80%ED%82%A8%EB%8B%A4.md) · [프로토콜 버퍼](../02_os/book/npg_network-programming-with-go/12-01.%EC%A7%81%EB%A0%AC%ED%99%94%EB%8A%94%20%EA%B5%AC%EC%A1%B0%EC%B2%B4%EB%A5%BC%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%A1%9C%20%EB%B0%94%EA%BE%B8%EA%B3%A0%20JSON%20%EC%9D%80%20%EC%82%AC%EB%9E%8C%EC%9D%B4%2C%20Gob%20%EC%9D%80%20Go%20%EA%B0%80%2C%20protobuf%20%EB%8A%94%20%EC%97%AC%EB%9F%AC%20%EC%96%B8%EC%96%B4%EA%B0%80%20%EC%9D%BD%EB%8A%94%EB%8B%A4.md) | |
| API 버저닝 | 선택 | | |
| HTTP 메서드 · Problem Details 에러 응답 | 선택 | [HTTP 메서드](../09_spring/books/spring-start-here/08.%EB%8F%99%EC%A0%81%20%EB%B7%B0%EC%99%80%20HTTP%20%EB%8D%B0%EC%9D%B4%ED%84%B0.md) | |
| JSON-MessagePack 직렬화 · 스트리밍 응답 | 선택 | | |
| 오프셋 페이지네이션 · 커서 기반 페이지네이션 · 배치 API | 선택 | | |
| 키셋 페이지네이션 · 안정 정렬 키 | 선택 | | |
| 웹훅 검증 · 웹훅 재시도 | 선택 | [웹훅 검증](../07_devops/02_Jenkins/05_operations/02-06a.Webhook%EA%B3%BC%20%EC%99%B8%EB%B6%80%20%EC%97%B0%EB%8F%99.md) · [웹훅 재시도](../07_devops/02_Jenkins/05_operations/02-06a.Webhook%EA%B3%BC%20%EC%99%B8%EB%B6%80%20%EC%97%B0%EB%8F%99.md) | |



## 4단계 · 트랜잭션과 이벤트

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| @Transactional 내부 구조 | 필수 | [스프링 트랜잭션](../05_data/03_persistence/jpa/04-01.%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98.md) | Spring Start Here 13장 |
| 전파 · 격리 · 동기화 | 필수 | [트랜잭션 전파 활용](../05_data/03_persistence/jpa/04-01b.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EC%A0%84%ED%8C%8C%20%ED%99%9C%EC%9A%A9.md) | Spring Start Here 13장 |
| 영속성 컨텍스트와 N+1 | 필수 | [프록시와 N+1](../05_data/03_persistence/jpa/03-03.%ED%94%84%EB%A1%9D%EC%8B%9C%EC%99%80%20N%2B1.md) | Spring in Action 3장 |
| 낙관적 · 비관적 락 | 추천 | [낙관적 비관적 락](../05_data/03_persistence/jpa/04-02.%EB%82%99%EA%B4%80%EC%A0%81%20%EB%B9%84%EA%B4%80%EC%A0%81%20%EB%9D%BD.md) | |
| MyBatis 와 JPA 혼용 | 추천 | [도구 혼용 패턴](../05_data/03_persistence/jpa/07-01.%EB%8F%84%EA%B5%AC%20%ED%98%BC%EC%9A%A9%20%ED%8C%A8%ED%84%B4.md) | |
| Spring Data 리포지토리 | 추천 | [Spring Data JPA](../05_data/03_persistence/jpa/03-01.Spring%20Data%20JPA%20%EA%B3%B5%ED%86%B5%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4.md) | Spring Start Here 14장 |
| 두 리스너의 차이 | 필수 | [두 리스너](../09_spring/06_events/01-01.%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EC%99%80%20%EB%91%90%20%EB%A6%AC%EC%8A%A4%EB%84%88%20%E2%80%94%20%40EventListener%20vs%20%40TransactionalEventListener.md) | |
| 커밋 전후 Phase 와 전파 | 필수 | [리스너 내부 동작](../09_spring/06_events/01-03.%40TransactionalEventListener%20%EB%82%B4%EB%B6%80%20%EB%8F%99%EC%9E%91%20%EC%9B%90%EB%A6%AC.md) | |
| 죽은 트랜잭션 피하기 | 필수 | [죽은 트랜잭션](../09_spring/06_events/01-02.%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%20%EC%A0%84%ED%8C%8C%20%EC%A1%B0%ED%95%A9%20%E2%80%94%20%EC%A3%BD%EC%9D%80%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98%EA%B3%BC%20REQUIRES_NEW.md) | |
| 동기와 비동기 이벤트 · 보상 | 추천 | [비동기 이벤트](../09_spring/06_events/01-04.%EB%8F%99%EA%B8%B0%EC%99%80%20%EB%B9%84%EB%8F%99%EA%B8%B0%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%E2%80%94%20%40Async%EC%99%80%20%EB%B3%B4%EC%83%81%20%ED%8A%B8%EB%9E%9C%EC%9E%AD%EC%85%98.md) | |
| 도메인 주도 설계 | 선택 | [도메인 주도 설계](../07_devops/book/cicd_cicd-patterns/08-01.Domain%20Driven%20Design%20Patterns%20for%20Regulated%20Sectors.md) | |
| 리포지토리 패턴 · 유닛 오브 워크 · 스펙 패턴 | 선택 | [리포지토리 패턴](../05_data/03_persistence/jpa/03-05.%EC%BB%A4%EC%8A%A4%ED%85%80%20%EB%A6%AC%ED%8F%AC%EC%A7%80%ED%86%A0%EB%A6%AC%20%ED%8C%A8%ED%84%B4.md) · [유닛 오브 워크](../03_architecture/04_ddd/02-03.Domain%20Service%2C%20Factory%2C%20Repository.md) | |



## 5단계 · 부트가 조립하는 세계

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 스타터와 BOM 버전 관리 | 필수 | [스타터와 버전 관리](../09_spring/07_autoconfig/01-01.%EC%8A%A4%ED%83%80%ED%84%B0%EC%99%80%20%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC%20%EB%B2%84%EC%A0%84%20%EA%B4%80%EB%A6%AC.md) | |
| 자동 구성과 @Conditional | 필수 | [자동 구성](../09_spring/07_autoconfig/01-02.%EC%9E%90%EB%8F%99%20%EA%B5%AC%EC%84%B1%20%E2%80%94%20%40AutoConfiguration%EA%B3%BC%20%40Conditional.md) | |
| 순서 · 게이트 · 기본값 | 필수 | [자동 구성 심화](../09_spring/07_autoconfig/01-04.%EC%9E%90%EB%8F%99%20%EA%B5%AC%EC%84%B1%20%EC%8B%AC%ED%99%94%20%E2%80%94%20%EC%88%9C%EC%84%9C%C2%B7%EA%B2%8C%EC%9D%B4%ED%8A%B8%C2%B7%EA%B8%B0%EB%B3%B8%EA%B0%92%20%EC%A3%BC%EC%9E%85.md) | |
| 커스텀 스타터 만들기 | 추천 | [커스텀 스타터 만들기](../09_spring/07_autoconfig/01-03.%EC%BB%A4%EC%8A%A4%ED%85%80%20%EC%8A%A4%ED%83%80%ED%84%B0%20%EB%A7%8C%EB%93%A4%EA%B8%B0.md) | |
| 외부 설정 우선순위 | 필수 | [외부 설정](../09_spring/07_autoconfig/02-01.%EC%99%B8%EB%B6%80%20%EC%84%A4%EC%A0%95%20%E2%80%94%20%EC%BB%A4%EB%A7%A8%EB%93%9C%EB%9D%BC%EC%9D%B8%EB%B6%80%ED%84%B0%20application.yml%EA%B9%8C%EC%A7%80.md) | Spring in Action 6장 |
| @ConfigurationProperties | 필수 | [@ConfigurationProperties](../09_spring/07_autoconfig/02-02.%40ConfigurationProperties%EC%99%80%20%ED%83%80%EC%9E%85%20%EC%95%88%EC%A0%84%20%EC%84%A4%EC%A0%95.md) | Spring in Action 6장 |
| 프로필로 환경 가르기 | 필수 | [프로필](../09_spring/07_autoconfig/02-03.%ED%94%84%EB%A1%9C%ED%95%84%20%E2%80%94%20%ED%99%98%EA%B2%BD%EB%B3%84%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC.md) | |
| 설정과 비밀 관리 | 추천 | [외부화 설정](../09_spring/books/cloud-native-spring-in-action/04.%EC%99%B8%EB%B6%80%ED%99%94%20%EC%84%A4%EC%A0%95%20%EA%B4%80%EB%A6%AC.md) | Cloud Native Spring 4·14장 |



## 6단계 · 외부 통신과 회복탄력성

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 클라이언트 네 갈래 비교 | 필수 | [WebClient 입문](../09_spring/03_network/webflux/01-01.WebClient%20%EC%9E%85%EB%AC%B8%EA%B3%BC%20RestTemplate%C2%B7RestClient%20%EB%B9%84%EA%B5%90.md) | |
| WebClient 빌드와 요청 | 필수 | [WebClient 빌드](../09_spring/03_network/webflux/01-02.WebClient%20%EB%B9%8C%EB%93%9C%EC%99%80%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EC%84%A4%EC%A0%95.md) | |
| 응답 처리와 에러 · 재시도 | 필수 | [에러 처리와 재시도](../09_spring/03_network/webflux/01-05.%EC%97%90%EB%9F%AC%20%EC%B2%98%EB%A6%AC%EC%99%80%20%EC%9E%AC%EC%8B%9C%EB%8F%84.md) | |
| 필터 함수로 공통 관심사 | 추천 | [ExchangeFilterFunction](../09_spring/03_network/webflux/01-06.ExchangeFilterFunction.md) | |
| block 안티패턴 | 필수 | [block 안티패턴](../09_spring/03_network/webflux/02-02.%EB%8F%99%EA%B8%B0%C2%B7%EB%B9%84%EB%8F%99%EA%B8%B0%20%EA%B2%B0%EC%A0%95%20%28block%20%EC%95%88%ED%8B%B0%ED%8C%A8%ED%84%B4%29.md) | |
| OpenFeign 선언형 호출 | 추천 | [Feign 기본 설정](../09_spring/03_network/feign/01-02.%EA%B8%B0%EB%B3%B8%20%EC%84%A4%EC%A0%95%EA%B3%BC%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%20%EC%84%A0%EC%96%B8.md) | |
| 상태 코드 실패와 무응답 실패 | 필수 | [Feign 에러 모델](../09_spring/03_network/feign/01-03.%EC%97%90%EB%9F%AC%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20%EC%83%81%ED%83%9C%20%EC%BD%94%EB%93%9C%20%EC%8B%A4%ED%8C%A8%20vs%20%EB%AC%B4%EC%9D%91%EB%8B%B5%20%EC%8B%A4%ED%8C%A8.md) | |
| Resilience4j 도입 결정 | 필수 | [Resilience4j 개요](../09_spring/03_network/resilience/01-01.Resilience4j%20%EA%B0%9C%EC%9A%94%20%E2%80%94%205%EA%B0%80%EC%A7%80%20%EB%AA%A8%EB%93%88%EA%B3%BC%20%EB%8F%84%EC%9E%85%20%EA%B2%B0%EC%A0%95.md) | |
| 서킷 브레이커 상태 전이 | 필수 | [Circuit Breaker 상세](../09_spring/03_network/resilience/01-02.Circuit%20Breaker%20%EC%83%81%EC%84%B8%20%E2%80%94%20%EC%83%81%ED%83%9C%20%EC%A0%84%EC%9D%B4%EC%99%80%20Sliding%20Window.md) | Cloud Native Spring 9장 |
| 재시도 · 백오프 · 지터 | 필수 | [Retry](../09_spring/03_network/resilience/01-03.Retry%20%E2%80%94%20exponential%20backoff%C2%B7jitter%C2%B7%EC%9E%AC%EC%8B%9C%EB%8F%84%20%ED%8F%AD%EC%A3%BC%20%EB%B0%A9%EC%A7%80.md) | |
| 격벽과 속도 제한 | 추천 | [Bulkhead](../09_spring/03_network/resilience/01-04.Bulkhead%20%E2%80%94%20Semaphore%20vs%20ThreadPool%20%EA%B2%A9%EB%A6%AC.md) | |
| API 게이트웨이 | 추천 | | Cloud Native Spring 9장 |
| 재시도 메커니즘 · 지터드 백오프 · 풀 지터 · 이퀄 지터 · 디코릴레이티드 지터 · 피보나치 백오프 · 재시도 예산 · 재시도 제한 · 재시도 스톰 · 재시도 스톰 방지 | 선택 | [재시도 메커니즘](../02_os/project/npg-lab/01-02.%EB%A6%AC%EB%B2%84%EC%8A%A4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%EC%97%85%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B8%B5%20%E2%80%94%20%EC%97%B0%EA%B2%B0%20%ED%92%80%C2%B7%EA%B8%B0%ED%95%9C%C2%B7%EB%8C%80%EA%B8%B0%EC%97%B4%C2%B7%EC%9E%AC%EC%8B%9C%EB%8F%84%EC%99%80%20%EC%8B%A4%ED%8C%A8%20%EB%B6%84%EB%A5%98.md) · [지터드 백오프](../09_spring/03_network/resilience/01-03.Retry%20%E2%80%94%20exponential%20backoff%C2%B7jitter%C2%B7%EC%9E%AC%EC%8B%9C%EB%8F%84%20%ED%8F%AD%EC%A3%BC%20%EB%B0%A9%EC%A7%80.md) · [재시도 스톰](../04_messaging/05_ConsistencyPattern/06-02.Retry%20Storm%20%EB%B0%A9%EC%A7%80%20%E2%80%94%20%EB%B0%B1%EC%98%A4%ED%94%84%20jitter%C2%B7%EB%8F%99%EC%8B%9C%EC%84%B1%20%EC%A0%9C%ED%95%9C%C2%B7%EC%84%9C%ED%82%B7.md) | |
| 멱등성 · 멱등성 키 · 요청 중복 제거 · 멱등성 재시도 · 비멱등성 재시도 방지 | 선택 | [멱등성](../03_architecture/05_edd/05-03.202%20Accepted%20%2B%20Polling%20%ED%8C%A8%ED%84%B4.md) · [멱등성 키](../04_messaging/01_Connect/03-02.%EC%9E%A5%EC%95%A0%20%EB%B3%B5%EA%B5%AC%EC%99%80%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1.md) · [요청 중복 제거](../03_architecture/book/bytebytego-system-design/08-01.%ED%8A%B8%EC%9C%84%ED%84%B0%20%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%C2%B7%EA%B5%AC%EA%B8%80%20%EB%8F%85%EC%8A%A4%20%EB%8F%99%EC%8B%9C%20%ED%8E%B8%EC%A7%91%C2%B7%EC%8A%AC%EB%9E%99%20%EC%95%8C%EB%A6%BC%20%ED%8C%90%EC%A0%95%C2%B7%ED%81%AC%EB%A1%A4%EB%9F%AC%20%EC%A4%91%EB%B3%B5%20%EC%A0%9C%EA%B1%B0%EB%8A%94%20%ED%8C%AC%EC%95%84%EC%9B%83%C2%B7OT%C2%B7%ED%9D%90%EB%A6%84%EB%8F%84%C2%B7%EB%B8%94%EB%A3%B8%20%ED%95%84%ED%84%B0%EB%A1%9C%20%ED%91%BC%EB%8B%A4.md) | |
| 서킷 브레이커 하프오픈 · 벌크헤드 | 선택 | [벌크헤드](../09_spring/03_network/resilience/01-04.Bulkhead%20%E2%80%94%20Semaphore%20vs%20ThreadPool%20%EA%B2%A9%EB%A6%AC.md) | |
| 타임아웃 전파 · 데드라인 전파 · 컨텍스트 캔슬 · 헤지 요청 | 선택 | [타임아웃 전파](../02_os/book/npg_network-programming-with-go/03-03.%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%80%20Dialer%C2%B7context%20%EB%A1%9C%2C%20%EC%9C%A0%ED%9C%B4%20%EA%B0%90%EC%A7%80%EB%8A%94%20%EB%8D%B0%EB%93%9C%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%ED%95%98%ED%8A%B8%EB%B9%84%ED%8A%B8%EB%A1%9C%20%EA%B1%B4%EB%8B%A4.md) · [데드라인 전파](../02_os/book/npg_network-programming-with-go/03-03.%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%80%20Dialer%C2%B7context%20%EB%A1%9C%2C%20%EC%9C%A0%ED%9C%B4%20%EA%B0%90%EC%A7%80%EB%8A%94%20%EB%8D%B0%EB%93%9C%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%ED%95%98%ED%8A%B8%EB%B9%84%ED%8A%B8%EB%A1%9C%20%EA%B1%B4%EB%8B%A4.md) · [컨텍스트 캔슬](../02_os/book/npg_network-programming-with-go/03-03.%ED%83%80%EC%9E%84%EC%95%84%EC%9B%83%EC%9D%80%20Dialer%C2%B7context%20%EB%A1%9C%2C%20%EC%9C%A0%ED%9C%B4%20%EA%B0%90%EC%A7%80%EB%8A%94%20%EB%8D%B0%EB%93%9C%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%ED%95%98%ED%8A%B8%EB%B9%84%ED%8A%B8%EB%A1%9C%20%EA%B1%B4%EB%8B%A4.md) | |
| 폴백 캐시 · 그레이스풀 디그레이데이션 | 선택 | | |
| 마이크로서비스 · BFF · API 컴포지션 | 선택 | [마이크로서비스](../03_architecture/05_edd/04-02.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EC%84%9C%EB%B9%84%EC%8A%A4%20%ED%85%8C%EC%8A%A4%ED%8C%85.md) · [BFF](../03_architecture/05_edd/03-03.%EC%9A%94%EC%B2%AD-%EC%9D%91%EB%8B%B5%EA%B3%BC%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%ED%86%B5%ED%95%A9.md) · [API 컴포지션](../03_architecture/02_application/01-07.%EB%8B%A4%EC%A4%91%20%EC%97%94%ED%8B%B0%ED%8B%B0%20%EC%A1%B0%ED%9A%8C%20API%20%EC%84%A4%EA%B3%84.md) | |
| 모듈러 모놀리스 | 선택 | | |
| 클라이언트 사이드 디스커버리 · 서버 사이드 디스커버리 | 선택 | | |
| 사이드카 프록시 · 앰배서더 패턴 | 선택 | [사이드카 프록시](../08_cloud/book/istio-in-action/14-01.Envoy%EB%A5%BC%20%EC%83%88%EB%A1%9C%20%EB%B9%8C%EB%93%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EC%9C%BC%EB%A0%A4%EA%B3%A0%20%EB%82%B8%20%EB%84%A4%20%EA%B0%9C%EC%9D%98%20%EB%AC%B8.md) · [앰배서더 패턴](../08_cloud/book/kubernetes-patterns/18-01.Ambassador%20%E2%80%94%20%EB%B0%94%EA%B9%A5%EC%84%B8%EC%83%81%EC%9C%BC%EB%A1%9C%EC%9D%98%20smart%20proxy.md) | |
| 인바운드 트래픽 · 아웃바운드 트래픽 · 이스트-웨스트 트래픽 · 노스-사우스 트래픽 · 서비스 투 서비스 | 선택 | [이스트-웨스트 트래픽](../08_cloud/book/cilium-up-and-running/07-02.Gateway%20API%20%EB%8A%94%20%EC%97%AD%ED%95%A0%EB%B3%84%20%EA%B0%9D%EC%B2%B4%EB%A1%9C%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EC%9D%84%20%EB%82%98%EB%88%84%EA%B3%A0%20%EA%B0%80%EC%A4%91%EC%B9%98%C2%B7%ED%97%A4%EB%8D%94%C2%B7%EB%8F%99%EC%84%9C%20%ED%8A%B8%EB%9E%98%ED%94%BD%EA%B9%8C%EC%A7%80%20%EB%A7%A1%EB%8A%94%EB%8B%A4.md) | |
| 스트랭글러 패턴 · 안티 코럽션 레이어 | 선택 | [스트랭글러 패턴](../01_language/book/five-lines-of-code/01-01.%ED%81%B4%EB%A6%B0%20%EC%BD%94%EB%93%9C%20%EC%9B%90%EC%B9%99.md) | |
| 서비스 디스커버리 | 선택 | [서비스 디스커버리](../05_data/book/designing-data-intensive-applications/05-04.%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%94%8C%EB%A1%9C%EC%9A%B0%20%E2%80%94%20DB%C2%B7REST%C2%B7RPC.md) | |



## 7단계 · 비동기와 실시간

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| @Async 와 스레드 풀 | 필수 | [어노테이션 AOP](../09_spring/05_aop/01-04.%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EA%B8%B0%EB%B0%98%20AOP%20%EC%9D%91%EC%9A%A9%20%E2%80%94%20%40Async%C2%B7%40Cacheable%C2%B7%40Retryable.md) | Spring in Action 9장 |
| 스케줄링과 Quartz | 필수 | [스프링 스케줄링](../09_spring/05_aop/01-02.%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%20%E2%80%94%20%40Scheduled%EC%97%90%EC%84%9C%20Quartz%EA%B9%8C%EC%A7%80.md) | |
| 캐시 추상화 | 추천 | [어노테이션 AOP](../09_spring/05_aop/01-04.%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EA%B8%B0%EB%B0%98%20AOP%20%EC%9D%91%EC%9A%A9%20%E2%80%94%20%40Async%C2%B7%40Cacheable%C2%B7%40Retryable.md) | |
| Reactor 와 백프레셔 | 추천 | [이벤트 기반과 NIO](../09_spring/03_network/reactive-net/01-02.%EC%9D%B4%EB%B2%A4%ED%8A%B8%20%EA%B8%B0%EB%B0%98%20%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%EA%B3%BC%20BIO%20vs%20NIO.md) | Spring in Action 11장 |
| WebFlux 두 모델 | 추천 | [WebFlux 서버](../09_spring/01_core/04-01.WebFlux%20%EC%84%9C%EB%B2%84%20%E2%80%94%20%EB%A6%AC%EC%95%A1%ED%8B%B0%EB%B8%8C%20%EC%8A%A4%ED%83%9D%EA%B3%BC%20%EC%96%B4%EB%85%B8%ED%85%8C%EC%9D%B4%EC%85%98%20%EB%AA%A8%EB%8D%B8.md) | Spring in Action 12장 |
| Netty 파이프라인 | 선택 | [채널 파이프라인과 코덱](../09_spring/03_network/reactive-net/01-04.%EC%B1%84%EB%84%90%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%EA%B3%BC%20%EC%BD%94%EB%8D%B1.md) | |
| SSE 와 신뢰성 | 추천 | [SSE](../09_spring/03_network/realtime/02-01.SSE%20%EC%9B%90%EB%A6%AC%EC%99%80%20Spring%20%EA%B5%AC%ED%98%84.md) | |
| WebSocket 과 STOMP | 추천 | [WebSocket vs STOMP](../09_spring/03_network/realtime/03-03.WebSocket%20vs%20STOMP.md) | |
| 연결 관리와 재연결 | 추천 | [재연결 전략](../09_spring/03_network/realtime/04-01.%EC%97%B0%EA%B2%B0%20%EA%B4%80%EB%A6%AC%EC%99%80%20%EC%9E%AC%EC%97%B0%EA%B2%B0%20%EC%A0%84%EB%9E%B5.md) | |
| Web Push — 연결이 끊긴 브라우저에 푸시 서비스를 거쳐 알림을 보낸다 · VAPID · 페이로드 암호화 · Service Worker | 선택 | | [RFC 8030](https://www.rfc-editor.org/rfc/rfc8030) · [RFC 8292](https://www.rfc-editor.org/rfc/rfc8292) · [RFC 8291](https://www.rfc-editor.org/rfc/rfc8291) |
| PWA — 설치 가능한 웹앱 · Web App Manifest · 보안 컨텍스트에서만 열리는 기능 | 선택 | | [Web App Manifest](https://www.w3.org/TR/appmanifest/) · [Secure Contexts](https://www.w3.org/TR/secure-contexts/) |
| 배치 — 잡과 스텝 | 선택 | | Spring Batch 2~4장 |
| 배치 — 리더 · 프로세서 · 라이터 | 선택 | | Spring Batch 7~9장 |
| 웹소켓 · Server-Sent Events | 선택 | [웹소켓](../03_architecture/book/system-design/12-01.%EC%B1%84%ED%8C%85%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%80%20%EC%9B%B9%EC%86%8C%EC%BC%93%20%EC%97%B0%EA%B2%B0%EC%9D%84%20%EC%83%81%ED%83%9C%20%EC%9C%A0%EC%A7%80%20%EC%84%9C%EB%B2%84%EC%97%90%20%EB%91%90%EA%B3%A0%20%ED%82%A4-%EA%B0%92%20%EC%A0%80%EC%9E%A5%EC%86%8C%EC%99%80%20%EB%A9%94%EC%8B%9C%EC%A7%80%20ID%20%EB%A1%9C%20%EB%8C%80%ED%99%94%EC%99%80%20%EC%A0%91%EC%86%8D%20%EC%83%81%ED%83%9C%EB%A5%BC%20%EB%8B%A4%EB%A3%AC%EB%8B%A4.md) · [Server-Sent Events](../03_architecture/05_edd/05-02.EDA%20%EA%B8%B0%EB%B0%98%20%EC%9A%94%EC%B2%AD%EC%9D%91%EB%8B%B5%20%ED%86%B5%ED%95%A9.md) | |



## 8단계 · 보안과 운영

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 필터 체인이 먼저다 | 필수 | | Spring Security 5장 |
| 인증과 사용자 · 비밀번호 | 필수 | | Spring Security 3·4·6장 |
| 엔드포인트 인가 | 필수 | | Spring Security 7·8장 |
| 인가를 어디서 하는가 — 게이트웨이의 거친 인가와 도메인 인가 · PEP · PDP · RBAC · ABAC | 추천 | | |
| CSRF 와 CORS | 추천 | | Spring Security 9·10장 |
| 메서드 수준 보안 | 추천 | | Spring Security 11·12장 |
| OAuth 2 와 OIDC | 추천 | [OAuth2와 OIDC](../99_ETC/security/01_concepts/2026-05-29_OAuth2%EC%99%80%20OIDC%20%E2%80%94%20%EC%9C%84%EC%9E%84%20%EC%9D%B8%EA%B0%80%EC%99%80%20%EA%B7%B8%20%EC%9C%84%EC%9D%98%20%EC%9D%B8%EC%A6%9D.md) | Spring Security 13~16장 |
| 액츄에이터 엔드포인트 | 필수 | | Spring in Action 15장 |
| Micrometer 와 메트릭 | 필수 | | Spring in Action 16·17장 |
| Prometheus 연동 | 추천 | | Cloud Native Spring 13장 |
| 세션 관리 · MFA | 선택 | | |
| 리프레시 토큰 · 토큰 로테이션 | 선택 | [토큰 로테이션](../07_devops/02_Jenkins/04_api/03-03.API%20%ED%86%A0%ED%81%B0%20%EB%B0%9C%EA%B8%89%C2%B7%ED%9A%8C%EC%A0%84%C2%B7%EC%88%98%EB%AA%85%20%EC%A0%90%EA%B2%80.md) | |
| OpenID Connect · 인가 코드 그랜트 · 클라이언트 자격 증명 그랜트 · 디바이스 코드 플로우 | 선택 | [OpenID Connect](../08_cloud/book/argocd-up-and-running/06-02.SSO%20%EC%97%B0%EA%B2%B0%EA%B3%BC%20RBAC%20%E2%80%94%20Dex%C2%B7%EC%A7%81%EC%A0%91%20OIDC%C2%B7%EC%97%AD%ED%95%A0%EA%B3%BC%20%EC%A0%95%EC%B1%85.md) · [인가 코드 그랜트](../99_ETC/security/01_concepts/2026-05-29_OAuth2%EC%99%80%20OIDC%20%E2%80%94%20%EC%9C%84%EC%9E%84%20%EC%9D%B8%EA%B0%80%EC%99%80%20%EA%B7%B8%20%EC%9C%84%EC%9D%98%20%EC%9D%B8%EC%A6%9D.md) | |
| 비밀번호 해싱 · bcrypt · scrypt · Argon2 · PBKDF2 · 비밀번호 스트레칭 · 솔트·솔팅 · 페퍼 · 레인보우 테이블 | 선택 | [비밀번호 해싱](../02_os/book/ostep_operating-systems-three-easy-pieces/45-01.%EC%9B%90%EA%B2%A9%20%EA%B8%B0%EA%B3%84%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9C%BC%EB%A1%9C%20%EB%AF%BF%EB%8A%94%EA%B0%80%20%E2%80%94%20%EC%9D%B8%EC%A6%9D%EC%84%9C%EC%9D%98%20%EC%84%9C%EB%AA%85%EA%B3%BC%20%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%20%ED%95%B4%EC%8B%9C.md) · [솔트·솔팅](../02_os/book/ostep_operating-systems-three-easy-pieces/45-01.%EC%9B%90%EA%B2%A9%20%EA%B8%B0%EA%B3%84%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9C%BC%EB%A1%9C%20%EB%AF%BF%EB%8A%94%EA%B0%80%20%E2%80%94%20%EC%9D%B8%EC%A6%9D%EC%84%9C%EC%9D%98%20%EC%84%9C%EB%AA%85%EA%B3%BC%20%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8%20%ED%95%B4%EC%8B%9C.md) | |
| 입력 유효성 검사 · SQL 인젝션 방지 · 준비된 문장 · XSS 방지 · CSRF 방지 | 선택 | [준비된 문장](../01_language/book/jpf_java-performance/11-01.JDBC%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84%C2%B7connection%20pool%C2%B7prepared%20statement.md) · [XSS 방지](../07_devops/02_Jenkins/02_security/04-01.%EC%9B%B9%20%EA%B3%84%EC%B8%B5%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20CSRF%C2%B7CSP%C2%B7%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%BD%98%ED%85%90%EC%B8%A0.md) · [CSRF 방지](../07_devops/02_Jenkins/02_security/04-01.%EC%9B%B9%20%EA%B3%84%EC%B8%B5%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20CSRF%C2%B7CSP%C2%B7%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%BD%98%ED%85%90%EC%B8%A0.md) | |
| API 게이트웨이 보안 · 레이트 리밋 바이패스 | 선택 | | |
| 요청 필터링 | 선택 | | |
| 봇 탐지 · 캡차 · 디바이스 핑거프린팅 · 행동 분석 · 이상 탐지 | 선택 | | |
| 액세스 토큰 | 선택 | | |
| CSP | 선택 | [CSP](../07_devops/02_Jenkins/02_security/04-01.%EC%9B%B9%20%EA%B3%84%EC%B8%B5%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20CSRF%C2%B7CSP%C2%B7%EC%82%AC%EC%9A%A9%EC%9E%90%20%EC%BD%98%ED%85%90%EC%B8%A0.md) | |



## 9단계 · 테스트와 배포

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 테스트 피라미드와 슬라이스 | 필수 | [테스트 피라미드](../09_spring/04_testing/01-01.%ED%85%8C%EC%8A%A4%ED%8A%B8%20%ED%94%BC%EB%9D%BC%EB%AF%B8%EB%93%9C%EC%99%80%20Spring%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%A2%85%EB%A5%98.md) | Spring Start Here 15장 |
| JUnit 5 와 AssertJ | 필수 | [JUnit 5·AssertJ](../09_spring/04_testing/01-02.JUnit%205%20%2B%20AssertJ%EB%A1%9C%20%EB%8B%A8%EC%9C%84%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%9E%91%EC%84%B1.md) | |
| Mockito 와 MockMvc | 필수 | [Mockito·MockMvc](../09_spring/04_testing/01-03.Mockito%EC%99%80%20MockMvc%20%EC%8A%AC%EB%9D%BC%EC%9D%B4%EC%8A%A4.md) | |
| @SpringBootTest 와 컨텍스트 러너 | 필수 | [@SpringBootTest](../09_spring/04_testing/01-04.%40SpringBootTest%EC%99%80%20ApplicationContextRunner.md) | |
| Testcontainers 로 진짜 DB | 필수 | [Testcontainers](../09_spring/04_testing/02-01.Testcontainers%EC%99%80%20%EC%A7%84%EC%A7%9C%20DB%20%ED%86%B5%ED%95%A9%20%ED%85%8C%EC%8A%A4%ED%8A%B8.md) | |
| 메시징 테스트 | 추천 | [메시징 테스트](../09_spring/04_testing/02-02.EmbeddedKafka%C2%B7Testcontainers%EB%A1%9C%20%EB%A9%94%EC%8B%9C%EC%A7%95%20%ED%85%8C%EC%8A%A4%ED%8A%B8.md) | |
| ArchUnit 가드레일 | 추천 | [ArchUnit](../09_spring/04_testing/02-03.ArchUnit%EC%9C%BC%EB%A1%9C%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B0%80%EB%93%9C%EB%A0%88%EC%9D%BC.md) | |
| WireMock 과 외부 시스템 | 추천 | [WireMock](../09_spring/04_testing/02-04.WireMock%EA%B3%BC%20%EC%99%B8%EB%B6%80%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20E2E.md) | |
| 테스트 데이터 — 정적·랜덤 픽스처와 매퍼 테스트 | 선택 |  |  |
| 보안 설정 테스트 | 추천 | | Spring Security 18장 |
| bootJar 와 Layered JAR | 필수 | [내장 톰캣](../09_spring/01_core/02-02.%EB%82%B4%EC%9E%A5%20%ED%86%B0%EC%BA%A3%EA%B3%BC%20SpringApplication%20%E2%80%94%20JAR%EB%A1%9C%20WAS%EB%A5%BC%20%ED%92%88%EB%8B%A4.md) | Spring in Action 18장 |
| 컨테이너화와 쿠버네티스 | 추천 | [Boot 컨테이너화](../09_spring/books/cloud-native-spring-in-action/06.Spring%20Boot%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%ED%99%94.md) | Cloud Native Spring 6·7장 |
| 지속 배포와 GitOps | 선택 | | Cloud Native Spring 15장 |
| 유닛 테스트 · 통합 테스트 · 테스트 더블 목·스텁·페이크 · 엔드투엔드 테스트 · 컨트랙트 테스팅 · 컨슈머 주도 컨트랙트 · 프로퍼티 기반 테스트 · 뮤테이션 테스팅 | 선택 | [유닛 테스트](../09_spring/04_testing/01-02.JUnit%205%20%2B%20AssertJ%EB%A1%9C%20%EB%8B%A8%EC%9C%84%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%9E%91%EC%84%B1.md) · [통합 테스트](../09_spring/04_testing/02-01.Testcontainers%EC%99%80%20%EC%A7%84%EC%A7%9C%20DB%20%ED%86%B5%ED%95%A9%20%ED%85%8C%EC%8A%A4%ED%8A%B8.md) · [테스트 더블 목·스텁·페이크](../09_spring/04_testing/01-03.Mockito%EC%99%80%20MockMvc%20%EC%8A%AC%EB%9D%BC%EC%9D%B4%EC%8A%A4.md) · [엔드투엔드 테스트](../03_architecture/book/bmf_building-micro-frontends/06-05.E2E%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%E2%80%94%20%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EB%84%98%EB%8A%94%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4%EB%8A%94%20%EB%88%84%EA%B5%AC%20%EA%B2%83%EC%9D%B8%EA%B0%80.md) · [컨슈머 주도 컨트랙트](../04_messaging/08_advanced/01_variants/01-04.%EC%8A%A4%ED%82%A4%EB%A7%88%20%EA%B1%B0%EB%B2%84%EB%84%8C%EC%8A%A4.md) | |
| 부하 테스트 · 스트레스 테스트 · 소크 테스트 · 카오스 엔지니어링 · 장애 주입 | 선택 | [카오스 엔지니어링](../09_spring/04_testing/02-04.WireMock%EA%B3%BC%20%EC%99%B8%EB%B6%80%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20E2E.md) · [장애 주입](../07_devops/02_Jenkins/05_operations/01-02.%EA%B0%80%EC%9A%A9%EC%84%B1%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4.md) | |
| 정적 분석 | 선택 | [정적 분석](../07_devops/docs/sonarqube/01-01.%EC%A0%95%EC%A0%81%20%EB%B6%84%EC%84%9D%EC%9D%B4%20%ED%91%B8%EB%8A%94%20%EA%B2%B0%ED%95%A8.md) | |
| 퍼징 | 선택 | [퍼징](../01_language/book/lgo_learning-go/15-03.%ED%8D%BC%EC%A7%95%EC%9D%80%20%EC%8B%9C%EB%93%9C%EB%A5%BC%20%EB%B9%84%ED%8B%80%EC%96%B4%20%EB%86%93%EC%B9%9C%20%EC%9E%85%EB%A0%A5%EC%9D%84%20%EC%B0%BE%EA%B3%A0%20%EB%B2%A4%EC%B9%98%EB%A7%88%ED%81%AC%EB%8A%94%20b.Loop%20%EB%A1%9C%20%ED%95%9C%20%EB%B2%88%EC%9D%98%20%EB%B9%84%EC%9A%A9%EC%9D%84%20%EC%9E%BD%EB%8B%88%EB%8B%A4.md) | |



## 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| GC · 클래스 로딩 · 힙 덤프 | [JVM 로드맵](../01_language/jvm-keywords.md)이 맡습니다. Spring 이 느린 것과 JVM 이 멈춘 것은 다른 층입니다 |
| 인덱스 자료구조 · 분산 일관성 | [데이터 로드맵](../05_data/data-keywords.md)이 맡습니다. 4단계는 트랜잭션 경계까지만 봅니다 |
| SQL 실행 계획 · 인덱스 튜닝 | 소장 책에 없고, 이 저장소에도 아직 노트가 없습니다 |
| PromQL · SLO · 알림 설계 | [관측 가능성 로드맵](../06_observability/observability-keywords.md)이 맡습니다. 8단계는 내보내는 쪽만 봅니다 |
| 쿠버네티스 오브젝트와 내부 구조 | [Kubernetes 로드맵](../08_cloud/k8s-keywords.md)이 맡습니다. 9단계는 배포 산출물까지입니다 |
| Kafka 프로듀서 · 컨슈머 설계 | `04_messaging` 이 정본입니다. `@KafkaListener` 는 그 주제 축 안에 둡니다 |
| QueryDSL 과 동적 쿼리 | `05_data/03_persistence/querydsl` 이 정본입니다 |
| 뷰 템플릿과 서버 렌더링 | Thymeleaf 로 화면을 그리는 축은 다룰 일이 없습니다. 3단계는 REST 응답까지입니다 |
| XML 설정과 레거시 마이그레이션 | 소장본에 부록으로 있지만 새로 쓸 일이 없습니다 |
| 비관계형 데이터 · Spring Integration · RSocket | Spring in Action 4·10·14장입니다. 쓰게 될 때 그 장만 폅니다 |
| GraalVM 네이티브 이미지와 Knative | Cloud Native Spring 16장입니다. 기동 시간이 문제가 되면 엽니다 |
