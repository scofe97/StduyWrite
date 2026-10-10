# 타입 스펙: type-data-flow — 요청 값(경로·헤더·쿼리) 두 줄이 HTTPRoute 매치 규칙을 거쳐 서로 다른 Service 로 가는 두 행 흐름. 건너가는 것은 요청과 응답 값. 포커스는 헤더 규칙 행의 매치 칸.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 686-725(http-app-1 두 규칙), 859-862(GET /details/1 → JSON), 873-898(magic: foo, great=example → 200, server: envoy, x-envoy-upstream-service-time: 9)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 400
CW, GAPX, X0 = 256, 46, 24
XS = [X0 + i * (CW + GAPX) for i in range(3)]
RH, Y0, STRIDE = 104, 148, 128

d = D(W, H, "CILIUM UP AND RUNNING · 07-02 §2", "요청 값이 규칙을 거쳐 Service 로 간다",
      "Gateway 주소 172.18.255.200:80 으로 들어온 요청 둘", "Gateway 주소 172.18.255.200:80 으로 들어온 요청 둘")

for x, nm in zip(XS, ["요청", "HTTPRoute 규칙", "Service"]):
    d.box(x, 96, CW, 32, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, 117, nm, 13, INK, KR, "middle", 600)

rows = [
    (["GET /details/1", "헤더 없음 · 쿼리 없음"], ["path PathPrefix /details"], ["details:9080", "JSON · William Shakespeare"], False),
    (["GET /?great=example", "magic: foo"], ["magic = foo", "great = example · GET"], ["productpage:9080", "200 OK · server: envoy"], True),
]
for i, (req, rule, svc, focal) in enumerate(rows):
    y = Y0 + i * STRIDE
    for j, lines in enumerate([req, rule, svc]):
        x = XS[j]
        if focal and j == 1:
            d.tone(x, y, CW, RH, ACC, r=6, op="14", sw=1.4)
        else:
            d.box(x, y, CW, RH, PAPER2, RULE, 0.9)
        y1 = y + 44 if len(lines) > 1 else y + RH / 2 + 4
        for k, ln in enumerate(lines):
            col = (ACC if (focal and j == 1) else INK) if k == 0 else MUTED
            fam = KR if any("가" <= c <= "힣" for c in ln) else MONO
            d.t(x + CW / 2, y1 + k * 24, ln, 12, col, fam, "middle", 600 if k == 0 else 400)
    for j in range(2):
        d.arrow([(XS[j] + CW + 4, y + RH / 2), (XS[j + 1] - 6, y + RH / 2)], MUTED, "ar", 1.5)
d.save("07-02.httproute-match-flow.svg")
