# [Spring Study] 05. DTO 코드스타일

주제: Spring Study

[[개발고민] Spring DTO는 어떻게 작성하고 변환해야 할까?](https://dukcode.github.io/spring/spring-dto/)

[데이터 전송 객체(DTO) 정의 및 사용 방법 | Okta Identity Korea](https://www.okta.com/kr/identity-101/dto/)

[[Spring] 엔티티(Entity) 또는 도메인 객체(Domain Object)와 DTO를 분리해야 하는 이유](https://mangkyu.tistory.com/192)

[The DTO Pattern (Data Transfer Object) | Baeldung](https://www.baeldung.com/java-dto-pattern)

[Web API design best practices - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)

### **DTO 패턴의 이해**

- **DTO 정의**: DTO는 애플리케이션의 다른 부분 간에 데이터를 전송하기 위한 객체입니다. 이러한 객체는 특정 요청에 대해 필요한 데이터만을 포함하여 네트워크를 통해 전송됩니다.
- **사용 이유**: 데이터베이스 엔티티 클래스는 데이터베이스 테이블을 직접 반영하기 위한 것이므로, 클라이언트가 요청하는 데이터 형태와는 다를 수 있습니다. DTO를 사용하면, 필요한 데이터만을 클라이언트에 전달할 수 있으며, 데이터의 직렬화 형태나 포함된 데이터를 더 유연하게 관리할 수 있습니다.

![Untitled](%5BSpring%20Study%5D%2005%20DTO%20%EC%BD%94%EB%93%9C%EC%8A%A4%ED%83%80%EC%9D%BC/Untitled.png)

### **DTO 패턴의 장점**

1. **네트워크 트래픽 감소**: 단일 요청으로 필요한 모든 데이터를 전송할 수 있어, 여러 번의 요청을 줄일 수 있습니다.
2. **직렬화 관리 용이**: DTO를 통해 데이터의 직렬화 형태(XML, JSON, YAML 등)를 한 곳에서 관리할 수 있어, 애플리케이션 전반의 유지보수가 용이해집니다.
3. **레이어 간의 결합도 감소**: DTO를 사용함으로써 프레젠테이션 레이어와 데이터 액세스 레이어 간의 의존성을 줄일 수 있으며, 각 레이어가 변경되어도 다른 레이어에 미치는 영향을 최소화할 수 있습니다.

### **DTO 구현**

- DTO 클래스는 클라이언트 요청에 맞춰 설계됩니다. 예를 들어, 고객 정보와 계좌 정보를 함께 전달해야 하는 경우, **`CustomerDetailsDTO`**와 같은 클래스를 만들고, 고객 정보와 계좌 정보를 모두 포함시킬 수 있습니다.
- 데이터베이스 엔티티에서 DTO로 데이터를 매핑하기 위한 로직을 구현해야 합니다. 이 과정에서는 Java 코드나 라이브러리를 활용하여 데이터베이스 엔티티의 데이터를 DTO 객체로 변환합니다.

### **DTO 클래스 생성 과정:**

1. **DTO 패키지 생성**: **`dto`**라는 이름의 새로운 패키지를 생성하여 모든 DTO 클래스를 이곳에 위치시킵니다.
2. **AccountDto와 CustomerDto 생성**: 데이터베이스의 **`Accounts`**와 **`Customer`** 테이블을 대표하는 **`AccountsDto`**와 **`CustomerDto`** 클래스를 생성합니다. 이 클래스들은 클라이언트에 전달될 데이터만을 포함합니다. 예를 들어, 내부 데이터베이스의 ID 값은 클라이언트에게 필요하지 않으므로 포함시키지 않습니다.
3. **응답용 DTO 생성**: **`ResponseDto`**와 **`ErrorResponseDto`** 클래스를 생성하여 클라이언트 요청에 대한 성공 응답 또는 오류 응답을 표준화합니다. 이 클래스들은 상태 코드, 메시지, 오류 발생 시간 등의 정보를 포함할 수 있습니다.

### **Lombok 사용:**

- **`@Data`** 어노테이션을 사용하여 getter, setter, toString, equals, hashCode 메소드를 자동으로 생성합니다. 엔티티 클래스에서는 이 어노테이션을 사용하지 않았는데, 이는 JPA 프레임워크와의 충돌을 피하기 위함입니다.

### **결론:**

DTO 패턴은 마이크로서비스 아키텍처에서 클라이언트와의 효율적인 데이터 교환을 위해 필수적인 디자인 패턴입니다. 이 패턴을 통해 데이터 전송을 최적화하고, 애플리케이션의 유지보수성을 높이며, 클라이언트 요구사항에 더 유연하게 대응할 수 있습니다. 강의에서는 이러한 DTO 클래스를 생성하는 방법을 실습을 통해 보여주었으며, 이는 향후 마이크로서비스 개발에 있어 중요한 기반을 마련합니다.

[P of EAA: Data Transfer Object](https://martinfowler.com/eaaCatalog/dataTransferObject.html)