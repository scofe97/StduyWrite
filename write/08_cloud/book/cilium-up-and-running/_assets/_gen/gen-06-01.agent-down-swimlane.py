# 타입 스펙: type-swimlane — 에이전트가 없는 동안과 복구 뒤에 같은 서비스로 보낸 요청의 결과 (배정 타입 중 swimlane)
# 사실 출처: 추출본 cil6.txt 줄 513-571(nodeSelector 패치·curl httpd·curl -m 2 시간 초과·복구 3/3)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 380
d = D(W, H, "CILIUM UP AND RUNNING · 06-01 §4", "에이전트가 없는 동안의 요청",
      "새 요청도 마지막 맵대로 통과하고 삭제된 백엔드가 뽑히면 시간 초과가 납니다",
      "nodeSelector foo=bar 로 에이전트를 내린 실험")

LBL_X, LBL_W, BODY_X, BODY_W, LANE_H, STRIDE, Y0 = 12, 132, 148, 760, 84, 100, 100
lanes = [("에이전트 없음", "foo=bar", WARN), ("에이전트 복구", "foo 제거", OK)]
for i, (nm, sub, c) in enumerate(lanes):
    y = Y0 + i * STRIDE
    d.box(LBL_X, y, LBL_W, LANE_H, PAPER2, RULE, 0.9)
    d.t(LBL_X + LBL_W / 2, y + 38, nm, 12, c, KR, "middle", 600)
    d.t(LBL_X + LBL_W / 2, y + 60, sub, 11, MUTED, MONO)
    d.box(BODY_X, y, BODY_W, LANE_H, PAPER2, RULE, 0.9)

SW, SH = 128, 58
XS = [164 + k * 148 for k in range(5)]
steps = [
    (0, 0, "DaemonSet", "DESIRED 0 · READY 0", WARN),
    (0, 1, "curl httpd", "It works!", OK),
    (0, 2, "Pod 삭제", "10.0.2.208", INFO),
    (0, 3, "curl -m 2", "timed out 2004ms", BAD),
    (1, 3, "DaemonSet", "DESIRED 3 · READY 3", OK),
    (1, 4, "맵 재조정", "낡은 항목 제거", OK),
]
pos = {}
for ln, k, t1, t2, c in steps:
    y = Y0 + ln * STRIDE + (LANE_H - SH) // 2
    x = XS[k]
    if c == BAD:
        d.tone(x, y, SW, SH, BAD, r=4, op="14", sw=1.4)
    else:
        d.box(x, y, SW, SH, PAPER, c, 1.0, 4)
    fam1 = MONO if t1[0].isascii() else KR
    d.t(x + SW / 2, y + 24, t1, 12, c, fam1, "middle", 600)
    d.t(x + SW / 2, y + 44, t2, 10 if t2[0].isascii() else 11, INK, MONO if t2[0].isascii() else KR)
    pos[(ln, k)] = (x, y)

def hy(ln): return Y0 + ln * STRIDE + LANE_H // 2
for k in range(3):
    d.arrow([(XS[k] + SW, hy(0)), (XS[k + 1], hy(0))], MUTED, "ar", 1.5)
# 4번째 상자(시간 초과)에서 복구 레인의 같은 열로 내려간 뒤 오른쪽 상자로 이어짐
x3 = XS[3] + SW // 2
d.arrow([(x3, Y0 + (LANE_H + SH) // 2), (x3, Y0 + STRIDE + (LANE_H - SH) // 2)], OK, "ok", 1.5)
d.arrow([(XS[3] + SW, hy(1)), (XS[4], hy(1))], OK, "ok", 1.5)

d.legend(Y0 + 2 * STRIDE + 8, [("에이전트 없음", WARN), ("요청 성공·복구", OK), ("백엔드 삭제", INFO), ("시간 초과", BAD)])
d.save("06-01.agent-down-swimlane.svg")
