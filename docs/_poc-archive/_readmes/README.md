# POC (Proof of Concept) 프로젝트

## 개요
개념 검증 및 실험용 프로젝트 모음. 기술 학습과 프로토타이핑을 위한 공간입니다.

## 폴더 구조

| 폴더 | 설명 | 주요 내용 |
|------|------|----------|
| `01_AI/` | AI/ML 기술 학습 | 생성형 AI, LLM |
| `02_Architecture/` | 아키텍처 실습 | EDA 패턴 (14챕터) |
| `03_CloudNative/` | 클라우드 네이티브 | (예정) |
| `04_Database/` | 데이터베이스 | (예정) |
| `05_DevOps/` | DevOps | (예정) |
| `06_Frontend/` | 프론트엔드 기술 학습 | WebSocket, React 패턴 |
| `07_Observability/` | 관찰 가능성 | OpenTelemetry, 분산 추적 |
| `08_MessageQueue/` | Kafka 메시징 | 이벤트 스트리밍, 프로듀서/컨슈머 |
| `09_goLang/` | Go 언어 학습 | 웹 개발, 시스템 프로그래밍, 동시성 |
| `10_Spring/` | Spring Framework | (예정) |
| `11_DevTools/` | 개발 도구 | 생산성 도구, 자동화 |

---

## 02_Architecture/

아키텍처 패턴 심화 실습

| 폴더 | 설명 |
|------|------|
| `01-event-driven/` | EDA 아키텍처 패턴 실습 (14챕터) - Saga, Outbox, CDC, 스트림 처리 등 |

---

## 06_Frontend/

프론트엔드 기술 심화 학습

| 폴더 | 설명 |
|------|------|
| `08-websocket/` | WebSocket 통신 패턴 |

### WebSocket 학습 내용
- `01-basics/` - TCP 연결, 4-Tuple, Ephemeral Port, 소켓 관리
- `05-message-types/` - SNAPSHOT/DELTA/ACK 메시지 패턴

---

## 09_goLang/

Go 언어 종합 학습

| 폴더 | 설명 |
|------|------|
| `01-fundamentals/` | Go 기초 문법 |
| `02-standard-library/` | 표준 라이브러리 |
| `03-concurrency/` | 동시성 (goroutine, channel) |
| `04-web/` | 웹 개발 (HTTP, WebSocket) |
| `05-cli/` | CLI 도구 개발 |
| `06-microservices/` | 마이크로서비스 |
| `07-database/` | 데이터베이스 연동 |
| `08-config-logging/` | 설정 & 로깅 |
| `09-patterns/` | 디자인 패턴 |
| `10-devops/` | DevOps |
| `11-capstone/` | 종합 프로젝트 |
| `12-system-programming/` | 시스템 프로그래밍 |

### 핵심 학습 경로

**네트워크 I/O 심화**:
```
04-web/02-websocket/     → gorilla/websocket 사용법, 4-Tuple 기초
12-system-programming/03-network-io/ → epoll, 시스템 콜, 패킷 라우팅
```

---

## 11_DevTools/

개발 도구 및 생산성 향상 학습

| 폴더 | 설명 |
|------|------|
| `01_tmux/` | 터미널 멀티플렉서 - 세션 관리, 화면 분할, Claude Code 통합 |
| `02_omc/` | oh-my-claudecode - Claude Code CLI 확장 플러그인 |
| `03_vim/` | Vim/NeoVim - 모달 편집, IDE급 환경, IdeaVim/Claude Code 통합 |

---

## 07_Observability/

분산 시스템 관찰 가능성 학습

| 내용 | 설명 |
|------|------|
| OpenTelemetry | 분산 추적, 메트릭, 로그 |
| Jaeger/Zipkin | 트레이싱 백엔드 |
| Spring Boot 통합 | 자동 계측 |

---

## 학습 연결 고리

### TCP/소켓 → WebSocket → 실시간 통신

```
[시스템 레벨]                    [애플리케이션 레벨]
09_goLang/12-system-programming/  →  09_goLang/04-web/02-websocket/
  - socket(), bind(), listen()     - gorilla/websocket
  - accept(), 4-Tuple               - 연결 관리
  - epoll 멀티플렉싱                - 메시지 브로드캐스트
          ↓
06_Frontend/08-websocket/
  - 클라이언트 관점
  - SNAPSHOT/DELTA/ACK 패턴
  - 낙관적 업데이트
```

### 분산 시스템 관찰

```
07_Observability/
  - 서비스 간 호출 추적
  - OpenTelemetry 계측
          ↓
08_MessageQueue/
  - 비동기 메시징
  - 이벤트 소싱
```

---

## 이론 문서 연결 (docs/)

| POC 폴더 | 관련 이론 문서 |
|----------|---------------|
| `01_AI/` | [docs/01_AI](../docs/01_AI/) |
| `02_Architecture/` | [docs/02_Architecture](../docs/02_Architecture/) |
| `03_CloudNative/` | [docs/03_CloudNative](../docs/03_CloudNative/) |
| `04_Database/` | [docs/04_Database](../docs/04_Database/) |
| `05_DevOps/` | [docs/05_DevOps](../docs/05_DevOps/) |
| `06_Frontend/` | [docs/06_Frontend](../docs/06_Frontend/) |
| `07_Observability/` | [docs/07_Observability](../docs/07_Observability/) |
| `08_MessageQueue/` | [docs/08_MessageQueue](../docs/08_MessageQueue/) |
| `09_goLang/` | [docs/09_goLang](../docs/09_goLang/) |
| `10_Spring/` | [docs/10_Spring](../docs/10_Spring/) |
| `11_DevTools/` | [docs/11_DevTools](../docs/11_DevTools/) |

> 전체 학습 인덱스는 [STUDY_INDEX.md](../STUDY_INDEX.md) 참조
