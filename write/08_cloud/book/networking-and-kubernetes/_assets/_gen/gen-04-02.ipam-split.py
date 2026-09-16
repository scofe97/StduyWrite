# 04-02.ipam-split — 주소 재고는 위에서 잘려 내려오고, 배분은 배선과 다른 플러그인이 맡는다
# 본문 요구: "명세에는 두 번째 인터페이스 IPAM … IPAM 플러그인이 인터페이스 IP·게이트웨이·경로를 결정 …
#           --cluster-cidr 로 준 전체 대역을 컨트롤러가 잘라 노드의 spec.podCIDR 에 적어 둔 값"
# 타입 스펙: type-data-flow — 주소 한 조각이 전체 대역 → 노드 조각 → 설정 → IPAM → 배선 플러그인으로 건너간다.
#           손으로 쓴 SVG 의 "둘을 갈라 둔 값" 장점 칸은 본문 205행이 이미 말하므로 뺐다(장점 격자 안티패턴).
#           손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 472
d = D(W, H, "IPAM · WHERE ONE POD ADDRESS COMES FROM",
      "주소 재고는 위에서 내려오고 배분은 따로 갈라져 있다",
      "클러스터 전체 대역이 노드별 조각으로 잘려 내려오고, 그 조각을 IPAM 플러그인이 Pod 하나에게 배분한다. "
      "배선 플러그인과 IPAM 은 별개 인터페이스다.",
      lead="배선하는 플러그인과 주소를 정하는 플러그인이 따로라 둘을 따로 고른다")

# 1행 — 재고가 내려오는 길
d.t(32, 116, "재고가 내려오는 길", 12, SOFT, KR, "start", 600)
BW, BH, STRIDE, X0, Y1 = 272, 72, 332, 32, 128
CX = [X0 + BW // 2 + i * STRIDE for i in range(3)]          # 168 500 832
STOCK = [("클러스터 전체 대역", "--cluster-cidr 10.1.0.0/16"),
         ("노드 조각", "spec.podCIDR 10.1.3.0/24"),
         ("설정 JSON 의 ipam 칸", '"subnet": "10.1.3.0/24"')]
for cx, (t, s) in zip(CX, STOCK):
    d.box(cx - BW // 2, Y1, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(cx, Y1 + 28, t, 13, MUTED, KR, "middle", 600)
    d.t(cx, Y1 + 52, ddx.fit(s, 12, BW - 16, s), 12, INK, MONO, "middle", 600)
for i, lab in enumerate(["분할", "기록"]):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.arrow([(a + 6, Y1 + BH // 2), (b - 10, Y1 + BH // 2)], MUTED, "ar", 1.5)
    d.t((a + b) // 2, Y1 + BH // 2 - 12, lab, 12, SOFT, KR)

# 2행 — 호출 한 번에서 갈리는 두 인터페이스
Y2, BH2 = 280, 112
d.t(32, Y2 - 16, "호출 한 번에서 갈리는 두 인터페이스", 12, SOFT, KR, "start", 600)
WX, WW = 32, 400
IX, IW = 568, 400
d.box(WX, Y2, WW, BH2, PAPER2, OK, 1.2, 8)
d.t(WX + 24, Y2 + 30, "배선 플러그인", 14, OK, KR, "start", 600)
d.t(WX + 24, Y2 + 56, "veth 생성 · 브리지 연결 · 네임스페이스 안으로", 12, MUTED, KR, "start")
d.t(WX + 24, Y2 + 88, "bridge · macvlan · ptp …", 12, SOFT, MONO, "start")
d.box(IX, Y2, IW, BH2, PAPER2, INFO, 1.2, 8)
d.t(IX + 24, Y2 + 30, "IPAM 플러그인", 14, INFO, KR, "start", 600)
d.t(IX + 24, Y2 + 56, "재고에서 주소 배분 · 게이트웨이 · 경로 결정", 12, MUTED, KR, "start")
d.t(IX + 24, Y2 + 88, "host-local · dhcp · 자체 구현", 12, SOFT, KR, "start")

# 재고 → IPAM (세로), 배선 ↔ IPAM (가로 두 줄)
d.arrow([(CX[2], Y1 + BH + 6), (CX[2], Y2 - 10)], INFO, "info", 1.5)
d.t(CX[2] + 12, Y1 + BH + 44, "재고", 12, INFO, KR, "start")
ya, yb = Y2 + 40, Y2 + 76
d.arrow([(WX + WW + 6, ya), (IX - 10, ya)], MUTED, "ar", 1.5)
d.t((WX + WW + IX) // 2, ya - 10, "주소 요청", 12, MUTED, KR)
d.arrow([(IX - 6, yb), (WX + WW + 10, yb)], INFO, "info", 1.5, "6 5")
d.t((WX + WW + IX) // 2, yb + 22, "10.1.3.7", 12, INFO, MONO, "middle", 600)

d.legend(424, [("선을 놓는 쪽", OK), ("주소를 정하는 쪽", INFO)])
d.save("04-02.ipam-split.svg")
print("ok ipam-split")
