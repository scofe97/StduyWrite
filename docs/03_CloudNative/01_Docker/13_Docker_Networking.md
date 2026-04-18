# Chapter 13: Docker Networking

## 📌 핵심 요약

> Docker 네트워킹은 **Container Network Model(CNM)** 설계를 기반으로 **libnetwork**가 구현하고, **드라이버**가 실제 네트워크 토폴로지를 생성한다. 기본 **bridge** 네트워크부터 기존 물리 네트워크에 연결하는 **MACVLAN**까지, Docker는 다양한 네트워킹 요구사항을 해결한다. **서비스 디스커버리**와 **DNS 기반 이름 해석**이 내장되어 있다.

---

## 🎯 학습 목표

- [ ] Container Network Model(CNM)의 구성 요소 이해
- [ ] libnetwork와 드라이버의 역할 파악
- [ ] 단일 호스트 bridge 네트워크 생성 및 활용
- [ ] 포트 매핑을 통한 외부 접근 설정
- [ ] MACVLAN을 통한 기존 네트워크/VLAN 연결
- [ ] 서비스 디스커버리와 DNS 해석 원리 이해

---

## 📖 본문 정리

### 1. Docker 네트워킹 개요

#### 💬 비유로 이해하기
> Docker 네트워크는 **아파트 단지의 내부 도로망**과 같다. 각 컨테이너(집)는 자체 주소(IP)를 가지며, 같은 네트워크(단지)에 있는 컨테이너끼리 이름으로 찾아갈 수 있다. 외부와 통신하려면 정문(포트 매핑)을 통해야 한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                   Docker 네트워킹 아키텍처                        │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │                        Applications                          │
  │  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
  │  │Container A│  │Container B│  │Container C│               │
  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘               │
  │        │              │              │                       │
  │        │   Endpoints (가상 NIC)       │                       │
  │        ▼              ▼              ▼                       │
  └────────┼──────────────┼──────────────┼───────────────────────┘
           │              │              │
  ┌────────┴──────────────┴──────────────┴───────────────────────┐
  │                     Docker Networks                          │
  │  ┌─────────────────────┐  ┌─────────────────────┐           │
  │  │    Network A        │  │    Network B        │           │
  │  │   (bridge/overlay)  │  │   (macvlan 등)      │           │
  │  └──────────┬──────────┘  └──────────┬──────────┘           │
  └─────────────┼─────────────────────────┼──────────────────────┘
                │                         │
  ┌─────────────┴─────────────────────────┴──────────────────────┐
  │                       libnetwork                              │
  │         (CNM 구현체, Control Plane, Service Discovery)        │
  └───────────────────────────────┬──────────────────────────────┘
                                  │
  ┌───────────────────────────────┴──────────────────────────────┐
  │                         Drivers                               │
  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐             │
  │  │ bridge │  │overlay │  │macvlan │  │  host  │             │
  │  └────────┘  └────────┘  └────────┘  └────────┘             │
  └──────────────────────────────────────────────────────────────┘
```

### 2. Container Network Model (CNM)

#### 세 가지 핵심 구성 요소

| 구성 요소 | 설명 | 비유 |
|-----------|------|------|
| **Sandbox** | 컨테이너의 격리된 네트워크 스택 (인터페이스, 라우팅 테이블, DNS 등) | 집의 내부 배선 |
| **Endpoint** | 가상 네트워크 인터페이스, Sandbox를 Network에 연결 | 집의 현관문 |
| **Network** | 가상 스위치 (802.1d 브리지), Endpoint들을 그룹화/격리 | 아파트 단지 내부 도로 |

```
┌─────────────────────────────────────────────────────────────────┐
│                    CNM 구성 요소 관계                            │
└─────────────────────────────────────────────────────────────────┘

  Container A                           Container B
  ┌─────────────────────┐               ┌─────────────────────┐
  │      Sandbox        │               │      Sandbox        │
  │  ┌───────────────┐  │               │  ┌───────────────┐  │
  │  │ • eth0        │  │               │  │ • eth0   eth1 │  │
  │  │ • 라우팅 테이블│  │               │  │ • 라우팅 테이블│  │
  │  │ • DNS 설정    │  │               │  │ • DNS 설정    │  │
  │  └───────┬───────┘  │               │  └───┬───────┬───┘  │
  │          │          │               │      │       │      │
  │    ┌─────┴─────┐    │               │ ┌────┴──┐ ┌──┴────┐ │
  │    │ Endpoint  │    │               │ │Endpt 1│ │Endpt 2│ │
  │    └─────┬─────┘    │               │ └───┬───┘ └───┬───┘ │
  └──────────┼──────────┘               └─────┼─────────┼─────┘
             │                                │         │
             ▼                                ▼         ▼
  ┌──────────────────────────────────────────┐   ┌───────────┐
  │              Network A                    │   │ Network B │
  │         (컨테이너 A, B 통신 가능)          │   │           │
  └──────────────────────────────────────────┘   └───────────┘

  • Container A: 1개 Endpoint → Network A만 연결
  • Container B: 2개 Endpoint → Network A, B 둘 다 연결
  • Endpoint는 1개 Network에만 연결 가능
```

### 3. libnetwork와 드라이버

#### 역할 분리

| 구성 요소 | 역할 | 담당 영역 |
|-----------|------|-----------|
| **libnetwork** | CNM 구현체 | Control Plane (관리 API, 서비스 디스커버리, 로드밸런싱) |
| **Drivers** | 네트워크 토폴로지 구현 | Data Plane (네트워크 생성, 격리, 연결) |

#### 기본 제공 드라이버

| 드라이버 | 용도 | 특징 |
|----------|------|------|
| `bridge` | 단일 호스트 로컬 네트워크 | 기본 드라이버, 개발/테스트용 |
| `overlay` | 멀티 호스트 컨테이너 네트워크 | Swarm용, VXLAN 기반 |
| `macvlan` | 기존 물리 네트워크 연결 | 고유 MAC/IP, 프로미스큐어스 모드 필요 |
| `host` | 호스트 네트워크 스택 공유 | 격리 없음, 최고 성능 |
| `none` | 네트워크 비활성화 | 완전 격리 |

### 4. 단일 호스트 Bridge 네트워크

#### 기본 bridge 네트워크

```bash
# 기본 네트워크 확인
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
c7464dce29ce   bridge    bridge    local    ← 기본 네트워크
c65ab18d0580   host      host      local
42a783df0fbe   none      null      local

# bridge 네트워크 상세 정보
$ docker network inspect bridge
{
  "Name": "bridge",
  "Driver": "bridge",
  "IPAM": {
    "Config": [{
      "Subnet": "172.17.0.0/16",
      "Gateway": "172.17.0.1"
    }]
  }
}
```

#### Docker bridge와 Linux bridge 매핑

```
┌─────────────────────────────────────────────────────────────────┐
│              Docker Network ↔ Linux Bridge 매핑                  │
└─────────────────────────────────────────────────────────────────┘

  Docker Layer                    Linux Kernel Layer
  ─────────────                   ─────────────────

  ┌─────────────────┐             ┌─────────────────┐
  │ Docker Network  │             │   Linux Bridge  │
  │    "bridge"     │────────────►│    "docker0"    │
  └─────────────────┘             └─────────────────┘

  ┌─────────────────┐             ┌─────────────────┐
  │ Docker Network  │             │   Linux Bridge  │
  │   "localnet"    │────────────►│"br-f918f1bb0602"│
  └─────────────────┘             └─────────────────┘

# 확인 명령어
$ docker network inspect bridge | grep bridge.name
"com.docker.network.bridge.name": "docker0"

$ brctl show
bridge name        bridge id             interfaces
docker0            8000.0242aff9eb4f     veth833aaf9
br-f918f1bb0602    8000.0242372a886b     veth1234567
```

#### 커스텀 bridge 네트워크 생성

```bash
# 새 bridge 네트워크 생성
$ docker network create -d bridge localnet
f918f1bb0602373bf949615d99cb2bbbef14ede935fbb2ff8e83c74f10e4b986

# 컨테이너를 네트워크에 연결
$ docker run -d --name c1 --network localnet alpine sleep 1d

# 네트워크에 연결된 컨테이너 확인
$ docker network inspect localnet --format '{{json .Containers}}' | jq
{
  "09c5f4926c87...": {
    "Name": "c1",
    "IPv4Address": "172.21.0.2/16"
  }
}
```

#### DNS 기반 이름 해석 테스트

```bash
# 같은 네트워크에 c2 컨테이너 생성
$ docker run -it --name c2 --network localnet alpine sh

# c1 컨테이너를 이름으로 ping
# ping c1
PING c1 (172.21.0.2): 56 data bytes
64 bytes from 172.21.0.2: seq=0 ttl=64 time=1.564 ms
```

**중요**: 기본 `bridge` 네트워크는 DNS 해석을 지원하지 않음. 커스텀 네트워크만 지원!

### 5. 포트 매핑을 통한 외부 접근

```
┌─────────────────────────────────────────────────────────────────┐
│                    포트 매핑 동작 원리                           │
└─────────────────────────────────────────────────────────────────┘

  External Client                    Docker Host
       │                                  │
       │ :5005                            │
       ▼                                  ▼
  ┌─────────┐                     ┌─────────────────┐
  │ Request │───────────────────►│ Host IP:5005    │
  └─────────┘                     └────────┬────────┘
                                           │ 포트 매핑
                                           │ (5005 → 80)
                                           ▼
                                  ┌─────────────────┐
                                  │  web Container  │
                                  │     :80         │
                                  │    (NGINX)      │
                                  └─────────────────┘
```

#### 포트 매핑 명령어

```bash
# NGINX 컨테이너를 5005 포트에 매핑
$ docker run -d --name web \
  --network localnet \
  --publish 5005:80 \
  nginx

# 포트 매핑 확인
$ docker port web
80/tcp -> 0.0.0.0:5005
80/tcp -> [::]:5005

# 외부에서 접근 테스트
$ curl localhost:5005
<!DOCTYPE html>
<html>
<head><title>Welcome to nginx!</title>
...
```

**포트 매핑의 한계**:
- 호스트에서 해당 포트 독점 사용
- 확장성 제한 (포트 충돌)
- 로컬 개발/테스트에만 적합

### 6. MACVLAN: 기존 네트워크/VLAN 연결

#### MACVLAN 개념

```
┌─────────────────────────────────────────────────────────────────┐
│              MACVLAN: 컨테이너를 물리 네트워크에 직접 연결         │
└─────────────────────────────────────────────────────────────────┘

  Physical Network (VLAN 100: 10.0.0.0/24)
  ─────────────────────────────────────────────────────────────
       │              │              │              │
       │              │              │              │
  ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
  │Physical │    │Physical │    │ Docker  │    │Container│
  │Server   │    │Server   │    │  Host   │    │(macvlan)│
  │10.0.0.10│    │10.0.0.11│    │10.0.0.50│    │10.0.0.2 │
  └─────────┘    └─────────┘    └─────────┘    └─────────┘

  • 컨테이너가 고유 MAC/IP 주소를 가짐
  • 외부 네트워크에서 물리 서버처럼 보임
  • 포트 매핑 불필요
```

#### MACVLAN 네트워크 생성

```bash
# MACVLAN 네트워크 생성 (VLAN 100 연결)
$ docker network create -d macvlan \
  --subnet=10.0.0.0/24 \
  --ip-range=10.0.0.0/25 \      # Docker가 할당할 IP 범위
  --gateway=10.0.0.1 \
  -o parent=eth0.100 \          # 부모 인터페이스 (VLAN 태깅)
  macvlan100

# MACVLAN 네트워크에 컨테이너 연결
$ docker run -d --name mactainer1 \
  --network macvlan100 \
  alpine sleep 1d

# 네트워크 정보 확인
$ docker network inspect macvlan100
{
  "Name": "macvlan100",
  "Driver": "macvlan",
  "Options": {
    "parent": "eth0.100"
  }
}
```

**MACVLAN 주의사항**:
- 호스트 NIC **프로미스큐어스 모드** 필요
- 대부분의 퍼블릭 클라우드에서 **지원하지 않음**
- IP 범위를 Docker 전용으로 예약해야 함

### 7. 서비스 디스커버리

#### DNS 기반 이름 해석 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│              Docker 서비스 디스커버리 흐름                        │
└─────────────────────────────────────────────────────────────────┘

  Container c1                              Container c2
  ┌─────────────────┐                       ┌─────────────────┐
  │  ping c2        │                       │  IP: 172.21.0.3 │
  │       │         │                       │                 │
  │  ① Local DNS    │                       │                 │
  │    Resolver     │                       │                 │
  │    (캐시 확인)   │                       │                 │
  │       │         │                       │                 │
  │       ▼         │                       │                 │
  │  ② 캐시 미스    │                       │                 │
  └───────┼─────────┘                       └─────────────────┘
          │                                          ▲
          │ ③ 재귀 쿼리                              │
          ▼                                          │
  ┌───────────────────────────────────────┐         │
  │        Docker Embedded DNS Server      │         │
  │  ┌───────────────────────────────────┐│         │
  │  │ Name-to-IP Mappings:              ││         │
  │  │   c1 → 172.21.0.2                 ││         │
  │  │   c2 → 172.21.0.3                 ││         │
  │  └───────────────────────────────────┘│         │
  └───────────────────┬───────────────────┘         │
                      │                              │
                      │ ④ IP 반환: 172.21.0.3       │
                      ▼                              │
               Container c1                          │
                      │                              │
                      │ ⑤ ICMP Echo Request         │
                      └──────────────────────────────┘
```

#### 서비스 디스커버리 동작 조건
- `--name` 또는 `--net-alias` 플래그로 컨테이너 생성
- **같은 네트워크**에 있어야 함 (네트워크 스코프)

#### 커스텀 DNS 설정

```bash
# 외부 DNS 서버와 검색 도메인 설정
$ docker run -it --name custom-dns \
  --dns=8.8.8.8 \                    # Google DNS
  --dns-search=example.com \          # 검색 도메인
  alpine sh

# /etc/resolv.conf 확인
# cat /etc/resolv.conf
nameserver 8.8.8.8
search example.com
```

### 8. Ingress 로드밸런싱 (Swarm)

#### 두 가지 퍼블리싱 모드

| 모드 | 접근 가능 노드 | 설정 방법 |
|------|----------------|-----------|
| **Ingress** (기본) | 모든 Swarm 노드 | `-p 5005:80` |
| **Host** | 복제본이 실행 중인 노드만 | `--publish mode=host,...` |

```
┌─────────────────────────────────────────────────────────────────┐
│              Swarm Ingress 모드 vs Host 모드                     │
└─────────────────────────────────────────────────────────────────┘

  Ingress Mode (기본)                    Host Mode
  ──────────────────                     ─────────

       Client                                 Client
          │                                      │
    ┌─────┴─────┐                         ┌─────┴─────┐
    ▼     ▼     ▼                         ▼           ✗
  ┌───┐ ┌───┐ ┌───┐                     ┌───┐       ┌───┐
  │ A │ │ B │ │ C │  ← 어느 노드든 OK    │ B │       │ C │
  └───┘ └───┘ └───┘                     └─┬─┘       └───┘
    │     │     │                          │
    └─────┼─────┘                          │
          ▼                                ▼
    ┌───────────┐                    ┌───────────┐
    │  Replica  │ (어느 노드에든)     │  Replica  │ (B 노드에만)
    └───────────┘                    └───────────┘
```

#### Ingress 모드 트래픽 흐름

```bash
# Swarm 서비스 생성 (ingress 모드)
$ docker service create -d --name svc1 \
  --publish published=5005,target=80 \
  --replicas 3 \
  nginx
```

```
┌─────────────────────────────────────────────────────────────────┐
│              Ingress 로드밸런싱 흐름                              │
└─────────────────────────────────────────────────────────────────┘

  External Request → Node1:5005
                          │
                          ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                    Ingress Network                            │
  │  ┌─────────┐      ┌─────────┐      ┌─────────┐              │
  │  │  Node1  │      │  Node2  │      │  Node3  │              │
  │  │ :5005   │◄────►│ :5005   │◄────►│ :5005   │              │
  │  └────┬────┘      └────┬────┘      └────┬────┘              │
  │       │                │                │                    │
  │       └────────────────┼────────────────┘                    │
  │                        │                                      │
  │              Layer 4 Load Balancing                          │
  │                        │                                      │
  │       ┌────────────────┼────────────────┐                    │
  │       ▼                ▼                ▼                    │
  │  ┌─────────┐      ┌─────────┐      ┌─────────┐              │
  │  │Replica 1│      │Replica 2│      │Replica 3│              │
  │  │  :80    │      │  :80    │      │  :80    │              │
  │  └─────────┘      └─────────┘      └─────────┘              │
  └───────────────────────────────────────────────────────────────┘
```

### 9. 트러블슈팅

#### 로그 위치

| 환경 | 로그 위치 |
|------|-----------|
| systemd | `journalctl -u docker.service` |
| Ubuntu (upstart) | `/var/log/upstart/docker.log` |
| RHEL | `/var/log/messages` |
| Debian | `/var/log/daemon.log` |
| Windows | Windows Event Viewer |

#### 디버그 모드 설정

```json
// /etc/docker/daemon.json
{
  "debug": true,
  "log-level": "debug"   // debug, info, warn, error, fatal
}
```

#### 컨테이너 로그 확인

```bash
# 컨테이너 로그
$ docker logs <container-name>

# Swarm 서비스 로그
$ docker service logs <service-name>
```

---

## 🔍 심화 학습

### 네트워크 드라이버별 사용 시나리오

| 시나리오 | 권장 드라이버 |
|----------|---------------|
| 로컬 개발/테스트 | bridge |
| 멀티 호스트 컨테이너 통신 | overlay |
| 기존 물리 네트워크 연결 | macvlan |
| 최고 성능 필요 | host |
| 완전 격리 | none |

### 추가 학습 주제
- Overlay 네트워크 (Chapter 14)
- 네트워크 보안 (암호화, 격리)
- 커스텀 IPAM 드라이버
- 서드파티 네트워크 플러그인

---

## 💡 실무 적용 포인트

### 면접 대비 질문

**Q1: CNM의 세 가지 핵심 구성 요소와 역할은?**
> **A**: **Sandbox**는 컨테이너의 격리된 네트워크 스택(인터페이스, 라우팅, DNS), **Endpoint**는 Sandbox를 Network에 연결하는 가상 NIC, **Network**는 Endpoint들을 그룹화하고 격리하는 가상 스위치이다.

**Q2: 기본 bridge 네트워크와 커스텀 bridge 네트워크의 차이점은?**
> **A**: 기본 `bridge` 네트워크는 DNS 기반 서비스 디스커버리를 지원하지 않아 컨테이너 이름으로 통신할 수 없다. 커스텀 bridge 네트워크는 `--name` 플래그로 생성한 컨테이너의 이름을 자동으로 DNS에 등록하여 이름 해석을 지원한다.

**Q3: MACVLAN 드라이버는 언제 사용하고, 어떤 제약이 있는가?**
> **A**: 컨테이너를 기존 물리 네트워크나 VLAN에 직접 연결할 때 사용한다. 각 컨테이너가 고유 MAC/IP를 받아 물리 서버처럼 보인다. 단, 호스트 NIC가 프로미스큐어스 모드여야 하므로 대부분의 퍼블릭 클라우드에서는 사용할 수 없다.

**Q4: Swarm의 Ingress 모드와 Host 모드 퍼블리싱 차이점은?**
> **A**: **Ingress 모드**는 모든 Swarm 노드에서 해당 포트로 접근 가능하며 내장 로드밸런서가 복제본들에 트래픽을 분산한다. **Host 모드**는 복제본이 실제로 실행 중인 노드에서만 접근 가능하다. Ingress가 기본이며 대부분의 경우 권장된다.

---

## ✅ 체크리스트

### CNM 이해
- [ ] Sandbox, Endpoint, Network 역할 설명 가능
- [ ] libnetwork와 드라이버의 Control/Data Plane 분리 이해
- [ ] 기본 제공 드라이버 종류와 용도 파악

### Bridge 네트워크
- [ ] `docker network create -d bridge`: 네트워크 생성
- [ ] `docker network inspect`: 네트워크 정보 확인
- [ ] `--network` 플래그로 컨테이너 연결
- [ ] DNS 기반 이름 해석 테스트
- [ ] Linux `brctl show`로 커널 브리지 확인

### 포트 매핑
- [ ] `--publish <host-port>:<container-port>`: 포트 매핑
- [ ] `docker port <container>`: 매핑 확인
- [ ] 포트 매핑의 한계 인식

### MACVLAN
- [ ] MACVLAN 네트워크 생성 (`-o parent=eth0.100`)
- [ ] `--ip-range`로 Docker 전용 IP 범위 지정
- [ ] 프로미스큐어스 모드 요구사항 이해

### 서비스 디스커버리
- [ ] Docker 내장 DNS 서버 동작 원리
- [ ] `--dns`와 `--dns-search` 플래그 활용
- [ ] 네트워크 스코프 개념 (같은 네트워크만 해석)

### 트러블슈팅
- [ ] Docker 데몬 로그 위치 파악
- [ ] 디버그 모드 설정 (`daemon.json`)
- [ ] `docker logs`로 컨테이너 로그 확인

---

## 🔗 참고 자료

- [Docker Network 공식 문서](https://docs.docker.com/network/)
- [Container Network Model (CNM)](https://github.com/moby/libnetwork/blob/master/docs/design.md)
- [libnetwork GitHub](https://github.com/moby/libnetwork)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 13
