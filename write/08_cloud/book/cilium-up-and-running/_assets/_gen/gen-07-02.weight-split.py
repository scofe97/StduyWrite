# 타입 스펙: type-dp-security-matrix — 행 = 가중치 구성 둘(50/50·99/1), 열 = echo-1·echo-2 의 weight 와 1,000번 요청 결과. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법을 가진 이 타입으로 바꿨다. 셀 1개만 focal.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 1007-1011(weight 50/50), 1047(517 echo-1), 1067(kubectl edit), 1081(990 echo-1). 의미: Gateway API v1.6.1 httproutes CRD weight 정의
import sys
sys.path.insert(0, ".")
from dd import D, ACC, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 336
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 188, 12, 160, 12
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 44, 52
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(4)]

d = D(W, H, "CILIUM UP AND RUNNING · 07-02 §4", "가중치와 1,000번 요청의 분배",
      "같은 /echo 요청 1,000번을 보낸 결과", "같은 /echo 요청 1,000번을 보낸 결과")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "가중치 구성", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "weight", 11, MUTED, MONO)
heads = [("echo-1", "weight"), ("echo-2", "weight"), ("echo-1", "응답 수"), ("echo-2", "응답 수")]
for j, (nm, sub) in enumerate(heads):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, MONO, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, sub, 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO)

rows = [("50 / 50", ["50", "50", "517", "483"], None), ("99 / 1", ["99", "1", "990", "10"], 3)]
for i, (name, vals, foc) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 27, name, 13, INK, MONO, "start", 600)
    for j, v in enumerate(vals):
        x = RX[j]
        if foc == j:
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
            col = ACC
        elif j < 2:
            d.tone(x, y, ROLE_W, ROW_H, INFO, r=4, op="10", sw=0.9)
            col = INFO
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
            col = INK
        d.t(x + ROLE_W / 2, y + 27, v, 13, col, MONO, "middle", 600)
d.legend(ROW_Y0 + 2 * STRIDE + 8, [("설정한 weight", INFO), ("카나리로 간 요청", ACC)])
d.save("07-02.weight-split.svg")
