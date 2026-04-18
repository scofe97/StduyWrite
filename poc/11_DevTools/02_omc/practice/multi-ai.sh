#!/bin/bash
# Claude(주) + Codex(보조) 교차 검증 세션
# ┌──────────────┬──────────────┐
# │   Claude     │    Codex     │
# │   (주 실행)   │  (교차 검증)  │
# └──────────────┴──────────────┘

SESSION="multi-ai"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux attach -t "$SESSION"
    exit 0
fi

tmux new-session -s "$SESSION" -d
tmux split-window -h -t "$SESSION"

# 양쪽 패인 모두 ~/claude로 이동
tmux send-keys -t "$SESSION:0.0" 'cd ~/claude' Enter
tmux send-keys -t "$SESSION:0.1" 'cd ~/claude' Enter

# Claude 좌측(주): 권한 스킵, Codex 우측(보조): untrusted 승인 모드
tmux send-keys -t "$SESSION:0.0" 'claude --dangerously-skip-permissions' Enter
tmux send-keys -t "$SESSION:0.1" 'codex -a untrusted' Enter

# 50:50 균등 분할 (기본값이므로 resize 불필요)

tmux attach -t "$SESSION"
