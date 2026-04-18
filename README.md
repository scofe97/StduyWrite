# TPS 티켓/워크플로우 백엔드 개선 프로젝트

> **토스 러너스 하이 프로젝트** - 1달간 TPS 시스템 개선 연구 및 문서화


## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **기간** | 2024.12 ~ 2025.01 (4주) |
| **목표** | TPS 티켓/워크플로우 흐름의 백엔드 개선 방향 연구 |
| **범위** | workflow-api, pipeline-api (백엔드 중심) |
| **산출물** | 기술 문서, PoC 코드, 프로덕션 적용 제안서 |

## 현재 시스템 Pain Points

1. **장애 추적 어려움** - 서비스 간 호출 시 트레이싱 없음
2. **동기 호출 장애 전파** - FeignClient 동기 호출로 장애 확산
3. **로그 분산** - 각 서비스별 로그 분리로 통합 분석 어려움

## 4주 로드맵

```
Week 1: 분산 트레이싱 연구 (Micrometer + Zipkin)
        ↓
Week 2: 비동기 메시지 큐 설계 (Kafka)
        ↓
Week 3: Kafka PoC 구현
        ↓
Week 4: 통합 모니터링 + 최종 정리
```

### Week 1: 분산 트레이싱

- Micrometer Tracing 학습
- Zipkin Docker 환경 구성
- TraceID 전파 메커니즘 이해
- LogAspect 개선안 도출

### Week 2: 비동기 메시지 큐 설계

- Kafka vs RabbitMQ 비교
- 이벤트 드리븐 아키텍처 설계
- Transactional Outbox Pattern
- 이벤트 스키마 설계 (Avro)

### Week 3: Kafka PoC

- Docker로 Kafka 환경 구성
- KafkaTicketEventPublisher 구현
- 기존 FeignClient 대체 PoC
- 성능/안정성 테스트

### Week 4: 통합 모니터링

- Prometheus + Grafana 구성
- 티켓 처리 메트릭 정의
- 프로덕션 적용 제안서 작성
- 최종 발표 자료 준비

## 기술 스택

| 영역 | 기술 |
|------|------|
| 분산 트레이싱 | Micrometer Tracing + Zipkin |
| 메시지 큐 | Apache Kafka |
| 모니터링 | Prometheus + Grafana |
| 로컬 환경 | Docker Compose |
| 이벤트 직렬화 | Apache Avro |

## 디렉토리 구조

```
runners-high/
├── README.md                 # 프로젝트 개요 (현재 파일)
├── PROGRESS.md               # 진행 현황 추적
├── daily/                    # 일일 TIL 문서
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
├── weekly/                   # 주간 회고
├── docs/                     # 기술 문서
├── poc/                      # PoC 코드
└── docker/                   # Docker 환경 설정
```

## 대상 코드베이스

- `workflow-api`: `/Users/simbohyeon/okestro/tps-gitlab2/workflow-api`
- `pipeline-api`: `/Users/simbohyeon/okestro/tps-gitlab2/pipeline-api`

## 진행 상황

- [ ] Week 1: 분산 트레이싱 연구
- [ ] Week 2: 비동기 메시지 큐 설계
- [ ] Week 3: Kafka PoC 구현
- [ ] Week 4: 통합 모니터링 + 최종 정리
