# a0-03 §5 규격의 자리와 Istio 의 부품.
# 값 근거(본문 a0-03 §5, 원문 부록 C.2.4·C.2.5):
#   - 대응: Workload Endpoint = Istio 파일럿 에이전트, Workload API = Istio CA(istiod),
#     신원을 받는 워크로드 = 서비스 프록시(Envoy).
#   - 선택: SVID 형식(X.509·JWT) 중 X.509 선택, SAN URI 확장에 SPIFFE ID 인코딩 → auto mTLS.
# 타입 스펙: type-swimlane — 같은 자리를 규격과 구현이라는 두 주체로 갈라 나란히 놓는 것이 논점이다.
#           레인마다 같은 열에 대응하는 항목을 두고 열 사이에 화살표를 둔다.
#           축약: accent 는 그 대응이 낳은 결과(auto mTLS) 하나에 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 580


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ISTIO IN ACTION · A0-03 §5",
      "규격의 세 자리에 Istio 의 세 부품이 앉는다",
      "위 레인이 규격이 정한 자리이고 아래 레인이 Istio 가 거기 앉힌 부품이다. X.509 를 고른 덕에 "
      "워크로드끼리 상호 인증까지 되고, 색이 붙은 칸이 그 결과의 이름이다.",
      "에이전트가 곁에 있어 엔드포인트 자리에, CA 가 istiod 안이라 API 자리에 앉습니다")

LANE_H, LANE_Y0 = 124, 140
lanes = [("SPIFFE 규격", "무엇을 정했나"), ("ISTIO 구현", "무엇을 앉혔나")]
for k, (name, sub) in enumerate(lanes):
    top = LANE_Y0 + k * LANE_H
    d.line(0, top, W, top, RULE, 0.8)
    d.t(20, top + 52, name, 13, INK, kr(name), "start", 600)
    d.t(20, top + 76, sub, 13, MUTED, KR, "start")
d.line(0, LANE_Y0 + 2 * LANE_H, W, LANE_Y0 + 2 * LANE_H, RULE, 0.8)
d.line(164, LANE_Y0, 164, LANE_Y0 + 2 * LANE_H, RULE, 1.0)

SW, SH = 240, 76


def sx(j):
    return 188 + j * 264


def sy(k):
    return LANE_Y0 + k * LANE_H + 24


def cell(k, j, label, sub, c=None):
    x, y = sx(j), sy(k)
    if c:
        d.tone(x, y, SW, SH, c, 6, "14", 1.2)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(x + SW / 2, y + 30, label, 14, c or INK, kr(label), "middle", 600)
    d.t(x + SW / 2, y + 54, sub, 13, MUTED, kr(sub), "middle")


cell(0, 0, "Workload Endpoint", "신원을 부트스트랩")
cell(0, 1, "Workload API", "인증서를 발급")
cell(0, 2, "신원을 받는 워크로드", "그 신원으로 자기를 밝힘")
cell(1, 0, "파일럿 에이전트", "곁에 배포된다", INFO)
cell(1, 1, "Istio CA", "istiod 의 컴포넌트", INFO)
cell(1, 2, "서비스 프록시", "Envoy", INFO)

for j in range(3):
    cx = sx(j) + SW / 2
    d.arrow([(cx, sy(0) + SH), (cx, sy(1) - 2)], MUTED, "ar", 1.3)

BY = 408
d.tone(28, BY, 944, 68, ACC, 6, "14", 1.4)
d.t(48, BY + 26, "auto mTLS", 14, ACC, MONO, "start", 600)
d.t(48, BY + 50, "SVID 를 X.509 로 고른 덕에 공개 키가 함께 실린다 — 모든 워크로드가 상호 인증하고 트래픽을 암호화한다", 13, MUTED, KR, "start")

d.t(28, 504, "SVID 의 형식은 X.509 와 JWT 둘인데 Istio 는 앞을 골라 SPIFFE ID 를 SAN 의 URI 확장에 인코딩한다", 13, SOFT, KR, "start")
d.legend(528, [("그 선택이 낳은 결과", ACC), ("Istio 가 앉힌 부품", INFO)])
d.save("a0-03.istio-mapping.svg")
print("ok istio-mapping")
