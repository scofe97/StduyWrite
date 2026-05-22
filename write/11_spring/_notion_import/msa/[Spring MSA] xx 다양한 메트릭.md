# [Spring MSA] xx. 다양한 메트릭

주제: Spring MSA

- 참고
    
    

# 다양한 메트릭

---

<aside>
💡 **NOTE**

> *마이크로미터와 액츄에이터가 기본으로 제공하는 다양한 메트릭을 확인해보자!*
> 

[Production-ready Features](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics.supported)

- JVM 메트릭
- 시스템 메트릭
- 애플리케이션 시작 메트릭
- 스프링 MVC 메트릭
- 톰캣 메트릭
- 데이터 소스 메트릭
- 로그 메트릭
- 기타 수 많은 메트릭이 존재한다.
</aside>

## *JVM 메트릭*

<aside>
✍️ **NOTE**

> *JVM 관련 메트릭을 제공하며, `.jvm`으로 시작한다.*
> 

![[http://localhost:8080/actuator/metrics](http://localhost:8080/actuator/metrics) 에서 확인가능](%5BSpring%20MSA%5D%20xx%20%EB%8B%A4%EC%96%91%ED%95%9C%20%EB%A9%94%ED%8A%B8%EB%A6%AD/Untitled.png)

[http://localhost:8080/actuator/metrics](http://localhost:8080/actuator/metrics) 에서 확인가능

- 메모리 및 버퍼 풀 세부 정보
- 가비지 수집 관련 통계
- 스레드 활용
- JVM 버전정보
</aside>

## *시스템 메트릭*

<aside>
✍️ **NOTE**

> `*system`, `process`, `disk`으로 시작한다*
> 

![localhost:8080/actuator/metrics 에서 확인가능](%5BSpring%20MSA%5D%20xx%20%EB%8B%A4%EC%96%91%ED%95%9C%20%EB%A9%94%ED%8A%B8%EB%A6%AD/Untitled%201.png)

localhost:8080/actuator/metrics 에서 확인가능

- CPU 지표
- 파일 디스크립터 메트릭
- 가동 시간 메트릭
- 사용 가능한 디스크 공간
</aside>

## *애플레키에션 시작 메트릭*

<aside>
✍️ **NOTE**

> *애플리케이션 시작 시간 메트릭을 제공한다*
> 

![Untitled](%5BSpring%20MSA%5D%20xx%20%EB%8B%A4%EC%96%91%ED%95%9C%20%EB%A9%94%ED%8A%B8%EB%A6%AD/Untitled%202.png)

- `application.started.time`
    - 애플리케이션을 시작하는데 걸리는 시간
    - ApplicationsStartedEvent로 측정
- `application.ready.time`
    - 애플리케이션이 요청을 처리할 준비가 되는데 걸리는 시간
</aside>

## *스프링 MVC 메트릭*

<aside>
✍️ **NOTE**

> *스프링 MVC 컨트롤러가 처리하는 모든 요청을 다룬다.*
> 

![Untitled](%5BSpring%20MSA%5D%20xx%20%EB%8B%A4%EC%96%91%ED%95%9C%20%EB%A9%94%ED%8A%B8%EB%A6%AD/Untitled%203.png)

- `http.server.requests`
- `TAG`를 사용해서 다음 정보를 분류해서 확인할 수 있다.
    - url
        - 요청 URL
    - methid
        - GET, POST와 같은 HTTP 메서드
    - status
        - 200, 400, 500같은 HTTP Status 코드
    - exception
        - 예외
    - outcome
        - 상태코드를 그룹으로 모아서 확인
</aside>

## *데이터소스 메트릭*

<aside>
✍️ **NOTE**

> *DataSource, 커넥션 풀에 관한 메트릭을 확인할 수 있다.*
> 

![Untitled](%5BSpring%20MSA%5D%20xx%20%EB%8B%A4%EC%96%91%ED%95%9C%20%EB%A9%94%ED%8A%B8%EB%A6%AD/Untitled%204.png)

- `jdbc.connection`으로 시작
- 최대 커넥션, 최소 커넥션, 활성 커넥션, 대기 커넥션 수 등을 확인할 수 있다.
</aside>

## *사용자 정의 매트릭*

<aside>
✍️ **NOTE**

> 사용자가 직접 메트릭을 정의할 수도 있다.
> 
- ex) 주문수, 취소수를 메트릭으로 만들 수 있음
- 사용자 정의 메트릭을 만들기 위해서는 마이크로미터의 사용법을 먼저 이해해야하므로 뒤에서 설명한다.
</aside>