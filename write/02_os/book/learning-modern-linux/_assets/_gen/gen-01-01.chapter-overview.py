# 01-01 학습 목표 뒤 전체 지도 — 1장 노트의 절 여섯을 읽는 순서로 잇는다.
# 원문: 1장은 modern 의 뜻 → 30년 약사 → 왜 OS 인가 → 배포판 → 자원 가시성 순으로 흐르고,
#       마지막 두 절에서 "PID 가 같은 프로세스가 여럿일 수 있다"는 물음이 컨테이너의 바탕이라고 못 박는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 01-01",
      "하드웨어를 가리고 나면 무엇이 보일지를 정해야 한다",
      "1장 노트의 절 여섯을 읽는 순서로 이은 지도. 1~3절이 운영체제가 무엇을 대신 지는가이고, "
      "4~5절이 그 위에서 자원 뷰가 갈라지는 자리, 6절이 그 갈라짐을 규정한 표준이다.",
      "5절에서 뷰와 격리가 서로 다른 축이라는 것이 밝혀집니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360]
cards = [
    ("§1", "OS 가 없으면 내가 다 한다", "메모리·인터럽트·I/O 를 누가 지나"),
    ("§2", "모던이 가리키는 무대", "폰·클라우드·IoT·달라진 CPU 계열"),
    ("§3", "커널과 배포판은 다른 말", "무엇까지가 커널이고 무엇이 묶음인가"),
    ("§4", "보는 자리에 따라 답이 갈린다", "같은 PID 가 둘일 수 있는가"),
    ("§5", "뷰와 격리는 다른 축", "namespace 와 cgroup 이 각각 무엇을 하나"),
    ("§6", "POSIX 가 뜻하는 것", "호환이라는 말의 범위는 어디까지인가"),
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

d.legend(492, [("이 장이 컨테이너로 이어지는 자리", ACC)])
d.save("01-01.chapter-overview.svg")
print("ok 01-01.chapter-overview")
