# 01-03.mac-rewrite-per-hop — 홉별 헤더 2층 변화
# 본문: "한 구간을 건널 때마다 프레임은 새로 만들어진다. 겉봉의 MAC 은 매번 다시 쓰이고
#        속에 든 IP 목적지는 8.8.8.8 그대로다."
# 타입 스펙: type-architecture.md — 노트북 · 게이트웨이 · 중간 라우터 · 최종 목적지를 잇는 구성도. 아래 헤더 줄이 구간마다 무엇이 바뀌는지를 받는다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 496
d = D(W, H, "ETHERNET HEADER vs IP HEADER",
      "매 홉 새 프레임이 만들어진다 — MAC 만 바뀌고 IP 는 그대로",
      "겉봉은 한 구간마다 새로 쓰고, 속의 목적지는 끝까지 손대지 않는다",
      lead="겉봉은 한 구간마다 새로 쓰고, 속의 목적지는 끝까지 손대지 않는다")

PAD, SLOT_W, HALF = 36, 232, 56
CX  = [PAD + j * SLOT_W + SLOT_W // 2 for j in range(4)]       # 152 384 616 848
MID = [(CX[j] + CX[j + 1]) // 2 for j in range(3)]             # 268 500 732
CY, CARD_Y, CARD_W, ROW_H = 180, 244, 208, 34

ddx.band(d, 104, 400, "구간마다 겉봉을 새로 쓴다 — 속의 IP 목적지는 한 번도 바뀌지 않는다")

for j, (t, s) in enumerate([("노트북", "192.168.0.15"), ("게이트웨이", "집 공유기"),
                            ("중간 라우터", "ISP 망"), ("8.8.8.8", "최종 목적지")]):
    ddx.node(d, CX[j], CY, t, s)
for j in range(3):
    ddx.hop(d, CX[j], CX[j + 1], CY, MUTED, "ar")

MACS = ["MAC = 게이트웨이", "MAC = 중간 라우터", "MAC = 8.8.8.8"]
for j in range(3):
    x = MID[j] - CARD_W // 2
    d.line(MID[j], CY + 14, MID[j], CARD_Y - 4, RULE, 0.9, "3 4")
    d.t(x + 4, CARD_Y + 6, f"구간 {j+1}", 11, SOFT, MONO, "start")
    # 겉봉 — 구간마다 다시 쓴다
    d.tone(x, CARD_Y + 14, CARD_W, ROW_H, WARN, 5, "14", 1.0)
    d.t(x + 10, CARD_Y + 35, "Ethernet", 11, WARN, MONO, "start")
    d.t(x + 62, CARD_Y + 36, ddx.fit(MACS[j], 12, CARD_W - 70, f"card{j+1} MAC"), 12, INK, KR, "start")
    # 속 — 세 번 똑같다
    d.tone(x, CARD_Y + 54, CARD_W, ROW_H, INFO, 5, "14", 1.0)
    d.t(x + 10, CARD_Y + 75, "IP", 11, INFO, MONO, "start")
    d.t(x + 62, CARD_Y + 76, ddx.fit("목적지 = 8.8.8.8", 12, CARD_W - 70, f"card{j+1} IP"), 12, INK, KR, "start")

d.t(500, 376, "IP 헤더는 어디로 가야 하는지를 끝까지 지고 가고, "
              "Ethernet 헤더는 지금 한 칸을 누구에게 건넬지만 말한다", 12, MUTED, KR)
d.legend(420, [("구간마다 다시 쓴다", WARN), ("끝까지 그대로", INFO)])
d.save("01-03.mac-rewrite-per-hop.svg")
print("ok mac-rewrite")
