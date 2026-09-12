# 02-01 학습 목표 뒤 전체 지도 — "같은 L2" 의 정의가 절마다 갱신되는 순서.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 무엇이 정하는가 · 대표 고장)이
#           반복되고 화살표가 정의가 갱신되는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 300
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 02-01",
      "같은 세그먼트 안에서만 통한다 — 읽는 순서",
      "01·02·03편을 묶은 노트의 절 셋. 무엇이 '같은 L2' 를 정하는지가 절마다 갱신된다.",
      "케이블은 필요조건일 뿐 — 마스크가 정하고, 그다음 태그가 정한다")

CW, CH, GAP, X0, Y = 261, 118, 24, 24, 120
cards = [
    ("§1", "마스크가 정한다", "서브넷 불일치 · 중복 IP"),
    ("§2", "스위치가 옮긴다", "루프 스톰 · FDB 오염"),
    ("§3", "태그가 정한다", "트렁크 허용 목록 비대칭"),
]

def x_of(i):
    return X0 + i * (CW + GAP)

for i in range(2):
    d.arrow([(x_of(i) + CW, Y + CH / 2), (x_of(i + 1) - 4, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, fault) in enumerate(cards):
    x = x_of(i)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, Y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, Y + 60, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, Y + 86, fault, 12, MUTED, KR, "start")

d.t(24, 272, "세 칸을 지나면 정의가 한 번 더 갱신된다 — 07장 캡슐", 12, SOFT, KR, "start")
d.save("02-01.chapter-overview.svg")
