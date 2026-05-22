# [Spring MSA] xx. 헥사고날 아키텍쳐

주제: Spring MSA

- 참고
    
    [만들면서 배우는 클린 아키텍처 정리 - 1 | Dongle](https://dgle.dev/clean-arch-1/)
    

# 아키텍쳐 요소 테스트하기

---

## 테스트 피라미드

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx%20%ED%97%A5%EC%82%AC%EA%B3%A0%EB%82%A0%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled.png)

테스트의 기본 전제는 만드는 비용이 적고, 유지보수하기 쉽고, 빨리 실행되고, 안정적인 작은 크기의 테스트들에 대해 높은 커버리지를 유지해야한다는 것이다.

이 테스트는 단 하나의 ‘단위’가 제대로 동작하는지 확인할 수 있는 단위 테스트들이다.

단위 테스트는 피라미드의 토대에 해당한다.

- 하나의 클래스를 인스턴스화하고 클래스의 인터페이스를 통해 기능들을 테스트한다.
- 테스트 중인 클래스가다른 클래스에 의존한다면 인스턴스화하지 않고 mock으로 대체한다.

통합 테스트는 연결된 여러 유닛을 인스턴스화하고 시작지점이 되는 클래스의 인터페이스로 데이터를 보낸후 유닛들의 네트워크가 기대한 대로 동작하는지 검증한다.

시스템 테스트는 애플리케이션을 구성하는 모든 객체 네트워크를 가동시켜 특정 유스케이스가 잘동작하는지 검증한다.

</aside>

## 단위 테스트로 도메인 엔티티, 유스케이스 테스트

<aside>
✍️ **NOTE**

```java
class AccountTest {

    @Test
    void withdrawalSucceeds() {
        AccountId accountId = new AccountId(1L);

        Account account = defaultAccount()
            .withAccountId(accountId)
            .withBaselineBalance(Money.of(555L))
            .withActivityWindow(new ActivityWindow(
                defaultActivity()
                    .withTargetAccount(accountId)
                    .withMoney(Money.of(999L)).build(),
                defaultActivity()
                    .withTargetAccount(accountId)
                    .withMoney(Money.of(1L)).build()))
            .build();

        boolean success = account.withdraw(Money.of(555L), new AccountId(99L));

        assertThat(success).isTrue();
        assertThat(account.getActivityWindow().getActivities()).hasSize(3);
        assertThat(account.calculateBalance()).isEqualTo(Money.of(1000L));
    }
}
```

테스트가 엔티티에 제대로 녹아 있는지 검증하며, 다른 클래스를 거의 의존하지 않는다.

```java
class SendMoneyServiceTest {

    // 테스트 샘플 생성
    @Test
    void transactionSucceeds() {
			
				// given
        Account sourceAccount = givenSourceAccount();
        Account targetAccount = givenTargetAccount();
        givenWithdrawalWillSucceed(sourceAccount);
        givenDepositWillSucceed(targetAccount);

        Money money = Money.of(500L);
        SendMoneyCommand command = new SendMoneyCommand(
            sourceAccount.getId(),
            targetAccount.getId(),
            money);

				// when
        boolean success = sendMoneyService.sendMoney(command);

        assertThat(success).isTrue();

        AccountId sourceAccountId = sourceAccount.getId();
        AccountId targetAccountId = targetAccount.getId();

        then(accountLock).should().lockAccount(eq(sourceAccountId));
        then(sourceAccount).should().withdraw(eq(money), eq(targetAccountId));
        then(accountLock).should().releaseAccount(eq(sourceAccountId));

        then(accountLock).should().lockAccount(eq(targetAccountId));
        then(targetAccount).should().deposit(eq(money), eq(sourceAccountId));
        then(accountLock).should().releaseAccount(eq(targetAccountId));

        thenAccountsHaveBeenUpdated(sourceAccountId, targetAccountId);
    }

    // 헬퍼 메서드는 생략
}
```

SendMoney의 유스케이스는 출금 계좌의 잔고가 다른 트랜잭션에 의해 변경되지 않도로 ㄱ락을 건다.

</aside>

## 통합 테스트로 웹 어댑터 테스트하기

<aside>
✍️ **NOTE**

```java
@WebMvcTest(controllers = SendMoneyController.class)
class SendMoneyControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private SendMoneyUseCase sendMoneyUseCase;

    @Test
    void testSendMoney() throws Exception {
        mockMvc.perform(
            post("/accounts/send/{sourceAccountId}/{targetAccountId}/{amount}", 
                 41L, 42L, 500)
                .header("Content-Type", "application/json"))
            .andExpect(status().isOk());

        then(sendMoneyUseCase).should()
            .sendMoney(eq(new SendMoneyCommand(
                new AccountId(41L),
                new AccountId(42L),
                Money.of(500L))));
    }

}
```

입력 객체를 만들고나서, HTTP요청을 실제로 보낸뒤, 정확히 호출되는지 확인한다.

</aside>

## 통합 테스트로 영속성 어댑터 테스트하기

<aside>
✍️ **NOTE**

```java
@DataJpaTest
@Import({AccountPersistenceAdapter.class, AccountMapper.class})
class AccountPersistenceAdapterTest {

    @Autowired
    private AccountPersistenceAdapter adapterUnderTest;

    @Autowired
    private ActivityRepository activityRepository;

    // @DataJpaTest 어노테이션이 JPA 관련 구성을 로드하고, 테스트용 데이터베이스를 자동으로 설정합니다.
    // 또한, 테스트 후 데이터를 롤백하여 데이터베이스 상태를 초기화합니다.
    
    @Test
    @Sql("/AccountPersistenceAdapterTest.sql")
    void loadsAccount() {
        // loadsAccount() 테스트 메서드는 AccountPersistenceAdapter 클래스의 loadAccount() 메서드를 테스트합니다.
        // 주어진 SQL 파일에서 테스트 데이터를 데이터베이스에 미리 적재하고, 해당 데이터를 사용하여 테스트를 수행합니다.
        // loadAccount() 메서드가 예상대로 동작하는지 확인합니다.

        Account account = adapterUnderTest.loadAccount(
            new AccountId(1L),
            LocalDateTime.of(2018, 8, 10, 0, 0));

        assertThat(account.getActivityWindow().getActivities()).hasSize(2);
        assertThat(account.calculateBalance()).isEqualTo(Money.of(500));
    }

    @Test
    void updateActivities() {
        // updateActivities() 테스트 메서드는 AccountPersistenceAdapter 클래스의 updateActivities() 메서드를 테스트합니다.
        // 비어있는 활동 목록을 가진 계정(Account)을 생성하고, 해당 계정을 사용하여 updateActivities() 메서드를 호출합니다.
        // updateActivities() 메서드가 예상대로 동작하는지 확인합니다.

        Account account = defaultAccount()
            .withAccountId(new AccountId(1L))
            .withActivityWindow(defaultActivityWindow()
                .withActivities(emptyList()))
            .build();

        adapterUnderTest.updateActivities(account);

        // 활동이 없는 계정을 업데이트하였으므로, 데이터베이스에는 활동이 추가되지 않아야 합니다.
        assertThat(activityRepository.findAll()).hasSize(0);
    }
}
```

@DataJpaTest 애노테이션으로 스프링 데이터 레포지토리들을 포함해서 데이터베이스 접근에 필요한 객체 네트워크를  인스턴스화해야한다고 스프링에 알려준다.

@Import 애노테이션을 추가해서 특정 객체가 이 네트워크에 추가되었다는걸 명확하게 표현할 수 있다.

### 유지보수 가능한 소프트웨어를 만드는데 어떻게 도움이되는가?

육각형 아키텍쳐는 도메인 로직과 바깥으로 향하는 어댑터를 깔끔하게 분리한다.

덕분에 핵심 도메인 로직은 단위 테스트로, 어댑터는 통합 테스트로 처리하는 명확한 테스트 전략을 정의할 수 있다.

입출력 포트는 테스트에서 아주 뚜렷한 모킹 지점이 된다. 각 포트에 대해 모킹할지 실제 구현을 이용할지 선택할 수 있따. 만약 포트가 아주 작고 핵심만 담고 있다면 모킹하는 것이 아주 쉽다.

</aside>

# 경계 간 매핑하기

---

<aside>
✍️ **NOTE**

책의 전반부에서는 웹-애플리케이션-도메인-영속성 계층에 대해 유스케이스를 구현하고 어떤 역할을 하는지 다루었다.

그런데 각 계층의 모델을 매핑하는 것에 대해서는 다루지 않았다. 각 계층에서 같은 모델을 사용하는 것은 과연 옳은 일인가?

- 매핑을 해야한다.
    - 두 계층간에 매핑을 하지 않으면 양 계층에서 같은 모델을 사용하고, 이는 강한 결합으로 이어진다.
- 매핑을 하지않아도 된다.
    - 두 계층 간에 매핑을하면 보일러플레이트 코드가 너무 많아지고, 유스케이스들이 오직 CRUD만 수행하고 계층에 걸쳐 같은 모델을 사용하기 때문에 매핑은 과하다.
</aside>

## 매핑하지 않기 전략

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx%20%ED%97%A5%EC%82%AC%EA%B3%A0%EB%82%A0%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled%201.png)

웹-애플리케이션-도메인-영속성이 모두 동일한 모델을 사용한다.

- 웹 계층과 영속성 계층은 모델에 대해 특별한 요구사항이 존재할 수 있다.
    - ex) 웹 계층의 경우 REST로 모델을 노출시켰다면 모델을 JSON으로 직렬화 하기위한 애너테이션을 붙여야할 수 있다.
    - ex) 영속성의 경우 ORM을 사용한다면 그에 맞는 애노테이션이 필요하다.

위와 같은 문제들은 단일 책임 원칙을 위반한다.

하지만 꼭 매핑하지 않기가 옳지않다는건 아니다. 간단한 CRUD의 개발은 단순한 수정이 있어도 1~2개일 뿐이다. 모든 계층이 정확히 같은 구조의, 같은 정보를 필요로한다면 완벽한 전략이 될 수 있다.

또한 어떤 매핑 전략을 선택하더라도 나중에 언제든 바꿀 수 있따.

</aside>

## 양방향 매핑 전략

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx%20%ED%97%A5%EC%82%AC%EA%B3%A0%EB%82%A0%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled%202.png)

아마 일반적으로 가장 많이 사용하는 전략이다. (DTO와 Entity를 구분하기 떄문)

이 매핑 전략은 웹이나 영속성 관심사로 오염되지 않은 깨끗한 도메인 모델로 이어진다. JSON이나 ORM매핑 애너테이션도 없어도 된다. 단일 책임 원칙을 만족하는 것이다.

물론 양방향 매핑 전략역시 은총알이 아니다. 하지만 많은 프로젝트에서 이런 종류의 매핑은 아주 간단한 CRUD 유스케이스에서조차 준수해야하는 법칙으로 여겨지곤 한다.

</aside>

## 생성자의 힘

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx%20%ED%97%A5%EC%82%AC%EA%B3%A0%EB%82%A0%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled%203.png)

모든 연산별로 별도의 모델을 사용한다.

가장 이상적이지만 그만큼 코드작성이 너무 많아진다.

</aside>

## 단방향 매핑 전략

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx%20%ED%97%A5%EC%82%AC%EA%B3%A0%EB%82%A0%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90/Untitled%204.png)

하나의 계층이 다른 계층으로부터 객체를 받으면 해당 계층에서 이용할 수 있도록 다른 무언가로 매핑한다. (각 계층은 하나의 방향으로만 매핑한다.)

</aside>