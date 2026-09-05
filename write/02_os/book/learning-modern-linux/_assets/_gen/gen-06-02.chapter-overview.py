# 06-02 학습 목표 뒤 전체 지도 — 6장 뒤 절반의 절 일곱을 읽는 순서로 잇는다.
# 원문 6장 서두: "In the next part of the chapter, we focus on containers: what they are and how they
#       work. We'll review the building blocks of containers, what tooling you have available, and good
#       practices around using containers. To round off this chapter, we look at modern ways to manage
#       Linux apps, especially in desktop environments."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 512
d = D(W, H, "LEARNING MODERN LINUX · 06-02",
      "컨테이너의 새로움은 재료가 아니라 조합에 있다",
      "6장 뒤 절반의 절 일곱을 읽는 순서로 이은 지도. 2~4절이 세 가지 재료이고 "
      "5~6절이 그 재료를 감싼 도구, 7절이 같은 재료를 쓰는 다른 쓰임새다.",
      "5절이 이 노트의 제목이 가리키는 자리입니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "오래됐고 새롭다", "Docker 가 얹은 두 가지"),
    ("§2", "네임스페이스", "무엇이 보이는가"),
    ("§3", "cgroups", "얼마나 쓰는가"),
    ("§4", "세 번째 재료", "CoW 는 5장에서 이미"),
    ("§5", "Docker", "재료를 감싸 준 것"),
    ("§6", "Dockerfile", "지시어가 층이 된다"),
    ("§7", "데스크톱 쪽 관리자", "같은 재료, 다른 목표"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 4)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(448, [("재료를 조합해 감싼 자리", ACC)])
d.save("06-02.chapter-overview.svg")
print("ok 06-02.chapter-overview")
