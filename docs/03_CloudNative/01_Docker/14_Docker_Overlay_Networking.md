# 14장: Docker Overlay Networking

## 📌 핵심 요약

> **Overlay Network**는 여러 호스트에 걸쳐 **평면적이고 안전한 Layer 2 네트워크**를 생성한다. Docker는 **VXLAN 터널**을 사용하여 복잡한 underlay 네트워크 위에 단순한 overlay 네트워크를 구축하며, 컨테이너는 서로 다른 호스트에 있어도 마치 같은 네트워크에 있는 것처럼 직접 통신할 수 있다.

---

## 🎯 학습 목표

- [ ] Overlay 네트워크의 개념과 필요성 이해
- [ ] VXLAN 터널링 원리 파악
- [ ] Swarm 기반 overlay 네트워크 생성 및 테스트
- [ ] VTEP(VXLAN Tunnel Endpoint) 동작 방식 이해
- [ ] 컨테이너 간 통신 흐름(Traffic Flow) 분석
- [ ] Overlay 네트워크 암호화 옵션 활용

---

## 📖 본문 정리

### 1. Docker Overlay Networking 개요

#### Overlay Network란?

💬 **비유**: Overlay 네트워크는 **지하철 노선**과 같다. 지상의 복잡한 도로망(underlay)과 상관없이, 지하철은 역에서 역으로 직접 연결된다. 컨테이너도 마찬가지로 호스트의 물리적 네트워크 구조와 무관하게 overlay를 통해 직접 통신한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Overlay Network (L2)                        │
│  ┌──────────┐                              ┌──────────┐        │
│  │Container │ ◄─────── 직접 통신 ─────────► │Container │        │
│  │  10.0.0.3│          (같은 서브넷)        │  10.0.0.4│        │
│  └──────────┘                              └──────────┘        │
└─────────────────────────────────────────────────────────────────┘
        │                                          │
        │           VXLAN 터널 (암호화)              │
        ▼                                          ▼
┌───────────────┐    ┌──────────┐    ┌───────────────┐
│    Node1      │    │  Router  │    │    Node2      │
│  172.31.1.5   │────│          │────│  172.31.2.8   │
└───────────────┘    └──────────┘    └───────────────┘
        └──────────── Underlay Network (L3) ──────────┘
```

#### 핵심 특징

| 특징 | 설명 |
|------|------|
| **멀티 호스트** | 여러 Docker 호스트에 걸쳐 네트워크 생성 |
| **평면적 L2** | 컨테이너가 같은 서브넷에 있는 것처럼 통신 |
| **기본 암호화** | Control plane 기본 암호화, data plane 선택적 |
| **Swarm 통합** | Swarm의 key-value store와 보안 기능 활용 |

#### 역사적 배경

```
2015년 3월: Docker, Inc.가 Socket Plane 인수
├─ 목표 1: Docker에 overlay networking 도입
└─ 목표 2: 개발자를 위한 간단한 컨테이너 네트워킹

결과: libnetwork + native overlay driver
```

---

### 2. Overlay 네트워크 구축하기

#### 사전 요구사항: Swarm 클러스터

**필수 포트 (노드 간 개방 필요)**:

| 포트 | 프로토콜 | 용도 |
|------|----------|------|
| `2377` | TCP | Management plane 통신 |
| `7946` | TCP/UDP | Control plane (SWIM 기반 gossip) |
| `4789` | UDP | VXLAN data plane |

#### Swarm 초기화

```bash
# Node1에서 (Manager)
$ docker swarm init
Swarm initialized: current node (1ex3...o3px) is now a manager.

# Node2에서 (Worker)
$ docker swarm join \
  --token SWMTKN-1-0hz2ec...2vye \
  172.31.1.5:2377
This node joined a swarm as a worker.
```

#### Overlay 네트워크 생성

```bash
# 암호화된 overlay 네트워크 생성
$ docker network create -d overlay -o encrypted uber-net

# 네트워크 확인
$ docker network ls
NETWORK ID     NAME              DRIVER    SCOPE
vdu1yly429jv   uber-net          overlay   swarm   ← 새 overlay
```

**암호화 옵션**:

| 옵션 | Control Plane | Data Plane | 성능 영향 |
|------|---------------|------------|-----------|
| 기본 | ✅ 암호화 | ❌ 평문 | 없음 |
| `-o encrypted` | ✅ 암호화 | ✅ 암호화 (AES-GCM) | ~10% 감소 |

> ⚠️ **Lazy Extension**: Docker는 overlay 네트워크를 **필요할 때만** worker 노드로 확장한다. 컨테이너가 실행되기 전까지 node2에서 uber-net이 보이지 않는 이유!

#### 컨테이너 연결하기

```bash
# Swarm 서비스로 컨테이너 배포
$ docker service create --name test \
   --network uber-net \
   --replicas 2 \
   ubuntu sleep infinity

# 배포 상태 확인
$ docker service ps test
ID          NAME    IMAGE           NODE      CURRENT STATE
sm1...1nw   test.1  ubuntu:latest   node1     Running
tro...kgk   test.2  ubuntu:latest   node2     Running
```

> 💡 **Standalone 컨테이너 연결**: `--attachable` 플래그로 네트워크 생성 필요
> ```bash
> $ docker network create -d overlay --attachable my-overlay
> ```

---

### 3. Overlay 네트워크 테스트

#### 네트워크 정보 확인

```bash
$ docker network inspect uber-net
[
    {
        "Name": "uber-net",
        "Subnet": "10.0.0.0/24",           ← Overlay 서브넷
        "Gateway": "10.0.0.1",
        "Containers": {
            "Name": "test.1.tro...kgk",
            "IPv4Address": "10.0.0.3/24",  ← 컨테이너 IP
        }
    }
]
```

#### 컨테이너 IP 확인

```bash
# 컨테이너 ID 확인
$ docker ps
CONTAINER ID   IMAGE           NAME
d7766923a5a7   ubuntu:latest   test.1.tro...kgk

# IP 주소 추출
$ docker inspect \
  --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' d7766923a5a7
10.0.0.3
```

#### Ping 테스트

```bash
# 컨테이너 접속
$ docker exec -it d7766923a5a7 bash

# ping 도구 설치
# apt update && apt-get install iputils-ping -y

# IP로 ping
# ping 10.0.0.4
64 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=1.06 ms

# 이름으로 ping (DNS 해석)
# ping test.2.sm180xqwm7k1bsyn3mt1fj1nw
64 bytes from test.2.sm1...1nw.uber-net (10.0.0.4): icmp_seq=1 ttl=64
```

#### Traceroute 확인

```bash
# traceroute 설치 및 실행
# apt install traceroute
# traceroute 10.0.0.4
traceroute to 10.0.0.4, 30 hops max
 1  test.2.sm1...1nw.uber-net (10.0.0.4)  1.110ms
```

> 🎯 **Single Hop**: traceroute 결과가 1홉인 이유는 컨테이너가 overlay 네트워크를 통해 **직접 통신**하기 때문. Underlay의 복잡한 경로는 추상화됨.

---

### 4. VXLAN 기술 심층 분석

#### VXLAN이란?

💬 **비유**: VXLAN은 **편지봉투**와 같다. 원본 편지(L2 프레임)를 봉투(UDP 패킷)에 넣어서 우체국(라우터)이 처리할 수 있게 한다. 봉투 안의 내용물(원본 트래픽)은 우체국이 알 필요 없이 목적지에 전달된다.

```
┌────────────────────────────────────────────────────────┐
│           VXLAN Encapsulation                          │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Original L2 Frame (Container Traffic)            │ │
│  │ ┌────────┬────────┬──────────────────┐          │ │
│  │ │Dst MAC │Src MAC │ Payload (Ping)   │          │ │
│  │ └────────┴────────┴──────────────────┘          │ │
│  └──────────────────────────────────────────────────┘ │
│                        ▼                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │ VXLAN Encapsulated Packet                        │ │
│  │ ┌────────┬────────┬────────┬────────┬─────────┐ │ │
│  │ │Outer IP│UDP 4789│VXLAN   │Original│ Payload │ │ │
│  │ │Header  │Header  │Header  │L2 Frame│         │ │ │
│  │ └────────┴────────┴────────┴────────┴─────────┘ │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

#### VTEP (VXLAN Tunnel Endpoint)

```
┌─────────────────────────────────────────────────────────────────┐
│                        VXLAN 터널 구조                          │
│                                                                 │
│  Node1                                           Node2          │
│  ┌────────────────────┐       ┌────────────────────┐           │
│  │   Sandbox (netns)  │       │   Sandbox (netns)  │           │
│  │  ┌──────────────┐  │       │  ┌──────────────┐  │           │
│  │  │  Container   │  │       │  │  Container   │  │           │
│  │  │   10.0.0.3   │  │       │  │   10.0.0.4   │  │           │
│  │  └──────┬───────┘  │       │  └──────┬───────┘  │           │
│  │         │veth      │       │         │veth      │           │
│  │  ┌──────┴───────┐  │       │  ┌──────┴───────┐  │           │
│  │  │   Br0 Switch │  │       │  │   Br0 Switch │  │           │
│  │  └──────┬───────┘  │       │  └──────┬───────┘  │           │
│  │         │          │       │         │          │           │
│  │  ┌──────┴───────┐  │       │  ┌──────┴───────┐  │           │
│  │  │     VTEP     │  │       │  │     VTEP     │  │           │
│  │  │  172.31.1.5  │  │       │  │  172.31.2.8  │  │           │
│  │  └──────┬───────┘  │       │  └──────┬───────┘  │           │
│  └─────────┼──────────┘       └─────────┼──────────┘           │
│            │                            │                       │
│            └────────── VXLAN ───────────┘                       │
│                       Tunnel                                    │
│                    (UDP/4789)                                   │
└─────────────────────────────────────────────────────────────────┘
```

**VTEP의 역할**:

| 기능 | 설명 |
|------|------|
| **Encapsulation** | L2 프레임을 UDP 패킷으로 캡슐화 |
| **De-encapsulation** | 수신된 UDP 패킷에서 원본 프레임 추출 |
| **VNID 매핑** | VLAN ↔ VXLAN Network ID 변환 |
| **터널 종단점** | VXLAN 터널의 시작과 끝 |

---

### 5. Traffic Flow 상세 분석

#### C1 → C2 Ping 과정

```
┌─────────────────────────────────────────────────────────────────┐
│                     Ping 10.0.0.4 트래픽 흐름                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: C1이 ping 시작                                         │
│  ┌─────────┐                                                    │
│  │   C1    │ ping 10.0.0.4                                      │
│  │10.0.0.3 │──────┐                                             │
│  └─────────┘      │                                             │
│                   ▼                                             │
│  Step 2: ARP 캐시 미스 → Br0로 flood                            │
│  ┌─────────┐      │                                             │
│  │   Br0   │◄─────┘  "10.0.0.4의 MAC은?"                        │
│  └────┬────┘                                             │
│       │                                                         │
│       ▼                                                         │
│  Step 3: Br0가 VTEP으로 전달 + Proxy ARP 응답                    │
│  ┌─────────┐                                                    │
│  │  VTEP   │  gossip으로 C2 정보 이미 알고 있음                  │
│  └────┬────┘                                                    │
│       │                                                         │
│       ▼                                                         │
│  Step 4: VXLAN 캡슐화                                           │
│  ┌────────────────────────────────────────────┐                │
│  │ Outer IP: 172.31.1.5 → 172.31.2.8          │                │
│  │ UDP: 4789                                   │                │
│  │ VXLAN Header: VNID=xxxxx                   │                │
│  │ Inner Frame: 10.0.0.3 → 10.0.0.4 (Ping)    │                │
│  └────────────────────────────────────────────┘                │
│       │                                                         │
│       │  Underlay 네트워크 통과 (라우터는 일반 UDP로 인식)        │
│       ▼                                                         │
│  Step 5: Node2 VTEP 수신                                        │
│  ┌─────────┐                                                    │
│  │  VTEP   │  UDP/4789 → VTEP로 전달                            │
│  └────┬────┘                                                    │
│       │                                                         │
│       ▼                                                         │
│  Step 6: VXLAN 디캡슐화 + VNID로 VLAN 결정                       │
│  ┌─────────┐                                                    │
│  │   Br0   │  원본 L2 프레임 복원                                │
│  └────┬────┘                                                    │
│       │                                                         │
│       ▼                                                         │
│  Step 7: C2에 전달                                              │
│  ┌─────────┐                                                    │
│  │   C2    │  Ping 수신!                                        │
│  │10.0.0.4 │                                                    │
│  └─────────┘                                                    │
└─────────────────────────────────────────────────────────────────┘
```

#### VXLAN 패킷 구조 상세

| 레이어 | 필드 | 값 예시 | 설명 |
|--------|------|---------|------|
| **Outer Ethernet** | Dst MAC | Node2 MAC | 다음 홉 MAC |
| **Outer IP** | Src IP | 172.31.1.5 | Node1 VTEP IP |
| | Dst IP | 172.31.2.8 | Node2 VTEP IP |
| **UDP** | Dst Port | 4789 | VXLAN 표준 포트 |
| **VXLAN Header** | VNID | 24-bit ID | 네트워크 격리 식별자 |
| **Inner Ethernet** | 원본 프레임 | C1→C2 | 컨테이너 간 실제 트래픽 |

---

### 6. 멀티 서브넷 Overlay

#### Layer 3 라우팅 지원

```bash
# 두 개의 서브넷을 가진 overlay 생성
$ docker network create \
  --subnet=10.1.1.0/24 \
  --subnet=11.1.1.0/24 \
  -d overlay \
  prod-net
```

**내부 구조**:

```
┌───────────────────────────────────────────┐
│           prod-net Overlay                │
│                                           │
│  ┌─────────────┐     ┌─────────────┐     │
│  │    Br0      │     │    Br1      │     │
│  │ 10.1.1.0/24 │◄───►│ 11.1.1.0/24 │     │
│  └─────────────┘     └─────────────┘     │
│        │      Docker가 자동으로      │     │
│        │      라우팅 처리           │     │
│  ┌─────┴─────┐            ┌─────┴─────┐ │
│  │Container A│            │Container B│ │
│  │ 10.1.1.5  │            │ 11.1.1.5  │ │
│  └───────────┘            └───────────┘ │
└───────────────────────────────────────────┘
```

---

### 7. 주요 명령어 정리

| 명령어 | 설명 |
|--------|------|
| `docker network create -d overlay` | Overlay 네트워크 생성 |
| `-o encrypted` | Data plane 암호화 활성화 |
| `--attachable` | Standalone 컨테이너 연결 허용 |
| `--subnet` | 서브넷 지정 (다중 가능) |
| `docker network ls` | 네트워크 목록 (Swarm에서는 필요시만 표시) |
| `docker network inspect` | 상세 정보 (서브넷, IP, VNID, 암호화 상태) |
| `docker network rm` | 네트워크 삭제 |

---

### 8. 정리 (Clean up)

```bash
# 서비스 삭제
$ docker service rm test

# 네트워크 삭제 (서비스 삭제 후 잠시 대기 필요)
$ docker network rm uber-net

# Swarm 해제 (node2 먼저, 그 다음 node1)
$ docker swarm leave -f
```

---

## 🔍 심화 학습

### Overlay vs Bridge 네트워크 비교

| 특성 | Bridge | Overlay |
|------|--------|---------|
| **범위** | 단일 호스트 | 멀티 호스트 |
| **기술** | Linux bridge | VXLAN 터널 |
| **Swarm 필요** | ❌ | ✅ |
| **암호화** | ❌ | ✅ (선택적) |
| **성능** | 높음 | 중간 (~10% 오버헤드 with 암호화) |
| **사용 사례** | 개발/테스트 | 프로덕션 MSA |

### VXLAN vs 다른 Overlay 기술

| 기술 | 캡슐화 | 최대 네트워크 수 | 표준 포트 |
|------|--------|------------------|-----------|
| **VXLAN** | UDP | 16M (24-bit VNID) | 4789 |
| **GRE** | IP | 4K | N/A |
| **Geneve** | UDP | 16M | 6081 |

### 핵심 참고 자료

1. **VXLAN RFC 7348**: https://tools.ietf.org/html/rfc7348
2. **Docker Networking Documentation**: https://docs.docker.com/network/
3. **libnetwork GitHub**: https://github.com/moby/libnetwork

---

## 💡 실무 적용 포인트

### 면접 대비 Q&A

**Q1: Docker Overlay 네트워크가 필요한 이유는?**

> A: 실제 마이크로서비스 환경에서 컨테이너는 여러 호스트에 분산 배포됩니다. Overlay 네트워크는 이러한 컨테이너들이 마치 같은 로컬 네트워크에 있는 것처럼 통신할 수 있게 해줍니다. 복잡한 underlay 인프라를 추상화하고, 기본적으로 안전한 통신을 제공합니다.

**Q2: VXLAN이 기존 네트워크 인프라와 호환되는 이유는?**

> A: VXLAN은 원본 L2 프레임을 표준 UDP 패킷(포트 4789)으로 캡슐화합니다. 기존 라우터와 스위치는 이를 일반 IP/UDP 트래픽으로 인식하므로 별도의 설정 변경 없이 기존 인프라를 통과할 수 있습니다.

**Q3: Overlay 네트워크 암호화의 성능 영향은?**

> A: `-o encrypted` 옵션으로 data plane을 암호화하면 약 10%의 성능 저하가 발생합니다. Control plane은 기본적으로 암호화되며, 암호화 키는 12시간마다 자동 로테이션됩니다. 보안 요구사항과 성능 사이의 트레이드오프를 고려해야 합니다.

**Q4: Worker 노드에서 overlay 네트워크가 바로 보이지 않는 이유는?**

> A: Docker는 "Lazy Extension" 전략을 사용합니다. Overlay 네트워크는 해당 노드에서 실제로 컨테이너가 실행될 때만 확장됩니다. 이는 네트워크 관련 gossip 트래픽을 최소화하여 대규모 Swarm의 확장성을 향상시킵니다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] Overlay 네트워크가 멀티 호스트 간 L2 통신을 제공하는 방식 이해
- [ ] VXLAN 캡슐화/디캡슐화 과정 설명 가능
- [ ] VTEP의 역할과 위치 파악
- [ ] Underlay vs Overlay 네트워크 구분

### 실습 완료
- [ ] Swarm 클러스터 구성 (2+ 노드)
- [ ] 암호화된 overlay 네트워크 생성
- [ ] 서비스 배포 및 레플리카 확인
- [ ] 컨테이너 간 ping/traceroute 테스트
- [ ] `docker network inspect`로 VNID, 서브넷 확인

### 아키텍처 이해
- [ ] Sandbox(netns) + Br0 + VTEP 구조 도식화 가능
- [ ] Traffic Flow 7단계 설명 가능
- [ ] VXLAN 패킷 구조 (Outer IP, UDP, VXLAN Header, Inner Frame)
- [ ] 멀티 서브넷 overlay의 내부 라우팅

### 운영 지식
- [ ] 필수 포트: 2377/tcp, 7946/tcp+udp, 4789/udp
- [ ] 암호화 옵션과 성능 트레이드오프
- [ ] Lazy Extension의 확장성 이점
- [ ] `--attachable` 플래그 사용 시점

---

## 🔗 참고 자료

- [Docker Overlay Networks](https://docs.docker.com/network/overlay/)
- [VXLAN: A Framework for Overlaying Virtualized Layer 2 Networks (RFC 7348)](https://tools.ietf.org/html/rfc7348)
- [libnetwork Design](https://github.com/moby/libnetwork/blob/master/docs/design.md)
- [Docker Swarm Mode Networking](https://docs.docker.com/engine/swarm/networking/)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 14
