# [Spring MSA] 05-5. 유스케이스/어댑터 구현

주제: Spring MSA

- 참고
    
    

# 유스케이스 구현

---

## 도메인 모델 구현

<aside>
✍️ **NOTE**

```java
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Account {

	@Getter private final AccountId id;
	@Getter private final Money baselineBalance;
	@Getter private final ActivityWindow activityWindow;

	// 생성자 1 ( 새로운 계정 생성, DB에서 아직 ID가 생성안됨 )
	public static Account withoutId(
					Money baselineBalance,
					ActivityWindow activityWindow) {
		return new Account(null, baselineBalance, activityWindow);
	}

	// 생성자 2
	public static Account withId(
					AccountId accountId,
					Money baselineBalance,
					ActivityWindow activityWindow) {
		return new Account(accountId, baselineBalance, activityWindow);
	}

	// Optional Getter
	public Optional<AccountId> getId(){
		return Optional.ofNullable(this.id);
	}

	// 환율 계산
	public Money calculateBalance() {
		// ..
	}

	// 출금
	public boolean withdraw(Money money, AccountId targetAccountId) {
		//..
	}

	private boolean mayWithdraw(Money money) {
		// ..
	}

	// 입금
	public boolean deposit(Money money, AccountId sourceAccountId) {
		// ..
	}

	// @Value => 모든 필드를 final + private로 생성 및 Getter 자동생성
	@Value
	public static class AccountId {
		private Long value;
	}

}
```

- 도메인 모델에 비즈니스 및 검증 로직이 들어가는것이 가장 좋다.
</aside>

## 유스케이스(서비스) 구현

<aside>
✍️ **NOTE**

> ***유스케이스는 소프트웨어 동작을 추상화하여, 소프트웨어가 무엇을 하는지 설명하는 역할을 한다!***
> 

![In Port (웹 - 도메인 인터페이스), Out port(도메인 - 영속성 인터페이스)
작성자가 이해한 흐름도이므로 틀린부분이 있을 수 있음
(Inport부분의 이름을 Usecase라고 적기도 하던데 정확한 구분법을 모겠음)](%5BSpring%20MSA%5D%2005-5%20%EC%9C%A0%EC%8A%A4%EC%BC%80%EC%9D%B4%EC%8A%A4%20%EC%96%B4%EB%8C%91%ED%84%B0%20%EA%B5%AC%ED%98%84/Untitled.png)

In Port (웹 - 도메인 인터페이스), Out port(도메인 - 영속성 인터페이스)
작성자가 이해한 흐름도이므로 틀린부분이 있을 수 있음
(Inport부분의 이름을 Usecase라고 적기도 하던데 정확한 구분법을 모겠음)

유스케이스는 다음의 과정을 거친다.

1. **입력을 받는다.**
    - Command, Query
2. **비즈니스 규칙을 검증한다.**
    - 유스케이스는 인커밍 어댑터로부터 입력을 받는다. 입력 유효성 검증에 대한 코드는 다른곳에서 처리하는것이 도메인 로직을 유지하는것에 유리하다.
3. **모델 상태를 조작한다.**
    - 비즈니스 규칙을 충족하면 유스케이스는 입력을 기반으로 모델의 상태를 변경한다.
    - 일반적으로 도메인 객체의 상태를 바꾸고 영속성 어댑터를 통해 구현된 포트로 이 상태를 전달해서 저장될 수 있게한다.
4. **출력을 반환한다.**
    - 아웃고잉 어댑터에서 온 출력값을, 유스케이스를 호출한 어댑터로 반환할 출력 객체로 변환한다.

유스케이스는 도메인 모델의 진입점으로 동작하며, 사용자의 의도만을 표현하는것이 좋다.

```java
@RequiredArgsConstructor
@UseCase
@Transactional
public class SendMoneyService implements SendMoneyUseCase // 인커밍 포트 {

	private final LoadAccountPort loadAccountPort; // 아웃고잉 포트 (도메인 처리후 내보냄)
	private final AccountLock accountLock;
	private final UpdateAccountStatePort updateAccountStatePort; // DB 업데이트

	@Override
	public boolean sendMoney(SendMoneyCommand command) {
		// TODO: 비즈니스 규칙 검증

		// TODO: 모델 상태 조작

		// TODO: 출력 값 반환		
	}
}
```

```java
@Getter
public class SendMoneyCommand extends SelfValidating<SendMoneyCommand> {

    @NotNull
    private final Account.AccountId sourceAccountId;
    @NotNull
    private final Account.AccountId targetAccountId;
    @NotNull
    private final Money money;

    public SendMoneyCommand(
        Account.AccountId sourceAccountId,
        Account.AccountId targetAccountId,
        Money money) {
        this.sourceAccountId = sourceAccountId;
        this.targetAccountId = targetAccountId;
        this.money = money;
        requireGreaterThan(money, 0);
        this.validateSelf();
    }
}
```

![Untitled](%5BSpring%20MSA%5D%2005-5%20%EC%9C%A0%EC%8A%A4%EC%BC%80%EC%9D%B4%EC%8A%A4%20%EC%96%B4%EB%8C%91%ED%84%B0%20%EA%B5%AC%ED%98%84/Untitled%201.png)

</aside>

# 웹 어댑터 구현하기

---

<aside>
💡 **NOTE**

> ***아키텍쳐 외부 세계와의 커뮤니케이션은 모두 어댑터를 이뤄진다!***
> 

![Controller는 DIP가 구현된건가? 책에서는 구현되었다고 한다.](%5BSpring%20MSA%5D%2005-5%20%EC%9C%A0%EC%8A%A4%EC%BC%80%EC%9D%B4%EC%8A%A4%20%EC%96%B4%EB%8C%91%ED%84%B0%20%EA%B5%AC%ED%98%84/Untitled%202.png)

Controller는 DIP가 구현된건가? 책에서는 구현되었다고 한다.

```java
@WebAdapter
@RestController
@RequiredArgsConstructor
class SendMoneyController {

	// UseCase 사용
	private final SendMoneyUseCase sendMoneyUseCase;

	@PostMapping(path = // ..)
	void sendMoney( // ..);
		sendMoneyUseCase.sendMoney(command);
	}

}
```

**웹 어댑터는 다음과 같은 작업을 수행한다.**

1. http request를 Java객체로 매핑
2. 권한 검사
3. 입력 유효성 검증
4. 입력 값을 UseCase용 입력 모델도 매핑
    - 유스케이스 입력모델은 유스케이스에서의 맥락에서 유효한 입력만 허용해야 한다.
5. 유스케이스 호출
6. 유스케이스 결과를 http로 매핑
7. http response를 반환

웹 어댑터의 경우 단일 컨트롤러에 모든 요청을 넣는것은 좋지 않다. 가급적이면 별도의 패키지안에 별도의 컨트롤러를 만드는 방식을 선호하자. (클래스명은 최대한 유스케이스를 반영해서 지어야한다.)

</aside>

# 영속성 어댑터 구현하기

---

<aside>
💡 **NOTE**

> ***데이터베이스가 아닌 도메인을 기준으로 설계하기 위해서는 DIP(의존성 역전)이 필요하다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-5%20%EC%9C%A0%EC%8A%A4%EC%BC%80%EC%9D%B4%EC%8A%A4%20%EC%96%B4%EB%8C%91%ED%84%B0%20%EA%B5%AC%ED%98%84/Untitled%203.png)

```java
@RequiredArgsConstructor
@PersistenceAdapter
class AccountPersistenceAdapter implements LoadAccountPort,UpdateAccountStatePort {

	// Repository 사용
	private final SpringDataAccountRepository accountRepository;
	private final ActivityRepository activityRepository;

	// 매핑
	private final AccountMapper accountMapper;

	@Override
	public Account loadAccount() {
		// ...
	}

	private Long orZero(Long value){
		return value == null ? 0L : value;
	}

	@Override
	public void updateActivities(Account account) {
		// ...
	}

}
```

서비스에서 영속성 작업을 수행하기 위해 output port를 사용하고, 영속성 어댑터는 output port 인터페이스를 구현한다.

**영속성 어댑터는 다음과 같은 작업을 수행한다.**

1. 입력값을 받는다.
2. 입력값을 데이터베이스용으로 매핑한 후 데이터베이스로 보내서 처리한다.
3. 데이터베이스 출력값을 애플리케이션 형식으로 매핑하여 반환한다.

### 유지보수 가능한 소프트웨어에 도움이 되는가?

도메인 코드에 플러그인처럼 동작하는 영속성 어댑터를 만들면 도메인 코드가 영속성과 관련된 것들로부터 분리되어 풍부한 도메인 모델을 만들 수 있다.

좁은 포트 인터페이스를 사용하면 포트마다 다른 방식으로 구현할 수 있는 유연함이 생긴다.

</aside>