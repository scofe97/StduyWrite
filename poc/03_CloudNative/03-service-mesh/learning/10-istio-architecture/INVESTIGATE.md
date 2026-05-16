<!-- migrated: write/09_cloud/service-mesh/deepdive/10-01.Istio 아키텍처 실습.md (2026-04-19) -->

# Ch10. Istio 아키텍처 — Deep Dive Questions

## Q1. istiod 모놀리식 전환은 실제로 안전한가? Mixer 시절과 비교했을 때 장애 폭발 반경은 줄었을까?

### 왜 중요한가?
Istio 1.5에서 Pilot, Citadel, Galley, Mixer를 하나의 istiod 프로세스로 통합한 결정은 운영 단순화를 목표로 했다. 그런데 모놀리식 설계는 "단일 장애점"이라는 전통적인 비판을 받는다. 분산 컴포넌트였던 Mixer 아키텍처와 통합된 istiod 중 어느 쪽이 실제 프로덕션에서 더 안전한지 판단하려면, 장애 모드를 구체적으로 비교해야 한다.

Mixer는 각 요청마다 동기 RPC 호출을 수행했다. Envoy 사이드카가 Mixer에 check와 report 요청을 보내야 했으므로, Mixer가 느려지거나 다운되면 데이터 플레인 전체가 영향을 받았다. 반면 istiod는 컨트롤 플레인에만 위치하고, Envoy는 xDS로 받은 설정을 캐싱해 데이터 플레인을 독립적으로 운영한다.

### 분석
istiod 장애 시나리오를 구체적으로 살펴보면, 기존 Envoy 인스턴스는 마지막으로 수신한 xDS 설정을 메모리에 유지한 채 트래픽을 계속 처리한다. 새 Pod 스케줄링이나 인증서 갱신(기본 24시간 주기)은 istiod 복구 전까지 중단되지만, 기존 서비스 간 통신은 유지된다. 이것이 Mixer 아키텍처와의 핵심 차이다. Mixer가 다운되면 check 호출이 실패하므로 fail-close 정책에서는 요청 자체가 거부됐다.

모놀리식 istiod의 실질적 위험은 단일 컴포넌트 장애보다 메모리 누수나 CPU 폭증 같은 성능 저하다. 대규모 클러스터에서 서비스 수가 수천 개에 달하면, istiod는 모든 xDS 구독자에게 설정 변경을 푸시하면서 CPU 스파이크가 발생한다. 이때 istiod가 OOMKilled되면 전체 컨트롤 플레인이 순간 마비된다. Mixer 시절에는 컴포넌트별로 스케일링이 가능했지만, istiod는 수평 확장 시 모든 기능이 함께 복제된다.

그럼에도 istiod의 복원성이 Mixer보다 높다고 평가받는 이유는 데이터 플레인 분리 때문이다. Mixer의 동기 호출 모델은 컨트롤 플레인 성능이 데이터 플레인 레이턴시에 직접 반영됐다. istiod는 비동기 푸시 모델로 설계되어, 컨트롤 플레인이 느려도 기존 트래픽에는 영향을 주지 않는다.

### 실무 적용
프로덕션에서는 istiod를 단일 Replica로 운영하지 말고, `replicaCount: 3` 이상으로 설정하고 PodAntiAffinity로 노드를 분산시켜야 한다. istiod의 메모리 사용량을 Prometheus로 모니터링하고, `pilot_xds_push_time` 메트릭이 5초를 초과하면 설정 변경이 너무 자주 발생하고 있다는 신호로 봐야 한다. HPA보다 VPA가 istiod에 더 적합한데, xDS 구독자 수는 급격히 변하지 않으나 클러스터 규모에 따라 메모리 요구량이 선형 증가하기 때문이다.

---

## Q2. Envoy WASM 필터를 프로덕션에 도입하면 어떤 보안 경계가 생기고, 어떤 위협이 새로 열리는가?

### 왜 중요한가?
WASM(WebAssembly) 필터는 Envoy의 기능을 Lua나 C++ 네이티브 코드 없이 확장할 수 있게 해준다. Rust나 Go로 작성한 필터를 OCI 이미지로 배포하거나, `WasmPlugin` CRD로 동적으로 로드할 수 있다. 그런데 "샌드박스 안에서 실행된다"는 설명만으로 보안을 충분히 이해했다고 말하기 어렵다. WASM 샌드박스가 실제로 무엇을 격리하고 무엇을 격리하지 않는지 명확히 알아야 한다.

### 분석
WASM 모듈은 선형 메모리 모델 안에서 실행되므로, 모듈 간 메모리 접근은 원천적으로 차단된다. 네트워크 소켓 접근이나 파일 시스템 접근도 호스트 API를 통해서만 가능하고, Envoy의 proxy-wasm ABI가 허용한 작업만 수행할 수 있다. 이 격리는 실제로 강력하다.

그러나 WASM 필터가 열 수 있는 위협도 분명히 존재한다. 첫째, 필터 로드 경로 문제다. `WasmPlugin`이 원격 URL에서 이미지를 pull할 때, 그 레지스트리가 신뢰할 수 있는지 검증하지 않으면 악성 필터가 로드될 수 있다. OCI 다이제스트를 사용해 이미지 무결성을 고정하는 것이 필수다. 둘째, CPU/메모리 소비 공격이다. WASM 모듈은 CPU 집약적 연산을 무한 루프로 실행할 수 있고, Envoy 워커 스레드를 고갈시켜 서비스 거부를 유발할 수 있다. Envoy는 WASM 모듈당 실행 시간 제한을 설정할 수 있지만 기본값이 넉넉하지 않다. 셋째, 호스트 함수 오남용이다. `proxy_http_call`을 통해 외부 서비스를 호출하는 필터는 사이드 채널로 데이터를 유출할 수 있다. 필터가 어떤 호스트 함수를 사용하는지 소스 수준에서 감사해야 한다.

WASM 런타임 자체의 취약점도 고려 대상이다. Envoy는 V8 기반 WASM 런타임을 사용하는데, V8에서 발견된 취약점이 샌드박스 탈출로 이어질 가능성이 있다. Wasmtime 런타임 옵션을 사용하는 경우 보안 특성이 다르다.

### 실무 적용
WASM 필터 도입 시 체크리스트: (1) 이미지 다이제스트 고정 (`sha256:...`), (2) 프라이빗 레지스트리 사용 및 접근 제어, (3) 필터 소스 코드 보안 감사 (외부 호출, 메모리 할당 패턴), (4) `failStrategy: FAIL_OPEN` vs `FAIL_CLOSED` 결정 — 필터 로드 실패 시 트래픽을 허용할지 차단할지, (5) 스테이징 환경에서 부하 테스트로 CPU 영향 측정.

---

## Q3. xDS 푸시 확장성 한계는 어디인가? 클러스터가 성장하면서 istiod가 병목이 되는 지점을 어떻게 예측할 수 있는가?

### 왜 중요한가?
xDS(Envoy Discovery Service) 프로토콜은 istiod가 모든 Envoy 프록시에게 설정을 스트리밍하는 메커니즘이다. 클러스터에 Envoy 인스턴스가 수백 개일 때는 문제가 없지만, 수천 개 Pod가 있고 서비스 설정이 자주 변경된다면 istiod의 xDS 푸시 부하가 병목으로 작용한다. 이 한계를 사전에 예측하지 못하면, 클러스터 성장 중 갑작스러운 컨트롤 플레인 장애를 맞이하게 된다.

### 분석
xDS 푸시 부하를 결정하는 세 가지 변수가 있다: (1) Envoy 인스턴스 수, (2) 서비스/엔드포인트 수, (3) 설정 변경 빈도. istiod는 설정 변경이 발생하면 관련된 모든 Envoy에 업데이트를 보내야 한다. Kubernetes Deployment 롤링 업데이트 중에는 엔드포인트가 지속적으로 변경되므로 EDS(Endpoint Discovery Service) 푸시가 폭증한다.

`pilot_xds_pushes` 메트릭과 `pilot_xds_push_time` 메트릭을 함께 보면 병목 징후를 파악할 수 있다. 푸시 시간이 증가하면서 큐에 대기 중인 푸시(`pilot_xds_pending_push_full`)가 쌓인다면, istiod가 푸시 속도보다 빠르게 이벤트를 받고 있다는 신호다. 이때 istiod의 CPU가 제한에 걸려 있는지 확인하는 것이 첫 번째 단계다.

Istio는 델타 xDS(Incremental xDS)를 지원하기 시작했다. 전체 설정을 매번 전송하는 State of the World 방식 대신, 변경된 리소스만 전송하므로 대규모 클러스터에서 대역폭과 처리 시간을 크게 줄인다. `PILOT_ENABLE_INCREMENTAL_PUSH=true` 환경변수로 활성화할 수 있는데, Istio 1.21 이후 기본값이 되었다. 또한 `PILOT_PUSH_THROTTLE` 설정으로 초당 최대 푸시 수를 제한할 수 있다. 이는 폭풍처럼 쏟아지는 이벤트로 인한 istiod CPU 폭증을 방어하는 배압(backpressure) 역할을 한다.

istiod 수평 확장은 단순히 Replica를 늘리는 것으로 해결되지 않는다. 각 istiod 인스턴스는 연결된 Envoy 전체를 담당해야 하므로, 실질적인 분산은 Kubernetes leader election을 통한 부하 분배로 이루어진다. `PILOT_ENABLE_LEADER_ELECTION=true` 설정과 함께 istiod가 여러 인스턴스를 운영하면, xDS 연결이 인스턴스 간에 분산된다.

### 실무 적용
클러스터 규모 계획 시 경험적 수치로 istiod 인스턴스당 약 1,000개 Envoy 연결을 안전한 상한으로 볼 수 있다. 다만 서비스 수와 변경 빈도에 따라 이 수치는 달라진다. 사전 부하 테스트로 `pilot_xds_push_time`의 99퍼센타일이 10초를 초과하는 시점을 찾는 것이 현실적인 한계 측정 방법이다. 네임스페이스별로 `exportTo`를 사용해 서비스 가시성 범위를 제한하면, 각 Envoy가 수신하는 설정 크기를 줄여 푸시 효율을 높일 수 있다.

---

## Q4. CRD 증식(sprawl) 문제를 어떻게 관리할 것인가? Istio CRD가 수십 개에 달할 때 운영 복잡도는 어떻게 제어하는가?

### 왜 중요한가?
Istio는 VirtualService, DestinationRule, Gateway, ServiceEntry, Sidecar, AuthorizationPolicy, PeerAuthentication, RequestAuthentication, EnvoyFilter, WasmPlugin, Telemetry, ProxyConfig 등 12개 이상의 CRD를 정의한다. 각 CRD는 독자적인 스펙을 갖고, 여러 CRD가 상호작용하면서 최종 Envoy 설정을 만들어낸다. 이 복잡도는 "설정이 어디서 오는가"를 추적하기 어렵게 만들고, 의도치 않은 설정 충돌을 유발한다.

### 분석
CRD 증식의 첫 번째 문제는 충돌 감지의 어려움이다. 동일 호스트에 대해 여러 VirtualService가 존재할 때, Istio는 병합 규칙에 따라 처리하지만 그 결과가 직관적이지 않다. `istioctl analyze` 명령이 충돌을 일부 감지하지만 모든 경우를 잡아내지 못한다. Kiali는 CRD 간 의존성을 그래프로 시각화하므로 관계 파악에 유용하다.

두 번째 문제는 네임스페이스 격리와 클러스터 전체 범위의 혼재다. Gateway는 클러스터 전체에 영향을 미치지만, VirtualService는 특정 네임스페이스에 바인딩된다. 팀마다 자체 VirtualService를 작성하면 충돌 없이 공존할 수 있지만, 공유 Gateway를 수정하면 다른 팀에 영향을 줄 수 있다. 이를 관리하기 위해 Gateway를 인프라 팀이 전담하고, 애플리케이션 팀은 VirtualService와 DestinationRule만 관리하는 역할 분리가 일반적이다.

세 번째 문제는 EnvoyFilter의 위험성이다. EnvoyFilter는 Envoy 설정을 직접 패치하는 탈출구(escape hatch)로, Istio 추상화를 우회한다. 강력하지만 Istio 버전 업그레이드 시 xDS API 변경으로 인해 EnvoyFilter가 실패하거나 예상치 못한 동작을 일으킬 수 있다. EnvoyFilter 사용 목록을 별도로 관리하고, 업그레이드 전 각 필터의 호환성을 검증해야 한다.

GitOps 접근법이 CRD 증식 관리에 효과적이다. 모든 Istio CRD를 Git 저장소에서 관리하면 변경 이력이 남고, PR 기반 검토로 충돌을 사전에 발견할 수 있다. `istioctl analyze --recursive` 를 CI 파이프라인에 포함시켜 변경 전 검증을 자동화하는 것이 권장 패턴이다.

### 실무 적용
팀 규모가 커질수록 CRD 소유권을 명확히 해야 한다. Kubernetes RBAC을 활용해 애플리케이션 팀은 자신의 네임스페이스 VirtualService와 DestinationRule만 수정할 수 있게 제한하고, Gateway와 PeerAuthentication은 플랫폼 팀만 관리하도록 분리하는 것이 현실적이다. `Sidecar` CRD를 사용해 각 서비스가 실제로 통신하는 서비스만 xDS 구독하도록 범위를 좁히면, 설정 복잡도와 istiod 부하를 동시에 줄일 수 있다.

---

## Q5. Istio와 Linkerd의 아키텍처 선택이 실제 운영 비용에 어떤 차이를 만드는가?

### 왜 중요한가?
Istio와 Linkerd는 서비스 메시의 두 대표 구현체인데, 설계 철학이 근본적으로 다르다. Istio는 Envoy를 사이드카로 사용하는 범용 프록시 접근법을 택했고, Linkerd는 Rust로 작성한 경량 마이크로프록시(linkerd2-proxy)를 사용한다. 이 선택이 리소스 사용량, 디버깅 용이성, 운영 부담에 어떤 구체적인 차이를 만드는지 파악해야 올바른 도구 선택이 가능하다.

### 분석
사이드카 리소스 비용 차이가 가장 눈에 띄는 지점이다. Envoy 프록시는 일반적으로 사이드카당 약 50-100MB 메모리를 사용하고, 설정 규모에 따라 증가한다. linkerd2-proxy는 약 10-20MB 수준으로 알려져 있다. Pod 수백 개 규모에서 이 차이는 상당한 인프라 비용으로 이어진다. CPU 오버헤드도 비슷한 패턴을 보이는데, Envoy는 더 많은 기능을 수행하는 만큼 CPU 사용량도 높다.

기능 범위에서 Istio가 Linkerd를 크게 앞선다. Istio는 트래픽 관리(VirtualService, DestinationRule), 세밀한 인가 정책, WASM 확장, 외부 인증 통합 등을 제공한다. Linkerd는 기본 mTLS, 트래픽 분할, 레이턴시 인식 부하 분산, 자동 재시도에 집중하고 고급 트래픽 관리는 SMI(Service Mesh Interface) 확장에 의존한다. 기능이 풍부할수록 운영 복잡도가 올라간다는 트레이드오프가 있다.

디버깅 경험도 다르다. Istio는 `istioctl proxy-config` 명령으로 Envoy 설정의 모든 세부 사항을 들여다볼 수 있고, Envoy admin 인터페이스도 접근 가능하다. 반면 linkerd2-proxy는 관찰성은 뛰어나지만 내부 설정을 직접 조회하는 도구가 제한적이다. Istio 디버깅은 "Envoy를 이해해야 한다"는 선행 학습 비용이 있고, Linkerd는 "단순하지만 내부를 열어보기 어렵다"는 단점이 있다.

### 실무 적용
선택 기준을 명확히 하면 판단이 쉬워진다. 세밀한 트래픽 제어(카나리, 미러링, 헤더 기반 라우팅), 외부 인증 통합, 멀티 클러스터 고급 시나리오가 필요하다면 Istio가 적합하다. 빠른 도입, 낮은 리소스 오버헤드, mTLS와 기본 관측성으로 충분하다면 Linkerd가 더 나은 선택일 수 있다. 두 선택 모두 장기 운영 비용이 초기 구축 비용보다 크다는 점을 감안해 팀의 학습 역량과 유지보수 계획을 먼저 세워야 한다.

---

## Q6. Istio의 Sidecar CRD를 사용하지 않으면 어떤 성능 비용이 발생하는가?

### 왜 중요한가?
기본 설정에서 각 Envoy 사이드카는 메시 내의 모든 서비스에 대한 설정을 보유한다. 클러스터에 500개 서비스가 있다면, 각 사이드카가 500개 클러스터, 수천 개의 라우팅 규칙을 메모리에 유지한다. 실제로 특정 서비스가 통신하는 서비스는 그 중 일부에 불과한데도 불구하고. `Sidecar` CRD를 통한 범위 제한이 왜 대규모 클러스터에서 필수적인지 이해해야 한다.

### 분석
각 Envoy 인스턴스의 메모리 사용량은 보유한 설정 크기에 비례한다. 모든 서비스 설정을 유지하면 사이드카당 수백 MB에 달하는 경우도 있다. 이는 단순히 비용 문제가 아니라, 설정 로드 시간이 길어지고 xDS 업데이트 처리 시간도 증가한다는 의미다. 새 Pod가 시작되어 Envoy가 초기화될 때, 전체 설정을 수신하는 시간이 길수록 서비스가 트래픽을 받기까지 걸리는 시간이 늘어난다.

`Sidecar` CRD로 `egress.hosts`를 명시하면, Envoy는 해당 서비스에 대한 설정만 수신한다. 예를 들어 결제 서비스가 오직 `payment-db.payments.svc.cluster.local`과 `fraud-check.security.svc.cluster.local`에만 접근한다면, 이 두 서비스에 대한 설정만 유지하면 된다. 나머지 498개 서비스의 설정은 필요 없다. 이것은 네트워크 정책(NetworkPolicy)이 실제 연결을 차단하는 것과 달리, 설정 자체를 전달하지 않아서 리소스를 절약한다.

`Sidecar` CRD 도입 시 주의점이 있다. 설정하지 않은 서비스로 트래픽을 보내면 Envoy가 해당 클러스터를 모르므로 연결이 실패한다. 애플리케이션 의존성을 정확히 파악하지 못한 상태에서 적용하면 예상치 못한 연결 실패가 발생한다. `istioctl analyze`로 `Sidecar` 설정의 누락된 서비스를 탐지하거나, 기존 연결 패턴을 먼저 분석한 후 적용하는 것이 안전하다.

### 실무 적용
대규모 클러스터(서비스 100개 이상)에서는 `Sidecar` CRD 도입이 성능 튜닝 필수 항목이다. 서비스별 `Sidecar` 리소스를 수동으로 관리하는 것이 번거롭다면, 서비스 의존성 그래프를 코드에서 추출해 `Sidecar` 설정을 자동 생성하는 도구를 CI 파이프라인에 포함시킬 수 있다. 적용 효과는 `container_memory_working_set_bytes{container="istio-proxy"}`를 적용 전후로 비교하면 측정 가능하다.
