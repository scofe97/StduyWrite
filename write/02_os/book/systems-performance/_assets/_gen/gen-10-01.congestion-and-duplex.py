# 10-01 §5 — 공유 자원이라 혼잡하고, 전이중이라 방향별로 봐야 한다.
# 타입 스펙: type-process — 위단은 프로토콜마다 같은 슬롯(어디서 · 무엇으로)이 반복되고,
#           아래단은 사용률을 방향별로 갈라 본다.
#           축약: 주체(lane)가 없는 대조 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO



W, H = 928, 520
CW, CH, GAP, X0, Y = 280, 128, 24, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01 §5",
      "혼잡을 피하는 세 자리와 방향별 사용률",
      "부하가 높으면 공유 자원인 네트워크가 막힌다. 프로토콜마다 혼잡을 피하는 장치가 다르고, 전이중 링크의 사용률은 방향을 합치면 병목이 가려진다. 막대 값은 본문의 가정 예시(1GbE 전이중, 10초 구간)다.",
      "한 방향이 100% 에 닿으면 그 방향이 병목입니다 — 합쳐 보면 보이지 않습니다")

CARDS = [
    ("이더넷", "L2", ["압도된 수신 호스트", "→ pause 프레임(802.3x)"], None),
    ("IP", "L3", ["헤더의 ECN 필드", "드롭 대신 혼잡 표시"], None),
    ("TCP", "L4", ["혼잡 윈도 축소", "알고리즘: 10-02"], ACC),
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
d.t(X0, YD - 20, "방향별 사용률 — 가정: 1GbE 전이중, 10초 구간", 14, INK, KR, "start", 600)
BARX, BARW = 176, 456
for k, (lab, pct, note, c) in enumerate([
        ("송신 TX", 0.95, "95% · 병목 방향", ACC),
        ("수신 RX", 0.10, "10% · 여유", INFO),
        ("두 방향 평균", 0.525, "52.5% · 병목이 가려짐", MUTED)]):
    y = YD + 12 + k * 52
    d.t(BARX - 16, y + 20, lab, 13, MUTED, KR, "end")
    d.box(BARX, y, BARW, 28, PAPER2, RULE, 1.0, 4)
    d.tone(BARX, y, BARW * pct, 28, c, 4)
    # 주석은 트랙 오른쪽 끝 밖 고정 위치에 둔다 — 채움 길이를 따라가면 캔버스를 넘는다
    d.t(BARX + BARW + 16, y + 19, note, 13, c, KR, "start")

d.legend(YD + 168, [("포화에 가까운 방향", ACC), ("여유 있는 방향", INFO), ("합친 평균 · 나머지", MUTED)])
d.save("10-01.congestion-and-duplex.svg")
