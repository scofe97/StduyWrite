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

## 실무 장애 시나리오 (Troubleshooting Scenarios)

실무에서 자주 만나는 장애를 직접 재현하고 진단하는 실습입니다. "증상이 보이면 → 어떤 명령으로 진단하고 → 어느 학습문서를 보는가"를 한 줄로 잇습니다. 일부 시나리오는 `scenarios/` 아래에 재현 매니페스트를 두어 `kubectl apply` 한 번으로 장애를 띄울 수 있습니다.

| # | 증상 | 1차 진단 명령 | 원인·해결 요지 | 학습문서 | 재현 |
|---|------|--------------|---------------|---------|------|
| 1 | Pod가 `OOMKilled`(exit 137) 반복, `CrashLoopBackOff` | `kubectl describe pod <p>`의 Last State Reason | 컨테이너 RSS가 cgroup `memory.max` 초과 → limit 상향 또는 JVM `MaxRAMPercentage` 하향 | [OOMKilled 사례](../../05_operations/05-12.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) · [자원 관리](../../05_operations/05-10.%EC%9E%90%EC%9B%90%20%EA%B4%80%EB%A6%AC.md) | `scenarios/oomkilled/` |
| 2 | `ImagePullBackOff` / `ErrImagePull` | `kubectl describe pod <p>` Events | 이미지명·태그 오타, 프라이빗 레지스트리 시크릿 누락 → 태그 확인, `imagePullSecrets` 설정 | [핵심 워크로드](../../01_foundation/01-02.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | `scenarios/imagepull/` |
| 3 | PVC가 `Pending`에서 안 넘어감 | `kubectl describe pvc <pvc>` Events | StorageClass 부재 또는 동적 프로비저너 없음 → `kubectl get sc`로 확인, 존재하는 SC로 교체 | [스토리지와 상태](../../01_foundation/01-03.%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80%EC%99%80%20%EC%83%81%ED%83%9C.md) | `scenarios/pvc-pending/` |
| 4 | 롤링업데이트가 멈춤(`rollout` 진행 안 됨) | `kubectl rollout status deploy/<d>` | readiness probe 실패로 새 Pod가 Ready 안 됨 + `maxUnavailable:0` → probe 수정 또는 `rollout undo` | [핵심 워크로드](../../01_foundation/01-02.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | `scenarios/rollout-stuck/` |
| 5 | Service로 연결 안 됨, `nslookup` 실패 | `kubectl get endpoints <svc>` / Pod에서 `nslookup <svc>` | selector-라벨 불일치로 endpoint 0개, 또는 ndots·search domain·CoreDNS 문제 | [Service와 EndpointSlice](../../02_networking/02-04.Service%EC%99%80%20EndpointSlice.md) · [DNS와 CoreDNS](../../02_networking/02-05.DNS%EC%99%80%20CoreDNS.md) | 명령 재현 |
| 6 | HPA가 스케일 안 함(`<unknown>/50%`) | `kubectl get hpa` / `kubectl top pods` | metrics-server 미설치·미동작 → `minikube addons enable metrics-server`, requests 설정 확인 | [오토스케일링](../../05_operations/05-11.%EC%98%A4%ED%86%A0%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | 명령 재현 |
| 7 | `Forbidden` — 리소스 접근 거부 | `kubectl auth can-i <verb> <res> --as=system:serviceaccount:<ns>:<sa>` | ServiceAccount에 Role/RoleBinding 부족 → 필요한 verb를 Role에 추가 | [RBAC과 보안](../../05_operations/05-09.RBAC%EA%B3%BC%20%EB%B3%B4%EC%95%88.md) | `scenarios/rbac-forbidden/` |

### 재현 매니페스트 사용법

`scenarios/` 아래 각 디렉토리에는 장애를 일부러 띄우는 매니페스트와 진단·정리 명령이 주석으로 들어 있습니다. 예를 들어 OOMKilled를 재현하려면 다음처럼 합니다.

```bash
# 장애 띄우기 (해당 ns는 클러스터 시작 시 생성돼 있어야 함)
kubectl apply -f scenarios/oomkilled/oom-pod.yaml

# 증상 관찰 — Running → OOMKilled → CrashLoopBackOff
kubectl get pod oom-demo -n ch06-hpa -w

# 진단 — Last State에 Reason: OOMKilled, Exit Code 137
kubectl describe pod oom-demo -n ch06-hpa | grep -A3 "Last State"

# 정리
kubectl delete -f scenarios/oomkilled/oom-pod.yaml
```

각 매니페스트 상단 주석의 `적용/관찰/진단/정리` 4단계를 그대로 따라가면 됩니다. 재현 컬럼이 "명령 재현"인 시나리오(DNS·HPA)는 매니페스트 없이 위 1차 진단 명령으로 상태를 만들고 확인합니다.

### 기본 환경 FAQ

장애 시나리오와 별개로, 실습 환경 자체가 안 뜰 때 보는 항목입니다.

```bash
# Minikube가 시작되지 않음 — Docker 실행 확인 후 재생성
docker ps
minikube delete && minikube start --cpus=4 --memory=8192 --driver=docker

# Helm 설치 실패 — repo 갱신 + dry-run 검증 후 재설치
helm repo update
helm install <release> <chart> -n <ns> -f values.yaml --dry-run --debug

# Operator CR이 Ready 안 됨 — Operator 로그와 CR status 확인
kubectl logs -f -n <operator-ns> <operator-pod>
kubectl get <cr-type> <cr-name> -n <ns> -o yaml | grep -A 20 status
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
