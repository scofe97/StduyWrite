# Service Mesh Practice
---
> 챕터 번호가 learning/ 디렉토리와 1:1로 매칭된다. 학습 중인 챕터 번호를 찾아 해당 폴더의 README.md를 따라가면 된다.

## 사전 요구사항

- Docker Desktop
- Kind (`go install sigs.k8s.io/kind@latest`)
- kubectl
- Helm 3
- linkerd CLI (`curl -sL https://run.linkerd.io/install | sh`)
- istioctl (`curl -L https://istio.io/downloadIstio | sh -`)
- Fortio (`brew install fortio`) — ch14 복원력 실습

## 빠른 시작

```bash
# 클러스터 생성
make cluster-up

# Istio 실습 (ch10~)
make mesh-istio
make app-bookinfo

# Linkerd 실습 (ch06~)
make mesh-linkerd
make app-emojivoto

# 정리
make clean
```

## 디렉토리 구조

```
practice/
├── cluster/              Kind 3노드 클러스터 설정
├── apps/                 공용 샘플 앱 (bookinfo, emojivoto)
│
├── ch01-service-mesh-fundamentals/  메시 전/후 통신 비교
├── ch02-proxy-architectures/        Envoy 단독 실행, Admin API
├── ch03-gateway-api/                K8s Gateway API CRD 실습
├── ch04-mtls-zero-trust/            openssl 인증서, mTLS curl
├── ch05-linkerd-architecture/       Linkerd 설치, control plane
├── ch06-linkerd-installation/       Linkerd Helm values
├── ch07-linkerd-traffic/            HTTPRoute 카나리
├── ch08-linkerd-security/           Server + AuthPolicy
├── ch09-linkerd-observability/      viz stat/tap/top, Grafana
│
├── ch10-architecture/            istiod, sidecar, proxy-config
├── ch11-installation/            istioctl/Helm 설치, addon
├── ch12-ingress-gateway/         Gateway TLS, SNI, TCP
├── ch13-traffic-management/      라우팅, 카나리, 미러링, Egress
├── ch14-resilience/              LB, Retry, Circuit Breaker
├── ch15-security/                mTLS, AuthZ, JWT
├── ch16-observability/           Prometheus, Grafana, Jaeger, Kiali
├── ch17-troubleshooting/         istioctl analyze, proxy-config 추적
├── ch18-performance-tuning/      Sidecar CRD, discoverySelectors
├── ch19-envoyfilter/             커스텀 필터, WasmPlugin
├── ch20-multi-cluster/           멀티클러스터 (개념 중심)
├── ch21-vm-integration/          WorkloadEntry, VM 시뮬레이션
├── ch22-ambient-mesh/            ztunnel, Waypoint Proxy
│
├── advanced/             Gateway API, Flagger 카나리
└── Makefile
```

## 챕터별 실습 가이드

### 기초 (ch01~04)

| 챕터 | 폴더 | 주요 실습 |
|------|------|----------|
| Ch01 서비스 메시 기초 | `ch01-service-mesh-fundamentals/` | 메시 없는 평문 통신 → sidecar 주입 후 mTLS 비교, tcpdump |
| Ch02 프록시 아키텍처 | `ch02-proxy-architectures/` | Envoy Docker 단독 실행, Admin API, retry 통계, Dynamic config |
| Ch03 Gateway API | `ch03-gateway-api/` | K8s Gateway API CRD, HTTPRoute, 가중치 분할 |
| Ch04 mTLS/Zero Trust | `ch04-mtls-zero-trust/` | openssl CA/서버/클라이언트 인증서, 단방향/양방향 TLS curl |

### Linkerd (ch05~09)

| 챕터 | 폴더 | 포함 파일 | 주요 실습 |
|------|------|----------|----------|
| Ch05 아키텍처 | `ch05-linkerd-architecture/` | README | 설치, control plane 구조, viz 대시보드 |
| Ch06 설치 | `ch06-linkerd-installation/` | `values.yaml` | Helm 설치, 리소스 설정 |
| Ch07 트래픽 | `ch07-linkerd-traffic/` | `httproute-canary.yaml` | HTTPRoute 90/10 분할 |
| Ch08 보안 | `ch08-linkerd-security/` | `default-deny.yaml` | Server, AuthPolicy, MeshTLS |
| Ch09 관측성 | `ch09-linkerd-observability/` | README | stat, tap, top, routes, Grafana |

### Istio 핵심 (ch10~16)

| 챕터 | 폴더 | 포함 파일 | 주요 실습 |
|------|------|----------|----------|
| Ch10 아키텍처 | `ch10-architecture/` | README | istiod 구조, sidecar injection, xDS 덤프 |
| Ch11 설치 | `ch11-installation/` | `istio-values.yaml`, `bookinfo-namespace.yaml` | istioctl/Helm 설치, 프로파일 비교, addon |
| Ch12 Gateway | `ch12-ingress-gateway/` | README | TLS(SIMPLE/MUTUAL/PASSTHROUGH), SNI, TCP |
| Ch13 트래픽 | `ch13-traffic-management/` | `virtual-service-canary.yaml` | 헤더 라우팅, 카나리, 미러링, ServiceEntry |
| Ch14 복원력 | `ch14-resilience/` | README | LB 전략, Timeout, Retry, Circuit Breaker |
| Ch15 보안 | `ch15-security/` | `peer-auth-strict.yaml` | mTLS STRICT, AuthZ, JWT |
| Ch16 관측성 | `ch16-observability/` | README | Prometheus, Grafana, Jaeger, Kiali |

### Istio 운영 (ch17~19)

| 챕터 | 폴더 | 주요 실습 |
|------|------|----------|
| Ch17 트러블슈팅 | `ch17-troubleshooting/` | istioctl analyze, proxy-config Listener→Route→Cluster→Endpoint, Access Log JSON |
| Ch18 성능 튜닝 | `ch18-performance-tuning/` | Sidecar CRD, discoverySelectors, Debounce, Scale Up/Out |
| Ch19 EnvoyFilter | `ch19-envoyfilter/` | Lua 헤더 추가, retriable_status_codes, WasmPlugin |

### Istio 고급 (ch20~22)

| 챕터 | 폴더 | 포함 파일 | 주요 실습 |
|------|------|----------|----------|
| Ch20 멀티클러스터 | `ch20-multi-cluster/` | README | 개념 분석, remote-secret (제한적 실습) |
| Ch21 VM 통합 | `ch21-vm-integration/` | README | WorkloadEntry, WorkloadGroup, VM 시뮬레이션 |
| Ch22 Ambient | `ch22-ambient-mesh/` | `ambient-values.yaml` | ztunnel, Waypoint Proxy, sidecar→ambient 마이그레이션 |

## 실습 진행 방법

1. 해당 챕터의 `learning/{번호}-{주제}/LEARN.md`를 읽는다
2. `practice/ch{번호}-{주제}/README.md`를 열고 단계별로 실행한다
3. 실습 완료 후 Cleanup 섹션으로 리소스를 정리한다
4. `learning/{번호}-{주제}/INVESTIGATE.md`의 심화 질문으로 이해도를 검증한다
