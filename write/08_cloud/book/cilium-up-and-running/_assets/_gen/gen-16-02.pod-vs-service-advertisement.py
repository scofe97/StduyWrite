# 타입 스펙: type-dp-security-matrix — 행 = PodCIDR 광고와 Service IP 광고, 열 = advertisementType · 광고 단위 · 클라이언트 목적지 · 에이전트 중단 때 대응 · IPv4 주소 소모 비교 행렬. 설치 목록에 comparison 타입이 없어 비교 행렬 문법을 가진 이 타입으로 선언했다. focal 은 1칸.
# 사실 출처: Cilium Up and Running 16장 cil16.txt 줄 703-727(Pod IP 변동·서비스 IP 안정·주소 공간) / docs.cilium.io v1.20 bgp-control-plane-configuration(PodCIDR·Service·/32·/128) · bgp-control-plane-operation Failure Scenarios(PodCIDR routes drain · Service routes ECMP 재해시)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 364
LP, LBL_W, GAP = 12, 116, 8
COL_WS = [136, 136, 144, 156, 128]
HDR_Y, HDR_H = 96, 48
ROW_Y0, ROW_H, STRIDE = 160, 60, 68
cols = [
    ("광고 종류", "advertisementType"),
    ("광고 단위", "prefix"),
    ("클라이언트 목적지", "destination"),
    ("에이전트 중단 때", "agent down"),
    ("IPv4 소모", "address space"),
]
rows = [
    ("Pod 대역", "PodCIDR", INFO, [
        ("PodCIDR", "노드에 할당된 대역", None),
        ("노드별 Pod 대역", "할당분만", None),
        ("바뀌는 Pod IP", "대상 직접 선택", WARN),
        ("Pod 접근 불가", "노드 drain 으로 이동", None),
        ("큼", "Pod 대역 노출", WARN)]),
    ("서비스 IP", "Service", INFO, [
        ("Service", "LoadBalancerIP 등", None),
        ("VIP 한 개씩", "/32 · /128", None),
        ("고정 VIP", "Cilium 이 Pod 분산", "focal"),
        ("연결 리셋 가능", "ECMP 재해시", None),
        ("작음", "서비스 대역만", OK)]),
]

x = LP
d = D(W, H, "CILIUM UP AND RUNNING · 16-02 §4", "Pod 대역 광고와 서비스 IP 광고 비교",
      "광고 대상이 바뀌는 주소인지 고정 주소인지에 따라 클라이언트와 주소 소모가 갈립니다",
      "BGP Control Plane 의 두 광고 종류")
d.box(LP, HDR_Y, LBL_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + LBL_W / 2, HDR_Y + 22, "광고 대상", 12, INK, KR, "middle", 600)
d.t(LP + LBL_W / 2, HDR_Y + 38, "target", 11, MUTED, MONO)
cx = LP + LBL_W + GAP
XS = []
for (t1, t2), w in zip(cols, COL_WS):
    XS.append(cx)
    d.box(cx, HDR_Y, w, HDR_H, PAPER2, SOFT, 1.0)
    d.t(cx + w / 2, HDR_Y + 22, t1, 12, INK, KR, "middle", 600)
    d.t(cx + w / 2, HDR_Y + 38, t2, 11, MUTED, MONO)
    cx += w + GAP

for i, (nm, code, col, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.tone(LP, y, LBL_W, ROW_H, col, r=6, op="14", sw=1.1)
    d.t(LP + LBL_W / 2, y + 26, nm, 13, col, KR, "middle", 600)
    d.t(LP + LBL_W / 2, y + 46, code, 11, MUTED, MONO)
    for j, (v1, v2, tone) in enumerate(cells):
        w, cx0 = COL_WS[j], XS[j]
        if tone == "focal":
            d.tone(cx0, y, w, ROW_H, ACC, r=4, op="14", sw=1.4)
        elif tone in (OK, WARN):
            d.tone(cx0, y, w, ROW_H, tone, r=4, op="10", sw=0.9)
        else:
            d.box(cx0, y, w, ROW_H, PAPER2, RULE, 0.7, 4)
        c1 = ACC if tone == "focal" else (tone if tone in (OK, WARN) else INK)
        d.t(cx0 + w / 2, y + 26, v1, 12, c1, KR if any("가" <= c <= "힣" for c in v1) else MONO, "middle", 600)
        d.t(cx0 + w / 2, y + 46, v2, 12, MUTED, KR if any("가" <= c <= "힣" for c in v2) else MONO)

d.legend(ROW_Y0 + 2 * STRIDE + 12, [("서비스 IP 의 핵심", ACC), ("부담이 큰 칸", WARN), ("부담이 작은 칸", OK), ("행 이름", INFO)])
d.save("16-02.pod-vs-service-advertisement.svg")
