---
title: QueryDSL 학습 MOC
tags: [moc, querydsl, spring-boot, jpa, persistence]
status: final
source:
  - https://github.com/OpenFeign/querydsl
  - https://docs.spring.io/spring-boot/docs/3.2.3/reference/htmlsingle/
related:
  - ../README.md
  - ../../12_spring/README.md
updated: 2026-05-07
---

# QueryDSL 학습 MOC

---

> Spring Boot 3.2.3 + QueryDSL 6.12 (OpenFeign fork) 환경에서 JPA를 이미 아는 학습자가 면접에서 자신있게 설명할 수 있는 수준까지 끌어올리는 챕터형 노트다. 12개 문서가 한 묶음으로 동작한다(표준 9 + 실무 변형 2 + 락 1).



## 왜 별도 묶음인가

> Spring Data JPA만으로는 끝까지 못 가는 이유와, QueryDSL이 메우는 빈틈을 한 자리에 모은다.

Spring Data JPA는 메서드 이름 규칙(`findByEmailAndStatus`)과 `@Query` 어노테이션으로 단순 조회를 잘 처리한다. 그런데 검색 조건이 동적으로 0개에서 5개까지 변하거나, 페이징과 페치 조인이 함께 필요하거나, 통계 SQL을 DTO로 받고 싶은 순간이 오면 문자열 JPQL이나 Criteria API로는 가독성이 무너진다.

QueryDSL은 그 지점에서 들어온다. 정적 타입 메타모델(Q클래스)을 빌드 타임에 생성해, 컴파일러가 컬럼 이름 오타를 잡아 주고 IDE 자동완성으로 쿼리를 조립한다. 본 묶음은 그 도구를 단순 흉내가 아니라 "왜 이렇게 설계됐는가"를 짚으면서 익힌다.



## 학습 순서

> 표준 9개를 두 장으로 나누고, 실무 변형 두 편과 동시성 제어 한 편을 부록으로 둔다. 1장은 "쓰는 법", 2장은 "팀에 적용하는 법", 02-04는 운영 코드베이스에서 자주 보이는 단일 패턴 변형 모음, 02-05는 락·동시성 영역, 02-06은 native SQL의 CTE/window 함수를 JPA QueryDSL로 옮길 때의 한 케이스 통째 분해다.

| # | 문서 | 다루는 핵심 |
|---|------|-----------|
| 01-01 | [입문과 6.12의 위치](01-01.QueryDSL%20입문과%206.12의%20위치.md) | 등장 동기, 원조 archived 사실, 6.12 vs 7.x 선택 |
| 01-02 | [프로젝트 셋업 (Gradle 6.12)](01-02.프로젝트%20셋업%20(Gradle%206.12).md) | `build.gradle`, annotationProcessor, Q클래스 경로, `JPAQueryFactory` 빈 |
| 01-03 | [기본 문법과 조인](01-03.기본%20문법과%20조인.md) | `select/from/where/join/fetchJoin`, `Expressions` |
| 01-04 | [동적 쿼리](01-04.동적%20쿼리.md) | `BooleanBuilder` vs `BooleanExpression`, null 안전성 |
| 01-05 | [프로젝션과 DTO 매핑](01-05.프로젝션과%20DTO%20매핑.md) | `Tuple`, `Projections.*`, `@QueryProjection` 트레이드오프 |
| 01-06 | [페이징과 fetch join 함정](01-06.페이징과%20fetch%20join%20함정.md) | `HHH000104`, `distinct`, 카운트 분리, `@BatchSize` |
| 02-01 | [커스텀 리포지토리 패턴](02-01.커스텀%20리포지토리%20패턴.md) | `RepositoryCustom` + `Impl`, fragment composition |
| 02-02 | [테스트와 멀티모듈](02-02.테스트와%20멀티모듈.md) | `@DataJpaTest` + `JPAQueryFactory`, Q클래스 가시성 |
| 02-03 | [대안 비교와 6.12→7.x 마이그레이션](02-03.대안%20비교와%206.12-7.x%20마이그레이션.md) | MyBatis/JOOQ 비교, OpenFeign 좌표 이전, 7.x 차이 |
| 02-04 | [실무 변형 모음](02-04.실무%20변형%20모음.md) | PathBuilder·Embedded ID·상관 서브쿼리·JPQL limit 한계·동적 검색 추상 베이스·`nullExpression` |
| 02-05 | [락과 동시성 제어](02-05.락과%20동시성%20제어.md) | `@Version` 낙관, `PESSIMISTIC_WRITE/READ`, `setLockMode` ↔ `@Lock`, 데드락 방어 |
| 02-06 | [window 함수 없는 JPA QueryDSL의 ROW_NUMBER 대체](02-06.window%20함수%20없는%20JPA%20QueryDSL의%20ROW_NUMBER%20대체.md) | 상관 sub-select + `CaseBuilder` 정렬로 `ROW_NUMBER`/`PARTITION BY` 의미 동등 표현, group by 이식성 함정 |

처음 보는 학습자는 01-01부터 순서대로 따라간다. 이미 QueryDSL을 써 봤다면 01-04(동적 쿼리), 01-06(페치 조인 함정), 02-01(커스텀 리포지토리)부터 골라 읽어도 된다. 운영 코드베이스의 비표준 패턴을 마주쳤다면 02-04를, 재고·결제처럼 동시성 충돌이 도메인에 박혀 있다면 02-05를, native SQL의 CTE·window 함수를 JPA로 옮겨야 한다면 02-06을 먼저 펼친다.



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

위 항목 중 막히는 부분이 있다면 [`06_data/`](../) 직접 하위와 [`spring/`](../../12_spring/)을 먼저 보고 돌아오는 편이 빠르다.



## 면접 대비 체크리스트

> 표준 9개를 다 읽은 뒤 다음 질문에 모두 답할 수 있어야 한다. 실무 변형(02-04, 02-06)과 락(02-05)은 운영 환경에서 마주쳤을 때 추가로 점검한다.

1. JPA Criteria API가 있는데 QueryDSL을 쓰는 이유를 두 가지 이상 들 수 있는가?
2. `BooleanBuilder`와 `BooleanExpression` 메서드 분해 패턴 중 어느 쪽이 재사용성이 좋고 왜 그런가?
3. `Projections.constructor`와 `@QueryProjection`의 트레이드오프가 무엇인가?
4. 페이징과 페치 조인을 동시에 쓰면 왜 `HHH000104` 경고가 뜨고, 무엇이 위험한가?
5. 6.12 vs 7.x 선택 기준을 한 문장으로 말할 수 있는가?
6. Spring Data JPA 커스텀 리포지토리에서 `XxxRepositoryImpl` 명명이 왜 강제되는가?
7. 멀티 모듈 프로젝트에서 다른 모듈의 Q클래스를 보려면 어떻게 해야 하는가?
8. 낙관적 락과 비관적 락 중 어느 쪽을 어떤 기준으로 선택하며, 비관 락 트랜잭션 안에서 외부 API 호출을 피해야 하는 이유는 무엇인가?

각 질문에 막히면 표 우측의 챕터를 다시 본다.



## 관련 문서

- [Spring 통합 MOC](../../12_spring/README.md) — 영속성 외 Spring 카테고리 진입점
- [`06_data/`](../README.md) — 데이터 카테고리 진입
- [Spring Data JPA Reference](https://docs.spring.io/spring-data/jpa/reference/) — 외부 공식 문서
- [OpenFeign/querydsl GitHub](https://github.com/OpenFeign/querydsl) — 6.12 릴리즈 노트와 이슈 트래커
