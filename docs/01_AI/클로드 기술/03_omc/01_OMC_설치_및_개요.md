# oh-my-claudecode 설치 및 개요

## 개요

oh-my-claudecode(OMC)는 Claude Code CLI의 기능을 확장하는 플러그인입니다. 복잡한 작업을 자동으로 병렬화하고, 지속적으로 실행하며, 실시간 상태를 모니터링할 수 있게 해줍니다.

## 왜 필요한가?

### 기존 Claude Code의 한계
- 복잡한 작업 시 수동으로 여러 번 프롬프트 입력 필요
- 작업 진행 상황 파악 어려움
- 토큰 사용량 추적 불가
- 병렬 처리 수동 관리

### OMC가 해결하는 문제
- **자동 지속 실행**: "완료될 때까지 멈추지 마" 한 마디로 끝까지 실행
- **실시간 모니터링**: HUD로 현재 상태, 컨텍스트 사용량 확인
- **토큰 분석**: CLI로 비용과 사용량 추적
- **지능적 병렬화**: 복잡한 작업을 자동으로 분산 처리

## 설치된 구성 요소

### 1. oh-my-claudecode 플러그인
**위치**: `~/.claude/plugins/cache/omc/oh-my-claudecode/`

Claude Code의 핵심 기능을 확장합니다:
- 자동화 모드 (ralph, ultrawork)
- 계획 수립 인터뷰 (plan, ralplan)
- 스킬 시스템 연동

### 2. HUD (Heads-Up Display)
**위치**: `~/.claude/hud/omc-hud.mjs`

터미널 상태 표시줄에 실시간 정보를 표시합니다:
- 현재 모드 (ralph, ultrawork 등)
- 컨텍스트 사용량 (%)
- 실행 중인 에이전트 수
- 할 일 진행 상황

### 3. OMC CLI
**설치**: `npm install -g oh-my-claude-sisyphus`

터미널에서 토큰 사용량과 비용을 분석합니다:
- `omc stats` - 통계 보기
- `omc agents` - 에이전트별 분석
- `omc tui` - 대화형 대시보드

### 4. AST Tools
**설치**: `npm install -g @ast-grep/napi`

코드 구조를 이해하는 검색/변환 도구:
- 17개 언어 지원
- 패턴 기반 AST 검색
- 구조적 코드 변환

### 5. MCP 서버
**위치**: `~/.mcp.json`

외부 도구와 Claude Code를 연결합니다:
- **Context7**: 라이브러리 문서 실시간 조회
- **Exa**: 향상된 웹 검색

## 설정 파일 위치

| 파일 | 용도 |
|------|------|
| `~/.claude/settings.json` | Claude Code 전역 설정 |
| `~/.claude/hud/omc-hud.mjs` | HUD 스크립트 |
| `~/.mcp.json` | MCP 서버 설정 |
| `.claude/OMC_CLAUDE.md` | 프로젝트별 OMC 설정 |

## 설치 확인

```bash
# 플러그인 확인
grep -q "oh-my-claudecode" ~/.claude/settings.json && echo "OK"

# CLI 확인
omc --version

# HUD 확인
ls ~/.claude/hud/omc-hud.mjs

# MCP 확인
cat ~/.mcp.json
```

## 다음 단계

- [45_OMC_자동화_모드_가이드.md](./45_OMC_자동화_모드_가이드.md) - ralph, ultrawork 사용법
- [46_OMC_HUD_상태표시줄_가이드.md](./46_OMC_HUD_상태표시줄_가이드.md) - HUD 설정
- [47_OMC_CLI_토큰_분석_가이드.md](./47_OMC_CLI_토큰_분석_가이드.md) - 비용 분석
- [48_OMC_MCP_서버_가이드.md](./48_OMC_MCP_서버_가이드.md) - Context7, Exa 활용
