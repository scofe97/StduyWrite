# [Spring MSA] 04-2. 서비스 디스커버리(Eureka)

주제: Spring MSA

- 참고
    
    [msaschool - msaschool](https://www.msaschool.io/operation/design/design-six/)
    
    [Spring Cloud Netflix](https://cloud.spring.io/spring-cloud-netflix/reference/html/#netflix-eureka-client-starter)
    
    [4장 서비스 디스커버리](https://develop-yyg.tistory.com/5)
    
    [Spring Cloud OpenFeign](https://spring.io/projects/spring-cloud-openfeign)
    
    [Netflix OSS and Spring Boot — Coming Full Circle](https://netflixtechblog.com/netflix-oss-and-spring-boot-coming-full-circle-4855947713a0)
    

# 서비스 디스커버리

---

<aside>
💡 **NOTE**

> *분산 환경에서 서비스 간 원격 호출을 하려면, 각 서비스의 IP와 포트를 알아야 합니다. 클라우드 기반의 MSA 환경에서는 네트워크가 동적으로 할당되므로, **서비스를 호출하기 위해 서비스 발견 메커니즘(Service Discovery)이 필요합니다.***
> 

`Service Registry`는 `Service Discovery`의 중요한 역할을 하며, 사용가능한 서비스 인스턴스의 목록을 관리하고 서비스 등록/해제/조회 등을 할 수 있는 API를 제공합니다.

![서비스 디스커버리 흐름](%5BSpring%20MSA%5D%2004-2%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%94%94%EC%8A%A4%EC%BB%A4%EB%B2%84%EB%A6%AC(Eureka)/Untitled.png)

서비스 디스커버리 흐름

Service Discovery를 하는 위치에 따라서 구현 방식이 2가지 방식으로 구분됩니다,

1. `Client-Side`
2. `Server-Side`
</aside>

## **Client-Side** Discovery

<aside>
✍️ **NOTE**

> `*Client-Side Discovery`방식은 client가 `Service Registry`에게 물어서 서비스를 찾은 후에 로드밸런싱 알고리즘을 통해 요청하는 방식입니다.*
> 

각 서비스는 실행될 때 `Service Registry`에 자신의 위치(IP, PORT, 서비스명 등)를 등록하고, 종료시에는 `Service Registry`에서 해당 정보를 삭제합니다. 

서비스가 다른 서비스를 호출하려면, `Service Registry`의 Query API를 호출하여 IP와 PORT 등을 확인한 후 호출합니다.

![Client-Side Discvoery](%5BSpring%20MSA%5D%2004-2%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%94%94%EC%8A%A4%EC%BB%A4%EB%B2%84%EB%A6%AC(Eureka)/Untitled%201.png)

Client-Side Discvoery

- 비교적 간단하게 구현할 수 있으며, 호출하려는 서비스를 알고 있기 때문에 서비스에 맞는 로드밸런싱을 각자 구현할 수 있습니다.
- 하지만 각 서비스마다 Service Registry를 구현해야 하는 종속성이 생깁니다.
- 대표적인 기술로는 **Netfilx Eureka**, **Netfilx Ribbon**이 있습니다.
</aside>

## **Server-Side** Discovery

<aside>
✍️ **NOTE**

> `*Service-Side Discovery`는 client가 플랫폼 라우터로 서비스를 호출하여 달라고 요청을 보내는 방식입니다.*
> 

플랫폼 라우터는 `Service Registry`에 query를 하여 서비스의 위치를 찾은 후에 이를 기반으로 라우팅을 진행합니다. `Client-Side Discvoery`와 동일하게 각 서비스는 등록되고 해제됩니다.

대표적인 `Server-Side Discovery`의 기술인 K8s는 `Kube-DNS`에게 Query를 요청하면 `Kube-DNS`는 `etcd`를 조회하여 호출하려는 서비스의 IP와 PORT를 넘겨줍니다.

![Server-Side Discovery 흐름도](%5BSpring%20MSA%5D%2004-2%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%94%94%EC%8A%A4%EC%BB%A4%EB%B2%84%EB%A6%AC(Eureka)/Untitled%202.png)

Server-Side Discovery 흐름도

- `Service-Side Discvoery`는 Discovery 로직을 클라이언트에서 분리할 수 있으며, AWS와 GKS에서는 이와 같은 기능을 무료로 제공하고있습니다.
- Private Cloud 환경에서는 로드밸런서를 직접 생성해줘야 합니다.(MetalLB)
- `Service Discovery`가 죽으면 전체 시스템이 동작하지 않기 때문에 고가용성 등 더 많은 관리가 필요해집니다.
</aside>

# 스프링 서비스 디스커버리(Eureka)

---

<aside>
💡 **NOTE**

> *스프링 클라우드는  Netflix Eureka, Consul, Zookeeper와 같은 Service Registry를 통합하여 `Client-side Discvoery`를 쉽게 구현할 수 있습니다.*
> 

https://github.com/eazybytes/eazybytes-config/blob/main/eurekaserver.yml

```yaml
eureka:
	
	# 유레카 서버 관련 설정 
	server: ...
		
	#	클라이언트가 레지스트리에서 다른 서비스의 정보를 얻을 수 있는 설정
	client: ...
	
	# port, name 등의 현재 eureak 클라이언트의 행동을 재정의
	instance: ...
```

</aside>

## Eureka Server 설정

<aside>
✍️ **NOTE**

```groovy
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-eureka-server'
}
```

```yaml
server:
  port: 8070

eureka:
  instance:
	  # 서버 인스턴스의 호스트 이름
    hostname: localhost
    
  #   
  client:
    # 유레카 서버가 서비스 레지스트리 정보를 가져오지 않음  
    fetchRegistry: false
    # 유레카 서버가 다른 유레카 서버에 자신을 등록하지 않는다.
    registerWithEureka: false
    # 유레카 클라이언트가 유레카 서버와 통신하기 위한 URL
    serviceUrl:
      defaultZone: http://${eureka.instance.hostname}:${server.port}/eureka/
```

```java
@EnableDiscoveryClient
@SpringBootApplication
public class UserServiceApplication {...}
```

</aside>

## Eureka Client 설정

<aside>
✍️ **NOTE**

```groovy
dependencies {
    implementation 'org.springframework.cloud:spring-cloud-starter-netflix-eureka-client'
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}
```

```yaml
spring:
  application:
    name: "cards"

eureka:
  instance:
	  # 호스트 이름 대신 IP사용
    preferIpAddress: true
    
    # 유레카 클라이언트가 자신의 상태를 알리는 주기
    leaseRenewalIntervalInSeconds: 30
    
       
  client:
    # 유레카 서버가 서비스 레지스트리 정보를 가져오지 않음  
    fetchRegistry: true
    
    # 유레카 서버가 다른 유레카 서버에 자신을 등록하지 않는다.
    registerWithEureka: true
    
    # 유레카 클라이언트가 유레카 서버와 통신하기 위한 URL
    serviceUrl:
      defaultZone: http://localhost:8070/eureka
      

 management:
  # info 정보 노출
  info:
    env:
      enabled: true

# http://실행IP&Port/actuator/info      
 info:
  app:
    name: "cards"
    description: "Scofe Bank Card Application"
    version: "1.0.0"
```

![Eureka에 Client 서비스가 등록되었다.](%5BSpring%20MSA%5D%2004-2%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%94%94%EC%8A%A4%EC%BB%A4%EB%B2%84%EB%A6%AC(Eureka)/Untitled%203.png)

Eureka에 Client 서비스가 등록되었다.

![출력값(info 정보) - http://[ip주소]:[port]/actuator/info](%5BSpring%20MSA%5D%2004-2%20%EC%84%9C%EB%B9%84%EC%8A%A4%20%EB%94%94%EC%8A%A4%EC%BB%A4%EB%B2%84%EB%A6%AC(Eureka)/Untitled%204.png)

출력값(info 정보) - http://[ip주소]:[port]/actuator/info

```yaml
server:
	port: 0 # 랜덤포트 설정

eureka:
	# instance id를 다르게해서 여러개 등록이 가능하게함
	instance: ${spring.cloud.client.hostname}:${spring.application.instance.id:${random.value}}
	client:
		register-with-eureka: true
		fetch-registry: true
		sevice-url:
			defaultZone: http://localhost:8070/eureka
```

</aside>

## Eureaka HeartBeat

<aside>
✍️ **NOTE**

> ***Eureka**의 **HeartBeat**기능은 서비스가 Eureka 서버에 지속적으로 자신의 상태를 보고함으로써 자신이 여전히 살아있고 정상적으로 동작한다는 것을 알리는 기능입니다.*
> 

각 서비스 인스턴스는 특정 주기(기본적으로 30초)마다 Eureka 서버에 HTTP 요청을 보냅니다.

Eureka 서버는 일정 시간(기본적으로 90초) 동안 Heartbeat 신호를 받지 못하면 해당 인스턴스를 비정상 상태로 간주하고, 레지스트리에서 제거하거나 불능 상태로 표시합니다.

```yaml
eureka:
  client:
	  # 클라이언트 HeartBeat 주기
    leaseRenewalIntervalInSeconds: 10
    
  instance:
	  # Eureka HeartBeat 최대 대기시간
    leaseExpirationDurationInSeconds: 30
    
    # 상태페이지 경로 (기본 /actuator/info)
    statusPageUrlPath: ${server.servlet.context-path}/actuator/info
    # Heartbeat 경로 (기본 /actuator/health)
    healthCheckUrlPath: ${server.servlet.context-path}/actuator/health
```

- `/info`, `/health`의 앤드포인트의 경우 Actuator을 사용하면 자동으로 생성됩니다.
- 유레카 서버는 `heartbeat` 메시지를 받지 못하면 레지스트리에서 해당 클라이언트를 삭제합니다.
- 클라이언트는 서버로부터 레지스트리 목록을 가져와 캐시하고, 주기적으로 변경사항을 확인합니다.
</aside>

## Eureka 자기보존(Self-Preservation)

<aside>
✍️ **NOTE**

> *Eureka의 자기 보존 모드는 다른 서비스에서 장애가 발생했을 때 Eureka의 가용성을 최대화하기 위한 기능입니다. 이 모드는 서비스의 heartbeat를 일정 기간 동안 수신하지 못하면 활성화됩니다. 자기 보존 모드가 활성화되면, Eureka 서버는 인스턴스의 등록 정보와 상태 정보를 삭제하지 않고 계속 유지합니다.*
> 

**Eureka 서버**가 일정 수 이상의 클라이언트로부터 `Heartbeat`신호를 받지 못하면, **Eureka 서버**는 클라이언트가 모두 비정상 상태가 되었거나, 통신이 불가능해진것으로 판단합니다.

**Eureka 서버**는 일정 시간 동안 수신된 `Heartbeat` 신호의 비율이 설정된 임계값(기본 85%) 아래로 떨어지면, 자기보존 모드를 활성화해서, 상태 정보를 삭제하지 않고 유지합니다. 

문제가 해결되어 `HeartBeat` 신호의 수신 비율이 임계값을 다시 초과하면 자기보존 모드를 해제합니다.

```yaml
eureka:
  server:
    # 인스턴스 제거 작업의 주기 (밀리초 단위)
    eviction-interval-timer-in-ms: 60000 # 60*1000

    # 자기 보존 모드를 활성화하는 임계값 비율 (자가보존 모드 전환 임계값)
    renewal-percent-threshold: 0.85

    # 분당 예상하는 하트비트 수를 계산하는 스케줄러 실행 빈도 (밀리초 단위)
    renewal-threshold-update-interval-ms: 900000 # 15*60*1000

    # 자가보존 모드 활성화 여부
    enable-self-preservation: true
```

- 네트워크 문제로 인해 일시적으로 `Heartbeat`를 보내지 못하는 상황에서도 서비스 인스턴스를 삭제하지 않게 해줍니다.
</aside>