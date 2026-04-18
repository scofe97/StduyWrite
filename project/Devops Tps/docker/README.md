# Devops TPS Docker Environment

개발 환경용 Docker Compose 구성입니다. 모든 서비스는 Redpanda(Kafka-compatible) 기반으로 통합되어 있습니다.

## 파일 구조

| 파일 | 용도 | 서비스 |
|------|------|--------|
| `docker-compose.yml` | 전체 통합 | 모든 서비스 |
| `docker-compose.db.yml` | 데이터베이스 | PostgreSQL, Redis |
| `docker-compose.kafka.yml` | 메시징 | Redpanda, Kafka UI, Topic Init |
| `docker-compose.monitoring.yml` | 모니터링 | OTel, Jaeger, Prometheus, Loki, Grafana |
| `docker-compose.cicd.yml` | CI/CD | Git Provider, Jenkins, Redpanda Connect |

## 사용법

### 전체 실행
```bash
docker compose up -d
```

### 개별 실행
```bash
# DB만
docker compose -f docker-compose.db.yml up -d

# Kafka만
docker compose -f docker-compose.kafka.yml up -d

# 모니터링만
docker compose -f docker-compose.monitoring.yml up -d
```

### 조합 실행
```bash
# DB + Kafka
docker compose -f docker-compose.db.yml -f docker-compose.kafka.yml up -d

# DB + Kafka + CI/CD (개발 워크플로우)
docker compose -f docker-compose.db.yml -f docker-compose.kafka.yml -f docker-compose.cicd.yml up -d

# DB + Kafka + Monitoring (운영 모니터링)
docker compose -f docker-compose.db.yml -f docker-compose.kafka.yml -f docker-compose.monitoring.yml up -d
```

## 포트 매핑

| 서비스 | 포트 | 설명 |
|--------|------|------|
| Redpanda | 9092 | Kafka API (host) |
| Redpanda | 18081 | Schema Registry |
| Redpanda | 9644 | Admin API |
| Kafka UI | 8090 | 웹 UI |
| PostgreSQL | 5432 | DB 접속 |
| Redis | 6379 | 캐시 |
| Git Provider | 50051 | gRPC |
| Git Provider | 8083 | REST Gateway |
| Jenkins | 9091 | CI 서버 UI |
| Redpanda Connect | 4195 | Webhook 수신 |
| Grafana | 3001 | 대시보드 |
| Prometheus | 9090 | 메트릭 |
| Jaeger | 16686 | 트레이싱 UI |
| Loki | 3100 | 로그 수집 |
| OTel Collector | 4317/4318 | OTLP gRPC/HTTP |

## 접속 정보

**PostgreSQL**
- Host: localhost:5432
- User: runners / Password: runners123
- Database: runners_high

**Grafana**
- URL: http://localhost:3001
- User: admin / Password: admin123

**Jenkins**
- URL: http://localhost:9091
- User: admin / Password: admin

**Kafka UI**
- URL: http://localhost:8090

## 토픽 목록

### Domain Events (tps-api <-> git-api)
| 토픽 | 용도 |
|------|------|
| runners-high.git.commands | tps-api -> git-api 명령 |
| runners-high.git.events | git-api -> tps-api 이벤트 |
| runners-high.notifications | 알림 |
| runners-high.ticket.events | 티켓 이벤트 |
| runners-high.build.events | 빌드 이벤트 |
| runners-high.deploy.events | 배포 이벤트 |
| runners-high.workflow.events | 워크플로우 이벤트 |
| runners-high.approval.events | 승인 이벤트 |

### CI/CD Events (git-provider)
| 토픽 | 용도 |
|------|------|
| git-events | Webhook -> git-provider |
| cicd.commands | CI/CD 명령 |
| cicd.events | CI/CD 이벤트 |
| cicd-results | CI/CD 결과 |
| workflow.events | 워크플로우 이벤트 |

## 네트워크

모든 서비스는 `devops-tps-network` 브리지 네트워크를 사용합니다.
모듈별 compose 파일을 조합 실행할 경우, 동일한 네트워크를 공유합니다.
