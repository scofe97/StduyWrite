# [Spring TDD] 02-2. 스프링 테스트 실습

주제: Spring TDD

- 참고
    
    [[Spring] @WebMvcTest에 의해 느려지는 테스트 속도와 해결 방법(컨트롤러에 대한 단위 테스트 작성하기)](https://mangkyu.tistory.com/244)
    
    [[Spring Security] @withUserDetails 알아보기](https://velog.io/@rmswjdtn/Spring-SecuritywithUserDetails-알아보기)
    
    [Testing Method Security :: Spring Security](https://docs.spring.io/spring-security/reference/servlet/test/method.html)
    
    [@Sql teadown.sql 적용](https://yenjjun187.tistory.com/m/797)
    
    [](https://github.com/HomoEfficio/dev-tips/blob/master/Spring%20Data%20JPA%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%9C%20auto-increment%20%EB%AC%B8%EC%A0%9C.md)
    
    [@DataJpaTest 주의사항](https://velog.io/@jea5158/DataJpaTest-주의사항)
    

# **Spring 단위 테스트**

---

## Controller 테스트 - ***@WebMvcTest***

<aside>
✍️ **NOTE**

> ***@WebMvcText 어노테이션을 사용하면, MockMvc가 자동으로 생성되며, ControllerAdvice나 Filter, Interceptor등 웹 계층에 필요한 요소들을 모두 빈으로 등록해서 환경을 구성한다.***
> 

[[Intellij / 인텔리제이] Spring Test MockMvc의 한글 깨짐](https://milenote.tistory.com/58)

```java
@WebMvcTest(AuthController.class)
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private WebApplicationContext ctx;

    @MockBean
    private AuthService authService;

    @MockBean
    private TokenProvider tokenProvider; // 이거 안하니 에러남;

		// 한글깨짐을 방지하기 위해 추가코드
    @BeforeEach
    void setUp() {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(ctx)
                .addFilters(new CharacterEncodingFilter("UTF-8", true))
                .alwaysDo(print())
                .build();
    }

		// 테스트 코드
}
```

- **@WebMvcTest**는 스프링부트가 제공하는 테스트 환경이므로 기존과 다르게 설정된다.
    - @Mock, @Spy ⇒ @MockBean, @SpyBean
- **@SpringBootTest와 차이점**
    - Web Layer 관련 빈만 로드하기 때문에, 속도가 @SpringBootTest보다 빠르다.
    - 통합테스트에서 테스트가 어려운 작은 단위 테스트들을 @WebMvcTest로 진행할 수 있다.
    - Mock 객체를 사용하기 때문에 실제 환경에서는 다른 오류가 발생할 수 있다.
</aside>

## Controller 테스트 - @WithUserDetails

<aside>
✍️ **NOTE**

> ***@WithUserDetails는 테스트에서 특정 사용자의 인증 상태를 시뮬레이션 하기 위해 사용된다!***
> 

```java
@BeforeEach
public void setUp() {
    userRepository.save(newUser("ssar", "쌀"));
    em.clear();
}

@WithUserDetails(value = "ssar", setupBefore = TestExecutionEvent.TEST_EXECUTION)
@Test
public void findUserAccount_test() throws Exception {
    // given

    // when
    ResultActions resultActions = mvc
                    .perform(get("/api/s/account/login-user"));

    String responseBody = resultActions.andReturn().getResponse().getContentAsString();
    System.out.println("테스트 : " + responseBody);

    // then
    resultActions.andExpect(status().isOk());
}
```

- 메서드에 사용자 이름을 제공하면, 해당 이름에 해당하는 사용자의 UserDetail을 사용한다.
- 실제로 해당 username을 가진 user가 존재해야 하므로 @BeforeEach를 통해서 user를 저장하자
    - @Before이전에 @withUserDetails가 동작하는 문제가 발생한다면 setupBefore 설정을 수정해야한다.
</aside>

## @Sql teadown.sql - PK초기화

<aside>
✍️ **NOTE**

> ***테스트 코드에서 @Transactinal을 사용하면 테스트 수행 후 롤백이 되지만, PK를 auto-increment를 설정한 경우 값이 초기화 되지 않는다!***
> 

![1번째 테스트](%5BSpring%20TDD%5D%2002-2%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%A4%EC%8A%B5/Untitled.png)

1번째 테스트

![2번쨰 테스트(PK가 1이 아닌 3부터 시작하는걸 볼 수 있다)](%5BSpring%20TDD%5D%2002-2%20%EC%8A%A4%ED%94%84%EB%A7%81%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EC%8B%A4%EC%8A%B5/Untitled%201.png)

2번쨰 테스트(PK가 1이 아닌 3부터 시작하는걸 볼 수 있다)

- 이를 해결하기 위해서는 테스트코드에 @Transactional이 아닌 쿼리로 테이블 자체를 초기화시킨다.

```sql
@Sql("classpath:db/teardown.sql")
@ActiveProfiles("test")
@AutoConfigureMockMvc
@SpringBootTest(webEnvironment = WebEnvironment.MOCK)
public class AccountControllerTest {..}
```

```sql
SET REFERENTIAL_INTEGRITY FALSE; -- 모든 제약 조건 비활성화
truncate table transaction_tb;
truncate table account_tb;
truncate table user_tb;
SET REFERENTIAL_INTEGRITY TRUE; -- 모든 제약 조건 활성화
```

- 하지만 위의 쿼리는 테이블을 모두 초기화해서 복구하기 어려울 수 있으므로, 테스트나 개발 목적으로 만 진행하는것을 권장한다.
</aside>

## 서비스 테스트에 대해 생각해보자

<aside>
✍️ **NOTE**

- 
- 

</aside>

## @DataJpaTest

<aside>
✍️ **NOTE**

- 
- 

</aside>

## CORS

<aside>
✍️ **NOTE**

- 
- 

</aside>

## 목차

<aside>
✍️ **NOTE**

- 
- 

</aside>

## 목차

<aside>
✍️ **NOTE**

- 
- 

</aside>