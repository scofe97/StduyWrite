# [Spring MSA] 03-2. 액츄에이터 실습

주제: Spring MSA

- 참고
    
    [6. health — spring-boot-actuator  documentation](http://forward.nhnent.com/hands-on-labs/java.spring-boot-actuator/06-health.html#)
    
    [4. 주요 엔드포인트 — spring-boot-actuator  documentation](http://forward.nhnent.com/hands-on-labs/java.spring-boot-actuator/04-endpoint.html#loggers)
    

# **액추에이터 - health**

---

<aside>
💡 **NOTE**

> *애플리케이션에 문제가 발생했는지 확인하는 앤드포인트!*
> 

[Production-ready Features](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.health.auto-configured-health-indicators)

```yaml
{"status": "UP"}
```

- 헬스 정보는 단순히 애플리케이션이 요청에 응답할 수 있는지 판단한다.
- 애플리케이션이 사용하는 데이터베이스가 응답하는지, 디스크 사용량이 문제가 없는지와 같은 정보들을 포함해서 만들어진다.
</aside>

## 상세보기

<aside>
✍️ **NOTE**

```yaml
management:
 endpoint:
 health:
 show-details: always
```

```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "H2",
        "validationQuery": "isValid()"
      }
    },
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 2000396742656,
        "free": 1813467586560,
        "threshold": 10485760,
        "path": "D:\\study\\Spring\\Spring_final\\start\\do-actuator-start\\.",
        "exists": true
      }
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

</aside>

## 컴포넌트 상태만 보기

<aside>
✍️ **NOTE**

```yaml
management:
 endpoint:
 health:
 show-components: always
```

```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP"
    },
    "diskSpace": {
      "status": "UP"
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

</aside>

## 헬스 이상상태

<aside>
✍️ **NOTE**

```json
{
	 "status": "DOWN",
	 "components": {
			 "db": {
				 "status": "DOWN"
			 },
			 "diskSpace": {
				 "status": "UP"
			 },
			 "ping": {
				 "status": "UP"
		 }
	 }
}
```

</aside>

# 액츄에이터 - info

---

<aside>
💡 **NOTE**

> *실행중인 **애플리케이션의 정보를 알기 위해**서 사용하는 엔드포인트!*
> 

[Production-ready Features](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.endpoints.info.writing-custom-info-contributors)

</aside>

## 기본/env 정보보기

<aside>
✍️ **NOTE**

```yaml
management:
  info:
		# 기본적으로 제공해주는 정보
    java:
      enabled: true
    os:
      enabled: true
    env:
      enabled: true # 커스텀한 정보를 보기위해 true

info:
	# 사용자가 커스텀한 정보
  app:
    name: hello-actuator
    company: yh
```

```json
{
  "app": {
    "name": "hello-actuator",
    "company": "yh"
  },
  "java": {
    "version": "19-ea",
    "vendor": {
      "name": "Oracle Corporation"
    },
    "runtime": {
      "name": "OpenJDK Runtime Environment",
      "version": "19-ea+20-1369"
    },
    "jvm": {
      "name": "OpenJDK 64-Bit Server VM",
      "vendor": "Oracle Corporation",
      "version": "19-ea+20-1369"
    }
  },
  "os": {
    "name": "Windows 10",
    "version": "10.0",
    "arch": "amd64"
  }
}
```

</aside>

## build 정보

<aside>
✍️ **NOTE**

![build.info.properties를 가져옴!](%5BSpring%20MSA%5D%2003-2%20%EC%95%A1%EC%B8%84%EC%97%90%EC%9D%B4%ED%84%B0%20%EC%8B%A4%EC%8A%B5/Untitled.png)

build.info.properties를 가져옴!

```groovy
springBoot {
    buildInfo()
}
```

```json
{
  // ...
  "build": {
    "artifact": "actuator",
    "name": "actuator",
    "time": "2023-04-02T13:46:56.634Z",
    "version": "0.0.1-SNAPSHOT",
    "group": "hello"
  },
	// ...
}
```

- **build-info.properties 코드**
    
    ```yaml
    build.artifact=actuator
    build.group=hello
    build.name=actuator
    build.time=2023-04-02T13\:46\:56.634580900Z
    build.version=0.0.1-SNAPSHOT
    ```
    
</aside>

## git 정보

<aside>
✍️ **NOTE**

![git.properteis를 가져옴!](%5BSpring%20MSA%5D%2003-2%20%EC%95%A1%EC%B8%84%EC%97%90%EC%9D%B4%ED%84%B0%20%EC%8B%A4%EC%8A%B5/Untitled%201.png)

git.properteis를 가져옴!

```groovy
plugins {
	 ...
	 id "com.gorylenko.gradle-git-properties" version "2.4.1" //git 버전작성
}
```

```json
{
  // ...
  "git": {
    "branch": "master",
    "commit": {
      "id": "87c5211",
      "time": "2023-03-17T06:57:52Z"
    }
  },
	// ...
}
```

```yaml
management:
 info:
 git:
 mode: "full"
```

- **git.properties 코드**
    
    ```yaml
    git.branch=master
    git.build.host=DESKTOP-MIP62RP
    git.build.user.email=tscofet@gmail.com
    git.build.user.name=tscofet
    git.build.version=0.0.1-SNAPSHOT
    git.closest.tag.commit.count=
    git.closest.tag.name=
    git.commit.id=87c5211ce5d427a217658361eeb8a0d80c86a56e
    git.commit.id.abbrev=87c5211
    git.commit.id.describe=
    git.commit.message.full=20230317\n
    git.commit.message.short=20230317
    git.commit.time=2023-03-17T15\:57\:52+0900
    git.commit.user.email=tscofet@gmail.com
    git.commit.user.name=scofe97
    git.dirty=true
    git.remote.origin.url=https\://github.com/scofe97/Study.git
    git.tags=
    git.total.commit.count=6
    ```
    
</aside>

# 액츄에이터 - logger

---

<aside>
💡 **NOTE**

> *loggers 엔드포인트를 사용하면 **로깅과 관련된 정보를 확인**하고, 또 **실시간으로 변경**할 수도 있다.*
> 
</aside>

## *LogController 생성*

<aside>
✍️ **NOTE**

```java
@Slf4j
@RestController
public class LogController {

	@GetMapping("/log")
	public String log(){
		log.trace("trace log");
		log.debug("debug log");
		log.info("info log");
		log.warn("warn log");
		log.error("error log");
		return "ok";
	}
}
```

</aside>

## *로그레벨 확인*

<aside>
✍️ **NOTE**

```yaml
logging:
  level:
    hello.controller: debug
```

- `hello.controller` 패키지와 그 하위는 debug 레벨을 출력하도록 함

### 실행결과

```json
// ...
{
	"hello": {
      "effectiveLevel": "INFO"
  },

  "hello.ActuatorApplication": {
    "effectiveLevel": "INFO"
  },

  "hello.controller": {
    "configuredLevel": "DEBUG",
    "effectiveLevel": "DEBUG"
  },

  "hello.controller.LogController": {
    "effectiveLevel": "DEBUG"
  },
}
```

- 로그를 별도로 설정하지 않으면 기본으로 `INFO`를 사용한다.
- 실행결과를 `hello`는 `INFO`, `hello.controller`부터는 `DEBUG`임을 확인할 수 있다.

### 자세히 조회하기

```json
{
  "configuredLevel": "DEBUG",
  "effectiveLevel": "DEBUG"
}
```

- 로거이름을 뒤에 넣으면 해당 부분의 로거정보만 조회가 가능하다.
</aside>

## *실시간 로그 레벨 변경*

<aside>
✍️ **NOTE**

> *개발 서버는 보통 DEBUG로그를 사용하지만, 운영 서버는 DEBUG로 하면 너무 많은 로그를 출력하게되 디스크에 영향을 주게된다.*
> 
- 서버는 중요하다고 판단되는 `INFO`레벨을 사용한다.
- 그런데 서비스 운영중에 문제가 있어서 `DEBUG`나 `TRACE`로그를 남겨야 하는경우 일반적으로는 로깅 설정을 변경하고, 서버를 다시 시작해야 한다.
- loggers엔드포인트를 사용하면 다시 시작하지 않고, 실시간으로 로그 레벨을 변경할 수 있다.

### POST 전달

```json
{
 "configuredLevel": "TRACE"
}
```

```json
{
  "configuredLevel": "TRACE",
  "effectiveLevel": "TRACE"
}
```

</aside>

# 액츄에이터 - httpexchanges

---

<aside>
💡 **NOTE**

> *HTTP 요청과 응답의 과거 기록을 확인하고 싶다면 `httpexchanges` 앤드포인트를 사용하면 된다.*
> 
</aside>

## *InMemoryHttpExchangesRepository 추가*

<aside>
✍️ **NOTE**

```java
@Bean
public InMemoryHttpExchangeRepository httpExchangeRepository() {
    return new InMemoryHttpExchangeRepository();
}
```

- `HttpExchangeRepository` 인터페이스의 구현체를 빈으로 등로갛면 `httpexchanges` 앤드포인트를 사용할 수 있다.
- 스프링 부트는 기본으로 `InMemoryHttpExchangeRepository` 구현체를 제공한다.
</aside>

## *httpexchanges 확인*

<aside>
✍️ **NOTE**

```json
`{
  "exchanges": [
    {
      "timestamp": "2023-04-03T05:23:15.725426400Z",
      "request": {
        "uri": "http://localhost:8080/actuator/httpexchanges",
        "method": "GET",
        "headers": {
          "host": [
            "localhost:8080"
          ],
          "connection": [
            "keep-alive"
          ],
          // ...
```

</aside>