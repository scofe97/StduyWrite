# 03-02 §6 — tmux 가 다루는 세 단위와 그 포함 관계.
# 원문("tmux"): "there are three core elements you're interacting with in tmux, from coarse-grained to
#       fine-grained units" —
#       Sessions: "A logical unit that you can think of as a working environment dedicated to a specific
#                 task ... It's the container for all other units."
#       Windows:  "You can think of a window as a tab in a browser, belonging to a session. It's optional
#                 to use, and often you only have one window per session."
#       Panes:    "These are your workhorses, effectively a single shell instance running. A pane is part
#                 of a window, and you can easily split it vertically or horizontally, as well as
#                 expand/collapse it (think: zoom) and close panes as you need them."
#       그리고 클라이언트·서버 모델 — "tmux is running as a server, and you find yourself in a shell
#       you've configured in tmux, running as the client. This client/server model allows you to create,
#       enter, leave, and destroy sessions."
# 타입 스펙: type-nested — 포함 관계로 드러나는 경계. accent 는 실제로 일이 벌어지는 가장 안쪽 단위.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 596
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §6",
      "세션이 윈도를 담고 윈도가 페인을 담는다",
      "tmux 의 세 단위를 큰 것에서 작은 것으로 포갠 것. 세션은 다른 모든 단위를 담는 그릇이고, "
      "실제로 셸이 도는 곳은 가장 안쪽의 페인이다.",
      "붙었다 뗄 수 있는 단위는 세션입니다")

RX, RY, RW, RH = 28, 140, 800, 288
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
_lbl = "세션 — 특정 일에 바친 작업 환경 하나"
_w = sum(12 if "가" <= c <= "힣" else 7 for c in _lbl) + 16
d.o.append(f'<rect x="{RX + 16}" y="{RY - 8}" width="{_w}" height="16" fill="{PAPER}"/>')
d.t(RX + 24, RY + 4, _lbl, 12, INFO, KR, "start", 600)
_cmd = "tmux new -s test"
_cw = len(_cmd) * 7 + 16
d.o.append(f'<rect x="{RX + RW - 20 - _cw + 8}" y="{RY - 8}" width="{_cw}" height="16" fill="{PAPER}"/>')
d.t(RX + RW - 20, RY + 4, _cmd, 12, INFO, MONO, "end")

# 윈도 둘 — 하나는 페인 셋으로 쪼갠 것
WX, WY, WW, WH = 60, 180, 376, 216
d.box(WX, WY, WW, WH, PAPER, MUTED, 1.1, 8)
d.t(WX + 16, WY + 26, "윈도 1", 14, INK, KR, "start", 600)
d.t(WX + 16, WY + 46, "브라우저의 탭 같은 것 · 쓰는 것은 선택", 12, MUTED, KR, "start")

panes = [("페인 A", "셸 하나가 돈다"), ("페인 B", "가로로 쪼갠 것"), ("페인 C", "세로로 쪼갠 것")]
for i, (name, sub) in enumerate(panes):
    px = WX + 16
    py = WY + 68 + i * 48
    d.o.append(f'<rect x="{px}" y="{py}" width="{WW - 32}" height="40" rx="6" '
               f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.3"/>')
    d.t(px + 14, py + 25, name, 13, ACC, KR, "start", 600)
    d.t(px + WW - 46, py + 25, sub, 12, MUTED, KR, "end")

W2X = 468
d.box(W2X, WY, 336, WH, PAPER, MUTED, 1.1, 8)
d.t(W2X + 16, WY + 26, "윈도 2", 14, INK, KR, "start", 600)
d.t(W2X + 16, WY + 46, "세션마다 하나만 두는 경우가 많다", 12, MUTED, KR, "start")
d.o.append(f'<rect x="{W2X + 16}" y="{WY + 68}" width="304" height="136" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.3"/>')
d.t(W2X + 168, WY + 118, "페인 하나", 14, ACC, KR, "middle", 600)
d.t(W2X + 168, WY + 142, "쪼개지 않으면 윈도 전체가", 12, MUTED, KR)
d.t(W2X + 168, WY + 162, "페인 하나입니다", 12, MUTED, KR)

d.tone(28, 452, W - 32 - 16, 76, INFO)
d.t(48, 480, "tmux 는 서버로 돌고 내가 보는 셸이 클라이언트다", 14, INK, KR, "start", 600)
d.t(48, 504, "그래서 세션을 만들고 들어가고 나오고 없앨 수 있습니다. Ctrl+b 다음 d 로 떼어 두면 "
             "나중에 tmux attach -t test 로 다시 붙습니다.", 12, MUTED, KR, "start")

d.legend(544, [("담는 것", INFO), ("실제로 셸이 도는 곳", ACC), ("그 사이 층", MUTED)])
d.save("03-02.tmux-units.svg")
print("ok 03-02.tmux-units")
