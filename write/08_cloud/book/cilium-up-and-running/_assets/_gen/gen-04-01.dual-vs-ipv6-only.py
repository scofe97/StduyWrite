# 타입 스펙: type-dp-security-matrix — 듀얼 스택 Pod·Service 와 IPv6 전용 Pod·Service 의 주소·kind 설정·Cilium 값 차이 비교.
# 사실 출처: 추출본 cil4.txt 줄 899-914 · 949-969 · 1003-1019 · 1083-1094 · 1125-1134 · 1141-1161 · 1187-1203.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W = 920
LP, LBL_W, GAP = 12, 168, 12
COL_W = 344
HDR_Y, HDR_H, ROW_Y0, STRIDE, ROW_H = 96, 40, 148, 48, 40
cols = ["듀얼 스택", "IPv6 전용"]
rows = [
    ("Pod 주소", "10.244.1.117 · fd00:10:244:1::8204", "2001:db8:10:1::4d69"),
    ("Service IP", "10.96.181.159 · fd00:10:96::d4d5", "2001:db8:10:96::6f43"),
    ("kind 설정", "ipFamily: dual", "ipFamily: ipv6 · podSubnet · serviceSubnet"),
    ("Service 정책", "PreferDualStack", "SingleStack · IPv6"),
    ("Cilium 값", "ipv6.enabled=true", "ipv6.enabled · ipv4.enabled=false"),
]
rows_bottom = ROW_Y0 + (len(rows) - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 24
H = LEG_Y + 48
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §6", "듀얼 스택과 IPv6 전용 구성 비교",
      "주소는 둘에서 하나로 줄고 IPv4 를 끄는 값은 따로 지정해야 합니다",
      "행 = 항목 · 열 = 주소 계열")

def cx(j): return LP + LBL_W + GAP + j * (COL_W + GAP)

d.box(LP, HDR_Y, LBL_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL_W / 2, HDR_Y + 25, "항목", 12, INK, KR, "middle", 600)
for j, c in enumerate(cols):
    d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, RULE, 0.9, 6)
    d.t(cx(j) + COL_W / 2, HDR_Y + 25, c, 12, INK, KR, "middle", 600)

for i, (lab, a, b) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, LBL_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 12, y + 25, lab, 12, INK, KR, "start", 600)
    d.tone(cx(0), y, COL_W, ROW_H, INFO, r=4, op="12", sw=1.0)
    d.t(cx(0) + COL_W / 2, y + 25, a, 11, INFO, MONO, "middle")
    if i == len(rows) - 1:
        d.tone(cx(1), y, COL_W, ROW_H, ACC, r=4, op="12", sw=1.4)
        d.t(cx(1) + COL_W / 2, y + 25, b, 11, ACC, MONO, "middle", 600)
    else:
        d.tone(cx(1), y, COL_W, ROW_H, OK, r=4, op="12", sw=1.0)
        d.t(cx(1) + COL_W / 2, y + 25, b, 11, OK, MONO, "middle")

d.legend(LEG_Y, [("듀얼 스택", INFO), ("IPv6 전용", OK), ("빠뜨리면 IPv4 가 남는 값", ACC)])
d.save("04-01.dual-vs-ipv6-only.svg")
