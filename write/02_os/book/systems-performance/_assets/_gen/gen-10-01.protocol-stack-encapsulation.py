# 10-01 §1 — 층마다 헤더가 붙고, 그 층에서 부르는 이름이 달라진다.
# 타입 스펙: type-layers — 프로토콜 스택은 layers 의 대표 용례(스펙 "Best for: OSI model")다.
#           인덱스 태그에 OSI 층 번호(L2·L3·L4)를 넣고, 오른쪽 서브라벨에 그 층의 메시지 호칭을 둔다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO



W, H = 928, 484
BX, BW, BH, Y0, STRIDE = 152, 592, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01 §1",
      "층마다 헤더가 붙고 이름이 바뀐다",
      "TCP/IP 스택의 네 층. 보낼 메시지는 아래로 내려가며 캡슐화로 커지고, 받을 메시지는 위로 올라가며 헤더가 벗겨진다. 층마다 메시지를 부르는 말이 다르다.",
      "도구 출력이 '패킷' 이라 부르는지 '프레임' 이라 부르는지가 어느 층을 보고 있는지를 알려 줍니다")

LAYERS = [
    ("L5-7", "애플리케이션", "HTTP · DNS · gRPC", "메시지", None),
    ("L4", "전송", "TCP · UDP · QUIC", "세그먼트 / 데이터그램", None),
    ("L3", "네트워크", "IP · ICMP", "패킷", ACC),
    ("L2", "데이터 링크", "이더넷 · Wi-Fi", "프레임", None),
]

for i, (tag, name, proto, unit, c) in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, tag, 12, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, proto, 12, MUTED, MONO, "start")
    d.t(BX + BW - 20, y + 36, unit, 12, c if c else MUTED, KR, "end")

# 양방향 — 캡슐화는 내려가고 역캡슐화는 올라간다
d.arrow([(BX + BW + 44, Y0 + 8), (BX + BW + 44, Y0 + 3 * STRIDE + BH - 4)], MUTED, "ar", 1.3)
d.t(BX + BW + 60, Y0 + 72, "헤더를", 13, MUTED, KR, "start")
d.t(BX + BW + 60, Y0 + 88, "붙인다", 13, MUTED, KR, "start")
d.arrow([(BX - 76, Y0 + 3 * STRIDE + BH - 4), (BX - 76, Y0 + 8)], SOFT, "soft", 1.3)
d.t(BX - 140, Y0 + 72, "헤더를", 13, SOFT, KR, "start")
d.t(BX - 140, Y0 + 88, "벗긴다", 13, SOFT, KR, "start")

d.t(BX, Y0 + 4 * STRIDE + 12, "이더넷 + IP + TCP 헤더만 54바이트 이상입니다 — 페이로드는 그대로인데 총 크기가 커지는 만큼이 전송 오버헤드입니다",
    13, MUTED, KR, "start")

d.legend(Y0 + 4 * STRIDE + 40, [("tcpdump 가 '패킷' 이라 부르는 층", ACC), ("나머지 층", MUTED)])
d.save("10-01.protocol-stack-encapsulation.svg")
