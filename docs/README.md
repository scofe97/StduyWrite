# 기술 문서 (docs)

> 책 요약, 개념 정리, 이론 학습 문서

## 카테고리

| 번호 | 주제 | 설명 | 실습 링크 |
|------|------|------|-----------|
| 01 | [AI](01_AI/) | 생성형 AI, Claude, LangChain | [poc/01_AI](../poc/01_AI/) |
| 02 | [Architecture](02_Architecture/) | DDD, Event-Driven | [poc/02_Architecture](../poc/02_Architecture/) |
| 03 | [CloudNative](03_CloudNative/) | Docker, K8s, ArgoCD | [poc/03_CloudNative](../poc/03_CloudNative/) |
| 04 | [Database](04_Database/) | DDIA, PostgreSQL, Vector DB | [poc/04_Database](../poc/04_Database/) |
| 05 | [DevOps](05_DevOps/) | CI/CD, DevOps Fundamentals | [poc/05_DevOps](../poc/05_DevOps/) |
| 06 | [Frontend](06_Frontend/) | React, TypeScript, Testing | [poc/06_Frontend](../poc/06_Frontend/) |
| 07 | [Observability](07_Observability/) | Tracing, Metrics, Logs | [poc/07_Observability](../poc/07_Observability/) |
| 08 | [MessageQueue](08_MessageQueue/) | Kafka, RabbitMQ, Redis | [poc/08_MessageQueue](../poc/08_MessageQueue/) |
| 09 | [goLang](09_goLang/) | Go 언어, gRPC, System Programming | [poc/09_goLang](../poc/09_goLang/) |
| 10 | [Spring](10_Spring/) | Spring Framework, Spring Boot | [poc/10_Spring](../poc/10_Spring/) |
| 11 | [DevTools](11_DevTools/) | 개발 도구, 생산성 | [poc/11_DevTools](../poc/11_DevTools/) |

## 기타 문서

- [JVM 최적화](JVM%20최적화/)
- [참고 자료](참고%20자료/)

> 전체 학습 인덱스는 [STUDY_INDEX.md](../STUDY_INDEX.md) 참조

---

## 학습 주제 체크리스트

> 마지막 업데이트: 2026-02-08
>
> daily-essay 스킬과 연계하여 일일 학습 문서 생성에 활용

### 진행 상태 범례
- [ ] 미작성
- [~] 작성 중
- [x] 완료 (YYYY-MM-DD | 제목)

---

### 08_MessageQueue

#### Kafka
- [x] 2026-02-08 | Exactly-Once Semantics
- [ ] Consumer Group Rebalancing
- [ ] Kafka Streams 기초
- [ ] Schema Registry와 Avro
- [ ] Kafka Connect 활용

#### RabbitMQ
- [ ] RabbitMQ vs Kafka 비교
- [ ] Exchange 타입별 라우팅
- [ ] Dead Letter Queue 패턴

---

### 09_goLang

#### 기초
- [x] 2026-02-26 | Goroutine과 Channel 기초
- [ ] Context 패턴과 취소 전파
- [ ] Error Handling 패턴

#### 고급
- [ ] Go 메모리 모델
- [ ] Sync 패키지 활용
- [ ] Go 런타임 스케줄러

---

### 10_Spring

#### Spring Boot
- [ ] Spring Boot Auto-Configuration 원리
- [ ] Spring Boot Actuator 활용
- [ ] Spring Boot 테스트 전략

#### Spring Security
- [ ] OAuth2 Resource Server 구현
- [ ] JWT 인증 구현

---

### 11_DevTools

- [ ] Git 고급 워크플로우
- [ ] Terminal 생산성 도구

---

### 01_AI

- [ ] Prompt Engineering 기법
- [ ] RAG 아키텍처 이해
- [ ] LangChain 기초

---

### 02_Architecture

- [x] 2026-02-08 | 분산 시스템의 하트비트와 장애 감지
- [ ] DDD Aggregate 설계
- [ ] Event Sourcing 기초
- [ ] CQRS 패턴

---

### 03_CloudNative

- [ ] Kubernetes Pod 라이프사이클
- [ ] Helm Chart 작성
- [ ] ArgoCD GitOps

---

### 04_Database

- [ ] PostgreSQL 인덱스 최적화
- [ ] 트랜잭션 격리 수준
- [ ] Vector DB 활용

---

### 05_DevOps

- [ ] CI/CD 파이프라인 설계
- [ ] Infrastructure as Code
- [ ] 모니터링 전략

---

### 06_Frontend

- [ ] React Server Components
- [ ] TypeScript 고급 타입
- [ ] 프론트엔드 테스트 전략

---

### 07_Observability

- [ ] 분산 트레이싱 이해
- [ ] 메트릭 수집과 알림
- [ ] 로그 집계 패턴
