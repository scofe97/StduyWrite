# 12-01 §8 — 원서 Figure 12-3(TCP 헤더). 보통 20 바이트이고 옵션이 있으면 늘어난다(최대 60).
#   원문 캡션: 음영 칸(Acknowledgment Number, Window Size, ECE·ACK 비트)은 이 세그먼트를 보낸 쪽 기준으로
#   반대 방향으로 흐르는 데이터에 관한 것이다. 플래그 8개는 CWR·ECE·URG·ACK·PSH·RST·SYN·FIN.
#   Header Length 는 4비트, 32비트 단어 수(최솟값 5). 포트 둘 + IP 헤더의 주소 둘 = 연결을 가리키는 4-tuple.
# 타입 스펙: type-layers — 32비트 줄이 위에서 아래로 쌓인다(헤더의 바이트 순서). 층 안을 비트 폭 비례 칸으로 가른 변형.
#           카탈로그에 "비트 필드 격자" 타입이 없어 layers 로 축약했다(N&K 01-02.tcp-header-layout 과 같은 선택).
#           칸 너비 = 비트 수 × 24px. 상태색 축: 반대 방향(info) 대 이 방향(중립). focal 은 4-tuple 의 절반인 포트 줄.
#           원서 그림의 예약 칸 폭(4비트)을 따른다 — 플래그가 8개라 4 + 4 + 8 + 16 = 32.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
X0, BITW, RH = 72, 24, 48
RY0 = 156
REV = "rev"
ROWS = [
    [(16, "Source Port", "출발지 포트", "focal"), (16, "Destination Port", "목적지 포트", "focal")],
    [(32, "Sequence Number", "이 세그먼트 첫 바이트의 번호", None)],
    [(32, "Acknowledgment Number", "다음에 받기를 기대하는 번호", REV)],
    [(4, "HLen", "", None), (4, "Resv", "", None),
     (1, "CWR", "", None), (1, "ECE", "", REV), (1, "URG", "", None), (1, "ACK", "", REV),
     (1, "PSH", "", None), (1, "RST", "", None), (1, "SYN", "", None), (1, "FIN", "", None),
     (16, "Window Size", "받을 수 있는 바이트 수", REV)],
    [(16, "TCP Checksum", "의사 헤더 포함", None), (16, "Urgent Pointer", "URG 일 때만", None)],
]

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §8",
      "TCP 헤더 20 바이트 — 어느 칸이 반대 방향 이야기인가",
      "원서 그림 12-3 의 배치를 32비트 줄 다섯과 옵션으로 옮겼다. 칸 너비가 비트 수에 비례하고 예약 4비트·플래그 8개는 원서와 RFC 9293 의 셈법이다. 파란 칸(ACK 번호·Window Size·ECE·ACK 비트)은 "
      "이 세그먼트를 보낸 쪽이 아니라 반대 방향으로 흐르는 데이터에 관한 값이고, 강조한 포트 두 칸은 IP 헤더의 주소 둘과 합쳐 연결 하나를 가리킨다.",
      "한 세그먼트가 자기 데이터를 나르면서 반대 방향의 확인과 창 광고를 함께 싣습니다")

# 비트 눈금
d.line(X0, 128, X0 + 32 * BITW, 128, RULE, 0.8)
for bit in (0, 8, 16, 24, 31):
    x = X0 + bit * BITW + (BITW / 2 if bit == 31 else 0)
    d.t(x, 146, str(bit), 11, SOFT, MONO, "middle" if 0 < bit < 31 else ("start" if bit == 0 else "middle"))

for r, cells in enumerate(ROWS):
    y = RY0 + r * RH
    d.t(X0 - 16, y + 29, f"+{r * 4}", 11, SOFT, MONO, "end")
    x = X0
    for bits, name, sub, kind in cells:
        w = bits * BITW
        if kind == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{RH}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            c = ACC
        elif kind == REV:
            d.tone(x, y, w, RH, INFO, 0, "16", 1.0); c = INFO
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 0); c = INK
        if bits == 1:
            d.t(x + w / 2, y + 29, name, 11, c, MONO, "middle", 600)
        elif sub:
            d.t(x + w / 2, y + 21, name, 13, c, MONO, "middle", 600)
            d.t(x + w / 2, y + 39, sub, 11, MUTED, KR)
        else:
            d.t(x + w / 2, y + 29, name, 12, c, MONO, "middle", 600)
        x += w


# 옵션 + 데이터
oy = RY0 + 5 * RH
d.o.append(f'<rect x="{X0}" y="{oy}" width="{32 * BITW}" height="40" fill="{PAPER}" stroke="{RULE}" stroke-width="1" stroke-dasharray="5 4"/>')
d.t(X0 + 16 * BITW, oy + 25, "Options · 최대 40 바이트 · MSS · SACK · Timestamp · Window Scale", 12, SOFT, KR)
d.t(X0 + 32 * BITW + 12, RY0 + 2 * RH + 4, "20 바이트", 12, MUTED, KR, "start", 600)
d.line(X0 + 32 * BITW + 6, RY0, X0 + 32 * BITW + 6, oy, MUTED, 1.0)
d.t(X0 + 32 * BITW + 12, oy + 25, "≤ 60", 12, MUTED, MONO, "start", 600)

d.legend(H - 56, [("4-tuple 중 TCP 가 싣는 절반", ACC), ("반대 방향 데이터에 관한 칸", INFO), ("이 방향 칸", MUTED)])
d.save("12-01.tcp-header.svg")
