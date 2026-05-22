# [Spring MSA] 02-2. 외부설정 읽기(Environment, @ConfigurationProperties)

주제: Spring MSA
연관 노트: [Spring MSA] 02-3. Spring Cloud Config (https://www.notion.so/Spring-MSA-02-3-Spring-Cloud-Config-e90fa4b775494935b6aee1df9dda8c79?pvs=21)

- 참고
    
    [Externalized Configuration :: Spring Boot](https://docs.spring.io/spring-boot/reference/features/external-config.html#features.external-config.typesafe-configuration-properties.conversion)
    
    [spring boot 3 migration#03 @ConstructorBinding 스펙 변경](https://multifrontgarden.tistory.com/307)
    

# 외부설정 읽기

---

<aside>
💡 **NOTE**

> *스프링 부트는 외부 설정을 통해 동일한 애플리케이션 코드를 다양한 환경(개발, 테스트, 프로덕션 )에서 사용할 수 있게 해줍니다. 외부 설정들은 스프링이 제공하는 다양한 방식으로 조회가 가능합니다.*
> 

스프링부트에서 사용가능한 외부 설정값을 읽는 방법은 다음과 같은 방식으로 이루어집니다.

![Environment로 4가지 방식을 공통적으로 사용할 수 있음!](%5BSpring%20MSA%5D%2002-2%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95%20%EC%9D%BD%EA%B8%B0(Environment,%20@Configurat/Untitled.png)

Environment로 4가지 방식을 공통적으로 사용할 수 있음!

- `@Environment`
- `@Value`
- `@ConfigurationProperties`
</aside>

## Environment

<aside>
✍️ **NOTE**

> *스프링은 `Environment` 인터페이스를 사용하여 설정값을 읽을 수 있습니다.*
> 

```yaml
build:
  version: "3.0"

accounts:
  message: "계정 메시지"
  contactDetails:
    name: "이름"
    email: "이메일"
  onCallSupport:
    - (555) 555-1234
    - (555) 523-1345
```

```java
@SpringBootTest
@ContextConfiguration(classes = SpringStudyApplication.class)
public class ConfigTest {

		// 
    private final Environment env;

    @Autowired
    public ConfigTest(Environment env) {
        this.env = env;
    }
    
    @Test
    void envTest(){
        String buildVersion = env.getProperty("build.version");
        System.out.println("buildVersion = " + buildVersion);
    }

    @Test
    void envTest2(){
        String accounts = env.getProperty("accounts");
        String accountsMessage = env.getProperty("accounts.message");
        System.out.println("accounts = " + accounts); // null
        System.out.println("accountsMessage = " + accountsMessage); // 계정 메시지
    }
}
```

</aside>

## @Value

<aside>
✍️ **NOTE**

> *@Value 방식은 개별 설정 값을 간단하게 주입받을 수 있는 방법입니다.*
> 

```yaml
build:
  version: "3.0"

accounts:
  message: "계정 메시지"
  contactDetails:
    name: "이름"
    email: "이메일"
  onCallSupport:
    - (555) 555-1234
    - (555) 523-1345
```

```java
@SpringBootTest
@ContextConfiguration(classes = SpringStudyApplication.class)
public class ConfigTest {

    @Value("${build.version}")
    private String buildVersion;

    //@Value("${accounts}")
    //private String accounts; // 에러발생(accounts의 내용은 String으로 담지못함)

    @Value("${accounts.message}")
    private String accountsMessage;

    @Test
    void valueTest(){
        System.out.println("buildVersion = " + buildVersion);
    }

    @Test
    void valueTest2(){
        // System.out.println("accounts = " + accounts); 
        System.out.println("accountsMessage = " + accountsMessage); // 계정 메시지
    }
}
```

- `@Value`로 하나하나 외부 설정의 키 값을 입력받고, 주입받는게 번거롭다.
- 설정데이터가 하나하나 분리되어 있는게 아니라, 정보의 묶음으로 되어있다.
    - 여기서는 my.datasource부분으로 묶여잇다.
    - 이런 부분을 **객체로 변환해서 사용하면 더 좋을 것!**
</aside>

## @ConfigurationProperties

<aside>
✍️ **NOTE**

> `*@ConfigurationProperties`는 스프링 부트에서 애플리케이션 설정 값을 객체에 바인딩 할 때 사용하며, 타입 안전성을 보장하고 유지보수성을 높여줍니다.*
> 

```yaml
accounts:
  message: "계정 메시지"
  contactDetails:
    name: "이름"
    email: "이메일"
  onCallSupport:
    - (555) 555-1234
    - (555) 523-1345
```

`@ConfigurationProperties`를 통해 accounts의 설정값을 바인딩하면서 타입이 어긋나는 경우 예외를 발생시킵니다.

```java
@Getter
@RequiredArgsConstructor
@ConfigurationProperties(prefix = "accounts")
public class AccountsProperties {

    private final String message;
    private final ContactDetails contactDetails;
    private final List<String> onCallSupport;

    @RequiredArgsConstructor
    @Getter
    public static class ContactDetails {
        private final String name;
        private final String email;
    }
}
```

`@EnableConfigurationProperties`는 스프링 부트에 `@ConfigurationProperties`로 정의된 클래스를 등록하여 사용할 수 있게 해줍니다. 이를 통해 해당 클래스가 스프링 컨테이너 Bean에 등록되고, 외부 설정값이 해당 클래스의 필드에 바인딩 됩니다.

```java
@SpringBootApplication
@EnableConfigurationProperties(AccountsProperties.class)
public class SpringStudyApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringStudyApplication.class, args);
	}
}
```

```java
@Test
void ConfigurationPropertiesTest(){
    System.out.println("Message: " + accountsProperties.getMessage());
    System.out.println("Contact Name: " + accountsProperties.getContactDetails().getName());
    System.out.println("Contact Email: " + accountsProperties.getContactDetails().getEmail());
    System.out.println("On Call Support: " + accountsProperties.getOnCallSupport());
}
```

</aside>

## @ConfigurationPropertiesScan

<aside>
✍️ **NOTE**

> `*@ConfigurationPropertiesScan`는 @ConfigurationProperties 애노테이션이 붙은 클래스를 자동으로 스캔하여 스프링 컨텍스트에 등록합니다.*
> 

```java
@SpringBootApplication
@ConfigurationPropertiesScan // 하위 패키지 검색
public class MyApplication {}
```

```java
@SpringBootApplication
@ConfigurationPropertiesScan({ "com.example.app", "com.example.another" }) // 특정 패키지 검색
public class MyApplication {}
```

</aside>

## @ConfigurationProperties 검증

<aside>
✍️ **NOTE**

> *자바에서는 **자바 빈 검증기(java bean validation)**라는 표준 검증기가 제공된다!*
> 

```groovy
implementation 'org.springframework.boot:spring-boot-starter-validation'
```

```yaml
accounts:
  message: "계정 메시지"
  contactDetails:
    name: "이름"
    email: "이메일"
  onCallSupport:
    - (555) 555-1234
    - (555) 523-1345
```

```java
@Getter
@ConfigurationProperties(prefix= "accounts")
@Validated
@RequiredArgsConstructor
public class AccountsProperties {

    @NotEmpty(message = "메시지를 입력해야 합니다")
    private final String message;

    @Valid
    private final ContactDetails contactDetails;

    @NotEmpty(message = "긴급 연락처 목록을 입력해야 합니다")
    private final List<@NotEmpty @Size(min = 10, max = 20, message = "전화번호는 10자에서 20자 사이여야 합니다") String> onCallSupport;

    @RequiredArgsConstructor
    @Getter
    public static class ContactDetails {
        @NotEmpty(message = "이름을 입력해야 합니다")
        private final String name;

        @Email(message = "유효한 이메일을 입력해야 합니다")
        @NotEmpty(message = "이메일을 입력해야 합니다")
        private final String email;
    }
}
```

```java
@SpringBootTest(classes = SpringStudyApplication.class)
public class ConfigTest {

    @Autowired
    private AccountsProperties accountsProperties;

    @Test
    void ConfigurationPropertiesTest(){
        System.out.println("Message: " + accountsProperties.getMessage());
        System.out.println("Contact Name: " + accountsProperties.getContactDetails().getName());
        System.out.println("Contact Email: " + accountsProperties.getContactDetails().getEmail());
        System.out.println("On Call Support: " + accountsProperties.getOnCallSupport());
    }
}
```

![Untitled](%5BSpring%20MSA%5D%2002-2%20%EC%99%B8%EB%B6%80%EC%84%A4%EC%A0%95%20%EC%9D%BD%EA%B8%B0(Environment,%20@Configurat/Untitled%201.png)

</aside>