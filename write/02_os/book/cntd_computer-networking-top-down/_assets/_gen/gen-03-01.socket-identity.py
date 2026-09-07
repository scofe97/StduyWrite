# 03-01 §4 — 도착한 세그먼트를 어느 소켓으로 보낼 것인가. UDP 는 값 둘만 보고 TCP 는 넷을 다 본다.
# 두 식별자 규칙은 원문 3.2 의 문장 그대로다. 아래 예시 값은 이 기계에서 실측한 것이다.
# 타입 스펙: type-flowchart — 판정을 물어 가며 좁히는 결정 흐름. 마름모가 물음이고 사각이 결과다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 620
CX = 340

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-01 §4",
      "값 둘을 보느냐 넷을 보느냐",
      "도착한 세그먼트를 소켓으로 보내는 판정. UDP 는 목적지 두 값만 보고 TCP 는 출발지까지 넷을 본다.",
      "이 차이가 웹 서버가 포트 하나로 수많은 연결을 구별하는 이유입니다")

def diamond(cx, cy, w, h, txt, c=MUTED):
    d.o.append(f'<polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, txt, 11, INK, KR)

def rect(cx, cy, w, h, l1, l2, c=MUTED, focal=False):
    if focal: d.tone(cx - w / 2, cy - h / 2, w, h, c, 6, "14", 1.4)
    else: d.box(cx - w / 2, cy - h / 2, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, cy - 4, l1, 12, c if focal else INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 11, SOFT, MONO)

# 진입
d.o.append(f'<circle cx="{CX}" cy="146" r="6" fill="{INK}"/>')
d.t(CX + 16, 150, "세그먼트 도착", 11, SOFT, KR, "start")
d.path(f"M {CX} 154 L {CX} 178", MUTED, 1.3, m="ar")

diamond(CX, 208, 260, 60, "UDP 세그먼트인가")

# 예 — UDP
d.path(f"M {CX - 130} 208 L 172 208 L 172 296", MUTED, 1.3, m="ar")
d.t(CX - 142, 200, "예", 11, MUTED, KR, "end")
rect(172, 330, 260, 68, "목적지 두 값만 봅니다", "(dst IP, dst port)", INFO, True)
d.path(f"M 172 364 L 172 434", MUTED, 1.3, m="ar")
rect(172, 468, 280, 68, "출발지가 달라도 같은 소켓", "2-tuple", MUTED)

# 아니오 — TCP
d.path(f"M {CX + 130} 208 L 660 208 L 660 296", MUTED, 1.3, m="ar")
d.t(CX + 142, 200, "아니오", 11, MUTED, KR, "start")
rect(660, 330, 300, 68, "네 값을 모두 봅니다", "(src IP, src port, dst IP, dst port)", ACC, True)
d.path(f"M 660 364 L 660 434", ACC, 1.4, m="acc")
rect(660, 468, 300, 68, "출발지가 다르면 다른 소켓", "4-tuple", ACC, True)

d.t(972, 330, "최초 연결 요청만", 11, SOFT, KR, "end")
d.t(972, 350, "환영 소켓으로 갑니다", 11, SOFT, KR, "end")

d.t(24, 534, "실측 — UDP 서버 소켓 하나가 출발지 포트 57418·49530 을 모두 받았고, TCP 는 56801·56802 에서 연결 소켓이 각각 생겼습니다.",
     11, MUTED, KR, "start")

d.legend(H - 60, [("TCP — 값 넷", ACC), ("UDP — 값 둘", INFO), ("판정", MUTED)])
d.save("03-01.socket-identity.svg")
