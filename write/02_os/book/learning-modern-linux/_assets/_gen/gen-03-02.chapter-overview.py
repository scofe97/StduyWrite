# 03-02 학습 목표 뒤 전체 지도 — 3장 가운데 구간(도구를 갈아 끼우는 축)을 읽는 순서로 잇는다.
# 원문 3장 "Common Tasks" · "Human-Friendly Shells" · "Terminal Multiplexer" 구간.
#       저자의 출발 문장은 "One fundamental insight with interfaces is that commands that you are using
#       very often should take the least effort—they should be quick to enter." 이고,
#       셸 절은 "While the bash shell is likely still the most widely used shell, it is not necessarily
#       the most human-friendly one", 멀티플렉서 절은 "multiplexing the terminal I/O" 로 연다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 03-02",
      "자주 치는 것일수록 짧아야 한다",
      "3장 가운데 구간 노트의 절 여섯을 읽는 순서로 이은 지도. 1~3절이 지금 쓰는 셸에서 손을 덜 쓰는 법이고, "
      "4~5절이 셸 자체를 갈아 끼우는 판단, 6절이 터미널을 쪼개 쓰는 법이다.",
      "5절에서 저자가 자기 선택을 밝힙니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "짧게 치는 법 두 가지", "별칭과 커서 단축키"),
    ("§2", "편집기를 열지 않고 다루기", "만들고 덧붙이고 바꾸고 비교하기"),
    ("§3", "날짜를 숫자로 다루기", "에포크 시간과 2038년"),
    ("§4", "bash 는 1980년대 말 물건이다", "Fish 가 다르게 하는 두 가지"),
    ("§5", "어느 셸을 고를 것인가", "무엇에 초점이 있고 호환은 되는가"),
    ("§6", "창을 늘리는 대신 쪼갠다", "세션 · 윈도 · 페인과 붙었다 떼기"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(5):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 4)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(492, [("저자가 자기 선택을 밝히는 자리", ACC)])
d.save("03-02.chapter-overview.svg")
print("ok 03-02.chapter-overview")
