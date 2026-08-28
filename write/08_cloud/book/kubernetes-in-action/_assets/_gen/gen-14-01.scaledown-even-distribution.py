# 14-01 §4 — 어느 것을 지우느냐가 분산을 정한다
# 본문이 "안 그러면 한 노드에 3벌이 몰릴 수 있다"로 반사실을 든다. before/after 만으로는
# 부족하고, 몰린 노드를 골라 지운 결과와 아무거나 지운 결과가 나란히 놓여야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 세 경우(지금·몰린 것부터·아무거나), 열은 노드 셋과 그 결과. 칸만 있고 흐름은 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 768, "KUBERNETES IN ACTION · 14-01",
      "몰린 노드의 것을 먼저 지운다",
      "5 벌을 3 벌로 줄일 때 어느 것을 지우느냐가 분산을 정한다. 복제본이 몰린 노드의 파드를 먼저 지우지 "
      "않으면 줄인 뒤에 한 노드에 3 벌이 남을 수 있다.",
      "노드 A 1 벌 · 노드 B 1 벌 · 노드 C 3 벌 → replicas 3")

NODES = ("노드 A", "노드 B", "노드 C")

def row(y0, label, marks, note, note_c):
    ddx.band(d, y0, y0 + 168, label, x=24, w=1172)
    for i, nm in enumerate(NODES):
        x0 = 110 + i * 300
        d.box(x0, y0 + 44, 260, 104, PAPER, RULE, 0.9, 8)
        d.t(x0 + 130, y0 + 68, nm, 11, SOFT, KR)
        col = marks[i]
        for j, mk in enumerate(col):
            cx = x0 + 130 + (j - (len(col) - 1) / 2) * 78
            if mk == "f":
                ddx.focal_tag(d, cx, y0 + 110, "지운다", 70)
            elif mk == "x":
                ddx.tag(d, cx, y0 + 110, "지운다", BAD, 70)
            else:
                ddx.tag(d, cx, y0 + 110, "파드", OK, 70)
    d.t(1050, y0 + 110, note, 11, note_c, KR)

row(100, "지금 — 5 벌", ([None], [None], [None, None, None]),
    "노드 C 에 몰려 있다", SOFT)
row(292, "몰린 노드 것을 먼저 지우면", ([None], [None], [None, "f", "f"]),
    "1 · 1 · 1 로 고르게 남는다", ACC)
row(484, "아무거나 지우면", (["x"], ["x"], [None, None, None]),
    "한 노드에 3 벌이 몰린다", BAD)

d.t(24, 684, "다만 이 정렬은 보장이 아니다. 공식 문서의 알고리즘은 Pending 먼저 · pod-deletion-cost 낮은 것 먼저 · "
             "복제본이 많은 노드 먼저 · 더 최근에 만들어진 것 먼저 순이고, 넷이 같으면 무작위다.",
     11, MUTED, KR, "start")
d.legend(706, [("남는 파드", OK), ("지워지는 파드", BAD), ("분산을 지키는 선택", ACC)])
d.save("14-01-scaledown-even-distribution.svg")
print("ok")
