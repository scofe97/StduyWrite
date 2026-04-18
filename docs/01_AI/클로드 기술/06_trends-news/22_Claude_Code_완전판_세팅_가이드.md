# 클로드 전문가의 클로드 코드 완전판 세팅

> 더 많이가 아니라, 정확히 필요한 것만

> 출처: affaan(@affaanmustafa) — 앤트로픽 해커톤 우승자, 10개월간 매일 Claude Code 사용

---

## 핵심 원칙

이 가이드를 읽는 순간 "내가 지금까지 뭘 한 거지?" 싶었다. 핵심은 명확하다. **과도한 설정은 독이며, 필요한 도구만 켜두는 것이 진짜 생산성**이다.

---

## 1. 컨텍스트 200k는 이론에 불과 — 진짜는 70k

Claude Code의 200k 컨텍스트는 이론치다. **MCP와 플러그인 너무 많이 켜두면 실사용은 70k까지 떨어진다.**

### affaan의 원칙

| 규칙 | 수치 |
|------|------|
| MCP 설정 | 14개를 config에 등록 |
| 프로젝트별 활성화 | **5~6개만** |
| 동시 활성 툴 | **80개 미만** |

### 실제 적용 방법

```json
// settings.json
{
  "mcpServers": {
    "github": { ... },
    "supabase": { ... },
    "vercel": { ... },
    "railway": { ... },
    "cloudflare-workers": { ... },
    "cloudflare-kv": { ... },
    "clickhouse": { ... }
    // ... 총 14개 등록
  },
  "disabledMcpServers": [
    "clickhouse",
    "railway"
    // 현재 프로젝트에서 안 쓰는 것은 명시적으로 비활성화
  ]
}
```

> 직접 적용하니 응답 품질이 확실히 올라갔다. 사용하지 않는 MCP가 컨텍스트를 잡아먹고 있었던 것이다.

---

## 2. Skills vs Hooks vs Subagents — 역할 분담이 핵심

처음엔 헷갈리지만 명확한 차이가 있다.

| 구분 | 위치 | 역할 | 예시 |
|------|------|------|------|
| **Skills** | `~/.claude/skills/` | 명령어 한 줄로 워크플로우 실행 | `/refactor-clean` |
| **Hooks** | 이벤트 기반 자동화 | 특정 시점에 자동 실행 | .ts 수정 후 자동 prettier |
| **Subagents** | `~/.claude/agents/` | 역할별 위임 | planner, architect, tdd-guide |

### Hooks 배치 전략

affaan은 Hooks를 3개 시점에 배치해서 자동화했다. 보리스 체니도 안내한 내용이다.

| Hook 시점 | 자동화 내용 |
|-----------|------------|
| **PreToolUse** | 파일 수정 전 검증 |
| **PostToolUse** | 포매팅, 타입 체크 |
| **Stop** | 보안 감사, console.log 검출 |

> `hookify` 플러그인으로 대화형으로 Hook을 생성할 수도 있다.

---

## 3. mgrep과 Git Worktrees가 게임 체인저

실용 팁 중 진짜 임팩트 있었던 것들.

### mgrep

ripgrep보다 정확하고 **웹 검색도 지원**한다.

```bash
/mgrep 'function handleSubmit'
# 로컬 + 웹 통합 검색 한 줄로 완료
```

### Git Worktrees

여러 feature를 동시 작업할 때 독립 체크아웃을 만들고 각각에서 Claude를 실행한다.

```bash
git worktree add ../feature-auth feature/auth
git worktree add ../feature-dashboard feature/dashboard
# 각 디렉토리에서 별도 Claude Code 세션 실행
```

- `/fork`로 대화 분기도 가능
- git worktrees vs repo clone 에 대해서는 의견이 나뉜다

### Zed 에디터

| 특징 | 설명 |
|------|------|
| Rust 기반 | 가볍다 |
| Agent Panel | Claude 수정 파일 실시간 트래킹 |
| CMD+Shift+R | 커스텀 커맨드 바로 실행 |

---

## 4. Rules 구조로 일관성 확보

`~/.claude/rules/`를 **관심사별로 모듈화**한다.

| 파일 | 역할 | 예시 규칙 |
|------|------|-----------|
| `security.md` | 보안 | 시크릿 하드코딩 금지 |
| `coding-style.md` | 코딩 스타일 | 불변성, 파일 구조 |
| `testing.md` | 테스트 | TDD, 80% 커버리지 |
| `git-workflow.md` | Git | 커밋 포맷 |
| `performance.md` | 성능 | 모델 선택 기준 |

> "console.log 절대 커밋 금지" 같은 규칙을 여기 넣고, **Stop Hook으로 감사**하면 실수가 사라진다.

### Rules + Hooks 연동 패턴

```
Rules에 규칙 정의
  → Stop Hook이 규칙 위반 자동 검출
  → 위반 시 에이전트에게 피드백
  → 에이전트가 자동 수정
```

이것은 [16번 — AI 루프와 채점 시스템](16_AI_루프와_채점_시스템.md)에서 다룬 "채점 도구 + 채점 기준"의 구체적 구현이다.

---

## 5. affaan의 5가지 핵심 원칙

| # | 원칙 | 설명 |
|---|------|------|
| 1 | **설정을 fine-tuning처럼** | 아키텍처처럼 거대하게 다루지 마라 |
| 2 | **컨텍스트 윈도우는 귀중하다** | 사용 안 하는 건 끄기 |
| 3 | **병렬 실행 활용** | fork, worktrees |
| 4 | **반복 작업 자동화** | Hooks |
| 5 | **Subagent 스코프 제한** | 역할을 좁게 정의 |

---

## 추가 의견: 브라우저 도구

원문에서는 Playwright 등을 추천하지만, 개인적으로 **Vercel의 agent-browser가 훨씬 안정적**이었다. 작업의 속도와 범위가 다르다고 느꼈다.

---

## 정리

| 항목 | 내용 |
|------|------|
| **핵심** | 더 많이가 아니라, 정확히 필요한 것만 |
| **컨텍스트** | 200k 이론치, MCP 과다 시 70k까지 하락 |
| **MCP 전략** | 14개 등록, 프로젝트별 5~6개만 활성화 |
| **자동화 3종** | Skills(명령), Hooks(이벤트), Subagents(위임) |
| **실용 도구** | mgrep(통합 검색), Git Worktrees(병렬 작업), Zed(경량 에디터) |
| **일관성** | Rules 모듈화 + Stop Hook 감사 |

> 모든 사람이 잘 못하는 게 덜어내는 것이다. 복사보다는 '왜'를 이해하고 자기 워크플로우에 맞게 조정하는 게 핵심이다.
