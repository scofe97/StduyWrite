# 02-02 §7 — 원문 Figure 2.11 의 두 스택. a. 전통적 보안 HTTP, b. QUIC 기반 HTTP/3.
# 위 두 칸을 애플리케이션 층으로 묶은 것은 원문의 주장 그대로다 — 원문은 TLS 도 QUIC 도
# 트랜스포트 프로토콜이 아니라 애플리케이션 층의 하위 층으로 놓는다.
# 타입 스펙: type-layers — 위에서 아래로 애플리케이션에서 아래층까지. 두 스택을 나란히 둬 대비한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 628
BW, BH, PITCH = 320, 54, 66
LCX, RCX = 268, 700
Y0 = 168

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 §7",
      "악수가 두 번이냐 한 번이냐",
      "원문 Figure 2.11 의 두 프로토콜 스택. 왼쪽은 TCP 위에 TLS 를 얹은 https, 오른쪽은 UDP 위의 QUIC 이다.",
      "원문은 TLS 도 QUIC 도 트랜스포트가 아니라 애플리케이션 층의 하위 층으로 놓습니다")

STACKS = [
    (LCX, "a. 전통적 보안 HTTP", ["HTTP/1.1 · HTTP/2", "TLS", "TCP", "IP"], False),
    (RCX, "b. QUIC 기반 HTTP/3", ["HTTP/3", "QUIC", "UDP", "IP"], True),
]

for cx, title, rows, focal in STACKS:
    d.t(cx, 132, title, 12, ACC if focal else INK, KR, "middle", 600)
    # 애플리케이션 층 묶음 (위 두 칸)
    d.o.append(f'<rect x="{cx - BW / 2 - 12}" y="{Y0 - 12}" width="{BW + 24}" height="{PITCH + BH + 24}" '
               f'rx="8" fill="{INK}05" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(cx - BW / 2 - 4, Y0 - 20, "애플리케이션 층", 11, SOFT, KR, "start")
    for i, name in enumerate(rows):
        y = Y0 + i * PITCH
        hot = focal and i == 1
        if hot:
            d.tone(cx - BW / 2, y, BW, BH, ACC, 6, "14", 1.4)
        else:
            d.box(cx - BW / 2, y, BW, BH, PAPER2, RULE, 1.0, 6)
        d.t(cx, y + 33, name, 12, ACC if hot else INK, MONO, "middle", 600)

# 악수 표시
d.t(LCX, Y0 + 4 * PITCH + 24, "악수 두 번", 12, MUTED, KR, "middle", 600)
d.t(LCX, Y0 + 4 * PITCH + 46, "TCP 연결 수립 뒤에", 11, SOFT, KR)
d.t(LCX, Y0 + 4 * PITCH + 66, "TLS 키 교환이 따로 옵니다", 11, SOFT, KR)

d.t(RCX, Y0 + 4 * PITCH + 24, "악수 한 번", 12, ACC, KR, "middle", 600)
d.t(RCX, Y0 + 4 * PITCH + 46, "QUIC 이 TLS 1.3 핸드셰이크를", 11, SOFT, KR)
d.t(RCX, Y0 + 4 * PITCH + 66, "자기 핸드셰이크에 품습니다", 11, SOFT, KR)

d.t(20, 546, "재접속할 때는 저장해 둔 세션과 암호 파라미터를 써서 0-RTT 로 바로 보낼 수도 있습니다.",
     11, MUTED, KR, "start")

d.legend(H - 48, [("이 층이 둘을 하나로 합칩니다", ACC), ("나머지 층", MUTED)])
d.save("02-02.quic-stack.svg")
