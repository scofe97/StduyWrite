# 타입 스펙: type-process — 다익스트라가 회차마다 한 노드씩 확정하며 표를 채워 가는 과정.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.1 Table 5.1
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 1000, 640
d = D(W, H, "SECTION 5.2.1 · DIJKSTRA STEP BY STEP",
      "회차마다 한 노드씩 확정됩니다",
      "u 를 출발지로 다익스트라를 돌릴 때 회차별로 D(v) 와 전임 p(v) 가 어떻게 바뀌는지 보여 주는 표. 회차마다 확정되지 않은 노드 중 가장 싼 것 하나가 N' 에 들어가고, 그 노드를 거쳐 더 싸지는 이웃만 값을 내린다.",
      "N' 밖에서 가장 싼 노드를 확정하고, 그를 거쳐 더 싸지는 이웃만 값을 내립니다")

COLS = [("회차", 66), ("확정된 N'", 150), ("v", 110), ("w", 110), ("x", 110), ("y", 110), ("z", 110)]
X0, Y0, HH, RH = 24, 152, 38, 46

# (회차, N', {노드: (표시값, 상태)})  상태 fix=이번에 확정 · new=값이 내려감 · same=그대로 · done=확정 완료
ROWS = [
    ("0", "u",      {"v": ("2, u", "new"), "w": ("5, u", "new"), "x": ("1, u", "new"), "y": ("∞", "same"), "z": ("∞", "same")}),
    ("1", "u x",    {"v": ("2, u", "same"), "w": ("4, x", "new"), "x": ("", "fix"),    "y": ("2, x", "new"), "z": ("∞", "same")}),
    ("2", "u x y",  {"v": ("2, u", "same"), "w": ("3, y", "new"), "x": ("", "done"),   "y": ("", "fix"),     "z": ("4, y", "new")}),
    ("3", "u x y v", {"v": ("", "fix"),     "w": ("3, y", "same"), "x": ("", "done"),  "y": ("", "done"),    "z": ("4, y", "same")}),
    ("4", "u x y v w", {"v": ("", "done"),  "w": ("", "fix"),     "x": ("", "done"),   "y": ("", "done"),    "z": ("4, y", "same")}),
    ("5", "u x y v w z", {"v": ("", "done"), "w": ("", "done"),   "x": ("", "done"),   "y": ("", "done"),    "z": ("", "fix")}),
]

xs, acc = [], X0
for _, cw in COLS:
    xs.append(acc); acc += cw
TW = acc - X0

# 헤더
d.box(X0, Y0, TW, HH, PAPER2, RULE, 1.0, 6)
for (name, cw), cx in zip(COLS, xs):
    d.t(cx + cw / 2, Y0 + 25, name, 11, INK, MONO if len(name) == 1 else KR, "middle", 600)

for r, (step, nprime, cells) in enumerate(ROWS):
    y = Y0 + HH + r * RH
    d.line(X0, y, X0 + TW, y, RULE, 0.8)
    d.t(xs[0] + COLS[0][1] / 2, y + 29, step, 11, MUTED, MONO)
    d.t(xs[1] + COLS[1][1] / 2, y + 29, nprime, 11, INK, MONO)
    for (name, cw), cx in list(zip(COLS, xs))[2:]:
        txt, st = cells[name]
        if st == "fix":
            d.tone(cx + 14, y + 10, cw - 28, 26, ACC, 5, "18", 1.2)
            d.t(cx + cw / 2, y + 28, "확정", 11, ACC, KR, "middle", 600)
        elif st == "new":
            d.t(cx + cw / 2, y + 29, txt, 11, ACC, MONO, "middle", 600)
        elif st == "same":
            d.t(cx + cw / 2, y + 29, txt, 11, MUTED, MONO)
        else:
            d.t(cx + cw / 2, y + 29, "·", 11, SOFT, MONO)

d.line(X0, Y0 + HH + len(ROWS) * RH, X0 + TW, Y0 + HH + len(ROWS) * RH, RULE, 0.8)
for cx in xs[1:]:
    d.line(cx, Y0, cx, Y0 + HH + len(ROWS) * RH, RULE, 0.5)

d.t(X0, 498, "칸의 값 = `D(노드), p(노드)` — 지금까지 아는 최소 비용과 그 경로의 전임 노드", 11, MUTED, KR, "start")
d.t(X0, 520, "1 회차 — x 확정 → w 5→4 · y ∞→2 (x 를 거치는 길이 생김)", 11, MUTED, KR, "start")
d.t(X0, 542, "2 회차 — v·y 가 나란히 2 · 동점은 임의로 깨고 원문은 y 채택", 11, MUTED, KR, "start")
d.t(X0, 564, "남는 것은 노드마다 전임 하나 · 거슬러 올라가 첫 홉만 뽑으면 u 의 전달 표", 11, INFO, KR, "start")

d.legend(600, [("이번 회차에 확정", ACC), ("값이 내려감", ACC), ("그대로", MUTED), ("확정 완료 — 더 안 봄", SOFT)])
d.t(976, 622, "KUROSE-ROSS 9E TABLE 5.1", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.dijkstra-steps.svg"
d.save(out)
print("→", out)
