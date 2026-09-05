# 03-01 학습 목표 뒤 전체 지도 — 3장 앞부분(셸 기본)을 읽는 순서로 잇는다.
# 원문 3장 "Basics": 터미널·셸 용어를 정의하고 스트림·변수·종료 상태·내장 명령·잡 컨트롤을 훑은 뒤
#       자주 쓰는 명령의 모던 대체를 소개한다. 저자는 "There are two major ways to interact with Linux,
#       from a CLI perspective. The first way is manually... The other mode of operation is the automated
#       processing of a series of commands" 로 장을 둘로 가른다. 이 노트는 그 앞쪽 절반의 기초 구간이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "셸의 실체는 스트림과 변수와 종료 상태다",
      "3장 앞부분 노트의 절 여섯을 읽는 순서로 이은 지도. 1절이 용어를 가르고, 2~4절이 셸을 셸이게 하는 "
      "세 가지이며, 5절이 실행 중인 것을 다루는 법, 6절이 같은 일을 덜 치고 하는 법이다.",
      "2절의 스트림이 나머지 절이 딛고 서는 바닥입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "터미널과 셸은 다른 것이다", "무엇이 창이고 무엇이 해석기인가"),
    ("§2", "모든 프로세스가 받는 세 갈래", "stdin · stdout · stderr 와 방향 바꾸기"),
    ("§3", "값을 담는 두 종류의 변수", "무엇이 자식에게 물려지는가"),
    ("§4", "명령은 숫자로 끝을 알린다", "0 과 1~255, 그리고 파이프의 함정"),
    ("§5", "실행 중인 것을 다루는 법", "앞으로 · 뒤로 · 셸을 닫아도 살리기"),
    ("§6", "같은 일을 덜 치고 한다", "ls·cat·grep 의 모던 대체"),
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
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(492, [("나머지가 딛고 서는 바닥", ACC)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01.chapter-overview")
