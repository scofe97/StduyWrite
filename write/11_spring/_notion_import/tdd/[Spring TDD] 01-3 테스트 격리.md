# [Spring TDD] 01-3. 테스트 격리

주제: Spring TDD
연관 노트: [Database Study] 04-x. 테스트 -  DB 트랜잭션⭐ (https://www.notion.so/Database-Study-04-x-DB-74d55654cb3c4ad5b254af101004ff00?pvs=21)

- 참고
    
    [[Spring] @SpringBootTest의 테스트 격리시키기(TestExecutionListener), @Transactional로 롤백되지 않는 이유](https://mangkyu.tistory.com/264)
    
    [테스트 격리(Test Isolation)](https://velog.io/@ljinsk3/테스트-격리Test-Isolation)
    
    [격리된 테스트 (Isolated Test) (feat. Spring 에서 테스트 격리하기)](https://hudi.blog/isolated-test/)
    
    [[Spring] 테스트 격리하기](https://velog.io/@bingomangsoo/Spring-테스트의-격리)
    

# **격리된 테스트 (Isolated Test)**

---

<aside>
💡 **NOTE**

> ***데이터베이스와 같은 공유 자원을 사용하는 테스트는 실행 순서에 따라 성공, 실패 여부가 결정되는 비결정적인 테스트가 될 수 있다!***
> 
- 비결정적 테스트는 실패하면 버그인지, 순서문제인지 파악하기 힘들다.
- 테스트는 순서에 상관없는 독립적(결정적)으로 실행되어야 한다.
- 테스트 격리는 공유자원을 사용하는 여러 테스트끼리 격리하여 서로 영향을 받지 못하게한다.
</aside>

# Spring 테스트 격리방법

---

## 테스트 더블(Test Double)

<aside>
✍️ **NOTE**

> ***테스트 더블 ⇒ 실제 객체가 아닌 테스트에 사용되는 객체를 만들어서 사용하는 방식!***
> 
- Mocking을 함으로써, 공유자원으로 부터의 의존을 제거한다.
- 보통 Mockito Framework를 많이 사용한다.
</aside>

## @Transactional ⭐

<aside>
✍️ **NOTE**

> ***테스트 코드의 @Transactional은 테스트 메소드가 종료될때 롤백되어 이전상태로 돌려준다!***
> 

```java
@Transactional
@JdbcTest
class ServiceTest {

    @Test
    void test1() {}
```

</aside>

## **@JdbcTest, @DataJpaTest**

<aside>
✍️ **NOTE**

> ***@JdbcTest, @DataJpaTest는 내부에 @Transactional을 가지고 있다!***
> 

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@BootstrapWith(JdbcTestContextBootstrapper.class)
@ExtendWith(SpringExtension.class)
@OverrideAutoConfiguration(enabled = false)
@TypeExcludeFilters(JdbcTypeExcludeFilter.class)
@Transactional
@AutoConfigureCache
@AutoConfigureJdbc
@AutoConfigureTestDatabase
@ImportAutoConfiguration
public @interface JdbcTest {
```

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@BootstrapWith(DataJpaTestContextBootstrapper.class)
@ExtendWith(SpringExtension.class)
@OverrideAutoConfiguration(enabled = false)
@TypeExcludeFilters(DataJpaTypeExcludeFilter.class)
@Transactional
@AutoConfigureCache
@AutoConfigureDataJpa
@AutoConfigureTestDatabase
@AutoConfigureTestEntityManager
@ImportAutoConfiguration
public @interface DataJpaTest {
```

- 스프링부트는 JPA Repository를 손쉽게 테스트할 수 있는 `@DataJpaTest`를 제공한다.
- 기본적으로 **인메모리 데이터베이스인 H2를 기반**으로 테스트용 데이터베이스를 구축하며, 테스트가 **끝나면 트랜잭션 롤백**을 해준다.
- Repository 계층은 실제 DB와 통신없이 단순 Mocking하는건 의미가 없으므로 직접 데이터베이스와 통싱하는 `@DataJpaTest`를 사용
</aside>

## @Sql 어노테이션

<aside>
✍️ **NOTE**

> ***스프링에서 제공하는 어노테이션으로, 테스트 클래스에 해당 어노테이션을 통해 테스트 실행전 지정된 경로의 SQL 스크립트를 실행시켜준다!***
> 

```java
@Sql("/truncate.sql")
public class IsolatedTest {
    // ...
```

```sql
TRUNCATE TABLE member;
TRUNCATE TABLE article;
```

- **TRUNCATE**
    - **SQL의 명령어로, 지정된 테이블의 모든 레코드를 삭제한다**
    - DELETE와는 달리, 구조나 스키마는 유지된다.
</aside>

# **@Transactional로 롤백되지 않는 상황**

---

<aside>
💡 **NOTE**

> ***@SpringBootTest를 RANDOM_PORT, DEFINED_PORT를 사용하면 @Transactional이 롤백되지 않는다!***
> 

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class MyTest {}
```

</aside>

## **@SpringBootTest에서 트랜잭션 롤백되지 않는 이유**

<aside>
✍️ **NOTE**

> ***RANDOM_PORT, DEFINED_PORT를 사용하면 별도의 쓰레드에서 스프링 컨테이너가 실행된다!***
> 
- 테스트가 끝나고 이를 롤백시키려면 트랜잭션으로 묶여야 하는데, 다른 쓰레드에서 실행되니 묶을수가 없는 것이다.
- 이 경우에는 **모든 테이블의 데이터를 삭제해 초기화해주는 방법 밖에 없다!**
</aside>

## **@SpringBootTest의 테스트 격리시키기(TestExecutionListener)**

<aside>
✍️ **NOTE**

> ***모든 테이블의 데이터를 삭제해 초기화 하는 방법은 2가지가 존재한다!***
> 

### 1. Repository를 조회해서 deleteAll() 실행 ❌

- 외래키 등의 제약 조건에 따라 삭제가 어려울 수 있다.
- Repository를 사용하지 않는 테이블은 삭제가 되지 않는다.

### 2. TRUNCATE 명령어 사용 ✅

- 1개의 테스트가 끝날 때마다 실행되어야 하고, 다음과 같이 실행되어야 한다.
1. 테스트가 끝나면 모든 테이블에 대한 TRUNCATE TABLE 명령어를 얻는다.
2. 제약조건 무효화 명령어를 실행시킨다.
3. 모든 TRUNCATE TABLE 명령어를 실행시킨다.
4. 제약조건 재설정 명령어를 실행시킨다.
</aside>

## TRUNCATE 명령어 사용

<aside>
✍️ **NOTE**

```java
@Component
public class DatabaseCleanup implements InitializingBean {
    @PersistenceContext
    private EntityManager entityManager;

    private List<String> tableNames;

    @Override // 1. 테스트가 끝나면 모든 테이블에 대한 TRUNCATE TABLE 명령어를 얻음
    public void afterPropertiesSet() {
        final Set<EntityType<?>> entities = entityManager.getMetamodel().getEntities(); // EntityManager에서 JPA Entity를 전부 가져오고
        tableNames = entities.stream()
                .filter(e -> isEntity(e) && hasTableAnnotation(e))  // Entity랑 TABLE 어노테이션 있는지 확인해서 tableNames에 리스트로 전부 담음.
                .map(e -> {
                    String tableName = e.getJavaType().getAnnotation(Table.class).name();
                    return tableName.isBlank() ? CaseFormat.UPPER_CAMEL.to(CaseFormat.LOWER_UNDERSCORE, e.getName()) : tableName;
                })
                .collect(Collectors.toList());

        final List<String> entityNames = entities.stream()
                .filter(e -> isEntity(e) && !hasTableAnnotation(e)) // entity면서 table이 없는애들을 ProductItem -> product_item처럼 변경
                .map(e -> CaseFormat.UPPER_CAMEL.to(CaseFormat.LOWER_UNDERSCORE, e.getName()))
                .toList();

        tableNames.addAll(entityNames);
    }

    private boolean isEntity(final EntityType<?> e) {
        return null != e.getJavaType().getAnnotation(Entity.class);
    }

    private boolean hasTableAnnotation(final EntityType<?> e) {
        return null != e.getJavaType().getAnnotation(Table.class);
    }

    @Transactional
    public void execute() {
        entityManager.flush();

				// 2. 제약조건 무효화 명령어를 실행시킴
        entityManager.createNativeQuery("SET REFERENTIAL_INTEGRITY FALSE").executeUpdate();
        for (final String tableName : tableNames) {

						// 3. 모든 TRUNCATE TABLE 명령어를 실행시킴
            entityManager.createNativeQuery("TRUNCATE TABLE " + tableName).executeUpdate();
            entityManager.createNativeQuery("ALTER TABLE " + tableName + " ALTER COLUMN ID RESTART WITH 1").executeUpdate();
        }

				// 4. 제약조건 무효화 명령어를 실행시킴
        entityManager.createNativeQuery("SET REFERENTIAL_INTEGRITY TRUE").executeUpdate();
    }

}
```

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class StationAcceptanceTest {

    @Autowired
    private JdbcTemplate jdbcTemplate;
    
    
    @AfterEach
    public void afterEach() {
        final List<String> truncateQueries = getTruncateQueries(jdbcTemplate);
        truncateTables(jdbcTemplate, truncateQueries);
    }

    private List<String> getTruncateQueries(final JdbcTemplate jdbcTemplate) {
        return jdbcTemplate.queryForList("SELECT Concat('TRUNCATE TABLE ', TABLE_NAME, ';') AS q FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC'", String.class);
    }

    private void truncateTables(final JdbcTemplate jdbcTemplate, final List<String> truncateQueries) {
        execute(jdbcTemplate, "SET REFERENTIAL_INTEGRITY FALSE");
        truncateQueries.forEach(v -> execute(jdbcTemplate, v));
        execute(jdbcTemplate, "SET REFERENTIAL_INTEGRITY TRUE");
    }

    private void execute(final JdbcTemplate jdbcTemplate, final String query) {
        jdbcTemplate.execute(query);
    }

}
```

```java
public class AcceptanceTestExecutionListener extends AbstractTestExecutionListener {

    @Override
    public void afterTestMethod(final TestContext testContext) {
        final JdbcTemplate jdbcTemplate = getJdbcTemplate(testContext);
        final List<String> truncateQueries = getTruncateQueries(jdbcTemplate);
        truncateTables(jdbcTemplate, truncateQueries);
    }

    private List<String> getTruncateQueries(final JdbcTemplate jdbcTemplate) {
        return jdbcTemplate.queryForList("SELECT Concat('TRUNCATE TABLE ', TABLE_NAME, ';') AS q FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'PUBLIC'", String.class);
    }

    private JdbcTemplate getJdbcTemplate(final TestContext testContext) {
        return testContext.getApplicationContext().getBean(JdbcTemplate.class);
    }

    private void truncateTables(final JdbcTemplate jdbcTemplate, final List<String> truncateQueries) {
        execute(jdbcTemplate, "SET REFERENTIAL_INTEGRITY FALSE");
        truncateQueries.forEach(v -> execute(jdbcTemplate, v));
        execute(jdbcTemplate, "SET REFERENTIAL_INTEGRITY TRUE");
    }

    private void execute(final JdbcTemplate jdbcTemplate, final String query) {
        jdbcTemplate.execute(query);
    }

}
```

</aside>