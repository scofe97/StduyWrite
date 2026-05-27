# 05. 실전 워크플로우

일상 개발에서 tmux + Claude Code 활용 패턴

---

## 목표

- [ ] 일일 개발 루틴 구축
- [ ] 프로젝트별 세션 관리
- [ ] 자주 쓰는 레이아웃 자동화

---

## 1. 일일 개발 루틴

### 아침: 작업 시작

```bash
# 1. 기존 세션 확인
tmux ls

# 2. 세션이 있으면 연결, 없으면 생성
tmux a -t project || tmux new -s project
```

### 저녁: 작업 종료

```bash
# 세션 유지하고 나가기 (내일 이어서)
Ctrl+A, d

# 또는 완전히 종료
exit
```

---

## 2. 프로젝트별 세션 관리

### 권장 명명 규칙

```bash
tmux new -s tps-frontend    # TPS 프론트엔드
tmux new -s tps-backend     # TPS 백엔드
tmux new -s study           # 학습용
tmux new -s personal        # 개인 프로젝트
```

### 세션 간 전환

```bash
# 외부에서
tmux a -t tps-frontend

# tmux 안에서
Ctrl+A, s    # 세션 목록 표시, 선택하여 전환
```

---

## 3. 자주 쓰는 레이아웃 스크립트

### ~/.tmux-layouts.sh

```bash
#!/bin/bash

# Claude Code + Shell 기본 레이아웃
claude_dev() {
  tmux new-session -d -s "$1" -c "$2"
  tmux split-window -h -t "$1"
  tmux select-pane -t "$1:0.0"
  tmux send-keys -t "$1:0.0" "claude" Enter
  tmux attach -t "$1"
}

# Fullstack 레이아웃 (Claude + Server + Shell)
fullstack() {
  tmux new-session -d -s "$1" -c "$2"
  tmux split-window -v -l 30% -t "$1"
  tmux split-window -h -t "$1:0.1"
  tmux select-pane -t "$1:0.0"
  tmux send-keys -t "$1:0.0" "claude" Enter
  tmux attach -t "$1"
}

# 사용법 표시
if [ -z "$1" ]; then
  echo "Usage:"
  echo "  source ~/.tmux-layouts.sh"
  echo "  claude_dev <session-name> <directory>"
  echo "  fullstack <session-name> <directory>"
fi
```

### 사용 방법

```bash
# 스크립트 로드
source ~/.tmux-layouts.sh

# Claude Code 개발 환경
claude_dev tps ~/okestro/tps-gitlab/react-app

# Fullstack 환경
fullstack myproject ~/projects/myproject
```

---

## 4. 실전 시나리오

### 시나리오 A: 프론트엔드 개발

```bash
# 세션 생성
tmux new -s frontend

# 레이아웃 설정
# Pane 0: Claude Code
# Pane 1: npm run dev
# Pane 2: git/shell

Ctrl+A, %     # 수평 분할
Ctrl+A, "     # Pane 1 수직 분할

# Pane 0에서
claude

# Pane 1에서
npm run dev

# Pane 2에서 git 작업
```

### 시나리오 B: 백엔드 디버깅

```
┌────────────────────────┐
│     Claude Code        │
├───────────┬────────────┤
│ Server    │ DB/Logs    │
│ ./gradlew │ tail -f    │
└───────────┴────────────┘
```

Claude에게:
- "아래 서버 로그에서 에러를 찾아줘"
- "DB 쿼리 결과를 분석해줘"

### 시나리오 C: 코드 리뷰

```bash
# Window 0: 원본 코드
# Window 1: Claude Code 리뷰

Ctrl+A, c    # 새 window
Ctrl+A, 0    # Window 0으로 (코드 확인)
Ctrl+A, 1    # Window 1로 (Claude와 논의)
```

---

## 5. 트러블슈팅

### 세션이 보이지 않음

```bash
# 서버 상태 확인
tmux ls

# "no server running" → tmux 서버가 꺼진 상태
# 새 세션 생성 필요
```

### Claude Code 세션 복구

```bash
# Claude Code 자체 세션 이어하기
claude -c

# tmux 세션과 별개로 관리됨
```

### 복사/붙여넣기 문제

```bash
# ~/.tmux.conf에 추가
set -g mouse on

# 또는 Shift 누른 상태에서 드래그
```

---

## 6. 핵심 단축키 치트시트

### 세션
| 단축키/명령 | 동작 |
|-------------|------|
| `tmux new -s NAME` | 세션 생성 |
| `tmux a -t NAME` | 세션 연결 |
| `Ctrl+A, d` | detach |
| `Ctrl+A, s` | 세션 목록 |

### Pane
| 단축키 | 동작 |
|--------|------|
| `Ctrl+A, %` | 수평 분할 |
| `Ctrl+A, "` | 수직 분할 |
| `Ctrl+A, 방향키` | pane 이동 |
| `Ctrl+A, z` | zoom |

### Window
| 단축키 | 동작 |
|--------|------|
| `Ctrl+A, c` | 새 window |
| `Ctrl+A, n/p` | 다음/이전 |
| `Ctrl+A, 숫자` | 해당 window |

### Claude Code 안에서
| 동작 | 방법 |
|------|------|
| tmux 단축키 | `Ctrl+A` (Prefix 변경으로 충돌 없음) |
| pane 참조 | `tmux 0.1` 형식 |

---

## 완료!

이제 tmux + Claude Code 통합 환경을 마스터했습니다.

### 다음 단계 (선택)

- [ ] tmux 플러그인 관리자 (tpm) 설치
- [ ] tmux-resurrect로 세션 영구 저장
- [ ] 커스텀 키바인딩 설정

---

## 학습 완료 체크리스트

- [ ] tmux 설치 및 기본 설정
- [ ] Session/Window/Pane 개념 이해
- [ ] 세션 생성/연결/분리/종료
- [ ] 화면 분할 및 이동
- [ ] Claude Code와 tmux 통합
- [ ] 실전 워크플로우 구축

**축하합니다!** 🎉
