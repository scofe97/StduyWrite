# 03-02 §3 — 원문 Figure 3.19 의 순서 번호 공간. 네 구간과 창 크기 N.
# 창 크기 N=4 와 base=2 는 원문 Figure 3.22 의 예에서 가져왔다(창 4, 패킷 2 손실).
# 타입 스펙: type-kanban — 상태별 현황 census. 연결선을 쓰지 않고, 진행 중 열에 WIP 상한을 붙인다.
#           여기서 WIP 상한이 곧 창 크기 N 이다 — 미확인 패킷 수의 상한이라는 뜻이 정확히 같다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 596
COLW, GUT, CX0, CY0 = 216, 20, 30, 152
CARD_H, CARD_GAP = 52, 10

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §3",
      "순서 번호 공간의 네 구간",
      "Go-Back-N 송신자가 보는 번호 공간. 가운데 두 열을 합한 크기가 창 N 이고, 창은 ACK 가 올 때마다 오른쪽으로 미끄러진다.",
      "base = 2 · N = 4 인 순간의 현황입니다")

COLS = [
    ("확인까지 받음", "[0, base-1]", None, ["pkt 0", "pkt 1"], OK, False),
    ("보냈지만 미확인", "[base, next-1]", "3/4", ["pkt 2", "pkt 3", "pkt 4"], ACC, True),
    ("바로 보낼 수 있음", "[next, base+N-1]", "1/4", ["pkt 5"], INFO, False),
    ("아직 못 씀", "base+N 이상", None, ["pkt 6", "pkt 7 …"], MUTED, False),
]

for i, (name, rng, wip, cards, c, focal) in enumerate(COLS):
    x = CX0 + i * (COLW + GUT)
    d.o.append(f'<rect x="{x}" y="{CY0}" width="{COLW}" height="300" rx="4" fill="{INK}05"/>')
    d.t(x + 14, CY0 + 26, name, 12, c if focal else INK, KR, "start", 600)
    if wip:
        d.o.append(f'<rect x="{x + COLW - 52}" y="{CY0 + 12}" width="38" height="18" rx="2" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1"/>')
        d.t(x + COLW - 33, CY0 + 25, wip, 8, c, MONO)
    d.t(x + 14, CY0 + 46, rng, 11, SOFT, MONO, "start")
    d.line(x, CY0 + 58, x + COLW, CY0 + 58, RULE, 0.8)
    for j, card in enumerate(cards):
        cy = CY0 + 74 + j * (CARD_H + CARD_GAP)
        if focal:
            d.tone(x + 16, cy, COLW - 32, CARD_H, c, 6, "14", 1.2)
        else:
            d.box(x + 16, cy, COLW - 32, CARD_H, PAPER2, c, 1.0, 6)
        d.t(x + 30, cy + 24, card, 12, c if focal else INK, MONO, "start", 600)
        if focal: d.t(x + 30, cy + 42, "타임아웃이면 재전송", 11, SOFT, KR, "start")

d.t(28, 486, "창 = 가운데 두 열 = N. 타임아웃이 나면 두 번째 열 전체를 다시 보냅니다 — 이름이 Go-Back-N 인 이유입니다.",
     11, MUTED, KR, "start")
d.t(28, 508, "ACK n 은 누적입니다. n 이하가 전부 도착했다는 뜻이라, ACK 하나가 오면 창이 그만큼 통째로 미끄러집니다.",
     11, MUTED, KR, "start")
d.t(28, 530, "창을 N 으로 제한하는 이유는 둘입니다 — 받는 쪽의 버퍼(흐름 제어)와 망의 혼잡(혼잡 제어)입니다.",
     11, SOFT, KR, "start")

d.legend(H - 40, [("타임아웃 시 전부 재전송", ACC), ("확인 완료", OK), ("보낼 수 있음", INFO), ("잠김", MUTED)])
d.save("03-02.gbn-window.svg")
