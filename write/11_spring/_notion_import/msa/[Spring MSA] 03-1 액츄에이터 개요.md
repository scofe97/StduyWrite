# [Spring MSA] 03-1. 액츄에이터 개요

주제: Spring MSA
연관 노트: [Devops Study] 08-2. 자율배포 - 모니터링 및 알림 (https://www.notion.so/Devops-Study-08-2-20cf29f1eaf441d48663a632075ec487?pvs=21)

- 참고
    
    [https://incheol-jung.gitbook.io/docs/study/srping-in-action-5th/chap-16](https://incheol-jung.gitbook.io/docs/study/srping-in-action-5th/chap-16).
    
    [[스프링 인 액션] 16. 스프링 부트 액추에이터 사용하기](https://velog.io/@ha0kim/스프링-인-액션-16.-스프링-부트-액추에이터-사용하기)
    

# **액추에이터 개요**

---

<aside>
💡 **NOTE**

> *실행중인 애플리케이션의 **내부를 볼 수 있게하고**, **모니터링**이나 **매트릭(metric)**과 같은 HTTP와 JMX 엔드포인트를 통해 제공한다.*
> 

![다음 이미지 처럼 /actuator/health로 들어가면 정보가 나옴!](%5BSpring%20MSA%5D%2003-1%20%EC%95%A1%EC%B8%84%EC%97%90%EC%9D%B4%ED%84%B0%20%EA%B0%9C%EC%9A%94/Untitled.png)

다음 이미지 처럼 /actuator/health로 들어가면 정보가 나옴!

- 애플리케이션 환경에서 사용할 수 있는 구성 속성들
- 애플리케이션에 포함된 다양한 패키지의 로깅 레벨
- 애플리케이션이 사용 중인 메모리
- 지정된 엔드포인트가 받은 요청 횟수
- 애플리케이션의 건강 상태 정보
</aside>

## *액츄에이터 앤드포인트*

<aside>
✍️ **NOTE**

![상당히 많은 정보를 제공해준다. (이거보다 더 있음)](%5BSpring%20MSA%5D%2003-1%20%EC%95%A1%EC%B8%84%EC%97%90%EC%9D%B4%ED%84%B0%20%EA%B0%9C%EC%9A%94/Untitled%201.png)

상당히 많은 정보를 제공해준다. (이거보다 더 있음)

</aside>

# **액추에이터 사용**

---

<aside>
💡 **NOTE**

> *액츄에이터가 제공하는 프로덕션 준비 기능을 사용하기 위해선 먼저 **라이브러리 추가해야함***
> 

```groovy
//actuator 추가
implementation 'org.springframework.boot:spring-boot-starter-actuator'
```

</aside>

## *액츄에이터 기본 경로 구성*

<aside>
✍️ **NOTE**

```yaml
management:
  endpoints:
    web:
      base-path: /management
```

- 액츄에이터의 모든 엔드포인트 경로에는 `/actuator`가 앞에 붙는다
- 위의 속성을 설정하여 기본경로를 변경할 수 있다.
</aside>

## **액추에이터 엔드포인트의 활성화와 비활성화**

<aside>
✍️ **NOTE**

> *앤드포인트를 활성화 하는것은 해당 기능을 사용할지 안할지 on, off를 선택하는 것이다.
HTTP 혹은 JMX에 노출할지 선택해야하는데 **대부분 HTTP로 한다.***
> 

```yaml
management:
  endpoint:
    shutdown: # 해당 엔드포인트는 보안이슈로 기본적으로 닫힘 (보통은 다 열려있음)
      enabled: true # fasle로 하면 비활성화

  endpoints:
    web:
      exposure:
        include: "*"  # *으로 표기하면 전체
        exclude: "threaddump", "heapdump"
```

- `endpoint.[엔드포인트].enabled=true`
    - 특정 엔드포인트에 대해서 활성화 시킨다
- `web.exposure`
    - `include`를 하면 해당 엔드포인트를 활성화
    - `exclude`를 하면 해당 엔드포인트 비활성화
- `shutdown` 속성을 post로 보내면 웹 애플리케이션이 종료가 된다.
    - `POST /actuator/shutdown`
    - 그래서 기본적으로 비활성화 되어 있음
</aside>