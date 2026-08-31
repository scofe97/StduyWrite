# 10-01 §4 config_dump 를 xDS 축으로 자르면 무엇이 나오는가.
# 본문(원문 10.3.2): istioctl proxy-config 는 Envoy xDS API 에 맞춰 하위 명령이 이름 지어져 있다 —
#       cluster · endpoint · listener · route · secret. 그리고 리스너는 Istio 에서 Gateway 리소스로,
#       라우트는 VirtualService 로 설정되며, 클러스터는 자동 발견되거나 DestinationRule 로 정의된다.
#       엔드포인트는 요청을 처리하는 워크로드의 IP 주소다.
# 세 레인이 같은 네 칸을 두고 각각 다른 이름을 쓰는 것이 이 절의 논점이다.
# 타입 스펙: type-swimlane — 같은 단계 열을 세 주체가 나눠 맡는다. 레인마다 왼쪽 여백에 mono eyebrow,
#           레인 구분선 1px, accent 는 이 장에서 비어 있던 칸 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 540
d = D(W, H, "ISTIO IN ACTION · 10-01 §4",
      "같은 네 칸을 셋이 다른 이름으로 부른다",
      "13,934줄짜리 config_dump 를 xDS 축으로 자르면 네 칸이 남는다. 명령 · 프록시 설정 · 사람이 쓰는 "
      "리소스가 같은 칸을 다른 이름으로 부를 뿐이다. 색이 붙은 칸이 저자의 예제에서 비어 있던 자리다.",
      "가운데 레인의 화살표 방향이 요청이 지나는 순서입니다")

LANE_H, LANE_Y0 = 104, 108
lanes = [("ISTIOCTL", "꺼내는 명령"),
         ("ENVOY", "프록시 안의 설정"),
         ("ISTIO", "사람이 쓰는 리소스")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 46, name, 9, SOFT, MONO, "start", 600)
    d.t(20, top + 64, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 3 * LANE_H, W, LANE_Y0 + 3 * LANE_H, RULE, 0.8)
d.line(184, LANE_Y0, 184, LANE_Y0 + 3 * LANE_H, RULE, 1.0)

SW, SH = 210, 60
def sx(j): return 232 + j * 246
def sy(k): return LANE_Y0 + k * LANE_H + 22
def cell(k, j, label, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 26, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 46, sub, 9, MUTED, MONO)

for j in range(4):
    d.line(sx(j) + SW / 2, LANE_Y0 + 8, sx(j) + SW / 2, LANE_Y0 + 3 * LANE_H - 8, RULE, 0.8, "3 6")
for j in range(3):
    d.arrow([(sx(j) + SW, sy(1) + SH / 2), (sx(j + 1) - 2, sy(1) + SH / 2)], MUTED, "ar", 1.4)

cell(0, 0, "pc listeners", "--port · deploy/…")
cell(0, 1, "pc routes", "--name http.8080")
cell(0, 2, "pc clusters", "--fqdn --port --subset")
cell(0, 3, "pc endpoints", "--cluster \"outbound|…\"")
cell(1, 0, "리스너", "0.0.0.0:8080")
cell(1, 1, "라우트", "http.8080")
cell(1, 2, "클러스터", "subset 별 묶음")
cell(1, 3, "엔드포인트", "10.1.0.60:3000")
cell(2, 0, "Gateway", "포트를 연다")
cell(2, 1, "VirtualService", "가중치를 적는다")
cell(2, 2, "DestinationRule", "없으면 클러스터도 없다", focal=True)
cell(2, 3, "자동 발견", "쿠버네티스 엔드포인트")

d.t(32, 456, "라우트는 나열된 순서대로 평가되고 처음 맞는 것이 쓰인다 — 뒤에 적은 규칙은 가려질 수 있다", 11, SOFT, KR, "start")
d.legend(484, [("예제에서 비어 있던 칸", ACC), ("요청이 지나는 순서", MUTED)])
d.save("10-01.config-slices.svg")
