---
title: QueryDSL 학습 MOC
tags: [moc, querydsl, spring-boot, jpa, persistence]
status: final
source:
  - https://github.com/OpenFeign/querydsl
  - https://docs.spring.io/spring-boot/docs/3.2.3/reference/htmlsingle/
related:
  - ../README.md
  - ../../11_spring/README.md
updated: 2026-05-07
---

# QueryDSL 학습 MOC

---

> Spring Boot 3.2.3 + QueryDSL 6.12 (OpenFeign fork) 환경에서 JPA를 이미 아는 학습자가 면접에서 자신있게 설명할 수 있는 수준까지 끌어올리는 챕터형 노트다. 16개 문서가 한 묶음으로 동작한다(1장 표준 이론 6 + 2장 심화 이론 4 + 3장 실무 변형 6).



## 왜 별도 묶음인가

> Spring Data JPA만으로는 끝까지 못 가는 이유와, QueryDSL이 메우는 빈틈을 한 자리에 모은다.

Spring Data JPA는 메서드 이름 규칙(`findByEmailAndStatus`)과 `@Query` 어노테이션으로 단순 조회를 잘 처리한다. 그런데 검색 조건이 동적으로 0개에서 5개까지 변하거나, 페이징과 페치 조인이 함께 필요하거나, 통계 SQL을 DTO로 받고 싶은 순간이 오면 문자열 JPQL이나 Criteria API로는 가독성이 무너진다.

QueryDSL은 그 지점에서 들어온다. 정적 타입 메타모델(Q클래스)을 빌드 타임에 생성해, 컴파일러가 컬럼 이름 오타를 잡아 주고 IDE 자동완성으로 쿼리를 조립한다. 본 묶음은 그 도구를 단순 흉내가 아니라 "왜 이렇게 설계됐는가"를 짚으면서 익힌다.



## 학습 순서

> 16개를 세 장으로 나눈다. 1장은 *표준 이론* — Q-class·동적 쿼리·프로젝션·페이징 같은 새 프로젝트에서 바로 쓰는 문법. 2장은 *심화 이론* — 1장 표준만으로는 운영 코드를 읽기 어려운 자리(PathBuilder·서브쿼리 합성·NULLS LAST/countDistinct/ExpressionUtils.as·Hooks/ThreadLocal/BooleanBuilder 누적 같은 표현식 합성 패턴)를 보충. 3장은 *실무 변형* — 커스텀 리포지토리·테스트·마이그레이션·실무 변형 모음·락·ROW_NUMBER 대체 같이 팀에 적용할 때 마주치는 패턴.

> 커스텀 리포지토리 패턴(`RepositoryCustom` + `Impl`)은 Spring Data JPA 주제라 [`jpa/03-05`](../jpa/03-05.커스텀%20리포지토리%20패턴.md) 로 분리해 두었다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [입문과 6.12의 위치](01-01.QueryDSL%20입문과%206.12의%20위치.md) | 등장 동기, 원조 archived 사실, 6.12 vs 7.x 선택 |
| 01-02 | [프로젝트 셋업 (Gradle 6.12)](01-02.프로젝트%20셋업%20(Gradle%206.12).md) | `build.gradle`, annotationProcessor, Q클래스 경로, `JPAQueryFactory` 빈 |
| 01-03 | [기본 문법과 조인](01-03.기본%20문법과%20조인.md) | `select/from/where/join/fetchJoin`, `Expressions` |
| 01-04 | [동적 쿼리](01-04.동적%20쿼리.md) | `BooleanBuilder` vs `BooleanExpression`, null 안전성 |
| 01-05 | [프로젝션과 DTO 매핑](01-05.프로젝션과%20DTO%20매핑.md) | `Tuple`, `Projections.*`, `@QueryProjection` 트레이드오프 |
| 01-06 | [페이징과 fetch join 함정](01-06.페이징과%20fetch%20join%20함정.md) | `HHH000104`, `distinct`, 카운트 분리, `@BatchSize` |
| 01-07 | [벌크 연산과 SQL 함수](01-07.벌크%20연산과%20SQL%20함수.md) | `update().execute()`/`delete().execute()`, 영속성 컨텍스트 우회, `Expressions.stringTemplate` |
| **02-01** | **[PathBuilder — 동적 path 빌더 깊이](02-01.PathBuilder%20%E2%80%94%20%EB%8F%99%EC%A0%81%20path%20%EB%B9%8C%EB%8D%94%20%EA%B9%8A%EC%9D%B4.md)** | **정의·생성·자료형 접근·SQL 별칭·트레이드오프, EmbeddedId 두 단계 접근, self-join 동기** |
| **02-02** | **[JPAExpressions — 서브쿼리 합성](02-02.JPAExpressions%20%E2%80%94%20%EC%84%9C%EB%B8%8C%EC%BF%BC%EB%A6%AC%20%ED%95%A9%EC%84%B1.md)** | **scalar / EXISTS / IN 세 형태, 상관 서브쿼리, sub-query LIMIT 제약** |
| **02-03** | **[정렬·집계·프로젝션 보충](02-03.%EC%A0%95%EB%A0%AC%C2%B7%EC%A7%91%EA%B3%84%C2%B7%ED%94%84%EB%A1%9C%EC%A0%9D%EC%85%98%20%EB%B3%B4%EC%B6%A9.md)** | **NULLS LAST API / CASE 기반, countDistinct, ExpressionUtils.as 로 서브쿼리에 alias** |
| **02-04** | **[표현식 합성 — Functional Predicate Supplier 와 transform groupBy](02-04.Hooks%C2%B7ThreadLocal%C2%B7BooleanBuilder%20%EB%88%84%EC%A0%81%20%E2%80%94%20%ED%91%9C%ED%98%84%EC%8B%9D%20%ED%95%A9%EC%84%B1%20%ED%8C%A8%ED%84%B4.md)** | **Functional Predicate Supplier 람다 binding (지연 평가 함정), transform(groupBy) 1:N 재조립** |
| 03-01 | [테스트와 멀티모듈](03-01.테스트와%20멀티모듈.md) | `@DataJpaTest` + `JPAQueryFactory`, Q클래스 가시성 |
| 03-02 | [대안 비교와 6.12→7.x 마이그레이션](03-02.대안%20비교와%206.12-7.x%20마이그레이션.md) | MyBatis/JOOQ 비교, OpenFeign 좌표 이전, 7.x 차이 |
| 03-03 | [실무 변형 모음](03-03.실무%20변형%20모음.md) | PathBuilder·Embedded ID·상관 서브쿼리·JPQL limit 한계·동적 검색 추상 베이스·`nullExpression`, **Hooks 4 분할·ThreadLocal userId 캡처·BooleanBuilder.or() 가상값 누적** (02-04 에서 이동) |
| 03-04 | [락과 동시성 제어](03-04.락과%20동시성%20제어.md) | `@Version` 낙관, `PESSIMISTIC_WRITE/READ`, `setLockMode` ↔ `@Lock`, 데드락 방어 |
| 03-05 | [window 함수 없는 JPA QueryDSL의 ROW_NUMBER 대체](03-05.window%20함수%20없는%20JPA%20QueryDSL의%20ROW_NUMBER%20대체.md) | 상관 sub-select + `CaseBuilder` 정렬로 `ROW_NUMBER`/`PARTITION BY` 의미 동등 표현, group by 이식성 함정 |
| 03-06 | [스프링 데이터 페이징 통합](03-06.스프링%20데이터%20페이징%20통합.md) | `JpaRepository` + `MemberRepositoryCustom` + `Impl` 합치기, 분리 카운트 패턴, `PageableExecutionUtils.getPage` |

처음 학습자는 01-01부터 순서대로. 1장을 끝낸 시점에 *표준 QueryDSL 문법으로 일반 검색* 을 짤 수 있다. 운영 코드(예: TPS operator 결재 도메인)에서 PathBuilder·서브쿼리·NULLS LAST·countDistinct 가 등장하면 2장으로. 2장까지 끝내면 *운영 코드의 모든 QueryDSL API* 를 1차 이해할 수 있다. 3장은 팀에 적용하는 패턴 — 운영 코드베이스의 비표준 패턴을 마주쳤다면 03-03, 재고·결제처럼 동시성 충돌이 도메인에 박혀 있다면 03-04, native SQL의 CTE·window 함수를 JPA로 옮겨야 한다면 03-05 를 먼저 펼친다.



## 환경과 버전

> 모든 코드 예제는 다음 조합에서 검증한다.

| 항목 | 값 | 비고 |
|------|-----|------|
| Spring Boot | 3.2.3 | Jakarta Persistence(`jakarta.persistence.*`) |
| Java | 17 | Spring Boot 3 최소 요구 버전 |
| Gradle | 8.x | annotationProcessor 표준 지원 |
| QueryDSL | 6.12 (OpenFeign fork) | 2024-06-09 릴리즈, 6.x 라인 마지막 안정 버전 |
| groupId | `io.github.openfeign.querydsl` | 원조 `com.querydsl`은 archived |
| Hibernate | 6.4.x (Spring Boot 3.2.3 기본) | `HHH000104` 경고 메시지 동일 |

원조 `querydsl/querydsl` 저장소는 마지막 릴리즈가 2년 넘게 멈춘 상태에서 OpenFeign 조직이 fork를 인수했다. Spring Boot 3 환경에서 jakarta 네임스페이스를 쓰려면 OpenFeign 좌표가 사실상 표준이다. 자세한 거버넌스 배경은 01-01에서 다룬다.



## 사전 지식

> 이 묶음은 다음을 안다고 가정한다.

1. JPA의 영속성 컨텍스트와 1차 캐시가 무엇인지 한 문장으로 설명할 수 있다.
2. JPQL 기본 문법(`select m from Member m where m.age > 20`)을 읽을 수 있다.
3. Spring Boot 프로젝트에 의존성을 추가하고 `JpaRepository`를 만들 수 있다.
4. 페치 조인과 일반 조인의 차이를 한두 문장으로 구분할 수 있다.

위 항목 중 막히는 부분이 있다면 [`05_data/`](../) 직접 하위와 [`spring/`](../../11_spring/)을 먼저 보고 돌아오는 편이 빠르다.



## 면접 대비 체크리스트

> 1장 + 2장(총 9편)을 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 한다. 3장 실무 변형(03-03, 03-05)과 락(03-04)은 운영 환경에서 마주쳤을 때 추가로 점검한다.

### 1장 — 표준 이론 (1~5번)

1. JPA Criteria API가 있는데 QueryDSL을 쓰는 이유를 두 가지 이상 들 수 있는가?
2. `BooleanBuilder`와 `BooleanExpression` 메서드 분해 패턴 중 어느 쪽이 재사용성이 좋고 왜 그런가?
3. `Projections.constructor`와 `@QueryProjection`의 트레이드오프가 무엇인가?
4. 페이징과 페치 조인을 동시에 쓰면 왜 `HHH000104` 경고가 뜨고, 무엇이 위험한가?
5. 6.12 vs 7.x 선택 기준을 한 문장으로 말할 수 있는가?

### 2장 — 심화 이론 (6~11번)

6. PathBuilder 를 쓰는 이유 세 가지(자기참조 join · 모듈 경계 · 동적 정렬 키)를 들 수 있는가? 그리고 컴파일 안전성 약화를 어떻게 보완하는가?
7. `JPAExpressions.selectOne().from(...).where(...).exists()` 가 만드는 SQL 은? `JPAExpressions` 와 `JPAQueryFactory` 의 진입점이 왜 분리되어 있는가?
8. `.nullsLast()` API 와 CASE 기반 NULLS LAST 의 차이는? 사용자 정렬과 별개의 tie-breaker 가 필요할 때 어느 쪽을 쓰는가?
9. `Projections.fields` 안에서 서브쿼리에 alias 를 부여하려면 어떤 우회가 필요한가? `.as("name")` 이 왜 안 되는가?
10. Registry binding 에 람다(`ctx -> ctx.field`)를 쓰는 이유는? 정적 시점에 표현식을 평가하면 어떤 문제가 생기는가?
11. ThreadLocal 로 userId 를 캡처하는 이유는? `clearUserId` 를 빠뜨리면 어떤 사고가 나는가?

### 3장 — 실무 변형 (운영 마주쳤을 때)

12. Spring Data JPA 커스텀 리포지토리에서 `XxxRepositoryImpl` 명명이 왜 강제되는가?
13. 멀티 모듈 프로젝트에서 다른 모듈의 Q클래스를 보려면 어떻게 해야 하는가?
14. 낙관적 락과 비관적 락 중 어느 쪽을 어떤 기준으로 선택하며, 비관 락 트랜잭션 안에서 외부 API 호출을 피해야 하는 이유는 무엇인가?
15. `queryFactory.update().execute()` 가 영속성 컨텍스트를 우회한다는 게 무슨 뜻인가? 같은 트랜잭션에서 갱신 후 같은 엔티티를 다시 쓰려면 어떤 처리가 필요한가?

각 질문에 막히면 표 우측의 챕터를 다시 본다.



## 관련 문서

- [Spring 통합 MOC](../../11_spring/README.md) — 영속성 외 Spring 카테고리 진입점
- [`05_data/`](../README.md) — 데이터 카테고리 진입
- [Spring Data JPA Reference](https://docs.spring.io/spring-data/jpa/reference/) — 외부 공식 문서
- [OpenFeign/querydsl GitHub](https://github.com/OpenFeign/querydsl) — 6.12 릴리즈 노트와 이슈 트래커
