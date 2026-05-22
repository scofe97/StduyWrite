# [Spring MSA] xx-3. Kafka 3

주제: Spring MSA

- 참고
    
    [kafka publisher의 성능 비교](https://rudaks.tistory.com/entry/kafka-publisher의-성능-비교)
    
    [KafkaListener에서 서로 다른  message mapping하기](https://rudaks.tistory.com/entry/KafkaListener에서-서로-다른-message-mapping하기)
    
    [spring kafka를 사용할 때의 트랜잭션 처리](https://rudaks.tistory.com/entry/spring-kafka를-사용할-때의-트랜잭션-처리)
    

# 실습 프로젝트

---

<aside>
✍️ **NOTE**

[](https://github.com/spacetime101/fastcampus-kafka/tree/main/Chapter6)

![Untitled](%5BSpring%20MSA%5D%20xx-3%20Kafka%203/Untitled.png)

```java
@Configuration
@EnableKafka
@EnableKafkaStreams
public class KafkaConfiguration {

    @Bean(name = KafkaStreamsDefaultConfiguration.DEFAULT_STREAMS_CONFIG_BEAN_NAME)
    public KafkaStreamsConfiguration kStreamsConfigs() {
        Map<String, Object> props = new HashMap<>();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "kafka-streams");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.COMMIT_INTERVAL_MS_CONFIG, 1000); // flush interval . default 30000

        return new KafkaStreamsConfiguration(props);
    }
}
```

```java
@Component
public class StreamListener {

    @Bean
    public KStream<String, String> kStream(StreamsBuilder builder) {
        final String inputTopic = "checkout.complete.v1";
        final String outputTopic = "checkout.productId.aggregated.v1";

        KStream<String, String> inputStream = builder.stream(inputTopic);
        inputStream
                .map((k, v) -> new KeyValue<>(JsonUtils.getProductId(v), JsonUtils.getAmount(v)))
                // Group by productId
                .groupByKey(Grouped.with(Serdes.Long(), Serdes.Long()))
                // Window 설정
                .windowedBy(TimeWindows.of(Duration.ofMinutes(1)))
                // Apply sum method
                .reduce(Long::sum)
                // map the window key
                .toStream((key, value) -> key.key())
                // outputTopic 에 보낼 Json String 으로 Generate
                .mapValues(JsonUtils::getSendingJson)
                // outputTopic 으로 보낼 key 값을 null 설정
                .selectKey((key, value) -> null)
                // outputTopic 으로 메세지(null, jsonString) 전송 설정
                .to(outputTopic, Produced.with(null, Serdes.String()));

        return inputStream;
    }
}
```

</aside>