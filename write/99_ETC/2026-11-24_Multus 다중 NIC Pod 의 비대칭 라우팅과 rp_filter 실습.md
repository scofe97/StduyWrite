---
title: Multus 다중 NIC Pod 의 비대칭 라우팅과 rp_filter 실습
tags: [kubernetes, multus, cni, linux, networking, routing, pbr, rp_filter, lab]
status: draft
related:
  - ./README.md
  - ./2026-11-24_쿠버네티스 CNI 깊게 공부하는 순서.md
  - ../08_cloud/book/networking-and-kubernetes/02-02.커널이 패킷을 판정하는 층 — Netfilter·Conntrack·라우팅.md
  - ../08_cloud/book/networking-and-kubernetes/04-02.CNI와 kube-proxy — Pod 네트워크의 배선공과 로드밸런서.md
  - ../02_os/book/learning-modern-linux/07-01.결국은 선과 공기를 타고 다니는 비트다.md
  - ../01_language/docs/go/net/02-01.Dial·Dialer.md
allow:
  - 10.244.0.1     # 실습용 예제 게이트웨이 주소, 실재 주소 아님
  - 10.244.0.11    # 실습용 예제 Pod 주소, 실재 주소 아님
  - 10.81.0.0/24   # 실습용 예제 대역, 실재 대역 아님
  - 10.81.0.10     # 실습용 예제 보조 NIC 주소, 실재 주소 아님
  - 10.81.0.11     # 실습용 예제 보조 NIC 주소, 실재 주소 아님
  - 10.81.0.50     # 실습용 예제 IPAM 종료 주소, 실재 주소 아님
updated: 2026-11-24
---

# Multus 다중 NIC Pod 의 비대칭 라우팅과 rp_filter 실습

---

> 다중 NIC 를 가진 Pod 에서 요청은 보조 NIC(`net1`)로 들어오고 응답은 기본 NIC(`eth0`)로 나가는 비대칭 라우팅을 재현하고, `rp_filter` 와 `ip rule` 의 동작을 단계별로 점검하는 실습 초안입니다.

이 문서는 외부 AI 가 작성한 실습 초안을 옮긴 기록입니다. Kubernetes 실습은 아직 한 번도 실행하지 않았습니다. 본문에 실린 출력과 로그 블록은 모두 원문이 적은 예상 출력입니다. 커널 동작 일부만 Linux VM 의 네트워크 네임스페이스에서 따로 재현해 4절에 판정을 적었습니다. [쿠버네티스 CNI 깊게 공부하는 순서](./2026-11-24_%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20CNI%20%EA%B9%8A%EA%B2%8C%20%EA%B3%B5%EB%B6%80%ED%95%98%EB%8A%94%20%EC%88%9C%EC%84%9C.md#8-cni-선택과-다중-인터페이스) 8단계의 Multus 다중 NIC 주제에 이어지는 초안으로, Kubernetes 클러스터에서의 실행 검증이 남아 있습니다.

## 1. 실습 목표와 확인 흐름

> Pod 에 NIC 가 둘 있을 때 요청과 응답이 서로 다른 인터페이스를 타면 `rp_filter` 설정에 따라 연결이 차단될 수 있으며, 정책 라우팅으로 테이블 선택을 분리할 수 있습니다.

Multus 로 보조 인터페이스 `net1` 을 붙인 Pod 에서는 출발지 IP 선택에 따라 경로가 엇갈립니다. 클라이언트 출발지를 기본 인터페이스 `eth0` 으로 고정하면 비대칭 라우팅(Asymmetric Routing)이 일어납니다. 비대칭 라우팅은 요청 패킷과 응답 패킷이 서로 다른 인터페이스나 경로로 이동하는 현상입니다. 이 실습은 연결 차단부터 `rp_filter` 완화, `ip rule` 기반 테이블 분리까지 순서대로 점검합니다.

| 개념 | 확인 내용 |
| --- | --- |
| Routing Table | 목적지 주소에 따라 출력 인터페이스를 결정하는 방식 |
| `ip rule` | 출발지 IP 같은 조건으로 조회할 Routing Table 을 고르는 규칙 |
| Policy-Based Routing | 정책 조건에 따라 기본 테이블 외의 경로를 선택하는 라우팅 |
| Asymmetric Routing | 요청과 응답이 서로 다른 인터페이스를 통과하는 비대칭 경로 |
| `rp_filter` | Reverse Path Filtering 을 통한 출발지 IP 역방향 검증 |
| Strict / Loose Mode | 역방향 경로의 인터페이스 일치 요구 여부에 따른 판정 차이 |

실습은 아래 여섯 단계로 진행합니다.

1. 클라이언트의 기본 NIC(`eth0`) IP 를 TCP 소켓의 출발지 IP 로 지정합니다.
2. 서버의 보조 NIC(`net1`) IP 로 TCP 연결을 시도합니다.
3. 요청은 `net1` 로 들어오고 응답은 `eth0` 으로 나가는 비대칭 경로를 만듭니다.
4. 서버의 `rp_filter=1` 설정에서 TCP 연결이 실패하는 장면을 관측합니다.
5. 서버의 `rp_filter=2` 로 바꾼 뒤 연결이 성공하는지 점검합니다.
6. `ip rule` 과 별도 Routing Table(`table 100`)을 적용해 테이블 선택을 확인합니다.



## 2. 일반 라우팅과 정책 라우팅

> 리눅스는 기본으로 목적지 IP 만 보고 경로를 고르지만, 출발지 IP 에 따라 다른 인터페이스를 쓰려면 `ip rule` 로 별도 라우팅 테이블을 먼저 조회해야 합니다.

목적지 IP 만 보고 경로를 고르는 일반 라우팅으로는 요청이 들어온 NIC 로 응답을 돌려보내기 어렵습니다. 다중 NIC 환경에서 정책 라우팅(PBR, Policy-Based Routing)과 `table 100` 분리를 쓰는 배경은 [복수 NIC 환경의 라우팅과 정책 라우팅](../02_os/book/learning-modern-linux/07-01.결국은%20선과%20공기를%20타고%20다니는%20비트다.md#복수-nic-환경의-라우팅과-정책-라우팅)에 정리돼 있습니다.

### 일반 라우팅의 목적지 기반 조회

리눅스는 보통 패킷의 목적지 IP 를 기준으로 기본 라우팅 테이블(`main`)을 조회합니다. 아래는 Pod 내부의 기본 라우팅 테이블을 조회하는 명령입니다.

```bash
# 현재 네임스페이스의 기본 라우팅 테이블을 출력합니다
ip route
```

아래 블록은 원문이 가정한 라우팅 테이블 예제입니다.

```bash
# 예제 라우팅 테이블 (미실행 초안)
default via 10.244.0.1 dev eth0
10.81.0.0/24 dev net1
```

목적지가 `10.81.0.10` 이면 커널은 기본 경로보다 접두사가 긴 `10.81.0.0/24` 경로를 선택합니다. 아래 명령으로 특정 목적지에 대해 커널이 고른 인터페이스와 출발지 주소를 미리 봅니다.

```bash
# 특정 목적지 주소로 가는 실제 라우팅 결정을 조회합니다
ip route get 10.81.0.10
```

아래는 위 예제 테이블을 기준으로 원문이 적은 예상 출력입니다.

```bash
# 예상 출력 (미실행 초안)
10.81.0.10 dev net1 src 10.81.0.11
```

### 정책 기반 라우팅과 조회 순서

금융망 요청은 금융망 NIC 로, 관리망 요청은 관리망 NIC 로 돌려보내야 할 때가 있습니다. 특정 출발지 IP 를 쓰는 트래픽만 전용 라우팅 테이블을 타게 분리할 때도 `ip rule` 을 사용합니다. 정책 라우팅이 켜져 있을 때 커널은 다음 순서로 출력 인터페이스를 정합니다.

1. 패킷의 출발지 IP 와 목적지 IP 등 메타데이터를 확인합니다.
2. `ip rule` 목록을 우선순위 번호가 작은 규칙부터 읽어 조회할 라우팅 테이블을 결정합니다.
3. 조건에 맞으면 전용 테이블(예: 보조 NIC 용 `Table 100`)을, 맞지 않으면 `main` 테이블을 조회합니다.
4. 선택된 테이블의 경로에 따라 출력 인터페이스를 확정합니다.

`ip rule` 은 출발지 IP 외에도 목적지 IP, 수신 인터페이스(`iif`), 방화벽 마크(`fwmark`)를 조건으로 씁니다. 아래 세 명령 틀은 정책 라우팅 상태를 조회할 때 사용합니다.

```bash
# 정책 규칙 목록, 100번 테이블 경로, 출발지·목적지 기준 경로 조회 명령 틀입니다
ip rule show
ip route show table 100
ip route get <DESTINATION> from <SOURCE>
```



## 3. 실습 환경과 전제

> 이 실습은 Multus·Whereabouts·bridge CNI 가 설치된 로컬 Kubernetes 환경에서 두 Pod 를 같은 워커 노드에 배치한다는 전제로 구성됐습니다.

운영 클러스터나 외부 네트워크는 쓰지 않고 로컬 Kubernetes 환경만 사용합니다. 두 Pod(`pbr-client`, `pbr-server`)는 모두 같은 워커 노드에 뜹니다. 각 Pod 는 기본 CNI 의 `eth0` 과 Multus 가 `br-pbr-lab` 브리지로 연결한 `net1` 을 가집니다.

클라이언트가 출발지 주소를 `eth0` IP 로 지정해 서버 `net1` IP 로 요청하면 경로가 엇갈립니다. 요청과 응답이 지나는 주소와 인터페이스는 아래와 같습니다.

| 방향 | 출발지 주소 | 목적지 주소 | 나가는 NIC | 들어오는 NIC |
| --- | --- | --- | --- | --- |
| 요청 | Client `eth0` IP | Server `net1` IP | Client `net1` | Server `net1` |
| 응답 | Server `net1` IP | Client `eth0` IP | Server `eth0` | Client `eth0` |



## 4. 실행 전에 확인할 것

> 이 문서를 옮기며 세운 다섯 가설을 1차 자료와 작은 재현으로 판정했습니다. 어긋난 곳은 실습 D~G 의 해당 단계에도 4절 번호로 짚어 뒀습니다.

Kubernetes 실습은 실행하지 않았습니다. 커널 동작만 Linux VM(커널 7.2.12)에서 네트워크 네임스페이스 둘과 veth 두 쌍으로 따로 재현했습니다. 이 환경에는 CNI·kube-proxy·브리지가 없어서 3·4·6·7번의 커널 동작은 판정하지만, 기본 CNI 와 노드 conntrack 이 얽힌 2번은 판정하지 못합니다. 판정은 자료로 확인됨, netns 재현으로 확인됨, 틀림, 확인하지 못함 중 하나로 적습니다. 6·7번은 원문에 없던 확인입니다.

1. 권한: 원문은 `NET_ADMIN`·`NET_RAW` 만 준 `debug` 컨테이너에서 `sysctl -w` 로 `rp_filter` 를 바꿉니다(실습 E·F). 판정은 자료로 확인됨(기본 스펙 기준)이고, 이 방식은 실패할 가능성이 큽니다. containerd 의 기본 OCI 스펙이 `/proc/sys` 를 읽기 전용 경로에 넣기 때문입니다.[^containerd] Pod 의 `securityContext.sysctls` 로 바꾸려 해도 안전 목록에 `rp_filter` 는 없습니다. 안전하지 않은 sysctl 은 노드마다 kubelet 의 `--allowed-unsafe-sysctls` 로 허용해야 합니다.[^ksysctl] 공식 문서가 뒷받침하는 대안은 NAD 에 `tuning` 플러그인을 이어 붙여 CNI 가 Pod 네임스페이스에서 `net.ipv4.conf.IFNAME.rp_filter` 를 쓰게 하는 것입니다.[^tuning] 실제로 쓰기가 막히는지는 클러스터에서 확인하지 못했습니다.
2. 응답 경로: 원문은 서버 `net1` 을 느슨(2)으로 바꾸면 연결이 성공한다고만 적습니다(실습 F). 이 문서의 의심은 다릅니다. 응답(SYN-ACK)이 서버 `net1` 주소를 출발지로 단 채 서버 `eth0` 으로 나가므로 기본 CNI 의 출발지 검사나 conntrack 판정에 걸릴 수 있다는 것입니다. 판정은 확인하지 못함입니다. kube-proxy iptables 모드는 `nf_conntrack_tcp_be_liberal` 이 꺼져 있으면 INVALID 상태 패킷을 버리는 규칙을 넣습니다.[^kproxy] 한편 `nf_conntrack_tcp_loose` 를 0 으로 끄면 이미 맺어진 연결을 중간부터 집어 올리지 않으며 기본값은 켜짐입니다.[^nfct] 그러나 SYN 없이 온 SYN-ACK 가 어느 쪽으로 판정되는지와 Calico·Cilium 의 출발지 검사는 자료에서 찾지 못했습니다. 실습 F 가 실패하면 클라이언트 `eth0` 에 SYN-ACK 가 도착하는지 `tcpdump` 로 먼저 봅니다.
3. 클라이언트의 rp_filter: 원문은 서버의 `rp_filter` 만 바꿉니다. 판정은 netns 재현으로 확인됨입니다. 서버를 `rp_filter=2` 로 둬도 클라이언트 `eth0` 이 엄격(1)이면 SYN-ACK 가 클라이언트에서 버려져 연결이 실패했고 클라이언트의 `TcpExtIPReversePathFilter` 가 0 에서 4 로 늘었습니다. 클라이언트 `eth0` 을 2 로 바꾸면 성공했습니다. 새 네임스페이스에서는 `all`·`default`·`eth0`·`net1` 이 모두 0 이었지만 Pod 의 초기값은 환경마다 다르니, 실습 F 전에 클라이언트의 `all` 과 `eth0` 값을 읽어 둡니다. 서버에서 `all=1, net1=0` 은 엄격으로, `all=2, net1=1` 은 느슨으로 동작해 큰 값을 쓴다는 규칙도 재현했고 값 0·1·2 의 뜻은 커널 문서와 같습니다.[^ip-sysctl]
4. via: 원문은 서버의 `ip route get "$CLIENT_ETH0"` 가 `via 10.244.0.1 dev eth0` 로 나온다고 적습니다(실습 D 3단계). 판정은 netns 재현으로 확인됨(조건부)입니다. 서버 `eth0` 이 클라이언트와 다른 서브넷이고 게이트웨이가 있으면 `via <게이트웨이> dev eth0 src <서버 eth0 주소> uid 0` 으로 나왔습니다. 같은 서브넷이면 `via` 없이 `dev eth0 src <서버 eth0 주소> uid 0` 이었습니다. 두 경우 모두 응답은 `eth0` 으로 나가 비대칭 구조는 같지만, 예상 출력에 없는 `src` 와 `uid 0` 이 붙습니다.
5. 이미지와 CNI 버전: 원문은 `golang:1.25-alpine`, `nicolaka/netshoot:v0.13`, NAD `cniVersion: "0.3.0"` 을 씁니다. 판정은 자료로 확인됨입니다. 두 태그는 Docker Hub 에 공개돼 있습니다(2026-11-24 조회).[^hub] bridge 플러그인 v1.10.0 이 쓰는 CNI 라이브러리 v1.3.1 의 지원 버전 목록에는 0.3.0 이 들어 있습니다.[^cniver] Multus v4.3.2 의 사용 문서 예제도 0.3.0 을 씁니다.[^multus] Whereabouts 의 `range`·`range_start`·`range_end` 와 Multus 주석 키 `k8s.v1.cni.cncf.io/networks` 도 각 저장소 문서에 있습니다.[^wb] 설치된 Multus·플러그인 버전이 다르면 실행 때 다시 확인합니다.
6. ARP 단계의 차단: 원문은 엄격 모드에서 `tcpdump` 에 SYN 이 관측될 수 있다고 적습니다(실습 E 2단계). 판정은 netns 재현으로 확인됨(조건부)입니다. 서버의 ARP 캐시가 빈 첫 연결에서는 SYN 이 찍히지 않았습니다. 클라이언트가 `net1` 로 보내는 ARP 요청의 보내는 쪽 주소가 `eth0` 주소(`10.244.0.11`)여서 엄격인 서버 `net1` 이 요청을 답 없이 버렸습니다. 클라이언트의 이웃 항목은 FAILED 가 됐고 `TcpExtIPReversePathFilter` 는 늘지 않았습니다. `net1` 만 2 로 바꾸자 같은 조건에서 연결이 성공했습니다. 커널의 ARP 요청 처리가 `ip_route_input_noref` 로 보내는 쪽 주소를 따지는 자리와 맞습니다.[^arp] 캐시가 채워진 뒤 엄격으로 바꾸면 SYN 이 찍히고 카운터가 0 에서 3 으로 늘었습니다. 실습 E 에서는 느슨 모드로 한 번 연결해 캐시를 채운 뒤 엄격으로 바꾸거나, `tcpdump` 필터에 `arp` 를 더해 요청이 오는지 봅니다.
7. 경로 조회의 출력 모양: 원문은 `ip route get "$SERVER_NET1" from "$CLIENT_ETH0"` 의 출력을 `10.81.0.10 dev net1 src 10.244.0.11` 로 적습니다(실습 D 2단계·G 3단계). 판정은 틀림(출력 모양)입니다. 재현에서는 `10.81.0.10 from 10.244.0.11 dev net1 uid 0` 이었고 `src` 는 나오지 않았습니다. `ip rule` 과 `table 100` 을 넣은 뒤에는 `10.81.0.10 from 10.244.0.11 dev net1 table 100 uid 0` 으로 `table 100` 이 붙어, 규칙이 테이블을 골랐는지 이 줄에서 읽을 수 있습니다. `from` 은 조회할 출발지 주소를 주는 인자입니다.[^iproute] 실습 G 의 `ip rule show` 예상 출력 둘은 재현 출력과 같았고 기본 규칙 셋과 조건 목록은 매뉴얼과 같습니다.[^iprule]



## 5. 실습 A — Multus 네트워크 구성

> `pbr-lab` 네임스페이스를 만들고 `br-pbr-lab` 브리지와 `10.81.0.0/24` 대역을 쓰는 `NetworkAttachmentDefinition` 을 배포하는 단계입니다.

먼저 실습용 네임스페이스와 워커 노드 변수를 준비합니다. 아래 블록은 클러스터에서 실행할 명령 목록입니다.

```bash
# 실습 전용 네임스페이스를 생성합니다
kubectl create namespace pbr-lab

# 클러스터의 워커 노드 목록과 이름을 확인합니다
kubectl get nodes -o wide

# 두 Pod 를 고정 배치할 워커 노드 이름을 변수에 담습니다
export NODE=<실습용-worker-node>
```

다음으로 보조 인터페이스 `net1` 이 사용할 `nad.yaml` 매니페스트를 작성합니다. 대역 `10.81.0.0/24` 가 기본 CNI 의 Pod CIDR 과 겹치지 않는지 먼저 확인해야 합니다.

```yaml
# nad.yaml — bridge CNI 와 whereabouts IPAM 을 묶은 보조 네트워크 정의입니다
apiVersion: k8s.cni.cncf.io/v1
kind: NetworkAttachmentDefinition
metadata:
  name: pbr-secondary
  namespace: pbr-lab
spec:
  config: |
    {
      "cniVersion": "0.3.0",
      "name": "pbr-secondary",
      "type": "bridge",
      "bridge": "br-pbr-lab",
      "ipam": {
        "type": "whereabouts",
        "range": "10.81.0.0/24",
        "range_start": "10.81.0.10",
        "range_end": "10.81.0.50"
      }
    }
```

작성한 `nad.yaml` 을 클러스터에 적용합니다.

```bash
# 보조 네트워크 정의를 클러스터에 생성합니다
kubectl apply -f nad.yaml
```



## 6. 실습 B — Go TCP 프로그램

> 서버는 `net1` 주소에서 TCP 9000번 포트를 열고, 클라이언트는 `SOURCE_IP` 환경변수로 지정한 `eth0` 주소로 접속하도록 Go 프로그램을 작성합니다.

아래 `main.go` 는 원문이 완전한 예제 소스라고 한 코드입니다. Go 1.25 에서 컴파일과 클라이언트 모드 실행은 확인했고, 서버 모드는 `net1` 이 있는 Pod 가 없어 확인하지 못했습니다. 서버 모드는 `net1` IPv4 주소를 찾아 수신 대기합니다. 클라이언트 모드는 `SOURCE_IP` 와 `TARGET_IP` 를 읽어 TCP 연결을 맺습니다.

```go
// main.go — net1 에서 대기하는 TCP 서버와 출발지 IP 를 고정하는 TCP 클라이언트입니다
package main

import (
    "fmt"
    "log"
    "net"
    "os"
    "time"
)

func interfaceIPv4(name string) (net.IP, error) {
    iface, err := net.InterfaceByName(name)
    if err != nil {
        return nil, err
    }

    addrs, err := iface.Addrs()
    if err != nil {
        return nil, err
    }

    for _, addr := range addrs {
        var ip net.IP

        switch v := addr.(type) {
        case *net.IPNet:
            ip = v.IP
        case *net.IPAddr:
            ip = v.IP
        }

        if ip4 := ip.To4(); ip4 != nil {
            return ip4, nil
        }
    }

    return nil, fmt.Errorf("IPv4 not found: %s", name)
}

func runServer() error {
    ip, err := interfaceIPv4("net1")
    if err != nil {
        return err
    }

    address := net.JoinHostPort(ip.String(), "9000")

    listener, err := net.Listen("tcp", address)
    if err != nil {
        return err
    }
    defer listener.Close()

    log.Printf("listening: %s", address)

    for {
        conn, err := listener.Accept()
        if err != nil {
            return err
        }

        log.Printf(
            "accepted: local=%s remote=%s",
            conn.LocalAddr(),
            conn.RemoteAddr(),
        )

        conn.Close()
    }
}

func runClient() error {
    sourceIP := net.ParseIP(os.Getenv("SOURCE_IP"))
    targetIP := os.Getenv("TARGET_IP")

    if sourceIP == nil || sourceIP.To4() == nil {
        return fmt.Errorf("valid IPv4 SOURCE_IP required")
    }

    if targetIP == "" {
        return fmt.Errorf("TARGET_IP required")
    }

    dialer := net.Dialer{
        Timeout: 5 * time.Second,
        LocalAddr: &net.TCPAddr{
            IP: sourceIP,
        },
    }

    target := net.JoinHostPort(targetIP, "9000")

    conn, err := dialer.Dial("tcp", target)
    if err != nil {
        return fmt.Errorf("dial failed: %w", err)
    }
    defer conn.Close()

    log.Printf(
        "connected: local=%s remote=%s",
        conn.LocalAddr(),
        conn.RemoteAddr(),
    )

    return nil
}

func main() {
    if len(os.Args) != 2 {
        log.Fatal("usage: probe server|client")
    }

    var err error

    switch os.Args[1] {
    case "server":
        err = runServer()
    case "client":
        err = runClient()
    default:
        err = fmt.Errorf("unknown command")
    }

    if err != nil {
        log.Fatal(err)
    }
}
```

아래 발췌 블록은 `Dialer.LocalAddr` 에 `sourceIP` 를 넘겨 소켓 출발지 IP 를 고정하는 자리입니다. 이 필드의 계약은 [Dial·Dialer](../01_language/docs/go/net/02-01.Dial·Dialer.md#공식-계약-dialer-구조체-필드와-dialcontext)에 정리돼 있습니다.

```go
// main.go 일부 — Dialer.LocalAddr 에 출발지 IP 를 바인딩합니다
LocalAddr: &net.TCPAddr{
    IP: sourceIP,
}
```

따라서 `SOURCE_IP` 에 클라이언트 `eth0` IP 를 넣고 `TARGET_IP` 에 서버 `net1` IP 를 지정합니다. 그러면 출발지가 `eth0` 이고 목적지가 `net1` 인 연결이 만들어집니다.



## 7. 실습 C — Pod 배포와 주소 추출

> `main.go` 를 ConfigMap 으로 올리고 `pbr-server` 와 `pbr-client` 두 Pod 를 같은 노드에 띄운 뒤 각 인터페이스의 IPv4 주소를 셸 변수에 담습니다.

먼저 작성한 `main.go` 파일을 ConfigMap 으로 생성합니다. 아래는 클러스터에 ConfigMap 을 등록하는 명령입니다.

```bash
# main.go 소스를 pbr-app ConfigMap 으로 등록합니다
kubectl create configmap pbr-app \
  --from-file=main.go=./main.go \
  -n pbr-lab
```

두 Pod 에는 Go 바이너리를 실행하는 `app` 컨테이너와 진단용 `debug` 컨테이너가 들어갑니다. `debug` 컨테이너에는 `NET_ADMIN` 과 `NET_RAW` 권한을 줍니다.

```yaml
# pods.yaml — pbr-secondary 네트워크가 연결된 server 와 client Pod 정의입니다
apiVersion: v1
kind: Pod
metadata:
  name: pbr-server
  namespace: pbr-lab
  annotations:
    k8s.v1.cni.cncf.io/networks: pbr-secondary
spec:
  nodeName: REPLACE_NODE
  containers:
    - name: app
      image: golang:1.25-alpine
      command: ["sh", "-c"]
      args:
        - go build -o /tmp/probe /lab/main.go &&
          exec /tmp/probe server
      volumeMounts:
        - name: source
          mountPath: /lab
    - name: debug
      image: nicolaka/netshoot:v0.13
      command: ["sh", "-c", "sleep 36000"]
      securityContext:
        capabilities:
          add: ["NET_ADMIN", "NET_RAW"]
      volumeMounts:
        - name: source
          mountPath: /lab
  volumes:
    - name: source
      configMap:
        name: pbr-app
---
apiVersion: v1
kind: Pod
metadata:
  name: pbr-client
  namespace: pbr-lab
  annotations:
    k8s.v1.cni.cncf.io/networks: pbr-secondary
spec:
  nodeName: REPLACE_NODE
  containers:
    - name: app
      image: golang:1.25-alpine
      command: ["sh", "-c"]
      args:
        - go build -o /tmp/probe /lab/main.go &&
          sleep 36000
      volumeMounts:
        - name: source
          mountPath: /lab
    - name: debug
      image: nicolaka/netshoot:v0.13
      command: ["sh", "-c", "sleep 36000"]
      securityContext:
        capabilities:
          add: ["NET_ADMIN", "NET_RAW"]
      volumeMounts:
        - name: source
          mountPath: /lab
  volumes:
    - name: source
      configMap:
        name: pbr-app
```

`REPLACE_NODE` 자리표시자를 `$NODE` 값으로 치환해 배포한 뒤 Pod 상태를 조회합니다.

```bash
# 노드 이름을 치환해 두 Pod 를 배포합니다
sed "s/REPLACE_NODE/${NODE}/g" pods.yaml | kubectl apply -f -

# Pod 배치 노드와 IP, 실행 상태를 확인합니다
kubectl get pods -n pbr-lab -o wide
```

두 Pod 가 올라왔으면 `debug` 컨테이너에서 `eth0` 과 `net1` 의 IPv4 주소를 뽑아 환경변수에 저장합니다.

```bash
# 클라이언트의 기본 NIC(eth0) IPv4 주소를 추출합니다
export CLIENT_ETH0=$(
  kubectl exec pbr-client -n pbr-lab -c debug -- \
    ip -4 -o addr show dev eth0 |
    awk '{split($4, a, "/"); print a[1]}'
)

# 클라이언트의 보조 NIC(net1) IPv4 주소를 추출합니다
export CLIENT_NET1=$(
  kubectl exec pbr-client -n pbr-lab -c debug -- \
    ip -4 -o addr show dev net1 |
    awk '{split($4, a, "/"); print a[1]}'
)

# 서버의 기본 NIC(eth0) IPv4 주소를 추출합니다
export SERVER_ETH0=$(
  kubectl exec pbr-server -n pbr-lab -c debug -- \
    ip -4 -o addr show dev eth0 |
    awk '{split($4, a, "/"); print a[1]}'
)

# 서버의 보조 NIC(net1) IPv4 주소를 추출합니다
export SERVER_NET1=$(
  kubectl exec pbr-server -n pbr-lab -c debug -- \
    ip -4 -o addr show dev net1 |
    awk '{split($4, a, "/"); print a[1]}'
)

# 추출한 네 주소를 터미널에 출력합니다
echo "CLIENT_ETH0=$CLIENT_ETH0"
echo "CLIENT_NET1=$CLIENT_NET1"
echo "SERVER_ETH0=$SERVER_ETH0"
echo "SERVER_NET1=$SERVER_NET1"
```



## 8. 실습 D — 비대칭 라우팅 재현

> 클라이언트와 서버에서 `ip route get` 을 조회해 요청은 `net1` 로 나가고 응답은 `eth0` 으로 돌아가는 비대칭 경로가 잡히는지 확인합니다.

### 1단계. 클라이언트의 라우팅 테이블 확인

먼저 `pbr-client` 의 `debug` 컨테이너에서 기본 라우팅 테이블을 조회합니다.

```bash
# 클라이언트 Pod 의 라우팅 테이블을 확인합니다
kubectl exec pbr-client -n pbr-lab -c debug -- ip route
```

아래는 원문이 적은 예상 출력 형태입니다. 실제 게이트웨이와 기본 CIDR 은 사용하는 CNI 환경에 따라 달라집니다.

```bash
# 예상 출력 (미실행 초안)
default via 10.244.0.1 dev eth0
10.81.0.0/24 dev net1
```

### 2단계. 출발지 IP 를 지정한 경로 조회

다음으로 출발지 IP 에 `$CLIENT_ETH0` 을 명시해 목적지 `$SERVER_NET1` 로 가는 경로를 커널에 묻습니다.

```bash
# 출발지가 CLIENT_ETH0 이고 목적지가 SERVER_NET1 인 경로를 조회합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip route get "$SERVER_NET1" from "$CLIENT_ETH0"
```

아래는 원문이 적은 예상 출력입니다. 재현에서는 `src` 자리에 `from 10.244.0.11` 이 찍히고 `uid 0` 이 붙었습니다(4절 7번). 출발지는 클라이언트 `eth0` 주소(`10.244.0.11`)지만 `dev` 는 `net1` 입니다.

```bash
# 예상 출력 (미실행 초안)
10.81.0.10 dev net1 src 10.244.0.11
```

### 3단계. 서버의 응답 경로 확인

이제 `pbr-server` 에서 클라이언트의 `eth0` 주소로 되돌아가는 경로를 조회합니다.

```bash
# 서버 Pod 에서 CLIENT_ETH0 으로 돌아가는 응답 경로를 조회합니다
kubectl exec pbr-server -n pbr-lab -c debug -- \
  ip route get "$CLIENT_ETH0"
```

아래는 원문이 적은 예상 출력입니다. 서버 `eth0` 의 서브넷에 따라 `via` 가 없을 수 있고 `src` 가 붙습니다(4절 4번). 요청은 `net1` 로 들어오고 응답은 `eth0` 으로 나가는 비대칭 구조가 만들어집니다.

```bash
# 예상 출력 (미실행 초안)
10.244.0.11 via 10.244.0.1 dev eth0
```



## 9. 실습 E — Strict 장애 주입

> 서버의 `net1` 에 엄격 모드(`rp_filter=1`)를 걸면 요청 SYN 이 `net1` 에 도착하더라도 역방향 경로(`eth0`)와 어긋나 커널이 패킷을 버립니다.

요청이 `net1` 로 들어와도 역방향 응답 경로가 `eth0` 이면 커널의 역방향 경로 검증(`rp_filter`)이 패킷을 버립니다. `rp_filter` 의 세 모드와 `all`·인터페이스 중 큰 값을 쓰는 규칙은 [심화 1 · Martian 검사와 rp_filter](../08_cloud/book/networking-and-kubernetes/02-02.커널이%20패킷을%20판정하는%20층%20—%20Netfilter·Conntrack·라우팅.md#심화-1--martian-검사와-rp_filter)에 정리돼 있습니다.

| 값 | 모드 | 동작 |
| ---: | --- | --- |
| 0 | Disabled | 출발지 역방향 경로를 검증하지 않음 |
| 1 | Strict | 들어온 인터페이스와 역방향 최적 경로의 인터페이스가 같아야 통과 |
| 2 | Loose | 역방향 경로가 어느 인터페이스로든 존재하면 통과 |

`rp_filter` 가 버린 패킷 수는 `nstat -az TcpExtIPReversePathFilter` 카운터로 봅니다. 카운터 해석은 [Calico 의 proxy_arp 와 rp_filter](../08_cloud/book/networking-and-kubernetes/04-02.CNI와%20kube-proxy%20—%20Pod%20네트워크의%20배선공과%20로드밸런서.md#calico-의-proxy_arp-와-rp_filter)에 나와 있습니다.

### 1단계. 서버의 기본 설정과 엄격 모드 적용

먼저 서버 Pod 의 현재 `all` 과 `net1` `rp_filter` 값을 조회합니다. 매개변수 조회·변경 문법은 [sysctl 참조 시트](../02_os/docs/cmd/sysinfo/sysctl.md)에 있습니다.

```bash
# 서버 Pod 의 현재 rp_filter 설정값을 조회합니다
kubectl exec pbr-server -n pbr-lab -c debug -- \
  sysctl net.ipv4.conf.all.rp_filter \
         net.ipv4.conf.net1.rp_filter
```

리눅스는 `conf/all` 과 `conf/<인터페이스>` 중 큰 값을 유효 설정으로 씁니다. 서버 네임스페이스 안에서 `all=0`, `net1=1` 로 맞춰 엄격 모드를 적용한 뒤 값을 다시 읽습니다. `debug` 컨테이너에서 `sysctl -w` 가 읽기 전용 파일 시스템으로 실패할 수 있습니다(4절 1번).

```bash
# all 을 0, net1 을 1 로 설정해 net1 에만 엄격 모드를 켭니다
kubectl exec pbr-server -n pbr-lab -c debug -- sh -c '
  sysctl -w net.ipv4.conf.all.rp_filter=0
  sysctl -w net.ipv4.conf.net1.rp_filter=1
'

# 변경한 rp_filter 값이 반영됐는지 확인합니다
kubectl exec pbr-server -n pbr-lab -c debug -- \
  sysctl net.ipv4.conf.all.rp_filter \
         net.ipv4.conf.net1.rp_filter
```

### 2단계. 패킷 캡처와 연결 시도

별도 터미널에서 서버 `net1` 의 9000번 포트를 캡처하면서 클라이언트 연결을 시도합니다.

```bash
# 별도 터미널에서 서버 net1 의 TCP 9000 트래픽을 캡처합니다
kubectl exec -it pbr-server -n pbr-lab -c debug -- \
  tcpdump -nn -i net1 'tcp port 9000'

# 클라이언트에서 eth0 주소를 출발지로 삼아 서버 net1 에 연결을 시도합니다
kubectl exec pbr-client -n pbr-lab -c app -- \
  env SOURCE_IP="$CLIENT_ETH0" \
      TARGET_IP="$SERVER_NET1" \
      /tmp/probe client
```

아래 두 블록은 엄격 모드(`rp_filter=1`)에서 원문이 적은 클라이언트 타임아웃과 `tcpdump` 예상 출력입니다. 서버의 ARP 캐시가 빈 첫 연결에서는 ARP 요청이 먼저 버려져 SYN 이 찍히지 않을 수 있습니다(4절 6번).

```bash
# 클라이언트 예상 출력 (미실행 초안)
dial failed: dial tcp 10.81.0.10:9000: i/o timeout
```

```bash
# tcpdump 예상 출력 (미실행 초안)
10.244.0.11.49152 > 10.81.0.10.9000: Flags [S]
```

`tcpdump` 에 SYN 이 찍혀도 서버 프로세스의 `Accept()` 는 호출되지 않습니다. 커널이 엄격 모드 판정으로 패킷을 버리는 흐름은 아래와 같습니다.

1. 출발지가 클라이언트 `eth0` IP 인 패킷이 서버 `net1` 인터페이스로 들어옵니다.
2. 커널은 출발지 IP 를 키로 라우팅 테이블을 거꾸로 조회합니다.
3. 서버 테이블에서 클라이언트 `eth0` 대역으로 돌아가는 경로는 `eth0` 입니다.
4. 들어온 인터페이스(`net1`)와 역방향 경로 인터페이스(`eth0`)가 달라 커널이 패킷을 드롭합니다.



## 10. 실습 F — Loose 모드 전환

> 서버 `net1` 을 느슨한 모드(`rp_filter=2`)로 바꾸면 역방향 경로가 다른 인터페이스(`eth0`)에 있더라도 존재 여부만 보고 패킷을 통과시킵니다.

서버 Pod 의 `net1` 설정을 `2` 로 바꾼 뒤 클라이언트에서 같은 명령으로 다시 연결합니다. 클라이언트 `eth0` 이 엄격이면 응답이 클라이언트에서 버려져 실패합니다(4절 3번). 응답이 노드에서 막히는지는 확인하지 못했습니다(4절 2번).

```bash
# 서버 net1 의 rp_filter 를 느슨한 모드(2)로 바꿉니다
kubectl exec pbr-server -n pbr-lab -c debug -- \
  sysctl -w net.ipv4.conf.net1.rp_filter=2

# 클라이언트에서 다시 서버 net1 로 연결을 시도합니다
kubectl exec pbr-client -n pbr-lab -c app -- \
  env SOURCE_IP="$CLIENT_ETH0" \
      TARGET_IP="$SERVER_NET1" \
      /tmp/probe client
```

아래는 느슨한 모드 변경 뒤 원문이 적은 클라이언트와 서버 로그의 예상 출력입니다.

```bash
# 클라이언트 예상 출력 (미실행 초안)
connected: local=10.244.0.11:xxxxx remote=10.81.0.10:9000
```

```bash
# 서버 앱 컨테이너 로그를 조회합니다
kubectl logs pbr-server -n pbr-lab -c app
```

```bash
# 서버 로그 예상 출력 (미실행 초안)
accepted: local=10.81.0.10:9000 remote=10.244.0.11:xxxxx
```

느슨한 모드에서는 출발지 IP 로 가는 역방향 경로가 어느 인터페이스로든 존재하면 패킷을 허용합니다. 다만 방화벽·NAT·라우팅 정책·NetworkPolicy 제약까지 해결하지는 못합니다.



## 11. 실습 G — ip rule 과 테이블

> 출발지 IP 를 조건으로 `ip rule` 을 추가하면 기본 `main` 테이블보다 먼저 전용 라우팅 테이블(`table 100`)을 조회하도록 경로 선택을 분리할 수 있습니다.

클라이언트 `main` 테이블에는 이미 `10.81.0.0/24 dev net1` 경로가 들어 있습니다. 이 단계에서는 출발지 IP 조건으로 `table 100` 을 고르도록 규칙을 세우고 해제합니다.

### 1단계. 기존 정책 규칙 확인

먼저 클라이언트 Pod 에서 기본 `ip rule` 목록을 조회합니다. 리눅스는 우선순위 숫자가 작은 규칙부터 순서대로 검사합니다.

```bash
# 클라이언트의 기본 ip rule 목록을 확인합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip rule show
```

아래는 기본 규칙 목록의 예상 출력입니다.

```bash
# 예상 출력 (미실행 초안)
0:      from all lookup local
32766:  from all lookup main
32767:  from all lookup default
```

### 2단계. 별도 라우팅 테이블과 규칙 추가

클라이언트 Pod 의 `table 100` 에 보조 대역 경로를 넣고 `table 100` 내용을 확인합니다.

```bash
# table 100 에 보조 네트워크 대역 경로를 추가합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip route add 10.81.0.0/24 dev net1 scope link table 100

# table 100 에 추가된 경로를 조회합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip route show table 100
```

아래는 `table 100` 조회의 예상 출력입니다.

```bash
# 예상 출력 (미실행 초안)
10.81.0.0/24 dev net1 scope link
```

이어서 우선순위 `100` 의 출발지 기반 규칙을 넣고 규칙 목록을 다시 확인합니다.

```bash
# CLIENT_ETH0 출발지 트래픽이 table 100 을 조회하도록 규칙을 추가합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip rule add priority 100 \
  from "${CLIENT_ETH0}/32" \
  table 100

# 우선순위 100번 규칙이 추가됐는지 확인합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip rule show
```

아래는 규칙 추가 뒤의 예상 출력입니다.

```bash
# 예상 출력 (미실행 초안)
0:      from all lookup local
100:    from 10.244.0.11 lookup 100
32766:  from all lookup main
32767:  from all lookup default
```

### 3단계. 경로 조회와 규칙 정리

규칙이 들어간 상태에서 다시 `ip route get` 으로 경로를 조회합니다.

```bash
# 규칙 추가 뒤 출발지·목적지 기준 경로 결정을 다시 확인합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip route get "$SERVER_NET1" from "$CLIENT_ETH0"
```

아래는 경로 재조회의 예상 출력입니다. 재현에서는 `table 100` 이 붙어 `10.81.0.10 from 10.244.0.11 dev net1 table 100 uid 0` 으로 나왔습니다(4절 7번).

```bash
# 예상 출력 (미실행 초안)
10.81.0.10 dev net1 src 10.244.0.11
```

이 실습에서는 `main` 테이블에도 `10.81.0.0/24 dev net1` 경로가 있어 출력 인터페이스 자체는 같습니다. 운영 환경에서 경로를 갈라 쓰려면 테이블마다 게이트웨이와 서브넷 경로를 따로 구성해야 합니다. 확인을 마쳤으면 추가한 100번 규칙과 테이블을 비웁니다.

```bash
# 추가했던 우선순위 100번 정책 규칙을 삭제합니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip rule del priority 100

# table 100 의 경로를 모두 비웁니다
kubectl exec pbr-client -n pbr-lab -c debug -- \
  ip route flush table 100
```



## 12. 관측 명령 정리

> `tcpdump` 로 NIC 에 패킷이 찍히더라도 커널 라우팅·`rp_filter`·방화벽을 통과하지 못하면 소켓 `Accept()` 로 넘어가지 않으므로, 각 계층 명령을 나눠 봐야 합니다.

장애 시 NIC 도착 여부와 소켓 수신 여부를 함께 보지 않으면 원인을 잘못 짚습니다. 패킷이 인터페이스에 도착한 것과 TCP 소켓이 수신한 것은 별개입니다. 소켓 수신 대기 상태는 [ss 참조 시트](../02_os/docs/cmd/net/ss.md)의 명령으로 함께 봅니다. 아래 표는 실습 단계마다 쓰는 관측 명령과 확인 대상을 짝지은 목록입니다.

| 관측 명령 | 확인 대상 |
| --- | --- |
| `ip route` | 기본 라우팅 테이블(`main`) 경로 |
| `ip rule show` | 출발지·우선순위별 라우팅 테이블 선택 규칙 |
| `ip route show table 100` | 분리된 전용 라우팅 테이블 경로 |
| `ip route get` | 주어진 조건으로 커널이 고른 최종 출력 경로 |
| `sysctl ...rp_filter` | `all` 과 `net1` 의 `rp_filter` 설정값 |
| `tcpdump -i net1` | 보조 NIC `net1` 도착 패킷 |
| `ss -ltn` | 서버 TCP 소켓의 LISTEN 상태 |



## 13. 정리 질문

> 실습을 마친 뒤 아래 다섯 질문을 패킷의 이동 순서와 커널 판정 규칙으로 연결해 답해 봅니다.

1. `ip route` 와 `ip rule` 은 각각 어떤 역할을 담당하며, 커널은 둘을 어떤 순서로 조회합니까?
2. 출발지 IP 가 `eth0` 주소인데도 실제 패킷이 `net1` 인터페이스로 나가는 것이 가능한 이유는 무엇입니까?
3. 엄격 모드 `rp_filter=1` 은 왜 요청 패킷을 차단했고, 느슨한 모드 `rp_filter=2` 에서는 왜 통신이 성공합니까?
4. `ip route get <destination> from <source>` 와 `ip route get <destination>` 은 무엇이 다릅니까?
5. 금융망과 관리망을 별도 NIC 로 구성한 서버에서 비대칭 라우팅이 발생할 때, 무조건 `rp_filter=0` 으로 끄는 것이 올바른 해결책입니까?



## 14. 실습 정리와 다음 단계

> 실습에서 바꾼 설정은 Pod 네트워크 네임스페이스 안에만 남으므로 네임스페이스를 지우면 함께 제거됩니다.

실습이 끝나면 `pbr-lab` 네임스페이스를 삭제합니다. 삭제 뒤 실습용 NAD 의 Whereabouts IP 할당도 회수되는지 확인하고, 공유 IPPool 이나 다른 실습 리소스는 건드리지 않습니다.

```bash
# 실습에 쓴 네임스페이스와 내부 Pod·ConfigMap·NAD 를 모두 삭제합니다
kubectl delete namespace pbr-lab
```

Multus 와 CNI 플러그인이 `ADD`·`DEL` 호출로 네임스페이스를 배선하는 규약은 [쿠버네티스 CNI 깊게 공부하는 순서](./2026-11-24_%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20CNI%20%EA%B9%8A%EA%B2%8C%20%EA%B3%B5%EB%B6%80%ED%95%98%EB%8A%94%20%EC%88%9C%EC%84%9C.md#3-cni-명세와-참조-플러그인) 3단계로 이어집니다.



## 참고 자료

- [심화 1 · Martian 검사와 rp_filter](../08_cloud/book/networking-and-kubernetes/02-02.커널이%20패킷을%20판정하는%20층%20—%20Netfilter·Conntrack·라우팅.md#심화-1--martian-검사와-rp_filter) — `rp_filter` 값 0·1·2 와 `all`·인터페이스 최댓값 규칙
- [Calico 의 proxy_arp 와 rp_filter](../08_cloud/book/networking-and-kubernetes/04-02.CNI와%20kube-proxy%20—%20Pod%20네트워크의%20배선공과%20로드밸런서.md#calico-의-proxy_arp-와-rp_filter) — `nstat -az TcpExtIPReversePathFilter` 드롭 카운터 진단
- [복수 NIC 환경의 라우팅과 정책 라우팅](../02_os/book/learning-modern-linux/07-01.결국은%20선과%20공기를%20타고%20다니는%20비트다.md#복수-nic-환경의-라우팅과-정책-라우팅) — `ip rule` 과 `table 100` 기반 정책 라우팅 원리
- [Dial·Dialer](../01_language/docs/go/net/02-01.Dial·Dialer.md#공식-계약-dialer-구조체-필드와-dialcontext) — `Dialer.LocalAddr` 소켓 로컬 송신 주소 바인딩 계약
- [쿠버네티스 CNI 깊게 공부하는 순서](./2026-11-24_%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20CNI%20%EA%B9%8A%EA%B2%8C%20%EA%B3%B5%EB%B6%80%ED%95%98%EB%8A%94%20%EC%88%9C%EC%84%9C.md#8-cni-선택과-다중-인터페이스) — CNI 학습 순서 중 8단계 Multus 다중 NIC 및 3단계 CNI 명세 위치
- [ip-rule(8)](https://man7.org/linux/man-pages/man8/ip-rule.8.html) — 리눅스 정책 라우팅 규칙 매뉴얼
- [ip-route(8)](https://man7.org/linux/man-pages/man8/ip-route.8.html) — 리눅스 라우팅 테이블 관리 매뉴얼
- [Linux IP Sysctl Documentation](https://docs.kernel.org/networking/ip-sysctl.html) — `rp_filter` 와 커널 IPv4 sysctl 공식 명세
- [CNI Specification](https://www.cni.dev/docs/) — Container Network Interface 공식 문서

[^containerd]: 기본 OCI 스펙의 읽기 전용 경로는 containerd v2.1.0 의 [pkg/oci/spec.go](https://github.com/containerd/containerd/blob/v2.1.0/pkg/oci/spec.go) 에서 `ReadonlyPaths` 목록에 "/proc/sys" 가 들어 있는 것으로 확인했습니다. 쿠버네티스가 이 스펙으로 띄운 비특권 컨테이너에서 쓰기가 실제로 막히는지는 실행해 보지 않았습니다.
[^ksysctl]: [Using sysctls in a Kubernetes Cluster](https://kubernetes.io/docs/tasks/administer-cluster/sysctl-cluster/) (2026-11-24 조회, `kubernetes/website` 의 release-1.34 원문과 대조). 안전하지 않은 sysctl 은 "are enabled on a node-by-node basis with a flag of the kubelet" 로 허용합니다. 같은 문서의 안전 목록에 `net.ipv4.conf.*` 나 `rp_filter` 항목은 없습니다.
[^tuning]: [tuning plugin](https://www.cni.dev/plugins/current/meta/tuning/) (2026-11-24 조회). 이 플러그인은 "will set /proc/sys/net/core/somaxconn to 500 and /proc/sys/net/ipv4/conf/IFNAME/arp_filter to 1, while IFNAME in the path will be substituted with an interface name passed to this plugin" 이라고 적고, "It is only useful when used in addition to other plugins" 라고 밝힙니다. 예시 키가 `arp_filter` 라서 `rp_filter` 를 직접 쓴 예는 아니고, 같은 문서의 "Other sysctls can be modified as long as they belong to the network namespace" 를 근거로 대안으로 적었습니다.
[^kproxy]: kube-proxy iptables 모드의 소스 [pkg/proxy/iptables/proxier.go](https://github.com/kubernetes/kubernetes/blob/v1.34.0/pkg/proxy/iptables/proxier.go) (v1.34.0). 주석이 "Drop the packets in INVALID state, which would potentially cause" 로 시작하고, `nf_conntrack_tcp_be_liberal` 이 켜져 있으면 "not installing DROP rules for INVALID packets" 를 남깁니다.
[^nfct]: 커널 문서 [nf_conntrack-sysctl](https://github.com/torvalds/linux/blob/v7.2/Documentation/networking/nf_conntrack-sysctl.rst) (v7.2). `nf_conntrack_tcp_loose` 는 "If it is set to zero, we disable picking up already established connections." 로 설명하고 기본값은 enabled 입니다.
[^ip-sysctl]: 커널 문서 [ip-sysctl](https://github.com/torvalds/linux/blob/v7.2/Documentation/networking/ip-sysctl.rst) (v7.2) 의 `rp_filter` 항목. 1 은 "Strict mode as defined in RFC3704 Strict Reverse Path" 이고 합치는 규칙은 "The max value from conf/{all,interface}/rp_filter is used" 입니다. 이 VM 커널(7.2.12)에서 `all`·인터페이스 조합을 서버에 걸어 동작을 직접 확인했습니다.
[^hub]: Docker Hub 의 공개 태그 조회 [golang:1.25-alpine](https://hub.docker.com/v2/repositories/library/golang/tags/1.25-alpine) 와 [nicolaka/netshoot:v0.13](https://hub.docker.com/v2/repositories/nicolaka/netshoot/tags/v0.13) 의 응답에 `name` 이 각각 "1.25-alpine" 과 "v0.13" 으로 들어 있습니다. 로그인 없이 조회했습니다.
[^cniver]: bridge 플러그인 v1.10.0 의 [bridge.go](https://github.com/containernetworking/plugins/blob/v1.10.0/plugins/main/bridge/bridge.go) 는 "version.All, bv.BuildString(" 으로 지원 버전을 등록하고, 같은 태그의 go.mod 가 요구하는 CNI v1.3.1 의 [version.go](https://github.com/containernetworking/cni/blob/v1.3.1/pkg/version/version.go) 에서 "All = PluginSupports(" 줄의 목록에 0.3.0 이 있습니다.
[^multus]: Multus v4.3.2 의 [how-to-use.md](https://github.com/k8snetworkplumbingwg/multus-cni/blob/v4.3.2/docs/how-to-use.md) 의 "NetworkAttachmentDefinition with json CNI config" 예제들이 `cniVersion` 으로 0.3.0 을 씁니다. Multus 가 이 값을 받아들이는지를 코드에서 따로 확인하지는 않았습니다.
[^wb]: Whereabouts v0.9.4 의 [README.md](https://github.com/k8snetworkplumbingwg/whereabouts/blob/v0.9.4/README.md) 는 `range_start` 를 "First IP to use when allocating from the" 로, `range_end` 를 "Last IP to use when allocating from the" 로 설명하고 `range` 는 예제에 씁니다. Multus 주석 키는 [how-to-use.md](https://github.com/k8snetworkplumbingwg/multus-cni/blob/v4.3.2/docs/how-to-use.md) 의 "k8s.v1.cni.cncf.io/networks: macvlan-conf-1, macvlan-conf-2" 예제에 있습니다.
[^arp]: 커널 [net/ipv4/arp.c](https://github.com/torvalds/linux/blob/v7.2/net/ipv4/arp.c) (v7.2) 의 `arp_process` 에 "ip_route_input_noref(skb, tip, sip, 0, dev) == 0" 조건이 있습니다. 이 호출이 보내는 쪽 주소(`sip`)에 입력 경로 검증을 거는 자리로 읽었을 뿐이고, 차단 원인은 `net1` 의 `rp_filter` 만 바꿔 결과가 뒤집힌 재현으로 판단했습니다.
[^iproute]: [ip-route(8)](https://man7.org/linux/man-pages/man8/ip-route.8.html) (2026-11-24 조회). `ip route get` 은 "this command gets a single route to a destination and prints its contents exactly as the kernel sees it" 이고 `from` 은 "from ADDRESS the source address." 로 적혀 있습니다.
[^iprule]: [ip-rule(8)](https://man7.org/linux/man-pages/man8/ip-rule.8.html) (2026-11-24 조회). 기본 규칙은 "Priority: 0, Selector: match anything, Action: lookup routing table local", "Priority: 32766, Selector: match anything, Action: lookup routing table main", "Priority: 32767, Selector: match anything, Action: lookup routing table default" 이고, 번호는 "a lower number means higher priority" 로 읽습니다. 조건에는 `fwmark`·`iif` 가 있습니다.
