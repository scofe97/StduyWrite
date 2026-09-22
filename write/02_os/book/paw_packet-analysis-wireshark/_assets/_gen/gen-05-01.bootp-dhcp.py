# 05-01 §6 — DHCP 는 BOOTP 의 메시지 형식과 포트를 물려받은 확장이다.
# 본문 요구: "DHCP 는 BOOTP 메커니즘의 확장입니다. 달리 말해 DHCP 는 BOOTP 를 자기 전송
#            프로토콜로 씁니다. 이 동작 덕분에 기존 BOOTP 클라이언트는 초기화 소프트웨어를
#            바꾸지 않고도 DHCP 서버와 상호 운용됩니다."
#            본문의 8행 대조표는 두 프로토콜의 항목별 값을 나란히 보일 뿐 '얹혀 있다'는
#            관계를 못 세운다. 표는 그대로 두고 이 도식이 관계만 맡는다.
# 타입 스펙: type-layers — 아래가 넓고 위가 특수한 포함 관계. 포트 층은 양쪽이 공유하므로
#           좌우로 가르지 않고 한 층으로 두며, 그 공유가 상호 운용의 근거라 focal 이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 560
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §6",
      "BOOTP 위에 얹힌 DHCP",
      "DHCP 는 BOOTP 를 걷어낸 것이 아니라 그 메시지 형식을 전송으로 쓰고 옵션만 더 얹었다. "
      "맨 아래 포트 층을 두 프로토콜이 공유하기 때문에 서버 하나가 양쪽 클라이언트를 모두 받는다. "
      "필터 이름이 오래도록 bootp 였던 것도 이 구조 때문이다.",
      "공유하는 것은 포트와 메시지 형식, 다른 것은 옵션뿐입니다")

LX, LW = 132, 700
LH, STRIDE = 68, 88
Y0 = 120

LAYERS = [
    ("L3", "DHCP 옵션 확장", "RFC 1531(1993) → 2131(1997) · 임대(lease) · 확장 가능한 options", ACC, True),
    ("L2", "BOOTP 메시지 형식", "RFC 951 · 1985 · 제한된 vendor extensions", INFO, False),
    ("L1", "UDP 67 · 68", "두 프로토콜이 공유하는 포트", OK, False),
]

for i, (tag, name, sub, col, focal) in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    if focal:
        d.tone(LX, y, LW, LH, col, 8, op="14", sw=1.5)
    else:
        d.tone(LX, y, LW, LH, col, 8, op="0A", sw=1.1)
    d.t(LX - 16, y + 40, tag, 9, SOFT, MONO, "end", 600)
    d.t(LX + 24, y + 30, name, 15, col, KR, "start", 600)
    d.t(LX + 24, y + 52, sub, 11, MUTED, KR, "start")

# 왼쪽 여백의 방향 표시 — 위로 갈수록 기능이 얹힌다
d.t(44, Y0 + 20, "확장 ↑", 11, SOFT, MONO, "start")
d.line(60, Y0 + 32, 60, Y0 + 2 * STRIDE + LH, RULE, 1.0, "3 6")
d.t(44, Y0 + 2 * STRIDE + LH + 4, "전송 ↓", 11, SOFT, MONO, "start")

# 공유 층이 상호 운용을 만든다는 것
d.t(24, 412, "포트가 같아 서버 하나가 BOOTP 클라이언트와 DHCP 클라이언트를 모두 받음",
     12, SOFT, KR, "start")
d.t(24, 436, "Wireshark 3.0 — 디섹터 이름이 bootp 에서 dhcp 로 변경 · bootp.dhcp 만 호환 제외",
     11, MUTED, KR, "start")
d.t(24, 458, "DHCPv4 의 rapid commit — DHCPv6 를 본떠 추가된 두 메시지 교환",
     11, MUTED, KR, "start")

d.legend(H - 44, [("DHCP 가 더한 층", ACC), ("전송으로 쓰이는 층", INFO), ("양쪽이 공유", OK)])
d.save("05-01.bootp-dhcp.svg")
