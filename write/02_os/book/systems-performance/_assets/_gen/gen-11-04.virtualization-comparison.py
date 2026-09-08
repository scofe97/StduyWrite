# 11-04 §4 — 세 기술은 성능이 아니라 관측성에서 갈린다.
# 타입 스펙: type-dp-security-matrix — 세 기술 × 네 속성의 비교 격자다.
#           축약: 보안 격자가 아니라 성능·관측 속성 격자로 문법만 빌린다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 572
CW, RH, X0, Y0, GAP = 240, 60, 220, 152, 16

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-04 §4",
       "세 기술은 관측성에서 갈린다",
       "CPU·I/O 성능은 셋 다 높다. 갈리는 곳은 메모리 할당 유연성과, 누가 무엇을 볼 수 있느냐다.",
       "마이크로벤치마크로 비교하면 정작 중요한 관측 능력을 놓칩니다")

COLS = ["하드웨어 VM", "컨테이너", "경량 VM"]
for i, c in enumerate(COLS):
    d.t(X0 + i * (CW + GAP) + CW / 2, Y0 - 16, c, 14, INK, KR, "middle", 600)

ROWS = [
    ("CPU · I/O 성능", [("높음", OK), ("높음", OK), ("높음", OK)]),
    ("메모리 할당", [("고정", WARN), ("유연", OK), ("고정", WARN)]),
    ("호스트 관측성", [("중간", WARN), ("높음", OK), ("중간", WARN)]),
    ("게스트 관측성", [("높음", OK), ("중간", WARN), ("높음", OK)]),
    ("관측이 유리한 쪽", [("엔드유저", ACC), ("호스트 운영자", ACC), ("엔드유저", ACC)]),
]

for r, (label, cells) in enumerate(ROWS):
    y = Y0 + r * (RH + 4)
    d.t(X0 - 20, y + RH / 2 + 4, label, 13, SOFT, KR, "end", 600)
    for i, (txt, c) in enumerate(cells):
        x = X0 + i * (CW + GAP)
        if c is ACC: d.tone(x, y, CW, RH, c, 6)
        else: d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
        d.t(x + CW / 2, y + RH / 2 + 5, txt, 13, c, KR, "middle", 600)

YB = Y0 + 5 * (RH + 4) + 24
d.t(X0 - 196, YB, "관측은 불필요한 일을 찾아 없애게 해 줍니다 — 그 이득이 하이퍼바이저 사이의 성능 차보다 큽니다",
    13, MUTED, KR, "start")

d.legend(YB + 28, [("선택을 가르는 축", ACC), ("유리", OK), ("제한", WARN)])
d.save("11-04.virtualization-comparison.svg")
