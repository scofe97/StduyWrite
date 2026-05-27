# tmux 실습 명령어 모음

## 세션 관리

```bash
# 세션 생성
tmux new -s practice

# 세션 목록 확인
tmux ls

# 세션 연결 (없으면 생성)
tmux a -t practice || tmux new -s practice

# detach: Ctrl+A, d
# 세션 종료
tmux kill-session -t practice
```

## Pane/Window

```bash
# 수직 분할: Ctrl+A, %
# 수평 분할: Ctrl+A, "
# Pane 이동: Ctrl+A, 방향키
# zoom 토글: Ctrl+A, z
# Pane 닫기: Ctrl+A, x
# Window 생성: Ctrl+A, c
# Window 닫기: Ctrl+A, &
# Window 전환: Ctrl+A, 숫자
```

## Claude Code 통합 레이아웃

```bash
# 3분할 개발 환경
tmux new -s dev \; split-window -v -l 30% \; split-window -h \; select-pane -t 0

# Pane 0: claude (상단)
# Pane 1: dev server (좌하단)
# Pane 2: shell (우하단)
```

## 스크롤 모드 (vi)

```bash
# 진입: Ctrl+A, [
# 이동: j/k, Ctrl+D/U
# 검색: /검색어
# 종료: q
```
