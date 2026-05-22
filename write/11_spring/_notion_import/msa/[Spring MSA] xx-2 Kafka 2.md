# [Spring MSA] xx-2. Kafka 2

주제: Spring MSA

- 참고

# Kafka 실제 구현 (자바 코드)

---

## 프로듀서

<aside>
✍️ **NOTE**

```java
public class Producer {

    private final static String BOOTSTRAP_SERVER = "localhost:9092";
    private final static String TOPIC_NAME = "topic";

    public static void main(String args[]) throws Exception {

				// 카프카 설정 (서버 경로, 직렬화, Acks, 재시도 ..)
        Properties configs = new Properties();
        configs.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVER);
        configs.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        configs.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        configs.put(ProducerConfig.ACKS_CONFIG, "all");
        configs.put(ProducerConfig.RETRIES_CONFIG, "100");

				// 카프카 Producer 생성
        KafkaProducer<String, String> producer = new KafkaProducer<>(configs);

				// 메시지 생성 및 적재
        String message = "Second Message";
        ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC_NAME, message);
        
				// 메시지 전송
				RecordMetadata metadata = producer.send(record).get();

        System.out.printf(">>> %s, %d, %d", message, metadata.partition(), metadata.offset());

        producer.flush();
        producer.close();
    }
}
```

</aside>

## 컨슈머

<aside>
✍️ **NOTE**

```java
public class Consumer {

    private final static String BOOTSTRAP_SERVER = "localhost:9092";
    private final static String TOPIC_NAME = "topic";
    private final static String GROUP_ID = "group_one";

    public static void main(String args []) {

				// 카프카 설정
        Properties configs = new Properties();
        configs.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVER);
        configs.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        configs.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        configs.put(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
        configs.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest"); // 특정 파티션의 오프셋이 유효하지 않을때 설정(초기시작 or 오프셋이 없는경우)

				// 컨슈머 생성 및 특정 토픽구독
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(configs);
        consumer.subscribe(Arrays.asList(TOPIC_NAME));

				// while문으로 1초마다 topics의 데이터 가져옴
        while(true){
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));

            for(ConsumerRecord<String, String> record : records) {
                System.out.println(">>>" + record);
                System.out.println(">>>>" + record.value());
            }
        }
    }
}
```

</aside>

# Kafka 실제 구현 (스프링 코드)

---

## 프로듀서

<aside>
✍️ **NOTE**

```java
@Configuration
public class KafkaProducerConfig {

    private static final String BOOTSTRAP_SERVER = "localhost:9092";

		// 문자열 카프카 설정
    @Bean
    public ProducerFactory<String, String> producerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVER);
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

        return new DefaultKafkaProducerFactory<>(configProps);
    }

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }

		// JSON 카프카 설정 (값을 JSON으로 직렬화)
    @Bean
    public ProducerFactory<String, MyMessage> newProducerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVER);
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, JsonSerializer.class);

        return new DefaultKafkaProducerFactory<>(configProps);
    }

    @Bean
    public KafkaTemplate<String, MyMessage> newKafkaTemplate() {
        return new KafkaTemplate<>(newProducerFactory());
    }
}
```

```java
@RestController
public class ProducerController {

    @Autowired
    private KafkaProduceService kafkaProduceService;

    @RequestMapping("/publish")
    public String publish(String message) {
        kafkaProduceService.send(message);
        return "published a message :" + message;
    }

    @RequestMapping("/publish2")
    public String publishWithCallback(String message) {
        kafkaProduceService.sendWithCallback(message);
        return "published a message with callback :" + message;
    }

    @RequestMapping("/publish3")
    public String publishJson(MyMessage message) {
        kafkaProduceService.sendJson(message);
        return "published a message with callback :" + message.getName() + "," + message.getMessage();
    }
}
```

```java
@Service
public class KafkaProduceService {

    private static final String TOPIC_NAME = "topic";

		// 문자열 설정 카프카
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

		// Json 설정 카프카
    @Autowired
    private KafkaTemplate<String, MyMessage> newKafkaTemplate;

		// Json 전송
    public void sendJson(MyMessage message) {
        newKafkaTemplate.send(TOPIC_NAME, message);
    }

		// 문자열 전송
    public void send(String message) {
        kafkaTemplate.send(TOPIC_NAME, message);
    }

		// 전송 이벤트
    public void sendWithCallback(String message) {
        ListenableFuture<SendResult<String, String>> future = kafkaTemplate.send(TOPIC_NAME, message);

        future.addCallback(new ListenableFutureCallback<SendResult<String, String>>() {
            @Override
            public void onFailure(Throwable ex) {
                System.out.println("Failed " + message + " due to : " + ex.getMessage());
            }

            @Override
            public void onSuccess(SendResult<String, String> result) {
                System.out.println("Sent " + message + " offset:"+result.getRecordMetadata().offset());
            }
        });
    }
}
```

</aside>

## 컨슈머

<aside>
✍️ **NOTE**

```java
@EnableKafka // 카프카 리스너 활성
@Configuration
public class KafkaConsumerConfig {
    private static final String BOOTSTRAP_SERVER = "localhost:9092";
    private static final String GROUP_ID = "group";

		// 카프카 설정
    @Bean
    public ConsumerFactory<String, String> consumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVER);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        return new DefaultKafkaConsumerFactory<>(props);
    }

		// Kafka 리스너 컨테이너 생성
		// 멀티스레드 환경에서 Kafka 메시지 리스너를 효율적으로 관리
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, String> factory =
                new ConcurrentKafkaListenerContainerFactory<>();

        factory.setConsumerFactory(consumerFactory());
        return factory;
    }

}
```

```java
@Component
public class KafkaConsumer {

    private static final String TOPIC_NAME = "topic";
    ObjectMapper objectMapper = new ObjectMapper();

		// 특정 토픽에 대한 발생
    @KafkaListener(topics = TOPIC_NAME)
    public void listenMessage(String jsonMessage) {
        try {
            MyMessage message = objectMapper.readValue(jsonMessage, MyMessage.class);
            System.out.println(">>>" + message.getName() + "," +message.getMessage());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

</aside>

# Kafak 활용사례

---

## 유저 활동 추적기능

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx-2%20Kafka%202/Untitled.png)

[https://creampuffy.tistory.com/210?category=986890](https://creampuffy.tistory.com/210?category=986890)

유저의 페이지 뷰, 클릭등의 구체적인 행위를 수집하여 고객 행동을 분석/모니터링하고, 이를 통해 기능 개선이나 비즈니스의 의사결정이나 데이터로 활용한다.

최대한 많이 수집하여 저장하고, 이후 필요에 따라 가공해서 사용한다.

데이터 수집은 고객에게 제공할 핵심가치는 아니므로, 데이터 수집을 위해 애플리케이션 성능에 영향을 주어선안된다. Batch 전송을 활용하여 심플하게 처리하는것이 좋다.

데이터 규모가 매우크고 폭발적으로 늘어날 수 있음을 고려해서 확장에 유연한 수집/저장 프로세스를 아키텍쳐링 해야한다.

인터넷 네트워크상의 문제로 데이터가 전달되지 않을 수 있으니, 유실없는 완벽한 수집보다는 빠르고 지속적인 수집에 관심 acks = 1

사용자 활동추적은 최대한 투명하고 고객이 거부할 수 있는 옵션을 제공하는것이 좋다.

</aside>

## 메세징

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx-2%20Kafka%202/Untitled%201.png)

비즈니스 도메인 간의 비동기 프로세스에 사용되는 방식

ex) 메세지 발행자 시스템의 트랜잭션이 완료된 후 해당 이벤트에 따라 후속 프로세스가 필요한 다른 시스템에 트랜잭션 결과를 통지

- 결제시스템 프로세스 완료 → 배송 도메인에 결과 메세지 전달
- 회원가입 프로세스 완료 → 마케팅 도미엔이 결과 메세지 전달
- 마케팅 도메인에서 고객에게 발생할 메세지 전송 요청건 생성하여, 메세지 발송 도메인에 전달

메세지 유실 가능성을 최소화 할 수 있도록, ack-all을 설정하거나, 컨슈머에서 dead letter queue(topic)을 사용하여 재처리 프로세스를 만들자.

데이터 누락이나 오류시 매우 크리티컬한 정보라면 별도의 대사 프로세스를 만들어 무결성을 체크하는 경우가 있다.

</aside>

## 스트리밍 프로세스

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx-2%20Kafka%202/Untitled%202.png)

지속적으로 토픽에 인입되는 이벤트 메세지를 실시간으로 가공, 집계, 분할하는 프로세싱

- 유저 활동 추적으로 들어오는 로그 메세지를 가공하여 새로운 토픽에 저장
- IoT시스템에서 지속적으로 들어오는 이벤트 데이터를 실시간으로 분석
- Time Window를 적용하여 최근 10분간의 집계데이터를 생성하여 Slack채널에 자동으로 리포트
- 시스템의 문제나 비즈니스 데이터의 문제상황을 실시간으로 캐치하려는 Alarm 발

</aside>

## 이벤트 소싱

<aside>
✍️ **NOTE**

![Untitled](%5BSpring%20MSA%5D%20xx-2%20Kafka%202/Untitled%203.png)

애플리케이션의 상태에 대한 모든 변경사항을 일련의 이벤트로 표현하는 패턴을 말한다.

애플리케이션은 상태에 대한 전체 변경 기록을 저장하고 이벤트를 재생하여 현재 상태를 재구성한다.

대규모 MSA 아키텍쳐에서 CQRS 패턴과 결합하여 도입되는 추세이다.

CQRS패턴에서 실시간으로 전체 이벤트에 기반하여 현재 상태를 생성하는것은 한계가 있으므로, Evenet Handler에서 조회시에 사용할 상태값을 구체화된 뷰에 생성하여 조회시에 사용

Kafka는 이벤트 소싱 기반 애플리케이션에서 이벤트 스토어로 활

- 
- 

</aside>

# 카프카 운영

---

## 브로커 && 파티션 추가

<aside>
✍️ **NOTE**

운영중인 카프카 토픽이라면 매우 신중하게 결정해야 한다.

- topic에 파티션 추가는 새로운, 파티션으로 메세지 재배치가 되는 과정에서 시스템 성능에 영향을 끼칠 수 있으니, 최대한 사용시간이 적을때 작업하자
- 실제 해당 Topic의 사용 사례를 고려해서, 필요시 테스트 서버에서 테스트를 해보고 실행하자
- 모든 메세지를 RoundRobin 방식으로 처리하고 있다면, 데이터 규모에 따른 지연시간 이후 곧 정상처리가 시작될 수 있지만, 특정 Key-Patition에 기반한 Consumer를 운영중이라면 메세지의 유실 가능성도 있으므로 신규 Topic을 생성해서 Migration전략을 짜는것이 더 좋을 수 있다,
- 따라서 Topic의 최초 생성시, 데이터확장 규모를 고려해서 Partition개수를 여유있게 설정하자

운영중인 카프카 클러스터라면

- 처리중인 데이터 규모에 따라 파티션 재배치에 따른 사용량 증가 및 임팩트가 클 수 있다.
- 상황에 따라 사용량이 적은 시간을 이용하거나, 임시로 retention을 작세 설정하거나 topci을 나눠서 실행해 부하를 분산하
</aside>

## 인증 추가하기

<aside>
✍️ **NOTE**

Kafka SASL 인증 종류

- SASL/PLAIN : 간단하게 사용자 이름과 암호를 사용하여 인증
- SASL/SCRAM : SCRAM 메커니즘을 사용
- SASL/GSSAPI
- SASL/OAUTHEBEARER

</aside>

## 오픈소스 모니터링 툴 소개

<aside>
✍️ **NOTE**

- CMAK
- Burrow
- XInfra
- Exporter + Prometheus +Grafana

![Untitled](%5BSpring%20MSA%5D%20xx-2%20Kafka%202/Untitled%204.png)

</aside>