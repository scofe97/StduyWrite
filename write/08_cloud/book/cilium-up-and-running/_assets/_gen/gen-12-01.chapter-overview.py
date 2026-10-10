# 타입 스펙: type-data-flow — Pod 라벨이 identity 번호가 되고 ipcache 의 IP→identity 조회와 정책 맵 키 대조를 거쳐 TCP 8080 은 허용, TCP 9113 은 폐기되는 판정 흐름 (칸 사이를 건너가는 것은 출발 Pod 의 IP·identity 번호)
# 사실 출처: 추출본 cil12.txt 줄 44-58·152-175(8080 허용·9113 타임아웃), 220-224(기본 거부), 402-427(IP 캐시 표), 467-485(CiliumIdentity 22727·24505), 542-561(정책 맵 키 (22727, Ingress, TCP, 8080) → ALLOW)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 452
CW, GAP, X0 = 152, 28, 24
XS = [X0 + i * (CW + GAP) for i in range(5)]
HDR_Y, HDR_H = 96, 40
RH, Y0, STRIDE = 100, 152, 116


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in txt) else MONO


d = D(W, H, "CILIUM UP AND RUNNING · 12-01", "라벨에서 허용까지 — 정책 판정 데이터 흐름",
      "test Pod 의 라벨이 identity 22727 이 되고 ipcache 조회와 정책 맵 키 대조로 8080 은 허용, 9113 은 폐기된다",
      "같은 출발지가 포트에 따라 다른 판정을 받는다")

headers = ["출발 Pod", "CiliumIdentity", "노드 ipcache", "정책 맵 키", "판정"]
for x, nm in zip(XS, headers):
    d.box(x, HDR_Y, CW, HDR_H, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, HDR_Y + 25, nm, 12, INK, fam(nm), "middle", 600)

rows = [
    (["10.0.0.68", "run=test"], ["22727", "k8s:run: test"], ["10.0.0.68/32", "→ identity 22727"],
     ["22727 · Ingress", "TCP · 8080"], ["ALLOW", "웹 서버로 전달"], OK),
    (["10.0.0.68", "run=test"], ["22727", "k8s:run: test"], ["10.0.0.68/32", "→ identity 22727"],
     ["22727 · Ingress", "TCP 9113 항목 없음"], ["DROP", "응답 없이 폐기"], BAD),
]

for i, (c0, c1, c2, c3, c4, col) in enumerate(rows):
    y = Y0 + i * STRIDE
    cells = [c0, c1, c2, c3, c4]
    for j, lines in enumerate(cells):
        x = XS[j]
        if j == 4:
            d.tone(x, y, CW, RH, col, r=6, op="14", sw=1.3)
        elif j == 2 and i == 0:
            d.tone(x, y, CW, RH, ACC, r=6, op="16", sw=1.4)
        else:
            d.box(x, y, CW, RH, PAPER2, RULE, 0.9)
        for k, ln in enumerate(lines):
            c_text = col if (j == 4 and k == 0) else (INK if k == 0 else MUTED)
            d.t(x + CW / 2, y + 44 + k * 28, ln, 12, c_text, fam(ln), "middle", 600 if k == 0 else 400)
    for j in range(4):
        d.arrow([(XS[j] + CW + 2, y + RH / 2), (XS[j + 1] - 4, y + RH / 2)], MUTED, "ar", 1.5)

d.legend(396, [("허용", OK), ("폐기", BAD), ("초점 · IP → identity", ACC)])
d.save("12-01.chapter-overview.svg")
