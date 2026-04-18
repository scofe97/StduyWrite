# 행동 패턴

---

> 행동 패턴(Behavioral Patterns)은 객체 간의 알고리즘과 책임 분배를 다룬다. 객체들이 어떻게 협력하고 통신하는지를 정의하여, 알고리즘의 변화가 클라이언트에 영향을 주지 않도록 캡슐화한다.

## 패턴 개요

| 패턴 | 목적 | 핵심 아이디어 |
|------|------|-------------|
| Strategy | 알고리즘 교체 가능 | 동작을 인터페이스로 캡슐화 |
| Template Method | 알고리즘 골격 고정 | 변하는 부분만 서브클래스에 위임 |
| Template Callback | 콜백으로 변하는 부분 주입 | `JdbcTemplate` 방식, 상속 없이 확장 |
| Command | 요청을 객체로 캡슐화 | 실행 취소, 큐잉, 로깅 가능 |
| Observer | 상태 변화를 다수에게 전파 | 이벤트 기반 느슨한 결합 |

## Strategy — 전략 패턴

**전략 패턴**은 동일 계열의 알고리즘을 인터페이스로 캡슐화하여 교체 가능하게 한다. 클라이언트는 알고리즘의 구현을 알 필요 없이 인터페이스만으로 사용하므로, 새 알고리즘 추가 시 기존 코드를 수정하지 않아도 된다(OCP). Java 21에서는 람다로 즉석 전략을 만들 수 있어 별도 클래스 없이도 동작한다.

```java
// 전략 인터페이스: @FunctionalInterface이므로 람다 사용 가능
@FunctionalInterface
interface SortStrategy<T extends Comparable<T>> {
    void sort(List<T> list);
}

// 명시적 구현체
class QuickSort<T extends Comparable<T>> implements SortStrategy<T> {
    public void sort(List<T> list) { Collections.sort(list); } // 예시
}

// 전략을 사용하는 컨텍스트
class DataProcessor<T extends Comparable<T>> {
    private SortStrategy<T> strategy;

    DataProcessor(SortStrategy<T> strategy) {
        this.strategy = strategy;
    }

    void setStrategy(SortStrategy<T> strategy) {
        this.strategy = strategy;
    }

    List<T> process(List<T> data) {
        var copy = new ArrayList<>(data);
        strategy.sort(copy);
        return copy;
    }
}

// 사용: 람다로 즉석 전략 주입
var processor = new DataProcessor<Integer>(list -> Collections.sort(list));
processor.setStrategy(list -> list.sort(Comparator.reverseOrder())); // 전략 교체
```

## Template Method — 템플릿 메서드 패턴

**템플릿 메서드 패턴**은 알고리즘의 골격을 상위 클래스의 메서드에 정의하고, 변하는 부분만 서브클래스가 오버라이드하게 한다. 변하지 않는 공통 흐름(순서, 예외 처리)은 상위 클래스가 통제하므로, 서브클래스는 핵심 로직에만 집중할 수 있다.

```java
// 추상 클래스: 알고리즘 골격 정의
abstract class DataExporter {
    // 템플릿 메서드: final로 골격 변경을 막는다
    public final void export(String destination) {
        List<String> data = fetchData();       // 공통 단계 (변함)
        String formatted  = format(data);      // 공통 단계 (변함)
        write(formatted, destination);         // 고정 단계
        notifyCompletion(destination);         // 고정 단계
    }

    protected abstract List<String> fetchData();    // 서브클래스가 구현
    protected abstract String format(List<String> data); // 서브클래스가 구현

    private void write(String data, String dest) {
        System.out.println("Writing to: " + dest);
    }

    // Hook: 서브클래스가 선택적으로 오버라이드
    protected void notifyCompletion(String dest) {
        System.out.println("Export complete: " + dest);
    }
}

class CsvExporter extends DataExporter {
    protected List<String> fetchData() { return List.of("id,name", "1,Alice"); }
    protected String format(List<String> data) { return String.join("\n", data); }
}
```

## Template Callback — 템플릿 콜백 패턴

**템플릿 콜백 패턴**은 템플릿 메서드의 변형으로, 상속 대신 콜백 인터페이스(람다)를 주입하여 변하는 부분을 처리한다. 스프링의 `JdbcTemplate`이 대표적이다. 커넥션 획득, 예외 변환, 리소스 해제라는 고정 흐름은 템플릿이 담당하고, SQL과 결과 매핑이라는 변하는 부분은 콜백으로 주입된다.

```java
// 콜백 인터페이스
@FunctionalInterface
interface ConnectionCallback<T> {
    T doWithConnection(Connection conn) throws SQLException;
}

// 템플릿: 고정 흐름(커넥션 관리)을 담당
class JdbcTemplate {
    private final DataSource dataSource;

    JdbcTemplate(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    // 변하는 부분(SQL 실행)을 콜백으로 받는다
    public <T> T execute(ConnectionCallback<T> callback) {
        try (Connection conn = dataSource.getConnection()) { // 고정: 커넥션 획득
            return callback.doWithConnection(conn);           // 변함: 사용자 로직
        } catch (SQLException e) {
            throw new RuntimeException("DB error", e);        // 고정: 예외 변환
        }
        // 고정: try-with-resources로 자동 해제
    }
}

// 사용: 람다로 변하는 부분만 전달
jdbcTemplate.execute(conn -> {
    var stmt = conn.prepareStatement("SELECT * FROM orders WHERE id = ?");
    stmt.setLong(1, orderId);
    return stmt.executeQuery();
});
```

### Template Method vs Template Callback

| 구분 | Template Method | Template Callback |
|------|----------------|-------------------|
| 확장 방법 | 상속 (서브클래스) | 구성 (콜백 주입) |
| 유연성 | 클래스마다 고정 | 호출마다 다른 콜백 가능 |
| Spring 예시 | `AbstractController` | `JdbcTemplate`, `RestTemplate` |
| 선택 기준 | 재사용 가능한 타입을 만들 때 | 한 번 쓰는 로직을 주입할 때 |

## Command — 커맨드 패턴

**커맨드 패턴**은 요청을 객체로 캡슐화하여 매개변수화, 큐잉, 실행 취소(undo)를 가능하게 한다. 요청을 보내는 쪽과 수행하는 쪽이 분리되므로, 실행 이력 관리나 재시도 로직 구현이 쉬워진다.

```java
@FunctionalInterface
interface Command {
    void execute();
}

interface ReversibleCommand extends Command {
    void undo();
}

// 수신자: 실제 작업을 수행한다
class TextEditor {
    private final StringBuilder text = new StringBuilder();

    void insert(String s) { text.append(s); }
    void delete(int count) { text.delete(text.length() - count, text.length()); }
    String getText() { return text.toString(); }
}

// 구체 커맨드
class InsertCommand implements ReversibleCommand {
    private final TextEditor editor;
    private final String text;

    InsertCommand(TextEditor editor, String text) {
        this.editor = editor;
        this.text = text;
    }

    public void execute() { editor.insert(text); }
    public void undo()    { editor.delete(text.length()); }
}

// 인보커: 커맨드 이력을 관리한다
class CommandHistory {
    private final Deque<ReversibleCommand> history = new ArrayDeque<>();

    void execute(ReversibleCommand cmd) {
        cmd.execute();
        history.push(cmd);
    }

    void undo() {
        if (!history.isEmpty()) history.pop().undo();
    }
}
```

## Observer — 옵저버 패턴

**옵저버 패턴**은 객체의 상태 변화를 구독하는 모든 관찰자(observer)에게 자동으로 알림을 보낸다. 발행자(subject)와 구독자(observer)가 인터페이스로만 연결되므로 느슨한 결합이 달성된다. Spring의 `ApplicationEvent`와 `@EventListener`가 이 패턴의 프레임워크 수준 구현이다.

```java
// 옵저버 인터페이스
interface OrderEventListener {
    void onOrderPlaced(Order order);
}

// 발행자
class OrderService {
    private final List<OrderEventListener> listeners = new ArrayList<>();

    void subscribe(OrderEventListener listener) {
        listeners.add(listener);
    }

    void placeOrder(Order order) {
        // 핵심 비즈니스 로직
        System.out.println("Order placed: " + order.id());
        // 이벤트 발행
        listeners.forEach(l -> l.onOrderPlaced(order));
    }
}

// 구독자들: 서로를 모른다
class EmailNotifier implements OrderEventListener {
    public void onOrderPlaced(Order order) {
        System.out.println("Email sent for order: " + order.id());
    }
}

class InventoryManager implements OrderEventListener {
    public void onOrderPlaced(Order order) {
        System.out.println("Inventory updated for order: " + order.id());
    }
}

// Spring 방식 (참고)
// @Component
// class EmailNotifier {
//     @EventListener
//     public void handle(OrderPlacedEvent event) { ... }
// }
```
