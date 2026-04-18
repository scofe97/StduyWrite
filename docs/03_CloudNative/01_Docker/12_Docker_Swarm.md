# Chapter 12: Docker Swarm

## 📌 핵심 요약

> **Docker Swarm**은 여러 Docker 노드를 **보안 클러스터**로 그룹화하고, **지능적인 애플리케이션 오케스트레이션**을 제공하는 기술이다. Kubernetes보다 학습 곡선이 낮아 소규모 비즈니스나 간단한 요구사항에 적합하다. Compose 파일을 사용한 **선언적 앱 관리**가 핵심이다.

---

## 🎯 학습 목표

- [ ] Docker Swarm의 개념과 Kubernetes와의 차이 이해
- [ ] 멀티 노드 Swarm 클러스터 구축
- [ ] Manager와 Worker 노드 역할 파악
- [ ] `docker stack deploy`로 앱 배포 및 관리
- [ ] 선언적 vs 명령적 앱 관리 방식 이해

---

## 📖 본문 정리

### 1. Docker Swarm이란?

#### 💬 비유로 이해하기
> Swarm은 **오케스트라**와 같다. Manager는 **지휘자**로서 전체 연주를 조율하고, Worker는 **연주자**로서 실제 음악(앱)을 연주한다. 지휘자가 여러 명 있으면(HA) 한 명이 아파도 연주가 계속된다.

#### Swarm의 두 가지 측면

| 측면 | 설명 | 표기 |
|------|------|------|
| **보안 클러스터** | Docker 노드들의 그룹 | swarm (소문자) |
| **오케스트레이터** | 앱 배포/관리 지능 | Swarm (대문자) |

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Swarm 아키텍처                         │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │                    Manager Nodes                             │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
  │  │   Manager   │  │   Manager   │  │   Manager   │          │
  │  │   (Leader)  │  │ (Reachable) │  │ (Reachable) │          │
  │  │             │  │             │  │             │          │
  │  │ • Control   │  │ • Backup    │  │ • Backup    │          │
  │  │   Plane     │  │ • Ready to  │  │ • Ready to  │          │
  │  │ • Raft      │  │   takeover  │  │   takeover  │          │
  │  │   Consensus │  │             │  │             │          │
  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
  │         └────────────────┼────────────────┘                  │
  │                          │                                   │
  │              Control Plane (포트 2377)                        │
  └──────────────────────────┼───────────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                     Worker Nodes                             │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
  │  │   Worker    │  │   Worker    │  │   Worker    │          │
  │  │             │  │             │  │             │          │
  │  │ • User Apps │  │ • User Apps │  │ • User Apps │          │
  │  │ • Replicas  │  │ • Replicas  │  │ • Replicas  │          │
  │  └─────────────┘  └─────────────┘  └─────────────┘          │
  └─────────────────────────────────────────────────────────────┘
```

### 2. Swarm vs Kubernetes

| 특성 | Docker Swarm | Kubernetes |
|------|--------------|------------|
| **학습 곡선** | 낮음 | 높음 |
| **설정 복잡도** | 간단 | 복잡 |
| **생태계** | 작음 | 대규모, 활발 |
| **확장성** | 중소 규모 | 대규모 |
| **적합 대상** | 소규모 비즈니스 | 엔터프라이즈 |
| **시장 점유율** | 감소 중 | 업계 표준 |

**Swarm 선택 시나리오**:
- 소규모 팀/프로젝트
- Kubernetes 오버헤드가 부담스러운 경우
- Docker 도구에 이미 익숙한 경우

### 3. Swarm 클러스터 구축

#### 노드 역할

| 역할 | 기능 | MANAGER STATUS |
|------|------|----------------|
| **Leader** | 클러스터 제어, 오케스트레이션 | Leader |
| **Reachable** | Leader 백업, 장애 시 승계 | Reachable |
| **Worker** | 사용자 앱 실행 | (비어있음) |

#### 클러스터 구축 단계

```bash
# 1단계: 첫 번째 Manager 초기화
$ docker swarm init
Swarm initialized: current node (b8slc7l29tg...) is now a manager.
To add a worker to this swarm, run the following command:
  docker swarm join --token SWMTKN-1-2hl6...-...3lqg 172.31.40.192:2377

# 2단계: Worker 추가 (선택)
# Worker 노드에서 실행
$ docker swarm join --token SWMTKN-1-2hl6...-...3lqg 172.31.40.192:2377
This node joined a swarm as a worker.

# 3단계: 추가 Manager 토큰 획득
$ docker swarm join-token manager
To add a manager to this swarm, run the following command:
  docker swarm join --token SWMTKN-1-2f4s47lja... 172.31.40.192:2377

# 4단계: 추가 Manager 조인 (다른 노드에서)
$ docker swarm join --token SWMTKN-1-2f4s47lja... 172.31.40.192:2377

# 클러스터 확인
$ docker node ls
ID            HOSTNAME   STATUS   AVAILABILITY   MANAGER STATUS   ENGINE
b8slc7l29tg*  node1      Ready    Active         Leader           27.3.1
y43jr1d754p   node2      Ready    Active         Reachable        27.3.1
k1npnfxr7yk   node3      Ready    Active         Reachable        27.3.1
w3e321uxty2   node4      Ready    Active                          27.3.1
kbodotf68tz   node5      Ready    Active                          27.3.1
```

#### 프로덕션 권장 구성
- **Manager 3개**: 가용성 영역(AZ) 분산 배치
- **Worker**: 애플리케이션 요구사항에 맞게 추가
- **포트 2377**: 네트워크에서 열려 있어야 함

```
┌─────────────────────────────────────────────────────────────────┐
│                프로덕션 Swarm 구성 예시                          │
└─────────────────────────────────────────────────────────────────┘

     AZ-1              AZ-2              AZ-3
  ┌─────────┐       ┌─────────┐       ┌─────────┐
  │ Manager │       │ Manager │       │ Manager │
  │ (Leader)│◄─────►│(Reachable)◄────►│(Reachable)
  └────┬────┘       └────┬────┘       └────┬────┘
       │                 │                 │
  ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
  │ Worker  │       │ Worker  │       │ Worker  │
  │ Worker  │       │ Worker  │       │ Worker  │
  └─────────┘       └─────────┘       └─────────┘

  • 1개 Manager 장애 시에도 클러스터 운영 지속
  • 앱 가용성은 별도 관리 필요 (replicas)
```

### 4. Swarm 앱 배포

#### 샘플 앱 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    Sample Swarm App                              │
└─────────────────────────────────────────────────────────────────┘

                        Port 5001 (Published)
                              │
                              ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                       web-fe Service                          │
  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
  │  │Replica 1│  │Replica 2│  │Replica 3│  │Replica 4│          │
  │  │  :8080  │  │  :8080  │  │  :8080  │  │  :8080  │          │
  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘          │
  │       └────────────┼────────────┼────────────┘               │
  │                    │            │                             │
  └────────────────────┼────────────┼─────────────────────────────┘
                       │            │
                       ▼            ▼
  ┌───────────────────────────────────────────────────────────────┐
  │              counter-net (Encrypted Overlay)                  │
  └───────────────────────────────────────────────────────────────┘
                              │
                              ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                      redis Service                            │
  │                    ┌─────────────┐                            │
  │                    │  Replica 1  │                            │
  │                    │             │                            │
  │                    └──────┬──────┘                            │
  │                           │                                   │
  │                    ┌──────┴──────┐                            │
  │                    │ counter-vol │                            │
  │                    │   /data     │                            │
  │                    └─────────────┘                            │
  └───────────────────────────────────────────────────────────────┘
```

#### Swarm용 Compose 파일

```yaml
networks:
  counter-net:
    driver: overlay            # Swarm 전용 오버레이 네트워크
    driver_opts:
      encrypted: 'yes'         # 트래픽 암호화 (~10% 성능 저하)

volumes:
  counter-vol:

services:
  web-fe:
    image: nigelpoulton/ddd-book:swarm-app
    command: python app.py
    deploy:                    # Swarm 배포 설정 (핵심!)
      replicas: 4              # 복제본 수
      update_config:           # 업데이트 정책
        parallelism: 2         # 한 번에 2개씩 업데이트
        delay: 10s             # 업데이트 간 대기 시간
        failure_action: rollback  # 실패 시 롤백
      restart_policy:          # 재시작 정책
        condition: on-failure  # 실패 시에만 재시작
        delay: 5s              # 재시작 대기 시간
        max_attempts: 3        # 최대 재시작 시도
        window: 120s           # 시도 기간
    networks:
      - counter-net
    ports:
      - "5001:8080"

  redis:
    image: "redis:alpine"
    networks:
      - counter-net
    volumes:
      - type: volume
        source: counter-vol
        target: /data
```

#### deploy 섹션 상세

| 설정 | 설명 | 예시 값 |
|------|------|---------|
| `replicas` | 서비스 복제본 수 | `4` |
| `update_config.parallelism` | 동시 업데이트 수 | `2` |
| `update_config.delay` | 업데이트 간 대기 | `10s` |
| `update_config.failure_action` | 실패 시 동작 | `rollback` |
| `restart_policy.condition` | 재시작 조건 | `on-failure` |
| `restart_policy.max_attempts` | 최대 재시작 시도 | `3` |
| `restart_policy.window` | 시도 기간 | `120s` |

#### 앱 배포 및 확인

```bash
# 앱 배포
$ docker stack deploy -c compose.yaml ddd
Creating network ddd_counter-net
Creating volume ddd_counter-vol
Creating service ddd_web-fe
Creating service ddd_redis

# 앱 목록 확인
$ docker stack ls
NAME   SERVICES   ORCHESTRATOR
ddd    2          Swarm

# 복제본 상태 확인
$ docker stack ps ddd
NAME           IMAGE                             NODE   DESIRED   CURRENT
ddd_redis.1    redis:alpine                      wrk2   Running   Running
ddd_web-fe.1   nigelpoulton/ddd-book:swarm-app   wrk1   Running   Running
ddd_web-fe.2   nigelpoulton/ddd-book:swarm-app   mgr1   Running   Running
ddd_web-fe.3   nigelpoulton/ddd-book:swarm-app   mgr2   Running   Running
ddd_web-fe.4   nigelpoulton/ddd-book:swarm-app   mgr3   Running   Running

# 서비스 상태 확인
$ docker stack services ddd
NAME        MODE   REPLICAS   IMAGE                             PORTS
ddd_redis   repl   1/1        redis:alpine
ddd_web-fe  repl   4/4        nigelpoulton/ddd-book:swarm-app   *:5001->8080
```

### 5. 앱 관리: 선언적 vs 명령적

#### 두 가지 관리 방식

| 방식 | 설명 | 권장 여부 |
|------|------|-----------|
| **명령적** | CLI 명령어로 직접 변경 | ❌ 비권장 |
| **선언적** | Compose 파일 수정 후 재배포 | ✅ 권장 |

```
┌─────────────────────────────────────────────────────────────────┐
│              명령적 vs 선언적 관리 비교                          │
└─────────────────────────────────────────────────────────────────┘

  명령적 (문제 발생 가능)                선언적 (권장)
  ─────────────────────                ─────────────────────

  $ docker service scale             1. compose.yaml 수정
    ddd_web-fe=10                       replicas: 4 → 10

         │                            2. 재배포
         ▼                               $ docker stack deploy
  ┌─────────────────┐                      -c compose.yaml ddd
  │ 관찰 상태: 10개  │
  │ 정의 상태: 4개   │ ← 불일치!     ┌─────────────────┐
  └────────┬────────┘               │ 관찰 상태: 10개  │
           │                        │ 정의 상태: 10개  │ ← 일치!
           ▼                        └─────────────────┘
  다음 배포 시 4개로 롤백됨!
```

**명령적 방식의 위험성 예시**:
1. Compose 파일: `replicas: 1`
2. CLI로 스케일 아웃: `docker service scale reporting=10`
3. 다른 변경으로 재배포: `docker stack deploy`
4. **문제**: Swarm이 Compose 파일 기준으로 1개로 롤백!

### 6. 롤링 업데이트 예시

#### 이미지 업데이트 + 스케일 아웃

```yaml
# compose.yaml 수정
services:
  web-fe:
    image: nigelpoulton/ddd-book:swarm-appv2  # 이미지 변경
    deploy:
      replicas: 10                             # 4 → 10으로 증가
```

```bash
# 재배포
$ docker stack deploy -c compose.yaml ddd
Updating service ddd_web-fe
Updating service ddd_redis

# 롤아웃 진행 상황 확인
$ docker stack ps ddd
NAME             IMAGE                               DESIRED   CURRENT STATE
ddd_web-fe.1     nigelpoulton/ddd-book:swarm-app     Running   Running 8 mins
ddd_web-fe.2     nigelpoulton/ddd-book:swarm-appv2   Running   Running 13 secs
\_ddd_web-fe.2   nigelpoulton/ddd-book:swarm-app     Shutdown  Shutdown 26 secs
ddd_web-fe.3     nigelpoulton/ddd-book:swarm-app     Running   Running 8 mins
...
```

**롤아웃 동작**:
1. 새 복제본 6개 즉시 추가
2. 기존 4개는 `update_config` 설정에 따라 업데이트
   - 2개씩 업데이트 (`parallelism: 2`)
   - 10초 대기 후 다음 2개 (`delay: 10s`)

### 7. 정리

```bash
# 앱 삭제 (확인 없이 즉시 삭제)
$ docker stack rm ddd
Removing service ddd_redis
Removing service ddd_web-fe
Removing network ddd_counter-net
# 주의: 볼륨은 삭제되지 않음

# 볼륨 수동 삭제 (redis 노드에서)
$ docker volume rm ddd_counter-vol

# Swarm 탈퇴 (모든 노드에서)
$ docker swarm leave
# Leader는 --force 필요
$ docker swarm leave --force
```

---

## 🔍 심화 학습

### Desired State와 Reconciliation
- **Desired State**: Compose 파일에 정의된 원하는 상태
- **Observed State**: 클러스터의 현재 실제 상태
- **Reconciliation**: 관찰 상태를 원하는 상태로 맞추는 과정

### 추가 학습 주제
- Swarm Secrets (민감 정보 관리)
- Swarm Configs (설정 파일 관리)
- Global 서비스 vs Replicated 서비스
- Placement 제약 조건

---

## 💡 실무 적용 포인트

### 면접 대비 질문

**Q1: Docker Swarm과 Kubernetes의 주요 차이점은?**
> **A**: Swarm은 Docker에 내장되어 학습 곡선이 낮고 설정이 간단하지만, Kubernetes는 대규모 생태계와 확장성을 제공한다. Swarm은 소규모 환경에, Kubernetes는 엔터프라이즈 환경에 적합하다.

**Q2: Swarm 앱을 선언적으로 관리해야 하는 이유는?**
> **A**: 명령적 변경(CLI)은 Compose 파일의 정의와 클러스터 상태 간 불일치를 야기한다. 다음 배포 시 Swarm이 Compose 파일 기준으로 롤백하여 예상치 못한 변경이 발생할 수 있다. Compose 파일을 수정하고 재배포하는 선언적 방식이 일관성을 보장한다.

**Q3: Swarm에서 Manager 3개를 권장하는 이유는?**
> **A**: Raft 합의 알고리즘으로 고가용성을 제공하기 위해서다. 3개 Manager 중 1개가 실패해도 과반수(2개)가 남아 클러스터 운영이 계속된다. 단, 이는 클러스터 가용성이며, 앱 가용성은 replicas로 별도 관리해야 한다.

**Q4: `update_config`의 `parallelism`과 `delay` 설정의 역할은?**
> **A**: `parallelism`은 한 번에 업데이트할 복제본 수, `delay`는 업데이트 간 대기 시간이다. 예를 들어 `parallelism: 2`, `delay: 10s`면 2개씩 업데이트하고 10초 대기 후 다음 2개를 업데이트한다. 이를 통해 무중단 롤링 업데이트가 가능하다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] Docker Swarm의 두 가지 측면 (클러스터 + 오케스트레이터)
- [ ] Manager와 Worker 노드 역할 차이
- [ ] Leader vs Reachable Manager 상태 구분
- [ ] Desired State vs Observed State 개념

### 클러스터 구축
- [ ] `docker swarm init`: 첫 Manager 초기화
- [ ] `docker swarm join`: Worker/Manager 추가
- [ ] `docker swarm join-token`: 토큰 확인
- [ ] `docker node ls`: 클러스터 상태 확인
- [ ] 프로덕션용 3 Manager 구성 이해

### 앱 배포 및 관리
- [ ] `docker stack deploy -c compose.yaml <name>`: 앱 배포
- [ ] `docker stack ls`: 앱 목록 확인
- [ ] `docker stack ps <name>`: 복제본 상태 확인
- [ ] `docker stack services <name>`: 서비스 상태 확인
- [ ] `docker stack rm <name>`: 앱 삭제

### Compose 파일 (Swarm)
- [ ] `deploy.replicas`: 복제본 수 설정
- [ ] `deploy.update_config`: 업데이트 정책
- [ ] `deploy.restart_policy`: 재시작 정책
- [ ] Overlay 네트워크와 암호화 옵션

### 운영 원칙
- [ ] 선언적 관리 (Compose 파일 수정 후 재배포)
- [ ] 명령적 변경의 위험성 인식
- [ ] Compose 파일 버전 관리 (Git)

---

## 🔗 참고 자료

- [Docker Swarm 공식 문서](https://docs.docker.com/engine/swarm/)
- [Swarm 튜토리얼](https://docs.docker.com/engine/swarm/swarm-tutorial/)
- [Play with Docker](https://labs.play-with-docker.com/)
- *Quick Start Kubernetes* - Nigel Poulton
- *The Kubernetes Book* - Nigel Poulton
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 12
