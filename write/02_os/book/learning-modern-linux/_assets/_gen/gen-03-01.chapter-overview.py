# 03-01 학습 목표 뒤 전체 지도 — 3장 앞부분(셸 기본)을 읽는 순서로 잇는다.
# 근거: 《Learning Modern Linux》 3장 "Basics" 가 터미널·셸 용어, 스트림, 변수, 종료 상태, 내장 명령,
#       잡 컨트롤, 모던 명령 순으로 간다. 칸의 값은 노트 본문이 Debian 12 · bash 5.2 에서 돌린 출력에서 왔다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절에서 쥐는 값)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "셸의 실체는 스트림과 변수와 종료 상태다",
      "3장 앞부분 노트의 절 여섯을 읽는 순서로 이은 지도. 1절이 터미널과 셸을 가르고, 2~4절이 스트림 · 변수 · "
      "종료 상태를 다루며, 5절이 잡과 세션, 6절이 자주 쓰는 명령의 모던 대체다. 칸마다 그 절에서 쥐는 값을 적었다.",
      "2절의 스트림이 나머지 절이 딛고 서는 바닥입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "터미널과 셸의 구분", "TERM · infocmp · sh 와 bash", MONO),
    ("§2", "프로세스가 받는 세 스트림", "FD 0 · 1 · 2,  >  2>  |,  버퍼 65,536 B", MONO),
    ("§3", "값을 담는 두 종류의 변수", "MY_VAR=42 와 export,  set · env", MONO),
    ("§4", "숫자로 알리는 종료 상태", "$? = 0 · 127 · 141,  PIPESTATUS", MONO),
    ("§5", "실행 중인 것을 다루는 법", "jobs · bg · fg,  SID · PGID,  SIGHUP", MONO),
    ("§6", "자주 쓰는 명령의 모던 대체", "eza · bat · rg · jq", MONO),
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

for i, (n, title, q, fam) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 12, MUTED, fam, "start")

d.legend(492, [("나머지가 딛고 서는 바닥", ACC)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01.chapter-overview")
