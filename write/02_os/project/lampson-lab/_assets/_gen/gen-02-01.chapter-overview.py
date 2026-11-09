# 02-01 학습 목표 뒤 전체 지도 — 절 넷이 SPIRE 의 신원 발급을 따라간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 국면 · 그 절이 주는 것)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 02-01",
      "신원은 프로세스에서 나온다 — 읽는 순서",
      "절 넷. 서명하는 쪽과 확인하는 쪽을 나누고, 호출자를 커널에 묻고, 대응표로 이름을 붙이고, 그 신원 단위의 한계로 닫는다.",
      "두 번째 절이 이 편의 핵심이다 — 신원은 요청이 아니라 커널이 아는 사실에서 나온다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "나뉜 구성 · server 와 agent", "서명하는 쪽 · 확인하는 쪽 · join token"),
    ("§2", "호출자 확인 · 커널에 묻는다", "unix attestor · 요청에 신원 칸이 없다"),
    ("§3", "대응표 · entry", "uid 에서 SPIFFE ID 로 · intruder 는 행이 없다"),
    ("§4", "한계 · 신원 단위", "계정(uid)까지만 가른다"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), (Y1 if i < 2 else Y2)

for i in range(3):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cy = Y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}", MUTED, 1.4, m="ar")

for i, (n, title, mark) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 84, mark, 12, MUTED, KR, "start")

d.t(24, 392, "이름을 붙이는 일과 이름이 가리키는 단위를 따로 본다 — 한계는 뒤의 것에 있다", 12, SOFT, KR, "start")
d.save("02-01.chapter-overview.svg")
