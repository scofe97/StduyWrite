# OMC 명령어 Quick Reference

실습 시 빠르게 참조할 수 있는 명령어 모음입니다.

---

## 설치 확인

```bash
# 플러그인
grep -q "oh-my-claudecode" ~/.claude/settings.json && echo "Plugin: OK"

# HUD
[ -f ~/.claude/hud/omc-hud.mjs ] && echo "HUD: OK"

# CLI
omc --version

# AST Tools
npx @ast-grep/napi --help > /dev/null 2>&1 && echo "AST: OK"

# MCP
[ -f ~/.mcp.json ] && echo "MCP: OK"
```

---

## 실행 모드 활성화

| 모드 | 활성화 방법 |
|------|------------|
| **Autopilot** | "완료될 때까지 멈추지 마" |
| **Ralph** | `ralph: 작업 설명` |
| **Ultrawork** | `ulw 작업 설명` |
| **Plan** | `plan 작업 설명` |
| **Ralplan** | `ralplan 작업 설명` |
| **Ultrapilot** | `ultrapilot: 작업 설명` |
| **Swarm** | `/oh-my-claudecode:swarm` |
| **Ecomode** | `/oh-my-claudecode:ecomode` |

---

## 작업 중단

```bash
# 키보드
Ctrl+C

# 자연어
"stop", "cancel", "멈춰"

# 명령어
/oh-my-claudecode:cancel
```

---

## HUD 제어

```bash
# 프리셋 변경
/oh-my-claudecode:hud minimal
/oh-my-claudecode:hud focused
/oh-my-claudecode:hud full

# HUD 초기 설정
/oh-my-claudecode:hud setup

# 진단
/oh-my-claudecode:doctor
```

---

## CLI 분석

```bash
# 종합 대시보드
omc

# 토큰 통계
omc stats
omc stats --days 7
omc stats --json

# 에이전트별 비용
omc agents

# 대화형 대시보드
omc tui

# 과거 데이터 채우기
omc backfill
```

---

## LSP 도구

```
# 타입/문서 조회
lsp_hover: file="src/auth.ts", line=10, character=5

# 정의 위치 이동
lsp_goto_definition: file="src/auth.ts", line=10, character=5

# 참조 검색
lsp_find_references: file="src/auth.ts", line=10, character=5

# 파일 진단 (에러/경고)
lsp_diagnostics: file="src/auth.ts"

# 프로젝트 전체 진단
lsp_diagnostics_directory: directory="src/"

# 심볼 목록
lsp_document_symbols: file="src/auth.ts"

# 워크스페이스 심볼 검색
lsp_workspace_symbols: query="UserService"

# 리네임
lsp_rename: file="src/auth.ts", line=10, character=5, newName="newVarName"
```

---

## AST Grep 패턴

```bash
# React useState 찾기
ast_grep_search: pattern="useState($INIT)", language="tsx"

# useEffect 찾기
ast_grep_search: pattern="useEffect($$$ARGS)", language="tsx"

# console.log → logger.info 변환
ast_grep_replace: pattern="console.log($MSG)", replacement="logger.info($MSG)", language="js"

# var → const 변환
ast_grep_replace: pattern="var $NAME = $VALUE", replacement="const $NAME = $VALUE", language="js"

# 함수 선언 찾기
ast_grep_search: pattern="async function $NAME($$$ARGS) { $$$BODY }", language="ts"

# Java 어노테이션 찾기
ast_grep_search: pattern="@Service", language="java"
```

### 와일드카드 문법

| 메타변수 | 의미 | 예시 |
|---------|------|------|
| `$NAME` | 단일 AST 노드 | `useState($INIT)` |
| `$$$ARGS` | 0개 이상 노드 | `console.log($$$ARGS)` |

---

## Multi-AI tmux 레이아웃

```bash
# 세션 생성
tmux new-session -s multi-ai -d

# 3분할 (Claude / Gemini / Codex)
tmux split-window -h -t multi-ai
tmux split-window -v -t multi-ai:0.1

# AI CLI 배치
tmux send-keys -t multi-ai:0.0 'claude' Enter
tmux send-keys -t multi-ai:0.1 'gemini' Enter
tmux send-keys -t multi-ai:0.2 'codex' Enter

# 세션 연결
tmux attach -t multi-ai
```

---

## 비용 구조 (참조)

| 모델 | 입력 (per 1M) | 출력 (per 1M) | 배수 |
|------|--------------|--------------|------|
| Haiku | $0.25 | $1.25 | 1x |
| Sonnet | $3 | $15 | 12x |
| Opus | $15 | $75 | 60x |

---

## 모드 선택 빠른 판단

```
긴급 버그 → Ralph
새 기능 설계 → Plan → Ralplan
대규모 구현 → Ultrapilot
대규모 반복 → Swarm
비용 절감 → Ecomode 조합
단순 작업 → Autopilot
보안 민감 → Claude + Gemini + Codex
```
