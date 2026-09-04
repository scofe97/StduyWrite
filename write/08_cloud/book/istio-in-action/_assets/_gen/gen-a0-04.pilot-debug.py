# a0-04 §5 무엇을 묻는가로 갈리는 두 묶음.
# 본문(부록 D.2.1): "Endpoints that represent the service mesh state as known to the Pilot"
#       (/debug/adsz · adsz?push=true · edsz · authorizationz) 와 "Endpoints that represent
#       the data-plane configuration as known to the Pilot"(/debug/config_distribution ·
#       config_dump · syncz). syncz 는 nonce 두 개가 같으면 최신이다.
# 타입 스펙: type-swimlane — 같은 포트 아래 엔드포인트가 무엇을 묻느냐로 갈리는 것이 논점이다.
#           레인 둘에 같은 형식의 칸을 놓고 레인 라벨이 묻는 대상을 나른다.
#           축약: accent 는 10 장의 SYNCED 판정 근거가 되는 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 552
d = D(W, H, "ISTIO IN ACTION · A0-04 §5",
      "메시 상태를 묻는 쪽과 설정을 묻는 쪽",
      "8080 이 여는 엔드포인트는 두 묶음이다. 위는 Pilot 이 아는 메시 상태를, 아래는 Pilot 이 아는 "
      "데이터 플레인 설정을 묻는다. 색이 붙은 칸이 10 장의 SYNCED 판정이 실제로 읽는 자리다.",
      "nonce 두 개가 같으면 그 프록시가 최신 설정을 갖고 있다는 뜻입니다")

LANE_H, LANE_Y0 = 128, 140
lanes = [("메시 상태", "Pilot 이 아는 것"), ("데이터 플레인 설정", "Pilot 이 만든 것")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 56, name, 12, INK, KR, "start", 600)
    d.t(20, top + 76, sub, 11, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(180, LANE_Y0, 180, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 184, 80
def sx(j): return 204 + j * 196
def sy(k): return LANE_Y0 + k * LANE_H + 24
def cell(k, j, name, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 26, name, 11, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 12, y + 50, sub, 11, MUTED, KR, "start")

cell(0, 0, "/debug/adsz", "클러스터 · 라우트 · 리스너")
cell(0, 1, "adsz?push=true", "모든 프록시에 푸시 발동")
cell(0, 2, "/debug/edsz", "그 프록시가 아는 엔드포인트")
cell(0, 3, "authorizationz", "네임스페이스의 인가 정책")
cell(1, 0, "config_distribution", "붙은 Envoy 들의 버전 상태")
cell(1, 1, "/debug/config_dump", "생성한 Envoy 설정")
cell(1, 2, "/debug/syncz", "보낸 nonce 와 받은 nonce", focal=True)

d.t(sx(3) + 12, sy(1) + 26, "10 장의 proxy-status 가", 11, ACC, KR, "start", 600)
d.t(sx(3) + 12, sy(1) + 48, "읽는 것이 왼쪽 칸이다", 11, MUTED, KR, "start")
d.path(f"M {sx(3) + 4} {sy(1) + 40} L {sx(2) + SW + 4} {sy(1) + 40}", ACC, 1.4, m="acc")

d.t(28, 428, "kubectl -n istio-system port-forward deploy/istiod 8080 을 걸고 /debug 로 가면 전체 목록이 나온다", 11, INK, MONO, "start")
d.t(28, 452, "운영에서는 ENABLE_DEBUG_ON_HTTP=false 로 끄기를 권한다 — 대신 이 엔드포인트를 쓰는 도구가 깨진다", 11, SOFT, KR, "start")
d.legend(476, [("SYNCED 판정이 읽는 자리", ACC), ("나머지 엔드포인트", MUTED)])
d.save("a0-04.pilot-debug.svg")
