# [Spring MSA] 05-2. 계층형 아키텍쳐의 문제점, DIP

주제: Spring MSA

- 참고
    
    

# 계층형 아키텍쳐의 문제

---

<aside>
💡 **NOTE**

> ***계층형 아키텍쳐는 시스템을 여러 계층으로 구분하여 설계하는 방식이다!***
> 

![일반적인 계층형 도메인 구조(표현 → 응용 → 도메인 → 인프라 스트럭쳐)](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled.png)

일반적인 계층형 도메인 구조(표현 → 응용 → 도메인 → 인프라 스트럭쳐)

![일반적인 3계층 구조](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%201.png)

일반적인 3계층 구조

잘 만들어진 계층형 아키텍쳐는 독립적으로 도메인 로직이 가능하며, 변화하는 요구사항과 외부 요인에 빠르게 적응하게 해준다.

하지만 계층형 아키텍쳐는 **‘나쁜 습관’**이 스며들기 쉬워지며 이러한 습관들이 이후 유지보수를 어렵게 만든다. 그러면 이 ‘나쁜 습관’이란 도대체 무엇인가?

</aside>

## 계층형 아키텍쳐는 데이터베이스 주도 설계를 유도한다!

<aside>
✍️ **NOTE**

> ***계층형 아키텍쳐 모든것이 영속성 계층을 토대로 만들어진다!***
> 

일반적인 계층형 아키텍쳐는 **상위 계층에서 하위 계층으로의 의존만 존재**하고 하위 계층은 상위 계층에 의존하지 않는다. 

- Web → Domain → Persistence(영속성)의 의존관계를 가지며 모든 것이 영속성 계층을 토대로 만들어지면서 문제를 초래한다.

**우리가 만드는 애플리케이션의 목적은 무엇인가?** 

- 일반적으로 비즈니스를 처리하는 규칙이나 정책을 반영한 모델을 만든다
- 사용자가 이러한 규칙과 정책을 더욱 편리하게 활용할 수 있게 한다.
- 즉, **우리는 상태(state, DB)가 아닌 행동(behavior, 도메인로직)을 중심으로 모델링해야 한다!**

그러면 우리는 왜 **‘도메인 로직’이 아닌 ‘데이터베이스’를 토대로 아키텍쳐를 만들고 있는가?**

책의 저자가 말하는 가장 큰 원인은 ‘ORM 프레임워크(JPA)’의 사용이다. JPA의 사용이 안좋다는 것은 아니지만 ORM과 계층형 아키텍쳐를 결합하면 **비즈니스 규칙을 영속성 관점과 섞고 싶은 유혹을 받는다.**

![@Entity코드에 도메인 로직이 들어가면, 도메인-영속성 계층간 강한 결합이 생긴다!](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%202.png)

@Entity코드에 도메인 로직이 들어가면, 도메인-영속성 계층간 강한 결합이 생긴다!

- 이러한 게층간의 결합은 이후 로딩정책, 트랜잭션, 캐시 관련 작업을 영속성 계층에서 구현하게 된다.

![계층형 아키텍쳐를 사용할때 계층을 건너뛰는 경우](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%203.png)

계층형 아키텍쳐를 사용할때 계층을 건너뛰는 경우

![Domain 계층에서 InfraStrcutre구조에 강하게 결합되는 경우](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%204.png)

Domain 계층에서 InfraStrcutre구조에 강하게 결합되는 경우

```java
// 인프라 스트럭쳐 코드 (예시코드 - 기능생각 X)
public class DroolsRuleEngine {
		// ..
    public void evaluate(String sessionName, List<?> facts) {
        // 무언가의 로직이 있다고만 생각해라
    }
}

// 응용 영역 코드
public class CalculateDiscountService {
    private DroolsRuleEngine ruleEngine;

    public CalculateDiscountService() {
        ruleEngine = new DroolsRuleEngine();
    }

    public Money calculateDiscount(List<OrderLine> orderLines, String customerId) {
        Customer customer = findCustomer(customerId);

				// Drools에 특화된 코드
        MutableMoney money = new MutableMoney(0);
        List<?> facts = Arrays.asList(customer, money);
        facts.addAll(orderLines);

				// discountCalculation 문자열은 Drools의 세션 이름을 의미한다?
				// 예시 코드로 보여주는건 DroolsRuleEngine를 직접 구현받는다는것이 문제인듯
        ruleEngine.evaluate("discountCalculation", facts);
        return money.toImmutableMoney();
    }

    // ...
}
```

- Web계층에서 간혹 단순 조회를 하는 경우 Domain을 거치지 않고 바로 영속성 계층의 Entity에서 데이터를 조회하는 경우가 있다.
- 이렇게 된다면 영속성의 변화가 모두에게 영향을 미치고, 계층간의 분리가 제대로 이루어지지 않아 테스트하기가 어려워진다.
- 또한 Domain계층에서 Persistence계층을 직접적으로 의존하는 경우도 Persistence의 로직에 강하게 의존하므로 테스트가 어려워진다.

**또한 데이터베이스를 토대로 하는 경우 동시작업이 어려워진다!**

- 모든것이 영속성 계층을 토대로 만들어지므로, 영속성 → 도메인 → 웹 계층의 순서로 개발되어야 한다.
- 인터페이스를 먼저 정의한다고 해도, 데이터베이스 주도 설계는 영속성 로직이 도메인 로직과 뒤섞여서 개별적으로 작업할 수 없게 만든다.

정리하자면 계층형 아키텍쳐가 무조건 나쁘다는건 아니다. 규칙을 잘 적용하면 유지보수하기 매우 쉽다.

</aside>

# 의존성 역전(DIP)

---

<aside>
💡 **NOTE**

> *앞서서 계층형 아키텍쳐에 대한 불만을 늘어놓았으니 이번에는 대안에 대해서 이야기한다. 대표적인 해결책인 **SOLID에서의 SPR과 DIP로 해결할 수 있다.***
> 
</aside>

## 단일 책임 원칙(SPR)

<aside>
✍️ **NOTE**

> ***하나의 컴포넌트는 오직 하나의 일만 해야하며, 변경하는 이유도 오직 하나여야 한다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%205.png)

- 하지만 변경할 이유라는 것은 컴포넌트 간의 의존성을 통해 너무나도 쉽게 전파된다.
- 대표적인 Spring만 하더라도 @Bean을 통해서 여러 컴포넌트들을 가져와서 사용하고 있다.
</aside>

## 의존성 역전(DIP)

<aside>
✍️ **NOTE**

> *DIP는 **시스템의 고수준 모듈이 저수준 모듈에 직접적으로 의존하는 것을 피하고**, 대신 **둘 모두가 추상화에 의존하도록 설계**해야 한다는 원칙*
> 

![직접적인 의존하면 결국 서로 영향을 받게된다.](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%206.png)

직접적인 의존하면 결국 서로 영향을 받게된다.

일반적인 계층형 아키텍쳐에서는 항상 하나의 방향으로 계층간 의존 가리키고 있다. 이는 단일 책임 원칙을 고수준에서 적용할 때 상위 계층들이 하위 계층들에 비해 변경할 이유가 더 많아진다는 의미이다.

- **웹 → 도메인 → 영속성**의 구조에서 영속성 계층에 대한 도메인 계층의 의존성 때문에, 변경마다 잠재적으로 도메인 계층도 수정해야 한다.
- 하지만 영속성 코드가 변경된다고 해서 도메인 코드까지 바꾸고 싶지는 않다. (어떻게 의존성을 제거할 수 있는가? ⇒ ***DIP가 이를 해결해준다!***

도메인 코드와 영속성 코드간의 의존성을 역전시켜서 영속성 코드가 도메인 코드를 ‘변경할 이유’의 개수를 줄여보자. 

![DIP 적용 (Persistence → Domain) 방향으로 의존성이 역전되었다!
***코드상의 어떤 의존성이든 그 방향을 바꿀 수(역전시킬 수) 있다!***](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%207.png)

DIP 적용 (Persistence → Domain) 방향으로 의존성이 역전되었다!
***코드상의 어떤 의존성이든 그 방향을 바꿀 수(역전시킬 수) 있다!***

</aside>

## DIP 주의사항 및 아키텍쳐

<aside>
✍️ **NOTE**

> ***DIP를 잘못 생각하면 단순히 인터페이스와 구현 클래스를 분리하는 정도로 받아들 수 있다.***
> 

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%208.png)

**DIP의 핵심은 고수준 모듈이 저수준 모듈에 의존하지 않도록 하는 것입니다**. 그러나 DIP를 적용했음에도 불구하고, 저수준 모듈에서 인터페이스를 추출하는 경우가 있습니다. 이는 잘못된 구조이며, 이 구조에서 도메인 영역은 여전히 인프라스트럭처 영역에 의존하고 있습니다.

DIP를 적용할 때, 하위 기능을 추상화한 인터페이스는 고수준 모듈 관점에서 도출해야 합니다.

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%209.png)

- CalculateDiscountService의 입장에서 봤을때 금액 할인을 구하기 위해 RuleEngine을 사용하는지 다른 방법을 사용하는지는 중요하지 않다.
- 단지 규칙에 따라 **할인 금액을 계산한다는 것이 가장 중요하다!**

인프라스트럭쳐 영역은 구현 기술을 다루는 저수준 모듈이고, 응용/도메인 영역은 고수준 모듈에 속한다.

![앞서 배운 아키텍쳐와 반대되는 의존관계를 가지게 된다.](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2010.png)

앞서 배운 아키텍쳐와 반대되는 의존관계를 가지게 된다.

- 아키텍쳐에 DIP를 적용하게 되면 **인프라스트럭쳐 영역이 응용/도메인 영역에 의존하는 구조(의존역전)가된다.**

인프라스트럭쳐에 위치한 클래스가 도메인이나 응용 영역에 정의한 인터페이스를 상속받아 구현하는 구조가 되므로 도메인과 응용 영역에 대한 영향을 주지않거나 최소화하면서 구현기술을 변경하는것이 가능하다.

![사실 일반적인 인프라스트럭쳐의 코드인 JPA Repository는 인터페이스로 제공되므로 실제로 겪을 일은 아닌거같다.](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2011.png)

사실 일반적인 인프라스트럭쳐의 코드인 JPA Repository는 인터페이스로 제공되므로 실제로 겪을 일은 아닌거같다.

![DIP를 이용해서 다른 구현체로 변경하는 예시](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2012.png)

DIP를 이용해서 다른 구현체로 변경하는 예시

- DIP를 통해 응용, 도메인, 인프라스트럭쳐의 영역을 깔끔하게 분리할 수 있다!
- DIP는 항상 적용할 필요는 없지만 이점을 얻는 수준에서 적용 범위를 검토해보자
</aside>

## 클린 아키텍쳐

<aside>
✍️ **NOTE**

> ***클린 아키텍쳐에서의 의존성 규칙은 계층 간의 모든 의존성이 안쪽으로 향해야 한다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2013.png)

아키텍쳐의 코어(core)에는 주변 유스케이스에 접근하는 도메인 Entity가 존재한다. 

비즈니스 규칙은 프레임워크, DB, UI 기술, 그 밖의 외부 애플리케이션이나 인터페이스로부터 독립적일 수 있으며, **도메인 코드가 바깥으로 향하는 어떠한 의존성도 없어야 함을 의미한다.**

- 대신 DIP의 도움으로 만든 의존성이 도메인 코드를 향하고 있다!
- 이러한 클린아키텍쳐는 비즈니스 규칙의 테스트를 용이하게 해준다.

각 계층이 외부 계층과 철저하게 분리되어야 하므로, 애플리케이션의 엔티티에 대한 모델을 각 계층에서 유지보수 해야한다.

</aside>

## 도메인 주도 모듈 구성

<aside>
✍️ **NOTE**

![catalog, order, member는 애그리거트로 보면된다.](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2014.png)

catalog, order, member는 애그리거트로 보면된다.

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2015.png)

- application - Controller
- domain - 엔티티, Vo, 애그리거트, 예외  …
</aside>

## 헥사고날 아키텍쳐(육각형 아키텍쳐)

<aside>
✍️ **NOTE**

> ***육각형 외부로 향하는 의존성이 없기 때문에, 클린 아키텍쳐의 의존성이 그대로 이루어진 아키텍쳐이다!***
> 

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2016.png)

![Controller는 SendMoneyUseCase를 통해 Application에 접근
Persistence는 LoadAccountPort를 통해 Application에 접근](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2017.png)

Controller는 SendMoneyUseCase를 통해 Application에 접근
Persistence는 LoadAccountPort를 통해 Application에 접근

![각 계층이 완벽히 분리되고, Adapter와 Port로 통해 통신하는 모습](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2018.png)

각 계층이 완벽히 분리되고, Adapter와 Port로 통해 통신하는 모습

**도메인 엔티티와 상호작용하는 유스케이스가 존재한다.**

- 육각형 외부로 향하는 의존성이 없기 때문에, 클린 아키텍쳐의 의존성이 그대로 이루어진다.
- 가장 핵심은 계층간의 격리라고 생각하면 된다.

### 포트와 어댑터

포트와 어댑터는 도메인으로부터 들어오는 것(인커밍)과 나가는 것(아웃고잉)으로 나눌 수 있다.

- 포트
    - 인터페이스이며, 로직에 대한 입구와 출구를 정의한다.
    - 애플리케이션 외부 세계 사이의 계약 정의
- 어댑터
    - 구현(실제 클래스), 포트를 통해 들어오고 나가는 데이터를 변환한다.
    - 애플리케이션의 핵심 로직과 외부 세계 사이의 통신을 담당하는 모듈
- 인커밍/아웃고잉
    - "요청이 어디에서 오는가?"와 "요청이 어디로 가는가?”로 구분하면 좋다.
    - 인커밍 ⇒ 애플리케이션으로 들어오는
    - 아웃고잉 ⇒ 애플리케이션에서 나가

- **인커밍 포트 ⇒ ex) UseCase**
    
    ```java
    public interface MoneyTransferUseCase {
        void transferMoney(TransferMoneyCommand command);
    }
    ```
    
- **인커밍 어댑터 ⇒ ex) Web/App**
    
    ```java
    @RestController
    public class MoneyTransferController {
    
        private final MoneyTransferUseCase moneyTransferUseCase;
    
        public MoneyTransferController(MoneyTransferUseCase moneyTransferUseCase) {
            this.moneyTransferUseCase = moneyTransferUseCase;
        }
    
        @PostMapping("/transfer")
        public ResponseEntity<Void> transferMoney(@RequestBody TransferMoneyCommand command) {
            moneyTransferUseCase.transferMoney(command);
            return ResponseEntity.ok().build();
        }
    }
    ```
    
- **아웃고잉 포트 ⇒ ex) Repository**
    
    ```java
    public interface AccountRepository {
        Account findAccountById(AccountId accountId);
        void updateAccount(Account account);
    }
    ```
    
- **아웃고잉 어댑터 ⇒ ex) MySQL / AWS S3**
    
    ```java
    public class AccountRepositoryAdapter implements AccountRepository {
    
        private final JpaAccountRepository jpaAccountRepository;
    
        public AccountRepositoryAdapter(JpaAccountRepository jpaAccountRepository) {
            this.jpaAccountRepository = jpaAccountRepository;
        }
    
        @Override
        public Account findAccountById(AccountId accountId) {
            return jpaAccountRepository.findById(accountId)
                    .orElseThrow(() -> new AccountNotFoundException(accountId));
        }
    
        @Override
        public void updateAccount(Account account) {
            jpaAccountRepository.save(account);
        }
    }
    ```
    
</aside>

## 헥사고날 아키텍쳐 패키지 구성

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%2005-2%20%EA%B3%84%EC%B8%B5%ED%98%95%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B3%90%EC%9D%98%20%EB%AC%B8%EC%A0%9C%EC%A0%90,%20DIP/Untitled%2019.png)

- **domain 패키지**
    - 도메인 모델(Entity)가 속한다.
- **application 패키지**
    - 서비스 계층을 포함한다.
    - 서비스는 port interface를 구현해서 사용한다.
- adapter 패키지
    - application 계층의 인커핑/아웃커밍 포트에 대한 어댑터를 포함한다.

adapter 패키지의 모든 클래스들은 application 패키지 내에 있는 port 인터페이스를 통하지 않고는 바깥에서 호출되지 않기에 **package-private 접근 수준으로 둬도 된다.** 

하지만 application, domain 패키지 내의 일부 클래스는 public으로 지정해야 한다.

- 의도적으로 어댑터에서 접근 가능해야 하는 포트들은 public이어야 함
- 도메인 클래스 역시 public
- 서비스는 인커핑 포트 인터페이스 뒤에 숨겨지기 때문에 public일 필요가 없다.
</aside>