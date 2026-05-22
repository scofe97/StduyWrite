# [Spring Study] 02-3. Servlet 멀티 쓰레드

주제: Spring Study

- 참고
    
    [서블릿, 동시 요청 - 멀티 쓰레드](https://mbc2579.tistory.com/37)
    
    [[WEB] Multi-Thread & Thread Pool의 이해](https://maenco.tistory.com/entry/WEB-Multi-Thread-Thread-Pool의-이해)
    

# Servlet과 멀티 쓰레드

---

<aside>
💡 **NOTE**

> `*Servlet Container`는 `Servlet`을 싱글톤으로 관리하지만, 멀티 쓰레드 방식으로 동작하여 여러 클라이언트의 요청을 처리할 수 있다. 싱글톤의 경우 멀티 쓰레드 방식으로 쓰기 어려울텐데 어떻게 구현하고 있을까?*
> 

Servlet Container는 클라이언트에서 요청이 오면 웹 애플리케이션 서버(WAS)에서 쓰레드 1개를 할당해서 요청을 처리하도록 한다.

![1 요청 = 1 쓰레드](%5BSpring%20Study%5D%2002-3%20Servlet%20%EB%A9%80%ED%8B%B0%20%EC%93%B0%EB%A0%88%EB%93%9C/ezgif-2-1065e8bcfd.gif)

1 요청 = 1 쓰레드

하지만 HTTP의 요청은 동시에 여러번 올 수 있다. Servlet 컨테이너는 이러한 동시 요청을 처리하기 위해 멀티 쓰레드를 사용한다.

![1작업 = 1쓰레드를 위해 쓰레드를 새로 생성한다!](%5BSpring%20Study%5D%2002-3%20Servlet%20%EB%A9%80%ED%8B%B0%20%EC%93%B0%EB%A0%88%EB%93%9C/Untitled.png)

1작업 = 1쓰레드를 위해 쓰레드를 새로 생성한다!

- `Servlet Container`는 요청을 처리할 쓰레드를 할당하며, 쓰레드는 `Servlet`의 `service()`를 호출해서 요청을 처리합니다.
- 하지만 쓰레드는 생성 비용이 크며, 위와 같이 요청마다 쓰레드를 생성하고, 제거하면 요청수가 많아질수록 쓰레드가 불필요하게 생성되고 삭제되는 오버헤드를 겪을 수 있습니다.
</aside>

## 쓰레드 풀

<aside>
✍️ **NOTE**

> ***쓰레드 풀**은 성능과 자원 관리 최적화를 위해 사용되며, 미리 일정 수의 쓰레드를 생성하여 대기시키고, 요청이 들어오면 사용 가능한 쓰레드를 할당하여 처리합니다.*
> 

![쓰레드 풀](%5BSpring%20Study%5D%2002-3%20Servlet%20%EB%A9%80%ED%8B%B0%20%EC%93%B0%EB%A0%88%EB%93%9C/ezgif-2-23e84193b9.gif)

쓰레드 풀

- 쓰레드 풀을 통해서 매번 새로운 쓰레드를 생성하지 않아도 됩니다.
- 쓰레드 풀은 쓰레드의 최대 수를 제한하여, 시스템 자원이 고갈되지 않도록 할 수 있습니다.

### 쓰레드 풀의 구성요소

- **쓰레드 풀 크기**: 유지할 수 있는 쓰레드의 최소 및 최대 개수를 설정합니다.
- **대기 큐**: 모든 쓰레드가 바쁠 때 요청이 대기하는 큐입니다. 쓰레드가 사용 가능해지면 대기 중인 요청이 처리됩니다.
- **거부 정책**: 쓰레드 풀과 대기 큐가 모두 가득찼을 때 요청을 어떻게 처리할지 결정하는 정책입니다. 요청을 거부하거나 대기시키는 방법이 있습니다.

```xml
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443"
           maxThreads="200"
           minSpareThreads="10"
           acceptCount="100"
           maxConnections="500" />
```

```java
@Configuration
@EnableAsync // 비동기 처리 활성화
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5); // 기본적으로 유지할 쓰레드 수
        executor.setMaxPoolSize(10); // 최대 쓰레드 수
        executor.setQueueCapacity(25); // 큐의 크기
        executor.setThreadNamePrefix("Async-"); // 쓰레드 이름 접두사
        executor.initialize();
        return executor;
    }
}
```

```java
@Service
public class AsyncService {

    @Async("taskExecutor")
    public void executeAsyncTask() {
        System.out.println("Execute method asynchronously - " + Thread.currentThread().getName());
        try {
            // 비동기 작업 시뮬레이션
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

### WAS 튜닝

- **WAS의 주요 튜닝 포인트는 최대 쓰레드의 개수이다**
    - 값이 너무 낮다?
        - 동시 요청이 많으면 클라이언트는 금방 응답 지연이 됨
        - 최소 50%는 사용하고 평균 70%는 사용해야 함
    - 값이 너무 높다?
        - 동시 요청이 많으면, CPU/메모리 리소스 임계점 초과로 서버가 다운됨
        - 즉 한계 범위를 모르기에 너무 높으면 서버가 다운된다

- **쓰레드 풀의 적정 숫자**
    - 애플리케이션의 복잡도, CPU 메모리, IO 리소스 상황에 따라 모두 다르다
    - 적절한 쓰레드 개수 = 사용 가능한 코어 * (1+대기시간 / 서비스 시간) → 예시
</aside>

## WAS 튜닝

<aside>
✍️ **NOTE**

> *WAS를 효율적으로 운영하기 위해서는 **적절한 쓰레드 수를 설정**해야 하며 이를 위해 여러가지 요소를 고려할 수 있습니다.*
> 

WAS의 주요 튜닝 포인트는 최대 쓰레드의 개수이며 다음과 같은 상황이 발생한다.

- 값이 너무 낮다?
    - 동시 요청이 많으면 클라이언트는 금방 응답 지연이 됨
    - 최소 50%는 사용하고 평균 70%는 사용해야 함
- 값이 너무 높다?
    - 동시 요청이 많으면, CPU/메모리 리소스 임계점 초과로 서버가 다운됨
    - 즉 한계 범위를 모르기에 너무 높으면 서버가 다운된다

### **적절한 쓰레드 개수 공식**

적절한 쓰레드 수를 계산하기 위한 공식은 다음과 같습니다:

```java
적절한 쓰레드 개수 = 사용 가능한 코어 수 * (1 + 대기 시간 / 서비스 시간)
```

- **사용 가능한 코어 수**: 서버의 물리적 코어 수입니다. 예를 들어, 8코어 CPU가 있는 서버라면 이 값은 8이 됩니다.
- **대기 시간**: I/O 작업이나 다른 자원을 기다리는 데 소요되는 시간입니다.
- **서비스 시간**: 실제로 요청을 처리하는 데 소요되는 시간입니다.
</aside>