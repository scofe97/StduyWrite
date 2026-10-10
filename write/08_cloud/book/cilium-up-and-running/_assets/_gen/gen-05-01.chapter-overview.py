# 타입 스펙: type-dp-security-matrix — 행 = 패킷 경로 셋, 열 = 거치는 장치·추가 헤더·필요한 설정의 비교 행렬. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법을 가진 이 타입으로 바꿨다. 셀 1개만 focal.
# 사실 출처: Cilium Up and Running 5장 cil5.txt 줄 260-277(bpftool), 399-408(native 설정), 620-651(VXLAN 경로), 723-729(50바이트) / docs.cilium.io v1.20.2 network/concepts/routing(tunnel 기본값·포트)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 424
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 200, 12, 204, 16
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 52, 60
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]

d = D(W, H, "CILIUM UP AND RUNNING · 05-01", "세 경로가 거치는 장치와 추가 헤더",
      "같은 노드는 veth 와 eBPF 로 넘기고, 다른 노드는 경로표나 터널로 잇는다", "같은 노드는 veth 와 eBPF 로 넘기고, 다른 노드는 경로표나 터널로 잇는다")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "경로", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "path", 11, MUTED, MONO)
for j, (nm, code) in enumerate([("거치는 장치", "device"), ("추가 헤더", "overhead"), ("필요한 설정", "helm value")]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, code, 11, MUTED, MONO)

rows = [
    ("같은 노드", "intranode", [
        ("lxc* → lxc*", "cil_from_container", None),
        ("없음", "", OK),
        ("기본 설치", "", None)]),
    ("다른 노드 · native", "routing", [
        ("lxc* → eth0", "호스트 경로표", None),
        ("없음", "", OK),
        ("routingMode: native", "ipv4NativeRoutingCIDR", None)]),
    ("다른 노드 · 터널", "overlay", [
        ("lxc* → cilium_vxlan", "경로는 cilium_host", None),
        ("+50바이트", "UDP 8472 · VNI", "focal"),
        ("tunnelProtocol: vxlan", "routingMode: tunnel (기본)", None)]),
]

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 31, name, 13, INK, KR, "start", 600)
    for j, (val, sub, tone) in enumerate(cells):
        x = RX[j]
        if tone == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
        elif tone == OK:
            d.tone(x, y, ROLE_W, ROW_H, OK, r=4, op="10", sw=0.9)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
        fam = KR if any("가" <= c <= "힣" for c in val) else MONO
        col = ACC if tone == "focal" else (OK if tone == OK else INK)
        if sub:
            d.t(x + ROLE_W / 2, y + 22, val, 12, col, fam, "middle", 600)
            sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
            d.t(x + ROLE_W / 2, y + 41, sub, 12, MUTED, sfam)
        else:
            d.t(x + ROLE_W / 2, y + 31, val, 12, col, fam, "middle", 600)

LEG_Y = ROW_Y0 + 2 * STRIDE + ROW_H + 24
d.legend(LEG_Y, [("추가 헤더 없음", OK), ("터널 헤더", ACC)])
d.save("05-01.chapter-overview.svg")
