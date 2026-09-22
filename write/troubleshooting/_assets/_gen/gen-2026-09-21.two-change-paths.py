# 개념 노트 "파이프라인 밖에서 노드를 바꾸는 장치" — 변경이 노드에 닿는 두 길.
# 논지는 "같은 노드를 바꾸는 주체가 둘이고, 둘은 시작·확산·접촉·실패 처리가 모두 다르다" 이다.
# 타입 스펙: type-swimlane — 레인 하나가 변경 주체 하나다. 열은 네 물음(누가 시작·어떻게 넓어짐·어떻게 닿음·실패하면)으로 맞춘다.
#           type-timeline 은 기각 — 파이프라인 쪽 실제 시각이 원문에 없어 시간축을 지어내게 된다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 452
d = D(W, H, "TROUBLESHOOTING CONCEPT · CHANGE PATHS",
      "노드를 바꾸는 길은 파이프라인 하나가 아닙니다",
      "위 레인은 사람이 미는 배포 파이프라인이다. 리전 하나씩 넓히고, 노드를 새것으로 바꾸고, 실패하면 되돌린다. "
      "아래 레인은 OS 이미지에 든 자동 업데이트다. 아무도 밀지 않아도 타이머가 깨우고, 같은 이미지에서 온 노드는 "
      "리전이 달라도 같은 기본 창에 함께 돌고, 돌던 노드를 제자리에서 바꾸며, 되돌리는 장치가 없다.",
      lead="같은 네 물음에 두 레인이 정반대로 답합니다")

LBW, X0, CW, STRIDE = 144, 196, 168, 196
HEAD_Y = 112
COLS = ["누가 시작하나", "어떻게 넓어지나", "노드에 어떻게 닿나", "실패했을 때"]
for i, h in enumerate(COLS):
    d.t(X0 + i * STRIDE + CW // 2, HEAD_Y, h, 11, SOFT, KR, "middle")

LANES = [
    (128, "배포 파이프라인", "변경 관리 도구", OK, [
        ("사람이 밂", "변경 요청 하나", None),
        ("리전 하나씩", "클러스터 · 노드 순차", None),
        ("새 노드로 교체", "blue/green", None),
        ("자동 되돌림", "롤백", None),
    ]),
    (252, "OS 자동 업데이트", "이미지 속 타이머", BAD, [
        ("아무도 안 밂", "타이머가 깨움", None),
        ("리전 다섯 동시", "기본 창 06:00~07:00", "focal"),
        ("돌던 노드 제자리", "패키지 갱신 · 재시작", None),
        ("되돌림 없음", "바뀐 채 남음", None),
    ]),
]
LH = 100

for ly, name, sub, c, steps in LANES:
    d.line(32, ly - 8, W - 32, ly - 8, RULE, 0.8)
    d.o.append(f'<rect x="36" y="{ly + 8}" width="4" height="{LH - 16}" rx="2" fill="{c}"/>')
    d.t(52, ly + 44, name, 13, INK, KR, "start", 600)
    d.t(52, ly + 64, sub, 11, MUTED, KR, "start")
    for i, (title, s2, mark) in enumerate(steps):
        x = X0 + i * STRIDE
        if i < len(steps) - 1:
            d.arrow([(x + CW, ly + LH // 2), (x + STRIDE - 2, ly + LH // 2)], MUTED, "ar", 1.2)
        if mark == "focal":
            d.tone(x, ly + 12, CW, LH - 24, ACC, 6)
            tc = ACC
        else:
            d.box(x, ly + 12, CW, LH - 24, PAPER2, c, 0.9, 6)
            tc = INK
        d.t(x + CW // 2, ly + 44, title, 13, tc, KR, "middle", 600)
        d.t(x + CW // 2, ly + 64, s2, 11, MUTED, KR if any('가' <= ch <= '힣' for ch in s2) else MONO)
d.line(32, 252 + LH + 8, W - 32, 252 + LH + 8, RULE, 0.8)

d.legend(H - 56, [("통제되는 변경 경로", OK), ("통제 밖 변경 경로", BAD), ("동시 발동을 만든 기본값", ACC)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.two-change-paths.svg"))
print("ok")
