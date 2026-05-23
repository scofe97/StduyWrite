# Ch10 - Istio 아키텍처 실습
---
> 대응 학습 문서: `learning/ch10-architecture/LEARN.md`

istiod의 내부 구조를 직접 확인하고, Envoy sidecar가 어떻게 주입되는지 관찰한다. xDS API를 통해 istiod가 Envoy에 설정을 전달하는 흐름을 `istioctl` 도구로 추적한다.

## 사전 조건

GCP K8s 클러스터에 Istio가 설치되어 있어야 한다. `istio-system` 네임스페이스에 `istiod` Pod이 Running 상태인지 확인한다.

```bash
kubectl get pods -n istio-system
```

bookinfo 샘플 앱이 없으면 먼저 배포한다:

```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/bookinfo/platform/kube/bookinfo.yaml -n bookinfo
```

## 실습 항목

| # | 개념 | 실습 내용 | 검증 방법 |
|---|------|----------|----------|
| 1 | istiod 구조 | Pod describe로 컨테이너/포트 확인 | discovery/15010/15014 포트 존재 확인 |
| 2 | Sidecar injection | 네임스페이스 레이블 → deploy → sidecar 확인 | Pod에 2개 컨테이너 존재 |
| 3 | proxy-status | 동기화 상태 전체 조회 | SYNCED 상태 확인 |
| 4 | proxy-config | listener/route/cluster/endpoint 조회 | 각 xDS 설정 덤프 출력 |
| 5 | Envoy Admin API | port-forward 15000으로 접속 | /stats, /clusters 응답 확인 |
| 6 | config_dump | 전체 설정 덤프 크기 측정 | jq로 파싱하여 섹션 수 확인 |

## 실습 상세

### 1. istiod Pod 구조 확인

**목표**: istiod가 어떤 컨테이너로 구성되고 어떤 포트를 노출하는지 파악한다.

**단계**:

```bash
# istiod Pod 이름 확인
kubectl get pods -n istio-system -l app=istiod

# Pod 상세 정보 확인 (컨테이너, 포트, 환경변수)
kubectl describe pod -n istio-system -l app=istiod

# istiod 서비스 포트 확인
kubectl get svc istiod -n istio-system -o yaml
```

**검증**: describe 출력에서 다음 포트가 보여야 한다:

```
15010  - xDS gRPC (평문)
15012  - xDS gRPC (mTLS)
15014  - Control plane 모니터링
15017  - Webhook (sidecar injection)
8080   - 상태 확인 HTTP
```

### 2. Sidecar Injection 테스트

**목표**: 네임스페이스 레이블만으로 자동 주입이 동작하는 과정을 직접 확인한다.

**단계**:

```bash
# 테스트용 네임스페이스 생성
kubectl create namespace injection-test

# 현재 상태 확인 (주입 레이블 없음)
kubectl get namespace injection-test --show-labels

# sidecar injection 활성화
kubectl label namespace injection-test istio-injection=enabled

# 레이블 적용 확인
kubectl get namespace injection-test --show-labels

# 테스트 Pod 배포 (nginx)
kubectl run test-nginx --image=nginx -n injection-test

# Pod 컨테이너 수 확인 (2개여야 함)
kubectl get pod test-nginx -n injection-test

# 컨테이너 목록 확인 (nginx + istio-proxy)
kubectl describe pod test-nginx -n injection-test | grep -A 5 "Containers:"
```

**검증**: `READY` 열이 `2/2`로 표시되어야 한다. `istio-proxy` 컨테이너가 sidecar로 주입된 것이다.

**정리**:

```bash
kubectl delete namespace injection-test
```

### 3. istioctl proxy-status로 동기화 상태 확인

**목표**: istiod가 모든 Envoy 프록시에 최신 설정을 전달했는지 확인한다.

**단계**:

```bash
# 전체 프록시 동기화 상태 조회
istioctl proxy-status

# 특정 Pod의 상태만 확인
istioctl proxy-status -n bookinfo
```

**검증**: 출력 형식은 다음과 같다:

```
NAME                                 CLUSTER  CDS  LDS  EDS  RDS  ECDS  ISTIOD  VERSION
productpage-v1-xxx.bookinfo          ...      SYNCED SYNCED SYNCED SYNCED ...
```

CDS/LDS/EDS/RDS 모두 `SYNCED`이면 정상이다. `STALE`이 보이면 istiod와 Envoy 간 연결에 문제가 있다.

### 4. istioctl proxy-config 조회

**목표**: Envoy에 실제로 전달된 xDS 설정을 확인하여 istiod → Envoy 설정 전파 흐름을 이해한다.

**단계**:

```bash
# bookinfo productpage Pod 이름 저장
PRODUCTPAGE=$(kubectl get pod -n bookinfo -l app=productpage -o jsonpath='{.items[0].metadata.name}')

# Listener 설정 조회 (inbound/outbound 포트 목록)
istioctl proxy-config listener $PRODUCTPAGE -n bookinfo

# Route 설정 조회 (HTTP 라우팅 규칙)
istioctl proxy-config route $PRODUCTPAGE -n bookinfo

# Cluster 설정 조회 (업스트림 서비스 목록)
istioctl proxy-config cluster $PRODUCTPAGE -n bookinfo

# Endpoint 설정 조회 (실제 Pod IP 목록)
istioctl proxy-config endpoint $PRODUCTPAGE -n bookinfo

# 특정 서비스 엔드포인트만 필터링
istioctl proxy-config endpoint $PRODUCTPAGE -n bookinfo --cluster "outbound|9080||reviews.bookinfo.svc.cluster.local"
```

**검증**: Cluster 조회 결과에 `reviews.bookinfo.svc.cluster.local`이 포함되어야 한다. Endpoint 조회에서 reviews Pod의 실제 IP가 표시되어야 한다.

### 5. Envoy Admin API 접속

**목표**: Envoy가 노출하는 Admin API(포트 15000)를 직접 호출하여 내부 상태를 확인한다.

**단계**:

```bash
# productpage Pod의 Envoy Admin API를 로컬 15000으로 포워딩
kubectl port-forward $PRODUCTPAGE -n bookinfo 15000:15000 &

# 사용 가능한 Admin 엔드포인트 목록 확인
curl -s http://localhost:15000/help | head -30

# 통계 확인 (요청 수, 에러율 등)
curl -s http://localhost:15000/stats | grep "upstream_rq_total" | head -10

# 클러스터 상태 확인
curl -s http://localhost:15000/clusters | head -20

# 로그 레벨 확인
curl -s http://localhost:15000/logging

# port-forward 종료
kill %1
```

**검증**: `/help` 응답에 `/config_dump`, `/stats`, `/clusters`, `/listeners` 등 엔드포인트 목록이 출력되어야 한다.

### 6. config_dump 조회 및 분석

**목표**: Envoy의 전체 설정 덤프를 조회하고, xDS 설정 구조를 파악한다.

**단계**:

```bash
kubectl port-forward $PRODUCTPAGE -n bookinfo 15000:15000 &

# 전체 config_dump 크기 측정
curl -s http://localhost:15000/config_dump | wc -c

# JSON 파싱하여 최상위 섹션 확인
curl -s http://localhost:15000/config_dump | python3 -c "
import json, sys
data = json.load(sys.stdin)
for config in data.get('configs', []):
    print(config.get('@type', '').split('.')[-1])
"

# Listener 섹션만 추출
curl -s http://localhost:15000/config_dump | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for c in data['configs']:
    if 'ListenersConfigDump' in c.get('@type', ''):
        listeners = c.get('dynamic_listeners', [])
        for l in listeners[:3]:
            print(l.get('name', ''))
"

# istioctl로도 동일하게 조회 가능
istioctl proxy-config all $PRODUCTPAGE -n bookinfo -o json | wc -c

kill %1
```

**검증**: config_dump 크기는 수백 KB 이상이다. 최상위 섹션에 `BootstrapConfigDump`, `ListenersConfigDump`, `ClustersConfigDump`, `RoutesConfigDump`, `EndpointsConfigDump`가 포함되어야 한다.

## 정리 (Cleanup)

```bash
# 테스트 중 생성한 리소스 확인
kubectl get namespace injection-test 2>/dev/null && kubectl delete namespace injection-test

# port-forward 프로세스가 남아있으면 종료
pkill -f "port-forward.*15000" || true
```
