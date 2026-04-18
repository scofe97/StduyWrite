# Mockito와 테스트 더블: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. Mock 남용이 테스트 품질을 해치는 메커니즘은 무엇인가?

### 왜 이 질문이 중요한가

Mock은 테스트 격리를 위한 강력한 도구지만, 과도하게 사용하면 테스트가 구현 세부사항에 결합되어 리팩토링 비용이 급증한다. "Mock이 많다 = 좋은 테스트"라는 오해를 깨는 것이 테스트 품질 향상의 출발점이다.

### 답변

Mock 남용이 테스트 품질을 해치는 메커니즘은 세 가지다.

**첫째, 구현 결합(Implementation Coupling)**이다. Mock으로 내부 메서드 호출을 검증(`verify`)하면, 테스트가 "무엇을 하는가(what)"가 아니라 "어떻게 하는가(how)"를 검증하게 된다. 내부 구현을 리팩토링하면 동작은 동일해도 테스트가 깨진다.

```java
// 나쁜 예: 내부 구현 흐름을 검증한다
@Test
void placeOrderCallsRepositoryAndPublisher() {
    orderService.placeOrder(order);

    verify(orderRepository).save(order);        // 구현 세부사항
    verify(eventPublisher).publish(any());      // 구현 세부사항
    verify(inventoryService).deduct(any());     // 구현 세부사항
}

// 좋은 예: 결과(outcome)를 검증한다
@Test
void placeOrderPersistsOrderWithConfirmedStatus() {
    orderService.placeOrder(order);

    var saved = orderRepository.findById(order.id());
    assertThat(saved).isPresent();
    assertThat(saved.get().status()).isEqualTo(CONFIRMED);
}
```

**둘째, 신뢰도 손실**이다. Mock은 실제 협력 객체가 아니므로, Mock이 잘못 설정되면 프로덕션에서는 다르게 동작할 수 있다. 특히 `thenReturn`으로 설정한 값이 실제 구현과 다른 타입이나 상태를 반환할 때 테스트는 통과하지만 실제 코드는 실패한다.

**셋째, 테스트 가독성 저하**이다. Mock 설정(`when...thenReturn`)이 테스트 본문보다 길어지면 무엇을 테스트하는지 파악하기 어려워진다. 한 테스트에 `when` 선언이 5개 이상이라면 테스트 대상이 너무 많은 의존성을 가진다는 설계 신호다.

올바른 Mock 사용 원칙은 **소유하지 않은 것만 Mock하라**는 규칙이다. 외부 시스템(DB, HTTP API, 메시지 브로커)을 격리할 때는 Mock이 적절하다. 같은 모듈 내부의 협력 객체를 Mock하는 것은 과도하다.

---

## Q2. Spy와 Mock의 실무 선택 기준은 무엇인가?

### 왜 이 질문이 중요한가

`@Mock`과 `@Spy`의 차이를 모르면 테스트 의도와 다른 동작을 만들게 된다. 특히 레거시 코드나 부분 동작을 테스트해야 할 때 잘못된 선택이 테스트 신뢰도를 낮춘다.

### 답변

`Mock`은 **완전한 가짜(fake)**다. 모든 메서드가 기본값(0, null, false, 빈 컬렉션)을 반환하며, `when`으로 명시하지 않은 메서드는 실제 코드를 실행하지 않는다. 의존성 격리에 사용한다.

`Spy`는 **실제 객체를 감시하는 래퍼**다. `when`으로 설정하지 않은 메서드는 실제 구현을 실행한다. 레거시 코드나 실제 동작의 일부만 교체해야 할 때 사용한다.

```java
// Mock: 모든 메서드가 기본값 반환
OrderRepository mockRepo = mock(OrderRepository.class);
// mockRepo.findAll() → [] (빈 리스트, 실제 DB 호출 안 함)

// Spy: 실제 객체 기반, 일부만 교체
List<String> spyList = spy(new ArrayList<>());
spyList.add("hello");                          // 실제 ArrayList.add() 실행
doReturn(999).when(spyList).size();            // size()만 교체
assertThat(spyList.get(0)).isEqualTo("hello"); // 실제 데이터 접근 가능
assertThat(spyList.size()).isEqualTo(999);      // 교체된 동작

// Spy 주의: when().thenReturn() 대신 doReturn().when() 사용
// when(spy.method()) 형식은 실제 메서드를 먼저 호출하므로 예외 발생 가능
// doReturn(value).when(spy).method() 형식이 안전하다
```

실무 선택 기준은 다음과 같다. Mock은 외부 의존성(Repository, RestClient, MessageBroker)을 격리할 때 사용한다. Spy는 두 가지 상황에서 사용한다. 첫째, 레거시 코드에서 일부 메서드만 교체해야 하는 경우다. 둘째, 실제 컬렉션이나 객체의 일부 동작을 오버라이드해야 하는 경우다. 단, Spy 사용이 잦다면 그 클래스의 의존성 구조가 테스트하기 어렵게 설계되어 있다는 신호일 수 있으므로, Spy보다 리팩토링을 먼저 고려해야 한다.

| 구분 | Mock | Spy |
|------|------|-----|
| 기반 | 완전 가짜 | 실제 객체 |
| 미설정 메서드 | 기본값 반환 | 실제 실행 |
| 주 용도 | 의존성 격리 | 부분 오버라이드 |
| 남용 신호 | verify가 너무 많음 | Spy 없이 리팩토링 가능한 경우 |
