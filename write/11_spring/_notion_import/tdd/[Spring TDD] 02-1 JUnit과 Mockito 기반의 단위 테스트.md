# [Spring TDD] 02-1. JUnit과 Mockito 기반의 단위 테스트

주제: Spring TDD

- 참고
    
    [[Java] Mockito 사용법 (1) - Mock이란?, Mockito 소개](https://effortguy.tistory.com/141)
    
    [[Spring Boot + Mockito] 07. Argument Matchers 활용](https://wiki.yowu.dev/ko/dev/Mockito/Spring-Boot-Mockito-Series/7-Utilizing-Argument-Matchers)
    
    [JUnit5 완벽 가이드](https://donghyeon.dev/junit/2021/04/11/JUnit5-완벽-가이드/)
    
    [[Spring] JUnit과 Mockito 기반의 Spring 단위 테스트 코드 작성법 (3/3)](https://mangkyu.tistory.com/145)
    

# **Mockito 소개**

---

<aside>
💡 **NOTE**

> ***Mockito ⇒ 개발자가 동작을 직접 제어할 수 있는 가짜 객체를 지원하는 테스트 프레임워크***
> 

![Mockito 예시) DB에서 실제로 데이터를 읽지않고, 가짜 객체(Mock)으로 만들어서 테스트한다!](%5BSpring%20TDD%5D%2002-1%20JUnit%EA%B3%BC%20Mockito%20%EA%B8%B0%EB%B0%98%EC%9D%98%20%EB%8B%A8%EC%9C%84%20%ED%85%8C%EC%8A%A4%ED%8A%B8/Untitled.png)

Mockito 예시) DB에서 실제로 데이터를 읽지않고, 가짜 객체(Mock)으로 만들어서 테스트한다!

- Spring 개발은 여러 객체들 간의 의존성이 생기고, 이러한 의존성이 단위 테스트 작성을 어렵게한다.
- 이러한 의존성이 복잡한 상황을 위해서 **가짜 객체를 주입시켜주는 Mockito 라이브러리를 활용**할 수 있다!
</aside>

## **Mockito 주석 활성화**

<aside>
✍️ **NOTE**

> ***Mockito도 테스팅 프레임워크이기 때문에 JUnit과 결합되기 위해서는 별도의 작업이 필요하다.***
> 

### 1. MockitoJunitRunner 방식(권장)

```java
@ExtendWith(MockitoExtension.class)
class Test{}
```

### 2. MockitoAnnotations.openMocks()

```java
@BeforeEach
void setUp() {
    MockitoAnnotations.openMocks(this);
}
```

</aside>

# **Mockito 사용법**

---

## Stubbing

<aside>
✍️ **NOTE**

> ***Stubbing은 테스트 중에 만들어진 호출에 대해 미리 준비된 답변을 제공하는 것이다!ㅑ***
> 

### **OngoingStubbing 메소드**

- when에 넣는 메소드의 리턴값을 정의해준다.

```java
// 메소드 형식
Mockito.when([Stubbing할 메소드]).thenReturn();

// 실제 예시
Mockito.when(mockList.size()).thenReturn(100);
```

| **메소드명** | **설명** |
| --- | --- |
| thenReturn | 스터빙한 메소드 호출 후 어떤 객체를 리턴할 건지 정의 |
| thenThrow | 스터빙한 메소드 호출 후 어떤 Exception을 Throw할 건지 정의 |
| thenAnswer | 스터빙한 메소드 호출 후 어떤 작업을 할지 custom하게 정의**mockito javadoc을 보면 이 메소드를 굳이 사용하지 말고 thenReturn, thenThrow 메소드 사용을 추천하고 있습니다.** |
| thenCallRealMethod | 실제 메소드 호출 |

### Stubber 메소드

- Ongoing과 다르게 when에 Stubbing할 클래스를 넣고 그 후에 메소드를 호출한다.

```java
// 메서드 형식
{Stubber 메소드}.when({스터빙할 클래스}).{스터빙할 메소드}

// 불가능 (List가 빈객체이므로 0번째 요소가 없다)
when(spy.get(0)).thenReturn("foo");
 
//위와 같은 경우를 doReturn을 사용한다.
doReturn("foo").when(spy).get(0);
```

| **메소드명** | **설명** |
| --- | --- |
| doReturn | 스터빙 메소드 호출 후 어떤 행동을 할 건지 정의 |
| doThrow | 스터빙 메소드 호출 후 어떤 Exception을 throw할  건지 정의 |
| doAnswer | 스터빙 메소드 호출 후 작업을 할지 custom하게 정의 |
| doNothing | 스터빙 메소드 호출 후 어떤 행동도 하지 않게 정의 |
| doCallRealMethod | 실제 메소드 호출 |
</aside>

## @Mock

<aside>
✍️ **NOTE**

> ***@Mock은 mock객체는 가짜 객체이며, 메소드 호출해서 사용하기 위해선 Stubbing을 해야한다!***
> 

```java
@Test
public void NotUseMockAnnotation() {
		// Mock 생성
    List mockList = Mockito.mock(ArrayList.class);
    
		// Mock 사용방법
    mockList.add("one"); // 데이터 추가(실제로는 추가되지 않음)
    Mockito.verify(mockList).add("one"); // 호출 검사
    assertEquals(0, mockList.size()); // 성공!

    Mockito.when(mockList.size()).thenReturn(100); // 해당함수 실행시 100반환
    assertEquals(100, mockList.size()); // 성공!
}
```

- Mockito로 생성된 mock객체는 실제 객체의 동작을 수행하지 않고, 테스트에서 정의된 동작만을 수행한다. (add를 해도 size는 증가하지 않는다.)

```java
@Mock
List<String> mockedList;

@Test
public void whenUseMockAnnotation_thenMockIsInjected() {
    mockedList.add("one");
    Mockito.verify(mockedList).add("one");
    assertEquals(0, mockedList.size());

    Mockito.when(mockedList.size()).thenReturn(100);
    assertEquals(100, mockedList.size());
}
```

</aside>

## @Spy

<aside>
✍️ **NOTE**

> ***@Spy로 만든 Mock객체는 진짜 객체이며, 메소드 실행시 Stubbing을 하지 않으면 기존 객체의 로직을 실행한 값을 리턴한다!***
> 

```java
@Test
public void whenNotUseSpyAnnotation_thenCorrect() {
    List<String> spyList = Mockito.spy(new ArrayList<String>());
    
    spyList.add("one");
    spyList.add("two");

		// 호출 검사
    Mockito.verify(spyList).add("one");
    Mockito.verify(spyList).add("two");

		// 실제로 값이 추가됨!
    assertEquals(2, spyList.size());

		// 100을 반환하도록 설정
    Mockito.doReturn(100).when(spyList).size();
    assertEquals(100, spyList.size());
}

```

```java
@Spy
List<String> spiedList = new ArrayList<String>();

@Test
public void whenUseSpyAnnotation_thenSpyIsInjectedCorrectly() {
    spiedList.add("one");
    spiedList.add("two");

    Mockito.verify(spiedList).add("one");
    Mockito.verify(spiedList).add("two");

    assertEquals(2, spiedList.size());

    Mockito.doReturn(100).when(spiedList).size();
    assertEquals(100, spiedList.size());
}
```

</aside>

## @**InjectMocks**

<aside>
✍️ **NOTE**

> ***@InjectMocks는 DI를 @Mock이나 @Spy로 생성된 mock객체를 자동으로 주입해주는 어노테이션이다!***
> 

```java
public class OrderService {
 
    UserService userService;
    ProductService productService;
 
    OrderService(UserService userService, ProductService productService) {
        this.userService = userService;
        this.productService = productService;
    }
 
    public User getUser() {
        return userService.getUser();
    }
 
    public Product getProduct() {
        return productService.getProduct();
    }
}
```

```java
@ExtendWith(MockitoExtension.class)
public class InjectMocksAnnotation {
 
    @Mock
    UserService userService;
 
    @Spy
    ProductService productService;
 
    @InjectMocks
		// OrderService의 DI인 UserService와 ProductService가 자동으로 추가됨
    OrderService orderService;
 
    @Test
    void testGetUser() {
        assertNull(orderService.getUser());
    }
 
    @Test
    void testGetProduct() {
        Product product = orderService.getProduct();
 
        assertEquals("A001", product.getSerial());
    }
}
```

</aside>

## verify 메소드

<aside>
✍️ **NOTE**

> ***verify메소드를 이용해서 스터빙한 메소드가 실행되었는지, n번 실행되었는지, 실행이 초과되지 않았는지 검증이 가능하다!***
> 

```java
// 메서드 형식
verify(T mock, VerificationMode mode)

@ExtendWith(MockitoExtension.class)
public class VerifyMethod {
 
    @Mock
    UserService userService;
 
    @Test
    void 호출_2번() {
        userService.getUser();
        userService.getUser();
 
        verify(userService, times(2)).getUser();
    }
 
    @Test
    void 호출되지않음() {
        verify(userService, never()).getUser();
    }
 
    @Test
    void 최소호출_1번() {
        userService.getUser();
        verify(userService, atLeastOnce()).getUser();
    }
 
    @Test
    void 최소호출_2번() {
        userService.getUser();
        userService.getUser();
        userService.getUser();
 
        verify(userService, atLeast(2)).getUser();
    }
 
    @Test
    void 최대호출_1번() {
        userService.getUser();
        // userService.getUser(); - 2번 이상 실행하면 fail
 
        verify(userService, atMostOnce()).getUser();
    }
 
    @Test
    void 최대호출_3번() {
        userService.getUser();
        userService.getUser();
        userService.getUser();
        // userService.getUser(); - 6번 이상 실행하면 fail
 
        verify(userService, atMost(3)).getUser();
    }
 
    @Test
    void 호출_지정함수() {
        userService.getUser();
        // userService.getLoginErrNum(); - getUser()가 아닌 다른 메소드 실행 시 fail
 
        verify(userService, only()).getUser();
    }
}
```

| **메소드명** | **설명 (테스트 내에서~)** |
| --- | --- |
| times(n) | 몇 번이 호출됐는지 검증 |
| never | 한 번도 호출되지 않았는지 검증 |
| atLeastOne | 최소 한 번은 호출됐는지 검증 |
| atLeast(n) | 최소 n 번이 호출됐는지 검증 |
| atMostOnce | 최대 한 번이 호출됐는지 검증 |
| atMost(n) | 최대 n 번이 호출됐는지 검증 |
| calls(n) | n번이 호출됐는지 검증 (InOrder랑 같이 사용해야 함) |
| only | 해당 검증 메소드만 실행됐는지 검증 |
| timeout(long mills) | n ms 이상 걸리면 Fail 그리고 바로 검증 종료 |
| after(long mills) | n ms 이상 걸리는지 확인**timeout과 다르게 시간이 지나도 바로 검증 종료가 되지 않는다.** |
| description | 실패한 경우 나올 문구 |
</aside>

## **Argument matchers**

<aside>
✍️ **NOTE**

```java
// any => 어떠한 값이든 타입에 맞으면 상관없다.
when(mockedList.get(anyInt())).thenReturn("int");
when(mockedList.add(anyFloat())).thenReturn(true);
when(mockedList.add(anyString())).thenReturn(true);

System.out.println(mockedList.get(999)); // int
System.out.println(mockedList.add(3.3)); // true
System.out.println(mockedList.add("string")); // true

// eq(Class) => 해당 클래스와 동일한지 확
```

</aside>