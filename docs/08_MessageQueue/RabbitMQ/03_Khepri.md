# RabbitMQ Khepri (메타데이터 저장소)

## 1. 개요

Khepri는 **RabbitMQ 4.0 (2024년)**부터 정식 지원되는 새로운 메타데이터 저장소입니다. 기존 Mnesia를 대체하며, Quorum Queues와 동일한 **Raft 합의 알고리즘**을 사용합니다.

### 타임라인

| 버전 | 상태 |
|------|------|
| 3.13.x | 실험적 (미지원) |
| **4.0** | **정식 지원** |
| **4.2** | **기본값으로 설정** |
| 향후 | Mnesia 제거 예정 |

---

## 2. 메타데이터 저장소란?

RabbitMQ 클러스터의 핵심 정보를 저장하는 데이터베이스:

### 저장 대상
- 가상 호스트 (Virtual Hosts)
- 사용자 및 권한
- Exchange, Queue, Binding 정의
- 정책 (Policies)
- 런타임 파라미터
- 클러스터 멤버십 정보

---

## 3. Mnesia vs Khepri

| 항목 | Mnesia (기존) | Khepri (신규) |
|------|--------------|---------------|
| **기반 기술** | Erlang 분산 DB | Raft 합의 알고리즘 |
| **일관성** | 최종 일관성 | 강한 일관성 |
| **네트워크 파티션** | 복잡한 복구 | 예측 가능한 동작 |
| **Split-brain** | 취약 | 방지 |
| **성능** | 기준 | 여러 시나리오에서 향상 |
| **복구** | 수동 개입 필요 | 자동 복구 |

---

## 4. Khepri의 장점

### 1. 예측 가능한 동작

```
Mnesia:
  네트워크 파티션 발생 → 복잡한 Split-brain 상황
  → 수동 개입 필요

Khepri:
  네트워크 파티션 발생 → Quorum이 있는 파티션만 동작
  → 명확한 동작, 자동 복구
```

### 2. 강한 일관성

- 모든 메타데이터 변경은 Quorum 확인 후 적용
- 읽기 일관성 보장
- 클러스터 전체에서 동일한 뷰

### 3. Quorum Queues/Streams와 통합

```
┌─────────────────────────────────────────────────┐
│              RabbitMQ 4.0+                      │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  Khepri  │  │ Quorum   │  │ Streams  │     │
│  │(metadata)│  │ Queues   │  │          │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │             │            │
│       └─────────────┴─────────────┘            │
│                     │                          │
│              Raft Consensus                    │
│           (동일한 알고리즘 사용)                 │
└─────────────────────────────────────────────────┘
```

### 4. 성능 향상

RabbitMQ 팀 벤치마크 결과:
- 많은 메타데이터 작업에서 성능 향상
- 특히 대규모 클러스터에서 효과적

---

## 5. Quorum 요구사항

Khepri는 Raft 기반이므로 Quorum이 필요합니다:

### 클러스터 시작 동작

```
5노드 클러스터에서 모든 노드가 중지된 경우:

1. 첫 번째 노드 시작 → 대기 (Quorum 미달)
2. 두 번째 노드 시작 → 대기 (Quorum 미달)
3. 세 번째 노드 시작 → Quorum 달성 (3/5) → 서비스 시작!
```

### 권장 클러스터 크기

| 노드 수 | Quorum | 허용 장애 노드 |
|--------|--------|---------------|
| 3 | 2 | 1 |
| 5 | 3 | 2 |
| 7 | 4 | 3 |

---

## 6. Khepri 활성화

### 신규 클러스터

```bash
# rabbitmq.conf
metadata_store = khepri
```

또는 환경 변수:

```bash
export RABBITMQ_FEATURE_FLAGS="khepri_db"
```

### 기존 클러스터 마이그레이션

```bash
# Feature flag 활성화
rabbitmqctl enable_feature_flag khepri_db
```

**주의사항:**
- 마이그레이션은 일방향 (Khepri → Mnesia 롤백 불가)
- 피크 시간 외에 수행 권장
- 마이그레이션 중 일시적 일시 중지 발생 가능

---

## 7. 운영 고려사항

### 클러스터 노드 추가/제거

```bash
# 노드 추가 (기존과 동일)
rabbitmqctl join_cluster rabbit@node1

# 노드 제거 전 확인
# Khepri는 Quorum 유지 필수!
rabbitmqctl forget_cluster_node rabbit@node3
```

### 백업 및 복구

```bash
# 정의 내보내기
rabbitmqctl export_definitions /path/to/definitions.json

# 정의 가져오기
rabbitmqctl import_definitions /path/to/definitions.json
```

### 상태 확인

```bash
# Khepri 상태 확인
rabbitmq-diagnostics metadata_store_status

# 클러스터 상태
rabbitmqctl cluster_status
```

---

## 8. 마이그레이션 가이드

### 사전 점검

1. **RabbitMQ 버전**: 4.0 이상 필요
2. **클러스터 상태**: 모든 노드 정상 동작 확인
3. **백업**: definitions.json 내보내기

### 마이그레이션 절차

```bash
# 1. 클러스터 상태 확인
rabbitmqctl cluster_status

# 2. 정의 백업
rabbitmqctl export_definitions backup.json

# 3. Khepri 활성화
rabbitmqctl enable_feature_flag khepri_db

# 4. 마이그레이션 진행 확인
rabbitmq-diagnostics metadata_store_status

# 5. 완료 후 검증
rabbitmqctl list_queues
rabbitmqctl list_exchanges
```

### 마이그레이션 특성

- **온라인 마이그레이션**: 서비스 중단 없이 진행
- **병렬 실행**: 일반 RabbitMQ 활동과 병렬로 진행
- **일시 중지**: 마이그레이션 마지막 단계에서 짧은 일시 중지

---

## 9. 트러블슈팅

### Quorum 손실

```
증상: 메타데이터 변경 불가, 새 큐 생성 실패

해결:
1. 장애 노드 복구 또는 새 노드 추가
2. Quorum 복구 시 자동으로 정상화
```

### 마이그레이션 실패

```
증상: enable_feature_flag 실패

해결:
1. 모든 노드가 4.0+ 버전인지 확인
2. 클러스터 연결 상태 확인
3. 로그 확인: /var/log/rabbitmq/
```

### 성능 저하

```
증상: 메타데이터 작업 느려짐

확인:
1. 네트워크 지연 확인
2. 디스크 I/O 확인
3. Raft 리더 분포 확인
```

---

## 10. FAQ

### Q: 3.13에서 Khepri를 사용했는데 4.0으로 업그레이드 가능한가요?

**A: 불가능합니다.** 3.13.x에서 Khepri는 미지원 상태였으므로, 해당 노드는 4.x로 업그레이드할 수 없습니다.

### Q: Mnesia는 언제까지 지원되나요?

**A:** 4.2 이후에도 당분간 지원되지만, 향후 버전에서 제거 예정입니다. 가능하면 조기에 Khepri로 마이그레이션을 권장합니다.

### Q: Single 노드에서도 Khepri를 사용해야 하나요?

**A:** 사용 가능하지만, Single 노드에서는 Khepri의 이점(고가용성, 분산 합의)이 크지 않습니다. 그래도 향후 클러스터 확장을 고려하면 사용을 권장합니다.

---

## 11. 참고 자료

- [RabbitMQ Metadata Store 문서](https://www.rabbitmq.com/docs/metadata-store)
- [Khepri Roadmap - Default Store](https://www.rabbitmq.com/blog/2025/09/01/6-khepri-default)
- [How to Enable Khepri](https://www.rabbitmq.com/docs/metadata-store/how-to-enable-khepri)
- [Khepri FAQ](https://www.rabbitmq.com/docs/metadata-store/khepri-faq)
