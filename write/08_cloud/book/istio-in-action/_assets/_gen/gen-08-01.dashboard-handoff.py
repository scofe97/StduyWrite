# 08-01 §2 Istio 대시보드가 Grafana 로 들어오는 손잡이.
# 본문: 대시보드 JSON 은 공식 배포판에 없어 소스나 grafana.com 에서 받아야 하고, 컨피그맵으로 만든 뒤
#       grafana_dashboard=1 라벨을 달아야 Grafana 사이드카가 집어 간다. 라벨이 레인을 넘는 손잡이다.
# 타입 스펙: type-swimlane — 같은 목표를 세 주체가 나눠 맡고 레인을 넘는 손잡이가 논점이다.
#           레인마다 왼쪽 여백에 mono eyebrow, 레인 구분선 1px, accent 는 손잡이 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 528
d = D(W, H, "ISTIO IN ACTION · 08-01 §2",
      "대시보드는 라벨 하나로 건너간다",
      "Istio 배포판에서 빠진 대시보드 JSON 여섯을 받아 컨피그맵으로 만들고, 라벨을 달면 Grafana 사이드카가 "
      "집어 간다. 색이 붙은 손잡이가 없으면 컨피그맵은 만들어져 있어도 화면에 나타나지 않는다.",
      "라벨을 감시하는 쪽은 Istio 가 아니라 kube-prometheus 스택의 Grafana 사이드카입니다")

LANE_H, LANE_Y0 = 112, 104
lanes = [("ISTIO SOURCE", "github · grafana.com"),
         ("OPERATOR", "kubectl"),
         ("GRAFANA", "prometheus ns")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 48, name, 9, SOFT, MONO, "start", 600)
    d.t(20, top + 66, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 3 * LANE_H, W, LANE_Y0 + 3 * LANE_H, RULE, 0.8)
d.line(184, LANE_Y0, 184, LANE_Y0 + 3 * LANE_H, RULE, 1.0)

SW, SH = 210, 64
def sx(j): return 232 + j * 246
def sy(k): return LANE_Y0 + k * LANE_H + 24
def step(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 26, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 46, sub, 9, MUTED, MONO)

# 레인 안 이동
d.arrow([(sx(1) + SW, sy(1) + SH / 2), (sx(2) - 2, sy(1) + SH / 2)], MUTED, "ar", 1.4)
# 레인을 넘는 이동 — 소스에서 운영자로
d.path(f"M {sx(0) + SW / 2} {sy(0) + SH} L {sx(0) + SW / 2} {sy(1) + SH / 2} L {sx(1) - 2} {sy(1) + SH / 2}", MUTED, 1.4, m="ar")
# 손잡이 — 라벨을 단 뒤에야 아래 레인으로 건너간다
d.path(f"M {sx(2) + SW / 2} {sy(1) + SH} L {sx(2) + SW / 2} {sy(2) + SH / 2} L {sx(3) - 2} {sy(2) + SH / 2}", ACC, 1.6, m="acc")
d.t(sx(2) + SW / 2 + 12, sy(2) - 6, "grafana_dashboard=1", 11, ACC, MONO, "start", 600)

step(0, 0, "대시보드 JSON 여섯", "ch8/dashboards")
step(1, 1, "컨피그맵으로 만든다", "create cm istio-dashboards")
step(1, 2, "라벨을 단다", "kubectl label cm")
step(2, 3, "사이드카가 집어 간다", "Home 에 목록이 뜬다", focal=True)

d.t(32, 464, "공식 배포판에는 없다 — 소스나 grafana.com/orgs/istio/dashboards 에서 받는다", 11, SOFT, KR, "start")
d.legend(488, [("라벨이 없으면 건너가지 않는다", ACC)])
d.save("08-01.dashboard-handoff.svg")
