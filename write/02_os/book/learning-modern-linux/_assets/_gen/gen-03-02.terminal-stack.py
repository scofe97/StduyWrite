# 03-02 §6 끝 — 터미널·셸·멀티플렉서를 한 벌로 묶은 저자의 구성.
# 원문(사이드바 "BRINGING IT ALL TOGETHER: TERMINAL, TMUX, AND SHELL"):
#       "I'm using Alacritty as my terminal ... to configure it I'm using a YAML configuration file that
#       I can version in Git, allowing me to use it on any target system in seconds."
#       alacritty.yml 의 shell 설정이 program: /usr/local/bin/fish 이고 args 가 -l · -i · -c ·
#       "tmux new-session -A -s zzz" 다. 저자의 설명 — "I configure Alacritty to use fish as the default
#       shell, but also, when I launch the terminal, it automatically attaches to a specific session.
#       Together with the tmux-continuum plug-in, this gives me peace of mind. Even if I switch off the
#       computer, once I restart I find my terminal with all its sessions, windows, and panes (almost)
#       exactly in the state it was in before a crash, besides the shell variables."
#       tmux-continuum 은 "Automatically saves/restores a session (15-minute interval)".
# 타입 스펙: type-layers — 위아래로 쌓인 층. accent 는 저자가 안심의 근거로 든 한 층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §6",
      "터미널이 셸을 띄우고 셸이 세션에 붙는다",
      "저자가 alacritty.yml 한 파일로 묶어 둔 구성을 층으로 편 것. 터미널이 띄우는 것은 셸이고, "
      "그 셸이 시작 명령으로 tmux 세션에 붙는 순서다.",
      "설정 파일을 Git 에 두면 어느 기계에서든 몇 초 만에 같은 환경이 섭니다")

X, BOX_W = 76, 728
layers = [
    ("L1", "Alacritty", "터미널 · alacritty.yml 을 Git 으로 버전 관리", False),
    ("L2", "fish", "셸 · program 으로 지정되고 -l -i -c 로 실행된다", False),
    ("L3", "tmux new-session -A -s zzz", "있으면 붙고 없으면 만든다 · 이 한 줄이 args 의 마지막", True),
    ("L4", "세션 zzz 의 윈도와 페인", "그 안에서 다시 셸들이 돈다", False),
]

Y0, LH, STRIDE = 128, 76, 88
for i, (tag, name, note, focal) in enumerate(layers):
    y = Y0 + i * STRIDE
    if focal:
        d.tone(X, y, BOX_W, LH, ACC, r=6)
    else:
        d.box(X, y, BOX_W, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 1.0, 6)
    d.t(X + 18, y + 30, tag, 12, SOFT, MONO, "start")
    d.t(X + 68, y + 30, name, 15, ACC if focal else INK,
        MONO if all(ord(c) < 128 for c in name) else KR, "start", 600)
    d.t(X + 68, y + 52, note, 12, MUTED, KR, "start")
    if i < len(layers) - 1:
        d.arrow([(X + BOX_W / 2, y + LH), (X + BOX_W / 2, y + STRIDE - 2)], MUTED, "ar", 1.2)

d.t(X, 500, "여기에 tmux-continuum 플러그인이 15분 간격으로 세션을 저장하고 복원합니다.",
    12, MUTED, KR, "start")
d.t(X, 522, "저자는 컴퓨터를 꺼도 다시 켜면 세션·윈도·페인이 거의 그대로 서 있다고 적습니다. "
            "다만 셸 변수는 예외라고 단서를 붙입니다.", 12, SOFT, KR, "start")

d.legend(542, [("저자가 안심의 근거로 든 층", ACC), ("나머지 층", MUTED)])
d.save("03-02.terminal-stack.svg")
print("ok 03-02.terminal-stack")
