# 타입 스펙: type-dp-security-matrix — 행 = 헤더 속성 다섯, 열 = VXLAN·Geneve 의 비교 행렬. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법을 가진 이 타입으로 바꿨다. 셀 1개만 focal(Geneve 가 옵션에 싣는 것).
# 사실 출처: Cilium Up and Running 5장 cil5.txt 줄 912-952(포트 8472·6081, Geneve 고정 필드, VNI 0x382e=14382). docs.cilium.io v1.20.2 kubeproxy-free(DSR with Geneve)·network/concepts/routing(tunnel-port), pkg/defaults/node.go(cilium_geneve)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 208, 12, 312, 16
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 44, 52
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(2)]

d = D(W, H, "CILIUM UP AND RUNNING · 05-01 §4", "VXLAN 과 Geneve 의 헤더 비교",
      "같은 UDP 터널이고 VNI 에 신원을 싣는다 — 다른 점은 포트와 옵션 필드", "같은 UDP 터널이고 VNI 에 신원을 싣는다 — 다른 점은 포트와 옵션 필드")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "속성", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "field", 11, MUTED, MONO)
for j, (nm, code) in enumerate([("VXLAN", "cilium_vxlan"), ("Geneve", "cilium_geneve")]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, MONO, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, code, 11, MUTED, MONO)

rows = [
    ("UDP 포트", "tunnelPort", [("8472", INFO), ("6081", INFO)]),
    ("옵션 필드", "TLV", [("없음", None), ("있음 · Opt Len", None)]),
    ("VNI 의 쓰임", "24비트", [("출발 Pod 신원", None), ("신원 14382 (0x382e)", None)]),
    ("고정 필드", "", [("flags I", None), ("ver 0 · flags 0x00 · proto 0x6558", None)]),
    ("옵션에 싣는 것", "", [("해당 없음", None), ("DSR 서비스 IP · 포트", "focal")]),
]
for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 27, name, 13, INK, KR, "start", 600)
    if hint:
        d.t(LP + COMP_W - 12, y + 27, hint, 12, MUTED, KR if any('가' <= c <= '힣' for c in hint) else MONO, "end")
    for j, (val, tone) in enumerate(cells):
        x = RX[j]
        if tone == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
        elif tone == INFO:
            d.tone(x, y, ROLE_W, ROW_H, INFO, r=4, op="10", sw=0.9)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
        fam = KR if any("가" <= c <= "힣" for c in val) else MONO
        col = ACC if tone == "focal" else (INFO if tone == INFO else INK)
        d.t(x + ROLE_W / 2, y + 27, val, 12, col, fam, "middle", 600)

LEG_Y = ROW_Y0 + 4 * STRIDE + ROW_H + 24
d.legend(LEG_Y, [("포트", INFO), ("Geneve 만의 기능", ACC)])
d.save("05-01.vxlan-vs-geneve.svg")
