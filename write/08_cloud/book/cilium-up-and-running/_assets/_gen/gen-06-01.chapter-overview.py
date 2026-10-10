# 타입 스펙: type-layers — 클라이언트에서 백엔드 Pod 까지 요청이 거치는 층과 바깥에 붙는 LB IPAM·BGP 의 자리 (배정 타입 type-layers 그대로)
# 사실 출처: 추출본 cil6.txt 줄 220-231(맵 조회), 888-920·988-991(httpd LoadBalancer 10.96.72.137·31478·192.168.9.1), 1045-1048(광고는 별도) / docs.cilium.io v1.20 network/lb-ipam, kubeproxy-free
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 06-01", "Service 요청이 거치는 층",
      "VIP 는 eBPF 맵 조회로 백엔드가 되고, 외부 IP 는 LB IPAM 이 붙입니다",
      "에이전트가 맵을 쓰고 프로그램이 읽습니다")

LX, LW, LH, Y0, ST = 12, 600, 60, 100, 88
layers = [
    ("클라이언트", ["클러스터 Pod", "외부 클라이언트"], INFO),
    ("Service", ["10.96.72.137:80", "NodePort :31478", "192.168.9.1:80"], INFO),
    ("KPR eBPF 맵", ["서비스 맵 조회", "백엔드 선택"], ACC),
    ("백엔드 Pod", ["httpd Pod", "httpd Pod"], OK),
]
for i, (nm, chips, c) in enumerate(layers):
    y = Y0 + i * ST
    if c == ACC:
        d.tone(LX, y, LW, LH, ACC, r=6, op="14", sw=1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, c, 1.0)
    d.t(LX + 14, y + 36, nm, 13, c, KR, "start", 600)
    n = len(chips)
    cw = 140
    x = LX + 160
    for ch in chips:
        d.chip(x + cw / 2, y + 30, ch, c, size=11, pad=8)
        x += cw + 10
    if i < len(layers) - 1:
        d.arrow([(LX + LW / 2, y + LH), (LX + LW / 2, y + ST)], MUTED, "ar", 1.5)

RX, RW = 664, 244
d.box(RX, Y0, RW, LH, PAPER2, SOFT, 1.0)
d.t(RX + RW / 2, Y0 + 26, "BGP · L2 Announcements", 12, INK, MONO, "middle", 600)
d.t(RX + RW / 2, Y0 + 46, "외부에 IP 광고", 12, MUTED, KR)
d.arrow([(RX, Y0 + 30), (LX + LW, Y0 + 30)], SOFT, "soft", 1.4, "4 4")

y1 = Y0 + ST
d.box(RX, y1, RW, LH, PAPER2, WARN, 1.0)
d.t(RX + RW / 2, y1 + 26, "LB IPAM", 12, INK, MONO, "middle", 600)
d.t(RX + RW / 2, y1 + 46, "풀에서 외부 IP 배정", 12, MUTED, KR)
d.arrow([(RX, y1 + 30), (LX + LW, y1 + 30)], WARN, "warn", 1.5)

y2 = Y0 + 2 * ST
d.box(RX, y2, RW, LH, PAPER2, ACC, 1.0)
d.t(RX + RW / 2, y2 + 26, "cilium-agent", 12, INK, MONO, "middle", 600)
d.t(RX + RW / 2, y2 + 46, "API 서버를 보며 맵 갱신", 12, MUTED, KR)
d.arrow([(RX, y2 + 30), (LX + LW, y2 + 30)], ACC, "acc", 1.5)

d.legend(Y0 + 4 * ST + 8, [("서비스 계층", INFO), ("eBPF 맵", ACC), ("IP 배정", WARN), ("백엔드", OK)])
d.save("06-01.chapter-overview.svg")
