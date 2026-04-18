# Ch.13 - PostgreSQL 클러스터링

> **이론 매핑**: 신규 작성 (Ch.12 복제/샤딩/합의 이론을 PostgreSQL 생태계에 적용)

---

## 핵심 요약

> PostgreSQL은 단일 노드 성능이 강력하지만, 고가용성(HA)과 수평 확장이 필요한 프로덕션 환경에서는 클러스터링이 필수이다. PostgreSQL 생태계의 클러스터링은 크게 **Streaming Replication**(물리 복제), **Logical Replication**(논리 복제), **Patroni + etcd**(HA 자동화), **Citus**(분산 확장), **pgpool-II**(커넥션 풀링/로드밸런싱) 다섯 가지 축으로 구성된다. 이 장에서는 각 기술의 원리를 이해하고, Docker Compose와 Kubernetes 환경에서의 배포 차이를 학습한다.

---

## 학습 목표

1. Streaming Replication의 동기/비동기 모드 차이를 설명하고 설정할 수 있다
2. Logical Replication의 Pub/Sub 모델과 사용 사례를 이해할 수 있다
3. Patroni + etcd로 자동 Failover가 동작하는 원리를 설명할 수 있다
4. Citus의 분산 테이블 개념과 샤딩 방식을 이해할 수 있다
5. Docker Compose와 Kubernetes Operator 배포의 차이를 비교할 수 있다

---

## 실습 환경

| 항목 | Docker (실습용) | Kubernetes (학습용) |
|------|----------------|-------------------|
| 구성 방식 | docker-compose.yml | Operator + CRD |
| PostgreSQL HA | Patroni + etcd 컨테이너 | CloudNativePG / Zalando Operator |
| PostgreSQL 분산 | Citus 컨테이너 | Citus Operator |
| 프록시 | pgpool-II 컨테이너 | Service + Ingress |
| 모니터링 | Prometheus + Grafana compose | kube-prometheus-stack |

---

## 본문

### 1. Streaming Replication (물리 복제)

Streaming Replication은 PostgreSQL의 기본 내장 복제 기능이다. Ch.12에서 배운 **Single-Leader 복제**를 WAL(Write-Ahead Log) 기반으로 구현한 것이다. Primary가 WAL 레코드를 생성하면, Standby가 이를 스트림으로 받아 재생(replay)한다.

#### 1.1 동작 원리

```
┌─────────────┐    WAL Stream    ┌─────────────┐
│   Primary   │ ──────────────→  │  Standby 1  │ (Hot Standby: 읽기 가능)
│             │ ──────────────→  │  Standby 2  │
│  WAL Writer │                  │  WAL Receiver│
│      ↓      │                  │      ↓      │
│  WAL Files  │                  │  WAL Replay │
└─────────────┘                  └─────────────┘
```

WAL은 데이터 변경 전에 로그를 먼저 기록하는 메커니즘이다. 이 로그를 네트워크로 전송하여 Standby에서 동일한 변경을 재생하므로, Standby는 Primary의 물리적 복사본이 된다. Ch.12에서 배운 "WAL Shipping" 복제 로그 구현 방식이 바로 이것이다.

#### 1.2 동기 vs 비동기 모드

| 모드 | `synchronous_commit` | 장점 | 단점 |
|------|---------------------|------|------|
| 비동기 (async) | `off` 또는 `local` | 빠른 응답, Primary 성능 영향 없음 | Failover 시 데이터 유실 가능 |
| 원격 쓰기 (remote_write) | `remote_write` | Standby OS 버퍼까지 도달 보장 | Standby 크래시 시 유실 가능 |
| 원격 적용 (remote_apply) | `remote_apply` | Standby에서 읽기 가능 상태 보장 | 가장 높은 지연 |
| 동기 (on) | `on` | Standby WAL 디스크 기록 보장 | 높은 지연, Standby 장애 시 쓰기 차단 |

`synchronous_standby_names` 파라미터로 동기 대상 Standby를 지정한다. `FIRST 1 (standby1, standby2)` 설정은 두 Standby 중 먼저 응답하는 하나만 동기식으로 동작하는 반동기식 구성이다.

#### 1.3 Docker Compose로 Streaming Replication 구성

```yaml
# docker-compose-streaming.yml
version: '3.8'

services:
  pg-primary:
    image: postgres:16
    container_name: pg-primary
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    command: >
      postgres
        -c wal_level=replica
        -c max_wal_senders=3
        -c max_replication_slots=3
        -c synchronous_commit=on
        -c synchronous_standby_names='FIRST 1 (standby1, standby2)'
    ports:
      - "5432:5432"
    volumes:
      - pg_primary_data:/var/lib/postgresql/data
      - ./init-primary.sh:/docker-entrypoint-initdb.d/init-primary.sh
    networks:
      - pg-cluster

  pg-standby1:
    image: postgres:16
    container_name: pg-standby1
    environment:
      PGUSER: replicator
      PGPASSWORD: repl_password
    command: >
      bash -c "
        until pg_basebackup -h pg-primary -D /var/lib/postgresql/data -U replicator -Fp -Xs -P -R; do
          echo 'Waiting for primary...'
          sleep 2
        done
        echo \"primary_conninfo = 'host=pg-primary port=5432 user=replicator password=repl_password application_name=standby1'\" >> /var/lib/postgresql/data/postgresql.auto.conf
        postgres
      "
    depends_on:
      - pg-primary
    ports:
      - "5433:5432"
    volumes:
      - pg_standby1_data:/var/lib/postgresql/data
    networks:
      - pg-cluster

  pg-standby2:
    image: postgres:16
    container_name: pg-standby2
    environment:
      PGUSER: replicator
      PGPASSWORD: repl_password
    command: >
      bash -c "
        until pg_basebackup -h pg-primary -D /var/lib/postgresql/data -U replicator -Fp -Xs -P -R; do
          echo 'Waiting for primary...'
          sleep 2
        done
        echo \"primary_conninfo = 'host=pg-primary port=5432 user=replicator password=repl_password application_name=standby2'\" >> /var/lib/postgresql/data/postgresql.auto.conf
        postgres
      "
    depends_on:
      - pg-primary
    ports:
      - "5434:5432"
    volumes:
      - pg_standby2_data:/var/lib/postgresql/data
    networks:
      - pg-cluster

volumes:
  pg_primary_data:
  pg_standby1_data:
  pg_standby2_data:

networks:
  pg-cluster:
    driver: bridge
```

`init-primary.sh`에서 replication 유저를 생성한다:

```bash
#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'repl_password';
    SELECT * FROM pg_create_physical_replication_slot('standby1_slot');
    SELECT * FROM pg_create_physical_replication_slot('standby2_slot');
EOSQL

# pg_hba.conf에 replication 허용 추가
echo "host replication replicator 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
```

---

### 2. Logical Replication (논리 복제)

Logical Replication은 PostgreSQL 10부터 지원되는 **행 단위 변경 이벤트** 기반 복제이다. Ch.12에서 배운 "Logical Log (Row-based)" 방식에 해당한다. Streaming Replication이 WAL 바이트를 그대로 전송하는 반면, Logical Replication은 INSERT/UPDATE/DELETE 이벤트를 논리적 형태로 전송한다.

#### 2.1 Pub/Sub 모델

```
┌──────────────┐                      ┌──────────────┐
│  Publisher   │   Logical WAL        │  Subscriber  │
│  (Primary)   │   Decoding           │  (Target)    │
│              │                      │              │
│ Publication  │ ──── 변경 이벤트 ──→  │ Subscription │
│ (테이블 선택) │                      │ (적용)       │
└──────────────┘                      └──────────────┘
```

Publication은 복제할 테이블을 정의하고, Subscription은 어떤 Publication을 구독할지 정의한다. 특정 테이블만 선택적으로 복제할 수 있다는 것이 물리 복제와의 핵심 차이이다.

#### 2.2 Streaming vs Logical 비교

| 특성 | Streaming Replication | Logical Replication |
|------|----------------------|---------------------|
| 복제 단위 | 전체 클러스터(물리 WAL) | 선택한 테이블(논리 이벤트) |
| 버전 호환 | 동일 메이저 버전 필요 | 다른 버전 간 가능 |
| 쓰기 가능 | Standby는 읽기 전용 | Subscriber에서 쓰기 가능 |
| 사용 사례 | HA, 읽기 분산 | 무중단 마이그레이션, 부분 복제, CDC |
| DDL 복제 | 자동 (물리 복사) | 불가 (수동 적용 필요) |
| 성능 영향 | 낮음 | Decoding 오버헤드 존재 |

#### 2.3 Logical Replication 설정 예시

Publisher(소스) 측:

```sql
-- wal_level = logical 필수 (postgresql.conf)
-- 또는 ALTER SYSTEM SET wal_level = logical;

-- Publication 생성
CREATE PUBLICATION my_pub FOR TABLE users, orders;

-- 또는 전체 테이블
CREATE PUBLICATION my_pub FOR ALL TABLES;
```

Subscriber(대상) 측:

```sql
-- 대상 테이블 미리 생성 필요 (스키마 복제 안 됨)
CREATE TABLE users (id int PRIMARY KEY, name text, email text);
CREATE TABLE orders (id int PRIMARY KEY, user_id int, total numeric);

-- Subscription 생성
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=publisher_host port=5432 dbname=mydb user=replicator password=repl_password'
  PUBLICATION my_pub;
```

---

### 3. Patroni + etcd: 자동 HA 클러스터

Streaming Replication만으로는 Failover를 수동으로 처리해야 한다. **Patroni**는 이를 자동화하는 HA 솔루션이다. Ch.12에서 배운 합의 알고리즘 기반 코디네이션 서비스(etcd)를 활용해 리더 선출과 자동 Failover를 구현한다.

#### 3.1 아키텍처

```
┌─────────────────────────────────────────────────┐
│                  etcd 클러스터                    │
│         (합의 기반 분산 키-값 저장소)              │
│   ┌────────┐  ┌────────┐  ┌────────┐           │
│   │ etcd-1 │──│ etcd-2 │──│ etcd-3 │           │
│   └────────┘  └────────┘  └────────┘           │
│        ↑           ↑           ↑                │
└────────┼───────────┼───────────┼────────────────┘
         │           │           │
   ┌─────┴─────┐ ┌──┴──────┐ ┌─┴────────┐
   │  Node 1   │ │ Node 2  │ │  Node 3  │
   │┌─────────┐│ │┌───────┐│ │┌────────┐│
   ││ Patroni ││ ││Patroni││ ││Patroni ││
   │├─────────┤│ │├───────┤│ │├────────┤│
   ││PostgreSQL││ ││PgSQL  ││ ││PgSQL   ││
   ││(Primary) ││ ││(Stby) ││ ││(Stby)  ││
   │└─────────┘│ │└───────┘│ │└────────┘│
   └───────────┘ └─────────┘ └──────────┘
```

**Patroni의 역할:**
- etcd에 리더 키(leader lock)를 생성하여 Primary를 결정
- Primary가 주기적으로 리더 키를 갱신(TTL 기반 리스)
- Primary 장애 시 리더 키가 만료되고, Standby 중 하나가 새 리더 키를 획득
- 새 Primary로 승격(promote) + 나머지 Standby를 새 Primary로 재설정

**etcd의 역할:**
- Raft 합의 알고리즘으로 리더 키의 일관성 보장
- Split Brain 방지: 과반수 etcd 노드가 동의해야 리더 키 생성 가능
- 클러스터 상태 저장: 각 노드의 역할, 타임라인, LSN 정보

#### 3.2 Failover 흐름

```
[T0] Primary 정상 운영, 30초마다 리더 키 갱신
         │
[T1] Primary 장애 발생 (프로세스 크래시 또는 네트워크 단절)
         │
[T2] 리더 키 TTL 만료 (기본 30초)
         │
[T3] Standby 노드들이 경쟁적으로 리더 키 획득 시도
     → etcd의 CAS(Compare-and-Set)로 하나만 성공
         │
[T4] 승리한 Standby가 pg_ctl promote 실행
     → Primary로 승격
         │
[T5] 나머지 Standby가 새 Primary를 팔로우하도록 재설정
     → pg_rewind 또는 pg_basebackup 사용
         │
[T6] 애플리케이션이 새 Primary에 연결
     → HAProxy/pgBouncer가 자동 라우팅 변경
```

#### 3.3 Docker Compose로 Patroni + etcd 구성

```yaml
# docker-compose-patroni.yml
version: '3.8'

services:
  etcd1:
    image: quay.io/coreos/etcd:v3.5.12
    container_name: etcd1
    environment:
      ETCD_NAME: etcd1
      ETCD_INITIAL_ADVERTISE_PEER_URLS: http://etcd1:2380
      ETCD_LISTEN_PEER_URLS: http://0.0.0.0:2380
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd1:2379
      ETCD_INITIAL_CLUSTER: etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
      ETCD_INITIAL_CLUSTER_STATE: new
      ETCD_INITIAL_CLUSTER_TOKEN: pg-cluster
    networks:
      - pg-cluster

  etcd2:
    image: quay.io/coreos/etcd:v3.5.12
    container_name: etcd2
    environment:
      ETCD_NAME: etcd2
      ETCD_INITIAL_ADVERTISE_PEER_URLS: http://etcd2:2380
      ETCD_LISTEN_PEER_URLS: http://0.0.0.0:2380
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd2:2379
      ETCD_INITIAL_CLUSTER: etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
      ETCD_INITIAL_CLUSTER_STATE: new
      ETCD_INITIAL_CLUSTER_TOKEN: pg-cluster
    networks:
      - pg-cluster

  etcd3:
    image: quay.io/coreos/etcd:v3.5.12
    container_name: etcd3
    environment:
      ETCD_NAME: etcd3
      ETCD_INITIAL_ADVERTISE_PEER_URLS: http://etcd3:2380
      ETCD_LISTEN_PEER_URLS: http://0.0.0.0:2380
      ETCD_LISTEN_CLIENT_URLS: http://0.0.0.0:2379
      ETCD_ADVERTISE_CLIENT_URLS: http://etcd3:2379
      ETCD_INITIAL_CLUSTER: etcd1=http://etcd1:2380,etcd2=http://etcd2:2380,etcd3=http://etcd3:2380
      ETCD_INITIAL_CLUSTER_STATE: new
      ETCD_INITIAL_CLUSTER_TOKEN: pg-cluster
    networks:
      - pg-cluster

  patroni1:
    image: patroni/patroni:latest
    container_name: patroni1
    environment:
      PATRONI_NAME: patroni1
      PATRONI_SCOPE: pg-cluster
      PATRONI_ETCD3_HOSTS: etcd1:2379,etcd2:2379,etcd3:2379
      PATRONI_RESTAPI_CONNECT_ADDRESS: patroni1:8008
      PATRONI_RESTAPI_LISTEN: 0.0.0.0:8008
      PATRONI_POSTGRESQL_CONNECT_ADDRESS: patroni1:5432
      PATRONI_POSTGRESQL_LISTEN: 0.0.0.0:5432
      PATRONI_POSTGRESQL_DATA_DIR: /var/lib/postgresql/data
      PATRONI_SUPERUSER_USERNAME: postgres
      PATRONI_SUPERUSER_PASSWORD: postgres
      PATRONI_REPLICATION_USERNAME: replicator
      PATRONI_REPLICATION_PASSWORD: repl_password
      PATRONI_POSTGRESQL_PARAMETERS: >-
        max_connections=100,
        max_wal_senders=5,
        wal_level=replica,
        hot_standby=on,
        synchronous_commit=on
    ports:
      - "5432:5432"
      - "8008:8008"
    volumes:
      - patroni1_data:/var/lib/postgresql/data
    depends_on:
      - etcd1
      - etcd2
      - etcd3
    networks:
      - pg-cluster

  patroni2:
    image: patroni/patroni:latest
    container_name: patroni2
    environment:
      PATRONI_NAME: patroni2
      PATRONI_SCOPE: pg-cluster
      PATRONI_ETCD3_HOSTS: etcd1:2379,etcd2:2379,etcd3:2379
      PATRONI_RESTAPI_CONNECT_ADDRESS: patroni2:8008
      PATRONI_RESTAPI_LISTEN: 0.0.0.0:8008
      PATRONI_POSTGRESQL_CONNECT_ADDRESS: patroni2:5432
      PATRONI_POSTGRESQL_LISTEN: 0.0.0.0:5432
      PATRONI_POSTGRESQL_DATA_DIR: /var/lib/postgresql/data
      PATRONI_SUPERUSER_USERNAME: postgres
      PATRONI_SUPERUSER_PASSWORD: postgres
      PATRONI_REPLICATION_USERNAME: replicator
      PATRONI_REPLICATION_PASSWORD: repl_password
    ports:
      - "5433:5432"
      - "8009:8008"
    volumes:
      - patroni2_data:/var/lib/postgresql/data
    depends_on:
      - etcd1
      - etcd2
      - etcd3
    networks:
      - pg-cluster

  patroni3:
    image: patroni/patroni:latest
    container_name: patroni3
    environment:
      PATRONI_NAME: patroni3
      PATRONI_SCOPE: pg-cluster
      PATRONI_ETCD3_HOSTS: etcd1:2379,etcd2:2379,etcd3:2379
      PATRONI_RESTAPI_CONNECT_ADDRESS: patroni3:8008
      PATRONI_RESTAPI_LISTEN: 0.0.0.0:8008
      PATRONI_POSTGRESQL_CONNECT_ADDRESS: patroni3:5432
      PATRONI_POSTGRESQL_LISTEN: 0.0.0.0:5432
      PATRONI_POSTGRESQL_DATA_DIR: /var/lib/postgresql/data
      PATRONI_SUPERUSER_USERNAME: postgres
      PATRONI_SUPERUSER_PASSWORD: postgres
      PATRONI_REPLICATION_USERNAME: replicator
      PATRONI_REPLICATION_PASSWORD: repl_password
    ports:
      - "5434:5432"
      - "8010:8008"
    volumes:
      - patroni3_data:/var/lib/postgresql/data
    depends_on:
      - etcd1
      - etcd2
      - etcd3
    networks:
      - pg-cluster

  haproxy:
    image: haproxy:2.9
    container_name: haproxy
    ports:
      - "5000:5000"  # Primary (읽기/쓰기)
      - "5001:5001"  # Standby (읽기 전용)
      - "7000:7000"  # HAProxy stats
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    depends_on:
      - patroni1
      - patroni2
      - patroni3
    networks:
      - pg-cluster

volumes:
  patroni1_data:
  patroni2_data:
  patroni3_data:

networks:
  pg-cluster:
    driver: bridge
```

HAProxy 설정(`haproxy.cfg`)은 Patroni REST API를 헬스체크에 활용한다:

```
global
    maxconn 100

defaults
    mode tcp
    timeout connect 10s
    timeout client  30s
    timeout server  30s

listen primary
    bind *:5000
    option httpchk GET /primary
    http-check expect status 200
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server patroni1 patroni1:5432 check port 8008
    server patroni2 patroni2:5432 check port 8008
    server patroni3 patroni3:5432 check port 8008

listen replicas
    bind *:5001
    option httpchk GET /replica
    http-check expect status 200
    balance roundrobin
    default-server inter 3s fall 3 rise 2 on-marked-down shutdown-sessions
    server patroni1 patroni1:5432 check port 8008
    server patroni2 patroni2:5432 check port 8008
    server patroni3 patroni3:5432 check port 8008

listen stats
    bind *:7000
    mode http
    stats enable
    stats uri /
```

---

### 4. Citus: 분산 PostgreSQL

Citus는 PostgreSQL 확장(extension)으로, Ch.12에서 배운 **해시 샤딩**을 PostgreSQL 위에 구현한다. 표준 PostgreSQL SQL을 그대로 사용하면서 데이터를 여러 노드에 분산 저장하고 병렬 쿼리를 실행한다.

#### 4.1 아키텍처

```
┌─────────────────────────────────────────────────┐
│                  Coordinator                     │
│          (쿼리 파싱, 계획, 라우팅)                │
│   ┌───────────────────────────────────────────┐ │
│   │  Distributed Tables 메타데이터             │ │
│   │  - 분산 컬럼(distribution column)          │ │
│   │  - 샤드 → 노드 매핑                        │ │
│   └───────────────────────────────────────────┘ │
└──────────┬──────────────┬──────────────┬────────┘
           │              │              │
    ┌──────▼──────┐ ┌────▼────────┐ ┌──▼──────────┐
    │  Worker 1   │ │  Worker 2   │ │  Worker 3   │
    │ ┌─────────┐ │ │ ┌─────────┐ │ │ ┌─────────┐ │
    │ │ Shard 1 │ │ │ │ Shard 2 │ │ │ │ Shard 3 │ │
    │ │ Shard 4 │ │ │ │ Shard 5 │ │ │ │ Shard 6 │ │
    │ └─────────┘ │ │ └─────────┘ │ │ └─────────┘ │
    └─────────────┘ └─────────────┘ └─────────────┘
```

Citus의 테이블 유형은 세 가지이다.

| 유형 | 설명 | 사용 사례 |
|------|------|----------|
| Distributed Table | 분산 컬럼 해시로 샤딩 | 대용량 테이블 (이벤트, 로그) |
| Reference Table | 모든 Worker에 전체 복제 | 소규모 참조 테이블 (국가, 카테고리) |
| Local Table | Coordinator에만 존재 | 메타데이터, 설정 |

```sql
-- Citus 활성화
CREATE EXTENSION citus;

-- Worker 노드 등록
SELECT citus_set_coordinator_host('coordinator', 5432);
SELECT * FROM citus_add_node('worker1', 5432);
SELECT * FROM citus_add_node('worker2', 5432);

-- 분산 테이블 생성
CREATE TABLE events (
    tenant_id int,
    event_id  bigserial,
    event_type text,
    payload   jsonb,
    created_at timestamptz DEFAULT now(),
    PRIMARY KEY (tenant_id, event_id)
);

SELECT create_distributed_table('events', 'tenant_id');

-- 참조 테이블 생성
CREATE TABLE event_types (
    id   int PRIMARY KEY,
    name text
);

SELECT create_reference_table('event_types');
```

`tenant_id`를 분산 컬럼으로 지정하면, 같은 테넌트의 데이터가 같은 샤드에 모인다. 이는 Ch.12에서 배운 멀티테넌시 샤딩 전략을 그대로 적용한 것이다.

#### 4.2 Docker Compose로 Citus 구성

```yaml
# docker-compose-citus.yml
version: '3.8'

services:
  coordinator:
    image: citusdata/citus:12.1
    container_name: citus-coordinator
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - citus_coordinator_data:/var/lib/postgresql/data
    networks:
      - citus-net

  worker1:
    image: citusdata/citus:12.1
    container_name: citus-worker1
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - citus_worker1_data:/var/lib/postgresql/data
    networks:
      - citus-net

  worker2:
    image: citusdata/citus:12.1
    container_name: citus-worker2
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - citus_worker2_data:/var/lib/postgresql/data
    networks:
      - citus-net

  manager:
    image: citusdata/membership-manager:0.3.0
    container_name: citus-manager
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - healthcheck-volume:/healthcheck
    depends_on:
      - coordinator
      - worker1
      - worker2
    networks:
      - citus-net

volumes:
  citus_coordinator_data:
  citus_worker1_data:
  citus_worker2_data:
  healthcheck-volume:

networks:
  citus-net:
    driver: bridge
```

---

### 5. pgpool-II: 커넥션 풀링과 로드밸런싱

pgpool-II는 PostgreSQL 클라이언트와 서버 사이에 위치하는 미들웨어이다. 커넥션 풀링, 읽기 쿼리 로드밸런싱, 자동 Failover 기능을 제공한다.

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ Client 1 │────→│              │────→│   Primary    │ (쓰기)
│ Client 2 │────→│   pgpool-II  │────→│   Standby 1  │ (읽기)
│ Client 3 │────→│              │────→│   Standby 2  │ (읽기)
└──────────┘     └──────────────┘     └──────────────┘
                  - 커넥션 풀링
                  - 쿼리 파싱 후 읽기/쓰기 분리
                  - SELECT → Standby 라운드로빈
                  - INSERT/UPDATE/DELETE → Primary
```

pgpool-II는 SQL을 파싱해서 SELECT 쿼리는 Standby로, 쓰기 쿼리는 Primary로 자동 라우팅한다. 다만 Patroni + HAProxy 조합이 더 단순하고 안정적이라는 이유로, 최근에는 Patroni를 선호하는 추세이다. pgpool-II는 커넥션 풀링 + 쿼리 캐싱이 필요한 경우에 적합하다.

---

### 6. Kubernetes에서의 PostgreSQL 클러스터링

Docker Compose는 개발/테스트에 적합하지만, 프로덕션에서는 Kubernetes Operator를 사용한다. Operator는 PostgreSQL 클러스터의 생명주기(생성, 스케일링, 백업, Failover)를 CRD(Custom Resource Definition)로 선언적으로 관리한다.

#### 6.1 CloudNativePG vs Zalando Postgres Operator

```
┌─────────────────────────────────────────────────────────┐
│                Kubernetes Cluster                        │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Operator (Controller)                  │ │
│  │   CRD 감시 → PostgreSQL 클러스터 생성/관리          │ │
│  └────────────────────┬───────────────────────────────┘ │
│                       │                                  │
│  ┌────────────────────▼───────────────────────────────┐ │
│  │                   StatefulSet                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │ │
│  │  │ Pod 0    │  │ Pod 1    │  │ Pod 2    │         │ │
│  │  │ Primary  │  │ Replica  │  │ Replica  │         │ │
│  │  │ PG + PVC │  │ PG + PVC │  │ PG + PVC │         │ │
│  │  └──────────┘  └──────────┘  └──────────┘         │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐                      │
│  │ Service(rw) │  │ Service(ro)  │                      │
│  │ → Primary   │  │ → Replicas   │                      │
│  └─────────────┘  └──────────────┘                      │
└──────────────────────────────────────────────────────────┘
```

| 비교 항목 | CloudNativePG | Zalando Postgres Operator |
|----------|---------------|--------------------------|
| 개발사 | EDB (EnterpriseDB) | Zalando SE |
| HA 메커니즘 | 자체 구현 (etcd 불필요) | Patroni 기반 (etcd/K8s API) |
| 백업 | Barman 통합 | WAL-G / S3 / GCS |
| 모니터링 | 내장 Prometheus 메트릭 | Prometheus 사이드카 |
| 풀링 | PgBouncer 내장 지원 | 외부 PgBouncer 배포 |
| 성숙도 | CNCF Sandbox 프로젝트 | 오래된 커뮤니티, 대규모 실전 검증 |
| CRD 예시 | `Cluster` | `postgresql` |

CloudNativePG CRD 예시:

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: my-cluster
spec:
  instances: 3
  storage:
    size: 10Gi
    storageClass: standard
  postgresql:
    parameters:
      max_connections: "100"
      shared_buffers: "256MB"
  backup:
    barmanObjectStore:
      destinationPath: s3://my-backup-bucket/
      s3Credentials:
        accessKeyId:
          name: aws-creds
          key: ACCESS_KEY_ID
        secretAccessKey:
          name: aws-creds
          key: SECRET_ACCESS_KEY
```

Zalando Operator CRD 예시:

```yaml
apiVersion: acid.zalan.do/v1
kind: postgresql
metadata:
  name: my-cluster
spec:
  teamId: "myteam"
  numberOfInstances: 3
  volume:
    size: 10Gi
  postgresql:
    version: "16"
    parameters:
      max_connections: "100"
      shared_buffers: "256MB"
  patroni:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
```

#### 6.2 Docker vs Kubernetes 배포 비교

| 항목 | Docker Compose | Kubernetes Operator |
|------|---------------|-------------------|
| Failover | Patroni가 직접 처리 | Operator + Patroni(또는 자체) |
| 스토리지 | Docker Volume | PersistentVolumeClaim |
| 서비스 디스커버리 | 컨테이너 이름/네트워크 | K8s Service (ClusterIP) |
| 스케일링 | compose 파일 수정 후 재배포 | `kubectl scale` 또는 CRD 수정 |
| 백업 | cron + pg_dump/pg_basebackup | Operator 내장 (S3/GCS 연동) |
| 모니터링 | 별도 Prometheus 컨테이너 | kube-prometheus-stack 통합 |
| 롤링 업데이트 | 수동 | Operator 자동 관리 |
| 적합 환경 | 개발, 테스트, PoC | 스테이징, 프로덕션 |

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| Streaming Replication | WAL 기반 물리 복제 - HA와 읽기 분산의 기본이다 |
| Logical Replication | 행 단위 논리 복제 - 선택적 복제, 무중단 마이그레이션에 사용한다 |
| Patroni + etcd | etcd의 합의 알고리즘으로 자동 Failover를 구현하는 HA 솔루션이다 |
| Citus | PostgreSQL 확장으로 해시 샤딩 기반 수평 확장을 제공한다 |
| pgpool-II | SQL 파싱 기반 읽기/쓰기 분리와 커넥션 풀링을 담당한다 |
| CloudNativePG | CNCF Sandbox의 K8s PostgreSQL Operator - etcd 불필요하다 |
| Zalando Operator | Patroni 기반의 성숙한 K8s PostgreSQL Operator이다 |
| HAProxy + Patroni | 헬스체크 API로 Primary/Replica를 자동 라우팅한다 |
