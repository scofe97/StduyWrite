# querydsl-practice

QueryDSL 학습 노트(`write/06_data/spring/querydsl/`)를 직접 코드로 실습하는 프로젝트다.
주문서 도메인(Member → Order → OrderItem → Item / Category)을 H2 in-memory 위에 띄워, 챕터별 패턴을 테스트로 검증한다.

## 환경

| 항목 | 값 |
|------|-----|
| Spring Boot | 3.2.3 |
| Java | 17 |
| Gradle | 8.5 (wrapper 동봉) |
| QueryDSL | 6.12 (`io.github.openfeign.querydsl`) |
| DB | H2 in-memory |

OpenFeign 좌표를 쓰는 이유와 6.12 vs 7.x 선택 기준은 노트 `01-01.QueryDSL 입문과 6.12의 위치.md` 참고.

## 시작

```bash
./gradlew test                                # 전체 테스트
./gradlew test --tests Ch03_*                 # 챕터별 실행
./gradlew compileJava                         # Q클래스 생성 확인
./gradlew bootRun                             # 앱 기동 (H2 콘솔: http://localhost:8080/h2-console)
```

처음 빌드 후 `build/generated/sources/annotationProcessor/java/main/com/runnershigh/querydsl/domain/` 에 `QMember`, `QOrder` 등이 생성된다. IDE 가 못 찾으면 해당 경로를 generated source 로 지정한다.

## 챕터 ↔ 테스트 매핑

| 챕터 | 노트 파일 | 테스트 파일 | 상태 |
|------|----------|-------------|------|
| 01-03 | 기본 문법과 조인 | `Ch03_BasicQueryAndJoinTest` | ✅ 완성본 (다른 챕터 패턴 참고용) |
| 01-04 | 동적 쿼리 | `Ch04_DynamicQueryTest` | 🟡 기본 2건 + TODO 3건 |
| 01-05 | 프로젝션과 DTO 매핑 | `Ch05_ProjectionAndDtoTest` | 🟡 기본 2건 + TODO 3건 |
| 01-06 | 페이징과 fetch join 함정 | `Ch06_PagingAndFetchJoinTest` | 🟡 기본 1건 + TODO 3건 |
| 02-01 | 커스텀 리포지토리 패턴 | `Ch07_CustomRepositoryTest` | 🟡 기본 2건 + TODO 2건 |
| 02-02 | 테스트와 멀티모듈 | `Ch08_TestSetupTest` | 🟡 기본 1건 + TODO 3건 |
| 02-04 | 실무 변형 모음 | `OrderRepositoryImpl#findSummaries` (상관 서브쿼리) | 🟡 코드 예제 |
| 02-05 | 락과 동시성 제어 | `Ch09_LockingTest` | 🟡 기본 5건 + TODO 4건 |

01-01(입문), 01-02(셋업), 02-03(마이그레이션)은 본 프로젝트의 `build.gradle` + 의존성 자체가 실습이다.

## 도메인

```
Member ─< Order ─< OrderItem >─ Item >─ Category(self-ref)
   │
   └─ Address (Embeddable: city/street/zipcode)
```

- Member: 4명 (alice/bob 서울, charlie/dave 부산, dave 는 주문 없음 — outer join 실습용)
- Order: 3건 (ORDERED 2, CANCELED 1)
- 카테고리/상품: 도서·식품 / 자바책·코틀린책·사과·우유

기본 픽스처는 `support/TestDataLoader#loadDefault` 가 매 테스트 `@BeforeEach` 에서 적재한다.

## 실습 흐름

1. 노트의 챕터를 읽는다.
2. 해당 `Ch??_*Test` 의 기본 케이스를 먼저 돌려 본다 (`./gradlew test --tests Ch04_*`).
3. 클래스 하단 `// TODO [실습 N]` 항목을 직접 채운다.
4. SQL 로그(`org.hibernate.SQL: debug`)로 실제 발생 쿼리를 확인한다.
5. 막히면 노트로 돌아가 해당 절을 다시 읽는다.

## 의도적으로 단순화한 부분

- 멀티모듈 미적용 — 본 프로젝트는 단일 모듈이다. 02-02 의 멀티모듈 가시성 이슈는 노트로 학습한다.
- Web 계층 미포함 — JPA + QueryDSL 학습이 목적이라 Controller/Service 는 만들지 않았다. 필요 시 직접 추가한다.
- BOK/PostgreSQL 등 외부 DB 미사용 — H2 가 충분히 표준 SQL/JPQL 동작을 재현한다.

## 다음 확장

- `@SpringBootTest` 기반 테스트 추가해 `@DataJpaTest` 와의 컨텍스트 차이 직접 확인
- `Querydsl 7.x` 브랜치를 따로 만들어 6.12 ↔ 7.x diff 비교 (02-03 학습 노트 연동)
