# 07-01 §7 차원 하나를 더할 때 손대야 하는 두 자리.
# 본문: "컨트롤 플레인 설정으로 무엇을 셀지 정하고, 워크로드 애노테이션으로 프록시에 그것을 내보내도 좋다고
#       알립니다." 두 레인이 모두 프록시 레인에 닿아야 값이 보인다.
# 타입 스펙: type-swimlane — 같은 목표를 두 주체가 나눠 맡고 레인을 넘는 손잡이가 논점이다.
#           레인마다 왼쪽 여백에 mono eyebrow, 레인 구분선은 1px, accent 는 잊기 쉬운 손잡이 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 508
d = D(W, H, "ISTIO IN ACTION · 07-01 §7",
      "새 차원은 두 자리를 함께 고쳐야 보인다",
      "컨트롤 플레인 설정이 무엇을 셀지 정하고, 워크로드 애노테이션이 프록시에 그 이름을 알린다. "
      "색이 붙은 손잡이가 빠뜨리기 쉬운 쪽이다. 애노테이션 없이는 차원이 설정돼 있어도 노출되지 않는다.",
      "애노테이션은 배포의 metadata 가 아니라 spec.template.metadata 에 붙습니다")

LX, LW = 160, 840
LANE_H, LANE_Y0 = 112, 104
lanes = [("CONTROL PLANE", "IstioOperator"),
         ("WORKLOAD", "Deployment"),
         ("PROXY", "istio-proxy")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(16, top + 48, name, 9, SOFT, MONO, "start", 600)
    d.t(16, top + 66, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 3 * LANE_H, W, LANE_Y0 + 3 * LANE_H, RULE, 0.8)
d.line(LX - 16, LANE_Y0, LX - 16, LANE_Y0 + 3 * LANE_H, RULE, 1.0)

SW, SH = 192, 64
def sx(j): return 188 + j * 224
def sy(k): return LANE_Y0 + k * LANE_H + 24
def step(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 26, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 46, sub, 9, MUTED, MONO)

# 레인 안 화살표 먼저
d.arrow([(sx(0) + SW, sy(0) + SH / 2), (sx(1) - 2, sy(0) + SH / 2)], MUTED, "ar", 1.4)
d.arrow([(sx(1) + SW, sy(0) + SH / 2), (sx(2) - 2, sy(0) + SH / 2)], MUTED, "ar", 1.4)
d.arrow([(sx(0) + SW, sy(1) + SH / 2), (sx(1) - 2, sy(1) + SH / 2)], MUTED, "ar", 1.4)
# 레인을 넘는 손잡이
# 컨트롤 플레인 경로도 같은 상자로 들어가야 한다. 세로로만 내리면 그 열(636~828)
# 오른쪽 빈 자리에서 끝나 허공을 가리킨다. ACC 손잡이가 왼쪽에서 들어오므로 대칭으로 오른쪽에서.
d.path(f"M 912 {sy(0) + SH} L 912 {sy(2) + SH / 2} L {sx(2) + SW + 2} {sy(2) + SH / 2}", MUTED, 1.4, m="ar")
d.path(f"M 632 {sy(1) + SH} L 632 {sy(2) + SH / 2} L {sx(2) - 2} {sy(2) + SH / 2}", ACC, 1.6, m="acc")
d.t(500, sy(2) + SH / 2 - 12, "없으면 노출되지 않는다", 11, ACC, KR, "start", 600)   # 손잡이 수직 구간(x=632) 왼쪽에서 끝나게

step(0, 0, "dimensions 를 적는다", "configOverride")
step(0, 1, "설치를 갱신한다", "istioctl install")
step(0, 2, "필터가 갱신된다", "stats-filter-1.13")
step(1, 0, "extraStatTags 를 적는다", "proxy.istio.io/config")
step(1, 1, "배포를 적용한다", "kubectl apply")
step(2, 2, "새 차원이 붙어 나온다", "istio_requests_total")

d.legend(464, [("빠뜨리기 쉬운 자리", ACC)])
d.save("07-01.two-place-config.svg")
