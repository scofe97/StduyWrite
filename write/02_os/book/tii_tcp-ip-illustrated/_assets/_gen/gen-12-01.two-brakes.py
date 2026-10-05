# 12-01 §4 — 창 크기 W 를 줄이게 만드는 신호가 두 곳에서 온다.
# 원문 12.1.3: 흐름 제어는 수신자가 창 광고(window advertisement)로 송신자에게 창 크기를 알린다 — 프로토콜 필드가
#   따로 있으니 명시적 신호. 송신 속도는 (S·W/R) bit/s 에 비례하므로 W 를 묶으면 속도가 묶인다.
#   그런데 가운데 라우터의 메모리가 작고 링크가 느리면 수신자가 아닌 망이 넘친다 — 그것을 막는 특수한 흐름 제어가 혼잡 제어.
#   송신자가 다른 증거로 느려져야 한다고 짐작하는 것이 암묵적 신호.
# 타입 스펙: type-architecture — 구성요소(송신자·라우터·수신자)와 연결, 그리고 무엇을 지키는가로 묶은 두 zone.
#           주 흐름은 왼쪽→오른쪽(데이터), 되돌아오는 신호 둘은 점선으로 위·아래 통로를 탄다.
#           focal 은 두 신호가 모두 조이는 손잡이, 송신자의 창 W 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §4",
      "창 W 를 조이는 두 신호",
      "데이터는 송신자에서 라우터를 거쳐 수신자로 간다. 수신자가 못 따라오면 수신자가 창 광고로 직접 알려 주고(명시 신호), "
      "가운데 라우터가 넘칠 때 라우터가 따로 알리지 않으면 송신자가 손실 같은 다른 증거로 짐작한다(암묵 신호). 두 신호 모두 송신자의 창 W 를 줄인다.",
      "지키는 대상이 다르고 신호의 출처도 다르지만, 손잡이는 W 하나입니다")

NY, NH = 228, 88
SX, SW_ = 40, 200
RX, RW = 356, 208
DX, DW = 680, 200

def mid_y(): return NY + NH / 2

# zone — 무엇을 지키는가
d.o.append(f'<rect x="{RX - 24}" y="{NY - 40}" width="{RW + 48}" height="{NH + 64}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{WARN}" stroke-width="0.9" stroke-dasharray="5 4"/>')
d.t(RX - 12, NY - 18, "혼잡 제어가 지킴", 12, WARN, KR, "start", 600)
d.o.append(f'<rect x="{DX - 24}" y="{NY - 40}" width="{DW + 48}" height="{NH + 64}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{INFO}" stroke-width="0.9" stroke-dasharray="5 4"/>')
d.t(DX - 12, NY - 18, "흐름 제어가 지킴", 12, INFO, KR, "start", 600)

# 데이터 흐름 (먼저 그려 z-order 뒤로)
d.arrow([(SX + SW_, mid_y()), (RX - 4, mid_y())], MUTED, "ar", 1.6)
d.t((SX + SW_ + RX) / 2, mid_y() - 10, "데이터", 12, MUTED, KR)
d.arrow([(RX + RW, mid_y()), (DX - 4, mid_y())], MUTED, "ar", 1.6)
d.t((RX + RW + DX) / 2, mid_y() - 10, "데이터", 12, MUTED, KR)

# 명시 신호 — 수신자 → 송신자, 위 통로
TOPY = 148
d.path(f"M {DX + DW / 2} {NY - 40} V {TOPY} H {SX + SW_ / 2 + 40} V {NY - 4}", INFO, 1.4, m="info", dash="5 4")
d.t((SX + DX + DW) / 2 + 40, TOPY - 10, "창 광고 · 프로토콜 필드 = 명시 신호", 12, INFO, KR)
# 암묵 신호 — 라우터의 손실 → 송신자, 아래 통로
BOTY = NY + NH + 72
d.path(f"M {RX + RW / 2} {NY + NH + 24} V {BOTY} H {SX + SW_ / 2 - 40} V {NY + NH + 4}", WARN, 1.4, m="warn", dash="5 4")
d.t((SX + SW_ / 2 + RX + RW / 2) / 2, BOTY + 20, "손실 등 다른 증거로 짐작 = 암묵 신호", 12, WARN, KR)

# 노드
d.o.append(f'<rect x="{SX}" y="{NY}" width="{SW_}" height="{NH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SX + SW_ / 2, NY + 30, "송신자", 14, ACC, KR, "middle", 600)
d.t(SX + SW_ / 2, NY + 54, "창 W 만큼 띄움", 12, INK, KR)
d.t(SX + SW_ / 2, NY + 74, "속도 ∝ S·W / R", 12, MUTED, MONO)

d.box(RX, NY, RW, NH, PAPER2, RULE, 1.0, 8)
d.t(RX + RW / 2, NY + 30, "라우터", 14, INK, KR, "middle", 600)
d.t(RX + RW / 2, NY + 54, "메모리 한정", 12, MUTED, KR)
d.t(RX + RW / 2, NY + 74, "느린 링크 앞 대기열", 12, MUTED, KR)

d.box(DX, NY, DW, NH, PAPER2, RULE, 1.0, 8)
d.t(DX + DW / 2, NY + 30, "수신자", 14, INK, KR, "middle", 600)
d.t(DX + DW / 2, NY + 54, "처리 · 메모리 한정", 12, MUTED, KR)
d.t(DX + DW / 2, NY + 74, "받을 수 있는 양", 12, MUTED, KR)

d.legend(H - 56, [("두 신호가 함께 조이는 손잡이", ACC), ("수신자를 지키는 흐름 제어", INFO), ("망을 지키는 혼잡 제어", WARN)])
d.save("12-01.two-brakes.svg")
