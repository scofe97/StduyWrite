# 04. Deployment

Redpanda Helm 차트 배포 실습 및 검증

---

## 사전 준비

### 1. Kubernetes 클러스터

```bash
# 로컬 테스트용 (kind)
kind create cluster --name redpanda-test

# 또는 minikube
minikube start --memory 4096 --cpus 2

# 클러스터 확인
kubectl cluster-info
```

### 2. Helm 설치 확인

```bash
# Helm 3.10+ 필요
helm version

# 차트 디렉토리로 이동
cd /Users/simbohyeon/okestro/tps_manifest/helm-charts/redpanda
```

---

## 배포 단계

### Step 1: 의존성 업데이트

```bash
helm dependency update
helm dependency list
```

### Step 2: Dry-run 확인

```bash
# 렌더링 결과 확인
helm install redpanda . \
  --namespace redpanda \
  --create-namespace \
  -f values-dev.yaml \
  --dry-run --debug > dry-run-output.yaml

# 결과 검토
cat dry-run-output.yaml | grep "kind:" | sort | uniq -c
```

### Step 3: 실제 배포

```bash
helm install redpanda . \
  --namespace redpanda \
  --create-namespace \
  -f values-dev.yaml
```

### Step 4: 배포 상태 확인

```bash
# Helm 릴리스 상태
helm status redpanda -n redpanda

# Pod 상태 (실시간)
kubectl get pods -n redpanda -w

# 모든 리소스 확인
kubectl get all -n redpanda
```

---

## 배포 검증

### Pod 상태 확인

```bash
# Pod 목록
kubectl get pods -n redpanda

# Pod 상세 정보
kubectl describe pod redpanda-0 -n redpanda

# Pod 로그
kubectl logs redpanda-0 -n redpanda -f

# 이전 컨테이너 로그 (재시작 시)
kubectl logs redpanda-0 -n redpanda --previous
```

### 클러스터 상태 확인

```bash
# rpk로 클러스터 정보 확인
kubectl exec -n redpanda redpanda-0 -- rpk cluster info

# 클러스터 상태
kubectl exec -n redpanda redpanda-0 -- rpk cluster health

# 브로커 목록
kubectl exec -n redpanda redpanda-0 -- rpk cluster metadata
```

### 서비스 확인

```bash
# 서비스 목록
kubectl get svc -n redpanda

# 엔드포인트 확인
kubectl get endpoints -n redpanda
```

---

## 접속 테스트

### Port-forward 설정

```bash
# Kafka API (새 터미널)
kubectl port-forward svc/redpanda 9092:9092 -n redpanda &

# Schema Registry (새 터미널)
kubectl port-forward svc/redpanda 8081:8081 -n redpanda &

# Admin API (새 터미널)
kubectl port-forward svc/redpanda 9644:9644 -n redpanda &

# Console UI (새 터미널)
kubectl port-forward svc/redpanda-console 8080:8080 -n redpanda &
```

### rpk 테스트

```bash
# 브로커 설정
export REDPANDA_BROKERS=localhost:9092

# 토픽 생성
rpk topic create test-topic --partitions 3 --replicas 1

# 토픽 목록
rpk topic list

# 메시지 발행
echo "hello redpanda" | rpk topic produce test-topic

# 메시지 소비
rpk topic consume test-topic --num 1

# 토픽 삭제
rpk topic delete test-topic
```

### Admin API 테스트

```bash
# 클러스터 상태
curl http://localhost:9644/v1/cluster/health_overview | jq

# 브로커 정보
curl http://localhost:9644/v1/brokers | jq

# 설정 확인
curl http://localhost:9644/v1/cluster_config | jq
```

---

## 트러블슈팅

### Pod이 Pending 상태

```bash
# 이벤트 확인
kubectl describe pod redpanda-0 -n redpanda

# 일반적 원인
# - PVC 바인딩 실패 → StorageClass 확인
# - 리소스 부족 → 노드 리소스 확인
# - 스케줄링 실패 → 노드 셀렉터/톨러레이션 확인
```

### Pod이 CrashLoopBackOff

```bash
# 로그 확인
kubectl logs redpanda-0 -n redpanda --previous

# 일반적 원인
# - 메모리 부족 → resources.memory 증가
# - 설정 오류 → ConfigMap 확인
# - 권한 문제 → RBAC 확인
```

### 연결 실패

```bash
# 서비스 엔드포인트 확인
kubectl get endpoints redpanda -n redpanda

# Pod 네트워크 확인
kubectl exec -n redpanda redpanda-0 -- netstat -tlnp

# DNS 확인
kubectl exec -n redpanda redpanda-0 -- nslookup redpanda
```

---

## 업그레이드

```bash
# 변경사항 확인
helm diff upgrade redpanda . -f values-dev.yaml -n redpanda

# 업그레이드 실행
helm upgrade redpanda . -f values-dev.yaml -n redpanda

# 롤백 (필요시)
helm rollback redpanda 1 -n redpanda

# 히스토리 확인
helm history redpanda -n redpanda
```

---

## 삭제

```bash
# Helm 릴리스 삭제
helm uninstall redpanda -n redpanda

# PVC 삭제 (데이터 삭제)
kubectl delete pvc -n redpanda --all

# 네임스페이스 삭제
kubectl delete namespace redpanda
```

---

## 참고

- [Redpanda Kubernetes Deployment](https://docs.redpanda.com/current/deploy/deployment-option/self-hosted/kubernetes/)
