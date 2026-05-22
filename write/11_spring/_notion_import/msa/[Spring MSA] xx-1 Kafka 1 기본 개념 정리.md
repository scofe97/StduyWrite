# [Spring MSA] xx-1. Kafka 1 기본 개념 정리

주제: Spring MSA
연관 노트: [고성능 서비스를 위한 Redis] 06. Pub/Sub를 이용한 채팅방 구현 (https://www.notion.so/Redis-06-Pub-Sub-9f2ad6b982b44f558e72ef0033c1a113?pvs=21)

- 참고
    
    [Server-Sent Events(SSE), Redis pub/sub, Kafka로 알림 기능 개선하기.](https://velog.io/@xogml951/Server-Sent-EventsSSE-Redis-pubsub-Kafka로-알림-기능-개선하기#4-kafka로-알림)
    
    [Spring Cloud로 개발하는 마이크로서비스(인프런 강의 정리)](https://velog.io/@kurikuri/Spring-Cloud로-개발하는-마이크로서비스인프런-강의-정리)
    
    [MSA 통신 패턴 (동기, 비동기)과 Apache Kafka, Zookeeper](https://developer-syubrofo.tistory.com/150)
    
    [3장. 카프카 기본 개념 설명](https://rudaks.tistory.com/entry/3장-카프카-기본-개념-설명)
    
    [[Apache Kafka]구성요소 이해하기(Cluster, Broker, Topic, Partition, Producer, Consumer, Zookeeper)](https://magpienote.tistory.com/212)
    
    [[Kafka] 카프카 토픽과 파티션, 레코드 저장방식](https://ksr930.tistory.com/182)
    

# 카프카란 무엇인가?

---

<aside>
💡 **NOTE**

> *카프카는 RabbitMQ, ActiveMQ와 비교했을 때, **높은 확장성과 내결함성, 대용량 데이터 처리, 실시간 데이터 처리에 특화되어 있는 오픈소스 메시징 시스템이다!***
> 

![카프카는 Pub/Sub 구조로 구성되며, 3개 이상의 클러스터를 사용하는것이 일반적이다.](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/Untitled.png)

카프카는 Pub/Sub 구조로 구성되며, 3개 이상의 클러스터를 사용하는것이 일반적이다.

- **프로듀서**
    - 데이터를 생성하고 카프카 토픽에 메시지를 발행하는 역할을 한다.
- **컨슈머**
    - 카프카 토픽에서 메시지를 읽는 역할을 한다.
- **주키퍼**
    - 카프카 클러스터, 토픽에 대한 관리를하는 역할을 한다.
- **브로커**
    - 브로커는 개별 카프카 서버로 생각하면 된다.
    - 브로커는 프로듀서로부터 메시지를 전달받고, 컨슈머에 전달하는 역할을 한다.
    - 브로커는 여러개의 토픽을 가질 수 있다.
- **토픽**
    - 토픽은 데이터가 저장되는 단위라고 할 수 있다.
    - 토픽은 이름으로 식별되며, 토픽에 한번 추가된 데이터는 수정할 수 없다.
    - 브로커별로 있다는 개념이 아니라, 전체 브로커에 공용적으로 사용되는 개념이다.
- **파티션**
    - 카프카의 확장성을 위해 토픽은 1개 이상의 파티션으로 구분될 수 있다.
    - 모든 파티션들은 Offset이라는 ID를 부여받으며, 불변의 속성을 가진다.
    - 각 브로커에 파티션이 복제되며, 리더 파티션이 읽기/쓰기 작업을 진행한다.
</aside>

## 다른 MessageQueue(Redis, RabbitMQ) 비교

<aside>
✍️ **NOTE**

대중적인 메세지 브로커로 RabbitMQ, Redis, Kafka를 주로 사용하면서 이를 메시지 플랫폼이라 한다.

메시지 플랫폼은 2가지 종류(메시지 || 이벤트 브로커)로 나누어 진다.

### 메시지 브로커(RabbitMQ, Redis)

대규모 메시지 기반 미들웨어 아키텍쳐에서 사용되어 왔으며, **메시지를 받아서 적절히 처리하면 짧은 시간내에 메시지가 삭제**된다. (데이터 손실의 위험)

### 이벤트 브로커(Kafka)

이벤트 or 메시지라고 불리는 정보를 하나만 보관하고, 인덱스를 통해 개별 액세스를 관리한다.

**메시지 브로커와 다르게 이벤트가 삭제되지 않으며**, 서비스에 발생하는 이벤트를 DB에 저장하듯 이벤트 브로커의 큐에 저장한다.

이벤트를 저장함으로써 얻는 장점은 다음과 같다.

- 장애가 발생했을 떄 장애가 일어난 시점부터 재처리 가능
- 많은 양의 실시간 스트림 데이터를 효과적으로 처리할 수 있다.
</aside>

## 카프카의 비동기성 프로세스

<aside>
✍️ **NOTE**

![동기 → 요청을 반환할때까지 반환시간이 느려진다.](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/%25EC%258B%259C%25EC%258A%25A4%25ED%2585%259C_%25EC%2595%2584%25ED%2582%25A4%25ED%2585%258D%25EC%25B3%2590_(2%25EC%2595%2588).png)

동기 → 요청을 반환할때까지 반환시간이 느려진다.

기존의 동기 프로세스는 Request(요청)을 보내면, 해당 요청에 대한 로직이 끝나고 반환될때까지 기다려야 한다. 이러한 프로세스는 로직이 오래걸릴수록 반환이 늦어진다.

![비동기 → 요청이 넘어가면 바로 응답해준다.](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/%25EC%258B%259C%25EC%258A%25A4%25ED%2585%259C_%25EC%2595%2584%25ED%2582%25A4%25ED%2585%258D%25EC%25B3%2590_(2%25EC%2595%2588)-1.png)

비동기 → 요청이 넘어가면 바로 응답해준다.

카프카를 이용한 메시지 기반의 비동기 프로세스는 카프카 브로커에 메시지가 전송되면 즉시 반환된다.

실제 처리 로직이 아직 수행되지 않았더라도, 메시지 브로커가 전송을 보장하기 때문에 메시지를 브로커에 적재한 후 역할을 마친다.

이러한 방식을 **이벤트 기반 아키텍쳐**라고 부르며, MSA구조에서 널리 사용되는 방식이다.

</aside>

## 데이터 복제(싱크)

<aside>
✍️ **NOTE**

> ***카프카의 데이터 복제는 파티션 단위로 이루어진다!***
> 

![카프카 클러스터로 묶인 브로커는, 하나의 브로커가 장애가 발생해도 다른 브로커를 통해 가용성을 보장한다.](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/Untitled%201.png)

카프카 클러스터로 묶인 브로커는, 하나의 브로커가 장애가 발생해도 다른 브로커를 통해 가용성을 보장한다.

- ex) 파티션의 복제가 3개인경우
- 프로듀서 또는 컨슈머와 직접 통신하는 파티션을 **리더**, 나머지 복제 파티션을 **팔로워**라고 한다.
- 팔로워 파티션은 리더 파티션의 오프셋을 확인하여 주기적으로 동기화한다.
- 컨트롤러를 통해 하나의 브로커에서 장애가 발생하면, 리더 파티션을 재분배하한다.

**카프카는 컨슈머가 데이터를 가져가더라도 토픽의 데이터는 삭제되지 않는다.**

- 오직 브로커만이 데이터를 삭제할 수 있으며, 삭제는 파일단위(로그 세그먼트)로 이루어진다.
</aside>

## 토픽, 파티션, 레코드

<aside>
✍️ **NOTE**

> ***토픽**은 카프카에서 데이터를 구분하는 단위이며, 토픽은 1개 이상의 **파티션**을 소유하고 있다. 그리고 파티션에 저장되는 데이터를 **레코드**라고 부른다.*
> 

![토픽에서 보낸 데이터(레코드)는 각 파티션에 저장된다.](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/Untitled%202.png)

토픽에서 보낸 데이터(레코드)는 각 파티션에 저장된다.

![Current Offset을 통해 카프카는 특정 컨슈머 그룹이 파티션에서 읽은 마지막 위치를 추적한다.](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/Untitled%203.png)

Current Offset을 통해 카프카는 특정 컨슈머 그룹이 파티션에서 읽은 마지막 위치를 추적한다.

**파티션**은 카프카의 병렬처리의 핵심으로, 그룹으로 묶인 컨슈머들이 레코드를 병렬로 처리할 수 있도록 매칭된다. 컨슈머의 처리량이 한정된 상황에서 많은 레코드를 병렬로 처리하는 가장 좋은 방법은 컨슈머의 개수를 늘리고, 파티션을 늘리는 것이다.

**레코드**는 타임스탬프, 메시지 키, 메시지 값, 오프셋으로 구성되어 있다. 레코드는 수정할 수 없고 로그 리텐션 기간 또는 용량에 따라서만 삭제된다.

- 타임스탬프
    - 브로커 기준 시간
- 메시지 키
    - 메시지 값을 순서대로 처리하거나, 값의 종류를 나타내기 위해 사용한다.
    - 메시지의 키의 해시값을 토대로 저장하게 된다. (동일 메시지 키라면 동일 파티션에 들어감)
    - 메시지 키를 사용하지 않는다면 기본 설정으로 분리된다.
- 메시지 값
    - 실직적으로 처리할 데이터
    - 메시지 키와 메시지 값은 직렬화되어 브로커로 전송되므로, 역직렬화 과정을 수행해야 한다.
- 오프셋
    - 0 이상의 숫자
    - 이전에 전송된 레코드의 오프셋 +1로 설정된다.

</aside>

## 카프카 기본 명령어

<aside>
✍️ **NOTE**

[Apache Kafka](https://kafka.apache.org/downloads)

설치 링크

![카프카는 기본적으로 해당 파일들을 실행시켜서 동작한다. (Window 기준)](%5BSpring%20MSA%5D%20xx-1%20Kafka%201%20%EA%B8%B0%EB%B3%B8%20%EA%B0%9C%EB%85%90%20%EC%A0%95%EB%A6%AC/Untitled%204.png)

카프카는 기본적으로 해당 파일들을 실행시켜서 동작한다. (Window 기준)

```powershell
# 주키퍼 시작
.\bin\windows\zookeeper-server-start.bat `
.\config\zookeeper.properties

# 카프카 서버 시작
.\bin\windows\kafka-server-start.bat `
.\config\server.properties

```

```powershell
# 토픽 생성
.\bin\windows\kafka-topics.bat `
--create `
--topic topic-example1 `
--bootstrap-server localhost:9092

# 토픽 리스트 조회
.\bin\windows\kafka-topics.bat `
--list `
--bootstrap-server localhost:9092 

# 토픽 상세 조회
.\bin\windows\kafka-topics.bat `
--describe `
--topic topic-example1 `
--bootstrap-server localhost:9092 

# 파티션 수를 3개로 변경합니다. (파티션은 늘리기만 가능하다.)
.\bin\windows\kafka-topics.bat `
--alter `
--topic topic-example1 `
--partitions 3 `

# 메시지 보존 기간을 1일(86,400,000ms)로 설정합니다.
.\bin\windows\kafka-configs.bat `
--alter `
--entity-type topics `
--entity-name topic-example1 `
--add-config retention.ms=86400000

```

```powershell
# topic-example1을 사용한다. (메세지 전송가능)
.\bin\windows\kafka-console-producer.bat `
--topic topic-example1 `
--bootstrap-server localhost:9092 

# 메세지 키를 사용해서 전송
# "1:2"의 값이 넘어가면 key 1은 해시값을 적용해서 키로 저장하고, 2는 value로 저장됨
.\bin\windows\kafka-console-producer.bat `
--topic topic-example1 `
--property "parse.key=true" `
--property "key.separator=:" `
--bootstrap-server localhost:9092 

# 옵션은 적어도 하나의 브로커가 메시지를 받았을 때까지 기다립니다.
# acks 옵션 (0, 1, all(-1)이 존재한다.
# 0(리더 파티션 저장확인 x), 1(리더 파티션 저장확인 o), all(모든 파티션 확인)
.\bin\windows\kafka-console-producer.bat `
--topic topic-example1 `
--request-required-acks 1 `
--bootstrap-server localhost:9092 

# 메시지 전송 실패 시 최대 5번 재시도합니다.
.\bin\windows\kafka-console-producer.bat `
--topic topic-example1 `
--message-send-max-retries 5 `
--bootstrap-server localhost:9092 
```

```powershell
# 컨슈머 확인
# from-beginning (처음부터 토픽의 모든 메시지를 소비한다.)
.\bin\windows\kafka-console-consumer.bat `
--topic topic-example1 `
--from-beginning `
--bootstrap-server localhost:9092

# 특정 offset부터 메시지 소비
.\bin\windows\kafka-console-consumer.bat `
--topic topic-example1 `
--offset 100 `
--bootstrap-server localhost:9092 

# 특정 그룹 Id로 메시지 소비
.\bin\windows\kafka-console-consumer.bat `
--topic topic-example1 `
--group my-consumer-group `
--bootstrap-server localhost:9092 

# Consumer Group정보 확인 (Offset)
.\bin\windows\kafka-consumer-groups.bat `
--describe `
--group my-consumer-group `
--bootstrap-server localhost:9092 

# 모든 컨슈머 그룹의 목록을 조회합니다.
.\bin\windows\kafka-consumer-groups.bat `
--list `
--bootstrap-server localhost:9092 

# 'group1' 컨슈머 그룹의 상세 정보를 조회합니다.
.\bin\windows\kafka-consumer-groups.bat `
--describe `
--group my-consumer-group `
--bootstrap-server localhost:9092 
```

```bash
Broker#0 - server.properties
broker.id=0
listeners=PLAINTEXT://localhost:9092
log.dirs=/tmp/kafka-logs

Broker#1 - server1.properties
broker.id=1
listeners=PLAINTEXT://localhost:9093
log.dirs=/tmp/kafka-logs1

Broker#2 - server2.properties
broker.id=2
listeners=PLAINTEXT://localhost:9094
log.dirs=/tmp/kafka-logs2
```

```bash
# Kafka Connect 관련 명령어
# Kafka Connect의 스탠드얼론 모드 설정 파일에서 스키마 사용 비활성화
key.converter.schemas.enable=false
value.converter.schemas.enable=false

# File Sink Connect 설정 파일에서 'topic3'를 대상 토픽으로 설정
topics=topic3

# 스탠드얼론 모드의 Kafka Connect를 실행
bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-sink.properties
```

</aside>