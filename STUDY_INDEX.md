# 학습 주제 인덱스

> docs(이론)와 poc(실습)를 연결하는 학습 가이드

## 빠른 탐색

| 번호 | 주제 | 이론 (docs/) | 실습 (poc/) |
|------|------|-------------|-------------|
| 01 | AI | [01_AI](docs/01_AI/) | [01_AI](poc/01_AI/) |
| 02 | Architecture | [02_Architecture](docs/02_Architecture/) | [02_Architecture](poc/02_Architecture/) |
| 03 | CloudNative | [03_CloudNative](docs/03_CloudNative/) | [03_CloudNative](poc/03_CloudNative/) |
| 04 | Database | [04_Database](docs/04_Database/) | [04_Database](poc/04_Database/) |
| 05 | DevOps | [05_DevOps](docs/05_DevOps/) | [05_DevOps](poc/05_DevOps/) |
| 06 | Frontend | [06_Frontend](docs/06_Frontend/) | [06_Frontend](poc/06_Frontend/) |
| 07 | Observability | [07_Observability](docs/07_Observability/) | [07_Observability](poc/07_Observability/) |
| 08 | MessageQueue | [08_MessageQueue](docs/08_MessageQueue/) | [08_MessageQueue](poc/08_MessageQueue/) |
| 09 | Go | [09_goLang](docs/09_goLang/) | [09_goLang](poc/09_goLang/) |
| 10 | Spring | [10_Spring](docs/10_Spring/) | [10_Spring](poc/10_Spring/) |
| 11 | DevTools | [11_DevTools](docs/11_DevTools/) | [11_DevTools](poc/11_DevTools/) |

---

## 권장 학습 순서

1. **Database 기본 → 분산시스템** (docs/04_Database)
2. **Go 기초 → 동시성 → 웹** (docs/09_goLang + poc/09_goLang)
3. **Frontend 기초 → React → 실시간통신** (docs/06_Frontend + poc/06_Frontend)
4. **Observability 이론 → OpenTelemetry 실습** (docs/07_Observability + poc/07_Observability)

---

## 교차 참조 맵

여러 관점에서 다뤄지는 주제들의 연결:

| 주제 | 이론 (docs/) | 실습 (poc/) |
|------|-------------|-------------|
| **WebSocket** | - | [06_Frontend/08-websocket](poc/06_Frontend/08-websocket/), [09_goLang/04-web/02-websocket](poc/09_goLang/04-web/02-websocket/) |
| **SSE** | - | [06_Frontend/09-sse](poc/06_Frontend/09-sse/) |
| **I/O 모델** | [09_goLang](docs/09_goLang/) | [09_goLang/12-system-programming](poc/09_goLang/12-system-programming/) |
| **동시성** | [09_goLang](docs/09_goLang/) | [09_goLang/03-concurrency](poc/09_goLang/03-concurrency/) |

---

## 심화 학습 경로

```
이론 (docs/)
    │
    ├── 06_Frontend/ ──────────▶ WebSocket/SSE 실습 (poc/06_Frontend/)
    │
    ├── 08_MessageQueue/ ──────▶ Kafka 실습 (poc/08_MessageQueue/)
    │
    └── 09_goLang/ ────────────▶ Go 시스템 프로그래밍 (poc/09_goLang/12-system-programming/)
                                 Go 동시성 (poc/09_goLang/03-concurrency/)
```

## 문서 구조

- **docs/**: 책 요약, 개념 정리, 이론 학습 문서
- **poc/**: Proof of Concept 실습 코드

> 프로젝트 개요는 [README.md](README.md) 참조
