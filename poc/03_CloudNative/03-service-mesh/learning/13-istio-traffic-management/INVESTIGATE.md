# Ch13. Istio 트래픽 관리 — Deep Dive Questions

## Q1. VirtualService에서 Kubernetes Gateway API로 마이그레이션할 때 표현 불가능한 기능은 무엇인가?

### 왜 중요한가?
Kubernetes Gateway API는 Ingress를 대체하기 위해 설계된 차세대 트래픽 관리 API다. Istio도 VirtualService/DestinationRule 대신 Gateway API를 사용할 수 있다. 그러나 두 API가 표현하는 기능의 교집합이 완전하지 않다. Gateway API로 표현할 수 없는 VirtualService 기능이 있다면, 마이그레이션 전 이를 파악해야 이후의 기능 회귀를 예방할 수 있다.

### 분석
VirtualService의 `timeout`과 `retries` 설정은 Gateway API의 `HTTPRoute`에도 있지만, 세부 제어 수준이 다르다. VirtualService는 `retries.perTryTimeout`, `retries.retryOn` (특정 HTTP 상태 코드, connection failure 등 세밀한 조건), `retries.retryRemoteLocalities` 같은 세부 옵션을 제공한다. Gateway API의 `HTTPRoute`는 재시도 설정을 표준화하는 과정에 있지만, Istio 특화 재시도 조건들을 완전히 커버하지 못하는 경우가 있다.

`HTTPRoute`의 미러링(`mirrors`) 기능은 VirtualService의 `mirror` + `mirrorPercentage` 조합과 유사하지만, 미러링 비율 설정이 Gateway API 표준에 포함되지 않아 Istio 확장 어노테이션으로만 표현 가능한 경우가 있다. 이 경우 표준 Gateway API를 쓰면서 Istio 특화 어노테이션에 의존하게 되어, 다른 Gateway API 구현체로 이식 불가능한 설정이 생긴다.

fault injection은 VirtualService에서 강력한 테스트 도구다. `fault.abort`(특정 조건에서 요청 중단)와 `fault.delay`(레이턴시 주입)를 HTTP 헤더 기반 조건으로 세밀하게 제어할 수 있다. Gateway API 표준에는 fault injection이 포함되지 않았고, Istio는 이를 실험적 확장(`ExtensionRef`)으로만 제공한다. VirtualService의 fault injection을 사용하는 카오스 엔지니어링 파이프라인이 있다면, Gateway API 전환 후 이 기능을 어떻게 대체할지 별도로 계획해야 한다.

EnvoyFilter와의 통합도 확인이 필요하다. 기존에 VirtualService와 함께 EnvoyFilter를 사용해 특정 라우트에 커스텀 Envoy 설정을 적용했다면, Gateway API 전환 후 동일한 효과를 내는 방법이 달라질 수 있다. EnvoyFilter는 Istio 내부 xDS 설정 구조에 의존하므로, Gateway API로 전환하면 EnvoyFilter의 `applyTo` 대상이 바뀔 수 있다.

### 실무 적용
마이그레이션 전 현재 사용 중인 VirtualService 기능을 인벤토리화하는 것이 첫 단계다. `kubectl get virtualservice -A -o yaml`로 전체 VirtualService를 추출하고, fault injection, mirrorPercentage, 복잡한 retryOn 조건, EnvoyFilter 연계 패턴 등 Gateway API 표준에서 지원되지 않는 기능을 목록으로 만든다. 이 목록에서 대체 방법을 찾을 수 없는 기능이 있다면, 그 서비스는 마이그레이션 후 일정 기간 VirtualService로 남겨두는 혼합 전략을 고려해야 한다.

---

## Q2. 트래픽 미러링 중 데이터 일관성 문제가 발생할 수 있는 시나리오는 무엇인가?

### 왜 중요한가?
트래픽 미러링(shadowing)은 실시간 트래픽의 복사본을 그림자 서비스(shadow service)로 전송해, 프로덕션 영향 없이 새 버전을 검증하는 기법이다. "미러링은 안전하다"는 인식이 있지만, 데이터 변경 요청(POST, PUT, DELETE)을 미러링할 때 데이터베이스 상태 변경이 두 번 발생한다. 이 부작용을 관리하지 않으면 데이터 불일치나 의도치 않은 외부 시스템 호출이 발생한다.

### 分析
GET 요청 미러링은 일반적으로 안전하다. 읽기 전용 쿼리는 상태를 변경하지 않으므로, 그림자 서비스로 미러링해도 프로덕션 데이터에 영향이 없다. 그러나 GET 요청도 캐시 열화(cache thrashing)를 일으킬 수 있다. 프로덕션과 그림자 서비스가 동일 캐시 인프라를 공유한다면, 그림자 트래픽이 프로덕션 캐시를 오염시킬 수 있다.

POST/PUT/DELETE 미러링의 위험은 명확하다. 주문 생성 API를 미러링하면 그림자 서비스도 주문을 생성하려 시도한다. 그림자 서비스가 프로덕션과 별도 데이터베이스를 사용한다면 격리되지만, 같은 데이터베이스를 공유한다면 주문이 중복 생성된다. 외부 서비스 호출(이메일 발송, 결제 처리, SMS 발송)이 있다면, 그림자 서비스도 외부 서비스를 호출해 실제 결과를 만들 수 있다.

미러링 응답 처리도 이해해야 한다. Istio는 그림자 서비스의 응답을 클라이언트에 반환하지 않는다. 그림자 서비스의 오류는 무시된다. 그러나 그림자 서비스가 데이터베이스에 쓰기를 성공했다면, 그 데이터는 그림자 서비스의 스토리지에 남는다. 미러링 기간 동안 그림자 서비스의 데이터베이스는 지속적으로 늘어나고, 이 데이터를 주기적으로 정리하지 않으면 용량 문제가 발생한다.

`mirrorPercentage` 설정을 100% 이하로 낮추면 미러링으로 인한 부하를 줄일 수 있지만, 데이터 일관성 문제가 사라지지는 않는다. 50% 미러링이면 절반의 요청이 그림자 서비스를 수정하는 것은 동일하다.

### 실무 적용
미러링 사용 지침: (1) 읽기 전용 API는 미러링 적합, (2) 쓰기 API 미러링 시 그림자 서비스는 반드시 별도 데이터베이스 인스턴스 사용, (3) 외부 서비스 호출은 그림자 서비스 환경에서 mock/stub으로 교체, (4) 그림자 서비스 데이터베이스 정기 초기화 계획 수립, (5) 미러링 기간 동안 그림자 서비스의 오류율을 별도 모니터링하여 프로덕션과 동작 차이를 측정. 멱등성이 보장된 API만 선택적으로 미러링하는 것이 안전한 접근법이다.

---

## Q3. 지역성 인식 라우팅(locality-aware routing)이 의도대로 동작하지 않는 경우는 언제인가?

### 왜 중요한가?
지역성 인식 라우팅은 클라이언트와 같은 가용 영역(AZ) 또는 리전에 있는 서버 인스턴스를 우선 선택해 레이턴시를 줄이고 크로스 AZ 데이터 전송 비용을 낮추는 기능이다. 설정이 단순해 보이지만, 실제로 이 기능이 올바르게 동작하려면 여러 전제 조건이 충족되어야 한다. 전제 조건이 빠지면 지역성 인식 라우팅이 의도와 반대로 동작해 특정 AZ 과부하를 야기할 수 있다.

### 분析
지역성 인식 라우팅의 첫 번째 전제 조건은 엔드포인트에 지역성 레이블이 있어야 한다는 것이다. Kubernetes 노드에 `topology.kubernetes.io/region`과 `topology.kubernetes.io/zone` 레이블이 있어야 하고, Pod가 그 노드에서 실행될 때 Istio가 이 정보를 EDS에 반영한다. 노드에 토폴로지 레이블이 없으면, Envoy는 모든 엔드포인트를 동일 지역성으로 간주하고 라운드로빈으로 분산한다.

두 번째 전제 조건은 health check와 outlier detection이다. 지역성 인식 라우팅은 특정 지역의 엔드포인트가 건강하지 않을 때 다른 지역으로 spillover하는 메커니즘을 포함한다. 그러나 Envoy가 엔드포인트 건강 상태를 알려면 outlier detection이 설정되어 있어야 한다. `DestinationRule`의 `outlierDetection`이 없으면, 건강하지 않은 엔드포인트가 지역성 라우팅 대상에서 자동으로 제외되지 않을 수 있다.

엔드포인트 불균형 문제가 실제 운영에서 자주 발생한다. 3개 AZ에 Pod가 각각 1, 5, 10개 있다면, 같은 AZ 우선 라우팅 시 클라이언트가 있는 AZ에 따라 서비스 인스턴스 수가 크게 다르다. AZ-A에서 보내는 트래픽은 AZ-A의 1개 인스턴스에 집중되어 과부하가 걸리고, AZ-C의 10개 인스턴스는 같은 AZ 클라이언트가 적으면 노는 상황이 된다. 이를 방지하려면 가중치 기반 spillover 설정이 필요하다.

`localityLbSetting.distribute`를 사용하면 지역성 간 트래픽 분배 비율을 명시할 수 있다. 같은 AZ 80%, 다른 AZ 20%처럼 설정할 수 있다. 그러나 이 설정은 엔드포인트 수를 고려하지 않고 고정 비율로 분배하므로, 엔드포인트 수가 AZ 간에 크게 다를 때 레이턴시 최적화가 오히려 악화될 수 있다.

### 실무 적용
지역성 인식 라우팅 도입 전 검증 절차: (1) 모든 노드에 토폴로지 레이블 확인(`kubectl get nodes -L topology.kubernetes.io/zone`), (2) 각 AZ의 Pod 수 확인 (불균형이 심하면 AZ 분산 배치 먼저 조정), (3) `DestinationRule`에 `outlierDetection` 반드시 추가, (4) Envoy 관리 인터페이스(`/clusters`)에서 엔드포인트 지역성 레이블이 올바르게 반영됐는지 확인(`istioctl proxy-config endpoints <pod>`). 도입 후 AZ별 트래픽 분산을 Prometheus에서 `istio_requests_total` 레이블의 `destination_locality`로 모니터링해 의도대로 동작하는지 검증해야 한다.

---

## Q4. Flagger로 카나리 배포를 자동화할 때 Istio VirtualService와 어떻게 통합되고, 어떤 경계 조건에서 실패하는가?

### 왜 중요한가?
Flagger는 Istio VirtualService의 가중치를 자동으로 조정하여 카나리 배포를 진행하는 프로그레시브 딜리버리 도구다. 수동으로 VirtualService 가중치를 변경하는 대신, Flagger가 메트릭 분석 결과에 따라 자동으로 트래픽을 증가 또는 롤백한다. 그러나 이 자동화가 Istio와 통합되는 방식에 숨겨진 경계 조건이 있고, 이를 이해하지 못하면 카나리 배포 자동화가 예상과 다르게 동작할 수 있다.

### 분析
Flagger는 `Canary` 커스텀 리소스를 정의하면, 자동으로 primary Deployment, canary Deployment, VirtualService, DestinationRule을 생성하고 관리한다. 사용자가 기존 Deployment를 업데이트하면 Flagger가 이를 감지하고 카나리 분석을 시작한다. 이 자동 생성 과정에서 기존에 수동으로 작성한 VirtualService와 충돌이 발생하는 경우가 있다. Flagger가 VirtualService를 소유하는 리소스로 관리하므로, 수동 변경 사항이 Flagger에 의해 덮어쓰일 수 있다.

분석 기간(analysis interval)과 Kubernetes 컨트롤러 루프 타이밍 간 경쟁 조건이 있다. Flagger는 설정된 간격(예: 1분)마다 메트릭을 수집하고 가중치를 업데이트한다. 이 기간에 Prometheus가 잠시 다운되거나 메트릭이 없으면, Flagger는 메트릭 조회 실패를 어떻게 처리하는가? `metrics.thresholdRange`에 기본값이 없으면 실패로 간주하고 롤백을 트리거할 수 있다. 메트릭 인프라 일시 장애가 카나리 자동 롤백을 일으키는 시나리오다.

카나리 가중치 업데이트와 Deployment HPA 간의 타이밍 충돌도 확인이 필요하다. 카나리 Pod 수가 HPA에 의해 자동으로 변경될 때, Flagger가 기대하는 엔드포인트 수와 실제 엔드포인트 수가 일치하지 않아 트래픽 분산이 기대 가중치와 달라질 수 있다. Flagger는 VirtualService 가중치를 기준으로 하지만, 실제 트래픽 분산은 Envoy의 엔드포인트 수에도 영향받는다.

헤더 기반 카나리(특정 사용자만 카나리 버전으로)를 Flagger로 구현하는 경우, `x-canary: true` 헤더가 있으면 카나리로, 없으면 primary로 라우팅하는 설정이 가능하다. 그러나 이 설정은 Flagger의 진행률 기반 가중치 업데이트와 병렬로 동작하므로, 두 라우팅 규칙이 동시에 VirtualService에 존재할 때의 우선순위를 명확히 이해해야 한다.

### 실무 적용
Flagger 도입 전 체크리스트: (1) 기존 VirtualService가 있다면 Flagger에게 소유권을 이전하는 방법 확인 (또는 삭제 후 Flagger가 재생성하도록), (2) Prometheus가 Flagger 분석에 필요한 메트릭을 안정적으로 제공하는지 확인, (3) `analysis.threshold`(최소 성공 횟수)와 `analysis.maxWeight`(최대 카나리 비율)를 비즈니스 요구에 맞게 설정, (4) 메트릭 조회 실패 시 `alerting` 설정으로 Slack/PagerDuty에 알림. Flagger Canary 객체의 `status.phase`를 모니터링해 카나리 진행 상태를 실시간으로 추적해야 한다.

---

## Q5. 서킷 브레이커 임계값을 어떻게 결정해야 하며, 잘못 설정하면 어떤 문제가 생기는가?

### 왜 중요한가?
Istio의 서킷 브레이커는 `DestinationRule`의 `outlierDetection`으로 설정한다. 설정값(consecutive5xxErrors, interval, baseEjectionTime 등)이 서킷 브레이커의 민감도를 결정하는데, 너무 민감하면 정상적인 일시적 오류에도 엔드포인트가 제거되고, 너무 둔감하면 장애 전파를 막지 못한다. 올바른 임계값은 "어디서 나오는가?"라는 질문에 답할 수 있어야 한다.

### 분析
`consecutiveGatewayErrors`와 `consecutive5xxErrors`의 차이를 먼저 이해해야 한다. `consecutive5xxErrors`는 HTTP 5xx 응답을 연속으로 받은 횟수이고, `consecutiveGatewayErrors`는 서버가 응답하지 않거나 게이트웨이 오류를 연속으로 받은 횟수다. 정상 운영 중에도 간헐적 5xx가 발생하는 서비스라면 `consecutive5xxErrors: 5`는 너무 엄격하다. 정상 오류율 기준선을 먼저 측정해야 한다.

`interval`과 `baseEjectionTime`의 관계도 중요하다. `interval: 30s`, `baseEjectionTime: 30s`로 설정하면, 엔드포인트가 30초간 제거된 후 다시 트래픽을 받는다. 엔드포인트가 복구되지 않았는데 다시 트래픽을 받으면 또 오류가 발생하고 다시 제거된다. `baseEjectionTime`은 제거 횟수에 비례해 증가하도록 설계되어 있어(`baseEjectionTime * 제거 횟수`), 지속적으로 오류를 내는 엔드포인트는 점점 더 오랫동안 제거된다.

`maxEjectionPercent`는 동시에 제거 가능한 엔드포인트 비율을 제한한다. 기본값이 10%인데, 10개 엔드포인트 중 최대 1개만 제거한다는 의미다. 연쇄 장애 상황에서 여러 엔드포인트가 동시에 오류를 내면, `maxEjectionPercent` 제한으로 일부 오류 엔드포인트가 제거되지 않고 계속 트래픽을 받는다. 반대로 이 값을 높이면, 일시적 장애 상황에서 너무 많은 엔드포인트가 제거되어 트래픽이 소수 엔드포인트에 집중되는 부하 폭발이 발생한다.

### 실무 적용
임계값 결정 방법론: (1) 정상 상태 오류율 기준선 측정 (1주일 `istio_requests_total{response_code=~"5.."}` 데이터 수집), (2) P99 오류율의 3배 이상을 `consecutive5xxErrors` 기준으로 설정 (정상 오류는 무시하고 이상 상황에만 반응), (3) `maxEjectionPercent`는 서비스 최소 인스턴스 수를 고려 (3개라면 33%로 설정해 최소 2개 유지), (4) `baseEjectionTime`은 서비스 평균 복구 시간보다 길게 설정. 서킷 브레이커 동작을 시뮬레이션하려면 chaos engineering 도구(Chaos Mesh, Litmus)를 사용해 의도적으로 엔드포인트를 오류 상태로 만들고 서킷 브레이커 반응을 측정해야 한다.

---

## Q6. ServiceEntry로 외부 서비스를 메시에 등록할 때 어떤 보안 위험이 생기는가?

### 왜 중요한가?
ServiceEntry는 메시 외부의 서비스(외부 API, 레거시 시스템, 클라우드 서비스)를 Istio 메시의 일원으로 등록해, 트래픽 관리와 관측성을 적용할 수 있게 한다. 편리한 기능이지만, 잘못 설정하면 메시 내부에서 외부 세계로 나가는 트래픽에 대한 제어가 오히려 느슨해지거나, 의도치 않은 외부 엔드포인트로 트래픽이 허용되는 결과를 낳을 수 있다.

### 분析
기본적으로 Istio는 `REGISTRY_ONLY` 모드(outboundTrafficPolicy)에서는 ServiceEntry에 없는 외부 서비스로의 트래픽을 차단한다. 이 모드에서 ServiceEntry는 화이트리스트다. 그러나 기본 설정은 `ALLOW_ANY`로, 모든 외부 트래픽이 허용된다. 많은 클러스터가 기본값을 사용하므로, ServiceEntry를 추가하지 않아도 외부 서비스 접근이 가능하다. 이 설정을 모르고 ServiceEntry만 추가하면, 보안을 강화한다는 착각을 하게 된다.

`REGISTRY_ONLY` 모드로 전환하면 기존에 동작하던 외부 서비스 호출이 갑자기 차단될 수 있다. 개발자들이 명시적으로 허용하지 않은 외부 서비스에 의존하고 있을 경우, 이 전환이 서비스 장애를 유발한다. `REGISTRY_ONLY` 전환 전에 현재 나가는 외부 트래픽 목록을 완전히 파악해야 한다.

ServiceEntry의 `addresses` 필드를 지정하지 않으면, 호스트명으로만 매칭된다. DNS 기반 ServiceEntry의 경우, DNS 스푸핑 공격으로 공격자가 다른 IP를 반환하게 만들 수 있다. `resolution: DNS`를 사용하는 ServiceEntry에서 외부 DNS를 신뢰하는 구조가 된다. `resolution: STATIC`과 `addresses`를 명시하면 이 위험을 줄일 수 있지만, IP가 변경되면 수동으로 업데이트해야 한다.

egress gateway를 통한 외부 트래픽 강제 경유도 중요한 보안 패턴이다. `ServiceEntry`만으로는 외부 트래픽이 각 Pod에서 직접 나간다. egress gateway를 설정하면 모든 외부 트래픽이 egress gateway를 통과하므로, 중앙에서 감사 로그를 남기고 추가 정책을 적용할 수 있다. 규제 환경에서 외부 트래픽 감사가 필요하다면 egress gateway가 필수다.

### 실무 적용
외부 서비스 관리 정책: (1) `outboundTrafficPolicy: REGISTRY_ONLY`를 기본 설정으로 사용 (전환 전 기존 외부 트래픽 완전 파악), (2) ServiceEntry에 `exportTo: ["."]`로 네임스페이스 범위 제한, (3) 민감한 외부 서비스(결제, 인증)는 egress gateway를 통해 경유하고 상세 로그 기록, (4) ServiceEntry 등록은 PR 검토를 거치는 GitOps 프로세스로 관리 — 무제한 외부 접근 허용을 방지하기 위해. 정기적으로 등록된 ServiceEntry가 실제 사용 중인지 Prometheus 메트릭으로 검증하고, 사용되지 않는 ServiceEntry는 제거하는 정리 프로세스가 필요하다.
