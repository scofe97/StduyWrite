# 03. Operations

운영 명령어, DR (Disaster Recovery), 트러블슈팅

---

## rpk 명령어

### 클러스터 관리

```bash
# 클러스터 정보
rpk cluster info
rpk cluster health

# 설정 확인
rpk cluster config status
rpk cluster config export > cluster-config.yaml

# 설정 변경
rpk cluster config set log_compression_type lz4
rpk cluster config import cluster-config.yaml
```

### 토픽 관리

```bash
# 생성
rpk topic create orders -p 6 -r 3

# 목록
rpk topic list

# 상세 정보
rpk topic describe orders

# 설정 변경
rpk topic alter-config orders --set retention.ms=604800000

# 삭제
rpk topic delete orders
```

### 메시지 작업

```bash
# 생산
echo '{"id":"1"}' | rpk topic produce orders

# 소비 (처음부터)
rpk topic consume orders --offset start

# 소비 (최신 N개)
rpk topic consume orders --num 10

# 특정 파티션
rpk topic consume orders --partition 0 --offset 100
```

### Consumer Group

```bash
# 목록
rpk group list

# 상세 (lag 포함)
rpk group describe order-consumers

# 오프셋 리셋
rpk group seek order-consumers --to start --topics orders
rpk group seek order-consumers --to end --topics orders
rpk group seek order-consumers --to-timestamp 1704067200000 --topics orders
```

### 파티션 관리

```bash
# 밸런서 상태
rpk cluster partitions balancer-status

# 수동 밸런싱
rpk cluster partitions balance

# 파티션 이동
rpk cluster partitions move orders 0 --to 2

# 언더레플리케이션 확인
rpk cluster partitions --under-replicated

# 리더 없는 파티션
rpk cluster partitions --leaderless
```

---

## Disaster Recovery

### Shadowing (v25.3+)

비동기 오프셋 보존 복제

```yaml
# Primary Cluster
config:
  cluster:
    cloud_storage_enabled: true
    cloud_storage_bucket: primary-bucket

# DR Cluster
config:
  cluster:
    shadow_indexing_enabled: true
    cloud_storage_enabled: true
    cloud_storage_bucket: primary-bucket  # 동일 버킷
```

### 백업 전략

#### 설정 백업

```bash
# 클러스터 설정
rpk cluster config export > backup/cluster-config.yaml

# 토픽 설정
for topic in $(rpk topic list | tail -n +2); do
  rpk topic describe $topic -c > backup/topics/$topic.yaml
done

# ACL 백업
rpk acl list --format json > backup/acls.json
```

#### 스키마 백업

```bash
# 모든 스키마 백업
mkdir -p backup/schemas
for subject in $(curl -s http://localhost:8081/subjects | jq -r '.[]'); do
  curl -s "http://localhost:8081/subjects/$subject/versions/latest" > "backup/schemas/$subject.json"
done
```

### 복구 절차

```bash
# 1. 새 클러스터 구성

# 2. 설정 복구
rpk cluster config import backup/cluster-config.yaml

# 3. 토픽 생성
for file in backup/topics/*.yaml; do
  topic=$(basename $file .yaml)
  rpk topic create $topic -c $file
done

# 4. 스키마 복구
for file in backup/schemas/*.json; do
  subject=$(basename $file .json)
  curl -X POST "http://localhost:8081/subjects/$subject/versions" \
    -H "Content-Type: application/vnd.schemaregistry.v1+json" \
    -d @$file
done

# 5. 데이터 복구 (Tiered Storage에서)
# 자동으로 클라우드에서 다운로드됨
```

---

## 트러블슈팅

### Pod 시작 안 됨

```bash
# 이벤트 확인
kubectl describe pod redpanda-0 -n redpanda

# 일반적 원인
# 1. PVC 바인딩 실패
kubectl get pvc -n redpanda

# 2. 리소스 부족
kubectl describe node

# 3. 이미지 풀 실패
kubectl get events -n redpanda
```

### 연결 실패

```bash
# 서비스 확인
kubectl get svc -n redpanda
kubectl get endpoints -n redpanda

# Pod 내부에서 테스트
kubectl exec -n redpanda redpanda-0 -- rpk cluster info

# 포트 확인
kubectl exec -n redpanda redpanda-0 -- netstat -tlnp
```

### 높은 지연시간

```bash
# 리더 분포 확인
rpk cluster partitions status

# 리밸런싱
rpk cluster partitions balance

# 디스크 I/O 확인
kubectl exec -n redpanda redpanda-0 -- iostat -x 1

# 메모리 확인
kubectl exec -n redpanda redpanda-0 -- free -h
```

### 언더레플리케이션

```bash
# 상태 확인
rpk cluster partitions --under-replicated

# 원인 파악
# 1. 브로커 다운
rpk cluster info

# 2. 네트워크 문제
kubectl logs -n redpanda redpanda-0 | grep -i "error\|timeout"

# 3. 디스크 공간
kubectl exec -n redpanda redpanda-0 -- df -h
```

### Consumer Lag 증가

```bash
# Lag 확인
rpk group describe my-group

# 원인
# 1. Consumer 처리 속도 < 생산 속도
# 2. 리밸런싱 중
# 3. 특정 파티션 문제

# 해결
# - Consumer 인스턴스 추가
# - 파티션 수 증가
# - Consumer 코드 최적화
```

---

## 운영 체크리스트

### 일일 점검

```bash
□ rpk cluster health
□ rpk cluster partitions --under-replicated
□ rpk group list (consumer lag 확인)
□ 디스크 사용량 확인
□ 메트릭 대시보드 확인
```

### 주간 점검

```bash
□ 백업 검증
□ 설정 백업
□ 로그 검토
□ 용량 계획 검토
```

### 업그레이드

```bash
# 1. 백업
rpk cluster config export > pre-upgrade-config.yaml

# 2. Dry-run
helm upgrade redpanda . --dry-run

# 3. 롤링 업그레이드
helm upgrade redpanda . -f values.yaml

# 4. 검증
rpk cluster health
rpk cluster info

# 5. 롤백 (필요시)
helm rollback redpanda 1
```

---

## 참고

- [rpk Reference](https://docs.redpanda.com/current/reference/rpk/)
- [Disaster Recovery](https://docs.redpanda.com/current/manage/disaster-recovery/)
- [Troubleshooting](https://docs.redpanda.com/current/manage/troubleshooting/)
