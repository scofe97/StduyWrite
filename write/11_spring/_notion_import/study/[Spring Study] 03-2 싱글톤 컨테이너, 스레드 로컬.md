# [Spring Study] 03-2. 싱글톤 컨테이너, 스레드 로컬

주제: Spring Study
연관 노트: [Java Study] 01-1.  정적 팩토리 메소드, 빌더 패턴, 싱글톤 (https://www.notion.so/Java-Study-01-1-924ae61e51324d33a70c015ace6655b7?pvs=21), [Java Study] 04-1.  불변 객체, Record (https://www.notion.so/Java-Study-04-1-Record-e7e8ed7545994d8392907eb83543078f?pvs=21)

- 참고
    
    [쓰레드 로컬](https://velog.io/@coconenne/쓰레드-로컬)
    
    [10. 싱글톤 컨테이너와 싱글톤 방식의 주의점](https://gdlovehush.tistory.com/470?category=993329)
    
    [11. @Configuration과 싱글톤](https://gdlovehush.tistory.com/471?category=993329)
    

# 웹 애플리케이션과 싱글톤

---

<aside>
💡 **NOTE**

> *웹 애플리케이션은 수 많은 사용자의 요청을 처리해야 합니다. 만약 요청이 들어올때마다 객채를 새로 만들게 되면 **메모리 낭비가 너무 심하므로, 1개를 생성하고 공유하도록 설계 해야하는데 이것을 싱글톤 패턴** 이라고 부릅니다.*
> 

싱글톤을 구현하는 기본적인 방법은 생성자를 private으로 선언하고, 1번만 생성한후, 정적 팩토리 메서드로 동일한 인스턴스를 반환하는것입니다.

```java
public class SingletonService {

    // 1. 자기 자신을 내부에 private 으로 선언. final 이니까 딱 1번만 생성하고, 2번 생성 불가하게 만든다.
    private static final SingletonService instance = new SingletonService();

    // 2. 인스턴스 조회는 public 으로 열어둠
    public static SingletonService getInstance(){
        return instance;
    }

    // 3. 생성자를 private 으로 생성. 외부에서 new 키워드로 객체 생성 불가하도록 막음
    private SingletonService(){}

    public void logic(){
        System.out.println("싱글톤 객체 로직 호출");
    }
}
```

![싱글톤 미사용 - 요청마다 객체생성](%5BSpring%20Study%5D%2003-2%20%EC%8B%B1%EA%B8%80%ED%86%A4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EB%A1%9C%EC%BB%AC/Untitled.png)

싱글톤 미사용 - 요청마다 객체생성

![싱글톤 사용 - 동일한 객체 사용](%5BSpring%20Study%5D%2003-2%20%EC%8B%B1%EA%B8%80%ED%86%A4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EB%A1%9C%EC%BB%AC/Untitled%201.png)

싱글톤 사용 - 동일한 객체 사용

- 스프링 컨테이너는 `@Bean` 어노테이션만으로 기존의 싱글톤 패턴에 필요한 코드나, 어려움들을 쉽게 극복할 수 있습니다.
- 스프링 빈의 등록 방식은 기본으로는 싱글톤이지만, 요청마다 새로운 객체를 생성해서 반환하는 것도 가능합니다. (빈 스코프 참조)
</aside>

## **싱글톤 방식의 주의점** ⭐

<aside>
✍️ **NOTE**

> *싱글톤 방식의 객체를 사용할 때는 무상태로 설계해야 합니다. 이는 웹 애플리케이션 서버는 보통 멀티 스레드로 동작하며, 멀티 스레드의 경우 코드, 데이터 영역을 공유해 동시성 문제가 발생할 수 있기 때문입니다.*
> 

만약 싱글톤 객체에 대해서 두 스레드가 모두 객체를 읽기만 하면 상관없지만, 각각의 스레드가 쓰기를 하는경우 동기화 문제가 발생할 수 있습니다.

```java
@Slf4j
public class FieldService {

    private String nameStore;

    public String logic(String name) {
        log.info("저장 name={} -> nameStore={}", name, nameStore);
        nameStore = name;
        
        sleep(1000); // 1초뒤에 저장값을 반환해준다.
        
        log.info("조회 nameStore={}", nameStore);
        return nameStore;
    }
}
```

```java
Thread threadA = new Thread(userA);
threadA.setName("thread-A");

Thread threadB = new Thread(userB);
threadB.setName("thread-B");

// A가 완전히 실행될떄 까지 대기
threadA.start();
sleep(2000);

// A가 끝난뒤 B시작
threadB.start();
sleep(3000);
```

### 동시성 문제 O (작업시간이 겹친다)

```java
Thread threadA = new Thread(userA);
threadA.setName("thread-A");

Thread threadB = new Thread(userB);
threadB.setName("thread-B");

threadA.start();
sleep(100); // 동시성 문제 발생 O
threadB.start();
sleep(3000);
```

![스레드A가 저장값을 받아내기전에, 스레드B의 값으로 덮어 씌워짐](%5BSpring%20Study%5D%2003-2%20%EC%8B%B1%EA%B8%80%ED%86%A4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EB%A1%9C%EC%BB%AC/Group_26_(2).png)

스레드A가 저장값을 받아내기전에, 스레드B의 값으로 덮어 씌워짐

![이제 스레드A도 스레드B가 기록한 내용을 읽어버린다!](%5BSpring%20Study%5D%2003-2%20%EC%8B%B1%EA%B8%80%ED%86%A4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EB%A1%9C%EC%BB%AC/Untitled%202.png)

이제 스레드A도 스레드B가 기록한 내용을 읽어버린다!

</aside>

## **스레드 로컬**

<aside>
✍️ **NOTE**

> *스레드 로컬은 각 스레드에 데이터를 별도로 저장하는 메커니즘을 제공합니다. 이를 사용하면 스레드는 독립적인 데이터를 가질 수 있어 동시성 문제를 해결할 수 있습니다.*
> 

```java
@Slf4j
public class ThreadLocalService {

		// 스레드 로컬 사용
    private ThreadLocal<String> nameStore = new ThreadLocal<>();

    public String logic(String name) {
        log.info("저장 name={} -> nameStore={}", name, nameStore.get());
        nameStore.set(name);
        
        sleep(1000); // 1초 동안 지연
        
        log.info("조회 nameStore={}", nameStore.get());
        return nameStore.get();
    }
}
```

![Untitled](%5BSpring%20Study%5D%2003-2%20%EC%8B%B1%EA%B8%80%ED%86%A4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EB%A1%9C%EC%BB%AC/Untitled%203.png)

- 필드를 스레드 로컬 객체로 설정하면 동시성 문제를 해결할 수 있습니다 이는 객체의 필드를 여러 스레드가 공유하는 것이 동시성 문제의 원인이기 때문입니다.
- 스레드 로컬을 사용한 후에는 `remove()`를 호출하여 스레드 로컬을 초기화하고 반환해야 합니다. 그렇지 않으면 다음 요청에서 이전 요청의 데이터에 접근할 수 있습니다. (메모리 누수)
</aside>

## **스프링 컨테이너의 싱글톤 보장(CGLIB)**

<aside>
✍️ **NOTE**

> *스프링에 컨테이너는 싱글톤으로 빈을 관리합니다. 하지만 아래의 코드를 보면 메소드가 여러번 호출되면서 새로운 인스턴스를 반환하고 있습니다.*
> 

```java
@Configuration
public class AppConfig {
		// 호출 1
    @Bean
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

		// 호출 2
    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }

		// 새로운 객체 반환 메서드
    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
    ...
}
```

- 메서드의 반환값은 `new MemoryMemberRepository();` 인데 메서드가 메서드가 여러번 쓰이면 여러개의 객체가 생성되는것처럼 생각할 수 있다.

스프링은 `@Configuration`과 `CGLIB`라는 바이트코드 조작 라이브러리를 사용하여 이 문제를 해결합니다. `@Configuration`이 붙은 클래스는 스프링에 의해 특별한 `CGLIB` 프록시 클래스로 변환됩니다. 이 프록시 클래스는 빈을 생성하는 메소드를 오버라이딩하여, 빈이 이미 존재할 경우에는 기존의 빈을 반환하도록 합니다.

```java
@Configuration
public class AppConfig {
    @Bean
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

    @Bean
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }

    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }
}
```

```java
public class AppConfigCglibProxy extends AppConfig {
    
    // 
    private MemberRepository memberRepository;

    @Override
    public MemberService memberService() {
        return new MemberServiceImpl(memberRepository());
    }

    @Override
    public OrderService orderService() {
        return new OrderServiceImpl(memberRepository(), discountPolicy());
    }

		// 이미 존재하는 경우, 기존값 쓰도록 변환
    @Override
    public MemberRepository memberRepository() {
        if (this.memberRepository == null) {
            this.memberRepository = super.memberRepository();
        }
        return this.memberRepository;
    }
}
```

![CGLIB의 개념은 AOP에서 자세히 다룹니다.](%5BSpring%20Study%5D%2003-2%20%EC%8B%B1%EA%B8%80%ED%86%A4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88,%20%EC%8A%A4%EB%A0%88%EB%93%9C%20%EB%A1%9C%EC%BB%AC/Untitled%204.png)

CGLIB의 개념은 AOP에서 자세히 다룹니다.

</aside>