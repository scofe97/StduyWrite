<!-- migrated: write/09_cloud/service-mesh/deepdive/18-02.Istio 성능 튜닝 점검.md (2026-04-19) -->

# Ch18. Istio 성능 튜닝 — 심화 탐구
---
> 📌 LEARN.md에서 다룬 튜닝 기법의 경계 조건과 운영 함정을 파고든다. 각 질문은 실제 운영에서 마주치는 판단 지점을 다루며, "언제", "왜", "어떤 순서로"에 집중한다.

## Q1. Sidecar CRD 적용 순서와 운영 중 서비스 중단 없이 점진 적용하는 전략은?

Sidecar CRD를 잘못 적용하면 기존에 동작하던 서비스 간 통신이 끊어진다. `outboundTrafficPolicy: REGISTRY_ONLY` 모드는 `egress.hosts`에 없는 목적지로의 트래픽을 즉시 차단하기 때문이다. 따라서 전체 메시에 한꺼번에 적용하는 것은 위험하다.

### 적용 전 의존성 지도 작성

먼저 각 서비스가 실제로 어떤 서비스에 접근하는지 파악해야 한다. Kiali의 서비스 그래프나 Prometheus의 `istio_requests_total` 메트릭으로 실제 트래픽 흐름을 확인한다:

```promql
# payment 서비스가 요청을 보내는 목적지 목록
topk(20, sum(rate(istio_requests_total{
  source_app="payment-service"
}[24h])) by (destination_service_name, destination_service_namespace))
```

24시간 이상의 범위를 사용해 배치 작업, 야간 정기 호출 등 저빈도 트래픽도 포함시킨다. 이 쿼리 결과가 Sidecar CRD의 `egress.hosts` 목록이 된다.

### 단계별 롤아웃 전략

안전한 적용 순서는 세 단계다.

**1단계: ALLOW_ANY 모드로 먼저 적용.** 트래픽을 차단하지 않고 egress 설정만 먼저 배포한다:

```yaml
spec:
  outboundTrafficPolicy:
    mode: ALLOW_ANY    # 차단 없이 관찰만
  egress:
  - hosts:
    - "./*"
    - "order/order-service"
```

이 상태에서 xDS 설정 크기가 줄어드는지 확인하고, `config_dump` 비교로 의도한 범위로 좁혀졌는지 검증한다.

**2단계: 스테이징 환경에서 REGISTRY_ONLY 테스트.** 스테이징에서 `REGISTRY_ONLY`로 전환 후 전체 E2E 테스트를 실행한다. 누락된 의존성이 있으면 503 오류와 함께 `upstream connect error` 메시지가 나타나므로, Envoy 접근 로그에서 `OUTBOUND|*|outbound|*` 항목을 확인한다:

```bash
kubectl logs -n payment <pod> -c istio-proxy | \
  grep '"response_code":"503"' | \
  awk '{print $0}' | tail -20
```

**3단계: 프로덕션 점진 적용.** 하나의 네임스페이스부터 시작해 7일간 모니터링 후 다음 네임스페이스로 확장한다. 각 단계에서 `pilot_total_xds_rejects`와 5xx 오류율을 기준 지표로 삼는다.

### 롤백 준비

문제가 생겼을 때 빠르게 되돌릴 수 있도록 롤백 리소스를 미리 준비한다:

```bash
# 즉시 롤백: Sidecar CRD 삭제로 기본 동작 복원
kubectl delete sidecar payment-sidecar -n payment
```

Sidecar CRD는 삭제하면 즉시 기본 동작(모든 서비스 설정 배포)으로 복원된다. 이 복원이 몇 초 안에 이뤄지므로 서비스 중단 없이 롤백이 가능하다.

## Q2. discoverySelectors와 Sidecar CRD의 차이 — 언제 어떤 것을 우선 적용하는가?

두 기법은 모두 istiod가 처리하는 설정 범위를 줄이지만, 작동 계층이 다르다.

`discoverySelectors`는 istiod 수준에서 동작한다. 선택된 네임스페이스의 리소스만 Watch하며, 제외된 네임스페이스의 Service·Pod·Endpoint는 istiod 내부 모델에 아예 존재하지 않는다. 따라서 제외된 네임스페이스에 있는 서비스로는 어떤 방법으로도 트래픽을 보낼 수 없다.

Sidecar CRD는 Envoy 수준에서 동작한다. istiod는 여전히 모든 네임스페이스를 추적하지만, 특정 워크로드에 배포하는 xDS 설정 범위를 좁힌다. 제한된 목적지도 istiod 내부 모델에는 존재하며, Sidecar CRD를 제거하면 즉시 다시 접근 가능해진다.

### 적용 우선순위 결정 기준

| 상황 | 권장 기법 |
|------|-----------|
| 메시에 포함할 필요가 없는 네임스페이스가 존재 (모니터링, CI, 로깅) | `discoverySelectors` 먼저 |
| 모든 네임스페이스가 메시에 필요하지만 워크로드별 접근 제어가 필요 | Sidecar CRD |
| 두 조건이 모두 해당 | `discoverySelectors`로 불필요한 네임스페이스 제외 후, 나머지 네임스페이스에 Sidecar CRD 적용 |

`discoverySelectors`를 먼저 적용해야 하는 이유는 효과 범위가 더 크기 때문이다. 제외된 네임스페이스의 리소스는 istiod가 처리조차 하지 않으므로, 해당 서비스에 대한 xDS 설정이 어떤 워크로드에도 생성되지 않는다. Sidecar CRD는 이미 생성된 설정을 배포하지 않는 것에 불과하다.

### 두 기법의 조합 예시

```yaml
# 1단계: discoverySelectors로 불필요한 네임스페이스 제외
meshConfig:
  discoverySelectors:
  - matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: NotIn
      values: [monitoring, logging, ci-ephemeral]

# 2단계: 메시 내 워크로드 기본 Sidecar
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: default
  namespace: istio-system
spec:
  egress:
  - hosts: ["./*", "istio-system/*"]
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY
```

이 조합에서 `discoverySelectors`로 먼저 범위를 줄이고, Sidecar CRD로 나머지를 세밀하게 제어한다. 두 기법이 충돌하는 경우는 없다. `discoverySelectors`로 제외된 네임스페이스는 Sidecar CRD의 `egress.hosts`에 포함시켜도 접근할 수 없다.

## Q3. 디바운스 시간을 늘리면 푸시 횟수가 줄지만, 오래된 설정으로 운영되는 윈도우가 길어진다. 적정값을 어떻게 결정하는가?

디바운스 적정값을 결정하는 데 보편적인 정답은 없다. 클러스터의 배포 패턴, SLO, 트래픽 특성에 따라 달라지므로 측정에서 시작해야 한다.

### 결정에 필요한 데이터 수집

먼저 현재 배포 이벤트 패턴을 파악한다:

```promql
# 시간대별 pilot_inbound_updates 분포
sum(rate(pilot_inbound_updates[5m]))

# 배포 시 이벤트 스파이크 패턴 확인 (1시간)
sum(increase(pilot_inbound_updates[1h]))
```

배포가 하루에 수십 번 몰리는 패턴이면 디바운스 증가 효과가 크다. 이벤트가 시간 전체에 고르게 분산되면 디바운스 증가의 CPU 절감 효과가 작다.

### 비용-효익 계산 프레임워크

디바운스 값은 두 비용의 균형점이다.

**xDS 푸시 비용**: 푸시 1회당 istiod CPU 소비, 네트워크 전송량, Envoy 재구성 시간이 발생한다. 이 비용은 푸시 횟수에 선형으로 비례한다.

**설정 지연 비용**: `PILOT_DEBOUNCE_AFTER` 값만큼 설정 반영이 늦어진다. 카나리 배포에서 트래픽을 5%로 제한하는 VirtualService를 적용했는데 2.5초 후에 반영된다면, 그 사이 트래픽이 전량 새 버전으로 흐를 수 있다.

### 서비스 유형별 권장 범위

운영 경험을 바탕으로 한 출발점 값이다:

| 서비스 유형 | PILOT_DEBOUNCE_AFTER | 근거 |
|-------------|---------------------|------|
| 배치 처리, 내부 작업 서비스 | 1000ms ~ 2500ms | 실시간 설정 변경 불필요 |
| 일반 웹 서비스 | 200ms ~ 500ms | 기본값 대비 적당한 절감 |
| 카나리 배포 중인 서비스 | 100ms (기본값 유지) | 즉각적인 트래픽 제어 필요 |
| 결제, 금융 서비스 | 100ms (기본값 유지) | 오래된 설정으로 인한 오류 허용 불가 |

### 디바운스 증가 전 반드시 확인할 사항

`PILOT_DEBOUNCE_AFTER`를 늘리기 전에 해당 환경의 서킷 브레이커 `consecutiveGatewayErrors` 임계값을 확인해야 한다. Envoy가 오래된 설정으로 운영되는 동안 새로 배포된 버전이 아직 준비되지 않은 상태라면, 일시적인 503이 서킷 브레이커를 열 수 있다. 디바운스 값이 서킷 브레이커 평가 윈도우보다 크면 의도치 않은 서킷 오픈이 발생한다.

## Q4. istiod 스케일 아웃 시 워크로드가 여러 istiod 인스턴스에 어떻게 분배되는가? 재분배 과정에서 설정 불일치가 발생할 수 있는가?

istiod 스케일 아웃은 생각보다 복잡한 분배 메커니즘을 갖는다.

### 연결 분배 메커니즘

Envoy 사이드카는 시작 시점에 istiod의 gRPC 서비스 엔드포인트 목록을 받아 그 중 하나에 연결한다. Kubernetes Service를 통해 로드밸런싱이 이뤄지므로, 이론적으로는 istiod replica 수에 비례해 연결이 분산된다.

그러나 실제로는 기존 연결이 살아있는 한 재연결이 발생하지 않는다. istiod를 3개로 늘려도 기존 프록시는 여전히 원래 연결된 istiod 인스턴스에 붙어 있다. 새로 시작되는 Pod만 세 인스턴스 중 하나에 균등 분배된다.

### 강제 재분배 방법

기존 프록시를 새 인스턴스로 분산하려면 강제 재연결이 필요하다:

```bash
# 방법 1: 프록시 graceful restart (Pod 재시작 없이 연결만 재확립)
istioctl proxy-config bootstrap <pod> | grep "xds_grpc"

# 방법 2: istiod Pod 순차 재시작으로 기존 연결 강제 종료
kubectl rollout restart deployment/istiod -n istio-system
```

istiod Pod를 재시작하면 해당 인스턴스에 연결된 모든 프록시가 reconnect backoff를 거쳐 세 인스턴스 중 하나에 재연결된다. 기본 reconnect backoff는 1초부터 시작해 지수적으로 증가하므로, 대규모 메시에서 istiod 재시작 시 reconvergence storm이 발생할 수 있다.

### 설정 불일치 발생 가능성

여러 istiod 인스턴스가 동시에 운영될 때 설정 불일치가 발생할 수 있는 시나리오가 있다. istiod는 Kubernetes etcd를 공유하지만, 각 인스턴스가 독립적으로 xDS 설정을 계산한다. ConfigMap·Secret 변경 이벤트를 각 인스턴스가 처리하는 타이밍이 다를 수 있으며, 이 때문에 서로 다른 인스턴스에 연결된 프록시가 잠시 다른 설정을 가질 수 있다.

일반적으로 이 불일치 윈도우는 수백 밀리초 이내다. 그러나 istiod가 리더 선출을 사용하는 기능(인증서 서명 등)과 xDS 배포가 함께 이뤄질 때는 더 길어질 수 있다. `pilot_proxy_convergence_time`을 각 istiod 인스턴스별로 따로 집계하면 인스턴스 간 수렴 속도 차이를 확인할 수 있다:

```promql
histogram_quantile(0.99,
  sum(rate(pilot_proxy_convergence_time_bucket[5m]))
    by (le, pod)
)
```

## Q5. 대규모 클러스터(1000+ 서비스)에서 pilot_proxy_convergence_time P99가 10초를 넘을 때 어디서부터 조사하는가?

수렴 시간 P99가 10초를 넘으면 체계적인 계층별 조사가 필요하다. 무작정 리소스를 늘리거나 디바운스를 조정하는 것보다, 병목이 어느 단계에 있는지 먼저 격리해야 한다.

### 1단계: 수렴 시간 분해

전체 수렴 시간은 세 구간으로 나뉜다:

```
[이벤트 수신] → [큐 대기] → [설정 계산] → [xDS 전송] → [프록시 적용]
                  ↑                ↑               ↑
         pilot_proxy_queue_time  (계산시간)   pilot_xds_push_time
```

각 메트릭을 개별 조회해 어느 구간이 길 지 확인한다:

```promql
# 큐 대기 시간 P99
histogram_quantile(0.99,
  sum(rate(pilot_proxy_queue_time_bucket[5m])) by (le))

# xDS 전송 시간 P99
histogram_quantile(0.99,
  sum(rate(pilot_xds_push_time_bucket[5m])) by (le))
```

큐 대기 시간이 길면 CPU 병목이다. xDS 전송 시간이 길면 설정 크기 또는 네트워크 병목이다.

### 2단계: 푸시 볼륨 확인

수렴이 느린 것이 개별 푸시가 느린 것인지, 아니면 푸시가 너무 많아 큐가 쌓이는 것인지 구분해야 한다:

```promql
# 초당 총 푸시 횟수
sum(rate(pilot_xds_pushes[5m]))

# 타입별 분류
sum(rate(pilot_xds_pushes[5m])) by (type)
```

EDS 타입 푸시가 전체의 80% 이상을 차지한다면, endpoint 변경이 자주 일어나는 서비스를 찾아야 한다. HPA(Horizontal Pod Autoscaler)로 인한 replica 수 변동, 롤링 배포 등이 EDS 폭풍의 주요 원인이다.

### 3단계: xDS 페이로드 크기 확인

`config_dump` 크기가 수 MB를 넘는 프록시가 있다면, Sidecar CRD 적용이 되어 있지 않은 것이다:

```bash
# 가장 큰 config_dump를 가진 Pod 찾기
for pod in $(kubectl get pods -A -o \
  jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'); do
  ns=$(echo $pod | cut -d/ -f1)
  name=$(echo $pod | cut -d/ -f2)
  size=$(kubectl exec -n $ns $name -c istio-proxy -- \
    curl -s http://localhost:15000/config_dump 2>/dev/null | wc -c)
  echo "$size $ns/$name"
done | sort -rn | head -10
```

### 4단계: 후보 조치 목록

각 진단 결과에 따른 조치:

- `pilot_proxy_queue_time` 높음 → istiod CPU 증가 (스케일 업), 디바운스 증가
- `pilot_xds_push_time` 높음, config_dump 크기 큼 → Sidecar CRD 또는 discoverySelectors 적용
- EDS 푸시 폭주 → HPA min/max 범위 조정, PodDisruptionBudget으로 롤링 속도 제한
- 모든 지표가 정상인데 P99만 높음 → 아웃라이어 존재 (특정 느린 프록시). `pilot_xds_push_time`을 pod 레이블로 분류해 특정 인스턴스 식별

## Q6. Ambient 모드가 Sidecar 모드 대비 컨트롤 플레인 부하에 미치는 영향은?

Istio 1.23(stable)부터 정식 지원하는 Ambient 모드는 사이드카 아키텍처를 근본적으로 바꾼다. 컨트롤 플레인 부하에도 의미 있는 차이가 생긴다.

### 아키텍처 차이

Sidecar 모드에서 istiod는 **모든 Envoy 사이드카**(Pod 수와 동일)에 xDS 설정을 배포한다. 1,000개 Pod가 있으면 1,000개의 gRPC 연결과 1,000개의 xDS 스트림을 유지한다. 서비스 하나가 변경되면 1,000번의 xDS 푸시가 발생한다.

Ambient 모드는 두 계층으로 분리된다:

- **ztunnel** (L4): 노드당 1개. Pod 수가 아닌 노드 수에 비례해 istiod 연결이 생긴다.
- **waypoint proxy** (L7): 네임스페이스 또는 서비스어카운트당 1개. L7 정책이 필요한 경우에만 배포.

1,000 Pod, 50노드 클러스터 기준으로 비교하면 다음과 같다:

| 지표 | Sidecar 모드 | Ambient 모드 |
|------|-------------|-------------|
| xDS 연결 수 | 1,000개 | 50개 (ztunnel) + waypoint 수 |
| 서비스 변경 시 푸시 수 | 1,000회 | 50회 |
| CPU 소비 (변경 이벤트) | 높음 | 낮음 |

### 컨트롤 플레인 메트릭 변화

Ambient 모드로 전환 후 `pilot_xds_pushes`와 `pilot_proxy_convergence_time`이 유의미하게 감소하는 것이 실험적으로 확인되었다. CNCF의 Ambient 성능 보고서(2024)에 따르면 컨트롤 플레인 CPU 사용량이 사이드카 모드 대비 65~80% 감소하는 경우가 있다.

### Ambient 모드에서 성능 튜닝의 의미 변화

Ambient 모드에서는 Sidecar CRD가 존재하지 않는다. xDS 설정 크기를 줄이는 대신, ztunnel이 받는 policy 수를 줄이는 것이 유사한 역할을 한다. `discoverySelectors`는 Ambient 모드에서도 동일하게 적용된다. 디바운스 튜닝은 여전히 유효하나, 프록시 연결 수 자체가 적으므로 효과 폭이 사이드카 모드보다 작다.

### 현재 Ambient 모드의 한계

Ambient 모드가 컨트롤 플레인 부하를 줄여주는 건 사실이지만, 몇 가지 운영 제약이 있다. L7 정책(AuthorizationPolicy의 HTTP 조건, HTTPRoute 등)을 적용하려면 waypoint proxy를 명시적으로 배포해야 한다. waypoint가 추가될수록 컨트롤 플레인 연결 수가 늘어나 사이드카 모드에 가까워진다. 또한 Sidecar CRD를 통한 세밀한 egress 제어는 waypoint 기반 정책으로 대체해야 하며, 기존 운영 경험이 그대로 이전되지 않는다.

대규모 클러스터에서 컨트롤 플레인 부하가 심각한 문제라면 Ambient 모드 전환을 중장기 옵션으로 고려할 만하다. 단기적으로는 이 챕터에서 다룬 Sidecar CRD와 discoverySelectors 조합이 더 안전하고 검증된 방법이다.
