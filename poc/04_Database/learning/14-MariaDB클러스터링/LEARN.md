# Ch.14 - MariaDB 클러스터링

> **이론 매핑**: 신규 작성 (Ch.12 복제/샤딩/합의 이론을 MariaDB 생태계에 적용)

---

## 핵심 요약

> MariaDB의 클러스터링 생태계는 PostgreSQL과 근본적으로 다른 철학을 갖는다. 가장 큰 차이는 **Galera Cluster**가 제공하는 동기식 Multi-Master 복제이다. PostgreSQL이 Single-Leader 기반 HA에 초점을 맞추는 반면, Galera는 모든 노드에서 읽기와 쓰기가 가능한 Multi-Master 구조를 제공한다. 여기에 **MaxScale** 프록시가 지능적 라우팅과 자동 Failover를 담당하고, **Semi-synchronous Replication**과 **Group Replication**이 추가 옵션을 제공한다. 이 장에서는 각 기술의 원리를 이해하고, PostgreSQL 클러스터링과의 차이를 비교한다.

---

## 학습 목표

1. Galera Cluster의 가상 동기(virtually synchronous) 복제 원리를 설명할 수 있다
2. Certification-based replication이 충돌을 감지하고 해결하는 방식을 이해할 수 있다
3. MaxScale의 라우팅 알고리즘과 자동 Failover 메커니즘을 설명할 수 있다
4. Semi-synchronous Replication의 동작과 한계를 이해할 수 있다
5. MariaDB와 PostgreSQL 클러스터링 기능을 비교하고 적절한 선택을 할 수 있다

---

## 실습 환경

| 항목 | Docker (실습용) | Kubernetes (학습용) |
|------|----------------|-------------------|
| 구성 방식 | docker-compose.yml | Operator + CRD |
| MariaDB HA | Galera 3-node compose | mariadb-operator |
| 프록시 | MaxScale 컨테이너 | Service + Ingress |
| 모니터링 | Prometheus + Grafana compose | kube-prometheus-stack |

---

## 본문

### 1. MariaDB 복제 개요

MariaDB는 MySQL에서 포크된 데이터베이스이므로, MySQL의 복제 메커니즘을 기반으로 확장된 여러 복제 방식을 제공한다. 각 방식은 Ch.12에서 배운 이론적 분류와 직접 대응된다.

| MariaDB 복제 방식 | Ch.12 이론 분류 | 특징 |
|-------------------|----------------|------|
| 비동기 복제 (기본) | Single-Leader, 비동기 | 가장 단순, 데이터 유실 가능 |
| Semi-synchronous | Single-Leader, 반동기 | 최소 1개 Replica 확인 후 커밋 |
| Galera Cluster | Multi-Leader, 가상 동기 | 모든 노드 쓰기 가능, Certification 기반 |
| Group Replication (MySQL 호환) | Multi-Leader/Single-Leader | Paxos 기반 합의 |

---

### 2. Galera Cluster: 동기식 Multi-Master

Galera Cluster는 MariaDB 클러스터링의 핵심이다. Ch.12에서 배운 Multi-Leader 복제를 **가상 동기(virtually synchronous)** 방식으로 구현하여, 모든 노드에서 읽기와 쓰기가 가능하면서도 노드 간 데이터 일관성을 보장한다.

"가상 동기"란 트랜잭션 커밋 시점에 모든 노드가 해당 변경을 **인증(certify)**하지만, 실제 적용(apply)은 비동기로 진행된다는 뜻이다. 인증은 동기적이고 적용은 비동기적이므로, 순수 동기식보다 빠르면서 일관성을 유지한다.

#### 2.1 Certification-based Replication

Galera의 핵심 메커니즘은 Certification-based Replication이다. 이는 Ch.12에서 배운 충돌 해결 전략 중 "충돌 감지 후 거부"에 해당한다. LWW처럼 하나를 채택하는 것이 아니라, 충돌이 감지되면 뒤늦은 트랜잭션을 **롤백**시킨다.

```
┌─────────────────────────────────────────────────────────────┐
│              Galera Certification 프로세스                     │
│                                                               │
│  Node A                  Group                  Node B        │
│    │                  Communication                │          │
│    │                     System                    │          │
│    │                                               │          │
│  [1] BEGIN                                         │          │
│  [2] INSERT INTO t VALUES(1, 'a')                  │          │
│  [3] COMMIT 요청                                    │          │
│    │                                               │          │
│    │──── Write Set 전송 ────→│                     │          │
│    │    (변경된 행 + PK)      │                     │          │
│    │                         │──── Write Set ────→ │          │
│    │                         │     브로드캐스트      │          │
│    │                         │                     │          │
│    │←── Certification ──────│──── Certification ──→│          │
│    │    결과: PASS/FAIL      │    결과: PASS/FAIL   │          │
│    │                         │                     │          │
│  [4] PASS → 커밋 완료       │                   [4] PASS      │
│      FAIL → 롤백            │                   → 비동기 적용  │
│                              │                     │          │
└─────────────────────────────────────────────────────────────┘
```

**Certification 판정 규칙:**

1. 트랜잭션 커밋 시점에 Write Set(변경된 행의 Primary Key + 변경 데이터)을 모든 노드에 브로드캐스트한다
2. 각 노드는 수신한 Write Set의 PK가 현재 진행 중인 다른 트랜잭션과 겹치는지 검사한다
3. 겹치지 않으면 PASS → 커밋 허용
4. 겹치면 FAIL → 나중에 도착한 트랜잭션 롤백 (먼저 도착한 것이 승리)

이 방식의 핵심 장점은 **분산 잠금(distributed lock)이 불필요**하다는 것이다. 각 노드는 로컬에서 자유롭게 트랜잭션을 실행하고, 커밋 시점에만 전체 클러스터와 조율한다. 이를 "낙관적 동시성 제어(optimistic concurrency control)"라고 부른다.

#### 2.2 Galera의 상태 전송: SST와 IST

새 노드가 클러스터에 합류하거나, 오랫동안 분리되었던 노드가 재합류할 때 상태 동기화가 필요하다.

| 방식 | 이름 | 동작 | 사용 시점 |
|------|------|------|----------|
| SST | State Snapshot Transfer | 전체 데이터 스냅샷 전송 | 신규 노드, 오래 분리된 노드 |
| IST | Incremental State Transfer | 누락된 Write Set만 전송 | 짧은 분리 후 재합류 |

SST 방법은 세 가지이다:
- **rsync**: 빠르지만 Donor 노드가 잠김(읽기 불가)
- **mariabackup**: Donor 노드 잠김 없이 핫 백업 (권장)
- **mysqldump**: 논리적 덤프, 느리지만 버전 호환성 좋음

IST는 Galera의 GCache(Group Cache)에 저장된 최근 Write Set을 전송한다. GCache 크기(`gcache.size`)가 누락된 Write Set을 모두 포함하면 IST로 빠르게 복구되고, 그렇지 않으면 SST로 전체 동기화를 해야 한다.

#### 2.3 Flow Control

Galera에서 한 노드의 적용(apply)이 느려지면 전체 클러스터 성능에 영향을 줄 수 있다. Flow Control은 뒤처진 노드가 다른 노드의 커밋 속도를 제한하는 메커니즘이다.

```
Node A (빠름): [TX1] [TX2] [TX3] [TX4] [TX5] ...
Node B (느림): [TX1] [TX2] ← 큐 쌓임
Node C (보통): [TX1] [TX2] [TX3] ...

Node B의 적용 큐가 gcs.fc_limit(기본 16) 초과
→ Node B가 Flow Control 메시지 전송
→ 모든 노드의 복제 일시 중지
→ Node B가 따라잡으면 재개
```

Flow Control이 자주 발동하면 전체 클러스터 처리량이 가장 느린 노드에 맞춰진다. 이것이 Galera의 근본적 트레이드오프 중 하나이다. 노드 간 하드웨어 스펙과 네트워크 지연을 최대한 균일하게 맞추는 것이 중요한 이유이다.

#### 2.4 Docker Compose로 Galera 3-Node 구성

```yaml
# docker-compose-galera.yml
version: '3.8'

services:
  galera-node1:
    image: mariadb:11.2
    container_name: galera-node1
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: mydb
      MYSQL_USER: app
      MYSQL_PASSWORD: apppass
    command: >
      --wsrep-on=ON
      --wsrep-provider=/usr/lib/galera/libgalera_smm.so
      --wsrep-cluster-address=gcomm://
      --wsrep-cluster-name=my_galera
      --wsrep-node-name=node1
      --wsrep-node-address=galera-node1
      --wsrep-sst-method=mariabackup
      --wsrep-sst-auth=root:rootpass
      --binlog-format=ROW
      --default-storage-engine=InnoDB
      --innodb-autoinc-lock-mode=2
      --innodb-flush-log-at-trx-commit=0
      --wsrep-slave-threads=4
    ports:
      - "3306:3306"
      - "4567:4567"
      - "4568:4568"
      - "4444:4444"
    volumes:
      - galera_node1_data:/var/lib/mysql
    networks:
      - galera-net
    healthcheck:
      test: ["CMD", "mariadb", "-uroot", "-prootpass", "-e", "SHOW STATUS LIKE 'wsrep_ready'"]
      interval: 10s
      timeout: 5s
      retries: 5

  galera-node2:
    image: mariadb:11.2
    container_name: galera-node2
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
    command: >
      --wsrep-on=ON
      --wsrep-provider=/usr/lib/galera/libgalera_smm.so
      --wsrep-cluster-address=gcomm://galera-node1,galera-node2,galera-node3
      --wsrep-cluster-name=my_galera
      --wsrep-node-name=node2
      --wsrep-node-address=galera-node2
      --wsrep-sst-method=mariabackup
      --wsrep-sst-auth=root:rootpass
      --binlog-format=ROW
      --default-storage-engine=InnoDB
      --innodb-autoinc-lock-mode=2
      --innodb-flush-log-at-trx-commit=0
      --wsrep-slave-threads=4
    ports:
      - "3307:3306"
    volumes:
      - galera_node2_data:/var/lib/mysql
    depends_on:
      galera-node1:
        condition: service_healthy
    networks:
      - galera-net

  galera-node3:
    image: mariadb:11.2
    container_name: galera-node3
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
    command: >
      --wsrep-on=ON
      --wsrep-provider=/usr/lib/galera/libgalera_smm.so
      --wsrep-cluster-address=gcomm://galera-node1,galera-node2,galera-node3
      --wsrep-cluster-name=my_galera
      --wsrep-node-name=node3
      --wsrep-node-address=galera-node3
      --wsrep-sst-method=mariabackup
      --wsrep-sst-auth=root:rootpass
      --binlog-format=ROW
      --default-storage-engine=InnoDB
      --innodb-autoinc-lock-mode=2
      --innodb-flush-log-at-trx-commit=0
      --wsrep-slave-threads=4
    ports:
      - "3308:3306"
    volumes:
      - galera_node3_data:/var/lib/mysql
    depends_on:
      galera-node1:
        condition: service_healthy
    networks:
      - galera-net

volumes:
  galera_node1_data:
  galera_node2_data:
  galera_node3_data:

networks:
  galera-net:
    driver: bridge
```

**주의**: 첫 번째 노드(`galera-node1`)의 `--wsrep-cluster-address=gcomm://`은 빈 주소로, 이 노드가 클러스터를 부트스트랩한다는 의미이다. 클러스터가 구성된 후에는 모든 노드의 주소를 포함하도록 변경해야 한다.

**필수 설정 설명:**

| 설정 | 값 | 이유 |
|------|---|------|
| `binlog-format` | ROW | Galera는 행 기반 복제만 지원 |
| `innodb-autoinc-lock-mode` | 2 (interleaved) | Multi-Master에서 AUTO_INCREMENT 충돌 방지 |
| `innodb-flush-log-at-trx-commit` | 0 | 성능 최적화 (Galera가 내구성 보장) |
| `wsrep-slave-threads` | 4 | 병렬 적용 스레드 수 (CPU 코어에 맞춤) |

Galera 포트 용도:

| 포트 | 용도 |
|------|------|
| 3306 | MySQL 클라이언트 연결 |
| 4567 | Galera 클러스터 통신 (Group Communication) |
| 4568 | IST (Incremental State Transfer) |
| 4444 | SST (State Snapshot Transfer) |

---

### 3. MaxScale: 지능형 프록시

MaxScale은 MariaDB Corporation이 개발한 데이터베이스 프록시이다. Ch.13의 pgpool-II와 유사한 역할을 하지만, 더 정교한 라우팅 알고리즘과 Galera 전용 모니터링을 제공한다.

#### 3.1 아키텍처

```
┌──────────┐     ┌────────────────────────────────┐     ┌──────────────┐
│ Client 1 │────→│          MaxScale               │────→│ Galera Node1 │
│ Client 2 │────→│                                  │────→│ Galera Node2 │
│ Client 3 │────→│  ┌──────────┐  ┌─────────────┐ │────→│ Galera Node3 │
└──────────┘     │  │ Monitor  │  │   Router    │ │     └──────────────┘
                 │  │ (상태감시)│  │ (쿼리분배)  │ │
                 │  └──────────┘  └─────────────┘ │
                 │  ┌──────────┐  ┌─────────────┐ │
                 │  │ Filter   │  │   Listener  │ │
                 │  │ (쿼리변환)│  │ (포트바인딩) │ │
                 │  └──────────┘  └─────────────┘ │
                 └────────────────────────────────┘
```

MaxScale의 핵심 컴포넌트:

| 컴포넌트 | 역할 |
|---------|------|
| **Monitor** | 백엔드 서버 상태를 주기적으로 확인 (galeramon, mariadbmon) |
| **Router** | 쿼리를 적절한 서버로 라우팅 |
| **Filter** | 쿼리 로깅, 변환, 방화벽 등 |
| **Listener** | 클라이언트 연결을 받는 포트 |

#### 3.2 라우팅 알고리즘

| Router | 동작 | 사용 사례 |
|--------|------|----------|
| **readwritesplit** | SELECT → Replica, 나머지 → Primary | 가장 일반적인 읽기/쓰기 분리 |
| **readconnroute** | 연결 단위로 서버 할당 | 단순 로드밸런싱 |
| **schemarouter** | 스키마(DB) 별로 서버 할당 | 멀티테넌트 |

`readwritesplit`은 SQL 파싱 없이 트랜잭션 상태를 추적하여 라우팅한다. 트랜잭션 내부의 모든 쿼리는 같은 서버(Primary)로 전송되고, 트랜잭션 밖의 SELECT만 Replica로 분산된다.

#### 3.3 Docker Compose에 MaxScale 추가

```yaml
# 위의 galera compose에 추가
  maxscale:
    image: mariadb/maxscale:latest
    container_name: maxscale
    ports:
      - "4006:4006"   # Read/Write Split
      - "4008:4008"   # Read Only
      - "8989:8989"   # MaxScale REST API
    volumes:
      - ./maxscale.cnf:/etc/maxscale.cnf:ro
    depends_on:
      - galera-node1
      - galera-node2
      - galera-node3
    networks:
      - galera-net
```

MaxScale 설정 파일(`maxscale.cnf`):

```ini
[maxscale]
threads=auto
admin_host=0.0.0.0
admin_port=8989

# 서버 정의
[node1]
type=server
address=galera-node1
port=3306
protocol=MariaDBBackend

[node2]
type=server
address=galera-node2
port=3306
protocol=MariaDBBackend

[node3]
type=server
address=galera-node3
port=3306
protocol=MariaDBBackend

# Galera 모니터
[Galera-Monitor]
type=monitor
module=galeramon
servers=node1,node2,node3
user=maxscale_monitor
password=monitor_pass
monitor_interval=2000
use_priority=true
available_when_donor=true

# Read/Write Split Router
[RW-Split-Service]
type=service
router=readwritesplit
servers=node1,node2,node3
user=maxscale_router
password=router_pass
master_reconnection=true
transaction_replay=true
transaction_replay_max_size=1Mi

# Read/Write Split Listener
[RW-Split-Listener]
type=listener
service=RW-Split-Service
protocol=MariaDBClient
port=4006

# Read Only Router
[RO-Service]
type=service
router=readconnroute
router_options=slave
servers=node1,node2,node3
user=maxscale_router
password=router_pass

# Read Only Listener
[RO-Listener]
type=listener
service=RO-Service
protocol=MariaDBClient
port=4008
```

MaxScale용 사용자 생성 (Galera 노드에서 실행):

```sql
CREATE USER 'maxscale_monitor'@'%' IDENTIFIED BY 'monitor_pass';
GRANT REPLICATION CLIENT, SUPER, RELOAD ON *.* TO 'maxscale_monitor'@'%';

CREATE USER 'maxscale_router'@'%' IDENTIFIED BY 'router_pass';
GRANT SELECT ON mysql.user TO 'maxscale_router'@'%';
GRANT SELECT ON mysql.db TO 'maxscale_router'@'%';
GRANT SELECT ON mysql.tables_priv TO 'maxscale_router'@'%';
GRANT SELECT ON mysql.columns_priv TO 'maxscale_router'@'%';
GRANT SELECT ON mysql.proxies_priv TO 'maxscale_router'@'%';
GRANT SELECT ON mysql.roles_mapping TO 'maxscale_router'@'%';
GRANT SHOW DATABASES ON *.* TO 'maxscale_router'@'%';
```

---

### 4. Semi-synchronous Replication

Semi-synchronous Replication은 기본 비동기 복제와 완전 동기 복제의 중간이다. Primary가 트랜잭션을 커밋할 때, **최소 1개의 Replica가 바이너리 로그를 수신했음을 확인**한 후 클라이언트에 응답한다.

```
Client → Primary: COMMIT
         Primary → Replica: 바이너리 로그 전송
         Primary ← Replica: ACK (수신 확인)
Client ← Primary: OK

※ Replica가 "수신"했을 뿐, "적용"은 보장하지 않음
```

| 비교 | 비동기 | Semi-sync | Galera |
|------|--------|-----------|--------|
| 커밋 조건 | Primary 로컬 기록 | 1+ Replica 수신 확인 | 전 노드 Certification |
| 데이터 손실 | 가능 | 거의 없음 | 없음 |
| 쓰기 지연 | 최소 | 네트워크 RTT 추가 | Certification 오버헤드 |
| Multi-Master | 불가 | 불가 | 가능 |

Semi-sync의 한계는 타임아웃이다. Replica가 설정된 시간(`rpl_semi_sync_master_timeout`, 기본 10초) 내에 ACK를 보내지 않으면 **자동으로 비동기 모드로 전환**된다. 이후 Replica가 복구되면 다시 Semi-sync로 돌아온다. 이 전환 과정에서 데이터 유실이 발생할 수 있다.

```sql
-- Semi-sync 활성화 (Primary)
INSTALL SONAME 'semisync_master';
SET GLOBAL rpl_semi_sync_master_enabled = 1;
SET GLOBAL rpl_semi_sync_master_timeout = 10000;  -- 10초

-- Semi-sync 활성화 (Replica)
INSTALL SONAME 'semisync_slave';
SET GLOBAL rpl_semi_sync_slave_enabled = 1;
```

---

### 5. Kubernetes에서의 MariaDB 클러스터링

#### 5.1 mariadb-operator

mariadb-operator는 Kubernetes에서 MariaDB와 Galera Cluster를 선언적으로 관리하는 Operator이다.

```
┌─────────────────────────────────────────────────────────┐
│                Kubernetes Cluster                        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │            mariadb-operator (Controller)            │ │
│  │   MariaDB CRD 감시 → Galera 클러스터 관리           │ │
│  └────────────────────┬───────────────────────────────┘ │
│                       │                                  │
│  ┌────────────────────▼───────────────────────────────┐ │
│  │                   StatefulSet                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │ │
│  │  │ Pod 0    │  │ Pod 1    │  │ Pod 2    │         │ │
│  │  │ Galera   │  │ Galera   │  │ Galera   │         │ │
│  │  │ Node     │  │ Node     │  │ Node     │         │ │
│  │  │ + PVC    │  │ + PVC    │  │ + PVC    │         │ │
│  │  └──────────┘  └──────────┘  └──────────┘         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─────────────────┐  ┌──────────────────┐              │
│  │ Service (rw)    │  │ MaxScale (선택)  │              │
│  │ → 모든 Galera   │  │ → 읽기/쓰기 분리 │              │
│  └─────────────────┘  └──────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

mariadb-operator CRD 예시:

```yaml
apiVersion: k8s.mariadb.com/v1alpha1
kind: MariaDB
metadata:
  name: mariadb-galera
spec:
  rootPasswordSecretKeyRef:
    name: mariadb-root
    key: password
  image: mariadb:11.2

  galera:
    enabled: true
    sst: mariabackup
    replicaThreads: 4
    agent:
      image: ghcr.io/mariadb-operator/mariadb-operator:latest
      gracefulShutdownTimeout: 5s

  replicas: 3

  storage:
    size: 10Gi
    storageClassName: standard

  service:
    type: ClusterIP

  metrics:
    enabled: true
    exporter:
      image: prom/mysqld-exporter:latest

  primaryService:
    type: ClusterIP
  secondaryService:
    type: ClusterIP
```

MaxScale도 CRD로 배포할 수 있다:

```yaml
apiVersion: k8s.mariadb.com/v1alpha1
kind: MaxScale
metadata:
  name: maxscale
spec:
  image: mariadb/maxscale:latest
  replicas: 2

  mariaDbRef:
    name: mariadb-galera

  services:
    - name: rw-router
      router: readwritesplit
      listener:
        port: 4006
    - name: ro-router
      router: readconnroute
      params:
        router_options: slave
      listener:
        port: 4008

  monitor:
    module: galeramon
    interval: 2s
```

#### 5.2 Docker vs Kubernetes 배포 비교

| 항목 | Docker Compose | Kubernetes (mariadb-operator) |
|------|---------------|-------------------------------|
| 부트스트랩 | 첫 노드 `gcomm://` 수동 설정 | Operator가 자동 관리 |
| SST/IST | 수동 설정 | CRD에서 선언적 설정 |
| 스케일링 | compose 파일 수정 | `kubectl scale` 또는 CRD replicas 변경 |
| 백업 | cron + mariabackup 수동 | Operator 내장 CronJob |
| MaxScale | 별도 컨테이너 + 설정 파일 | MaxScale CRD로 선언적 관리 |
| 모니터링 | 별도 Prometheus 구성 | metrics 옵션 활성화로 자동 |
| 클러스터 복구 | 수동 (부트스트랩 노드 선택) | Operator 자동 복구 시도 |
| 적합 환경 | 개발, 테스트 | 스테이징, 프로덕션 |

---

### 6. MariaDB vs PostgreSQL 클러스터링 비교

이 비교는 Ch.13과 Ch.14의 핵심 내용을 종합하는 것이다.

#### 6.1 HA 아키텍처 비교

```
PostgreSQL HA (Patroni)              MariaDB HA (Galera)
┌─────────────────────┐              ┌─────────────────────┐
│      etcd 클러스터    │              │  (외부 의존성 없음)  │
│   (합의 기반 리더선출)  │              │                     │
└──────────┬──────────┘              │                     │
           │                         │                     │
   ┌───────▼───────┐                ┌▼─────┐ ┌─────┐ ┌───▼─┐
   │ Primary (R/W) │                │Node1 │ │Node2│ │Node3│
   │    Patroni    │                │(R/W) │ │(R/W)│ │(R/W)│
   ├───────────────┤                └──────┘ └─────┘ └─────┘
   │Standby 1 (R)  │                    모든 노드가 R/W
   │Standby 2 (R)  │
   └───────────────┘
    하나의 Primary만 R/W
```

#### 6.2 기능 비교 테이블

| 비교 항목 | PostgreSQL (Patroni + Streaming) | MariaDB (Galera Cluster) |
|----------|--------------------------------|--------------------------|
| 복제 모델 | Single-Leader | Multi-Master |
| 쓰기 가능 노드 | 1개 (Primary만) | 전체 노드 |
| 복제 방식 | WAL 스트리밍 (물리) | Write Set 인증 (논리) |
| 일관성 | 강한 (동기 설정 시) | 가상 동기 (Certification) |
| Failover | Patroni + etcd 자동 (30~40초) | 자동 (노드 탈퇴 감지 즉시) |
| Split Brain 방지 | etcd 합의 | Quorum 기반 (과반수 생존) |
| 충돌 해결 | 불필요 (Single-Leader) | Certification (뒤늦은 TX 롤백) |
| 읽기 확장 | Standby 추가 | 모든 노드에서 읽기 |
| 쓰기 확장 | 불가 (Citus 필요) | 제한적 (Certification 오버헤드) |
| DDL 복제 | Streaming: 자동 | Galera: TOI(Total Order Isolation) |
| 수평 샤딩 | Citus | 네이티브 미지원 (ProxySQL 등 외부) |
| K8s Operator | CloudNativePG, Zalando | mariadb-operator |
| 프록시 | HAProxy, pgpool-II | MaxScale, ProxySQL |
| 장점 | 단순한 모델, 강한 일관성, 풍부한 SQL 기능 | Multi-Master, 빠른 Failover, 쓰기 분산 |
| 단점 | 쓰기 확장 제한, Failover 시간 | Certification 오버헤드, InnoDB만 지원, DDL 잠금 |

#### 6.3 선택 가이드

| 상황 | 권장 |
|------|------|
| 복잡한 SQL, 고급 데이터 타입(JSON, GIS) 필요 | PostgreSQL |
| 모든 노드에서 쓰기가 필요한 Multi-DC 배포 | MariaDB (Galera) |
| 읽기 >> 쓰기, 강한 일관성 필수 | PostgreSQL (Patroni) |
| 빠른 Failover가 최우선 (수초 이내) | MariaDB (Galera) |
| 수평 샤딩으로 대규모 데이터 처리 | PostgreSQL (Citus) |
| MySQL 호환성이 필요한 레거시 마이그레이션 | MariaDB |
| 풍부한 확장 생태계 (PostGIS, TimescaleDB 등) | PostgreSQL |

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| Galera Cluster | Certification 기반 가상 동기 Multi-Master - 모든 노드에서 읽기/쓰기가 가능하다 |
| Certification | 커밋 시점에 Write Set의 PK 충돌을 검사해 뒤늦은 트랜잭션을 롤백한다 |
| SST/IST | 전체 스냅샷 전송(SST)과 증분 Write Set 전송(IST)으로 노드를 동기화한다 |
| Flow Control | 느린 노드가 클러스터 전체 속도를 제한하는 메커니즘이다 |
| MaxScale | SQL 파싱 없이 트랜잭션 상태를 추적하여 읽기/쓰기를 분리하는 프록시이다 |
| Semi-sync | 최소 1개 Replica의 수신 확인 후 커밋하는 절충 방식이다 |
| mariadb-operator | Kubernetes에서 Galera + MaxScale을 CRD로 선언적 관리한다 |
| PG vs MariaDB | Single-Leader(PG) vs Multi-Master(Galera)가 근본적 아키텍처 차이이다 |
