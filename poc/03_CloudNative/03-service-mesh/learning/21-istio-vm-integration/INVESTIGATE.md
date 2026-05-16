<!-- migrated:
  - write/09_cloud/service-mesh/deepdive/21-01.Istio VM 통합 실습.md
  - write/09_cloud/service-mesh/deepdive/21-02.Istio VM 통합 점검.md
  (2026-04-19) -->

# Ch21. Istio와 가상머신 통합 — Deep Dive Questions

---

## Q1. WorkloadEntry와 ServiceEntry의 사용 시나리오 차이는?

### 왜 중요한가?

VM을 Istio 메시에 편입할 때 WorkloadEntry와 ServiceEntry를 혼동하면 "VM에서 K8s 서비스를 호출할 수는 있는데 K8s Pod에서 VM을 DNS로 호출할 수 없다"거나 "트래픽 관리 정책이 VM에 적용되지 않는다"는 상황이 발생한다. 두 리소스는 목적이 다르며, 어떤 시나리오에서 각각 또는 함께 사용해야 하는지 이해하는 것이 VM 통합 설계의 출발점이다.

### 분석

**WorkloadEntry**는 VM의 개별 인스턴스를 메시 서비스 레지스트리에 등록하는 리소스다. Pod에 비유하면 WorkloadEntry는 VM의 "Pod 정의"에 해당한다. IP 주소, 레이블, 서비스 계정을 선언하면 istiod가 이 VM 인스턴스를 엔드포인트로 관리한다. WorkloadEntry만 있어도 VM은 메시의 일원이 되어 mTLS 통신이 가능하다. 그러나 DNS 이름이 없어 K8s Pod가 VM을 서비스 이름으로 호출할 수 없다.

**ServiceEntry**는 메시 외부의 서비스(도메인, IP 범위, 외부 API 등)를 Istio 서비스 레지스트리에 추가하는 리소스다. VM을 위한 ServiceEntry는 `workloadSelector`로 WorkloadEntry를 선택하여, VM 인스턴스들을 엔드포인트로 가지는 서비스 이름을 정의한다. ServiceEntry가 있어야 비로소 Pod가 `legacy-api.production.svc.cluster.local`처럼 DNS 이름으로 VM을 호출할 수 있다.

시나리오별 사용 패턴은 다음과 같이 구분된다.

**VM을 호출하는 쪽이 없고, VM이 K8s 서비스만 호출하는 단방향 시나리오**에서는 WorkloadEntry만으로 충분하다. VM의 Envoy가 메시에 편입되어 outbound 트래픽에 mTLS를 적용하는 것이 목적이라면 ServiceEntry가 없어도 된다. 레거시 배치 서버가 K8s에 있는 API를 호출하는 구조가 여기 해당한다.

**K8s Pod가 VM을 호출해야 하는 양방향 시나리오**에서는 WorkloadEntry와 ServiceEntry가 함께 필요하다. `workloadSelector`로 WorkloadEntry를 연결하면 ServiceEntry가 VM 인스턴스들을 엔드포인트로 관리한다. VirtualService와 DestinationRule도 이 ServiceEntry의 `hosts`를 참조해서 VM 트래픽에 정책을 적용한다.

**autoRegistration을 사용하는 다수의 VM 인스턴스 시나리오**에서는 WorkloadGroup + ServiceEntry 조합이 기준이다. WorkloadGroup이 VM 집합의 템플릿을 정의하고, 각 VM이 온보딩될 때 WorkloadEntry가 자동 생성된다. ServiceEntry의 `workloadSelector`는 WorkloadGroup이 부여하는 공통 레이블을 선택하면 모든 VM 인스턴스가 자동으로 포함된다.

### 실무 적용

VM 통합을 설계할 때 다음 질문으로 필요한 리소스를 결정한다.

- K8s Pod가 VM을 DNS 이름으로 호출하는가? → ServiceEntry 필요
- 여러 VM 인스턴스를 하나의 서비스로 묶어 로드밸런싱할 필요가 있는가? → ServiceEntry + workloadSelector
- VM이 K8s 서비스를 호출하기만 하는가? → WorkloadEntry만으로 충분
- DestinationRule로 VM 트래픽에 정책(타임아웃, 서킷 브레이커)을 적용할 필요가 있는가? → ServiceEntry 필요 (DestinationRule의 `host`가 ServiceEntry `hosts`와 일치해야 한다)

ServiceEntry의 `resolution: STATIC`은 WorkloadEntry의 IP를 직접 사용하고, `resolution: DNS`는 DNS 조회를 사용한다. VM처럼 고정 IP를 가진 경우는 STATIC이 적합하다.

---

## Q2. VM에서 Istio sidecar의 인증서 갱신이 실패하면 어떤 일이 발생하는가?

### 왜 중요한가?

VM의 Istio sidecar는 K8s Pod와 달리 재시작이 쉽지 않다. Pod는 인증서 갱신에 문제가 생기면 재시작으로 새 인증서를 발급받을 수 있지만, VM은 프로세스 재시작과 인증서 재발급이 수동 개입이 필요한 경우가 있다. 인증서 만료가 조용히 진행되어 트래픽이 갑자기 끊기는 것은 VM 통합에서 가장 흔한 운영 사고 중 하나다.

### 분석

VM 인증서는 istiod의 CA에서 발급하는 SVID(SPIFFE Verifiable Identity Document)다. 기본 TTL은 24시간이며 만료 2/3 시점(약 16시간 후)에 pilot-agent가 자동 갱신을 시도한다.

**갱신 실패의 주요 원인**은 세 가지다.

첫째, **istiod 연결 불가**다. VM이 istiod의 15012 포트에 접근할 수 없으면 갱신 요청 자체가 불가능하다. 네트워크 정책 변경, East-West Gateway 장애, istiod Pod 재시작 중 연결 유실이 원인이 된다. 갱신 재시도는 exponential backoff로 반복되며, 인증서가 만료되기 전까지 계속 시도한다.

둘째, **토큰 만료**다. 초기 인증서 발급 시 사용하는 `istio-token`은 Kubernetes ServiceAccount 토큰이며 만료 시간이 있다. 인증서가 갱신된 이후에는 기존 인증서로 mTLS 연결을 열어 새 CSR을 제출하므로 토큰이 필요 없다. 그러나 VM이 오랫동안 오프라인이었다가 재시작하면 기존 인증서도 만료되고 토큰도 만료된 상황이 발생한다. 이 경우 새 토큰을 VM에 복사한 뒤 `systemctl restart istio`로 재초기화해야 한다.

셋째, **root-cert.pem 불일치**다. 클러스터 CA가 교체되면 VM의 `/etc/certs/root-cert.pem`이 구버전으로 남아 있어 새 istiod 서버를 검증하지 못하고 TLS 핸드셰이크가 실패한다.

**인증서 만료 후 발생하는 현상**은 즉각적이다. mTLS가 STRICT 모드인 경우, VM에서 나가는 모든 outbound 트래픽의 mTLS 핸드셰이크가 실패하여 연결이 거부된다. VM으로 들어오는 inbound 트래픽도 동일하게 실패한다. Envoy Access Log에는 `CERTIFICATE_VERIFY_FAILED`나 `UF`(Upstream connection Failure) Flag가 기록된다.

인증서 만료까지의 시간을 Prometheus로 모니터링할 수 있다.

```promql
# Envoy 인증서 만료까지 남은 초
envoy_server_days_until_first_cert_expiring * 86400
```

이 값이 4시간 이하로 떨어지면 갱신 실패를 의심하고 VM 상태를 확인한다.

### 실무 적용

VM 인증서 상태를 확인하는 절차는 다음과 같다.

```bash
# VM에서 현재 인증서 만료 시간 확인
openssl x509 -in /etc/certs/cert-chain.pem -noout -dates

# pilot-agent 로그에서 갱신 시도 확인
journalctl -u istio -f | grep -i "cert\|renew\|error"

# istiod 연결 상태 확인
curl -v --cacert /etc/certs/root-cert.pem \
  https://istiod.istio-system.svc:15012/healthz/ready
```

예방 차원에서는 VM의 `systemd` 유닛 파일에 자동 재시작을 설정하고, Prometheus 알림으로 인증서 만료 4시간 전에 경보를 보내는 것이 기본이다. 클러스터 CA를 교체할 때는 반드시 모든 VM의 `root-cert.pem`을 사전에 업데이트하는 runbook을 만들어 두어야 한다.

---

## Q3. autoRegistration을 사용할 때 보안 위험은 무엇인가?

### 왜 중요한가?

autoRegistration은 VM 온보딩 자동화의 핵심 기능이지만, 잘못 구성하면 인가되지 않은 VM이 메시에 편입되는 경로가 된다. K8s 환경에서 Pod는 네임스페이스, RBAC, 네트워크 정책으로 격리되지만, autoRegistration을 사용하는 VM은 istiod에 연결할 수 있는 네트워크 경로만 있으면 등록이 가능하다. 이 위험을 이해하지 않으면 메시 보안 경계가 의도치 않게 확장된다.

### 분석

autoRegistration의 동작 방식은 다음과 같다. VM에서 Istio agent가 시작될 때, `cluster.env`에 지정된 WorkloadGroup 이름을 istiod에 전달하며 등록 요청을 보낸다. istiod는 이 요청을 검증하고 WorkloadEntry를 생성한다. VM은 WorkloadGroup에 정의된 serviceAccount의 SPIFFE ID를 발급받는다.

**위험 1: 네트워크 경로 보유 시 무단 등록 가능**이다. istiod의 15012 포트에 도달할 수 있는 어떤 호스트도 등록 요청을 보낼 수 있다. `cluster.env`가 유출되거나, 공격자가 네트워크 내에 발판을 마련했다면 임의의 VM이 등록될 수 있다. 등록된 VM은 WorkloadGroup의 serviceAccount 권한을 그대로 얻으므로, 해당 서비스 계정이 접근 가능한 모든 서비스에 mTLS로 연결할 수 있다.

**위험 2: serviceAccount 권한의 과도한 부여**다. 하나의 WorkloadGroup에 여러 종류의 레거시 서버가 등록되면, 한 서버가 침해됐을 때 동일 WorkloadGroup의 모든 권한을 갖게 된다. 서버 종류별로 별도의 WorkloadGroup과 serviceAccount를 만들고, 각 serviceAccount에 최소 권한만 부여해야 한다.

**위험 3: stale WorkloadEntry를 통한 위장**이다. VM이 제거됐는데 WorkloadEntry가 삭제되지 않은 경우, 동일한 IP를 획득한 다른 호스트가 그 WorkloadEntry의 신원으로 트래픽을 받을 수 있다. 특히 동적 IP 환경에서 IP가 재할당될 때 발생한다.

완화 방법은 여러 레이어에서 적용한다. istiod의 15012 포트에 대한 네트워크 접근을 VPN 또는 특정 IP 대역으로 제한하는 것이 첫 번째 방어선이다. WorkloadGroup에 `network` 필드를 명시하면 지정된 네트워크 식별자를 가진 VM만 등록할 수 있다. `cleanupDelay` 설정으로 VM 오프라인 시 WorkloadEntry를 자동 정리하면 stale 항목 위험을 줄인다.

```yaml
# WorkloadGroup에서 네트워크 범위 제한
spec:
  template:
    serviceAccount: legacy-api-sa
    network: prod-vpc-east   # 이 네트워크에서만 등록 허용
```

### 실무 적용

autoRegistration 사용 환경의 보안 체크리스트는 다음과 같다.

- istiod 15012 포트를 NetworkPolicy 또는 방화벽으로 VM 서브넷만 허용
- WorkloadGroup별로 별도의 서비스 계정 사용 (서버 종류당 1개)
- 각 서비스 계정에 AuthorizationPolicy로 최소 권한 부여
- `cleanupDelay: 90s` 설정으로 오프라인 VM의 WorkloadEntry 자동 정리
- VM shutdown 스크립트에 `systemctl stop istio` 포함 (정상 종료 신호 전달)
- 정기적으로 `kubectl get workloadentry -A`로 비활성 항목 감사

autoRegistration이 편의성을 높이지만 보안 요구사항이 높은 환경이라면 수동 WorkloadEntry 관리를 유지하고 Git으로 상태를 관리하는 GitOps 방식이 더 안전하다. 이 경우 VM 등록이 PR로 승인을 거쳐야 하므로 감사 추적도 자동으로 확보된다.

---

## Q4. VM과 K8s Pod 간 mTLS에서 SPIFFE ID 체계의 차이와 AuthorizationPolicy 작성 시 주의점은?

### 왜 중요한가?

AuthorizationPolicy의 `source.principals`는 SPIFFE ID를 기준으로 발신자를 식별한다. VM과 Pod의 SPIFFE ID 체계는 동일한 형식을 따르지만, VM의 경우 실제 K8s ServiceAccount 사용 여부와 무관하게 WorkloadEntry의 `serviceAccount` 필드값으로 ID가 결정된다. 이 차이를 모르면 AuthorizationPolicy를 잘못 작성하거나, VM 트래픽이 예상치 못하게 차단되거나 허용되는 상황이 발생한다.

### 분석

**Pod의 SPIFFE ID**는 `spiffe://cluster.local/ns/{namespace}/sa/{serviceAccountName}` 형식이다. Pod가 사용하는 실제 K8s ServiceAccount에서 자동으로 결정된다. Pod spec에 `serviceAccountName`을 명시하지 않으면 `default` ServiceAccount가 사용되어 `spiffe://cluster.local/ns/{ns}/sa/default` ID를 갖는다.

**VM의 SPIFFE ID**는 WorkloadEntry의 `serviceAccount`와 `namespace` 필드로 결정된다. VM에 실제로 K8s ServiceAccount가 존재하지 않아도 된다. istiod가 그 이름의 SPIFFE ID를 가진 인증서를 발급하는 것이다. 이 점이 핵심 차이다. VM의 SPIFFE ID는 실제 K8s 권한 체계와 분리되어 있으므로, WorkloadEntry를 잘못 구성하면 VM이 의도하지 않은 서비스 계정 이름의 ID를 갖게 된다.

**AuthorizationPolicy 작성 시 주의점**은 세 가지다.

첫째, **`serviceAccount` 필드 존재 여부 확인**이다. WorkloadEntry에 `serviceAccount`를 명시하지 않으면 VM의 SPIFFE ID가 예측 불가능한 형태가 된다. AuthorizationPolicy에서 principals로 VM을 정확히 식별하려면 WorkloadEntry에 반드시 `serviceAccount`를 명시해야 한다.

```yaml
# AuthorizationPolicy에서 VM을 source로 지정
spec:
  rules:
  - from:
    - source:
        principals:
        - "cluster.local/ns/production/sa/legacy-api-sa"
```

둘째, **namespace가 SPIFFE ID에 포함된다는 점**이다. 같은 `legacy-api-sa` 이름이라도 `production` namespace와 `staging` namespace의 VM은 다른 SPIFFE ID를 갖는다. AuthorizationPolicy에서 namespace를 포함한 전체 principal을 명시해야 한다.

셋째, **멀티클러스터 환경에서 trust domain 차이**다. 클러스터 간 신뢰가 설정되지 않은 환경에서는 다른 클러스터의 VM SPIFFE ID가 `spiffe://cluster.local/...`이 아닌 별도의 trust domain을 가질 수 있다. 멀티클러스터 설정 시 trust domain을 통일(`meshConfig.trustDomain`)하거나, `principals` 대신 `namespaces`나 `ipBlocks`를 사용하는 것을 검토한다.

VM과 Pod에 동일한 serviceAccount 이름을 부여하면 AuthorizationPolicy에서 둘을 동일하게 취급할 수 있다. 이것은 때로 유용하지만, VM이 침해됐을 때 Pod와 동일한 접근 권한을 갖게 되는 위험도 있다.

### 실무 적용

VM과 Pod를 구분해서 정책을 적용하려면 서비스 계정 이름에 의미 있는 구분자를 사용하는 것이 좋다.

```yaml
# VM 전용 서비스 계정 (별도 네이밍)
# WorkloadEntry
serviceAccount: legacy-api-vm-sa

# Pod 서비스 계정
serviceAccountName: legacy-api-pod-sa

# AuthorizationPolicy에서 VM만 허용하는 경우
rules:
- from:
  - source:
      principals:
      - "cluster.local/ns/production/sa/legacy-api-vm-sa"
```

VM의 현재 SPIFFE ID를 확인하려면 VM에서 다음 명령으로 발급된 인증서의 SAN을 확인한다.

```bash
openssl x509 -in /etc/certs/cert-chain.pem -noout -text | grep "URI:"
# 출력: URI:spiffe://cluster.local/ns/production/sa/legacy-api-sa
```

---

## Q5. 멀티클라우드 환경(AWS EC2 + GKE)에서 VM 통합 시 네트워크 설계 고려사항은?

### 왜 중요한가?

VM 통합에서 가장 복잡한 시나리오는 VM과 K8s 클러스터가 서로 다른 클라우드 또는 네트워크에 있는 경우다. AWS EC2의 VM이 GKE 클러스터의 Istio 메시에 참여하려면 단순히 istiod에 연결하는 것 이상의 네트워크 설계가 필요하다. 이 구조를 잘못 설계하면 mTLS 연결이 불가능하거나 East-West 트래픽 비용이 예상을 초과한다.

### 분석

**네트워크 연결성 요구사항**이 첫 번째 고려사항이다. VM에서 istiod(GKE)의 15012 포트에 도달할 수 있어야 한다. 직접 연결이 없다면 East-West Gateway를 통해 라우팅한다. East-West Gateway는 클러스터 외부에서 istiod와 Pod에 접근하는 진입점 역할을 한다.

```yaml
# East-West Gateway 서비스 (외부 접근 허용)
apiVersion: v1
kind: Service
metadata:
  name: istio-eastwestgateway
  namespace: istio-system
spec:
  type: LoadBalancer
  ports:
  - port: 15012     # istiod xDS
    name: tls-istiod
  - port: 15443     # mTLS 터널
    name: tls
```

AWS EC2에서 GKE의 East-West Gateway IP로 15012 포트에 접근할 수 있으면 된다. `cluster.env`의 `ISTIO_PILOT_PORT`를 East-West Gateway의 외부 IP로 설정한다.

**IP 주소 충돌 방지**가 두 번째 고려사항이다. AWS VPC의 Pod CIDR이 GKE 클러스터의 Pod CIDR과 겹치면 라우팅 오류가 발생한다. 멀티클라우드 환경에서는 각 네트워크의 IP 대역을 설계 단계부터 분리해야 한다. Istio의 멀티네트워크(multi-network) 설정을 사용하면 네트워크 간 트래픽은 Gateway를 통해 라우팅되어 직접 IP 라우팅이 필요 없다.

**WorkloadEntry의 `network` 필드**가 멀티네트워크 설정의 핵심이다. AWS EC2의 VM을 `aws-us-east-1` 네트워크로 선언하고, GKE 클러스터를 `gke-us-central1` 네트워크로 설정하면, Istio가 서로 다른 네트워크 간 트래픽은 자동으로 East-West Gateway를 통해 라우팅한다.

```yaml
apiVersion: networking.istio.io/v1beta1
kind: WorkloadEntry
metadata:
  name: aws-legacy-api
  namespace: production
spec:
  address: "10.0.1.100"       # AWS EC2 내부 IP
  network: aws-us-east-1      # 네트워크 식별자
  labels:
    app: legacy-api
  serviceAccount: legacy-api-sa
```

**레이턴시와 비용**이 세 번째 고려사항이다. AWS EC2와 GKE Pod 간 모든 요청이 인터클라우드 네트워크를 통과하면 레이턴시가 50~200ms 증가할 수 있다. 또한 클라우드 간 egress 트래픽 비용이 발생한다. 이를 최소화하려면 VM이 자주 호출하는 서비스는 VM과 동일한 클라우드로 이전하거나, ServiceMirror(멀티클러스터)를 통해 GKE 서비스를 AWS에 미러링하는 구조를 검토한다.

**DNS 해석 경로**도 고려해야 한다. VM의 DNS Proxy가 `*.svc.cluster.local` 쿼리를 istiod에서 받은 서비스 레지스트리로 해석한다. 멀티네트워크 환경에서 VM이 K8s 서비스를 DNS로 호출할 때, DNS Proxy가 반환하는 IP는 직접 연결 가능한 실제 Pod IP가 아니라 가상 IP일 수 있다. 이 트래픽은 Envoy가 처리하면서 East-West Gateway를 통해 목적지 Pod로 전달된다.

### 실무 적용

멀티클라우드 VM 통합 설계의 검증 순서는 다음과 같다.

1. East-West Gateway 외부 IP 확인: `kubectl get svc istio-eastwestgateway -n istio-system`
2. AWS EC2에서 연결 가능 여부 확인: `nc -zv <east-west-gw-ip> 15012`
3. `cluster.env`에 East-West Gateway IP 설정
4. VM 온보딩 후 istiod 연결 확인: `journalctl -u istio | grep "Connected to"`
5. K8s Pod에서 VM으로 요청 테스트: `kubectl exec -it <pod> -- curl http://legacy-api.production.svc.cluster.local:8080/health`
6. VM에서 K8s 서비스 호출 테스트: `curl http://payment-svc.payments.svc.cluster.local:8080/health`

인터클라우드 레이턴시가 허용 범위를 초과한다면 VM을 K8s 클러스터와 동일한 클라우드로 이전하거나, 프로세스를 컨테이너화하는 것이 근본적인 해결책이다. VM 통합은 마이그레이션 과도기의 임시 구조로 보는 것이 장기적으로 건전한 접근이다.

---

## Q6. VM 워크로드를 Ambient 모드로 전환하는 로드맵과 현재 제약은?

### 왜 중요한가?

Ambient 모드는 사이드카 없이 메시 기능을 제공하는 Istio의 새로운 아키텍처다. VM 환경에서 사이드카를 수동으로 설치하고 관리하는 부담을 없애줄 수 있다는 점에서 기대가 높지만, 2024~2025년 기준으로 VM에 대한 Ambient 지원은 아직 GA 단계가 아니다. 이 제약을 파악하지 않으면 잘못된 시점에 전환을 시도하거나, 현재 sidecar 기반 구조를 조기에 폐기하는 실수를 범한다.

### 분석

**Ambient 모드의 기본 구조**는 ztunnel과 waypoint proxy로 구성된다. ztunnel은 각 K8s 노드에 DaemonSet으로 배포되어 L4 mTLS 터널을 처리한다. waypoint proxy는 L7 정책이 필요한 서비스를 위한 선택적 컴포넌트다. Pod는 사이드카 없이 ztunnel의 eBPF 기반 트래픽 가로채기를 통해 메시에 참여한다.

**VM에서 ztunnel의 문제**는 구조적이다. ztunnel은 K8s 노드의 커널 네임스페이스와 긴밀하게 통합되어 eBPF 프로그램으로 트래픽을 가로챈다. VM은 K8s 노드가 아니므로 ztunnel DaemonSet이 VM에 배포되지 않는다. VM에 ztunnel 바이너리를 독립 실행 모드로 설치하는 방안이 Istio 커뮤니티에서 논의되고 있지만, K8s API와의 통합, 인증서 프로비저닝, 헬스체크 등 여러 부분을 별도로 처리해야 하는 복잡성이 있다.

**현재 공식 지원 상태**(Istio 1.21 기준)는 다음과 같다. ztunnel의 독립 실행 모드는 실험적 기능으로 문서화되어 있다. waypoint proxy를 통한 L7 정책(AuthorizationPolicy, HTTP route)은 VM에 적용되지 않는다. Ambient 모드의 VM 지원은 "Beta" 이전 단계다.

**실용적인 전환 로드맵**은 단계적 접근이다. 첫 번째 단계는 K8s Pod를 sidecar에서 Ambient로 전환하는 것이다. VM은 여전히 sidecar를 사용하면서 Ambient 메시의 Pod와 통신할 수 있다. 두 번째 단계는 Ambient의 VM 지원이 GA가 되는 시점에 VM을 전환하는 것이다. 단계적 전환이 가능한 이유는 Ambient Pod와 sidecar VM 간의 mTLS 통신이 이미 지원되기 때문이다.

```
현재 상태:
VM (sidecar) ←mTLS→ Pod (sidecar)  지원됨
VM (sidecar) ←mTLS→ Pod (Ambient)  지원됨
VM (ztunnel) ←→ Pod (Ambient)      실험적

전환 목표:
VM (ztunnel or Ambient) ←→ Pod (Ambient)  GA 대기 중
```

VM과 함께 Ambient 전환을 계획하는 팀은 Istio 릴리즈 노트에서 "VM support in Ambient mode" 항목을 주기적으로 확인하는 것이 가장 정확한 정보 소스다.

### 실무 적용

현재 VM이 sidecar 기반으로 운영 중인 환경에서 향후 Ambient 전환을 준비하는 접근은 다음과 같다.

**단기 (현재)**: sidecar 기반 VM 통합을 유지하고, K8s Pod만 Ambient로 전환을 시작한다. VM과 Ambient Pod 간 통신을 먼저 검증한다.

**중기 (Ambient VM GA 후)**: 비중요 VM부터 ztunnel 설치 파일럿 테스트를 진행한다. L4 전용 요구사항인지 L7 정책(waypoint)도 필요한지에 따라 전환 복잡도가 달라진다.

**VM 마이그레이션 우선 고려**: Ambient 전환 이전에 VM 워크로드를 컨테이너화할 수 있는지 검토하는 것이 장기적으로 운영 비용을 낮춘다. 컨테이너화 가능한 워크로드라면 VM 통합보다 K8s 마이그레이션이 더 깔끔한 해결책이다.

Ambient 모드의 VM 지원 GA 이전에 ztunnel을 프로덕션 VM에 적용하는 것은 권장하지 않는다. sidecar 기반 VM 통합을 안정적으로 운영하면서 Istio 로드맵을 모니터링하는 것이 현실적인 전략이다.
