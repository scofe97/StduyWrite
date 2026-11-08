# 04-02.four-cni-compare — 4대 CNI 는 NetworkPolicy 강제 여부라는 첫 관문에서 갈린다
# 본문 요구: "Cilium·Calico 는 정책을 직접 강제하고 Flannel 은 flanneld 가 강제하지 않아 Helm 차트의 netpol 옵션 같은
#           별도 컨트롤러가 필요 … Weave Net 은 저장소가 아카이브 … 남은 둘은 배선 방식으로 갈립니다"
# 타입 스펙: type-dp-security-matrix — 행이 CNI, 열이 판정 축. 첫 관문 열만 행 색으로 칠해 판정 축임을 드러낸다.
#           Weave Net 은 후보에서 빠진 행이라 격자 아래 띠로 내렸다. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, PAPER, PAPER2, KR, MONO

W, H = 1000, 520
d = D(W, H, "FOUR CNIs · THE GATE AND THE WIRING",
      "4대 CNI 는 첫 관문에서 갈린다",
      "NetworkPolicy 를 직접 강제하는가가 첫 기준이고, 그다음 배선 방식이 캡슐화냐 라우팅 광고냐 커널 프로그램이냐로 갈린다.",
      lead="정책을 직접 강제하는지가 첫 관문 · 배선 방식은 그다음 축")

X0, GAP = 24, 12
COLS = [(172, "이름"), (236, "NetworkPolicy 강제 · 첫 관문"), (276, "배선 방식"), (244, "상태 저장소")]
HY, RY0, RH = 128, 144, 72
XS = []
x = X0
for w, name in COLS:
    XS.append((x, w)); d.t(x + w // 2, HY, name, 12, SOFT, KR, "middle", 600); x += w + GAP

ROWS = [("Cilium", OK, [("직접 강제", "L7 까지"), ("eBPF", "커널에서 처리"), ("Kubernetes CRD", "etcd 는 선택")]),
        ("Calico", OK, [("직접 강제", None), ("라우팅 또는 캡슐화", "BGP · VXLAN · IP-in-IP"), ("Kubernetes API", "또는 etcd")]),
        ("Flannel", WARN, [("flanneld 는 강제 안 함", "차트 netpol 옵션으로 보완"), ("L3 IPv4 오버레이", "VXLAN 등"), ("Kubernetes API", "또는 etcd")])]

for r, (name, rc, cells) in enumerate(ROWS):
    y = RY0 + r * (RH + GAP)
    nx, nw = XS[0]
    d.o.append(f'<rect x="{nx}" y="{y}" width="{nw}" height="{RH}" rx="6" fill="{rc}12" stroke="{rc}" stroke-width="1.2"/>')
    d.t(nx + nw // 2, y + 42, name, 15, rc, KR, "middle", 600)
    for i, (t, s) in enumerate(cells, 1):
        cx0, cw = XS[i]
        gate = i == 1
        d.o.append(f'<rect x="{cx0}" y="{y}" width="{cw}" height="{RH}" rx="6" '
                   f'fill="{rc + "12" if gate else PAPER2}" stroke="{rc if gate else RULE}" stroke-width="{1.2 if gate else 1.0}"/>')
        tc = rc if gate else INK
        if s:
            d.t(cx0 + 20, y + 32, ddx.fit(t, 13, cw - 40, t), 13, tc, KR, "start", 600)
            d.t(cx0 + 20, y + 54, ddx.fit(s, 12, cw - 40, s), 12, MUTED, KR, "start")
        else:
            d.t(cx0 + 20, y + 42, ddx.fit(t, 13, cw - 40, t), 13, tc, KR, "start", 600)

# 후보에서 빠진 행 — 격자 밖 띠
WY = RY0 + 3 * (RH + GAP) + 4
d.box(X0, WY, 952, 40, PAPER, RULE, 0.9, 6)
d.t(X0 + 20, WY + 26, "Weave Net", 13, SOFT, KR, "start", 600)
d.t(X0 + 136, WY + 26, "저장소 아카이브(2024-06) · 마지막 릴리스 v2.8.1(2021-01)", 12, SOFT, KR, "start")

d.legend(472, [("직접 강제", OK), ("별도 구성요소 필요", WARN), ("후보에서 빠짐", SOFT)])
d.save("04-02.four-cni-compare.svg")
print("ok four-cni-compare")
