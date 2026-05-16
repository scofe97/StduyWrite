<!-- migrated:
  - write/09_cloud/service-mesh/deepdive/22-01.Istio Ambient Mesh 실습.md
  - write/09_cloud/service-mesh/deepdive/22-02.Istio Ambient Mesh 점검.md
  (2026-04-19) -->

# Ch22. Istio Ambient Mesh — Deep Dive Questions

## Q1. ztunnel DaemonSet 장애 시 폭발 반경(blast radius)은 어떻게 결정되는가?

### 왜 중요한가?
ztunnel은 각 노드에서 DaemonSet으로 실행되며, 해당 노드의 모든 ambient 모드 Pod 트래픽을 처리한다. 사이드카 모델에서는 개별 Pod의 프록시가 장애를 일으켜도 그 Pod에만 영향이 국한된다. 그런데 ztunnel이 장애를 일으키면 그 노드의 모든 ambient Pod가 동시에 영향을 받는다. 이 폭발 반경 차이를 명확히 이해해야 장애 시나리오에 적절히 대비할 수 있다.

### 분석
ztunnel 장애 모드를 분류하면 세 가지로 나눌 수 있다. 첫 번째는 완전 크래시(OOMKilled, panic)로, ztunnel 프로세스가 죽으면 노드의 모든 ambient Pod에서 인바운드/아웃바운드 L4 처리가 중단된다. Pod 자체는 살아있지만 메시 내 통신이 끊기는 상황이다. Kubernetes는 DaemonSet Pod를 자동으로 재시작하지만, 재시작 시간(수 초에서 수십 초) 동안 해당 노드의 서비스가 오류를 반환한다.

두 번째는 성능 저하(CPU 폭증, 높은 레이턴시)다. ztunnel이 죽지는 않지만 느려지면, 그 노드를 통과하는 모든 트래픽의 레이턴시가 함께 올라간다. 이 상황은 특히 탐지하기 어렵다. 노드 단위로 레이턴시 분포를 모니터링하지 않으면, 특정 노드의 Pod만 느린 이유를 파악하기 어렵다.

세 번째는 부분 기능 장애다. ztunnel의 HBONE 터널 처리는 정상이지만 인증서 갱신 로직에 버그가 있다면, 기존 연결은 유지되다가 인증서가 만료되는 시점에 일괄적으로 연결이 끊길 수 있다. 이런 시한폭탄형 장애는 발견이 늦다.

사이드카 모델과의 비교에서 눈여겨볼 점이 있다. 사이드카 크래시는 해당 Pod만 영향받고, Kubernetes가 사이드카 컨테이너를 재시작한다. ambient에서는 ztunnel 재시작이 완료되기 전까지 노드 전체가 영향을 받는다. 노드당 50개 Pod가 있다면, 사이드카 모델 대비 장애 영향 범위가 50배 확장된다.

### 실무 적용
ztunnel의 DaemonSet에 리소스 요청/제한을 명시적으로 설정하고, OOM을 방지하기 위해 메모리 제한을 충분히 여유 있게 잡아야 한다. `ztunnel_inbound_traffic_total` 메트릭을 노드별로 추적하여, 특정 노드의 트래픽이 갑자기 0으로 떨어지는 패턴을 알람으로 감지하는 것이 현실적인 모니터링 방법이다. 또한 중요 서비스는 여러 노드에 분산 배치(Pod Anti-Affinity)하여, 단일 ztunnel 장애로 서비스 전체가 다운되지 않도록 설계해야 한다.

---

## Q2. waypoint 프록시의 스케일링 전략은 어떻게 결정해야 하는가?

### 왜 중요한가?
ambient 모드에서 waypoint는 L7 처리를 담당하는 선택적 컴포넌트다. 모든 트래픽이 ztunnel을 통과하지만, L7 정책(헤더 기반 라우팅, 인가 정책, 재시도 등)을 적용하려면 waypoint를 통과해야 한다. waypoint는 네임스페이스 단위 또는 서비스 계정 단위로 배포할 수 있다. 이 스케일링 단위 선택이 성능과 격리에 미치는 영향을 이해해야 한다.

### 분석
네임스페이스 단위 waypoint는 단일 waypoint 인스턴스가 해당 네임스페이스의 모든 서비스로 향하는 L7 트래픽을 처리한다. 운영 단순성이 높고, 네임스페이스 내 정책을 한 곳에서 관리할 수 있다. 그러나 네임스페이스 내 한 서비스에 트래픽이 폭증하면 waypoint 전체가 영향을 받고, 다른 서비스도 레이턴시 증가를 경험한다. 이른바 "noisy neighbor" 문제가 waypoint 수준에서 발생한다.

서비스 계정 단위 waypoint는 서비스별 독립 waypoint를 배포한다. 장애 격리가 완벽하고 서비스별 독립적 스케일링이 가능하다. 그러나 Pod 수가 늘어나고 리소스 오버헤드가 증가한다. 10개 서비스가 있다면 10개 waypoint Deployment가 필요하고, 각각 HPA 설정과 리소스 요청을 관리해야 한다.

waypoint의 HPA 설정도 중요하다. waypoint는 Envoy 기반이므로 CPU 사용량이 트래픽 양에 비례한다. `targetCPUUtilizationPercentage: 70`으로 HPA를 설정하면 적절한 자동 스케일링이 가능하다. 그런데 waypoint Pod 수가 증가할 때 ztunnel이 새 waypoint 엔드포인트를 인식하는 데 지연이 있을 수 있으므로, 스케일아웃 시 초반에 레이턴시 스파이크가 발생할 수 있다.

waypoint와 사이드카의 L7 처리 비용 차이도 고려해야 한다. 사이드카 모델에서는 L7 처리가 각 Pod의 로컬 사이드카에서 수행되어 네트워크 홉이 없다. ambient 모드에서는 L7 처리를 위해 트래픽이 ztunnel → waypoint → ztunnel → 목적지 Pod 경로를 거친다. 이 추가 홉이 레이턴시에 얼마나 영향을 미치는지는 waypoint의 위치(소스 노드에 가까운지 목적지 노드에 가까운지)에 따라 달라진다.

### 실무 적용
초기 도입 시 네임스페이스 단위 waypoint로 시작하고, 트래픽 패턴을 분석한 후 noisy neighbor 문제가 발생하는 서비스를 서비스 계정 단위 waypoint로 분리하는 점진적 접근이 현실적이다. `istio_requests_total` 메트릭을 waypoint 인스턴스별로 모니터링하여, waypoint가 포화 상태에 가까워지는 시점을 사전에 탐지해야 한다.

---

## Q3. sidecar 모드에서 ambient 모드로 전환할 때 디버깅 가능성(debuggability)이 어떻게 변화하는가?

### 왜 중요한가?
사이드카 모델에서는 Envoy 프록시가 각 Pod에 붙어 있으므로, `kubectl exec -c istio-proxy` 로 해당 Pod의 프록시에 직접 접근하고, `istioctl proxy-config`로 설정을 확인하며, 액세스 로그를 Pod 로그에서 확인할 수 있다. ambient 모드에서는 이 익숙한 디버깅 패턴이 바뀐다. 어떻게 바뀌는지 파악하지 못하면 장애 대응 시간이 늘어난다.

### 분석
ambient 모드에서 L4 트래픽은 ztunnel이 처리하고, L7 트래픽은 waypoint가 처리한다. 특정 Pod의 트래픽을 디버깅하려면 해당 Pod가 아닌 ztunnel과 waypoint를 조사해야 한다. `istioctl ztunnel-config workload` 명령으로 ztunnel이 인식하는 워크로드 목록을 확인할 수 있고, `istioctl experimental ztunnel-config` 명령으로 ztunnel의 현재 설정을 확인할 수 있다. 이 명령들은 `istioctl proxy-config` 만큼 성숙하지 않아, 출력 형식이 불안정하거나 정보가 충분하지 않을 수 있다.

waypoint 디버깅은 Envoy 기반이므로 사이드카 디버깅과 유사하다. `kubectl exec -n <namespace> -c istio-proxy deployment/waypoint -- curl localhost:15000/config_dump` 명령으로 waypoint의 Envoy 설정을 확인할 수 있다. 그러나 특정 서비스에 대한 트래픽이 어떤 waypoint를 거쳐 가는지, 어떤 L7 정책이 적용됐는지를 추적하는 과정이 사이드카 모델보다 더 많은 단계를 필요로 한다.

tcpdump를 사용한 트래픽 캡처도 달라진다. 사이드카 모델에서는 Pod 네트워크 인터페이스에서 tcpdump를 실행하면 사이드카 전후 트래픽을 모두 볼 수 있었다. ambient 모드에서는 HBONE 터널 내부 트래픽이 암호화되어 있으므로, tcpdump로 내용을 확인하기 어렵다. ztunnel 자체의 로그에 의존해야 하는 경우가 많아진다.

Kiali는 ambient 모드를 지원하기 시작했지만, 사이드카 모드만큼의 세밀한 서비스 토폴로지 시각화는 아직 제한적인 경우가 있다. Ambient 모드에서 Kiali가 서비스 간 레이턴시와 에러율을 올바르게 표시하는지 확인이 필요하다.

### 실무 적용
ambient 모드 도입 시 팀의 디버깅 역량을 미리 강화해야 한다. `istioctl experimental ztunnel-config` 명령 패밀리를 익히고, ztunnel과 waypoint의 로그 레벨 조정 방법(`kubectl set env -n istio-system ds/ztunnel RUST_LOG=debug`)을 미리 문서화해 두는 것이 도움이 된다. 장애 대응 런북에 ambient 전용 디버깅 절차를 추가하여 인시던트 발생 시 당황하지 않도록 준비해야 한다.

---

## Q4. ambient 모드로 마이그레이션하면 안 되는 상황은 무엇인가?

### 왜 중요한가?
ambient 모드가 사이드카 모델의 리소스 오버헤드를 줄인다는 장점은 명확하다. 그러나 "항상 ambient가 낫다"는 결론은 잘못됐다. 특정 요구사항이나 기존 구성에 따라 사이드카 모드가 더 적합한 경우가 있다. 어떤 상황에서 ambient 전환을 보류하거나 포기해야 하는지 알아야 전환 결정의 품질이 높아진다.

### 분석
첫째, EnvoyFilter를 적극적으로 활용하는 경우다. 사이드카 모드에서는 각 Pod의 Envoy 프록시에 커스텀 필터를 직접 적용할 수 있다. ambient 모드의 ztunnel은 Rust로 작성된 단순한 L4 프록시로, Envoy 기반 확장이 불가능하다. L7 커스텀 필터는 waypoint에서만 적용 가능하다. 복잡한 EnvoyFilter나 WASM 필터를 사이드카에 적용하던 패턴을 그대로 ambient로 옮기기 어렵다.

둘째, 사이드카 컨테이너 인젝션에 의존하는 운영 도구가 있는 경우다. 일부 APM 에이전트나 보안 스캐너가 사이드카 패턴으로 배포되어 Envoy와 상호작용한다. ambient 모드에서는 `istio-proxy` 컨테이너가 없으므로, 이런 도구들이 동작하지 않거나 별도 조정이 필요하다.

셋째, 멀티 클러스터 환경에서 ClusterConfig 복잡도가 높은 경우다. ambient 모드의 멀티 클러스터 지원은 사이드카 모드보다 성숙도가 낮다. 특히 동일 네임스페이스를 여러 클러스터에 걸쳐 관리하는 패턴에서 ambient 모드의 동작이 예상과 다를 수 있다.

넷째, 세밀한 Pod 수준 격리가 필요한 경우다. ztunnel은 노드 수준에서 동작하므로, 멀티테넌트 환경에서 동일 노드의 서로 다른 테넌트 Pod 간 완전한 격리가 보장되는지 확인이 필요하다. 사이드카 모델에서는 각 Pod의 프록시가 완전히 분리되어 있었다.

다섯째, Istio 버전이 낮거나 CNI가 ambient를 지원하지 않는 경우다. ambient 모드는 특정 CNI(Calico, Cilium 등)와 호환성 문제가 있을 수 있고, 특정 커널 버전 이하에서 동작하지 않는다. 인프라 제약 조건을 먼저 확인해야 한다.

### 실무 적용
ambient 전환을 검토할 때 체크리스트를 작성해야 한다: (1) 기존 EnvoyFilter 목록과 용도, (2) 사이드카에 의존하는 사드파티 도구, (3) 현재 CNI 및 커널 버전 확인, (4) 멀티 클러스터 사용 여부, (5) 테넌트 격리 요구사항. 이 체크리스트에서 하나라도 막히면, 전환 전 Istio 로드맵과 커뮤니티 이슈를 확인하여 해결 가능 여부를 판단해야 한다. 점진적 전환(일부 네임스페이스만 ambient, 나머지는 사이드카)이 가능하므로 혼합 모드로 시작하는 것도 선택지다.

---

## Q5. ztunnel이 HBONE 터널 처리에 실패할 때 트래픽은 어떻게 되는가?

### 왜 중요한가?
HBONE(HTTP-Based Overlay Network Environment)은 ambient 모드에서 Pod 간 암호화 터널을 구성하는 프로토콜이다. ztunnel 간 mTLS 터널이 HBONE으로 설정된다. ztunnel이 HBONE 연결 수립에 실패하거나 기존 터널이 단절되면, 그 트래픽의 운명이 어떻게 되는지 명확히 알아야 장애 시 트래픽 손실 가능성을 평가할 수 있다.

### 분석
HBONE 터널 실패 모드는 연결 수립 실패와 기존 터널 단절 두 가지로 나뉜다. 연결 수립 실패는 목적지 ztunnel이 소스 ztunnel의 인증서를 검증하지 못했거나, 네트워크 정책으로 HBONE 포트(15008)가 차단된 경우에 발생한다. 이때 연결 시도 자체가 실패하고, 애플리케이션은 connection refused나 connection timeout을 받는다.

기존 터널이 단절되는 경우, ztunnel은 HTTP/2 스트림을 통해 이를 탐지하고 재연결을 시도한다. HTTP/2는 연결 유지 헬스 체크(PING 프레임)를 가지고 있어 터널 단절을 비교적 빠르게 감지한다. 재연결 시도 중 해당 터널을 사용하던 기존 요청은 실패한다. 이 실패를 애플리케이션이 재시도할 수 있는지는 애플리케이션 코드와 waypoint의 재시도 정책에 달려 있다.

ztunnel이 새 ztunnel과 HBONE 터널을 맺는 과정에서 인증서 검증이 핵심이다. 인증서가 만료됐거나 istiod에서 새 인증서를 받지 못한 상태라면, HBONE 터널 수립 자체가 불가능해진다. ztunnel은 인증서 만료 전 갱신을 시도하지만, istiod가 다운되어 갱신에 실패하면 인증서 만료 후 모든 HBONE 터널이 끊긴다. 기본 인증서 수명은 24시간이므로, istiod가 24시간 이상 다운되면 이 문제가 발생한다.

fail-open vs fail-close 동작도 중요하다. ztunnel은 기본적으로 HBONE 터널 수립 실패 시 평문(plaintext) 폴백을 허용하지 않는다. 이는 보안상 올바른 결정이지만, 장애 상황에서 트래픽 손실을 의미한다. 일부 서비스에서 잠시 평문 통신을 허용하고 싶다면, PeerAuthentication 정책을 `PERMISSIVE`로 설정하는 방법이 있지만 보안 수준이 낮아진다.

### 실무 적용
HBONE 포트(15008)가 네트워크 방화벽이나 NetworkPolicy에 의해 차단되지 않았는지 확인하는 것이 도입 전 필수 검증 항목이다. ztunnel 로그에서 `tunnel_failed`나 `connection_rejected` 패턴을 알람으로 설정하면 터널 장애를 빠르게 탐지할 수 있다. istiod 인증서 갱신 실패 알람(`citadel_server_csr_sign_error_count`)도 함께 설정해야 HBONE 터널 연쇄 장애를 예방할 수 있다.

---

## Q6. 멀티테넌트 환경에서 ambient 모드의 네임스페이스 격리는 충분한가?

### 왜 중요한가?
서로 다른 팀이나 고객의 워크로드가 동일 클러스터에서 실행되는 멀티테넌트 환경에서는 테넌트 간 격리가 보안의 핵심이다. 사이드카 모델에서는 각 Pod의 Envoy가 그 Pod의 트래픽만 처리하므로 격리가 명확했다. ambient 모드에서 ztunnel은 노드 전체 트래픽을 처리하므로, 테넌트 격리가 어떻게 보장되는지 구체적인 메커니즘을 이해해야 한다.

### 분석
ztunnel의 멀티테넌트 격리는 SPIFFE/SVID 기반 ID와 AuthorizationPolicy로 구현된다. 각 Pod는 서비스 계정에 기반한 SVID(SPIFFE Verifiable Identity Document)를 갖고, HBONE 터널은 이 ID를 사용해 mTLS를 수행한다. AuthorizationPolicy로 "tenant-a 워크로드는 tenant-b 워크로드에 접근 불가"를 명시하면, ztunnel 수준에서 L4 접근을 차단한다.

그러나 ztunnel이 단일 프로세스에서 여러 테넌트 트래픽을 처리하므로, 프로세스 수준 격리는 존재하지 않는다. 사이드카 모델에서는 테넌트별로 별도 Envoy 프로세스가 실행됐다. ztunnel 내부 버그로 인해 테넌트 A의 트래픽 처리 중 테넌트 B의 데이터에 접근하는 취약점이 이론적으로 가능하다. 이는 Rust의 메모리 안전성 덕분에 극히 낮은 위험이지만, 엄격한 규제 환경에서는 이 가능성 자체가 허용되지 않을 수 있다.

네임스페이스 수준 waypoint도 격리 경계가 된다. 서로 다른 테넌트가 각자의 네임스페이스에 waypoint를 운영하면, L7 처리가 테넌트별로 분리된다. 그러나 ztunnel은 공유되므로, L4 수준의 완전한 프로세스 격리는 달성할 수 없다.

규제 요구사항(PCI-DSS, HIPAA 등)이 있는 환경에서는 ambient 모드의 공유 ztunnel 아키텍처가 요구사항을 충족하는지 법률 및 컴플라이언스 팀과 먼저 확인해야 한다. 요구사항이 "프로세스 수준 격리"를 명시한다면 사이드카 모드가 더 적합할 수 있다.

### 실무 적용
멀티테넌트 ambient 환경에서는 AuthorizationPolicy를 `DENY` 기본 원칙으로 설정하고, 허용할 통신만 명시적으로 열어주는 화이트리스트 접근법을 사용해야 한다. 각 테넌트 네임스페이스에 `PeerAuthentication`을 `STRICT` mTLS로 강제하여, HBONE 터널 외의 통신을 원천 차단하는 것이 기본 보안 구성이다. 테넌트 간 격리 요구사항이 극도로 높다면, 테넌트별 노드 풀을 구성하여 ztunnel 자체를 물리적으로 분리하는 것이 가장 강력한 격리 방법이다.
