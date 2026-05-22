# [Spring Study] 05-5. Jackson - ObjectMapper의 동작 방식

주제: Spring Study

- 참고
    
    [추가 배포 없이 API의 case 통일시키기 / if(kakaoAI)2024](https://www.youtube.com/watch?v=ZE5xgQuvHFQ)
    
    [Value Object Design Pattern in Hibernate/Spring | HackerNoon](https://hackernoon.com/value-object-design-pattern-in-hibernatespring)
    
    [Value Object Design Pattern in Hibernate/Spring | HackerNoon](https://hackernoon.com/value-object-design-pattern-in-hibernatespring)
    
    [Jackson 라이브러리 Annotation 총정리](https://demoversion.tistory.com/118)
    
    [Intro to the Jackson ObjectMapper | Baeldung](https://www.baeldung.com/jackson-object-mapper-tutorial#bd-builder-pattern-for-objectmapper)
    
    [[Spring] ObjectMapper의 동작 방식과 SpringBoot가 제공하는 추가 기능들](https://mangkyu.tistory.com/223)
    
    [[Spring] ObjectMapper에서 LocalDateTime이 변환되지 않는 문제](https://woo-chang.tistory.com/75)
    
    [[Java] Spring Boot 환경에서 Jackson 모듈 활용하기 : JSON 파싱, 직렬화, 역 직렬화, JSON 파일 읽어오기/생성](https://adjh54.tistory.com/375)
    
    [[JVM] Jackson ObjectMapper의 성능을 높여줄 Blackbird 모듈](https://mangkyu.tistory.com/355)
    

# **ObjectMapper**

---

<aside>
💡 **NOTE**

> `*ObjectMapper`는 Jackson 라이브러리에서 찾아 볼 수 있으며, JSON - Java 객체간의 변환(직렬화, 역직렬화)를 해주는 라이브러리 클래스입니다.*
> 
</aside>

## ObjectMapper - 직렬화

<aside>
✍️ **NOTE**

> `*ObjectMapper`는 리플렉션을 활용해서 **객체로부터 Json 형태의 문자열**을 만들어내는데, 이것을 **직렬화**라고 합니다. 해당 부분은 주로 `@ResponseBody`나 `@RestController`, `ResponseEntity`등을 사용하는데 처리됩니다.*
> 

![Untitled](%5BSpring%20Study%5D%2005-5%20Jackson%20-%20ObjectMapper%EC%9D%98%20%EB%8F%99%EC%9E%91%20%EB%B0%A9%EC%8B%9D/Untitled.png)

String에서는 기본적으로 jackson 모듈의 `ObjectMapper`라는 클래스가 직렬화를 처리합니다. 그 과정에서 `ObjectMapper`의 `writeValueAsString`이라는 메소드가 사용됩니다.

```java
public class Person {
    private String name;
    private int age;

    // 기본 생성자 필요 for JSON 역직렬화
    public Person() {}

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // getter 메소드 ..
}
```

```java
@Component
@RequiredArgsConstructor
public class ObjectMapperService {

    private final ObjectMapper objectMapper;

		// 직렬화
    public String personToJson() throws Exception {
        Person person = new Person("John Doe", 30);
        return objectMapper.writeValueAsString(person); 
        
        // {"name":"John Doe","age":30}
    }
}
```

- `ObjectMapper`의 기본 설정으로는 public 필드 또는 public 형태의 getter만 접근이 가능합니다. 그러므로 직렬화를 위해 기본적으로 getter를 만드는 것이 좋습니다.

위에서 말한 `getter`의 접근으로 생성한다는 점이 때로는 의도치 않은 메시지를 만들어 내기도 합니다.

```java
public class Person {
    private String name;
    private int age;

    // 기본 생성자 필요 for JSON 역직렬화
    public Person() {}

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

		// 이상한 getter 추가
    public String getNameWithAge(){
        return name + "(" + age + ")";
    }
}
```

```java
@Component
@RequiredArgsConstructor
public class ObjectMapperService {

    private final ObjectMapper objectMapper;

		// 직렬화
    public String personToJson() throws Exception {
        Person person = new Person("John Doe", 30);
        return objectMapper.writeValueAsString(person); 
        
        // {"name":"John Doe","age":30,"nameWithAge":"John Doe(30)"}
    }
}
```

</aside>

## ObjectMapper - 역직렬화

<aside>
✍️ **NOTE**

> `*ObjectMapper`는 리플렉션을 사용해 Json 문자열에서 객체를 생성하는데, 이를 역직렬화라고 합니다. 이 과정은 주로 `@RequestBody`로 json 문자열을 받을 때 사용됩니다.*
> 

![](%5BSpring%20Study%5D%2005-5%20Jackson%20-%20ObjectMapper%EC%9D%98%20%EB%8F%99%EC%9E%91%20%EB%B0%A9%EC%8B%9D/Untitled%201.png)

역직렬화는 기본적으로 다음과 같은 과정을 거칩니다.

1. 기본 생성자를 사용해 객체를 생성합니다.
2. 필드 값을 찾아 바인딩합니다.

먼저, 객체를 생성하는데 기본 생성자가 없으면 에러가 발생합니다. 기본 생성자로 객체를 생성한 후에는 필드 값을 찾아야 하는데, 기본적으로 Public 필드 또는 public 형태의 `getter`를 이용해 찾을 수 있습니다.

```java
@Test
void jsonToPersonTest() throws Exception {
    String personJson = "{\"name\":\"John Doe\",\"age\":30}"; // json 문자열

    Person result = objectMapperService.jsonToPerson(personJson);
    System.out.println("result = " + result); // 객체값 출력!
}
```

</aside>

## ObjectMapper에서 LocalDateTime 사용하기

<aside>
✍️ **NOTE**

> `*LocalDateTime`은 자바8에서 도입이 되었고, Jackson 라이브러리는 이전 버전과의 호환성을 위해 해당 타입에 대한 지원을 기본적으로 하지 않습니다. 따라서 이를 위해 `JavaTimeMoudle`을 `ObjectMapeer`에 등록해줘야 합니다.*
> 

```java
objectMapper = new ObjectMapper();
objectMapper.registerModule(new JavaTimeModule()); // 추가
```

</aside>

## ObjectMapper를 위한 DTO 클래스 작성법

<aside>
✍️ **NOTE**

> `*ObjetMapper`를 위한 DTO 클래스 작성법은 위에서 말한대로 기본 생성자와, 올바른 `getter()`함수를 제공하면 되지만, 이외에도 **추가적인 어노테이션 옵션이 있습니다.***
> 

```java
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@ToString
public class Person {

    private String name;

    private int age;

		// json 필드 이름과 다른경우 매칭시켜준다.
    @JsonProperty("email_address")
    private String email;

		// json 직렬화/역직렬화에서 제외된다.
    @JsonIgnore
    private String password;

		// 날짜형식을 지정해줍니다.
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-mm-dd")
    private LocalDate birthDate;
}

```

```java
@Test
void jsonTest3() throws Exception {
    // Person 객체 생성
    Person person = new Person("John Doe", 30, "johndoe@example.com", "supersecret", LocalDate.of(1990, 1, 1));

    String jsonString = objectMapper.writeValueAsString(person);
    System.out.println("jsonString = " + jsonString); // email -> email_address로 변환, password 무시
    // {"name":"John Doe","age":30,"birthDate":"1990-01-01","email_address":"johndoe@example.com"}

    String jsonInput = "{\"name\":\"Jane Doe\",\"age\":25,\"email_address\":\"janedoe@example.com\",\"birthDate\":\"1995-05-30\"}";
    Person personFromJson = objectMapper.readValue(jsonInput, Person.class);
    System.out.println("personFromJson = " + personFromJson);
    // Person(name=Jane Doe, age=25, email=janedoe@example.com, password=null, birthDate=1995-05-30)
}
```

</aside>