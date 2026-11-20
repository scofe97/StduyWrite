---
title: Ambient 모드와 ztunnel·waypoint — 사이드카 없이 L4 와 L7 을 나눈 데이터 플레인
tags: [istio, ambient-mesh, ztunnel, waypoint, hbone, service-mesh, kubernetes]
status: draft
review:
  status: pending
source:
  - https://istio.io/v1.32/docs/ambient/overview/
  - https://istio.io/v1.32/docs/ambient/architecture/data-plane/
  - https://istio.io/v1.32/docs/ambient/architecture/control-plane/
  - https://istio.io/v1.32/docs/ambient/architecture/hbone/
  - https://istio.io/v1.32/docs/ambient/architecture/traffic-redirection/
  - https://istio.io/v1.32/docs/ambient/usage/waypoint/
  - https://istio.io/v1.32/docs/ambient/migrate/
  - https://istio.io/v1.32/docs/ambient/migrate/install-ambient-components/
  - https://istio.io/v1.32/docs/ambient/migrate/enable-ambient-mode/
  - https://istio.io/latest/blog/2024/ambient-reaches-ga/
  - https://istio.io/latest/blog/2022/ambient-security/
  - https://istio.io/latest/blog/2023/rust-based-ztunnel/
related:
  - ../../book/istio-in-action/01-01.서비스 메시는 무엇을 인프라로 밀어냈는가.md
  - ./README.md
updated: 2026-11-17
---

# Ambient 모드와 ztunnel·waypoint — 사이드카 없이 L4 와 L7 을 나눈 데이터 플레인

---

> 파드마다 주입하던 사이드카 프록시를 걷어내고 L4 보안 전송 계층과 L7 애플리케이션 프록시 계층을 분리한 Istio Ambient 모드의 동작 원리를 다룹니다. 노드 공유 데몬셋인 ztunnel 과 필요할 때만 붙이는 waypoint 프록시의 책임 경계를 확인합니다.

## 학습 목표

> 이 문서를 읽고 나면 아래 다섯 가지를 설명할 수 있습니다.

1. 사이드카 배포 모델이 안고 있던 리소스 오버헤드와 애플리케이션 결합 문제를 설명할 수 있습니다.
2. ztunnel 이 Rust 기반 데몬셋으로 동작하며 HBONE 터널로 L4 mTLS 를 맺는 원리를 설명할 수 있습니다.
3. waypoint 프록시가 Gateway API 기반으로 선언되고 L7 정책을 집행하는 과정을 설명할 수 있습니다.
4. 노드 공유 프록시 환경에서 멀티테넌시 격리와 위협 완화 모델을 공식 문서에 근거해 설명할 수 있습니다.
5. 기존 사이드카 워크로드와 Ambient 워크로드의 상호 운용 방식과 단계별 전환 절차를 설명할 수 있습니다.

기준 판은 Istio 1.32 문서입니다. 다루지 않는 범위가 둘 있습니다. 단일 노드 테스트 클러스터 설치 명령의 세부 파라미터는 여기서 다루지 않습니다. Gateway API 의 GAMMA 라우팅 명세와 HTTPRoute 문법은 별도 가이드가 다룹니다.

아래 도식은 기존 사이드카 모델과 Ambient 2계층 데이터 플레인의 구조적 차이를 한눈에 보여 줍니다.

![사이드카 배포와 Ambient 2계층 데이터 플레인 비교](./_assets/Ambient%20%EB%AA%A8%EB%93%9C%C2%B7ztunnel%C2%B7waypoint.overview.svg)



## 1. 사이드카 모델의 비용과 결합

> 사이드카 패턴은 애플리케이션 파드마다 Envoy 프록시를 동반하여 네트워크 기능을 인프라로 격리했습니다. 그러나 파드 수명주기와의 강한 결합과 리소스 과할당이라는 구조적 한계를 남겼습니다.

사이드카 모드는 워크로드마다 Envoy 프록시 인스턴스를 하나씩 곁에 띄웁니다.[^istio-waypoint] 애플리케이션 코드 수정 없이 트래픽을 가로채려고 파드 네트워크를 공유한 구조입니다. 사이드카 모델의 등장 배경은 [01-01.서비스 메시는 무엇을 인프라로 밀어냈는가.md](../../book/istio-in-action/01-01.서비스%20메시는%20무엇을%20인프라로%20밀어냈는가.md)에서 자세히 다룹니다.

Ambient GA 발표는 사용자들이 사이드카에서 겪은 어려움을 세 가지로 꼽습니다.[^ambient-ga]

첫째로 파드 수명주기의 강한 결합입니다. Istio 새 릴리스가 나올 때마다 프록시를 올리려고 애플리케이션 파드를 재시작해야 했습니다. 같은 발표에 실린 사용자 후기는 사이드카의 기동·종료 순서에서 생기는 경쟁 조건(race condition)도 함께 꼽습니다.

둘째로 리소스 과할당 오버헤드입니다. 워크로드마다 붙은 프록시가 CPU 와 메모리를 크게 요구합니다. 쿠버네티스 스케줄러는 컨테이너들의 requests 합을 기준으로 노드를 배정하므로, 예상 부하에 맞춰 프록시마다 잡아 둔 여유분이 파드 수만큼 쌓입니다.

셋째로 애플리케이션 호환성입니다. 사이드카를 넣은 뒤에 애플리케이션이 깨지는 일이 있었습니다. 발표는 Ambient 에서 서버가 먼저 말을 거는(server-send-first) 프로토콜이 동작하고, 예약 포트 대부분을 다시 쓸 수 있다고 설명합니다.

Istio Ambient 모드는 데이터 플레인을 두 계층으로 쪼개어 이 문제를 풉니다. 노드마다 하나씩 도는 L4 프록시가 기본 전송 보안을 맡습니다. L7 프록시는 필요한 곳에만 붙습니다.[^istio-overview] 사이드카에서는 mTLS 만 쓰더라도 L7 까지 처리하는 프록시 전체를 들여야 했습니다. Ambient 에서는 L4 오버레이로 시작해 L7 을 필요한 만큼만 더합니다.[^ambient-security]



## 2. ztunnel 과 HBONE 터널링

> ztunnel 은 노드마다 데몬셋으로 떠서 L4 암호화와 신원 인증을 처리하는 공유 프록시입니다. 메시 안 워크로드 사이의 TCP 트래픽을 HBONE mTLS 터널로 감쌉니다.

파드마다 프록시를 띄우지 않으려면 노드 수준에서 L4 전송을 대리할 공용 프록시가 필요합니다. Istio 는 노드마다 데몬셋으로 `ztunnel`(Zero Trust tunnel) 파드를 띄웁니다. ztunnel 은 범용 Envoy 가 아니라 Rust 로 작성한 Ambient 전용 노드 프록시이고, 처리 범위를 L3·L4 로 의도적으로 좁혔습니다.[^istio-ztunnel]

ztunnel 의 핵심 설계 원칙은 최소성과 안전성입니다.

- L4 전용 처리: 워크로드의 HTTP 트래픽을 종단하거나 HTTP 헤더를 파싱하지 않습니다. mTLS, 인증, L4 인가 정책 검사, TCP 텔레메트리 수집만 수행합니다.
- Rust 기반 구현: Envoy 일부를 재사용하는 C++ 구현도 검토했지만 메모리 안전성 부족 등을 이유로 접었습니다.[^rust-ztunnel] 목표는 빠르고 안전하고 가벼운 프록시였습니다.
- 동적 신원 발급: ztunnel 은 xDS 로 istiod 에서 자기 노드에 스케줄된 모든 파드의 ServiceAccount 용 mTLS 인증서를 받습니다.[^istio-control-plane] 인증서가 만료에 가까워지면 교체도 ztunnel 이 맡습니다.

워크로드 간 통신에는 **HBONE**(HTTP-Based Overlay Network Environment) 프로토콜을 씁니다. HBONE 은 세 표준을 조합합니다.

- HTTP CONNECT: 터널 연결을 엽니다.
- mTLS: 그 연결을 암호화하고 양쪽 신원을 확인합니다.
- HTTP/2: 여러 애플리케이션 연결을 한 터널 위에 다중화합니다.

Istio 관례상 HBONE 을 이해하는 프록시는 TCP 15008 번 포트에서 받습니다.[^istio-hbone]

파드 안의 애플리케이션은 프록시의 존재를 알지 못합니다. istio-cni 노드 에이전트가 파드의 네트워크 네임스페이스 안에 리다이렉션 규칙을 넣습니다. ztunnel 은 그 네임스페이스 안에 수신 포트(15008·15006·15001)를 엽니다.[^istio-redirection] 그래서 파드를 드나드는 패킷이 노드의 ztunnel 로 투명하게 넘어갑니다.



## 3. waypoint 프록시와 L7 정책 집행

> L7 라우팅과 헤더 조작, 고급 인가 정책이 필요할 때만 독립적인 waypoint 프록시를 띄웁니다. 워크로드 파드 외부에서 서비스 단위로 수평 확장됩니다.

L4 암호화만으로는 헤더 기반 라우팅이나 세밀한 인가를 처리할 수 없습니다. Istio 는 필요한 서비스에만 독립 Envoy 프록시인 **waypoint** 를 붙입니다.[^istio-waypoint] waypoint 는 파드 외부에서 네임스페이스나 서비스 단위로 배포됩니다.

아래 도식은 L4 기본 통신 경로와 L7 waypoint 경유 경로를 비교해 보여 줍니다.

![Ambient 모드의 두 가지 트래픽 경로](./_assets/Ambient%20%EB%AA%A8%EB%93%9C%C2%B7ztunnel%C2%B7waypoint.traffic-path.svg)

waypoint 프록시는 쿠버네티스 Gateway API 의 Gateway 리소스로 선언됩니다.[^istio-waypoint] `istioctl waypoint generate --for service -n default` 가 만드는 리소스는 다음과 같습니다.

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  labels:
    istio.io/waypoint-for: service
  name: waypoint
  namespace: default
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE
```

운영자는 `istioctl waypoint apply -n default` 로 기본 waypoint 를 배포합니다. 대상 네임스페이스에 `istio.io/use-waypoint: waypoint` 라벨을 달면 ztunnel 이 그 네임스페이스의 서비스로 가는 트래픽을 waypoint 로 먼저 보냅니다. `--enroll-namespace` 를 붙이면 배포와 라벨을 한 번에 처리합니다. 라벨 `istio.io/waypoint-for: service` 는 기본값이며, 서비스로 향하는 트래픽만 받는다는 뜻입니다. 파드 IP 로 직접 가는 트래픽까지 받으려면 `--for workload` 나 `--for all` 을 씁니다.

waypoint 의 핵심 특성은 다음과 같습니다.

1. 선택적 프로비저닝: L4 암호화만 필요한 서비스는 waypoint 를 생성할 필요가 없습니다. 불필요한 프록시 홉과 연산 낭비가 사라집니다.
2. 독립적 수명주기: waypoint 는 애플리케이션과 따로 설치·업그레이드·확장되므로, waypoint 를 올려도 애플리케이션 파드를 재시작할 일이 없습니다.
3. 대상 중심 정책 집행: waypoint 는 호출자(Source)가 아니라 호출받는 대상(Destination)의 경계에서 정책을 집행합니다. 목적지 서비스의 HTTPRoute, 타임아웃, L7 인가 정책이 여기서 적용됩니다.



## 4. 노드 공유 프록시의 멀티테넌시 위협 모델

> 여러 파드가 한 노드의 ztunnel 을 공유하므로, ztunnel 이 뚫렸을 때 피해가 어디까지 번지는지가 보안 모델의 핵심 과제입니다. Istio 는 L4 로 좁힌 공격 표면, 노드 단위 신원 발급, 파드 안 리다이렉션, waypoint 강제 정책으로 피해 범위를 줄입니다.

ztunnel 은 노드의 모든 파드가 공유하는 구성 요소입니다. 그래서 CNI 에이전트나 kubelet 과 같은 수준으로 민감하게 다뤄야 합니다.[^ambient-security] 공식 문서와 설계 블로그에 흩어진 설명을 모으면 방어선이 네 겹 보입니다.

첫째로 공격 표면 최소화입니다. L7 프로토콜 처리와 Wasm·Lua 확장은 코드가 많아 취약점이 나올 가능성이 큽니다. 설계 블로그는 Envoy 취약점도 역사적으로 대부분 L7 처리 스택에서 나왔다고 적습니다.[^ambient-security] ztunnel 은 L4 만 처리하도록 범위를 좁혔기 때문에 공유 구성 요소로 안전하게 둘 수 있습니다.[^istio-waypoint] L7 처리는 여러 신원이 한 프록시를 나눠 쓰지 않도록 waypoint 로 따로 뺍니다.

둘째로 노드 로컬 신원 격리입니다. ztunnel 은 자기 신원으로 CA 에 인증하되 다른 워크로드의 신원을 요청하고, CA 는 그 노드에서 실행 중이 아닌 신원 요청을 거부합니다.[^istio-data-plane] 그래서 ztunnel 하나가 뚫려도 털릴 수 있는 자격증명은 그 노드에 지금 떠 있는 파드의 것뿐입니다. ztunnel 자신의 신원은 워크로드 간 mTLS 에 쓰이지 않습니다.

셋째로 트래픽 리다이렉션 강제입니다. ztunnel 을 우회할 수 있으면 인가 정책도 우회되므로, 트래픽 가로채기는 보안에 직결됩니다.[^istio-redirection] istio-cni 는 파드의 네트워크 네임스페이스 안에 iptables 규칙을 넣습니다. 이 규칙이 파드를 드나드는 TCP 를 ztunnel 이 그 네임스페이스 안에 연 포트로 돌립니다. GA 발표는 컨테이너가 악의로든 실수로든 사이드카를 우회하던 틈이 Ambient 에서 없어졌다고 설명합니다.[^ambient-ga-bypass]

넷째로 waypoint 우회 방지입니다. `istio.io/use-waypoint` 라벨은 의도를 적을 뿐 경유를 보장하지 않습니다. ztunnel 은 두 경우에 요청을 실패시키지 않고 목적지로 바로 보냅니다. 지정한 waypoint 가 없거나 주소가 없을 때, 그리고 트래픽 종류가 waypoint 가 받는 종류와 다를 때입니다. 서비스용 waypoint 앞에서 파드 IP 로 직접 보낸 요청이 뒤의 예입니다.[^istio-waypoint] 클라이언트가 워크로드에 직접 접속해도 마찬가지로 waypoint 를 건너뜁니다.

L7 정책이 보안 요건이면 목적지 워크로드에 waypoint 의 서비스 계정만 허용하는 `AuthorizationPolicy` 를 겁니다.

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: require-waypoint
  namespace: default
spec:
  selector:
    matchLabels:
      app: reviews
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/reviews-svc-waypoint
```

이 정책은 targetRef 가 아니라 워크로드 selector 를 쓰므로 ztunnel 이 L4 에서 집행합니다. 그래서 waypoint 가 없을 때와 클라이언트가 직접 접속할 때 모두 막힙니다.



## 5. 사이드카와의 공존과 점진적 전환

> 운영 중인 클러스터를 한 번에 전환할 수는 없습니다. Istio 는 사이드카 워크로드와 Ambient 워크로드가 같은 메시 안에서 통신하게 하고, 네임스페이스 하나씩 옮기는 전환 절차를 안내합니다.

사이드카 워크로드와 Ambient 워크로드는 같은 메시 안에 함께 있을 수 있고, 전환은 네임스페이스 하나씩 진행합니다.[^istio-migrate]

- Ambient 에서 Sidecar 로 호출: 목적지가 사이드카처럼 Istio 프록시 기능을 가졌으면 출발지 ztunnel 이 요청을 HBONE 터널로 올려 보냅니다.[^istio-data-plane]
- Sidecar 에서 Ambient 로 호출: HBONE 을 켠 사이드카가 목적지 파드의 ztunnel 로 HBONE 터널을 직접 엽니다.[^istio-migrate-install]

공존 환경에서 반드시 인지해야 할 구조적 제약이 하나 있습니다. 사이드카 워크로드가 Ambient 대상 서비스를 호출하면 목적지의 waypoint 프록시를 거치지 않습니다.[^istio-migrate-install] 사이드카는 자기 L7 로직을 적용한 뒤 HBONE 으로 목적지 파드의 ztunnel 에 바로 보내기 때문입니다. 따라서 waypoint 에 건 L7 정책(HTTPRoute, targetRefs 를 쓰는 AuthorizationPolicy)은 사이드카 호출자에게 적용되지 않습니다. 앞 절의 waypoint 강제 정책을 걸어 두었다면 사이드카 호출자의 트래픽도 거부됩니다.

L7 정책이 있으면 아직 무중단 전환 경로가 없습니다. 옛 selector 기반 정책을 지우고 waypoint 기반 정책을 새로 거는 사이에 L7 규칙이 집행되지 않는 구간이 생깁니다. 그래서 공식 가이드는 정비 시간을 잡으라고 권합니다.[^istio-migrate]

공식 가이드의 전환 순서는 다음과 같습니다.

1. Ambient 구성 요소 설치: ambient 프로파일로 올려 ztunnel 데몬셋을 더하고 CNI 를 갱신합니다. 기존 사이드카는 재시작해서 ambient 프로파일이 MeshConfig 에 넣은 `ISTIO_META_ENABLE_HBONE=true` 를 받게 합니다. L7 기능이 필요한 네임스페이스에는 waypoint 를 미리 배포해 두되 아직 활성화하지 않습니다.
2. 정책 이관: VirtualService 는 HTTPRoute 로 옮깁니다. Ambient 에서 VirtualService 지원은 Alpha 단계입니다. L7 규칙이 있는 AuthorizationPolicy, RequestAuthentication, WasmPlugin 은 targetRefs 로 waypoint 에 붙입니다. L4 정책만 쓰면 이 단계를 건너뜁니다.
3. 네임스페이스 단위 전환: `istio.io/use-waypoint` 라벨로 waypoint 를 먼저 활성화합니다. 그다음 네임스페이스에 `istio.io/dataplane-mode=ambient` 라벨을 답니다. Ambient 가 동작하는 것을 확인한 뒤 사이드카 주입 라벨을 빼고, 파드는 마지막에 재시작합니다. 순서를 어기면 사이드카도 ztunnel 도 처리하지 않는 트래픽이 생길 수 있습니다.[^istio-migrate-enable]
4. 옛 정책 정리와 확대: 파드를 재시작한 직후 옛 사이드카용 정책을 지웁니다. ztunnel 은 AuthorizationPolicy 의 L7 조건을 조용히 버리므로, L7 조건만 있던 ALLOW 정책은 그 워크로드로 가는 트래픽을 모두 막을 수 있습니다. 확인이 끝나면 다음 네임스페이스로 넓힙니다.



## 6. 점검 질문

> 되물어야 할 핵심 설계 원칙을 질문 형태로 정리합니다.

### Q1. ztunnel 의 L7 트래픽 해석 여부

ztunnel 은 HTTP 헤더나 요청 URL 경로를 검사하여 인가 정책을 집행할 수 있습니까?

### Q2. waypoint 프록시의 네임스페이스 분리 이유

waypoint 프록시를 클러스터에 단 하나만 중앙 집중형으로 두지 않고 네임스페이스나 서비스 단위로 분리하는 이유는 무엇입니까?

### Q3. 사이드카 없는 mTLS 암호화와 신원 보장 원리

파드 안에 사이드카 컨테이너가 없는데도 어떻게 워크로드 수준의 mTLS 암호화와 암호학적 신원이 보장됩니까?

### Q4. 사이드카의 waypoint 우회 원인

사이드카 모드 워크로드가 Ambient 모드 대상 서비스를 호출할 때 대상 waypoint 프록시가 우회되는 이유는 무엇입니까?



## 정답 (자답 후 펼치기)

> 위 점검 질문 4개에 먼저 자답한 뒤 아래를 읽으세요.

### 정답 1 — ztunnel 의 L4 전용 설계

해석할 수 없습니다. ztunnel 은 L3 와 L4 전송 계층만 다루는 전용 프록시입니다. HTTP 헤더 해석, 패스 기반 라우팅, JWT 검증 같은 L7 기능은 의도적으로 배제되어 있습니다. 이러한 L7 기능이 필요하면 대상 서비스에 waypoint 프록시를 연결해야 합니다.

### 정답 2 — 멀티테넌시 격리와 장애 반경 제한

L7 처리는 코드가 복잡해 취약점과 설정 변수가 많습니다. 여러 신원의 복잡한 정책과 확장을 한 프록시에 모으면 비용을 공정하게 나누기 어렵고, 최악에는 프록시 하나가 뚫려 모든 테넌트가 함께 무너집니다. 그래서 waypoint 는 보안 경계가 비슷한 애플리케이션끼리만, 예컨대 한 워크로드의 인스턴스들이나 한 네임스페이스 단위로 나눠 씁니다. 범위가 정해져 있으니 그 범위의 부하에 맞춰 따로 확장할 수도 있습니다.

### 정답 3 — CNI 와 동적 mTLS 인증서 발급

istio-cni 가 파드의 네트워크 네임스페이스 안에 넣은 리다이렉션 규칙이 트래픽을 노드의 ztunnel 로 돌립니다. ztunnel 은 istiod 에서 그 파드의 ServiceAccount 신원 인증서를 받아 목적지 쪽과 HBONE mTLS 터널을 맺습니다. 공식 문서는 이 터널이 실제로는 출발지 파드와 목적지 파드의 네트워크 네임스페이스 사이에 놓인다고 설명합니다. 따라서 파드 내부 수정 없이도 전송 구간 암호화와 신원 검증이 완성됩니다.

### 정답 4 — 사이드카 발신의 waypoint 우회

사이드카는 자기 L7 라우팅을 스스로 처리한 뒤 HBONE 터널로 목적지 파드의 ztunnel 에 바로 보내기 때문입니다. 지금의 사이드카와 게이트웨이는 waypoint 를 알지 못하고, 공식 문서는 이후 릴리스에서 알게 할 예정이라고 적습니다. 그 사이 waypoint 의 L7 정책을 사이드카 호출자에게도 적용하려면 호출자도 Ambient 모드로 옮겨야 합니다.



## 7. 다음 단계

> 이 문서가 다룬 데이터 플레인 분리를 외부 인그레스와 GAMMA 메시 라우팅으로 확장합니다.

L4 전송 오버레이와 L7 waypoint 분리는 클러스터 내부 트래픽의 아키텍처를 단순화했습니다. 외부에서 들어오는 진입점과의 통합은 Istio Ingress Gateway 와 Gateway API 명세가 이어받습니다.

메시 내부 서비스 간 HTTPRoute 라우팅을 표준화하는 Gateway API GAMMA 명세는 별도 가이드에서 다룹니다.



## 관련 문서

> 데이터 플레인 아키텍처 및 서비스 메시 개념과 이어지는 학습 문서입니다.

- [서비스 메시는 무엇을 인프라로 밀어냈는가](../../book/istio-in-action/01-01.서비스%20메시는%20무엇을%20인프라로%20밀어냈는가.md) — 서비스 메시의 기원과 사이드카 패턴의 구조적 필요성
- [Istio 공식문서 정독 인덱스](./README.md) — 제품 폴더 MOC 및 공식 문서 학습 가이드
- [쿠버네티스 공식문서 정독](../kubernetes/README.md) — 노드 네트워크 및 파드 수명주기 기반 인프라



## 참고 자료

> 본문에서 인용한 공식 1차 자료입니다. 문서 주소는 Istio 1.32 판으로 고정했습니다.

- [Istio 1.32 — Ambient 모드 개요](https://istio.io/v1.32/docs/ambient/overview/) — Ambient 메시 개념과 2계층 데이터 플레인, ztunnel·waypoint 소개
- [Istio 1.32 — Ambient 데이터 플레인](https://istio.io/v1.32/docs/ambient/architecture/data-plane/) — 메시 안 라우팅, 노드 단위 신원 발급, waypoint 경유 경로
- [Istio 1.32 — Ambient 와 컨트롤 플레인](https://istio.io/v1.32/docs/ambient/architecture/control-plane/) — ztunnel 과 istiod 의 xDS 통신과 인증서 수령
- [Istio 1.32 — HBONE](https://istio.io/v1.32/docs/ambient/architecture/hbone/) — HTTP-Based Overlay Network Environment 터널 프로토콜
- [Istio 1.32 — ztunnel 트래픽 리다이렉션](https://istio.io/v1.32/docs/ambient/architecture/traffic-redirection/) — istio-cni 의 파드 안 리다이렉션 모델
- [Istio 1.32 — waypoint 프록시 구성](https://istio.io/v1.32/docs/ambient/usage/waypoint/) — Gateway API 기반 waypoint 배포, 라벨, 우회 방지 정책
- [Istio 1.32 — 사이드카에서 Ambient 로 전환](https://istio.io/v1.32/docs/ambient/migrate/) — 전환 전략, 리소스 대응표, 지원하지 않는 구성
- [Istio 1.32 — Ambient 구성 요소 설치](https://istio.io/v1.32/docs/ambient/migrate/install-ambient-components/) — 사이드카 HBONE 활성화와 공존 중 waypoint 우회
- [Istio 1.32 — Ambient 모드 활성화](https://istio.io/v1.32/docs/ambient/migrate/enable-ambient-mode/) — 네임스페이스 전환 순서와 옛 정책 정리
- [Istio 블로그 — Ambient GA 발표 (v1.24)](https://istio.io/latest/blog/2024/ambient-reaches-ga/) — Istio 1.24 Ambient 모드 정식 릴리스 안내
- [Istio 블로그 — Ambient 모드 보안 심층 분석 (2022)](https://istio.io/latest/blog/2022/ambient-security/) — 노드 공유 ztunnel 과 L7 프록시 분리의 보안 근거
- [Istio 블로그 — Rust 기반 ztunnel 소개 (2023)](https://istio.io/latest/blog/2023/rust-based-ztunnel/) — ztunnel 을 Envoy 대신 Rust 로 새로 만든 이유

[^istio-overview]: Istio 1.32 — Ambient mode overview. "In ambient mode, Istio implements its features using a per-node Layer 4 (L4) proxy, and optionally a per-namespace Layer 7 (L7) proxy." <https://istio.io/v1.32/docs/ambient/overview/> (2026-11-17 조회)

[^ambient-ga]: Istio Blog — Fast, Secure, and Simple: Istio’s Ambient Mode Reaches General Availability in v1.24. "Challenges that Istio users shared with us include how sidecars can break applications after they are added, the large CPU and memory requirement for a proxy with every workload, and the inconvenience of needing to restart application pods with every new Istio release." <https://istio.io/latest/blog/2024/ambient-reaches-ga/> (2026-11-17 조회)

[^ambient-ga-bypass]: Istio Blog — Fast, Secure, and Simple: Istio’s Ambient Mode Reaches General Availability in v1.24. "Server-send-first protocols now work, most reserved ports are now available, and the ability for containers to bypass the sidecar — either maliciously or not — is eliminated." <https://istio.io/latest/blog/2024/ambient-reaches-ga/> (2026-11-17 조회)

[^ambient-security]: Istio Blog — Ambient Mode Security Deep Dive (2022). "This ensures that the blast radius for a compromised ztunnel is that only credentials for pods currently scheduled on that node could be stolen." <https://istio.io/latest/blog/2022/ambient-security/> (2026-11-17 조회)

[^istio-ztunnel]: Istio 1.32 — Ambient mode overview, 「ztunnel」 절. "The ztunnel proxy is written in Rust and is intentionally scoped to handle L3 and L4 functions such as mTLS, authentication, L4 authorization and telemetry." <https://istio.io/v1.32/docs/ambient/overview/> (2026-11-17 조회)

[^rust-ztunnel]: Istio Blog — Introducing Rust-Based Ztunnel for Istio Ambient Service Mesh (2023). "A C++ implementation – likely reusing parts of Envoy – was also considered. However, this option was not pursued due to lack of memory safety, developer experience concerns, and a general industry trend towards Rust." <https://istio.io/latest/blog/2023/rust-based-ztunnel/> (2026-11-17 조회)

[^istio-control-plane]: Istio 1.32 — Ambient and the Istio control plane. "The ztunnel proxy also obtains mTLS certificates for the Service Accounts of all pods that are scheduled on its Kubernetes node using xDS." <https://istio.io/v1.32/docs/ambient/architecture/control-plane/> (2026-11-17 조회)

[^istio-hbone]: Istio 1.32 — HBONE. "By Istio convention, ztunnel and other proxies that understand the HBONE protocol expose listeners on TCP port 15008." <https://istio.io/v1.32/docs/ambient/architecture/hbone/> (2026-11-17 조회)

[^istio-redirection]: Istio 1.32 — Ztunnel traffic redirection. "This is a security critical task: if the ztunnel can be bypassed, authorization policies can be bypassed." <https://istio.io/v1.32/docs/ambient/architecture/traffic-redirection/> (2026-11-17 조회)

[^istio-waypoint]: Istio 1.32 — Configure waypoint proxies. "Ztunnel is scoped to only process traffic at Layer 4 (L4), so that it can safely operate as a shared component." <https://istio.io/v1.32/docs/ambient/usage/waypoint/> (2026-11-17 조회)

[^istio-data-plane]: Istio 1.32 — Ambient data plane. "Requests for identities not running on the node are rejected. This is critical to ensure that a compromised node does not compromise the entire mesh." <https://istio.io/v1.32/docs/ambient/architecture/data-plane/> (2026-11-17 조회)

[^istio-migrate]: Istio 1.32 — Migrate from Sidecar to Ambient. "If you have L7 policies, zero-downtime migration is not currently possible." <https://istio.io/v1.32/docs/ambient/migrate/> (2026-11-17 조회)

[^istio-migrate-install]: Istio 1.32 — Install ambient components. "When a sidecar-injected pod communicates with a workload that has already been moved to ambient mode, the sidecar uses the HBONE protocol to tunnel traffic directly to the destination pod’s ztunnel." <https://istio.io/v1.32/docs/ambient/migrate/install-ambient-components/> (2026-11-17 조회)

[^istio-migrate-enable]: Istio 1.32 — Enable ambient mode. "Failing to follow this sequence can result in traffic being processed by neither sidecar nor ztunnel, causing disruption in your workloads." <https://istio.io/v1.32/docs/ambient/migrate/enable-ambient-mode/> (2026-11-17 조회)
