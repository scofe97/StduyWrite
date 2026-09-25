# 05-01 학습 목표 뒤 전체 지도 — 절 넷이 연결의 생애를 따라간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 연결의 어느 국면 · 그 절이 주는 지문)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 05-01",
      "연결은 양 끝만의 일이 아니다 — 읽는 순서",
      "08·09·10·11편을 묶은 노트의 절 넷. 연결이 맺히고 유지되고 재작성되는 국면마다 다른 지문이 나온다.",
      "마지막 절이 앞의 셋을 합성한다 — 저자가 11편을 그렇게 설계했다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "맺힐 때", "타임아웃 · refused · RST 의 TTL"),
    ("§2", "유지될 때", "조용한 죽음 · 신규만 실패"),
    ("§3", "재작성될 때", "소스를 빌리는 대가"),
    ("§4", "왕복이 갈릴 때", "타임아웃인데 무응답이 아니다"),
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
    focal = (i == 3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 84, mark, 12, MUTED, KR, "start")

d.t(24, 392, "증상 문장 하나가 원인 부위를 좁힌다 — 그것이 이 블록의 산출물이다", 12, SOFT, KR, "start")
d.save("05-01.chapter-overview.svg")
