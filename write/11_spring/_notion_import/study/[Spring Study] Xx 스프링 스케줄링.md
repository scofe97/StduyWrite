# [Spring Study] Xx. 스프링 스케줄링

주제: Spring Study

- 참고
    
    [Spring Boot 환경의 Quartz Scheduler 활용](https://velog.io/@park2348190/Spring-Boot-환경의-Quartz-Scheduler-활용)
    
    [[Java] 스케줄링 & Spring Boot Quartz 이해하고 적용하기 -1 : 설정 및 간단예시](https://adjh54.tistory.com/170#1.%20%ED%85%8C%EC%8A%A4%ED%8A%B8%20%EA%B0%9C%EB%B0%9C%ED%99%98%EA%B2%BD-1)
    
    [Scheduling in Spring with Quartz | Baeldung](https://www.baeldung.com/spring-quartz-schedule)
    
    [quartz/examples/src/main/java/org/quartz/examples at main · quartz-scheduler/quartz](https://github.com/quartz-scheduler/quartz/tree/main/examples/src/main/java/org/quartz/examples)
    
    [Quartz Job Scheduler란?](https://advenoh.tistory.com/51)
    
    [https://wouldyou.tistory.com/94#google_vignette](https://wouldyou.tistory.com/94#google_vignette)
    
    [https://github.com/HomoEfficio/dev-tips/blob/master/Spring 1.5.* - Quartz Scheduler 연동.md](https://github.com/HomoEfficio/dev-tips/blob/master/Spring%201.5.*%20-%20Quartz%20Scheduler%20%EC%97%B0%EB%8F%99.md)
    
    [@Scheduled를 대체한 Quartz (v2)](https://velog.io/@choizz/팀-프로젝트에서-정기-결제-구현-Quartz.-v2)
    
    [spring quartz | D-log](https://leejaedoo.github.io/spring_quartz/#google_vignette)
    
    [[Quartz-3] Multi WAS 환경을 위한 Cluster 환경의 Quartz Job Scheduler 구현](https://blog.advenoh.pe.kr/spring/Multi-WAS-환경을-위한-Cluster-환경의-Quartz-Job-Scheduler-구현/)
    

# Batch와 Scheduler의 차이

---

<aside>
💡 **NOTE**

> ***배치**와 **스케줄러**는 자동화된 작업 수행에 필수적인 개념이지만, 두 개념은 서로 다릅니다. 스케줄러는 일정한 간격으로 반복 작업을 수행하는 반면, 배치는 대량의 데이터 처리 작업을 자동화하는 프로그램을 가리킵니다.*
> 

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled.png)

- **배치 프로그램**은 **일괄 처리를 위한 프로그램**이며, 사용자의 명령에 따라 실행됩니다. 주로 대량의 로그 처리나 정기적인 업데이트에 사용됩니다.
- **스케줄러**는 **정해진 시간에 자동으로 실행되는 프로그램**으로, 주기적으로 실행되는 작업을 설정할 수 있습니다. 주로 주기적인 백업이나 정기적인 데이터 처리에 사용됩니다.
</aside>

## Java에서의 스케줄링

<aside>
✍️ **NOTE**

> *Java에서는 기본적으로 스케줄링 기능을 제공하고 있습니다. 대표적으로 `java.util.Timer`와 `ScheduledExecutorService`가 있습니다.*
> 

`java.util.Timer`는 `TimerTask` 객체를 스케줄링 하는데 사용되며 `TimerTask` 객체는 `Timer` 클래스가 실행되는 스레드에서 실행되며 주어진 시간 이후에 수행됩니다.

```java
@Test
void timer() throws InterruptedException {
		// Timer 생성
    Timer timer1 = new Timer();
    Timer timer2 = new Timer();

		// task11, task12 생성
    TimerTask task11 = new TimerTask() {
        // 실행하는 작업
        @Override
        public void run() {
            System.out.println("작업1-1 수행! " + Thread.currentThread());
        }
    };
    TimerTask task12 = new TimerTask() {
        // 실행하는 작업
        @Override
        public void run() {
            System.out.println("작업1-2 수행! " + Thread.currentThread());
        }
    };

		// task21, task22 생성
    TimerTask task21 = new TimerTask() {
        // 실행하는 작업
        @Override
        public void run() {
            System.out.println("작업2-1 수행! " + Thread.currentThread());
        }
    };

    TimerTask task22 = new TimerTask() {
        // 실행하는 작업
        @Override
        public void run() {
            System.out.println("작업2-2 수행! " + Thread.currentThread());
        }
    };

		// Timer1 - task11, task12 할당 
    timer1.schedule(task11, 5000); // 5초 후에 작업 수행
    timer1.schedule(task12, 5000, 2000); // 5초 후에 첫 작업을 수행하고, 이후 2초마다 반복

		// Timer2 = task21, task22 할당
    timer2.schedule(task21, 5000); // 5초 후에 작업 수행
    timer2.schedule(task22, 5000, 2000); // 첫 작업 수행 시간과 이후 2초마다 반복

    TimeUnit.SECONDS.sleep(10);
}
```

![TimerTask - Timer (1대다), 싱글 스레드](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%201.png)

TimerTask - Timer (1대다), 싱글 스레드

- Timer는 반복 작업을 간편하게 처리하는 방법을 제공하지만, 대규모 병렬 처리나 복잡한 스케줄링 요구사항을 충족시키는 데에는 한계가 있습니다.

`ScheduledExecutor`는 `java.util.concurrent` 패키지에서 제공되며, Java에서 스케줄러를 사용하기 위한 보다 고급 인터페이스 입니다. `Timer`보다 더 세밀한 제어와 복잡한 스케줄링, 복수의 작업을 관리할 수 있게 됩니다.

```java
@Test
void scheduler() throws InterruptedException {
		// 스레드 풀 3 설정
    ScheduledExecutorService executor = Executors.newScheduledThreadPool(3);
    
    // 작업 생성
    // 스레드 할당을 위해 1초씩 시간을 할당한다.
    Runnable task1 = () -> {
        System.out.println("작업1 실행! " + Thread.currentThread());
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("작업1 중단");
        }
    };
    Runnable task2 = () -> {
        System.out.println("작업2 실행! " + Thread.currentThread());
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("작업2 중단");
        }
    };
    Runnable task3 = () -> {
        System.out.println("작업3 실행! " + Thread.currentThread());
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            System.out.println("작업3 중단");
        }
    };

    executor.schedule(task1, 5, TimeUnit.SECONDS); // // 5초 후에 작업 실행
    executor.scheduleAtFixedRate(task2, 5, 2, TimeUnit.SECONDS); // 첫 작업 실행 후, 2초 간격으로 반복 실행
    executor.scheduleWithFixedDelay(task3, 5, 2, TimeUnit.SECONDS); // 첫 작업 실행 후, 이전 작업 완료 후 2초 간격으로 반복 실행

    TimeUnit.SECONDS.sleep(10);
    executor.shutdown();
}
```

![Task - ScheduledExecutorService (스레드 풀 사용시 병렬)](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%202.png)

Task - ScheduledExecutorService (스레드 풀 사용시 병렬)

</aside>

# Spring Quartz란 무엇인가?

---

<aside>
💡 **NOTE**

> *Spring Quartz는 Java기반의 강력한 오픈소스 작업 스케줄링 라이브러리이며 복잡한 스케줄링 요구사항을 구현할 수 있습니다.*
> 

Quartz의 스케줄링은 Job, Trigger, Scheduler라는 3가지 구성요소로 구성되어 있습니다.

- Job: 실행할 작업에 대한 정보를 포함하며, 실제 작업 내용은 Job 인터페이스의 execute() 메소드를 통해 구현합니다.
- Trigger: 작업이 언제 및 어떤 주기로 실행될지를 결정합니다. SimpleTrigger와 CronTrigger 등이 사용 가능합니다.
- Scheduler: Job과 Trigger를 결합하여 작업 실행을 관리합니다.
</aside>

## Job

<aside>
✍️ **NOTE**

> `*Job`은 스케줄러에서 실행되어야 하는 작업을 정의하는 인터페이스 입니다.*
> 

```java
public class MyJob implements Job {
    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        JobDataMap dataMap = context.getJobDetail().getJobDataMap();

        String email = dataMap.getString("email");
        String filePath = dataMap.getString("filePath");

        System.out.println("email = " + email);
        System.out.println("filePath = " + filePath);
    }
}
```

`Job` 인터페이스를 구현한 후에는 `JobDetail` 객체를 생성해야 합니다. `JobDetail`은 `Job` 인스턴스와 그 실행에 필요한 추가 정보를 포함하고 있습니다.

```java
JobDetail jobDetail = JobBuilder.newJob(MyJob.class)
      .withIdentity("myJob", "group1") // 키 설정
      .usingJobData("email", "user@example.com") // 이메일 주소 설정
      .usingJobData("filePath", "/path/to/file") // 파일 경로 설정
      .build();
```

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%203.png)

```java
// JobDetail 함수
JobKey jobKey = jobDetail.getKey(); // Job의 Key 조회

String description = jobDetail.getDescription(); // Job의 설명 조회

Class<? extends Job> jobClass = jobDetail.getJobClass(); // Job의 구현 클래스 조회

JobDataMap dataMap = jobDetail.getJobDataMap(); // Job의 data map 조회

boolean isDurable = jobDetail.isDurable(); // Job의 지속성 조회

boolean isPersistJobDataAfterExecution = jobDetail.isPersistJobDataAfterExecution(); // Job 실행 후 data map 지속 저장 여부 조회

boolean isConcurrentExecutionDisallowed = jobDetail.isConcurrentExectionDisallowed(); // 동시 실행 금지 여부 조회

boolean requestsRecovery = jobDetail.requestsRecovery(); // 실패 시 재실행 요청 여부 조회
```

</aside>

## Trigger

<aside>
✍️ **NOTE**

> *Trigger는 스케줄링 작업의 실행 시간을 결정하는 요소 이며 크게 SimpleTrigger, CronTrigger 유형이 있습니다.*
> 

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%204.png)

- `SimpleTrigger`: 특정 시간에 주기적으로 작업을 실행하며 실행 주기와 반복 횟수를 설정할 수 있습니다.
- `CronTrigger`: cron 표현식을 사용하여 복잡한 스케줄링 요구 사항을 정의할 수 있습니다. 주간, 월간, 연간 반복 작업 등 다양한 시간 기반 스케줄링이 가능합니다.

`Trigger`를 쉽게 생성하기 위해 `TriggerBuilder`를 사용할 수 있습니다. `TriggerBuilder`는 유연한 API를 제공하여 작업 실행 시간, 반복 주기, 우선 순위 등 다양한 옵션을 설정할 수 있게 합니다.

```java
Trigger trigger = TriggerBuilder.newTrigger()
		// 트리거 식별자 설정
    .withIdentity("complexTrigger", "group1")
    
    // 실행할 JobDetail 지정
    .forJob(jobDetail)
    
    // 현재로부터 10분 후 시작
    .startAt(DateBuilder.futureDate(10, DateBuilder.IntervalUnit.MINUTE))
    
    // 매 30초마다 실행하는 크론 스케줄
    .withSchedule(CronScheduleBuilder.cronSchedule("0/30 * * * * ?"))
    
    // 시작 후 1시간 동안만 유효
    .endAt(DateBuilder.futureDate(1, DateBuilder.IntervalUnit.HOUR))
    
    // JobDataMap에 데이터 추가
    .usingJobData("myKey", "myValue") 
    
    // 우선순위 설정
    .withPriority(5)
    
    // 사용할 달력 이름 설정 (예: 공휴일 제외)
    .modifiedByCalendar("myCalendar")
    .build();
```

- Trigger를 생성할때는 Date값을 받습니다. 기본적으로 java.util.Date 인스턴스는 불변성을 보장하지 않지만, DateBuilder를 사용해서 관리하면 최대한 비슷하게 만들 수 있습니다.

```java
Trigger trigger = TriggerBuilder.newTrigger()
    .withIdentity("simpleTrigger", "group1")
    .startNow()
    .withSchedule(SimpleScheduleBuilder.simpleSchedule()
        .withIntervalInSeconds(60) // 60초 간격
        .withRepeatCount(5) // 총 5회 반복
        .withMisfireHandlingInstructionFireNow()) // misfire 발생 시 즉시 실행
    .build();
```

```java
Trigger cronTrigger = TriggerBuilder.newTrigger()
    .withIdentity("weeklyTrigger", "group1")
    .withSchedule(CronScheduleBuilder.cronSchedule("0 30 10 ? * MON")) // 매주 월요일 오전 10:30에 실행
    .build();
```

</aside>

## Scheduler

<aside>
✍️ **NOTE**

> `*Scheduler`는 `Job`과 `Trigger`를 등록하여 스케줄링을 하며, 작업 실행주기를 관리하고 특정 작업을 삭제하거나 수정할 수 있습니다.*
> 

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%205.png)

`Scheduler`는 스프링을 사용하지 않는 경우, `StdSchedulerFactroy`를 통해 인스턴스를 생성합니다. `getDefaultScheduler()` 메소드를 호출하면 기본 설정으로 `Scheduler` 인스턴스를 얻을 수 있습니다.

```java
// 스케줄러 생성
Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();

// 스케줄러 시작
scheduler.start();

// 스케줄러에 Job과 Trigger 등록
scheduler.scheduleJob(jobDetail, trigger);

// 특정 Job 삭제
scheduler.deleteJob(job.getKey());

// 스케줄러 종료
scheduler.shutdown();
```

Spring Framework에서는 `StdScheduleFactory`를 사용하는 것 보다는, `SchedulerFactoryBean`을 사용하는 것이 더 좋습니다. `SchedulerFactoryBean`은 의존성 주입, 트랜잭션, AOP, 이벤트 리스너등을 효율적으로 사용할 수 있습니다.

```java
@Bean
public SchedulerFactoryBean schedulerFactoryBean(Trigger trigger, @Qualifier("printJob") JobDetail jobDetail){
    SchedulerFactoryBean schedulerFactory = new SchedulerFactoryBean();

    // 스프링 애플리케이션 시작 시 스케줄러 자동 시작 설정
    schedulerFactory.setAutoStartup(true);

    // 스케줄러 시작 지연 시간 설정 (예: 애플리케이션 시작 후 10초 후에 스케줄러 시작)
    schedulerFactory.setStartupDelay(1);

		// 설정파일 적용
    schedulerFactory.setQuartzProperties(quartzProperties());

    return schedulerFactory;
}

private Properties quartzProperties() {
    PropertiesFactoryBean propertiesFactoryBean = new PropertiesFactoryBean();
    propertiesFactoryBean.setLocation(new ClassPathResource("quarts.properties"));
    Properties properties = null;
    try {
        propertiesFactoryBean.afterPropertiesSet();
        properties = propertiesFactoryBean.getObject();
    } catch (IOException e) {
        throw new RuntimeException(e);
    }
    return properties;
}
```

```bash
# 스케줄러 기본 설정
org.quartz.scheduler.instanceName=MyScheduler   # 스케줄러의 고유한 이름을 설정합니다.
org.quartz.scheduler.instanceId=AUTO            # 스케줄러 인스턴스의 ID를 설정합니다. 'AUTO'로 설정 시, 자동으로 생성됩니다.

# 스레드 풀 설정
org.quartz.threadPool.class=org.quartz.simpl.SimpleThreadPool  # 사용할 스레드 풀의 구현 클래스를 설정합니다.
org.quartz.threadPool.threadCount=3                            # 스레드 풀에서 관리할 스레드의 수를 설정합니다.
org.quartz.threadPool.threadPriority=5                         # 생성된 스레드의 우선순위를 설정합니다.

# JobStore 설정
org.quartz.jobStore.class=org.quartz.simpl.RAMJobStore  # Job 정보를 저장할 JobStore의 구현 클래스를 설정합니다. RAMJobStore는 모든 정보를 RAM에 저장합니다.

# JobStore 관련 추가 설정 (예시)
org.quartz.jobStore.misfireThreshold=60000  # Job 미스파이어 처리를 위한 임계값을 설정합니다. 단위는 밀리초(ms)입니다.

# 클러스터 설정 (예시)
org.quartz.jobStore.isClustered=false       # 스케줄러 클러스터링 여부를 설정합니다. 기본값은 'false'입니다.
org.quartz.jobStore.clusterCheckinInterval=20000  # 클러스터 노드 간 체크인 간격을 설정합니다. 단위는 밀리초(ms)입니다.

# 플러그인 설정 (예시)
org.quartz.plugin.shutdownHook.class=org.quartz.plugins.management.ShutdownHookPlugin  # 스케줄러 종료 시 실행할 플러그인 클래스를 설정합니다.
org.quartz.plugin.shutdownHook.cleanShutdown= true  # 스케줄러가 정상 종료될 때 모든 Job이 완료될 때까지 대기할지 여부를 설정합니다.
```

### 스케줄러 등록방법

```java
// Job이 등록되어있는 경우
if(Objects.isNull(scheduler.getJobDetail(jobKey)))
    scheduler.scheduleJob(jobDetail, lastTrigger);
    
// Job이 등록되어있지 않은 경우    
else
    scheduler.scheduleJob(lastTrigger);

```

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%206.png)

</aside>

## Listener

<aside>
✍️ **NOTE**

> *Quartz는 `JobListnet`와, `TriggerListner`와 같은 리스너를 활용하여 작업의 생명 주기와 트리거 이벤트를 세밀하게 관리할 수 있습니다.*
> 

`JobListener` 는 Job의 생명 주기 동안 발생하는 다양한 이벤트를 감지하고, 이에 대응하는 로직을 수행할 수 있게 해줍니다.

```java
@Component
public class JobsListener implements JobListener {
    
    @Override
    public String getName() {
        return "myJobListener";
    }

    @Override
    public void jobToBeExecuted(JobExecutionContext context) {
        System.out.println("Job 실행되기 이전에 수행됩니다.");
    }

    @Override
    public void jobExecutionVetoed(JobExecutionContext context) {
        System.out.println("Job 실행이 실패하였을때 수행됩니다.");
    }

    @Override
    public void jobWasExecuted(JobExecutionContext context, JobExecutionException jobException) {
        System.out.println("Job 실행 이후에 수행됩니다.");
    }
}
```

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%207.png)

`TriggerListener`는 트리거 이벤트 발생시 호출되는 메서드를 제공합니다. 이 리스너를 통해 트리거가 발동을 감지하고 대응 로직을 수행할 수 있게 해줍니다.

```java
@Component
public class TriggersListener implements TriggerListener {
    @Override
    public String getName() {
        // 리스너의 이름을 반환합니다. 이 이름은 리스너를 식별하는 데 사용됩니다.
        return "MyTriggerListener";
    }

    @Override
    public void triggerFired(Trigger trigger, JobExecutionContext context) {
        // 트리거가 발동됐을 때 호출됩니다.
        System.out.println("Trigger fired: " + trigger.getKey());
    }

    @Override
    public boolean vetoJobExecution(Trigger trigger, JobExecutionContext context) {
        // 작업 실행 여부를 결정합니다. true를 반환하면 작업 실행이 거부됩니다.
        return false;
    }

    @Override
    public void triggerMisfired(Trigger trigger) {
        // 미발동된 트리거에 대해 호출됩니다.
        System.out.println("Trigger misfired: " + trigger.getKey());
    }

    @Override
    public void triggerComplete(Trigger trigger, JobExecutionContext context,
                                Trigger.CompletedExecutionInstruction triggerInstructionCode) {
        // 트리거 작업이 완료된 후 호출됩니다.
        System.out.println("Trigger completed: " + trigger.getKey());
    }
}
```

![Untitled](%5BSpring%20Study%5D%20Xx%20%EC%8A%A4%ED%94%84%EB%A7%81%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81/Untitled%208.png)

```java
schedulerFactory.setGlobalJobListeners(jobsListener); // JobListener 등록
schedulerFactory.setGlobalTriggerListeners(triggersListener); // TriggerListner 등록
```

</aside>

# Spring Quarts 실습

---

<aside>
💡 **NOTE**

```java
@Slf4j
public class NormalJob implements Job {

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        JobKey key = context.getJobDetail().getKey();

        System.out.println("NormalJob key = " + key);
    }
}
```

```java
@Component
public class JobDetailService {

    public JobDetail serviceBuild(JobKey jobKey) {

        JobDataMap jobDataMap = new JobDataMap();
        jobDataMap.put("data1", "data1");
        jobDataMap.put("data2", "data2");
        jobDataMap.put("data3", "data3");

        return JobBuilder.newJob(NormalJob.class)
                .withIdentity(jobKey.getName(), jobKey.getGroup())
                .usingJobData(jobDataMap)
                .build();
    }
}
```

```java
@Slf4j
@Service
public class TriggerService {
    public Trigger everySeconds(JobKey jobKey) {
        return TriggerBuilder.newTrigger()
                .forJob(jobKey)
                .withIdentity(jobKey.getName())
                .withSchedule(CronScheduleBuilder.cronSchedule("0/10 * * * * ?"))
                .build();
    }
}
```

```java
@Configuration
@RequiredArgsConstructor
public class QuartzConfig {

    private final JobsGlobalListener jobsGlobalListener;
    private final TriggersGlobalListener triggersGlobalListener;

    @Bean
    public SchedulerFactoryBean schedulerFactoryBean() {
        SchedulerFactoryBean schedulerFactory = new SchedulerFactoryBean();

        // 스프링 애플리케이션 시작 시 스케줄러 자동 시작 설정
        schedulerFactory.setAutoStartup(true);

        // 스케줄러 시작 지연 시간 설정 (예: 애플리케이션 시작 후 10초 후에 스케줄러 시작)
        schedulerFactory.setStartupDelay(1);

        // 설정 적용
        schedulerFactory.setQuartzProperties(quartzProperties());

				// 리스너 적용
        schedulerFactory.setGlobalJobListeners(jobsGlobalListener);
        schedulerFactory.setGlobalTriggerListeners(triggersGlobalListener);

        return schedulerFactory;
    }

		// 프로퍼티 설정
    private Properties quartzProperties() {
        PropertiesFactoryBean propertiesFactoryBean = new PropertiesFactoryBean();
        propertiesFactoryBean.setLocation(new ClassPathResource("quarts.properties"));
        Properties properties = null;
        try {
            propertiesFactoryBean.afterPropertiesSet();
            properties = propertiesFactoryBean.getObject();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return properties;
    }
}

```

```java
@Service
@RequiredArgsConstructor
public class SubscriptionService {
    private final Scheduler scheduler;
    private final TriggerService triggerService;
    private final JobDetailService jobDetailService;
    
    private final TriggersGlobalListener triggersGlobalListener;
    private final JobsListener jobsListener;

    @PostConstruct
    public void init() throws SchedulerException {
        startSchedule();

        ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);
        executor.schedule(this::resetNormalSchedule, 5, TimeUnit.SECONDS);
    }

    public void startSchedule() {
        // 일반 잡
        applyNormalSchedule(JobKey.jobKey("normal Key111",  "normal Group" ));
        applyNormalSchedule(JobKey.jobKey("normal Key222",  "normal Group"));
        // applyNormalSchedule(JobKey.jobKey("normal Key3", "normal Group"));

        // 특정 JobDetail에 대한 JobListener 등록
        KeyMatcher<JobKey> exampleJob1Matcher = KeyMatcher.keyEquals(JobKey.jobKey("normal Key111", "normal Group"));
        KeyMatcher<TriggerKey> exampleJob1TriggerMatcher = KeyMatcher.keyEquals(TriggerKey.triggerKey("normal Key1"));

        try {
            scheduler.getListenerManager().addJobListener(jobsListener, exampleJob1Matcher);
            scheduler.getListenerManager().addTriggerListener(triggersGlobalListener, exampleJob1TriggerMatcher);
        } catch (SchedulerException e) {
            throw new RuntimeException(e);
        }
    }

    private void applyNormalSchedule(JobKey jobKey){
        System.out.println("jobKey = " + jobKey.getName());
        JobDetail jobDetail = jobDetailService.serviceBuild(jobKey);
        Trigger trigger = triggerService.everySeconds(jobKey);

        schedule(jobDetail, trigger);
    }

    private void applyErrorSchedule(){
        JobKey jobKey = JobKey.jobKey("error Key", "error Group");
        JobDetail jobDetail = jobDetailService.errorBuild(jobKey);
        Trigger trigger = triggerService.everySeconds(jobKey);
        schedule(jobDetail, trigger);
    }

    private void resetNormalSchedule(){
        startSchedule();
        deleteNormalSchedule();
    }

    private void deleteNormalSchedule(){
        try {
            scheduler.deleteJob(JobKey.jobKey("normal Key111", "normal Group"));
        } catch (SchedulerException e) {
            throw new RuntimeException(e);
        }
    }

    private void schedule(JobDetail jobDetail, Trigger lastTrigger) {
        try {
            scheduler.scheduleJob(jobDetail, lastTrigger);
        } catch (SchedulerException e) {
            JobExecutionException jobExecutionException = new JobExecutionException(e);
            jobExecutionException.setRefireImmediately(true);
        }
    }
}
```

</aside>

## **@PersistJobDataAfterExecution, @DisallowConcurrentExecution**

<aside>
✍️ **NOTE**

> *Quartz의 작업은 기본적으로 상태가 없다(stateless)고 가정하며, 작업이 실행될 때마다 `JobDataMap`의 데이터를 유지하지 않습니다.*
> 

만약 `JobData`의 데이터를 유지하고 다음 실행에 사용하고 싶은 경우 `@PersistJobDataAfterExecution`을 사용하여 작업 실행마다 `JobDataMap`에 저장된 데이터를 유지하게 할 수 있습니다.

```java
@PersistJobDataAfterExecution
public class StatefulJob implements Job {
    public void execute(JobExecutionContext context) throws JobExecutionException {
        JobDataMap dataMap = context.getJobDetail().getJobDataMap();
        int count = dataMap.getInt("count");
        count++;
        dataMap.put("count", count);
        System.out.println("Job is running for the " + count + " time");
    }
}
```

하지만 상태를 가지는 작업은 항상 스레드 문제가 발생합니다. 만약 동일한 작업을 여러 트리거로 등록해서 사용하게한다면 `race Condition`문제가 발생할 수 있습니다.

```java
private void applyStatefulSchedule() {
    JobKey jobKey = JobKey.jobKey("stateful key1", "stateful group");
    JobDetail jobDetail = jobDetailService.statefulBuild(jobKey);

		// 10초마다 실행한다.
    TriggerKey triggerKey = TriggerKey.triggerKey("stateful key1", "stateful group");
    Trigger trigger = triggerService.everySeconds(jobKey, triggerKey);

		// 10초마다 실행한다.
    TriggerKey triggerKey2 = TriggerKey.triggerKey("stateful key2", "stateful group");
    Trigger trigger2 = triggerService.everySeconds(jobKey, triggerKey2);

		// 5초 마다 실행한다.
    TriggerKey triggerKey3 = TriggerKey.triggerKey("stateful key3", "stateful group");
    Trigger trigger3 = triggerService.everySeconds2(jobKey, triggerKey3);

    schedule(jobDetail, trigger, jobKey, triggerKey);
    schedule(jobDetail, trigger2, jobKey, triggerKey2);
    schedule(jobDetail, trigger3, jobKey, triggerKey3);
}

// ...
if(Objects.isNull(scheduler.getJobDetail(jobKey)))
    scheduler.scheduleJob(jobDetail, lastTrigger);
else
    scheduler.scheduleJob(lastTrigger);
```

- 해당 코드를 동작시키면, 동일 시간(10초) 시간대의 작업은 +3이 아닌 각각 +1이 겹쳐서 진행됩니다.

이러한 문제를 해결하기 위해 Quartz에서는 `@DisallowConcurrentExecution` 어노테이션을 지원합니다. 해당 어노테이션은 한 작업 클래스를 하나의 트리거에서만 실행할 수 있도록 제한할 수 있습니다.

```java
@PersistJobDataAfterExecution
@DisallowConcurrentExecution // 여러개의 트리거에 적용되면 동시실행을 막아준다.
public class StatefulJob implements Job {

    @Override
    public void execute(JobExecutionContext context) {
        JobDataMap dataMap = context.getJobDetail().getJobDataMap();
        int count = dataMap.getInt("count");
        count++;

        try {
            Thread.sleep(1000); // 100 밀리초 대기
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        dataMap.put("count", count);
        System.out.println("Job is running for the " + count + " time");
    }
}
```

</aside>