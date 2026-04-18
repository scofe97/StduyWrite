# Claude Code `/context` 명령어 분석

## 명령어 목적

`/context`는 현재 Claude가 "기억하고 있는" 모든 정보와 그 토큰 사용량을 보여줍니다. LLM은 한 번에 처리할 수 있는 토큰 수가 제한되어 있기 때문에, 이 명령어로 컨텍스트가 얼마나 차 있는지 모니터링할 수 있습니다.

---

## 섹션별 분석

### 1. Context Usage (상단 요약)

```
claude-opus-4-5-20251101 · 39k/200k tokens (19%)
```

| 항목 | 토큰 | 비율 | 설명 |
|------|------|------|------|
| System prompt | 4.1k | 2.0% | Claude의 기본 행동 지침 |
| System tools | 24.1k | 12.1% | 사용 가능한 도구 정의 |
| MCP tools | 4.0k | 2.0% | MCP 서버 도구들 |
| Custom agents | 1.6k | 0.8% | 사용자 정의 에이전트 |
| Memory files | 4.1k | 2.1% | CLAUDE.md 등 메모리 파일 |
| Skills | 803 | 0.4% | 스킬 정의 |
| Messages | 8 | 0.0% | 현재 대화 메시지 |
| **Free space** | **116k** | **58.2%** | 남은 공간 |
| Autocompact buffer | 45.0k | 22.5% | 자동 압축용 버퍼 |

---

### 2. MCP Tools (`/mcp`)

MCP(Model Context Protocol) 서버에서 제공하는 **파일 시스템 도구들**입니다.

```
mcp_morphllm-fast-apply__read_file: 230 tokens
mcp_morphllm-fast-apply__tiny_edit_file: 274 tokens
mcp_sequential-thinking__sequentialthinking: 1.1k tokens
mcp_context7__query-docs: 408 tokens
```

이 도구들은 Claude가 파일을 읽고, 수정하고, 디렉토리를 탐색할 수 있게 해주는 MCP 서버 기능입니다. `morphllm-fast-apply`는 빠른 파일 편집 도구, `context7`은 문서 검색 도구로 보입니다.

---

### 3. Custom Agents (`/agents`)

사용자가 정의한 **전문 에이전트들**입니다. 특정 역할에 특화된 프롬프트가 포함되어 있습니다.

**Project 레벨 에이전트:**

| 에이전트 | 토큰 | 용도 추정 |
|----------|------|----------|
| system-architect | 125 | 시스템 설계 |
| requirements-analyst | 125 | 요구사항 분석 |
| frontend-developer | 111 | 프론트엔드 개발 |
| quality-engineer | 110 | 품질 관리 |
| socratic-mentor | 108 | 소크라테스식 질문/교육 |
| devops-architect | 86 | DevOps 아키텍처 |

**User 레벨 에이전트:**

| 에이전트 | 토큰 | 용도 추정 |
|----------|------|----------|
| java-testing-expert | 65 | Java 테스트 전문가 |
| java-expert | 63 | Java 개발 전문가 |
| tps-ticket-management | 58 | 티켓 관리 시스템 |

---

### 4. Memory Files (`/memory`)

프로젝트와 사용자에 대한 **지속적인 컨텍스트**를 저장하는 파일들입니다.

```
~/.claude/CLAUDE.md: 2.2k tokens  ← 전역 사용자 설정
CLAUDE.md: 1.9k tokens            ← 프로젝트별 설정
```

이 파일들에는 프로젝트 구조, 코딩 컨벤션, 자주 사용하는 명령어 등이 기록됩니다.

---

### 5. Skills (`/skills`)

Claude Code가 특정 작업을 수행할 때 참조하는 **스킬 정의**입니다.

**Project 스킬:**

```
skill-creator: 47 tokens          ← 새 스킬 생성 가이드
research-plan-implement: 34 tokens
sc:implement, sc:design, sc:analyze...  ← 슬래시 커맨드용 스킬
```

**User 스킬:**

```
sc:design: 26 tokens
sc:index: 26 tokens
sc:brainstorm: 25 tokens
...
```

`sc:` 접두사가 붙은 것들은 `/design`, `/analyze` 같은 슬래시 커맨드로 호출할 수 있는 스킬들입니다.

---

## 시각적 표현 (상단 그리드)

```
⊚ ⊚ ⊚ ⊚ ⊚ ⊚ ⊚ ⊚    ⊚ System prompt
⊚ ⊚ ● ● ● ⊚ ⊚ ⊚    ● MCP tools  
◇ ◇ ◇ ◇ ◇ ◇ ◇ ◇    ◇ Custom agents
⊞ ⊞ ⊞ ⊞ ⊞ ⊞ ⊞ ⊞    ⊞ Memory files
▢ ▢ ▢ ▢ ▢ ▢ ▢ ▢    ▢ Free space
```

각 셀이 토큰 블록을 나타내며, 한눈에 컨텍스트 분포를 파악할 수 있습니다.

---

## 새 대화에도 컨텍스트가 존재하는 이유

**Messages: 8 tokens (0.0%)** ← 실제 대화 내용은 이것뿐입니다.

나머지는 모두 **대화와 무관하게 항상 로드되는 "인프라"**입니다.

### 컨텍스트 구성 요소의 성격

```
┌─────────────────────────────────────────────────────────────┐
│                    매 대화마다 자동 로드                       │
│  (새 대화를 시작해도 항상 존재)                                │
├─────────────────────────────────────────────────────────────┤
│  System prompt     → Claude의 기본 행동 규칙                  │
│  System tools      → bash, 파일 읽기/쓰기 등 기본 도구 정의     │
│  MCP tools         → 연결된 MCP 서버의 도구들                  │
│  Custom agents     → 프로젝트/사용자 에이전트 정의              │
│  Memory files      → CLAUDE.md (프로젝트 컨텍스트)            │
│  Skills            → 슬래시 커맨드 스킬 정의                   │
├─────────────────────────────────────────────────────────────┤
│                    대화 중 누적                               │
│  (새 대화 시작하면 리셋)                                       │
├─────────────────────────────────────────────────────────────┤
│  Messages          → 실제 주고받은 대화 내용                   │
│                      (현재 8 tokens = 거의 비어있음)           │
└─────────────────────────────────────────────────────────────┘
```

### 비유: 웹 애플리케이션

| Claude Code | 웹 앱 비유 |
|-------------|-----------|
| System prompt | 프레임워크 코드 |
| System/MCP tools | 라이브러리, SDK |
| Custom agents | 플러그인 |
| Memory files | 설정 파일 (config) |
| Skills | 유틸리티 함수 |
| **Messages** | **사용자 세션 데이터** |

새 브라우저 탭을 열어도 프레임워크와 라이브러리는 다시 로드되는 것처럼, 새 대화를 시작해도 Claude Code의 기반 시스템은 매번 컨텍스트에 주입됩니다.

---

## 실제 "가용 공간" 계산

```
전체: 200k tokens
- 인프라: ~39k (19%)
- Autocompact buffer: 45k (22.5%)  ← 압축용 예약 공간
─────────────────────────────
실제 대화용: ~116k (58%)
```

새 대화를 시작해도 약 **40%는 이미 사용된 상태**로 시작하는 것입니다. 이게 Claude Code가 프로젝트 컨텍스트를 "기억"하면서도 도구를 사용할 수 있는 이유입니다.

---

## 실용적 활용

이 정보를 바탕으로:

1. **컨텍스트가 부족할 때** → 불필요한 에이전트/스킬 비활성화
2. **대화가 길어질 때** → `/compact` 명령어로 압축
3. **MCP 도구가 많을 때** → 필요한 MCP 서버만 연결
