# a0-04 §5 무엇을 묻는가로 갈리는 두 묶음.
# 본문(부록 D.2.1): "Endpoints that represent the service mesh state as known to the Pilot"
#       (/debug/adsz · adsz?push=true · edsz · authorizationz) 와 "Endpoints that represent
#       the data-plane configuration as known to the Pilot"(/debug/config_distribution ·
#       config_dump · syncz). syncz 는 nonce 두 개가 같으면 최신이다.
# 타입 스펙: type-swimlane — 같은 포트(8080) 아래 엔드포인트가 묻는 대상으로 두 레인에 갈린다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 496
d = D(W, H, "ISTIO IN ACTION · A0-04 §5",
      "메시 상태를 묻는 묶음과 설정을 묻는 묶음",
      "8080 디버그 엔드포인트는 위 레인의 메시 상태 네 개와 아래 레인의 데이터 플레인 설정 "
      "세 개로 갈린다. 경로는 모두 /debug/ 아래에 있고 색이 붙은 syncz 가 istioctl proxy-status 의 SYNCED 판정 근거다.",
      lead="nonce 두 개가 같으면 프록시가 최신 설정을 갖고 있습니다")

LANE_H, LANE_Y0 = 136, 128
lanes = [("메시 상태", "Pilot 이 아는 것"), ("데이터 플레인 설정", "Pilot 이 만든 것")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 58, name, 13, INK, KR, "start", 600)
    d.t(20, top + 82, sub, 13, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(176, LANE_Y0, 176, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 180, 88
def sx(j): return 192 + j * 188
def sy(k): return LANE_Y0 + k * LANE_H + 24

def cell(k, j, name, sub, focal=False):
    x, y = sx(j), sy(k)
    if focal:
        d.tone(x, y, SW, SH, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 30, name, 12, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 12, y + 60, sub, 13, MUTED, KR, "start")

cell(0, 0, "adsz", "클러스터·라우트·리스너")
cell(0, 1, "adsz?push=true", "모든 프록시에 푸시 발동")
cell(0, 2, "edsz?proxyID=", "프록시가 아는 엔드포인트")
cell(0, 3, "authorizationz", "네임스페이스 인가 정책")

cell(1, 0, "config_distribution", "Envoy 들의 버전 상태")
cell(1, 1, "config_dump?proxyID=", "생성한 Envoy 설정")
cell(1, 2, "syncz", "송신·확인 nonce 비교", focal=True)

d.t(sx(3) + 12, sy(1) + 32, "istioctl proxy-status", 13, ACC, KR, "start", 600)
d.t(sx(3) + 12, sy(1) + 56, "SYNCED 판정 근거", 13, MUTED, KR, "start")
d.arrow([(sx(3) + 8, sy(1) + 44), (sx(2) + SW + 4, sy(1) + 44)], ACC, "acc", 1.4)

d.legend(436, [("SYNCED 판정이 읽는 자리", ACC)])
d.save("a0-04.pilot-debug.svg")
print("ok a0-04.pilot-debug")
