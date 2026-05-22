# [Spring MSA] xx.  프로메테우스, 그라파나

주제: Spring MSA

- 참고
    
    

# 프로메테우스와 그라파나

---

<aside>
💡 **NOTE**

![micrometer → 프로메테우스 → 그라파나](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Untitled.png)

micrometer → 프로메테우스 → 그라파나

1. **스프링 부트 액츄에이터**와 **마이크로미터**를 사용해서 수 많은 메트릭을 자동으로 생성한다.
    - 마이크로미터 프로메테우스 구현체는 프로메테우스가 읽을 수 있는 메트릭을 생성한다.
2. **프로메테우스**는 이렇게 만들어진 메트릭을 지속해서 수집한다.
3. **프로메테우스**는 수집한 메트릭을 내부 DB에 저장한다.
4. 사용자는 **그라파나 대시보드 툴**을 통해 그래프로 편리하게 메트릭을 조회한다. 이때 필요한 데이터는 프로메테우스를 통해서 조회한다.
</aside>

# 프로메테우스

---

<aside>
💡 **NOTE**

> *메트릭을 지속해서 수집하고 DB에 저장하는 툴!*
> 

![프로메테우스 구조도](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Untitled%201.png)

프로메테우스 구조도

### 📌 참고

- 프로메테우스와 그라파나는 내용이 매우 방대해 자세한 내용을 다루지는 않는다.
- 각각의 기술들을 어떻게 다루고 활용해야 하는지, 기초 내용과 올바른 방향을 설명하는데 초점을 맞춘다.
</aside>

## 설치

<aside>
✍️ **NOTE**

### 윈도우(설치 링크)

[https://github.com/prometheus/prometheus/releases/download/v2.42.0/prometheus-2.42.0.windows-amd64.zip](https://github.com/prometheus/prometheus/releases/download/v2.42.0/prometheus-2.42.0.windows-amd64.zip)

![Group 1.png](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Group_1.png)

- 설치이후 `prometheus`를 통해 프로메테우스를 실행한다.

![설치이후 9090포트로 들어가면 접속가능](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Untitled%202.png)

설치이후 9090포트로 들어가면 접속가능

</aside>

## 애플리케이션 설정

<aside>
✍️ **NOTE**

```groovy
implementation 'io.micrometer:micrometer-registry-prometheus'
```

- 설치이후 `prometheus`를 통해 프로메테우스를 실행한다.

```groovy
# HELP tomcat_global_request_seconds  
# TYPE tomcat_global_request_seconds summary
tomcat_global_request_seconds_count{name="http-nio-8080",} 3.0
tomcat_global_request_seconds_sum{name="http-nio-8080",} 1.076
# HELP executor_active_threads The approximate number of threads that are actively executing tasks
# TYPE executor_active_threads gauge
executor_active_threads{name="applicationTaskExecutor",} 0.0
# HELP jvm_memory_used_bytes The amount of used memory
# TYPE jvm_memory_used_bytes gauge
jvm_memory_used_bytes{area="heap",id="G1 Survivor Space",} 4291312.0
jvm_memory_used_bytes{area="heap",id="G1 Old Gen",} 2.3995904E7
jvm_memory_used_bytes{area="nonheap",id="Metaspace",} 5.6625224E7
jvm_memory_used_bytes{area="nonheap",id="CodeCache",} 1.0783872E7
jvm_memory_used_bytes{area="heap",id="G1 Eden Space",} 4194304.0
jvm_memory_used_bytes{area="nonheap",id="Compressed Class Space",} 7743424.0
# HELP jdbc_connections_max Maximum number of active connections that can be allocated at the same time.
# TYPE jdbc_connections_max gauge
jdbc_connections_max{name="dataSource",} 10.0

// ...
```

- 액츄에이터에 프로메테우스 매트릭 수집 앤드포인트가 자동으로 추가됨!
- 모든 메트릭이 프로메테우스 포맷으로 만들어 진 것을 확인할 수 있다.

### 포맷차이

- `jvm.info` → `jvm_info`
    - 프로메테우스는 `.` 대신에 `_` 포맷을 사용한다.
    - 자동으로 `.`에서 `_`로 변환된것을 확인할 수 있다.
- `http.server.request`
    - 이 매트릭은 내부에 요청수, 시간 합, 최대 시간 정보를 가지고 있었다.
    - 프로메테우스에서는 다음 3가지로 분리된다.
        - `http_server_requests_seconds_count`
            - 요청 수
        - `http_server_requests_seconds_sum`
            - 시간 합(요청수의 시간을 합함)
        - `http_server_requests_seconds_max`
            - 최대 시간(가장 오래걸린 요청 수)
</aside>

## 수집 설정

<aside>
✍️ **NOTE**

> *프로메테우스가 애플리케이션의 `/actuator/prometheus`를 호출해서 메트릭을 주기적으로 수집하도록 설계한다.*
> 

![Group 1.png](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Group_1%201.png)

```yaml
global:
  scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

	- job_name: "spring-actuator"
    metrics_path: "/actuator/prometheus"
    scrape_interval: 3s
    static_configs:
      - targets: ['localhost:8080']
```

- **job_name**
    - 수집하는 이름이다. (임의의 이름 사용)
- **metrics_path**
    - 수집할 경로를 지정한다.
- **scapre_interval**
    - 수집할 주기를 결정한다.
- **targets**
    - 수집할 서버의 IP, PORT를 지정한다.

### 연동 확인

![다음과 같이 spring-actuator가 추가됨을 확인가능](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Untitled%203.png)

다음과 같이 spring-actuator가 추가됨을 확인가능

### 데이터 조회

![jvm_info 검색한 결과](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Untitled%204.png)

jvm_info 검색한 결과

</aside>

## 기본 기능

<aside>
✍️ **NOTE**

![프로메테우스 검색결과를 자세히 보자](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Group_1%202.png)

프로메테우스 검색결과를 자세히 보자

- **태그, 레이블**
    - `error`, `exception`, `instance`, `job`, `method`, `outcome`, `status`, `url`
    - 각각의 매트릭 정보를 구분해서 사용하기 위한 태그이다.
    - **마이크로미터**에서는 이것을 **태그(Tag)**라 하고, **프로메테우스**에서는 **레이블(Label)**이라 한다.
- 숫자
    - 마지막에 보면 `1`, `56`와 같은 숫자가 보이는데 이 숫자가 바로 해당 메트릭의 값이다.

- `Table`
    - Evaluation time을 수정해서 과거 시간 조회 가능
- `Graph`
    - 메트릭을 그래프로 조회 가능
</aside>

## 필터 기능

<aside>
✍️ **NOTE**

![http_server_requests_seconds_count{uri="/log", method="GET"} 검색 예시](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Group_1%203.png)

http_server_requests_seconds_count{uri="/log", method="GET"} 검색 예시

- 레이블을 기준으로 필터를 사용할 수 있다. (중괄호 `{}`문법 사용)

### 레이블 일치 연산자

- `=`
    - 제공된 문자열과 정확히 동일한 레이블 선택
    - ex) `http_server_requests_seconds_count{uri="/log", method="GET"}`
- `≠`
    - 제공된 문자열과 같지 않은 레이블 선택
    - ex) `http_server_requests_seconds_count{uri!="/actuator/prometheus"}`
- `=~`
    - 제공된 문자열과 정규칙 일치하는 레이블 선택
    - ex) `http_server_requests_seconds_count{method=~"GET|POST"}`
- `!~`
    - 제공된 문자열과 정규식 일치하지 않는 레이블 선택
    - ex) `http_server_requests_seconds_count{uri!~"/actuator.*"}`
</aside>

## 연산자 쿼리 함수

<aside>
✍️ **NOTE**

![http_server_requests_seconds_count{uri="/log", method="GET"} 검색 예시](%5BSpring%20MSA%5D%20xx%20%ED%94%84%EB%A1%9C%EB%A9%94%ED%85%8C%EC%9A%B0%EC%8A%A4,%20%EA%B7%B8%EB%9D%BC%ED%8C%8C%EB%82%98/Group_1%203.png)

http_server_requests_seconds_count{uri="/log", method="GET"} 검색 예시

</aside>