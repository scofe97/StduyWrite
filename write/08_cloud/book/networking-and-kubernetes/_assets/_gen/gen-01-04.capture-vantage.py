# 01-04.capture-vantage — 2행 대조 (같은 자리끼리 세로로 맞춰 본다)
# 본문: "윗줄이 lo0 이고 아랫줄이 en0 입니다. 같은 자리끼리 세로로 맞춰 보면
#        관측 지점 하나가 무엇을 바꾸는지 갈립니다. 둘째 칸이 이 편의 갈림길입니다."
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — 열 머리를 세워 세로 대조가 성립하게 한다.
#           coral 은 본문이 "갈림길"이라 부른 둘째 열 하나에만.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 652
d = D(W, H, "CAPTURE VANTAGE · lo0 vs en0",
      "어디서 잡느냐가 어디까지 보이느냐를 정한다",
      "윗줄이 lo0, 아랫줄이 en0. 같은 자리끼리 세로로 맞춰 보면 관측 지점 하나가 무엇을 바꾸는지 갈린다.",
      lead="같은 자리끼리 세로로 맞춰 보면 관측 지점 하나가 무엇을 바꾸는지 갈린다")

LBL_W, CW, GAP, CH = 156, 183, 16, 100
COL0 = 196                                                      # 라벨 열(24~180) 뒤 16 여백
COLX = [COL0 + i * (CW + GAP) for i in range(4)]                 # 196 395 594 793 (우단 976)
ROW_Y = [300, 428]
HEAD_Y = 214
HEADS = ["보이는 계층", "MTU", "잡음", "어느 절"]
FOCAL_COL = 0                                                   # 본문이 "둘째 칸"이라 부른 그 열

ddx.band(d, 104, 596, "관측 지점 하나가 계층·분할·잡음을 한꺼번에 바꾼다")

for i, h in enumerate(HEADS):
    c = ACC if i == FOCAL_COL else SOFT
    d.t(COLX[i] + CW // 2, HEAD_Y, ddx.fit(h, 12, CW - 12, h), 12, c, KR, "middle", 600)
if True:                                                        # 갈림길 열을 세로로 짚는다
    x, top = COLX[FOCAL_COL] - 8, HEAD_Y - 26
    bot = ROW_Y[1] + CH // 2 + 12
    d.o.append(f'<rect x="{x}" y="{top}" width="{CW+16}" height="{bot-top}" rx="8" '
               f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
    d.t(x + (CW + 16) // 2, bot + 24, "이 편의 갈림길", 11, ACC, KR)

for r, (iface, sub, cells, c) in enumerate([
        ("lo0 캡처", "localhost:8080 · 통제된 환경",
         [("L3 부터 보인다", "MAC · ARP 못 봄"), ("16384", "en0 의 열 배"),
          ("잡음 0", "남의 트래픽 없음"), ("§2", "패킷 12개 세기")], INFO),
        ("en0 캡처", "실제 랜 · 남의 트래픽 섞임",
         [("L2 부터 보인다", "ARP 관측 가능"), ("1500", "표준 이더넷"),
          ("필터 필수", "port · arp 로 좁힘"), ("§3 · §5", "ARP · 대조")], WARN)]):
    cy = ROW_Y[r]
    d.box(24, cy - CH // 2, LBL_W, CH, PAPER2, c, 1.2, 6)
    d.t(24 + LBL_W // 2, cy - 8, iface, 13, c, KR, "middle", 600)
    d.t(24 + LBL_W // 2, cy + 14, ddx.fit(sub.split(" · ")[0], 11, LBL_W - 16, iface), 11, MUTED, KR)
    for i, (main, note) in enumerate(cells):
        x = COLX[i]
        cc = ACC if i == FOCAL_COL else RULE
        d.box(x, cy - CH // 2, CW, CH, PAPER2, cc, 1.1, 6)
        d.t(x + CW // 2, cy - 6, ddx.fit(main, 12, CW - 16, main), 12,
            ACC if i == FOCAL_COL else INK, KR, "middle", 600)
        d.t(x + CW // 2, cy + 16, ddx.fit(note, 11, CW - 16, note), 11, MUTED, KR)

d.t(36, 556, "MAC 이 없으면 ARP 도 Ethernet 프레임도 존재하지 않는다 — 01-03 의 Link 계층을 "
             "루프백에서 확인할 수 없는 이유가 이것이다", 12, MUTED, KR, "start")
d.legend(612, [("lo0", INFO), ("en0", WARN), ("갈림길", ACC)])
d.save("01-04.capture-vantage.svg")
print("ok capture-vantage")
