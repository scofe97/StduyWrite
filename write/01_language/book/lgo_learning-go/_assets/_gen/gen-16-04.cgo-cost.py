# 16-04.cgo-cost — 빈 C 함수 한 번 호출 비용을 툴체인 넷으로 잰 막대(중앙값)와 다섯 번 측정 범위. Go 1.26 부터 내려간다
# 본문 요구(16-04 §3 「이 노트에서 빈 C 함수 호출은 go1.25.1 에서 약 26ns, Go 1.26 부터 약 18~19ns 였습니다」): 중앙값 26.37 · 25.49 · 17.93 · 19.42 ns,
#           범위 25.65~27.18 · 25.42~26.78 · 16.96~21.85 · 17.15~24.63.
# 타입 스펙: type-bar — 세로 막대 4개(pitch 180, 막대 88), 값축 0~30ns 선형(0 부터). 막대 위 세로 선이 다섯 번 측정 범위. focal 은 go1.26.8 막대 하나.
# 사실 출처: go1.24.4·go1.25.1·go1.26.8·go1.27.1 darwin/arm64(Apple M3) 에서 C noop 호출을 b.Loop 벤치마크 -count 5 (2026-09-29), Go 1.26 릴리스 노트.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 520
PY0, PY1 = 400, 140          # y at 0ns, y at 30ns
VMAX = 30.0
X0, PITCH, BW = 200, 180, 88


def py(v):
    return round(PY0 - v / VMAX * (PY0 - PY1))


d = D(W, H, "BAR · 16-04 §3",
      "cgo 호출 비용은 Go 1.26 에서 줄었지만 여전히 고정비가 큽니다",
      "아무 일도 하지 않는 C 함수를 한 번 부르는 데 든 나노초. 막대는 다섯 번 측정의 중앙값, 가는 세로선은 최솟값에서 최댓값까지다. "
      "go1.24.4 26.37ns, go1.25.1 25.49ns 에서 go1.26.8 17.93ns, go1.27.1 19.42ns 로 내려갔다. Go 1.26 릴리스 노트는 cgo 호출의 기본 비용이 약 30% 줄었다고 적는다.",
      lead="막대는 중앙값, 가는 세로선은 다섯 번 측정의 범위입니다. 값축은 0 부터 선형입니다.")

for v in range(0, 31, 10):
    y = py(v)
    d.line(X0 - 40, y, X0 + 3 * PITCH + BW + 40, y, RULE, 0.8 if v else 1.0)
    d.t(X0 - 52, y + 4, f"{v}ns", 11, MUTED, MONO, "end")

rows = [("go1.24.4", 26.37, 25.65, 27.18, INFO), ("go1.25.1", 25.49, 25.42, 26.78, INFO),
        ("go1.26.8", 17.93, 16.96, 21.85, ACC), ("go1.27.1", 19.42, 17.15, 24.63, OK)]
for i, (tc, med, lo, hi, c) in enumerate(rows):
    x = X0 + i * PITCH
    y = py(med)
    d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{PY0 - y}" fill="{PAPER}"/>')
    d.tone(x, y, BW, PY0 - y, c, 2, "22" if c == ACC else "14", 1.3 if c == ACC else 1.0)
    cx = x + BW / 2
    d.line(cx, py(hi), cx, py(lo), INK, 1.2)
    d.line(cx - 8, py(hi), cx + 8, py(hi), INK, 1.2)
    d.line(cx - 8, py(lo), cx + 8, py(lo), INK, 1.2)
    d.t(cx, py(hi) - 10, f"{med:.2f}", 12, c, MONO, "middle", 600)
    d.t(cx, PY0 + 22, tc, 12, INK, MONO, "middle", 600)
d.t(X0 + 2 * PITCH + BW / 2, PY0 + 42, "Go 1.26 약 30% 감소", 11, ACC, KR, "middle", 600)

d.legend(464, [("Go 1.26 이전", INFO), ("Go 1.26", ACC), ("Go 1.27", OK)])
d.save("16-04.cgo-cost.svg")
print("ok 16-04 cgo-cost")
