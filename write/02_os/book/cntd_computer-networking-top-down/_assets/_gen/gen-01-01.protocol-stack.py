# 01-01 §3 — 다섯 층과 각 층의 PDU 이름, 그리고 장비마다 어디까지 구현하는가.
# 원문: "호스트는 다섯 층을 모두 구현한다 — 인터넷 아키텍처가 복잡성을 가장자리에 둔다는 관점과 일치한다."
# 타입 스펙: type-layers — 위에서 아래로 애플리케이션에서 물리까지. 오른쪽 세 칸이 장비별 도달 범위다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 592
X0, RW, RH, GAP, Y0 = 24, 568, 64, 10, 128
DEV_X = [616, 732, 848]
DEV_W = 104

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-01 §3",
      "다섯 층과 거기까지 닿는 장비",
      "인터넷 프로토콜 스택 다섯 층. 층마다 패킷을 부르는 이름이 다르고, 장비마다 구현하는 층이 다르다. 다섯 층을 다 가진 것은 호스트뿐이다.",
      "복잡성이 가장자리에 몰려 있다는 설계가 이 표에서 그대로 보입니다")

ROWS = [
    ("애플리케이션", "메시지 · message", "HTTP · SMTP · DNS", 3),
    ("트랜스포트", "세그먼트 · segment", "TCP · UDP", 3),
    ("네트워크", "데이터그램 · datagram", "IP 하나 + 라우팅 프로토콜", 2),
    ("링크", "프레임 · frame", "이더넷 · WiFi · DOCSIS", 1),
    ("물리", "비트 · bit", "매체마다 다릅니다", 1),
]
DEVS = [("호스트", "HOST"), ("라우터", "ROUTER"), ("스위치", "SWITCH")]

for j, (nm, eb) in enumerate(DEVS):
    d.t(DEV_X[j] + DEV_W / 2, Y0 - 26, nm, 11, INK, KR, "middle", 600)
    d.t(DEV_X[j] + DEV_W / 2, Y0 - 10, eb, 9, SOFT, MONO)

for i, (name, pdu, ex, reach) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    d.box(X0, y, RW, RH, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 26, name, 12, INK, KR, "start", 600)
    d.t(X0 + 16, y + 47, pdu, 11, ACC, MONO, "start")
    d.t(X0 + RW - 16, y + 38, ex, 11, MUTED, KR, "end")
    # 호스트는 다섯 층 전부, 라우터는 네트워크 층부터 아래, 스위치는 링크 층부터 아래
    for j in range(3):
        hit = [True, i >= 2, i >= 3][j]
        if hit: d.tone(DEV_X[j], y, DEV_W, RH, OK, 6)
        else: d.box(DEV_X[j], y, DEV_W, RH, PAPER, RULE, 0.8, 6)
        d.t(DEV_X[j] + DEV_W / 2, y + 38, "구현" if hit else "없음", 11, OK if hit else SOFT, KR)

BOT = Y0 + len(ROWS) * (RH + GAP) - GAP
d.t(X0, BOT + 26, "라우터는 IP 주소를 보고 링크 계층 스위치는 이더넷 주소만 봅니다 — 스위치가 IP 를 모르는 것은 고장이 아니라 설계입니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("그 장비가 구현하는 층", OK), ("층마다 패킷을 부르는 이름", ACC)])
d.save("01-01.protocol-stack.svg")
