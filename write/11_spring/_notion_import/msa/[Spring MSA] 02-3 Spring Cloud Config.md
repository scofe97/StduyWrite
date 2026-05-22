# [Spring MSA] 02-3. Spring Cloud Config

주제: Spring MSA
연관 노트: [Spring MSA] 02-2. 외부설정 읽기(Environment, @ConfigurationProperties) (https://www.notion.so/Spring-MSA-02-2-Environment-ConfigurationProperties-297d988ee40e498c8a1125bb79f7c6db?pvs=21)

- 참고
    
    [Spring Cloud Config](https://spring.io/projects/spring-cloud-config)
    
    [Spring Cloud Bus](https://docs.spring.io/spring-cloud-bus/docs/current/reference/html/)
    
    [Configuration Properties :: Spring Cloud Openfeign](https://docs.spring.io/spring-cloud-openfeign/reference/configprops.html)
    
    [Spring Cloud Config 시작하기 | Carrey`s 기술블로그](https://jaehun2841.github.io/2022/03/10/2022-03-11-spring-cloud-config/#3-Properties-Table-추가)
    
    [[Spring] Spring Cloud Config 도입하기 및 private 레포지토리 SSL로 연결 설정 및 privateKey 암호화](https://mangkyu.tistory.com/253)
    
    [back_study/msa/section6/config at main · scofe97/back_study](https://github.com/scofe97/back_study/tree/main/msa/section6/config)
    

# **Spring Cloud Config**

---

<aside>
💡 **NOTE**

> ***Spring Cloud Config**는 분산 시스템의 외부화된 설정 정보를 서버 및 클라이언트에게 제공하는 시스템입니다.*
> 

![Untitled](%5BSpring%20MSA%5D%2002-3%20Spring%20Cloud%20Config/Untitled.png)

**Spring Cloud Config**의 주요이점은 다음과 같습니다.

1. 모든 마이크로서비스의 구성을 한 곳에서 관리할 수 있어, 유지보수성이 올라갑니다.
2. 애플리케이션을 재시작하지 않고도 실시간으로 구성 변경을 적용할 수 있습니다.
3. 중요한 구성 정보를 소스코드 밖에서 안전하게 관리할 수 있습니다.
</aside>

## Spring Cluoud Config Server 구현

<aside>
✍️ **NOTE**

### 1. 설정 서버 구성

설정 서버 구성을 위해서는 먼저 spring-cloud-starter-config와 mavenBom의 spring-cloud-dependencies 추가해주면 됩니다.

```groovy
dependencies {
  implementation 'org.springframework.cloud:spring-cloud-starter-config'
}

dependencyManagement {
  imports {
    mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
  }
}
```

설정 서버의 application.yaml에는 사용해야하는 설정 정보 저장소를 설정하고, 추가적인 설정을 진행해주면 됩니다. 현재는 Git을 외부 설정 저장소로 사용하며, 이외에도 다양한 저장소가 있습니다.

```yaml
server:
  port: 8888 # 일반적으로 설정서버는 8888 사용

spring:
  # 활성화할 프로필을 지정
  profiles:
    active: git  # 'git' 프로필을 활성화하여 Git 저장소를 구성 정보의 소스로 사용

  # Spring Cloud Config 관련 설정
  cloud:
    config:
      server:
        # Git 저장소 설정을 사용하여 구성 정보를 관리
        git:
          uri: "https://github.com/scofe97/back_study.git"  # 구성 파일이 저장된 Git 저장소의 URI
          default-label: main   # 기본적으로 사용할 브랜치명
          search-paths: msa/section6/config  # 구성 파일을 찾을 저장소 내의 경로
          timeout: 5            # 저장소 요청 시 타임아웃 시간 (초 단위)
          clone-on-start: true  # 서버 시작 시 저장소를 클론할지 여부
          force-pull: true      # 서버가 시작할 때마다 저장소의 최신 상태를 강제로 Pull할지 여부
```

마지막으로 Main클래스에 @EnableConfigServer를 붙여주면 끝납니다.

```java
@SpringBootApplication
@EnableConfigServer // 추가!
public class ConfigserverApplication {
	// ..
}
```

### 2. 설정 서버 실행 및 확인

**Spring Cloud Config**를 사용하면 다양한 설정 파일을 읽을 수 있는데 다음의 순서대로 읽어집니다. 만약 순서대로 읽다가 동일한 값을 지니는 설정 정보가 있다면 덮어 씌워지므로 주의해야 합니다.

1. 프로젝트의 application.yaml
2. 설정 저장소의 application.yaml
3. 프로젝트의 application-{profile} .yaml
4. 설정 저장소의 application-{profile} 

```yaml
spring:
  config:
    activate:
      on-profile: "prod"

build:
  version: "1.0"

cards:
  message: "Welcome to EazyBank cards related prod APIs "
  contactDetails:
    name: "Sandra Harald - Product Owner"
    email: "{cipher}40fd4a26acdbe428d773ac93852b759a3f10e136b21445547371d7c0c42f2617dbdf3a8f59e266ec2707ea96c2e9ef4d"
  onCallSupport:
    - (617) 432-2356
    - (936) 564-8721
```

```json
// # GET http://localhost:8088/cards/prod
{
    "name": "cards",
    "profiles": [
        "prod"
    ],
    "label": null,
    "version": "65213dff6d30fbff1c3c74b60d66a7dce4330a68",
    "state": null,
    "propertySources": [
        {
            "name": "https://github.com/scofe97/back_study.git/msa/section6/config/cards-prod.yml",
            "source": {
                "spring.config.activate.on-profile": "prod",
                "build.version": "1.0",
                "cards.message": "Welcome to EazyBank cards related prod APIs ",
                "cards.contactDetails.name": "Sandra Harald - Product Owner",
                "cards.contactDetails.email": "sandra@eazybank.com"
                "cards.onCallSupport[0]": "(617) 432-2356",
                "cards.onCallSupport[1]": "(936) 564-8721"
            }
        },
        {
            "name": "https://github.com/scofe97/back_study.git/msa/section6/config/cards.yml",
            "source": {
                "build.version": "3.0",
                "cards.message": "Welcome to EazyBank cards related local APIs ",
                "cards.contactDetails.name": "Dragos Lech - Developer",
                "cards.contactDetails.email": "dragos@eazybank.com",
                "cards.onCallSupport[0]": "(412) 419-3491",
                "cards.onCallSupport[1]": "(915) 382-1932"
            }
        }
    ]
}
```

</aside>

## Spring Cloud Config Client 구현

<aside>
✍️ **NOTE**

### 1. Config 서버 의존성 추가

**Config Server**와 동일하게 의존성이 필요합니다.

```groovy
dependencies {
  implementation 'org.springframework.cloud:spring-cloud-starter-config'
}

dependencyManagement {
  imports {
    mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
  }
}
```

`application.yaml`에는 **Config server**의 정보와 애플리케이션의 정보를 입력합니다. **Config server**의 URL에 `optional`이 붙는 이유는 통신 실패시에도 계속해서 동작할 수 있도록 하기 위함입니다.

```yaml
spring:
	# 서비스 이름 등록
  application:
    name: "accounts" 
    
  # 기본 프로필 등록
  profiles:
    active: "prod"
	
	# config 서버 연결
  config:
    import: "optional:configserver:http://localhost:8071/"
```

- 마이크로서비스의 `spring.application.name` 속성을 사용하여 이름을 설정합니다.
- 설정된 이름은 서버에 저장된 파일 이름과 일치해야 합니다. 예를 들어, `accounts`가 서비스의 이름이라면 설정 파일은 `account.yaml`이 됩니다.
- `spring.config.import`를 설정하여 Config 서버의 URL을 지정합니다. optional 설정을 하지 않으면 구성서버 연결 실패시 예외가 발생하게 됩니다.
</aside>

## **GitHub 저장소에 암호화된 구성 속성 저장**

<aside>
✍️ **NOTE**

> ***Spring Cloud Config**는 구성 정보를 안전하게 관리하기 위해 암호화 및 복호화 기능을 내장하고 있습니다.*
> 

**Spring Cloud Config**는 구성 정보에 대한 암호화를 지원해줍니다. 가장 간단한 방식인 `encrypt.key`값을 설정하고 암호화/복호화 하는 과정을 진행해봅시다. 

key값을 설정하고나면, `/encrypt`, `/decrypt` 엔드포인트를 기본으로 제공해줍니다.

```yaml
# 암호화 키
encrypt:
  key: 'test' # 어떠한 값도 상관없음
```

```json
// POST http://localhost:8071/encrypt
55b6339f4e4d29a7ed9117a77b73c14a8ff033c39b4766135a9de24eddfd563e559be8e5bc62be0238afaa6b0fdce5c9

// POST http://localhost:8071/decrypt
sandra@eazybank.com
```

이렇게 암호화된 값을 저장할때는 `cipher` 접두어를 사용합니다. 이 접두어를 사용하면 구성 값을 로드할때 자동으로 값을 복호화 합니다.

```bash
# '{cipher}암호화된값'
email: '{cipher}55b6339f4e4d29a7ed9117a77b73c14a8ff033c39b4766135a9de24eddfd563e559be8e5bc62be0238afaa6b0fdce5c9'
```

</aside>

# **Cloud Config** 설정 파일 내용을 갱신하는 방법

---

<aside>
💡 **NOTE**

> ***Spring Cloud Config**의 설정 파일을 변경되어도 별다른 설정을 하지 않으면, 변경사항이 바로 반영되지 않는다. 왜냐하면 설정 서버에 부하를 줄이도록 **Spring Cloud Config Server에 부담을 줄이기위해서 클라이언트측에서 실행시점서 1번 읽고 로컬에 캐싱해두기 때문이다.***
> 

만약 배포 후에 값을 수정하거나 추가해야 할때마다 Config 서버를 재배포하는 것은 매우 비효율적이다. 그러므로 설정이 바뀌면 자동 갱신을 하는 방법이 3가지 있다.

1. `Actuator` 요청 (`@Refresh`)
2. Spring Cloud Bus(`RabbitMq`, Kafka)
3. Watcher를 통해 변경사항을 지속적으로 확인한다.
</aside>

## Actuator 갱신(**@RefreshScope)**

<aside>
✍️ **NOTE**

> `*Actuator`는 애플리케이션의 상태를 모니터링하고 관리하는 여러 엔드 포인트를 제공하며, `/actuator/refresh`를 통해 설정값의 변경을 감지할 수 있습니다!*
> 

설정값을 변경하고 `/actuator/refresh`를 클라이언트에서 요청하면, 변경된 값을 감지하고 자동으로 변경해줍니다.

```json
// Post http://localhost:8080/actuator/refresh
[
    "build.version",
    "config.client.version",
    "accounts.message"
]
```

```java

@ConfigurationProperties(prefix = "accounts")
@Getter
@Setter
public class AccountsContactInfoDto {
    private String message;

    private Map<String, String> contactDetails;

    private List<String> onCallSupport;
}
```

그런데 `@ConfigurationProperties`로 값을 받아오는 경우는 상관없지만, 단순 `@Value`로 값을 받는 경우에는 최신화되지 가 않습니다. 이 경우에는 `@RefreshScope`를 붙여서 해결할 수 있습니다.

[Notes on Dynamic Configuration Properties](https://gist.github.com/dsyer/a43fe5f74427b371519af68c5c4904c7)

참고글

```java
@RefreshScope
@RestController
@RequestMapping(path="/api", produces = {MediaType.APPLICATION_JSON_VALUE})
public class AccountsController {

    private final IAccountsService iAccountsService;

    @Value("${build.version}")
    private String buildVersion;
		
		// ...   
}
```

위와 같은 방식은 무중단으로 진행이 가능하지만 결국 각 서비스가 `/refresh`를 호출해서 직접 설정 정보를 갱신해야하는 번거로움이 남아있습니다.

</aside>

## Spring Cloud Bus(RabbitMQ)

<aside>
✍️ **NOTE**

> ***Spring Cloud Bus**는 메시지 브로커를 통해 마이크로서비스 간에 이벤트, 구성 변경 등을 전파할 수 있습니다. 이를 통해 한 서비스의 변경사항을 네트워크상의 **모든 서비스에 즉각적으로 알릴 수 있습니다.***
> 

[Installing RabbitMQ | RabbitMQ](https://www.rabbitmq.com/docs/download)

**RabbitMQ**는 경량 메시지 브로커로, 스프링 클라우드 버스에 의해 사용됩니다. 이전에 사용했던 Actuator 방식은 각각의 단일 인스턴스에 대해 `/refresh` 요청을 보내야했지만, Cloud Bus방식은 1번의 요청으로 모든 서비스에 `/refresh` 요청을 보낼수 있습니다.

**RabbitMQ**는 단순 `/refresh`가 아닌 `/busrefresh`를 사용해야 각 서비스에 전파가 됩니다.

![Config 변경 흐름도](%5BSpring%20MSA%5D%2002-3%20Spring%20Cloud%20Config/Untitled%201.png)

Config 변경 흐름도

```bash
# latest RabbitMQ 3.13
docker run -it --rm --name rabbitmq \
	-p 5672:5672 \
	-p 15672:15672 \
	rabbitmq:3.13-management
```

```java
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-starter-bus-amqp</artifactId>
</dependency>
```

```java
spring:
  rabbitmq:
    host: "localhost"
    port: 5672
    username: "guest"
    password: "guest"
```

/busrefresh를 보내면 204 성공요청이 발생하며, 이후 /actuator/refresh를 적용한것과 동일하게 동작합니다.

```json
// Post http://localhost:8080/actuator/busrefresh 
```

</aside>

## 설정 갱신 자동화

<aside>
✍️ **NOTE**

> `*spring-cloud-config-monitor`의존성을 추가해서 `/monitor`라는 API를 사용하면 변경사항이 커밋될 때마다 웹훅이 이를 감지하여 자동으로 호출하게 설정할 수 있습니다.*
> 

[Hookdeck - A reliable Event Gateway for event-driven applications](https://hookdeck.com/)

[CLI Reference - Hookdeck](https://hookdeck.com/docs/cli)

![Untitled](%5BSpring%20MSA%5D%2002-3%20Spring%20Cloud%20Config/Untitled%202.png)

```xml
<dependency>
	<groupId>org.springframework.cloud</groupId>
	<artifactId>spring-cloud-config-monitor</artifactId>
</dependency>
```

- Github 저장소에 `/monitor` 엔드포인트를 지정하는 웹훅을 설정합니다.
- `/monitor`는 내부적으로 `/busrefresh`를 호출하여 변경사항을 전파합니다.
- 로컬에서 테스트할 때는 Hookdeck과 같은 서비스를 사용해서 웹훅을 사용할 수 있습니다.
</aside>

## 도커 이동

<aside>
✍️ **NOTE**

```yaml
services:
	# RabbitMQ
  rabbit:
    image: rabbitmq:3.13-management
    hostname: rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: rabbitmq-diagnostics check_port_connectivity
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 5s
    deploy:
      resources:
        limits:
          memory: 700m
    extends:
      file: common-config.yml
      service: network-deploy-service

	# ConfigServer
  configserver:
    image: "eazybytes/configserver:s6"
    container_name: configserver-ms
    ports:
      - "8071:8071"
    depends_on:
      rabbit:
        condition: service_healthy
    healthcheck:
      test: "curl --fail --silent localhost:8071/actuator/health/readiness | grep UP || exit 1"
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 10s
    extends:
      file: common-config.yml
      service: network-base-config

	# Service 1
  accounts:
    image: "eazybytes/accounts:s6"
    container_name: accounts-ms
    ports:
      - "8080:8080"
    depends_on:
      configserver:
        condition: service_healthy
    environment:
      SPRING_APPLICATION_NAME: "accounts"
    extends:
      file: common-config.yml
      service: microservice-configserver-config

	# Service 2
  loans:
    image: "eazybytes/loans:s6"
    container_name: loans-ms
    ports:
      - "8090:8090"
    depends_on:
      configserver:
        condition: service_healthy
    environment:
      SPRING_APPLICATION_NAME: "loans"
    extends:
      file: common-config.yml
      service: microservice-configserver-config

	# Service 3
  cards:
    image: "eazybytes/cards:s6"
    container_name: cards-ms
    ports:
      - "9000:9000"
    depends_on:
      configserver:
        condition: service_healthy
    environment:
      SPRING_APPLICATION_NAME: "cards"
    extends:
      file: common-config.yml
      service: microservice-configserver-config

networks:
  eazybank:
    driver: "bridge"
```

```yaml
services:
  network-deploy-service:
    networks:
      - eazybank

  microservice-base-config:
    extends:
      service: network-deploy-service
    deploy:
      resources:
        limits:
          memory: 700m
    environment:
      SPRING_RABBITMQ_HOST: "rabbit"

  microservice-configserver-config:
    extends:
      service: microservice-base-config
    environment:
      SPRING_PROFILES_ACTIVE: default
      SPRING_CONFIG_IMPORT: configserver:http://configserver:8071/
```

**Liveness Probes**는 ****컨테이너 또는 애플리케이션이 정상 작동 중인지, 혹은 실패 상태인지를 감지하는 신호를 보냅니다. 

- 컨테이너가 정상 작동 중이라면, 추가적인 조치가 필요 없습니다. 즉, 애플리케이션의 현재 상태가 좋다는 의미입니다.
- 컨테이너가 실패 상태라면, 애플리케이션을 복구하기 위한 시도가 필요하며, 보통은 애플리케이션을 재시작하는 것을 의미합니다.

**Readiness Probes**는 컨테이너나 애플리케이션이 네트워크 트래픽을 받을 준비가 되었는지를 판단하기 위해 사용됩니다.

- 컨테이너가 정상 작동 중이지만, 네트워크 트래픽을 처리할 준비가 안된 상태라면, Readiness Probe는 실패합니다. 이는 준비되지 않은 컨테이너로 트래픽을 보내지 않기 위함입니다.
- 준비되지 않은 컨테이너에 네트워크 트래픽을 성급하게 보내면, 로드 밸런서나 라우터가 클라이언트에게 502 오류를 반환하고 요청을 거부할 수 있습니다.
</aside>