# 13-02 §4 — Window Scale: 32비트 실제 창 → 오른쪽 시프트 S → 16비트 칸 → 받는 쪽이 왼쪽 시프트 R 로 복원.
# 원문 13.3.3: 보낼 때 실제 32비트 창을 S 비트 오른쪽으로 밀어 16비트 칸에 넣고, 받은 16비트 값은 R 비트 왼쪽으로 밀어 실제 창을 얻는다.
#   시프트는 0~14, 14 면 최대 창 65,535 × 2^14 = 1,073,725,440 바이트. 옵션은 SYN 에만 실리고 양쪽이 다 보내야 켜진다.
# 값: OrbStack Ubuntu 캡처(2026-10-04) — SYN 의 wscale 10, 이후 세그먼트의 win 64 → 64 × 2^10 = 65,536.
# 타입 스펙: type-process — 칸 셋(보내는 쪽의 실제 창 · 헤더의 16비트 칸 · 받는 쪽이 복원한 창)이 같은 슬롯(값 · 비트 폭)을 반복하고
#           화살표가 시프트 연산을 나른다. 축약: 주체 lane 대신 칸 위에 송신·헤더·수신 이름을 단다. focal 은 헤더의 16비트 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 420
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02 §4",
      "16비트 창 칸을 시프트로 늘려 쓰기",
      "보내는 쪽은 실제 창 65,536 바이트를 SYN 에서 알린 시프트 10 만큼 오른쪽으로 밀어 헤더에 64 를 넣는다. 받는 쪽은 그 64 를 같은 10 만큼 왼쪽으로 밀어 65,536 을 되찾는다. "
      "칸 크기는 그대로 16비트이고 읽는 법만 바뀐다.",
      "칸은 16비트 그대로, 단위만 2^10 바이트가 됩니다")

CW, CH = 232, 112
XS = [40, 344, 648]
Y = 148
cards = [
    ("보내는 쪽", "실제 창", "65,536", "32비트로 관리", None),
    ("TCP 헤더", "Window Size 칸", "64", "16비트 · 0–65,535", "focal"),
    ("받는 쪽", "복원한 창", "65,536", "32비트로 관리", None),
]
d.arrow([(XS[0] + CW, Y + CH / 2), (XS[1] - 4, Y + CH / 2)], MUTED, "ar", 1.5)
d.t((XS[0] + CW + XS[1]) / 2, Y + CH / 2 - 10, ">> 10", 13, INFO, MONO, "middle", 600)
d.arrow([(XS[1] + CW, Y + CH / 2), (XS[2] - 4, Y + CH / 2)], MUTED, "ar", 1.5)
d.t((XS[1] + CW + XS[2]) / 2, Y + CH / 2 - 10, "<< 10", 13, OK, MONO, "middle", 600)

for x, (who, what, val, bits, kind) in zip(XS, cards):
    if kind == "focal":
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8); c = INK
    d.t(x + CW / 2, Y - 12, who, 12, SOFT, KR, "middle", 600)
    d.t(x + CW / 2, Y + 30, what, 13, MUTED, KR)
    d.t(x + CW / 2, Y + 66, val, 22, c, MONO, "middle", 600)
    d.t(x + CW / 2, Y + 94, bits, 11, MUTED, KR)

# 아래 줄 — 한계와 규칙
yb = Y + CH + 48
d.chip(XS[1] + CW / 2, yb, "시프트 0–14 · 최대 65,535 × 2^14 = 1,073,725,440", MUTED, 12)
d.chip(XS[1] + CW / 2, yb + 36, "SYN 에서만 교환 · SYN 의 창 칸은 시프트 없이 읽음", MUTED, 12)

d.legend(H - 56, [("헤더에 실리는 16비트 값", ACC), ("보낼 때 오른쪽 시프트 S", INFO), ("받을 때 왼쪽 시프트 R", OK)])
d.save("13-02.window-scale.svg")
