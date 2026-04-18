# Claude Opus 4.6 업데이트 정리

> 출처: Anthropic 공식 발표, Claude Code Docs
> 정리일: 2026-02-06

---

## 핵심 요약

Claude Opus 4.6 (2026.02.05 출시)의 주요 변화:

- **Claude Code**: Agent Teams, Memory, Summarize from here
- **API**: Adaptive Thinking, Effort Control, Context Compaction
- **오피스**: Excel 개선, PowerPoint (연구 미리보기)
- **인프라**: US-Only Inference, 1M 컨텍스트

---

## Agent Teams 완전 가이드

### 개요

여러 Claude Code 인스턴스가 **팀으로 협업**합니다.

- **Team Lead**: 작업 조정, 태스크 할당, 결과 종합
- **Teammates**: 독립 컨텍스트에서 병렬 작업
- **Task List**: 공유 작업 목록
- **Mailbox**: 에이전트 간 메시지 시스템

### 활성화

```bash
# 환경변수
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### 디스플레이 모드

**in-process (기본)**
- 모든 팀원이 메인 터미널에서 실행
- 어떤 터미널에서든 작동

**split panes**
- 각 팀원이 별도 창에서 실행
- tmux 또는 iTerm2 필요

```json
// settings.json
{
  "teammateMode": "in-process"  // 또는 "tmux", "auto"
}
```

```bash
# 단일 세션에서 모드 지정
claude --teammate-mode in-process
```

### 키보드 단축키

- `Shift+Up/Down`: 팀원 선택
- `Enter`: 선택한 팀원 세션 보기
- `Escape`: 현재 작업 중단
- `Ctrl+T`: 태스크 리스트 토글
- `Shift+Tab`: Delegate Mode 전환

### TeammateTool 명령어

**팀 생성**
```javascript
Teammate({ operation: "spawnTeam", team_name: "my-team" })
```

**팀원 생성**
```javascript
Task({
  team_name: "my-team",
  name: "worker",
  subagent_type: "general-purpose",
  prompt: "작업 설명...",
  run_in_background: true
})
```

**메시지 전송**
```javascript
// 특정 팀원에게
Teammate({ operation: "write", target_agent_id: "worker-1", value: "메시지" })

// 전체 브로드캐스트 (비용 주의)
Teammate({ operation: "broadcast", value: "전체 메시지" })
```

**종료 요청**
```javascript
Teammate({ operation: "requestShutdown", target_agent_id: "worker-1" })
```

**팀 정리**
```javascript
Teammate({ operation: "cleanup" })
```

### 환경변수 (팀 내부)

- `CLAUDE_CODE_TEAM_NAME`: 팀 이름
- `CLAUDE_CODE_AGENT_ID`: 에이전트 ID
- `CLAUDE_CODE_AGENT_TYPE`: 에이전트 타입

### 저장 위치

- 팀 설정: `~/.claude/teams/{team-name}/config.json`
- 태스크 리스트: `~/.claude/tasks/{team-name}/`

### Delegate Mode

Lead가 직접 구현하지 않고 **조정만** 하도록 제한합니다.

```
# 팀 시작 후 Shift+Tab으로 활성화
```

사용 가능 도구: 팀원 생성, 메시지, 종료, 태스크 관리만

### Plan Approval 요구

팀원이 구현 전 **계획 승인**을 받도록 설정:

```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

승인 기준 지정 가능:
```
"only approve plans that include test coverage"
"reject plans that modify the database schema"
```

### 적합한 케이스

1. **연구 및 리뷰**: 여러 관점에서 동시 분석
2. **새 모듈/기능**: 병렬로 독립 컴포넌트 개발
3. **디버깅**: 경쟁 가설 동시 탐색
4. **크로스레이어**: 프론트/백/DB 동시 작업

### Subagent vs Agent Teams

| 항목 | Subagents | Agent Teams |
|------|-----------|-------------|
| 컨텍스트 | 자체 윈도우, 결과만 반환 | 완전 독립 |
| 통신 | 메인에게만 보고 | 팀원 간 직접 메시지 |
| 조정 | 메인이 모든 작업 관리 | 공유 태스크로 자체 조정 |
| 적합 | 결과만 필요한 집중 작업 | 토론/협업 필요한 복잡 작업 |
| 토큰 | 낮음 (요약되어 반환) | 높음 (각각 별도 인스턴스) |

### 사용 예시

**병렬 코드 리뷰**
```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

**경쟁 가설 디버깅**
```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses.
Have them talk to each other to try to disprove each other's theories,
like a scientific debate.
```

### 제한사항

- 세션 재개(resume) 미지원 (in-process 모드)
- 중첩 팀(nested teams) 불가
- 세션당 하나의 팀만 가능
- Lead 변경 불가
- Split panes: VS Code 터미널, Windows Terminal, Ghostty 미지원

### Best Practices

1. **충분한 컨텍스트 제공**: 팀원은 Lead의 대화 히스토리 상속 안 함
2. **적절한 태스크 크기**: 너무 작으면 오버헤드 > 이득, 너무 크면 낭비 위험
3. **팀원 완료 대기**: Lead가 직접 구현하면 "Wait for your teammates"
4. **파일 충돌 방지**: 팀원별로 다른 파일 담당
5. **모니터링**: 진행 상황 체크, 방향 수정

---

## 실험 기능 환경변수 전체 목록

| 환경변수 | 기본값 | 설명 |
|----------|--------|------|
| CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS | 0 | 멀티에이전트 팀 |
| CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS | 0 | 실험 기능 전체 끄기 |
| CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD | 0 | 추가 디렉토리 CLAUDE.md |
| CLAUDE_CODE_ENABLE_TASKS | true | 새 Task 시스템 |
| CLAUDE_CODE_DISABLE_BACKGROUND_TASKS | 0 | 백그라운드 작업 끄기 |
| CLAUDE_CODE_TMPDIR | 시스템 기본 | 임시 파일 경로 |
| CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS | - | 파일 읽기 토큰 제한 |

---

## Claude Code 기타 신기능

### Memory (Persistent)

세션 간 정보를 **자동으로 기억**합니다.

스코프: user (모든 프로젝트) / project (현재 프로젝트) / local (현재 세션)

### Summarize from here

```
/summarize from here
```

긴 세션에서 특정 지점부터 요약.

### Hook Events 추가

- `TeammateIdle`: 팀원 유휴 상태
- `TaskCompleted`: 작업 완료

### 기타

- PDF 페이지 지정: `pages: "1-5"`
- 키바인딩 커스텀: `/keybindings`
- 추가 디렉토리 스킬 자동 로드

---

## API 신기능

### Adaptive Thinking

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[...]
)
```

Deprecated: `thinking: {type: "enabled"}`, `budget_tokens`

### Effort Control

| 레벨 | 동작 | 적합한 작업 |
|------|------|-------------|
| low | 사고 건너뛸 수 있음 | 간단한 질문 |
| medium | 적절한 깊이 | 일반 코딩 |
| high (기본) | 거의 항상 사고 | 복잡한 버그 |
| max | 최대 사고 시간 | 시스템 설계 |

### Context Compaction (베타)

```python
response = client.messages.create(
    model="claude-opus-4-6",
    extra_headers={"anthropic-beta": "compact-2026-01-12"},
    context_management={"edits": ["compact_20260112"]},
    compaction_control={
        "enabled": True,
        "context_token_threshold": 100000,
    },
    messages=[...]
)
```

### US-Only Inference

```python
response = client.messages.create(
    model="claude-opus-4-6",
    region="us-only",  # 1.1x 가격
    messages=[...]
)
```

---

## 오피스 통합

- **Excel**: 장시간 작업 처리 개선, 비정형 데이터 자동 구조화
- **PowerPoint (연구 미리보기)**: 슬라이드 디자인/스타일 유지, 템플릿 기반 생성

---

## 스펙 비교

| 항목 | Opus 4.5 | Opus 4.6 |
|------|----------|----------|
| 컨텍스트 윈도우 | 200K | 1M (베타) |
| 최대 출력 토큰 | 64K | 128K |
| Agent Teams | X | O (실험) |
| Adaptive Thinking | X | O |
| Context Compaction | X | O (베타) |

---

## 벤치마크

| 벤치마크 | Opus 4.5 | Opus 4.6 | GPT-5.2 |
|----------|----------|----------|---------|
| Terminal Bench | 59.8% | 65.4% | - |
| OSWorld | 66.3% | 72.7% | - |
| ARC AGI 2 | 37.6% | 68.8% | 54.2% |
| GDPval-AA | - | +144 Elo | 기준 |

---

## 가격

| 구분 | 입력 | 출력 |
|------|------|------|
| 표준 (200k 이하) | $5/M | $25/M |
| 확장 (200k 초과) | $10/M | $37.50/M |
| US-Only | x1.1 | x1.1 |

---

## 당장 시도할 것

```bash
# 1. Agent Teams 활성화
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# 2. 팀 생성 테스트
"Create an agent team with 3 teammates to review this module"

# 3. Delegate Mode
# Shift+Tab으로 전환

# 4. 키보드 단축키
# Shift+Up/Down: 팀원 선택
# Ctrl+T: 태스크 리스트
```

---

## 참고 링크

- [Anthropic 공식 발표](https://www.anthropic.com/news/claude-opus-4-6)
- [Claude Code Docs - Agent Teams](https://code.claude.com/docs/en/agent-teams)
- [Claude Code Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)
- [Claude API Docs - Adaptive Thinking](https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking)
- [TechCrunch](https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/)
