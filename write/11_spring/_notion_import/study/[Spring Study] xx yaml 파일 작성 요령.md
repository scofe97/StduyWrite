# [Spring Study] xx. yaml 파일 작성 요령

주제: Spring Study
연관 노트: [Kubernetes Infra] 01-4. YAML 문법 (https://www.notion.so/Kubernetes-Infra-01-4-YAML-221c73cb2474443b9ade969ed7267e4b?pvs=21)

- 참고
    
    [yaml 파일 작성 요령 (기초편, 스프링편)](https://velog.io/@bloomspes/yaml-%ED%8C%8C%EC%9D%BC-%EC%9E%91%EC%84%B1-%EC%9A%94%EB%A0%B9-%EA%B8%B0%EC%B4%88%ED%8E%B8-%EC%8A%A4%ED%94%84%EB%A7%81%ED%8E%B8)
    

# **what is a 'YAML'/'YML'?**

---

<aside>
💡 **NOTE**

> ***Yet Another Markup Language(YAML), 사람이 읽을 수 있는 데이터 직렬화 언어이다.***
> 

![Untitled](%5BSpring%20Study%5D%20xx%20yaml%20%ED%8C%8C%EC%9D%BC%20%EC%9E%91%EC%84%B1%20%EC%9A%94%EB%A0%B9/Untitled.png)

- 다른 종류로는 Xml, Json도 데이터 직렬화 언어에 포함된다.
- yaml이 다른 종류보다 훨씬 간결하고 눈에 들어온다.
</aside>

# **YAML/YML 파일의 구성 및 작성법**

---

<aside>
💡 **NOTE**

- key-value 구성으로 작성된 파일이다.
- YAML/YML 파일은 Json 파일과 상위 호환되기 때문에, Json 시퀀스와 맵을 사용할 수 있다.
</aside>

## **YAML의 기본 자료형**

<aside>
✍️ **NOTE**

- 스칼라(Scalar) : String 혹은 Number
- 시퀀스(Sequence) : 배열 혹은 리스트
- 매핑(Mapping) : 해시 혹은 딕셔너리(key-value) 쌍
</aside>

## **Collections**

<aside>
✍️ **NOTE**

```yaml
---
hr: # 1998 hr ranking
  - Mark McGwire
  - Sammy Sosa
rbi:
  # 1998 rbi ranking
  - Sammy Sosa
  - Ken Griffey
...
```

- `Key-Value`의 매핑은 :으로 구분한다.
- 문서의 시작(`---`삽입)과 끝(`…` 삽입)을 지정할 수 있다. (선택사항)
- tab키가 아닌 space bar 하나로 들여쓰기를 한다.
- key와 value 사이에 공백이 존재해야 한다.
</aside>

# **[Spring] application.yml에 데이터 매핑**

---

<aside>
💡 **NOTE**

- `@Value`와 `@ConfigurationProperties` 두 가지 어노테이션을 사용해서 **데이터 매핑**을 할 수 있다.
- `@ConfigurationProperties`는 메타데이터 지원과 유연한 바인딩이 가능하기 떄문에 `@Value`보다 많은 상황에서 두루 쓰이는 장점이 있다.
- 고정 값을 매핑하는 경우, `@Value`를 사용해서 구성하는 것이 더 간편하고 가독성이 좋다.

1. ***application.yml에 Youtube를 Key값으로 하는 리스트 데이터 작성***
    
    ```yaml
    Youtube:
     channel:
      - name : penbird
        type : keyboard and hand writings
      - name : kyleschool
        type : data science and engineering
      - name : habithackers
        type : opct training
    ```
    
2. ***@ConfigurationProperties에 Youtuber객체 바인딩***
    
    ```java
    @Data
    @Component
    @ConfigurationProperties("Youtube")
    public class YoutubeProperty {
        private List<Youtube> channel;
        
         public YoutubeProperty(List<Map<String, String>> channel) {
            this.channel = channel;
        }
    
        public List<Map<String, String>> getChannel() {
            return channel;
        }
    
    }
    ```
    
3. ***테스트 수행***
    
    ```java
    @SpringBootTest
    class YoutubePropertyTest {
    
        @Autowired
        private YoutubeProperty youtubeProperty;
    
        @DisplayName("Property build Test at Springboot")
        @Test
        void configurationPropertyTest() {
            List<Map<String, String>> channel = YoutubeProperty.getChannel();
    
            assertAll(
                    () -> assertThat(channel).hasSize(3),
                    () -> assertThat(channel.get(0).get("name")).isEqualTo("penbird"),
                    () -> assertThat(channel.get(0).get("type")).isEqualTo("keyboard and hand writings")
            );
        }
    }
    ```
    
</aside>