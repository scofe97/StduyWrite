# Ch07. Grafana Mimir — 점검 질문

## Q1. Prometheus 단독으로 부족해지는 세 가지 벽은 무엇인가?

**핵심 포인트**:
- 용량: 활성 시계열 수백만 개 이상이면 단일 인스턴스 메모리/디스크 I/O 한계
- 보존: 로컬 TSDB 기본 15일, 장기 보존 시 디스크 장애 = 전체 유실
- 멀티 클러스터 뷰: 클러스터별 Prometheus로는 글로벌 쿼리 불가, Federation은 집계 데이터만

## Q2. Write Path에서 Distributor와 Ingester의 역할을 구분하라

**핵심 포인트**:
- Distributor: 수신 + 검증(라벨, 타임스탬프) + consistent hashing으로 Ingester 라우팅 + 테넌트별 rate limit
- Ingester: 인메모리 버퍼링 + WAL 기록 + 2시간마다 블록 압축 후 Object Storage flush
- Replication factor(기본 3)로 Ingester 간 시계열 복제하여 장애 대비

## Q3. 멀티 테넌시는 어떻게 동작하며, 왜 필요한가?

**핵심 포인트**:
- `X-Scope-OrgID` 헤더로 테넌트 식별, 테넌트별 독립된 저장·쿼리
- 팀별 rate limit, 보존 정책, 접근 제어를 분리 가능
- Thanos는 라벨 기반으로 제한적, Mimir는 설계 초기부터 네이티브 지원

## Q4. Thanos, Mimir, VictoriaMetrics의 핵심 차이는?

**핵심 포인트**:
- Thanos: Sidecar 패턴으로 기존 Prometheus 변경 최소화, Apache 2.0
- Mimir: 독립 클러스터 + remote_write, LGTM 스택 통합, AGPL v3
- VictoriaMetrics: 단일 바이너리 가능, 디스크 효율 7-10배, 운영 단순
- 선택 기준: LGTM 통합 → Mimir, 기존 유지 → Thanos, 운영 단순 → VM

## Q5. Object Storage가 Mimir에서 핵심인 이유는?

**핵심 포인트**:
- 용량 무제한 확장 (S3, GCS, Azure Blob)
- 비용 효율: 로컬 SSD 대비 10배 이상 저렴한 저장 단가
- 내구성: 99.999999999% (11 nines), 로컬 디스크 장애와 무관
- Store Gateway가 인덱스를 캐싱하여 조회 성능 보완

## Q6. Prometheus 있는 환경에 Mimir 도입 여부를 어떻게 판단하나?

**핵심 포인트**:
- 활성 시계열 100만 미만 + 보존 1개월 이내 → Prometheus 단독으로 충분
- 멀티 클러스터 통합 뷰 또는 3개월 이상 보존 필요 → Mimir 도입 검토
- LGTM 스택 이미 사용 중이면 Mimir가 자연스러운 선택
- 운영 인력이 부족하면 VictoriaMetrics나 Grafana Cloud(매니지드) 고려

## Q7. LGTM 스택 완성 시 Alloy→Mimir 경로는 어떻게 구성되나?

**핵심 포인트**:
- Alloy의 `prometheus.remote_write` 컴포넌트가 Mimir Distributor 엔드포인트로 push
- 메트릭(Mimir), 로그(Loki), 트레이스(Tempo)가 동일한 Alloy에서 분기
- Grafana가 Mimir를 Prometheus 타입 데이터 소스로 등록하여 PromQL 쿼리
- Ch08에서 이 통합 파이프라인의 구체적인 설정을 다룸
