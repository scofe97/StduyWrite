# JUnit 5 기초
---
> JUnit 5는 단순한 테스트 러너를 넘어 플랫폼 수준의 확장 가능한 테스트 생태계로 설계되었다. 생명주기 애노테이션과 풍부한 Assertions API를 통해 가독성 높은 테스트를 작성할 수 있다.

## 1. JUnit 5 아키텍처

JUnit 5는 세 개의 독립 모듈로 구성된다. 단일 JAR로 배포되던 JUnit 4와 달리, 각 모듈이 명확한 책임을 갖도록 분리되어 IDE, 빌드 도구, 서드파티 엔진이 독립적으로 진화할 수 있다.

세 모듈의 역할은 다음과 같다:

- **JUnit Platform**: 테스트를 발견하고 실행하는 기반 인프라. `TestEngine` SPI를 통해 다양한 테스트 프레임워크를 플러그인 방식으로 지원한다.
- **JUnit Jupiter**: JUnit 5 스타일의 테스트를 작성하는 API와 엔진. `@Test`, `@BeforeEach` 등 새로운 애노테이션을 제공한다.
- **JUnit Vintage**: JUnit 3/4로 작성된 기존 테스트를 Platform 위에서 실행할 수 있도록 브릿지 역할을 한다.

```java
// build.gradle 의존성 구성
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

test {
    useJUnitPlatform()
}
```

## 2. 생명주기 애노테이션

테스트 메서드는 독립적으로 실행되어야 한다. JUnit 5는 기본적으로 각 테스트 메서드마다 테스트 클래스 인스턴스를 새로 생성하므로, 생명주기 메서드로 공유 상태를 안전하게 관리할 수 있다.

생명주기 애노테이션과 실행 순서는 다음과 같다:

- `@BeforeAll`: 클래스 내 모든 테스트 실행 전 한 번만 실행. `static` 메서드여야 한다.
- `@BeforeEach`: 각 테스트 메서드 실행 전마다 실행. 픽스처(fixture) 초기화에 사용한다.
- `@AfterEach`: 각 테스트 메서드 실행 후마다 실행. 리소스 해제에 사용한다.
- `@AfterAll`: 클래스 내 모든 테스트 실행 후 한 번만 실행. `static` 메서드여야 한다.

```java
class OrderServiceTest {

    static DatabaseConnection db;
    OrderService orderService;

    @BeforeAll
    static void initDatabase() {
        db = DatabaseConnection.connect("jdbc:h2:mem:test");
    }

    @BeforeEach
    void setUp() {
        orderService = new OrderService(db);
        db.beginTransaction();
    }

    @AfterEach
    void tearDown() {
        db.rollback();
    }

    @AfterAll
    static void closeDatabase() {
        db.close();
    }
}
```

## 3. 주요 애노테이션

JUnit 5는 테스트 구성과 문서화를 위한 다양한 애노테이션을 제공한다. 이 애노테이션들을 조합하면 테스트 의도를 코드 수준에서 명확히 표현할 수 있다.

### 3-1. 기본 구성 애노테이션

```java
@DisplayName("주문 서비스 테스트")
class OrderServiceTest {

    @Test
    @DisplayName("재고가 충분할 때 주문이 성공한다")
    void 재고가_충분할때_주문_성공() {
        // 테스트 내용
    }

    @Test
    @Disabled("결제 모듈 연동 후 활성화 예정")
    void 결제_연동_테스트() {
        // 비활성화된 테스트
    }

    @Test
    @Tag("integration")
    void 외부_API_연동_테스트() {
        // 태그로 그룹화하여 선택적 실행 가능
    }
}
```

`@DisplayName`은 테스트 보고서에 표시될 이름을 지정한다. 한국어나 공백을 포함한 자연어 설명을 쓸 수 있어 메서드명보다 가독성이 높다. `@Tag`는 빌드 설정에서 특정 태그를 포함하거나 제외하여 테스트 스위트를 구성할 때 유용하다.

### 3-2. 중첩 테스트와 반복 테스트

`@Nested`는 관련 테스트를 논리적 그룹으로 묶는다. 같은 도메인의 시나리오를 계층 구조로 표현하면 테스트 보고서가 문서처럼 읽힌다.

```java
@DisplayName("재고 관리 테스트")
class InventoryTest {

    @Nested
    @DisplayName("재고 감소 시나리오")
    class 재고_감소 {

        @Test
        @DisplayName("정상 수량 감소")
        void 정상_수량_감소() { }

        @Test
        @DisplayName("재고 초과 감소 시 예외 발생")
        void 재고_초과_시_예외() { }
    }

    @RepeatedTest(3)
    @DisplayName("동시 요청 처리 테스트 (3회 반복)")
    void 동시_요청_처리(RepetitionInfo info) {
        System.out.println("반복 " + info.getCurrentRepetition());
    }
}
```

## 4. Assertions

JUnit Jupiter의 `Assertions` 클래스는 다양한 검증 메서드를 제공한다. 검증 실패 시 의미 있는 에러 메시지를 출력하도록 설명 메시지를 추가하는 것이 좋다.

### 4-1. 기본 검증

```java
import static org.junit.jupiter.api.Assertions.*;

@Test
void 기본_검증_예시() {
    Order order = new Order(1L, "PENDING", 5000);

    assertEquals(5000, order.getAmount(), "주문 금액이 일치해야 한다");
    assertTrue(order.isPending(), "신규 주문은 PENDING 상태여야 한다");
    assertNotNull(order.getId(), "주문 ID는 null이면 안 된다");
}

@Test
void 예외_검증() {
    InventoryService service = new InventoryService();

    IllegalArgumentException ex = assertThrows(
        IllegalArgumentException.class
        , () -> service.decrease(0, -1)
        , "음수 수량 감소는 예외를 던져야 한다"
    );

    assertEquals("수량은 양수여야 합니다", ex.getMessage());
}
```

### 4-2. 복합 검증과 타임아웃

`assertAll`은 모든 검증을 한 번에 실행하고 실패 목록을 한꺼번에 보고한다. 첫 번째 검증 실패 시 이후 검증을 건너뛰는 일반 방식과 달리, 전체 실패 원인을 한 번에 파악할 수 있다.

```java
@Test
void 복합_검증() {
    Order order = createOrder();

    assertAll("주문 객체 전체 검증"
        , () -> assertEquals(1L, order.getId())
        , () -> assertEquals("PENDING", order.getStatus())
        , () -> assertEquals(5000, order.getAmount())
    );
}

@Test
void 타임아웃_검증() {
    assertTimeout(Duration.ofMillis(100), () -> {
        // 100ms 이내에 완료되어야 한다
        orderService.process(new Order());
    });
}
```

## 5. 파라미터화 테스트

`@ParameterizedTest`는 동일한 테스트 로직을 다양한 입력값으로 반복 실행한다. 경계값 분석이나 동등 분할 테스트에 효과적이며, 테스트 중복을 제거한다.

### 5-1. 소스 애노테이션 종류

```java
// @ValueSource: 단일 타입 값 배열
@ParameterizedTest
@ValueSource(ints = {1, 5, 100, Integer.MAX_VALUE})
@DisplayName("양수 수량은 검증을 통과해야 한다")
void 양수_수량_검증(int quantity) {
    assertTrue(InventoryValidator.isValid(quantity));
}

// @CsvSource: 다중 파라미터 (CSV 형식)
@ParameterizedTest
@CsvSource({
    "1000, 10, 10000"
    , "2000, 5, 10000"
    , "500, 3, 1500"
})
void 총액_계산(int price, int qty, int expected) {
    assertEquals(expected, price * qty);
}

// @MethodSource: 복잡한 객체 파라미터
@ParameterizedTest
@MethodSource("provideOrders")
void 주문_상태_검증(Order order, String expectedStatus) {
    assertEquals(expectedStatus, order.getStatus());
}

static Stream<Arguments> provideOrders() {
    return Stream.of(
        Arguments.of(new Order(1L, 5000), "PENDING")
        , Arguments.of(new Order(2L, 0), "INVALID")
    );
}

// @EnumSource: Enum 값 순회
@ParameterizedTest
@EnumSource(OrderStatus.class)
void 모든_상태값_처리(OrderStatus status) {
    assertDoesNotThrow(() -> orderService.handleStatus(status));
}
```

## 6. 조건부 실행

특정 환경에서만 실행해야 하는 테스트는 `@Enabled*` / `@Disabled*` 애노테이션으로 조건을 선언한다. `@Assumptions`로 런타임 조건을 확인하는 방식보다 의도가 명확하다.

```java
@Test
@EnabledOnOs(OS.LINUX)
void Linux_전용_테스트() {
    // Linux 환경에서만 실행된다
}

@Test
@EnabledOnOs({OS.MAC, OS.WINDOWS})
void 로컬_개발_환경_테스트() {
    // Mac과 Windows에서만 실행된다
}

@Test
@EnabledIf("#{systemProperties['env'] == 'dev'}")
void 개발_환경_전용_테스트() {
    // env 시스템 프로퍼티가 'dev'일 때만 실행된다
}
```

## 7. 테스트 실행 순서

기본적으로 JUnit 5는 테스트 메서드 실행 순서를 보장하지 않는다. 각 테스트는 독립적이어야 하므로 순서 의존성은 설계 결함을 의미한다. 그러나 통합 테스트나 시나리오 테스트에서 순서가 필요하다면 `@TestMethodOrder`를 사용한다.

```java
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class 주문_시나리오_통합테스트 {

    @Test
    @Order(1)
    void 주문_생성() { }

    @Test
    @Order(2)
    void 결제_처리() { }

    @Test
    @Order(3)
    void 배송_시작() { }
}

// 알파벳 순서로 실행
@TestMethodOrder(MethodOrderer.MethodName.class)
class AlphabetOrderTest { }

// 랜덤 순서 (순서 의존성 검출에 유용)
@TestMethodOrder(MethodOrderer.Random.class)
class RandomOrderTest { }
```

`MethodOrderer.OrderAnnotation`은 `@Order` 값이 작을수록 먼저 실행된다. 순서 없는 테스트는 `@Order`가 없는 것으로 처리되어 뒤에 배치된다.

## 8. 테스트 인스턴스 생명주기

JUnit 5는 기본적으로 각 테스트 메서드마다 테스트 클래스의 새 인스턴스를 생성한다. 이를 *PER_METHOD* 생명주기라 하며, 테스트 간 상태 공유를 막아 격리성을 보장한다.

`@TestInstance(Lifecycle.PER_CLASS)`를 선언하면 클래스 전체에서 인스턴스 하나를 공유한다:

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class SharedStateTest {

    private List<String> executionLog = new ArrayList<>();

    @BeforeAll
    void initAll() {
        // static 없이 @BeforeAll 사용 가능
        executionLog.add("init");
    }

    @Test
    void firstTest() {
        executionLog.add("first");
        assertThat(executionLog).contains("init", "first");
    }

    @Test
    void secondTest() {
        // executionLog에 이전 테스트 결과가 누적되어 있다 — 주의 필요
        executionLog.add("second");
    }
}
```

`PER_CLASS`의 주요 사용 사례는 두 가지다. 첫째, Kotlin처럼 `static` 메서드를 직접 지원하지 않는 언어에서 `@BeforeAll`을 쓸 때다. 둘째, 생성 비용이 큰 객체(예: DB 커넥션, 임베디드 서버)를 인스턴스 필드로 공유할 때다. 단, 테스트 간 상태 누출이 발생하지 않도록 `@BeforeEach`에서 가변 상태를 명시적으로 초기화해야 한다.
