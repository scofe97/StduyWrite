# OMC HUD 상태표시줄 가이드

## 개요

HUD(Heads-Up Display)는 Claude Code 터미널 하단에 실시간 상태 정보를 표시합니다. 현재 모드, 컨텍스트 사용량, 에이전트 상태 등을 한눈에 파악할 수 있습니다.

## 왜 필요한가?

Claude Code 사용 시 다음 정보를 실시간으로 알 수 없었습니다:
- 컨텍스트 창이 얼마나 찼는지
- 어떤 모드가 활성화되어 있는지
- 백그라운드 에이전트가 몇 개 실행 중인지
- 작업 진행률이 어떻게 되는지

HUD는 이 모든 정보를 상태 표시줄 한 줄에 보여줍니다.

## 표시 형식

### Focused 모드 (기본)
```
[OMC] ralph:3/10 | US-002 | ultrawork skill:planner | ctx:67% | agents:2 | bg:3/5 | todos:2/5
```

### 각 요소 설명

| 요소 | 의미 | 예시 |
|------|------|------|
| `[OMC]` | OMC 활성화 표시 | - |
| `ralph:3/10` | ralph 반복 횟수/최대 | 3번째 반복, 최대 10회 |
| `US-002` | 현재 PRD 스토리 ID | - |
| `ultrawork` | 활성 모드 뱃지 | - |
| `skill:planner` | 마지막 실행 스킬 | planner 스킬 사용 중 |
| `ctx:67%` | 컨텍스트 창 사용량 | 67% 사용 |
| `agents:2` | 실행 중인 에이전트 | 2개 에이전트 |
| `bg:3/5` | 백그라운드 작업 | 3개 실행 중, 5개 슬롯 |
| `todos:2/5` | 할 일 진행률 | 2개 완료, 5개 중 |

## 색상 코드

- **초록색**: 정상 상태
- **노란색**: 경고 (컨텍스트 >70%, ralph >7회)
- **빨간색**: 위험 (컨텍스트 >85%, ralph 최대)

## 프리셋 변경

### Minimal (최소)
```
[OMC] ralph | ultrawork | todos:2/5
```

### Focused (기본)
```
[OMC] ralph:3/10 | US-002 | ultrawork skill:planner | ctx:67% | agents:2 | bg:3/5 | todos:2/5
```

### Full (전체)
```
[OMC] ralph:3/10 | US-002 (2/5) | ultrawork | ctx:[████░░]67% | agents:3 | bg:3/5 | todos:2/5
├─ O architect    2m   analyzing architecture patterns...
├─ e explore     45s   searching for test files
└─ s executor     1m   implementing validation logic
```

### 프리셋 변경 명령

```
/oh-my-claudecode:hud minimal
/oh-my-claudecode:hud focused
/oh-my-claudecode:hud full
```

## 설정 파일

**위치**: `~/.claude/.omc/hud-config.json`

```json
{
  "preset": "focused",
  "elements": {
    "omcLabel": true,
    "ralph": true,
    "prdStory": true,
    "activeSkills": true,
    "lastSkill": true,
    "contextBar": true,
    "agents": true,
    "backgroundTasks": true,
    "todos": true,
    "showCache": true,
    "showCost": true,
    "maxOutputLines": 4
  },
  "thresholds": {
    "contextWarning": 70,
    "contextCritical": 85,
    "ralphWarning": 7
  }
}
```

### 주요 설정 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `preset` | 표시 프리셋 | "focused" |
| `contextWarning` | 컨텍스트 경고 임계값 | 70% |
| `contextCritical` | 컨텍스트 위험 임계값 | 85% |
| `maxOutputLines` | 에이전트 상세 표시 줄 수 | 4 |

## 트러블슈팅

### HUD가 표시되지 않을 때

1. **Claude Code 재시작**: 설정 후 재시작 필요
2. **설정 확인**:
```bash
cat ~/.claude/settings.json | grep statusLine
```
3. **HUD 스크립트 확인**:
```bash
ls ~/.claude/hud/omc-hud.mjs
```

### HUD 재설정

```
/oh-my-claudecode:hud setup
```

### 진단 실행

```
/oh-my-claudecode:doctor
```

## 활용 팁

1. **컨텍스트 관리**: ctx가 70%를 넘으면 새 세션 시작 고려
2. **ralph 모니터링**: 반복 횟수가 많으면 문제 재정의 필요
3. **에이전트 추적**: agents 수가 많으면 작업이 병렬화되고 있음

## 관련 문서

- [44_oh-my-claudecode_설치_및_개요.md](./44_oh-my-claudecode_설치_및_개요.md)
- [45_OMC_자동화_모드_가이드.md](./45_OMC_자동화_모드_가이드.md)
