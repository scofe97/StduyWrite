# 06-01 §2 — 죽음에는 두 경우가 있다
# 본문: "여기서 두 경우를 구분해야 합니다 — 같은 Pod 안의 컨테이너가 죽은 경우 / Pod 자체가 사라진 경우"
#       각 경우를 "누가 대응 → 오브젝트는 → phase 는" 으로 끝까지 따라간다.
# 타입 스펙: type-swimlane.md — 대응 주체가 갈리므로(kubelet / Deployment) 주체당 레인 하나를
#           두고 단계는 그 레인 안에 놓는다. 옛 판은 이 인과를 2x4 격자로 그려 칸이 서로
#           독립처럼 보였고, 위쪽에 pod-phases 도식의 phase 사슬을 재탕했다. 격자는 방향을
#           주지 않고 레인은 준다 — 스펙의 "steps placed inside the lane of the actor
#           performing them; arrows show flow" 를 따른다.
#           레인을 넘는 화살표(handoff)는 없다 — 두 경우는 인계가 아니라 서로 배타적 대안이다.
#           스펙이 handoff 를 "consider" 로 두므로 없어도 위반이 아니다.
#           1열은 레인 주체의 동작이 아니라 촉발 사건이라 파선·muted 로 낮추고 열 머리에 밝힌다.
# 관례형(§2 공식 없음) → stride 를 4의 배수로 고정: 셀폭 184 · 간격 24 · 레인 높이 136 · 레인 stride 152
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER, PAPER2, KR, MONO
from ddx import fit

W, H = 1000, 580
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "죽음에는 두 경우가 있다 — 누가 대응하고 phase 는 어떻게 되나",
      "같은 Pod 안의 컨테이너가 죽으면 kubelet 이 그 자리에서 다시 띄우므로 Pod 는 그대로 살아 있고 "
      "phase 도 Running 에 머문다. Pod 자체가 사라지면 그 Pod 의 복구는 없고 Deployment 가 새 Pod 를 "
      "만들어 Pending 부터 다시 시작한다.",
      lead="쿠버네티스는 Pod 를 고쳐 쓰지 않고 새로 만들어 교체한다")

LX, LW = 24, 952          # 레인 가로 범위
CW, GAP = 184, 24         # 셀 폭 · 간격
SX = 168                  # 셀 구역 시작 (왼쪽 140px 은 레인 라벨 여백)
CX = [SX + CW // 2 + i * (CW + GAP) for i in range(4)]
BH = 88                   # 셀 높이
LANE_H, LANE_STRIDE = 136, 152
Y1, Y2 = 170, 322         # 레인 상단
CY1, CY2 = Y1 + LANE_H // 2, Y2 + LANE_H // 2

d.box(LX, 104, LW, 404, PAPER2, RULE, 0.9, 8)
# 밴드 라벨은 두 레인을 가르는 축을 말하고, 되돌아가지 않는다는 사실은 하단 캡션이 진다 — 중복 금지
d.t(LX + 14, 126, "무엇이 죽었느냐가 대응 주체와 phase 를 가른다", 12, SOFT, KR, "start")

# 열 머리 — 1열은 사건이지 레인 주체의 동작이 아님을 여기서 밝힌다
for cx, h in zip(CX, ["① 무엇이 죽었나 (사건)", "② 대응 동작", "③ Pod 오브젝트는", "④ phase 는"]):
    d.t(cx, 154, fit(h, 12, CW, h), 12, SOFT, KR, "middle", 600)

def lane(y, cy, tag, sub, c, cells, focal_last=False):
    d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LANE_H}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.0" stroke-dasharray="7 6"/>')
    d.t(LX + 16, cy - 6, tag, 10, c, MONO, "start", 600)
    d.t(LX + 16, cy + 12, fit(sub, 10, 132, sub), 10, MUTED, KR, "start")
    for i, (cx, (t, s, g)) in enumerate(zip(CX, cells)):
        last = focal_last and i == 3
        trig = i == 0
        col = ACC if last else (MUTED if trig else c)
        if last:
            d.o.append(f'<rect x="{cx-CW//2}" y="{cy-BH//2}" width="{CW}" height="{BH}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        elif trig:
            d.o.append(f'<rect x="{cx-CW//2}" y="{cy-BH//2}" width="{CW}" height="{BH}" rx="6" '
                       f'fill="{PAPER}" stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="5 4"/>')
        else:
            d.box(cx - CW // 2, cy - BH // 2, CW, BH, PAPER2, c, 1.1, 6)
        d.t(cx, cy - 18, fit(t, 13, CW - 16, t), 13, col, KR, "middle", 600)
        d.t(cx, cy + 4, fit(s, 11, CW - 14, s), 11, MUTED, KR)
        d.t(cx, cy + 28, fit(g, 10, CW - 12, g), 10, SOFT,
            MONO if all(ord(ch) < 128 or ch in "·=" for ch in g) else KR)
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+CW//2+6} {cy} L {b-CW//2-10} {cy}", MUTED, 1.4, m="ar")

lane(Y1, CY1, "KUBELET", "같은 Pod 안에서 고친다", INFO, [
    ("컨테이너가 죽음", "같은 Pod 안에서", "컨테이너 수준의 사건"),
    ("그 자리에 다시 띄운다", "kubelet 이 재시작", "restarts 증가"),
    ("그대로 살아 있다", "오브젝트는 안 바뀐다", "같은 UID"),
    ("Running 유지", "phase 는 안 바뀐다", "실측 restarts=4"),
])

d.line(LX + 8, (Y1 + LANE_H + Y2) // 2, LX + LW - 8, (Y1 + LANE_H + Y2) // 2, RULE, 1.0)

lane(Y2, CY2, "DEPLOYMENT", "Pod 를 새로 만든다", WARN, [
    ("Pod 가 사라짐", "노드 장애·삭제", "Pod 수준의 사건"),
    ("새 Pod 를 만든다", "그 Pod 의 복구는 없다", "고쳐 쓰지 않는다"),
    ("새 오브젝트로 교체", "이름·UID 가 다르다", "다른 오브젝트"),
    ("Pending 부터 다시", "새 Pod 의 첫 phase", "되돌린 것이 아니다"),
], focal_last=True)

d.t(LX + 12, 488, "한번 Running 에 도달한 Pod 가 Pending 으로 되돌아가는 일은 실무에서 관찰되지 않는다 — "
                  "아랫줄의 Pending 은 되돌린 것이 아니라 새 Pod 의 첫 phase 다.", 12, MUTED, KR, "start")
d.legend(532, [("컨테이너 수준의 사건", INFO), ("Pod 교체", WARN), ("본문이 짚는 자리", ACC)])
d.save("06-01-phase-lifecycle-rules.svg")
print("ok phase-lifecycle-rules (swimlane)")
