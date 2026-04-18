# Ch08. Docker Networking - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Bridge 네트워크와 MACVLAN의 성능 차이는 얼마나 나며, 언제 MACVLAN을 선택해야 하는가?

### 왜 이 질문이 중요한가
Bridge는 기본 드라이버로 사용하기 쉽지만, MACVLAN은 설정이 복잡하다. 성능 이점이 명확하지 않으면 복잡도를 감수할 이유가 없다.

### 답변
**Bridge 네트워크의 패킷 경로**:
```
Container → veth → Bridge → iptables (NAT) → Host NIC → Network
  ↑         ↑       ↑         ↑
  앱       가상NIC  L2스위치   방화벽/라우팅
```
- **3~4개의 네트워크 홉**
- **iptables NAT 오버헤드** (CPU 사용)
- **커널 네트워크 스택 2회 통과** (Container → Host → Network)

**MACVLAN의 패킷 경로**:
```
Container → MACVLAN Sub-interface → Host NIC → Network
  ↑              ↑                      ↑
  앱         고유 MAC/IP             물리 NIC
```
- **1~2개의 네트워크 홉**
- **NAT 없음** (컨테이너가 직접 물리 네트워크 IP 사용)
- **커널 스택 1회 통과**

**성능 측정 결과** (10Gbps 네트워크 기준):
| 메트릭 | Bridge | MACVLAN | 차이 |
|--------|--------|---------|------|
| Throughput | ~9.2 Gbps | ~9.8 Gbps | +6% |
| Latency (avg) | 0.15ms | 0.08ms | -47% |
| CPU Usage | 15% | 8% | -47% |
| iptables rules | 수십 개 | 0개 | - |

**MACVLAN 선택 시나리오**:
1. **레거시 앱 마이그레이션**: 고정 IP가 필요하거나 브로드캐스트/멀티캐스트 사용
2. **네트워크 집약적 워크로드**: 고성능 데이터베이스, 캐시, 메시지 큐
3. **기존 모니터링 통합**: VLAN 기반 네트워크 모니터링 도구 사용 중
4. **포트 충돌 회피**: 여러 컨테이너가 같은 포트를 사용해야 하는 경우
5. **Bare-metal 환경**: 클라우드가 아닌 자체 데이터센터

**MACVLAN 제약사항**:
- **프로미스큐어스 모드 필요**: 일부 스위치에서 보안 정책으로 차단
- **퍼블릭 클라우드 미지원**: AWS, Azure, GCP에서 작동 안 함
- **호스트-컨테이너 통신 불가**: 추가 MACVLAN 인터페이스를 호스트에 생성해야 함
- **IP 관리 복잡도**: DHCP 서버 필요하거나 수동 IP 할당

### 실무 적용
대부분의 경우 Bridge로 충분하다. MACVLAN은 온프레미스 환경에서 레거시 시스템을 컨테이너로 마이그레이션할 때 주로 사용된다. 클라우드 환경에서는 대신 Overlay 네트워크나 CNI 플러그인(Calico, Cilium)을 사용한다.

---

## Q2. Overlay 네트워크에서 VXLAN 캡슐화가 성능에 미치는 영향은 얼마나 큰가?

### 왜 이 질문이 중요한가
Overlay 네트워크는 멀티 호스트 통신에 필수적이지만, VXLAN 캡슐화로 인한 오버헤드가 발생한다. 이 비용을 정량화하지 못하면 아키텍처 결정을 내리기 어렵다.

### 답변
**VXLAN 오버헤드 분석**:

**패킷 크기 증가**:
```
원본 이더넷 프레임: 1500 bytes (MTU)
├─ Ethernet Header: 14 bytes
├─ IP Header: 20 bytes
├─ TCP Header: 20 bytes
└─ Payload: 1446 bytes

VXLAN 캡슐화 후:
├─ Outer Ethernet: 14 bytes  ← 추가
├─ Outer IP: 20 bytes        ← 추가
├─ UDP Header: 8 bytes       ← 추가
├─ VXLAN Header: 8 bytes     ← 추가
└─ Original Frame: 1500 bytes
───────────────────────────
Total: 1550 bytes (→ MTU 초과, 단편화 발생 가능!)
```

**성능 영향**:
| 메트릭 | Overlay (암호화 OFF) | Overlay (암호화 ON) | Host 네트워크 | 차이 |
|--------|---------------------|---------------------|---------------|------|
| Throughput | ~9.1 Gbps | ~8.2 Gbps | ~9.4 Gbps | -3% / -13% |
| Latency | +0.1ms | +0.3ms | 기준 | +5% / +15% |
| CPU Usage | +5% | +12% | 기준 | - |
| 패킷 크기 | +50 bytes | +50 bytes | 기준 | - |

**암호화 오버헤드**:
- `-o encrypted` 옵션: AES-GCM을 사용한 IPSec 암호화
- CPU 집약적: 10Gbps에서 ~10-15% 처리량 감소
- 키 로테이션: 12시간마다 자동 (추가 오버헤드 미미)

**최적화 전략**:

**1. MTU 조정**:
```bash
# Overlay 네트워크 생성 시 MTU 설정
docker network create -d overlay \
  --opt com.docker.network.driver.mtu=1450 \
  mynet

# 호스트 NIC MTU가 9000 (Jumbo Frame)이면 더 여유 있음
```

**2. TCP 최적화**:
```bash
# 컨테이너에서 TCP Segmentation Offload 활성화
docker run --sysctl net.ipv4.tcp_mtu_probing=1 ...
```

**3. 암호화 선택적 적용**:
```bash
# 민감한 데이터만 암호화 네트워크 사용
docker network create -d overlay -o encrypted secure-net
docker network create -d overlay fast-net  # 암호화 OFF

# 서비스별로 네트워크 선택
docker service create --network secure-net payment-service
docker service create --network fast-net cache-service
```

**4. Hardware Offload**:
- NIC가 VXLAN offload 지원 시 CPU 부담 감소 (Intel X710, Mellanox ConnectX 등)

### 실무 적용
대부분의 마이크로서비스에서 ~10% 오버헤드는 허용 가능하다. 극한의 성능이 필요하면 (HFT, 실시간 스트리밍 등) Host 네트워크 모드나 SR-IOV 같은 기술을 고려한다. 보안이 중요한 서비스는 암호화 오버헤드를 감수하고 `-o encrypted`를 사용한다.

---

## Q3. DNS 라운드 로빈의 한계는 무엇이며, 어떻게 보완할 수 있는가?

### 왜 이 질문이 중요한가
같은 서비스의 여러 복제본이 있을 때 Docker는 DNS 라운드 로빈으로 로드밸런싱한다. 하지만 이는 진정한 로드밸런싱이 아니다.

### 답변
**Docker DNS의 동작**:
```bash
# Swarm 서비스 3개 복제본
$ docker service create --name web --replicas 3 nginx

# DNS 조회
$ nslookup web
Name:   web
Address: 10.0.0.2
Address: 10.0.0.3
Address: 10.0.0.4
```

**라운드 로빈의 한계**:

**1. 캐싱 문제**:
```
Client → DNS 조회 → 10.0.0.2 (캐시 60초)
  │
  └─→ 60초 동안 계속 10.0.0.2로만 요청
      (10.0.0.3, 10.0.0.4는 유휴 상태)
```

**2. 불균등 분산**:
- 클라이언트 A: 10.0.0.2 (60초)
- 클라이언트 B: 10.0.0.2 (60초) ← 같은 IP!
- 클라이언트 C: 10.0.0.3 (60초)
- 결과: 10.0.0.2에 2배 부하

**3. 헬스체크 미반영**:
- 10.0.0.3이 다운되어도 DNS는 여전히 반환
- 클라이언트는 연결 실패 후 재시도해야 함

**4. Sticky 세션 불가**:
- 같은 클라이언트가 매번 다른 백엔드로 라우팅될 수 있음
- 세션 기반 앱에서 문제

**보완 방법**:

**1. Swarm Ingress 모드 (VIP 로드밸런싱)**:
```bash
# VIP (Virtual IP) 로드밸런싱
$ docker service create --name web \
  --endpoint-mode vip \  # 기본값
  --replicas 3 \
  nginx

# DNS 조회 결과
$ nslookup web
Name:   web
Address: 10.0.0.10  ← 하나의 VIP만 반환

# VIP가 IPVS로 백엔드에 분산
VIP 10.0.0.10 → IPVS → 10.0.0.2, 10.0.0.3, 10.0.0.4
```

**2. 클라이언트 사이드 로드밸런싱**:
```javascript
// Node.js 예시: DNS 캐시 비활성화 + 재시도
const dns = require('dns');
dns.setDefaultResultOrder('ipv4first');

const options = {
  lookup: (hostname, options, callback) => {
    dns.resolve4(hostname, (err, addresses) => {
      if (err) return callback(err);
      // 랜덤하게 하나 선택
      const addr = addresses[Math.floor(Math.random() * addresses.length)];
      callback(null, addr, 4);
    });
  }
};
```

**3. Nginx/HAProxy 프록시**:
```nginx
upstream backend {
    least_conn;  # 최소 연결 수 기반 분산
    server web.1.task:80;
    server web.2.task:80;
    server web.3.task:80;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

**4. Service Mesh (Envoy/Istio)**:
```yaml
# Envoy가 자동으로 헬스체크 + 로드밸런싱
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 80
---
# Istio가 트래픽 분산 + 서킷 브레이커 + 재시도 처리
```

### 실무 적용
Swarm에서는 VIP 모드가 기본이므로 문제가 적다. Kubernetes에서는 kube-proxy가 iptables/IPVS로 진정한 로드밸런싱을 제공한다. 외부 트래픽은 Nginx Ingress나 Traefik을 사용하여 고급 로드밸런싱 (가중치, 헬스체크, Circuit Breaker)을 적용한다.

---

## Q4. 네트워크 격리와 보안을 어떻게 구현하는가? (NetworkPolicy 개념)

### 왜 이 질문이 중요한가
같은 Docker 네트워크에 있는 모든 컨테이너는 기본적으로 서로 통신할 수 있다. 마이크로서비스 환경에서 이는 보안 위험이다.

### 답변
**기본 상태의 문제**:
```
┌─────────────────────────────────────────────────┐
│            myapp_default 네트워크                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ frontend │◄─┼─► api    │◄─┼─► db     │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│       ▲              ▲              ▲           │
│       └──────────────┼──────────────┘           │
│  frontend가 db에 직접 접근 가능! (위험)          │
└─────────────────────────────────────────────────┘
```

**해결책 1: 네트워크 분리**:
```yaml
services:
  frontend:
    networks:
      - public

  api:
    networks:
      - public
      - backend

  db:
    networks:
      - backend

  redis:
    networks:
      - backend

networks:
  public:
  backend:
    internal: true  # 외부 인터넷 접근 차단
```

**해결책 2: iptables 규칙 추가**:
```bash
# Docker가 생성한 브리지 확인
$ brctl show
bridge name       interfaces
br-abc123def      veth1a2b3c4

# 특정 컨테이너 간 통신 차단
$ iptables -I DOCKER-USER -s 172.18.0.2 -d 172.18.0.3 -j DROP
# frontend (172.18.0.2) → db (172.18.0.3) 차단
```

**해결책 3: Docker Network Plugin (Calico 예시)**:
```yaml
# Calico NetworkPolicy (Kubernetes 스타일)
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  selector: service == 'db'
  ingress:
    - action: Allow
      source:
        selector: service == 'api'
    - action: Deny
      source: {}
  egress:
    - action: Allow
```

**해결책 4: Swarm + 암호화 네트워크**:
```bash
# 암호화된 Overlay 네트워크
$ docker network create -d overlay \
  -o encrypted \
  --attachable \
  secure-net

# 민감한 서비스만 연결
$ docker service create --network secure-net payment-service
$ docker service create --network secure-net billing-service
```

**보안 체크리스트**:
- [ ] DB/Cache는 절대 public 네트워크에 노출 안 함
- [ ] Frontend와 Backend 네트워크 분리
- [ ] 내부 네트워크는 `internal: true` 설정
- [ ] 민감한 트래픽은 `-o encrypted` 사용
- [ ] 불필요한 포트 매핑 제거 (--publish 최소화)
- [ ] 컨테이너 간 통신은 서비스명 사용 (IP 하드코딩 금지)

### 실무 적용
Kubernetes 환경에서는 NetworkPolicy 리소스로 세밀한 트래픽 제어를 할 수 있다. Istio 같은 Service Mesh를 사용하면 mTLS로 모든 서비스 간 통신을 암호화하고, Authorization Policy로 접근 제어를 구현한다.

---

## Q5. IPv6 지원 상태는 어떻게 되며, IPv4/IPv6 듀얼 스택을 어떻게 구성하는가?

### 왜 이 질문이 중요한가
일부 클라우드 환경이나 ISP는 IPv6를 우선하거나 IPv6 전용으로 제공한다. Docker의 IPv6 지원을 이해하지 못하면 네트워크 장애가 발생할 수 있다.

### 답변
**Docker의 IPv6 지원 현황**:
- **기본적으로 비활성화**: Docker는 IPv4만 사용
- **수동 활성화 필요**: 데몬 설정 파일에서 명시적으로 활성화
- **듀얼 스택 지원**: IPv4와 IPv6 동시 사용 가능
- **NAT64 미지원**: IPv6 전용 컨테이너가 IPv4 서비스에 접근하려면 외부 게이트웨이 필요

**IPv6 활성화 (Bridge 네트워크)**:

**1. Docker 데몬 설정**:
```json
// /etc/docker/daemon.json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64",
  "experimental": true,
  "ip6tables": true
}
```

```bash
$ sudo systemctl restart docker
```

**2. 네트워크 생성**:
```bash
# IPv4/IPv6 듀얼 스택 네트워크
$ docker network create --ipv6 \
  --subnet=172.20.0.0/16 \
  --subnet=2001:db8::/64 \
  mynet

# 네트워크 검사
$ docker network inspect mynet
"IPAM": {
  "Config": [
    { "Subnet": "172.20.0.0/16" },
    { "Subnet": "2001:db8::/64" }
  ]
}
```

**3. 컨테이너 실행 및 확인**:
```bash
$ docker run -it --rm --network mynet alpine sh

# ip addr show eth0
eth0:
    inet 172.20.0.2/16
    inet6 2001:db8::2/64
    inet6 fe80::42:acff:fe14:2/64 scope link

# ping6 google.com
PING google.com (2404:6800:4004:820::200e): 56 data bytes
```

**Overlay 네트워크에서 IPv6**:
```bash
$ docker network create -d overlay \
  --ipv6 \
  --subnet=2001:db8:abcd::/64 \
  --attachable \
  myoverlay
```

**IPv6 전용 컨테이너**:
```bash
# IPv6만 사용 (IPv4 서브넷 없음)
$ docker network create --ipv6 \
  --subnet=2001:db8:2::/64 \
  ipv6only

$ docker run --network ipv6only nginx

# 주의: IPv4 서비스 접근 불가!
# NAT64 게이트웨이 필요
```

**문제 해결**:

**1. Host IPv6 활성화 확인**:
```bash
$ cat /proc/sys/net/ipv6/conf/all/disable_ipv6
0  # 0이면 활성화, 1이면 비활성화
```

**2. ip6tables 규칙 확인**:
```bash
$ sudo ip6tables -L -n -v
# Docker가 생성한 IPv6 NAT 규칙 확인
```

**3. 외부 IPv6 접근 테스트**:
```bash
$ docker run --rm --network mynet curlimages/curl:latest \
  curl -6 https://ipv6.google.com
```

### 실무 적용
AWS의 IPv6 전용 서브넷이나 Google Cloud의 IPv6 우선 네트워크에서는 듀얼 스택 설정이 필수다. Kubernetes에서는 CNI 플러그인(Calico, Cilium)이 IPv6를 네이티브로 지원한다. 프로덕션에서는 IPv4/IPv6 듀얼 스택을 권장한다.

---

## Q6. Service Mesh (Istio, Linkerd)와 Docker 네트워킹의 관계는?

### 왜 이 질문이 중요한가
마이크로서비스가 증가하면 네트워크 복잡도가 기하급수적으로 늘어난다. Service Mesh는 이 문제를 해결하는 현대적 접근법이다.

### 답변
**Docker 네트워킹의 한계**:
1. **단순 로드밸런싱**: 라운드 로빈만 지원, 가중치/지연 기반 라우팅 불가
2. **제한적 관측성**: 어느 서비스가 어느 서비스를 호출하는지 추적 어려움
3. **재시도/타임아웃 로직 없음**: 앱 레벨에서 직접 구현해야 함
4. **서킷 브레이커 없음**: 장애 전파 방지 불가
5. **보안 정책 부족**: mTLS 수동 구성 필요

**Service Mesh가 해결하는 문제**:

```
┌─────────────────────────────────────────────────────────┐
│              Without Service Mesh                        │
├─────────────────────────────────────────────────────────┤
│  Service A                    Service B                  │
│  ┌──────────────────┐         ┌──────────────────┐      │
│  │ • HTTP Client    │────────►│ • HTTP Server    │      │
│  │ • Retry Logic    │         │ • Auth Logic     │      │
│  │ • Circuit Breaker│         │ • Metrics        │      │
│  │ • Metrics        │         │ • Tracing        │      │
│  │ • Tracing        │         │ • Logging        │      │
│  │ • mTLS           │         │ • mTLS           │      │
│  └──────────────────┘         └──────────────────┘      │
│                                                          │
│  모든 서비스가 같은 로직을 중복 구현 (유지보수 악몽)    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              With Service Mesh (Istio)                   │
├─────────────────────────────────────────────────────────┤
│  Service A              Service B                        │
│  ┌────────┐             ┌────────┐                       │
│  │  App   │             │  App   │                       │
│  │(단순화) │             │(단순화) │                       │
│  └───┬────┘             └───┬────┘                       │
│      │                      │                            │
│  ┌───┴────┐             ┌───┴────┐                       │
│  │ Envoy  │────────────►│ Envoy  │                       │
│  │ Proxy  │  mTLS+암호화 │ Proxy  │                       │
│  └────────┘             └────────┘                       │
│      │                      │                            │
│      └──── Telemetry ───────┴──► Control Plane (Istio)  │
│                                   • Traffic Management   │
│                                   • Security             │
│                                   • Observability        │
└─────────────────────────────────────────────────────────┘
```

**Istio + Docker 네트워킹 통합**:

**1. Sidecar 패턴**:
```yaml
# Kubernetes Pod 예시
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:latest
  - name: istio-proxy  # Sidecar
    image: istio/proxyv2:latest
```

**2. 트래픽 가로채기**:
```bash
# Envoy가 모든 Inbound/Outbound 트래픽을 가로챔
iptables -t nat -A OUTPUT -p tcp -j REDIRECT --to-port 15001  # Outbound
iptables -t nat -A PREROUTING -p tcp -j REDIRECT --to-port 15006  # Inbound
```

**3. Service Mesh 제공 기능**:

**a. 트래픽 관리**:
```yaml
# Canary Deployment (10% 트래픽만 v2로)
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - match:
    - headers:
        user:
          exact: tester
    route:
    - destination:
        host: myapp
        subset: v2
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 90
    - destination:
        host: myapp
        subset: v2
      weight: 10
```

**b. 복원력**:
```yaml
# Retry + Circuit Breaker
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
    outlierDetection:  # Circuit Breaker
      consecutiveErrors: 5
      interval: 30s
      baseEjectionTime: 1m
```

**c. 보안 (mTLS)**:
```yaml
# 모든 서비스 간 mTLS 강제
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT  # PERMISSIVE | STRICT | DISABLE
```

**d. 관측성**:
```bash
# Distributed Tracing (Jaeger)
curl http://myapp/endpoint
# → Jaeger UI에서 전체 요청 흐름 시각화

# Metrics (Prometheus + Grafana)
# → 서비스별 요청 수, 지연, 에러율 대시보드
```

**Docker Swarm + Istio**:
- Istio는 주로 Kubernetes 환경 지원
- Swarm에서는 Consul Connect나 Linkerd 1.x 고려

### 실무 적용
소규모 앱은 Service Mesh 없이 Docker 네트워킹으로 충분하다. 마이크로서비스가 10개 이상 넘어가고, 카나리 배포/서킷 브레이커/분산 추적이 필요하면 Istio를 도입한다. 초기 학습 곡선이 가파르지만, 중앙화된 정책 관리와 관측성 이점이 크다.

---

## Q7. 네트워크 디버깅 시 유용한 도구와 기법은 무엇인가?

### 왜 이 질문이 중요한가
컨테이너 네트워킹 문제는 디버깅이 어렵다. 컨테이너는 격리되어 있고, 네트워크 스택이 가상화되어 있기 때문이다.

### 답변
**디버깅 도구 모음**:

**1. nicolaka/netshoot (만능 도구)**:
```bash
# 네트워크 디버깅 전용 컨테이너 실행
$ docker run -it --rm --network container:myapp \
  nicolaka/netshoot

# 포함된 도구:
# - tcpdump, tshark (패킷 캡처)
# - curl, wget (HTTP 테스트)
# - nmap, ncat (포트 스캔)
# - iftop, iperf3 (대역폭 측정)
# - dig, nslookup (DNS 조회)
# - traceroute, mtr (경로 추적)
# - ss, netstat (소켓 상태)
```

**2. DNS 문제 진단**:
```bash
# 컨테이너 내부 DNS 확인
$ docker exec myapp cat /etc/resolv.conf
nameserver 127.0.0.11  # Docker 내장 DNS

# DNS 쿼리 테스트
$ docker exec myapp nslookup db
Server:    127.0.0.11
Name:      db
Address:   172.18.0.3

# 직접 DNS 서버 쿼리
$ docker exec myapp dig @127.0.0.11 db +short
172.18.0.3
```

**3. 연결 테스트**:
```bash
# 포트 접근 가능 여부
$ docker exec myapp nc -zv db 5432
Connection to db (172.18.0.3) 5432 port [tcp/postgresql] succeeded!

# HTTP 엔드포인트 테스트
$ docker exec myapp curl -v http://api:8080/health
```

**4. 패킷 캡처**:
```bash
# 컨테이너 내부에서 캡처
$ docker run --rm --network container:myapp \
  nicolaka/netshoot tcpdump -i any port 5432 -w /tmp/dump.pcap

# 호스트에서 veth 인터페이스 캡처
$ docker inspect myapp | grep -i pid
"Pid": 12345
$ nsenter -t 12345 -n tcpdump -i eth0 -w /tmp/dump.pcap
```

**5. 라우팅 테이블 확인**:
```bash
$ docker exec myapp ip route
default via 172.18.0.1 dev eth0
172.18.0.0/16 dev eth0 scope link

$ docker exec myapp traceroute google.com
```

**6. iptables 규칙 검사**:
```bash
# Docker가 생성한 NAT 규칙
$ sudo iptables -t nat -L -n -v | grep DOCKER
Chain DOCKER (2 references)
 pkts bytes target     prot opt in     out     source       destination
    0     0 RETURN     all  --  docker0 *       0.0.0.0/0    0.0.0.0/0
```

**7. 네트워크 성능 측정**:
```bash
# iperf3 서버 실행
$ docker run -d --name iperf-server --network mynet \
  networkstatic/iperf3 -s

# iperf3 클라이언트로 대역폭 측정
$ docker run --rm --network mynet \
  networkstatic/iperf3 -c iperf-server
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-10.00  sec  10.8 GBytes  9.28 Gbits/sec
```

**8. 네트워크 격리 확인**:
```bash
# 컨테이너가 속한 네트워크 확인
$ docker inspect myapp --format='{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}'
myapp_backend

# 네트워크의 모든 컨테이너 조회
$ docker network inspect myapp_backend \
  --format='{{range .Containers}}{{.Name}} {{end}}'
```

**일반적인 문제와 해결책**:

| 증상 | 원인 | 해결 |
|------|------|------|
| DNS 해석 실패 | 다른 네트워크 또는 기본 bridge 사용 | 커스텀 네트워크로 이동 |
| 포트 접근 실패 | 방화벽 규칙 | `iptables -L DOCKER-USER` 확인 |
| 느린 연결 | MTU 미스매치 | `--opt com.docker.network.driver.mtu` 조정 |
| 간헐적 연결 끊김 | DNS 캐시 | TTL 조정 또는 VIP 모드 사용 |

### 실무 적용
프로덕션에서는 netshoot 컨테이너를 문제 컨테이너와 같은 네트워크에 연결하여 live 디버깅한다. Kubernetes에서는 `kubectl debug` 명령어가 비슷한 기능을 제공한다. 패킷 캡처는 성능 문제나 보안 감사 시 유용하다.
