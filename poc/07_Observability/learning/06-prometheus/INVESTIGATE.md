# Ch06. Prometheus — 점검 질문

## Q1. Pull 모델은 Push 모델과 비교해 어떤 운영상 이점을 주는가?

**핵심 포인트**:
- 서비스 디스커버리로 수집 대상 자동 발견 — 서비스가 Prometheus 주소를 몰라도 됨
- scrape 실패 자체가 장애 탐지 신호로 활용 가능
- 수집 주기를 중앙에서 통제하여 수집 서버 과부하 방지
- 단점: 방화벽 뒤 서비스나 단기 배치 작업은 Pushgateway 필요

## Q2. Counter, Gauge, Histogram, Summary를 각각 언제 쓰는가?

**핵심 포인트**:
- Counter: 단조 증가 누적값 (요청 수, 에러 수) → `rate()`로 초당 변화율 변환
- Gauge: 현재 상태값 (메모리 사용량, 큐 길이) → `avg_over_time()`으로 기간 평균
- Histogram: 서버 측 분위수 계산, 집계 가능 → 대부분의 지연 시간 측정에 권장
- Summary: 클라이언트 측 분위수 계산, 집계 불가 → 특수한 경우에만 사용

## Q3. PromQL에서 `rate()`가 핵심 함수인 이유는?

**핵심 포인트**:
- Counter는 누적값이라 그 자체로는 "현재 부하"를 나타내지 못함
- `rate()`가 구간 내 증가량을 시간으로 나눠 초당 변화율을 계산
- Counter 리셋(재시작)도 자동 처리
- `increase()`는 총 증가량, `rate()`는 초당 증가율 — 용도에 따라 선택

## Q4. Service Discovery가 Prometheus pull 모델에서 어떤 역할을 하는가?

**핵심 포인트**:
- Kubernetes API, Consul, DNS 등에서 수집 대상 목록을 자동 갱신
- Pod 생성·삭제 시 scrape 대상이 자동으로 추가·제거
- `relabel_configs`로 어노테이션 기반 필터링 가능 (예: `prometheus.io/scrape: "true"`)

## Q5. Node Exporter와 Alloy를 함께 쓰는 이유는?

**핵심 포인트**:
- Node Exporter: 호스트 하드웨어/OS 메트릭 전문 (수백 개 커널 메트릭)
- Alloy: 범용 텔레메트리 수집·라우팅 (앱 메트릭, 로그, 트레이스)
- 장애 격리: 한쪽 재시작 시 다른 쪽 수집 영향 없음
- 소규모 환경에서는 Alloy의 `prometheus.exporter.unix`로 대체 가능하나, 커버리지 차이 존재

## Q6. 로컬 TSDB의 한계 3가지와 각각의 해결 방향은?

**핵심 포인트**:
- 장기 보존 어려움 → `remote_write`로 Mimir/Thanos에 전달
- 수평 확장 불가 → Mimir의 distributor-ingester 분산 아키텍처
- HA 제한 → Mimir의 replication factor 기반 고가용성

## Q7. Federation은 언제 쓰고, 왜 Mimir가 더 나은 대안인가?

**핵심 포인트**:
- Federation: 상위 Prometheus가 하위 Prometheus의 집계된 메트릭을 scrape하는 계층 구조
- 소규모 멀티 클러스터에서는 충분하지만, 세밀한 원본 데이터 쿼리가 불가
- Mimir는 모든 원본 시계열을 저장하므로 글로벌 뷰에서 상세 쿼리 가능
- Federation은 임시 방편, 장기적으로는 remote_write + 중앙 저장소가 표준
