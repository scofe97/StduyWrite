# 03-01 학습 목표 뒤 전체 지도 — 절 넷이 라우팅 지문을 갈라 가는 순서.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 무엇을 배우나 · 그 절이 주는 지문)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 03-01",
      "세그먼트를 넘으면 테이블이 전부다 — 읽는 순서",
      "04·05·06편을 묶은 노트의 절 넷. 절마다 같은 '안 됨' 이 남기는 다른 지문을 하나씩 더한다.",
      "절이 하나씩 지문을 더한다 — 넷을 모으면 증상만으로 원인 후보가 좁혀진다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "테이블이 전부다", "왕복은 별개의 두 결정"),
    ("§2", "편도만 성립할 때", "즉시 에러 · 타임아웃 · 소멸 지점"),
    ("§3", "구체 경로가 이긴다", "딱 한 IP · 첫 홉부터 전멸"),
    ("§4", "TTL 이 루프를 끝낸다", "time-exceeded 반복 · 홉 교대"),
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

d.t(24, 392, "진단 순서는 ip route get · traceroute · 양 끝과 중간의 tcpdump", 12, SOFT, KR, "start")
d.save("03-01.chapter-overview.svg")
