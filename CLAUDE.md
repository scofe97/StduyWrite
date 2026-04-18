# Runners-High 프로젝트
## 프로젝트 개요

Runners-High는 TPS(Trombone Platform System)를 기반으로 한 Polyglot 아키텍처 학습 프로젝트입니다.

- **Java (tps-api)**: 핵심 비즈니스 로직, 메타데이터 관리
- **Go (git-api)**: 외부 Git API 연동 (GitHub, GitLab)

---

## 프로젝트 구조

```
runners-high/
├── CLAUDE.md              # 이 파일 (프로젝트 지침)
├── README.md              # 프로젝트 소개
├── PROGRESS.md            # 진행 상황 추적
│
├── research/              # 📚 리서치 문서 (skill: research-plan-implement)
│   ├── tps-analysis.md    # TPS 분석
│   └── _archive/          # 완료된 리서치
│
├── plans/                 # 📝 계획 문서 (skill: research-plan-implement)
│   ├── implementation-plan.md
│   ├── architecture-decisions.md
│   └── _archive/          # 완료된 계획
│
├── project/               # 💻 소스 코드 (Go 모듈 분리)
│   ├── git-api/           # Go 모듈 (github.com/runners-high/git-api)
│   │   ├── cmd/server/    # 진입점 (main.go)
│   │   ├── internal/      # 내부 패키지
│   │   │   ├── client/    # Git Provider 클라이언트
│   │   │   │   ├── github_client.go   # GitHub API
│   │   │   │   ├── gitlab_client.go   # GitLab API
│   │   │   │   └── bitbucket_client.go # Bitbucket API (예정)
│   │   │   ├── config/    # 설정 관리
│   │   │   ├── handler/   # Kafka 핸들러
│   │   │   └── service/   # 비즈니스 로직
│   │   └── pkg/           # 공개 패키지
│   │       ├── event/     # Kafka 이벤트 타입
│   │       └── kafka/     # Kafka Producer/Consumer
│   │
│   ├── tps-api/           # Java Spring Boot (향후)
│   └── docker/            # Docker Compose 환경
│
├── docs/                  # 참고 문서
│   └── TPS/               # TPS 시스템 설계 문서
│       └── tech/git-api/  # Git-API 기술 문서
│
├── poc/                   # PoC 코드
└── skills/                # 프로젝트 특화 skill
```

---

## ⚠️ 필수 워크플로우

### research-plan-implement Skill 적용

이 프로젝트는 **반드시** `research-plan-implement` skill을 따릅니다:

```
📚 1단계: 리서치     →     📝 2단계: 계획     →     💻 3단계: 구현
research/[name].md        plans/[name].md           project/코드
```

**자동 활성화 키워드**:
- `분석`, `분석해줘`, `리서치`, `research`
- `조사`, `파악해줘`, `코드 분석`
- `아키텍처 분석`, `구조 분석`

**중요 규칙**:
- ❌ `claudedocs/`에 저장 금지
- ✅ `research/`에 분석 결과 저장
- ✅ `plans/`에 계획 저장 (plan/ 아님, plans/!)

---

## 아키텍처 결정 사항 (ADR)

| ID | 제목 | 상태 |
|----|------|------|
| ADR-001 | Polyglot 아키텍처 | ✅ 승인 |
| ADR-002 | Java/Go 서비스 분리 | ✅ 승인 (Go 분리) |
| ADR-003 | Kafka 비동기 통신 | ✅ 승인 |
| ADR-004 | 4계층 도메인 구조 | ✅ 승인 |
| ADR-005 | MyBatis 매퍼 | ✅ 승인 |

상세: `plans/architecture-decisions.md`

---

## 서비스 구성

### TPS-API (Java)
- **역할**: 메타데이터 CRUD, 비즈니스 로직
- **도메인**: Connection, Repository, Branch, Project, Workflow, Ticket, User
- **기술**: Spring Boot, MyBatis, PostgreSQL

### Git-API (Go)
- **역할**: 외부 Git API 호출 (Polyglot 아키텍처)
- **모듈**: `github.com/runners-high/git-api` (Go 모듈 분리)
- **위치**: `project/git-api/`
- **기능**: 브랜치 생성/삭제, 저장소 동기화, PR/MR 생성
- **지원 Provider**:
  - GitHub (Cloud, Enterprise)
  - GitLab (Cloud, Self-hosted)
  - Bitbucket (Cloud, Server/DC) - 예정
- **기술**: Go 1.21, Kafka, go-github, go-gitlab
- **인증**: TPS-API에서 Connection/Credential 관리, Kafka를 통해 토큰 전달

### Kafka Topics
```
runners-high.git.commands  # TPS-API → Git-API (명령)
runners-high.git.events    # Git-API → TPS-API (결과)
runners-high.notifications # 알림
```

---

## 개발 환경

### Docker Compose 시작
```bash
cd project/docker
docker compose up -d
```

### 서비스 포트
| 서비스 | 포트 |
|--------|------|
| Kafka | 9092 |
| Kafka UI | 8080 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Zookeeper | 2181 |

---

## 참조 Skill

| Skill | 용도 | 위치 |
|-------|------|------|
| `research-plan-implement` | 분석/계획/구현 워크플로우 | `~/.claude/skills/` |

---

## 세션 시작 시 확인사항

1. 현재 작업 위치 확인
2. `PROGRESS.md` 진행 상황 확인
3. `research/`, `plans/` 기존 문서 확인
4. 새 기능 시 리서치부터 시작

---

## 커밋 규칙

```
[프로젝트][이슈] 타입: 설명

예시:
[tps-api][RH-001] feat: 브랜치 동기화 API 구현
[git-api][RH-002] fix: GitHub API 토큰 갱신 오류 수정
```

타입: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
