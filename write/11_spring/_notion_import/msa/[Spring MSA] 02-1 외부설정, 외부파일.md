# [Spring MSA] 02-1. 외부설정, 외부파일

주제: Spring MSA

- 참고
    
    [[Spring Boot] 외부 설정](https://hhlin.tistory.com/m/117)
    
    [Externalized Configuration :: Spring Boot](https://docs.spring.io/spring-boot/reference/features/external-config.html#features.external-config.typesafe-configuration-properties.conversion)
    

# 외부 설정

---

<aside>
💡 **NOTE**

> ***스프링은 애플리케이션의 설정과 구성 정보를 외부 파일에 정의하고 관리할 수 있는 다양한 방법을 유지하며, 이를 통해 애플리케이션의 유연성과 유지 보수성을 높일 수 있습니다.***
> 

![개발 환경, 운영 환경에서 다른 DB를 사용한다. (설정값을 바꿔가며 따로 빌드)](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled.png)

개발 환경, 운영 환경에서 다른 DB를 사용한다. (설정값을 바꿔가며 따로 빌드)

- **개발 서버** : `dev.db.com`이 필요하므로, 이 값을 넣은 `개발app.jar`이 필요하다
- **운영 서버** : **** `prod.db.com`이 필요하므로, 이 값을 넣은 `운영app.jar`이 필요하다

개발과 운영 서버는 각각 다른 DB를 사용하고 있습니다. 이에 따라 각각의 DB 설정이 필요한데, 설정값을 변경하여 각각 빌드하는 것은 비효율적입니다. 그래서 빌드는 한 번만 수행하고, **실행 시점에 외부 설정값을 주입하는 방식을 사용할 수 있습니다.**

![1번의 빌드로 개발/운영 빌드 결과물을 만든다.](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%201.png)

1번의 빌드로 개발/운영 빌드 결과물을 만든다.

- **개발 서버** : `app.jar`을 실행할 때, `dev.db.com`값을 외부 설정으로 주입한다.
- **운영 서버** : `app.jar`을 실행할 때 `prod.db.com`값을 외부 설정으로 주입한다.

이러한 외부설정은 일반적으로 4가지 ㅂ

</aside>

## 외부 설정 종류

<aside>
✍️ **NOTE**

> ***외부 설정은 일반적으로 4가지 방법이 있다!***
> 

![Untitled](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%202.png)

- OS 환경변수: OS에서 지원하는 외부 설정
- 자바 시스템 속성: 자바에서 지원하는 외부 설정(JVM안에서 사용)
- 자바 커맨드 라인 인수: CLI에 전달하는 외부 설정, 실행시 main(args)에서 사용
- 외부 파일
</aside>

## OS 환경변수

<aside>
✍️ **NOTE**

```bash
# window 환경변수 조회
set

# MAC 환경변수 조회
printenv
```

```java
@Test
void OsEnv(){
    // 전체 OS환경변수 조회
    Map<String, String> envMap = System.getenv();

    for (String key : envMap.keySet()) {
        log.info("env {}={}", key, System.getenv(key));
    }
}
```

</aside>

## 자바 시스템 속성

<aside>
✍️ **NOTE**

> ***자바 시스템 속성은 실행한 JVM안에서 접근 가능한 외부 설정입니다. 추가로 자바가 내부에서 미리 설정해두고 사용하는 속성들도 있습니다.***
> 

![IDE 실행시 VM 옵션추가](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%203.png)

IDE 실행시 VM 옵션추가

자바 시스템 속성은 일반적으로 `-D` 옵션을 사용하여 지정합니다. 예를 들어 스프링에서 애플리케이션 서버 포트를 지정하고자 한다면, 다음과 같이 설정할 수 있습니다.

```bash
# 서버포트 8081
java -jar myapp.jar -Dserver.port=8081

# 다중 커스텀 옵션 
java -jar myapp.jar -Dserver.port=8081 -Dspring.datasource.url=jdbc:mysql://localhost:3306/mydb -Dcustom.property1=value1 -Dcustom.property2=value2
```

```java
@Test
void JavaEnv(){
    // 자바 시스템 변수
    System.out.println("javaConfig.getCustomProperty1() = " + javaConfig.getTest1());
    System.out.println("javaConfig.getCustomProperty2() = " + javaConfig.getTest2());
}
```

</aside>

## 자바 커맨드 라인 인수

<aside>
✍️ **NOTE**

> *자바 커맨드 라인 인수는 프로그램을 실행할 때 명령줄에서 전달되는 추가적인 인수들을 의미하며, 자바 프로그램에서는 `main`의 `String[] args` 파라미터를 통해 사용합니다.*
> 

![Untitled](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%204.png)

```bash
--username=userA --username=userB
```

```java
@Slf4j
@SpringBootTest(classes = SpringStudyApplication.class, args = {"--username=userA", "--username=userB"})
public class ExternalEnvTest {

    @Autowired
    private CliConfig cliConfig;

    @Test
    void CliEnv(){
        // 자바 커맨드 라인 변수
        List<String> usernames = cliConfig.getUsernames();
        System.out.println("javaConfig.get(0) = " + usernames.get(0));
        System.out.println("javaConfig.get(1) = " + usernames.get(1));
    }
}

```

- 커맨드 라인에 전달하는 값은 형식이 없고, **단순히 띄어쓰기로 구분한다.**
    - `aaa bbb` ⇒ `[aaa, bbb]` 값 2개
    - `hello world` ⇒ `[hello, wolrd]`  값 2개
    - `“hello world”` ⇒ `[hello world]`  값 1개
</aside>

# 외부 파일과 내부 파일 분리

---

<aside>
💡 **NOTE**

> *개발을 하면 설정 값이 점점 늘어나고 복잡해지며 관리하기 어려워집니다. 이런 문제를 해결하기 위해 설정 값을 파일에 넣어 관리하는 방법을 사용할 수 있습니다.*
> 

외부 파일(`.properties`)를 사용하면 설정 값을 쉽게 관리할 수 있습니다.

![.properties파일을 조회해서 설정값 관리](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%205.png)

.properties파일을 조회해서 설정값 관리

```java
// 개발서버 외부파일
url=dev.db.com
username=dev_user
password=dev_pw

// 운영서버 외부파일
url=prod.db.com
username=prod_user
password=prod_pw
```

외부 설정 파일을 관리하는 과정에서 파일 자체를 관리하는 데 어려움이 발생할 수 있습니다. 

서버가 여러 대인 경우, 변경 사항이 있을 때마다 각 서버의 설정을 모두 변경해야 하는 문제가 있습니다. 이 문제를 해결하기 위해 설정 파일을 내부에 포함시켜 관리하는 방법을 사용할 수 있습니다.

![개발(dev), 운영(prod) 설정 데이터를 포함해서 관리한다.](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%206.png)

개발(dev), 운영(prod) 설정 데이터를 포함해서 관리한다.

빌드 시점에 개발, 운영 설정 파일을 모두 포함해서 빌드합니다.

- **개발 환경**이라면 `application-dev.properties`를 읽어온다.
- **운영 환경**이라면 `application-prod.properties`를 읽어온다.
- 실행할 때 외부 설정을 사용해서 **개발 서버**는 `dev`를, **운영 서버**는 `prod`라는 값을 제공하며 이를 프로필이라 한다.
</aside>

## 내부 파일 합체

<aside>
✍️ **NOTE**

> *설정 파일을 각각 분리해서 관리하면 환경마다 파일이 생성되어 관리하기 어려워질 수 있다. 이런 단점을 보완하기 위해 물리적인 하나의 파일안에서 여러 논리적인 영역을 구분하는 방법을 제공한다.*
> 

![#--- 또는 !---으로 구분한다!  (yaml에서는 ---)](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%207.png)

#--- 또는 !---으로 구분한다!  (yaml에서는 ---)

```java
spring.config.activate.on-profile=dev
url=dev.db.com
username=dev_user
password=dev_pw
---
spring.config.activate.on-profile=prod
url=prod.db.com
username=prod_user
password=prod_pw
```

</aside>

# @Profile

---

<aside>
💡 **NOTE**

> *스프링은 **프로필**이라는 개념을 통해 원하는 설정파일을 읽어오게 할 수 있다!*
> 

```yaml
# 기본 환경
spring:
  profiles:
    active: dev

---
# dev 환경
spring:
  config:
    activate:
      on-profile: dev

url: dev.db.com
username: dev_user
password: dev_pw

---
# prod 환경
spring:
  config:
    activate:
      on-profile: prod

url: prod.db.com
username: prod_user
password: prod_pw
```

- 커맨드 라인 옵션 인수 프로필 설정
    - `--spring.profiles.active=dev`
- 자바 시스템 속성 프로필 설정
    - `-Dspring.profiles.active=dev`
- Jar 프로필 설정
    - `./gradlew clean build`
    - `build/libs` 이동
        - `java -Dspring.profiles.active=dev -jar external-0.0.1-SNPASHOT.jar`
        - `java -jar external-0.0.1-SNPASHOT.jar --spring.profiles.active=dev`
</aside>

## @Profile 실습

<aside>
✍️ **NOTE**

```java
public interface PayClient {
	void pay(int money);
}
```

```java
@Slf4j
public class LocalPayClient implements PayClient {

    @Override
    public void pay(int money) {
        log.info("로컬 결제 money={}", money);
    }
}
```

```java
@Slf4j
public class ProdPayClient implements PayClient {
	 @Override
	 public void pay(int money) {
		 log.info("운영 결제 money={}", money);
	 }
}
```

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final PayClient payClient;

    public void order(int money){
        // 주문 로직
        payClient.pay(money);
    }
}
```

```java
@Slf4j
@Configuration
public class PayConfig {

    @Bean
    @Profile("default")
    public LocalPayClient localPayClient(){
        log.info("LocalPayClient 빈 등록");
        return new LocalPayClient();
    }

    @Bean
    @Profile("prod")
    public ProdPayClient prodPayClient(){
        log.info("ProdPayClient 빈 등록");
        return new ProdPayClient();
    }
}
```

- **default 프로필** (프로필 없이 실행)
    
    ![Untitled](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%208.png)
    
    - 기본값이 활성화 되어 있으면 `LocalPayClient` 등록
- **prod 프로필**
    
    ![Untitled](%5BSpring%20MSA%5D%2002-1%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95,%20%EC%99%B8%EB%B6%80%ED%8C%8C%EC%9D%BC/Untitled%209.png)
    
    - prod 프로필이 활성화 되어있으면, `ProdPayClient` 등록
</aside>

## 우선순위

<aside>
✍️ **NOTE**

> *만약 아래와 같이 프로필을 설정하고 적용하지 않는다면 어떻게 될까?*
> 

```yaml
# 기본 환경
spring:
  profiles:
    active: dev

---
# dev 환경
spring:
  config:
    activate:
      on-profile: dev

url: dev.db.com
username: dev_user
password: dev_pw

---
# prod 환경
spring:
  config:
    activate:
      on-profile: prod

url: prod.db.com
username: prod_user
password: prod_pw
```

- PC에서 개발할 떄 항상 프로필을 지정하면서 실행하는건 상당히 귀찮은 일이다.
- 설정 데이터에는 기본값을 적용할 수 있는데, 이는 프로필과 무관하게 사용된다.

```yaml
# 기본 설정 (프로필이 활성화되지 않았을 때 사용)
url: local.db.com
username: local_user
password: local_pw

---
spring:
  config:
    activate:
      on-profile: dev

url: dev.db.com
username: dev_user
password: dev_pw

---
spring:
  config:
    activate:
      on-profile: prod

url: prod.db.com
username: prod_user
password: prod_pw
```

### 자주 사용하는 우선순위

- 설정 데이터(application.properties)
- OS 환경변수
- 자바 시스템 속성
- 커맨드 라인 옵션 인수
- `@TestPropertySource`

### 설정 데이터 우선순위

- jar 내부 `application.properties`
- jar 내부 프로필 적용 파일 `application-(profile).properties`
- jar 외부 `application.properties`
- jar 외부 프로필 적용 파일 `application-(profile).properties`
</aside>