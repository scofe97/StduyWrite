# Kubernetes PoC - Practice Guide

이 디렉토리는 Kubernetes 학습 프로젝트의 실습 환경입니다. Minikube 기반으로 15개 챕터의 실습 시나리오를 제공합니다.

## Quick Start

```bash
# 클러스터 시작
make cluster-up

# 클러스터 상태 확인
kubectl cluster-info
kubectl get nodes

# 특정 챕터 실습 시작 (예: MySQL Operator)
make mysql-up

# 실습 종료
make mysql-down

# 클러스터 중지
make cluster-down
```

## Environment Setup

### Prerequisites
- Docker Desktop (or Docker Engine)
- minikube v1.32+
- kubectl v1.28+
- helm v3.12+

### Cluster Specification
- CPU: 4 cores
- Memory: 8GB
- Driver: docker
- Kubernetes: v1.28+
- Addons: ingress, metrics-server, dashboard, storage-provisioner

### Start Command
```bash
minikube start \
  --cpus=4 \
  --memory=8192 \
  --driver=docker \
  --kubernetes-version=v1.28.0
```

## Namespaces

| Namespace | Purpose | Chapter |
|-----------|---------|---------|
| `ch01-setup` | Initial verification | Ch01 |
| `ch02-core` | Pod, Deployment, Service | Ch02 |
| `ch03-storage` | PV, PVC, StorageClass | Ch03 |
| `ch04-network` | Ingress, NetworkPolicy | Ch04 |
| `ch05-helm` | Helm Chart deployment | Ch05 |
| `ch06-hpa` | HPA, VPA, CA | Ch06 |
| `ch07-scheduling` | NodeAffinity, Taint/Toleration | Ch07 |
| `ch08-mysql` | MySQL InnoDB Cluster | Ch08 |
| `ch09-pg` | PostgreSQL (CloudNativePG) | Ch09 |
| `ch10-redis` | Redis Cluster | Ch10 |
| `ch11-kafka` | Kafka (Strimzi) | Ch11 |
| `ch12-jenkins` | Jenkins CI/CD | Ch12 |
| `ch13-sonarqube` | SonarQube (Code Quality) | Ch13 |
| `ch14-argocd` | ArgoCD (GitOps) | Ch14 |
| `ch15-monitoring` | Prometheus + Grafana | Ch15 |

## Practice Scenarios

| # | Scenario | Description | Key Resources |
|---|----------|-------------|---------------|
| 1 | Core Workloads | Pod, Deployment, Service 배포 | Deployment, Service |
| 2 | Storage | PVC로 MySQL StatefulSet 구성 | PVC, StatefulSet |
| 3 | Networking | Ingress로 다중 서비스 노출 | Ingress, NetworkPolicy |
| 4 | Helm Chart | 커스텀 차트 작성 및 배포 | Helm Chart, Values |
| 5 | Autoscaling | CPU 기반 HPA 테스트 | HPA, Metrics |
| 6 | Scheduling | Node Affinity + Taint 테스트 | NodeSelector, Affinity |
| 7 | MySQL Operator | InnoDB Cluster 3노드 구성 | MySQL CR |
| 8 | PostgreSQL | CloudNativePG 백업/복구 | Cluster CR, Backup |
| 9 | Redis Cluster | 3 leader Redis Cluster | RedisCluster CR |
| 10 | Kafka | Topic 생성 및 Producer/Consumer | Kafka CR, KafkaTopic |
| 11 | Jenkins | Pipeline 실행 및 Agent 확장 | Jenkins CR, Values |
| 12 | SonarQube | 코드 분석 파이프라인 연동 | Values, Ingress |
| 13 | ArgoCD | GitOps 배포 자동화 | Application CR |
| 14 | Monitoring | Prometheus 쿼리 + Grafana 대시보드 | ServiceMonitor, Values |
| 15 | Full Stack | Jenkins → SonarQube → ArgoCD 파이프라인 | Multi-namespace |

## Useful Commands

### Cluster Management
```bash
# 클러스터 상태
minikube status
minikube dashboard

# SSH 접속
minikube ssh

# IP 확인
minikube ip

# Service URL 확인
minikube service <service-name> -n <namespace> --url
```

### Kubectl Shortcuts
```bash
# 리소스 확인
kubectl get all -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Pod 로그
kubectl logs -f <pod-name> -n <namespace>

# Pod 진입
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash

# 리소스 사용량
kubectl top nodes
kubectl top pods -n <namespace>

# Port Forward
kubectl port-forward svc/<service-name> <local-port>:<svc-port> -n <namespace>
```

### Helm Commands
```bash
# Repository 관리
helm repo add <name> <url>
helm repo update
helm search repo <keyword>

# Chart 설치
helm install <release-name> <chart> -n <namespace> -f values.yaml

# 업그레이드
helm upgrade <release-name> <chart> -n <namespace> -f values.yaml

# 제거
helm uninstall <release-name> -n <namespace>

# 릴리스 목록
helm list -A
```

### Operator Management
```bash
# Operator 설치 확인
kubectl get deployment -n <operator-namespace>

# CRD 확인
kubectl get crd | grep <operator-name>

# CR 상태 확인
kubectl get <cr-type> -n <namespace>
kubectl describe <cr-type> <cr-name> -n <namespace>
```

## Troubleshooting FAQ

### 1. Minikube가 시작되지 않음
```bash
# Docker Desktop 실행 확인
docker ps

# 기존 클러스터 삭제 후 재시작
minikube delete
minikube start --cpus=4 --memory=8192 --driver=docker
```

### 2. Pod가 Pending 상태
```bash
# 이벤트 확인 (리소스 부족, PVC 바인딩 실패 등)
kubectl describe pod <pod-name> -n <namespace>

# 노드 리소스 확인
kubectl top nodes
```

### 3. ImagePullBackOff 에러
```bash
# 이미지 이름 확인
kubectl describe pod <pod-name> -n <namespace>

# Minikube Docker 환경에서 직접 pull 테스트
minikube ssh
docker pull <image-name>
```

### 4. Service 연결 안 됨
```bash
# Service Endpoints 확인
kubectl get endpoints <service-name> -n <namespace>

# Pod Selector 확인
kubectl get svc <service-name> -n <namespace> -o yaml | grep selector -A 5

# NetworkPolicy 확인
kubectl get networkpolicy -n <namespace>
```

### 5. Helm 설치 실패
```bash
# Repository 업데이트
helm repo update

# Dry-run으로 검증
helm install <release> <chart> -n <namespace> -f values.yaml --dry-run --debug

# 기존 릴리스 제거 후 재설치
helm uninstall <release> -n <namespace>
kubectl delete ns <namespace>
```

### 6. Operator CR이 Ready 안 됨
```bash
# Operator Pod 로그 확인
kubectl logs -f -n <operator-namespace> <operator-pod>

# CR Status 확인
kubectl get <cr-type> <cr-name> -n <namespace> -o yaml | grep -A 20 status

# CRD 버전 확인
kubectl get crd <crd-name> -o yaml | grep version
```

## Data Management

### Snapshot
```bash
# 현재 상태 저장
minikube stop
minikube snapshot save <snapshot-name>

# 복원
minikube snapshot restore <snapshot-name>
```

### Resource Export
```bash
# Namespace 전체 리소스 백업
kubectl get all -n <namespace> -o yaml > backup-<namespace>.yaml

# 특정 리소스 백업
kubectl get <resource-type> -n <namespace> -o yaml > backup-<resource>.yaml
```

### Clean Up
```bash
# 특정 챕터 리소스 삭제
make <chapter>-down

# 모든 리소스 삭제 (네임스페이스 기반)
make clean-all

# 클러스터 완전 삭제
minikube delete
```

## Resource Limits

Minikube 8GB 메모리 기준으로 최적화된 리소스 제한:

| Component | Memory Limit | CPU Limit |
|-----------|--------------|-----------|
| MySQL Operator | 512Mi | 500m |
| PostgreSQL Instance | 256Mi | 250m |
| Redis Node | 128Mi | 100m |
| Kafka Broker | 512Mi | 500m |
| Jenkins Controller | 512Mi | 500m |
| SonarQube | 1Gi | 1000m |
| ArgoCD Server | 256Mi | 250m |
| Prometheus | 512Mi | 500m |
| Grafana | 256Mi | 250m |

**주의**: 모든 Operator를 동시에 실행하면 메모리 부족 발생 가능. 챕터별로 순차 실습 권장.

## Next Steps

1. `make cluster-up`으로 클러스터 시작
2. `learning/00-intro/LEARN.md`에서 학습 목표 확인
3. 각 챕터별 `LEARN.md` → `INVESTIGATE.md` 순서로 학습
4. 해당 챕터의 `make <chapter>-up` 실행
5. 실습 완료 후 `make <chapter>-down`으로 정리
6. 다음 챕터로 진행

## References

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Operator Hub](https://operatorhub.io/)
