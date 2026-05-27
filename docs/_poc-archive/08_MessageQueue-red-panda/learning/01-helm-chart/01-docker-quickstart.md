# Redpanda Docker 빠른 시작 가이드

**작성일**: 2025-02-05
**목적**: Docker/Docker Compose를 사용한 Redpanda 로컬 개발 환경 구축

---

## 1. Docker vs Helm 비교

### Docker/Docker Compose가 적합한 경우

Docker는 **로컬 개발 및 테스트 환경**에 적합합니다. 복잡한 오케스트레이션 없이 빠르게 Redpanda를 실행하고 애플리케이션 개발을 시작할 수 있습니다. 개발자 머신에서 코드를 작성하고 테스트할 때, 또는 CI/CD 파이프라인에서 통합 테스트를 실행할 때 사용합니다.

Docker Compose는 단일 YAML 파일로 Redpanda, Console, 클라이언트 애플리케이션을 한 번에 실행할 수 있어 개발 워크플로우가 단순합니다. 노트북에서도 실행 가능하며, 설정 변경 후 즉시 재시작할 수 있습니다.

### Helm/Kubernetes가 적합한 경우

Helm은 **스테이징 및 프로덕션 환경**에 적합합니다. Kubernetes 클러스터에서 실행되며 고가용성, 자동 스케일링, 모니터링이 필요한 상황에서 사용합니다.

Helm 차트는 Redpanda 클러스터를 StatefulSet으로 배포하여 파드가 재시작되어도 데이터를 유지합니다. Prometheus, Grafana와 통합하여 메트릭을 수집하고, TLS/SASL 인증으로 보안을 강화할 수 있습니다. 프로덕션에서는 네트워크 파티션, 디스크 장애 등의 상황을 자동으로 처리해야 하므로 Kubernetes의 자가 치유 기능이 필수적입니다.

### 비교 요약

| 항목 | Docker Compose | Helm (Kubernetes) |
|------|---------------|------------|
| 적합 환경 | 로컬 개발/테스트 | 스테이징/프로덕션 |
| 복잡도 | 낮음 (YAML 파일 하나) | 중간-높음 (K8s 개념 필요) |
| 스케일링 | 수동 (docker-compose.yml 수정) | 자동 (HPA) |
| 모니터링 | Redpanda Console | Prometheus+Grafana |
| 네트워크 | Docker bridge | K8s Service/Ingress |
| 영속성 | Docker volume | PersistentVolumeClaim |
| 장애 복구 | 수동 재시작 (`docker restart`) | 자동 (StatefulSet) |
| 보안 | 기본 없음 (개발용) | TLS+SASL+ACL |
| 리소스 격리 | cgroup 기반 제한 | Namespace, ResourceQuota |
| 설정 관리 | docker-compose.yml 직접 수정 | Helm values.yaml + 버전 관리 |

**권장 사항**: 개발 중에는 Docker Compose로 빠르게 검증하고, 프로덕션 배포 전에 Helm으로 전환하여 스테이징 환경에서 충분히 테스트합니다.

---

## 2. Single Node 설정 (docker run)

### 기본 실행 명령어

```bash
docker run -d --name=redpanda \
  -p 9092:9092 -p 8081:8081 -p 8082:8082 -p 9644:9644 \
  docker.redpanda.com/redpandadata/redpanda:v25.1.1 \
  redpanda start --smp 1 --memory 1G --overprovisioned \
  --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092 \
  --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092 \
  --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082 \
  --advertise-pandaproxy-addr internal://redpanda:8082,external://localhost:18082 \
  --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:18081 \
  --rpc-addr redpanda:33145 --advertise-rpc-addr redpanda:33145
```

이 명령어는 단일 노드 Redpanda 브로커를 백그라운드에서 실행합니다. 개발 환경에 최적화된 설정으로, 노트북에서도 안정적으로 동작합니다.

### docker run 옵션 상세 설명

#### 리소스 설정

- **`--smp 1`**: 사용할 CPU 코어 수를 지정합니다. Redpanda는 Seastar 프레임워크의 thread-per-core 모델을 사용하므로, 1 코어를 할당하면 1개의 Reactor 스레드가 생성됩니다. 개발 환경에서는 1 코어로 충분하며, 프로덕션에서는 머신의 물리적 코어 수에 맞춰 증가시킵니다.

- **`--memory 1G`**: Redpanda에 할당할 메모리 용량입니다. 1GB는 개발 및 테스트에 충분합니다. Redpanda는 메모리를 페이지 캐시, 로그 버퍼, 내부 데이터 구조에 사용하므로, 프로덕션에서는 최소 4GB 이상 권장됩니다.

- **`--overprovisioned`**: 전용 하드웨어가 아닌 공유 환경(컨테이너, VM, 개발자 머신)에서 실행할 때 **필수**입니다. 이 옵션이 없으면 Seastar의 I/O 스케줄러가 전체 디스크 대역폭을 독점하려고 시도하여 다른 프로세스를 방해할 수 있습니다. `--overprovisioned`를 설정하면 I/O 스케줄러가 보수적으로 동작하여 CPU와 디스크를 다른 프로세스와 공유합니다.

#### 네트워크 주소 설정

Redpanda는 **internal**과 **external** 두 가지 리스너를 구분합니다. 이는 Docker 네트워크의 특성 때문입니다.

- **`--kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092`**:
  - `internal`: Docker 네트워크 내부의 다른 컨테이너(예: Redpanda Console)가 접근하는 주소입니다. 포트 9092를 사용합니다.
  - `external`: 호스트 머신(개발자 노트북)에서 접근하는 주소입니다. 포트 19092를 사용하며, Docker의 포트 포워딩으로 매핑됩니다.

- **`--advertise-kafka-addr internal://redpanda:9092,external://localhost:19092`**:
  - 클라이언트에게 "이 주소로 접속하세요"라고 알려주는 advertised 주소입니다.
  - `internal://redpanda:9092`: Docker 네트워크 내부에서는 컨테이너 이름 `redpanda`로 접근합니다.
  - `external://localhost:19092`: 호스트 머신에서는 `localhost:19092`로 접근합니다.
  - **중요**: Kafka 프로토콜은 초기 연결 후 브로커가 advertised 주소를 클라이언트에게 전달하므로, 이 설정이 잘못되면 "연결은 되는데 메타데이터를 가져올 수 없음" 오류가 발생합니다.

- **`--pandaproxy-addr`**, **`--schema-registry-addr`**: Kafka API와 동일한 internal/external 분리 전략을 사용합니다. HTTP API이므로 Kafka 프로토콜보다 단순하지만, REST 클라이언트가 올바른 포트로 접근하도록 설정해야 합니다.

#### RPC 주소

- **`--rpc-addr redpanda:33145`**, **`--advertise-rpc-addr redpanda:33145`**: 브로커 간 내부 통신에 사용되는 RPC 주소입니다. 단일 노드에서는 사용되지 않지만, 클러스터 모드에서는 브로커들이 이 주소로 Raft 합의, 메타데이터 동기화, 복제를 수행합니다.

### 컨테이너 관리 명령어

```bash
# 컨테이너 시작 확인
docker ps | grep redpanda

# 로그 확인
docker logs redpanda

# 컨테이너 중지
docker stop redpanda

# 컨테이너 삭제
docker rm redpanda
```

---

## 3. Docker Compose (단일 노드)

Docker Compose를 사용하면 Redpanda와 Console을 함께 실행하고 관리할 수 있습니다. YAML 파일 하나로 전체 스택을 정의하므로 설정 관리가 쉽습니다.

### docker-compose.yml 작성

```yaml
version: '3.7'

services:
  redpanda:
    image: docker.redpanda.com/redpandadata/redpanda:v25.1.1
    container_name: redpanda
    command:
      - redpanda start
      - --smp 1
      - --memory 1G
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda:9092,external://localhost:19092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr internal://redpanda:8082,external://localhost:18082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:18081
      - --rpc-addr redpanda:33145
      - --advertise-rpc-addr redpanda:33145
    ports:
      - "18081:18081"  # Schema Registry (external)
      - "18082:18082"  # Pandaproxy (external)
      - "19092:19092"  # Kafka API (external)
      - "9644:9644"    # Admin API
    volumes:
      - redpanda-data:/var/lib/redpanda/data
    healthcheck:
      test: ["CMD-SHELL", "rpk cluster health | grep -E 'Healthy:.+true'"]
      interval: 15s
      timeout: 3s
      retries: 5
      start_period: 5s
    networks:
      - redpanda-network

  console:
    image: docker.redpanda.com/redpandadata/console:v2.8.0
    container_name: redpanda-console
    ports:
      - "8080:8080"
    environment:
      CONFIG_FILEPATH: /tmp/config.yml
      CONSOLE_CONFIG_FILE: |
        kafka:
          brokers: ["redpanda:9092"]
          schemaRegistry:
            enabled: true
            urls: ["http://redpanda:8081"]
        redpanda:
          adminApi:
            enabled: true
            urls: ["http://redpanda:9644"]
    depends_on:
      redpanda:
        condition: service_healthy
    networks:
      - redpanda-network

volumes:
  redpanda-data:
    driver: local

networks:
  redpanda-network:
    driver: bridge
```

### 주요 구성 요소 설명

#### healthcheck

```yaml
healthcheck:
  test: ["CMD-SHELL", "rpk cluster health | grep -E 'Healthy:.+true'"]
  interval: 15s
  timeout: 3s
  retries: 5
  start_period: 5s
```

Healthcheck는 Redpanda 브로커가 실제로 요청을 처리할 준비가 되었는지 확인합니다. `rpk cluster health` 명령어를 실행하여 "Healthy: true" 응답을 확인하며, 실패하면 5번까지 재시도합니다. Console 컨테이너는 `depends_on.condition: service_healthy` 덕분에 Redpanda가 준비될 때까지 대기합니다. 이렇게 하면 Console이 너무 일찍 시작되어 연결 오류가 발생하는 문제를 방지할 수 있습니다.

#### volumes

```yaml
volumes:
  - redpanda-data:/var/lib/redpanda/data
```

Docker Volume을 사용하면 컨테이너를 삭제하고 재생성해도 토픽과 메시지 데이터가 보존됩니다. Volume을 마운트하지 않으면 `docker-compose down` 시 모든 데이터가 사라지므로, 개발 중 데이터를 유지하려면 필수입니다.

#### Console 환경변수

```yaml
environment:
  CONFIG_FILEPATH: /tmp/config.yml
  CONSOLE_CONFIG_FILE: |
    kafka:
      brokers: ["redpanda:9092"]
      schemaRegistry:
        enabled: true
        urls: ["http://redpanda:8081"]
    redpanda:
      adminApi:
        enabled: true
        urls: ["http://redpanda:9644"]
```

Console은 Kafka 브로커, Schema Registry, Admin API에 접근하여 토픽, 메시지, 스키마를 시각화합니다. Docker 네트워크 내부에서 실행되므로 `redpanda:9092` (internal 주소)를 사용합니다. `localhost`를 사용하면 Console 컨테이너 자신을 가리키므로 연결에 실패합니다.

### 실행 명령어

```bash
# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# Redpanda만 로그 확인
docker-compose logs -f redpanda

# 중지 및 삭제
docker-compose down

# 볼륨까지 삭제 (데이터 완전 삭제)
docker-compose down -v
```

### Console 접속

브라우저에서 `http://localhost:8080`으로 접속하면 Redpanda Console이 열립니다. 여기서 토픽 생성, 메시지 확인, 컨슈머 그룹 모니터링, 스키마 관리 등을 GUI로 수행할 수 있습니다.

---

## 4. Docker Compose (3노드 클러스터)

프로덕션에 가까운 환경을 테스트하려면 3노드 클러스터를 구성합니다. 복제, 파티션 재분배, 리더 선출 등의 분산 시스템 동작을 로컬에서 확인할 수 있습니다.

### docker-compose-cluster.yml

```yaml
version: '3.7'

services:
  redpanda-1:
    image: docker.redpanda.com/redpandadata/redpanda:v25.1.1
    container_name: redpanda-1
    command:
      - redpanda start
      - --node-id 0
      - --smp 1
      - --memory 1G
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:19092
      - --advertise-kafka-addr internal://redpanda-1:9092,external://localhost:19092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:18082
      - --advertise-pandaproxy-addr internal://redpanda-1:8082,external://localhost:18082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:18081
      - --rpc-addr redpanda-1:33145
      - --advertise-rpc-addr redpanda-1:33145
      - --seeds redpanda-1:33145,redpanda-2:33145,redpanda-3:33145
    ports:
      - "19092:19092"
      - "18081:18081"
      - "18082:18082"
      - "9644:9644"
    volumes:
      - redpanda-1-data:/var/lib/redpanda/data
    networks:
      - redpanda-network

  redpanda-2:
    image: docker.redpanda.com/redpandadata/redpanda:v25.1.1
    container_name: redpanda-2
    command:
      - redpanda start
      - --node-id 1
      - --smp 1
      - --memory 1G
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:29092
      - --advertise-kafka-addr internal://redpanda-2:9092,external://localhost:29092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:28082
      - --advertise-pandaproxy-addr internal://redpanda-2:8082,external://localhost:28082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:28081
      - --rpc-addr redpanda-2:33145
      - --advertise-rpc-addr redpanda-2:33145
      - --seeds redpanda-1:33145,redpanda-2:33145,redpanda-3:33145
    ports:
      - "29092:29092"
      - "28081:28081"
      - "28082:28082"
      - "9645:9644"
    volumes:
      - redpanda-2-data:/var/lib/redpanda/data
    networks:
      - redpanda-network

  redpanda-3:
    image: docker.redpanda.com/redpandadata/redpanda:v25.1.1
    container_name: redpanda-3
    command:
      - redpanda start
      - --node-id 2
      - --smp 1
      - --memory 1G
      - --overprovisioned
      - --kafka-addr internal://0.0.0.0:9092,external://0.0.0.0:39092
      - --advertise-kafka-addr internal://redpanda-3:9092,external://localhost:39092
      - --pandaproxy-addr internal://0.0.0.0:8082,external://0.0.0.0:38082
      - --advertise-pandaproxy-addr internal://redpanda-3:8082,external://localhost:38082
      - --schema-registry-addr internal://0.0.0.0:8081,external://0.0.0.0:38081
      - --rpc-addr redpanda-3:33145
      - --advertise-rpc-addr redpanda-3:33145
      - --seeds redpanda-1:33145,redpanda-2:33145,redpanda-3:33145
    ports:
      - "39092:39092"
      - "38081:38081"
      - "38082:38082"
      - "9646:9644"
    volumes:
      - redpanda-3-data:/var/lib/redpanda/data
    networks:
      - redpanda-network

  console:
    image: docker.redpanda.com/redpandadata/console:v2.8.0
    container_name: redpanda-console
    ports:
      - "8080:8080"
    environment:
      CONFIG_FILEPATH: /tmp/config.yml
      CONSOLE_CONFIG_FILE: |
        kafka:
          brokers:
            - redpanda-1:9092
            - redpanda-2:9092
            - redpanda-3:9092
          schemaRegistry:
            enabled: true
            urls:
              - http://redpanda-1:8081
              - http://redpanda-2:8081
              - http://redpanda-3:8081
        redpanda:
          adminApi:
            enabled: true
            urls:
              - http://redpanda-1:9644
              - http://redpanda-2:9644
              - http://redpanda-3:9644
    networks:
      - redpanda-network
    depends_on:
      - redpanda-1
      - redpanda-2
      - redpanda-3

volumes:
  redpanda-1-data:
  redpanda-2-data:
  redpanda-3-data:

networks:
  redpanda-network:
    driver: bridge
```

### 클러스터 구성 핵심 포인트

#### node-id와 seeds

```bash
--node-id 0
--seeds redpanda-1:33145,redpanda-2:33145,redpanda-3:33145
```

각 브로커는 고유한 `--node-id`를 가져야 합니다. 0, 1, 2처럼 연속된 정수를 사용합니다. `--seeds` 옵션은 클러스터의 초기 멤버 목록입니다. 새 브로커가 시작되면 seed 목록의 브로커에 연결하여 클러스터에 참여하고 메타데이터를 동기화합니다.

모든 브로커가 동일한 seed 목록을 가지므로, 어떤 브로커가 먼저 시작되어도 최종적으로 하나의 클러스터로 형성됩니다. 이는 Raft 합의 알고리즘으로 구현됩니다.

#### 포트 매핑

각 브로커는 서로 다른 external 포트를 사용해야 합니다. 호스트 머신에서 포트 충돌을 방지하기 위함입니다.

| 브로커 | Kafka API | Schema Registry | Pandaproxy | Admin API |
|--------|-----------|-----------------|------------|-----------|
| redpanda-1 | 19092 | 18081 | 18082 | 9644 |
| redpanda-2 | 29092 | 28081 | 28082 | 9645 |
| redpanda-3 | 39092 | 38081 | 38082 | 9646 |

Spring Boot 애플리케이션에서는 `bootstrap-servers: localhost:19092,localhost:29092,localhost:39092`처럼 모든 브로커를 명시하거나, 하나만 지정해도 됩니다 (Kafka 클라이언트가 자동으로 나머지 브로커를 발견합니다).

#### Console 설정

Console은 모든 브로커에 연결하여 클러스터 전체 상태를 보여줍니다.

```yaml
brokers:
  - redpanda-1:9092
  - redpanda-2:9092
  - redpanda-3:9092
```

### 클러스터 테스트

```bash
# 클러스터 실행
docker-compose -f docker-compose-cluster.yml up -d

# 클러스터 상태 확인
docker exec -it redpanda-1 rpk cluster info

# 예상 출력:
# CLUSTER
# =======
# redpanda.7fbd7fb3-3532-42c7-9eb2-3d1c15f59a05
#
# BROKERS
# =======
# ID    HOST        PORT
# 0*    redpanda-1  9092
# 1     redpanda-2  9092
# 2     redpanda-3  9092

# 복제 팩터 3인 토픽 생성
docker exec -it redpanda-1 rpk topic create my-replicated-topic -p 3 -r 3

# 토픽 상세 확인
docker exec -it redpanda-1 rpk topic describe my-replicated-topic
```

복제 팩터 3으로 토픽을 생성하면 각 파티션의 데이터가 3개 브로커에 모두 복제됩니다. 한 브로커가 중단되어도 다른 브로커에서 데이터를 읽을 수 있습니다.

```bash
# redpanda-2 브로커 중지
docker stop redpanda-2

# 여전히 읽기/쓰기 가능
docker exec -it redpanda-1 rpk topic produce my-replicated-topic
# "test message" 입력 후 Ctrl+C

docker exec -it redpanda-1 rpk topic consume my-replicated-topic --offset start --num 1
# 메시지 확인됨

# redpanda-2 재시작
docker start redpanda-2
```

---

## 5. 주요 포트 설명

Redpanda는 여러 프로토콜과 API를 제공하므로 포트가 많습니다. Internal/External 분리로 인해 각 API마다 2개의 포트가 있습니다.

| Port | 서비스 | 설명 | 사용 대상 |
|------|--------|------|-----------|
| **9092** | Kafka API (internal) | Docker 네트워크 내부에서 브로커 간, 컨테이너 간 통신에 사용됩니다. Kafka 프로토콜을 사용하며, 프로듀서/컨슈머가 이 포트로 메시지를 주고받습니다. | Redpanda Console, 같은 Docker 네트워크의 애플리케이션 |
| **19092** | Kafka API (external) | 호스트 머신에서 접근하는 Kafka 포트입니다. Spring Boot 애플리케이션을 로컬에서 실행할 때 `localhost:19092`로 연결합니다. | 개발자 노트북의 Kafka 클라이언트, IDE에서 실행한 애플리케이션 |
| **8081** | Schema Registry (internal) | Avro, Protobuf, JSON Schema를 관리하는 Schema Registry의 내부 포트입니다. Console이 스키마 목록을 조회할 때 사용합니다. | Redpanda Console, 컨테이너 내부 애플리케이션 |
| **18081** | Schema Registry (external) | 호스트 머신에서 Schema Registry REST API에 접근하는 포트입니다. `curl http://localhost:18081/subjects` 같은 명령어로 스키마를 조회할 수 있습니다. | 로컬 개발 환경의 스키마 클라이언트 |
| **8082** | Pandaproxy (internal) | Kafka API를 HTTP/JSON으로 감싼 REST API의 내부 포트입니다. Kafka 클라이언트 라이브러리 없이 HTTP로 메시지를 생산/소비할 수 있습니다. | 내부 마이크로서비스 간 HTTP 통신 |
| **18082** | Pandaproxy (external) | 호스트에서 접근하는 Pandaproxy 포트입니다. `curl http://localhost:18082/topics` 같은 요청으로 토픽 목록을 조회합니다. | Postman, curl, 외부 HTTP 클라이언트 |
| **9644** | Admin API | 클러스터 설정, 브로커 상태, 파티션 재분배 등 관리 작업을 수행하는 REST API입니다. Redpanda Console이 이 API를 호출하여 클러스터 메트릭을 표시합니다. `rpk` CLI도 이 API를 사용합니다. | Redpanda Console, rpk, 운영 자동화 스크립트 |
| **8080** | Redpanda Console | 웹 브라우저로 접속하는 UI 포트입니다. 토픽, 메시지, 컨슈머 그룹, ACL, 스키마를 시각화합니다. | 개발자 웹 브라우저 |
| **33145** | RPC (internal) | 브로커 간 내부 통신에 사용되는 RPC 포트입니다. Raft 합의, 메타데이터 복제, 파티션 리더 선출 등의 작업이 이 포트를 통해 이루어집니다. 클라이언트는 접근하지 않습니다. | Redpanda 브로커 간 통신 |

### 포트 선택 가이드

- **Spring Boot 애플리케이션**: `localhost:19092` (external Kafka API)
- **rpk CLI**: Docker 내부에서 실행하므로 `redpanda:9092` (internal)
- **Console**: Docker 네트워크 내부이므로 `redpanda:9092`, `redpanda:8081`, `redpanda:9644` (모두 internal)
- **Postman/curl**: `localhost:18082` (external Pandaproxy), `localhost:18081` (external Schema Registry)

---

## 6. rpk 기본 명령어 (Docker에서)

`rpk`는 Redpanda의 공식 CLI 도구입니다. Redpanda 컨테이너 안에 포함되어 있으므로 `docker exec`로 실행합니다.

### 클러스터 정보

```bash
# 클러스터 상태 확인
docker exec -it redpanda rpk cluster info

# 브로커 목록, 클러스터 ID, 버전 정보를 보여줍니다.
# 출력 예시:
# CLUSTER
# =======
# redpanda.a1b2c3d4-e5f6-7890-abcd-ef1234567890
#
# BROKERS
# =======
# ID    HOST        PORT
# 0*    redpanda    9092

# 클러스터 헬스체크
docker exec -it redpanda rpk cluster health

# 각 브로커의 상태(Healthy/Unhealthy)를 표시합니다.
```

### 토픽 관리

```bash
# 토픽 목록 조회
docker exec -it redpanda rpk topic list

# 토픽 생성 (파티션 3개, 복제 팩터 1)
docker exec -it redpanda rpk topic create test-topic -p 3

# 복제 팩터를 지정하려면 (클러스터 모드에서만 유효)
docker exec -it redpanda rpk topic create my-replicated-topic -p 3 -r 3

# 토픽 상세 정보
docker exec -it redpanda rpk topic describe test-topic

# 파티션 수, 복제본 위치, 리더 브로커, ISR(In-Sync Replicas)을 보여줍니다.

# 토픽 삭제
docker exec -it redpanda rpk topic delete test-topic
```

### 메시지 생산

```bash
# 메시지 생산 (대화형 모드)
docker exec -it redpanda rpk topic produce test-topic

# 프롬프트가 나타나면 메시지 입력 후 Enter
# 여러 메시지를 입력할 수 있으며, Ctrl+C로 종료

# 한 줄 명령어로 메시지 전송
echo '{"user": "alice", "action": "login"}' | docker exec -i redpanda rpk topic produce test-topic

# 키-값 형식으로 전송
echo 'user1:{"name":"alice"}' | docker exec -i redpanda rpk topic produce test-topic --key-separator ':'
```

### 메시지 소비

```bash
# 토픽의 모든 메시지 소비
docker exec -it redpanda rpk topic consume test-topic --offset start

# 최근 10개 메시지만 소비
docker exec -it redpanda rpk topic consume test-topic --offset start --num 10

# 새로운 메시지만 소비 (tail 모드)
docker exec -it redpanda rpk topic consume test-topic --offset end

# 메시지 키와 헤더 포함하여 출력
docker exec -it redpanda rpk topic consume test-topic --offset start --print-keys --print-headers

# 특정 컨슈머 그룹으로 소비
docker exec -it redpanda rpk topic consume test-topic --group my-consumer-group
```

### 컨슈머 그룹 관리

```bash
# 컨슈머 그룹 목록
docker exec -it redpanda rpk group list

# 컨슈머 그룹 상세 정보
docker exec -it redpanda rpk group describe my-consumer-group

# 각 파티션의 offset, lag를 보여줍니다.

# 컨슈머 그룹 오프셋 리셋
docker exec -it redpanda rpk group seek my-consumer-group --to start
```

### ACL 관리

```bash
# ACL 목록 조회
docker exec -it redpanda rpk acl list

# ACL 추가 (예: user1에게 test-topic 읽기 권한 부여)
docker exec -it redpanda rpk acl create --allow-principal User:user1 --operation read --topic test-topic

# ACL 삭제
docker exec -it redpanda rpk acl delete --allow-principal User:user1 --operation read --topic test-topic
```

---

## 7. Spring Boot 연결 설정

Spring Boot 애플리케이션에서 Docker로 실행 중인 Redpanda에 연결하려면 `application.yml`을 다음과 같이 설정합니다.

### application.yml

```yaml
spring:
  kafka:
    bootstrap-servers: localhost:19092

    consumer:
      group-id: my-app-group
      auto-offset-reset: earliest
      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer
      properties:
        # 세션 타임아웃 (기본 10초, 개발 환경에서 짧게 설정)
        session.timeout.ms: 10000
        # 하트비트 간격
        heartbeat.interval.ms: 3000

    producer:
      key-serializer: org.apache.kafka.common.serialization.StringSerializer
      value-serializer: org.apache.kafka.common.serialization.StringSerializer
      properties:
        # 메시지 압축 (선택)
        compression.type: snappy
        # ACK 설정 (1: 리더만, all: 모든 복제본)
        acks: 1

    # Admin 클라이언트 설정 (토픽 자동 생성 등)
    admin:
      properties:
        bootstrap.servers: localhost:19092
```

### 주요 설정 설명

#### bootstrap-servers

```yaml
bootstrap-servers: localhost:19092
```

Kafka 클라이언트가 최초 연결할 브로커 주소입니다. 클라이언트는 이 주소로 연결한 후 클러스터 메타데이터를 가져와 모든 브로커를 발견합니다. 따라서 클러스터의 모든 브로커를 나열할 필요는 없지만, 고가용성을 위해 여러 브로커를 명시하는 것이 좋습니다.

클러스터 모드에서는 다음과 같이 설정합니다:
```yaml
bootstrap-servers: localhost:19092,localhost:29092,localhost:39092
```

#### auto-offset-reset

```yaml
auto-offset-reset: earliest
```

컨슈머 그룹이 처음 시작되거나 오프셋이 유효하지 않을 때 어디서부터 읽을지 결정합니다.
- `earliest`: 토픽의 처음부터 읽습니다 (개발 환경 권장).
- `latest`: 새로운 메시지만 읽습니다 (프로덕션 일반적).

#### acks

```yaml
acks: 1
```

프로듀서가 메시지를 전송한 후 얼마나 많은 복제본이 확인해야 성공으로 간주할지 결정합니다.
- `0`: 확인 없음 (최고 성능, 메시지 손실 가능).
- `1`: 리더 브로커만 확인 (기본값, 적절한 균형).
- `all` (`-1`): 모든 ISR(In-Sync Replicas) 확인 (최고 안정성, 느림).

### 간단한 Producer/Consumer 예제

#### KafkaProducerConfig.java

```java
@Configuration
public class KafkaProducerConfig {

    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;

    @Bean
    public ProducerFactory<String, String> producerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return new DefaultKafkaProducerFactory<>(configProps);
    }

    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
```

#### MessageProducer.java

```java
@Service
@RequiredArgsConstructor
public class MessageProducer {

    private final KafkaTemplate<String, String> kafkaTemplate;

    public void sendMessage(String topic, String message) {
        kafkaTemplate.send(topic, message)
            .whenComplete((result, ex) -> {
                if (ex == null) {
                    System.out.println("메시지 전송 성공: " + message);
                } else {
                    System.err.println("메시지 전송 실패: " + ex.getMessage());
                }
            });
    }
}
```

#### MessageConsumer.java

```java
@Service
public class MessageConsumer {

    @KafkaListener(topics = "test-topic", groupId = "my-app-group")
    public void consume(String message) {
        System.out.println("수신한 메시지: " + message);
    }
}
```

### 연결 테스트

```bash
# Spring Boot 애플리케이션 실행
./gradlew bootRun

# 또는 IDE에서 실행

# 메시지 전송 (REST API 또는 직접 호출)
curl -X POST http://localhost:8080/send?message=hello

# Redpanda에서 메시지 확인
docker exec -it redpanda rpk topic consume test-topic --offset start --num 1
```

---

## 8. 트러블슈팅

### Container가 시작하자마자 종료되는 경우

**증상**: `docker ps`에 redpanda가 보이지 않음

**원인**: 메모리 부족 또는 잘못된 설정

**해결**:
```bash
# 로그 확인
docker logs redpanda

# 메모리 부족 메시지가 보이면 --memory 값 조정
# docker-compose.yml 수정:
command:
  - --memory 512M  # 1G에서 512M로 축소

# 또는 Docker Desktop 리소스 제한 확인
# Settings → Resources → Memory를 4GB 이상으로 설정
```

### rpk 명령이 연결 실패하는 경우

**증상**: `rpk cluster info` 실행 시 timeout 또는 connection refused

**원인**: advertise 주소가 잘못 설정됨

**해결**:
```bash
# advertise-kafka-addr 확인
docker exec -it redpanda cat /etc/redpanda/redpanda.yaml | grep advertise

# 올바른 설정:
# advertised_kafka_api:
#   - address: redpanda
#     port: 9092
#   - address: localhost
#     port: 19092

# 잘못 설정되었다면 컨테이너 재생성
docker-compose down
# docker-compose.yml 수정 후
docker-compose up -d
```

### Consumer가 연결 안 되는 경우

**증상**: Spring Boot 애플리케이션이 `Connection to node -1 could not be established` 오류 발생

**원인**: external port를 사용하지 않음

**해결**:
```yaml
# application.yml에서 확인
spring:
  kafka:
    bootstrap-servers: localhost:19092  # ✅ 올바름
    # bootstrap-servers: localhost:9092  # ❌ 잘못됨 (internal 포트)
```

```bash
# 포트 포워딩 확인
docker ps | grep redpanda

# PORTS 컬럼에 0.0.0.0:19092->19092/tcp 보여야 함
```

### Redpanda Console이 안 보이는 경우

**증상**: `http://localhost:8080` 접속 시 "Connection refused" 또는 빈 화면

**원인**: Console이 Redpanda의 healthcheck를 통과하지 못함

**해결**:
```bash
# Console 로그 확인
docker-compose logs console

# Redpanda healthcheck 상태 확인
docker inspect redpanda | grep Health -A 10

# healthcheck가 실패하면 Redpanda 로그 확인
docker-compose logs redpanda

# healthcheck 통과 대기 (최대 75초)
# start_period(5s) + interval(15s) * retries(5) = 80s

# 즉시 확인하려면
docker exec -it redpanda rpk cluster health
# 출력: Healthy: true 나올 때까지 대기
```

### 메시지가 사라지는 경우

**증상**: 메시지를 전송했는데 소비할 수 없음

**원인**: 토픽의 retention 설정이 너무 짧거나, 컨테이너를 volume 없이 재시작함

**해결**:
```bash
# 토픽 retention 설정 확인
docker exec -it redpanda rpk topic describe test-topic

# retention.ms가 짧으면 수정
docker exec -it redpanda rpk topic alter-config test-topic --set retention.ms=604800000
# 604800000ms = 7일

# volume 확인
docker volume ls | grep redpanda

# volume이 없다면 docker-compose.yml에 추가
volumes:
  - redpanda-data:/var/lib/redpanda/data
```

### 디스크 공간 부족

**증상**: "No space left on device" 오류

**해결**:
```bash
# Docker 볼륨 정리
docker volume prune

# 사용하지 않는 이미지/컨테이너 정리
docker system prune -a

# Redpanda 로그 크기 제한
# docker-compose.yml에 추가:
services:
  redpanda:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 9. 다음 단계

Docker로 Redpanda를 실행하는 방법을 익혔다면, 다음 주제로 넘어갈 수 있습니다:

1. **Helm으로 Kubernetes 배포**: 프로덕션 환경을 위한 StatefulSet, PersistentVolume, TLS 설정
2. **모니터링 설정**: Prometheus와 Grafana로 메트릭 수집 및 시각화
3. **보안 강화**: SASL/SCRAM 인증, ACL 설정, TLS 암호화
4. **성능 튜닝**: 파티션 수, 복제 팩터, 배치 크기 최적화
5. **스키마 관리**: Schema Registry로 Avro/Protobuf 스키마 버전 관리

---

## 참고 자료

- [Redpanda 공식 문서](https://docs.redpanda.com/)
- [Redpanda Docker 빠른 시작](https://docs.redpanda.com/current/get-started/quick-start/)
- [rpk 명령어 레퍼런스](https://docs.redpanda.com/current/reference/rpk/)
- [Kafka 프로토콜 호환성](https://docs.redpanda.com/current/reference/compatibility/)
