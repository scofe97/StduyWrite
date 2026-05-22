# [Spring Study] 03-4. 빈 생명주기(@Post, @Destroy) /스코프

주제: Spring Study
연관 노트: [Spring Study] 08-5. 빈 후처리기 (https://www.notion.so/Spring-Study-08-5-df4311d322a54b2b8988b4af946377cd?pvs=21)

- 참고
    
    [19. 빈 생명주기 콜백](https://gdlovehush.tistory.com/480?category=993329)
    
    [20. 스프링의 빈 생명주기 콜백 지원방법 3가지](https://gdlovehush.tistory.com/481?category=993329)
    
    [](https://velog.io/@rmswjdtn/spring-%EB%B9%88%EC%8A%A4%EC%BD%94%ED%94%84-%ED%94%84%EB%A1%9C%ED%86%A0%ED%83%80%EC%9E%85-%EC%8A%A4%EC%BD%94%ED%94%84-%EC%8A%A4%ED%94%84%EB%A7%81-%EA%B8%B0%EB%B3%B8%ED%8E%B8-by-%EA%B9%80%EC%98%81%ED%95%9C)
    
    [[spring] 빈스코프 : 웹스코프 (스프링 기본편 by 김영한)](https://velog.io/@rmswjdtn/spring-빈스코프-웹스코프-스프링-기본편-by-김영한)
    

# 빈 생명주기 콜백

---

<aside>
💡 **NOTE**

> *스프링 프레임워크는 빈의 시작과 종료 시점에 필요한 리소스를 효율적으로 관리할 수 있도록 여러 방법을 제공해줍니다.*
> 

데이터베이스 커넥션 풀이나 네트워크 소켓처럼 시작 시점과 종료 시점에 작업이 필요한 작업이 있다고 가정해봅시다.

```java
public class NetworkClient {
    private String url;
    
    public NetworkClient() {
        System.out.println("생성자 호출, url = " + url);
        
        // 문제코드(url초기화 이전에 사용하게됨)
        connect();
        call("초기화 연결 메시지");
    }
    
    public void setUrl(String url) {
        this.url = url;
    }
    
    //서비스 시작시 호출
    public void connect() {
        System.out.println("connect: " + url);
    }
    
    public void call(String message) {
        System.out.println("call: " + url + " message = " + message);
    }
    
    //서비스 종료시 호출
    public void disconnect() {
        System.out.println("close: " + url);
    }
}
```

```java
class NetworkClientTest {

    @Test
    public void lifeCycleTest() {
        ConfigurableApplicationContext ac = new
                AnnotationConfigApplicationContext(LifeCycleConfig.class);
                
        // 객체 검색
        NetworkClient client = ac.getBean(NetworkClient.class);
        
        ac.close(); //스프링 컨테이너를 종료, ConfigurableApplicationContext 필요
    }
    
    @Configuration
    static class LifeCycleConfig {
        @Bean
        public NetworkClient networkClient() {
            NetworkClient networkClient = new NetworkClient();
            
            networkClient.setUrl("http://hello-spring.dev"); // 생성이후 설정
            return networkClient;
        }
    }
}
```

![Untitled](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled.png)

- 생성자 호출시 `url = null`이 호출되는 이유는, 객체 생성 시점에는 `url`이 입력되지 않고, 생성 완료후 setter를 통해 입력되기 때문입니다. 이러한 방식은 생성자에서 url없이 `connect()`와 `call()`을 호출하게되어 큰 문제가 있습니다.
- 스프링 빈은 의존관계 주입이 이루어진 이후에 사용될 준비가 완료됩니다. 만약 빈의 시작 시점에 필요한 초기화 작업이 있다면 이러한 DI가 모두 끝난뒤에 실행해야 합니다.
</aside>

## 스프링 빈의 생명주기

<aside>
✍️ **NOTE**

> *네트워크의 URL을 초기화하려면 의존성 주입이 완료된 후에 초기화 콜백을 사용해야 합니다. 스프링에서는 이러한 초기화/소멸 콜백을 지원하는 여러 방법이 있습니다.*
> 

![생명주기 흐름](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%201.png)

생명주기 흐름

- **초기화 콜백**: 빈이 생성되고, 의존주입이 완료된 후 호출되는 메소드
- **소멸전 콜백**: 빈이 소멸되기 직전에 호출된다.

❗**참고:** 객체의 생성과 초기화는 분리하는것이 좋습니다. 

- **생성자**: 필수 정보(파라미터)를 받고, 메모리를 할당해 객체를 생성한다.
- **초기화**: 생성된 값을 활용해서 외부 커넥션을 연결한다.

### 스프링 초기화/소멸 콜백

스프링 `@Bean`에 속성으로 초기화, 소멸 메서드를 지정할 수 있습니다.

```java
public class NetworkClient{

	  // 생성자 메서드
    public NetworkClient() {
		    System.out.println("생성자 호출, url = " + url);
		    // connect(), call() 메서드를 init로 옮김
    }

		// 초기화 메서드
    public void init() {
        System.out.println("NetworkClient.init");
        connect();
        call("초기화 연결 메세지");
    }

		// 종료 메서드
    public void close() {
        System.out.println("NetworkClient.close");
        disconnect();
    }
}
```

```java
@Configuration
static class LifeCycleConfig {
    @Bean(initMethod = "init", destroyMethod = "close")
    public NetworkClient networkClient() {
        NetworkClient networkClient = new NetworkClient();
        networkClient.setUrl("http://hello-spring.dev");

        return networkClient;
    }
}
```

- 메서드 이름을 자유롭게 줄 수 있습니다.
- **‘설정 정보’를 사용하므로 외부 라이브러리에도 초기화, 소멸 메서드 적용이 가능합니다.**
- `destroyMethod`는 추론기능이 존재해 기본값으로 `inferred`가 설정되어 있는데, 이 기능은 `clouse`, `shutdown`의 메서드를 자동 호출해준다.

`@PostConstruct`, `@PreDestroy`으로 간편하게 등록할 수도 있다. 스프링에 종속적이지 않고 JSR-250자바 표준이다.

```java
@PostConstruct // 주입완료시 호출
public void init() {
    System.out.println("NetworkClient.init");
    connect();
    call("초기화 연결 메시지");
}

@PreDestroy // 서비스 종료시 호출
public void close() throws Exception {
    System.out.println("NetworkClient.close");
    disconnect();
}
```

- 패키지가 javax(자바 표준)이므로, 스프링이 아닌 곳에서도 잘 동작한다.
- **유일한 단점은 외부 라이브러이에 적용이 불가능하다.**

![실행결과](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%202.png)

실행결과

</aside>

# 빈 스코프

---

<aside>
💡 **NOTE**

> *빈 스코프는 **스프링 빈이 존재할 수 있는 범위를 정의**합니다. 기본적으로 스프링 컨테이너는 싱글톤 스코프로 생성되므로, 스프링 컨테이너와 생명주기가 동일하기 때문에 별도의 관리가 필요 없었습니다. 그러나 설정에 따라 생성과 소멸을 직접 관리해야 할 수도 있습니다.*
> 

빈 스코프의 종류는 다음과 같습니다.

- **싱글톤**: 기본 스코프, 스프링 컨테이너 시작-종료까지 하나만 존재합니다. 대부분의 상황에서 효율적으로 동작합니다.
- **프토토타입**: 각 요청마다 새로운 빈 인스턴스를 생성하며, 스프링이 생성과 의존관계 주입까지만 관리하고, 이후부터는 직접 관리해야 합니다.
- **웹 관련 스코프**
    - `reuqest`: 웹 요청이 들어오고 나갈 떄 까지
    - `session`: 웹 세션이 생성되고 종료될때 까지
    - `application`: 웹의 서블릿 컨텍스트와 같은 범위로 유지

```java
// 컴포넌트 스캔 자동 등록 예
@Scope("prototype")
@Component
public class HelloBean {}
```

```java
// 수동 등록 예
@Scope("prototype")
@Bean
PrototypeBean HelloBean() {
  return new HelloBean();
}
```

</aside>

## 싱글톤 스코프

<aside>
✍️ **NOTE**

> *기존 스프링 컨테이너에 등록된 스프링 빈은 **싱글톤 스코프**라고 하며, 스프링 컨테이너는 항상 같은 인스턴스의 빈을 반환합니다.*
> 

![항상 같은 값을 반환한다.](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%203.png)

항상 같은 값을 반환한다.

```java
public class SingletonTest {
    @Test
    public void singletonBeanFind() {
        ConfigurableApplicationContext ac = new AnnotationConfigApplicationContext(SingletonBean.class);
        
        // 싱글톤 스코프 객체 2개생성 후 비교
        SingletonBean singletonBean1 = ac.getBean(SingletonBean.class);
        SingletonBean singletonBean2 = ac.getBean(SingletonBean.class);
        System.out.println("singletonBean1 = " + singletonBean1);
        System.out.println("singletonBean2 = " + singletonBean2);

        assertThat(singletonBean1).isSameAs(singletonBean2);

        ac.close();
    }

    @Scope("singleton")
    static class SingletonBean{
        @PostConstruct
        public void init() {
            System.out.println("SingletonBean.init");
        }

        @PreDestroy
        public void destroy() {
            System.out.println("SingletonBean.destroy");
        }
    }
}
```

![생성 - 사용 - 삭제 모두출력](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%204.png)

생성 - 사용 - 삭제 모두출력

</aside>

## 프로토타입 스코프

<aside>
✍️ **NOTE**

> ***프로토타입 스코프**는 매 요청마다 새로운 객체를 생성합니다! 싱글톤과 달리 스프링 컨테이너가 생성과 초기화까지만 책임지고, 이후는 클라이언트가 관리해야합니다. (`@PreDestroy`호출 안됨)*
> 

![요청마다 새로운 빈이 생성된다!](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%205.png)

요청마다 새로운 빈이 생성된다!

```java
public class PrototypeTest {
    @Test
    public void singletonBeanFind() {
        ConfigurableApplicationContext ac = new AnnotationConfigApplicationContext(PrototypeBean.class);
        
        // 프로토타입 스코프 2개생성 후 비교
        PrototypeBean prototypeBean1 = ac.getBean(PrototypeBean.class);
        PrototypeBean prototypeBean2 = ac.getBean(PrototypeBean.class);
        System.out.println("PrototypeBean = " + prototypeBean1);
        System.out.println("PrototypeBean = " + prototypeBean2);

        assertThat(prototypeBean1).isNotSameAs(prototypeBean2);

        ac.close();
    }

    @Scope("prototype")
    static class PrototypeBean{
        @PostConstruct
        public void init() {
            System.out.println("PrototypeBean.init");
        }

        @PreDestroy
        public void destroy() {
            System.out.println("PrototypeBean.destroy");
        }
    }
}
```

![@PreDesroy가 출력되지 않는다.](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%206.png)

@PreDesroy가 출력되지 않는다.

</aside>

## 싱글톤 + 프로토타입 스코프 사용시 문제점

<aside>
✍️ **NOTE**

> *싱글톤과 프로토타입 빈을 함께 사용하면 예상한대로 동작하지 않아 문제가 발생할 수 있습니다. 특히, 싱글톤 내부에서 프로토타입을 사용할 경우, 프로토타입이 새롭게 생성되지 않는 문제가 발생합니다.*
> 

```java
public class SingleTonWithPrototypeTest1 {

    @Test
    void singletonClientUserPrototype() {
        AnnotationConfigApplicationContext ac = new AnnotationConfigApplicationContext(ClientBean.class, PrototypeBean.class);
        
        // 싱글톤 스코프 내부의 프로토타입 스코프의 변수 증가
        ClientBean clientBean1 = ac.getBean(ClientBean.class);
        int count1 = clientBean1.logic();
        assertThat(count1).isEqualTo(1);

        // 싱글톤 스코프 내부의 프로토타입 스코프의 변수 증가
        ClientBean clientBean2 = ac.getBean(ClientBean.class);
        int count2 = clientBean2.logic();
        assertThat(count2).isEqualTo(2); // 이전 객체를 사용해 2가나옴
    }

		// 싱글톤 스코프
    static class ClientBean{
        private final PrototypeBean prototypeBean;

        public ClientBean(PrototypeBean prototypeBean) {
            this.prototypeBean = prototypeBean;
        }

        public int logic() {
            prototypeBean.addCount();
            int count = prototypeBean.getCount();
            return count;
        }

    }

		// 프로토타입 스코프
    @Scope("prototype")
    static class PrototypeBean{
        private int count = 0 ;

        public void addCount() {
            count ++;
        }

        public int getCount() {
            return count;
        }

        @PostConstruct
        public void init() {
            System.out.println("PrototypeBean.init");
        }

        @PreDestroy
        public void destroy() {
            System.out.println("PrototypeBean.destroy");
        }

    }
}
```

![Untitled](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%207.png)

- 싱글톤 타입을 통해 프로토타입 빈을 호출하는 경우, 프로토타입의 스코프는 요청마다 새롭게 생성되지 않습니다.
- 싱글톤 내에 있기 때문에, 요청2도 같은 clientBean에 요청이 되고 그 안에 있는 프로토타입 빈은 동일합니다. 따라서 새로운 프로토타입 빈이 생성되지 않습니다.
- 프로토타입은 의존주입에 사용되는 경우 주입받는 시점에 새로운 빈이 생성됩니다.
    - ex) clientA → prototypeBean1, clientB → prototypeBean2
    - 사용할때 마다 새롭게 생성되지는 않습니다.
</aside>

## 프로토타입 빈 문제점 해결

<aside>
💡 **NOTE**

> *스프링은 싱글톤과 프로토타입 빈을 같이 사용할 때 발생하는 문제를 해결하기 위해 여러가지 해결책을 제공하고 있습니다.*
> 

### **ObjectProvider**

스프링은 ObjectProvider를 제공하여 필요할 때마다 스프링 컨테이너로부터 새로운 프로토타입 빈을 요청할 수 있게 해주는 DL(Dependecy Lookup) 서비스를 제공합니다.

```java
@Component
static class ClientBean{

    @Autowired
    private ObjectProvider<PrototypeBean> prototypeBeanProvider;

    public int logic() {
		    // 스프링 컨테이너에서 새로운 프로토타입 빈 반환
        PrototypeBean prototypeBean = prototypeBeanProvider.getObject();
        prototypeBean.addCount();

        int count = prototypeBean.getCount();
        return count;
    }
}
```

### **JSR-330 Provider**

스프링 부트 3.0 이상에서는 자바 표준의 방법인 provider를 사용할 수 있습니다.

```java
@Component
static class ClientBean{

    @Autowired
    private Provider<PrototypeBean> provider;

    public int logic() {
    		// 스프링 컨테이너에서 새로운 프로토타입 빈 반환
        PrototypeBean prototypeBean = provider.get();
        prototypeBean.addCount();

        int count = prototypeBean.getCount();
        return count;
    }

}
```

</aside>

## 웹 스코프

<aside>
✍️ **NOTE**

> *웹 스코프는 HTTP 요청의 생명주기에 따라 스프링 빈의 생명주기가 결정되는 특별한 범위를 지칭합니다. 주로 웹 애플리케이션에서 사용되며, 각 요청이나 세션에 따라 빈의 생성과 소멸이 관리됩니다.*
> 

![Untitled](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%208.png)

웹 스코프의 종류는 다음과 같습니다.

- **Request Scope**: HTTP 요청이 시작될 때 생성되어 끝날 때 소멸합니다.
- **Session Scope**: HTTP 세션이 시작될 때 생성되어 세션이 종료될 때 소멸합니다.
- **Application Scope**: 서블릿 컨텍스트와 동일한 생명주기를 가집니다.
- **Websocket Scope**: 웹 소켓의 연결 생명주기와 동일하게 관리됩니다.

```java
@Component
@Scope(value = "request") // request 스코프 설정
public class MyLogger {

    private String uuid;
    private String requestURL;

    public void setRequestURL(String requestURL) {
        this.requestURL = requestURL;
    }

    public void log(String message) {
        System.out.println("[" + uuid + "]" + "[" + requestURL + "] " + message);
    }

    @PostConstruct
    public void init() {
        uuid = UUID.randomUUID().toString();
        System.out.println("[" + uuid + "] request scope bean create:" + this);
    }

    @PreDestroy
    public void close() {
        System.out.println("[" + uuid + "] request scope bean close:" + this);
    }
}
```

```java
@Controller
@RequiredArgsConstructor
public class LogDemoController {
    private final LogDemoService logDemoService;
    private final ObjectProvider<MyLogger> myLoggerProvider;

    @RequestMapping("log-demo")
    @ResponseBody
    public String logDemo(HttpServletRequest request) {
        String requestURL = request.getRequestURL().toString();
        MyLogger myLogger = myLoggerProvider.getObject();
        myLogger.setRequestURL(requestURL);
        myLogger.log("controller test");
        logDemoService.logic("testId");
        return "OK";
    }
}
```

- 현재 시점에서는 `Scope ‘reuqest’ is not active`오류가 발생하는데 이유는 싱글톤 빈이 생성되는 시점에 reqest scope가 활성화되지 않았기 때문입니다.

### 해결책: 스코프 프록시 사용

이 문제를 해결하기 위해서 스프링은 스코프 프록시를 제공합니다. 스코프 프록시를 제공하면 싱글톤 빈이 실제로 request 스코프 빈을 참조하는 대신 프록시로 간접적으로 참조합니다. 이 프록시는 실제 요청이 시작될때 실제 request빈을 찾아 사용합니다.

```java
@Component
@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS) // 프록시 모드 추가
public class MyLogger {
	// ..
}
```

```java
@Controller
@RequiredArgsConstructor
public class LogDemoController {
    private final LogDemoService logDemoService;
    private final MyLogger myLogger;  // 프록시 주입

    @RequestMapping("log-demo")
    @ResponseBody
    public String logDemo(HttpServletRequest request) {
        String requestURL = request.getRequestURL().toString();
        
        myLogger.setRequestURL(requestURL);  // 프록시를 통한 메소드 호출
        myLogger.log("controller test");
        logDemoService.logic("testId");
        return "OK";
    }
}
```

![의존성 주입을 프록시 객체로 변경한다!](%5BSpring%20Study%5D%2003-4%20%EB%B9%88%20%EC%83%9D%EB%AA%85%EC%A3%BC%EA%B8%B0(@Post,%20@Destroy)%20%EC%8A%A4%EC%BD%94%ED%94%84/Untitled%209.png)

의존성 주입을 프록시 객체로 변경한다!

</aside>