# 00. 환경 설정

tmux 설치 및 기본 환경 구성

---

## 목표

- [ ] tmux 설치 완료
- [ ] 버전 확인
- [ ] 기본 설정 파일 생성

---

## 1. tmux 설치

### macOS (Homebrew)
```bash
brew install tmux
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install tmux
```

---

## 2. 설치 확인

```bash
tmux -V
# 출력 예: tmux 3.4
```

---

## 3. 기본 설정 파일 생성

`~/.tmux.conf` 파일을 생성합니다:

```bash
cat > ~/.tmux.conf << 'EOF'
# 마우스 지원
set -g mouse on

# 스크롤백 버퍼 증가 (기본 2000 → 50000)
set -g history-limit 50000

# 256 색상 지원
set -g default-terminal "screen-256color"

# pane 번호 표시 시간 증가 (3초)
set -g display-panes-time 3000

# 새 window/pane에서 현재 경로 유지
bind c new-window -c "#{pane_current_path}"
bind % split-window -h -c "#{pane_current_path}"
bind '"' split-window -v -c "#{pane_current_path}"
EOF
```

---

## 4. 설정 적용 확인

```bash
# 설정 파일 확인
cat ~/.tmux.conf

# tmux가 실행 중이라면 설정 리로드
tmux source-file ~/.tmux.conf
```

---

## 체크포인트

다음 명령어들이 정상 동작하는지 확인:

```bash
# 1. 버전 확인
tmux -V

# 2. 설정 파일 존재 확인
ls -la ~/.tmux.conf

# 3. tmux 실행 테스트 (바로 종료)
tmux new -s test -d && tmux kill-session -t test && echo "OK"
```

모두 성공하면 다음 단계로 진행: [01-concepts](../01-concepts/)
