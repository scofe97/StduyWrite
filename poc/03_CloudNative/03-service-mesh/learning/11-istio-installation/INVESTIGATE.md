# Ch11. Istio 설치와 메시 구성 — Deep Dive Questions

## Q1. 리비전 기반 카나리 업그레이드에서 롤백이 예상대로 동작하지 않는 시나리오는 무엇인가?

### 왜 중요한가?
Istio의 리비전(revision) 메커니즘은 클러스터에 여러 Istio 버전을 공존시켜 점진적 업그레이드를 가능하게 한다. 네임스페이스에 `istio.io/rev=1-21` 레이블을 붙이면 해당 Istio 버전의 사이드카가 인젝션된다. 이론적으로 "문제가 생기면 레이블만 변경해 이전 버전으로 돌아간다"는 롤백이 가능해 보이지만, 실제로는 롤백이 의도대로 동작하지 않는 경우가 있다.

### 분석
리비전 변경 후 롤백의 핵심은 Pod 재시작이다. 네임스페이스 레이블을 이전 리비전으로 되돌려도, 기존에 실행 중인 Pod는 여전히 새 버전의 사이드카를 사용하고 있다. Pod를 재시작해야 이전 버전의 사이드카가 인젝션된다. 배포 롤링 재시작(`kubectl rollout restart deployment`) 전까지는 같은 Deployment 내에서 이전 버전과 새 버전 사이드카가 혼재한다.

혼재 상황에서의 호환성 문제가 실질적 위험이다. Istio 마이너 버전 간에는 xDS API 호환성이 보장되지만, 패치 버전 간에도 Envoy 필터 행동이 변경될 수 있다. 새 버전 사이드카가 처리한 요청이 이전 버전 사이드카를 통과할 때, 헤더나 메타데이터 형식 차이로 인해 예상치 못한 오류가 발생하는 경우가 있다. 특히 인증 헤더나 분산 추적 헤더 처리 방식이 다를 때 문제가 된다.

롤백이 더 복잡해지는 상황은 Istio CRD 스키마가 변경된 경우다. 새 Istio 버전에서 VirtualService나 AuthorizationPolicy 스펙이 변경되었다면, 새 버전에서만 동작하는 설정을 이미 적용한 상태에서 롤백하면 이전 버전이 그 설정을 인식하지 못해 오류를 발생시킨다. CRD는 클러스터 전체에 하나의 스키마만 존재하므로, "이전 CRD 버전으로 롤백"이 간단하지 않다.

istiod 리비전과 사이드카 리비전의 생명주기가 다르다는 점도 주의해야 한다. `istiod-1-21`과 `istiod-1-20`이 동시에 실행되는 동안, 각 istiod는 자신의 리비전을 사용하는 사이드카와만 통신한다. 이전 istiod를 너무 빨리 삭제하면, 아직 이전 리비전 사이드카를 사용하는 Pod들이 컨트롤 플레인을 잃는다.

### 실무 적용
롤백 절차를 미리 문서화하고 스테이징에서 검증해야 한다. 구체적으로: (1) 네임스페이스 레이블을 이전 리비전으로 변경, (2) Deployment를 롤링 재시작(`kubectl rollout restart`), (3) 모든 Pod의 사이드카 버전 확인(`kubectl get pods -o jsonpath='{.items[*].metadata.annotations.kubectl\.kubernetes\.io/last-applied-configuration}'`), (4) 이전 istiod 유지(삭제 시기는 모든 Pod 롤백 확인 후). 업그레이드 전 변경한 CRD 목록을 기록하고, 롤백 시 CRD 스키마 비호환성이 없는지 확인하는 단계가 필수다.

---

## Q2. ambient 모드와 sidecar 모드가 같은 클러스터에 공존할 때 발생하는 문제는 무엇인가?

### 왜 중요한가?
Istio는 동일 클러스터에서 ambient 모드와 sidecar 모드의 혼합 운영을 지원한다. 일부 네임스페이스는 `istio.io/dataplane-mode=ambient` 레이블로 ambient 모드로, 나머지는 사이드카 인젝션으로 설정할 수 있다. 이 혼합 구성이 가능하다는 것과, 실제로 예상대로 동작한다는 것은 다른 이야기다.

### 분석
ambient 네임스페이스의 Pod가 sidecar 네임스페이스의 Pod와 통신할 때 트래픽 경로가 복잡해진다. 소스(ambient) Pod에서 나온 트래픽은 ztunnel을 통해 HBONE으로 처리된다. 목적지(sidecar) Pod는 Envoy 사이드카가 있으므로, ztunnel은 HBONE 대신 일반 TCP로 목적지 Pod의 Envoy에 연결한다. 이 경계 처리 로직이 올바르게 동작하는지 확인이 필요하다.

mTLS 정책의 일관성이 문제가 될 수 있다. ambient 네임스페이스의 PeerAuthentication이 `STRICT`이고, sidecar 네임스페이스의 PeerAuthentication도 `STRICT`이면, 두 네임스페이스 간 통신은 올바르게 mTLS로 처리된다. 그러나 정책이 다르거나, 네임스페이스 경계에서 정책 적용 주체가 모호한 경우 예상치 못한 차단이 발생할 수 있다.

AuthorizationPolicy의 적용 방식도 확인이 필요하다. ambient 모드에서 AuthorizationPolicy는 ztunnel에서 적용되고, sidecar 모드에서는 각 Pod의 Envoy에서 적용된다. ambient Pod → sidecar Pod 방향 트래픽에 대한 Authorization 정책이 어느 쪽에서, 어떤 순서로 적용되는지 Istio 문서를 구체적으로 확인해야 한다.

telemetry 데이터 수집 방식의 차이도 혼합 환경에서 문제를 만들 수 있다. sidecar 모드에서는 각 사이드카가 Prometheus 메트릭을 노출하고, ambient 모드에서는 ztunnel과 waypoint가 메트릭을 노출한다. Prometheus 스크래핑 설정이 두 방식을 모두 커버하는지 확인해야 하고, 서비스 토폴로지를 시각화하는 Kiali가 혼합 환경을 올바르게 표시하는지도 검증해야 한다.

### 실무 적용
혼합 모드 구성은 이주 기간의 과도적 상태로만 사용하는 것이 권장된다. 장기 혼합 운영은 운영 복잡도를 높이고 디버깅을 어렵게 만든다. 혼합 환경 테스트는 반드시 스테이징에서 먼저 수행하고, ambient 네임스페이스와 sidecar 네임스페이스 간 통신 경로를 모두 테스트한 후 프로덕션에 적용해야 한다. 혼합 모드 이주는 명확한 완료 기한을 설정하고 진행해야 한다.

---

## Q3. IstioOperator CRD 지원 중단(deprecation) 후 Helm으로의 마이그레이션에서 무엇을 잃는가?

### 왜 중요한가?
Istio 커뮤니티는 `istioctl install`과 IstioOperator CRD 기반 설치에서 Helm 차트 기반 설치로의 전환을 권장하고 있다. IstioOperator는 설치 선언을 CRD로 관리하는 편리한 방법이었지만, 활발한 개발이 중단되고 Helm이 공식 설치 방법으로 자리잡았다. 이 전환에서 무엇을 잃고 무엇을 얻는지 파악해야 마이그레이션 결정을 내릴 수 있다.

### 분석
IstioOperator의 핵심 편의성은 단일 CRD에 설치 전체를 선언하고, `istioctl apply` 한 번으로 모든 컴포넌트(istiod, ingress gateway, egress gateway, CNI)를 설치/업그레이드할 수 있다는 점이다. Helm으로 전환하면 각 컴포넌트가 별도 Helm 차트(`istiod`, `gateway`, `cni`)가 되어, 순서에 맞게 각각 설치해야 한다. 이 점이 자동화 스크립트를 더 복잡하게 만든다.

IstioOperator가 제공하던 오버레이(overlay) 병합 기능도 Helm에서는 `values.yaml` 방식으로 대체된다. IstioOperator는 기본 설정 위에 사용자 정의를 계층적으로 덮어쓰는 방식이 직관적이었다. Helm values 파일 방식도 비슷한 결과를 낼 수 있지만, 어떤 설정이 어디서 오는지 추적하기가 더 어렵다.

Helm으로 전환하면서 얻는 것도 있다. Helm은 GitOps 도구(ArgoCD, Flux)와 더 잘 통합된다. ArgoCD에서 IstioOperator CRD를 관리하려면 별도 Application 리소스를 통한 간접 관리가 필요했지만, Helm 차트는 ArgoCD Application으로 직접 관리할 수 있다. `helm diff` 플러그인으로 업그레이드 전후 변경 사항을 미리 확인하는 것도 Helm의 장점이다.

마이그레이션 경로 자체의 위험도 있다. 기존 IstioOperator 기반 설치에서 Helm 기반 설치로 전환하는 과정은 설치 상태의 소유권을 변경하는 작업이다. `istioctl manifest generate`로 현재 설치의 Kubernetes 리소스를 추출하고, 이를 Helm 차트 values로 역변환하는 과정이 필요하다. 이 과정에서 설정이 누락될 위험이 있다.

### 실무 적용
마이그레이션은 새 클러스터를 Helm으로 구축한 후, 기존 클러스터에서 마이그레이션하는 순서로 진행하는 것이 안전하다. 기존 IstioOperator CRD 설정을 Helm values로 변환한 후, `helm template`으로 생성되는 Kubernetes 리소스를 `istioctl manifest generate`와 비교하여 차이점을 확인해야 한다. 프로덕션 마이그레이션 전 스테이징 환경에서 전체 마이그레이션 절차를 검증하는 것이 필수다.

---

## Q4. 프로덕션 Helm values 파일에서 반드시 명시적으로 결정해야 하는 설정은 무엇인가?

### 왜 중요한가?
Helm 차트의 기본값(default values)은 개발 환경이나 데모에 적합하게 설정되어 있다. 프로덕션에 그대로 사용하면 가용성, 성능, 보안 측면에서 문제가 생긴다. 어떤 기본값이 프로덕션에 부적합한지 알지 못하면, 나중에 장애로 발견하게 된다.

### 분석
가용성 측면에서 기본값이 단일 Replica인 컴포넌트를 확인해야 한다. istiod의 기본 `replicaCount: 1`은 프로덕션에서 사용하면 안 된다. 최소 2개, 고가용성 클러스터에서는 3개 이상을 권장하며, PodAntiAffinity로 다른 노드에 분산 배치해야 한다. ingress gateway도 마찬가지로 단일 Replica로 운영하면 게이트웨이 Pod 재시작 시 모든 인바운드 트래픽이 순간 차단된다.

리소스 요청/제한의 기본값도 재검토 대상이다. Helm 차트의 기본 리소스 값은 소규모 환경 기준으로 설정되어 있다. 프로덕션에서는 실제 부하 테스트를 통해 적절한 리소스 요청과 제한을 측정하고 명시해야 한다. 특히 리소스 제한(limits)을 요청(requests)보다 지나치게 높게 설정하면 OOMKilled가 발생해도 Kubernetes가 높은 우선순위를 부여할 수 있다.

글로벌 mTLS 설정도 기본값을 그대로 쓰면 안 된다. `meshConfig.defaultConfig.holdApplicationUntilProxyStarts: true` 설정은 istiod에 연결되기 전까지 애플리케이션 컨테이너 시작을 지연시켜, 사이드카가 완전히 준비되기 전 트래픽이 발생하는 문제를 방지한다. 기본값은 `false`인데, 사이드카가 초기화 중일 때 일부 요청이 프록시를 우회하는 현상이 발생할 수 있다.

프로파일 선택도 중요한 결정이다. Istio는 `default`, `demo`, `minimal`, `remote` 프로파일을 제공한다. `demo` 프로파일은 모든 기능을 활성화하고 제한 없는 리소스를 사용하므로 프로덕션에 절대 사용하면 안 된다. `minimal` 프로파일은 istiod만 설치하므로 ingress gateway를 별도로 설치해야 한다. `default` 프로파일이 일반적인 시작점이지만, 여기서도 가용성 설정은 반드시 재정의해야 한다.

### 실무 적용
프로덕션 values 파일 체크리스트: (1) `pilot.replicaCount: 3`, (2) `pilot.podAntiAffinityTermLabelSelector` 설정, (3) `gateways.istio-ingressgateway.replicaCount: 2` 이상, (4) `meshConfig.holdApplicationUntilProxyStarts: true`, (5) `global.proxy.resources` 명시 (측정값 기반), (6) `pilot.traceSampling: 1.0`을 프로덕션에서 낮춤 (1.0이면 100% 샘플링), (7) `global.defaultPodDisruptionBudget.enabled: true`. 이 체크리스트를 기반으로 팀의 프로덕션 values 파일 템플릿을 만들고, 새 클러스터 구축 시 재활용해야 한다.

---

## Q5. Calico나 Cilium 같은 CNI 플러그인과 Istio CNI(ambient 모드)가 충돌하는 경우는 언제인가?

### 왜 중요한가?
Istio의 ambient 모드는 트래픽 리다이렉션을 위해 독자적인 CNI 플러그인을 사용한다. 대부분의 Kubernetes 클러스터는 이미 Calico나 Cilium 같은 CNI 플러그인을 운영 중이다. 두 CNI 플러그인이 같은 클러스터에서 공존할 때, 네트워크 설정 충돌이 발생할 수 있다. 이 충돌이 무엇인지, 어떻게 해결할 수 있는지 이해해야 ambient 모드 도입이 가능한지 판단할 수 있다.

### 분析
CNI 플러그인 체인(chaining)이 핵심 메커니즘이다. Kubernetes는 여러 CNI 플러그인을 체인으로 구성할 수 있다. Istio CNI 플러그인은 iptables 규칙을 설정해 트래픽을 ztunnel로 리다이렉션하는 역할을 한다. Calico는 Pod 네트워킹과 NetworkPolicy를 담당한다. 두 플러그인이 체인으로 실행될 때, 순서가 중요하다. Istio CNI 플러그인은 Calico 이후에 실행되어야 Calico가 Pod 네트워크를 설정한 후 Istio가 트래픽을 가로챌 수 있다.

Cilium의 경우 eBPF 기반 네트워킹이 iptables와 충돌할 수 있다. Cilium은 기본적으로 iptables를 비활성화하고 eBPF로 모든 네트워킹을 처리한다. Istio ambient 모드는 ztunnel로의 트래픽 리다이렉션에 iptables를 사용했었으나, Istio 1.24 이후에는 eBPF 기반 리다이렉션도 지원하기 시작했다. Cilium과 함께 사용하려면 Istio의 CNI 모드를 eBPF로 설정하거나, Cilium의 iptables 모드(`kubeProxyReplacement: false`)를 사용해야 할 수 있다.

Calico의 eBPF 모드도 비슷한 충돌 가능성이 있다. Calico를 eBPF 모드로 운영 중이라면, Istio의 iptables 기반 리다이렉션이 예상대로 동작하지 않을 수 있다. Calico를 표준 iptables 모드로 사용하는 경우에는 일반적으로 문제가 없다.

cloud managed 환경의 CNI도 확인해야 한다. GKE의 Dataplane V2(Cilium 기반), EKS의 AWS VPC CNI, AKS의 Azure CNI는 각각 Istio CNI와의 호환성이 다르다. Managed Kubernetes 서비스를 사용한다면 해당 클라우드 공급자의 Istio 호환성 문서를 먼저 확인해야 한다.

### 실무 적용
CNI 호환성 검증은 ambient 모드 도입 전 필수 단계다. 스테이징 클러스터에서 동일 CNI 구성으로 Istio ambient 모드를 설치하고, `istioctl verify-install` 명령으로 설치 상태를 확인한다. Pod 간 통신 테스트로 트래픽 리다이렉션이 올바르게 동작하는지 검증하고, NetworkPolicy가 ambient 모드에서도 올바르게 적용되는지 별도로 테스트해야 한다. Cilium 사용 환경에서는 Cilium의 Istio 통합 가이드를 반드시 참고해야 한다.
