# 07-01 §2 — 네 층과, 층마다 헤더를 붙이고 벗기는 두 방향.
# 원문("The TCP/IP Stack"): "Each layer must be aware of and able to communicate with only the layers
#       right above and below itself. The data is encapsulated in packets, and each layer typically wraps
#       the data in a header that contains information relevant for its function. So, if an app wants to
#       send data, it would interact directly with the highest layer that would add a header and so on
#       down the stack (the send path). Conversely, if an app wants to receive data, it would arrive at
#       the lowest layer, and each layer in turn would process it based on the header information it
#       finds and pass the payload on to the layer above (the receive path)."
#       "The layering means that the header and the payload of a layer make up the payload for the next
#       layer. ... the internet layer takes the packet it gets from the transport layer, treats it as an
#       opaque chunk of bytes, and can focus on its function, the routing of the packet to the target
#       machine."
#       층 번호 — "since the hardware counts as layer 1, the link layer would be 2, the internet layer 3,
#       the transport layer 4, and (for historical reasons, to be OSI model-aligned), the application
#       layer would be 7."
# 타입 스펙: type-layers — 위아래 층과 그 사이의 계약. accent 는 이 절의 논점, 곧 위층의 것이
#           아래층에게는 불투명한 덩어리가 된다는 사실. 축약: 헤더 필드는 §5 와 07-02 의 표에 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 692
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §2",
      "위층이 준 것을 아래층은 열어 보지 않는다",
      "각 층은 바로 위와 바로 아래만 알면 된다. 그래서 인터넷 계층은 전송 계층이 준 패킷을 "
      "불투명한 바이트 덩어리로 취급하고 라우팅에만 집중할 수 있다.",
      "하드웨어가 1계층이라 링크가 2 · 인터넷이 3 · 전송이 4 입니다")

LX, LW, LH, GAP = 168, 544, 82, 10
Y0 = 160
layers = [
    ("애플리케이션 계층", "7", "웹 · SSH · 메일 같은 사용자 대면 도구", WARN),
    ("전송 계층", "4", "종단 간 통신 · TCP 와 UDP · 포트", OK),
    ("인터넷 계층", "3", "IP 로 라우팅 · 네트워크를 가로지른다", ACC),
    ("링크 계층", "2", "하드웨어와 커널 드라이버 · 물리 장치 사이", INFO),
]
for i, (name, num, note, col) in enumerate(layers):
    y = Y0 + i * (LH + GAP)
    focal = (col is ACC)
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, col, 1.2, 8)
    d.t(LX + 20, y + 30, name, 15, col, KR, "start", 600)
    d.t(LX + LW - 20, y + 30, f"L{num}", 14, col, MONO, "end", 600)
    d.t(LX + 20, y + 54, note, 11.5, MUTED, KR, "start")
    # 헤더 + 페이로드 띠
    hy = y + 62
    d.o.append(f'<rect x="{LX + 20}" y="{hy}" width="56" height="14" rx="3" '
               f'fill="{col}30" stroke="{col}" stroke-width="0.9"/>')
    d.t(LX + 48, hy + 11, "헤더", 11, col, KR)
    d.o.append(f'<rect x="{LX + 80}" y="{hy}" width="{LW - 100}" height="14" rx="3" '
               f'fill="{MUTED}18" stroke="{MUTED}" stroke-width="0.9"/>')
    d.t(LX + 80 + (LW - 100) / 2, hy + 11,
        "위층의 헤더와 페이로드를 통째로 — 열어 보지 않는다" if i > 0 else "앱의 데이터",
        11, MUTED, KR)

BOT = Y0 + 4 * (LH + GAP)
d.path(f"M {LX - 60} {Y0 + 20} L {LX - 60} {BOT - GAP - 20}", MUTED, 1.6, m="ar")
d.t(LX - 76, (Y0 + BOT) / 2 - 40, "보내는 길", 12, MUTED, KR, "end", 600)
d.t(LX - 76, (Y0 + BOT) / 2 - 20, "헤더를 붙이며", 11, MUTED, KR, "end")
d.t(LX - 76, (Y0 + BOT) / 2, "내려간다", 11, MUTED, KR, "end")

d.path(f"M {LX + LW + 60} {BOT - GAP - 20} L {LX + LW + 60} {Y0 + 20}", MUTED, 1.6, m="ar")
d.t(LX + LW + 76, (Y0 + BOT) / 2 - 40, "받는 길", 12, MUTED, KR, "start", 600)
d.t(LX + LW + 76, (Y0 + BOT) / 2 - 20, "헤더를 읽고", 11, MUTED, KR, "start")
d.t(LX + LW + 76, (Y0 + BOT) / 2, "위로 넘긴다", 11, MUTED, KR, "start")

d.tone(24, BOT + 4, W - 48, 62, INFO)
d.t(44, BOT + 32, "OSI 는 일곱 층인데 실무에서 쓰는 것은 TCP/IP 의 네 층입니다", 12.5, INK, KR, "start", 600)
d.t(44, BOT + 54,
    "L4 로드밸런서와 L7 인그레스라는 말의 숫자가 이 표의 오른쪽 열에서 나옵니다.", 11.5, MUTED, KR, "start")

d.legend(BOT + 96, [("가장 아래", INFO), ("포트가 있는 층", OK),
                    ("불투명하게 받는 층", ACC), ("사용자를 만나는 층", WARN)])
d.save("07-01.tcp-ip-stack.svg")
print("ok 07-01.tcp-ip-stack")
