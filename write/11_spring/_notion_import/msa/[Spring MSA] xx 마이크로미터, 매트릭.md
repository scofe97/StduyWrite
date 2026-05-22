# [Spring MSA] xx. 마이크로미터, 매트릭

주제: Spring MSA

- 참고
    
    [[마이크로서비스] 서비스 모니터링 - 엑추에이터, 프로메테우스, 그라파나 (13)](https://velog.io/@hyeokjinon/마이크로서비스-서비스-모니터링-엑추에이터-프로메테우스-그라파나)
    

# 마이크로미터

---

<aside>
💡 **NOTE**

> *마이크로미터는 **애플리케이션 지표를 제공**하는 라이브러리이며, 애플리케이션 지표 수집 활동에 오버헤드가 거의 없도록 설계되었다.*
> 

[](https://micrometer.io/docs)

![JMX → 프로메테우스 변경비용이 너무 커진다..](%5BSpring%20MSA%5D%20xx%20%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EB%AF%B8%ED%84%B0,%20%EB%A7%A4%ED%8A%B8%EB%A6%AD/Untitled.png)

JMX → 프로메테우스 변경비용이 너무 커진다..

- 모니터링 툴을 **JMX → 프로메테우스**로 변경하면 기존에 측정했던 코드들을 모두 변경할 툴에 맞도록 수정해야한다.
- 이를 해결해주는 것이 **마이크로미터 라이브러리**

![JDBC와 비슷한 개념이라 생각 (하나의 인터페이스를 여러 구현체가 사용)](%5BSpring%20MSA%5D%20xx%20%EB%A7%88%EC%9D%B4%ED%81%AC%EB%A1%9C%EB%AF%B8%ED%84%B0,%20%EB%A7%A4%ED%8A%B8%EB%A6%AD/Untitled%201.png)

JDBC와 비슷한 개념이라 생각 (하나의 인터페이스를 여러 구현체가 사용)

- **마이크로미터**는 애플리케이션 메트릭 파사드라고 불리는데, 애플리케이션의 매트릭(측정 지표)을 마이크로미터가 정한 표준 방법으로 모아서 제공해준다,
- 보통은 스프링이 이런 추상화를 제공해주지만, 마이크로미터라는 이미 잘만들어진 추상화가 존재하기에 사용한다.
- 스프링 액츄에이터는 **마이크로미터**를 기본으로 내장해서 사용한다.
</aside>

## 마이크로미터 지원하는 툴

<aside>
✍️ **NOTE**

- CloudWatch
- Datadog
- Elastic
- Influx
- JMX
- Prometheus
- Wavefront
</aside>

# 매트릭

---

<aside>
💡 **NOTE**

> *데이터들을 시각화해서 우리들에게 보여주는 툴*
> 

[Production-ready Features](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html#actuator.metrics.supported)

- 스프링 부트 액츄에이터를 사용하면 수 많은 매트릭(지표)를 편리하게 사용할 수 있다.
</aside>

## metrics 조회

<aside>
✍️ **NOTE**

```json
{
  "names": [
    "application.ready.time",
    "application.started.time",
    "disk.free",
    "disk.total",
    "executor.active",
    "executor.completed",
    "executor.pool.core",
		// ...
	]
}
```

- 액츄에이터가 마이크로미터를 통해서 등록한 기본 매트릭을 확인할 수 있다.
- 내용이 너무 많아서 일부만 가져옴

### 자세히 확인

```json
{
  "name": "jvm.memory.used",
  "description": "The amount of used memory",
  "baseUnit": "bytes",
  "measurements": [
    {
      "statistic": "VALUE",
      "value": 114998624 // 전체 메모리 사용량
    }
  ],
  "availableTags": [
    {
      "tag": "area",
      "values": [
        "heap",
        "nonheap"
      ]
    },
    {
      "tag": "id",
      "values": [
        "G1 Survivor Space",
        "Compressed Class Space",
        "Metaspace",
        "CodeCache",
        "G1 Old Gen",
        "G1 Eden Space"
      ]
    }
  ]
}
```

- 현재 매모리 사용량을 확인할 수 있다.

### tag 필터링

```json
{
  "name": "jvm.memory.used",
  "description": "The amount of used memory",
  "baseUnit": "bytes",
  "measurements": [
    {
      "statistic": "VALUE",
      "value": 37676880 // heap의 메모리
    }
  ],
  "availableTags": [
    {
      "tag": "id",
      "values": [
        "G1 Survivor Space",
        "G1 Old Gen",
        "G1 Eden Space"
      ]
    }
  ]
}
```

- `tag`를 사용해서 특정 데이터만 가져올 수 있다.
</aside>

## HTTP 요청수를 확인

<aside>
✍️ **NOTE**

```json
{
  "name": "http.server.requests",
  "baseUnit": "seconds",
  "measurements": [
    {
      "statistic": "COUNT",
      "value": 24.0 // 요청횟수
    },
    {
      "statistic": "TOTAL_TIME",
      "value": 0.26396369999999997
    },
    {
      "statistic": "MAX",
      "value": 0.0278227
    }
  ],
  "availableTags": [
		// ...
```

- HTTP 요청수에 일부 내용을 필터링 해서 확인한다.
</aside>