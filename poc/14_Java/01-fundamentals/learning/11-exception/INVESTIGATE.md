# 예외 처리: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 체크 예외를 언체크로 감싸는 것은 올바른 접근인가?

### 왜 이 질문이 중요한가
`IOException`을 잡아서 `RuntimeException`으로 감싸 던지는 코드는 실무에서 흔하다. 이것이 단순히 컴파일러를 침묵시키는 편법인지, 아니면 합리적인 설계 결정인지 구분하지 못하면 예외 처리 전략을 체계적으로 세울 수 없다. Spring이 이 접근을 어떻게 활용하는지도 함께 이해해야 한다.

### 답변

체크 예외의 원래 의도는 "호출자가 반드시 처리해야 하는 복구 가능한 조건"을 강제하는 것이다. `FileNotFoundException`은 파일이 없을 때 호출자가 다른 경로를 시도하거나 사용자에게 알릴 수 있다는 의미다. 그러나 현실에서 체크 예외가 과도하게 사용되면 두 가지 문제가 생긴다.

첫째, 의미 없는 전파다. 하위 계층의 `SQLException`이 서비스, 컨트롤러까지 `throws SQLException`으로 전파되면 상위 계층이 SQL 세부사항에 결합된다. 컨트롤러가 `SQLException`을 알 이유가 없다.

둘째, 람다와의 호환성 문제다. `Runnable`, `Function` 등 함수형 인터페이스는 체크 예외를 선언하지 않으므로 체크 예외를 던지는 코드를 람다 안에서 쓰면 컴파일 에러가 난다.

```java
// 체크 예외를 언체크로 변환하는 합리적인 경우
// 1. 복구 불가능한 경우 — DB 연결 실패 등
public User findById(Long id) {
    try {
        return jdbcTemplate.queryForObject(...);
    } catch (DataAccessException e) {
        // Spring이 이미 SQLException → DataAccessException(언체크)으로 변환해줌
        throw new UserNotFoundException("User not found: " + id, e); // cause 보존 필수
    }
}

// 2. 람다에서 체크 예외가 필요할 때
@FunctionalInterface
interface CheckedSupplier<T> {
    T get() throws Exception;
}

static <T> Supplier<T> wrap(CheckedSupplier<T> supplier) {
    return () -> {
        try { return supplier.get(); }
        catch (Exception e) { throw new RuntimeException(e); } // cause 보존
    };
}
```

핵심 원칙은 두 가지다. 첫째, 변환 시 반드시 원인(cause)을 보존해야 한다. `new RuntimeException(e)`처럼 원래 예외를 cause로 전달해야 스택 트레이스에서 실제 원인을 추적할 수 있다. `new RuntimeException("message")`처럼 원인을 버리면 디버깅이 불가능해진다. 둘째, 복구 가능한 조건은 체크 예외로 유지한다. "이 예외를 받은 호출자가 다르게 행동할 수 있는가?"가 체크 여부 판단 기준이다.

---

## Q2. Spring의 예외 처리 전략과 도메인 예외 설계

### 왜 이 질문이 중요한가
Spring MVC 애플리케이션에서 예외 처리를 `try-catch`로 각 메서드마다 처리하는 것은 관심사 분리 원칙 위반이다. Spring이 제공하는 예외 처리 메커니즘을 이해하고, 도메인 예외를 어떻게 설계해야 HTTP 응답 코드와 자연스럽게 매핑되는지 알아야 한다.

### 답변

Spring의 예외 처리는 세 계층으로 나뉜다. 첫 번째는 `@ExceptionHandler`로, 특정 컨트롤러 내부에서 발생한 예외를 처리한다. 컨트롤러 전용 예외 처리에 적합하다. 두 번째는 `@ControllerAdvice`(`@RestControllerAdvice`)로, 전역 예외 처리기다. 모든 컨트롤러에서 발생한 예외를 한 곳에서 처리할 수 있다. 세 번째는 `ResponseEntityExceptionHandler`로, Spring MVC 기본 예외(메서드 인자 바인딩 실패 등)를 처리하는 기반 클래스다.

```java
// 도메인 예외 계층 설계
public abstract class BusinessException extends RuntimeException {
    private final ErrorCode errorCode;
    protected BusinessException(ErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
    public ErrorCode getErrorCode() { return errorCode; }
}

public class UserNotFoundException extends BusinessException {
    public UserNotFoundException(Long id) {
        super(ErrorCode.USER_NOT_FOUND, "User not found: " + id);
    }
}

public class InsufficientBalanceException extends BusinessException {
    public InsufficientBalanceException(Money required, Money available) {
        super(ErrorCode.INSUFFICIENT_BALANCE,
              "Required: " + required + ", Available: " + available);
    }
}

// ErrorCode에 HTTP 상태 코드 매핑
public enum ErrorCode {
    USER_NOT_FOUND(HttpStatus.NOT_FOUND, "U001"),
    INSUFFICIENT_BALANCE(HttpStatus.UNPROCESSABLE_ENTITY, "P001"),
    INVALID_INPUT(HttpStatus.BAD_REQUEST, "C001");

    private final HttpStatus status;
    private final String code;
    // ...
}

// 전역 예외 처리기
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(BusinessException e) {
        ErrorCode code = e.getErrorCode();
        return ResponseEntity.status(code.getStatus())
            .body(new ErrorResponse(code.getCode(), e.getMessage()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception e) {
        log.error("Unexpected error", e); // 내부 에러는 로그만, 클라이언트에 노출 금지
        return ResponseEntity.internalServerError()
            .body(new ErrorResponse("S001", "Internal server error"));
    }
}
```

이 설계의 핵심은 비즈니스 로직 코드에서 HTTP 개념(`HttpStatus`, `ResponseEntity`)이 완전히 사라진다는 점이다. 서비스 레이어는 도메인 예외만 던지고 HTTP 매핑은 `GlobalExceptionHandler`가 담당한다. 도메인 로직을 HTTP 없이도 테스트할 수 있고, REST API에서 gRPC로 전환해도 서비스 코드는 변경이 없다.
