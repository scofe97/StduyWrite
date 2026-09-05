# 01-01 §1 — 패킷 분석기가 스택의 어느 층에서 가로채는가.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 아래로 갈수록 선에 가깝고, 위로 갈수록 해석된 데이터다.
#           focal 은 분석기가 실제로 서는 층 하나(패킷 소켓 · libpcap).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 512
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §1",
      "분석기가 가로채는 층",
      "애플리케이션에서 물리 인터페이스까지의 다섯 층. 애플리케이션 로그는 맨 위 층만 보고, 패킷 분석기는 커널 패킷 소켓 층에서 프레임 사본을 받는다.",
      "위로 갈수록 해석된 데이터, 아래로 갈수록 선 위의 원본 프레임입니다")

LX, LW, LH = 96, 852, 64                 # 레이어 x · 폭 · 높이. stride = LH
Y0 = 104
layers = [
    ("L5", "애플리케이션",            "curl · 브라우저 · 서버 프로세스", False),
    ("L4", "소켓 API",                "socket() · read() · write()",     False),
    ("L3", "커널 프로토콜 스택",      "이더넷 · IP · TCP 헤더 해석",      False),
    ("L2", "패킷 소켓 · libpcap",     "원본 프레임 사본을 받는 자리",     True),
    ("L1", "NIC 드라이버 · 물리 인터페이스", "en0 · eth0 · 선",           False),
]

for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 1.0, 6)
    d.t(LX + 20, y + 38, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(LX + 68, y + 39, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 20, y + 39, sub, 12, MUTED, KR, "end")

# 왼쪽 여백의 방향 지시 — 회전 라벨은 한글이 뒤집히므로 가로 두 줄로 끊는다
d.t(12, Y0 + 12, "해석된", 11, SOFT, KR, "start")
d.t(12, Y0 + 30, "데이터", 11, SOFT, KR, "start")
d.path(f"M 52 {Y0 + 40} V {Y0 + len(layers) * LH - 44}", SOFT, 1.2, m="soft")
d.t(12, Y0 + len(layers) * LH - 26, "선 위의", 11, SOFT, KR, "start")
d.t(12, Y0 + len(layers) * LH - 8, "원본 프레임", 11, SOFT, KR, "start")

d.legend(Y0 + len(layers) * LH + 24, [("분석기가 서는 층", ACC)])
d.save("01-01.capture-path.svg")
