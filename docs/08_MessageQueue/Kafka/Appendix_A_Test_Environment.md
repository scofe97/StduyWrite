# Appendix A: Kafka 테스트 환경 설정

---

## 📌 핵심 요약
> 이 부록에서는 **단일 머신에서 3-노드 Kafka 클러스터를 설정하는 방법**을 다룬다. KRaft 모드(Dual Mode)로 구성하여 ZooKeeper 없이 동작하며, 부분 장애 시 Kafka의 동작을 테스트할 수 있다. **프로덕션 환경에서는 절대 사용하지 말 것.**

---

## 🎯 학습 목표
이 내용을 읽고 나면:
- [ ] 로컬 환경에 3-노드 Kafka 클러스터를 설정할 수 있다
- [ ] KRaft Dual Mode의 개념을 이해할 수 있다
- [ ] Kafka 브로커를 시작/중지할 수 있다
- [ ] 클러스터 상태를 확인할 수 있다

---

## 📖 본문 정리

### 1. 테스트 환경 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    Local Machine                            │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Broker 1   │  │  Broker 2   │  │  Broker 3   │         │
│  │             │  │             │  │             │         │
│  │ Port: 9092  │  │ Port: 9093  │  │ Port: 9094  │         │
│  │ Ctrl: 9192  │  │ Ctrl: 9193  │  │ Ctrl: 9194  │         │
│  │             │  │             │  │             │         │
│  │ [Dual Mode] │  │ [Dual Mode] │  │ [Dual Mode] │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> 💬 **Dual Mode**: 브로커가 Controller와 Broker 역할을 동시에 수행. ZooKeeper 없이 KRaft로 동작.

---

### 2. 지원 운영체제

| OS | 지원 여부 | 비고 |
|----|----------|------|
| macOS | ✅ | Apple Silicon, Intel 모두 지원 |
| Linux (Ubuntu) | ✅ | 24.04 LTS 테스트됨 |
| Windows | ⚠️ | WSL(Windows Subsystem for Linux) 권장 |

---

### 3. Kafka 다운로드

```bash
# 최신 버전 다운로드 (3.9.0 기준)
wget "https://downloads.apache.org/kafka/3.9.0/kafka_2.13-3.9.0.tgz"

# 압축 해제 및 이동
tar xfz kafka_2.13-3.9.0.tgz
rm kafka_2.13-3.9.0.tgz
mv kafka_2.13-3.9.0/ ~/kafka

# PATH 추가 (~/.bashrc 또는 ~/.zshrc에 추가 권장)
export PATH=~/kafka/bin:"$PATH"
```

**디렉토리 구조:**
```
~/kafka/
├── bin/          # CLI 도구
├── config/       # 설정 파일
├── libs/         # JAR 라이브러리
├── site-docs/    # 문서
├── LICENSE
└── NOTICE
```

---

### 4. 브로커 설정

#### Broker 1 (`~/kafka/config/kafka1.properties`)

```properties
broker.id=1
log.dirs=/home/USER/kafka/data/kafka1
listeners=PLAINTEXT://:9092,CONTROLLER://:9192
process.roles=broker,controller
controller.quorum.voters=1@localhost:9192,2@localhost:9193,3@localhost:9194
controller.listener.names=CONTROLLER
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
```

#### Broker 2 (`~/kafka/config/kafka2.properties`)

```properties
broker.id=2
log.dirs=/home/USER/kafka/data/kafka2
listeners=PLAINTEXT://:9093,CONTROLLER://:9193
process.roles=broker,controller
controller.quorum.voters=1@localhost:9192,2@localhost:9193,3@localhost:9194
controller.listener.names=CONTROLLER
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
```

#### Broker 3 (`~/kafka/config/kafka3.properties`)

```properties
broker.id=3
log.dirs=/home/USER/kafka/data/kafka3
listeners=PLAINTEXT://:9094,CONTROLLER://:9194
process.roles=broker,controller
controller.quorum.voters=1@localhost:9192,2@localhost:9193,3@localhost:9194
controller.listener.names=CONTROLLER
listener.security.protocol.map=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
```

**설정 항목 설명:**

| 설정 | 설명 |
|------|------|
| `broker.id` | 브로커 고유 ID |
| `log.dirs` | 데이터 저장 디렉토리 |
| `listeners` | 브로커/컨트롤러 리스너 포트 |
| `process.roles` | `broker,controller` = Dual Mode |
| `controller.quorum.voters` | 모든 컨트롤러 연결 정보 |

---

### 5. 데이터 디렉토리 초기화

```bash
# 1. 데이터 디렉토리 생성
mkdir -p ~/kafka/data/kafka1 ~/kafka/data/kafka2 ~/kafka/data/kafka3

# 2. 클러스터 ID 생성
export KAFKA_CLUSTER_ID="$(kafka-storage.sh random-uuid)"

# 3. 각 브로커 디렉토리 포맷
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c ~/kafka/config/kafka1.properties
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c ~/kafka/config/kafka2.properties
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c ~/kafka/config/kafka3.properties
```

> ⚠️ **클러스터 ID**: 동일한 ID로 포맷된 디렉토리만 같은 클러스터에서 사용 가능. 실수로 다른 클러스터 데이터 혼용 방지.

---

### 6. Kafka 시작

#### 포그라운드 실행 (디버깅용)

```bash
# 터미널 1
~/kafka/bin/kafka-server-start.sh ~/kafka/config/kafka1.properties

# 터미널 2
~/kafka/bin/kafka-server-start.sh ~/kafka/config/kafka2.properties

# 터미널 3
~/kafka/bin/kafka-server-start.sh ~/kafka/config/kafka3.properties
```

#### 백그라운드 실행 (Daemon)

```bash
~/kafka/bin/kafka-server-start.sh -daemon ~/kafka/config/kafka1.properties
~/kafka/bin/kafka-server-start.sh -daemon ~/kafka/config/kafka2.properties
~/kafka/bin/kafka-server-start.sh -daemon ~/kafka/config/kafka3.properties
```

#### 클러스터 상태 확인

```bash
kafka-broker-api-versions.sh \
    --bootstrap-server localhost:9092,localhost:9093,localhost:9094
```

**정상 출력:**
```
localhost:9092 (id: 1 rack: null) -> (...)
localhost:9093 (id: 2 rack: null) -> (...)
localhost:9094 (id: 3 rack: null) -> (...)
```

---

### 7. Kafka 중지

#### 전체 브로커 중지

```bash
~/kafka/bin/kafka-server-stop.sh
```

#### 개별 브로커 중지 스크립트

`~/kafka/bin/kafka-broker-stop.sh` 생성:

```bash
#!/bin/bash
BROKER_ID="$1"

if [ -z "$BROKER_ID" ]; then
  echo "usage ./kafka-broker-stop.sh [BROKER-ID]"
  exit 1
fi

PIDS=$(ps ax | grep -i 'kafka\.Kafka' | grep java \
    | grep "kafka${BROKER_ID}.properties" | grep -v grep | awk '{print $1}')

if [ -z "$PIDS" ]; then
  echo "No kafka server to stop"
  exit 1
else
  kill -s TERM $PIDS
fi
```

```bash
# 실행 권한 부여
chmod +x ~/kafka/bin/kafka-broker-stop.sh

# Broker 1만 중지
~/kafka/bin/kafka-broker-stop.sh 1
```

---

## 💡 실무 적용 포인트

### Quick Reference

| 작업 | 명령어 |
|------|--------|
| **전체 시작** | `kafka-server-start.sh -daemon config/kafkaX.properties` (×3) |
| **전체 중지** | `kafka-server-stop.sh` |
| **개별 중지** | `kafka-broker-stop.sh [ID]` |
| **상태 확인** | `kafka-broker-api-versions.sh --bootstrap-server localhost:9092,9093,9094` |

### 주의할 점
- ⚠️ **프로덕션 사용 금지**: 이 설정은 테스트/학습 전용
- ⚠️ **TLS 미적용**: 보안 설정 없음 (`PLAINTEXT`)
- ⚠️ **단일 머신**: 실제 장애 복구 테스트 한계

---

## 🔗 참고 자료
- 📄 공식 다운로드: [kafka.apache.org/downloads](https://kafka.apache.org/downloads)
- 📄 KRaft 설정: [Kafka KRaft Documentation](https://kafka.apache.org/documentation/#kraft)
