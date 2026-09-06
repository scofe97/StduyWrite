# 09-01 학습 목표 뒤 전체 지도 — 절 다섯과 각 절이 필요해지는 조건.
# 원문 9장 서두: "This final chapter is a bit of a mixed bag. We cover a range of topics, from virtual
#       machines to security to new ways to use Linux. What the topics in this chapter have in common is
#       that most of them are relevant for you only if you have a specific use case in mind, or if you
#       require them in a professional setup."
# 주의: 각 칸 셋째 줄은 저자가 그 절에서 밝힌 조건을 옮긴 것이고, 없는 조건을 지어내지 않았다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 언제 필요해지나)이 반복되고 읽는 순서가
#           화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 428
d = D(W, H, "LEARNING MODERN LINUX · 09-01",
      "이 장을 묶는 것은 주제가 아니라 필요해지는 조건이다",
      "마지막 장의 절 다섯을 읽는 순서로 이은 지도. 셋째 줄은 저자가 그 절에서 밝힌 조건이고, "
      "저자 자신이 대부분은 구체적 용례가 있을 때만 필요하다고 미리 적는다.",
      "저자는 이 장을 잡탕이라고 부르며 시작합니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 108, 12, 20, 20, 112
cards = [
    ("§1", "프로세스 사이 통신", "한 기계 안에서 프로세스끼리", "말을 주고받아야 할 때"),
    ("§2", "가상 머신", "강한 격리가 필요할 때 —", "공용 클라우드와 데이터 센터"),
    ("§3", "현대 배포판", "쿠버네티스 같은 분산 시스템", "문맥에서 자주 만납니다"),
    ("§4", "인증 두 가지", "프로그램마다 인증을 다시", "짜고 싶지 않을 때"),
    ("§5", "아직 주류가 아닌 것", "저자가 집필 시점에 주류가", "아니라고 밝힌 것들"),
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

for i, (n, title, c1, c2) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 52, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 76, c1, 11.5, MUTED, KR, "start")
    d.t(x + 16, y + 94, c2, 11.5, MUTED, KR, "start")

d.legend(384, [("저자가 마주칠 자리를 가장 구체적으로 적은 절", ACC)])
d.save("09-01.chapter-overview.svg")
print("ok 09-01.chapter-overview")
