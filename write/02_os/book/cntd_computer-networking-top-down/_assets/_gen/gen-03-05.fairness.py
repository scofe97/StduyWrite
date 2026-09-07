# 03-05 §5 — 원문 Figure 3.56. 두 연결의 처리량 평면에서 AIMD 가 공평선으로 수렴하는 궤적.
# 점 A·B·C·D 와 45도 증가·원점 방향 감소는 원문 3.7.4 의 논증 그대로다.
# 타입 스펙: type-scatter — 두 연속 변수를 축으로 놓고 점을 찍는다. 초점 점 하나만 강조색.
#           축약: 점들이 독립 표본이 아니라 시간 순서를 갖는 궤적이라 점 사이를 선으로 잇는다.
#           그 순서가 이 그림의 논증이므로, 스펙의 "점만" 규칙보다 원문의 논증을 우선했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 596
PX0, PY1 = 180, 452
SIDE = 300
R = 1.0

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-05 §5",
      "왜 반씩 나뉘는가",
      "두 연결의 처리량 평면. 더하기는 45도로 움직이고 나누기는 원점 쪽으로 당기므로 궤적이 공평선으로 수렴한다.",
      "평면 어디에서 시작하든 같은 곳으로 갑니다")

def px(v): return PX0 + v * SIDE
def py(v): return PY1 - v * SIDE

d.line(PX0, PY1, PX0 + SIDE * 1.15, PY1, MUTED, 1.0)
d.line(PX0, PY1, PX0, PY1 - SIDE * 1.15, MUTED, 1.0)
d.t(PX0 + SIDE * 0.58, PY1 + 30, "연결 1 의 처리량", 11, SOFT, KR)
d.t(PX0 - 14, PY1 - SIDE * 1.15 - 8, "연결 2 의 처리량", 11, SOFT, KR, "end")

# 공평선과 완전 이용선
d.path(f"M {px(0)} {py(0)} L {px(1.05)} {py(1.05)}", INFO, 1.3, dash="5 4")
d.t(px(1.06), py(1.06) - 8, "공평선", 11, INFO, KR, "start")
d.path(f"M {px(0)} {py(R)} L {px(R)} {py(0)}", OK, 1.3, dash="5 4")
d.t(px(R) + 8, py(0) - 14, "합이 R 인 선", 11, OK, KR, "start")

# 궤적 — A 에서 45도로 올라 B 에서 손실, 원점 쪽 절반으로 C, 다시 45도로 D …
TRAJ = [(0.14, 0.52, "A"), (0.38, 0.76, "B"), (0.19, 0.38, "C"),
        (0.36, 0.55, "D"), (0.18, 0.275, "E"), (0.34, 0.435, "F")]
for i in range(len(TRAJ) - 1):
    (x1, y1, _), (x2, y2, _) = TRAJ[i], TRAJ[i + 1]
    c = ACC if i % 2 else MUTED
    d.path(f"M {px(x1)} {py(y1)} L {px(x2)} {py(y2)}", c, 1.5, m="acc" if i % 2 else "ar")
for x, y, lab in TRAJ:
    focal = lab == "F"
    d.o.append(f'<circle cx="{px(x)}" cy="{py(y)}" r="{6 if focal else 5}" '
               f'fill="{ACC if focal else MUTED}" opacity="{1 if focal else 0.85}"/>')
    d.t(px(x) - 14, py(y) - 10, lab, 11, INK, MONO)

d.t(px(0.42), py(0.80), "합이 R 을 넘어 손실", 11, SOFT, KR, "start")
d.t(px(0.44), py(0.55), "둘 다 절반 — 원점 쪽으로", 11, ACC, KR, "start")
d.t(px(0.20), py(0.19), "차이가 매번 절반씩 줄어듭니다", 11, SOFT, KR, "start")

d.t(20, 512, "더하기는 방향이 45도로 고정이고 나누기는 원점 쪽으로 당깁니다. 당기는 동작이 두 값의 차이를 절반으로 줄이므로 공평선 위에서 오르내리게 됩니다.",
     11, MUTED, KR, "start")
d.t(20, 534, "현실에서는 깨집니다 — 왕복 시간이 다르거나, UDP 가 섞이거나, 한 앱이 병렬 연결을 여럿 열면 몫이 크게 갈립니다.",
     11, MUTED, KR, "start")

d.legend(H - 28, [("승산 감소 — 원점 방향", ACC), ("가산 증가 — 45도", MUTED)])
d.save("03-05.fairness.svg")
