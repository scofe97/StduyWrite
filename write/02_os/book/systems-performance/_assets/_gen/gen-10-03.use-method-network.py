# 10-03 §1 — USE 를 네트워크에 적용하면 무엇을 어떻게 재는가.
# 타입 스펙: type-process — 세 축(에러·사용률·포화)마다 같은 슬롯(무엇을 · 어떻게 · 함정)이 반복된다.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 464
CW, CH, GAP, X0, Y = 280, 200, 24, 24, 124

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-03 §1",
       "USE 를 네트워크에 적용하는 순서",
       "인터페이스별·방향별로 에러·사용률·포화를 본다. 셋 중 에러를 먼저 보는 이유는 빠르고 해석이 쉽기 때문이다.",
       "에러부터 봅니다 — 빠르고 해석이 쉽습니다")

CARDS = [
    ("01", "에러", "먼저 본다", OK,
     ["errors · dropped · overruns", "carrier · collisions"],
     "해석이 명확해 가장 싸게 걸러집니다"),
    ("02", "사용률", "계산해야 한다", ACC,
     ["현재 처리량 ÷ 협상 속도.", "방향별(TX/RX)로 따로"],
     "OS 도구가 직접 안 주는 경우가 많습니다"),
    ("03", "포화", "재기 어렵다", WARN,
     ["직접 지표가 마땅치 않습니다.", "TCP 재전송을 대리 지표로"],
     "재전송이 네트워크 포화의 신호가 됩니다"),
]

for i, (n, name, tag, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.o.append(f'<rect x="{x + 16}" y="{Y + 16}" width="22" height="18" rx="9" fill="{c}" stroke="{c}" stroke-width="1"/>')
    d.t(x + 27, Y + 29, n, 9, PAPER, MONO)
    d.t(x + 48, Y + 29, name, 15, c, KR, "start", 600)
    d.t(x + CW - 16, Y + 29, tag, 13, SOFT, KR, "end")
    d.line(x + 16, Y + 46, x + CW - 16, Y + 46, RULE, 0.8)
    for j, line in enumerate(body):
        d.t(x + 16, Y + 72 + j * 20, line, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 44, "왜", 13, SOFT, KR, "start", 600)
    d.t(x + 16, Y + CH - 22, foot, 13, c, KR, "start")

YB = Y + CH + 36
d.t(X0, YB, "인터페이스별로, 그리고 방향별로 봅니다 — 합쳐 평균 내면 포화된 방향이 여유 있는 방향에 가려집니다",
    13, MUTED, KR, "start")

d.legend(YB + 24, [("계산이 필요한 축", ACC), ("가장 먼저 보는 축", OK), ("대리 지표를 쓰는 축", WARN)])
d.save("10-03.use-method-network.svg")
