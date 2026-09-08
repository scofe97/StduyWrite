# 10-01 §5 — 공유 자원이라 혼잡하고, 전이중이라 방향별로 봐야 한다.
# 타입 스펙: type-process — 위단은 프로토콜마다 같은 슬롯(어디서 · 무엇으로)이 반복되고,
#           아래단은 사용률을 방향별로 갈라 본다.
#           축약: 주체(lane)가 없는 대조 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO



W, H = 928, 496
CW, CH, GAP, X0, Y = 280, 128, 24, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01 §5",
      "혼잡을 피하는 세 자리와 방향별 사용률",
      "부하가 높으면 공유 자원인 네트워크가 막힌다. 프로토콜마다 혼잡을 피하는 장치가 다르고, 전이중 링크의 사용률은 방향을 합치면 병목이 가려진다.",
      "한 방향이 100% 에 닿으면 그 방향이 병목입니다 — 합쳐 보면 보이지 않습니다")

CARDS = [
    ("이더넷", "L2", ["압도된 호스트가 송신자에게", "pause 프레임(802.3x)을 보냅니다"], None),
    ("IP", "L3", ["헤더의 ECN 필드로 혼잡을", "드롭 대신 알립니다"], None),
    ("TCP", "L4", ["혼잡 윈도를 줄입니다.", "알고리즘은 10-02 에서 봅니다"], ACC),
]

for i, (name, layer, body, c) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(x + CW - 16, Y + 28, layer, 11, SOFT, MONO, "end")
    for j, line in enumerate(body):
        d.t(x + 16, Y + 58 + j * 20, line, 13, MUTED, KR, "start")

# 방향별 사용률
YD = Y + CH + 52
d.t(X0, YD - 20, "사용률은 방향별로 본다", 14, INK, KR, "start", 600)
BARX, BARW = 176, 456
for k, (lab, pct, note) in enumerate([
        ("송신 (서버 위주)", 0.92, "92% — 이 방향이 병목입니다"),
        ("수신", 0.31, "31% — 여유가 있습니다")]):
    y = YD + 12 + k * 52
    d.t(BARX - 16, y + 20, lab, 13, MUTED, KR, "end")
    d.box(BARX, y, BARW, 28, PAPER2, RULE, 1.0, 4)
    c = ACC if k == 0 else INFO
    d.tone(BARX, y, BARW * pct, 28, c, 4)
    # 주석은 트랙 오른쪽 끝 밖 고정 위치에 둔다 — 채움 길이를 따라가면 캔버스를 넘는다
    d.t(BARX + BARW + 16, y + 19, note, 13, c, KR, "start")

d.t(X0, YD + 136, "자동 협상으로 대역폭·듀플렉스가 바뀌므로 사용률 계산이 단순하지 않습니다. 패킷 수만 보고하는 도구로는 처리량을 계산할 수 없습니다",
    13, MUTED, KR, "start")

d.legend(YD + 160, [("포화에 가까운 방향", ACC), ("여유 있는 방향 · 중립 사실", INFO), ("나머지", MUTED)])
d.save("10-01.congestion-and-duplex.svg")
